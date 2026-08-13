#!/usr/bin/env python3
"""
Digital Life — Chapter 24 V3
Does Recent Local Process History Determine Causal Gain?
========================================================

CONTEXT
-------

Chapter 24 V1:
    Frontier Creation Potential strongly distinguished immediate opportunity
    geometry, but did NOT establish greater transient causal gain.

Chapter 24 V2:
    Exact six-neighbour motif did NOT add detectable transient-gain or
    opportunity information beyond matched scalar state.

The next qualitatively new candidate is therefore not a larger static
neighbourhood.

It is PROCESS HISTORY.

Two frontier sites can look similar now while having arrived there through
different recent local dynamics:

    recent attachment
    recent loss
    recent reoccupation
    recent evaluated opportunity
    recent material turnover

V3 asks:

    Among frontier sites with comparable PRESENT local geometry, does RECENT
    local process history predict the causal leverage of one transient
    attachment intervention?

TARGET
------

As in Chapter 23 V4 and Chapter 24 V1/V2:

    FORCE x during canonical growth
        vs
    PREVENT x during the same growth update

Both branches receive canonical loss.

x receives one full causal update.

After lag 1:
    remove x from FORCE if still occupied.

Continue ordinary dynamics to:

    H = 12

Primary outcome:

    G_T(H)
        =
        cumulative FORCE - PREVENT realized attachments
        within hex distance 1..H
        over lags 1..H

d=0 is excluded.

RECENT PROCESS WINDOW
---------------------

Before the intervention checkpoint, retain the final:

    W = 6 completed updates

For every candidate x, within hex radius:

    R_history = 2

measure:

    recent_attachments
    recent_losses
    recent_reoccupations
    recent_first_occupations
    recent_evaluations

and define:

    RECENT MATERIAL TURNOVER
        T(x)
        =
        recent_attachments
        +
        recent_losses

This is the PRIMARY process-history variable.

Reoccupation and first occupation are reported to decompose attachment history,
but are not required for H1.

A reoccupation is an attachment to a site that had been occupied previously
and was empty immediately before that attachment.

A first occupation is an attachment to a site never previously occupied in the
tracked run.

PRESENT-STATE MATCHING
----------------------

High-turnover and low-turnover sites are paired within the SAME independent
checkpoint.

Every pair must satisfy:

    same canonical six-neighbour motif
    same occupied-neighbour count automatically follows from motif
    same radial bin, width 3
    baseline attachment probability difference <= 0.05
    current local frontier-density difference <= 0.10
    current Frontier Creation Potential difference <= 1

The pair must also satisfy:

    turnover difference >= 2 recent material events

Sites are used once per pair family.

Pairs are greedily ranked by:

    largest turnover contrast
    then smallest baseline-p difference
    then smallest frontier-density difference
    then smallest radial-distance difference

PRIMARY HYPOTHESIS
------------------

H1 — RECENT LOCAL TURNOVER PREDICTS TRANSIENT CAUSAL GAIN

For each matched pair:

    Delta_G
        =
        G_T(high-turnover)
        -
        G_T(low-turnover)

Within each independent group:
    average all pair differences to one group value.

Frozen success gates:

    mean Delta_G >= +0.15 attachments
    95% bootstrap CI lower bound > 0
    one-sided group-level sign-flip p < 0.05
    >= 70% of requested groups provide at least one usable pair

If successful, the bounded sentence is:

    Among Digital Crystal frontier sites with comparable present local
    geometry, sites embedded in regions with greater recent material turnover
    produced greater transient causal construction gain under the frozen
    intervention.

This would support LOCAL PROCESS HISTORY as relevant beyond present geometry.

It would NOT establish memory, learning, adaptation or a persistent causal
field.

SECONDARY VALIDITY / MECHANISM TESTS
------------------------------------

H2 — TURNOVER CONTRAST EXISTS

The matched high/low pairs must actually differ in recent material turnover.

Frozen gates:

    mean Delta_turnover >= +2.0 events
    CI lower bound > 0
    sign-flip p < 0.05

This is a design/construct validity gate.

H3 — CURRENT GEOMETRY REMAINS MATCHED

Report high-minus-low differences in:

    baseline p
    current frontier density
    FCP
    radial distance

No confirmatory zero-effect claim is made.

If H1 succeeds despite these remaining small under their frozen matching
tolerances, the result is evidence beyond the measured present-state controls.

PROCESS-HISTORY DECOMPOSITION
-----------------------------

Descriptively report high-minus-low differences in:

    recent attachments
    recent losses
    recent reoccupations
    recent first occupations
    recent evaluations

Also report descriptive Spearman relations between G_T and each component.

No post-hoc component is promoted to a new causal claim in V3.

AMPLIFICATION VS REDISTRIBUTION
-------------------------------

For each intervention report:

    local transient gain
    global transient gain
    far-field gain = global - local
    evaluated-set overlap with PREVENT

This continues the Chapter 24 observation that local gain can be accompanied
by opposite-signed far-field redistribution.

H1 uses LOCAL gain.

No net-global-amplification claim is made from H1.

NO CLASSIFIER
-------------

No random forest.
No neural network.
No automated feature selection.
No post-hoc threshold sweep.

The primary inference is the predeclared matched high-turnover versus
low-turnover intervention.

STOP RULE
---------

If H1 FAILS on a valid run:

    Do not rescue it by:
        changing history radius
        changing history window
        dropping motif matching
        selecting a different history component
        adding a classifier

Record the failure.

At that point Chapter 24 has tested:
    scalar present geometry
    exact present motif
    recent local process history

and should stop unless a genuinely new property is proposed.

FRESHNESS
---------

Default seed:
    20260908

Previous:
    Chapter 23 V1  20260902
    Chapter 23 V2  20260903
    Chapter 23 V3  20260904
    Chapter 23 V4  20260905
    Chapter 24 V1  20260906
    Chapter 24 V2  20260907

SCIENTIFIC BOUNDARY
-------------------

Success supports:
    recent local process history contributes information about transient
    causal gain beyond the measured present-state matching variables under this
    protocol.

It does NOT establish:
    memory
    learning
    adaptation
    causal-gain field
    coherent structure
    criticality
    percolation
    phase transition
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
EXPERIMENT_VERSION = "digital-crystal-local-process-history-v3"
SCHEMA_VERSION = 3
CHAPTER = 24
CHAPTER_TITLE = "Where Is Causal Gain Created?"
RUN_TITLE = "Does Recent Local Process History Determine Causal Gain?"


PROFILES = {
    "smoke": {
        "groups": 8,
        "radius": 54,
        "warmup_steps": 14,
        "lossy_pre_steps": 14,
        "history_window": 4,
        "history_radius": 2,
        "horizon": 6,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.08,
        "local_frontier_density_tolerance": 0.15,
        "fcp_tolerance": 1,
        "minimum_turnover_difference": 1,
        "minimum_gain_difference": 0.15,
        "minimum_turnover_contrast": 1.0,
        "minimum_group_coverage_fraction": 0.50,
        "max_pairs_per_group": 6,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "radius": 78,
        "warmup_steps": 20,
        "lossy_pre_steps": 20,
        "history_window": 6,
        "history_radius": 2,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "fcp_tolerance": 1,
        "minimum_turnover_difference": 2,
        "minimum_gain_difference": 0.15,
        "minimum_turnover_contrast": 2.0,
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
        "radius": 94,
        "warmup_steps": 24,
        "lossy_pre_steps": 24,
        "history_window": 6,
        "history_radius": 2,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "fcp_tolerance": 1,
        "minimum_turnover_difference": 2,
        "minimum_gain_difference": 0.15,
        "minimum_turnover_contrast": 2.0,
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
        "radius": 110,
        "warmup_steps": 24,
        "lossy_pre_steps": 28,
        "history_window": 6,
        "history_radius": 2,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 3,
        "probability_tolerance": 0.05,
        "local_frontier_density_tolerance": 0.10,
        "fcp_tolerance": 1,
        "minimum_turnover_difference": 2,
        "minimum_gain_difference": 0.15,
        "minimum_turnover_contrast": 2.0,
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

    after_loss, lost = ch21.apply_background_loss(
        grown,
        loss_rate,
    )

    return (
        after_loss,
        additions,
        lost,
        selected,
        frontier_count,
    )


# ============================================================================
# History recording
# ============================================================================

@dataclass
class EventFrame:
    attachments: Set[Cell]
    losses: Set[Cell]
    reoccupations: Set[Cell]
    first_occupations: Set[Cell]
    evaluated: Set[Cell]


@dataclass
class CheckpointBundle:
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray
    history_frames: List[EventFrame]
    max_capacity_fraction: float


def build_checkpoint_with_history(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group: int,
) -> CheckpointBundle:
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

    history_window = int(
        profile[
            "history_window"
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

    ever_occupied: Set[Cell] = set(
        state.occupied
    )

    frames: List[
        EventFrame
    ] = []

    max_capacity = float(
        ch18.capacity_fraction_occupied(
            state.occupied,
            radius,
        )
    )

    for j in range(
        pre_steps
    ):
        occupied_before = set(
            state.occupied
        )

        (
            next_state,
            additions,
            lost,
            evaluated,
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

        additions_set = set(
            additions
        )

        reoccupations = {
            cell
            for cell in additions_set
            if (
                cell in ever_occupied
                and cell not in occupied_before
            )
        }

        first_occupations = (
            additions_set
            - ever_occupied
        )

        ever_occupied.update(
            additions_set
        )

        frames.append(
            EventFrame(
                attachments=additions_set,
                losses=set(
                    lost
                ),
                reoccupations=set(
                    reoccupations
                ),
                first_occupations=set(
                    first_occupations
                ),
                evaluated=set(
                    evaluated
                ),
            )
        )

        if len(
            frames
        ) > history_window:
            frames = frames[
                -history_window:
            ]

        state = next_state

        max_capacity = max(
            max_capacity,
            float(
                ch18.capacity_fraction_occupied(
                    state.occupied,
                    radius,
                )
            ),
        )

    future_env = np.asarray(
        env[
            warmup + pre_steps:
            warmup + pre_steps + horizon + 1
        ],
        dtype=float,
    )

    return CheckpointBundle(
        checkpoint=state,
        future_env=future_env,
        history_frames=list(
            frames
        ),
        max_capacity_fraction=float(
            max_capacity
        ),
    )


# ============================================================================
# Present geometry
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


def canonical_binary_motif(
    bits: Sequence[int],
) -> str:
    seq = tuple(
        int(
            x
        )
        for x in bits
    )

    variants = []

    for shift in range(
        6
    ):
        rotated = (
            seq[
                shift:
            ]
            + seq[
                :shift
            ]
        )

        variants.append(
            rotated
        )

        variants.append(
            tuple(
                reversed(
                    rotated
                )
            )
        )

    return "".join(
        str(
            x
        )
        for x in min(
            variants
        )
    )


def cells_within_hex_radius(
    origin: Cell,
    radius: int,
) -> List[Cell]:
    oq, or_ = origin

    out = []

    for dq in range(
        -radius,
        radius + 1,
    ):
        for dr in range(
            -radius,
            radius + 1,
        ):
            cell = (
                oq + dq,
                or_ + dr,
            )

            if (
                relative_distance(
                    cell,
                    origin,
                )
                <= radius
            ):
                out.append(
                    cell
                )

    return out


@dataclass
class SiteState:
    cell: Cell
    motif: str
    occupied_neighbors: int
    baseline_p: float
    radial_distance: int
    radial_bin: int
    local_frontier_density_r2: float
    fcp: int
    promoted_frontier: int
    recent_attachments: int
    recent_losses: int
    recent_reoccupations: int
    recent_first_occupations: int
    recent_evaluations: int
    recent_turnover: int


def history_count(
    frames: Sequence[
        EventFrame
    ],
    origin: Cell,
    history_radius: int,
    getter,
) -> int:
    total = 0

    for frame in frames:
        cells = getter(
            frame
        )

        total += sum(
            relative_distance(
                cell,
                origin,
            )
            <= history_radius
            for cell in cells
        )

    return int(
        total
    )


def measure_site_state(
    checkpoint: ch18.MaterialCrystalState,
    frames: Sequence[
        EventFrame
    ],
    cell: Cell,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> SiteState:
    occupied = set(
        checkpoint.occupied
    )

    radius = int(
        profile[
            "radius"
        ]
    )

    history_radius = int(
        profile[
            "history_radius"
        ]
    )

    frontier_before = set(
        frontier_cells(
            occupied,
            radius,
        )
    )

    forced = set(
        occupied
    )
    forced.add(
        cell
    )

    frontier_after = set(
        frontier_cells(
            forced,
            radius,
        )
    )

    ring = list(
        ch18.neighbors(
            cell
        )
    )

    bits = tuple(
        1
        if nb in occupied
        else 0
        for nb in ring
    )

    promoted = [
        nb
        for nb in ring
        if (
            nb not in occupied
            and nb not in frontier_before
            and nb in frontier_after
        )
    ]

    neighborhood = cells_within_hex_radius(
        cell,
        2,
    )

    local_density = (
        sum(
            x in frontier_before
            for x in neighborhood
        )
        / len(
            neighborhood
        )
    )

    recent_attachments = history_count(
        frames,
        cell,
        history_radius,
        lambda f:
        f.attachments,
    )

    recent_losses = history_count(
        frames,
        cell,
        history_radius,
        lambda f:
        f.losses,
    )

    recent_reoccupations = history_count(
        frames,
        cell,
        history_radius,
        lambda f:
        f.reoccupations,
    )

    recent_first_occupations = history_count(
        frames,
        cell,
        history_radius,
        lambda f:
        f.first_occupations,
    )

    recent_evaluations = history_count(
        frames,
        cell,
        history_radius,
        lambda f:
        f.evaluated,
    )

    radial_distance = int(
        ch18.hex_distance(
            cell
        )
    )

    return SiteState(
        cell=cell,
        motif=canonical_binary_motif(
            bits
        ),
        occupied_neighbors=int(
            sum(
                bits
            )
        ),
        baseline_p=float(
            attachment_probability(
                cell,
                occupied,
                next_input,
                crystal_params,
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
        local_frontier_density_r2=float(
            local_density
        ),
        fcp=int(
            len(
                frontier_after
            )
            - len(
                frontier_before
            )
        ),
        promoted_frontier=int(
            len(
                promoted
            )
        ),
        recent_attachments=recent_attachments,
        recent_losses=recent_losses,
        recent_reoccupations=recent_reoccupations,
        recent_first_occupations=recent_first_occupations,
        recent_evaluations=recent_evaluations,
        recent_turnover=int(
            recent_attachments
            + recent_losses
        ),
    )


def evaluated_site_states(
    bundle: CheckpointBundle,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    SiteState
]:
    checkpoint = bundle.checkpoint

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
            <= radius
            - horizon
            - 2
        )
    ]

    return [
        measure_site_state(
            checkpoint,
            bundle.history_frames,
            cell,
            float(
                bundle.future_env[
                    0
                ]
            ),
            profile,
            crystal_params,
        )
        for cell in usable
    ]


# ============================================================================
# Present-state matched turnover pairs
# ============================================================================

@dataclass
class SitePair:
    high: SiteState
    low: SiteState


def compatible_present_state(
    high: SiteState,
    low: SiteState,
    profile: dict,
) -> bool:
    if (
        high.motif
        != low.motif
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

    if (
        abs(
            high.fcp
            - low.fcp
        )
        > int(
            profile[
                "fcp_tolerance"
            ]
        )
    ):
        return False

    if (
        high.recent_turnover
        - low.recent_turnover
        < int(
            profile[
                "minimum_turnover_difference"
            ]
        )
    ):
        return False

    return True


def construct_turnover_pairs(
    sites: Sequence[
        SiteState
    ],
    profile: dict,
) -> List[
    SitePair
]:
    candidates = []

    for i, a in enumerate(
        sites
    ):
        for j, b in enumerate(
            sites
        ):
            if i >= j:
                continue

            if (
                a.recent_turnover
                == b.recent_turnover
            ):
                continue

            high, low = (
                (a, b)
                if (
                    a.recent_turnover
                    > b.recent_turnover
                )
                else (b, a)
            )

            if not compatible_present_state(
                high,
                low,
                profile,
            ):
                continue

            candidates.append(
                (
                    -(
                        high.recent_turnover
                        - low.recent_turnover
                    ),
                    abs(
                        high.baseline_p
                        - low.baseline_p
                    ),
                    abs(
                        high.local_frontier_density_r2
                        - low.local_frontier_density_r2
                    ),
                    abs(
                        high.radial_distance
                        - low.radial_distance
                    ),
                    high.cell,
                    low.cell,
                    high,
                    low,
                )
            )

    candidates.sort(
        key=lambda x:
        x[
            :6
        ]
    )

    used: Set[
        Cell
    ] = set()

    pairs = []

    for item in candidates:
        high = item[
            6
        ]
        low = item[
            7
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
    state: SiteState
    g1: float
    G_local: float
    G_global: float
    far_field_gain: float
    mean_eval_overlap: float
    max_capacity_fraction: float


def set_overlap(
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


def run_transient(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    site: SiteState,
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

    x = site.cell

    (
        force_grown,
        _,
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
        _,
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
            "intervention-step evaluated sets diverged"
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    local_gain = 0.0
    global_gain = 0.0
    overlaps = []
    g1 = 0.0
    max_capacity = 0.0

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

        delta_local = float(
            force_local
            - prevent_local
        )

        delta_global = float(
            sum(
                cell != x
                for cell in force_add
            )
            - sum(
                cell != x
                for cell in prevent_add
            )
        )

        local_gain += delta_local
        global_gain += delta_global

        overlaps.append(
            set_overlap(
                force_eval,
                prevent_eval,
            )
        )

        if lag == 1:
            g1 = delta_local

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

    return InterventionResult(
        group=int(
            group
        ),
        pair_index=int(
            pair_index
        ),
        side=side,
        state=site,
        g1=float(
            g1
        ),
        G_local=float(
            local_gain
        ),
        G_global=float(
            global_gain
        ),
        far_field_gain=float(
            global_gain
            - local_gain
        ),
        mean_eval_overlap=float(
            np.mean(
                overlaps
            )
        ),
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
        boot[
            i
        ] = float(
            np.mean(
                rng.choice(
                    arr,
                    size=len(
                        arr
                    ),
                    replace=True,
                )
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
            / "ch24-local-process-history-v3-full-report.md"
        )

        parts = [
            "# Chapter 24 — Does Recent Local Process History Determine Causal Gain? (V3)",
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
            "RECENT LOCAL PROCESS HISTORY / TRANSIENT CAUSAL GAIN TEST"
        ),
        "fresh_seed": int(
            seed
        ),
        "history_window": int(
            profile[
                "history_window"
            ]
        ),
        "history_radius": int(
            profile[
                "history_radius"
            ]
        ),
        "primary_history_variable": (
            "recent_turnover = recent_attachments + recent_losses"
        ),
        "target": (
            "transient causal gain G_T(H)"
        ),
        "horizon": int(
            profile[
                "horizon"
            ]
        ),
        "present_state_matching": {
            "same_canonical_motif": True,
            "same_radial_bin_width": int(
                profile[
                    "radial_bin_width"
                ]
            ),
            "max_baseline_p_difference": float(
                profile[
                    "probability_tolerance"
                ]
            ),
            "max_local_frontier_density_difference": float(
                profile[
                    "local_frontier_density_tolerance"
                ]
            ),
            "max_FCP_difference": int(
                profile[
                    "fcp_tolerance"
                ]
            ),
        },
        "H1": {
            "quantity": (
                "G_T(high recent turnover) - G_T(low recent turnover), "
                "one mean per independent group"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_gain_difference"
                ]
            ),
            "alpha": float(
                profile[
                    "alpha"
                ]
            ),
            "minimum_group_coverage_fraction": float(
                profile[
                    "minimum_group_coverage_fraction"
                ]
            ),
        },
        "H2": {
            "quantity": (
                "recent_turnover(high) - recent_turnover(low)"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_turnover_contrast"
                ]
            ),
            "role": (
                "construct validity gate"
            ),
        },
        "stop_rule": (
            "If H1 fails on a valid run, do not tune history radius/window or "
            "select another history component from the same run."
        ),
        "classifier_used": False,
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
        "Stage 0 — Frozen Chapter 24 V3 Protocol",
        payload,
    )

    return payload


# ============================================================================
# Stage 1
# ============================================================================

@dataclass
class PairResult:
    high: InterventionResult
    low: InterventionResult


def stage_1_run(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[
        PairResult
    ],
    dict,
]:
    results: List[
        PairResult
    ] = []

    groups_with_pairs = 0
    pair_counts = []
    max_capacity = 0.0

    for group in tqdm(
        range(
            int(
                profile[
                    "groups"
                ]
            )
        ),
        desc="Chapter 24 V3 process-history groups",
    ):
        bundle = build_checkpoint_with_history(
            profile,
            crystal_params,
            seed,
            group,
        )

        max_capacity = max(
            max_capacity,
            bundle.max_capacity_fraction,
        )

        sites = evaluated_site_states(
            bundle,
            profile,
            crystal_params,
        )

        pairs = construct_turnover_pairs(
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
            high = run_transient(
                bundle.checkpoint,
                bundle.future_env,
                pair.high,
                profile,
                crystal_params,
                group,
                pair_index,
                "high_turnover",
            )

            low = run_transient(
                bundle.checkpoint,
                bundle.future_env,
                pair.low,
                profile,
                crystal_params,
                group,
                pair_index,
                "low_turnover",
            )

            max_capacity = max(
                max_capacity,
                high.max_capacity_fraction,
                low.max_capacity_fraction,
            )

            results.append(
                PairResult(
                    high=high,
                    low=low,
                )
            )

    coverage = (
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
            coverage
        ),
        "minimum_coverage_fraction": float(
            profile[
                "minimum_group_coverage_fraction"
            ]
        ),
        "coverage_gate_passed": bool(
            coverage
            >= profile[
                "minimum_group_coverage_fraction"
            ]
        ),
        "total_pairs": int(
            len(
                results
            )
        ),
        "mean_pairs_per_group_with_pairs": float(
            len(
                results
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
        "stage-01-history-matched-interventions.json",
        payload,
    )

    reporter.stage(
        "stage-01-history-matched-interventions.md",
        "Stage 1 — Present-State-Matched Process-History Interventions",
        payload,
    )

    return (
        results,
        payload,
    )


# ============================================================================
# Stage 2
# ============================================================================

def group_pair_means(
    results: Sequence[
        PairResult
    ],
    getter,
) -> List[float]:
    buckets: Dict[
        int,
        List[float],
    ] = {}

    for result in results:
        group = result.high.group

        buckets.setdefault(
            group,
            [],
        ).append(
            float(
                getter(
                    result.high,
                    result.low,
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
    results: Sequence[
        PairResult
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

    gain_delta = group_pair_means(
        results,
        lambda h, l:
        h.G_local
        - l.G_local,
    )

    turnover_delta = group_pair_means(
        results,
        lambda h, l:
        h.state.recent_turnover
        - l.state.recent_turnover,
    )

    component_getters = {
        "recent_attachments": (
            lambda h, l:
            h.state.recent_attachments
            - l.state.recent_attachments
        ),
        "recent_losses": (
            lambda h, l:
            h.state.recent_losses
            - l.state.recent_losses
        ),
        "recent_reoccupations": (
            lambda h, l:
            h.state.recent_reoccupations
            - l.state.recent_reoccupations
        ),
        "recent_first_occupations": (
            lambda h, l:
            h.state.recent_first_occupations
            - l.state.recent_first_occupations
        ),
        "recent_evaluations": (
            lambda h, l:
            h.state.recent_evaluations
            - l.state.recent_evaluations
        ),
    }

    matching_getters = {
        "baseline_probability": (
            lambda h, l:
            h.state.baseline_p
            - l.state.baseline_p
        ),
        "current_frontier_density": (
            lambda h, l:
            h.state.local_frontier_density_r2
            - l.state.local_frontier_density_r2
        ),
        "FCP": (
            lambda h, l:
            h.state.fcp
            - l.state.fcp
        ),
        "radial_distance": (
            lambda h, l:
            h.state.radial_distance
            - l.state.radial_distance
        ),
    }

    system_getters = {
        "global_gain": (
            lambda h, l:
            h.G_global
            - l.G_global
        ),
        "far_field_gain": (
            lambda h, l:
            h.far_field_gain
            - l.far_field_gain
        ),
        "eval_overlap": (
            lambda h, l:
            h.mean_eval_overlap
            - l.mean_eval_overlap
        ),
    }

    H1_summary = bootstrap_mean_ci(
        gain_delta,
        reps,
        seed + 201,
    )

    H1_test = signflip_greater(
        gain_delta,
        perms,
        seed + 202,
    )

    H2_summary = bootstrap_mean_ci(
        turnover_delta,
        reps,
        seed + 203,
    )

    H2_test = signflip_greater(
        turnover_delta,
        perms,
        seed + 204,
    )

    payload = {
        "H1_recent_turnover_predicts_transient_gain": {
            "group_gain_difference_high_minus_low": (
                H1_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_gain_difference"
                ]
            ),
            "signflip": H1_test,
        },
        "H2_turnover_construct_validity": {
            "group_turnover_difference_high_minus_low": (
                H2_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_turnover_contrast"
                ]
            ),
            "signflip": H2_test,
        },
        "history_component_differences": {
            name: bootstrap_mean_ci(
                group_pair_means(
                    results,
                    getter,
                ),
                reps,
                seed + 300 + index,
            )
            for index, (
                name,
                getter,
            ) in enumerate(
                component_getters.items()
            )
        },
        "present_state_matching_diagnostics": {
            name: bootstrap_mean_ci(
                group_pair_means(
                    results,
                    getter,
                ),
                reps,
                seed + 400 + index,
            )
            for index, (
                name,
                getter,
            ) in enumerate(
                matching_getters.items()
            )
        },
        "system_level_diagnostics": {
            name: bootstrap_mean_ci(
                group_pair_means(
                    results,
                    getter,
                ),
                reps,
                seed + 500 + index,
            )
            for index, (
                name,
                getter,
            ) in enumerate(
                system_getters.items()
            )
        },
    }

    reporter.json(
        "stage-02-primary-history-tests.json",
        payload,
    )

    reporter.stage(
        "stage-02-primary-history-tests.md",
        "Stage 2 — Primary Process-History Tests",
        payload,
    )

    return payload


# ============================================================================
# Stage 3 — descriptive history map
# ============================================================================

def stage_3_descriptive(
    reporter: Reporter,
    results: Sequence[
        PairResult
    ],
    image_dir: Path,
) -> dict:
    sites = []

    seen = set()

    for pair in results:
        for result in (
            pair.high,
            pair.low,
        ):
            key = (
                result.group,
                result.state.cell,
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            sites.append(
                result
            )

    gain = [
        result.G_local
        for result in sites
    ]

    fields = {
        "recent_turnover": [
            result.state.recent_turnover
            for result in sites
        ],
        "recent_attachments": [
            result.state.recent_attachments
            for result in sites
        ],
        "recent_losses": [
            result.state.recent_losses
            for result in sites
        ],
        "recent_reoccupations": [
            result.state.recent_reoccupations
            for result in sites
        ],
        "recent_first_occupations": [
            result.state.recent_first_occupations
            for result in sites
        ],
        "recent_evaluations": [
            result.state.recent_evaluations
            for result in sites
        ],
    }

    correlations = {
        name: spearman(
            values,
            gain,
        )
        for name, values in fields.items()
    }

    turnover_values = sorted(
        set(
            int(
                x
            )
            for x in fields[
                "recent_turnover"
            ]
        )
    )

    binned = []

    for value in turnover_values:
        subset = [
            result.G_local
            for result in sites
            if (
                result.state.recent_turnover
                == value
            )
        ]

        binned.append({
            "recent_turnover": int(
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
        "n_unique_intervention_sites": int(
            len(
                sites
            )
        ),
        "spearman_correlations_descriptive": (
            correlations
        ),
        "gain_by_recent_turnover": binned,
        "scope": (
            "Descriptive only. No history component is promoted to a new "
            "hypothesis from V3."
        ),
    }

    reporter.json(
        "stage-03-history-map.json",
        payload,
    )

    reporter.stage(
        "stage-03-history-map.md",
        "Stage 3 — Descriptive Local Process-History Map",
        payload,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(
            8,
            5,
        ),
    )

    ax.scatter(
        fields[
            "recent_turnover"
        ],
        gain,
        alpha=0.5,
    )

    ax.axhline(
        0.0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Recent local material turnover"
    )

    ax.set_ylabel(
        "Transient causal gain G_T(H)"
    )

    ax.set_title(
        "Chapter 24 V3: recent process history versus causal gain"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch24-v3-recent-turnover-vs-transient-gain.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    if binned:
        fig, ax = plt.subplots(
            figsize=(
                8,
                5,
            ),
        )

        ax.plot(
            [
                row[
                    "recent_turnover"
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
            "Recent local material turnover"
        )

        ax.set_ylabel(
            "Mean transient causal gain"
        )

        ax.set_title(
            "Chapter 24 V3: mean gain by recent turnover"
        )

        fig.tight_layout()

        fig.savefig(
            image_dir
            / "ch24-v3-mean-gain-by-recent-turnover.png",
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
        "H1_recent_turnover_predicts_transient_gain"
    ]

    H2 = stage2[
        "H2_turnover_construct_validity"
    ]

    H1_summary = H1[
        "group_gain_difference_high_minus_low"
    ]

    H2_summary = H2[
        "group_turnover_difference_high_minus_low"
    ]

    H2_supported = bool(
        valid
        and H2_summary[
            "mean"
        ]
        >= profile[
            "minimum_turnover_contrast"
        ]
        and H2_summary[
            "ci95_low"
        ]
        > 0.0
        and H2[
            "signflip"
        ][
            "p_value"
        ]
        < profile[
            "alpha"
        ]
    )

    H1_supported = bool(
        valid
        and H2_supported
        and H1_summary[
            "mean"
        ]
        >= profile[
            "minimum_gain_difference"
        ]
        and H1_summary[
            "ci95_low"
        ]
        > 0.0
        and H1[
            "signflip"
        ][
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

    elif not H2_supported:
        status = (
            "PROCESS_HISTORY_CONTRAST_INVALID"
        )
        bounded = (
            "V3 did not establish the frozen recent-turnover contrast required "
            "to interpret the high/low history comparison."
        )

    elif H1_supported:
        status = (
            "RECENT_PROCESS_HISTORY_PREDICTS_TRANSIENT_CAUSAL_GAIN"
        )
        bounded = (
            "Among evaluated frontier sites matched on present motif, baseline "
            "attachment probability, radial position, frontier density and "
            "Frontier Creation Potential, sites embedded in regions with "
            "greater recent material turnover produced greater transient "
            "causal construction gain."
        )

    else:
        status = (
            "RECENT_PROCESS_HISTORY_GAIN_LINK_FAILED"
        )
        bounded = (
            "The frozen V3 pairs differed strongly in recent local material "
            "turnover, but the experiment did not establish a scientifically "
            "meaningful corresponding increase in transient causal gain after "
            "matching present local geometry."
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
            "memory",
            "learning",
            "adaptation",
            "history is the only determinant of causal gain",
            "causal-gain field",
            "high-gain regions",
            "spatial clustering",
            "temporal persistence",
            "coherent structure",
            "criticality",
            "percolation",
            "natural boundary",
            "individuality",
            "autonomy",
            "organism",
            "life",
        ],
        "stop_rule_if_failed": (
            "Do not tune history radius/window or select a different history "
            "component from this run. Chapter 24 should close unless a "
            "qualitatively new causal property is proposed."
        ),
        "next_if_supported": (
            "Freshly confirm the process-history effect before mapping any "
            "history-derived high-gain regions through space-time."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        payload,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 24 V3 Verdict",
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
        default=20260908,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch24-local-process-history-v3"
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
        "chapter_title": (
            CHAPTER_TITLE
        ),
        "run_title": RUN_TITLE,
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "previous_seed": 20260907,
        "fresh_seed": bool(
            int(
                args.seed
            )
            != 20260907
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
        "CHAPTER 24 V3 — DOES RECENT LOCAL PROCESS HISTORY DETERMINE CAUSAL GAIN?"
    )

    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"W={profile['history_window']} "
        f"Rhist={profile['history_radius']} "
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
            "No usable present-state-matched process-history pairs."
        )

    s2 = stage_2_primary(
        reporter,
        profile,
        results,
        args.seed,
    )

    s3 = stage_3_descriptive(
        reporter,
        results,
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
