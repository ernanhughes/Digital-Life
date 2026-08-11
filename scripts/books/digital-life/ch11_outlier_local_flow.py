from __future__ import annotations

"""
Chapter 11 — Outlier: recent-c2 ancestry + local-flow subtraction.

This script is intentionally ANALYSIS ONLY.

It reuses the expensive experiment cached by:

    scripts/books/digital-life/ch11_outlier_radial_flocking.py

Expected database:

    data/digital-life/outlier.sqlite3

No cellular automaton generations are recomputed.

Questions tested
================

1. Can we assign moving clusters to their most recent causal c2 ancestor,
   rather than only to the four first branches of the original c2?

2. After removing a LOCAL background velocity field, do nearby moving
   structures still show directional coherence?

3. Does residual coherence occur:

       within the same recent-c2 family

   or:

       between different recent-c2 families?

The local background flow for each moving structure is estimated from nearby
moving structures while EXCLUDING structures with the same recent-c2 ancestor.
That makes the test deliberately conservative: we do not want a distributed
member of the same causal organization to define the "environmental flow"
that we later subtract from itself.

Outputs
=======

    static/images/books/digital-life/
        ch11-outlier-local-flow-family-test.png
        ch11-outlier-family-coverage.png

New SQLite cache
================

    c2_recent_ancestor

The ancestry table is computed once per run and reused on later executions.
The numerical analysis is also cached in analysis_results.
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

EXTRA_SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;

CREATE TABLE IF NOT EXISTS c2_recent_ancestor (
    run_id INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    ancestor_uid INTEGER,
    distance INTEGER,
    ambiguous INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (run_id, uid)
);

CREATE INDEX IF NOT EXISTS idx_recent_c2_run_ancestor
ON c2_recent_ancestor(run_id, ancestor_uid);

CREATE INDEX IF NOT EXISTS idx_recent_c2_run_ambiguous
ON c2_recent_ancestor(run_id, ambiguous);
"""


def connect_db(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(
            f"SQLite cache not found: {path}\n"
            "Run ch11_outlier_radial_flocking.py once first."
        )

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA busy_timeout=60000")
    conn.executescript(EXTRA_SCHEMA)
    return conn


def latest_complete_run(conn: sqlite3.Connection, requested_run: int | None) -> int:
    if requested_run is not None:
        row = conn.execute(
            "SELECT id FROM experiment_runs WHERE id=? AND status='complete'",
            (requested_run,),
        ).fetchone()
        if not row:
            raise RuntimeError(
                f"run_id={requested_run} does not exist or is not complete"
            )
        return requested_run

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
        raise RuntimeError("No completed Outlier experiment exists in the database")

    return int(row[0])


def run_metadata(conn: sqlite3.Connection, run_id: int) -> dict:
    row = conn.execute(
        """
        SELECT size, generations, min_track_length
        FROM experiment_runs
        WHERE id=?
        """,
        (run_id,),
    ).fetchone()

    if not row:
        raise RuntimeError(f"Unknown run_id={run_id}")

    return {
        "size": int(row[0]),
        "generations": int(row[1]),
        "min_track_length": int(row[2]),
    }


# =====================================================================
# Most-recent c2 ancestry
# =====================================================================

def ancestry_is_cached(conn: sqlite3.Connection, run_id: int) -> bool:
    cluster_count = conn.execute(
        "SELECT COUNT(*) FROM clusters WHERE run_id=?",
        (run_id,),
    ).fetchone()[0]

    ancestry_count = conn.execute(
        "SELECT COUNT(*) FROM c2_recent_ancestor WHERE run_id=?",
        (run_id,),
    ).fetchone()[0]

    return int(cluster_count) > 0 and int(ancestry_count) == int(cluster_count)


def build_recent_c2_ancestry(
    conn: sqlite3.Connection,
    run_id: int,
    rebuild: bool = False,
) -> None:
    """
    Assign each cluster its nearest causal c2 ancestor.

    Because causal edges connect t -> t+1, we can process clusters in time
    order.

    Rules:
      * if the current cluster is c2, it becomes its own ancestor (distance 0)
      * otherwise inherit the parent candidate with minimum causal distance
      * if multiple equally-near parents imply different c2 ancestors,
        mark the result ambiguous rather than choosing arbitrarily
      * if no parent has a c2 ancestor, leave ancestor NULL

    This is "most recent c2 ancestor" in causal-step distance, not merely
    temporal proximity.
    """
    if rebuild:
        conn.execute(
            "DELETE FROM c2_recent_ancestor WHERE run_id=?",
            (run_id,),
        )
        conn.commit()

    if ancestry_is_cached(conn, run_id):
        print("Using cached most-recent c2 ancestry")
        return

    print("Computing most-recent causal c2 ancestor for every cluster ...")

    c2_set = {
        int(row[0])
        for row in conn.execute(
            "SELECT uid FROM c2_occurrences WHERE run_id=?",
            (run_id,),
        )
    }

    cluster_rows = list(
        conn.execute(
            """
            SELECT uid, time
            FROM clusters
            WHERE run_id=?
            ORDER BY time, uid
            """,
            (run_id,),
        )
    )

    parents: dict[int, list[int]] = defaultdict(list)

    for parent, child in conn.execute(
        """
        SELECT parent_uid, child_uid
        FROM causal_edges
        WHERE run_id=?
        ORDER BY parent_uid, child_uid
        """,
        (run_id,),
    ):
        parents[int(child)].append(int(parent))

    # uid -> (ancestor_uid | None, distance | None, ambiguous)
    assignment: dict[int, tuple[int | None, int | None, int]] = {}

    for uid, _time in tqdm(
        cluster_rows,
        desc="Assigning recent c2 ancestors",
        unit="cluster",
        dynamic_ncols=True,
    ):
        uid = int(uid)

        if uid in c2_set:
            assignment[uid] = (uid, 0, 0)
            continue

        candidates: list[tuple[int, int]] = []

        for parent in parents.get(uid, ()):
            ancestor, distance, ambiguous = assignment.get(
                parent,
                (None, None, 0),
            )

            if ambiguous:
                # Ambiguous parent does not give us a defensible family.
                continue

            if ancestor is not None and distance is not None:
                candidates.append((ancestor, distance + 1))

        if not candidates:
            assignment[uid] = (None, None, 0)
            continue

        min_distance = min(distance for _, distance in candidates)

        nearest_ancestors = {
            ancestor
            for ancestor, distance in candidates
            if distance == min_distance
        }

        if len(nearest_ancestors) == 1:
            assignment[uid] = (
                next(iter(nearest_ancestors)),
                min_distance,
                0,
            )
        else:
            assignment[uid] = (None, min_distance, 1)

    with conn:
        conn.execute(
            "DELETE FROM c2_recent_ancestor WHERE run_id=?",
            (run_id,),
        )

        conn.executemany(
            """
            INSERT INTO c2_recent_ancestor(
                run_id, uid, ancestor_uid, distance, ambiguous
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                (
                    run_id,
                    uid,
                    ancestor,
                    distance,
                    ambiguous,
                )
                for uid, (ancestor, distance, ambiguous) in assignment.items()
            ),
        )

    known = sum(
        1
        for ancestor, _distance, ambiguous in assignment.values()
        if ancestor is not None and not ambiguous
    )
    ambiguous = sum(
        1
        for _ancestor, _distance, flag in assignment.values()
        if flag
    )

    print(
        f"recent-c2 ancestry cached: "
        f"known={known:,} ambiguous={ambiguous:,} "
        f"unassigned={len(assignment) - known - ambiguous:,}"
    )


# =====================================================================
# Motion data
# =====================================================================

def load_motion_by_time(
    conn: sqlite3.Connection,
    run_id: int,
):
    """
    Load motion observations joined to the stronger recent-c2 ancestry table.

    family:
        integer c2 ancestor uid when unambiguous
        None otherwise
    """
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
          ON a.run_id=m.run_id AND a.uid=m.uid
        WHERE m.run_id=?
        ORDER BY m.time, m.track_id, m.seq
        """,
        (run_id,),
    )

    total = 0
    labelled = 0
    ambiguous = 0

    for time, uid, row, col, vr, vc, ancestor, ambiguity in cursor:
        velocity = np.array([vr, vc], dtype=np.float64)

        if np.linalg.norm(velocity) <= 1e-12:
            continue

        family = None

        if ambiguity:
            ambiguous += 1
        elif ancestor is not None:
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
        f"recent-c2 labelled: {labelled:,} ({labelled / max(total,1):.1%}) | "
        f"ambiguous: {ambiguous:,}"
    )

    return by_time


# =====================================================================
# Vector helpers
# =====================================================================

def unit_vectors(vectors: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    speeds = np.linalg.norm(vectors, axis=1)
    valid = speeds > 1e-12

    units = np.zeros_like(vectors)
    units[valid] = vectors[valid] / speeds[valid, None]

    return units, valid


def periodic_displacements(
    a: np.ndarray,
    b: np.ndarray,
    world_size: float,
) -> np.ndarray:
    delta = b - a
    return (delta + world_size / 2.0) % world_size - world_size / 2.0


def sample_pairs(
    pairs: np.ndarray,
    max_pairs: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if len(pairs) <= max_pairs:
        return pairs

    selected = rng.choice(
        len(pairs),
        size=max_pairs,
        replace=False,
    )

    return pairs[selected]


def accumulate(
    sums: np.ndarray,
    counts: np.ndarray,
    bins: np.ndarray,
    distances: np.ndarray,
    values: np.ndarray,
    mask: np.ndarray,
) -> None:
    if not np.any(mask):
        return

    distances = distances[mask]
    values = values[mask]

    indices = np.digitize(distances, bins) - 1

    valid = (
        (indices >= 0)
        & (indices < len(sums))
        & np.isfinite(values)
    )

    if not np.any(valid):
        return

    indices = indices[valid]
    values = values[valid]

    sums += np.bincount(
        indices,
        weights=values,
        minlength=len(sums),
    )[: len(sums)]

    counts += np.bincount(
        indices,
        minlength=len(sums),
    )[: len(sums)]


# =====================================================================
# Local background flow
# =====================================================================

def estimate_external_local_flow(
    positions: np.ndarray,
    velocities: np.ndarray,
    families: np.ndarray,
    world_size: int,
    radius: float,
    min_neighbors: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Estimate local environmental/background flow for every structure.

    Crucial detail:
        neighbours with the SAME known recent-c2 family are excluded.

    Therefore, when we subtract the local flow, we are not using obvious
    members of the focal structure's own causal family to define its
    environmental background.

    Returns:
        local_flow        shape (N, 2)
        valid_flow        shape (N,)
        neighbor_counts   shape (N,)
    """
    positions = positions % float(world_size)

    tree = cKDTree(
        positions,
        boxsize=float(world_size),
    )

    neighborhoods = tree.query_ball_point(
        positions,
        r=radius,
    )

    flow = np.zeros_like(velocities)
    valid = np.zeros(len(positions), dtype=bool)
    counts = np.zeros(len(positions), dtype=np.int32)

    for i, neighborhood in enumerate(neighborhoods):
        if not neighborhood:
            continue

        candidates = np.asarray(
            [j for j in neighborhood if j != i],
            dtype=np.int64,
        )

        if candidates.size == 0:
            continue

        focal_family = families[i]

        # If the focal structure has a known family, exclude same-family
        # neighbours. Unknown-family neighbours are retained as environmental
        # context because we cannot establish that they are the same entity.
        if focal_family >= 0:
            candidates = candidates[
                families[candidates] != focal_family
            ]

        if candidates.size < min_neighbors:
            continue

        flow[i] = velocities[candidates].mean(axis=0)
        counts[i] = int(candidates.size)
        valid[i] = True

    return flow, valid, counts


# =====================================================================
# Main experiment
# =====================================================================

def run_local_flow_family_test(
    by_time,
    world_size: int,
    pair_radius: float,
    flow_radius: float,
    flow_min_neighbors: int,
    n_bins: int,
    max_pairs_per_tick: int,
    shuffles: int,
    seed: int,
):
    rng = np.random.default_rng(seed)

    bins = np.linspace(
        0.0,
        pair_radius,
        n_bins + 1,
    )

    curve_names = [
        "raw_all",
        "local_residual_all",
        "local_residual_same_family",
        "local_residual_diff_family",
    ]

    sums = {
        name: np.zeros(n_bins, dtype=np.float64)
        for name in curve_names
    }
    counts = {
        name: np.zeros(n_bins, dtype=np.int64)
        for name in curve_names
    }

    # For shuffled controls we cache only sampled geometry and normalized
    # residual vectors. No spatial search is repeated.
    prepared: list[dict] = []

    total_pairs = 0
    total_flow_valid = 0
    total_points = 0
    total_family_pair = 0
    total_diff_family_pair = 0

    flow_neighbor_counts: list[int] = []

    for time, points in tqdm(
        sorted(by_time.items()),
        desc="Subtracting local flow + indexing pairs",
        unit="tick",
        dynamic_ncols=True,
    ):
        if len(points) < 2:
            continue

        positions = np.asarray(
            [point["position"] for point in points],
            dtype=np.float64,
        )

        velocities = np.asarray(
            [point["velocity"] for point in points],
            dtype=np.float64,
        )

        families = np.asarray(
            [
                -1 if point["family"] is None else point["family"]
                for point in points
            ],
            dtype=np.int64,
        )

        positions %= float(world_size)

        local_flow, flow_valid, neighbor_counts = estimate_external_local_flow(
            positions=positions,
            velocities=velocities,
            families=families,
            world_size=world_size,
            radius=flow_radius,
            min_neighbors=flow_min_neighbors,
        )

        residual = velocities - local_flow

        raw_units, raw_valid = unit_vectors(velocities)
        residual_units, residual_nonzero = unit_vectors(residual)

        residual_valid = flow_valid & residual_nonzero

        total_points += len(points)
        total_flow_valid += int(flow_valid.sum())

        flow_neighbor_counts.extend(
            neighbor_counts[flow_valid].tolist()
        )

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

        pairs = np.asarray(
            pair_set,
            dtype=np.int64,
        ).reshape(-1, 2)

        pairs = sample_pairs(
            pairs,
            max_pairs=max_pairs_per_tick,
            rng=rng,
        )

        i = pairs[:, 0]
        j = pairs[:, 1]

        delta = periodic_displacements(
            positions[i],
            positions[j],
            float(world_size),
        )

        distances = np.linalg.norm(
            delta,
            axis=1,
        )

        raw_alignment = np.sum(
            raw_units[i] * raw_units[j],
            axis=1,
        )

        residual_alignment = np.sum(
            residual_units[i] * residual_units[j],
            axis=1,
        )

        pair_raw_valid = raw_valid[i] & raw_valid[j]

        pair_residual_valid = (
            residual_valid[i]
            & residual_valid[j]
        )

        family_known = (
            (families[i] >= 0)
            & (families[j] >= 0)
        )

        same_family = (
            family_known
            & (families[i] == families[j])
        )

        diff_family = (
            family_known
            & (families[i] != families[j])
        )

        total_family_pair += int(
            (pair_residual_valid & family_known).sum()
        )

        total_diff_family_pair += int(
            (pair_residual_valid & diff_family).sum()
        )

        accumulate(
            sums["raw_all"],
            counts["raw_all"],
            bins,
            distances,
            raw_alignment,
            pair_raw_valid,
        )

        accumulate(
            sums["local_residual_all"],
            counts["local_residual_all"],
            bins,
            distances,
            residual_alignment,
            pair_residual_valid,
        )

        accumulate(
            sums["local_residual_same_family"],
            counts["local_residual_same_family"],
            bins,
            distances,
            residual_alignment,
            pair_residual_valid & same_family,
        )

        accumulate(
            sums["local_residual_diff_family"],
            counts["local_residual_diff_family"],
            bins,
            distances,
            residual_alignment,
            pair_residual_valid & diff_family,
        )

        prepared.append(
            {
                "pairs": pairs,
                "distances": distances,
                "residual_units": residual_units,
                "residual_valid": residual_valid,
            }
        )

        total_pairs += len(pairs)

    print(f"sampled nearby pairs: {total_pairs:,}")
    print(
        f"local-flow estimate available: "
        f"{total_flow_valid:,}/{total_points:,} "
        f"({total_flow_valid / max(total_points,1):.1%})"
    )
    print(f"known-family residual pairs: {total_family_pair:,}")
    print(f"DIFFERENT-family residual pairs: {total_diff_family_pair:,}")

    if flow_neighbor_counts:
        values = np.asarray(flow_neighbor_counts)
        print(
            "external-flow neighbours per usable observation: "
            f"median={np.median(values):.0f} "
            f"p10={np.percentile(values,10):.0f} "
            f"p90={np.percentile(values,90):.0f}"
        )

    means = {}

    for name in curve_names:
        means[name] = np.divide(
            sums[name],
            counts[name],
            out=np.full(n_bins, np.nan, dtype=np.float64),
            where=counts[name] > 0,
        )

    # -----------------------------------------------------------------
    # Null control
    #
    # Preserve:
    #   - exact time slice
    #   - positions
    #   - spatial pair geometry
    #   - distribution of local-flow residual directions
    #
    # Destroy:
    #   - which residual velocity belongs to which structure
    #
    # Geometry never gets recomputed.
    # -----------------------------------------------------------------

    null_curves = np.full(
        (shuffles, n_bins),
        np.nan,
        dtype=np.float64,
    )

    for shuffle_index in tqdm(
        range(shuffles),
        desc="Shuffling local-flow residuals",
        unit="shuffle",
        dynamic_ncols=True,
    ):
        null_sum = np.zeros(
            n_bins,
            dtype=np.float64,
        )
        null_count = np.zeros(
            n_bins,
            dtype=np.int64,
        )

        for item in prepared:
            units = item["residual_units"]
            valid = item["residual_valid"]
            pairs = item["pairs"]
            distances = item["distances"]

            permutation = rng.permutation(
                len(units)
            )

            shuffled_units = units[permutation]
            shuffled_valid = valid[permutation]

            i = pairs[:, 0]
            j = pairs[:, 1]

            pair_valid = (
                shuffled_valid[i]
                & shuffled_valid[j]
            )

            alignment = np.sum(
                shuffled_units[i]
                * shuffled_units[j],
                axis=1,
            )

            accumulate(
                null_sum,
                null_count,
                bins,
                distances,
                alignment,
                pair_valid,
            )

        null_curves[shuffle_index] = np.divide(
            null_sum,
            null_count,
            out=np.full(
                n_bins,
                np.nan,
                dtype=np.float64,
            ),
            where=null_count > 0,
        )

    with np.errstate(
        all="ignore",
    ):
        null_mean = np.nanmean(
            null_curves,
            axis=0,
        )

        null_low = np.nanpercentile(
            null_curves,
            5,
            axis=0,
        )

        null_high = np.nanpercentile(
            null_curves,
            95,
            axis=0,
        )

    return {
        "bins": bins.tolist(),
        "centres": (
            (bins[:-1] + bins[1:]) / 2.0
        ).tolist(),
        "means": {
            key: value.tolist()
            for key, value in means.items()
        },
        "counts": {
            key: value.tolist()
            for key, value in counts.items()
        },
        "null_mean": null_mean.tolist(),
        "null_low": null_low.tolist(),
        "null_high": null_high.tolist(),
        "sampled_pairs": int(total_pairs),
        "flow_valid": int(total_flow_valid),
        "motion_points": int(total_points),
        "known_family_pairs": int(total_family_pair),
        "diff_family_pairs": int(total_diff_family_pair),
    }


# =====================================================================
# Analysis cache
# =====================================================================

def make_analysis_key(params: dict) -> str:
    encoded = json.dumps(
        params,
        sort_keys=True,
    ).encode("utf-8")

    digest = hashlib.sha256(
        encoded
    ).hexdigest()[:20]

    return f"local-flow-recent-c2-v1-{digest}"


def load_analysis(
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

    return (
        json.loads(row[0])
        if row
        else None
    )


def store_analysis(
    conn: sqlite3.Connection,
    run_id: int,
    key: str,
    params: dict,
    result: dict,
) -> None:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO analysis_results(
                run_id,
                analysis_key,
                params_json,
                result_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?)
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

def build_family_coverage_figure(
    conn: sqlite3.Connection,
    run_id: int,
) -> Path:
    rows = conn.execute(
        """
        SELECT
            CASE
                WHEN a.ambiguous=1 THEN 'Ambiguous ancestry'
                WHEN a.ancestor_uid IS NOT NULL THEN 'Known recent c2 ancestor'
                ELSE 'No c2 ancestor assigned'
            END AS category,
            COUNT(*)
        FROM motion_points AS m
        LEFT JOIN c2_recent_ancestor AS a
          ON a.run_id=m.run_id AND a.uid=m.uid
        WHERE m.run_id=?
        GROUP BY category
        """,
        (run_id,),
    ).fetchall()

    labels = [
        str(row[0])
        for row in rows
    ]

    values = np.asarray(
        [int(row[1]) for row in rows],
        dtype=np.int64,
    )

    fig, ax = plt.subplots(
        figsize=(9, 5),
    )

    bars = ax.bar(
        labels,
        values,
    )

    ax.set_title(
        "Outlier: Coverage of Most-Recent c2 Ancestry"
    )

    ax.set_ylabel(
        "Motion observations"
    )

    ax.tick_params(
        axis="x",
        rotation=15,
    )

    total = int(
        values.sum()
    )

    for bar, value in zip(
        bars,
        values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,}\n({value / max(total,1):.1%})",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch11-outlier-family-coverage.png"
    )

    fig.savefig(
        path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")

    return path


def build_main_figure(
    result: dict,
    min_pairs: int,
) -> Path:
    centres = np.asarray(
        result["centres"],
        dtype=np.float64,
    )

    curves = {
        "Raw motion": (
            "raw_all",
            "raw",
        ),
        "After local-flow subtraction": (
            "local_residual_all",
            "residual",
        ),
        "Residual: same recent-c2 family": (
            "local_residual_same_family",
            "same",
        ),
        "Residual: different recent-c2 families": (
            "local_residual_diff_family",
            "different",
        ),
    }

    fig, ax = plt.subplots(
        figsize=(12, 7),
    )

    for label, (
        key,
        _short,
    ) in curves.items():
        values = np.asarray(
            result["means"][key],
            dtype=np.float64,
        )

        counts = np.asarray(
            result["counts"][key],
            dtype=np.int64,
        )

        valid = (
            (counts >= min_pairs)
            & np.isfinite(values)
        )

        if np.any(valid):
            ax.plot(
                centres[valid],
                values[valid],
                marker="o",
                label=label,
            )

            for x, y, n in zip(
                centres[valid],
                values[valid],
                counts[valid],
            ):
                ax.annotate(
                    f"n={n:,}",
                    (x, y),
                    xytext=(0, 7),
                    textcoords="offset points",
                    ha="center",
                    fontsize=7,
                )

    null_mean = np.asarray(
        result["null_mean"],
        dtype=np.float64,
    )

    null_low = np.asarray(
        result["null_low"],
        dtype=np.float64,
    )

    null_high = np.asarray(
        result["null_high"],
        dtype=np.float64,
    )

    valid_null = np.isfinite(
        null_mean
    )

    ax.plot(
        centres[valid_null],
        null_mean[valid_null],
        linestyle="--",
        label="Shuffled local-residual control",
    )

    ax.fill_between(
        centres[valid_null],
        null_low[valid_null],
        null_high[valid_null],
        alpha=0.18,
        label="Control 5–95%",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_ylim(
        -1.05,
        1.05,
    )

    ax.set_xlabel(
        "Distance between simultaneously moving clusters"
    )

    ax.set_ylabel(
        "Velocity alignment (1=same direction, -1=opposite)"
    )

    ax.set_title(
        "Outlier: Does Coherence Survive Local-Flow Subtraction?"
    )

    ax.grid(
        alpha=0.25,
    )

    ax.legend()

    note = (
        f"Pairs sampled: {result['sampled_pairs']:,}. "
        f"Local-flow residual available for "
        f"{result['flow_valid']:,}/{result['motion_points']:,} observations. "
        f"Different-family residual pairs: {result['diff_family_pairs']:,}."
    )

    fig.text(
        0.5,
        0.01,
        note,
        ha="center",
        fontsize=9,
    )

    fig.tight_layout(
        rect=(0, 0.04, 1, 1),
    )

    path = (
        OUTPUT_DIR
        / "ch11-outlier-local-flow-family-test.png"
    )

    fig.savefig(
        path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")

    return path


# =====================================================================
# CLI
# =====================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Analyze cached Outlier motion using most-recent c2 ancestry "
            "and local-background-flow subtraction"
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
        help="Completed cached run to analyze. Defaults to latest.",
    )

    parser.add_argument(
        "--pair-radius",
        type=float,
        default=96.0,
        help="Maximum distance for the pairwise alignment test.",
    )

    parser.add_argument(
        "--flow-radius",
        type=float,
        default=48.0,
        help="Radius used to estimate the local external background flow.",
    )

    parser.add_argument(
        "--flow-min-neighbors",
        type=int,
        default=3,
        help="Minimum external-family neighbors required to estimate local flow.",
    )

    parser.add_argument(
        "--bins",
        type=int,
        default=6,
    )

    parser.add_argument(
        "--max-pairs-per-tick",
        type=int,
        default=10_000,
    )

    parser.add_argument(
        "--shuffles",
        type=int,
        default=50,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--min-pairs",
        type=int,
        default=100,
        help="Minimum observations required before plotting a bin.",
    )

    parser.add_argument(
        "--rebuild-ancestry",
        action="store_true",
        help="Recompute the recent-c2 ancestry table, not the CA simulation.",
    )

    parser.add_argument(
        "--reanalyze",
        action="store_true",
        help="Ignore a matching cached numerical analysis.",
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
        f"Using cached Outlier run_id={run_id} "
        f"size={metadata['size']} "
        f"generations={metadata['generations']}"
    )

    build_recent_c2_ancestry(
        conn,
        run_id,
        rebuild=args.rebuild_ancestry,
    )

    build_family_coverage_figure(
        conn,
        run_id,
    )

    params = {
        "pair_radius": args.pair_radius,
        "flow_radius": args.flow_radius,
        "flow_min_neighbors": args.flow_min_neighbors,
        "bins": args.bins,
        "max_pairs_per_tick": args.max_pairs_per_tick,
        "shuffles": args.shuffles,
        "seed": args.seed,
        "analysis_version": 1,
    }

    key = make_analysis_key(
        params
    )

    result = (
        None
        if args.reanalyze
        else load_analysis(
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

        result = run_local_flow_family_test(
            by_time=by_time,
            world_size=metadata["size"],
            pair_radius=args.pair_radius,
            flow_radius=args.flow_radius,
            flow_min_neighbors=args.flow_min_neighbors,
            n_bins=args.bins,
            max_pairs_per_tick=args.max_pairs_per_tick,
            shuffles=args.shuffles,
            seed=args.seed,
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
        result,
        min_pairs=args.min_pairs,
    )

    print()
    print("First distance-bin results:")

    labels = [
        ("raw_all", "raw"),
        (
            "local_residual_all",
            "local-flow residual",
        ),
        (
            "local_residual_same_family",
            "same recent-c2 family",
        ),
        (
            "local_residual_diff_family",
            "different recent-c2 families",
        ),
    ]

    for key_name, label in labels:
        values = result["means"][key_name]
        counts = result["counts"][key_name]

        value = (
            values[0]
            if values
            else None
        )

        count = (
            counts[0]
            if counts
            else 0
        )

        print(
            f"  {label:30s} "
            f"alignment={str(value):>12s} "
            f"n={count:,}"
        )

    print(
        f"  {'shuffled residual control':30s} "
        f"alignment={str(result['null_mean'][0]):>12s}"
    )

    print()
    print(
        "Interpretation target:"
    )
    print(
        "  If different-family residual alignment remains well above the "
        "shuffled control after local-flow subtraction, the motion coherence "
        "cannot be explained solely by global expansion, local background "
        "flow, or obvious membership in the same recent-c2 causal family."
    )


if __name__ == "__main__":
    main()
