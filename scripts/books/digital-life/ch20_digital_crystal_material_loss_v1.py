#!/usr/bin/env python3
"""
Chapter 20 — What Happens When the Crystal Can Lose Material? (V1)

One new substrate rule
======================

    occupied
        |
        | background loss with probability delta
        v
      empty

Nothing else is added.

There is no:
    repair mechanism
    maintenance controller
    resource budget
    metabolism
    death state
    aging variable
    homeostasis target

The existing Digital Crystal growth rule remains frozen.

Scientific question
-------------------
Does adding background material loss turn irreversible monotone growth into a
finite dynamic regime where construction and loss can balance?

A second, controlled question asks whether WHERE loss occurs matters when the
number of loss events is held exactly equal:

    surface-biased loss
    vs
    interior-biased loss

The chapter deliberately distinguishes:

    ordinary regrowth into newly emptied sites
    !=
    an explicit repair mechanism

V1 is a characterization experiment.  A positive result earns only a bounded
claim about construction/loss balance and finite sustainable scale under this
specific substrate.

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
EXPERIMENT_VERSION = "digital-crystal-material-loss-v1"
SCHEMA_VERSION = 1
CHAPTER = 20
CHAPTER_TITLE = "What Happens When the Crystal Can Lose Material?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 24,
        "seed_noise_groups": 96,
        "radius": 72,
        "warmup_steps": 14,
        "continuation_steps": 48,
        "late_window": 12,

        # Frozen exploratory loss sweep.
        "loss_rates": [0.0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16],

        # A finite dynamic regime must have a late population slope whose
        # magnitude is <= 0.25% of late mean population per update.
        "bounded_normalized_slope_max": 0.0025,

        # Decay-off must still be clearly expanding to call a nonzero arm
        # "bounded relative to the irreversible baseline".
        "baseline_expanding_normalized_slope_min": 0.0040,

        # Avoid calling near-extinction or world-capacity saturation a balance.
        "minimum_sustainable_population": 100,
        "max_capacity_fraction": 0.75,

        # A bounded arm must be at least 25% smaller than decay-off over the
        # same late window to be scientifically interesting.
        "minimum_size_reduction_fraction": 0.25,

        # Exact-count placement control.
        "placement_groups": 32,
        "placement_steps": 32,
        "loss_budget_fraction_of_min_eligible": 0.10,
        "placement_sei_population_fraction": 0.10,

        "bootstrap_reps": 2000,
        "permutations": 4000,
        "alpha": 0.05,
    },
    "standard": {
        "groups": 48,
        "seed_noise_groups": 160,
        "radius": 80,
        "warmup_steps": 14,
        "continuation_steps": 64,
        "late_window": 16,
        "loss_rates": [0.0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16],
        "bounded_normalized_slope_max": 0.0025,
        "baseline_expanding_normalized_slope_min": 0.0040,
        "minimum_sustainable_population": 100,
        "max_capacity_fraction": 0.75,
        "minimum_size_reduction_fraction": 0.25,
        "placement_groups": 64,
        "placement_steps": 40,
        "loss_budget_fraction_of_min_eligible": 0.10,
        "placement_sei_population_fraction": 0.10,
        "bootstrap_reps": 4000,
        "permutations": 8000,
        "alpha": 0.05,
    },
    "full": {
        "groups": 96,
        "seed_noise_groups": 240,
        "radius": 96,
        "warmup_steps": 14,
        "continuation_steps": 80,
        "late_window": 20,
        "loss_rates": [0.0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16],
        "bounded_normalized_slope_max": 0.0025,
        "baseline_expanding_normalized_slope_min": 0.0040,
        "minimum_sustainable_population": 100,
        "max_capacity_fraction": 0.75,
        "minimum_size_reduction_fraction": 0.25,
        "placement_groups": 96,
        "placement_steps": 48,
        "loss_budget_fraction_of_min_eligible": 0.10,
        "placement_sei_population_fraction": 0.10,
        "bootstrap_reps": 6000,
        "permutations": 12000,
        "alpha": 0.05,
    },
}


# ============================================================================
# State helpers
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


def boundary_and_interior(
    occupied: Set[Cell],
) -> Tuple[List[Cell], List[Cell]]:
    surface: List[Cell] = []
    interior: List[Cell] = []

    for cell in sorted(occupied):
        degree = sum(
            nb in occupied
            for nb in ch18.neighbors(cell)
        )
        if degree < 6:
            surface.append(cell)
        else:
            interior.append(cell)

    return surface, interior


def hole_count(occupied: Set[Cell]) -> int:
    """
    Count empty cells completely surrounded by occupied neighbours.

    This is a local morphology diagnostic, not a claim about damage or repair.
    """
    candidates: Set[Cell] = set()
    for cell in occupied:
        for nb in ch18.neighbors(cell):
            if nb not in occupied:
                candidates.add(nb)

    return sum(
        all(nb in occupied for nb in ch18.neighbors(cell))
        for cell in candidates
    )


# ============================================================================
# Independent keyed material-loss RNG
# ============================================================================

def loss_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    payload = (
        f"{stream_seed}|{step}|{cell[0]}|{cell[1]}|material-loss-v1"
    ).encode("utf-8")
    digest = hashlib.blake2b(
        payload,
        digest_size=8,
    ).digest()
    value = int.from_bytes(digest, "big")
    return value / float(2**64)


# ============================================================================
# Loss dynamics
# ============================================================================

def apply_probability_loss(
    state: ch18.MaterialCrystalState,
    loss_rate: float,
    policy: str = "uniform",
) -> Tuple[ch18.MaterialCrystalState, int]:
    """
    Apply loss AFTER the canonical growth update.

    Any emptied location can therefore be encountered by ordinary crystal
    growth on a later update.  No explicit repair operator exists.
    """
    occupied_before = set(state.occupied)

    surface, interior = boundary_and_interior(occupied_before)

    if policy == "uniform":
        eligible = sorted(occupied_before)
    elif policy == "surface":
        eligible = surface
    elif policy == "interior":
        eligible = interior
    else:
        raise ValueError(policy)

    lost = [
        cell
        for cell in eligible
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

    return out, len(lost)


def choose_exact_loss_targets(
    eligible: Sequence[Cell],
    stream_seed: int,
    step: int,
    budget: int,
) -> List[Cell]:
    if budget < 0 or budget > len(eligible):
        raise ValueError(
            f"Invalid loss budget={budget}, eligible={len(eligible)}"
        )

    return sorted(
        eligible,
        key=lambda cell: (
            loss_uniform(stream_seed, step, cell),
            cell,
        ),
    )[:budget]


def apply_exact_loss_targets(
    state: ch18.MaterialCrystalState,
    targets: Sequence[Cell],
) -> ch18.MaterialCrystalState:
    out = clone_state(state)

    for cell in targets:
        out.occupied.discard(cell)
        out.birth_time.pop(cell, None)

    if out.population_by_step:
        out.population_by_step[-1] = len(out.occupied)

    return out


def growth_then_probability_loss(
    state: ch18.MaterialCrystalState,
    input_value: float,
    loss_rate: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    policy: str = "uniform",
) -> Tuple[ch18.MaterialCrystalState, int, int]:
    grown, additions, _ = ch18.grow_one_step_without_transmission(
        state,
        input_value,
        0,
        radius,
        crystal_params,
        no_material_params(),
    )

    out, losses = apply_probability_loss(
        grown,
        loss_rate,
        policy,
    )
    return out, len(additions), losses


# ============================================================================
# One decay-sweep run
# ============================================================================

def run_loss_rate(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
    loss_rate: float,
) -> dict:
    warmup = profile["warmup_steps"]
    horizon = profile["continuation_steps"]
    radius = profile["radius"]

    gseed = seed + group_index * 1009
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

    populations = []
    attachments = []
    losses = []
    nets = []
    boundaries = []
    holes = []
    capacity = []

    for j in range(horizon):
        state, a, l = growth_then_probability_loss(
            state,
            float(env[warmup + j]),
            loss_rate,
            radius,
            crystal_params,
            "uniform",
        )

        surf, _ = boundary_and_interior(state.occupied)

        populations.append(len(state.occupied))
        attachments.append(a)
        losses.append(l)
        nets.append(a - l)
        boundaries.append(len(surf))
        holes.append(hole_count(state.occupied))
        capacity.append(
            ch18.capacity_fraction_occupied(
                state.occupied,
                radius,
            )
        )

        if not state.occupied:
            # Once the crystal is empty the frozen local growth rule has no
            # occupied neighbour from which growth can restart.
            remaining = horizon - j - 1
            populations.extend([0] * remaining)
            attachments.extend([0] * remaining)
            losses.extend([0] * remaining)
            nets.extend([0] * remaining)
            boundaries.extend([0] * remaining)
            holes.extend([0] * remaining)
            capacity.extend([0.0] * remaining)
            break

    late = profile["late_window"]
    y = np.asarray(populations[-late:], dtype=float)
    x = np.arange(len(y), dtype=float)

    if len(y) >= 2 and np.mean(y) > 0:
        slope = float(np.polyfit(x, y, 1)[0])
        normalized_slope = slope / float(np.mean(y))
    else:
        slope = 0.0
        normalized_slope = 0.0

    return {
        "loss_rate": float(loss_rate),
        "final_population": int(populations[-1]),
        "late_mean_population": float(np.mean(populations[-late:])),
        "late_population_slope": slope,
        "late_normalized_population_slope": normalized_slope,
        "late_mean_attachments": float(np.mean(attachments[-late:])),
        "late_mean_losses": float(np.mean(losses[-late:])),
        "late_mean_net": float(np.mean(nets[-late:])),
        "late_mean_boundary": float(np.mean(boundaries[-late:])),
        "late_mean_holes": float(np.mean(holes[-late:])),
        "max_capacity_fraction": float(max(capacity)),
        "collapsed": bool(populations[-1] == 0),
        "population_trajectory": populations,
        "attachment_trajectory": attachments,
        "loss_trajectory": losses,
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
        boot[i] = np.mean(
            rng.choice(arr, size=len(arr), replace=True)
        )

    return {
        "n": len(arr),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "ci95_low": float(np.quantile(boot, 0.025)),
        "ci95_high": float(np.quantile(boot, 0.975)),
    }


def signflip_greater(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    arr = np.asarray(values, dtype=float)
    observed = float(np.mean(arr))

    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        signs = rng.choice(
            np.asarray([-1.0, 1.0]),
            size=len(arr),
        )
        null[i] = np.mean(arr * signs)

    p = (
        1.0 + float(np.sum(null >= observed))
    ) / (permutations + 1.0)

    return {
        "observed_mean": observed,
        "p_value": p,
        "permutations": permutations,
        "alternative": "greater",
    }


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections = []

    def json(self, filename: str, payload: dict) -> None:
        clean = {
            k: v
            for k, v in payload.items()
            if not k.startswith("_")
        }
        (self.root / filename).write_text(
            json.dumps(clean, indent=2),
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
            + json.dumps(clean, indent=2)
            + "\n```"
        )
        (self.root / filename).write_text(
            f"# {title}\n\n{body}\n",
            encoding="utf-8",
        )
        self.sections.append((title, body))

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch20-material-loss-v1-full-report.md"

        parts = [
            "# Chapter 20 — What Happens When the Crystal Can Lose Material?",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(metadata, indent=2),
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
        "role": "MATERIAL-LOSS CHARACTERIZATION",
        "new_substrate_rule": (
            "After each ordinary growth update, eligible occupied cells are "
            "removed independently with probability delta."
        ),
        "question": (
            "Does background material loss create a finite dynamic regime "
            "where ordinary construction no longer yields irreversible "
            "monotone expansion?"
        ),
        "candidate_scaling_argument": (
            "If construction opportunity is dominated by a boundary-like set "
            "while uniform loss acts throughout occupied material, increasing "
            "size should eventually increase expected loss faster than "
            "construction. This is a hypothesis, not assumed truth."
        ),
        "primary_loss_sweep": profile["loss_rates"],
        "bounded_regime_definition": {
            "abs_late_normalized_population_slope_max": profile[
                "bounded_normalized_slope_max"
            ],
            "minimum_late_population": profile[
                "minimum_sustainable_population"
            ],
            "maximum_capacity_fraction": profile[
                "max_capacity_fraction"
            ],
            "minimum_size_reduction_vs_decay_off": profile[
                "minimum_size_reduction_fraction"
            ],
        },
        "baseline_requirement": {
            "decay_off_normalized_slope_min": profile[
                "baseline_expanding_normalized_slope_min"
            ]
        },
        "secondary_exact_count_test": (
            "Compare surface-biased versus interior-biased loss while holding "
            "the number of removed cells exactly equal each step."
        ),
        "forbidden_overclaims": [
            "death",
            "aging",
            "repair",
            "homeostasis",
            "metabolism",
            "energy",
            "organism",
            "life",
        ],
        "status": "MEASURED",
    }

    reporter.json("stage-00-protocol.json", result)
    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Freeze the Material-Loss Question",
        result,
    )
    return result


# ============================================================================
# Stage 1 — seed-noise baseline
# ============================================================================

def stage_1_seed_noise(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    final_population = []
    late_slope = []
    late_net = []

    for g in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 decay-off seed noise",
    ):
        r = run_loss_rate(
            profile,
            crystal_params,
            seed + 1_000_000,
            g,
            0.0,
        )
        final_population.append(r["final_population"])
        late_slope.append(r["late_normalized_population_slope"])
        late_net.append(r["late_mean_net"])

    result = {
        "role": "DECAY-OFF SEED-NOISE BASELINE",
        "groups": profile["seed_noise_groups"],
        "final_population": {
            "mean": float(np.mean(final_population)),
            "std": float(np.std(final_population, ddof=1)),
            "q05": float(np.quantile(final_population, 0.05)),
            "q95": float(np.quantile(final_population, 0.95)),
        },
        "late_normalized_population_slope": {
            "mean": float(np.mean(late_slope)),
            "std": float(np.std(late_slope, ddof=1)),
            "q05": float(np.quantile(late_slope, 0.05)),
            "q95": float(np.quantile(late_slope, 0.95)),
        },
        "late_mean_net_growth": {
            "mean": float(np.mean(late_net)),
            "std": float(np.std(late_net, ddof=1)),
        },
        "status": "MEASURED",
    }

    reporter.json("stage-01-seed-noise.json", result)
    reporter.stage(
        "stage-01-seed-noise.md",
        "Stage 1 — Measure the Irreversible Baseline",
        result,
    )
    return result


# ============================================================================
# Stage 2 — loss sweep
# ============================================================================

def classify_rate(
    profile: dict,
    rate_summary: dict,
    baseline_mean_population: float,
) -> dict:
    bounded = (
        abs(rate_summary["late_normalized_population_slope"]["mean"])
        <= profile["bounded_normalized_slope_max"]
    )

    sustainable = (
        rate_summary["late_mean_population"]["mean"]
        >= profile["minimum_sustainable_population"]
    )

    unsaturated = (
        rate_summary["max_capacity_fraction"]["mean"]
        < profile["max_capacity_fraction"]
    )

    reduction = 1.0 - (
        rate_summary["late_mean_population"]["mean"]
        / max(1.0, baseline_mean_population)
    )

    meaningful_reduction = (
        reduction >= profile["minimum_size_reduction_fraction"]
    )

    return {
        "bounded_slope": bounded,
        "sustainable_population": sustainable,
        "unsaturated": unsaturated,
        "size_reduction_fraction_vs_decay_off": reduction,
        "meaningful_size_reduction": meaningful_reduction,
        "qualifies_as_finite_dynamic_regime": bool(
            bounded
            and sustainable
            and unsaturated
            and meaningful_reduction
        ),
    }


def stage_2_loss_sweep(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    by_rate = {}
    trajectory_means = {}

    raw_by_rate = {}

    for rate_i, rate in enumerate(profile["loss_rates"]):
        runs = []

        for g in tqdm(
            range(profile["groups"]),
            desc=f"Stage 2 loss delta={rate:.3f}",
        ):
            runs.append(
                run_loss_rate(
                    profile,
                    crystal_params,
                    seed + 2_000_000 + rate_i * 100_000,
                    g,
                    rate,
                )
            )

        raw_by_rate[rate] = runs

        def summary(field):
            vals = [r[field] for r in runs]
            return bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 2_500_000 + rate_i * 1000,
            )

        rate_summary = {
            "loss_rate": rate,
            "late_mean_population": summary("late_mean_population"),
            "final_population": summary("final_population"),
            "late_normalized_population_slope": summary(
                "late_normalized_population_slope"
            ),
            "late_mean_attachments": summary("late_mean_attachments"),
            "late_mean_losses": summary("late_mean_losses"),
            "late_mean_net": summary("late_mean_net"),
            "late_mean_boundary": summary("late_mean_boundary"),
            "late_mean_holes": summary("late_mean_holes"),
            "max_capacity_fraction": summary("max_capacity_fraction"),
            "collapsed_fraction": float(np.mean([
                r["collapsed"] for r in runs
            ])),
        }

        by_rate[str(rate)] = rate_summary

        trajectory_means[str(rate)] = list(np.mean(
            np.asarray([
                r["population_trajectory"] for r in runs
            ], dtype=float),
            axis=0,
        ))

    baseline_pop = by_rate["0.0"]["late_mean_population"]["mean"]

    classifications = {}
    for rate in profile["loss_rates"]:
        classifications[str(rate)] = classify_rate(
            profile,
            by_rate[str(rate)],
            baseline_pop,
        )

    result = {
        "groups_per_rate": profile["groups"],
        "loss_rates": profile["loss_rates"],
        "by_rate": by_rate,
        "classifications": classifications,
        "qualifying_nonzero_rates": [
            rate
            for rate in profile["loss_rates"]
            if rate > 0
            and classifications[str(rate)][
                "qualifies_as_finite_dynamic_regime"
            ]
        ],
        "status": "MEASURED",
        "_trajectory_means": trajectory_means,
    }

    reporter.json("stage-02-loss-sweep.json", result)
    reporter.stage(
        "stage-02-loss-sweep.md",
        "Stage 2 — Sweep Background Material Loss",
        result,
    )

    image_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    xs = np.arange(1, profile["continuation_steps"] + 1)

    for rate in profile["loss_rates"]:
        ax.plot(
            xs,
            trajectory_means[str(rate)],
            label=f"δ={rate:g}",
        )

    ax.set_xlabel("Continuation update")
    ax.set_ylabel("Mean occupied cells")
    ax.set_title("Chapter 20: growth under background material loss")
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch20-01-material-loss-sweep.png",
        dpi=160,
    )
    plt.close(fig)

    return result


# ============================================================================
# Stage 3 — exact matched loss placement
# ============================================================================

def run_exact_placement_pair(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
) -> dict:
    warmup = profile["warmup_steps"]
    horizon = profile["placement_steps"]
    radius = profile["radius"]

    gseed = seed + group_index * 1013
    env = ch18.make_environment(
        warmup + horizon + 8,
        gseed + 1,
    )

    base = ch18.warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        no_material_params(),
    )

    surface_state = clone_state(base)
    interior_state = clone_state(base)

    budgets = []
    surface_pop = []
    interior_pop = []
    surface_holes = []
    interior_holes = []

    for j in range(horizon):
        forcing = float(env[warmup + j])

        s_grown, _, _ = ch18.grow_one_step_without_transmission(
            surface_state,
            forcing,
            0,
            radius,
            crystal_params,
            no_material_params(),
        )
        i_grown, _, _ = ch18.grow_one_step_without_transmission(
            interior_state,
            forcing,
            0,
            radius,
            crystal_params,
            no_material_params(),
        )

        s_surface, _ = boundary_and_interior(s_grown.occupied)
        _, i_interior = boundary_and_interior(i_grown.occupied)

        base_eligible = min(
            len(s_surface),
            len(i_interior),
        )
        k = int(round(
            profile["loss_budget_fraction_of_min_eligible"]
            * base_eligible
        ))
        k = max(0, min(base_eligible, k))

        s_targets = choose_exact_loss_targets(
            s_surface,
            s_grown.stream_seed,
            s_grown.step,
            k,
        )
        i_targets = choose_exact_loss_targets(
            i_interior,
            i_grown.stream_seed,
            i_grown.step,
            k,
        )

        surface_state = apply_exact_loss_targets(
            s_grown,
            s_targets,
        )
        interior_state = apply_exact_loss_targets(
            i_grown,
            i_targets,
        )

        if len(s_targets) != len(i_targets):
            raise RuntimeError(
                "Exact placement-loss budget mismatch."
            )

        budgets.append(k)
        surface_pop.append(len(surface_state.occupied))
        interior_pop.append(len(interior_state.occupied))
        surface_holes.append(hole_count(surface_state.occupied))
        interior_holes.append(hole_count(interior_state.occupied))

    denom = max(
        1.0,
        0.5 * (
            np.mean(surface_pop[-profile["late_window"]:])
            + np.mean(interior_pop[-profile["late_window"]:])
        ),
    )

    late_pop_diff_norm = (
        np.mean(interior_pop[-profile["late_window"]:])
        - np.mean(surface_pop[-profile["late_window"]:])
    ) / denom

    return {
        "exact_budget_all_steps": True,
        "cumulative_losses_surface": int(sum(budgets)),
        "cumulative_losses_interior": int(sum(budgets)),
        "late_mean_population_surface": float(np.mean(
            surface_pop[-profile["late_window"]:]
        )),
        "late_mean_population_interior": float(np.mean(
            interior_pop[-profile["late_window"]:]
        )),
        "late_population_advantage_interior_minus_surface_norm": float(
            late_pop_diff_norm
        ),
        "late_mean_holes_surface": float(np.mean(
            surface_holes[-profile["late_window"]:]
        )),
        "late_mean_holes_interior": float(np.mean(
            interior_holes[-profile["late_window"]:]
        )),
    }


def stage_3_loss_placement(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    runs = []

    for g in tqdm(
        range(profile["placement_groups"]),
        desc="Stage 3 exact loss placement",
    ):
        runs.append(
            run_exact_placement_pair(
                profile,
                crystal_params,
                seed + 3_000_000,
                g,
            )
        )

    effects = [
        r[
            "late_population_advantage_interior_minus_surface_norm"
        ]
        for r in runs
    ]

    summary = bootstrap_mean_ci(
        effects,
        profile["bootstrap_reps"],
        seed + 3_500_000,
    )
    test = signflip_greater(
        effects,
        profile["permutations"],
        seed + 3_600_000,
    )

    result = {
        "role": "EXACT-COUNT LOSS-PLACEMENT CONTROL",
        "groups": profile["placement_groups"],
        "all_loss_budgets_exactly_matched": bool(all(
            r["cumulative_losses_surface"]
            == r["cumulative_losses_interior"]
            for r in runs
        )),
        "mean_cumulative_losses_each_policy": float(np.mean([
            r["cumulative_losses_surface"]
            for r in runs
        ])),
        "late_population_advantage_interior_minus_surface": summary,
        "directional_test": test,
        "predeclared_sei_population_fraction": profile[
            "placement_sei_population_fraction"
        ],
        "mean_late_holes_surface": float(np.mean([
            r["late_mean_holes_surface"] for r in runs
        ])),
        "mean_late_holes_interior": float(np.mean([
            r["late_mean_holes_interior"] for r in runs
        ])),
        "status": "MEASURED",
    }

    reporter.json("stage-03-loss-placement.json", result)
    reporter.stage(
        "stage-03-loss-placement.md",
        "Stage 3 — Does the Location of Equal Loss Matter?",
        result,
    )
    return result


# ============================================================================
# Stage 4 — bounded verdict
# ============================================================================

def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    baseline_slope = stage1[
        "late_normalized_population_slope"
    ]["mean"]

    baseline_expanding = (
        baseline_slope
        >= profile["baseline_expanding_normalized_slope_min"]
    )

    qualifying = stage2["qualifying_nonzero_rates"]

    finite_regime_supported = (
        baseline_expanding
        and len(qualifying) >= 1
    )

    placement = stage3[
        "late_population_advantage_interior_minus_surface"
    ]
    placement_effect = placement["mean"]

    placement_supported = (
        stage3["all_loss_budgets_exactly_matched"]
        and stage3["directional_test"]["p_value"] < profile["alpha"]
        and placement_effect >= profile[
            "placement_sei_population_fraction"
        ]
    )

    if finite_regime_supported:
        status = "SUPPORTED"
        bounded = (
            "Under this frozen Digital Crystal material-loss protocol, "
            "background loss produced at least one nonzero-loss regime whose "
            "late population was substantially smaller than the irreversible "
            "baseline and approximately stationary over the predeclared late "
            "window, without collapse or world-capacity saturation. This "
            "supports a finite dynamic construction/loss regime under the "
            "tested conditions."
        )
    else:
        status = "FAILED"
        bounded = (
            "Chapter 20 V1 did not establish a finite dynamic "
            "construction/loss regime under the frozen loss sweep and "
            "predeclared late-window criteria."
        )

    result = {
        "question": (
            "Does background material loss create a finite dynamic regime "
            "rather than irreversible monotone expansion?"
        ),
        "decay_off_baseline_expanding": baseline_expanding,
        "decay_off_mean_normalized_slope": baseline_slope,
        "qualifying_nonzero_loss_rates": qualifying,
        "finite_dynamic_regime_supported": finite_regime_supported,
        "exact_count_loss_location_test": {
            "supported_at_predeclared_SEI": placement_supported,
            "mean_interior_minus_surface_population_advantage_norm": (
                placement_effect
            ),
            "p_value": stage3["directional_test"]["p_value"],
            "sei": profile["placement_sei_population_fraction"],
        },
        "status": status,
        "bounded_claim": bounded,
        "forbidden_overclaims": [
            "death",
            "aging",
            "repair",
            "homeostasis",
            "metabolism",
            "energy",
            "organism",
            "life",
        ],
        "next_question_if_supported": (
            "What computational budget is required to remain in the "
            "construction/loss regime, and how does sustainable size scale "
            "with that budget?"
        ),
        "next_question_if_failed": (
            "Do not tune loss rates to force a plateau. Diagnose whether the "
            "finite observation window, geometry, or construction law makes "
            "the perimeter/occupied-material scaling hypothesis inapplicable."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 20 Verdict",
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
        default=20260826,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch20-material-loss-v1"
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

    profile = dict(PROFILES[args.profile])
    crystal_params = ch18.CrystalParams()

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "run_type": "MATERIAL-LOSS CHARACTERIZATION",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_growth_rule_modified": False,
        "new_substrate_rule": (
            "Post-growth occupied-cell removal with independent keyed "
            "probability delta."
        ),
        "scientific_boundary": (
            "Construction/loss dynamics only. No death, aging, repair, "
            "homeostasis, metabolism, energy, organism, or life claim."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 20 — WHAT HAPPENS WHEN THE CRYSTAL CAN LOSE MATERIAL?")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )
    s1 = stage_1_seed_noise(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )
    s2 = stage_2_loss_sweep(
        reporter,
        profile,
        crystal_params,
        args.seed,
        args.image_dir,
    )
    s3 = stage_3_loss_placement(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )
    s4 = stage_4_verdict(
        reporter,
        profile,
        s1,
        s2,
        s3,
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_0_status": s0["status"],
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "final_status": s4["status"],
        "bounded_claim": s4["bounded_claim"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print()
    print("=" * 78)
    print("CHAPTER 20 COMPLETE")
    print(f"protocol={s0['status']}")
    print(f"baseline={s1['status']}")
    print(f"loss_sweep={s2['status']}")
    print(f"placement_control={s3['status']}")
    print(f"FINAL={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
