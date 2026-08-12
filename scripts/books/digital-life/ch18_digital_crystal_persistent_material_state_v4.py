from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt

from tqdm import tqdm


# ============================================================================
# Chapter 18 — Can Experience Change the Material?
# ============================================================================

BASE_MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v4"
SCHEMA_VERSION = 4

Cell = Tuple[int, int]

HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)


# ============================================================================
# Frozen Digital Crystal v1 parameters
# ============================================================================

@dataclass(frozen=True)
class CrystalParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


# ============================================================================
# Chapter 18 experimental material-state extension
# ============================================================================

@dataclass(frozen=True)
class MaterialParams:
    """
    Chapter 18 v3 experimental material-state extension.

    A cell is either:
        occupied-normal
        occupied-modified

    Existing v1/v2 rules remain:
        - explicit pulse can write modified state to occupied boundary cells;
        - modified state persists irreversibly;
        - modified occupied neighbours bias later frontier attachment.

    V3 adds exactly ONE new local mechanism:
        - a newly attached cell may inherit modified state when at least one of
          its occupied neighbours was already modified before the attachment.

    This is local propagation of material state, not a global memory register,
    history list, decoder, learned parameter, target morphology, or agent state.
    """
    write_probability: float = 0.20
    modified_neighbor_gain: float = 0.30
    inheritance_probability: float = 0.50


@dataclass
class CrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    attachments_by_step: List[int]
    population_by_step: List[int]


@dataclass
class MaterialCrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    modified: Set[Cell]
    step: int
    stream_seed: int
    attachments_by_step: List[int]
    population_by_step: List[int]
    modified_count_by_step: List[int]


# ============================================================================
# Geometry and frozen growth mechanics
# ============================================================================

def neighbors(cell: Cell) -> Iterable[Cell]:
    q, r = cell
    for dq, dr in HEX_DIRECTIONS:
        yield q + dq, r + dr


def hex_distance(cell: Cell) -> int:
    q, r = cell
    s = -q - r
    return max(abs(q), abs(r), abs(s))


def axial_to_xy(cell: Cell) -> Tuple[float, float]:
    q, r = cell
    return math.sqrt(3.0) * (q + r / 2.0), 1.5 * r


def logistic_scalar(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def local_exposure_angle(cell: Cell, occupied: Set[Cell]) -> float:
    x, y = axial_to_xy(cell)
    vx = 0.0
    vy = 0.0
    count = 0

    for nb in neighbors(cell):
        if nb in occupied:
            nx, ny = axial_to_xy(nb)
            vx += x - nx
            vy += y - ny
            count += 1

    if count == 0 or abs(vx) + abs(vy) < 1e-12:
        return 0.0
    return math.atan2(vy, vx)


def hex_disk_capacity(radius: int) -> int:
    return 1 + 3 * radius * (radius + 1)


def capacity_fraction_occupied(occupied: Set[Cell], radius: int) -> float:
    return len(occupied) / float(hex_disk_capacity(radius))


def normalize_signal(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if len(x) == 0:
        return x

    x = x - float(np.mean(x))
    m = float(np.max(np.abs(x)))
    if m > 0:
        x = x / m
    return np.clip(x, -1.0, 1.0)


def make_environment(steps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)

    p1 = rng.uniform(11.0, 19.0)
    p2 = rng.uniform(23.0, 37.0)
    ph1 = rng.uniform(0.0, 2 * np.pi)
    ph2 = rng.uniform(0.0, 2 * np.pi)

    deterministic = (
        0.55 * np.sin((2 * np.pi * t / p1) + ph1)
        + 0.25 * np.sin((2 * np.pi * t / p2) + ph2)
    )

    drift = 0.18 * normalize_signal(
        np.cumsum(rng.normal(0.0, 0.10, size=steps))
    )
    noise = rng.normal(0.0, 0.08, size=steps)

    return normalize_signal(deterministic + drift + noise)


# ============================================================================
# Frozen canonical sequential-RNG implementation
# ============================================================================

def initial_state(seed: int) -> CrystalState:
    rng = random.Random(seed)
    return CrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        step=0,
        rng_state=rng.getstate(),
        attachments_by_step=[1],
        population_by_step=[1],
    )


def advance_one_step(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: CrystalParams,
) -> Tuple[CrystalState, int]:
    """
    Frozen Digital Crystal v1 implementation.
    """
    rng = random.Random()
    rng.setstate(state.rng_state)

    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions: List[Cell] = []

    for cell in sorted(frontier):
        n = sum(nb in occupied for nb in neighbors(cell))
        theta = local_exposure_angle(cell, occupied)
        phase = params.signal_phase_gain * float(input_value)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)

        score = (
            params.base_bias
            + params.neighbor_gain * n
            + params.signal_rate_gain * float(input_value)
            + params.anisotropy_gain * anisotropy
            - params.crowding_penalty * crowding
        )

        if rng.random() < logistic_scalar(score):
            additions.append(cell)

    next_step = state.step + 1
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    return CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=next_step,
        rng_state=rng.getstate(),
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
    ), len(additions)


# ============================================================================
# Cell-keyed CRN runner retained from Chapter 17
# ============================================================================

def cell_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Stable U[0,1) draw keyed by (seed, absolute step, cell).

    This is the Chapter 17 counterfactual coupling. It keeps corresponding
    cell-step opportunities aligned across branches.
    """
    q, r = cell
    payload = f"{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def material_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Separate deterministic random channel for material-state writing.

    The 'material:' namespace prevents the material write decision from
    consuming or correlating with the frozen CRN growth draw.
    """
    q, r = cell
    payload = (
        f"material:{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}"
    ).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)



def inheritance_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Separate deterministic random channel for local material inheritance.

    The namespace is disjoint from both growth CRN draws and pulse-write draws.
    """
    q, r = cell
    payload = (
        f"inheritance:{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}"
    ).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def initial_material_state(stream_seed: int) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        modified=set(),
        step=0,
        stream_seed=int(stream_seed),
        attachments_by_step=[1],
        population_by_step=[1],
        modified_count_by_step=[0],
    )


def clone_material_state(state: MaterialCrystalState) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def erase_material_labels(state: MaterialCrystalState) -> MaterialCrystalState:
    """
    Causal ablation: preserve visible morphology, birth times, step, stream seed,
    and execution history while deleting only the experimental material state.
    """
    out = clone_material_state(state)
    out.modified = set()
    out.modified_count_by_step = list(out.modified_count_by_step)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = 0
    return out


def advance_one_step_material(
    state: MaterialCrystalState,
    input_value: float,
    pulse_bit: int,
    max_radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> Tuple[MaterialCrystalState, int, int]:
    """
    Chapter 18 v3 material-state growth step.

    Ordering:

      1. growth decisions use material state existing BEFORE this step;
      2. newly attached cells are added;
      3. new cells adjacent to pre-existing modified material may inherit state;
      4. if pulse_bit == 1, occupied boundary material may also be directly written;
      5. inherited/written state affects growth only on later steps.

    This keeps the causal ordering explicit and prevents same-update feedback.
    """
    occupied_before = set(state.occupied)
    modified_before = set(state.modified)

    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)
    modified = set(state.modified)

    frontier: Set[Cell] = set()
    for cell in occupied_before:
        for nb in neighbors(cell):
            if nb not in occupied_before and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions: List[Cell] = []
    next_step = state.step + 1

    for cell in sorted(frontier):
        n = sum(nb in occupied_before for nb in neighbors(cell))
        modified_n = sum(nb in modified_before for nb in neighbors(cell))

        theta = local_exposure_angle(cell, occupied_before)
        phase = crystal_params.signal_phase_gain * float(input_value)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)

        score = (
            crystal_params.base_bias
            + crystal_params.neighbor_gain * n
            + crystal_params.signal_rate_gain * float(input_value)
            + crystal_params.anisotropy_gain * anisotropy
            - crystal_params.crowding_penalty * crowding
            + material_params.modified_neighbor_gain * modified_n
        )

        if (
            cell_uniform(state.stream_seed, next_step, cell)
            < logistic_scalar(score)
        ):
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    newly_inherited = 0

    # V3 mechanism: new material may inherit the local state from material
    # already modified before this growth step.
    if material_params.inheritance_probability > 0:
        for cell in additions:
            modified_n = sum(
                nb in modified_before for nb in neighbors(cell)
            )
            if modified_n <= 0:
                continue

            if (
                inheritance_uniform(state.stream_seed, next_step, cell)
                < material_params.inheritance_probability
            ):
                modified.add(cell)
                newly_inherited += 1

    newly_written = 0

    if int(pulse_bit) != 0:
        # Direct write remains identical in spirit to v1/v2: the pulse writes
        # only to occupied boundary cells.
        candidates: List[Cell] = []
        for cell in sorted(occupied):
            degree = sum(nb in occupied for nb in neighbors(cell))
            if degree < 6:
                candidates.append(cell)

        for cell in candidates:
            if cell in modified:
                continue

            if (
                material_uniform(state.stream_seed, next_step, cell)
                < material_params.write_probability
            ):
                modified.add(cell)
                newly_written += 1

    out = MaterialCrystalState(
        occupied=occupied,
        birth_time=birth_time,
        modified=modified,
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
        modified_count_by_step=state.modified_count_by_step + [len(modified)],
    )

    return out, len(additions), newly_written + newly_inherited

def warm_material_checkpoint(
    env: np.ndarray,
    warmup_steps: int,
    stream_seed: int,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> MaterialCrystalState:
    state = initial_material_state(stream_seed)

    for t in range(warmup_steps):
        state, _, _ = advance_one_step_material(
            state=state,
            input_value=float(env[t]),
            pulse_bit=0,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )

    return state


def advance_material_sequence(
    checkpoint: MaterialCrystalState,
    env_future: np.ndarray,
    pulse_bits: Sequence[int],
    message_gain: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    observation_steps: Sequence[int],
    guard: float,
) -> Dict[int, MaterialCrystalState]:
    state = clone_material_state(checkpoint)
    wanted = set(map(int, observation_steps))
    observations: Dict[int, MaterialCrystalState] = {}

    for i in range(max(wanted)):
        bit = int(pulse_bits[i]) if i < len(pulse_bits) else 0
        forcing = float(env_future[i]) + message_gain * bit

        state, _, _ = advance_one_step_material(
            state=state,
            input_value=forcing,
            pulse_bit=bit,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )

        frac = capacity_fraction_occupied(state.occupied, radius)
        if frac >= guard:
            raise RuntimeError(
                f"Saturation guard reached at elapsed step {i + 1}: "
                f"{frac:.3f} >= {guard:.3f}"
            )

        elapsed = i + 1
        if elapsed in wanted:
            observations[elapsed] = clone_material_state(state)

    return observations


# ============================================================================
# Measurement model
# ============================================================================

FEATURE_NAMES = [
    "population_fraction",
    "max_radius_fraction",
    "mean_radius_fraction",
    "std_radius_fraction",
    "centroid_x_scaled",
    "centroid_y_scaled",
    "cov_trace_scaled",
    "cov_anisotropy",
    "boundary_fraction",
    "mean_degree",
    "degree_1",
    "degree_2",
    "degree_3",
    "degree_4",
    "degree_5",
    "degree_6",
    "sector_0",
    "sector_1",
    "sector_2",
    "sector_3",
    "sector_4",
    "sector_5",
    "harmonic6_cos",
    "harmonic6_sin",
]


def morphology_features_from_occupied(
    occupied: Set[Cell],
    radius: int,
) -> np.ndarray:
    occ = occupied
    xy = np.asarray([axial_to_xy(c) for c in occ], dtype=float)
    rs = np.asarray([hex_distance(c) for c in occ], dtype=float)

    centroid = np.mean(xy, axis=0)
    centered = xy - centroid

    if len(xy) >= 2:
        cov = np.cov(centered.T, bias=True)
        eig = np.sort(np.maximum(np.linalg.eigvalsh(cov), 0.0))
        cov_trace = float(np.sum(eig))
        cov_aniso = float(
            (eig[-1] - eig[0]) / max(1e-12, eig[-1] + eig[0])
        )
    else:
        cov_trace = 0.0
        cov_aniso = 0.0

    degrees = np.asarray(
        [sum(nb in occ for nb in neighbors(c)) for c in occ],
        dtype=int,
    )
    boundary_fraction = float(np.mean(degrees < 6))
    degree_fracs = [float(np.mean(degrees == k)) for k in range(1, 7)]

    angles = np.arctan2(xy[:, 1], xy[:, 0])
    sector_idx = ((angles + np.pi) / (2 * np.pi) * 6).astype(int) % 6
    sectors = [float(np.mean(sector_idx == k)) for k in range(6)]
    harmonic6 = np.mean(np.exp(1j * 6.0 * angles))

    scale_xy = max(1.0, 1.5 * radius)
    scale_cov = max(1.0, scale_xy * scale_xy)

    return np.asarray([
        len(occ) / float(hex_disk_capacity(radius)),
        float(np.max(rs)) / max(1.0, radius),
        float(np.mean(rs)) / max(1.0, radius),
        float(np.std(rs)) / max(1.0, radius),
        float(centroid[0]) / scale_xy,
        float(centroid[1]) / scale_xy,
        cov_trace / scale_cov,
        cov_aniso,
        boundary_fraction,
        float(np.mean(degrees)),
        *degree_fracs,
        *sectors,
        float(np.real(harmonic6)),
        float(np.imag(harmonic6)),
    ], dtype=float)


def normalized_symmetric_difference(a: Set[Cell], b: Set[Cell]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a ^ b) / float(len(union))


def pooled_feature_scale(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    pooled = np.vstack([X, Y])
    sd = np.std(pooled, axis=0)
    return np.where(sd < 1e-12, 1.0, sd)


def paired_standardized_deltas(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    if X.shape != Y.shape:
        raise ValueError("Paired statistics require equal shapes.")
    return (X - Y) / pooled_feature_scale(X, Y)


def stat_paired_ridge_hotelling(
    X: np.ndarray,
    Y: np.ndarray,
    ridge_fraction: float = 0.25,
) -> float:
    D = paired_standardized_deltas(X, Y)
    mean = np.mean(D, axis=0)

    if len(D) <= 1:
        return float(mean @ mean)

    cov = np.cov(D, rowvar=False, bias=True)
    diag_scale = float(np.mean(np.diag(cov)))
    ridge = max(1e-8, ridge_fraction * max(diag_scale, 1e-8))
    reg = cov + ridge * np.eye(cov.shape[0])
    inv = np.linalg.pinv(reg)

    return float(mean @ inv @ mean)


def paired_ridge_test(
    X: np.ndarray,
    Y: np.ndarray,
    permutations: int,
    seed: int,
) -> dict:
    if X.shape != Y.shape:
        raise ValueError("Paired test requires equal paired shapes.")

    observed = stat_paired_ridge_hotelling(X, Y)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X)).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = stat_paired_ridge_hotelling(Xp, Yp)

    p = (1 + float(np.sum(null >= observed))) / (permutations + 1)

    return {
        "statistic": float(observed),
        "p_value": float(p),
        "permutations": int(permutations),
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
    }


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    x = np.asarray(values, dtype=float)

    if len(x) == 0:
        return {"n": 0}

    rng = np.random.default_rng(seed)
    means = np.empty(reps, dtype=float)

    for i in range(reps):
        sample = x[rng.integers(0, len(x), size=len(x))]
        means[i] = np.mean(sample)

    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "std": float(np.std(x)),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def response_delta(
    pulse_state: MaterialCrystalState,
    no_pulse_state: MaterialCrystalState,
    radius: int,
) -> np.ndarray:
    return (
        morphology_features_from_occupied(pulse_state.occupied, radius)
        - morphology_features_from_occupied(no_pulse_state.occupied, radius)
    )


def frontier_cells(occupied: Set[Cell], radius: int) -> Set[Cell]:
    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= radius:
                frontier.add(nb)
    return frontier


def material_accessibility_metrics(
    state: MaterialCrystalState,
    radius: int,
) -> dict:
    """
    Measure whether persistent modified material remains reachable by the active
    growth frontier.

    Persistent state is dynamically accessible only if current frontier cells
    have at least one modified occupied neighbour.
    """
    frontier = frontier_cells(state.occupied, radius)

    modified_boundary = []
    for cell in state.modified:
        degree = sum(nb in state.occupied for nb in neighbors(cell))
        if degree < 6:
            modified_boundary.append(cell)

    exposed_frontier = []
    modified_neighbor_counts = []

    for cell in frontier:
        m = sum(nb in state.modified for nb in neighbors(cell))
        if m > 0:
            exposed_frontier.append(cell)
            modified_neighbor_counts.append(m)

    frontier_n = len(frontier)
    exposed_n = len(exposed_frontier)

    return {
        "modified_count": int(len(state.modified)),
        "modified_boundary_count": int(len(modified_boundary)),
        "frontier_count": int(frontier_n),
        "frontier_cells_with_modified_neighbor": int(exposed_n),
        "frontier_exposed_fraction": (
            float(exposed_n / frontier_n) if frontier_n else 0.0
        ),
        "mean_modified_neighbors_among_exposed_frontier": (
            float(np.mean(modified_neighbor_counts))
            if modified_neighbor_counts
            else 0.0
        ),
        "max_modified_neighbors_on_frontier": (
            int(max(modified_neighbor_counts))
            if modified_neighbor_counts
            else 0
        ),
    }


def continue_material_no_pulse(
    checkpoint: MaterialCrystalState,
    env_future: np.ndarray,
    steps: int,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    guard: float,
) -> MaterialCrystalState:
    state = clone_material_state(checkpoint)
    for i in range(steps):
        state, _, _ = advance_one_step_material(
            state=state,
            input_value=float(env_future[i]),
            pulse_bit=0,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )
        frac = capacity_fraction_occupied(state.occupied, radius)
        if frac >= guard:
            raise RuntimeError(
                f"Saturation guard reached during no-pulse continuation at "
                f"step {i+1}: {frac:.3f} >= {guard:.3f}"
            )
    return state


def frontier_cell_growth_probability(
    state: MaterialCrystalState,
    cell: Cell,
    input_value: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    include_material_bias: bool,
) -> float:
    """
    Compute the attachment probability for one current frontier cell.

    The only difference between retained and erased probability is whether the
    modified-neighbour term is included. Geometry and external forcing are held
    fixed.
    """
    if cell in state.occupied:
        raise ValueError("Audit cell must be unoccupied frontier material.")
    if hex_distance(cell) > radius:
        raise ValueError("Audit cell outside radius.")

    occupied = state.occupied
    modified = state.modified

    n = sum(nb in occupied for nb in neighbors(cell))
    modified_n = sum(nb in modified for nb in neighbors(cell))

    theta = local_exposure_angle(cell, occupied)
    phase = crystal_params.signal_phase_gain * float(input_value)
    anisotropy = math.cos(6.0 * theta + phase)
    crowding = max(0, n - 2)

    score = (
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain * float(input_value)
        + crystal_params.anisotropy_gain * anisotropy
        - crystal_params.crowding_penalty * crowding
    )

    if include_material_bias:
        score += material_params.modified_neighbor_gain * modified_n

    return logistic_scalar(score)


def frontier_material_causal_audit(
    state: MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> dict:
    """
    Direct mechanistic audit at the active frontier.

    For every frontier cell:
        p_erased   = attachment probability with material term removed
        p_retained = attachment probability with material term retained
        delta_p    = p_retained - p_erased

    With keyed CRN, a realized causal flip occurs when:
        p_erased <= u < p_retained

    That cell attaches in the retained-material world but not in the erased
    world under the same stochastic opportunity.
    """
    frontier = sorted(frontier_cells(state.occupied, radius))
    next_step = state.step + 1

    exposed = 0
    delta_ps = []
    realized_flips = 0
    realized_flip_cells = []

    for cell in frontier:
        modified_n = sum(nb in state.modified for nb in neighbors(cell))
        if modified_n <= 0:
            continue

        exposed += 1

        p_erased = frontier_cell_growth_probability(
            state, cell, input_value, radius,
            crystal_params, material_params,
            include_material_bias=False,
        )
        p_retained = frontier_cell_growth_probability(
            state, cell, input_value, radius,
            crystal_params, material_params,
            include_material_bias=True,
        )

        delta = float(p_retained - p_erased)
        delta_ps.append(delta)

        u = cell_uniform(state.stream_seed, next_step, cell)
        if p_erased <= u < p_retained:
            realized_flips += 1
            realized_flip_cells.append(cell)

    frontier_n = len(frontier)

    return {
        "frontier_count": int(frontier_n),
        "exposed_frontier_count": int(exposed),
        "exposed_frontier_fraction": (
            float(exposed / frontier_n) if frontier_n else 0.0
        ),
        "sum_delta_p": float(np.sum(delta_ps)) if delta_ps else 0.0,
        "mean_delta_p_exposed": (
            float(np.mean(delta_ps)) if delta_ps else 0.0
        ),
        "max_delta_p_exposed": (
            float(np.max(delta_ps)) if delta_ps else 0.0
        ),
        "realized_causal_flips": int(realized_flips),
        "realized_flip_fraction_of_exposed": (
            float(realized_flips / exposed) if exposed else 0.0
        ),
        "realized_flip_cells": [
            [int(q), int(r)] for q, r in realized_flip_cells
        ],
    }


def propagation_lifetime_from_summary(
    summary_by_step: dict,
    steps: Sequence[int],
) -> dict:
    """
    Describe how long frontier exposure remains visible at the ensemble level.

    This is descriptive. It does not infer a mathematical phase transition from
    the five-point inheritance sweep.
    """
    positive_steps = []
    for t in steps:
        mean_contact = summary_by_step[str(t)][
            "frontier_cells_with_modified_neighbor"
        ]["mean"]
        if mean_contact > 0:
            positive_steps.append(int(t))

    return {
        "last_observed_step_with_positive_mean_frontier_contact": (
            max(positive_steps) if positive_steps else None
        ),
        "positive_contact_observed_through_final_step": bool(
            positive_steps and max(positive_steps) == max(steps)
        ),
    }


# ============================================================================
# Experiment profiles
# ============================================================================

PROFILES = {
    "quick": {
        "groups": 40,
        "radius": 64,
        "warmup_steps": 14,

        # Frozen initial experience/write mechanism.
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,

        # Mechanistic sweep. This is characterization, not model selection.
        "inheritance_sweep": [0.00, 0.25, 0.50, 0.75, 1.00],

        # Observe material accessibility over time for each inheritance regime.
        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],

        # Direct cell-level causal audit at late checkpoints.
        "cell_audit_steps": [8, 10, 12, 14, 18],

        # A late whole-crystal ablation remains secondary corroboration only.
        "late_ablation_step": 14,
        "late_ablation_followup": 4,

        "permutations": 1500,
        "bootstrap_reps": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 80,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "inheritance_sweep": [0.00, 0.25, 0.50, 0.75, 1.00],
        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "cell_audit_steps": [8, 10, 12, 14, 18],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "permutations": 3000,
        "bootstrap_reps": 2000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 160,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "inheritance_sweep": [0.00, 0.25, 0.50, 0.75, 1.00],
        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "cell_audit_steps": [8, 10, 12, 14, 18],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "permutations": 5000,
        "bootstrap_reps": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
}


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections: List[str] = []

    def json(self, name: str, payload):
        (self.root / name).write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    def stage(self, filename: str, title: str, body: str):
        text = f"# {title}\n\n{body.strip()}\n"
        (self.root / filename).write_text(text, encoding="utf-8")
        self.sections.append(text)

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch18-persistent-material-state-v4-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V4 Propagation Mechanics)\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
        )
        path.write_text(
            header + "\n\n".join(self.sections),
            encoding="utf-8",
        )
        return path


# ============================================================================
# Stage 0 — extension audit
# ============================================================================

def stage_0_extension_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Audit reproducibility and the limiting cases of the inheritance mechanism.

    This stage does not select an inheritance probability.
    """
    radius = profile["radius"]
    steps = profile["warmup_steps"] + 10
    env = make_environment(steps, seed + 1)

    exact_by_probability = {}

    for p_inherit in profile["inheritance_sweep"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            inheritance_probability=float(p_inherit),
        )

        a = initial_material_state(seed + 100 + int(round(1000 * p_inherit)))
        b = initial_material_state(seed + 100 + int(round(1000 * p_inherit)))

        for t in range(steps):
            bit = int(t == profile["experience_pulse_step"])
            forcing = float(env[t]) + profile["message_gain"] * bit

            a, _, _ = advance_one_step_material(
                a, forcing, bit, radius, crystal_params, mp
            )
            b, _, _ = advance_one_step_material(
                b, forcing, bit, radius, crystal_params, mp
            )

        exact_by_probability[str(p_inherit)] = bool(
            a.occupied == b.occupied
            and a.modified == b.modified
            and a.birth_time == b.birth_time
            and a.attachments_by_step == b.attachments_by_step
        )

    all_exact = all(exact_by_probability.values())

    # Critical limiting case: p_inherit=0 means no new attachment can acquire
    # material state through inheritance.
    p0 = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        inheritance_probability=0.0,
    )

    result = {
        "role": "V4 MECHANISM CHARACTERIZATION AUDIT",
        "canonical_model_modified": False,
        "inheritance_sweep": list(profile["inheritance_sweep"]),
        "exact_reproducibility_by_inheritance_probability": exact_by_probability,
        "all_sweep_regimes_exactly_reproducible": all_exact,
        "zero_inheritance_limiting_case": {
            "inheritance_probability": p0.inheritance_probability,
            "interpretation": (
                "At p=0, material may still be written by the original pulse and "
                "affect nearby growth, but no newly attached cell inherits state."
            ),
        },
        "scientific_role": (
            "Characterize accessibility and direct causal leverage across a "
            "predeclared inheritance sweep; do not select the best regime by "
            "significance."
        ),
    }

    if not all_exact:
        raise RuntimeError("V4 reproducibility audit failed.")

    reporter.json("stage-00-v4-audit.json", result)
    reporter.stage(
        "stage-00-v4-audit.md",
        "Stage 0 — V4 Mechanism Characterization Audit",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def run_experienced_trajectory_v4(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
    max_elapsed: int,
) -> Tuple[Dict[int, MaterialCrystalState], np.ndarray]:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]

    total = warmup + max_elapsed + 5
    gseed = seed + 100_000 + group_index * 1009
    env = make_environment(total, gseed + 1)

    state = warm_material_checkpoint(
        env, warmup, gseed + 2, radius,
        crystal_params, material_params,
    )

    future = env[warmup:]
    out = {}

    for i in range(max_elapsed):
        bit = int(i == profile["experience_pulse_step"])
        forcing = float(future[i]) + profile["message_gain"] * bit
        state, _, _ = advance_one_step_material(
            state, forcing, bit, radius,
            crystal_params, material_params,
        )
        out[i + 1] = clone_material_state(state)

    return out, future


def stage_1_inheritance_sweep_accessibility(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    """
    Characterize how inheritance probability changes material-frontier contact.

    No p-value is used to choose a preferred inheritance probability.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    steps = profile["observation_steps"]
    max_elapsed = max(steps)

    sweep_results = {}

    for p_inherit in profile["inheritance_sweep"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            inheritance_probability=float(p_inherit),
        )

        metrics = {
            t: {
                "modified_count": [],
                "modified_boundary_count": [],
                "frontier_cells_with_modified_neighbor": [],
                "frontier_exposed_fraction": [],
            }
            for t in steps
        }

        for g in tqdm(
            range(groups),
            desc=f"Stage 1 inheritance={p_inherit:.2f}",
        ):
            traj, _ = run_experienced_trajectory_v4(
                profile, crystal_params, mp,
                seed + int(round(10000 * p_inherit)), g, max_elapsed,
            )

            for t in steps:
                m = material_accessibility_metrics(traj[t], radius)
                metrics[t]["modified_count"].append(m["modified_count"])
                metrics[t]["modified_boundary_count"].append(
                    m["modified_boundary_count"]
                )
                metrics[t]["frontier_cells_with_modified_neighbor"].append(
                    m["frontier_cells_with_modified_neighbor"]
                )
                metrics[t]["frontier_exposed_fraction"].append(
                    m["frontier_exposed_fraction"]
                )

        summary = {}
        for t in steps:
            summary[str(t)] = {
                key: bootstrap_mean_ci(
                    vals,
                    profile["bootstrap_reps"],
                    seed
                    + 210_000
                    + int(round(10000 * p_inherit))
                    + t * 100
                    + j,
                )
                for j, (key, vals) in enumerate(metrics[t].items())
            }

        sweep_results[str(p_inherit)] = {
            "inheritance_probability": float(p_inherit),
            "summary": summary,
            "lifetime": propagation_lifetime_from_summary(summary, steps),
        }

    result = {
        "groups_per_regime": groups,
        "inheritance_sweep": list(profile["inheritance_sweep"]),
        "observation_steps": steps,
        "results": sweep_results,
        "status": "MEASURED",
        "bounded_statement": (
            "The inheritance sweep characterizes how local propagation changes "
            "material abundance and contact with the active growth surface. It is "
            "not used to optimize or select a significance result."
        ),
    }

    reporter.json("stage-01-inheritance-sweep.json", result)
    reporter.stage(
        "stage-01-inheritance-sweep.md",
        "Stage 1 — How Does Local Inheritance Change Frontier Access?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    for p_inherit in profile["inheritance_sweep"]:
        s = sweep_results[str(p_inherit)]["summary"]
        ys = [
            s[str(t)]["frontier_exposed_fraction"]["mean"]
            for t in steps
        ]
        ax.plot(steps, ys, marker="o", label=f"p={p_inherit:.2f}")

    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("Propagation regimes across inheritance probability")
    ax.legend()
    fig.tight_layout()

    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v4-01-inheritance-sweep.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_2_cell_level_causal_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Directly measure how much causal leverage modified material has at the frontier.

    This separates:
        availability  -> how many frontier cells are exposed
        leverage      -> how much p(attach) changes for exposed cells
        realization   -> how many keyed random draws cross the retained/erased
                         attachment boundary
    """
    groups = profile["groups"]
    radius = profile["radius"]
    audit_steps = profile["cell_audit_steps"]
    max_elapsed = max(audit_steps)

    sweep_results = {}

    for p_inherit in profile["inheritance_sweep"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            inheritance_probability=float(p_inherit),
        )

        per_step = {
            t: {
                "exposed_frontier_count": [],
                "exposed_frontier_fraction": [],
                "sum_delta_p": [],
                "mean_delta_p_exposed": [],
                "max_delta_p_exposed": [],
                "realized_causal_flips": [],
                "realized_flip_fraction_of_exposed": [],
            }
            for t in audit_steps
        }

        for g in tqdm(
            range(groups),
            desc=f"Stage 2 cell audit p={p_inherit:.2f}",
        ):
            traj, future = run_experienced_trajectory_v4(
                profile, crystal_params, mp,
                seed + 300_000 + int(round(10000 * p_inherit)),
                g,
                max_elapsed,
            )

            for t in audit_steps:
                state = traj[t]

                # Input used for the NEXT update after checkpoint t.
                next_input = float(future[t])

                audit = frontier_material_causal_audit(
                    state,
                    next_input,
                    radius,
                    crystal_params,
                    mp,
                )

                for key in per_step[t]:
                    per_step[t][key].append(audit[key])

        summary = {}
        for t in audit_steps:
            summary[str(t)] = {
                key: bootstrap_mean_ci(
                    vals,
                    profile["bootstrap_reps"],
                    seed
                    + 310_000
                    + int(round(10000 * p_inherit))
                    + t * 100
                    + j,
                )
                for j, (key, vals) in enumerate(per_step[t].items())
            }

        sweep_results[str(p_inherit)] = {
            "inheritance_probability": float(p_inherit),
            "summary": summary,
        }

    result = {
        "groups_per_regime": groups,
        "inheritance_sweep": list(profile["inheritance_sweep"]),
        "audit_steps": audit_steps,
        "results": sweep_results,
        "status": "MEASURED",
        "causal_definition": (
            "For an exposed frontier cell under common random numbers, a realized "
            "causal flip occurs when p_erased <= u < p_retained."
        ),
        "bounded_statement": (
            "V4 separates frontier availability, probability leverage, and "
            "realized attachment flips caused by retained material state."
        ),
    }

    reporter.json("stage-02-cell-level-causal-audit.json", result)
    reporter.stage(
        "stage-02-cell-level-causal-audit.md",
        "Stage 2 — What Does Modified Material Do to a Frontier Cell?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_3_secondary_late_ablation(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Secondary corroboration at t=14 for every inheritance regime.

    The sweep is not ranked by these p-values.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    probe = profile["late_ablation_step"]
    followup = profile["late_ablation_followup"]

    results = {}

    for p_inherit in profile["inheritance_sweep"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            inheritance_probability=float(p_inherit),
        )

        Xs, Ys = [], []
        symdiff = []
        contact = []

        for g in tqdm(
            range(groups),
            desc=f"Stage 3 late ablation p={p_inherit:.2f}",
        ):
            traj, future = run_experienced_trajectory_v4(
                profile,
                crystal_params,
                mp,
                seed + 400_000 + int(round(10000 * p_inherit)),
                g,
                probe,
            )

            retained = traj[probe]
            erased = erase_material_labels(retained)

            access = material_accessibility_metrics(retained, radius)
            contact.append(
                access["frontier_cells_with_modified_neighbor"]
            )

            future_after_probe = future[probe:]

            A = continue_material_no_pulse(
                retained,
                future_after_probe,
                followup,
                radius,
                crystal_params,
                mp,
                profile["max_capacity_fraction"],
            )
            B = continue_material_no_pulse(
                erased,
                future_after_probe,
                followup,
                radius,
                crystal_params,
                mp,
                profile["max_capacity_fraction"],
            )

            Xs.append(
                morphology_features_from_occupied(A.occupied, radius)
            )
            Ys.append(
                morphology_features_from_occupied(B.occupied, radius)
            )
            symdiff.append(
                normalized_symmetric_difference(
                    A.occupied, B.occupied
                )
            )

        X = np.asarray(Xs, dtype=float)
        Y = np.asarray(Ys, dtype=float)

        test = paired_ridge_test(
            X,
            Y,
            permutations=profile["permutations"],
            seed=seed + 410_000 + int(round(10000 * p_inherit)),
        )

        results[str(p_inherit)] = {
            "inheritance_probability": float(p_inherit),
            "frontier_contact_at_ablation": bootstrap_mean_ci(
                contact,
                profile["bootstrap_reps"],
                seed + 420_000 + int(round(10000 * p_inherit)),
            ),
            "pathwise_symmetric_difference_after_followup": bootstrap_mean_ci(
                symdiff,
                profile["bootstrap_reps"],
                seed + 430_000 + int(round(10000 * p_inherit)),
            ),
            "paired_ridge_test": test,
        }

    result = {
        "late_ablation_step": probe,
        "followup_steps": followup,
        "results": results,
        "status": "MEASURED",
        "interpretation": (
            "Late whole-crystal ablation is secondary corroboration. V4 does not "
            "select an inheritance probability by the smallest p-value."
        ),
    }

    reporter.json("stage-03-secondary-late-ablation.json", result)
    reporter.stage(
        "stage-03-secondary-late-ablation.md",
        "Stage 3 — Secondary Late Ablation Across Propagation Regimes",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_mechanistic_verdict(
    reporter: Reporter,
    profile: dict,
    stage0: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    """
    Produce a mechanism map, not a winner.

    For each inheritance regime, classify the dominant late limitation:
      NO_ACCESS
      ACCESS_LOW_LEVERAGE
      ACCESS_WITH_REALIZED_FLIPS
    """
    target_step = profile["late_ablation_step"]
    classifications = {}

    for p_inherit in profile["inheritance_sweep"]:
        key = str(p_inherit)
        audit = stage2["results"][key]["summary"][str(target_step)]

        exposure = audit["exposed_frontier_count"]["mean"]
        leverage = audit["sum_delta_p"]["mean"]
        flips = audit["realized_causal_flips"]["mean"]

        if exposure <= 0:
            cls = "NO_ACCESS"
        elif leverage <= 1e-12:
            cls = "ACCESS_LOW_LEVERAGE"
        elif flips <= 0:
            cls = "ACCESS_WITH_PROBABILITY_LEVERAGE_BUT_NO_MEAN_REALIZED_FLIPS"
        else:
            cls = "ACCESS_WITH_REALIZED_FLIPS"

        classifications[key] = {
            "inheritance_probability": float(p_inherit),
            "late_step": target_step,
            "mean_exposed_frontier_count": exposure,
            "mean_sum_delta_p": leverage,
            "mean_realized_causal_flips": flips,
            "mechanistic_classification": cls,
        }

    any_realized = any(
        x["mechanistic_classification"] == "ACCESS_WITH_REALIZED_FLIPS"
        for x in classifications.values()
    )

    result = {
        "experiment_role": "EXPLORATORY MECHANISM CHARACTERIZATION",
        "chapter": 18,
        "question": (
            "Why can propagated material remain present near the frontier yet "
            "fail to produce a strong late whole-crystal effect?"
        ),
        "inheritance_sweep_is_descriptive_not_selection": True,
        "mechanistic_classification_at_late_step": classifications,
        "any_regime_with_realized_late_causal_flips": any_realized,
        "final_status": "MEASURED",
        "bounded_claim": (
            "V4 characterizes three separable quantities: whether modified "
            "material reaches the frontier, how strongly it changes attachment "
            "probabilities there, and whether those probability shifts produce "
            "realized CRN attachment flips."
        ),
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "phase transition",
            "critical threshold",
            "information storage",
            "genetic inheritance",
            "epigenetics",
            "signalling",
            "semantics",
            "agency",
            "individuality",
            "reproduction",
            "life",
        ],
        "next_question": (
            "Use the mechanism map to decide whether the next intervention should "
            "target propagation availability, local causal gain, or surface-biased "
            "state transmission. Do not choose solely from a significance result."
        ),
    }

    reporter.json("stage-04-mechanistic-verdict.json", result)
    reporter.stage(
        "stage-04-mechanistic-verdict.md",
        "Stage 4 — Bounded Chapter 18 V4 Mechanism Map",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260817)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch18-persistent-material-state-v4"
        ),
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    crystal_params = CrystalParams()

    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": 18,
        "chapter_title": "Can Experience Change the Material?",
        "run_type": "EXPLORATORY MECHANISM CHARACTERIZATION",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "v3_result_being_explained": (
            "Local inheritance extended frontier contact, but the late retained-"
            "vs-erased whole-crystal ablation did not establish a systematic "
            "population-level effect."
        ),
        "v4_design": (
            "Predeclared inheritance-probability sweep plus direct cell-level "
            "frontier causal audit. The sweep characterizes propagation regimes "
            "and is not used to select a winner by significance."
        ),
        "scientific_boundary": (
            "Mechanistic characterization only. No claim of memory, learning, "
            "adaptation, phase transition, criticality, or biological inheritance."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V4 — PROPAGATION MECHANICS")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups/regime={profile['groups']}"
    )
    print(f"inheritance_sweep={profile['inheritance_sweep']}")
    print("=" * 78)

    s0 = stage_0_extension_audit(
        reporter, profile, crystal_params, args.seed
    )

    s1 = stage_1_inheritance_sweep_accessibility(
        reporter, profile, crystal_params,
        args.seed, args.image_dir,
    )

    s2 = stage_2_cell_level_causal_audit(
        reporter, profile, crystal_params, args.seed
    )

    s3 = stage_3_secondary_late_ablation(
        reporter, profile, crystal_params, args.seed
    )

    s4 = stage_4_mechanistic_verdict(
        reporter, profile, s0, s1, s2, s3
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "final_status": s4["final_status"],
        "next_question": s4["next_question"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("CHAPTER 18 V4 COMPLETE")
    print(f"inheritance_sweep={s1['status']}")
    print(f"cell_level_causal_audit={s2['status']}")
    print(f"secondary_late_ablation={s3['status']}")
    print(f"final_status={s4['final_status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
