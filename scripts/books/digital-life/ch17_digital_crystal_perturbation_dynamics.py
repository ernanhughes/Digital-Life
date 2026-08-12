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
EXPERIMENT_VERSION = "digital-crystal-perturbation-dynamics-v1"
SCHEMA_VERSION = 1

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
        path = self.root / "ch17-perturbation-dynamics-full-report.md"
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
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    pulse_idx = profile["pulse_step"]
    observations = sorted(set(profile["observation_steps"] + [pulse_idx + 1]))

    response_by_step = {
        t: {
            "population_delta": [],
            "absolute_population_delta": [],
            "symdiff": [],
            "feature_distance": [],
            "attachment_delta": [],
        }
        for t in observations
    }
    feature_delta_vectors = {t: [] for t in observations}
    max_capacity = 0.0

    baseline_bits = pulse_train(horizon, [])
    pulse_bits = pulse_train(horizon, [pulse_idx])

    for group in tqdm(range(groups), desc="Stage 1 impulse"):
        gseed = seed + 10_000 + group * 1009
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(
            env, warmup, gseed + 2, radius, params
        )
        future = env[warmup:]

        base = advance_with_pulses(
            checkpoint, future, baseline_bits,
            profile["message_gain"], radius, params,
            observations, profile["max_capacity_fraction"],
        )
        pulse = advance_with_pulses(
            checkpoint, future, pulse_bits,
            profile["message_gain"], radius, params,
            observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            b = base[t]
            p = pulse[t]
            diff = state_difference(p, b, radius)
            response_by_step[t]["population_delta"].append(
                diff["population_difference"]
            )
            response_by_step[t]["absolute_population_delta"].append(
                diff["absolute_population_difference"]
            )
            response_by_step[t]["symdiff"].append(
                diff["normalized_symmetric_difference"]
            )
            response_by_step[t]["feature_distance"].append(
                diff["feature_distance"]
            )

            # attachments_by_step includes the initial seed entry.
            response_by_step[t]["attachment_delta"].append(
                p.attachments_by_step[-1] - b.attachments_by_step[-1]
            )
            feature_delta_vectors[t].append(
                morphology_features(p, radius) - morphology_features(b, radius)
            )
            max_capacity = max(
                max_capacity,
                capacity_fraction(b, radius),
                capacity_fraction(p, radius),
            )

    summary = {}
    for t in observations:
        summary[str(t)] = {
            metric: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 100_000 + t * 31 + i,
            )
            for i, (metric, vals) in enumerate(response_by_step[t].items())
        }

    result = {
        "pulse_zero_index": pulse_idx,
        "pulse_elapsed_step": pulse_idx + 1,
        "message_gain": profile["message_gain"],
        "groups": groups,
        "observation_steps": observations,
        "max_capacity_fraction_observed": max_capacity,
        "summary": summary,
    }

    reporter.json("stage-01-impulse-response.json", result)
    reporter.stage(
        "stage-01-impulse-response.md",
        "Stage 1 — Measure One Pulse Before Calling Anything a Channel",
        f"""A single isolated pulse is compared against an exact matched baseline:
same checkpoint, same RNG state, same future environment, pulse bit only changed.

```json
{json.dumps(result, indent=2)}
```""",
    )

    # Figure 1: symmetric-difference response.
    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    ys = [summary[str(t)]["symdiff"]["mean"] for t in xs]
    lo = [summary[str(t)]["symdiff"]["ci95_low"] for t in xs]
    hi = [summary[str(t)]["symdiff"]["ci95_high"] for t in xs]
    ax.plot(xs, ys, marker="o")
    ax.fill_between(xs, lo, hi, alpha=0.2)
    ax.axvline(pulse_idx + 1, linestyle="--", linewidth=1)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Normalized morphology symmetric difference")
    ax.set_title("Single-pulse causal response and decay")
    fig.tight_layout()
    path = image_dir / "ch17-01-impulse-response.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)

    return result, feature_delta_vectors


# ---------------------------------------------------------------------------
# Stage 2 — superposition test
# ---------------------------------------------------------------------------

def stage_2_superposition(reporter, profile, params, seed, image_dir):
    """
    Test whether a multi-pulse response in morphology-feature space is
    approximated by the sum of matched single-pulse responses.

    For each receiver group we use the same checkpoint/environment and run:
      baseline
      one branch for each single pulse position
      full clustered train
      full dispersed train

    At each observation:
      predicted_delta(train) = sum(single_pulse_delta_i)
      actual_delta(train)    = feature(train) - feature(baseline)
      residual               = ||actual - predicted||

    This is not a theorem-level linearity test of the full microscopic state.
    It is an operational superposition test in the declared measurement space.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["horizon"]
    observations = profile["matched_observation_steps"]

    clustered_positions = [0, 1, 2, 15]
    dispersed_positions = [0, 7, 8, 15]
    all_positions = sorted(set(clustered_positions + dispersed_positions))

    baseline_bits = pulse_train(horizon, [])
    singles = {p: pulse_train(horizon, [p]) for p in all_positions}
    clustered_bits = pulse_train(horizon, clustered_positions)
    dispersed_bits = pulse_train(horizon, dispersed_positions)

    rows = {t: {"clustered": [], "dispersed": []} for t in observations}
    actual_norms = {t: {"clustered": [], "dispersed": []} for t in observations}

    for group in tqdm(range(groups), desc="Stage 2 superposition"):
        gseed = seed + 20_000 + group * 1013
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(
            env, warmup, gseed + 2, radius, params
        )
        future = env[warmup:]

        base = advance_with_pulses(
            checkpoint, future, baseline_bits,
            profile["message_gain"], radius, params,
            observations, profile["max_capacity_fraction"],
        )

        single_obs = {}
        for pos, bits_ in singles.items():
            single_obs[pos] = advance_with_pulses(
                checkpoint, future, bits_,
                profile["message_gain"], radius, params,
                observations, profile["max_capacity_fraction"],
            )

        multi = {
            "clustered": advance_with_pulses(
                checkpoint, future, clustered_bits,
                profile["message_gain"], radius, params,
                observations, profile["max_capacity_fraction"],
            ),
            "dispersed": advance_with_pulses(
                checkpoint, future, dispersed_bits,
                profile["message_gain"], radius, params,
                observations, profile["max_capacity_fraction"],
            ),
        }

        for t in observations:
            f0 = morphology_features(base[t], radius)
            for name, positions in (
                ("clustered", clustered_positions),
                ("dispersed", dispersed_positions),
            ):
                predicted = np.zeros_like(f0)
                for pos in positions:
                    predicted += morphology_features(
                        single_obs[pos][t], radius
                    ) - f0

                actual = morphology_features(multi[name][t], radius) - f0
                residual = float(np.linalg.norm(actual - predicted))
                actual_norm = float(np.linalg.norm(actual))
                relative = residual / max(1e-12, actual_norm)

                rows[t][name].append(relative)
                actual_norms[t][name].append(actual_norm)

    summary = {}
    for t in observations:
        summary[str(t)] = {}
        for name in ("clustered", "dispersed"):
            summary[str(t)][name] = {
                "relative_superposition_error": bootstrap_mean_ci(
                    rows[t][name],
                    profile["bootstrap_reps"],
                    seed + 200_000 + t * 13 + (0 if name == "clustered" else 1),
                ),
                "actual_feature_delta_norm": bootstrap_mean_ci(
                    actual_norms[t][name],
                    profile["bootstrap_reps"],
                    seed + 210_000 + t * 13 + (0 if name == "clustered" else 1),
                ),
            }

    result = {
        "measurement_space": "24 normalized morphology features",
        "clustered_positions_zero_indexed": clustered_positions,
        "dispersed_positions_zero_indexed": dispersed_positions,
        "same_onset": True,
        "same_offset": True,
        "same_pulse_count": True,
        "interpretation": (
            "Relative superposition error near zero means additive single-pulse "
            "responses explain the measured multi-pulse feature response. Large "
            "residuals indicate non-additivity in this measurement space; they do "
            "not by themselves establish memory or information storage."
        ),
        "summary": summary,
    }
    reporter.json("stage-02-superposition.json", result)
    reporter.stage(
        "stage-02-superposition.md",
        "Stage 2 — Does One-Pulse Physics Explain the Pulse Train?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    xs = observations
    for name in ("clustered", "dispersed"):
        ys = [
            summary[str(t)][name]["relative_superposition_error"]["mean"]
            for t in xs
        ]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_xlabel("Elapsed step")
    ax.set_ylabel("Relative superposition error")
    ax.set_title("Measured multi-pulse response vs additive single-pulse prediction")
    ax.legend()
    fig.tight_layout()
    path = image_dir / "ch17-02-superposition-error.png"
    fig.savefig(path, dpi=160)
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
        t: {"symdiff": [], "feature_distance": [], "abs_population_difference": []}
        for t in observations
    }

    for group in tqdm(range(groups), desc="Stage 3 matched arrangement"):
        gseed = seed + 30_000 + group * 1019
        env = make_environment(warmup + horizon, gseed + 1)
        checkpoint = warm_checkpoint(
            env, warmup, gseed + 2, radius, params
        )
        future = env[warmup:]

        obs_a = advance_with_pulses(
            checkpoint, future, bits_a,
            profile["message_gain"], radius, params,
            observations, profile["max_capacity_fraction"],
        )
        obs_b = advance_with_pulses(
            checkpoint, future, bits_b,
            profile["message_gain"], radius, params,
            observations, profile["max_capacity_fraction"],
        )

        for t in observations:
            features[t]["A"].append(morphology_features(obs_a[t], radius))
            features[t]["B"].append(morphology_features(obs_b[t], radius))
            d = state_difference(obs_a[t], obs_b[t], radius)
            paired_diff[t]["symdiff"].append(
                d["normalized_symmetric_difference"]
            )
            paired_diff[t]["feature_distance"].append(
                d["feature_distance"]
            )
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
        "same_pulse_count": sum(MATCHED_CODEWORD_A) == sum(MATCHED_CODEWORD_B),
        "same_first_pulse": True,
        "same_last_pulse": True,
        "groups": groups,
        "primary_measurement": (
            "decoder-free multivariate energy distance on normalized morphology "
            "features with paired within-group swap permutation"
        ),
        "secondary_measurements": (
            "paired morphology symmetric difference, feature distance, "
            "absolute population difference"
        ),
        "results": results,
    }
    reporter.json("stage-03-matched-arrangement.json", result)
    reporter.stage(
        "stage-03-matched-arrangement.md",
        "Stage 3 — Match Count, Onset and Offset; Change Only Interior Timing",
        f"""This stage directly removes the recency-of-last-pulse confound.

```json
{json.dumps(result, indent=2)}
```""",
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
    ax.set_title("Matched-endpoint interior timing effect")
    fig.tight_layout()
    path = image_dir / "ch17-03-matched-arrangement.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)

    return result, features


# ---------------------------------------------------------------------------
# Stage 4 — sham controls on the analysis pipeline
# ---------------------------------------------------------------------------

def stage_4_sham_controls(reporter, profile, params, seed):
    """
    Known-null control.

    Generate one state per independent receiver group under the SAME pulse train.
    Randomly partition those states into two labels and run the same energy-
    distance permutation test. Repeat this as sealed-like pseudoexperiments.

    This tests whether the analysis machinery produces suspiciously frequent
    positives when there is no treatment distinction.
    """
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
        checkpoint = warm_checkpoint(
            env, warmup, gseed + 2, radius, params
        )
        future = env[warmup:]
        obs = advance_with_pulses(
            checkpoint, future, same_bits,
            profile["message_gain"], radius, params,
            [endpoint], profile["max_capacity_fraction"],
        )
        Xall.append(morphology_features(obs[endpoint], radius))

    Xall = np.asarray(Xall, dtype=float)
    rng = np.random.default_rng(seed + 400_000)
    p_values = []
    stats = []

    for rep in range(profile["sham_reps"]):
        order = rng.permutation(len(Xall))
        half = len(order) // 2
        A = Xall[order[:half]]
        B = Xall[order[half:2 * half]]

        # Ordinary label permutation is appropriate here because these sham
        # samples are independent groups rather than matched treatment forks.
        observed = energy_distance_statistic(A, B)
        null = []
        pooled = np.vstack([A, B])
        n = len(A)
        for _ in range(profile["permutations"]):
            perm = rng.permutation(len(pooled))
            Ap = pooled[perm[:n]]
            Bp = pooled[perm[n:2*n]]
            null.append(energy_distance_statistic(Ap, Bp))
        null = np.asarray(null)
        p = (1 + np.sum(null >= observed)) / (len(null) + 1)
        p_values.append(float(p))
        stats.append(float(observed))

    alpha = 0.05
    result = {
        "known_null": True,
        "endpoint": endpoint,
        "same_codeword_both_pseudoarms": "".join(map(str, MATCHED_CODEWORD_A)),
        "sham_reps": profile["sham_reps"],
        "alpha": alpha,
        "false_positive_count": int(np.sum(np.asarray(p_values) < alpha)),
        "false_positive_rate": float(np.mean(np.asarray(p_values) < alpha)),
        "p_value_summary": bootstrap_mean_ci(
            p_values,
            profile["bootstrap_reps"],
            seed + 410_000,
        ),
        "minimum_p_value": float(np.min(p_values)),
        "maximum_energy_statistic": float(np.max(stats)),
    }
    reporter.json("stage-04-sham-controls.json", result)
    reporter.stage(
        "stage-04-sham-controls.md",
        "Stage 4 — Does the Measuring Apparatus Invent Effects?",
        f"""Known-null sham pseudoexperiments use the same treatment in both arms.

```json
{json.dumps(result, indent=2)}
```""",
    )
    return result


# ---------------------------------------------------------------------------
# Stage 5 — spike-in sensitivity
# ---------------------------------------------------------------------------

def stage_5_spike_in(reporter, profile, matched_features, seed):
    """
    Known-effect calibration of the two-sample measurement pipeline.

    Start from the Stage 3 A-feature vectors at endpoint 20 (or 16) and add a
    controlled shift along one standardized feature dimension to a copied arm.
    This is explicitly a pipeline calibration, not a Digital Crystal result.
    """
    endpoint = 20 if 20 in matched_features else 16
    X = np.asarray(matched_features[endpoint]["A"], dtype=float)
    rng = np.random.default_rng(seed + 500_000)

    pooled_sd = np.std(X, axis=0)
    candidate_dims = np.flatnonzero(pooled_sd > 1e-9)
    if len(candidate_dims) == 0:
        raise RuntimeError("No varying feature available for spike-in control.")

    # Choose the most variable feature deterministically.
    dim = int(candidate_dims[np.argmax(pooled_sd[candidate_dims])])
    sd = float(pooled_sd[dim])

    strengths = [0.0, 0.25, 0.5, 1.0]
    result_rows = []

    for strength in strengths:
        detections = 0
        pvals = []
        for rep in range(profile["spike_in_reps"]):
            # Bootstrap independent pseudo-samples from the same empirical base.
            idx_a = rng.integers(0, len(X), size=len(X))
            idx_b = rng.integers(0, len(X), size=len(X))
            A = X[idx_a].copy()
            B = X[idx_b].copy()
            B[:, dim] += strength * sd

            # Unpaired permutation for calibration pseudo-samples.
            obs = energy_distance_statistic(A, B)
            pooled = np.vstack([A, B])
            n = len(A)
            null = []
            # Fewer permutations inside repeated calibration to keep runtime sane.
            inner_perms = max(50, min(200, profile["permutations"]))
            for _ in range(inner_perms):
                perm = rng.permutation(len(pooled))
                Ap = pooled[perm[:n]]
                Bp = pooled[perm[n:2*n]]
                null.append(energy_distance_statistic(Ap, Bp))
            null = np.asarray(null)
            p = (1 + np.sum(null >= obs)) / (len(null) + 1)
            pvals.append(float(p))
            detections += int(p < 0.05)

        result_rows.append({
            "shift_sd_units": strength,
            "detection_rate_alpha_0_05": detections / profile["spike_in_reps"],
            "p_value_mean": float(np.mean(pvals)),
            "p_value_median": float(np.median(pvals)),
        })

    result = {
        "known_effect_calibration": True,
        "endpoint": endpoint,
        "feature_index": dim,
        "feature_name": FEATURE_NAMES[dim],
        "empirical_feature_sd": sd,
        "spike_in_reps": profile["spike_in_reps"],
        "results": result_rows,
        "interpretation": (
            "This does not test the crystal. It measures whether the declared "
            "two-sample pipeline can recover synthetic effects of known size."
        ),
    }
    reporter.json("stage-05-spike-in.json", result)
    reporter.stage(
        "stage-05-spike-in.md",
        "Stage 5 — Can the Measuring Apparatus Recover a Known Effect?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


# ---------------------------------------------------------------------------
# Stage 6 — bounded verdict
# ---------------------------------------------------------------------------

def stage_6_verdict(reporter, impulse, superposition, matched, sham):
    endpoint_key = "20" if "20" in matched["results"] else "16"
    matched_primary = matched["results"][endpoint_key]["energy_distance_test"]
    sham_rate = sham["false_positive_rate"]

    # This is deliberately descriptive. v1 is an exploratory characterization
    # experiment, not a confirmatory claim test.
    if matched_primary["p_value"] < 0.05:
        arrangement = "PROVISIONAL"
        arrangement_text = (
            "At the declared matched-endpoint observation, interior temporal "
            "arrangement produced a measurable receiver-state distribution "
            "difference under the decoder-free energy-distance test."
        )
    else:
        arrangement = "FAILED"
        arrangement_text = (
            "At the declared matched-endpoint observation, this protocol did "
            "not establish a receiver-state distribution difference attributable "
            "to interior temporal arrangement."
        )

    result = {
        "experiment_role": "EXPLORATORY / MECHANISM CHARACTERIZATION",
        "single_pulse_response": "MEASURED",
        "superposition_characterized": "MEASURED",
        "matched_endpoint_arrangement_status": arrangement,
        "matched_endpoint_primary_endpoint": int(endpoint_key),
        "matched_endpoint_p_value": matched_primary["p_value"],
        "sham_false_positive_rate": sham_rate,
        "bounded_statement": arrangement_text,
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
            "if_matched_endpoint_effect_absent": (
                "Treat the old Chapter 17 L3 candidate as consistent with recency/"
                "ordinary response dynamics and push the information-survival "
                "interpretation back."
            ),
            "if_effect_present_but_superposition_error_small": (
                "Interpret the difference primarily through ordinary additive "
                "response dynamics; do not promote an information-retention claim."
            ),
            "if_effect_present_and_superposition_error_material": (
                "Freeze the matched-endpoint condition and design a separate "
                "Chapter 18 confirmatory information-survival experiment."
            ),
            "if_sham_false_positive_rate_suspicious": (
                "Do not trust the scientific endpoint until the analysis pipeline "
                "is repaired and the sham calibration is repeated."
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
        default=Path("research/digital-life/ch17-perturbation-dynamics"),
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
    s1, _ = stage_1_impulse_response(
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
        reporter, s1, s2, s3, s4
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
