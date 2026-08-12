#!/usr/bin/env python3
"""
Chapter 20 — What Happens When the Crystal Can Lose Material? (V2)

Mechanism autopsy
=================

V1 FAILED to establish a finite, near-stationary construction/loss regime.

But V1 revealed a stronger mechanistic clue:

    more loss
    -> much more attachment

and with exact matched loss quantity:

    interior-biased loss
    -> substantially larger late population
    -> many more enclosed holes

V2 does NOT rescue the V1 plateau hypothesis.

Instead it asks one new question:

    When material is removed, how much later construction is
    genuinely new occupation and how much is reoccupation of
    previously occupied material?

We explicitly distinguish:

    FIRST OCCUPATION
        a cell becomes occupied for the first time ever

    REOCCUPATION
        a cell was previously occupied, was lost, and later becomes occupied again

No explicit repair mechanism is added.

Scientific question
-------------------
Does material loss itself create attachment opportunities that are subsequently
used by the ordinary frozen Digital Crystal growth rule?

Primary exact-count comparison
------------------------------
Surface-biased and interior-biased loss remove exactly the same number of cells
per update.

Primary outcome:
    cumulative reoccupations per cumulative loss

Prediction:
    interior loss > surface loss

Secondary outcomes:
    fraction of lost sites ever reoccupied
    median time-to-reoccupation
    new frontier opportunities created per loss
    first-occupation count
    late population
    enclosed holes

This does not establish:
    repair
    regeneration
    maintenance
    homeostasis
    metabolism
    death
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
from typing import Dict, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-material-loss-v2"
SCHEMA_VERSION = 2
CHAPTER = 20
CHAPTER_TITLE = "What Happens When the Crystal Can Lose Material?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 48,
        "seed_noise_groups": 96,
        "radius": 72,
        "warmup_steps": 14,
        "continuation_steps": 40,

        # Exact matched-loss placement protocol.
        "loss_budget_fraction_of_min_eligible": 0.10,

        # Primary SEI:
        # interior must increase reoccupations/loss by >= 0.15 absolute.
        "primary_sei_reoccupation_per_loss": 0.15,

        # Secondary SEI:
        # at least 15 percentage-point increase in fraction of lost sites
        # that are subsequently reoccupied.
        "secondary_sei_reoccupied_lost_site_fraction": 0.15,

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
        "continuation_steps": 52,
        "loss_budget_fraction_of_min_eligible": 0.10,
        "primary_sei_reoccupation_per_loss": 0.15,
        "secondary_sei_reoccupied_lost_site_fraction": 0.15,
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
        "continuation_steps": 64,
        "loss_budget_fraction_of_min_eligible": 0.10,
        "primary_sei_reoccupation_per_loss": 0.15,
        "secondary_sei_reoccupied_lost_site_fraction": 0.15,
        "bootstrap_reps": 6000,
        "permutations": 12000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.75,
    },
}


# ============================================================================
# State / geometry helpers
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
    surface = []
    interior = []

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


def frontier_cells(
    occupied: Set[Cell],
    radius: int,
) -> Set[Cell]:
    frontier = set()

    for cell in occupied:
        for nb in ch18.neighbors(cell):
            if (
                nb not in occupied
                and ch18.hex_distance(nb) <= radius
            ):
                frontier.add(nb)

    return frontier


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
# Loss RNG / exact loss
# ============================================================================

def loss_uniform(
    stream_seed: int,
    step: int,
    cell: Cell,
) -> float:
    payload = (
        f"{stream_seed}|{step}|{cell[0]}|{cell[1]}|material-loss-v2"
    ).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def choose_exact_loss_targets(
    eligible: Sequence[Cell],
    stream_seed: int,
    step: int,
    budget: int,
) -> List[Cell]:
    if budget < 0 or budget > len(eligible):
        raise ValueError(
            f"Invalid budget={budget}, eligible={len(eligible)}"
        )

    return sorted(
        eligible,
        key=lambda c: (
            loss_uniform(stream_seed, step, c),
            c,
        ),
    )[:budget]


def apply_exact_loss(
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


# ============================================================================
# Occupancy history ledger
# ============================================================================

class OccupancyLedger:
    """
    Observer-only history of site occupancy.

    This does NOT feed back into crystal dynamics.
    """

    def __init__(self, initially_occupied: Set[Cell]):
        self.ever_occupied: Set[Cell] = set(initially_occupied)
        self.currently_lost: Set[Cell] = set()

        self.loss_count = 0
        self.first_occupation_count = 0
        self.reoccupation_count = 0

        self.loss_times_by_cell: Dict[Cell, List[int]] = defaultdict(list)
        self.reoccupation_delays: List[int] = []

        # Track whether a lost site has ever been reoccupied at least once.
        self.lost_sites: Set[Cell] = set()
        self.reoccupied_lost_sites: Set[Cell] = set()

    def register_losses(
        self,
        cells: Sequence[Cell],
        step: int,
    ) -> None:
        for cell in cells:
            self.loss_count += 1
            self.currently_lost.add(cell)
            self.lost_sites.add(cell)
            self.loss_times_by_cell[cell].append(step)

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
                self.reoccupied_lost_sites.add(cell)

                if self.loss_times_by_cell[cell]:
                    delay = step - self.loss_times_by_cell[cell][-1]
                    self.reoccupation_delays.append(delay)

                self.currently_lost.discard(cell)

            elif cell not in self.ever_occupied:
                first += 1
                self.first_occupation_count += 1

            # If the cell was occupied before but isn't in currently_lost,
            # this should not normally occur because it is already occupied.
            self.ever_occupied.add(cell)

        return first, reoccupied

    def summary(self) -> dict:
        return {
            "loss_count": int(self.loss_count),
            "first_occupation_count": int(self.first_occupation_count),
            "reoccupation_count": int(self.reoccupation_count),
            "reoccupation_per_loss": (
                float(self.reoccupation_count / self.loss_count)
                if self.loss_count else 0.0
            ),
            "unique_lost_sites": int(len(self.lost_sites)),
            "unique_reoccupied_lost_sites": int(
                len(self.reoccupied_lost_sites)
            ),
            "lost_site_reoccupied_fraction": (
                float(
                    len(self.reoccupied_lost_sites)
                    / len(self.lost_sites)
                )
                if self.lost_sites else 0.0
            ),
            "median_reoccupation_delay": (
                float(np.median(self.reoccupation_delays))
                if self.reoccupation_delays
                else None
            ),
            "mean_reoccupation_delay": (
                float(np.mean(self.reoccupation_delays))
                if self.reoccupation_delays
                else None
            ),
        }


# ============================================================================
# One synchronized exact-count pair
# ============================================================================

def run_exact_pair(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    group_index: int,
) -> dict:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    horizon = profile["continuation_steps"]

    gseed = seed + group_index * 1009
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

    surface_ledger = OccupancyLedger(set(base.occupied))
    interior_ledger = OccupancyLedger(set(base.occupied))

    cumulative_budget = 0

    per_step = {
        "surface": {
            "population": [],
            "first": [],
            "reoccupation": [],
            "losses": [],
            "frontier_before_loss": [],
            "frontier_after_loss": [],
            "new_frontier_from_loss": [],
            "holes": [],
        },
        "interior": {
            "population": [],
            "first": [],
            "reoccupation": [],
            "losses": [],
            "frontier_before_loss": [],
            "frontier_after_loss": [],
            "new_frontier_from_loss": [],
            "holes": [],
        },
    }

    for j in range(horizon):
        forcing = float(env[warmup + j])

        # -------- Surface branch growth --------
        s_grown, s_additions, _ = ch18.grow_one_step_without_transmission(
            surface_state,
            forcing,
            0,
            radius,
            crystal_params,
            no_material_params(),
        )
        s_first, s_reocc = surface_ledger.classify_additions(
            s_additions,
            s_grown.step,
        )

        # -------- Interior branch growth --------
        i_grown, i_additions, _ = ch18.grow_one_step_without_transmission(
            interior_state,
            forcing,
            0,
            radius,
            crystal_params,
            no_material_params(),
        )
        i_first, i_reocc = interior_ledger.classify_additions(
            i_additions,
            i_grown.step,
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

        if len(s_targets) != len(i_targets):
            raise RuntimeError(
                "Exact matched loss count failed."
            )

        s_frontier_before = frontier_cells(
            s_grown.occupied,
            radius,
        )
        i_frontier_before = frontier_cells(
            i_grown.occupied,
            radius,
        )

        surface_state = apply_exact_loss(
            s_grown,
            s_targets,
        )
        interior_state = apply_exact_loss(
            i_grown,
            i_targets,
        )

        surface_ledger.register_losses(
            s_targets,
            surface_state.step,
        )
        interior_ledger.register_losses(
            i_targets,
            interior_state.step,
        )

        s_frontier_after = frontier_cells(
            surface_state.occupied,
            radius,
        )
        i_frontier_after = frontier_cells(
            interior_state.occupied,
            radius,
        )

        s_new_frontier = len(
            s_frontier_after - s_frontier_before
        )
        i_new_frontier = len(
            i_frontier_after - i_frontier_before
        )

        cumulative_budget += k

        per_step["surface"]["population"].append(
            len(surface_state.occupied)
        )
        per_step["surface"]["first"].append(s_first)
        per_step["surface"]["reoccupation"].append(s_reocc)
        per_step["surface"]["losses"].append(k)
        per_step["surface"]["frontier_before_loss"].append(
            len(s_frontier_before)
        )
        per_step["surface"]["frontier_after_loss"].append(
            len(s_frontier_after)
        )
        per_step["surface"]["new_frontier_from_loss"].append(
            s_new_frontier
        )
        per_step["surface"]["holes"].append(
            hole_count(surface_state.occupied)
        )

        per_step["interior"]["population"].append(
            len(interior_state.occupied)
        )
        per_step["interior"]["first"].append(i_first)
        per_step["interior"]["reoccupation"].append(i_reocc)
        per_step["interior"]["losses"].append(k)
        per_step["interior"]["frontier_before_loss"].append(
            len(i_frontier_before)
        )
        per_step["interior"]["frontier_after_loss"].append(
            len(i_frontier_after)
        )
        per_step["interior"]["new_frontier_from_loss"].append(
            i_new_frontier
        )
        per_step["interior"]["holes"].append(
            hole_count(interior_state.occupied)
        )

        for st in (surface_state, interior_state):
            frac = ch18.capacity_fraction_occupied(
                st.occupied,
                radius,
            )
            if frac >= profile["max_capacity_fraction"]:
                raise RuntimeError(
                    f"Saturation guard: {frac:.3f}"
                )

    s_summary = surface_ledger.summary()
    i_summary = interior_ledger.summary()

    s_reocc_per_loss = s_summary["reoccupation_per_loss"]
    i_reocc_per_loss = i_summary["reoccupation_per_loss"]

    return {
        "exact_loss_count_match": True,
        "cumulative_loss_count_each": int(cumulative_budget),

        "surface": {
            **s_summary,
            "late_mean_population": float(np.mean(
                per_step["surface"]["population"][-10:]
            )),
            "mean_new_frontier_sites_per_loss": (
                float(
                    np.sum(per_step["surface"]["new_frontier_from_loss"])
                    / max(1, cumulative_budget)
                )
            ),
            "late_mean_holes": float(np.mean(
                per_step["surface"]["holes"][-10:]
            )),
        },

        "interior": {
            **i_summary,
            "late_mean_population": float(np.mean(
                per_step["interior"]["population"][-10:]
            )),
            "mean_new_frontier_sites_per_loss": (
                float(
                    np.sum(per_step["interior"]["new_frontier_from_loss"])
                    / max(1, cumulative_budget)
                )
            ),
            "late_mean_holes": float(np.mean(
                per_step["interior"]["holes"][-10:]
            )),
        },

        "primary_difference_interior_minus_surface": float(
            i_reocc_per_loss - s_reocc_per_loss
        ),

        "secondary_lost_site_reoccupied_fraction_difference": float(
            i_summary["lost_site_reoccupied_fraction"]
            - s_summary["lost_site_reoccupied_fraction"]
        ),

        "per_step": per_step,
    }


# ============================================================================
# Seed-noise control with no loss
# ============================================================================

def run_no_loss_baseline(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    """
    Establish that reoccupation is structurally zero when no sites are removed.
    Also characterizes ordinary first occupation.
    """
    first_counts = []
    final_pop = []

    for g in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 no-loss baseline",
    ):
        radius = profile["radius"]
        warmup = profile["warmup_steps"]
        horizon = profile["continuation_steps"]

        gseed = seed + 1_000_000 + g * 1013
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

        ledger = OccupancyLedger(set(state.occupied))

        for j in range(horizon):
            state, additions, _ = ch18.grow_one_step_without_transmission(
                state,
                float(env[warmup + j]),
                0,
                radius,
                crystal_params,
                no_material_params(),
            )
            ledger.classify_additions(
                additions,
                state.step,
            )

        summary = ledger.summary()

        if summary["reoccupation_count"] != 0:
            raise RuntimeError(
                "No-loss baseline generated a reoccupation unexpectedly."
            )

        first_counts.append(summary["first_occupation_count"])
        final_pop.append(len(state.occupied))

    return {
        "groups": profile["seed_noise_groups"],
        "reoccupation_count_all_groups": 0,
        "mean_first_occupations": float(np.mean(first_counts)),
        "std_first_occupations": float(np.std(first_counts, ddof=1)),
        "mean_final_population": float(np.mean(final_pop)),
        "std_final_population": float(np.std(final_pop, ddof=1)),
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
        null[i] = float(np.mean(arr * signs))

    p = (
        1.0 + float(np.sum(null >= observed))
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
        path = self.root / "ch20-material-loss-v2-full-report.md"
        parts = [
            "# Chapter 20 — What Happens When the Crystal Can Lose Material? (V2)",
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
# Stages
# ============================================================================

def stage_0_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": "LOSS-CREATED-CONSTRUCTION-OPPORTUNITY AUTOPSY",
        "v1_status": (
            "FAILED: no tested loss rate produced the predeclared finite "
            "near-stationary construction/loss regime."
        ),
        "new_question": (
            "When material is lost, how much subsequent attachment is "
            "first occupation and how much is reoccupation of previously "
            "occupied material?"
        ),
        "primary_comparison": (
            "Interior-biased versus surface-biased loss with exactly matched "
            "loss count every update."
        ),
        "primary_outcome": (
            "reoccupation_count / cumulative_loss_count, "
            "interior minus surface"
        ),
        "primary_sei": profile[
            "primary_sei_reoccupation_per_loss"
        ],
        "secondary_outcome": (
            "fraction of unique lost sites subsequently reoccupied, "
            "interior minus surface"
        ),
        "secondary_sei": profile[
            "secondary_sei_reoccupied_lost_site_fraction"
        ],
        "mechanism_chain": [
            "material loss",
            "new empty location",
            "changed frontier",
            "ordinary attachment opportunity",
            "reoccupation or first occupation",
        ],
        "observer_only_history_ledger": True,
        "forbidden_overclaims": [
            "repair",
            "regeneration",
            "maintenance",
            "homeostasis",
            "metabolism",
            "death",
            "aging",
            "organism",
            "life",
        ],
        "status": "MEASURED",
    }

    reporter.json("stage-00-protocol.json", result)
    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Freeze the V2 Mechanism Question",
        result,
    )
    return result


def stage_1_no_loss(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
) -> dict:
    result = run_no_loss_baseline(
        profile,
        crystal_params,
        seed,
    )
    result.update({
        "role": "NO-LOSS STRUCTURAL NULL",
        "interpretation": (
            "With no material removal, reoccupation must be zero by "
            "construction; all attachments are first occupations."
        ),
        "status": "MEASURED",
    })

    reporter.json("stage-01-no-loss.json", result)
    reporter.stage(
        "stage-01-no-loss.md",
        "Stage 1 — Verify the Reoccupation Null",
        result,
    )
    return result


def stage_2_exact_pair(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    seed: int,
    image_dir: Path,
) -> dict:
    runs = []

    for g in tqdm(
        range(profile["groups"]),
        desc="Stage 2 exact-count reoccupation test",
    ):
        runs.append(
            run_exact_pair(
                profile,
                crystal_params,
                seed + 2_000_000,
                g,
            )
        )

    primary = [
        r["primary_difference_interior_minus_surface"]
        for r in runs
    ]
    secondary = [
        r[
            "secondary_lost_site_reoccupied_fraction_difference"
        ]
        for r in runs
    ]

    primary_summary = bootstrap_mean_ci(
        primary,
        profile["bootstrap_reps"],
        seed + 2_500_000,
    )
    primary_test = signflip_greater(
        primary,
        profile["permutations"],
        seed + 2_600_000,
    )

    secondary_summary = bootstrap_mean_ci(
        secondary,
        profile["bootstrap_reps"],
        seed + 2_700_000,
    )
    secondary_test = signflip_greater(
        secondary,
        profile["permutations"],
        seed + 2_800_000,
    )

    def mean_nested(policy: str, key: str):
        vals = [r[policy][key] for r in runs]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else None

    result = {
        "groups": profile["groups"],
        "all_exact_loss_counts_matched": bool(all(
            r["exact_loss_count_match"] for r in runs
        )),
        "mean_cumulative_loss_count_each": float(np.mean([
            r["cumulative_loss_count_each"] for r in runs
        ])),

        "surface": {
            "mean_reoccupation_per_loss": mean_nested(
                "surface", "reoccupation_per_loss"
            ),
            "mean_lost_site_reoccupied_fraction": mean_nested(
                "surface", "lost_site_reoccupied_fraction"
            ),
            "mean_reoccupation_delay": mean_nested(
                "surface", "mean_reoccupation_delay"
            ),
            "mean_first_occupation_count": mean_nested(
                "surface", "first_occupation_count"
            ),
            "mean_reoccupation_count": mean_nested(
                "surface", "reoccupation_count"
            ),
            "mean_new_frontier_sites_per_loss": mean_nested(
                "surface", "mean_new_frontier_sites_per_loss"
            ),
            "mean_late_population": mean_nested(
                "surface", "late_mean_population"
            ),
            "mean_late_holes": mean_nested(
                "surface", "late_mean_holes"
            ),
        },

        "interior": {
            "mean_reoccupation_per_loss": mean_nested(
                "interior", "reoccupation_per_loss"
            ),
            "mean_lost_site_reoccupied_fraction": mean_nested(
                "interior", "lost_site_reoccupied_fraction"
            ),
            "mean_reoccupation_delay": mean_nested(
                "interior", "mean_reoccupation_delay"
            ),
            "mean_first_occupation_count": mean_nested(
                "interior", "first_occupation_count"
            ),
            "mean_reoccupation_count": mean_nested(
                "interior", "reoccupation_count"
            ),
            "mean_new_frontier_sites_per_loss": mean_nested(
                "interior", "mean_new_frontier_sites_per_loss"
            ),
            "mean_late_population": mean_nested(
                "interior", "late_mean_population"
            ),
            "mean_late_holes": mean_nested(
                "interior", "late_mean_holes"
            ),
        },

        "primary_interior_minus_surface_reoccupation_per_loss": (
            primary_summary
        ),
        "primary_directional_test": primary_test,
        "primary_sei": profile[
            "primary_sei_reoccupation_per_loss"
        ],

        "secondary_interior_minus_surface_lost_site_reoccupied_fraction": (
            secondary_summary
        ),
        "secondary_directional_test": secondary_test,
        "secondary_sei": profile[
            "secondary_sei_reoccupied_lost_site_fraction"
        ],

        "status": "MEASURED",
        "_runs": runs,
    }

    reporter.json("stage-02-exact-pair.json", result)
    reporter.stage(
        "stage-02-exact-pair.md",
        "Stage 2 — Separate First Occupation from Reoccupation",
        result,
    )

    # Plot mean per-step first occupation and reoccupation.
    image_dir.mkdir(parents=True, exist_ok=True)

    horizon = profile["continuation_steps"]
    xs = np.arange(1, horizon + 1)

    s_first = np.mean(np.asarray([
        r["per_step"]["surface"]["first"]
        for r in runs
    ], dtype=float), axis=0)
    s_reocc = np.mean(np.asarray([
        r["per_step"]["surface"]["reoccupation"]
        for r in runs
    ], dtype=float), axis=0)
    i_first = np.mean(np.asarray([
        r["per_step"]["interior"]["first"]
        for r in runs
    ], dtype=float), axis=0)
    i_reocc = np.mean(np.asarray([
        r["per_step"]["interior"]["reoccupation"]
        for r in runs
    ], dtype=float), axis=0)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(xs, s_first, label="surface: first occupation")
    ax.plot(xs, s_reocc, label="surface: reoccupation")
    ax.plot(xs, i_first, label="interior: first occupation")
    ax.plot(xs, i_reocc, label="interior: reoccupation")
    ax.set_xlabel("Continuation update")
    ax.set_ylabel("Mean attachments")
    ax.set_title(
        "Chapter 20 V2: first occupation vs reoccupation"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch20-v2-01-first-vs-reoccupation.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_3_causal_chain(
    reporter: Reporter,
    profile: dict,
    stage2: dict,
) -> dict:
    s = stage2["surface"]
    i = stage2["interior"]

    result = {
        "mechanism_chain": {
            "surface": {
                "new_frontier_sites_per_loss": s[
                    "mean_new_frontier_sites_per_loss"
                ],
                "reoccupation_per_loss": s[
                    "mean_reoccupation_per_loss"
                ],
                "lost_site_reoccupied_fraction": s[
                    "mean_lost_site_reoccupied_fraction"
                ],
                "late_holes": s[
                    "mean_late_holes"
                ],
            },
            "interior": {
                "new_frontier_sites_per_loss": i[
                    "mean_new_frontier_sites_per_loss"
                ],
                "reoccupation_per_loss": i[
                    "mean_reoccupation_per_loss"
                ],
                "lost_site_reoccupied_fraction": i[
                    "mean_lost_site_reoccupied_fraction"
                ],
                "late_holes": i[
                    "mean_late_holes"
                ],
            },
        },
        "bounded_interpretation": (
            "This stage is descriptive. It checks whether equal-count interior "
            "loss creates more new frontier and more subsequent reoccupation "
            "than equal-count surface loss. It does not label reoccupation as "
            "repair."
        ),
        "status": "MEASURED",
    }

    reporter.json("stage-03-causal-chain.json", result)
    reporter.stage(
        "stage-03-causal-chain.md",
        "Stage 3 — Trace Loss to Frontier to Reoccupation",
        result,
    )
    return result


def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage2: dict,
) -> dict:
    primary = stage2[
        "primary_interior_minus_surface_reoccupation_per_loss"
    ]
    secondary = stage2[
        "secondary_interior_minus_surface_lost_site_reoccupied_fraction"
    ]

    primary_ok = (
        stage2["all_exact_loss_counts_matched"]
        and stage2["primary_directional_test"]["p_value"]
        < profile["alpha"]
        and primary["mean"]
        >= profile["primary_sei_reoccupation_per_loss"]
    )

    secondary_ok = (
        stage2["secondary_directional_test"]["p_value"]
        < profile["alpha"]
        and secondary["mean"]
        >= profile[
            "secondary_sei_reoccupied_lost_site_fraction"
        ]
    )

    if primary_ok:
        status = "SUPPORTED"
        bounded = (
            "With loss quantity held exactly equal, interior-biased material "
            "loss produced a scientifically meaningful increase in ordinary "
            "reoccupation of previously occupied sites relative to "
            "surface-biased loss. This supports the mechanism that material "
            "removal can create construction opportunities that the frozen "
            "Digital Crystal growth rule subsequently reuses."
        )
    else:
        status = "FAILED"
        bounded = (
            "Chapter 20 V2 did not establish the predeclared increase in "
            "reoccupation per loss for interior-biased versus surface-biased "
            "material removal under the exact-count protocol."
        )

    result = {
        "question": (
            "Does material loss create new construction opportunity that is "
            "used as reoccupation by ordinary Digital Crystal growth?"
        ),
        "primary_gate_passed": primary_ok,
        "primary_mean_interior_minus_surface_reoccupation_per_loss": (
            primary["mean"]
        ),
        "primary_ci95": [
            primary["ci95_low"],
            primary["ci95_high"],
        ],
        "primary_p_value": stage2[
            "primary_directional_test"
        ]["p_value"],
        "primary_sei": profile[
            "primary_sei_reoccupation_per_loss"
        ],

        "secondary_gate_passed": secondary_ok,
        "secondary_mean_interior_minus_surface_lost_site_reoccupied_fraction": (
            secondary["mean"]
        ),
        "secondary_p_value": stage2[
            "secondary_directional_test"
        ]["p_value"],
        "secondary_sei": profile[
            "secondary_sei_reoccupied_lost_site_fraction"
        ],

        "status": status,
        "bounded_claim": bounded,

        "forbidden_overclaims": [
            "repair",
            "regeneration",
            "maintenance",
            "homeostasis",
            "metabolism",
            "death",
            "aging",
            "organism",
            "life",
        ],

        "next_question_if_supported": (
            "Does reoccupation merely refill local vacancies, or can a finite "
            "computational update budget force a tradeoff between outward "
            "construction and preservation of already-built material?"
        ),
        "next_question_if_failed": (
            "Do not tune placement fractions. Close the reoccupation mechanism "
            "and move to a qualitatively different maintenance constraint."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 20 V2 Verdict",
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
        default=20260827,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch20-material-loss-v2"
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
        "run_type": "LOSS-CREATED-CONSTRUCTION-OPPORTUNITY AUTOPSY",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_growth_rule_modified": False,
        "v1_result": (
            "FAILED finite-regime hypothesis; exact-count placement test "
            "showed interior loss retained substantially larger late "
            "population and many more holes."
        ),
        "v2_new_measurement": (
            "Observer-only distinction between first occupation and "
            "reoccupation after material loss."
        ),
        "scientific_boundary": (
            "Reoccupation mechanism only. No repair, regeneration, "
            "maintenance, homeostasis, metabolism, death, organism, or life "
            "claim."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 20 V2 — LOSS-CREATED CONSTRUCTION OPPORTUNITY")
    print(
        f"profile={args.profile} "
        f"groups={profile['groups']} "
        f"version={EXPERIMENT_VERSION}"
    )
    print("=" * 78)

    s0 = stage_0_protocol(
        reporter,
        profile,
    )
    s1 = stage_1_no_loss(
        reporter,
        profile,
        crystal_params,
        args.seed,
    )
    s2 = stage_2_exact_pair(
        reporter,
        profile,
        crystal_params,
        args.seed,
        args.image_dir,
    )
    s3 = stage_3_causal_chain(
        reporter,
        profile,
        s2,
    )
    s4 = stage_4_verdict(
        reporter,
        profile,
        s2,
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
    print("CHAPTER 20 V2 COMPLETE")
    print(f"protocol={s0['status']}")
    print(f"no_loss_null={s1['status']}")
    print(f"exact_pair={s2['status']}")
    print(f"causal_chain={s3['status']}")
    print(f"FINAL={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
