#!/usr/bin/env python3
"""
Digital Life — Chapter 26 V1 Audit
True-Unbounded Primary Contrast + Per-Lag Construction-Rate Audit
=================================================================

THIS IS AN AUDIT, NOT A NEW SCIENTIFIC EXPERIMENT.

It preserves:
- original experiment: digital-crystal-matched-rate-causal-amplification-v1
- original seed: 20260912
- original checkpoints, probes, FORCE/PREVENT intervention, environment,
  keyed randomness, budget fractions, calibration rule, horizon, and SEI.

AUDIT A
-------
Compute the paired group contrast:
    G_T(f=0.10) - G_T(unbounded)
from the existing raw-amplification-arms.jsonl.

This is POST-HOC / SECONDARY and does not replace the frozen primary.

AUDIT B
-------
Deterministically replay the SAME seed/protocol and record per-lag expected
and realized construction for lags 1..12.

This is required because the original raw file did not serialize per-lag
construction rates.

The replay is an audit of the existing run, not a new scientific sample.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21
import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4
import ch26_digital_crystal_matched_rate_causal_amplification_v1 as ch26


AUDIT_VERSION = "ch26-v1-audit-true-unbounded-and-rate-drift"
ORIGINAL_SEED = 20260912
ORIGINAL_SEI = 0.15
ORIGINAL_MATCH_TOLERANCE = 0.02
HORIZON = ch26.HORIZON

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143


def finite_array(values: Sequence[float]) -> np.ndarray:
    return np.asarray(
        [float(v) for v in values if math.isfinite(float(v))],
        dtype=float,
    )


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = finite_array(values)

    if len(arr) == 0:
        return {
            "n": 0,
            "mean": float("nan"),
            "sd": float("nan"),
            "se": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
            "achieved_mde80_one_sided": float("nan"),
        }

    rng = np.random.default_rng(seed)
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
    se = sd / math.sqrt(len(arr)) if len(arr) else float("nan")

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
        "achieved_mde80_one_sided": float(
            se * (Z_95_ONE_SIDED + Z_80_POWER)
        ),
    }


def paired_posthoc_status(summary: dict) -> str:
    powered = summary["achieved_mde80_one_sided"] <= ORIGINAL_SEI

    if not powered:
        return "POSTHOC_UNRESOLVED_AT_ORIGINAL_SEI"

    if (
        summary["ci95_low"] > -ORIGINAL_SEI
        and summary["ci95_high"] < ORIGINAL_SEI
    ):
        return "POSTHOC_BOUNDED_WITHIN_ORIGINAL_SEI"

    if (
        summary["ci95_low"] > ORIGINAL_SEI
        or summary["ci95_high"] < -ORIGINAL_SEI
    ):
        return "POSTHOC_DIFFERENCE_EXCEEDS_ORIGINAL_SEI"

    return "POSTHOC_UNRESOLVED_AT_ORIGINAL_SEI"


def load_raw_arm_rows(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Raw Chapter 26 V1 file not found: {path}")

    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def group_arm_means_from_raw(
    rows: Sequence[dict],
    label: str,
    field: str,
) -> Dict[int, float]:
    buckets: Dict[int, List[float]] = {}

    for row in rows:
        if row["budget_label"] != label:
            continue

        value = float(row[field])
        if not math.isfinite(value):
            continue

        buckets.setdefault(int(row["group"]), []).append(value)

    return {
        group: float(np.mean(values))
        for group, values in buckets.items()
        if values
    }


def paired_raw_difference(
    rows: Sequence[dict],
    label_a: str,
    label_b: str,
    field: str,
) -> List[float]:
    a = group_arm_means_from_raw(rows, label_a, field)
    b = group_arm_means_from_raw(rows, label_b, field)
    common = sorted(set(a) & set(b))

    return [float(a[g] - b[g]) for g in common]


def audit_true_unbounded(
    raw_rows: Sequence[dict],
    bootstrap_reps: int,
    seed: int,
) -> dict:
    delta_G = paired_raw_difference(
        raw_rows, "f=0.10", "unbounded", "G_local"
    )

    summary_G = bootstrap_mean_ci(
        delta_G,
        bootstrap_reps,
        seed + 10,
    )

    delta_E1 = paired_raw_difference(
        raw_rows, "f=0.10", "unbounded", "E1_ring1"
    )
    delta_far = paired_raw_difference(
        raw_rows, "f=0.10", "unbounded", "E1_far"
    )
    delta_div = paired_raw_difference(
        raw_rows,
        "f=0.10",
        "unbounded",
        "realized_lag1_divergence",
    )
    delta_nonzero = paired_raw_difference(
        raw_rows, "f=0.10", "unbounded", "G_nonzero"
    )

    full_vs_unbounded_far = paired_raw_difference(
        raw_rows, "f=1.00", "unbounded", "E1_far"
    )
    full_vs_unbounded_G = paired_raw_difference(
        raw_rows, "f=1.00", "unbounded", "G_local"
    )

    return {
        "role": (
            "POST-HOC SECONDARY AUDIT; does not replace frozen V1 primary"
        ),
        "original_frozen_primary": "G_T(f=0.10) - G_T(f=1.00)",
        "audited_true_unbounded_contrast": (
            "G_T(f=0.10) - G_T(unbounded)"
        ),
        "original_SEI_abs": ORIGINAL_SEI,
        "G_local_0p10_minus_unbounded": summary_G,
        "posthoc_status": paired_posthoc_status(summary_G),
        "E1_ring1_0p10_minus_unbounded": bootstrap_mean_ci(
            delta_E1,
            bootstrap_reps,
            seed + 11,
        ),
        "E1_far_0p10_minus_unbounded": bootstrap_mean_ci(
            delta_far,
            bootstrap_reps,
            seed + 12,
        ),
        "lag1_realized_divergence_0p10_minus_unbounded": (
            bootstrap_mean_ci(
                delta_div,
                bootstrap_reps,
                seed + 13,
            )
        ),
        "G_nonzero_rate_0p10_minus_unbounded": bootstrap_mean_ci(
            delta_nonzero,
            bootstrap_reps,
            seed + 14,
        ),
        "f1p00_minus_unbounded_diagnostic": {
            "E1_far": bootstrap_mean_ci(
                full_vs_unbounded_far,
                bootstrap_reps,
                seed + 15,
            ),
            "G_local": bootstrap_mean_ci(
                full_vs_unbounded_G,
                bootstrap_reps,
                seed + 16,
            ),
            "interpretation": (
                "A non-zero f=1.00 minus unbounded E1_far confirms that "
                "f=1.00 is not operationally identical to dynamic "
                "full-frontier evaluation throughout continuation."
            ),
        },
    }


@dataclass
class LagAuditRow:
    group: int
    probe_index: int
    budget_label: str
    fraction: float | None
    lag: int
    target_expected_attachments: float
    offset: float
    budget: int | None
    force_frontier_size: int
    prevent_frontier_size: int
    force_selected_count: int
    prevent_selected_count: int
    force_expected_attachments: float
    prevent_expected_attachments: float
    mean_expected_attachments: float
    force_realized_attachments: int
    prevent_realized_attachments: int
    mean_realized_attachments: float
    force_relative_expected_error: float
    prevent_relative_expected_error: float
    mean_relative_expected_error: float
    branch_expected_difference: float


def clone_state(state: ch18.MaterialCrystalState) -> ch18.MaterialCrystalState:
    return ch18.MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def expected_for_current_state(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
) -> Tuple[float, List[Tuple[int, int]], int]:
    frontier = v4.frontier_cells(set(state.occupied), radius)

    selected = ch26.select_candidates_for_budget(
        frontier,
        state,
        budget,
    )

    expected = ch26.expected_selected_attachments(
        state,
        input_value,
        selected,
        crystal_params,
        offset,
    )

    return float(expected), selected, int(len(frontier))


def replay_probe_arm(
    prepared: ch26.PreparedIntervention,
    calibration: ch26.ArmCalibration,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[LagAuditRow]:
    probe = prepared.probe
    force_state = clone_state(prepared.force_state)
    prevent_state = clone_state(prepared.prevent_state)

    radius = int(source_profile["radius"])
    loss_rate = float(source_profile["loss_rate"])
    x = probe.cell
    target = float(calibration.target_expected_attachments)

    rows: List[LagAuditRow] = []

    for lag in range(1, HORIZON + 1):
        input_value = float(probe.future_env[lag])

        force_expected, force_selected_pre, force_frontier_size = (
            expected_for_current_state(
                force_state,
                input_value,
                radius,
                crystal_params,
                calibration.budget,
                calibration.offset,
            )
        )

        prevent_expected, prevent_selected_pre, prevent_frontier_size = (
            expected_for_current_state(
                prevent_state,
                input_value,
                radius,
                crystal_params,
                calibration.budget,
                calibration.offset,
            )
        )

        (
            force_state,
            force_add,
            _force_lost,
            force_selected_actual,
        ) = ch26.calibrated_canonical_step(
            force_state,
            input_value,
            radius,
            crystal_params,
            calibration.budget,
            calibration.offset,
            loss_rate,
        )

        (
            prevent_state,
            prevent_add,
            _prevent_lost,
            prevent_selected_actual,
        ) = ch26.calibrated_canonical_step(
            prevent_state,
            input_value,
            radius,
            crystal_params,
            calibration.budget,
            calibration.offset,
            loss_rate,
        )

        if force_selected_pre != force_selected_actual:
            raise RuntimeError(
                "Audit FORCE selected-set mismatch against replay step."
            )

        if prevent_selected_pre != prevent_selected_actual:
            raise RuntimeError(
                "Audit PREVENT selected-set mismatch against replay step."
            )

        force_rel_error = (
            (force_expected - target)
            / max(target, 1e-12)
        )

        prevent_rel_error = (
            (prevent_expected - target)
            / max(target, 1e-12)
        )

        mean_expected = (force_expected + prevent_expected) / 2.0
        mean_rel_error = (
            mean_expected - target
        ) / max(target, 1e-12)

        force_realized = len([c for c in force_add if c != x])
        prevent_realized = len([c for c in prevent_add if c != x])

        rows.append(
            LagAuditRow(
                group=int(probe.group),
                probe_index=int(probe.probe_index),
                budget_label=calibration.budget_label,
                fraction=calibration.fraction,
                lag=int(lag),
                target_expected_attachments=target,
                offset=float(calibration.offset),
                budget=calibration.budget,
                force_frontier_size=int(force_frontier_size),
                prevent_frontier_size=int(prevent_frontier_size),
                force_selected_count=int(len(force_selected_pre)),
                prevent_selected_count=int(len(prevent_selected_pre)),
                force_expected_attachments=float(force_expected),
                prevent_expected_attachments=float(prevent_expected),
                mean_expected_attachments=float(mean_expected),
                force_realized_attachments=int(force_realized),
                prevent_realized_attachments=int(prevent_realized),
                mean_realized_attachments=float(
                    (force_realized + prevent_realized) / 2.0
                ),
                force_relative_expected_error=float(force_rel_error),
                prevent_relative_expected_error=float(prevent_rel_error),
                mean_relative_expected_error=float(mean_rel_error),
                branch_expected_difference=float(
                    force_expected - prevent_expected
                ),
            )
        )

        if lag == 1 and x in force_state.occupied:
            force_state.occupied.remove(x)
            force_state.birth_time.pop(x, None)

            if force_state.population_by_step:
                force_state.population_by_step[-1] = len(
                    force_state.occupied
                )

    return rows


def replay_all_lags(
    profile_name: str,
    seed: int,
) -> Tuple[List[LagAuditRow], dict]:
    profile = dict(ch26.PROFILES[profile_name])

    source_profile = dict(
        v4.PROFILES[profile["source_profile"]]
    )
    source_profile["groups"] = int(profile["groups"])
    source_profile["horizon"] = HORIZON

    crystal_params = ch18.CrystalParams()

    probes, support = ch26.prepare_probes(
        profile,
        source_profile,
        crystal_params,
        seed,
    )

    rows: List[LagAuditRow] = []
    invalid_calibrations = 0
    total_calibrations = 0

    for probe in tqdm(
        probes,
        desc="Chapter 26 deterministic lag audit",
    ):
        prepared = ch26.prepare_common_intervention(
            probe,
            source_profile,
            crystal_params,
        )

        arms, _ = ch26.calibrate_probe_arms(
            prepared,
            source_profile,
            crystal_params,
        )

        for calibration in arms.values():
            total_calibrations += 1

            if not calibration.valid:
                invalid_calibrations += 1
                continue

            rows.extend(
                replay_probe_arm(
                    prepared,
                    calibration,
                    source_profile,
                    crystal_params,
                )
            )

    return rows, {
        "profile": profile_name,
        "seed": int(seed),
        "groups": int(profile["groups"]),
        "probes": int(len(probes)),
        "probe_support": support,
        "total_calibrations": int(total_calibrations),
        "invalid_calibrations": int(invalid_calibrations),
        "audit_rows": int(len(rows)),
    }


def group_lag_means(
    rows: Sequence[LagAuditRow],
    label: str,
    lag: int,
    getter,
) -> List[float]:
    buckets: Dict[int, List[float]] = {}

    for row in rows:
        if row.budget_label != label or row.lag != lag:
            continue

        value = float(getter(row))
        if not math.isfinite(value):
            continue

        buckets.setdefault(row.group, []).append(value)

    return [
        float(np.mean(values))
        for _, values in sorted(buckets.items())
        if values
    ]


def aggregate_rate_audit(
    rows: Sequence[LagAuditRow],
    bootstrap_reps: int,
    seed: int,
) -> dict:
    labels = [
        f"f={fraction:.2f}"
        for fraction in ch26.FRACTIONS
    ] + ["unbounded"]

    per_arm = {}

    for arm_index, label in enumerate(labels):
        arm_raw = [
            row
            for row in rows
            if row.budget_label == label
        ]

        target_values = [
            row.target_expected_attachments
            for row in arm_raw
        ]

        target_mean = (
            float(np.mean(target_values))
            if target_values
            else float("nan")
        )

        lag_rows = {}

        for lag in range(1, HORIZON + 1):
            mean_expected = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.mean_expected_attachments,
            )
            force_expected = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.force_expected_attachments,
            )
            prevent_expected = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.prevent_expected_attachments,
            )
            mean_rel = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.mean_relative_expected_error,
            )
            force_rel = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.force_relative_expected_error,
            )
            prevent_rel = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.prevent_relative_expected_error,
            )
            realized = group_lag_means(
                rows,
                label,
                lag,
                lambda r: r.mean_realized_attachments,
            )

            lag_rows[str(lag)] = {
                "mean_expected_attachments": bootstrap_mean_ci(
                    mean_expected,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20,
                ),
                "force_expected_attachments": bootstrap_mean_ci(
                    force_expected,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 1,
                ),
                "prevent_expected_attachments": bootstrap_mean_ci(
                    prevent_expected,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 2,
                ),
                "mean_relative_expected_error": bootstrap_mean_ci(
                    mean_rel,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 3,
                ),
                "force_relative_expected_error": bootstrap_mean_ci(
                    force_rel,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 4,
                ),
                "prevent_relative_expected_error": bootstrap_mean_ci(
                    prevent_rel,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 5,
                ),
                "mean_realized_attachments": bootstrap_mean_ci(
                    realized,
                    bootstrap_reps,
                    seed + arm_index * 500 + lag * 20 + 6,
                ),
            }

        abs_errors = np.asarray(
            [
                abs(row.mean_relative_expected_error)
                for row in arm_raw
            ],
            dtype=float,
        )

        pop_abs = [
            abs(
                lag_rows[str(lag)][
                    "mean_relative_expected_error"
                ]["mean"]
            )
            for lag in range(1, HORIZON + 1)
        ]

        per_arm[label] = {
            "target_expected_attachments_mean": target_mean,
            "lags": lag_rows,
            "all_probe_lag_records_within_original_2pct": (
                float(
                    np.mean(
                        abs_errors
                        <= ORIGINAL_MATCH_TOLERANCE
                    )
                )
                if len(abs_errors)
                else float("nan")
            ),
            "mean_absolute_record_level_relative_deviation": (
                float(np.mean(abs_errors))
                if len(abs_errors)
                else float("nan")
            ),
            "max_population_mean_relative_deviation_across_lags": (
                float(max(pop_abs))
                if pop_abs
                else float("nan")
            ),
        }

    cross_arm = {}

    for lag in range(1, HORIZON + 1):
        arm_means = {
            label: per_arm[label]["lags"][str(lag)][
                "mean_expected_attachments"
            ]["mean"]
            for label in labels
        }

        values = np.asarray(
            list(arm_means.values()),
            dtype=float,
        )

        cross_arm[str(lag)] = {
            "arm_means": arm_means,
            "range": float(np.max(values) - np.min(values)),
            "coefficient_of_variation": (
                float(np.std(values) / np.mean(values))
                if np.mean(values) != 0
                else float("nan")
            ),
            "max_pairwise_relative_spread": (
                float(
                    (np.max(values) - np.min(values))
                    / np.mean(values)
                )
                if np.mean(values) != 0
                else float("nan")
            ),
        }

    return {
        "original_match_tolerance": ORIGINAL_MATCH_TOLERANCE,
        "interpretation": (
            "The original 2% tolerance was frozen for lag-1 calibration only. "
            "Later-lag values are diagnostic and do not retroactively alter "
            "the original validity status."
        ),
        "per_arm": per_arm,
        "cross_arm_expected_construction_dispersion": cross_arm,
    }


def write_lag_rows(
    root: Path,
    rows: Sequence[LagAuditRow],
) -> None:
    jsonl = root / "raw-per-lag-construction-audit.jsonl"

    with jsonl.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row)) + "\n")

    if not rows:
        return

    csv_path = root / "raw-per-lag-construction-audit.csv"
    fields = list(asdict(rows[0]).keys())

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(asdict(row))


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source-report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch26-matched-rate-causal-amplification-v1"
        ),
    )

    parser.add_argument(
        "--profile",
        choices=sorted(ch26.PROFILES),
        default="full",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=ORIGINAL_SEED,
    )

    parser.add_argument(
        "--allow-different-seed",
        action="store_true",
    )

    parser.add_argument(
        "--bootstrap-reps",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch26-v1-audit"
        ),
    )

    parser.add_argument(
        "--skip-replay",
        action="store_true",
        help=(
            "Run only raw-data Audit A. "
            "Per-lag rate audit will not be produced."
        ),
    )

    args = parser.parse_args()

    if (
        args.seed != ORIGINAL_SEED
        and not args.allow_different_seed
    ):
        raise RuntimeError(
            "Scientific audit must replay original seed 20260912. "
            "Use --allow-different-seed only for engineering diagnostics."
        )

    profile = dict(ch26.PROFILES[args.profile])

    bootstrap_reps = (
        int(args.bootstrap_reps)
        if args.bootstrap_reps is not None
        else int(profile["bootstrap_reps"])
    )

    args.audit_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = {
        "audit_version": AUDIT_VERSION,
        "audited_experiment": ch26.EXPERIMENT_VERSION,
        "profile": args.profile,
        "seed": int(args.seed),
        "original_seed": ORIGINAL_SEED,
        "same_seed": bool(args.seed == ORIGINAL_SEED),
        "original_SEI": ORIGINAL_SEI,
        "original_match_tolerance": ORIGINAL_MATCH_TOLERANCE,
        "scientific_status": "AUDIT_ONLY_NOT_NEW_EXPERIMENT",
    }

    raw_path = (
        args.source_report_dir
        / "raw-amplification-arms.jsonl"
    )

    print("=" * 78)
    print("CHAPTER 26 V1 AUDIT")
    print(f"Source raw: {raw_path}")
    print(f"Replay profile: {args.profile}")
    print(f"Seed: {args.seed}")
    print("=" * 78)

    raw_rows = load_raw_arm_rows(raw_path)

    audit_a = audit_true_unbounded(
        raw_rows,
        bootstrap_reps,
        args.seed + 10000,
    )

    (
        args.audit_dir
        / "audit-a-true-unbounded-contrast.json"
    ).write_text(
        json.dumps(audit_a, indent=2),
        encoding="utf-8",
    )

    if args.skip_replay:
        result = {
            "metadata": metadata,
            "audit_A_true_unbounded": audit_a,
            "audit_B_rate_drift": "SKIPPED",
        }

        (
            args.audit_dir
            / "ch26-v1-audit-report.json"
        ).write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

        print(
            json.dumps(
                {
                    "posthoc_true_unbounded": (
                        audit_a[
                            "G_local_0p10_minus_unbounded"
                        ]
                    ),
                    "status": audit_a["posthoc_status"],
                },
                indent=2,
            )
        )
        return

    lag_rows, replay_info = replay_all_lags(
        args.profile,
        args.seed,
    )

    write_lag_rows(
        args.audit_dir,
        lag_rows,
    )

    audit_b = aggregate_rate_audit(
        lag_rows,
        bootstrap_reps,
        args.seed + 20000,
    )

    (
        args.audit_dir
        / "audit-b-per-lag-rate-drift.json"
    ).write_text(
        json.dumps(audit_b, indent=2),
        encoding="utf-8",
    )

    result = {
        "metadata": metadata,
        "replay_info": replay_info,
        "audit_A_true_unbounded": audit_a,
        "audit_B_rate_drift": audit_b,
        "interpretation_boundary": {
            "frozen_primary_status_unchanged": True,
            "audit_A_is_posthoc_secondary": True,
            "audit_B_is_deterministic_same_seed_diagnostic": True,
            "no_new_seed_used": bool(args.seed == ORIGINAL_SEED),
        },
    }

    (
        args.audit_dir
        / "ch26-v1-audit-report.json"
    ).write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    md_path = (
        args.audit_dir
        / "ch26-v1-audit-report.md"
    )

    md = [
        "# Chapter 26 V1 Audit",
        "",
        "## Audit status",
        "",
        "```json",
        json.dumps(metadata, indent=2),
        "```",
        "",
        "## Audit A — f=.10 versus true unbounded",
        "",
        "```json",
        json.dumps(audit_a, indent=2),
        "```",
        "",
        "## Audit B — per-lag construction-rate drift",
        "",
        "```json",
        json.dumps(audit_b, indent=2),
        "```",
        "",
        "## Interpretation boundary",
        "",
        "- The frozen Chapter 26 V1 primary verdict is not rewritten.",
        "- Audit A is post-hoc / secondary.",
        "- Audit B replays the original seed deterministically and adds missing diagnostics.",
        "- No fresh scientific sample is introduced.",
        "",
    ]

    md_path.write_text(
        "\n".join(md),
        encoding="utf-8",
    )

    print()
    print("=" * 78)
    print("AUDIT A")
    print(
        json.dumps(
            {
                "contrast": audit_a[
                    "audited_true_unbounded_contrast"
                ],
                "result": audit_a[
                    "G_local_0p10_minus_unbounded"
                ],
                "status": audit_a["posthoc_status"],
            },
            indent=2,
        )
    )
    print()
    print(f"Audit report: {md_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
