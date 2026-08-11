from __future__ import annotations

"""
Chapter 11 — Outlier causal relatedness vs motion coherence.

ANALYSIS ONLY.
Reuses the SQLite cache produced by the previous Outlier experiments.

No CA simulation is rerun.

Primary questions
=================

A. Pair-excluded local-flow test
--------------------------------
When comparing two moving structures A and B, estimate the local background
flow while excluding BOTH of their recent-c2 families.

This fixes the main confound in the previous analysis, where A could
contribute to B's background estimate and vice versa, artificially creating
anti-correlation.

B. Causal relatedness vs velocity coherence
-------------------------------------------
For each nearby pair with known recent-c2 ancestry, measure how recently
their c2 ancestors share a common causal ancestor.

Then ask:

    does closer causal relatedness predict stronger motion coherence?

If yes, causal organization has an independently measurable dynamical
signature.

Expected database
=================

    data/digital-life/outlier.sqlite3

Expected tables already present:

    experiment_runs
    clusters
    causal_edges
    c2_occurrences
    c2_recent_ancestor
    motion_points
    analysis_results

Outputs
=======

    static/images/books/digital-life/
        ch11-outlier-pair-excluded-flow.png
        ch11-outlier-relatedness-coherence.png

The numerical result is cached in analysis_results.
"""

import argparse
import hashlib
import json
import math
import sqlite3
from collections import defaultdict, deque
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
# SQLite helpers
# =====================================================================

def connect_db(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(
            f"Database not found: {path}\n"
            "Run ch11_outlier_radial_flocking.py first."
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
        """
        SELECT size, generations
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
    }


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type='table' AND name=?
        """,
        (name,),
    ).fetchone()
    return row is not None


# =====================================================================
# Load c2 ancestry graph
# =====================================================================

def load_c2_parent_graph(
    conn: sqlite3.Connection,
    run_id: int,
):
    """
    Collapse causal history to a graph between c2 occurrences.

    We already have c2_return_edges from the previous analysis.
    Each edge means a c2 occurrence causally reaches another c2 occurrence
    before encountering another c2 on that branch.

    Returns:
        parents: child_c2 -> set(parent_c2)
        children: parent_c2 -> set(child_c2)
    """
    parents: dict[int, set[int]] = defaultdict(set)
    children: dict[int, set[int]] = defaultdict(set)

    for parent, child in conn.execute(
        """
        SELECT parent_uid, child_uid
        FROM c2_return_edges
        WHERE run_id=?
        """,
        (run_id,),
    ):
        parent = int(parent)
        child = int(child)
        parents[child].add(parent)
        children[parent].add(child)

    return parents, children


def load_c2_times(
    conn: sqlite3.Connection,
    run_id: int,
) -> dict[int, int]:
    return {
        int(uid): int(time)
        for uid, time in conn.execute(
            """
            SELECT uid, time
            FROM c2_occurrences
            WHERE run_id=?
            """,
            (run_id,),
        )
    }


def compute_c2_ancestor_sets(
    c2_uids: list[int],
    parents: dict[int, set[int]],
    times: dict[int, int],
):
    """
    For each c2 node, compute shortest backward distance to all c2 ancestors.

    Number of c2 nodes is small (~144 in current run), so this is cheap.

    distances[node][ancestor] = minimum c2-edge distance backward.
    """
    distances: dict[int, dict[int, int]] = {}

    for node in tqdm(
        c2_uids,
        desc="Indexing c2 ancestry",
        unit="c2",
        dynamic_ncols=True,
    ):
        d: dict[int, int] = {node: 0}
        queue = deque([node])

        while queue:
            current = queue.popleft()
            base = d[current]

            for parent in parents.get(current, ()):
                candidate = base + 1
                old = d.get(parent)

                if old is None or candidate < old:
                    d[parent] = candidate
                    queue.append(parent)

        distances[node] = d

    return distances


def pair_relatedness(
    a: int,
    b: int,
    ancestor_distances: dict[int, dict[int, int]],
    c2_times: dict[int, int],
) -> tuple[int | None, int | None]:
    """
    Return:
        combined_distance:
            minimum da + db to a shared c2 ancestor

        common_ancestor_time:
            latest-time common ancestor among those with minimum distance

    same recent-c2 family => distance 0.
    sibling branches often => distance 2.
    more distant relationship => larger values.

    None means no shared c2 ancestor in our reconstructed graph.
    """
    if a == b:
        return 0, c2_times.get(a)

    da = ancestor_distances.get(a)
    db = ancestor_distances.get(b)

    if not da or not db:
        return None, None

    common = da.keys() & db.keys()

    if not common:
        return None, None

    best_distance = min(
        da[x] + db[x]
        for x in common
    )

    best_common = [
        x
        for x in common
        if da[x] + db[x] == best_distance
    ]

    latest = max(
        (c2_times.get(x, -1) for x in best_common),
        default=-1,
    )

    return int(best_distance), int(latest)


# =====================================================================
# Motion loading
# =====================================================================

def load_motion_by_time(
    conn: sqlite3.Connection,
    run_id: int,
):
    if not table_exists(conn, "c2_recent_ancestor"):
        raise RuntimeError(
            "c2_recent_ancestor table is missing.\n"
            "Run ch11_outlier_local_flow.py once first."
        )

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
    known = 0

    for time, uid, row, col, vr, vc, ancestor, ambiguous in cursor:
        velocity = np.array(
            [vr, vc],
            dtype=np.float64,
        )

        if np.linalg.norm(velocity) <= 1e-12:
            continue

        family = None

        if not ambiguous and ancestor is not None:
            family = int(ancestor)
            known += 1

        by_time[int(time)].append(
            {
                "uid": int(uid),
                "position": np.array(
                    [row, col],
                    dtype=np.float64,
                ),
                "velocity": velocity,
                "family": family,
            }
        )

        total += 1

    print(
        f"motion observations: {total:,} | "
        f"known recent-c2 family: {known:,} ({known / max(total,1):.1%})"
    )

    return by_time


# =====================================================================
# Geometry / vector helpers
# =====================================================================

def unit_vectors(vectors: np.ndarray):
    norms = np.linalg.norm(
        vectors,
        axis=1,
    )

    valid = norms > 1e-12

    units = np.zeros_like(vectors)

    units[valid] = (
        vectors[valid]
        / norms[valid, None]
    )

    return units, valid


def periodic_delta(
    a: np.ndarray,
    b: np.ndarray,
    world_size: float,
) -> np.ndarray:
    delta = b - a

    return (
        delta + world_size / 2.0
    ) % world_size - world_size / 2.0


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


# =====================================================================
# Pair-excluded local background flow
# =====================================================================

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
    For each tested pair (i,j):

        background_i = mean velocity of neighbors near i
                       excluding family(i) AND family(j)

        background_j = mean velocity of neighbors near j
                       excluding family(i) AND family(j)

    Thus neither member's causal family can contaminate the other's
    background estimate.

    This explicitly fixes the anti-correlation confound in the previous
    experiment.

    Returns:
        residual_i
        residual_j
        valid
        background_neighbor_counts_i
        background_neighbor_counts_j
    """
    n_pairs = len(pairs)

    residual_i = np.zeros(
        (n_pairs, 2),
        dtype=np.float64,
    )

    residual_j = np.zeros(
        (n_pairs, 2),
        dtype=np.float64,
    )

    valid = np.zeros(
        n_pairs,
        dtype=bool,
    )

    count_i = np.zeros(
        n_pairs,
        dtype=np.int32,
    )

    count_j = np.zeros(
        n_pairs,
        dtype=np.int32,
    )

    # Cache neighborhood lists per point once per time slice.
    neighborhoods = tree.query_ball_point(
        positions,
        r=flow_radius,
    )

    for k, (i, j) in enumerate(pairs):
        fi = families[i]
        fj = families[j]

        excluded_families = {
            f
            for f in (fi, fj)
            if f >= 0
        }

        ni = [
            x
            for x in neighborhoods[i]
            if x != i
            and x != j
            and (
                families[x] < 0
                or families[x] not in excluded_families
            )
        ]

        nj = [
            x
            for x in neighborhoods[j]
            if x != i
            and x != j
            and (
                families[x] < 0
                or families[x] not in excluded_families
            )
        ]

        if (
            len(ni) < min_neighbors
            or len(nj) < min_neighbors
        ):
            continue

        background_i = velocities[
            np.asarray(ni, dtype=np.int64)
        ].mean(axis=0)

        background_j = velocities[
            np.asarray(nj, dtype=np.int64)
        ].mean(axis=0)

        residual_i[k] = (
            velocities[i] - background_i
        )

        residual_j[k] = (
            velocities[j] - background_j
        )

        count_i[k] = len(ni)
        count_j[k] = len(nj)
        valid[k] = True

    return (
        residual_i,
        residual_j,
        valid,
        count_i,
        count_j,
    )


# =====================================================================
# Analysis aggregation
# =====================================================================

def relation_bucket(distance: int | None) -> str:
    if distance is None:
        return "unrelated"

    if distance == 0:
        return "same_family"

    if distance <= 2:
        return "very_close"

    if distance <= 4:
        return "close"

    if distance <= 8:
        return "distant"

    return "very_distant"


RELATION_ORDER = [
    "same_family",
    "very_close",
    "close",
    "distant",
    "very_distant",
    "unrelated",
]

RELATION_LABELS = {
    "same_family": "Same recent c2 ancestor",
    "very_close": "Very close c2 ancestry",
    "close": "Close c2 ancestry",
    "distant": "Distant c2 ancestry",
    "very_distant": "Very distant c2 ancestry",
    "unrelated": "No shared c2 ancestor found",
}


def run_experiment(
    by_time,
    world_size: int,
    c2_ancestor_distances,
    c2_times,
    pair_radius: float,
    flow_radius: float,
    flow_min_neighbors: int,
    max_pairs_per_tick: int,
    seed: int,
):
    rng = np.random.default_rng(seed)

    # Store pair-level summary samples rather than millions of raw vectors.
    by_relation = {
        name: {
            "alignment_sum": 0.0,
            "count": 0,
            "distance_sum": 0.0,
        }
        for name in RELATION_ORDER
    }

    # Spatial-distance curve for pair-excluded residual alignment.
    spatial_bins = np.linspace(
        0.0,
        pair_radius,
        7,
    )

    spatial_sum = np.zeros(
        len(spatial_bins) - 1,
        dtype=np.float64,
    )

    spatial_count = np.zeros(
        len(spatial_bins) - 1,
        dtype=np.int64,
    )

    # Raw control for comparison.
    raw_sum = np.zeros_like(
        spatial_sum
    )

    raw_count = np.zeros_like(
        spatial_count
    )

    tested_pairs = 0
    usable_pairs = 0
    known_family_pairs = 0
    unrelated_pairs = 0

    neighbor_counts = []

    for time, points in tqdm(
        sorted(by_time.items()),
        desc="Pair-excluded flow + causal relatedness",
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
                -1 if p["family"] is None
                else int(p["family"])
                for p in points
            ],
            dtype=np.int64,
        )

        positions %= float(
            world_size
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

        tested_pairs += len(
            pairs
        )

        i = pairs[:, 0]
        j = pairs[:, 1]

        delta = periodic_delta(
            positions[i],
            positions[j],
            float(world_size),
        )

        distances = np.linalg.norm(
            delta,
            axis=1,
        )

        raw_units, raw_valid = unit_vectors(
            velocities
        )

        raw_alignment = np.sum(
            raw_units[i]
            * raw_units[j],
            axis=1,
        )

        (
            residual_i,
            residual_j,
            flow_valid,
            n_i,
            n_j,
        ) = pair_excluded_residuals(
            positions=positions,
            velocities=velocities,
            families=families,
            pairs=pairs,
            tree=tree,
            flow_radius=flow_radius,
            min_neighbors=flow_min_neighbors,
        )

        ri_units, ri_valid = unit_vectors(
            residual_i
        )

        rj_units, rj_valid = unit_vectors(
            residual_j
        )

        valid = (
            flow_valid
            & ri_valid
            & rj_valid
        )

        usable_pairs += int(
            valid.sum()
        )

        if np.any(valid):
            neighbor_counts.extend(
                np.minimum(
                    n_i[valid],
                    n_j[valid],
                ).tolist()
            )

        residual_alignment = np.sum(
            ri_units
            * rj_units,
            axis=1,
        )

        # Spatial aggregation.
        spatial_idx = np.digitize(
            distances,
            spatial_bins,
        ) - 1

        raw_pair_valid = (
            raw_valid[i]
            & raw_valid[j]
        )

        for b in range(
            len(spatial_sum)
        ):
            mask_raw = (
                raw_pair_valid
                & (spatial_idx == b)
            )

            if np.any(mask_raw):
                raw_sum[b] += float(
                    raw_alignment[
                        mask_raw
                    ].sum()
                )

                raw_count[b] += int(
                    mask_raw.sum()
                )

            mask_residual = (
                valid
                & (spatial_idx == b)
            )

            if np.any(mask_residual):
                spatial_sum[b] += float(
                    residual_alignment[
                        mask_residual
                    ].sum()
                )

                spatial_count[b] += int(
                    mask_residual.sum()
                )

        # Causal-relatedness aggregation.
        valid_indices = np.flatnonzero(
            valid
        )

        for k in valid_indices:
            fi = int(
                families[i[k]]
            )

            fj = int(
                families[j[k]]
            )

            if fi < 0 or fj < 0:
                continue

            known_family_pairs += 1

            rel_distance, _common_time = pair_relatedness(
                fi,
                fj,
                c2_ancestor_distances,
                c2_times,
            )

            bucket = relation_bucket(
                rel_distance
            )

            if bucket == "unrelated":
                unrelated_pairs += 1

            entry = by_relation[
                bucket
            ]

            entry[
                "alignment_sum"
            ] += float(
                residual_alignment[k]
            )

            entry[
                "distance_sum"
            ] += float(
                distances[k]
            )

            entry["count"] += 1

    print(
        f"tested nearby pairs: {tested_pairs:,}"
    )

    print(
        f"usable pair-excluded residual pairs: "
        f"{usable_pairs:,} "
        f"({usable_pairs / max(tested_pairs,1):.1%})"
    )

    print(
        f"known-family usable pairs: "
        f"{known_family_pairs:,}"
    )

    print(
        f"no-shared-c2-ancestor pairs: "
        f"{unrelated_pairs:,}"
    )

    if neighbor_counts:
        values = np.asarray(
            neighbor_counts
        )

        print(
            "pair-excluded background neighbors: "
            f"median={np.median(values):.0f} "
            f"p10={np.percentile(values,10):.0f} "
            f"p90={np.percentile(values,90):.0f}"
        )

    relation_result = {}

    for name in RELATION_ORDER:
        entry = by_relation[
            name
        ]

        count = entry[
            "count"
        ]

        relation_result[
            name
        ] = {
            "count": int(count),
            "mean_alignment": (
                entry["alignment_sum"]
                / count
                if count
                else None
            ),
            "mean_spatial_distance": (
                entry["distance_sum"]
                / count
                if count
                else None
            ),
        }

    raw_mean = np.divide(
        raw_sum,
        raw_count,
        out=np.full(
            len(raw_sum),
            np.nan,
        ),
        where=raw_count > 0,
    )

    residual_mean = np.divide(
        spatial_sum,
        spatial_count,
        out=np.full(
            len(spatial_sum),
            np.nan,
        ),
        where=spatial_count > 0,
    )

    return {
        "relation": relation_result,
        "spatial_bins": spatial_bins.tolist(),
        "spatial_centres": (
            (
                spatial_bins[:-1]
                + spatial_bins[1:]
            ) / 2
        ).tolist(),
        "raw_spatial_alignment": raw_mean.tolist(),
        "raw_spatial_counts": raw_count.tolist(),
        "pair_excluded_spatial_alignment": residual_mean.tolist(),
        "pair_excluded_spatial_counts": spatial_count.tolist(),
        "tested_pairs": int(tested_pairs),
        "usable_pairs": int(usable_pairs),
        "known_family_pairs": int(known_family_pairs),
        "unrelated_pairs": int(unrelated_pairs),
    }


# =====================================================================
# Cache results
# =====================================================================

def analysis_key(
    params: dict,
) -> str:
    payload = json.dumps(
        params,
        sort_keys=True,
    ).encode(
        "utf-8"
    )

    digest = hashlib.sha256(
        payload
    ).hexdigest()[:20]

    return (
        "pair-excluded-causal-motion-v1-"
        + digest
    )


def load_cached_analysis(
    conn,
    run_id,
    key,
):
    row = conn.execute(
        """
        SELECT result_json
        FROM analysis_results
        WHERE run_id=? AND analysis_key=?
        """,
        (
            run_id,
            key,
        ),
    ).fetchone()

    if not row:
        return None

    return json.loads(
        row[0]
    )


def store_analysis(
    conn,
    run_id,
    key,
    params,
    result,
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
                json.dumps(
                    result
                ),
                datetime.now(
                    timezone.utc
                ).isoformat(),
            ),
        )


# =====================================================================
# Figures
# =====================================================================

def build_pair_excluded_figure(
    result: dict,
    min_pairs: int,
):
    centres = np.asarray(
        result[
            "spatial_centres"
        ],
        dtype=np.float64,
    )

    raw = np.asarray(
        result[
            "raw_spatial_alignment"
        ],
        dtype=np.float64,
    )

    raw_n = np.asarray(
        result[
            "raw_spatial_counts"
        ],
        dtype=np.int64,
    )

    residual = np.asarray(
        result[
            "pair_excluded_spatial_alignment"
        ],
        dtype=np.float64,
    )

    residual_n = np.asarray(
        result[
            "pair_excluded_spatial_counts"
        ],
        dtype=np.int64,
    )

    fig, ax = plt.subplots(
        figsize=(11, 6),
    )

    valid_raw = (
        (raw_n >= min_pairs)
        & np.isfinite(raw)
    )

    valid_residual = (
        (residual_n >= min_pairs)
        & np.isfinite(residual)
    )

    ax.plot(
        centres[valid_raw],
        raw[valid_raw],
        marker="o",
        label="Raw velocity alignment",
    )

    ax.plot(
        centres[
            valid_residual
        ],
        residual[
            valid_residual
        ],
        marker="o",
        label=(
            "Pair-excluded "
            "local-flow residual"
        ),
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
        "Velocity alignment"
    )

    ax.set_title(
        "Outlier: Motion Coherence After Pair-Excluded Local-Flow Subtraction"
    )

    ax.grid(
        alpha=0.25
    )

    ax.legend()

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch11-outlier-pair-excluded-flow.png"
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


def build_relatedness_figure(
    result: dict,
    min_pairs: int,
):
    labels = []
    values = []
    counts = []

    for key in RELATION_ORDER:
        entry = result[
            "relation"
        ][key]

        if (
            entry["count"]
            < min_pairs
            or entry[
                "mean_alignment"
            ] is None
        ):
            continue

        labels.append(
            RELATION_LABELS[
                key
            ]
        )

        values.append(
            entry[
                "mean_alignment"
            ]
        )

        counts.append(
            entry[
                "count"
            ]
        )

    fig, ax = plt.subplots(
        figsize=(11, 6),
    )

    x = np.arange(
        len(labels)
    )

    bars = ax.bar(
        x,
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

    ax.set_xticks(
        x
    )

    ax.set_xticklabels(
        labels,
        rotation=18,
        ha="right",
    )

    ax.set_ylabel(
        "Pair-excluded residual velocity alignment"
    )

    ax.set_title(
        "Outlier: Does Causal Relatedness Predict Motion Coherence?"
    )

    ax.grid(
        axis="y",
        alpha=0.25,
    )

    for bar, value, count in zip(
        bars,
        values,
        counts,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            value
            + (
                0.03
                if value >= 0
                else -0.08
            ),
            f"{value:.3f}\nn={count:,}",
            ha="center",
            va=(
                "bottom"
                if value >= 0
                else "top"
            ),
            fontsize=9,
        )

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch11-outlier-relatedness-coherence.png"
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
            "Test pair-excluded local flow and causal-relatedness "
            "motion coherence using cached Outlier data"
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
        "--flow-min-neighbors",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--max-pairs-per-tick",
        type=int,
        default=4_000,
        help=(
            "Pair-excluded background estimation is more expensive than "
            "the previous vectorized analyses. 4000/tick is already a "
            "large deterministic sample."
        ),
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

    by_time = load_motion_by_time(
        conn,
        run_id,
    )

    c2_parents, _c2_children = load_c2_parent_graph(
        conn,
        run_id,
    )

    c2_times = load_c2_times(
        conn,
        run_id,
    )

    c2_uids = sorted(
        c2_times,
        key=lambda uid: (
            c2_times[uid],
            uid,
        ),
    )

    c2_ancestor_distances = compute_c2_ancestor_sets(
        c2_uids,
        c2_parents,
        c2_times,
    )

    params = {
        "pair_radius": args.pair_radius,
        "flow_radius": args.flow_radius,
        "flow_min_neighbors": args.flow_min_neighbors,
        "max_pairs_per_tick": args.max_pairs_per_tick,
        "seed": args.seed,
        "analysis_version": 1,
    }

    key = analysis_key(
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
        result = run_experiment(
            by_time=by_time,
            world_size=metadata[
                "size"
            ],
            c2_ancestor_distances=c2_ancestor_distances,
            c2_times=c2_times,
            pair_radius=args.pair_radius,
            flow_radius=args.flow_radius,
            flow_min_neighbors=args.flow_min_neighbors,
            max_pairs_per_tick=args.max_pairs_per_tick,
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

    build_pair_excluded_figure(
        result,
        min_pairs=args.min_pairs,
    )

    build_relatedness_figure(
        result,
        min_pairs=args.min_pairs,
    )

    print()
    print(
        "Causal relatedness results:"
    )

    for key_name in RELATION_ORDER:
        entry = result[
            "relation"
        ][key_name]

        print(
            f"  {RELATION_LABELS[key_name]:32s} "
            f"alignment={str(entry['mean_alignment']):>12s} "
            f"n={entry['count']:,} "
            f"mean_distance={str(entry['mean_spatial_distance']):>12s}"
        )

    print()
    print(
        "Interpretation:"
    )

    print(
        "  1. If different-family anti-alignment disappears under the "
        "pair-excluded background, the previous negative value was an "
        "estimator artifact."
    )

    print(
        "  2. If alignment decreases systematically as c2 causal "
        "relatedness becomes more distant, then causal organization "
        "predicts an independent dynamical property: coherent motion."
    )

    print(
        "  3. If even causally unrelated structures remain strongly "
        "aligned after pair-excluded flow subtraction, that would be "
        "the strongest evidence so far for genuine collective motion "
        "between distinct digital organizations."
    )


if __name__ == "__main__":
    main()
