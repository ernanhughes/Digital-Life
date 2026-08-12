#!/usr/bin/env python3
"""
Digital Life — Chapter 23 V3
Causal Gain of One Attachment
=============================

WHY V3 EXISTS
-------------

Chapter 23 V1:
    pooled material-event propagation
    -> FAILED

Chapter 23 V2:
    source/sink interpretation
    -> FAILED / REVERSED once definitional d=0 effects were separated

The surviving V2 neighbourhood result was:

    attachment at x
        -> increased later attachment nearby

    loss at x
        -> decreased later attachment nearby

with rapid attenuation by distance and no directed propagation detectable at
d >= 3.

The obvious first explanation is not "emergent self-excitation".
It is the frozen attachment rule itself:

    score =
        base_bias
        + neighbor_gain * occupied_neighbor_count
        + signal_rate_gain * environment
        + anisotropy_gain * anisotropy
        - crowding_penalty * crowding

neighbor_gain > 0.

Adding one occupied cell therefore raises the support of neighbouring frontier
candidates. Removing one occupied cell lowers it.

V3 stops using observational source/control matching and makes a direct
counterfactual intervention.

QUESTION
--------

What is the causal construction gain of one forced attachment?

At the same checkpoint and same eligible frontier site x:

    FORCE branch:
        insert x as occupied

    PREVENT branch:
        leave x empty

Then evolve both branches under:
    - the same frozen Digital Crystal rule,
    - the same environment,
    - the same stream seed,
    - the same cell-keyed attachment randomness,
    - the same cell-keyed loss randomness,
    - the same finite global evaluation budget.

The only initial difference is occupancy of x.

This removes the V2 selection/anisotropy confound because the same cell is used
in both branches.

IMPORTANT SCOPE
---------------

The intervention is inserted BETWEEN completed canonical updates.
Therefore the forced cell is not immediately subject to the previous update's
loss draw. From the next canonical update onward, both branches obey the frozen
growth -> loss sequence normally.

The intervention cell itself (distance d=0) is EXCLUDED from every causal-gain
claim. d=0 is definitional because the force branch is occupied and the prevent
branch is empty at intervention time.

PRIMARY QUANTITIES
------------------

1. g_mech_1

    Analytic / mechanical expected one-step gain on ring d=1.

    For the first future update, compute the exact frontier and exact evaluated
    candidate set in each branch. For every evaluated cell y != x at d=1,
    compute its frozen attachment probability.

        g_mech_1
            =
            sum_y p_force(y)
            -
            sum_y p_prevent(y)

    This includes:
        - neighbor-gain arithmetic,
        - newly created frontier opportunity,
        - crowding,
        - anisotropy,
        - environment,
        - the exact finite-budget selected sets.

    It does NOT use the realized Bernoulli outcome.

2. g1

    Realized one-step causal gain:

        extra realized attachments
        at d=1
        during the first canonical update
        after the intervention.

3. G_H

    Finite-horizon causal construction gain:

        cumulative(
            attachments_force
            -
            attachments_prevent
        )

    over distances:
        d = 1 .. H

    and lags:
        1 .. H

    where H is frozen by profile.

    G_H is NOT automatically a formal branching ratio because it can include:
        - direct descendants,
        - descendants of descendants,
        - overlapping causal pathways,
        - finite-budget substitutions,
        - repeated local effects.

    It is therefore named:
        finite-horizon causal construction gain.

4. G_H_global

    Same cumulative attachment difference over the whole lattice excluding x.

    This is diagnostic because the finite global budget can produce distant
    substitution effects.

5. spatial causal gain

    Net extra realized attachments by:
        distance d
        lag tau

    This directly measures attenuation.

FROZEN SCIENTIFIC TESTS
-----------------------

H1 — DIRECT CAUSAL EXCITATION

    mean g1 >= +0.10 attachments
    one-sided paired sign-flip p < 0.05

Success earns:

    Forcing one eligible frontier attachment causes a positive increase in
    next-update attachment activity among its immediate neighbours under the
    frozen Digital Crystal rule and finite evaluation budget.

H2 — MECHANICAL ACCOUNTING

    Compare:
        g1 - g_mech_1

    This is primarily a calibration check, not an emergence test.

"Consistent with one-step mechanics" requires:
    abs(mean(g1 - g_mech_1)) <= 0.10
    AND the 95% bootstrap interval includes 0.

If not, investigate observer/model accounting before interpreting amplification.

H3 — MULTI-STEP AMPLIFICATION

    amplification =
        G_H - g1

    mean amplification >= +0.20 attachments
    one-sided paired sign-flip p < 0.05

Success means that the causal effect does more than the first local update:
later construction contributes additional positive gain.

Failure means:
    no scientifically meaningful positive multi-step amplification under the
    frozen horizon/effect floor.

H4 — SUBCRITICAL REFERENCE

    If:
        upper 95% CI of G_H < 1.0

    report:

        finite-horizon causal gain lies below the branching-critical reference
        of one additional event per intervention.

This is NOT a formal branching-ratio claim.

If:
        lower 95% CI of G_H > 1.0

    report:
        finite-horizon gain exceeds the branching-critical reference.

Otherwise:
        unresolved relative to 1.

This is a descriptive criticality reference only.

MECHANICAL NULL
---------------

V3 computes g_mech_1 BEFORE reading the realized first-step outcomes.

The mechanical expectation is not "zero".
The relevant comparison is:

    observed causal one-step gain
    versus
    gain mechanically expected from the frozen rule.

This prevents the Chapter 21 "flux null" mistake from recurring.

INTERVENTION-SITE SELECTION
---------------------------

No V2 source-selection is reused.

For each independent group:
    1. build a lossy finite-budget checkpoint;
    2. enumerate interior frontier cells;
    3. compute each cell's baseline attachment probability using the next
       environment value;
    4. choose predeclared probability quantiles.

Quick profile uses four probes near:
    20%, 40%, 60%, 80%

This samples low-to-high ordinary frontier opportunities without conditioning
on whether the cell would actually attach under its RNG draw.

Each probe creates a separate force/prevent pair from the same checkpoint.

Statistics are aggregated to ONE mean per group before bootstrap/sign-flip so
multiple probes from one group are not treated as independent replicates.

COMMON-RANDOM-NUMBER COUPLING
-----------------------------

The frozen model already uses:
    cell-keyed attachment draws
    cell-keyed loss draws
    keyed finite-budget selection

Both branches retain the same stream seed and step index.

Thus cells facing the same stochastic opportunity receive the same random draw.
Divergence then arises from the intervention and its downstream geometric and
budget consequences.

FORBIDDEN OVERCLAIMS
--------------------

Do not call G_H:
    branching ratio
unless direct descendant semantics are later established.

Do not call G_H < 1:
    proof of subcriticality
for the universal substrate.

Do not claim:
    critical point
    phase transition
    directed percolation
    Hawkes process
    excitable medium
    wave
    individuality
    autonomy
    organism
    life

Chapter 24 may later vary neighbor_gain and/or budget to ask whether a causal
gain transition exists. V3 keeps the substrate parameters frozen.

Requires beside this file:
    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21


Cell = Tuple[int, int]

BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
PARENT_EXPERIMENT_VERSION = ch21.EXPERIMENT_VERSION
EXPERIMENT_VERSION = "digital-crystal-causal-attachment-gain-v3"
SCHEMA_VERSION = 3
CHAPTER = 23
CHAPTER_TITLE = "Does the Process Move?"
RUN_TITLE = "Causal Gain of One Attachment"


PROFILES = {
    "smoke": {
        "groups": 8,
        "probes_per_group": 2,
        "probe_quantiles": [0.33, 0.67],
        "radius": 48,
        "initial_warmup_steps": 14,
        "lossy_pre_steps": 12,
        "horizon": 6,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 8,
        "minimum_frontier_candidates": 12,
        "minimum_direct_gain": 0.10,
        "minimum_multistep_amplification": 0.20,
        "mechanical_consistency_tolerance": 0.10,
        "alpha": 0.05,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "probes_per_group": 4,
        "probe_quantiles": [0.20, 0.40, 0.60, 0.80],
        "radius": 72,
        "initial_warmup_steps": 20,
        "lossy_pre_steps": 20,
        "horizon": 10,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 12,
        "minimum_frontier_candidates": 24,
        "minimum_direct_gain": 0.10,
        "minimum_multistep_amplification": 0.20,
        "mechanical_consistency_tolerance": 0.10,
        "alpha": 0.05,
        "bootstrap_reps": 2500,
        "signflip_permutations": 5000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "probes_per_group": 4,
        "probe_quantiles": [0.20, 0.40, 0.60, 0.80],
        "radius": 88,
        "initial_warmup_steps": 24,
        "lossy_pre_steps": 24,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 14,
        "minimum_frontier_candidates": 32,
        "minimum_direct_gain": 0.10,
        "minimum_multistep_amplification": 0.20,
        "mechanical_consistency_tolerance": 0.10,
        "alpha": 0.05,
        "bootstrap_reps": 4000,
        "signflip_permutations": 10000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "probes_per_group": 6,
        "probe_quantiles": [0.10, 0.25, 0.40, 0.60, 0.75, 0.90],
        "radius": 104,
        "initial_warmup_steps": 24,
        "lossy_pre_steps": 28,
        "horizon": 14,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 16,
        "minimum_frontier_candidates": 48,
        "minimum_direct_gain": 0.10,
        "minimum_multistep_amplification": 0.20,
        "mechanical_consistency_tolerance": 0.10,
        "alpha": 0.05,
        "bootstrap_reps": 6000,
        "signflip_permutations": 20000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Frozen rule helpers
# ============================================================================

def clone_state(
    state: ch18.MaterialCrystalState,
) -> ch18.MaterialCrystalState:
    return ch21.clone_state(state)


def frontier_cells(
    occupied: Set[Cell],
    radius: int,
) -> List[Cell]:
    return ch21.frontier_cells(
        occupied,
        radius,
    )


def attachment_probability(
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
        6.0 * theta + phase
    )

    crowding = max(
        0,
        n - 2,
    )

    score = (
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain * float(input_value)
        + crystal_params.anisotropy_gain * anisotropy
        - crystal_params.crowding_penalty * crowding
    )

    return float(
        ch18.logistic_scalar(score)
    )


def growth_step_with_evaluated(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
    int,
]:
    """
    Exact frozen Chapter 21 neutral finite-budget growth rule, returning the
    selected/evaluated set used for attachment decisions.
    """
    occupied_before = set(
        state.occupied
    )
    occupied = set(
        state.occupied
    )
    birth_time = dict(
        state.birth_time
    )

    frontier = frontier_cells(
        occupied_before,
        radius,
    )

    next_step = (
        state.step + 1
    )

    selected = ch21.select_candidates(
        frontier,
        budget,
        state.stream_seed,
        next_step,
    )

    additions: List[Cell] = []

    for cell in selected:
        p = attachment_probability(
            cell,
            occupied_before,
            input_value,
            crystal_params,
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

    selected_set = set(
        selected
    )
    addition_set = set(
        additions
    )

    assert addition_set <= selected_set

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

    return (
        out,
        additions,
        selected,
        len(frontier),
    )


def canonical_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
    loss_rate: float,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
    List[Cell],
    int,
]:
    (
        grown,
        additions,
        evaluated,
        frontier_count,
    ) = growth_step_with_evaluated(
        state,
        input_value,
        radius,
        crystal_params,
        budget,
    )

    after_loss, lost = ch21.apply_background_loss(
        grown,
        loss_rate,
    )

    return (
        after_loss,
        additions,
        lost,
        evaluated,
        frontier_count,
    )


# ============================================================================
# Checkpoint generation and intervention selection
# ============================================================================

def build_checkpoint(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group: int,
) -> Tuple[
    ch18.MaterialCrystalState,
    np.ndarray,
    float,
]:
    radius = int(
        profile["radius"]
    )
    warmup = int(
        profile["initial_warmup_steps"]
    )
    pre_steps = int(
        profile["lossy_pre_steps"]
    )
    horizon = int(
        profile["horizon"]
    )

    gseed = int(seed) + group * 1009

    env = ch18.make_environment(
        warmup
        + pre_steps
        + horizon
        + 8,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env=env,
        warmup_steps=warmup,
        stream_seed=gseed + 2,
        radius=radius,
        crystal_params=crystal_params,
        material_params=ch21.no_material_params(),
    )

    max_capacity = float(
        ch18.capacity_fraction_occupied(
            state.occupied,
            radius,
        )
    )

    for j in range(
        pre_steps
    ):
        state, _, _, _, _ = canonical_step(
            state=state,
            input_value=float(
                env[
                    warmup + j
                ]
            ),
            radius=radius,
            crystal_params=crystal_params,
            budget=int(
                profile["budget"]
            ),
            loss_rate=float(
                profile["loss_rate"]
            ),
        )

        max_capacity = max(
            max_capacity,
            float(
                ch18.capacity_fraction_occupied(
                    state.occupied,
                    radius,
                )
            ),
        )

        if not state.occupied:
            break

    future_env = np.asarray(
        env[
            warmup + pre_steps:
            warmup + pre_steps + horizon + 1
        ],
        dtype=float,
    )

    return (
        state,
        future_env,
        max_capacity,
    )


def choose_probe_cells(
    checkpoint: ch18.MaterialCrystalState,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    Tuple[Cell, float]
]:
    radius = int(
        profile["radius"]
    )
    margin = int(
        profile["interior_margin"]
    )

    frontier = [
        cell
        for cell in frontier_cells(
            checkpoint.occupied,
            radius,
        )
        if (
            cell not in checkpoint.occupied
            and ch18.hex_distance(cell)
            <= radius - margin
        )
    ]

    if len(frontier) < int(
        profile["minimum_frontier_candidates"]
    ):
        return []

    scored = sorted(
        [
            (
                cell,
                attachment_probability(
                    cell,
                    checkpoint.occupied,
                    next_input,
                    crystal_params,
                ),
            )
            for cell in frontier
        ],
        key=lambda item: (
            item[1],
            item[0],
        ),
    )

    probes: List[
        Tuple[Cell, float]
    ] = []

    used: Set[Cell] = set()

    for q in profile[
        "probe_quantiles"
    ]:
        index = int(
            round(
                float(q)
                * (
                    len(scored)
                    - 1
                )
            )
        )

        # Deterministic outward search if quantiles land on same cell.
        for offset in range(
            len(scored)
        ):
            for candidate_index in (
                index + offset,
                index - offset,
            ):
                if not (
                    0
                    <= candidate_index
                    < len(scored)
                ):
                    continue

                cell, p = scored[
                    candidate_index
                ]

                if cell in used:
                    continue

                used.add(cell)
                probes.append(
                    (
                        cell,
                        float(p),
                    )
                )
                break

            else:
                continue
            break

    return probes[
        : int(
            profile["probes_per_group"]
        )
    ]


# ============================================================================
# Intervention and one-step mechanical expectation
# ============================================================================

def force_attachment(
    checkpoint: ch18.MaterialCrystalState,
    cell: Cell,
) -> ch18.MaterialCrystalState:
    if cell in checkpoint.occupied:
        raise ValueError(
            "intervention cell already occupied"
        )

    if cell not in set(
        frontier_cells(
            checkpoint.occupied,
            10**9,
        )
    ):
        # Radius is intentionally not used here; the caller selected from the
        # real frontier. This is merely a defensive local-eligibility check.
        if not any(
            nb in checkpoint.occupied
            for nb in ch18.neighbors(cell)
        ):
            raise ValueError(
                "intervention cell is not an eligible local frontier cell"
            )

    out = clone_state(
        checkpoint
    )

    out.occupied.add(
        cell
    )
    out.birth_time[
        cell
    ] = int(
        checkpoint.step
    )

    if out.population_by_step:
        out.population_by_step[-1] = len(
            out.occupied
        )

    return out


def expected_one_step_ring1_gain(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    intervention_cell: Cell,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> dict:
    """
    Exact expected difference in NEXT-UPDATE ring-1 attachments under the
    branch-specific frontier geometry and exact branch-specific evaluated sets.

    This is an expectation over attachment Bernoulli draws only. Candidate
    selection is held to the actual frozen deterministic finite-budget rule.
    """
    radius = int(
        profile["radius"]
    )
    budget = int(
        profile["budget"]
    )

    force_frontier = frontier_cells(
        force_state.occupied,
        radius,
    )
    prevent_frontier = frontier_cells(
        prevent_state.occupied,
        radius,
    )

    next_step = int(
        prevent_state.step + 1
    )

    force_selected = ch21.select_candidates(
        force_frontier,
        budget,
        force_state.stream_seed,
        next_step,
    )
    prevent_selected = ch21.select_candidates(
        prevent_frontier,
        budget,
        prevent_state.stream_seed,
        next_step,
    )

    def expected(
        selected: Sequence[Cell],
        occupied: Set[Cell],
    ) -> Tuple[float, Dict[Cell, float]]:
        probs: Dict[Cell, float] = {}

        for cell in selected:
            if cell == intervention_cell:
                continue

            if (
                ch18.hex_distance(
                    (
                        cell[0] - intervention_cell[0],
                        cell[1] - intervention_cell[1],
                    )
                )
                != 1
            ):
                continue

            probs[cell] = attachment_probability(
                cell,
                occupied,
                next_input,
                crystal_params,
            )

        return (
            float(
                sum(
                    probs.values()
                )
            ),
            probs,
        )

    force_expected, force_probs = expected(
        force_selected,
        force_state.occupied,
    )
    prevent_expected, prevent_probs = expected(
        prevent_selected,
        prevent_state.occupied,
    )

    union = sorted(
        set(force_probs)
        | set(prevent_probs)
    )

    cell_deltas = {
        f"{cell[0]},{cell[1]}": float(
            force_probs.get(
                cell,
                0.0,
            )
            - prevent_probs.get(
                cell,
                0.0,
            )
        )
        for cell in union
    }

    return {
        "g_mech_1": float(
            force_expected
            - prevent_expected
        ),
        "force_expected_ring1_attachments": (
            force_expected
        ),
        "prevent_expected_ring1_attachments": (
            prevent_expected
        ),
        "force_frontier_count": int(
            len(force_frontier)
        ),
        "prevent_frontier_count": int(
            len(prevent_frontier)
        ),
        "immediate_frontier_opportunity_delta": int(
            len(force_frontier)
            - len(prevent_frontier)
        ),
        "force_selected_count": int(
            len(force_selected)
        ),
        "prevent_selected_count": int(
            len(prevent_selected)
        ),
        "ring1_probability_deltas": (
            cell_deltas
        ),
    }


# ============================================================================
# Paired future
# ============================================================================

def relative_distance(
    cell: Cell,
    origin: Cell,
) -> int:
    return int(
        ch18.hex_distance(
            (
                cell[0] - origin[0],
                cell[1] - origin[1],
            )
        )
    )


@dataclass
class ProbeResult:
    group: int
    probe: int
    quantile: float
    intervention_cell: Cell
    baseline_probability: float
    g_mech_1: float
    g1: float
    G_H: float
    G_H_global: float
    amplification: float
    immediate_frontier_delta: int
    lag_gain: List[float]
    distance_gain: List[float]
    distance_lag_gain: List[List[float]]
    force_population_end: int
    prevent_population_end: int
    force_total_attachments: int
    prevent_total_attachments: int
    max_capacity_fraction: float


def run_probe(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    intervention_cell: Cell,
    baseline_probability: float,
    quantile: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    group: int,
    probe_index: int,
) -> ProbeResult:
    horizon = int(
        profile["horizon"]
    )
    radius = int(
        profile["radius"]
    )

    prevent_state = clone_state(
        checkpoint
    )
    force_state = force_attachment(
        checkpoint,
        intervention_cell,
    )

    mech = expected_one_step_ring1_gain(
        force_state=force_state,
        prevent_state=prevent_state,
        intervention_cell=intervention_cell,
        next_input=float(
            future_env[0]
        ),
        profile=profile,
        crystal_params=crystal_params,
    )

    distance_lag = np.zeros(
        (
            horizon,
            horizon + 1,
        ),
        dtype=float,
    )

    lag_gain: List[float] = []
    global_lag_gain: List[float] = []

    force_total = 0
    prevent_total = 0

    max_capacity = max(
        float(
            ch18.capacity_fraction_occupied(
                force_state.occupied,
                radius,
            )
        ),
        float(
            ch18.capacity_fraction_occupied(
                prevent_state.occupied,
                radius,
            )
        ),
    )

    for lag in range(
        1,
        horizon + 1,
    ):
        (
            force_state,
            force_additions,
            _force_lost,
            _force_eval,
            _force_frontier,
        ) = canonical_step(
            state=force_state,
            input_value=float(
                future_env[
                    lag - 1
                ]
            ),
            radius=radius,
            crystal_params=crystal_params,
            budget=int(
                profile["budget"]
            ),
            loss_rate=float(
                profile["loss_rate"]
            ),
        )

        (
            prevent_state,
            prevent_additions,
            _prevent_lost,
            _prevent_eval,
            _prevent_frontier,
        ) = canonical_step(
            state=prevent_state,
            input_value=float(
                future_env[
                    lag - 1
                ]
            ),
            radius=radius,
            crystal_params=crystal_params,
            budget=int(
                profile["budget"]
            ),
            loss_rate=float(
                profile["loss_rate"]
            ),
        )

        force_total += len(
            force_additions
        )
        prevent_total += len(
            prevent_additions
        )

        force_by_d = np.zeros(
            horizon + 1,
            dtype=float,
        )
        prevent_by_d = np.zeros(
            horizon + 1,
            dtype=float,
        )

        for cell in force_additions:
            d = relative_distance(
                cell,
                intervention_cell,
            )
            if (
                1
                <= d
                <= horizon
            ):
                force_by_d[
                    d
                ] += 1.0

        for cell in prevent_additions:
            d = relative_distance(
                cell,
                intervention_cell,
            )
            if (
                1
                <= d
                <= horizon
            ):
                prevent_by_d[
                    d
                ] += 1.0

        delta_by_d = (
            force_by_d
            - prevent_by_d
        )

        distance_lag[
            lag - 1,
            :
        ] = delta_by_d

        lag_gain.append(
            float(
                np.sum(
                    delta_by_d[
                        1:
                    ]
                )
            )
        )

        # Global diagnostic excludes intervention site.
        force_global = sum(
            cell != intervention_cell
            for cell in force_additions
        )
        prevent_global = sum(
            cell != intervention_cell
            for cell in prevent_additions
        )

        global_lag_gain.append(
            float(
                force_global
                - prevent_global
            )
        )

        max_capacity = max(
            max_capacity,
            float(
                ch18.capacity_fraction_occupied(
                    force_state.occupied,
                    radius,
                )
            ),
            float(
                ch18.capacity_fraction_occupied(
                    prevent_state.occupied,
                    radius,
                )
            ),
        )

    distance_gain = np.sum(
        distance_lag,
        axis=0,
    )

    g1 = float(
        distance_lag[
            0,
            1,
        ]
    )

    G_H = float(
        np.sum(
            distance_lag[
                :,
                1:
            ]
        )
    )

    G_H_global = float(
        np.sum(
            global_lag_gain
        )
    )

    return ProbeResult(
        group=int(group),
        probe=int(
            probe_index
        ),
        quantile=float(
            quantile
        ),
        intervention_cell=(
            int(
                intervention_cell[0]
            ),
            int(
                intervention_cell[1]
            ),
        ),
        baseline_probability=float(
            baseline_probability
        ),
        g_mech_1=float(
            mech[
                "g_mech_1"
            ]
        ),
        g1=g1,
        G_H=G_H,
        G_H_global=G_H_global,
        amplification=float(
            G_H - g1
        ),
        immediate_frontier_delta=int(
            mech[
                "immediate_frontier_opportunity_delta"
            ]
        ),
        lag_gain=[
            float(x)
            for x in lag_gain
        ],
        distance_gain=[
            float(x)
            for x in distance_gain
        ],
        distance_lag_gain=[
            [
                float(value)
                for value in row
            ]
            for row in distance_lag
        ],
        force_population_end=int(
            len(
                force_state.occupied
            )
        ),
        prevent_population_end=int(
            len(
                prevent_state.occupied
            )
        ),
        force_total_attachments=int(
            force_total
        ),
        prevent_total_attachments=int(
            prevent_total
        ),
        max_capacity_fraction=float(
            max_capacity
        ),
    )


# ============================================================================
# Statistics
# ============================================================================

def group_means(
    results: Sequence[ProbeResult],
    field: str,
) -> List[float]:
    by_group: Dict[
        int,
        List[float],
    ] = {}

    for result in results:
        by_group.setdefault(
            result.group,
            [],
        ).append(
            float(
                getattr(
                    result,
                    field,
                )
            )
        )

    return [
        float(
            np.mean(values)
        )
        for _, values in sorted(
            by_group.items()
        )
        if values
    ]


def group_mean_custom(
    results: Sequence[ProbeResult],
    fn,
) -> List[float]:
    by_group: Dict[
        int,
        List[float],
    ] = {}

    for result in results:
        by_group.setdefault(
            result.group,
            [],
        ).append(
            float(
                fn(
                    result
                )
            )
        )

    return [
        float(
            np.mean(values)
        )
        for _, values in sorted(
            by_group.items()
        )
        if values
    ]


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            float(value)
            for value in values
            if math.isfinite(
                float(value)
            )
        ],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "n": 0,
            "mean": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
            "half_width": float("nan"),
        }

    rng = np.random.default_rng(
        seed
    )

    boot = np.empty(
        int(reps),
        dtype=float,
    )

    for i in range(
        int(reps)
    ):
        sample = rng.choice(
            arr,
            size=len(arr),
            replace=True,
        )

        boot[i] = float(
            np.mean(
                sample
            )
        )

    low = float(
        np.quantile(
            boot,
            0.025,
        )
    )
    high = float(
        np.quantile(
            boot,
            0.975,
        )
    )

    return {
        "n": int(
            len(arr)
        ),
        "mean": float(
            np.mean(arr)
        ),
        "ci95_low": low,
        "ci95_high": high,
        "half_width": float(
            (
                high - low
            )
            / 2.0
        ),
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            float(value)
            for value in values
            if math.isfinite(
                float(value)
            )
        ],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "n": 0,
            "observed_mean": float("nan"),
            "p_value": float("nan"),
        }

    observed = float(
        np.mean(
            arr
        )
    )

    rng = np.random.default_rng(
        seed
    )

    null = np.empty(
        int(permutations),
        dtype=float,
    )

    for i in range(
        int(permutations)
    ):
        signs = rng.choice(
            np.asarray(
                [-1.0, 1.0]
            ),
            size=len(arr),
        )

        null[i] = float(
            np.mean(
                arr * signs
            )
        )

    p = (
        1.0
        + float(
            np.sum(
                null >= observed
            )
        )
    ) / (
        len(null)
        + 1.0
    )

    return {
        "n": int(
            len(arr)
        ),
        "observed_mean": observed,
        "p_value": float(
            p
        ),
        "permutations": int(
            permutations
        ),
        "null_mean": float(
            np.mean(
                null
            )
        ),
        "null_q95": float(
            np.quantile(
                null,
                0.95,
            )
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
        self.sections: List[
            Tuple[str, str]
        ] = []

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
            / "ch23-causal-attachment-gain-v3-full-report.md"
        )

        parts = [
            "# Chapter 23 — Causal Gain of One Attachment (V3)",
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
            parts.extend([
                "---",
                "",
                f"## {title}",
                "",
                body,
                "",
            ])

        path.write_text(
            "\n".join(parts),
            encoding="utf-8",
        )

        return path


# ============================================================================
# Stage 0 — frozen protocol
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
    seed: int,
) -> dict:
    result = {
        "role": (
            "FRESH COUNTERFACTUAL CAUSAL-GAIN EXPERIMENT"
        ),
        "fresh_seed": int(
            seed
        ),
        "v2_interpretive_correction": (
            "d=0 source/control effects are definitional and excluded. "
            "V3 tests the same frontier cell in force/prevent branches."
        ),
        "intervention": (
            "Insert one eligible frontier cell into FORCE between completed "
            "updates; leave the same cell empty in PREVENT."
        ),
        "d0_rule": (
            "Intervention site excluded from every causal-gain claim."
        ),
        "probe_quantiles": list(
            profile[
                "probe_quantiles"
            ]
        ),
        "probes_per_group": int(
            profile[
                "probes_per_group"
            ]
        ),
        "horizon": int(
            profile[
                "horizon"
            ]
        ),
        "g_mech_1": (
            "Exact branch-specific expected next-update ring-1 attachment "
            "difference under frozen probabilities and exact finite-budget "
            "evaluated sets."
        ),
        "g1": (
            "Realized force-minus-prevent next-update ring-1 attachments."
        ),
        "G_H": (
            "Finite-horizon force-minus-prevent attachments over d=1..H, "
            "lags=1..H. Not called a formal branching ratio."
        ),
        "G_H_global": (
            "Whole-lattice attachment difference excluding intervention site; "
            "diagnostic for finite-budget substitutions."
        ),
        "H1_direct_causal_excitation": {
            "minimum_mean_g1": float(
                profile[
                    "minimum_direct_gain"
                ]
            ),
            "alpha": float(
                profile[
                    "alpha"
                ]
            ),
        },
        "H2_mechanical_accounting": {
            "comparison": (
                "g1 - g_mech_1"
            ),
            "consistency_tolerance": float(
                profile[
                    "mechanical_consistency_tolerance"
                ]
            ),
            "requires_ci_include_zero": True,
        },
        "H3_multistep_amplification": {
            "quantity": "G_H - g1",
            "minimum_mean_amplification": float(
                profile[
                    "minimum_multistep_amplification"
                ]
            ),
            "alpha": float(
                profile[
                    "alpha"
                ]
            ),
        },
        "H4_branching_critical_reference": (
            "Compare 95% CI of G_H with 1.0 descriptively. "
            "G_H is not asserted to be a formal branching ratio."
        ),
        "scientific_boundary": (
            "Causal construction gain only. No formal branching ratio, "
            "critical point, phase transition, directed percolation, Hawkes, "
            "excitable medium, wave, individuality, autonomy, organism, or "
            "life claim."
        ),
        "status": (
            "FROZEN"
            if profile[
                "scientific"
            ]
            else "ENGINEERING_SMOKE_ONLY"
        ),
    }

    reporter.json(
        "stage-00-protocol.json",
        result,
    )

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen V3 Causal-Gain Protocol",
        result,
    )

    return result


# ============================================================================
# Stage 1 — run interventions
# ============================================================================

def stage_1_interventions(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[ProbeResult],
    dict,
]:
    results: List[
        ProbeResult
    ] = []

    skipped_groups = 0
    maximum_capacity = 0.0

    for group in tqdm(
        range(
            int(
                profile[
                    "groups"
                ]
            )
        ),
        desc="Chapter 23 V3 force/prevent groups",
    ):
        (
            checkpoint,
            future_env,
            checkpoint_capacity,
        ) = build_checkpoint(
            profile,
            crystal_params,
            seed,
            group,
        )

        maximum_capacity = max(
            maximum_capacity,
            checkpoint_capacity,
        )

        if not checkpoint.occupied:
            skipped_groups += 1
            continue

        probes = choose_probe_cells(
            checkpoint,
            float(
                future_env[0]
            ),
            profile,
            crystal_params,
        )

        if (
            len(probes)
            < int(
                profile[
                    "probes_per_group"
                ]
            )
        ):
            skipped_groups += 1
            continue

        for probe_index, (
            cell,
            baseline_p,
        ) in enumerate(
            probes
        ):
            result = run_probe(
                checkpoint=checkpoint,
                future_env=future_env,
                intervention_cell=cell,
                baseline_probability=baseline_p,
                quantile=float(
                    profile[
                        "probe_quantiles"
                    ][
                        probe_index
                    ]
                ),
                profile=profile,
                crystal_params=crystal_params,
                group=group,
                probe_index=probe_index,
            )

            maximum_capacity = max(
                maximum_capacity,
                result.max_capacity_fraction,
            )

            results.append(
                result
            )

    groups_used = len(
        set(
            result.group
            for result in results
        )
    )

    result_payload = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "groups_used": int(
            groups_used
        ),
        "skipped_groups": int(
            skipped_groups
        ),
        "total_probes": int(
            len(results)
        ),
        "probes_per_used_group": (
            float(
                len(results)
                / max(
                    1,
                    groups_used,
                )
            )
        ),
        "maximum_capacity_fraction": float(
            maximum_capacity
        ),
        "max_allowed_capacity_fraction": float(
            profile[
                "max_capacity_fraction"
            ]
        ),
        "capacity_gate_passed": bool(
            maximum_capacity
            < profile[
                "max_capacity_fraction"
            ]
        ),
        "minimum_group_coverage_gate": bool(
            groups_used
            >= max(
                4,
                int(
                    0.80
                    * profile[
                        "groups"
                    ]
                ),
            )
        ),
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-interventions.json",
        result_payload,
    )

    reporter.stage(
        "stage-01-interventions.md",
        "Stage 1 — Force/Prevent Attachment Interventions",
        result_payload,
    )

    return (
        results,
        result_payload,
    )


# ============================================================================
# Stage 2 — causal-gain measurements
# ============================================================================

def stage_2_measurements(
    reporter: Reporter,
    profile: dict,
    results: Sequence[ProbeResult],
    seed: int,
    image_dir: Path,
) -> dict:
    g_mech_groups = group_means(
        results,
        "g_mech_1",
    )
    g1_groups = group_means(
        results,
        "g1",
    )
    GH_groups = group_means(
        results,
        "G_H",
    )
    GH_global_groups = group_means(
        results,
        "G_H_global",
    )
    amplification_groups = group_means(
        results,
        "amplification",
    )
    mechanical_delta_groups = group_mean_custom(
        results,
        lambda r: (
            r.g1
            - r.g_mech_1
        ),
    )
    frontier_delta_groups = group_means(
        results,
        "immediate_frontier_delta",
    )

    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    payload = {
        "g_mech_1": bootstrap_mean_ci(
            g_mech_groups,
            reps,
            seed + 301,
        ),
        "g1_realized_ring1": bootstrap_mean_ci(
            g1_groups,
            reps,
            seed + 302,
        ),
        "g1_minus_g_mech_1": bootstrap_mean_ci(
            mechanical_delta_groups,
            reps,
            seed + 303,
        ),
        "G_H_local": bootstrap_mean_ci(
            GH_groups,
            reps,
            seed + 304,
        ),
        "G_H_global": bootstrap_mean_ci(
            GH_global_groups,
            reps,
            seed + 305,
        ),
        "multistep_amplification_GH_minus_g1": (
            bootstrap_mean_ci(
                amplification_groups,
                reps,
                seed + 306,
            )
        ),
        "immediate_frontier_opportunity_delta": (
            bootstrap_mean_ci(
                frontier_delta_groups,
                reps,
                seed + 307,
            )
        ),
        "scope": (
            "Statistics use one mean per independent group; multiple probes "
            "within a group are not treated as independent replicates."
        ),
    }

    # Population distance-lag causal gain matrix.
    horizon = int(
        profile[
            "horizon"
        ]
    )

    group_ids = sorted(
        set(
            result.group
            for result in results
        )
    )

    group_matrices: List[
        np.ndarray
    ] = []

    for group in group_ids:
        matrices = [
            np.asarray(
                result.distance_lag_gain,
                dtype=float,
            )
            for result in results
            if result.group == group
        ]

        if matrices:
            group_matrices.append(
                np.mean(
                    np.stack(
                        matrices,
                        axis=0,
                    ),
                    axis=0,
                )
            )

    population_matrix = np.mean(
        np.stack(
            group_matrices,
            axis=0,
        ),
        axis=0,
    )

    population_lag_gain = np.sum(
        population_matrix[
            :,
            1:
        ],
        axis=1,
    )

    population_distance_gain = np.sum(
        population_matrix,
        axis=0,
    )

    payload[
        "population_distance_lag_gain"
    ] = population_matrix.tolist()

    payload[
        "population_gain_by_lag"
    ] = [
        float(x)
        for x in population_lag_gain
    ]

    payload[
        "population_gain_by_distance"
    ] = [
        float(x)
        for x in population_distance_gain
    ]

    # Probe-stratified diagnostics.
    payload[
        "probe_probability_strata"
    ] = []

    for probe_index in range(
        int(
            profile[
                "probes_per_group"
            ]
        )
    ):
        subset = [
            result
            for result in results
            if result.probe == probe_index
        ]

        if not subset:
            continue

        payload[
            "probe_probability_strata"
        ].append({
            "probe": int(
                probe_index
            ),
            "quantile": float(
                profile[
                    "probe_quantiles"
                ][
                    probe_index
                ]
            ),
            "mean_baseline_probability": float(
                np.mean(
                    [
                        result.baseline_probability
                        for result in subset
                    ]
                )
            ),
            "mean_g_mech_1": float(
                np.mean(
                    [
                        result.g_mech_1
                        for result in subset
                    ]
                )
            ),
            "mean_g1": float(
                np.mean(
                    [
                        result.g1
                        for result in subset
                    ]
                )
            ),
            "mean_G_H": float(
                np.mean(
                    [
                        result.G_H
                        for result in subset
                    ]
                )
            ),
        })

    reporter.json(
        "stage-02-causal-gain.json",
        payload,
    )

    reporter.stage(
        "stage-02-causal-gain.md",
        "Stage 2 — Causal-Gain Measurements",
        payload,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Distance-lag heat map.
    fig, ax = plt.subplots(
        figsize=(9, 5),
    )

    im = ax.imshow(
        population_matrix[
            :,
            1:
        ].T,
        aspect="auto",
        origin="lower",
    )

    ax.set_xlabel(
        "Lag after intervention"
    )
    ax.set_ylabel(
        "Hex distance from intervention"
    )
    ax.set_xticks(
        np.arange(
            horizon
        )
    )
    ax.set_xticklabels(
        np.arange(
            1,
            horizon + 1,
        )
    )
    ax.set_yticks(
        np.arange(
            horizon
        )
    )
    ax.set_yticklabels(
        np.arange(
            1,
            horizon + 1,
        )
    )
    ax.set_title(
        "Chapter 23 V3: force − prevent attachment gain"
    )

    fig.colorbar(
        im,
        ax=ax,
        label=(
            "Extra realized attachments"
        ),
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch23-v3-distance-lag-causal-gain.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    # Gain by lag.
    fig, ax = plt.subplots(
        figsize=(8, 5),
    )

    ax.plot(
        np.arange(
            1,
            horizon + 1,
        ),
        population_lag_gain,
        marker="o",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Lag after intervention"
    )
    ax.set_ylabel(
        "Extra attachments across d=1..H"
    )
    ax.set_title(
        "Chapter 23 V3: causal construction gain by lag"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch23-v3-gain-by-lag.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    # Gain by distance.
    fig, ax = plt.subplots(
        figsize=(8, 5),
    )

    ax.plot(
        np.arange(
            1,
            horizon + 1,
        ),
        population_distance_gain[
            1:
        ],
        marker="o",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Hex distance from intervention"
    )
    ax.set_ylabel(
        "Cumulative extra attachments"
    )
    ax.set_title(
        "Chapter 23 V3: spatial attenuation of causal gain"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch23-v3-gain-by-distance.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    return payload


# ============================================================================
# Stage 3 — frozen hypothesis verdicts
# ============================================================================

def stage_3_verdicts(
    reporter: Reporter,
    profile: dict,
    results: Sequence[ProbeResult],
    stage1: dict,
    stage2: dict,
    seed: int,
) -> dict:
    alpha = float(
        profile[
            "alpha"
        ]
    )

    g1_groups = group_means(
        results,
        "g1",
    )

    amplification_groups = group_means(
        results,
        "amplification",
    )

    direct_test = signflip_greater(
        g1_groups,
        int(
            profile[
                "signflip_permutations"
            ]
        ),
        seed + 401,
    )

    amplification_test = signflip_greater(
        amplification_groups,
        int(
            profile[
                "signflip_permutations"
            ]
        ),
        seed + 402,
    )

    g1_summary = stage2[
        "g1_realized_ring1"
    ]

    delta_summary = stage2[
        "g1_minus_g_mech_1"
    ]

    GH_summary = stage2[
        "G_H_local"
    ]

    amp_summary = stage2[
        "multistep_amplification_GH_minus_g1"
    ]

    H1 = bool(
        stage1[
            "capacity_gate_passed"
        ]
        and stage1[
            "minimum_group_coverage_gate"
        ]
        and g1_summary[
            "mean"
        ]
        >= profile[
            "minimum_direct_gain"
        ]
        and g1_summary[
            "ci95_low"
        ]
        > 0.0
        and direct_test[
            "p_value"
        ]
        < alpha
    )

    H2_mechanical_consistent = bool(
        abs(
            delta_summary[
                "mean"
            ]
        )
        <= profile[
            "mechanical_consistency_tolerance"
        ]
        and delta_summary[
            "ci95_low"
        ]
        <= 0.0
        <= delta_summary[
            "ci95_high"
        ]
    )

    H3 = bool(
        amp_summary[
            "mean"
        ]
        >= profile[
            "minimum_multistep_amplification"
        ]
        and amp_summary[
            "ci95_low"
        ]
        > 0.0
        and amplification_test[
            "p_value"
        ]
        < alpha
    )

    if (
        math.isfinite(
            GH_summary[
                "ci95_high"
            ]
        )
        and GH_summary[
            "ci95_high"
        ]
        < 1.0
    ):
        H4_reference = (
            "BELOW_ONE"
        )
    elif (
        math.isfinite(
            GH_summary[
                "ci95_low"
            ]
        )
        and GH_summary[
            "ci95_low"
        ]
        > 1.0
    ):
        H4_reference = (
            "ABOVE_ONE"
        )
    else:
        H4_reference = (
            "UNRESOLVED_AROUND_ONE"
        )

    payload = {
        "validity": {
            "capacity_gate_passed": bool(
                stage1[
                    "capacity_gate_passed"
                ]
            ),
            "group_coverage_gate_passed": bool(
                stage1[
                    "minimum_group_coverage_gate"
                ]
            ),
            "valid_for_scientific_interpretation": bool(
                stage1[
                    "capacity_gate_passed"
                ]
                and stage1[
                    "minimum_group_coverage_gate"
                ]
            ),
        },
        "H1_direct_causal_excitation": {
            "minimum_effect": float(
                profile[
                    "minimum_direct_gain"
                ]
            ),
            "summary": g1_summary,
            "signflip": direct_test,
            "status": (
                "SUPPORTED"
                if H1
                else "FAILED"
            ),
        },
        "H2_one_step_mechanical_accounting": {
            "quantity": (
                "g1 - g_mech_1"
            ),
            "tolerance": float(
                profile[
                    "mechanical_consistency_tolerance"
                ]
            ),
            "summary": delta_summary,
            "status": (
                "CONSISTENT_WITH_MECHANICS"
                if H2_mechanical_consistent
                else "NOT_ACCOUNTED_FOR_WITHIN_TOLERANCE"
            ),
            "interpretation": (
                "Calibration/accounting check, not an emergence claim."
            ),
        },
        "H3_multistep_amplification": {
            "quantity": (
                "G_H - g1"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_multistep_amplification"
                ]
            ),
            "summary": amp_summary,
            "signflip": amplification_test,
            "status": (
                "SUPPORTED"
                if H3
                else "FAILED"
            ),
        },
        "H4_branching_critical_reference": {
            "G_H_summary": GH_summary,
            "reference_value": 1.0,
            "status": H4_reference,
            "interpretation_boundary": (
                "G_H is finite-horizon causal construction gain, not a "
                "formal branching ratio."
            ),
        },
    }

    reporter.json(
        "stage-03-verdicts.json",
        payload,
    )

    reporter.stage(
        "stage-03-verdicts.md",
        "Stage 3 — Frozen V3 Hypothesis Verdicts",
        payload,
    )

    return payload


# ============================================================================
# Stage 4 — bounded chapter verdict
# ============================================================================

def stage_4_bounded_verdict(
    reporter: Reporter,
    profile: dict,
    stage3: dict,
) -> dict:
    valid = bool(
        stage3[
            "validity"
        ][
            "valid_for_scientific_interpretation"
        ]
    )

    H1 = (
        stage3[
            "H1_direct_causal_excitation"
        ][
            "status"
        ]
        == "SUPPORTED"
    )

    H2 = (
        stage3[
            "H2_one_step_mechanical_accounting"
        ][
            "status"
        ]
        == "CONSISTENT_WITH_MECHANICS"
    )

    H3 = (
        stage3[
            "H3_multistep_amplification"
        ][
            "status"
        ]
        == "SUPPORTED"
    )

    reference = stage3[
        "H4_branching_critical_reference"
    ][
        "status"
    ]

    if not profile[
        "scientific"
    ]:
        status = (
            "ENGINEERING_SMOKE_ONLY"
        )
        bounded = (
            "Smoke profile completed. No scientific conclusion is eligible."
        )

    elif not valid:
        status = (
            "INVALID_FOR_SCIENTIFIC_INTERPRETATION"
        )
        bounded = (
            "One or more frozen validity gates failed. Do not interpret the "
            "causal-gain hypotheses."
        )

    elif H1 and H2 and not H3:
        status = (
            "DIRECT_CAUSAL_GAIN_MECHANICALLY_ACCOUNTED_NO_AMPLIFICATION"
        )
        bounded = (
            "Forcing one eligible Digital Crystal attachment caused a "
            "positive next-update increase in neighbouring realized "
            "attachment, and the one-step magnitude was consistent with the "
            "mechanical expectation from the frozen local rule within the "
            "predeclared tolerance. The frozen horizon did not establish "
            "additional scientifically meaningful multi-step amplification."
        )

    elif H1 and H3:
        status = (
            "DIRECT_CAUSAL_GAIN_WITH_MULTISTEP_AMPLIFICATION"
        )
        bounded = (
            "Forcing one eligible Digital Crystal attachment caused a "
            "positive next-update increase in neighbouring construction and "
            "the causal effect accumulated additional positive gain over the "
            "frozen horizon. The finite-horizon gain must not yet be called a "
            "formal branching ratio."
        )

    elif H1:
        status = (
            "DIRECT_CAUSAL_GAIN_SUPPORTED"
        )
        bounded = (
            "Forcing one eligible frontier attachment caused a positive "
            "next-update increase in neighbouring attachment under the frozen "
            "Digital Crystal dynamics. Mechanical accounting or later "
            "amplification did not satisfy every stronger frozen criterion."
        )

    else:
        status = (
            "DIRECT_CAUSAL_GAIN_FAILED"
        )
        bounded = (
            "The fresh force/prevent intervention did not establish the "
            "predeclared minimum positive next-update causal construction gain."
        )

    payload = {
        "status": status,
        "bounded_claim": bounded,
        "critical_reference": reference,
        "critical_reference_note": (
            "BELOW_ONE means only that the 95% CI of finite-horizon causal "
            "construction gain lies below 1. It does not establish a formal "
            "subcritical branching process."
        ),
        "what_this_does_not_establish": [
            "formal branching ratio",
            "critical point",
            "phase transition",
            "directed percolation",
            "Hawkes process",
            "excitable medium",
            "wave",
            "individuality",
            "autonomy",
            "organism",
            "life",
        ],
        "next_if_gain_below_one": (
            "Close Chapter 23 around measured local causal gain and rapid "
            "attenuation. Chapter 24 can then freeze a neighbor_gain sweep, "
            "with budget fixed, to ask whether a causal-gain transition exists."
        ),
        "next_if_gain_above_one": (
            "Freshly confirm causal gain before any criticality language, then "
            "map spatial/temporal persistence and define direct descendant "
            "semantics."
        ),
    }

    reporter.json(
        "stage-04-bounded-verdict.json",
        payload,
    )

    reporter.stage(
        "stage-04-bounded-verdict.md",
        "Stage 4 — Bounded Chapter 23 V3 Verdict",
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
        default="quick",
    )

    parser.add_argument(
        "--seed",
        type=int,
        # Fresh relative to V1=20260902, V2=20260903.
        default=20260904,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch23-causal-attachment-gain-v3"
        ),
    )

    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path(
            "static/images/books/digital-life"
        ),
    )

    args = parser.parse_args()

    profile = dict(
        PROFILES[
            args.profile
        ]
    )

    crystal_params = (
        ch18.CrystalParams()
    )

    reporter = Reporter(
        args.report_dir
    )

    metadata = {
        "base_model_version": (
            BASE_MODEL_VERSION
        ),
        "parent_experiment_version": (
            PARENT_EXPERIMENT_VERSION
        ),
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
        "run_title": RUN_TITLE,
        "run_type": (
            "FRESH FORCE/PREVENT COUNTERFACTUAL CAUSAL-GAIN EXPERIMENT"
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "previous_seeds": {
            "v1": 20260902,
            "v2": 20260903,
        },
        "fresh_seed": bool(
            int(
                args.seed
            )
            not in {
                20260902,
                20260903,
            }
        ),
        "frozen_model_parameters": {
            "base_bias": float(
                crystal_params.base_bias
            ),
            "neighbor_gain": float(
                crystal_params.neighbor_gain
            ),
            "signal_rate_gain": float(
                crystal_params.signal_rate_gain
            ),
            "anisotropy_gain": float(
                crystal_params.anisotropy_gain
            ),
            "signal_phase_gain": float(
                crystal_params.signal_phase_gain
            ),
            "crowding_penalty": float(
                crystal_params.crowding_penalty
            ),
            "loss_rate": float(
                profile[
                    "loss_rate"
                ]
            ),
            "budget": int(
                profile[
                    "budget"
                ]
            ),
        },
        "canonical_rules_modified": False,
        "intervention_only": (
            "One frontier cell inserted in FORCE between completed updates; "
            "same checkpoint unchanged in PREVENT."
        ),
        "started_at_unix": float(
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 23 V3 — CAUSAL GAIN OF ONE ATTACHMENT"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"probes/group={profile['probes_per_group']} "
        f"horizon={profile['horizon']} "
        f"budget={profile['budget']} "
        f"loss={profile['loss_rate']} "
        f"seed={args.seed}"
    )
    print("=" * 78)

    stage_0_protocol(
        reporter,
        profile,
        args.seed,
    )

    results, s1 = stage_1_interventions(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    if not results:
        raise RuntimeError(
            "No usable V3 interventions were generated."
        )

    s2 = stage_2_measurements(
        reporter,
        profile,
        results,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_verdicts(
        reporter,
        profile,
        results,
        s1,
        s2,
        args.seed,
    )

    s4 = stage_4_bounded_verdict(
        reporter,
        profile,
        s3,
    )

    metadata[
        "finished_at_unix"
    ] = float(
        time.time()
    )
    metadata[
        "final_status"
    ] = s4[
        "status"
    ]
    metadata[
        "critical_reference"
    ] = s4[
        "critical_reference"
    ]

    reporter.json(
        "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()
    print("=" * 78)
    print(
        f"FINAL STATUS: {s4['status']}"
    )
    print(
        f"CRITICAL REFERENCE: {s4['critical_reference']}"
    )
    print(
        s4[
            "bounded_claim"
        ]
    )
    print(
        f"Report: {report}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
