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
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v3"
SCHEMA_VERSION = 3

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


# ============================================================================
# Experiment profiles
# ============================================================================

PROFILES = {
    "quick": {
        "groups": 40,
        "radius": 64,
        "warmup_steps": 14,

        # Initial experience/write.
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,

        # New v3 local propagation mechanism.
        "inheritance_probability": 0.50,

        # Follow the material far beyond the v2 burial window.
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],

        # Late causal ablation occurs after v2 state had become inaccessible.
        "late_ablation_step": 14,
        "late_ablation_followup": 4,

        # Second identical challenge after late propagation.
        "challenge_step": 14,
        "challenge_horizon": 4,
        "challenge_pulse_step": 0,
        "challenge_observation_steps": [1, 2, 4],
        "challenge_primary_endpoint": 2,

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
        "inheritance_probability": 0.50,
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "challenge_step": 14,
        "challenge_horizon": 4,
        "challenge_pulse_step": 0,
        "challenge_observation_steps": [1, 2, 4],
        "challenge_primary_endpoint": 2,
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
        "inheritance_probability": 0.50,
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "challenge_step": 14,
        "challenge_horizon": 4,
        "challenge_pulse_step": 0,
        "challenge_observation_steps": [1, 2, 4],
        "challenge_primary_endpoint": 2,
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
        path = self.root / "ch18-persistent-material-state-v3-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V3 Propagation)\n\n"
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
    material_params: MaterialParams,
    seed: int,
) -> dict:
    """
    Audit the new propagation mechanism.

    1. With no modified cells, inheritance must be inert.
    2. With inheritance_probability=0, v3 must reproduce the v2 mechanism.
    3. Full v3 must be exactly reproducible.
    """
    radius = profile["radius"]
    steps = profile["warmup_steps"] + 10
    env = make_environment(steps, seed + 1)

    no_inheritance = MaterialParams(
        write_probability=material_params.write_probability,
        modified_neighbor_gain=material_params.modified_neighbor_gain,
        inheritance_probability=0.0,
    )

    # Empty-material invariance.
    a = initial_material_state(seed + 2)
    b = initial_material_state(seed + 2)
    for t in range(steps):
        a, _, _ = advance_one_step_material(
            a, float(env[t]), 0, radius,
            crystal_params, material_params,
        )
        b, _, _ = advance_one_step_material(
            b, float(env[t]), 0, radius,
            crystal_params, no_inheritance,
        )

    exact_when_material_empty = (
        a.occupied == b.occupied
        and a.modified == b.modified == set()
        and a.birth_time == b.birth_time
        and a.attachments_by_step == b.attachments_by_step
    )

    # Exact reproducibility with a pulse and inheritance enabled.
    c = initial_material_state(seed + 3)
    d = initial_material_state(seed + 3)
    for t in range(steps):
        bit = int(t == profile["experience_pulse_step"])
        forcing = float(env[t]) + profile["message_gain"] * bit
        c, _, _ = advance_one_step_material(
            c, forcing, bit, radius,
            crystal_params, material_params,
        )
        d, _, _ = advance_one_step_material(
            d, forcing, bit, radius,
            crystal_params, material_params,
        )

    exact_repro = (
        c.occupied == d.occupied
        and c.modified == d.modified
        and c.birth_time == d.birth_time
        and c.attachments_by_step == d.attachments_by_step
    )

    if not exact_when_material_empty:
        raise RuntimeError(
            "V3 propagation altered growth with no modified material present."
        )
    if not exact_repro:
        raise RuntimeError("V3 propagation is not exactly reproducible.")

    result = {
        "role": "V3 PROPAGATION EXTENSION AUDIT",
        "base_model_version": BASE_MODEL_VERSION,
        "experimental_extension": EXPERIMENT_VERSION,
        "canonical_model_modified": False,
        "exact_when_material_state_empty": exact_when_material_empty,
        "material_extension_exact_reproducibility": exact_repro,
        "write_probability": material_params.write_probability,
        "modified_neighbor_gain": material_params.modified_neighbor_gain,
        "inheritance_probability": material_params.inheritance_probability,
        "new_mechanism": (
            "newly attached cells adjacent to pre-existing modified material "
            "inherit modified state with fixed probability"
        ),
        "interpretation": (
            "Inheritance is local and inert until experience-written modified "
            "material exists."
        ),
    }

    reporter.json("stage-00-propagation-extension-audit.json", result)
    reporter.stage(
        "stage-00-propagation-extension-audit.md",
        "Stage 0 — Propagation Extension Audit",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def run_experienced_trajectory(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
    max_elapsed: int,
) -> Dict[int, MaterialCrystalState]:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]

    total = warmup + max_elapsed + 3
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

    return out


def stage_1_propagation_and_accessibility(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    image_dir: Path,
) -> dict:
    """
    Primary mechanism question:
        Does local inheritance keep experience-written state in contact with the
        active growth surface beyond the v2 burial window?
    """
    groups = profile["groups"]
    radius = profile["radius"]
    observations = profile["accessibility_observation_steps"]
    max_elapsed = max(observations)

    metrics = {
        t: {
            "modified_count": [],
            "modified_boundary_count": [],
            "frontier_cells_with_modified_neighbor": [],
            "frontier_exposed_fraction": [],
        }
        for t in observations
    }

    for g in tqdm(range(groups), desc="Stage 1 propagated accessibility"):
        traj = run_experienced_trajectory(
            profile, crystal_params, material_params,
            seed + 200_000, g, max_elapsed,
        )

        for t in observations:
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
    for t in observations:
        summary[str(t)] = {
            key: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 210_000 + t * 100 + j,
            )
            for j, (key, vals) in enumerate(metrics[t].items())
        }

    late_t = profile["late_ablation_step"]
    late_contact = summary[str(late_t)][
        "frontier_cells_with_modified_neighbor"
    ]["mean"]

    status = "SUPPORTED" if late_contact > 0 else "FAILED"

    result = {
        "groups": groups,
        "inheritance_probability": material_params.inheritance_probability,
        "observation_steps": observations,
        "late_target_step": late_t,
        "summary": summary,
        "status": status,
        "bounded_statement": (
            "Local inheritance "
            + (
                "kept experience-written material in contact with the active "
                "growth frontier beyond the v2 burial window."
                if status == "SUPPORTED"
                else "did not keep experience-written material in contact with "
                "the active growth frontier through the declared late target."
            )
        ),
    }

    reporter.json("stage-01-propagated-accessibility.json", result)
    reporter.stage(
        "stage-01-propagated-accessibility.md",
        "Stage 1 — Can Material State Travel With the Growth Front?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    ys = [
        summary[str(t)]["frontier_exposed_fraction"]["mean"]
        for t in xs
    ]
    ax.plot(xs, ys, marker="o")
    ax.axvline(
        profile["experience_pulse_step"] + 1,
        linestyle="--",
        linewidth=1,
    )
    ax.axvline(
        late_t,
        linestyle=":",
        linewidth=1,
    )
    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("Accessibility of propagated experience-written state")
    fig.tight_layout()

    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v3-01-propagated-accessibility.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def build_state_and_future_at_step(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
    elapsed_step: int,
    future_needed: int,
) -> Tuple[MaterialCrystalState, np.ndarray]:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]

    total = warmup + elapsed_step + future_needed + 3
    gseed = seed + 300_000 + group_index * 1013
    env = make_environment(total, gseed + 1)

    state = warm_material_checkpoint(
        env, warmup, gseed + 2, radius,
        crystal_params, material_params,
    )
    future = env[warmup:]

    for i in range(elapsed_step):
        bit = int(i == profile["experience_pulse_step"])
        forcing = float(future[i]) + profile["message_gain"] * bit
        state, _, _ = advance_one_step_material(
            state, forcing, bit, radius,
            crystal_params, material_params,
        )

    return state, future[elapsed_step:]


def stage_2_late_erase_ablation(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
) -> dict:
    """
    Critical causal test.

    At a time when v2 non-propagating material was already buried, compare:
        propagated state retained
        vs
        identical morphology with all material labels erased

    If later growth differs, propagated state remains causally active.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    probe = profile["late_ablation_step"]
    followup = profile["late_ablation_followup"]

    Xs, Ys = [], []
    symdiff = []
    contact = []

    for g in tqdm(range(groups), desc="Stage 2 late erase ablation"):
        retained, future = build_state_and_future_at_step(
            profile, crystal_params, material_params,
            seed + 400_000, g, probe, followup,
        )
        erased = erase_material_labels(retained)

        if retained.occupied != erased.occupied:
            raise RuntimeError("Late erase changed visible morphology.")
        if retained.birth_time != erased.birth_time:
            raise RuntimeError("Late erase changed birth history.")

        access = material_accessibility_metrics(retained, radius)
        contact.append(access["frontier_cells_with_modified_neighbor"])

        A = continue_material_no_pulse(
            retained, future, followup,
            radius, crystal_params, material_params,
            profile["max_capacity_fraction"],
        )
        B = continue_material_no_pulse(
            erased, future, followup,
            radius, crystal_params, material_params,
            profile["max_capacity_fraction"],
        )

        Xs.append(morphology_features_from_occupied(A.occupied, radius))
        Ys.append(morphology_features_from_occupied(B.occupied, radius))
        symdiff.append(
            normalized_symmetric_difference(A.occupied, B.occupied)
        )

    X = np.asarray(Xs, dtype=float)
    Y = np.asarray(Ys, dtype=float)

    test = paired_ridge_test(
        X, Y,
        permutations=profile["permutations"],
        seed=seed + 410_000,
    )

    positive = bool(test["p_value"] < profile["alpha"])

    result = {
        "groups": groups,
        "late_ablation_step": probe,
        "followup_steps": followup,
        "frontier_contact_at_ablation": bootstrap_mean_ci(
            contact,
            profile["bootstrap_reps"],
            seed + 411_000,
        ),
        "visible_morphology_identical_at_ablation": True,
        "pathwise_symmetric_difference_after_followup": bootstrap_mean_ci(
            symdiff,
            profile["bootstrap_reps"],
            seed + 412_000,
        ),
        "primary_test": test,
        "alpha": profile["alpha"],
        "status": "SUPPORTED" if positive else "FAILED",
        "bounded_statement": (
            "At a late step beyond the v2 burial window, erasing only propagated "
            "material state "
            + (
                "systematically changed subsequent growth."
                if positive
                else "did not establish a systematic change in subsequent growth."
            )
        ),
    }

    reporter.json("stage-02-late-erase-ablation.json", result)
    reporter.stage(
        "stage-02-late-erase-ablation.md",
        "Stage 2 — Is Propagated State Still Causally Active Late?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_3_late_reexposure_response(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
) -> dict:
    """
    Secondary exploratory test:
        does retaining propagated material state alter response to a later pulse?

    Retained and erased branches begin with identical visible morphology.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    challenge_step = profile["challenge_step"]
    horizon = profile["challenge_horizon"]
    observations = profile["challenge_observation_steps"]
    endpoint = profile["challenge_primary_endpoint"]

    retained_delta = {t: [] for t in observations}
    erased_delta = {t: [] for t in observations}

    pulse_bits = [0] * horizon
    pulse_bits[profile["challenge_pulse_step"]] = 1
    zero_bits = [0] * horizon

    for g in tqdm(range(groups), desc="Stage 3 late re-exposure"):
        retained, future = build_state_and_future_at_step(
            profile, crystal_params, material_params,
            seed + 500_000, g, challenge_step, horizon,
        )
        erased = erase_material_labels(retained)

        if retained.occupied != erased.occupied:
            raise RuntimeError(
                "Retained/erased challenge states differ in morphology."
            )

        RP = advance_material_sequence(
            retained, future, pulse_bits,
            profile["message_gain"], radius,
            crystal_params, material_params,
            observations, profile["max_capacity_fraction"],
        )
        R0 = advance_material_sequence(
            retained, future, zero_bits,
            profile["message_gain"], radius,
            crystal_params, material_params,
            observations, profile["max_capacity_fraction"],
        )
        EP = advance_material_sequence(
            erased, future, pulse_bits,
            profile["message_gain"], radius,
            crystal_params, material_params,
            observations, profile["max_capacity_fraction"],
        )
        E0 = advance_material_sequence(
            erased, future, zero_bits,
            profile["message_gain"], radius,
            crystal_params, material_params,
            observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            retained_delta[t].append(
                response_delta(RP[t], R0[t], radius)
            )
            erased_delta[t].append(
                response_delta(EP[t], E0[t], radius)
            )

    results = {}
    for t in observations:
        R = np.asarray(retained_delta[t], dtype=float)
        E = np.asarray(erased_delta[t], dtype=float)

        results[str(t)] = paired_ridge_test(
            R, E,
            permutations=profile["permutations"],
            seed=seed + 510_000 + t,
        )

    primary = results[str(endpoint)]
    positive = bool(primary["p_value"] < profile["alpha"])

    result = {
        "groups": groups,
        "challenge_step": challenge_step,
        "challenge_pulse_zero_index": profile["challenge_pulse_step"],
        "observation_steps": observations,
        "primary_endpoint": endpoint,
        "primary_contrast": (
            "difference in later-pulse response between propagated-state retained "
            "and propagated-state erased branches with identical visible morphology"
        ),
        "results": results,
        "primary_test": primary,
        "alpha": profile["alpha"],
        "status": "PROVISIONAL" if positive else "FAILED",
        "bounded_statement": (
            "Retained propagated material state "
            + (
                "changed the morphology response to a later identical pulse under "
                "this exploratory protocol."
                if positive
                else "did not establish a changed morphology response to a later "
                "identical pulse under this exploratory protocol."
            )
        ),
    }

    reporter.json("stage-03-late-reexposure.json", result)
    reporter.stage(
        "stage-03-late-reexposure.md",
        "Stage 3 — Does Propagated Experience Alter Later Response?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_verdict(
    reporter: Reporter,
    stage0: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    if not (
        stage0["exact_when_material_state_empty"]
        and stage0["material_extension_exact_reproducibility"]
    ):
        final_status = "UNTESTED"
        next_question = "Fix the propagation extension before interpretation."

    elif stage1["status"] != "SUPPORTED":
        final_status = "FAILED"
        next_question = (
            "Local inheritance did not maintain frontier accessibility through "
            "the declared late window."
        )

    elif stage2["status"] != "SUPPORTED":
        final_status = "FAILED"
        next_question = (
            "Propagation preserved frontier contact but the late retained state "
            "was not shown to be causally active."
        )

    elif stage3["status"] == "PROVISIONAL":
        final_status = "PROVISIONAL"
        next_question = (
            "Can the propagated material state be overwritten or updated by a "
            "second experience rather than only copied forward?"
        )

    else:
        final_status = "SUPPORTED"
        next_question = (
            "Propagation extended causal persistence, but later-response "
            "modulation was not established. Characterize the propagated state "
            "before introducing update/overwrite dynamics."
        )

    result = {
        "experiment_role": "EXPLORATORY MECHANISM EXTENSION",
        "chapter": 18,
        "question": (
            "Can experience-written material state propagate with growth and "
            "remain causally accessible?"
        ),
        "stage_1_propagated_accessibility": stage1["status"],
        "stage_2_late_causal_ablation": stage2["status"],
        "stage_3_later_response_modulation": stage3["status"],
        "final_status": final_status,
        "bounded_claim": (
            "V3 tests one local propagation rule: newly attached material may "
            "inherit experience-written state from adjacent modified material. "
            "It tests whether that keeps the state causally accessible beyond the "
            "v2 burial window and whether retained propagated state matters later."
        ),
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
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
        "next_question": next_question,
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 18 V3 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch18-persistent-material-state-v3"
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
    material_params = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        inheritance_probability=profile["inheritance_probability"],
    )

    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": 18,
        "chapter_title": "Can Experience Change the Material?",
        "run_type": "EXPLORATORY MECHANISM EXTENSION",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "v2_supported_result": (
            "Persistent material was causally active while it contacted the "
            "growth frontier and became inert after growth moved beyond it."
        ),
        "v3_new_mechanism": (
            "A newly attached cell adjacent to pre-existing modified material "
            "inherits modified state with fixed probability."
        ),
        "material_parameters": {
            "write_probability": material_params.write_probability,
            "modified_neighbor_gain": material_params.modified_neighbor_gain,
            "inheritance_probability": material_params.inheritance_probability,
        },
        "scientific_boundary": (
            "Local propagation of material state only. No global memory register, "
            "history buffer, learned parameter, target behaviour, decoder, or "
            "biological inheritance claim."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V3 — CAN MATERIAL STATE TRAVEL WITH GROWTH?")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']}"
    )
    print("=" * 78)

    s0 = stage_0_extension_audit(
        reporter, profile, crystal_params, material_params, args.seed
    )

    s1 = stage_1_propagation_and_accessibility(
        reporter, profile, crystal_params, material_params,
        args.seed, args.image_dir,
    )

    s2 = stage_2_late_erase_ablation(
        reporter, profile, crystal_params, material_params, args.seed
    )

    s3 = stage_3_late_reexposure_response(
        reporter, profile, crystal_params, material_params, args.seed
    )

    s4 = stage_4_verdict(
        reporter, s0, s1, s2, s3
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
    print("CHAPTER 18 V3 COMPLETE")
    print(f"propagated_accessibility={s1['status']}")
    print(f"late_material_state_causal={s2['status']}")
    print(f"later_response_changed={s3['status']}")
    print(f"final_status={s4['final_status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
