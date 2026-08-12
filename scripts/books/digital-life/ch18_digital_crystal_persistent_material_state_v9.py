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
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v9"
SCHEMA_VERSION = 9

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
    Chapter 18 v6 experimental material-state extension.

    Existing rules remain:
        - explicit pulse writes modified state to occupied boundary cells;
        - modified state persists irreversibly;
        - modified occupied neighbours bias later frontier attachment.

    V6 isolates propagation PLACEMENT under an exactly matched transmission
    budget across three synchronized counterfactual branches:

        interior_biased
        random_matched
        surface_biased

    A controller computes ONE shared budget K at each propagation step:

        K = round(
            transmission_fraction
            * min(eligible_interior, eligible_random, eligible_surface)
        )

    Each branch must transmit exactly K eligible newly attached cells.
    Cumulative transmission counts are asserted equal after every step.

    Therefore the intervention is not "how much state gets copied"; it is
    "where the same amount of copied state is placed."

    No memory register, history buffer, learned parameter, target morphology,
    decoder, or biological inheritance claim is introduced.
    """
    write_probability: float = 0.20
    modified_neighbor_gain: float = 0.30
    transmission_fraction: float = 0.50


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



def transmission_rank_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    """
    Stable keyed rank used by the equal-budget uniform placement policy.
    """
    q, r = cell
    payload = (
        f"transmission-uniform:{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}"
    ).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def surface_exposure_after_attachment(
    cell: Cell,
    occupied_after: Set[Cell],
) -> int:
    """
    Number of empty neighbouring positions after the step's attachments.

    Larger values mean the newly attached cell sits on a more exposed part of
    the current growth surface.
    """
    return sum(nb not in occupied_after for nb in neighbors(cell))


def eligible_transmission_targets(
    additions: Sequence[Cell],
    modified_before: Set[Cell],
) -> List[Cell]:
    return [
        cell
        for cell in additions
        if any(nb in modified_before for nb in neighbors(cell))
    ]


def choose_targets_with_exact_budget(
    eligible: Sequence[Cell],
    occupied_after: Set[Cell],
    stream_seed: int,
    step: int,
    budget: int,
    policy: str,
) -> Tuple[List[Cell], dict]:
    """
    Choose exactly `budget` cells from the already-computed eligible set.

    Policies differ only in spatial allocation.
    """
    eligible = list(eligible)
    n = len(eligible)

    if budget < 0:
        raise ValueError("budget must be nonnegative")
    if budget > n:
        raise ValueError(
            f"budget={budget} exceeds eligible_count={n} for policy={policy}"
        )

    if budget == 0:
        selected = []

    elif policy == "random_matched":
        selected = sorted(
            eligible,
            key=lambda c: (
                transmission_rank_uniform(stream_seed, step, c),
                c,
            ),
        )[:budget]

    elif policy == "surface_biased":
        selected = sorted(
            eligible,
            key=lambda c: (
                -surface_exposure_after_attachment(c, occupied_after),
                transmission_rank_uniform(stream_seed, step, c),
                c,
            ),
        )[:budget]

    elif policy == "interior_biased":
        selected = sorted(
            eligible,
            key=lambda c: (
                surface_exposure_after_attachment(c, occupied_after),
                transmission_rank_uniform(stream_seed, step, c),
                c,
            ),
        )[:budget]

    else:
        raise ValueError(f"Unknown matched-budget policy: {policy!r}")

    eligible_surface = [
        surface_exposure_after_attachment(c, occupied_after)
        for c in eligible
    ]
    selected_surface = [
        surface_exposure_after_attachment(c, occupied_after)
        for c in selected
    ]

    return selected, {
        "eligible_count": int(n),
        "budget": int(budget),
        "selected_count": int(len(selected)),
        "mean_eligible_surface_exposure": (
            float(np.mean(eligible_surface)) if eligible_surface else 0.0
        ),
        "mean_selected_surface_exposure": (
            float(np.mean(selected_surface)) if selected_surface else 0.0
        ),
    }


def shared_transmission_budget(
    eligible_counts: Sequence[int],
    transmission_fraction: float,
) -> int:
    """
    Exact common budget shared by all synchronized branches.
    """
    if not eligible_counts:
        return 0

    base = min(int(x) for x in eligible_counts)
    k = int(round(float(transmission_fraction) * base))
    return max(0, min(base, k))


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


def grow_one_step_without_transmission(
    state: MaterialCrystalState,
    input_value: float,
    pulse_bit: int,
    max_radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> Tuple[MaterialCrystalState, List[Cell], int]:
    """
    Growth phase only.

    V6 deliberately separates:
        growth
        transmission placement

    so multiple branches can first grow, then share one exact propagation budget.
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

    newly_written = 0

    if int(pulse_bit) != 0:
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

    return out, additions, newly_written


def apply_transmission_targets(
    state_after_growth: MaterialCrystalState,
    selected: Sequence[Cell],
) -> MaterialCrystalState:
    out = clone_material_state(state_after_growth)
    out.modified.update(selected)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = len(out.modified)
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
    Compatibility wrapper used for warmup/no-propagation contexts.

    It performs growth and direct pulse writing but NO propagation.
    Synchronized propagation is handled by the V6 multi-branch controller.
    """
    out, additions, newly_written = grow_one_step_without_transmission(
        state,
        input_value,
        pulse_bit,
        max_radius,
        crystal_params,
        material_params,
    )
    return out, len(additions), newly_written

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
        "groups": 64,
        "radius": 64,
        "warmup_steps": 14,

        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,

        # Surface-biased propagation rule retained from v7.
        "transmission_fraction": 0.50,

        # Frozen observation window.
        "window_start": 5,
        "window_end": 24,

        # Reference schedule is generated from a separate frozen seed namespace.
        "reference_groups": 64,

        # Sustained loss definition.
        "sustained_zero_steps": 3,

        # Descriptive checkpoints only.
        "descriptive_steps": [5, 8, 10, 12, 14, 18, 22, 24],

        "bootstrap_reps": 1500,
        "permutations": 2000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 128,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "transmission_fraction": 0.50,
        "window_start": 5,
        "window_end": 24,
        "reference_groups": 128,
        "sustained_zero_steps": 3,
        "descriptive_steps": [5, 8, 10, 12, 14, 18, 22, 24],
        "bootstrap_reps": 3000,
        "permutations": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 256,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "transmission_fraction": 0.50,
        "window_start": 5,
        "window_end": 24,
        "reference_groups": 256,
        "sustained_zero_steps": 3,
        "descriptive_steps": [5, 8, 10, 12, 14, 18, 22, 24],
        "bootstrap_reps": 5000,
        "permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
}


def choose_surface_targets_with_budget(
    eligible: Sequence[Cell],
    occupied_after: Set[Cell],
    stream_seed: int,
    step: int,
    budget: int,
) -> Tuple[List[Cell], dict]:
    return choose_targets_with_exact_budget(
        eligible=eligible,
        occupied_after=occupied_after,
        stream_seed=stream_seed,
        step=step,
        budget=budget,
        policy="surface_biased",
    )


def natural_budget(eligible_count: int, transmission_fraction: float) -> int:
    k = int(round(float(transmission_fraction) * int(eligible_count)))
    return max(0, min(int(eligible_count), k))


def build_reference_schedule(
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Build an exogenous per-step transmission schedule from separate reference
    trajectories before evaluating treatment groups.

    The schedule is the rounded median natural-feedback budget across reference
    groups at each elapsed step. Evaluation branches never influence it.
    """
    groups = profile["reference_groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    end = profile["window_end"]

    per_step_budgets = {t: [] for t in range(1, end + 1)}

    mp = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )

    for g in tqdm(range(groups), desc="Reference schedule"):
        total = warmup + end + 8
        gseed = seed + 700_000 + g * 1013
        env = make_environment(total, gseed + 1)

        state = warm_material_checkpoint(
            env,
            warmup,
            gseed + 2,
            radius,
            crystal_params,
            mp,
        )
        future = env[warmup:]

        for i in range(end):
            bit = int(i == profile["experience_pulse_step"])
            forcing = float(future[i]) + profile["message_gain"] * bit

            modified_before = set(state.modified)
            grown, additions, _ = grow_one_step_without_transmission(
                state,
                forcing,
                bit,
                radius,
                crystal_params,
                mp,
            )

            eligible = eligible_transmission_targets(
                additions,
                modified_before,
            )

            if i <= profile["experience_pulse_step"]:
                k = 0
            else:
                k = natural_budget(
                    len(eligible),
                    profile["transmission_fraction"],
                )

            selected, _ = choose_surface_targets_with_budget(
                eligible,
                grown.occupied,
                grown.stream_seed,
                grown.step,
                k,
            )

            state = apply_transmission_targets(grown, selected)
            per_step_budgets[i + 1].append(k)

            frac = capacity_fraction_occupied(state.occupied, radius)
            if frac >= profile["max_capacity_fraction"]:
                raise RuntimeError(
                    f"Reference schedule saturation at elapsed={i+1}: {frac:.3f}"
                )

    schedule = {}
    distribution = {}

    for t in range(1, end + 1):
        vals = np.asarray(per_step_budgets[t], dtype=int)
        schedule[t] = int(round(float(np.median(vals))))
        distribution[t] = {
            "n": int(len(vals)),
            "mean": float(np.mean(vals)),
            "median": float(np.median(vals)),
            "min": int(np.min(vals)),
            "max": int(np.max(vals)),
        }

    return {
        "schedule": schedule,
        "distribution": distribution,
        "reference_groups": groups,
        "schedule_rule": "rounded median natural-feedback budget per elapsed step",
    }


def run_feedback_pair(
    profile: dict,
    crystal_params: CrystalParams,
    frozen_schedule: Dict[int, int],
    seed: int,
    group_index: int,
) -> dict:
    """
    Run paired NATURAL_FEEDBACK and CLAMPED_SCHEDULE branches.

    Both branches:
      - start from same warm checkpoint,
      - receive same experience pulse,
      - use same surface-biased placement,
      - share environment and cell-keyed CRN.

    Difference:
      NATURAL_FEEDBACK:
        K_t = round(fraction * own eligible_count_t)

      CLAMPED_SCHEDULE:
        K_t = frozen exogenous schedule, truncated only if branch has fewer
        eligible cells than the scheduled amount.

    Truncation is measured explicitly; excessive truncation weakens interpretation.
    """
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    end = profile["window_end"]

    total = warmup + end + 8
    gseed = seed + 100_000 + group_index * 1009
    env = make_environment(total, gseed + 1)

    mp = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )

    base = warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        mp,
    )

    states = {
        "natural_feedback": clone_material_state(base),
        "clamped_schedule": clone_material_state(base),
    }

    future = env[warmup:]
    observations = {k: {} for k in states}
    logs = []
    cumulative = {k: 0 for k in states}

    for i in range(end):
        elapsed = i + 1
        bit = int(i == profile["experience_pulse_step"])
        forcing = float(future[i]) + profile["message_gain"] * bit

        row = {"elapsed_step": elapsed}

        for branch in ("natural_feedback", "clamped_schedule"):
            state = states[branch]
            modified_before = set(state.modified)

            grown, additions, _ = grow_one_step_without_transmission(
                state,
                forcing,
                bit,
                radius,
                crystal_params,
                mp,
            )

            eligible = eligible_transmission_targets(
                additions,
                modified_before,
            )

            if i <= profile["experience_pulse_step"]:
                requested = 0
            elif branch == "natural_feedback":
                requested = natural_budget(
                    len(eligible),
                    profile["transmission_fraction"],
                )
            else:
                requested = int(frozen_schedule[elapsed])

            applied = min(requested, len(eligible))
            truncated = int(applied < requested)

            selected, meta = choose_surface_targets_with_budget(
                eligible,
                grown.occupied,
                grown.stream_seed,
                grown.step,
                applied,
            )

            states[branch] = apply_transmission_targets(
                grown,
                selected,
            )
            cumulative[branch] += len(selected)

            row[branch] = {
                "eligible_count": int(len(eligible)),
                "requested_budget": int(requested),
                "applied_budget": int(applied),
                "truncated": int(truncated),
                "mean_selected_surface_exposure": meta[
                    "mean_selected_surface_exposure"
                ],
                "cumulative_transmissions": int(cumulative[branch]),
            }

            observations[branch][elapsed] = clone_material_state(
                states[branch]
            )

            frac = capacity_fraction_occupied(
                states[branch].occupied,
                radius,
            )
            if frac >= profile["max_capacity_fraction"]:
                raise RuntimeError(
                    f"Feedback pair saturation: branch={branch}, "
                    f"elapsed={elapsed}, fraction={frac:.3f}"
                )

        logs.append(row)

    return {
        "states": observations,
        "future": future,
        "logs": logs,
        "final_cumulative": cumulative,
    }


def discrete_auc(values_by_step: Dict[int, float], start: int, end: int) -> float:
    """
    Discrete integrated quantity over an inclusive integer-step window.
    """
    return float(sum(float(values_by_step[t]) for t in range(start, end + 1)))

def sustained_zero_loss_time(
    contact_by_step: Dict[int, float],
    start: int,
    end: int,
    consecutive: int,
) -> int:
    """
    First step beginning a run of `consecutive` zero-contact updates.

    If no such run occurs, returns end + 1 (right-censored in this experiment).
    """
    if consecutive <= 0:
        raise ValueError("consecutive must be positive")

    for t in range(start, end - consecutive + 2):
        if all(
            float(contact_by_step[k]) == 0.0
            for k in range(t, t + consecutive)
        ):
            return int(t)

    return int(end + 1)

def ordered_three_way(values: Dict[str, float]) -> bool:
    return bool(
        values["interior_biased"]
        < values["random_matched"]
        < values["surface_biased"]
    )

def paired_sign_test_order(
    interior: Sequence[float],
    random_values: Sequence[float],
    surface: Sequence[float],
) -> dict:
    """
    Descriptive paired ordering support.

    Counts groups satisfying:
        interior < random < surface

    No inferential claim is based solely on this count.
    """
    I = np.asarray(interior, dtype=float)
    R = np.asarray(random_values, dtype=float)
    S = np.asarray(surface, dtype=float)

    if not (len(I) == len(R) == len(S)):
        raise ValueError("paired ordering arrays must have same length")

    strict = (I < R) & (R < S)
    nondecreasing = (I <= R) & (R <= S)

    return {
        "n": int(len(I)),
        "strict_order_count": int(np.sum(strict)),
        "strict_order_fraction": float(np.mean(strict)),
        "nondecreasing_order_count": int(np.sum(nondecreasing)),
        "nondecreasing_order_fraction": float(np.mean(nondecreasing)),
    }

def paired_randomization_difference_test(
    A: Sequence[float],
    B: Sequence[float],
    permutations: int,
    seed: int,
    alternative: str = "greater",
) -> dict:
    """
    Paired sign-flip randomization test on mean difference B-A.

    alternative='greater' tests whether B tends to exceed A.
    """
    a = np.asarray(A, dtype=float)
    b = np.asarray(B, dtype=float)

    if a.shape != b.shape:
        raise ValueError("paired test requires equal shapes")

    d = b - a
    observed = float(np.mean(d))

    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        signs = rng.choice(np.asarray([-1.0, 1.0]), size=len(d))
        null[i] = float(np.mean(d * signs))

    if alternative == "greater":
        p = (1 + np.sum(null >= observed)) / (permutations + 1)
    elif alternative == "two-sided":
        p = (1 + np.sum(np.abs(null) >= abs(observed))) / (permutations + 1)
    else:
        raise ValueError("unsupported alternative")

    return {
        "mean_difference_B_minus_A": observed,
        "p_value": float(p),
        "permutations": int(permutations),
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
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
        path = self.root / "ch18-persistent-material-state-v9-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V9 Temporal Alignment)\n\n"
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

def run_synchronized_policy_trajectory(
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
    group_index: int,
    max_elapsed: int,
) -> dict:
    """
    Run interior/random/surface branches side-by-side under an exact common
    transmission budget.

    Each propagation step:
      1. grow all branches under shared environment + cell-keyed CRN;
      2. compute eligible propagation targets per branch;
      3. compute ONE shared K from the minimum eligible count;
      4. allocate exactly K targets in each branch by placement policy;
      5. assert equal per-step and cumulative transmission counts.
    """
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    policies = profile["placement_policies"]

    total = warmup + max_elapsed + 8
    gseed = seed + 100_000 + group_index * 1009
    env = make_environment(total, gseed + 1)

    mp = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )

    base = warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        mp,
    )

    states = {
        p: clone_material_state(base)
        for p in policies
    }

    future = env[warmup:]
    observations = {p: {} for p in policies}
    transmission_log = []
    cumulative = {p: 0 for p in policies}

    for i in range(max_elapsed):
        bit = int(i == profile["experience_pulse_step"])
        forcing = float(future[i]) + profile["message_gain"] * bit

        growth = {}
        additions = {}
        modified_before = {}

        for p in policies:
            modified_before[p] = set(states[p].modified)
            grown, adds, _ = grow_one_step_without_transmission(
                states[p],
                forcing,
                bit,
                radius,
                crystal_params,
                mp,
            )
            growth[p] = grown
            additions[p] = adds

        eligible = {
            p: eligible_transmission_targets(
                additions[p],
                modified_before[p],
            )
            for p in policies
        }

        # Do not propagate on or before the direct pulse-write step.
        if i <= profile["experience_pulse_step"]:
            shared_k = 0
        else:
            shared_k = shared_transmission_budget(
                [len(eligible[p]) for p in policies],
                profile["transmission_fraction"],
            )

        selected_meta = {}

        for p in policies:
            selected, meta = choose_targets_with_exact_budget(
                eligible[p],
                growth[p].occupied,
                growth[p].stream_seed,
                growth[p].step,
                shared_k,
                p,
            )

            states[p] = apply_transmission_targets(
                growth[p],
                selected,
            )

            cumulative[p] += len(selected)
            selected_meta[p] = meta

        per_step_counts = [
            selected_meta[p]["selected_count"]
            for p in policies
        ]

        if len(set(per_step_counts)) != 1:
            raise RuntimeError(
                f"V7 invalid: per-step transmission counts diverged at "
                f"elapsed={i+1}: {per_step_counts}"
            )

        if len(set(cumulative.values())) != 1:
            raise RuntimeError(
                f"V7 invalid: cumulative transmission counts diverged at "
                f"elapsed={i+1}: {cumulative}"
            )

        transmission_log.append({
            "elapsed_step": i + 1,
            "shared_budget": int(shared_k),
            "eligible_counts": {
                p: len(eligible[p]) for p in policies
            },
            "selected_counts": {
                p: selected_meta[p]["selected_count"]
                for p in policies
            },
            "mean_selected_surface_exposure": {
                p: selected_meta[p]["mean_selected_surface_exposure"]
                for p in policies
            },
            "cumulative_transmissions": dict(cumulative),
        })

        for p in policies:
            observations[p][i + 1] = clone_material_state(states[p])

            frac = capacity_fraction_occupied(
                states[p].occupied,
                radius,
            )
            if frac >= profile["max_capacity_fraction"]:
                raise RuntimeError(
                    f"Saturation guard reached: policy={p}, elapsed={i+1}, "
                    f"fraction={frac:.3f}"
                )

    return {
        "states": observations,
        "future": future,
        "transmission_log": transmission_log,
        "final_cumulative": dict(cumulative),
    }


def stage_0_reference_schedule(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    reference = build_reference_schedule(
        profile,
        crystal_params,
        seed,
    )

    result = {
        "role": "V8 FROZEN EXOGENOUS REFERENCE SCHEDULE",
        "reference_groups": reference["reference_groups"],
        "schedule_rule": reference["schedule_rule"],
        "schedule": {
            str(k): v for k, v in reference["schedule"].items()
        },
        "distribution": {
            str(k): v for k, v in reference["distribution"].items()
        },
        "scientific_role": (
            "The clamped branch receives a propagation schedule generated from "
            "separate reference trajectories. Evaluation outcomes cannot change "
            "that schedule."
        ),
        "status": "MEASURED",
    }

    reporter.json("stage-00-reference-schedule.json", result)
    reporter.stage(
        "stage-00-reference-schedule.md",
        "Stage 0 — Freeze the Exogenous Propagation Schedule",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    return {
        **result,
        "_schedule_int_keys": reference["schedule"],
    }


def stage_1_feedback_mechanism_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    frozen_schedule: Dict[int, int],
    seed: int,
) -> dict:
    """
    Measure the proposed feedback chain directly:
        current access
        -> eligible propagation opportunities
        -> actual transmissions
        -> future access
    """
    groups = profile["groups"]
    start = profile["window_start"]
    end = profile["window_end"]

    natural = {
        "access": [],
        "eligible": [],
        "transmissions": [],
    }
    clamped = {
        "access": [],
        "eligible": [],
        "transmissions": [],
    }

    truncations = []

    for g in tqdm(range(groups), desc="Stage 1 feedback mechanism audit"):
        run = run_feedback_pair(
            profile,
            crystal_params,
            frozen_schedule,
            seed + 200_000,
            g,
        )

        for branch, store in (
            ("natural_feedback", natural),
            ("clamped_schedule", clamped),
        ):
            access_by_t = {}
            eligible_by_t = {}
            tx_by_t = {}

            for t in range(start, end + 1):
                state = run["states"][branch][t]
                access = material_accessibility_metrics(
                    state,
                    profile["radius"],
                )
                access_by_t[t] = access[
                    "frontier_cells_with_modified_neighbor"
                ]

                row = run["logs"][t - 1][branch]
                eligible_by_t[t] = row["eligible_count"]
                tx_by_t[t] = row["applied_budget"]

                if branch == "clamped_schedule":
                    truncations.append(row["truncated"])

            store["access"].append(
                discrete_auc(access_by_t, start, end)
            )
            store["eligible"].append(
                discrete_auc(eligible_by_t, start, end)
            )
            store["transmissions"].append(
                discrete_auc(tx_by_t, start, end)
            )

    trunc_rate = float(np.mean(truncations)) if truncations else 0.0

    result = {
        "groups": groups,
        "window": {"start": start, "end": end},
        "natural_feedback": {
            "access_auc": bootstrap_mean_ci(
                natural["access"],
                profile["bootstrap_reps"],
                seed + 210_000,
            ),
            "eligible_opportunity_auc": bootstrap_mean_ci(
                natural["eligible"],
                profile["bootstrap_reps"],
                seed + 210_100,
            ),
            "transmission_count_auc": bootstrap_mean_ci(
                natural["transmissions"],
                profile["bootstrap_reps"],
                seed + 210_200,
            ),
        },
        "clamped_schedule": {
            "access_auc": bootstrap_mean_ci(
                clamped["access"],
                profile["bootstrap_reps"],
                seed + 211_000,
            ),
            "eligible_opportunity_auc": bootstrap_mean_ci(
                clamped["eligible"],
                profile["bootstrap_reps"],
                seed + 211_100,
            ),
            "transmission_count_auc": bootstrap_mean_ci(
                clamped["transmissions"],
                profile["bootstrap_reps"],
                seed + 211_200,
            ),
        },
        "clamped_schedule_truncation_rate": trunc_rate,
        "status": "MEASURED",
        "bounded_statement": (
            "V8 directly measures whether greater causal accessibility is "
            "associated with more eligible propagation opportunities and, in the "
            "natural branch, more realized transmissions."
        ),
    }

    reporter.json("stage-01-feedback-mechanism.json", result)
    reporter.stage(
        "stage-01-feedback-mechanism.md",
        "Stage 1 — Does Accessibility Generate Future Propagation Opportunity?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_2_feedback_vs_clamped(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    frozen_schedule: Dict[int, int],
    seed: int,
    image_dir: Path,
) -> dict:
    """
    Primary V8 causal comparison:
        natural opportunity feedback
        vs
        exogenous clamped propagation schedule
    """
    groups = profile["groups"]
    radius = profile["radius"]
    start = profile["window_start"]
    end = profile["window_end"]
    zero_n = profile["sustained_zero_steps"]

    metrics = {
        branch: {
            "access_fraction_auc": [],
            "contact_count_auc": [],
            "probability_leverage_auc": [],
            "total_realized_flips": [],
            "sustained_loss_time": [],
            "cumulative_transmissions": [],
        }
        for branch in ("natural_feedback", "clamped_schedule")
    }

    trajectories = {
        branch: {
            t: {
                "frontier_exposed_fraction": [],
                "frontier_contact": [],
                "sum_delta_p": [],
                "realized_flips": [],
            }
            for t in range(start, end + 1)
        }
        for branch in metrics
    }

    truncations = []

    for g in tqdm(range(groups), desc="Stage 2 feedback vs clamped"):
        run = run_feedback_pair(
            profile,
            crystal_params,
            frozen_schedule,
            seed + 300_000,
            g,
        )

        future = run["future"]

        for branch in metrics:
            mp = MaterialParams(
                write_probability=profile["write_probability"],
                modified_neighbor_gain=profile["modified_neighbor_gain"],
                transmission_fraction=profile["transmission_fraction"],
            )

            frac_by_t = {}
            contact_by_t = {}
            leverage_by_t = {}
            flips_by_t = {}

            for t in range(start, end + 1):
                state = run["states"][branch][t]
                access = material_accessibility_metrics(
                    state,
                    radius,
                )
                audit = frontier_material_causal_audit(
                    state,
                    float(future[t]),
                    radius,
                    crystal_params,
                    mp,
                )

                frac_by_t[t] = access["frontier_exposed_fraction"]
                contact_by_t[t] = access[
                    "frontier_cells_with_modified_neighbor"
                ]
                leverage_by_t[t] = audit["sum_delta_p"]
                flips_by_t[t] = audit["realized_causal_flips"]

                trajectories[branch][t][
                    "frontier_exposed_fraction"
                ].append(frac_by_t[t])
                trajectories[branch][t][
                    "frontier_contact"
                ].append(contact_by_t[t])
                trajectories[branch][t][
                    "sum_delta_p"
                ].append(leverage_by_t[t])
                trajectories[branch][t][
                    "realized_flips"
                ].append(flips_by_t[t])

            metrics[branch]["access_fraction_auc"].append(
                discrete_auc(frac_by_t, start, end)
            )
            metrics[branch]["contact_count_auc"].append(
                discrete_auc(contact_by_t, start, end)
            )
            metrics[branch]["probability_leverage_auc"].append(
                discrete_auc(leverage_by_t, start, end)
            )
            metrics[branch]["total_realized_flips"].append(
                discrete_auc(flips_by_t, start, end)
            )
            metrics[branch]["sustained_loss_time"].append(
                sustained_zero_loss_time(
                    contact_by_t,
                    start,
                    end,
                    zero_n,
                )
            )
            metrics[branch]["cumulative_transmissions"].append(
                run["final_cumulative"][branch]
            )

        for row in run["logs"]:
            truncations.append(
                row["clamped_schedule"]["truncated"]
            )

    summary = {}
    for bi, branch in enumerate(metrics):
        summary[branch] = {
            key: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 310_000 + bi * 1000 + j,
            )
            for j, (key, vals) in enumerate(metrics[branch].items())
        }

    trajectory_summary = {
        branch: {
            str(t): {
                k: float(np.mean(v))
                for k, v in trajectories[branch][t].items()
            }
            for t in range(start, end + 1)
        }
        for branch in trajectories
    }

    primary_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
        "sustained_loss_time",
    )

    tests = {}
    for i, metric in enumerate(primary_metrics):
        tests[metric] = paired_randomization_difference_test(
            metrics["clamped_schedule"][metric],
            metrics["natural_feedback"][metric],
            profile["permutations"],
            seed + 320_000 + i * 100,
            alternative="greater",
        )

    transmission_test = paired_randomization_difference_test(
        metrics["clamped_schedule"]["cumulative_transmissions"],
        metrics["natural_feedback"]["cumulative_transmissions"],
        profile["permutations"],
        seed + 325_000,
        alternative="greater",
    )

    trunc_rate = float(np.mean(truncations)) if truncations else 0.0

    result = {
        "groups": groups,
        "window": {"start": start, "end": end},
        "summary": summary,
        "trajectory_summary": trajectory_summary,
        "paired_tests_natural_gt_clamped": tests,
        "natural_gt_clamped_cumulative_transmissions_test": transmission_test,
        "clamped_schedule_truncation_rate": trunc_rate,
        "status": "MEASURED",
        "bounded_statement": (
            "V8 compares an endogenous opportunity-feedback branch with a branch "
            "whose propagation opportunity is clamped to a frozen exogenous "
            "schedule."
        ),
    }

    reporter.json("stage-02-feedback-vs-clamped.json", result)
    reporter.stage(
        "stage-02-feedback-vs-clamped.md",
        "Stage 2 — Does Opportunity Feedback Extend Causal Accessibility?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = list(range(start, end + 1))

    for branch in ("natural_feedback", "clamped_schedule"):
        ys = [
            trajectory_summary[branch][str(t)][
                "frontier_exposed_fraction"
            ]
            for t in xs
        ]
        ax.plot(xs, ys, marker="o", label=branch)

    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("V8 opportunity feedback vs frozen propagation schedule")
    ax.legend()
    fig.tight_layout()

    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v8-01-feedback-vs-clamped.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_3_descriptive_checkpoints(
    reporter: Reporter,
    profile: dict,
    stage2: dict,
) -> dict:
    steps = profile["descriptive_steps"]

    result = {
        "role": "SECONDARY DESCRIPTIVE",
        "steps": steps,
        "results": {
            str(t): {
                branch: stage2["trajectory_summary"][branch][str(t)]
                for branch in (
                    "natural_feedback",
                    "clamped_schedule",
                )
            }
            for t in steps
        },
        "cannot_change_primary_decision": True,
        "status": "MEASURED",
    }

    reporter.json("stage-03-descriptive-checkpoints.json", result)
    reporter.stage(
        "stage-03-descriptive-checkpoints.md",
        "Stage 3 — Secondary Feedback Checkpoints",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage0: dict,
    stage1: dict,
    stage2: dict,
) -> dict:
    alpha = profile["alpha"]

    required_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
    )

    causal_metrics_ok = all(
        stage2["paired_tests_natural_gt_clamped"][m]["p_value"] < alpha
        for m in required_metrics
    )

    lifetime_supportive = (
        stage2["paired_tests_natural_gt_clamped"][
            "sustained_loss_time"
        ]["p_value"] < alpha
    )

    transmission_feedback_present = (
        stage2["natural_gt_clamped_cumulative_transmissions_test"][
            "p_value"
        ] < alpha
    )

    truncation_rate = stage2["clamped_schedule_truncation_rate"]

    # A high truncation rate means the frozen schedule often exceeded what the
    # clamped branch could realize, weakening a clean "same exogenous schedule"
    # interpretation.
    truncation_ok = truncation_rate <= 0.10

    if causal_metrics_ok and transmission_feedback_present and truncation_ok:
        status = "SUPPORTED"
        bounded = (
            "Under the frozen reference schedule used here, allowing current "
            "surface accessibility to determine future propagation opportunity "
            "produced more realized transmissions and greater integrated causal "
            "accessibility and causal work than the exogenously scheduled branch."
        )

    elif causal_metrics_ok and transmission_feedback_present:
        status = "PROVISIONAL"
        bounded = (
            "The natural-feedback branch exceeded the clamped branch in causal "
            "lifetime and realized propagation, but schedule truncation was too "
            "frequent for a clean exogenous-schedule interpretation."
        )

    else:
        status = "FAILED"
        bounded = (
            "V8 did not establish that endogenous propagation opportunity extends "
            "causal accessibility beyond the frozen exogenous schedule."
        )

    result = {
        "experiment_role": "EXPLORATORY OPPORTUNITY-FEEDBACK TEST",
        "chapter": 18,
        "question": (
            "Can causal accessibility create propagation opportunities that help "
            "causal accessibility continue?"
        ),
        "required_metrics": list(required_metrics),
        "causal_metrics_natural_gt_clamped": causal_metrics_ok,
        "sustained_loss_time_supportive": lifetime_supportive,
        "natural_produces_more_transmissions": transmission_feedback_present,
        "clamped_schedule_truncation_rate": truncation_rate,
        "truncation_rate_acceptable": truncation_ok,
        "status": status,
        "bounded_claim": bounded,
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "self-maintenance",
            "homeostasis",
            "autopoiesis",
            "active boundary",
            "agency",
            "individuality",
            "reproduction",
            "life",
        ],
        "next_question": (
            "If opportunity feedback is supported, intervene directly on the "
            "feedback link itself: selectively suppress or restore propagation "
            "opportunities while holding current material state fixed, before "
            "considering any self-maintenance terminology."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 18 V8 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result





# ============================================================================
# V9 timing-isolation experiment
# ============================================================================

def generate_donor_timing_schedules(
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Generate one donor-derived natural-feedback schedule from independent runs,
    then create SHUFFLED and circularly SHIFTED replays with the exact same
    window multiset and requested total.
    """
    groups = int(profile["donor_groups"])
    radius = int(profile["radius"])
    warmup = int(profile["warmup_steps"])
    start = int(profile["window_start"])
    end = int(profile["window_end"])

    mp = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )

    budgets = {t: [] for t in range(1, end + 1)}

    for g in tqdm(range(groups), desc="V9 donor schedules"):
        total = warmup + end + 8
        gseed = seed + 700_000 + g * 1013
        env = make_environment(total, gseed + 1)
        state = warm_material_checkpoint(
            env, warmup, gseed + 2, radius, crystal_params, mp
        )
        future = env[warmup:]

        for i in range(end):
            elapsed = i + 1
            bit = int(i == profile["experience_pulse_step"])
            forcing = float(future[i]) + profile["message_gain"] * bit
            modified_before = set(state.modified)

            grown, additions, _ = grow_one_step_without_transmission(
                state, forcing, bit, radius, crystal_params, mp
            )
            eligible = eligible_transmission_targets(additions, modified_before)

            if i <= profile["experience_pulse_step"]:
                k = 0
            else:
                k = natural_budget(
                    len(eligible), profile["transmission_fraction"]
                )

            selected, _ = choose_surface_targets_with_budget(
                eligible, grown.occupied, grown.stream_seed, grown.step, k
            )
            state = apply_transmission_targets(grown, selected)
            budgets[elapsed].append(k)

    aligned = {
        t: int(round(float(np.median(budgets[t]))))
        for t in range(1, end + 1)
    }

    window_values = [aligned[t] for t in range(start, end + 1)]

    shuffled_values = list(window_values)
    rng = np.random.default_rng(seed + 880_001)
    rng.shuffle(shuffled_values)

    shift = int(profile["shift_steps"])
    n = len(window_values)
    shifted_values = [
        window_values[(i - shift) % n]
        for i in range(n)
    ]

    shuffled = dict(aligned)
    shifted = dict(aligned)
    for i, t in enumerate(range(start, end + 1)):
        shuffled[t] = int(shuffled_values[i])
        shifted[t] = int(shifted_values[i])

    totals = {
        "aligned": int(sum(aligned[t] for t in range(start, end + 1))),
        "shuffled": int(sum(shuffled[t] for t in range(start, end + 1))),
        "shifted": int(sum(shifted[t] for t in range(start, end + 1))),
    }

    if len(set(totals.values())) != 1:
        raise RuntimeError(f"V9 requested totals mismatch: {totals}")
    if sorted(window_values) != sorted(shuffled_values):
        raise RuntimeError("V9 shuffled multiset mismatch.")
    if sorted(window_values) != sorted(shifted_values):
        raise RuntimeError("V9 shifted multiset mismatch.")

    return {
        "aligned": aligned,
        "shuffled": shuffled,
        "shifted": shifted,
        "totals": totals,
        "donor_groups": groups,
    }


def run_timing_triplet(
    profile: dict,
    crystal_params: CrystalParams,
    schedules: dict,
    seed: int,
    group_index: int,
) -> dict:
    """
    ALIGNED / SHUFFLED / SHIFTED replay under the same environment, CRN,
    surface-biased placement, and requested schedule multiset/total.

    Eligibility may differ after trajectories diverge, so requested budgets can
    be truncated. That truncation and realized applied copy count are explicit
    validity diagnostics.
    """
    radius = int(profile["radius"])
    warmup = int(profile["warmup_steps"])
    end = int(profile["window_end"])

    total = warmup + end + 8
    gseed = seed + 100_000 + group_index * 1009
    env = make_environment(total, gseed + 1)

    mp = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )
    base = warm_material_checkpoint(
        env, warmup, gseed + 2, radius, crystal_params, mp
    )

    branches = ("aligned", "shuffled", "shifted")
    states = {b: clone_material_state(base) for b in branches}
    observations = {b: {} for b in branches}
    future = env[warmup:]
    logs = []

    for i in range(end):
        elapsed = i + 1
        bit = int(i == profile["experience_pulse_step"])
        forcing = float(future[i]) + profile["message_gain"] * bit
        row = {"elapsed_step": elapsed}

        for branch in branches:
            modified_before = set(states[branch].modified)
            grown, additions, _ = grow_one_step_without_transmission(
                states[branch], forcing, bit, radius, crystal_params, mp
            )
            eligible = eligible_transmission_targets(additions, modified_before)

            requested = int(schedules[branch][elapsed])
            applied = min(requested, len(eligible))

            selected, meta = choose_surface_targets_with_budget(
                eligible,
                grown.occupied,
                grown.stream_seed,
                grown.step,
                applied,
            )
            states[branch] = apply_transmission_targets(grown, selected)
            observations[branch][elapsed] = clone_material_state(states[branch])

            row[branch] = {
                "eligible_count": int(len(eligible)),
                "requested_budget": requested,
                "applied_budget": int(applied),
                "truncated": int(applied < requested),
                "mean_selected_surface_exposure": meta[
                    "mean_selected_surface_exposure"
                ],
            }

            frac = capacity_fraction_occupied(states[branch].occupied, radius)
            if frac >= profile["max_capacity_fraction"]:
                raise RuntimeError(
                    f"V9 saturation: branch={branch}, elapsed={elapsed}, "
                    f"fraction={frac:.3f}"
                )

        logs.append(row)

    return {
        "states": observations,
        "future": future,
        "logs": logs,
    }


def stage_0_freeze_timing_schedules(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    donor = generate_donor_timing_schedules(profile, crystal_params, seed)
    start, end = profile["window_start"], profile["window_end"]

    result = {
        "role": "V9 FROZEN TIMING SCHEDULES",
        "donor_groups": donor["donor_groups"],
        "window": {"start": start, "end": end},
        "shift_steps": profile["shift_steps"],
        "requested_totals": donor["totals"],
        "exact_same_multiset_and_total": True,
        "aligned": {str(t): donor["aligned"][t] for t in range(start, end + 1)},
        "shuffled": {str(t): donor["shuffled"][t] for t in range(start, end + 1)},
        "shifted": {str(t): donor["shifted"][t] for t in range(start, end + 1)},
        "status": "MEASURED",
        "scientific_role": (
            "The three replay schedules contain the same donor-derived budget "
            "multiset and total. Only their temporal ordering differs."
        ),
    }
    reporter.json("stage-00-frozen-timing-schedules.json", result)
    reporter.stage(
        "stage-00-frozen-timing-schedules.md",
        "Stage 0 — Freeze Aligned, Shuffled, and Shifted Schedules",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return {
        **result,
        "_schedules": {
            "aligned": donor["aligned"],
            "shuffled": donor["shuffled"],
            "shifted": donor["shifted"],
        },
    }


def stage_1_replay_integrity(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    schedules: dict,
    seed: int,
) -> dict:
    groups = profile["groups"]
    start, end = profile["window_start"], profile["window_end"]
    branches = ("aligned", "shuffled", "shifted")

    requested = {b: [] for b in branches}
    applied = {b: [] for b in branches}
    trunc = {b: [] for b in branches}

    for g in tqdm(range(groups), desc="V9 replay integrity"):
        run = run_timing_triplet(
            profile, crystal_params, schedules, seed + 200_000, g
        )
        for b in branches:
            requested[b].append(sum(
                run["logs"][t - 1][b]["requested_budget"]
                for t in range(start, end + 1)
            ))
            applied[b].append(sum(
                run["logs"][t - 1][b]["applied_budget"]
                for t in range(start, end + 1)
            ))
            trunc[b].extend(
                run["logs"][t - 1][b]["truncated"]
                for t in range(start, end + 1)
            )

    summary = {}
    for i, b in enumerate(branches):
        summary[b] = {
            "requested_total": bootstrap_mean_ci(
                requested[b], profile["bootstrap_reps"], seed + 210_000 + i * 100
            ),
            "applied_total": bootstrap_mean_ci(
                applied[b], profile["bootstrap_reps"], seed + 211_000 + i * 100
            ),
            "truncation_rate": float(np.mean(trunc[b])),
        }

    requested_equal = len({
        summary[b]["requested_total"]["mean"] for b in branches
    }) == 1

    result = {
        "groups": groups,
        "summary": summary,
        "requested_totals_exactly_equal": requested_equal,
        "status": "MEASURED",
        "bounded_statement": (
            "Requested copy quantity is exact by construction. Applied copy "
            "quantity and truncation are audited because timing can alter later "
            "eligibility."
        ),
    }
    reporter.json("stage-01-replay-integrity.json", result)
    reporter.stage(
        "stage-01-replay-integrity.md",
        "Stage 1 — Replay Integrity",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_2_timing_effect(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    schedules: dict,
    seed: int,
    image_dir: Path,
) -> dict:
    groups = profile["groups"]
    radius = profile["radius"]
    start, end = profile["window_start"], profile["window_end"]
    branches = ("aligned", "shuffled", "shifted")

    metrics = {
        b: {
            "access_fraction_auc": [],
            "contact_count_auc": [],
            "probability_leverage_auc": [],
            "total_realized_flips": [],
            "sustained_loss_time": [],
            "applied_transmissions": [],
        }
        for b in branches
    }

    trajectories = {
        b: {
            t: {
                "frontier_exposed_fraction": [],
                "frontier_contact": [],
                "sum_delta_p": [],
                "realized_flips": [],
            }
            for t in range(start, end + 1)
        }
        for b in branches
    }
    trunc = {b: [] for b in branches}

    for g in tqdm(range(groups), desc="V9 timing effect"):
        run = run_timing_triplet(
            profile, crystal_params, schedules, seed + 300_000, g
        )
        future = run["future"]

        for b in branches:
            mp = MaterialParams(
                write_probability=profile["write_probability"],
                modified_neighbor_gain=profile["modified_neighbor_gain"],
                transmission_fraction=profile["transmission_fraction"],
            )
            frac, contact, leverage, flips = {}, {}, {}, {}

            for t in range(start, end + 1):
                state = run["states"][b][t]
                access = material_accessibility_metrics(state, radius)
                audit = frontier_material_causal_audit(
                    state, float(future[t]), radius, crystal_params, mp
                )

                frac[t] = access["frontier_exposed_fraction"]
                contact[t] = access["frontier_cells_with_modified_neighbor"]
                leverage[t] = audit["sum_delta_p"]
                flips[t] = audit["realized_causal_flips"]

                trajectories[b][t]["frontier_exposed_fraction"].append(frac[t])
                trajectories[b][t]["frontier_contact"].append(contact[t])
                trajectories[b][t]["sum_delta_p"].append(leverage[t])
                trajectories[b][t]["realized_flips"].append(flips[t])

            metrics[b]["access_fraction_auc"].append(
                discrete_auc(frac, start, end)
            )
            metrics[b]["contact_count_auc"].append(
                discrete_auc(contact, start, end)
            )
            metrics[b]["probability_leverage_auc"].append(
                discrete_auc(leverage, start, end)
            )
            metrics[b]["total_realized_flips"].append(
                discrete_auc(flips, start, end)
            )
            metrics[b]["sustained_loss_time"].append(
                sustained_zero_loss_time(
                    contact, start, end, profile["sustained_zero_steps"]
                )
            )
            metrics[b]["applied_transmissions"].append(sum(
                run["logs"][t - 1][b]["applied_budget"]
                for t in range(start, end + 1)
            ))
            trunc[b].extend(
                run["logs"][t - 1][b]["truncated"]
                for t in range(start, end + 1)
            )

    summary = {}
    for i, b in enumerate(branches):
        summary[b] = {
            k: bootstrap_mean_ci(
                v, profile["bootstrap_reps"], seed + 310_000 + i * 1000 + j
            )
            for j, (k, v) in enumerate(metrics[b].items())
        }
        summary[b]["truncation_rate"] = float(np.mean(trunc[b]))

    trajectory_summary = {
        b: {
            str(t): {
                k: float(np.mean(v))
                for k, v in trajectories[b][t].items()
            }
            for t in range(start, end + 1)
        }
        for b in branches
    }

    required_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
    )
    tests = {}
    for i, metric in enumerate(required_metrics):
        tests[metric] = {
            "aligned_gt_shuffled": paired_randomization_difference_test(
                metrics["shuffled"][metric],
                metrics["aligned"][metric],
                profile["permutations"],
                seed + 320_000 + i * 100,
                alternative="greater",
            ),
            "aligned_gt_shifted": paired_randomization_difference_test(
                metrics["shifted"][metric],
                metrics["aligned"][metric],
                profile["permutations"],
                seed + 330_000 + i * 100,
                alternative="greater",
            ),
        }

    result = {
        "groups": groups,
        "window": {"start": start, "end": end},
        "summary": summary,
        "trajectory_summary": trajectory_summary,
        "paired_tests": tests,
        "status": "MEASURED",
        "bounded_statement": (
            "V9 tests temporal alignment while preserving the donor-derived "
            "requested copy multiset, requested total, and surface placement rule."
        ),
    }
    reporter.json("stage-02-timing-effect.json", result)
    reporter.stage(
        "stage-02-timing-effect.md",
        "Stage 2 — Does Timing Matter Independently of Copy Quantity?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = list(range(start, end + 1))
    for b in branches:
        ax.plot(
            xs,
            [
                trajectory_summary[b][str(t)]["frontier_exposed_fraction"]
                for t in xs
            ],
            marker="o",
            label=b,
        )
    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("V9 temporal alignment of propagation schedule")
    ax.legend()
    fig.tight_layout()
    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(image_dir / "ch18-v9-01-timing-alignment.png", dpi=160)
    plt.close(fig)

    return result


def stage_3_timing_checkpoints(
    reporter: Reporter,
    profile: dict,
    stage2: dict,
) -> dict:
    result = {
        "role": "SECONDARY DESCRIPTIVE",
        "steps": profile["descriptive_steps"],
        "results": {
            str(t): {
                b: stage2["trajectory_summary"][b][str(t)]
                for b in ("aligned", "shuffled", "shifted")
            }
            for t in profile["descriptive_steps"]
        },
        "cannot_change_primary_decision": True,
        "status": "MEASURED",
    }
    reporter.json("stage-03-descriptive-checkpoints.json", result)
    reporter.stage(
        "stage-03-descriptive-checkpoints.md",
        "Stage 3 — Secondary Timing Checkpoints",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_timing_verdict(
    reporter: Reporter,
    profile: dict,
    stage0: dict,
    stage1: dict,
    stage2: dict,
) -> dict:
    alpha = profile["alpha"]
    required_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
    )

    requested_valid = bool(
        stage0["exact_same_multiset_and_total"]
        and stage1["requested_totals_exactly_equal"]
    )
    aligned_beats_both = all(
        stage2["paired_tests"][m]["aligned_gt_shuffled"]["p_value"] < alpha
        and stage2["paired_tests"][m]["aligned_gt_shifted"]["p_value"] < alpha
        for m in required_metrics
    )

    max_truncation = max(
        stage2["summary"][b]["truncation_rate"]
        for b in ("aligned", "shuffled", "shifted")
    )
    truncation_ok = max_truncation <= 0.10

    applied = {
        b: stage2["summary"][b]["applied_transmissions"]["mean"]
        for b in ("aligned", "shuffled", "shifted")
    }
    mean_applied = float(np.mean(list(applied.values())))
    spread = max(applied.values()) - min(applied.values())
    relative_spread = spread / mean_applied if mean_applied else 0.0
    applied_balance_ok = relative_spread <= 0.05

    if requested_valid and aligned_beats_both and truncation_ok and applied_balance_ok:
        status = "SUPPORTED"
        claim = (
            "With the same donor-derived requested transmission multiset and "
            "total, the same surface-biased placement rule, low truncation, and "
            "closely balanced realized copy quantity, original temporal alignment "
            "produced greater integrated causal accessibility, probability "
            "leverage, and realized causal work than shuffled or shifted replay."
        )
    elif requested_valid and aligned_beats_both:
        status = "PROVISIONAL"
        claim = (
            "Aligned timing outperformed shuffled and shifted timing on all "
            "predeclared causal metrics, but truncation or realized-copy imbalance "
            "prevented a clean timing-only interpretation."
        )
    else:
        status = "FAILED"
        claim = (
            "V9 did not establish that temporal alignment independently improves "
            "causal lifetime."
        )

    result = {
        "experiment_role": "EXPLORATORY TEMPORAL-ALIGNMENT TEST",
        "chapter": 18,
        "question": (
            "Does the timing of propagated state matter independently of its "
            "amount and placement?"
        ),
        "required_metrics": list(required_metrics),
        "requested_quantity_invariant_valid": requested_valid,
        "aligned_beats_shuffled_and_shifted": aligned_beats_both,
        "max_truncation_rate": max_truncation,
        "truncation_rate_acceptable": truncation_ok,
        "applied_transmission_means": applied,
        "applied_relative_spread": relative_spread,
        "applied_copy_balance_acceptable": applied_balance_ok,
        "status": status,
        "bounded_claim": claim,
        "nonclaims": [
            "memory", "learning", "adaptation", "self-maintenance",
            "homeostasis", "autopoiesis", "active boundary", "agency",
            "individuality", "reproduction", "life",
        ],
        "next_question": (
            "If temporal alignment is supported, ask whether a second experience "
            "can alter which temporal propagation pattern is expressed, before "
            "using memory or adaptation terminology."
        ),
    }
    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 18 V9 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260822)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("research/digital-life/ch18-persistent-material-state-v9"),
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    profile["donor_groups"] = int(profile["groups"])
    profile["shift_steps"] = 4

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
        "run_type": "EXPLORATORY TEMPORAL-ALIGNMENT TEST",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "v8_result_being_followed": (
            "Natural feedback improved integrated causal metrics, but the run did "
            "not establish that simply making more copies was the mechanism."
        ),
        "v9_design": (
            "Generate a donor-derived schedule independently, then replay the same "
            "budget multiset and total as aligned, shuffled, and circularly shifted "
            "timing under the same surface-biased placement rule."
        ),
        "scientific_boundary": (
            "Timing only. No claim of memory, learning, adaptation, self-maintenance, "
            "homeostasis, autopoiesis, or life."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V9 — TEMPORAL ALIGNMENT")
    print(
        f"profile={args.profile} groups={profile['groups']} "
        f"window={profile['window_start']}..{profile['window_end']} "
        f"shift={profile['shift_steps']}"
    )
    print("=" * 78)

    s0 = stage_0_freeze_timing_schedules(
        reporter, profile, crystal_params, args.seed
    )
    schedules = s0["_schedules"]

    s1 = stage_1_replay_integrity(
        reporter, profile, crystal_params, schedules, args.seed
    )
    s2 = stage_2_timing_effect(
        reporter, profile, crystal_params, schedules, args.seed, args.image_dir
    )
    s3 = stage_3_timing_checkpoints(reporter, profile, s2)
    s4 = stage_4_timing_verdict(reporter, profile, s0, s1, s2)

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_0_status": s0["status"],
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "final_status": s4["status"],
        "next_question": s4["next_question"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("CHAPTER 18 V9 COMPLETE")
    print(f"timing_schedules={s0['status']}")
    print(f"replay_integrity={s1['status']}")
    print(f"timing_effect={s2['status']}")
    print(f"final_status={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
