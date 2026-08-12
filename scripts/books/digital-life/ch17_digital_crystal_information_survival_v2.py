#!/usr/bin/env python3
"""
Digital Life — Chapter 17
What Survives the Channel?
==========================

Experiment version: digital-crystal-information-survival-v1.2

Question
--------
Can distinct constant-weight temporal codewords be recovered from a Digital
Crystal receiver after transmission has ended?

This experiment follows Chapter 16. Chapter 16 established primitive causal
transmission but did NOT establish sender-specific signalling. Here we remove
sender identity entirely and ask a smaller information question:

    different temporal input
        ↓
    same receiver checkpoint
        ↓
    same RNG state
        ↓
    same external forcing
        ↓
    Digital Crystal evolves
        ↓
    can a held-out decoder identify which codeword was sent?

Scientific boundary
-------------------
This does NOT establish:
    language
    semantics
    meaning
    understanding
    sender identity
    coordination
    learning
    agency
    individuality
    selfhood
    life
    Shannon channel capacity

The strongest possible claim is deliberately narrow:

    RECOVERABLE_CODEWORD_INFORMATION_SUPPORTED

meaning that, under this protocol, codeword identity remains decodable from
receiver-only measurements after transmission has ended.

Design
------
Stage 0  Freeze Digital Crystal v1 and verify reproducibility.
Stage 1  Construct nested 2/4/8-word constant-weight temporal codebooks.
Stage 2  Fork matched receiver checkpoints and collect receiver-only outcomes.
Stage 3  Decode 1/2/3 encoded bits with held-out GROUPED cross-validation.
Stage 4  Attack the decoder with group-wise label permutation and no-channel nulls.
Stage 5  Measure retention after transmission ends.
Stage 6  Ask where recoverable information lives: morphology, recent growth, combined.
Stage 7  Emit a bounded verdict and evidence ledger.

Key controls
------------
* Every codeword has the same length and the same number of 1 bits.
* Every codeword has the same first and last bit.
* Every codeword in one experimental group starts from the SAME checkpoint,
  RNG state, and future environmental forcing.
* Train/test folds are split by receiver group. No checkpoint appears in both.
* Decoder sees receiver measurements only, never the transmitted codeword.
* A no-channel control duplicates the same receiver outcome across labels.
* Label-permutation nulls preserve the grouped experimental structure.
* Hard-radius saturation is a kill condition, not something to average through.

Recommended
-----------
    python ch17_digital_crystal_information_survival.py --profile quick
    python ch17_digital_crystal_information_survival.py --profile standard
    python ch17_digital_crystal_information_survival.py --profile full
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np

# Headless plotting is mandatory for the experiment runner. On Windows the
# default TkAgg backend can create Tk objects that are later finalized from a
# scikit-learn worker thread, causing:
#   RuntimeError: main thread is not in main loop
#   Tcl_AsyncDelete: async handler deleted by the wrong thread
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt

from tqdm import tqdm

try:
    from sklearn.base import clone
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import GroupKFold, cross_val_predict
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
except ImportError as exc:
    raise SystemExit(
        "Chapter 17 requires scikit-learn. Install it with: pip install scikit-learn"
    ) from exc


MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "digital-crystal-information-survival-v1.2"
SCHEMA_VERSION = 1

Cell = Tuple[int, int]
HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)

PROFILES = {
    "quick": {
        "groups": 24,
        "radius": 64,
        "warmup_steps": 14,
        "codeword_length": 16,
        "codeword_weight": 6,
        "retention_lags": [0, 4, 8, 16, 24],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 4,
        "null_permutations": 100,
        "rf_trees": 160,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 40,
        "radius": 48,
        "warmup_steps": 16,
        "codeword_length": 16,
        "codeword_weight": 6,
        "retention_lags": [0, 4, 8, 16, 32],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 5,
        "null_permutations": 200,
        "rf_trees": 240,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 60,
        "radius": 80,
        "warmup_steps": 18,
        "codeword_length": 16,
        "codeword_weight": 6,
        "retention_lags": [0, 4, 8, 16, 32],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 5,
        "null_permutations": 500,
        "rf_trees": 320,
        "max_capacity_fraction": 0.85,
    },
}


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
# Progressive information ladder
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LadderLevel:
    level: str
    title: str
    codewords: Tuple[Tuple[int, ...], ...]
    interpretation: str


def bits(s: str) -> Tuple[int, ...]:
    return tuple(int(ch) for ch in s.strip())


def build_information_ladder(length: int = 16) -> List[LadderLevel]:
    if length != 16:
        raise ValueError("Chapter 17 v2 currently uses a frozen 16-step transmission window.")

    # The ladder deliberately begins with extremely coarse timing distinctions
    # and only then climbs toward the hard constant-weight codebook from v1.
    #
    # Within every level all codewords have identical length and identical pulse count.
    return [
        LadderLevel(
            "L1",
            "One pulse: early vs late",
            (
                bits("0010000000000000"),
                bits("0000000000000100"),
            ),
            "Same pulse count and energy; only coarse pulse timing differs.",
        ),
        LadderLevel(
            "L2",
            "Two-pulse burst: early vs late",
            (
                bits("0011000000000000"),
                bits("0000000000001100"),
            ),
            "Same two adjacent pulses; only burst location differs.",
        ),
        LadderLevel(
            "L3",
            "Four pulses: clustered vs dispersed",
            (
                bits("0011110000000000"),
                bits("0010010010010000"),
            ),
            "Same four pulses; temporal concentration differs strongly.",
        ),
        LadderLevel(
            "L4",
            "Two hard constant-weight temporal words",
            (
                bits("1000000010001111"),
                bits("1111100000000001"),
            ),
            "Same length, weight, first bit and last bit; finer chronology differs.",
        ),
        LadderLevel(
            "L5",
            "Four hard constant-weight temporal words",
            (
                bits("1000000010001111"),
                bits("1111100000000001"),
                bits("1000011101000001"),
                bits("1100010000110001"),
            ),
            "Two encoded bits in a constant-weight temporal codebook.",
        ),
        LadderLevel(
            "L6",
            "Eight hard constant-weight temporal words",
            (
                bits("1000000010001111"),
                bits("1111100000000001"),
                bits("1000011101000001"),
                bits("1100010000110001"),
                bits("1010001010100001"),
                bits("1001000100011001"),
                bits("1000100001100101"),
                bits("1010000001010011"),
            ),
            "Three encoded bits in the hard constant-weight codebook from v1.",
        ),
    ]


def ladder_diagnostics(levels: Sequence[LadderLevel]) -> dict:
    rows = []
    for level in levels:
        arr = [np.asarray(c, dtype=np.int8) for c in level.codewords]
        weights = [int(np.sum(c)) for c in arr]
        dists = []
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                dists.append(int(np.sum(arr[i] != arr[j])))
        rows.append({
            "level": level.level,
            "title": level.title,
            "n_codewords": len(arr),
            "encoded_bits": float(math.log2(len(arr))),
            "length": len(arr[0]),
            "weight_each": weights,
            "equal_weight_within_level": len(set(weights)) == 1,
            "pairwise_hamming_min": min(dists) if dists else 0,
            "pairwise_hamming_mean": float(np.mean(dists)) if dists else 0.0,
            "pairwise_hamming_max": max(dists) if dists else 0,
            "codewords": ["".join(str(int(v)) for v in c) for c in arr],
            "interpretation": level.interpretation,
        })
    return {"levels": rows}


# ---------------------------------------------------------------------------
# Receiver-only measurements
# ---------------------------------------------------------------------------

MORPH_FEATURE_NAMES = [
    "population_fraction",
    "max_hex_radius_fraction",
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
    h6 = np.exp(1j * 6.0 * angles)
    harmonic6 = np.mean(h6)

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


def recent_growth_features(
    attachments: Sequence[int],
    populations: Sequence[int],
    window: int,
) -> np.ndarray:
    att = np.asarray(attachments[-window:], dtype=float)
    pop = np.asarray(populations[-window:], dtype=float)

    if len(att) < window:
        att = np.pad(att, (window - len(att), 0))
    if len(pop) < window:
        pop = np.pad(pop, (window - len(pop), 0), mode="edge")

    # Use a fixed normalization rather than dividing by the maximum inside each
    # sample. Per-sample max normalization can erase amplitude distinctions that
    # are legitimately present in receiver growth.
    att_scale = 128.0
    pop_scale = max(1.0, float(pop[-1]))

    return np.concatenate([
        att / att_scale,
        np.diff(np.r_[pop[0], pop]) / att_scale,
        np.asarray([
            float(np.mean(att)) / att_scale,
            float(np.std(att)) / att_scale,
            float(att[-1]) / att_scale,
            float(pop[-1] - pop[0]) / pop_scale,
        ]),
    ])


def combined_features(
    state: CrystalState,
    radius: int,
    recent_window: int,
) -> Dict[str, np.ndarray]:
    morph = morphology_features(state, radius)
    growth = recent_growth_features(
        state.attachments_by_step,
        state.population_by_step,
        recent_window,
    )
    return {
        "morphology": morph,
        "recent_growth": growth,
        "combined": np.concatenate([morph, growth]),
    }


# ---------------------------------------------------------------------------
# Matched branch execution with DURING + AFTER observations
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


def run_temporal_branch(
    checkpoint: CrystalState,
    env_future: np.ndarray,
    codeword: np.ndarray,
    message_gain: float,
    radius: int,
    params: CrystalParams,
    observation_steps: Sequence[int],
    recent_window: int,
    saturation_guard: float,
) -> Dict[int, Dict[str, np.ndarray]]:
    """
    observation_steps are 1-indexed elapsed steps from transmission start.

    For a 16-step codeword:
      step 4, 8, 12, 16 = during / end of transmission
      step 20 = +4 after
      step 24 = +8 after
      ...
    """
    state = clone_state(checkpoint)
    L = len(codeword)
    max_obs = max(observation_steps)
    if len(env_future) < max_obs:
        raise ValueError("env_future is too short for requested observation schedule.")

    observations: Dict[int, Dict[str, np.ndarray]] = {}
    for t in range(max_obs):
        bit = int(codeword[t]) if t < L else 0
        forcing = float(env_future[t]) + message_gain * bit
        state, _ = advance_one_step(state, forcing, radius, params)

        frac = capacity_fraction(state, radius)
        if frac >= saturation_guard:
            raise RuntimeError(
                "Chapter 17 v2 branch reached hard-radius saturation guard: "
                f"elapsed_step={t+1}, fraction={frac:.3f}, "
                f"guard={saturation_guard:.3f}. Increase canvas radius."
            )

        elapsed = t + 1
        if elapsed in observation_steps:
            feat = combined_features(state, radius, recent_window)
            feat["capacity_fraction"] = np.asarray([frac], dtype=float)
            observations[elapsed] = feat

    missing = sorted(set(observation_steps) - set(observations))
    if missing:
        raise RuntimeError(f"Missing observations: {missing}")
    return observations


def observation_schedule(codeword_length: int, after_lags: Sequence[int]) -> List[int]:
    during = sorted(set([
        max(1, codeword_length // 4),
        max(1, codeword_length // 2),
        max(1, (3 * codeword_length) // 4),
        codeword_length,
    ]))
    after = [codeword_length + int(lag) for lag in after_lags if lag > 0]
    return sorted(set(during + after))


def collect_level_dataset(
    level: LadderLevel,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> Tuple[List[dict], Dict[int, Dict[int, Dict[str, np.ndarray]]], dict]:
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    L = profile["codeword_length"]
    obs_steps = observation_schedule(L, profile["retention_lags"])
    max_obs = max(obs_steps)
    guard = profile["max_capacity_fraction"]

    rows: List[dict] = []
    baselines: Dict[int, Dict[int, Dict[str, np.ndarray]]] = {}
    max_capacity = 0.0

    codewords = [np.asarray(c, dtype=np.int8) for c in level.codewords]

    for group in tqdm(range(groups), desc=f"{level.level} receiver groups", leave=False):
        group_seed = (
            seed
            + 100_000 * (1 + int(level.level[1:]))
            + group * 1009
        )
        env = make_environment(warmup + max_obs, group_seed + 1)
        checkpoint = warm_checkpoint(
            env,
            warmup,
            group_seed + 2,
            radius,
            params,
        )
        future = env[warmup:]

        baseline = run_temporal_branch(
            checkpoint,
            future,
            np.zeros(L, dtype=np.int8),
            profile["message_gain"],
            radius,
            params,
            obs_steps,
            profile["recent_growth_window"],
            guard,
        )
        baselines[group] = baseline

        for label, codeword in enumerate(codewords):
            obs = run_temporal_branch(
                checkpoint,
                future,
                codeword,
                profile["message_gain"],
                radius,
                params,
                obs_steps,
                profile["recent_growth_window"],
                guard,
            )
            for elapsed in obs_steps:
                phase = (
                    "during"
                    if elapsed < L
                    else ("end" if elapsed == L else "after")
                )
                after_lag = max(0, elapsed - L)
                frac = float(obs[elapsed]["capacity_fraction"][0])
                max_capacity = max(max_capacity, frac)

                row = {
                    "level": level.level,
                    "level_title": level.title,
                    "group": group,
                    "label": label,
                    "elapsed_step": elapsed,
                    "phase": phase,
                    "after_lag": after_lag,
                    "codeword": "".join(str(int(v)) for v in codeword),
                    "capacity_fraction": frac,
                }
                for feature_set in ("morphology", "recent_growth", "combined"):
                    raw = obs[elapsed][feature_set]
                    base = baseline[elapsed][feature_set]
                    row[feature_set] = raw
                    row[f"delta_{feature_set}"] = raw - base
                rows.append(row)

    return rows, baselines, {
        "level": level.level,
        "title": level.title,
        "groups": groups,
        "n_codewords": len(codewords),
        "observation_steps": obs_steps,
        "max_capacity_fraction_observed": max_capacity,
        "saturation_guard": guard,
    }


# ---------------------------------------------------------------------------
# Decoding
# ---------------------------------------------------------------------------

def primary_decoder() -> Pipeline:
    return Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(
            max_iter=3000,
            solver="lbfgs",
            C=1.0,
        )),
    ])


def secondary_decoder(trees: int, seed: int) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=trees,
        random_state=seed,
        min_samples_leaf=2,
        n_jobs=1,
    )


def decoder_mutual_information_bits(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    labels = np.unique(np.concatenate([y_true, y_pred]))
    cm = confusion_matrix(y_true, y_pred, labels=labels).astype(float)
    pxy = cm / max(1.0, np.sum(cm))
    px = np.sum(pxy, axis=1, keepdims=True)
    py = np.sum(pxy, axis=0, keepdims=True)
    mi = 0.0
    for i in range(pxy.shape[0]):
        for j in range(pxy.shape[1]):
            p = pxy[i, j]
            if p > 0 and px[i, 0] > 0 and py[0, j] > 0:
                mi += p * math.log2(p / (px[i, 0] * py[0, j]))
    return float(mi)


def level_matrix(
    rows: List[dict],
    elapsed_step: int,
    feature_set: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    selected = [r for r in rows if r["elapsed_step"] == elapsed_step]
    X = np.asarray([r[feature_set] for r in selected], dtype=float)
    y = np.asarray([r["label"] for r in selected], dtype=int)
    groups = np.asarray([r["group"] for r in selected], dtype=int)
    return X, y, groups


def grouped_predictions(model, X, y, groups, splits):
    cv = GroupKFold(n_splits=min(splits, len(np.unique(groups))))
    return cross_val_predict(
        clone(model),
        X,
        y,
        groups=groups,
        cv=cv,
        method="predict",
    )


def decode_level(
    rows: List[dict],
    level: LadderLevel,
    elapsed_step: int,
    feature_set: str,
    profile: dict,
    seed: int,
) -> dict:
    X, y, groups = level_matrix(rows, elapsed_step, feature_set)
    p1 = grouped_predictions(
        primary_decoder(), X, y, groups, profile["cv_splits"]
    )
    p2 = grouped_predictions(
        secondary_decoder(profile["rf_trees"], seed),
        X, y, groups, profile["cv_splits"]
    )

    n_classes = len(level.codewords)
    return {
        "level": level.level,
        "title": level.title,
        "n_classes": n_classes,
        "encoded_bits": float(math.log2(n_classes)),
        "elapsed_step": elapsed_step,
        "phase": (
            "during"
            if elapsed_step < profile["codeword_length"]
            else (
                "end"
                if elapsed_step == profile["codeword_length"]
                else "after"
            )
        ),
        "after_lag": max(0, elapsed_step - profile["codeword_length"]),
        "feature_set": feature_set,
        "samples": int(len(y)),
        "groups": int(len(np.unique(groups))),
        "chance_accuracy": 1.0 / n_classes,
        "primary_accuracy": float(accuracy_score(y, p1)),
        "primary_decoder_mi_bits": decoder_mutual_information_bits(y, p1),
        "secondary_accuracy": float(accuracy_score(y, p2)),
        "secondary_decoder_mi_bits": decoder_mutual_information_bits(y, p2),
        "primary_confusion_matrix": confusion_matrix(
            y, p1, labels=np.arange(n_classes)
        ).tolist(),
    }


def groupwise_permute_labels(y, groups, rng):
    out = np.array(y, copy=True)
    for g in np.unique(groups):
        idx = np.flatnonzero(groups == g)
        out[idx] = rng.permutation(out[idx])
    return out


def permutation_null(
    rows: List[dict],
    elapsed_step: int,
    feature_set: str,
    profile: dict,
    seed: int,
) -> dict:
    X, y, groups = level_matrix(rows, elapsed_step, feature_set)
    cv = GroupKFold(n_splits=min(profile["cv_splits"], len(np.unique(groups))))
    rng = np.random.default_rng(seed)
    vals = []

    for _ in range(profile["null_permutations"]):
        yp = groupwise_permute_labels(y, groups, rng)
        pred = cross_val_predict(
            clone(primary_decoder()),
            X,
            yp,
            groups=groups,
            cv=cv,
            method="predict",
        )
        vals.append(float(accuracy_score(yp, pred)))

    arr = np.asarray(vals)
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "q95": float(np.quantile(arr, 0.95)),
        "q99": float(np.quantile(arr, 0.99)),
        "max": float(np.max(arr)),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def summarize(values: Sequence[float]) -> dict:
    x = np.asarray(list(values), dtype=float)
    if len(x) == 0:
        return {"n": 0}
    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "std": float(np.std(x)),
        "median": float(np.median(x)),
        "q05": float(np.quantile(x, 0.05)),
        "q95": float(np.quantile(x, 0.95)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections: List[str] = []

    def json(self, name: str, payload: dict):
        (self.root / name).write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    def stage(self, name: str, title: str, body: str):
        text = f"# {title}\n\n{body.strip()}\n"
        (self.root / name).write_text(text, encoding="utf-8")
        self.sections.append(text)

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch17-v2-full-experimental-report.md"
        header = (
            "# Chapter 17 — What Survives the Channel? v2 Experimental Report\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
        )
        path.write_text(
            header + "\n\n".join(self.sections),
            encoding="utf-8",
        )
        return path


def save_ladder_figure(levels: Sequence[LadderLevel], path: Path):
    max_words = max(len(x.codewords) for x in levels)
    L = len(levels[0].codewords[0])
    canvas = np.full((len(levels) * max_words, L), np.nan)
    labels = []
    row = 0
    for level in levels:
        for c in level.codewords:
            canvas[row, :] = np.asarray(c)
            labels.append(f"{level.level}-{row % max_words}")
            row += 1
        while row % max_words != 0:
            labels.append("")
            row += 1

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(canvas, aspect="auto", interpolation="nearest")
    ax.set_xlabel("Transmission step")
    ax.set_ylabel("Progressive codewords")
    ax.set_title("Chapter 17 v2 — progressive information ladder")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_ladder_accuracy_figure(results: List[dict], path: Path):
    fig, ax = plt.subplots(figsize=(10, 6))
    levels = sorted(set(r["level"] for r in results))
    for level in levels:
        sub = sorted(
            [
                r for r in results
                if r["level"] == level
                and r["feature_set"] == "combined"
            ],
            key=lambda r: r["elapsed_step"],
        )
        ax.plot(
            [r["elapsed_step"] for r in sub],
            [r["primary_accuracy"] for r in sub],
            marker="o",
            label=level,
        )
    ax.axvline(16, linestyle="--", linewidth=0.9)
    ax.set_xlabel("Elapsed steps from transmission start")
    ax.set_ylabel("Held-out decoding accuracy")
    ax.set_ylim(0.0, 1.02)
    ax.set_title("When is temporal distinction recoverable?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Experimental stages
# ---------------------------------------------------------------------------

def stage_0_reproducibility(reporter, profile, params, seed):
    print("\n=== STAGE 0 — REPRODUCIBILITY INVARIANT ===")
    env = make_environment(18, seed + 1)

    def run_once():
        s = initial_state(seed + 2)
        additions = []
        for x in env:
            s, n = advance_one_step(s, float(x), profile["radius"], params)
            additions.append(n)
        return s, additions

    a, aa = run_once()
    b, bb = run_once()
    result = {
        "canonical_rng_traversal": "sorted(frontier)",
        "repeat_from_identical_state_exact": (
            a.occupied == b.occupied
            and a.rng_state == b.rng_state
            and aa == bb
        ),
        "morphology_hash_a": morphology_hash(a),
        "morphology_hash_b": morphology_hash(b),
    }
    if not result["repeat_from_identical_state_exact"]:
        raise RuntimeError("Stage 0 reproducibility invariant failed.")

    reporter.json("stage-00-reproducibility.json", result)
    reporter.stage(
        "stage-00-reproducibility.md",
        "Stage 0 — Freeze the Substrate",
        f"""```json
{json.dumps(result, indent=2)}
```""",
    )
    return result


def stage_1_ladder(reporter, image_dir):
    print("\n=== STAGE 1 — PROGRESSIVE INFORMATION LADDER ===")
    levels = build_information_ladder()
    result = ladder_diagnostics(levels)
    fig = image_dir / "ch17-v2-01-information-ladder.png"
    save_ladder_figure(levels, fig)
    result["figure"] = str(fig)
    reporter.json("stage-01-information-ladder.json", result)
    reporter.stage(
        "stage-01-information-ladder.md",
        "Stage 1 — Start With the Simplest Distinction",
        f"""
The ladder does not begin with eight hard codewords.

It begins with one early pulse versus one late pulse and increases difficulty
only after simpler distinctions are measured.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`
""",
    )
    return levels, result


def stage_2_collect(reporter, profile, params, levels, seed):
    print("\n=== STAGE 2 — MATCHED RECEIVER FORKS ===")
    all_rows = {}
    all_baselines = {}
    diagnostics = []

    for level in levels:
        rows, baseline, diag = collect_level_dataset(
            level, profile, params, seed
        )
        all_rows[level.level] = rows
        all_baselines[level.level] = baseline
        diagnostics.append(diag)

    result = {
        "levels": diagnostics,
        "measurement_schedule": {
            "during_transmission": [4, 8, 12],
            "end_of_transmission": [16],
            "after_transmission": profile["retention_lags"],
        },
        "checkpoint_control": (
            "Within each level and receiver group all codewords begin from the "
            "same checkpoint, RNG state, and future environmental forcing."
        ),
        "raw_and_paired_delta_features": (
            "Raw receiver features are primary. Matched no-channel feature deltas "
            "are reported as a mechanistic diagnostic, not the headline decoder."
        ),
    }
    reporter.json("stage-02-matched-forks.json", result)
    reporter.stage(
        "stage-02-matched-forks.md",
        "Stage 2 — During the Message and After It",
        f"""```json
{json.dumps(result, indent=2)}
```""",
    )
    return all_rows, all_baselines, result


def stage_3_decode(reporter, profile, levels, all_rows, seed):
    print("\n=== STAGE 3 — PROGRESSIVE HELD-OUT DECODING ===")
    results = []
    for level in levels:
        rows = all_rows[level.level]
        steps = sorted(set(r["elapsed_step"] for r in rows))
        for elapsed in steps:
            for feature_set in (
                "morphology",
                "recent_growth",
                "combined",
                "delta_combined",
            ):
                results.append(
                    decode_level(
                        rows,
                        level,
                        elapsed,
                        feature_set,
                        profile,
                        seed + 1000 * int(level.level[1:]) + elapsed,
                    )
                )

    payload = {
        "primary_headline_feature_set": "combined",
        "paired_delta_feature_set": "delta_combined",
        "primary_decoder": "standardized logistic regression",
        "secondary_decoder": "random forest",
        "cross_validation": "GroupKFold by receiver checkpoint group",
        "results": results,
    }
    reporter.json("stage-03-decoding.json", payload)
    reporter.stage(
        "stage-03-decoding.md",
        "Stage 3 — Where Does Recoverability First Appear?",
        f"""
The primary headline remains raw receiver `combined` features.

`delta_combined` subtracts the matched no-channel receiver and is reported only
as a causal-localization diagnostic.

```json
{json.dumps(payload, indent=2)}
```
""",
    )
    return results


def stage_4_nulls(reporter, profile, levels, all_rows, decode_results, seed):
    print("\n=== STAGE 4 — GROUPED LABEL NULLS ===")
    nulls = {}
    headline = {}

    for level in levels:
        rows = all_rows[level.level]
        steps = sorted(set(r["elapsed_step"] for r in rows))
        nulls[level.level] = {}
        headline[level.level] = {}

        for elapsed in steps:
            null = permutation_null(
                rows,
                elapsed,
                "combined",
                profile,
                seed + 10_000 * int(level.level[1:]) + elapsed,
            )
            nulls[level.level][str(elapsed)] = null

            observed = next(
                r for r in decode_results
                if r["level"] == level.level
                and r["elapsed_step"] == elapsed
                and r["feature_set"] == "combined"
            )
            headline[level.level][str(elapsed)] = {
                "accuracy": observed["primary_accuracy"],
                "chance": observed["chance_accuracy"],
                "null_q95": null["q95"],
                "beats_null_q95": observed["primary_accuracy"] > null["q95"],
            }

    result = {
        "groupwise_label_permutation": nulls,
        "headline_observed_vs_null": headline,
    }
    reporter.json("stage-04-nulls.json", result)
    reporter.stage(
        "stage-04-nulls.md",
        "Stage 4 — Attack Every Rung of the Ladder",
        f"""```json
{json.dumps(result, indent=2)}
```""",
    )
    return result


def stage_5_boundary(reporter, profile, levels, decode_results, null_result):
    print("\n=== STAGE 5 — INFORMATION BOUNDARY ===")

    boundary = {}
    first_supported_level = None
    first_supported_step = None

    for level in levels:
        entries = []
        for r in sorted(
            [
                x for x in decode_results
                if x["level"] == level.level
                and x["feature_set"] == "combined"
            ],
            key=lambda x: x["elapsed_step"],
        ):
            q95 = null_result["groupwise_label_permutation"][
                level.level
            ][str(r["elapsed_step"])]["q95"]

            # v2 uses a milder exploratory effect threshold than v1 because the
            # purpose is to locate the boundary. Full confirmation should freeze
            # the discovered rung and use a new confirmatory profile.
            margin = r["primary_accuracy"] - r["chance_accuracy"]
            passes = (
                r["primary_accuracy"] > q95
                and margin >= 0.075
            )
            entries.append({
                "elapsed_step": r["elapsed_step"],
                "phase": r["phase"],
                "after_lag": r["after_lag"],
                "accuracy": r["primary_accuracy"],
                "chance": r["chance_accuracy"],
                "margin_above_chance": margin,
                "null_q95": q95,
                "passes_exploratory_threshold": passes,
            })

            if passes and first_supported_level is None:
                first_supported_level = level.level
                first_supported_step = r["elapsed_step"]

        boundary[level.level] = entries

    result = {
        "exploratory_threshold": (
            "raw combined accuracy > grouped permutation q95 AND >= 0.075 "
            "absolute accuracy above chance"
        ),
        "first_supported_level": first_supported_level,
        "first_supported_elapsed_step": first_supported_step,
        "levels": boundary,
        "interpretation": (
            "v2 is a boundary-finding experiment. Any positive rung discovered "
            "here should be frozen and rerun in a separate confirmatory version."
        ),
    }
    reporter.json("stage-05-information-boundary.json", result)
    reporter.stage(
        "stage-05-information-boundary.md",
        "Stage 5 — Find the Simplest Surviving Distinction",
        f"""```json
{json.dumps(result, indent=2)}
```""",
    )
    return result


def stage_6_verdict(reporter, boundary_result):
    print("\n=== STAGE 6 — EXPLORATORY VERDICT ===")
    level = boundary_result["first_supported_level"]
    step = boundary_result["first_supported_elapsed_step"]

    if level is None:
        verdict = "NO_TEMPORAL_DISTINCTION_RECOVERED_AS_TESTED"
        claim = (
            "No rung of the progressive temporal information ladder produced "
            "reliable raw receiver-only recovery under the exploratory threshold."
        )
    else:
        verdict = "TEMPORAL_INFORMATION_BOUNDARY_LOCATED"
        claim = (
            f"The exploratory ladder first recovered codeword identity at {level}, "
            f"elapsed step {step}. This is a candidate boundary, not yet a "
            "confirmatory claim."
        )

    result = {
        "verdict": verdict,
        "bounded_claim": claim,
        "next_action": (
            "Freeze the simplest positive rung and its observation time, then run "
            "a new confirmatory version with larger independent groups and a "
            "predeclared endpoint."
            if level is not None
            else
            "Revisit the receiver coupling or measurement representation before "
            "increasing sample size."
        ),
        "explicit_nonclaims": [
            "semantics",
            "meaning",
            "understanding",
            "sender identity",
            "coordination",
            "learning",
            "agency",
            "individuality",
            "life",
            "Shannon channel capacity",
        ],
    }
    reporter.json("stage-06-verdict.json", result)
    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Exploratory Verdict",
        f"""**Verdict: `{verdict}`**

> {claim}

```json
{json.dumps(result, indent=2)}
```""",
    )
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PROFILES = {
    "quick": {
        "groups": 24,
        "radius": 64,
        "warmup_steps": 14,
        "codeword_length": 16,
        "retention_lags": [0, 4, 8, 16, 24],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 4,
        "null_permutations": 100,
        "rf_trees": 160,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 40,
        "radius": 72,
        "warmup_steps": 16,
        "codeword_length": 16,
        "retention_lags": [0, 4, 8, 16, 32],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 5,
        "null_permutations": 200,
        "rf_trees": 240,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 60,
        "radius": 88,
        "warmup_steps": 18,
        "codeword_length": 16,
        "retention_lags": [0, 4, 8, 16, 32],
        "recent_growth_window": 8,
        "message_gain": 0.65,
        "cv_splits": 5,
        "null_permutations": 500,
        "rf_trees": 320,
        "max_capacity_fraction": 0.85,
    },
}

EXPERIMENT_VERSION = "digital-crystal-information-survival-v2"
SCHEMA_VERSION = 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260812)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("research/digital-life/ch17-v2-reports"),
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
    started = time.time()

    metadata = {
        "model_version": MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "started_at_unix": started,
        "scientific_boundary": (
            "Exploratory boundary-finding for receiver-side temporal codeword "
            "distinction. No semantics, sender identity, coordination, agency, "
            "individuality, life, or Shannon-capacity claim."
        ),
        "primary_headline_measurement": "raw combined receiver features",
        "paired_delta_measurement_role": "diagnostic only",
        "cross_validation_boundary": "GroupKFold by receiver checkpoint group",
        "matplotlib_backend": "Agg",
    }

    print("=" * 78)
    print("CHAPTER 17 — WHAT SURVIVES THE CHANNEL? v2")
    print(f"profile={args.profile}  version={EXPERIMENT_VERSION}")
    print("=" * 78)

    s0 = stage_0_reproducibility(reporter, profile, params, args.seed)
    levels, s1 = stage_1_ladder(reporter, args.image_dir)
    rows, baselines, s2 = stage_2_collect(
        reporter, profile, params, levels, args.seed
    )
    s3 = stage_3_decode(
        reporter, profile, levels, rows, args.seed
    )
    s4 = stage_4_nulls(
        reporter, profile, levels, rows, s3, args.seed
    )
    s5 = stage_5_boundary(
        reporter, profile, levels, s3, s4
    )
    s6 = stage_6_verdict(reporter, s5)

    fig = args.image_dir / "ch17-v2-05-information-boundary.png"
    save_ladder_accuracy_figure(s3, fig)

    metadata.update({
        "finished_at_unix": time.time(),
        "stage0_reproducibility_passed": s0[
            "repeat_from_identical_state_exact"
        ],
        "final_verdict": s6["verdict"],
        "first_supported_level": s5["first_supported_level"],
        "first_supported_elapsed_step": s5["first_supported_elapsed_step"],
        "accuracy_figure": str(fig),
    })

    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print(f"VERDICT: {s6['verdict']}")
    print(s6["bounded_claim"])
    print(f"Full report: {report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
