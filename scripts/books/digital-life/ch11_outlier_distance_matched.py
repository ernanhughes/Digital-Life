from __future__ import annotations

"""
Chapter 11 — Outlier distance-matched causal coherence.

ANALYSIS ONLY.
Uses the existing SQLite cache. No CA simulation is rerun.

Research question
=================

Does membership in the same recent-c2 causal family predict stronger
pair-excluded motion coherence AFTER controlling for spatial context?

We match same-family and different-family pairs on:

    * time bin
    * spatial distance bin
    * local density bin

Then compare their pair-excluded residual velocity alignment.

This is stronger than simply plotting same-family vs different-family means,
because same-family pairs in the current run are much more spatially compact.

Expected database
=================

    data/digital-life/outlier.sqlite3

Expected prior tables:

    experiment_runs
    motion_points
    c2_recent_ancestor
    analysis_results

Output
======

    static/images/books/digital-life/
        ch11-outlier-distance-matched-coherence.png
        ch11-outlier-distance-matched-effect-by-distance.png

Numerical result is cached in analysis_results.
"""

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    def tqdm(iterable=None, **kwargs):
        return iterable if iterable is not None else range(kwargs.get("total", 0))


DEFAULT_DB = Path("data/digital-life/outlier.sqlite3")
OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# SQLite
# =====================================================================

def connect_db(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(
            f"SQLite cache not found: {path}\n"
            "Run the previous chapter-11 cache scripts first."
        )

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA busy_timeout=60000")
    conn.execute("PRAGMA temp_store=MEMORY")
    return conn


def latest_complete_run(conn: sqlite3.Connection, requested: int | None) -> int:
    if requested is not None:
        row = conn.execute(
            "SELECT id FROM experiment_runs WHERE id=? AND status='complete'",
            (requested,),
        ).fetchone()
        if not row:
            raise RuntimeError(f"run_id={requested} is not complete")
        return requested

    row = conn.execute(
        """
        SELECT id
        FROM experiment_runs
        WHERE status='complete'
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    if not row:
        raise RuntimeError("No completed cached Outlier run found")

    return int(row[0])


def run_metadata(conn: sqlite3.Connection, run_id: int) -> dict:
    row = conn.execute(
        "SELECT size, generations FROM experiment_runs WHERE id=?",
        (run_id,),
    ).fetchone()

    if not row:
        raise RuntimeError(f"Unknown run_id={run_id}")

    return {
        "size": int(row[0]),
        "generations": int(row[1]),
    }


# =====================================================================
# Motion loading
# =====================================================================

def load_motion_by_time(conn: sqlite3.Connection, run_id: int):
    by_time: dict[int, list[dict]] = defaultdict(list)

    cursor = conn.execute(
        """
        SELECT
            m.time,
            m.uid,
            m.row,
            m.col,
            m.velocity_row,
            m.velocity_col,
            a.ancestor_uid,
            a.ambiguous
        FROM motion_points AS m
        LEFT JOIN c2_recent_ancestor AS a
          ON a.run_id=m.run_id
         AND a.uid=m.uid
        WHERE m.run_id=?
        ORDER BY m.time, m.track_id, m.seq
        """,
        (run_id,),
    )

    total = 0
    labelled = 0

    for time, uid, row, col, vr, vc, ancestor, ambiguous in cursor:
        velocity = np.array([vr, vc], dtype=np.float64)

        if np.linalg.norm(velocity) <= 1e-12:
            continue

        family = None

        if not ambiguous and ancestor is not None:
            family = int(ancestor)
            labelled += 1

        by_time[int(time)].append(
            {
                "uid": int(uid),
                "position": np.array([row, col], dtype=np.float64),
                "velocity": velocity,
                "family": family,
            }
        )
        total += 1

    print(
        f"motion observations: {total:,} | "
        f"known recent-c2 family: {labelled:,} ({labelled / max(total,1):.1%})"
    )

    return by_time


# =====================================================================
# Geometry / residual helpers
# =====================================================================

def unit_vectors(vectors: np.ndarray):
    norms = np.linalg.norm(vectors, axis=1)
    valid = norms > 1e-12

    units = np.zeros_like(vectors)
    units[valid] = vectors[valid] / norms[valid, None]

    return units, valid


def periodic_delta(a: np.ndarray, b: np.ndarray, world_size: float):
    delta = b - a
    return (delta + world_size / 2.0) % world_size - world_size / 2.0


def sample_pairs(
    pairs: np.ndarray,
    max_pairs: int,
    rng: np.random.Generator,
):
    if len(pairs) <= max_pairs:
        return pairs

    chosen = rng.choice(
        len(pairs),
        size=max_pairs,
        replace=False,
    )

    return pairs[chosen]


def local_density_counts(
    tree: cKDTree,
    positions: np.ndarray,
    radius: float,
) -> np.ndarray:
    neighborhoods = tree.query_ball_point(
        positions,
        r=radius,
    )

    return np.asarray(
        [
            max(0, len(neighborhood) - 1)
            for neighborhood in neighborhoods
        ],
        dtype=np.int32,
    )


def pair_excluded_residuals(
    positions: np.ndarray,
    velocities: np.ndarray,
    families: np.ndarray,
    pairs: np.ndarray,
    tree: cKDTree,
    flow_radius: float,
    min_neighbors: int,
):
    """
    Pair-excluded local-flow estimator.

    For pair (i,j), estimate background near i and j while excluding:
      * i and j themselves
      * family(i)
      * family(j)

    This prevents the tested pair/families from defining their own
    environmental background.
    """
    neighborhoods = tree.query_ball_point(
        positions,
        r=flow_radius,
    )

    residual_i = np.zeros((len(pairs), 2), dtype=np.float64)
    residual_j = np.zeros((len(pairs), 2), dtype=np.float64)
    valid = np.zeros(len(pairs), dtype=bool)

    for k, (i, j) in enumerate(pairs):
        fi = int(families[i])
        fj = int(families[j])

        excluded = {
            fam
            for fam in (fi, fj)
            if fam >= 0
        }

        ni = [
            x
            for x in neighborhoods[i]
            if x != i
            and x != j
            and (
                families[x] < 0
                or int(families[x]) not in excluded
            )
        ]

        nj = [
            x
            for x in neighborhoods[j]
            if x != i
            and x != j
            and (
                families[x] < 0
                or int(families[x]) not in excluded
            )
        ]

        if len(ni) < min_neighbors or len(nj) < min_neighbors:
            continue

        bg_i = velocities[np.asarray(ni, dtype=np.int64)].mean(axis=0)
        bg_j = velocities[np.asarray(nj, dtype=np.int64)].mean(axis=0)

        residual_i[k] = velocities[i] - bg_i
        residual_j[k] = velocities[j] - bg_j
        valid[k] = True

    return residual_i, residual_j, valid


# =====================================================================
# Pair extraction
# =====================================================================

def make_bins(values: np.ndarray, edges: list[float]):
    return np.digitize(values, np.asarray(edges, dtype=float)) - 1


def density_bucket(values: np.ndarray):
    """
    Coarse density buckets that stay reasonably populated.
    """
    edges = np.array([0, 8, 16, 32, 64, 128, 10_000], dtype=float)
    return np.digitize(values, edges) - 1


def time_bucket(time_value: int, width: int) -> int:
    return int(time_value // width)


def collect_pair_records(
    by_time,
    world_size: int,
    pair_radius: float,
    flow_radius: float,
    density_radius: float,
    flow_min_neighbors: int,
    max_pairs_per_tick: int,
    distance_edges: list[float],
    time_bin_width: int,
    seed: int,
):
    rng = np.random.default_rng(seed)

    records = []

    for time_value, points in tqdm(
        sorted(by_time.items()),
        desc="Building matched-pair dataset",
        unit="tick",
        dynamic_ncols=True,
    ):
        if len(points) < 2:
            continue

        positions = np.asarray(
            [p["position"] for p in points],
            dtype=np.float64,
        )
        velocities = np.asarray(
            [p["velocity"] for p in points],
            dtype=np.float64,
        )
        families = np.asarray(
            [
                -1 if p["family"] is None else int(p["family"])
                for p in points
            ],
            dtype=np.int64,
        )

        positions %= float(world_size)

        tree = cKDTree(
            positions,
            boxsize=float(world_size),
        )

        pair_set = tree.query_pairs(
            r=pair_radius,
            output_type="ndarray",
        )

        if pair_set.size == 0:
            continue

        pairs = np.asarray(pair_set, dtype=np.int64).reshape(-1, 2)

        pairs = sample_pairs(
            pairs,
            max_pairs=max_pairs_per_tick,
            rng=rng,
        )

        i = pairs[:, 0]
        j = pairs[:, 1]

        # Need known family on both sides.
        known_family = (
            (families[i] >= 0)
            & (families[j] >= 0)
        )

        if not np.any(known_family):
            continue

        pairs = pairs[known_family]
        i = pairs[:, 0]
        j = pairs[:, 1]

        delta = periodic_delta(
            positions[i],
            positions[j],
            float(world_size),
        )

        distances = np.linalg.norm(delta, axis=1)

        # Pair-excluded residuals.
        residual_i, residual_j, residual_valid = pair_excluded_residuals(
            positions=positions,
            velocities=velocities,
            families=families,
            pairs=pairs,
            tree=tree,
            flow_radius=flow_radius,
            min_neighbors=flow_min_neighbors,
        )

        ui, vi = unit_vectors(residual_i)
        uj, vj = unit_vectors(residual_j)

        valid = residual_valid & vi & vj

        if not np.any(valid):
            continue

        pairs = pairs[valid]
        i = pairs[:, 0]
        j = pairs[:, 1]
        distances = distances[valid]
        ui = ui[valid]
        uj = uj[valid]

        alignment = np.sum(ui * uj, axis=1)

        density = local_density_counts(
            tree=tree,
            positions=positions,
            radius=density_radius,
        )

        pair_density = (
            density[i].astype(np.float64)
            + density[j].astype(np.float64)
        ) / 2.0

        same_family = families[i] == families[j]

        dist_bin = make_bins(
            distances,
            distance_edges,
        )

        dens_bin = density_bucket(
            pair_density,
        )

        t_bin = time_bucket(
            time_value,
            time_bin_width,
        )

        for k in range(len(pairs)):
            if dist_bin[k] < 0 or dist_bin[k] >= len(distance_edges) - 1:
                continue

            records.append(
                (
                    int(t_bin),
                    int(dist_bin[k]),
                    int(dens_bin[k]),
                    bool(same_family[k]),
                    float(alignment[k]),
                    float(distances[k]),
                    float(pair_density[k]),
                    int(time_value),
                )
            )

    print(f"usable matched-analysis pair records: {len(records):,}")

    return records


# =====================================================================
# Matching
# =====================================================================

def matched_analysis(
    records,
    seed: int,
    max_matches_per_stratum: int,
):
    """
    Exact matching on:
        time_bin
        distance_bin
        density_bin

    Within each stratum:
        sample equal numbers of same-family and different-family pairs.

    This creates a balanced matched comparison without giving the enormous
    majority class extra weight.

    We retain both:
        paired-stratum effect
        overall matched means
    """
    rng = np.random.default_rng(seed)

    strata = defaultdict(
        lambda: {
            "same": [],
            "diff": [],
        }
    )

    for record in records:
        (
            t_bin,
            d_bin,
            dens_bin,
            same_family,
            alignment,
            distance,
            density,
            time_value,
        ) = record

        key = (
            t_bin,
            d_bin,
            dens_bin,
        )

        bucket = (
            "same"
            if same_family
            else "diff"
        )

        strata[key][bucket].append(
            (
                alignment,
                distance,
                density,
                time_value,
            )
        )

    matched_same = []
    matched_diff = []
    stratum_effects = []
    effect_by_distance = defaultdict(list)

    used_strata = 0

    for key, groups in tqdm(
        strata.items(),
        desc="Matching same/different family strata",
        unit="stratum",
        dynamic_ncols=True,
    ):
        same = groups["same"]
        diff = groups["diff"]

        n = min(
            len(same),
            len(diff),
            max_matches_per_stratum,
        )

        if n <= 0:
            continue

        same_idx = rng.choice(
            len(same),
            size=n,
            replace=False,
        )
        diff_idx = rng.choice(
            len(diff),
            size=n,
            replace=False,
        )

        selected_same = [
            same[index]
            for index in same_idx
        ]
        selected_diff = [
            diff[index]
            for index in diff_idx
        ]

        same_values = np.asarray(
            [row[0] for row in selected_same],
            dtype=np.float64,
        )
        diff_values = np.asarray(
            [row[0] for row in selected_diff],
            dtype=np.float64,
        )

        matched_same.extend(
            same_values.tolist()
        )
        matched_diff.extend(
            diff_values.tolist()
        )

        effect = float(
            same_values.mean()
            - diff_values.mean()
        )

        stratum_effects.append(
            effect
        )

        distance_bin = key[1]
        effect_by_distance[
            int(distance_bin)
        ].append(
            (
                effect,
                n,
            )
        )

        used_strata += 1

    matched_same = np.asarray(
        matched_same,
        dtype=np.float64,
    )
    matched_diff = np.asarray(
        matched_diff,
        dtype=np.float64,
    )
    stratum_effects = np.asarray(
        stratum_effects,
        dtype=np.float64,
    )

    if len(matched_same) == 0:
        raise RuntimeError(
            "No matched strata contained both same-family and "
            "different-family pairs."
        )

    # Bootstrap strata, not individual pairs. This is more conservative
    # because observations within a time/density/distance stratum are not
    # independent.
    bootstrap_rng = np.random.default_rng(
        seed + 991
    )

    bootstrap = []

    for _ in tqdm(
        range(1000),
        desc="Bootstrapping matched-stratum effect",
        unit="bootstrap",
        dynamic_ncols=True,
    ):
        sample_idx = bootstrap_rng.integers(
            0,
            len(stratum_effects),
            size=len(stratum_effects),
        )

        bootstrap.append(
            float(
                stratum_effects[
                    sample_idx
                ].mean()
            )
        )

    bootstrap = np.asarray(
        bootstrap,
        dtype=np.float64,
    )

    by_distance_result = {}

    for distance_bin, effects in sorted(
        effect_by_distance.items()
    ):
        values = np.asarray(
            [effect for effect, _n in effects],
            dtype=np.float64,
        )

        weights = np.asarray(
            [n for _effect, n in effects],
            dtype=np.float64,
        )

        by_distance_result[
            str(distance_bin)
        ] = {
            "strata": int(len(values)),
            "matched_pairs": int(weights.sum()),
            "mean_effect_unweighted": float(values.mean()),
            "mean_effect_weighted": float(
                np.average(
                    values,
                    weights=weights,
                )
            ),
        }

    return {
        "matched_pairs_per_group": int(len(matched_same)),
        "used_strata": int(used_strata),
        "same_mean": float(matched_same.mean()),
        "diff_mean": float(matched_diff.mean()),
        "raw_difference": float(
            matched_same.mean()
            - matched_diff.mean()
        ),
        "mean_stratum_effect": float(
            stratum_effects.mean()
        ),
        "bootstrap_95_low": float(
            np.percentile(
                bootstrap,
                2.5,
            )
        ),
        "bootstrap_95_high": float(
            np.percentile(
                bootstrap,
                97.5,
            )
        ),
        "same_std": float(
            matched_same.std()
        ),
        "diff_std": float(
            matched_diff.std()
        ),
        "effect_by_distance": by_distance_result,
    }


# =====================================================================
# Cache
# =====================================================================

def make_analysis_key(params: dict) -> str:
    payload = json.dumps(
        params,
        sort_keys=True,
    ).encode("utf-8")

    digest = hashlib.sha256(
        payload
    ).hexdigest()[:20]

    return f"distance-matched-coherence-v1-{digest}"


def load_cached_analysis(
    conn: sqlite3.Connection,
    run_id: int,
    key: str,
):
    row = conn.execute(
        """
        SELECT result_json
        FROM analysis_results
        WHERE run_id=? AND analysis_key=?
        """,
        (run_id, key),
    ).fetchone()

    if not row:
        return None

    return json.loads(
        row[0]
    )


def store_analysis(
    conn: sqlite3.Connection,
    run_id: int,
    key: str,
    params: dict,
    result: dict,
):
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO analysis_results(
                run_id,
                analysis_key,
                params_json,
                result_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                run_id,
                key,
                json.dumps(
                    params,
                    sort_keys=True,
                ),
                json.dumps(result),
                datetime.now(
                    timezone.utc
                ).isoformat(),
            ),
        )


# =====================================================================
# Figures
# =====================================================================

def build_main_figure(result: dict):
    labels = [
        "Same recent-c2 family",
        "Different recent-c2 family",
    ]

    values = [
        result["same_mean"],
        result["diff_mean"],
    ]

    fig, ax = plt.subplots(
        figsize=(9, 6),
    )

    bars = ax.bar(
        labels,
        values,
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_ylim(
        -1.05,
        1.05,
    )

    ax.set_ylabel(
        "Pair-excluded residual velocity alignment"
    )

    ax.set_title(
        "Outlier: Distance-, Time-, and Density-Matched Motion Coherence"
    )

    note = (
        f"Matched pairs per group: {result['matched_pairs_per_group']:,} | "
        f"strata: {result['used_strata']:,}\n"
        f"Mean matched-stratum effect = {result['mean_stratum_effect']:.3f} "
        f"(bootstrap 95%: {result['bootstrap_95_low']:.3f} "
        f"to {result['bootstrap_95_high']:.3f})"
    )

    fig.text(
        0.5,
        0.01,
        note,
        ha="center",
        fontsize=9,
    )

    for bar, value in zip(
        bars,
        values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 0.03,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    ax.grid(
        axis="y",
        alpha=0.25,
    )

    fig.tight_layout(
        rect=(0, 0.06, 1, 1)
    )

    path = (
        OUTPUT_DIR
        / "ch11-outlier-distance-matched-coherence.png"
    )

    fig.savefig(
        path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )

    print(
        f"saved: {path}"
    )


def build_distance_effect_figure(
    result: dict,
    distance_edges: list[float],
):
    rows = []

    for key, entry in result[
        "effect_by_distance"
    ].items():
        distance_bin = int(
            key
        )

        if (
            distance_bin < 0
            or distance_bin >= len(distance_edges) - 1
        ):
            continue

        rows.append(
            (
                distance_bin,
                (
                    distance_edges[distance_bin]
                    + distance_edges[distance_bin + 1]
                ) / 2.0,
                entry[
                    "mean_effect_weighted"
                ],
                entry[
                    "matched_pairs"
                ],
                entry[
                    "strata"
                ],
            )
        )

    rows.sort(
        key=lambda row: row[0]
    )

    if not rows:
        return

    centres = np.asarray(
        [row[1] for row in rows],
        dtype=np.float64,
    )

    effects = np.asarray(
        [row[2] for row in rows],
        dtype=np.float64,
    )

    counts = [
        row[3]
        for row in rows
    ]

    strata_counts = [
        row[4]
        for row in rows
    ]

    fig, ax = plt.subplots(
        figsize=(10, 6),
    )

    ax.plot(
        centres,
        effects,
        marker="o",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Spatial distance"
    )

    ax.set_ylabel(
        "Same-family minus different-family residual alignment"
    )

    ax.set_title(
        "Outlier: Matched Causal-Family Effect by Spatial Distance"
    )

    ax.grid(
        alpha=0.25,
    )

    for x, y, n, strata in zip(
        centres,
        effects,
        counts,
        strata_counts,
    ):
        ax.annotate(
            f"{y:.3f}\n{n:,} pairs",
            (x, y),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch11-outlier-distance-matched-effect-by-distance.png"
    )

    fig.savefig(
        path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )

    print(
        f"saved: {path}"
    )


# =====================================================================
# CLI
# =====================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Distance/time/density matched causal-family coherence analysis "
            "using cached Outlier motion data"
        )
    )

    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
    )

    parser.add_argument(
        "--run-id",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--pair-radius",
        type=float,
        default=96.0,
    )

    parser.add_argument(
        "--flow-radius",
        type=float,
        default=48.0,
    )

    parser.add_argument(
        "--density-radius",
        type=float,
        default=32.0,
    )

    parser.add_argument(
        "--flow-min-neighbors",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--max-pairs-per-tick",
        type=int,
        default=2500,
        help=(
            "Pair-excluded local-flow estimation is expensive. "
            "2500 per tick still gives a large matched dataset."
        ),
    )

    parser.add_argument(
        "--time-bin-width",
        type=int,
        default=25,
    )

    parser.add_argument(
        "--max-matches-per-stratum",
        type=int,
        default=5000,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--reanalyze",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    conn = connect_db(
        args.db
    )

    run_id = latest_complete_run(
        conn,
        args.run_id,
    )

    metadata = run_metadata(
        conn,
        run_id,
    )

    print(
        f"Using cached run_id={run_id} "
        f"size={metadata['size']} "
        f"generations={metadata['generations']}"
    )

    # Chosen to resolve the very short range where same-family pairs dominate,
    # while still retaining broader controls.
    distance_edges = [
        0.0,
        4.0,
        8.0,
        12.0,
        16.0,
        24.0,
        32.0,
        48.0,
        64.0,
        96.0,
    ]

    params = {
        "pair_radius": args.pair_radius,
        "flow_radius": args.flow_radius,
        "density_radius": args.density_radius,
        "flow_min_neighbors": args.flow_min_neighbors,
        "max_pairs_per_tick": args.max_pairs_per_tick,
        "time_bin_width": args.time_bin_width,
        "max_matches_per_stratum": args.max_matches_per_stratum,
        "distance_edges": distance_edges,
        "seed": args.seed,
        "analysis_version": 1,
    }

    key = make_analysis_key(
        params
    )

    result = (
        None
        if args.reanalyze
        else load_cached_analysis(
            conn,
            run_id,
            key,
        )
    )

    if result is None:
        by_time = load_motion_by_time(
            conn,
            run_id,
        )

        records = collect_pair_records(
            by_time=by_time,
            world_size=metadata["size"],
            pair_radius=args.pair_radius,
            flow_radius=args.flow_radius,
            density_radius=args.density_radius,
            flow_min_neighbors=args.flow_min_neighbors,
            max_pairs_per_tick=args.max_pairs_per_tick,
            distance_edges=distance_edges,
            time_bin_width=args.time_bin_width,
            seed=args.seed,
        )

        result = matched_analysis(
            records=records,
            seed=args.seed,
            max_matches_per_stratum=args.max_matches_per_stratum,
        )

        store_analysis(
            conn,
            run_id,
            key,
            params,
            result,
        )

        print(
            f"analysis cached: {key}"
        )

    else:
        print(
            f"Using cached analysis: {key}"
        )

    build_main_figure(
        result
    )

    build_distance_effect_figure(
        result,
        distance_edges,
    )

    print()
    print("Distance-matched causal coherence:")
    print(
        f"  same-family matched mean       = {result['same_mean']:.6f}"
    )
    print(
        f"  different-family matched mean  = {result['diff_mean']:.6f}"
    )
    print(
        f"  raw matched difference         = {result['raw_difference']:.6f}"
    )
    print(
        f"  mean stratum effect            = {result['mean_stratum_effect']:.6f}"
    )
    print(
        f"  bootstrap 95% interval         = "
        f"[{result['bootstrap_95_low']:.6f}, "
        f"{result['bootstrap_95_high']:.6f}]"
    )
    print(
        f"  matched pairs per group        = "
        f"{result['matched_pairs_per_group']:,}"
    )
    print(
        f"  matched strata                 = "
        f"{result['used_strata']:,}"
    )

    print()
    print("Effect by distance bin:")

    for key_name, entry in sorted(
        result["effect_by_distance"].items(),
        key=lambda item: int(item[0]),
    ):
        index = int(key_name)

        low = distance_edges[index]
        high = distance_edges[index + 1]

        print(
            f"  {low:5.1f}-{high:5.1f}  "
            f"effect={entry['mean_effect_weighted']:+.6f}  "
            f"pairs={entry['matched_pairs']:,}  "
            f"strata={entry['strata']:,}"
        )

    print()
    print("Interpretation:")
    print(
        "  Positive matched effects mean same-family pairs move more coherently "
        "than different-family pairs observed at similar time, spatial distance, "
        "and local density."
    )
    print(
        "  If the bootstrap interval remains entirely above zero, that is "
        "evidence that causal-family membership predicts motion coherence "
        "beyond the matched spatial context used here."
    )


if __name__ == "__main__":
    main()
