#!/usr/bin/env python3
"""
Digital Life — Chapter 23 V2
Interface Source/Sink Transition Field
=======================================

V1 FAILED its frozen propagation claim.

Post-run diagnosis showed three important facts:
1. positive-weighted ridge centroids can turn "short-range signal + far-field
   noise" into an apparent outward ridge;
2. the dominant V1 feature was signed and negative at d=1, but the positive
   weighting deleted it before inference;
3. attachment and loss were pooled even though they have opposite interface
   roles.

V2 therefore changes the measurement, not the V1 thresholds.

FRESH-SEED QUESTIONS
--------------------
H1 — attachment-associated depletion
    attachment -> attachment excess at d in {1,2} is NEGATIVE.

    Interpretation boundary:
    This confirms a signed local depletion phenomenon. "Local opportunity
    consumption" remains the candidate mechanism until a direct attachment
    intervention establishes it causally.

H2 — loss-associated interface source
    loss -> attachment excess at d in {0,1} is POSITIVE at short lag.
    loss -> reoccupation is reported separately as the strongest mechanistic
    positive control inherited from Chapter 20.

H3 — non-recovery over the frozen observation window
    the attachment -> attachment deficit at d=1 remains negative at late lags
    and retains at least half the magnitude of the early deficit.

    This weakens a simple refractory interpretation. It does NOT establish
    permanent non-recovery.

H4 — conditional loss-hazard null (VALIDITY CONTROL)
    after conditioning on future occupied loss opportunity, prior loss should
    not materially change future per-eligible-cell loss hazard.

    Loss is i.i.d. per occupied cell by construction. Raw loss event density
    can still be spatially structured because occupancy is structured, so H4
    uses conditional hazard rather than raw density.

TRANSITION FIELD
----------------
Source classes:
    attachment
    loss

Target classes:
    attachment
    loss
    reoccupation
    first_occupation

Reoccupation and first occupation are subsets of attachment and are reported
as such.

SIGNED STATISTICS
-----------------
No positive-weighted centroid is used anywhere.

For each channel c and distance d:

    S_c(d) = sum_{tau=d..d+W} excess_c(d,tau), W=4

with tau starting at 1 for d=0.

Negative lags are measured on the same source window:

    A_c(d,tau) = excess_c(d,+tau) - excess_c(d,-tau)

The formal propagation screen is separate from H1/H2/H3:
    attachment -> attachment forward/backward asymmetry at d >= 3,
    after comparison with the k-partner cross-run future null.

CAUSAL CONE / GLOBAL BUDGET DIAGNOSTIC
--------------------------------------
For local radius-1 dynamics, tau < d is outside the ordinary local causal cone.
V2 measures rather than discards that region.

Because the finite global budget couples frontier selection weakly across the
whole frontier, a small distance-independent offset is possible. V2 reports:
    - raw signed surfaces (PRIMARY inference)
    - forbidden-region offset estimate
    - offset-corrected surfaces (DIAGNOSTIC only)

The raw surface is frozen as the inferential representation.

GEOMETRY
--------
- uniform distance grid
- uniform lag grid
- max_lag >= 2 * max_distance
- common source-time window for every lag:
      max_lag <= t < horizon - max_lag
- all sources and matched controls must be at least max_distance from the
  hard outer radius
- exact radial-distance bin width = 1
- exact occupied-neighbour-count matching
- one-to-one matching without replacement
- separate match gates for attachment and loss
- matching equality is asserted; no silent truncation

EVALUATED FRONTIER
------------------
V2 does NOT reconstruct the evaluated candidate set by calling
select_candidates twice. It uses a local copy of the frozen Chapter 21 neutral
growth step that returns the exact selected/evaluated set used in the growth
decision. The attachment probability rule, keyed RNG, and scheduling rule are
unchanged. We assert:
    additions <= evaluated

NULL
----
Cross-run future null is retained because V1 showed that generic developmental
structure can otherwise look like propagation.

Each source run uses k=4 deterministic partner runs and averages their target
surfaces.

POWER / EFFECT FLOOR
--------------------
V1 measured a population-surface noise scale around 1e-4.

Fresh V2 predeclares:
    minimum directional H1/H2 effect = 5e-4
    minimum propagation asymmetry excess = 5e-4

V2 reports achieved bootstrap precision explicitly.

VERDICT STRUCTURE
-----------------
No pooled "everything passed" verdict.

Validity:
    per-class match gates
    capacity gate
    no collapse
    H4 conditional loss-hazard null
    positive-control recovery of loss -> reoccupation

Findings:
    H1 attachment-associated local depletion
    H2 loss-associated local construction source
    H3 depletion non-recovery over frozen observation window
    PROPAGATION — only forward/backward asymmetry at d >= 3

FORBIDDEN OVERCLAIMS
--------------------
Do not call the negative band:
    refractory
unless recovery is demonstrated.

Do not call the process:
    wave
    excitable medium
    self
    individual
    organism
    life

"Interface source/sink field" is an operational description:
    loss creates local construction opportunity;
    attachment consumes local construction opportunity;
    finite computation rations which opportunities are evaluated.

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
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch21_digital_crystal_finite_update_budget_v3 as ch21


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
PARENT_EXPERIMENT_VERSION = ch21.EXPERIMENT_VERSION
EXPERIMENT_VERSION = "digital-crystal-interface-source-sink-v2"
SCHEMA_VERSION = 2
CHAPTER = 23
CHAPTER_TITLE = "Does the Process Move?"
RUN_TITLE = "Interface Source/Sink Transition Field"

Cell = Tuple[int, int]

SOURCE_CLASSES = ("attachment", "loss")
TARGET_CLASSES = (
    "attachment",
    "loss",
    "reoccupation",
    "first_occupation",
)
CHANNELS = tuple(
    (source, target)
    for source in SOURCE_CLASSES
    for target in TARGET_CLASSES
)


PROFILES = {
    # Engineering only. Never scientifically interpretable.
    "smoke": {
        "groups": 8,
        "radius": 48,
        "warmup_steps": 14,
        "continuation_steps": 48,
        "loss_rate": 0.08,
        "budget": 96,
        "max_distance": 4,
        "max_lag": 8,
        "band_width": 4,
        "radial_bin_width": 1,
        "cross_run_partners": 4,
        "minimum_attachment_match_fraction": 0.25,
        "minimum_loss_match_fraction": 0.70,
        "mde_signed_excess": 5e-4,
        "mde_propagation_asymmetry": 5e-4,
        "h4_loss_hazard_tolerance": 2e-3,
        "h3_min_retained_fraction": 0.50,
        "bootstrap_reps": 500,
        "signflip_permutations": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "radius": 72,
        "warmup_steps": 20,
        "continuation_steps": 96,
        "loss_rate": 0.08,
        "budget": 96,
        "max_distance": 8,
        "max_lag": 16,
        "band_width": 4,
        "radial_bin_width": 1,
        "cross_run_partners": 4,
        "minimum_attachment_match_fraction": 0.25,
        "minimum_loss_match_fraction": 0.70,
        "mde_signed_excess": 5e-4,
        "mde_propagation_asymmetry": 5e-4,
        "h4_loss_hazard_tolerance": 2e-3,
        "h3_min_retained_fraction": 0.50,
        "bootstrap_reps": 2500,
        "signflip_permutations": 5000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "radius": 88,
        "warmup_steps": 24,
        "continuation_steps": 128,
        "loss_rate": 0.08,
        "budget": 96,
        "max_distance": 10,
        "max_lag": 20,
        "band_width": 4,
        "radial_bin_width": 1,
        "cross_run_partners": 4,
        "minimum_attachment_match_fraction": 0.25,
        "minimum_loss_match_fraction": 0.70,
        "mde_signed_excess": 5e-4,
        "mde_propagation_asymmetry": 5e-4,
        "h4_loss_hazard_tolerance": 2e-3,
        "h3_min_retained_fraction": 0.50,
        "bootstrap_reps": 4000,
        "signflip_permutations": 10000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "radius": 104,
        "warmup_steps": 24,
        "continuation_steps": 160,
        "loss_rate": 0.08,
        "budget": 96,
        "max_distance": 12,
        "max_lag": 24,
        "band_width": 4,
        "radial_bin_width": 1,
        "cross_run_partners": 4,
        "minimum_attachment_match_fraction": 0.25,
        "minimum_loss_match_fraction": 0.70,
        "mde_signed_excess": 5e-4,
        "mde_propagation_asymmetry": 5e-4,
        "h4_loss_hazard_tolerance": 2e-3,
        "h3_min_retained_fraction": 0.50,
        "bootstrap_reps": 6000,
        "signflip_permutations": 20000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Deterministic helpers
# ============================================================================

def keyed_order(
    namespace: str,
    seed: int,
    group: int,
    step: int,
    cell: Cell,
) -> int:
    payload = (
        f"{namespace}|{seed}|{group}|{step}|{cell[0]}|{cell[1]}"
    ).encode("utf-8")
    return int.from_bytes(
        hashlib.blake2b(
            payload,
            digest_size=8,
        ).digest(),
        "big",
    )


def radial_bin(
    cell: Cell,
    width: int,
) -> int:
    return int(
        ch18.hex_distance(cell)
        // max(1, int(width))
    )


def occupied_neighbor_count(
    cell: Cell,
    occupied: Set[Cell],
) -> int:
    return int(
        sum(
            nb in occupied
            for nb in ch18.neighbors(cell)
        )
    )


def axial_ring_offsets(
    distance: int,
) -> np.ndarray:
    d = int(distance)
    if d == 0:
        return np.asarray(
            [[0, 0]],
            dtype=np.int16,
        )

    directions = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
    ]

    q = directions[4][0] * d
    r = directions[4][1] * d
    out: List[Cell] = []

    for side in range(6):
        dq, dr = directions[side]
        for _ in range(d):
            out.append((q, r))
            q += dq
            r += dr

    if len(set(out)) != 6 * d:
        raise RuntimeError(
            f"bad hex ring d={d}"
        )

    return np.asarray(
        out,
        dtype=np.int16,
    )


# ============================================================================
# Exact frozen Chapter 21 step, returning evaluated candidates
# ============================================================================

def budgeted_growth_step_with_evaluated(
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
    Semantically identical to ch21.budgeted_growth_step, except it also returns
    the exact selected/evaluated candidate list used in the decision loop.
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

    frontier = ch21.frontier_cells(
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

        if (
            ch18.cell_uniform(
                state.stream_seed,
                next_step,
                cell,
            )
            < ch18.logistic_scalar(score)
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


# ============================================================================
# Matching
# ============================================================================

def match_class(
    *,
    events: Sequence[Cell],
    controls: Sequence[Cell],
    geometry_occupied: Set[Cell],
    radius: int,
    max_distance: int,
    radial_bin_width: int,
    seed: int,
    group: int,
    step: int,
    namespace: str,
) -> Tuple[List[Cell], List[Cell], int]:
    """
    Exact one-to-one matching without replacement.

    Both event and control centers are excluded if their entire max-distance
    ring cannot fit inside the hard radius.
    """
    interior_limit = (
        int(radius)
        - int(max_distance)
    )

    eligible_events = [
        cell
        for cell in events
        if ch18.hex_distance(cell)
        <= interior_limit
    ]

    eligible_controls = [
        cell
        for cell in controls
        if ch18.hex_distance(cell)
        <= interior_limit
    ]

    buckets: Dict[
        Tuple[int, int],
        List[Cell],
    ] = defaultdict(list)

    for cell in eligible_controls:
        key = (
            occupied_neighbor_count(
                cell,
                geometry_occupied,
            ),
            radial_bin(
                cell,
                radial_bin_width,
            ),
        )
        buckets[key].append(cell)

    for key, pool in buckets.items():
        pool.sort(
            key=lambda cell: (
                keyed_order(
                    namespace + "-control",
                    seed,
                    group,
                    step,
                    cell,
                ),
                cell,
            )
        )

    event_order = sorted(
        eligible_events,
        key=lambda cell: (
            keyed_order(
                namespace + "-event",
                seed,
                group,
                step,
                cell,
            ),
            cell,
        ),
    )

    matched_events: List[Cell] = []
    matched_controls: List[Cell] = []

    for event in event_order:
        key = (
            occupied_neighbor_count(
                event,
                geometry_occupied,
            ),
            radial_bin(
                event,
                radial_bin_width,
            ),
        )

        pool = buckets.get(
            key,
            [],
        )

        if not pool:
            continue

        matched_events.append(
            event
        )
        matched_controls.append(
            pool.pop()
        )

    assert (
        len(matched_events)
        == len(matched_controls)
    )

    return (
        matched_events,
        matched_controls,
        len(eligible_events),
    )


# ============================================================================
# Dense observer frames
# ============================================================================

@dataclass
class DenseFrameSet:
    radius: int
    size: int
    shift: int
    attachment: np.ndarray
    loss: np.ndarray
    reoccupation: np.ndarray
    first_occupation: np.ndarray
    loss_eligible: np.ndarray

    def target(
        self,
        name: str,
        step: int,
    ) -> np.ndarray:
        return getattr(
            self,
            name,
        )[step]


@dataclass
class SourceRun:
    group: int
    frames: DenseFrameSet
    source_attachment: List[np.ndarray]
    control_attachment: List[np.ndarray]
    source_loss: List[np.ndarray]
    control_loss: List[np.ndarray]
    attachment_total_events: int
    attachment_eligible_events: int
    attachment_matched_events: int
    loss_total_events: int
    loss_eligible_events: int
    loss_matched_events: int
    max_capacity_fraction: float
    collapsed: bool


def cells_to_coords(
    cells: Sequence[Cell],
) -> np.ndarray:
    if not cells:
        return np.empty(
            (0, 2),
            dtype=np.int16,
        )
    return np.asarray(
        cells,
        dtype=np.int16,
    )


def set_cells(
    frame: np.ndarray,
    cells: Iterable[Cell],
    shift: int,
) -> None:
    cells = list(cells)
    if not cells:
        return
    arr = np.asarray(
        cells,
        dtype=np.int32,
    )
    frame[
        arr[:, 0] + shift,
        arr[:, 1] + shift,
    ] = True


def run_process(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group: int,
) -> SourceRun:
    radius = int(
        profile["radius"]
    )
    warmup = int(
        profile["warmup_steps"]
    )
    horizon = int(
        profile["continuation_steps"]
    )
    loss_rate = float(
        profile["loss_rate"]
    )
    budget = int(
        profile["budget"]
    )
    max_distance = int(
        profile["max_distance"]
    )
    radial_width = int(
        profile["radial_bin_width"]
    )

    size = (
        2 * radius + 1
    )
    shift = radius

    shape = (
        horizon,
        size,
        size,
    )

    attachment_frames = np.zeros(
        shape,
        dtype=bool,
    )
    loss_frames = np.zeros(
        shape,
        dtype=bool,
    )
    reoccupation_frames = np.zeros(
        shape,
        dtype=bool,
    )
    first_frames = np.zeros(
        shape,
        dtype=bool,
    )
    loss_eligible_frames = np.zeros(
        shape,
        dtype=bool,
    )

    src_attachment: List[np.ndarray] = []
    ctl_attachment: List[np.ndarray] = []
    src_loss: List[np.ndarray] = []
    ctl_loss: List[np.ndarray] = []

    gseed = (
        int(seed)
        + group * 1009
    )

    env = ch18.make_environment(
        warmup
        + horizon
        + 8,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        ch21.no_material_params(),
    )

    ledger = ch21.OccupancyLedger(
        set(state.occupied)
    )

    attachment_total_events = 0
    attachment_eligible_events = 0
    attachment_matched_events = 0

    loss_total_events = 0
    loss_eligible_events = 0
    loss_matched_events = 0

    max_capacity = 0.0
    collapsed = False

    for j in range(
        horizon
    ):
        before_growth = set(
            state.occupied
        )

        (
            after_growth,
            additions,
            evaluated,
            _frontier_count,
        ) = budgeted_growth_step_with_evaluated(
            state,
            float(
                env[
                    warmup + j
                ]
            ),
            radius,
            crystal_params,
            budget,
        )

        addition_set = set(
            additions
        )
        evaluated_set = set(
            evaluated
        )

        assert addition_set <= evaluated_set

        attachment_non_events = [
            cell
            for cell in evaluated
            if cell not in addition_set
        ]

        (
            matched_a,
            matched_a_ctl,
            eligible_a,
        ) = match_class(
            events=additions,
            controls=attachment_non_events,
            geometry_occupied=before_growth,
            radius=radius,
            max_distance=max_distance,
            radial_bin_width=radial_width,
            seed=seed,
            group=group,
            step=j,
            namespace="ch23-v2-attachment",
        )

        first_cells: Set[Cell] = set()
        reoccupied_cells: Set[Cell] = set()

        for cell in additions:
            if cell in ledger.currently_lost:
                reoccupied_cells.add(
                    cell
                )
            elif cell not in ledger.ever_occupied:
                first_cells.add(
                    cell
                )

        ledger.classify_additions(
            additions
        )

        before_loss = set(
            after_growth.occupied
        )

        set_cells(
            loss_eligible_frames[j],
            before_loss,
            shift,
        )

        after_loss, lost = (
            ch21.apply_background_loss(
                after_growth,
                loss_rate,
            )
        )

        lost_set = set(
            lost
        )

        loss_non_events = [
            cell
            for cell in before_loss
            if cell not in lost_set
        ]

        (
            matched_l,
            matched_l_ctl,
            eligible_l,
        ) = match_class(
            events=lost,
            controls=loss_non_events,
            geometry_occupied=before_loss,
            radius=radius,
            max_distance=max_distance,
            radial_bin_width=radial_width,
            seed=seed,
            group=group,
            step=j,
            namespace="ch23-v2-loss",
        )

        ledger.register_losses(
            lost
        )

        set_cells(
            attachment_frames[j],
            additions,
            shift,
        )
        set_cells(
            loss_frames[j],
            lost,
            shift,
        )
        set_cells(
            reoccupation_frames[j],
            reoccupied_cells,
            shift,
        )
        set_cells(
            first_frames[j],
            first_cells,
            shift,
        )

        src_attachment.append(
            cells_to_coords(
                matched_a
            )
        )
        ctl_attachment.append(
            cells_to_coords(
                matched_a_ctl
            )
        )
        src_loss.append(
            cells_to_coords(
                matched_l
            )
        )
        ctl_loss.append(
            cells_to_coords(
                matched_l_ctl
            )
        )

        assert (
            len(src_attachment[-1])
            == len(ctl_attachment[-1])
        )
        assert (
            len(src_loss[-1])
            == len(ctl_loss[-1])
        )

        attachment_total_events += len(
            additions
        )
        attachment_eligible_events += (
            eligible_a
        )
        attachment_matched_events += len(
            matched_a
        )

        loss_total_events += len(
            lost
        )
        loss_eligible_events += (
            eligible_l
        )
        loss_matched_events += len(
            matched_l
        )

        max_capacity = max(
            max_capacity,
            float(
                ch18.capacity_fraction_occupied(
                    after_loss.occupied,
                    radius,
                )
            ),
        )

        state = after_loss

        if not state.occupied:
            collapsed = True

            for _ in range(
                j + 1,
                horizon,
            ):
                src_attachment.append(
                    np.empty(
                        (0, 2),
                        dtype=np.int16,
                    )
                )
                ctl_attachment.append(
                    np.empty(
                        (0, 2),
                        dtype=np.int16,
                    )
                )
                src_loss.append(
                    np.empty(
                        (0, 2),
                        dtype=np.int16,
                    )
                )
                ctl_loss.append(
                    np.empty(
                        (0, 2),
                        dtype=np.int16,
                    )
                )
            break

    frames = DenseFrameSet(
        radius=radius,
        size=size,
        shift=shift,
        attachment=attachment_frames,
        loss=loss_frames,
        reoccupation=reoccupation_frames,
        first_occupation=first_frames,
        loss_eligible=loss_eligible_frames,
    )

    return SourceRun(
        group=group,
        frames=frames,
        source_attachment=src_attachment,
        control_attachment=ctl_attachment,
        source_loss=src_loss,
        control_loss=ctl_loss,
        attachment_total_events=attachment_total_events,
        attachment_eligible_events=attachment_eligible_events,
        attachment_matched_events=attachment_matched_events,
        loss_total_events=loss_total_events,
        loss_eligible_events=loss_eligible_events,
        loss_matched_events=loss_matched_events,
        max_capacity_fraction=max_capacity,
        collapsed=collapsed,
    )


# ============================================================================
# Vectorized shell observer
# ============================================================================

def shell_density(
    centers: np.ndarray,
    target_frame: np.ndarray,
    ring: np.ndarray,
    shift: int,
) -> float:
    if centers.size == 0:
        return float("nan")

    positions = (
        centers[:, None, :].astype(
            np.int32
        )
        + ring[
            None,
            :,
            :,
        ].astype(
            np.int32
        )
    )

    qi = (
        positions[:, :, 0]
        + shift
    )
    ri = (
        positions[:, :, 1]
        + shift
    )

    # Center exclusion guarantees full rings; this is still asserted.
    if (
        np.any(qi < 0)
        or np.any(ri < 0)
        or np.any(qi >= target_frame.shape[0])
        or np.any(ri >= target_frame.shape[1])
    ):
        raise RuntimeError(
            "boundary clipping reached V2 observer; source exclusion failed"
        )

    hits = target_frame[
        qi,
        ri,
    ]

    return float(
        np.mean(hits)
    )


def shell_conditional_hazard(
    centers: np.ndarray,
    event_frame: np.ndarray,
    eligible_frame: np.ndarray,
    ring: np.ndarray,
    shift: int,
) -> float:
    if centers.size == 0:
        return float("nan")

    positions = (
        centers[:, None, :].astype(
            np.int32
        )
        + ring[
            None,
            :,
            :,
        ].astype(
            np.int32
        )
    )

    qi = (
        positions[:, :, 0]
        + shift
    )
    ri = (
        positions[:, :, 1]
        + shift
    )

    if (
        np.any(qi < 0)
        or np.any(ri < 0)
        or np.any(qi >= event_frame.shape[0])
        or np.any(ri >= event_frame.shape[1])
    ):
        raise RuntimeError(
            "boundary clipping reached conditional observer"
        )

    eligible = eligible_frame[
        qi,
        ri,
    ]

    denom = int(
        np.sum(eligible)
    )

    if denom == 0:
        return float("nan")

    events = event_frame[
        qi,
        ri,
    ]

    numer = int(
        np.sum(
            events & eligible
        )
    )

    return float(
        numer
        / denom
    )


def source_lists(
    run: SourceRun,
    source_class: str,
) -> Tuple[
    List[np.ndarray],
    List[np.ndarray],
]:
    if source_class == "attachment":
        return (
            run.source_attachment,
            run.control_attachment,
        )
    if source_class == "loss":
        return (
            run.source_loss,
            run.control_loss,
        )
    raise KeyError(
        source_class
    )


def signed_surface(
    source_run: SourceRun,
    target_run: SourceRun,
    source_class: str,
    target_class: str,
    profile: dict,
) -> np.ndarray:
    """
    Signed source-minus-matched-control event density.

    Negative and positive lags use the same frozen common source-time window.
    """
    max_d = int(
        profile["max_distance"]
    )
    max_lag = int(
        profile["max_lag"]
    )
    horizon = int(
        profile["continuation_steps"]
    )

    distances = list(
        range(
            0,
            max_d + 1,
        )
    )
    lags = list(
        range(
            -max_lag,
            max_lag + 1,
        )
    )

    rings = {
        d: axial_ring_offsets(
            d
        )
        for d in distances
    }

    source_frames, control_frames = (
        source_lists(
            source_run,
            source_class,
        )
    )

    target = target_run.frames.target(
        target_class,
        0,
    )
    del target

    sum_source = np.zeros(
        (
            len(distances),
            len(lags),
        ),
        dtype=float,
    )
    sum_control = np.zeros_like(
        sum_source
    )
    weights = np.zeros_like(
        sum_source
    )

    common_start = max_lag
    common_stop = (
        horizon
        - max_lag
    )

    for t in range(
        common_start,
        common_stop,
    ):
        src = source_frames[t]
        ctl = control_frames[t]

        assert len(src) == len(ctl)

        n = len(src)

        if n == 0:
            continue

        for j, lag in enumerate(
            lags
        ):
            target_t = (
                t + lag
            )

            target_frame = (
                target_run.frames.target(
                    target_class,
                    target_t,
                )
            )

            for i, distance in enumerate(
                distances
            ):
                sd = shell_density(
                    src,
                    target_frame,
                    rings[
                        distance
                    ],
                    source_run.frames.shift,
                )
                cd = shell_density(
                    ctl,
                    target_frame,
                    rings[
                        distance
                    ],
                    source_run.frames.shift,
                )

                if (
                    math.isfinite(sd)
                    and math.isfinite(cd)
                ):
                    sum_source[i, j] += (
                        sd * n
                    )
                    sum_control[i, j] += (
                        cd * n
                    )
                    weights[i, j] += n

    with np.errstate(
        divide="ignore",
        invalid="ignore",
    ):
        source_mean = (
            sum_source
            / weights
        )
        control_mean = (
            sum_control
            / weights
        )

    source_mean[
        weights == 0
    ] = np.nan
    control_mean[
        weights == 0
    ] = np.nan

    return (
        source_mean
        - control_mean
    )


def conditional_loss_hazard_surface(
    source_run: SourceRun,
    target_run: SourceRun,
    profile: dict,
) -> np.ndarray:
    """
    loss-source minus matched-survivor-control future loss hazard,
    conditional on future target cells being occupied and therefore eligible
    for the frozen i.i.d. loss draw.
    """
    max_d = int(
        profile["max_distance"]
    )
    max_lag = int(
        profile["max_lag"]
    )
    horizon = int(
        profile["continuation_steps"]
    )

    distances = list(
        range(
            0,
            max_d + 1,
        )
    )
    lags = list(
        range(
            -max_lag,
            max_lag + 1,
        )
    )

    rings = {
        d: axial_ring_offsets(
            d
        )
        for d in distances
    }

    src_frames = (
        source_run.source_loss
    )
    ctl_frames = (
        source_run.control_loss
    )

    source_sum = np.zeros(
        (
            len(distances),
            len(lags),
        ),
        dtype=float,
    )
    control_sum = np.zeros_like(
        source_sum
    )
    counts = np.zeros_like(
        source_sum
    )

    common_start = max_lag
    common_stop = (
        horizon
        - max_lag
    )

    for t in range(
        common_start,
        common_stop,
    ):
        src = src_frames[t]
        ctl = ctl_frames[t]

        assert len(src) == len(ctl)

        if len(src) == 0:
            continue

        for j, lag in enumerate(
            lags
        ):
            target_t = (
                t + lag
            )

            event_frame = (
                target_run.frames.loss[
                    target_t
                ]
            )
            eligible_frame = (
                target_run.frames.loss_eligible[
                    target_t
                ]
            )

            for i, distance in enumerate(
                distances
            ):
                sh = (
                    shell_conditional_hazard(
                        src,
                        event_frame,
                        eligible_frame,
                        rings[
                            distance
                        ],
                        source_run.frames.shift,
                    )
                )
                ch = (
                    shell_conditional_hazard(
                        ctl,
                        event_frame,
                        eligible_frame,
                        rings[
                            distance
                        ],
                        source_run.frames.shift,
                    )
                )

                if (
                    math.isfinite(sh)
                    and math.isfinite(ch)
                ):
                    source_sum[i, j] += sh
                    control_sum[i, j] += ch
                    counts[i, j] += 1

    with np.errstate(
        divide="ignore",
        invalid="ignore",
    ):
        out = (
            source_sum
            / counts
            - control_sum
            / counts
        )

    out[
        counts == 0
    ] = np.nan

    return out


# ============================================================================
# Surface summaries
# ============================================================================

def lag_index(
    lag: int,
    max_lag: int,
) -> int:
    return int(
        lag + max_lag
    )


def causal_band_values(
    surface: np.ndarray,
    profile: dict,
    distances: Sequence[int],
) -> List[float]:
    max_lag = int(
        profile["max_lag"]
    )
    width = int(
        profile["band_width"]
    )

    values: List[float] = []

    for d in distances:
        start = max(
            1,
            int(d),
        )
        stop = min(
            max_lag,
            int(d) + width,
        )

        for tau in range(
            start,
            stop + 1,
        ):
            value = float(
                surface[
                    int(d),
                    lag_index(
                        tau,
                        max_lag,
                    ),
                ]
            )
            if math.isfinite(value):
                values.append(
                    value
                )

    return values


def causal_band_sum_by_distance(
    surface: np.ndarray,
    profile: dict,
) -> Dict[str, float]:
    max_d = int(
        profile["max_distance"]
    )
    max_lag = int(
        profile["max_lag"]
    )
    width = int(
        profile["band_width"]
    )

    result: Dict[
        str,
        float,
    ] = {}

    for d in range(
        0,
        max_d + 1,
    ):
        start = max(
            1,
            d,
        )
        stop = min(
            max_lag,
            d + width,
        )

        vals = [
            float(
                surface[
                    d,
                    lag_index(
                        tau,
                        max_lag,
                    ),
                ]
            )
            for tau in range(
                start,
                stop + 1,
            )
            if math.isfinite(
                float(
                    surface[
                        d,
                        lag_index(
                            tau,
                            max_lag,
                        ),
                    ]
                )
            )
        ]

        result[
            str(d)
        ] = (
            float(
                np.sum(vals)
            )
            if vals
            else float("nan")
        )

    return result


def forbidden_region_values(
    surface: np.ndarray,
    profile: dict,
) -> List[float]:
    max_d = int(
        profile["max_distance"]
    )
    max_lag = int(
        profile["max_lag"]
    )

    values: List[float] = []

    for d in range(
        1,
        max_d + 1,
    ):
        for tau in range(
            1,
            min(
                d,
                max_lag + 1,
            ),
        ):
            value = float(
                surface[
                    d,
                    lag_index(
                        tau,
                        max_lag,
                    ),
                ]
            )

            if math.isfinite(value):
                values.append(
                    value
                )

    return values


def forbidden_offset(
    surface: np.ndarray,
    profile: dict,
) -> float:
    values = forbidden_region_values(
        surface,
        profile,
    )
    return (
        float(
            np.mean(values)
        )
        if values
        else 0.0
    )


def forward_backward_asymmetry(
    surface: np.ndarray,
    profile: dict,
    distances: Sequence[int],
) -> float:
    max_lag = int(
        profile["max_lag"]
    )
    width = int(
        profile["band_width"]
    )

    values: List[float] = []

    for d in distances:
        start = max(
            1,
            int(d),
        )
        stop = min(
            max_lag,
            int(d) + width,
        )

        for tau in range(
            start,
            stop + 1,
        ):
            forward = float(
                surface[
                    int(d),
                    lag_index(
                        tau,
                        max_lag,
                    ),
                ]
            )
            backward = float(
                surface[
                    int(d),
                    lag_index(
                        -tau,
                        max_lag,
                    ),
                ]
            )

            if (
                math.isfinite(forward)
                and math.isfinite(backward)
            ):
                values.append(
                    forward
                    - backward
                )

    return (
        float(
            np.mean(values)
        )
        if values
        else float("nan")
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
        boot[i] = float(
            np.mean(
                rng.choice(
                    arr,
                    size=len(arr),
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
            len(arr)
        ),
        "mean": float(
            np.mean(arr)
        ),
        "ci95_low": low,
        "ci95_high": high,
        "half_width": float(
            (high - low)
            / 2.0
        ),
    }


def signflip_test(
    values: Sequence[float],
    permutations: int,
    seed: int,
    alternative: str,
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
            "alternative": alternative,
        }

    observed = float(
        np.mean(arr)
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
                [-1.0, 1.0],
            ),
            size=len(arr),
        )
        null[i] = float(
            np.mean(
                arr * signs
            )
        )

    if alternative == "less":
        extreme = int(
            np.sum(
                null <= observed
            )
        )
    elif alternative == "greater":
        extreme = int(
            np.sum(
                null >= observed
            )
        )
    elif alternative == "two-sided":
        extreme = int(
            np.sum(
                np.abs(null)
                >= abs(observed)
            )
        )
    else:
        raise ValueError(
            alternative
        )

    p = (
        1.0
        + extreme
    ) / (
        len(null)
        + 1.0
    )

    return {
        "n": int(
            len(arr)
        ),
        "observed_mean": observed,
        "p_value": float(p),
        "alternative": alternative,
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
            / "ch23-interface-source-sink-v2-full-report.md"
        )

        parts = [
            "# Chapter 23 — Does the Process Move? (V2)",
            "",
            "## Interface Source/Sink Transition Field",
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
# Protocol
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
    seed: int,
) -> dict:
    max_distance = int(
        profile["max_distance"]
    )
    max_lag = int(
        profile["max_lag"]
    )

    if max_lag < 2 * max_distance:
        raise ValueError(
            "V2 requires max_lag >= 2 * max_distance"
        )

    result = {
        "role": (
            "INTERFACE SOURCE/SINK TRANSITION FIELD"
        ),
        "fresh_seed": int(
            seed
        ),
        "v1_status": (
            "FAILED. Do not retune the V1 ridge statistic."
        ),
        "measurement_change": (
            "Signed source-class x target-class transition surfaces with "
            "negative lags; no positive-weighted centroid."
        ),
        "source_classes": list(
            SOURCE_CLASSES
        ),
        "target_classes": list(
            TARGET_CLASSES
        ),
        "subset_note": (
            "reoccupation and first_occupation are subsets of attachment"
        ),
        "distances": list(
            range(
                0,
                max_distance + 1,
            )
        ),
        "lags": list(
            range(
                -max_lag,
                max_lag + 1,
            )
        ),
        "uniform_grid": True,
        "max_lag_at_least_twice_max_distance": (
            max_lag
            >= 2 * max_distance
        ),
        "common_source_window": [
            max_lag,
            int(
                profile[
                    "continuation_steps"
                ]
                - max_lag
                - 1
            ),
        ],
        "band_width": int(
            profile[
                "band_width"
            ]
        ),
        "formal_representation": (
            "raw signed excess surface"
        ),
        "offset_corrected_surface_role": (
            "diagnostic only"
        ),
        "h1": (
            "Fresh-seed attachment -> attachment excess at d in {1,2} is "
            "negative by at least the frozen 5e-4 directional effect floor."
        ),
        "h2": (
            "Fresh-seed loss -> attachment excess at d in {0,1} is positive "
            "by at least the frozen 5e-4 directional effect floor."
        ),
        "h3": (
            "At d=1, late attachment -> attachment excess remains negative "
            "over the frozen late window and retains at least 50% of the "
            "absolute early deficit."
        ),
        "h4_validity": (
            "Future per-eligible-cell loss hazard around loss sources versus "
            "matched survivor controls remains within the frozen null "
            "tolerance."
        ),
        "positive_control": (
            "loss -> reoccupation must be positive at short range/lag; this "
            "recovers the independently established Chapter 20 mechanism."
        ),
        "propagation_test": (
            "attachment -> attachment forward/backward asymmetry at d>=3, "
            "compared with four-partner cross-run future null. Separate from "
            "short-range source/sink findings."
        ),
        "mde_signed_excess": float(
            profile[
                "mde_signed_excess"
            ]
        ),
        "mde_propagation_asymmetry": float(
            profile[
                "mde_propagation_asymmetry"
            ]
        ),
        "scientific_boundary": (
            "Interface source/sink dynamics only. Local opportunity "
            "consumption is a candidate mechanism until causal intervention. "
            "No refractory, wave, excitable-medium, individuality, autonomy, "
            "organism, agency, or life claim."
        ),
        "status": (
            "FROZEN"
            if profile["scientific"]
            else "ENGINEERING_SMOKE_ONLY"
        ),
    }

    reporter.json(
        "stage-00-protocol.json",
        result,
    )
    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen V2 Source/Sink Protocol",
        result,
    )

    return result


# ============================================================================
# Generate fresh runs
# ============================================================================

def stage_1_generate(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    List[SourceRun],
    dict,
]:
    runs: List[SourceRun] = []

    for group in tqdm(
        range(
            int(
                profile["groups"]
            )
        ),
        desc="Chapter 23 V2 fresh runs",
    ):
        runs.append(
            run_process(
                profile,
                crystal_params,
                seed,
                group,
            )
        )

    a_eligible = int(
        sum(
            run.attachment_eligible_events
            for run in runs
        )
    )
    a_matched = int(
        sum(
            run.attachment_matched_events
            for run in runs
        )
    )
    l_eligible = int(
        sum(
            run.loss_eligible_events
            for run in runs
        )
    )
    l_matched = int(
        sum(
            run.loss_matched_events
            for run in runs
        )
    )

    a_fraction = (
        a_matched
        / max(
            1,
            a_eligible,
        )
    )
    l_fraction = (
        l_matched
        / max(
            1,
            l_eligible,
        )
    )

    max_capacity = float(
        max(
            run.max_capacity_fraction
            for run in runs
        )
    )

    collapsed = int(
        sum(
            run.collapsed
            for run in runs
        )
    )

    result = {
        "groups": int(
            len(runs)
        ),
        "attachment": {
            "total_events": int(
                sum(
                    run.attachment_total_events
                    for run in runs
                )
            ),
            "interior_eligible_events": (
                a_eligible
            ),
            "matched_events": a_matched,
            "match_fraction": float(
                a_fraction
            ),
            "minimum_match_fraction": float(
                profile[
                    "minimum_attachment_match_fraction"
                ]
            ),
            "match_gate_passed": bool(
                a_fraction
                >= profile[
                    "minimum_attachment_match_fraction"
                ]
            ),
        },
        "loss": {
            "total_events": int(
                sum(
                    run.loss_total_events
                    for run in runs
                )
            ),
            "interior_eligible_events": (
                l_eligible
            ),
            "matched_events": l_matched,
            "match_fraction": float(
                l_fraction
            ),
            "minimum_match_fraction": float(
                profile[
                    "minimum_loss_match_fraction"
                ]
            ),
            "match_gate_passed": bool(
                l_fraction
                >= profile[
                    "minimum_loss_match_fraction"
                ]
            ),
        },
        "maximum_capacity_fraction": (
            max_capacity
        ),
        "max_allowed_capacity_fraction": float(
            profile[
                "max_capacity_fraction"
            ]
        ),
        "capacity_gate_passed": bool(
            max_capacity
            < profile[
                "max_capacity_fraction"
            ]
        ),
        "collapsed_groups": collapsed,
        "collapse_gate_passed": bool(
            collapsed == 0
        ),
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-fresh-runs.json",
        result,
    )
    reporter.stage(
        "stage-01-fresh-runs.md",
        "Stage 1 — Fresh-Seed Source/Control Runs",
        result,
    )

    return (
        runs,
        result,
    )


# ============================================================================
# Measure all channels
# ============================================================================

def channel_key(
    source: str,
    target: str,
) -> str:
    return (
        f"{source}_to_{target}"
    )


def stage_2_measure_channels(
    reporter: Reporter,
    profile: dict,
    runs: Sequence[SourceRun],
    seed: int,
    image_dir: Path,
) -> Tuple[dict, Dict[str, List[np.ndarray]]]:
    k = int(
        profile[
            "cross_run_partners"
        ]
    )

    if len(runs) <= k:
        raise ValueError(
            "need more runs than cross-run partners"
        )

    all_real: Dict[
        str,
        List[np.ndarray],
    ] = {
        channel_key(
            source,
            target,
        ): []
        for source, target in CHANNELS
    }

    all_null: Dict[
        str,
        List[np.ndarray],
    ] = {
        key: []
        for key in all_real
    }

    all_hazard: List[
        np.ndarray
    ] = []

    for i, run in enumerate(
        tqdm(
            runs,
            desc="Chapter 23 V2 transition fields",
        )
    ):
        partners = [
            runs[
                (i + offset)
                % len(runs)
            ]
            for offset in range(
                1,
                k + 1,
            )
        ]

        for source, target in CHANNELS:
            key = channel_key(
                source,
                target,
            )

            real = signed_surface(
                run,
                run,
                source,
                target,
                profile,
            )

            partner_surfaces = [
                signed_surface(
                    run,
                    partner,
                    source,
                    target,
                    profile,
                )
                for partner in partners
            ]

            null = np.nanmean(
                np.stack(
                    partner_surfaces,
                    axis=0,
                ),
                axis=0,
            )

            all_real[
                key
            ].append(
                real
            )
            all_null[
                key
            ].append(
                null
            )

        all_hazard.append(
            conditional_loss_hazard_surface(
                run,
                run,
                profile,
            )
        )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary: dict = {
        "channels": {},
        "conditional_loss_hazard": {},
        "formal_surface": (
            "raw signed excess"
        ),
        "corrected_surface": (
            "diagnostic only"
        ),
    }

    max_lag = int(
        profile[
            "max_lag"
        ]
    )

    for source, target in CHANNELS:
        key = channel_key(
            source,
            target,
        )

        real_stack = np.stack(
            all_real[
                key
            ],
            axis=0,
        )
        null_stack = np.stack(
            all_null[
                key
            ],
            axis=0,
        )

        real_mean = np.nanmean(
            real_stack,
            axis=0,
        )
        null_mean = np.nanmean(
            null_stack,
            axis=0,
        )

        raw_offset = forbidden_offset(
            real_mean,
            profile,
        )
        null_offset = forbidden_offset(
            null_mean,
            profile,
        )

        corrected = (
            real_mean
            - raw_offset
        )

        summary[
            "channels"
        ][
            key
        ] = {
            "real_surface": (
                real_mean.tolist()
            ),
            "cross_run_null_surface": (
                null_mean.tolist()
            ),
            "real_minus_null_surface": (
                (
                    real_mean
                    - null_mean
                ).tolist()
            ),
            "forbidden_region_offset": float(
                raw_offset
            ),
            "cross_run_forbidden_offset": float(
                null_offset
            ),
            "offset_corrected_real_surface_diagnostic": (
                corrected.tolist()
            ),
            "signed_band_sum_by_distance": (
                causal_band_sum_by_distance(
                    real_mean,
                    profile,
                )
            ),
        }

        # One figure per channel: no multipanel visual inference.
        fig, ax = plt.subplots(
            figsize=(9, 5),
        )

        im = ax.imshow(
            real_mean,
            aspect="auto",
            origin="lower",
        )

        distances = list(
            range(
                0,
                int(
                    profile[
                        "max_distance"
                    ]
                )
                + 1,
            )
        )
        lags = list(
            range(
                -max_lag,
                max_lag + 1,
            )
        )

        tick_positions = list(
            range(
                0,
                len(lags),
                max(
                    1,
                    len(lags) // 8,
                ),
            )
        )

        ax.set_xticks(
            tick_positions
        )
        ax.set_xticklabels(
            [
                lags[pos]
                for pos in tick_positions
            ]
        )
        ax.set_yticks(
            np.arange(
                len(distances)
            )
        )
        ax.set_yticklabels(
            distances
        )
        ax.set_xlabel(
            "Lag (updates)"
        )
        ax.set_ylabel(
            "Hex distance"
        )
        ax.set_title(
            f"Chapter 23 V2: {source} → {target}"
        )
        fig.colorbar(
            im,
            ax=ax,
            label=(
                "Signed excess event density"
            ),
        )
        fig.tight_layout()
        fig.savefig(
            image_dir
            / f"ch23-v2-{key}.png",
            dpi=160,
        )
        plt.close(fig)

    hazard_stack = np.stack(
        all_hazard,
        axis=0,
    )
    hazard_mean = np.nanmean(
        hazard_stack,
        axis=0,
    )

    summary[
        "conditional_loss_hazard"
    ] = {
        "loss_source_minus_survivor_control_surface": (
            hazard_mean.tolist()
        ),
        "max_absolute_population_difference": float(
            np.nanmax(
                np.abs(
                    hazard_mean
                )
            )
        ),
    }

    reporter.json(
        "stage-02-transition-fields.json",
        summary,
    )
    reporter.stage(
        "stage-02-transition-fields.md",
        "Stage 2 — Signed Source/Sink Transition Fields",
        summary,
    )

    return (
        summary,
        {
            "real": all_real,
            "null": all_null,
            "hazard": all_hazard,
        },
    )


# ============================================================================
# Hypothesis tests
# ============================================================================

def mean_selected_cells(
    surface: np.ndarray,
    profile: dict,
    cells: Sequence[
        Tuple[int, int]
    ],
) -> float:
    max_lag = int(
        profile[
            "max_lag"
        ]
    )

    values = [
        float(
            surface[
                int(d),
                lag_index(
                    int(tau),
                    max_lag,
                ),
            ]
        )
        for d, tau in cells
        if math.isfinite(
            float(
                surface[
                    int(d),
                    lag_index(
                        int(tau),
                        max_lag,
                    ),
                ]
            )
        )
    ]

    return (
        float(
            np.mean(values)
        )
        if values
        else float("nan")
    )


def stage_3_hypotheses(
    reporter: Reporter,
    profile: dict,
    measured: Dict[
        str,
        List[np.ndarray],
    ],
    seed: int,
) -> dict:
    mde = float(
        profile[
            "mde_signed_excess"
        ]
    )
    alpha = float(
        profile[
            "alpha"
        ]
    )
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
    max_lag = int(
        profile[
            "max_lag"
        ]
    )

    # H1: attachment -> attachment negative, d 1/2, causal band d..d+4.
    h1_cells: List[
        Tuple[int, int]
    ] = []

    for d in (1, 2):
        for tau in range(
            d,
            min(
                max_lag,
                d + int(
                    profile[
                        "band_width"
                    ]
                ),
            )
            + 1,
        ):
            h1_cells.append(
                (
                    d,
                    tau,
                )
            )

    h1_values = [
        mean_selected_cells(
            surface,
            profile,
            h1_cells,
        )
        for surface in measured[
            "real"
        ][
            "attachment_to_attachment"
        ]
    ]

    h1_summary = bootstrap_mean_ci(
        h1_values,
        reps,
        seed + 23101,
    )
    h1_test = signflip_test(
        h1_values,
        perms,
        seed + 23102,
        "less",
    )

    h1_supported = bool(
        h1_summary[
            "mean"
        ] <= -mde
        and h1_summary[
            "ci95_high"
        ] < 0.0
        and h1_test[
            "p_value"
        ] < alpha
    )

    # H2: loss -> attachment positive d 0/1, short causal band.
    h2_cells: List[
        Tuple[int, int]
    ] = []

    for d in (0, 1):
        start = max(
            1,
            d,
        )
        stop = min(
            max_lag,
            d + int(
                profile[
                    "band_width"
                ]
            ),
        )
        for tau in range(
            start,
            stop + 1,
        ):
            h2_cells.append(
                (
                    d,
                    tau,
                )
            )

    h2_values = [
        mean_selected_cells(
            surface,
            profile,
            h2_cells,
        )
        for surface in measured[
            "real"
        ][
            "loss_to_attachment"
        ]
    ]

    h2_summary = bootstrap_mean_ci(
        h2_values,
        reps,
        seed + 23201,
    )
    h2_test = signflip_test(
        h2_values,
        perms,
        seed + 23202,
        "greater",
    )

    h2_supported = bool(
        h2_summary[
            "mean"
        ] >= mde
        and h2_summary[
            "ci95_low"
        ] > 0.0
        and h2_test[
            "p_value"
        ] < alpha
    )

    # Positive control: loss -> reoccupation at d 0/1, lag 1/2.
    pc_cells = [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
    ]

    positive_control_values = [
        mean_selected_cells(
            surface,
            profile,
            pc_cells,
        )
        for surface in measured[
            "real"
        ][
            "loss_to_reoccupation"
        ]
    ]

    positive_control_summary = (
        bootstrap_mean_ci(
            positive_control_values,
            reps,
            seed + 23301,
        )
    )

    positive_control_passed = bool(
        positive_control_summary[
            "mean"
        ] > 0.0
        and positive_control_summary[
            "ci95_low"
        ] > 0.0
    )

    # H3: d=1 deficit persists from early to late frozen windows.
    early_lags = list(
        range(
            2,
            min(
                4,
                max_lag,
            )
            + 1,
        )
    )

    late_start = max(
        2,
        max_lag - 4,
    )
    late_lags = list(
        range(
            late_start,
            max_lag + 1,
        )
    )

    early_values: List[float] = []
    late_values: List[float] = []
    retained_values: List[float] = []

    for surface in measured[
        "real"
    ][
        "attachment_to_attachment"
    ]:
        early = mean_selected_cells(
            surface,
            profile,
            [
                (1, tau)
                for tau in early_lags
            ],
        )
        late = mean_selected_cells(
            surface,
            profile,
            [
                (1, tau)
                for tau in late_lags
            ],
        )

        early_values.append(
            early
        )
        late_values.append(
            late
        )

        if (
            math.isfinite(early)
            and math.isfinite(late)
            and early < 0.0
        ):
            retained_values.append(
                abs(late)
                / max(
                    abs(early),
                    1e-12,
                )
            )

    early_summary = bootstrap_mean_ci(
        early_values,
        reps,
        seed + 23401,
    )
    late_summary = bootstrap_mean_ci(
        late_values,
        reps,
        seed + 23402,
    )
    retained_summary = (
        bootstrap_mean_ci(
            retained_values,
            reps,
            seed + 23403,
        )
    )

    h3_supported = bool(
        late_summary[
            "mean"
        ] <= -mde
        and late_summary[
            "ci95_high"
        ] < 0.0
        and retained_summary[
            "mean"
        ] >= profile[
            "h3_min_retained_fraction"
        ]
    )

    # H4 validity: conditional future loss hazard should remain near zero.
    hazard_values: List[float] = []

    for surface in measured[
        "hazard"
    ]:
        vals = causal_band_values(
            surface,
            profile,
            distances=range(
                1,
                min(
                    4,
                    int(
                        profile[
                            "max_distance"
                        ]
                    ),
                )
                + 1,
            ),
        )
        hazard_values.append(
            float(
                np.mean(vals)
            )
            if vals
            else float("nan")
        )

    h4_summary = bootstrap_mean_ci(
        hazard_values,
        reps,
        seed + 23501,
    )

    h4_passed = bool(
        math.isfinite(
            h4_summary[
                "mean"
            ]
        )
        and abs(
            h4_summary[
                "mean"
            ]
        )
        <= profile[
            "h4_loss_hazard_tolerance"
        ]
        and h4_summary[
            "ci95_low"
        ]
        <= profile[
            "h4_loss_hazard_tolerance"
        ]
        and h4_summary[
            "ci95_high"
        ]
        >= -profile[
            "h4_loss_hazard_tolerance"
        ]
    )

    # Propagation: forward/backward asymmetry at d>=3, real minus 4-partner null.
    prop_distances = list(
        range(
            3,
            int(
                profile[
                    "max_distance"
                ]
            )
            + 1,
        )
    )

    real_prop = [
        forward_backward_asymmetry(
            surface,
            profile,
            prop_distances,
        )
        for surface in measured[
            "real"
        ][
            "attachment_to_attachment"
        ]
    ]

    null_prop = [
        forward_backward_asymmetry(
            surface,
            profile,
            prop_distances,
        )
        for surface in measured[
            "null"
        ][
            "attachment_to_attachment"
        ]
    ]

    prop_excess = [
        real - null
        for real, null in zip(
            real_prop,
            null_prop,
        )
        if (
            math.isfinite(real)
            and math.isfinite(null)
        )
    ]

    prop_summary = bootstrap_mean_ci(
        prop_excess,
        reps,
        seed + 23601,
    )
    prop_test = signflip_test(
        prop_excess,
        perms,
        seed + 23602,
        "two-sided",
    )

    propagation_supported = bool(
        abs(
            prop_summary[
                "mean"
            ]
        )
        >= profile[
            "mde_propagation_asymmetry"
        ]
        and prop_test[
            "p_value"
        ] < alpha
    )

    result = {
        "H1_attachment_associated_local_depletion": {
            "direction": "negative",
            "cells": [
                {
                    "distance": d,
                    "lag": tau,
                }
                for d, tau in h1_cells
            ],
            "minimum_effect": (
                -mde
            ),
            "summary": h1_summary,
            "signflip": h1_test,
            "status": (
                "SUPPORTED"
                if h1_supported
                else "FAILED"
            ),
            "bounded_claim_if_supported": (
                "On the fresh V2 seed, attachment events are followed by a "
                "scientifically meaningful short-range reduction in later "
                "attachment activity relative to matched non-attachment "
                "opportunities. Local opportunity consumption remains the "
                "candidate mechanism, not yet a causal mechanism claim."
            ),
        },
        "H2_loss_associated_interface_source": {
            "direction": "positive",
            "cells": [
                {
                    "distance": d,
                    "lag": tau,
                }
                for d, tau in h2_cells
            ],
            "minimum_effect": mde,
            "summary": h2_summary,
            "signflip": h2_test,
            "status": (
                "SUPPORTED"
                if h2_supported
                else "FAILED"
            ),
        },
        "positive_control_loss_to_reoccupation": {
            "cells": [
                {
                    "distance": d,
                    "lag": tau,
                }
                for d, tau in pc_cells
            ],
            "summary": (
                positive_control_summary
            ),
            "passed": (
                positive_control_passed
            ),
        },
        "H3_non_recovery_over_frozen_window": {
            "early_lags": early_lags,
            "late_lags": late_lags,
            "early_deficit": (
                early_summary
            ),
            "late_deficit": late_summary,
            "retained_absolute_fraction": (
                retained_summary
            ),
            "minimum_retained_fraction": float(
                profile[
                    "h3_min_retained_fraction"
                ]
            ),
            "status": (
                "SUPPORTED"
                if h3_supported
                else "FAILED"
            ),
            "interpretation_boundary": (
                "No recovery over the frozen observation window only; not "
                "permanent non-recovery and not 'refractory'."
            ),
        },
        "H4_conditional_loss_hazard_validity": {
            "tolerance": float(
                profile[
                    "h4_loss_hazard_tolerance"
                ]
            ),
            "summary": h4_summary,
            "passed": h4_passed,
            "role": (
                "VALIDITY CONTROL, not a scientific finding"
            ),
        },
        "propagation_forward_backward_asymmetry": {
            "channel": (
                "attachment_to_attachment"
            ),
            "distances": (
                prop_distances
            ),
            "real_minus_cross_run_null": (
                prop_summary
            ),
            "minimum_absolute_effect": float(
                profile[
                    "mde_propagation_asymmetry"
                ]
            ),
            "signflip": prop_test,
            "status": (
                "SUPPORTED"
                if propagation_supported
                else "FAILED"
            ),
            "interpretation_boundary": (
                "Propagation-like directed asymmetry only. No wave claim."
            ),
        },
        "achieved_precision": {
            "H1_bootstrap_half_width": (
                h1_summary[
                    "half_width"
                ]
            ),
            "H2_bootstrap_half_width": (
                h2_summary[
                    "half_width"
                ]
            ),
            "target_directional_effect_floor": (
                mde
            ),
        },
    }

    reporter.json(
        "stage-03-hypotheses.json",
        result,
    )
    reporter.stage(
        "stage-03-hypotheses.md",
        "Stage 3 — Fresh-Seed Source/Sink Hypotheses",
        result,
    )

    return result


# ============================================================================
# Final verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage3: dict,
) -> dict:
    validity = {
        "attachment_match": bool(
            stage1[
                "attachment"
            ][
                "match_gate_passed"
            ]
        ),
        "loss_match": bool(
            stage1[
                "loss"
            ][
                "match_gate_passed"
            ]
        ),
        "capacity": bool(
            stage1[
                "capacity_gate_passed"
            ]
        ),
        "collapse": bool(
            stage1[
                "collapse_gate_passed"
            ]
        ),
        "conditional_loss_hazard": bool(
            stage3[
                "H4_conditional_loss_hazard_validity"
            ][
                "passed"
            ]
        ),
        "loss_to_reoccupation_positive_control": bool(
            stage3[
                "positive_control_loss_to_reoccupation"
            ][
                "passed"
            ]
        ),
    }

    validity_ok = all(
        validity.values()
    )

    h1 = (
        stage3[
            "H1_attachment_associated_local_depletion"
        ][
            "status"
        ]
        == "SUPPORTED"
    )
    h2 = (
        stage3[
            "H2_loss_associated_interface_source"
        ][
            "status"
        ]
        == "SUPPORTED"
    )
    h3 = (
        stage3[
            "H3_non_recovery_over_frozen_window"
        ][
            "status"
        ]
        == "SUPPORTED"
    )
    propagation = (
        stage3[
            "propagation_forward_backward_asymmetry"
        ][
            "status"
        ]
        == "SUPPORTED"
    )

    if not profile["scientific"]:
        overall = (
            "ENGINEERING_SMOKE_ONLY"
        )
        bounded = (
            "Smoke profile completed. No scientific interpretation is "
            "eligible."
        )

    elif not validity_ok:
        overall = (
            "INVALID_FOR_SCIENTIFIC_INTERPRETATION"
        )
        bounded = (
            "One or more frozen validity controls failed. Do not interpret "
            "the source/sink or propagation hypotheses scientifically."
        )

    elif h1 and h2:
        overall = (
            "INTERFACE_SOURCE_SINK_SUPPORTED"
        )
        bounded = (
            "Under the fresh frozen Chapter 23 V2 protocol, attachment and "
            "loss exhibit opposite signed short-range relationships with "
            "future construction: attachment is followed by local depletion "
            "of later attachment activity while loss is followed by increased "
            "local attachment activity. This supports an operational "
            "interface source/sink description. Local opportunity consumption "
            "remains the candidate explanation for the attachment-associated "
            "depletion until directly intervened."
        )

    elif h1 or h2:
        overall = (
            "PARTIAL_SOURCE_SINK_SUPPORT"
        )
        bounded = (
            "Only one of the two frozen source/sink directions was supported. "
            "Do not promote the full interface source/sink model."
        )

    else:
        overall = (
            "SOURCE_SINK_HYPOTHESIS_FAILED"
        )
        bounded = (
            "Fresh Chapter 23 V2 did not confirm the paired interface "
            "source/sink hypothesis at the frozen effect floor."
        )

    result = {
        "validity": validity,
        "all_validity_gates_passed": (
            validity_ok
        ),
        "H1_local_depletion": (
            "SUPPORTED"
            if h1
            else "FAILED"
        ),
        "H2_loss_source": (
            "SUPPORTED"
            if h2
            else "FAILED"
        ),
        "H3_non_recovery_window": (
            "SUPPORTED"
            if h3
            else "FAILED"
        ),
        "propagation": (
            "SUPPORTED"
            if propagation
            else "FAILED"
        ),
        "overall_source_sink_status": (
            overall
        ),
        "bounded_claim": bounded,
        "important_separation": (
            "Interface source/sink dynamics and long-range propagation are "
            "independent verdicts. Source/sink dynamics can be supported while "
            "propagation fails."
        ),
        "forbidden_overclaims": [
            "refractory",
            "permanent non-recovery",
            "causally proven opportunity consumption",
            "wave",
            "wave equation",
            "excitable medium",
            "individual",
            "individuality",
            "autonomy",
            "self",
            "organism",
            "agency",
            "life",
        ],
        "next_if_source_sink_supported": (
            "Run a direct cell-keyed counterfactual attachment intervention: "
            "force versus prevent the same eligible attachment and measure "
            "later local construction opportunity. That can distinguish "
            "causal opportunity consumption from residual trajectory "
            "confounding."
        ),
        "next_if_propagation_supported": (
            "Confirm directed asymmetry on a fresh run and characterize "
            "distance-dependent velocity/dispersion before any wave language."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        result,
    )
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 23 V2 Verdict",
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
        # Fresh relative to V1's 20260902.
        default=20260903,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch23-interface-source-sink-v2"
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
            "FRESH CONFIRMATORY INTERFACE SOURCE/SINK TRANSITION FIELD"
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "v1_seed": 20260902,
        "fresh_seed_relative_to_v1": bool(
            int(args.seed)
            != 20260902
        ),
        "canonical_attachment_probability_modified": (
            False
        ),
        "canonical_loss_rule_modified": (
            False
        ),
        "canonical_budget_scheduling_modified": (
            False
        ),
        "observer_only_changes": [
            "exact evaluated-set return",
            "per-source-class matching",
            "signed transition surfaces",
            "negative lags",
            "common source-time window",
            "boundary exclusion",
            "four-partner cross-run null",
            "conditional loss-hazard validity control",
        ],
        "scientific_boundary": (
            "Interface source/sink dynamics and directed spatiotemporal "
            "asymmetry only. No refractory, permanent non-recovery, wave, "
            "excitable medium, individuality, autonomy, organism, agency, or "
            "life claim."
        ),
        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 23 V2 — INTERFACE SOURCE/SINK TRANSITION FIELD"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"radius={profile['radius']} "
        f"distance=0..{profile['max_distance']} "
        f"lag=-{profile['max_lag']}..+{profile['max_lag']} "
        f"seed={args.seed}"
    )
    print("=" * 78)

    stage_0_protocol(
        reporter,
        profile,
        args.seed,
    )

    runs, s1 = stage_1_generate(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    _s2, measured = (
        stage_2_measure_channels(
            reporter,
            profile,
            runs,
            args.seed,
            args.image_dir,
        )
    )

    s3 = stage_3_hypotheses(
        reporter,
        profile,
        measured,
        args.seed,
    )

    s4 = stage_4_verdict(
        reporter,
        profile,
        s1,
        s3,
    )

    metadata[
        "finished_at_unix"
    ] = time.time()
    metadata[
        "final_status"
    ] = s4[
        "overall_source_sink_status"
    ]
    metadata[
        "propagation_status"
    ] = s4[
        "propagation"
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
        "SOURCE/SINK STATUS:",
        s4[
            "overall_source_sink_status"
        ],
    )
    print(
        "PROPAGATION STATUS:",
        s4[
            "propagation"
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
    print("=" * 78)


if __name__ == "__main__":
    main()
