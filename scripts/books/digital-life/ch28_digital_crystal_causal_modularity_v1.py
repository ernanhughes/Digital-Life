#!/usr/bin/env python3
"""
Digital Life — Chapter 28 V1
Does a Causal Individual Emerge?
================================

SCIENTIFIC QUESTION
-------------------

Does the Digital Crystal ever contain a spatial region whose INTERNAL causal
coupling is stronger than its EXTERNAL causal coupling by a predeclared margin?

This chapter deliberately does NOT define an individual from:
    - connected geometry
    - visual enclosure
    - density
    - circularity
    - persistence
    - lineage
    - material state
    - biological analogy

Instead it asks whether a candidate region behaves as a CAUSAL MODULE.

CORE IDEA
---------

For a candidate region R:

    INTERNAL COUPLING
        perturb inside R
        -> expected downstream consequence inside R

    OUTWARD COUPLING
        perturb inside R
        -> expected downstream consequence outside R

    INWARD COUPLING
        perturb just outside R
        -> expected downstream consequence inside R

A causal individual should satisfy:

    internal coupling
        >
    external coupling

by a predeclared meaningful margin.

CHAPTER 25 CONSTRAINT
---------------------

Finite global evaluation budgets create non-local coupling:

    local frontier change
    -> fixed global evaluation slots
    -> candidate substitution
    -> distant expected construction difference

Therefore a region can appear causally coupled to distant space even when
nearest-neighbour dynamics provide no direct local path.

Chapter 28 V1 removes that confound by using:

    TRUE UNBOUNDED EVALUATION

All current frontier candidates are evaluated.

Thus:
    selector-mediated far-field coupling = 0 by construction

This is a structural assertion, not a finding.

WHY UNBOUNDED FIRST
-------------------

The question is whether the crystal's LOCAL dynamics generate causal modularity.

If individuality cannot be detected when finite-budget redistribution is
removed, there is no reason to attribute modularity to the substrate itself.

A later experiment could ask whether bounded computation strengthens or weakens
an already-existing module.

CANDIDATE REGIONS
-----------------

V1 does NOT allow arbitrary region optimization.

That would create severe selection bias.

For each independent checkpoint we define candidate regions from the occupied
geometry BEFORE any causal outcomes are computed.

Candidate centers are occupied cells satisfying a local-density support rule.

Candidate regions are fixed-radius axial hex disks:

    R(center, radius)

Frozen region radii:

    REGION_RADII = [2, 3, 4, 5]

These are exploratory across scale.

The primary confirmatory scale is:

    PRIMARY_REGION_RADIUS = 4

The other radii are secondary scale diagnostics only.

WHY FIXED HEX DISKS
-------------------

They:
    - avoid visually choosing boundaries;
    - avoid connected-component cargo cult;
    - make inside/outside volumes explicit;
    - allow exact distance-matched controls;
    - do not assume an organism shape.

PROBE CLASSES
-------------

For each supported candidate region R:

1. INTERNAL PROBES
   Frontier cells x inside R.

2. EXTERNAL-SHELL PROBES
   Frontier cells x outside R but within one axial step of the region boundary.

All probes must have:
    occupied-neighbour count n = 1

This keeps local perturbation geometry comparable to Chapters 24–27.

For each region:
    choose up to K_INTERNAL internal probes
    choose up to K_EXTERNAL external-shell probes

Frozen:
    K_INTERNAL = 3
    K_EXTERNAL = 3

Selection is deterministic and outcome-blind.

PERTURBATION
------------

Use the corrected Chapter 27 semantics.

At t0:

    FORCE   = checkpoint + x occupied
    PREVENT = checkpoint with x empty

At lag 1:
    PREVENT explicitly blocks x from attachment
    FORCE contains x for exactly one growth exposure

After lag 1:
    remove x from FORCE
    ensure x absent in PREVENT

At lags 2..H:
    ordinary dynamics resume.

Frozen horizon:

    H = 8

WHY H = 8
---------

Chapter 28 is testing spatial causal retention, not long-run morphology.

A shorter horizon:
    - reduces stochastic accumulation;
    - keeps the causal cone interpretable;
    - limits boundary crossing opportunity;
    - is sufficient for multiple local propagation steps.

PRIMARY ESTIMATOR
-----------------

Use Rao-Blackwellized expected causal consequence.

At each lag:

    delta_p(y,t)
        =
        p_FORCE(y,t) - p_PREVENT(y,t)

For an INTERNAL perturbation x:

    I_in(x)
        =
        sum_t sum_{y in R} delta_p(y,t)

    I_out(x)
        =
        sum_t sum_{y outside R} delta_p(y,t)

For an EXTERNAL perturbation x:

    O_in(x)
        =
        sum_t sum_{y in R} delta_p(y,t)

    O_out(x)
        =
        sum_t sum_{y outside R} delta_p(y,t)

All sums exclude x itself.

We use ABSOLUTE causal mass for modularity:

    A_in(x)
        =
        sum_t sum_{y in R} |delta_p(y,t)|

    A_out(x)
        =
        sum_t sum_{y outside R} |delta_p(y,t)|

Signed effects are still recorded separately.

WHY ABSOLUTE CAUSAL MASS
------------------------

Internal positive and negative probability shifts can cancel.

A module is about where causal influence is expressed, not whether the net
signed attachment count happens to sum positive or negative.

PRIMARY MODULARITY SCORE
------------------------

For each region R:

    internal_retention
        =
        mean_internal_probe[
            A_in / (A_in + A_out)
        ]

    external_penetration
        =
        mean_external_probe[
            A_in / (A_in + A_out)
        ]

Then:

    MODULE_SCORE
        =
        internal_retention
        -
        external_penetration

Interpretation:

    internal_retention high
        -> perturbations originating inside preferentially express inside

    external_penetration low
        -> perturbations originating outside do not equivalently penetrate inside

A genuine causal module requires BOTH.

PRIMARY HYPOTHESIS H1
---------------------

At PRIMARY_REGION_RADIUS = 4:

    mean MODULE_SCORE > MODULE_SEI

Frozen:

    MODULE_SEI = 0.15

SUPPORTED:
    95% CI lower bound > 0.15
    achieved one-sided MDE80 <= 0.15

BOUNDED_BELOW_SEI:
    95% CI upper bound < 0.15
    achieved MDE80 <= 0.15

UNRESOLVED:
    otherwise

INVALID:
    validity gate fails

WHY 0.15
--------

A 15 percentage-point difference in causal retention between internally and
externally initiated perturbations is large enough to represent a meaningful
module rather than a tiny geometric asymmetry.

SECONDARY NECESSARY CONDITION
-----------------------------

A region is not treated as module-like if its internal perturbations simply
have high retention because the region occupies most of the local causal cone.

So report a GEOMETRIC NULL.

For every internal probe:
    construct a distance-preserving shuffled label null by rotating/translating
    an equal-area hex disk to matched radial context where possible.

Simpler V1 implementation:
    use matched control regions of the same radius centered on occupied cells
    with similar radial distance from crystal origin and similar occupancy
    fraction.

For each candidate region compute:

    EXCESS_MODULE_SCORE
        =
        observed MODULE_SCORE
        -
        matched-control MODULE_SCORE

This is SECONDARY in V1.

Do NOT promote it over H1.

REGION SUPPORT
--------------

Candidate region must satisfy, before outcomes:

    >= MIN_OCCUPIED_IN_REGION occupied cells
    >= MIN_INTERNAL_FRONTIER_PROBES supported internal probes
    >= MIN_EXTERNAL_FRONTIER_PROBES supported external probes
    occupancy fraction neither near-empty nor near-full

Frozen primary-radius support:

    MIN_OCCUPIED_IN_REGION = 12
    MIN_INTERNAL_FRONTIER_PROBES = 2
    MIN_EXTERNAL_FRONTIER_PROBES = 2

REGION SAMPLING
---------------

To avoid cherry-picking the "best" region:

For each independent group:
    enumerate all supported primary-radius candidate regions
    rank deterministically by:
        1. occupancy fraction closest to 0.50
        2. center radial distance
        3. axial coordinates

Select:

    REGIONS_PER_GROUP = 3

The chapter-level primary statistic averages regions within group first, then
uses independent groups for uncertainty.

No maximization over MODULE_SCORE is allowed.

VISIBLE BOUNDARY DIAGNOSTICS
----------------------------

For descriptive comparison only, record:

    occupancy fraction
    boundary occupied fraction
    internal frontier count
    external-shell frontier count
    center radius from origin

These are NOT used as evidence of individuality.

CAUSAL CONE ACCOUNTING
----------------------

All probability differences are evaluated over the full frontier under true
unbounded evaluation.

For reporting:
    inside R
    outside R but within H of probe
    far outside H

Under local nearest-neighbour dynamics and unbounded evaluation:

    expected far-outside-H effect should be exactly zero

Assert this numerically.

This is a correctness assertion.

COMMON RANDOM NUMBERS
---------------------

FORCE and PREVENT use the same:
    checkpoint
    future environment
    cell-keyed randomness

The only difference is the transient perturbation.

No dynamic construction-rate calibration is used in V1.

WHY NO CALIBRATION
------------------

Chapter 26 and Chapter 27 showed that global calibration itself can create
causal channels.

Chapter 28 is specifically measuring intrinsic causal modularity.

Therefore V1 does not normalize branch-wide construction rates.

If a region's perturbation changes overall construction, that is part of its
causal consequence.

VALIDITY GATE
-------------

Scientific validity requires:

    >= 90% independent-group coverage

    >= 2 supported primary-radius regions per covered group on average

    lag-1 intervention assertions pass for every probe

    far-outside-H expected effect <= 1e-12 under unbounded evaluation

    no outcome-dependent region selection

If invalid:
    INVALID

SECONDARY SCALE SWEEP
---------------------

Evaluate radii:
    2, 3, 4, 5

Report:
    internal retention
    external penetration
    module score

The scale sweep asks:

    does causal modularity peak at a finite spatial scale?

This is descriptive unless the primary radius-4 test passes.

A peak alone is NOT evidence of individuality.

INDIVIDUALITY CLAIM BOUNDARY
----------------------------

Even if H1 is SUPPORTED, Chapter 28 may claim only:

    "a causally modular region exists under this operational test"

It may NOT claim:
    organism
    self
    agent
    biological individual
    autonomy
    homeostasis
    reproduction
    metabolism
    life

A supported causal module would be a necessary ingredient for stronger
individuality claims, not a complete individual.

STOP RULE
---------

If primary radius-4 MODULE_SCORE is:

SUPPORTED:
    close V1 with bounded causal-modularity claim.
    Do not tune radius to improve effect.

BOUNDED_BELOW_SEI:
    causal modularity not established at this scale.
    scale sweep remains descriptive.

UNRESOLVED solely because MDE > SEI:
    increase independent groups only.

Do NOT rescue by changing:
    H
    region radius
    probe count
    module score
    SEI
    occupancy support
    absolute-vs-signed metric

PROFILES
--------

smoke:
    8 groups
    1 region/group
    up to 2+2 probes
    engineering only

quick:
    48 groups
    2 regions/group
    up to 3+3 probes

standard:
    96 groups
    3 regions/group
    up to 3+3 probes

full:
    192 groups
    3 regions/group
    up to 3+3 probes

FRESH SEED
----------

Default:

    20260916

OUTPUTS
-------

raw-v1-region-results.jsonl
raw-v1-region-results.csv
raw-v1-probe-results.jsonl
raw-v1-probe-results.csv
raw-v1-per-lag.jsonl
raw-v1-per-lag.csv

stage-00-protocol.*
stage-01-support.*
stage-02-validity.*
stage-03-primary.*
stage-04-scale-sweep.*
stage-05-controls.*
stage-06-verdict.*

full Markdown report

DEPENDENCIES
------------

Requires beside this file:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py
    ch27_digital_crystal_decaying_material_history_causal_response_v2.py

Chapter 27 V2 is reused for:
    corrected transient perturbation semantics
    unbounded growth helpers
    probe/checkpoint preparation
    statistical conventions
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21
import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4
import ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2 as ch26
import ch27_digital_crystal_decaying_material_history_causal_response_v2 as ch27


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-causal-modularity-v1"
SCHEMA_VERSION = 1
CHAPTER = 28
CHAPTER_TITLE = "Does a Causal Individual Emerge?"

HORIZON = 8

REGION_RADII = [
    2,
    3,
    4,
    5,
]

PRIMARY_REGION_RADIUS = 4

MODULE_SEI = 0.15

MIN_OCCUPIED_IN_REGION = 12
MIN_INTERNAL_FRONTIER_PROBES = 2
MIN_EXTERNAL_FRONTIER_PROBES = 2

REGIONS_PER_GROUP = 3
K_INTERNAL = 3
K_EXTERNAL = 3

MIN_GROUP_COVERAGE = 0.90
FAR_ASSERT_TOL = 1e-12

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

PROFILES = {
    "smoke": {
        "groups": 8,
        "source_profile": "smoke",
        "regions_per_group": 1,
        "k_internal": 2,
        "k_external": 2,
        "bootstrap_reps": 500,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "source_profile": "quick",
        "regions_per_group": 2,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 3000,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "source_profile": "standard",
        "regions_per_group": 3,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 5000,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "source_profile": "full",
        "regions_per_group": 3,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 7000,
        "scientific": True,
    },
}


# ============================================================================
# Statistics
# ============================================================================

def finite_array(
    values: Iterable[float],
) -> np.ndarray:
    return np.asarray(
        [
            float(v)
            for v in values
            if math.isfinite(
                float(v)
            )
        ],
        dtype=float,
    )


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = finite_array(
        values
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
        float(
            np.std(
                arr,
                ddof=1,
            )
        )
        if len(arr) > 1
        else 0.0
    )

    se = (
        sd
        / math.sqrt(
            len(arr)
        )
    )

    return {
        "n": int(
            len(arr)
        ),
        "mean": float(
            np.mean(
                arr
            )
        ),
        "sd": sd,
        "se": float(
            se
        ),
        "ci95_low": float(
            np.quantile(
                boot,
                0.025,
            )
        ),
        "ci95_high": float(
            np.quantile(
                boot,
                0.975,
            )
        ),
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
        > MODULE_SEI
    ):
        return "UNRESOLVED"

    low = float(
        summary[
            "ci95_low"
        ]
    )

    high = float(
        summary[
            "ci95_high"
        ]
    )

    if low > MODULE_SEI:
        return "SUPPORTED"

    if high < MODULE_SEI:
        return "BOUNDED_BELOW_SEI"

    return "UNRESOLVED"


# ============================================================================
# Hex geometry
# ============================================================================

def axial_distance(
    a: Cell,
    b: Cell,
) -> int:
    dq = (
        a[0]
        - b[0]
    )

    dr = (
        a[1]
        - b[1]
    )

    return int(
        max(
            abs(dq),
            abs(dr),
            abs(
                dq + dr
            ),
        )
    )


def hex_disk(
    center: Cell,
    radius: int,
) -> Set[Cell]:
    cq, cr = center

    cells = set()

    for dq in range(
        -radius,
        radius + 1,
    ):
        for dr in range(
            -radius,
            radius + 1,
        ):
            cell = (
                cq + dq,
                cr + dr,
            )

            if (
                axial_distance(
                    center,
                    cell,
                )
                <= radius
            ):
                cells.add(
                    cell
                )

    return cells


def shell(
    center: Cell,
    radius: int,
) -> Set[Cell]:
    return {
        cell
        for cell
        in hex_disk(
            center,
            radius,
        )
        if (
            axial_distance(
                center,
                cell,
            )
            == radius
        )
    }


# ============================================================================
# Checkpoint state
# ============================================================================

HistoryState = ch27.HistoryState
Probe = ch27.Probe


def state_from_checkpoint(
    checkpoint: ch18.MaterialCrystalState,
) -> HistoryState:
    # No material-state treatment in Chapter 28.
    state = ch27.from_checkpoint(
        checkpoint
    )

    state.material_strength = {}

    return state


def frontier_cells(
    state: HistoryState,
    radius: int,
) -> List[Cell]:
    return ch27.frontier_cells(
        state,
        radius,
    )


def attachment_probability(
    cell: Cell,
    state: HistoryState,
    input_value: float,
    crystal_params: ch18.CrystalParams,
) -> float:
    return ch27.attachment_probability(
        cell,
        state,
        input_value,
        crystal_params,
        0.0,
    )


# ============================================================================
# Candidate regions
# ============================================================================

@dataclass
class CandidateRegion:
    group: int
    region_index: int
    center: Cell
    radius: int

    cells: Set[Cell]

    occupied_count: int
    occupancy_fraction: float

    internal_frontier: Tuple[Cell, ...]
    external_frontier: Tuple[Cell, ...]

    center_radial_distance: int


def supported_frontier_n1(
    state: HistoryState,
    cells: Set[Cell],
    world_radius: int,
) -> List[Cell]:
    occupied = set(
        state.occupied
    )

    frontier = set(
        frontier_cells(
            state,
            world_radius,
        )
    )

    result = []

    for cell in sorted(
        frontier
        & cells
    ):
        n = sum(
            nb in occupied
            for nb
            in ch18.neighbors(
                cell
            )
        )

        if n == 1:
            result.append(
                cell
            )

    return result


def build_candidate_regions(
    group: int,
    checkpoint: ch18.MaterialCrystalState,
    region_radius: int,
    world_radius: int,
    regions_per_group: int,
    k_internal: int,
    k_external: int,
) -> List[CandidateRegion]:
    state = state_from_checkpoint(
        checkpoint
    )

    occupied = set(
        state.occupied
    )

    candidates = []

    for center in sorted(
        occupied
    ):
        cells = hex_disk(
            center,
            region_radius,
        )

        occupied_count = len(
            cells
            & occupied
        )

        occupancy_fraction = (
            occupied_count
            / max(
                1,
                len(
                    cells
                ),
            )
        )

        if (
            occupied_count
            < MIN_OCCUPIED_IN_REGION
        ):
            continue

        # Avoid trivial all-empty or nearly-full windows.
        if not (
            0.20
            <= occupancy_fraction
            <= 0.80
        ):
            continue

        internal = supported_frontier_n1(
            state,
            cells,
            world_radius,
        )

        external_shell_cells = (
            hex_disk(
                center,
                region_radius + 1,
            )
            - cells
        )

        external = supported_frontier_n1(
            state,
            external_shell_cells,
            world_radius,
        )

        if (
            len(
                internal
            )
            < MIN_INTERNAL_FRONTIER_PROBES
            or len(
                external
            )
            < MIN_EXTERNAL_FRONTIER_PROBES
        ):
            continue

        internal = tuple(
            internal[
                :k_internal
            ]
        )

        external = tuple(
            external[
                :k_external
            ]
        )

        candidates.append(
            CandidateRegion(
                group=int(
                    group
                ),
                region_index=-1,
                center=center,
                radius=int(
                    region_radius
                ),
                cells=cells,
                occupied_count=int(
                    occupied_count
                ),
                occupancy_fraction=float(
                    occupancy_fraction
                ),
                internal_frontier=internal,
                external_frontier=external,
                center_radial_distance=int(
                    axial_distance(
                        (
                            0,
                            0,
                        ),
                        center,
                    )
                ),
            )
        )

    candidates.sort(
        key=lambda region: (
            abs(
                region.occupancy_fraction
                - 0.50
            ),
            region.center_radial_distance,
            region.center,
        )
    )

    selected = candidates[
        :regions_per_group
    ]

    out = []

    for idx, region in enumerate(
        selected
    ):
        out.append(
            CandidateRegion(
                group=region.group,
                region_index=int(
                    idx
                ),
                center=region.center,
                radius=region.radius,
                cells=region.cells,
                occupied_count=region.occupied_count,
                occupancy_fraction=region.occupancy_fraction,
                internal_frontier=region.internal_frontier,
                external_frontier=region.external_frontier,
                center_radial_distance=region.center_radial_distance,
            )
        )

    return out


# ============================================================================
# Corrected transient perturbation
# ============================================================================

@dataclass
class Branches:
    force: HistoryState
    prevent: HistoryState


def make_branches(
    checkpoint: ch18.MaterialCrystalState,
    x: Cell,
) -> Branches:
    base = state_from_checkpoint(
        checkpoint
    )

    prevent = ch27.clone_state(
        base
    )

    if x in prevent.occupied:
        raise RuntimeError(
            "Probe x must be empty."
        )

    force = ch27.clone_state(
        base
    )

    force.occupied.add(
        x
    )

    force.birth_time[
        x
    ] = int(
        force.step
    )

    return Branches(
        force=force,
        prevent=prevent,
    )


def growth_step(
    state: HistoryState,
    input_value: float,
    world_radius: int,
    crystal_params: ch18.CrystalParams,
    blocked_cell: Cell | None,
):
    occupied = set(
        state.occupied
    )

    birth_time = dict(
        state.birth_time
    )

    frontier = frontier_cells(
        state,
        world_radius,
    )

    if blocked_cell is not None:
        frontier = [
            cell
            for cell
            in frontier
            if cell
            != blocked_cell
        ]

    next_step = int(
        state.step
        + 1
    )

    additions = []

    for cell in frontier:
        p = attachment_probability(
            cell,
            state,
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

    for cell in additions:
        occupied.add(
            cell
        )

        birth_time[
            cell
        ] = next_step

    out = HistoryState(
        occupied=occupied,
        birth_time=birth_time,
        material_strength={},
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
        material_mass_by_step=(
            list(
                state.material_mass_by_step
            )
            + [
                0.0
            ]
        ),
    )

    return (
        out,
        additions,
    )


def canonical_step(
    state: HistoryState,
    input_value: float,
    world_radius: int,
    crystal_params: ch18.CrystalParams,
    loss_rate: float,
    blocked_cell: Cell | None,
):
    grown, additions = growth_step(
        state,
        input_value,
        world_radius,
        crystal_params,
        blocked_cell,
    )

    after_loss, lost = (
        ch27.v1.apply_background_loss(
            grown,
            loss_rate,
        )
    )

    return (
        after_loss,
        additions,
        lost,
    )


# ============================================================================
# Expected causal mass
# ============================================================================

@dataclass
class ExpectedMass:
    signed_inside: float
    signed_outside_local: float
    signed_far: float

    absolute_inside: float
    absolute_outside_local: float
    absolute_far: float


def expected_mass(
    force: HistoryState,
    prevent: HistoryState,
    x: Cell,
    region_cells: Set[Cell],
    input_value: float,
    world_radius: int,
    crystal_params: ch18.CrystalParams,
    blocked_prevent_x: bool,
) -> ExpectedMass:
    ff = set(
        frontier_cells(
            force,
            world_radius,
        )
    )

    pf = set(
        frontier_cells(
            prevent,
            world_radius,
        )
    )

    if blocked_prevent_x:
        pf.discard(
            x
        )

    signed_inside = 0.0
    signed_outside_local = 0.0
    signed_far = 0.0

    abs_inside = 0.0
    abs_outside_local = 0.0
    abs_far = 0.0

    for cell in ff | pf:
        if cell == x:
            continue

        p_force = (
            attachment_probability(
                cell,
                force,
                input_value,
                crystal_params,
            )
            if cell
            in ff
            else 0.0
        )

        p_prevent = (
            attachment_probability(
                cell,
                prevent,
                input_value,
                crystal_params,
            )
            if cell
            in pf
            else 0.0
        )

        delta = (
            p_force
            - p_prevent
        )

        d_probe = axial_distance(
            cell,
            x,
        )

        if cell in region_cells:
            signed_inside += delta
            abs_inside += abs(
                delta
            )

        elif d_probe <= HORIZON:
            signed_outside_local += delta
            abs_outside_local += abs(
                delta
            )

        else:
            signed_far += delta
            abs_far += abs(
                delta
            )

    return ExpectedMass(
        signed_inside=float(
            signed_inside
        ),
        signed_outside_local=float(
            signed_outside_local
        ),
        signed_far=float(
            signed_far
        ),
        absolute_inside=float(
            abs_inside
        ),
        absolute_outside_local=float(
            abs_outside_local
        ),
        absolute_far=float(
            abs_far
        ),
    )


# ============================================================================
# Probe run
# ============================================================================

@dataclass
class ProbeResult:
    group: int
    region_index: int
    region_radius: int
    center_q: int
    center_r: int

    probe_class: str
    probe_q: int
    probe_r: int

    signed_inside: float
    signed_outside_local: float
    signed_far: float

    absolute_inside: float
    absolute_outside_local: float
    absolute_far: float

    inside_fraction: float
    total_local_absolute: float

    far_assertion_max: float


@dataclass
class PerLagRow:
    group: int
    region_index: int
    region_radius: int
    probe_class: str
    probe_q: int
    probe_r: int
    lag: int

    signed_inside: float
    signed_outside_local: float
    signed_far: float

    absolute_inside: float
    absolute_outside_local: float
    absolute_far: float


def run_probe(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    region: CandidateRegion,
    x: Cell,
    probe_class: str,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    ProbeResult,
    List[
        PerLagRow
    ],
]:
    branches = make_branches(
        checkpoint,
        x,
    )

    force = branches.force
    prevent = branches.prevent

    world_radius = int(
        source_profile[
            "radius"
        ]
    )

    loss_rate = float(
        source_profile[
            "loss_rate"
        ]
    )

    total_signed_inside = 0.0
    total_signed_outside = 0.0
    total_signed_far = 0.0

    total_abs_inside = 0.0
    total_abs_outside = 0.0
    total_abs_far = 0.0

    far_max = 0.0
    lag_rows = []

    for lag in range(
        1,
        HORIZON + 1,
    ):
        input_value = float(
            future_env[
                lag
            ]
        )

        mass = expected_mass(
            force,
            prevent,
            x,
            region.cells,
            input_value,
            world_radius,
            crystal_params,
            blocked_prevent_x=(
                lag == 1
            ),
        )

        total_signed_inside += (
            mass.signed_inside
        )

        total_signed_outside += (
            mass.signed_outside_local
        )

        total_signed_far += (
            mass.signed_far
        )

        total_abs_inside += (
            mass.absolute_inside
        )

        total_abs_outside += (
            mass.absolute_outside_local
        )

        total_abs_far += (
            mass.absolute_far
        )

        far_max = max(
            far_max,
            abs(
                mass.signed_far
            ),
            mass.absolute_far,
        )

        lag_rows.append(
            PerLagRow(
                group=region.group,
                region_index=region.region_index,
                region_radius=region.radius,
                probe_class=probe_class,
                probe_q=int(
                    x[0]
                ),
                probe_r=int(
                    x[1]
                ),
                lag=int(
                    lag
                ),
                signed_inside=mass.signed_inside,
                signed_outside_local=mass.signed_outside_local,
                signed_far=mass.signed_far,
                absolute_inside=mass.absolute_inside,
                absolute_outside_local=mass.absolute_outside_local,
                absolute_far=mass.absolute_far,
            )
        )

        (
            force,
            _force_add,
            _force_lost,
        ) = canonical_step(
            force,
            input_value,
            world_radius,
            crystal_params,
            loss_rate,
            blocked_cell=None,
        )

        (
            prevent,
            prevent_add,
            _prevent_lost,
        ) = canonical_step(
            prevent,
            input_value,
            world_radius,
            crystal_params,
            loss_rate,
            blocked_cell=(
                x
                if lag == 1
                else None
            ),
        )

        if (
            lag == 1
            and x
            in prevent_add
        ):
            raise RuntimeError(
                "PREVENT intervention failed."
            )

        if lag == 1:
            force.occupied.discard(
                x
            )

            force.birth_time.pop(
                x,
                None,
            )

            prevent.occupied.discard(
                x
            )

            prevent.birth_time.pop(
                x,
                None,
            )

            if (
                x in force.occupied
                or x
                in prevent.occupied
            ):
                raise RuntimeError(
                    "Intervention cleanup failed."
                )

    denom = (
        total_abs_inside
        + total_abs_outside
    )

    inside_fraction = (
        total_abs_inside
        / denom
        if denom > 0.0
        else float(
            "nan"
        )
    )

    return (
        ProbeResult(
            group=region.group,
            region_index=region.region_index,
            region_radius=region.radius,
            center_q=int(
                region.center[
                    0
                ]
            ),
            center_r=int(
                region.center[
                    1
                ]
            ),
            probe_class=probe_class,
            probe_q=int(
                x[0]
            ),
            probe_r=int(
                x[1]
            ),
            signed_inside=float(
                total_signed_inside
            ),
            signed_outside_local=float(
                total_signed_outside
            ),
            signed_far=float(
                total_signed_far
            ),
            absolute_inside=float(
                total_abs_inside
            ),
            absolute_outside_local=float(
                total_abs_outside
            ),
            absolute_far=float(
                total_abs_far
            ),
            inside_fraction=float(
                inside_fraction
            ),
            total_local_absolute=float(
                denom
            ),
            far_assertion_max=float(
                far_max
            ),
        ),
        lag_rows,
    )


# ============================================================================
# Region aggregation
# ============================================================================

@dataclass
class RegionResult:
    group: int
    region_index: int
    region_radius: int
    center_q: int
    center_r: int

    occupied_count: int
    occupancy_fraction: float
    internal_probe_count: int
    external_probe_count: int

    internal_retention: float
    external_penetration: float
    module_score: float

    mean_internal_absolute_mass: float
    mean_external_absolute_mass: float

    max_far_assertion: float


def aggregate_region(
    region: CandidateRegion,
    probes: Sequence[
        ProbeResult
    ],
) -> RegionResult:
    internal = [
        p
        for p in probes
        if (
            p.group
            == region.group
            and p.region_index
            == region.region_index
            and p.region_radius
            == region.radius
            and p.probe_class
            == "internal"
        )
    ]

    external = [
        p
        for p in probes
        if (
            p.group
            == region.group
            and p.region_index
            == region.region_index
            and p.region_radius
            == region.radius
            and p.probe_class
            == "external"
        )
    ]

    if (
        not internal
        or not external
    ):
        raise RuntimeError(
            "Region missing probe class."
        )

    internal_retention = float(
        np.mean(
            [
                p.inside_fraction
                for p in internal
            ]
        )
    )

    external_penetration = float(
        np.mean(
            [
                p.inside_fraction
                for p in external
            ]
        )
    )

    return RegionResult(
        group=region.group,
        region_index=region.region_index,
        region_radius=region.radius,
        center_q=int(
            region.center[
                0
            ]
        ),
        center_r=int(
            region.center[
                1
            ]
        ),
        occupied_count=region.occupied_count,
        occupancy_fraction=region.occupancy_fraction,
        internal_probe_count=len(
            internal
        ),
        external_probe_count=len(
            external
        ),
        internal_retention=internal_retention,
        external_penetration=external_penetration,
        module_score=float(
            internal_retention
            - external_penetration
        ),
        mean_internal_absolute_mass=float(
            np.mean(
                [
                    p.total_local_absolute
                    for p in internal
                ]
            )
        ),
        mean_external_absolute_mass=float(
            np.mean(
                [
                    p.total_local_absolute
                    for p in external
                ]
            )
        ),
        max_far_assertion=float(
            max(
                [
                    p.far_assertion_max
                    for p
                    in internal
                    + external
                ]
            )
        ),
    )


# ============================================================================
# Group aggregation
# ============================================================================

def group_metric(
    regions: Sequence[
        RegionResult
    ],
    radius: int,
    field: str,
) -> Dict[
    int,
    float,
]:
    buckets = defaultdict(
        list
    )

    for region in regions:
        if (
            region.region_radius
            != radius
        ):
            continue

        buckets[
            region.group
        ].append(
            float(
                getattr(
                    region,
                    field,
                )
            )
        )

    return {
        group: float(
            np.mean(
                vals
            )
        )
        for group, vals
        in buckets.items()
        if vals
    }


# ============================================================================
# Checkpoint preparation
# ============================================================================

@dataclass
class GroupCheckpoint:
    group: int
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray


def prepare_groups(
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> List[
    GroupCheckpoint
]:
    # Reuse Chapter 26/27 probe preparation only to obtain deterministic
    # independent checkpoints + future environments. Deduplicate by group.
    raw_probes, _support = (
        ch26.prepare_probes(
            profile,
            source_profile,
            crystal_params,
            seed,
        )
    )

    by_group = {}

    for p in raw_probes:
        if p.group not in by_group:
            by_group[
                int(
                    p.group
                )
            ] = GroupCheckpoint(
                group=int(
                    p.group
                ),
                checkpoint=p.checkpoint,
                future_env=p.future_env,
            )

    return [
        by_group[
            g
        ]
        for g
        in sorted(
            by_group
        )
    ]


# ============================================================================
# IO
# ============================================================================

def write_rows(
    jsonl_path: Path,
    csv_path: Path,
    rows,
) -> None:
    with jsonl_path.open(
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

    if not rows:
        return

    fields = list(
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
            fieldnames=fields,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                asdict(
                    row
                )
            )


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

    def save_json(
        self,
        filename: str,
        payload,
    ):
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
        payload,
    ):
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
        metadata,
    ) -> Path:
        path = (
            self.root
            / "ch28-causal-modularity-v1-full-report.md"
        )

        parts = [
            "# Chapter 28 — Does a Causal Individual Emerge? (V1)",
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
        default=20260916,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch28-causal-modularity-v1"
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
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "profile": args.profile,
        "seed": int(
            args.seed
        ),
        "fresh_seed": bool(
            args.seed
            not in {
                20260909,
                20260910,
                20260911,
                20260912,
                20260913,
                20260914,
                20260915,
            }
        ),
        "horizon": HORIZON,
        "region_radii": REGION_RADII,
        "primary_region_radius": PRIMARY_REGION_RADIUS,
        "module_SEI": MODULE_SEI,
        "allocation_policy": "true_unbounded",
        "started_at_unix": time.time(),
    }

    protocol = {
        "status": (
            "FROZEN"
            if profile[
                "scientific"
            ]
            else "ENGINEERING_SMOKE_ONLY"
        ),
        "question": (
            "Does a predeclared spatial region exhibit stronger internal "
            "causal retention than penetration from an equivalently local "
            "external perturbation?"
        ),
        "primary_radius": PRIMARY_REGION_RADIUS,
        "primary_metric": (
            "internal_retention - external_penetration"
        ),
        "module_SEI": MODULE_SEI,
        "causal_mass": (
            "sum absolute expected probability differences over H=8"
        ),
        "allocation": (
            "true_unbounded"
        ),
        "region_selection": (
            "outcome-blind fixed-radius disks; no module-score maximization"
        ),
        "forbidden_claims": [
            "organism",
            "self",
            "agent",
            "autonomy",
            "homeostasis",
            "life",
        ],
        "stop_rule": (
            "No radius or metric rescue. Increase groups only if unresolved "
            "solely because MDE exceeds SEI."
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 28 V1 Protocol",
        protocol,
    )

    reporter.save_json(
        "stage-00-protocol.json",
        protocol,
    )

    groups = prepare_groups(
        profile,
        source_profile,
        crystal_params,
        args.seed,
    )

    region_results = []
    probe_results = []
    per_lag_rows = []

    support_by_radius = {
        radius: {
            "groups_with_regions": 0,
            "regions": 0,
        }
        for radius
        in REGION_RADII
    }

    region_support_detail = []

    for group_record in tqdm(
        groups,
        desc="Chapter 28 groups",
    ):
        checkpoint = (
            group_record.checkpoint
        )

        future_env = (
            group_record.future_env
        )

        for radius in REGION_RADII:
            regions = (
                build_candidate_regions(
                    group_record.group,
                    checkpoint,
                    radius,
                    int(
                        source_profile[
                            "radius"
                        ]
                    ),
                    int(
                        profile[
                            "regions_per_group"
                        ]
                    ),
                    int(
                        profile[
                            "k_internal"
                        ]
                    ),
                    int(
                        profile[
                            "k_external"
                        ]
                    ),
                )
            )

            if regions:
                support_by_radius[
                    radius
                ][
                    "groups_with_regions"
                ] += 1

            support_by_radius[
                radius
            ][
                "regions"
            ] += len(
                regions
            )

            for region in regions:
                region_support_detail.append({
                    "group": region.group,
                    "region_index": region.region_index,
                    "region_radius": region.radius,
                    "center": list(
                        region.center
                    ),
                    "occupied_count": region.occupied_count,
                    "occupancy_fraction": region.occupancy_fraction,
                    "internal_frontier_count": len(
                        region.internal_frontier
                    ),
                    "external_frontier_count": len(
                        region.external_frontier
                    ),
                    "center_radial_distance": (
                        region.center_radial_distance
                    ),
                })

                local_probe_results = []

                for x in region.internal_frontier:
                    result, lag_rows = run_probe(
                        checkpoint,
                        future_env,
                        region,
                        x,
                        "internal",
                        source_profile,
                        crystal_params,
                    )

                    probe_results.append(
                        result
                    )

                    local_probe_results.append(
                        result
                    )

                    per_lag_rows.extend(
                        lag_rows
                    )

                for x in region.external_frontier:
                    result, lag_rows = run_probe(
                        checkpoint,
                        future_env,
                        region,
                        x,
                        "external",
                        source_profile,
                        crystal_params,
                    )

                    probe_results.append(
                        result
                    )

                    local_probe_results.append(
                        result
                    )

                    per_lag_rows.extend(
                        lag_rows
                    )

                region_results.append(
                    aggregate_region(
                        region,
                        local_probe_results,
                    )
                )

    write_rows(
        reporter.root
        / "raw-v1-region-results.jsonl",
        reporter.root
        / "raw-v1-region-results.csv",
        region_results,
    )

    write_rows(
        reporter.root
        / "raw-v1-probe-results.jsonl",
        reporter.root
        / "raw-v1-probe-results.csv",
        probe_results,
    )

    write_rows(
        reporter.root
        / "raw-v1-per-lag.jsonl",
        reporter.root
        / "raw-v1-per-lag.csv",
        per_lag_rows,
    )

    reporter.save_json(
        "region-support-detail.json",
        {
            "regions": (
                region_support_detail
            )
        },
    )

    total_requested_groups = int(
        profile[
            "groups"
        ]
    )

    support = {}

    for radius in REGION_RADII:
        info = support_by_radius[
            radius
        ]

        support[
            str(
                radius
            )
        ] = {
            "groups_with_regions": int(
                info[
                    "groups_with_regions"
                ]
            ),
            "coverage_fraction": float(
                info[
                    "groups_with_regions"
                ]
                / max(
                    1,
                    total_requested_groups,
                )
            ),
            "regions": int(
                info[
                    "regions"
                ]
            ),
            "mean_regions_per_requested_group": float(
                info[
                    "regions"
                ]
                / max(
                    1,
                    total_requested_groups,
                )
            ),
        }

    reporter.stage(
        "stage-01-support.md",
        "Stage 1 — Candidate Region Support",
        support,
    )

    reporter.save_json(
        "stage-01-support.json",
        support,
    )

    primary_regions = [
        r
        for r
        in region_results
        if (
            r.region_radius
            == PRIMARY_REGION_RADIUS
        )
    ]

    primary_group_map = group_metric(
        region_results,
        PRIMARY_REGION_RADIUS,
        "module_score",
    )

    coverage = float(
        len(
            primary_group_map
        )
        / max(
            1,
            total_requested_groups,
        )
    )

    far_max = (
        max(
            [
                r.max_far_assertion
                for r
                in primary_regions
            ]
        )
        if primary_regions
        else float(
            "inf"
        )
    )

    mean_regions_per_covered_group = (
        len(
            primary_regions
        )
        / max(
            1,
            len(
                primary_group_map
            ),
        )
    )

    validity = {
        "primary_radius": PRIMARY_REGION_RADIUS,
        "group_coverage_fraction": coverage,
        "required_group_coverage": MIN_GROUP_COVERAGE,
        "mean_regions_per_covered_group": float(
            mean_regions_per_covered_group
        ),
        "required_mean_regions_per_covered_group": 2.0,
        "far_expected_effect_max_abs": float(
            far_max
        ),
        "far_assertion_tolerance": FAR_ASSERT_TOL,
        "far_zero_assertion_pass": bool(
            far_max
            <= FAR_ASSERT_TOL
        ),
        "outcome_dependent_region_selection": False,
    }

    validity[
        "scientific_valid"
    ] = bool(
        coverage
        >= MIN_GROUP_COVERAGE
        and mean_regions_per_covered_group
        >= 2.0
        and far_max
        <= FAR_ASSERT_TOL
    )

    validity[
        "status"
    ] = (
        "PASS"
        if validity[
            "scientific_valid"
        ]
        else "FAIL"
    )

    reporter.stage(
        "stage-02-validity.md",
        "Stage 2 — Construct Validity",
        validity,
    )

    reporter.save_json(
        "stage-02-validity.json",
        validity,
    )

    primary_values = [
        value
        for _, value
        in sorted(
            primary_group_map.items()
        )
    ]

    primary_summary = (
        bootstrap_mean_ci(
            primary_values,
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed
            + 5000,
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
            validity[
                "scientific_valid"
            ],
        )

    internal_map = group_metric(
        region_results,
        PRIMARY_REGION_RADIUS,
        "internal_retention",
    )

    external_map = group_metric(
        region_results,
        PRIMARY_REGION_RADIUS,
        "external_penetration",
    )

    primary = {
        "primary_radius": PRIMARY_REGION_RADIUS,
        "module_score": primary_summary,
        "status": p_status,
        "internal_retention": bootstrap_mean_ci(
            [
                value
                for _, value
                in sorted(
                    internal_map.items()
                )
            ],
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed
            + 5001,
        ),
        "external_penetration": bootstrap_mean_ci(
            [
                value
                for _, value
                in sorted(
                    external_map.items()
                )
            ],
            int(
                profile[
                    "bootstrap_reps"
                ]
            ),
            args.seed
            + 5002,
        ),
        "SEI": MODULE_SEI,
    }

    reporter.stage(
        "stage-03-primary.md",
        "Stage 3 — Primary Causal Modularity Test",
        primary,
    )

    reporter.save_json(
        "stage-03-primary.json",
        primary,
    )

    scale_sweep = {}

    for idx, radius in enumerate(
        REGION_RADII
    ):
        payload = {}

        for j, field in enumerate(
            [
                "internal_retention",
                "external_penetration",
                "module_score",
            ]
        ):
            mapping = group_metric(
                region_results,
                radius,
                field,
            )

            payload[
                field
            ] = bootstrap_mean_ci(
                [
                    value
                    for _, value
                    in sorted(
                        mapping.items()
                    )
                ],
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6000
                + idx * 100
                + j,
            )

        scale_sweep[
            str(
                radius
            )
        ] = payload

    reporter.stage(
        "stage-04-scale-sweep.md",
        "Stage 4 — Descriptive Spatial Scale Sweep",
        scale_sweep,
    )

    reporter.save_json(
        "stage-04-scale-sweep.json",
        scale_sweep,
    )

    controls = {
        "far_zero": {
            "max_abs_expected_effect": float(
                far_max
            ),
            "status": (
                "PASS"
                if far_max
                <= FAR_ASSERT_TOL
                else "FAIL"
            ),
            "role": (
                "STRUCTURAL_ASSERTION_NOT_FINDING"
            ),
        },
        "region_geometry": {
            "selection_uses_module_score": False,
            "selection_uses_outcomes": False,
            "selection_basis": (
                "occupancy fraction closeness to 0.50, radial distance, "
                "axial coordinates"
            ),
        },
        "note": (
            "Matched-region geometric null is reserved as secondary follow-up "
            "if primary support and runtime justify it; V1 does not promote "
            "visual geometry into individuality evidence."
        ),
    }

    reporter.stage(
        "stage-05-controls.md",
        "Stage 5 — Structural Controls",
        controls,
    )

    reporter.save_json(
        "stage-05-controls.json",
        controls,
    )

    if not profile[
        "scientific"
    ]:
        overall = (
            "ENGINEERING_SMOKE_ONLY"
        )

        bounded = (
            "Engineering smoke profile only."
        )

    elif not validity[
        "scientific_valid"
    ]:
        overall = (
            "INVALID"
        )

        bounded = (
            "The candidate-region support or far-zero validity gate failed."
        )

    elif p_status == "SUPPORTED":
        overall = (
            "CAUSAL_MODULARITY_SUPPORTED"
        )

        bounded = (
            "At the frozen radius-4 scale, internally initiated perturbations "
            "were retained inside predeclared regions more strongly than "
            "equivalently local externally initiated perturbations penetrated "
            "those regions, by more than the frozen 0.15 module-score margin."
        )

    elif p_status == "BOUNDED_BELOW_SEI":
        overall = (
            "CAUSAL_MODULARITY_BOUNDED_BELOW_SEI"
        )

        bounded = (
            "At the frozen radius-4 scale, the mean causal-modularity score "
            "was bounded below the predeclared 0.15 meaningful margin."
        )

    else:
        overall = (
            "CAUSAL_MODULARITY_UNRESOLVED"
        )

        bounded = (
            "The experiment did not resolve whether radius-4 regions exceed "
            "the frozen 0.15 causal-modularity margin."
        )

    verdict = {
        "validity": validity,
        "primary_status": p_status,
        "overall_status": overall,
        "bounded_claim": bounded,
        "claim_boundary": {
            "supported_if_positive": (
                "causally modular spatial region under this operational test"
            ),
            "not_established": [
                "organism",
                "self",
                "agent",
                "autonomy",
                "homeostasis",
                "life",
            ],
        },
        "stop_rule": (
            "No radius or metric rescue. Increase independent groups only if "
            "UNRESOLVED solely because MDE exceeds SEI."
        ),
    }

    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Chapter 28 V1 Verdict",
        verdict,
    )

    reporter.save_json(
        "stage-06-verdict.json",
        verdict,
    )

    metadata[
        "finished_at_unix"
    ] = time.time()

    metadata[
        "final_status"
    ] = overall

    reporter.save_json(
        "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()
    print("=" * 78)
    print(
        f"FINAL STATUS: {overall}"
    )
    print(
        bounded
    )
    print(
        f"Report: {report}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
