"""Decaying material-history extension for the Digital Crystal substrate.

Adds exactly one new state channel on top of `_shared/digital_crystal.py`'s
frozen growth mechanics: a per-occupied-cell scalar `material_strength` that
starts at some initial value when written and halves every `history_half_life`
updates (a decaying trace, not a persistent flag). It contributes to a
frontier candidate's attachment score through a `material_exposure` term --
the sum of *occupied neighbours'* material strength -- exactly matching
`scripts/books/digital-life/ch27_digital_crystal_decaying_material_history_causal_response_v1.py`'s
`attachment_score` (see that script's `MATERIAL_GAIN`, `attachment_score`,
`decay_material`). New cells that attach inherit **no** material state --
this channel is write-only and non-propagating, so any effect it has on a
distant future must route through the visible occupied/empty morphology it
leaves behind, not through the trace itself spreading.

Named `crystal_history.py` (not `crystal_material.py`) to avoid colliding
with Chapter 9's unrelated MODIFIED-cell material-state module of that name
-- the two chapters model materially different mechanisms (a discrete,
persistent MODIFIED flag for Ch.9 vs. a continuous, exponentially decaying
scalar trace here for Ch.15) and are not meant to share a module.

This module deliberately builds directly on `digital_crystal.py` and reuses
`crystal_causal.py`'s `local_population` helper rather than duplicating it --
only the material-aware score computation, decay step, and CRN-coupled growth
step are new.

Update order within one step (matches the canonical script's `canonical_step`
exactly): GROWTH (using the *current*, not-yet-decayed material state) then
DECAY (material ages by one update, for the *next* step's exposure term).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Sequence, Set, Tuple

from digital_crystal import (
    Cell,
    CrystalParams,
    cell_keyed_uniform,
    frontier,
    local_exposure_angle,
    logistic,
    neighbors,
)

MATERIAL_GAIN = 0.30
HISTORY_HALF_LIFE = 6.0


def decay_factor(half_life: float = HISTORY_HALF_LIFE) -> float:
    return float(2.0 ** (-1.0 / half_life))


def initial_strength(age: float, half_life: float = HISTORY_HALF_LIFE) -> float:
    """A trace written `age` updates ago, already decayed that far: 2^(-age/half_life)."""
    return float(2.0 ** (-age / half_life))


def material_exposure(cell: Cell, occupied: Set[Cell], material_strength: Dict[Cell, float]) -> float:
    return float(sum(material_strength.get(nb, 0.0) for nb in neighbors(cell) if nb in occupied))


def material_score(
    cell: Cell,
    occupied: Set[Cell],
    material_strength: Dict[Cell, float],
    input_value: float,
    params: CrystalParams,
    material_gain: float = MATERIAL_GAIN,
) -> float:
    n = sum(nb in occupied for nb in neighbors(cell))
    theta = local_exposure_angle(cell, occupied)
    phase = params.signal_phase_gain * float(input_value)
    anisotropy = math.cos(6.0 * theta + phase)
    crowding = max(0, n - 2)
    return (
        params.base_bias
        + params.neighbor_gain * n
        + params.signal_rate_gain * float(input_value)
        + params.anisotropy_gain * anisotropy
        - params.crowding_penalty * crowding
        + material_gain * material_exposure(cell, occupied, material_strength)
    )


def material_attachment_probability(
    cell: Cell,
    occupied: Set[Cell],
    material_strength: Dict[Cell, float],
    input_value: float,
    params: CrystalParams,
    material_gain: float = MATERIAL_GAIN,
) -> float:
    return logistic(material_score(cell, occupied, material_strength, input_value, params, material_gain))


def decay_material(
    material_strength: Dict[Cell, float], occupied: Set[Cell], half_life: float = HISTORY_HALF_LIFE, floor: float = 1e-12
) -> Dict[Cell, float]:
    factor = decay_factor(half_life)
    out: Dict[Cell, float] = {}
    for cell, strength in material_strength.items():
        if cell not in occupied:
            continue
        v = strength * factor
        if v > floor:
            out[cell] = v
    return out


def material_mass(material_strength: Dict[Cell, float]) -> float:
    return float(sum(max(0.0, v) for v in material_strength.values()))


def crn_step_material(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    material_strength: Dict[Cell, float],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    *,
    material_gain: float = MATERIAL_GAIN,
    half_life: float = HISTORY_HALF_LIFE,
    forced: Sequence[Cell] = (),
    excluded: Sequence[Cell] = (),
) -> Tuple[Set[Cell], Dict[Cell, int], Dict[Cell, float], int]:
    """One material-aware growth update: CRN-coupled coin flips (as
    `crystal_causal.crn_step`), using `material_attachment_probability`
    instead of the base rule's `attachment_probability`, followed by
    decaying the (unchanged-this-step) material trace for the next update.
    `forced`/`excluded` behave exactly as in `crystal_causal.crn_step`.
    """
    forced_set = set(forced)
    excluded_set = set(excluded)
    candidates = sorted(frontier(occupied, radius))
    new_occupied = set(occupied)
    new_birth_time = dict(birth_time)
    next_step = step + 1
    additions = 0
    for cell in candidates:
        if cell in excluded_set:
            continue
        if cell in forced_set:
            attach = True
        else:
            u = cell_keyed_uniform(seed, next_step, cell)
            p = material_attachment_probability(cell, occupied, material_strength, input_value, params, material_gain)
            attach = u < p
        if attach:
            new_occupied.add(cell)
            new_birth_time[cell] = next_step
            additions += 1
    new_material = decay_material(material_strength, new_occupied, half_life)
    return new_occupied, new_birth_time, new_material, additions


def naive_unblocked_step_material(occupied, birth_time, material_strength, step, input_value, radius, params, seed, **kw):
    """Deliberately reproduces original book Chapter 27 V1's construct-validity
    bug for teaching purposes: an ordinary CRN step with NO special handling
    of `x` at all -- `x` is just another frontier candidate, free to attach
    on its own ordinary coin flip. If this is used as the "PREVENT" arm's
    lag-1 step (instead of `prevent_transient_material`'s explicit exclusion),
    x can "naturally reacquire" the target cell during the very update meant
    to withhold it -- and because accessible material raises baseline
    attachment probability generally, x's own reacquisition rate is *not*
    independent of the treatment arm, contaminating the PREVENT branch
    correlated with ACCESSIBLE vs REMOTE/ERASED. See
    `research/digital-life/ch27-v1-construct-validity-audit`.
    """
    return crn_step_material(occupied, birth_time, material_strength, step, input_value, radius, params, seed, **kw)


@dataclass
class MaterialCausalBranches:
    prevent_occupied: Set[Cell]
    prevent_birth_time: Dict[Cell, int]
    prevent_material: Dict[Cell, float]
    transient_occupied: Set[Cell]
    transient_birth_time: Dict[Cell, int]
    transient_material: Dict[Cell, float]
    step: int
    x: Cell
    force_present_at_exposure: bool
    prevent_blocked_at_exposure: bool
    equalized_after_exposure: bool


def prevent_transient_material(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    material_strength: Dict[Cell, float],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    x: Cell,
    *,
    material_gain: float = MATERIAL_GAIN,
    half_life: float = HISTORY_HALF_LIFE,
) -> MaterialCausalBranches:
    """The corrected (V2-style) single controlled causal exposure: x is
    forced occupied for exactly the lag-1 update (TRANSIENT: one causal
    update as an occupied neighbour, then explicitly removed) and compared
    to PREVENT (x explicitly excluded at lag 1, never inserted). Both
    branches share `seed`, so any candidate legal in both branches gets the
    identical CRN draw. Mirrors `crystal_causal.force_prevent_retained_transient`,
    restricted to the two arms Chapter 27/15 actually uses (no RETAINED arm)
    and threading `material_strength` through.
    """
    force_occ = set(occupied) | {x}
    force_bt = dict(birth_time)
    force_bt.setdefault(x, step)

    prevent_before = set(occupied) - {x}
    prevent_bt_before = {k: v for k, v in birth_time.items() if k != x}

    tra_occ, tra_bt, tra_mat, _ = crn_step_material(
        force_occ, force_bt, material_strength, step, input_value, radius, params, seed,
        material_gain=material_gain, half_life=half_life,
    )
    pre_occ, pre_bt, pre_mat, _ = crn_step_material(
        prevent_before, prevent_bt_before, material_strength, step, input_value, radius, params, seed,
        material_gain=material_gain, half_life=half_life, excluded=[x],
    )

    force_present = x in tra_occ
    prevent_blocked = x not in pre_occ

    tra_occ = set(tra_occ)
    tra_occ.discard(x)
    tra_bt = dict(tra_bt)
    tra_bt.pop(x, None)

    equalized = (x not in tra_occ) and (x not in pre_occ)

    return MaterialCausalBranches(
        prevent_occupied=pre_occ,
        prevent_birth_time=pre_bt,
        prevent_material=pre_mat,
        transient_occupied=tra_occ,
        transient_birth_time=tra_bt,
        transient_material=tra_mat,
        step=step + 1,
        x=x,
        force_present_at_exposure=force_present,
        prevent_blocked_at_exposure=prevent_blocked,
        equalized_after_exposure=equalized,
    )


def run_material_causal_horizon(
    branches: MaterialCausalBranches,
    env: Sequence[float],
    radius: int,
    params: CrystalParams,
    seed: int,
    horizon: int,
    *,
    local_radius: int,
    material_gain: float = MATERIAL_GAIN,
    half_life: float = HISTORY_HALF_LIFE,
) -> Dict[str, object]:
    """Advance PREVENT / TRANSIENT for `horizon` total updates (lag 1 already
    applied in `branches`), measuring the local population difference
    (TRANSIENT - PREVENT), x excluded throughout, restricted to `local_radius`
    -- the same idiom as `crystal_causal.run_causal_horizon`."""
    from crystal_causal import local_population
    import numpy as np

    def pop_excluding_x(occ: Set[Cell]) -> int:
        return local_population(occ, branches.x, local_radius)

    pre_occ, pre_bt, pre_mat = set(branches.prevent_occupied), dict(branches.prevent_birth_time), dict(branches.prevent_material)
    tra_occ, tra_bt, tra_mat = set(branches.transient_occupied), dict(branches.transient_birth_time), dict(branches.transient_material)
    step = branches.step

    pre_pop = [pop_excluding_x(pre_occ)]
    tra_pop = [pop_excluding_x(tra_occ)]
    pre_mass = [material_mass(pre_mat)]
    tra_mass = [material_mass(tra_mat)]

    remaining = max(0, horizon - 1)
    for j in range(remaining):
        value = float(env[j])
        pre_occ, pre_bt, pre_mat, _ = crn_step_material(
            pre_occ, pre_bt, pre_mat, step, value, radius, params, seed, material_gain=material_gain, half_life=half_life
        )
        tra_occ, tra_bt, tra_mat, _ = crn_step_material(
            tra_occ, tra_bt, tra_mat, step, value, radius, params, seed, material_gain=material_gain, half_life=half_life
        )
        step += 1
        pre_pop.append(pop_excluding_x(pre_occ))
        tra_pop.append(pop_excluding_x(tra_occ))
        pre_mass.append(material_mass(pre_mat))
        tra_mass.append(material_mass(tra_mat))

    pre_pop_a = np.array(pre_pop, dtype=float)
    tra_pop_a = np.array(tra_pop, dtype=float)
    lag_gain = tra_pop_a - pre_pop_a
    return {
        "prevent_population": pre_pop_a,
        "transient_population": tra_pop_a,
        "lag_gain": lag_gain,
        "cumulative_gain": np.cumsum(lag_gain),
        "G": float(np.sum(lag_gain)),
        "transient_material_mass": np.array(tra_mass, dtype=float),
        "prevent_material_mass": np.array(pre_mass, dtype=float),
    }
