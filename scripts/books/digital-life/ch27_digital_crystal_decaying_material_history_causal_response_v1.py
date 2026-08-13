#!/usr/bin/env python3
"""
Digital Life — Chapter 27 V1
Can Stored Material History Change a Causal Response?
=====================================================

SCIENTIFIC QUESTION
-------------------

At the SAME present occupancy geometry, SAME probe geometry, SAME allocation
policy, SAME future environment, and dynamically matched PREVENT background
construction rate:

    can a decaying persistent material trace change the causal consequence
    of the same transient local perturbation?

This is the first chapter in which "history" is given an independent causal
state channel while PRESENT OCCUPANCY is held fixed.

WHY THIS IS DIFFERENT FROM CHAPTER 24 V3
----------------------------------------

Chapter 24 V3 tried to test recent history while material memory was OFF.
The dynamics were Markov in present occupancy, so "history" had no independent
causal variable through which to act.

Chapter 27 introduces one explicitly:

    material_strength[cell] > 0

The material trace:
    - is stored on occupied cells;
    - decays with a frozen half-life;
    - biases attachment probability through modified-neighbour influence;
    - does NOT alter present occupancy at the moment histories are compared;
    - does NOT propagate to newly attached cells in V1.

The experiment therefore compares:

    SAME VISIBLE GEOMETRY
    DIFFERENT STORED MATERIAL STATE

HISTORY ARMS
------------

For every supported n=1 frontier probe x:

1. ACCESSIBLE_HISTORY

   Write the same-strength material trace onto exactly K occupied cells close
   to x.

   The sole occupied neighbour of x is always included.

2. REMOTE_HISTORY

   Write the SAME number of cells with the SAME strength, but place them more
   than H + REMOTE_MARGIN cells away from x.

   Therefore the material trace cannot reach the local H-step outcome cone
   through nearest-neighbour propagation during the experiment.

3. ERASED

   No material trace.

   This is secondary only and provides a no-history reference.

ACCESSIBLE vs REMOTE is the PRIMARY scientific contrast.

Both material-history arms have:

    exact same occupied set
    exact same birth times
    exact same total initial material mass
    exact same trace age
    exact same decay law

Only spatial causal accessibility differs.

THIS IS A WRITE-ONLY HISTORY ENCODING
-------------------------------------

V1 deliberately writes the material trace without changing occupancy.

This is not claimed to be a naturally self-generated memory.

It is an experimental history channel.

The purpose is narrower:

    if stored state is present while visible geometry is held fixed,
    can that state change later causal response?

If the answer is no, there is no reason yet to build a more elaborate
experience encoder.

FINITE MEMORY TIMESCALE
-----------------------

The trace is NOT permanent.

Frozen:

    HISTORY_HALF_LIFE = 6 updates
    HISTORY_AGE       = 3 updates

Initial test-time strength:

    s0 = 2^(-HISTORY_AGE / HISTORY_HALF_LIFE)

After every continuation update:

    strength *= 2^(-1 / HISTORY_HALF_LIFE)

Lost cells lose their material trace.

Newly attached cells inherit no material state in V1.

This creates a finite causal-access window instead of a permanent structural
label.

MATERIAL CAUSAL TERM
--------------------

For frontier candidate y:

    material_exposure(y)
        = sum(material_strength[nb] for nb in neighbours(y))

Attachment score:

    score =
        frozen Digital Crystal v1 score
        + MATERIAL_GAIN * material_exposure(y)
        + calibration_offset

Frozen:

    MATERIAL_GAIN = 0.30

This reuses the Chapter 18 material-neighbour effect scale.

IMPORTANT:
The existence of this score term means that "material can alter attachment
probability" is part of the MODEL DEFINITION, not a scientific discovery.

The scientific question is whether a matched stored-history difference changes
the RESPONSE TO THE SAME PERTURBATION, especially finite-horizon G_T.

ALLOCATION POLICY
-----------------

Chapter 27 uses TRUE UNBOUNDED evaluation only.

Every current frontier candidate is evaluated.

Why?

Chapter 25 established that finite candidate selection creates its own
non-local redistribution pathway.

Chapter 27 is about material history, so V1 removes selector competition from
the scientific contrast.

This also means:

    unbounded far selector effect = 0

is a structural assertion, not a finding.

INTERVENTION SURVIVAL BY DESIGN
-------------------------------

Chapter 26 discovered that ~8% of transient probes were annihilated by the
intervention-step loss draw before their causal effect could be expressed.

Chapter 27 removes that dead weight by design.

At time 0:

    PREVENT = history state with x empty
    FORCE   = exact clone + x occupied

The perturbation is inserted AFTER the checkpoint has been formed and BEFORE
the first continuation growth update.

No loss operation is allowed to erase x before that first causal exposure.

After lag 1:

    remove x from FORCE if still occupied

Thus every recruited probe receives one complete causal growth exposure.

This is a protocol definition, not post-hoc survivor conditioning.

DYNAMIC BACKGROUND-CONSTRUCTION MATCHING
----------------------------------------

Material state itself can alter background growth rate.

If ACCESSIBLE and REMOTE histories were allowed to run at different background
construction rates, a G_T difference could be a trivial rate effect.

So Chapter 27 reuses the Chapter 26 V2 discipline.

At every lag tau:

1. A dedicated ERASED PREVENT reference trajectory defines:

       C_target(tau)

   under:
       unbounded evaluation
       material_strength = {}
       calibration_offset = 0

2. For each history arm independently:
   - inspect the CURRENT PREVENT state;
   - evaluate the full frontier;
   - solve ONE additive score offset so PREVENT expected attachments equal
     C_target(tau);
   - apply the SAME offset to that arm's FORCE branch.

FORCE is not independently calibrated.

Therefore:
    background construction is matched;
    causal FORCE-PREVENT response remains free to differ.

VALIDITY GATE
-------------

Frozen PREVENT matching tolerance:

    2%

Scientific validity requires:

    >= 95% of probe x arm x lag records within 2%

AND:

    every population-mean history-arm x lag PREVENT error within +/-2%

AND:

    >= 90% independent-group probe coverage

AND history-placement invariants pass:

    ACCESSIBLE and REMOTE both have exactly HISTORY_K cells
    total initial material mass matches exactly
    REMOTE cells are > H + REMOTE_MARGIN from x
    ACCESSIBLE includes x's sole occupied neighbour

If matching fails:

    INVALID_DYNAMIC_RATE_MATCH

If history placement fails for a probe:
    that probe is unsupported BEFORE outcomes are examined.

PRIMARY OUTCOME
---------------

For each history arm:

    G_T(H)

= cumulative FORCE-minus-PREVENT realized attachment difference within
distance 1..H of x over lags 1..H, excluding x.

Frozen:

    H = 12

PRIMARY HYPOTHESIS H1
---------------------

    Delta_G_history
        =
        G_T(ACCESSIBLE_HISTORY)
        -
        G_T(REMOTE_HISTORY)

Frozen SEI:

    +/- 0.15 attachments

Two-sided statuses:

SUPPORTED
    if |mean Delta_G_history| >= 0.15,
       95% CI excludes 0,
       achieved MDE80 <= 0.15

BOUNDED_NEAR_ZERO
    if full 95% CI lies inside [-0.15,+0.15]
       and achieved MDE80 <= 0.15

UNRESOLVED
    otherwise

INVALID
    if validity gate fails

We do NOT assume in advance whether accessible history amplifies or suppresses
the perturbation.

SECONDARY MEASUREMENTS
----------------------

Mechanism:
    E1_ring1
    E1_global
    material exposure in the ring-1 candidate set
    FORCE/PREVENT expected-construction difference

History persistence:
    total material strength by lag
    accessible material strength near x by lag

Outcome decomposition:
    P(G_T != 0)
    E[G_T | G_T != 0] descriptive only

Controls:
    REMOTE_HISTORY vs ERASED
    ACCESSIBLE_HISTORY vs ERASED

The ERASED comparisons are secondary and do not replace H1.

VISIBLE-GEOMETRY CONTROL
------------------------

At time 0, all three history arms use the exact same:
    occupied set
    birth-time map
    step
    stream seed

Probe geometry is therefore exactly matched.

Because the same probe is reused:
    occupied-neighbour count
    promoted-neighbour count
    shared-neighbour count
    radial position

are identical between history arms automatically.

No statistical matching is needed for those variables.

STOP RULE
---------

If H1 is BOUNDED_NEAR_ZERO:
    close the decaying-material-history response question at +/-0.15 for this
    tested strength, half-life and accessible-placement regime.

If H1 is SUPPORTED:
    Chapter 27 earns a new bounded sentence:
        stored decaying material state can change the causal response of the
        same visible geometry to the same perturbation.

A later experiment may then ask whether different EXPERIENCE ENCODERS can
produce such state naturally.

If UNRESOLVED only because MDE > SEI:
    increase independent groups only.

Do NOT rescue by changing:
    MATERIAL_GAIN
    half-life
    age
    HISTORY_K
    local radius
    remote distance
    horizon
    SEI
    probe geometry
    outcome definition

PROFILES
--------

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

Default:

    20260914

Previous scientific seeds:
    Ch24 V4  20260909
    Ch24 V5  20260910
    Ch25 V1  20260911
    Ch26 V1  20260912
    Ch26 V2  20260913

OUTPUTS
-------

raw-v1-arm-results.jsonl
raw-v1-arm-results.csv
raw-v1-per-lag.jsonl
raw-v1-per-lag.csv

staged JSON/Markdown reports
full Markdown report

DEPENDENCIES
------------

Requires beside this file:

    ch18_digital_crystal_persistent_material_state_v7.py
    ch21_digital_crystal_finite_update_budget_v3.py
    ch24_digital_crystal_frontier_creation_causal_gain_v4.py
    ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py

Chapter 26 V2 is reused for probe/checkpoint selection and statistical helpers.
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


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-decaying-material-history-causal-response-v1"
SCHEMA_VERSION = 1
CHAPTER = 27
CHAPTER_TITLE = "Can Stored Material History Change a Causal Response?"

HORIZON = 12
PRIMARY_SEI = 0.15

HISTORY_K = 2
LOCAL_HISTORY_RADIUS = 3
REMOTE_MARGIN = 3

HISTORY_HALF_LIFE = 6.0
HISTORY_AGE = 3.0
MATERIAL_GAIN = 0.30

INITIAL_HISTORY_STRENGTH = float(
    2.0 ** (
        -HISTORY_AGE
        / HISTORY_HALF_LIFE
    )
)

DECAY_FACTOR = float(
    2.0 ** (
        -1.0
        / HISTORY_HALF_LIFE
    )
)

MATCH_TOLERANCE = 0.02
MIN_RECORD_MATCH_FRACTION = 0.95
MIN_GROUP_COVERAGE = 0.90

CALIBRATION_OFFSET_MIN = -12.0
CALIBRATION_OFFSET_MAX = 12.0
CALIBRATION_TOLERANCE = 1e-10
CALIBRATION_MAX_ITER = 100

ASSERT_TOL = 1e-12

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

HISTORY_ARMS = [
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
        summary[
            "achieved_mde80_one_sided"
        ]
        > PRIMARY_SEI
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

    mean = float(
        summary[
            "mean"
        ]
    )

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
# History state
# ============================================================================

@dataclass
class HistoryState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    material_strength: Dict[Cell, float]
    step: int
    stream_seed: int
    attachments_by_step: List[int]
    population_by_step: List[int]
    material_mass_by_step: List[float]


def clone_state(
    state: HistoryState,
) -> HistoryState:
    return HistoryState(
        occupied=set(
            state.occupied
        ),
        birth_time=dict(
            state.birth_time
        ),
        material_strength=dict(
            state.material_strength
        ),
        step=int(
            state.step
        ),
        stream_seed=int(
            state.stream_seed
        ),
        attachments_by_step=list(
            state.attachments_by_step
        ),
        population_by_step=list(
            state.population_by_step
        ),
        material_mass_by_step=list(
            state.material_mass_by_step
        ),
    )


def from_checkpoint(
    checkpoint: ch18.MaterialCrystalState,
) -> HistoryState:
    return HistoryState(
        occupied=set(
            checkpoint.occupied
        ),
        birth_time=dict(
            checkpoint.birth_time
        ),
        material_strength={},
        step=int(
            checkpoint.step
        ),
        stream_seed=int(
            checkpoint.stream_seed
        ),
        attachments_by_step=list(
            checkpoint.attachments_by_step
        ),
        population_by_step=list(
            checkpoint.population_by_step
        ),
        material_mass_by_step=[0.0],
    )


def material_mass(
    state: HistoryState,
) -> float:
    return float(
        sum(
            max(
                0.0,
                float(v),
            )
            for v
            in state.material_strength.values()
        )
    )


def decay_material(
    state: HistoryState,
) -> HistoryState:
    out = clone_state(
        state
    )

    new_strength = {}

    for cell, strength in out.material_strength.items():
        if cell not in out.occupied:
            continue

        value = float(
            strength
            * DECAY_FACTOR
        )

        if value > 1e-12:
            new_strength[
                cell
            ] = value

    out.material_strength = (
        new_strength
    )

    if out.material_mass_by_step:
        out.material_mass_by_step[
            -1
        ] = material_mass(
            out
        )

    return out


# ============================================================================
# Frozen probability mechanics
# ============================================================================

def attachment_score(
    cell: Cell,
    state: HistoryState,
    input_value: float,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    occupied = set(
        state.occupied
    )

    n = sum(
        nb in occupied
        for nb in ch18.neighbors(
            cell
        )
    )

    theta = (
        ch18.local_exposure_angle(
            cell,
            occupied,
        )
    )

    phase = (
        crystal_params.signal_phase_gain
        * float(
            input_value
        )
    )

    anisotropy = math.cos(
        6.0 * theta
        + phase
    )

    crowding = max(
        0,
        n - 2,
    )

    material_exposure = float(
        sum(
            state.material_strength.get(
                nb,
                0.0,
            )
            for nb
            in ch18.neighbors(
                cell
            )
            if nb in occupied
        )
    )

    return float(
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain
        * float(
            input_value
        )
        + crystal_params.anisotropy_gain
        * anisotropy
        - crystal_params.crowding_penalty
        * crowding
        + MATERIAL_GAIN
        * material_exposure
        + float(
            offset
        )
    )


def attachment_probability(
    cell: Cell,
    state: HistoryState,
    input_value: float,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    return float(
        ch18.logistic_scalar(
            attachment_score(
                cell,
                state,
                input_value,
                crystal_params,
                offset,
            )
        )
    )


def frontier_cells(
    state: HistoryState,
    radius: int,
) -> List[Cell]:
    return v4.frontier_cells(
        set(
            state.occupied
        ),
        radius,
    )


def expected_attachments(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> float:
    frontier = frontier_cells(
        state,
        radius,
    )

    return float(
        sum(
            attachment_probability(
                cell,
                state,
                input_value,
                crystal_params,
                offset,
            )
            for cell
            in frontier
        )
    )


def solve_offset(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    target: float,
) -> Tuple[
    float,
    float,
    bool,
]:
    frontier = frontier_cells(
        state,
        radius,
    )

    if not frontier:
        return (
            0.0,
            0.0,
            abs(
                target
            )
            <= CALIBRATION_TOLERANCE,
        )

    def evaluate(
        offset: float,
    ) -> float:
        return float(
            sum(
                attachment_probability(
                    cell,
                    state,
                    input_value,
                    crystal_params,
                    offset,
                )
                for cell
                in frontier
            )
        )

    lo = (
        CALIBRATION_OFFSET_MIN
    )

    hi = (
        CALIBRATION_OFFSET_MAX
    )

    e_lo = evaluate(
        lo
    )

    e_hi = evaluate(
        hi
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

        e_mid = evaluate(
            mid
        )

        if (
            abs(
                e_mid
                - target
            )
            <= CALIBRATION_TOLERANCE
        ):
            return (
                float(
                    mid
                ),
                float(
                    e_mid
                ),
                True,
            )

        if e_mid < target:
            lo = mid
        else:
            hi = mid

    offset = (
        lo + hi
    ) / 2.0

    achieved = evaluate(
        offset
    )

    return (
        float(
            offset
        ),
        float(
            achieved
        ),
        True,
    )


# ============================================================================
# Growth / loss / decay
# ============================================================================

def growth_step(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> Tuple[
    HistoryState,
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

    material_strength = dict(
        state.material_strength
    )

    frontier = frontier_cells(
        state,
        radius,
    )

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
        occupied.add(
            cell
        )

        birth_time[
            cell
        ] = next_step

    out = HistoryState(
        occupied=occupied,
        birth_time=birth_time,
        material_strength=material_strength,
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
                material_mass(
                    state
                )
            ]
        ),
    )

    return (
        out,
        additions,
    )


def apply_background_loss(
    state: HistoryState,
    loss_rate: float,
) -> Tuple[
    HistoryState,
    List[Cell],
]:
    out = clone_state(
        state
    )

    lost = [
        cell
        for cell in sorted(
            state.occupied
        )
        if (
            ch21.loss_uniform(
                state.stream_seed,
                state.step,
                cell,
            )
            < float(
                loss_rate
            )
        )
    ]

    for cell in lost:
        out.occupied.discard(
            cell
        )

        out.birth_time.pop(
            cell,
            None,
        )

        out.material_strength.pop(
            cell,
            None,
        )

    if out.population_by_step:
        out.population_by_step[
            -1
        ] = len(
            out.occupied
        )

    if out.material_mass_by_step:
        out.material_mass_by_step[
            -1
        ] = material_mass(
            out
        )

    return (
        out,
        lost,
    )


def canonical_step(
    state: HistoryState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
    loss_rate: float,
) -> Tuple[
    HistoryState,
    List[Cell],
    List[Cell],
]:
    grown, additions = (
        growth_step(
            state,
            input_value,
            radius,
            crystal_params,
            offset,
        )
    )

    after_loss, lost = (
        apply_background_loss(
            grown,
            loss_rate,
        )
    )

    decayed = (
        decay_material(
            after_loss
        )
    )

    return (
        decayed,
        additions,
        lost,
    )


# ============================================================================
# Probe preparation
# ============================================================================

@dataclass
class Probe:
    group: int
    probe_index: int
    cell: Cell
    checkpoint: ch18.MaterialCrystalState
    future_env: np.ndarray


def prepare_probes(
    profile: dict,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[Probe],
    dict,
]:
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
            group=int(
                p.group
            ),
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
# History placement
# ============================================================================

@dataclass
class HistoryPlacement:
    accessible_cells: Tuple[
        Cell,
        ...,
    ]
    remote_cells: Tuple[
        Cell,
        ...,
    ]
    sole_occupied_neighbor: Cell


def sole_occupied_neighbor(
    checkpoint: ch18.MaterialCrystalState,
    x: Cell,
) -> Cell | None:
    occupied = set(
        checkpoint.occupied
    )

    nbs = [
        nb
        for nb in ch18.neighbors(
            x
        )
        if nb in occupied
    ]

    if len(nbs) != 1:
        return None

    return nbs[0]


def build_history_placement(
    probe: Probe,
) -> HistoryPlacement | None:
    occupied = set(
        probe.checkpoint.occupied
    )

    x = probe.cell

    sole = (
        sole_occupied_neighbor(
            probe.checkpoint,
            x,
        )
    )

    if sole is None:
        return None

    local_candidates = [
        cell
        for cell
        in occupied
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
            0
            if cell == sole
            else 1,
            v4.relative_distance(
                cell,
                x,
            ),
            cell,
        )
    )

    if len(
        local_candidates
    ) < HISTORY_K:
        return None

    accessible = tuple(
        local_candidates[
            :HISTORY_K
        ]
    )

    if sole not in accessible:
        return None

    min_remote_distance = (
        HORIZON
        + REMOTE_MARGIN
    )

    remote_candidates = [
        cell
        for cell
        in occupied
        if (
            v4.relative_distance(
                cell,
                x,
            )
            > min_remote_distance
            and cell not in accessible
        )
    ]

    remote_candidates.sort(
        key=lambda cell: (
            -v4.relative_distance(
                cell,
                x,
            ),
            cell,
        )
    )

    if len(
        remote_candidates
    ) < HISTORY_K:
        return None

    remote = tuple(
        remote_candidates[
            :HISTORY_K
        ]
    )

    return HistoryPlacement(
        accessible_cells=(
            accessible
        ),
        remote_cells=(
            remote
        ),
        sole_occupied_neighbor=(
            sole
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
        for cell
        in cells
    }

    state.material_mass_by_step = [
        material_mass(
            state
        )
    ]

    return state


def build_history_states(
    probe: Probe,
    placement: HistoryPlacement,
) -> Dict[
    str,
    HistoryState,
]:
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

    ma = material_mass(
        accessible
    )

    mr = material_mass(
        remote
    )

    if abs(
        ma - mr
    ) > ASSERT_TOL:
        raise RuntimeError(
            "Accessible/remote history mass mismatch."
        )

    if (
        len(
            accessible.material_strength
        )
        != HISTORY_K
        or len(
            remote.material_strength
        )
        != HISTORY_K
    ):
        raise RuntimeError(
            "History cell-count invariant failed."
        )

    if (
        placement.sole_occupied_neighbor
        not in accessible.material_strength
    ):
        raise RuntimeError(
            "Accessible history does not include sole occupied neighbour."
        )

    for cell in placement.remote_cells:
        if (
            v4.relative_distance(
                cell,
                probe.cell,
            )
            <= (
                HORIZON
                + REMOTE_MARGIN
            )
        ):
            raise RuntimeError(
                "Remote history violated causal-separation distance."
            )

    return {
        "accessible": accessible,
        "remote": remote,
        "erased": erased,
    }


# ============================================================================
# Guaranteed transient intervention
# ============================================================================

@dataclass
class PreparedBranches:
    force: HistoryState
    prevent: HistoryState


def make_branches(
    history_state: HistoryState,
    x: Cell,
) -> PreparedBranches:
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

    force.occupied.add(
        x
    )

    force.birth_time[
        x
    ] = int(
        force.step
    )

    # No material trace is written onto x.
    force.material_strength.pop(
        x,
        None,
    )

    # Structural intervention-delivery assertions.
    if x not in force.occupied:
        raise RuntimeError(
            "FORCE intervention was not delivered."
        )

    if x in prevent.occupied:
        raise RuntimeError(
            "PREVENT intervention contains x."
        )

    return PreparedBranches(
        force=force,
        prevent=prevent,
    )


# ============================================================================
# Erased reference target trajectory
# ============================================================================

@dataclass
class ReferenceTarget:
    lag: int
    target: float
    prevent_state_before: HistoryState
    prevent_state_after: HistoryState


def build_reference_targets(
    probe: Probe,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> List[
    ReferenceTarget
]:
    state = from_checkpoint(
        probe.checkpoint
    )

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

    targets = []

    for lag in range(
        1,
        HORIZON + 1,
    ):
        input_value = float(
            probe.future_env[
                lag
            ]
        )

        target = (
            expected_attachments(
                state,
                input_value,
                radius,
                crystal_params,
                0.0,
            )
        )

        before = clone_state(
            state
        )

        (
            state,
            _additions,
            _lost,
        ) = canonical_step(
            state,
            input_value,
            radius,
            crystal_params,
            0.0,
            loss_rate,
        )

        targets.append(
            ReferenceTarget(
                lag=int(
                    lag
                ),
                target=float(
                    target
                ),
                prevent_state_before=(
                    before
                ),
                prevent_state_after=(
                    clone_state(
                        state
                    )
                ),
            )
        )

    return targets


# ============================================================================
# Exact lag-1 diagnostics
# ============================================================================

def exact_lag1_difference(
    force: HistoryState,
    prevent: HistoryState,
    input_value: float,
    x: Cell,
    radius: int,
    crystal_params: ch18.CrystalParams,
    offset: float,
) -> dict:
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

    E_ring1 = 0.0
    E_global = 0.0

    force_material_exposure_ring1 = []
    prevent_material_exposure_ring1 = []

    for cell in ff | pf:
        if cell == x:
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

        delta = (
            p_force
            - p_prevent
        )

        E_global += delta

        d = v4.relative_distance(
            cell,
            x,
        )

        if d <= 1:
            E_ring1 += delta

            if cell in ff:
                force_material_exposure_ring1.append(
                    sum(
                        force.material_strength.get(
                            nb,
                            0.0,
                        )
                        for nb
                        in ch18.neighbors(
                            cell
                        )
                        if nb in force.occupied
                    )
                )

            if cell in pf:
                prevent_material_exposure_ring1.append(
                    sum(
                        prevent.material_strength.get(
                            nb,
                            0.0,
                        )
                        for nb
                        in ch18.neighbors(
                            cell
                        )
                        if nb in prevent.occupied
                    )
                )

    return {
        "E1_ring1": float(
            E_ring1
        ),
        "E1_global": float(
            E_global
        ),
        "mean_force_material_exposure_ring1": (
            float(
                np.mean(
                    force_material_exposure_ring1
                )
            )
            if force_material_exposure_ring1
            else 0.0
        ),
        "mean_prevent_material_exposure_ring1": (
            float(
                np.mean(
                    prevent_material_exposure_ring1
                )
            )
            if prevent_material_exposure_ring1
            else 0.0
        ),
    }


# ============================================================================
# Run one history arm
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
    force_relative_difference_from_target: float

    prevent_realized_attachments: int
    force_realized_attachments: int

    prevent_frontier_size: int
    force_frontier_size: int

    prevent_material_mass: float
    force_material_mass: float

    prevent_local_material_mass: float
    force_local_material_mass: float


@dataclass
class ArmResult:
    group: int
    probe_index: int
    q: int
    r: int
    history_arm: str

    G_local: float
    G_global: float
    G_nonzero: int

    E1_ring1: float
    E1_global: float

    mean_force_material_exposure_ring1: float
    mean_prevent_material_exposure_ring1: float

    max_prevent_relative_error: float
    mean_abs_prevent_relative_error: float

    mean_offset: float
    max_abs_offset: float


def local_material_mass(
    state: HistoryState,
    x: Cell,
    radius: int,
) -> float:
    return float(
        sum(
            strength
            for cell, strength
            in state.material_strength.items()
            if (
                v4.relative_distance(
                    cell,
                    x,
                )
                <= radius
            )
        )
    )


def run_arm(
    probe: Probe,
    history_state: HistoryState,
    history_arm: str,
    reference_targets: Sequence[
        ReferenceTarget
    ],
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[
    ArmResult,
    List[
        PerLagRow
    ],
]:
    branches = make_branches(
        history_state,
        probe.cell,
    )

    force = branches.force
    prevent = branches.prevent

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

    local_total = 0.0
    global_total = 0.0

    lag_rows = []
    prevent_abs_errors = []
    offsets = []

    E1 = None

    for lag in range(
        1,
        HORIZON + 1,
    ):
        input_value = float(
            probe.future_env[
                lag
            ]
        )

        target = float(
            reference_targets[
                lag - 1
            ].target
        )

        if history_arm == "erased":
            # Definition/reference assertion.
            offset = 0.0

            prevent_expected = (
                expected_attachments(
                    prevent,
                    input_value,
                    radius,
                    crystal_params,
                    offset,
                )
            )

            # Erased PREVENT should replay reference trajectory exactly.
            if (
                abs(
                    prevent_expected
                    - target
                )
                > ASSERT_TOL
            ):
                raise RuntimeError(
                    "Erased PREVENT reference expectation diverged."
                )

            solved = True

        else:
            (
                offset,
                prevent_expected,
                solved,
            ) = solve_offset(
                prevent,
                input_value,
                radius,
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
            offset = (
                0.0
                if not math.isfinite(
                    offset
                )
                else float(
                    offset
                )
            )

        force_expected = (
            expected_attachments(
                force,
                input_value,
                radius,
                crystal_params,
                offset,
            )
        )

        if lag == 1:
            E1 = (
                exact_lag1_difference(
                    force,
                    prevent,
                    input_value,
                    x,
                    radius,
                    crystal_params,
                    offset,
                )
            )

        prevent_frontier_size = len(
            frontier_cells(
                prevent,
                radius,
            )
        )

        force_frontier_size = len(
            frontier_cells(
                force,
                radius,
            )
        )

        (
            force,
            force_add,
            _force_lost,
        ) = canonical_step(
            force,
            input_value,
            radius,
            crystal_params,
            offset,
            loss_rate,
        )

        (
            prevent,
            prevent_add,
            _prevent_lost,
        ) = canonical_step(
            prevent,
            input_value,
            radius,
            crystal_params,
            offset,
            loss_rate,
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

        # Guarantee exactly one causal growth exposure.
        if lag == 1:
            if x in force.occupied:
                force.occupied.remove(
                    x
                )

                force.birth_time.pop(
                    x,
                    None,
                )

                force.material_strength.pop(
                    x,
                    None,
                )

                if force.population_by_step:
                    force.population_by_step[
                        -1
                    ] = len(
                        force.occupied
                    )

        prevent_local_mass = (
            local_material_mass(
                prevent,
                x,
                HORIZON,
            )
        )

        force_local_mass = (
            local_material_mass(
                force,
                x,
                HORIZON,
            )
        )

        lag_rows.append(
            PerLagRow(
                group=int(
                    probe.group
                ),
                probe_index=int(
                    probe.probe_index
                ),
                history_arm=(
                    history_arm
                ),
                lag=int(
                    lag
                ),
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
                force_relative_difference_from_target=float(
                    (
                        force_expected
                        - target
                    )
                    / max(
                        target,
                        1e-12,
                    )
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
                    prevent_frontier_size
                ),
                force_frontier_size=int(
                    force_frontier_size
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
                prevent_local_material_mass=float(
                    prevent_local_mass
                ),
                force_local_material_mass=float(
                    force_local_mass
                ),
            )
        )

        prevent_abs_errors.append(
            float(
                prevent_rel_error
            )
        )

        offsets.append(
            float(
                offset
            )
        )

    if E1 is None:
        raise RuntimeError(
            "Missing lag-1 diagnostics."
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
            history_arm=(
                history_arm
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
            E1_global=float(
                E1[
                    "E1_global"
                ]
            ),
            mean_force_material_exposure_ring1=float(
                E1[
                    "mean_force_material_exposure_ring1"
                ]
            ),
            mean_prevent_material_exposure_ring1=float(
                E1[
                    "mean_prevent_material_exposure_ring1"
                ]
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
            mean_offset=float(
                np.mean(
                    offsets
                )
                if offsets
                else float(
                    "nan"
                )
            ),
            max_abs_offset=float(
                max(
                    abs(v)
                    for v
                    in offsets
                )
                if offsets
                else float(
                    "nan"
                )
            ),
        ),
        lag_rows,
    )


# ============================================================================
# Aggregation helpers
# ============================================================================

def group_mean_map(
    rows: Sequence[
        ArmResult
    ],
    arm: str,
    getter,
) -> Dict[
    int,
    float,
]:
    buckets: Dict[
        int,
        List[
            float
        ],
    ] = {}

    for row in rows:
        if (
            row.history_arm
            != arm
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
        for group, values
        in buckets.items()
        if values
    }


def paired_group_difference(
    rows: Sequence[
        ArmResult
    ],
    arm_a: str,
    arm_b: str,
    getter,
) -> List[
    float
]:
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
        for g
        in common
    ]


def group_lag_values(
    rows: Sequence[
        PerLagRow
    ],
    arm: str,
    lag: int,
    getter,
) -> List[
    float
]:
    buckets: Dict[
        int,
        List[
            float
        ],
    ] = {}

    for row in rows:
        if (
            row.history_arm
            != arm
            or row.lag
            != lag
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

    return [
        float(
            np.mean(
                vals
            )
        )
        for _, vals
        in sorted(
            buckets.items()
        )
        if vals
    ]


# ============================================================================
# Validity
# ============================================================================

def dynamic_matching_validity(
    lag_rows: Sequence[
        PerLagRow
    ],
    support: dict,
) -> dict:
    scientific_arms = [
        "accessible",
        "remote",
    ]

    relevant_rows = [
        row
        for row
        in lag_rows
        if row.history_arm
        in scientific_arms
    ]

    flags = [
        bool(
            row.calibration_valid
        )
        for row
        in relevant_rows
    ]

    record_pass_fraction = (
        float(
            np.mean(
                flags
            )
        )
        if flags
        else 0.0
    )

    population_gate = True
    per_arm_lag = {}

    for arm in scientific_arms:
        per_arm_lag[
            arm
        ] = {}

        for lag in range(
            1,
            HORIZON + 1,
        ):
            vals = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.prevent_relative_error,
                )
            )

            mean = (
                float(
                    np.mean(
                        vals
                    )
                )
                if vals
                else float(
                    "nan"
                )
            )

            within = bool(
                math.isfinite(
                    mean
                )
                and abs(
                    mean
                )
                <= MATCH_TOLERANCE
            )

            if not within:
                population_gate = (
                    False
                )

            per_arm_lag[
                arm
            ][
                str(
                    lag
                )
            ] = {
                "n_groups": int(
                    len(
                        vals
                    )
                ),
                "mean_relative_error": float(
                    mean
                ),
                "within_2pct": bool(
                    within
                ),
            }

    coverage = float(
        support[
            "coverage_fraction"
        ]
    )

    valid = bool(
        record_pass_fraction
        >= MIN_RECORD_MATCH_FRACTION
        and population_gate
        and coverage
        >= MIN_GROUP_COVERAGE
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
        "probe_group_coverage_fraction": float(
            coverage
        ),
        "required_probe_group_coverage": float(
            MIN_GROUP_COVERAGE
        ),
        "per_arm_lag": (
            per_arm_lag
        ),
        "scientific_valid": bool(
            valid
        ),
        "status": (
            "PASS"
            if valid
            else "FAIL"
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
            / "ch27-decaying-material-history-causal-response-v1-full-report.md"
        )

        parts = [
            "# Chapter 27 — Can Stored Material History Change a Causal Response? (V1)",
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
        default=20260914,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch27-decaying-material-history-causal-response-v1"
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
                20260913,
            }
        ),
        "horizon": (
            HORIZON
        ),
        "primary_SEI": (
            PRIMARY_SEI
        ),
        "history_k": (
            HISTORY_K
        ),
        "local_history_radius": (
            LOCAL_HISTORY_RADIUS
        ),
        "remote_min_distance": (
            HORIZON
            + REMOTE_MARGIN
        ),
        "history_half_life": (
            HISTORY_HALF_LIFE
        ),
        "history_age": (
            HISTORY_AGE
        ),
        "initial_history_strength": (
            INITIAL_HISTORY_STRENGTH
        ),
        "decay_factor_per_update": (
            DECAY_FACTOR
        ),
        "material_gain": (
            MATERIAL_GAIN
        ),
        "allocation_policy": (
            "true_unbounded"
        ),
        "started_at_unix": float(
            time.time()
        ),
    }

    protocol = {
        "role": (
            "DECOUPLED PRESENT-GEOMETRY / MATERIAL-HISTORY CAUSAL RESPONSE TEST"
        ),
        "question": (
            "At matched present occupancy geometry and dynamically matched "
            "background construction, can a decaying persistent material "
            "trace change the causal response to the same perturbation?"
        ),
        "primary_contrast": (
            "G_T(accessible_history) - G_T(remote_history)"
        ),
        "primary_SEI_abs": (
            PRIMARY_SEI
        ),
        "two_sided": True,
        "history_arms": {
            "accessible": (
                f"{HISTORY_K} trace cells within radius "
                f"{LOCAL_HISTORY_RADIUS}; includes sole occupied neighbour"
            ),
            "remote": (
                f"{HISTORY_K} matched trace cells beyond distance "
                f"{HORIZON + REMOTE_MARGIN}"
            ),
            "erased": (
                "secondary no-material reference"
            ),
        },
        "history_state": {
            "half_life_updates": (
                HISTORY_HALF_LIFE
            ),
            "age_at_test_updates": (
                HISTORY_AGE
            ),
            "initial_strength_per_cell": (
                INITIAL_HISTORY_STRENGTH
            ),
            "material_neighbor_gain": (
                MATERIAL_GAIN
            ),
            "transmission": False,
            "new_cell_inheritance": False,
        },
        "visible_geometry_identical_at_t0": True,
        "intervention_survival": (
            "guaranteed by insertion immediately before first causal growth update"
        ),
        "allocation_policy": (
            "true_unbounded, all current frontier cells evaluated"
        ),
        "dynamic_matching": {
            "reference": (
                "dedicated erased PREVENT trajectory with offset 0"
            ),
            "target": (
                "lag-specific expected attachments"
            ),
            "arm_calibration": (
                "solve offset on arm PREVENT every lag; apply same offset to FORCE"
            ),
            "relative_tolerance": (
                MATCH_TOLERANCE
            ),
        },
        "stop_rule": (
            "No parameter rescue after full scientific run."
        ),
        "forbidden_overclaims": [
            "memory",
            "learning",
            "adaptation",
            "homeostasis",
            "formal branching ratio",
            "criticality",
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
        "Stage 0 — Frozen Chapter 27 V1 Protocol",
        protocol,
    )

    reporter.json(
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

    supported_probes = []
    placements = {}

    group_supported = set()

    placement_rows = []

    for probe in raw_probes:
        placement = (
            build_history_placement(
                probe
            )
        )

        if placement is None:
            continue

        key = (
            probe.group,
            probe.probe_index,
        )

        placements[
            key
        ] = placement

        supported_probes.append(
            probe
        )

        group_supported.add(
            probe.group
        )

        placement_rows.append({
            "group": int(
                probe.group
            ),
            "probe_index": int(
                probe.probe_index
            ),
            "q": int(
                probe.cell[
                    0
                ]
            ),
            "r": int(
                probe.cell[
                    1
                ]
            ),
            "accessible_cells": [
                list(
                    c
                )
                for c
                in placement.accessible_cells
            ],
            "remote_cells": [
                list(
                    c
                )
                for c
                in placement.remote_cells
            ],
            "sole_occupied_neighbor": list(
                placement.sole_occupied_neighbor
            ),
            "initial_material_mass_each_history": float(
                HISTORY_K
                * INITIAL_HISTORY_STRENGTH
            ),
            "min_remote_distance": int(
                min(
                    v4.relative_distance(
                        c,
                        probe.cell,
                    )
                    for c
                    in placement.remote_cells
                )
            ),
        })

    support = {
        "requested_groups": int(
            profile[
                "groups"
            ]
        ),
        "initial_probe_support": (
            initial_support
        ),
        "groups_with_history_supported_probe": int(
            len(
                group_supported
            )
        ),
        "coverage_fraction": float(
            len(
                group_supported
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
                supported_probes
            )
        ),
        "history_k": (
            HISTORY_K
        ),
        "local_radius": (
            LOCAL_HISTORY_RADIUS
        ),
        "remote_min_distance": (
            HORIZON
            + REMOTE_MARGIN
        ),
        "placement_outcome_blind": True,
    }

    reporter.stage(
        "stage-01-history-support.md",
        "Stage 1 — History Placement Support",
        support,
    )

    reporter.json(
        "stage-01-history-support.json",
        support,
    )

    reporter.json(
        "history-placement-details.json",
        {
            "placements": (
                placement_rows
            )
        },
    )

    if not supported_probes:
        raise RuntimeError(
            "No supported Chapter 27 probes."
        )

    arm_results = []
    lag_rows = []

    for probe in tqdm(
        supported_probes,
        desc="Chapter 27 material-history arms",
    ):
        placement = placements[
            (
                probe.group,
                probe.probe_index,
            )
        ]

        histories = (
            build_history_states(
                probe,
                placement,
            )
        )

        reference_targets = (
            build_reference_targets(
                probe,
                source_profile,
                crystal_params,
            )
        )

        for arm in HISTORY_ARMS:
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
        / "raw-v1-arm-results.jsonl",
        reporter.root
        / "raw-v1-arm-results.csv",
        arm_results,
    )

    write_raw(
        reporter.root
        / "raw-v1-per-lag.jsonl",
        reporter.root
        / "raw-v1-per-lag.csv",
        lag_rows,
    )

    matching = (
        dynamic_matching_validity(
            lag_rows,
            support,
        )
    )

    scientific_valid = bool(
        matching[
            "scientific_valid"
        ]
    )

    reporter.stage(
        "stage-02-validity.md",
        "Stage 2 — Dynamic Matching Validity",
        matching,
    )

    reporter.json(
        "stage-02-validity.json",
        matching,
    )

    # Per-arm scientific profiles.
    arm_profiles = {}

    for idx, arm in enumerate(
        HISTORY_ARMS
    ):
        def gm(
            getter,
        ):
            mapping = (
                group_mean_map(
                    arm_results,
                    arm,
                    getter,
                )
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
            for r
            in arm_results
            if r.history_arm
            == arm
        ]

        raw_G = np.asarray(
            [
                r.G_local
                for r
                in subset
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
            arm
        ] = {
            "groups": int(
                len(
                    set(
                        r.group
                        for r
                        in subset
                    )
                )
            ),
            "probes": int(
                len(
                    subset
                )
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
                + idx * 50,
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
                + idx * 50,
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
                + idx * 50,
            ),
            "E1_global": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.E1_global
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 103
                + idx * 50,
            ),
            "force_material_exposure_ring1": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.mean_force_material_exposure_ring1
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 104
                + idx * 50,
            ),
            "prevent_material_exposure_ring1": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.mean_prevent_material_exposure_ring1
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 105
                + idx * 50,
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
                + 106
                + idx * 50,
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
                "mean_given_nonzero": (
                    float(
                        np.mean(
                            nz
                        )
                    )
                    if len(
                        nz
                    )
                    else float(
                        "nan"
                    )
                ),
            },
            "mean_offset": bootstrap_mean_ci(
                gm(
                    lambda r:
                    r.mean_offset
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 107
                + idx * 50,
            ),
        }

    reporter.stage(
        "stage-03-arm-profiles.md",
        "Stage 3 — History-Arm Profiles",
        arm_profiles,
    )

    reporter.json(
        "stage-03-arm-profiles.json",
        arm_profiles,
    )

    # Primary history contrast.
    primary_delta = (
        paired_group_difference(
            arm_results,
            "accessible",
            "remote",
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
        p_status = (
            primary_status(
                primary_summary,
                scientific_valid,
            )
        )

    primary_payload = {
        "contrast": (
            "G_T(accessible_history) - G_T(remote_history)"
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
        "stage-04-primary-history-response.md",
        "Stage 4 — Primary Accessible-vs-Remote History Response",
        primary_payload,
    )

    reporter.json(
        "stage-04-primary-history-response.json",
        primary_payload,
    )

    # Secondary mechanistic contrasts.
    secondary = {
        "accessible_minus_remote": {
            "E1_ring1": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "remote",
                    lambda r:
                    r.E1_ring1,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6000,
            ),
            "E1_global": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "remote",
                    lambda r:
                    r.E1_global,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6001,
            ),
            "G_nonzero_rate": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "remote",
                    lambda r:
                    r.G_nonzero,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6002,
            ),
            "force_material_exposure_ring1": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "remote",
                    lambda r:
                    r.mean_force_material_exposure_ring1,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6003,
            ),
        },
        "remote_minus_erased": {
            "G_local": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "remote",
                    "erased",
                    lambda r:
                    r.G_local,
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
            "G_local": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
                    "erased",
                    lambda r:
                    r.G_local,
                ),
                int(
                    profile[
                        "bootstrap_reps"
                    ]
                ),
                args.seed
                + 6200,
            ),
            "E1_ring1": bootstrap_mean_ci(
                paired_group_difference(
                    arm_results,
                    "accessible",
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
                + 6201,
            ),
        },
    }

    reporter.stage(
        "stage-05-secondary-mechanism.md",
        "Stage 5 — Secondary History Mechanism Contrasts",
        secondary,
    )

    reporter.json(
        "stage-05-secondary-mechanism.json",
        secondary,
    )

    # Per-lag material persistence and calibration.
    per_lag = {}

    for lag in range(
        1,
        HORIZON + 1,
    ):
        per_lag[
            str(
                lag
            )
        ] = {}

        for arm in HISTORY_ARMS:
            target = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.target_expected_attachments,
                )
            )

            prevent_expected = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.prevent_expected_attachments,
                )
            )

            force_expected = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.force_expected_attachments,
                )
            )

            local_mass = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.prevent_local_material_mass,
                )
            )

            total_mass = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.prevent_material_mass,
                )
            )

            offsets = (
                group_lag_values(
                    lag_rows,
                    arm,
                    lag,
                    lambda r:
                    r.offset,
                )
            )

            per_lag[
                str(
                    lag
                )
            ][
                arm
            ] = {
                "target": bootstrap_mean_ci(
                    target,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10000
                    + lag * 100
                    + HISTORY_ARMS.index(
                        arm
                    ) * 10,
                ),
                "prevent_expected": bootstrap_mean_ci(
                    prevent_expected,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10001
                    + lag * 100
                    + HISTORY_ARMS.index(
                        arm
                    ) * 10,
                ),
                "force_expected": bootstrap_mean_ci(
                    force_expected,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10002
                    + lag * 100
                    + HISTORY_ARMS.index(
                        arm
                    ) * 10,
                ),
                "prevent_local_material_mass": bootstrap_mean_ci(
                    local_mass,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10003
                    + lag * 100
                    + HISTORY_ARMS.index(
                        arm
                    ) * 10,
                ),
                "prevent_total_material_mass": bootstrap_mean_ci(
                    total_mass,
                    int(
                        profile[
                            "bootstrap_reps"
                        ]
                    ),
                    args.seed
                    + 10004
                    + lag * 100
                    + HISTORY_ARMS.index(
                        arm
                    ) * 10,
                ),
                "offset": (
                    {
                        "role": (
                            "DEFINITION_ASSERTION"
                        ),
                        "value": 0.0,
                    }
                    if arm
                    == "erased"
                    else bootstrap_mean_ci(
                        offsets,
                        int(
                            profile[
                                "bootstrap_reps"
                            ]
                        ),
                        args.seed
                        + 10005
                        + lag * 100
                        + HISTORY_ARMS.index(
                            arm
                        ) * 10,
                    )
                ),
            }

    reporter.stage(
        "stage-06-history-persistence.md",
        "Stage 6 — Per-Lag Material Persistence and Calibration",
        per_lag,
    )

    reporter.json(
        "stage-06-history-persistence.json",
        per_lag,
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
            "The history-placement or dynamically matched background-construction "
            "validity gate failed. No history-response verdict is eligible."
        )

    elif p_status == "SUPPORTED":
        overall = (
            "ACCESSIBLE_MATERIAL_HISTORY_CHANGES_CAUSAL_RESPONSE"
        )

        bounded = (
            "With visible occupancy geometry, total initial material mass, "
            "allocation policy, future environment and dynamically matched "
            "PREVENT background construction controlled, moving the decaying "
            "material trace from outside the H-step causal reach to the local "
            "probe neighbourhood changed mean finite-horizon causal response "
            "by at least the frozen meaningful scale."
        )

    elif (
        p_status
        == "BOUNDED_NEAR_ZERO"
    ):
        overall = (
            "MATERIAL_HISTORY_RESPONSE_BOUNDED_NEAR_ZERO"
        )

        bounded = (
            "Under the frozen trace strength, age, half-life, placement and "
            "dynamically matched background construction protocol, accessible "
            "versus remote decaying material history changed mean finite-horizon "
            "causal response by less than the predeclared +/-0.15 attachment scale."
        )

    else:
        overall = (
            "MATERIAL_HISTORY_CAUSAL_RESPONSE_UNRESOLVED"
        )

        bounded = (
            "The experiment did not resolve whether causally accessible decaying "
            "material history changes finite-horizon response at the frozen "
            "+/-0.15 attachment scale."
        )

    verdict = {
        "validity": (
            matching
        ),
        "primary_status": (
            p_status
        ),
        "overall_status": (
            overall
        ),
        "bounded_claim": (
            bounded
        ),
        "interpretation_boundary": {
            "what_is_established_if_supported": (
                "A stored decaying material state channel can change response "
                "while visible occupancy is held fixed."
            ),
            "what_is_not_established": [
                "self-generated memory",
                "learning",
                "adaptation",
                "history decoding",
                "semantic memory",
                "formal branching process",
                "criticality",
                "individuality",
                "organism",
                "life",
            ],
            "write_only_history_encoding": True,
            "new_cells_inherit_history": False,
            "history_transmission": False,
        },
        "stop_rule": (
            "No V2 parameter rescue. Increase independent groups only if the "
            "scientific run is unresolved solely because achieved MDE exceeds "
            "the frozen SEI."
        ),
        "next_if_supported": (
            "Ask whether a genuine experience encoder can create the same "
            "causally effective material state without direct experimental writing."
        ),
        "next_if_bounded": (
            "Treat decaying stored material as causally weak at this tested "
            "strength/timescale and move to the individuality experiment."
        ),
    }

    reporter.stage(
        "stage-07-verdict.md",
        "Stage 7 — Bounded Chapter 27 V1 Verdict",
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
    ] = (
        overall
    )

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
