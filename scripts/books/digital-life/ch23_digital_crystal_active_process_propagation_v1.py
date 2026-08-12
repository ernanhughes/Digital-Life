#!/usr/bin/env python3
"""
Digital Life — Chapter 23
Does the Process Move? (V1)

Spatiotemporal active-process propagation screen
=================================================

Chapter 22 FAILED to establish either:
    - a privileged predictive spatial region, or
    - a privileged outer causal boundary.

What survived was spatial causal locality, while Chapters 18–21 repeatedly
implicated dynamically generated construction interfaces and process flux.

Chapter 23 therefore changes the experimental object.

It does NOT begin with:
    "the crystal is the occupied region inside radius R"

It asks:
    Does local process activity propagate through space-time with reproducible
    lag-distance structure beyond what is explained by current geometry,
    radial position, opportunity class, and generic time-dependent event rates?

Primary process events
----------------------
The V1 active-process field is deliberately event based.

A MATERIAL EVENT is either:
    - an attachment, or
    - a material loss.

For each event at location x and time t, the script asks whether later material
events occur at hex distance d and lag tau more often than around a matched
location that had the same local opportunity class but did NOT realize the
event.

Attachment controls:
    evaluated frontier candidates that did not attach,
    matched on radial bin and occupied-neighbour count.

Loss controls:
    occupied cells that survived the loss step,
    matched on radial bin and occupied-neighbour count.

This makes the local contrast:

    EVENT SOURCE
    versus
    GEOMETRY / OPPORTUNITY-MATCHED NON-EVENT SOURCE

A second null destroys process continuity while preserving the target frame's
time-dependent event burden:

    sources from run g
    versus
    future event frames from a different run at the same relative time.

This is the CROSS-RUN FUTURE NULL.

Primary lag-distance object
---------------------------
For frozen distances d and lags tau:

    excess(d, tau)
        =
        future event density around real event sources
        -
        future event density around matched non-event controls

If process activity merely persists locally, the strongest excess should remain
at short lag for every distance.

A propagation-like pattern instead predicts that the center of positive excess
moves to later lags as spatial distance increases.

For each distance d:

    ridge_center(d)
        =
        positive-excess-weighted mean lag

Primary group statistic:

    ridge_shift
        =
        mean ridge_center(far distances)
        -
        mean ridge_center(near distances)

The same statistic is computed using the cross-run future null.

Primary confirmatory gates
--------------------------
All gates must pass:

1. validity:
       matched-control fraction >= frozen minimum

2. real lag displacement:
       mean real ridge_shift >= 1.0 update

3. excess over cross-run future null:
       mean(real ridge_shift - null ridge_shift) >= 0.50 update

4. paired sign-flip:
       one-sided p < 0.05 for
       real ridge_shift - null ridge_shift

5. directional structure:
       population-level ridge-center slope across distance >= 0.15
       updates per hex cell

6. monotonic association:
       Spearman(distance, ridge_center) >= 0.60

No gate may be changed after seeing the result.

Interpretation boundary
-----------------------
Success supports only:

    reproducible spatiotemporal propagation-like organization of local
    Digital Crystal material-event activity under this frozen measurement.

It does NOT establish:
    wave
    wave equation
    phase
    dispersion relation
    individual
    individuality
    autonomy
    causal closure
    self
    organism
    agency
    life

A literal wave claim would require additional phase/dispersion evidence.

Failure means:
    do not tune the lag family, distance family, bin widths, or thresholds.
    Record spatial locality without demonstrated propagation under this screen.

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
EXPERIMENT_VERSION = "digital-crystal-active-process-propagation-v1"
SCHEMA_VERSION = 1
CHAPTER = 23
CHAPTER_TITLE = "Does the Process Move?"

Cell = Tuple[int, int]


PROFILES = {
    # Engineering-only smoke test. Never interpret scientifically.
    "smoke": {
        "groups": 8,
        "radius": 48,
        "warmup_steps": 14,
        "continuation_steps": 36,
        "loss_rate": 0.08,
        "budget": 96,
        "distances": [1, 2, 3, 4, 6],
        "lags": [1, 2, 3, 4, 6],
        "near_distances": [1, 2],
        "far_distances": [4, 6],
        "radial_bin_width": 3,
        "minimum_match_fraction": 0.50,
        "minimum_real_ridge_shift": 1.0,
        "minimum_null_excess_shift": 0.50,
        "minimum_ridge_slope": 0.15,
        "minimum_spearman": 0.60,
        "alpha": 0.05,
        "signflip_permutations": 1000,
        "bootstrap_reps": 500,
        "max_capacity_fraction": 0.75,
        "scientific": False,
    },

    "quick": {
        "groups": 48,
        "radius": 72,
        "warmup_steps": 20,
        "continuation_steps": 84,
        "loss_rate": 0.08,
        "budget": 96,
        "distances": [1, 2, 3, 4, 6, 8],
        "lags": [1, 2, 3, 4, 6, 8],
        "near_distances": [1, 2],
        "far_distances": [4, 6, 8],
        "radial_bin_width": 3,
        "minimum_match_fraction": 0.60,
        "minimum_real_ridge_shift": 1.0,
        "minimum_null_excess_shift": 0.50,
        "minimum_ridge_slope": 0.15,
        "minimum_spearman": 0.60,
        "alpha": 0.05,
        "signflip_permutations": 5000,
        "bootstrap_reps": 2000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },

    "standard": {
        "groups": 96,
        "radius": 80,
        "warmup_steps": 20,
        "continuation_steps": 112,
        "loss_rate": 0.08,
        "budget": 96,
        "distances": [1, 2, 3, 4, 6, 8, 10],
        "lags": [1, 2, 3, 4, 6, 8, 10],
        "near_distances": [1, 2],
        "far_distances": [6, 8, 10],
        "radial_bin_width": 3,
        "minimum_match_fraction": 0.60,
        "minimum_real_ridge_shift": 1.0,
        "minimum_null_excess_shift": 0.50,
        "minimum_ridge_slope": 0.15,
        "minimum_spearman": 0.60,
        "alpha": 0.05,
        "signflip_permutations": 10000,
        "bootstrap_reps": 4000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },

    "full": {
        "groups": 192,
        "radius": 96,
        "warmup_steps": 24,
        "continuation_steps": 144,
        "loss_rate": 0.08,
        "budget": 96,
        "distances": [1, 2, 3, 4, 6, 8, 10, 12],
        "lags": [1, 2, 3, 4, 6, 8, 10, 12],
        "near_distances": [1, 2],
        "far_distances": [8, 10, 12],
        "radial_bin_width": 3,
        "minimum_match_fraction": 0.60,
        "minimum_real_ridge_shift": 1.0,
        "minimum_null_excess_shift": 0.50,
        "minimum_ridge_slope": 0.15,
        "minimum_spearman": 0.60,
        "alpha": 0.05,
        "signflip_permutations": 20000,
        "bootstrap_reps": 6000,
        "max_capacity_fraction": 0.75,
        "scientific": True,
    },
}


# ============================================================================
# Small deterministic helpers
# ============================================================================

def stable_uniform(
    namespace: str,
    seed: int,
    group: int,
    step: int,
    cell: Cell,
    extra: int = 0,
) -> float:
    payload = (
        f"{namespace}|{seed}|{group}|{step}|{cell[0]}|{cell[1]}|{extra}"
    ).encode("utf-8")

    digest = hashlib.blake2b(
        payload,
        digest_size=8,
    ).digest()

    return int.from_bytes(
        digest,
        "big",
    ) / float(2**64)


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
) -> List[Cell]:
    """
    Exact axial-coordinate ring at hex distance `distance`.
    """
    d = int(distance)

    if d == 0:
        return [(0, 0)]

    out: List[Cell] = []

    # Start at direction 4 * d, then walk six sides.
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

    for side in range(6):
        dq, dr = directions[side]

        for _ in range(d):
            out.append((q, r))
            q += dq
            r += dr

    # Defensive invariant.
    unique = sorted(set(out))

    if len(unique) != 6 * d:
        raise RuntimeError(
            f"ring construction failed for d={d}: "
            f"{len(unique)} != {6*d}"
        )

    if any(
        ch18.hex_distance(cell) != d
        for cell in unique
    ):
        raise RuntimeError(
            f"ring contains wrong-distance cell for d={d}"
        )

    return unique


# ============================================================================
# Opportunity-matched source controls
# ============================================================================

def match_events_to_controls(
    events: Sequence[Cell],
    controls: Sequence[Cell],
    occupied_for_geometry: Set[Cell],
    radial_bin_width: int,
    seed: int,
    group: int,
    step: int,
    namespace: str,
) -> Tuple[List[Cell], List[Cell], int]:
    """
    One-to-one, without-replacement matching.

    Exact primary strata:
        occupied-neighbour count
        radial-distance bin

    If no exact control remains, leave the event unmatched.
    No post-hoc widening is allowed.
    """
    buckets: Dict[Tuple[int, int], List[Cell]] = defaultdict(list)

    for cell in controls:
        key = (
            occupied_neighbor_count(
                cell,
                occupied_for_geometry,
            ),
            radial_bin(
                cell,
                radial_bin_width,
            ),
        )
        buckets[key].append(cell)

    for key in list(buckets):
        buckets[key] = sorted(
            buckets[key],
            key=lambda c: (
                stable_uniform(
                    namespace + "-control-order",
                    seed,
                    group,
                    step,
                    c,
                ),
                c,
            ),
        )

    matched_events: List[Cell] = []
    matched_controls: List[Cell] = []
    unmatched = 0

    event_order = sorted(
        events,
        key=lambda c: (
            stable_uniform(
                namespace + "-event-order",
                seed,
                group,
                step,
                c,
            ),
            c,
        ),
    )

    for cell in event_order:
        key = (
            occupied_neighbor_count(
                cell,
                occupied_for_geometry,
            ),
            radial_bin(
                cell,
                radial_bin_width,
            ),
        )

        pool = buckets.get(
            key,
            [],
        )

        if pool:
            matched_events.append(
                cell
            )
            matched_controls.append(
                pool.pop()
            )
        else:
            unmatched += 1

    return (
        matched_events,
        matched_controls,
        unmatched,
    )


# ============================================================================
# Simulate and record the active-process event field
# ============================================================================

@dataclass
class ProcessRun:
    group: int
    stream_seed: int
    event_frames: List[Set[Cell]]
    source_frames: List[List[Cell]]
    control_frames: List[List[Cell]]
    attachment_frames: List[Set[Cell]]
    loss_frames: List[Set[Cell]]
    reoccupation_frames: List[Set[Cell]]
    first_occupation_frames: List[Set[Cell]]
    evaluated_frames: List[Set[Cell]]
    population: List[int]
    capacity: List[float]
    total_events: int
    matched_events: int
    unmatched_events: int


def run_process(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group: int,
) -> ProcessRun:
    radius = int(
        profile["radius"]
    )
    warmup_steps = int(
        profile["warmup_steps"]
    )
    horizon = int(
        profile["continuation_steps"]
    )
    budget = int(
        profile["budget"]
    )
    loss_rate = float(
        profile["loss_rate"]
    )
    radial_width = int(
        profile["radial_bin_width"]
    )

    gseed = (
        int(seed)
        + group * 1009
    )

    env = ch18.make_environment(
        warmup_steps
        + horizon
        + max(profile["lags"])
        + 16,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env,
        warmup_steps,
        gseed + 2,
        radius,
        crystal_params,
        ch21.no_material_params(),
    )

    ledger = ch21.OccupancyLedger(
        set(state.occupied)
    )

    event_frames: List[Set[Cell]] = []
    source_frames: List[List[Cell]] = []
    control_frames: List[List[Cell]] = []
    attachment_frames: List[Set[Cell]] = []
    loss_frames: List[Set[Cell]] = []
    reoccupation_frames: List[Set[Cell]] = []
    first_occupation_frames: List[Set[Cell]] = []
    evaluated_frames: List[Set[Cell]] = []
    population: List[int] = []
    capacity: List[float] = []

    total_events = 0
    matched_events = 0
    unmatched_events = 0

    for j in range(horizon):
        occupied_before_growth = set(
            state.occupied
        )

        frontier = ch21.frontier_cells(
            occupied_before_growth,
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

        state_after_growth, additions, _, _ = (
            ch21.budgeted_growth_step(
                state,
                float(
                    env[
                        warmup_steps + j
                    ]
                ),
                radius,
                crystal_params,
                budget,
            )
        )

        addition_set = set(
            additions
        )

        evaluated_nonattachments = [
            cell
            for cell in selected
            if cell not in addition_set
        ]

        (
            matched_attachment_sources,
            attachment_controls,
            attachment_unmatched,
        ) = match_events_to_controls(
                events=additions,
                controls=evaluated_nonattachments,
                occupied_for_geometry=occupied_before_growth,
                radial_bin_width=radial_width,
                seed=seed,
                group=group,
                step=j,
                namespace="ch23-attachment",
            )

        # Classify additions before registering this step's losses.
        first_cells: Set[Cell] = set()
        reoccupied_cells: Set[Cell] = set()

        for cell in additions:
            if cell in ledger.currently_lost:
                reoccupied_cells.add(cell)
            elif cell not in ledger.ever_occupied:
                first_cells.add(cell)

        # Keep the canonical observer ledger in sync.
        ledger.classify_additions(
            additions
        )

        occupied_before_loss = set(
            state_after_growth.occupied
        )

        state_after_loss, lost = (
            ch21.apply_background_loss(
                state_after_growth,
                loss_rate,
            )
        )

        lost_set = set(
            lost
        )

        surviving_occupied = [
            cell
            for cell in occupied_before_loss
            if cell not in lost_set
        ]

        (
            matched_loss_sources,
            loss_controls,
            loss_unmatched,
        ) = match_events_to_controls(
                events=lost,
                controls=surviving_occupied,
                occupied_for_geometry=occupied_before_loss,
                radial_bin_width=radial_width,
                seed=seed,
                group=group,
                step=j,
                namespace="ch23-loss",
            )

        ledger.register_losses(
            lost
        )

        # Each material event contributes one source and, when possible,
        # one opportunity/geometry-matched non-event source.
        sources = list(additions) + list(lost)
        controls = (
            list(attachment_controls)
            + list(loss_controls)
        )

        matched_sources = (
            matched_attachment_sources
            + matched_loss_sources
        )

        event_frames.append(
            set(sources)
        )
        source_frames.append(
            list(matched_sources)
        )
        control_frames.append(
            list(controls)
        )
        attachment_frames.append(
            set(additions)
        )
        loss_frames.append(
            set(lost)
        )
        reoccupation_frames.append(
            set(reoccupied_cells)
        )
        first_occupation_frames.append(
            set(first_cells)
        )
        evaluated_frames.append(
            set(selected)
        )
        population.append(
            len(state_after_loss.occupied)
        )
        capacity.append(
            ch18.capacity_fraction_occupied(
                state_after_loss.occupied,
                radius,
            )
        )

        total_events += len(
            sources
        )
        matched_events += len(
            matched_sources
        )
        unmatched_events += (
            attachment_unmatched
            + loss_unmatched
        )

        state = state_after_loss

        if not state.occupied:
            # Keep frame indexing stable if a smoke profile ever collapses.
            remaining = horizon - j - 1

            for _ in range(remaining):
                event_frames.append(set())
                source_frames.append([])
                control_frames.append([])
                attachment_frames.append(set())
                loss_frames.append(set())
                reoccupation_frames.append(set())
                first_occupation_frames.append(set())
                evaluated_frames.append(set())
                population.append(0)
                capacity.append(0.0)

            break

    return ProcessRun(
        group=group,
        stream_seed=int(state.stream_seed),
        event_frames=event_frames,
        source_frames=source_frames,
        control_frames=control_frames,
        attachment_frames=attachment_frames,
        loss_frames=loss_frames,
        reoccupation_frames=reoccupation_frames,
        first_occupation_frames=first_occupation_frames,
        evaluated_frames=evaluated_frames,
        population=population,
        capacity=capacity,
        total_events=total_events,
        matched_events=matched_events,
        unmatched_events=unmatched_events,
    )


# ============================================================================
# Lag-distance measurement
# ============================================================================

def shell_event_density(
    centers: Sequence[Cell],
    target_events: Set[Cell],
    ring_offsets: Sequence[Cell],
    radius: int,
) -> float:
    """
    Mean future-event density over valid exact-distance shell positions.

    Each center contributes:
        target events on valid shell / valid shell positions

    Centers are then averaged equally.
    """
    if not centers:
        return float("nan")

    per_center: List[float] = []

    for cq, cr in centers:
        hits = 0
        valid = 0

        for dq, dr in ring_offsets:
            cell = (
                cq + dq,
                cr + dr,
            )

            if ch18.hex_distance(cell) > radius:
                continue

            valid += 1

            if cell in target_events:
                hits += 1

        if valid > 0:
            per_center.append(
                hits / valid
            )

    if not per_center:
        return float("nan")

    return float(
        np.mean(
            per_center
        )
    )


def measure_surface(
    run: ProcessRun,
    target_run: ProcessRun,
    profile: dict,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Measure source-minus-matched-control future event density.

    `run` supplies source and matched-control frames.
    `target_run` supplies future event frames.

    Real surface:
        run == target_run

    Cross-run future null:
        target_run is a different group
    """
    distances = list(
        profile["distances"]
    )
    lags = list(
        profile["lags"]
    )
    radius = int(
        profile["radius"]
    )

    rings = {
        d: axial_ring_offsets(d)
        for d in distances
    }

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
    weights = np.zeros_like(
        source_sum
    )

    horizon = min(
        len(run.event_frames),
        len(target_run.event_frames),
    )

    for t in range(horizon):
        sources = run.source_frames[t]
        controls = run.control_frames[t]

        if (
            not sources
            or not controls
        ):
            continue

        # The matching design aims for exact equal counts.
        n = min(
            len(sources),
            len(controls),
        )

        if n <= 0:
            continue

        sources = sources[:n]
        controls = controls[:n]

        for j, lag in enumerate(lags):
            future_t = (
                t + int(lag)
            )

            if future_t >= horizon:
                continue

            target_events = (
                target_run.event_frames[
                    future_t
                ]
            )

            for i, distance in enumerate(
                distances
            ):
                ring = rings[
                    distance
                ]

                sd = shell_event_density(
                    sources,
                    target_events,
                    ring,
                    radius,
                )
                cd = shell_event_density(
                    controls,
                    target_events,
                    ring,
                    radius,
                )

                if (
                    math.isfinite(sd)
                    and math.isfinite(cd)
                ):
                    source_sum[i, j] += (
                        sd * n
                    )
                    control_sum[i, j] += (
                        cd * n
                    )
                    weights[i, j] += n

    with np.errstate(
        divide="ignore",
        invalid="ignore",
    ):
        source_density = (
            source_sum
            / weights
        )
        control_density = (
            control_sum
            / weights
        )

    source_density[
        weights == 0
    ] = np.nan
    control_density[
        weights == 0
    ] = np.nan

    excess = (
        source_density
        - control_density
    )

    return (
        source_density,
        control_density,
        excess,
    )


def positive_ridge_centers(
    excess: np.ndarray,
    lags: Sequence[int],
) -> np.ndarray:
    lag_arr = np.asarray(
        lags,
        dtype=float,
    )

    centers = np.full(
        excess.shape[0],
        np.nan,
        dtype=float,
    )

    for i in range(
        excess.shape[0]
    ):
        row = np.asarray(
            excess[i],
            dtype=float,
        )

        weights = np.where(
            np.isfinite(row),
            np.maximum(
                row,
                0.0,
            ),
            0.0,
        )

        total = float(
            np.sum(weights)
        )

        if total > 0.0:
            centers[i] = float(
                np.sum(
                    weights * lag_arr
                )
                / total
            )

    return centers


def ridge_shift(
    centers: np.ndarray,
    distances: Sequence[int],
    near_distances: Sequence[int],
    far_distances: Sequence[int],
) -> float:
    lookup = {
        int(d): float(
            centers[i]
        )
        for i, d in enumerate(
            distances
        )
        if math.isfinite(
            float(centers[i])
        )
    }

    near = [
        lookup[d]
        for d in near_distances
        if d in lookup
    ]
    far = [
        lookup[d]
        for d in far_distances
        if d in lookup
    ]

    if (
        not near
        or not far
    ):
        return float("nan")

    return float(
        np.mean(far)
        - np.mean(near)
    )


def spearman_no_scipy(
    x: Sequence[float],
    y: Sequence[float],
) -> float:
    """
    Spearman correlation without scipy.
    Distances are unique, so only y ties need average ranks.
    """
    x_arr = np.asarray(
        x,
        dtype=float,
    )
    y_arr = np.asarray(
        y,
        dtype=float,
    )

    mask = (
        np.isfinite(x_arr)
        & np.isfinite(y_arr)
    )

    x_arr = x_arr[mask]
    y_arr = y_arr[mask]

    if len(x_arr) < 3:
        return float("nan")

    def rankdata(
        arr: np.ndarray,
    ) -> np.ndarray:
        order = np.argsort(
            arr,
            kind="mergesort",
        )
        ranks = np.empty(
            len(arr),
            dtype=float,
        )

        start = 0

        while start < len(arr):
            end = start + 1
            value = arr[
                order[start]
            ]

            while (
                end < len(arr)
                and arr[
                    order[end]
                ] == value
            ):
                end += 1

            avg_rank = (
                start + end - 1
            ) / 2.0

            for pos in range(
                start,
                end,
            ):
                ranks[
                    order[pos]
                ] = avg_rank

            start = end

        return ranks

    rx = rankdata(
        x_arr
    )
    ry = rankdata(
        y_arr
    )

    if (
        np.std(rx) == 0
        or np.std(ry) == 0
    ):
        return float("nan")

    return float(
        np.corrcoef(
            rx,
            ry,
        )[0, 1]
    )


def ridge_slope(
    centers: np.ndarray,
    distances: Sequence[int],
) -> float:
    x = np.asarray(
        distances,
        dtype=float,
    )
    y = np.asarray(
        centers,
        dtype=float,
    )

    mask = (
        np.isfinite(x)
        & np.isfinite(y)
    )

    if int(
        np.sum(mask)
    ) < 3:
        return float("nan")

    return float(
        np.polyfit(
            x[mask],
            y[mask],
            1,
        )[0]
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
            value
            for value in values
            if math.isfinite(
                float(value)
            )
        ],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "mean": float("nan"),
            "ci95_low": float("nan"),
            "ci95_high": float("nan"),
            "n": 0,
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
        sample = rng.choice(
            arr,
            size=len(arr),
            replace=True,
        )
        boot[i] = float(
            np.mean(sample)
        )

    return {
        "mean": float(
            np.mean(arr)
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
        "n": int(
            len(arr)
        ),
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(
        [
            value
            for value in values
            if math.isfinite(
                float(value)
            )
        ],
        dtype=float,
    )

    if len(arr) == 0:
        return {
            "observed_mean": float("nan"),
            "p_value": float("nan"),
            "permutations": int(
                permutations
            ),
            "n": 0,
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

    p = (
        1.0
        + float(
            np.sum(
                null >= observed
            )
        )
    ) / (
        len(null)
        + 1.0
    )

    return {
        "observed_mean": observed,
        "p_value": float(p),
        "permutations": int(
            permutations
        ),
        "n": int(
            len(arr)
        ),
        "null_mean": float(
            np.mean(null)
        ),
        "null_q95": float(
            np.quantile(
                null,
                0.95,
            )
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
            / "ch23-active-process-propagation-v1-full-report.md"
        )

        parts = [
            "# Chapter 23 — Does the Process Move? (V1)",
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
# Stage 0
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": (
            "SPATIOTEMPORAL ACTIVE-PROCESS PROPAGATION SCREEN"
        ),
        "question": (
            "Does local Digital Crystal material-event activity show a "
            "reproducible lag-distance displacement beyond current geometry, "
            "radial position, opportunity class, and a cross-run future null?"
        ),
        "active_process_field_v1": {
            "material_event": [
                "attachment",
                "loss",
            ],
            "supporting_channels_recorded": [
                "evaluated frontier",
                "attachment",
                "loss",
                "reoccupation",
                "first occupation",
            ],
        },
        "source_control_design": {
            "attachment_event_control": (
                "evaluated-but-not-attached frontier candidate"
            ),
            "loss_event_control": (
                "occupied cell surviving the same loss step"
            ),
            "matching": [
                "occupied-neighbour count",
                "radial-distance bin",
                "same event opportunity class",
                "one-to-one without replacement",
            ],
        },
        "cross_run_future_null": (
            "Sources and matched controls from group g are evaluated against "
            "future event frames from a different group at the same relative "
            "time, preserving target-frame event burden while destroying "
            "within-process space-time continuity."
        ),
        "distances": list(
            profile["distances"]
        ),
        "lags": list(
            profile["lags"]
        ),
        "near_distances": list(
            profile["near_distances"]
        ),
        "far_distances": list(
            profile["far_distances"]
        ),
        "ridge_center": (
            "positive-excess-weighted mean lag at each exact hex distance"
        ),
        "primary_group_statistic": (
            "mean ridge center over frozen far distances minus mean ridge "
            "center over frozen near distances"
        ),
        "primary_success_gates": {
            "minimum_match_fraction": float(
                profile[
                    "minimum_match_fraction"
                ]
            ),
            "minimum_real_ridge_shift": float(
                profile[
                    "minimum_real_ridge_shift"
                ]
            ),
            "minimum_real_minus_null_shift": float(
                profile[
                    "minimum_null_excess_shift"
                ]
            ),
            "minimum_population_ridge_slope": float(
                profile[
                    "minimum_ridge_slope"
                ]
            ),
            "minimum_population_spearman": float(
                profile[
                    "minimum_spearman"
                ]
            ),
            "paired_signflip_alpha": float(
                profile[
                    "alpha"
                ]
            ),
        },
        "new_sentence_if_successful": (
            "Under the frozen Chapter 23 V1 measurement, local Digital Crystal "
            "material-event activity exhibits reproducible spatiotemporal "
            "lag-distance displacement beyond matched local opportunity and a "
            "cross-run future null."
        ),
        "scientific_boundary": (
            "Propagation-like process organization only. No wave, phase, "
            "dispersion, individuality, autonomy, self, organism, agency, or "
            "life claim."
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
        "Stage 0 — Frozen Propagation Screen",
        result,
    )

    return result


# ============================================================================
# Stage 1
# ============================================================================

def stage_1_generate_process_fields(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[List[ProcessRun], dict]:
    runs: List[ProcessRun] = []

    for group in tqdm(
        range(
            int(
                profile["groups"]
            )
        ),
        desc="Chapter 23 V1 process runs",
    ):
        runs.append(
            run_process(
                profile,
                crystal_params,
                seed,
                group,
            )
        )

    total_events = int(
        sum(
            run.total_events
            for run in runs
        )
    )
    matched_events = int(
        sum(
            run.matched_events
            for run in runs
        )
    )
    unmatched_events = int(
        sum(
            run.unmatched_events
            for run in runs
        )
    )

    match_fraction = (
        matched_events
        / max(
            1,
            total_events,
        )
    )

    maximum_capacity_fraction = float(
        max(
            max(run.capacity)
            if run.capacity
            else 0.0
            for run in runs
        )
    )

    collapsed_groups = int(
        sum(
            bool(
                run.population
                and run.population[-1] == 0
            )
            for run in runs
        )
    )

    result = {
        "groups": int(
            len(runs)
        ),
        "total_material_events": total_events,
        "matched_event_sources": matched_events,
        "unmatched_event_sources": unmatched_events,
        "match_fraction": float(
            match_fraction
        ),
        "minimum_match_fraction": float(
            profile[
                "minimum_match_fraction"
            ]
        ),
        "match_gate_passed": bool(
            match_fraction
            >= profile[
                "minimum_match_fraction"
            ]
        ),
        "maximum_capacity_fraction": (
            maximum_capacity_fraction
        ),
        "max_allowed_capacity_fraction": float(
            profile[
                "max_capacity_fraction"
            ]
        ),
        "capacity_gate_passed": bool(
            maximum_capacity_fraction
            < profile[
                "max_capacity_fraction"
            ]
        ),
        "collapsed_groups": collapsed_groups,
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-process-fields.json",
        result,
    )
    reporter.stage(
        "stage-01-process-fields.md",
        "Stage 1 — Generate Active-Process Event Fields",
        result,
    )

    return runs, result


# ============================================================================
# Stage 2
# ============================================================================

def stage_2_measure_lag_distance(
    reporter: Reporter,
    profile: dict,
    runs: Sequence[ProcessRun],
    seed: int,
    image_dir: Path,
) -> Tuple[dict, dict]:
    distances = list(
        profile["distances"]
    )
    lags = list(
        profile["lags"]
    )

    real_surfaces: List[np.ndarray] = []
    null_surfaces: List[np.ndarray] = []
    real_centers: List[np.ndarray] = []
    null_centers: List[np.ndarray] = []
    real_shifts: List[float] = []
    null_shifts: List[float] = []

    n_runs = len(runs)

    for i, run in enumerate(
        tqdm(
            runs,
            desc="Chapter 23 V1 lag-distance surfaces",
        )
    ):
        # Deterministic cross-run derangement by one position.
        null_target = runs[
            (i + 1) % n_runs
        ]

        _, _, real_excess = (
            measure_surface(
                run,
                run,
                profile,
            )
        )

        _, _, null_excess = (
            measure_surface(
                run,
                null_target,
                profile,
            )
        )

        rc = positive_ridge_centers(
            real_excess,
            lags,
        )
        nc = positive_ridge_centers(
            null_excess,
            lags,
        )

        rs = ridge_shift(
            rc,
            distances,
            profile[
                "near_distances"
            ],
            profile[
                "far_distances"
            ],
        )
        ns = ridge_shift(
            nc,
            distances,
            profile[
                "near_distances"
            ],
            profile[
                "far_distances"
            ],
        )

        real_surfaces.append(
            real_excess
        )
        null_surfaces.append(
            null_excess
        )
        real_centers.append(
            rc
        )
        null_centers.append(
            nc
        )
        real_shifts.append(
            rs
        )
        null_shifts.append(
            ns
        )

    real_stack = np.stack(
        real_surfaces,
        axis=0,
    )
    null_stack = np.stack(
        null_surfaces,
        axis=0,
    )

    pop_real_surface = np.nanmean(
        real_stack,
        axis=0,
    )
    pop_null_surface = np.nanmean(
        null_stack,
        axis=0,
    )
    pop_surface_excess = (
        pop_real_surface
        - pop_null_surface
    )

    pop_real_centers = (
        positive_ridge_centers(
            pop_real_surface,
            lags,
        )
    )
    pop_null_centers = (
        positive_ridge_centers(
            pop_null_surface,
            lags,
        )
    )

    slope = ridge_slope(
        pop_real_centers,
        distances,
    )
    spearman = spearman_no_scipy(
        distances,
        pop_real_centers,
    )

    paired_shift_excess = [
        real - null
        for real, null in zip(
            real_shifts,
            null_shifts,
        )
        if (
            math.isfinite(
                float(real)
            )
            and math.isfinite(
                float(null)
            )
        )
    ]

    real_shift_summary = (
        bootstrap_mean_ci(
            real_shifts,
            profile[
                "bootstrap_reps"
            ],
            seed + 2301,
        )
    )

    null_shift_summary = (
        bootstrap_mean_ci(
            null_shifts,
            profile[
                "bootstrap_reps"
            ],
            seed + 2302,
        )
    )

    excess_shift_summary = (
        bootstrap_mean_ci(
            paired_shift_excess,
            profile[
                "bootstrap_reps"
            ],
            seed + 2303,
        )
    )

    paired_test = signflip_greater(
        paired_shift_excess,
        profile[
            "signflip_permutations"
        ],
        seed + 2304,
    )

    result = {
        "distances": distances,
        "lags": lags,
        "population_real_excess_surface": (
            pop_real_surface.tolist()
        ),
        "population_cross_run_null_surface": (
            pop_null_surface.tolist()
        ),
        "population_real_minus_null_surface": (
            pop_surface_excess.tolist()
        ),
        "population_real_ridge_centers": (
            pop_real_centers.tolist()
        ),
        "population_null_ridge_centers": (
            pop_null_centers.tolist()
        ),
        "population_real_ridge_slope": float(
            slope
        ),
        "population_real_ridge_spearman": float(
            spearman
        ),
        "real_group_ridge_shift": (
            real_shift_summary
        ),
        "null_group_ridge_shift": (
            null_shift_summary
        ),
        "real_minus_null_group_ridge_shift": (
            excess_shift_summary
        ),
        "paired_signflip_test": (
            paired_test
        ),
        "groups_with_finite_paired_shift": int(
            len(
                paired_shift_excess
            )
        ),
        "status": "MEASURED",
    }

    reporter.json(
        "stage-02-lag-distance.json",
        result,
    )
    reporter.stage(
        "stage-02-lag-distance.md",
        "Stage 2 — Lag-Distance Propagation Measurement",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Figure 1 — real matched-control excess surface.
    fig, ax = plt.subplots(
        figsize=(8, 5),
    )
    im = ax.imshow(
        pop_real_surface,
        aspect="auto",
        origin="lower",
    )
    ax.set_xticks(
        np.arange(
            len(lags)
        )
    )
    ax.set_xticklabels(
        lags
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
        "Chapter 23 V1: real event-source excess future activity"
    )
    fig.colorbar(
        im,
        ax=ax,
        label=(
            "Future event density excess over "
            "matched non-event sources"
        ),
    )
    fig.tight_layout()
    fig.savefig(
        image_dir
        / "ch23-v1-01-real-lag-distance.png",
        dpi=160,
    )
    plt.close(fig)

    # Figure 2 — cross-run future null surface.
    fig, ax = plt.subplots(
        figsize=(8, 5),
    )
    im = ax.imshow(
        pop_null_surface,
        aspect="auto",
        origin="lower",
    )
    ax.set_xticks(
        np.arange(
            len(lags)
        )
    )
    ax.set_xticklabels(
        lags
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
        "Chapter 23 V1: cross-run future null"
    )
    fig.colorbar(
        im,
        ax=ax,
        label=(
            "Future event density excess over "
            "matched non-event sources"
        ),
    )
    fig.tight_layout()
    fig.savefig(
        image_dir
        / "ch23-v1-02-cross-run-null.png",
        dpi=160,
    )
    plt.close(fig)

    # Figure 3 — population ridge centers.
    fig, ax = plt.subplots(
        figsize=(8, 5),
    )
    ax.plot(
        distances,
        pop_real_centers,
        marker="o",
        label="real",
    )
    ax.plot(
        distances,
        pop_null_centers,
        marker="o",
        label="cross-run null",
    )
    ax.set_xlabel(
        "Hex distance"
    )
    ax.set_ylabel(
        "Positive-excess weighted lag"
    )
    ax.set_title(
        "Chapter 23 V1: lag ridge center versus distance"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir
        / "ch23-v1-03-ridge-centers.png",
        dpi=160,
    )
    plt.close(fig)

    plot_manifest = {
        "real_surface": (
            "ch23-v1-01-real-lag-distance.png"
        ),
        "cross_run_null_surface": (
            "ch23-v1-02-cross-run-null.png"
        ),
        "ridge_centers": (
            "ch23-v1-03-ridge-centers.png"
        ),
    }

    return result, plot_manifest


# ============================================================================
# Stage 3
# ============================================================================

def stage_3_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
) -> dict:
    match_ok = bool(
        stage1[
            "match_gate_passed"
        ]
    )

    capacity_ok = bool(
        stage1[
            "capacity_gate_passed"
        ]
    )

    real_shift = float(
        stage2[
            "real_group_ridge_shift"
        ][
            "mean"
        ]
    )

    excess_shift = float(
        stage2[
            "real_minus_null_group_ridge_shift"
        ][
            "mean"
        ]
    )

    p_value = float(
        stage2[
            "paired_signflip_test"
        ][
            "p_value"
        ]
    )

    slope = float(
        stage2[
            "population_real_ridge_slope"
        ]
    )

    spearman = float(
        stage2[
            "population_real_ridge_spearman"
        ]
    )

    real_shift_ok = bool(
        math.isfinite(real_shift)
        and real_shift
        >= profile[
            "minimum_real_ridge_shift"
        ]
    )

    excess_shift_ok = bool(
        math.isfinite(excess_shift)
        and excess_shift
        >= profile[
            "minimum_null_excess_shift"
        ]
    )

    p_ok = bool(
        math.isfinite(p_value)
        and p_value
        < profile[
            "alpha"
        ]
    )

    slope_ok = bool(
        math.isfinite(slope)
        and slope
        >= profile[
            "minimum_ridge_slope"
        ]
    )

    spearman_ok = bool(
        math.isfinite(spearman)
        and spearman
        >= profile[
            "minimum_spearman"
        ]
    )

    finite_groups_ok = bool(
        stage2[
            "groups_with_finite_paired_shift"
        ]
        >= max(
            4,
            int(
                0.50
                * profile[
                    "groups"
                ]
            ),
        )
    )

    validity_ok = all([
        match_ok,
        capacity_ok,
        finite_groups_ok,
    ])

    supported = all([
        validity_ok,
        real_shift_ok,
        excess_shift_ok,
        p_ok,
        slope_ok,
        spearman_ok,
    ])

    if not profile["scientific"]:
        status = (
            "ENGINEERING_SMOKE_ONLY"
        )
        bounded = (
            "Smoke profile completed. This profile is not eligible for a "
            "scientific Chapter 23 claim."
        )

    elif supported:
        status = "SUPPORTED"
        bounded = (
            "Under the frozen Chapter 23 V1 event-field measurement, local "
            "Digital Crystal material-event activity showed reproducible "
            "lag-distance displacement: farther activity was centered at later "
            "lags, the displacement exceeded the cross-run future null by the "
            "predeclared magnitude, and the paired sign-flip and population "
            "ridge-direction gates passed. This supports propagation-like "
            "spatiotemporal process organization under the tested substrate. "
            "It does not establish a wave, phase, dispersion, individuality, "
            "autonomy, or life."
        )

    else:
        status = "FAILED"
        bounded = (
            "Chapter 23 V1 did not satisfy all frozen gates required to claim "
            "propagation-like spatiotemporal organization of Digital Crystal "
            "material-event activity beyond matched local opportunity and the "
            "cross-run future null. Spatial causal locality from Chapter 22 "
            "remains measured; propagation is not established by this screen."
        )

    result = {
        "question": (
            "Does local material-event activity exhibit propagation-like "
            "lag-distance displacement beyond matched local opportunity and a "
            "cross-run future null?"
        ),
        "validity": {
            "match_gate_passed": match_ok,
            "capacity_gate_passed": capacity_ok,
            "finite_group_gate_passed": (
                finite_groups_ok
            ),
            "all_validity_gates_passed": (
                validity_ok
            ),
        },
        "real_ridge_shift_mean": real_shift,
        "minimum_real_ridge_shift": float(
            profile[
                "minimum_real_ridge_shift"
            ]
        ),
        "real_ridge_shift_gate_passed": (
            real_shift_ok
        ),
        "real_minus_null_shift_mean": (
            excess_shift
        ),
        "minimum_real_minus_null_shift": float(
            profile[
                "minimum_null_excess_shift"
            ]
        ),
        "real_minus_null_gate_passed": (
            excess_shift_ok
        ),
        "paired_signflip_p_value": p_value,
        "alpha": float(
            profile[
                "alpha"
            ]
        ),
        "significance_gate_passed": p_ok,
        "population_ridge_slope": slope,
        "minimum_ridge_slope": float(
            profile[
                "minimum_ridge_slope"
            ]
        ),
        "ridge_slope_gate_passed": slope_ok,
        "population_ridge_spearman": (
            spearman
        ),
        "minimum_spearman": float(
            profile[
                "minimum_spearman"
            ]
        ),
        "spearman_gate_passed": (
            spearman_ok
        ),
        "status": status,
        "bounded_claim": bounded,
        "forbidden_overclaims": [
            "wave",
            "wave equation",
            "phase",
            "dispersion relation",
            "individual",
            "individuality",
            "autonomy",
            "causal closure",
            "self",
            "organism",
            "agency",
            "life",
        ],
        "next_question_if_supported": (
            "Run a fresh causal intervention on the measured active-process "
            "field: perturb an upstream activity patch and test whether the "
            "predicted downstream lag-distance region changes preferentially. "
            "Do not yet use individuality terminology."
        ),
        "next_question_if_failed": (
            "Do not retune distances, lags, matching strata, or success "
            "thresholds. Record local causal structure without demonstrated "
            "propagation and reconsider whether the active field is locally "
            "persistent, dispersive, or only geometry-driven."
        ),
    }

    reporter.json(
        "stage-03-verdict.json",
        result,
    )
    reporter.stage(
        "stage-03-verdict.md",
        "Stage 3 — Bounded Chapter 23 V1 Verdict",
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
        default=20260902,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch23-active-process-propagation-v1"
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
        "run_type": (
            "SPATIOTEMPORAL ACTIVE-PROCESS PROPAGATION SCREEN"
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": int(
            args.seed
        ),
        "canonical_attachment_rule_modified": (
            False
        ),
        "canonical_loss_rule_modified": (
            False
        ),
        "canonical_budget_rule_modified": (
            False
        ),
        "scientific_boundary": (
            "Propagation-like spatiotemporal process organization only. "
            "No wave, phase, dispersion, individuality, autonomy, self, "
            "organism, agency, or life claim."
        ),
        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 23 V1 — DOES THE PROCESS MOVE?"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"budget={profile['budget']} "
        f"loss={profile['loss_rate']} "
        f"distances={profile['distances']} "
        f"lags={profile['lags']}"
    )
    print("=" * 78)

    stage_0_protocol(
        reporter,
        profile,
    )

    runs, s1 = (
        stage_1_generate_process_fields(
            reporter,
            profile,
            crystal_params,
            args.seed,
        )
    )

    s2, plot_manifest = (
        stage_2_measure_lag_distance(
            reporter,
            profile,
            runs,
            args.seed,
            args.image_dir,
        )
    )

    s3 = stage_3_verdict(
        reporter,
        profile,
        s1,
        s2,
    )

    metadata[
        "finished_at_unix"
    ] = time.time()
    metadata[
        "final_status"
    ] = s3[
        "status"
    ]
    metadata[
        "plot_manifest"
    ] = plot_manifest

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
        f"FINAL STATUS: {s3['status']}"
    )
    print(
        s3[
            "bounded_claim"
        ]
    )
    print(
        f"Report: {report_path}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
