#!/usr/bin/env python3
"""
Digital Life — Chapter 23 V5
Retained State, Corrected Transient Consequence, and Local Gain
===============================================================

PURPOSE
-------

V4 decomposed the causal consequence of one forced frontier attachment into:

    immediate local mechanics
    transient downstream consequence
    consequence when the initiating state is not experimentally removed
    possible long-lag growth-rate offset

A construct-validity audit found one defect in V4's transient control:

    PREVENT could reattach x during the first causal exposure,
    while TRANSIENT then deleted x only from its own branch.

That could create a sign-reversed focal-state difference exactly where the
experiment intended to equalize the focal state.

V5 is a construct-validity correction only. It keeps the frozen model,
profiles, horizon, probe strata, scientific thresholds, and group-level
inference conventions. It back-ports the corrected intervention semantics
used later in Chapter 27 V2.

CORRECTED INTERVENTION
----------------------

At the frozen checkpoint:

    FORCE-DERIVED STATE
        x is inserted as occupied.

    PREVENT STATE
        x remains empty.

No ordinary loss is applied between intervention delivery and the first causal
growth exposure.

At lag 1 growth:

    FORCE / RETAINED / TRANSIENT
        x is present as an occupied neighbour for the full growth exposure.

    PREVENT
        x is explicitly removed from the frontier before finite-budget
        selection, so x cannot attach during the exposure.

Ordinary background loss is applied AFTER lag-1 growth in every branch.

After lag 1 growth + loss:

    TRANSIENT
        x is forcibly removed if still occupied.

    PREVENT
        x is explicitly removed as a safety/equalization operation.

    Assertions require:
        x absent from TRANSIENT
        x absent from PREVENT

At lags 2..H:

    TRANSIENT and PREVENT return to identical ordinary update rules.
    x may later reoccupy naturally in either branch.
    Such reoccupation is a downstream consequence, not intervention
    contamination.

RETAINED ARM
------------

The historical V4 field name "persistent" is retained internally in a few
dataclasses for compatibility, but the scientific arm is RETAINED:

    RETAINED
        x is not experimentally removed after the intervention.

It is NOT clamped occupied.

Ordinary loss may remove x and ordinary dynamics may later reoccupy it.
V5 therefore reports focal-cell residence diagnostics explicitly.

PRIMARY OBJECTS
---------------

For each force-derived arm A in {retained, transient}:

    gain_A(tau)
        =
        attachments_A(tau)
        -
        attachments_prevent(tau)

excluding the intervention cell x itself.

Local gain:
    distance 1 .. H around x.

Global gain:
    whole lattice excluding x.

Far-field gain:
    global gain - local gain.

Cumulative gain:

    G_A(H)
        =
        sum_{tau=1..H} gain_A(tau)

The transient branch now receives exactly one guaranteed causal growth
exposure from x before focal-state equalization.

MECHANICAL ONE-STEP EXPECTATION
-------------------------------

g_mech_1 is computed before lag-1 Bernoulli realization from the exact
branch-specific finite-budget candidate sets.

At lag 1 the PREVENT candidate pool explicitly excludes x before selection,
matching the corrected realized intervention.

The realized lag-1 ring-one gain g1 is then compared with g_mech_1.

TRANSIENT CONVERGENCE
---------------------

Transient tail is practically converged if:

    abs(late-window mean) < 0.02 attachments/update

AND

    95% CI lies inside [-0.04, +0.04]

This is a practical convergence criterion, not mathematical proof.

RETAINED LATE OFFSET
--------------------

A retained-arm positive late offset is supported only if BOTH:

    retained late-window mean > +0.02 attachments/update
    95% bootstrap CI lower bound > 0

AND

    retained fitted c > 0
    95% bootstrap CI lower bound > 0

The fit remains descriptive:

    gain(tau) = A * exp(-tau/lambda) + c

TRANSIENT CUMULATIVE CONSEQUENCE
--------------------------------

V5 reports whether G_transient(H) itself has a 95% CI above zero separately
from whether its late accumulation rate converges.

These are different claims:

    positive finite cumulative consequence
    !=
    continuing positive accumulation rate

BRANCHING-CRITICAL REFERENCE
----------------------------

Only G_transient(30) is compared descriptively with 1.

This remains a reference, NOT a branching ratio and NOT evidence for
criticality, subcriticality, or a phase transition.

PROBE STRATA / GEOMETRY
-----------------------

V5 keeps V4's frozen probability-quantile probes and geometry diagnostics.

Because the V4 contamination audit suggested unequal contamination across
probe strata, V5 reports all corrected stratum results again rather than
filtering or reusing V4 estimates.

FRESHNESS
---------

Default V5 seed:
    20260906

Previous:
    V1 20260902
    V2 20260903
    V3 20260904
    V4 20260905

V5 therefore reruns the corrected control on fresh stochastic realizations.

FORBIDDEN OVERCLAIMS
--------------------

Do not call:
    retained G(H) a branching ratio
    transient G(H) a formal branching ratio
    G > 1 a supercritical neighbourhood
    G < 1 proof of subcriticality
    fitted c an asymptotic theorem
    retained x permanently occupied
    transient convergence disappearance of every branch difference
    critical point
    phase transition
    directed percolation
    Hawkes process
    excitable medium
    wave
    individuality
    organism
    life

Use:
    retained finite-horizon causal gain
    transient finite-horizon causal gain
    no continuing positive transient accumulation over the frozen late window
    retained-minus-transient cumulative consequence
    local gain regime

Requires beside this file:
    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21


Cell = Tuple[int, int]

BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
PARENT_EXPERIMENT_VERSION = ch21.EXPERIMENT_VERSION
EXPERIMENT_VERSION = "digital-crystal-retained-transient-causal-gain-v5"
SCHEMA_VERSION = 5
CHAPTER = 23
RUN_TITLE = "Retained State, Corrected Transient Consequence, and Local Gain"


PROFILES = {
    "smoke": {
        "groups": 8,
        "probe_quantiles": [0.25, 0.75],
        "radius": 52,
        "warmup_steps": 14,
        "lossy_pre_steps": 12,
        "horizon": 8,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 10,
        "minimum_evaluated_candidates": 16,
        "late_window_start": 5,
        "persistent_offset_floor": 0.02,
        "transient_tail_abs_floor": 0.02,
        "transient_tail_ci_bound": 0.04,
        "mechanical_tolerance": 0.10,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },
    "quick": {
        "groups": 96,
        "probe_quantiles": [0.20, 0.40, 0.60, 0.80],
        "radius": 76,
        "warmup_steps": 20,
        "lossy_pre_steps": 20,
        "horizon": 30,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 34,
        "minimum_evaluated_candidates": 24,
        "late_window_start": 21,
        "persistent_offset_floor": 0.02,
        "transient_tail_abs_floor": 0.02,
        "transient_tail_ci_bound": 0.04,
        "mechanical_tolerance": 0.10,
        "bootstrap_reps": 3000,
        "signflip_permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "standard": {
        "groups": 192,
        "probe_quantiles": [0.20, 0.40, 0.60, 0.80],
        "radius": 96,
        "warmup_steps": 24,
        "lossy_pre_steps": 24,
        "horizon": 30,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 34,
        "minimum_evaluated_candidates": 32,
        "late_window_start": 21,
        "persistent_offset_floor": 0.02,
        "transient_tail_abs_floor": 0.02,
        "transient_tail_ci_bound": 0.04,
        "mechanical_tolerance": 0.10,
        "bootstrap_reps": 5000,
        "signflip_permutations": 12000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "full": {
        "groups": 384,
        "probe_quantiles": [0.10, 0.25, 0.40, 0.60, 0.75, 0.90],
        "radius": 112,
        "warmup_steps": 24,
        "lossy_pre_steps": 28,
        "horizon": 30,
        "loss_rate": 0.08,
        "budget": 96,
        "interior_margin": 34,
        "minimum_evaluated_candidates": 48,
        "late_window_start": 21,
        "persistent_offset_floor": 0.02,
        "transient_tail_abs_floor": 0.02,
        "transient_tail_ci_bound": 0.04,
        "mechanical_tolerance": 0.10,
        "bootstrap_reps": 7000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Frozen model helpers
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
        6.0 * theta
        + phase
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
        ch18.logistic_scalar(
            score
        )
    )


def growth_with_fixed_decision(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
    force_cell: Cell | None = None,
    prevent_cell: Cell | None = None,
    blocked_cell: Cell | None = None,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
    int,
]:
    """
    Frozen finite-budget synchronous growth.

    force_cell / prevent_cell:
        legacy V4 intervention-decision hooks. V5 does not use them for the
        corrected transient decomposition, but they remain available for
        backwards-compatible diagnostics.

    blocked_cell:
        remove this cell from the frontier BEFORE finite-budget selection.
        V5 uses this at lag 1 in PREVENT so x cannot consume a slot or attach.
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

    if blocked_cell is not None:
        frontier = [
            cell
            for cell in frontier
            if cell != blocked_cell
        ]

    next_step = int(
        state.step + 1
    )

    selected = ch21.select_candidates(
        frontier,
        budget,
        state.stream_seed,
        next_step,
    )

    selected_set = set(
        selected
    )

    if (
        force_cell is not None
        and force_cell not in selected_set
    ):
        raise RuntimeError(
            "force cell was not in the exact evaluated set"
        )

    if (
        prevent_cell is not None
        and prevent_cell not in selected_set
    ):
        raise RuntimeError(
            "prevent cell was not in the exact evaluated set"
        )

    additions: List[Cell] = []

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
            additions.append(
                cell
            )

    assert set(
        additions
    ) <= selected_set

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
        len(
            frontier
        ),
    )

def canonical_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
    loss_rate: float,
    blocked_cell: Cell | None = None,
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
        selected,
        frontier_count,
    ) = growth_with_fixed_decision(
        state,
        input_value,
        radius,
        crystal_params,
        budget,
        blocked_cell=blocked_cell,
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
        frontier_count,
    )

@dataclass
class PreparedBranchesV5:
    force: ch18.MaterialCrystalState
    prevent: ch18.MaterialCrystalState


def prepare_branches_v5(
    checkpoint: ch18.MaterialCrystalState,
    intervention_cell: Cell,
) -> PreparedBranchesV5:
    """
    Corrected state intervention.

    FORCE starts with x occupied.
    PREVENT starts from the identical checkpoint with x empty.

    No ordinary loss is applied before the first causal growth exposure.
    """
    prevent = clone_state(
        checkpoint
    )

    if intervention_cell in prevent.occupied:
        raise RuntimeError(
            "Probe x must be empty before intervention."
        )

    force = clone_state(
        checkpoint
    )

    force.occupied.add(
        intervention_cell
    )

    force.birth_time[
        intervention_cell
    ] = int(
        force.step
    )

    # Keep state bookkeeping internally consistent without pretending the
    # experimental intervention was an ordinary stochastic attachment.
    if force.population_by_step:
        force.population_by_step[
            -1
        ] = len(
            force.occupied
        )

    if intervention_cell not in force.occupied:
        raise RuntimeError(
            "FORCE intervention was not delivered."
        )

    if intervention_cell in prevent.occupied:
        raise RuntimeError(
            "PREVENT state contains x before first causal exposure."
        )

    return PreparedBranchesV5(
        force=force,
        prevent=prevent,
    )


# ============================================================================
# Checkpoint and probe selection
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
        profile[
            "radius"
        ]
    )

    warmup = int(
        profile[
            "warmup_steps"
        ]
    )

    pre_steps = int(
        profile[
            "lossy_pre_steps"
        ]
    )

    horizon = int(
        profile[
            "horizon"
        ]
    )

    gseed = (
        int(seed)
        + group * 1009
    )

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
        (
            state,
            _,
            _,
            _,
            _,
        ) = canonical_step(
            state,
            float(
                env[
                    warmup + j
                ]
            ),
            radius,
            crystal_params,
            int(
                profile[
                    "budget"
                ]
            ),
            float(
                profile[
                    "loss_rate"
                ]
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


def exact_evaluated_candidates(
    checkpoint: ch18.MaterialCrystalState,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    Tuple[Cell, float]
]:
    radius = int(
        profile[
            "radius"
        ]
    )

    margin = int(
        profile[
            "interior_margin"
        ]
    )

    frontier = frontier_cells(
        checkpoint.occupied,
        radius,
    )

    next_step = int(
        checkpoint.step + 1
    )

    selected = ch21.select_candidates(
        frontier,
        int(
            profile[
                "budget"
            ]
        ),
        checkpoint.stream_seed,
        next_step,
    )

    interior = [
        cell
        for cell in selected
        if (
            ch18.hex_distance(
                cell
            )
            <= radius
            - margin
        )
    ]

    return sorted(
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
            for cell in interior
        ],
        key=lambda item: (
            item[
                1
            ],
            item[
                0
            ],
        ),
    )


def select_probe_cells(
    checkpoint: ch18.MaterialCrystalState,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    Tuple[
        Cell,
        float,
        float,
    ]
]:
    candidates = (
        exact_evaluated_candidates(
            checkpoint,
            next_input,
            profile,
            crystal_params,
        )
    )

    if (
        len(
            candidates
        )
        < int(
            profile[
                "minimum_evaluated_candidates"
            ]
        )
    ):
        return []

    probes: List[
        Tuple[
            Cell,
            float,
            float,
        ]
    ] = []

    used: Set[
        Cell
    ] = set()

    for quantile in profile[
        "probe_quantiles"
    ]:
        index = int(
            round(
                float(
                    quantile
                )
                * (
                    len(
                        candidates
                    )
                    - 1
                )
            )
        )

        chosen = None

        for offset in range(
            len(
                candidates
            )
        ):
            for candidate_index in (
                index + offset,
                index - offset,
            ):
                if not (
                    0
                    <= candidate_index
                    < len(
                        candidates
                    )
                ):
                    continue

                cell, p = (
                    candidates[
                        candidate_index
                    ]
                )

                if cell in used:
                    continue

                chosen = (
                    cell,
                    float(
                        p
                    ),
                    float(
                        quantile
                    ),
                )
                break

            if (
                chosen is not None
            ):
                break

        if (
            chosen is not None
        ):
            used.add(
                chosen[
                    0
                ]
            )
            probes.append(
                chosen
            )

    return probes


# ============================================================================
# Geometry diagnostics
# ============================================================================

def geometry_diagnostics(
    checkpoint: ch18.MaterialCrystalState,
    intervention_cell: Cell,
    radius: int,
) -> dict:
    occupied = set(
        checkpoint.occupied
    )

    ring = list(
        ch18.neighbors(
            intervention_cell
        )
    )

    frontier_before = set(
        frontier_cells(
            occupied,
            radius,
        )
    )

    occupied_force = set(
        occupied
    )
    occupied_force.add(
        intervention_cell
    )

    frontier_after = set(
        frontier_cells(
            occupied_force,
            radius,
        )
    )

    ring_empty = [
        cell
        for cell in ring
        if cell not in occupied
    ]

    ring_frontier_before = [
        cell
        for cell in ring_empty
        if cell in frontier_before
    ]

    ring_promoted = [
        cell
        for cell in ring_empty
        if (
            cell not in frontier_before
            and cell in frontier_after
        )
    ]

    return {
        "occupied_neighbor_count": int(
            sum(
                cell in occupied
                for cell in ring
            )
        ),
        "ring1_empty_neighbors": int(
            len(
                ring_empty
            )
        ),
        "ring1_frontier_before": int(
            len(
                ring_frontier_before
            )
        ),
        "ring1_newly_promoted_frontier": int(
            len(
                ring_promoted
            )
        ),
        "ring1_occupied_neighbors": int(
            sum(
                cell in occupied
                for cell in ring
            )
        ),
        "global_frontier_delta_if_forced_before_loss": int(
            len(
                frontier_after
            )
            - len(
                frontier_before
            )
        ),
    }


def relative_distance(
    cell: Cell,
    origin: Cell,
) -> int:
    return int(
        ch18.hex_distance(
            (
                cell[
                    0
                ]
                - origin[
                    0
                ],
                cell[
                    1
                ]
                - origin[
                    1
                ],
            )
        )
    )


# ============================================================================
# Mechanical next-step expectation
# ============================================================================

def expected_next_ring1_gain(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    intervention_cell: Cell,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> float:
    """
    Exact expected lag-1 ring-one construction difference under the corrected
    V5 intervention.

    PREVENT explicitly removes x from its frontier BEFORE finite-budget
    selection. This matters even though x itself is excluded from the outcome,
    because allowing x to consume a slot would change which other candidates
    receive evaluation.
    """
    radius = int(
        profile[
            "radius"
        ]
    )

    budget = int(
        profile[
            "budget"
        ]
    )

    def expected(
        state: ch18.MaterialCrystalState,
        blocked_cell: Cell | None = None,
    ) -> float:
        frontier = frontier_cells(
            state.occupied,
            radius,
        )

        if blocked_cell is not None:
            frontier = [
                cell
                for cell in frontier
                if cell != blocked_cell
            ]

        selected = ch21.select_candidates(
            frontier,
            budget,
            state.stream_seed,
            int(
                state.step + 1
            ),
        )

        total = 0.0

        for cell in selected:
            if (
                cell
                == intervention_cell
            ):
                continue

            if (
                relative_distance(
                    cell,
                    intervention_cell,
                )
                != 1
            ):
                continue

            total += attachment_probability(
                cell,
                state.occupied,
                next_input,
                crystal_params,
            )

        return float(
            total
        )

    return float(
        expected(
            force_state,
            blocked_cell=None,
        )
        - expected(
            prevent_state,
            blocked_cell=intervention_cell,
        )
    )


# ============================================================================
# Arm simulation
# ============================================================================

@dataclass
class ArmResult:
    lag_gain_local: List[float]
    lag_gain_global: List[float]
    selected_symmetric_difference: List[float]
    selected_overlap_fraction: List[float]
    distance_lag_gain: List[List[float]]
    cumulative_local: float
    cumulative_global: float
    far_field_gain: float
    late_mean: float


@dataclass
class ProbeResult:
    group: int
    probe: int
    quantile: float
    baseline_probability: float
    geometry: dict
    g_mech_1: float

    # Legacy field name retained internally for compatibility with the V4
    # analysis shape. Scientifically this arm is RETAINED, not clamped
    # persistent occupancy.
    persistent_g1: float
    transient_g1: float
    persistent: ArmResult
    transient: ArmResult
    level_shift_cumulative: float

    persistent_fit_A: float
    persistent_fit_lambda: float
    persistent_fit_c: float
    transient_fit_A: float
    transient_fit_lambda: float
    transient_fit_c: float

    # V5 construct-validity diagnostics.
    lag1_force_x_present_before_growth: bool
    lag1_prevent_x_blocked: bool
    lag1_equalized_after_cleanup: bool

    retained_x_occupied_updates: int
    retained_x_occupancy_fraction: float
    retained_x_present_at_horizon: bool

    transient_x_reoccupied: bool
    transient_x_first_reoccupation_lag: int | None
    prevent_x_reoccupied: bool
    prevent_x_first_reoccupation_lag: int | None

    max_capacity_fraction: float


def selected_set_metrics(
    a: Sequence[Cell],
    b: Sequence[Cell],
) -> Tuple[
    float,
    float,
]:
    sa = set(
        a
    )
    sb = set(
        b
    )

    sym = float(
        len(
            sa
            ^ sb
        )
    )

    union = (
        sa
        | sb
    )

    overlap = (
        float(
            len(
                sa
                & sb
            )
            / len(
                union
            )
        )
        if union
        else 1.0
    )

    return (
        sym,
        overlap,
    )


def fit_exp_offset(
    y: Sequence[float],
) -> Tuple[
    float,
    float,
    float,
]:
    """
    Descriptive least-squares fit:
        y(t) = A exp(-t/lambda) + c

    Avoids scipy dependency by grid-searching lambda and solving A,c linearly.
    """
    arr = np.asarray(
        y,
        dtype=float,
    )

    t = np.arange(
        1,
        len(
            arr
        )
        + 1,
        dtype=float,
    )

    lambdas = np.geomspace(
        0.35,
        max(
            2.0,
            4.0
            * len(
                arr
            ),
        ),
        240,
    )

    best = None

    for lam in lambdas:
        x = np.exp(
            -t
            / lam
        )

        design = np.column_stack(
            [
                x,
                np.ones_like(
                    x
                ),
            ]
        )

        coef, *_ = np.linalg.lstsq(
            design,
            arr,
            rcond=None,
        )

        fitted = (
            design
            @ coef
        )

        sse = float(
            np.sum(
                (
                    arr
                    - fitted
                )
                ** 2
            )
        )

        if (
            best is None
            or sse
            < best[
                0
            ]
        ):
            best = (
                sse,
                float(
                    coef[
                        0
                    ]
                ),
                float(
                    lam
                ),
                float(
                    coef[
                        1
                    ]
                ),
            )

    assert (
        best is not None
    )

    return (
        best[
            1
        ],
        best[
            2
        ],
        best[
            3
        ],
    )


def simulate_probe(
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
    radius = int(
        profile[
            "radius"
        ]
    )

    budget = int(
        profile[
            "budget"
        ]
    )

    loss_rate = float(
        profile[
            "loss_rate"
        ]
    )

    horizon = int(
        profile[
            "horizon"
        ]
    )

    late_start = int(
        profile[
            "late_window_start"
        ]
    )

    geometry = geometry_diagnostics(
        checkpoint,
        intervention_cell,
        radius,
    )

    branches = prepare_branches_v5(
        checkpoint,
        intervention_cell,
    )

    # Historical internal field names remain "persistent"; scientifically this
    # is the RETAINED arm: no experimental removal after intervention.
    persistent_state = clone_state(
        branches.force
    )
    transient_state = clone_state(
        branches.force
    )
    prevent_state = clone_state(
        branches.prevent
    )

    # Exact expected immediate effect before realized lag-1 Bernoulli draws.
    # V5 uses future_env[0] for the first causal exposure because the
    # intervention is a state manipulation at the frozen checkpoint rather
    # than a separate growth+loss update.
    g_mech_1 = expected_next_ring1_gain(
        persistent_state,
        prevent_state,
        intervention_cell,
        float(
            future_env[
                0
            ]
        ),
        profile,
        crystal_params,
    )

    persistent_local: List[
        float
    ] = []

    persistent_global: List[
        float
    ] = []

    transient_local: List[
        float
    ] = []

    transient_global: List[
        float
    ] = []

    persistent_sym: List[
        float
    ] = []

    persistent_overlap: List[
        float
    ] = []

    transient_sym: List[
        float
    ] = []

    transient_overlap: List[
        float
    ] = []

    persistent_matrix = np.zeros(
        (
            horizon,
            horizon + 1,
        ),
        dtype=float,
    )

    transient_matrix = np.zeros_like(
        persistent_matrix
    )

    max_capacity = 0.0

    persistent_g1 = 0.0
    transient_g1 = 0.0

    lag1_force_x_present_before_growth = False
    lag1_prevent_x_blocked = False
    lag1_equalized_after_cleanup = False

    retained_x_occupied_updates = 0

    transient_x_reoccupied = False
    transient_x_first_reoccupation_lag: int | None = None

    prevent_x_reoccupied = False
    prevent_x_first_reoccupation_lag: int | None = None

    for lag in range(
        1,
        horizon + 1,
    ):
        input_value = float(
            future_env[
                lag - 1
            ]
        )

        blocked_prevent = (
            intervention_cell
            if lag == 1
            else None
        )

        retained_x_present_before_growth = bool(
            intervention_cell
            in persistent_state.occupied
        )

        if retained_x_present_before_growth:
            retained_x_occupied_updates += 1

        if lag == 1:
            lag1_force_x_present_before_growth = bool(
                retained_x_present_before_growth
                and intervention_cell
                in transient_state.occupied
            )

            lag1_prevent_x_blocked = bool(
                blocked_prevent
                == intervention_cell
                and intervention_cell
                not in prevent_state.occupied
            )

            if not lag1_force_x_present_before_growth:
                raise RuntimeError(
                    "V5 FORCE x missing before first causal exposure."
                )

            if not lag1_prevent_x_blocked:
                raise RuntimeError(
                    "V5 PREVENT x was not cleanly blocked at lag 1."
                )

        (
            persistent_state,
            p_add,
            _,
            p_selected,
            _,
        ) = canonical_step(
            persistent_state,
            input_value,
            radius,
            crystal_params,
            budget,
            loss_rate,
            blocked_cell=None,
        )

        (
            transient_state,
            t_add,
            _,
            t_selected,
            _,
        ) = canonical_step(
            transient_state,
            input_value,
            radius,
            crystal_params,
            budget,
            loss_rate,
            blocked_cell=None,
        )

        (
            prevent_state,
            c_add,
            _,
            c_selected,
            _,
        ) = canonical_step(
            prevent_state,
            input_value,
            radius,
            crystal_params,
            budget,
            loss_rate,
            blocked_cell=blocked_prevent,
        )

        if (
            lag == 1
            and intervention_cell in c_add
        ):
            raise RuntimeError(
                "Corrected PREVENT allowed x to attach at lag 1."
            )

        p_by_d = np.zeros(
            horizon + 1,
            dtype=float,
        )

        t_by_d = np.zeros_like(
            p_by_d
        )

        c_by_d = np.zeros_like(
            p_by_d
        )

        for cell in p_add:
            if cell == intervention_cell:
                continue

            d = relative_distance(
                cell,
                intervention_cell,
            )

            if (
                1
                <= d
                <= horizon
            ):
                p_by_d[
                    d
                ] += 1.0

        for cell in t_add:
            if cell == intervention_cell:
                continue

            d = relative_distance(
                cell,
                intervention_cell,
            )

            if (
                1
                <= d
                <= horizon
            ):
                t_by_d[
                    d
                ] += 1.0

        for cell in c_add:
            if cell == intervention_cell:
                continue

            d = relative_distance(
                cell,
                intervention_cell,
            )

            if (
                1
                <= d
                <= horizon
            ):
                c_by_d[
                    d
                ] += 1.0

        p_delta = (
            p_by_d
            - c_by_d
        )

        t_delta = (
            t_by_d
            - c_by_d
        )

        persistent_matrix[
            lag - 1,
            :
        ] = p_delta

        transient_matrix[
            lag - 1,
            :
        ] = t_delta

        p_local = float(
            np.sum(
                p_delta[
                    1:
                ]
            )
        )

        t_local = float(
            np.sum(
                t_delta[
                    1:
                ]
            )
        )

        persistent_local.append(
            p_local
        )

        transient_local.append(
            t_local
        )

        p_global_count = sum(
            cell
            != intervention_cell
            for cell in p_add
        )

        t_global_count = sum(
            cell
            != intervention_cell
            for cell in t_add
        )

        c_global_count = sum(
            cell
            != intervention_cell
            for cell in c_add
        )

        persistent_global.append(
            float(
                p_global_count
                - c_global_count
            )
        )

        transient_global.append(
            float(
                t_global_count
                - c_global_count
            )
        )

        p_sym, p_overlap = (
            selected_set_metrics(
                p_selected,
                c_selected,
            )
        )

        t_sym, t_overlap = (
            selected_set_metrics(
                t_selected,
                c_selected,
            )
        )

        persistent_sym.append(
            p_sym
        )

        persistent_overlap.append(
            p_overlap
        )

        transient_sym.append(
            t_sym
        )

        transient_overlap.append(
            t_overlap
        )

        if lag == 1:
            persistent_g1 = float(
                p_delta[
                    1
                ]
            )

            transient_g1 = float(
                t_delta[
                    1
                ]
            )

            # Corrected V5 equalization:
            # after exactly one causal growth exposure, remove x from both
            # TRANSIENT and PREVENT. RETAINED is not experimentally removed.
            transient_state.occupied.discard(
                intervention_cell
            )
            transient_state.birth_time.pop(
                intervention_cell,
                None,
            )

            prevent_state.occupied.discard(
                intervention_cell
            )
            prevent_state.birth_time.pop(
                intervention_cell,
                None,
            )

            if transient_state.population_by_step:
                transient_state.population_by_step[
                    -1
                ] = len(
                    transient_state.occupied
                )

            if prevent_state.population_by_step:
                prevent_state.population_by_step[
                    -1
                ] = len(
                    prevent_state.occupied
                )

            lag1_equalized_after_cleanup = bool(
                intervention_cell
                not in transient_state.occupied
                and intervention_cell
                not in prevent_state.occupied
            )

            if not lag1_equalized_after_cleanup:
                raise RuntimeError(
                    "V5 focal-state equalization failed after lag 1."
                )

        # Natural reoccupation after the controlled lag-1 cleanup is part of
        # the downstream process and is recorded, not blocked. Detect it from
        # additions so a same-update loss cannot hide a reoccupation event.
        if lag >= 2:
            if (
                not transient_x_reoccupied
                and intervention_cell
                in t_add
            ):
                transient_x_reoccupied = True
                transient_x_first_reoccupation_lag = int(
                    lag
                )

            if (
                not prevent_x_reoccupied
                and intervention_cell
                in c_add
            ):
                prevent_x_reoccupied = True
                prevent_x_first_reoccupation_lag = int(
                    lag
                )

        max_capacity = max(
            max_capacity,
            float(
                ch18.capacity_fraction_occupied(
                    persistent_state.occupied,
                    radius,
                )
            ),
            float(
                ch18.capacity_fraction_occupied(
                    transient_state.occupied,
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

    def arm_result(
        local: List[float],
        global_gain: List[float],
        sym: List[float],
        overlap: List[float],
        matrix: np.ndarray,
    ) -> ArmResult:
        cumulative_local = float(
            np.sum(
                local
            )
        )

        cumulative_global = float(
            np.sum(
                global_gain
            )
        )

        late_values = local[
            late_start - 1:
        ]

        return ArmResult(
            lag_gain_local=[
                float(
                    x
                )
                for x in local
            ],
            lag_gain_global=[
                float(
                    x
                )
                for x in global_gain
            ],
            selected_symmetric_difference=[
                float(
                    x
                )
                for x in sym
            ],
            selected_overlap_fraction=[
                float(
                    x
                )
                for x in overlap
            ],
            distance_lag_gain=[
                [
                    float(
                        value
                    )
                    for value in row
                ]
                for row in matrix
            ],
            cumulative_local=(
                cumulative_local
            ),
            cumulative_global=(
                cumulative_global
            ),
            far_field_gain=float(
                cumulative_global
                - cumulative_local
            ),
            late_mean=float(
                np.mean(
                    late_values
                )
            ),
        )

    persistent = arm_result(
        persistent_local,
        persistent_global,
        persistent_sym,
        persistent_overlap,
        persistent_matrix,
    )

    transient = arm_result(
        transient_local,
        transient_global,
        transient_sym,
        transient_overlap,
        transient_matrix,
    )

    pA, pLambda, pc = (
        fit_exp_offset(
            persistent_local
        )
    )

    tA, tLambda, tc = (
        fit_exp_offset(
            transient_local
        )
    )

    retained_x_occupancy_fraction = float(
        retained_x_occupied_updates
        / max(
            horizon,
            1,
        )
    )

    return ProbeResult(
        group=int(
            group
        ),
        probe=int(
            probe_index
        ),
        quantile=float(
            quantile
        ),
        baseline_probability=float(
            baseline_probability
        ),
        geometry=geometry,
        g_mech_1=float(
            g_mech_1
        ),
        persistent_g1=float(
            persistent_g1
        ),
        transient_g1=float(
            transient_g1
        ),
        persistent=persistent,
        transient=transient,
        level_shift_cumulative=float(
            persistent.cumulative_local
            - transient.cumulative_local
        ),
        persistent_fit_A=float(
            pA
        ),
        persistent_fit_lambda=float(
            pLambda
        ),
        persistent_fit_c=float(
            pc
        ),
        transient_fit_A=float(
            tA
        ),
        transient_fit_lambda=float(
            tLambda
        ),
        transient_fit_c=float(
            tc
        ),
        lag1_force_x_present_before_growth=bool(
            lag1_force_x_present_before_growth
        ),
        lag1_prevent_x_blocked=bool(
            lag1_prevent_x_blocked
        ),
        lag1_equalized_after_cleanup=bool(
            lag1_equalized_after_cleanup
        ),
        retained_x_occupied_updates=int(
            retained_x_occupied_updates
        ),
        retained_x_occupancy_fraction=float(
            retained_x_occupancy_fraction
        ),
        retained_x_present_at_horizon=bool(
            intervention_cell
            in persistent_state.occupied
        ),
        transient_x_reoccupied=bool(
            transient_x_reoccupied
        ),
        transient_x_first_reoccupation_lag=(
            transient_x_first_reoccupation_lag
        ),
        prevent_x_reoccupied=bool(
            prevent_x_reoccupied
        ),
        prevent_x_first_reoccupation_lag=(
            prevent_x_first_reoccupation_lag
        ),
        max_capacity_fraction=float(
            max_capacity
        ),
    )


# ============================================================================
# Group-level statistics
# ============================================================================

def by_group_mean(
    results: Sequence[
        ProbeResult
    ],
    getter,
) -> List[float]:
    buckets: Dict[
        int,
        List[float],
    ] = {}

    for result in results:
        buckets.setdefault(
            result.group,
            [],
        ).append(
            float(
                getter(
                    result
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


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            float(
                value
            )
            for value in values
            if math.isfinite(
                float(
                    value
                )
            )
        ],
        dtype=float,
    )

    if len(
        arr
    ) == 0:
        return {
            "n": 0,
            "mean": float(
                "nan"
            ),
            "ci95_low": float(
                "nan"
            ),
            "ci95_high": float(
                "nan"
            ),
            "half_width": float(
                "nan"
            ),
        }

    rng = np.random.default_rng(
        seed
    )

    boot = np.empty(
        int(
            reps
        ),
        dtype=float,
    )

    for i in range(
        int(
            reps
        )
    ):
        sample = rng.choice(
            arr,
            size=len(
                arr
            ),
            replace=True,
        )

        boot[
            i
        ] = float(
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
            len(
                arr
            )
        ),
        "mean": float(
            np.mean(
                arr
            )
        ),
        "ci95_low": (
            low
        ),
        "ci95_high": (
            high
        ),
        "half_width": float(
            (
                high
                - low
            )
            / 2.0
        ),
    }


def signflip_two_sided(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            float(
                value
            )
            for value in values
            if math.isfinite(
                float(
                    value
                )
            )
        ],
        dtype=float,
    )

    if len(
        arr
    ) == 0:
        return {
            "n": 0,
            "observed_mean": float(
                "nan"
            ),
            "p_value": float(
                "nan"
            ),
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
        int(
            permutations
        ),
        dtype=float,
    )

    for i in range(
        int(
            permutations
        )
    ):
        signs = rng.choice(
            np.asarray(
                [
                    -1.0,
                    1.0,
                ]
            ),
            size=len(
                arr
            ),
        )

        null[
            i
        ] = float(
            np.mean(
                arr
                * signs
            )
        )

    p = (
        1.0
        + float(
            np.sum(
                np.abs(
                    null
                )
                >= abs(
                    observed
                )
            )
        )
    ) / (
        len(
            null
        )
        + 1.0
    )

    return {
        "n": int(
            len(
                arr
            )
        ),
        "observed_mean": (
            observed
        ),
        "p_value": float(
            p
        ),
        "permutations": int(
            permutations
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
            Tuple[
                str,
                str,
            ]
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
            / "ch23-retained-transient-causal-gain-v5-full-report.md"
        )

        parts = [
            "# Chapter 23 — Retained State, Corrected Transient Consequence, and Local Gain (V5)",
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
# Stage 0
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
    seed: int,
) -> dict:
    payload = {
        "role": (
            "CORRECTED RETAINED / TRANSIENT CAUSAL-GAIN DECOMPOSITION"
        ),
        "construct_validity_correction": (
            "PREVENT blocks x during the one intended causal exposure; "
            "after lag 1 x is removed from both TRANSIENT and PREVENT."
        ),
        "fresh_seed": int(
            seed
        ),
        "previous_v4_seed": (
            20260905
        ),
        "horizon": int(
            profile[
                "horizon"
            ]
        ),
        "late_window": [
            int(
                profile[
                    "late_window_start"
                ]
            ),
            int(
                profile[
                    "horizon"
                ]
            ),
        ],
        "probe_quantiles": list(
            profile[
                "probe_quantiles"
            ]
        ),
        "intervention_timing": (
            "At the frozen checkpoint, FORCE-derived branches receive x as "
            "occupied and PREVENT remains x-empty. Intervention delivery is "
            "external and does not consume a lag-1 evaluation slot. No "
            "ordinary loss occurs before the first causal growth exposure."
        ),
        "probe_support": (
            "x is still selected from the checkpoint's exact finite-budget "
            "evaluated candidate set using the same first-exposure input."
        ),
        "lag1_control": (
            "During lag 1 growth PREVENT removes x from the frontier before "
            "finite-budget selection; FORCE-derived branches contain x as an "
            "occupied neighbour. Ordinary loss follows growth."
        ),
        "transient_equalization": (
            "Immediately after lag 1 growth+loss, x is explicitly removed "
            "from both TRANSIENT and PREVENT and absence is asserted."
        ),
        "later_x_semantics": (
            "From lag 2 onward no branch specially blocks x. Natural "
            "reoccupation is downstream dynamics and x remains excluded from "
            "outcome accounting."
        ),
        "retained_semantics": (
            "RETAINED means x is not experimentally removed after the "
            "intervention. It is not clamped occupied and remains subject to "
            "ordinary loss/reoccupation."
        ),
        "retained_offset_test": {
            "late_mean_floor": float(
                profile[
                    "persistent_offset_floor"
                ]
            ),
            "requires_late_ci_above_zero": True,
            "requires_fit_c_ci_above_zero": True,
        },
        "transient_convergence_test": {
            "absolute_late_mean_floor": float(
                profile[
                    "transient_tail_abs_floor"
                ]
            ),
            "ci_bound": float(
                profile[
                    "transient_tail_ci_bound"
                ]
            ),
        },
        "descriptive_fit": (
            "gain(tau)=A*exp(-tau/lambda)+c"
        ),
        "critical_reference": (
            "Only transient G(30) is compared descriptively with 1."
        ),
        "formal_branching_ratio_claim": False,
        "primary_inference_uses": (
            "group means; probes within one checkpoint are repeated measures"
        ),
        "validity_assertions": [
            "FORCE x present before lag-1 growth",
            "PREVENT x blocked from lag-1 frontier before selection",
            "PREVENT x not attached at lag 1",
            "x absent from TRANSIENT and PREVENT after lag-1 cleanup",
        ],
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
        payload,
    )

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen V5 Corrected Decomposition Protocol",
        payload,
    )

    return payload


# ============================================================================
# Stage 1
# ============================================================================

def stage_1_run(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[
        ProbeResult
    ],
    dict,
]:
    results: List[
        ProbeResult
    ] = []

    skipped = 0
    max_capacity = 0.0

    for group in tqdm(
        range(
            int(
                profile[
                    "groups"
                ]
            )
        ),
        desc=(
            "Chapter 23 V5 corrected retained/transient groups"
        ),
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

        max_capacity = max(
            max_capacity,
            checkpoint_capacity,
        )

        if not checkpoint.occupied:
            skipped += 1
            continue

        probes = select_probe_cells(
            checkpoint,
            float(
                future_env[
                    0
                ]
            ),
            profile,
            crystal_params,
        )

        if (
            len(
                probes
            )
            != len(
                profile[
                    "probe_quantiles"
                ]
            )
        ):
            skipped += 1
            continue

        for probe_index, (
            cell,
            p,
            quantile,
        ) in enumerate(
            probes
        ):
            result = simulate_probe(
                checkpoint,
                future_env,
                cell,
                p,
                quantile,
                profile,
                crystal_params,
                group,
                probe_index,
            )

            results.append(
                result
            )

            max_capacity = max(
                max_capacity,
                result.max_capacity_fraction,
            )

    groups_used = len(
        set(
            result.group
            for result in results
        )
    )

    intervention_control_gate_passed = bool(
        results
        and all(
            result.lag1_force_x_present_before_growth
            and result.lag1_prevent_x_blocked
            and result.lag1_equalized_after_cleanup
            for result in results
        )
    )

    payload = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "groups_used": int(
            groups_used
        ),
        "skipped_groups": int(
            skipped
        ),
        "total_probes": int(
            len(
                results
            )
        ),
        "probes_per_group": int(
            len(
                profile[
                    "probe_quantiles"
                ]
            )
        ),
        "maximum_capacity_fraction": float(
            max_capacity
        ),
        "capacity_gate_passed": bool(
            max_capacity
            < profile[
                "max_capacity_fraction"
            ]
        ),
        "coverage_gate_passed": bool(
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
        "intervention_control_gate_passed": (
            intervention_control_gate_passed
        ),
        "lag1_force_present_fraction": float(
            np.mean(
                [
                    result.lag1_force_x_present_before_growth
                    for result in results
                ]
            )
            if results
            else float("nan")
        ),
        "lag1_prevent_blocked_fraction": float(
            np.mean(
                [
                    result.lag1_prevent_x_blocked
                    for result in results
                ]
            )
            if results
            else float("nan")
        ),
        "lag1_equalized_fraction": float(
            np.mean(
                [
                    result.lag1_equalized_after_cleanup
                    for result in results
                ]
            )
            if results
            else float("nan")
        ),
        "status": "MEASURED",
    }

    raw_probe_payload = {
        "probes": [
            {
                "group": int(result.group),
                "probe": int(result.probe),
                "quantile": float(result.quantile),
                "baseline_probability": float(result.baseline_probability),
                "g_mech_1": float(result.g_mech_1),
                "retained_g1": float(result.persistent_g1),
                "transient_g1": float(result.transient_g1),
                "retained_G_H_local": float(
                    result.persistent.cumulative_local
                ),
                "transient_G_H_local": float(
                    result.transient.cumulative_local
                ),
                "retained_late_mean": float(
                    result.persistent.late_mean
                ),
                "transient_late_mean": float(
                    result.transient.late_mean
                ),
                "retained_minus_transient": float(
                    result.level_shift_cumulative
                ),
                "lag1_force_x_present_before_growth": bool(
                    result.lag1_force_x_present_before_growth
                ),
                "lag1_prevent_x_blocked": bool(
                    result.lag1_prevent_x_blocked
                ),
                "lag1_equalized_after_cleanup": bool(
                    result.lag1_equalized_after_cleanup
                ),
                "retained_x_occupied_growth_exposures": int(
                    result.retained_x_occupied_updates
                ),
                "retained_x_occupancy_fraction": float(
                    result.retained_x_occupancy_fraction
                ),
                "retained_x_present_at_horizon": bool(
                    result.retained_x_present_at_horizon
                ),
                "transient_x_reoccupied": bool(
                    result.transient_x_reoccupied
                ),
                "transient_x_first_reoccupation_lag": (
                    result.transient_x_first_reoccupation_lag
                ),
                "prevent_x_reoccupied": bool(
                    result.prevent_x_reoccupied
                ),
                "prevent_x_first_reoccupation_lag": (
                    result.prevent_x_first_reoccupation_lag
                ),
                "geometry": result.geometry,
            }
            for result in results
        ]
    }

    reporter.json(
        "raw-v5-probe-diagnostics.json",
        raw_probe_payload,
    )

    reporter.json(
        "stage-01-interventions.json",
        payload,
    )

    reporter.stage(
        "stage-01-interventions.md",
        "Stage 1 — Corrected Retained and Transient Interventions",
        payload,
    )

    return (
        results,
        payload,
    )


# ============================================================================
# Stage 2 — aggregate decomposition
# ============================================================================

def stage_2_decomposition(
    reporter: Reporter,
    profile: dict,
    results: Sequence[
        ProbeResult
    ],
    seed: int,
    image_dir: Path,
) -> dict:
    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    metrics = {
        "g_mech_1": (
            lambda r:
            r.g_mech_1
        ),
        "retained_g1": (
            lambda r:
            r.persistent_g1
        ),
        "transient_g1": (
            lambda r:
            r.transient_g1
        ),
        "retained_G_H_local": (
            lambda r:
            r.persistent.cumulative_local
        ),
        "transient_G_H_local": (
            lambda r:
            r.transient.cumulative_local
        ),
        "retained_G_H_global": (
            lambda r:
            r.persistent.cumulative_global
        ),
        "transient_G_H_global": (
            lambda r:
            r.transient.cumulative_global
        ),
        "retained_far_field": (
            lambda r:
            r.persistent.far_field_gain
        ),
        "transient_far_field": (
            lambda r:
            r.transient.far_field_gain
        ),
        "retained_late_mean": (
            lambda r:
            r.persistent.late_mean
        ),
        "transient_late_mean": (
            lambda r:
            r.transient.late_mean
        ),
        "retained_fit_c": (
            lambda r:
            r.persistent_fit_c
        ),
        "transient_fit_c": (
            lambda r:
            r.transient_fit_c
        ),
        "retained_fit_lambda": (
            lambda r:
            r.persistent_fit_lambda
        ),
        "transient_fit_lambda": (
            lambda r:
            r.transient_fit_lambda
        ),
        "retained_minus_transient_cumulative": (
            lambda r:
            r.level_shift_cumulative
        ),
        "mechanical_discrepancy": (
            lambda r:
            r.persistent_g1
            - r.g_mech_1
        ),
    }

    payload = {
        key: bootstrap_mean_ci(
            by_group_mean(
                results,
                getter,
            ),
            reps,
            seed
            + 1000
            + index,
        )
        for index, (
            key,
            getter,
        ) in enumerate(
            metrics.items()
        )
    }

    payload["focal_state_diagnostics"] = {
        "retained_x_occupied_growth_exposures": bootstrap_mean_ci(
            by_group_mean(
                results,
                lambda r: r.retained_x_occupied_updates,
            ),
            reps,
            seed + 1500,
        ),
        "retained_x_occupancy_fraction": bootstrap_mean_ci(
            by_group_mean(
                results,
                lambda r: r.retained_x_occupancy_fraction,
            ),
            reps,
            seed + 1501,
        ),
        "retained_x_present_at_horizon_fraction": float(
            np.mean(
                [
                    result.retained_x_present_at_horizon
                    for result in results
                ]
            )
        ),
        "transient_x_reoccupation_fraction": float(
            np.mean(
                [
                    result.transient_x_reoccupied
                    for result in results
                ]
            )
        ),
        "prevent_x_reoccupation_fraction": float(
            np.mean(
                [
                    result.prevent_x_reoccupied
                    for result in results
                ]
            )
        ),
        "transient_first_reoccupation_lag_mean": float(
            np.mean(
                [
                    result.transient_x_first_reoccupation_lag
                    for result in results
                    if result.transient_x_first_reoccupation_lag is not None
                ]
            )
        ) if any(
            result.transient_x_first_reoccupation_lag is not None
            for result in results
        ) else float("nan"),
        "prevent_first_reoccupation_lag_mean": float(
            np.mean(
                [
                    result.prevent_x_first_reoccupation_lag
                    for result in results
                    if result.prevent_x_first_reoccupation_lag is not None
                ]
            )
        ) if any(
            result.prevent_x_first_reoccupation_lag is not None
            for result in results
        ) else float("nan"),
    }

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

    persistent_lag_by_group = []
    transient_lag_by_group = []

    persistent_sym_by_group = []
    transient_sym_by_group = []

    persistent_overlap_by_group = []
    transient_overlap_by_group = []

    persistent_distance_mats = []
    transient_distance_mats = []

    for group in group_ids:
        subset = [
            result
            for result in results
            if result.group == group
        ]

        persistent_lag_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.persistent.lag_gain_local
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        transient_lag_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.transient.lag_gain_local
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        persistent_sym_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.persistent.selected_symmetric_difference
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        transient_sym_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.transient.selected_symmetric_difference
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        persistent_overlap_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.persistent.selected_overlap_fraction
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        transient_overlap_by_group.append(
            np.mean(
                np.asarray(
                    [
                        result.transient.selected_overlap_fraction
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        persistent_distance_mats.append(
            np.mean(
                np.asarray(
                    [
                        result.persistent.distance_lag_gain
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

        transient_distance_mats.append(
            np.mean(
                np.asarray(
                    [
                        result.transient.distance_lag_gain
                        for result in subset
                    ],
                    dtype=float,
                ),
                axis=0,
            )
        )

    persistent_lag_mean = np.mean(
        np.stack(
            persistent_lag_by_group,
            axis=0,
        ),
        axis=0,
    )

    transient_lag_mean = np.mean(
        np.stack(
            transient_lag_by_group,
            axis=0,
        ),
        axis=0,
    )

    persistent_cumulative = np.cumsum(
        persistent_lag_mean
    )

    transient_cumulative = np.cumsum(
        transient_lag_mean
    )

    payload[
        "population_lag_profile"
    ] = {
        "retained": [
            float(
                x
            )
            for x in persistent_lag_mean
        ],
        "transient": [
            float(
                x
            )
            for x in transient_lag_mean
        ],
        "level_shift": [
            float(
                p - t
            )
            for p, t in zip(
                persistent_lag_mean,
                transient_lag_mean,
            )
        ],
    }

    payload[
        "population_cumulative_gain_by_horizon"
    ] = {
        "retained": [
            float(
                x
            )
            for x in persistent_cumulative
        ],
        "transient": [
            float(
                x
            )
            for x in transient_cumulative
        ],
    }

    payload[
        "budget_reshuffling_by_lag"
    ] = {
        "retained_symmetric_difference": [
            float(
                x
            )
            for x in np.mean(
                np.stack(
                    persistent_sym_by_group,
                    axis=0,
                ),
                axis=0,
            )
        ],
        "transient_symmetric_difference": [
            float(
                x
            )
            for x in np.mean(
                np.stack(
                    transient_sym_by_group,
                    axis=0,
                ),
                axis=0,
            )
        ],
        "retained_overlap_fraction": [
            float(
                x
            )
            for x in np.mean(
                np.stack(
                    persistent_overlap_by_group,
                    axis=0,
                ),
                axis=0,
            )
        ],
        "transient_overlap_fraction": [
            float(
                x
            )
            for x in np.mean(
                np.stack(
                    transient_overlap_by_group,
                    axis=0,
                ),
                axis=0,
            )
        ],
    }

    p_matrix = np.mean(
        np.stack(
            persistent_distance_mats,
            axis=0,
        ),
        axis=0,
    )

    t_matrix = np.mean(
        np.stack(
            transient_distance_mats,
            axis=0,
        ),
        axis=0,
    )

    payload[
        "population_distance_lag_gain"
    ] = {
        "retained": (
            p_matrix.tolist()
        ),
        "transient": (
            t_matrix.tolist()
        ),
    }

    # Descriptive population-level fit too.
    pA, pLambda, pc = fit_exp_offset(
        persistent_lag_mean
    )

    tA, tLambda, tc = fit_exp_offset(
        transient_lag_mean
    )

    payload[
        "population_descriptive_fit"
    ] = {
        "retained": {
            "A": float(
                pA
            ),
            "lambda": float(
                pLambda
            ),
            "c": float(
                pc
            ),
        },
        "transient": {
            "A": float(
                tA
            ),
            "lambda": float(
                tLambda
            ),
            "c": float(
                tc
            ),
        },
    }

    reporter.json(
        "stage-02-decomposition.json",
        payload,
    )

    reporter.stage(
        "stage-02-decomposition.md",
        "Stage 2 — Corrected Retained / Transient Gain Decomposition",
        payload,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Lag profile.
    fig, ax = plt.subplots(
        figsize=(
            9,
            5,
        ),
    )

    lags = np.arange(
        1,
        horizon + 1,
    )

    ax.plot(
        lags,
        persistent_lag_mean,
        marker="o",
        label="retained",
    )

    ax.plot(
        lags,
        transient_lag_mean,
        marker="o",
        label="transient",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Lag after intervention"
    )

    ax.set_ylabel(
        "Force − prevent local attachments"
    )

    ax.set_title(
        "Chapter 23 V5: retained vs transient lag profile"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch23-v5-retained-vs-transient-lag.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    # Cumulative gain.
    fig, ax = plt.subplots(
        figsize=(
            9,
            5,
        ),
    )

    ax.plot(
        lags,
        persistent_cumulative,
        marker="o",
        label="retained",
    )

    ax.plot(
        lags,
        transient_cumulative,
        marker="o",
        label="transient",
    )

    ax.axhline(
        1.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Horizon H"
    )

    ax.set_ylabel(
        "Cumulative causal construction gain"
    )

    ax.set_title(
        "Chapter 23 V5: G(H) by retained vs transient intervention"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch23-v5-cumulative-gain.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    return payload


# ============================================================================
# Stage 3 — probe strata
# ============================================================================

def stage_3_strata(
    reporter: Reporter,
    profile: dict,
    results: Sequence[
        ProbeResult
    ],
    seed: int,
) -> dict:
    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    strata = []

    for probe_index, quantile in enumerate(
        profile[
            "probe_quantiles"
        ]
    ):
        subset = [
            result
            for result in results
            if result.probe == probe_index
        ]

        def ci(
            getter,
            offset: int,
        ):
            return bootstrap_mean_ci(
                [
                    getter(
                        result
                    )
                    for result in subset
                ],
                reps,
                seed
                + offset
                + probe_index
                * 100,
            )

        strata.append({
            "probe": int(
                probe_index
            ),
            "quantile": float(
                quantile
            ),
            "baseline_probability": ci(
                lambda r:
                r.baseline_probability,
                2000,
            ),
            "occupied_neighbor_count": ci(
                lambda r:
                r.geometry[
                    "occupied_neighbor_count"
                ],
                2010,
            ),
            "ring1_newly_promoted_frontier": ci(
                lambda r:
                r.geometry[
                    "ring1_newly_promoted_frontier"
                ],
                2020,
            ),
            "global_frontier_delta_if_forced_before_loss": ci(
                lambda r:
                r.geometry[
                    "global_frontier_delta_if_forced_before_loss"
                ],
                2030,
            ),
            "g_mech_1": ci(
                lambda r:
                r.g_mech_1,
                2040,
            ),
            "retained_g1": ci(
                lambda r:
                r.persistent_g1,
                2050,
            ),
            "retained_G30": ci(
                lambda r:
                r.persistent.cumulative_local,
                2060,
            ),
            "transient_G30": ci(
                lambda r:
                r.transient.cumulative_local,
                2070,
            ),
            "retained_late_mean": ci(
                lambda r:
                r.persistent.late_mean,
                2080,
            ),
            "transient_late_mean": ci(
                lambda r:
                r.transient.late_mean,
                2090,
            ),
            "retained_x_occupied_growth_exposures": ci(
                lambda r:
                r.retained_x_occupied_updates,
                2100,
            ),
            "retained_x_occupancy_fraction": ci(
                lambda r:
                r.retained_x_occupancy_fraction,
                2110,
            ),
            "transient_x_reoccupation_fraction": ci(
                lambda r:
                1.0 if r.transient_x_reoccupied else 0.0,
                2120,
            ),
            "prevent_x_reoccupation_fraction": ci(
                lambda r:
                1.0 if r.prevent_x_reoccupied else 0.0,
                2130,
            ),
        })

    lowest = min(
        result.probe
        for result in results
    )

    highest = max(
        result.probe
        for result in results
    )

    by_group: Dict[
        int,
        Dict[
            int,
            ProbeResult,
        ],
    ] = {}

    for result in results:
        by_group.setdefault(
            result.group,
            {},
        )[
            result.probe
        ] = result

    paired = [
        pair
        for pair in by_group.values()
        if (
            lowest in pair
            and highest in pair
        )
    ]

    def paired_difference(
        getter,
    ) -> List[float]:
        return [
            float(
                getter(
                    pair[
                        lowest
                    ]
                )
                - getter(
                    pair[
                        highest
                    ]
                )
            )
            for pair in paired
        ]

    comparisons = {}

    comparison_defs = {
        "frontier_delta_low_minus_high": (
            lambda r:
            r.geometry[
                "global_frontier_delta_if_forced_before_loss"
            ]
        ),
        "promoted_frontier_low_minus_high": (
            lambda r:
            r.geometry[
                "ring1_newly_promoted_frontier"
            ]
        ),
        "transient_G30_low_minus_high": (
            lambda r:
            r.transient.cumulative_local
        ),
        "retained_G30_low_minus_high": (
            lambda r:
            r.persistent.cumulative_local
        ),
    }

    for index, (
        name,
        getter,
    ) in enumerate(
        comparison_defs.items()
    ):
        values = paired_difference(
            getter
        )

        comparisons[
            name
        ] = {
            "summary": (
                bootstrap_mean_ci(
                    values,
                    reps,
                    seed
                    + 3000
                    + index,
                )
            ),
            "paired_signflip_two_sided": (
                signflip_two_sided(
                    values,
                    int(
                        profile[
                            "signflip_permutations"
                        ]
                    ),
                    seed
                    + 3100
                    + index,
                )
            ),
        }

    payload = {
        "strata": strata,
        "paired_lowest_vs_highest": (
            comparisons
        ),
        "scope": (
            "Probe quantiles were predeclared. Stratum intervals are "
            "descriptive/confirmatory for this frozen V5 protocol; group is "
            "the independent unit."
        ),
    }

    reporter.json(
        "stage-03-probe-strata.json",
        payload,
    )

    reporter.stage(
        "stage-03-probe-strata.md",
        "Stage 3 — Corrected Local Gain Regimes by Probe Stratum",
        payload,
    )

    return payload


# ============================================================================
# Stage 4 — verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
) -> dict:
    valid = bool(
        stage1[
            "capacity_gate_passed"
        ]
        and stage1[
            "coverage_gate_passed"
        ]
        and stage1[
            "intervention_control_gate_passed"
        ]
    )

    r_late = stage2[
        "retained_late_mean"
    ]

    r_c = stage2[
        "retained_fit_c"
    ]

    t_late = stage2[
        "transient_late_mean"
    ]

    t_G = stage2[
        "transient_G_H_local"
    ]

    r_minus_t = stage2[
        "retained_minus_transient_cumulative"
    ]

    retained_offset_supported = bool(
        r_late[
            "mean"
        ]
        >= profile[
            "persistent_offset_floor"
        ]
        and r_late[
            "ci95_low"
        ]
        > 0.0
        and r_c[
            "ci95_low"
        ]
        > 0.0
    )

    transient_converged = bool(
        abs(
            t_late[
                "mean"
            ]
        )
        < profile[
            "transient_tail_abs_floor"
        ]
        and t_late[
            "ci95_low"
        ]
        >= -profile[
            "transient_tail_ci_bound"
        ]
        and t_late[
            "ci95_high"
        ]
        <= profile[
            "transient_tail_ci_bound"
        ]
    )

    transient_positive_cumulative = bool(
        t_G[
            "ci95_low"
        ]
        > 0.0
    )

    retained_larger_than_transient = bool(
        r_minus_t[
            "ci95_low"
        ]
        > 0.0
    )

    if (
        t_G[
            "ci95_high"
        ]
        < 1.0
    ):
        transient_reference = (
            "TRANSIENT_GAIN_BELOW_ONE_REFERENCE"
        )
    elif (
        t_G[
            "ci95_low"
        ]
        > 1.0
    ):
        transient_reference = (
            "TRANSIENT_GAIN_ABOVE_ONE_REFERENCE"
        )
    else:
        transient_reference = (
            "TRANSIENT_GAIN_UNRESOLVED_AROUND_ONE"
        )

    mech = stage2[
        "mechanical_discrepancy"
    ]

    mechanics_consistent = bool(
        abs(
            mech[
                "mean"
            ]
        )
        <= profile[
            "mechanical_tolerance"
        ]
        and mech[
            "ci95_low"
        ]
        <= 0.0
        <= mech[
            "ci95_high"
        ]
    )

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
            "One or more frozen V5 validity gates failed, including the "
            "corrected focal-state intervention-control assertions."
        )

    elif (
        transient_converged
        and retained_larger_than_transient
    ):
        status = (
            "CORRECTED_TRANSIENT_CONSEQUENCE_SEPARATED_FROM_RETAINED_ARM"
        )

        if transient_positive_cumulative:
            bounded = (
                "Under the frozen V5 corrected intervention, the transient "
                "branch has a positive finite-horizon cumulative causal "
                "consequence while its late accumulation rate is practically "
                "consistent with convergence. The retained arm produces a "
                "larger cumulative consequence. No permanent retained-arm "
                "growth-rate offset is implied."
            )
        else:
            bounded = (
                "Under the frozen V5 corrected intervention, the transient "
                "branch is practically consistent with no continuing positive "
                "late accumulation, while the retained arm produces a larger "
                "finite-horizon cumulative consequence. A positive transient "
                "total is not independently established."
            )

    elif transient_converged:
        status = (
            "CORRECTED_TRANSIENT_CONSEQUENCE_CONVERGES_RETAINED_CONTRAST_UNRESOLVED"
        )
        bounded = (
            "The corrected transient branch is practically consistent with "
            "no continuing positive late accumulation, but V5 did not establish "
            "a larger retained-arm cumulative consequence."
        )

    else:
        status = (
            "CORRECTED_GAIN_DECOMPOSITION_UNRESOLVED"
        )
        bounded = (
            "V5 did not cleanly establish the corrected transient/retained "
            "decomposition under the frozen criteria."
        )

    payload = {
        "validity": {
            "valid": valid,
            "capacity_gate": bool(
                stage1[
                    "capacity_gate_passed"
                ]
            ),
            "coverage_gate": bool(
                stage1[
                    "coverage_gate_passed"
                ]
            ),
            "intervention_control_gate": bool(
                stage1[
                    "intervention_control_gate_passed"
                ]
            ),
        },
        "retained_offset": {
            "late_mean": r_late,
            "fit_c": r_c,
            "floor": float(
                profile[
                    "persistent_offset_floor"
                ]
            ),
            "status": (
                "SUPPORTED"
                if retained_offset_supported
                else "FAILED"
            ),
            "note": (
                "RETAINED means not experimentally removed; x is not clamped "
                "occupied and remains subject to ordinary loss/reoccupation."
            ),
        },
        "transient_cumulative_consequence": {
            "G30": t_G,
            "status": (
                "SUPPORTED_POSITIVE"
                if transient_positive_cumulative
                else "POSITIVE_TOTAL_NOT_ESTABLISHED"
            ),
        },
        "transient_convergence": {
            "late_mean": t_late,
            "status": (
                "SUPPORTED"
                if transient_converged
                else "FAILED"
            ),
            "claim": (
                "No continuing positive transient accumulation over the frozen "
                "late window."
            ),
        },
        "retained_minus_transient": {
            "difference": r_minus_t,
            "status": (
                "SUPPORTED_RETAINED_LARGER"
                if retained_larger_than_transient
                else "NOT_ESTABLISHED"
            ),
        },
        "transient_critical_reference": {
            "G30": t_G,
            "status": (
                transient_reference
            ),
            "note": (
                "Reference only. Transient G(30) is not asserted to be a "
                "formal branching ratio."
            ),
        },
        "one_step_mechanical_accounting": {
            "discrepancy": mech,
            "status": (
                "CONSISTENT_WITH_MECHANICS"
                if mechanics_consistent
                else "NOT_ACCOUNTED_FOR_WITHIN_TOLERANCE"
            ),
        },
        "focal_state_diagnostics": stage2[
            "focal_state_diagnostics"
        ],
        "overall_status": status,
        "bounded_claim": bounded,
        "forbidden_overclaims": [
            "formal branching ratio",
            "supercritical neighbourhood",
            "proof of subcriticality",
            "permanent retained occupancy",
            "mathematical convergence theorem",
            "critical point",
            "phase transition",
            "directed percolation",
            "Hawkes process",
            "excitable medium",
            "wave",
            "individuality",
            "organism",
            "life",
        ],
        "next_if_strata_remain_large": (
            "Re-evaluate corrected stratum contrasts before promoting any "
            "geometry-to-long-run-gain relationship. Do not rescue failed "
            "comparisons by changing the frozen probe strata."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        payload,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 23 V5 Verdict",
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
        default=20260906,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch23-retained-transient-causal-gain-v5"
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
        "base_model_version": (
            BASE_MODEL_VERSION
        ),
        "parent_experiment_version": (
            PARENT_EXPERIMENT_VERSION
        ),
        "chapter": CHAPTER,
        "run_title": RUN_TITLE,
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "previous_seeds": {
            "v1": 20260902,
            "v2": 20260903,
            "v3": 20260904,
            "v4": 20260905,
        },
        "fresh_seed": bool(
            int(
                args.seed
            )
            not in {
                20260902,
                20260903,
                20260904,
                20260905,
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
        "intervention_timing": (
            "V5 direct state intervention at checkpoint; PREVENT blocks x "
            "during lag-1 growth; after lag-1 growth+loss x is removed from "
            "TRANSIENT and PREVENT before ordinary lag-2+ dynamics resume."
        ),
        "canonical_rules_modified": False,
        "construct_validity_correction": True,
        "started_at_unix": float(
            time.time()
        ),
    }

    print(
        "="
        * 78
    )
    print(
        "CHAPTER 23 V5 — CORRECTED RETAINED / TRANSIENT CONSEQUENCE"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"probes={len(profile['probe_quantiles'])} "
        f"H={profile['horizon']} "
        f"seed={args.seed}"
    )
    print(
        "="
        * 78
    )

    stage_0_protocol(
        reporter,
        profile,
        args.seed,
    )

    results, s1 = stage_1_run(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    if not results:
        raise RuntimeError(
            "No usable V5 corrected interventions."
        )

    s2 = stage_2_decomposition(
        reporter,
        profile,
        results,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_strata(
        reporter,
        profile,
        results,
        args.seed,
    )

    s4 = stage_4_verdict(
        reporter,
        profile,
        s1,
        s2,
    )

    metadata[
        "finished_at_unix"
    ] = float(
        time.time()
    )

    metadata[
        "final_status"
    ] = s4[
        "overall_status"
    ]

    metadata[
        "transient_reference"
    ] = s4[
        "transient_critical_reference"
    ][
        "status"
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
        f"FINAL STATUS: {s4['overall_status']}"
    )
    print(
        "TRANSIENT REFERENCE:",
        s4[
            "transient_critical_reference"
        ][
            "status"
        ],
    )
    print(
        s4[
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
