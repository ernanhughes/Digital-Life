#!/usr/bin/env python3
"""
Chapter 21 — What Does It Cost to Stay? (V3)

Stable process, not stable size
==============================

Chapter 21 V2 FAILED to establish a finite budget with approximately stationary
population under the frozen slope criterion.

But V2 revealed a striking descriptive regularity:

    across B = 48, 64, 80, 96, 128

the late turnover fraction remained near ~0.17 despite large differences in
population scale.

V3 does NOT search for a flatter population slope.
V3 does NOT add new budgets after seeing V2.
V3 does NOT redefine the V2 primary endpoint.

Instead it tests one new substrate-native hypothesis:

    population size may drift while normalized process flows converge toward
    a stable regime.

Scientific question
-------------------

Across different starting sizes and finite evaluation budgets, do normalized
construction/loss flows converge to approximately invariant late-regime values?

Primary process vector
----------------------

For every late-window update, define:

    loss_fraction           = losses / population
    attachment_fraction     = attachments / population
    reoccupation_fraction   = reoccupations / population
    first_fraction          = first_occupations / population
    gross_turnover_fraction = (attachments + losses) / population

V3 asks whether the late means of these quantities are stable:

1. within a run over time,
2. across different starting sizes at the same B,
3. across a frozen set of budgets.

This is not a fixed-point claim.
This is not an attractor claim.
This is not homeostasis.

It is a test for a stable normalized process regime.

Fresh frozen design
-------------------

Budgets:
    B = 48, 64, 80, 96, 128

Starting-size conditions:
    SMALL   : warmup 8
    MEDIUM  : warmup 14
    LARGE   : warmup 20

All use:
    loss rate delta = 0.08
    neutral scheduling only

Primary hypothesis
------------------

For each normalized process metric:

    between-start-size coefficient of variation at each budget <= 0.10

AND

for gross_turnover_fraction specifically:

    between-budget coefficient of variation across budget means <= 0.10

AND

late-window temporal drift in gross_turnover_fraction must be small:

    absolute normalized slope <= 0.0025 per update

All gates must pass.

Scientific boundary
-------------------

Success would establish only:

    a stable normalized turnover regime under the tested Digital Crystal
    loss/scarcity conditions

It would NOT establish:

    homeostasis
    maintenance
    metabolism
    energy
    attractor
    self-preservation
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
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-finite-update-budget-v3"
SCHEMA_VERSION = 3
CHAPTER = 21
CHAPTER_TITLE = "What Does It Cost to Stay?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 48,
        "radius": 72,
        "continuation_steps": 72,
        "late_window": 20,
        "loss_rate": 0.08,

        "candidate_budgets": [48, 64, 80, 96, 128],

        "start_conditions": {
            "small": 8,
            "medium": 14,
            "large": 20,
        },

        # Process stability gates.
        "max_start_size_cv": 0.10,
        "max_budget_cv_gross_turnover": 0.10,
        "max_abs_gross_turnover_slope": 0.0025,

        # Require meaningful continued activity.
        "minimum_gross_turnover_fraction": 0.05,
        "minimum_late_population": 100,
        "max_capacity_fraction": 0.75,

        "bootstrap_reps": 2000,
    },

    "standard": {
        "groups": 96,
        "radius": 80,
        "continuation_steps": 96,
        "late_window": 24,
        "loss_rate": 0.08,

        "candidate_budgets": [48, 64, 80, 96, 128],

        "start_conditions": {
            "small": 8,
            "medium": 14,
            "large": 20,
        },

        "max_start_size_cv": 0.10,
        "max_budget_cv_gross_turnover": 0.10,
        "max_abs_gross_turnover_slope": 0.0025,

        "minimum_gross_turnover_fraction": 0.05,
        "minimum_late_population": 100,
        "max_capacity_fraction": 0.75,

        "bootstrap_reps": 4000,
    },

    "full": {
        "groups": 192,
        "radius": 96,
        "continuation_steps": 120,
        "late_window": 30,
        "loss_rate": 0.08,

        "candidate_budgets": [48, 64, 80, 96, 128],

        "start_conditions": {
            "small": 8,
            "medium": 14,
            "large": 20,
        },

        "max_start_size_cv": 0.10,
        "max_budget_cv_gross_turnover": 0.10,
        "max_abs_gross_turnover_slope": 0.0025,

        "minimum_gross_turnover_fraction": 0.05,
        "minimum_late_population": 100,
        "max_capacity_fraction": 0.75,

        "bootstrap_reps": 6000,
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

    return int.from_bytes(
        digest,
        "big",
    ) / float(2**64)


def loss_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    return keyed_uniform(
        "ch21-v3-loss",
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
        "ch21-v3-schedule",
        stream_seed,
        step,
        cell,
    )


# ============================================================================
# Observer occupancy ledger
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
    ) -> Tuple[int, int]:
        first = 0
        reoccupied = 0

        for cell in additions:
            if cell in self.currently_lost:
                reoccupied += 1
                self.currently_lost.discard(cell)

            elif cell not in self.ever_occupied:
                first += 1

            self.ever_occupied.add(cell)

        return first, reoccupied

    def register_losses(
        self,
        lost: Sequence[Cell],
    ) -> None:
        for cell in lost:
            self.currently_lost.add(cell)


# ============================================================================
# Neutral budgeted growth
# ============================================================================

def select_candidates(
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
    int,
    int,
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

    selected = select_candidates(
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
# Run one start-size / budget condition
# ============================================================================

def run_condition(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
    warmup_steps: int,
    budget: int,
) -> dict:
    radius = profile[
        "radius"
    ]
    horizon = profile[
        "continuation_steps"
    ]
    late = profile[
        "late_window"
    ]

    gseed = (
        seed
        + group_index * 1009
    )

    env = ch18.make_environment(
        warmup_steps
        + horizon
        + 8,
        gseed + 1,
    )

    state = ch18.warm_material_checkpoint(
        env,
        warmup_steps,
        gseed + 2,
        radius,
        crystal_params,
        no_material_params(),
    )

    ledger = OccupancyLedger(
        set(state.occupied)
    )

    population = []
    losses = []
    attachments = []
    first = []
    reoccupations = []
    gross_turnover = []
    loss_fraction = []
    attachment_fraction = []
    first_fraction = []
    reoccupation_fraction = []
    gross_turnover_fraction = []
    capacity = []

    for j in range(
        horizon
    ):
        state, additions, _, _ = (
            budgeted_growth_step(
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

        first_n, reocc_n = (
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

        pop = len(
            state.occupied
        )
        att = len(
            additions
        )
        los = len(
            lost
        )

        population.append(
            pop
        )
        attachments.append(
            att
        )
        losses.append(
            los
        )
        first.append(
            first_n
        )
        reoccupations.append(
            reocc_n
        )
        gross_turnover.append(
            att + los
        )

        denom = max(
            1,
            pop,
        )

        loss_fraction.append(
            los / denom
        )
        attachment_fraction.append(
            att / denom
        )
        first_fraction.append(
            first_n / denom
        )
        reoccupation_fraction.append(
            reocc_n / denom
        )
        gross_turnover_fraction.append(
            (att + los) / denom
        )

        capacity.append(
            ch18.capacity_fraction_occupied(
                state.occupied,
                radius,
            )
        )

        if not state.occupied:
            remaining = (
                horizon - j - 1
            )

            for arr in [
                population,
                losses,
                attachments,
                first,
                reoccupations,
                gross_turnover,
            ]:
                arr.extend(
                    [0] * remaining
                )

            for arr in [
                loss_fraction,
                attachment_fraction,
                first_fraction,
                reoccupation_fraction,
                gross_turnover_fraction,
                capacity,
            ]:
                arr.extend(
                    [0.0] * remaining
                )

            break

    def late_mean(
        values,
    ):
        return float(
            np.mean(
                values[-late:]
            )
        )

    def late_slope(
        values,
    ):
        y = np.asarray(
            values[-late:],
            dtype=float,
        )
        x = np.arange(
            len(y),
            dtype=float,
        )

        if len(y) < 2:
            return 0.0

        return float(
            np.polyfit(
                x,
                y,
                1,
            )[0]
        )

    return {
        "warmup_steps": int(
            warmup_steps
        ),
        "budget": int(
            budget
        ),

        "late_mean_population": late_mean(
            population
        ),

        "late_mean_loss_fraction": late_mean(
            loss_fraction
        ),

        "late_mean_attachment_fraction": late_mean(
            attachment_fraction
        ),

        "late_mean_first_fraction": late_mean(
            first_fraction
        ),

        "late_mean_reoccupation_fraction": late_mean(
            reoccupation_fraction
        ),

        "late_mean_gross_turnover_fraction": late_mean(
            gross_turnover_fraction
        ),

        "late_gross_turnover_fraction_slope": late_slope(
            gross_turnover_fraction
        ),

        "max_capacity_fraction": float(
            max(capacity)
        ),

        "collapsed": bool(
            population[-1] == 0
        ),

        "population_trajectory": population,
        "gross_turnover_fraction_trajectory": gross_turnover_fraction,
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

    for i in range(
        reps
    ):
        boot[i] = float(np.mean(
            rng.choice(
                arr,
                size=len(arr),
                replace=True,
            )
        ))

    return {
        "n": int(
            len(arr)
        ),
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


def coefficient_of_variation(
    values: Sequence[float],
) -> float:
    arr = np.asarray(
        values,
        dtype=float,
    )

    mean = float(
        np.mean(arr)
    )

    if abs(mean) < 1e-12:
        return float("inf")

    return float(
        np.std(
            arr,
            ddof=0,
        )
        / abs(mean)
    )


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
            / "ch21-finite-update-budget-v3-full-report.md"
        )

        parts = [
            "# Chapter 21 — What Does It Cost to Stay? (V3)",
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
            "NORMALIZED PROCESS-STABILITY TEST"
        ),

        "v2_status": (
            "FAILED bounded-population hypothesis because every candidate "
            "missed the frozen population-slope gate. V3 does not retry "
            "population stationarity."
        ),

        "question": (
            "Can normalized construction/loss flows remain stable across "
            "different starting sizes and finite budgets even while total "
            "population drifts?"
        ),

        "candidate_budgets": (
            profile[
                "candidate_budgets"
            ]
        ),

        "start_conditions": (
            profile[
                "start_conditions"
            ]
        ),

        "process_metrics": [
            "loss_fraction",
            "attachment_fraction",
            "reoccupation_fraction",
            "first_fraction",
            "gross_turnover_fraction",
        ],

        "primary_gates": {
            "max_start_size_cv_per_metric_per_budget": (
                profile[
                    "max_start_size_cv"
                ]
            ),
            "max_budget_cv_for_gross_turnover_fraction": (
                profile[
                    "max_budget_cv_gross_turnover"
                ]
            ),
            "max_abs_late_gross_turnover_fraction_slope": (
                profile[
                    "max_abs_gross_turnover_slope"
                ]
            ),
            "minimum_gross_turnover_fraction": (
                profile[
                    "minimum_gross_turnover_fraction"
                ]
            ),
            "minimum_late_population": (
                profile[
                    "minimum_late_population"
                ]
            ),
            "max_capacity_fraction": (
                profile[
                    "max_capacity_fraction"
                ]
            ),
            "all_required": True,
        },

        "new_sentence_if_successful": (
            "Across different starting sizes and finite evaluation budgets, "
            "the Digital Crystal converges to a stable normalized turnover "
            "regime even though absolute population size may drift."
        ),

        "forbidden_overclaims": [
            "homeostasis",
            "maintenance",
            "metabolism",
            "energy",
            "attractor",
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
        "Stage 0 — Freeze the Stable-Process Question",
        result,
    )

    return result


# ============================================================================
# Stage 1 — run all frozen conditions
# ============================================================================

def stage_1_condition_grid(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    metrics = [
        "late_mean_loss_fraction",
        "late_mean_attachment_fraction",
        "late_mean_reoccupation_fraction",
        "late_mean_first_fraction",
        "late_mean_gross_turnover_fraction",
        "late_gross_turnover_fraction_slope",
        "late_mean_population",
        "max_capacity_fraction",
    ]

    by_budget = {}

    for bi, budget in enumerate(
        profile[
            "candidate_budgets"
        ]
    ):
        budget_entry = {}

        for si, (
            start_name,
            warmup_steps,
        ) in enumerate(
            profile[
                "start_conditions"
            ].items()
        ):
            runs = []

            for g in tqdm(
                range(
                    profile[
                        "groups"
                    ]
                ),
                desc=(
                    f"Stage 1 B={budget} "
                    f"start={start_name}"
                ),
            ):
                runs.append(
                    run_condition(
                        profile,
                        crystal_params,
                        seed
                        + 1_000_000
                        + bi * 100_000
                        + si * 10_000,
                        g,
                        warmup_steps,
                        budget,
                    )
                )

            summaries = {}

            for mi, metric in enumerate(
                metrics
            ):
                summaries[
                    metric
                ] = bootstrap_mean_ci(
                    [
                        r[metric]
                        for r in runs
                    ],
                    profile[
                        "bootstrap_reps"
                    ],
                    seed
                    + 1_500_000
                    + bi * 10_000
                    + si * 1000
                    + mi * 10,
                )

            summaries[
                "collapsed_fraction"
            ] = float(np.mean([
                r[
                    "collapsed"
                ]
                for r in runs
            ]))

            budget_entry[
                start_name
            ] = summaries

        by_budget[
            str(budget)
        ] = budget_entry

    result = {
        "role": (
            "FROZEN START-SIZE × BUDGET GRID"
        ),
        "groups_per_condition": (
            profile["groups"]
        ),
        "by_budget": by_budget,
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-condition-grid.json",
        result,
    )

    reporter.stage(
        "stage-01-condition-grid.md",
        "Stage 1 — Run the Frozen Process-Stability Grid",
        result,
    )

    return result


# ============================================================================
# Stage 2 — process invariance analysis
# ============================================================================

def stage_2_process_invariance(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    image_dir: Path,
) -> dict:
    process_keys = {
        "loss_fraction": (
            "late_mean_loss_fraction"
        ),
        "attachment_fraction": (
            "late_mean_attachment_fraction"
        ),
        "reoccupation_fraction": (
            "late_mean_reoccupation_fraction"
        ),
        "first_fraction": (
            "late_mean_first_fraction"
        ),
        "gross_turnover_fraction": (
            "late_mean_gross_turnover_fraction"
        ),
    }

    start_size_cv_by_budget = {}
    mean_gross_by_budget = {}
    slope_abs_by_budget = {}
    population_min_by_budget = {}
    capacity_max_by_budget = {}
    collapsed_max_by_budget = {}

    all_start_cv_pass = True
    all_slope_pass = True
    all_activity_pass = True
    all_population_pass = True
    all_capacity_pass = True
    all_collapse_pass = True

    for budget, starts in (
        stage1[
            "by_budget"
        ].items()
    ):
        start_size_cv_by_budget[
            budget
        ] = {}

        for label, metric_key in (
            process_keys.items()
        ):
            vals = [
                starts[start][metric_key]["mean"]
                for start in starts
            ]

            cv = (
                coefficient_of_variation(
                    vals
                )
            )

            passed = (
                cv
                <= profile[
                    "max_start_size_cv"
                ]
            )

            start_size_cv_by_budget[
                budget
            ][label] = {
                "cv": cv,
                "passed": passed,
                "start_means": {
                    start: starts[
                        start
                    ][
                        metric_key
                    ]["mean"]
                    for start in starts
                },
            }

            all_start_cv_pass = (
                all_start_cv_pass
                and passed
            )

        gross_vals = [
            starts[start][
                "late_mean_gross_turnover_fraction"
            ]["mean"]
            for start in starts
        ]

        mean_gross = float(
            np.mean(
                gross_vals
            )
        )

        mean_gross_by_budget[
            budget
        ] = mean_gross

        activity_ok = (
            mean_gross
            >= profile[
                "minimum_gross_turnover_fraction"
            ]
        )

        all_activity_pass = (
            all_activity_pass
            and activity_ok
        )

        slope_vals = [
            abs(
                starts[start][
                    "late_gross_turnover_fraction_slope"
                ]["mean"]
            )
            for start in starts
        ]

        max_abs_slope = float(
            max(
                slope_vals
            )
        )

        slope_abs_by_budget[
            budget
        ] = max_abs_slope

        slope_ok = (
            max_abs_slope
            <= profile[
                "max_abs_gross_turnover_slope"
            ]
        )

        all_slope_pass = (
            all_slope_pass
            and slope_ok
        )

        pops = [
            starts[start][
                "late_mean_population"
            ]["mean"]
            for start in starts
        ]

        min_pop = float(
            min(
                pops
            )
        )

        population_min_by_budget[
            budget
        ] = min_pop

        pop_ok = (
            min_pop
            >= profile[
                "minimum_late_population"
            ]
        )

        all_population_pass = (
            all_population_pass
            and pop_ok
        )

        capacities = [
            starts[start][
                "max_capacity_fraction"
            ]["mean"]
            for start in starts
        ]

        max_cap = float(
            max(
                capacities
            )
        )

        capacity_max_by_budget[
            budget
        ] = max_cap

        cap_ok = (
            max_cap
            < profile[
                "max_capacity_fraction"
            ]
        )

        all_capacity_pass = (
            all_capacity_pass
            and cap_ok
        )

        collapsed = [
            starts[start][
                "collapsed_fraction"
            ]
            for start in starts
        ]

        max_collapsed = float(
            max(
                collapsed
            )
        )

        collapsed_max_by_budget[
            budget
        ] = max_collapsed

        collapse_ok = (
            max_collapsed == 0.0
        )

        all_collapse_pass = (
            all_collapse_pass
            and collapse_ok
        )

    budget_cv_gross = (
        coefficient_of_variation(
            list(
                mean_gross_by_budget.values()
            )
        )
    )

    budget_cv_pass = (
        budget_cv_gross
        <= profile[
            "max_budget_cv_gross_turnover"
        ]
    )

    supported = all([
        all_start_cv_pass,
        budget_cv_pass,
        all_slope_pass,
        all_activity_pass,
        all_population_pass,
        all_capacity_pass,
        all_collapse_pass,
    ])

    result = {
        "role": (
            "PRIMARY NORMALIZED PROCESS-INVARIANCE TEST"
        ),

        "start_size_cv_by_budget": (
            start_size_cv_by_budget
        ),

        "mean_gross_turnover_fraction_by_budget": (
            mean_gross_by_budget
        ),

        "gross_turnover_fraction_between_budget_cv": (
            budget_cv_gross
        ),

        "gross_turnover_between_budget_cv_gate_passed": (
            budget_cv_pass
        ),

        "max_abs_gross_turnover_fraction_slope_by_budget": (
            slope_abs_by_budget
        ),

        "minimum_late_population_by_budget": (
            population_min_by_budget
        ),

        "maximum_capacity_fraction_by_budget": (
            capacity_max_by_budget
        ),

        "maximum_collapsed_fraction_by_budget": (
            collapsed_max_by_budget
        ),

        "all_start_size_cv_gates_passed": (
            all_start_cv_pass
        ),

        "all_temporal_slope_gates_passed": (
            all_slope_pass
        ),

        "all_activity_gates_passed": (
            all_activity_pass
        ),

        "all_population_gates_passed": (
            all_population_pass
        ),

        "all_capacity_gates_passed": (
            all_capacity_pass
        ),

        "all_collapse_gates_passed": (
            all_collapse_pass
        ),

        "stable_normalized_process_regime_supported": (
            supported
        ),

        "status": "MEASURED",
    }

    reporter.json(
        "stage-02-process-invariance.json",
        result,
    )

    reporter.stage(
        "stage-02-process-invariance.md",
        "Stage 2 — Are the Normalized Flows Stable?",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    labels = list(
        mean_gross_by_budget.keys()
    )

    values = [
        mean_gross_by_budget[
            x
        ]
        for x in labels
    ]

    ax.plot(
        [int(x) for x in labels],
        values,
        marker="o",
    )

    ax.set_xlabel(
        "Evaluation budget B"
    )

    ax.set_ylabel(
        "Mean late gross turnover / population"
    )

    ax.set_title(
        "Chapter 21 V3: normalized turnover across budgets"
    )

    fig.tight_layout()

    fig.savefig(
        image_dir
        / "ch21-v3-01-normalized-turnover-vs-budget.png",
        dpi=160,
    )

    plt.close(fig)

    return result


# ============================================================================
# Stage 3 — bounded verdict
# ============================================================================

def stage_3_verdict(
    reporter: Reporter,
    stage2: dict,
) -> dict:
    supported = bool(
        stage2[
            "stable_normalized_process_regime_supported"
        ]
    )

    if supported:
        status = "SUPPORTED"

        bounded = (
            "Under the frozen Chapter 21 V3 protocol, normalized construction, "
            "loss and turnover flows remained within the predeclared stability "
            "bounds across different starting sizes and finite evaluation "
            "budgets, while substantial gross turnover continued. This "
            "supports a stable normalized process regime despite drift in "
            "absolute population scale."
        )

    else:
        status = "FAILED"

        bounded = (
            "Chapter 21 V3 did not establish that normalized construction, "
            "loss and turnover flows satisfy all predeclared invariance and "
            "temporal-stability criteria across different starting sizes and "
            "finite evaluation budgets."
        )

    result = {
        "question": (
            "Can the Digital Crystal exhibit a stable normalized turnover "
            "regime even when absolute population size drifts?"
        ),

        "stable_normalized_process_regime_supported": (
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
            "attractor",
            "self-preservation",
            "adaptation",
            "agency",
            "organism",
            "life",
        ],

        "next_question_if_supported": (
            "Does the stable process occupy a causally coherent region whose "
            "future is predicted better by its own internal state than by the "
            "surrounding lattice?"
        ),

        "next_question_if_failed": (
            "Do not relax the invariance thresholds after seeing the result. "
            "Close Chapter 21 and move to causal-individuation tests."
        ),
    }

    reporter.json(
        "stage-03-verdict.json",
        result,
    )

    reporter.stage(
        "stage-03-verdict.md",
        "Stage 3 — Bounded Chapter 21 V3 Verdict",
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
        default=20260830,
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch21-finite-update-budget-v3"
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
            "NORMALIZED PROCESS-STABILITY TEST"
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

        "candidate_budgets_frozen": (
            profile[
                "candidate_budgets"
            ]
        ),

        "start_conditions_frozen": (
            profile[
                "start_conditions"
            ]
        ),

        "scheduling_policy": (
            "neutral only"
        ),

        "scientific_boundary": (
            "Stable normalized process flows only. No homeostasis, "
            "maintenance, metabolism, energy, attractor, self-preservation, "
            "adaptation, agency, organism, or life claim."
        ),

        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 21 V3 — STABLE PROCESS, NOT STABLE SIZE"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"budgets={profile['candidate_budgets']} "
        f"starts={profile['start_conditions']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )

    s1 = stage_1_condition_grid(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    s2 = stage_2_process_invariance(
        reporter,
        profile,
        s1,
        args.image_dir,
    )

    s3 = stage_3_verdict(
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

        "final_status": (
            s3["status"]
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
        "CHAPTER 21 V3 COMPLETE"
    )
    print(
        f"protocol={s0['status']}"
    )
    print(
        f"condition_grid={s1['status']}"
    )
    print(
        f"process_invariance={s2['status']}"
    )
    print(
        f"FINAL={s3['status']}"
    )
    print(
        f"report={report_path}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
