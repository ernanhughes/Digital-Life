#!/usr/bin/env python3
"""
Digital Life — Chapter 27 V2
Can Stored Material History Change Downstream Causal Consequence?
===============================================================

SCIENTIFIC ROLE
---------------

Corrected Chapter 27 experiment.

V1 established a valid immediate E1 effect but its 12-step primary intervention
was invalid because PREVENT did not explicitly prevent x from attaching during
the first causal exposure.

V2 fixes that construct-validity defect and freezes a more precise estimator.

THIS IS NOT PARAMETER RESCUE.

Frozen from V1:
    HISTORY_K              = 2
    LOCAL_HISTORY_RADIUS   = 3
    HISTORY_HALF_LIFE      = 6
    HISTORY_AGE            = 3
    MATERIAL_GAIN          = 0.30
    HORIZON                = 12
    PRIMARY_SEI            = +/-0.15 attachments
    allocation policy      = true unbounded
    dynamic PREVENT matching = per-lag
    accessible placement   = includes x's sole occupied neighbour
    no material inheritance
    no material propagation

Construct-validity corrections only:
    1. PREVENT explicitly blocks x during lag 1.
    2. FORCE explicitly contains x during lag 1.
    3. Remote trace carriers are matched to accessible carriers on baseline
       frontier influence rather than chosen simply as the farthest cells.
    4. Primary estimator is the lag-wise conditional expected local causal
       consequence (Rao-Blackwellized), exactly aligned to G_local's spatial
       support and excluding x at every lag.
    5. Realized G_local remains secondary.

FRESH SCIENTIFIC SEED
---------------------

Default:
    20260915

Previous scientific seeds:
    Ch24 V4  20260909
    Ch24 V5  20260910
    Ch25 V1  20260911
    Ch26 V1  20260912
    Ch26 V2  20260913
    Ch27 V1  20260914

PRIMARY QUESTION
----------------

At identical visible occupancy geometry, identical probe geometry, matched
initial material mass, matched remote-carrier baseline influence, same future
environment, same cell-keyed randomness, true-unbounded evaluation, and
dynamically matched PREVENT background construction:

    does locally accessible decaying material state change finite-horizon
    expected causal consequence relative to an equally strong causally remote
    material state?

PRIMARY CONTRAST
----------------

For each probe and history arm:

    RB_G_LOCAL(H)
      =
      sum over lags 1..H
      [
        sum_{1 <= d(cell,x) <= H, cell != x}
            p_FORCE(cell, lag)
        -
        sum_{1 <= d(cell,x) <= H, cell != x}
            p_PREVENT(cell, lag)
      ]

computed on the actual branch states immediately before each lag's growth step.

Primary:
    Delta_RB_G
      =
      RB_G_LOCAL(accessible)
      -
      RB_G_LOCAL(remote)

This removes within-lag Bernoulli attachment noise but preserves:
    branch-state divergence
    history decay
    background loss
    nonlinear probability changes
    downstream consequences of earlier realized events

The estimator does NOT normalize FORCE independently.

REALIZED SECONDARY
------------------

Also report:

    G_LOCAL_REALIZED(H)

using the same spatial support:
    1 <= distance(cell,x) <= H
    x excluded at every lag.

INTERVENTION SEMANTICS
----------------------

At t0:
    FORCE   = history state + x occupied
    PREVENT = history state + x empty

At lag 1 growth:
    FORCE explicitly blocks x from being treated as a frontier candidate
          because x is already occupied.
    PREVENT explicitly excludes x from attachment.

After lag 1 growth + loss:
    x is forcibly removed from FORCE if still occupied.
    x is absent from PREVENT by construction.

Thus the transient intervention receives exactly one causal growth exposure
and the two branches do not acquire a sign-reversed control defect.

At lags 2..H:
    x is no longer specially blocked in either branch.
    If ordinary dynamics later reoccupy x, that is part of the downstream
    process, but x itself remains excluded from both expected and realized
    outcome accounting.

REMOTE MATCHING
---------------

Accessible history uses:
    HISTORY_K occupied cells within LOCAL_HISTORY_RADIUS
    including x's sole occupied neighbour.

For every accessible carrier c, define its baseline frontier influence on the
ERASED checkpoint:

    carrier_frontier_count(c)
        = number of erased frontier cells adjacent to c

    carrier_frontier_probability_mass(c)
        = sum of erased offset-0 attachment probabilities over those adjacent
          frontier cells at the first continuation input.

Remote candidates must:
    distance(cell,x) > HORIZON + REMOTE_MARGIN
    not be accessible carriers
    be occupied at the same checkpoint.

Each accessible carrier is greedily matched to a distinct remote carrier with:
    exact same carrier_frontier_count
and minimum:
    absolute difference in carrier_frontier_probability_mass.

Frozen support tolerance:
    abs(probability_mass_remote - probability_mass_accessible) <= 0.05

If a complete HISTORY_K remote match cannot be formed before looking at
outcomes:
    probe is UNSUPPORTED.

This controls the main V1 remote-placement defect while preserving causal
separation.

DYNAMIC BACKGROUND-CONSTRUCTION MATCHING
----------------------------------------

Same discipline as V1.

A dedicated ERASED PREVENT reference trajectory defines:
    C_target(tau)

At every lag, for accessible and remote:
    solve one additive offset on CURRENT PREVENT state so expected total
    attachments match C_target(tau).

Apply the SAME solved offset to FORCE.

FORCE is never separately normalized.

ERASED:
    offset = 0 by definition.

VALIDITY
--------

Scientific validity requires:

1. >= 90% independent-group probe coverage.
2. >= 95% accessible/remote probe x lag PREVENT calibration records within 2%.
3. Every population-mean accessible/remote arm x lag relative error within 2%.
4. Every supported probe:
       same occupied set across history arms at t0
       HISTORY_K accessible cells
       HISTORY_K remote cells
       equal initial material mass
       sole occupied neighbour included in accessible
       every remote cell farther than H + REMOTE_MARGIN
       matched carrier frontier count exactly
       matched carrier probability mass within 0.05
5. Lag-1 intervention assertion:
       PREVENT x not selected / not attached
       FORCE x present during first growth exposure
       x absent from both branches after intervention cleanup.

If validity fails:
    INVALID

PRIMARY STATUS
--------------

Frozen SEI:
    +/-0.15 expected local attachments

SUPPORTED:
    |mean Delta_RB_G| >= 0.15
    95% CI excludes 0
    achieved MDE80 <= 0.15

BOUNDED_NEAR_ZERO:
    full 95% CI lies inside [-0.15,+0.15]
    achieved MDE80 <= 0.15

UNRESOLVED:
    otherwise

INVALID:
    validity gate fails

SECONDARY
---------

Report:
    realized G_local accessible - remote
    E1_ring1 accessible - remote
    E1_global accessible - remote
    G_nonzero rate
    material mass trajectory
    calibration offsets
    carrier matching quality
    CRN correlation
    remote - erased controls
    accessible - erased controls

V1 immediate saturation mechanism is NOT retested as a new primary claim.

STOP RULE
---------

If V2 is scientifically valid and:
    SUPPORTED -> close Chapter 27 with bounded positive downstream claim.
    BOUNDED_NEAR_ZERO -> close at +/-0.15.
    UNRESOLVED only because MDE > SEI -> increase independent groups only.

No parameter changes after full run.

PROFILES
--------

smoke:
    8 groups, 2 probes/group, engineering only

quick:
    48 groups, 4 probes/group

standard:
    96 groups, 4 probes/group

full:
    192 groups, 4 probes/group

OUTPUTS
-------

raw-v2-arm-results.jsonl
raw-v2-arm-results.csv
raw-v2-per-lag.jsonl
raw-v2-per-lag.csv
history-matching-details.json
stage reports
full Markdown report

DEPENDENCIES
------------

Requires beside this script:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py
    ch27_digital_crystal_decaying_material_history_causal_response_v1.py
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
import ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2 as ch26
import ch27_digital_crystal_decaying_material_history_causal_response_v1 as v1


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-decaying-material-history-causal-response-v2"
SCHEMA_VERSION = 2
CHAPTER = 27
CHAPTER_TITLE = "Can Stored Material History Change Downstream Causal Consequence?"

HORIZON = 12
PRIMARY_SEI = 0.15

HISTORY_K = v1.HISTORY_K
LOCAL_HISTORY_RADIUS = v1.LOCAL_HISTORY_RADIUS
REMOTE_MARGIN = v1.REMOTE_MARGIN

HISTORY_HALF_LIFE = v1.HISTORY_HALF_LIFE
HISTORY_AGE = v1.HISTORY_AGE
MATERIAL_GAIN = v1.MATERIAL_GAIN
INITIAL_HISTORY_STRENGTH = v1.INITIAL_HISTORY_STRENGTH
DECAY_FACTOR = v1.DECAY_FACTOR

REMOTE_INFLUENCE_MASS_TOL = 0.05

MATCH_TOLERANCE = v1.MATCH_TOLERANCE
MIN_RECORD_MATCH_FRACTION = v1.MIN_RECORD_MATCH_FRACTION
MIN_GROUP_COVERAGE = v1.MIN_GROUP_COVERAGE

ASSERT_TOL = 1e-12

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

ARMS = [
    "accessible",
    "remote",
    "erased",
]

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

    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / math.sqrt(len(arr))

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "sd": sd,
        "se": float(se),
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
        "achieved_mde80_one_sided": float(
            se * (
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
        summary["achieved_mde80_one_sided"]
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


def corr(
    x: Sequence[float],
    y: Sequence[float],
) -> float:
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)

    mask = np.isfinite(xa) & np.isfinite(ya)
    xa = xa[mask]
    ya = ya[mask]

    if len(xa) < 3:
        return float("nan")

    if np.std(xa) == 0 or np.std(ya) == 0:
        return float("nan")

    return float(
        np.corrcoef(xa, ya)[0, 1]
    )


# ============================================================================
# State helpers
# ============================================================================

HistoryState = v1.HistoryState
Probe = v1.Probe


def clone_state(
    state: HistoryState,
) -> HistoryState:
    return v1.clone_state(state)


def from_checkpoint(
    checkpoint: ch18.MaterialCrystalState,
) -> HistoryState:
    return v1.from_checkpoint(checkpoint)


def material_mass(
    state: HistoryState,
) -> float:
    return v1.material_mass(state)


def attachment_probability(
    cell: Cell,
    state: HistoryState,
    input_value: float,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    return v1.attachment_probability(
        cell,
        state,
        input_value,
        crystal_params,
        offset,
    )


def frontier_cells(
    state: HistoryState,
    radius: int,
) -> List[Cell]:
    return v1.frontier_cells(
        state,
        radius,
    )


def expected_attachments(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    return v1.expected_attachments(
        state,
        input_value,
        radius,
        crystal_params,
        offset,
    )


def solve_offset(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    target: float,
):
    return v1.solve_offset(
        state,
        input_value,
        radius,
        crystal_params,
        target,
    )


# ============================================================================
# Remote influence matching
# ============================================================================

@dataclass
class CarrierInfluence:
    cell: Cell
    frontier_count: int
    probability_mass: float


@dataclass
class HistoryPlacementV2:
    accessible_cells: Tuple[Cell, ...]
    remote_cells: Tuple[Cell, ...]
    sole_occupied_neighbor: Cell
    accessible_influence: Tuple[CarrierInfluence, ...]
    remote_influence: Tuple[CarrierInfluence, ...]
    max_probability_mass_error: float


def sole_occupied_neighbor(
    checkpoint: ch18.MaterialCrystalState,
    x: Cell,
) -> Cell | None:
    occupied = set(
        checkpoint.occupied
    )

    nbs = [
        nb
        for nb in ch18.neighbors(x)
        if nb in occupied
    ]

    if len(nbs) != 1:
        return None

    return nbs[0]


def carrier_influence(
    carrier: Cell,
    erased_state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
) -> CarrierInfluence:
    frontier = set(
        frontier_cells(
            erased_state,
            radius,
        )
    )

    affected = [
        nb
        for nb in ch18.neighbors(carrier)
        if nb in frontier
    ]

    probability_mass = float(
        sum(
            attachment_probability(
                cell,
                erased_state,
                input_value,
                crystal_params,
                0.0,
            )
            for cell in affected
        )
    )

    return CarrierInfluence(
        cell=carrier,
        frontier_count=int(len(affected)),
        probability_mass=probability_mass,
    )


def build_history_placement_v2(
    probe: Probe,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> HistoryPlacementV2 | None:
    occupied = set(
        probe.checkpoint.occupied
    )

    x = probe.cell
    sole = sole_occupied_neighbor(
        probe.checkpoint,
        x,
    )

    if sole is None:
        return None

    erased_state = from_checkpoint(
        probe.checkpoint
    )

    input_value = float(
        probe.future_env[1]
    )

    radius = int(
        source_profile["radius"]
    )

    local_candidates = [
        cell
        for cell in occupied
        if (
            v4.relative_distance(
                cell,
                x,
            )
            <= LOCAL_HISTORY_RADIUS
        )
    ]

    local_candidates.sort(
        key=lambda cell: (
            0 if cell == sole else 1,
            v4.relative_distance(
                cell,
                x,
            ),
            cell,
        )
    )

    if len(local_candidates) < HISTORY_K:
        return None

    accessible = tuple(
        local_candidates[:HISTORY_K]
    )

    if sole not in accessible:
        return None

    accessible_influence = tuple(
        carrier_influence(
            cell,
            erased_state,
            input_value,
            radius,
            crystal_params,
        )
        for cell in accessible
    )

    remote_min_distance = (
        HORIZON
        + REMOTE_MARGIN
    )

    remote_candidates = [
        cell
        for cell in occupied
        if (
            v4.relative_distance(
                cell,
                x,
            )
            > remote_min_distance
            and cell not in accessible
        )
    ]

    remote_influence_map = {
        cell: carrier_influence(
            cell,
            erased_state,
            input_value,
            radius,
            crystal_params,
        )
        for cell in remote_candidates
    }

    chosen = []
    chosen_influence = []
    used = set()
    errors = []

    for target in accessible_influence:
        candidates = [
            inf
            for cell, inf
            in remote_influence_map.items()
            if (
                cell not in used
                and inf.frontier_count
                == target.frontier_count
            )
        ]

        if not candidates:
            return None

        candidates.sort(
            key=lambda inf: (
                abs(
                    inf.probability_mass
                    - target.probability_mass
                ),
                -v4.relative_distance(
                    inf.cell,
                    x,
                ),
                inf.cell,
            )
        )

        best = candidates[0]
        error = abs(
            best.probability_mass
            - target.probability_mass
        )

        if (
            error
            > REMOTE_INFLUENCE_MASS_TOL
        ):
            return None

        used.add(
            best.cell
        )

        chosen.append(
            best.cell
        )

        chosen_influence.append(
            best
        )

        errors.append(
            error
        )

    if len(chosen) != HISTORY_K:
        return None

    return HistoryPlacementV2(
        accessible_cells=tuple(accessible),
        remote_cells=tuple(chosen),
        sole_occupied_neighbor=sole,
        accessible_influence=accessible_influence,
        remote_influence=tuple(chosen_influence),
        max_probability_mass_error=float(
            max(errors) if errors else 0.0
        ),
    )


def apply_history(
    checkpoint: ch18.MaterialCrystalState,
    cells: Sequence[Cell],
) -> HistoryState:
    state = from_checkpoint(
        checkpoint
    )

    state.material_strength = {
        cell: float(
            INITIAL_HISTORY_STRENGTH
        )
        for cell in cells
    }

    state.material_mass_by_step = [
        material_mass(state)
    ]

    return state


def build_history_states_v2(
    probe: Probe,
    placement: HistoryPlacementV2,
) -> Dict[str, HistoryState]:
    accessible = apply_history(
        probe.checkpoint,
        placement.accessible_cells,
    )

    remote = apply_history(
        probe.checkpoint,
        placement.remote_cells,
    )

    erased = from_checkpoint(
        probe.checkpoint
    )

    if abs(
        material_mass(accessible)
        - material_mass(remote)
    ) > ASSERT_TOL:
        raise RuntimeError(
            "Initial material mass mismatch."
        )

    return {
        "accessible": accessible,
        "remote": remote,
        "erased": erased,
    }


# ============================================================================
# Corrected controlled growth
# ============================================================================

def growth_step_controlled(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
    blocked_cell: Cell | None = None,
) -> Tuple[
    HistoryState,
    List[Cell],
]:
    occupied = set(
        state.occupied
    )

    birth_time = dict(
        state.birth_time
    )

    material_strength = dict(
        state.material_strength
    )

    frontier = frontier_cells(
        state,
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

    additions = []

    for cell in frontier:
        p = attachment_probability(
            cell,
            state,
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
        occupied.add(cell)
        birth_time[cell] = next_step

    out = HistoryState(
        occupied=occupied,
        birth_time=birth_time,
        material_strength=material_strength,
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
        material_mass_by_step=(
            list(state.material_mass_by_step)
            + [material_mass(state)]
        ),
    )

    return (
        out,
        additions,
    )


def canonical_step_controlled(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
    loss_rate: float,
    blocked_cell: Cell | None = None,
):
    grown, additions = (
        growth_step_controlled(
            state,
            input_value,
            radius,
            crystal_params,
            offset,
            blocked_cell=blocked_cell,
        )
    )

    after_loss, lost = (
        v1.apply_background_loss(
            grown,
            loss_rate,
        )
    )

    decayed = v1.decay_material(
        after_loss
    )

    return (
        decayed,
        additions,
        lost,
    )


# ============================================================================
# Intervention + reference
# ============================================================================

@dataclass
class Branches:
    force: HistoryState
    prevent: HistoryState


def make_branches_v2(
    history_state: HistoryState,
    x: Cell,
) -> Branches:
    prevent = clone_state(
        history_state
    )

    if x in prevent.occupied:
        raise RuntimeError(
            "Probe x must be empty before intervention."
        )

    force = clone_state(
        history_state
    )

    force.occupied.add(x)
    force.birth_time[x] = int(
        force.step
    )
    force.material_strength.pop(
        x,
        None,
    )

    return Branches(
        force=force,
        prevent=prevent,
    )


def build_reference_targets_v2(
    probe: Probe,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
):
    state = from_checkpoint(
        probe.checkpoint
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
            probe.future_env[lag]
        )

        target = expected_attachments(
            state,
            input_value,
            radius,
            crystal_params,
            0.0,
        )

        targets.append(
            float(target)
        )

        (
            state,
            _add,
            _lost,
        ) = canonical_step_controlled(
            state,
            input_value,
            radius,
            crystal_params,
            0.0,
            loss_rate,
            blocked_cell=(
                probe.cell
                if lag == 1
                else None
            ),
        )

    return targets


# ============================================================================
# Exact expected local causal increment
# ============================================================================

def expected_local_difference(
    force: HistoryState,
    prevent: HistoryState,
    input_value: float,
    x: Cell,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
    blocked_prevent_x: bool,
) -> float:
    ff = set(
        frontier_cells(
            force,
            radius,
        )
    )

    pf = set(
        frontier_cells(
            prevent,
            radius,
        )
    )

    if blocked_prevent_x:
        pf.discard(x)

    total = 0.0

    for cell in ff | pf:
        if cell == x:
            continue

        d = v4.relative_distance(
            cell,
            x,
        )

        if not (
            1
            <= d
            <= HORIZON
        ):
            continue

        p_force = (
            attachment_probability(
                cell,
                force,
                input_value,
                crystal_params,
                offset,
            )
            if cell in ff
            else 0.0
        )

        p_prevent = (
            attachment_probability(
                cell,
                prevent,
                input_value,
                crystal_params,
                offset,
            )
            if cell in pf
            else 0.0
        )

        total += (
            p_force
            - p_prevent
        )

    return float(total)


def exact_E1_ring1(
    force: HistoryState,
    prevent: HistoryState,
    input_value: float,
    x: Cell,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    ff = set(
        frontier_cells(
            force,
            radius,
        )
    )

    pf = set(
        frontier_cells(
            prevent,
            radius,
        )
    )

    pf.discard(x)

    total = 0.0

    for cell in ff | pf:
        if cell == x:
            continue

        if (
            v4.relative_distance(
                cell,
                x,
            )
            > 1
        ):
            continue

        pfv = (
            attachment_probability(
                cell,
                force,
                input_value,
                crystal_params,
                offset,
            )
            if cell in ff
            else 0.0
        )

        ppv = (
            attachment_probability(
                cell,
                prevent,
                input_value,
                crystal_params,
                offset,
            )
            if cell in pf
            else 0.0
        )

        total += (
            pfv
            - ppv
        )

    return float(total)


# ============================================================================
# Run one arm
# ============================================================================

@dataclass
class PerLagRow:
    group: int
    probe_index: int
    history_arm: str
    lag: int

    target_expected_attachments: float
    offset: float
    calibration_valid: bool

    prevent_expected_attachments: float
    force_expected_attachments: float
    prevent_relative_error: float

    expected_local_causal_increment: float

    prevent_realized_attachments: int
    force_realized_attachments: int

    prevent_frontier_size: int
    force_frontier_size: int

    prevent_material_mass: float
    force_material_mass: float

    prevent_x_blocked: bool
    prevent_x_attached: bool
    force_x_present_before_growth: bool
    force_x_present_after_cleanup: bool


@dataclass
class ArmResult:
    group: int
    probe_index: int
    q: int
    r: int
    history_arm: str

    RB_G_local: float
    G_local_realized: float
    G_global_realized: float

    E1_ring1: float

    max_prevent_relative_error: float
    mean_abs_prevent_relative_error: float

    mean_offset: float
    max_abs_offset: float


def run_arm(
    probe: Probe,
    history_state: HistoryState,
    arm: str,
    reference_targets: Sequence[float],
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    ArmResult,
    List[PerLagRow],
]:
    branches = make_branches_v2(
        history_state,
        probe.cell,
    )

    force = branches.force
    prevent = branches.prevent

    x = probe.cell

    radius = int(
        source_profile["radius"]
    )

    loss_rate = float(
        source_profile["loss_rate"]
    )

    RB_total = 0.0
    G_local = 0.0
    G_global = 0.0

    lag_rows = []
    abs_errors = []
    offsets = []

    E1 = None

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
            ]
        )

        blocked_prevent_x = (
            lag == 1
        )

        # PREVENT matching must exclude x at lag 1, because x is explicitly
        # blocked by the corrected intervention.
        if arm == "erased":
            offset = 0.0

            prevent_frontier = frontier_cells(
                prevent,
                radius,
            )

            if blocked_prevent_x:
                prevent_frontier = [
                    c
                    for c in prevent_frontier
                    if c != x
                ]

            prevent_expected = float(
                sum(
                    attachment_probability(
                        c,
                        prevent,
                        input_value,
                        crystal_params,
                        0.0,
                    )
                    for c
                    in prevent_frontier
                )
            )

            solved = True

        else:
            # Solve against a temporary PREVENT state expectation with x
            # explicitly omitted at lag 1.
            frontier = frontier_cells(
                prevent,
                radius,
            )

            if blocked_prevent_x:
                frontier = [
                    c
                    for c in frontier
                    if c != x
                ]

            def eval_offset(
                off: float,
            ) -> float:
                return float(
                    sum(
                        attachment_probability(
                            c,
                            prevent,
                            input_value,
                            crystal_params,
                            off,
                        )
                        for c
                        in frontier
                    )
                )

            lo = v1.CALIBRATION_OFFSET_MIN
            hi = v1.CALIBRATION_OFFSET_MAX

            e_lo = eval_offset(lo)
            e_hi = eval_offset(hi)

            if (
                target < e_lo
                or target > e_hi
            ):
                solved = False
                offset = float("nan")
                prevent_expected = float("nan")
            else:
                solved = True

                for _ in range(
                    v1.CALIBRATION_MAX_ITER
                ):
                    mid = (
                        lo + hi
                    ) / 2.0

                    e_mid = eval_offset(mid)

                    if abs(
                        e_mid - target
                    ) <= v1.CALIBRATION_TOLERANCE:
                        lo = mid
                        hi = mid
                        break

                    if e_mid < target:
                        lo = mid
                    else:
                        hi = mid

                offset = (
                    lo + hi
                ) / 2.0

                prevent_expected = eval_offset(
                    offset
                )

        rel_error = (
            abs(
                prevent_expected
                - target
            )
            / max(
                target,
                1e-12,
            )
            if solved
            else float("inf")
        )

        calibration_valid = bool(
            solved
            and rel_error
            <= MATCH_TOLERANCE
        )

        if not calibration_valid:
            raise RuntimeError(
                f"Calibration failure "
                f"group={probe.group} "
                f"probe={probe.probe_index} "
                f"arm={arm} lag={lag}"
            )

        force_expected = expected_attachments(
            force,
            input_value,
            radius,
            crystal_params,
            offset,
        )

        if lag == 1:
            E1 = exact_E1_ring1(
                force,
                prevent,
                input_value,
                x,
                radius,
                crystal_params,
                offset,
            )

        expected_increment = (
            expected_local_difference(
                force,
                prevent,
                input_value,
                x,
                radius,
                crystal_params,
                offset,
                blocked_prevent_x=(
                    blocked_prevent_x
                ),
            )
        )

        RB_total += expected_increment

        force_x_present_before = bool(
            x in force.occupied
        )

        prevent_frontier_before = set(
            frontier_cells(
                prevent,
                radius,
            )
        )

        (
            force,
            force_add,
            _force_lost,
        ) = canonical_step_controlled(
            force,
            input_value,
            radius,
            crystal_params,
            offset,
            loss_rate,
            blocked_cell=None,
        )

        (
            prevent,
            prevent_add,
            _prevent_lost,
        ) = canonical_step_controlled(
            prevent,
            input_value,
            radius,
            crystal_params,
            offset,
            loss_rate,
            blocked_cell=(
                x
                if lag == 1
                else None
            ),
        )

        prevent_x_attached = bool(
            x in prevent_add
        )

        force_add_set = {
            c
            for c
            in force_add
            if c != x
        }

        prevent_add_set = {
            c
            for c
            in prevent_add
            if c != x
        }

        force_local = sum(
            1
            <= v4.relative_distance(
                c,
                x,
            )
            <= HORIZON
            for c
            in force_add_set
        )

        prevent_local = sum(
            1
            <= v4.relative_distance(
                c,
                x,
            )
            <= HORIZON
            for c
            in prevent_add_set
        )

        G_local += float(
            force_local
            - prevent_local
        )

        G_global += float(
            len(force_add_set)
            - len(prevent_add_set)
        )

        # After exactly one growth exposure, remove x from FORCE.
        if lag == 1:
            force.occupied.discard(x)
            force.birth_time.pop(
                x,
                None,
            )
            force.material_strength.pop(
                x,
                None,
            )

            prevent.occupied.discard(x)
            prevent.birth_time.pop(
                x,
                None,
            )
            prevent.material_strength.pop(
                x,
                None,
            )

            if force.population_by_step:
                force.population_by_step[-1] = len(
                    force.occupied
                )

            if prevent.population_by_step:
                prevent.population_by_step[-1] = len(
                    prevent.occupied
                )

        force_x_after_cleanup = bool(
            x in force.occupied
        )

        if lag == 1:
            if prevent_x_attached:
                raise RuntimeError(
                    "Corrected PREVENT allowed x to attach."
                )

            if not force_x_present_before:
                raise RuntimeError(
                    "FORCE x missing before first causal exposure."
                )

            if (
                x in prevent.occupied
                or x in force.occupied
            ):
                raise RuntimeError(
                    "x remained after intervention cleanup."
                )

        lag_rows.append(
            PerLagRow(
                group=int(
                    probe.group
                ),
                probe_index=int(
                    probe.probe_index
                ),
                history_arm=arm,
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
                expected_local_causal_increment=float(
                    expected_increment
                ),
                prevent_realized_attachments=int(
                    len(
                        prevent_add_set
                    )
                ),
                force_realized_attachments=int(
                    len(
                        force_add_set
                    )
                ),
                prevent_frontier_size=int(
                    len(
                        prevent_frontier_before
                    )
                ),
                force_frontier_size=int(
                    len(
                        frontier_cells(
                            force,
                            radius,
                        )
                    )
                ),
                prevent_material_mass=float(
                    material_mass(
                        prevent
                    )
                ),
                force_material_mass=float(
                    material_mass(
                        force
                    )
                ),
                prevent_x_blocked=bool(
                    lag == 1
                ),
                prevent_x_attached=bool(
                    prevent_x_attached
                ),
                force_x_present_before_growth=bool(
                    force_x_present_before
                ),
                force_x_present_after_cleanup=bool(
                    force_x_after_cleanup
                ),
            )
        )

        abs_errors.append(
            rel_error
        )

        offsets.append(
            offset
        )

    if E1 is None:
        raise RuntimeError(
            "Missing E1."
        )

    return (
        ArmResult(
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
            history_arm=arm,
            RB_G_local=float(
                RB_total
            ),
            G_local_realized=float(
                G_local
            ),
            G_global_realized=float(
                G_global
            ),
            E1_ring1=float(
                E1
            ),
            max_prevent_relative_error=float(
                max(
                    abs_errors
                )
            ),
            mean_abs_prevent_relative_error=float(
                np.mean(
                    abs_errors
                )
            ),
            mean_offset=float(
                np.mean(
                    offsets
                )
            ),
            max_abs_offset=float(
                max(
                    abs(v)
                    for v
                    in offsets
                )
            ),
        ),
        lag_rows,
    )


# ============================================================================
# Probe preparation
# ============================================================================

def prepare_probes(
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
):
    raw_probes, support = (
        ch26.prepare_probes(
            profile,
            source_profile,
            crystal_params,
            seed,
        )
    )

    probes = [
        Probe(
            group=int(p.group),
            probe_index=int(
                p.probe_index
            ),
            cell=p.cell,
            checkpoint=p.checkpoint,
            future_env=p.future_env,
        )
        for p
        in raw_probes
    ]

    return (
        probes,
        support,
    )


# ============================================================================
# Aggregation
# ============================================================================

def group_mean_map(
    rows: Sequence[ArmResult],
    arm: str,
    getter,
) -> Dict[int, float]:
    buckets = {}

    for row in rows:
        if row.history_arm != arm:
            continue

        buckets.setdefault(
            row.group,
            [],
        ).append(
            float(
                getter(row)
            )
        )

    return {
        g: float(
            np.mean(vals)
        )
        for g, vals
        in buckets.items()
        if vals
    }


def paired_group_difference(
    rows: Sequence[ArmResult],
    arm_a: str,
    arm_b: str,
    getter,
) -> List[float]:
    a = group_mean_map(
        rows,
        arm_a,
        getter,
    )

    b = group_mean_map(
        rows,
        arm_b,
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


def group_arm_vectors(
    rows: Sequence[ArmResult],
    arm_a: str,
    arm_b: str,
    getter,
):
    a = group_mean_map(
        rows,
        arm_a,
        getter,
    )

    b = group_mean_map(
        rows,
        arm_b,
        getter,
    )

    common = sorted(
        set(a)
        & set(b)
    )

    av = [
        a[g]
        for g in common
    ]

    bv = [
        b[g]
        for g in common
    ]

    return (
        common,
        av,
        bv,
    )


# ============================================================================
# Validity
# ============================================================================

def validity_report(
    arm_results: Sequence[ArmResult],
    lag_rows: Sequence[PerLagRow],
    support: dict,
    matching_details: Sequence[dict],
) -> dict:
    relevant = [
        row
        for row in lag_rows
        if row.history_arm
        in {
            "accessible",
            "remote",
        }
    ]

    record_pass = float(
        np.mean(
            [
                row.calibration_valid
                for row in relevant
            ]
        )
    ) if relevant else 0.0

    population_gate = True
    per_arm_lag = {}

    for arm in [
        "accessible",
        "remote",
    ]:
        per_arm_lag[arm] = {}

        for lag in range(
            1,
            HORIZON + 1,
        ):
            vals = [
                row.prevent_relative_error
                for row in relevant
                if (
                    row.history_arm == arm
                    and row.lag == lag
                )
            ]

            mean = float(
                np.mean(vals)
            ) if vals else float(
                "nan"
            )

            within = bool(
                math.isfinite(mean)
                and abs(mean)
                <= MATCH_TOLERANCE
            )

            if not within:
                population_gate = False

            per_arm_lag[arm][
                str(lag)
            ] = {
                "mean_relative_error": mean,
                "within_2pct": within,
            }

    intervention_ok = all(
        (
            not row.prevent_x_attached
            and (
                row.force_x_present_before_growth
                if row.lag == 1
                else True
            )
            and (
                not row.force_x_present_after_cleanup
                if row.lag == 1
                else True
            )
        )
        for row in lag_rows
        if row.lag == 1
    )

    matching_ok = all(
        float(
            row[
                "max_probability_mass_error"
            ]
        )
        <= REMOTE_INFLUENCE_MASS_TOL
        + ASSERT_TOL
        for row in matching_details
    )

    coverage = float(
        support[
            "coverage_fraction"
        ]
    )

    valid = bool(
        record_pass
        >= MIN_RECORD_MATCH_FRACTION
        and population_gate
        and intervention_ok
        and matching_ok
        and coverage
        >= MIN_GROUP_COVERAGE
    )

    return {
        "record_level_match_pass_fraction": record_pass,
        "required_record_level_fraction": MIN_RECORD_MATCH_FRACTION,
        "population_mean_every_arm_lag_within_2pct": population_gate,
        "intervention_assertions_pass": intervention_ok,
        "remote_matching_pass": matching_ok,
        "group_coverage_fraction": coverage,
        "required_group_coverage": MIN_GROUP_COVERAGE,
        "per_arm_lag": per_arm_lag,
        "scientific_valid": valid,
        "status": (
            "PASS"
            if valid
            else "FAIL"
        ),
    }


# ============================================================================
# IO / reporter
# ============================================================================

def write_raw(
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
                asdict(row)
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
    ):
        path = (
            self.root
            / "ch27-decaying-material-history-causal-response-v2-full-report.md"
        )

        parts = [
            "# Chapter 27 — Stored Material History and Downstream Causal Consequence (V2)",
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
        default=20260915,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch27-decaying-material-history-causal-response-v2"
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
        "seed": int(args.seed),
        "fresh_seed": bool(
            args.seed
            not in {
                20260909,
                20260910,
                20260911,
                20260912,
                20260913,
                20260914,
            }
        ),
        "horizon": HORIZON,
        "primary_SEI": PRIMARY_SEI,
        "history_k": HISTORY_K,
        "local_history_radius": LOCAL_HISTORY_RADIUS,
        "remote_min_distance": HORIZON + REMOTE_MARGIN,
        "remote_influence_mass_tolerance": REMOTE_INFLUENCE_MASS_TOL,
        "history_half_life": HISTORY_HALF_LIFE,
        "history_age": HISTORY_AGE,
        "material_gain": MATERIAL_GAIN,
        "primary_estimator": (
            "lag-wise Rao-Blackwellized expected local causal consequence"
        ),
        "realized_secondary": True,
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
        "primary_contrast": (
            "RB_G_local(accessible) - RB_G_local(remote)"
        ),
        "SEI_abs": PRIMARY_SEI,
        "construct_validity_fixes": [
            "PREVENT explicitly blocks x during lag 1",
            "FORCE contains x for exactly lag-1 growth exposure",
            "remote carrier influence matched to accessible carriers",
            "Rao-Blackwellized local expected consequence is primary",
        ],
        "frozen_from_v1": {
            "history_k": HISTORY_K,
            "half_life": HISTORY_HALF_LIFE,
            "age": HISTORY_AGE,
            "material_gain": MATERIAL_GAIN,
            "horizon": HORIZON,
            "allocation": "true_unbounded",
            "dynamic_prevent_matching": True,
        },
        "stop_rule": (
            "No parameter changes after full run. "
            "Increase groups only if unresolved solely from MDE."
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen V2 Protocol",
        protocol,
    )

    reporter.save_json(
        "stage-00-protocol.json",
        protocol,
    )

    raw_probes, initial_support = (
        prepare_probes(
            profile,
            source_profile,
            crystal_params,
            args.seed,
        )
    )

    supported = []
    placements = {}
    matching_details = []
    supported_groups = set()

    for probe in raw_probes:
        placement = (
            build_history_placement_v2(
                probe,
                source_profile,
                crystal_params,
            )
        )

        if placement is None:
            continue

        supported.append(
            probe
        )

        supported_groups.add(
            probe.group
        )

        key = (
            probe.group,
            probe.probe_index,
        )

        placements[key] = placement

        matching_details.append({
            "group": int(
                probe.group
            ),
            "probe_index": int(
                probe.probe_index
            ),
            "accessible_cells": [
                list(c)
                for c in placement.accessible_cells
            ],
            "remote_cells": [
                list(c)
                for c in placement.remote_cells
            ],
            "accessible_frontier_counts": [
                inf.frontier_count
                for inf
                in placement.accessible_influence
            ],
            "remote_frontier_counts": [
                inf.frontier_count
                for inf
                in placement.remote_influence
            ],
            "accessible_probability_mass": [
                inf.probability_mass
                for inf
                in placement.accessible_influence
            ],
            "remote_probability_mass": [
                inf.probability_mass
                for inf
                in placement.remote_influence
            ],
            "max_probability_mass_error": (
                placement.max_probability_mass_error
            ),
            "initial_material_mass": (
                HISTORY_K
                * INITIAL_HISTORY_STRENGTH
            ),
        })

    support = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "initial_probe_support": initial_support,
        "groups_with_supported_probe": int(
            len(
                supported_groups
            )
        ),
        "coverage_fraction": float(
            len(
                supported_groups
            )
            / max(
                1,
                int(
                    profile[
                        "groups"
                    ]
                ),
            )
        ),
        "supported_probes": int(
            len(
                supported
            )
        ),
        "remote_matching_outcome_blind": True,
    }

    reporter.stage(
        "stage-01-support.md",
        "Stage 1 — Probe and Remote-Matching Support",
        support,
    )

    reporter.save_json(
        "stage-01-support.json",
        support,
    )

    reporter.save_json(
        "history-matching-details.json",
        {
            "matches": matching_details
        },
    )

    if not supported:
        raise RuntimeError(
            "No supported V2 probes."
        )

    arm_results = []
    lag_rows = []

    for probe in tqdm(
        supported,
        desc="Chapter 27 V2",
    ):
        placement = placements[
            (
                probe.group,
                probe.probe_index,
            )
        ]

        histories = (
            build_history_states_v2(
                probe,
                placement,
            )
        )

        reference_targets = (
            build_reference_targets_v2(
                probe,
                source_profile,
                crystal_params,
            )
        )

        for arm in ARMS:
            result, per_lag = (
                run_arm(
                    probe,
                    histories[
                        arm
                    ],
                    arm,
                    reference_targets,
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

    write_raw(
        reporter.root
        / "raw-v2-arm-results.jsonl",
        reporter.root
        / "raw-v2-arm-results.csv",
        arm_results,
    )

    write_raw(
        reporter.root
        / "raw-v2-per-lag.jsonl",
        reporter.root
        / "raw-v2-per-lag.csv",
        lag_rows,
    )

    validity = validity_report(
        arm_results,
        lag_rows,
        support,
        matching_details,
    )

    reporter.stage(
        "stage-02-validity.md",
        "Stage 2 — Construct and Dynamic-Matching Validity",
        validity,
    )

    reporter.save_json(
        "stage-02-validity.json",
        validity,
    )

    # Arm profiles.
    arm_profiles = {}

    for idx, arm in enumerate(
        ARMS
    ):
        arm_profiles[arm] = {}

        for name, getter in [
            (
                "RB_G_local",
                lambda r:
                r.RB_G_local,
            ),
            (
                "G_local_realized",
                lambda r:
                r.G_local_realized,
            ),
            (
                "E1_ring1",
                lambda r:
                r.E1_ring1,
            ),
            (
                "mean_offset",
                lambda r:
                r.mean_offset,
            ),
        ]:
            mapping = group_mean_map(
                arm_results,
                arm,
                getter,
            )

            arm_profiles[arm][
                name
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
                + 1000
                + idx * 100
                + len(
                    arm_profiles[
                        arm
                    ]
                ),
            )

    reporter.stage(
        "stage-03-arm-profiles.md",
        "Stage 3 — Arm Profiles",
        arm_profiles,
    )

    reporter.save_json(
        "stage-03-arm-profiles.json",
        arm_profiles,
    )

    # Primary.
    primary_diff = (
        paired_group_difference(
            arm_results,
            "accessible",
            "remote",
            lambda r:
            r.RB_G_local,
        )
    )

    primary_summary = (
        bootstrap_mean_ci(
            primary_diff,
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

    primary = {
        "contrast": (
            "RB_G_local(accessible) - RB_G_local(remote)"
        ),
        "SEI_abs": PRIMARY_SEI,
        "result": primary_summary,
        "status": p_status,
    }

    reporter.stage(
        "stage-04-primary.md",
        "Stage 4 — Primary Rao-Blackwellized History Effect",
        primary,
    )

    reporter.save_json(
        "stage-04-primary.json",
        primary,
    )

    # Secondary realized and immediate.
    realized_diff = (
        paired_group_difference(
            arm_results,
            "accessible",
            "remote",
            lambda r:
            r.G_local_realized,
        )
    )

    E1_diff = (
        paired_group_difference(
            arm_results,
            "accessible",
            "remote",
            lambda r:
            r.E1_ring1,
        )
    )

    _, av_real, rv_real = (
        group_arm_vectors(
            arm_results,
            "accessible",
            "remote",
            lambda r:
            r.G_local_realized,
        )
    )

    secondary = {
        "realized_G_local_accessible_minus_remote": (
            bootstrap_mean_ci(
                realized_diff,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6000,
            )
        ),
        "E1_ring1_accessible_minus_remote": (
            bootstrap_mean_ci(
                E1_diff,
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6001,
            )
        ),
        "CRN_pairing_realized_G": {
            "corr_accessible_remote": corr(
                av_real,
                rv_real,
            )
        },
        "remote_minus_erased": {
            "RB_G_local": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "remote",
                    "erased",
                    lambda r:
                    r.RB_G_local,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6100,
            ),
            "E1_ring1": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "remote",
                    "erased",
                    lambda r:
                    r.E1_ring1,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6101,
            ),
        },
        "accessible_minus_erased": {
            "RB_G_local": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "erased",
                    lambda r:
                    r.RB_G_local,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6200,
            ),
        },
    }

    reporter.stage(
        "stage-05-secondary.md",
        "Stage 5 — Secondary Realized and Immediate Effects",
        secondary,
    )

    reporter.save_json(
        "stage-05-secondary.json",
        secondary,
    )

    # Matching quality.
    match_errors = [
        float(
            row[
                "max_probability_mass_error"
            ]
        )
        for row
        in matching_details
    ]

    matching_summary = {
        "n_supported_probes": int(
            len(
                matching_details
            )
        ),
        "max_probability_mass_error": float(
            max(
                match_errors
            )
            if match_errors
            else float(
                "nan"
            )
        ),
        "mean_probability_mass_error": float(
            np.mean(
                match_errors
            )
            if match_errors
            else float(
                "nan"
            )
        ),
        "tolerance": (
            REMOTE_INFLUENCE_MASS_TOL
        ),
    }

    reporter.stage(
        "stage-06-remote-match.md",
        "Stage 6 — Remote Carrier Matching Quality",
        matching_summary,
    )

    reporter.save_json(
        "stage-06-remote-match.json",
        matching_summary,
    )

    # Verdict.
    if not profile[
        "scientific"
    ]:
        overall = (
            "ENGINEERING_SMOKE_ONLY"
        )
        bounded = (
            "Smoke profile only."
        )

    elif not validity[
        "scientific_valid"
    ]:
        overall = (
            "INVALID"
        )
        bounded = (
            "Construct-validity or dynamic-matching gate failed."
        )

    elif p_status == "SUPPORTED":
        overall = (
            "ACCESSIBLE_MATERIAL_HISTORY_CHANGES_DOWNSTREAM_CAUSAL_CONSEQUENCE"
        )
        bounded = (
            "With visible geometry, material amount, remote carrier baseline "
            "influence, allocation policy and dynamically matched PREVENT "
            "background construction controlled, locally accessible decaying "
            "material state changed mean finite-horizon expected local causal "
            "consequence by at least the frozen meaningful scale."
        )

    elif p_status == "BOUNDED_NEAR_ZERO":
        overall = (
            "DOWNSTREAM_MATERIAL_HISTORY_EFFECT_BOUNDED_NEAR_ZERO"
        )
        bounded = (
            "Under the frozen corrected V2 protocol, accessible versus remote "
            "decaying material state changed mean finite-horizon expected local "
            "causal consequence by less than the predeclared +/-0.15 scale."
        )

    else:
        overall = (
            "DOWNSTREAM_MATERIAL_HISTORY_EFFECT_UNRESOLVED"
        )
        bounded = (
            "The corrected experiment did not resolve the finite-horizon "
            "expected local causal consequence at the frozen +/-0.15 scale."
        )

    verdict = {
        "validity": validity,
        "primary_status": p_status,
        "overall_status": overall,
        "bounded_claim": bounded,
        "V1_immediate_result_role": (
            "Prior valid evidence; not re-promoted by V2."
        ),
        "not_established": [
            "self-generated memory",
            "learning",
            "adaptation",
            "semantic memory",
            "individuality",
            "organism",
            "life",
        ],
        "stop_rule": (
            "No parameter rescue. Increase groups only if unresolved solely "
            "because achieved MDE exceeds the frozen SEI."
        ),
    }

    reporter.stage(
        "stage-07-verdict.md",
        "Stage 7 — Chapter 27 V2 Verdict",
        verdict,
    )

    reporter.save_json(
        "stage-07-verdict.json",
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
