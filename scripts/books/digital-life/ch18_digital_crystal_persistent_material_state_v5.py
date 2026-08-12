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
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v5"
SCHEMA_VERSION = 5

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
    Chapter 18 v5 experimental material-state extension.

    A cell is either:
        occupied-normal
        occupied-modified

    Existing rules:
        - an explicit pulse writes modified state to occupied boundary cells;
        - modified state persists irreversibly;
        - modified occupied neighbours bias later frontier attachment.

    V5 changes ONLY the propagation allocation rule.

    Eligible propagation targets are newly attached cells adjacent to material
    that was already modified before the step.

    A fixed transmission_fraction determines a per-step budget K:
        K = round(transmission_fraction * eligible_new_cells)

    The same K is used for both placement policies:

        uniform_budget:
            choose K eligible new cells by keyed pseudorandom rank.

        surface_biased_budget:
            choose K eligible new cells with greatest post-attachment outward
            exposure; keyed pseudorandom rank breaks ties.

    Therefore the policies copy the state into the same NUMBER of eligible new
    cells at each step whenever they start from the same eligible set. The
    experimental question is whether WHERE the state is placed matters.

    No global memory register, history list, decoder, learned parameter,
    target morphology, or biological inheritance claim is introduced.
    """
    write_probability: float = 0.20
    modified_neighbor_gain: float = 0.30
    transmission_fraction: float = 0.50
    transmission_policy: str = "uniform_budget"


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


def choose_transmission_targets(
    additions: Sequence[Cell],
    occupied_after: Set[Cell],
    modified_before: Set[Cell],
    stream_seed: int,
    step: int,
    transmission_fraction: float,
    policy: str,
) -> Tuple[List[Cell], dict]:
    """
    Select which eligible newly attached cells inherit modified material.

    The per-step budget K depends only on the number of eligible additions and
    transmission_fraction. Placement policy changes allocation, not budget.
    """
    eligible = [
        cell
        for cell in additions
        if any(nb in modified_before for nb in neighbors(cell))
    ]

    n = len(eligible)
    if n == 0 or transmission_fraction <= 0.0:
        return [], {
            "eligible_count": int(n),
            "budget": 0,
            "selected_count": 0,
            "mean_selected_surface_exposure": 0.0,
            "mean_eligible_surface_exposure": (
                float(np.mean([
                    surface_exposure_after_attachment(c, occupied_after)
                    for c in eligible
                ]))
                if eligible else 0.0
            ),
        }

    budget = int(round(float(transmission_fraction) * n))
    budget = max(0, min(n, budget))

    if budget == 0:
        return [], {
            "eligible_count": int(n),
            "budget": 0,
            "selected_count": 0,
            "mean_selected_surface_exposure": 0.0,
            "mean_eligible_surface_exposure": float(np.mean([
                surface_exposure_after_attachment(c, occupied_after)
                for c in eligible
            ])),
        }

    if policy == "uniform_budget":
        ranked = sorted(
            eligible,
            key=lambda c: (
                transmission_rank_uniform(stream_seed, step, c),
                c,
            ),
        )
        selected = ranked[:budget]

    elif policy == "surface_biased_budget":
        ranked = sorted(
            eligible,
            key=lambda c: (
                -surface_exposure_after_attachment(c, occupied_after),
                transmission_rank_uniform(stream_seed, step, c),
                c,
            ),
        )
        selected = ranked[:budget]

    elif policy == "none":
        selected = []

    else:
        raise ValueError(f"Unknown transmission policy: {policy!r}")

    eligible_exposure = [
        surface_exposure_after_attachment(c, occupied_after)
        for c in eligible
    ]
    selected_exposure = [
        surface_exposure_after_attachment(c, occupied_after)
        for c in selected
    ]

    return selected, {
        "eligible_count": int(n),
        "budget": int(budget),
        "selected_count": int(len(selected)),
        "mean_selected_surface_exposure": (
            float(np.mean(selected_exposure)) if selected_exposure else 0.0
        ),
        "mean_eligible_surface_exposure": (
            float(np.mean(eligible_exposure)) if eligible_exposure else 0.0
        ),
    }


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
    Chapter 18 v5 material-state growth step.

    Ordering:
      1. growth uses material state existing BEFORE this step;
      2. new cells attach under cell-keyed CRN;
      3. among newly attached cells adjacent to pre-existing modified material,
         a matched transmission budget is allocated according to policy;
      4. an explicit pulse may directly write boundary material;
      5. newly transmitted/written state affects growth only on later steps.

    Surface-biased and uniform policies differ in allocation, not nominal budget.
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

    transmitted, transmission_meta = choose_transmission_targets(
        additions=additions,
        occupied_after=occupied,
        modified_before=modified_before,
        stream_seed=state.stream_seed,
        step=next_step,
        transmission_fraction=material_params.transmission_fraction,
        policy=material_params.transmission_policy,
    )

    for cell in transmitted:
        modified.add(cell)

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

    # Existing callers expect the third item to be "new material state count".
    # In V5 it includes both transmitted and direct-write state.
    return out, len(additions), len(transmitted) + newly_written

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
        "groups": 48,
        "radius": 64,
        "warmup_steps": 14,

        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,

        # Equal copying budget across allocation policies.
        "transmission_fraction": 0.50,
        "transmission_policies": [
            "none",
            "uniform_budget",
            "surface_biased_budget",
        ],

        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "cell_audit_steps": [8, 10, 12, 14, 18],

        "late_ablation_step": 14,
        "late_ablation_followup": 4,

        "permutations": 2000,
        "bootstrap_reps": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 96,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "transmission_fraction": 0.50,
        "transmission_policies": [
            "none",
            "uniform_budget",
            "surface_biased_budget",
        ],
        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "cell_audit_steps": [8, 10, 12, 14, 18],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "permutations": 4000,
        "bootstrap_reps": 2000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 192,
        "radius": 64,
        "warmup_steps": 14,
        "experience_pulse_step": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "transmission_fraction": 0.50,
        "transmission_policies": [
            "none",
            "uniform_budget",
            "surface_biased_budget",
        ],
        "observation_steps": [4, 5, 6, 7, 8, 10, 12, 14, 18, 22],
        "cell_audit_steps": [8, 10, 12, 14, 18],
        "late_ablation_step": 14,
        "late_ablation_followup": 4,
        "permutations": 8000,
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
        path = self.root / "ch18-persistent-material-state-v5-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V5 Surface-Biased Transmission)\n\n"
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
    Audit exact reproducibility and equal-budget placement logic.
    """
    radius = profile["radius"]
    steps = profile["warmup_steps"] + 10
    env = make_environment(steps, seed + 1)

    reproducible = {}

    for policy in profile["transmission_policies"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            transmission_fraction=profile["transmission_fraction"],
            transmission_policy=policy,
        )

        a = initial_material_state(seed + 100)
        b = initial_material_state(seed + 100)

        for t in range(steps):
            bit = int(t == profile["experience_pulse_step"])
            forcing = float(env[t]) + profile["message_gain"] * bit

            a, _, _ = advance_one_step_material(
                a, forcing, bit, radius, crystal_params, mp
            )
            b, _, _ = advance_one_step_material(
                b, forcing, bit, radius, crystal_params, mp
            )

        reproducible[policy] = bool(
            a.occupied == b.occupied
            and a.modified == b.modified
            and a.birth_time == b.birth_time
            and a.attachments_by_step == b.attachments_by_step
        )

    # Unit-like budget test on a synthetic eligible set.
    synthetic_occupied = {
        (0, 0), (1, 0), (1, -1), (0, -1),
    }
    synthetic_modified = {(0, 0), (1, 0)}
    synthetic_additions = [(0, 1), (-1, 1), (2, -1), (2, 0)]

    uniform_sel, uniform_meta = choose_transmission_targets(
        synthetic_additions,
        synthetic_occupied | set(synthetic_additions),
        synthetic_modified,
        seed,
        99,
        profile["transmission_fraction"],
        "uniform_budget",
    )
    surface_sel, surface_meta = choose_transmission_targets(
        synthetic_additions,
        synthetic_occupied | set(synthetic_additions),
        synthetic_modified,
        seed,
        99,
        profile["transmission_fraction"],
        "surface_biased_budget",
    )

    budget_equal = (
        uniform_meta["budget"] == surface_meta["budget"]
        and len(uniform_sel) == len(surface_sel)
    )

    if not all(reproducible.values()):
        raise RuntimeError("V5 reproducibility audit failed.")
    if not budget_equal:
        raise RuntimeError("V5 equal-budget allocation audit failed.")

    result = {
        "role": "V5 SURFACE-PLACEMENT AUDIT",
        "canonical_model_modified": False,
        "transmission_fraction": profile["transmission_fraction"],
        "transmission_policies": profile["transmission_policies"],
        "exact_reproducibility_by_policy": reproducible,
        "all_policies_exactly_reproducible": all(reproducible.values()),
        "synthetic_equal_budget_check": {
            "uniform": uniform_meta,
            "surface_biased": surface_meta,
            "equal_selected_count": budget_equal,
        },
        "scientific_role": (
            "Compare transmission placement at a matched per-step copying budget. "
            "The experiment asks whether placing state on more exposed new "
            "material improves long-term causal accessibility."
        ),
    }

    reporter.json("stage-00-v5-audit.json", result)
    reporter.stage(
        "stage-00-v5-audit.md",
        "Stage 0 — V5 Surface-Placement Audit",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def run_experienced_trajectory_v5(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
    max_elapsed: int,
) -> Tuple[Dict[int, MaterialCrystalState], np.ndarray]:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]

    total = warmup + max_elapsed + 6
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


def transmission_step_metrics(
    state_before: MaterialCrystalState,
    state_after: MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> dict:
    """
    Reconstruct a one-step allocation audit from state transition geometry.

    This is descriptive and used to verify that the surface-biased policy is
    actually placing transmitted state on more exposed newly attached cells.
    """
    additions = sorted(state_after.occupied - state_before.occupied)
    newly_modified = sorted(state_after.modified - state_before.modified)

    eligible = [
        c for c in additions
        if any(nb in state_before.modified for nb in neighbors(c))
    ]
    transmitted = [c for c in newly_modified if c in additions]

    eligible_surface = [
        surface_exposure_after_attachment(c, state_after.occupied)
        for c in eligible
    ]
    transmitted_surface = [
        surface_exposure_after_attachment(c, state_after.occupied)
        for c in transmitted
    ]

    return {
        "addition_count": int(len(additions)),
        "eligible_count": int(len(eligible)),
        "transmitted_count": int(len(transmitted)),
        "mean_eligible_surface_exposure": (
            float(np.mean(eligible_surface)) if eligible_surface else 0.0
        ),
        "mean_transmitted_surface_exposure": (
            float(np.mean(transmitted_surface)) if transmitted_surface else 0.0
        ),
    }


def stage_1_equal_budget_surface_allocation(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    """
    Verify the intended intervention:
        uniform and surface-biased policies use comparable copying counts,
        but surface-biased placement targets more exposed newly attached cells.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    max_elapsed = max(profile["observation_steps"])

    policies = ["uniform_budget", "surface_biased_budget"]
    per_policy = {
        p: {
            "eligible_count": [],
            "transmitted_count": [],
            "mean_eligible_surface_exposure": [],
            "mean_transmitted_surface_exposure": [],
        }
        for p in policies
    }

    for policy in policies:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            transmission_fraction=profile["transmission_fraction"],
            transmission_policy=policy,
        )

        for g in tqdm(
            range(groups),
            desc=f"Stage 1 allocation {policy}",
        ):
            traj, future = run_experienced_trajectory_v5(
                profile, crystal_params, mp,
                seed + 200_000, g, max_elapsed,
            )

            # Aggregate only steps AFTER the direct experience pulse. We want
            # propagation placement, not the pulse-write event.
            first = profile["experience_pulse_step"] + 2

            for t in range(first, max_elapsed + 1):
                before = traj[t - 1]
                after = traj[t]
                met = transmission_step_metrics(
                    before, after, float(future[t - 1]),
                    radius, crystal_params, mp,
                )
                for key in per_policy[policy]:
                    per_policy[policy][key].append(met[key])

    summary = {}
    for pi, policy in enumerate(policies):
        summary[policy] = {
            key: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 210_000 + pi * 1000 + j,
            )
            for j, (key, vals) in enumerate(per_policy[policy].items())
        }

    result = {
        "groups": groups,
        "transmission_fraction": profile["transmission_fraction"],
        "policies": policies,
        "summary": summary,
        "status": "MEASURED",
        "bounded_statement": (
            "V5 verifies that surface-biased allocation changes where propagated "
            "state is placed while holding the nominal per-step transmission "
            "budget fixed."
        ),
    }

    reporter.json("stage-01-equal-budget-allocation.json", result)
    reporter.stage(
        "stage-01-equal-budget-allocation.md",
        "Stage 1 — Does Surface Bias Change Placement Rather Than Copy Count?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_2_policy_accessibility_map(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    groups = profile["groups"]
    radius = profile["radius"]
    steps = profile["observation_steps"]
    max_elapsed = max(steps)

    results = {}

    for policy in profile["transmission_policies"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            transmission_fraction=profile["transmission_fraction"],
            transmission_policy=policy,
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
            desc=f"Stage 2 accessibility {policy}",
        ):
            traj, _ = run_experienced_trajectory_v5(
                profile, crystal_params, mp,
                seed + 300_000, g, max_elapsed,
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
                    seed + 310_000 + t * 100 + j,
                )
                for j, (key, vals) in enumerate(metrics[t].items())
            }

        results[policy] = {
            "summary": summary,
            "lifetime": propagation_lifetime_from_summary(summary, steps),
        }

    result = {
        "groups_per_policy": groups,
        "transmission_fraction": profile["transmission_fraction"],
        "policies": profile["transmission_policies"],
        "observation_steps": steps,
        "results": results,
        "status": "MEASURED",
        "bounded_statement": (
            "V5 compares no transmission, equal-budget uniform transmission, and "
            "equal-budget surface-biased transmission on material abundance and "
            "active-frontier accessibility."
        ),
    }

    reporter.json("stage-02-policy-accessibility.json", result)
    reporter.stage(
        "stage-02-policy-accessibility.md",
        "Stage 2 — Does Surface-Biased Transmission Keep State on the Active Surface?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    for policy in profile["transmission_policies"]:
        s = results[policy]["summary"]
        ys = [
            s[str(t)]["frontier_exposed_fraction"]["mean"]
            for t in steps
        ]
        ax.plot(steps, ys, marker="o", label=policy)

    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("Matched-budget transmission policy and frontier accessibility")
    ax.legend()
    fig.tight_layout()

    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v5-01-surface-biased-accessibility.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_3_cell_level_policy_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    groups = profile["groups"]
    radius = profile["radius"]
    audit_steps = profile["cell_audit_steps"]
    max_elapsed = max(audit_steps)

    results = {}

    for policy in profile["transmission_policies"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            transmission_fraction=profile["transmission_fraction"],
            transmission_policy=policy,
        )

        per_step = {
            t: {
                "exposed_frontier_count": [],
                "exposed_frontier_fraction": [],
                "sum_delta_p": [],
                "mean_delta_p_exposed": [],
                "realized_causal_flips": [],
                "realized_flip_fraction_of_exposed": [],
            }
            for t in audit_steps
        }

        for g in tqdm(
            range(groups),
            desc=f"Stage 3 cell audit {policy}",
        ):
            traj, future = run_experienced_trajectory_v5(
                profile, crystal_params, mp,
                seed + 400_000, g, max_elapsed,
            )

            for t in audit_steps:
                audit = frontier_material_causal_audit(
                    traj[t],
                    float(future[t]),
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
                    seed + 410_000 + t * 100 + j,
                )
                for j, (key, vals) in enumerate(per_step[t].items())
            }

        results[policy] = {"summary": summary}

    result = {
        "groups_per_policy": groups,
        "audit_steps": audit_steps,
        "results": results,
        "status": "MEASURED",
        "bounded_statement": (
            "V5 measures whether matched-budget surface placement increases "
            "frontier availability, total probability leverage, and realized "
            "CRN-controlled causal attachment flips."
        ),
    }

    reporter.json("stage-03-cell-level-policy-audit.json", result)
    reporter.stage(
        "stage-03-cell-level-policy-audit.md",
        "Stage 3 — Does Surface Placement Increase Realized Causal Work?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_late_ablation_by_policy(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    seed: int,
) -> dict:
    groups = profile["groups"]
    radius = profile["radius"]
    probe = profile["late_ablation_step"]
    followup = profile["late_ablation_followup"]

    results = {}

    for policy in profile["transmission_policies"]:
        mp = MaterialParams(
            write_probability=profile["write_probability"],
            modified_neighbor_gain=profile["modified_neighbor_gain"],
            transmission_fraction=profile["transmission_fraction"],
            transmission_policy=policy,
        )

        Xs, Ys = [], []
        symdiff = []
        contact = []

        for g in tqdm(
            range(groups),
            desc=f"Stage 4 late ablation {policy}",
        ):
            traj, future = run_experienced_trajectory_v5(
                profile, crystal_params, mp,
                seed + 500_000, g, probe,
            )

            retained = traj[probe]
            erased = erase_material_labels(retained)

            access = material_accessibility_metrics(retained, radius)
            contact.append(
                access["frontier_cells_with_modified_neighbor"]
            )

            future_after = future[probe:]

            A = continue_material_no_pulse(
                retained, future_after, followup,
                radius, crystal_params, mp,
                profile["max_capacity_fraction"],
            )
            B = continue_material_no_pulse(
                erased, future_after, followup,
                radius, crystal_params, mp,
                profile["max_capacity_fraction"],
            )

            Xs.append(
                morphology_features_from_occupied(A.occupied, radius)
            )
            Ys.append(
                morphology_features_from_occupied(B.occupied, radius)
            )
            symdiff.append(
                normalized_symmetric_difference(A.occupied, B.occupied)
            )

        X = np.asarray(Xs, dtype=float)
        Y = np.asarray(Ys, dtype=float)

        test = paired_ridge_test(
            X, Y,
            permutations=profile["permutations"],
            seed=seed + 510_000,
        )

        results[policy] = {
            "frontier_contact_at_ablation": bootstrap_mean_ci(
                contact,
                profile["bootstrap_reps"],
                seed + 520_000,
            ),
            "pathwise_symmetric_difference_after_followup": bootstrap_mean_ci(
                symdiff,
                profile["bootstrap_reps"],
                seed + 530_000,
            ),
            "paired_ridge_test": test,
        }

    result = {
        "late_ablation_step": probe,
        "followup_steps": followup,
        "results": results,
        "status": "MEASURED",
        "interpretation": (
            "Whole-crystal ablation is corroborative. The primary mechanistic "
            "question is whether matched-budget surface placement produces more "
            "accessible and causally active state than uniform placement."
        ),
    }

    reporter.json("stage-04-late-ablation-by-policy.json", result)
    reporter.stage(
        "stage-04-late-ablation-by-policy.md",
        "Stage 4 — Late Causal Ablation by Transmission Policy",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_5_verdict(
    reporter: Reporter,
    profile: dict,
    stage0: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
    stage4: dict,
) -> dict:
    target = str(profile["late_ablation_step"])

    uniform_access = stage2["results"]["uniform_budget"]["summary"][target][
        "frontier_cells_with_modified_neighbor"
    ]["mean"]
    surface_access = stage2["results"]["surface_biased_budget"]["summary"][target][
        "frontier_cells_with_modified_neighbor"
    ]["mean"]

    uniform_flips = stage3["results"]["uniform_budget"]["summary"][target][
        "realized_causal_flips"
    ]["mean"]
    surface_flips = stage3["results"]["surface_biased_budget"]["summary"][target][
        "realized_causal_flips"
    ]["mean"]

    placement_exposure_uniform = stage1["summary"]["uniform_budget"][
        "mean_transmitted_surface_exposure"
    ]["mean"]
    placement_exposure_surface = stage1["summary"]["surface_biased_budget"][
        "mean_transmitted_surface_exposure"
    ]["mean"]

    surface_targets_more_exposed = (
        placement_exposure_surface > placement_exposure_uniform
    )
    surface_improves_late_access = surface_access > uniform_access
    surface_improves_realized_work = surface_flips > uniform_flips

    if (
        surface_targets_more_exposed
        and surface_improves_late_access
        and surface_improves_realized_work
    ):
        status = "SUPPORTED"
        bounded = (
            "At the same nominal transmission fraction, preferentially placing "
            "propagated material on more exposed newly attached cells increased "
            "late frontier accessibility and realized local causal attachment "
            "flips relative to uniform allocation."
        )
    elif surface_targets_more_exposed and (
        surface_improves_late_access or surface_improves_realized_work
    ):
        status = "PROVISIONAL"
        bounded = (
            "Surface-biased placement successfully targeted more exposed new "
            "material and improved part, but not all, of the late causal-access "
            "chain relative to matched-budget uniform allocation."
        )
    else:
        status = "FAILED"
        bounded = (
            "Matched-budget surface-biased placement did not establish an "
            "improvement in late causal accessibility over uniform allocation."
        )

    result = {
        "experiment_role": "EXPLORATORY MECHANISM COMPARISON",
        "chapter": 18,
        "question": (
            "Can historical material be preferentially preserved where future "
            "growth occurs, without increasing the nominal copying budget?"
        ),
        "matched_transmission_fraction": profile["transmission_fraction"],
        "surface_targets_more_exposed_material": surface_targets_more_exposed,
        "surface_improves_late_frontier_access": surface_improves_late_access,
        "surface_improves_late_realized_causal_flips": (
            surface_improves_realized_work
        ),
        "late_step_summary": {
            "uniform_budget": {
                "mean_frontier_contact": uniform_access,
                "mean_realized_causal_flips": uniform_flips,
            },
            "surface_biased_budget": {
                "mean_frontier_contact": surface_access,
                "mean_realized_causal_flips": surface_flips,
            },
        },
        "status": status,
        "bounded_claim": bounded,
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "attention",
            "homeostasis",
            "active boundary",
            "phase transition",
            "critical threshold",
            "information storage",
            "genetic inheritance",
            "epigenetics",
            "agency",
            "individuality",
            "reproduction",
            "life",
        ],
        "next_question": (
            "If surface-biased placement is supported, test whether the state can "
            "be updated or displaced by a later experience while the copying "
            "budget remains fixed. If not, return to the local propagation rule "
            "rather than increasing causal gain."
        ),
    }

    reporter.json("stage-05-verdict.json", result)
    reporter.stage(
        "stage-05-verdict.md",
        "Stage 5 — Bounded Chapter 18 V5 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260818)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch18-persistent-material-state-v5"
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
        "run_type": "EXPLORATORY MECHANISM COMPARISON",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "v4_supported_mechanism_map": (
            "Late causal work increased with successful propagation. Local causal "
            "gain was sufficient when modified material remained available at "
            "the active frontier."
        ),
        "v5_new_mechanism": (
            "Matched-budget propagation allocation: uniform placement versus "
            "preferential placement on newly attached cells with greater outward "
            "surface exposure."
        ),
        "scientific_boundary": (
            "V5 tests placement of propagated local state at a fixed nominal "
            "copying budget. It does not claim memory, learning, adaptation, "
            "attention, homeostasis, or an active biological boundary."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V5 — SURFACE-BIASED STATE TRANSMISSION")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups/policy={profile['groups']}"
    )
    print(f"policies={profile['transmission_policies']}")
    print(f"transmission_fraction={profile['transmission_fraction']}")
    print("=" * 78)

    s0 = stage_0_extension_audit(
        reporter, profile, crystal_params, args.seed
    )

    s1 = stage_1_equal_budget_surface_allocation(
        reporter, profile, crystal_params, args.seed
    )

    s2 = stage_2_policy_accessibility_map(
        reporter, profile, crystal_params,
        args.seed, args.image_dir,
    )

    s3 = stage_3_cell_level_policy_audit(
        reporter, profile, crystal_params, args.seed
    )

    s4 = stage_4_late_ablation_by_policy(
        reporter, profile, crystal_params, args.seed
    )

    s5 = stage_5_verdict(
        reporter, profile, s0, s1, s2, s3, s4
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "stage_4_status": s4["status"],
        "final_status": s5["status"],
        "next_question": s5["next_question"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("CHAPTER 18 V5 COMPLETE")
    print(f"allocation_audit={s1['status']}")
    print(f"accessibility_map={s2['status']}")
    print(f"cell_level_policy_audit={s3['status']}")
    print(f"late_ablation={s4['status']}")
    print(f"final_status={s5['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
