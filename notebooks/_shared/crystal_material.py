"""MODIFIED-cell material-state extension for the Digital Crystal substrate.

Implements Chapter 9's "one more kind of cell" idiom that the historical
`ch18_digital_crystal_persistent_material_state_v1..v10` chain and the
`ch19_digital_crystal_two_pasts_v1/v2` chain both built on top of:

    EMPTY  ->  OCCUPIED_NORMAL  ->  OCCUPIED_MODIFIED

A pulse can convert already-occupied *boundary* cells from normal to
modified. Modification does exactly two things: it persists (nothing in
this module ever un-modifies a cell), and while a modified cell sits next
to a frontier candidate, it adds `modified_neighbor_gain * modified_n` to
that candidate's attachment-probability score (`modified_n` = count of
modified neighbours). There is no history list, decoder, learned weight,
or target morphology anywhere in this module.

This is a faithful, reduced re-implementation of the mechanism shared by
`scripts/books/digital-life/ch18_digital_crystal_persistent_material_state_v1.py`
(write/persist/erase-ablation/causal-chain-audit) and `..._v7.py` (matched-
budget placement policies used for the integrated causal-lifetime result,
DL-09-C04) and `ch19_digital_crystal_two_pasts_v2.py` (directional write +
orientation diagnostic used for the non-symbolic history-discrimination
test). It does not import those scripts directly -- they are single, very
long CLI programs bundling simulation, staged reporting and plotting -- but
every function below mirrors one specific function from that family
one-for-one, named the same way, so the mapping back to the canonical
source is direct. Deliberate reductions (radius, groups, propagation
window) are disclosed in the notebook, not here.

CRN coupling
------------
Growth draws use `digital_crystal.cell_keyed_uniform` (cell-keyed common
random numbers), exactly like `crystal_causal.py`'s `crn_step` -- this is
what lets a "retained" branch and an "erased" branch (or two directional
histories A/B) share identical growth luck at every shared candidate cell,
so any divergence is attributable to the material difference, not
independently-sampled randomness. Material writes and transmission-target
ranking use their own separate keyed streams (`"material:"` / `"transmission-
uniform:"` namespaces below), matching the canonical scripts' design of
keeping the material channel from ever perturbing the growth RNG stream.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Set, Tuple

import numpy as np

from digital_crystal import (
    Cell,
    CrystalParams,
    cell_keyed_uniform,
    frontier,
    hex_capacity,
    hex_distance,
    local_exposure_angle,
    logistic,
    neighbors,
)


# ---------------------------------------------------------------------------
# Material parameters and state
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MaterialParams:
    """Matches the canonical archive's frozen values exactly:
    `write_probability=0.20`, `modified_neighbor_gain=0.30`."""

    write_probability: float = 0.20
    modified_neighbor_gain: float = 0.30


@dataclass
class MaterialCrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    modified: Set[Cell]
    step: int
    stream_seed: int
    attachments_by_step: List[int] = field(default_factory=lambda: [1])
    population_by_step: List[int] = field(default_factory=lambda: [1])
    modified_count_by_step: List[int] = field(default_factory=lambda: [0])


def initial_material_state(stream_seed: int) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        modified=set(),
        step=0,
        stream_seed=int(stream_seed),
        attachments_by_step=[1],
        population_by_step=[1],
        modified_count_by_step=[0],
    )


def clone_material_state(state: MaterialCrystalState) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def erase_material_labels(state: MaterialCrystalState) -> MaterialCrystalState:
    """Causal ablation: preserve visible morphology, birth times, step and stream
    seed while deleting only the experimental material state -- the "erase the
    modified labels while leaving the visible occupied geometry exactly as it
    is" intervention Chapter 9 uses throughout."""
    out = clone_material_state(state)
    out.modified = set()
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = 0
    return out


def boundary_cells(occupied: Set[Cell]) -> List[Cell]:
    """Occupied cells with fewer than 6 occupied neighbours (degree < 6)."""
    return [c for c in sorted(occupied) if sum(nb in occupied for nb in neighbors(c)) < 6]


def capacity_fraction_occupied(occupied: Set[Cell], radius: int) -> float:
    return len(occupied) / float(hex_capacity(radius))


# ---------------------------------------------------------------------------
# Keyed random channels (each namespace is a separate stream, never mixed)
# ---------------------------------------------------------------------------


def _keyed_uniform(namespace: str, seed: int, step: int, cell: Cell) -> float:
    q, r = cell
    payload = f"{namespace}:{int(seed)}:{int(step)}:{int(q)}:{int(r)}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def material_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """Separate deterministic channel for the pulse write decision -- cannot
    correlate with or consume the growth CRN stream."""
    return _keyed_uniform("material", stream_seed, step, cell)


def transmission_rank_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """Separate deterministic channel used only to break ties in the
    equal-budget placement-policy ranking."""
    return _keyed_uniform("transmission-uniform", stream_seed, step, cell)


# ---------------------------------------------------------------------------
# Material-aware attachment probability and growth step
# ---------------------------------------------------------------------------


def material_attachment_probability(
    cell: Cell,
    occupied: Set[Cell],
    modified: Set[Cell],
    input_value: float,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> float:
    """Frozen v1 attachment score plus one additional term:
    `modified_neighbor_gain * modified_n`, where `modified_n` is the count of
    `cell`'s occupied neighbours that are currently MODIFIED. Identical to
    `digital_crystal.attachment_probability` when `modified` is empty."""
    n = sum(nb in occupied for nb in neighbors(cell))
    modified_n = sum(nb in modified for nb in neighbors(cell))
    theta = local_exposure_angle(cell, occupied)
    phase = crystal_params.signal_phase_gain * float(input_value)
    anisotropy = math.cos(6.0 * theta + phase)
    crowding = max(0, n - 2)
    score = (
        crystal_params.base_bias
        + crystal_params.neighbor_gain * n
        + crystal_params.signal_rate_gain * float(input_value)
        + crystal_params.anisotropy_gain * anisotropy
        - crystal_params.crowding_penalty * crowding
        + material_params.modified_neighbor_gain * modified_n
    )
    return logistic(score)


def grow_one_step_without_transmission(
    state: MaterialCrystalState,
    input_value: float,
    pulse_bit: int,
    max_radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> Tuple[MaterialCrystalState, List[Cell], int]:
    """Growth phase only (mirrors `ch18_v7.grow_one_step_without_transmission`):
    ordinary CRN-coupled attachment using `material_attachment_probability`,
    then (if `pulse_bit`) an independent pulse write of new MODIFIED labels
    onto already-occupied boundary cells. Deliberately does NOT propagate
    modification onto newly-attached cells -- that is a separate, explicit
    step (`choose_targets_with_exact_budget`) so multiple branches can grow
    first and then share one exact matched propagation budget."""
    occupied_before = set(state.occupied)
    modified_before = set(state.modified)
    birth_time = dict(state.birth_time)

    candidates = sorted(frontier(occupied_before, max_radius))
    next_step = state.step + 1
    additions: List[Cell] = []
    for cell in candidates:
        p = material_attachment_probability(
            cell, occupied_before, modified_before, input_value, crystal_params, material_params
        )
        if cell_keyed_uniform(state.stream_seed, next_step, cell) < p:
            additions.append(cell)

    occupied = set(occupied_before)
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    modified = set(modified_before)
    newly_modified = 0
    if int(pulse_bit) != 0:
        for cell in boundary_cells(occupied):
            if cell in modified:
                continue
            if material_uniform(state.stream_seed, next_step, cell) < material_params.write_probability:
                modified.add(cell)
                newly_modified += 1

    out = MaterialCrystalState(
        occupied=occupied,
        birth_time=birth_time,
        modified=modified,
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
        modified_count_by_step=state.modified_count_by_step + [len(modified)],
    )
    return out, additions, newly_modified


def advance_one_step_material(
    state: MaterialCrystalState,
    input_value: float,
    pulse_bit: int,
    max_radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> Tuple[MaterialCrystalState, int, int]:
    """One full update: growth + pulse write, no propagation. Mirrors
    `ch18_v1.advance_one_step_material` -- the mechanism used for the
    write-and-persist / erase-ablation / causal-chain-audit experiments,
    where modified state never spreads beyond wherever the pulse wrote it."""
    out, additions, newly_modified = grow_one_step_without_transmission(
        state, input_value, pulse_bit, max_radius, crystal_params, material_params
    )
    return out, len(additions), newly_modified


def make_environment(steps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)
    p1 = rng.uniform(11.0, 19.0)
    p2 = rng.uniform(23.0, 37.0)
    ph1 = rng.uniform(0.0, 2 * np.pi)
    ph2 = rng.uniform(0.0, 2 * np.pi)
    deterministic = 0.55 * np.sin(2 * np.pi * t / p1 + ph1) + 0.25 * np.sin(2 * np.pi * t / p2 + ph2)
    drift_raw = np.cumsum(rng.normal(0.0, 0.10, size=steps))
    peak = np.max(np.abs(drift_raw)) if steps else 1.0
    drift = 0.18 * (drift_raw / peak if peak > 1e-12 else drift_raw)
    noise = rng.normal(0.0, 0.08, size=steps)
    combined = deterministic + drift + noise
    peak2 = np.max(np.abs(combined)) if steps else 1.0
    return combined / peak2 if peak2 > 1e-12 else combined


def warm_material_checkpoint(
    env: np.ndarray,
    warmup_steps: int,
    seed: int,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> MaterialCrystalState:
    """Grow an ordinary (no-pulse) checkpoint -- matches
    `ch18_v1.warm_material_checkpoint`."""
    state = initial_material_state(seed)
    no_material = MaterialParams(write_probability=0.0, modified_neighbor_gain=0.0)
    for t in range(warmup_steps):
        state, _, _ = advance_one_step_material(
            state, float(env[t]), 0, radius, crystal_params, no_material
        )
    return state


# ---------------------------------------------------------------------------
# Frontier-contact / causal-aperture diagnostics
# ---------------------------------------------------------------------------


def aperture_metrics(state: MaterialCrystalState, radius: int) -> dict:
    """Mirrors `ch19_v2.aperture_metrics`: how much of the *current* active
    frontier is adjacent to at least one MODIFIED cell."""
    fr = frontier(state.occupied, radius)
    if not fr:
        return {"frontier_count": 0, "contact_count": 0, "contact_fraction": 0.0,
                "modified_count": len(state.modified)}
    contact = sum(any(nb in state.modified for nb in neighbors(cell)) for cell in fr)
    return {
        "frontier_count": len(fr),
        "contact_count": int(contact),
        "contact_fraction": float(contact) / len(fr),
        "modified_count": len(state.modified),
    }


def modified_orientation_summary(state: MaterialCrystalState) -> dict:
    """Secondary diagnostic (mirrors `ch19_v2.modified_orientation_summary`):
    circular mean angle of MODIFIED cells relative to the seed. Not
    interpreted as a wave, phase code, or representation -- purely a spatial
    organization descriptor used to confirm two directional histories remain
    distinguishable."""
    if not state.modified:
        return {"n": 0, "mean_cos": 0.0, "mean_sin": 0.0, "resultant_length": 0.0, "mean_angle": 0.0}
    angles = []
    for cell in state.modified:
        q, r = cell
        x = math.sqrt(3.0) * (q + r / 2.0)
        y = 1.5 * r
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


def angular_distance(a: float, b: float) -> float:
    d = (a - b + math.pi) % (2.0 * math.pi) - math.pi
    return abs(d)


def directional_write(
    state: MaterialCrystalState, target_angle: float, write_fraction: float
) -> Tuple[MaterialCrystalState, List[Cell]]:
    """Write the SAME MODIFIED state to a directional subset of the active
    boundary, ranked by angular closeness to `target_angle` (ties broken by
    the material-write keyed stream). Mirrors `ch19_v2.directional_write` --
    there is no A/B state identity anywhere in the substrate, only where the
    same mark is written."""
    candidates = boundary_cells(state.occupied)
    if not candidates:
        raise RuntimeError("No boundary cells available for directional write.")
    k = max(1, min(len(candidates), int(round(float(write_fraction) * len(candidates)))))
    ranked = sorted(
        candidates,
        key=lambda c: (
            angular_distance(local_exposure_angle(c, state.occupied), target_angle),
            material_uniform(state.stream_seed, state.step + 1, c),
            c,
        ),
    )
    selected = ranked[:k]
    out = clone_material_state(state)
    out.modified.update(selected)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = len(out.modified)
    return out, selected


# ---------------------------------------------------------------------------
# Exact-matched-budget placement policies (interior / random / surface)
# ---------------------------------------------------------------------------


def eligible_transmission_targets(additions: Sequence[Cell], modified_before: Set[Cell]) -> List[Cell]:
    """Newly-attached cells adjacent to at least one already-MODIFIED cell --
    the only cells eligible to inherit the mark this step."""
    return [c for c in additions if any(nb in modified_before for nb in neighbors(c))]


def surface_exposure_after_attachment(cell: Cell, occupied_after: Set[Cell]) -> int:
    """Count of `cell`'s empty neighbours once this step's attachments are
    applied. Larger = more exposed / surface-like; smaller = more interior."""
    return sum(nb not in occupied_after for nb in neighbors(cell))


def shared_transmission_budget(eligible_counts: Sequence[int], transmission_fraction: float) -> int:
    """One exact common propagation budget shared by every synchronized
    branch this step -- the smallest eligible count times `transmission_fraction`,
    so no branch is ever allowed to transmit more than another."""
    if not eligible_counts:
        return 0
    base = min(int(x) for x in eligible_counts)
    k = int(round(float(transmission_fraction) * base))
    return max(0, min(base, k))


def choose_targets_with_exact_budget(
    eligible: Sequence[Cell],
    occupied_after: Set[Cell],
    stream_seed: int,
    step: int,
    budget: int,
    policy: str,
) -> Tuple[List[Cell], dict]:
    """Choose exactly `budget` cells from `eligible`. Policies differ only in
    spatial allocation (mirrors `ch18_v7.choose_targets_with_exact_budget`):

        surface_biased    prefer cells with MORE post-attachment exposure
        interior_biased   prefer cells with LESS post-attachment exposure
        random_matched    no exposure preference, keyed-uniform order only
    """
    eligible = list(eligible)
    n = len(eligible)
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    if budget > n:
        raise ValueError(f"budget={budget} exceeds eligible_count={n} for policy={policy}")

    if budget == 0:
        selected: List[Cell] = []
    elif policy == "random_matched":
        selected = sorted(eligible, key=lambda c: (transmission_rank_uniform(stream_seed, step, c), c))[:budget]
    elif policy == "surface_biased":
        selected = sorted(
            eligible,
            key=lambda c: (-surface_exposure_after_attachment(c, occupied_after),
                            transmission_rank_uniform(stream_seed, step, c), c),
        )[:budget]
    elif policy == "interior_biased":
        selected = sorted(
            eligible,
            key=lambda c: (surface_exposure_after_attachment(c, occupied_after),
                            transmission_rank_uniform(stream_seed, step, c), c),
        )[:budget]
    else:
        raise ValueError(f"Unknown matched-budget policy: {policy!r}")

    eligible_surface = [surface_exposure_after_attachment(c, occupied_after) for c in eligible]
    selected_surface = [surface_exposure_after_attachment(c, occupied_after) for c in selected]
    return selected, {
        "eligible_count": int(n),
        "budget": int(budget),
        "selected_count": int(len(selected)),
        "mean_eligible_surface_exposure": float(np.mean(eligible_surface)) if eligible_surface else 0.0,
        "mean_selected_surface_exposure": float(np.mean(selected_surface)) if selected_surface else 0.0,
    }


def matched_placement_step(
    state: MaterialCrystalState,
    input_value: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    transmission_fraction: float,
    policy: str,
) -> Tuple[MaterialCrystalState, dict]:
    """Grow one ordinary step, then propagate MODIFIED state onto newly
    attached cells under a fixed policy, using a budget computed from THIS
    branch's own eligible count (single-branch convenience wrapper; the
    matched multi-branch version calls `shared_transmission_budget` across
    all branches' eligible counts before calling `choose_targets_with_exact_budget`).
    """
    before_modified = set(state.modified)
    grown, additions, _ = grow_one_step_without_transmission(
        state, input_value, 0, radius, crystal_params, material_params
    )
    eligible = eligible_transmission_targets(additions, before_modified)
    budget = shared_transmission_budget([len(eligible)], transmission_fraction)
    selected, meta = choose_targets_with_exact_budget(
        eligible, grown.occupied, grown.stream_seed, grown.step, budget, policy
    )
    out = clone_material_state(grown)
    out.modified.update(selected)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = len(out.modified)
    return out, meta


# ---------------------------------------------------------------------------
# Causal-chain audit: probability delta and realized attachment flips
# ---------------------------------------------------------------------------


def material_delta_p(
    cell: Cell,
    occupied: Set[Cell],
    modified: Set[Cell],
    input_value: float,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> float:
    """Delta-p at one candidate site: attachment probability WITH the material
    term present minus WITHOUT it (material set forced empty). Mirrors the
    "for every candidate site at the frontier we can compute its attachment
    probability with the material effect and without it" audit."""
    with_material = material_attachment_probability(
        cell, occupied, modified, input_value, crystal_params, material_params
    )
    without_material = material_attachment_probability(
        cell, occupied, set(), input_value, crystal_params, material_params
    )
    return with_material - without_material


def realized_material_flips(
    occupied: Set[Cell],
    modified: Set[Cell],
    input_value: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    stream_seed: int,
    step: int,
) -> dict:
    """Counterfactual audit over every frontier candidate this step: does the
    SAME coin flip (from `cell_keyed_uniform`, shared by construction between
    the with-material and without-material comparison) land on opposite sides
    of `with_material` vs `without_material`'s attachment probability? That is
    a realized causal flip -- the point where a probability shift becomes a
    difference in what gets built."""
    candidates = sorted(frontier(occupied, radius))
    next_step = step + 1
    sum_delta_p = 0.0
    flips = 0
    for cell in candidates:
        p_with = material_attachment_probability(cell, occupied, modified, input_value, crystal_params, material_params)
        p_without = material_attachment_probability(cell, occupied, set(), input_value, crystal_params, material_params)
        sum_delta_p += p_with - p_without
        u = cell_keyed_uniform(stream_seed, next_step, cell)
        if (u < p_with) != (u < p_without):
            flips += 1
    return {"n_candidates": len(candidates), "sum_delta_p": sum_delta_p, "realized_flips": flips}
