#!/usr/bin/env python3
"""
Digital Life — Chapter 24 V2
Do Local Frontier Motifs Determine Causal Gain?
================================================

CONTEXT
-------

Chapter 24 V1 tested a scalar observer:

    Frontier Creation Potential (FCP)

Matched high-FCP sites strongly differed in immediate frontier promotion, but
the frozen high-FCP -> higher transient causal-gain claim FAILED.

The descriptive map showed:
    - almost no monotonic rank relation between FCP and gain;
    - a suggestive high mean at FCP=+2;
    - exact baseline attachment probability matching;
    - residual local geometric heterogeneity.

The next candidate variable is therefore not "more frontier" as a scalar.
It is the exact local arrangement of occupied neighbours.

A frontier cell on a hex lattice has six neighbour positions. Its immediate
occupancy pattern is a six-bit ring:

    b0 b1 b2 b3 b4 b5

There are 64 raw binary patterns, and far fewer equivalence classes after
rotation and reflection.

V2 asks:

    Among sites matched on the usual scalar summaries, does changing the exact
    six-neighbour motif produce a larger difference in transient causal gain
    than changing sites within the same motif?

This is an omnibus motif test. It does NOT choose a "best motif" after looking
at the result.

MOTIF DEFINITION
----------------

For each evaluated frontier cell x:

    raw_pattern(x)
        = six occupied/unoccupied bits in ch18.neighbors(x) order

    canonical_motif(x)
        = lexicographically smallest bit string over all six rotations and
          their reflections

Thus rotational/reflection copies share one motif ID.

The center x itself is empty before intervention.

TRANSIENT INTERVENTION
----------------------

As in Chapter 23 V4 / Chapter 24 V1:

    FORCE x during canonical growth
        vs
    PREVENT x during the same growth update

Both branches receive the canonical loss step.

x is allowed one full causal update.

After lag 1:
    remove x from FORCE if it remains occupied.

Continue ordinary frozen dynamics to H=12.

Target:

    G_T(H)
        =
        cumulative FORCE - PREVENT realized attachments
        within hex distance 1..H
        over lags 1..H

The intervention site d=0 is excluded.

PAIR DESIGN
-----------

Every intervention site comes from the EXACT evaluated candidate set.

Sites are first measured once, then paired.

All pairs must satisfy:

    same occupied-neighbour count n
    same radial bin, width 3
    baseline attachment probability difference <= 0.05
    local frontier-density difference <= 0.10

Two pair families are constructed separately:

    CROSS-MOTIF PAIRS
        canonical motif differs

    SAME-MOTIF PAIRS
        canonical motif is identical

One-to-one matching is used within each pair family.
A site may appear in one cross-motif pair and one same-motif pair because the
two pair families estimate different contrasts, but never twice within the
same family.

Pairs are greedily chosen to minimize:
    baseline-p difference
    local-density difference
    radial-distance difference

PRIMARY HYPOTHESIS
------------------

H1 — EXACT MOTIF ARRANGEMENT MATTERS

For each pair:

    D_gain
        =
        abs(G_T(site A) - G_T(site B))

For each independent group:

    motif_contrast(group)
        =
        mean D_gain across CROSS-MOTIF pairs
        -
        mean D_gain across SAME-MOTIF pairs

Frozen gates:

    mean motif_contrast >= +0.20 attachments
    95% bootstrap CI lower bound > 0
    one-sided group-level sign-flip p < 0.05
    >= 70% of requested groups have at least one cross-motif AND one
       same-motif pair

If successful:

    Among frontier sites matched on occupied-neighbour count, baseline
    attachment probability, radial position and local frontier density, exact
    six-neighbour motif class predicts differences in transient causal gain.

This does NOT establish which motif is high-gain.

SECONDARY MECHANISTIC TEST
--------------------------

H2 — MOTIF DIFFERENCE CHANGES OPPORTUNITY TRANSFORMATION

For each pair:

    D_promoted
        =
        abs(promoted_frontier_A - promoted_frontier_B)

Compute the same cross-minus-same contrast.

Frozen gates:

    mean contrast >= +0.50 cells
    CI lower bound > 0
    sign-flip p < 0.05

If H2 passes but H1 fails:
    motif geometry changes immediate opportunity transformation but the gain
    consequence is not established.

If H1 passes but H2 fails:
    motif affects gain through something not captured by promoted-frontier
    count; do not retrofit a mechanism.

DESCRIPTIVE MOTIF TABLE
-----------------------

For every canonical motif with adequate representation report:

    count
    occupied-neighbour count
    mean baseline p
    mean FCP
    mean promoted frontier
    mean one-step g1
    mean transient G_T(H)
    mean global gain
    mean far-field gain

Bootstrap motif intervals use GROUP means, not raw site independence.

These are descriptive. No motif is promoted to a new hypothesis in V2.

N=2 STRUCTURAL SUBTYPES
-----------------------

As a transparent geometry diagnostic, classify n=2 motifs by circular
separation of the two occupied neighbours:

    adjacent        separation 1
    one-gap         separation 2
    opposite        separation 3

Report their descriptive outcomes.

No n=2 subtype receives a confirmatory directional claim in V2.

BUDGET REDISTRIBUTION
---------------------

Report local, global and far-field transient gain by motif.

Also record evaluated-set overlap with PREVENT.

This checks whether a motif changes where construction occurs rather than how
much occurs globally.

NO CLASSIFIER
-------------

No random forest.
No neural network.
No automated feature selection.
No post-hoc motif ranking claim.

The primary inference is the matched cross-motif versus same-motif contrast.

FRESHNESS
---------

Default seed:
    20260907

Previous:
    Chapter 23 V1  20260902
    Chapter 23 V2  20260903
    Chapter 23 V3  20260904
    Chapter 23 V4  20260905
    Chapter 24 V1  20260906

SCIENTIFIC BOUNDARY
-------------------

Success supports:
    exact local frontier arrangement contributes information about transient
    causal gain beyond the matched scalar summaries in this protocol.

It does NOT establish:
    a physical causal-gain field
    high-gain regions
    coherent structures
    spatial clustering
    temporal persistence
    criticality
    percolation
    phase transition
    natural boundary
    individuality
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
EXPERIMENT_VERSION = "digital-crystal-local-frontier-motifs-v2"
SCHEMA_VERSION = 2
CHAPTER = 24
CHAPTER_TITLE = "Where Is Causal Gain Created?"
RUN_TITLE = "Do Local Frontier Motifs Determine Causal Gain?"


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
        "max_sites_per_group": 24,
        "max_cross_pairs_per_group": 8,
        "max_same_pairs_per_group": 8,
        "minimum_motif_gain_contrast": 0.20,
        "minimum_motif_promoted_contrast": 0.50,
        "minimum_group_coverage_fraction": 0.50,
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
        "max_sites_per_group": 32,
        "max_cross_pairs_per_group": 10,
        "max_same_pairs_per_group": 10,
        "minimum_motif_gain_contrast": 0.20,
        "minimum_motif_promoted_contrast": 0.50,
        "minimum_group_coverage_fraction": 0.70,
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
        "max_sites_per_group": 40,
        "max_cross_pairs_per_group": 12,
        "max_same_pairs_per_group": 12,
        "minimum_motif_gain_contrast": 0.20,
        "minimum_motif_promoted_contrast": 0.50,
        "minimum_group_coverage_fraction": 0.70,
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
        "max_sites_per_group": 48,
        "max_cross_pairs_per_group": 16,
        "max_same_pairs_per_group": 16,
        "minimum_motif_gain_contrast": 0.20,
        "minimum_motif_promoted_contrast": 0.50,
        "minimum_group_coverage_fraction": 0.70,
        "bootstrap_reps": 7000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Frozen Digital Crystal
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
# Motifs and local geometry
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
    if len(
        bits
    ) != 6:
        raise ValueError(
            "hex motif requires six bits"
        )

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

    canonical = min(
        variants
    )

    return "".join(
        str(
            x
        )
        for x in canonical
    )


def raw_ring_bits(
    cell: Cell,
    occupied: Set[Cell],
) -> Tuple[int, ...]:
    return tuple(
        1
        if nb in occupied
        else 0
        for nb in ch18.neighbors(
            cell
        )
    )


def n2_separation(
    bits: Sequence[int],
) -> str | None:
    positions = [
        i
        for i, bit in enumerate(
            bits
        )
        if bit
    ]

    if len(
        positions
    ) != 2:
        return None

    a, b = positions

    raw = abs(
        a - b
    )

    separation = min(
        raw,
        6 - raw,
    )

    return {
        1: "adjacent",
        2: "one_gap",
        3: "opposite",
    }[
        separation
    ]


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
class SiteGeometry:
    cell: Cell
    raw_pattern: str
    motif: str
    n2_subtype: str | None
    occupied_neighbors: int
    baseline_p: float
    radial_distance: int
    radial_bin: int
    local_frontier_density_r2: float
    fcp: int
    promoted_frontier: int


def measure_site_geometry(
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

    bits = raw_ring_bits(
        cell,
        occupied,
    )

    ring_empty = [
        nb
        for nb in ch18.neighbors(
            cell
        )
        if nb not in occupied
    ]

    promoted = [
        nb
        for nb in ring_empty
        if (
            nb not in frontier_before
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

    radial_distance = int(
        ch18.hex_distance(
            cell
        )
    )

    return SiteGeometry(
        cell=cell,
        raw_pattern="".join(
            str(
                x
            )
            for x in bits
        ),
        motif=canonical_binary_motif(
            bits
        ),
        n2_subtype=n2_separation(
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
    )


def evaluated_geometries(
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

    selected = [
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

    geometries = [
        measure_site_geometry(
            checkpoint,
            cell,
            next_input,
            profile,
            crystal_params,
        )
        for cell in selected
    ]

    # Balanced deterministic sampling across motif classes.
    by_motif: Dict[
        str,
        List[SiteGeometry],
    ] = {}

    for geometry in geometries:
        by_motif.setdefault(
            geometry.motif,
            [],
        ).append(
            geometry
        )

    for motif in by_motif:
        by_motif[
            motif
        ].sort(
            key=lambda g: (
                g.baseline_p,
                g.radial_distance,
                g.cell,
            )
        )

    max_sites = int(
        profile[
            "max_sites_per_group"
        ]
    )

    chosen: List[
        SiteGeometry
    ] = []

    motif_order = sorted(
        by_motif
    )

    cursor = {
        motif: 0
        for motif in motif_order
    }

    while (
        len(
            chosen
        )
        < max_sites
    ):
        added = False

        for motif in motif_order:
            i = cursor[
                motif
            ]

            if i >= len(
                by_motif[
                    motif
                ]
            ):
                continue

            chosen.append(
                by_motif[
                    motif
                ][
                    i
                ]
            )

            cursor[
                motif
            ] += 1

            added = True

            if (
                len(
                    chosen
                )
                >= max_sites
            ):
                break

        if not added:
            break

    return chosen


# ============================================================================
# Transient intervention
# ============================================================================

@dataclass
class SiteResult:
    group: int
    geometry: SiteGeometry
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
    geometry: SiteGeometry,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    group: int,
) -> SiteResult:
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
            "intervention evaluated sets must match"
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

    return SiteResult(
        group=int(
            group
        ),
        geometry=geometry,
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
# Pairing
# ============================================================================

@dataclass
class ResultPair:
    a: SiteResult
    b: SiteResult


def scalar_compatible(
    a: SiteResult,
    b: SiteResult,
    profile: dict,
) -> bool:
    ga = a.geometry
    gb = b.geometry

    if (
        ga.occupied_neighbors
        != gb.occupied_neighbors
    ):
        return False

    if (
        ga.radial_bin
        != gb.radial_bin
    ):
        return False

    if (
        abs(
            ga.baseline_p
            - gb.baseline_p
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
            ga.local_frontier_density_r2
            - gb.local_frontier_density_r2
        )
        > float(
            profile[
                "local_frontier_density_tolerance"
            ]
        )
    ):
        return False

    return True


def build_pairs(
    results: Sequence[
        SiteResult
    ],
    profile: dict,
    same_motif: bool,
    limit: int,
) -> List[
    ResultPair
]:
    candidates = []

    for i, a in enumerate(
        results
    ):
        for j, b in enumerate(
            results
        ):
            if i >= j:
                continue

            if not scalar_compatible(
                a,
                b,
                profile,
            ):
                continue

            motif_same = (
                a.geometry.motif
                == b.geometry.motif
            )

            if motif_same != same_motif:
                continue

            score = (
                abs(
                    a.geometry.baseline_p
                    - b.geometry.baseline_p
                ),
                abs(
                    a.geometry.local_frontier_density_r2
                    - b.geometry.local_frontier_density_r2
                ),
                abs(
                    a.geometry.radial_distance
                    - b.geometry.radial_distance
                ),
                a.geometry.cell,
                b.geometry.cell,
            )

            candidates.append(
                (
                    score,
                    a,
                    b,
                )
            )

    candidates.sort(
        key=lambda x: x[
            0
        ]
    )

    used: Set[
        Cell
    ] = set()

    pairs = []

    for _, a, b in candidates:
        if (
            a.geometry.cell in used
            or b.geometry.cell in used
        ):
            continue

        used.add(
            a.geometry.cell
        )

        used.add(
            b.geometry.cell
        )

        pairs.append(
            ResultPair(
                a=a,
                b=b,
            )
        )

        if len(
            pairs
        ) >= limit:
            break

    return pairs


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
            / "ch24-local-frontier-motifs-v2-full-report.md"
        )

        parts = [
            "# Chapter 24 — Do Local Frontier Motifs Determine Causal Gain? (V2)",
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
            "EXACT LOCAL FRONTIER MOTIF / TRANSIENT CAUSAL GAIN TEST"
        ),
        "fresh_seed": int(
            seed
        ),
        "motif": (
            "six-neighbour occupancy pattern canonicalized under D6 "
            "rotation/reflection symmetry"
        ),
        "target": (
            "transient causal gain G_T(H)"
        ),
        "horizon": int(
            profile[
                "horizon"
            ]
        ),
        "pair_matching": {
            "same_occupied_neighbor_count": True,
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
        },
        "H1": {
            "statistic": (
                "mean abs gain difference cross-motif minus same-motif, "
                "one value per group"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_motif_gain_contrast"
                ]
            ),
            "coverage": float(
                profile[
                    "minimum_group_coverage_fraction"
                ]
            ),
        },
        "H2": {
            "statistic": (
                "mean abs promoted-frontier difference cross-motif minus "
                "same-motif"
            ),
            "minimum_effect": float(
                profile[
                    "minimum_motif_promoted_contrast"
                ]
            ),
        },
        "classifier_used": False,
        "motif_specific_outcomes": (
            "descriptive only in V2"
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
        "Stage 0 — Frozen Chapter 24 V2 Protocol",
        payload,
    )

    return payload


# ============================================================================
# Stage 1
# ============================================================================

@dataclass
class GroupData:
    group: int
    site_results: List[SiteResult]
    cross_pairs: List[ResultPair]
    same_pairs: List[ResultPair]


def stage_1_run(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[GroupData],
    dict,
]:
    groups: List[
        GroupData
    ] = []

    max_capacity = 0.0

    for group in tqdm(
        range(
            int(
                profile[
                    "groups"
                ]
            )
        ),
        desc="Chapter 24 V2 motif interventions",
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

        geometries = evaluated_geometries(
            checkpoint,
            float(
                future_env[
                    0
                ]
            ),
            profile,
            crystal_params,
        )

        site_results = [
            run_transient(
                checkpoint,
                future_env,
                geometry,
                profile,
                crystal_params,
                group,
            )
            for geometry in geometries
        ]

        for result in site_results:
            max_capacity = max(
                max_capacity,
                result.max_capacity_fraction,
            )

        cross_pairs = build_pairs(
            site_results,
            profile,
            same_motif=False,
            limit=int(
                profile[
                    "max_cross_pairs_per_group"
                ]
            ),
        )

        same_pairs = build_pairs(
            site_results,
            profile,
            same_motif=True,
            limit=int(
                profile[
                    "max_same_pairs_per_group"
                ]
            ),
        )

        groups.append(
            GroupData(
                group=group,
                site_results=site_results,
                cross_pairs=cross_pairs,
                same_pairs=same_pairs,
            )
        )

    groups_with_both = sum(
        bool(
            group.cross_pairs
            and group.same_pairs
        )
        for group in groups
    )

    coverage = (
        groups_with_both
        / max(
            1,
            int(
                profile[
                    "groups"
                ]
            ),
        )
    )

    motif_counts: Dict[
        str,
        int,
    ] = {}

    for group in groups:
        for result in group.site_results:
            motif_counts[
                result.geometry.motif
            ] = (
                motif_counts.get(
                    result.geometry.motif,
                    0,
                )
                + 1
            )

    payload = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "groups_with_cross_and_same_pairs": int(
            groups_with_both
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
        "total_sites": int(
            sum(
                len(
                    group.site_results
                )
                for group in groups
            )
        ),
        "total_cross_pairs": int(
            sum(
                len(
                    group.cross_pairs
                )
                for group in groups
            )
        ),
        "total_same_pairs": int(
            sum(
                len(
                    group.same_pairs
                )
                for group in groups
            )
        ),
        "motif_counts": motif_counts,
        "number_of_observed_canonical_motifs": int(
            len(
                motif_counts
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
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-motif-interventions.json",
        payload,
    )

    reporter.stage(
        "stage-01-motif-interventions.md",
        "Stage 1 — Exact Motif Interventions and Matched Pairs",
        payload,
    )

    return (
        groups,
        payload,
    )


# ============================================================================
# Stage 2 — primary contrasts
# ============================================================================

def pair_abs_gain(
    pair: ResultPair,
) -> float:
    return float(
        abs(
            pair.a.G_local
            - pair.b.G_local
        )
    )


def pair_abs_promoted(
    pair: ResultPair,
) -> float:
    return float(
        abs(
            pair.a.geometry.promoted_frontier
            - pair.b.geometry.promoted_frontier
        )
    )


def group_contrast(
    group: GroupData,
    getter,
) -> float:
    cross = [
        getter(
            pair
        )
        for pair in group.cross_pairs
    ]

    same = [
        getter(
            pair
        )
        for pair in group.same_pairs
    ]

    if (
        not cross
        or not same
    ):
        return float(
            "nan"
        )

    return float(
        np.mean(
            cross
        )
        - np.mean(
            same
        )
    )


def stage_2_primary(
    reporter: Reporter,
    profile: dict,
    groups: Sequence[
        GroupData
    ],
    seed: int,
) -> dict:
    gain_contrasts = [
        group_contrast(
            group,
            pair_abs_gain,
        )
        for group in groups
    ]

    promoted_contrasts = [
        group_contrast(
            group,
            pair_abs_promoted,
        )
        for group in groups
    ]

    gain_contrasts = [
        x
        for x in gain_contrasts
        if math.isfinite(
            x
        )
    ]

    promoted_contrasts = [
        x
        for x in promoted_contrasts
        if math.isfinite(
            x
        )
    ]

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

    H1_summary = bootstrap_mean_ci(
        gain_contrasts,
        reps,
        seed + 201,
    )

    H1_test = signflip_greater(
        gain_contrasts,
        perms,
        seed + 202,
    )

    H2_summary = bootstrap_mean_ci(
        promoted_contrasts,
        reps,
        seed + 203,
    )

    H2_test = signflip_greater(
        promoted_contrasts,
        perms,
        seed + 204,
    )

    payload = {
        "H1_exact_motif_gain_contrast": {
            "cross_minus_same_abs_gain_difference": (
                H1_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_motif_gain_contrast"
                ]
            ),
            "signflip": H1_test,
        },
        "H2_exact_motif_opportunity_contrast": {
            "cross_minus_same_abs_promoted_frontier_difference": (
                H2_summary
            ),
            "minimum_effect": float(
                profile[
                    "minimum_motif_promoted_contrast"
                ]
            ),
            "signflip": H2_test,
        },
    }

    reporter.json(
        "stage-02-primary-motif-tests.json",
        payload,
    )

    reporter.stage(
        "stage-02-primary-motif-tests.md",
        "Stage 2 — Primary Exact-Motif Tests",
        payload,
    )

    return payload


# ============================================================================
# Stage 3 — descriptive motif atlas
# ============================================================================

def motif_group_means(
    groups: Sequence[
        GroupData
    ],
    motif: str,
    getter,
) -> List[float]:
    values = []

    for group in groups:
        subset = [
            result
            for result in group.site_results
            if result.geometry.motif == motif
        ]

        if subset:
            values.append(
                float(
                    np.mean(
                        [
                            getter(
                                result
                            )
                            for result in subset
                        ]
                    )
                )
            )

    return values


def stage_3_atlas(
    reporter: Reporter,
    profile: dict,
    groups: Sequence[
        GroupData
    ],
    seed: int,
    image_dir: Path,
) -> dict:
    all_results = [
        result
        for group in groups
        for result in group.site_results
    ]

    motifs = sorted(
        set(
            result.geometry.motif
            for result in all_results
        )
    )

    reps = int(
        profile[
            "bootstrap_reps"
        ]
    )

    atlas = []

    for index, motif in enumerate(
        motifs
    ):
        subset = [
            result
            for result in all_results
            if result.geometry.motif == motif
        ]

        if not subset:
            continue

        n = subset[
            0
        ].geometry.occupied_neighbors

        atlas.append({
            "motif": motif,
            "occupied_neighbors": int(
                n
            ),
            "raw_site_count": int(
                len(
                    subset
                )
            ),
            "groups_represented": int(
                len(
                    set(
                        result.group
                        for result in subset
                    )
                )
            ),
            "baseline_p": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.geometry.baseline_p,
                ),
                reps,
                seed + 1000 + index * 20,
            ),
            "FCP": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.geometry.fcp,
                ),
                reps,
                seed + 1001 + index * 20,
            ),
            "promoted_frontier": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.geometry.promoted_frontier,
                ),
                reps,
                seed + 1002 + index * 20,
            ),
            "g1": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.g1,
                ),
                reps,
                seed + 1003 + index * 20,
            ),
            "G_transient_local": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.G_local,
                ),
                reps,
                seed + 1004 + index * 20,
            ),
            "G_transient_global": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.G_global,
                ),
                reps,
                seed + 1005 + index * 20,
            ),
            "far_field_gain": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.far_field_gain,
                ),
                reps,
                seed + 1006 + index * 20,
            ),
            "mean_eval_overlap": bootstrap_mean_ci(
                motif_group_means(
                    groups,
                    motif,
                    lambda r:
                    r.mean_eval_overlap,
                ),
                reps,
                seed + 1007 + index * 20,
            ),
        })

    n2 = {}

    for subtype in (
        "adjacent",
        "one_gap",
        "opposite",
    ):
        subset = [
            result
            for result in all_results
            if result.geometry.n2_subtype == subtype
        ]

        if subset:
            n2[
                subtype
            ] = {
                "raw_site_count": int(
                    len(
                        subset
                    )
                ),
                "mean_FCP": float(
                    np.mean(
                        [
                            result.geometry.fcp
                            for result in subset
                        ]
                    )
                ),
                "mean_promoted_frontier": float(
                    np.mean(
                        [
                            result.geometry.promoted_frontier
                            for result in subset
                        ]
                    )
                ),
                "mean_G_transient_local": float(
                    np.mean(
                        [
                            result.G_local
                            for result in subset
                        ]
                    )
                ),
            }

    payload = {
        "canonical_motif_atlas": atlas,
        "n2_subtypes_descriptive": n2,
        "scope": (
            "Motif-specific outcomes are descriptive in V2. No motif is "
            "promoted to a directional claim from this atlas."
        ),
    }

    reporter.json(
        "stage-03-motif-atlas.json",
        payload,
    )

    reporter.stage(
        "stage-03-motif-atlas.md",
        "Stage 3 — Descriptive Frontier-Motif Atlas",
        payload,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    eligible = [
        row
        for row in atlas
        if row[
            "groups_represented"
        ] >= 4
    ]

    if eligible:
        fig, ax = plt.subplots(
            figsize=(
                10,
                5,
            ),
        )

        labels = [
            row[
                "motif"
            ]
            for row in eligible
        ]

        means = [
            row[
                "G_transient_local"
            ][
                "mean"
            ]
            for row in eligible
        ]

        ax.bar(
            np.arange(
                len(
                    labels
                )
            ),
            means,
        )

        ax.axhline(
            0.0,
            linewidth=1,
        )

        ax.set_xticks(
            np.arange(
                len(
                    labels
                )
            )
        )

        ax.set_xticklabels(
            labels,
            rotation=45,
            ha="right",
        )

        ax.set_ylabel(
            "Mean transient causal gain"
        )

        ax.set_xlabel(
            "Canonical six-neighbour motif"
        )

        ax.set_title(
            "Chapter 24 V2: descriptive gain by local frontier motif"
        )

        fig.tight_layout()

        fig.savefig(
            image_dir
            / "ch24-v2-gain-by-frontier-motif.png",
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
        "H1_exact_motif_gain_contrast"
    ]

    H2 = stage2[
        "H2_exact_motif_opportunity_contrast"
    ]

    H1_summary = H1[
        "cross_minus_same_abs_gain_difference"
    ]

    H2_summary = H2[
        "cross_minus_same_abs_promoted_frontier_difference"
    ]

    H1_supported = bool(
        valid
        and H1_summary[
            "mean"
        ]
        >= profile[
            "minimum_motif_gain_contrast"
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

    H2_supported = bool(
        valid
        and H2_summary[
            "mean"
        ]
        >= profile[
            "minimum_motif_promoted_contrast"
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
            "Frozen motif-pair coverage or capacity validity gates failed."
        )

    elif (
        H1_supported
        and H2_supported
    ):
        status = (
            "LOCAL_FRONTIER_MOTIF_PREDICTS_TRANSIENT_CAUSAL_GAIN"
        )
        bounded = (
            "Among evaluated frontier sites matched on occupied-neighbour "
            "count, baseline attachment probability, radial position and local "
            "frontier density, cross-motif pairs differed more in transient "
            "causal gain than same-motif pairs. Exact motif differences also "
            "produced larger differences in immediate frontier promotion."
        )

    elif H2_supported:
        status = (
            "MOTIF_CHANGES_OPPORTUNITY_GAIN_LINK_FAILED"
        )
        bounded = (
            "Exact local frontier motif changed immediate opportunity "
            "transformation beyond matched scalar summaries, but V2 did not "
            "establish the frozen corresponding difference in transient causal "
            "gain."
        )

    else:
        status = (
            "LOCAL_MOTIF_HYPOTHESIS_FAILED"
        )
        bounded = (
            "V2 did not establish that exact six-neighbour motif contributes "
            "scientifically meaningful causal-gain or opportunity differences "
            "beyond the matched scalar summaries."
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
            "which motif is high-gain",
            "motif is the only determinant of gain",
            "causal-gain field",
            "high-gain regions",
            "spatial clustering",
            "temporal persistence",
            "coherent structure",
            "criticality",
            "percolation",
            "natural boundary",
            "individuality",
            "organism",
            "life",
        ],
        "next_if_supported": (
            "Freshly confirm specific predeclared motif contrasts before "
            "mapping motif-derived high-gain regions in space-time."
        ),
        "next_if_failed": (
            "Do not add a classifier. Treat immediate motif geometry as "
            "insufficient and move toward larger local state/history features "
            "only if they earn a qualitatively new hypothesis."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        payload,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 24 V2 Verdict",
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
        default=20260907,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch24-local-frontier-motifs-v2"
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
        "previous_seed": 20260906,
        "fresh_seed": bool(
            int(
                args.seed
            )
            != 20260906
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
        "CHAPTER 24 V2 — DO LOCAL FRONTIER MOTIFS DETERMINE CAUSAL GAIN?"
    )

    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"H={profile['horizon']} "
        f"sites/group<={profile['max_sites_per_group']} "
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

    groups, s1 = stage_1_run(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    s2 = stage_2_primary(
        reporter,
        profile,
        groups,
        args.seed,
    )

    s3 = stage_3_atlas(
        reporter,
        profile,
        groups,
        args.seed,
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
