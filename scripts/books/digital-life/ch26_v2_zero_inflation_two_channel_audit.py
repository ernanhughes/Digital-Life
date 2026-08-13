#!/usr/bin/env python3
"""
Digital Life — Chapter 26 V2 Mechanism Audit
Zero-Inflation + Two-Channel Ring-1 Causal Accounting
=====================================================

ROLE
----

ANALYSIS-ONLY AUDIT.

This script does NOT:
- create a new scientific sample
- change the Chapter 26 V2 seed
- change the frozen primary contrast
- change the frozen +/-0.15 SEI
- create a Chapter 26 V3
- rescue or replace the V2 result

It tests two mechanistic questions suggested by the V2 audit.

AUDIT A — ZERO-INFLATION ACCOUNTING
-----------------------------------

For an n=1 probe, FORCE and PREVENT differ initially only at x.

If x is removed by the intervention-step loss operation, the post-intervention
FORCE and PREVENT states become identical.

Then, under common future randomness:

    E1_ring1 = 0
    G_T = 0

structurally.

If x survives, E1_ring1 can still be zero under partial evaluation when none
of the affected ring-1 candidates are selected.

For each probe and arm, compute an exact finite-population approximation to:

    P(E1 structurally active)

using:

    P(x survives) = 1 - loss_rate

and the without-replacement probability that at least one affected ring-1
candidate is selected:

    P(any affected selected)
      = 1 - C(F-k, B) / C(F, B)

where:
    F = relevant frontier size
    k = count of affected eligible ring-1 frontier candidates
    B = finite budget

For unbounded evaluation:
    P(any affected selected) = 1 when k > 0.

Compare predicted arm-level active fractions against observed:

    |E1_ring1| > epsilon

Also reconstruct the realized intervention-step x-survival indicator from the
same keyed loss mechanism where possible.

IMPORTANT:
The hypergeometric expression is an exact combinatorial reference only if the
selector is uniform over frontier candidates. If the implementation uses a
deterministic keyed ranking that is distributionally uniform but not sampled
fresh in this audit, treat the prediction as a parameter-free protocol
expectation, not a per-probe realized identity.

AUDIT B — EXACT TWO-CHANNEL RING-1 ACCOUNTING
---------------------------------------------

Condition on probes where x survives the intervention step.

For each arm at lag 1, decompose exact E1_ring1 into:

1. PROMOTED / FORCE-ONLY CHANNEL

    sum over ring-1 cells selected only in FORCE:
        +p_force(cell)

2. PREVENT-ONLY SELECTOR CHANNEL

    sum over ring-1 cells selected only in PREVENT:
        -p_prevent(cell)

3. SHARED PROBABILITY-SHIFT CHANNEL

    sum over ring-1 cells selected in both branches:
        p_force(cell) - p_prevent(cell)

Then verify the accounting identity:

    E1_ring1
      =
      promoted_force_only
      +
      prevent_only_selector
      +
      shared_probability_shift

up to floating tolerance.

This exact decomposition is preferable to a regression when the raw state can
be reconstructed.

SECONDARY COMPRESSED MODEL
--------------------------

For interpretability, also fit within each arm on surviving probes:

    E1_ring1
      ~ a * n_promoted_scaled
      + b * n_shared_scaled

where:

    n_promoted_scaled
      = n_promoted * C_target / F_prevent

    n_shared_scaled
      = (5 - n_promoted) * C_target / F_prevent

This is a compressed descriptive approximation.

The coefficients are NOT automatically interpreted as literal probabilities,
because candidate-specific probabilities and selector substitutions are
heterogeneous.

AUDIT C — STRUCTURAL NULL CONTRIBUTION TO G_T
---------------------------------------------

Report:

    fraction x lost
    fraction E1 exactly/approximately zero
    fraction G_T exactly zero

and compare:

    P(x lost) ~= loss_rate

Do NOT remove x-lost probes from the frozen V2 primary result.

This audit only quantifies how much structural-null mass the original estimator
contained.

For future experiments:
    prefer guaranteeing intervention survival by design
rather than post-hoc survivor conditioning.

ASSERTION RULE
--------------

Quantities forced by code structure are assertions.

This audit therefore ASSERTS:

    exact channel sum == E1_ring1

and, for unbounded evaluation:

    E1_far == 0

It does not bootstrap those identities.

INPUTS
------

Expected source directory:

    research/digital-life/
    ch26-dynamically-matched-rate-causal-amplification-v2

Expected raw files:

    raw-v2-arm-results.jsonl
    raw-v2-per-lag.jsonl

Required modules beside this script:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py

SEED
----

Original V2 seed only:

    20260913

OUTPUTS
-------

    ch26-v2-mechanism-audit-report.json
    ch26-v2-mechanism-audit-report.md

    audit-zero-inflation-by-arm.csv
    audit-ring1-channel-accounting.csv
    audit-two-channel-regression.csv
    audit-structural-null-summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import numpy as np

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21
import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4
import ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2 as v2


Cell = Tuple[int, int]

ORIGINAL_V2_SEED = 20260913
ZERO_EPS = 1e-3
ASSERT_TOL = 1e-12
LOSS_RATE = 0.08

ARM_ORDER = [
    "f=0.10",
    "f=0.25",
    "f=0.50",
    "f=0.75",
    "f=1.00",
    "unbounded",
]


# ============================================================================
# IO / stats
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
        writer.writerows(rows)


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            float(v)
            for v in values
            if math.isfinite(float(v))
        ],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "n": 0,
            "mean": float("nan"),
            "sd": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
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

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": (
            float(np.std(arr, ddof=1))
            if len(arr) > 1
            else 0.0
        ),
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
    }


def comb_ratio_no_selected(
    F: int,
    k: int,
    B: int,
) -> float:
    """
    C(F-k, B) / C(F, B), calculated stably as a product.
    """
    F = int(F)
    k = int(k)
    B = int(B)

    if k <= 0:
        return 1.0

    if B <= 0:
        return 1.0

    if B > F:
        B = F

    if B > F - k:
        return 0.0

    # Product representation:
    # C(F-k,B)/C(F,B) = Π_{i=0}^{B-1} (F-k-i)/(F-i)
    logp = 0.0

    for i in range(B):
        num = F - k - i
        den = F - i

        if num <= 0:
            return 0.0

        logp += math.log(num) - math.log(den)

    return float(math.exp(logp))


# ============================================================================
# Probe reconstruction
# ============================================================================

@dataclass
class ProbeRecord:
    group: int
    probe_index: int
    cell: Cell
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray
    n_promoted: int
    n_shared_empty: int
    occupied_neighbors: int


def clone_state(
    state: ch18.MaterialCrystalState,
) -> ch18.MaterialCrystalState:
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


def reconstruct_probes(
    profile_name: str,
    seed: int,
) -> Dict[Tuple[int, int], ProbeRecord]:
    profile = dict(v2.PROFILES[profile_name])

    source_profile = dict(
        v4.PROFILES[
            profile["source_profile"]
        ]
    )
    source_profile["groups"] = int(
        profile["groups"]
    )
    source_profile["horizon"] = v2.HORIZON

    crystal_params = ch18.CrystalParams()

    probes, _support = v2.prepare_probes(
        profile,
        source_profile,
        crystal_params,
        seed,
    )

    radius = int(
        source_profile["radius"]
    )

    out = {}

    for probe in probes:
        occupied = set(
            probe.checkpoint.occupied
        )
        x = probe.cell

        frontier_before = set(
            v4.frontier_cells(
                occupied,
                radius,
            )
        )

        forced = set(occupied)
        forced.add(x)

        frontier_after = set(
            v4.frontier_cells(
                forced,
                radius,
            )
        )

        n_promoted = 0
        n_shared_empty = 0

        for nb in ch18.neighbors(x):
            if nb in occupied:
                continue

            in_before = nb in frontier_before
            in_after = nb in frontier_after

            if (
                not in_before
                and in_after
            ):
                n_promoted += 1
            elif (
                in_before
                and in_after
            ):
                n_shared_empty += 1

        occupied_neighbors = sum(
            nb in occupied
            for nb in ch18.neighbors(x)
        )

        out[
            (
                int(probe.group),
                int(probe.probe_index),
            )
        ] = ProbeRecord(
            group=int(probe.group),
            probe_index=int(
                probe.probe_index
            ),
            cell=x,
            checkpoint=probe.checkpoint,
            future_env=probe.future_env,
            n_promoted=int(n_promoted),
            n_shared_empty=int(
                n_shared_empty
            ),
            occupied_neighbors=int(
                occupied_neighbors
            ),
        )

    return out


# ============================================================================
# Common intervention reconstruction
# ============================================================================

@dataclass
class PreparedProbe:
    probe: ProbeRecord
    force_state: ch18.MaterialCrystalState
    prevent_state: ch18.MaterialCrystalState
    x_survived: bool


def prepare_common_intervention(
    probe: ProbeRecord,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> PreparedProbe:
    radius = int(
        source_profile["radius"]
    )

    loss_rate = float(
        source_profile["loss_rate"]
    )

    x = probe.cell

    force_grown, _, force_selected, _ = (
        v4.growth_step(
            probe.checkpoint,
            float(probe.future_env[0]),
            radius,
            crystal_params,
            v2.INTERVENTION_BUDGET,
            force_cell=x,
        )
    )

    prevent_grown, _, prevent_selected, _ = (
        v4.growth_step(
            probe.checkpoint,
            float(probe.future_env[0]),
            radius,
            crystal_params,
            v2.INTERVENTION_BUDGET,
            prevent_cell=x,
        )
    )

    if force_selected != prevent_selected:
        raise RuntimeError(
            "Common intervention selected sets diverged before FORCE/PREVENT."
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    x_survived = bool(
        x in force_state.occupied
    )

    if not x_survived:
        # Structural check: if x was the only intervention difference and is
        # removed, states should collapse back together.
        if (
            set(force_state.occupied)
            != set(prevent_state.occupied)
        ):
            raise RuntimeError(
                "x lost but FORCE/PREVENT occupancy states did not collapse."
            )

    return PreparedProbe(
        probe=probe,
        force_state=force_state,
        prevent_state=prevent_state,
        x_survived=x_survived,
    )


# ============================================================================
# Dynamic lag-1 calibration reconstruction
# ============================================================================

@dataclass
class ArmLag1State:
    budget_label: str
    fraction: float | None
    budget: int | None
    offset: float
    target: float
    force_frontier: List[Cell]
    prevent_frontier: List[Cell]
    force_selected: List[Cell]
    prevent_selected: List[Cell]


def build_reference_target_lag1(
    prepared: PreparedProbe,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> float:
    state = clone_state(
        prepared.prevent_state
    )

    radius = int(
        source_profile["radius"]
    )

    input_value = float(
        prepared.probe.future_env[1]
    )

    frontier = v4.frontier_cells(
        set(state.occupied),
        radius,
    )

    budget = v2.budget_from_fraction(
        len(frontier),
        v2.REFERENCE_FRACTION,
    )

    selected = v2.select_candidates(
        frontier,
        state,
        budget,
    )

    return float(
        v2.expected_selected_attachments(
            state,
            input_value,
            selected,
            crystal_params,
            0.0,
        )
    )


def build_arm_lag1_state(
    prepared: PreparedProbe,
    arm: str,
    fraction: float | None,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    target: float,
) -> ArmLag1State:
    radius = int(
        source_profile["radius"]
    )

    input_value = float(
        prepared.probe.future_env[1]
    )

    force_frontier = v4.frontier_cells(
        set(
            prepared.force_state.occupied
        ),
        radius,
    )

    prevent_frontier = v4.frontier_cells(
        set(
            prepared.prevent_state.occupied
        ),
        radius,
    )

    if fraction is None:
        budget = None
    else:
        budget = v2.budget_from_fraction(
            len(prevent_frontier),
            fraction,
        )

    prevent_selected = v2.select_candidates(
        prevent_frontier,
        prepared.prevent_state,
        budget,
    )

    (
        offset,
        achieved,
        solved,
    ) = v2.solve_offset(
        prepared.prevent_state,
        input_value,
        prevent_selected,
        crystal_params,
        target,
    )

    if not solved:
        raise RuntimeError(
            f"Could not solve lag-1 offset for {arm}."
        )

    rel_err = (
        abs(
            achieved - target
        )
        / max(
            target,
            1e-12,
        )
    )

    if rel_err > v2.MATCH_TOLERANCE:
        raise RuntimeError(
            f"Lag-1 matching failed for {arm}: {rel_err}"
        )

    force_selected = v2.select_candidates(
        force_frontier,
        prepared.force_state,
        budget,
    )

    return ArmLag1State(
        budget_label=arm,
        fraction=fraction,
        budget=budget,
        offset=float(offset),
        target=float(target),
        force_frontier=force_frontier,
        prevent_frontier=prevent_frontier,
        force_selected=force_selected,
        prevent_selected=prevent_selected,
    )


# ============================================================================
# Exact ring-1 channel accounting
# ============================================================================

@dataclass
class ChannelRow:
    group: int
    probe_index: int
    budget_label: str
    x_survived: bool
    n_promoted: int
    n_shared_empty: int

    target: float
    prevent_frontier_size: int
    force_frontier_size: int
    budget: int | None
    offset: float

    E1_ring1_exact: float

    force_only_ring1: float
    prevent_only_ring1: float
    shared_probability_shift_ring1: float
    channel_sum: float
    accounting_error: float

    ring1_force_only_count: int
    ring1_prevent_only_count: int
    ring1_shared_count: int

    affected_frontier_count_for_zero_model: int


def exact_ring1_channels(
    prepared: PreparedProbe,
    arm_state: ArmLag1State,
    crystal_params: ch18.CrystalParams,
) -> ChannelRow:
    probe = prepared.probe
    x = probe.cell

    input_value = float(
        probe.future_env[1]
    )

    sf = set(
        arm_state.force_selected
    )

    sp = set(
        arm_state.prevent_selected
    )

    force_occ = set(
        prepared.force_state.occupied
    )

    prevent_occ = set(
        prepared.prevent_state.occupied
    )

    force_only = 0.0
    prevent_only = 0.0
    shared_shift = 0.0

    force_only_count = 0
    prevent_only_count = 0
    shared_count = 0

    for cell in sf | sp:
        if cell == x:
            continue

        d = v4.relative_distance(
            cell,
            x,
        )

        if d > 1:
            continue

        if cell in sf and cell not in sp:
            pf = v2.calibrated_probability(
                cell,
                force_occ,
                input_value,
                crystal_params,
                arm_state.offset,
            )

            force_only += pf
            force_only_count += 1

        elif cell in sp and cell not in sf:
            pp = v2.calibrated_probability(
                cell,
                prevent_occ,
                input_value,
                crystal_params,
                arm_state.offset,
            )

            prevent_only -= pp
            prevent_only_count += 1

        else:
            pf = v2.calibrated_probability(
                cell,
                force_occ,
                input_value,
                crystal_params,
                arm_state.offset,
            )

            pp = v2.calibrated_probability(
                cell,
                prevent_occ,
                input_value,
                crystal_params,
                arm_state.offset,
            )

            shared_shift += (
                pf - pp
            )
            shared_count += 1

    exact = (
        force_only
        + prevent_only
        + shared_shift
    )

    # The caller compares this direct selected-set accounting against the
    # serialized raw E1_ring1 and asserts exact agreement.

    # k for zero-inflation model:
    # number of ring-1 cells whose evaluation can reveal FORCE/PREVENT
    # difference. Use union of eligible ring1 frontier candidates.
    affected = set()

    for cell in (
        set(arm_state.force_frontier)
        | set(arm_state.prevent_frontier)
    ):
        if (
            cell != x
            and v4.relative_distance(
                cell,
                x,
            )
            <= 1
        ):
            affected.add(cell)

    return ChannelRow(
        group=int(probe.group),
        probe_index=int(
            probe.probe_index
        ),
        budget_label=(
            arm_state.budget_label
        ),
        x_survived=bool(
            prepared.x_survived
        ),
        n_promoted=int(
            probe.n_promoted
        ),
        n_shared_empty=int(
            probe.n_shared_empty
        ),
        target=float(
            arm_state.target
        ),
        prevent_frontier_size=int(
            len(
                arm_state.prevent_frontier
            )
        ),
        force_frontier_size=int(
            len(
                arm_state.force_frontier
            )
        ),
        budget=(
            None
            if arm_state.budget is None
            else int(
                arm_state.budget
            )
        ),
        offset=float(
            arm_state.offset
        ),
        E1_ring1_exact=float(
            exact
        ),
        force_only_ring1=float(
            force_only
        ),
        prevent_only_ring1=float(
            prevent_only
        ),
        shared_probability_shift_ring1=float(
            shared_shift
        ),
        channel_sum=float(
            exact
        ),
        accounting_error=0.0,
        ring1_force_only_count=int(
            force_only_count
        ),
        ring1_prevent_only_count=int(
            prevent_only_count
        ),
        ring1_shared_count=int(
            shared_count
        ),
        affected_frontier_count_for_zero_model=int(
            len(affected)
        ),
    )


# ============================================================================
# Fix exact channel function radius-independent mistake by direct raw comparison
# ============================================================================

# exact_ring1_channels intentionally computes directly from the selected sets.
# The audit later compares E1_ring1_exact against serialized raw E1_ring1 and
# ASSERTS equality. No call to v2.exact_expectation_difference is needed.


# ============================================================================
# Zero inflation
# ============================================================================

def zero_activity_probability(
    x_survival_probability: float,
    F: int,
    k: int,
    B: int | None,
) -> float:
    if k <= 0:
        return 0.0

    if B is None or B >= F:
        p_any = 1.0
    else:
        p_none = comb_ratio_no_selected(
            F,
            k,
            B,
        )
        p_any = 1.0 - p_none

    return float(
        x_survival_probability
        * p_any
    )


# ============================================================================
# Regression
# ============================================================================

def ols_no_intercept(
    X: np.ndarray,
    y: np.ndarray,
) -> dict:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    mask = (
        np.all(
            np.isfinite(X),
            axis=1,
        )
        & np.isfinite(y)
    )

    X = X[mask]
    y = y[mask]

    if len(y) <= X.shape[1]:
        return {
            "n": int(len(y)),
            "coef": [],
            "r2": float("nan"),
            "rmse": float("nan"),
        }

    beta = (
        np.linalg.pinv(
            X.T @ X
        )
        @ X.T
        @ y
    )

    pred = X @ beta
    resid = y - pred

    sse = float(
        np.sum(
            resid ** 2
        )
    )

    sst0 = float(
        np.sum(
            y ** 2
        )
    )

    return {
        "n": int(len(y)),
        "coef": [
            float(v)
            for v in beta
        ],
        "r2_through_origin": (
            1.0
            - sse / sst0
            if sst0 > 0
            else float("nan")
        ),
        "rmse": float(
            math.sqrt(
                np.mean(
                    resid ** 2
                )
            )
        ),
        "mae": float(
            np.mean(
                np.abs(resid)
            )
        ),
    }


def compressed_two_channel_regression(
    channel_rows: Sequence[dict],
) -> Tuple[dict, List[dict]]:
    results = {}
    csv_rows = []

    for arm in ARM_ORDER:
        rows = [
            row
            for row in channel_rows
            if row["budget_label"] == arm
            and bool(row["x_survived"])
        ]

        X = []
        y = []

        for row in rows:
            F = float(
                row[
                    "prevent_frontier_size"
                ]
            )
            C = float(
                row["target"]
            )

            if F <= 0:
                continue

            scale = C / F

            X.append(
                [
                    float(
                        row["n_promoted"]
                    )
                    * scale,
                    float(
                        row["n_shared_empty"]
                    )
                    * scale,
                ]
            )

            y.append(
                float(
                    row[
                        "E1_ring1_exact"
                    ]
                )
            )

        fit = ols_no_intercept(
            np.asarray(
                X,
                dtype=float,
            ),
            np.asarray(
                y,
                dtype=float,
            ),
        )

        if fit["coef"]:
            a = fit["coef"][0]
            b = fit["coef"][1]
        else:
            a = float("nan")
            b = float("nan")

        payload = {
            "model": (
                "E1 ~ a*(n_promoted*C/F) "
                "+ b*(n_shared_empty*C/F)"
            ),
            "conditioned_on_x_survival": True,
            "coefficient_a_promotion_proxy": a,
            "coefficient_b_shared_shift_proxy": b,
            **fit,
        }

        results[arm] = payload

        csv_rows.append({
            "budget_label": arm,
            **payload,
        })

    return results, csv_rows


# ============================================================================
# Main audit runner
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
            "ch26-v2-mechanism-audit"
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

    args = parser.parse_args()

    if (
        args.seed != ORIGINAL_V2_SEED
        and not args.allow_different_seed
    ):
        raise RuntimeError(
            "This is a same-sample Chapter 26 V2 audit. "
            "Use seed 20260913."
        )

    args.audit_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    arm_rows = read_jsonl(
        args.source_report_dir
        / "raw-v2-arm-results.jsonl"
    )

    lag_rows = read_jsonl(
        args.source_report_dir
        / "raw-v2-per-lag.jsonl"
    )

    raw_arm_lookup = {
        (
            int(row["group"]),
            int(row["probe_index"]),
            row["budget_label"],
        ): row
        for row in arm_rows
    }

    print("=" * 78)
    print("CHAPTER 26 V2 MECHANISM AUDIT")
    print(f"arm rows: {len(arm_rows)}")
    print(f"lag rows: {len(lag_rows)}")
    print("=" * 78)

    profile = dict(
        v2.PROFILES[
            args.profile
        ]
    )

    source_profile = dict(
        v4.PROFILES[
            profile["source_profile"]
        ]
    )
    source_profile[
        "groups"
    ] = int(
        profile["groups"]
    )
    source_profile[
        "horizon"
    ] = v2.HORIZON

    crystal_params = (
        ch18.CrystalParams()
    )

    probes = reconstruct_probes(
        args.profile,
        args.seed,
    )

    channel_rows = []

    arm_fraction = {
        "f=0.10": 0.10,
        "f=0.25": 0.25,
        "f=0.50": 0.50,
        "f=0.75": 0.75,
        "f=1.00": 1.00,
        "unbounded": None,
    }

    survival_flags = {}

    for key, probe in probes.items():
        prepared = prepare_common_intervention(
            probe,
            source_profile,
            crystal_params,
        )

        survival_flags[key] = bool(
            prepared.x_survived
        )

        target = build_reference_target_lag1(
            prepared,
            source_profile,
            crystal_params,
        )

        for arm in ARM_ORDER:
            state = build_arm_lag1_state(
                prepared,
                arm,
                arm_fraction[arm],
                source_profile,
                crystal_params,
                target,
            )

            row = exact_ring1_channels(
                prepared,
                state,
                crystal_params,
            )

            raw_key = (
                key[0],
                key[1],
                arm,
            )

            if raw_key not in raw_arm_lookup:
                raise RuntimeError(
                    f"Missing raw arm row for {raw_key}"
                )

            raw_E1 = float(
                raw_arm_lookup[
                    raw_key
                ][
                    "E1_ring1"
                ]
            )

            error = (
                row.E1_ring1_exact
                - raw_E1
            )

            if abs(error) > ASSERT_TOL:
                raise RuntimeError(
                    f"Ring1 channel accounting mismatch "
                    f"{raw_key}: {error}"
                )

            d = asdict(row)
            d[
                "raw_E1_ring1"
            ] = raw_E1
            d[
                "accounting_error"
            ] = float(
                error
            )

            channel_rows.append(d)

    write_csv(
        args.audit_dir
        / "audit-ring1-channel-accounting.csv",
        channel_rows,
    )

    # ------------------------------------------------------------------------
    # Audit A: zero inflation
    # ------------------------------------------------------------------------

    zero_rows = []
    zero_summary = {}

    for arm_index, arm in enumerate(
        ARM_ORDER
    ):
        rows = [
            row
            for row in channel_rows
            if row["budget_label"] == arm
        ]

        predicted = []
        observed_active = []
        realized_survival = []
        observed_G_nonzero = []

        for row in rows:
            F = int(
                row[
                    "prevent_frontier_size"
                ]
            )

            k = int(
                row[
                    "affected_frontier_count_for_zero_model"
                ]
            )

            B = row["budget"]

            p_active = (
                zero_activity_probability(
                    1.0 - LOSS_RATE,
                    F,
                    k,
                    (
                        None
                        if B is None
                        else int(B)
                    ),
                )
            )

            raw_key = (
                int(row["group"]),
                int(
                    row["probe_index"]
                ),
                arm,
            )

            raw = raw_arm_lookup[
                raw_key
            ]

            active = int(
                abs(
                    float(
                        raw["E1_ring1"]
                    )
                )
                > ZERO_EPS
            )

            survived = int(
                bool(
                    row["x_survived"]
                )
            )

            g_nonzero = int(
                abs(
                    float(
                        raw["G_local"]
                    )
                )
                > 0.0
            )

            predicted.append(
                p_active
            )
            observed_active.append(
                active
            )
            realized_survival.append(
                survived
            )
            observed_G_nonzero.append(
                g_nonzero
            )

        predicted_mean = (
            float(
                np.mean(predicted)
            )
            if predicted
            else float("nan")
        )

        observed_mean = (
            float(
                np.mean(
                    observed_active
                )
            )
            if observed_active
            else float("nan")
        )

        survival_mean = (
            float(
                np.mean(
                    realized_survival
                )
            )
            if realized_survival
            else float("nan")
        )

        G_nonzero_mean = (
            float(
                np.mean(
                    observed_G_nonzero
                )
            )
            if observed_G_nonzero
            else float("nan")
        )

        row_out = {
            "budget_label": arm,
            "predicted_active_fraction": (
                predicted_mean
            ),
            "observed_abs_E1_gt_epsilon_fraction": (
                observed_mean
            ),
            "observed_minus_predicted": (
                observed_mean
                - predicted_mean
            ),
            "realized_x_survival_fraction": (
                survival_mean
            ),
            "expected_x_survival_fraction": (
                1.0 - LOSS_RATE
            ),
            "G_nonzero_fraction": (
                G_nonzero_mean
            ),
            "epsilon": ZERO_EPS,
        }

        zero_rows.append(
            row_out
        )

        zero_summary[arm] = (
            row_out
        )

    write_csv(
        args.audit_dir
        / "audit-zero-inflation-by-arm.csv",
        zero_rows,
    )

    # ------------------------------------------------------------------------
    # Audit B: exact two-channel summaries
    # ------------------------------------------------------------------------

    channel_summary = {}

    for arm_index, arm in enumerate(
        ARM_ORDER
    ):
        rows = [
            row
            for row in channel_rows
            if (
                row["budget_label"] == arm
                and bool(
                    row["x_survived"]
                )
            )
        ]

        channel_summary[arm] = {
            "n_surviving_probes": int(
                len(rows)
            ),
            "force_only_ring1": (
                bootstrap_mean_ci(
                    [
                        r[
                            "force_only_ring1"
                        ]
                        for r in rows
                    ],
                    args.bootstrap_reps,
                    args.seed
                    + arm_index * 100
                    + 1,
                )
            ),
            "prevent_only_ring1": (
                bootstrap_mean_ci(
                    [
                        r[
                            "prevent_only_ring1"
                        ]
                        for r in rows
                    ],
                    args.bootstrap_reps,
                    args.seed
                    + arm_index * 100
                    + 2,
                )
            ),
            "shared_probability_shift_ring1": (
                bootstrap_mean_ci(
                    [
                        r[
                            "shared_probability_shift_ring1"
                        ]
                        for r in rows
                    ],
                    args.bootstrap_reps,
                    args.seed
                    + arm_index * 100
                    + 3,
                )
            ),
            "E1_ring1": (
                bootstrap_mean_ci(
                    [
                        r[
                            "E1_ring1_exact"
                        ]
                        for r in rows
                    ],
                    args.bootstrap_reps,
                    args.seed
                    + arm_index * 100
                    + 4,
                )
            ),
            "mean_n_promoted": (
                float(
                    np.mean(
                        [
                            r[
                                "n_promoted"
                            ]
                            for r in rows
                        ]
                    )
                )
                if rows
                else float("nan")
            ),
            "mean_n_shared_empty": (
                float(
                    np.mean(
                        [
                            r[
                                "n_shared_empty"
                            ]
                            for r in rows
                        ]
                    )
                )
                if rows
                else float("nan")
            ),
        }

    regression, regression_rows = (
        compressed_two_channel_regression(
            channel_rows
        )
    )

    write_csv(
        args.audit_dir
        / "audit-two-channel-regression.csv",
        regression_rows,
    )

    # ------------------------------------------------------------------------
    # Audit C: structural null summary
    # ------------------------------------------------------------------------

    survival_values = [
        int(v)
        for v in survival_flags.values()
    ]

    raw_primary = [
        row
        for row in arm_rows
        if row[
            "budget_label"
        ] == "f=0.10"
    ]

    structural_summary = {
        "realized_x_survival_fraction": (
            float(
                np.mean(
                    survival_values
                )
            )
            if survival_values
            else float("nan")
        ),
        "realized_x_loss_fraction": (
            1.0
            - float(
                np.mean(
                    survival_values
                )
            )
            if survival_values
            else float("nan")
        ),
        "expected_x_loss_fraction": (
            LOSS_RATE
        ),
        "primary_arm_E1_zero_fraction": (
            float(
                np.mean(
                    [
                        abs(
                            float(
                                row[
                                    "E1_ring1"
                                ]
                            )
                        )
                        <= ZERO_EPS
                        for row in raw_primary
                    ]
                )
            )
            if raw_primary
            else float("nan")
        ),
        "primary_arm_G_zero_fraction": (
            float(
                np.mean(
                    [
                        abs(
                            float(
                                row[
                                    "G_local"
                                ]
                            )
                        )
                        == 0.0
                        for row in raw_primary
                    ]
                )
            )
            if raw_primary
            else float("nan")
        ),
        "frozen_primary_result_unchanged": True,
        "future_design_note": (
            "Do not post-hoc remove x-lost probes from V2. "
            "Future experiments should guarantee intervention survival "
            "by design if the intended estimand is conditional on an "
            "actually delivered perturbation."
        ),
    }

    write_csv(
        args.audit_dir
        / "audit-structural-null-summary.csv",
        [
            structural_summary
        ],
    )

    # ------------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------------

    # Channel accounting was asserted row by row above.

    unbounded_far = [
        abs(
            float(
                row["E1_far"]
            )
        )
        for row in arm_rows
        if row[
            "budget_label"
        ] == "unbounded"
    ]

    max_unbounded_far = (
        max(
            unbounded_far
        )
        if unbounded_far
        else float("nan")
    )

    if (
        not math.isfinite(
            max_unbounded_far
        )
        or max_unbounded_far
        > ASSERT_TOL
    ):
        raise RuntimeError(
            "Unbounded far-field structural zero assertion failed."
        )

    # f=.10 reference offset is a definition.
    lag1_primary_offsets = [
        float(
            row["offset"]
        )
        for row in lag_rows
        if (
            row["budget_label"]
            == "f=0.10"
        )
    ]

    max_primary_offset = (
        max(
            abs(v)
            for v in lag1_primary_offsets
        )
        if lag1_primary_offsets
        else float("nan")
    )

    if (
        not math.isfinite(
            max_primary_offset
        )
        or max_primary_offset
        > ASSERT_TOL
    ):
        raise RuntimeError(
            "Reference f=.10 offset-zero assertion failed."
        )

    assertions = {
        "ring1_channel_accounting": {
            "status": "PASS",
            "tolerance": ASSERT_TOL,
            "rows_checked": int(
                len(
                    channel_rows
                )
            ),
            "role": (
                "ASSERTION_NOT_SCIENTIFIC_FINDING"
            ),
        },
        "unbounded_E1_far_zero": {
            "status": "PASS",
            "max_abs": float(
                max_unbounded_far
            ),
            "tolerance": ASSERT_TOL,
            "role": (
                "ASSERTION_NOT_SCIENTIFIC_FINDING"
            ),
        },
        "reference_f0p10_offset_zero": {
            "status": "PASS",
            "max_abs": float(
                max_primary_offset
            ),
            "tolerance": ASSERT_TOL,
            "role": (
                "DEFINITION_ASSERTION_NOT_SCIENTIFIC_FINDING"
            ),
        },
    }

    report = {
        "metadata": {
            "audit_version": (
                "chapter26-v2-zero-inflation-two-channel-audit-v1"
            ),
            "scientific_role": (
                "ANALYSIS_ONLY_NO_NEW_EXPERIMENT"
            ),
            "audited_seed": int(
                args.seed
            ),
            "same_original_v2_seed": bool(
                args.seed
                == ORIGINAL_V2_SEED
            ),
            "frozen_v2_verdict_unchanged": True,
        },
        "audit_A_zero_inflation": {
            "reference": (
                "P(active) = P(x survives) * "
                "[1 - C(F-k,B)/C(F,B)]"
            ),
            "by_arm": zero_summary,
            "notes": [
                (
                    "Observed activity uses |E1_ring1| > 1e-3."
                ),
                (
                    "Finite-selection combinatorial prediction is "
                    "parameter-free at the protocol level."
                ),
                (
                    "x-loss produces a structural null when FORCE/PREVENT "
                    "states collapse."
                ),
            ],
        },
        "audit_B_exact_ring1_channels": {
            "identity": (
                "E1_ring1 = force_only + prevent_only + "
                "shared_probability_shift"
            ),
            "conditioned_summary_x_survives": (
                channel_summary
            ),
            "compressed_two_channel_regression": (
                regression
            ),
        },
        "audit_C_structural_nulls": (
            structural_summary
        ),
        "assertions": assertions,
        "interpretive_boundary": {
            "two_channel_exact_decomposition": (
                "MECHANISTIC ACCOUNTING"
            ),
            "compressed_regression": (
                "DESCRIPTIVE APPROXIMATION"
            ),
            "zero_inflation_reference": (
                "PARAMETER-FREE PROTOCOL PREDICTION"
            ),
            "frozen_primary_status": (
                "UNCHANGED"
            ),
            "no_v3_created": True,
        },
    }

    json_path = (
        args.audit_dir
        / "ch26-v2-mechanism-audit-report.json"
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
        / "ch26-v2-mechanism-audit-report.md"
    )

    md = [
        "# Chapter 26 V2 Mechanism Audit",
        "",
        "## Scientific boundary",
        "",
        "This is an analysis-only audit of the original V2 sample.",
        "The frozen V2 primary verdict remains unchanged.",
        "",
        "## A. Zero-inflation accounting",
        "",
        "```json",
        json.dumps(
            report[
                "audit_A_zero_inflation"
            ],
            indent=2,
        ),
        "```",
        "",
        "## B. Exact ring-1 channel accounting",
        "",
        "```json",
        json.dumps(
            report[
                "audit_B_exact_ring1_channels"
            ],
            indent=2,
        ),
        "```",
        "",
        "## C. Structural-null contribution",
        "",
        "```json",
        json.dumps(
            report[
                "audit_C_structural_nulls"
            ],
            indent=2,
        ),
        "```",
        "",
        "## Assertions",
        "",
        "```json",
        json.dumps(
            assertions,
            indent=2,
        ),
        "```",
        "",
    ]

    md_path.write_text(
        "\n".join(
            md
        ),
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
