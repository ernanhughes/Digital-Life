#!/usr/bin/env python3
"""
Digital Life — Chapter 24 V1
Where Is Causal Gain Created?
=============================

PURPOSE
-------

Chapter 23 established:

1. a forced frontier attachment has measurable causal leverage;
2. its immediate effect is quantitatively consistent with the frozen local rule;
3. a transient force/remove cascade is small and converges;
4. sparse and dense frontier geometries respond very differently to the same
   one-cell intervention;
5. the stronger claim that those geometric differences reliably produce
   different long-run causal gain was NOT established.

Chapter 24 therefore asks a narrower, mechanism-first question:

    Among locally comparable frontier sites, do interventions that create more
    new frontier opportunity produce greater transient causal gain?

The target is TRANSIENT causal gain, not persistent gain.

The intervention is:

    FORCE x during the canonical growth update
        vs
    PREVENT x during the same update

Both branches then receive the ordinary frozen loss step.

The forced cell is allowed to exert one full causal update.

After lag 1:
    if x is still occupied in FORCE, delete it.

The future then continues under ordinary frozen dynamics.

This removes continuing direct support from x and measures what causal
consequence the intervention launched into the process.

NEW OBSERVER: FRONTIER CREATION POTENTIAL
-----------------------------------------

For an eligible evaluated frontier cell x:

    FCP(x)
        =
        |frontier if x forced occupied|
        -
        |frontier before forcing x|

Interpretation:

    FCP > 0
        forcing x expands the number of currently available construction
        opportunities

    FCP = 0
        forcing x rearranges opportunity without changing total frontier count

    FCP < 0
        forcing x consumes more frontier opportunity than it creates

Supporting geometry records:

    occupied-neighbour count
    baseline attachment probability
    ring-1 empty neighbours
    ring-1 frontier neighbours
    ring-1 newly promoted frontier cells
    local frontier density within radius 2
    radial position

PRIMARY HYPOTHESIS
------------------

H1 — FRONTIER CREATION POTENTIAL PREDICTS TRANSIENT CAUSAL GAIN

Within each independent checkpoint, form matched HIGH-FCP / LOW-FCP site pairs.

Matching constraints are frozen:

    same occupied-neighbour count
    same radial bin (width 3)
    baseline attachment probability difference <= 0.05
    local frontier-density difference <= 0.10
    FCP difference >= 1

For every paired site independently measure:

    G_T(H)
        =
        cumulative FORCE - PREVENT realized attachments
        over lags 1..H
        and distances 1..H

with:
    H = 12

The group is the independent statistical unit.

For each group:
    average all within-group pair differences:

        Delta_G
            =
            G_T(high-FCP)
            -
            G_T(low-FCP)

Frozen success gates:

    mean Delta_G >= +0.15 attachments
    95% bootstrap CI lower bound > 0
    paired group-level sign-flip p < 0.05
    at least 70% of requested groups produce >= 1 usable matched pair

If successful, the bounded sentence is:

    Among locally comparable evaluated frontier sites, forcing sites that
    create more frontier opportunity produces greater transient causal
    construction gain under the frozen Digital Crystal dynamics.

This does NOT establish that FCP is the only determinant of gain.

SECONDARY HYPOTHESES
---------------------

H2 — FRONTIER PROMOTION MECHANISM

For matched pairs:

    Delta_promoted
        =
        newly promoted ring-1 frontier(high)
        -
        newly promoted ring-1 frontier(low)

must be positive with:
    mean >= +1.0 cell
    95% CI lower bound > 0
    sign-flip p < 0.05

This checks that the high/low FCP contrast is mechanistically what it claims to be.

H3 — BASELINE PROBABILITY IS NOT SUFFICIENT

Because pairs are matched on baseline p within <= 0.05, report:

    abs(mean p_high - p_low)

and its CI.

No claim requires it to equal zero exactly.

The point is that any H1 gain difference survives a deliberately small
baseline-p difference.

H4 — LOCAL GAIN IS NOT JUST GLOBAL BUDGET REDISTRIBUTION

Report, for high and low FCP sites separately:

    local transient gain
    global transient gain
    far-field gain = global - local
    evaluated-set overlap with PREVENT

H1 is based on LOCAL transient gain.

A large positive local effect accompanied by equally large negative far-field
gain would indicate redistribution rather than net construction gain.

DESCRIPTIVE MAP
---------------

No classifier is used in V1.

Across all sampled sites, report descriptive relationships between transient
gain and:

    FCP
    ring-1 promoted frontier
    occupied-neighbour count
    baseline p
    local frontier density

Use:
    binned means
    Spearman correlation
    direct scatter plots

These are descriptive only.

No random forest.
No neural net.
No post-hoc feature search.

PAIR CONSTRUCTION
-----------------

Candidate sites come from the EXACT evaluated candidate set of the
intervention update.

This matters because Chapter 23 showed that observational matching can become
load-bearing.

For each checkpoint:

1. build the exact evaluated set;
2. restrict to sites at least H+2 cells from the hard outer boundary;
3. compute local geometry and FCP for every site;
4. construct one-to-one high/low FCP pairs without replacement;
5. maximize FCP contrast while satisfying all frozen matching constraints.

"High" and "low" are relative only to the matched pair.

No global threshold is tuned from the result.

FRESHNESS
---------

Default seed:
    20260906

Previous:
    Chapter 23 V1  20260902
    Chapter 23 V2  20260903
    Chapter 23 V3  20260904
    Chapter 23 V4  20260905

SCIENTIFIC BOUNDARY
-------------------

Success would support:

    frontier-creation geometry as a causal predictor of local transient
    construction gain under the tested Digital Crystal substrate.

It would NOT establish:

    a causal-gain field as a physical field
    criticality
    percolation
    phase transition
    branching process
    coherent structure
    natural boundary
    individuality
    autonomy
    organism
    life

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
EXPERIMENT_VERSION = "digital-crystal-frontier-creation-causal-gain-v1"
SCHEMA_VERSION = 1
CHAPTER = 24
CHAPTER_TITLE = "Where Is Causal Gain Created?"


PROFILES = {
    "smoke": {
        "groups": 8,
        "radius": 52,
        "warmup_steps": 14,
        "lossy_pre_steps": 12,
        "horizon": 6,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.08,
        "local_frontier_density_tolerance": 0.15,
        "minimum_fcp_difference": 1,
        "minimum_pair_gain_difference": 0.15,
        "minimum_promoted_difference": 1.0,
        "minimum_group_coverage_fraction": 0.50,
        "max_pairs_per_group": 4,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "radius": 76,
        "warmup_steps": 20,
        "lossy_pre_steps": 20,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "minimum_fcp_difference": 1,
        "minimum_pair_gain_difference": 0.15,
        "minimum_promoted_difference": 1.0,
        "minimum_group_coverage_fraction": 0.70,
        "max_pairs_per_group": 8,
        "bootstrap_reps": 3000,
        "signflip_permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "radius": 92,
        "warmup_steps": 24,
        "lossy_pre_steps": 24,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "minimum_fcp_difference": 1,
        "minimum_pair_gain_difference": 0.15,
        "minimum_promoted_difference": 1.0,
        "minimum_group_coverage_fraction": 0.70,
        "max_pairs_per_group": 10,
        "bootstrap_reps": 5000,
        "signflip_permutations": 12000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "radius": 108,
        "warmup_steps": 24,
        "lossy_pre_steps": 28,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "minimum_fcp_difference": 1,
        "minimum_pair_gain_difference": 0.15,
        "minimum_promoted_difference": 1.0,
        "minimum_group_coverage_fraction": 0.70,
        "max_pairs_per_group": 12,
        "bootstrap_reps": 7000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Frozen Digital Crystal helpers
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


def growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
    force_cell: Cell | None = None,
    prevent_cell: Cell | None = None,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    List[Cell],
    int,
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

    frontier = frontier_cells(
        occupied_before,
        radius,
    )

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
            "force cell not in exact evaluated set"
        )

    if (
        prevent_cell is not None
        and prevent_cell not in selected_set
    ):
        raise RuntimeError(
            "prevent cell not in exact evaluated set"
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
    ) = growth_step(
        state,
        input_value,
        radius,
        crystal_params,
        budget,
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


# ============================================================================
# Checkpoint
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


# ============================================================================
# Local geometry and FCP
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


def cells_within_hex_radius(
    origin: Cell,
    radius: int,
) -> List[Cell]:
    oq, or_ = origin

    out: List[Cell] = []

    for dq in range(
        -radius,
        radius + 1,
    ):
        for dr in range(
            -radius,
            radius + 1,
        ):
            candidate = (
                oq + dq,
                or_ + dr,
            )

            if (
                relative_distance(
                    candidate,
                    origin,
                )
                <= radius
            ):
                out.append(
                    candidate
                )

    return out


@dataclass
class SiteGeometry:
    cell: Cell
    baseline_p: float
    occupied_neighbors: int
    radial_distance: int
    radial_bin: int
    ring1_empty_neighbors: int
    ring1_frontier_before: int
    ring1_newly_promoted_frontier: int
    local_frontier_density_r2: float
    frontier_before_count: int
    frontier_after_count: int
    fcp: int


def site_geometry(
    checkpoint: ch18.MaterialCrystalState,
    cell: Cell,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> SiteGeometry:
    occupied = set(
        checkpoint.occupied
    )

    radius = int(
        profile[
            "radius"
        ]
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
        cell
    )

    frontier_after = set(
        frontier_cells(
            occupied_force,
            radius,
        )
    )

    ring = list(
        ch18.neighbors(
            cell
        )
    )

    ring_empty = [
        x
        for x in ring
        if x not in occupied
    ]

    ring_frontier_before = [
        x
        for x in ring_empty
        if x in frontier_before
    ]

    ring_promoted = [
        x
        for x in ring_empty
        if (
            x not in frontier_before
            and x in frontier_after
        )
    ]

    neighborhood = cells_within_hex_radius(
        cell,
        2,
    )

    local_frontier_count = sum(
        x in frontier_before
        for x in neighborhood
    )

    local_density = (
        local_frontier_count
        / len(
            neighborhood
        )
    )

    radial_distance = int(
        ch18.hex_distance(
            cell
        )
    )

    return SiteGeometry(
        cell=cell,
        baseline_p=float(
            attachment_probability(
                cell,
                occupied,
                next_input,
                crystal_params,
            )
        ),
        occupied_neighbors=int(
            sum(
                nb in occupied
                for nb in ring
            )
        ),
        radial_distance=radial_distance,
        radial_bin=int(
            radial_distance
            // int(
                profile[
                    "radial_bin_width"
                ]
            )
        ),
        ring1_empty_neighbors=int(
            len(
                ring_empty
            )
        ),
        ring1_frontier_before=int(
            len(
                ring_frontier_before
            )
        ),
        ring1_newly_promoted_frontier=int(
            len(
                ring_promoted
            )
        ),
        local_frontier_density_r2=float(
            local_density
        ),
        frontier_before_count=int(
            len(
                frontier_before
            )
        ),
        frontier_after_count=int(
            len(
                frontier_after
            )
        ),
        fcp=int(
            len(
                frontier_after
            )
            - len(
                frontier_before
            )
        ),
    )


def evaluated_site_geometries(
    checkpoint: ch18.MaterialCrystalState,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    SiteGeometry
]:
    radius = int(
        profile[
            "radius"
        ]
    )

    horizon = int(
        profile[
            "horizon"
        ]
    )

    margin = (
        horizon
        + 2
    )

    frontier = frontier_cells(
        checkpoint.occupied,
        radius,
    )

    selected = ch21.select_candidates(
        frontier,
        int(
            profile[
                "budget"
            ]
        ),
        checkpoint.stream_seed,
        int(
            checkpoint.step + 1
        ),
    )

    usable = [
        cell
        for cell in selected
        if (
            ch18.hex_distance(
                cell
            )
            <= radius - margin
        )
    ]

    return [
        site_geometry(
            checkpoint,
            cell,
            next_input,
            profile,
            crystal_params,
        )
        for cell in usable
    ]


# ============================================================================
# Frozen matched high/low FCP pairs
# ============================================================================

@dataclass
class SitePair:
    high: SiteGeometry
    low: SiteGeometry


def pair_compatible(
    high: SiteGeometry,
    low: SiteGeometry,
    profile: dict,
) -> bool:
    if (
        high.fcp
        - low.fcp
        < int(
            profile[
                "minimum_fcp_difference"
            ]
        )
    ):
        return False

    if (
        high.occupied_neighbors
        != low.occupied_neighbors
    ):
        return False

    if (
        high.radial_bin
        != low.radial_bin
    ):
        return False

    if (
        abs(
            high.baseline_p
            - low.baseline_p
        )
        > float(
            profile[
                "probability_tolerance"
            ]
        )
    ):
        return False

    if (
        abs(
            high.local_frontier_density_r2
            - low.local_frontier_density_r2
        )
        > float(
            profile[
                "local_frontier_density_tolerance"
            ]
        )
    ):
        return False

    return True


def construct_pairs(
    sites: Sequence[
        SiteGeometry
    ],
    profile: dict,
) -> List[
    SitePair
]:
    """
    Greedy one-to-one pairing without replacement.

    Candidate pairs are ranked by:
        largest FCP contrast,
        then smallest baseline-p difference,
        then smallest local-density difference.
    """
    candidates = []

    for i, a in enumerate(
        sites
    ):
        for j, b in enumerate(
            sites
        ):
            if i >= j:
                continue

            if a.fcp == b.fcp:
                continue

            high, low = (
                (a, b)
                if a.fcp > b.fcp
                else (b, a)
            )

            if not pair_compatible(
                high,
                low,
                profile,
            ):
                continue

            candidates.append(
                (
                    -(
                        high.fcp
                        - low.fcp
                    ),
                    abs(
                        high.baseline_p
                        - low.baseline_p
                    ),
                    abs(
                        high.local_frontier_density_r2
                        - low.local_frontier_density_r2
                    ),
                    high.cell,
                    low.cell,
                    high,
                    low,
                )
            )

    candidates.sort(
        key=lambda x: x[
            :5
        ]
    )

    used: Set[
        Cell
    ] = set()

    pairs: List[
        SitePair
    ] = []

    for item in candidates:
        high = item[
            5
        ]
        low = item[
            6
        ]

        if (
            high.cell in used
            or low.cell in used
        ):
            continue

        used.add(
            high.cell
        )
        used.add(
            low.cell
        )

        pairs.append(
            SitePair(
                high=high,
                low=low,
            )
        )

        if (
            len(
                pairs
            )
            >= int(
                profile[
                    "max_pairs_per_group"
                ]
            )
        ):
            break

    return pairs


# ============================================================================
# Transient intervention
# ============================================================================

@dataclass
class InterventionResult:
    group: int
    pair_index: int
    side: str
    geometry: SiteGeometry
    g1: float
    G_local: float
    G_global: float
    far_field_gain: float
    lag_gain_local: List[float]
    selected_overlap_fraction: List[float]
    max_capacity_fraction: float


def selected_overlap(
    a: Sequence[Cell],
    b: Sequence[Cell],
) -> float:
    sa = set(
        a
    )
    sb = set(
        b
    )

    union = (
        sa
        | sb
    )

    if not union:
        return 1.0

    return float(
        len(
            sa
            & sb
        )
        / len(
            union
        )
    )


def run_transient_intervention(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    geometry: SiteGeometry,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    group: int,
    pair_index: int,
    side: str,
) -> InterventionResult:
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

    x = geometry.cell

    # Intervention update: force vs prevent on exact same candidate.
    (
        force_grown,
        _force_add,
        force_selected,
        _,
    ) = growth_step(
        checkpoint,
        float(
            future_env[
                0
            ]
        ),
        radius,
        crystal_params,
        budget,
        force_cell=x,
    )

    (
        prevent_grown,
        _prevent_add,
        prevent_selected,
        _,
    ) = growth_step(
        checkpoint,
        float(
            future_env[
                0
            ]
        ),
        radius,
        crystal_params,
        budget,
        prevent_cell=x,
    )

    if (
        force_selected
        != prevent_selected
    ):
        raise RuntimeError(
            "intervention-step evaluated sets diverged unexpectedly"
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    lag_local: List[
        float
    ] = []

    lag_global: List[
        float
    ] = []

    overlaps: List[
        float
    ] = []

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

    g1 = 0.0

    for lag in range(
        1,
        horizon + 1,
    ):
        (
            force_state,
            force_add,
            _,
            force_eval,
            _,
        ) = canonical_step(
            force_state,
            float(
                future_env[
                    lag
                ]
            ),
            radius,
            crystal_params,
            budget,
            loss_rate,
        )

        (
            prevent_state,
            prevent_add,
            _,
            prevent_eval,
            _,
        ) = canonical_step(
            prevent_state,
            float(
                future_env[
                    lag
                ]
            ),
            radius,
            crystal_params,
            budget,
            loss_rate,
        )

        force_local = sum(
            (
                cell != x
                and 1
                <= relative_distance(
                    cell,
                    x,
                )
                <= horizon
            )
            for cell in force_add
        )

        prevent_local = sum(
            (
                cell != x
                and 1
                <= relative_distance(
                    cell,
                    x,
                )
                <= horizon
            )
            for cell in prevent_add
        )

        local_delta = float(
            force_local
            - prevent_local
        )

        global_delta = float(
            sum(
                cell != x
                for cell in force_add
            )
            - sum(
                cell != x
                for cell in prevent_add
            )
        )

        lag_local.append(
            local_delta
        )
        lag_global.append(
            global_delta
        )
        overlaps.append(
            selected_overlap(
                force_eval,
                prevent_eval,
            )
        )

        if lag == 1:
            g1 = local_delta

            # Remove direct support after one full causal update.
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

    G_local = float(
        np.sum(
            lag_local
        )
    )

    G_global = float(
        np.sum(
            lag_global
        )
    )

    return InterventionResult(
        group=int(
            group
        ),
        pair_index=int(
            pair_index
        ),
        side=side,
        geometry=geometry,
        g1=float(
            g1
        ),
        G_local=G_local,
        G_global=G_global,
        far_field_gain=float(
            G_global
            - G_local
        ),
        lag_gain_local=[
            float(
                x_
            )
            for x_ in lag_local
        ],
        selected_overlap_fraction=[
            float(
                x_
            )
            for x_ in overlaps
        ],
        max_capacity_fraction=float(
            max_capacity
        ),
    )


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
            float(
                x
            )
            for x in values
            if math.isfinite(
                float(
                    x
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
        "ci95_low": low,
        "ci95_high": high,
        "half_width": float(
            (
                high
                - low
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
            float(
                x
            )
            for x in values
            if math.isfinite(
                float(
                    x
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
                null
                >= observed
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
        "observed_mean": observed,
        "p_value": float(
            p
        ),
        "permutations": int(
            permutations
        ),
    }


def rankdata(
    arr: np.ndarray,
) -> np.ndarray:
    order = np.argsort(
        arr,
        kind="mergesort",
    )

    ranks = np.empty(
        len(
            arr
        ),
        dtype=float,
    )

    start = 0

    while start < len(
        arr
    ):
        end = (
            start + 1
        )

        while (
            end < len(
                arr
            )
            and arr[
                order[
                    end
                ]
            ]
            == arr[
                order[
                    start
                ]
            ]
        ):
            end += 1

        avg = (
            start
            + end
            - 1
        ) / 2.0

        ranks[
            order[
                start:end
            ]
        ] = avg

        start = end

    return ranks


def spearman(
    x: Sequence[float],
    y: Sequence[float],
) -> float:
    xa = np.asarray(
        x,
        dtype=float,
    )

    ya = np.asarray(
        y,
        dtype=float,
    )

    mask = (
        np.isfinite(
            xa
        )
        & np.isfinite(
            ya
        )
    )

    xa = xa[
        mask
    ]

    ya = ya[
        mask
    ]

    if len(
        xa
    ) < 3:
        return float(
            "nan"
        )

    rx = rankdata(
        xa
    )

    ry = rankdata(
        ya
    )

    if (
        np.std(
            rx
        )
        == 0
        or np.std(
            ry
        )
        == 0
    ):
        return float(
            "nan"
        )

    return float(
        np.corrcoef(
            rx,
            ry,
        )[
            0,
            1
        ]
    )


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
            / "ch24-frontier-creation-causal-gain-v1-full-report.md"
        )

        parts = [
            "# Chapter 24 — Where Is Causal Gain Created? (V1)",
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
            "FRONTIER CREATION POTENTIAL / TRANSIENT CAUSAL GAIN TEST"
        ),
        "fresh_seed": int(
            seed
        ),
        "target": (
            "transient causal gain G_T(H), force x then remove after one "
            "causal update"
        ),
        "horizon": int(
            profile[
                "horizon"
            ]
        ),
        "FCP_definition": (
            "|frontier after forcing x occupied| - |frontier before forcing x|"
        ),
        "matching": {
            "same_occupied_neighbor_count": True,
            "same_radial_bin_width": int(
                profile[
                    "radial_bin_width"
                ]
            ),
            "max_baseline_probability_difference": float(
                profile[
                    "probability_tolerance"
                ]
            ),
            "max_local_frontier_density_difference": float(
                profile[
                    "local_frontier_density_tolerance"
                ]
            ),
            "minimum_fcp_difference": int(
                profile[
                    "minimum_fcp_difference"
                ]
            ),
        },
        "H1": {
            "quantity": (
                "G_T(high-FCP) - G_T(low-FCP), averaged to one value/group"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_pair_gain_difference"
                ]
            ),
            "requires_ci_low_above_zero": True,
            "alpha": float(
                profile[
                    "alpha"
                ]
            ),
        },
        "H2": {
            "quantity": (
                "ring1 newly promoted frontier(high) - low"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_promoted_difference"
                ]
            ),
            "requires_ci_low_above_zero": True,
        },
        "coverage_gate": float(
            profile[
                "minimum_group_coverage_fraction"
            ]
        ),
        "descriptive_only": [
            "Spearman correlations",
            "scatter plots",
            "binned means",
        ],
        "no_classifier": True,
        "scientific_boundary": (
            "Local frontier geometry as a causal predictor of transient "
            "construction gain only."
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
        payload,
    )

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 24 V1 Protocol",
        payload,
    )

    return payload


# ============================================================================
# Stage 1 — generate pairs and run interventions
# ============================================================================

def stage_1_run(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[
        Tuple[
            InterventionResult,
            InterventionResult,
        ]
    ],
    dict,
]:
    paired_results: List[
        Tuple[
            InterventionResult,
            InterventionResult,
        ]
    ] = []

    groups_with_pairs = 0
    max_capacity = 0.0
    pair_counts = []

    for group in tqdm(
        range(
            int(
                profile[
                    "groups"
                ]
            )
        ),
        desc="Chapter 24 V1 matched FCP groups",
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
            pair_counts.append(
                0
            )
            continue

        sites = evaluated_site_geometries(
            checkpoint,
            float(
                future_env[
                    0
                ]
            ),
            profile,
            crystal_params,
        )

        pairs = construct_pairs(
            sites,
            profile,
        )

        pair_counts.append(
            len(
                pairs
            )
        )

        if not pairs:
            continue

        groups_with_pairs += 1

        for pair_index, pair in enumerate(
            pairs
        ):
            high = run_transient_intervention(
                checkpoint,
                future_env,
                pair.high,
                profile,
                crystal_params,
                group,
                pair_index,
                "high",
            )

            low = run_transient_intervention(
                checkpoint,
                future_env,
                pair.low,
                profile,
                crystal_params,
                group,
                pair_index,
                "low",
            )

            max_capacity = max(
                max_capacity,
                high.max_capacity_fraction,
                low.max_capacity_fraction,
            )

            paired_results.append(
                (
                    high,
                    low,
                )
            )

    coverage_fraction = (
        groups_with_pairs
        / max(
            1,
            int(
                profile[
                    "groups"
                ]
            ),
        )
    )

    payload = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "groups_with_pairs": int(
            groups_with_pairs
        ),
        "coverage_fraction": float(
            coverage_fraction
        ),
        "minimum_coverage_fraction": float(
            profile[
                "minimum_group_coverage_fraction"
            ]
        ),
        "coverage_gate_passed": bool(
            coverage_fraction
            >= profile[
                "minimum_group_coverage_fraction"
            ]
        ),
        "total_pairs": int(
            len(
                paired_results
            )
        ),
        "mean_pairs_per_group_with_pairs": float(
            len(
                paired_results
            )
            / max(
                1,
                groups_with_pairs,
            )
        ),
        "pair_count_distribution": {
            "min": int(
                min(
                    pair_counts
                )
                if pair_counts
                else 0
            ),
            "median": float(
                np.median(
                    pair_counts
                )
                if pair_counts
                else 0.0
            ),
            "max": int(
                max(
                    pair_counts
                )
                if pair_counts
                else 0
            ),
        },
        "maximum_capacity_fraction": float(
            max_capacity
        ),
        "capacity_gate_passed": bool(
            max_capacity
            < profile[
                "max_capacity_fraction"
            ]
        ),
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-matched-interventions.json",
        payload,
    )

    reporter.stage(
        "stage-01-matched-interventions.md",
        "Stage 1 — Matched High/Low FCP Interventions",
        payload,
    )

    return (
        paired_results,
        payload,
    )


# ============================================================================
# Stage 2 — primary matched tests
# ============================================================================

def group_pair_means(
    paired_results: Sequence[
        Tuple[
            InterventionResult,
            InterventionResult,
        ]
    ],
    getter,
) -> List[float]:
    buckets: Dict[
        int,
        List[float],
    ] = {}

    for high, low in paired_results:
        buckets.setdefault(
            high.group,
            [],
        ).append(
            float(
                getter(
                    high,
                    low,
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


def stage_2_primary(
    reporter: Reporter,
    profile: dict,
    paired_results: Sequence[
        Tuple[
            InterventionResult,
            InterventionResult,
        ]
    ],
    seed: int,
) -> dict:
    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    perms = int(
        profile[
            "signflip_permutations"
        ]
    )

    gain_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.G_local
        - l.G_local,
    )

    promoted_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.geometry.ring1_newly_promoted_frontier
        - l.geometry.ring1_newly_promoted_frontier,
    )

    fcp_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.geometry.fcp
        - l.geometry.fcp,
    )

    p_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.geometry.baseline_p
        - l.geometry.baseline_p,
    )

    density_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.geometry.local_frontier_density_r2
        - l.geometry.local_frontier_density_r2,
    )

    global_gain_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.G_global
        - l.G_global,
    )

    far_field_deltas = group_pair_means(
        paired_results,
        lambda h, l:
        h.far_field_gain
        - l.far_field_gain,
    )

    H1_summary = bootstrap_mean_ci(
        gain_deltas,
        reps,
        seed + 201,
    )

    H1_test = signflip_greater(
        gain_deltas,
        perms,
        seed + 202,
    )

    H2_summary = bootstrap_mean_ci(
        promoted_deltas,
        reps,
        seed + 203,
    )

    H2_test = signflip_greater(
        promoted_deltas,
        perms,
        seed + 204,
    )

    payload = {
        "H1_high_fcp_greater_transient_gain": {
            "group_delta_G_local": (
                H1_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_pair_gain_difference"
                ]
            ),
            "signflip": H1_test,
        },
        "H2_frontier_promotion_contrast": {
            "group_delta_promoted_frontier": (
                H2_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_promoted_difference"
                ]
            ),
            "signflip": H2_test,
        },
        "matching_diagnostics": {
            "fcp_difference": bootstrap_mean_ci(
                fcp_deltas,
                reps,
                seed + 205,
            ),
            "baseline_probability_difference_high_minus_low": (
                bootstrap_mean_ci(
                    p_deltas,
                    reps,
                    seed + 206,
                )
            ),
            "local_frontier_density_difference_high_minus_low": (
                bootstrap_mean_ci(
                    density_deltas,
                    reps,
                    seed + 207,
                )
            ),
        },
        "system_level_diagnostics": {
            "global_gain_difference_high_minus_low": (
                bootstrap_mean_ci(
                    global_gain_deltas,
                    reps,
                    seed + 208,
                )
            ),
            "far_field_gain_difference_high_minus_low": (
                bootstrap_mean_ci(
                    far_field_deltas,
                    reps,
                    seed + 209,
                )
            ),
        },
    }

    reporter.json(
        "stage-02-primary-matched-tests.json",
        payload,
    )

    reporter.stage(
        "stage-02-primary-matched-tests.md",
        "Stage 2 — Primary Matched FCP Tests",
        payload,
    )

    return payload


# ============================================================================
# Stage 3 — descriptive causal-gain map
# ============================================================================

def stage_3_map(
    reporter: Reporter,
    paired_results: Sequence[
        Tuple[
            InterventionResult,
            InterventionResult,
        ]
    ],
    image_dir: Path,
) -> dict:
    observations: List[
        InterventionResult
    ] = []

    for high, low in paired_results:
        observations.extend(
            [
                high,
                low,
            ]
        )

    FCP = [
        float(
            x.geometry.fcp
        )
        for x in observations
    ]

    promoted = [
        float(
            x.geometry.ring1_newly_promoted_frontier
        )
        for x in observations
    ]

    n = [
        float(
            x.geometry.occupied_neighbors
        )
        for x in observations
    ]

    p = [
        float(
            x.geometry.baseline_p
        )
        for x in observations
    ]

    density = [
        float(
            x.geometry.local_frontier_density_r2
        )
        for x in observations
    ]

    gain = [
        float(
            x.G_local
        )
        for x in observations
    ]

    correlations = {
        "FCP_vs_gain": spearman(
            FCP,
            gain,
        ),
        "promoted_frontier_vs_gain": spearman(
            promoted,
            gain,
        ),
        "occupied_neighbors_vs_gain": spearman(
            n,
            gain,
        ),
        "baseline_probability_vs_gain": spearman(
            p,
            gain,
        ),
        "local_frontier_density_vs_gain": spearman(
            density,
            gain,
        ),
    }

    fcp_values = sorted(
        set(
            int(
                x
            )
            for x in FCP
        )
    )

    binned = []

    for value in fcp_values:
        subset = [
            gain_value
            for fcp_value, gain_value in zip(
                FCP,
                gain,
            )
            if int(
                fcp_value
            )
            == value
        ]

        binned.append({
            "FCP": int(
                value
            ),
            "n": int(
                len(
                    subset
                )
            ),
            "mean_transient_gain": float(
                np.mean(
                    subset
                )
            )
            if subset
            else float(
                "nan"
            ),
        })

    payload = {
        "n_intervention_sites": int(
            len(
                observations
            )
        ),
        "spearman_correlations_descriptive": (
            correlations
        ),
        "gain_by_FCP": binned,
        "scope": (
            "Descriptive only. Sites within checkpoints are repeated measures "
            "and are not treated as independent confirmatory replicates."
        ),
    }

    reporter.json(
        "stage-03-causal-gain-map.json",
        payload,
    )

    reporter.stage(
        "stage-03-causal-gain-map.md",
        "Stage 3 — Descriptive Local Causal-Gain Map",
        payload,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Scatter: FCP vs transient gain.
    fig, ax = plt.subplots(
        figsize=(
            8,
            5,
        ),
    )

    ax.scatter(
        FCP,
        gain,
        alpha=0.5,
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Frontier Creation Potential"
    )

    ax.set_ylabel(
        "Transient causal gain G_T(H)"
    )

    ax.set_title(
        "Chapter 24 V1: FCP versus transient causal gain"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch24-v1-fcp-vs-transient-gain.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    # Binned mean.
    fig, ax = plt.subplots(
        figsize=(
            8,
            5,
        ),
    )

    ax.plot(
        [
            row[
                "FCP"
            ]
            for row in binned
        ],
        [
            row[
                "mean_transient_gain"
            ]
            for row in binned
        ],
        marker="o",
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Frontier Creation Potential"
    )

    ax.set_ylabel(
        "Mean transient causal gain"
    )

    ax.set_title(
        "Chapter 24 V1: mean gain by FCP"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch24-v1-mean-gain-by-fcp.png",
        dpi=160,
    )

    plt.close(
        fig
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
            "coverage_gate_passed"
        ]
        and stage1[
            "capacity_gate_passed"
        ]
    )

    H1 = stage2[
        "H1_high_fcp_greater_transient_gain"
    ]

    H2 = stage2[
        "H2_frontier_promotion_contrast"
    ]

    H1_summary = H1[
        "group_delta_G_local"
    ]

    H1_test = H1[
        "signflip"
    ]

    H2_summary = H2[
        "group_delta_promoted_frontier"
    ]

    H2_test = H2[
        "signflip"
    ]

    H1_supported = bool(
        valid
        and H1_summary[
            "mean"
        ]
        >= profile[
            "minimum_pair_gain_difference"
        ]
        and H1_summary[
            "ci95_low"
        ]
        > 0.0
        and H1_test[
            "p_value"
        ]
        < profile[
            "alpha"
        ]
    )

    H2_supported = bool(
        valid
        and H2_summary[
            "mean"
        ]
        >= profile[
            "minimum_promoted_difference"
        ]
        and H2_summary[
            "ci95_low"
        ]
        > 0.0
        and H2_test[
            "p_value"
        ]
        < profile[
            "alpha"
        ]
    )

    if not profile[
        "scientific"
    ]:
        status = (
            "ENGINEERING_SMOKE_ONLY"
        )
        bounded = (
            "Smoke profile completed. No scientific interpretation is eligible."
        )

    elif not valid:
        status = (
            "INVALID_FOR_SCIENTIFIC_INTERPRETATION"
        )
        bounded = (
            "Frozen coverage or capacity validity gates failed."
        )

    elif (
        H1_supported
        and H2_supported
    ):
        status = (
            "FRONTIER_CREATION_PREDICTS_TRANSIENT_CAUSAL_GAIN"
        )
        bounded = (
            "Among locally comparable evaluated frontier sites, forcing cells "
            "that create more frontier opportunity produced greater transient "
            "causal construction gain. The matched high-FCP sites also "
            "promoted more new ring-1 frontier cells, supporting frontier "
            "creation as a mechanistic predictor under the tested substrate."
        )

    elif H2_supported:
        status = (
            "FRONTIER_GEOMETRY_CONTRAST_SUPPORTED_GAIN_LINK_FAILED"
        )
        bounded = (
            "The matched high-FCP sites created more frontier opportunity as "
            "designed, but the frozen experiment did not establish a "
            "scientifically meaningful increase in transient causal gain."
        )

    else:
        status = (
            "FCP_CAUSAL_GAIN_HYPOTHESIS_FAILED"
        )
        bounded = (
            "Chapter 24 V1 did not establish the frozen Frontier Creation "
            "Potential mechanism or its predicted transient-gain difference."
        )

    payload = {
        "validity": {
            "valid": valid,
            "coverage_gate": bool(
                stage1[
                    "coverage_gate_passed"
                ]
            ),
            "capacity_gate": bool(
                stage1[
                    "capacity_gate_passed"
                ]
            ),
        },
        "H1": {
            "status": (
                "SUPPORTED"
                if H1_supported
                else "FAILED"
            ),
            "result": H1,
        },
        "H2": {
            "status": (
                "SUPPORTED"
                if H2_supported
                else "FAILED"
            ),
            "result": H2,
        },
        "overall_status": status,
        "bounded_claim": bounded,
        "what_this_does_not_establish": [
            "FCP is the only determinant of causal gain",
            "causal-gain field is a physical field",
            "high-gain regions",
            "spatial clustering",
            "temporal persistence",
            "percolation",
            "criticality",
            "phase transition",
            "coherent structure",
            "natural boundary",
            "individuality",
            "organism",
            "life",
        ],
        "next_if_supported": (
            "Map a validated local gain proxy across whole frontiers and test "
            "whether high-gain locations cluster in space beyond matched "
            "radial/density controls."
        ),
        "next_if_failed": (
            "Do not add a classifier. Audit which local geometric term "
            "actually distinguishes causal gain before attempting spatial maps."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        payload,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 24 V1 Verdict",
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
            "research/digital-life/ch24-frontier-creation-causal-gain-v1"
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
        "chapter_title": (
            CHAPTER_TITLE
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "previous_ch23_seeds": [
            20260902,
            20260903,
            20260904,
            20260905,
        ],
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
        "target": (
            "transient causal gain"
        ),
        "classifier_used": False,
        "canonical_rules_modified": False,
        "started_at_unix": float(
            time.time()
        ),
    }

    print(
        "="
        * 78
    )

    print(
        "CHAPTER 24 V1 — WHERE IS CAUSAL GAIN CREATED?"
    )

    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"H={profile['horizon']} "
        f"max_pairs/group={profile['max_pairs_per_group']} "
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

    paired_results, s1 = stage_1_run(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    if not paired_results:
        raise RuntimeError(
            "No usable matched FCP pairs were generated."
        )

    s2 = stage_2_primary(
        reporter,
        profile,
        paired_results,
        args.seed,
    )

    s3 = stage_3_map(
        reporter,
        paired_results,
        args.image_dir,
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
