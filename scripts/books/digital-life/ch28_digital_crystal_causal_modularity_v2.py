#!/usr/bin/env python3
"""
Digital Life — Chapter 28 V2
Does Causal Modularity Exceed a Geometry-Matched Null?
======================================================

Purpose
-------
Chapter 28 V1 showed a large raw radius-4 module score, but the raw score
increased with region radius. V2 tests whether that result exceeds what is
produced by arbitrary same-sized regions with closely matched pre-outcome
geometry in the SAME checkpoint.

Primary estimand
----------------
For each independent group:

    observed_module
        = mean module score over the V1-selected radius-4 regions

    matched_control_module
        = mean module score over geometry-matched control regions

    EXCESS_MODULE_SCORE
        = observed_module - matched_control_module

Primary status uses a frozen excess-margin SEI of +0.10.

SUPPORTED:
    CI_low > +0.10 and MDE80 <= 0.10

BOUNDED_BELOW_SEI:
    CI_high < +0.10 and MDE80 <= 0.10

UNRESOLVED:
    otherwise

INVALID:
    validity gate fails

This does not alter the V1 result. V1 remains evidence for raw spatial causal
containment asymmetry. V2 asks whether the selected regions are causally
privileged relative to matched arbitrary geometry.

Matching
--------
Observed regions use exactly the V1 outcome-blind selection rule at radius 4:
supported occupied-cell-centered hex disks ranked by:
    1. |occupancy_fraction - 0.50|
    2. center radial distance
    3. axial coordinates

Controls come from other supported radius-4 regions in the same checkpoint and
are matched without replacement using only pre-outcome geometry:

    occupancy fraction
    center radial distance
    occupied count
    internal n=1 frontier count
    external-shell n=1 frontier count
    internal probe mean boundary depth
    external probe mean boundary depth
    boundary occupied fraction

Hard pair tolerances:
    occupancy fraction diff <= 0.08
    radial distance diff <= 6
    occupied count diff <= 8
    internal frontier-count diff <= 4
    external frontier-count diff <= 4
    standardized match distance <= 4.0

Primary full profile:
    192 groups
    3 observed regions/group
    2 controls/observed
    3 internal + 3 external probes/region
    H = 8
    true unbounded evaluation
    no construction-rate calibration
    seed = 20260917

Claim boundary
--------------
Even if supported, V2 establishes only:

    privileged causal region relative to this matched spatial null

It does not establish:
    organism, self, agent, autonomy, biological individual,
    homeostasis, or life.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch24_digital_crystal_frontier_creation_causal_gain_v4 as v4
import ch27_digital_crystal_decaying_material_history_causal_response_v2 as ch27


Cell = Tuple[int, int]

EXPERIMENT_VERSION = "digital-crystal-causal-modularity-v2"
SCHEMA_VERSION = 2
CHAPTER = 28
CHAPTER_TITLE = "Does Causal Modularity Exceed a Geometry-Matched Null?"

HORIZON = 8
REGION_RADIUS = 4
EXCESS_SEI = 0.10

MIN_OCCUPIED_IN_REGION = 12
MIN_INTERNAL_FRONTIER_PROBES = 2
MIN_EXTERNAL_FRONTIER_PROBES = 2

OCCUPANCY_MIN = 0.20
OCCUPANCY_MAX = 0.80

MATCH_MAX_OCCUPANCY_DIFF = 0.08
MATCH_MAX_RADIAL_DIFF = 6
MATCH_MAX_OCCUPIED_COUNT_DIFF = 8
MATCH_MAX_INTERNAL_FRONTIER_DIFF = 4
MATCH_MAX_EXTERNAL_FRONTIER_DIFF = 4
MATCH_MAX_STANDARDIZED_DISTANCE = 4.0

MIN_GROUP_COVERAGE = 0.90
FAR_ASSERT_TOL = 1e-12

Z_95_ONE_SIDED = 1.6448536269514722
Z_80_POWER = 0.8416212335729143

PROFILES = {
    "smoke": {
        "groups": 8,
        "source_profile": "smoke",
        "observed_regions_per_group": 2,
        "controls_per_observed": 1,
        "k_internal": 2,
        "k_external": 2,
        "bootstrap_reps": 500,
        "scientific": False,
    },
    "quick": {
        "groups": 48,
        "source_profile": "quick",
        "observed_regions_per_group": 3,
        "controls_per_observed": 2,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 3000,
        "scientific": True,
    },
    "standard": {
        "groups": 96,
        "source_profile": "standard",
        "observed_regions_per_group": 3,
        "controls_per_observed": 2,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 5000,
        "scientific": True,
    },
    "full": {
        "groups": 192,
        "source_profile": "full",
        "observed_regions_per_group": 3,
        "controls_per_observed": 2,
        "k_internal": 3,
        "k_external": 3,
        "bootstrap_reps": 7000,
        "scientific": True,
    },
}


def finite_array(values: Iterable[float]) -> np.ndarray:
    return np.asarray(
        [float(v) for v in values if math.isfinite(float(v))],
        dtype=float,
    )


def bootstrap_mean_ci(values: Sequence[float], reps: int, seed: int) -> dict:
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
        boot[i] = float(np.mean(rng.choice(arr, size=len(arr), replace=True)))

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
            se * (Z_95_ONE_SIDED + Z_80_POWER)
        ),
    }


def primary_status(summary: dict, valid: bool) -> str:
    if not valid:
        return "INVALID"

    if summary["achieved_mde80_one_sided"] > EXCESS_SEI:
        return "UNRESOLVED"

    low = float(summary["ci95_low"])
    high = float(summary["ci95_high"])

    if low > EXCESS_SEI:
        return "SUPPORTED"

    if high < EXCESS_SEI:
        return "BOUNDED_BELOW_SEI"

    return "UNRESOLVED"


def directional_status(summary: dict) -> str:
    low = float(summary["ci95_low"])
    high = float(summary["ci95_high"])

    if low > 0.0:
        return "DIRECTION_POSITIVE"

    if high < 0.0:
        return "DIRECTION_NEGATIVE"

    return "DIRECTION_UNRESOLVED"


def axial_distance(a: Cell, b: Cell) -> int:
    dq = a[0] - b[0]
    dr = a[1] - b[1]
    return int(max(abs(dq), abs(dr), abs(dq + dr)))


def hex_disk(center: Cell, radius: int) -> Set[Cell]:
    cq, cr = center
    cells = set()

    for dq in range(-radius, radius + 1):
        for dr in range(-radius, radius + 1):
            cell = (cq + dq, cr + dr)
            if axial_distance(center, cell) <= radius:
                cells.add(cell)

    return cells


def hex_shell(center: Cell, radius: int) -> Set[Cell]:
    return {
        cell
        for cell in hex_disk(center, radius)
        if axial_distance(center, cell) == radius
    }


HistoryState = ch27.HistoryState


def state_from_checkpoint(checkpoint: ch18.MaterialCrystalState) -> HistoryState:
    state = ch27.from_checkpoint(checkpoint)
    state.material_strength = {}
    return state


def frontier_cells(state: HistoryState, radius: int) -> List[Cell]:
    return ch27.frontier_cells(state, radius)


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


@dataclass
class RegionCandidate:
    group: int
    center: Cell
    cells: Set[Cell]

    occupied_count: int
    occupancy_fraction: float
    boundary_occupied_fraction: float
    center_radial_distance: int

    internal_frontier_all: Tuple[Cell, ...]
    external_frontier_all: Tuple[Cell, ...]

    internal_probe_depth_mean: float
    external_probe_depth_mean: float

    match_features: Tuple[float, ...]


def supported_frontier_n1(
    state: HistoryState,
    cells: Set[Cell],
    world_radius: int,
) -> List[Cell]:
    occupied = set(state.occupied)
    frontier = set(frontier_cells(state, world_radius))

    out = []

    for cell in sorted(frontier & cells):
        n = sum(nb in occupied for nb in ch18.neighbors(cell))
        if n == 1:
            out.append(cell)

    return out


def build_region_candidate(
    group: int,
    center: Cell,
    state: HistoryState,
    world_radius: int,
) -> RegionCandidate | None:
    occupied = set(state.occupied)
    cells = hex_disk(center, REGION_RADIUS)

    occupied_count = len(occupied & cells)
    occupancy_fraction = occupied_count / max(1, len(cells))

    if occupied_count < MIN_OCCUPIED_IN_REGION:
        return None

    if not (OCCUPANCY_MIN <= occupancy_fraction <= OCCUPANCY_MAX):
        return None

    boundary = hex_shell(center, REGION_RADIUS)

    boundary_occupied_fraction = (
        len(boundary & occupied)
        / max(1, len(boundary))
    )

    internal_all = supported_frontier_n1(
        state,
        cells,
        world_radius,
    )

    external_shell = (
        hex_disk(center, REGION_RADIUS + 1)
        - cells
    )

    external_all = supported_frontier_n1(
        state,
        external_shell,
        world_radius,
    )

    if (
        len(internal_all) < MIN_INTERNAL_FRONTIER_PROBES
        or len(external_all) < MIN_EXTERNAL_FRONTIER_PROBES
    ):
        return None

    internal_depth_mean = float(
        np.mean(
            [
                REGION_RADIUS - axial_distance(center, cell)
                for cell in internal_all
            ]
        )
    )

    external_depth_mean = float(
        np.mean(
            [
                axial_distance(center, cell) - REGION_RADIUS
                for cell in external_all
            ]
        )
    )

    center_radial_distance = axial_distance((0, 0), center)

    features = (
        float(occupancy_fraction),
        float(center_radial_distance),
        float(occupied_count),
        float(len(internal_all)),
        float(len(external_all)),
        float(internal_depth_mean),
        float(external_depth_mean),
        float(boundary_occupied_fraction),
    )

    return RegionCandidate(
        group=int(group),
        center=center,
        cells=cells,
        occupied_count=int(occupied_count),
        occupancy_fraction=float(occupancy_fraction),
        boundary_occupied_fraction=float(boundary_occupied_fraction),
        center_radial_distance=int(center_radial_distance),
        internal_frontier_all=tuple(internal_all),
        external_frontier_all=tuple(external_all),
        internal_probe_depth_mean=float(internal_depth_mean),
        external_probe_depth_mean=float(external_depth_mean),
        match_features=features,
    )


def enumerate_candidates(
    group: int,
    checkpoint: ch18.MaterialCrystalState,
    world_radius: int,
) -> List[RegionCandidate]:
    state = state_from_checkpoint(checkpoint)

    candidates = []

    for center in sorted(state.occupied):
        candidate = build_region_candidate(
            group,
            center,
            state,
            world_radius,
        )

        if candidate is not None:
            candidates.append(candidate)

    return candidates


def observed_regions(
    candidates: Sequence[RegionCandidate],
    count: int,
) -> List[RegionCandidate]:
    ranked = sorted(
        candidates,
        key=lambda region: (
            abs(region.occupancy_fraction - 0.50),
            region.center_radial_distance,
            region.center,
        ),
    )

    return list(ranked[:count])


FEATURE_NAMES = [
    "occupancy_fraction",
    "center_radial_distance",
    "occupied_count",
    "internal_frontier_count",
    "external_frontier_count",
    "internal_probe_depth_mean",
    "external_probe_depth_mean",
    "boundary_occupied_fraction",
]


def robust_scales(candidates: Sequence[RegionCandidate]) -> np.ndarray:
    X = np.asarray(
        [region.match_features for region in candidates],
        dtype=float,
    )

    scales = []

    for j in range(X.shape[1]):
        col = X[:, j]
        med = float(np.median(col))
        mad = float(np.median(np.abs(col - med)))
        robust = 1.4826 * mad

        if robust > 1e-12:
            scales.append(robust)
            continue

        sd = float(np.std(col, ddof=1)) if len(col) > 1 else 0.0
        scales.append(sd if sd > 1e-12 else 1.0)

    return np.asarray(scales, dtype=float)


def hard_match_gate(
    observed: RegionCandidate,
    control: RegionCandidate,
) -> bool:
    if abs(
        observed.occupancy_fraction - control.occupancy_fraction
    ) > MATCH_MAX_OCCUPANCY_DIFF:
        return False

    if abs(
        observed.center_radial_distance - control.center_radial_distance
    ) > MATCH_MAX_RADIAL_DIFF:
        return False

    if abs(
        observed.occupied_count - control.occupied_count
    ) > MATCH_MAX_OCCUPIED_COUNT_DIFF:
        return False

    if abs(
        len(observed.internal_frontier_all)
        - len(control.internal_frontier_all)
    ) > MATCH_MAX_INTERNAL_FRONTIER_DIFF:
        return False

    if abs(
        len(observed.external_frontier_all)
        - len(control.external_frontier_all)
    ) > MATCH_MAX_EXTERNAL_FRONTIER_DIFF:
        return False

    return True


def standardized_match_distance(
    observed: RegionCandidate,
    control: RegionCandidate,
    scales: np.ndarray,
) -> float:
    a = np.asarray(observed.match_features, dtype=float)
    b = np.asarray(control.match_features, dtype=float)
    z = (a - b) / scales
    return float(np.sqrt(np.sum(z * z)))


@dataclass
class MatchedPair:
    group: int
    observed_index: int
    control_index: int

    observed_center: Cell
    control_center: Cell
    distance: float

    occupancy_diff: float
    radial_diff: int
    occupied_count_diff: int
    internal_frontier_diff: int
    external_frontier_diff: int

    observed: RegionCandidate
    control: RegionCandidate


def match_controls(
    candidates: Sequence[RegionCandidate],
    observed: Sequence[RegionCandidate],
    controls_per_observed: int,
) -> List[MatchedPair]:
    if not candidates:
        return []

    scales = robust_scales(candidates)

    observed_centers = {
        region.center
        for region in observed
    }

    eligible = [
        region
        for region in candidates
        if region.center not in observed_centers
    ]

    used_control_centers = set()
    pairs = []

    for obs_idx, obs in enumerate(observed):
        scored = []

        for control in eligible:
            if control.center in used_control_centers:
                continue

            if not hard_match_gate(obs, control):
                continue

            distance = standardized_match_distance(
                obs,
                control,
                scales,
            )

            if distance > MATCH_MAX_STANDARDIZED_DISTANCE:
                continue

            scored.append(
                (
                    distance,
                    control.center_radial_distance,
                    control.center,
                    control,
                )
            )

        scored.sort(
            key=lambda item: (
                item[0],
                item[1],
                item[2],
            )
        )

        for control_idx, (
            distance,
            _radial,
            _center,
            control,
        ) in enumerate(scored[:controls_per_observed]):
            used_control_centers.add(control.center)

            pairs.append(
                MatchedPair(
                    group=int(obs.group),
                    observed_index=int(obs_idx),
                    control_index=int(control_idx),
                    observed_center=obs.center,
                    control_center=control.center,
                    distance=float(distance),
                    occupancy_diff=float(
                        abs(
                            obs.occupancy_fraction
                            - control.occupancy_fraction
                        )
                    ),
                    radial_diff=int(
                        abs(
                            obs.center_radial_distance
                            - control.center_radial_distance
                        )
                    ),
                    occupied_count_diff=int(
                        abs(
                            obs.occupied_count
                            - control.occupied_count
                        )
                    ),
                    internal_frontier_diff=int(
                        abs(
                            len(obs.internal_frontier_all)
                            - len(control.internal_frontier_all)
                        )
                    ),
                    external_frontier_diff=int(
                        abs(
                            len(obs.external_frontier_all)
                            - len(control.external_frontier_all)
                        )
                    ),
                    observed=obs,
                    control=control,
                )
            )

    return pairs


@dataclass
class Branches:
    force: HistoryState
    prevent: HistoryState


def make_branches(
    checkpoint: ch18.MaterialCrystalState,
    x: Cell,
) -> Branches:
    base = state_from_checkpoint(checkpoint)

    prevent = ch27.clone_state(base)

    if x in prevent.occupied:
        raise RuntimeError("Probe x must be empty.")

    force = ch27.clone_state(base)
    force.occupied.add(x)
    force.birth_time[x] = int(force.step)

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
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier = frontier_cells(
        state,
        world_radius,
    )

    if blocked_cell is not None:
        frontier = [
            cell
            for cell in frontier
            if cell != blocked_cell
        ]

    next_step = int(state.step + 1)
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
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    out = HistoryState(
        occupied=occupied,
        birth_time=birth_time,
        material_strength={},
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
            + [0.0]
        ),
    )

    return out, additions


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

    after_loss, lost = ch27.v1.apply_background_loss(
        grown,
        loss_rate,
    )

    return after_loss, additions, lost


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
    ff = set(frontier_cells(force, world_radius))
    pf = set(frontier_cells(prevent, world_radius))

    if blocked_prevent_x:
        pf.discard(x)

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
            if cell in ff
            else 0.0
        )

        p_prevent = (
            attachment_probability(
                cell,
                prevent,
                input_value,
                crystal_params,
            )
            if cell in pf
            else 0.0
        )

        delta = p_force - p_prevent
        d_probe = axial_distance(cell, x)

        if cell in region_cells:
            signed_inside += delta
            abs_inside += abs(delta)

        elif d_probe <= HORIZON:
            signed_outside_local += delta
            abs_outside_local += abs(delta)

        else:
            signed_far += delta
            abs_far += abs(delta)

    return ExpectedMass(
        signed_inside=float(signed_inside),
        signed_outside_local=float(signed_outside_local),
        signed_far=float(signed_far),
        absolute_inside=float(abs_inside),
        absolute_outside_local=float(abs_outside_local),
        absolute_far=float(abs_far),
    )


@dataclass
class ProbeResult:
    group: int
    role: str
    region_id: str
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
    role: str
    region_id: str
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


@dataclass
class RegionResult:
    group: int
    role: str
    region_id: str

    center_q: int
    center_r: int

    occupied_count: int
    occupancy_fraction: float
    boundary_occupied_fraction: float
    center_radial_distance: int

    internal_probe_count: int
    external_probe_count: int

    internal_retention: float
    external_penetration: float
    module_score: float

    mean_internal_absolute_mass: float
    mean_external_absolute_mass: float

    max_far_assertion: float


def run_probe(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    region: RegionCandidate,
    role: str,
    region_id: str,
    x: Cell,
    probe_class: str,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[ProbeResult, List[PerLagRow]]:
    branches = make_branches(
        checkpoint,
        x,
    )

    force = branches.force
    prevent = branches.prevent

    world_radius = int(source_profile["radius"])
    loss_rate = float(source_profile["loss_rate"])

    total_signed_inside = 0.0
    total_signed_outside = 0.0
    total_signed_far = 0.0

    total_abs_inside = 0.0
    total_abs_outside = 0.0
    total_abs_far = 0.0

    far_max = 0.0
    lag_rows = []

    for lag in range(1, HORIZON + 1):
        input_value = float(future_env[lag])

        mass = expected_mass(
            force,
            prevent,
            x,
            region.cells,
            input_value,
            world_radius,
            crystal_params,
            blocked_prevent_x=(lag == 1),
        )

        total_signed_inside += mass.signed_inside
        total_signed_outside += mass.signed_outside_local
        total_signed_far += mass.signed_far

        total_abs_inside += mass.absolute_inside
        total_abs_outside += mass.absolute_outside_local
        total_abs_far += mass.absolute_far

        far_max = max(
            far_max,
            abs(mass.signed_far),
            mass.absolute_far,
        )

        lag_rows.append(
            PerLagRow(
                group=int(region.group),
                role=role,
                region_id=region_id,
                probe_class=probe_class,
                probe_q=int(x[0]),
                probe_r=int(x[1]),
                lag=int(lag),
                signed_inside=mass.signed_inside,
                signed_outside_local=mass.signed_outside_local,
                signed_far=mass.signed_far,
                absolute_inside=mass.absolute_inside,
                absolute_outside_local=mass.absolute_outside_local,
                absolute_far=mass.absolute_far,
            )
        )

        force, _force_add, _force_lost = canonical_step(
            force,
            input_value,
            world_radius,
            crystal_params,
            loss_rate,
            blocked_cell=None,
        )

        prevent, prevent_add, _prevent_lost = canonical_step(
            prevent,
            input_value,
            world_radius,
            crystal_params,
            loss_rate,
            blocked_cell=(x if lag == 1 else None),
        )

        if lag == 1 and x in prevent_add:
            raise RuntimeError("PREVENT intervention failed.")

        if lag == 1:
            force.occupied.discard(x)
            force.birth_time.pop(x, None)

            prevent.occupied.discard(x)
            prevent.birth_time.pop(x, None)

            if x in force.occupied or x in prevent.occupied:
                raise RuntimeError("Intervention cleanup failed.")

    denom = total_abs_inside + total_abs_outside

    inside_fraction = (
        total_abs_inside / denom
        if denom > 0.0
        else float("nan")
    )

    return (
        ProbeResult(
            group=int(region.group),
            role=role,
            region_id=region_id,
            probe_class=probe_class,
            probe_q=int(x[0]),
            probe_r=int(x[1]),
            signed_inside=float(total_signed_inside),
            signed_outside_local=float(total_signed_outside),
            signed_far=float(total_signed_far),
            absolute_inside=float(total_abs_inside),
            absolute_outside_local=float(total_abs_outside),
            absolute_far=float(total_abs_far),
            inside_fraction=float(inside_fraction),
            total_local_absolute=float(denom),
            far_assertion_max=float(far_max),
        ),
        lag_rows,
    )


def evaluate_region(
    checkpoint: ch18.MaterialCrystalState,
    future_env: np.ndarray,
    region: RegionCandidate,
    role: str,
    region_id: str,
    k_internal: int,
    k_external: int,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> Tuple[RegionResult, List[ProbeResult], List[PerLagRow]]:
    internal_probes = list(
        region.internal_frontier_all[:k_internal]
    )

    external_probes = list(
        region.external_frontier_all[:k_external]
    )

    if (
        len(internal_probes) < MIN_INTERNAL_FRONTIER_PROBES
        or len(external_probes) < MIN_EXTERNAL_FRONTIER_PROBES
    ):
        raise RuntimeError("Region lost required probe support.")

    probes = []
    lag_rows = []

    for x in internal_probes:
        result, rows = run_probe(
            checkpoint,
            future_env,
            region,
            role,
            region_id,
            x,
            "internal",
            source_profile,
            crystal_params,
        )
        probes.append(result)
        lag_rows.extend(rows)

    for x in external_probes:
        result, rows = run_probe(
            checkpoint,
            future_env,
            region,
            role,
            region_id,
            x,
            "external",
            source_profile,
            crystal_params,
        )
        probes.append(result)
        lag_rows.extend(rows)

    internal = [
        p for p in probes
        if p.probe_class == "internal"
    ]

    external = [
        p for p in probes
        if p.probe_class == "external"
    ]

    internal_retention = float(
        np.mean(
            [p.inside_fraction for p in internal]
        )
    )

    external_penetration = float(
        np.mean(
            [p.inside_fraction for p in external]
        )
    )

    result = RegionResult(
        group=int(region.group),
        role=role,
        region_id=region_id,
        center_q=int(region.center[0]),
        center_r=int(region.center[1]),
        occupied_count=int(region.occupied_count),
        occupancy_fraction=float(region.occupancy_fraction),
        boundary_occupied_fraction=float(
            region.boundary_occupied_fraction
        ),
        center_radial_distance=int(
            region.center_radial_distance
        ),
        internal_probe_count=int(len(internal)),
        external_probe_count=int(len(external)),
        internal_retention=float(internal_retention),
        external_penetration=float(external_penetration),
        module_score=float(
            internal_retention - external_penetration
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
                p.far_assertion_max
                for p in probes
            )
        ),
    )

    return result, probes, lag_rows


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
) -> List[GroupCheckpoint]:
    groups = []

    for group in tqdm(
        range(int(profile["groups"])),
        desc="Chapter 28 V2 checkpoints",
    ):
        checkpoint, future_env, _max_capacity = v4.build_checkpoint(
            source_profile,
            crystal_params,
            seed,
            group,
        )

        groups.append(
            GroupCheckpoint(
                group=int(group),
                checkpoint=checkpoint,
                future_env=future_env,
            )
        )

    return groups


@dataclass
class MatchResult:
    group: int
    observed_index: int
    control_index: int

    observed_region_id: str
    control_region_id: str

    observed_center_q: int
    observed_center_r: int
    control_center_q: int
    control_center_r: int

    match_distance: float

    occupancy_diff: float
    radial_diff: int
    occupied_count_diff: int
    internal_frontier_diff: int
    external_frontier_diff: int

    observed_module_score: float
    control_module_score: float
    excess_module_score: float

    observed_internal_retention: float
    control_internal_retention: float
    excess_internal_retention: float

    observed_external_penetration: float
    control_external_penetration: float
    excess_external_penetration: float


def group_match_metrics(
    matches: Sequence[MatchResult],
) -> Dict[int, dict]:
    buckets = defaultdict(list)

    for match in matches:
        buckets[match.group].append(match)

    out = {}

    for group, rows in buckets.items():
        out[int(group)] = {
            "excess_module_score": float(
                np.mean(
                    [
                        row.excess_module_score
                        for row in rows
                    ]
                )
            ),
            "observed_module_score": float(
                np.mean(
                    [
                        row.observed_module_score
                        for row in rows
                    ]
                )
            ),
            "control_module_score": float(
                np.mean(
                    [
                        row.control_module_score
                        for row in rows
                    ]
                )
            ),
            "excess_internal_retention": float(
                np.mean(
                    [
                        row.excess_internal_retention
                        for row in rows
                    ]
                )
            ),
            "excess_external_penetration": float(
                np.mean(
                    [
                        row.excess_external_penetration
                        for row in rows
                    ]
                )
            ),
            "match_count": int(len(rows)),
            "unique_observed_count": int(
                len(
                    {
                        row.observed_index
                        for row in rows
                    }
                )
            ),
        }

    return out


def write_rows(
    jsonl_path: Path,
    csv_path: Path,
    rows,
) -> None:
    rows = list(rows)

    with jsonl_path.open(
        "w",
        encoding="utf-8",
    ) as f:
        for row in rows:
            f.write(
                json.dumps(asdict(row))
                + "\n"
            )

    if not rows:
        return

    fields = list(
        asdict(rows[0]).keys()
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
            writer.writerow(asdict(row))


class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.sections = []

    def save_json(self, filename: str, payload):
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

    def stage(self, filename: str, title: str, payload):
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
            (title, body)
        )

    def full_report(self, metadata) -> Path:
        path = (
            self.root
            / "ch28-causal-modularity-v2-full-report.md"
        )

        parts = [
            "# Chapter 28 — Geometry-Matched Causal Modularity Null (V2)",
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
            "\n".join(parts),
            encoding="utf-8",
        )

        return path


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="full",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=20260917,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch28-causal-modularity-v2"
        ),
    )

    args = parser.parse_args()

    profile = dict(
        PROFILES[args.profile]
    )

    source_profile = dict(
        v4.PROFILES[
            profile["source_profile"]
        ]
    )

    source_profile["groups"] = int(
        profile["groups"]
    )

    source_profile["horizon"] = HORIZON

    crystal_params = ch18.CrystalParams()
    reporter = Reporter(args.report_dir)

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
                20260915,
                20260916,
            }
        ),
        "horizon": HORIZON,
        "region_radius": REGION_RADIUS,
        "excess_SEI": EXCESS_SEI,
        "allocation_policy": "true_unbounded",
        "started_at_unix": time.time(),
    }

    protocol = {
        "status": (
            "FROZEN"
            if profile["scientific"]
            else "ENGINEERING_SMOKE_ONLY"
        ),
        "primary_question": (
            "Do V1-selected radius-4 regions exceed geometry-matched "
            "same-checkpoint controls in causal modularity?"
        ),
        "primary_estimand": (
            "mean_group(observed_module_score - matched_control_module_score)"
        ),
        "excess_SEI": EXCESS_SEI,
        "region_radius": REGION_RADIUS,
        "horizon": HORIZON,
        "matching": {
            "same_checkpoint": True,
            "outcome_blind": True,
            "controls_per_observed": int(
                profile["controls_per_observed"]
            ),
            "features": FEATURE_NAMES,
            "max_occupancy_diff": MATCH_MAX_OCCUPANCY_DIFF,
            "max_radial_diff": MATCH_MAX_RADIAL_DIFF,
            "max_occupied_count_diff": MATCH_MAX_OCCUPIED_COUNT_DIFF,
            "max_internal_frontier_diff": MATCH_MAX_INTERNAL_FRONTIER_DIFF,
            "max_external_frontier_diff": MATCH_MAX_EXTERNAL_FRONTIER_DIFF,
            "max_standardized_distance": MATCH_MAX_STANDARDIZED_DISTANCE,
        },
        "stop_rule": (
            "No metric/radius/matching rescue. Increase groups only if "
            "UNRESOLVED solely because MDE exceeds 0.10."
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 28 V2 Protocol",
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

    all_region_results = []
    all_probe_results = []
    all_lag_rows = []
    all_matches = []

    support_rows = []
    match_quality_rows = []
    covered_groups = []

    for group_record in tqdm(
        groups,
        desc="Chapter 28 V2 groups",
    ):
        candidates = enumerate_candidates(
            group_record.group,
            group_record.checkpoint,
            int(source_profile["radius"]),
        )

        observed = observed_regions(
            candidates,
            int(
                profile[
                    "observed_regions_per_group"
                ]
            ),
        )

        pairs = match_controls(
            candidates,
            observed,
            int(
                profile[
                    "controls_per_observed"
                ]
            ),
        )

        pair_count_by_observed = defaultdict(int)

        for pair in pairs:
            pair_count_by_observed[
                pair.observed_index
            ] += 1

        matched_observed_indices = sorted(
            [
                idx
                for idx, count
                in pair_count_by_observed.items()
                if count >= 1
            ]
        )

        group_supported = (
            len(matched_observed_indices)
            >= 2
        )

        support_rows.append(
            {
                "group": int(
                    group_record.group
                ),
                "candidate_count": int(
                    len(candidates)
                ),
                "observed_count": int(
                    len(observed)
                ),
                "matched_pair_count": int(
                    len(pairs)
                ),
                "matched_observed_count": int(
                    len(
                        matched_observed_indices
                    )
                ),
                "supported": bool(
                    group_supported
                ),
            }
        )

        if not group_supported:
            continue

        covered_groups.append(
            group_record.group
        )

        region_eval_cache = {}

        def eval_cached(
            region: RegionCandidate,
            role: str,
            region_id: str,
        ) -> RegionResult:
            key = (
                role,
                region.center,
            )

            if key in region_eval_cache:
                return region_eval_cache[key]

            result, probes, lag_rows = evaluate_region(
                group_record.checkpoint,
                group_record.future_env,
                region,
                role,
                region_id,
                int(profile["k_internal"]),
                int(profile["k_external"]),
                source_profile,
                crystal_params,
            )

            region_eval_cache[key] = result

            all_region_results.append(result)
            all_probe_results.extend(probes)
            all_lag_rows.extend(lag_rows)

            return result

        for pair in pairs:
            if (
                pair.observed_index
                not in matched_observed_indices
            ):
                continue

            obs_id = (
                f"g{pair.group}:obs{pair.observed_index}"
            )

            ctrl_id = (
                f"g{pair.group}:obs{pair.observed_index}:"
                f"ctrl{pair.control_index}"
            )

            obs_result = eval_cached(
                pair.observed,
                "observed",
                obs_id,
            )

            ctrl_result = eval_cached(
                pair.control,
                "control",
                ctrl_id,
            )

            match_result = MatchResult(
                group=int(pair.group),
                observed_index=int(
                    pair.observed_index
                ),
                control_index=int(
                    pair.control_index
                ),
                observed_region_id=obs_id,
                control_region_id=ctrl_id,
                observed_center_q=int(
                    pair.observed_center[0]
                ),
                observed_center_r=int(
                    pair.observed_center[1]
                ),
                control_center_q=int(
                    pair.control_center[0]
                ),
                control_center_r=int(
                    pair.control_center[1]
                ),
                match_distance=float(
                    pair.distance
                ),
                occupancy_diff=float(
                    pair.occupancy_diff
                ),
                radial_diff=int(
                    pair.radial_diff
                ),
                occupied_count_diff=int(
                    pair.occupied_count_diff
                ),
                internal_frontier_diff=int(
                    pair.internal_frontier_diff
                ),
                external_frontier_diff=int(
                    pair.external_frontier_diff
                ),
                observed_module_score=float(
                    obs_result.module_score
                ),
                control_module_score=float(
                    ctrl_result.module_score
                ),
                excess_module_score=float(
                    obs_result.module_score
                    - ctrl_result.module_score
                ),
                observed_internal_retention=float(
                    obs_result.internal_retention
                ),
                control_internal_retention=float(
                    ctrl_result.internal_retention
                ),
                excess_internal_retention=float(
                    obs_result.internal_retention
                    - ctrl_result.internal_retention
                ),
                observed_external_penetration=float(
                    obs_result.external_penetration
                ),
                control_external_penetration=float(
                    ctrl_result.external_penetration
                ),
                excess_external_penetration=float(
                    obs_result.external_penetration
                    - ctrl_result.external_penetration
                ),
            )

            all_matches.append(match_result)

            match_quality_rows.append(
                {
                    "group": int(pair.group),
                    "observed_index": int(
                        pair.observed_index
                    ),
                    "control_index": int(
                        pair.control_index
                    ),
                    "distance": float(
                        pair.distance
                    ),
                    "occupancy_diff": float(
                        pair.occupancy_diff
                    ),
                    "radial_diff": int(
                        pair.radial_diff
                    ),
                    "occupied_count_diff": int(
                        pair.occupied_count_diff
                    ),
                    "internal_frontier_diff": int(
                        pair.internal_frontier_diff
                    ),
                    "external_frontier_diff": int(
                        pair.external_frontier_diff
                    ),
                }
            )

    write_rows(
        reporter.root
        / "raw-v2-region-results.jsonl",
        reporter.root
        / "raw-v2-region-results.csv",
        all_region_results,
    )

    write_rows(
        reporter.root
        / "raw-v2-match-results.jsonl",
        reporter.root
        / "raw-v2-match-results.csv",
        all_matches,
    )

    write_rows(
        reporter.root
        / "raw-v2-probe-results.jsonl",
        reporter.root
        / "raw-v2-probe-results.csv",
        all_probe_results,
    )

    write_rows(
        reporter.root
        / "raw-v2-per-lag.jsonl",
        reporter.root
        / "raw-v2-per-lag.csv",
        all_lag_rows,
    )

    total_requested_groups = int(
        profile["groups"]
    )

    coverage = (
        len(set(covered_groups))
        / max(1, total_requested_groups)
    )

    matched_obs_counts = [
        row["matched_observed_count"]
        for row in support_rows
        if row["supported"]
    ]

    by_group_obs = defaultdict(int)

    for match in all_matches:
        by_group_obs[
            (
                match.group,
                match.observed_index,
            )
        ] += 1

    controls_per_obs_values = list(
        by_group_obs.values()
    )

    support = {
        "requested_groups": total_requested_groups,
        "covered_groups": int(
            len(set(covered_groups))
        ),
        "coverage_fraction": float(
            coverage
        ),
        "median_matched_observed_regions_per_covered_group": (
            float(
                statistics.median(
                    matched_obs_counts
                )
            )
            if matched_obs_counts
            else 0.0
        ),
        "median_controls_per_matched_observed": (
            float(
                statistics.median(
                    controls_per_obs_values
                )
            )
            if controls_per_obs_values
            else 0.0
        ),
        "total_matches": int(
            len(all_matches)
        ),
        "support_rows": support_rows,
    }

    reporter.stage(
        "stage-01-support.md",
        "Stage 1 — Same-Checkpoint Match Support",
        support,
    )

    reporter.save_json(
        "stage-01-support.json",
        support,
    )

    if match_quality_rows:
        distances = [
            row["distance"]
            for row in match_quality_rows
        ]

        occupancy_diffs = [
            row["occupancy_diff"]
            for row in match_quality_rows
        ]

        radial_diffs = [
            row["radial_diff"]
            for row in match_quality_rows
        ]

        occupied_count_diffs = [
            row["occupied_count_diff"]
            for row in match_quality_rows
        ]

        internal_diffs = [
            row["internal_frontier_diff"]
            for row in match_quality_rows
        ]

        external_diffs = [
            row["external_frontier_diff"]
            for row in match_quality_rows
        ]

        match_quality = {
            "n_matches": int(
                len(match_quality_rows)
            ),
            "distance": {
                "mean": float(
                    np.mean(distances)
                ),
                "median": float(
                    np.median(distances)
                ),
                "max": float(
                    max(distances)
                ),
            },
            "occupancy_diff": {
                "mean": float(
                    np.mean(
                        occupancy_diffs
                    )
                ),
                "max": float(
                    max(occupancy_diffs)
                ),
            },
            "radial_diff": {
                "mean": float(
                    np.mean(radial_diffs)
                ),
                "max": int(
                    max(radial_diffs)
                ),
            },
            "occupied_count_diff": {
                "mean": float(
                    np.mean(
                        occupied_count_diffs
                    )
                ),
                "max": int(
                    max(
                        occupied_count_diffs
                    )
                ),
            },
            "internal_frontier_diff": {
                "mean": float(
                    np.mean(internal_diffs)
                ),
                "max": int(
                    max(internal_diffs)
                ),
            },
            "external_frontier_diff": {
                "mean": float(
                    np.mean(external_diffs)
                ),
                "max": int(
                    max(external_diffs)
                ),
            },
        }

    else:
        match_quality = {
            "n_matches": 0
        }

    reporter.stage(
        "stage-02-match-quality.md",
        "Stage 2 — Geometry Match Quality",
        match_quality,
    )

    reporter.save_json(
        "stage-02-match-quality.json",
        match_quality,
    )

    far_max = (
        max(
            [
                region.max_far_assertion
                for region in all_region_results
            ]
        )
        if all_region_results
        else float("inf")
    )

    median_matched_obs = support[
        "median_matched_observed_regions_per_covered_group"
    ]

    median_controls = support[
        "median_controls_per_matched_observed"
    ]

    validity = {
        "group_coverage_fraction": float(
            coverage
        ),
        "required_group_coverage": MIN_GROUP_COVERAGE,
        "median_matched_observed_regions_per_covered_group": (
            median_matched_obs
        ),
        "required_median_matched_observed_regions_per_group": 2.0,
        "median_controls_per_matched_observed": (
            median_controls
        ),
        "required_median_controls_per_observed": 1.0,
        "far_expected_effect_max_abs": float(
            far_max
        ),
        "far_assertion_tolerance": FAR_ASSERT_TOL,
        "far_zero_assertion_pass": bool(
            far_max <= FAR_ASSERT_TOL
        ),
        "matching_outcome_blind": True,
        "same_checkpoint_matching": True,
        "control_reuse_within_group": False,
    }

    validity["scientific_valid"] = bool(
        coverage >= MIN_GROUP_COVERAGE
        and median_matched_obs >= 2.0
        and median_controls >= 1.0
        and far_max <= FAR_ASSERT_TOL
    )

    validity["status"] = (
        "PASS"
        if validity["scientific_valid"]
        else "FAIL"
    )

    reporter.stage(
        "stage-03-validity.md",
        "Stage 3 — Construct Validity",
        validity,
    )

    reporter.save_json(
        "stage-03-validity.json",
        validity,
    )

    group_metrics = group_match_metrics(
        all_matches
    )

    primary_values = [
        payload["excess_module_score"]
        for _, payload in sorted(
            group_metrics.items()
        )
    ]

    primary_summary = bootstrap_mean_ci(
        primary_values,
        int(profile["bootstrap_reps"]),
        args.seed + 5000,
    )

    if not profile["scientific"]:
        p_status = "ENGINEERING_SMOKE_ONLY"
    else:
        p_status = primary_status(
            primary_summary,
            validity["scientific_valid"],
        )

    direction = directional_status(
        primary_summary
    )

    observed_summary = bootstrap_mean_ci(
        [
            payload["observed_module_score"]
            for _, payload in sorted(
                group_metrics.items()
            )
        ],
        int(profile["bootstrap_reps"]),
        args.seed + 5001,
    )

    control_summary = bootstrap_mean_ci(
        [
            payload["control_module_score"]
            for _, payload in sorted(
                group_metrics.items()
            )
        ],
        int(profile["bootstrap_reps"]),
        args.seed + 5002,
    )

    primary = {
        "estimand": (
            "observed module score - matched-control module score"
        ),
        "EXCESS_SEI": EXCESS_SEI,
        "result": primary_summary,
        "status": p_status,
        "directional_substatus": direction,
        "observed_module_score": observed_summary,
        "matched_control_module_score": control_summary,
    }

    reporter.stage(
        "stage-04-primary.md",
        "Stage 4 — Excess Causal Modularity Above Geometry Null",
        primary,
    )

    reporter.save_json(
        "stage-04-primary.json",
        primary,
    )

    excess_internal = bootstrap_mean_ci(
        [
            payload["excess_internal_retention"]
            for _, payload in sorted(
                group_metrics.items()
            )
        ],
        int(profile["bootstrap_reps"]),
        args.seed + 6000,
    )

    excess_external = bootstrap_mean_ci(
        [
            payload["excess_external_penetration"]
            for _, payload in sorted(
                group_metrics.items()
            )
        ],
        int(profile["bootstrap_reps"]),
        args.seed + 6001,
    )

    decomposition = {
        "excess_internal_retention": (
            excess_internal
        ),
        "excess_external_penetration": (
            excess_external
        ),
        "identity": (
            "excess_module = excess_internal_retention "
            "- excess_external_penetration"
        ),
        "interpretation": {
            "positive_excess_internal_retention": (
                "observed regions retain more internally generated causal mass"
            ),
            "negative_excess_external_penetration": (
                "observed regions admit less externally generated causal mass"
            ),
        },
    }

    reporter.stage(
        "stage-05-decomposition.md",
        "Stage 5 — Excess-Modularity Decomposition",
        decomposition,
    )

    reporter.save_json(
        "stage-05-decomposition.json",
        decomposition,
    )

    if not profile["scientific"]:
        overall = "ENGINEERING_SMOKE_ONLY"
        bounded = "Engineering smoke profile only."

    elif not validity["scientific_valid"]:
        overall = "INVALID"
        bounded = (
            "Same-checkpoint geometry matching or causal-cone validity failed."
        )

    elif p_status == "SUPPORTED":
        overall = "EXCESS_CAUSAL_MODULARITY_SUPPORTED"
        bounded = (
            "At frozen radius 4, V1-selected regions exceeded same-checkpoint "
            "geometry-matched controls by more than the predeclared +0.10 "
            "module-score margin."
        )

    elif p_status == "BOUNDED_BELOW_SEI":
        overall = "EXCESS_CAUSAL_MODULARITY_BOUNDED_BELOW_SEI"
        bounded = (
            "At frozen radius 4, any excess causal modularity of V1-selected "
            "regions over same-checkpoint geometry-matched controls was bounded "
            "below the predeclared +0.10 meaningful margin."
        )

    else:
        overall = "EXCESS_CAUSAL_MODULARITY_UNRESOLVED"
        bounded = (
            "The geometry-matched experiment did not resolve whether V1-selected "
            "regions exceed the +0.10 excess-modularity margin."
        )

    verdict = {
        "validity": validity,
        "primary_status": p_status,
        "directional_substatus": direction,
        "overall_status": overall,
        "bounded_claim": bounded,
        "V1_status_preserved": (
            "RAW_CAUSAL_MODULARITY_SUPPORTED"
        ),
        "claim_boundary": {
            "supported_if_positive": (
                "privileged causal region relative to this matched spatial null"
            ),
            "not_established": [
                "organism",
                "self",
                "agent",
                "autonomy",
                "biological individual",
                "homeostasis",
                "life",
            ],
        },
        "stop_rule": (
            "No metric/radius/matching rescue. Increase independent groups "
            "only if unresolved solely because MDE exceeds 0.10."
        ),
    }

    reporter.stage(
        "stage-06-verdict.md",
        "Stage 6 — Chapter 28 V2 Verdict",
        verdict,
    )

    reporter.save_json(
        "stage-06-verdict.json",
        verdict,
    )

    metadata["finished_at_unix"] = time.time()
    metadata["final_status"] = overall

    reporter.save_json(
        "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()
    print("=" * 78)
    print(f"FINAL STATUS: {overall}")
    print(bounded)
    print(f"Report: {report}")
    print("=" * 78)


if __name__ == "__main__":
    main()
