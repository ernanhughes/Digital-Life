#!/usr/bin/env python3
"""
Chapter 19 — Can the Crystal Tell Two Pasts Apart? (V2)

Mechanism redesign
==================

V1 used two symbolic material identities:

    HISTORY_A
    HISTORY_B

and an explicit A/B-specific challenge decoder.  That produced a detectable
but sub-SEI effect and therefore FAILED.

V2 removes the symbolic decoder entirely.

There is now only ONE altered material state:

    NORMAL
    MODIFIED

Two different experiences are represented by two different directional
external write events.  Both write exactly the same number of MODIFIED cells,
using the same local material state and the same later growth physics.  They
differ only in WHERE that state is initially written.

    experience A -> directional write around angle 0
    experience B -> directional write around angle pi/6

During retention, modified material uses the ordinary Chapter 18 material
interaction and propagates under an exact matched copy budget.  Thus the two
histories can produce different spatial material organizations without any
A/B label existing in the substrate.

Later, both histories receive the exact same challenge.

Primary causal question
-----------------------
Does the different retained material organization mediate a different response
to that common challenge?

Because A and B may already have different visible geometry by challenge time,
V2 uses a stronger geometry-preserving erasure control:

    retain A material -> challenge / no-challenge
    retain B material -> challenge / no-challenge

and, from the SAME pre-challenge checkpoints:

    erase A material labels -> challenge / no-challenge
    erase B material labels -> challenge / no-challenge

Primary outcome:

    retained-history interaction
    -
    erased-history interaction

where each interaction is:

    (A challenge - A no-challenge)
    -
    (B challenge - B no-challenge)

normalized by the mean pre-challenge population.

This asks whether retained material organization contributes to differential
challenge response beyond any geometry differences already created by history.

No symbolic history decoder exists.

Scientific boundary
-------------------
This is a history-dependent material-response experiment only.
It does not establish memory, learning, adaptation, recall, meaning,
representation, individuality, selfhood, or life.

Requires in the same directory:
    ch18_digital_crystal_persistent_material_state_v7.py
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import time
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import ch18_digital_crystal_persistent_material_state_v7 as ch18


BASE_MODEL_VERSION = ch18.BASE_MODEL_VERSION
EXPERIMENT_VERSION = "digital-crystal-two-pasts-v2"
SCHEMA_VERSION = 2
CHAPTER = 19
CHAPTER_TITLE = "Can the Crystal Tell Two Pasts Apart?"

Cell = Tuple[int, int]


PROFILES = {
    "quick": {
        "groups": 96,
        "seed_noise_groups": 200,
        "radius": 64,
        "warmup_steps": 14,

        # Experience is written immediately after this many ordinary
        # continuation steps following warmup.
        "pre_experience_steps": 3,

        # Retention period after directional material write.
        "retention_steps": 10,

        # Common challenge response window.
        "response_horizon": 4,

        # Same quantity written in both histories.
        "write_fraction": 0.20,

        # Exact matched per-step propagation quantity.
        "transmission_fraction": 0.50,

        # Frozen Chapter 18 local material gain.
        "modified_neighbor_gain": 0.30,

        # Identical external challenge magnitude.
        "challenge_gain": 0.65,

        # Two non-equivalent directions under six-fold anisotropy.
        "experience_angle_A": 0.0,
        "experience_angle_B": 0.5235987755982988,  # pi / 6

        # Same Chapter 19 effect-size discipline as V1.
        "primary_sei_population_fraction": 0.01,
        "primary_sei_seed_noise_sd": 0.50,

        "bootstrap_reps": 2000,
        "permutations": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,

        # Secondary diagnostics only.
        "aperture_observation_steps": [1, 2, 4, 6, 8, 10],
    },
    "standard": {
        "groups": 200,
        "seed_noise_groups": 300,
        "radius": 64,
        "warmup_steps": 14,
        "pre_experience_steps": 3,
        "retention_steps": 10,
        "response_horizon": 4,
        "write_fraction": 0.20,
        "transmission_fraction": 0.50,
        "modified_neighbor_gain": 0.30,
        "challenge_gain": 0.65,
        "experience_angle_A": 0.0,
        "experience_angle_B": 0.5235987755982988,
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
        "pre_experience_steps": 3,
        "retention_steps": 10,
        "response_horizon": 4,
        "write_fraction": 0.20,
        "transmission_fraction": 0.50,
        "modified_neighbor_gain": 0.30,
        "challenge_gain": 0.65,
        "experience_angle_A": 0.0,
        "experience_angle_B": 0.5235987755982988,
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
# Small utilities
# ============================================================================

def angular_distance(a: float, b: float) -> float:
    d = (a - b + math.pi) % (2.0 * math.pi) - math.pi
    return abs(d)


def boundary_cells(occupied: Set[Cell]) -> List[Cell]:
    out = []
    for cell in sorted(occupied):
        degree = sum(nb in occupied for nb in ch18.neighbors(cell))
        if degree < 6:
            out.append(cell)
    return out


def clone_state(state: ch18.MaterialCrystalState) -> ch18.MaterialCrystalState:
    return ch18.MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def erase_modified(state: ch18.MaterialCrystalState) -> ch18.MaterialCrystalState:
    out = clone_state(state)
    out.modified.clear()
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = 0
    return out


def normalized_difference(a: float, b: float, denom: float) -> float:
    return float((a - b) / max(1.0, float(denom)))


def bootstrap_mean_ci(values, reps: int, seed: int) -> dict:
    arr = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = np.empty(reps, dtype=float)
    for i in range(reps):
        means[i] = np.mean(
            rng.choice(arr, size=len(arr), replace=True)
        )
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
    }


def signflip_greater(values, permutations: int, seed: int) -> dict:
    arr = np.asarray(values, dtype=float)
    observed = float(np.mean(arr))
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)
    for i in range(permutations):
        signs = rng.choice(np.asarray([-1.0, 1.0]), size=len(arr))
        null[i] = np.mean(arr * signs)
    p = (1.0 + float(np.sum(null >= observed))) / (permutations + 1.0)
    return {
        "observed_mean": observed,
        "p_value": p,
        "alternative": "greater",
        "permutations": permutations,
    }


# ============================================================================
# Directional experience write
# ============================================================================

def directional_write(
    state: ch18.MaterialCrystalState,
    target_angle: float,
    write_fraction: float,
) -> Tuple[ch18.MaterialCrystalState, List[Cell]]:
    """
    Write the SAME modified state to a directional subset of the active
    boundary.

    A and B use the same K.  There is no A/B state identity in the substrate.
    """
    candidates = boundary_cells(state.occupied)
    if not candidates:
        raise RuntimeError("No boundary cells available for directional write.")

    k = int(round(float(write_fraction) * len(candidates)))
    k = max(1, min(len(candidates), k))

    ranked = sorted(
        candidates,
        key=lambda c: (
            angular_distance(
                ch18.local_exposure_angle(c, state.occupied),
                target_angle,
            ),
            ch18.material_uniform(state.stream_seed, state.step + 1, c),
            c,
        ),
    )
    selected = ranked[:k]

    out = clone_state(state)
    out.modified.update(selected)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = len(out.modified)

    return out, selected


# ============================================================================
# Retention / propagation
# ============================================================================

def matched_surface_propagation_step(
    a: ch18.MaterialCrystalState,
    b: ch18.MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    transmission_fraction: float,
) -> Tuple[ch18.MaterialCrystalState, ch18.MaterialCrystalState, dict]:
    """
    Grow A and B independently under the same environment, then enforce one
    shared propagation count K.  Placement remains surface-biased within each
    branch's own eligible set.

    Thus histories may develop different organizations, but never because one
    history was allowed more material-copy events than the other.
    """
    a_before = set(a.modified)
    b_before = set(b.modified)

    a_grown, a_additions, _ = ch18.grow_one_step_without_transmission(
        a,
        input_value,
        0,
        radius,
        crystal_params,
        material_params,
    )
    b_grown, b_additions, _ = ch18.grow_one_step_without_transmission(
        b,
        input_value,
        0,
        radius,
        crystal_params,
        material_params,
    )

    a_eligible = ch18.eligible_transmission_targets(
        a_additions, a_before
    )
    b_eligible = ch18.eligible_transmission_targets(
        b_additions, b_before
    )

    k = ch18.shared_transmission_budget(
        [len(a_eligible), len(b_eligible)],
        transmission_fraction,
    )

    a_sel, a_meta = ch18.choose_targets_with_exact_budget(
        a_eligible,
        a_grown.occupied,
        a_grown.stream_seed,
        a_grown.step,
        k,
        "surface_biased",
    )
    b_sel, b_meta = ch18.choose_targets_with_exact_budget(
        b_eligible,
        b_grown.occupied,
        b_grown.stream_seed,
        b_grown.step,
        k,
        "surface_biased",
    )

    a_out = clone_state(a_grown)
    b_out = clone_state(b_grown)
    a_out.modified.update(a_sel)
    b_out.modified.update(b_sel)

    if a_out.modified_count_by_step:
        a_out.modified_count_by_step[-1] = len(a_out.modified)
    if b_out.modified_count_by_step:
        b_out.modified_count_by_step[-1] = len(b_out.modified)

    if len(a_sel) != len(b_sel):
        raise RuntimeError("Exact matched propagation budget failed.")

    return a_out, b_out, {
        "shared_budget": int(k),
        "a_eligible": len(a_eligible),
        "b_eligible": len(b_eligible),
        "a_selected": len(a_sel),
        "b_selected": len(b_sel),
        "a_mean_selected_surface_exposure": a_meta[
            "mean_selected_surface_exposure"
        ],
        "b_mean_selected_surface_exposure": b_meta[
            "mean_selected_surface_exposure"
        ],
    }


def aperture_metrics(state: ch18.MaterialCrystalState, radius: int) -> dict:
    frontier: Set[Cell] = set()
    for cell in state.occupied:
        for nb in ch18.neighbors(cell):
            if nb not in state.occupied and ch18.hex_distance(nb) <= radius:
                frontier.add(nb)

    if not frontier:
        return {
            "frontier_count": 0,
            "contact_count": 0,
            "contact_fraction": 0.0,
            "modified_count": len(state.modified),
        }

    contact = sum(
        any(nb in state.modified for nb in ch18.neighbors(cell))
        for cell in frontier
    )

    return {
        "frontier_count": len(frontier),
        "contact_count": int(contact),
        "contact_fraction": float(contact / len(frontier)),
        "modified_count": len(state.modified),
    }


def modified_orientation_summary(
    state: ch18.MaterialCrystalState,
) -> dict:
    """
    Secondary diagnostic: where does modified material lie angularly?

    This is not interpreted as a wave, phase, or symbolic code.
    """
    if not state.modified:
        return {
            "n": 0,
            "mean_cos": 0.0,
            "mean_sin": 0.0,
            "resultant_length": 0.0,
            "mean_angle": 0.0,
        }

    angles = []
    for cell in state.modified:
        x, y = ch18.axial_to_xy(cell)
        angles.append(math.atan2(y, x))

    c = float(np.mean(np.cos(angles)))
    s = float(np.mean(np.sin(angles)))

    return {
        "n": len(angles),
        "mean_cos": c,
        "mean_sin": s,
        "resultant_length": float(math.hypot(c, s)),
        "mean_angle": float(math.atan2(s, c)),
    }


# ============================================================================
# Build two different histories from one checkpoint
# ============================================================================

def build_two_histories(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
    group_index: int,
) -> dict:
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    pre = profile["pre_experience_steps"]
    retention = profile["retention_steps"]
    horizon = profile["response_horizon"]

    total = warmup + pre + retention + horizon + 16

    gseed = seed + group_index * 1009
    env = ch18.make_environment(total, gseed + 1)

    no_material = ch18.MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=0.0,
        transmission_fraction=0.0,
    )
    state = ch18.warm_material_checkpoint(
        env,
        warmup,
        gseed + 2,
        radius,
        crystal_params,
        no_material,
    )

    future = env[warmup:]

    # Common pre-experience continuation.
    for i in range(pre):
        state, _, _ = ch18.advance_one_step_material(
            state,
            float(future[i]),
            0,
            radius,
            crystal_params,
            no_material,
        )

    # Two external directional experiences write SAME material state and SAME K.
    a, a_written = directional_write(
        state,
        profile["experience_angle_A"],
        profile["write_fraction"],
    )
    b, b_written = directional_write(
        state,
        profile["experience_angle_B"],
        profile["write_fraction"],
    )

    if len(a_written) != len(b_written):
        raise RuntimeError("Directional histories wrote unequal quantities.")

    propagation_budgets = []
    aperture = {}
    orientation = {}

    for r in range(1, retention + 1):
        env_i = pre + r - 1

        a, b, prop = matched_surface_propagation_step(
            a,
            b,
            float(future[env_i]),
            radius,
            crystal_params,
            material_params,
            profile["transmission_fraction"],
        )
        propagation_budgets.append(prop["shared_budget"])

        if r in profile["aperture_observation_steps"]:
            aperture[r] = {
                "A": aperture_metrics(a, radius),
                "B": aperture_metrics(b, radius),
            }
            orientation[r] = {
                "A": modified_orientation_summary(a),
                "B": modified_orientation_summary(b),
            }

    if sum(propagation_budgets) < 0:
        raise RuntimeError("Impossible propagation budget.")

    return {
        "a_state": a,
        "b_state": b,
        "future": future,
        "next_env_index": pre + retention,
        "initial_write_count": len(a_written),
        "cumulative_propagation_count_A": int(sum(propagation_budgets)),
        "cumulative_propagation_count_B": int(sum(propagation_budgets)),
        "aperture": aperture,
        "orientation": orientation,
    }


# ============================================================================
# Challenge branches
# ============================================================================

def run_challenge_or_control(
    checkpoint: ch18.MaterialCrystalState,
    future: np.ndarray,
    start_env_index: int,
    challenge: bool,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
) -> dict:
    state = clone_state(checkpoint)
    attachments = []
    populations = []

    for j in range(profile["response_horizon"]):
        forcing = float(future[start_env_index + j])
        if challenge and j == 0:
            forcing += profile["challenge_gain"]

        state, additions, _ = ch18.grow_one_step_without_transmission(
            state,
            forcing,
            0,  # challenge never writes new material
            profile["radius"],
            crystal_params,
            material_params,
        )

        attachments.append(len(additions))
        populations.append(len(state.occupied))

        frac = ch18.capacity_fraction_occupied(
            state.occupied,
            profile["radius"],
        )
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


def run_one_group(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
    group_index: int,
) -> dict:
    built = build_two_histories(
        profile,
        crystal_params,
        material_params,
        seed,
        group_index,
    )

    a = built["a_state"]
    b = built["b_state"]
    ea = erase_modified(a)
    eb = erase_modified(b)

    denom = 0.5 * (len(a.occupied) + len(b.occupied))

    # Retained-history arms.
    a_ch = run_challenge_or_control(
        a, built["future"], built["next_env_index"], True,
        profile, crystal_params, material_params,
    )
    a_no = run_challenge_or_control(
        a, built["future"], built["next_env_index"], False,
        profile, crystal_params, material_params,
    )
    b_ch = run_challenge_or_control(
        b, built["future"], built["next_env_index"], True,
        profile, crystal_params, material_params,
    )
    b_no = run_challenge_or_control(
        b, built["future"], built["next_env_index"], False,
        profile, crystal_params, material_params,
    )

    retained_a_response = (
        a_ch["cumulative_attachments"] - a_no["cumulative_attachments"]
    )
    retained_b_response = (
        b_ch["cumulative_attachments"] - b_no["cumulative_attachments"]
    )
    retained_interaction = normalized_difference(
        retained_a_response,
        retained_b_response,
        denom,
    )

    # Geometry-preserving erasure arms.
    ea_ch = run_challenge_or_control(
        ea, built["future"], built["next_env_index"], True,
        profile, crystal_params, material_params,
    )
    ea_no = run_challenge_or_control(
        ea, built["future"], built["next_env_index"], False,
        profile, crystal_params, material_params,
    )
    eb_ch = run_challenge_or_control(
        eb, built["future"], built["next_env_index"], True,
        profile, crystal_params, material_params,
    )
    eb_no = run_challenge_or_control(
        eb, built["future"], built["next_env_index"], False,
        profile, crystal_params, material_params,
    )

    erased_a_response = (
        ea_ch["cumulative_attachments"] - ea_no["cumulative_attachments"]
    )
    erased_b_response = (
        eb_ch["cumulative_attachments"] - eb_no["cumulative_attachments"]
    )
    erased_interaction = normalized_difference(
        erased_a_response,
        erased_b_response,
        denom,
    )

    # PRIMARY: retained material contribution beyond geometry.
    mediated_interaction = retained_interaction - erased_interaction

    return {
        "mean_prechallenge_population": float(denom),
        "pre_challenge_population_A": len(a.occupied),
        "pre_challenge_population_B": len(b.occupied),
        "pre_challenge_modified_A": len(a.modified),
        "pre_challenge_modified_B": len(b.modified),
        "initial_write_count": built["initial_write_count"],
        "cumulative_propagation_count_A": built[
            "cumulative_propagation_count_A"
        ],
        "cumulative_propagation_count_B": built[
            "cumulative_propagation_count_B"
        ],
        "retained_a_response": int(retained_a_response),
        "retained_b_response": int(retained_b_response),
        "erased_a_response": int(erased_a_response),
        "erased_b_response": int(erased_b_response),
        "retained_interaction_norm": float(retained_interaction),
        "erased_interaction_norm": float(erased_interaction),
        "mediated_interaction_norm": float(mediated_interaction),
        "a_challenge_attachments": a_ch["attachments"],
        "b_challenge_attachments": b_ch["attachments"],
        "aperture": built["aperture"],
        "orientation": built["orientation"],
    }


# ============================================================================
# Seed-noise baseline
# ============================================================================

def run_seed_noise(
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
) -> dict:
    """
    Baseline challenge-response variation in crystals with no written history.
    """
    values = []
    no_material = ch18.MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=0.0,
        transmission_fraction=0.0,
    )

    total_pre = (
        profile["pre_experience_steps"]
        + profile["retention_steps"]
    )

    for g in tqdm(
        range(profile["seed_noise_groups"]),
        desc="Stage 1 seed-noise null",
    ):
        radius = profile["radius"]
        warmup = profile["warmup_steps"]
        horizon = profile["response_horizon"]
        total = warmup + total_pre + horizon + 16

        gseed = seed + 1_000_000 + g * 1013
        env = ch18.make_environment(total, gseed + 1)

        state = ch18.warm_material_checkpoint(
            env,
            warmup,
            gseed + 2,
            radius,
            crystal_params,
            no_material,
        )
        future = env[warmup:]

        for i in range(total_pre):
            state, _, _ = ch18.advance_one_step_material(
                state,
                float(future[i]),
                0,
                radius,
                crystal_params,
                no_material,
            )

        pop = len(state.occupied)

        ch = run_challenge_or_control(
            state, future, total_pre, True,
            profile, crystal_params, no_material,
        )
        no = run_challenge_or_control(
            state, future, total_pre, False,
            profile, crystal_params, no_material,
        )

        values.append(
            normalized_difference(
                ch["cumulative_attachments"],
                no["cumulative_attachments"],
                pop,
            )
        )

    arr = np.asarray(values, dtype=float)
    return {
        "n": len(values),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)),
        "q05": float(np.quantile(arr, 0.05)),
        "q50": float(np.quantile(arr, 0.50)),
        "q95": float(np.quantile(arr, 0.95)),
        "_values": values,
    }


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections = []

    def json(self, name: str, payload: dict) -> None:
        clean = {
            k: v
            for k, v in payload.items()
            if not k.startswith("_")
        }
        (self.root / name).write_text(
            json.dumps(clean, indent=2),
            encoding="utf-8",
        )

    def stage(self, filename: str, title: str, payload: dict) -> None:
        clean = {
            k: v
            for k, v in payload.items()
            if not k.startswith("_")
        }
        body = f"```json\n{json.dumps(clean, indent=2)}\n```"
        text = f"# {title}\n\n{body}\n"
        (self.root / filename).write_text(text, encoding="utf-8")
        self.sections.append((title, body))

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch19-two-pasts-v2-full-report.md"
        parts = [
            "# Chapter 19 — Can the Crystal Tell Two Pasts Apart? (V2)",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(metadata, indent=2),
            "```",
            "",
        ]

        for title, body in self.sections:
            parts += ["---", "", f"## {title}", "", body, ""]

        path.write_text("\n".join(parts), encoding="utf-8")
        return path


# ============================================================================
# Stages
# ============================================================================

def stage_0_freeze_protocol(
    reporter: Reporter,
    profile: dict,
) -> dict:
    result = {
        "role": "FROZEN MECHANISM-REDESIGN PROTOCOL",
        "v1_failure_being_respected": (
            "V1 detected a directional A/B effect but failed both predeclared "
            "scientific-effect gates. V2 does not increase N, lower the SEI, "
            "increase the old decoder gain, or promote the first response step."
        ),
        "question": (
            "Can two different directional experiences create different "
            "spatial organizations of the SAME material state such that "
            "retained material contributes to a different response to one "
            "identical later challenge?"
        ),
        "history_encoding": (
            "Same MODIFIED state; same initial write count; different spatial "
            "write direction only."
        ),
        "no_symbolic_decoder": True,
        "exact_matched_propagation_quantity": True,
        "primary_outcome": (
            "[(A challenge-A no)-(B challenge-B no)] retained "
            "minus the same interaction after geometry-preserving material "
            "erasure, normalized by mean pre-challenge population."
        ),
        "primary_direction": "greater than zero",
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
            "wave",
            "flocking",
            "self",
            "life",
        ],
        "status": "MEASURED",
    }
    reporter.json("stage-00-protocol.json", result)
    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Freeze the V2 Mechanism Redesign",
        result,
    )
    return result


def stage_1_seed_noise(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
) -> dict:
    null = run_seed_noise(
        profile,
        crystal_params,
        material_params,
        seed,
    )
    result = {
        "role": "SEED-NOISE NULL",
        "groups": profile["seed_noise_groups"],
        "challenge_response_normalized": {
            k: v for k, v in null.items() if not k.startswith("_")
        },
        "status": "MEASURED",
        "_values": null["_values"],
    }
    reporter.json("stage-01-seed-noise.json", result)
    reporter.stage(
        "stage-01-seed-noise.md",
        "Stage 1 — Establish the Seed-Noise Scale",
        result,
    )
    return result


def stage_2_mechanism_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
) -> dict:
    groups = min(24, profile["groups"])

    initial_counts = []
    prop_a = []
    prop_b = []
    final_mod_a = []
    final_mod_b = []
    pop_diff = []

    aperture = {
        t: {"A": [], "B": []}
        for t in profile["aperture_observation_steps"]
    }
    orientation = {
        t: {"A": [], "B": []}
        for t in profile["aperture_observation_steps"]
    }

    for g in tqdm(range(groups), desc="Stage 2 mechanism audit"):
        r = run_one_group(
            profile,
            crystal_params,
            material_params,
            seed + 2_000_000,
            g,
        )
        initial_counts.append(r["initial_write_count"])
        prop_a.append(r["cumulative_propagation_count_A"])
        prop_b.append(r["cumulative_propagation_count_B"])
        final_mod_a.append(r["pre_challenge_modified_A"])
        final_mod_b.append(r["pre_challenge_modified_B"])
        pop_diff.append(
            r["pre_challenge_population_A"]
            - r["pre_challenge_population_B"]
        )

        for t in aperture:
            if t in r["aperture"]:
                aperture[t]["A"].append(
                    r["aperture"][t]["A"]["contact_fraction"]
                )
                aperture[t]["B"].append(
                    r["aperture"][t]["B"]["contact_fraction"]
                )
                orientation[t]["A"].append(
                    r["orientation"][t]["A"]["mean_angle"]
                )
                orientation[t]["B"].append(
                    r["orientation"][t]["B"]["mean_angle"]
                )

    exact_copy_quantity = all(a == b for a, b in zip(prop_a, prop_b))

    aperture_summary = {}
    orientation_summary = {}
    for t in aperture:
        aperture_summary[str(t)] = {
            "A_mean_contact_fraction": (
                float(np.mean(aperture[t]["A"]))
                if aperture[t]["A"] else 0.0
            ),
            "B_mean_contact_fraction": (
                float(np.mean(aperture[t]["B"]))
                if aperture[t]["B"] else 0.0
            ),
        }
        orientation_summary[str(t)] = {
            "A_mean_angle": (
                float(np.angle(np.mean(
                    np.exp(1j * np.asarray(orientation[t]["A"]))
                )))
                if orientation[t]["A"] else 0.0
            ),
            "B_mean_angle": (
                float(np.angle(np.mean(
                    np.exp(1j * np.asarray(orientation[t]["B"]))
                )))
                if orientation[t]["B"] else 0.0
            ),
        }

    result = {
        "audit_groups": groups,
        "initial_write_quantity_equal_by_construction": True,
        "mean_initial_write_count": float(np.mean(initial_counts)),
        "exact_cumulative_propagation_quantity_match_all_groups": (
            exact_copy_quantity
        ),
        "mean_cumulative_propagation_A": float(np.mean(prop_a)),
        "mean_cumulative_propagation_B": float(np.mean(prop_b)),
        "mean_prechallenge_modified_A": float(np.mean(final_mod_a)),
        "mean_prechallenge_modified_B": float(np.mean(final_mod_b)),
        "mean_prechallenge_population_difference_A_minus_B": float(
            np.mean(pop_diff)
        ),
        "co_moving_aperture_diagnostic": aperture_summary,
        "modified_orientation_diagnostic": orientation_summary,
        "diagnostic_note": (
            "Aperture/orientation summaries are secondary mechanism diagnostics. "
            "They do not establish a wave, phase code, or representation."
        ),
        "status": "MEASURED" if exact_copy_quantity else "FAILED",
    }

    reporter.json("stage-02-mechanism-audit.json", result)
    reporter.stage(
        "stage-02-mechanism-audit.md",
        "Stage 2 — Audit Quantity, Placement, and Causal Aperture",
        result,
    )
    return result


def stage_3_primary(
    reporter: Reporter,
    profile: dict,
    crystal_params: ch18.CrystalParams,
    material_params: ch18.MaterialParams,
    seed: int,
    image_dir: Path,
) -> dict:
    mediated = []
    retained = []
    erased = []

    response_a = []
    response_b = []
    er_response_a = []
    er_response_b = []

    pop_a = []
    pop_b = []
    mod_a = []
    mod_b = []
    copy_equal = []

    step_a = np.zeros(profile["response_horizon"], dtype=float)
    step_b = np.zeros(profile["response_horizon"], dtype=float)

    for g in tqdm(
        range(profile["groups"]),
        desc="Stage 3 V2 primary test",
    ):
        r = run_one_group(
            profile,
            crystal_params,
            material_params,
            seed + 3_000_000,
            g,
        )

        mediated.append(r["mediated_interaction_norm"])
        retained.append(r["retained_interaction_norm"])
        erased.append(r["erased_interaction_norm"])

        response_a.append(r["retained_a_response"])
        response_b.append(r["retained_b_response"])
        er_response_a.append(r["erased_a_response"])
        er_response_b.append(r["erased_b_response"])

        pop_a.append(r["pre_challenge_population_A"])
        pop_b.append(r["pre_challenge_population_B"])
        mod_a.append(r["pre_challenge_modified_A"])
        mod_b.append(r["pre_challenge_modified_B"])

        copy_equal.append(
            r["cumulative_propagation_count_A"]
            == r["cumulative_propagation_count_B"]
        )

        step_a += np.asarray(r["a_challenge_attachments"], dtype=float)
        step_b += np.asarray(r["b_challenge_attachments"], dtype=float)

    step_a /= profile["groups"]
    step_b /= profile["groups"]

    primary_summary = bootstrap_mean_ci(
        mediated,
        profile["bootstrap_reps"],
        seed + 3_100_000,
    )
    primary_test = signflip_greater(
        mediated,
        profile["permutations"],
        seed + 3_200_000,
    )

    result = {
        "groups": profile["groups"],
        "primary_material_mediated_interaction": primary_summary,
        "primary_directional_test": primary_test,
        "retained_history_interaction": bootstrap_mean_ci(
            retained,
            profile["bootstrap_reps"],
            seed + 3_300_000,
        ),
        "erased_geometry_only_interaction": bootstrap_mean_ci(
            erased,
            profile["bootstrap_reps"],
            seed + 3_400_000,
        ),
        "mean_raw_retained_response_A": float(np.mean(response_a)),
        "mean_raw_retained_response_B": float(np.mean(response_b)),
        "mean_raw_erased_response_A": float(np.mean(er_response_a)),
        "mean_raw_erased_response_B": float(np.mean(er_response_b)),
        "mean_prechallenge_population_A": float(np.mean(pop_a)),
        "mean_prechallenge_population_B": float(np.mean(pop_b)),
        "mean_prechallenge_modified_A": float(np.mean(mod_a)),
        "mean_prechallenge_modified_B": float(np.mean(mod_b)),
        "exact_propagation_quantity_match_all_groups": bool(all(copy_equal)),
        "mean_challenge_attachments_by_response_step": {
            "A": [float(x) for x in step_a],
            "B": [float(x) for x in step_b],
        },
        "status": "MEASURED",
        "_mediated_values": mediated,
    }

    reporter.json("stage-03-primary.json", result)
    reporter.stage(
        "stage-03-primary.md",
        "Stage 3 — Does Material Organization Mediate Different Later Response?",
        result,
    )

    image_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    xs = np.arange(1, profile["response_horizon"] + 1)
    ax.plot(xs, step_a, marker="o", label="experience A")
    ax.plot(xs, step_b, marker="o", label="experience B")
    ax.set_xlabel("Response step")
    ax.set_ylabel("Mean attachments")
    ax.set_title(
        "Chapter 19 V2: same challenge after two spatial material histories"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        image_dir / "ch19-v2-01-common-challenge.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def stage_4_verdict(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    primary = stage3["primary_material_mediated_interaction"]
    effect = primary["mean"]
    p = stage3["primary_directional_test"]["p_value"]

    seed_sd = stage1["challenge_response_normalized"]["std"]
    effect_sd = effect / seed_sd if seed_sd > 0 else float("inf")

    mechanism_ok = (
        stage2["status"] == "MEASURED"
        and stage3["exact_propagation_quantity_match_all_groups"]
    )
    significance_ok = p < profile["alpha"]
    magnitude_ok = (
        effect >= profile["primary_sei_population_fraction"]
    )
    noise_ok = (
        effect_sd >= profile["primary_sei_seed_noise_sd"]
    )

    supported = (
        mechanism_ok
        and significance_ok
        and magnitude_ok
        and noise_ok
    )

    if supported:
        status = "SUPPORTED"
        bounded = (
            "Under the frozen Chapter 19 V2 protocol, two different "
            "directional experiences created different spatial organizations "
            "of the same retained material state, and that retained material "
            "contributed a scientifically meaningful difference in response "
            "to the same later challenge beyond the geometry-only erasure "
            "control."
        )
    else:
        status = "FAILED"
        bounded = (
            "Chapter 19 V2 did not establish that different spatial "
            "organizations produced by two prior directional experiences "
            "contribute a scientifically meaningful difference in response "
            "to the later common challenge beyond the geometry-only erasure "
            "control."
        )

    result = {
        "experiment_role": "NON-SYMBOLIC TWO-HISTORY MATERIAL TEST",
        "question": (
            "Can different experiences create different spatial material "
            "organizations that materially mediate different later responses?"
        ),
        "mechanism_validity_gate_passed": mechanism_ok,
        "primary_p_value": p,
        "primary_mean_material_mediated_interaction": effect,
        "primary_ci95": [
            primary["ci95_low"],
            primary["ci95_high"],
        ],
        "predeclared_sei_population_fraction": profile[
            "primary_sei_population_fraction"
        ],
        "seed_noise_sd": seed_sd,
        "effect_in_seed_noise_sd": effect_sd,
        "predeclared_sei_seed_noise_sd": profile[
            "primary_sei_seed_noise_sd"
        ],
        "significance_gate_passed": significance_ok,
        "raw_magnitude_gate_passed": magnitude_ok,
        "seed_noise_magnitude_gate_passed": noise_ok,
        "status": status,
        "bounded_claim": bounded,
        "forbidden_overclaims": [
            "memory",
            "learning",
            "adaptation",
            "recall",
            "recognition",
            "meaning",
            "representation",
            "wave",
            "flocking",
            "self",
            "life",
        ],
        "next_question_if_supported": (
            "Can a later experience rewrite or compete with the spatial "
            "material organization left by an earlier experience?"
        ),
        "next_question_if_failed": (
            "Do not tune the effect threshold or promote a secondary endpoint. "
            "Close this specific history-discrimination mechanism unless a "
            "qualitatively different material encoding mechanism is proposed."
        ),
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 19 V2 Verdict",
        result,
    )
    return result


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="quick",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260825,
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch19-two-pasts-v2"
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
    material_params = ch18.MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=profile["modified_neighbor_gain"],
        transmission_fraction=profile["transmission_fraction"],
    )

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "run_type": "NON-SYMBOLIC TWO-HISTORY MATERIAL TEST",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_ch18_substrate_modified": False,
        "v1_result": (
            "FAILED: explicit A/B label decoder produced a statistically "
            "detectable but sub-SEI effect."
        ),
        "v2_design": (
            "Remove symbolic A/B states. Use one MODIFIED state written to "
            "different directional boundary locations, exact-match subsequent "
            "propagation quantity, then test one common later challenge with a "
            "geometry-preserving label-erasure control."
        ),
        "scientific_boundary": (
            "History-dependent material response only. No memory, learning, "
            "adaptation, recall, representation, wave, flocking, self, or life "
            "claim."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 19 V2 — CAN THE CRYSTAL TELL TWO PASTS APART?")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']}"
    )
    print("=" * 78)

    s0 = stage_0_freeze_protocol(
        reporter,
        profile,
    )
    s1 = stage_1_seed_noise(
        reporter,
        profile,
        crystal_params,
        material_params,
        args.seed,
    )
    s2 = stage_2_mechanism_audit(
        reporter,
        profile,
        crystal_params,
        material_params,
        args.seed,
    )
    s3 = stage_3_primary(
        reporter,
        profile,
        crystal_params,
        material_params,
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
    print("CHAPTER 19 V2 COMPLETE")
    print(f"protocol={s0['status']}")
    print(f"seed_noise={s1['status']}")
    print(f"mechanism_audit={s2['status']}")
    print(f"primary={s3['status']}")
    print(f"FINAL={s4['status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
