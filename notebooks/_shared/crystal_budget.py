"""Finite-evaluation-budget extension for the Digital Crystal substrate.

Implements the two mechanisms current book Chapter 14 ("Can Finite Computation
Couple Distant Events?") needs on top of `_shared/digital_crystal.py`'s frozen
growth mechanics and `_shared/crystal_causal.py`'s CRN-coupled FORCE/PREVENT
machinery, neither of which this module modifies:

  BUDGET SELECTION   each update, only `budget` of the (possibly larger) set
                      of legal frontier candidates are actually evaluated for
                      attachment this step -- the rest simply get no coin
                      flip this update (they remain eligible on a later
                      update, if the frontier is re-evaluated). Selection is
                      a deterministic, cell-keyed pseudo-random ranking
                      (`budget_select`), using a *different* hash stream from
                      the attach-decision draw (`cell_keyed_uniform(2*seed+1,
                      ...)` vs `cell_keyed_uniform(seed, ...)`), so which
                      cells get evaluated and whether an evaluated cell
                      attaches never share randomness with each other, and
                      neither perturbs any stateful sequential RNG.

  NEAR / FAR SPLIT    a candidate cell is classified NEAR the intervention
                      site `x` if it is one of `x`'s own six hex neighbours
                      (hex-distance 1), FAR otherwise. This is the "one-step
                      reach" boundary the chapter's central question is
                      about: can competition for a *shared, finite* budget
                      couple locations OUTSIDE that one-step reach?

Mirrors the canonical archive's actual approach
(`scripts/books/digital-life/ch25_digital_crystal_finite_budget_redistribution_v1.py`):
the far-field statistic E_far is computed as an *exact expected* quantity --
a sum of attachment probabilities over the selected candidate set, not a
Monte Carlo count of realized draws -- which is what makes the full-evaluation
hard-zero identity checkable to machine precision rather than merely
"close to zero" over many samples. The multi-lag amplification statistic
(`run_budget_causal_horizon`), by contrast, uses genuinely realized CRN draws,
matching the canonical archive's own `run_arm`/`calibrated_canonical_step`
(which does simulate real attach/no-attach outcomes lag by lag), because a
finite-horizon downstream trajectory is not analytically tractable the way a
single lag's expected count is.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from digital_crystal import (
    Cell,
    CrystalParams,
    attachment_probability,
    cell_keyed_uniform,
    frontier,
    logistic,
    local_exposure_angle,
    neighbors,
)


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def cell_distance(a: Cell, b: Cell) -> int:
    """Hex distance between two arbitrary cells (not just from the origin --
    `digital_crystal.hex_distance` only measures distance from (0,0))."""
    dq = a[0] - b[0]
    dr = a[1] - b[1]
    ds = -dq - dr
    return max(abs(dq), abs(dr), abs(ds))


def classify_near_far(x: Cell, cells: Iterable[Cell]) -> Tuple[Set[Cell], Set[Cell]]:
    """Split `cells` (excluding `x` itself) into NEAR (one of x's six hex
    neighbours) and FAR (everything else, at hex-distance >= 2 from x)."""
    xn = set(neighbors(x))
    near: Set[Cell] = set()
    far: Set[Cell] = set()
    for c in cells:
        if c == x:
            continue
        (near if c in xn else far).add(c)
    return near, far


# ---------------------------------------------------------------------------
# Budget selection
# ---------------------------------------------------------------------------


def budget_select(candidates: Sequence[Cell], seed: int, step: int, budget: Optional[int]) -> List[Cell]:
    """Deterministically select up to `budget` of `candidates`, ranked by a
    cell-keyed hash stream distinct from the attach-decision draw (offsets
    the seed so `budget_select` and `crn_step`-style attach draws never
    collide). `budget=None` or `budget >= len(candidates)` means unbounded:
    every candidate is selected (full evaluation)."""
    ordered = sorted(candidates)
    if budget is None or budget >= len(ordered):
        return ordered
    ranked = sorted(ordered, key=lambda c: (cell_keyed_uniform(2 * seed + 1, step, c), c))
    return sorted(ranked[: max(0, budget)])


def score_with_offset(
    cell: Cell,
    occupied: Set[Cell],
    input_value: float,
    params: CrystalParams,
    offset: float = 0.0,
) -> float:
    """Same pre-logistic score as `digital_crystal.attachment_probability`,
    plus an additive calibration `offset` -- the mechanism the canonical
    archive uses to match expected construction rate across budget arms
    (`score' = score + calibration_offset`)."""
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
        + float(offset)
    )


def attachment_probability_with_offset(
    cell: Cell, occupied: Set[Cell], input_value: float, params: CrystalParams, offset: float = 0.0
) -> float:
    return logistic(score_with_offset(cell, occupied, input_value, params, offset))


def budget_crn_step(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    budget: Optional[int],
    *,
    offset: float = 0.0,
    excluded: Sequence[Cell] = (),
) -> Tuple[Set[Cell], Dict[Cell, int], int, Set[Cell]]:
    """One growth update, CRN-coupled (like `crystal_causal.crn_step`), with
    only `budget` of the frontier candidates actually evaluated this update
    (see `budget_select`). `excluded` cells are never selected regardless of
    budget (used for the PREVENT intervention). Returns (new_occupied,
    new_birth_time, additions, selected) where `selected` is the set of
    cells that were actually evaluated this update (whether or not they
    attached) -- needed to reason about which candidates got a coin flip
    at all under a finite budget.
    """
    excluded_set = set(excluded)
    candidates = sorted(frontier(occupied, radius))
    eligible = [c for c in candidates if c not in excluded_set]
    selected = set(budget_select(eligible, seed, step + 1, budget))

    new_occupied = set(occupied)
    new_birth_time = dict(birth_time)
    next_step = step + 1
    additions = 0
    for cell in candidates:
        if cell not in selected:
            continue
        u = cell_keyed_uniform(seed, next_step, cell)
        p = attachment_probability_with_offset(cell, occupied, input_value, params, offset)
        if u < p:
            new_occupied.add(cell)
            new_birth_time[cell] = next_step
            additions += 1
    return new_occupied, new_birth_time, additions, selected


# ---------------------------------------------------------------------------
# Design 1: exact expected far-field / near-field effect (analytic, not simulated)
# ---------------------------------------------------------------------------


@dataclass
class ExpectedEffect:
    x: Cell
    budget: Optional[int]
    f_force: int  # |FORCE candidate set| (excludes x)
    f_prevent: int  # |PREVENT candidate set|
    delta_f: int  # f_force - f_prevent (near-field candidates created by forcing x)
    near_shared: Set[Cell]
    force_only: Set[Cell]  # near-field candidates that exist only in the FORCE branch
    far_common: Set[Cell]  # far-field candidates -- provably identical set in both branches
    e_near: float  # exact expected near-field (ring-1) FORCE-minus-PREVENT effect
    e_far: float  # exact expected far-field FORCE-minus-PREVENT effect
    shared_shift_near: float  # near-field channel: probability shift on candidates in both branches
    force_only_swap_near: float  # near-field channel: candidates that exist as candidates only because of x
    p_bar_far: float  # mean attachment probability over far_common, evaluated once (branch-independent)


def expected_force_prevent_effect(
    occupied: Set[Cell],
    x: Cell,
    input_value: float,
    radius: int,
    params: CrystalParams,
    seed: int,
    step: int,
    budget: Optional[int],
) -> ExpectedEffect:
    """Exact expected (probability-sum, not simulated) FORCE-minus-PREVENT
    effect at lag 1, split into NEAR (x's own six neighbours) and FAR
    (everything else) regions, under a finite evaluation `budget` shared by
    both branches.

    FORCE: `x` is inserted occupied before the update is evaluated (matching
    `crystal_causal.force_branch_step`'s "x acts as a genuine occupied
    neighbour this same update" design).
    PREVENT: `x` stays empty and is excluded from the candidate list, so it
    cannot itself attach.

    Candidate SETS (which cells are legal frontier candidates) are branch-
    independent for FAR cells -- a cell outside x's six neighbours is a
    candidate under `digital_crystal.frontier()` iff it already has >=1
    *other* occupied neighbour, which x's occupancy cannot affect, since x is
    not one of that cell's neighbours. This is the identity this function's
    caller checks: with `budget=None` (full evaluation), every FAR candidate
    that exists is selected in *both* branches, so `e_far` must be exactly
    zero to floating-point tolerance.
    """
    occ_force = set(occupied) | {x}
    occ_prevent = set(occupied) - {x}

    cand_force = sorted(frontier(occ_force, radius) - {x})
    cand_prevent = sorted(frontier(occ_prevent, radius) - {x})

    sel_force = set(budget_select(cand_force, seed, step + 1, budget))
    sel_prevent = set(budget_select(cand_prevent, seed, step + 1, budget))

    near_force, far_force = classify_near_far(x, sel_force)
    near_prevent, far_prevent = classify_near_far(x, sel_prevent)

    near_shared = near_force & near_prevent
    force_only = near_force - near_prevent
    prevent_only = near_prevent - near_force  # expected empty: x's neighbours can only gain candidacy from x

    shared_shift_near = 0.0
    for c in near_shared:
        pf = attachment_probability(c, occ_force, input_value, params)
        pp = attachment_probability(c, occ_prevent, input_value, params)
        shared_shift_near += pf - pp
    force_only_swap_near = sum(attachment_probability(c, occ_force, input_value, params) for c in force_only)
    prevent_only_swap_near = -sum(attachment_probability(c, occ_prevent, input_value, params) for c in prevent_only)
    e_near = shared_shift_near + force_only_swap_near + prevent_only_swap_near

    far_shared = far_force & far_prevent
    far_force_only = far_force - far_prevent
    far_prevent_only = far_prevent - far_force
    e_far = 0.0
    for c in far_shared:
        pf = attachment_probability(c, occ_force, input_value, params)
        pp = attachment_probability(c, occ_prevent, input_value, params)
        e_far += pf - pp
    e_far += sum(attachment_probability(c, occ_force, input_value, params) for c in far_force_only)
    e_far -= sum(attachment_probability(c, occ_prevent, input_value, params) for c in far_prevent_only)

    far_common = far_force | far_prevent  # provably equal when budget is unbounded; see docstring
    p_bar_far = (
        float(sum(attachment_probability(c, occ_prevent, input_value, params) for c in far_common)) / len(far_common)
        if far_common
        else float("nan")
    )

    return ExpectedEffect(
        x=x,
        budget=budget,
        f_force=len(cand_force),
        f_prevent=len(cand_prevent),
        delta_f=len(cand_force) - len(cand_prevent),
        near_shared=near_shared,
        force_only=force_only,
        far_common=far_common,
        e_near=e_near,
        e_far=e_far,
        shared_shift_near=shared_shift_near,
        force_only_swap_near=force_only_swap_near,
        p_bar_far=p_bar_far,
    )


def expected_active_fraction(f_total: int, budget: Optional[int], k: int, p_survive: float) -> float:
    """Parameter-free combinatorial prediction: the probability that at least
    one of `k` marked candidates (out of `f_total` total legal candidates) is
    among the `budget` cells selected by `budget_select`, times a prior
    `p_survive` that the marked candidates are still eligible at all --

        P(active) = p_survive * (1 - C(f_total-k, budget) / C(f_total, budget))

    matching `research/digital-life/ch26-v2-mechanism-audit`'s zero-inflation
    reference formula exactly. No fitted constants: only counts and a prior.
    """
    if budget is None or budget >= f_total:
        return float(p_survive)
    if k <= 0 or f_total <= 0:
        return 0.0
    if f_total - k < budget:
        return float(p_survive)
    p_not_selected = math.comb(f_total - k, budget) / math.comb(f_total, budget)
    return float(p_survive) * (1.0 - p_not_selected)


# ---------------------------------------------------------------------------
# Design 2: realized multi-lag amplification under budget selection
# ---------------------------------------------------------------------------


def solve_calibration_offset(
    candidates: Sequence[Cell],
    occupied: Set[Cell],
    input_value: float,
    params: CrystalParams,
    target_count: float,
    *,
    lo: float = -12.0,
    hi: float = 12.0,
    iters: int = 60,
) -> float:
    """Bisect for the additive score offset that makes
    sum(attachment_probability_with_offset(c, ...)) over `candidates` equal
    `target_count`. The sum is monotonically increasing in `offset`, so
    bisection is exact to `iters` bits of precision. Matches the canonical
    archive's `solve_offset` (used to calibrate a higher-budget arm's
    expected construction rate down to a lower-budget reference arm's)."""
    if not candidates:
        return 0.0

    def total_at(offset: float) -> float:
        return sum(attachment_probability_with_offset(c, occupied, input_value, params, offset) for c in candidates)

    lo_v, hi_v = total_at(lo), total_at(hi)
    if target_count <= lo_v:
        return lo
    if target_count >= hi_v:
        return hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if total_at(mid) < target_count:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run_budget_causal_horizon(
    force_occ: Set[Cell],
    force_bt: Dict[Cell, int],
    prevent_occ: Set[Cell],
    prevent_bt: Dict[Cell, int],
    step: int,
    x: Cell,
    env: Sequence[float],
    radius: int,
    params: CrystalParams,
    seed: int,
    budget: Optional[int],
    horizon: int,
    *,
    local_radius: int,
    static_offset: Optional[float] = None,
) -> Dict[str, object]:
    """Advance FORCE and PREVENT branches for `horizon` updates under a
    shared evaluation budget, with x already forced/excluded going into lag
    1 by the caller (this function does not itself set up the lag-1
    exposure -- see the notebook's own probe loop, which mirrors
    `crystal_causal.force_prevent_retained_transient`'s TRANSIENT arm: x
    gets exactly one causal update as an occupied neighbour, then is
    explicitly removed, matching Chapter 26's "one transient FORCE/PREVENT
    intervention").

    Calibration: at every lag, an additive offset is solved so the PREVENT
    branch's own expected attachment count (over its currently-selected
    candidates) matches a `target_rate` computed once from a low-budget
    reference (passed in via the notebook). If `static_offset` is given, that
    single fixed offset is reused at every lag instead (the V1 "single-lag
    calibration" design this chapter shows is invalid); if `static_offset`
    is None, callers are expected to have already applied a fresh per-lag
    offset via `offset=` before calling `budget_crn_step` themselves for the
    lag actually being measured -- this function threads `static_offset`
    through unchanged when given, mainly for the FULL/unbounded arm's V1
    static-calibration demonstration.

    Returns per-branch local-population trajectories (excluding x) and the
    cumulative causal-gain statistic G_T = sum_{lag=1..horizon}(FORCE_local -
    PREVENT_local), matching `crystal_causal.run_causal_horizon`'s
    "measure everything except x, restricted to a local disk" idiom.
    """
    from crystal_causal import local_population  # local import: avoid a hard module-order dependency

    offset = 0.0 if static_offset is None else static_offset

    def pop(occ: Set[Cell]) -> int:
        return local_population(occ, x, local_radius)

    force_pop = [pop(force_occ)]
    prevent_pop = [pop(prevent_occ)]
    lag_gain = []
    for j in range(horizon):
        value = float(env[j])
        force_occ, force_bt, _, _ = budget_crn_step(
            force_occ, force_bt, step, value, radius, params, seed, budget, offset=offset
        )
        prevent_occ, prevent_bt, _, _ = budget_crn_step(
            prevent_occ, prevent_bt, step, value, radius, params, seed, budget, offset=offset
        )
        step += 1
        fp, pp = pop(force_occ), pop(prevent_occ)
        force_pop.append(fp)
        prevent_pop.append(pp)
        lag_gain.append(fp - pp)

    import numpy as np

    lag_gain_a = np.array(lag_gain, dtype=float)
    return {
        "force_population": np.array(force_pop, dtype=float),
        "prevent_population": np.array(prevent_pop, dtype=float),
        "lag_gain": lag_gain_a,
        "cumulative_gain": np.cumsum(lag_gain_a),
        "G_T": float(np.sum(lag_gain_a)),
    }
