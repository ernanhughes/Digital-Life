"""Causal-intervention extension for the Digital Crystal substrate.

Implements the FORCE / PREVENT / RETAINED / TRANSIENT causal-decomposition
idiom that original book Chapter 23 ("What Does One Attachment Cause?")
introduced and that the current book's Chapters 13-16 all reuse:

  FORCE     a target frontier cell `x` is forced to attach on the next
            update, bypassing its stochastic attachment probability.
  PREVENT   `x` is explicitly excluded from the candidate list on that
            update, so it cannot attach even if its coin flip would have
            succeeded.
  TRANSIENT `x` is forced to attach, gets exactly one full causal update as
            an occupied neighbour, and is then explicitly removed. Any
            divergence from PREVENT after that point must be carried by
            consequences already created downstream, not by the continued
            presence of `x`.
  RETAINED  `x` is forced to attach and is simply left alone -- not
            clamped occupied, just not experimentally removed. Its later
            fate follows ordinary dynamics (it can be lost and reoccupied
            exactly like any other cell, if a loss rule is present).

This module is built entirely on top of `digital_crystal.py`'s frozen
growth mechanics (`frontier`, `attachment_probability`, `neighbors`,
`cell_keyed_uniform`) and does not modify that module. It reuses
`crystal_loss.py`'s `make_environment` / `warm_checkpoint` helpers for
generating the forcing signal and growing an ordinary warmup checkpoint,
rather than duplicating that logic.

Deliberate scope simplification: the canonical terminal experiment
(`research/digital-life/ch23-retained-transient-causal-gain-v5/`) layered
this same FORCE/PREVENT/RETAINED/TRANSIENT mechanism on top of *both*
Chapter 10's material-loss rule *and* Chapter 11's finite-evaluation-budget
candidate selector. This module intentionally omits both -- it operates
directly on the plain `digital-crystal-v1-frozen` substrate. Reoccupation
of `x` after removal (TRANSIENT) or continued exposure to ordinary dynamics
(RETAINED) therefore comes entirely from the base stochastic growth rule,
not from an explicit loss-then-regrowth cycle. This is disclosed wherever
this module's numbers are compared against the canonical archive.

CRN coupling
------------
`digital_crystal.advance_one_step` draws attachment coin-flips from a
*stateful, sequential* `random.Random` stream: each candidate consumes the
next draw in sorted order. That is fine for growing a single, unperturbed
trajectory, but it is the wrong tool for comparing branches that differ in
which cells are candidates (e.g. PREVENT excludes `x`): removing one
candidate from the sorted list shifts which draw every subsequent candidate
receives, so branches would diverge for a purely bookkeeping reason having
nothing to do with the intervention. (This is exactly the artifact Chapter 8
documents as DL-08-C06, "sequential-RNG-coupling is a major measurement
artifact", fixed there via a cell-keyed CRN runner.)

`crn_step` below fixes this the same way: every candidate's attach decision
is drawn from `cell_keyed_uniform(seed, next_step, cell)`, a value that
depends only on (seed, step, cell), never on what else is being evaluated
that step or in what order. Two branches sharing the same `seed` therefore
give every *shared* candidate cell the identical draw at the identical step,
so any difference in outcome is attributable to the intervention itself
(which cells are occupied, forced, or excluded), not to independently-
sampled luck. This "common random numbers" (CRN) idiom is used throughout
this module and is intended for reuse by Chapters 14-16.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

import numpy as np

from digital_crystal import (
    Cell,
    CrystalParams,
    attachment_probability,
    cell_keyed_uniform,
    frontier,
    neighbors,
)

# Re-exported for convenience so notebooks only need to import this module
# for the causal-intervention machinery plus environment/checkpoint setup.
from crystal_loss import make_environment, warm_checkpoint  # noqa: F401


# ---------------------------------------------------------------------------
# Core CRN-coupled growth step
# ---------------------------------------------------------------------------


def crn_step(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    *,
    forced: Sequence[Cell] = (),
    excluded: Sequence[Cell] = (),
) -> Tuple[Set[Cell], Dict[Cell, int], int]:
    """One growth update using cell-keyed common random numbers instead of the
    base module's stateful sequential RNG.

    Every frontier candidate's attach/no-attach decision comes from
    ``cell_keyed_uniform(seed, step + 1, cell) < attachment_probability(...)``,
    except:

    - cells in ``forced`` attach unconditionally (bypasses the coin flip
      entirely -- this is the FORCE intervention);
    - cells in ``excluded`` never attach this update, regardless of their
      coin flip (this is the PREVENT intervention).

    Attachment probabilities are computed from ``occupied`` (the state
    *before* this update), matching ``digital_crystal.advance_one_step``'s
    simultaneous-evaluation semantics: an attachment decided this step does
    not itself change any other candidate's probability within the same
    step.

    Parameters
    ----------
    occupied, birth_time : the state to advance from.
    step : the *current* step count (the returned state has step + 1).
    input_value : the forcing signal value used for this update.
    radius : maximum hex distance from the origin a candidate may occupy.
    params : CrystalParams (the frozen v1 growth-rule parameters).
    seed : the CRN seed. Two calls sharing the same seed and step give every
        shared candidate cell an identical draw.
    forced, excluded : cells to force-attach / block, respectively. A cell
        should not appear in both.

    Returns
    -------
    (new_occupied, new_birth_time, additions) where additions is the number
    of cells newly attached this update.
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
            p = attachment_probability(cell, occupied, input_value, params)
            attach = u < p
        if attach:
            new_occupied.add(cell)
            new_birth_time[cell] = next_step
            additions += 1
    return new_occupied, new_birth_time, additions


def run_crn_horizon(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    env: Sequence[float],
    radius: int,
    params: CrystalParams,
    seed: int,
) -> Tuple[Set[Cell], Dict[Cell, int], int, List[int]]:
    """Advance a single branch through ``len(env)`` ordinary CRN-coupled updates.

    No cell is forced or excluded here -- this is for growing a common
    checkpoint, or for continuing a branch through "ordinary dynamics" once
    an intervention's special handling window has ended. Returns
    (occupied, birth_time, step, population_trajectory).
    """
    pops = [len(occupied)]
    for value in env:
        occupied, birth_time, _ = crn_step(occupied, birth_time, step, float(value), radius, params, seed)
        step += 1
        pops.append(len(occupied))
    return occupied, birth_time, step, pops


# ---------------------------------------------------------------------------
# One-step FORCE / PREVENT primitive and mechanical-match diagnostics
# ---------------------------------------------------------------------------


def force_branch_step(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    x: Cell,
) -> Tuple[Set[Cell], Dict[Cell, int], int]:
    """FORCE: `x` is inserted as occupied *before* this update is evaluated, so it acts
    as a genuine occupied neighbour for this same update's frontier and
    attachment-probability computations -- matching the book's "x inserted as occupied
    at the checkpoint" design (`force_prevent_retained_transient` uses the identical
    approach for RETAINED/TRANSIENT).

    Note this is deliberately *not* implemented as ``crn_step(..., forced=[x])``: that
    would only make `x` itself attach unconditionally while leaving the candidate set
    for this step computed from the *pre-x* occupied set, so `x`'s other empty
    neighbours (candidates only because `x` is now occupied) would never even be
    evaluated this update. Pre-inserting `x` is what lets its neighbours be legal
    candidates and feel its support within the same causal exposure.
    """
    occ = set(occupied) | {x}
    bt = dict(birth_time)
    bt.setdefault(x, step)
    return crn_step(occ, bt, step, input_value, radius, params, seed)


def prevent_branch_step(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    x: Cell,
) -> Tuple[Set[Cell], Dict[Cell, int], int]:
    """PREVENT: `x` is excluded from the candidate list on the next update, so it
    cannot attach even if `cell_keyed_uniform(...) < attachment_probability(...)`
    would otherwise have been true."""
    return crn_step(occupied, birth_time, step, input_value, radius, params, seed, excluded=[x])


def mechanical_gain_g1(
    occupied: Set[Cell],
    input_value: float,
    params: CrystalParams,
    radius: int,
    x: Cell,
) -> float:
    """g_mech_1: the frozen rule's *mechanically expected* neighbouring construction
    difference at lag one -- summed, over every "affected neighbouring candidate" of
    `x`, of P(attach | x occupied) - P(attach | x empty), computed directly from
    probabilities before any Bernoulli draw is taken. Excludes `x` itself, matching
    the book's "measure everything except x" design.

    "Affected neighbouring candidate" means a cell that is already a legal frontier
    candidate of `occupied` alone (i.e. has at least one occupied neighbour besides
    `x`) -- so it would actually be evaluated in *both* the FORCE and PREVENT
    branches. A cell adjacent only to `x` is not a candidate at all under
    `digital_crystal.frontier()`'s adjacency-gated candidacy rule unless `x` is
    occupied, so it has no well-defined "PREVENT-branch probability" to compare
    against; including it would systematically inflate `p_prevent` above its
    physically realizable value (0, since such a cell is never evaluated in the
    PREVENT branch) and bias g_mech_1 below the realized g1 it is meant to predict.
    """
    force_occ = set(occupied) | {x}
    prevent_candidates = frontier(occupied, radius)
    total = 0.0
    for nb in neighbors(x):
        if nb not in prevent_candidates:
            continue
        p_force = attachment_probability(nb, force_occ, input_value, params)
        p_prevent = attachment_probability(nb, occupied, input_value, params)
        total += p_force - p_prevent
    return total


def realized_gain_g1(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    x: Cell,
) -> float:
    """g1: the *realized* neighbouring construction difference at lag one -- the
    count of x's "affected neighbouring candidates" (see `mechanical_gain_g1`) that
    attach in the FORCE branch minus the count that attach in the CRN-matched
    PREVENT branch, excluding x itself.
    """
    force_occ, _, _ = force_branch_step(occupied, birth_time, step, input_value, radius, params, seed, x)
    prevent_occ, _, _ = prevent_branch_step(occupied, birth_time, step, input_value, radius, params, seed, x)
    prevent_candidates = frontier(occupied, radius)
    affected = [nb for nb in neighbors(x) if nb in prevent_candidates]
    force_count = sum(1 for c in affected if c in force_occ)
    prevent_count = sum(1 for c in affected if c in prevent_occ)
    return float(force_count - prevent_count)


# ---------------------------------------------------------------------------
# Three-branch PREVENT / TRANSIENT / RETAINED decomposition
# ---------------------------------------------------------------------------


@dataclass
class CausalBranches:
    """The three post-intervention branches immediately after the single
    controlled causal exposure (lag 1), sharing one checkpoint and one CRN seed.
    """

    prevent_occupied: Set[Cell]
    prevent_birth_time: Dict[Cell, int]
    transient_occupied: Set[Cell]
    transient_birth_time: Dict[Cell, int]
    retained_occupied: Set[Cell]
    retained_birth_time: Dict[Cell, int]
    step: int
    x: Cell
    force_present_at_exposure: bool
    prevent_blocked_at_exposure: bool
    equalized_after_exposure: bool


def force_prevent_retained_transient(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    x: Cell,
) -> CausalBranches:
    """Build PREVENT / TRANSIENT / RETAINED from one shared checkpoint, delivering
    the single controlled causal exposure at lag 1.

    - RETAINED, TRANSIENT: `x` is inserted as occupied *before* the lag-1 update
      (so it acts as an occupied neighbour during that update) -- "x inserted as
      occupied at the checkpoint, no loss step before the exposure."
    - PREVENT: `x` is excluded from the frontier during the lag-1 update, so it
      cannot attach.

    All three branches share `seed`, so every candidate cell other than `x`
    that is a legal candidate in more than one branch receives the identical
    CRN draw in each -- differences in what attaches are attributable to the
    intervention, not to independent luck.

    Immediately after the lag-1 update, `x` is deleted from TRANSIENT (the
    "one full causal update, then removed" control) and its absence in
    PREVENT is (re)asserted. RETAINED keeps `x` and is not touched again by
    this function -- its later fate is ordinary dynamics, handled by
    `run_causal_horizon`.

    The three `..._at_exposure` / `equalized_after_exposure` flags on the
    returned `CausalBranches` are validity assertions, not measurements --
    they should be True on every probe; the notebook should assert this
    across the whole run rather than merely printing it.
    """
    force_occ = set(occupied) | {x}
    force_bt = dict(birth_time)
    force_bt.setdefault(x, step)

    prevent_before = set(occupied) - {x}
    prevent_bt_before = {k: v for k, v in birth_time.items() if k != x}

    ret_occ, ret_bt, _ = crn_step(force_occ, force_bt, step, input_value, radius, params, seed)
    tra_occ, tra_bt, _ = crn_step(force_occ, force_bt, step, input_value, radius, params, seed)
    pre_occ, pre_bt, _ = crn_step(
        prevent_before, prevent_bt_before, step, input_value, radius, params, seed, excluded=[x]
    )

    force_present = (x in ret_occ) and (x in tra_occ)
    prevent_blocked = x not in pre_occ

    tra_occ = set(tra_occ)
    tra_occ.discard(x)
    tra_bt = dict(tra_bt)
    tra_bt.pop(x, None)

    equalized = (x not in tra_occ) and (x not in pre_occ)

    return CausalBranches(
        prevent_occupied=pre_occ,
        prevent_birth_time=pre_bt,
        transient_occupied=tra_occ,
        transient_birth_time=tra_bt,
        retained_occupied=ret_occ,
        retained_birth_time=ret_bt,
        step=step + 1,
        x=x,
        force_present_at_exposure=force_present,
        prevent_blocked_at_exposure=prevent_blocked,
        equalized_after_exposure=equalized,
    )


def local_population(occupied: Set[Cell], x: Cell, local_radius: int) -> int:
    """Count of occupied cells within `local_radius` hex-distance of `x`, excluding
    `x` itself.

    Used to restrict the causal-gain statistic to a bounded region around the
    intervention site. The canonical archive's per-distance breakdown
    (`population_gain_by_distance` in `ch23-causal-attachment-gain-v3`) shows the
    force-minus-prevent effect concentrated at distance 1 and decaying to
    near-zero by distance ~4-5; a whole-crystal ("global") population difference
    additionally picks up chaotic far-field divergence that is real (the book's
    own far-field result, DL-13-C07) but much noisier and off-topic for this
    chapter's core RETAINED/TRANSIENT question. Restricting to a local disk
    around `x` is this module's simplified analogue of the canonical archive's
    spatially-restricted "G_H_local" -- not a reproduction of its exact
    finite-budget ring accounting.
    """
    ox, oy = x
    count = 0
    for c in occupied:
        if c == x:
            continue
        dq = c[0] - ox
        dr = c[1] - oy
        ds = -dq - dr
        if max(abs(dq), abs(dr), abs(ds)) <= local_radius:
            count += 1
    return count


def run_causal_horizon(
    branches: CausalBranches,
    env: Sequence[float],
    radius: int,
    params: CrystalParams,
    seed: int,
    horizon: int,
    *,
    local_radius: Optional[int] = None,
) -> Dict[str, object]:
    """Advance PREVENT / TRANSIENT / RETAINED for `horizon` total updates counting
    the lag-1 exposure already applied in `branches` (so this function runs
    `horizon - 1` further ordinary CRN-coupled updates, lag 2 onward).

    From lag 2 onward no branch treats `x` specially: it may reoccupy naturally
    in any branch (PREVENT included), and if it does, that is downstream
    dynamics, not a control failure -- matching the book's "later x semantics."
    `x` itself is excluded from every population count, per the design's
    "measure everything except x."

    If `local_radius` is given, populations are counted only within that
    hex-distance of `x` (see `local_population`) -- the recommended mode,
    since it is far less noisy than a whole-crystal count and is this
    module's analogue of the canonical archive's "local" causal-gain
    statistic. If `local_radius` is None, the whole crystal is counted
    (analogue of the canonical archive's noisier "global" statistic).

    Returns a dict with per-branch population trajectories (length `horizon`,
    index 0 == lag 1) and the cumulative causal-gain statistics:

        transient_G, retained_G : sum over lag=1..horizon of
            (branch population - PREVENT population), x excluded from both.
        transient_late_mean, retained_late_mean : mean per-update gain over
            the last `late_window` entries (late_window is inferred as
            roughly the final third of the horizon, minimum 3).
    """

    def pop_excluding_x(occ: Set[Cell]) -> int:
        if local_radius is not None:
            return local_population(occ, branches.x, local_radius)
        return len(occ) - (1 if branches.x in occ else 0)

    pre_occ, pre_bt = set(branches.prevent_occupied), dict(branches.prevent_birth_time)
    tra_occ, tra_bt = set(branches.transient_occupied), dict(branches.transient_birth_time)
    ret_occ, ret_bt = set(branches.retained_occupied), dict(branches.retained_birth_time)
    step = branches.step

    pre_pop = [pop_excluding_x(pre_occ)]
    tra_pop = [pop_excluding_x(tra_occ)]
    ret_pop = [pop_excluding_x(ret_occ)]
    pre_present = [branches.x in pre_occ]
    tra_present = [branches.x in tra_occ]
    ret_present = [branches.x in ret_occ]

    remaining = max(0, horizon - 1)
    for j in range(remaining):
        value = float(env[j])
        pre_occ, pre_bt, _ = crn_step(pre_occ, pre_bt, step, value, radius, params, seed)
        tra_occ, tra_bt, _ = crn_step(tra_occ, tra_bt, step, value, radius, params, seed)
        ret_occ, ret_bt, _ = crn_step(ret_occ, ret_bt, step, value, radius, params, seed)
        step += 1
        pre_pop.append(pop_excluding_x(pre_occ))
        tra_pop.append(pop_excluding_x(tra_occ))
        ret_pop.append(pop_excluding_x(ret_occ))
        pre_present.append(branches.x in pre_occ)
        tra_present.append(branches.x in tra_occ)
        ret_present.append(branches.x in ret_occ)

    pre_pop_a = np.array(pre_pop, dtype=float)
    tra_pop_a = np.array(tra_pop, dtype=float)
    ret_pop_a = np.array(ret_pop, dtype=float)

    transient_lag_gain = tra_pop_a - pre_pop_a
    retained_lag_gain = ret_pop_a - pre_pop_a

    late_window = max(3, len(transient_lag_gain) // 3)

    return {
        "prevent_population": pre_pop_a,
        "transient_population": tra_pop_a,
        "retained_population": ret_pop_a,
        "transient_lag_gain": transient_lag_gain,
        "retained_lag_gain": retained_lag_gain,
        "transient_cumulative_gain": np.cumsum(transient_lag_gain),
        "retained_cumulative_gain": np.cumsum(retained_lag_gain),
        "transient_G": float(np.sum(transient_lag_gain)),
        "retained_G": float(np.sum(retained_lag_gain)),
        "transient_late_mean": float(np.mean(transient_lag_gain[-late_window:])),
        "retained_late_mean": float(np.mean(retained_lag_gain[-late_window:])),
        "late_window": late_window,
        "transient_x_present_at_horizon": bool(tra_present[-1]),
        "retained_x_present_at_horizon": bool(ret_present[-1]),
        "retained_occupied_updates": int(sum(ret_present)),
        "retained_occupancy_fraction": float(sum(ret_present)) / len(ret_present),
        "transient_reoccupied_ever": bool(any(tra_present[1:])),
        "prevent_reoccupied_ever": bool(any(pre_present[1:])),
    }


# ---------------------------------------------------------------------------
# Local-predictor diagnostics: Frontier Creation Potential (FCP)
# ---------------------------------------------------------------------------


def occupied_neighbor_count(occupied: Set[Cell], cell: Cell) -> int:
    """Number of `cell`'s six hex neighbours that are currently occupied."""
    return sum(1 for nb in neighbors(cell) if nb in occupied)


def frontier_creation_potential(occupied: Set[Cell], x: Cell, radius: int) -> int:
    """FCP(x) = |frontier after forcing x occupied| - |frontier before|, both sets
    excluding `x` itself. Positive when occupying `x` creates net new frontier
    opportunity (typically sparse local geometry); negative when it mostly
    consumes opportunity by leaving the frontier itself (typically dense local
    geometry). Matches the book's Chapter 13 definition exactly.
    """
    before = frontier(occupied, radius) - {x}
    after = frontier(occupied | {x}, radius) - {x}
    return len(after) - len(before)


def choose_probe_cells(candidates: Sequence[Cell], seed: int, step: int, n: int) -> List[Cell]:
    """Deterministically select up to `n` cells from `candidates`, ranked by the
    cell-keyed hash (lowest first) -- reproducible pseudo-random probe sampling
    that does not consume or perturb any sequential RNG stream.
    """
    ranked = sorted(candidates, key=lambda c: (cell_keyed_uniform(seed, step, c), c))
    return ranked[: max(0, n)]
