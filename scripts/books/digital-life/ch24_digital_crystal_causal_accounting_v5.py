#!/usr/bin/env python3
"""
Digital Life — Chapter 24 V5
Causal Accounting: Probability Shift, Selector Swap, and Divergence
==================================================================

PURPOSE
-------

Chapter 24 V4 finally had enough precision to resolve the original question.

V4 found:

    EXTREME FCP +2 versus -1
        does NOT produce a scientifically meaningful +0.10 difference
        in signed expected lag-1 local construction.

But V4 also found:

    high-FCP interventions
        -> higher model-implied lag-1 divergence probability
        -> higher realized nonzero transient rate
        -> more FORCE/PREVENT selected-set displacement
        -> negative far-field construction difference

The remaining ambiguity is MECHANISTIC.

Two candidate explanations can both produce:

    signed E1 difference ~ 0
    while divergence increases.

A. SHARED-CELL CANCELLATION

    Cells evaluated in both branches may receive positive and negative
    probability shifts whose signed sum cancels.

B. FIXED-BUDGET SELECTOR REDISTRIBUTION

    The intervention changes frontier size/composition.
    The budget stays exactly B.
    FORCE and PREVENT therefore evaluate different candidate sets.

    FORCE-only cells contribute +p.
    PREVENT-only cells contribute -p.

    If frontier-cell probabilities are similar, these swapped terms can
    approximately cancel in signed expectation while still increasing
    path divergence.

V5 decomposes the exact lag-1 expectation into these terms.

It also performs three analyses that V4 should have reported directly:

1. absolute E1_local for HIGH and LOW separately;
2. distribution of occupied-neighbour count in the extreme pairs;
3. a paired realized test of lag-1 divergence / nonzero G_T.

Finally, it tests an analytic first-order selector-dilution law.

THIS IS NOT A NEW SEARCH FOR A FEATURE.

It is a mechanistic accounting experiment on the V4 effect.

DEPENDENCY
----------

Requires beside this file:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py

V5 imports the V4 implementation so that checkpoint construction, frozen
Digital Crystal mechanics, extreme-pair selection, and transient intervention
remain exactly aligned with the reset experiment.

FRESH SEED
----------

Default:
    20260910

Previous Chapter 24:
    V1 20260906
    V2 20260907
    V3 20260908
    V4 20260909

PROFILE
-------

The default confirmatory profile uses:

    384 groups
    same FCP +2 versus -1 exposure
    same same-n / same-radial-bin pairing
    same B = 96
    same H = 12

V5 is computationally cheap relative to V4 because the primary mechanistic
measurements are lag-1 expectations.

PRIMARY QUESTION
----------------

For the lag-1 exact expected attachment difference:

    E1_global
        =
        sum_selected_FORCE p_FORCE
        -
        sum_selected_PREVENT p_PREVENT

decompose:

    E1_global
        =
        SHARED_SHIFT
        +
        FORCE_ONLY_SWAP
        +
        PREVENT_ONLY_SWAP

where:

    SHARED_SHIFT
        =
        sum over cells evaluated in BOTH branches:
            p_force - p_prevent

    FORCE_ONLY_SWAP
        =
        sum over FORCE-only selected cells:
            +p_force

    PREVENT_ONLY_SWAP
        =
        sum over PREVENT-only selected cells:
            -p_prevent

The same decomposition is reported for LOCAL and FAR-FIELD regions.

For every term report:

    HIGH absolute mean
    LOW absolute mean
    HIGH - LOW paired group contrast
    bootstrap CI
    achieved MDE

NO TERM IS CALLED "THE MECHANISM" UNLESS THE ACCOUNTING SUPPORTS IT.

CAUSAL-CONE CORRECTNESS CONTROL
--------------------------------

C1 — FAR-FIELD SHARED-CELL EFFECT MUST BE ZERO AT LAG 1

At lag 1, outside the local causal radius d > 1, ordinary nearest-neighbour
probability influence from x cannot arrive by local propagation.

Therefore any lag-1 far-field expected difference must arise through changed
candidate selection.

V5 defines:

    E1_far_exact
        =
        exact expected FORCE - PREVENT attachments
        for cells with d > 1

and:

    E1_far_swap
        =
        FORCE_ONLY_SWAP_far
        +
        PREVENT_ONLY_SWAP_far

Because shared far-field cells have the same occupied-neighbour state at lag 1
except for selector-mediated membership effects, the prediction is:

    E1_far_exact ≈ E1_far_swap

Frozen equivalence tolerance:

    ±0.02 expected attachments per intervention

Primary group-level discrepancy:

    D_far
        =
        E1_far_exact
        -
        E1_far_swap

Because cells at d > 1 cannot receive ordinary nearest-neighbour influence
from x by lag 1, shared selected cells in that region must have identical local
attachment probabilities. Thus:

    shared_shift_far = 0

and therefore:

    E1_far_exact = selector_swap_far

This is a hard causal-cone / implementation correctness control, not an
independent scientific discovery. The frozen tolerance is ±0.02.

PRIMARY MECHANISTIC TEST — ANALYTIC SELECTOR-DILUTION LAW
-----------------------------------

For one intervention, let:

    F = frontier size before the lag-1 selector
    B = evaluation budget
    DeltaF = F_force - F_prevent

A first-order uniform-selector dilution approximation is:

    selection_rate_prevent
        =
        min(1, B / F_prevent)

    expected_prevent_far_if_sampled
        =
        selection_rate_prevent
        * sum_{c in PREVENT far frontier} p_prevent(c)

    predicted_far_dilution
        =
        -(DeltaF / F_prevent)
        * expected_prevent_far_if_sampled

This uses the full PREVENT frontier probability mass, not the particular
realized selected subset, so it is an analytic expectation under approximately
uniform finite-budget sampling.

This law is intentionally simple.

V5 compares it with:

    exact E1_far_swap

using:

    signed correlation
    regression slope through the origin
    mean residual
    bootstrap CI of mean residual

This is a MECHANISTIC MODEL CHECK.

It is not declared supported merely because signs match.

Frozen practical residual tolerance:

    ±0.05 expected attachments

H3 — REALIZED DIVERGENCE RATE
-----------------------------

V4 reported but did not formally compare:

    HIGH lag-1 realized divergence rate
    LOW lag-1 realized divergence rate

V5 predeclares the paired group contrast:

    Delta P_realized_divergence
        =
        P_high - P_low

SEI:
    +0.05 probability

Statuses:
    SUPPORTED
    BOUNDED_BELOW_SEI
    UNRESOLVED
    INVALID

This is assumption-free with respect to the model-implied divergence formula.

H4 — NONZERO TRANSIENT RATE
---------------------------

Similarly:

    Delta P(G_T != 0)

SEI:
    +0.05 probability

This is downstream and secondary.

CONDITIONAL MAGNITUDE
---------------------

Report:

    E[G_T | G_T != 0] HIGH
    E[G_T | G_T != 0] LOW

and their difference.

No directional hypothesis is frozen for conditional magnitude.

The purpose is to test the V4 descriptive claim:

    class difference is mainly carried by probability of divergence,
    not by cascade magnitude once divergence occurs.

OCCUPIED-NEIGHBOUR SUPPORT
--------------------------

V5 reports the complete n distribution among the 471-style extreme pairs.

If the contrast is concentrated in one n stratum, all bounded claims must be
worded for that stratum rather than for all frontier geometry.

BASELINE-P DIAGNOSTIC
---------------------

Report absolute HIGH and LOW baseline p and paired differences, stratified by n.

Do not infer "natural collapse" from a near-zero aggregate difference without
checking support.

ABSOLUTE E1
-----------

Report HIGH and LOW separately for:

    E1_local
    E1_global
    E1_far

This distinguishes:

    "causal effect roughly constant across classes"

from:

    "signed net expected effect is approximately conserved near zero".

FINITE-BUDGET SELECTION
-----------------------

Report at lag 1:

    F_force
    F_prevent
    DeltaF

    selected shared count
    FORCE-only count
    PREVENT-only count
    symmetric difference
    Jaccard

and all corresponding expected-p contributions.

NO CLAIM ABOUT CHAPTER 25 YET
-----------------------------

V5 does not sweep B.

It only decides whether the B=96 V4 effect is quantitatively accounted for by
the selector mechanism strongly enough to justify Chapter 25's budget sweep.

STOP RULE
---------

V5 closes Chapter 24.

Do not create V6 to retune:
    FCP thresholds
    radial bins
    equivalence tolerance
    divergence SEI
    dilution formula

If the simple dilution model fails, report that failure and move to a direct
budget-sweep mechanism experiment rather than tuning it.

SCIENTIFIC BOUNDARY
-------------------

Success can establish:

    a fixed-budget candidate-selector contribution to immediate non-local
    causal redistribution under the tested Digital Crystal protocol.

It does NOT establish:

    energy
    metabolism
    resource competition in the biological sense
    criticality
    branching ratio
    coherent structure
    individuality
    organism
    life
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21
import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-causal-accounting-v5"
SCHEMA_VERSION = 5
CHAPTER = 24
RUN_TITLE = "Causal Accounting: Probability Shift, Selector Swap, and Divergence"

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

PROFILES = {
    "smoke": {
        "groups": 8,
        "source_profile": "smoke",
        "equivalence_far_accounting": 0.02,
        "dilution_residual_tolerance": 0.05,
        "sei_realized_divergence": 0.05,
        "sei_nonzero_GT": 0.05,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "alpha": 0.05,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "source_profile": "quick",
        "equivalence_far_accounting": 0.02,
        "dilution_residual_tolerance": 0.05,
        "sei_realized_divergence": 0.05,
        "sei_nonzero_GT": 0.05,
        "bootstrap_reps": 3000,
        "signflip_permutations": 8000,
        "alpha": 0.05,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "source_profile": "standard",
        "equivalence_far_accounting": 0.02,
        "dilution_residual_tolerance": 0.05,
        "sei_realized_divergence": 0.05,
        "sei_nonzero_GT": 0.05,
        "bootstrap_reps": 5000,
        "signflip_permutations": 12000,
        "alpha": 0.05,
        "scientific": True,
    },
    "full": {
        "groups": 384,
        "source_profile": "full",
        "equivalence_far_accounting": 0.02,
        "dilution_residual_tolerance": 0.05,
        "sei_realized_divergence": 0.05,
        "sei_nonzero_GT": 0.05,
        "bootstrap_reps": 7000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "scientific": True,
    },
}


# ============================================================================
# Statistics
# ============================================================================

def finite_array(values: Sequence[float]) -> np.ndarray:
    return np.asarray(
        [
            float(v)
            for v in values
            if math.isfinite(float(v))
        ],
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
            "half_width": float("nan"),
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

    low = float(np.quantile(boot, 0.025))
    high = float(np.quantile(boot, 0.975))

    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / math.sqrt(len(arr))
    mde = se * (Z_95_ONE_SIDED + Z_80_POWER)

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": low,
        "ci95_high": high,
        "half_width": float((high - low) / 2.0),
        "achieved_mde80_one_sided": float(mde),
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = finite_array(values)

    if len(arr) == 0:
        return {
            "n": 0,
            "observed_mean": float("nan"),
            "p_value": float("nan"),
        }

    observed = float(np.mean(arr))
    rng = np.random.default_rng(seed)

    null = np.empty(int(permutations), dtype=float)

    for i in range(int(permutations)):
        signs = rng.choice(
            np.asarray([-1.0, 1.0]),
            size=len(arr),
        )
        null[i] = float(np.mean(arr * signs))

    p = (
        1.0 + float(np.sum(null >= observed))
    ) / (
        len(null) + 1.0
    )

    return {
        "n": int(len(arr)),
        "observed_mean": observed,
        "p_value": float(p),
        "permutations": int(permutations),
    }


def directional_status(
    summary: dict,
    test: dict,
    sei: float,
    alpha: float,
    valid: bool,
) -> str:
    if not valid:
        return "INVALID"

    powered = (
        summary["achieved_mde80_one_sided"]
        <= sei
    )

    if (
        powered
        and summary["mean"] >= sei
        and summary["ci95_low"] > 0.0
        and test["p_value"] < alpha
    ):
        return "SUPPORTED"

    if (
        powered
        and summary["ci95_high"] < sei
    ):
        return "BOUNDED_BELOW_SEI"

    return "UNRESOLVED"


def equivalence_status(
    summary: dict,
    tolerance: float,
    valid: bool,
) -> str:
    if not valid:
        return "INVALID"

    if (
        summary["ci95_low"] > -tolerance
        and summary["ci95_high"] < tolerance
    ):
        return "CONSISTENT_WITH_MECHANICAL_ACCOUNTING"

    return "UNRESOLVED"


def correlation(x: Sequence[float], y: Sequence[float]) -> float:
    xa = finite_array(x)
    ya = finite_array(y)

    if len(xa) != len(ya) or len(xa) < 3:
        return float("nan")

    if np.std(xa) == 0 or np.std(ya) == 0:
        return float("nan")

    return float(np.corrcoef(xa, ya)[0, 1])


# ============================================================================
# Exact lag-1 accounting
# ============================================================================

@dataclass
class Accounting:
    group: int
    pair_index: int
    side: str

    fcp: int
    promoted_frontier: int
    occupied_neighbors: int
    baseline_p: float
    local_frontier_density_r2: float

    frontier_force: int
    frontier_prevent: int
    delta_frontier: int

    selected_force: int
    selected_prevent: int
    selected_shared: int
    selected_force_only: int
    selected_prevent_only: int
    selected_symdiff: int
    selected_jaccard: float

    E1_local_exact: float
    E1_far_exact: float
    E1_global_exact: float

    shared_shift_local: float
    shared_shift_far: float
    shared_shift_global: float

    force_only_swap_local: float
    force_only_swap_far: float
    force_only_swap_global: float

    prevent_only_swap_local: float
    prevent_only_swap_far: float
    prevent_only_swap_global: float

    swap_total_local: float
    swap_total_far: float
    swap_total_global: float

    prevent_expected_attachments_far_selected: float
    prevent_expected_attachments_global_selected: float
    prevent_frontier_probability_mass_far: float
    prevent_frontier_probability_mass_global: float
    prevent_selection_rate: float

    predicted_far_dilution: float
    dilution_residual: float

    model_prob_any_local_divergence: float

    realized_lag1_divergence: int
    GT_nonzero: int
    GT_local: float
    GT_global: float
    GT_far: float


def selected_stats(
    force_selected: Sequence[Cell],
    prevent_selected: Sequence[Cell],
) -> dict:
    sf = set(force_selected)
    sp = set(prevent_selected)

    union = sf | sp
    shared = sf & sp

    return {
        "force": sf,
        "prevent": sp,
        "shared": shared,
        "force_only": sf - sp,
        "prevent_only": sp - sf,
        "symdiff": sf ^ sp,
        "jaccard": (
            1.0
            if not union
            else len(shared) / len(union)
        ),
    }


def expected_terms(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    next_input: float,
    origin: Cell,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> dict:
    radius = int(source_profile["radius"])
    budget = int(source_profile["budget"])

    force_frontier = v4.frontier_cells(
        set(force_state.occupied),
        radius,
    )

    prevent_frontier = v4.frontier_cells(
        set(prevent_state.occupied),
        radius,
    )

    force_selected = ch21.select_candidates(
        force_frontier,
        budget,
        force_state.stream_seed,
        int(force_state.step + 1),
    )

    prevent_selected = ch21.select_candidates(
        prevent_frontier,
        budget,
        prevent_state.stream_seed,
        int(prevent_state.step + 1),
    )

    ss = selected_stats(
        force_selected,
        prevent_selected,
    )

    force_occ = set(force_state.occupied)
    prevent_occ = set(prevent_state.occupied)

    terms = {
        "local": {
            "shared": 0.0,
            "force_only": 0.0,
            "prevent_only": 0.0,
            "exact": 0.0,
        },
        "far": {
            "shared": 0.0,
            "force_only": 0.0,
            "prevent_only": 0.0,
            "exact": 0.0,
        },
        "global": {
            "shared": 0.0,
            "force_only": 0.0,
            "prevent_only": 0.0,
            "exact": 0.0,
        },
    }

    q_local = []

    def region(cell: Cell) -> str:
        d = v4.relative_distance(cell, origin)
        return "local" if d <= 1 else "far"

    for cell in ss["shared"]:
        if cell == origin:
            continue

        pf = v4.attachment_probability(
            cell,
            force_occ,
            next_input,
            crystal_params,
        )

        pp = v4.attachment_probability(
            cell,
            prevent_occ,
            next_input,
            crystal_params,
        )

        delta = pf - pp
        reg = region(cell)

        terms[reg]["shared"] += delta
        terms[reg]["exact"] += delta

        terms["global"]["shared"] += delta
        terms["global"]["exact"] += delta

        if reg == "local":
            q_local.append(abs(delta))

    for cell in ss["force_only"]:
        if cell == origin:
            continue

        pf = v4.attachment_probability(
            cell,
            force_occ,
            next_input,
            crystal_params,
        )

        reg = region(cell)

        terms[reg]["force_only"] += pf
        terms[reg]["exact"] += pf

        terms["global"]["force_only"] += pf
        terms["global"]["exact"] += pf

        if reg == "local":
            q_local.append(pf)

    for cell in ss["prevent_only"]:
        if cell == origin:
            continue

        pp = v4.attachment_probability(
            cell,
            prevent_occ,
            next_input,
            crystal_params,
        )

        reg = region(cell)

        terms[reg]["prevent_only"] -= pp
        terms[reg]["exact"] -= pp

        terms["global"]["prevent_only"] -= pp
        terms["global"]["exact"] -= pp

        if reg == "local":
            q_local.append(pp)

    # Expected PREVENT attachments in the actual selected subset.
    prevent_far_selected = 0.0
    prevent_global_selected = 0.0

    for cell in prevent_selected:
        if cell == origin:
            continue

        pp = v4.attachment_probability(
            cell,
            prevent_occ,
            next_input,
            crystal_params,
        )

        prevent_global_selected += pp

        if v4.relative_distance(cell, origin) > 1:
            prevent_far_selected += pp

    # Full PREVENT frontier probability mass.
    prevent_frontier_mass_far = 0.0
    prevent_frontier_mass_global = 0.0

    for cell in prevent_frontier:
        if cell == origin:
            continue

        pp = v4.attachment_probability(
            cell,
            prevent_occ,
            next_input,
            crystal_params,
        )

        prevent_frontier_mass_global += pp

        if v4.relative_distance(cell, origin) > 1:
            prevent_frontier_mass_far += pp

    F_prevent = len(prevent_frontier)
    delta_F = (
        len(force_frontier)
        - len(prevent_frontier)
    )

    selection_rate_prevent = (
        min(
            1.0,
            budget / F_prevent,
        )
        if F_prevent > 0
        else 0.0
    )

    expected_prevent_far_if_sampled = (
        selection_rate_prevent
        * prevent_frontier_mass_far
    )

    # First-order selector-dilution law.
    predicted_far_dilution = (
        -(
            delta_F
            / F_prevent
        )
        * expected_prevent_far_if_sampled
        if F_prevent > 0
        else 0.0
    )

    swap_far = (
        terms["far"]["force_only"]
        + terms["far"]["prevent_only"]
    )

    q_local = [
        min(1.0, max(0.0, float(q)))
        for q in q_local
    ]

    prob_any_local = (
        1.0
        - float(
            np.prod(
                [
                    1.0 - q
                    for q in q_local
                ]
            )
        )
        if q_local
        else 0.0
    )

    return {
        "force_frontier": force_frontier,
        "prevent_frontier": prevent_frontier,
        "force_selected": force_selected,
        "prevent_selected": prevent_selected,
        "selected_stats": ss,
        "terms": terms,
        "prevent_far_selected": float(
            prevent_far_selected
        ),
        "prevent_global_selected": float(
            prevent_global_selected
        ),
        "prevent_frontier_mass_far": float(
            prevent_frontier_mass_far
        ),
        "prevent_frontier_mass_global": float(
            prevent_frontier_mass_global
        ),
        "selection_rate_prevent": float(
            selection_rate_prevent
        ),
        "predicted_far_dilution": float(
            predicted_far_dilution
        ),
        "dilution_residual": float(
            swap_far - predicted_far_dilution
        ),
        "prob_any_local_divergence": float(
            prob_any_local
        ),
    }


# ============================================================================
# Checkpoint intervention with accounting
# ============================================================================

def intervention_with_accounting(
    prepared: v4.GroupPrepared,
    pair: v4.SitePair,
    pair_index: int,
    side: str,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Accounting:
    geometry = (
        pair.high
        if side == "high"
        else pair.low
    )

    checkpoint = prepared.checkpoint
    future_env = prepared.future_env

    radius = int(source_profile["radius"])
    budget = int(source_profile["budget"])
    loss_rate = float(source_profile["loss_rate"])

    x = geometry.cell

    force_grown, _, force_intervention_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        budget,
        force_cell=x,
    )

    prevent_grown, _, prevent_intervention_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        budget,
        prevent_cell=x,
    )

    if (
        force_intervention_selected
        != prevent_intervention_selected
    ):
        raise RuntimeError(
            "intervention evaluated sets diverged before intervention"
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    accounting = expected_terms(
        force_state,
        prevent_state,
        float(future_env[1]),
        x,
        source_profile,
        crystal_params,
    )

    # Reuse V4's canonical transient outcome implementation so realized
    # lag1 divergence / G_T remain exactly aligned with the reset experiment.
    realized = v4.run_transient_intervention(
        checkpoint,
        future_env,
        geometry,
        source_profile,
        crystal_params,
        prepared.group,
        pair_index,
        side,
    )

    ss = accounting["selected_stats"]
    terms = accounting["terms"]

    return Accounting(
        group=int(prepared.group),
        pair_index=int(pair_index),
        side=side,
        fcp=int(geometry.fcp),
        promoted_frontier=int(
            geometry.promoted_frontier
        ),
        occupied_neighbors=int(
            geometry.occupied_neighbors
        ),
        baseline_p=float(
            geometry.baseline_p
        ),
        local_frontier_density_r2=float(
            geometry.local_frontier_density_r2
        ),
        frontier_force=int(
            len(
                accounting[
                    "force_frontier"
                ]
            )
        ),
        frontier_prevent=int(
            len(
                accounting[
                    "prevent_frontier"
                ]
            )
        ),
        delta_frontier=int(
            len(
                accounting[
                    "force_frontier"
                ]
            )
            - len(
                accounting[
                    "prevent_frontier"
                ]
            )
        ),
        selected_force=int(
            len(
                accounting[
                    "force_selected"
                ]
            )
        ),
        selected_prevent=int(
            len(
                accounting[
                    "prevent_selected"
                ]
            )
        ),
        selected_shared=int(
            len(
                ss[
                    "shared"
                ]
            )
        ),
        selected_force_only=int(
            len(
                ss[
                    "force_only"
                ]
            )
        ),
        selected_prevent_only=int(
            len(
                ss[
                    "prevent_only"
                ]
            )
        ),
        selected_symdiff=int(
            len(
                ss[
                    "symdiff"
                ]
            )
        ),
        selected_jaccard=float(
            ss[
                "jaccard"
            ]
        ),
        E1_local_exact=float(
            terms[
                "local"
            ][
                "exact"
            ]
        ),
        E1_far_exact=float(
            terms[
                "far"
            ][
                "exact"
            ]
        ),
        E1_global_exact=float(
            terms[
                "global"
            ][
                "exact"
            ]
        ),
        shared_shift_local=float(
            terms[
                "local"
            ][
                "shared"
            ]
        ),
        shared_shift_far=float(
            terms[
                "far"
            ][
                "shared"
            ]
        ),
        shared_shift_global=float(
            terms[
                "global"
            ][
                "shared"
            ]
        ),
        force_only_swap_local=float(
            terms[
                "local"
            ][
                "force_only"
            ]
        ),
        force_only_swap_far=float(
            terms[
                "far"
            ][
                "force_only"
            ]
        ),
        force_only_swap_global=float(
            terms[
                "global"
            ][
                "force_only"
            ]
        ),
        prevent_only_swap_local=float(
            terms[
                "local"
            ][
                "prevent_only"
            ]
        ),
        prevent_only_swap_far=float(
            terms[
                "far"
            ][
                "prevent_only"
            ]
        ),
        prevent_only_swap_global=float(
            terms[
                "global"
            ][
                "prevent_only"
            ]
        ),
        swap_total_local=float(
            terms[
                "local"
            ][
                "force_only"
            ]
            + terms[
                "local"
            ][
                "prevent_only"
            ]
        ),
        swap_total_far=float(
            terms[
                "far"
            ][
                "force_only"
            ]
            + terms[
                "far"
            ][
                "prevent_only"
            ]
        ),
        swap_total_global=float(
            terms[
                "global"
            ][
                "force_only"
            ]
            + terms[
                "global"
            ][
                "prevent_only"
            ]
        ),
        prevent_expected_attachments_far_selected=float(
            accounting[
                "prevent_far_selected"
            ]
        ),
        prevent_expected_attachments_global_selected=float(
            accounting[
                "prevent_global_selected"
            ]
        ),
        prevent_frontier_probability_mass_far=float(
            accounting[
                "prevent_frontier_mass_far"
            ]
        ),
        prevent_frontier_probability_mass_global=float(
            accounting[
                "prevent_frontier_mass_global"
            ]
        ),
        prevent_selection_rate=float(
            accounting[
                "selection_rate_prevent"
            ]
        ),
        predicted_far_dilution=float(
            accounting[
                "predicted_far_dilution"
            ]
        ),
        dilution_residual=float(
            accounting[
                "dilution_residual"
            ]
        ),
        model_prob_any_local_divergence=float(
            accounting[
                "prob_any_local_divergence"
            ]
        ),
        realized_lag1_divergence=int(
            realized.lag1_realized_divergence
        ),
        GT_nonzero=int(
            realized.GT_nonzero
        ),
        GT_local=float(
            realized.G_local
        ),
        GT_global=float(
            realized.G_global
        ),
        GT_far=float(
            realized.far_field_gain
        ),
    )


# ============================================================================
# Group aggregations
# ============================================================================

def group_side_mean(
    rows: Sequence[Accounting],
    side: str,
    getter,
) -> List[float]:
    buckets: Dict[int, List[float]] = {}

    for row in rows:
        if row.side != side:
            continue

        buckets.setdefault(
            row.group,
            [],
        ).append(
            float(
                getter(
                    row
                )
            )
        )

    return [
        float(
            np.mean(
                values
            )
        )
        for _, values in sorted(
            buckets.items()
        )
        if values
    ]


def paired_group_difference(
    rows: Sequence[Accounting],
    getter,
) -> List[float]:
    keyed: Dict[
        Tuple[int, int],
        Dict[str, Accounting],
    ] = {}

    for row in rows:
        keyed.setdefault(
            (
                row.group,
                row.pair_index,
            ),
            {},
        )[
            row.side
        ] = row

    buckets: Dict[
        int,
        List[float],
    ] = {}

    for (
        group,
        _pair_index,
    ), pair_rows in keyed.items():
        if (
            "high" not in pair_rows
            or "low" not in pair_rows
        ):
            continue

        high = pair_rows[
            "high"
        ]

        low = pair_rows[
            "low"
        ]

        buckets.setdefault(
            group,
            [],
        ).append(
            float(
                getter(
                    high
                )
                - getter(
                    low
                )
            )
        )

    return [
        float(
            np.mean(
                values
            )
        )
        for _, values in sorted(
            buckets.items()
        )
        if values
    ]


def conditional_nonzero(
    rows: Sequence[Accounting],
    side: str,
) -> dict:
    values = np.asarray(
        [
            row.GT_local
            for row in rows
            if row.side == side
        ],
        dtype=float,
    )

    nonzero = values[
        np.abs(
            values
        )
        > 0.0
    ]

    return {
        "n": int(
            len(
                values
            )
        ),
        "nonzero_n": int(
            len(
                nonzero
            )
        ),
        "nonzero_fraction": float(
            len(
                nonzero
            )
            / len(
                values
            )
        )
        if len(
            values
        )
        else float(
            "nan"
        ),
        "mean_all": float(
            np.mean(
                values
            )
        )
        if len(
            values
        )
        else float(
            "nan"
        ),
        "mean_given_nonzero": float(
            np.mean(
                nonzero
            )
        )
        if len(
            nonzero
        )
        else float(
            "nan"
        ),
    }


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(
        self,
        root: Path,
    ):
        self.root = root
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.sections = []

    def json(
        self,
        filename: str,
        payload: dict,
    ) -> None:
        (
            self.root
            / filename
        ).write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

    def stage(
        self,
        filename: str,
        title: str,
        payload: dict,
    ) -> None:
        body = (
            "```json\n"
            + json.dumps(
                payload,
                indent=2,
            )
            + "\n```"
        )

        (
            self.root
            / filename
        ).write_text(
            f"# {title}\n\n{body}\n",
            encoding="utf-8",
        )

        self.sections.append(
            (
                title,
                body,
            )
        )

    def full_report(
        self,
        metadata: dict,
    ) -> Path:
        path = (
            self.root
            / "ch24-causal-accounting-v5-full-report.md"
        )

        parts = [
            "# Chapter 24 — Causal Accounting: Probability Shift, Selector Swap, and Divergence (V5)",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(
                metadata,
                indent=2,
            ),
            "```",
            "",
        ]

        for title, body in self.sections:
            parts.extend(
                [
                    "---",
                    "",
                    f"## {title}",
                    "",
                    body,
                    "",
                ]
            )

        path.write_text(
            "\n".join(
                parts
            ),
            encoding="utf-8",
        )

        return path


# ============================================================================
# Raw output
# ============================================================================

def write_raw(
    reporter: Reporter,
    rows: Sequence[Accounting],
) -> None:
    jsonl = (
        reporter.root
        / "raw-accounting.jsonl"
    )

    with jsonl.open(
        "w",
        encoding="utf-8",
    ) as f:
        for row in rows:
            f.write(
                json.dumps(
                    asdict(
                        row
                    )
                )
                + "\n"
            )

    csv_path = (
        reporter.root
        / "raw-accounting.csv"
    )

    if rows:
        fieldnames = list(
            asdict(
                rows[
                    0
                ]
            ).keys()
        )

        with csv_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for row in rows:
                writer.writerow(
                    asdict(
                        row
                    )
                )


# ============================================================================
# Stage 0
# ============================================================================

def stage_0(
    reporter: Reporter,
    profile: dict,
    source_profile: dict,
    seed: int,
) -> dict:
    payload = {
        "experiment_version": (
            EXPERIMENT_VERSION
        ),
        "role": (
            "MECHANISTIC ACCOUNTING OF V4 EXTREME-FCP EFFECT"
        ),
        "seed": int(
            seed
        ),
        "source_profile": profile[
            "source_profile"
        ],
        "groups": int(
            source_profile[
                "groups"
            ]
        ),
        "exposure": {
            "high": (
                f"FCP >= {source_profile['high_fcp_min']}"
            ),
            "low": (
                f"FCP <= {source_profile['low_fcp_max']}"
            ),
            "minimum_delta_FCP": int(
                source_profile[
                    "minimum_fcp_difference"
                ]
            ),
        },
        "primary_accounting_identity": (
            "E1 = shared_shift + force_only_swap + prevent_only_swap"
        ),
        "C1_causal_cone_correctness": {
            "quantity": (
                "E1_far_exact - swap_total_far = shared_shift_far"
            ),
            "role": "hard lag-1 causal-cone correctness control",
            "equivalence_tolerance": float(
                profile[
                    "equivalence_far_accounting"
                ]
            ),
        },
        "H1_selector_dilution": {
            "prediction": (
                "-(DeltaF / F_prevent) * expected PREVENT far attachments"
            ),
            "residual_tolerance": float(
                profile[
                    "dilution_residual_tolerance"
                ]
            ),
        },
        "H3_realized_divergence": {
            "SEI": float(
                profile[
                    "sei_realized_divergence"
                ]
            ),
        },
        "H4_nonzero_GT_rate": {
            "SEI": float(
                profile[
                    "sei_nonzero_GT"
                ]
            ),
        },
        "occupied_neighbor_distribution": (
            "mandatory scope diagnostic"
        ),
        "absolute_E1_high_low": (
            "mandatory mechanism discriminator"
        ),
        "status": (
            "FROZEN"
            if profile[
                "scientific"
            ]
            else "ENGINEERING_SMOKE_ONLY"
        ),
        "stop_rule": (
            "V5 closes Chapter 24; no threshold or formula tuning after run."
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen V5 Causal Accounting Protocol",
        payload,
    )

    reporter.json(
        "stage-00-protocol.json",
        payload,
    )

    return payload


# ============================================================================
# Stage 1 — run
# ============================================================================

def stage_1_run(
    reporter: Reporter,
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[Accounting],
    dict,
]:
    prepared = v4.prepare_groups(
        source_profile,
        crystal_params,
        seed,
    )

    support_groups = [
        group
        for group in prepared
        if group.pairs
    ]

    rows: List[
        Accounting
    ] = []

    for group in tqdm(
        support_groups,
        desc="Chapter 24 V5 accounting",
    ):
        for pair_index, pair in enumerate(
            group.pairs
        ):
            rows.append(
                intervention_with_accounting(
                    group,
                    pair,
                    pair_index,
                    "high",
                    source_profile,
                    crystal_params,
                )
            )

            rows.append(
                intervention_with_accounting(
                    group,
                    pair,
                    pair_index,
                    "low",
                    source_profile,
                    crystal_params,
                )
            )

    coverage = (
        len(
            support_groups
        )
        / int(
            source_profile[
                "groups"
            ]
        )
    )

    n_counts: Dict[
        int,
        int,
    ] = {}

    pair_n_counts: Dict[
        int,
        int,
    ] = {}

    for row in rows:
        n_counts[
            row.occupied_neighbors
        ] = (
            n_counts.get(
                row.occupied_neighbors,
                0,
            )
            + 1
        )

    seen_pairs = set()

    for row in rows:
        key = (
            row.group,
            row.pair_index,
        )

        if key in seen_pairs:
            continue

        seen_pairs.add(
            key
        )

        pair_n_counts[
            row.occupied_neighbors
        ] = (
            pair_n_counts.get(
                row.occupied_neighbors,
                0,
            )
            + 1
        )

    payload = {
        "requested_groups": int(
            source_profile[
                "groups"
            ]
        ),
        "groups_with_pairs": int(
            len(
                support_groups
            )
        ),
        "coverage_fraction": float(
            coverage
        ),
        "total_pairs": int(
            len(
                rows
            )
            // 2
        ),
        "total_interventions": int(
            len(
                rows
            )
        ),
        "occupied_neighbor_site_distribution": {
            str(
                k
            ): int(
                v
            )
            for k, v in sorted(
                n_counts.items()
            )
        },
        "occupied_neighbor_pair_distribution": {
            str(
                k
            ): int(
                v
            )
            for k, v in sorted(
                pair_n_counts.items()
            )
        },
    }

    reporter.stage(
        "stage-01-run-and-support.md",
        "Stage 1 — V5 Extreme-Pair Support and n Distribution",
        payload,
    )

    reporter.json(
        "stage-01-run-and-support.json",
        payload,
    )

    write_raw(
        reporter,
        rows,
    )

    return rows, payload


# ============================================================================
# Stage 2 — absolute E1 and accounting
# ============================================================================

def stage_2_accounting(
    reporter: Reporter,
    profile: dict,
    rows: Sequence[
        Accounting
    ],
    seed: int,
) -> dict:
    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    high_E1_local = group_side_mean(
        rows,
        "high",
        lambda r:
        r.E1_local_exact,
    )

    low_E1_local = group_side_mean(
        rows,
        "low",
        lambda r:
        r.E1_local_exact,
    )

    high_E1_global = group_side_mean(
        rows,
        "high",
        lambda r:
        r.E1_global_exact,
    )

    low_E1_global = group_side_mean(
        rows,
        "low",
        lambda r:
        r.E1_global_exact,
    )

    high_E1_far = group_side_mean(
        rows,
        "high",
        lambda r:
        r.E1_far_exact,
    )

    low_E1_far = group_side_mean(
        rows,
        "low",
        lambda r:
        r.E1_far_exact,
    )

    # Accounting identity residual.
    far_residual = group_side_mean(
        rows,
        "high",
        lambda r:
        r.E1_far_exact
        - r.swap_total_far,
    ) + []

    # Need both high and low accounting residuals.
    far_residual_all = []

    buckets: Dict[
        int,
        List[float],
    ] = {}

    for row in rows:
        buckets.setdefault(
            row.group,
            [],
        ).append(
            float(
                row.E1_far_exact
                - row.swap_total_far
            )
        )

    far_residual_all = [
        float(
            np.mean(
                values
            )
        )
        for _, values in sorted(
            buckets.items()
        )
    ]

    far_residual_summary = bootstrap_mean_ci(
        far_residual_all,
        reps,
        seed + 201,
    )

    far_accounting_status = equivalence_status(
        far_residual_summary,
        float(
            profile[
                "equivalence_far_accounting"
            ]
        ),
        True,
    )

    # Shared vs swap terms, absolute by side.
    component_names = [
        "shared_shift_local",
        "swap_total_local",
        "shared_shift_far",
        "swap_total_far",
        "shared_shift_global",
        "swap_total_global",
    ]

    components = {}

    for index, name in enumerate(
        component_names
    ):
        components[
            name
        ] = {
            "high": bootstrap_mean_ci(
                group_side_mean(
                    rows,
                    "high",
                    lambda r, n=name:
                    getattr(
                        r,
                        n,
                    ),
                ),
                reps,
                seed + 220 + index * 3,
            ),
            "low": bootstrap_mean_ci(
                group_side_mean(
                    rows,
                    "low",
                    lambda r, n=name:
                    getattr(
                        r,
                        n,
                    ),
                ),
                reps,
                seed + 221 + index * 3,
            ),
            "high_minus_low": bootstrap_mean_ci(
                paired_group_difference(
                    rows,
                    lambda r, n=name:
                    getattr(
                        r,
                        n,
                    ),
                ),
                reps,
                seed + 222 + index * 3,
            ),
        }

    payload = {
        "absolute_E1": {
            "local": {
                "high": bootstrap_mean_ci(
                    high_E1_local,
                    reps,
                    seed + 250,
                ),
                "low": bootstrap_mean_ci(
                    low_E1_local,
                    reps,
                    seed + 251,
                ),
                "high_minus_low": bootstrap_mean_ci(
                    paired_group_difference(
                        rows,
                        lambda r:
                        r.E1_local_exact,
                    ),
                    reps,
                    seed + 252,
                ),
            },
            "far": {
                "high": bootstrap_mean_ci(
                    high_E1_far,
                    reps,
                    seed + 253,
                ),
                "low": bootstrap_mean_ci(
                    low_E1_far,
                    reps,
                    seed + 254,
                ),
                "high_minus_low": bootstrap_mean_ci(
                    paired_group_difference(
                        rows,
                        lambda r:
                        r.E1_far_exact,
                    ),
                    reps,
                    seed + 255,
                ),
            },
            "global": {
                "high": bootstrap_mean_ci(
                    high_E1_global,
                    reps,
                    seed + 256,
                ),
                "low": bootstrap_mean_ci(
                    low_E1_global,
                    reps,
                    seed + 257,
                ),
                "high_minus_low": bootstrap_mean_ci(
                    paired_group_difference(
                        rows,
                        lambda r:
                        r.E1_global_exact,
                    ),
                    reps,
                    seed + 258,
                ),
            },
        },
        "shared_vs_swap_components": components,
        "H1_far_field_accounting": {
            "discrepancy_E1_far_minus_swap_far": (
                far_residual_summary
            ),
            "equivalence_tolerance": float(
                profile[
                    "equivalence_far_accounting"
                ]
            ),
            "status": (
                far_accounting_status
            ),
        },
    }

    reporter.stage(
        "stage-02-exact-accounting.md",
        "Stage 2 — Absolute E1 and Shared-vs-Swap Accounting",
        payload,
    )

    reporter.json(
        "stage-02-exact-accounting.json",
        payload,
    )

    return payload


# ============================================================================
# Stage 3 — dilution law
# ============================================================================

def stage_3_dilution(
    reporter: Reporter,
    profile: dict,
    rows: Sequence[
        Accounting
    ],
    seed: int,
) -> dict:
    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    predicted = [
        float(
            row.predicted_far_dilution
        )
        for row in rows
    ]

    exact_swap = [
        float(
            row.swap_total_far
        )
        for row in rows
    ]

    residual = [
        float(
            row.dilution_residual
        )
        for row in rows
    ]

    x = np.asarray(
        predicted,
        dtype=float,
    )

    y = np.asarray(
        exact_swap,
        dtype=float,
    )

    denom = float(
        np.sum(
            x * x
        )
    )

    slope = (
        float(
            np.sum(
                x * y
            )
            / denom
        )
        if denom > 0
        else float(
            "nan"
        )
    )

    corr = correlation(
        predicted,
        exact_swap,
    )

    # Independent group residual for uncertainty.
    group_residual: Dict[
        int,
        List[float],
    ] = {}

    for row in rows:
        group_residual.setdefault(
            row.group,
            [],
        ).append(
            row.dilution_residual
        )

    group_residual_values = [
        float(
            np.mean(
                values
            )
        )
        for _, values in sorted(
            group_residual.items()
        )
    ]

    residual_summary = bootstrap_mean_ci(
        group_residual_values,
        reps,
        seed + 301,
    )

    tolerance = float(
        profile[
            "dilution_residual_tolerance"
        ]
    )

    status = (
        "CONSISTENT_WITH_SIMPLE_DILUTION_LAW"
        if (
            residual_summary[
                "ci95_low"
            ]
            > -tolerance
            and residual_summary[
                "ci95_high"
            ]
            < tolerance
        )
        else "SIMPLE_DILUTION_LAW_FAILED_OR_UNRESOLVED"
    )

    payload = {
        "prediction": (
            "predicted_far = -(DeltaF/F_prevent) * "
            "(B/F_prevent) * sum_far_frontier p_prevent"
        ),
        "raw_intervention_count": int(
            len(
                rows
            )
        ),
        "correlation_predicted_vs_exact_swap": float(
            corr
        ),
        "slope_through_origin": float(
            slope
        ),
        "mean_residual_exact_swap_minus_prediction": (
            residual_summary
        ),
        "frozen_residual_tolerance": float(
            tolerance
        ),
        "status": status,
        "note": (
            "Correlation/slope are descriptive model checks. "
            "The frozen practical criterion is the group-level residual interval."
        ),
    }

    reporter.stage(
        "stage-03-selector-dilution.md",
        "Stage 3 — First-Order Selector-Dilution Law",
        payload,
    )

    reporter.json(
        "stage-03-selector-dilution.json",
        payload,
    )

    return payload


# ============================================================================
# Stage 4 — realized divergence and conditional cascade
# ============================================================================

def stage_4_realized(
    reporter: Reporter,
    profile: dict,
    rows: Sequence[
        Accounting
    ],
    seed: int,
) -> dict:
    alpha = float(
        profile[
            "alpha"
        ]
    )

    div_delta = paired_group_difference(
        rows,
        lambda r:
        r.realized_lag1_divergence,
    )

    nz_delta = paired_group_difference(
        rows,
        lambda r:
        r.GT_nonzero,
    )

    div_summary = bootstrap_mean_ci(
        div_delta,
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 401,
    )

    div_test = signflip_greater(
        div_delta,
        int(
            profile[
                "signflip_permutations"
            ]
        ),
        seed + 402,
    )

    div_status = directional_status(
        div_summary,
        div_test,
        float(
            profile[
                "sei_realized_divergence"
            ]
        ),
        alpha,
        True,
    )

    nz_summary = bootstrap_mean_ci(
        nz_delta,
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 403,
    )

    nz_test = signflip_greater(
        nz_delta,
        int(
            profile[
                "signflip_permutations"
            ]
        ),
        seed + 404,
    )

    nz_status = directional_status(
        nz_summary,
        nz_test,
        float(
            profile[
                "sei_nonzero_GT"
            ]
        ),
        alpha,
        True,
    )

    high_div_abs = bootstrap_mean_ci(
        group_side_mean(
            rows,
            "high",
            lambda r:
            r.realized_lag1_divergence,
        ),
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 405,
    )

    low_div_abs = bootstrap_mean_ci(
        group_side_mean(
            rows,
            "low",
            lambda r:
            r.realized_lag1_divergence,
        ),
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 406,
    )

    high_nz_abs = bootstrap_mean_ci(
        group_side_mean(
            rows,
            "high",
            lambda r:
            r.GT_nonzero,
        ),
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 407,
    )

    low_nz_abs = bootstrap_mean_ci(
        group_side_mean(
            rows,
            "low",
            lambda r:
            r.GT_nonzero,
        ),
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        seed + 408,
    )

    high_cond = conditional_nonzero(
        rows,
        "high",
    )

    low_cond = conditional_nonzero(
        rows,
        "low",
    )

    payload = {
        "H3_realized_lag1_divergence": {
            "high_absolute": high_div_abs,
            "low_absolute": low_div_abs,
            "high_minus_low": div_summary,
            "SEI": float(
                profile[
                    "sei_realized_divergence"
                ]
            ),
            "signflip": div_test,
            "status": div_status,
        },
        "H4_nonzero_transient_rate": {
            "high_absolute": high_nz_abs,
            "low_absolute": low_nz_abs,
            "high_minus_low": nz_summary,
            "SEI": float(
                profile[
                    "sei_nonzero_GT"
                ]
            ),
            "signflip": nz_test,
            "status": nz_status,
        },
        "conditional_transient_magnitude": {
            "high": high_cond,
            "low": low_cond,
            "difference_of_raw_conditional_means": float(
                high_cond[
                    "mean_given_nonzero"
                ]
                - low_cond[
                    "mean_given_nonzero"
                ]
            ),
            "scope": (
                "Descriptive mechanism decomposition; no directional claim frozen."
            ),
        },
    }

    reporter.stage(
        "stage-04-realized-divergence.md",
        "Stage 4 — Realized Divergence and Conditional Cascade",
        payload,
    )

    reporter.json(
        "stage-04-realized-divergence.json",
        payload,
    )

    return payload


# ============================================================================
# Stage 5 — n-stratified baseline p and scope
# ============================================================================

def stage_5_scope(
    reporter: Reporter,
    profile: dict,
    rows: Sequence[
        Accounting
    ],
    seed: int,
) -> dict:
    by_n = {}

    n_values = sorted(
        set(
            row.occupied_neighbors
            for row in rows
        )
    )

    for index, n in enumerate(
        n_values
    ):
        subset = [
            row
            for row in rows
            if row.occupied_neighbors == n
        ]

        high = [
            row.baseline_p
            for row in subset
            if row.side == "high"
        ]

        low = [
            row.baseline_p
            for row in subset
            if row.side == "low"
        ]

        # pair difference by group/pair within this n
        pair_map: Dict[
            Tuple[int, int],
            Dict[str, Accounting],
        ] = {}

        for row in subset:
            pair_map.setdefault(
                (
                    row.group,
                    row.pair_index,
                ),
                {},
            )[
                row.side
            ] = row

        raw_diffs = [
            pair_rows[
                "high"
            ].baseline_p
            - pair_rows[
                "low"
            ].baseline_p
            for pair_rows in pair_map.values()
            if (
                "high" in pair_rows
                and "low" in pair_rows
            )
        ]

        by_n[
            str(
                n
            )
        ] = {
            "interventions": int(
                len(
                    subset
                )
            ),
            "pairs": int(
                len(
                    raw_diffs
                )
            ),
            "high_baseline_p_mean": float(
                np.mean(
                    high
                )
            )
            if high
            else float(
                "nan"
            ),
            "low_baseline_p_mean": float(
                np.mean(
                    low
                )
            )
            if low
            else float(
                "nan"
            ),
            "raw_pair_baseline_p_difference": bootstrap_mean_ci(
                raw_diffs,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                seed + 500 + index,
            ),
        }

    pair_counts = {
        str(
            n
        ): int(
            len(
                [
                    row
                    for row in rows
                    if (
                        row.side == "high"
                        and row.occupied_neighbors == n
                    )
                ]
            )
        )
        for n in n_values
    }

    total_pairs = sum(
        pair_counts.values()
    )

    dominant_n = (
        max(
            pair_counts,
            key=pair_counts.get,
        )
        if pair_counts
        else None
    )

    dominant_fraction = (
        pair_counts[
            dominant_n
        ]
        / total_pairs
        if (
            dominant_n is not None
            and total_pairs
        )
        else float(
            "nan"
        )
    )

    payload = {
        "pair_distribution_by_occupied_neighbors": (
            pair_counts
        ),
        "dominant_n": dominant_n,
        "dominant_n_fraction": float(
            dominant_fraction
        ),
        "baseline_p_by_n": by_n,
        "scope_warning": (
            "If one n stratum dominates, scientific prose must explicitly "
            "scope the extreme-FCP result to that supported stratum."
        ),
    }

    reporter.stage(
        "stage-05-scope-and-baseline-p.md",
        "Stage 5 — Occupied-Neighbour Support and Baseline-p Scope",
        payload,
    )

    reporter.json(
        "stage-05-scope-and-baseline-p.json",
        payload,
    )

    return payload


# ============================================================================
# Stage 6 — verdict
# ============================================================================

def stage_6_verdict(
    reporter: Reporter,
    profile: dict,
    accounting: dict,
    dilution: dict,
    realized: dict,
    scope: dict,
) -> dict:
    h1 = accounting[
        "H1_far_field_accounting"
    ][
        "status"
    ]

    h2 = dilution[
        "status"
    ]

    h3 = realized[
        "H3_realized_lag1_divergence"
    ][
        "status"
    ]

    h4 = realized[
        "H4_nonzero_transient_rate"
    ][
        "status"
    ]

    if not profile[
        "scientific"
    ]:
        overall = "ENGINEERING_SMOKE_ONLY"

        bounded = (
            "Smoke profile completed. No scientific interpretation is eligible."
        )

    elif (
        h1
        == "CONSISTENT_WITH_MECHANICAL_ACCOUNTING"
        and h2
        == "CONSISTENT_WITH_SIMPLE_DILUTION_LAW"
    ):
        overall = (
            "FIXED_BUDGET_SELECTOR_ACCOUNTING_SUPPORTED"
        )

        bounded = (
            "At B=96, the lag-1 far-field expected attachment difference was "
            "accounted for by FORCE/PREVENT selector swaps within the frozen "
            "equivalence tolerance, and the simple frontier-dilution law "
            "matched the selector-swap term within its predeclared residual "
            "tolerance. Realized divergence and downstream nonzero-rate "
            "results are reported separately."
        )

    elif (
        h1
        == "CONSISTENT_WITH_MECHANICAL_ACCOUNTING"
    ):
        overall = (
            "SELECTOR_SWAP_ACCOUNTING_SUPPORTED_SIMPLE_DILUTION_UNRESOLVED"
        )

        bounded = (
            "The exact lag-1 far-field effect was accounted for by changed "
            "candidate selection, but the simple first-order dilution law did "
            "not clear its frozen approximation tolerance."
        )

    else:
        overall = (
            "V5_SELECTOR_MECHANISM_UNRESOLVED"
        )

        bounded = (
            "V5 did not establish the frozen selector-accounting mechanism "
            "strongly enough to promote it as the Chapter 24 explanation."
        )

    payload = {
        "overall_status": overall,
        "bounded_claim": bounded,
        "C1_causal_cone_correctness": h1,
        "H1_simple_dilution": h2,
        "H3_realized_divergence": h3,
        "H4_nonzero_transient_rate": h4,
        "dominant_n": scope[
            "dominant_n"
        ],
        "dominant_n_fraction": scope[
            "dominant_n_fraction"
        ],
        "chapter24_stop_rule": (
            "STOP. No V6. Rewrite Chapter 24 using V4/V5 and then move to "
            "the dedicated finite-budget sweep."
        ),
        "next": (
            "Chapter 25: B in {24,48,96,192,unbounded}, outside-causal-cone "
            "selection/attachment displacement, analytic mechanical reference, "
            "and unbounded hard-zero correctness control."
        ),
    }

    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Bounded Chapter 24 V5 Verdict",
        payload,
    )

    reporter.json(
        "stage-06-verdict.json",
        payload,
    )

    return payload


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--profile",
        choices=sorted(
            PROFILES
        ),
        default="full",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=20260910,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch24-causal-accounting-v5"
        ),
    )

    args = parser.parse_args()

    profile = dict(
        PROFILES[
            args.profile
        ]
    )

    source_profile = dict(
        v4.PROFILES[
            profile[
                "source_profile"
            ]
        ]
    )

    # Ensure exact intended group count even if imported V4 profile evolves.
    source_profile[
        "groups"
    ] = int(
        profile[
            "groups"
        ]
    )

    crystal_params = ch18.CrystalParams()

    reporter = Reporter(
        args.report_dir
    )

    metadata = {
        "experiment_version": (
            EXPERIMENT_VERSION
        ),
        "schema_version": (
            SCHEMA_VERSION
        ),
        "chapter": CHAPTER,
        "run_title": RUN_TITLE,
        "profile": args.profile,
        "profile_config": profile,
        "source_v4_profile": source_profile,
        "seed": int(
            args.seed
        ),
        "fresh_seed": bool(
            int(
                args.seed
            )
            not in {
                20260906,
                20260907,
                20260908,
                20260909,
            }
        ),
        "started_at_unix": float(
            time.time()
        ),
    }

    print(
        "="
        * 78
    )

    print(
        "CHAPTER 24 V5 — CAUSAL ACCOUNTING"
    )

    print(
        f"profile={args.profile} "
        f"groups={source_profile['groups']} "
        f"B={source_profile['budget']} "
        f"seed={args.seed}"
    )

    print(
        "="
        * 78
    )

    stage_0(
        reporter,
        profile,
        source_profile,
        args.seed,
    )

    rows, run_info = stage_1_run(
        reporter,
        profile,
        source_profile,
        crystal_params,
        args.seed,
    )

    if not rows:
        raise RuntimeError(
            "No extreme FCP pairs available."
        )

    accounting = stage_2_accounting(
        reporter,
        profile,
        rows,
        args.seed,
    )

    dilution = stage_3_dilution(
        reporter,
        profile,
        rows,
        args.seed,
    )

    realized = stage_4_realized(
        reporter,
        profile,
        rows,
        args.seed,
    )

    scope = stage_5_scope(
        reporter,
        profile,
        rows,
        args.seed,
    )

    verdict = stage_6_verdict(
        reporter,
        profile,
        accounting,
        dilution,
        realized,
        scope,
    )

    metadata[
        "finished_at_unix"
    ] = float(
        time.time()
    )

    metadata[
        "final_status"
    ] = verdict[
        "overall_status"
    ]

    reporter.json(
        "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()

    print(
        "="
        * 78
    )

    print(
        f"FINAL STATUS: {verdict['overall_status']}"
    )

    print(
        verdict[
            "bounded_claim"
        ]
    )

    print(
        f"Report: {report}"
    )

    print(
        "="
        * 78
    )


if __name__ == "__main__":
    main()
