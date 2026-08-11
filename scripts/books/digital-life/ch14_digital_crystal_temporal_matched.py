#!/usr/bin/env python3
"""
Chapter 14 — Digital Crystal v1
Matched-Distribution Temporal-Order Experiment
================================================

Purpose
-------
Freeze the Digital Crystal v1 growth mechanism and test one surgical question:

    If several source processes contain EXACTLY THE SAME VALUES
    (same multiset, mean, variance, histogram, min/max),
    but arrange those values differently in time,
    can final crystal morphology recover the temporal organization?

This experiment is deliberately designed to avoid a leakage trap:
all temporal organizations derived from the same base multiset share a
"group id", and train/test splitting is performed by group. Therefore the
classifier never sees one ordering of a particular multiset in training and
another ordering of that same multiset in testing.

The Digital Crystal v1 growth rule is copied exactly from the frozen
ch14_digital_crystal.py model. No model parameters are tuned here.

Temporal organizations
----------------------
random
    Random permutation of the base values.

block
    Sorted from low to high: long low region -> long high region.

alternating
    Alternates low/high extremes: low, high, second-low, second-high, ...

smooth
    Nearest-neighbour ordering through value space, producing slow local change.
    For scalar values this is effectively monotone but may start from either end.

burst
    Values near zero are spread through quiet periods while large-magnitude
    excursions are concentrated into short bursts.

periodic
    Values are partitioned by rank into phase buckets and interleaved to create
    a repeating temporal motif while preserving every value exactly once.

All classes use the same base multiset for each replicate.

Outputs
-------
research/digital-life/ch14-temporal-matched.sqlite3
research/digital-life/ch14-temporal-matched-reports/
static/images/books/digital-life/ch14-09-*.png

Recommended:
    python ch14_digital_crystal_temporal_matched.py --profile quick
    python ch14_digital_crystal_temporal_matched.py --profile standard
    python ch14_digital_crystal_temporal_matched.py --profile full

Dependencies:
    pip install numpy matplotlib scikit-learn tqdm
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sqlite3
import time
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 0. FROZEN DIGITAL CRYSTAL V1 MODEL
# =============================================================================

MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "matched-temporal-v1"

Cell = Tuple[int, int]

HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)

TEMPORAL_CLASSES = (
    "random",
    "block",
    "alternating",
    "smooth",
    "burst",
    "periodic",
)

FEATURE_NAMES = [
    "area",
    "perimeter",
    "max_radius",
    "compactness",
    "roughness",
    "bbox_aspect",
    "centroid_offset",
    "radial_mean",
    "radial_std",
    "angular_resultant",
    "angular_sixfold",
    "boundary_radius_mean",
    "boundary_radius_std",
    "boundary_radius_cv",
]
FEATURE_NAMES += [f"radial_bin_{i:02d}" for i in range(16)]
FEATURE_NAMES += [f"angular_bin_{i:02d}" for i in range(12)]

PROFILES = {
    "quick": dict(replicates=10, steps=72, max_radius=44),
    "standard": dict(replicates=40, steps=72, max_radius=44),
    "full": dict(replicates=100, steps=72, max_radius=44),
}


@dataclass(frozen=True)
class ModelParams:
    # EXACTLY the same defaults used by ch14_digital_crystal.py
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


@dataclass(frozen=True)
class TemporalRunSpec:
    replicate: int
    temporal_class: str
    base_seed: int
    crystal_seed: int
    steps: int
    max_radius: int
    forcing_scale: float = 1.0
    model_params: ModelParams = ModelParams()

    def key_dict(self) -> dict:
        d = asdict(self)
        d["model_version"] = MODEL_VERSION
        d["experiment_version"] = EXPERIMENT_VERSION
        return d

    def run_key(self) -> str:
        raw = json.dumps(self.key_dict(), sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:24]


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


def logistic(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def local_exposure_angle(cell: Cell, occupied: Set[Cell]) -> float:
    x, y = axial_to_xy(cell)
    vec_x = 0.0
    vec_y = 0.0
    count = 0
    for nb in neighbors(cell):
        if nb in occupied:
            nx, ny = axial_to_xy(nb)
            vec_x += x - nx
            vec_y += y - ny
            count += 1
    if count == 0 or (abs(vec_x) + abs(vec_y) < 1e-12):
        return 0.0
    return math.atan2(vec_y, vec_x)


# =============================================================================
# 1. SAME MULTISET, DIFFERENT TEMPORAL ORGANIZATION
# =============================================================================

def make_base_multiset(steps: int, seed: int) -> np.ndarray:
    """
    One continuous bounded distribution per replicate.
    Every temporal class receives exactly these values.
    """
    rng = np.random.default_rng(seed)

    # Use a symmetric continuous distribution and rank-normalize to [-1, 1].
    # Rank normalization makes replicate distributions broadly comparable
    # while preserving exact same values within a replicate.
    raw = rng.normal(0.0, 1.0, size=steps)
    order = np.argsort(raw)
    ranked = np.empty_like(raw, dtype=float)
    ranked[order] = np.linspace(-1.0, 1.0, steps)
    return ranked


def arrange_random(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    return rng.permutation(values)


def arrange_block(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    x = np.sort(values)
    if rng.random() < 0.5:
        x = x[::-1]
    return x.copy()


def arrange_alternating(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    x = np.sort(values)
    out = []
    lo = 0
    hi = len(x) - 1
    flip = bool(rng.integers(0, 2))
    while lo <= hi:
        if not flip:
            out.append(x[lo]); lo += 1
            if lo <= hi:
                out.append(x[hi]); hi -= 1
        else:
            out.append(x[hi]); hi -= 1
            if lo <= hi:
                out.append(x[lo]); lo += 1
    return np.asarray(out, dtype=float)


def arrange_smooth(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    # For scalar data, sorting minimizes adjacent changes.
    x = np.sort(values)
    if rng.random() < 0.5:
        x = x[::-1]
    # Circularly rotate so "smooth" isn't always anchored at the minimum.
    shift = int(rng.integers(0, len(x)))
    return np.roll(x, shift).copy()


def arrange_burst(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Concentrate high-|value| samples into a few contiguous bursts while
    distributing low-|value| samples through the remaining positions.
    """
    n = len(values)
    order_mag = np.argsort(np.abs(values))
    quiet_count = int(round(n * 0.67))
    quiet = values[order_mag[:quiet_count]]
    active = values[order_mag[quiet_count:]]

    quiet = rng.permutation(quiet)
    # Active values preserve alternating sign where possible to create
    # high-amplitude bursts rather than a simple monotone block.
    active = active[np.argsort(-np.abs(active))]

    out = np.empty(n, dtype=float)
    out[:] = np.nan

    # Two burst windows.
    burst_len = len(active) // 2
    start1 = n // 4 - burst_len // 2
    start2 = 3 * n // 4 - (len(active) - burst_len) // 2
    positions = list(range(max(0, start1), min(n, start1 + burst_len)))
    positions += list(range(max(0, start2), min(n, start2 + len(active) - burst_len)))

    # Repair if clipping changed count.
    positions = list(dict.fromkeys(positions))
    if len(positions) < len(active):
        for i in range(n):
            if i not in positions:
                positions.append(i)
                if len(positions) == len(active):
                    break
    positions = positions[:len(active)]

    for pos, val in zip(positions, active):
        out[pos] = val

    qi = 0
    for i in range(n):
        if np.isnan(out[i]):
            out[i] = quiet[qi]
            qi += 1

    return out


def arrange_periodic(values: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Create a repeating four-phase motif by assigning values by rank to
    phase buckets, then interleaving one value from each bucket.
    """
    x = np.sort(values)
    buckets = [list(chunk) for chunk in np.array_split(x, 4)]

    # Reverse alternating buckets to create a high/low repeating phase motif.
    buckets[1] = buckets[1][::-1]
    buckets[3] = buckets[3][::-1]

    # Rotate phase order per replicate without changing motif class.
    phase_order = list(range(4))
    shift = int(rng.integers(0, 4))
    phase_order = phase_order[shift:] + phase_order[:shift]

    out = []
    idx = [0, 0, 0, 0]
    while len(out) < len(x):
        for b in phase_order:
            if idx[b] < len(buckets[b]):
                out.append(buckets[b][idx[b]])
                idx[b] += 1
                if len(out) == len(x):
                    break
    return np.asarray(out, dtype=float)


ARRANGERS = {
    "random": arrange_random,
    "block": arrange_block,
    "alternating": arrange_alternating,
    "smooth": arrange_smooth,
    "burst": arrange_burst,
    "periodic": arrange_periodic,
}


def make_arranged_signal(spec: TemporalRunSpec) -> np.ndarray:
    base = make_base_multiset(spec.steps, spec.base_seed)
    rng = np.random.default_rng(
        spec.base_seed + 1_000_003 * (TEMPORAL_CLASSES.index(spec.temporal_class) + 1)
    )
    arranged = ARRANGERS[spec.temporal_class](base, rng)
    arranged = np.asarray(arranged, dtype=float) * spec.forcing_scale

    # Hard validation: exact multiset preservation.
    if not np.allclose(np.sort(arranged / spec.forcing_scale), np.sort(base), atol=1e-12):
        raise RuntimeError(f"Temporal arranger {spec.temporal_class} changed the value multiset.")
    return arranged


# =============================================================================
# 2. FROZEN GROWTH RULE WITH EXTERNALLY PROVIDED SIGNAL
# =============================================================================

@dataclass
class SimulationResult:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    population_by_step: List[int]
    attachments_by_step: List[int]
    signal: np.ndarray


def grow_crystal_with_signal(spec: TemporalRunSpec, signal: np.ndarray) -> SimulationResult:
    p = spec.model_params
    rng = random.Random(spec.crystal_seed)

    occupied: Set[Cell] = {(0, 0)}
    birth_time: Dict[Cell, int] = {(0, 0): 0}
    population_by_step = [1]
    attachments_by_step = [1]

    for step, s in enumerate(signal, start=1):
        frontier: Set[Cell] = set()
        for cell in occupied:
            for nb in neighbors(cell):
                if nb not in occupied and hex_distance(nb) <= spec.max_radius:
                    frontier.add(nb)

        if not frontier:
            population_by_step.append(len(occupied))
            attachments_by_step.append(0)
            continue

        additions: List[Cell] = []

        for cell in frontier:
            n = sum(nb in occupied for nb in neighbors(cell))
            theta = local_exposure_angle(cell, occupied)

            phase = p.signal_phase_gain * float(s)
            anisotropy = math.cos(6.0 * theta + phase)
            crowding = max(0, n - 2)

            score = (
                p.base_bias
                + p.neighbor_gain * n
                + p.signal_rate_gain * float(s)
                + p.anisotropy_gain * anisotropy
                - p.crowding_penalty * crowding
            )

            if rng.random() < logistic(score):
                additions.append(cell)

        for cell in additions:
            occupied.add(cell)
            birth_time[cell] = step

        population_by_step.append(len(occupied))
        attachments_by_step.append(len(additions))

    return SimulationResult(
        occupied=occupied,
        birth_time=birth_time,
        population_by_step=population_by_step,
        attachments_by_step=attachments_by_step,
        signal=np.asarray(signal, dtype=float),
    )


# =============================================================================
# 3. MORPHOLOGY — EXACT SAME FEATURE FAMILY AS V1
# =============================================================================

def perimeter_edges(occupied: Set[Cell]) -> int:
    return sum(
        1
        for cell in occupied
        for nb in neighbors(cell)
        if nb not in occupied
    )


def boundary_cells(occupied: Set[Cell]) -> List[Cell]:
    return [
        cell for cell in occupied
        if any(nb not in occupied for nb in neighbors(cell))
    ]


def morphology_features(
    occupied: Set[Cell],
    max_radius: int,
    radial_bins: int = 16,
    angular_bins: int = 12,
) -> np.ndarray:
    cells = list(occupied)
    if not cells:
        return np.zeros(len(FEATURE_NAMES), dtype=float)

    xy = np.array([axial_to_xy(c) for c in cells], dtype=float)
    radii_hex = np.array([hex_distance(c) for c in cells], dtype=float)
    euclidean_r = np.sqrt((xy ** 2).sum(axis=1))
    angles = np.arctan2(xy[:, 1], xy[:, 0])

    area = float(len(cells))
    perimeter = float(perimeter_edges(occupied))
    max_r = float(radii_hex.max())
    compactness = area / max(1.0, 1.0 + 3.0 * max_r * (max_r + 1.0))
    roughness = perimeter / max(1.0, math.sqrt(area))

    xspan = float(xy[:, 0].max() - xy[:, 0].min() + 1e-9)
    yspan = float(xy[:, 1].max() - xy[:, 1].min() + 1e-9)
    bbox_aspect = max(xspan, yspan) / max(1e-9, min(xspan, yspan))

    centroid = xy.mean(axis=0)
    centroid_offset = float(np.linalg.norm(centroid))

    radial_mean = float(np.mean(euclidean_r))
    radial_std = float(np.std(euclidean_r))

    angular_resultant = float(abs(np.mean(np.exp(1j * angles))))
    angular_sixfold = float(abs(np.mean(np.exp(1j * 6.0 * angles))))

    bnd = boundary_cells(occupied)
    bxy = np.array([axial_to_xy(c) for c in bnd], dtype=float)
    br = np.sqrt((bxy ** 2).sum(axis=1))
    br_mean = float(np.mean(br))
    br_std = float(np.std(br))
    br_cv = br_std / max(1e-9, br_mean)

    redges = np.linspace(0.0, max(1.0, max_r + 1.0), radial_bins + 1)
    radial_profile = []
    for lo, hi in zip(redges[:-1], redges[1:]):
        mask = (radii_hex >= lo) & (radii_hex < hi)
        radial_profile.append(float(mask.mean()))

    aedges = np.linspace(-np.pi, np.pi, angular_bins + 1)
    angular_profile = []
    for lo, hi in zip(aedges[:-1], aedges[1:]):
        mask = (angles >= lo) & (angles < hi)
        angular_profile.append(float(mask.mean()))

    out = np.array([
        area,
        perimeter,
        max_r,
        compactness,
        roughness,
        bbox_aspect,
        centroid_offset,
        radial_mean,
        radial_std,
        angular_resultant,
        angular_sixfold,
        br_mean,
        br_std,
        br_cv,
        *radial_profile,
        *angular_profile,
    ], dtype=float)

    if len(out) != len(FEATURE_NAMES):
        raise RuntimeError(f"Feature length mismatch: {len(out)} != {len(FEATURE_NAMES)}")
    return out


# =============================================================================
# 4. SQLITE CACHE
# =============================================================================

class Cache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS runs (
            run_key TEXT PRIMARY KEY,
            spec_json TEXT NOT NULL,
            replicate INTEGER NOT NULL,
            temporal_class TEXT NOT NULL,
            feature_json TEXT NOT NULL,
            signal_blob BLOB NOT NULL,
            occupied_blob BLOB NOT NULL,
            birth_blob BLOB NOT NULL,
            population_json TEXT NOT NULL,
            attachments_json TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        self.conn.commit()

    @staticmethod
    def _pack(obj) -> bytes:
        return zlib.compress(json.dumps(obj).encode("utf-8"), level=6)

    @staticmethod
    def _unpack(blob: bytes):
        return json.loads(zlib.decompress(blob).decode("utf-8"))

    def close(self):
        self.conn.close()

    def get(self, key: str):
        row = self.conn.execute("""
            SELECT feature_json, signal_blob, occupied_blob, birth_blob,
                   population_json, attachments_json
            FROM runs WHERE run_key=?
        """, (key,)).fetchone()
        if row is None:
            return None
        birth_raw = self._unpack(row[3])
        return {
            "features": np.array(json.loads(row[0]), dtype=float),
            "signal": np.array(self._unpack(row[1]), dtype=float),
            "occupied": {tuple(x) for x in self._unpack(row[2])},
            "birth": {tuple(map(int, k.split(","))): int(v) for k, v in birth_raw.items()},
            "population": json.loads(row[4]),
            "attachments": json.loads(row[5]),
            "cached": True,
        }

    def put(self, spec: TemporalRunSpec, result: SimulationResult, features: np.ndarray):
        birth_obj = {f"{q},{r}": int(t) for (q, r), t in result.birth_time.items()}
        occupied_obj = [[int(q), int(r)] for q, r in result.occupied]
        self.conn.execute("""
        INSERT OR REPLACE INTO runs(
            run_key, spec_json, replicate, temporal_class, feature_json,
            signal_blob, occupied_blob, birth_blob,
            population_json, attachments_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            spec.run_key(),
            json.dumps(spec.key_dict(), sort_keys=True),
            spec.replicate,
            spec.temporal_class,
            json.dumps(features.tolist()),
            self._pack(result.signal.tolist()),
            self._pack(occupied_obj),
            self._pack(birth_obj),
            json.dumps(result.population_by_step),
            json.dumps(result.attachments_by_step),
            time.time(),
        ))
        self.conn.commit()

    def get_or_run(self, spec: TemporalRunSpec):
        cached = self.get(spec.run_key())
        if cached is not None:
            return cached
        signal = make_arranged_signal(spec)
        result = grow_crystal_with_signal(spec, signal)
        features = morphology_features(result.occupied, spec.max_radius)
        self.put(spec, result, features)
        return {
            "features": features,
            "signal": signal,
            "occupied": result.occupied,
            "birth": result.birth_time,
            "population": result.population_by_step,
            "attachments": result.attachments_by_step,
            "cached": False,
        }


# =============================================================================
# 5. VISUALS
# =============================================================================

def draw_crystal(ax, occupied: Set[Cell], birth: Dict[Cell, int], title: str):
    births = np.asarray(list(birth.values()), dtype=float)
    bmin = float(births.min()) if len(births) else 0.0
    bmax = float(births.max()) if len(births) else 1.0
    denom = max(1.0, bmax - bmin)

    for cell in occupied:
        x, y = axial_to_xy(cell)
        value = (birth.get(cell, 0) - bmin) / denom
        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=0.94,
            orientation=np.pi / 6,
            facecolor=plt.cm.viridis(value),
            edgecolor="none",
        )
        ax.add_patch(patch)

    if occupied:
        pts = np.array([axial_to_xy(c) for c in occupied], dtype=float)
        margin = 2.5
        ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
        ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)


def save_signal_gallery(exemplars: Dict[str, dict], path: Path):
    fig, ax = plt.subplots(figsize=(13, 6))
    for name in TEMPORAL_CLASSES:
        ax.plot(exemplars[name]["signal"], label=name)
    ax.set_title("Exact same values, different temporal organization")
    ax.set_xlabel("time")
    ax.set_ylabel("forcing")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_crystal_gallery(exemplars: Dict[str, dict], path: Path):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, name in zip(axes.flat, TEMPORAL_CLASSES):
        run = exemplars[name]
        draw_crystal(ax, run["occupied"], run["birth"], name.title())
    fig.suptitle("Frozen Digital Crystal v1 — matched-distribution temporal sources")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_confusion(cm: np.ndarray, labels: List[str], path: Path):
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm)
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("predicted")
    ax.set_ylabel("actual")
    ax.set_title("Matched-distribution temporal-class recovery")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(int(cm[i, j])), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_accuracy(result: dict, path: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    names = ["Random forest", "Logistic"]
    vals = [result["random_forest_accuracy"], result["logistic_accuracy"]]
    ax.bar(names, vals)
    ax.axhline(result["chance"], linestyle="--", label=f"chance = {result['chance']:.3f}")
    ax.set_ylim(0, 1)
    ax.set_ylabel("group-held-out accuracy")
    ax.set_title("Can morphology recover temporal organization?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


# =============================================================================
# 6. GROUP-SAFE CLASSIFICATION
# =============================================================================

def grouped_classifier_result(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    seed: int,
) -> dict:
    """
    Split by replicate, not by row.

    Each replicate contributes one crystal per temporal class, all derived from
    the same base multiset. Group splitting prevents matched-value leakage.
    """
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    labels = sorted(set(y.tolist()))

    rf = RandomForestClassifier(
        n_estimators=700,
        min_samples_leaf=2,
        random_state=seed,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)

    lr = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=5000, random_state=seed),
    )
    lr.fit(X_train, y_train)
    pred_lr = lr.predict(X_test)

    return {
        "labels": labels,
        "chance": 1.0 / len(labels),
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "train_groups": sorted(set(map(int, groups[train_idx]))),
        "test_groups": sorted(set(map(int, groups[test_idx]))),
        "random_forest_accuracy": float(accuracy_score(y_test, pred_rf)),
        "logistic_accuracy": float(accuracy_score(y_test, pred_lr)),
        "random_forest_confusion": confusion_matrix(y_test, pred_rf, labels=labels).tolist(),
        "logistic_confusion": confusion_matrix(y_test, pred_lr, labels=labels).tolist(),
    }


def permutation_baseline(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    seed: int,
    repeats: int = 100,
) -> dict:
    """
    Empirical null: shuffle class labels within the whole dataset while keeping
    the exact same grouped train/test split rule.
    """
    rng = np.random.default_rng(seed)
    scores = []
    for i in tqdm(range(repeats), desc="Permutation null"):
        yp = np.array(y, copy=True)
        rng.shuffle(yp)
        r = grouped_classifier_result(X, yp, groups, seed + i + 1)
        scores.append(r["random_forest_accuracy"])
    return {
        "repeats": repeats,
        "mean": float(np.mean(scores)),
        "std": float(np.std(scores)),
        "p95": float(np.quantile(scores, 0.95)),
        "max": float(np.max(scores)),
    }


# =============================================================================
# 7. MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILES), default="quick")
    parser.add_argument(
        "--db",
        default="research/digital-life/ch14-temporal-matched.sqlite3",
    )
    parser.add_argument(
        "--images",
        default="static/images/books/digital-life",
    )
    parser.add_argument(
        "--reports",
        default="research/digital-life/ch14-temporal-matched-reports",
    )
    parser.add_argument("--seed", type=int, default=20260811)
    parser.add_argument("--force-recompute", action="store_true")
    parser.add_argument(
        "--permutations",
        type=int,
        default=None,
        help="Override permutation-null repeats (quick=30, standard=100, full=200)",
    )
    args = parser.parse_args()

    profile = PROFILES[args.profile]
    db_path = Path(args.db)
    image_dir = Path(args.images)
    report_dir = Path(args.reports)
    image_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    if args.force_recompute and db_path.exists():
        db_path.unlink()

    cache = Cache(db_path)

    specs: List[TemporalRunSpec] = []
    for rep in range(profile["replicates"]):
        base_seed = args.seed + rep * 1009
        for ci, temporal_class in enumerate(TEMPORAL_CLASSES):
            # Different morphology randomness per class. This is intentional:
            # classification must survive ordinary crystal stochasticity.
            crystal_seed = args.seed + rep * 1_000_003 + ci * 10_007 + 77
            specs.append(
                TemporalRunSpec(
                    replicate=rep,
                    temporal_class=temporal_class,
                    base_seed=base_seed,
                    crystal_seed=crystal_seed,
                    steps=profile["steps"],
                    max_radius=profile["max_radius"],
                )
            )

    X = []
    y = []
    groups = []
    cached_count = 0
    exemplars = {}

    print("\n=== MATCHED-DISTRIBUTION TEMPORAL EXPERIMENT ===")
    for spec in tqdm(specs, desc="Growing matched temporal crystals"):
        run = cache.get_or_run(spec)
        cached_count += int(run["cached"])
        X.append(run["features"])
        y.append(spec.temporal_class)
        groups.append(spec.replicate)
        if spec.replicate == 0:
            exemplars[spec.temporal_class] = run

    X = np.vstack(X)
    y = np.asarray(y)
    groups = np.asarray(groups)

    # Validate exact same multiset for exemplar replicate.
    exemplar_sorted = {
        name: np.sort(exemplars[name]["signal"])
        for name in TEMPORAL_CLASSES
    }
    reference = exemplar_sorted[TEMPORAL_CLASSES[0]]
    exact_multiset_ok = all(
        np.allclose(reference, exemplar_sorted[name], atol=1e-12)
        for name in TEMPORAL_CLASSES[1:]
    )

    signal_fig = image_dir / "ch14-09-matched-temporal-signals.png"
    crystal_fig = image_dir / "ch14-09-matched-temporal-crystals.png"
    save_signal_gallery(exemplars, signal_fig)
    save_crystal_gallery(exemplars, crystal_fig)

    result = grouped_classifier_result(X, y, groups, args.seed + 99)

    perm_repeats = args.permutations
    if perm_repeats is None:
        perm_repeats = {"quick": 30, "standard": 100, "full": 200}[args.profile]

    null = permutation_baseline(
        X, y, groups,
        seed=args.seed + 555,
        repeats=perm_repeats,
    )

    cm_path = image_dir / "ch14-09-matched-temporal-confusion.png"
    acc_path = image_dir / "ch14-09-matched-temporal-accuracy.png"
    save_confusion(
        np.asarray(result["random_forest_confusion"]),
        result["labels"],
        cm_path,
    )
    save_accuracy(result, acc_path)

    # Conservative interpretation.
    materially_above_chance = (
        result["random_forest_accuracy"] >= result["chance"] + 0.15
        and result["logistic_accuracy"] >= result["chance"] + 0.10
        and result["random_forest_accuracy"] > null["p95"]
    )

    if materially_above_chance:
        verdict = "TEMPORAL_ORGANIZATION_RECOVERABLE"
        claim = (
            "With the Digital Crystal v1 growth rule frozen and input value "
            "distributions exactly matched, final morphology retained "
            "recoverable information about temporal organization."
        )
    else:
        verdict = "TEMPORAL_ORGANIZATION_NOT_RECOVERABLE"
        claim = (
            "With the Digital Crystal v1 growth rule frozen and input value "
            "distributions exactly matched, this experiment did not establish "
            "recoverable information about temporal organization in final morphology."
        )

    summary = {
        "experiment_version": EXPERIMENT_VERSION,
        "model_version": MODEL_VERSION,
        "profile": args.profile,
        "replicates": profile["replicates"],
        "steps": profile["steps"],
        "max_radius": profile["max_radius"],
        "temporal_classes": list(TEMPORAL_CLASSES),
        "total_crystals": int(len(y)),
        "cached_runs": int(cached_count),
        "exact_multiset_validation": bool(exact_multiset_ok),
        "group_safe_split": True,
        "classification": result,
        "permutation_null": null,
        "verdict": verdict,
        "bounded_claim": claim,
        "figures": {
            "signals": str(signal_fig),
            "crystals": str(crystal_fig),
            "confusion": str(cm_path),
            "accuracy": str(acc_path),
        },
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "life",
            "universal temporal encoding",
        ],
    }

    json_path = report_dir / "ch14-temporal-matched-summary.json"
    md_path = report_dir / "ch14-temporal-matched-report.md"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = f"""# Chapter 14 — Matched-Distribution Temporal Experiment

## Question

If source processes contain **exactly the same values** but arrange those values
differently in time, can final Digital Crystal v1 morphology recover the temporal
organization?

## Design

- Frozen model: `{MODEL_VERSION}`
- Temporal classes: {", ".join(TEMPORAL_CLASSES)}
- Replicates: **{profile["replicates"]}**
- Crystals: **{len(y)}**
- Steps per crystal: **{profile["steps"]}**
- Exact multiset validation: **{exact_multiset_ok}**
- Train/test split by matched-value replicate group: **True**
- Cached runs reused: **{cached_count}/{len(y)}**

The group split is critical: all six orderings created from one base multiset
remain entirely in train or entirely in test. There is no matched-multiset leakage.

## Held-out classification

Six-way chance: **{result["chance"]:.3f}**

- Random forest: **{result["random_forest_accuracy"]:.3f}**
- Logistic regression: **{result["logistic_accuracy"]:.3f}**

## Permutation-label null

- Repeats: **{null["repeats"]}**
- Mean RF accuracy: **{null["mean"]:.3f}**
- Std: **{null["std"]:.3f}**
- 95th percentile: **{null["p95"]:.3f}**
- Maximum observed null accuracy: **{null["max"]:.3f}**

## Verdict

**`{verdict}`**

> {claim}

## Interpretation

A positive result would strengthen the Chapter 14 claim from
"morphology carries source-family information" to the narrower but stronger
claim that morphology can retain information about temporal organization even
when source-value distributions are exactly matched.

A negative result is equally useful: it would indicate that Digital Crystal v1
primarily encodes distributional/statistical characteristics of forcing rather
than temporal order, giving the next state/history chapter a concrete missing
capability to solve.

## Figures

- `{signal_fig}`
- `{crystal_fig}`
- `{cm_path}`
- `{acc_path}`
"""
    md_path.write_text(md, encoding="utf-8")

    print("\n" + "=" * 78)
    print("MATCHED-DISTRIBUTION TEMPORAL EXPERIMENT COMPLETE")
    print("=" * 78)
    print(f"Exact multiset validation: {exact_multiset_ok}")
    print(f"Chance:          {result['chance']:.3f}")
    print(f"Random forest:   {result['random_forest_accuracy']:.3f}")
    print(f"Logistic:        {result['logistic_accuracy']:.3f}")
    print(f"Null 95th pct:   {null['p95']:.3f}")
    print(f"Verdict:         {verdict}")
    print(claim)
    print(f"Report:          {md_path}")
    print(f"Summary:         {json_path}")
    print("=" * 78)

    cache.close()


if __name__ == "__main__":
    main()
