#!/usr/bin/env python3
"""
Chapter 21 — What Does It Cost to Stay? (V2)

Bounded dynamic persistence under computational scarcity
=======================================================

Chapter 21 V1 established three strong descriptive results:

1. Finite frontier-evaluation budget strongly constrains crystal scale.
2. At fixed budget, local scheduling strongly changes reoccupation/persistence.
3. Under neutral scheduling, severe scarcity produced very small late net growth.

But V1's primary two-arm allocation tradeoff FAILED because the low-support
first-occupation advantage did not clear its predeclared SEI.

V2 does NOT retry the scheduling-policy hypothesis.

Instead it tests one qualitatively new sentence:

    Under ongoing material loss, there exists a finite evaluation budget
    at which population is approximately stationary while gross turnover
    continues.

Only NEUTRAL scheduling is used.

No new biological mechanism is introduced.

There is still no:
    maintenance controller
    target size
    homeostasis variable
    energy
    metabolism
    repair instruction
    adaptation
    agency

New scientific object
---------------------

A bounded dynamic regime requires ALL of:

    population remains substantially nonzero
    late normalized population slope is near zero
    gross material loss continues
    reoccupation continues
    first occupation continues
    simulation capacity is not binding

Therefore:

    static freeze != success
    extinction != success
    world saturation != success

Fresh frozen candidate budgets
------------------------------

Based on V1's exploratory neutral sweep, V2 predeclares a narrow independent
candidate set around the apparent near-zero-net region:

    B = 48, 64, 80, 96, 128

No candidate may be added after seeing V2 results.

Primary decision rule
---------------------

At least one candidate B must satisfy every bounded-dynamic criterion on the
fresh V2 sample.

This is an existence test across a frozen candidate family.  To avoid
post-hoc cherry-picking, the candidate set and all thresholds are frozen in
this script before execution.

Scientific boundary
-------------------

Success would establish only:

    bounded dynamic persistence under material loss and finite computational
    opportunity in this Digital Crystal protocol

It would NOT establish:

    homeostasis
    maintenance
    metabolism
    self-preservation
    agency
    organism
    life

Requires beside this file:
    ch18_digital_crystal_persistent_material_state_v7.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-finite-update-budget-v2"
SCHEMA_VERSION = 2
CHAPTER = 21
CHAPTER_TITLE = "What Does It Cost to Stay?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 96,
        "seed_noise_groups": 160,
        "radius": 72,
        "warmup_steps": 14,
        "continuation_steps": 72,
        "late_window": 20,

        # Frozen material-loss regime from Chapter 20/21.
        "loss_rate": 0.08,

        # Fresh candidate family derived from V1 exploratory bracket.
        "candidate_budgets": [48, 64, 80, 96, 128],

        # Bounded-dynamic criteria.
        # Late population slope normalized by late mean population.
        "abs_normalized_slope_max": 0.0025,

        # Population must remain clearly nonzero.
        "minimum_late_population": 150,

        # World-capacity guard.
        "max_capacity_fraction": 0.75,

        # Gross turnover gates, all measured over the late window.
        "minimum_late_mean_losses": 5.0,
        "minimum_late_mean_reoccupations": 2.0,
        "minimum_late_mean_first_occupations": 2.0,

        # Require meaningful gross activity despite near-zero net change.
        # (attachments + losses) / late population per update.
        "minimum_turnover_fraction": 0.05,

        # Avoid classifying a budget as bounded if it is merely crossing
        # rapidly through zero slope because of large noise.
        "maximum_abs_late_net_per_update": 3.0,

        "bootstrap_reps": 3000,
        "alpha": 0.05,
    },
    "standard": {
        "groups": 192,
        "seed_noise_groups": 240,
        "radius": 80,
        "warmup_steps": 14,
        "continuation_steps": 96,
        "late_window": 24,
        "loss_rate": 0.08,
        "candidate_budgets": [48, 64, 80, 96, 128],
        "abs_normalized_slope_max": 0.0025,
        "minimum_late_population": 150,
        "max_capacity_fraction": 0.75,
        "minimum_late_mean_losses": 5.0,
        "minimum_late_mean_reoccupations": 2.0,
        "minimum_late_mean_first_occupations": 2.0,
        "minimum_turnover_fraction": 0.05,
        "maximum_abs_late_net_per_update": 3.0,
        "bootstrap_reps": 5000,
        "alpha": 0.05,
    },
    "full": {
        "groups": 384,
        "seed_noise_groups": 320,
        "radius": 96,
        "warmup_steps": 14,
        "continuation_steps": 120,
        "late_window": 30,
        "loss_rate": 0.08,
        "candidate_budgets": [48, 64, 80, 96, 128],
        "abs_normalized_slope_max": 0.0025,
        "minimum_late_population": 150,
        "max_capacity_fraction": 0.75,
        "minimum_late_mean_losses": 5.0,
        "minimum_late_mean_reoccupations": 2.0,
        "minimum_late_mean_first_occupations": 2.0,
        "minimum_turnover_fraction": 0.05,
        "maximum_abs_late_net_per_update": 3.0,
        "bootstrap_reps": 8000,
        "alpha": 0.05,
    },
}


# ============================================================================
# Base helpers
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


# ============================================================================
# Keyed randomness
# ============================================================================

def keyed_uniform(
    namespace: str,
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    payload = (
        f"{namespace}|{stream_seed}|{step}|{cell[0]}|{cell[1]}"
    ).encode("utf-8")
    digest = hashlib.blake2b(
        payload,
        digest_size=8,
    ).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def loss_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    return keyed_uniform(
        "ch21-v2-loss",
        stream_seed,
        step,
        cell,
    )


def schedule_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    return keyed_uniform(
        "ch21-v2-neutral-schedule",
        stream_seed,
        step,
        cell,
    )


# ============================================================================
# Observer-only occupancy ledger
# ============================================================================

class OccupancyLedger:
    def __init__(self, occupied: Set[Cell]):
        self.ever_occupied = set(occupied)
        self.currently_lost: Set[Cell] = set()

        self.loss_count = 0
        self.first_occupation_count = 0
        self.reoccupation_count = 0

    def classify_additions(
        self,
        additions: Sequence[Cell],
    ) -> Tuple[int, int]:
        first = 0
        reoccupied = 0

        for cell in additions:
            if cell in self.currently_lost:
                reoccupied += 1
                self.reoccupation_count += 1
                self.currently_lost.discard(cell)

            elif cell not in self.ever_occupied:
                first += 1
                self.first_occupation_count += 1

            self.ever_occupied.add(cell)

        return first, reoccupied

    def register_losses(
        self,
        lost: Sequence[Cell],
    ) -> None:
        for cell in lost:
            self.loss_count += 1
            self.currently_lost.add(cell)


# ============================================================================
# Neutral finite-budget growth
# ============================================================================

def select_neutral_candidates(
    frontier: Sequence[Cell],
    budget: int,
    stream_seed: int,
    step: int,
) -> List[Cell]:
    frontier = list(frontier)
    k = max(0, min(int(budget), len(frontier)))

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
    int,
    int,
]:
    occupied_before = set(state.occupied)
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier = frontier_cells(
        occupied_before,
        radius,
    )

    next_step = state.step + 1

    selected = select_neutral_candidates(
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
        crowding = max(0, n - 2)

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

    return (
        out,
        additions,
        len(frontier),
        len(selected),
    )


# ============================================================================
# Background loss
# ============================================================================

def apply_background_loss(
    state: ch18.MaterialCrystalState,
    loss_rate: float,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
]:
    lost = [
        cell
        for cell in sorted(state.occupied)
        if loss_uniform(
            state.stream_seed,
            state.step,
            cell,
        ) < float(loss_rate)
    ]

    out = clone_state(state)

    for cell in lost:
        out.occupied.discard(cell)
        out.birth_time.pop(cell, None)

    if out.population_by_step:
        out.population_by_step[-1] = len(out.occupied)

    return out, lost


# ============================================================================
# One candidate-budget run
# ============================================================================

def run_candidate_budget(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
    budget: int,
) -> dict:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["continuation_steps"]
    late = profile["late_window"]

    gseed = (
        seed
        + group_index * 1009
    )

    env = ch18.make_environment(
        warmup + horizon + 8,
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
        set(state.occupied)
    )

    population = []
    attachments = []
    losses = []
    first = []
    reoccupations = []
    net = []
    frontier = []
    evaluated = []
    capacity = []

    for j in range(horizon):
        state, additions, frontier_n, evaluated_n = (
            budgeted_growth_step(
                state,
                float(env[warmup + j]),
                radius,
                crystal_params,
                budget,
            )
        )

        first_n, reocc_n = (
            ledger.classify_additions(
                additions
            )
        )

        state, lost = apply_background_loss(
            state,
            profile["loss_rate"],
        )
        ledger.register_losses(lost)

        population.append(
            len(state.occupied)
        )
        attachments.append(
            len(additions)
        )
        losses.append(
            len(lost)
        )
        first.append(
            first_n
        )
        reoccupations.append(
            reocc_n
        )
        net.append(
            len(additions) - len(lost)
        )
        frontier.append(
            frontier_n
        )
        evaluated.append(
            evaluated_n
        )

        frac = ch18.capacity_fraction_occupied(
            state.occupied,
            radius,
        )
        capacity.append(frac)

        if not state.occupied:
            remaining = horizon - j - 1

            for arr in [
                population,
                attachments,
                losses,
                first,
                reoccupations,
                net,
                frontier,
                evaluated,
            ]:
                arr.extend(
                    [0] * remaining
                )

            capacity.extend(
                [0.0] * remaining
            )
            break

    y = np.asarray(
        population[-late:],
        dtype=float,
    )
    x = np.arange(
        len(y),
        dtype=float,
    )

    if (
        len(y) >= 2
        and np.mean(y) > 0
    ):
        slope = float(
            np.polyfit(
                x,
                y,
                1,
            )[0]
        )
        normalized_slope = (
            slope / float(np.mean(y))
        )
    else:
        slope = 0.0
        normalized_slope = 0.0

    late_population = float(
        np.mean(population[-late:])
    )
    late_attachments = float(
        np.mean(attachments[-late:])
    )
    late_losses = float(
        np.mean(losses[-late:])
    )
    late_first = float(
        np.mean(first[-late:])
    )
    late_reocc = float(
        np.mean(reoccupations[-late:])
    )
    late_net = float(
        np.mean(net[-late:])
    )

    turnover_fraction = (
        (late_attachments + late_losses)
        / max(1.0, late_population)
    )

    return {
        "budget": int(budget),

        "late_mean_population": (
            late_population
        ),
        "late_population_slope": (
            slope
        ),
        "late_normalized_population_slope": (
            normalized_slope
        ),

        "late_mean_attachments": (
            late_attachments
        ),
        "late_mean_losses": (
            late_losses
        ),
        "late_mean_first_occupations": (
            late_first
        ),
        "late_mean_reoccupations": (
            late_reocc
        ),
        "late_mean_net": (
            late_net
        ),

        "late_turnover_fraction": (
            turnover_fraction
        ),

        "mean_frontier": float(
            np.mean(frontier)
        ),
        "mean_evaluated": float(
            np.mean(evaluated)
        ),
        "mean_evaluation_fraction": float(
            np.mean(
                np.asarray(evaluated)
                / np.maximum(
                    1,
                    np.asarray(frontier),
                )
            )
        ),

        "max_capacity_fraction": float(
            max(capacity)
        ),
        "collapsed": bool(
            population[-1] == 0
        ),

        "population_trajectory": (
            population
        ),
        "attachment_trajectory": (
            attachments
        ),
        "loss_trajectory": (
            losses
        ),
        "first_trajectory": (
            first
        ),
        "reoccupation_trajectory": (
            reoccupations
        ),
    }


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

    for i in range(reps):
        boot[i] = float(np.mean(
            rng.choice(
                arr,
                size=len(arr),
                replace=True,
            )
        ))

    return {
        "n": int(len(arr)),
        "mean": float(
            np.mean(arr)
        ),
        "median": float(
            np.median(arr)
        ),
        "std": (
            float(
                np.std(
                    arr,
                    ddof=1,
                )
            )
            if len(arr) > 1
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
        clean = {
            k: v
            for k, v in payload.items()
            if not k.startswith("_")
        }

        (
            self.root / filename
        ).write_text(
            json.dumps(
                clean,
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
        clean = {
            k: v
            for k, v in payload.items()
            if not k.startswith("_")
        }

        body = (
            "```json\n"
            + json.dumps(
                clean,
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
            (title, body)
        )

    def full_report(
        self,
        metadata: dict,
    ) -> Path:
        path = (
            self.root
            / "ch21-finite-update-budget-v2-full-report.md"
        )

        parts = [
            "# Chapter 21 — What Does It Cost to Stay? (V2)",
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
# Stage 0 — protocol
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": (
            "BOUNDED DYNAMIC PERSISTENCE TEST"
        ),

        "v1_status": (
            "FAILED primary allocation tradeoff because the first-occupation "
            "arm did not clear its predeclared SEI. V2 does not retry that "
            "policy hypothesis."
        ),

        "question": (
            "Under ongoing material loss and neutral finite evaluation budget, "
            "does at least one frozen candidate budget produce approximately "
            "stationary population while gross turnover continues?"
        ),

        "candidate_budgets": (
            profile["candidate_budgets"]
        ),

        "loss_rate": (
            profile["loss_rate"]
        ),

        "success_criteria": {
            "abs_normalized_late_population_slope_max": (
                profile[
                    "abs_normalized_slope_max"
                ]
            ),
            "minimum_late_population": (
                profile[
                    "minimum_late_population"
                ]
            ),
            "maximum_capacity_fraction": (
                profile[
                    "max_capacity_fraction"
                ]
            ),
            "minimum_late_mean_losses": (
                profile[
                    "minimum_late_mean_losses"
                ]
            ),
            "minimum_late_mean_reoccupations": (
                profile[
                    "minimum_late_mean_reoccupations"
                ]
            ),
            "minimum_late_mean_first_occupations": (
                profile[
                    "minimum_late_mean_first_occupations"
                ]
            ),
            "minimum_turnover_fraction": (
                profile[
                    "minimum_turnover_fraction"
                ]
            ),
            "maximum_abs_late_net_per_update": (
                profile[
                    "maximum_abs_late_net_per_update"
                ]
            ),
            "all_required": True,
        },

        "new_sentence_if_successful": (
            "Under ongoing material loss, a finite neutral evaluation budget "
            "can support an approximately bounded Digital Crystal population "
            "while first occupation, loss and reoccupation all continue."
        ),

        "forbidden_overclaims": [
            "homeostasis",
            "maintenance",
            "metabolism",
            "energy",
            "repair",
            "self-preservation",
            "adaptation",
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
        "Stage 0 — Freeze the Bounded-Dynamics Test",
        result,
    )

    return result


# ============================================================================
# Stage 1 — fresh no-loss / high-budget orientation control
# ============================================================================

def stage_1_reference(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    """
    Fresh reference at B=128 under the same loss process.
    This is descriptive and not part of the primary existence decision.
    """
    runs = []

    for g in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 fresh B=128 reference",
    ):
        runs.append(
            run_candidate_budget(
                profile,
                crystal_params,
                seed + 1_000_000,
                g,
                128,
            )
        )

    result = {
        "role": (
            "FRESH DESCRIPTIVE B=128 REFERENCE"
        ),

        "groups": (
            profile["seed_noise_groups"]
        ),

        "late_mean_population": bootstrap_mean_ci(
            [
                r["late_mean_population"]
                for r in runs
            ],
            profile["bootstrap_reps"],
            seed + 1_500_000,
        ),

        "late_normalized_population_slope": bootstrap_mean_ci(
            [
                r["late_normalized_population_slope"]
                for r in runs
            ],
            profile["bootstrap_reps"],
            seed + 1_600_000,
        ),

        "late_mean_net": bootstrap_mean_ci(
            [
                r["late_mean_net"]
                for r in runs
            ],
            profile["bootstrap_reps"],
            seed + 1_700_000,
        ),

        "late_turnover_fraction": bootstrap_mean_ci(
            [
                r["late_turnover_fraction"]
                for r in runs
            ],
            profile["bootstrap_reps"],
            seed + 1_800_000,
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-reference.json",
        result,
    )

    reporter.stage(
        "stage-01-reference.md",
        "Stage 1 — Fresh Reference Under Scarcity",
        result,
    )

    return result


# ============================================================================
# Stage 2 — primary candidate family
# ============================================================================

def classify_budget(
    profile: dict,
    summary: dict,
) -> dict:
    slope_ok = (
        abs(
            summary[
                "late_normalized_population_slope"
            ]["mean"]
        )
        <= profile[
            "abs_normalized_slope_max"
        ]
    )

    population_ok = (
        summary[
            "late_mean_population"
        ]["mean"]
        >= profile[
            "minimum_late_population"
        ]
    )

    unsaturated_ok = (
        summary[
            "max_capacity_fraction"
        ]["mean"]
        < profile[
            "max_capacity_fraction"
        ]
    )

    losses_ok = (
        summary[
            "late_mean_losses"
        ]["mean"]
        >= profile[
            "minimum_late_mean_losses"
        ]
    )

    reocc_ok = (
        summary[
            "late_mean_reoccupations"
        ]["mean"]
        >= profile[
            "minimum_late_mean_reoccupations"
        ]
    )

    first_ok = (
        summary[
            "late_mean_first_occupations"
        ]["mean"]
        >= profile[
            "minimum_late_mean_first_occupations"
        ]
    )

    turnover_ok = (
        summary[
            "late_turnover_fraction"
        ]["mean"]
        >= profile[
            "minimum_turnover_fraction"
        ]
    )

    net_ok = (
        abs(
            summary[
                "late_mean_net"
            ]["mean"]
        )
        <= profile[
            "maximum_abs_late_net_per_update"
        ]
    )

    qualifies = all([
        slope_ok,
        population_ok,
        unsaturated_ok,
        losses_ok,
        reocc_ok,
        first_ok,
        turnover_ok,
        net_ok,
    ])

    return {
        "slope_gate": slope_ok,
        "population_gate": population_ok,
        "unsaturated_gate": unsaturated_ok,
        "loss_gate": losses_ok,
        "reoccupation_gate": reocc_ok,
        "first_occupation_gate": first_ok,
        "turnover_gate": turnover_ok,
        "late_net_gate": net_ok,
        "qualifies_as_bounded_dynamic_regime": bool(
            qualifies
        ),
    }


def stage_2_candidate_family(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    by_budget = {}
    trajectories = {}

    for bi, budget in enumerate(
        profile["candidate_budgets"]
    ):
        runs = []

        for g in tqdm(
            range(profile["groups"]),
            desc=f"Stage 2 candidate B={budget}",
        ):
            runs.append(
                run_candidate_budget(
                    profile,
                    crystal_params,
                    seed
                    + 2_000_000
                    + bi * 100_000,
                    g,
                    budget,
                )
            )

        def summary(field: str):
            vals = [
                r[field]
                for r in runs
            ]

            return bootstrap_mean_ci(
                vals,
                profile[
                    "bootstrap_reps"
                ],
                seed
                + 2_500_000
                + bi * 1000,
            )

        budget_summary = {
            "budget": budget,

            "late_mean_population": summary(
                "late_mean_population"
            ),

            "late_normalized_population_slope": summary(
                "late_normalized_population_slope"
            ),

            "late_mean_attachments": summary(
                "late_mean_attachments"
            ),

            "late_mean_losses": summary(
                "late_mean_losses"
            ),

            "late_mean_first_occupations": summary(
                "late_mean_first_occupations"
            ),

            "late_mean_reoccupations": summary(
                "late_mean_reoccupations"
            ),

            "late_mean_net": summary(
                "late_mean_net"
            ),

            "late_turnover_fraction": summary(
                "late_turnover_fraction"
            ),

            "mean_evaluation_fraction": summary(
                "mean_evaluation_fraction"
            ),

            "max_capacity_fraction": summary(
                "max_capacity_fraction"
            ),

            "collapsed_fraction": float(
                np.mean([
                    r["collapsed"]
                    for r in runs
                ])
            ),
        }

        budget_summary[
            "classification"
        ] = classify_budget(
            profile,
            budget_summary,
        )

        by_budget[
            str(budget)
        ] = budget_summary

        trajectories[
            str(budget)
        ] = list(np.mean(
            np.asarray([
                r[
                    "population_trajectory"
                ]
                for r in runs
            ], dtype=float),
            axis=0,
        ))

    qualifying = [
        int(b)
        for b, s in by_budget.items()
        if s["classification"][
            "qualifies_as_bounded_dynamic_regime"
        ]
    ]

    result = {
        "role": (
            "PRIMARY FROZEN BUDGET-FAMILY TEST"
        ),

        "groups_per_budget": (
            profile["groups"]
        ),

        "candidate_budgets": (
            profile["candidate_budgets"]
        ),

        "by_budget": by_budget,

        "qualifying_budgets": (
            qualifying
        ),

        "at_least_one_qualifies": bool(
            qualifying
        ),

        "status": "MEASURED",

        "_trajectories": trajectories,
    }

    reporter.json(
        "stage-02-candidate-family.json",
        result,
    )

    reporter.stage(
        "stage-02-candidate-family.md",
        "Stage 2 — Does a Bounded Dynamic Budget Exist?",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    xs = np.arange(
        1,
        profile[
            "continuation_steps"
        ] + 1,
    )

    for label, vals in trajectories.items():
        ax.plot(
            xs,
            vals,
            label=f"B={label}",
        )

    ax.set_xlabel(
        "Continuation update"
    )
    ax.set_ylabel(
        "Mean occupied cells"
    )
    ax.set_title(
        "Chapter 21 V2: candidate bounded-dynamic budgets"
    )
    ax.legend()
    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch21-v2-01-bounded-dynamic-candidates.png",
        dpi=160,
    )

    plt.close(fig)

    return result


# ============================================================================
# Stage 3 — descriptive turnover decomposition
# ============================================================================

def stage_3_turnover(
    reporter: Reporter,
    stage2: dict,
) -> dict:
    rows = {}

    for budget, summary in (
        stage2["by_budget"].items()
    ):
        rows[budget] = {
            "late_population": (
                summary[
                    "late_mean_population"
                ]["mean"]
            ),
            "late_net": (
                summary[
                    "late_mean_net"
                ]["mean"]
            ),
            "late_attachments": (
                summary[
                    "late_mean_attachments"
                ]["mean"]
            ),
            "late_losses": (
                summary[
                    "late_mean_losses"
                ]["mean"]
            ),
            "late_first_occupations": (
                summary[
                    "late_mean_first_occupations"
                ]["mean"]
            ),
            "late_reoccupations": (
                summary[
                    "late_mean_reoccupations"
                ]["mean"]
            ),
            "turnover_fraction": (
                summary[
                    "late_turnover_fraction"
                ]["mean"]
            ),
            "qualifies": (
                summary[
                    "classification"
                ][
                    "qualifies_as_bounded_dynamic_regime"
                ]
            ),
        }

    result = {
        "role": (
            "TURNOVER DECOMPOSITION"
        ),

        "by_budget": rows,

        "interpretation_boundary": (
            "This is descriptive support for the primary bounded-dynamics "
            "classification. Turnover is not called metabolism or maintenance."
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-03-turnover.json",
        result,
    )

    reporter.stage(
        "stage-03-turnover.md",
        "Stage 3 — Is Near-Zero Net Growth Hiding Ongoing Turnover?",
        result,
    )

    return result


# ============================================================================
# Stage 4 — verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    stage2: dict,
) -> dict:
    supported = bool(
        stage2[
            "at_least_one_qualifies"
        ]
    )

    qualifying = (
        stage2[
            "qualifying_budgets"
        ]
    )

    if supported:
        status = "SUPPORTED"

        bounded = (
            "Under the frozen Chapter 21 V2 protocol, at least one finite "
            "neutral frontier-evaluation budget supported an approximately "
            "stationary Digital Crystal population while material loss, "
            "reoccupation and first occupation all continued, without "
            "extinction or world-capacity saturation. This establishes a "
            "bounded dynamic persistence regime under ongoing material loss "
            "and finite computational opportunity for the tested conditions."
        )
    else:
        status = "FAILED"

        bounded = (
            "Chapter 21 V2 did not establish a finite neutral evaluation "
            "budget that simultaneously satisfied the predeclared population, "
            "late-slope, turnover, reoccupation, first-occupation, capacity "
            "and late-net criteria for bounded dynamic persistence."
        )

    result = {
        "question": (
            "Can finite computational opportunity support an approximately "
            "bounded Digital Crystal population while gross material turnover "
            "continues?"
        ),

        "qualifying_budgets": (
            qualifying
        ),

        "bounded_dynamic_regime_supported": (
            supported
        ),

        "status": (
            status
        ),

        "bounded_claim": (
            bounded
        ),

        "forbidden_overclaims": [
            "homeostasis",
            "maintenance",
            "metabolism",
            "energy",
            "repair",
            "self-preservation",
            "adaptation",
            "agency",
            "organism",
            "life",
        ],

        "next_question_if_supported": (
            "Can the allocation rule itself emerge from local state rather "
            "than being supplied externally, while preserving the bounded "
            "dynamic regime?"
        ),

        "next_question_if_failed": (
            "Do not add new budgets after seeing the result. Close this "
            "candidate family and reconsider whether frontier evaluations are "
            "the correct scarce computational resource."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        result,
    )

    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 21 V2 Verdict",
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
        default=20260829,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch21-finite-update-budget-v2"
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

        "chapter": CHAPTER,

        "chapter_title": (
            CHAPTER_TITLE
        ),

        "run_type": (
            "BOUNDED DYNAMIC PERSISTENCE TEST"
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

        "canonical_attachment_probability_modified": (
            False
        ),

        "scheduling_policy": (
            "neutral only"
        ),

        "candidate_budgets_frozen_before_v2": (
            profile[
                "candidate_budgets"
            ]
        ),

        "scientific_boundary": (
            "Bounded dynamic persistence under material loss and finite "
            "computational opportunity only. No homeostasis, maintenance, "
            "metabolism, energy, repair, self-preservation, adaptation, "
            "agency, organism, or life claim."
        ),

        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 21 V2 — BOUNDED DYNAMIC PERSISTENCE"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"loss={profile['loss_rate']} "
        f"budgets={profile['candidate_budgets']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )

    s1 = stage_1_reference(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    s2 = stage_2_candidate_family(
        reporter,
        profile,
        crystal_params,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_turnover(
        reporter,
        s2,
    )

    s4 = stage_4_verdict(
        reporter,
        s2,
    )

    metadata.update({
        "finished_at_unix": (
            time.time()
        ),

        "stage_0_status": (
            s0["status"]
        ),

        "stage_1_status": (
            s1["status"]
        ),

        "stage_2_status": (
            s2["status"]
        ),

        "stage_3_status": (
            s3["status"]
        ),

        "final_status": (
            s4["status"]
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
        "CHAPTER 21 V2 COMPLETE"
    )
    print(
        f"protocol={s0['status']}"
    )
    print(
        f"reference={s1['status']}"
    )
    print(
        f"candidate_family={s2['status']}"
    )
    print(
        f"turnover={s3['status']}"
    )
    print(
        f"FINAL={s4['status']}"
    )
    print(
        f"qualifying_budgets={s4['qualifying_budgets']}"
    )
    print(
        f"report={report_path}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
