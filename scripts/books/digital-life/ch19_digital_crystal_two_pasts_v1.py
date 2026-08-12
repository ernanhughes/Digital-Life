#!/usr/bin/env python3
"""
Chapter 19 — Can the Crystal Tell Two Pasts Apart?

Scientific question
-------------------
Can two different prior experiences leave different retained local material
states that change the response to the same later challenge?

This experiment deliberately starts from Chapter 18's frozen Digital Crystal
substrate and introduces the smallest qualitative extension needed to ask that
question:

    NORMAL
    HISTORY_A
    HISTORY_B

The two history states are written to EXACTLY THE SAME material locations and
are propagated through EXACTLY THE SAME material locations before challenge.
They are inert during retention.  Therefore, immediately before the challenge:

    visible morphology        identical
    occupied cells            identical
    label locations           identical
    environment history       identical
    copy quantity             identical
    propagation placement     identical

Only label identity differs.

A later common challenge reads the retained state through a symmetric local
material interaction:

    HISTORY_A neighbor -> + history_read_gain during challenge
    HISTORY_B neighbor -> - history_read_gain during challenge

The primary result is the difference in challenge response between A-history
and B-history, expressed as cumulative post-challenge attachment difference
normalized by pre-challenge population.

This is NOT a memory experiment in the strong sense.  It tests only whether
the identity of a prior experience can remain locally encoded and alter a
later response under this minimal material mechanism.

Requires the Chapter 18 V7 script in the same directory:
    ch18_digital_crystal_persistent_material_state_v7.py
"""

from __future__ import annotations

import argparse
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
EXPERIMENT_VERSION = "digital-crystal-two-pasts-v1"
SCHEMA_VERSION = 1
CHAPTER = 19
CHAPTER_TITLE = "Can the Crystal Tell Two Pasts Apart?"

Cell = Tuple[int, int]


# ============================================================================
# Frozen Chapter 19 protocol
# ============================================================================

@dataclass(frozen=True)
class HistoryParams:
    """
    Minimal two-history material extension.

    Both history states use identical storage and propagation mechanics.
    They differ only in how they bias a later challenge.

    During ordinary retention:
        history labels are causally inert.

    During the one-step common challenge:
        A-neighbours add +history_read_gain
        B-neighbours add -history_read_gain

    This symmetry is deliberate.  It keeps history identity as the only
    pre-challenge difference while allowing a later common event to test
    whether that identity is still causally readable.
    """

    write_fraction: float = 0.20
    transmission_fraction: float = 0.50
    history_read_gain: float = 0.18
    challenge_gain: float = 0.65


@dataclass
class HistoryState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    history_a: Set[Cell]
    history_b: Set[Cell]
    step: int
    stream_seed: int
    attachments_by_step: List[int]
    population_by_step: List[int]


PROFILES = {
    "quick": {
        "groups": 96,
        "seed_noise_groups": 200,
        "radius": 64,
        "warmup_steps": 14,

        # One experience-writing event after warmup.
        "experience_elapsed_step": 3,

        # Retain/propagate the material state before challenge.
        "retention_steps": 10,

        # One identical later challenge.
        "challenge_elapsed_step": 14,

        # Primary response integrates the challenge step and the following
        # three updates.
        "response_horizon": 4,

        "write_fraction": 0.20,
        "transmission_fraction": 0.50,
        "history_read_gain": 0.18,
        "challenge_gain": 0.65,

        # Scientifically meaningful minimum effect:
        # A-vs-B challenge interaction must alter cumulative construction by
        # at least 1% of the pre-challenge crystal population.
        "primary_sei_population_fraction": 0.01,

        # It must also be at least half one seed-noise SD.
        "primary_sei_seed_noise_sd": 0.50,

        "bootstrap_reps": 2000,
        "permutations": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,

        # Secondary/co-moving diagnostic only.
        "aperture_observation_steps": [1, 2, 4, 6, 8, 10],
    },
    "standard": {
        "groups": 200,
        "seed_noise_groups": 300,
        "radius": 64,
        "warmup_steps": 14,
        "experience_elapsed_step": 3,
        "retention_steps": 10,
        "challenge_elapsed_step": 14,
        "response_horizon": 4,
        "write_fraction": 0.20,
        "transmission_fraction": 0.50,
        "history_read_gain": 0.18,
        "challenge_gain": 0.65,
        "primary_sei_population_fraction": 0.01,
        "primary_sei_seed_noise_sd": 0.50,
        "bootstrap_reps": 4000,
        "permutations": 8000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
        "aperture_observation_steps": [1, 2, 4, 6, 8, 10],
    },
    "full": {
        "groups": 400,
        "seed_noise_groups": 500,
        "radius": 64,
        "warmup_steps": 14,
        "experience_elapsed_step": 3,
        "retention_steps": 10,
        "challenge_elapsed_step": 14,
        "response_horizon": 4,
        "write_fraction": 0.20,
        "transmission_fraction": 0.50,
        "history_read_gain": 0.18,
        "challenge_gain": 0.65,
        "primary_sei_population_fraction": 0.01,
        "primary_sei_seed_noise_sd": 0.50,
        "bootstrap_reps": 6000,
        "permutations": 12000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
        "aperture_observation_steps": [1, 2, 4, 6, 8, 10],
    },
}


# ============================================================================
# State helpers
# ============================================================================

def history_params_from_profile(profile: dict) -> HistoryParams:
    return HistoryParams(
        write_fraction=float(profile["write_fraction"]),
        transmission_fraction=float(profile["transmission_fraction"]),
        history_read_gain=float(profile["history_read_gain"]),
        challenge_gain=float(profile["challenge_gain"]),
    )


def from_ch18_checkpoint(state: ch18.MaterialCrystalState) -> HistoryState:
    return HistoryState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        history_a=set(),
        history_b=set(),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
    )


def clone_history_state(state: HistoryState) -> HistoryState:
    return HistoryState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        history_a=set(state.history_a),
        history_b=set(state.history_b),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
    )


def history_locations(state: HistoryState) -> Set[Cell]:
    return set(state.history_a) | set(state.history_b)


def history_type(state: HistoryState) -> str:
    if state.history_a and state.history_b:
        return "mixed"
    if state.history_a:
        return "A"
    if state.history_b:
        return "B"
    return "none"


def erase_history_identity(state: HistoryState) -> HistoryState:
    out = clone_history_state(state)
    out.history_a.clear()
    out.history_b.clear()
    return out


# ============================================================================
# Frozen geometry / growth
# ============================================================================

def frontier_cells(occupied: Set[Cell], radius: int) -> Set[Cell]:
    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in ch18.neighbors(cell):
            if nb not in occupied and ch18.hex_distance(nb) <= radius:
                frontier.add(nb)
    return frontier


def boundary_cells(occupied: Set[Cell]) -> List[Cell]:
    out: List[Cell] = []
    for cell in sorted(occupied):
        degree = sum(nb in occupied for nb in ch18.neighbors(cell))
        if degree < 6:
            out.append(cell)
    return out


def grow_history_one_step(
    state: HistoryState,
    input_value: float,
    challenge_bit: int,
    radius: int,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
) -> Tuple[HistoryState, List[Cell]]:
    """
    Frozen Digital Crystal growth plus the Chapter 19 challenge readout term.

    HISTORY_A and HISTORY_B are inert unless challenge_bit == 1.
    """

    occupied_before = set(state.occupied)
    a_before = set(state.history_a)
    b_before = set(state.history_b)

    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    next_step = state.step + 1
    additions: List[Cell] = []

    for cell in sorted(frontier_cells(occupied_before, radius)):
        n = sum(nb in occupied_before for nb in ch18.neighbors(cell))
        a_n = sum(nb in a_before for nb in ch18.neighbors(cell))
        b_n = sum(nb in b_before for nb in ch18.neighbors(cell))

        theta = ch18.local_exposure_angle(cell, occupied_before)
        phase = crystal_params.signal_phase_gain * float(input_value)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)

        history_read = (
            int(challenge_bit)
            * history_params.history_read_gain
            * float(a_n - b_n)
        )

        score = (
            crystal_params.base_bias
            + crystal_params.neighbor_gain * n
            + crystal_params.signal_rate_gain * float(input_value)
            + crystal_params.anisotropy_gain * anisotropy
            - crystal_params.crowding_penalty * crowding
            + history_read
        )

        u = ch18.cell_uniform(state.stream_seed, next_step, cell)
        if u < ch18.logistic_scalar(score):
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    out = HistoryState(
        occupied=occupied,
        birth_time=birth_time,
        history_a=set(a_before),
        history_b=set(b_before),
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
    )

    return out, additions


# ============================================================================
# Experience writing and propagation
# ============================================================================

def write_history_to_same_locations(
    base: HistoryState,
    history_label: str,
    write_fraction: float,
) -> Tuple[HistoryState, List[Cell]]:
    """
    A and B histories write to exactly the same deterministic boundary cells.

    The selected locations depend only on the frozen checkpoint geometry and
    keyed material RNG.  Label identity is applied after selection.
    """

    candidates = boundary_cells(base.occupied)
    if not candidates:
        raise RuntimeError("No boundary cells available for history write.")

    k = int(round(write_fraction * len(candidates)))
    k = max(1, min(len(candidates), k))

    ranked = sorted(
        candidates,
        key=lambda c: (
            ch18.material_uniform(base.stream_seed, base.step + 1, c),
            c,
        ),
    )
    selected = ranked[:k]

    out = clone_history_state(base)
    if history_label == "A":
        out.history_a.update(selected)
    elif history_label == "B":
        out.history_b.update(selected)
    else:
        raise ValueError(history_label)

    return out, selected


def eligible_history_targets(
    additions: Sequence[Cell],
    labelled_before: Set[Cell],
) -> List[Cell]:
    return [
        cell
        for cell in additions
        if any(nb in labelled_before for nb in ch18.neighbors(cell))
    ]


def select_shared_surface_targets(
    eligible: Sequence[Cell],
    occupied_after: Set[Cell],
    stream_seed: int,
    step: int,
    k: int,
) -> List[Cell]:
    """
    Surface-biased deterministic keyed selection.

    A and B branches have identical geometry/label locations before challenge,
    therefore they receive exactly the same selected propagation locations.
    """

    if k <= 0:
        return []

    def exposure(cell: Cell) -> float:
        return ch18.surface_exposure_after_attachment(cell, occupied_after)

    ranked = sorted(
        eligible,
        key=lambda c: (
            -exposure(c),
            ch18.transmission_rank_uniform(stream_seed, step, c),
            c,
        ),
    )
    return ranked[:k]


def apply_history_targets(
    state: HistoryState,
    selected: Sequence[Cell],
    label: str,
) -> HistoryState:
    out = clone_history_state(state)
    if label == "A":
        out.history_a.update(selected)
    elif label == "B":
        out.history_b.update(selected)
    else:
        raise ValueError(label)
    return out


def accessibility_metrics(state: HistoryState, radius: int) -> dict:
    labelled = history_locations(state)
    frontier = frontier_cells(state.occupied, radius)

    if not frontier:
        return {
            "frontier_count": 0,
            "frontier_contact_count": 0,
            "frontier_contact_fraction": 0.0,
            "labelled_count": len(labelled),
        }

    contact = sum(
        any(nb in labelled for nb in ch18.neighbors(cell))
        for cell in frontier
    )

    return {
        "frontier_count": len(frontier),
        "frontier_contact_count": int(contact),
        "frontier_contact_fraction": float(contact / len(frontier)),
        "labelled_count": len(labelled),
    }


# ============================================================================
# Build identical A/B pre-challenge histories
# ============================================================================

def build_history_pair(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
    group_index: int,
) -> dict:
    """
    Construct A and B histories with exact pre-challenge geometry/location match.
    """

    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    experience_step = profile["experience_elapsed_step"]
    retention_steps = profile["retention_steps"]

    total_steps = (
        warmup
        + experience_step
        + retention_steps
        + profile["response_horizon"]
        + 12
    )

    gseed = seed + group_index * 1009
    env = ch18.make_environment(total_steps, gseed + 1)

    # Chapter 18 material state disabled during warmup.
    ch18_mp = ch18.MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=0.0,
        transmission_fraction=0.0,
    )

    warm = ch18.warm_material_checkpoint(
        env=env,
        warmup_steps=warmup,
        stream_seed=gseed + 2,
        radius=radius,
        crystal_params=crystal_params,
        material_params=ch18_mp,
    )
    state = from_ch18_checkpoint(warm)

    future = env[warmup:]

    # Grow identically until the experience-write point.
    for i in range(experience_step):
        state, _ = grow_history_one_step(
            state,
            input_value=float(future[i]),
            challenge_bit=0,
            radius=radius,
            crystal_params=crystal_params,
            history_params=history_params,
        )

    a_state, a_written = write_history_to_same_locations(
        state,
        "A",
        history_params.write_fraction,
    )
    b_state, b_written = write_history_to_same_locations(
        state,
        "B",
        history_params.write_fraction,
    )

    if a_written != b_written:
        raise RuntimeError("A/B experience write locations differ.")

    aperture = {}

    # During retention labels are inert, so geometry must remain identical.
    # Propagation positions are also forced identical.
    for r in range(1, retention_steps + 1):
        env_i = experience_step + r - 1

        a_label_before = history_locations(a_state)
        b_label_before = history_locations(b_state)

        a_grown, a_additions = grow_history_one_step(
            a_state,
            float(future[env_i]),
            0,
            radius,
            crystal_params,
            history_params,
        )
        b_grown, b_additions = grow_history_one_step(
            b_state,
            float(future[env_i]),
            0,
            radius,
            crystal_params,
            history_params,
        )

        if a_grown.occupied != b_grown.occupied:
            raise RuntimeError(
                f"A/B geometry diverged during inert retention at step {r}."
            )
        if a_additions != b_additions:
            raise RuntimeError(
                f"A/B additions diverged during inert retention at step {r}."
            )

        a_eligible = eligible_history_targets(a_additions, a_label_before)
        b_eligible = eligible_history_targets(b_additions, b_label_before)

        if a_eligible != b_eligible:
            raise RuntimeError(
                f"A/B eligible propagation locations diverged at step {r}."
            )

        k = int(round(
            history_params.transmission_fraction * len(a_eligible)
        ))
        k = max(0, min(len(a_eligible), k))

        selected = select_shared_surface_targets(
            a_eligible,
            a_grown.occupied,
            a_grown.stream_seed,
            a_grown.step,
            k,
        )

        a_state = apply_history_targets(a_grown, selected, "A")
        b_state = apply_history_targets(b_grown, selected, "B")

        if history_locations(a_state) != history_locations(b_state):
            raise RuntimeError(
                f"A/B label locations diverged after propagation at step {r}."
            )

        if r in profile["aperture_observation_steps"]:
            aperture[r] = accessibility_metrics(a_state, radius)

    return {
        "a_state": a_state,
        "b_state": b_state,
        "env": env,
        "future": future,
        "next_env_index": experience_step + retention_steps,
        "written_locations": a_written,
        "aperture": aperture,
    }


# ============================================================================
# Common challenge
# ============================================================================

def run_response_branch(
    checkpoint: HistoryState,
    future: np.ndarray,
    start_env_index: int,
    challenge: bool,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
) -> dict:
    """
    Apply one common challenge (or no challenge) then continue for the frozen
    response horizon.
    """

    state = clone_history_state(checkpoint)
    horizon = profile["response_horizon"]
    radius = profile["radius"]

    attachments: List[int] = []
    populations: List[int] = []

    for j in range(horizon):
        challenge_bit = int(challenge and j == 0)
        forcing = float(future[start_env_index + j])
        if challenge_bit:
            forcing += history_params.challenge_gain

        state, additions = grow_history_one_step(
            state,
            input_value=forcing,
            challenge_bit=challenge_bit,
            radius=radius,
            crystal_params=crystal_params,
            history_params=history_params,
        )

        attachments.append(len(additions))
        populations.append(len(state.occupied))

        frac = ch18.capacity_fraction_occupied(state.occupied, radius)
        if frac >= profile["max_capacity_fraction"]:
            raise RuntimeError(
                f"Saturation guard: {frac:.3f} >= "
                f"{profile['max_capacity_fraction']:.3f}"
            )

    return {
        "state": state,
        "attachments": attachments,
        "cumulative_attachments": int(sum(attachments)),
        "populations": populations,
    }


def run_primary_group(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
    group_index: int,
) -> dict:
    built = build_history_pair(
        profile,
        crystal_params,
        history_params,
        seed,
        group_index,
    )

    a = built["a_state"]
    b = built["b_state"]

    # Validity invariant immediately before challenge.
    exact_prechallenge_match = (
        a.occupied == b.occupied
        and history_locations(a) == history_locations(b)
        and a.step == b.step
    )

    if not exact_prechallenge_match:
        raise RuntimeError("Pre-challenge A/B matching invariant failed.")

    prechallenge_population = len(a.occupied)

    a_ch = run_response_branch(
        a, built["future"], built["next_env_index"], True,
        profile, crystal_params, history_params,
    )
    a_no = run_response_branch(
        a, built["future"], built["next_env_index"], False,
        profile, crystal_params, history_params,
    )
    b_ch = run_response_branch(
        b, built["future"], built["next_env_index"], True,
        profile, crystal_params, history_params,
    )
    b_no = run_response_branch(
        b, built["future"], built["next_env_index"], False,
        profile, crystal_params, history_params,
    )

    response_a = (
        a_ch["cumulative_attachments"] - a_no["cumulative_attachments"]
    )
    response_b = (
        b_ch["cumulative_attachments"] - b_no["cumulative_attachments"]
    )

    interaction_raw = response_a - response_b
    interaction_norm = interaction_raw / max(1, prechallenge_population)

    # Strong negative control:
    # erase the retained state identity immediately before challenge.
    erased_a = erase_history_identity(a)
    erased_b = erase_history_identity(b)

    ea_ch = run_response_branch(
        erased_a, built["future"], built["next_env_index"], True,
        profile, crystal_params, history_params,
    )
    eb_ch = run_response_branch(
        erased_b, built["future"], built["next_env_index"], True,
        profile, crystal_params, history_params,
    )

    erased_exact = (
        ea_ch["state"].occupied == eb_ch["state"].occupied
        and ea_ch["attachments"] == eb_ch["attachments"]
    )

    # No-challenge A and B should remain exactly matched because retained state
    # is inert outside the challenge step.
    no_challenge_exact = (
        a_no["state"].occupied == b_no["state"].occupied
        and a_no["attachments"] == b_no["attachments"]
    )

    return {
        "prechallenge_population": prechallenge_population,
        "labelled_count": len(history_locations(a)),
        "exact_prechallenge_match": exact_prechallenge_match,
        "no_challenge_exact": no_challenge_exact,
        "erased_challenge_exact": erased_exact,
        "response_a": int(response_a),
        "response_b": int(response_b),
        "interaction_raw": int(interaction_raw),
        "interaction_norm": float(interaction_norm),
        "aperture": built["aperture"],
        "a_challenge_attachments": a_ch["attachments"],
        "b_challenge_attachments": b_ch["attachments"],
    }


# ============================================================================
# Seed-noise null
# ============================================================================

def run_seed_noise_null(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
) -> dict:
    """
    Seed-only baseline for the common challenge.

    Each replicate has no retained history.  We measure the normalized paired
    challenge response (challenge - no challenge) across independent seeds.
    """

    values = []

    for i in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 seed-noise null",
    ):
        radius = profile["radius"]
        warmup = profile["warmup_steps"]
        experience_step = profile["experience_elapsed_step"]
        retention_steps = profile["retention_steps"]
        horizon = profile["response_horizon"]

        total_steps = (
            warmup + experience_step + retention_steps + horizon + 12
        )
        gseed = seed + 1_000_000 + i * 1013
        env = ch18.make_environment(total_steps, gseed + 1)

        ch18_mp = ch18.MaterialParams(
            write_probability=0.0,
            modified_neighbor_gain=0.0,
            transmission_fraction=0.0,
        )
        warm = ch18.warm_material_checkpoint(
            env,
            warmup,
            gseed + 2,
            radius,
            crystal_params,
            ch18_mp,
        )
        state = from_ch18_checkpoint(warm)
        future = env[warmup:]

        pre_steps = experience_step + retention_steps
        for j in range(pre_steps):
            state, _ = grow_history_one_step(
                state,
                float(future[j]),
                0,
                radius,
                crystal_params,
                history_params,
            )

        pop = len(state.occupied)

        ch = run_response_branch(
            state, future, pre_steps, True,
            profile, crystal_params, history_params,
        )
        no = run_response_branch(
            state, future, pre_steps, False,
            profile, crystal_params, history_params,
        )

        delta = (
            ch["cumulative_attachments"] - no["cumulative_attachments"]
        ) / max(1, pop)

        values.append(float(delta))

    arr = np.asarray(values, dtype=float)
    return {
        "n": len(values),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "q05": float(np.quantile(arr, 0.05)),
        "q50": float(np.quantile(arr, 0.50)),
        "q95": float(np.quantile(arr, 0.95)),
        "values": values,
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

    means = np.empty(reps, dtype=float)
    for i in range(reps):
        sample = rng.choice(arr, size=len(arr), replace=True)
        means[i] = np.mean(sample)

    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
    }


def paired_signflip_test_positive(
    values: Sequence[float],
    permutations: int,
    seed: int,
) -> dict:
    """
    One-sample paired sign-flip test for mean(values) > 0.

    Each value is already the within-seed A-vs-B interaction.
    """
    arr = np.asarray(values, dtype=float)
    observed = float(np.mean(arr))

    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        signs = rng.choice(np.asarray([-1.0, 1.0]), size=len(arr))
        null[i] = float(np.mean(arr * signs))

    p = (1.0 + float(np.sum(null >= observed))) / (permutations + 1.0)

    return {
        "observed_mean": observed,
        "p_value": p,
        "alternative": "greater",
        "permutations": permutations,
    }


# ============================================================================
# Reporting
# ============================================================================

class Reporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.sections: List[Tuple[str, str]] = []

    def json(self, name: str, obj: dict) -> None:
        clean = {
            k: v
            for k, v in obj.items()
            if not k.startswith("_")
        }
        (self.report_dir / name).write_text(
            json.dumps(clean, indent=2),
            encoding="utf-8",
        )

    def stage(self, name: str, title: str, body: str) -> None:
        path = self.report_dir / name
        path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        self.sections.append((title, body))

    def full_report(self, metadata: dict) -> Path:
        path = self.report_dir / "ch19-two-pasts-v1-full-report.md"

        parts = [
            "# Chapter 19 — Can the Crystal Tell Two Pasts Apart?",
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

        path.write_text("\n".join(parts), encoding="utf-8")
        return path


# ============================================================================
# Experimental stages
# ============================================================================

def stage_0_protocol_audit(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "question": (
            "Can two different prior experiences leave different retained "
            "material states that change response to the same later challenge?"
        ),
        "new_sentence_if_successful": (
            "Under this minimal two-state material extension, the identity of "
            "an earlier experience remains locally encoded and alters the "
            "crystal's response to a later identical challenge."
        ),
        "primary_outcome": (
            "(A challenge response - A no-challenge response) - "
            "(B challenge response - B no-challenge response), normalized by "
            "pre-challenge population"
        ),
        "primary_direction": "A > B",
        "primary_sei_population_fraction": profile[
            "primary_sei_population_fraction"
        ],
        "primary_sei_seed_noise_sd": profile[
            "primary_sei_seed_noise_sd"
        ],
        "alpha": profile["alpha"],
        "forbidden_overclaims": [
            "memory",
            "learning",
            "adaptation",
            "recall",
            "recognition",
            "meaning",
            "representation",
            "self",
            "life",
        ],
        "status": "MEASURED",
    }

    reporter.json("stage-00-protocol-audit.json", result)
    reporter.stage(
        "stage-00-protocol-audit.md",
        "Stage 0 — Freeze the Chapter 19 Claim",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_1_seed_noise(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
) -> dict:
    null = run_seed_noise_null(
        profile,
        crystal_params,
        history_params,
        seed,
    )

    result = {
        "role": "SEED-NOISE NULL",
        "groups": profile["seed_noise_groups"],
        "challenge_response_normalized": {
            k: v for k, v in null.items() if k != "values"
        },
        "status": "MEASURED",
    }

    reporter.json("stage-01-seed-noise.json", result)
    reporter.stage(
        "stage-01-seed-noise.md",
        "Stage 1 — Establish the Seed-Noise Scale",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    return {
        **result,
        "_values": null["values"],
    }


def stage_2_prechallenge_invariants(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
) -> dict:
    groups = min(24, profile["groups"])

    pre = []
    no_ch = []
    erased = []
    labelled = []
    aperture_by_step = {
        t: [] for t in profile["aperture_observation_steps"]
    }

    for g in tqdm(
        range(groups),
        desc="Stage 2 invariants",
    ):
        r = run_primary_group(
            profile,
            crystal_params,
            history_params,
            seed + 2_000_000,
            g,
        )

        pre.append(r["exact_prechallenge_match"])
        no_ch.append(r["no_challenge_exact"])
        erased.append(r["erased_challenge_exact"])
        labelled.append(r["labelled_count"])

        for t, m in r["aperture"].items():
            aperture_by_step[t].append(
                m["frontier_contact_fraction"]
            )

    aperture_summary = {
        str(t): {
            "mean_frontier_contact_fraction": float(
                np.mean(aperture_by_step[t])
            ) if aperture_by_step[t] else 0.0,
        }
        for t in profile["aperture_observation_steps"]
    }

    result = {
        "audit_groups": groups,
        "prechallenge_geometry_and_label_locations_exact_all": bool(all(pre)),
        "no_challenge_A_B_exact_all": bool(all(no_ch)),
        "erased_history_challenge_exact_all": bool(all(erased)),
        "mean_labelled_cells_at_challenge": float(np.mean(labelled)),
        "co_moving_aperture_diagnostic": aperture_summary,
        "aperture_note": (
            "Secondary only. This tracks whether retained history remains in "
            "contact with the moving growth frontier; it is not a wave claim."
        ),
        "status": (
            "MEASURED"
            if all(pre) and all(no_ch) and all(erased)
            else "FAILED"
        ),
    }

    reporter.json("stage-02-invariants.json", result)
    reporter.stage(
        "stage-02-invariants.md",
        "Stage 2 — Prove A and B Differ Only in Retained State Identity",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_3_primary_test(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    history_params: HistoryParams,
    seed: int,
    image_dir: Path,
) -> dict:
    interactions = []
    response_a = []
    response_b = []
    populations = []
    labelled = []

    per_step_a = np.zeros(profile["response_horizon"], dtype=float)
    per_step_b = np.zeros(profile["response_horizon"], dtype=float)

    invariant_pre = []
    invariant_no = []
    invariant_erased = []

    for g in tqdm(
        range(profile["groups"]),
        desc="Stage 3 primary two-pasts test",
    ):
        r = run_primary_group(
            profile,
            crystal_params,
            history_params,
            seed + 3_000_000,
            g,
        )

        interactions.append(r["interaction_norm"])
        response_a.append(r["response_a"])
        response_b.append(r["response_b"])
        populations.append(r["prechallenge_population"])
        labelled.append(r["labelled_count"])

        per_step_a += np.asarray(r["a_challenge_attachments"], dtype=float)
        per_step_b += np.asarray(r["b_challenge_attachments"], dtype=float)

        invariant_pre.append(r["exact_prechallenge_match"])
        invariant_no.append(r["no_challenge_exact"])
        invariant_erased.append(r["erased_challenge_exact"])

    per_step_a /= profile["groups"]
    per_step_b /= profile["groups"]

    summary = bootstrap_mean_ci(
        interactions,
        profile["bootstrap_reps"],
        seed + 3_100_000,
    )
    test = paired_signflip_test_positive(
        interactions,
        profile["permutations"],
        seed + 3_200_000,
    )

    result = {
        "groups": profile["groups"],
        "primary_interaction_normalized": summary,
        "primary_directional_test": test,
        "mean_raw_response_A_attachments": float(np.mean(response_a)),
        "mean_raw_response_B_attachments": float(np.mean(response_b)),
        "mean_prechallenge_population": float(np.mean(populations)),
        "mean_labelled_cells_at_challenge": float(np.mean(labelled)),
        "all_prechallenge_invariants_pass": bool(all(invariant_pre)),
        "all_no_challenge_A_B_exact": bool(all(invariant_no)),
        "all_erased_history_challenge_exact": bool(all(invariant_erased)),
        "mean_challenge_attachments_by_response_step": {
            "A": [float(x) for x in per_step_a],
            "B": [float(x) for x in per_step_b],
        },
        "status": "MEASURED",
    }

    reporter.json("stage-03-primary-test.json", result)
    reporter.stage(
        "stage-03-primary-test.md",
        "Stage 3 — Does the Identity of the Past Change the Later Response?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    image_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = np.arange(1, profile["response_horizon"] + 1)
    ax.plot(xs, per_step_a, marker="o", label="history A")
    ax.plot(xs, per_step_b, marker="o", label="history B")
    ax.set_xlabel("Response step")
    ax.set_ylabel("Mean attachments")
    ax.set_title("Chapter 19: identical challenge after two retained histories")
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch19-01-two-pasts-common-challenge.png",
        dpi=160,
    )
    plt.close(fig)

    return {
        **result,
        "_interactions": interactions,
    }


def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    interaction = stage3["primary_interaction_normalized"]
    p = stage3["primary_directional_test"]["p_value"]

    effect = interaction["mean"]
    raw_sei = profile["primary_sei_population_fraction"]

    seed_noise_sd = stage1[
        "challenge_response_normalized"
    ]["std"]
    seed_noise_standardized = (
        effect / seed_noise_sd if seed_noise_sd > 0 else float("inf")
    )

    invariant_ok = (
        stage2["status"] == "MEASURED"
        and stage3["all_prechallenge_invariants_pass"]
        and stage3["all_no_challenge_A_B_exact"]
        and stage3["all_erased_history_challenge_exact"]
    )

    significance_ok = p < profile["alpha"]
    raw_magnitude_ok = effect >= raw_sei
    noise_magnitude_ok = (
        seed_noise_standardized
        >= profile["primary_sei_seed_noise_sd"]
    )

    supported = (
        invariant_ok
        and significance_ok
        and raw_magnitude_ok
        and noise_magnitude_ok
    )

    if supported:
        status = "SUPPORTED"
        bounded_claim = (
            "Under the frozen Chapter 19 two-state material protocol, two "
            "different prior experiences left identically located but "
            "different retained local states, and those states produced "
            "meaningfully different responses to the same later challenge."
        )
    else:
        status = "FAILED"
        bounded_claim = (
            "Chapter 19 did not establish that the identity of the earlier "
            "experience produces a scientifically meaningful difference in "
            "response to the later common challenge under this protocol."
        )

    result = {
        "experiment_role": "TWO-PASTS COMMON-CHALLENGE TEST",
        "question": (
            "Can two different prior experiences leave different retained "
            "states that alter response to the same later challenge?"
        ),
        "invariant_gate_passed": invariant_ok,
        "primary_p_value": p,
        "primary_mean_normalized_interaction": effect,
        "primary_ci95": [
            interaction["ci95_low"],
            interaction["ci95_high"],
        ],
        "predeclared_sei_population_fraction": raw_sei,
        "seed_noise_sd": seed_noise_sd,
        "effect_in_seed_noise_sd": seed_noise_standardized,
        "predeclared_sei_seed_noise_sd": profile[
            "primary_sei_seed_noise_sd"
        ],
        "significance_gate_passed": significance_ok,
        "raw_magnitude_gate_passed": raw_magnitude_ok,
        "seed_noise_magnitude_gate_passed": noise_magnitude_ok,
        "status": status,
        "bounded_claim": bounded_claim,
        "forbidden_overclaims": [
            "memory",
            "learning",
            "adaptation",
            "recall",
            "recognition",
            "meaning",
            "representation",
            "self",
            "life",
        ],
        "next_question_if_supported": (
            "Can a later experience overwrite, compete with, or transform the "
            "retained state left by an earlier experience?"
        ),
        "next_question_if_failed": (
            "Do not tune significance. Diagnose whether failure came from "
            "loss of causal-aperture contact or insufficiently distinct "
            "material readout, then decide whether the mechanism itself should "
            "be redesigned."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 19 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
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
        default=20260824,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch19-two-pasts-v1"
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
    history_params = history_params_from_profile(profile)

    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "run_type": "TWO-PASTS COMMON-CHALLENGE TEST",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_ch18_substrate_modified": False,
        "chapter_19_extension": {
            "material_states": [
                "normal",
                "history_A",
                "history_B",
            ],
            "pre_challenge_A_B_geometry_identical": True,
            "pre_challenge_A_B_label_locations_identical": True,
            "history_identity_inert_until_challenge": True,
            "common_challenge": True,
        },
        "scientific_boundary": (
            "History discrimination only. No memory, learning, adaptation, "
            "recall, meaning, representation, self, or life claim."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 19 — CAN THE CRYSTAL TELL TWO PASTS APART?")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']} "
        f"seed_noise={profile['seed_noise_groups']}"
    )
    print("=" * 78)

    s0 = stage_0_protocol_audit(
        reporter,
        profile,
    )

    s1 = stage_1_seed_noise(
        reporter,
        profile,
        crystal_params,
        history_params,
        args.seed,
    )

    s2 = stage_2_prechallenge_invariants(
        reporter,
        profile,
        crystal_params,
        history_params,
        args.seed,
    )

    s3 = stage_3_primary_test(
        reporter,
        profile,
        crystal_params,
        history_params,
        args.seed,
        args.image_dir,
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
    print("CHAPTER 19 COMPLETE")
    print(f"protocol={s0['status']}")
    print(f"seed_noise={s1['status']}")
    print(f"invariants={s2['status']}")
    print(f"primary_test={s3['status']}")
    print(f"FINAL={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
