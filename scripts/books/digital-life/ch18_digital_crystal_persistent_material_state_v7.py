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
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v7"
SCHEMA_VERSION = 7

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

        # Exact matched copy quantity from v6.
        "transmission_fraction": 0.50,
        "placement_policies": [
            "interior_biased",
            "random_matched",
            "surface_biased",
        ],

        # V7 primary integrated observation window.
        "window_start": 5,
        "window_end": 18,

        # Lifetime definition:
        # first elapsed step such that frontier contact is zero for this many
        # consecutive observed updates. If never reached, censor at window_end+1.
        "sustained_zero_steps": 3,

        # Secondary descriptive checkpoints only.
        "descriptive_steps": [5, 8, 10, 12, 14, 18],

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
        "placement_policies": [
            "interior_biased",
            "random_matched",
            "surface_biased",
        ],
        "window_start": 5,
        "window_end": 18,
        "sustained_zero_steps": 3,
        "descriptive_steps": [5, 8, 10, 12, 14, 18],
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
        "placement_policies": [
            "interior_biased",
            "random_matched",
            "surface_biased",
        ],
        "window_start": 5,
        "window_end": 18,
        "sustained_zero_steps": 3,
        "descriptive_steps": [5, 8, 10, 12, 14, 18],
        "bootstrap_reps": 5000,
        "permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
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
        path = self.root / "ch18-persistent-material-state-v7-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V7 Integrated Causal Lifetime)\n\n"
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


def stage_0_extension_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Reuse and harden the v6 exact matched-budget invariant.
    """
    policies = profile["placement_policies"]

    synthetic_eligible = {
        "interior_biased": [(0, 1), (1, 1), (2, 0), (2, -1)],
        "random_matched": [(0, 1), (1, 1), (2, 0), (2, -1), (3, -1)],
        "surface_biased": [(0, 1), (1, 1), (2, 0), (2, -1), (3, -1), (3, -2)],
    }

    budget = shared_transmission_budget(
        [len(synthetic_eligible[p]) for p in policies],
        profile["transmission_fraction"],
    )

    synthetic_occ = {
        (0, 0), (1, 0), (1, -1), (0, -1),
        (0, 1), (1, 1), (2, 0), (2, -1), (3, -1), (3, -2),
    }

    selected_counts = {}
    for p in policies:
        selected, _ = choose_targets_with_exact_budget(
            synthetic_eligible[p],
            synthetic_occ,
            seed,
            99,
            budget,
            p,
        )
        selected_counts[p] = len(selected)

    valid = (
        len(set(selected_counts.values())) == 1
        and all(v == budget for v in selected_counts.values())
    )

    if not valid:
        raise RuntimeError("V7 exact matched-budget unit audit failed.")

    result = {
        "role": "V7 EXACT MATCHED-BUDGET VALIDITY GATE",
        "canonical_model_modified": False,
        "placement_policies": policies,
        "transmission_fraction": profile["transmission_fraction"],
        "shared_budget": budget,
        "selected_counts": selected_counts,
        "budget_unit_check_pass": valid,
        "window_start": profile["window_start"],
        "window_end": profile["window_end"],
        "sustained_zero_steps": profile["sustained_zero_steps"],
        "scientific_role": (
            "V7 preserves the exact matched-copy-quantity control from v6 and "
            "changes only the outcome definition from a single late endpoint to "
            "predeclared integrated causal-lifetime measures."
        ),
    }

    reporter.json("stage-00-v7-validity-gate.json", result)
    reporter.stage(
        "stage-00-v7-validity-gate.md",
        "Stage 0 — V7 Validity Gate",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_1_run_integrity(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Verify exact per-step and cumulative transmission matching in all groups.
    """
    groups = profile["groups"]
    policies = profile["placement_policies"]
    end = profile["window_end"]

    final_counts = {p: [] for p in policies}
    all_valid = []

    for g in tqdm(range(groups), desc="Stage 1 budget integrity"):
        run = run_synchronized_policy_trajectory(
            profile,
            crystal_params,
            seed + 200_000,
            g,
            end,
        )

        counts = run["final_cumulative"]
        valid = len(set(counts.values())) == 1
        all_valid.append(valid)

        for p in policies:
            final_counts[p].append(counts[p])

    if not all(all_valid):
        raise RuntimeError(
            "V7 invalid: exact cumulative transmission budget failed."
        )

    summary = {
        p: bootstrap_mean_ci(
            final_counts[p],
            profile["bootstrap_reps"],
            seed + 210_000 + i * 100,
        )
        for i, p in enumerate(policies)
    }

    result = {
        "groups": groups,
        "all_groups_exact_cumulative_budget_match": all(all_valid),
        "final_cumulative_transmissions": summary,
        "status": "MEASURED",
        "bounded_statement": (
            "Every branch copied exactly the same number of cells in every "
            "paired group through the full V7 observation window."
        ),
    }

    reporter.json("stage-01-budget-integrity.json", result)
    reporter.stage(
        "stage-01-budget-integrity.md",
        "Stage 1 — Exact Copy-Quantity Integrity",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_2_integrated_causal_lifetime(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    """
    Primary V7 experiment.

    For each paired group and policy, integrate over the predeclared window:
      - frontier exposed fraction AUC
      - frontier contact-count AUC
      - sum(delta_p) AUC
      - total realized CRN causal flips
      - sustained zero-contact loss time
    """
    groups = profile["groups"]
    policies = profile["placement_policies"]
    radius = profile["radius"]
    start = profile["window_start"]
    end = profile["window_end"]
    zero_n = profile["sustained_zero_steps"]

    per_policy = {
        p: {
            "access_fraction_auc": [],
            "contact_count_auc": [],
            "probability_leverage_auc": [],
            "total_realized_flips": [],
            "sustained_loss_time": [],
        }
        for p in policies
    }

    trajectory_means = {
        p: {
            t: {
                "frontier_exposed_fraction": [],
                "frontier_contact": [],
                "sum_delta_p": [],
                "realized_flips": [],
            }
            for t in range(start, end + 1)
        }
        for p in policies
    }

    for g in tqdm(
        range(groups),
        desc="Stage 2 integrated causal lifetime",
    ):
        run = run_synchronized_policy_trajectory(
            profile,
            crystal_params,
            seed + 300_000,
            g,
            end,
        )

        future = run["future"]

        for p in policies:
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
                state = run["states"][p][t]
                access = material_accessibility_metrics(state, radius)
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

                trajectory_means[p][t][
                    "frontier_exposed_fraction"
                ].append(frac_by_t[t])
                trajectory_means[p][t][
                    "frontier_contact"
                ].append(contact_by_t[t])
                trajectory_means[p][t][
                    "sum_delta_p"
                ].append(leverage_by_t[t])
                trajectory_means[p][t][
                    "realized_flips"
                ].append(flips_by_t[t])

            per_policy[p]["access_fraction_auc"].append(
                discrete_auc(frac_by_t, start, end)
            )
            per_policy[p]["contact_count_auc"].append(
                discrete_auc(contact_by_t, start, end)
            )
            per_policy[p]["probability_leverage_auc"].append(
                discrete_auc(leverage_by_t, start, end)
            )
            per_policy[p]["total_realized_flips"].append(
                discrete_auc(flips_by_t, start, end)
            )
            per_policy[p]["sustained_loss_time"].append(
                sustained_zero_loss_time(
                    contact_by_t,
                    start,
                    end,
                    zero_n,
                )
            )

    summary = {}
    for pi, p in enumerate(policies):
        summary[p] = {
            key: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 310_000 + pi * 1000 + j,
            )
            for j, (key, vals) in enumerate(per_policy[p].items())
        }

    trajectory_summary = {}
    for p in policies:
        trajectory_summary[p] = {}
        for t in range(start, end + 1):
            trajectory_summary[p][str(t)] = {
                k: float(np.mean(v))
                for k, v in trajectory_means[p][t].items()
            }

    # Primary integrated predictions.
    mean_access_auc = {
        p: summary[p]["access_fraction_auc"]["mean"]
        for p in policies
    }
    mean_leverage_auc = {
        p: summary[p]["probability_leverage_auc"]["mean"]
        for p in policies
    }
    mean_flips = {
        p: summary[p]["total_realized_flips"]["mean"]
        for p in policies
    }
    mean_loss = {
        p: summary[p]["sustained_loss_time"]["mean"]
        for p in policies
    }

    ordering = {
        "access_fraction_auc": ordered_three_way(mean_access_auc),
        "probability_leverage_auc": ordered_three_way(mean_leverage_auc),
        "total_realized_flips": ordered_three_way(mean_flips),
        "sustained_loss_time": ordered_three_way(mean_loss),
    }

    # Directional paired randomization tests: interior<random and random<surface.
    paired_tests = {}
    test_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
        "sustained_loss_time",
    )
    for metric_index, metric in enumerate(test_metrics):
        paired_tests[metric] = {
            "random_gt_interior": paired_randomization_difference_test(
                per_policy["interior_biased"][metric],
                per_policy["random_matched"][metric],
                profile["permutations"],
                seed + 320_000 + metric_index * 100,
                alternative="greater",
            ),
            "surface_gt_random": paired_randomization_difference_test(
                per_policy["random_matched"][metric],
                per_policy["surface_biased"][metric],
                profile["permutations"],
                seed + 330_000 + metric_index * 100,
                alternative="greater",
            ),
        }

    group_ordering = {
        metric: paired_sign_test_order(
            per_policy["interior_biased"][metric],
            per_policy["random_matched"][metric],
            per_policy["surface_biased"][metric],
        )
        for metric in (
            "access_fraction_auc",
            "probability_leverage_auc",
            "total_realized_flips",
            "sustained_loss_time",
        )
    }

    result = {
        "groups": groups,
        "window_start": start,
        "window_end": end,
        "sustained_zero_steps": zero_n,
        "summary": summary,
        "trajectory_summary": trajectory_summary,
        "mean_ordering": ordering,
        "paired_directional_tests": paired_tests,
        "per_group_ordering": group_ordering,
        "status": "MEASURED",
        "bounded_statement": (
            "V7 measures causal lifetime over a frozen observation window rather "
            "than choosing a single late endpoint after observing the trajectory."
        ),
    }

    reporter.json("stage-02-integrated-causal-lifetime.json", result)
    reporter.stage(
        "stage-02-integrated-causal-lifetime.md",
        "Stage 2 — Does Placement Change Causal Lifetime?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    # Evidence plot: frontier exposure across the entire frozen window.
    fig, ax = plt.subplots(figsize=(9, 5))
    xs = list(range(start, end + 1))

    for p in policies:
        ys = [
            trajectory_summary[p][str(t)]["frontier_exposed_fraction"]
            for t in xs
        ]
        ax.plot(xs, ys, marker="o", label=p)

    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("V7 matched-budget causal-access trajectory")
    ax.legend()
    fig.tight_layout()

    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v7-01-causal-lifetime-window.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_3_descriptive_checkpoints(
    reporter: Reporter,
    profile: dict,
    stage2: dict,
) -> dict:
    """
    Secondary descriptive snapshots only.

    They cannot alter the V7 primary integrated decision.
    """
    steps = profile["descriptive_steps"]
    policies = profile["placement_policies"]

    out = {}

    for t in steps:
        out[str(t)] = {}
        for p in policies:
            row = stage2["trajectory_summary"][p][str(t)]
            out[str(t)][p] = row

    result = {
        "role": "SECONDARY DESCRIPTIVE",
        "steps": steps,
        "results": out,
        "cannot_change_primary_decision": True,
        "status": "MEASURED",
    }

    reporter.json("stage-03-descriptive-checkpoints.json", result)
    reporter.stage(
        "stage-03-descriptive-checkpoints.md",
        "Stage 3 — Secondary Descriptive Checkpoints",
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
    """
    Primary decision requires:
      - exact budget invariant
      - predicted mean ordering for access AUC, leverage AUC, realized flips
      - both adjacent directional paired tests p < alpha for the three causal metrics

    Sustained loss time is supportive but not required because right-censoring at
    window_end+1 can create ties.
    """
    alpha = profile["alpha"]

    budget_valid = bool(
        stage0["budget_unit_check_pass"]
        and stage1["all_groups_exact_cumulative_budget_match"]
    )

    required_metrics = (
        "access_fraction_auc",
        "probability_leverage_auc",
        "total_realized_flips",
    )

    mean_order_ok = all(
        stage2["mean_ordering"][m]
        for m in required_metrics
    )

    directional_tests_ok = all(
        stage2["paired_directional_tests"][m]["random_gt_interior"]["p_value"]
        < alpha
        and stage2["paired_directional_tests"][m]["surface_gt_random"]["p_value"]
        < alpha
        for m in required_metrics
    )

    lifetime_order_supportive = bool(
        stage2["mean_ordering"]["sustained_loss_time"]
    )

    if not budget_valid:
        status = "UNTESTED"
        bounded = (
            "The exact matched-copy-quantity invariant failed, so causal-lifetime "
            "differences cannot be attributed to spatial placement."
        )

    elif mean_order_ok and directional_tests_ok:
        status = "SUPPORTED"
        bounded = (
            "With exact per-step and cumulative copy quantity held fixed, "
            "interior, random, and surface placement showed the predeclared "
            "ordered difference in integrated frontier accessibility, integrated "
            "local probability leverage, and total realized causal attachment "
            "flips over the frozen observation window."
        )

    elif mean_order_ok:
        status = "PROVISIONAL"
        bounded = (
            "The integrated metrics followed the predicted interior < random < "
            "surface mean ordering, but the paired directional evidence did not "
            "clear all predeclared tests."
        )

    else:
        status = "FAILED"
        bounded = (
            "Under exact matched copy quantity, V7 did not establish the "
            "predeclared interior < random < surface ordering across the integrated "
            "causal-lifetime metrics."
        )

    result = {
        "experiment_role": "EXPLORATORY INTEGRATED CAUSAL-LIFETIME TEST",
        "chapter": 18,
        "question": (
            "Does spatial placement change how long an exactly fixed quantity of "
            "propagated material remains causally available to growth?"
        ),
        "window": {
            "start": profile["window_start"],
            "end": profile["window_end"],
        },
        "budget_invariant_valid": budget_valid,
        "required_metrics": list(required_metrics),
        "mean_ordering_supported_for_required_metrics": mean_order_ok,
        "paired_directional_tests_supported": directional_tests_ok,
        "sustained_loss_time_order_supportive": lifetime_order_supportive,
        "status": status,
        "bounded_claim": bounded,
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "self-maintenance",
            "homeostasis",
            "attention",
            "active boundary",
            "information storage",
            "biological inheritance",
            "agency",
            "individuality",
            "reproduction",
            "life",
        ],
        "next_question": (
            "If causal lifetime is supported, restore the opportunity feedback "
            "observed in v5 and test whether causal accessibility helps generate "
            "future opportunities for its own continuation, while keeping the "
            "claim below self-maintenance."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 18 V7 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260820)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch18-persistent-material-state-v7"
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
        "run_type": "EXPLORATORY INTEGRATED CAUSAL-LIFETIME TEST",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "v6_result_being_followed": (
            "The exact matched-copy-quantity late t=14 endpoint failed, while an "
            "earlier exploratory t=8 pattern showed interior < random < surface "
            "for frontier access, probability leverage, and realized causal flips."
        ),
        "v7_design": (
            "Keep exact matched per-step and cumulative transmission counts, but "
            "replace a single late endpoint with predeclared integrated causal-"
            "lifetime measures over a frozen observation window."
        ),
        "scientific_boundary": (
            "Causal lifetime only. No claim of memory, learning, adaptation, "
            "self-maintenance, homeostasis, active boundary, or life."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V7 — INTEGRATED CAUSAL LIFETIME")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']}"
    )
    print(
        f"window={profile['window_start']}..{profile['window_end']} "
        f"sustained_zero={profile['sustained_zero_steps']}"
    )
    print("=" * 78)

    s0 = stage_0_extension_audit(
        reporter, profile, crystal_params, args.seed
    )

    s1 = stage_1_run_integrity(
        reporter, profile, crystal_params, args.seed
    )

    s2 = stage_2_integrated_causal_lifetime(
        reporter, profile, crystal_params,
        args.seed, args.image_dir,
    )

    s3 = stage_3_descriptive_checkpoints(
        reporter, profile, s2
    )

    s4 = stage_4_verdict(
        reporter, profile, s0, s1, s2
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "final_status": s4["status"],
        "next_question": s4["next_question"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("CHAPTER 18 V7 COMPLETE")
    print(f"budget_integrity={s1['status']}")
    print(f"integrated_causal_lifetime={s2['status']}")
    print(f"descriptive_checkpoints={s3['status']}")
    print(f"final_status={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
