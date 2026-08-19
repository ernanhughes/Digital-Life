"""Predictive-coherence and causal-boundary-localization machinery for Chapter 12.

Two independent frozen designs, both built on top of `_shared/crystal_evaluation_budget.py`'s
finite-evaluation-budget substrate (loss rate delta=0.08, neutral budget B=96, matching
the book's own frozen substrate for this chapter):

V1 -- PREDICTIVE COHERENCE SCREEN
    For five frozen candidate radii (as a fraction of the crystal's effective
    radius), does a candidate region's own 19-dimensional process state contribute
    held-out predictive power for its own future beyond what the surrounding
    annulus already provides, beyond a radial-geometry-matched observer-only null?

V2 -- CAUSAL BOUNDARY LOCALIZATION
    Remove a matched set of cells just inside vs. just outside a candidate boundary
    and an interior control boundary, run both counterfactual branches forward
    under cell-keyed CRN coupling, and measure whether the candidate boundary
    localizes downstream occupancy divergence more strongly than the control.

This is a faithful, reduced re-implementation of the mechanism in
``scripts/books/digital-life/ch22_digital_crystal_predictive_coherence_v1.py`` and
``ch22_digital_crystal_causal_boundary_coherence_v2.py``. It does not import those
scripts directly (they depend on the heavier Chapter 18 ``ch18`` material-state
module this chapter's claims do not need) but reproduces their statistical design:
the same 19-dimensional process vector, the same radial-bin-matched observer null,
the same ridge/held-out-R2 self-prediction-gain statistic, the same family-wise
run-group future-permutation null, and the same neighbour-count/distance-bin
matched intervention selection for the causal-localization test.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple

import numpy as np

from digital_crystal import Cell, CrystalParams, axial_to_xy, hex_distance
from crystal_evaluation_budget import (
    BudgetState,
    OccupancyLedger,
    apply_background_loss,
    budgeted_growth_step,
    loss_uniform,
    warm_budget_checkpoint,
)

# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def euclidean_radius(cell: Cell) -> float:
    x, y = axial_to_xy(cell)
    return math.hypot(x, y)


def cell_angle(cell: Cell) -> float:
    x, y = axial_to_xy(cell)
    theta = math.atan2(y, x)
    return theta + 2.0 * math.pi if theta < 0 else theta


def effective_radius(occupied: Set[Cell]) -> float:
    if not occupied:
        return 1.0
    return max(1.0, max(euclidean_radius(c) for c in occupied))


def make_universe(radius: int) -> Set[Cell]:
    return {(q, r) for q in range(-radius, radius + 1) for r in range(-radius, radius + 1) if hex_distance((q, r)) <= radius}


def region_membership(cells: Sequence[Cell], radius_cutoff: float) -> Set[Cell]:
    return {c for c in cells if euclidean_radius(c) <= radius_cutoff}


def annulus_membership(cells: Sequence[Cell], inner_radius: float, outer_radius: float) -> Set[Cell]:
    return {c for c in cells if inner_radius < euclidean_radius(c) <= outer_radius}


def radial_shell(universe: Set[Cell], low: float, high: float, include_low: bool = True) -> Set[Cell]:
    if include_low:
        return {c for c in universe if low <= euclidean_radius(c) <= high}
    return {c for c in universe if low < euclidean_radius(c) <= high}


def sector_index(cell: Cell, sector_count: int) -> int:
    theta = cell_angle(cell)
    return min(sector_count - 1, int(theta / (2.0 * math.pi) * sector_count))


def radial_bin_index(cell: Cell, max_radius: float, bins: int) -> int:
    frac = min(0.999999, euclidean_radius(cell) / max(1e-9, max_radius))
    return min(bins - 1, int(frac * bins))


# ---------------------------------------------------------------------------
# Observer-side per-step frames (occupied/frontier/additions/losses/first/reocc)
# ---------------------------------------------------------------------------


@dataclass
class StepFrame:
    step: int
    occupied: Set[Cell]
    additions: Set[Cell]
    losses: Set[Cell]
    first: Set[Cell]
    reoccupations: Set[Cell]


def run_frames(
    env: np.ndarray,
    warmup: int,
    total_steps: int,
    radius: int,
    params: CrystalParams,
    loss_rate: float,
    budget: Optional[int],
    seed: int,
) -> List[StepFrame]:
    """Grow past warmup under the frozen (delta, B) substrate, recording one
    StepFrame per update. Stops early (frames list simply ends) if the crystal
    collapses to empty."""
    state = warm_budget_checkpoint(env, warmup, seed, radius, params)
    ledger = OccupancyLedger.initial(state.occupied)
    frames: List[StepFrame] = []
    for j in range(total_steps):
        state, additions, _, _ = budgeted_growth_step(
            state, float(env[warmup + j]), radius, params, budget, "neutral", seed
        )
        first_set, reocc_set = ledger.classify_additions_detailed(additions)
        state, lost = apply_background_loss(state, seed, loss_rate)
        ledger.register_losses(lost)
        frames.append(
            StepFrame(
                step=state.step,
                occupied=set(state.occupied),
                additions=set(additions),
                losses=set(lost),
                first=first_set,
                reoccupations=reocc_set,
            )
        )
        if not state.occupied:
            break
    return frames


# ---------------------------------------------------------------------------
# Feature extraction: 19-dim dynamic process vector
# ---------------------------------------------------------------------------


def summarize_region(frames: Sequence[StepFrame], region: Set[Cell], sector_count: int) -> np.ndarray:
    """19-dim dynamic process vector: population density, a frontier-density proxy
    (recent attachment density -- this reduced reimplementation does not track an
    explicit per-frame frontier set, so instantaneous frontier size is approximated
    by recent attachment activity; disclosed as a deliberate simplification, not a
    historical-value match), recent attachment/loss/first-occupation/reoccupation/
    gross-turnover fractions (5 dims), then sectorized population density and
    sectorized gross turnover (6 + 6 = 12 more dims). 2 + 5 + 6 + 6 = 19 dims total,
    matching the book's own stated feature count."""
    latest = frames[-1]
    region_size = max(1.0, float(len(region)))

    population_density = len(latest.occupied & region) / region_size
    att = sum(len(f.additions & region) for f in frames)
    los = sum(len(f.losses & region) for f in frames)
    first = sum(len(f.first & region) for f in frames)
    reocc = sum(len(f.reoccupations & region) for f in frames)
    time_denom = region_size * max(1, len(frames))
    frontier_proxy = min(1.0, att / max(1.0, region_size))

    out = [
        population_density,
        frontier_proxy,
        att / time_denom,
        los / time_denom,
        first / time_denom,
        reocc / time_denom,
        (att + los) / time_denom,
    ]

    region_by_sector = [{c for c in region if sector_index(c, sector_count) == s} for s in range(sector_count)]

    for sector_cells in region_by_sector:
        denom = max(1.0, float(len(sector_cells)))
        out.append(len(latest.occupied & sector_cells) / denom)

    for sector_cells in region_by_sector:
        denom = max(1.0, float(len(sector_cells))) * max(1, len(frames))
        turnover = sum(len((f.additions | f.losses) & sector_cells) for f in frames)
        out.append(turnover / denom)

    return np.asarray(out, dtype=float)


def scrambled_region_mask(
    universe: Set[Cell],
    real_region: Set[Cell],
    max_radius: float,
    bins: int,
    seed: int,
    step: int,
    scale_index: int,
) -> Set[Cell]:
    """Observer-only geometry-matched null: preserve how many lattice sites the
    real region owns in each radial bin, but reassign *which* angular sites
    within that bin belong to the null region, using keyed observer-only
    randomness. Preserves approximate radial scale; destroys the centered
    contiguous region assignment."""
    result: Set[Cell] = set()
    by_bin_universe: Dict[int, List[Cell]] = {b: [] for b in range(bins)}
    by_bin_real_count: Dict[int, int] = {b: 0 for b in range(bins)}
    for cell in universe:
        by_bin_universe[radial_bin_index(cell, max_radius, bins)].append(cell)
    for cell in real_region:
        by_bin_real_count[radial_bin_index(cell, max_radius, bins)] += 1
    for b in range(bins):
        cells = by_bin_universe[b]
        k = min(by_bin_real_count[b], len(cells))
        ranked = sorted(
            cells,
            key=lambda c: (loss_uniform(seed, step, c, tag=f"ch22-v1-null-{scale_index}-{b}"), c),
        )
        result.update(ranked[:k])
    return result


# ---------------------------------------------------------------------------
# Ridge regression / held-out R^2
# ---------------------------------------------------------------------------


@dataclass
class Standardizer:
    mean: np.ndarray
    scale: np.ndarray

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) / self.scale


def fit_standardizer(x: np.ndarray) -> Standardizer:
    mean = np.mean(x, axis=0)
    scale = np.std(x, axis=0, ddof=0)
    scale = np.where(scale < 1e-12, 1.0, scale)
    return Standardizer(mean=mean, scale=scale)


def fit_ridge(x: np.ndarray, y: np.ndarray, alpha: float):
    xs, ys = fit_standardizer(x), fit_standardizer(y)
    xz, yz = xs.transform(x), ys.transform(y)
    xtx = xz.T @ xz
    coef = np.linalg.solve(xtx + alpha * np.eye(xtx.shape[0]), xz.T @ yz)
    return xs, ys, coef


def predict_ridge(model, x: np.ndarray) -> np.ndarray:
    xs, ys, coef = model
    return xs.transform(x) @ coef * ys.scale + ys.mean


def multivariate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    resid = np.sum((y_true - y_pred) ** 2)
    baseline = np.sum((y_true - np.mean(y_true, axis=0, keepdims=True)) ** 2)
    if baseline <= 1e-12:
        return 0.0
    return float(1.0 - resid / baseline)


def frozen_group_split(groups: Sequence[int], seed: int, test_fraction: float) -> Tuple[Set[int], Set[int]]:
    unique = sorted(set(groups))
    rng = np.random.default_rng(seed)
    perm = list(rng.permutation(unique))
    n_test = max(1, int(round(len(unique) * test_fraction)))
    return set(int(x) for x in perm[n_test:]), set(int(x) for x in perm[:n_test])


@dataclass
class Sample:
    group: int
    checkpoint: int
    scale_index: int
    real_s: np.ndarray
    real_e: np.ndarray
    real_future: np.ndarray
    null_s: np.ndarray
    null_e: np.ndarray
    null_future: np.ndarray


def evaluate_scale(samples: Sequence[Sample], scale_index: int, alpha: float, split_seed: int, test_fraction: float, null: bool) -> dict:
    subset = [s for s in samples if s.scale_index == scale_index]
    groups = [s.group for s in subset]
    train_groups, test_groups = frozen_group_split(groups, split_seed, test_fraction)

    if null:
        s_mat = np.asarray([s.null_s for s in subset])
        e_mat = np.asarray([s.null_e for s in subset])
        y_mat = np.asarray([s.null_future for s in subset])
    else:
        s_mat = np.asarray([s.real_s for s in subset])
        e_mat = np.asarray([s.real_e for s in subset])
        y_mat = np.asarray([s.real_future for s in subset])

    train_mask = np.asarray([s.group in train_groups for s in subset])
    test_mask = np.asarray([s.group in test_groups for s in subset])

    x_e = e_mat
    x_se = np.concatenate([s_mat, e_mat], axis=1)

    model_e = fit_ridge(x_e[train_mask], y_mat[train_mask], alpha)
    model_se = fit_ridge(x_se[train_mask], y_mat[train_mask], alpha)

    r2_e = multivariate_r2(y_mat[test_mask], predict_ridge(model_e, x_e[test_mask]))
    r2_se = multivariate_r2(y_mat[test_mask], predict_ridge(model_se, x_se[test_mask]))

    return {
        "scale_index": scale_index,
        "train_groups": len(train_groups),
        "test_groups": len(test_groups),
        "r2_environment_only": r2_e,
        "r2_system_plus_environment": r2_se,
        "delta_self": r2_se - r2_e,
    }


def permuted_copy(samples: Sequence[Sample], permutation: Dict[int, int]) -> List[Sample]:
    """Re-pair each current-state sample with future vectors from a *different*
    run group, matched by checkpoint and scale -- both real and null futures."""
    lookup = {(s.group, s.checkpoint, s.scale_index): s for s in samples}
    out: List[Sample] = []
    for s in samples:
        target = lookup.get((permutation[s.group], s.checkpoint, s.scale_index))
        if target is None:
            continue
        out.append(
            Sample(
                group=s.group, checkpoint=s.checkpoint, scale_index=s.scale_index,
                real_s=s.real_s, real_e=s.real_e, real_future=target.real_future,
                null_s=s.null_s, null_e=s.null_e, null_future=target.null_future,
            )
        )
    return out


def derangement(groups: Sequence[int], rng: np.random.Generator) -> Dict[int, int]:
    groups = sorted(set(groups))
    if len(groups) < 2:
        return {g: g for g in groups}
    shifted = list(rng.permutation(groups))
    for _ in range(20):
        if not any(shifted[i] == groups[i] for i in range(len(groups))):
            break
        shifted = list(rng.permutation(groups))
    if any(shifted[i] == groups[i] for i in range(len(groups))):
        shifted = groups[1:] + groups[:1]
    return {g: h for g, h in zip(groups, shifted)}


# ---------------------------------------------------------------------------
# V2: matched intervention selection + causal-localization statistic
# ---------------------------------------------------------------------------


def occupied_neighbor_count(cell: Cell, occupied: Set[Cell]) -> int:
    from digital_crystal import neighbors

    return sum(nb in occupied for nb in neighbors(cell))


def distance_bin(cell: Cell, cutoff: float, bin_width: float) -> int:
    return int(math.floor(abs(euclidean_radius(cell) - cutoff) / max(1e-9, bin_width)))


def intervention_stratum(cell: Cell, occupied: Set[Cell], cutoff: float, bin_width: float) -> Tuple[int, int]:
    return occupied_neighbor_count(cell, occupied), distance_bin(cell, cutoff, bin_width)


def matched_intervention_sets(
    state: BudgetState,
    universe: Set[Cell],
    cutoff: float,
    shell_width: float,
    bin_width: float,
    k: int,
    boundary_index: int,
    seed: int,
) -> Optional[Tuple[List[Cell], List[Cell], dict]]:
    occupied = set(state.occupied)
    inner_zone = radial_shell(universe, max(0.0, cutoff - shell_width), cutoff, include_low=True)
    outer_zone = radial_shell(universe, cutoff, cutoff + shell_width, include_low=False)

    inside_candidates = sorted(occupied & inner_zone)
    outside_candidates = sorted(occupied & outer_zone)

    inside_by: Dict[Tuple[int, int], List[Cell]] = {}
    outside_by: Dict[Tuple[int, int], List[Cell]] = {}
    for cell in inside_candidates:
        inside_by.setdefault(intervention_stratum(cell, occupied, cutoff, bin_width), []).append(cell)
    for cell in outside_candidates:
        outside_by.setdefault(intervention_stratum(cell, occupied, cutoff, bin_width), []).append(cell)

    matched_pairs: List[Tuple[Cell, Cell, Tuple[int, int]]] = []
    for key in sorted(set(inside_by) & set(outside_by)):
        ins = sorted(inside_by[key], key=lambda c: (loss_uniform(seed, state.step, c, tag=f"ch22-v2-in-{boundary_index}"), c))
        outs = sorted(outside_by[key], key=lambda c: (loss_uniform(seed, state.step, c, tag=f"ch22-v2-out-{boundary_index}"), c))
        for i in range(min(len(ins), len(outs))):
            matched_pairs.append((ins[i], outs[i], key))

    matched_pairs = sorted(
        matched_pairs,
        key=lambda pair: (loss_uniform(seed, state.step, pair[0], tag=f"ch22-v2-order-{boundary_index}"), pair[0], pair[1]),
    )

    if len(matched_pairs) < k:
        return None

    chosen = matched_pairs[:k]
    inside = [p[0] for p in chosen]
    outside = [p[1] for p in chosen]
    diagnostics = {
        "inside_candidates": len(inside_candidates),
        "outside_candidates": len(outside_candidates),
        "matched_pair_pool": len(matched_pairs),
        "selected_k": k,
    }
    return inside, outside, diagnostics


def remove_cells(state: BudgetState, cells: Sequence[Cell]) -> BudgetState:
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)
    for c in cells:
        occupied.discard(c)
        birth_time.pop(c, None)
    return BudgetState(occupied=occupied, birth_time=birth_time, step=state.step)


def run_future_crn(
    state: BudgetState, future_env: Sequence[float], radius: int, params: CrystalParams,
    budget: Optional[int], loss_rate: float, seed: int,
) -> BudgetState:
    """Advance one branch under the CRN-coupled budgeted growth rule. Two branches
    built from the same checkpoint and given the same `seed` see an *identical*
    coin flip for every candidate cell they share at every step -- differences are
    attributable to the intervention, not to luck (the same idiom Chapter 8's
    DL-08-C06 fix and Chapter 13's `crystal_causal.crn_step` use)."""
    out = state
    for value in future_env:
        out, _, _, _ = budgeted_growth_step(out, float(value), radius, params, budget, "neutral", seed)
        out, _ = apply_background_loss(out, seed, loss_rate)
        if not out.occupied:
            break
    return out


def occupancy_divergence(branch: Set[Cell], control: Set[Cell], target: Set[Cell]) -> float:
    if not target:
        return 0.0
    changed = branch ^ control
    return len(changed & target) / float(len(target))


@dataclass
class BoundaryResult:
    radius_fraction: float
    cutoff: float
    inside_to_inner: float
    outside_to_inner: float
    inside_to_outer: float
    outside_to_outer: float
    causal_localization: float
    diagnostics: dict


def evaluate_boundary(
    checkpoint: BudgetState,
    future_env: Sequence[float],
    radius: int,
    params: CrystalParams,
    budget: Optional[int],
    loss_rate: float,
    universe: Set[Cell],
    radius_fraction: float,
    shell_width: float,
    bin_width: float,
    k: int,
    boundary_index: int,
    seed: int,
) -> Optional[BoundaryResult]:
    reff = effective_radius(checkpoint.occupied)
    cutoff = radius_fraction * reff

    matched = matched_intervention_sets(checkpoint, universe, cutoff, shell_width, bin_width, k, boundary_index, seed)
    if matched is None:
        return None
    inside_cells, outside_cells, diagnostics = matched

    control_start = checkpoint
    inside_start = remove_cells(checkpoint, inside_cells)
    outside_start = remove_cells(checkpoint, outside_cells)

    control_end = run_future_crn(control_start, future_env, radius, params, budget, loss_rate, seed)
    inside_end = run_future_crn(inside_start, future_env, radius, params, budget, loss_rate, seed)
    outside_end = run_future_crn(outside_start, future_env, radius, params, budget, loss_rate, seed)

    inner_target = radial_shell(universe, max(0.0, cutoff - shell_width), cutoff, include_low=True)
    outer_target = radial_shell(universe, cutoff, cutoff + shell_width, include_low=False)

    inside_to_inner = occupancy_divergence(inside_end.occupied, control_end.occupied, inner_target)
    outside_to_inner = occupancy_divergence(outside_end.occupied, control_end.occupied, inner_target)
    inside_to_outer = occupancy_divergence(inside_end.occupied, control_end.occupied, outer_target)
    outside_to_outer = occupancy_divergence(outside_end.occupied, control_end.occupied, outer_target)

    causal_localization = (inside_to_inner - outside_to_inner) + (outside_to_outer - inside_to_outer)

    diagnostics.update({"effective_radius": reff, "cutoff": cutoff})

    return BoundaryResult(
        radius_fraction=radius_fraction, cutoff=cutoff,
        inside_to_inner=inside_to_inner, outside_to_inner=outside_to_inner,
        inside_to_outer=inside_to_outer, outside_to_outer=outside_to_outer,
        causal_localization=causal_localization, diagnostics=diagnostics,
    )
