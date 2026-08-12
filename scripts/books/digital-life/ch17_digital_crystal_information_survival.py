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
# Codebook construction
# ---------------------------------------------------------------------------

def hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.sum(np.asarray(a) != np.asarray(b)))


def make_constant_weight_codebook(
    length: int,
    weight: int,
    n_codewords: int,
    seed: int,
) -> List[np.ndarray]:
    """
    Build a deterministic max-min codebook.

    All codewords:
      * have identical length;
      * have identical Hamming weight;
      * begin with 1;
      * end with 1.

    The remaining 1s are selected from interior positions. Greedy selection
    maximizes minimum Hamming distance to already chosen words.
    """
    if length < 8:
        raise ValueError("Codeword length must be at least 8.")
    if weight < 3 or weight > length - 1:
        raise ValueError("Codeword weight must be between 3 and length-1.")

    interior_ones = weight - 2
    interior = list(range(1, length - 1))
    candidates = []

    for combo in itertools.combinations(interior, interior_ones):
        x = np.zeros(length, dtype=np.int8)
        x[0] = 1
        x[-1] = 1
        x[list(combo)] = 1
        candidates.append(x)

    if len(candidates) < n_codewords:
        raise ValueError("Not enough constant-weight codewords for requested size.")

    rng = np.random.default_rng(seed)
    first = int(rng.integers(0, len(candidates)))
    chosen = [candidates.pop(first)]

    while len(chosen) < n_codewords:
        scores = []
        for idx, cand in enumerate(candidates):
            min_d = min(hamming(cand, old) for old in chosen)
            mean_d = float(np.mean([hamming(cand, old) for old in chosen]))
            scores.append((min_d, mean_d, -idx, idx))
        _, _, _, best_idx = max(scores)
        chosen.append(candidates.pop(best_idx))

    return chosen


def codebook_diagnostics(codewords: List[np.ndarray]) -> dict:
    dists = []
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            dists.append(hamming(codewords[i], codewords[j]))

    return {
        "count": len(codewords),
        "length": int(len(codewords[0])),
        "weight_each": [int(np.sum(c)) for c in codewords],
        "first_bit_each": [int(c[0]) for c in codewords],
        "last_bit_each": [int(c[-1]) for c in codewords],
        "pairwise_hamming": {
            "min": int(min(dists)) if dists else 0,
            "mean": float(np.mean(dists)) if dists else 0.0,
            "max": int(max(dists)) if dists else 0,
        },
        "codewords": ["".join(str(int(v)) for v in c) for c in codewords],
    }


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
    n = max(1, len(occ))
    xy = np.asarray([axial_to_xy(c) for c in occ], dtype=float)
    rs = np.asarray([hex_distance(c) for c in occ], dtype=float)

    centroid = np.mean(xy, axis=0)
    centered = xy - centroid

    if len(xy) >= 2:
        cov = np.cov(centered.T, bias=True)
        eig = np.linalg.eigvalsh(cov)
        eig = np.sort(np.maximum(eig, 0.0))
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

    out = [
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
    ]
    return np.asarray(out, dtype=float)


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

    att_scale = max(1.0, float(np.max(att)))
    pop0 = max(1.0, float(pop[0]))

    return np.concatenate([
        att / att_scale,
        (pop - pop[0]) / pop0,
        np.asarray([
            float(np.mean(att)) / att_scale,
            float(np.std(att)) / att_scale,
            float(att[-1]) / att_scale,
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
# Experimental data generation
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


def run_codeword_branch(
    checkpoint: CrystalState,
    env_future: np.ndarray,
    codeword: np.ndarray,
    message_gain: float,
    radius: int,
    params: CrystalParams,
    retention_lags: Sequence[int],
    recent_window: int,
    saturation_guard: float,
) -> Dict[int, Dict[str, np.ndarray]]:
    """
    Apply one codeword, then turn the channel off and observe at retention lags.

    lag=0 means immediately after the final codeword bit has been applied.
    """
    state = clone_state(checkpoint)
    L = len(codeword)
    max_lag = max(retention_lags)
    if len(env_future) < L + max_lag:
        raise ValueError("env_future is too short for codeword + retention horizon.")

    observations: Dict[int, Dict[str, np.ndarray]] = {}

    for t in range(L + max_lag):
        bit = int(codeword[t]) if t < L else 0
        forcing = float(env_future[t]) + message_gain * bit
        state, _ = advance_one_step(state, forcing, radius, params)

        frac = capacity_fraction(state, radius)
        if frac >= saturation_guard:
            raise RuntimeError(
                "Chapter 17 branch reached hard-radius saturation guard: "
                f"step={t+1}, fraction={frac:.3f}, guard={saturation_guard:.3f}. "
                "The radius is only an experimental canvas boundary in Chapter 17; "
                "increase the profile radius rather than interpreting this endpoint."
            )

        elapsed_after_message = t - (L - 1)
        if elapsed_after_message in retention_lags:
            observations[elapsed_after_message] = combined_features(
                state, radius, recent_window
            )
            observations[elapsed_after_message]["capacity_fraction"] = np.asarray(
                [frac], dtype=float
            )

    missing = sorted(set(retention_lags) - set(observations))
    if missing:
        raise RuntimeError(f"Missing retention observations: {missing}")
    return observations


def collect_dataset(
    profile: dict,
    params: CrystalParams,
    codebook: List[np.ndarray],
    seed: int,
) -> Tuple[List[dict], Dict[int, Dict[int, Dict[str, np.ndarray]]], dict]:
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    lags = profile["retention_lags"]
    L = profile["codeword_length"]
    total_future = L + max(lags)
    guard = profile["max_capacity_fraction"]

    rows: List[dict] = []
    baseline_by_group: Dict[int, Dict[int, Dict[str, np.ndarray]]] = {}
    checkpoint_hashes = []
    max_capacity = 0.0

    for group in tqdm(range(groups), desc="Receiver groups"):
        env = make_environment(
            warmup + total_future,
            seed + 10_000 + group * 1009,
        )
        checkpoint = warm_checkpoint(
            env,
            warmup,
            seed + 20_000 + group * 1013,
            radius,
            params,
        )
        checkpoint_hashes.append(morphology_hash(checkpoint))

        future = env[warmup:]

        # No-channel baseline is generated once per group.
        baseline = run_codeword_branch(
            checkpoint,
            future,
            np.zeros(L, dtype=np.int8),
            profile["message_gain"],
            radius,
            params,
            lags,
            profile["recent_growth_window"],
            guard,
        )
        baseline_by_group[group] = baseline

        for label, codeword in enumerate(codebook):
            obs = run_codeword_branch(
                checkpoint,
                future,
                codeword,
                profile["message_gain"],
                radius,
                params,
                lags,
                profile["recent_growth_window"],
                guard,
            )

            for lag in lags:
                frac = float(obs[lag]["capacity_fraction"][0])
                max_capacity = max(max_capacity, frac)
                rows.append({
                    "group": group,
                    "label": label,
                    "lag": lag,
                    "codeword": "".join(str(int(v)) for v in codeword),
                    "morphology": obs[lag]["morphology"],
                    "recent_growth": obs[lag]["recent_growth"],
                    "combined": obs[lag]["combined"],
                    "capacity_fraction": frac,
                })

    return rows, baseline_by_group, {
        "groups": groups,
        "radius": radius,
        "hard_radius_capacity": hex_disk_capacity(radius),
        "checkpoint_hash_unique_count": len(set(checkpoint_hashes)),
        "max_capacity_fraction_observed": max_capacity,
        "saturation_guard": guard,
        "canvas_boundary_role": (
            "Experimental truncation boundary only; no boundary interaction is "
            "intended in the information-survival protocol."
        ),
    }


# ---------------------------------------------------------------------------
# Decoding
# ---------------------------------------------------------------------------

def primary_decoder() -> Pipeline:
    # Predeclared primary decoder. Linear, regularized, and deterministic.
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
        class_weight=None,
    )


def decoder_mutual_information_bits(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Plug-in mutual information I(true_label ; decoded_label).

    This is decoder-dependent recoverable information, NOT Shannon channel
    capacity and NOT I(input ; receiver_state).
    """
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


def subset_matrix(
    rows: List[dict],
    n_classes: int,
    lag: int,
    feature_set: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    selected = [
        r for r in rows
        if r["label"] < n_classes and r["lag"] == lag
    ]
    X = np.asarray([r[feature_set] for r in selected], dtype=float)
    y = np.asarray([r["label"] for r in selected], dtype=int)
    groups = np.asarray([r["group"] for r in selected], dtype=int)
    return X, y, groups


def grouped_predictions(
    model,
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    splits: int,
) -> np.ndarray:
    unique_groups = np.unique(groups)
    n_splits = min(splits, len(unique_groups))
    if n_splits < 2:
        raise RuntimeError("Need at least two receiver groups for held-out decoding.")
    cv = GroupKFold(n_splits=n_splits)
    return cross_val_predict(
        clone(model),
        X,
        y,
        groups=groups,
        cv=cv,
        method="predict",
        n_jobs=None,
    )


def decode_condition(
    rows: List[dict],
    n_classes: int,
    lag: int,
    feature_set: str,
    profile: dict,
    seed: int,
) -> dict:
    X, y, groups = subset_matrix(rows, n_classes, lag, feature_set)

    pred_primary = grouped_predictions(
        primary_decoder(), X, y, groups, profile["cv_splits"]
    )
    pred_secondary = grouped_predictions(
        secondary_decoder(profile["rf_trees"], seed),
        X, y, groups, profile["cv_splits"]
    )

    return {
        "n_classes": n_classes,
        "encoded_bits": float(math.log2(n_classes)),
        "chance_accuracy": 1.0 / n_classes,
        "lag": lag,
        "feature_set": feature_set,
        "samples": int(len(y)),
        "groups": int(len(np.unique(groups))),
        "primary_model": "standardized_logistic_regression",
        "primary_accuracy": float(accuracy_score(y, pred_primary)),
        "primary_decoder_mi_bits": decoder_mutual_information_bits(
            y, pred_primary
        ),
        "secondary_model": "random_forest",
        "secondary_accuracy": float(accuracy_score(y, pred_secondary)),
        "secondary_decoder_mi_bits": decoder_mutual_information_bits(
            y, pred_secondary
        ),
        "primary_confusion_matrix": confusion_matrix(
            y, pred_primary, labels=np.arange(n_classes)
        ).tolist(),
    }


def groupwise_permute_labels(
    y: np.ndarray,
    groups: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    out = np.array(y, copy=True)
    for g in np.unique(groups):
        idx = np.flatnonzero(groups == g)
        out[idx] = rng.permutation(out[idx])
    return out


def permutation_null(
    rows: List[dict],
    n_classes: int,
    lag: int,
    feature_set: str,
    profile: dict,
    seed: int,
) -> dict:
    X, y, groups = subset_matrix(rows, n_classes, lag, feature_set)
    rng = np.random.default_rng(seed)
    cv = GroupKFold(n_splits=min(profile["cv_splits"], len(np.unique(groups))))
    model = primary_decoder()

    values = []
    for _ in tqdm(
        range(profile["null_permutations"]),
        desc=f"Null {n_classes}c lag={lag}",
        leave=False,
    ):
        yp = groupwise_permute_labels(y, groups, rng)
        pred = cross_val_predict(
            clone(model),
            X,
            yp,
            groups=groups,
            cv=cv,
            method="predict",
        )
        values.append(float(accuracy_score(yp, pred)))

    arr = np.asarray(values, dtype=float)
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "q95": float(np.quantile(arr, 0.95)),
        "q99": float(np.quantile(arr, 0.99)),
        "max": float(np.max(arr)),
    }


def no_channel_decode(
    baseline_by_group: Dict[int, Dict[int, Dict[str, np.ndarray]]],
    n_classes: int,
    lag: int,
    feature_set: str,
    profile: dict,
) -> dict:
    X = []
    y = []
    groups = []
    for g, lag_map in baseline_by_group.items():
        feat = lag_map[lag][feature_set]
        for label in range(n_classes):
            X.append(feat)
            y.append(label)
            groups.append(g)

    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    groups = np.asarray(groups, dtype=int)

    pred = grouped_predictions(
        primary_decoder(), X, y, groups, profile["cv_splits"]
    )
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "chance_accuracy": 1.0 / n_classes,
        "decoder_mi_bits": decoder_mutual_information_bits(y, pred),
    }


# ---------------------------------------------------------------------------
# Output helpers
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
        "q25": float(np.quantile(x, 0.25)),
        "q75": float(np.quantile(x, 0.75)),
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

    def full_report(self, metadata: dict, verdict: dict) -> Path:
        path = self.root / "ch17-full-experimental-report.md"
        header = (
            "# Chapter 17 — What Survives the Channel? Full Experimental Report\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
        )
        path.write_text(
            header + "\n\n".join(self.sections),
            encoding="utf-8",
        )
        return path


def write_feature_csv(rows: List[dict], path: Path):
    if not rows:
        return
    morph_n = len(rows[0]["morphology"])
    growth_n = len(rows[0]["recent_growth"])

    fieldnames = (
        ["group", "label", "lag", "codeword", "capacity_fraction"]
        + [f"morph_{i:02d}" for i in range(morph_n)]
        + [f"growth_{i:02d}" for i in range(growth_n)]
    )

    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            row = {
                "group": r["group"],
                "label": r["label"],
                "lag": r["lag"],
                "codeword": r["codeword"],
                "capacity_fraction": r["capacity_fraction"],
            }
            row.update({
                f"morph_{i:02d}": float(v)
                for i, v in enumerate(r["morphology"])
            })
            row.update({
                f"growth_{i:02d}": float(v)
                for i, v in enumerate(r["recent_growth"])
            })
            w.writerow(row)


def save_codebook_figure(codebook: List[np.ndarray], path: Path):
    data = np.asarray(codebook, dtype=float)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(data, aspect="auto", interpolation="nearest")
    ax.set_xlabel("Transmission step")
    ax.set_ylabel("Codeword")
    ax.set_yticks(range(len(codebook)))
    ax.set_yticklabels([str(i) for i in range(len(codebook))])
    ax.set_title("Chapter 17 constant-weight temporal codebook")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_retention_figure(results: List[dict], path: Path):
    fig, ax = plt.subplots(figsize=(9, 5))
    for n_classes in (2, 4, 8):
        sub = sorted(
            [
                r for r in results
                if r["n_classes"] == n_classes
                and r["feature_set"] == "combined"
            ],
            key=lambda r: r["lag"],
        )
        ax.plot(
            [r["lag"] for r in sub],
            [r["primary_accuracy"] for r in sub],
            marker="o",
            label=f"{n_classes} codewords ({int(math.log2(n_classes))} bits)",
        )
        ax.axhline(1.0 / n_classes, linestyle="--", linewidth=0.8)

    ax.set_xlabel("Steps after transmission ended")
    ax.set_ylabel("Held-out decoder accuracy")
    ax.set_ylim(0.0, 1.02)
    ax.set_title("Recoverable codeword identity over time")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_feature_figure(results: List[dict], path: Path):
    # Show full 8-codeword case only.
    fig, ax = plt.subplots(figsize=(9, 5))
    for feature_set in ("morphology", "recent_growth", "combined"):
        sub = sorted(
            [
                r for r in results
                if r["n_classes"] == 8
                and r["feature_set"] == feature_set
            ],
            key=lambda r: r["lag"],
        )
        ax.plot(
            [r["lag"] for r in sub],
            [r["primary_accuracy"] for r in sub],
            marker="o",
            label=feature_set,
        )

    ax.axhline(1.0 / 8.0, linestyle="--", linewidth=0.8)
    ax.set_xlabel("Steps after transmission ended")
    ax.set_ylabel("Held-out decoder accuracy")
    ax.set_ylim(0.0, 1.02)
    ax.set_title("Where does recoverable information live? (8 codewords)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Stages
# ---------------------------------------------------------------------------

def stage_0_reproducibility(
    reporter: Reporter,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 0 — REPRODUCIBILITY INVARIANT ===")
    steps = 18
    env = make_environment(steps, seed + 1)

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
        f"""
Digital Crystal v1 is unchanged from Chapter 16.

```json
{json.dumps(result, indent=2)}
```

No information-survival result is interpreted unless this invariant passes.
""",
    )
    return result


def stage_1_codebook(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    seed: int,
) -> Tuple[List[np.ndarray], dict]:
    print("\n=== STAGE 1 — CONSTANT-WEIGHT CODEBOOK ===")
    codebook = make_constant_weight_codebook(
        profile["codeword_length"],
        profile["codeword_weight"],
        8,
        seed + 300,
    )
    result = codebook_diagnostics(codebook)
    result["nested_tests"] = {
        "2_codewords": result["codewords"][:2],
        "4_codewords": result["codewords"][:4],
        "8_codewords": result["codewords"][:8],
    }
    result["encoded_bits"] = {"2": 1, "4": 2, "8": 3}
    result["design_rule"] = (
        "All words have equal length, equal Hamming weight, and identical "
        "first/last bits. Only temporal arrangement carries codeword identity."
    )

    fig = image_dir / "ch17-01-codebook.png"
    save_codebook_figure(codebook, fig)
    result["figure"] = str(fig)

    reporter.json("stage-01-codebook.json", result)
    reporter.stage(
        "stage-01-codebook.md",
        "Stage 1 — Different Inputs Without Different Energy",
        f"""
The experiment uses a nested constant-weight codebook.

Every word has:
* the same length;
* the same number of 1 bits;
* the same first bit;
* the same last bit.

Only temporal arrangement distinguishes one word from another.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`
""",
    )
    return codebook, result


def stage_2_collect(
    reporter: Reporter,
    data_dir: Path,
    profile: dict,
    params: CrystalParams,
    codebook: List[np.ndarray],
    seed: int,
):
    print("\n=== STAGE 2 — MATCHED RECEIVER FORKS ===")
    rows, baselines, diagnostics = collect_dataset(
        profile, params, codebook, seed
    )
    csv_path = data_dir / "ch17-receiver-features.csv"
    write_feature_csv(rows, csv_path)

    result = {
        **diagnostics,
        "rows": len(rows),
        "codewords_per_group": 8,
        "retention_lags": profile["retention_lags"],
        "checkpoint_control": (
            "Within each group all eight codewords begin from the same receiver "
            "checkpoint, RNG state, and future environmental forcing."
        ),
        "train_test_boundary": (
            "Decoder folds are grouped by receiver group; one checkpoint never "
            "appears in both train and test."
        ),
        "feature_csv": str(csv_path),
    }

    reporter.json("stage-02-dataset.json", result)
    reporter.stage(
        "stage-02-dataset.md",
        "Stage 2 — Same Receiver, Different Codeword",
        f"""
Each receiver group creates one checkpoint and eight exact forks.

The only deliberate difference between those forks is the temporal codeword.

```json
{json.dumps(result, indent=2)}
```

The decoder never receives the transmitted bits.
""",
    )
    return rows, baselines, result


def stage_3_decode(
    reporter: Reporter,
    profile: dict,
    rows: List[dict],
    seed: int,
) -> List[dict]:
    print("\n=== STAGE 3 — HELD-OUT CODEWORD DECODING ===")
    results = []
    for n_classes in (2, 4, 8):
        for lag in profile["retention_lags"]:
            for feature_set in ("morphology", "recent_growth", "combined"):
                results.append(
                    decode_condition(
                        rows,
                        n_classes,
                        lag,
                        feature_set,
                        profile,
                        seed + n_classes * 100 + lag,
                    )
                )

    payload = {
        "primary_decoder_predeclared": "standardized logistic regression",
        "secondary_decoder": "random forest",
        "cross_validation": "GroupKFold by receiver checkpoint group",
        "results": results,
    }

    reporter.json("stage-03-decoding.json", payload)
    reporter.stage(
        "stage-03-decoding.md",
        "Stage 3 — Can the Receiver Reveal Which Codeword Was Sent?",
        f"""
The primary decoder is fixed in advance: standardized logistic regression.

A random forest is reported only as a secondary nonlinear diagnostic.

Every held-out fold contains receiver checkpoints absent from training.

```json
{json.dumps(payload, indent=2)}
```

Accuracy above chance is evidence of decoder-accessible codeword distinction,
not semantics and not channel capacity.
""",
    )
    return results


def stage_4_nulls(
    reporter: Reporter,
    profile: dict,
    rows: List[dict],
    baselines: Dict[int, Dict[int, Dict[str, np.ndarray]]],
    decode_results: List[dict],
    seed: int,
) -> dict:
    print("\n=== STAGE 4 — NULL ATTACKS ===")

    # Nulls target the predeclared primary combined decoder for every class
    # count and retention lag. This avoids choosing only successful conditions.
    nulls = {}
    no_channel = {}

    for n_classes in (2, 4, 8):
        nulls[str(n_classes)] = {}
        no_channel[str(n_classes)] = {}
        for lag in profile["retention_lags"]:
            key = str(lag)
            nulls[str(n_classes)][key] = permutation_null(
                rows,
                n_classes,
                lag,
                "combined",
                profile,
                seed + n_classes * 10_000 + lag,
            )
            no_channel[str(n_classes)][key] = no_channel_decode(
                baselines,
                n_classes,
                lag,
                "combined",
                profile,
            )

    observed = {}
    for r in decode_results:
        if r["feature_set"] == "combined":
            observed[f'{r["n_classes"]}:{r["lag"]}'] = {
                "accuracy": r["primary_accuracy"],
                "chance": r["chance_accuracy"],
                "null_q95": nulls[str(r["n_classes"])][str(r["lag"])]["q95"],
                "beats_null_q95": (
                    r["primary_accuracy"]
                    > nulls[str(r["n_classes"])][str(r["lag"])]["q95"]
                ),
            }

    result = {
        "groupwise_label_permutation": nulls,
        "no_channel": no_channel,
        "observed_vs_null": observed,
    }

    reporter.json("stage-04-nulls.json", result)
    reporter.stage(
        "stage-04-nulls.md",
        "Stage 4 — Could the Decoder Be Inventing the Signal?",
        f"""
Two nulls attack the decoding result.

1. Labels are permuted independently inside each receiver group.
2. The no-channel receiver outcome is duplicated across all codeword labels.

```json
{json.dumps(result, indent=2)}
```

A surviving claim requires the primary decoder to beat the 95th percentile of
the grouped label-permutation null.
""",
    )
    return result


def stage_5_retention(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    decode_results: List[dict],
    null_result: dict,
) -> dict:
    print("\n=== STAGE 5 — RETENTION AFTER TRANSMISSION ===")
    rows = [
        r for r in decode_results
        if r["feature_set"] == "combined"
    ]

    retention = {}
    for n_classes in (2, 4, 8):
        vals = []
        for r in sorted(
            [x for x in rows if x["n_classes"] == n_classes],
            key=lambda x: x["lag"],
        ):
            q95 = null_result["groupwise_label_permutation"][
                str(n_classes)
            ][str(r["lag"])]["q95"]
            vals.append({
                "lag": r["lag"],
                "accuracy": r["primary_accuracy"],
                "chance": r["chance_accuracy"],
                "null_q95": q95,
                "survives_null": r["primary_accuracy"] > q95,
                "decoder_mi_bits": r["primary_decoder_mi_bits"],
            })
        retention[str(n_classes)] = vals

    fig = image_dir / "ch17-05-retention.png"
    save_retention_figure(rows, fig)

    result = {
        "retention_curves": retention,
        "figure": str(fig),
        "interpretation_boundary": (
            "This measures decoder-accessible codeword identity after the "
            "channel is off. It is not a Shannon capacity estimate."
        ),
    }

    reporter.json("stage-05-retention.json", result)
    reporter.stage(
        "stage-05-retention.md",
        "Stage 5 — How Long Does the Difference Survive?",
        f"""
Transmission ends before every positive retention lag.

The decoder is then asked to identify the original codeword from the receiver.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`
""",
    )
    return result


def stage_6_where(
    reporter: Reporter,
    image_dir: Path,
    decode_results: List[dict],
) -> dict:
    print("\n=== STAGE 6 — WHERE DOES THE INFORMATION LIVE? ===")
    eight = [r for r in decode_results if r["n_classes"] == 8]

    by_lag = {}
    for lag in sorted(set(r["lag"] for r in eight)):
        by_lag[str(lag)] = {
            r["feature_set"]: {
                "primary_accuracy": r["primary_accuracy"],
                "primary_decoder_mi_bits": r["primary_decoder_mi_bits"],
                "secondary_accuracy": r["secondary_accuracy"],
            }
            for r in eight
            if r["lag"] == lag
        }

    fig = image_dir / "ch17-06-feature-location.png"
    save_feature_figure(decode_results, fig)

    result = {
        "eight_codeword_feature_comparison": by_lag,
        "feature_definitions": {
            "morphology": (
                "current occupied-cell geometry only; no birth-time history"
            ),
            "recent_growth": (
                "recent receiver attachment and population window only"
            ),
            "combined": "morphology + recent growth",
        },
        "figure": str(fig),
    }

    reporter.json("stage-06-feature-location.json", result)
    reporter.stage(
        "stage-06-feature-location.md",
        "Stage 6 — Where Does Recoverable Information Live?",
        f"""
The decoder is split into receiver-only measurement families.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`

Birth-time metadata is deliberately excluded from the morphology features.
""",
    )
    return result


def stage_7_verdict(
    reporter: Reporter,
    profile: dict,
    decode_results: List[dict],
    null_result: dict,
    retention_result: dict,
) -> dict:
    print("\n=== STAGE 7 — VERDICT ===")

    combined = {
        (r["n_classes"], r["lag"]): r
        for r in decode_results
        if r["feature_set"] == "combined"
    }

    tests = {}
    for n_classes in (2, 4, 8):
        chance = 1.0 / n_classes
        tests[str(n_classes)] = {}
        for lag in profile["retention_lags"]:
            r = combined[(n_classes, lag)]
            q95 = null_result["groupwise_label_permutation"][
                str(n_classes)
            ][str(lag)]["q95"]
            margin = r["primary_accuracy"] - chance
            passes = (
                r["primary_accuracy"] > q95
                and margin >= 0.10
            )
            tests[str(n_classes)][str(lag)] = {
                "accuracy": r["primary_accuracy"],
                "chance": chance,
                "margin_above_chance": margin,
                "null_q95": q95,
                "passes_predeclared_threshold": passes,
            }

    immediate_2 = tests["2"]["0"]["passes_predeclared_threshold"]
    retained_2 = any(
        tests["2"][str(lag)]["passes_predeclared_threshold"]
        for lag in profile["retention_lags"]
        if lag >= 8
    )

    if immediate_2 and retained_2:
        verdict = "RECOVERABLE_CODEWORD_INFORMATION_SUPPORTED"
        bounded_claim = (
            "Within this protocol, receiver-only measurements retained "
            "above-null information about which constant-weight temporal "
            "codeword had been transmitted after transmission ended."
        )
    elif immediate_2:
        verdict = "IMMEDIATE_CODEWORD_DISTINGUISHABILITY_SUPPORTED"
        bounded_claim = (
            "Within this protocol, receiver-only measurements distinguished "
            "constant-weight temporal codewords immediately after transmission, "
            "but persistent recovery at lag >= 8 was not established."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        bounded_claim = (
            "This protocol did not establish reliable receiver-only recovery "
            "of constant-weight temporal codeword identity."
        )

    # Largest nested codebook that passes at each lag.
    largest_by_lag = {}
    for lag in profile["retention_lags"]:
        passed = [
            n for n in (2, 4, 8)
            if tests[str(n)][str(lag)]["passes_predeclared_threshold"]
        ]
        largest_by_lag[str(lag)] = max(passed) if passed else 0

    result = {
        "verdict": verdict,
        "bounded_claim": bounded_claim,
        "predeclared_threshold": (
            "primary combined accuracy > grouped permutation q95 AND at least "
            "0.10 absolute accuracy above chance"
        ),
        "tests": tests,
        "largest_recoverable_nested_codebook_by_lag": largest_by_lag,
        "explicit_nonclaims": [
            "language",
            "semantics",
            "meaning",
            "understanding",
            "sender identity",
            "coordination",
            "learning",
            "intelligence",
            "agency",
            "individuality",
            "selfhood",
            "life",
            "Shannon channel capacity",
        ],
        "evidence_ledger": [
            {
                "claim": "Distinct constant-weight temporal inputs can alter receiver state differently",
                "status": "SUPPORTED" if immediate_2 else "FAILED",
            },
            {
                "claim": "Codeword identity is recoverable after transmission has ended",
                "status": "SUPPORTED" if retained_2 else "FAILED",
            },
            {
                "claim": "The receiver understands message meaning",
                "status": "UNTESTED",
            },
            {
                "claim": "Sender identity survives the channel",
                "status": "UNTESTED",
            },
            {
                "claim": "Shannon channel capacity has been measured",
                "status": "UNTESTED",
            },
        ],
    }

    reporter.json("stage-07-verdict.json", result)
    reporter.stage(
        "stage-07-verdict.md",
        "Stage 7 — Experimental Verdict",
        f"""
**Verdict: `{verdict}`**

> {bounded_claim}

```json
{json.dumps(result, indent=2)}
```
""",
    )
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="quick",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260812,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("research/digital-life/ch17-reports"),
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("research/digital-life/ch17"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    params = CrystalParams()

    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)
    args.data_dir.mkdir(parents=True, exist_ok=True)

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
            "Recoverable receiver-side codeword distinction only. No semantics, "
            "sender identity, coordination, agency, individuality, or life claim."
        ),
        "canvas_policy": (
            "The hard-radius lattice is treated as an experimental canvas boundary, "
            "not as the phenomenon under test. Profiles deliberately use a larger "
            "radius than Chapter 16 so the retention window remains well inside the "
            "boundary; any branch reaching 85% capacity still aborts."
        ),
        "primary_decoder": "standardized logistic regression",
        "cross_validation_boundary": "GroupKFold by receiver checkpoint group",
        "runtime_policy": {
            "matplotlib_backend": "Agg",
            "random_forest_n_jobs": 1,
            "reason": (
                "Headless plotting and single-process RF execution avoid "
                "Windows Tk/Tcl finalization from worker threads. This changes "
                "runtime behavior only, not the experimental protocol."
            ),
        },
    }

    print("=" * 78)
    print("CHAPTER 17 — WHAT SURVIVES THE CHANNEL?")
    print(f"profile={args.profile}  version={EXPERIMENT_VERSION}")
    print("=" * 78)

    s0 = stage_0_reproducibility(
        reporter, profile, params, args.seed
    )
    codebook, s1 = stage_1_codebook(
        reporter, args.image_dir, profile, args.seed
    )
    rows, baselines, s2 = stage_2_collect(
        reporter,
        args.data_dir,
        profile,
        params,
        codebook,
        args.seed,
    )
    s3 = stage_3_decode(
        reporter, profile, rows, args.seed
    )
    s4 = stage_4_nulls(
        reporter,
        profile,
        rows,
        baselines,
        s3,
        args.seed,
    )
    s5 = stage_5_retention(
        reporter,
        args.image_dir,
        profile,
        s3,
        s4,
    )
    s6 = stage_6_where(
        reporter,
        args.image_dir,
        s3,
    )
    s7 = stage_7_verdict(
        reporter,
        profile,
        s3,
        s4,
        s5,
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage0_reproducibility_passed": s0[
            "repeat_from_identical_state_exact"
        ],
        "final_verdict": s7["verdict"],
        "largest_recoverable_nested_codebook_by_lag": s7[
            "largest_recoverable_nested_codebook_by_lag"
        ],
    })

    report_path = reporter.full_report(metadata, s7)

    print("\n" + "=" * 78)
    print(f"VERDICT: {s7['verdict']}")
    print(s7["bounded_claim"])
    print(f"Full report: {report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
