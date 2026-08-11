#!/usr/bin/env python3
"""
Digital Life Chapter 14 — Digital Crystal Experiment
=====================================================

Purpose
-------
Build and attack a falsifiable "digital crystal" model before writing the chapter.

Working hypothesis:
    A fixed local computational growth rule can transform a time-varying input
    into persistent morphology from which information about the source process
    remains recoverable.

The script is intentionally one large, self-contained experimental harness.
It uses:
    - SQLite caching
    - tqdm progress bars
    - Matplotlib figures
    - staged Markdown + JSON reports
    - compressed run artifacts in SQLite
    - held-out classification tests
    - temporal-order controls
    - same-mean controls
    - modest robustness tests

Nothing here demonstrates life, learning, adaptation, agency, memory, or a
universal theory of digital crystals.

Recommended first run:
    python ch14_digital_crystal.py --profile quick

Then:
    python ch14_digital_crystal.py --profile standard

And only if useful:
    python ch14_digital_crystal.py --profile full

Dependencies:
    pip install numpy matplotlib scikit-learn tqdm

Default outputs:
    research/digital-life/ch14-digital-crystal.sqlite3
    static/images/books/digital-life/ch14-*.png
    research/digital-life/ch14-reports/*.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sqlite3
import statistics
import sys
import textwrap
import time
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

try:
    from tqdm import tqdm
except ImportError as exc:
    raise SystemExit("Missing tqdm. Install with: pip install tqdm") from exc

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
except ImportError as exc:
    raise SystemExit(
        "Missing scikit-learn. Install with: pip install scikit-learn"
    ) from exc


# =============================================================================
# 0. CONFIGURATION
# =============================================================================

SCHEMA_VERSION = 1
MODEL_VERSION = "digital-crystal-v1"

Cell = Tuple[int, int]

HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)

SIGNAL_NAMES = (
    "constant",
    "sine",
    "square",
    "saw",
    "white_noise",
    "random_walk",
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
    "quick": dict(
        runs_per_class=8,
        steps=36,
        max_radius=24,
        robustness_runs=3,
        robustness_levels=(0.85, 1.00, 1.15),
    ),
    "standard": dict(
        runs_per_class=36,
        steps=54,
        max_radius=34,
        robustness_runs=10,
        robustness_levels=(0.80, 0.90, 1.00, 1.10, 1.20),
    ),
    "full": dict(
        runs_per_class=100,
        steps=72,
        max_radius=44,
        robustness_runs=24,
        robustness_levels=(0.75, 0.85, 0.95, 1.00, 1.05, 1.15, 1.25),
    ),
}


@dataclass(frozen=True)
class ModelParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


@dataclass(frozen=True)
class RunSpec:
    signal_name: str
    signal_seed: int
    crystal_seed: int
    steps: int
    max_radius: int
    order_mode: str = "ordered"       # ordered | shuffled
    forcing_scale: float = 1.0
    model_params: ModelParams = ModelParams()

    def key_dict(self) -> dict:
        d = asdict(self)
        d["model_version"] = MODEL_VERSION
        return d

    def run_key(self) -> str:
        raw = json.dumps(self.key_dict(), sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:24]


# =============================================================================
# 1. HEX GRID + LOCAL GROWTH MODEL
# =============================================================================

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
    """
    Estimate the outward-facing direction of a frontier cell from only its
    occupied neighbours. This avoids giving the rule an explicit target shape.
    """
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
# 2. SIGNAL FAMILIES
# =============================================================================

def normalize_signal(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    x = x - float(np.mean(x))
    mx = float(np.max(np.abs(x))) if len(x) else 0.0
    if mx > 0:
        x = x / mx
    return np.clip(x, -1.0, 1.0)


def make_signal(name: str, steps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)

    if name == "constant":
        return np.zeros(steps, dtype=float)

    if name == "sine":
        period = rng.uniform(10.0, 18.0)
        phase = rng.uniform(0.0, 2 * np.pi)
        return normalize_signal(np.sin((2 * np.pi * t / period) + phase))

    if name == "square":
        period = rng.uniform(10.0, 18.0)
        phase = rng.uniform(0.0, 2 * np.pi)
        return normalize_signal(
            np.where(np.sin((2 * np.pi * t / period) + phase) >= 0, 1.0, -1.0)
        )

    if name == "saw":
        period = rng.uniform(10.0, 18.0)
        phase = rng.uniform(0.0, period)
        x = ((t + phase) % period) / period
        return normalize_signal((2.0 * x) - 1.0)

    if name == "white_noise":
        return normalize_signal(rng.uniform(-1.0, 1.0, size=steps))

    if name == "random_walk":
        walk = np.cumsum(rng.normal(0.0, 0.25, size=steps))
        return normalize_signal(walk)

    raise ValueError(f"Unknown signal: {name}")


# =============================================================================
# 3. SIMULATION
# =============================================================================

@dataclass
class SimulationResult:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    population_by_step: List[int]
    attachments_by_step: List[int]
    signal: np.ndarray


def grow_crystal(spec: RunSpec) -> SimulationResult:
    """
    Fixed local rule. The source class never changes the rule itself.

    The scalar signal does only two things:
      1. very weakly changes overall attachment propensity;
      2. rotates the phase of a fixed local six-fold anisotropy.

    Thus a signal can alter how growth unfolds, but there is no
    "if sine then draw X" logic.
    """
    signal = make_signal(spec.signal_name, spec.steps, spec.signal_seed)
    if spec.order_mode == "shuffled" and spec.signal_name != "constant":
        rng_order = np.random.default_rng(spec.signal_seed + 9_999_991)
        signal = np.array(signal, copy=True)
        rng_order.shuffle(signal)
    signal = np.clip(signal * spec.forcing_scale, -1.5, 1.5)

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

            # Signal rotates the preferred local attachment phase.
            phase = p.signal_phase_gain * float(s)
            anisotropy = math.cos(6.0 * theta + phase)

            # Dense frontier positions are less likely to fill immediately,
            # preserving a nontrivial boundary rather than deterministic discs.
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
        signal=signal,
    )


# =============================================================================
# 4. MORPHOLOGY MEASUREMENTS
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

    # Circular concentration and six-fold harmonic.
    angular_resultant = float(
        abs(np.mean(np.exp(1j * angles)))
    )
    angular_sixfold = float(
        abs(np.mean(np.exp(1j * 6.0 * angles)))
    )

    bnd = boundary_cells(occupied)
    bxy = np.array([axial_to_xy(c) for c in bnd], dtype=float)
    br = np.sqrt((bxy ** 2).sum(axis=1))
    br_mean = float(np.mean(br))
    br_std = float(np.std(br))
    br_cv = br_std / max(1e-9, br_mean)

    # Radial mass fractions. We normalize by total occupied mass, not shell
    # capacity, because this is a morphology descriptor rather than a growth-law test.
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
        raise RuntimeError(
            f"Feature length mismatch: {len(out)} != {len(FEATURE_NAMES)}"
        )
    return out


# =============================================================================
# 5. SQLITE CACHE
# =============================================================================

class Cache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS runs (
            run_key TEXT PRIMARY KEY,
            model_version TEXT NOT NULL,
            spec_json TEXT NOT NULL,
            signal_name TEXT NOT NULL,
            order_mode TEXT NOT NULL,
            forcing_scale REAL NOT NULL,
            signal_seed INTEGER NOT NULL,
            crystal_seed INTEGER NOT NULL,
            steps INTEGER NOT NULL,
            max_radius INTEGER NOT NULL,
            feature_json TEXT NOT NULL,
            population_json TEXT NOT NULL,
            attachments_json TEXT NOT NULL,
            signal_blob BLOB NOT NULL,
            occupied_blob BLOB NOT NULL,
            birth_blob BLOB NOT NULL,
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS analyses (
            analysis_key TEXT PRIMARY KEY,
            analysis_type TEXT NOT NULL,
            config_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        self.conn.execute(
            "INSERT OR REPLACE INTO metadata(key,value) VALUES('schema_version',?)",
            (str(SCHEMA_VERSION),)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    @staticmethod
    def _pack_json(obj) -> bytes:
        return zlib.compress(json.dumps(obj).encode("utf-8"), level=6)

    @staticmethod
    def _unpack_json(blob: bytes):
        return json.loads(zlib.decompress(blob).decode("utf-8"))

    def get_run(self, run_key: str):
        row = self.conn.execute("""
            SELECT feature_json, population_json, attachments_json,
                   signal_blob, occupied_blob, birth_blob, spec_json
            FROM runs WHERE run_key=?
        """, (run_key,)).fetchone()
        if row is None:
            return None

        features = np.array(json.loads(row[0]), dtype=float)
        population = list(json.loads(row[1]))
        attachments = list(json.loads(row[2]))
        signal = np.array(self._unpack_json(row[3]), dtype=float)
        occupied = {tuple(x) for x in self._unpack_json(row[4])}
        birth_raw = self._unpack_json(row[5])
        birth = {tuple(map(int, k.split(","))): int(v) for k, v in birth_raw.items()}
        spec_json = json.loads(row[6])
        return dict(
            features=features,
            population=population,
            attachments=attachments,
            signal=signal,
            occupied=occupied,
            birth=birth,
            spec_json=spec_json,
        )

    def put_run(self, spec: RunSpec, result: SimulationResult, features: np.ndarray):
        birth_obj = {f"{q},{r}": int(t) for (q, r), t in result.birth_time.items()}
        occupied_obj = [[int(q), int(r)] for q, r in result.occupied]
        self.conn.execute("""
            INSERT OR REPLACE INTO runs(
                run_key, model_version, spec_json, signal_name, order_mode,
                forcing_scale, signal_seed, crystal_seed, steps, max_radius,
                feature_json, population_json, attachments_json,
                signal_blob, occupied_blob, birth_blob, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            spec.run_key(),
            MODEL_VERSION,
            json.dumps(spec.key_dict(), sort_keys=True),
            spec.signal_name,
            spec.order_mode,
            spec.forcing_scale,
            spec.signal_seed,
            spec.crystal_seed,
            spec.steps,
            spec.max_radius,
            json.dumps(features.tolist()),
            json.dumps(result.population_by_step),
            json.dumps(result.attachments_by_step),
            self._pack_json(result.signal.tolist()),
            self._pack_json(occupied_obj),
            self._pack_json(birth_obj),
            time.time(),
        ))
        self.conn.commit()

    def get_or_run(self, spec: RunSpec):
        cached = self.get_run(spec.run_key())
        if cached is not None:
            cached["cached"] = True
            return cached

        result = grow_crystal(spec)
        features = morphology_features(result.occupied, spec.max_radius)
        self.put_run(spec, result, features)
        return dict(
            features=features,
            population=result.population_by_step,
            attachments=result.attachments_by_step,
            signal=result.signal,
            occupied=result.occupied,
            birth=result.birth_time,
            spec_json=spec.key_dict(),
            cached=False,
        )

    def analysis_get(self, key: str):
        row = self.conn.execute(
            "SELECT result_json FROM analyses WHERE analysis_key=?",
            (key,)
        ).fetchone()
        return None if row is None else json.loads(row[0])

    def analysis_put(self, key: str, kind: str, config: dict, result: dict):
        self.conn.execute("""
            INSERT OR REPLACE INTO analyses(
                analysis_key, analysis_type, config_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            key,
            kind,
            json.dumps(config, sort_keys=True),
            json.dumps(result),
            time.time(),
        ))
        self.conn.commit()


# =============================================================================
# 6. REPORTING HELPERS
# =============================================================================

class Reporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.stage_summaries: List[Tuple[str, str]] = []

    def write_stage(self, filename: str, title: str, body: str):
        text = f"# {title}\n\n{body.strip()}\n"
        path = self.report_dir / filename
        path.write_text(text, encoding="utf-8")
        self.stage_summaries.append((title, body.strip()))
        print(f"[report] {path}")

    def write_json(self, filename: str, data: dict):
        path = self.report_dir / filename
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[report] {path}")

    def write_final(self, metadata: dict):
        chunks = [
            "# Chapter 14 — Digital Crystal: Full Experimental Report",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(metadata, indent=2),
            "```",
            "",
        ]
        for title, body in self.stage_summaries:
            chunks += [f"## {title}", "", body, ""]
        path = self.report_dir / "ch14-full-report.md"
        path.write_text("\n".join(chunks), encoding="utf-8")
        print(f"[report] {path}")
        return path


# =============================================================================
# 7. VISUALIZATION
# =============================================================================

def draw_crystal(ax, occupied: Set[Cell], birth: Dict[Cell, int], title: str = ""):
    births = np.array(list(birth.values()), dtype=float)
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


def save_baseline_figure(run, image_dir: Path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    draw_crystal(axes[0], run["occupied"], run["birth"], "Constant-input crystal")
    axes[1].plot(run["signal"])
    axes[1].set_title("Input")
    axes[1].set_xlabel("step")
    axes[1].set_ylabel("forcing")
    axes[2].plot(run["population"])
    axes[2].set_title("Population growth")
    axes[2].set_xlabel("step")
    axes[2].set_ylabel("occupied cells")
    fig.tight_layout()
    path = image_dir / "ch14-01-baseline.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_source_gallery(exemplars: Dict[str, dict], image_dir: Path):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, name in zip(axes.flat, SIGNAL_NAMES):
        run = exemplars[name]
        draw_crystal(ax, run["occupied"], run["birth"], name.replace("_", " ").title())
    fig.suptitle("Same digital-crystal rule, different source processes")
    fig.tight_layout()
    path = image_dir / "ch14-02-source-gallery.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_signal_gallery(exemplars: Dict[str, dict], image_dir: Path):
    fig, ax = plt.subplots(figsize=(12, 6))
    for name in SIGNAL_NAMES:
        ax.plot(exemplars[name]["signal"], label=name.replace("_", " "))
    ax.set_xlabel("growth step")
    ax.set_ylabel("forcing")
    ax.set_title("Example source signals")
    ax.legend()
    fig.tight_layout()
    path = image_dir / "ch14-02-source-signals.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_metric_distributions(rows: List[Tuple[str, np.ndarray]], image_dir: Path):
    # Plot a compact set of interpretable metrics.
    selected = ["area", "roughness", "angular_sixfold", "boundary_radius_cv"]
    indices = [FEATURE_NAMES.index(x) for x in selected]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    for ax, feature_name, idx in zip(axes.flat, selected, indices):
        grouped = []
        labels = []
        for name in SIGNAL_NAMES:
            vals = [feat[idx] for label, feat in rows if label == name]
            grouped.append(vals)
            labels.append(name.replace("_", "\n"))
        ax.boxplot(grouped, tick_labels=labels, showfliers=False)
        ax.set_title(feature_name.replace("_", " ").title())
    fig.tight_layout()
    path = image_dir / "ch14-05-morphology-metrics.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_confusion(cm: np.ndarray, labels: List[str], title: str, path: Path):
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm)
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels([x.replace("_", "\n") for x in labels], rotation=35, ha="right")
    ax.set_yticklabels([x.replace("_", " ") for x in labels])
    ax.set_xlabel("predicted")
    ax.set_ylabel("actual")
    ax.set_title(title)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(int(cm[i, j])), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_accuracy_plot(results: Dict[str, float], chance: float, title: str, path: Path):
    names = list(results.keys())
    vals = [results[k] for k in names]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(names, vals)
    ax.axhline(chance, linestyle="--", label=f"chance = {chance:.3f}")
    ax.set_ylim(0, 1)
    ax.set_ylabel("held-out accuracy")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


# =============================================================================
# 8. ANALYSIS
# =============================================================================

def dataset_from_specs(cache: Cache, specs: List[RunSpec], desc: str):
    X = []
    y = []
    cached_count = 0
    exemplars = {}

    for spec in tqdm(specs, desc=desc):
        run = cache.get_or_run(spec)
        cached_count += int(run["cached"])
        X.append(run["features"])
        y.append(spec.signal_name)
        exemplars.setdefault(spec.signal_name, run)

    return np.vstack(X), np.array(y), exemplars, cached_count


def classifier_result(X: np.ndarray, y: np.ndarray, seed: int) -> dict:
    labels = sorted(set(y.tolist()))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.30,
        stratify=y,
        random_state=seed,
    )

    rf = RandomForestClassifier(
        n_estimators=500,
        min_samples_leaf=2,
        random_state=seed,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)

    lr = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=4000, random_state=seed),
    )
    lr.fit(X_train, y_train)
    pred_lr = lr.predict(X_test)

    return {
        "labels": labels,
        "chance": 1.0 / len(labels),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "random_forest_accuracy": float(accuracy_score(y_test, pred_rf)),
        "logistic_accuracy": float(accuracy_score(y_test, pred_lr)),
        "random_forest_confusion": confusion_matrix(
            y_test, pred_rf, labels=labels
        ).tolist(),
        "logistic_confusion": confusion_matrix(
            y_test, pred_lr, labels=labels
        ).tolist(),
    }


def binary_order_test(cache: Cache, base_specs: List[RunSpec], seed: int) -> dict:
    X = []
    y = []
    for spec in tqdm(base_specs, desc="Stage 7: ordered vs shuffled"):
        if spec.signal_name == "constant":
            continue
        ordered = RunSpec(
            signal_name=spec.signal_name,
            signal_seed=spec.signal_seed,
            crystal_seed=spec.crystal_seed,
            steps=spec.steps,
            max_radius=spec.max_radius,
            order_mode="ordered",
            forcing_scale=spec.forcing_scale,
            model_params=spec.model_params,
        )
        shuffled = RunSpec(
            signal_name=spec.signal_name,
            signal_seed=spec.signal_seed,
            crystal_seed=spec.crystal_seed + 33_333_333,
            steps=spec.steps,
            max_radius=spec.max_radius,
            order_mode="shuffled",
            forcing_scale=spec.forcing_scale,
            model_params=spec.model_params,
        )
        X.append(cache.get_or_run(ordered)["features"])
        y.append("ordered")
        X.append(cache.get_or_run(shuffled)["features"])
        y.append("shuffled")

    return classifier_result(np.vstack(X), np.array(y), seed)


def class_centroid_distances(X: np.ndarray, y: np.ndarray):
    labels = sorted(set(y.tolist()))
    means = {lab: X[y == lab].mean(axis=0) for lab in labels}
    # Standardize dimensions globally before distances.
    sd = X.std(axis=0)
    sd[sd < 1e-9] = 1.0
    out = {}
    for a in labels:
        for b in labels:
            d = float(np.linalg.norm((means[a] - means[b]) / sd))
            out[f"{a}__{b}"] = d
    return out


# =============================================================================
# 9. STAGED EXPERIMENT
# =============================================================================

def build_specs(profile: dict, seed: int, order_mode="ordered", forcing_scale=1.0):
    specs = []
    for class_idx, name in enumerate(SIGNAL_NAMES):
        for run_idx in range(profile["runs_per_class"]):
            signal_seed = seed + class_idx * 1_000_000 + run_idx * 101
            crystal_seed = seed + class_idx * 2_000_000 + run_idx * 313 + 17
            specs.append(
                RunSpec(
                    signal_name=name,
                    signal_seed=signal_seed,
                    crystal_seed=crystal_seed,
                    steps=profile["steps"],
                    max_radius=profile["max_radius"],
                    order_mode=order_mode,
                    forcing_scale=forcing_scale,
                )
            )
    return specs


def main():
    parser = argparse.ArgumentParser(
        description="Chapter 14 Digital Crystal falsifiable experiment"
    )
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILES.keys()),
        default="quick",
        help="quick first, then standard/full if the model survives",
    )
    parser.add_argument(
        "--db",
        default="research/digital-life/ch14-digital-crystal.sqlite3",
    )
    parser.add_argument(
        "--images",
        default="static/images/books/digital-life",
    )
    parser.add_argument(
        "--reports",
        default="research/digital-life/ch14-reports",
    )
    parser.add_argument("--seed", type=int, default=20260811)
    parser.add_argument(
        "--force-recompute",
        action="store_true",
        help="Delete cached DB before run",
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
    reporter = Reporter(report_dir)

    metadata = {
        "model_version": MODEL_VERSION,
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "database": str(db_path),
        "images": str(image_dir),
        "reports": str(report_dir),
        "started_at_unix": time.time(),
    }

    # -------------------------------------------------------------------------
    # STAGE 1 — BASELINE
    # -------------------------------------------------------------------------
    print("\n=== STAGE 1: BASELINE CRYSTAL ===")
    baseline_spec = RunSpec(
        signal_name="constant",
        signal_seed=args.seed,
        crystal_seed=args.seed + 1,
        steps=profile["steps"],
        max_radius=profile["max_radius"],
    )
    baseline = cache.get_or_run(baseline_spec)
    baseline_fig = save_baseline_figure(baseline, image_dir)

    baseline_summary = {
        "cached": baseline["cached"],
        "final_population": int(len(baseline["occupied"])),
        "max_radius": int(max(hex_distance(c) for c in baseline["occupied"])),
        "final_perimeter": int(perimeter_edges(baseline["occupied"])),
        "figure": str(baseline_fig),
    }
    reporter.write_json("stage-01-baseline.json", baseline_summary)
    reporter.write_stage(
        "stage-01-baseline.md",
        "Stage 1 — Baseline Crystal",
        f"""
The generalized harness first runs with a constant zero-valued environment.

- Final occupied cells: **{baseline_summary['final_population']}**
- Maximum hex radius reached: **{baseline_summary['max_radius']}**
- Boundary edge count: **{baseline_summary['final_perimeter']}**
- Cached run: **{baseline_summary['cached']}**

Interpretation: this is only a plumbing check. The generalized model must still
produce a coherent growing structure before source-dependent experiments mean
anything.

Figure: `{baseline_fig}`
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 2 — SOURCE POPULATIONS + GALLERY
    # -------------------------------------------------------------------------
    print("\n=== STAGE 2: SOURCE POPULATIONS ===")
    ordered_specs = build_specs(profile, args.seed, order_mode="ordered")
    X, y, exemplars, cached_count = dataset_from_specs(
        cache, ordered_specs, "Stage 2: source populations"
    )
    gallery = save_source_gallery(exemplars, image_dir)
    signals_fig = save_signal_gallery(exemplars, image_dir)

    counts = {name: int(np.sum(y == name)) for name in SIGNAL_NAMES}
    stage2 = {
        "counts": counts,
        "cached_runs": int(cached_count),
        "total_runs": int(len(y)),
        "gallery": str(gallery),
        "signals": str(signals_fig),
    }
    reporter.write_json("stage-02-source-populations.json", stage2)
    reporter.write_stage(
        "stage-02-source-populations.md",
        "Stage 2 — Different Sources, Same Rule",
        f"""
Generated **{len(y)}** crystals across six source families with one fixed
local-growth rule.

Counts: `{counts}`

Cached runs reused: **{cached_count}/{len(y)}**

At this stage visual differences are only hypotheses. They are not yet evidence
that source information survives in morphology.

Figures:
- `{gallery}`
- `{signals_fig}`
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 3 — SAME-MEAN CONTROL
    # -------------------------------------------------------------------------
    print("\n=== STAGE 3: SAME-MEAN CONTROL ===")
    # Every nonconstant signal is normalized to approximately zero mean.
    # Constant control is exactly zero. Compare simple feature-centroid distance.
    constant_X = X[y == "constant"]
    same_mean = {}
    global_sd = X.std(axis=0)
    global_sd[global_sd < 1e-9] = 1.0
    cmean = constant_X.mean(axis=0)
    for name in SIGNAL_NAMES:
        if name == "constant":
            continue
        m = X[y == name].mean(axis=0)
        same_mean[name] = float(np.linalg.norm((m - cmean) / global_sd))

    reporter.write_json("stage-03-same-mean.json", same_mean)
    reporter.write_stage(
        "stage-03-same-mean.md",
        "Stage 3 — Same-Mean Control",
        f"""
All varying source families are centered to approximately zero mean, while the
constant control is exactly zero.

Standardized morphology-centroid distances from the constant control:

```json
{json.dumps(same_mean, indent=2)}
```

These distances are descriptive only. They ask whether time variation leaves a
morphological difference beyond the mean input level. Classification and
temporal-order controls provide the stronger tests later.
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 4 — TEMPORAL SHUFFLE POPULATIONS
    # -------------------------------------------------------------------------
    print("\n=== STAGE 4: TEMPORAL SHUFFLE CONTROL ===")
    shuffled_specs = build_specs(profile, args.seed, order_mode="shuffled")
    Xs, ys, _, cached_shuffled = dataset_from_specs(
        cache, shuffled_specs, "Stage 4: shuffled populations"
    )

    # Compare class-centroid displacement ordered -> shuffled.
    temporal_shift = {}
    sd_both = np.vstack([X, Xs]).std(axis=0)
    sd_both[sd_both < 1e-9] = 1.0
    for name in SIGNAL_NAMES:
        if name == "constant":
            continue
        a = X[y == name].mean(axis=0)
        b = Xs[ys == name].mean(axis=0)
        temporal_shift[name] = float(np.linalg.norm((a - b) / sd_both))

    reporter.write_json("stage-04-temporal-shuffle.json", temporal_shift)
    reporter.write_stage(
        "stage-04-temporal-shuffle.md",
        "Stage 4 — Destroy Temporal Order",
        f"""
For each nonconstant source, the exact sampled values are shuffled before
growth. This preserves the value distribution while destroying temporal order.

Standardized morphology-centroid shifts, ordered vs shuffled:

```json
{json.dumps(temporal_shift, indent=2)}
```

Cached shuffled runs reused: **{cached_shuffled}/{len(ys)}**

A nonzero descriptive shift is not enough by itself. Stage 7 asks whether
ordered and shuffled crystals can actually be distinguished on held-out runs.
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 5 — MORPHOLOGY METRICS
    # -------------------------------------------------------------------------
    print("\n=== STAGE 5: MORPHOLOGY METRICS ===")
    rows = [(label, feat) for label, feat in zip(y.tolist(), X)]
    metrics_fig = save_metric_distributions(rows, image_dir)
    centroid_dist = class_centroid_distances(X, y)

    reporter.write_json("stage-05-feature-distances.json", centroid_dist)
    reporter.write_stage(
        "stage-05-morphology.md",
        "Stage 5 — Stop Trusting the Pictures",
        f"""
Measured **{len(FEATURE_NAMES)}** morphology features per final crystal.

Feature set includes:
- area and perimeter
- compactness and roughness
- bounding-box aspect
- centroid offset
- radial statistics/profile
- angular profile
- six-fold angular harmonic
- boundary-radius variation

The measurements intentionally exclude the original signal values.

Figure: `{metrics_fig}`

Pairwise standardized class-centroid distances are saved in
`stage-05-feature-distances.json`.
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 6 — SOURCE RECOVERY
    # -------------------------------------------------------------------------
    print("\n=== STAGE 6: HELD-OUT SOURCE RECOVERY ===")
    source_result = classifier_result(X, y, args.seed + 500)
    cm_path = image_dir / "ch14-06-source-confusion.png"
    save_confusion(
        np.asarray(source_result["random_forest_confusion"]),
        source_result["labels"],
        "Recovering source family from final crystal morphology",
        cm_path,
    )

    acc_path = image_dir / "ch14-06-source-accuracy.png"
    save_accuracy_plot(
        {
            "Random forest": source_result["random_forest_accuracy"],
            "Logistic": source_result["logistic_accuracy"],
        },
        source_result["chance"],
        "Held-out source recovery",
        acc_path,
    )

    reporter.write_json("stage-06-source-recovery.json", source_result)
    reporter.write_stage(
        "stage-06-source-recovery.md",
        "Stage 6 — Can We Recover the Source?",
        f"""
Six-way chance accuracy is **{source_result['chance']:.3f}**.

Held-out results:
- Random forest: **{source_result['random_forest_accuracy']:.3f}**
- Logistic regression: **{source_result['logistic_accuracy']:.3f}**

Interpretation rule decided in advance:
source recovery supports the working hypothesis only if held-out performance is
materially above chance across more than one classifier and later robustness
checks do not immediately destroy it.

Figures:
- `{cm_path}`
- `{acc_path}`
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 7 — ORDERED VS SHUFFLED RECOVERY
    # -------------------------------------------------------------------------
    print("\n=== STAGE 7: ORDERED VS SHUFFLED RECOVERY ===")
    order_result = binary_order_test(cache, ordered_specs, args.seed + 700)
    order_cm_path = image_dir / "ch14-07-order-confusion.png"
    save_confusion(
        np.asarray(order_result["random_forest_confusion"]),
        order_result["labels"],
        "Can morphology distinguish ordered from shuffled histories?",
        order_cm_path,
    )
    order_acc_path = image_dir / "ch14-07-order-accuracy.png"
    save_accuracy_plot(
        {
            "Random forest": order_result["random_forest_accuracy"],
            "Logistic": order_result["logistic_accuracy"],
        },
        order_result["chance"],
        "Temporal-order recovery",
        order_acc_path,
    )

    reporter.write_json("stage-07-order-recovery.json", order_result)
    reporter.write_stage(
        "stage-07-order-recovery.md",
        "Stage 7 — Does Temporal Order Survive?",
        f"""
Binary chance accuracy is **{order_result['chance']:.3f}**.

Held-out ordered-vs-shuffled results:
- Random forest: **{order_result['random_forest_accuracy']:.3f}**
- Logistic regression: **{order_result['logistic_accuracy']:.3f}**

This is the stronger control because ordered and shuffled cases contain the
same source values but in different temporal order.

Figures:
- `{order_cm_path}`
- `{order_acc_path}`
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 8 — MODEST ROBUSTNESS TO FORCING STRENGTH
    # -------------------------------------------------------------------------
    print("\n=== STAGE 8: ROBUSTNESS SWEEP ===")
    robustness = {}
    rob_specs_total = []
    # Smaller independent dataset for each forcing scale.
    for scale in profile["robustness_levels"]:
        local_profile = dict(profile)
        local_profile["runs_per_class"] = profile["robustness_runs"]
        specs = build_specs(
            local_profile,
            args.seed + int(scale * 10_000) + 900_000_000,
            order_mode="ordered",
            forcing_scale=float(scale),
        )
        rob_specs_total.extend(specs)
        Xr, yr, _, _ = dataset_from_specs(
            cache, specs, f"Stage 8: forcing scale {scale:.2f}"
        )
        rr = classifier_result(Xr, yr, args.seed + int(scale * 1000))
        robustness[f"{scale:.2f}"] = {
            "random_forest_accuracy": rr["random_forest_accuracy"],
            "logistic_accuracy": rr["logistic_accuracy"],
            "chance": rr["chance"],
            "n_test": rr["n_test"],
        }

    rob_fig = image_dir / "ch14-08-robustness.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    scales = [float(x) for x in robustness.keys()]
    rf_vals = [robustness[k]["random_forest_accuracy"] for k in robustness]
    lr_vals = [robustness[k]["logistic_accuracy"] for k in robustness]
    chance = next(iter(robustness.values()))["chance"]
    ax.plot(scales, rf_vals, marker="o", label="Random forest")
    ax.plot(scales, lr_vals, marker="o", label="Logistic")
    ax.axhline(chance, linestyle="--", label=f"chance = {chance:.3f}")
    ax.set_xlabel("forcing scale")
    ax.set_ylabel("held-out source accuracy")
    ax.set_ylim(0, 1)
    ax.set_title("Source recovery under modest forcing-strength changes")
    ax.legend()
    fig.tight_layout()
    fig.savefig(rob_fig, dpi=180)
    plt.close(fig)

    reporter.write_json("stage-08-robustness.json", robustness)
    reporter.write_stage(
        "stage-08-robustness.md",
        "Stage 8 — Does the Effect Survive Modest Parameter Change?",
        f"""
The forcing amplitude is varied while the local growth rule remains otherwise
unchanged.

```json
{json.dumps(robustness, indent=2)}
```

Figure: `{rob_fig}`

This is not a universal robustness proof. It only asks whether source recovery
is a knife-edge effect of one forcing amplitude.
""",
    )

    # -------------------------------------------------------------------------
    # STAGE 9 — COALESCED VERDICT
    # -------------------------------------------------------------------------
    print("\n=== STAGE 9: COALESCED VERDICT ===")
    source_rf = source_result["random_forest_accuracy"]
    source_lr = source_result["logistic_accuracy"]
    source_chance = source_result["chance"]
    order_rf = order_result["random_forest_accuracy"]
    order_lr = order_result["logistic_accuracy"]

    # Deliberately transparent heuristic verdict, not a p-value.
    source_supported = (
        source_rf >= source_chance + 0.20
        and source_lr >= source_chance + 0.10
    )
    order_supported = (
        order_rf >= 0.65
        and order_lr >= 0.60
    )
    robust_above_chance = sum(
        1 for v in robustness.values()
        if v["random_forest_accuracy"] >= source_chance + 0.15
    )
    robustness_supported = robust_above_chance >= max(
        1, math.ceil(len(robustness) / 2)
    )

    if source_supported and order_supported and robustness_supported:
        verdict = "SUPPORTED_WITHIN_THIS_MODEL"
        bounded_claim = (
            "Within this specific digital-crystal model, final morphology "
            "contains recoverable information about the source process, "
            "including information about temporal ordering, and the effect "
            "survives modest changes in forcing strength."
        )
    elif source_supported:
        verdict = "PARTIALLY_SUPPORTED"
        bounded_claim = (
            "Within this model, source family is recoverable from final "
            "morphology, but stronger temporal-order and/or robustness tests "
            "did not all survive. The Digital Crystal idea remains useful but "
            "the stronger history-encoding interpretation is not yet earned."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        bounded_claim = (
            "This implementation did not establish reliable recovery of the "
            "source process from final morphology. The model or the Digital "
            "Crystal hypothesis must be revised rather than written up as a "
            "positive result."
        )

    final_summary = {
        "verdict": verdict,
        "bounded_claim": bounded_claim,
        "source_recovery": source_result,
        "temporal_order_recovery": order_result,
        "robustness": robustness,
        "model_params": asdict(ModelParams()),
        "feature_names": FEATURE_NAMES,
        "explicit_nonclaims": [
            "life",
            "learning",
            "adaptation",
            "agency",
            "selfhood",
            "biological memory",
            "universal digital-crystal theory",
        ],
    }

    reporter.write_json("ch14-summary.json", final_summary)
    reporter.write_stage(
        "stage-09-verdict.md",
        "Stage 9 — Experimental Verdict",
        f"""
**Verdict: `{verdict}`**

> {bounded_claim}

Primary held-out source recovery:
- chance: **{source_chance:.3f}**
- random forest: **{source_rf:.3f}**
- logistic regression: **{source_lr:.3f}**

Temporal-order recovery:
- chance: **0.500**
- random forest: **{order_rf:.3f}**
- logistic regression: **{order_lr:.3f}**

Robustness forcing levels above the predeclared RF margin:
**{robust_above_chance}/{len(robustness)}**

The verdict logic is intentionally simple and printed in the script. It is a
book-development gate, not a formal statistical theorem.
""",
    )

    metadata["finished_at_unix"] = time.time()
    metadata["final_verdict"] = verdict
    full_report = reporter.write_final(metadata)

    print("\n" + "=" * 78)
    print("DIGITAL CRYSTAL EXPERIMENT COMPLETE")
    print("=" * 78)
    print(f"Verdict: {verdict}")
    print(bounded_claim)
    print()
    print(f"SQLite cache:  {db_path}")
    print(f"Full report:   {full_report}")
    print(f"Summary JSON:  {report_dir / 'ch14-summary.json'}")
    print(f"Figures:       {image_dir}")
    print("=" * 78)

    cache.close()


if __name__ == "__main__":
    main()
