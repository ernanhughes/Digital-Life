#!/usr/bin/env python3
"""
Chapter 22 — When Does the Process Become One Thing? (V1)

Predictive coherence screen
===========================

Chapter 21 established a lossy Digital Crystal with finite computational
opportunity and strikingly stable normalized material turnover, but it did not
establish that the continuing process constitutes a natural individual.

Chapter 22 begins by asking a weaker question:

    Does any predeclared spatial scale contain predictive information about
    its own future beyond that available from the surrounding lattice?

V1 is observational/predictive only.

It does NOT establish:
    causal individuality
    autonomy
    causal closure
    organism
    self
    agency
    life

Fresh frozen protocol
---------------------

Substrate:
    Digital Crystal v1 frozen attachment rule
    loss rate delta = 0.08
    neutral finite evaluation budget B = 96

Candidate spatial scales:
    R / R_eff = 0.30, 0.45, 0.60, 0.75, 0.90

At each measurement checkpoint:

    S_t = dynamic state of centered candidate region
    E_t = dynamic state of surrounding active annulus
    S_future = candidate-region dynamic state tau updates later

State features are deliberately process-oriented rather than raw occupancy
alone.  Features include normalized population/frontier structure plus recent
attachment, loss, reoccupation, first-occupation and turnover flows, with a
small angular-sector decomposition.

Prediction models
-----------------

For each candidate scale:

    MODEL_E:
        predict S_future from E_t

    MODEL_SE:
        predict S_future from S_t + E_t

Held-out groups are used for evaluation.

Unique self-prediction:

    Delta_self =
        score(S_t + E_t -> S_future)
        -
        score(E_t -> S_future)

Geometry-matched observer null
------------------------------

A null "system" representation is built at each checkpoint by preserving the
candidate region's radial-bin occupancy/activity counts while randomly
reassigning angular membership using keyed observer-only scrambling.

The null does NOT feed back into the Digital Crystal dynamics.

The same prediction comparison is made for the null representation:

    Delta_self_null

Primary statistic:

    EXCESS_PREDICTIVE_COHERENCE =
        Delta_self_real - Delta_self_null

Primary family-level test
-------------------------

The candidate scales are frozen before the fresh run.

The primary family statistic is the maximum excess coherence across the frozen
scale family.

A run-group permutation null is used to estimate how large that family maximum
can become when current system-state vectors are paired with future vectors from
different run groups, preserving the decoder and scale-selection procedure.

Primary success requires:

    observed family max excess >= frozen SEI
    and permutation p < alpha

SEI:
    +0.02 held-out multivariate R^2

This is a predictive screen only.

If supported, the next experiment must use causal intervention.
If failed, do not tune radii or decoder complexity.

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
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-predictive-coherence-v1"
SCHEMA_VERSION = 1
CHAPTER = 22
CHAPTER_TITLE = "When Does the Process Become One Thing?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 96,
        "radius": 72,
        "warmup_steps": 20,
        "continuation_steps": 84,
        "loss_rate": 0.08,
        "budget": 96,

        "candidate_radius_fractions": [
            0.30,
            0.45,
            0.60,
            0.75,
            0.90,
        ],

        "history_window": 4,
        "prediction_horizon": 4,
        "checkpoint_stride": 4,
        "first_checkpoint_after_warmup": 12,

        "sector_count": 6,
        "radial_null_bins": 6,

        "ridge_alpha": 10.0,
        "test_fraction": 0.25,

        "primary_sei_excess_r2": 0.02,
        "permutations": 1000,
        "alpha": 0.05,

        "max_capacity_fraction": 0.75,
    },

    "standard": {
        "groups": 192,
        "radius": 80,
        "warmup_steps": 20,
        "continuation_steps": 112,
        "loss_rate": 0.08,
        "budget": 96,

        "candidate_radius_fractions": [
            0.30,
            0.45,
            0.60,
            0.75,
            0.90,
        ],

        "history_window": 4,
        "prediction_horizon": 4,
        "checkpoint_stride": 4,
        "first_checkpoint_after_warmup": 12,

        "sector_count": 6,
        "radial_null_bins": 6,

        "ridge_alpha": 10.0,
        "test_fraction": 0.25,

        "primary_sei_excess_r2": 0.02,
        "permutations": 3000,
        "alpha": 0.05,

        "max_capacity_fraction": 0.75,
    },

    "full": {
        "groups": 384,
        "radius": 96,
        "warmup_steps": 20,
        "continuation_steps": 144,
        "loss_rate": 0.08,
        "budget": 96,

        "candidate_radius_fractions": [
            0.30,
            0.45,
            0.60,
            0.75,
            0.90,
        ],

        "history_window": 4,
        "prediction_horizon": 4,
        "checkpoint_stride": 4,
        "first_checkpoint_after_warmup": 12,

        "sector_count": 6,
        "radial_null_bins": 6,

        "ridge_alpha": 10.0,
        "test_fraction": 0.25,

        "primary_sei_excess_r2": 0.02,
        "permutations": 5000,
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
        "ch22-v1-schedule",
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
        "ch22-v1-loss",
        stream_seed,
        step,
        cell,
    )


def null_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
    scale_index: int,
) -> float:
    return keyed_uniform(
        "ch22-v1-null",
        stream_seed,
        step,
        cell,
        scale_index,
    )


# ============================================================================
# Observer-only history ledger
# ============================================================================

class OccupancyLedger:
    def __init__(
        self,
        occupied: Set[Cell],
    ):
        self.ever_occupied = set(
            occupied
        )
        self.currently_lost: Set[Cell] = set()

    def classify_additions(
        self,
        additions: Sequence[Cell],
    ) -> Tuple[List[Cell], List[Cell]]:
        first: List[Cell] = []
        reoccupied: List[Cell] = []

        for cell in additions:
            if cell in self.currently_lost:
                reoccupied.append(cell)
                self.currently_lost.discard(cell)

            elif cell not in self.ever_occupied:
                first.append(cell)

            self.ever_occupied.add(cell)

        return first, reoccupied

    def register_losses(
        self,
        lost: Sequence[Cell],
    ) -> None:
        for cell in lost:
            self.currently_lost.add(cell)


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
            + crystal_params.neighbor_gain
            * n
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
        ) < float(
            loss_rate
        )
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
# Geometry / region representation
# ============================================================================

def axial_to_xy(
    cell: Cell,
) -> Tuple[float, float]:
    q, r = cell
    x = q + 0.5 * r
    y = (math.sqrt(3.0) / 2.0) * r
    return x, y


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


def cell_angle(
    cell: Cell,
) -> float:
    x, y = axial_to_xy(
        cell
    )

    theta = math.atan2(
        y,
        x,
    )

    if theta < 0:
        theta += (
            2.0 * math.pi
        )

    return theta


def effective_radius(
    occupied: Set[Cell],
) -> float:
    if not occupied:
        return 1.0

    return max(
        1.0,
        max(
            euclidean_radius(
                c
            )
            for c in occupied
        ),
    )


def region_membership(
    cells: Iterable[Cell],
    radius_cutoff: float,
) -> Set[Cell]:
    return {
        c
        for c in cells
        if euclidean_radius(
            c
        ) <= radius_cutoff
    }


def annulus_membership(
    cells: Iterable[Cell],
    inner_radius: float,
    outer_radius: float,
) -> Set[Cell]:
    return {
        c
        for c in cells
        if (
            euclidean_radius(c)
            > inner_radius
            and euclidean_radius(c)
            <= outer_radius
        )
    }


def sector_index(
    cell: Cell,
    sector_count: int,
) -> int:
    theta = cell_angle(
        cell
    )

    return min(
        sector_count - 1,
        int(
            theta
            / (2.0 * math.pi)
            * sector_count
        ),
    )


# ============================================================================
# Observer-side event frames
# ============================================================================

@dataclass
class StepFrame:
    step: int
    occupied: Set[Cell]
    frontier: Set[Cell]
    additions: Set[Cell]
    losses: Set[Cell]
    first: Set[Cell]
    reoccupations: Set[Cell]


def make_frame(
    step: int,
    state: ch18.MaterialCrystalState,
    additions: Sequence[Cell],
    losses: Sequence[Cell],
    first: Sequence[Cell],
    reoccupations: Sequence[Cell],
    radius: int,
) -> StepFrame:
    occupied = set(
        state.occupied
    )

    return StepFrame(
        step=step,
        occupied=occupied,
        frontier=set(
            frontier_cells(
                occupied,
                radius,
            )
        ),
        additions=set(
            additions
        ),
        losses=set(
            losses
        ),
        first=set(
            first
        ),
        reoccupations=set(
            reoccupations
        ),
    )


# ============================================================================
# Feature extraction
# ============================================================================

def normalized_count(
    cells: Set[Cell],
    region: Set[Cell],
    denom: float,
) -> float:
    if not region:
        return 0.0

    return (
        len(
            cells
            & region
        )
        / max(
            1.0,
            denom,
        )
    )


def summarize_region(
    frames: Sequence[StepFrame],
    region: Set[Cell],
    sector_count: int,
) -> np.ndarray:
    """
    Dynamic process vector.

    Base:
        population density
        frontier density
        recent attachment fraction
        recent loss fraction
        recent first-occupation fraction
        recent reoccupation fraction
        recent gross-turnover fraction

    Then sectorized recent gross turnover and population density.
    """
    latest = frames[-1]

    region_size = max(
        1.0,
        float(
            len(region)
        ),
    )

    population_density = (
        len(
            latest.occupied
            & region
        )
        / region_size
    )

    frontier_density = (
        len(
            latest.frontier
            & region
        )
        / region_size
    )

    att = sum(
        len(
            f.additions
            & region
        )
        for f in frames
    )

    los = sum(
        len(
            f.losses
            & region
        )
        for f in frames
    )

    first = sum(
        len(
            f.first
            & region
        )
        for f in frames
    )

    reocc = sum(
        len(
            f.reoccupations
            & region
        )
        for f in frames
    )

    time_denom = (
        region_size
        * max(
            1,
            len(frames),
        )
    )

    out = [
        population_density,
        frontier_density,
        att / time_denom,
        los / time_denom,
        first / time_denom,
        reocc / time_denom,
        (att + los) / time_denom,
    ]

    # Sectorized population density.
    region_by_sector = [
        {
            c
            for c in region
            if sector_index(
                c,
                sector_count,
            ) == s
        }
        for s in range(
            sector_count
        )
    ]

    for sector_cells in (
        region_by_sector
    ):
        denom = max(
            1.0,
            float(
                len(
                    sector_cells
                )
            ),
        )

        out.append(
            len(
                latest.occupied
                & sector_cells
            )
            / denom
        )

    # Sectorized recent gross turnover.
    for sector_cells in (
        region_by_sector
    ):
        denom = (
            max(
                1.0,
                float(
                    len(
                        sector_cells
                    )
                ),
            )
            * max(
                1,
                len(
                    frames
                ),
            )
        )

        sector_turnover = sum(
            len(
                (
                    f.additions
                    | f.losses
                )
                & sector_cells
            )
            for f in frames
        )

        out.append(
            sector_turnover
            / denom
        )

    return np.asarray(
        out,
        dtype=float,
    )


def radial_bin_index(
    cell: Cell,
    max_radius: float,
    bins: int,
) -> int:
    frac = min(
        0.999999,
        euclidean_radius(
            cell
        )
        / max(
            1e-9,
            max_radius,
        ),
    )

    return min(
        bins - 1,
        int(
            frac * bins
        ),
    )


def scrambled_region_mask(
    universe: Set[Cell],
    real_region: Set[Cell],
    max_radius: float,
    bins: int,
    stream_seed: int,
    step: int,
    scale_index: int,
) -> Set[Cell]:
    """
    Observer-only geometry-matched null.

    Preserve the number of selected lattice sites in each radial bin while
    randomly reassigning angular membership within that bin.

    The null therefore preserves radial occupancy opportunity and approximate
    scale, while destroying the centered contiguous region assignment.
    """
    result: Set[Cell] = set()

    by_bin_universe: Dict[int, List[Cell]] = {
        b: []
        for b in range(
            bins
        )
    }

    by_bin_real_count: Dict[int, int] = {
        b: 0
        for b in range(
            bins
        )
    }

    for cell in universe:
        b = radial_bin_index(
            cell,
            max_radius,
            bins,
        )
        by_bin_universe[b].append(
            cell
        )

    for cell in real_region:
        b = radial_bin_index(
            cell,
            max_radius,
            bins,
        )
        by_bin_real_count[b] += 1

    for b in range(
        bins
    ):
        cells = by_bin_universe[b]
        k = min(
            by_bin_real_count[b],
            len(cells),
        )

        ranked = sorted(
            cells,
            key=lambda c: (
                null_uniform(
                    stream_seed,
                    step,
                    c,
                    scale_index
                    * 100
                    + b,
                ),
                c,
            ),
        )

        result.update(
            ranked[:k]
        )

    return result


# ============================================================================
# Dataset generation
# ============================================================================

@dataclass
class Sample:
    group: int
    checkpoint: int
    scale_index: int
    real_s: np.ndarray
    real_e: np.ndarray
    real_future: np.ndarray
    null_s: np.ndarray
    null_e: np.ndarray
    null_future: np.ndarray


def simulate_group(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
) -> List[Sample]:
    warmup = profile[
        "warmup_steps"
    ]

    horizon = profile[
        "continuation_steps"
    ]

    radius = profile[
        "radius"
    ]

    history = profile[
        "history_window"
    ]

    tau = profile[
        "prediction_horizon"
    ]

    stride = profile[
        "checkpoint_stride"
    ]

    first_cp = profile[
        "first_checkpoint_after_warmup"
    ]

    gseed = (
        seed
        + group_index * 1009
    )

    env = ch18.make_environment(
        warmup
        + horizon
        + tau
        + history
        + 8,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        no_material_params(),
    )

    ledger = OccupancyLedger(
        set(
            state.occupied
        )
    )

    frames: List[StepFrame] = []

    total_steps = (
        horizon + tau
    )

    for j in range(
        total_steps
    ):
        state, additions = (
            budgeted_growth_step(
                state,
                float(
                    env[
                        warmup + j
                    ]
                ),
                radius,
                crystal_params,
                profile[
                    "budget"
                ],
            )
        )

        first, reocc = (
            ledger.classify_additions(
                additions
            )
        )

        state, lost = (
            apply_background_loss(
                state,
                profile[
                    "loss_rate"
                ],
            )
        )

        ledger.register_losses(
            lost
        )

        if (
            ch18.capacity_fraction_occupied(
                state.occupied,
                radius,
            )
            >= profile[
                "max_capacity_fraction"
            ]
        ):
            raise RuntimeError(
                "Capacity guard triggered."
            )

        frames.append(
            make_frame(
                step=state.step,
                state=state,
                additions=additions,
                losses=lost,
                first=first,
                reoccupations=reocc,
                radius=radius,
            )
        )

        if not state.occupied:
            break

    samples: List[Sample] = []

    candidate_fracs = (
        profile[
            "candidate_radius_fractions"
        ]
    )

    for cp in range(
        first_cp,
        min(
            horizon - tau,
            len(frames) - tau,
        ),
        stride,
    ):
        if cp < history:
            continue

        present_frames = frames[
            cp - history + 1:
            cp + 1
        ]

        future_frames = frames[
            cp + tau - history + 1:
            cp + tau + 1
        ]

        latest = present_frames[
            -1
        ]

        future_latest = future_frames[
            -1
        ]

        reff = effective_radius(
            latest.occupied
        )

        future_reff = effective_radius(
            future_latest.occupied
        )

        universe = {
            (q, r)
            for q in range(
                -radius,
                radius + 1,
            )
            for r in range(
                -radius,
                radius + 1,
            )
            if (
                ch18.hex_distance(
                    (q, r)
                )
                <= radius
            )
        }

        outer_radius = min(
            float(radius),
            max(
                reff,
                future_reff,
            )
            * 1.15,
        )

        for scale_index, frac in enumerate(
            candidate_fracs
        ):
            cutoff = max(
                1.0,
                frac * reff,
            )

            future_cutoff = max(
                1.0,
                frac * future_reff,
            )

            real_region_now = (
                region_membership(
                    universe,
                    cutoff,
                )
            )

            real_region_future = (
                region_membership(
                    universe,
                    future_cutoff,
                )
            )

            real_env_now = (
                annulus_membership(
                    universe,
                    cutoff,
                    outer_radius,
                )
            )

            # For prediction target, use the future region only.
            real_s = summarize_region(
                present_frames,
                real_region_now,
                profile[
                    "sector_count"
                ],
            )

            real_e = summarize_region(
                present_frames,
                real_env_now,
                profile[
                    "sector_count"
                ],
            )

            real_future = summarize_region(
                future_frames,
                real_region_future,
                profile[
                    "sector_count"
                ],
            )

            # Observer-only radial-bin-matched null.
            null_region_now = (
                scrambled_region_mask(
                    universe=universe,
                    real_region=real_region_now,
                    max_radius=float(radius),
                    bins=profile[
                        "radial_null_bins"
                    ],
                    stream_seed=gseed + 3,
                    step=latest.step,
                    scale_index=scale_index,
                )
            )

            null_region_future = (
                scrambled_region_mask(
                    universe=universe,
                    real_region=real_region_future,
                    max_radius=float(radius),
                    bins=profile[
                        "radial_null_bins"
                    ],
                    stream_seed=gseed + 3,
                    step=future_latest.step,
                    scale_index=scale_index,
                )
            )

            null_env_now = (
                universe
                - null_region_now
            )

            null_s = summarize_region(
                present_frames,
                null_region_now,
                profile[
                    "sector_count"
                ],
            )

            null_e = summarize_region(
                present_frames,
                null_env_now,
                profile[
                    "sector_count"
                ],
            )

            null_future = summarize_region(
                future_frames,
                null_region_future,
                profile[
                    "sector_count"
                ],
            )

            samples.append(
                Sample(
                    group=group_index,
                    checkpoint=cp,
                    scale_index=scale_index,
                    real_s=real_s,
                    real_e=real_e,
                    real_future=real_future,
                    null_s=null_s,
                    null_e=null_e,
                    null_future=null_future,
                )
            )

    return samples


# ============================================================================
# Ridge regression / held-out scoring
# ============================================================================

@dataclass
class Standardizer:
    mean: np.ndarray
    scale: np.ndarray

    def transform(
        self,
        x: np.ndarray,
    ) -> np.ndarray:
        return (
            x - self.mean
        ) / self.scale


def fit_standardizer(
    x: np.ndarray,
) -> Standardizer:
    mean = np.mean(
        x,
        axis=0,
    )

    scale = np.std(
        x,
        axis=0,
        ddof=0,
    )

    scale = np.where(
        scale < 1e-12,
        1.0,
        scale,
    )

    return Standardizer(
        mean=mean,
        scale=scale,
    )


def fit_ridge(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float,
) -> Tuple[
    Standardizer,
    Standardizer,
    np.ndarray,
    np.ndarray,
]:
    xs = fit_standardizer(
        x
    )

    ys = fit_standardizer(
        y
    )

    xz = xs.transform(
        x
    )

    yz = ys.transform(
        y
    )

    # Intercept is zero after centering/standardization.
    xtx = (
        xz.T @ xz
    )

    reg = (
        alpha
        * np.eye(
            xtx.shape[0]
        )
    )

    coef = np.linalg.solve(
        xtx + reg,
        xz.T @ yz,
    )

    return (
        xs,
        ys,
        coef,
        ys.mean,
    )


def predict_ridge(
    model,
    x: np.ndarray,
) -> np.ndarray:
    xs, ys, coef, _ = model

    xz = xs.transform(
        x
    )

    yz_hat = (
        xz @ coef
    )

    return (
        yz_hat
        * ys.scale
        + ys.mean
    )


def multivariate_r2(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    resid = np.sum(
        (
            y_true
            - y_pred
        ) ** 2
    )

    baseline = np.sum(
        (
            y_true
            - np.mean(
                y_true,
                axis=0,
                keepdims=True,
            )
        ) ** 2
    )

    if baseline <= 1e-12:
        return 0.0

    return float(
        1.0
        - resid / baseline
    )


def frozen_group_split(
    groups: Sequence[int],
    seed: int,
    test_fraction: float,
) -> Tuple[
    Set[int],
    Set[int],
]:
    unique = sorted(
        set(
            groups
        )
    )

    rng = np.random.default_rng(
        seed
    )

    perm = list(
        rng.permutation(
            unique
        )
    )

    n_test = max(
        1,
        int(
            round(
                len(unique)
                * test_fraction
            )
        ),
    )

    test = set(
        int(x)
        for x in perm[:n_test]
    )

    train = set(
        int(x)
        for x in perm[n_test:]
    )

    return train, test


def evaluate_scale(
    samples: Sequence[Sample],
    scale_index: int,
    alpha: float,
    split_seed: int,
    test_fraction: float,
    null: bool,
) -> dict:
    subset = [
        s
        for s in samples
        if s.scale_index
        == scale_index
    ]

    groups = [
        s.group
        for s in subset
    ]

    train_groups, test_groups = (
        frozen_group_split(
            groups,
            split_seed,
            test_fraction,
        )
    )

    if null:
        s_mat = np.asarray([
            s.null_s
            for s in subset
        ])
        e_mat = np.asarray([
            s.null_e
            for s in subset
        ])
        y_mat = np.asarray([
            s.null_future
            for s in subset
        ])
    else:
        s_mat = np.asarray([
            s.real_s
            for s in subset
        ])
        e_mat = np.asarray([
            s.real_e
            for s in subset
        ])
        y_mat = np.asarray([
            s.real_future
            for s in subset
        ])

    train_mask = np.asarray([
        s.group
        in train_groups
        for s in subset
    ])

    test_mask = np.asarray([
        s.group
        in test_groups
        for s in subset
    ])

    x_e = e_mat
    x_se = np.concatenate(
        [
            s_mat,
            e_mat,
        ],
        axis=1,
    )

    model_e = fit_ridge(
        x_e[
            train_mask
        ],
        y_mat[
            train_mask
        ],
        alpha,
    )

    model_se = fit_ridge(
        x_se[
            train_mask
        ],
        y_mat[
            train_mask
        ],
        alpha,
    )

    pred_e = predict_ridge(
        model_e,
        x_e[
            test_mask
        ],
    )

    pred_se = predict_ridge(
        model_se,
        x_se[
            test_mask
        ],
    )

    y_test = y_mat[
        test_mask
    ]

    r2_e = multivariate_r2(
        y_test,
        pred_e,
    )

    r2_se = multivariate_r2(
        y_test,
        pred_se,
    )

    return {
        "scale_index": int(
            scale_index
        ),
        "train_groups": int(
            len(
                train_groups
            )
        ),
        "test_groups": int(
            len(
                test_groups
            )
        ),
        "train_samples": int(
            np.sum(
                train_mask
            )
        ),
        "test_samples": int(
            np.sum(
                test_mask
            )
        ),
        "r2_environment_only": (
            r2_e
        ),
        "r2_system_plus_environment": (
            r2_se
        ),
        "delta_self": (
            r2_se - r2_e
        ),
    }


# ============================================================================
# Group-permuted future null
# ============================================================================

def permuted_copy(
    samples: Sequence[Sample],
    permutation: Dict[int, int],
) -> List[Sample]:
    """
    Re-pair each current-state sample with future vectors from another group,
    matched by checkpoint and scale.

    Real and observer-null futures are both permuted.
    """
    lookup = {
        (
            s.group,
            s.checkpoint,
            s.scale_index,
        ): s
        for s in samples
    }

    out: List[Sample] = []

    for s in samples:
        target_group = (
            permutation[
                s.group
            ]
        )

        target = lookup.get(
            (
                target_group,
                s.checkpoint,
                s.scale_index,
            )
        )

        if target is None:
            continue

        out.append(
            Sample(
                group=s.group,
                checkpoint=s.checkpoint,
                scale_index=s.scale_index,
                real_s=s.real_s,
                real_e=s.real_e,
                real_future=target.real_future,
                null_s=s.null_s,
                null_e=s.null_e,
                null_future=target.null_future,
            )
        )

    return out


def derangement(
    groups: Sequence[int],
    rng: np.random.Generator,
) -> Dict[int, int]:
    groups = list(
        sorted(
            set(
                groups
            )
        )
    )

    if len(groups) < 2:
        return {
            g: g
            for g in groups
        }

    shifted = list(
        rng.permutation(
            groups
        )
    )

    # Simple repair to avoid fixed points.
    for _ in range(
        20
    ):
        fixed = [
            i
            for i, g in enumerate(
                groups
            )
            if shifted[i] == g
        ]

        if not fixed:
            break

        shifted = list(
            rng.permutation(
                groups
            )
        )

    if any(
        shifted[i] == groups[i]
        for i in range(
            len(groups)
        )
    ):
        shifted = groups[1:] + groups[:1]

    return {
        g: h
        for g, h in zip(
            groups,
            shifted,
        )
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
            self.root / filename
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
            self.root / filename
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
            / "ch22-predictive-coherence-v1-full-report.md"
        )

        parts = [
            "# Chapter 22 — When Does the Process Become One Thing? (V1)",
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
# Stage 0 — freeze protocol
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": (
            "PREDICTIVE COHERENCE SCREEN"
        ),

        "question": (
            "Does any predeclared spatial scale contain predictive information "
            "about its own future beyond the surrounding lattice and beyond "
            "a radial-geometry-matched observer null?"
        ),

        "substrate": {
            "loss_rate": (
                profile[
                    "loss_rate"
                ]
            ),
            "evaluation_budget": (
                profile[
                    "budget"
                ]
            ),
            "scheduling": (
                "neutral keyed scheduling"
            ),
        },

        "candidate_radius_fractions": (
            profile[
                "candidate_radius_fractions"
            ]
        ),

        "history_window": (
            profile[
                "history_window"
            ]
        ),

        "prediction_horizon": (
            profile[
                "prediction_horizon"
            ]
        ),

        "state_representation": (
            "process-oriented region features: population/frontier density, "
            "recent attachment/loss/first/reoccupation/turnover flows, plus "
            "six-sector population and turnover decomposition"
        ),

        "primary_statistic": (
            "max_R[(R2(S+E -> S_future)-R2(E -> S_future))_real - "
            "(R2(S+E -> S_future)-R2(E -> S_future))_null]"
        ),

        "primary_sei_excess_r2": (
            profile[
                "primary_sei_excess_r2"
            ]
        ),

        "family_null": (
            "run-group future permutation preserving candidate-scale search"
        ),

        "alpha": (
            profile[
                "alpha"
            ]
        ),

        "geometry_null": (
            "observer-only radial-bin-matched angular scrambling of region "
            "membership; null state never feeds back into dynamics"
        ),

        "new_sentence_if_successful": (
            "At one or more predeclared spatial scales, the current Digital "
            "Crystal state contains predictive information about its own "
            "future beyond that available from the surrounding lattice and "
            "beyond the frozen geometry-matched observer null."
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

        "status": "MEASURED",
    }

    reporter.json(
        "stage-00-protocol.json",
        result,
    )

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Freeze the Predictive-Coherence Question",
        result,
    )

    return result


# ============================================================================
# Stage 1 — fresh dataset
# ============================================================================

def stage_1_generate_data(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> Tuple[
    dict,
    List[Sample],
]:
    samples: List[Sample] = []

    for g in tqdm(
        range(
            profile[
                "groups"
            ]
        ),
        desc="Stage 1 fresh predictive-coherence runs",
    ):
        samples.extend(
            simulate_group(
                profile,
                crystal_params,
                seed,
                g,
            )
        )

    by_scale = {}

    for i, frac in enumerate(
        profile[
            "candidate_radius_fractions"
        ]
    ):
        subset = [
            s
            for s in samples
            if s.scale_index == i
        ]

        by_scale[
            str(frac)
        ] = {
            "samples": int(
                len(
                    subset
                )
            ),
            "groups": int(
                len(
                    set(
                        s.group
                        for s in subset
                    )
                )
            ),
            "checkpoints": int(
                len(
                    set(
                        s.checkpoint
                        for s in subset
                    )
                )
            ),
        }

    result = {
        "role": (
            "FRESH OBSERVATIONAL DATASET"
        ),

        "total_samples": int(
            len(
                samples
            )
        ),

        "by_scale": (
            by_scale
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-dataset.json",
        result,
    )

    reporter.stage(
        "stage-01-dataset.md",
        "Stage 1 — Generate the Fresh Predictive Dataset",
        result,
    )

    return result, samples


# ============================================================================
# Stage 2 — observed scale family
# ============================================================================

def stage_2_observed_family(
    reporter: Reporter,
    profile: dict,
    samples: Sequence[Sample],
    seed: int,
    image_dir: Path,
) -> dict:
    rows = []

    for i, frac in enumerate(
        profile[
            "candidate_radius_fractions"
        ]
    ):
        real = evaluate_scale(
            samples=samples,
            scale_index=i,
            alpha=profile[
                "ridge_alpha"
            ],
            split_seed=seed
            + 2_000_000,
            test_fraction=profile[
                "test_fraction"
            ],
            null=False,
        )

        null = evaluate_scale(
            samples=samples,
            scale_index=i,
            alpha=profile[
                "ridge_alpha"
            ],
            split_seed=seed
            + 2_000_000,
            test_fraction=profile[
                "test_fraction"
            ],
            null=True,
        )

        excess = (
            real[
                "delta_self"
            ]
            - null[
                "delta_self"
            ]
        )

        rows.append({
            "scale_index": i,
            "radius_fraction": frac,

            "real": real,
            "geometry_null": null,

            "excess_predictive_coherence": (
                excess
            ),
        })

    family_max = max(
        row[
            "excess_predictive_coherence"
        ]
        for row in rows
    )

    best = max(
        rows,
        key=lambda r: r[
            "excess_predictive_coherence"
        ],
    )

    result = {
        "role": (
            "OBSERVED FROZEN SCALE FAMILY"
        ),

        "by_scale": rows,

        "family_max_excess_predictive_coherence": (
            family_max
        ),

        "best_scale_radius_fraction": (
            best[
                "radius_fraction"
            ]
        ),

        "best_scale_index": (
            best[
                "scale_index"
            ]
        ),

        "primary_sei_excess_r2": (
            profile[
                "primary_sei_excess_r2"
            ]
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-02-observed-family.json",
        result,
    )

    reporter.stage(
        "stage-02-observed-family.md",
        "Stage 2 — Measure Excess Predictive Coherence",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(
            9,
            5,
        )
    )

    ax.plot(
        [
            r[
                "radius_fraction"
            ]
            for r in rows
        ],
        [
            r[
                "excess_predictive_coherence"
            ]
            for r in rows
        ],
        marker="o",
    )

    ax.axhline(
        profile[
            "primary_sei_excess_r2"
        ],
        linestyle="--",
    )

    ax.set_xlabel(
        "Candidate radius / effective radius"
    )

    ax.set_ylabel(
        "Excess held-out predictive coherence (ΔR²)"
    )

    ax.set_title(
        "Chapter 22 V1: predictive coherence across candidate scales"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch22-v1-01-predictive-coherence-by-scale.png",
        dpi=160,
    )

    plt.close(
        fig
    )

    return result


# ============================================================================
# Stage 3 — family permutation null
# ============================================================================

def stage_3_family_null(
    reporter: Reporter,
    profile: dict,
    samples: Sequence[Sample],
    observed: dict,
    seed: int,
) -> dict:
    rng = np.random.default_rng(
        seed + 3_000_000
    )

    groups = sorted(
        set(
            s.group
            for s in samples
        )
    )

    null_maxima = []

    for p in tqdm(
        range(
            profile[
                "permutations"
            ]
        ),
        desc="Stage 3 family permutation null",
    ):
        mapping = derangement(
            groups,
            rng,
        )

        perm_samples = permuted_copy(
            samples,
            mapping,
        )

        scale_excess = []

        for i, _ in enumerate(
            profile[
                "candidate_radius_fractions"
            ]
        ):
            real = evaluate_scale(
                samples=perm_samples,
                scale_index=i,
                alpha=profile[
                    "ridge_alpha"
                ],
                split_seed=seed
                + 2_000_000,
                test_fraction=profile[
                    "test_fraction"
                ],
                null=False,
            )

            null = evaluate_scale(
                samples=perm_samples,
                scale_index=i,
                alpha=profile[
                    "ridge_alpha"
                ],
                split_seed=seed
                + 2_000_000,
                test_fraction=profile[
                    "test_fraction"
                ],
                null=True,
            )

            scale_excess.append(
                real[
                    "delta_self"
                ]
                - null[
                    "delta_self"
                ]
            )

        null_maxima.append(
            max(
                scale_excess
            )
        )

    observed_max = (
        observed[
            "family_max_excess_predictive_coherence"
        ]
    )

    p_value = (
        1.0
        + sum(
            x >= observed_max
            for x in null_maxima
        )
    ) / (
        len(
            null_maxima
        )
        + 1.0
    )

    result = {
        "role": (
            "FAMILY-WISE RUN-GROUP FUTURE-PERMUTATION NULL"
        ),

        "observed_family_max": (
            observed_max
        ),

        "null_mean_family_max": float(
            np.mean(
                null_maxima
            )
        ),

        "null_q95_family_max": float(
            np.quantile(
                null_maxima,
                0.95,
            )
        ),

        "p_value": float(
            p_value
        ),

        "permutations": (
            profile[
                "permutations"
            ]
        ),

        "alternative": (
            "observed family max greater than permuted future-pairing family max"
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-03-family-null.json",
        result,
    )

    reporter.stage(
        "stage-03-family-null.md",
        "Stage 3 — Test the Frozen Scale Family Against Permuted Futures",
        result,
    )

    return result


# ============================================================================
# Stage 4 — verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    observed: dict,
    null_result: dict,
) -> dict:
    magnitude_ok = (
        observed[
            "family_max_excess_predictive_coherence"
        ]
        >= profile[
            "primary_sei_excess_r2"
        ]
    )

    permutation_ok = (
        null_result[
            "p_value"
        ]
        < profile[
            "alpha"
        ]
    )

    supported = (
        magnitude_ok
        and permutation_ok
    )

    if supported:
        status = (
            "SUPPORTED"
        )

        bounded = (
            "Under the frozen Chapter 22 V1 protocol, at least one "
            "predeclared spatial scale showed a scientifically meaningful "
            "held-out self-prediction advantage beyond the surrounding "
            "lattice and beyond the radial-geometry-matched observer null, "
            "and the family maximum exceeded the run-group future-permutation "
            "null. This supports predictive coherence at a spatial scale; it "
            "does not establish causal individuality."
        )

    else:
        status = (
            "FAILED"
        )

        bounded = (
            "Chapter 22 V1 did not establish the predeclared family-level "
            "excess predictive-coherence claim across the frozen candidate "
            "spatial scales."
        )

    result = {
        "question": (
            "Does any predeclared Digital Crystal spatial scale carry unique "
            "predictive information about its own future beyond its "
            "environment and beyond a geometry-matched observer null?"
        ),

        "best_scale_radius_fraction": (
            observed[
                "best_scale_radius_fraction"
            ]
        ),

        "family_max_excess_predictive_coherence": (
            observed[
                "family_max_excess_predictive_coherence"
            ]
        ),

        "primary_sei": (
            profile[
                "primary_sei_excess_r2"
            ]
        ),

        "magnitude_gate_passed": (
            magnitude_ok
        ),

        "family_permutation_p_value": (
            null_result[
                "p_value"
            ]
        ),

        "permutation_gate_passed": (
            permutation_ok
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
            "Does perturbing the predictively coherent candidate region have "
            "preferential causal leverage over that region's own subsequent "
            "dynamics relative to matched external and null-region "
            "interventions?"
        ),

        "next_question_if_failed": (
            "Do not tune candidate radii or decoder complexity. Close the "
            "predictive-boundary screen and test causal coherence directly "
            "only if a qualitatively new intervention design is justified."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        result,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 22 V1 Verdict",
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
        default=20260831,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch22-predictive-coherence-v1"
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
            "PREDICTIVE COHERENCE SCREEN"
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

        "candidate_scale_family_frozen": (
            profile[
                "candidate_radius_fractions"
            ]
        ),

        "canonical_attachment_probability_modified": (
            False
        ),

        "observer_null_feeds_back_into_dynamics": (
            False
        ),

        "scientific_boundary": (
            "Predictive coherence only. No individual, individuality, "
            "autonomy, causal closure, self, agency, organism, or life claim."
        ),

        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 22 V1 — PREDICTIVE COHERENCE SCREEN"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"budget={profile['budget']} "
        f"loss={profile['loss_rate']} "
        f"scales={profile['candidate_radius_fractions']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )

    s1, samples = (
        stage_1_generate_data(
            reporter,
            profile,
            crystal_params,
            args.seed,
        )
    )

    if not samples:
        raise RuntimeError(
            "No predictive samples were generated."
        )

    s2 = stage_2_observed_family(
        reporter,
        profile,
        samples,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_family_null(
        reporter,
        profile,
        samples,
        s2,
        args.seed,
    )

    s4 = stage_4_verdict(
        reporter,
        profile,
        s2,
        s3,
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

        "stage_3_status": (
            s3[
                "status"
            ]
        ),

        "final_status": (
            s4[
                "status"
            ]
        ),

        "bounded_claim": (
            s4[
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
        "CHAPTER 22 V1 COMPLETE"
    )
    print(
        f"protocol={s0['status']}"
    )
    print(
        f"dataset={s1['status']}"
    )
    print(
        f"observed_family={s2['status']}"
    )
    print(
        f"family_null={s3['status']}"
    )
    print(
        f"FINAL={s4['status']}"
    )
    print(
        f"best_scale={s4['best_scale_radius_fraction']}"
    )
    print(
        f"excess={s4['family_max_excess_predictive_coherence']:.6f}"
    )
    print(
        f"p={s4['family_permutation_p_value']:.6f}"
    )
    print(
        f"report={report_path}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
