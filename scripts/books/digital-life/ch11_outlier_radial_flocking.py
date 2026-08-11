from __future__ import annotations

"""
Chapter 11 — cached Outlier collective-motion analysis.

This script has two jobs:

1. Build a reusable SQLite cache from the expensive Outlier simulation and
   causal analysis. The simulation is only run when a matching cached run does
   not already exist (or --rebuild is requested).

2. Test whether the apparent flocking survives two stronger controls:

   A. subtract the common radial expansion field;
   B. compare motion within the same causal c2 family versus motion between
      different causal c2 families.

The expensive reusable layers stored in SQLite are:

    experiment_runs
    clusters
    causal_edges
    c2_occurrences
    c2_return_edges
    motion_tracks
    motion_points
    analysis_results

The analysis results themselves are also cached by parameter set, so rerunning
with the same arguments can regenerate the figure without repeating the test.

Expected companion module:
    scripts/books/digital-life/ch10_outlier_lineage.py

That module contains the published Outlier rule, simulation, cluster detector,
counterfactual causal tracer, c2 detector, and persistent-track builder.
"""

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict, deque
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    def tqdm(iterable=None, **kwargs):
        return iterable if iterable is not None else range(kwargs.get("total", 0))

import ch10_outlier_lineage as outlier


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DB = Path("data/digital-life/outlier.sqlite3")


# =====================================================================
# SQLite schema
# =====================================================================

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS experiment_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    size INTEGER NOT NULL,
    generations INTEGER NOT NULL,
    min_area INTEGER NOT NULL,
    max_area INTEGER NOT NULL,
    min_track_length INTEGER NOT NULL,
    outlier_map TEXT NOT NULL,
    status TEXT NOT NULL,
    c2_signature BLOB
);

CREATE TABLE IF NOT EXISTS clusters (
    run_id INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    time INTEGER NOT NULL,
    area INTEGER NOT NULL,
    row REAL NOT NULL,
    col REAL NOT NULL,
    signature BLOB NOT NULL,
    PRIMARY KEY (run_id, uid),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_clusters_run_time
ON clusters(run_id, time);

CREATE INDEX IF NOT EXISTS idx_clusters_run_signature
ON clusters(run_id, signature);

CREATE TABLE IF NOT EXISTS causal_edges (
    run_id INTEGER NOT NULL,
    parent_uid INTEGER NOT NULL,
    child_uid INTEGER NOT NULL,
    causal_cells INTEGER NOT NULL,
    PRIMARY KEY (run_id, parent_uid, child_uid),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_edges_run_parent
ON causal_edges(run_id, parent_uid);

CREATE INDEX IF NOT EXISTS idx_edges_run_child
ON causal_edges(run_id, child_uid);

CREATE TABLE IF NOT EXISTS c2_occurrences (
    run_id INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    time INTEGER NOT NULL,
    PRIMARY KEY (run_id, uid),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS c2_return_edges (
    run_id INTEGER NOT NULL,
    parent_uid INTEGER NOT NULL,
    child_uid INTEGER NOT NULL,
    PRIMARY KEY (run_id, parent_uid, child_uid),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS motion_tracks (
    run_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    length INTEGER NOT NULL,
    PRIMARY KEY (run_id, track_id),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS motion_points (
    run_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    seq INTEGER NOT NULL,
    time INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    row REAL NOT NULL,
    col REAL NOT NULL,
    velocity_row REAL NOT NULL,
    velocity_col REAL NOT NULL,
    family_id INTEGER,
    PRIMARY KEY (run_id, track_id, seq),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_motion_run_time
ON motion_points(run_id, time);

CREATE INDEX IF NOT EXISTS idx_motion_run_uid
ON motion_points(run_id, uid);

CREATE INDEX IF NOT EXISTS idx_motion_run_family
ON motion_points(run_id, family_id);

CREATE TABLE IF NOT EXISTS analysis_results (
    run_id INTEGER NOT NULL,
    analysis_key TEXT NOT NULL,
    params_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (run_id, analysis_key),
    FOREIGN KEY (run_id) REFERENCES experiment_runs(id) ON DELETE CASCADE
);
"""


def connect_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA busy_timeout=60000")
    conn.executescript(SCHEMA)
    return conn


def cache_key(
    size: int,
    generations: int,
    min_area: int,
    max_area: int,
    min_track_length: int,
) -> str:
    payload = {
        "size": size,
        "generations": generations,
        "min_area": min_area,
        "max_area": max_area,
        "min_track_length": min_track_length,
        "outlier_map": outlier.OUTLIER_MAP,
        "seed": outlier.SEED_C0.tolist(),
        "cache_version": 2,
    }
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


# =====================================================================
# Persist expensive experiment layers
# =====================================================================


def insert_run(
    conn: sqlite3.Connection,
    key: str,
    args,
    c2_signature: bytes,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO experiment_runs(
            cache_key, created_at, size, generations,
            min_area, max_area, min_track_length,
            outlier_map, status, c2_signature
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'building', ?)
        """,
        (
            key,
            datetime.now(timezone.utc).isoformat(),
            args.size,
            args.generations,
            args.min_area,
            args.max_area,
            args.min_track_length,
            outlier.OUTLIER_MAP,
            sqlite3.Binary(c2_signature),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_completed_run(conn: sqlite3.Connection, key: str) -> int | None:
    row = conn.execute(
        "SELECT id FROM experiment_runs WHERE cache_key=? AND status='complete'",
        (key,),
    ).fetchone()
    return int(row[0]) if row else None


def delete_run_by_key(conn: sqlite3.Connection, key: str) -> None:
    conn.execute("DELETE FROM experiment_runs WHERE cache_key=?", (key,))
    conn.commit()


def find_branching_root(return_graph: dict[int, list[int]], clusters) -> int:
    branching = [uid for uid, kids in return_graph.items() if len(kids) >= 2]
    if branching:
        return min(branching, key=lambda uid: clusters[uid].time)
    if return_graph:
        return min(return_graph, key=lambda uid: clusters[uid].time)
    raise RuntimeError("No c2 causal-return graph was produced")


def causal_family_labels(
    clusters,
    edges,
    return_graph: dict[int, list[int]],
    root: int,
) -> dict[int, int]:
    """
    Label descendants of the root's first-return c2 children.

    family 0,1,2,... = descendants that trace to one immediate c2 branch.
    family -1        = descendants reached by more than one branch (merge).
    missing          = not downstream of one of those branch roots.

    Because causal edges connect t -> t+1, a time-ordered propagation is a
    simple DAG pass. This is deliberately conservative: once two branch labels
    merge, downstream nodes remain ambiguous (-1).
    """
    branch_roots = list(return_graph.get(root, []))
    if not branch_roots:
        return {}

    labels: dict[int, int] = {
        uid: family for family, uid in enumerate(branch_roots)
    }

    # The simulation emitted edges in chronological order. Sort explicitly so
    # this remains true even if the upstream implementation changes.
    ordered_edges = sorted(
        edges,
        key=lambda e: (
            clusters[e.parent].time,
            e.parent,
            e.child,
        ),
    )

    for edge in tqdm(
        ordered_edges,
        desc="Propagating causal families",
        unit="edge",
        dynamic_ncols=True,
    ):
        parent_label = labels.get(edge.parent)
        if parent_label is None:
            continue

        old = labels.get(edge.child)
        if old is None:
            labels[edge.child] = parent_label
        elif old != parent_label:
            labels[edge.child] = -1

    return labels


def persist_experiment(
    conn: sqlite3.Connection,
    run_id: int,
    clusters,
    edges,
    c2_signature: bytes,
    return_graph: dict[int, list[int]],
    tracks,
    family_labels: dict[int, int],
) -> None:
    print("Persisting experiment to SQLite ...")

    with conn:
        conn.executemany(
            """
            INSERT INTO clusters(run_id, uid, time, area, row, col, signature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                (
                    run_id,
                    c.uid,
                    c.time,
                    c.area,
                    c.centroid[0],
                    c.centroid[1],
                    sqlite3.Binary(c.signature),
                )
                for c in clusters.values()
            ),
        )

        conn.executemany(
            """
            INSERT INTO causal_edges(run_id, parent_uid, child_uid, causal_cells)
            VALUES (?, ?, ?, ?)
            """,
            (
                (run_id, e.parent, e.child, e.causal_cells)
                for e in edges
            ),
        )

        c2_uids = outlier.c2_occurrences(clusters, c2_signature)
        conn.executemany(
            "INSERT INTO c2_occurrences(run_id, uid, time) VALUES (?, ?, ?)",
            ((run_id, uid, clusters[uid].time) for uid in c2_uids),
        )

        conn.executemany(
            """
            INSERT INTO c2_return_edges(run_id, parent_uid, child_uid)
            VALUES (?, ?, ?)
            """,
            (
                (run_id, parent, child)
                for parent, children in return_graph.items()
                for child in children
            ),
        )

        conn.executemany(
            "INSERT INTO motion_tracks(run_id, track_id, length) VALUES (?, ?, ?)",
            (
                (run_id, track_id, len(track))
                for track_id, track in enumerate(tracks)
            ),
        )

        def motion_rows():
            for track_id, track in enumerate(tracks):
                for seq, point in enumerate(track):
                    velocity = np.asarray(point.velocity, dtype=float)
                    yield (
                        run_id,
                        track_id,
                        seq,
                        point.time,
                        point.uid,
                        float(point.centroid[0]),
                        float(point.centroid[1]),
                        float(velocity[0]),
                        float(velocity[1]),
                        family_labels.get(point.uid),
                    )

        conn.executemany(
            """
            INSERT INTO motion_points(
                run_id, track_id, seq, time, uid,
                row, col, velocity_row, velocity_col, family_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            motion_rows(),
        )

        conn.execute(
            "UPDATE experiment_runs SET status='complete' WHERE id=?",
            (run_id,),
        )


def build_cache(conn: sqlite3.Connection, args, key: str) -> int:
    print("No matching completed cache found. Building it once.")

    c2_signature, _ = outlier.derive_c2_signature(args.size)
    run_id = insert_run(conn, key, args, c2_signature)

    try:
        clusters, edges, _ = outlier.run_causal_experiment(
            size=args.size,
            generations=args.generations,
        )

        print(f"clusters:     {len(clusters):,}")
        print(f"causal edges: {len(edges):,}")

        _visible, root, return_graph = outlier.build_c2_return_graph(
            clusters,
            edges,
            c2_signature,
            max_generations=args.lineage_depth,
        )

        tracks = outlier.build_persistent_tracks(
            clusters,
            edges,
            world_size=args.size,
            min_area=args.min_area,
            max_area=args.max_area,
            min_length=args.min_track_length,
        )

        family_labels = causal_family_labels(
            clusters,
            edges,
            return_graph,
            root,
        )

        persist_experiment(
            conn,
            run_id,
            clusters,
            edges,
            c2_signature,
            return_graph,
            tracks,
            family_labels,
        )

        print(f"SQLite cache complete: run_id={run_id}")
        return run_id

    except Exception:
        conn.execute(
            "UPDATE experiment_runs SET status='failed' WHERE id=?",
            (run_id,),
        )
        conn.commit()
        raise


# =====================================================================
# Load only the lightweight data required by the new experiment
# =====================================================================


def load_motion_by_time(conn: sqlite3.Connection, run_id: int):
    by_time: dict[int, list[dict]] = defaultdict(list)

    cursor = conn.execute(
        """
        SELECT time, uid, row, col, velocity_row, velocity_col, family_id
        FROM motion_points
        WHERE run_id=?
        ORDER BY time, track_id, seq
        """,
        (run_id,),
    )

    for time, uid, row, col, vr, vc, family in cursor:
        velocity = np.array([vr, vc], dtype=np.float64)
        if np.linalg.norm(velocity) <= 1e-12:
            continue
        by_time[int(time)].append(
            {
                "uid": int(uid),
                "position": np.array([row, col], dtype=np.float64),
                "velocity": velocity,
                "family": None if family is None else int(family),
            }
        )

    return by_time


# =====================================================================
# Radial subtraction
# =====================================================================


def periodic_delta(points: np.ndarray, centre: np.ndarray, size: float) -> np.ndarray:
    delta = points - centre
    return (delta + size / 2.0) % size - size / 2.0


def residual_velocities(
    positions: np.ndarray,
    velocities: np.ndarray,
    centre: np.ndarray,
    world_size: float,
) -> np.ndarray:
    """Remove each velocity's component along the seed-centred radial field."""
    radial = periodic_delta(positions, centre, world_size)
    norms = np.linalg.norm(radial, axis=1)

    unit_radial = np.zeros_like(radial)
    valid = norms > 1e-12
    unit_radial[valid] = radial[valid] / norms[valid, None]

    radial_speed = np.sum(velocities * unit_radial, axis=1)
    radial_component = radial_speed[:, None] * unit_radial
    return velocities - radial_component


def unit_vectors(vectors: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    speeds = np.linalg.norm(vectors, axis=1)
    valid = speeds > 1e-12
    units = np.zeros_like(vectors)
    units[valid] = vectors[valid] / speeds[valid, None]
    return units, valid


# =====================================================================
# Efficient local-pair experiment
# =====================================================================


def sample_pairs(
    pairs: np.ndarray,
    max_pairs: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if len(pairs) <= max_pairs:
        return pairs
    idx = rng.choice(len(pairs), size=max_pairs, replace=False)
    return pairs[idx]


def accumulate_alignment(
    sums: np.ndarray,
    counts: np.ndarray,
    bins: np.ndarray,
    distances: np.ndarray,
    alignments: np.ndarray,
    mask: np.ndarray | None = None,
) -> None:
    if mask is not None:
        distances = distances[mask]
        alignments = alignments[mask]
    if len(distances) == 0:
        return

    indices = np.digitize(distances, bins) - 1
    valid = (
        (indices >= 0)
        & (indices < len(sums))
        & np.isfinite(alignments)
    )
    indices = indices[valid]
    values = alignments[valid]

    sums += np.bincount(indices, weights=values, minlength=len(sums))[: len(sums)]
    counts += np.bincount(indices, minlength=len(sums))[: len(sums)]


def run_radial_family_test(
    by_time,
    world_size: int,
    radius: float,
    n_bins: int,
    max_pairs_per_tick: int,
    shuffles: int,
    seed: int,
):
    """
    Compute four observed curves:

      raw                  original velocity alignment
      residual             after removing radial expansion
      residual_same_family residual alignment among same causal branch
      residual_diff_family residual alignment among different causal branches

    A velocity-shuffled residual control is computed on exactly the same
    sampled spatial pairs. Pair geometry is never recomputed during shuffles.
    """
    rng = np.random.default_rng(seed)
    bins = np.linspace(0.0, radius, n_bins + 1)
    centre = np.array([world_size / 2.0, world_size / 2.0], dtype=np.float64)

    names = [
        "raw",
        "residual",
        "residual_same_family",
        "residual_diff_family",
    ]
    sums = {name: np.zeros(n_bins, dtype=np.float64) for name in names}
    counts = {name: np.zeros(n_bins, dtype=np.int64) for name in names}

    # Cache sampled per-tick geometry + normalized velocity arrays. This is
    # enough for all shuffled controls; no KD-tree work is repeated.
    prepared: list[dict] = []
    total_sampled_pairs = 0

    for time, points in tqdm(
        sorted(by_time.items()),
        desc="Indexing local pairs + radial residuals",
        unit="tick",
        dynamic_ncols=True,
    ):
        if len(points) < 2:
            continue

        positions = np.asarray([p["position"] for p in points], dtype=np.float64)
        velocities = np.asarray([p["velocity"] for p in points], dtype=np.float64)
        families = np.asarray([
            -999999 if p["family"] is None else p["family"]
            for p in points
        ], dtype=np.int64)

        positions %= float(world_size)

        tree = cKDTree(positions, boxsize=float(world_size))
        pair_set = tree.query_pairs(r=radius, output_type="ndarray")
        if pair_set.size == 0:
            continue

        pairs = np.asarray(pair_set, dtype=np.int64).reshape(-1, 2)
        pairs = sample_pairs(pairs, max_pairs_per_tick, rng)

        # Periodic pair distances.
        delta = positions[pairs[:, 1]] - positions[pairs[:, 0]]
        delta = (delta + world_size / 2.0) % world_size - world_size / 2.0
        distances = np.linalg.norm(delta, axis=1)

        raw_units, raw_valid = unit_vectors(velocities)
        residual = residual_velocities(positions, velocities, centre, float(world_size))
        residual_units, residual_valid = unit_vectors(residual)

        i = pairs[:, 0]
        j = pairs[:, 1]

        raw_alignment = np.sum(raw_units[i] * raw_units[j], axis=1)
        residual_alignment = np.sum(residual_units[i] * residual_units[j], axis=1)

        valid_raw_pairs = raw_valid[i] & raw_valid[j]
        valid_residual_pairs = residual_valid[i] & residual_valid[j]

        family_known = (families[i] >= 0) & (families[j] >= 0)
        same_family = family_known & (families[i] == families[j])
        diff_family = family_known & (families[i] != families[j])

        accumulate_alignment(
            sums["raw"], counts["raw"], bins,
            distances, raw_alignment, valid_raw_pairs,
        )
        accumulate_alignment(
            sums["residual"], counts["residual"], bins,
            distances, residual_alignment, valid_residual_pairs,
        )
        accumulate_alignment(
            sums["residual_same_family"], counts["residual_same_family"], bins,
            distances, residual_alignment,
            valid_residual_pairs & same_family,
        )
        accumulate_alignment(
            sums["residual_diff_family"], counts["residual_diff_family"], bins,
            distances, residual_alignment,
            valid_residual_pairs & diff_family,
        )

        prepared.append(
            {
                "distances": distances,
                "pairs": pairs,
                "residual_units": residual_units,
                "residual_valid": residual_valid,
            }
        )
        total_sampled_pairs += len(pairs)

    print(f"sampled local pairs: {total_sampled_pairs:,}")

    means = {}
    for name in names:
        means[name] = np.divide(
            sums[name],
            counts[name],
            out=np.full(n_bins, np.nan, dtype=np.float64),
            where=counts[name] > 0,
        )

    # Null: preserve positions, time slices, pair geometry, and residual speed
    # distribution; shuffle residual directions among structures within each
    # tick. We aggregate directly into bins instead of retaining millions of
    # pair values.
    null_curves = np.full((shuffles, n_bins), np.nan, dtype=np.float64)

    for shuffle_idx in tqdm(
        range(shuffles),
        desc="Shuffling residual velocity field",
        unit="shuffle",
        dynamic_ncols=True,
    ):
        null_sum = np.zeros(n_bins, dtype=np.float64)
        null_count = np.zeros(n_bins, dtype=np.int64)

        for item in prepared:
            units = item["residual_units"]
            valid = item["residual_valid"]
            pairs = item["pairs"]
            distances = item["distances"]

            permutation = rng.permutation(len(units))
            shuffled = units[permutation]
            shuffled_valid = valid[permutation]

            i = pairs[:, 0]
            j = pairs[:, 1]
            pair_valid = shuffled_valid[i] & shuffled_valid[j]
            alignment = np.sum(shuffled[i] * shuffled[j], axis=1)

            accumulate_alignment(
                null_sum,
                null_count,
                bins,
                distances,
                alignment,
                pair_valid,
            )

        null_curves[shuffle_idx] = np.divide(
            null_sum,
            null_count,
            out=np.full(n_bins, np.nan, dtype=np.float64),
            where=null_count > 0,
        )

    null_mean = np.nanmean(null_curves, axis=0)
    null_low = np.nanpercentile(null_curves, 5, axis=0)
    null_high = np.nanpercentile(null_curves, 95, axis=0)

    return {
        "bins": bins.tolist(),
        "centres": ((bins[:-1] + bins[1:]) / 2.0).tolist(),
        "means": {k: v.tolist() for k, v in means.items()},
        "counts": {k: v.tolist() for k, v in counts.items()},
        "null_mean": null_mean.tolist(),
        "null_low": null_low.tolist(),
        "null_high": null_high.tolist(),
        "sampled_pairs": int(total_sampled_pairs),
        "ticks": len(prepared),
    }


# =====================================================================
# Cache analysis results too
# =====================================================================


def analysis_key(params: dict) -> str:
    raw = json.dumps(params, sort_keys=True).encode("utf-8")
    return "radial-family-v2-" + hashlib.sha256(raw).hexdigest()[:20]


def load_cached_analysis(
    conn: sqlite3.Connection,
    run_id: int,
    key: str,
):
    row = conn.execute(
        "SELECT result_json FROM analysis_results WHERE run_id=? AND analysis_key=?",
        (run_id, key),
    ).fetchone()
    return json.loads(row[0]) if row else None


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
                run_id, analysis_key, params_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                run_id,
                key,
                json.dumps(params, sort_keys=True),
                json.dumps(result),
                datetime.now(timezone.utc).isoformat(),
            ),
        )


# =====================================================================
# Figure
# =====================================================================


def array(result: dict, key: str) -> np.ndarray:
    return np.asarray(result[key], dtype=np.float64)


def nested_array(result: dict, group: str, key: str) -> np.ndarray:
    return np.asarray(result[group][key], dtype=np.float64)


def build_figure(result: dict, min_pairs: int) -> Path:
    centres = array(result, "centres")
    means = result["means"]
    counts = result["counts"]

    raw = np.asarray(means["raw"], dtype=float)
    residual = np.asarray(means["residual"], dtype=float)
    same = np.asarray(means["residual_same_family"], dtype=float)
    diff = np.asarray(means["residual_diff_family"], dtype=float)

    raw_n = np.asarray(counts["raw"], dtype=int)
    residual_n = np.asarray(counts["residual"], dtype=int)
    same_n = np.asarray(counts["residual_same_family"], dtype=int)
    diff_n = np.asarray(counts["residual_diff_family"], dtype=int)

    null_mean = array(result, "null_mean")
    null_low = array(result, "null_low")
    null_high = array(result, "null_high")

    fig, ax = plt.subplots(figsize=(12, 7))

    valid_raw = (raw_n >= min_pairs) & np.isfinite(raw)
    valid_residual = (residual_n >= min_pairs) & np.isfinite(residual)
    valid_same = (same_n >= min_pairs) & np.isfinite(same)
    valid_diff = (diff_n >= min_pairs) & np.isfinite(diff)

    ax.plot(centres[valid_raw], raw[valid_raw], marker="o", label="Raw velocity alignment")
    ax.plot(
        centres[valid_residual], residual[valid_residual], marker="o",
        label="After subtracting radial expansion",
    )
    ax.plot(
        centres[valid_same], same[valid_same], marker="o",
        label="Residual: same causal family",
    )
    ax.plot(
        centres[valid_diff], diff[valid_diff], marker="o",
        label="Residual: different causal families",
    )

    valid_null = np.isfinite(null_mean)
    ax.plot(
        centres[valid_null], null_mean[valid_null], linestyle="--",
        label="Residual velocity-shuffled control",
    )
    ax.fill_between(
        centres[valid_null], null_low[valid_null], null_high[valid_null],
        alpha=0.18, label="Control 5–95%",
    )

    ax.axhline(0.0, linewidth=1)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel("Distance between simultaneously moving clusters")
    ax.set_ylabel("Velocity alignment (1=same direction, -1=opposite)")
    ax.set_title("Outlier: Does Local Motion Coherence Survive Radial Subtraction?")
    ax.grid(alpha=0.25)
    ax.legend()

    subtitle = (
        f"Sampled local pairs: {result['sampled_pairs']:,} across "
        f"{result['ticks']:,} ticks. Same/different-family curves use "
        "only non-ambiguous c2 causal branch assignments."
    )
    fig.text(0.5, 0.01, subtitle, ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))

    path = OUTPUT_DIR / "ch11-outlier-radial-family-flocking.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")
    return path


# =====================================================================
# CLI
# =====================================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cache Outlier in SQLite and test radial/family flocking hypotheses"
    )
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--generations", type=int, default=1600)
    parser.add_argument("--lineage-depth", type=int, default=4)

    parser.add_argument("--min-area", type=int, default=3)
    parser.add_argument("--max-area", type=int, default=200)
    parser.add_argument("--min-track-length", type=int, default=8)

    parser.add_argument("--radius", type=float, default=96.0)
    parser.add_argument("--bins", type=int, default=6)
    parser.add_argument(
        "--max-pairs-per-tick",
        type=int,
        default=10_000,
        help="Deterministic sampling cap. Millions of correlated pairs add cost, not much evidence.",
    )
    parser.add_argument("--shuffles", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-pairs", type=int, default=100)

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete the matching cached simulation and rebuild it from scratch.",
    )
    parser.add_argument(
        "--reanalyze",
        action="store_true",
        help="Reuse cached simulation/tracks but recompute the radial/family analysis.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    conn = connect_db(args.db)

    key = cache_key(
        args.size,
        args.generations,
        args.min_area,
        args.max_area,
        args.min_track_length,
    )

    if args.rebuild:
        print(f"Deleting matching cache: {key}")
        delete_run_by_key(conn, key)

    run_id = get_completed_run(conn, key)
    if run_id is None:
        # Remove a stale failed/building row with the same unique key before
        # retrying it.
        delete_run_by_key(conn, key)
        run_id = build_cache(conn, args, key)
    else:
        print(f"Using cached Outlier run: run_id={run_id} db={args.db}")

    params = {
        "radius": args.radius,
        "bins": args.bins,
        "max_pairs_per_tick": args.max_pairs_per_tick,
        "shuffles": args.shuffles,
        "seed": args.seed,
        "analysis_version": 2,
    }
    akey = analysis_key(params)

    result = None if args.reanalyze else load_cached_analysis(conn, run_id, akey)

    if result is None:
        print("Loading cached motion observations ...")
        by_time = load_motion_by_time(conn, run_id)
        print(
            f"motion ticks: {len(by_time):,} | "
            f"motion observations: {sum(len(v) for v in by_time.values()):,}"
        )

        result = run_radial_family_test(
            by_time=by_time,
            world_size=args.size,
            radius=args.radius,
            n_bins=args.bins,
            max_pairs_per_tick=args.max_pairs_per_tick,
            shuffles=args.shuffles,
            seed=args.seed,
        )
        store_analysis(conn, run_id, akey, params, result)
        print(f"analysis cached: {akey}")
    else:
        print(f"Using cached analysis: {akey}")

    build_figure(result, min_pairs=args.min_pairs)

    print()
    print("Key first-bin values:")
    for name, values in result["means"].items():
        first = values[0] if values else None
        count = result["counts"][name][0] if result["counts"][name] else 0
        print(f"  {name:28s} alignment={first!s:>10}  n={count:,}")
    print(
        f"  {'shuffled residual control':28s} "
        f"alignment={result['null_mean'][0]!s:>10}"
    )


if __name__ == "__main__":
    main()
