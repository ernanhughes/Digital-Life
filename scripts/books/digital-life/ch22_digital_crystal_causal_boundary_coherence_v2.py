#!/usr/bin/env python3
"""
Chapter 22 — When Does the Process Become One Thing? (V2)

Causal boundary coherence
=========================

Chapter 22 V1 found large held-out self-prediction advantages, especially at
R = 0.90 R_eff, but the frozen family maximum did not beat the run-group
future-permutation null (p ~= 0.085).  V1 therefore FAILED.

V2 does not tune the V1 decoder, radii, alpha, or permutation procedure.

Instead it changes modality completely:

    prediction -> causal intervention

Fresh frozen question
---------------------

Does the V1 carry-forward candidate boundary at:

    R = 0.90 R_eff

localize causal consequences more strongly than an ordinary interior
pseudo-boundary at:

    R = 0.60 R_eff

inside the same Digital Crystal?

At a frozen checkpoint, V2 creates common-random-number counterfactual branches:

    CONTROL
        no intervention

    INSIDE
        remove K occupied cells from a thin shell just inside the boundary

    OUTSIDE
        remove K occupied cells from a thin shell just outside the boundary

Inside/outside removal sets are matched on:

    occupied-neighbour count
    absolute distance-from-boundary bin
    exact intervention count K

The future stochastic field is cell-keyed, so surviving cells receive the same
random draws across counterfactual branches.

Primary response
----------------

At the frozen response horizon, measure occupancy divergence from CONTROL in:

    INNER TARGET SHELL
    OUTER TARGET SHELL

For each boundary:

    causal_localization =
        (inside_perturbation -> inner_target
         - outside_perturbation -> inner_target)
        +
        (outside_perturbation -> outer_target
         - inside_perturbation -> outer_target)

All divergences are normalized by the number of lattice sites in the
corresponding target shell.

This asks whether consequences preferentially remain on the same side of the
candidate boundary as the perturbation.

Primary statistic
-----------------

    CAUSAL_COHERENCE_EXCESS =
        causal_localization(R=0.90)
        -
        causal_localization(R=0.60)

The 0.60 boundary is not claimed to be a geometry-perfect null.  It is a
predeclared same-substrate pseudo-boundary control for ordinary radial/local
causal localization.

Success requires:

    mean causal coherence excess >= 0.01
    paired sign-flip p < 0.05
    candidate causal localization > 0

No alternate radii may be added after seeing V2 results.

Scientific boundary
-------------------

Success would establish only:

    preferential causal localization at the V1 carry-forward spatial boundary
    relative to the predeclared interior pseudo-boundary control

It would NOT establish:

    individuality
    autonomy
    causal closure
    self
    organism
    life

If V2 fails:
    do not tune radii, shell width, K, or horizon.
    close the causal-boundary test.

Requires beside this file:
    ch18_digital_crystal_persistent_material_state_v7.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-causal-boundary-coherence-v2"
SCHEMA_VERSION = 2
CHAPTER = 22
CHAPTER_TITLE = "When Does the Process Become One Thing?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 96,
        "radius": 72,
        "warmup_steps": 20,
        "checkpoint_after_warmup": 36,
        "response_horizon": 8,

        "loss_rate": 0.08,
        "budget": 96,

        # V1 carry-forward candidate and predeclared interior control.
        "candidate_radius_fraction": 0.90,
        "control_radius_fraction": 0.60,

        # Boundary-local intervention geometry.
        "shell_width": 4.0,
        "distance_bin_width": 1.0,
        "intervention_k": 16,

        # Primary scientific magnitude gate:
        # 1 percentage point of target-shell sites in the paired interaction.
        "primary_sei": 0.01,

        "bootstrap_reps": 3000,
        "permutations": 4000,
        "alpha": 0.05,

        "max_capacity_fraction": 0.75,
    },

    "standard": {
        "groups": 192,
        "radius": 80,
        "warmup_steps": 20,
        "checkpoint_after_warmup": 40,
        "response_horizon": 8,

        "loss_rate": 0.08,
        "budget": 96,

        "candidate_radius_fraction": 0.90,
        "control_radius_fraction": 0.60,

        "shell_width": 4.0,
        "distance_bin_width": 1.0,
        "intervention_k": 16,

        "primary_sei": 0.01,

        "bootstrap_reps": 5000,
        "permutations": 8000,
        "alpha": 0.05,

        "max_capacity_fraction": 0.75,
    },

    "full": {
        "groups": 384,
        "radius": 96,
        "warmup_steps": 20,
        "checkpoint_after_warmup": 48,
        "response_horizon": 10,

        "loss_rate": 0.08,
        "budget": 96,

        "candidate_radius_fraction": 0.90,
        "control_radius_fraction": 0.60,

        "shell_width": 4.0,
        "distance_bin_width": 1.0,
        "intervention_k": 16,

        "primary_sei": 0.01,

        "bootstrap_reps": 8000,
        "permutations": 12000,
        "alpha": 0.05,

        "max_capacity_fraction": 0.75,
    },
}


# ============================================================================
# Frozen base helpers
# ============================================================================

def no_material_params() -> ch18.MaterialParams:
    return ch18.MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=0.0,
        transmission_fraction=0.0,
    )


def clone_state(
    state: ch18.MaterialCrystalState,
) -> ch18.MaterialCrystalState:
    return ch18.MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def frontier_cells(
    occupied: Set[Cell],
    radius: int,
) -> List[Cell]:
    frontier: Set[Cell] = set()

    for cell in occupied:
        for nb in ch18.neighbors(cell):
            if (
                nb not in occupied
                and ch18.hex_distance(nb) <= radius
            ):
                frontier.add(nb)

    return sorted(frontier)


def occupied_neighbor_count(
    cell: Cell,
    occupied: Set[Cell],
) -> int:
    return sum(
        nb in occupied
        for nb in ch18.neighbors(cell)
    )


# ============================================================================
# Keyed randomness
# ============================================================================

def keyed_uniform(
    namespace: str,
    stream_seed: int,
    step: int,
    cell: Cell,
    extra: int = 0,
) -> float:
    payload = (
        f"{namespace}|{stream_seed}|{step}|"
        f"{cell[0]}|{cell[1]}|{extra}"
    ).encode("utf-8")

    digest = hashlib.blake2b(
        payload,
        digest_size=8,
    ).digest()

    return int.from_bytes(
        digest,
        "big",
    ) / float(2**64)


def schedule_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    return keyed_uniform(
        "ch22-v2-schedule",
        stream_seed,
        step,
        cell,
    )


def loss_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    return keyed_uniform(
        "ch22-v2-loss",
        stream_seed,
        step,
        cell,
    )


def selection_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
    boundary_index: int,
    side_index: int,
) -> float:
    return keyed_uniform(
        "ch22-v2-intervention-selection",
        stream_seed,
        step,
        cell,
        boundary_index * 10 + side_index,
    )


# ============================================================================
# Neutral finite-budget dynamics
# ============================================================================

def select_neutral_candidates(
    frontier: Sequence[Cell],
    budget: int,
    stream_seed: int,
    step: int,
) -> List[Cell]:
    frontier = list(frontier)

    k = max(
        0,
        min(
            int(budget),
            len(frontier),
        ),
    )

    return sorted(
        frontier,
        key=lambda c: (
            schedule_uniform(
                stream_seed,
                step,
                c,
            ),
            c,
        ),
    )[:k]


def budgeted_growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: int,
) -> Tuple[
    ch18.MaterialCrystalState,
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

    frontier = frontier_cells(
        occupied_before,
        radius,
    )

    next_step = (
        state.step + 1
    )

    selected = select_neutral_candidates(
        frontier,
        budget,
        state.stream_seed,
        next_step,
    )

    additions: List[Cell] = []

    for cell in selected:
        n = occupied_neighbor_count(
            cell,
            occupied_before,
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
            + crystal_params.signal_rate_gain
            * float(input_value)
            + crystal_params.anisotropy_gain
            * anisotropy
            - crystal_params.crowding_penalty
            * crowding
        )

        if (
            ch18.cell_uniform(
                state.stream_seed,
                next_step,
                cell,
            )
            < ch18.logistic_scalar(score)
        ):
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

    return out, additions


def apply_background_loss(
    state: ch18.MaterialCrystalState,
    loss_rate: float,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
]:
    lost = [
        cell
        for cell in sorted(
            state.occupied
        )
        if loss_uniform(
            state.stream_seed,
            state.step,
            cell,
        ) < float(loss_rate)
    ]

    out = clone_state(
        state
    )

    for cell in lost:
        out.occupied.discard(cell)
        out.birth_time.pop(
            cell,
            None,
        )

    if out.population_by_step:
        out.population_by_step[-1] = len(
            out.occupied
        )

    return out, lost


# ============================================================================
# Geometry
# ============================================================================

def axial_to_xy(
    cell: Cell,
) -> Tuple[float, float]:
    q, r = cell
    return (
        q + 0.5 * r,
        (math.sqrt(3.0) / 2.0) * r,
    )


def euclidean_radius(
    cell: Cell,
) -> float:
    x, y = axial_to_xy(
        cell
    )
    return math.hypot(
        x,
        y,
    )


def effective_radius(
    occupied: Set[Cell],
) -> float:
    if not occupied:
        return 1.0

    return max(
        1.0,
        max(
            euclidean_radius(c)
            for c in occupied
        ),
    )


def make_universe(
    radius: int,
) -> Set[Cell]:
    return {
        (q, r)
        for q in range(
            -radius,
            radius + 1,
        )
        for r in range(
            -radius,
            radius + 1,
        )
        if ch18.hex_distance(
            (q, r)
        ) <= radius
    }


def radial_shell(
    universe: Set[Cell],
    low: float,
    high: float,
    include_low: bool = True,
) -> Set[Cell]:
    if include_low:
        return {
            c
            for c in universe
            if (
                euclidean_radius(c) >= low
                and euclidean_radius(c) <= high
            )
        }

    return {
        c
        for c in universe
        if (
            euclidean_radius(c) > low
            and euclidean_radius(c) <= high
        )
    }


# ============================================================================
# Matched intervention selection
# ============================================================================

def distance_bin(
    cell: Cell,
    cutoff: float,
    bin_width: float,
) -> int:
    d = abs(
        euclidean_radius(cell)
        - cutoff
    )

    return int(
        math.floor(
            d
            / max(
                1e-9,
                bin_width,
            )
        )
    )


def intervention_stratum(
    cell: Cell,
    occupied: Set[Cell],
    cutoff: float,
    bin_width: float,
) -> Tuple[int, int]:
    return (
        occupied_neighbor_count(
            cell,
            occupied,
        ),
        distance_bin(
            cell,
            cutoff,
            bin_width,
        ),
    )


def matched_intervention_sets(
    state: ch18.MaterialCrystalState,
    universe: Set[Cell],
    cutoff: float,
    shell_width: float,
    bin_width: float,
    k: int,
    boundary_index: int,
) -> Optional[
    Tuple[
        List[Cell],
        List[Cell],
        dict,
    ]
]:
    occupied = set(
        state.occupied
    )

    inner_zone = radial_shell(
        universe,
        max(
            0.0,
            cutoff - shell_width,
        ),
        cutoff,
        include_low=True,
    )

    outer_zone = radial_shell(
        universe,
        cutoff,
        cutoff + shell_width,
        include_low=False,
    )

    inside_candidates = sorted(
        occupied
        & inner_zone
    )

    outside_candidates = sorted(
        occupied
        & outer_zone
    )

    inside_by: Dict[
        Tuple[int, int],
        List[Cell],
    ] = {}

    outside_by: Dict[
        Tuple[int, int],
        List[Cell],
    ] = {}

    for cell in inside_candidates:
        key = intervention_stratum(
            cell,
            occupied,
            cutoff,
            bin_width,
        )

        inside_by.setdefault(
            key,
            [],
        ).append(cell)

    for cell in outside_candidates:
        key = intervention_stratum(
            cell,
            occupied,
            cutoff,
            bin_width,
        )

        outside_by.setdefault(
            key,
            [],
        ).append(cell)

    matched_pairs: List[
        Tuple[Cell, Cell, Tuple[int, int]]
    ] = []

    common_keys = sorted(
        set(
            inside_by
        )
        & set(
            outside_by
        )
    )

    for key in common_keys:
        ins = sorted(
            inside_by[key],
            key=lambda c: (
                selection_uniform(
                    state.stream_seed,
                    state.step,
                    c,
                    boundary_index,
                    0,
                ),
                c,
            ),
        )

        outs = sorted(
            outside_by[key],
            key=lambda c: (
                selection_uniform(
                    state.stream_seed,
                    state.step,
                    c,
                    boundary_index,
                    1,
                ),
                c,
            ),
        )

        n = min(
            len(ins),
            len(outs),
        )

        for i in range(n):
            matched_pairs.append(
                (
                    ins[i],
                    outs[i],
                    key,
                )
            )

    matched_pairs = sorted(
        matched_pairs,
        key=lambda pair: (
            keyed_uniform(
                "ch22-v2-pair-order",
                state.stream_seed,
                state.step,
                pair[0],
                boundary_index,
            ),
            pair[0],
            pair[1],
        ),
    )

    if len(
        matched_pairs
    ) < k:
        return None

    chosen = matched_pairs[
        :k
    ]

    inside = [
        p[0]
        for p in chosen
    ]

    outside = [
        p[1]
        for p in chosen
    ]

    stratum_counts: Dict[
        str,
        int,
    ] = {}

    for _, _, key in chosen:
        label = (
            f"neighbors={key[0]},distance_bin={key[1]}"
        )

        stratum_counts[label] = (
            stratum_counts.get(
                label,
                0,
            )
            + 1
        )

    diagnostics = {
        "inside_candidates": int(
            len(
                inside_candidates
            )
        ),
        "outside_candidates": int(
            len(
                outside_candidates
            )
        ),
        "matched_pair_pool": int(
            len(
                matched_pairs
            )
        ),
        "selected_k": int(
            k
        ),
        "stratum_counts": (
            stratum_counts
        ),
    }

    return (
        inside,
        outside,
        diagnostics,
    )


# ============================================================================
# Branching
# ============================================================================

def remove_cells(
    state: ch18.MaterialCrystalState,
    cells: Sequence[Cell],
) -> ch18.MaterialCrystalState:
    out = clone_state(
        state
    )

    for cell in cells:
        out.occupied.discard(
            cell
        )
        out.birth_time.pop(
            cell,
            None,
        )

    if out.population_by_step:
        out.population_by_step[-1] = len(
            out.occupied
        )

    return out


def run_future(
    state: ch18.MaterialCrystalState,
    future_env: Sequence[float],
    profile: dict,
    crystal_params: ch18.CrystalParams,
) -> ch18.MaterialCrystalState:
    out = clone_state(
        state
    )

    for value in future_env:
        out, _ = budgeted_growth_step(
            out,
            float(value),
            profile[
                "radius"
            ],
            crystal_params,
            profile[
                "budget"
            ],
        )

        out, _ = apply_background_loss(
            out,
            profile[
                "loss_rate"
            ],
        )

        if not out.occupied:
            break

        if (
            ch18.capacity_fraction_occupied(
                out.occupied,
                profile[
                    "radius"
                ],
            )
            >= profile[
                "max_capacity_fraction"
            ]
        ):
            raise RuntimeError(
                "Capacity guard triggered in branch."
            )

    return out


# ============================================================================
# Causal response
# ============================================================================

def occupancy_divergence(
    branch: Set[Cell],
    control: Set[Cell],
    target: Set[Cell],
) -> float:
    if not target:
        return 0.0

    changed = (
        branch
        ^ control
    )

    return (
        len(
            changed
            & target
        )
        / float(
            len(
                target
            )
        )
    )


@dataclass
class BoundaryResult:
    radius_fraction: float
    cutoff: float

    inside_to_inner: float
    outside_to_inner: float
    inside_to_outer: float
    outside_to_outer: float

    causal_localization: float

    diagnostics: dict


def evaluate_boundary(
    checkpoint: ch18.MaterialCrystalState,
    future_env: Sequence[float],
    profile: dict,
    crystal_params: ch18.CrystalParams,
    universe: Set[Cell],
    radius_fraction: float,
    boundary_index: int,
) -> Optional[BoundaryResult]:
    reff = effective_radius(
        checkpoint.occupied
    )

    cutoff = (
        radius_fraction
        * reff
    )

    matched = matched_intervention_sets(
        state=checkpoint,
        universe=universe,
        cutoff=cutoff,
        shell_width=profile[
            "shell_width"
        ],
        bin_width=profile[
            "distance_bin_width"
        ],
        k=profile[
            "intervention_k"
        ],
        boundary_index=boundary_index,
    )

    if matched is None:
        return None

    inside_cells, outside_cells, diagnostics = matched

    control_start = clone_state(
        checkpoint
    )

    inside_start = remove_cells(
        checkpoint,
        inside_cells,
    )

    outside_start = remove_cells(
        checkpoint,
        outside_cells,
    )

    control_end = run_future(
        control_start,
        future_env,
        profile,
        crystal_params,
    )

    inside_end = run_future(
        inside_start,
        future_env,
        profile,
        crystal_params,
    )

    outside_end = run_future(
        outside_start,
        future_env,
        profile,
        crystal_params,
    )

    inner_target = radial_shell(
        universe,
        max(
            0.0,
            cutoff
            - profile[
                "shell_width"
            ],
        ),
        cutoff,
        include_low=True,
    )

    outer_target = radial_shell(
        universe,
        cutoff,
        cutoff
        + profile[
            "shell_width"
        ],
        include_low=False,
    )

    inside_to_inner = (
        occupancy_divergence(
            inside_end.occupied,
            control_end.occupied,
            inner_target,
        )
    )

    outside_to_inner = (
        occupancy_divergence(
            outside_end.occupied,
            control_end.occupied,
            inner_target,
        )
    )

    inside_to_outer = (
        occupancy_divergence(
            inside_end.occupied,
            control_end.occupied,
            outer_target,
        )
    )

    outside_to_outer = (
        occupancy_divergence(
            outside_end.occupied,
            control_end.occupied,
            outer_target,
        )
    )

    causal_localization = (
        (
            inside_to_inner
            - outside_to_inner
        )
        +
        (
            outside_to_outer
            - inside_to_outer
        )
    )

    diagnostics = dict(
        diagnostics
    )

    diagnostics.update({
        "effective_radius": float(
            reff
        ),
        "cutoff": float(
            cutoff
        ),
        "inner_target_sites": int(
            len(
                inner_target
            )
        ),
        "outer_target_sites": int(
            len(
                outer_target
            )
        ),
    })

    return BoundaryResult(
        radius_fraction=float(
            radius_fraction
        ),
        cutoff=float(
            cutoff
        ),
        inside_to_inner=float(
            inside_to_inner
        ),
        outside_to_inner=float(
            outside_to_inner
        ),
        inside_to_outer=float(
            inside_to_outer
        ),
        outside_to_outer=float(
            outside_to_outer
        ),
        causal_localization=float(
            causal_localization
        ),
        diagnostics=diagnostics,
    )


# ============================================================================
# One fresh run group
# ============================================================================

def simulate_to_checkpoint(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
) -> Tuple[
    ch18.MaterialCrystalState,
    np.ndarray,
]:
    warmup = profile[
        "warmup_steps"
    ]

    cp_steps = profile[
        "checkpoint_after_warmup"
    ]

    future_steps = profile[
        "response_horizon"
    ]

    gseed = (
        seed
        + group_index * 1009
    )

    env = ch18.make_environment(
        warmup
        + cp_steps
        + future_steps
        + 8,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        profile[
            "radius"
        ],
        crystal_params,
        no_material_params(),
    )

    for j in range(
        cp_steps
    ):
        state, _ = budgeted_growth_step(
            state,
            float(
                env[
                    warmup + j
                ]
            ),
            profile[
                "radius"
            ],
            crystal_params,
            profile[
                "budget"
            ],
        )

        state, _ = apply_background_loss(
            state,
            profile[
                "loss_rate"
            ],
        )

        if not state.occupied:
            break

        if (
            ch18.capacity_fraction_occupied(
                state.occupied,
                profile[
                    "radius"
                ],
            )
            >= profile[
                "max_capacity_fraction"
            ]
        ):
            raise RuntimeError(
                "Capacity guard triggered before checkpoint."
            )

    future_env = np.asarray(
        env[
            warmup
            + cp_steps:
            warmup
            + cp_steps
            + future_steps
        ],
        dtype=float,
    )

    return (
        state,
        future_env,
    )


@dataclass
class GroupResult:
    group: int
    candidate: BoundaryResult
    control: BoundaryResult
    excess: float


def run_group(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
    universe: Set[Cell],
) -> Optional[GroupResult]:
    checkpoint, future_env = (
        simulate_to_checkpoint(
            profile,
            crystal_params,
            seed,
            group_index,
        )
    )

    if not checkpoint.occupied:
        return None

    candidate = evaluate_boundary(
        checkpoint=checkpoint,
        future_env=future_env,
        profile=profile,
        crystal_params=crystal_params,
        universe=universe,
        radius_fraction=profile[
            "candidate_radius_fraction"
        ],
        boundary_index=0,
    )

    control = evaluate_boundary(
        checkpoint=checkpoint,
        future_env=future_env,
        profile=profile,
        crystal_params=crystal_params,
        universe=universe,
        radius_fraction=profile[
            "control_radius_fraction"
        ],
        boundary_index=1,
    )

    if (
        candidate is None
        or control is None
    ):
        return None

    excess = (
        candidate.causal_localization
        - control.causal_localization
    )

    return GroupResult(
        group=group_index,
        candidate=candidate,
        control=control,
        excess=float(
            excess
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
        values,
        dtype=float,
    )

    rng = np.random.default_rng(
        seed
    )

    boot = np.empty(
        reps,
        dtype=float,
    )

    for i in range(
        reps
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

        "median": float(
            np.median(
                arr
            )
        ),

        "std": (
            float(
                np.std(
                    arr,
                    ddof=1,
                )
            )
            if len(
                arr
            ) > 1
            else 0.0
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
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        values,
        dtype=float,
    )

    observed = float(
        np.mean(
            arr
        )
    )

    rng = np.random.default_rng(
        seed
    )

    null = np.empty(
        permutations,
        dtype=float,
    )

    for i in range(
        permutations
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

        null[i] = float(
            np.mean(
                arr * signs
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
        permutations
        + 1.0
    )

    return {
        "observed_mean": (
            observed
        ),

        "p_value": float(
            p
        ),

        "alternative": (
            "greater"
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
            / "ch22-causal-boundary-coherence-v2-full-report.md"
        )

        parts = [
            "# Chapter 22 — When Does the Process Become One Thing? (V2)",
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

        for title, body in (
            self.sections
        ):
            parts.extend([
                "---",
                "",
                f"## {title}",
                "",
                body,
                "",
            ])

        path.write_text(
            "\n".join(
                parts
            ),
            encoding="utf-8",
        )

        return path


# ============================================================================
# Stages
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": (
            "CAUSAL BOUNDARY COHERENCE TEST"
        ),

        "v1_status": (
            "FAILED predictive-coherence family test because the observed "
            "family maximum did not beat the frozen run-group future-"
            "permutation null at alpha=0.05."
        ),

        "v1_control_note": (
            "The V1 observer-null environment was not identical in geometry "
            "to the real annular environment. V2 does not reuse that "
            "predictive null as a causal control."
        ),

        "question": (
            "Does the V1 carry-forward boundary at 0.90 R_eff localize "
            "causal consequences more strongly than a predeclared interior "
            "pseudo-boundary at 0.60 R_eff?"
        ),

        "candidate_radius_fraction": (
            profile[
                "candidate_radius_fraction"
            ]
        ),

        "control_radius_fraction": (
            profile[
                "control_radius_fraction"
            ]
        ),

        "intervention": {
            "type": (
                "occupied-cell removal"
            ),
            "k": (
                profile[
                    "intervention_k"
                ]
            ),
            "shell_width": (
                profile[
                    "shell_width"
                ]
            ),
            "matching": [
                "occupied-neighbour count",
                "absolute distance-from-boundary bin",
                "exact intervention count",
            ],
        },

        "response_horizon": (
            profile[
                "response_horizon"
            ]
        ),

        "primary_statistic": (
            "causal_localization(0.90 R_eff) - "
            "causal_localization(0.60 R_eff)"
        ),

        "causal_localization_definition": (
            "(inside perturbation -> inner target - outside perturbation -> "
            "inner target) + (outside perturbation -> outer target - inside "
            "perturbation -> outer target)"
        ),

        "primary_sei": (
            profile[
                "primary_sei"
            ]
        ),

        "alpha": (
            profile[
                "alpha"
            ]
        ),

        "new_sentence_if_successful": (
            "Perturbations on opposite sides of the V1 carry-forward spatial "
            "boundary produced preferentially boundary-localized causal "
            "consequences beyond those observed at the predeclared interior "
            "pseudo-boundary."
        ),

        "forbidden_overclaims": [
            "individual",
            "individuality",
            "autonomy",
            "causal closure",
            "self",
            "agency",
            "organism",
            "life",
        ],

        "status": (
            "MEASURED"
        ),
    }

    reporter.json(
        "stage-00-protocol.json",
        result,
    )

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Freeze the Causal-Boundary Test",
        result,
    )

    return result


def stage_1_run_interventions(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    dict,
    List[GroupResult],
]:
    universe = make_universe(
        profile[
            "radius"
        ]
    )

    results: List[
        GroupResult
    ] = []

    skipped = 0

    for g in tqdm(
        range(
            profile[
                "groups"
            ]
        ),
        desc="Stage 1 paired causal interventions",
    ):
        result = run_group(
            profile,
            crystal_params,
            seed,
            g,
            universe,
        )

        if result is None:
            skipped += 1
            continue

        results.append(
            result
        )

    if not results:
        raise RuntimeError(
            "No groups had enough matched intervention sites."
        )

    result = {
        "role": (
            "FRESH PAIRED CAUSAL INTERVENTION DATASET"
        ),

        "requested_groups": (
            profile[
                "groups"
            ]
        ),

        "usable_groups": int(
            len(
                results
            )
        ),

        "skipped_groups": int(
            skipped
        ),

        "usable_fraction": float(
            len(
                results
            )
            / profile[
                "groups"
            ]
        ),

        "status": (
            "MEASURED"
        ),
    }

    reporter.json(
        "stage-01-intervention-dataset.json",
        result,
    )

    reporter.stage(
        "stage-01-intervention-dataset.md",
        "Stage 1 — Run Fresh Paired Counterfactual Branches",
        result,
    )

    return (
        result,
        results,
    )


def stage_2_measure_coherence(
    reporter: Reporter,
    profile: dict,
    results: Sequence[GroupResult],
    seed: int,
    image_dir: Path,
) -> dict:
    candidate_localization = [
        r.candidate.causal_localization
        for r in results
    ]

    control_localization = [
        r.control.causal_localization
        for r in results
    ]

    excess = [
        r.excess
        for r in results
    ]

    candidate_summary = (
        bootstrap_mean_ci(
            candidate_localization,
            profile[
                "bootstrap_reps"
            ],
            seed
            + 2_000_000,
        )
    )

    control_summary = (
        bootstrap_mean_ci(
            control_localization,
            profile[
                "bootstrap_reps"
            ],
            seed
            + 2_100_000,
        )
    )

    excess_summary = (
        bootstrap_mean_ci(
            excess,
            profile[
                "bootstrap_reps"
            ],
            seed
            + 2_200_000,
        )
    )

    excess_test = (
        signflip_greater(
            excess,
            profile[
                "permutations"
            ],
            seed
            + 2_300_000,
        )
    )

    def mean_component(
        attr: str,
        which: str,
    ) -> float:
        vals = []

        for r in results:
            obj = (
                r.candidate
                if which == "candidate"
                else r.control
            )

            vals.append(
                getattr(
                    obj,
                    attr,
                )
            )

        return float(
            np.mean(
                vals
            )
        )

    result = {
        "role": (
            "PRIMARY CAUSAL COHERENCE MEASUREMENT"
        ),

        "candidate_radius_fraction": (
            profile[
                "candidate_radius_fraction"
            ]
        ),

        "control_radius_fraction": (
            profile[
                "control_radius_fraction"
            ]
        ),

        "candidate_causal_localization": (
            candidate_summary
        ),

        "control_causal_localization": (
            control_summary
        ),

        "candidate_minus_control_excess": (
            excess_summary
        ),

        "paired_signflip_test": (
            excess_test
        ),

        "primary_sei": (
            profile[
                "primary_sei"
            ]
        ),

        "candidate_components": {
            "inside_to_inner": mean_component(
                "inside_to_inner",
                "candidate",
            ),
            "outside_to_inner": mean_component(
                "outside_to_inner",
                "candidate",
            ),
            "inside_to_outer": mean_component(
                "inside_to_outer",
                "candidate",
            ),
            "outside_to_outer": mean_component(
                "outside_to_outer",
                "candidate",
            ),
        },

        "control_components": {
            "inside_to_inner": mean_component(
                "inside_to_inner",
                "control",
            ),
            "outside_to_inner": mean_component(
                "outside_to_inner",
                "control",
            ),
            "inside_to_outer": mean_component(
                "inside_to_outer",
                "control",
            ),
            "outside_to_outer": mean_component(
                "outside_to_outer",
                "control",
            ),
        },

        "status": (
            "MEASURED"
        ),
    }

    reporter.json(
        "stage-02-causal-coherence.json",
        result,
    )

    reporter.stage(
        "stage-02-causal-coherence.md",
        "Stage 2 — Measure Boundary-Localized Causal Effects",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(
            8,
            5,
        )
    )

    ax.boxplot(
        [
            candidate_localization,
            control_localization,
            excess,
        ],
        labels=[
            "candidate\n0.90 R_eff",
            "control\n0.60 R_eff",
            "excess",
        ],
    )

    ax.axhline(
        0.0,
        linestyle="--",
    )

    ax.axhline(
        profile[
            "primary_sei"
        ],
        linestyle=":",
    )

    ax.set_ylabel(
        "Normalized causal-localization response"
    )

    ax.set_title(
        "Chapter 22 V2: causal localization across boundaries"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch22-v2-01-causal-boundary-coherence.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    return result


def stage_3_verdict(
    reporter: Reporter,
    profile: dict,
    measured: dict,
) -> dict:
    candidate_positive = (
        measured[
            "candidate_causal_localization"
        ][
            "mean"
        ]
        > 0.0
    )

    magnitude_ok = (
        measured[
            "candidate_minus_control_excess"
        ][
            "mean"
        ]
        >= profile[
            "primary_sei"
        ]
    )

    p_ok = (
        measured[
            "paired_signflip_test"
        ][
            "p_value"
        ]
        < profile[
            "alpha"
        ]
    )

    supported = all([
        candidate_positive,
        magnitude_ok,
        p_ok,
    ])

    if supported:
        status = (
            "SUPPORTED"
        )

        bounded = (
            "Under the frozen Chapter 22 V2 protocol, the V1 carry-forward "
            "boundary at 0.90 R_eff showed positive boundary-localized causal "
            "response and exceeded the predeclared interior pseudo-boundary "
            "control by the frozen magnitude and paired-significance gates. "
            "This supports preferential causal localization at that spatial "
            "boundary under the tested intervention. It does not establish "
            "individuality or causal closure."
        )

    else:
        status = (
            "FAILED"
        )

        bounded = (
            "Chapter 22 V2 did not establish all predeclared gates required "
            "for preferential causal localization at the V1 carry-forward "
            "boundary relative to the interior pseudo-boundary control."
        )

    result = {
        "question": (
            "Does the V1 carry-forward spatial boundary preferentially "
            "localize causal consequences relative to an ordinary interior "
            "pseudo-boundary?"
        ),

        "candidate_positive_gate_passed": (
            candidate_positive
        ),

        "candidate_localization_mean": (
            measured[
                "candidate_causal_localization"
            ][
                "mean"
            ]
        ),

        "excess_mean": (
            measured[
                "candidate_minus_control_excess"
            ][
                "mean"
            ]
        ),

        "excess_ci95": [
            measured[
                "candidate_minus_control_excess"
            ][
                "ci95_low"
            ],
            measured[
                "candidate_minus_control_excess"
            ][
                "ci95_high"
            ],
        ],

        "primary_sei": (
            profile[
                "primary_sei"
            ]
        ),

        "magnitude_gate_passed": (
            magnitude_ok
        ),

        "paired_signflip_p_value": (
            measured[
                "paired_signflip_test"
            ][
                "p_value"
            ]
        ),

        "significance_gate_passed": (
            p_ok
        ),

        "status": (
            status
        ),

        "bounded_claim": (
            bounded
        ),

        "forbidden_overclaims": [
            "individual",
            "individuality",
            "autonomy",
            "causal closure",
            "self",
            "agency",
            "organism",
            "life",
        ],

        "next_question_if_supported": (
            "Does the same preferential causal boundary persist under a fresh "
            "starting-size and computational-budget robustness test without "
            "retuning the boundary?"
        ),

        "next_question_if_failed": (
            "Do not tune radii, intervention count, shell width, or response "
            "horizon. Close the Chapter 22 causal-boundary hypothesis and "
            "treat the Digital Crystal as a spatially structured field unless "
            "a qualitatively new individuation mechanism is introduced."
        ),
    }

    reporter.json(
        "stage-03-verdict.json",
        result,
    )

    reporter.stage(
        "stage-03-verdict.md",
        "Stage 3 — Bounded Chapter 22 V2 Verdict",
        result,
    )

    return result


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
        default=20260901,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch22-causal-boundary-coherence-v2"
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

        "experiment_version": (
            EXPERIMENT_VERSION
        ),

        "schema_version": (
            SCHEMA_VERSION
        ),

        "chapter": (
            CHAPTER
        ),

        "chapter_title": (
            CHAPTER_TITLE
        ),

        "run_type": (
            "CAUSAL BOUNDARY COHERENCE TEST"
        ),

        "profile": (
            args.profile
        ),

        "profile_config": (
            profile
        ),

        "seed": (
            args.seed
        ),

        "v1_carry_forward_boundary": (
            profile[
                "candidate_radius_fraction"
            ]
        ),

        "predeclared_interior_control_boundary": (
            profile[
                "control_radius_fraction"
            ]
        ),

        "canonical_attachment_probability_modified": (
            False
        ),

        "common_random_numbers": (
            "cell-keyed attachment, loss, and scheduling draws"
        ),

        "scientific_boundary": (
            "Preferential causal localization only. No individual, "
            "individuality, autonomy, causal closure, self, agency, organism, "
            "or life claim."
        ),

        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 22 V2 — CAUSAL BOUNDARY COHERENCE"
    )

    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"candidate={profile['candidate_radius_fraction']} "
        f"control={profile['control_radius_fraction']} "
        f"K={profile['intervention_k']} "
        f"horizon={profile['response_horizon']}"
    )

    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )

    s1, results = (
        stage_1_run_interventions(
            reporter,
            profile,
            crystal_params,
            args.seed,
        )
    )

    s2 = stage_2_measure_coherence(
        reporter,
        profile,
        results,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_verdict(
        reporter,
        profile,
        s2,
    )

    metadata.update({
        "finished_at_unix": (
            time.time()
        ),

        "stage_0_status": (
            s0[
                "status"
            ]
        ),

        "stage_1_status": (
            s1[
                "status"
            ]
        ),

        "stage_2_status": (
            s2[
                "status"
            ]
        ),

        "final_status": (
            s3[
                "status"
            ]
        ),

        "bounded_claim": (
            s3[
                "bounded_claim"
            ]
        ),
    })

    reporter.json(
        "run-metadata.json",
        metadata,
    )

    report_path = (
        reporter.full_report(
            metadata
        )
    )

    print()
    print("=" * 78)

    print(
        "CHAPTER 22 V2 COMPLETE"
    )

    print(
        f"protocol={s0['status']}"
    )

    print(
        f"dataset={s1['status']} "
        f"usable_groups={s1['usable_groups']}"
    )

    print(
        f"measurement={s2['status']}"
    )

    print(
        f"FINAL={s3['status']}"
    )

    print(
        f"candidate_localization="
        f"{s3['candidate_localization_mean']:.6f}"
    )

    print(
        f"excess={s3['excess_mean']:.6f}"
    )

    print(
        f"p={s3['paired_signflip_p_value']:.6f}"
    )

    print(
        f"report={report_path}"
    )

    print("=" * 78)


if __name__ == "__main__":
    main()
