#!/usr/bin/env python3
"""
Chapter 13 — Outlier overlap / positivity hardening analysis v2
===============================================================

This version is designed for the ACTUAL Chapter 13 research pipeline.

It does NOT assume a pre-existing `pair_records` table.

Instead it:

1. Opens the canonical Outlier SQLite specimen:
       data/digital-life/outlier.sqlite3

2. Reuses the EXACT pair-construction and matching code from:
       ch11_outlier_distance_matched.py

   That preserves the original Chapter 13 definitions:
       pair radius             96
       pair-excluded flow      radius 48
       density radius          32
       minimum flow neighbors  3
       max pairs per tick      2500
       time-bin width          25
       distance edges          [0,4,8,12,16,24,32,48,64,96]
       max matches/stratum     5000
       seed                    42

3. Persists the expensive derived pair dataset into SQLite as:
       ch13_pair_datasets
       ch13_pair_records

   so the intermediate scientific evidence is not lost again.

4. Audits overlap / positivity between:
       same recent-c2 family
       different recent-c2 family

5. Defines common support using an explicit operational rule.

6. Reports THREE distinct estimands:
       A. raw descriptive effect inside support
       B. balanced matched pooled effect using the ORIGINAL matching code
       C. equal-stratum matched effect + bootstrap CI using the ORIGINAL code

7. Runs support-threshold sensitivity:
       min rows/group/bin = 50, 100, 250, 500
   unless overridden.

8. Quantifies how large a positive ancestry effect remains compatible with
   the matched common-support data relative to the original apparent gap:
       0.746 - 0.101 = 0.645

9. Writes:
       Markdown report
       JSON report
       distance-bin CSV
       sensitivity CSV
       two figures

Important scientific scope
--------------------------
This hardens inference for the existing Chapter 13 experiment only.

It does NOT resolve the separate scale limitation:

    Chapter 13 run:
        512 x 512
        1,600 generations

    published causal Outlier study:
        1024 x 1024
        20,000 updates

Prerequisite
------------
The database must contain `c2_recent_ancestor`.

If it does not, run:

    python scripts/books/digital-life/ch11_outlier_local_flow.py

first.

Typical run
-----------
    python scripts/books/digital-life/ch13_outlier_overlap_analysis.py

Force pair reconstruction
-------------------------
    python scripts/books/digital-life/ch13_outlier_overlap_analysis.py --rebuild-pairs

Dependencies
------------
numpy
pandas
matplotlib
scipy
tqdm
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# CRITICAL: reuse the original Chapter 13 implementation rather than silently
# reimplementing its pair construction / matched estimator.
# ---------------------------------------------------------------------------

try:
    import ch11_outlier_distance_matched as original
except ImportError as exc:
    raise SystemExit(
        "Could not import ch11_outlier_distance_matched.py.\n"
        "Place this script in the same scripts/books/digital-life directory."
    ) from exc


ANALYSIS_VERSION = "ch13-overlap-v2"
PAIR_DATASET_VERSION = "ch13-pairs-v1"

DEFAULT_DB = Path("data/digital-life/outlier.sqlite3")
DEFAULT_REPORTS = Path("research/digital-life/ch13-reports")
DEFAULT_IMAGES = Path("static/images/books/digital-life")

DISTANCE_EDGES = [
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

DEFAULT_SUPPORT_THRESHOLDS = [50, 100, 250, 500]


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass(frozen=True)
class PairParams:
    pair_radius: float = 96.0
    flow_radius: float = 48.0
    density_radius: float = 32.0
    flow_min_neighbors: int = 3
    max_pairs_per_tick: int = 2500
    time_bin_width: int = 25
    max_matches_per_stratum: int = 5000
    seed: int = 42

    def pair_key_payload(self, run_id: int) -> dict:
        return {
            "run_id": run_id,
            "pair_radius": self.pair_radius,
            "flow_radius": self.flow_radius,
            "density_radius": self.density_radius,
            "flow_min_neighbors": self.flow_min_neighbors,
            "max_pairs_per_tick": self.max_pairs_per_tick,
            "time_bin_width": self.time_bin_width,
            "distance_edges": DISTANCE_EDGES,
            "seed": self.seed,
            "pair_dataset_version": PAIR_DATASET_VERSION,
        }


@dataclass(frozen=True)
class Support:
    threshold: int
    lower: float
    upper: float
    bins_supported: int
    bins_total: int
    same_inside: int
    different_inside: int
    same_total: int
    different_total: int
    rule: str


# =============================================================================
# SQLITE
# =============================================================================

PAIR_SCHEMA = """
CREATE TABLE IF NOT EXISTS ch13_pair_datasets (
    pair_dataset_key TEXT PRIMARY KEY,
    run_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    params_json TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (run_id)
        REFERENCES experiment_runs(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ch13_pair_records (
    pair_dataset_key TEXT NOT NULL,
    pair_id INTEGER NOT NULL,

    run_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    time_bin INTEGER NOT NULL,

    distance REAL NOT NULL,
    distance_bin INTEGER NOT NULL,

    local_density REAL NOT NULL,
    density_bin INTEGER NOT NULL,

    same_family INTEGER NOT NULL,
    coherence REAL NOT NULL,

    PRIMARY KEY (pair_dataset_key, pair_id),

    FOREIGN KEY (pair_dataset_key)
        REFERENCES ch13_pair_datasets(pair_dataset_key)
        ON DELETE CASCADE,

    FOREIGN KEY (run_id)
        REFERENCES experiment_runs(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ch13_pairs_dataset_distance
ON ch13_pair_records(pair_dataset_key, distance);

CREATE INDEX IF NOT EXISTS idx_ch13_pairs_dataset_family_distance
ON ch13_pair_records(pair_dataset_key, same_family, distance);

CREATE INDEX IF NOT EXISTS idx_ch13_pairs_dataset_stratum
ON ch13_pair_records(
    pair_dataset_key,
    time_bin,
    distance_bin,
    density_bin,
    same_family
);
"""


def connect_db(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(
            f"SQLite cache not found: {path}\n"
            "Rebuild with ch11_outlier_radial_flocking.py --rebuild first."
        )

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA busy_timeout=60000")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type IN ('table', 'view') AND name=?
        """,
        (name,),
    ).fetchone()
    return row is not None


def latest_complete_run(
    conn: sqlite3.Connection,
    requested: int | None,
) -> int:
    return original.latest_complete_run(conn, requested)


def run_metadata(conn: sqlite3.Connection, run_id: int) -> dict:
    return original.run_metadata(conn, run_id)


def pair_dataset_key(params: PairParams, run_id: int) -> str:
    raw = json.dumps(
        params.pair_key_payload(run_id),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def ensure_pair_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(PAIR_SCHEMA)
    conn.commit()


def completed_pair_dataset(
    conn: sqlite3.Connection,
    key: str,
) -> tuple[int, str] | None:
    row = conn.execute(
        """
        SELECT row_count, status
        FROM ch13_pair_datasets
        WHERE pair_dataset_key=?
        """,
        (key,),
    ).fetchone()

    if not row or row[1] != "complete":
        return None

    actual = conn.execute(
        """
        SELECT COUNT(*)
        FROM ch13_pair_records
        WHERE pair_dataset_key=?
        """,
        (key,),
    ).fetchone()[0]

    if int(actual) != int(row[0]):
        raise RuntimeError(
            "Pair-dataset metadata says complete but row count does not match: "
            f"metadata={row[0]:,}, actual={actual:,}. "
            "Use --rebuild-pairs."
        )

    return int(actual), str(row[1])


def delete_pair_dataset(
    conn: sqlite3.Connection,
    key: str,
) -> None:
    with conn:
        conn.execute(
            "DELETE FROM ch13_pair_datasets WHERE pair_dataset_key=?",
            (key,),
        )


# =============================================================================
# EXACT ORIGINAL PAIR DATASET
# =============================================================================

def reconstruct_pair_records(
    conn: sqlite3.Connection,
    run_id: int,
    metadata: dict,
    params: PairParams,
):
    """
    Call the ORIGINAL Chapter 13 pair-construction function.

    Record tuple returned by original.collect_pair_records:

        (
            time_bin,
            distance_bin,
            density_bin,
            same_family,
            alignment,
            distance,
            density,
            time_value,
        )
    """
    print("\nReconstructing pair records using original Chapter 13 logic ...")

    by_time = original.load_motion_by_time(
        conn,
        run_id,
    )

    records = original.collect_pair_records(
        by_time=by_time,
        world_size=metadata["size"],
        pair_radius=params.pair_radius,
        flow_radius=params.flow_radius,
        density_radius=params.density_radius,
        flow_min_neighbors=params.flow_min_neighbors,
        max_pairs_per_tick=params.max_pairs_per_tick,
        distance_edges=DISTANCE_EDGES,
        time_bin_width=params.time_bin_width,
        seed=params.seed,
    )

    return records


def persist_pair_records(
    conn: sqlite3.Connection,
    key: str,
    run_id: int,
    params: PairParams,
    records,
) -> None:
    print(f"Persisting {len(records):,} pair records to SQLite ...")

    delete_pair_dataset(conn, key)

    with conn:
        conn.execute(
            """
            INSERT INTO ch13_pair_datasets(
                pair_dataset_key,
                run_id,
                created_at,
                params_json,
                row_count,
                status
            )
            VALUES (?, ?, ?, ?, ?, 'building')
            """,
            (
                key,
                run_id,
                datetime.now(timezone.utc).isoformat(),
                json.dumps(
                    params.pair_key_payload(run_id),
                    sort_keys=True,
                ),
                len(records),
            ),
        )

    insert_sql = """
        INSERT INTO ch13_pair_records(
            pair_dataset_key,
            pair_id,
            run_id,
            time,
            time_bin,
            distance,
            distance_bin,
            local_density,
            density_bin,
            same_family,
            coherence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    def rows():
        for pair_id, record in enumerate(records):
            (
                time_bin,
                distance_bin,
                density_bin,
                same_family,
                alignment,
                distance,
                density,
                time_value,
            ) = record

            yield (
                key,
                pair_id,
                run_id,
                int(time_value),
                int(time_bin),
                float(distance),
                int(distance_bin),
                float(density),
                int(density_bin),
                int(bool(same_family)),
                float(alignment),
            )

    # Chunked insertion keeps transactions bounded while remaining fast.
    iterator = iter(rows())
    batch_size = 50_000
    inserted = 0

    while True:
        batch = []
        try:
            for _ in range(batch_size):
                batch.append(next(iterator))
        except StopIteration:
            pass

        if not batch:
            break

        with conn:
            conn.executemany(insert_sql, batch)

        inserted += len(batch)
        print(f"  persisted {inserted:,}/{len(records):,}")

    with conn:
        conn.execute(
            """
            UPDATE ch13_pair_datasets
            SET row_count=?, status='complete'
            WHERE pair_dataset_key=?
            """,
            (inserted, key),
        )

    if inserted != len(records):
        raise RuntimeError(
            f"Pair persistence mismatch: expected={len(records):,}, "
            f"inserted={inserted:,}"
        )

    print("Pair dataset persisted successfully.")


def ensure_pair_dataset(
    conn: sqlite3.Connection,
    key: str,
    run_id: int,
    metadata: dict,
    params: PairParams,
    rebuild: bool,
) -> int:
    if rebuild:
        print(f"Deleting pair dataset cache: {key}")
        delete_pair_dataset(conn, key)

    found = completed_pair_dataset(conn, key)
    if found is not None:
        n, _ = found
        print(
            f"Using persisted Chapter 13 pair dataset: "
            f"key={key} rows={n:,}"
        )
        return n

    records = reconstruct_pair_records(
        conn,
        run_id,
        metadata,
        params,
    )

    persist_pair_records(
        conn,
        key,
        run_id,
        params,
        records,
    )

    return len(records)


# =============================================================================
# LOAD / CONVERSION
# =============================================================================

def load_pair_dataframe(
    conn: sqlite3.Connection,
    key: str,
) -> pd.DataFrame:
    print("\nLoading persisted pair evidence ...")

    df = pd.read_sql_query(
        """
        SELECT
            time,
            time_bin,
            distance,
            distance_bin,
            local_density,
            density_bin,
            same_family,
            coherence
        FROM ch13_pair_records
        WHERE pair_dataset_key=?
        ORDER BY pair_id
        """,
        conn,
        params=(key,),
    )

    df["same_family"] = df["same_family"].astype(bool)

    print(
        f"pair rows: {len(df):,} | "
        f"same-family: {int(df.same_family.sum()):,} | "
        f"different-family: {int((~df.same_family).sum()):,}"
    )

    return df


def dataframe_to_original_records(df: pd.DataFrame):
    """
    Convert persisted evidence back into the exact tuple format expected by
    original.matched_analysis().
    """
    return list(
        zip(
            df["time_bin"].astype(int).tolist(),
            df["distance_bin"].astype(int).tolist(),
            df["density_bin"].astype(int).tolist(),
            df["same_family"].astype(bool).tolist(),
            df["coherence"].astype(float).tolist(),
            df["distance"].astype(float).tolist(),
            df["local_density"].astype(float).tolist(),
            df["time"].astype(int).tolist(),
        )
    )


# =============================================================================
# OVERLAP / POSITIVITY
# =============================================================================

def fixed_distance_bins() -> np.ndarray:
    return np.asarray(DISTANCE_EDGES, dtype=float)


def distance_counts(df: pd.DataFrame) -> pd.DataFrame:
    bins = fixed_distance_bins()

    work = df.copy()
    work["distance_interval"] = pd.cut(
        work["distance"],
        bins=bins,
        include_lowest=True,
        right=False,
    )

    counts = (
        work.groupby(
            ["distance_interval", "same_family"],
            observed=False,
        )
        .size()
        .unstack(fill_value=0)
        .rename(
            columns={
                False: "different_n",
                True: "same_n",
            }
        )
        .reset_index()
    )

    for col in ("same_n", "different_n"):
        if col not in counts:
            counts[col] = 0

    counts["lower"] = counts["distance_interval"].map(
        lambda x: float(x.left)
    )
    counts["upper"] = counts["distance_interval"].map(
        lambda x: float(x.right)
    )

    return counts


def contiguous_regions(mask: np.ndarray):
    regions = []
    start = None

    for i, value in enumerate(mask):
        if value and start is None:
            start = i

        if start is not None and (
            not value or i == len(mask) - 1
        ):
            end = (
                i
                if value and i == len(mask) - 1
                else i - 1
            )
            regions.append((start, end))
            start = None

    return regions


def define_support(
    df: pd.DataFrame,
    counts_base: pd.DataFrame,
    threshold: int,
) -> tuple[Support, pd.DataFrame]:
    counts = counts_base.copy()

    counts["supported"] = (
        (counts["same_n"] >= threshold)
        & (counts["different_n"] >= threshold)
    )

    regions = contiguous_regions(
        counts["supported"].to_numpy(bool)
    )

    if not regions:
        raise RuntimeError(
            f"No common-support region for threshold={threshold}."
        )

    # Select largest contiguous supported region by total observations.
    best = max(
        regions,
        key=lambda ab: int(
            counts.loc[
                ab[0]:ab[1],
                ["same_n", "different_n"],
            ].to_numpy().sum()
        ),
    )

    a, b = best
    lower = float(counts.loc[a, "lower"])
    upper = float(counts.loc[b, "upper"])

    # Original bins are left-closed, right-open except effectively max edge.
    inside = df[
        (df["distance"] >= lower)
        & (df["distance"] < upper)
    ].copy()

    support = Support(
        threshold=int(threshold),
        lower=lower,
        upper=upper,
        bins_supported=int(counts["supported"].sum()),
        bins_total=int(len(counts)),
        same_inside=int(inside["same_family"].sum()),
        different_inside=int((~inside["same_family"]).sum()),
        same_total=int(df["same_family"].sum()),
        different_total=int((~df["same_family"]).sum()),
        rule=(
            "largest contiguous ORIGINAL Chapter 13 distance-bin region "
            f"with at least {threshold} same-family and {threshold} "
            "different-family raw pair records per bin"
        ),
    )

    return support, counts


def raw_group_effect(df: pd.DataFrame) -> dict:
    same = df.loc[
        df["same_family"],
        "coherence",
    ].to_numpy(float)

    different = df.loc[
        ~df["same_family"],
        "coherence",
    ].to_numpy(float)

    return {
        "same_mean": float(np.mean(same)),
        "different_mean": float(np.mean(different)),
        "difference": float(
            np.mean(same) - np.mean(different)
        ),
        "same_n": int(len(same)),
        "different_n": int(len(different)),
    }


def run_original_matched(
    df: pd.DataFrame,
    params: PairParams,
) -> dict:
    records = dataframe_to_original_records(df)

    return original.matched_analysis(
        records=records,
        seed=params.seed,
        max_matches_per_stratum=params.max_matches_per_stratum,
    )


# =============================================================================
# SENSITIVITY
# =============================================================================

def run_sensitivity(
    df: pd.DataFrame,
    counts_base: pd.DataFrame,
    thresholds: Sequence[int],
    params: PairParams,
) -> list[dict]:
    rows = []

    for threshold in thresholds:
        try:
            support, _ = define_support(
                df,
                counts_base,
                threshold,
            )
        except RuntimeError:
            rows.append(
                {
                    "threshold": int(threshold),
                    "supported": False,
                    "lower": None,
                    "upper": None,
                }
            )
            continue

        inside = df[
            (df["distance"] >= support.lower)
            & (df["distance"] < support.upper)
        ].copy()

        raw = raw_group_effect(inside)
        matched = run_original_matched(
            inside,
            params,
        )

        rows.append(
            {
                "threshold": int(threshold),
                "supported": True,
                "lower": support.lower,
                "upper": support.upper,
                "same_raw_n": raw["same_n"],
                "different_raw_n": raw["different_n"],
                "raw_effect": raw["difference"],
                "matched_pairs_per_group": matched[
                    "matched_pairs_per_group"
                ],
                "matched_strata": matched["used_strata"],
                "matched_same_mean": matched["same_mean"],
                "matched_different_mean": matched["diff_mean"],
                "matched_pooled_effect": matched[
                    "raw_difference"
                ],
                "equal_stratum_effect": matched[
                    "mean_stratum_effect"
                ],
                "bootstrap_95_low": matched[
                    "bootstrap_95_low"
                ],
                "bootstrap_95_high": matched[
                    "bootstrap_95_high"
                ],
            }
        )

    return rows


# =============================================================================
# FIGURES
# =============================================================================

def plot_distance_overlap(
    df: pd.DataFrame,
    support: Support,
    path: Path,
) -> None:
    same = df.loc[
        df["same_family"],
        "distance",
    ].to_numpy(float)

    different = df.loc[
        ~df["same_family"],
        "distance",
    ].to_numpy(float)

    bins = fixed_distance_bins()

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.hist(
        same,
        bins=bins,
        density=True,
        alpha=0.55,
        label="same recent-c2 family",
    )

    ax.hist(
        different,
        bins=bins,
        density=True,
        alpha=0.55,
        label="different recent-c2 family",
    )

    ax.axvspan(
        support.lower,
        support.upper,
        alpha=0.16,
        label=(
            f"common support "
            f"[{support.lower:g}, {support.upper:g})"
        ),
    )

    ax.set_xlabel("Pair separation (cells)")
    ax.set_ylabel("Density")
    ax.set_title(
        "Outlier: Distance Overlap for Same- vs Different-Family Pairs"
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_effect_by_distance(
    df: pd.DataFrame,
    counts_base: pd.DataFrame,
    support: Support,
    path: Path,
) -> None:
    rows = []

    for distance_bin in sorted(
        df["distance_bin"].unique()
    ):
        if (
            distance_bin < 0
            or distance_bin >= len(DISTANCE_EDGES) - 1
        ):
            continue

        sub = df[
            df["distance_bin"] == distance_bin
        ]

        same = sub[
            sub["same_family"]
        ]["coherence"].to_numpy(float)

        diff = sub[
            ~sub["same_family"]
        ]["coherence"].to_numpy(float)

        effect = (
            float(np.mean(same) - np.mean(diff))
            if len(same) and len(diff)
            else np.nan
        )

        rows.append(
            {
                "distance_bin": int(distance_bin),
                "centre": (
                    DISTANCE_EDGES[distance_bin]
                    + DISTANCE_EDGES[distance_bin + 1]
                ) / 2.0,
                "effect": effect,
                "min_group_n": min(
                    len(same),
                    len(diff),
                ),
            }
        )

    plot_df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axhline(0.0, linewidth=1)

    ax.plot(
        plot_df["centre"],
        plot_df["effect"],
        marker="o",
        label="raw same-family − different-family",
    )

    max_n = max(
        float(plot_df["min_group_n"].max()),
        1.0,
    )

    sizes = (
        25.0
        + 125.0
        * plot_df["min_group_n"].to_numpy(float)
        / max_n
    )

    ax.scatter(
        plot_df["centre"],
        plot_df["effect"],
        s=sizes,
        alpha=0.45,
        label="marker size = weaker group count",
    )

    ax.axvspan(
        support.lower,
        support.upper,
        alpha=0.16,
        label="primary common-support region",
    )

    ax.set_xlabel("Pair separation (cells)")
    ax.set_ylabel("Raw coherence difference")
    ax.set_title(
        "Outlier: Family-Coherence Contrast and Empirical Overlap by Distance"
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# REPORT
# =============================================================================

def write_report(
    report_path: Path,
    result: dict,
) -> None:
    primary = result["primary"]
    support = primary["support"]
    raw = primary["raw_inside_support"]
    matched = primary["matched_inside_support"]
    original = result["original_apparent_effect"]

    text = f"""# Chapter 13 — Outlier Overlap / Positivity Analysis

## Purpose

This analysis tests whether the Chapter 13 comparison between same-family and
different-family motion pairs has adequate spatial overlap.

It reuses the **exact pair-construction and matched-analysis implementation**
from `ch11_outlier_distance_matched.py`.

It does not silently substitute a new matching estimator.

## Source specimen

- Database: `{result["database"]}`
- Outlier run ID: **{result["run_id"]}**
- Grid: **{result["run_metadata"]["size"]} × {result["run_metadata"]["size"]}**
- Generations: **{result["run_metadata"]["generations"]}**
- Persisted pair dataset key: `{result["pair_dataset_key"]}`
- Pair records: **{result["pair_rows"]:,}**

## Original Chapter 13 pair-construction parameters

```json
{json.dumps(result["pair_params"], indent=2)}
```

Distance bins are the original Chapter 13 bins:

```text
{DISTANCE_EDGES}
```

## Primary common-support rule

> {support["rule"]}

Primary threshold:

**{support["threshold"]} rows per group per distance bin**

Resulting common-support interval:

**[{support["lower"]:.1f}, {support["upper"]:.1f}) cells**

Coverage:

- same-family inside: **{support["same_inside"]:,} / {support["same_total"]:,}**
- different-family inside: **{support["different_inside"]:,} / {support["different_total"]:,}**
- supported distance bins: **{support["bins_supported"]} / {support["bins_total"]}**

## Estimand A — raw descriptive effect inside common support

This estimate is descriptive only. It weights every pair equally and does not
balance the original time/distance/density strata.

```json
{json.dumps(raw, indent=2)}
```

## Estimands B/C — original balanced matching inside common support

The original Chapter 13 matcher performs exact matching on:

```text
time_bin
distance_bin
density_bin
```

Within each stratum it selects equal numbers of same-family and
different-family pairs.

Results:

- matched same-family mean: **{matched["same_mean"]:+.6f}**
- matched different-family mean: **{matched["diff_mean"]:+.6f}**
- balanced matched pooled effect: **{matched["raw_difference"]:+.6f}**
- equal-stratum effect: **{matched["mean_stratum_effect"]:+.6f}**
- bootstrap 95% interval: **[{matched["bootstrap_95_low"]:+.6f}, {matched["bootstrap_95_high"]:+.6f}]**
- matched pairs per group: **{matched["matched_pairs_per_group"]:,}**
- matched strata: **{matched["used_strata"]:,}**

### Why the matched pooled and equal-stratum effects differ

They are different estimands.

The matched pooled effect gives strata weight in proportion to the number of
matched pairs they contribute.

The equal-stratum effect first computes one same-minus-different effect for
each matched stratum and then gives every stratum equal weight.

A difference between them is therefore expected when large and small strata
have different effects.

## Original apparent family gap

Before spatial matching, the stronger pair-excluded analysis reported:

- same recent-c2 ancestor: **{original["same"]:.3f}**
- comparison group: **{original["comparison"]:.3f}**
- apparent gap: **{original["gap"]:.3f}**

Inside primary common support, the upper bootstrap bound is:

**{matched["bootstrap_95_high"]:+.6f}**

As a fraction of the original apparent gap:

**{original["primary_upper_ci_percent_of_original_gap"]:.2f}%**

This is the useful quantitative bound.

## Support-threshold sensitivity

The support rule was repeated under several minimum-count thresholds.

```json
{json.dumps(result["sensitivity"], indent=2)}
```

The conclusion is more credible if the support interval and matched effect do
not depend qualitatively on one arbitrary count threshold.

CSV:

`{result["artifacts"]["sensitivity_csv"]}`

## Distance-bin counts

CSV:

`{result["artifacts"]["distance_counts_csv"]}`

## Figures

- `{result["artifacts"]["distance_overlap_figure"]}`
- `{result["artifacts"]["effect_by_distance_figure"]}`

## Bounded conclusion

> **{result["bounded_claim"]}**

## Scope limitation

This analysis hardens inference only for the existing Chapter 13 Outlier run.

It does **not** establish that the same result applies to the larger published
causal regime.

```text
our run
512 × 512
1,600 generations

published causal study
1024 × 1024
20,000 updates
```

The very-short-range region should be described as unresolved whenever the
different-family comparison population is insufficient for the declared
common-support criterion.

## Evidence architecture improvement

The derived pair-level evidence is now persisted in SQLite:

```text
ch13_pair_datasets
ch13_pair_records
```

Future overlap, matching, or sensitivity analyses can therefore operate on
the same frozen pair dataset instead of silently reconstructing it.
"""

    report_path.write_text(
        text,
        encoding="utf-8",
    )


# =============================================================================
# CLI
# =============================================================================

def parse_thresholds(value: str) -> list[int]:
    vals = []
    for piece in value.split(","):
        piece = piece.strip()
        if not piece:
            continue
        vals.append(int(piece))

    if not vals:
        raise argparse.ArgumentTypeError(
            "Provide at least one support threshold."
        )

    return vals


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Persist the Chapter 13 Outlier pair dataset and perform "
            "overlap/positivity hardening using the original matcher."
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
        "--rebuild-pairs",
        action="store_true",
        help=(
            "Delete and reconstruct the derived Chapter 13 pair dataset. "
            "The expensive CA simulation is NOT rerun."
        ),
    )

    # Exact original pair-analysis parameters.
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
        "--primary-support-threshold",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--support-thresholds",
        type=parse_thresholds,
        default=DEFAULT_SUPPORT_THRESHOLDS,
        help="Comma-separated sensitivity thresholds. Default: 50,100,250,500",
    )

    parser.add_argument(
        "--original-same",
        type=float,
        default=0.746,
    )

    parser.add_argument(
        "--original-comparator",
        type=float,
        default=0.101,
    )

    parser.add_argument(
        "--reports",
        type=Path,
        default=DEFAULT_REPORTS,
    )

    parser.add_argument(
        "--images",
        type=Path,
        default=DEFAULT_IMAGES,
    )

    return parser.parse_args()


# =============================================================================
# MAIN
# =============================================================================

def main():
    args = parse_args()

    args.reports.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.images.mkdir(
        parents=True,
        exist_ok=True,
    )

    params = PairParams(
        pair_radius=args.pair_radius,
        flow_radius=args.flow_radius,
        density_radius=args.density_radius,
        flow_min_neighbors=args.flow_min_neighbors,
        max_pairs_per_tick=args.max_pairs_per_tick,
        time_bin_width=args.time_bin_width,
        max_matches_per_stratum=args.max_matches_per_stratum,
        seed=args.seed,
    )

    conn = connect_db(args.db)

    try:
        ensure_pair_schema(conn)

        run_id = latest_complete_run(
            conn,
            args.run_id,
        )

        metadata = run_metadata(
            conn,
            run_id,
        )

        print(
            f"Using Outlier run_id={run_id} "
            f"size={metadata['size']} "
            f"generations={metadata['generations']}"
        )

        if not table_exists(
            conn,
            "c2_recent_ancestor",
        ):
            raise RuntimeError(
                "Required table c2_recent_ancestor is missing.\n\n"
                "Run:\n"
                "  python scripts/books/digital-life/ch11_outlier_local_flow.py\n\n"
                "Then rerun this script."
            )

        key = pair_dataset_key(
            params,
            run_id,
        )

        pair_rows = ensure_pair_dataset(
            conn=conn,
            key=key,
            run_id=run_id,
            metadata=metadata,
            params=params,
            rebuild=args.rebuild_pairs,
        )

        df = load_pair_dataframe(
            conn,
            key,
        )

    finally:
        conn.close()

    counts_base = distance_counts(df)

    # -----------------------------------------------------------------------
    # Primary support definition
    # -----------------------------------------------------------------------

    support, primary_counts = define_support(
        df,
        counts_base,
        args.primary_support_threshold,
    )

    inside = df[
        (df["distance"] >= support.lower)
        & (df["distance"] < support.upper)
    ].copy()

    raw_inside = raw_group_effect(
        inside,
    )

    print("\nRunning original matched estimator inside primary common support ...")

    matched_inside = run_original_matched(
        inside,
        params,
    )

    # -----------------------------------------------------------------------
    # Sensitivity
    # -----------------------------------------------------------------------

    thresholds = sorted(
        set(
            args.support_thresholds
            + [args.primary_support_threshold]
        )
    )

    print("\nRunning common-support threshold sensitivity ...")

    sensitivity = run_sensitivity(
        df=df,
        counts_base=counts_base,
        thresholds=thresholds,
        params=params,
    )

    # -----------------------------------------------------------------------
    # Quantitative bound
    # -----------------------------------------------------------------------

    original_gap = (
        args.original_same
        - args.original_comparator
    )

    upper_fraction = (
        matched_inside["bootstrap_95_high"]
        / original_gap
        if original_gap != 0
        else float("nan")
    )

    # -----------------------------------------------------------------------
    # Artifacts
    # -----------------------------------------------------------------------

    counts_csv = (
        args.reports
        / "ch13-distance-bin-counts.csv"
    )

    counts_out = primary_counts.copy()
    counts_out["distance_interval"] = counts_out[
        "distance_interval"
    ].astype(str)
    counts_out.to_csv(
        counts_csv,
        index=False,
    )

    sensitivity_csv = (
        args.reports
        / "ch13-overlap-sensitivity.csv"
    )
    pd.DataFrame(
        sensitivity
    ).to_csv(
        sensitivity_csv,
        index=False,
    )

    overlap_png = (
        args.images
        / "ch13-outlier-distance-overlap.png"
    )

    effect_png = (
        args.images
        / "ch13-outlier-overlap-effect-by-distance.png"
    )

    plot_distance_overlap(
        df,
        support,
        overlap_png,
    )

    plot_effect_by_distance(
        df,
        counts_base,
        support,
        effect_png,
    )

    bounded_claim = (
        f"Within the empirically supported distance region "
        f"[{support.lower:.1f}, {support.upper:.1f}) cells under the "
        f"declared minimum-count criterion, the original balanced "
        f"time/distance/density matching gives a same-family minus "
        f"different-family effect of "
        f"{matched_inside['raw_difference']:+.4f}. "
        f"The equal-stratum effect is "
        f"{matched_inside['mean_stratum_effect']:+.4f} with a "
        f"bootstrap 95% interval "
        f"[{matched_inside['bootstrap_95_low']:+.4f}, "
        f"{matched_inside['bootstrap_95_high']:+.4f}]. "
        f"The upper bound is {upper_fraction * 100.0:.1f}% of the "
        f"original apparent {original_gap:.3f} family gap. "
        f"Outside adequate common support, especially at the shortest "
        f"separations if different-family controls are sparse there, "
        f"this experiment does not identify an independent ancestry effect."
    )

    result = {
        "analysis_version": ANALYSIS_VERSION,
        "database": str(args.db),
        "run_id": run_id,
        "run_metadata": metadata,
        "pair_dataset_key": key,
        "pair_rows": pair_rows,
        "pair_params": asdict(params),
        "distance_edges": DISTANCE_EDGES,
        "primary": {
            "support": asdict(support),
            "raw_inside_support": raw_inside,
            "matched_inside_support": matched_inside,
        },
        "sensitivity": sensitivity,
        "original_apparent_effect": {
            "same": args.original_same,
            "comparison": args.original_comparator,
            "gap": original_gap,
            "primary_upper_ci_fraction_of_original_gap": upper_fraction,
            "primary_upper_ci_percent_of_original_gap": (
                upper_fraction * 100.0
            ),
        },
        "bounded_claim": bounded_claim,
        "artifacts": {
            "distance_counts_csv": str(counts_csv),
            "sensitivity_csv": str(sensitivity_csv),
            "distance_overlap_figure": str(overlap_png),
            "effect_by_distance_figure": str(effect_png),
        },
        "scope_limit": {
            "our_size": metadata["size"],
            "our_generations": metadata["generations"],
            "published_reference_size": 1024,
            "published_reference_updates": 20000,
        },
    }

    json_path = (
        args.reports
        / "ch13-overlap-analysis.json"
    )

    json_path.write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )

    report_path = (
        args.reports
        / "ch13-overlap-analysis.md"
    )

    write_report(
        report_path,
        result,
    )

    # -----------------------------------------------------------------------
    # Console summary
    # -----------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("CHAPTER 13 OVERLAP / POSITIVITY ANALYSIS COMPLETE")
    print("=" * 80)

    print(
        f"Pair dataset:       {key}"
    )

    print(
        f"Pair rows:          {pair_rows:,}"
    )

    print(
        f"Primary support:    "
        f"[{support.lower:.1f}, {support.upper:.1f})"
    )

    print(
        f"Raw support effect: "
        f"{raw_inside['difference']:+.6f}"
    )

    print(
        f"Matched pooled:     "
        f"{matched_inside['raw_difference']:+.6f}"
    )

    print(
        f"Equal-stratum:      "
        f"{matched_inside['mean_stratum_effect']:+.6f}"
    )

    print(
        f"Bootstrap 95%:      "
        f"[{matched_inside['bootstrap_95_low']:+.6f}, "
        f"{matched_inside['bootstrap_95_high']:+.6f}]"
    )

    print(
        f"Upper CI/original:  "
        f"{upper_fraction * 100.0:.2f}%"
    )

    print()
    print(f"Report:             {report_path}")
    print(f"JSON:               {json_path}")
    print(f"Counts CSV:         {counts_csv}")
    print(f"Sensitivity CSV:    {sensitivity_csv}")
    print(f"Overlap figure:     {overlap_png}")
    print(f"Effect figure:      {effect_png}")
    print("=" * 80)


if __name__ == "__main__":
    main()
