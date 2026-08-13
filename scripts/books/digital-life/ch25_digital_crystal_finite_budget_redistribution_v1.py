#!/usr/bin/env python3
"""
Digital Life — Chapter 25 V1
How Does Finite Computation Create Non-Local Coupling?
======================================================

CONTEXT
-------

Chapter 24 V4/V5 established a bounded mechanism in the supported
single-contact frontier regime (occupied-neighbour count n=1):

    LOCAL INTERVENTION
        ↓
    FRONTIER SIZE / COMPOSITION CHANGES
        ↓
    FIXED GLOBAL EVALUATION BUDGET
        ↓
    DIFFERENT FRONTIER CANDIDATES ARE EVALUATED
        ↓
    EXPECTED FAR-FIELD CONSTRUCTION CHANGES

At B=96, the strongest quantitative observation was:

    FCP +2  -> far-field expected effect ≈ -0.117
    FCP -1  -> far-field expected effect ≈ +0.063

Observed ratio:
    -0.117 / +0.063 ≈ -1.86

Parameter-free size-dilution prediction:
    -2 : +1

Chapter 25 does NOT grow different crystals under different budgets.

That would confound:
    budget
    morphology
    population
    frontier size
    history

Instead Chapter 25 freezes the checkpoint and intervention, then changes only
the LAG-1 evaluation budget.

PRIMARY QUESTION
----------------

How does the selector-mediated outside-causal-cone effect change as the
fraction of frontier opportunities that can be evaluated approaches one?

For each frozen checkpoint/site/intervention:

    SAME checkpoint
    SAME x
    SAME FORCE/PREVENT intervention update
    SAME intervention loss realization
    SAME lag-1 environment
    SAME cell-keyed probability rule

Only:

    B_lag1

changes.

CONTROL PARAMETER
-----------------

Let:

    F_ref = max(F_force, F_prevent)

at lag 1 after the intervention update and ordinary loss.

For each requested fraction f:

    f ∈ {0.05, 0.10, 0.25, 0.50, 0.75, 1.00}

use:

    B = ceil(f * F_ref)

with:

    B >= 1

The same absolute B is used in FORCE and PREVENT for that intervention.

An additional:

    UNBOUNDED

arm evaluates the entire branch-specific frontier directly.

At f=1.00:
    B >= both branch frontier sizes.

Therefore both branches evaluate all their frontier cells.

The frontier sets may still differ LOCALLY.

But outside the nearest-neighbour causal cone (d > 1), the branch frontiers are
identical at lag 1.

Therefore:

    outside-cone selected-set displacement = 0
    outside-cone expected attachment displacement = 0

at full/unbounded evaluation.

This is a HARD correctness control.

SUPPORTED SITE REGIME
---------------------

Chapter 24 V5 showed that the extreme FCP +2 versus -1 contrast was supported
entirely at:

    occupied_neighbors = 1

Chapter 25 therefore freezes:

    n = 1

rather than silently generalizing beyond the supported regime.

FCP LEVELS
----------

Chapter 24's outcome-blind support audit found all four local FCP levels:

    -1
     0
    +1
    +2

Chapter 25 uses all supported n=1 levels.

This allows two complementary tests:

1. LINEARITY / RATIO
       far-field effect ∝ -DeltaF

2. FCP = 0 COMPOSITION CONTROL
       frontier SIZE change is zero,
       but frontier COMPOSITION can still change.

Thus FCP=0 isolates composition substitution from the size-dilution term.

IMPORTANT DISTINCTION
---------------------

For a frontier intervention:

    FCP at checkpoint

describes the deterministic local frontier transformation if x is occupied.

But ordinary intervention loss can remove x before lag 1.

Therefore the exact lag-1 branch frontier difference is measured directly as:

    DeltaF_lag1 = F_force - F_prevent

All analytic calculations use the ACTUAL lag-1 DeltaF.

Original FCP remains the exposure class.

INTERVENTION UPDATE
-------------------

The intervention update itself remains the canonical Chapter 24 reset
intervention at:

    B_intervention = 96

This creates FORCE and PREVENT lag-1 states without changing the historical
checkpoint.

Then the Chapter 25 budget sweep begins.

This design asks:

    GIVEN THE SAME LOCAL CAUSAL PERTURBATION,
    how does lag-1 allocation change with evaluation capacity?

OUTSIDE-CAUSAL-CONE REGION
--------------------------

Primary region:

    d > 1

At lag 1, the local nearest-neighbour attachment rule cannot transmit the
effect of x beyond one lattice step.

Therefore any expected FORCE/PREVENT difference at d > 1 is selector-mediated.

This locality statement is a code/property assertion, not an empirical
hypothesis.

MEASUREMENTS PER SITE × BUDGET
------------------------------

For each branch:

    frontier size
    effective B
    evaluation fraction

For FORCE vs PREVENT:

    outside-cone selected shared count
    outside-cone FORCE-only count
    outside-cone PREVENT-only count
    outside-cone symmetric difference
    outside-cone Jaccard

    exact expected outside-cone attachment difference

    exact local ring-1 expected attachment difference
    exact global expected attachment difference

    selector swap contribution

    shared-cell probability contribution

Correctness assertion:
    shared far-field probability shift == 0

PRIMARY HYPOTHESIS H1
---------------------

H1 — LOW-BUDGET FAR-FIELD EFFECT SCALES WITH -DeltaF

In the subsampling regime:

    f ∈ {0.05, 0.10, 0.25}

the first-order size-dilution model predicts:

    E_far
        ∝
        -DeltaF

For exposure classes with non-zero mean actual DeltaF:

    FCP = -1
    FCP = +1
    FCP = +2

compute the class mean outside-cone expected effect.

For each budget fraction separately, fit THROUGH THE ORIGIN:

    mean_E_far(FCP class)
        =
        beta_f * (-mean_DeltaF_class)

No intercept.

Report:
    beta_f
    class-level R² through origin
    relative residual for each class

Frozen low-budget linearity criterion:

    for each f in {0.05, 0.10, 0.25}:
        weighted mean absolute residual
        <= 25% of weighted mean absolute predicted magnitude

The tolerance is RELATIVE to the predicted effect, not a fixed ±0.05.

H1 is SUPPORTED only if all three low-budget fractions clear this criterion.

PARAMETER-FREE EXTREME RATIO
----------------------------

For the original extreme classes:

    FCP +2
    FCP -1

compute:

    R_f
        =
        mean_E_far(+2)
        /
        mean_E_far(-1)

The size-only parameter-free prediction is approximately:

    -2.0

because their deterministic checkpoint frontier changes are +2 and -1 and the
ordinary loss survival factor is common.

For each low-budget fraction report:

    observed ratio
    bootstrap CI by independent group
    relative error from -2

Frozen ratio criterion:

    |R_f - (-2)| / 2 <= 0.25

The ratio is a MECHANISTIC calibration target.

No p-value against zero is used for the ratio.

H2 — COMPOSITION-ONLY CONTROL AT FCP = 0
----------------------------------------

For FCP=0:

    size-dilution contribution predicted from DeltaF is approximately zero.

But frontier composition can still change:
    x leaves frontier
    another local cell can enter.

Therefore FCP=0 measures composition substitution with the size term removed.

Report for each budget fraction:

    mean actual DeltaF
    mean outside-cone symmetric difference
    mean outside-cone E_far

This is primarily a decomposition/control.

No claim that E_far must be exactly zero under finite B.

H3 — BUDGET SATURATION / BREAKDOWN
----------------------------------

As f -> 1:

    candidate subsampling disappears.

The first-order low-budget dilution approximation must therefore break down.

For each non-zero FCP class compute:

    normalized far-field magnitude:

        |E_far(f)| / |E_far(0.10)|

The mechanistic prediction is:

    substantial at low f
    declining near saturation
    exactly zero at full/unbounded evaluation.

No monotonicity p-value is required.

The key hard endpoint is H4.

H4 — FULL-EVALUATION HARD ZERO
------------------------------

At:

    f = 1.00

and:

    UNBOUNDED

assert for EVERY intervention:

    outside-cone FORCE-only selected count == 0
    outside-cone PREVENT-only selected count == 0
    outside-cone symmetric difference == 0
    outside-cone exact expected effect == 0

Tolerance for floating arithmetic:

    1e-12

Any violation:

    INVALID_FULL_EVALUATION_CONTROL

This is an implementation/correctness condition, not a statistical result.

BREAKDOWN LOCATION
------------------

For each non-zero FCP class and budget fraction, compare:

    exact E_far

against the low-budget linear prediction extrapolated from f=0.10.

Define relative prediction error:

    |observed - predicted|
    /
    max(|predicted|, epsilon)

The first fraction where group-aggregated relative error exceeds:

    25%

is reported as the empirical breakdown point of the linear approximation.

This is descriptive unless the frozen low-budget H1 criterion fails.

NO DIFFERENT CRYSTALS PER B
---------------------------

This is non-negotiable.

Budget affects only lag-1 selection.

The checkpoint, intervention state and local geometry are frozen before the
budget sweep.

NO REALIZED BERNOULLI OUTCOME REQUIRED
--------------------------------------

Chapter 25 V1 is primarily an EXPECTATION / allocation mechanism experiment.

It does not need to threshold probabilities into noisy realized attachments to
identify the selector mechanism.

A later realized validation can be run only if this expectation-level law
earns one.

RAW OUTPUT
----------

Save every site × budget measurement to:

    raw-budget-sweep.jsonl
    raw-budget-sweep.csv

including:
    group
    cell
    FCP class
    actual DeltaF
    frontier sizes
    budget fraction
    effective B
    selected-set displacement
    exact E_ring1
    exact E_far
    exact E_global
    low-budget prediction
    prediction residual

CLAIM STATUS SPACE
------------------

Scientific hypotheses use:

    SUPPORTED
    BOUNDED
    UNRESOLVED
    INVALID

Hard code identities use:

    ASSERT / correctness control

They are never promoted into evidence because a bootstrap CI happened to be
zero-width.

STOP RULE
---------

Chapter 25 V1 asks whether finite evaluation capacity itself is the control
parameter for the non-local selector effect.

Do not rescue failure by:
    changing FCP levels
    changing n
    changing fraction grid
    changing the 25% residual criterion
    removing FCP=0
    removing the full-evaluation hard-zero arm

If low-budget linearity fails, report it and inspect the exact selector
combinatorics rather than tuning a new regression.

FRESH SEED
----------

Default:
    20260911

Previous:
    Ch24 V4 20260909
    Ch24 V5 20260910

DEPENDENCIES
------------

Requires beside this file:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
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

EXPERIMENT_VERSION = "digital-crystal-finite-budget-redistribution-v1"
SCHEMA_VERSION = 1
CHAPTER = 25
CHAPTER_TITLE = "How Does Finite Computation Create Non-Local Coupling?"

FRACTIONS = [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
LOW_BUDGET_FRACTIONS = [0.05, 0.10, 0.25]
FCP_LEVELS = [-1, 0, 1, 2]

FULL_ZERO_TOLERANCE = 1e-12
RELATIVE_RESIDUAL_TOLERANCE = 0.25
RATIO_TARGET = -2.0
RATIO_RELATIVE_TOLERANCE = 0.25


PROFILES = {
    "smoke": {
        "groups": 8,
        "source_profile": "smoke",
        "max_sites_per_fcp_per_group": 2,
        "bootstrap_reps": 500,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "source_profile": "quick",
        "max_sites_per_fcp_per_group": 3,
        "bootstrap_reps": 3000,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "source_profile": "standard",
        "max_sites_per_fcp_per_group": 4,
        "bootstrap_reps": 5000,
        "scientific": True,
    },
    "full": {
        "groups": 384,
        "source_profile": "full",
        "max_sites_per_fcp_per_group": 4,
        "bootstrap_reps": 7000,
        "scientific": True,
    },
}


# ============================================================================
# Statistics
# ============================================================================

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
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
    }


def bootstrap_ratio_ci(
    high_by_group: Dict[int, float],
    low_by_group: Dict[int, float],
    reps: int,
    seed: int,
) -> dict:
    common = sorted(
        set(high_by_group)
        & set(low_by_group)
    )

    if not common:
        return {
            "n_groups": 0,
            "ratio": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
            "relative_error_from_minus2": float("nan"),
        }

    high = np.asarray(
        [high_by_group[g] for g in common],
        dtype=float,
    )

    low = np.asarray(
        [low_by_group[g] for g in common],
        dtype=float,
    )

    mean_low = float(np.mean(low))

    ratio = (
        float(np.mean(high) / mean_low)
        if abs(mean_low) > 1e-15
        else float("nan")
    )

    rng = np.random.default_rng(seed)
    boot = []

    for _ in range(int(reps)):
        idx = rng.integers(
            0,
            len(common),
            size=len(common),
        )

        h = float(np.mean(high[idx]))
        l = float(np.mean(low[idx]))

        if abs(l) > 1e-15:
            boot.append(h / l)

    if boot:
        low_ci = float(np.quantile(boot, 0.025))
        high_ci = float(np.quantile(boot, 0.975))
    else:
        low_ci = float("nan")
        high_ci = float("nan")

    relative_error = (
        abs(ratio - RATIO_TARGET)
        / abs(RATIO_TARGET)
        if math.isfinite(ratio)
        else float("nan")
    )

    return {
        "n_groups": int(len(common)),
        "ratio": ratio,
        "ci95_low": low_ci,
        "ci95_high": high_ci,
        "target": RATIO_TARGET,
        "relative_error_from_minus2": float(relative_error),
        "within_25_percent_target": bool(
            math.isfinite(relative_error)
            and relative_error
            <= RATIO_RELATIVE_TOLERANCE
        ),
    }


# ============================================================================
# Frozen checkpoint/site preparation
# ============================================================================

@dataclass
class FrozenSite:
    group: int
    site_index: int
    cell: Cell
    fcp: int
    occupied_neighbors: int
    baseline_p: float
    radial_distance: int
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray


def choose_n1_sites(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    group: int,
    max_per_level: int,
) -> List[FrozenSite]:
    geometries = v4.evaluated_geometries(
        checkpoint,
        float(future_env[0]),
        source_profile,
        crystal_params,
    )

    by_fcp: Dict[int, List[v4.SiteGeometry]] = {
        level: []
        for level in FCP_LEVELS
    }

    for geometry in geometries:
        if geometry.occupied_neighbors != 1:
            continue

        if geometry.fcp not in by_fcp:
            continue

        by_fcp[geometry.fcp].append(geometry)

    # Deterministic sample: radial then cell.
    for level in by_fcp:
        by_fcp[level].sort(
            key=lambda g: (
                g.radial_distance,
                g.cell,
            )
        )

    out: List[FrozenSite] = []
    site_index = 0

    for level in FCP_LEVELS:
        for geometry in by_fcp[level][:max_per_level]:
            out.append(
                FrozenSite(
                    group=int(group),
                    site_index=int(site_index),
                    cell=geometry.cell,
                    fcp=int(geometry.fcp),
                    occupied_neighbors=int(
                        geometry.occupied_neighbors
                    ),
                    baseline_p=float(
                        geometry.baseline_p
                    ),
                    radial_distance=int(
                        geometry.radial_distance
                    ),
                    checkpoint=checkpoint,
                    future_env=future_env,
                )
            )
            site_index += 1

    return out


def prepare_sites(
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[List[FrozenSite], dict]:
    sites: List[FrozenSite] = []
    group_support: Dict[int, Dict[int, int]] = {}

    for group in tqdm(
        range(int(profile["groups"])),
        desc="Chapter 25 frozen checkpoints",
    ):
        checkpoint, future_env, _ = v4.build_checkpoint(
            source_profile,
            crystal_params,
            seed,
            group,
        )

        selected = choose_n1_sites(
            checkpoint,
            future_env,
            source_profile,
            crystal_params,
            group,
            int(
                profile[
                    "max_sites_per_fcp_per_group"
                ]
            ),
        )

        support = {
            level: 0
            for level in FCP_LEVELS
        }

        for site in selected:
            support[site.fcp] += 1
            sites.append(site)

        group_support[group] = support

    site_counts = {
        level: sum(
            site.fcp == level
            for site in sites
        )
        for level in FCP_LEVELS
    }

    groups_by_level = {
        level: sum(
            group_support[g][level] > 0
            for g in group_support
        )
        for level in FCP_LEVELS
    }

    payload = {
        "requested_groups": int(profile["groups"]),
        "total_sites": int(len(sites)),
        "site_counts_by_FCP": {
            str(k): int(v)
            for k, v in site_counts.items()
        },
        "groups_with_level": {
            str(k): int(v)
            for k, v in groups_by_level.items()
        },
        "supported_regime": "occupied_neighbors = 1",
    }

    return sites, payload


# ============================================================================
# Intervention state
# ============================================================================

@dataclass
class InterventionState:
    site: FrozenSite
    force_state: ch18.MaterialCrystalState
    prevent_state: ch18.MaterialCrystalState
    force_frontier: List[Cell]
    prevent_frontier: List[Cell]
    delta_frontier: int
    reference_frontier: int


def make_intervention_state(
    site: FrozenSite,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> InterventionState:
    checkpoint = site.checkpoint
    future_env = site.future_env

    radius = int(source_profile["radius"])
    intervention_budget = int(
        source_profile["budget"]
    )
    loss_rate = float(
        source_profile["loss_rate"]
    )

    force_grown, _, force_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        intervention_budget,
        force_cell=site.cell,
    )

    prevent_grown, _, prevent_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        intervention_budget,
        prevent_cell=site.cell,
    )

    if force_selected != prevent_selected:
        raise RuntimeError(
            "Intervention-step FORCE/PREVENT evaluated sets diverged "
            "before the intervention."
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    force_frontier = v4.frontier_cells(
        set(force_state.occupied),
        radius,
    )

    prevent_frontier = v4.frontier_cells(
        set(prevent_state.occupied),
        radius,
    )

    delta_frontier = (
        len(force_frontier)
        - len(prevent_frontier)
    )

    reference_frontier = max(
        len(force_frontier),
        len(prevent_frontier),
    )

    return InterventionState(
        site=site,
        force_state=force_state,
        prevent_state=prevent_state,
        force_frontier=force_frontier,
        prevent_frontier=prevent_frontier,
        delta_frontier=int(delta_frontier),
        reference_frontier=int(
            reference_frontier
        ),
    )


# ============================================================================
# Budget-sweep accounting
# ============================================================================

@dataclass
class SweepRow:
    group: int
    site_index: int
    q: int
    r: int
    fcp: int
    occupied_neighbors: int
    baseline_p: float

    budget_label: str
    requested_fraction: float | None
    effective_budget: int | None

    force_frontier_size: int
    prevent_frontier_size: int
    reference_frontier_size: int
    actual_delta_frontier: int

    force_evaluation_fraction: float
    prevent_evaluation_fraction: float

    far_shared_count: int
    far_force_only_count: int
    far_prevent_only_count: int
    far_symdiff_count: int
    far_jaccard: float

    shared_shift_far: float
    selector_swap_far: float
    E1_far: float

    shared_shift_ring1: float
    selector_swap_ring1: float
    E1_ring1: float

    shared_shift_global: float
    selector_swap_global: float
    E1_global: float

    low_budget_prediction_far: float
    prediction_residual_far: float


def select_with_budget(
    frontier: Sequence[Cell],
    state: ch18.MaterialCrystalState,
    budget: int | None,
) -> List[Cell]:
    if budget is None:
        # Explicit unbounded arm.
        return list(frontier)

    if budget >= len(frontier):
        # Full evaluation.
        return list(frontier)

    return ch21.select_candidates(
        list(frontier),
        int(budget),
        state.stream_seed,
        int(state.step + 1),
    )


def budget_for_fraction(
    reference_frontier: int,
    fraction: float,
) -> int:
    return max(
        1,
        int(
            math.ceil(
                fraction
                * reference_frontier
            )
        ),
    )


def accounting_for_budget(
    intervention: InterventionState,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    budget_label: str,
    requested_fraction: float | None,
    effective_budget: int | None,
) -> SweepRow:
    site = intervention.site
    x = site.cell
    next_input = float(
        site.future_env[1]
    )

    force_frontier = intervention.force_frontier
    prevent_frontier = intervention.prevent_frontier

    force_selected = select_with_budget(
        force_frontier,
        intervention.force_state,
        effective_budget,
    )

    prevent_selected = select_with_budget(
        prevent_frontier,
        intervention.prevent_state,
        effective_budget,
    )

    sf = set(force_selected)
    sp = set(prevent_selected)

    force_occ = set(
        intervention.force_state.occupied
    )
    prevent_occ = set(
        intervention.prevent_state.occupied
    )

    # Region accumulators.
    shared_far = 0.0
    swap_far = 0.0
    shared_ring1 = 0.0
    swap_ring1 = 0.0
    shared_global = 0.0
    swap_global = 0.0

    far_sf = {
        c
        for c in sf
        if v4.relative_distance(c, x) > 1
    }

    far_sp = {
        c
        for c in sp
        if v4.relative_distance(c, x) > 1
    }

    far_shared = far_sf & far_sp
    far_force_only = far_sf - far_sp
    far_prevent_only = far_sp - far_sf

    far_union = far_sf | far_sp

    far_jaccard = (
        1.0
        if not far_union
        else len(far_shared)
        / len(far_union)
    )

    # Shared cells.
    for cell in sf & sp:
        if cell == x:
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
        d = v4.relative_distance(
            cell,
            x,
        )

        shared_global += delta

        if d <= 1:
            shared_ring1 += delta
        else:
            shared_far += delta

    # FORCE-only cells.
    for cell in sf - sp:
        if cell == x:
            continue

        pf = v4.attachment_probability(
            cell,
            force_occ,
            next_input,
            crystal_params,
        )

        d = v4.relative_distance(
            cell,
            x,
        )

        swap_global += pf

        if d <= 1:
            swap_ring1 += pf
        else:
            swap_far += pf

    # PREVENT-only cells.
    for cell in sp - sf:
        if cell == x:
            continue

        pp = v4.attachment_probability(
            cell,
            prevent_occ,
            next_input,
            crystal_params,
        )

        d = v4.relative_distance(
            cell,
            x,
        )

        swap_global -= pp

        if d <= 1:
            swap_ring1 -= pp
        else:
            swap_far -= pp

    E_far = shared_far + swap_far
    E_ring1 = (
        shared_ring1
        + swap_ring1
    )
    E_global = (
        shared_global
        + swap_global
    )

    # Locality correctness assertion.
    if abs(shared_far) > FULL_ZERO_TOLERANCE:
        raise RuntimeError(
            f"Far shared probability shift violated locality: {shared_far}"
        )

    # First-order low-budget dilution model using the full PREVENT far frontier
    # probability mass and actual lag-1 DeltaF.
    Fp = len(
        prevent_frontier
    )

    if effective_budget is None:
        selection_rate = 1.0
    else:
        selection_rate = min(
            1.0,
            effective_budget
            / max(
                1,
                Fp,
            ),
        )

    prevent_far_probability_mass = 0.0

    for cell in prevent_frontier:
        if (
            cell == x
            or v4.relative_distance(
                cell,
                x,
            )
            <= 1
        ):
            continue

        prevent_far_probability_mass += (
            v4.attachment_probability(
                cell,
                prevent_occ,
                next_input,
                crystal_params,
            )
        )

    expected_prevent_far_sampled = (
        selection_rate
        * prevent_far_probability_mass
    )

    predicted = (
        -(
            intervention.delta_frontier
            / Fp
        )
        * expected_prevent_far_sampled
        if Fp > 0
        else 0.0
    )

    residual = (
        E_far
        - predicted
    )

    force_fraction = (
        len(force_selected)
        / len(force_frontier)
        if force_frontier
        else 1.0
    )

    prevent_fraction = (
        len(prevent_selected)
        / len(prevent_frontier)
        if prevent_frontier
        else 1.0
    )

    # Hard full-evaluation correctness controls.
    full_evaluation = (
        effective_budget is None
        or (
            effective_budget
            >= max(
                len(force_frontier),
                len(prevent_frontier),
            )
        )
    )

    if full_evaluation:
        if far_force_only:
            raise RuntimeError(
                "Full evaluation produced FORCE-only far cells."
            )

        if far_prevent_only:
            raise RuntimeError(
                "Full evaluation produced PREVENT-only far cells."
            )

        if abs(E_far) > FULL_ZERO_TOLERANCE:
            raise RuntimeError(
                f"Full evaluation outside-cone E_far != 0: {E_far}"
            )

    return SweepRow(
        group=int(site.group),
        site_index=int(
            site.site_index
        ),
        q=int(
            x[0]
        ),
        r=int(
            x[1]
        ),
        fcp=int(
            site.fcp
        ),
        occupied_neighbors=int(
            site.occupied_neighbors
        ),
        baseline_p=float(
            site.baseline_p
        ),
        budget_label=budget_label,
        requested_fraction=(
            None
            if requested_fraction is None
            else float(
                requested_fraction
            )
        ),
        effective_budget=(
            None
            if effective_budget is None
            else int(
                effective_budget
            )
        ),
        force_frontier_size=int(
            len(
                force_frontier
            )
        ),
        prevent_frontier_size=int(
            len(
                prevent_frontier
            )
        ),
        reference_frontier_size=int(
            intervention.reference_frontier
        ),
        actual_delta_frontier=int(
            intervention.delta_frontier
        ),
        force_evaluation_fraction=float(
            force_fraction
        ),
        prevent_evaluation_fraction=float(
            prevent_fraction
        ),
        far_shared_count=int(
            len(
                far_shared
            )
        ),
        far_force_only_count=int(
            len(
                far_force_only
            )
        ),
        far_prevent_only_count=int(
            len(
                far_prevent_only
            )
        ),
        far_symdiff_count=int(
            len(
                far_force_only
            )
            + len(
                far_prevent_only
            )
        ),
        far_jaccard=float(
            far_jaccard
        ),
        shared_shift_far=float(
            shared_far
        ),
        selector_swap_far=float(
            swap_far
        ),
        E1_far=float(
            E_far
        ),
        shared_shift_ring1=float(
            shared_ring1
        ),
        selector_swap_ring1=float(
            swap_ring1
        ),
        E1_ring1=float(
            E_ring1
        ),
        shared_shift_global=float(
            shared_global
        ),
        selector_swap_global=float(
            swap_global
        ),
        E1_global=float(
            E_global
        ),
        low_budget_prediction_far=float(
            predicted
        ),
        prediction_residual_far=float(
            residual
        ),
    )


# ============================================================================
# Run sweep
# ============================================================================

def run_sweep(
    sites: Sequence[FrozenSite],
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    List[SweepRow],
    dict,
]:
    rows: List[
        SweepRow
    ] = []

    full_control_count = 0

    for site in tqdm(
        sites,
        desc="Chapter 25 budget sweep",
    ):
        intervention = (
            make_intervention_state(
                site,
                source_profile,
                crystal_params,
            )
        )

        for fraction in FRACTIONS:
            B = budget_for_fraction(
                intervention.reference_frontier,
                fraction,
            )

            label = (
                f"f={fraction:.2f}"
            )

            row = accounting_for_budget(
                intervention,
                source_profile,
                crystal_params,
                label,
                fraction,
                B,
            )

            rows.append(
                row
            )

            if (
                fraction
                == 1.0
            ):
                full_control_count += 1

        # Explicit unbounded arm.
        rows.append(
            accounting_for_budget(
                intervention,
                source_profile,
                crystal_params,
                "unbounded",
                None,
                None,
            )
        )

        full_control_count += 1

    payload = {
        "sites": int(
            len(
                sites
            )
        ),
        "rows": int(
            len(
                rows
            )
        ),
        "fractions": FRACTIONS,
        "unbounded_arm": True,
        "hard_full_evaluation_controls_checked": int(
            full_control_count
        ),
        "status": "MEASURED",
    }

    return rows, payload


# ============================================================================
# Aggregation helpers
# ============================================================================

def rows_for(
    rows: Sequence[SweepRow],
    *,
    fcp: int | None = None,
    budget_label: str | None = None,
) -> List[SweepRow]:
    out = []

    for row in rows:
        if (
            fcp is not None
            and row.fcp != fcp
        ):
            continue

        if (
            budget_label is not None
            and row.budget_label
            != budget_label
        ):
            continue

        out.append(row)

    return out


def group_means(
    rows: Sequence[SweepRow],
    getter,
) -> Dict[int, float]:
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
                getter(
                    row
                )
            )
        )

    return {
        group: float(
            np.mean(
                values
            )
        )
        for group, values in buckets.items()
        if values
    }


def mean_by_group_values(
    mapping: Dict[int, float],
) -> List[float]:
    return [
        float(v)
        for _, v in sorted(
            mapping.items()
        )
    ]


# ============================================================================
# H1 low-budget -DeltaF scaling
# ============================================================================

def class_summary_at_budget(
    rows: Sequence[SweepRow],
    budget_label: str,
    bootstrap_reps: int,
    seed: int,
) -> dict:
    out = {}

    for index, level in enumerate(
        FCP_LEVELS
    ):
        subset = rows_for(
            rows,
            fcp=level,
            budget_label=budget_label,
        )

        e_by_group = group_means(
            subset,
            lambda r:
            r.E1_far,
        )

        dF_by_group = group_means(
            subset,
            lambda r:
            r.actual_delta_frontier,
        )

        sym_by_group = group_means(
            subset,
            lambda r:
            r.far_symdiff_count,
        )

        out[
            str(
                level
            )
        ] = {
            "groups": int(
                len(
                    e_by_group
                )
            ),
            "E_far": bootstrap_mean_ci(
                mean_by_group_values(
                    e_by_group
                ),
                bootstrap_reps,
                seed + index * 10,
            ),
            "actual_deltaF": bootstrap_mean_ci(
                mean_by_group_values(
                    dF_by_group
                ),
                bootstrap_reps,
                seed + index * 10 + 1,
            ),
            "far_symdiff": bootstrap_mean_ci(
                mean_by_group_values(
                    sym_by_group
                ),
                bootstrap_reps,
                seed + index * 10 + 2,
            ),
        }

    return out


def fit_class_linearity(
    summary: dict,
) -> dict:
    xs = []
    ys = []
    weights = []
    levels = []

    for level in (-1, 1, 2):
        row = summary[
            str(
                level
            )
        ]

        dF = float(
            row[
                "actual_deltaF"
            ][
                "mean"
            ]
        )

        e = float(
            row[
                "E_far"
            ][
                "mean"
            ]
        )

        n = int(
            row[
                "groups"
            ]
        )

        if (
            not math.isfinite(
                dF
            )
            or not math.isfinite(
                e
            )
            or abs(
                dF
            )
            < 1e-12
            or n == 0
        ):
            continue

        xs.append(
            -dF
        )
        ys.append(
            e
        )
        weights.append(
            n
        )
        levels.append(
            level
        )

    if len(
        xs
    ) < 2:
        return {
            "status": "INSUFFICIENT_CLASS_SUPPORT"
        }

    x = np.asarray(
        xs,
        dtype=float,
    )

    y = np.asarray(
        ys,
        dtype=float,
    )

    w = np.asarray(
        weights,
        dtype=float,
    )

    denom = float(
        np.sum(
            w
            * x
            * x
        )
    )

    beta = (
        float(
            np.sum(
                w
                * x
                * y
            )
            / denom
        )
        if denom > 0
        else float(
            "nan"
        )
    )

    predicted = beta * x
    residual = y - predicted

    weighted_abs_resid = float(
        np.sum(
            w
            * np.abs(
                residual
            )
        )
        / np.sum(
            w
        )
    )

    weighted_abs_pred = float(
        np.sum(
            w
            * np.abs(
                predicted
            )
        )
        / np.sum(
            w
        )
    )

    relative_residual = (
        weighted_abs_resid
        / weighted_abs_pred
        if weighted_abs_pred > 1e-15
        else float(
            "inf"
        )
    )

    # Weighted through-origin R² relative to zero model.
    sse = float(
        np.sum(
            w
            * residual
            * residual
        )
    )

    sst0 = float(
        np.sum(
            w
            * y
            * y
        )
    )

    r2_origin = (
        1.0
        - sse
        / sst0
        if sst0 > 0
        else float(
            "nan"
        )
    )

    per_class = {}

    for level, xx, yy, pp in zip(
        levels,
        x,
        y,
        predicted,
    ):
        per_class[
            str(
                level
            )
        ] = {
            "minus_mean_deltaF": float(
                xx
            ),
            "observed_E_far": float(
                yy
            ),
            "predicted_E_far": float(
                pp
            ),
            "relative_residual": float(
                abs(
                    yy - pp
                )
                / max(
                    abs(
                        pp
                    ),
                    1e-12,
                )
            ),
        }

    return {
        "beta_through_origin": float(
            beta
        ),
        "R2_through_origin": float(
            r2_origin
        ),
        "weighted_mean_absolute_residual": float(
            weighted_abs_resid
        ),
        "weighted_mean_absolute_predicted_magnitude": float(
            weighted_abs_pred
        ),
        "relative_residual": float(
            relative_residual
        ),
        "passes_25_percent_relative_residual": bool(
            relative_residual
            <= RELATIVE_RESIDUAL_TOLERANCE
        ),
        "classes": per_class,
    }


# ============================================================================
# Ratio test
# ============================================================================

def extreme_ratio_at_budget(
    rows: Sequence[SweepRow],
    budget_label: str,
    reps: int,
    seed: int,
) -> dict:
    high = group_means(
        rows_for(
            rows,
            fcp=2,
            budget_label=budget_label,
        ),
        lambda r:
        r.E1_far,
    )

    low = group_means(
        rows_for(
            rows,
            fcp=-1,
            budget_label=budget_label,
        ),
        lambda r:
        r.E1_far,
    )

    return bootstrap_ratio_ci(
        high,
        low,
        reps,
        seed,
    )


# ============================================================================
# Budget saturation / breakdown
# ============================================================================

def budget_breakdown(
    summaries: Dict[str, dict],
) -> dict:
    out = {}

    reference_label = "f=0.10"

    for level in (-1, 1, 2):
        ref = float(
            summaries[
                reference_label
            ][
                str(
                    level
                )
            ][
                "E_far"
            ][
                "mean"
            ]
        )

        points = []
        breakdown = None

        for fraction in FRACTIONS:
            label = (
                f"f={fraction:.2f}"
            )

            observed = float(
                summaries[
                    label
                ][
                    str(
                        level
                    )
                ][
                    "E_far"
                ][
                    "mean"
                ]
            )

            # Low-budget linear extrapolation from f=0.10:
            # selector effect approximately proportional to f.
            predicted = (
                ref
                * (
                    fraction
                    / 0.10
                )
            )

            relative_error = (
                abs(
                    observed
                    - predicted
                )
                / max(
                    abs(
                        predicted
                    ),
                    1e-12,
                )
            )

            points.append({
                "fraction": float(
                    fraction
                ),
                "observed_E_far": float(
                    observed
                ),
                "linear_extrapolation_from_0.10": float(
                    predicted
                ),
                "relative_error": float(
                    relative_error
                ),
            })

            if (
                breakdown is None
                and fraction > 0.10
                and relative_error
                > RELATIVE_RESIDUAL_TOLERANCE
            ):
                breakdown = float(
                    fraction
                )

        out[
            str(
                level
            )
        ] = {
            "reference_E_far_at_0.10": float(
                ref
            ),
            "first_fraction_exceeding_25_percent_error": (
                breakdown
            ),
            "points": points,
        }

    return out


# ============================================================================
# Raw output / reporting
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
            / "ch25-finite-budget-redistribution-v1-full-report.md"
        )

        parts = [
            "# Chapter 25 — How Does Finite Computation Create Non-Local Coupling? (V1)",
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


def write_raw(
    reporter: Reporter,
    rows: Sequence[SweepRow],
) -> None:
    jsonl = (
        reporter.root
        / "raw-budget-sweep.jsonl"
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
        / "raw-budget-sweep.csv"
    )

    if not rows:
        return

    fields = list(
        asdict(
            rows[0]
        ).keys()
    )

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
            writer.writerow(
                asdict(
                    row
                )
            )


# ============================================================================
# Main analysis
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
        default=20260911,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch25-finite-budget-redistribution-v1"
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
        "chapter_title": (
            CHAPTER_TITLE
        ),
        "profile": args.profile,
        "profile_config": profile,
        "source_checkpoint_profile": (
            source_profile
        ),
        "seed": int(
            args.seed
        ),
        "fresh_seed": bool(
            int(
                args.seed
            )
            not in {
                20260909,
                20260910,
            }
        ),
        "fractions": FRACTIONS,
        "low_budget_fractions": (
            LOW_BUDGET_FRACTIONS
        ),
        "supported_n": 1,
        "started_at_unix": float(
            time.time()
        ),
    }

    protocol = {
        "role": (
            "FINITE-BUDGET CONTROL-PARAMETER EXPERIMENT"
        ),
        "same_checkpoint_across_budget_arms": True,
        "same_intervention_state_across_budget_arms": True,
        "budget_varies_only_at_lag1": True,
        "control_parameter": (
            "B / max(F_force, F_prevent)"
        ),
        "fractions": FRACTIONS,
        "unbounded_arm": True,
        "primary_region": (
            "outside nearest-neighbour causal cone: d > 1 at lag 1"
        ),
        "supported_scope": (
            "occupied_neighbors = 1"
        ),
        "FCP_levels": FCP_LEVELS,
        "H1": {
            "claim": (
                "Low-budget outside-cone E_far scales with -DeltaF"
            ),
            "fractions": (
                LOW_BUDGET_FRACTIONS
            ),
            "relative_residual_tolerance": (
                RELATIVE_RESIDUAL_TOLERANCE
            ),
        },
        "extreme_ratio": {
            "FCP_levels": [
                2,
                -1,
            ],
            "target": (
                RATIO_TARGET
            ),
            "relative_tolerance": (
                RATIO_RELATIVE_TOLERANCE
            ),
        },
        "FCP0_control": (
            "composition substitution with size change removed"
        ),
        "full_evaluation_control": {
            "f=1.00": (
                "hard outside-cone zero"
            ),
            "unbounded": (
                "hard outside-cone zero"
            ),
            "tolerance": (
                FULL_ZERO_TOLERANCE
            ),
        },
        "scientific": bool(
            profile[
                "scientific"
            ]
        ),
        "status": (
            "FROZEN"
            if profile[
                "scientific"
            ]
            else "ENGINEERING_SMOKE_ONLY"
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 25 V1 Protocol",
        protocol,
    )

    reporter.json(
        "stage-00-protocol.json",
        protocol,
    )

    sites, support = prepare_sites(
        profile,
        source_profile,
        crystal_params,
        args.seed,
    )

    reporter.stage(
        "stage-01-site-support.md",
        "Stage 1 — Frozen n=1 Site Support",
        support,
    )

    reporter.json(
        "stage-01-site-support.json",
        support,
    )

    if not sites:
        raise RuntimeError(
            "No supported n=1 sites."
        )

    rows, sweep_info = run_sweep(
        sites,
        source_profile,
        crystal_params,
    )

    reporter.stage(
        "stage-02-budget-sweep.md",
        "Stage 2 — Same-Checkpoint Budget Sweep",
        sweep_info,
    )

    reporter.json(
        "stage-02-budget-sweep.json",
        sweep_info,
    )

    write_raw(
        reporter,
        rows,
    )

    # Summaries for every finite fraction and unbounded.
    summaries: Dict[
        str,
        dict,
    ] = {}

    for idx, fraction in enumerate(
        FRACTIONS
    ):
        label = (
            f"f={fraction:.2f}"
        )

        summaries[
            label
        ] = class_summary_at_budget(
            rows,
            label,
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed
            + 1000
            + idx
            * 100,
        )

    summaries[
        "unbounded"
    ] = class_summary_at_budget(
        rows,
        "unbounded",
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        args.seed
        + 2000,
    )

    reporter.stage(
        "stage-03-class-summaries.md",
        "Stage 3 — FCP-Class Far-Field Effects by Budget Fraction",
        summaries,
    )

    reporter.json(
        "stage-03-class-summaries.json",
        summaries,
    )

    # H1 linearity.
    linearity = {}

    for fraction in (
        LOW_BUDGET_FRACTIONS
    ):
        label = (
            f"f={fraction:.2f}"
        )

        linearity[
            label
        ] = fit_class_linearity(
            summaries[
                label
            ]
        )

    H1_supported = bool(
        all(
            result.get(
                "passes_25_percent_relative_residual",
                False,
            )
            for result in linearity.values()
        )
    )

    linearity_payload = {
        "fractions": linearity,
        "relative_residual_tolerance": (
            RELATIVE_RESIDUAL_TOLERANCE
        ),
        "status": (
            "SUPPORTED"
            if H1_supported
            else "UNRESOLVED"
        ),
    }

    reporter.stage(
        "stage-04-low-budget-linearity.md",
        "Stage 4 — Low-Budget -DeltaF Scaling",
        linearity_payload,
    )

    reporter.json(
        "stage-04-low-budget-linearity.json",
        linearity_payload,
    )

    # Parameter-free extreme ratio.
    ratios = {}

    for idx, fraction in enumerate(
        LOW_BUDGET_FRACTIONS
    ):
        label = (
            f"f={fraction:.2f}"
        )

        ratios[
            label
        ] = extreme_ratio_at_budget(
            rows,
            label,
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed
            + 3000
            + idx
            * 100,
        )

    ratio_supported = bool(
        all(
            result.get(
                "within_25_percent_target",
                False,
            )
            for result in ratios.values()
        )
    )

    ratio_payload = {
        "target_ratio": (
            RATIO_TARGET
        ),
        "relative_tolerance": (
            RATIO_RELATIVE_TOLERANCE
        ),
        "fractions": ratios,
        "status": (
            "SUPPORTED"
            if ratio_supported
            else "UNRESOLVED"
        ),
    }

    reporter.stage(
        "stage-05-extreme-ratio.md",
        "Stage 5 — Parameter-Free FCP +2 : -1 Ratio",
        ratio_payload,
    )

    reporter.json(
        "stage-05-extreme-ratio.json",
        ratio_payload,
    )

    # FCP=0 composition-only control.
    fcp0 = {}

    for idx, fraction in enumerate(
        FRACTIONS
    ):
        label = (
            f"f={fraction:.2f}"
        )

        subset = rows_for(
            rows,
            fcp=0,
            budget_label=label,
        )

        fcp0[
            label
        ] = {
            "actual_deltaF": bootstrap_mean_ci(
                mean_by_group_values(
                    group_means(
                        subset,
                        lambda r:
                        r.actual_delta_frontier,
                    )
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 4000
                + idx
                * 20,
            ),
            "far_symdiff": bootstrap_mean_ci(
                mean_by_group_values(
                    group_means(
                        subset,
                        lambda r:
                        r.far_symdiff_count,
                    )
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 4001
                + idx
                * 20,
            ),
            "E_far": bootstrap_mean_ci(
                mean_by_group_values(
                    group_means(
                        subset,
                        lambda r:
                        r.E1_far,
                    )
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 4002
                + idx
                * 20,
            ),
        }

    reporter.stage(
        "stage-06-fcp0-composition-control.md",
        "Stage 6 — FCP=0 Composition-Only Control",
        fcp0,
    )

    reporter.json(
        "stage-06-fcp0-composition-control.json",
        fcp0,
    )

    # Saturation / breakdown.
    breakdown = budget_breakdown(
        summaries
    )

    reporter.stage(
        "stage-07-budget-saturation.md",
        "Stage 7 — Breakdown of the Low-Budget Linear Approximation",
        breakdown,
    )

    reporter.json(
        "stage-07-budget-saturation.json",
        breakdown,
    )

    # Hard endpoint is already asserted per intervention. Summarize measured
    # full/unbounded means.
    hard_zero = {
        "f=1.00": summaries[
            "f=1.00"
        ],
        "unbounded": summaries[
            "unbounded"
        ],
        "assertion": (
            "Every intervention passed exact outside-cone zero controls."
        ),
        "tolerance": (
            FULL_ZERO_TOLERANCE
        ),
        "status": (
            "PASS"
        ),
    }

    reporter.stage(
        "stage-08-full-evaluation-hard-zero.md",
        "Stage 8 — Full-Evaluation Hard-Zero Correctness Control",
        hard_zero,
    )

    reporter.json(
        "stage-08-full-evaluation-hard-zero.json",
        hard_zero,
    )

    if not profile[
        "scientific"
    ]:
        overall = (
            "ENGINEERING_SMOKE_ONLY"
        )

        bounded = (
            "Smoke profile completed. No scientific interpretation is eligible."
        )

    elif (
        H1_supported
        and ratio_supported
    ):
        overall = (
            "FINITE_BUDGET_REDISTRIBUTION_CONTROL_PARAMETER_SUPPORTED"
        )

        bounded = (
            "Within the frozen n=1 Digital Crystal regime, low-budget lag-1 "
            "outside-cone expected construction followed the predeclared "
            "-DeltaF scaling within the relative residual tolerance, including "
            "the parameter-free FCP +2 versus -1 ratio calibration. The "
            "selector-mediated far-field effect vanished exactly when the "
            "entire frontier was evaluated."
        )

    elif H1_supported:
        overall = (
            "LOW_BUDGET_SCALING_SUPPORTED_EXTREME_RATIO_UNRESOLVED"
        )

        bounded = (
            "Low-budget outside-cone effects followed the broader -DeltaF "
            "scaling criterion, but the parameter-free extreme-class ratio did "
            "not clear its frozen tolerance at every low-budget fraction."
        )

    else:
        overall = (
            "FINITE_BUDGET_SCALING_UNRESOLVED"
        )

        bounded = (
            "The hard full-evaluation zero control passed, but the predeclared "
            "low-budget -DeltaF scaling law did not clear its frozen relative "
            "residual criterion."
        )

    verdict = {
        "overall_status": overall,
        "bounded_claim": bounded,
        "H1_low_budget_linearity": (
            linearity_payload[
                "status"
            ]
        ),
        "extreme_ratio": (
            ratio_payload[
                "status"
            ]
        ),
        "full_evaluation_hard_zero": (
            "PASS"
        ),
        "next_if_supported": (
            "Use the measured breakdown curve as the finite-computation "
            "control law, then ask whether changing this control parameter "
            "changes downstream causal amplification / branching behaviour."
        ),
        "next_if_unresolved": (
            "Inspect exact finite-sampling combinatorics and composition "
            "substitution. Do not retune the FCP classes or fraction grid."
        ),
        "stop_rule": (
            "No rescue by changing the frozen fraction grid, FCP levels, n, "
            "or 25% residual criterion."
        ),
    }

    reporter.stage(
        "stage-09-verdict.md",
        "Stage 9 — Bounded Chapter 25 V1 Verdict",
        verdict,
    )

    reporter.json(
        "stage-09-verdict.json",
        verdict,
    )

    metadata[
        "finished_at_unix"
    ] = float(
        time.time()
    )

    metadata[
        "final_status"
    ] = overall

    reporter.json(
        "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()
    print("=" * 78)
    print(f"FINAL STATUS: {overall}")
    print(bounded)
    print(f"Report: {report}")
    print("=" * 78)


if __name__ == "__main__":
    main()
