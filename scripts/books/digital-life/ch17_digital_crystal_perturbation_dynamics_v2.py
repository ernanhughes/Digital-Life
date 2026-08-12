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
EXPERIMENT_VERSION = "digital-crystal-perturbation-dynamics-v2"
SCHEMA_VERSION = 2

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
        "horizon": 32,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 6, 8, 12, 16, 20, 24, 32],
        "matched_observation_steps": [16, 18, 20, 24, 28, 32],
        "permutations": 250,
        "bootstrap_reps": 500,
        "sham_reps": 20,
        "spike_in_reps": 100,
        "spike_in_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
        "sensitivity_target_sd": 1.0,
        "sensitivity_target_power": 0.80,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 60,
        "radius": 72,
        "warmup_steps": 16,
        "horizon": 40,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40],
        "matched_observation_steps": [16, 18, 20, 24, 28, 32, 40],
        "permutations": 1000,
        "bootstrap_reps": 2000,
        "sham_reps": 50,
        "spike_in_reps": 250,
        "spike_in_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
        "sensitivity_target_sd": 1.0,
        "sensitivity_target_power": 0.80,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 120,
        "radius": 88,
        "warmup_steps": 18,
        "horizon": 48,
        "pulse_step": 4,
        "message_gain": 0.65,
        "observation_steps": [1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48],
        "matched_observation_steps": [16, 18, 20, 24, 28, 32, 40, 48],
        "permutations": 5000,
        "bootstrap_reps": 5000,
        "sham_reps": 100,
        "spike_in_reps": 500,
        "spike_in_strengths": [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
        "sensitivity_target_sd": 1.0,
        "sensitivity_target_power": 0.80,
        "max_capacity_fraction": 0.85,
    },
}


# Matched endpoint pair:
#   equal length
#   equal pulse count
#   equal first pulse
#   equal last pulse
#   different interior arrangement
MATCHED_CODEWORD_A = tuple(int(c) for c in "1110000000000001")
MATCHED_CODEWORD_B = tuple(int(c) for c in "1000000110000001")


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
        path = self.root / "ch17-perturbation-dynamics-v2-full-report.md"
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

def stage_0_reproducibility(reporter, profile, params, seed):
    env = make_environment(24, seed + 1)

    def once():
        s = initial_state(seed + 2)
        adds = []
        for x in env:
            s, n = advance_one_step(s, float(x), profile["radius"], params)
            adds.append(n)
        return s, adds

    a, aa = once()
    b, bb = once()
    result = {
        "canonical_rng_traversal": "sorted(frontier)",
        "exact": (
            a.occupied == b.occupied
            and a.rng_state == b.rng_state
            and aa == bb
        ),
        "hash_a": morphology_hash(a),
        "hash_b": morphology_hash(b),
    }
    if not result["exact"]:
        raise RuntimeError("Reproducibility invariant failed.")

    reporter.json("stage-00-reproducibility.json", result)
    reporter.stage(
        "stage-00-reproducibility.md",
        "Stage 0 — Freeze the Substrate",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


# ---------------------------------------------------------------------------
# Stage 1 — isolated impulse response
# ---------------------------------------------------------------------------


def stage_1_impulse_response(reporter, profile, params, seed, image_dir):
    """
    Characterize two distinct quantities:

    A. Exact causal fork:
       same checkpoint, same RNG state, same future environment,
       pulse bit changed only.

    B. Independent stochastic baseline:
       same checkpoint geometry and future environment, no pulse in either arm,
       but independently reseeded RNG continuations.

    The second quantity is not a counterfactual estimate. It is a scale for the
    ordinary stochastic spread of equivalent continuations.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    pulse_idx = profile["pulse_step"]
    observations = sorted(set(profile["observation_steps"] + [pulse_idx + 1]))

    def blank_series():
        return {
            t: {
                "population_delta": [],
                "absolute_population_delta": [],
                "symdiff": [],
                "feature_distance": [],
            }
            for t in observations
        }

    causal = blank_series()
    stochastic = blank_series()
    excess_symdiff = {t: [] for t in observations}
    excess_feature_distance = {t: [] for t in observations}
    max_capacity = 0.0

    baseline_bits = pulse_train(horizon, [])
    pulse_bits = pulse_train(horizon, [pulse_idx])

    for group in tqdm(range(groups), desc="Stage 1 impulse + stochastic baseline"):
        gseed = seed + 10_000 + group * 1009
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        future = env[warmup:]

        # Exact causal pair: same initial RNG state.
        base_exact = advance_with_pulses(
            checkpoint, future, baseline_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        pulse_exact = advance_with_pulses(
            checkpoint, future, pulse_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        # Independent no-pulse stochastic pair: same geometry/environment,
        # different RNG continuations.
        stoch_a_state = reseed_state_rng(checkpoint, gseed + 901)
        stoch_b_state = reseed_state_rng(checkpoint, gseed + 902)
        stoch_a = advance_with_pulses(
            stoch_a_state, future, baseline_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        stoch_b = advance_with_pulses(
            stoch_b_state, future, baseline_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            dc = state_difference(pulse_exact[t], base_exact[t], radius)
            ds = state_difference(stoch_a[t], stoch_b[t], radius)

            for target, diff in ((causal, dc), (stochastic, ds)):
                target[t]["population_delta"].append(diff["population_difference"])
                target[t]["absolute_population_delta"].append(
                    diff["absolute_population_difference"]
                )
                target[t]["symdiff"].append(diff["normalized_symmetric_difference"])
                target[t]["feature_distance"].append(diff["feature_distance"])

            excess_symdiff[t].append(
                dc["normalized_symmetric_difference"]
                - ds["normalized_symmetric_difference"]
            )
            excess_feature_distance[t].append(
                dc["feature_distance"] - ds["feature_distance"]
            )

            max_capacity = max(
                max_capacity,
                capacity_fraction(base_exact[t], radius),
                capacity_fraction(pulse_exact[t], radius),
                capacity_fraction(stoch_a[t], radius),
                capacity_fraction(stoch_b[t], radius),
            )

    causal_summary = summarize_difference_series(
        causal, profile, seed + 100_000
    )
    stochastic_summary = summarize_difference_series(
        stochastic, profile, seed + 120_000
    )
    excess_summary = {}
    for t in observations:
        excess_summary[str(t)] = {
            "symdiff_causal_minus_stochastic": bootstrap_mean_ci(
                excess_symdiff[t], profile["bootstrap_reps"],
                seed + 140_000 + t,
            ),
            "feature_distance_causal_minus_stochastic": bootstrap_mean_ci(
                excess_feature_distance[t], profile["bootstrap_reps"],
                seed + 150_000 + t,
            ),
        }

    result = {
        "pulse_zero_index": pulse_idx,
        "pulse_elapsed_step": pulse_idx + 1,
        "message_gain": profile["message_gain"],
        "groups": groups,
        "observation_steps": observations,
        "max_capacity_fraction_observed": max_capacity,
        "exact_causal_fork": causal_summary,
        "independent_no_pulse_stochastic_baseline": stochastic_summary,
        "excess_over_stochastic_baseline": excess_summary,
        "interpretation": (
            "The exact causal fork measures the effect of changing the pulse while "
            "holding checkpoint RNG state and future environment fixed. The "
            "independent no-pulse fork is only a reference scale for stochastic "
            "continuation spread; it is not an exact counterfactual."
        ),
    }

    reporter.json("stage-01-impulse-response.json", result)
    reporter.stage(
        "stage-01-impulse-response.md",
        "Stage 1 — One Pulse, and the Background Divergence Scale",
        f"""The pulse effect is measured against an exact matched continuation,
and separately compared with the spread of independent no-pulse stochastic forks.

```json
{json.dumps(result, indent=2)}
```""",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    causal_y = [causal_summary[str(t)]["symdiff"]["mean"] for t in xs]
    stoch_y = [stochastic_summary[str(t)]["symdiff"]["mean"] for t in xs]
    ax.plot(xs, causal_y, marker="o", label="exact pulse vs baseline")
    ax.plot(xs, stoch_y, marker="o", label="independent no-pulse forks")
    ax.axvline(pulse_idx + 1, linestyle="--", linewidth=1)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Normalized morphology symmetric difference")
    ax.set_title("Causal pulse divergence vs ordinary stochastic divergence scale")
    ax.legend()
    fig.tight_layout()
    fig.savefig(image_dir / "ch17-v2-01-impulse-vs-stochastic.png", dpi=160)
    plt.close(fig)

    return result


# ---------------------------------------------------------------------------
# Stage 2 — ensemble-mean superposition
# ---------------------------------------------------------------------------

def stage_2_superposition(reporter, profile, params, seed, image_dir):
    """
    Operational additivity test at the ensemble-mean morphology-feature level.

    The v1 script added together group-specific stochastic counterfactual deltas.
    That mixed pulse-response structure with separate path-dependent stochastic
    divergences. v2 instead averages the response to each isolated pulse across
    receiver groups first, then sums those ensemble mean responses.

        predicted mean train response
            = sum_s E[Delta F | isolated pulse at s]

    This is compared with:

        actual mean train response
            = E[Delta F | full pulse train]

    A residual still does not establish memory. It establishes only that this
    declared additive mean-response model is inadequate in the measurement space.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    observations = profile["matched_observation_steps"]

    patterns = {
        "clustered": [0, 1, 2, 15],
        "dispersed": [0, 7, 8, 15],
    }
    all_positions = sorted(set(sum(patterns.values(), [])))

    baseline_bits = pulse_train(horizon, [])
    singles = {p: pulse_train(horizon, [p]) for p in all_positions}
    trains = {
        name: pulse_train(horizon, positions)
        for name, positions in patterns.items()
    }

    single_delta = {
        t: {p: [] for p in all_positions}
        for t in observations
    }
    train_delta = {
        t: {name: [] for name in patterns}
        for t in observations
    }

    for group in tqdm(range(groups), desc="Stage 2 ensemble superposition"):
        gseed = seed + 20_000 + group * 1013
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        future = env[warmup:]

        base = advance_with_pulses(
            checkpoint, future, baseline_bits, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        single_obs = {}
        for pos, bits_ in singles.items():
            single_obs[pos] = advance_with_pulses(
                checkpoint, future, bits_, profile["message_gain"],
                radius, params, observations, profile["max_capacity_fraction"],
            )

        train_obs = {}
        for name, bits_ in trains.items():
            train_obs[name] = advance_with_pulses(
                checkpoint, future, bits_, profile["message_gain"],
                radius, params, observations, profile["max_capacity_fraction"],
            )

        for t in observations:
            f0 = morphology_features(base[t], radius)
            for pos in all_positions:
                single_delta[t][pos].append(
                    morphology_features(single_obs[pos][t], radius) - f0
                )
            for name in patterns:
                train_delta[t][name].append(
                    morphology_features(train_obs[name][t], radius) - f0
                )

    summary = {}
    for t in observations:
        summary[str(t)] = {}
        single_arrays = {
            p: np.asarray(single_delta[t][p], dtype=float)
            for p in all_positions
        }
        for name, positions in patterns.items():
            actual = np.asarray(train_delta[t][name], dtype=float)
            summary[str(t)][name] = bootstrap_superposition_summary(
                single_arrays,
                actual,
                positions,
                profile["bootstrap_reps"],
                seed + 220_000 + t * 29 + (0 if name == "clustered" else 1),
            )

    result = {
        "measurement_space": f"{len(FEATURE_NAMES)} normalized morphology features",
        "model": "ensemble-mean isolated-pulse additive prediction",
        "patterns_zero_indexed": patterns,
        "same_onset": True,
        "same_offset": True,
        "same_pulse_count": True,
        "summary": summary,
        "interpretation": (
            "Small ensemble-mean residuals support this declared additive mean-"
            "response approximation. Large residuals reject that approximation "
            "in the measured feature space, but do not establish memory, storage, "
            "or a special information-processing mechanism."
        ),
    }

    reporter.json("stage-02-ensemble-superposition.json", result)
    reporter.stage(
        "stage-02-ensemble-superposition.md",
        "Stage 2 — Can Ensemble Single-Pulse Responses Predict the Pulse Train?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    for name in patterns:
        ys = [
            summary[str(t)][name]["relative_superposition_error"]["value"]
            for t in xs
        ]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Ensemble relative superposition error")
    ax.set_title("Ensemble-mean additive prediction error")
    ax.legend()
    fig.tight_layout()
    fig.savefig(image_dir / "ch17-v2-02-ensemble-superposition.png", dpi=160)
    plt.close(fig)

    return result


# ---------------------------------------------------------------------------
# Stage 3 — matched endpoint arrangement test
# ---------------------------------------------------------------------------

def stage_3_matched_arrangement(reporter, profile, params, seed, image_dir):
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    observations = profile["matched_observation_steps"]

    if sum(MATCHED_CODEWORD_A) != sum(MATCHED_CODEWORD_B):
        raise RuntimeError("Matched codewords do not have equal pulse count.")
    if MATCHED_CODEWORD_A[0] != MATCHED_CODEWORD_B[0]:
        raise RuntimeError("Matched codewords do not have equal onset.")
    if MATCHED_CODEWORD_A[-1] != MATCHED_CODEWORD_B[-1]:
        raise RuntimeError("Matched codewords do not have equal offset.")

    bits_a = tuple(MATCHED_CODEWORD_A) + (0,) * max(
        0, horizon - len(MATCHED_CODEWORD_A)
    )
    bits_b = tuple(MATCHED_CODEWORD_B) + (0,) * max(
        0, horizon - len(MATCHED_CODEWORD_B)
    )

    features = {t: {"A": [], "B": []} for t in observations}
    paired_diff = {
        t: {
            "symdiff": [],
            "feature_distance": [],
            "abs_population_difference": [],
        }
        for t in observations
    }

    for group in tqdm(range(groups), desc="Stage 3 matched arrangement"):
        gseed = seed + 30_000 + group * 1019
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        future = env[warmup:]

        obs_a = advance_with_pulses(
            checkpoint, future, bits_a, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )
        obs_b = advance_with_pulses(
            checkpoint, future, bits_b, profile["message_gain"],
            radius, params, observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            features[t]["A"].append(morphology_features(obs_a[t], radius))
            features[t]["B"].append(morphology_features(obs_b[t], radius))
            d = state_difference(obs_a[t], obs_b[t], radius)
            paired_diff[t]["symdiff"].append(
                d["normalized_symmetric_difference"]
            )
            paired_diff[t]["feature_distance"].append(d["feature_distance"])
            paired_diff[t]["abs_population_difference"].append(
                d["absolute_population_difference"]
            )

    results = {}
    for t in observations:
        X = np.asarray(features[t]["A"], dtype=float)
        Y = np.asarray(features[t]["B"], dtype=float)
        test = paired_swap_permutation_test(
            X, Y, profile["permutations"], seed + 300_000 + t
        )
        results[str(t)] = {
            "energy_distance_test": test,
            "paired_state_difference": {
                name: bootstrap_mean_ci(
                    values,
                    profile["bootstrap_reps"],
                    seed + 310_000 + t * 17 + i,
                )
                for i, (name, values) in enumerate(paired_diff[t].items())
            },
            "steps_since_last_pulse_A": max(0, t - 16),
            "steps_since_last_pulse_B": max(0, t - 16),
            "equal_time_since_last_pulse": True,
        }

    result = {
        "codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "pulse_positions_A_zero_indexed": [
            i for i, v in enumerate(MATCHED_CODEWORD_A) if v
        ],
        "pulse_positions_B_zero_indexed": [
            i for i, v in enumerate(MATCHED_CODEWORD_B) if v
        ],
        "same_pulse_count": True,
        "same_first_pulse": True,
        "same_last_pulse": True,
        "groups": groups,
        "primary_measurement": (
            "decoder-free multivariate energy distance on normalized morphology "
            "features with paired within-group swap permutation"
        ),
        "results": results,
        "interpretation": (
            "Paired trajectories may diverge strongly even when the ensemble "
            "distributions are not systematically distinguishable. The primary "
            "test asks for a consistent arrangement signature across groups."
        ),
    }

    reporter.json("stage-03-matched-arrangement.json", result)
    reporter.stage(
        "stage-03-matched-arrangement.md",
        "Stage 3 — Same Count, Same Onset, Same Offset; Different Interior Timing",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    ys = [
        results[str(t)]["paired_state_difference"]["symdiff"]["mean"]
        for t in xs
    ]
    lo = [
        results[str(t)]["paired_state_difference"]["symdiff"]["ci95_low"]
        for t in xs
    ]
    hi = [
        results[str(t)]["paired_state_difference"]["symdiff"]["ci95_high"]
        for t in xs
    ]
    ax.plot(xs, ys, marker="o")
    ax.fill_between(xs, lo, hi, alpha=0.2)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Paired normalized morphology difference")
    ax.set_title("Matched-endpoint causal trajectory divergence")
    fig.tight_layout()
    fig.savefig(image_dir / "ch17-v2-03-matched-arrangement.png", dpi=160)
    plt.close(fig)

    return result, features


# ---------------------------------------------------------------------------
# Stage 4 — sham controls
# ---------------------------------------------------------------------------

def stage_4_sham_controls(reporter, profile, params, seed):
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    endpoint = 20 if 20 in profile["matched_observation_steps"] else 16
    same_bits = tuple(MATCHED_CODEWORD_A) + (0,) * max(
        0, horizon - len(MATCHED_CODEWORD_A)
    )

    Xall = []
    for group in tqdm(range(groups * 2), desc="Stage 4 sham source"):
        gseed = seed + 40_000 + group * 1021
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(env, warmup, gseed + 2, radius, params)
        future = env[warmup:]
        obs = advance_with_pulses(
            checkpoint, future, same_bits, profile["message_gain"],
            radius, params, [endpoint], profile["max_capacity_fraction"],
        )
        Xall.append(morphology_features(obs[endpoint], radius))

    Xall = np.asarray(Xall, dtype=float)
    rng = np.random.default_rng(seed + 400_000)
    p_values = []

    for _ in range(profile["sham_reps"]):
        order = rng.permutation(len(Xall))
        half = len(order) // 2
        A = Xall[order[:half]]
        B = Xall[order[half:2 * half]]
        observed = energy_distance_statistic(A, B)
        pooled = np.vstack([A, B])
        n = len(A)
        null = np.empty(profile["permutations"], dtype=float)
        for j in range(profile["permutations"]):
            perm = rng.permutation(len(pooled))
            null[j] = energy_distance_statistic(
                pooled[perm[:n]], pooled[perm[n:2*n]]
            )
        p_values.append(
            (1 + float(np.sum(null >= observed))) / (len(null) + 1)
        )

    p_values = np.asarray(p_values, dtype=float)
    alpha = 0.05
    result = {
        "known_null": True,
        "endpoint": endpoint,
        "sham_reps": profile["sham_reps"],
        "alpha": alpha,
        "false_positive_count": int(np.sum(p_values < alpha)),
        "false_positive_rate": float(np.mean(p_values < alpha)),
        "p_value_summary": bootstrap_mean_ci(
            p_values.tolist(), profile["bootstrap_reps"], seed + 410_000
        ),
        "interpretation": (
            "A small sham set can reveal gross anti-conservatism but cannot certify "
            "a nominal 5% false-positive rate."
        ),
    }

    reporter.json("stage-04-sham-controls.json", result)
    reporter.stage(
        "stage-04-sham-controls.md",
        "Stage 4 — Known-Null Calibration",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


# ---------------------------------------------------------------------------
# Stage 5 — sensitivity / spike-in curve
# ---------------------------------------------------------------------------

def stage_5_spike_in(reporter, profile, matched_features, seed):
    """
    Known-effect calibration of the declared energy-distance pipeline.

    The calibration deliberately does not claim to be a universal power curve
    for every possible multivariate alternative. It asks a narrower question:
    how often does this exact analysis detect a controlled shift of known size
    along a real, varying morphology feature?
    """
    endpoint = 20 if 20 in matched_features else 16
    X = np.asarray(matched_features[endpoint]["A"], dtype=float)
    rng = np.random.default_rng(seed + 500_000)

    feature_sd = np.std(X, axis=0)
    varying = np.flatnonzero(feature_sd > 1e-9)
    if len(varying) == 0:
        raise RuntimeError("No varying feature available for spike-in calibration.")

    dim = int(varying[np.argmax(feature_sd[varying])])
    sd = float(feature_sd[dim])

    strengths = list(profile["spike_in_strengths"])
    rows = []
    inner_perms = max(50, min(200, profile["permutations"]))

    for strength in strengths:
        detections = 0
        pvals = []
        for _ in range(profile["spike_in_reps"]):
            idx_a = rng.integers(0, len(X), size=len(X))
            idx_b = rng.integers(0, len(X), size=len(X))
            A = X[idx_a].copy()
            B = X[idx_b].copy()
            B[:, dim] += float(strength) * sd

            observed = energy_distance_statistic(A, B)
            pooled = np.vstack([A, B])
            n = len(A)
            null = np.empty(inner_perms, dtype=float)
            for j in range(inner_perms):
                perm = rng.permutation(len(pooled))
                null[j] = energy_distance_statistic(
                    pooled[perm[:n]], pooled[perm[n:2*n]]
                )
            p = (1 + float(np.sum(null >= observed))) / (inner_perms + 1)
            pvals.append(p)
            detections += int(p < 0.05)

        rows.append({
            "shift_sd_units": float(strength),
            "detection_rate_alpha_0_05": detections / profile["spike_in_reps"],
            "p_value_mean": float(np.mean(pvals)),
            "p_value_median": float(np.median(pvals)),
        })

    target_sd = float(profile["sensitivity_target_sd"])
    target_row = min(rows, key=lambda r: abs(r["shift_sd_units"] - target_sd))
    adequate = (
        target_row["detection_rate_alpha_0_05"]
        >= float(profile["sensitivity_target_power"])
    )

    result = {
        "known_effect_calibration": True,
        "endpoint": endpoint,
        "feature_index": dim,
        "feature_name": FEATURE_NAMES[dim],
        "empirical_feature_sd": sd,
        "spike_in_reps": profile["spike_in_reps"],
        "results": rows,
        "declared_sensitivity_target_sd": target_sd,
        "declared_sensitivity_target_power": profile["sensitivity_target_power"],
        "target_detection_rate": target_row["detection_rate_alpha_0_05"],
        "sensitivity_adequate_for_target": adequate,
        "interpretation": (
            "This is a narrow pipeline sensitivity curve for synthetic shifts "
            "along one real feature. Poor sensitivity prevents a strong negative "
            "interpretation of the matched-arrangement test."
        ),
    }

    reporter.json("stage-05-spike-in-sensitivity.json", result)
    reporter.stage(
        "stage-05-spike-in-sensitivity.md",
        "Stage 5 — Known-Effect Sensitivity Curve",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


# ---------------------------------------------------------------------------
# Stage 6 — bounded verdict
# ---------------------------------------------------------------------------

def stage_6_verdict(reporter, impulse, superposition, matched, sham, sensitivity):
    endpoint_key = "20" if "20" in matched["results"] else "16"
    primary = matched["results"][endpoint_key]["energy_distance_test"]
    sensitivity_ok = sensitivity["sensitivity_adequate_for_target"]

    if primary["p_value"] < 0.05:
        arrangement_status = "PROVISIONAL"
        arrangement_statement = (
            "At the declared matched-endpoint observation, interior temporal "
            "arrangement produced a measurable population-level morphology "
            "distribution difference under the declared test."
        )
    elif not sensitivity_ok:
        arrangement_status = "UNTESTED"
        arrangement_statement = (
            "The matched-endpoint test did not establish a systematic arrangement "
            "signature, but the declared spike-in calibration showed insufficient "
            "sensitivity at the predeclared target effect. The underlying "
            "arrangement claim therefore remains unresolved under this protocol."
        )
    else:
        arrangement_status = "FAILED"
        arrangement_statement = (
            "With the declared sensitivity target met, this protocol did not "
            "establish a systematic receiver-state distribution difference "
            "attributable to interior temporal arrangement."
        )

    # Descriptive pulse divergence endpoint.
    pulse_step = str(max(map(int, impulse["exact_causal_fork"].keys())))
    pulse_symdiff = impulse["exact_causal_fork"][pulse_step]["symdiff"]["mean"]
    stoch_symdiff = (
        impulse["independent_no_pulse_stochastic_baseline"][pulse_step]
        ["symdiff"]["mean"]
    )

    result = {
        "experiment_role": "EXPLORATORY / MECHANISM CHARACTERIZATION",
        "single_pulse_response": "MEASURED",
        "single_pulse_latest_observation": int(pulse_step),
        "single_pulse_causal_symdiff_mean": pulse_symdiff,
        "independent_stochastic_symdiff_mean": stoch_symdiff,
        "ensemble_superposition": "MEASURED",
        "matched_endpoint_arrangement_status": arrangement_status,
        "matched_endpoint_primary_endpoint": int(endpoint_key),
        "matched_endpoint_p_value": primary["p_value"],
        "pipeline_sham_false_positive_rate": sham["false_positive_rate"],
        "pipeline_sensitivity_adequate": sensitivity_ok,
        "bounded_statement": arrangement_statement,
        "nonclaims": [
            "information storage",
            "memory",
            "signalling",
            "semantics",
            "sender identity",
            "coordination",
            "learning",
            "agency",
            "individuality",
            "life",
            "Shannon channel capacity",
        ],
        "next_decision_logic": {
            "if_sensitivity_inadequate": (
                "Do not interpret a negative matched-arrangement result as absence. "
                "Increase groups or improve the primary measurement only after "
                "using the calibration curve to justify the change."
            ),
            "if_matched_effect_absent_with_adequate_sensitivity": (
                "Treat matched interior timing as unsupported under this protocol "
                "and retain the earlier L3 result as compatible with recency or "
                "other ordinary response dynamics."
            ),
            "if_matched_effect_present": (
                "Freeze the matched condition and design a separate Chapter 18 "
                "confirmatory recoverability experiment."
            ),
            "if_superposition_residual_large": (
                "Investigate the mechanism of ensemble non-additivity before "
                "describing the result with information-processing language."
            ),
        },
    }

    reporter.json("stage-06-verdict.json", result)
    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Bounded Experimental Verdict",
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
        default=Path("research/digital-life/ch17-perturbation-dynamics-v2"),
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

    metadata = {
        "model_version": MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": 17,
        "chapter_title": "How Does the Crystal Respond to Perturbation?",
        "version_2_focus": (
            "Causal divergence vs stochastic spread, ensemble-mean superposition, "
            "matched-endpoint timing, and calibrated measurement sensitivity."
        ),
        "run_type": "EXPLORATORY",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "matched_codeword_A": "".join(map(str, MATCHED_CODEWORD_A)),
        "matched_codeword_B": "".join(map(str, MATCHED_CODEWORD_B)),
        "scientific_boundary": (
            "Perturbation-response characterization only. The old information-"
            "survival question is deferred to Chapter 18."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 17 — HOW DOES THE CRYSTAL RESPOND TO PERTURBATION?")
    print(f"profile={args.profile} version={EXPERIMENT_VERSION}")
    print("=" * 78)

    s0 = stage_0_reproducibility(
        reporter, profile, params, args.seed
    )
    s1 = stage_1_impulse_response(
        reporter, profile, params, args.seed, args.image_dir
    )
    s2 = stage_2_superposition(
        reporter, profile, params, args.seed, args.image_dir
    )
    s3, matched_features = stage_3_matched_arrangement(
        reporter, profile, params, args.seed, args.image_dir
    )
    s4 = stage_4_sham_controls(
        reporter, profile, params, args.seed
    )
    s5 = stage_5_spike_in(
        reporter, profile, matched_features, args.seed
    )
    s6 = stage_6_verdict(
        reporter, s1, s2, s3, s4, s5
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "reproducibility_passed": s0["exact"],
        "final_status": s6["matched_endpoint_arrangement_status"],
        "primary_matched_endpoint": s6["matched_endpoint_primary_endpoint"],
    })
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("EXPERIMENT COMPLETE")
    print(f"Matched-endpoint status: {s6['matched_endpoint_arrangement_status']}")
    print(s6["bounded_statement"])
    print(f"Report: {report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
