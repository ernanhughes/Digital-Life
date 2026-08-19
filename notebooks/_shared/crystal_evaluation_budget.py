"""Finite per-update evaluation-budget extension for the Digital Crystal substrate.

Adds exactly one new rule on top of ``digital_crystal.py``'s frozen growth mechanics:
at most ``B`` frontier candidates may receive a canonical attachment evaluation per
update. An unevaluated candidate gets no attachment attempt that update -- it is not
blocked, not penalized, not remembered, and may be evaluated again next update. No
energy, fuel, resource counter, metabolism variable, maintenance controller, target
size, or memory of what was neglected is added anywhere.

This module is a faithful, reduced re-implementation of the mechanism in
``scripts/books/digital-life/ch21_digital_crystal_finite_update_budget_v1.py`` (and
the unchanged core it shares with the ``_v2``/``_v3`` scripts): keyed deterministic
scheduling policies, a budgeted growth step, and an observer-only occupancy ledger
that classifies each new attachment as a first occupation or a reoccupation without
that classification ever being visible to the scheduling policies or the attachment
rule itself. It does not import the historical script directly because that script
depends on the heavier Chapter 18 "material state" module (``ch18``), which Chapter
11's claims do not need -- exactly the same simplification Chapter 10's
``crystal_loss.py`` already made for the material-loss rule this module reuses.

Departing from the historical scripts in one deliberate way: attachment draws here
use ``digital_crystal.cell_keyed_uniform`` (a cell/step/seed-keyed hash) rather than
a stateful sequential ``random.Random`` stream. The historical Chapter 21 scripts
already did the same thing (via ``ch18.cell_uniform``), so this is not a
simplification relative to history -- it is what lets a budgeted growth step double,
unmodified, as the CRN-coupled branch mechanism Chapter 12's causal-boundary test
needs (matching Chapter 8's CRN-artifact-fix idiom, reused again in
``_shared/crystal_causal.py`` for Chapter 13).

Note: this module is named ``crystal_evaluation_budget`` (not ``crystal_budget``)
because Chapter 14's reconstruction independently claimed the ``crystal_budget``
filename in this shared directory for a different (though related) finite-budget
mechanism; the two are not interchangeable and are kept as separate modules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
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
from crystal_loss import (  # noqa: F401 -- re-exported for notebook convenience
    make_environment,
    normalized_late_slope,
    loss_uniform,
)

POLICIES = ("neutral", "high_support", "low_support")


def occupied_neighbor_count(cell: Cell, occupied: Set[Cell]) -> int:
    return sum(nb in occupied for nb in neighbors(cell))


def schedule_uniform(seed: int, step: int, cell: Cell) -> float:
    """Keyed scheduling noise, independent of the loss stream and the attachment
    coin-flip stream (different string tag hashed in) -- used only to break ties
    within a scheduling policy, never to decide attachment itself."""
    return loss_uniform(seed, step, cell, tag="ch21-schedule")


def select_candidates(
    frontier_cells: Sequence[Cell],
    occupied: Set[Cell],
    budget: Optional[int],
    policy: str,
    seed: int,
    step: int,
) -> List[Cell]:
    """Select at most `budget` frontier sites to receive a canonical attachment
    evaluation this update. Policies use only current geometry (occupied-neighbour
    count) plus keyed scheduling noise -- never the observer-only occupancy ledger,
    so they cannot "know" whether a candidate is a reoccupation site."""
    cells = list(frontier_cells)
    if budget is None or budget >= len(cells):
        return sorted(cells)
    k = max(0, min(int(budget), len(cells)))
    if policy == "neutral":
        ranked = sorted(cells, key=lambda c: (schedule_uniform(seed, step, c), c))
    elif policy == "high_support":
        ranked = sorted(
            cells,
            key=lambda c: (-occupied_neighbor_count(c, occupied), schedule_uniform(seed, step, c), c),
        )
    elif policy == "low_support":
        ranked = sorted(
            cells,
            key=lambda c: (occupied_neighbor_count(c, occupied), schedule_uniform(seed, step, c), c),
        )
    else:
        raise ValueError(f"Unknown policy: {policy!r}")
    return ranked[:k]


@dataclass
class BudgetState:
    """Same shape as CrystalState, but with no sequential RNG -- attachment draws
    are cell-keyed (see module docstring), so there is no RNG state to thread."""

    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int


def budgeted_growth_step(
    state: BudgetState,
    input_value: float,
    radius: int,
    params: CrystalParams,
    budget: Optional[int],
    policy: str,
    seed: int,
) -> Tuple[BudgetState, List[Cell], int, int]:
    """One canonical Digital Crystal growth update, restricted to `budget` frontier
    candidates chosen by `policy`. Returns (new_state, additions, frontier_count,
    evaluated_count)."""
    occupied_before = set(state.occupied)
    frontier_cells = sorted(frontier(occupied_before, radius))
    next_step = state.step + 1
    selected = select_candidates(frontier_cells, occupied_before, budget, policy, seed, next_step)

    occupied = set(occupied_before)
    birth_time = dict(state.birth_time)
    additions: List[Cell] = []
    for cell in selected:
        p = attachment_probability(cell, occupied_before, input_value, params)
        if cell_keyed_uniform(seed, next_step, cell) < p:
            additions.append(cell)
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    return (
        BudgetState(occupied=occupied, birth_time=birth_time, step=next_step),
        additions,
        len(frontier_cells),
        len(selected),
    )


def apply_background_loss(
    state: BudgetState, seed: int, loss_rate: float
) -> Tuple[BudgetState, List[Cell]]:
    """Independent post-growth cell loss at rate `loss_rate`, keyed on the same
    hash family Chapter 10's `crystal_loss.py` uses (default tag) -- the loss rule
    is unchanged from Chapter 10; only the growth step above is new this chapter."""
    lost = [c for c in sorted(state.occupied) if loss_uniform(seed, state.step, c) < float(loss_rate)]
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)
    for c in lost:
        occupied.discard(c)
        birth_time.pop(c, None)
    return BudgetState(occupied=occupied, birth_time=birth_time, step=state.step), lost


def initial_budget_state(seed: int = 0) -> BudgetState:
    return BudgetState(occupied={(0, 0)}, birth_time={(0, 0): 0}, step=0)


def warm_budget_checkpoint(
    env: np.ndarray, warmup_steps: int, seed: int, radius: int, params: CrystalParams
) -> BudgetState:
    """Warmup uses an effectively unlimited budget (matching Ch.21's own warmup,
    which grows the canonical unlimited-budget crystal before scarcity begins)."""
    state = initial_budget_state(seed)
    for t in range(warmup_steps):
        state, _, _, _ = budgeted_growth_step(state, float(env[t]), radius, params, None, "neutral", seed)
    return state


@dataclass
class OccupancyLedger:
    """Observer-side site history. None of these fields influence candidate
    selection or attachment dynamics -- purely a measurement instrument."""

    ever_occupied: Set[Cell] = field(default_factory=set)
    currently_lost: Set[Cell] = field(default_factory=set)
    loss_count: int = 0
    first_occupation_count: int = 0
    reoccupation_count: int = 0

    @staticmethod
    def initial(occupied: Set[Cell]) -> "OccupancyLedger":
        return OccupancyLedger(ever_occupied=set(occupied))

    def classify_additions(self, additions: Sequence[Cell]) -> Tuple[int, int]:
        first_set, reocc_set = self.classify_additions_detailed(additions)
        return len(first_set), len(reocc_set)

    def classify_additions_detailed(self, additions: Sequence[Cell]) -> Tuple[Set[Cell], Set[Cell]]:
        first_set: Set[Cell] = set()
        reocc_set: Set[Cell] = set()
        for cell in additions:
            if cell in self.currently_lost:
                reocc_set.add(cell)
                self.reoccupation_count += 1
                self.currently_lost.discard(cell)
            elif cell not in self.ever_occupied:
                first_set.add(cell)
                self.first_occupation_count += 1
            self.ever_occupied.add(cell)
        return first_set, reocc_set

    def register_losses(self, lost: Sequence[Cell]) -> None:
        for cell in lost:
            self.loss_count += 1
            self.currently_lost.add(cell)


def run_budget_policy(
    env: np.ndarray,
    warmup: int,
    horizon: int,
    late_window: int,
    radius: int,
    params: CrystalParams,
    loss_rate: float,
    budget: Optional[int],
    policy: str,
    seed: int,
) -> dict:
    """One full run: unlimited-budget warmup, then `horizon` updates of
    (budgeted growth -> background loss) under the given (budget, policy)."""
    state = warm_budget_checkpoint(env, warmup, seed, radius, params)
    ledger = OccupancyLedger.initial(state.occupied)

    pop, frontier_n, evaluated_n, attach_n, first_n, reocc_n, loss_n, net_n = ([] for _ in range(8))

    for j in range(horizon):
        state, additions, f_n, e_n = budgeted_growth_step(
            state, float(env[warmup + j]), radius, params, budget, policy, seed
        )
        first, reoccupied = ledger.classify_additions(additions)
        state, lost = apply_background_loss(state, seed, loss_rate)
        ledger.register_losses(lost)

        pop.append(len(state.occupied))
        frontier_n.append(f_n)
        evaluated_n.append(e_n)
        attach_n.append(len(additions))
        first_n.append(first)
        reocc_n.append(reoccupied)
        loss_n.append(len(lost))
        net_n.append(len(additions) - len(lost))

        if not state.occupied:
            remaining = horizon - j - 1
            for arr, fill in (
                (pop, 0), (frontier_n, 0), (evaluated_n, 0), (attach_n, 0),
                (first_n, 0), (reocc_n, 0), (loss_n, 0), (net_n, 0),
            ):
                arr.extend([fill] * remaining)
            break

    late = late_window
    total_evals = max(1, int(np.sum(evaluated_n)))
    eval_fraction = [e / f if f else 0.0 for e, f in zip(evaluated_n, frontier_n)]
    loss_count = ledger.loss_count
    slope, nslope = normalized_late_slope(pop, late)

    gross_turnover = [a + l for a, l in zip(attach_n, loss_n)]
    turnover_fraction = [t / p if p else 0.0 for t, p in zip(gross_turnover, pop)]

    return {
        "budget": "unlimited" if budget is None else int(budget),
        "policy": policy,
        "final_population": pop[-1],
        "late_mean_population": float(np.mean(pop[-late:])),
        "late_normalized_slope": nslope,
        "late_mean_net": float(np.mean(net_n[-late:])),
        "late_mean_attachments": float(np.mean(attach_n[-late:])),
        "late_mean_losses": float(np.mean(loss_n[-late:])),
        "late_mean_first_occupations": float(np.mean(first_n[-late:])),
        "late_mean_reoccupations": float(np.mean(reocc_n[-late:])),
        "late_turnover_fraction": float(np.mean(turnover_fraction[-late:])),
        "mean_evaluation_fraction": float(np.mean(eval_fraction)),
        "total_evaluations": total_evals,
        "first_occupation_count": ledger.first_occupation_count,
        "reoccupation_count": ledger.reoccupation_count,
        "loss_count": loss_count,
        "reoccupation_per_loss": (ledger.reoccupation_count / loss_count) if loss_count else 0.0,
        "first_occupations_per_1000_evals": 1000.0 * ledger.first_occupation_count / total_evals,
        "reoccupations_per_1000_evals": 1000.0 * ledger.reoccupation_count / total_evals,
        "collapsed": pop[-1] == 0,
        "population_trajectory": pop,
        "turnover_fraction_series": turnover_fraction,
    }


def capacity_fraction(occupied: Set[Cell], radius: int) -> float:
    from digital_crystal import hex_capacity

    return len(occupied) / float(hex_capacity(radius))
