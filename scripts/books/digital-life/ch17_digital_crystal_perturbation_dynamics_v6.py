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


MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "digital-crystal-perturbation-dynamics-v6"
SCHEMA_VERSION = 6

Cell = Tuple[int, int]
HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)

# ---------------------------------------------------------------------------
# Digital Crystal v1 — frozen from Chapters 14–16
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CrystalParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


@dataclass
class CrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    attachments_by_step: List[int]
    population_by_step: List[int]


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


def clone_state(state: CrystalState) -> CrystalState:
    return CrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        step=state.step,
        rng_state=copy.deepcopy(state.rng_state),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
    )


def morphology_hash(state: CrystalState) -> str:
    payload = json.dumps(
        sorted((int(q), int(r)) for q, r in state.occupied),
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def advance_one_step(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: CrystalParams,
) -> Tuple[CrystalState, int]:
    """
    Frozen Digital Crystal v1 growth rule.

    Reproducibility invariant:
        every RNG-consuming frontier traversal uses sorted(frontier).
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


def hex_disk_capacity(radius: int) -> int:
    return 1 + 3 * radius * (radius + 1)


# ---------------------------------------------------------------------------
# Counterfactual common-random-number (CRN) runner
# ---------------------------------------------------------------------------

def cell_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Stable iid U[0,1) keyed by (stream_seed, absolute_step, q, r).

    This does NOT replace frozen Digital Crystal v1. It is a separate
    counterfactual coupling used to keep common cell/step opportunities aligned
    after branch frontiers diverge.
    """
    q, r = cell
    payload = f"{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def initial_state_crn(stream_seed: int) -> CrystalState:
    return CrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        step=0,
        rng_state=int(stream_seed),
        attachments_by_step=[1],
        population_by_step=[1],
    )


def advance_one_step_crn(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: CrystalParams,
) -> Tuple[CrystalState, int]:
    stream_seed = int(state.rng_state)
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions: List[Cell] = []
    next_step = state.step + 1

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
        if cell_uniform(stream_seed, next_step, cell) < logistic_scalar(score):
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    return CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=next_step,
        rng_state=stream_seed,
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
    ), len(additions)


def warm_checkpoint_crn(
    env: np.ndarray,
    warmup_steps: int,
    stream_seed: int,
    radius: int,
    params: CrystalParams,
) -> CrystalState:
    state = initial_state_crn(stream_seed)
    for t in range(warmup_steps):
        state, _ = advance_one_step_crn(state, float(env[t]), radius, params)
    return state


def advance_with_pulses_crn(
    checkpoint: CrystalState,
    env_future: np.ndarray,
    pulse_bits: Sequence[int],
    message_gain: float,
    radius: int,
    params: CrystalParams,
    observation_steps: Sequence[int],
    guard: float,
) -> Dict[int, CrystalState]:
    state = clone_state(checkpoint)
    wanted = set(map(int, observation_steps))
    observations: Dict[int, CrystalState] = {}

    for i in range(max(wanted)):
        bit = int(pulse_bits[i]) if i < len(pulse_bits) else 0
        forcing = float(env_future[i]) + message_gain * bit
        state, _ = advance_one_step_crn(state, forcing, radius, params)

        frac = capacity_fraction(state, radius)
        if frac >= guard:
            raise RuntimeError(
                f"CRN saturation guard reached at elapsed step {i+1}: "
                f"{frac:.3f} >= {guard:.3f}"
            )

        elapsed = i + 1
        if elapsed in wanted:
            observations[elapsed] = clone_state(state)

    return observations


def capacity_fraction(state: CrystalState, radius: int) -> float:
    return len(state.occupied) / float(hex_disk_capacity(radius))




# ---------------------------------------------------------------------------
# Chapter 17 — How Does the Crystal Respond to Perturbation?
# ---------------------------------------------------------------------------

"""
Scientific purpose
------------------
Chapter 16 established that changing one received bit can causally change a
Digital Crystal receiver. The previous Chapter 17 immediately asked whether
temporal codeword identity could survive that channel.

This experiment inserts a missing dynamical-systems layer.

It asks:

    1. What is the receiver's response to one isolated perturbation?
    2. How long does that response remain measurable?
    3. Are responses to multiple perturbations approximately additive?
    4. If onset, offset, and total pulse count are matched, does interior
       temporal arrangement still produce different receiver states?
    5. Does the analysis pipeline itself behave on known-null sham data?

This experiment does NOT establish:
    information storage
    memory
    signalling
    semantics
    sender identity
    coordination
    learning
    agency
    individuality
    life
    Shannon channel capacity

The intended bounded output is a characterization of perturbation dynamics.
"""


PROFILES = {
    "quick": {
        # Confirmatory sample size chosen before this v6 run.
        "groups": 48,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "message_gain": 0.65,

        # Frozen temporal-arrangement design.
        "primary_endpoint": 8,
        "secondary_endpoints": [9, 10, 12],
        "matched_observation_steps": [8, 9, 10, 12],

        # Frozen analysis.
        "primary_alpha": 0.05,
        "permutations": 2000,
        "bootstrap_reps": 1000,

        # Independent preflight / marginal-compatibility audit.
        "preflight_groups": 96,
        "preflight_permutations": 2000,
        "equivalence_margin_population_fraction": 0.05,
        "equivalence_margin_max_radius_fraction": 0.05,
        "equivalence_margin_attachment_rate_fraction": 0.10,
        "equivalence_margin_cov_anisotropy": 0.10,

        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 96,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "message_gain": 0.65,
        "primary_endpoint": 8,
        "secondary_endpoints": [9, 10, 12],
        "matched_observation_steps": [8, 9, 10, 12],
        "primary_alpha": 0.05,
        "permutations": 5000,
        "bootstrap_reps": 2000,
        "preflight_groups": 192,
        "preflight_permutations": 5000,
        "equivalence_margin_population_fraction": 0.05,
        "equivalence_margin_max_radius_fraction": 0.05,
        "equivalence_margin_attachment_rate_fraction": 0.10,
        "equivalence_margin_cov_anisotropy": 0.10,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 192,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "message_gain": 0.65,
        "primary_endpoint": 8,
        "secondary_endpoints": [9, 10, 12],
        "matched_observation_steps": [8, 9, 10, 12],
        "primary_alpha": 0.05,
        "permutations": 10000,
        "bootstrap_reps": 4000,
        "preflight_groups": 384,
        "preflight_permutations": 10000,
        "equivalence_margin_population_fraction": 0.05,
        "equivalence_margin_max_radius_fraction": 0.05,
        "equivalence_margin_attachment_rate_fraction": 0.10,
        "equivalence_margin_cov_anisotropy": 0.10,
        "max_capacity_fraction": 0.85,
    },
}

# Matched endpoint pair:
#   equal length
#   equal pulse count
#   equal first pulse
#   equal last pulse
#   different interior arrangement
MATCHED_CODEWORD_A = tuple(int(c) for c in "11100001")
MATCHED_CODEWORD_B = tuple(int(c) for c in "10001101")


# ---------------------------------------------------------------------------
# Measurement model
# ---------------------------------------------------------------------------

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

ANGULAR_FEATURE_NAMES = (
    "cov_anisotropy",
    "sector_0",
    "sector_1",
    "sector_2",
    "sector_3",
    "sector_4",
    "sector_5",
    "harmonic6_cos",
    "harmonic6_sin",
)
ANGULAR_FEATURE_INDICES = tuple(
    FEATURE_NAMES.index(name) for name in ANGULAR_FEATURE_NAMES
)



def morphology_features(state: CrystalState, radius: int) -> np.ndarray:
    occ = state.occupied
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


def state_difference(a: CrystalState, b: CrystalState, radius: int) -> dict:
    fa = morphology_features(a, radius)
    fb = morphology_features(b, radius)
    return {
        "population_difference": int(len(a.occupied) - len(b.occupied)),
        "absolute_population_difference": int(abs(len(a.occupied) - len(b.occupied))),
        "normalized_symmetric_difference": normalized_symmetric_difference(
            a.occupied, b.occupied
        ),
        "feature_distance": float(np.linalg.norm(fa - fb)),
    }


def standardize_pooled(X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pooled = np.vstack([X, Y])
    mean = np.mean(pooled, axis=0)
    sd = np.std(pooled, axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    return (X - mean) / sd, (Y - mean) / sd


def pairwise_distances(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    diff = A[:, None, :] - B[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def energy_distance_statistic(X: np.ndarray, Y: np.ndarray) -> float:
    if len(X) == 0 or len(Y) == 0:
        return float("nan")
    Xs, Ys = standardize_pooled(X, Y)
    xy = pairwise_distances(Xs, Ys)
    xx = pairwise_distances(Xs, Xs)
    yy = pairwise_distances(Ys, Ys)
    return float(
        2.0 * np.mean(xy)
        - np.mean(xx)
        - np.mean(yy)
    )


def paired_swap_permutation_test(
    X: np.ndarray,
    Y: np.ndarray,
    permutations: int,
    seed: int,
) -> dict:
    if X.shape != Y.shape:
        raise ValueError("Paired swap test requires equal paired shapes.")

    observed = energy_distance_statistic(X, Y)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X), dtype=np.int8).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = energy_distance_statistic(Xp, Yp)

    p = (1.0 + float(np.sum(null >= observed))) / (permutations + 1.0)
    return {
        "statistic": observed,
        "permutations": int(permutations),
        "p_value": p,
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
        "null_max": float(np.max(null)),
    }


def bootstrap_mean_ci(values: Sequence[float], reps: int, seed: int) -> dict:
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return {"n": 0}
    rng = np.random.default_rng(seed)
    means = np.empty(reps, dtype=float)
    for i in range(reps):
        sample = rng.choice(x, size=len(x), replace=True)
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


# ---------------------------------------------------------------------------
# Execution helpers
# ---------------------------------------------------------------------------

def warm_checkpoint(
    env: np.ndarray,
    warmup_steps: int,
    seed: int,
    radius: int,
    params: CrystalParams,
) -> CrystalState:
    state = initial_state(seed)
    for t in range(warmup_steps):
        state, _ = advance_one_step(state, float(env[t]), radius, params)
    return state


def advance_with_pulses(
    checkpoint: CrystalState,
    env_future: np.ndarray,
    pulse_bits: Sequence[int],
    message_gain: float,
    radius: int,
    params: CrystalParams,
    observation_steps: Sequence[int],
    guard: float,
) -> Dict[int, CrystalState]:
    state = clone_state(checkpoint)
    wanted = set(int(x) for x in observation_steps)
    max_step = max(wanted)
    observations: Dict[int, CrystalState] = {}

    for i in range(max_step):
        bit = int(pulse_bits[i]) if i < len(pulse_bits) else 0
        forcing = float(env_future[i]) + message_gain * bit
        state, _ = advance_one_step(state, forcing, radius, params)

        frac = capacity_fraction(state, radius)
        if frac >= guard:
            raise RuntimeError(
                f"Saturation guard reached at elapsed step {i+1}: "
                f"{frac:.3f} >= {guard:.3f}"
            )

        elapsed = i + 1
        if elapsed in wanted:
            observations[elapsed] = clone_state(state)

    return observations


def pulse_train(length: int, pulse_steps_zero_indexed: Sequence[int]) -> Tuple[int, ...]:
    x = [0] * length
    for idx in pulse_steps_zero_indexed:
        if idx < 0 or idx >= length:
            raise ValueError(f"Pulse index out of range: {idx}")
        x[idx] = 1
    return tuple(x)



# ---------------------------------------------------------------------------
# Stochastic-fork helpers
# ---------------------------------------------------------------------------

def reseed_state_rng(state: CrystalState, seed: int) -> CrystalState:
    """
    Preserve the complete visible crystal state while replacing only the RNG
    continuation with an independently seeded stream.

    This is NOT an exact counterfactual. It is used only to estimate the
    background spread of equivalent stochastic continuations under the same
    geometry and future external forcing.
    """
    rng = random.Random(seed)
    return CrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        step=state.step,
        rng_state=rng.getstate(),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
    )


def summarize_difference_series(series: Dict[int, Dict[str, list]], profile, seed_offset):
    out = {}
    for t, metrics in series.items():
        out[str(t)] = {
            name: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed_offset + t * 37 + i,
            )
            for i, (name, vals) in enumerate(metrics.items())
        }
    return out


def bootstrap_superposition_summary(
    single_delta_by_pos: Dict[int, np.ndarray],
    actual_delta: np.ndarray,
    positions: Sequence[int],
    reps: int,
    seed: int,
) -> dict:
    """
    Estimate additivity at the ENSEMBLE-MEAN response level.

    Each array has shape [group, feature]. We bootstrap groups, compute the
    mean isolated-pulse response for each pulse position, sum those means,
    and compare that prediction with the mean observed multi-pulse response.
    """
    n = actual_delta.shape[0]
    rng = np.random.default_rng(seed)

    def compute(indices):
        predicted = np.zeros(actual_delta.shape[1], dtype=float)
        for pos in positions:
            predicted += np.mean(single_delta_by_pos[pos][indices], axis=0)
        actual = np.mean(actual_delta[indices], axis=0)
        residual = float(np.linalg.norm(actual - predicted))
        actual_norm = float(np.linalg.norm(actual))
        pred_norm = float(np.linalg.norm(predicted))
        relative = residual / max(1e-12, actual_norm)
        cosine = float(
            np.dot(actual, predicted)
            / max(1e-12, np.linalg.norm(actual) * np.linalg.norm(predicted))
        )
        return residual, actual_norm, pred_norm, relative, cosine

    base_idx = np.arange(n)
    point = compute(base_idx)

    boot = np.empty((reps, 5), dtype=float)
    for i in range(reps):
        idx = rng.integers(0, n, size=n)
        boot[i] = compute(idx)

    names = [
        "residual_norm",
        "actual_mean_delta_norm",
        "predicted_mean_delta_norm",
        "relative_superposition_error",
        "cosine_actual_vs_predicted",
    ]
    result = {}
    for j, name in enumerate(names):
        result[name] = {
            "value": float(point[j]),
            "bootstrap_ci95_low": float(np.quantile(boot[:, j], 0.025)),
            "bootstrap_ci95_high": float(np.quantile(boot[:, j], 0.975)),
        }
    return result



# ---------------------------------------------------------------------------
# V3 measurement-resolution helpers
# ---------------------------------------------------------------------------

CANDIDATE_INSTRUMENTS = (
    "energy_distance",
    "paired_mean_l2",
    "paired_max_abs_mean",
    "paired_ridge_hotelling",
)


INSTRUMENT_CLASSES = {
    "energy_distance": "MARGINAL_DISTRIBUTION",
    "paired_mean_l2": "PAIRED_DIRECTIONAL",
    "paired_max_abs_mean": "PAIRED_DIRECTIONAL",
    "paired_ridge_hotelling": "PAIRED_DIRECTIONAL",
}


def pooled_feature_scale(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    pooled = np.vstack([X, Y])
    sd = np.std(pooled, axis=0)
    return np.where(sd < 1e-12, 1.0, sd)


def paired_standardized_deltas(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Return checkpoint-paired differences in standardized feature units.

    Positive values mean X > Y for the declared feature. Standardization uses
    the pooled marginal feature scale, not the treatment difference itself.
    """
    if X.shape != Y.shape:
        raise ValueError("Paired delta statistics require equal paired shapes.")
    return (X - Y) / pooled_feature_scale(X, Y)


def stat_paired_mean_l2(X: np.ndarray, Y: np.ndarray) -> float:
    D = paired_standardized_deltas(X, Y)
    return float(np.linalg.norm(np.mean(D, axis=0)))


def stat_paired_max_abs_mean(X: np.ndarray, Y: np.ndarray) -> float:
    D = paired_standardized_deltas(X, Y)
    return float(np.max(np.abs(np.mean(D, axis=0))))


def stat_paired_ridge_hotelling(
    X: np.ndarray,
    Y: np.ndarray,
    ridge_fraction: float = 0.25,
) -> float:
    """
    Regularized paired mean-shift statistic.

    With only ~24 groups and 24 features, the ordinary Hotelling T^2 covariance
    inverse is unstable/singular. We therefore use a fixed ridge chosen before
    seeing the matched-arrangement result.

    This is a candidate measurement instrument, not a canonical statistical
    theorem or an information-theoretic quantity.
    """
    D = paired_standardized_deltas(X, Y)
    mean = np.mean(D, axis=0)
    if len(D) <= 1:
        return float(np.dot(mean, mean))

    cov = np.cov(D, rowvar=False, bias=True)
    diag_scale = float(np.mean(np.diag(cov)))
    ridge = max(1e-8, ridge_fraction * max(diag_scale, 1e-8))
    reg = cov + ridge * np.eye(cov.shape[0])
    inv = np.linalg.pinv(reg)
    return float(mean @ inv @ mean)


def instrument_statistic(name: str, X: np.ndarray, Y: np.ndarray) -> float:
    if name == "energy_distance":
        return energy_distance_statistic(X, Y)
    if name == "paired_mean_l2":
        return stat_paired_mean_l2(X, Y)
    if name == "paired_max_abs_mean":
        return stat_paired_max_abs_mean(X, Y)
    if name == "paired_ridge_hotelling":
        return stat_paired_ridge_hotelling(X, Y)
    raise ValueError(f"Unknown candidate instrument: {name}")


def paired_signflip_test(
    name: str,
    X: np.ndarray,
    Y: np.ndarray,
    permutations: int,
    seed: int,
) -> dict:
    """
    Paired randomization test.

    Under the sharp paired null, each checkpoint's A/B labels may be exchanged.
    This preserves checkpoint pairing while destroying a consistent treatment
    direction. The statistic is recomputed after every swap.
    """
    if X.shape != Y.shape:
        raise ValueError("Paired sign-flip test requires equal paired shapes.")

    observed = instrument_statistic(name, X, Y)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X), dtype=np.int8).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = instrument_statistic(name, Xp, Yp)

    p = (1.0 + float(np.sum(null >= observed))) / (permutations + 1.0)
    return {
        "instrument": name,
        "statistic": float(observed),
        "permutations": int(permutations),
        "p_value": float(p),
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
    }


def effect_directions(X: np.ndarray, seed: int) -> dict:
    """
    Predeclare three different synthetic effect geometries.

    All directions are expressed in standardized feature coordinates and have
    Euclidean norm 1, so `strength=1.0` means a standardized multivariate shift
    of norm one, not necessarily a one-SD shift in every feature.
    """
    sd = np.std(X, axis=0)
    varying = np.flatnonzero(sd > 1e-9)
    if len(varying) == 0:
        raise RuntimeError("No varying features available for calibration.")

    # Single-feature: the most variable raw feature.
    single_idx = int(varying[np.argmax(sd[varying])])
    single = np.zeros(X.shape[1], dtype=float)
    single[single_idx] = 1.0

    # Sparse-three: three most variable raw features, equal standardized weight.
    ordered = varying[np.argsort(sd[varying])[::-1]]
    sparse_idx = [int(i) for i in ordered[: min(3, len(ordered))]]
    sparse = np.zeros(X.shape[1], dtype=float)
    sparse[sparse_idx] = 1.0
    sparse /= max(1e-12, np.linalg.norm(sparse))

    # Dense PC1: leading principal direction in standardized feature space.
    Xs = (X - np.mean(X, axis=0)) / np.where(sd < 1e-12, 1.0, sd)
    cov = np.cov(Xs, rowvar=False, bias=True)
    vals, vecs = np.linalg.eigh(cov)
    dense = np.asarray(vecs[:, int(np.argmax(vals))], dtype=float)
    dense /= max(1e-12, np.linalg.norm(dense))

    # Fix eigenvector sign deterministically for stable artifacts.
    first_nonzero = np.flatnonzero(np.abs(dense) > 1e-12)
    if len(first_nonzero) and dense[first_nonzero[0]] < 0:
        dense *= -1.0

    return {
        "single_feature": {
            "direction": single,
            "description": f"single feature: {FEATURE_NAMES[single_idx]}",
            "feature_indices": [single_idx],
        },
        "sparse_three": {
            "direction": sparse,
            "description": "equal standardized shift across top-variance features",
            "feature_indices": sparse_idx,
        },
        "dense_pc1": {
            "direction": dense,
            "description": "leading principal direction of standardized baseline features",
            "feature_indices": None,
        },
    }


def apply_standardized_shift(
    X: np.ndarray,
    direction: np.ndarray,
    strength: float,
) -> np.ndarray:
    """
    Shift X by `strength * direction` in standardized feature coordinates.
    """
    sd = np.std(X, axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    return X + float(strength) * direction[None, :] * sd[None, :]



def build_symmetric_calibration_pair(
    base: np.ndarray,
    noise: np.ndarray,
    direction: np.ndarray,
    strength: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Construct a paired synthetic experiment around a shared latent baseline.

    The v3 calibration used:

        A = base
        B = base + empirical_noise

    Even if empirical_noise were symmetrized, that construction gives B extra
    variance and is therefore not a true null for a marginal-distribution test.

    V4 instead places both arms symmetrically around the same baseline:

        A = base + 0.5 * signed_noise - 0.5 * treatment_shift
        B = base - 0.5 * signed_noise + 0.5 * treatment_shift

    Under strength=0 and a sign-symmetric noise distribution, A and B are
    exchangeable and have the same marginal distribution.

    Under strength>0, the paired B-A contrast contains the declared treatment
    shift plus realistic correlated stochastic noise.

    The treatment direction is defined in standardized feature units relative
    to the sampled baseline feature scale.
    """
    if base.shape != noise.shape:
        raise ValueError("base and noise must have identical [n, feature] shapes.")

    sd = np.std(base, axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    treatment = float(strength) * direction[None, :] * sd[None, :]

    A = base + 0.5 * noise - 0.5 * treatment
    B = base - 0.5 * noise + 0.5 * treatment
    return A, B


def top_directional_features(X: np.ndarray, Y: np.ndarray, limit: int = 6) -> list:
    D = paired_standardized_deltas(X, Y)
    mean = np.mean(D, axis=0)
    order = np.argsort(np.abs(mean))[::-1][:limit]
    return [
        {
            "feature_index": int(i),
            "feature_name": FEATURE_NAMES[int(i)],
            "mean_standardized_delta_A_minus_B": float(mean[int(i)]),
        }
        for i in order
    ]



# ---------------------------------------------------------------------------
# V6 confirmatory preflight helpers
# ---------------------------------------------------------------------------

def mean_difference_bootstrap_ci(
    x: Sequence[float],
    y: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    """
    Bootstrap the difference in means: CRN - sequential.

    This is used as an equivalence-style practical compatibility check.
    Passing means the entire bootstrap 95% CI lies inside the predeclared
    practical margin. It is not a formal proof of identical stochastic laws.
    """
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)
    if len(xa) == 0 or len(ya) == 0:
        return {"n_x": int(len(xa)), "n_y": int(len(ya)), "passed": False}

    observed = float(np.mean(ya) - np.mean(xa))
    rng = np.random.default_rng(seed)
    boot = np.empty(reps, dtype=float)
    for i in range(reps):
        xb = xa[rng.integers(0, len(xa), size=len(xa))]
        yb = ya[rng.integers(0, len(ya), size=len(ya))]
        boot[i] = np.mean(yb) - np.mean(xb)

    return {
        "n_x": int(len(xa)),
        "n_y": int(len(ya)),
        "difference_crn_minus_sequential": observed,
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
    }


def practical_equivalence_result(
    x: Sequence[float],
    y: Sequence[float],
    margin: float,
    reps: int,
    seed: int,
) -> dict:
    out = mean_difference_bootstrap_ci(x, y, reps, seed)
    out["predeclared_margin"] = float(margin)
    if "ci95_low" not in out:
        out["passed"] = False
        return out
    out["passed"] = bool(
        out["ci95_low"] >= -float(margin)
        and out["ci95_high"] <= float(margin)
    )
    return out


def attachment_rate(state: CrystalState) -> float:
    if len(state.attachments_by_step) <= 1:
        return 0.0
    return float(np.mean(state.attachments_by_step[1:]))


def max_radius_fraction(state: CrystalState, radius: int) -> float:
    if not state.occupied:
        return 0.0
    return float(max(hex_distance(c) for c in state.occupied)) / max(1.0, radius)


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

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
        path = self.root / "ch17-perturbation-dynamics-v6-full-report.md"
        header = (
            "# Chapter 17 — How Does the Crystal Respond to Perturbation?\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
        )
        path.write_text(
            header + "\n\n".join(self.sections),
            encoding="utf-8",
        )
        return path


# ---------------------------------------------------------------------------
# Stage 0 — reproducibility
# ---------------------------------------------------------------------------

def codeword_pulse_positions(bits: Sequence[int]) -> List[int]:
    return [i for i, v in enumerate(bits) if int(v) != 0]


def validate_matched_codewords(a: Sequence[int], b: Sequence[int]) -> dict:
    pa = codeword_pulse_positions(a)
    pb = codeword_pulse_positions(b)
    if not pa or not pb:
        raise RuntimeError("Matched codewords must contain at least one pulse.")
    result = {
        "pulse_count_A": len(pa),
        "pulse_count_B": len(pb),
        "first_pulse_A": pa[0],
        "first_pulse_B": pb[0],
        "last_pulse_A": pa[-1],
        "last_pulse_B": pb[-1],
        "same_pulse_count": len(pa) == len(pb),
        "same_first_pulse": pa[0] == pb[0],
        "same_last_pulse": pa[-1] == pb[-1],
    }
    if not (
        result["same_pulse_count"]
        and result["same_first_pulse"]
        and result["same_last_pulse"]
    ):
        raise RuntimeError(f"Matched-codeword invariant failed: {result}")
    return result


def summarize_scalar(values, bootstrap_reps, seed):
    return bootstrap_mean_ci(
        list(map(float, values)), int(bootstrap_reps), int(seed)
    )


def codeword_pulse_positions(bits: Sequence[int]) -> List[int]:
    return [i for i, v in enumerate(bits) if int(v) != 0]


def validate_matched_codewords(a: Sequence[int], b: Sequence[int]) -> dict:
    pa = codeword_pulse_positions(a)
    pb = codeword_pulse_positions(b)
    if not pa or not pb:
        raise RuntimeError("Matched codewords must contain at least one pulse.")

    result = {
        "pulse_count_A": len(pa),
        "pulse_count_B": len(pb),
        "first_pulse_A": pa[0],
        "first_pulse_B": pb[0],
        "last_pulse_A": pa[-1],
        "last_pulse_B": pb[-1],
        "same_pulse_count": len(pa) == len(pb),
        "same_first_pulse": pa[0] == pb[0],
        "same_last_pulse": pa[-1] == pb[-1],
    }
    if not (
        result["same_pulse_count"]
        and result["same_first_pulse"]
        and result["same_last_pulse"]
    ):
        raise RuntimeError(f"Matched-codeword invariant failed: {result}")
    return result


def summarize_scalar(values, bootstrap_reps, seed):
    return bootstrap_mean_ci(
        list(map(float, values)), int(bootstrap_reps), int(seed)
    )


def stage_0_confirmatory_preflight(
    reporter, profile, params, seed
):
    """
    Independent preflight before the confirmatory A/B sample is generated.

    The canonical sequential-RNG implementation is not modified. The keyed-CRN
    counterfactual runner must satisfy:

      1. exact reproducibility for both runners;
      2. no detected gross 24-feature marginal distribution mismatch;
      3. practical-equivalence-style CI checks on four predeclared observables.

    The preflight uses a seed namespace disjoint from the confirmatory sample.
    Failure blocks scientific interpretation of Stage 1.
    """
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    groups = profile["preflight_groups"]
    perms = profile["preflight_permutations"]
    reps = profile["bootstrap_reps"]

    # Exact reproducibility checks.
    env0 = make_environment(warmup + horizon, seed + 1)

    def run_seq_once():
        s = initial_state(seed + 2)
        for x in env0:
            s, _ = advance_one_step(s, float(x), radius, params)
        return s

    def run_crn_once():
        s = initial_state_crn(seed + 2)
        for x in env0:
            s, _ = advance_one_step_crn(s, float(x), radius, params)
        return s

    sa, sb = run_seq_once(), run_seq_once()
    ca, cb = run_crn_once(), run_crn_once()

    sequential_exact = (
        sa.occupied == sb.occupied
        and sa.rng_state == sb.rng_state
        and sa.attachments_by_step == sb.attachments_by_step
    )
    crn_exact = (
        ca.occupied == cb.occupied
        and ca.rng_state == cb.rng_state
        and ca.attachments_by_step == cb.attachments_by_step
    )
    if not sequential_exact or not crn_exact:
        raise RuntimeError("V6 preflight reproducibility failed.")

    seq_features, crn_features = [], []
    observables = {
        "population_fraction": {"seq": [], "crn": []},
        "max_radius_fraction": {"seq": [], "crn": []},
        "attachment_rate_fraction": {"seq": [], "crn": []},
        "cov_anisotropy": {"seq": [], "crn": []},
    }

    capacity = float(hex_disk_capacity(radius))

    for g in tqdm(range(groups), desc="Stage 0 v6 confirmatory preflight"):
        # Separate namespace from Stage 1 confirmatory data.
        gseed = seed + 1_000_000 + g * 1009
        env = make_environment(warmup + horizon, gseed + 1)

        ss = initial_state(gseed + 2)
        cs = initial_state_crn(gseed + 2)

        for x in env:
            ss, _ = advance_one_step(ss, float(x), radius, params)
            cs, _ = advance_one_step_crn(cs, float(x), radius, params)

        sf = morphology_features(ss, radius)
        cf = morphology_features(cs, radius)
        seq_features.append(sf)
        crn_features.append(cf)

        observables["population_fraction"]["seq"].append(len(ss.occupied) / capacity)
        observables["population_fraction"]["crn"].append(len(cs.occupied) / capacity)

        observables["max_radius_fraction"]["seq"].append(
            max_radius_fraction(ss, radius)
        )
        observables["max_radius_fraction"]["crn"].append(
            max_radius_fraction(cs, radius)
        )

        # Normalize attachment rate by final frontier-scale proxy:
        # population count, keeping the quantity bounded and comparable.
        observables["attachment_rate_fraction"]["seq"].append(
            attachment_rate(ss) / max(1.0, len(ss.occupied))
        )
        observables["attachment_rate_fraction"]["crn"].append(
            attachment_rate(cs) / max(1.0, len(cs.occupied))
        )

        observables["cov_anisotropy"]["seq"].append(float(sf[7]))
        observables["cov_anisotropy"]["crn"].append(float(cf[7]))

    X = np.asarray(seq_features, dtype=float)
    Y = np.asarray(crn_features, dtype=float)
    observed_energy = energy_distance_statistic(X, Y)

    pooled = np.vstack([X, Y])
    n = len(X)
    rng = np.random.default_rng(seed + 1_900_000)
    null = np.empty(perms, dtype=float)
    for i in range(perms):
        order = rng.permutation(len(pooled))
        null[i] = energy_distance_statistic(
            pooled[order[:n]], pooled[order[n:2*n]]
        )

    omnibus_p = (1 + float(np.sum(null >= observed_energy))) / (perms + 1)

    margins = {
        "population_fraction": profile["equivalence_margin_population_fraction"],
        "max_radius_fraction": profile["equivalence_margin_max_radius_fraction"],
        "attachment_rate_fraction": profile["equivalence_margin_attachment_rate_fraction"],
        "cov_anisotropy": profile["equivalence_margin_cov_anisotropy"],
    }

    eq = {}
    for i, name in enumerate(margins):
        eq[name] = practical_equivalence_result(
            observables[name]["seq"],
            observables[name]["crn"],
            margins[name],
            reps,
            seed + 1_910_000 + i * 100,
        )

    all_equivalence_passed = all(v["passed"] for v in eq.values())

    # Omnibus is treated as a gross discrepancy screen.
    preflight_passed = bool(
        omnibus_p >= 0.05
        and all_equivalence_passed
    )

    result = {
        "role": "CONFIRMATORY PREFLIGHT",
        "sequential_exact": sequential_exact,
        "crn_exact": crn_exact,
        "canonical_substrate_modified": False,
        "preflight_groups_per_runner": groups,
        "omnibus_marginal_feature_test": {
            "energy_distance": float(observed_energy),
            "p_value": float(omnibus_p),
            "null_q95": float(np.quantile(null, 0.95)),
            "gross_mismatch_screen_passed": bool(omnibus_p >= 0.05),
        },
        "practical_equivalence_checks": eq,
        "all_equivalence_checks_passed": all_equivalence_passed,
        "preflight_passed": preflight_passed,
        "interpretation": (
            "Passing is practical compatibility evidence for using the keyed-CRN "
            "runner as the declared counterfactual coupling. It is not proof of "
            "identical stochastic laws."
        ),
    }

    reporter.json("stage-00-confirmatory-preflight.json", result)
    reporter.stage(
        "stage-00-confirmatory-preflight.md",
        "Stage 0 — Confirmatory CRN Preflight",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def paired_ridge_subset_test(
    X: np.ndarray,
    Y: np.ndarray,
    indices: Sequence[int],
    permutations: int,
    seed: int,
) -> dict:
    idx = np.asarray(indices, dtype=int)

    def stat(A, B):
        return stat_paired_ridge_hotelling(A[:, idx], B[:, idx])

    observed = stat(X, Y)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X)).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = stat(Xp, Yp)

    p = (1 + float(np.sum(null >= observed))) / (permutations + 1)

    return {
        "statistic": float(observed),
        "p_value": float(p),
        "permutations": int(permutations),
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
    }


def stage_1_confirmatory_matched_arrangement(
    reporter, profile, params, seed
):
    """
    Frozen confirmatory experiment.

    Counterfactual coupling:
        cell-keyed CRN only

    Codewords:
        A = 11100001
        B = 10001101

    Primary endpoint:
        elapsed step 8

    Primary instrument:
        paired ridge Hotelling on the frozen mechanism-derived angular9 subspace

    Secondary instrument:
        paired ridge Hotelling on all 24 morphology features

    Secondary endpoints:
        9, 10, 12 — descriptive / secondary only

    No endpoint, feature-set, or statistic selection is allowed after seeing
    this sample.
    """
    invariants = validate_matched_codewords(
        MATCHED_CODEWORD_A, MATCHED_CODEWORD_B
    )

    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    observations = profile["matched_observation_steps"]

    bits_a = tuple(MATCHED_CODEWORD_A) + (0,) * max(
        0, horizon - len(MATCHED_CODEWORD_A)
    )
    bits_b = tuple(MATCHED_CODEWORD_B) + (0,) * max(
        0, horizon - len(MATCHED_CODEWORD_B)
    )

    features = {
        t: {"A": [], "B": []}
        for t in observations
    }
    symdiff = {t: [] for t in observations}

    for g in tqdm(range(groups), desc="Stage 1 v6 confirmatory matched timing"):
        # Disjoint namespace from Stage 0 preflight and all v5 pilot seeds.
        gseed = seed + 2_000_000 + g * 1019
        env = make_environment(warmup + horizon, gseed + 1)
        future = env[warmup:]
        cp = warm_checkpoint_crn(env, warmup, gseed + 2, radius, params)

        A = advance_with_pulses_crn(
            cp, future, bits_a, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        B = advance_with_pulses_crn(
            cp, future, bits_b, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            features[t]["A"].append(morphology_features(A[t], radius))
            features[t]["B"].append(morphology_features(B[t], radius))
            symdiff[t].append(
                normalized_symmetric_difference(
                    A[t].occupied, B[t].occupied
                )
            )

    results = {}
    for t in observations:
        X = np.asarray(features[t]["A"], dtype=float)
        Y = np.asarray(features[t]["B"], dtype=float)

        results[str(t)] = {
            "steps_since_last_pulse": int(t - 8),
            "symdiff": summarize_scalar(
                symdiff[t],
                profile["bootstrap_reps"],
                seed + 2_300_000 + t,
            ),
            "primary_angular9": paired_ridge_subset_test(
                X, Y,
                ANGULAR_FEATURE_INDICES,
                profile["permutations"],
                seed + 2_310_000 + t,
            ),
            "secondary_all24": paired_ridge_subset_test(
                X, Y,
                range(len(FEATURE_NAMES)),
                profile["permutations"],
                seed + 2_320_000 + t,
            ),
            "top_directional_features_descriptive_only": (
                top_directional_features(X, Y)
            ),
        }

    primary_t = str(profile["primary_endpoint"])
    primary = results[primary_t]["primary_angular9"]
    alpha = float(profile["primary_alpha"])

    primary_positive = bool(primary["p_value"] < alpha)

    result = {
        "role": "CONFIRMATORY MATCHED TEMPORAL-ARRANGEMENT TEST",
        "groups": groups,
        "coupling": "cell-keyed CRN",
        "codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "codeword_validation": invariants,
        "primary_endpoint": int(profile["primary_endpoint"]),
        "secondary_endpoints": list(profile["secondary_endpoints"]),
        "primary_alpha": alpha,
        "primary_instrument": {
            "name": "paired_ridge_hotelling_angular9",
            "feature_names": list(ANGULAR_FEATURE_NAMES),
            "feature_indices": list(ANGULAR_FEATURE_INDICES),
            "frozen_before_run": True,
        },
        "secondary_instrument": {
            "name": "paired_ridge_hotelling_all24",
            "frozen_before_run": True,
        },
        "results": results,
        "primary_positive": primary_positive,
        "decision_rule": (
            "Primary angular9 paired-ridge test at t=8 only. "
            "p < 0.05 => PROVISIONAL matched-arrangement signature. "
            "p >= 0.05 => FAILED under this frozen calibrated protocol. "
            "Secondary endpoints and all24 may not rescue or overturn the primary."
        ),
    }

    reporter.json("stage-01-confirmatory-matched-arrangement.json", result)
    reporter.stage(
        "stage-01-confirmatory-matched-arrangement.md",
        "Stage 1 — Confirmatory Matched Temporal Arrangement",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_2_confirmatory_verdict(
    reporter,
    preflight,
    confirmatory,
):
    if not preflight["preflight_passed"]:
        status = "UNTESTED"
        statement = (
            "The CRN practical-compatibility preflight failed, so the "
            "confirmatory matched-arrangement result is not scientifically "
            "interpreted."
        )
    elif confirmatory["primary_positive"]:
        status = "PROVISIONAL"
        statement = (
            "Under the frozen CRN coupling, short matched codewords, t=8 "
            "endpoint, angular9 feature set, and paired ridge statistic, the "
            "independent v6 sample detected a systematic temporal-arrangement "
            "signature. This supports a provisional receiver-history claim, "
            "not memory, semantics, or information storage."
        )
    else:
        status = "FAILED"
        statement = (
            "Under the frozen CRN coupling, short matched codewords, t=8 "
            "endpoint, angular9 feature set, and paired ridge statistic, the "
            "independent v6 sample did not establish a systematic temporal-"
            "arrangement signature. Secondary endpoints or all24 results do "
            "not alter this primary decision."
        )

    primary = confirmatory["results"][
        str(confirmatory["primary_endpoint"])
    ]["primary_angular9"]

    result = {
        "experiment_role": "CONFIRMATORY",
        "preflight_passed": bool(preflight["preflight_passed"]),
        "matched_arrangement_status": status,
        "primary_endpoint": confirmatory["primary_endpoint"],
        "primary_instrument": "paired_ridge_hotelling_angular9",
        "primary_p_value": primary["p_value"],
        "primary_alpha": confirmatory["primary_alpha"],
        "bounded_statement": statement,
        "secondary_results_cannot_change_primary_decision": True,
        "chapter18_status": (
            "ELIGIBLE_FOR_NEXT_DESIGN"
            if status == "PROVISIONAL"
            else "DEFERRED"
        ),
        "nonclaims": [
            "memory",
            "information storage",
            "semantics",
            "sender identity",
            "coordination",
            "learning",
            "agency",
            "individuality",
            "life",
            "Shannon channel capacity",
        ],
    }

    reporter.json("stage-02-confirmatory-verdict.json", result)
    reporter.stage(
        "stage-02-confirmatory-verdict.md",
        "Stage 2 — Bounded V6 Confirmatory Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")

    # New seed is deliberately different from the v5 exploratory pilot.
    parser.add_argument("--seed", type=int, default=20260813)

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("research/digital-life/ch17-perturbation-dynamics-v6"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    params = CrystalParams()

    args.report_dir.mkdir(parents=True, exist_ok=True)
    reporter = Reporter(args.report_dir)

    codeword_check = validate_matched_codewords(
        MATCHED_CODEWORD_A, MATCHED_CODEWORD_B
    )

    metadata = {
        "model_version": MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": 17,
        "chapter_title": "How Does the Crystal Respond to Perturbation?",
        "run_type": "CONFIRMATORY",
        "version_6_focus": (
            "Independent confirmation of the frozen short matched temporal-"
            "arrangement design under cell-keyed CRN. Primary endpoint t=8, "
            "primary instrument paired ridge Hotelling on the predeclared "
            "angular9 feature subspace. Secondary endpoints and all24 cannot "
            "change the primary decision."
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "seed_note": (
            "Different from v5 exploratory seed 20260812. Stage 0 and Stage 1 "
            "also use disjoint internal seed namespaces."
        ),
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN",
        "matched_codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "matched_codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "matched_codeword_validation": codeword_check,
        "primary_endpoint": profile["primary_endpoint"],
        "primary_alpha": profile["primary_alpha"],
        "primary_feature_subspace": list(ANGULAR_FEATURE_NAMES),
        "scientific_boundary": (
            "Confirmatory test of a systematic matched temporal-arrangement "
            "morphology signature only. No memory, semantics, signalling, or "
            "information-storage claim is licensed by this experiment alone."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 17 — CONFIRMATORY TEMPORAL-ARRANGEMENT TEST")
    print(f"profile={args.profile} version={EXPERIMENT_VERSION}")
    print(f"seed={args.seed} groups={profile['groups']}")
    print("=" * 78)

    s0 = stage_0_confirmatory_preflight(
        reporter, profile, params, args.seed
    )

    # Run Stage 1 regardless, so computational artifacts exist even if the
    # preflight later blocks scientific interpretation. Stage 2 enforces the gate.
    s1 = stage_1_confirmatory_matched_arrangement(
        reporter, profile, params, args.seed
    )

    s2 = stage_2_confirmatory_verdict(
        reporter, s0, s1
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "reproducibility_passed": bool(
            s0["sequential_exact"] and s0["crn_exact"]
        ),
        "preflight_passed": bool(s0["preflight_passed"]),
        "primary_p_value": s2["primary_p_value"],
        "final_status": s2["matched_arrangement_status"],
        "chapter18_status": s2["chapter18_status"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("V6 COMPLETE")
    print(f"preflight_passed={s0['preflight_passed']}")
    print(f"primary_p={s2['primary_p_value']:.8g}")
    print(f"final_status={s2['matched_arrangement_status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
