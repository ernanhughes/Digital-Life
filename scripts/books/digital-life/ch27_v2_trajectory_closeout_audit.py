#!/usr/bin/env python3
"""
Chapter 27 V2 trajectory closeout audit.

Analysis-only. Reads existing V2 raw outputs and asks:
does the accessible-minus-remote downstream causal effect merely track the
decaying material trace, or does it continue after the trace has weakened?

No new simulation. No changed SEI. No changed V2 verdict.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

H = 12
M0 = 2 * 0.7071067811865476
HALF = 0.50 * M0
QUARTER = 0.25 * M0
Z95 = 1.6448536269514722
Z80 = 0.8416212335729143

EPOCHS = {
    "early": (1, 4),
    "middle": (5, 8),
    "late": (9, 12),
}


def read_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows):
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                fields.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def finite(values):
    return np.asarray(
        [float(v) for v in values if math.isfinite(float(v))],
        dtype=float,
    )


def boot(values, reps, seed):
    arr = finite(values)
    if len(arr) == 0:
        return {
            "n": 0, "mean": float("nan"), "sd": float("nan"),
            "se": float("nan"), "ci95_low": float("nan"),
            "ci95_high": float("nan"),
            "achieved_mde80_one_sided": float("nan"),
        }
    rng = np.random.default_rng(seed)
    bs = np.empty(reps)
    for i in range(reps):
        bs[i] = np.mean(rng.choice(arr, size=len(arr), replace=True))
    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / math.sqrt(len(arr))
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": float(np.quantile(bs, 0.025)),
        "ci95_high": float(np.quantile(bs, 0.975)),
        "achieved_mde80_one_sided": float(se * (Z95 + Z80)),
    }


def corr(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def ols_hc1(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.all(np.isfinite(X), axis=1) & np.isfinite(y)
    X, y = X[m], y[m]
    n, p = X.shape
    inv = np.linalg.pinv(X.T @ X)
    beta = inv @ X.T @ y
    resid = y - X @ beta
    meat = np.zeros((p, p))
    for i in range(n):
        xi = X[i:i+1].T
        meat += (resid[i] ** 2) * (xi @ xi.T)
    cov = (n / max(1, n - p)) * (inv @ meat @ inv)
    se = np.sqrt(np.maximum(0.0, np.diag(cov)))
    return {
        "n": int(n),
        "coef": [float(v) for v in beta],
        "se_hc1": [float(v) for v in se],
    }


def group_arm_lag_means(rows):
    fields = [
        "expected_local_causal_increment",
        "prevent_material_mass",
        "force_material_mass",
        "offset",
        "prevent_realized_attachments",
        "force_realized_attachments",
    ]
    buckets = defaultdict(lambda: defaultdict(list))
    for r in rows:
        key = (int(r["group"]), r["history_arm"], int(r["lag"]))
        for f in fields:
            buckets[key][f].append(float(r[f]))
    out = {}
    for key, vals in buckets.items():
        out[key] = {f: float(np.mean(v)) for f, v in vals.items()}
        out[key]["realized_total_increment"] = (
            out[key]["force_realized_attachments"]
            - out[key]["prevent_realized_attachments"]
        )
    return out


def complete_groups(g):
    groups = sorted({k[0] for k in g})
    return [
        group for group in groups
        if all((group, arm, lag) in g
               for arm in ("accessible", "remote")
               for lag in range(1, H + 1))
    ]


def build_group_lag(g, groups):
    rows = []
    cum = {grp: 0.0 for grp in groups}
    for lag in range(1, H + 1):
        for grp in groups:
            a = g[(grp, "accessible", lag)]
            r = g[(grp, "remote", lag)]
            d = (
                a["expected_local_causal_increment"]
                - r["expected_local_causal_increment"]
            )
            cum[grp] += d
            rows.append({
                "group": grp,
                "lag": lag,
                "delta_RB_increment": d,
                "cumulative_delta_RB": cum[grp],
                "accessible_prevent_material_mass": a["prevent_material_mass"],
                "remote_prevent_material_mass": r["prevent_material_mass"],
                "delta_prevent_material_mass": (
                    a["prevent_material_mass"] - r["prevent_material_mass"]
                ),
                "accessible_force_material_mass": a["force_material_mass"],
                "remote_force_material_mass": r["force_material_mass"],
                "accessible_offset": a["offset"],
                "remote_offset": r["offset"],
                "delta_offset": a["offset"] - r["offset"],
                "delta_realized_total_increment_DIAGNOSTIC": (
                    a["realized_total_increment"]
                    - r["realized_total_increment"]
                ),
            })
    return rows


def per_lag_summary(rows, reps, seed):
    by_lag = defaultdict(list)
    for r in rows:
        by_lag[int(r["lag"])].append(r)

    out = {}
    csv_rows = []

    for lag in range(1, H + 1):
        rr = by_lag[lag]
        payload = {
            "delta_RB_increment": boot(
                [x["delta_RB_increment"] for x in rr], reps, seed + lag * 100 + 1
            ),
            "cumulative_delta_RB": boot(
                [x["cumulative_delta_RB"] for x in rr], reps, seed + lag * 100 + 2
            ),
            "accessible_prevent_material_mass": boot(
                [x["accessible_prevent_material_mass"] for x in rr],
                reps, seed + lag * 100 + 3,
            ),
            "remote_prevent_material_mass": boot(
                [x["remote_prevent_material_mass"] for x in rr],
                reps, seed + lag * 100 + 4,
            ),
            "delta_prevent_material_mass": boot(
                [x["delta_prevent_material_mass"] for x in rr],
                reps, seed + lag * 100 + 5,
            ),
            "delta_offset": boot(
                [x["delta_offset"] for x in rr], reps, seed + lag * 100 + 6
            ),
            "delta_realized_total_increment_DIAGNOSTIC": boot(
                [x["delta_realized_total_increment_DIAGNOSTIC"] for x in rr],
                reps, seed + lag * 100 + 7,
            ),
        }
        out[str(lag)] = payload
        csv_rows.append({
            "lag": lag,
            "delta_RB_increment_mean": payload["delta_RB_increment"]["mean"],
            "delta_RB_increment_ci_low": payload["delta_RB_increment"]["ci95_low"],
            "delta_RB_increment_ci_high": payload["delta_RB_increment"]["ci95_high"],
            "cumulative_delta_RB_mean": payload["cumulative_delta_RB"]["mean"],
            "cumulative_delta_RB_ci_low": payload["cumulative_delta_RB"]["ci95_low"],
            "cumulative_delta_RB_ci_high": payload["cumulative_delta_RB"]["ci95_high"],
            "accessible_material_mass_mean": payload["accessible_prevent_material_mass"]["mean"],
            "remote_material_mass_mean": payload["remote_prevent_material_mass"]["mean"],
            "delta_material_mass_mean": payload["delta_prevent_material_mass"]["mean"],
            "delta_offset_mean": payload["delta_offset"]["mean"],
            "delta_realized_total_increment_diagnostic_mean": (
                payload["delta_realized_total_increment_DIAGNOSTIC"]["mean"]
            ),
        })
    return out, csv_rows


def epoch_summary(rows, reps, seed):
    by_group = defaultdict(list)
    for r in rows:
        by_group[int(r["group"])].append(r)

    out = {}
    csv_rows = []

    for idx, (name, (lo, hi)) in enumerate(EPOCHS.items()):
        contrib = []
        mean_inc = []
        mass_a = []
        mass_r = []
        d_offset = []

        for grp, rr in by_group.items():
            selected = [x for x in rr if lo <= int(x["lag"]) <= hi]
            contrib.append(sum(x["delta_RB_increment"] for x in selected))
            mean_inc.append(np.mean([x["delta_RB_increment"] for x in selected]))
            mass_a.append(np.mean([x["accessible_prevent_material_mass"] for x in selected]))
            mass_r.append(np.mean([x["remote_prevent_material_mass"] for x in selected]))
            d_offset.append(np.mean([x["delta_offset"] for x in selected]))

        p = {
            "lags": [lo, hi],
            "RB_contribution": boot(contrib, reps, seed + idx * 20 + 1),
            "mean_RB_increment": boot(mean_inc, reps, seed + idx * 20 + 2),
            "accessible_material_mass": boot(mass_a, reps, seed + idx * 20 + 3),
            "remote_material_mass": boot(mass_r, reps, seed + idx * 20 + 4),
            "delta_offset": boot(d_offset, reps, seed + idx * 20 + 5),
        }
        out[name] = p
        csv_rows.append({
            "epoch": name,
            "lag_start": lo,
            "lag_end": hi,
            "RB_contribution_mean": p["RB_contribution"]["mean"],
            "RB_contribution_ci_low": p["RB_contribution"]["ci95_low"],
            "RB_contribution_ci_high": p["RB_contribution"]["ci95_high"],
            "mean_RB_increment": p["mean_RB_increment"]["mean"],
            "accessible_material_mass_mean": p["accessible_material_mass"]["mean"],
            "remote_material_mass_mean": p["remote_material_mass"]["mean"],
            "delta_offset_mean": p["delta_offset"]["mean"],
        })
    return out, csv_rows


def decay_closeout(per_lag):
    mass = {
        lag: float(per_lag[str(lag)]["accessible_prevent_material_mass"]["mean"])
        for lag in range(1, H + 1)
    }
    inc = {
        lag: float(per_lag[str(lag)]["delta_RB_increment"]["mean"])
        for lag in range(1, H + 1)
    }
    cum = {
        lag: float(per_lag[str(lag)]["cumulative_delta_RB"]["mean"])
        for lag in range(1, H + 1)
    }

    first_half = next((l for l in range(1, H + 1) if mass[l] <= HALF), None)
    first_quarter = next((l for l in range(1, H + 1) if mass[l] <= QUARTER), None)
    final = cum[H]

    def threshold_info(first):
        if first is None:
            return {
                "reached": False,
                "first_lag": None,
                "effect_before_threshold": float("nan"),
                "effect_accrued_after_threshold": float("nan"),
                "absolute_fraction_of_final": float("nan"),
            }
        before = cum[first - 1] if first > 1 else 0.0
        after = final - before
        return {
            "reached": True,
            "first_lag": int(first),
            "effect_before_threshold": float(before),
            "effect_accrued_after_threshold": float(after),
            "absolute_fraction_of_final": float(
                abs(after) / max(abs(final), 1e-12)
            ),
        }

    half = threshold_info(first_half)
    quarter = threshold_info(first_quarter)
    late_mean = float(np.mean([inc[l] for l in range(9, 13)]))

    fsign = -1 if final < 0 else 1 if final > 0 else 0
    lsign = -1 if late_mean < 0 else 1 if late_mean > 0 else 0

    if (
        half["reached"]
        and half["absolute_fraction_of_final"] < 0.20
        and abs(late_mean) < 0.02
    ):
        desc = "TRACE_TRACKING"
    elif (
        half["reached"]
        and half["absolute_fraction_of_final"] >= 0.40
        and lsign == fsign
        and abs(late_mean) >= 0.02
    ):
        desc = "TRAJECTORY_PERSISTENCE"
    else:
        desc = "MIXED_TRANSIENT_AND_TRAJECTORY"

    return {
        "initial_material_mass": M0,
        "half_mass_threshold": HALF,
        "quarter_mass_threshold": QUARTER,
        "first_half_mass_or_lower": half,
        "first_quarter_mass_or_lower": quarter,
        "final_cumulative_delta_RB": final,
        "late_mean_delta_RB_increment": late_mean,
        "suggested_descriptive_mechanism": desc,
        "descriptor_role": "DESCRIPTIVE_CLOSEOUT_HEURISTIC_NOT_CONFIRMATORY_STATUS",
    }


def tracking_models(rows):
    material = np.asarray(
        [r["accessible_prevent_material_mass"] for r in rows], dtype=float
    )
    inc = np.asarray([r["delta_RB_increment"] for r in rows], dtype=float)
    lag = np.asarray([r["lag"] for r in rows], dtype=float)

    pooled = ols_hc1(
        np.column_stack([np.ones(len(rows)), material, lag]),
        inc,
    )

    by_group = defaultdict(list)
    for r in rows:
        by_group[int(r["group"])].append(r)

    final = []
    mean_mass = []
    mean_delta_mass = []
    for grp, rr in sorted(by_group.items()):
        rr = sorted(rr, key=lambda x: int(x["lag"]))
        final.append(rr[-1]["cumulative_delta_RB"])
        mean_mass.append(np.mean([x["accessible_prevent_material_mass"] for x in rr]))
        mean_delta_mass.append(np.mean([x["delta_prevent_material_mass"] for x in rr]))

    group_fit = ols_hc1(
        np.column_stack(
            [np.ones(len(final)), np.asarray(mean_mass), np.asarray(mean_delta_mass)]
        ),
        np.asarray(final),
    )

    return {
        "pooled_group_lag": {
            "correlation_accessible_material_mass_vs_delta_RB_increment": corr(
                material, inc
            ),
            "model": (
                "Delta_RB_increment = intercept + beta_mass * "
                "accessible_material_mass + beta_lag * lag"
            ),
            "intercept": pooled["coef"][0],
            "beta_mass": pooled["coef"][1],
            "beta_lag": pooled["coef"][2],
            "intercept_HC1_SE": pooled["se_hc1"][0],
            "beta_mass_HC1_SE": pooled["se_hc1"][1],
            "beta_lag_HC1_SE": pooled["se_hc1"][2],
            "role": "DESCRIPTIVE_ONLY_ROWS_NOT_INDEPENDENT",
        },
        "group_final_effect": {
            "corr_final_delta_RB_vs_mean_accessible_mass": corr(final, mean_mass),
            "corr_final_delta_RB_vs_mean_delta_material_mass": corr(
                final, mean_delta_mass
            ),
            "model": (
                "final_Delta_RB = intercept + beta_mean_accessible_mass * "
                "mean_accessible_mass + beta_delta_mass * mean_delta_mass"
            ),
            "intercept": group_fit["coef"][0],
            "beta_mean_accessible_mass": group_fit["coef"][1],
            "beta_delta_mass": group_fit["coef"][2],
            "intercept_HC1_SE": group_fit["se_hc1"][0],
            "beta_mean_accessible_mass_HC1_SE": group_fit["se_hc1"][1],
            "beta_delta_mass_HC1_SE": group_fit["se_hc1"][2],
            "role": "DESCRIPTIVE_ONLY",
        },
    }


def reconcile(arm_rows, group_rows):
    arm = defaultdict(list)
    for r in arm_rows:
        arm[(int(r["group"]), r["history_arm"])].append(float(r["RB_G_local"]))

    by_group = defaultdict(list)
    for r in group_rows:
        by_group[int(r["group"])].append(r)

    errors = []
    for grp, rr in by_group.items():
        expected = (
            np.mean(arm[(grp, "accessible")])
            - np.mean(arm[(grp, "remote")])
        )
        reconstructed = sorted(rr, key=lambda x: x["lag"])[-1]["cumulative_delta_RB"]
        errors.append(float(reconstructed - expected))

    max_abs = max(abs(x) for x in errors)
    return {
        "n_groups": len(errors),
        "max_abs_group_reconciliation_error": float(max_abs),
        "mean_error": float(np.mean(errors)),
        "status": "PASS" if max_abs <= 1e-9 else "FAIL",
        "role": "CORRECTNESS_ASSERTION_NOT_FINDING",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--source-report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch27-decaying-material-history-causal-response-v2"
        ),
    )
    p.add_argument(
        "--audit-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch27-v2-trajectory-closeout-audit"
        ),
    )
    p.add_argument("--bootstrap-reps", type=int, default=7000)
    p.add_argument("--seed", type=int, default=20260915)
    args = p.parse_args()

    args.audit_dir.mkdir(parents=True, exist_ok=True)

    lag_rows = read_jsonl(args.source_report_dir / "raw-v2-per-lag.jsonl")
    arm_rows = read_jsonl(args.source_report_dir / "raw-v2-arm-results.jsonl")
    primary = read_json(args.source_report_dir / "stage-04-primary.json")
    verdict = read_json(args.source_report_dir / "stage-07-verdict.json")

    print("=" * 78)
    print("CHAPTER 27 V2 TRAJECTORY / CLOSEOUT AUDIT")
    print(f"per-lag rows: {len(lag_rows)}")
    print(f"arm rows: {len(arm_rows)}")
    print("=" * 78)

    grouped = group_arm_lag_means(lag_rows)
    groups = complete_groups(grouped)
    print(f"complete paired groups: {len(groups)}")

    group_rows = build_group_lag(grouped, groups)
    per_lag, per_lag_csv = per_lag_summary(
        group_rows, args.bootstrap_reps, args.seed + 10000
    )
    epochs, epoch_csv = epoch_summary(
        group_rows, args.bootstrap_reps, args.seed + 20000
    )
    decay = decay_closeout(per_lag)
    tracking = tracking_models(group_rows)
    check = reconcile(arm_rows, group_rows)

    if check["status"] != "PASS":
        raise RuntimeError(
            "Per-lag cumulative RB values do not reconcile with arm-level RB_G_local."
        )

    formal_status = (
        primary.get("status", "UNKNOWN_NOT_FOUND")
        if primary
        else "UNKNOWN_NOT_FOUND"
    )

    final_ci_low = per_lag[str(H)]["cumulative_delta_RB"]["ci95_low"]
    final_ci_high = per_lag[str(H)]["cumulative_delta_RB"]["ci95_high"]

    direction = (
        "NEGATIVE"
        if final_ci_high < 0
        else "POSITIVE"
        if final_ci_low > 0
        else "UNRESOLVED_DIRECTION"
    )

    desc = decay["suggested_descriptive_mechanism"]

    if desc == "TRACE_TRACKING":
        sentence = (
            "The accessible-history causal difference was concentrated while "
            "the material trace remained strong, with little additional expected "
            "causal difference accumulating after the trace weakened. The V2 "
            "trajectory is therefore most consistent with a transient "
            "trace-tracking mechanism."
        )
    elif desc == "TRAJECTORY_PERSISTENCE":
        sentence = (
            "A substantial share of the accessible-history causal difference "
            "continued to accumulate after the material trace had fallen below "
            "half its initial mass, while late expected increments retained the "
            "same direction. The V2 trajectory is therefore most consistent with "
            "early material-state modulation redirecting later construction, "
            "rather than merely acting as a contemporaneous attachment bias."
        )
    else:
        sentence = (
            "The accessible-history causal difference was established partly "
            "while the material trace remained strong, but non-trivial trajectory "
            "effects continued after the trace weakened. The V2 sample is most "
            "consistent with a mixed transient-state and trajectory-redirection "
            "mechanism."
        )

    report = {
        "metadata": {
            "audit_version": "chapter27-v2-trajectory-closeout-audit-v1",
            "scientific_role": "ANALYSIS_ONLY_EXISTING_V2_SAMPLE",
            "source_seed": args.seed,
            "complete_paired_groups": len(groups),
            "initial_material_mass": M0,
            "formal_V2_primary_status_unchanged": formal_status,
        },
        "correctness_reconciliation": check,
        "per_lag": per_lag,
        "epochs": epochs,
        "decay_relative_closeout": decay,
        "material_tracking_models": tracking,
        "directional_summary": {
            "final_mean": per_lag[str(H)]["cumulative_delta_RB"]["mean"],
            "ci95_low": final_ci_low,
            "ci95_high": final_ci_high,
            "direction": direction,
            "formal_frozen_magnitude_status": formal_status,
        },
        "chapter_closeout": {
            "suggested_descriptive_mechanism": desc,
            "suggested_sentence": sentence,
            "formal_magnitude_status_remains": formal_status,
            "interpretation_boundary": [
                "This audit does not change the frozen V2 primary magnitude status.",
                "The mechanism descriptor is descriptive, not a new confirmatory hypothesis.",
                "The material state was experimentally written; this does not establish self-generated memory.",
                "Per-lag realized attachment increments are total/global diagnostics because local realized increments were not stored.",
            ],
        },
        "source_verdict": verdict,
    }

    json_path = args.audit_dir / "ch27-v2-trajectory-closeout-audit.json"
    md_path = args.audit_dir / "ch27-v2-trajectory-closeout-audit.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_csv(args.audit_dir / "ch27-v2-per-lag-closeout.csv", per_lag_csv)
    write_csv(args.audit_dir / "ch27-v2-group-lag-closeout.csv", group_rows)
    write_csv(args.audit_dir / "ch27-v2-epoch-closeout.csv", epoch_csv)

    md = [
        "# Chapter 27 V2 Trajectory / Closeout Audit",
        "",
        "## Scientific boundary",
        "",
        "Analysis only. Existing V2 sample. No new experiment.",
        "",
        f"Formal V2 primary magnitude status remains: **{formal_status}**.",
        "",
        "## Correctness reconciliation",
        "",
        "```json",
        json.dumps(check, indent=2),
        "```",
        "",
        "## Per-lag causal and material trajectory",
        "",
        "```json",
        json.dumps(per_lag, indent=2),
        "```",
        "",
        "## Epoch decomposition",
        "",
        "```json",
        json.dumps(epochs, indent=2),
        "```",
        "",
        "## Decay-relative closeout",
        "",
        "```json",
        json.dumps(decay, indent=2),
        "```",
        "",
        "## Material-tracking models",
        "",
        "```json",
        json.dumps(tracking, indent=2),
        "```",
        "",
        "## Directional summary",
        "",
        "```json",
        json.dumps(report["directional_summary"], indent=2),
        "```",
        "",
        "## Suggested Chapter 27 closeout",
        "",
        sentence,
        "",
        "The mechanism descriptor is descriptive only and does not replace "
        "the frozen V2 primary status.",
        "",
    ]
    md_path.write_text("\n".join(md), encoding="utf-8")

    print()
    print("=" * 78)
    print("CLOSEOUT AUDIT COMPLETE")
    print(f"Formal V2 status remains: {formal_status}")
    print(f"Suggested mechanism: {desc}")
    print(sentence)
    print(f"Markdown: {md_path}")
    print(f"JSON: {json_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
