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
EXPERIMENT_VERSION = "digital-crystal-perturbation-dynamics-v5"
SCHEMA_VERSION = 5

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
        "groups": 24,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 5, 6, 8, 10, 12, 16, 20],
        "matched_observation_steps": [8, 9, 10, 12],
        "bootstrap_reps": 500,
        "permutations": 500,
        "coupling_validation_groups": 48,
        "calibration_reps": 200,
        "calibration_permutations": 500,
        "mde_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
        "mde_target_power": 0.80,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 60,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 5, 6, 8, 10, 12, 16, 20],
        "matched_observation_steps": [8, 9, 10, 12],
        "bootstrap_reps": 1000,
        "permutations": 1000,
        "coupling_validation_groups": 120,
        "calibration_reps": 300,
        "calibration_permutations": 1000,
        "mde_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
        "mde_target_power": 0.80,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 120,
        "radius": 64,
        "warmup_steps": 14,
        "horizon": 20,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 5, 6, 8, 10, 12, 16, 20],
        "matched_observation_steps": [8, 9, 10, 12],
        "bootstrap_reps": 2000,
        "permutations": 2000,
        "coupling_validation_groups": 240,
        "calibration_reps": 500,
        "calibration_permutations": 1000,
        "mde_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
        "mde_target_power": 0.80,
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
        path = self.root / "ch17-perturbation-dynamics-v5-full-report.md"
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


def stage_0_reproducibility_and_marginals(
    reporter, profile, params, seed, image_dir
):
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    groups = profile["coupling_validation_groups"]

    env = make_environment(warmup + horizon, seed + 1)

    def run_seq():
        s = initial_state(seed + 2)
        adds = []
        for x in env:
            s, n = advance_one_step(s, float(x), radius, params)
            adds.append(n)
        return s, adds

    def run_crn():
        s = initial_state_crn(seed + 2)
        adds = []
        for x in env:
            s, n = advance_one_step_crn(s, float(x), radius, params)
            adds.append(n)
        return s, adds

    sa, saa = run_seq()
    sb, sbb = run_seq()
    ca, caa = run_crn()
    cb, cbb = run_crn()

    sequential_exact = (
        sa.occupied == sb.occupied
        and sa.rng_state == sb.rng_state
        and saa == sbb
    )
    crn_exact = (
        ca.occupied == cb.occupied
        and ca.rng_state == cb.rng_state
        and caa == cbb
    )
    if not sequential_exact or not crn_exact:
        raise RuntimeError("Stage 0 reproducibility failed.")

    seq_features, crn_features = [], []
    seq_pop, crn_pop = [], []

    for g in tqdm(range(groups), desc="Stage 0 marginal coupling audit"):
        gseed = seed + 1_000 + g * 1009
        genv = make_environment(warmup + horizon, gseed + 1)

        ss = initial_state(gseed + 2)
        cs = initial_state_crn(gseed + 2)
        for x in genv:
            ss, _ = advance_one_step(ss, float(x), radius, params)
            cs, _ = advance_one_step_crn(cs, float(x), radius, params)

        seq_features.append(morphology_features(ss, radius))
        crn_features.append(morphology_features(cs, radius))
        seq_pop.append(len(ss.occupied))
        crn_pop.append(len(cs.occupied))

    X = np.asarray(seq_features, dtype=float)
    Y = np.asarray(crn_features, dtype=float)
    observed = energy_distance_statistic(X, Y)

    pooled = np.vstack([X, Y])
    n = len(X)
    rng = np.random.default_rng(seed + 9_000)
    null = np.empty(profile["permutations"])
    for i in range(profile["permutations"]):
        order = rng.permutation(len(pooled))
        null[i] = energy_distance_statistic(
            pooled[order[:n]], pooled[order[n:2*n]]
        )

    p = (1 + float(np.sum(null >= observed))) / (len(null) + 1)

    result = {
        "sequential_exact": sequential_exact,
        "crn_exact": crn_exact,
        "canonical_runner": "sequential RNG over sorted(frontier)",
        "counterfactual_runner": "cell-keyed CRN U(seed, step, q, r)",
        "canonical_substrate_modified": False,
        "validation_groups_per_runner": groups,
        "marginal_feature_test": {
            "energy_distance": float(observed),
            "p_value": float(p),
            "null_q95": float(np.quantile(null, 0.95)),
            "interpretation": (
                "Failure to reject is compatibility evidence only; it does not "
                "prove equality of the two stochastic laws."
            ),
        },
        "population": {
            "sequential": summarize_scalar(
                seq_pop, profile["bootstrap_reps"], seed + 9_100
            ),
            "crn": summarize_scalar(
                crn_pop, profile["bootstrap_reps"], seed + 9_200
            ),
        },
    }

    reporter.json("stage-00-coupling-audit.json", result)
    reporter.stage(
        "stage-00-coupling-audit.md",
        "Stage 0 — Canonical Sequential RNG vs Counterfactual CRN",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_1_coupling_impulse_audit(
    reporter, profile, params, seed, image_dir
):
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    pulse_idx = profile["pulse_step"]
    observations = sorted(set(profile["observation_steps"] + [pulse_idx + 1]))
    zero_bits = pulse_train(horizon, [])
    pulse_bits = pulse_train(horizon, [pulse_idx])

    fields = ("symdiff", "feature_distance", "abs_population_difference")
    kinds = (
        "sequential_causal",
        "crn_causal",
        "independent_reseed_reference",
    )
    data = {
        kind: {t: {f: [] for f in fields} for t in observations}
        for kind in kinds
    }

    def record(target, t, a, b):
        d = state_difference(a, b, radius)
        target[t]["symdiff"].append(d["normalized_symmetric_difference"])
        target[t]["feature_distance"].append(d["feature_distance"])
        target[t]["abs_population_difference"].append(
            d["absolute_population_difference"]
        )

    for g in tqdm(range(groups), desc="Stage 1 coupling impulse audit"):
        gseed = seed + 10_000 + g * 1013
        env = make_environment(warmup + horizon, gseed + 1)
        future = env[warmup:]

        seq_cp = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        crn_cp = warm_checkpoint_crn(env, warmup, gseed + 2, radius, params)

        seq0 = advance_with_pulses(
            seq_cp, future, zero_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        seq1 = advance_with_pulses(
            seq_cp, future, pulse_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        crn0 = advance_with_pulses_crn(
            crn_cp, future, zero_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        crn1 = advance_with_pulses_crn(
            crn_cp, future, pulse_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        r1cp = reseed_state_rng(seq_cp, gseed + 901)
        r2cp = reseed_state_rng(seq_cp, gseed + 902)
        r1 = advance_with_pulses(
            r1cp, future, zero_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        r2 = advance_with_pulses(
            r2cp, future, zero_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            record(data["sequential_causal"], t, seq1[t], seq0[t])
            record(data["crn_causal"], t, crn1[t], crn0[t])
            record(data["independent_reseed_reference"], t, r1[t], r2[t])

    summary = {}
    for kind_i, kind in enumerate(kinds):
        summary[kind] = {}
        for t in observations:
            summary[kind][str(t)] = {}
            for metric_i, metric in enumerate(fields):
                summary[kind][str(t)][metric] = summarize_scalar(
                    data[kind][t][metric],
                    profile["bootstrap_reps"],
                    seed + 100_000 + kind_i * 10_000 + t * 101 + metric_i,
                )

    ratios = {}
    for t in observations:
        ref = summary["independent_reseed_reference"][str(t)]["symdiff"]["mean"]
        seqv = summary["sequential_causal"][str(t)]["symdiff"]["mean"]
        crnv = summary["crn_causal"][str(t)]["symdiff"]["mean"]
        ratios[str(t)] = {
            "sequential_to_independent": float(seqv / ref) if ref > 1e-12 else None,
            "crn_to_independent": float(crnv / ref) if ref > 1e-12 else None,
        }

    result = {
        "pulse_zero_index": pulse_idx,
        "pulse_elapsed_step": pulse_idx + 1,
        "observation_steps": observations,
        "summary": summary,
        "ratios": ratios,
        "interpretation": (
            "Pathwise divergence is compared under two declared couplings. A "
            "difference between them is evidence that pathwise counterfactual "
            "distance is coupling-dependent, not a coupling-invariant property."
        ),
    }

    reporter.json("stage-01-randomness-coupling-audit.json", result)
    reporter.stage(
        "stage-01-randomness-coupling-audit.md",
        "Stage 1 — Randomness Coupling Audit",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    for key, label in (
        ("sequential_causal", "pulse: sequential RNG"),
        ("crn_causal", "pulse: keyed CRN"),
        ("independent_reseed_reference", "independent reseeds"),
    ):
        ys = [summary[key][str(t)]["symdiff"]["mean"] for t in xs]
        ax.plot(xs, ys, marker="o", label=label)
    ax.axvline(pulse_idx + 1, linestyle="--", linewidth=1)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Mean normalized morphology symmetric difference")
    ax.set_title("Pathwise divergence under alternative randomness couplings")
    ax.legend()
    fig.tight_layout()
    fig.savefig(image_dir / "ch17-v5-01-randomness-coupling-audit.png", dpi=160)
    plt.close(fig)

    return result


def stage_2_crn_superposition_with_floor(
    reporter, profile, params, seed, image_dir
):
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    observations = profile["matched_observation_steps"]

    patterns = {
        "clustered": [0, 1, 2, 7],
        "dispersed": [0, 4, 5, 7],
    }
    all_positions = sorted(set(sum(patterns.values(), [])))
    baseline_bits = pulse_train(horizon, [])
    single_bits = {p: pulse_train(horizon, [p]) for p in all_positions}
    train_bits = {
        name: pulse_train(horizon, positions)
        for name, positions in patterns.items()
    }

    baseline_features = {t: [] for t in observations}
    single_delta = {t: {p: [] for p in all_positions} for t in observations}
    train_delta = {t: {name: [] for name in patterns} for t in observations}

    for g in tqdm(range(groups), desc="Stage 2 CRN superposition"):
        gseed = seed + 20_000 + g * 1019
        env = make_environment(warmup + horizon, gseed + 1)
        future = env[warmup:]
        cp = warm_checkpoint_crn(env, warmup, gseed + 2, radius, params)

        base = advance_with_pulses_crn(
            cp, future, baseline_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        singles = {
            p: advance_with_pulses_crn(
                cp, future, bits_, profile["message_gain"],
                radius, params, observations, profile["max_capacity_fraction"],
            )
            for p, bits_ in single_bits.items()
        }
        trains = {
            name: advance_with_pulses_crn(
                cp, future, bits_, profile["message_gain"],
                radius, params, observations, profile["max_capacity_fraction"],
            )
            for name, bits_ in train_bits.items()
        }

        for t in observations:
            f0 = morphology_features(base[t], radius)
            baseline_features[t].append(f0)
            for p in all_positions:
                single_delta[t][p].append(
                    morphology_features(singles[p][t], radius) - f0
                )
            for name in patterns:
                train_delta[t][name].append(
                    morphology_features(trains[name][t], radius) - f0
                )

    rng = np.random.default_rng(seed + 220_000)
    out = {}

    for t in observations:
        base_arr = np.asarray(baseline_features[t], dtype=float)
        floor_norms = []
        floor_reps = max(100, min(500, profile["bootstrap_reps"]))
        for _ in range(floor_reps):
            order = rng.permutation(len(base_arr))
            half = len(order) // 2
            if half < 2:
                continue
            A = base_arr[order[:half]]
            B = base_arr[order[half:2*half]]
            floor_norms.append(
                float(np.linalg.norm(np.mean(A, axis=0) - np.mean(B, axis=0)))
            )

        out[str(t)] = {
            "zero_response_population_mean_noise_floor": summarize_scalar(
                floor_norms,
                profile["bootstrap_reps"],
                seed + 221_000 + t,
            )
        }

        single_arrays = {
            p: np.asarray(single_delta[t][p], dtype=float)
            for p in all_positions
        }
        for name, positions in patterns.items():
            actual = np.asarray(train_delta[t][name], dtype=float)
            out[str(t)][name] = bootstrap_superposition_summary(
                single_arrays,
                actual,
                positions,
                profile["bootstrap_reps"],
                seed + 222_000 + t * 31
                + (0 if name == "clustered" else 1),
            )

    result = {
        "coupling": "cell-keyed CRN",
        "patterns_zero_indexed": patterns,
        "summary": out,
        "interpretation": (
            "Superposition residuals are compared with a finite-sample baseline "
            "mean-difference floor before being described as non-additivity."
        ),
    }
    reporter.json("stage-02-crn-superposition-with-floor.json", result)
    reporter.stage(
        "stage-02-crn-superposition-with-floor.md",
        "Stage 2 — CRN Superposition With Mean-Estimation Floor",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def ridge_stat_subset(X: np.ndarray, Y: np.ndarray, indices: Sequence[int]) -> float:
    idx = np.asarray(indices, dtype=int)
    return stat_paired_ridge_hotelling(X[:, idx], Y[:, idx])


def paired_ridge_subset_test(
    X, Y, indices, permutations, seed
):
    observed = ridge_stat_subset(X, Y, indices)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)
    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X)).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = ridge_stat_subset(Xp, Yp, indices)
    return {
        "statistic": float(observed),
        "p_value": float((1 + np.sum(null >= observed)) / (len(null) + 1)),
        "null_q95": float(np.quantile(null, 0.95)),
        "permutations": int(permutations),
    }


def stage_3_short_matched_arrangement(
    reporter, profile, params, seed, image_dir
):
    invariants = validate_matched_codewords(
        MATCHED_CODEWORD_A, MATCHED_CODEWORD_B
    )
    pa = codeword_pulse_positions(MATCHED_CODEWORD_A)
    pb = codeword_pulse_positions(MATCHED_CODEWORD_B)
    last_pulse_elapsed = pa[-1] + 1

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
        coupling: {t: {"A": [], "B": []} for t in observations}
        for coupling in ("sequential", "crn")
    }
    symdiff = {
        coupling: {t: [] for t in observations}
        for coupling in ("sequential", "crn")
    }

    for g in tqdm(range(groups), desc="Stage 3 short matched timing"):
        gseed = seed + 30_000 + g * 1021
        env = make_environment(warmup + horizon, gseed + 1)
        future = env[warmup:]

        seq_cp = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        crn_cp = warm_checkpoint_crn(env, warmup, gseed + 2, radius, params)

        seq_a = advance_with_pulses(
            seq_cp, future, bits_a, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        seq_b = advance_with_pulses(
            seq_cp, future, bits_b, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        crn_a = advance_with_pulses_crn(
            crn_cp, future, bits_a, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        crn_b = advance_with_pulses_crn(
            crn_cp, future, bits_b, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            for coupling, aa, bb in (
                ("sequential", seq_a[t], seq_b[t]),
                ("crn", crn_a[t], crn_b[t]),
            ):
                features[coupling][t]["A"].append(
                    morphology_features(aa, radius)
                )
                features[coupling][t]["B"].append(
                    morphology_features(bb, radius)
                )
                d = state_difference(aa, bb, radius)
                symdiff[coupling][t].append(
                    d["normalized_symmetric_difference"]
                )

    results = {}
    for coupling_i, coupling in enumerate(("sequential", "crn")):
        results[coupling] = {}
        for t in observations:
            X = np.asarray(features[coupling][t]["A"], dtype=float)
            Y = np.asarray(features[coupling][t]["B"], dtype=float)
            results[coupling][str(t)] = {
                "steps_since_last_pulse": int(t - last_pulse_elapsed),
                "symdiff": summarize_scalar(
                    symdiff[coupling][t],
                    profile["bootstrap_reps"],
                    seed + 330_000 + coupling_i * 10_000 + t,
                ),
                "ridge_all24": paired_ridge_subset_test(
                    X, Y, range(len(FEATURE_NAMES)),
                    profile["permutations"],
                    seed + 331_000 + coupling_i * 10_000 + t,
                ),
                "ridge_angular9": paired_ridge_subset_test(
                    X, Y, ANGULAR_FEATURE_INDICES,
                    profile["permutations"],
                    seed + 332_000 + coupling_i * 10_000 + t,
                ),
                "top_directional_features": top_directional_features(X, Y),
            }

    result = {
        "codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "pulse_positions_A_zero_indexed": pa,
        "pulse_positions_B_zero_indexed": pb,
        "codeword_invariants": invariants,
        "last_pulse_elapsed_step": last_pulse_elapsed,
        "observation_steps": observations,
        "angular_subspace": {
            "basis": "mechanism-derived before v5 data",
            "feature_names": list(ANGULAR_FEATURE_NAMES),
            "feature_indices": list(ANGULAR_FEATURE_INDICES),
        },
        "results": results,
        "scientific_status": "EXPLORATORY ONLY",
    }
    reporter.json("stage-03-short-matched-arrangement.json", result)
    reporter.stage(
        "stage-03-short-matched-arrangement.md",
        "Stage 3 — Short Matched Timing Under Sequential RNG and CRN",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result, features


def centered_symmetrized_noise(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    D = np.asarray(X, dtype=float) - np.asarray(Y, dtype=float)
    D = D - np.mean(D, axis=0, keepdims=True)
    return np.vstack([D, -D])


def synthetic_paired_sample(
    base_pool, noise_pool, indices, shift_norm, rng
):
    n = len(base_pool) // 2
    base = base_pool[rng.integers(0, len(base_pool), size=n)].copy()
    noise = noise_pool[rng.integers(0, len(noise_pool), size=n)].copy()

    idx = np.asarray(indices, dtype=int)
    direction = np.ones(len(idx), dtype=float)
    direction /= np.linalg.norm(direction)

    sd = np.std(base[:, idx], axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    shift = np.zeros_like(base)
    shift[:, idx] = float(shift_norm) * direction[None, :] * sd[None, :]

    A = base + 0.5 * noise - 0.5 * shift
    B = base - 0.5 * noise + 0.5 * shift
    return A, B


def stage_4_and_5_sham_mde(
    reporter, profile, matched_features, seed
):
    endpoint = min(profile["matched_observation_steps"])
    X = np.asarray(matched_features["crn"][endpoint]["A"], dtype=float)
    Y = np.asarray(matched_features["crn"][endpoint]["B"], dtype=float)

    noise_pool = centered_symmetrized_noise(X, Y)
    base_pool = np.vstack([X, Y])

    instruments = {
        "ridge_all24": tuple(range(len(FEATURE_NAMES))),
        "ridge_angular9": tuple(ANGULAR_FEATURE_INDICES),
    }
    reps = int(profile["calibration_reps"])
    perms = int(profile["calibration_permutations"])
    strengths = list(map(float, profile["mde_strengths"]))
    target = float(profile["mde_target_power"])
    rng = np.random.default_rng(seed + 400_000)

    outputs = {}
    for name, indices in instruments.items():
        rows = []
        for strength in strengths:
            detections = 0
            pvals = []
            for rep in tqdm(
                range(reps),
                desc=f"Stage 4/5 {name} shift={strength:g}",
                leave=False,
            ):
                A, B = synthetic_paired_sample(
                    base_pool, noise_pool, indices, strength, rng
                )
                test = paired_ridge_subset_test(
                    A, B, indices, perms,
                    seed + 410_000 + rep * 101
                    + int(strength * 1000)
                    + (0 if name == "ridge_all24" else 20_000),
                )
                detections += int(test["p_value"] < 0.05)
                pvals.append(test["p_value"])

            rows.append({
                "shift_norm": strength,
                "detection_rate_alpha_0_05": float(detections / reps),
                "mean_p_value": float(np.mean(pvals)),
            })

        zero = next(r for r in rows if r["shift_norm"] == 0.0)
        mde80 = next(
            (
                r["shift_norm"]
                for r in rows
                if r["shift_norm"] > 0
                and r["detection_rate_alpha_0_05"] >= target
            ),
            None,
        )

        outputs[name] = {
            "feature_names": [FEATURE_NAMES[i] for i in indices],
            "null_fpr": zero["detection_rate_alpha_0_05"],
            "target_power": target,
            "mde80_grid_estimate": mde80,
            "power_curve": rows,
        }

    result = {
        "endpoint": endpoint,
        "calibration_role": "EXPLORATORY INSTRUMENT DEVELOPMENT",
        "noise_model": (
            "centered + sign-symmetrized CRN matched-pair deltas from this v5 "
            "pilot; therefore this same pilot is not confirmatory evidence"
        ),
        "calibration_reps": reps,
        "permutations_per_test": perms,
        "instruments": outputs,
        "interpretation": (
            "MDE grid values describe instrument resolution for the declared "
            "synthetic direction. They are not upper bounds on the real effect."
        ),
    }
    reporter.json("stage-04-05-sham-and-mde.json", result)
    reporter.stage(
        "stage-04-05-sham-and-mde.md",
        "Stages 4–5 — End-to-End Paired Sham and MDE Calibration",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_6_verdict(
    reporter, stage0, stage1, stage2, stage3, calibration
):
    marginal_p = stage0["marginal_feature_test"]["p_value"]
    crn_compatible = marginal_p >= 0.05
    first_obs = str(min(stage3["observation_steps"]))

    result = {
        "experiment_role": "EXPLORATORY / RANDOMNESS-COUPLING AUDIT",
        "canonical_substrate_modified": False,
        "crn_is_separate_counterfactual_runner": True,
        "marginal_compatibility_not_rejected_at_0_05": bool(crn_compatible),
        "marginal_compatibility_p_value": float(marginal_p),
        "short_codeword_first_observation": int(first_obs),
        "short_codeword_sequential_symdiff_mean": float(
            stage3["results"]["sequential"][first_obs]["symdiff"]["mean"]
        ),
        "short_codeword_crn_symdiff_mean": float(
            stage3["results"]["crn"][first_obs]["symdiff"]["mean"]
        ),
        "matched_arrangement_status": "UNTESTED",
        "chapter18_status": "DEFERRED",
        "bounded_statement": (
            "V5 audits how randomness coupling changes pathwise perturbation "
            "response. The short matched-arrangement experiment remains an "
            "exploratory instrument-development pilot, not a memory or "
            "information-survival claim."
        ),
        "decision_logic": {
            "if_crn_marginals_disagree": (
                "Do not use CRN as a variance-reduction coupling until the "
                "marginal discrepancy is understood."
            ),
            "if_crn_marginals_compatible_and_coherence_improves": (
                "Freeze the CRN runner, short codewords, observation schedule "
                "and chosen ridge instrument; choose N from MDE/power curves "
                "before a new-seed confirmatory run."
            ),
            "if_crn_does_not_improve_coherence": (
                "Treat rapid decorrelation as robust to coupling choice and "
                "reconsider temporal-arrangement recoverability."
            ),
        },
        "nonclaims": [
            "memory",
            "information storage",
            "sender-specific signalling",
            "semantics",
            "Shannon channel capacity",
            "life",
        ],
    }

    reporter.json("stage-06-v5-verdict.json", result)
    reporter.stage(
        "stage-06-v5-verdict.md",
        "Stage 6 — Bounded V5 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260812)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("research/digital-life/ch17-perturbation-dynamics-v5"),
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    params = CrystalParams()
    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)
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
        "version_5_focus": (
            "Randomness-coupling audit: preserve the canonical sequential-RNG "
            "substrate, add a separate cell-keyed CRN counterfactual runner, "
            "audit marginal compatibility, shorten the matched codewords, add "
            "a mean-estimation noise floor, and report paired ridge MDE curves."
        ),
        "run_type": "EXPLORATORY",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "matched_codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "matched_codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "matched_codeword_validation": codeword_check,
        "angular_subspace": list(ANGULAR_FEATURE_NAMES),
        "scientific_boundary": (
            "Perturbation-response and counterfactual-coupling characterization "
            "only. Chapter 18 information-survival remains deferred."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 17 — HOW DOES THE CRYSTAL RESPOND TO PERTURBATION?")
    print(f"profile={args.profile} version={EXPERIMENT_VERSION}")
    print("=" * 78)

    s0 = stage_0_reproducibility_and_marginals(
        reporter, profile, params, args.seed, args.image_dir
    )
    s1 = stage_1_coupling_impulse_audit(
        reporter, profile, params, args.seed, args.image_dir
    )
    s2 = stage_2_crn_superposition_with_floor(
        reporter, profile, params, args.seed, args.image_dir
    )
    s3, matched_features = stage_3_short_matched_arrangement(
        reporter, profile, params, args.seed, args.image_dir
    )
    s45 = stage_4_and_5_sham_mde(
        reporter, profile, matched_features, args.seed
    )
    s6 = stage_6_verdict(reporter, s0, s1, s2, s3, s45)

    metadata.update({
        "finished_at_unix": time.time(),
        "reproducibility_passed": bool(
            s0["sequential_exact"] and s0["crn_exact"]
        ),
        "marginal_compatibility_p_value": (
            s0["marginal_feature_test"]["p_value"]
        ),
        "final_status": s6["matched_arrangement_status"],
        "chapter18_status": s6["chapter18_status"],
    })

    reporter.json("run-metadata.json", metadata)
    reporter.assemble(
        "ch17-perturbation-dynamics-v5-full-report.md",
        metadata=metadata,
    )

    print("\n" + "=" * 78)
    print("V5 COMPLETE")
    print(
        "marginal CRN compatibility p="
        f"{s0['marginal_feature_test']['p_value']:.6g}"
    )
    print(f"matched arrangement status={s6['matched_arrangement_status']}")
    print(
        "report="
        f"{reporter.root / 'ch17-perturbation-dynamics-v5-full-report.md'}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
