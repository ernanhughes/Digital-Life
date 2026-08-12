#!/usr/bin/env python3
"""
Chapter 21 — What Does It Cost to Stay? (V1)

Finite construction opportunity
===============================

Chapter 20 discovered that, when computation is effectively unlimited, material
loss is followed by very high and rapid reoccupation.  More than 93% of lost
sites were reused under the tested exact-count conditions.

But the canonical Digital Crystal evaluates every eligible frontier site on
every update.

That means reoccupation and outward construction do not truly compete.

Chapter 21 removes that luxury.

One new substrate constraint:

    at most B frontier sites may be evaluated for attachment per update

An unevaluated site does not receive an attachment draw on that update.

Nothing else is added.

There is no:
    maintenance controller
    repair policy
    energy
    metabolism
    target size
    homeostasis variable
    memory-based scheduler

Scientific questions
--------------------

1. Under ongoing material loss, does finite evaluation budget change sustainable
   crystal scale and material turnover?

2. At the SAME finite budget, does local scheduling change what the crystal
   preserves versus what it builds?

The scheduling policies use only current local geometry:

    neutral
        keyed random frontier ordering

    high_support
        evaluate candidates with MORE occupied neighbours first

    low_support
        evaluate candidates with FEWER occupied neighbours first

These policies do not know whether a cell is a reoccupation site.  Reoccupation
is classified only by an observer-side occupancy ledger.

Primary fixed-budget tradeoff test
----------------------------------

At B = 256 candidate evaluations/update and background loss delta = 0.08:

    high_support should increase reoccupation per loss
    low_support should increase first occupations per 1000 evaluations

Both effects must clear frozen magnitude gates for the tradeoff claim.

Secondary budget sweep
----------------------

Under neutral scheduling:

    B = 64, 128, 256, 512, 1024, 2048, unlimited

This characterizes how late population, first occupation, reoccupation,
evaluation pressure and net growth change with computational opportunity.

Scientific boundary
-------------------

This tests allocation under computational scarcity.

It does NOT establish:
    maintenance
    homeostasis
    metabolism
    energy
    repair
    adaptation
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
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-finite-update-budget-v1"
SCHEMA_VERSION = 1
CHAPTER = 21
CHAPTER_TITLE = "What Does It Cost to Stay?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 48,
        "seed_noise_groups": 96,
        "radius": 72,
        "warmup_steps": 14,
        "continuation_steps": 48,
        "late_window": 12,

        # Frozen from the Chapter 20 characterized non-collapse regime.
        "loss_rate": 0.08,

        # Primary fixed-budget policy comparison.
        "primary_budget": 256,

        # Secondary neutral-policy budget characterization.
        "budget_sweep": [64, 128, 256, 512, 1024, 2048, None],

        # Primary tradeoff SEIs.
        # High-support must improve reoccupation/loss by >= 0.15.
        "sei_reoccupation_per_loss": 0.15,

        # Low-support must improve first occupations per 1000 evaluations
        # by >= 100, i.e. 0.10 first occupations/evaluation.
        "sei_first_occupations_per_1000_evals": 100.0,

        "bootstrap_reps": 2000,
        "permutations": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
    },
    "standard": {
        "groups": 96,
        "seed_noise_groups": 160,
        "radius": 80,
        "warmup_steps": 14,
        "continuation_steps": 64,
        "late_window": 16,
        "loss_rate": 0.08,
        "primary_budget": 256,
        "budget_sweep": [64, 128, 256, 512, 1024, 2048, None],
        "sei_reoccupation_per_loss": 0.15,
        "sei_first_occupations_per_1000_evals": 100.0,
        "bootstrap_reps": 4000,
        "permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
    },
    "full": {
        "groups": 192,
        "seed_noise_groups": 240,
        "radius": 96,
        "warmup_steps": 14,
        "continuation_steps": 80,
        "late_window": 20,
        "loss_rate": 0.08,
        "primary_budget": 256,
        "budget_sweep": [64, 128, 256, 512, 1024, 2048, None],
        "sei_reoccupation_per_loss": 0.15,
        "sei_first_occupations_per_1000_evals": 100.0,
        "bootstrap_reps": 6000,
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


def hole_count(occupied: Set[Cell]) -> int:
    candidates = set()

    for cell in occupied:
        for nb in ch18.neighbors(cell):
            if nb not in occupied:
                candidates.add(nb)

    return sum(
        all(nb in occupied for nb in ch18.neighbors(cell))
        for cell in candidates
    )


# ============================================================================
# Independent keyed scheduling / loss RNG
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
        "ch21-loss",
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
        "ch21-schedule",
        stream_seed,
        step,
        cell,
    )


# ============================================================================
# Observer-only occupancy ledger
# ============================================================================

class OccupancyLedger:
    """
    Observer-side site history.

    None of these fields influence candidate selection or attachment dynamics.
    """

    def __init__(self, occupied: Set[Cell]):
        self.ever_occupied = set(occupied)
        self.currently_lost: Set[Cell] = set()

        self.loss_count = 0
        self.first_occupation_count = 0
        self.reoccupation_count = 0

        self.unique_lost_sites: Set[Cell] = set()
        self.unique_reoccupied_sites: Set[Cell] = set()

        self.last_loss_step: Dict[Cell, int] = {}
        self.reoccupation_delays: List[int] = []

    def classify_additions(
        self,
        additions: Sequence[Cell],
        step: int,
    ) -> Tuple[int, int]:
        first = 0
        reoccupied = 0

        for cell in additions:
            if cell in self.currently_lost:
                reoccupied += 1
                self.reoccupation_count += 1
                self.unique_reoccupied_sites.add(cell)

                if cell in self.last_loss_step:
                    self.reoccupation_delays.append(
                        step - self.last_loss_step[cell]
                    )

                self.currently_lost.discard(cell)

            elif cell not in self.ever_occupied:
                first += 1
                self.first_occupation_count += 1

            self.ever_occupied.add(cell)

        return first, reoccupied

    def register_losses(
        self,
        lost: Sequence[Cell],
        step: int,
    ) -> None:
        for cell in lost:
            self.loss_count += 1
            self.currently_lost.add(cell)
            self.unique_lost_sites.add(cell)
            self.last_loss_step[cell] = step

    def summary(self) -> dict:
        return {
            "loss_count": int(self.loss_count),
            "first_occupation_count": int(
                self.first_occupation_count
            ),
            "reoccupation_count": int(
                self.reoccupation_count
            ),
            "reoccupation_per_loss": (
                float(self.reoccupation_count / self.loss_count)
                if self.loss_count
                else 0.0
            ),
            "lost_site_reoccupied_fraction": (
                float(
                    len(self.unique_reoccupied_sites)
                    / len(self.unique_lost_sites)
                )
                if self.unique_lost_sites
                else 0.0
            ),
            "mean_reoccupation_delay": (
                float(np.mean(self.reoccupation_delays))
                if self.reoccupation_delays
                else None
            ),
        }


# ============================================================================
# Candidate scheduling under finite budget
# ============================================================================

def occupied_neighbor_count(
    cell: Cell,
    occupied: Set[Cell],
) -> int:
    return sum(
        nb in occupied
        for nb in ch18.neighbors(cell)
    )


def select_candidates(
    frontier: Sequence[Cell],
    occupied: Set[Cell],
    budget: Optional[int],
    policy: str,
    stream_seed: int,
    step: int,
) -> List[Cell]:
    """
    Select at most B frontier sites to receive canonical attachment evaluation.

    Policies use ONLY current geometry and keyed scheduling noise.
    They never inspect the observer occupancy ledger.
    """
    frontier = list(frontier)

    if budget is None or budget >= len(frontier):
        return sorted(frontier)

    k = max(0, min(int(budget), len(frontier)))

    if policy == "neutral":
        ranked = sorted(
            frontier,
            key=lambda c: (
                schedule_uniform(stream_seed, step, c),
                c,
            ),
        )

    elif policy == "high_support":
        ranked = sorted(
            frontier,
            key=lambda c: (
                -occupied_neighbor_count(c, occupied),
                schedule_uniform(stream_seed, step, c),
                c,
            ),
        )

    elif policy == "low_support":
        ranked = sorted(
            frontier,
            key=lambda c: (
                occupied_neighbor_count(c, occupied),
                schedule_uniform(stream_seed, step, c),
                c,
            ),
        )

    else:
        raise ValueError(f"Unknown policy: {policy!r}")

    return ranked[:k]


# ============================================================================
# Budgeted canonical growth
# ============================================================================

def budgeted_growth_step(
    state: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    budget: Optional[int],
    policy: str,
) -> Tuple[
    ch18.MaterialCrystalState,
    List[Cell],
    int,
    int,
]:
    """
    Canonical Digital Crystal attachment rule, but evaluate only selected
    frontier candidates.

    Returns:
        new state
        additions
        total frontier count
        evaluated count
    """
    occupied_before = set(state.occupied)
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier = frontier_cells(
        occupied_before,
        radius,
    )

    next_step = state.step + 1

    selected = select_candidates(
        frontier,
        occupied_before,
        budget,
        policy,
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
) -> Tuple[ch18.MaterialCrystalState, List[Cell]]:
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
# One run
# ============================================================================

def run_budget_policy(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
    budget: Optional[int],
    policy: str,
) -> dict:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["continuation_steps"]

    gseed = seed + group_index * 1009
    env = ch18.make_environment(
        warmup + horizon + 8,
        gseed + 1,
    )

    # Warmup remains the canonical unlimited no-loss crystal.
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

    per_step = {
        "population": [],
        "frontier": [],
        "evaluated": [],
        "evaluation_fraction": [],
        "attachments": [],
        "first": [],
        "reoccupation": [],
        "losses": [],
        "net": [],
        "holes": [],
    }

    for j in range(horizon):
        state, additions, frontier_n, evaluated_n = (
            budgeted_growth_step(
                state,
                float(env[warmup + j]),
                radius,
                crystal_params,
                budget,
                policy,
            )
        )

        first, reoccupied = ledger.classify_additions(
            additions,
            state.step,
        )

        state, lost = apply_background_loss(
            state,
            profile["loss_rate"],
        )
        ledger.register_losses(
            lost,
            state.step,
        )

        per_step["population"].append(
            len(state.occupied)
        )
        per_step["frontier"].append(
            frontier_n
        )
        per_step["evaluated"].append(
            evaluated_n
        )
        per_step["evaluation_fraction"].append(
            evaluated_n / frontier_n
            if frontier_n
            else 0.0
        )
        per_step["attachments"].append(
            len(additions)
        )
        per_step["first"].append(
            first
        )
        per_step["reoccupation"].append(
            reoccupied
        )
        per_step["losses"].append(
            len(lost)
        )
        per_step["net"].append(
            len(additions) - len(lost)
        )
        per_step["holes"].append(
            hole_count(state.occupied)
        )

        if not state.occupied:
            # Empty crystal cannot regrow under the frozen neighbour rule.
            remaining = horizon - j - 1
            for key in per_step:
                fill = 0.0 if key == "evaluation_fraction" else 0
                per_step[key].extend(
                    [fill] * remaining
                )
            break

        frac = ch18.capacity_fraction_occupied(
            state.occupied,
            radius,
        )
        if frac >= profile["max_capacity_fraction"]:
            raise RuntimeError(
                f"Saturation guard: {frac:.3f}"
            )

    late = profile["late_window"]
    led = ledger.summary()

    total_evals = int(
        sum(per_step["evaluated"])
    )

    return {
        "budget": (
            "unlimited"
            if budget is None
            else int(budget)
        ),
        "policy": policy,

        "final_population": int(
            per_step["population"][-1]
        ),
        "late_mean_population": float(
            np.mean(per_step["population"][-late:])
        ),
        "late_mean_net": float(
            np.mean(per_step["net"][-late:])
        ),
        "late_mean_holes": float(
            np.mean(per_step["holes"][-late:])
        ),

        "mean_frontier": float(
            np.mean(per_step["frontier"])
        ),
        "mean_evaluated": float(
            np.mean(per_step["evaluated"])
        ),
        "mean_evaluation_fraction": float(
            np.mean(per_step["evaluation_fraction"])
        ),

        "total_evaluations": total_evals,
        "total_attachments": int(
            sum(per_step["attachments"])
        ),
        "first_occupation_count": led[
            "first_occupation_count"
        ],
        "reoccupation_count": led[
            "reoccupation_count"
        ],
        "loss_count": led[
            "loss_count"
        ],
        "reoccupation_per_loss": led[
            "reoccupation_per_loss"
        ],
        "lost_site_reoccupied_fraction": led[
            "lost_site_reoccupied_fraction"
        ],
        "mean_reoccupation_delay": led[
            "mean_reoccupation_delay"
        ],

        "first_occupations_per_1000_evals": (
            1000.0
            * led["first_occupation_count"]
            / max(1, total_evals)
        ),
        "reoccupations_per_1000_evals": (
            1000.0
            * led["reoccupation_count"]
            / max(1, total_evals)
        ),

        "collapsed": bool(
            per_step["population"][-1] == 0
        ),

        "per_step": per_step,
    }


# ============================================================================
# Statistics
# ============================================================================

def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    arr = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)

    boot = np.empty(reps, dtype=float)

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
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": (
            float(np.std(arr, ddof=1))
            if len(arr) > 1
            else 0.0
        ),
        "ci95_low": float(
            np.quantile(boot, 0.025)
        ),
        "ci95_high": float(
            np.quantile(boot, 0.975)
        ),
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(values, dtype=float)
    observed = float(np.mean(arr))

    rng = np.random.default_rng(seed)
    null = np.empty(
        permutations,
        dtype=float,
    )

    for i in range(permutations):
        signs = rng.choice(
            np.asarray([-1.0, 1.0]),
            size=len(arr),
        )
        null[i] = float(
            np.mean(arr * signs)
        )

    p = (
        1.0
        + float(np.sum(null >= observed))
    ) / (permutations + 1.0)

    return {
        "observed_mean": observed,
        "p_value": p,
        "alternative": "greater",
        "permutations": permutations,
    }


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
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
        (self.root / filename).write_text(
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

        (self.root / filename).write_text(
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
            / "ch21-finite-update-budget-v1-full-report.md"
        )

        parts = [
            "# Chapter 21 — What Does It Cost to Stay?",
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
            "FINITE CONSTRUCTION-EVALUATION BUDGET"
        ),
        "chapter_20_bridge": (
            "Chapter 20 measured rapid reoccupation under effectively "
            "unlimited frontier evaluation. Chapter 21 limits how many "
            "frontier candidates can receive an attachment evaluation."
        ),
        "new_constraint": (
            "At most B frontier candidates are evaluated for attachment "
            "per update."
        ),
        "loss_rate": profile[
            "loss_rate"
        ],
        "primary_budget": profile[
            "primary_budget"
        ],
        "primary_policies": [
            "high_support",
            "low_support",
        ],
        "policy_information_boundary": (
            "Policies use only current occupied-neighbour count plus keyed "
            "scheduling noise. They do not know occupancy history or whether "
            "a candidate is a reoccupation site."
        ),
        "primary_tradeoff_requirements": {
            "high_support_reoccupation_per_loss_advantage_min": profile[
                "sei_reoccupation_per_loss"
            ],
            "low_support_first_occupations_per_1000_evals_advantage_min": profile[
                "sei_first_occupations_per_1000_evals"
            ],
            "alpha": profile["alpha"],
            "both_required": True,
        },
        "secondary_budget_sweep": [
            "unlimited" if b is None else b
            for b in profile["budget_sweep"]
        ],
        "new_sentence_if_primary_succeeds": (
            "With computational opportunity held fixed, local scheduling "
            "changes the tradeoff between reusing lost material and occupying "
            "new sites."
        ),
        "forbidden_overclaims": [
            "maintenance",
            "homeostasis",
            "metabolism",
            "energy",
            "repair",
            "adaptation",
            "agency",
            "choice",
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
        "Stage 0 — Freeze the Scarcity Question",
        result,
    )
    return result


# ============================================================================
# Stage 1 — unlimited reference
# ============================================================================

def stage_1_unlimited_reference(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    runs = []

    for g in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 unlimited reference",
    ):
        runs.append(
            run_budget_policy(
                profile,
                crystal_params,
                seed + 1_000_000,
                g,
                None,
                "neutral",
            )
        )

    def mean_field(field: str):
        vals = [r[field] for r in runs]
        vals = [
            v for v in vals
            if v is not None
        ]
        return float(np.mean(vals))

    result = {
        "role": (
            "UNLIMITED-EVALUATION REFERENCE"
        ),
        "groups": profile[
            "seed_noise_groups"
        ],
        "mean_late_population": mean_field(
            "late_mean_population"
        ),
        "mean_evaluation_fraction": mean_field(
            "mean_evaluation_fraction"
        ),
        "mean_first_occupations_per_1000_evals": mean_field(
            "first_occupations_per_1000_evals"
        ),
        "mean_reoccupations_per_1000_evals": mean_field(
            "reoccupations_per_1000_evals"
        ),
        "mean_reoccupation_per_loss": mean_field(
            "reoccupation_per_loss"
        ),
        "mean_lost_site_reoccupied_fraction": mean_field(
            "lost_site_reoccupied_fraction"
        ),
        "mean_reoccupation_delay": mean_field(
            "mean_reoccupation_delay"
        ),
        "collapsed_fraction": float(np.mean([
            r["collapsed"]
            for r in runs
        ])),
        "status": "MEASURED",
    }

    reporter.json(
        "stage-01-unlimited-reference.json",
        result,
    )
    reporter.stage(
        "stage-01-unlimited-reference.md",
        "Stage 1 — Measure the Unlimited-Opportunity Reference",
        result,
    )
    return result


# ============================================================================
# Stage 2 — neutral budget sweep
# ============================================================================

def stage_2_budget_sweep(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    by_budget = {}
    trajectories = {}

    for bi, budget in enumerate(
        profile["budget_sweep"]
    ):
        label = (
            "unlimited"
            if budget is None
            else str(budget)
        )

        runs = []

        for g in tqdm(
            range(profile["groups"]),
            desc=f"Stage 2 neutral B={label}",
        ):
            runs.append(
                run_budget_policy(
                    profile,
                    crystal_params,
                    seed
                    + 2_000_000
                    + bi * 100_000,
                    g,
                    budget,
                    "neutral",
                )
            )

        def summary(field: str):
            vals = [
                r[field]
                for r in runs
                if r[field] is not None
            ]
            return bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed
                + 2_500_000
                + bi * 1000,
            )

        by_budget[label] = {
            "budget": label,
            "late_mean_population": summary(
                "late_mean_population"
            ),
            "mean_evaluation_fraction": summary(
                "mean_evaluation_fraction"
            ),
            "first_occupations_per_1000_evals": summary(
                "first_occupations_per_1000_evals"
            ),
            "reoccupations_per_1000_evals": summary(
                "reoccupations_per_1000_evals"
            ),
            "reoccupation_per_loss": summary(
                "reoccupation_per_loss"
            ),
            "lost_site_reoccupied_fraction": summary(
                "lost_site_reoccupied_fraction"
            ),
            "late_mean_net": summary(
                "late_mean_net"
            ),
            "collapsed_fraction": float(np.mean([
                r["collapsed"]
                for r in runs
            ])),
        }

        trajectories[label] = list(
            np.mean(
                np.asarray([
                    r["per_step"]["population"]
                    for r in runs
                ], dtype=float),
                axis=0,
            )
        )

    finite_labels = [
        str(b)
        for b in profile["budget_sweep"]
        if b is not None
    ]

    budgets_numeric = np.asarray(
        [int(x) for x in finite_labels],
        dtype=float,
    )
    pops = np.asarray([
        by_budget[x]["late_mean_population"]["mean"]
        for x in finite_labels
    ], dtype=float)

    # Descriptive monotonicity only; no formal law claim.
    order = np.argsort(budgets_numeric)
    monotone_non_decreasing = bool(
        np.all(
            np.diff(pops[order])
            >= -1e-12
        )
    )

    result = {
        "role": (
            "NEUTRAL-POLICY BUDGET CHARACTERIZATION"
        ),
        "loss_rate": profile["loss_rate"],
        "by_budget": by_budget,
        "finite_budget_late_population_monotone_non_decreasing": (
            monotone_non_decreasing
        ),
        "interpretation_boundary": (
            "This sweep characterizes computational opportunity. "
            "It does not establish a universal scaling law."
        ),
        "status": "MEASURED",
        "_trajectories": trajectories,
    }

    reporter.json(
        "stage-02-budget-sweep.json",
        result,
    )
    reporter.stage(
        "stage-02-budget-sweep.md",
        "Stage 2 — What Changes as Evaluation Budget Shrinks?",
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
        profile["continuation_steps"] + 1,
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
        "Chapter 21: population under finite evaluation budget"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir
        / "ch21-01-budget-population-trajectories.png",
        dpi=160,
    )
    plt.close(fig)

    return result


# ============================================================================
# Stage 3 — primary fixed-budget policy tradeoff
# ============================================================================

def stage_3_policy_tradeoff(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    high_runs = []
    low_runs = []
    neutral_runs = []

    budget = profile["primary_budget"]

    for g in tqdm(
        range(profile["groups"]),
        desc="Stage 3 fixed-budget policy triplets",
    ):
        base_seed = (
            seed
            + 3_000_000
        )

        # Same group index, environment seed, stream seed and budget.
        high_runs.append(
            run_budget_policy(
                profile,
                crystal_params,
                base_seed,
                g,
                budget,
                "high_support",
            )
        )
        low_runs.append(
            run_budget_policy(
                profile,
                crystal_params,
                base_seed,
                g,
                budget,
                "low_support",
            )
        )
        neutral_runs.append(
            run_budget_policy(
                profile,
                crystal_params,
                base_seed,
                g,
                budget,
                "neutral",
            )
        )

    reocc_adv = [
        hi["reoccupation_per_loss"]
        - lo["reoccupation_per_loss"]
        for hi, lo in zip(
            high_runs,
            low_runs,
        )
    ]

    first_adv = [
        lo["first_occupations_per_1000_evals"]
        - hi["first_occupations_per_1000_evals"]
        for hi, lo in zip(
            high_runs,
            low_runs,
        )
    ]

    reocc_summary = bootstrap_mean_ci(
        reocc_adv,
        profile["bootstrap_reps"],
        seed + 3_500_000,
    )
    first_summary = bootstrap_mean_ci(
        first_adv,
        profile["bootstrap_reps"],
        seed + 3_600_000,
    )

    reocc_test = signflip_greater(
        reocc_adv,
        profile["permutations"],
        seed + 3_700_000,
    )
    first_test = signflip_greater(
        first_adv,
        profile["permutations"],
        seed + 3_800_000,
    )

    def aggregate(runs, field):
        vals = [
            r[field]
            for r in runs
            if r[field] is not None
        ]
        return float(np.mean(vals))

    policy_summary = {}

    for name, runs in [
        ("high_support", high_runs),
        ("neutral", neutral_runs),
        ("low_support", low_runs),
    ]:
        policy_summary[name] = {
            "mean_late_population": aggregate(
                runs,
                "late_mean_population",
            ),
            "mean_reoccupation_per_loss": aggregate(
                runs,
                "reoccupation_per_loss",
            ),
            "mean_first_occupations_per_1000_evals": aggregate(
                runs,
                "first_occupations_per_1000_evals",
            ),
            "mean_reoccupations_per_1000_evals": aggregate(
                runs,
                "reoccupations_per_1000_evals",
            ),
            "mean_lost_site_reoccupied_fraction": aggregate(
                runs,
                "lost_site_reoccupied_fraction",
            ),
            "mean_evaluation_fraction": aggregate(
                runs,
                "mean_evaluation_fraction",
            ),
            "mean_late_net": aggregate(
                runs,
                "late_mean_net",
            ),
            "collapsed_fraction": float(np.mean([
                r["collapsed"]
                for r in runs
            ])),
        }

    result = {
        "role": (
            "PRIMARY FIXED-BUDGET ALLOCATION TRADEOFF"
        ),
        "budget": budget,
        "loss_rate": profile["loss_rate"],
        "policies_use_history": False,
        "policy_summary": policy_summary,

        "high_minus_low_reoccupation_per_loss": (
            reocc_summary
        ),
        "reoccupation_directional_test": (
            reocc_test
        ),
        "reoccupation_sei": profile[
            "sei_reoccupation_per_loss"
        ],

        "low_minus_high_first_occupations_per_1000_evals": (
            first_summary
        ),
        "first_occupation_directional_test": (
            first_test
        ),
        "first_occupation_sei": profile[
            "sei_first_occupations_per_1000_evals"
        ],

        "status": "MEASURED",

        "_high_runs": high_runs,
        "_neutral_runs": neutral_runs,
        "_low_runs": low_runs,
    }

    reporter.json(
        "stage-03-policy-tradeoff.json",
        result,
    )
    reporter.stage(
        "stage-03-policy-tradeoff.md",
        "Stage 3 — At Equal Budget, What Gets Built?",
        result,
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    labels = [
        "high_support",
        "neutral",
        "low_support",
    ]
    reocc = [
        policy_summary[x][
            "mean_reoccupation_per_loss"
        ]
        for x in labels
    ]
    first = [
        policy_summary[x][
            "mean_first_occupations_per_1000_evals"
        ]
        for x in labels
    ]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )
    ax.bar(
        x - width / 2,
        reocc,
        width,
        label="reoccupation / loss",
    )
    ax.bar(
        x + width / 2,
        np.asarray(first) / 1000.0,
        width,
        label="first occupation / evaluation",
    )
    ax.set_xticks(
        x,
        labels,
        rotation=15,
    )
    ax.set_ylabel(
        "Normalized construction outcome"
    )
    ax.set_title(
        "Chapter 21: same budget, different local scheduling"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir
        / "ch21-02-fixed-budget-policy-tradeoff.png",
        dpi=160,
    )
    plt.close(fig)

    return result


# ============================================================================
# Stage 4 — verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage3: dict,
) -> dict:
    reocc = stage3[
        "high_minus_low_reoccupation_per_loss"
    ]
    first = stage3[
        "low_minus_high_first_occupations_per_1000_evals"
    ]

    reocc_ok = (
        stage3[
            "reoccupation_directional_test"
        ]["p_value"]
        < profile["alpha"]
        and reocc["mean"]
        >= profile[
            "sei_reoccupation_per_loss"
        ]
    )

    first_ok = (
        stage3[
            "first_occupation_directional_test"
        ]["p_value"]
        < profile["alpha"]
        and first["mean"]
        >= profile[
            "sei_first_occupations_per_1000_evals"
        ]
    )

    supported = (
        reocc_ok and first_ok
    )

    if supported:
        status = "SUPPORTED"
        bounded = (
            "With candidate-evaluation budget held fixed, local geometric "
            "scheduling produced the predeclared tradeoff: prioritizing "
            "higher-support frontier sites increased reuse of lost material, "
            "while prioritizing lower-support frontier sites increased first "
            "occupation of new sites. This establishes a construction-"
            "allocation tradeoff under computational scarcity in the tested "
            "Digital Crystal protocol."
        )
    else:
        status = "FAILED"
        bounded = (
            "Chapter 21 V1 did not establish both predeclared arms of the "
            "construction-allocation tradeoff under the fixed finite "
            "evaluation budget."
        )

    result = {
        "question": (
            "When attachment evaluations are scarce, does local scheduling "
            "change the tradeoff between reusing lost material and occupying "
            "new sites?"
        ),

        "reoccupation_gate_passed": (
            reocc_ok
        ),
        "reoccupation_advantage": (
            reocc["mean"]
        ),
        "reoccupation_ci95": [
            reocc["ci95_low"],
            reocc["ci95_high"],
        ],
        "reoccupation_p_value": (
            stage3[
                "reoccupation_directional_test"
            ]["p_value"]
        ),
        "reoccupation_sei": profile[
            "sei_reoccupation_per_loss"
        ],

        "first_occupation_gate_passed": (
            first_ok
        ),
        "first_occupation_advantage_per_1000_evals": (
            first["mean"]
        ),
        "first_occupation_ci95": [
            first["ci95_low"],
            first["ci95_high"],
        ],
        "first_occupation_p_value": (
            stage3[
                "first_occupation_directional_test"
            ]["p_value"]
        ),
        "first_occupation_sei": profile[
            "sei_first_occupations_per_1000_evals"
        ],

        "status": status,
        "bounded_claim": bounded,

        "forbidden_overclaims": [
            "maintenance",
            "homeostasis",
            "metabolism",
            "energy",
            "repair",
            "adaptation",
            "agency",
            "choice",
            "organism",
            "life",
        ],

        "next_question_if_supported": (
            "Can a local rule allocate scarce construction opportunity in a "
            "way that preserves a bounded process without an externally "
            "selected scheduling policy?"
        ),
        "next_question_if_failed": (
            "Do not tune B or the neighbour-count thresholds to force a "
            "tradeoff. Use the budget sweep to determine whether candidate "
            "evaluation scarcity itself is the wrong resource abstraction."
        ),
    }

    reporter.json(
        "stage-04-verdict.json",
        result,
    )
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 21 Verdict",
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
        choices=sorted(PROFILES),
        default="quick",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260828,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch21-finite-update-budget-v1"
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
        PROFILES[args.profile]
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
            "FINITE CONSTRUCTION-EVALUATION BUDGET"
        ),
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,

        "canonical_attachment_probability_modified": False,
        "new_constraint": (
            "At most B frontier candidates receive canonical attachment "
            "evaluation per update."
        ),
        "loss_process": (
            "Uniform keyed background loss after growth at frozen delta."
        ),
        "scientific_boundary": (
            "Allocation under computational scarcity only. No maintenance, "
            "homeostasis, metabolism, energy, repair, adaptation, agency, "
            "organism, or life claim."
        ),
        "started_at_unix": (
            time.time()
        ),
    }

    print("=" * 78)
    print(
        "CHAPTER 21 — WHAT DOES IT COST TO STAY?"
    )
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"budget={profile['primary_budget']} "
        f"loss={profile['loss_rate']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )

    s1 = stage_1_unlimited_reference(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )

    s2 = stage_2_budget_sweep(
        reporter,
        profile,
        crystal_params,
        args.seed,
        args.image_dir,
    )

    s3 = stage_3_policy_tradeoff(
        reporter,
        profile,
        crystal_params,
        args.seed,
        args.image_dir,
    )

    s4 = stage_4_verdict(
        reporter,
        profile,
        s3,
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
            s4["bounded_claim"]
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
    print("CHAPTER 21 COMPLETE")
    print(
        f"protocol={s0['status']}"
    )
    print(
        f"unlimited_reference={s1['status']}"
    )
    print(
        f"budget_sweep={s2['status']}"
    )
    print(
        f"policy_tradeoff={s3['status']}"
    )
    print(
        f"FINAL={s4['status']}"
    )
    print(
        f"report={report_path}"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
