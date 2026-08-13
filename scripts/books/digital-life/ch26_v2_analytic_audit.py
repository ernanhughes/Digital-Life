#!/usr/bin/env python3
"""
Digital Life — Chapter 26 V2 Analytic Audit
===========================================

PURPOSE
-------

This is an ANALYSIS-ONLY audit of Chapter 26 V2.

It does NOT:
- create a new scientific sample
- use a fresh seed
- change the frozen V2 primary verdict
- retune the SEI
- change the horizon
- change probe selection
- change any allocation arm
- create a V3

It uses the existing V2 raw outputs:

    raw-v2-arm-results.jsonl
    raw-v2-per-lag.jsonl

and optionally imports the V2 module to reconstruct exact probe geometry
descriptors that were not serialized explicitly.

The audit addresses seven questions:

1. Does dynamic expected-construction matching approximately pin E1_ring1?

   For each probe/arm compute:

       Q = E1_ring1 * F_prevent / C_target

   and compare Q against the probe's actual promoted-neighbour count.

   Candidate reference:

       E1_ring1 ≈ n_promoted * C_target / F_prevent

2. What calibration offset was required in every arm and lag?

   Report offset by arm × lag and overall arm summaries.

3. How much common-random-number pairing survived?

   Compute group-level correlation of G_T between arms, especially:

       f=.10 vs unbounded
       f=1.00 vs unbounded

4. Is unbounded E1_far structurally zero?

   Treat this as a correctness ASSERTION, not a bootstrap finding.

5. Is the immediate E1 constraint sufficiently tight that ratio-style
   amplification is numerically safe?

   Report the distribution of E1_ring1, minimum absolute denominator, and
   descriptive arm-level mean(G)/mean(E1).

   Do NOT promote mean of per-probe G/E1 unless denominators are safely bounded.

6. Does allocation arm explain additional downstream consequence after
   conditioning on immediate causal input?

   Fit a group-level ANCOVA-style model:

       G_group_probe_mean ~ E1_group_probe_mean + arm_indicator

   Primary post-hoc adjusted contrast:

       f=.10 vs unbounded

   Also fit the paired group difference model:

       ΔG_group = alpha + beta * ΔE1_group + error

   where alpha is the residual arm effect after accounting for ΔE1.

7. What should be rewritten in Chapter 26?

   Produce a compact audit verdict distinguishing:
   - exact/asserted quantities
   - induced constraints
   - measured downstream result
   - precision boundary

SCIENTIFIC BOUNDARY
-------------------

The frozen Chapter 26 V2 primary result remains:

    BOUNDED_NEAR_ZERO at ±0.15 attachments

This audit cannot upgrade that verdict.

It can only sharpen interpretation.

INPUT EXPECTATIONS
------------------

Default source directory:

    research/digital-life/
    ch26-dynamically-matched-rate-causal-amplification-v2

Expected files:

    raw-v2-arm-results.jsonl
    raw-v2-per-lag.jsonl

Optional geometry reconstruction requires the original chapter modules beside
this script:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py

OUTPUTS
-------

    ch26-v2-analytic-audit-report.json
    ch26-v2-analytic-audit-report.md
    audit-promoted-e1-constraint.csv
    audit-offsets-by-arm-lag.csv
    audit-group-arm-correlations.csv
    audit-adjusted-amplification.csv

SEED
----

Geometry reconstruction defaults to the original V2 seed:

    20260913

A different seed is blocked unless explicitly overridden for engineering only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


ORIGINAL_V2_SEED = 20260913
ORIGINAL_SEI = 0.15
ZERO_TOL = 1e-12

PRIMARY_ARM = "f=0.10"
TRUE_UNBOUNDED_ARM = "unbounded"
BOUNDARY_ARM = "f=1.00"

ARM_ORDER = [
    "f=0.10",
    "f=0.25",
    "f=0.50",
    "f=0.75",
    "f=1.00",
    "unbounded",
]


# ============================================================================
# Generic helpers
# ============================================================================

def read_jsonl(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(path)

    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [float(v) for v in values if math.isfinite(float(v))],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "n": 0,
            "mean": float("nan"),
            "sd": float("nan"),
            "se": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
        }

    rng = np.random.default_rng(seed)
    boot = np.empty(int(reps), dtype=float)

    for i in range(int(reps)):
        boot[i] = float(
            np.mean(
                rng.choice(arr, size=len(arr), replace=True)
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
    }


def corr(x: Sequence[float], y: Sequence[float]) -> float:
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)

    mask = np.isfinite(xa) & np.isfinite(ya)
    xa = xa[mask]
    ya = ya[mask]

    if len(xa) < 3:
        return float("nan")

    if np.std(xa) == 0 or np.std(ya) == 0:
        return float("nan")

    return float(np.corrcoef(xa, ya)[0, 1])


def group_mean_map(
    rows: Sequence[dict],
    arm: str,
    field: str,
) -> Dict[int, float]:
    buckets = defaultdict(list)

    for row in rows:
        if row["budget_label"] != arm:
            continue

        v = float(row[field])
        if not math.isfinite(v):
            continue

        buckets[int(row["group"])].append(v)

    return {
        g: float(np.mean(vals))
        for g, vals in buckets.items()
        if vals
    }


def paired_group_vectors(
    rows: Sequence[dict],
    arm_a: str,
    arm_b: str,
    field: str,
) -> Tuple[List[int], np.ndarray, np.ndarray]:
    a = group_mean_map(rows, arm_a, field)
    b = group_mean_map(rows, arm_b, field)

    common = sorted(set(a) & set(b))

    return (
        common,
        np.asarray([a[g] for g in common], dtype=float),
        np.asarray([b[g] for g in common], dtype=float),
    )


# ============================================================================
# Geometry reconstruction
# ============================================================================

@dataclass
class ProbeGeometry:
    group: int
    probe_index: int
    q: int
    r: int
    promoted_count: int
    fcp: int
    occupied_neighbors: int


def reconstruct_probe_geometry(
    profile_name: str,
    seed: int,
) -> Dict[Tuple[int, int], ProbeGeometry]:
    """
    Rebuild the same probes using the original V2 module, then calculate
    deterministic checkpoint-level frontier promotion count.

    For a frontier site x:

        promoted_count =
            number of empty neighbours of x that are not frontier before x
            is occupied and become frontier after x is occupied.

    For the chapter's n=1 probes:

        FCP = promoted_count - 1

    because x itself leaves the frontier when forced occupied.
    """
    import ch18_digital_crystal_persistent_material_state_v7 as ch18
    import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4
    import ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2 as v2

    profile = dict(v2.PROFILES[profile_name])

    source_profile = dict(
        v4.PROFILES[profile["source_profile"]]
    )
    source_profile["groups"] = int(profile["groups"])
    source_profile["horizon"] = v2.HORIZON

    crystal_params = ch18.CrystalParams()

    probes, _support = v2.prepare_probes(
        profile,
        source_profile,
        crystal_params,
        seed,
    )

    radius = int(source_profile["radius"])
    result = {}

    for probe in probes:
        occupied = set(probe.checkpoint.occupied)
        x = probe.cell

        frontier_before = set(
            v4.frontier_cells(
                occupied,
                radius,
            )
        )

        forced_occupied = set(occupied)
        forced_occupied.add(x)

        frontier_after = set(
            v4.frontier_cells(
                forced_occupied,
                radius,
            )
        )

        promoted = [
            cell
            for cell in frontier_after - frontier_before
            if cell != x
            and v4.relative_distance(cell, x) <= 1
        ]

        fcp = len(frontier_after) - len(frontier_before)

        n = sum(
            nb in occupied
            for nb in ch18.neighbors(x)
        )

        result[
            (int(probe.group), int(probe.probe_index))
        ] = ProbeGeometry(
            group=int(probe.group),
            probe_index=int(probe.probe_index),
            q=int(x[0]),
            r=int(x[1]),
            promoted_count=int(len(promoted)),
            fcp=int(fcp),
            occupied_neighbors=int(n),
        )

    return result


# ============================================================================
# Audit 1 — induced E1 constraint
# ============================================================================

def e1_constraint_audit(
    arm_rows: Sequence[dict],
    lag_rows: Sequence[dict],
    geometry: Dict[Tuple[int, int], ProbeGeometry],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[dict, List[dict]]:
    lag1 = {
        (
            int(row["group"]),
            int(row["probe_index"]),
            row["budget_label"],
        ): row
        for row in lag_rows
        if int(row["lag"]) == 1
    }

    detailed = []

    by_arm_delta = defaultdict(list)
    by_arm_q = defaultdict(list)
    by_arm_pred = defaultdict(list)
    by_arm_obs = defaultdict(list)

    for row in arm_rows:
        key_gp = (
            int(row["group"]),
            int(row["probe_index"]),
        )

        if key_gp not in geometry:
            continue

        arm = row["budget_label"]

        lag_key = (
            key_gp[0],
            key_gp[1],
            arm,
        )

        if lag_key not in lag1:
            continue

        g = geometry[key_gp]
        lr = lag1[lag_key]

        E1 = float(row["E1_ring1"])
        F = float(lr["prevent_frontier_size"])
        C = float(lr["target_expected_attachments"])

        if C <= 0 or F <= 0:
            continue

        Q = E1 * F / C

        predicted = (
            g.promoted_count
            * C
            / F
        )

        residual = E1 - predicted

        detailed.append({
            "group": key_gp[0],
            "probe_index": key_gp[1],
            "budget_label": arm,
            "promoted_count": g.promoted_count,
            "fcp": g.fcp,
            "occupied_neighbors": g.occupied_neighbors,
            "prevent_frontier_size": F,
            "target_expected_attachments": C,
            "E1_ring1": E1,
            "Q_E1_times_F_over_C": Q,
            "analytic_prediction_npromoted_C_over_F": predicted,
            "prediction_residual": residual,
            "Q_minus_promoted": Q - g.promoted_count,
        })

        by_arm_delta[arm].append(Q - g.promoted_count)
        by_arm_q[arm].append(Q)
        by_arm_pred[arm].append(predicted)
        by_arm_obs[arm].append(E1)

    arm_summary = {}

    for idx, arm in enumerate(ARM_ORDER):
        vals = by_arm_delta.get(arm, [])

        obs = np.asarray(by_arm_obs.get(arm, []), dtype=float)
        pred = np.asarray(by_arm_pred.get(arm, []), dtype=float)

        if len(obs) and len(pred):
            rmse = float(
                math.sqrt(
                    np.mean(
                        (obs - pred) ** 2
                    )
                )
            )
            mae = float(
                np.mean(
                    np.abs(obs - pred)
                )
            )
            r = corr(obs, pred)
        else:
            rmse = float("nan")
            mae = float("nan")
            r = float("nan")

        arm_summary[arm] = {
            "Q_minus_promoted": bootstrap_mean_ci(
                vals,
                bootstrap_reps,
                seed + idx * 50,
            ),
            "Q": bootstrap_mean_ci(
                by_arm_q.get(arm, []),
                bootstrap_reps,
                seed + idx * 50 + 1,
            ),
            "prediction_RMSE": rmse,
            "prediction_MAE": mae,
            "corr_observed_vs_analytic": r,
        }

    all_delta = [
        row["Q_minus_promoted"]
        for row in detailed
    ]

    all_residual = [
        row["prediction_residual"]
        for row in detailed
    ]

    overall = {
        "reference_equation": (
            "E1_ring1 ≈ n_promoted * C_target / F_prevent"
        ),
        "transformed_check": (
            "Q = E1_ring1 * F_prevent / C_target ≈ n_promoted"
        ),
        "overall_Q_minus_promoted": bootstrap_mean_ci(
            all_delta,
            bootstrap_reps,
            seed + 999,
        ),
        "overall_prediction_residual": bootstrap_mean_ci(
            all_residual,
            bootstrap_reps,
            seed + 1000,
        ),
        "by_arm": arm_summary,
    }

    return overall, detailed


# ============================================================================
# Audit 2 — calibration offsets
# ============================================================================

def offset_audit(
    lag_rows: Sequence[dict],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[dict, List[dict]]:
    rows_out = []
    payload = {}

    for arm_index, arm in enumerate(ARM_ORDER):
        payload[arm] = {}

        for lag in range(1, 13):
            vals = [
                float(row["offset"])
                for row in lag_rows
                if row["budget_label"] == arm
                and int(row["lag"]) == lag
            ]

            summary = bootstrap_mean_ci(
                vals,
                bootstrap_reps,
                seed + arm_index * 1000 + lag,
            )

            payload[arm][str(lag)] = summary

            rows_out.append({
                "budget_label": arm,
                "lag": lag,
                **summary,
            })

        all_vals = [
            float(row["offset"])
            for row in lag_rows
            if row["budget_label"] == arm
        ]

        payload[arm]["all_lags"] = bootstrap_mean_ci(
            all_vals,
            bootstrap_reps,
            seed + arm_index * 1000 + 500,
        )

    return payload, rows_out


# ============================================================================
# Audit 3 — CRN pairing / correlations
# ============================================================================

def pairing_audit(
    arm_rows: Sequence[dict],
) -> Tuple[dict, List[dict]]:
    comparisons = [
        (PRIMARY_ARM, TRUE_UNBOUNDED_ARM),
        (BOUNDARY_ARM, TRUE_UNBOUNDED_ARM),
        ("f=0.25", TRUE_UNBOUNDED_ARM),
        ("f=0.50", TRUE_UNBOUNDED_ARM),
        ("f=0.75", TRUE_UNBOUNDED_ARM),
    ]

    out = {}
    csv_rows = []

    for arm_a, arm_b in comparisons:
        groups, a, b = paired_group_vectors(
            arm_rows,
            arm_a,
            arm_b,
            "G_local",
        )

        delta = a - b

        r = corr(a, b)

        row = {
            "arm_a": arm_a,
            "arm_b": arm_b,
            "n_groups": int(len(groups)),
            "corr_G_local": r,
            "sd_arm_a": float(np.std(a, ddof=1))
            if len(a) > 1
            else float("nan"),
            "sd_arm_b": float(np.std(b, ddof=1))
            if len(b) > 1
            else float("nan"),
            "sd_difference": float(np.std(delta, ddof=1))
            if len(delta) > 1
            else float("nan"),
            "mean_difference": float(np.mean(delta))
            if len(delta)
            else float("nan"),
        }

        key = f"{arm_a}_vs_{arm_b}"
        out[key] = row
        csv_rows.append(row)

    return out, csv_rows


# ============================================================================
# Audit 4 — exact unbounded E1_far assertion
# ============================================================================

def unbounded_far_assertion(
    arm_rows: Sequence[dict],
) -> dict:
    vals = np.asarray(
        [
            float(row["E1_far"])
            for row in arm_rows
            if row["budget_label"] == TRUE_UNBOUNDED_ARM
        ],
        dtype=float,
    )

    max_abs = (
        float(np.max(np.abs(vals)))
        if len(vals)
        else float("nan")
    )

    passed = bool(
        len(vals)
        and max_abs <= ZERO_TOL
    )

    if not passed:
        raise RuntimeError(
            f"Unbounded E1_far assertion failed: max_abs={max_abs}"
        )

    return {
        "role": "ASSERTION_NOT_SCIENTIFIC_FINDING",
        "n_rows": int(len(vals)),
        "tolerance": ZERO_TOL,
        "max_abs_E1_far": max_abs,
        "status": "PASS",
        "statement": (
            "True unbounded evaluation must produce zero lag-1 far-field "
            "selector-mediated expected difference in this construction."
        ),
    }


# ============================================================================
# Audit 5 — denominator safety / descriptive amplification
# ============================================================================

def denominator_and_descriptive_ratio_audit(
    arm_rows: Sequence[dict],
) -> dict:
    out = {}

    for arm in ARM_ORDER:
        E1 = np.asarray(
            [
                float(row["E1_ring1"])
                for row in arm_rows
                if row["budget_label"] == arm
            ],
            dtype=float,
        )

        G = np.asarray(
            [
                float(row["G_local"])
                for row in arm_rows
                if row["budget_label"] == arm
            ],
            dtype=float,
        )

        mask = (
            np.isfinite(E1)
            & np.isfinite(G)
        )

        E1 = E1[mask]
        G = G[mask]

        safe = np.abs(E1) > 1e-6

        per_probe_ratio = (
            G[safe] / E1[safe]
            if np.any(safe)
            else np.asarray([], dtype=float)
        )

        out[arm] = {
            "n": int(len(E1)),
            "E1_mean": float(np.mean(E1))
            if len(E1)
            else float("nan"),
            "E1_sd": float(np.std(E1, ddof=1))
            if len(E1) > 1
            else float("nan"),
            "E1_min": float(np.min(E1))
            if len(E1)
            else float("nan"),
            "E1_max": float(np.max(E1))
            if len(E1)
            else float("nan"),
            "min_abs_E1": float(np.min(np.abs(E1)))
            if len(E1)
            else float("nan"),
            "fraction_abs_E1_gt_1e-3": float(
                np.mean(np.abs(E1) > 1e-3)
            )
            if len(E1)
            else float("nan"),
            "ratio_of_arm_means_G_over_E1": (
                float(np.mean(G) / np.mean(E1))
                if len(G)
                and abs(float(np.mean(E1))) > 1e-12
                else float("nan")
            ),
            "per_probe_ratio_median": (
                float(np.median(per_probe_ratio))
                if len(per_probe_ratio)
                else float("nan")
            ),
            "per_probe_ratio_IQR": (
                [
                    float(np.quantile(per_probe_ratio, 0.25)),
                    float(np.quantile(per_probe_ratio, 0.75)),
                ]
                if len(per_probe_ratio)
                else [float("nan"), float("nan")]
            ),
        }

    return out


# ============================================================================
# Audit 6 — adjusted downstream amplification
# ============================================================================

def ols_fit(
    X: np.ndarray,
    y: np.ndarray,
) -> dict:
    """
    Plain OLS with HC1 robust covariance.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    mask = (
        np.all(np.isfinite(X), axis=1)
        & np.isfinite(y)
    )

    X = X[mask]
    y = y[mask]

    n, p = X.shape

    if n <= p:
        return {
            "n": int(n),
            "coef": [float("nan")] * p,
            "se_hc1": [float("nan")] * p,
        }

    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta

    meat = np.zeros((p, p), dtype=float)

    for i in range(n):
        xi = X[i:i+1].T
        meat += (resid[i] ** 2) * (xi @ xi.T)

    hc1 = (
        n / max(1, n - p)
    ) * XtX_inv @ meat @ XtX_inv

    se = np.sqrt(
        np.maximum(
            0.0,
            np.diag(hc1),
        )
    )

    return {
        "n": int(n),
        "coef": [float(v) for v in beta],
        "se_hc1": [float(v) for v in se],
    }


def adjusted_amplification_audit(
    arm_rows: Sequence[dict],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[dict, List[dict]]:
    """
    Two complementary analyses.

    A. Group-level paired residual model:
         dG = alpha + beta*dE1 + error
       alpha = allocation-regime difference after accounting for immediate E1.

    B. Pooled two-arm group-level ANCOVA:
         G = intercept + beta*E1 + gamma*I(f=.10)
       gamma = adjusted arm effect.
    """
    groups, G_a, G_b = paired_group_vectors(
        arm_rows,
        PRIMARY_ARM,
        TRUE_UNBOUNDED_ARM,
        "G_local",
    )

    _groups_e, E_a, E_b = paired_group_vectors(
        arm_rows,
        PRIMARY_ARM,
        TRUE_UNBOUNDED_ARM,
        "E1_ring1",
    )

    if groups != _groups_e:
        raise RuntimeError(
            "Group mismatch between G and E1 paired vectors."
        )

    dG = G_a - G_b
    dE = E_a - E_b

    X_delta = np.column_stack(
        [
            np.ones(len(dE)),
            dE,
        ]
    )

    fit_delta = ols_fit(
        X_delta,
        dG,
    )

    alpha = fit_delta["coef"][0]
    alpha_se = fit_delta["se_hc1"][0]

    # Nonparametric bootstrap on groups for alpha.
    rng = np.random.default_rng(seed)
    alpha_boot = []

    if len(dG) >= 3:
        for _ in range(int(bootstrap_reps)):
            idx = rng.integers(
                0,
                len(dG),
                size=len(dG),
            )

            fit = ols_fit(
                np.column_stack(
                    [
                        np.ones(len(idx)),
                        dE[idx],
                    ]
                ),
                dG[idx],
            )

            a = fit["coef"][0]
            if math.isfinite(a):
                alpha_boot.append(a)

    alpha_ci = (
        [
            float(np.quantile(alpha_boot, 0.025)),
            float(np.quantile(alpha_boot, 0.975)),
        ]
        if alpha_boot
        else [float("nan"), float("nan")]
    )

    # Pooled group-level ANCOVA with one observation per group×arm.
    rows_pooled = []

    map_G_a = group_mean_map(
        arm_rows,
        PRIMARY_ARM,
        "G_local",
    )
    map_G_b = group_mean_map(
        arm_rows,
        TRUE_UNBOUNDED_ARM,
        "G_local",
    )

    map_E_a = group_mean_map(
        arm_rows,
        PRIMARY_ARM,
        "E1_ring1",
    )
    map_E_b = group_mean_map(
        arm_rows,
        TRUE_UNBOUNDED_ARM,
        "E1_ring1",
    )

    common = sorted(
        set(map_G_a)
        & set(map_G_b)
        & set(map_E_a)
        & set(map_E_b)
    )

    X = []
    y = []

    for g in common:
        X.append(
            [
                1.0,
                map_E_a[g],
                1.0,
            ]
        )
        y.append(map_G_a[g])

        X.append(
            [
                1.0,
                map_E_b[g],
                0.0,
            ]
        )
        y.append(map_G_b[g])

        rows_pooled.append({
            "group": g,
            "arm": PRIMARY_ARM,
            "G_local": map_G_a[g],
            "E1_ring1": map_E_a[g],
        })

        rows_pooled.append({
            "group": g,
            "arm": TRUE_UNBOUNDED_ARM,
            "G_local": map_G_b[g],
            "E1_ring1": map_E_b[g],
        })

    fit_ancova = ols_fit(
        np.asarray(X, dtype=float),
        np.asarray(y, dtype=float),
    )

    gamma = fit_ancova["coef"][2]
    gamma_se = fit_ancova["se_hc1"][2]

    result = {
        "paired_difference_adjustment": {
            "model": (
                "Delta_G_group = alpha + beta * Delta_E1_group"
            ),
            "n_groups": int(len(dG)),
            "alpha_adjusted_arm_effect": float(alpha),
            "alpha_HC1_SE": float(alpha_se),
            "alpha_bootstrap_CI95": alpha_ci,
            "beta_on_Delta_E1": float(
                fit_delta["coef"][1]
            ),
            "corr_DeltaG_DeltaE1": corr(
                dG,
                dE,
            ),
            "raw_DeltaG_mean": float(
                np.mean(dG)
            ),
            "raw_DeltaE1_mean": float(
                np.mean(dE)
            ),
        },
        "pooled_group_ancova": {
            "model": (
                "G_group = intercept + beta*E1_group + "
                "gamma*I(f=.10)"
            ),
            "n_observations": int(
                fit_ancova["n"]
            ),
            "beta_E1": float(
                fit_ancova["coef"][1]
            ),
            "gamma_adjusted_f0p10_effect": float(gamma),
            "gamma_HC1_SE": float(gamma_se),
        },
    }

    return result, rows_pooled


# ============================================================================
# Audit verdict
# ============================================================================

def build_verdict(
    e1_constraint: dict,
    offsets: dict,
    pairing: dict,
    assertion: dict,
    denominator: dict,
    adjusted: dict,
) -> dict:
    primary_adjusted = adjusted[
        "paired_difference_adjustment"
    ]

    return {
        "frozen_V2_primary_status_unchanged": True,
        "frozen_V2_primary_SEI": ORIGINAL_SEI,
        "interpretive_updates": [
            (
                "Dynamic construction-rate matching did not merely hold "
                "background growth constant; in the n=1 probe regime it also "
                "strongly constrained the immediate expected causal input."
            ),
            (
                "The correct Chapter 26 downstream question is therefore "
                "whether allocation regime adds amplification beyond a "
                "matched/approximately pinned immediate causal input."
            ),
            (
                "Calibration changes both evaluation breadth and per-candidate "
                "attachment probability. The manipulation is not 'same rule, "
                "different allocation' in the narrow sense."
            ),
            (
                "f=1.00 is a PREVENT-exhaustive / FORCE-near-saturation "
                "boundary arm, not true unbounded evaluation."
            ),
            (
                "True-unbounded E1_far=0 is a correctness assertion, not a "
                "bootstrap result."
            ),
            (
                "The bounded-near-zero claim is specific to the frozen ±0.15 "
                "scale; V2 was not powered to establish a ±0.10 equivalence."
            ),
        ],
        "e1_constraint_reference": e1_constraint[
            "reference_equation"
        ],
        "adjusted_primary_posthoc": {
            "alpha_adjusted_arm_effect": primary_adjusted[
                "alpha_adjusted_arm_effect"
            ],
            "alpha_bootstrap_CI95": primary_adjusted[
                "alpha_bootstrap_CI95"
            ],
            "role": (
                "POST-HOC INTERPRETIVE ANALYSIS; does not replace frozen primary"
            ),
        },
        "assertion_status": assertion,
        "recommended_chapter_claim": (
            "After dynamically matching background construction—and thereby "
            "strongly constraining the immediate expected causal input for "
            "these n=1 probes—strong candidate subsampling did not produce an "
            "additional mean twelve-step causal consequence larger than the "
            "frozen ±0.15 attachment scale relative to true exhaustive "
            "evaluation."
        ),
        "recommended_distinction": (
            "CAUSAL REDISTRIBUTION != ADDITIONAL DOWNSTREAM AMPLIFICATION"
        ),
    }


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source-report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch26-dynamically-matched-rate-causal-amplification-v2"
        ),
    )

    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch26-v2-analytic-audit"
        ),
    )

    parser.add_argument(
        "--profile",
        default="full",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=ORIGINAL_V2_SEED,
    )

    parser.add_argument(
        "--allow-different-seed",
        action="store_true",
    )

    parser.add_argument(
        "--bootstrap-reps",
        type=int,
        default=7000,
    )

    parser.add_argument(
        "--skip-geometry-reconstruction",
        action="store_true",
        help=(
            "Skip Q≈n_promoted audit if original modules are unavailable."
        ),
    )

    args = parser.parse_args()

    if (
        args.seed != ORIGINAL_V2_SEED
        and not args.allow_different_seed
    ):
        raise RuntimeError(
            "This audit must use the original V2 seed 20260913. "
            "A different seed would be a new diagnostic sample, not the "
            "Chapter 26 V2 audit."
        )

    args.audit_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    arm_path = (
        args.source_report_dir
        / "raw-v2-arm-results.jsonl"
    )

    lag_path = (
        args.source_report_dir
        / "raw-v2-per-lag.jsonl"
    )

    arm_rows = read_jsonl(arm_path)
    lag_rows = read_jsonl(lag_path)

    print("=" * 78)
    print("CHAPTER 26 V2 ANALYTIC AUDIT")
    print(f"Arm rows: {len(arm_rows)}")
    print(f"Lag rows: {len(lag_rows)}")
    print(f"Seed: {args.seed}")
    print("=" * 78)

    # 1. E1 constraint / promoted count.
    if not args.skip_geometry_reconstruction:
        geometry = reconstruct_probe_geometry(
            args.profile,
            args.seed,
        )

        e1_constraint, e1_rows = e1_constraint_audit(
            arm_rows,
            lag_rows,
            geometry,
            args.bootstrap_reps,
            args.seed + 1000,
        )

        write_csv(
            args.audit_dir
            / "audit-promoted-e1-constraint.csv",
            e1_rows,
        )
    else:
        e1_constraint = {
            "status": "SKIPPED_GEOMETRY_RECONSTRUCTION"
        }
        e1_rows = []

    # 2. Offsets.
    offsets, offset_rows = offset_audit(
        lag_rows,
        args.bootstrap_reps,
        args.seed + 2000,
    )

    write_csv(
        args.audit_dir
        / "audit-offsets-by-arm-lag.csv",
        offset_rows,
    )

    # 3. CRN pairing.
    pairing, pairing_rows = pairing_audit(
        arm_rows
    )

    write_csv(
        args.audit_dir
        / "audit-group-arm-correlations.csv",
        pairing_rows,
    )

    # 4. Structural assertion.
    assertion = unbounded_far_assertion(
        arm_rows
    )

    # 5. Denominator safety.
    denominator = (
        denominator_and_descriptive_ratio_audit(
            arm_rows
        )
    )

    # 6. Adjusted amplification.
    adjusted, adjusted_rows = (
        adjusted_amplification_audit(
            arm_rows,
            args.bootstrap_reps,
            args.seed + 3000,
        )
    )

    write_csv(
        args.audit_dir
        / "audit-adjusted-amplification.csv",
        adjusted_rows,
    )

    # 7. Verdict.
    verdict = build_verdict(
        e1_constraint,
        offsets,
        pairing,
        assertion,
        denominator,
        adjusted,
    )

    report = {
        "metadata": {
            "audit_version": (
                "chapter26-v2-analytic-audit-v1"
            ),
            "audited_experiment": (
                "digital-crystal-dynamically-matched-rate-"
                "causal-amplification-v2"
            ),
            "seed": int(args.seed),
            "same_original_seed": bool(
                args.seed
                == ORIGINAL_V2_SEED
            ),
            "scientific_role": (
                "ANALYSIS_ONLY_NO_NEW_EXPERIMENT"
            ),
            "frozen_primary_SEI": ORIGINAL_SEI,
        },
        "audit_1_E1_constraint": e1_constraint,
        "audit_2_calibration_offsets": offsets,
        "audit_3_pairing_correlations": pairing,
        "audit_4_unbounded_far_assertion": assertion,
        "audit_5_denominator_and_descriptive_ratio": denominator,
        "audit_6_adjusted_amplification": adjusted,
        "audit_7_interpretive_verdict": verdict,
    }

    json_path = (
        args.audit_dir
        / "ch26-v2-analytic-audit-report.json"
    )

    json_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    md_path = (
        args.audit_dir
        / "ch26-v2-analytic-audit-report.md"
    )

    md = [
        "# Chapter 26 V2 Analytic Audit",
        "",
        "## Scientific boundary",
        "",
        "This is an analysis-only audit of the original V2 sample.",
        "It does not replace the frozen Chapter 26 V2 primary result.",
        "",
        "## 1. Immediate E1 constraint",
        "",
        "```json",
        json.dumps(
            e1_constraint,
            indent=2,
        ),
        "```",
        "",
        "## 2. Calibration offsets",
        "",
        "```json",
        json.dumps(
            offsets,
            indent=2,
        ),
        "```",
        "",
        "## 3. Common-random-number pairing",
        "",
        "```json",
        json.dumps(
            pairing,
            indent=2,
        ),
        "```",
        "",
        "## 4. Unbounded far-field assertion",
        "",
        "```json",
        json.dumps(
            assertion,
            indent=2,
        ),
        "```",
        "",
        "## 5. Denominator safety / descriptive ratios",
        "",
        "```json",
        json.dumps(
            denominator,
            indent=2,
        ),
        "```",
        "",
        "## 6. Adjusted downstream amplification",
        "",
        "```json",
        json.dumps(
            adjusted,
            indent=2,
        ),
        "```",
        "",
        "## 7. Interpretive verdict",
        "",
        "```json",
        json.dumps(
            verdict,
            indent=2,
        ),
        "```",
        "",
    ]

    md_path.write_text(
        "\n".join(md),
        encoding="utf-8",
    )

    print()
    print("=" * 78)
    print("AUDIT COMPLETE")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
