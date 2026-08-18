#!/usr/bin/env python3
"""
Digital Life — Chapter 28 V2
Post-hoc Spatial-Overlap Robustness Audit
=========================================

PURPOSE
-------
Chapter 28 V2 compared outcome-blind selected radius-4 regions against
same-checkpoint geometry-matched control regions.

The frozen V2 matcher excluded:
    - exact reuse of an observed center as a control center;
    - reuse of a control center within a group.

It did NOT freeze:
    - a minimum selected/control center separation;
    - a maximum disk-overlap fraction;
    - a non-overlap requirement.

This script audits that issue WITHOUT changing or replacing the frozen V2
primary result.

It:

1. Reads the existing V2 match results.
2. Computes exact selected/control center distance.
3. Computes exact radius-R hex-disk overlap.
4. Computes probe overlap from the existing probe-results file when available.
5. Optionally reconstructs the original V2 checkpoints (NO causal outcomes)
   to measure overlap of OCCUPIED cells inside selected/control disks.
6. Reproduces the frozen V2 group-level excess estimate as a sanity check.
7. Recomputes the same excess-modularity contrast after progressively stricter
   POST-HOC spatial-distinctness filters.
8. Writes JSON/CSV/Markdown audit outputs.

IMPORTANT EPISTEMIC STATUS
--------------------------
Every filtered result produced here is:

    POST_HOC ROBUSTNESS / SENSITIVITY ANALYSIS

It is NOT:
    - a new confirmatory V2 result;
    - a replacement for the frozen V2 primary;
    - permission to tune a threshold until a preferred answer appears.

The frozen V2 result remains whatever the original V2 report declared.

STRICT NON-OVERLAP
------------------
For radius-R disks in the hex graph metric, strict site non-overlap requires
center distance > 2R. For R=4, that means center distance >= 9.

The script computes disk overlap directly, so it does not rely only on this
geometric shortcut.

USAGE
-----
Fast audit using existing outcome files only:

    python scripts/books/digital-life/ch28_causal_modularity_overlap_audit.py

Also reconstruct V2 checkpoints to measure occupied-cell overlap:

    python scripts/books/digital-life/ch28_causal_modularity_overlap_audit.py \
        --reconstruct-occupied

Custom report directory:

    python scripts/books/digital-life/ch28_causal_modularity_overlap_audit.py \
        --report-dir research/digital-life/ch28-causal-modularity-v2

OUTPUTS
-------
Written beside the V2 report:

    raw-v2-spatial-overlap-audit.csv
    raw-v2-spatial-overlap-audit.jsonl
    stage-07-spatial-overlap-audit.json
    stage-07-spatial-overlap-audit.md

This script does not modify any V1/V2 output.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np


Cell = Tuple[int, int]

DEFAULT_RADIUS = 4
DEFAULT_EXCESS_SEI = 0.10
DEFAULT_BOOTSTRAP_REPS = 7000
DEFAULT_BOOTSTRAP_SEED = 20260918

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def axial_distance(a: Cell, b: Cell) -> int:
    dq = int(a[0]) - int(b[0])
    dr = int(a[1]) - int(b[1])
    return int(max(abs(dq), abs(dr), abs(dq + dr)))


def hex_disk(center: Cell, radius: int) -> Set[Cell]:
    cq, cr = center
    out: Set[Cell] = set()

    for dq in range(-radius, radius + 1):
        for dr in range(-radius, radius + 1):
            cell = (cq + dq, cr + dr)
            if axial_distance(center, cell) <= radius:
                out.add(cell)

    return out


def safe_fraction(numer: int | float, denom: int | float) -> float:
    return float(numer / denom) if denom else float("nan")


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------

def read_jsonl(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(path)

    rows: List[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Invalid JSONL at {path}:{lineno}: {exc}"
                ) from exc

    return rows


def write_jsonl(path: Path, rows: Sequence[Mapping]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(dict(row), sort_keys=True) + "\n")


def write_csv(path: Path, rows: Sequence[Mapping]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))


# ---------------------------------------------------------------------------
# Probe overlap
# ---------------------------------------------------------------------------

def build_probe_index(probe_rows: Sequence[dict]) -> Dict[Tuple[int, str], dict]:
    """
    Key by (group, region_id).

    Stores:
      coordinate_set: {(q,r), ...}
      typed_set: {(probe_class,q,r), ...}
      internal_set / external_set
    """
    out: Dict[Tuple[int, str], dict] = {}

    for row in probe_rows:
        key = (int(row["group"]), str(row["region_id"]))
        entry = out.setdefault(
            key,
            {
                "coordinate_set": set(),
                "typed_set": set(),
                "internal_set": set(),
                "external_set": set(),
            },
        )

        cell = (int(row["probe_q"]), int(row["probe_r"]))
        probe_class = str(row["probe_class"])

        entry["coordinate_set"].add(cell)
        entry["typed_set"].add((probe_class, cell[0], cell[1]))

        if probe_class == "internal":
            entry["internal_set"].add(cell)
        elif probe_class == "external":
            entry["external_set"].add(cell)

    return out


def overlap_stats(a: Set, b: Set) -> dict:
    inter = len(a & b)
    union = len(a | b)
    smaller = min(len(a), len(b))

    return {
        "count": int(inter),
        "jaccard": safe_fraction(inter, union),
        "fraction_of_smaller": safe_fraction(inter, smaller),
    }


# ---------------------------------------------------------------------------
# Audit row
# ---------------------------------------------------------------------------

@dataclass
class AuditRow:
    group: int
    observed_index: int
    control_index: int
    observed_region_id: str
    control_region_id: str

    observed_center_q: int
    observed_center_r: int
    control_center_q: int
    control_center_r: int

    center_distance: int

    disk_size: int
    disk_overlap_count: int
    disk_overlap_fraction: float
    disk_jaccard: float
    strict_disk_nonoverlap: bool

    probe_overlap_count: int | None
    probe_overlap_fraction_smaller: float | None
    probe_jaccard: float | None
    typed_probe_overlap_count: int | None
    internal_probe_overlap_count: int | None
    external_probe_overlap_count: int | None

    occupied_observed_count: int | None
    occupied_control_count: int | None
    occupied_overlap_count: int | None
    occupied_overlap_fraction_smaller: float | None
    occupied_jaccard: float | None

    match_distance: float
    occupancy_diff: float
    radial_diff: int
    occupied_count_diff: int
    internal_frontier_diff: int
    external_frontier_diff: int

    observed_module_score: float
    control_module_score: float
    excess_module_score: float

    observed_internal_retention: float
    control_internal_retention: float
    excess_internal_retention: float

    observed_external_penetration: float
    control_external_penetration: float
    excess_external_penetration: float


def make_audit_rows(
    match_rows: Sequence[dict],
    radius: int,
    probe_index: Mapping[Tuple[int, str], dict],
    occupied_by_group: Mapping[int, Set[Cell]] | None,
) -> List[AuditRow]:
    out: List[AuditRow] = []

    for row in match_rows:
        group = int(row["group"])

        obs_center = (
            int(row["observed_center_q"]),
            int(row["observed_center_r"]),
        )
        ctrl_center = (
            int(row["control_center_q"]),
            int(row["control_center_r"]),
        )

        obs_disk = hex_disk(obs_center, radius)
        ctrl_disk = hex_disk(ctrl_center, radius)
        disk_inter = obs_disk & ctrl_disk
        disk_union = obs_disk | ctrl_disk

        center_d = axial_distance(obs_center, ctrl_center)

        obs_region_id = str(row["observed_region_id"])
        ctrl_region_id = str(row["control_region_id"])

        obs_probe = probe_index.get((group, obs_region_id))
        ctrl_probe = probe_index.get((group, ctrl_region_id))

        if obs_probe is not None and ctrl_probe is not None:
            p = overlap_stats(
                obs_probe["coordinate_set"],
                ctrl_probe["coordinate_set"],
            )
            typed = overlap_stats(
                obs_probe["typed_set"],
                ctrl_probe["typed_set"],
            )
            internal = overlap_stats(
                obs_probe["internal_set"],
                ctrl_probe["internal_set"],
            )
            external = overlap_stats(
                obs_probe["external_set"],
                ctrl_probe["external_set"],
            )

            probe_overlap_count = p["count"]
            probe_overlap_fraction_smaller = p["fraction_of_smaller"]
            probe_jaccard = p["jaccard"]
            typed_probe_overlap_count = typed["count"]
            internal_probe_overlap_count = internal["count"]
            external_probe_overlap_count = external["count"]
        else:
            probe_overlap_count = None
            probe_overlap_fraction_smaller = None
            probe_jaccard = None
            typed_probe_overlap_count = None
            internal_probe_overlap_count = None
            external_probe_overlap_count = None

        if occupied_by_group is not None and group in occupied_by_group:
            occupied = occupied_by_group[group]
            obs_occ = obs_disk & occupied
            ctrl_occ = ctrl_disk & occupied
            occ = overlap_stats(obs_occ, ctrl_occ)

            occupied_observed_count = len(obs_occ)
            occupied_control_count = len(ctrl_occ)
            occupied_overlap_count = occ["count"]
            occupied_overlap_fraction_smaller = occ["fraction_of_smaller"]
            occupied_jaccard = occ["jaccard"]
        else:
            occupied_observed_count = None
            occupied_control_count = None
            occupied_overlap_count = None
            occupied_overlap_fraction_smaller = None
            occupied_jaccard = None

        out.append(
            AuditRow(
                group=group,
                observed_index=int(row["observed_index"]),
                control_index=int(row["control_index"]),
                observed_region_id=obs_region_id,
                control_region_id=ctrl_region_id,
                observed_center_q=obs_center[0],
                observed_center_r=obs_center[1],
                control_center_q=ctrl_center[0],
                control_center_r=ctrl_center[1],
                center_distance=center_d,
                disk_size=len(obs_disk),
                disk_overlap_count=len(disk_inter),
                disk_overlap_fraction=safe_fraction(
                    len(disk_inter),
                    len(obs_disk),
                ),
                disk_jaccard=safe_fraction(
                    len(disk_inter),
                    len(disk_union),
                ),
                strict_disk_nonoverlap=(len(disk_inter) == 0),
                probe_overlap_count=probe_overlap_count,
                probe_overlap_fraction_smaller=probe_overlap_fraction_smaller,
                probe_jaccard=probe_jaccard,
                typed_probe_overlap_count=typed_probe_overlap_count,
                internal_probe_overlap_count=internal_probe_overlap_count,
                external_probe_overlap_count=external_probe_overlap_count,
                occupied_observed_count=occupied_observed_count,
                occupied_control_count=occupied_control_count,
                occupied_overlap_count=occupied_overlap_count,
                occupied_overlap_fraction_smaller=occupied_overlap_fraction_smaller,
                occupied_jaccard=occupied_jaccard,
                match_distance=float(row["match_distance"]),
                occupancy_diff=float(row["occupancy_diff"]),
                radial_diff=int(row["radial_diff"]),
                occupied_count_diff=int(row["occupied_count_diff"]),
                internal_frontier_diff=int(row["internal_frontier_diff"]),
                external_frontier_diff=int(row["external_frontier_diff"]),
                observed_module_score=float(row["observed_module_score"]),
                control_module_score=float(row["control_module_score"]),
                excess_module_score=float(row["excess_module_score"]),
                observed_internal_retention=float(
                    row["observed_internal_retention"]
                ),
                control_internal_retention=float(
                    row["control_internal_retention"]
                ),
                excess_internal_retention=float(
                    row["excess_internal_retention"]
                ),
                observed_external_penetration=float(
                    row["observed_external_penetration"]
                ),
                control_external_penetration=float(
                    row["control_external_penetration"]
                ),
                excess_external_penetration=float(
                    row["excess_external_penetration"]
                ),
            )
        )

    return out


# ---------------------------------------------------------------------------
# Optional occupied-cell reconstruction
# ---------------------------------------------------------------------------

def reconstruct_occupied(
    repo_root: Path,
    profile_name: str,
    seed: int,
) -> Dict[int, Set[Cell]]:
    """
    Reconstruct only the original V2 checkpoints.

    This calls the frozen checkpoint-generation path but DOES NOT evaluate any
    causal modularity outcomes.
    """
    script_dir = repo_root / "scripts" / "books" / "digital-life"
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    try:
        import ch28_digital_crystal_causal_modularity_v2 as v2
    except ImportError as exc:
        raise RuntimeError(
            "Could not import ch28_digital_crystal_causal_modularity_v2.py. "
            f"Expected it under {script_dir}"
        ) from exc

    profile = dict(v2.PROFILES[profile_name])
    source_profile = dict(v2.v4.PROFILES[profile["source_profile"]])
    source_profile["groups"] = int(profile["groups"])
    source_profile["horizon"] = int(v2.HORIZON)

    crystal_params = v2.ch18.CrystalParams()

    checkpoints = v2.prepare_groups(
        profile,
        source_profile,
        crystal_params,
        int(seed),
    )

    return {
        int(record.group): set(record.checkpoint.occupied)
        for record in checkpoints
    }


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def finite(values: Iterable[float]) -> np.ndarray:
    return np.asarray(
        [float(v) for v in values if math.isfinite(float(v))],
        dtype=float,
    )


def summary(values: Sequence[float], reps: int, seed: int) -> dict:
    arr = finite(values)

    if len(arr) == 0:
        return {
            "n": 0,
            "mean": None,
            "sd": None,
            "se": None,
            "ci95_low": None,
            "ci95_high": None,
            "achieved_mde80_one_sided": None,
        }

    rng = np.random.default_rng(int(seed))
    boot = np.empty(int(reps), dtype=float)

    for i in range(int(reps)):
        boot[i] = float(
            np.mean(
                rng.choice(
                    arr,
                    size=len(arr),
                    replace=True,
                )
            )
        )

    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = float(sd / math.sqrt(len(arr)))

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": se,
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
        "achieved_mde80_one_sided": float(
            se * (Z_95_ONE_SIDED + Z_80_POWER)
        ),
    }


def group_values(
    rows: Sequence[AuditRow],
    field: str,
) -> Dict[int, float]:
    """
    Equal-weight observed-region aggregation inside each group.

    Frozen V2 had two controls for essentially every observed region, so this
    reproduces the original group mean.

    After post-hoc filtering, an observed region may retain one control while
    another retains two. To avoid giving extra weight to the latter, this audit:
        1. averages retained controls within observed region;
        2. averages observed-region contrasts within group.

    This is the natural sensitivity extension of the frozen balanced design.
    """
    by_group_obs: Dict[int, Dict[int, List[float]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for row in rows:
        by_group_obs[row.group][row.observed_index].append(
            float(getattr(row, field))
        )

    out: Dict[int, float] = {}

    for group, obs_map in by_group_obs.items():
        obs_means = [
            float(np.mean(values))
            for values in obs_map.values()
            if values
        ]
        if obs_means:
            out[int(group)] = float(np.mean(obs_means))

    return out


def sensitivity_result(
    name: str,
    rows: Sequence[AuditRow],
    total_groups: int,
    reps: int,
    seed: int,
    excess_sei: float,
) -> dict:
    ex = group_values(rows, "excess_module_score")
    ret = group_values(rows, "excess_internal_retention")
    pen = group_values(rows, "excess_external_penetration")

    group_pair_counts = defaultdict(int)
    group_observed = defaultdict(set)

    for row in rows:
        group_pair_counts[row.group] += 1
        group_observed[row.group].add(row.observed_index)

    pair_counts = list(group_pair_counts.values())
    obs_counts = [len(v) for v in group_observed.values()]

    ex_summary = summary(
        list(ex.values()),
        reps,
        seed,
    )

    ci_high = ex_summary["ci95_high"]
    mde = ex_summary["achieved_mde80_one_sided"]

    reference_status = "INSUFFICIENT_POST_HOC_SUPPORT"

    if ex_summary["n"] > 0:
        # This is NOT promoted to a confirmatory status.
        # It is only a reference against the frozen V2 criterion.
        if (
            ci_high is not None
            and mde is not None
            and ci_high < excess_sei
            and mde <= excess_sei
        ):
            reference_status = "CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI"
        else:
            reference_status = "DOES_NOT_REPRODUCE_FROZEN_BOUND_AT_THIS_FILTER"

    return {
        "name": name,
        "epistemic_status": "POST_HOC_ROBUSTNESS_ONLY",
        "pairs_retained": int(len(rows)),
        "groups_retained": int(len(ex)),
        "group_coverage_fraction": safe_fraction(len(ex), total_groups),
        "median_pairs_per_retained_group": (
            float(statistics.median(pair_counts))
            if pair_counts
            else None
        ),
        "median_observed_regions_per_retained_group": (
            float(statistics.median(obs_counts))
            if obs_counts
            else None
        ),
        "excess_module_score": ex_summary,
        "excess_internal_retention": summary(
            list(ret.values()),
            reps,
            seed + 11,
        ),
        "excess_external_penetration": summary(
            list(pen.values()),
            reps,
            seed + 23,
        ),
        "frozen_excess_SEI_reference": float(excess_sei),
        "reference_only_status": reference_status,
    }


# ---------------------------------------------------------------------------
# Audit summaries
# ---------------------------------------------------------------------------

def quantiles(values: Sequence[float]) -> dict:
    arr = finite(values)
    if len(arr) == 0:
        return {}

    return {
        "min": float(np.min(arr)),
        "q05": float(np.quantile(arr, 0.05)),
        "q25": float(np.quantile(arr, 0.25)),
        "median": float(np.quantile(arr, 0.50)),
        "q75": float(np.quantile(arr, 0.75)),
        "q95": float(np.quantile(arr, 0.95)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
    }


def make_overlap_summary(rows: Sequence[AuditRow]) -> dict:
    distances = [r.center_distance for r in rows]
    disk_overlap = [r.disk_overlap_fraction for r in rows]

    result = {
        "pairs": int(len(rows)),
        "center_distance": quantiles(distances),
        "disk_overlap_fraction": quantiles(disk_overlap),
        "strict_nonoverlap_pairs": int(
            sum(r.strict_disk_nonoverlap for r in rows)
        ),
        "strict_nonoverlap_fraction": safe_fraction(
            sum(r.strict_disk_nonoverlap for r in rows),
            len(rows),
        ),
        "center_distance_counts": {
            str(d): int(sum(r.center_distance == d for r in rows))
            for d in sorted(set(distances))
        },
        "pairs_with_center_distance_le_1": int(
            sum(r.center_distance <= 1 for r in rows)
        ),
        "pairs_with_center_distance_le_2": int(
            sum(r.center_distance <= 2 for r in rows)
        ),
        "pairs_with_disk_overlap_ge_0_50": int(
            sum(r.disk_overlap_fraction >= 0.50 for r in rows)
        ),
        "pairs_with_disk_overlap_ge_0_75": int(
            sum(r.disk_overlap_fraction >= 0.75 for r in rows)
        ),
    }

    probe_values = [
        r.probe_overlap_fraction_smaller
        for r in rows
        if r.probe_overlap_fraction_smaller is not None
    ]

    if probe_values:
        result["probe_overlap_fraction_of_smaller"] = quantiles(
            probe_values
        )
        result["pairs_with_any_probe_overlap"] = int(
            sum(
                (r.probe_overlap_count or 0) > 0
                for r in rows
            )
        )

    occ_values = [
        r.occupied_overlap_fraction_smaller
        for r in rows
        if r.occupied_overlap_fraction_smaller is not None
    ]

    if occ_values:
        result["occupied_overlap_fraction_of_smaller"] = quantiles(
            occ_values
        )
        result["pairs_with_any_occupied_overlap"] = int(
            sum(
                (r.occupied_overlap_count or 0) > 0
                for r in rows
            )
        )

    return result


def apply_filters(
    rows: Sequence[AuditRow],
    radius: int,
) -> List[Tuple[str, List[AuditRow]]]:
    """
    These thresholds are reported as a sensitivity GRID.

    They are NOT chosen after looking at outcomes. The script reports all of
    them in one table precisely to avoid threshold fishing.
    """
    filters: List[Tuple[str, List[AuditRow]]] = []

    filters.append(("baseline_all_existing_pairs", list(rows)))

    for d in [2, 4, 6, 8, 2 * radius + 1]:
        filters.append(
            (
                f"center_distance_ge_{d}",
                [r for r in rows if r.center_distance >= d],
            )
        )

    for max_overlap in [0.75, 0.50, 0.25, 0.10, 0.0]:
        label = str(max_overlap).replace(".", "_")
        filters.append(
            (
                f"disk_overlap_fraction_le_{label}",
                [
                    r
                    for r in rows
                    if r.disk_overlap_fraction <= max_overlap + 1e-15
                ],
            )
        )

    # Exact strict non-overlap from actual disk intersections.
    filters.append(
        (
            "strict_disk_nonoverlap",
            [r for r in rows if r.strict_disk_nonoverlap],
        )
    )

    # Optional occupied-cell filters only if reconstructed.
    if any(r.occupied_overlap_fraction_smaller is not None for r in rows):
        for max_overlap in [0.75, 0.50, 0.25, 0.10, 0.0]:
            label = str(max_overlap).replace(".", "_")
            filters.append(
                (
                    f"occupied_overlap_fraction_smaller_le_{label}",
                    [
                        r
                        for r in rows
                        if (
                            r.occupied_overlap_fraction_smaller is not None
                            and r.occupied_overlap_fraction_smaller
                            <= max_overlap + 1e-15
                        )
                    ],
                )
            )

    return filters


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def fnum(value, digits=4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float) and not math.isfinite(value):
        return "NA"
    return f"{float(value):.{digits}f}"


def markdown_report(payload: dict) -> str:
    baseline = payload["baseline_reproduction"]
    overlap = payload["overlap_summary"]
    sensitivities = payload["sensitivity_grid"]

    lines = [
        "# Chapter 28 V2 — Spatial-Overlap Robustness Audit",
        "",
        "> **Epistemic status: POST-HOC ROBUSTNESS ONLY.** "
        "This audit does not replace or modify the frozen V2 result.",
        "",
        "## Baseline reproduction",
        "",
        "The audit first re-aggregates all existing V2 pairs using the "
        "group as the independent unit.",
        "",
        "```text",
        f"groups             {baseline['groups_retained']}",
        f"pairs              {baseline['pairs_retained']}",
        f"mean excess M      {fnum(baseline['excess_module_score']['mean'], 6)}",
        f"95% CI             "
        f"[{fnum(baseline['excess_module_score']['ci95_low'], 6)}, "
        f"{fnum(baseline['excess_module_score']['ci95_high'], 6)}]",
        "```",
        "",
        "## Existing-pair spatial overlap",
        "",
        "```text",
        f"matched pairs                    {overlap['pairs']}",
        f"strict non-overlap pairs         "
        f"{overlap['strict_nonoverlap_pairs']}",
        f"strict non-overlap fraction      "
        f"{fnum(overlap['strict_nonoverlap_fraction'], 4)}",
        f"pairs center distance <= 1       "
        f"{overlap['pairs_with_center_distance_le_1']}",
        f"pairs center distance <= 2       "
        f"{overlap['pairs_with_center_distance_le_2']}",
        f"pairs disk overlap >= 0.50       "
        f"{overlap['pairs_with_disk_overlap_ge_0_50']}",
        f"pairs disk overlap >= 0.75       "
        f"{overlap['pairs_with_disk_overlap_ge_0_75']}",
        "```",
        "",
        "Center-distance quantiles:",
        "",
        "```json",
        json.dumps(overlap.get("center_distance", {}), indent=2),
        "```",
        "",
        "Disk-overlap-fraction quantiles:",
        "",
        "```json",
        json.dumps(overlap.get("disk_overlap_fraction", {}), indent=2),
        "```",
        "",
    ]

    if "probe_overlap_fraction_of_smaller" in overlap:
        lines.extend(
            [
                "Probe-overlap-fraction quantiles:",
                "",
                "```json",
                json.dumps(
                    overlap["probe_overlap_fraction_of_smaller"],
                    indent=2,
                ),
                "```",
                "",
            ]
        )

    if "occupied_overlap_fraction_of_smaller" in overlap:
        lines.extend(
            [
                "Occupied-cell-overlap-fraction quantiles:",
                "",
                "```json",
                json.dumps(
                    overlap["occupied_overlap_fraction_of_smaller"],
                    indent=2,
                ),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Post-hoc sensitivity grid",
            "",
            "Each row recomputes the excess-modularity contrast after a "
            "spatial-distinctness filter. Within an observed region, retained "
            "controls are averaged first; observed regions are then averaged "
            "within group. Groups remain the independent statistical unit.",
            "",
            "| Filter | Pairs | Groups | Coverage | Mean excess M | 95% CI | MDE80 | Reference only |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in sensitivities:
        s = row["excess_module_score"]
        ci = (
            f"[{fnum(s['ci95_low'], 4)}, {fnum(s['ci95_high'], 4)}]"
            if s["n"] > 0
            else "NA"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    row["name"],
                    str(row["pairs_retained"]),
                    str(row["groups_retained"]),
                    fnum(row["group_coverage_fraction"], 3),
                    fnum(s["mean"], 4),
                    ci,
                    fnum(s["achieved_mde80_one_sided"], 4),
                    row["reference_only_status"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This audit may support statements such as:",
            "",
            "```text",
            "the frozen V2 result is / is not robust when near-overlapping",
            "selected-control pairs are removed",
            "```",
            "",
            "It does **not** change the frozen V2 status and does not create a "
            "new confirmatory threshold.",
            "",
            "If strict spatial separation leaves poor support, the correct "
            "next step is an explicitly labelled outcome-blind rematching "
            "sensitivity analysis — not weakening the separation rule after "
            "looking at the causal result.",
            "",
        ]
    )

    warnings = payload.get("warnings", [])
    if warnings:
        lines.extend(["## Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def infer_repo_root() -> Path:
    # scripts/books/digital-life/THIS_FILE.py -> repository root
    return Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Post-hoc spatial-overlap robustness audit for Chapter 28 V2."
        )
    )

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to path inferred from this script.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=None,
        help=(
            "V2 report directory. Defaults to "
            "research/digital-life/ch28-causal-modularity-v2"
        ),
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=DEFAULT_RADIUS,
    )
    parser.add_argument(
        "--excess-sei",
        type=float,
        default=DEFAULT_EXCESS_SEI,
    )
    parser.add_argument(
        "--bootstrap-reps",
        type=int,
        default=DEFAULT_BOOTSTRAP_REPS,
    )
    parser.add_argument(
        "--bootstrap-seed",
        type=int,
        default=DEFAULT_BOOTSTRAP_SEED,
    )
    parser.add_argument(
        "--reconstruct-occupied",
        action="store_true",
        help=(
            "Regenerate frozen V2 checkpoints to measure occupied-cell "
            "overlap. Does not rerun causal outcomes."
        ),
    )
    parser.add_argument(
        "--profile",
        default="full",
        choices=["smoke", "quick", "standard", "full"],
        help="Used only with --reconstruct-occupied.",
    )
    parser.add_argument(
        "--v2-seed",
        type=int,
        default=20260917,
        help="Frozen V2 seed used only with --reconstruct-occupied.",
    )

    args = parser.parse_args()

    repo_root = (
        args.repo_root.resolve()
        if args.repo_root is not None
        else infer_repo_root()
    )

    report_dir = (
        args.report_dir.resolve()
        if args.report_dir is not None
        else (
            repo_root
            / "research"
            / "digital-life"
            / "ch28-causal-modularity-v2"
        )
    )

    match_path = report_dir / "raw-v2-match-results.jsonl"
    probe_path = report_dir / "raw-v2-probe-results.jsonl"

    match_rows = read_jsonl(match_path)

    if not match_rows:
        raise RuntimeError(f"No match rows found in {match_path}")

    probe_rows: List[dict] = []
    if probe_path.exists():
        probe_rows = read_jsonl(probe_path)

    probe_index = build_probe_index(probe_rows)

    occupied_by_group = None
    if args.reconstruct_occupied:
        occupied_by_group = reconstruct_occupied(
            repo_root=repo_root,
            profile_name=args.profile,
            seed=args.v2_seed,
        )

    audit_rows = make_audit_rows(
        match_rows=match_rows,
        radius=int(args.radius),
        probe_index=probe_index,
        occupied_by_group=occupied_by_group,
    )

    total_groups = len({r.group for r in audit_rows})

    filters = apply_filters(
        audit_rows,
        radius=int(args.radius),
    )

    sensitivity_grid = []

    for i, (name, filtered_rows) in enumerate(filters):
        sensitivity_grid.append(
            sensitivity_result(
                name=name,
                rows=filtered_rows,
                total_groups=total_groups,
                reps=int(args.bootstrap_reps),
                seed=int(args.bootstrap_seed + 101 * i),
                excess_sei=float(args.excess_sei),
            )
        )

    baseline = sensitivity_grid[0]

    warnings: List[str] = []

    strict = next(
        (
            row
            for row in sensitivity_grid
            if row["name"] == "strict_disk_nonoverlap"
        ),
        None,
    )

    if strict is not None and strict["group_coverage_fraction"] < 0.90:
        warnings.append(
            "Strict non-overlap retains fewer than 90% of groups. "
            "Do not treat the strict-filter estimate as a clean replacement "
            "for frozen V2; consider a separately labelled outcome-blind "
            "rematching sensitivity analysis."
        )

    if not probe_rows:
        warnings.append(
            "raw-v2-probe-results.jsonl was not found; probe-overlap metrics "
            "were not computed."
        )

    if not args.reconstruct_occupied:
        warnings.append(
            "Occupied-cell overlap was not computed. Re-run with "
            "--reconstruct-occupied to regenerate checkpoints without "
            "rerunning causal outcomes."
        )

    payload = {
        "audit_version": "ch28-v2-spatial-overlap-posthoc-v1",
        "epistemic_status": "POST_HOC_ROBUSTNESS_ONLY",
        "frozen_v2_result_is_not_modified": True,
        "inputs": {
            "match_file": str(match_path),
            "probe_file": (
                str(probe_path)
                if probe_path.exists()
                else None
            ),
            "radius": int(args.radius),
            "strict_nonoverlap_definition": (
                "exact disk intersection == 0; for radius 4 this implies "
                "center distance >= 9"
            ),
            "reconstructed_occupied": bool(args.reconstruct_occupied),
            "v2_seed_if_reconstructed": (
                int(args.v2_seed)
                if args.reconstruct_occupied
                else None
            ),
            "profile_if_reconstructed": (
                args.profile
                if args.reconstruct_occupied
                else None
            ),
            "bootstrap_reps": int(args.bootstrap_reps),
            "bootstrap_seed": int(args.bootstrap_seed),
            "frozen_excess_SEI_reference": float(args.excess_sei),
        },
        "baseline_reproduction": baseline,
        "overlap_summary": make_overlap_summary(audit_rows),
        "sensitivity_grid": sensitivity_grid,
        "warnings": warnings,
    }

    json_rows = [asdict(r) for r in audit_rows]

    csv_path = report_dir / "raw-v2-spatial-overlap-audit.csv"
    jsonl_path = report_dir / "raw-v2-spatial-overlap-audit.jsonl"
    json_path = report_dir / "stage-07-spatial-overlap-audit.json"
    md_path = report_dir / "stage-07-spatial-overlap-audit.md"

    write_csv(csv_path, json_rows)
    write_jsonl(jsonl_path, json_rows)
    json_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(
        markdown_report(payload),
        encoding="utf-8",
    )

    print("Chapter 28 V2 spatial-overlap audit complete.")
    print(f"  pairs:        {len(audit_rows)}")
    print(f"  groups:       {total_groups}")
    print(
        "  baseline M:   "
        f"{baseline['excess_module_score']['mean']:.6f}"
    )
    print(
        "  strict pairs: "
        f"{payload['overlap_summary']['strict_nonoverlap_pairs']}"
    )
    print(
        "  strict frac:  "
        f"{payload['overlap_summary']['strict_nonoverlap_fraction']:.4f}"
    )
    print(f"  report:       {md_path}")

    if warnings:
        print("")
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
