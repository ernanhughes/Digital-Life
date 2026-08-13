#!/usr/bin/env python3
"""
Digital Life — Chapter 26 V2
Does Candidate Subsampling Change Causal Amplification
When Background Construction Is Matched Dynamically?
==========================================================================

WHY V2 EXISTS
-------------

Chapter 26 V1 successfully matched expected construction at lag 1, but its
audit showed that the fixed calibration offset did not preserve matching over
the full H=12 continuation.

V1 therefore established:

    initial expected construction matched

but NOT:

    background expected construction matched over the whole trajectory

The V1 audit also showed that f=1.00 was not dynamically exhaustive because its
absolute B was frozen from an earlier frontier size. The true exhaustive arm
was the explicit UNBOUNDED arm.

V2 fixes both issues.

SCIENTIFIC QUESTION
-------------------

At dynamically matched background expected construction rate:

    does strong candidate subsampling change finite-horizon
    transient causal amplification relative to true exhaustive evaluation?

PRIMARY CONTRAST
----------------

    G_T(f=0.10) - G_T(unbounded)

Frozen SEI:

    +/- 0.15 attachments

Primary status:

    SUPPORTED
        if |mean| >= 0.15,
        CI excludes 0,
        achieved MDE80 <= 0.15

    BOUNDED_NEAR_ZERO
        if entire 95% CI lies inside [-0.15, +0.15]
        and achieved MDE80 <= 0.15

    UNRESOLVED
        otherwise

    INVALID
        if dynamic construction-rate matching fails

This is TWO-SIDED.

We do not assume whether stronger subsampling increases or suppresses causal
amplification.

CORE DESIGN
-----------

For every independent group:

    SAME checkpoint
    SAME n=1 probe site
    SAME FORCE/PREVENT intervention
    SAME post-intervention FORCE/PREVENT states
    SAME future environment
    SAME cell-keyed randomness

Only the continuation allocation policy changes.

Arms:

    f=0.10          primary strong-subsampling arm
    f=0.25          secondary
    f=0.50          secondary
    f=0.75          secondary
    fixed-f=1.00    secondary high fixed-budget arm, NOT called exhaustive
    unbounded       PRIMARY exhaustive reference

TRUE UNBOUNDED
--------------

The unbounded arm evaluates the entire CURRENT frontier independently at every
lag.

Therefore it remains dynamically exhaustive as the frontier evolves.

The fixed-f=1.00 arm keeps an absolute B derived from the initial continuation
frontier. It is retained as a mechanism arm only.

It is NOT called exhaustive.

COMMON INTERVENTION
-------------------

The FORCE/PREVENT perturbation is generated ONCE using the frozen Chapter 24
intervention mechanics:

    intervention budget = 96
    base attachment rule
    same selected set before intervention
    ordinary background loss

Every continuation arm starts from clones of those exact same post-intervention
states.

The budget manipulation does not change the causal perturbation itself.

DYNAMIC BACKGROUND-RATE MATCHING
--------------------------------

This is the V2 change.

At EVERY continuation lag tau:

1. Each arm has a PREVENT state and a FORCE state.

2. Define a common population-level construction target C_target(tau) from a
   dedicated REFERENCE PREVENT trajectory.

3. The reference policy is:

       f_ref = 0.10
       base attachment calibration offset = 0

   and it is propagated as its own PREVENT-only state using the canonical
   calibrated rule.

4. C_target(tau) is the exact expected attachment count on that reference
   PREVENT state at that lag.

5. For every continuation arm independently:
   - compute its CURRENT PREVENT frontier
   - compute its CURRENT selected candidate set for that arm
   - solve ONE additive score offset so that PREVENT expected attachments
     match C_target(tau)
   - apply that SAME offset to the corresponding FORCE branch

The FORCE branch is NOT independently calibrated.

Why?

If FORCE and PREVENT were separately tuned to the same target, part of the
causal response itself would be mechanically erased.

Instead:

    PREVENT establishes the background construction policy
    SAME offset is applied to FORCE
    FORCE-PREVENT causal differences remain free to emerge

MATCHING VALIDITY
-----------------

Frozen tolerance:

    2% relative error

At every lag, for every arm, PREVENT expected construction must satisfy:

    |E_prevent - C_target| / C_target <= 0.02

Scientific validity requires BOTH:

    >= 95% of group x probe x arm x lag records within 2%

AND

    population-mean PREVENT relative error for EVERY arm x lag
    within +/- 2%

If either gate fails:

    INVALID_DYNAMIC_RATE_MATCH

The FORCE branch is reported but NOT required to equal target because its
difference from PREVENT is part of the causal response.

REFERENCE-TARGET TRAJECTORY
---------------------------

The target trajectory is not a global fixed number.

It may naturally rise or fall as the reference PREVENT crystal evolves.

This avoids V1's mistake of trying to preserve the lag-1 absolute target
through a changing morphology.

What is matched is:

    construction policy across arms at the same lag

not:

    one constant attachment count forever

PRIMARY OUTCOME
---------------

Transient finite-horizon causal gain:

    G_T(H)

with:

    H = 12

Definition:

    cumulative FORCE-minus-PREVENT realized attachments
    within distance 1..H from x
    across lags 1..H
    excluding x

The transient FORCE cell is removed after lag 1 if still occupied.

INFERENCE UNIT
--------------

Probe sites within a checkpoint are repeated measures.

For inference:

    average probes within group
    then infer across independent groups

Never treat individual probes as independent scientific replicates.

SECONDARY MEASUREMENTS
----------------------

Per arm:

    G_T local
    G_T global
    P(G_T != 0)
    E[G_T | G_T != 0]

    exact E1_ring1
    exact E1_far
    exact E1_global

    realized lag-1 divergence

    per-lag PREVENT expected construction
    per-lag FORCE expected construction
    per-lag target
    per-lag calibration offset

    selected-set Jaccard
    selected-set symmetric difference

    frontier size
    selected count

CROSS-ARM RATE MATCH
--------------------

For every lag, report the population-mean PREVENT expected construction for
all arms.

This is the direct audit that V1 was missing.

NO RATIO ESTIMATOR
------------------

Do NOT use:

    G_T / E1

V1 showed that ratio estimates become unstable when E1 approaches zero.

NO BRANCHING-RATIO CLAIM
------------------------

G_T is a finite-horizon causal amplification measure.

It is NOT a formal branching ratio.

Do not call it:

    subcritical
    supercritical
    critical

unless a later experiment establishes descendant semantics and a proper
branching process.

PROBE REGIME
------------

Use the supported single-contact frontier regime:

    occupied_neighbors = 1

Select up to 4 deterministic spread probes per group.

Do not choose probes by FCP.

Chapter 26 is testing an allocation control parameter, not searching for
another geometry class.

FROZEN PROFILES
---------------

smoke:
    8 groups
    2 probes/group
    engineering only

quick:
    48 groups
    4 probes/group

standard:
    96 groups
    4 probes/group

full:
    192 groups
    4 probes/group
    intended scientific run

FRESH SEED
----------

Default V2 seed:

    20260913

Previous:
    Ch24 V4 20260909
    Ch24 V5 20260910
    Ch25 V1 20260911
    Ch26 V1 20260912

V1 and its audit remain historical evidence.

V2 is a new preregistered experiment with a fresh independent seed.

STOP RULE
---------

If the primary is BOUNDED_NEAR_ZERO:

    close the amplification question at the frozen +/-0.15 scale
    for this tested regime.

Do not rescue by changing:
    SEI
    horizon
    probe geometry
    budget fractions
    target reference policy
    dynamic calibration method

If SUPPORTED:

    proceed to map the amplification effect over allocation concentration.

If UNRESOLVED only because achieved MDE > SEI:

    increase independent groups without changing the effect definition.

If INVALID:

    fix only the matching implementation, not the scientific hypothesis.

RAW OUTPUT
----------

Save:

    raw-v2-arm-results.jsonl
    raw-v2-arm-results.csv

and:

    raw-v2-per-lag.jsonl
    raw-v2-per-lag.csv

so the matching trajectory can be audited without replay.

DEPENDENCIES
------------

Requires beside this file:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_matched_rate_causal_amplification_v1.py

The V1 module is reused for stable helpers only. V2 owns its scientific
protocol and reporting.
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
import ch26_digital_crystal_matched_rate_causal_amplification_v1 as v1


Cell = Tuple[int, int]

EXPERIMENT_VERSION = (
    "digital-crystal-dynamically-matched-rate-causal-amplification-v2"
)
SCHEMA_VERSION = 2
CHAPTER = 26
CHAPTER_TITLE = (
    "Does Candidate Subsampling Change Causal Amplification?"
)

FRACTIONS = [0.10, 0.25, 0.50, 0.75, 1.00]
REFERENCE_FRACTION = 0.10
HORIZON = 12

INTERVENTION_BUDGET = 96
PRIMARY_SEI = 0.15

MATCH_TOLERANCE = 0.02
MIN_RECORD_MATCH_FRACTION = 0.95

CALIBRATION_OFFSET_MIN = -12.0
CALIBRATION_OFFSET_MAX = 12.0
CALIBRATION_TOLERANCE = 1e-10
CALIBRATION_MAX_ITER = 100

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

PROFILES = {
    "smoke": {
        "groups": 8,
        "source_profile": "smoke",
        "probes_per_group": 2,
        "bootstrap_reps": 500,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "source_profile": "quick",
        "probes_per_group": 4,
        "bootstrap_reps": 3000,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "source_profile": "standard",
        "probes_per_group": 4,
        "bootstrap_reps": 5000,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "source_profile": "full",
        "probes_per_group": 4,
        "bootstrap_reps": 7000,
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

    sd = (
        float(np.std(arr, ddof=1))
        if len(arr) > 1
        else 0.0
    )

    se = (
        sd / math.sqrt(len(arr))
        if len(arr)
        else float("nan")
    )

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
        "achieved_mde80_one_sided": float(
            se
            * (
                Z_95_ONE_SIDED
                + Z_80_POWER
            )
        ),
    }


def primary_status(
    summary: dict,
    valid: bool,
) -> str:
    if not valid:
        return "INVALID"

    if (
        summary[
            "achieved_mde80_one_sided"
        ]
        > PRIMARY_SEI
    ):
        return "UNRESOLVED"

    low = float(summary["ci95_low"])
    high = float(summary["ci95_high"])
    mean = float(summary["mean"])

    if (
        low > -PRIMARY_SEI
        and high < PRIMARY_SEI
    ):
        return "BOUNDED_NEAR_ZERO"

    if (
        abs(mean) >= PRIMARY_SEI
        and (
            low > 0.0
            or high < 0.0
        )
    ):
        return "SUPPORTED"

    return "UNRESOLVED"


# ============================================================================
# State helpers
# ============================================================================

def clone_state(
    state: ch18.MaterialCrystalState,
) -> ch18.MaterialCrystalState:
    return ch18.MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(
            state.attachments_by_step
        ),
        population_by_step=list(
            state.population_by_step
        ),
        modified_count_by_step=list(
            state.modified_count_by_step
        ),
    )


# ============================================================================
# Calibrated probability
# ============================================================================

def attachment_score(
    cell: Cell,
    occupied_before: Set[Cell],
    input_value: float,
    crystal_params: ch18.CrystalParams,
) -> float:
    n = sum(
        nb in occupied_before
        for nb in ch18.neighbors(cell)
    )

    theta = ch18.local_exposure_angle(
        cell,
        occupied_before,
    )

    phase = (
        crystal_params.signal_phase_gain
        * float(input_value)
    )

    anisotropy = math.cos(
        6.0 * theta
        + phase
    )

    crowding = max(
        0,
        n - 2,
    )

    return float(
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain * float(input_value)
        + crystal_params.anisotropy_gain * anisotropy
        - crystal_params.crowding_penalty * crowding
    )


def calibrated_probability(
    cell: Cell,
    occupied_before: Set[Cell],
    input_value: float,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    return float(
        ch18.logistic_scalar(
            attachment_score(
                cell,
                occupied_before,
                input_value,
                crystal_params,
            )
            + offset
        )
    )


# ============================================================================
# Candidate selection
# ============================================================================

def select_candidates(
    frontier: Sequence[Cell],
    state: ch18.MaterialCrystalState,
    budget: int | None,
) -> List[Cell]:
    if budget is None:
        return list(frontier)

    if budget >= len(frontier):
        return list(frontier)

    return ch21.select_candidates(
        list(frontier),
        int(budget),
        state.stream_seed,
        int(state.step + 1),
    )


def budget_from_fraction(
    frontier_size: int,
    fraction: float,
) -> int:
    return max(
        1,
        int(
            math.ceil(
                float(fraction)
                * frontier_size
            )
        ),
    )


# ============================================================================
# Expected construction and dynamic calibration
# ============================================================================

def expected_selected_attachments(
    state: ch18.MaterialCrystalState,
    input_value: float,
    selected: Sequence[Cell],
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    occupied = set(state.occupied)

    return float(
        sum(
            calibrated_probability(
                cell,
                occupied,
                input_value,
                crystal_params,
                offset,
            )
            for cell in selected
        )
    )


def solve_offset(
    state: ch18.MaterialCrystalState,
    input_value: float,
    selected: Sequence[Cell],
    crystal_params: ch18.CrystalParams,
    target: float,
) -> Tuple[float, float, bool]:
    if not selected:
        return (
            0.0,
            0.0,
            abs(target)
            <= CALIBRATION_TOLERANCE,
        )

    lo = CALIBRATION_OFFSET_MIN
    hi = CALIBRATION_OFFSET_MAX

    e_lo = expected_selected_attachments(
        state,
        input_value,
        selected,
        crystal_params,
        lo,
    )

    e_hi = expected_selected_attachments(
        state,
        input_value,
        selected,
        crystal_params,
        hi,
    )

    if (
        target < e_lo
        or target > e_hi
    ):
        return (
            float("nan"),
            float("nan"),
            False,
        )

    for _ in range(
        CALIBRATION_MAX_ITER
    ):
        mid = (
            lo + hi
        ) / 2.0

        e_mid = expected_selected_attachments(
            state,
            input_value,
            selected,
            crystal_params,
            mid,
        )

        if (
            abs(
                e_mid
                - target
            )
            <= CALIBRATION_TOLERANCE
        ):
            return (
                float(mid),
                float(e_mid),
                True,
            )

        if e_mid < target:
            lo = mid
        else:
            hi = mid

    offset = (
        lo + hi
    ) / 2.0

    achieved = expected_selected_attachments(
        state,
        input_value,
        selected,
        crystal_params,
        offset,
    )

    return (
        float(offset),
        float(achieved),
        True,
    )


# ============================================================================
# Growth
# ============================================================================

def calibrated_growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
]:
    occupied_before = set(state.occupied)
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier = v4.frontier_cells(
        occupied_before,
        radius,
    )

    selected = select_candidates(
        frontier,
        state,
        budget,
    )

    next_step = int(
        state.step + 1
    )

    additions = []

    for cell in selected:
        p = calibrated_probability(
            cell,
            occupied_before,
            input_value,
            crystal_params,
            offset,
        )

        if (
            ch18.cell_uniform(
                state.stream_seed,
                next_step,
                cell,
            )
            < p
        ):
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    out = ch18.MaterialCrystalState(
        occupied=occupied,
        birth_time=birth_time,
        modified=set(),
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=(
            list(state.attachments_by_step)
            + [len(additions)]
        ),
        population_by_step=(
            list(state.population_by_step)
            + [len(occupied)]
        ),
        modified_count_by_step=(
            list(state.modified_count_by_step)
            + [0]
        ),
    )

    return out, additions, selected


def calibrated_canonical_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
    loss_rate: float,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
    List[Cell],
]:
    grown, additions, selected = (
        calibrated_growth_step(
            state,
            input_value,
            radius,
            crystal_params,
            budget,
            offset,
        )
    )

    after_loss, lost = (
        ch21.apply_background_loss(
            grown,
            loss_rate,
        )
    )

    return (
        after_loss,
        additions,
        lost,
        selected,
    )


# ============================================================================
# Checkpoint / probe preparation
# ============================================================================

@dataclass
class Probe:
    group: int
    probe_index: int
    cell: Cell
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray


def choose_probes(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    group: int,
    max_probes: int,
) -> List[Probe]:
    geometries = v4.evaluated_geometries(
        checkpoint,
        float(future_env[0]),
        source_profile,
        crystal_params,
    )

    candidates = [
        g
        for g in geometries
        if g.occupied_neighbors == 1
    ]

    candidates.sort(
        key=lambda g: (
            g.radial_distance,
            g.cell,
        )
    )

    if len(candidates) <= max_probes:
        chosen = candidates
    else:
        indices = np.linspace(
            0,
            len(candidates) - 1,
            num=max_probes,
        )

        chosen = [
            candidates[
                int(round(idx))
            ]
            for idx in indices
        ]

    return [
        Probe(
            group=int(group),
            probe_index=int(i),
            cell=g.cell,
            checkpoint=checkpoint,
            future_env=future_env,
        )
        for i, g in enumerate(chosen)
    ]


def prepare_probes(
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[List[Probe], dict]:
    probes = []
    counts = []

    for group in tqdm(
        range(int(profile["groups"])),
        desc="Chapter 26 V2 checkpoints",
    ):
        checkpoint, future_env, _ = (
            v4.build_checkpoint(
                source_profile,
                crystal_params,
                seed,
                group,
            )
        )

        selected = choose_probes(
            checkpoint,
            future_env,
            source_profile,
            crystal_params,
            group,
            int(
                profile[
                    "probes_per_group"
                ]
            ),
        )

        counts.append(
            len(selected)
        )

        probes.extend(selected)

    groups_with_probes = sum(
        c > 0
        for c in counts
    )

    return probes, {
        "requested_groups": int(
            profile["groups"]
        ),
        "groups_with_probes": int(
            groups_with_probes
        ),
        "coverage_fraction": float(
            groups_with_probes
            / max(
                1,
                int(
                    profile["groups"]
                ),
            )
        ),
        "total_probes": int(
            len(probes)
        ),
        "probe_count_distribution": {
            "min": int(min(counts))
            if counts
            else 0,
            "median": float(
                np.median(counts)
            )
            if counts
            else 0.0,
            "max": int(max(counts))
            if counts
            else 0,
        },
        "supported_scope": (
            "occupied_neighbors = 1"
        ),
    }


# ============================================================================
# Common FORCE/PREVENT intervention
# ============================================================================

@dataclass
class PreparedIntervention:
    probe: Probe
    force_state: ch18.MaterialCrystalState
    prevent_state: ch18.MaterialCrystalState


def prepare_common_intervention(
    probe: Probe,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> PreparedIntervention:
    radius = int(
        source_profile["radius"]
    )

    loss_rate = float(
        source_profile["loss_rate"]
    )

    checkpoint = probe.checkpoint
    x = probe.cell

    force_grown, _, force_selected, _ = (
        v4.growth_step(
            checkpoint,
            float(probe.future_env[0]),
            radius,
            crystal_params,
            INTERVENTION_BUDGET,
            force_cell=x,
        )
    )

    prevent_grown, _, prevent_selected, _ = (
        v4.growth_step(
            checkpoint,
            float(probe.future_env[0]),
            radius,
            crystal_params,
            INTERVENTION_BUDGET,
            prevent_cell=x,
        )
    )

    if force_selected != prevent_selected:
        raise RuntimeError(
            "FORCE/PREVENT intervention selected sets diverged."
        )

    force_state, _ = (
        ch21.apply_background_loss(
            force_grown,
            loss_rate,
        )
    )

    prevent_state, _ = (
        ch21.apply_background_loss(
            prevent_grown,
            loss_rate,
        )
    )

    return PreparedIntervention(
        probe=probe,
        force_state=force_state,
        prevent_state=prevent_state,
    )


# ============================================================================
# Reference PREVENT target trajectory
# ============================================================================

@dataclass
class ReferenceLagTarget:
    lag: int
    target: float
    state_before: ch18.MaterialCrystalState
    state_after: ch18.MaterialCrystalState
    budget: int
    frontier_size: int
    selected_count: int
    realized_attachments: int


def build_reference_targets(
    prepared: PreparedIntervention,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[ReferenceLagTarget]:
    """
    Dedicated PREVENT-only reference trajectory.

    Policy:
        f_ref = 0.10
        base offset = 0

    This trajectory defines C_target(tau).
    """
    state = clone_state(
        prepared.prevent_state
    )

    radius = int(
        source_profile["radius"]
    )

    loss_rate = float(
        source_profile["loss_rate"]
    )

    targets = []

    for lag in range(
        1,
        HORIZON + 1,
    ):
        input_value = float(
            prepared.probe.future_env[
                lag
            ]
        )

        frontier = v4.frontier_cells(
            set(state.occupied),
            radius,
        )

        budget = budget_from_fraction(
            len(frontier),
            REFERENCE_FRACTION,
        )

        selected = select_candidates(
            frontier,
            state,
            budget,
        )

        target = (
            expected_selected_attachments(
                state,
                input_value,
                selected,
                crystal_params,
                0.0,
            )
        )

        before = clone_state(state)

        (
            state,
            additions,
            _lost,
            selected_actual,
        ) = calibrated_canonical_step(
            state,
            input_value,
            radius,
            crystal_params,
            budget,
            0.0,
            loss_rate,
        )

        if selected != selected_actual:
            raise RuntimeError(
                "Reference selected set mismatch."
            )

        targets.append(
            ReferenceLagTarget(
                lag=int(lag),
                target=float(target),
                state_before=before,
                state_after=clone_state(
                    state
                ),
                budget=int(budget),
                frontier_size=int(
                    len(frontier)
                ),
                selected_count=int(
                    len(selected)
                ),
                realized_attachments=int(
                    len(additions)
                ),
            )
        )

    return targets


# ============================================================================
# Exact E1 diagnostics
# ============================================================================

def exact_expectation_difference(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    input_value: float,
    x: Cell,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
) -> dict:
    force_frontier = v4.frontier_cells(
        set(force_state.occupied),
        radius,
    )

    prevent_frontier = v4.frontier_cells(
        set(prevent_state.occupied),
        radius,
    )

    force_selected = select_candidates(
        force_frontier,
        force_state,
        budget,
    )

    prevent_selected = select_candidates(
        prevent_frontier,
        prevent_state,
        budget,
    )

    sf = set(force_selected)
    sp = set(prevent_selected)

    force_occ = set(
        force_state.occupied
    )

    prevent_occ = set(
        prevent_state.occupied
    )

    E_ring1 = 0.0
    E_far = 0.0
    E_global = 0.0

    for cell in sf | sp:
        if cell == x:
            continue

        pf = (
            calibrated_probability(
                cell,
                force_occ,
                input_value,
                crystal_params,
                offset,
            )
            if cell in sf
            else 0.0
        )

        pp = (
            calibrated_probability(
                cell,
                prevent_occ,
                input_value,
                crystal_params,
                offset,
            )
            if cell in sp
            else 0.0
        )

        delta = pf - pp

        d = v4.relative_distance(
            cell,
            x,
        )

        E_global += delta

        if d <= 1:
            E_ring1 += delta
        else:
            E_far += delta

    union = sf | sp

    return {
        "E1_ring1": float(
            E_ring1
        ),
        "E1_far": float(
            E_far
        ),
        "E1_global": float(
            E_global
        ),
        "selected_jaccard": (
            1.0
            if not union
            else float(
                len(sf & sp)
                / len(union)
            )
        ),
        "selected_symdiff": int(
            len(sf ^ sp)
        ),
    }


# ============================================================================
# Arm execution
# ============================================================================

@dataclass
class PerLagRow:
    group: int
    probe_index: int
    budget_label: str
    fraction: float | None
    lag: int

    target_expected_attachments: float
    offset: float
    calibration_valid: bool

    prevent_frontier_size: int
    force_frontier_size: int
    prevent_selected_count: int
    force_selected_count: int

    prevent_expected_attachments: float
    force_expected_attachments: float
    prevent_relative_error: float
    force_relative_difference_from_target: float

    prevent_realized_attachments: int
    force_realized_attachments: int

    selected_jaccard: float
    selected_symdiff: int


@dataclass
class ArmResult:
    group: int
    probe_index: int
    q: int
    r: int

    budget_label: str
    fraction: float | None

    G_local: float
    G_global: float
    G_nonzero: int

    E1_ring1: float
    E1_far: float
    E1_global: float

    lag1_realized_divergence: int

    mean_selected_jaccard: float
    mean_selected_symdiff: float

    all_lags_calibrated: bool
    max_prevent_relative_error: float
    mean_abs_prevent_relative_error: float


def arm_budget(
    prevent_frontier_size: int,
    fraction: float | None,
) -> int | None:
    if fraction is None:
        return None

    return budget_from_fraction(
        prevent_frontier_size,
        fraction,
    )


def run_arm(
    prepared: PreparedIntervention,
    reference_targets: Sequence[ReferenceLagTarget],
    fraction: float | None,
    label: str,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    ArmResult,
    List[PerLagRow],
]:
    probe = prepared.probe
    x = probe.cell

    radius = int(
        source_profile["radius"]
    )

    loss_rate = float(
        source_profile["loss_rate"]
    )

    force_state = clone_state(
        prepared.force_state
    )

    prevent_state = clone_state(
        prepared.prevent_state
    )

    local_total = 0.0
    global_total = 0.0
    lag1_divergence = 0

    lag_rows = []
    jaccards = []
    symdiffs = []
    prevent_abs_errors = []

    E1 = None
    all_valid = True

    for lag in range(
        1,
        HORIZON + 1,
    ):
        input_value = float(
            probe.future_env[lag]
        )

        target = float(
            reference_targets[
                lag - 1
            ].target
        )

        prevent_frontier = (
            v4.frontier_cells(
                set(
                    prevent_state.occupied
                ),
                radius,
            )
        )

        force_frontier = (
            v4.frontier_cells(
                set(
                    force_state.occupied
                ),
                radius,
            )
        )

        budget = arm_budget(
            len(
                prevent_frontier
            ),
            fraction,
        )

        prevent_selected = (
            select_candidates(
                prevent_frontier,
                prevent_state,
                budget,
            )
        )

        (
            offset,
            prevent_expected,
            solved,
        ) = solve_offset(
            prevent_state,
            input_value,
            prevent_selected,
            crystal_params,
            target,
        )

        prevent_rel_error = (
            abs(
                prevent_expected
                - target
            )
            / max(
                target,
                1e-12,
            )
            if solved
            else float(
                "inf"
            )
        )

        calibration_valid = bool(
            solved
            and prevent_rel_error
            <= MATCH_TOLERANCE
        )

        if not calibration_valid:
            all_valid = False

        if not solved:
            offset = 0.0

        force_selected = (
            select_candidates(
                force_frontier,
                force_state,
                budget,
            )
        )

        force_expected = (
            expected_selected_attachments(
                force_state,
                input_value,
                force_selected,
                crystal_params,
                offset,
            )
        )

        force_rel_from_target = (
            (
                force_expected
                - target
            )
            / max(
                target,
                1e-12,
            )
        )

        if lag == 1:
            E1 = (
                exact_expectation_difference(
                    force_state,
                    prevent_state,
                    input_value,
                    x,
                    radius,
                    crystal_params,
                    budget,
                    offset,
                )
            )

        (
            force_state,
            force_add,
            _force_lost,
            force_selected_actual,
        ) = calibrated_canonical_step(
            force_state,
            input_value,
            radius,
            crystal_params,
            budget,
            offset,
            loss_rate,
        )

        (
            prevent_state,
            prevent_add,
            _prevent_lost,
            prevent_selected_actual,
        ) = calibrated_canonical_step(
            prevent_state,
            input_value,
            radius,
            crystal_params,
            budget,
            offset,
            loss_rate,
        )

        if (
            force_selected
            != force_selected_actual
        ):
            raise RuntimeError(
                "FORCE selected-set mismatch."
            )

        if (
            prevent_selected
            != prevent_selected_actual
        ):
            raise RuntimeError(
                "PREVENT selected-set mismatch."
            )

        force_add_set = {
            c
            for c in force_add
            if c != x
        }

        prevent_add_set = {
            c
            for c in prevent_add
            if c != x
        }

        force_local = sum(
            1
            <= v4.relative_distance(
                c,
                x,
            )
            <= HORIZON
            for c in force_add_set
        )

        prevent_local = sum(
            1
            <= v4.relative_distance(
                c,
                x,
            )
            <= HORIZON
            for c in prevent_add_set
        )

        local_total += float(
            force_local
            - prevent_local
        )

        global_total += float(
            len(force_add_set)
            - len(prevent_add_set)
        )

        sf = set(
            force_selected
        )

        sp = set(
            prevent_selected
        )

        union = sf | sp

        jaccard = (
            1.0
            if not union
            else len(
                sf & sp
            )
            / len(
                union
            )
        )

        symdiff = len(
            sf ^ sp
        )

        jaccards.append(
            float(jaccard)
        )

        symdiffs.append(
            float(symdiff)
        )

        if lag == 1:
            f_local_set = {
                c
                for c in force_add_set
                if 1
                <= v4.relative_distance(
                    c,
                    x,
                )
                <= HORIZON
            }

            p_local_set = {
                c
                for c in prevent_add_set
                if 1
                <= v4.relative_distance(
                    c,
                    x,
                )
                <= HORIZON
            }

            lag1_divergence = int(
                f_local_set
                != p_local_set
            )

        lag_rows.append(
            PerLagRow(
                group=int(
                    probe.group
                ),
                probe_index=int(
                    probe.probe_index
                ),
                budget_label=label,
                fraction=(
                    None
                    if fraction is None
                    else float(
                        fraction
                    )
                ),
                lag=int(lag),
                target_expected_attachments=float(
                    target
                ),
                offset=float(
                    offset
                ),
                calibration_valid=bool(
                    calibration_valid
                ),
                prevent_frontier_size=int(
                    len(
                        prevent_frontier
                    )
                ),
                force_frontier_size=int(
                    len(
                        force_frontier
                    )
                ),
                prevent_selected_count=int(
                    len(
                        prevent_selected
                    )
                ),
                force_selected_count=int(
                    len(
                        force_selected
                    )
                ),
                prevent_expected_attachments=float(
                    prevent_expected
                ),
                force_expected_attachments=float(
                    force_expected
                ),
                prevent_relative_error=float(
                    (
                        prevent_expected
                        - target
                    )
                    / max(
                        target,
                        1e-12,
                    )
                ),
                force_relative_difference_from_target=float(
                    force_rel_from_target
                ),
                prevent_realized_attachments=int(
                    len(
                        [
                            c
                            for c in prevent_add
                            if c != x
                        ]
                    )
                ),
                force_realized_attachments=int(
                    len(
                        [
                            c
                            for c in force_add
                            if c != x
                        ]
                    )
                ),
                selected_jaccard=float(
                    jaccard
                ),
                selected_symdiff=int(
                    symdiff
                ),
            )
        )

        prevent_abs_errors.append(
            float(
                abs(
                    (
                        prevent_expected
                        - target
                    )
                    / max(
                        target,
                        1e-12,
                    )
                )
            )
        )

        # transient intervention semantics
        if (
            lag == 1
            and x
            in force_state.occupied
        ):
            force_state.occupied.remove(
                x
            )

            force_state.birth_time.pop(
                x,
                None,
            )

            if (
                force_state.population_by_step
            ):
                force_state.population_by_step[
                    -1
                ] = len(
                    force_state.occupied
                )

    if E1 is None:
        raise RuntimeError(
            "Missing lag-1 expectation diagnostics."
        )

    result = ArmResult(
        group=int(
            probe.group
        ),
        probe_index=int(
            probe.probe_index
        ),
        q=int(
            x[0]
        ),
        r=int(
            x[1]
        ),
        budget_label=label,
        fraction=(
            None
            if fraction is None
            else float(
                fraction
            )
        ),
        G_local=float(
            local_total
        ),
        G_global=float(
            global_total
        ),
        G_nonzero=int(
            abs(
                local_total
            )
            > 0.0
        ),
        E1_ring1=float(
            E1[
                "E1_ring1"
            ]
        ),
        E1_far=float(
            E1[
                "E1_far"
            ]
        ),
        E1_global=float(
            E1[
                "E1_global"
            ]
        ),
        lag1_realized_divergence=int(
            lag1_divergence
        ),
        mean_selected_jaccard=float(
            np.mean(
                jaccards
            )
        ),
        mean_selected_symdiff=float(
            np.mean(
                symdiffs
            )
        ),
        all_lags_calibrated=bool(
            all_valid
        ),
        max_prevent_relative_error=float(
            max(
                prevent_abs_errors
            )
            if prevent_abs_errors
            else float(
                "nan"
            )
        ),
        mean_abs_prevent_relative_error=float(
            np.mean(
                prevent_abs_errors
            )
            if prevent_abs_errors
            else float(
                "nan"
            )
        ),
    )

    return result, lag_rows


# ============================================================================
# Aggregation
# ============================================================================

def group_means(
    rows: Sequence[ArmResult],
    label: str,
    getter,
) -> Dict[int, float]:
    buckets: Dict[
        int,
        List[float],
    ] = {}

    for row in rows:
        if (
            row.budget_label
            != label
        ):
            continue

        value = float(
            getter(row)
        )

        if not math.isfinite(
            value
        ):
            continue

        buckets.setdefault(
            row.group,
            [],
        ).append(
            value
        )

    return {
        group: float(
            np.mean(values)
        )
        for group, values
        in buckets.items()
        if values
    }


def paired_group_difference(
    rows: Sequence[ArmResult],
    label_a: str,
    label_b: str,
    getter,
) -> List[float]:
    a = group_means(
        rows,
        label_a,
        getter,
    )

    b = group_means(
        rows,
        label_b,
        getter,
    )

    common = sorted(
        set(a)
        & set(b)
    )

    return [
        float(
            a[g]
            - b[g]
        )
        for g in common
    ]


def group_lag_values(
    rows: Sequence[PerLagRow],
    label: str,
    lag: int,
    getter,
) -> List[float]:
    buckets: Dict[
        int,
        List[float],
    ] = {}

    for row in rows:
        if (
            row.budget_label
            != label
            or row.lag
            != lag
        ):
            continue

        value = float(
            getter(row)
        )

        if not math.isfinite(
            value
        ):
            continue

        buckets.setdefault(
            row.group,
            [],
        ).append(
            value
        )

    return [
        float(
            np.mean(values)
        )
        for _, values
        in sorted(
            buckets.items()
        )
        if values
    ]


# ============================================================================
# Dynamic matching validity
# ============================================================================

def matching_validity(
    lag_rows: Sequence[PerLagRow],
) -> dict:
    labels = [
        f"f={f:.2f}"
        for f in FRACTIONS
    ] + [
        "unbounded"
    ]

    all_record_flags = [
        bool(
            row.calibration_valid
        )
        for row in lag_rows
    ]

    record_pass_fraction = (
        float(
            np.mean(
                all_record_flags
            )
        )
        if all_record_flags
        else 0.0
    )

    per_arm_lag = {}

    population_gate = True

    for label in labels:
        per_arm_lag[
            label
        ] = {}

        for lag in range(
            1,
            HORIZON + 1,
        ):
            vals = group_lag_values(
                lag_rows,
                label,
                lag,
                lambda r:
                r.prevent_relative_error,
            )

            mean = (
                float(
                    np.mean(vals)
                )
                if vals
                else float(
                    "nan"
                )
            )

            within = bool(
                math.isfinite(mean)
                and abs(mean)
                <= MATCH_TOLERANCE
            )

            if not within:
                population_gate = False

            per_arm_lag[
                label
            ][
                str(lag)
            ] = {
                "n_groups": int(
                    len(vals)
                ),
                "mean_prevent_relative_error": float(
                    mean
                ),
                "within_2pct": bool(
                    within
                ),
            }

    valid = bool(
        record_pass_fraction
        >= MIN_RECORD_MATCH_FRACTION
        and population_gate
    )

    return {
        "record_level_pass_fraction": float(
            record_pass_fraction
        ),
        "required_record_pass_fraction": float(
            MIN_RECORD_MATCH_FRACTION
        ),
        "population_mean_every_arm_lag_within_2pct": bool(
            population_gate
        ),
        "per_arm_lag": per_arm_lag,
        "status": (
            "PASS"
            if valid
            else "FAIL"
        ),
        "scientific_valid": bool(
            valid
        ),
    }


# ============================================================================
# Reporting
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
            / "ch26-dynamically-matched-rate-causal-amplification-v2-full-report.md"
        )

        parts = [
            "# Chapter 26 — Dynamically Matched Causal Amplification (V2)",
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
            "\n".join(parts),
            encoding="utf-8",
        )

        return path


def write_raw_dataclasses(
    path_jsonl: Path,
    path_csv: Path,
    rows,
) -> None:
    with path_jsonl.open(
        "w",
        encoding="utf-8",
    ) as f:
        for row in rows:
            f.write(
                json.dumps(
                    asdict(row)
                )
                + "\n"
            )

    if not rows:
        return

    fields = list(
        asdict(
            rows[0]
        ).keys()
    )

    with path_csv.open(
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
                asdict(row)
            )


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
        default=20260913,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch26-dynamically-matched-rate-causal-amplification-v2"
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

    source_profile[
        "horizon"
    ] = HORIZON

    crystal_params = (
        ch18.CrystalParams()
    )

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
                20260911,
                20260912,
            }
        ),
        "fractions": FRACTIONS,
        "reference_fraction": (
            REFERENCE_FRACTION
        ),
        "horizon": HORIZON,
        "primary_SEI": (
            PRIMARY_SEI
        ),
        "match_tolerance": (
            MATCH_TOLERANCE
        ),
        "started_at_unix": float(
            time.time()
        ),
    }

    protocol = {
        "role": (
            "DYNAMICALLY MATCHED BACKGROUND CONSTRUCTION-RATE "
            "CAUSAL AMPLIFICATION TEST"
        ),
        "question": (
            "At dynamically matched background expected construction rate, "
            "does strong candidate subsampling change finite-horizon causal "
            "amplification relative to true exhaustive evaluation?"
        ),
        "primary_contrast": (
            "G_T(f=0.10) - G_T(unbounded)"
        ),
        "primary_SEI_abs": (
            PRIMARY_SEI
        ),
        "two_sided": True,
        "same_checkpoint_across_arms": True,
        "same_probe_across_arms": True,
        "same_post_intervention_states_across_arms": True,
        "intervention_budget": (
            INTERVENTION_BUDGET
        ),
        "dynamic_matching": {
            "reference_policy": (
                "dedicated PREVENT-only f=0.10 trajectory, base offset 0"
            ),
            "target": (
                "lag-specific exact expected attachments from reference PREVENT"
            ),
            "arm_calibration": (
                "solve offset on each arm's PREVENT state every lag; "
                "apply same offset to FORCE"
            ),
            "relative_tolerance": (
                MATCH_TOLERANCE
            ),
            "minimum_record_pass_fraction": (
                MIN_RECORD_MATCH_FRACTION
            ),
            "population_mean_every_arm_lag_must_pass": True,
        },
        "arms": {
            "f=0.10": "primary strong-subsampling arm",
            "f=0.25": "secondary",
            "f=0.50": "secondary",
            "f=0.75": "secondary",
            "f=1.00": (
                "secondary fixed-budget arm; NOT dynamically exhaustive"
            ),
            "unbounded": (
                "primary true exhaustive reference"
            ),
        },
        "supported_probe_scope": (
            "occupied_neighbors = 1"
        ),
        "forbidden_overclaims": [
            "formal branching ratio",
            "subcritical",
            "supercritical",
            "critical point",
            "phase transition",
            "directed percolation",
            "coherent structure",
            "individuality",
            "organism",
            "life",
        ],
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
        "Stage 0 — Frozen Chapter 26 V2 Protocol",
        protocol,
    )

    reporter.json(
        "stage-00-protocol.json",
        protocol,
    )

    probes, support = (
        prepare_probes(
            profile,
            source_profile,
            crystal_params,
            args.seed,
        )
    )

    reporter.stage(
        "stage-01-probe-support.md",
        "Stage 1 — Probe Support",
        support,
    )

    reporter.json(
        "stage-01-probe-support.json",
        support,
    )

    if not probes:
        raise RuntimeError(
            "No supported probes."
        )

    arm_results = []
    lag_rows = []

    arm_defs = [
        ("f=0.10", 0.10),
        ("f=0.25", 0.25),
        ("f=0.50", 0.50),
        ("f=0.75", 0.75),
        ("f=1.00", 1.00),
        ("unbounded", None),
    ]

    for probe in tqdm(
        probes,
        desc="Chapter 26 V2 dynamic arms",
    ):
        prepared = (
            prepare_common_intervention(
                probe,
                source_profile,
                crystal_params,
            )
        )

        reference_targets = (
            build_reference_targets(
                prepared,
                source_profile,
                crystal_params,
            )
        )

        for label, fraction in arm_defs:
            result, per_lag = (
                run_arm(
                    prepared,
                    reference_targets,
                    fraction,
                    label,
                    source_profile,
                    crystal_params,
                )
            )

            arm_results.append(
                result
            )

            lag_rows.extend(
                per_lag
            )

    write_raw_dataclasses(
        reporter.root
        / "raw-v2-arm-results.jsonl",
        reporter.root
        / "raw-v2-arm-results.csv",
        arm_results,
    )

    write_raw_dataclasses(
        reporter.root
        / "raw-v2-per-lag.jsonl",
        reporter.root
        / "raw-v2-per-lag.csv",
        lag_rows,
    )

    validity = (
        matching_validity(
            lag_rows
        )
    )

    probe_coverage_valid = bool(
        support[
            "coverage_fraction"
        ]
        >= 0.90
    )

    scientific_valid = bool(
        validity[
            "scientific_valid"
        ]
        and probe_coverage_valid
    )

    validity_payload = {
        "dynamic_matching": validity,
        "probe_coverage_fraction": float(
            support[
                "coverage_fraction"
            ]
        ),
        "probe_coverage_valid": bool(
            probe_coverage_valid
        ),
        "scientific_valid": bool(
            scientific_valid
        ),
    }

    reporter.stage(
        "stage-02-dynamic-rate-validity.md",
        "Stage 2 — Dynamic Construction-Rate Matching Validity",
        validity_payload,
    )

    reporter.json(
        "stage-02-dynamic-rate-validity.json",
        validity_payload,
    )

    # Per-arm summary.
    arm_profiles = {}

    for idx, (
        label,
        fraction,
    ) in enumerate(
        arm_defs
    ):
        def gm(getter):
            mapping = group_means(
                arm_results,
                label,
                getter,
            )

            return [
                value
                for _, value
                in sorted(
                    mapping.items()
                )
            ]

        subset = [
            r
            for r in arm_results
            if r.budget_label
            == label
        ]

        raw_G = np.asarray(
            [
                r.G_local
                for r in subset
            ],
            dtype=float,
        )

        nz = raw_G[
            np.abs(
                raw_G
            )
            > 0
        ]

        arm_profiles[
            label
        ] = {
            "fraction": fraction,
            "groups": int(
                len(
                    set(
                        r.group
                        for r in subset
                    )
                )
            ),
            "probes": int(
                len(subset)
            ),
            "G_local": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.G_local
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 100
                + idx * 30,
            ),
            "G_global": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.G_global
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 101
                + idx * 30,
            ),
            "E1_ring1": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.E1_ring1
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 102
                + idx * 30,
            ),
            "E1_far": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.E1_far
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 103
                + idx * 30,
            ),
            "lag1_realized_divergence": (
                bootstrap_mean_ci(
                    gm(
                        lambda r:
                        r.lag1_realized_divergence
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 104
                    + idx * 30,
                )
            ),
            "G_nonzero_rate": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.G_nonzero
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 105
                + idx * 30,
            ),
            "conditional_G_given_nonzero": {
                "n_all": int(
                    len(raw_G)
                ),
                "n_nonzero": int(
                    len(nz)
                ),
                "nonzero_fraction": float(
                    len(nz)
                    / max(
                        1,
                        len(raw_G),
                    )
                ),
                "mean_given_nonzero": (
                    float(
                        np.mean(nz)
                    )
                    if len(nz)
                    else float(
                        "nan"
                    )
                ),
            },
            "mean_selected_jaccard": (
                bootstrap_mean_ci(
                    gm(
                        lambda r:
                        r.mean_selected_jaccard
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 106
                    + idx * 30,
                )
            ),
            "mean_selected_symdiff": (
                bootstrap_mean_ci(
                    gm(
                        lambda r:
                        r.mean_selected_symdiff
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 107
                    + idx * 30,
                )
            ),
            "max_prevent_relative_error": (
                bootstrap_mean_ci(
                    gm(
                        lambda r:
                        r.max_prevent_relative_error
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 108
                    + idx * 30,
                )
            ),
        }

    reporter.stage(
        "stage-03-arm-profiles.md",
        "Stage 3 — Dynamically Matched Arm Profiles",
        arm_profiles,
    )

    reporter.json(
        "stage-03-arm-profiles.json",
        arm_profiles,
    )

    # Primary contrast.
    primary_delta = (
        paired_group_difference(
            arm_results,
            "f=0.10",
            "unbounded",
            lambda r:
            r.G_local,
        )
    )

    primary_summary = (
        bootstrap_mean_ci(
            primary_delta,
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed + 5000,
        )
    )

    if not profile[
        "scientific"
    ]:
        p_status = (
            "ENGINEERING_SMOKE_ONLY"
        )
    else:
        p_status = primary_status(
            primary_summary,
            scientific_valid,
        )

    primary_payload = {
        "contrast": (
            "G_T(f=0.10) - G_T(unbounded)"
        ),
        "SEI_abs": (
            PRIMARY_SEI
        ),
        "result": (
            primary_summary
        ),
        "status": (
            p_status
        ),
    }

    reporter.stage(
        "stage-04-primary-test.md",
        "Stage 4 — Primary Strong-Subsampling vs True-Unbounded Test",
        primary_payload,
    )

    reporter.json(
        "stage-04-primary-test.json",
        primary_payload,
    )

    # Secondary contrasts.
    secondary = {}

    for idx, (
        label,
        _fraction,
    ) in enumerate(
        arm_defs[
            :-1
        ]
    ):
        secondary[
            label
        ] = {
            "G_local_minus_unbounded": (
                bootstrap_mean_ci(
                    paired_group_difference(
                        arm_results,
                        label,
                        "unbounded",
                        lambda r:
                        r.G_local,
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 6000
                    + idx * 50,
                )
            ),
            "E1_ring1_minus_unbounded": (
                bootstrap_mean_ci(
                    paired_group_difference(
                        arm_results,
                        label,
                        "unbounded",
                        lambda r:
                        r.E1_ring1,
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 6001
                    + idx * 50,
                )
            ),
            "E1_far_minus_unbounded": (
                bootstrap_mean_ci(
                    paired_group_difference(
                        arm_results,
                        label,
                        "unbounded",
                        lambda r:
                        r.E1_far,
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 6002
                    + idx * 50,
                )
            ),
            "G_nonzero_rate_minus_unbounded": (
                bootstrap_mean_ci(
                    paired_group_difference(
                        arm_results,
                        label,
                        "unbounded",
                        lambda r:
                        r.G_nonzero,
                    ),
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 6003
                    + idx * 50,
                )
            ),
        }

    reporter.stage(
        "stage-05-secondary-contrasts.md",
        "Stage 5 — Secondary Allocation-Concentration Contrasts",
        secondary,
    )

    reporter.json(
        "stage-05-secondary-contrasts.json",
        secondary,
    )

    # Per-lag matching summaries.
    lag_summary = {}

    labels = [
        label
        for label, _
        in arm_defs
    ]

    for lag in range(
        1,
        HORIZON + 1,
    ):
        lag_summary[
            str(lag)
        ] = {}

        arm_means = []

        for label in labels:
            prevent_vals = (
                group_lag_values(
                    lag_rows,
                    label,
                    lag,
                    lambda r:
                    r.prevent_expected_attachments,
                )
            )

            target_vals = (
                group_lag_values(
                    lag_rows,
                    label,
                    lag,
                    lambda r:
                    r.target_expected_attachments,
                )
            )

            force_vals = (
                group_lag_values(
                    lag_rows,
                    label,
                    lag,
                    lambda r:
                    r.force_expected_attachments,
                )
            )

            prevent_summary = (
                bootstrap_mean_ci(
                    prevent_vals,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10000
                    + lag * 100
                    + labels.index(
                        label
                    ) * 3,
                )
            )

            target_summary = (
                bootstrap_mean_ci(
                    target_vals,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10001
                    + lag * 100
                    + labels.index(
                        label
                    ) * 3,
                )
            )

            force_summary = (
                bootstrap_mean_ci(
                    force_vals,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10002
                    + lag * 100
                    + labels.index(
                        label
                    ) * 3,
                )
            )

            lag_summary[
                str(lag)
            ][
                label
            ] = {
                "target": target_summary,
                "prevent_expected": (
                    prevent_summary
                ),
                "force_expected": (
                    force_summary
                ),
            }

            arm_means.append(
                float(
                    prevent_summary[
                        "mean"
                    ]
                )
            )

        values = np.asarray(
            arm_means,
            dtype=float,
        )

        lag_summary[
            str(lag)
        ][
            "cross_arm_prevent_dispersion"
        ] = {
            "range": float(
                np.max(values)
                - np.min(values)
            ),
            "relative_range": float(
                (
                    np.max(values)
                    - np.min(values)
                )
                / np.mean(values)
            )
            if np.mean(values)
            != 0
            else float(
                "nan"
            ),
            "cv": float(
                np.std(values)
                / np.mean(values)
            )
            if np.mean(values)
            != 0
            else float(
                "nan"
            ),
        }

    reporter.stage(
        "stage-06-per-lag-matching.md",
        "Stage 6 — Per-Lag Background Construction Matching",
        lag_summary,
    )

    reporter.json(
        "stage-06-per-lag-matching.json",
        lag_summary,
    )

    # Verdict.
    if not profile[
        "scientific"
    ]:
        overall = (
            "ENGINEERING_SMOKE_ONLY"
        )

        bounded = (
            "Smoke profile completed. No scientific interpretation is eligible."
        )

    elif not scientific_valid:
        overall = (
            "INVALID_DYNAMIC_RATE_MATCH"
        )

        bounded = (
            "The dynamically matched background-construction validity gate "
            "failed, so no causal-amplification verdict is eligible."
        )

    elif p_status == "SUPPORTED":
        overall = (
            "CANDIDATE_SUBSAMPLING_CHANGES_CAUSAL_AMPLIFICATION"
        )

        direction = (
            "greater"
            if primary_summary[
                "mean"
            ]
            > 0
            else "lower"
        )

        bounded = (
            "At dynamically matched background expected construction rate, "
            f"the f=0.10 strong-subsampling arm produced {direction} "
            "finite-horizon transient causal amplification than true "
            "unbounded evaluation by at least the frozen meaningful scale."
        )

    elif (
        p_status
        == "BOUNDED_NEAR_ZERO"
    ):
        overall = (
            "CAUSAL_AMPLIFICATION_BOUNDED_NEAR_ZERO_AT_MATCHED_RATE"
        )

        bounded = (
            "At dynamically matched background expected construction rate, "
            "the strong-subsampling versus true-unbounded difference in "
            "finite-horizon transient causal amplification was bounded within "
            "the frozen +/-0.15 attachment equivalence region."
        )

    else:
        overall = (
            "DYNAMICALLY_MATCHED_CAUSAL_AMPLIFICATION_UNRESOLVED"
        )

        bounded = (
            "The dynamically matched experiment did not resolve whether "
            "strong candidate subsampling changes finite-horizon transient "
            "causal amplification at the frozen +/-0.15 effect scale."
        )

    verdict = {
        "validity": {
            "dynamic_rate_match": (
                validity[
                    "status"
                ]
            ),
            "probe_coverage_fraction": float(
                support[
                    "coverage_fraction"
                ]
            ),
            "scientific_valid": bool(
                scientific_valid
            ),
        },
        "primary_status": (
            p_status
        ),
        "overall_status": (
            overall
        ),
        "bounded_claim": (
            bounded
        ),
        "what_this_does_not_establish": [
            "formal branching ratio",
            "subcriticality",
            "supercriticality",
            "criticality",
            "phase transition",
            "coherent structure",
            "individuality",
            "organism",
            "life",
        ],
        "stop_rule": (
            "Do not alter SEI, horizon, probe geometry, fraction grid, "
            "reference policy or dynamic calibration to rescue the result."
        ),
        "next_if_supported": (
            "Map amplification across allocation concentration while retaining "
            "dynamic rate matching."
        ),
        "next_if_bounded": (
            "Close the finite-selection amplification question at this scale "
            "and treat finite-budget effects as redistribution rather than "
            "material amplification in the tested regime."
        ),
        "next_if_unresolved": (
            "Increase independent groups only if achieved MDE exceeds the "
            "frozen SEI."
        ),
    }

    reporter.stage(
        "stage-07-verdict.md",
        "Stage 7 — Bounded Chapter 26 V2 Verdict",
        verdict,
    )

    reporter.json(
        "stage-07-verdict.json",
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
