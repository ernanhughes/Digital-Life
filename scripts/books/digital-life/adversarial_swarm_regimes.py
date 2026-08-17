from __future__ import annotations

"""
Digital Life — Experiment 2: dynamical-regime persistence

Question
--------
The first adversarial swarm experiment asked whether a damaged system returned
to one pre-intervention visible macrostate. Long runs showed that even the
untouched control can move far from that reference. This experiment therefore
changes the question:

    Does the swarm persist as a distribution / dynamical regime rather than
    as one particular visible form?

And, after intervention:

    Does damage change the distribution of macrostates the system visits?

This script deliberately reuses the exact same microscopic swarm and
interventions from:

    adversarial_swarm_persistence.py

so that Experiment 2 changes the *measurement*, not the world.

Primary analyses
----------------
1. CONTROL SELF-DRIFT
   Split the untouched control trajectory into time blocks and measure how far
   each block's macrostate distribution is from the others.

2. INTERVENTION DISTRIBUTION SHIFT
   Compare the late post-intervention macrostate distribution of:
       - material damage
       - organizational damage
   against the matched control distribution from the same seed.

3. DESCRIPTIVE REGIME OCCUPANCY
   Fit a small k-means partition only to pooled control states, then ask how
   often each branch visits those descriptive regions of macrostate space.
   These clusters are visualization aids, NOT claimed natural kinds.

4. PCA VISUALIZATION
   Project standardized macrostate features into the first two control-derived
   principal components.

Interpretation discipline
-------------------------
A branch does NOT "fail to persist" merely because it does not return to a
single snapshot. Stronger evidence of intervention-induced change is:

    branch-to-control distribution distance
    >
    ordinary control-to-control temporal drift

Dependencies
------------
    pip install numpy scipy matplotlib

Run
---
    # Put this file beside adversarial_swarm_persistence.py
    python scripts/books/digital-life/adversarial_swarm_regimes.py

Quick smoke test:
    python scripts/books/digital-life/adversarial_swarm_regimes.py --quick
"""

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist, pdist
from scipy.special import rel_entr

import adversarial_swarm_persistence as swarm


EPS = 1e-12


# =====================================================================
# Configuration
# =====================================================================


@dataclass(frozen=True)
class RegimeConfig:
    particles: int = 256
    burn_in: int = 10_000
    post_steps: int = 12_000
    sample_stride: int = 20

    damage_fraction: float = 0.30
    damage_scale: float = 2.5
    rewire_fraction: float = 0.30

    replicates: int = 8
    base_seed: int = 20260817

    control_blocks: int = 6
    regimes: int = 4
    kmeans_iterations: int = 100

    max_energy_samples: int = 400
    late_fraction: float = 0.50


FEATURE_NAMES = [
    "log_radius_gyration",
    "log_anisotropy",
    "mean_speed",
    "radial_q10",
    "radial_q25",
    "radial_q50",
    "radial_q75",
    "radial_q90",
    "pair_q10",
    "pair_q25",
    "pair_q50",
    "pair_q75",
    "pair_q90",
    "friend_q25",
    "friend_q50",
    "friend_q75",
    "enemy_q25",
    "enemy_q50",
    "enemy_q75",
]


# =====================================================================
# Macrostate features
# =====================================================================


def _quantiles(x: np.ndarray, qs: Iterable[float]) -> list[float]:
    x = np.asarray(x, dtype=np.float64)
    return [float(v) for v in np.quantile(x, list(qs))]


def macrostate_features(state: swarm.SwarmState) -> np.ndarray:
    """
    A scale-aware description of the visible and relational macrostate.

    Important:
    - no material_id is included;
    - no exact friend/enemy node identity is included;
    - features describe geometry/dynamics, not the implementation labels.
    """
    pos = state.position
    rg = max(swarm.radius_of_gyration(pos), EPS)

    radial = swarm.radial_distances(pos) / rg
    pair = swarm.pairwise_distances(pos) / rg

    friend_dist = np.linalg.norm(
        pos[state.friend] - pos,
        axis=1,
    ) / rg
    enemy_dist = np.linalg.norm(
        pos[state.enemy] - pos,
        axis=1,
    ) / rg

    values = [
        math.log(rg + EPS),
        math.log(swarm.anisotropy(pos) + EPS),
        swarm.mean_speed(state),
        *_quantiles(radial, (0.10, 0.25, 0.50, 0.75, 0.90)),
        *_quantiles(pair, (0.10, 0.25, 0.50, 0.75, 0.90)),
        *_quantiles(friend_dist, (0.25, 0.50, 0.75)),
        *_quantiles(enemy_dist, (0.25, 0.50, 0.75)),
    ]

    arr = np.asarray(values, dtype=np.float64)
    if len(arr) != len(FEATURE_NAMES):
        raise RuntimeError("Feature-name mismatch")
    return arr


# =====================================================================
# Trajectory generation
# =====================================================================


def make_world_config(cfg: RegimeConfig) -> swarm.Config:
    # Use Experiment 1's microscopic defaults exactly, changing only duration
    # and requested intervention strengths.
    return swarm.Config(
        particles=cfg.particles,
        burn_in=cfg.burn_in,
        reference_window=min(1_000, max(100, cfg.burn_in // 5)),
        post_steps=cfg.post_steps,
        sample_stride=cfg.sample_stride,
        damage_fraction=cfg.damage_fraction,
        damage_scale=cfg.damage_scale,
        rewire_fraction=cfg.rewire_fraction,
    )


def run_replicate(
    cfg: RegimeConfig,
    seed: int,
) -> tuple[list[dict], dict]:
    world_cfg = make_world_config(cfg)
    rng = np.random.default_rng(seed)

    state = swarm.make_state(world_cfg, rng)

    # Burn in with no measurement claim that a stable point has been reached.
    for _ in range(cfg.burn_in):
        swarm.step(state, world_cfg)

    checkpoint = state.clone()

    branches = {
        "control": checkpoint.clone(),
        "material_damage": checkpoint.clone(),
        "organizational_damage": checkpoint.clone(),
    }

    swarm.material_damage(
        branches["material_damage"],
        world_cfg,
        np.random.default_rng(seed + 10_001),
    )
    swarm.organizational_damage(
        branches["organizational_damage"],
        world_cfg,
        np.random.default_rng(seed + 20_001),
    )

    rows: list[dict] = []

    def record(branch: str, t: int) -> None:
        state_now = branches[branch]
        feat = macrostate_features(state_now)

        row = {
            "seed": seed,
            "branch": branch,
            "step": t,
            "graph_similarity": (
                1.0
                if branch != "organizational_damage"
                else float(
                    0.5
                    * (
                        np.mean(state_now.friend == checkpoint.friend)
                        + np.mean(state_now.enemy == checkpoint.enemy)
                    )
                )
            ),
        }
        row.update(
            {
                name: float(value)
                for name, value in zip(FEATURE_NAMES, feat, strict=True)
            }
        )
        rows.append(row)

    for name in branches:
        record(name, 0)

    for t in range(1, cfg.post_steps + 1):
        for state_now in branches.values():
            swarm.step(state_now, world_cfg)

        if t % cfg.sample_stride == 0 or t == cfg.post_steps:
            for name in branches:
                record(name, t)

    meta = {
        "seed": seed,
        "samples_per_branch": sum(
            1 for r in rows if r["branch"] == "control"
        ),
        "final_graph_similarity": {
            name: float(
                0.5
                * (
                    np.mean(branch.friend == checkpoint.friend)
                    + np.mean(branch.enemy == checkpoint.enemy)
                )
            )
            for name, branch in branches.items()
        },
    }
    return rows, meta


# =====================================================================
# Standardization / PCA
# =====================================================================


def rows_to_matrix(rows: list[dict]) -> np.ndarray:
    return np.asarray(
        [[r[name] for name in FEATURE_NAMES] for r in rows],
        dtype=np.float64,
    )


@dataclass
class Standardizer:
    mean: np.ndarray
    scale: np.ndarray

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) / self.scale


def fit_standardizer(x: np.ndarray) -> Standardizer:
    mean = np.mean(x, axis=0)
    scale = np.std(x, axis=0)
    scale = np.where(scale < 1e-9, 1.0, scale)
    return Standardizer(mean=mean, scale=scale)


@dataclass
class PCAProjection:
    mean: np.ndarray
    components: np.ndarray
    explained_variance_ratio: np.ndarray

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) @ self.components.T


def fit_pca(x: np.ndarray, n_components: int = 2) -> PCAProjection:
    mean = np.mean(x, axis=0)
    centred = x - mean
    _, s, vt = np.linalg.svd(centred, full_matrices=False)

    variances = (s * s) / max(len(x) - 1, 1)
    total = float(np.sum(variances))
    ratio = variances / total if total > EPS else np.zeros_like(variances)

    return PCAProjection(
        mean=mean,
        components=vt[:n_components],
        explained_variance_ratio=ratio[:n_components],
    )


# =====================================================================
# Distribution distances
# =====================================================================


def deterministic_subsample(
    x: np.ndarray,
    max_n: int,
) -> np.ndarray:
    if len(x) <= max_n:
        return x
    idx = np.linspace(0, len(x) - 1, max_n, dtype=np.int64)
    return x[idx]


def energy_distance_mv(
    x: np.ndarray,
    y: np.ndarray,
    max_n: int = 400,
) -> float:
    """
    Multivariate energy distance:

        2 E||X-Y|| - E||X-X'|| - E||Y-Y'||

    Uses deterministic subsampling for bounded runtime.
    """
    x = deterministic_subsample(np.asarray(x), max_n)
    y = deterministic_subsample(np.asarray(y), max_n)

    cross = float(np.mean(cdist(x, y, metric="euclidean")))

    xx = (
        0.0
        if len(x) < 2
        else float(2.0 * np.sum(pdist(x)) / (len(x) ** 2))
    )
    yy = (
        0.0
        if len(y) < 2
        else float(2.0 * np.sum(pdist(y)) / (len(y) ** 2))
    )

    return max(0.0, 2.0 * cross - xx - yy)


def split_blocks(x: np.ndarray, n_blocks: int) -> list[np.ndarray]:
    n_blocks = max(2, min(n_blocks, len(x)))
    return [part for part in np.array_split(x, n_blocks) if len(part) > 0]


def control_drift_rows(
    standardized_rows_by_seed: dict[int, dict[str, np.ndarray]],
    cfg: RegimeConfig,
) -> list[dict]:
    out: list[dict] = []

    for seed, branches in standardized_rows_by_seed.items():
        control = branches["control"]
        blocks = split_blocks(control, cfg.control_blocks)

        adjacent = []
        for i in range(len(blocks) - 1):
            d = energy_distance_mv(
                blocks[i],
                blocks[i + 1],
                cfg.max_energy_samples,
            )
            adjacent.append(d)
            out.append(
                {
                    "seed": seed,
                    "comparison": "adjacent",
                    "block_a": i,
                    "block_b": i + 1,
                    "energy_distance": d,
                }
            )

        first_last = energy_distance_mv(
            blocks[0],
            blocks[-1],
            cfg.max_energy_samples,
        )
        out.append(
            {
                "seed": seed,
                "comparison": "first_last",
                "block_a": 0,
                "block_b": len(blocks) - 1,
                "energy_distance": first_last,
            }
        )

        # All pairwise blocks give the baseline range of ordinary control drift.
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                d = energy_distance_mv(
                    blocks[i],
                    blocks[j],
                    cfg.max_energy_samples,
                )
                out.append(
                    {
                        "seed": seed,
                        "comparison": "all_pairs",
                        "block_a": i,
                        "block_b": j,
                        "energy_distance": d,
                    }
                )

    return out


def late_slice(x: np.ndarray, late_fraction: float) -> np.ndarray:
    start = int(round(len(x) * (1.0 - late_fraction)))
    start = max(0, min(start, len(x) - 1))
    return x[start:]


def intervention_shift_rows(
    standardized_rows_by_seed: dict[int, dict[str, np.ndarray]],
    cfg: RegimeConfig,
) -> list[dict]:
    out: list[dict] = []

    for seed, branches in standardized_rows_by_seed.items():
        control = late_slice(branches["control"], cfg.late_fraction)
        control_blocks = split_blocks(control, max(2, cfg.control_blocks // 2))

        baseline_distances = []
        for i in range(len(control_blocks)):
            for j in range(i + 1, len(control_blocks)):
                baseline_distances.append(
                    energy_distance_mv(
                        control_blocks[i],
                        control_blocks[j],
                        cfg.max_energy_samples,
                    )
                )

        baseline = float(np.median(baseline_distances))
        baseline = max(baseline, EPS)

        for branch in ("material_damage", "organizational_damage"):
            treatment = late_slice(
                branches[branch],
                cfg.late_fraction,
            )
            d = energy_distance_mv(
                treatment,
                control,
                cfg.max_energy_samples,
            )
            out.append(
                {
                    "seed": seed,
                    "branch": branch,
                    "late_energy_distance_to_control": d,
                    "control_baseline_drift_median": baseline,
                    "distance_over_baseline": d / baseline,
                }
            )

    return out


# =====================================================================
# Descriptive k-means regimes
# =====================================================================


def kmeans(
    x: np.ndarray,
    k: int,
    iterations: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Small deterministic-enough k-means implementation.

    Initialization uses farthest-point seeding from one RNG-selected point.
    The clusters are descriptive partitions only.
    """
    rng = np.random.default_rng(seed)
    n = len(x)
    if k < 1 or k > n:
        raise ValueError("Invalid k")

    first = int(rng.integers(0, n))
    centres = [x[first].copy()]

    for _ in range(1, k):
        d2 = np.min(
            np.stack(
                [
                    np.sum((x - c) ** 2, axis=1)
                    for c in centres
                ],
                axis=1,
            ),
            axis=1,
        )
        next_idx = int(np.argmax(d2))
        centres.append(x[next_idx].copy())

    centres_arr = np.asarray(centres)

    labels = np.zeros(n, dtype=np.int64)

    for _ in range(iterations):
        dist = cdist(x, centres_arr)
        new_labels = np.argmin(dist, axis=1)

        if np.array_equal(new_labels, labels):
            labels = new_labels
            break
        labels = new_labels

        new_centres = centres_arr.copy()
        for j in range(k):
            members = x[labels == j]
            if len(members):
                new_centres[j] = np.mean(members, axis=0)

        if np.allclose(new_centres, centres_arr):
            centres_arr = new_centres
            break
        centres_arr = new_centres

    return centres_arr, labels


def assign_centres(x: np.ndarray, centres: np.ndarray) -> np.ndarray:
    return np.argmin(cdist(x, centres), axis=1)


def occupancy(labels: np.ndarray, k: int) -> np.ndarray:
    counts = np.bincount(labels, minlength=k).astype(np.float64)
    return counts / max(float(np.sum(counts)), 1.0)


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64) + EPS
    q = np.asarray(q, dtype=np.float64) + EPS
    p /= np.sum(p)
    q /= np.sum(q)
    m = 0.5 * (p + q)
    # rel_entr gives p * log(p/m)
    return float(
        0.5 * np.sum(rel_entr(p, m))
        + 0.5 * np.sum(rel_entr(q, m))
    )


def regime_rows(
    standardized_rows_by_seed: dict[int, dict[str, np.ndarray]],
    centres: np.ndarray,
    cfg: RegimeConfig,
) -> list[dict]:
    out: list[dict] = []

    for seed, branches in standardized_rows_by_seed.items():
        control_late = late_slice(
            branches["control"],
            cfg.late_fraction,
        )
        control_labels = assign_centres(control_late, centres)
        control_occ = occupancy(control_labels, cfg.regimes)

        for branch, x in branches.items():
            x_late = late_slice(x, cfg.late_fraction)
            labels = assign_centres(x_late, centres)
            occ = occupancy(labels, cfg.regimes)
            js = js_divergence(occ, control_occ)

            for regime in range(cfg.regimes):
                out.append(
                    {
                        "seed": seed,
                        "branch": branch,
                        "regime": regime,
                        "occupancy": float(occ[regime]),
                        "control_occupancy": float(
                            control_occ[regime]
                        ),
                        "js_divergence_from_control": js,
                    }
                )

    return out


# =====================================================================
# Aggregate summaries
# =====================================================================


def summarize_shifts(rows: list[dict]) -> list[dict]:
    out = []
    branches = sorted({r["branch"] for r in rows})

    for branch in branches:
        subset = [r for r in rows if r["branch"] == branch]
        d = np.asarray(
            [r["late_energy_distance_to_control"] for r in subset]
        )
        ratios = np.asarray(
            [r["distance_over_baseline"] for r in subset]
        )

        out.append(
            {
                "branch": branch,
                "replicates": len(subset),
                "mean_energy_distance_to_control": float(np.mean(d)),
                "sd_energy_distance_to_control": float(np.std(d, ddof=1))
                if len(d) > 1 else 0.0,
                "median_distance_over_control_drift": float(
                    np.median(ratios)
                ),
                "mean_distance_over_control_drift": float(
                    np.mean(ratios)
                ),
                "fraction_replicates_above_control_drift": float(
                    np.mean(ratios > 1.0)
                ),
                "fraction_replicates_above_2x_control_drift": float(
                    np.mean(ratios > 2.0)
                ),
            }
        )

    return out


def summarize_control_drift(rows: list[dict]) -> dict:
    adjacent = np.asarray(
        [
            r["energy_distance"]
            for r in rows
            if r["comparison"] == "adjacent"
        ],
        dtype=np.float64,
    )
    first_last = np.asarray(
        [
            r["energy_distance"]
            for r in rows
            if r["comparison"] == "first_last"
        ],
        dtype=np.float64,
    )
    all_pairs = np.asarray(
        [
            r["energy_distance"]
            for r in rows
            if r["comparison"] == "all_pairs"
        ],
        dtype=np.float64,
    )

    return {
        "adjacent_block_distance_mean": float(np.mean(adjacent)),
        "adjacent_block_distance_median": float(np.median(adjacent)),
        "all_control_block_pairs_mean": float(np.mean(all_pairs)),
        "all_control_block_pairs_median": float(np.median(all_pairs)),
        "first_last_distance_mean": float(np.mean(first_last)),
        "first_last_distance_median": float(np.median(first_last)),
        "first_last_over_adjacent_median": float(
            np.median(first_last)
            / max(float(np.median(adjacent)), EPS)
        ),
    }


# =====================================================================
# CSV / JSON
# =====================================================================


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


# =====================================================================
# Figures
# =====================================================================


def plot_control_drift(
    path: Path,
    drift_rows: list[dict],
) -> None:
    by_seed: dict[int, dict[str, list[float]]] = {}

    for row in drift_rows:
        by_seed.setdefault(
            int(row["seed"]),
            {"adjacent": [], "first_last": []},
        )
        if row["comparison"] in ("adjacent", "first_last"):
            by_seed[int(row["seed"])][row["comparison"]].append(
                float(row["energy_distance"])
            )

    seeds = sorted(by_seed)
    adjacent = [
        float(np.median(by_seed[s]["adjacent"]))
        for s in seeds
    ]
    first_last = [
        float(np.median(by_seed[s]["first_last"]))
        for s in seeds
    ]

    x = np.arange(len(seeds))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, adjacent, width, label="adjacent blocks")
    ax.bar(x + width / 2, first_last, width, label="first vs last")
    ax.set_xlabel("Replicate")
    ax.set_ylabel("Multivariate energy distance")
    ax.set_title("Untouched swarm: ordinary temporal drift")
    ax.set_xticks(x)
    ax.set_xticklabels([str(i + 1) for i in range(len(seeds))])
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_distribution_shift(
    path: Path,
    shift_rows: list[dict],
) -> None:
    branches = ["material_damage", "organizational_damage"]

    fig, ax = plt.subplots(figsize=(9, 6))

    for i, branch in enumerate(branches):
        vals = [
            float(r["distance_over_baseline"])
            for r in shift_rows
            if r["branch"] == branch
        ]
        x = np.full(len(vals), i, dtype=float)
        ax.scatter(x, vals, s=45)
        ax.hlines(
            np.median(vals),
            i - 0.20,
            i + 0.20,
            linewidth=3,
        )

    ax.axhline(
        1.0,
        linestyle="--",
        linewidth=1.5,
        label="ordinary control drift",
    )
    ax.set_xticks(range(len(branches)))
    ax.set_xticklabels(
        [b.replace("_", " ") for b in branches]
    )
    ax.set_ylabel("Distance to control / ordinary control drift")
    ax.set_title(
        "Does intervention move the swarm into a different macrostate distribution?"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_pca(
    path: Path,
    rows: list[dict],
    standardized_all: np.ndarray,
    pca: PCAProjection,
) -> None:
    projected = pca.transform(standardized_all)

    branches = np.asarray([r["branch"] for r in rows])
    steps = np.asarray([r["step"] for r in rows])
    late_threshold = np.quantile(steps[branches == "control"], 0.50)

    fig, ax = plt.subplots(figsize=(10, 7))

    for branch in (
        "control",
        "material_damage",
        "organizational_damage",
    ):
        mask = (branches == branch) & (steps >= late_threshold)
        pts = projected[mask]
        if len(pts) > 1500:
            idx = np.linspace(
                0, len(pts) - 1, 1500, dtype=np.int64
            )
            pts = pts[idx]

        ax.scatter(
            pts[:, 0],
            pts[:, 1],
            s=10,
            alpha=0.35,
            label=branch.replace("_", " "),
        )

    evr = pca.explained_variance_ratio
    ax.set_xlabel(f"PC1 ({evr[0] * 100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({evr[1] * 100:.1f}% variance)")
    ax.set_title("Late trajectories through macrostate space")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_regime_occupancy(
    path: Path,
    regime_rows_data: list[dict],
    cfg: RegimeConfig,
) -> None:
    branches = [
        "control",
        "material_damage",
        "organizational_damage",
    ]

    means = {}
    for branch in branches:
        vals = []
        for regime in range(cfg.regimes):
            occ = [
                float(r["occupancy"])
                for r in regime_rows_data
                if r["branch"] == branch
                and int(r["regime"]) == regime
            ]
            vals.append(float(np.mean(occ)))
        means[branch] = vals

    x = np.arange(cfg.regimes)
    width = 0.24

    fig, ax = plt.subplots(figsize=(10, 6))
    offsets = np.linspace(
        -width,
        width,
        len(branches),
    )

    for offset, branch in zip(offsets, branches, strict=True):
        ax.bar(
            x + offset,
            means[branch],
            width,
            label=branch.replace("_", " "),
        )

    ax.set_xlabel("Descriptive macrostate region")
    ax.set_ylabel("Mean late occupancy")
    ax.set_title(
        "Which parts of control-defined macrostate space are visited?"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"R{i}" for i in range(cfg.regimes)]
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


# =====================================================================
# Console report
# =====================================================================


def print_report(
    drift_summary: dict,
    shift_summary: list[dict],
) -> None:
    print()
    print("DYNAMICAL-REGIME PERSISTENCE EXPERIMENT")
    print("=" * 76)

    print()
    print("Untouched control self-drift")
    print("-" * 76)
    print(
        "median adjacent-block distance : "
        f"{drift_summary['adjacent_block_distance_median']:.4f}"
    )
    print(
        "median first-to-last distance  : "
        f"{drift_summary['first_last_distance_median']:.4f}"
    )
    print(
        "first/last ÷ adjacent median   : "
        f"{drift_summary['first_last_over_adjacent_median']:.3f}"
    )

    print()
    print(
        f"{'branch':24s} {'energy':>10s} "
        f"{'÷ drift':>10s} {'> drift':>10s} {'> 2x':>10s}"
    )
    print("-" * 76)

    for row in shift_summary:
        print(
            f"{row['branch']:24s} "
            f"{row['mean_energy_distance_to_control']:10.4f} "
            f"{row['median_distance_over_control_drift']:10.3f} "
            f"{row['fraction_replicates_above_control_drift']:10.3f} "
            f"{row['fraction_replicates_above_2x_control_drift']:10.3f}"
        )

    print()
    print("Reading the result:")
    print(
        "  ratio ~ 1   -> branch/control separation is comparable to"
    )
    print(
        "               ordinary temporal drift within the untouched control"
    )
    print(
        "  ratio >> 1  -> intervention pushes the system into a distribution"
    )
    print(
        "               of macrostates farther away than ordinary control drift"
    )
    print()
    print(
        "The descriptive regime clusters are visualization aids only."
    )
    print(
        "Do not interpret k-means region labels as natural individuals or"
    )
    print(
        "intrinsic biological states."
    )


# =====================================================================
# CLI / main
# =====================================================================


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Measure persistence as a dynamical macrostate distribution "
            "rather than return to one snapshot."
        )
    )

    p.add_argument("--particles", type=int, default=256)
    p.add_argument("--burn-in", type=int, default=10_000)
    p.add_argument("--post-steps", type=int, default=12_000)
    p.add_argument("--sample-stride", type=int, default=20)
    p.add_argument("--replicates", type=int, default=8)
    p.add_argument("--seed", type=int, default=20260817)

    p.add_argument("--damage-fraction", type=float, default=0.30)
    p.add_argument("--damage-scale", type=float, default=2.5)
    p.add_argument("--rewire-fraction", type=float, default=0.30)

    p.add_argument("--control-blocks", type=int, default=6)
    p.add_argument("--regimes", type=int, default=4)
    p.add_argument("--late-fraction", type=float, default=0.50)

    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/digital-life/adversarial-swarm-regimes"
        ),
    )
    p.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )

    p.add_argument(
        "--quick",
        action="store_true",
        help="Small smoke test; not suitable for book claims.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.quick:
        args.particles = min(args.particles, 96)
        args.burn_in = min(args.burn_in, 1_500)
        args.post_steps = min(args.post_steps, 2_000)
        args.replicates = min(args.replicates, 2)
        args.control_blocks = min(args.control_blocks, 4)

    if not (0.10 <= args.late_fraction <= 1.0):
        raise ValueError("--late-fraction must be in [0.10, 1.0]")

    cfg = RegimeConfig(
        particles=args.particles,
        burn_in=args.burn_in,
        post_steps=args.post_steps,
        sample_stride=args.sample_stride,
        damage_fraction=args.damage_fraction,
        damage_scale=args.damage_scale,
        rewire_fraction=args.rewire_fraction,
        replicates=args.replicates,
        base_seed=args.seed,
        control_blocks=args.control_blocks,
        regimes=args.regimes,
        late_fraction=args.late_fraction,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    trial_meta: list[dict] = []

    for replicate in range(cfg.replicates):
        seed = cfg.base_seed + replicate * 100_003
        print(
            f"[{replicate + 1}/{cfg.replicates}] "
            f"running seed={seed} ..."
        )

        rows, meta = run_replicate(cfg, seed)
        all_rows.extend(rows)
        trial_meta.append(meta)

    # Standardizer is fit ONLY from control states, across all seeds.
    control_rows = [
        r for r in all_rows if r["branch"] == "control"
    ]
    control_raw = rows_to_matrix(control_rows)

    standardizer = fit_standardizer(control_raw)

    standardized_by_seed: dict[
        int, dict[str, np.ndarray]
    ] = {}

    for seed in sorted({int(r["seed"]) for r in all_rows}):
        standardized_by_seed[seed] = {}
        for branch in (
            "control",
            "material_damage",
            "organizational_damage",
        ):
            subset = [
                r for r in all_rows
                if int(r["seed"]) == seed
                and r["branch"] == branch
            ]
            x = rows_to_matrix(subset)
            standardized_by_seed[seed][branch] = (
                standardizer.transform(x)
            )

    control_standardized = standardizer.transform(control_raw)

    drift_rows = control_drift_rows(
        standardized_by_seed,
        cfg,
    )
    shift_rows = intervention_shift_rows(
        standardized_by_seed,
        cfg,
    )

    drift_summary = summarize_control_drift(drift_rows)
    shift_summary = summarize_shifts(shift_rows)

    # Descriptive regime partition is fit ONLY to pooled control states.
    centres, _ = kmeans(
        control_standardized,
        cfg.regimes,
        cfg.kmeans_iterations,
        cfg.base_seed,
    )
    regime_rows_data = regime_rows(
        standardized_by_seed,
        centres,
        cfg,
    )

    pca = fit_pca(control_standardized, 2)

    all_raw = rows_to_matrix(all_rows)
    standardized_all = standardizer.transform(all_raw)

    # Write PCA coordinates into the main timeseries output.
    projected_all = pca.transform(standardized_all)
    for row, pc in zip(all_rows, projected_all, strict=True):
        row["pc1"] = float(pc[0])
        row["pc2"] = float(pc[1])

    write_csv(
        args.output_dir / "macrostate_timeseries.csv",
        all_rows,
    )
    write_csv(
        args.output_dir / "control_block_drift.csv",
        drift_rows,
    )
    write_csv(
        args.output_dir / "intervention_shift.csv",
        shift_rows,
    )
    write_csv(
        args.output_dir / "distribution_summary.csv",
        shift_summary,
    )
    write_csv(
        args.output_dir / "regime_occupancy.csv",
        regime_rows_data,
    )

    metadata = {
        "experiment": "adversarial_swarm_regimes",
        "claim_status": "EXPERIMENTAL",
        "question": (
            "Does persistence reside in a distribution of macrostates, "
            "and do interventions change that distribution beyond ordinary "
            "control self-drift?"
        ),
        "config": asdict(cfg),
        "feature_names": FEATURE_NAMES,
        "standardization": {
            "fit_on": "pooled control states only",
            "mean": standardizer.mean.tolist(),
            "scale": standardizer.scale.tolist(),
        },
        "pca": {
            "fit_on": "pooled standardized control states only",
            "components": pca.components.tolist(),
            "explained_variance_ratio": (
                pca.explained_variance_ratio.tolist()
            ),
        },
        "descriptive_regimes": {
            "method": "k-means",
            "fit_on": "pooled standardized control states only",
            "k": cfg.regimes,
            "centres": centres.tolist(),
            "warning": (
                "These regions are descriptive partitions, not claimed "
                "natural kinds or intrinsic states."
            ),
        },
        "control_drift_summary": drift_summary,
        "intervention_shift_summary": shift_summary,
        "trials": trial_meta,
        "interpretation": [
            (
                "A branch-to-control distance comparable to ordinary "
                "control block drift does not establish a changed regime."
            ),
            (
                "A branch-to-control distance consistently larger than "
                "ordinary control drift supports an intervention-induced "
                "change in macrostate distribution."
            ),
            (
                "This experiment does not define persistence as return "
                "to one pre-intervention snapshot."
            ),
        ],
    }

    (args.output_dir / "run.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    plot_control_drift(
        args.figure_dir / "adversarial-swarm-control-drift.png",
        drift_rows,
    )
    plot_distribution_shift(
        args.figure_dir
        / "adversarial-swarm-distribution-shift.png",
        shift_rows,
    )
    plot_pca(
        args.figure_dir / "adversarial-swarm-regime-pca.png",
        all_rows,
        standardized_all,
        pca,
    )
    plot_regime_occupancy(
        args.figure_dir
        / "adversarial-swarm-regime-occupancy.png",
        regime_rows_data,
        cfg,
    )

    print_report(drift_summary, shift_summary)

    print()
    print("Outputs:")
    for name in (
        "macrostate_timeseries.csv",
        "control_block_drift.csv",
        "intervention_shift.csv",
        "distribution_summary.csv",
        "regime_occupancy.csv",
        "run.json",
    ):
        print(f"  {args.output_dir / name}")

    for name in (
        "adversarial-swarm-control-drift.png",
        "adversarial-swarm-distribution-shift.png",
        "adversarial-swarm-regime-pca.png",
        "adversarial-swarm-regime-occupancy.png",
    ):
        print(f"  {args.figure_dir / name}")


if __name__ == "__main__":
    main()
