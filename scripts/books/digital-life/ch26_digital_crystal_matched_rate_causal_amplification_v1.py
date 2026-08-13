#!/usr/bin/env python3
"""
Digital Life — Chapter 26 V1
Does Candidate Subsampling Change Causal Amplification?
=======================================================

CONTEXT
-------

Chapter 25 established a real substrate mechanism:

    PARTIAL FRONTIER EVALUATION
        -> finite evaluation-slot competition
        -> outside-causal-cone redistribution

    FULL FRONTIER EVALUATION
        -> exact zero selector-mediated far-field coupling

That result is spatial/allocation-level.

The next question is dynamical:

    Does stronger candidate subsampling change DOWNSTREAM CAUSAL AMPLIFICATION?

A naive budget sweep is invalid because:

    larger B
        -> more evaluated candidates
        -> more expected attachments
        -> more descendants

That would confound "how much construction occurs" with "how concentrated the
selection process is."

Chapter 26 therefore matches expected construction rate across budget arms.

SCIENTIFIC QUESTION
-------------------

At approximately matched expected attachment count per update:

    does changing the fraction of frontier candidates evaluated
    alter the downstream causal amplification caused by one transient
    FORCE/PREVENT intervention?

CONTROL PARAMETER
-----------------

For each frozen checkpoint:

    F = frontier size

Choose evaluation fractions:

    f in {0.10, 0.25, 0.50, 0.75, 1.00}

plus:

    UNBOUNDED

For each arm:

    B = ceil(f * F)

except UNBOUNDED, which evaluates all frontier cells.

EXPECTED-CONSTRUCTION MATCHING
------------------------------

Let:

    C_target

be the expected number of attachments per update under the REFERENCE arm.

Reference arm:

    f_ref = 0.10

using the frozen base attachment rule.

The smallest-budget arm defines the target because no lower-budget arm can be
asked to realize more expected attachments than it has evaluation slots.
All higher-budget arms are calibrated DOWN to this natural low-budget
construction rate.

For every other continuation budget arm, apply a single additive score offset:

    score' = score + calibration_offset

chosen so that:

    sum_selected p'(cell)
        ~= C_target

on the SAME post-intervention PREVENT state at lag 1.

Thus calibration matches expected continuation construction after the common
causal perturbation has already been created.

The offset is solved by monotone bisection.

This changes the attachment calibration, not the geometry, candidate selector,
or random-number coupling.

The calibration is frozen BEFORE the causal intervention outcome is evaluated.

MATCHING GATE
-------------

For each checkpoint × arm:

    |expected_attachments_arm - C_target|
        / max(C_target, epsilon)
        <= 0.02

Required:

    at least 95% of scientific arms pass this 2% expected-construction match.

Otherwise:

    INVALID_CONSTRUCTION_RATE_MATCH

INTERVENTION
------------

Use the same transient FORCE/PREVENT intervention family as Chapter 23/24:

    SAME checkpoint
    SAME intervention cell x
    SAME environment
    SAME cell-keyed randomness

    FORCE x
    vs
    PREVENT x

The intervention update is generated ONCE with the frozen base rule and
B_intervention = 96.

All budget arms reuse those exact post-intervention states.

From lag 1 onward, each arm applies its own matched-rate continuation budget and
calibration offset.

x is allowed one full causal update at lag 1, then removed from FORCE if still
occupied.

Continue for:

    H = 12

PRIMARY OUTCOME
---------------

Define:

    G_T(H)

as cumulative FORCE-minus-PREVENT attachments within distance 1..H over
lags 1..H, excluding x.

Chapter 26 uses the GROUP mean over probe sites as the independent unit.

PRIMARY HYPOTHESIS H1
---------------------

H1 — CANDIDATE SUBSAMPLING CHANGES TRANSIENT CAUSAL AMPLIFICATION
     AT MATCHED EXPECTED CONSTRUCTION RATE.

Primary contrast:

    strongest subsampling arm:
        f = 0.10

    versus exhaustive arm:
        f = 1.00

Outcome:

    Delta_G
        =
        G_T(f=0.10) - G_T(f=1.00)

Frozen SEI:

    0.15 attachments

Three-way status:

    SUPPORTED
        if |mean Delta_G| >= 0.15,
           CI excludes zero,
           and achieved MDE80 <= 0.15

    BOUNDED_NEAR_ZERO
        if 95% CI lies wholly within [-0.15, +0.15]
           and achieved MDE80 <= 0.15

    UNRESOLVED
        otherwise

This is deliberately TWO-SIDED.

We do not pre-assume whether stronger subsampling increases or suppresses
amplification.

SECONDARY OUTCOMES
------------------

H2 — LAG-1 CAUSAL EFFECT

Compare exact expected lag-1 local gain:

    E1_ring1

across matched-rate budget arms.

This tells us whether any downstream difference starts immediately.

H3 — PATH DIVERGENCE RATE

Report:

    P(any lag-1 attachment-set divergence)

for each arm.

H4 — CONDITIONAL CASCADE

Report:

    P(G_T != 0)

    E[G_T | G_T != 0]

descriptively.

No post-hoc directional promotion.

AMPLIFICATION PROFILE
---------------------

For each budget fraction report:

    mean G_T
    mean E1_ring1
    mean lag-1 divergence probability
    mean selected-set overlap
    mean far-field expected redistribution
    expected construction rate
    calibration offset

Also report:

    G_T / max(E1_ring1, epsilon)

as a descriptive downstream-amplification factor.

Do NOT call this a branching ratio.

WHY NOT A BRANCHING RATIO?
--------------------------

Finite-horizon G_T can contain:

    descendants of descendants
    overlapping pathways
    substitutions
    branch-specific candidate-set changes

It is not a formal Galton-Watson branching parameter.

Use:

    finite-horizon causal amplification

unless descendant semantics are explicitly established.

PROBE SITES
-----------

Use the supported Chapter 24/25 single-contact frontier regime:

    occupied_neighbors = 1

Sample up to:

    4 probe sites / group

across the available n=1 frontier.

Do NOT select probes by FCP.

Chapter 26 is about the budget control parameter, not another geometry-class
search.

Each probe is reused across ALL budget arms.

This gives exact within-probe budget comparisons.

SAME CHECKPOINT ACROSS ARMS
---------------------------

Non-negotiable:

    checkpoint is frozen
    probe cell is frozen
    future environment is frozen
    random keys are frozen

Only:

    candidate budget
    attachment calibration offset

change.

UNBOUNDED REFERENCE
-------------------

Include an explicit unbounded/full-frontier evaluation arm calibrated to the
same expected construction rate.

This separates:

    candidate subsampling
from
    total expected construction

at the closest available control point.

CALIBRATION DETAILS
-------------------

Base attachment score:

    s(cell)

Calibrated score:

    s'(cell) = s(cell) + offset

Then:

    p'(cell) = logistic(s'(cell))

The offset is solved against the exact selected candidate set for that budget.

Bounds:

    offset in [-12, +12]

Bisection tolerance:

    1e-10 expected attachments

Max iterations:

    100

If target cannot be reached within bounds:

    arm invalid

TARGET RATE
-----------

For each checkpoint, calculate C_target from the common post-intervention
PREVENT lag-1 state under:

    f_ref = 0.10
    base offset = 0

This preserves the natural construction scale of that checkpoint rather than
forcing a global constant across heterogeneous checkpoints.

SCIENTIFIC UNIT
---------------

Multiple probes within one checkpoint are repeated measures.

All inference:

    average probes within group
    then infer across groups

Never treat probes as independent replicates.

ZERO-INFLATION
--------------

Report separately:

    P(G_T = 0)
    P(G_T != 0)
    E[G_T | nonzero]

because Chapter 24 showed that realized causal outcomes can be strongly
zero-inflated.

SELECTION DIAGNOSTICS
---------------------

Per lag report FORCE/PREVENT:

    selected-set Jaccard
    symmetric difference count

These quantify how strongly the two futures allocate computation differently.

FAR-FIELD DIAGNOSTIC
--------------------

At lag 1, report exact expected outside-cone effect:

    E1_far, d > 1

This is selector-mediated.

It is diagnostic here, not the primary hypothesis.

STOP RULE
---------

If H1 is BOUNDED_NEAR_ZERO:

    do not rescue by changing fractions,
    horizon,
    probe geometry,
    calibration target,
    or SEI.

Then Chapter 26 establishes:

    finite selection redistributes construction
    but does not materially change transient causal amplification
    at matched expected construction rate.

If H1 is SUPPORTED:

    the next experiment may ask where in parameter space amplification changes
    and whether any regime approaches sustained causal activity.

If UNRESOLVED:

    increase independent groups only if achieved MDE > SEI.
    Do not change the effect definition.

PROFILES
--------

smoke:
    8 groups, engineering only

quick:
    48 groups

standard:
    96 groups

full:
    192 groups
    intended scientific run

FRESH SEED
----------

Default:
    20260912

Previous:
    Ch24 V4 20260909
    Ch24 V5 20260910
    Ch25 V1 20260911

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

EXPERIMENT_VERSION = "digital-crystal-matched-rate-causal-amplification-v1"
SCHEMA_VERSION = 1
CHAPTER = 26
CHAPTER_TITLE = "Does Candidate Subsampling Change Causal Amplification?"

FRACTIONS = [0.10, 0.25, 0.50, 0.75, 1.00]
REFERENCE_FRACTION = 0.10
HORIZON = 12
CONSTRUCTION_MATCH_TOLERANCE = 0.02
PRIMARY_SEI = 0.15
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

    mde = se * (
        Z_95_ONE_SIDED
        + Z_80_POWER
    )

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
        "achieved_mde80_one_sided": float(mde),
    }


def two_sided_status(
    summary: dict,
    sei: float,
    scientific_valid: bool,
) -> str:
    if not scientific_valid:
        return "INVALID"

    powered = (
        summary[
            "achieved_mde80_one_sided"
        ]
        <= sei
    )

    if not powered:
        return "UNRESOLVED"

    low = summary["ci95_low"]
    high = summary["ci95_high"]
    mean = summary["mean"]

    if (
        low > -sei
        and high < sei
    ):
        return "BOUNDED_NEAR_ZERO"

    if (
        abs(mean) >= sei
        and (
            low > 0.0
            or high < 0.0
        )
    ):
        return "SUPPORTED"

    return "UNRESOLVED"


# ============================================================================
# Frozen attachment rule with calibration offset
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


def calibrated_probability_from_score(
    score: float,
    offset: float,
) -> float:
    return float(
        ch18.logistic_scalar(
            score + offset
        )
    )


def calibrated_attachment_probability(
    cell: Cell,
    occupied_before: Set[Cell],
    input_value: float,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    return calibrated_probability_from_score(
        attachment_score(
            cell,
            occupied_before,
            input_value,
            crystal_params,
        ),
        offset,
    )


# ============================================================================
# Candidate selection / calibration
# ============================================================================

def select_candidates_for_budget(
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
            calibrated_attachment_probability(
                cell,
                occupied,
                input_value,
                crystal_params,
                offset,
            )
            for cell in selected
        )
    )


def solve_offset_for_target(
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
            abs(target) <= CALIBRATION_TOLERANCE,
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

    if target < e_lo or target > e_hi:
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
                e_mid - target
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
# Checkpoint and probe preparation
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

    # Deterministic spread across radial position.
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
                int(
                    round(
                        idx
                    )
                )
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
    probes: List[Probe] = []
    group_counts = []

    for group in tqdm(
        range(int(profile["groups"])),
        desc="Chapter 26 checkpoints",
    ):
        checkpoint, future_env, _ = v4.build_checkpoint(
            source_profile,
            crystal_params,
            seed,
            group,
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

        group_counts.append(
            len(selected)
        )

        probes.extend(
            selected
        )

    groups_with_probes = sum(
        count > 0
        for count in group_counts
    )

    payload = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "groups_with_probes": int(
            groups_with_probes
        ),
        "coverage_fraction": float(
            groups_with_probes
            / max(
                1,
                int(
                    profile[
                        "groups"
                    ]
                ),
            )
        ),
        "total_probes": int(
            len(
                probes
            )
        ),
        "probe_count_distribution": {
            "min": int(
                min(
                    group_counts
                )
                if group_counts
                else 0
            ),
            "median": float(
                np.median(
                    group_counts
                )
                if group_counts
                else 0
            ),
            "max": int(
                max(
                    group_counts
                )
                if group_counts
                else 0
            ),
        },
        "supported_scope": (
            "occupied_neighbors = 1"
        ),
    }

    return probes, payload


# ============================================================================
# Reference target and arm calibration
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
    """
    Create the causal perturbation ONCE using the frozen Chapter 24
    intervention mechanics. Every Chapter 26 budget arm reuses these exact
    post-intervention states.
    """
    checkpoint = probe.checkpoint
    future_env = probe.future_env

    radius = int(source_profile["radius"])
    loss_rate = float(source_profile["loss_rate"])

    intervention_budget = int(source_profile["budget"])

    force_grown, _, force_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        intervention_budget,
        force_cell=probe.cell,
    )

    prevent_grown, _, prevent_selected, _ = v4.growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        intervention_budget,
        prevent_cell=probe.cell,
    )

    if force_selected != prevent_selected:
        raise RuntimeError(
            "Common intervention evaluated sets differ before force/prevent."
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    return PreparedIntervention(
        probe=probe,
        force_state=force_state,
        prevent_state=prevent_state,
    )


@dataclass
class ArmCalibration:
    budget_label: str
    fraction: float | None
    budget: int | None
    offset: float
    target_expected_attachments: float
    achieved_expected_attachments: float
    relative_error: float
    valid: bool


def budget_from_fraction(
    frontier_size: int,
    fraction: float,
) -> int:
    return max(
        1,
        int(
            math.ceil(
                fraction
                * frontier_size
            )
        ),
    )


def calibrate_probe_arms(
    prepared: PreparedIntervention,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    Dict[str, ArmCalibration],
    dict,
]:
    """
    Match expected CONTINUATION construction on the common lag-1 PREVENT state.

    This prevents budget from changing the intervention itself.
    """
    state = prepared.prevent_state
    probe = prepared.probe

    radius = int(source_profile["radius"])

    next_input = float(probe.future_env[1])

    frontier = v4.frontier_cells(
        set(state.occupied),
        radius,
    )

    F = len(frontier)

    ref_budget = budget_from_fraction(
        F,
        REFERENCE_FRACTION,
    )

    ref_selected = select_candidates_for_budget(
        frontier,
        state,
        ref_budget,
    )

    target = expected_selected_attachments(
        state,
        next_input,
        ref_selected,
        crystal_params,
        0.0,
    )

    arms: Dict[str, ArmCalibration] = {}

    for fraction in FRACTIONS:
        label = f"f={fraction:.2f}"

        B = budget_from_fraction(
            F,
            fraction,
        )

        selected = select_candidates_for_budget(
            frontier,
            state,
            B,
        )

        if abs(fraction - REFERENCE_FRACTION) < 1e-12:
            offset = 0.0
            achieved = expected_selected_attachments(
                state,
                next_input,
                selected,
                crystal_params,
                offset,
            )
            ok = True
        else:
            offset, achieved, ok = solve_offset_for_target(
                state,
                next_input,
                selected,
                crystal_params,
                target,
            )

        rel_error = (
            abs(achieved - target)
            / max(target, 1e-12)
            if ok
            else float("inf")
        )

        arms[label] = ArmCalibration(
            budget_label=label,
            fraction=float(fraction),
            budget=int(B),
            offset=float(offset),
            target_expected_attachments=float(target),
            achieved_expected_attachments=float(achieved),
            relative_error=float(rel_error),
            valid=bool(
                ok
                and rel_error <= CONSTRUCTION_MATCH_TOLERANCE
            ),
        )

    selected = list(frontier)

    offset, achieved, ok = solve_offset_for_target(
        state,
        next_input,
        selected,
        crystal_params,
        target,
    )

    rel_error = (
        abs(achieved - target)
        / max(target, 1e-12)
        if ok
        else float("inf")
    )

    arms["unbounded"] = ArmCalibration(
        budget_label="unbounded",
        fraction=None,
        budget=None,
        offset=float(offset),
        target_expected_attachments=float(target),
        achieved_expected_attachments=float(achieved),
        relative_error=float(rel_error),
        valid=bool(
            ok
            and rel_error <= CONSTRUCTION_MATCH_TOLERANCE
        ),
    )

    info = {
        "frontier_size": int(F),
        "target_expected_attachments": float(target),
        "reference_fraction": float(REFERENCE_FRACTION),
        "reference_budget": int(ref_budget),
        "calibration_state": "common post-intervention PREVENT state at lag 1",
    }

    return arms, info

# ============================================================================
# Calibrated growth
# ============================================================================

def calibrated_growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
    force_cell: Cell | None = None,
    prevent_cell: Cell | None = None,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
]:
    occupied_before = set(
        state.occupied
    )

    occupied = set(
        state.occupied
    )

    birth_time = dict(
        state.birth_time
    )

    frontier = v4.frontier_cells(
        occupied_before,
        radius,
    )

    next_step = int(
        state.step + 1
    )

    selected = select_candidates_for_budget(
        frontier,
        state,
        budget,
    )

    selected_set = set(
        selected
    )

    if (
        force_cell is not None
        and force_cell not in selected_set
    ):
        raise RuntimeError(
            "force cell not in evaluated set"
        )

    if (
        prevent_cell is not None
        and prevent_cell not in selected_set
    ):
        raise RuntimeError(
            "prevent cell not in evaluated set"
        )

    additions: List[
        Cell
    ] = []

    for cell in selected:
        if (
            force_cell is not None
            and cell == force_cell
        ):
            additions.append(
                cell
            )
            continue

        if (
            prevent_cell is not None
            and cell == prevent_cell
        ):
            continue

        p = calibrated_attachment_probability(
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
            additions.append(
                cell
            )

    for cell in additions:
        occupied.add(
            cell
        )

        birth_time[
            cell
        ] = next_step

    out = ch18.MaterialCrystalState(
        occupied=occupied,
        birth_time=birth_time,
        modified=set(),
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=(
            list(
                state.attachments_by_step
            )
            + [
                len(
                    additions
                )
            ]
        ),
        population_by_step=(
            list(
                state.population_by_step
            )
            + [
                len(
                    occupied
                )
            ]
        ),
        modified_count_by_step=(
            list(
                state.modified_count_by_step
            )
            + [0]
        ),
    )

    return (
        out,
        additions,
        selected,
    )


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
    grown, additions, selected = calibrated_growth_step(
        state,
        input_value,
        radius,
        crystal_params,
        budget,
        offset,
    )

    after_loss, lost = ch21.apply_background_loss(
        grown,
        loss_rate,
    )

    return (
        after_loss,
        additions,
        lost,
        selected,
    )


# ============================================================================
# Exact lag-1 expectation under calibrated arm
# ============================================================================

def exact_lag1_expectation(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    next_input: float,
    x: Cell,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int | None,
    offset: float,
) -> dict:
    force_frontier = v4.frontier_cells(
        set(
            force_state.occupied
        ),
        radius,
    )

    prevent_frontier = v4.frontier_cells(
        set(
            prevent_state.occupied
        ),
        radius,
    )

    force_selected = select_candidates_for_budget(
        force_frontier,
        force_state,
        budget,
    )

    prevent_selected = select_candidates_for_budget(
        prevent_frontier,
        prevent_state,
        budget,
    )

    sf = set(
        force_selected
    )

    sp = set(
        prevent_selected
    )

    force_occ = set(
        force_state.occupied
    )

    prevent_occ = set(
        prevent_state.occupied
    )

    E_ring1 = 0.0
    E_far = 0.0
    E_global = 0.0

    divergence_q = []

    for cell in sf | sp:
        if cell == x:
            continue

        pf = (
            calibrated_attachment_probability(
                cell,
                force_occ,
                next_input,
                crystal_params,
                offset,
            )
            if cell in sf
            else 0.0
        )

        pp = (
            calibrated_attachment_probability(
                cell,
                prevent_occ,
                next_input,
                crystal_params,
                offset,
            )
            if cell in sp
            else 0.0
        )

        delta = (
            pf - pp
        )

        d = v4.relative_distance(
            cell,
            x,
        )

        E_global += delta

        if d <= 1:
            E_ring1 += delta
        else:
            E_far += delta

        if cell in sf and cell in sp:
            q = abs(
                pf - pp
            )
        elif cell in sf:
            q = pf
        else:
            q = pp

        divergence_q.append(
            min(
                1.0,
                max(
                    0.0,
                    float(
                        q
                    ),
                ),
            )
        )

    prob_none = (
        float(
            np.prod(
                [
                    1.0 - q
                    for q in divergence_q
                ]
            )
        )
        if divergence_q
        else 1.0
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
        "prob_any_divergence": float(
            1.0 - prob_none
        ),
        "selected_jaccard": float(
            jaccard
        ),
        "selected_symdiff": int(
            len(
                sf ^ sp
            )
        ),
    }


# ============================================================================
# Transient calibrated intervention
# ============================================================================

@dataclass
class ArmResult:
    group: int
    probe_index: int
    q: int
    r: int

    budget_label: str
    fraction: float | None
    budget: int | None
    offset: float

    target_expected_attachments: float
    achieved_expected_attachments: float
    construction_match_error: float

    E1_ring1: float
    E1_far: float
    E1_global: float
    model_prob_any_divergence: float

    realized_lag1_divergence: int

    G_local: float
    G_global: float
    G_nonzero: int

    selected_jaccard_mean: float
    selected_symdiff_mean: float

    downstream_amplification_factor: float


def run_arm(
    prepared: PreparedIntervention,
    calibration: ArmCalibration,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> ArmResult:
    probe = prepared.probe
    future_env = probe.future_env

    radius = int(
        source_profile[
            "radius"
        ]
    )

    loss_rate = float(
        source_profile[
            "loss_rate"
        ]
    )

    x = probe.cell

    # Every arm starts from the exact same post-intervention states.
    force_state = ch21.clone_state(prepared.force_state)
    prevent_state = ch21.clone_state(prepared.prevent_state)

    exact = exact_lag1_expectation(
        force_state,
        prevent_state,
        float(
            future_env[
                1
            ]
        ),
        x,
        radius,
        crystal_params,
        calibration.budget,
        calibration.offset,
    )

    local_total = 0.0
    global_total = 0.0
    lag1_divergence = 0
    jaccards = []
    symdiffs = []

    for lag in range(
        1,
        HORIZON + 1,
    ):
        (
            force_state,
            force_add,
            _,
            force_selected,
        ) = calibrated_canonical_step(
            force_state,
            float(
                future_env[
                    lag
                ]
            ),
            radius,
            crystal_params,
            calibration.budget,
            calibration.offset,
            loss_rate,
        )

        (
            prevent_state,
            prevent_add,
            _,
            prevent_selected,
        ) = calibrated_canonical_step(
            prevent_state,
            float(
                future_env[
                    lag
                ]
            ),
            radius,
            crystal_params,
            calibration.budget,
            calibration.offset,
            loss_rate,
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
            1 <= v4.relative_distance(
                c,
                x,
            ) <= HORIZON
            for c in force_add_set
        )

        prevent_local = sum(
            1 <= v4.relative_distance(
                c,
                x,
            ) <= HORIZON
            for c in prevent_add_set
        )

        local_total += float(
            force_local
            - prevent_local
        )

        global_total += float(
            len(
                force_add_set
            )
            - len(
                prevent_add_set
            )
        )

        sf = set(
            force_selected
        )

        sp = set(
            prevent_selected
        )

        union = sf | sp

        jaccards.append(
            1.0
            if not union
            else len(
                sf & sp
            )
            / len(
                union
            )
        )

        symdiffs.append(
            len(
                sf ^ sp
            )
        )

        if lag == 1:
            f_local_set = {
                c
                for c in force_add_set
                if 1 <= v4.relative_distance(
                    c,
                    x,
                ) <= HORIZON
            }

            p_local_set = {
                c
                for c in prevent_add_set
                if 1 <= v4.relative_distance(
                    c,
                    x,
                ) <= HORIZON
            }

            lag1_divergence = int(
                f_local_set
                != p_local_set
            )

            # Transient intervention: remove x after one causal update.
            if x in force_state.occupied:
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

    amp_factor = (
        local_total
        / exact[
            "E1_ring1"
        ]
        if abs(
            exact[
                "E1_ring1"
            ]
        ) > 1e-9
        else float(
            "nan"
        )
    )

    return ArmResult(
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
        budget_label=calibration.budget_label,
        fraction=calibration.fraction,
        budget=calibration.budget,
        offset=float(
            calibration.offset
        ),
        target_expected_attachments=float(
            calibration.target_expected_attachments
        ),
        achieved_expected_attachments=float(
            calibration.achieved_expected_attachments
        ),
        construction_match_error=float(
            calibration.relative_error
        ),
        E1_ring1=float(
            exact[
                "E1_ring1"
            ]
        ),
        E1_far=float(
            exact[
                "E1_far"
            ]
        ),
        E1_global=float(
            exact[
                "E1_global"
            ]
        ),
        model_prob_any_divergence=float(
            exact[
                "prob_any_divergence"
            ]
        ),
        realized_lag1_divergence=int(
            lag1_divergence
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
        selected_jaccard_mean=float(
            np.mean(
                jaccards
            )
        ),
        selected_symdiff_mean=float(
            np.mean(
                symdiffs
            )
        ),
        downstream_amplification_factor=float(
            amp_factor
        ),
    )


# ============================================================================
# Group aggregation
# ============================================================================

def group_arm_means(
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
            getter(
                row
            )
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
            np.mean(
                values
            )
        )
        for group, values in buckets.items()
        if values
    }


def paired_group_difference(
    rows: Sequence[ArmResult],
    label_a: str,
    label_b: str,
    getter,
) -> List[float]:
    a = group_arm_means(
        rows,
        label_a,
        getter,
    )

    b = group_arm_means(
        rows,
        label_b,
        getter,
    )

    common = sorted(
        set(
            a
        )
        & set(
            b
        )
    )

    return [
        float(
            a[g]
            - b[g]
        )
        for g in common
    ]


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
            / "ch26-matched-rate-causal-amplification-v1-full-report.md"
        )

        parts = [
            "# Chapter 26 — Does Candidate Subsampling Change Causal Amplification? (V1)",
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
    rows: Sequence[ArmResult],
) -> None:
    jsonl = (
        reporter.root
        / "raw-amplification-arms.jsonl"
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
        / "raw-amplification-arms.csv"
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
        default=20260912,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch26-matched-rate-causal-amplification-v1"
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
        "fractions": FRACTIONS,
        "reference_fraction": (
            REFERENCE_FRACTION
        ),
        "construction_match_tolerance": (
            CONSTRUCTION_MATCH_TOLERANCE
        ),
        "primary_SEI": (
            PRIMARY_SEI
        ),
        "fresh_seed": bool(
            int(
                args.seed
            )
            not in {
                20260909,
                20260910,
                20260911,
            }
        ),
        "started_at_unix": float(
            time.time()
        ),
    }

    protocol = {
        "role": (
            "MATCHED-CONSTRUCTION-RATE CAUSAL AMPLIFICATION TEST"
        ),
        "question": (
            "At matched expected construction rate, does stronger candidate "
            "subsampling change transient causal amplification?"
        ),
        "same_checkpoint_across_arms": True,
        "same_probe_across_arms": True,
        "same_post_intervention_force_prevent_states_across_arms": True,
        "intervention_budget_fixed_at": 96,
        "same_future_environment": True,
        "same_random_keys": True,
        "control_parameter": (
            "fraction of frontier candidates evaluated"
        ),
        "fractions": FRACTIONS,
        "unbounded_arm": True,
        "reference_fraction_for_target": (
            REFERENCE_FRACTION
        ),
        "construction_rate_match": {
            "target": (
                "checkpoint-specific expected attachments under f=0.10 "
                "with base offset 0 on the common post-intervention PREVENT state"
            ),
            "relative_tolerance": (
                CONSTRUCTION_MATCH_TOLERANCE
            ),
            "required_arm_pass_fraction": 0.95,
        },
        "primary_H1": {
            "contrast": (
                "G_T(f=0.10) - G_T(f=1.00)"
            ),
            "SEI_abs": (
                PRIMARY_SEI
            ),
            "two_sided": True,
            "statuses": [
                "SUPPORTED",
                "BOUNDED_NEAR_ZERO",
                "UNRESOLVED",
                "INVALID",
            ],
        },
        "supported_probe_scope": (
            "occupied_neighbors = 1"
        ),
        "horizon": (
            HORIZON
        ),
        "forbidden_overclaims": [
            "formal branching ratio",
            "critical point",
            "supercriticality",
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
        "Stage 0 — Frozen Chapter 26 V1 Protocol",
        protocol,
    )

    reporter.json(
        "stage-00-protocol.json",
        protocol,
    )

    probes, support = prepare_probes(
        profile,
        source_profile,
        crystal_params,
        args.seed,
    )

    reporter.stage(
        "stage-01-probe-support.md",
        "Stage 1 — Frozen Probe Support",
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

    rows: List[
        ArmResult
    ] = []

    calibration_rows = []

    valid_arm_count = 0
    total_arm_count = 0

    for probe in tqdm(
        probes,
        desc="Chapter 26 matched-rate arms",
    ):
        prepared = prepare_common_intervention(
            probe,
            source_profile,
            crystal_params,
        )

        arms, info = calibrate_probe_arms(
            prepared,
            source_profile,
            crystal_params,
        )

        for label, calibration in arms.items():
            total_arm_count += 1

            if calibration.valid:
                valid_arm_count += 1

            calibration_rows.append({
                "group": int(
                    probe.group
                ),
                "probe_index": int(
                    probe.probe_index
                ),
                "budget_label": label,
                "frontier_size": int(
                    info[
                        "frontier_size"
                    ]
                ),
                "target_expected_attachments": float(
                    calibration.target_expected_attachments
                ),
                "achieved_expected_attachments": float(
                    calibration.achieved_expected_attachments
                ),
                "relative_error": float(
                    calibration.relative_error
                ),
                "offset": float(
                    calibration.offset
                ),
                "valid": bool(
                    calibration.valid
                ),
            })

            if not calibration.valid:
                continue

            rows.append(
                run_arm(
                    prepared,
                    calibration,
                    source_profile,
                    crystal_params,
                )
            )

    arm_pass_fraction = (
        valid_arm_count
        / max(
            1,
            total_arm_count,
        )
    )

    calibration_summary = {
        "total_arms": int(
            total_arm_count
        ),
        "valid_arms": int(
            valid_arm_count
        ),
        "pass_fraction": float(
            arm_pass_fraction
        ),
        "required_pass_fraction": 0.95,
        "construction_match_valid": bool(
            arm_pass_fraction
            >= 0.95
        ),
        "relative_tolerance": (
            CONSTRUCTION_MATCH_TOLERANCE
        ),
    }

    reporter.stage(
        "stage-02-construction-rate-calibration.md",
        "Stage 2 — Expected Construction-Rate Matching",
        calibration_summary,
    )

    reporter.json(
        "stage-02-construction-rate-calibration.json",
        calibration_summary,
    )

    reporter.json(
        "calibration-arms.json",
        {
            "arms": calibration_rows
        },
    )

    write_raw(
        reporter,
        rows,
    )

    scientific_valid = bool(
        calibration_summary[
            "construction_match_valid"
        ]
        and support[
            "coverage_fraction"
        ]
        >= 0.90
    )

    # Per-arm profiles.
    arm_profiles = {}

    labels = [
        f"f={fraction:.2f}"
        for fraction in FRACTIONS
    ] + [
        "unbounded"
    ]

    for idx, label in enumerate(
        labels
    ):
        subset = [
            row
            for row in rows
            if row.budget_label == label
        ]

        def gm(getter):
            mapping = group_arm_means(
                rows,
                label,
                getter,
            )

            return [
                v
                for _, v in sorted(
                    mapping.items()
                )
            ]

        G_values = gm(
            lambda r:
            r.G_local
        )

        E1_values = gm(
            lambda r:
            r.E1_ring1
        )

        divergence_values = gm(
            lambda r:
            r.realized_lag1_divergence
        )

        nonzero_values = gm(
            lambda r:
            r.G_nonzero
        )

        jaccard_values = gm(
            lambda r:
            r.selected_jaccard_mean
        )

        symdiff_values = gm(
            lambda r:
            r.selected_symdiff_mean
        )

        far_values = gm(
            lambda r:
            r.E1_far
        )

        match_values = gm(
            lambda r:
            r.achieved_expected_attachments
        )

        offset_values = gm(
            lambda r:
            r.offset
        )

        amp_values = gm(
            lambda r:
            r.downstream_amplification_factor
        )

        raw_G = np.asarray(
            [
                row.G_local
                for row in subset
            ],
            dtype=float,
        )

        nz = raw_G[
            np.abs(
                raw_G
            )
            > 0.0
        ]

        arm_profiles[
            label
        ] = {
            "groups": int(
                len(
                    set(
                        row.group
                        for row in subset
                    )
                )
            ),
            "probes": int(
                len(
                    subset
                )
            ),
            "G_local": bootstrap_mean_ci(
                G_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 100 + idx * 20,
            ),
            "E1_ring1": bootstrap_mean_ci(
                E1_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 101 + idx * 20,
            ),
            "lag1_realized_divergence": bootstrap_mean_ci(
                divergence_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 102 + idx * 20,
            ),
            "G_nonzero_rate": bootstrap_mean_ci(
                nonzero_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 103 + idx * 20,
            ),
            "E1_far": bootstrap_mean_ci(
                far_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 104 + idx * 20,
            ),
            "selected_jaccard": bootstrap_mean_ci(
                jaccard_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 105 + idx * 20,
            ),
            "selected_symdiff": bootstrap_mean_ci(
                symdiff_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 106 + idx * 20,
            ),
            "matched_expected_attachments": bootstrap_mean_ci(
                match_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 107 + idx * 20,
            ),
            "calibration_offset": bootstrap_mean_ci(
                offset_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 108 + idx * 20,
            ),
            "descriptive_G_over_E1": bootstrap_mean_ci(
                amp_values,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 109 + idx * 20,
            ),
            "conditional_G_given_nonzero": {
                "n_all": int(
                    len(
                        raw_G
                    )
                ),
                "n_nonzero": int(
                    len(
                        nz
                    )
                ),
                "nonzero_fraction": float(
                    len(
                        nz
                    )
                    / max(
                        1,
                        len(
                            raw_G
                        ),
                    )
                ),
                "mean_given_nonzero": float(
                    np.mean(
                        nz
                    )
                )
                if len(
                    nz
                )
                else float(
                    "nan"
                ),
            },
        }

    reporter.stage(
        "stage-03-arm-profiles.md",
        "Stage 3 — Matched-Rate Budget Arm Profiles",
        arm_profiles,
    )

    reporter.json(
        "stage-03-arm-profiles.json",
        arm_profiles,
    )

    # Primary H1: f=0.10 vs f=1.00.
    primary_delta = paired_group_difference(
        rows,
        "f=0.10",
        "f=1.00",
        lambda r:
        r.G_local,
    )

    primary_summary = bootstrap_mean_ci(
        primary_delta,
        int(
            profile[
                "bootstrap_reps"
            ]
        ),
        args.seed + 500,
    )

    primary_status = (
        "ENGINEERING_SMOKE_ONLY"
        if not profile[
            "scientific"
        ]
        else two_sided_status(
            primary_summary,
            PRIMARY_SEI,
            scientific_valid,
        )
    )

    primary = {
        "contrast": (
            "G_T(f=0.10) - G_T(f=1.00)"
        ),
        "SEI_abs": (
            PRIMARY_SEI
        ),
        "result": (
            primary_summary
        ),
        "status": (
            primary_status
        ),
    }

    reporter.stage(
        "stage-04-primary-amplification-test.md",
        "Stage 4 — Primary Matched-Rate Amplification Test",
        primary,
    )

    reporter.json(
        "stage-04-primary-amplification-test.json",
        primary,
    )

    # Secondary pairwise contrasts to exhaustive arm.
    contrasts = {}

    for idx, fraction in enumerate(
        FRACTIONS[
            :-1
        ]
    ):
        label = (
            f"f={fraction:.2f}"
        )

        contrasts[
            label
        ] = {
            "G_local_minus_full": bootstrap_mean_ci(
                paired_group_difference(
                    rows,
                    label,
                    "f=1.00",
                    lambda r:
                    r.G_local,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 600 + idx * 30,
            ),
            "E1_ring1_minus_full": bootstrap_mean_ci(
                paired_group_difference(
                    rows,
                    label,
                    "f=1.00",
                    lambda r:
                    r.E1_ring1,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 601 + idx * 30,
            ),
            "lag1_divergence_minus_full": bootstrap_mean_ci(
                paired_group_difference(
                    rows,
                    label,
                    "f=1.00",
                    lambda r:
                    r.realized_lag1_divergence,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 602 + idx * 30,
            ),
            "far_effect_minus_full": bootstrap_mean_ci(
                paired_group_difference(
                    rows,
                    label,
                    "f=1.00",
                    lambda r:
                    r.E1_far,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed + 603 + idx * 30,
            ),
        }

    reporter.stage(
        "stage-05-secondary-contrasts.md",
        "Stage 5 — Secondary Budget-to-Full Contrasts",
        contrasts,
    )

    reporter.json(
        "stage-05-secondary-contrasts.json",
        contrasts,
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

    elif not scientific_valid:
        overall = (
            "INVALID_MATCHED_CONSTRUCTION_RATE"
        )

        bounded = (
            "The expected-construction-rate calibration or probe-coverage gate "
            "failed, so the budget arms cannot be compared scientifically."
        )

    elif primary_status == "SUPPORTED":
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
            "At matched expected construction rate, the strongest candidate "
            f"subsampling arm produced {direction} finite-horizon causal "
            "amplification than exhaustive evaluation by at least the frozen "
            "scientifically meaningful scale."
        )

    elif primary_status == "BOUNDED_NEAR_ZERO":
        overall = (
            "CAUSAL_AMPLIFICATION_INVARIANT_WITHIN_SEI"
        )

        bounded = (
            "At matched expected construction rate, the f=0.10 versus full "
            "evaluation difference in finite-horizon causal amplification was "
            "bounded within the predeclared ±0.15 attachment equivalence region."
        )

    else:
        overall = (
            "MATCHED_RATE_CAUSAL_AMPLIFICATION_UNRESOLVED"
        )

        bounded = (
            "The matched-rate experiment did not resolve whether strong "
            "candidate subsampling changes finite-horizon causal amplification "
            "at the frozen ±0.15 effect scale."
        )

    verdict = {
        "validity": {
            "scientific_valid": bool(
                scientific_valid
            ),
            "construction_match_valid": bool(
                calibration_summary[
                    "construction_match_valid"
                ]
            ),
            "probe_coverage_fraction": float(
                support[
                    "coverage_fraction"
                ]
            ),
        },
        "primary_status": (
            primary_status
        ),
        "overall_status": (
            overall
        ),
        "bounded_claim": (
            bounded
        ),
        "what_this_does_not_establish": [
            "formal branching ratio",
            "criticality",
            "supercriticality",
            "phase transition",
            "coherent structure",
            "individuality",
            "organism",
            "life",
        ],
        "stop_rule": (
            "Do not alter budget fractions, horizon, construction target, "
            "calibration method or SEI to rescue the primary result."
        ),
        "next_if_supported": (
            "Map causal amplification over matched-rate selection concentration "
            "and test whether any regime approaches sustained amplification."
        ),
        "next_if_bounded": (
            "Treat finite-budget redistribution as a spatial allocation law "
            "rather than an amplification mechanism, then move to persistent "
            "material memory or individuation."
        ),
        "next_if_unresolved": (
            "Increase independent groups only if achieved MDE exceeds the "
            "frozen SEI; otherwise preserve the unresolved result."
        ),
    }

    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Bounded Chapter 26 V1 Verdict",
        verdict,
    )

    reporter.json(
        "stage-06-verdict.json",
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
