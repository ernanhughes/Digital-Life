#!/usr/bin/env python3
"""
Digital Life — Chapter 24 V4
Frontier Creation, Divergence, and Causal Gain — Reset Experiment
=================================================================

WHY V4 EXISTS
-------------

Chapter 24 V1-V3 exposed several design problems:

1. V1 used a weak FCP contrast and was underpowered for its declared SEI.
2. FCP and promoted_frontier are algebraically redundant:
       FCP = promoted_frontier - 1
   for a frontier intervention. Promotion is therefore an invariant check,
   not independent scientific evidence.
3. Tight matching on baseline attachment probability can condition on a
   mediator of local geometry rather than merely remove confounding.
4. Realized attachment counts discard most of the information in the known
   stochastic rule. The exact conditional expectation is available.
5. G_T is zero-inflated. We need to separate:
       probability of divergence
       from
       consequence conditional on divergence.
6. Prior reports discarded absolute FORCE/PREVENT selection displacement.
7. "failed significance gate" is not the same as "effect ruled out".

V4 restarts the analysis around the known mechanism.

SCIENTIFIC QUESTION
-------------------

Does EXTREME frontier-creation geometry change the immediate expected causal
effect of one forced attachment, and how does that expected effect become a
realized branch divergence and finite transient cascade?

EXPOSURE
--------

For an evaluated frontier cell x:

    FCP(x)
        =
        |frontier after x is occupied|
        -
        |frontier before x is occupied|

For a frontier cell:

    FCP = promoted_frontier - 1

This identity is recorded as a hard invariant.

The scientific exposure is not "FCP independent of every other local
quantity". It is:

    EXTREME FRONTIER-CREATION GEOMETRY

Primary pair contrast:

    HIGH:
        FCP >= +2

    LOW:
        FCP <= -1

Thus:
        Delta FCP >= 3

Pairs must share:
    occupied-neighbour count
    radial bin

They are NOT matched on baseline p or local frontier density.

Those quantities are reported as possible mediators / accompanying state
differences rather than conditioned away.

NO AUTOMATIC FALLBACK
---------------------

If the extreme contrast lacks adequate support, the scientific run is INVALID.

The script never silently falls back from Delta FCP >= 3 to 2 or 1.

Use:
    --mode audit

to inspect support without running causal outcomes.

AUDIT MODE does not use outcome data and is safe for design-support checking.

TRANSIENT INTERVENTION
----------------------

Same canonical intervention family as Chapter 23 V4:

    FORCE x during the intervention growth update
        vs
    PREVENT x during the same update

Both branches receive ordinary background loss.

Then x is allowed one full causal update.

After lag 1:
    if x remains occupied in FORCE, remove it.

Continue ordinary frozen dynamics to H.

MEASUREMENT STACK
-----------------

A. MECHANICAL EXPECTED LAG-1 EFFECT

Before drawing lag-1 Bernoulli outcomes, calculate from the exact branch states
and exact branch-specific evaluated candidate sets:

    E1_local
        =
        sum p_force(candidate)
        -
        sum p_prevent(candidate)

within distance 1..H of x.

Also calculate E1_global.

This is the conditional expectation of realized lag-1 attachment difference
under the frozen stochastic rule.

B. EXPECTED LAG-1 DIVERGENCE

Under common cell-keyed uniforms, for a candidate selected in both branches:

    P(decision differs) = |p_force - p_prevent|

For a FORCE-only selected candidate:
    P(decision differs) = p_force

For a PREVENT-only selected candidate:
    P(decision differs) = p_prevent

Report:

    expected divergent attachment decisions
    model-implied probability of any lag-1 local divergence

The latter uses the product of per-cell non-divergence probabilities and is
descriptive of the frozen independent-keyed-uniform model.

C. REALIZED LAG-1 EFFECT

    g1_local
        =
        realized FORCE - PREVENT local attachment count at lag 1

D. ZERO-INFLATION / DIVERGENCE SPLIT

Report:

    P(any local lag-1 attachment-set divergence)

    P(G_T(H) != 0)

    E[G_T(H) | G_T(H) != 0]

Do not collapse these into a single mean without showing the decomposition.

E. FINITE-HORIZON TRANSIENT GAIN

    G_T(H)

remains a downstream realized outcome, but it is no longer the only or primary
measurement.

PRIMARY HYPOTHESIS
------------------

H1 — EXTREME FRONTIER-CREATION GEOMETRY CHANGES EXPECTED IMMEDIATE CAUSAL GAIN

For each matched HIGH/LOW pair:

    Delta_E1
        =
        E1_local(high)
        -
        E1_local(low)

One mean per independent group.

Frozen smallest effect of interest:

    SEI_E1 = +0.10 expected attachments

Support requires all:

    mean Delta_E1 >= +0.10
    95% bootstrap CI lower bound > 0
    one-sided group sign-flip p < 0.05
    achieved 80% one-sided MDE <= 0.10
    support coverage gate passes

If CI upper bound < +0.10 and achieved MDE <= 0.10:
    BOUNDED_BELOW_SEI

Otherwise:
    UNRESOLVED

This explicitly distinguishes absence-of-evidence from a bounded negative.

SECONDARY CONFIRMATORY OUTCOME
------------------------------

H2 — REALIZED LAG-1 CONSTRUCTION DIFFERENCE

    Delta_g1
        =
        g1_local(high)
        -
        g1_local(low)

Frozen SEI:
    +0.10 realized attachments

Same precision-aware three-way interpretation:
    SUPPORTED
    BOUNDED_BELOW_SEI
    UNRESOLVED

MECHANISTIC / DECOMPOSITION OUTCOMES
------------------------------------

H3:
    high-minus-low difference in model-implied P(any lag-1 local divergence)

Frozen SEI:
    +0.05 probability

H4:
    high-minus-low difference in realized finite-horizon G_T(H)

Frozen SEI:
    +0.15 attachments

H4 is downstream and expected to be noisier.

For all hypotheses:
    achieved MDE is reported.

ZERO-INFLATION
--------------

For HIGH and LOW sites separately report:

    lag1 divergence rate
    nonzero G_T rate
    mean G_T
    mean G_T conditional on nonzero

These are predeclared decompositions, not post-hoc rescue metrics.

FINITE-BUDGET DIAGNOSTICS
-------------------------

For every intervention and every lag report absolute:

    evaluated-set Jaccard overlap
    symmetric-difference count
    shared count
    force-only count
    prevent-only count

Also report:

    local gain
    global gain
    far-field gain = global - local

These are diagnostics here.

A dedicated budget-sweep / outside-causal-cone experiment belongs after V4.

POWER / PRECISION
-----------------

The independent unit is GROUP.

For every group-level outcome estimate:

    observed SD
    standard error
    achieved one-sided 80% MDE

with:

    MDE80 = SE * (z_0.95 + z_0.80)
          ~= SE * (1.644854 + 0.841621)

A directional test cannot be labelled FAILED merely because p >= .05.

Statuses:

    SUPPORTED
    BOUNDED_BELOW_SEI
    UNRESOLVED
    INVALID

DESIGN SUPPORT
--------------

The frozen scientific contrast is Delta FCP >= 3.

Coverage gate:

    at least 50% of requested groups
    must yield at least one extreme matched pair.

This 50% gate was frozen after an OUTCOME-BLIND 48-group design-support audit
showed 54.2% support for the exact FCP +2 versus -1 contrast. No causal outcome
from V4 was inspected before freezing this support criterion.

If not:
    INVALID_EXTREME_FCP_SUPPORT

No weaker contrast is substituted.

PROFILES
--------

quick:
    engineering/scientific preview, 48 groups

standard:
    96 groups

full:
    384 groups
    DEFAULT confirmatory profile

The larger full profile compensates for the roughly 50-55% expected support
rate of the strict Delta-FCP=3 contrast while leaving the final interpretation
subject to the achieved-MDE precision gate.

The full profile is the intended confirmatory run.

FRESH SEED
----------

Default:
    20260909

Previous Chapter 24 seeds:
    V1 20260906
    V2 20260907
    V3 20260908

SCIENTIFIC BOUNDARY
-------------------

Success supports only:

    extreme frontier-creation geometry changes the expected / realized local
    causal consequence of a one-cell transient intervention under the frozen
    Digital Crystal dynamics.

It does NOT establish:

    FCP is an independent causal variable
    causal-gain field
    stable high-gain region
    criticality
    percolation
    coherent structure
    individuality
    organism
    life

Requires beside this file:
    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-frontier-creation-causal-gain-v4-reset"
SCHEMA_VERSION = 4
CHAPTER = 24
CHAPTER_TITLE = "Where Is Causal Gain Created?"
RUN_TITLE = "Frontier Creation, Divergence, and Causal Gain — Reset Experiment"

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143


PROFILES = {
    "smoke": {
        "groups": 8,
        "radius": 54,
        "warmup_steps": 14,
        "lossy_pre_steps": 14,
        "horizon": 6,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 4,
        "high_fcp_min": 2,
        "low_fcp_max": -1,
        "minimum_fcp_difference": 3,
        "minimum_group_coverage_fraction": 0.25,
        "max_pairs_per_group": 4,
        "sei_E1": 0.10,
        "sei_g1": 0.10,
        "sei_divergence_probability": 0.05,
        "sei_GT": 0.15,
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
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 4,
        "high_fcp_min": 2,
        "low_fcp_max": -1,
        "minimum_fcp_difference": 3,
        "minimum_group_coverage_fraction": 0.50,
        "max_pairs_per_group": 6,
        "sei_E1": 0.10,
        "sei_g1": 0.10,
        "sei_divergence_probability": 0.05,
        "sei_GT": 0.15,
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
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 4,
        "high_fcp_min": 2,
        "low_fcp_max": -1,
        "minimum_fcp_difference": 3,
        "minimum_group_coverage_fraction": 0.50,
        "max_pairs_per_group": 8,
        "sei_E1": 0.10,
        "sei_g1": 0.10,
        "sei_divergence_probability": 0.05,
        "sei_GT": 0.15,
        "bootstrap_reps": 5000,
        "signflip_permutations": 12000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "full": {
        "groups": 384,
        "radius": 110,
        "warmup_steps": 24,
        "lossy_pre_steps": 28,
        "horizon": 12,
        "loss_rate": 0.08,
        "budget": 96,
        "radial_bin_width": 4,
        "high_fcp_min": 2,
        "low_fcp_max": -1,
        "minimum_fcp_difference": 3,
        "minimum_group_coverage_fraction": 0.50,
        "max_pairs_per_group": 10,
        "sei_E1": 0.10,
        "sei_g1": 0.10,
        "sei_divergence_probability": 0.05,
        "sei_GT": 0.15,
        "bootstrap_reps": 7000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Frozen crystal mechanics
# ============================================================================

def frontier_cells(occupied: Set[Cell], radius: int) -> List[Cell]:
    return ch21.frontier_cells(occupied, radius)


def attachment_probability(
    cell: Cell,
    occupied_before: Set[Cell],
    input_value: float,
    crystal_params: ch18.CrystalParams,
) -> float:
    n = sum(nb in occupied_before for nb in ch18.neighbors(cell))
    theta = ch18.local_exposure_angle(cell, occupied_before)
    phase = crystal_params.signal_phase_gain * float(input_value)
    anisotropy = math.cos(6.0 * theta + phase)
    crowding = max(0, n - 2)

    score = (
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain * float(input_value)
        + crystal_params.anisotropy_gain * anisotropy
        - crystal_params.crowding_penalty * crowding
    )

    return float(ch18.logistic_scalar(score))


def select_for_state(
    state: ch18.MaterialCrystalState,
    radius: int,
    budget: int,
) -> Tuple[List[Cell], List[Cell]]:
    frontier = frontier_cells(set(state.occupied), radius)
    selected = ch21.select_candidates(
        frontier,
        budget,
        state.stream_seed,
        int(state.step + 1),
    )
    return frontier, selected


def growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
    force_cell: Cell | None = None,
    prevent_cell: Cell | None = None,
) -> Tuple[ch18.MaterialCrystalState, List[Cell], List[Cell], int]:
    occupied_before = set(state.occupied)
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier = frontier_cells(occupied_before, radius)
    next_step = int(state.step + 1)

    selected = ch21.select_candidates(
        frontier,
        budget,
        state.stream_seed,
        next_step,
    )
    selected_set = set(selected)

    if force_cell is not None and force_cell not in selected_set:
        raise RuntimeError("force cell is not in exact intervention evaluated set")

    if prevent_cell is not None and prevent_cell not in selected_set:
        raise RuntimeError("prevent cell is not in exact intervention evaluated set")

    additions: List[Cell] = []

    for cell in selected:
        if force_cell is not None and cell == force_cell:
            additions.append(cell)
            continue

        if prevent_cell is not None and cell == prevent_cell:
            continue

        p = attachment_probability(
            cell,
            occupied_before,
            input_value,
            crystal_params,
        )

        if ch18.cell_uniform(state.stream_seed, next_step, cell) < p:
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
        attachments_by_step=list(state.attachments_by_step) + [len(additions)],
        population_by_step=list(state.population_by_step) + [len(occupied)],
        modified_count_by_step=list(state.modified_count_by_step) + [0],
    )

    return out, additions, selected, len(frontier)


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
    grown, additions, selected, frontier_count = growth_step(
        state,
        input_value,
        radius,
        crystal_params,
        budget,
    )

    after_loss, lost = ch21.apply_background_loss(grown, loss_rate)

    return after_loss, additions, lost, selected, frontier_count


# ============================================================================
# Checkpoint construction
# ============================================================================

def build_checkpoint(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group: int,
) -> Tuple[ch18.MaterialCrystalState, np.ndarray, float]:
    radius = int(profile["radius"])
    warmup = int(profile["warmup_steps"])
    pre_steps = int(profile["lossy_pre_steps"])
    horizon = int(profile["horizon"])

    gseed = int(seed) + group * 1009

    env = ch18.make_environment(
        warmup + pre_steps + horizon + 8,
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
        ch18.capacity_fraction_occupied(state.occupied, radius)
    )

    for j in range(pre_steps):
        state, _, _, _, _ = canonical_step(
            state,
            float(env[warmup + j]),
            radius,
            crystal_params,
            int(profile["budget"]),
            float(profile["loss_rate"]),
        )

        max_capacity = max(
            max_capacity,
            float(ch18.capacity_fraction_occupied(state.occupied, radius)),
        )

    future_env = np.asarray(
        env[
            warmup + pre_steps:
            warmup + pre_steps + horizon + 1
        ],
        dtype=float,
    )

    return state, future_env, max_capacity


# ============================================================================
# Geometry
# ============================================================================

def relative_distance(cell: Cell, origin: Cell) -> int:
    return int(
        ch18.hex_distance(
            (cell[0] - origin[0], cell[1] - origin[1])
        )
    )


def cells_within_hex_radius(origin: Cell, radius: int) -> List[Cell]:
    oq, or_ = origin
    out: List[Cell] = []

    for dq in range(-radius, radius + 1):
        for dr in range(-radius, radius + 1):
            cell = (oq + dq, or_ + dr)
            if relative_distance(cell, origin) <= radius:
                out.append(cell)

    return out


@dataclass
class SiteGeometry:
    cell: Cell
    baseline_p: float
    occupied_neighbors: int
    radial_distance: int
    radial_bin: int
    local_frontier_density_r2: float
    frontier_before_count: int
    frontier_after_count: int
    promoted_frontier: int
    fcp: int


def measure_geometry(
    checkpoint: ch18.MaterialCrystalState,
    cell: Cell,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    frontier_before: Set[Cell],
) -> SiteGeometry:
    """
    Exact O(local-neighbourhood) FCP calculation.

    For a frontier intervention x:
        x leaves frontier when forced occupied         -1
        each newly eligible ring-1 empty cell          +1

    Therefore:
        FCP = promoted_frontier - 1

    We no longer recompute the entire frontier after every hypothetical force.
    The identity is exact for this local frontier definition.
    """
    occupied = set(checkpoint.occupied)

    ring = list(ch18.neighbors(cell))

    promoted = [
        nb
        for nb in ring
        if (
            nb not in occupied
            and nb not in frontier_before
            and ch18.hex_distance(nb) <= int(profile["radius"])
        )
    ]

    neighborhood = cells_within_hex_radius(cell, 2)

    local_density = (
        sum(x in frontier_before for x in neighborhood)
        / len(neighborhood)
    )

    promoted_count = int(len(promoted))
    fcp = int(promoted_count - 1)

    radial_distance = int(ch18.hex_distance(cell))

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
        occupied_neighbors=int(sum(nb in occupied for nb in ring)),
        radial_distance=radial_distance,
        radial_bin=int(
            radial_distance // int(profile["radial_bin_width"])
        ),
        local_frontier_density_r2=float(local_density),
        frontier_before_count=int(len(frontier_before)),
        frontier_after_count=int(len(frontier_before) + fcp),
        promoted_frontier=promoted_count,
        fcp=fcp,
    )

def evaluated_geometries(
    checkpoint: ch18.MaterialCrystalState,
    next_input: float,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[SiteGeometry]:
    radius = int(profile["radius"])
    horizon = int(profile["horizon"])

    frontier = frontier_cells(checkpoint.occupied, radius)
    frontier_set = set(frontier)

    selected = ch21.select_candidates(
        frontier,
        int(profile["budget"]),
        checkpoint.stream_seed,
        int(checkpoint.step + 1),
    )

    usable = [
        cell
        for cell in selected
        if ch18.hex_distance(cell) <= radius - horizon - 2
    ]

    return [
        measure_geometry(
            checkpoint,
            cell,
            next_input,
            profile,
            crystal_params,
            frontier_set,
        )
        for cell in usable
    ]


# ============================================================================
# Extreme support and pairing
# ============================================================================

@dataclass
class SitePair:
    high: SiteGeometry
    low: SiteGeometry


def extreme_pair_compatible(
    high: SiteGeometry,
    low: SiteGeometry,
    profile: dict,
) -> bool:
    if high.fcp < int(profile["high_fcp_min"]):
        return False

    if low.fcp > int(profile["low_fcp_max"]):
        return False

    if high.fcp - low.fcp < int(profile["minimum_fcp_difference"]):
        return False

    if high.occupied_neighbors != low.occupied_neighbors:
        return False

    if high.radial_bin != low.radial_bin:
        return False

    return True


def construct_extreme_pairs(
    sites: Sequence[SiteGeometry],
    profile: dict,
) -> List[SitePair]:
    candidates = []

    highs = [
        site
        for site in sites
        if site.fcp >= int(profile["high_fcp_min"])
    ]

    lows = [
        site
        for site in sites
        if site.fcp <= int(profile["low_fcp_max"])
    ]

    for high in highs:
        for low in lows:
            if not extreme_pair_compatible(high, low, profile):
                continue

            # Do NOT rank on baseline p or density.
            # Those are potential mediators/accompanying state.
            candidates.append(
                (
                    -(high.fcp - low.fcp),
                    abs(high.radial_distance - low.radial_distance),
                    high.cell,
                    low.cell,
                    high,
                    low,
                )
            )

    candidates.sort(key=lambda x: x[:4])

    used: Set[Cell] = set()
    pairs: List[SitePair] = []

    for item in candidates:
        high = item[4]
        low = item[5]

        if high.cell in used or low.cell in used:
            continue

        used.add(high.cell)
        used.add(low.cell)

        pairs.append(SitePair(high=high, low=low))

        if len(pairs) >= int(profile["max_pairs_per_group"]):
            break

    return pairs


# ============================================================================
# Exact lag-1 expectation and divergence
# ============================================================================

@dataclass
class Lag1Expectation:
    E1_local: float
    E1_global: float
    expected_divergent_decisions_local: float
    expected_divergent_decisions_global: float
    prob_any_divergence_local: float
    prob_any_divergence_global: float
    selected_jaccard: float
    selected_symdiff_count: int
    selected_shared_count: int
    selected_force_only_count: int
    selected_prevent_only_count: int


def selected_set_stats(
    force_selected: Sequence[Cell],
    prevent_selected: Sequence[Cell],
) -> dict:
    sf = set(force_selected)
    sp = set(prevent_selected)

    union = sf | sp
    inter = sf & sp

    jaccard = 1.0 if not union else len(inter) / len(union)

    return {
        "jaccard": float(jaccard),
        "symdiff": int(len(sf ^ sp)),
        "shared": int(len(inter)),
        "force_only": int(len(sf - sp)),
        "prevent_only": int(len(sp - sf)),
    }


def exact_lag1_expectation(
    force_state: ch18.MaterialCrystalState,
    prevent_state: ch18.MaterialCrystalState,
    next_input: float,
    origin: Cell,
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Lag1Expectation:
    radius = int(profile["radius"])
    budget = int(profile["budget"])
    horizon = int(profile["horizon"])

    _, force_selected = select_for_state(
        force_state,
        radius,
        budget,
    )

    _, prevent_selected = select_for_state(
        prevent_state,
        radius,
        budget,
    )

    sf = set(force_selected)
    sp = set(prevent_selected)
    union = sf | sp

    stats = selected_set_stats(force_selected, prevent_selected)

    force_occ = set(force_state.occupied)
    prevent_occ = set(prevent_state.occupied)

    E_local = 0.0
    E_global = 0.0

    q_local = []
    q_global = []

    for cell in union:
        if cell == origin:
            continue

        pf = (
            attachment_probability(
                cell,
                force_occ,
                next_input,
                crystal_params,
            )
            if cell in sf
            else 0.0
        )

        pp = (
            attachment_probability(
                cell,
                prevent_occ,
                next_input,
                crystal_params,
            )
            if cell in sp
            else 0.0
        )

        delta = pf - pp
        E_global += delta

        if 1 <= relative_distance(cell, origin) <= horizon:
            E_local += delta

        if cell in sf and cell in sp:
            q = abs(pf - pp)
        elif cell in sf:
            q = pf
        else:
            q = pp

        q = min(1.0, max(0.0, float(q)))

        q_global.append(q)

        if 1 <= relative_distance(cell, origin) <= horizon:
            q_local.append(q)

    expected_div_global = float(np.sum(q_global))
    expected_div_local = float(np.sum(q_local))

    prob_none_global = float(
        np.prod([1.0 - q for q in q_global])
    ) if q_global else 1.0

    prob_none_local = float(
        np.prod([1.0 - q for q in q_local])
    ) if q_local else 1.0

    return Lag1Expectation(
        E1_local=float(E_local),
        E1_global=float(E_global),
        expected_divergent_decisions_local=expected_div_local,
        expected_divergent_decisions_global=expected_div_global,
        prob_any_divergence_local=float(1.0 - prob_none_local),
        prob_any_divergence_global=float(1.0 - prob_none_global),
        selected_jaccard=float(stats["jaccard"]),
        selected_symdiff_count=int(stats["symdiff"]),
        selected_shared_count=int(stats["shared"]),
        selected_force_only_count=int(stats["force_only"]),
        selected_prevent_only_count=int(stats["prevent_only"]),
    )


# ============================================================================
# Transient intervention
# ============================================================================

@dataclass
class InterventionResult:
    group: int
    pair_index: int
    side: str
    geometry: SiteGeometry

    E1_local: float
    E1_global: float
    expected_divergent_decisions_local: float
    prob_any_divergence_local: float

    g1_local: float
    g1_global: float
    lag1_realized_divergence: int

    G_local: float
    G_global: float
    far_field_gain: float
    GT_nonzero: int

    lag_local_gain: List[float]
    lag_global_gain: List[float]

    selected_jaccard_by_lag: List[float]
    selected_symdiff_by_lag: List[int]
    selected_shared_by_lag: List[int]
    selected_force_only_by_lag: List[int]
    selected_prevent_only_by_lag: List[int]

    max_capacity_fraction: float


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
    radius = int(profile["radius"])
    budget = int(profile["budget"])
    loss_rate = float(profile["loss_rate"])
    horizon = int(profile["horizon"])
    x = geometry.cell

    # Intervention update.
    force_grown, _, force_intervention_selected, _ = growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        budget,
        force_cell=x,
    )

    prevent_grown, _, prevent_intervention_selected, _ = growth_step(
        checkpoint,
        float(future_env[0]),
        radius,
        crystal_params,
        budget,
        prevent_cell=x,
    )

    if force_intervention_selected != prevent_intervention_selected:
        raise RuntimeError(
            "intervention evaluated sets unexpectedly differ"
        )

    force_state, _ = ch21.apply_background_loss(
        force_grown,
        loss_rate,
    )

    prevent_state, _ = ch21.apply_background_loss(
        prevent_grown,
        loss_rate,
    )

    # Exact conditional expectation before lag-1 Bernoulli thresholding.
    lag1_expect = exact_lag1_expectation(
        force_state,
        prevent_state,
        float(future_env[1]),
        x,
        profile,
        crystal_params,
    )

    lag_local: List[float] = []
    lag_global: List[float] = []

    jaccard_by_lag: List[float] = []
    symdiff_by_lag: List[int] = []
    shared_by_lag: List[int] = []
    force_only_by_lag: List[int] = []
    prevent_only_by_lag: List[int] = []

    g1_local = 0.0
    g1_global = 0.0
    lag1_realized_divergence = 0

    max_capacity = max(
        float(ch18.capacity_fraction_occupied(force_state.occupied, radius)),
        float(ch18.capacity_fraction_occupied(prevent_state.occupied, radius)),
    )

    for lag in range(1, horizon + 1):
        (
            force_state,
            force_add,
            _,
            force_eval,
            _,
        ) = canonical_step(
            force_state,
            float(future_env[lag]),
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
            float(future_env[lag]),
            radius,
            crystal_params,
            budget,
            loss_rate,
        )

        fset = {cell for cell in force_add if cell != x}
        pset = {cell for cell in prevent_add if cell != x}

        force_local = sum(
            1 <= relative_distance(cell, x) <= horizon
            for cell in fset
        )

        prevent_local = sum(
            1 <= relative_distance(cell, x) <= horizon
            for cell in pset
        )

        local_delta = float(force_local - prevent_local)
        global_delta = float(len(fset) - len(pset))

        lag_local.append(local_delta)
        lag_global.append(global_delta)

        stats = selected_set_stats(force_eval, prevent_eval)
        jaccard_by_lag.append(float(stats["jaccard"]))
        symdiff_by_lag.append(int(stats["symdiff"]))
        shared_by_lag.append(int(stats["shared"]))
        force_only_by_lag.append(int(stats["force_only"]))
        prevent_only_by_lag.append(int(stats["prevent_only"]))

        if lag == 1:
            g1_local = local_delta
            g1_global = global_delta

            f_local_set = {
                cell
                for cell in fset
                if 1 <= relative_distance(cell, x) <= horizon
            }
            p_local_set = {
                cell
                for cell in pset
                if 1 <= relative_distance(cell, x) <= horizon
            }

            lag1_realized_divergence = int(
                f_local_set != p_local_set
            )

            # Remove continuing direct support after one causal update.
            if x in force_state.occupied:
                force_state.occupied.remove(x)
                force_state.birth_time.pop(x, None)

                if force_state.population_by_step:
                    force_state.population_by_step[-1] = len(
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

    G_local = float(np.sum(lag_local))
    G_global = float(np.sum(lag_global))

    return InterventionResult(
        group=int(group),
        pair_index=int(pair_index),
        side=side,
        geometry=geometry,
        E1_local=float(lag1_expect.E1_local),
        E1_global=float(lag1_expect.E1_global),
        expected_divergent_decisions_local=float(
            lag1_expect.expected_divergent_decisions_local
        ),
        prob_any_divergence_local=float(
            lag1_expect.prob_any_divergence_local
        ),
        g1_local=float(g1_local),
        g1_global=float(g1_global),
        lag1_realized_divergence=int(lag1_realized_divergence),
        G_local=G_local,
        G_global=G_global,
        far_field_gain=float(G_global - G_local),
        GT_nonzero=int(abs(G_local) > 0.0),
        lag_local_gain=[float(v) for v in lag_local],
        lag_global_gain=[float(v) for v in lag_global],
        selected_jaccard_by_lag=jaccard_by_lag,
        selected_symdiff_by_lag=symdiff_by_lag,
        selected_shared_by_lag=shared_by_lag,
        selected_force_only_by_lag=force_only_by_lag,
        selected_prevent_only_by_lag=prevent_only_by_lag,
        max_capacity_fraction=float(max_capacity),
    )


# ============================================================================
# Statistics and precision-aware statuses
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
    se = sd / math.sqrt(len(arr)) if len(arr) else float("nan")
    achieved_mde = se * (Z_95_ONE_SIDED + Z_80_POWER)

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": low,
        "ci95_high": high,
        "half_width": float((high - low) / 2.0),
        "achieved_mde80_one_sided": float(achieved_mde),
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
        1.0
        + float(np.sum(null >= observed))
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

    powered_for_sei = (
        summary["achieved_mde80_one_sided"]
        <= sei
    )

    if (
        powered_for_sei
        and summary["mean"] >= sei
        and summary["ci95_low"] > 0.0
        and test["p_value"] < alpha
    ):
        return "SUPPORTED"

    if (
        powered_for_sei
        and summary["ci95_high"] < sei
    ):
        return "BOUNDED_BELOW_SEI"

    return "UNRESOLVED"


def summarize_directional(
    values: Sequence[float],
    sei: float,
    profile: dict,
    seed: int,
) -> dict:
    summary = bootstrap_mean_ci(
        values,
        int(profile["bootstrap_reps"]),
        seed,
    )

    test = signflip_greater(
        values,
        int(profile["signflip_permutations"]),
        seed + 1,
    )

    return {
        "sei": float(sei),
        "summary": summary,
        "signflip_greater": test,
    }


# ============================================================================
# Group aggregation
# ============================================================================

def group_pair_means(
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
    getter,
) -> List[float]:
    buckets: Dict[int, List[float]] = {}

    for high, low in paired_results:
        buckets.setdefault(high.group, []).append(
            float(getter(high, low))
        )

    return [
        float(np.mean(values))
        for _, values in sorted(buckets.items())
        if values
    ]


def group_side_means(
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
    side: str,
    getter,
) -> List[float]:
    buckets: Dict[int, List[float]] = {}

    for high, low in paired_results:
        result = high if side == "high" else low
        buckets.setdefault(result.group, []).append(
            float(getter(result))
        )

    return [
        float(np.mean(values))
        for _, values in sorted(buckets.items())
        if values
    ]


# ============================================================================
# Raw serialization
# ============================================================================

def geometry_dict(g: SiteGeometry) -> dict:
    d = asdict(g)
    d["cell"] = [int(g.cell[0]), int(g.cell[1])]
    return d


def intervention_dict(r: InterventionResult) -> dict:
    return {
        "group": r.group,
        "pair_index": r.pair_index,
        "side": r.side,
        "geometry": geometry_dict(r.geometry),
        "E1_local": r.E1_local,
        "E1_global": r.E1_global,
        "expected_divergent_decisions_local": (
            r.expected_divergent_decisions_local
        ),
        "prob_any_divergence_local": r.prob_any_divergence_local,
        "g1_local": r.g1_local,
        "g1_global": r.g1_global,
        "lag1_realized_divergence": r.lag1_realized_divergence,
        "G_local": r.G_local,
        "G_global": r.G_global,
        "far_field_gain": r.far_field_gain,
        "GT_nonzero": r.GT_nonzero,
        "lag_local_gain": r.lag_local_gain,
        "lag_global_gain": r.lag_global_gain,
        "selected_jaccard_by_lag": r.selected_jaccard_by_lag,
        "selected_symdiff_by_lag": r.selected_symdiff_by_lag,
        "selected_shared_by_lag": r.selected_shared_by_lag,
        "selected_force_only_by_lag": r.selected_force_only_by_lag,
        "selected_prevent_only_by_lag": r.selected_prevent_only_by_lag,
        "max_capacity_fraction": r.max_capacity_fraction,
    }


def write_raw_jsonl(
    path: Path,
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
) -> None:
    with path.open("w", encoding="utf-8") as f:
        for high, low in paired_results:
            f.write(json.dumps(intervention_dict(high)) + "\n")
            f.write(json.dumps(intervention_dict(low)) + "\n")


def write_raw_csv(
    path: Path,
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
) -> None:
    rows = []

    for high, low in paired_results:
        for r in (high, low):
            rows.append({
                "group": r.group,
                "pair_index": r.pair_index,
                "side": r.side,
                "q": r.geometry.cell[0],
                "r": r.geometry.cell[1],
                "FCP": r.geometry.fcp,
                "promoted_frontier": r.geometry.promoted_frontier,
                "occupied_neighbors": r.geometry.occupied_neighbors,
                "baseline_p": r.geometry.baseline_p,
                "radial_distance": r.geometry.radial_distance,
                "local_frontier_density_r2": (
                    r.geometry.local_frontier_density_r2
                ),
                "E1_local": r.E1_local,
                "E1_global": r.E1_global,
                "expected_divergent_decisions_local": (
                    r.expected_divergent_decisions_local
                ),
                "prob_any_divergence_local": (
                    r.prob_any_divergence_local
                ),
                "g1_local": r.g1_local,
                "g1_global": r.g1_global,
                "lag1_realized_divergence": (
                    r.lag1_realized_divergence
                ),
                "G_local": r.G_local,
                "G_global": r.G_global,
                "far_field_gain": r.far_field_gain,
                "GT_nonzero": r.GT_nonzero,
                "mean_selected_jaccard": float(
                    np.mean(r.selected_jaccard_by_lag)
                ),
                "mean_selected_symdiff": float(
                    np.mean(r.selected_symdiff_by_lag)
                ),
            })

    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections: List[Tuple[str, str]] = []

    def json(self, filename: str, payload: dict) -> None:
        (self.root / filename).write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    def stage(self, filename: str, title: str, payload: dict) -> None:
        body = "```json\n" + json.dumps(payload, indent=2) + "\n```"

        (self.root / filename).write_text(
            f"# {title}\n\n{body}\n",
            encoding="utf-8",
        )

        self.sections.append((title, body))

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch24-frontier-creation-causal-gain-v4-full-report.md"

        parts = [
            "# Chapter 24 — Frontier Creation, Divergence, and Causal Gain (V4)",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(metadata, indent=2),
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

        path.write_text("\n".join(parts), encoding="utf-8")
        return path


# ============================================================================
# Stage 0 — protocol
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
    seed: int,
    mode: str,
) -> dict:
    payload = {
        "experiment_version": EXPERIMENT_VERSION,
        "role": "RESET EXTREME-FCP CAUSAL MECHANISM TEST",
        "seed": int(seed),
        "mode": mode,
        "exposure": {
            "high": f"FCP >= {profile['high_fcp_min']}",
            "low": f"FCP <= {profile['low_fcp_max']}",
            "minimum_delta_FCP": int(
                profile["minimum_fcp_difference"]
            ),
            "FCP_identity": "FCP = promoted_frontier - 1",
            "promotion_status": (
                "implementation invariant, not independent evidence"
            ),
        },
        "pairing": {
            "same_occupied_neighbor_count": True,
            "same_radial_bin_width": int(
                profile["radial_bin_width"]
            ),
            "baseline_p_matched": False,
            "frontier_density_matched": False,
            "reason": (
                "baseline p and density may lie on or summarize the geometry "
                "pathway; V4 estimates the total extreme-geometry contrast"
            ),
        },
        "H1_primary": {
            "outcome": "Delta exact E1_local",
            "SEI": float(profile["sei_E1"]),
            "status_space": [
                "SUPPORTED",
                "BOUNDED_BELOW_SEI",
                "UNRESOLVED",
                "INVALID",
            ],
            "precision_gate": (
                "achieved one-sided 80% MDE must be <= SEI"
            ),
        },
        "H2_secondary": {
            "outcome": "Delta realized g1_local",
            "SEI": float(profile["sei_g1"]),
        },
        "H3_mechanism": {
            "outcome": "Delta model-implied P(any lag1 local divergence)",
            "SEI": float(
                profile["sei_divergence_probability"]
            ),
        },
        "H4_downstream": {
            "outcome": "Delta G_T(H)",
            "SEI": float(profile["sei_GT"]),
        },
        "zero_inflation_decomposition": [
            "P(lag1 realized divergence)",
            "P(G_T != 0)",
            "E[G_T | G_T != 0]",
        ],
        "support_gate": {
            "minimum_group_coverage_fraction": float(
                profile["minimum_group_coverage_fraction"]
            ),
            "no_automatic_weaker_contrast": True,
            "design_audit_provenance": (
                "Frozen at 0.50 after outcome-blind 48-group seed-20260909 "
                "support audit found 0.5417 coverage for exact Delta-FCP=3. "
                "No V4 causal outcomes were inspected."
            ),
        },
        "horizon": int(profile["horizon"]),
        "classifier_used": False,
        "scientific": bool(profile["scientific"]),
        "status": (
            "FROZEN"
            if profile["scientific"]
            else "ENGINEERING_SMOKE_ONLY"
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 24 V4 Reset Protocol",
        payload,
    )
    reporter.json("stage-00-protocol.json", payload)

    return payload


# ============================================================================
# Stage 1 — support audit
# ============================================================================

@dataclass
class GroupPrepared:
    group: int
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray
    sites: List[SiteGeometry]
    pairs: List[SitePair]
    checkpoint_capacity: float


def prepare_groups(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> List[GroupPrepared]:
    groups = []

    for group in tqdm(
        range(int(profile["groups"])),
        desc="Chapter 24 V4 support audit",
    ):
        checkpoint, future_env, capacity = build_checkpoint(
            profile,
            crystal_params,
            seed,
            group,
        )

        sites = evaluated_geometries(
            checkpoint,
            float(future_env[0]),
            profile,
            crystal_params,
        )

        pairs = construct_extreme_pairs(
            sites,
            profile,
        )

        groups.append(
            GroupPrepared(
                group=group,
                checkpoint=checkpoint,
                future_env=future_env,
                sites=sites,
                pairs=pairs,
                checkpoint_capacity=capacity,
            )
        )

    return groups


def stage_1_support(
    reporter: Reporter,
    profile: dict,
    groups: Sequence[GroupPrepared],
) -> dict:
    groups_with_pairs = sum(bool(g.pairs) for g in groups)

    coverage = groups_with_pairs / max(1, len(groups))

    all_sites = [
        site
        for g in groups
        for site in g.sites
    ]

    fcp_counts: Dict[int, int] = {}

    for site in all_sites:
        fcp_counts[site.fcp] = fcp_counts.get(site.fcp, 0) + 1

    pair_counts = [len(g.pairs) for g in groups]

    pair_fcp_deltas = [
        pair.high.fcp - pair.low.fcp
        for g in groups
        for pair in g.pairs
    ]

    pair_p_deltas = [
        pair.high.baseline_p - pair.low.baseline_p
        for g in groups
        for pair in g.pairs
    ]

    pair_density_deltas = [
        (
            pair.high.local_frontier_density_r2
            - pair.low.local_frontier_density_r2
        )
        for g in groups
        for pair in g.pairs
    ]

    payload = {
        "requested_groups": int(len(groups)),
        "groups_with_extreme_pairs": int(groups_with_pairs),
        "coverage_fraction": float(coverage),
        "minimum_coverage_fraction": float(
            profile["minimum_group_coverage_fraction"]
        ),
        "coverage_gate_passed": bool(
            coverage
            >= profile["minimum_group_coverage_fraction"]
        ),
        "total_evaluated_usable_sites": int(len(all_sites)),
        "FCP_site_counts": {
            str(k): int(v)
            for k, v in sorted(fcp_counts.items())
        },
        "total_extreme_pairs": int(sum(pair_counts)),
        "pair_count_distribution": {
            "min": int(min(pair_counts) if pair_counts else 0),
            "median": float(
                np.median(pair_counts) if pair_counts else 0.0
            ),
            "max": int(max(pair_counts) if pair_counts else 0),
        },
        "achieved_pair_delta_FCP": {
            "mean": float(np.mean(pair_fcp_deltas))
            if pair_fcp_deltas
            else float("nan"),
            "min": int(min(pair_fcp_deltas))
            if pair_fcp_deltas
            else None,
            "max": int(max(pair_fcp_deltas))
            if pair_fcp_deltas
            else None,
        },
        "unmatched_possible_mediator_diagnostics": {
            "baseline_p_high_minus_low_mean": float(
                np.mean(pair_p_deltas)
            )
            if pair_p_deltas
            else float("nan"),
            "frontier_density_high_minus_low_mean": float(
                np.mean(pair_density_deltas)
            )
            if pair_density_deltas
            else float("nan"),
        },
        "note": (
            "No causal outcome data are used in this stage. "
            "No weaker FCP contrast is substituted if coverage fails."
        ),
    }

    reporter.stage(
        "stage-01-design-support.md",
        "Stage 1 — Extreme-FCP Design Support Audit",
        payload,
    )
    reporter.json("stage-01-design-support.json", payload)

    return payload


# ============================================================================
# Stage 2 — interventions
# ============================================================================

def stage_2_interventions(
    reporter: Reporter,
    profile: dict,
    groups: Sequence[GroupPrepared],
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    List[Tuple[InterventionResult, InterventionResult]],
    dict,
]:
    paired_results = []
    max_capacity = 0.0

    for prepared in tqdm(
        groups,
        desc="Chapter 24 V4 causal interventions",
    ):
        max_capacity = max(
            max_capacity,
            prepared.checkpoint_capacity,
        )

        for pair_index, pair in enumerate(prepared.pairs):
            high = run_transient_intervention(
                prepared.checkpoint,
                prepared.future_env,
                pair.high,
                profile,
                crystal_params,
                prepared.group,
                pair_index,
                "high",
            )

            low = run_transient_intervention(
                prepared.checkpoint,
                prepared.future_env,
                pair.low,
                profile,
                crystal_params,
                prepared.group,
                pair_index,
                "low",
            )

            max_capacity = max(
                max_capacity,
                high.max_capacity_fraction,
                low.max_capacity_fraction,
            )

            paired_results.append((high, low))

    payload = {
        "total_pairs_run": int(len(paired_results)),
        "maximum_capacity_fraction": float(max_capacity),
        "capacity_gate_passed": bool(
            max_capacity < profile["max_capacity_fraction"]
        ),
    }

    reporter.stage(
        "stage-02-interventions.md",
        "Stage 2 — Extreme-FCP Transient Interventions",
        payload,
    )
    reporter.json("stage-02-interventions.json", payload)

    write_raw_jsonl(
        reporter.root / "raw-interventions.jsonl",
        paired_results,
    )

    write_raw_csv(
        reporter.root / "raw-interventions.csv",
        paired_results,
    )

    return paired_results, payload


# ============================================================================
# Stage 3 — primary and secondary analyses
# ============================================================================

def stage_3_analysis(
    reporter: Reporter,
    profile: dict,
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
    seed: int,
    valid: bool,
) -> dict:
    delta_E1 = group_pair_means(
        paired_results,
        lambda h, l: h.E1_local - l.E1_local,
    )

    delta_g1 = group_pair_means(
        paired_results,
        lambda h, l: h.g1_local - l.g1_local,
    )

    delta_div_prob = group_pair_means(
        paired_results,
        lambda h, l:
        (
            h.prob_any_divergence_local
            - l.prob_any_divergence_local
        ),
    )

    delta_GT = group_pair_means(
        paired_results,
        lambda h, l: h.G_local - l.G_local,
    )

    H1 = summarize_directional(
        delta_E1,
        float(profile["sei_E1"]),
        profile,
        seed + 300,
    )

    H2 = summarize_directional(
        delta_g1,
        float(profile["sei_g1"]),
        profile,
        seed + 310,
    )

    H3 = summarize_directional(
        delta_div_prob,
        float(profile["sei_divergence_probability"]),
        profile,
        seed + 320,
    )

    H4 = summarize_directional(
        delta_GT,
        float(profile["sei_GT"]),
        profile,
        seed + 330,
    )

    H1["status"] = directional_status(
        H1["summary"],
        H1["signflip_greater"],
        float(profile["sei_E1"]),
        float(profile["alpha"]),
        valid,
    )

    H2["status"] = directional_status(
        H2["summary"],
        H2["signflip_greater"],
        float(profile["sei_g1"]),
        float(profile["alpha"]),
        valid,
    )

    H3["status"] = directional_status(
        H3["summary"],
        H3["signflip_greater"],
        float(profile["sei_divergence_probability"]),
        float(profile["alpha"]),
        valid,
    )

    H4["status"] = directional_status(
        H4["summary"],
        H4["signflip_greater"],
        float(profile["sei_GT"]),
        float(profile["alpha"]),
        valid,
    )

    payload = {
        "H1_primary_exact_expected_lag1_gain": H1,
        "H2_realized_lag1_gain": H2,
        "H3_model_implied_lag1_divergence_probability": H3,
        "H4_finite_horizon_transient_gain": H4,
    }

    reporter.stage(
        "stage-03-primary-analysis.md",
        "Stage 3 — Precision-Aware Causal Analysis",
        payload,
    )
    reporter.json("stage-03-primary-analysis.json", payload)

    return payload


# ============================================================================
# Stage 4 — zero-inflation and budget diagnostics
# ============================================================================

def conditional_nonzero_mean(values: Sequence[float]) -> dict:
    arr = finite_array(values)
    nz = arr[np.abs(arr) > 0.0]

    return {
        "n_all": int(len(arr)),
        "nonzero_n": int(len(nz)),
        "nonzero_fraction": float(len(nz) / len(arr))
        if len(arr)
        else float("nan"),
        "mean_all": float(np.mean(arr))
        if len(arr)
        else float("nan"),
        "mean_given_nonzero": float(np.mean(nz))
        if len(nz)
        else float("nan"),
    }


def stage_4_decomposition(
    reporter: Reporter,
    profile: dict,
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
    seed: int,
) -> dict:
    high_lag1_div = group_side_means(
        paired_results,
        "high",
        lambda r: r.lag1_realized_divergence,
    )

    low_lag1_div = group_side_means(
        paired_results,
        "low",
        lambda r: r.lag1_realized_divergence,
    )

    high_nonzero = group_side_means(
        paired_results,
        "high",
        lambda r: r.GT_nonzero,
    )

    low_nonzero = group_side_means(
        paired_results,
        "low",
        lambda r: r.GT_nonzero,
    )

    high_GT = [
        high.G_local
        for high, _ in paired_results
    ]

    low_GT = [
        low.G_local
        for _, low in paired_results
    ]

    high_jaccard = group_side_means(
        paired_results,
        "high",
        lambda r: float(
            np.mean(r.selected_jaccard_by_lag)
        ),
    )

    low_jaccard = group_side_means(
        paired_results,
        "low",
        lambda r: float(
            np.mean(r.selected_jaccard_by_lag)
        ),
    )

    high_symdiff = group_side_means(
        paired_results,
        "high",
        lambda r: float(
            np.mean(r.selected_symdiff_by_lag)
        ),
    )

    low_symdiff = group_side_means(
        paired_results,
        "low",
        lambda r: float(
            np.mean(r.selected_symdiff_by_lag)
        ),
    )

    high_far = group_side_means(
        paired_results,
        "high",
        lambda r: r.far_field_gain,
    )

    low_far = group_side_means(
        paired_results,
        "low",
        lambda r: r.far_field_gain,
    )

    payload = {
        "zero_inflation": {
            "high": {
                "lag1_realized_divergence_rate": bootstrap_mean_ci(
                    high_lag1_div,
                    int(profile["bootstrap_reps"]),
                    seed + 401,
                ),
                "GT_nonzero_rate": bootstrap_mean_ci(
                    high_nonzero,
                    int(profile["bootstrap_reps"]),
                    seed + 402,
                ),
                "GT": conditional_nonzero_mean(high_GT),
            },
            "low": {
                "lag1_realized_divergence_rate": bootstrap_mean_ci(
                    low_lag1_div,
                    int(profile["bootstrap_reps"]),
                    seed + 403,
                ),
                "GT_nonzero_rate": bootstrap_mean_ci(
                    low_nonzero,
                    int(profile["bootstrap_reps"]),
                    seed + 404,
                ),
                "GT": conditional_nonzero_mean(low_GT),
            },
        },
        "absolute_selection_displacement": {
            "high_mean_jaccard": bootstrap_mean_ci(
                high_jaccard,
                int(profile["bootstrap_reps"]),
                seed + 405,
            ),
            "low_mean_jaccard": bootstrap_mean_ci(
                low_jaccard,
                int(profile["bootstrap_reps"]),
                seed + 406,
            ),
            "high_mean_symdiff_count": bootstrap_mean_ci(
                high_symdiff,
                int(profile["bootstrap_reps"]),
                seed + 407,
            ),
            "low_mean_symdiff_count": bootstrap_mean_ci(
                low_symdiff,
                int(profile["bootstrap_reps"]),
                seed + 408,
            ),
        },
        "far_field_gain": {
            "high": bootstrap_mean_ci(
                high_far,
                int(profile["bootstrap_reps"]),
                seed + 409,
            ),
            "low": bootstrap_mean_ci(
                low_far,
                int(profile["bootstrap_reps"]),
                seed + 410,
            ),
        },
    }

    reporter.stage(
        "stage-04-decomposition.md",
        "Stage 4 — Divergence, Zero Inflation, and Budget Diagnostics",
        payload,
    )
    reporter.json("stage-04-decomposition.json", payload)

    return payload


# ============================================================================
# Stage 5 — bounded verdict
# ============================================================================

def stage_5_verdict(
    reporter: Reporter,
    profile: dict,
    support: dict,
    interventions: dict,
    analysis: dict,
) -> dict:
    support_valid = bool(support["coverage_gate_passed"])
    capacity_valid = bool(interventions["capacity_gate_passed"])
    valid = support_valid and capacity_valid

    if not profile["scientific"]:
        overall = "ENGINEERING_SMOKE_ONLY"
        bounded = (
            "Smoke profile completed. No scientific interpretation is eligible."
        )

    elif not support_valid:
        overall = "INVALID_EXTREME_FCP_SUPPORT"
        bounded = (
            "The predeclared FCP >= +2 versus FCP <= -1 contrast did not "
            "achieve the frozen group-coverage gate. No weaker contrast was "
            "substituted."
        )

    elif not capacity_valid:
        overall = "INVALID_CAPACITY"
        bounded = (
            "The run crossed the frozen capacity validity gate."
        )

    else:
        h1 = analysis[
            "H1_primary_exact_expected_lag1_gain"
        ]["status"]

        h2 = analysis[
            "H2_realized_lag1_gain"
        ]["status"]

        h4 = analysis[
            "H4_finite_horizon_transient_gain"
        ]["status"]

        if h1 == "SUPPORTED":
            overall = "EXTREME_FCP_CHANGES_EXPECTED_IMMEDIATE_CAUSAL_GAIN"

            bounded = (
                "Under the frozen extreme-contrast protocol, frontier sites "
                "with FCP >= +2 had a scientifically meaningful larger exact "
                "expected lag-1 local construction effect than matched FCP <= "
                "-1 sites. Realized and downstream outcomes are reported "
                "separately and are not required to share the same precision."
            )

        elif h1 == "BOUNDED_BELOW_SEI":
            overall = "EXTREME_FCP_EXPECTED_EFFECT_BOUNDED_BELOW_SEI"

            bounded = (
                "The full-precision V4 run bounded the high-minus-low extreme "
                "FCP difference in exact expected lag-1 local construction "
                "below the predeclared scientifically meaningful effect size."
            )

        else:
            overall = "EXTREME_FCP_EXPECTED_EFFECT_UNRESOLVED"

            bounded = (
                "V4 did not resolve the predeclared extreme-FCP expected "
                "lag-1 effect at its frozen smallest effect of interest. "
                "This is reported as unresolved rather than failed."
            )

    payload = {
        "validity": {
            "valid": bool(valid),
            "support_gate": bool(support_valid),
            "capacity_gate": bool(capacity_valid),
        },
        "overall_status": overall,
        "bounded_claim": bounded,
        "hypothesis_statuses": {
            name: result.get("status")
            for name, result in analysis.items()
        },
        "interpretation_rules": {
            "underpowered_non_significance_is_failure": False,
            "FCP_promotion_identity_is_independent_evidence": False,
            "baseline_p_was_conditioned_away": False,
            "realized_GT_is_only_outcome": False,
        },
        "what_this_does_not_establish": [
            "FCP is an independent causal variable",
            "baseline p is not a mediator",
            "causal-gain field",
            "stable high-gain regions",
            "criticality",
            "percolation",
            "coherent structures",
            "individuality",
            "organism",
            "life",
        ],
        "next": (
            "Regardless of outcome, use the absolute FORCE/PREVENT selection "
            "displacement measurements to design a dedicated finite-budget "
            "redistribution experiment with an unbounded-budget hard-zero "
            "control."
        ),
    }

    reporter.stage(
        "stage-05-verdict.md",
        "Stage 5 — Bounded Chapter 24 V4 Verdict",
        payload,
    )
    reporter.json("stage-05-verdict.json", payload)

    return payload


# ============================================================================
# Plots
# ============================================================================

def make_plots(
    paired_results: Sequence[
        Tuple[InterventionResult, InterventionResult]
    ],
    image_dir: Path,
) -> None:
    image_dir.mkdir(parents=True, exist_ok=True)

    if not paired_results:
        return

    fcp = []
    e1 = []
    gt = []

    for high, low in paired_results:
        for result in (high, low):
            fcp.append(result.geometry.fcp)
            e1.append(result.E1_local)
            gt.append(result.G_local)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(fcp, e1, alpha=0.35)
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Frontier Creation Potential")
    ax.set_ylabel("Exact expected lag-1 local gain")
    ax.set_title("Chapter 24 V4: FCP and exact expected causal effect")
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch24-v4-fcp-vs-expected-lag1-gain.png",
        dpi=160,
    )
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(e1, gt, alpha=0.35)
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Exact expected lag-1 local gain")
    ax.set_ylabel("Realized transient G_T(H)")
    ax.set_title("Chapter 24 V4: expected immediate effect vs realized cascade")
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch24-v4-expected-vs-realized-transient-gain.png",
        dpi=160,
    )
    plt.close(fig)


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="full",
    )

    parser.add_argument(
        "--mode",
        choices=["audit", "run"],
        default="run",
        help=(
            "audit: support only, no causal outcomes; "
            "run: full frozen experiment"
        ),
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=20260909,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch24-frontier-creation-causal-gain-v4"
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

    profile = dict(PROFILES[args.profile])
    crystal_params = ch18.CrystalParams()

    reporter = Reporter(args.report_dir)

    metadata = {
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "run_title": RUN_TITLE,
        "profile": args.profile,
        "profile_config": profile,
        "mode": args.mode,
        "seed": int(args.seed),
        "previous_ch24_seeds": [
            20260906,
            20260907,
            20260908,
        ],
        "fresh_seed": bool(
            int(args.seed)
            not in {
                20260906,
                20260907,
                20260908,
            }
        ),
        "classifier_used": False,
        "canonical_rules_modified": False,
        "started_at_unix": float(time.time()),
    }

    print("=" * 78)
    print("CHAPTER 24 V4 — FRONTIER CREATION / DIVERGENCE RESET")
    print(
        f"profile={args.profile} "
        f"mode={args.mode} "
        f"groups={profile['groups']} "
        f"contrast=FCP>={profile['high_fcp_min']} "
        f"vs FCP<={profile['low_fcp_max']} "
        f"H={profile['horizon']} "
        f"seed={args.seed}"
    )
    print("=" * 78)

    stage_0_protocol(
        reporter,
        profile,
        args.seed,
        args.mode,
    )

    groups = prepare_groups(
        profile,
        crystal_params,
        args.seed,
    )

    support = stage_1_support(
        reporter,
        profile,
        groups,
    )

    if args.mode == "audit":
        metadata["finished_at_unix"] = float(time.time())
        metadata["final_status"] = (
            "AUDIT_SUPPORT_PASSED"
            if support["coverage_gate_passed"]
            else "AUDIT_SUPPORT_FAILED"
        )

        reporter.json("run-metadata.json", metadata)
        report = reporter.full_report(metadata)

        print()
        print("=" * 78)
        print(metadata["final_status"])
        print(f"coverage={support['coverage_fraction']:.3f}")
        print(f"Report: {report}")
        print("=" * 78)
        return

    interventions, s2 = stage_2_interventions(
        reporter,
        profile,
        groups,
        crystal_params,
    )

    valid_for_analysis = bool(
        support["coverage_gate_passed"]
        and s2["capacity_gate_passed"]
    )

    analysis = stage_3_analysis(
        reporter,
        profile,
        interventions,
        args.seed,
        valid_for_analysis,
    )

    decomposition = stage_4_decomposition(
        reporter,
        profile,
        interventions,
        args.seed,
    )

    verdict = stage_5_verdict(
        reporter,
        profile,
        support,
        s2,
        analysis,
    )

    make_plots(
        interventions,
        args.image_dir,
    )

    metadata["finished_at_unix"] = float(time.time())
    metadata["final_status"] = verdict["overall_status"]

    reporter.json("run-metadata.json", metadata)
    report = reporter.full_report(metadata)

    print()
    print("=" * 78)
    print(f"FINAL STATUS: {verdict['overall_status']}")
    print(verdict["bounded_claim"])
    print(f"Report: {report}")
    print("=" * 78)


if __name__ == "__main__":
    main()
