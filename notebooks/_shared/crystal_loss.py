"""Material-loss extension for the Digital Crystal substrate.

Adds exactly one new rule on top of ``digital_crystal.py``'s frozen growth
mechanics: an occupied cell can become empty with independent probability
``delta`` after the ordinary growth step. No repair, maintenance, resource
budget, metabolism, or target morphology is added.

This module is a faithful, reduced re-implementation of the mechanism in
``scripts/books/digital-life/ch20_digital_crystal_material_loss_v1.py``
(surface/interior classification, cell-keyed hash-based loss decisions,
exact-budget matched placement). It does not import that script directly
because the script depends on the heavier Chapter 18 "material state"
module, which this experiment does not need — Chapter 10's claims only
concern the plain occupied/empty crystal plus loss, not the hidden
material trace introduced in Chapters 9/15.
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
    CrystalState,
    advance_one_step,
    initial_state,
    neighbors,
)


@dataclass
class LossCrystalState:
    """Same shape as CrystalState, plus per-step loss bookkeeping."""

    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    attachments_by_step: List[int]
    population_by_step: List[int]
    losses_by_step: List[int] = field(default_factory=list)

    @staticmethod
    def from_crystal_state(state: CrystalState) -> "LossCrystalState":
        return LossCrystalState(
            occupied=set(state.occupied),
            birth_time=dict(state.birth_time),
            step=state.step,
            rng_state=state.rng_state,
            attachments_by_step=list(state.attachments_by_step),
            population_by_step=list(state.population_by_step),
            losses_by_step=[0] * len(state.population_by_step),
        )

    def clone(self) -> "LossCrystalState":
        import copy

        return LossCrystalState(
            occupied=set(self.occupied),
            birth_time=dict(self.birth_time),
            step=self.step,
            rng_state=copy.deepcopy(self.rng_state),
            attachments_by_step=list(self.attachments_by_step),
            population_by_step=list(self.population_by_step),
            losses_by_step=list(self.losses_by_step),
        )


def boundary_and_interior(occupied: Set[Cell]) -> Tuple[List[Cell], List[Cell]]:
    """Split occupied cells into surface (<6 occupied neighbours) vs interior (6/6)."""
    surface: List[Cell] = []
    interior: List[Cell] = []
    for cell in sorted(occupied):
        degree = sum(nb in occupied for nb in neighbors(cell))
        if degree < 6:
            surface.append(cell)
        else:
            interior.append(cell)
    return surface, interior


def hole_count(occupied: Set[Cell]) -> int:
    """Count empty cells completely surrounded by occupied neighbours."""
    candidates: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied:
                candidates.add(nb)
    return sum(all(nb in occupied for nb in neighbors(cell)) for cell in candidates)


def loss_uniform(stream_seed: int, step: int, cell: Cell, tag: str = "material-loss-v1") -> float:
    """Cell-keyed deterministic uniform in [0, 1) for the loss decision.

    Independent of the growth-step RNG stream (which is threaded sequentially
    through ``advance_one_step``), so adding a loss rule cannot silently
    perturb the growth RNG's draw sequence.
    """
    payload = f"{stream_seed}|{step}|{cell[0]}|{cell[1]}|{tag}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def apply_probability_loss(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    stream_seed: int,
    step: int,
    loss_rate: float,
    policy: str = "uniform",
) -> Tuple[Set[Cell], Dict[Cell, int], int]:
    """Apply loss AFTER growth. Any emptied location can be reoccupied by
    ordinary growth on a later update -- no explicit repair operator exists."""
    surface, interior = boundary_and_interior(occupied)
    if policy == "uniform":
        eligible = sorted(occupied)
    elif policy == "surface":
        eligible = surface
    elif policy == "interior":
        eligible = interior
    else:
        raise ValueError(policy)

    lost = [c for c in eligible if loss_uniform(stream_seed, step, c) < float(loss_rate)]

    occupied_out = set(occupied)
    birth_out = dict(birth_time)
    for c in lost:
        occupied_out.discard(c)
        birth_out.pop(c, None)
    return occupied_out, birth_out, len(lost)


def choose_exact_loss_targets(
    eligible: Sequence[Cell], stream_seed: int, step: int, budget: int
) -> List[Cell]:
    """Deterministically rank `eligible` by the loss-hash and take the lowest `budget`."""
    if budget < 0 or budget > len(eligible):
        raise ValueError(f"Invalid loss budget={budget}, eligible={len(eligible)}")
    return sorted(eligible, key=lambda cell: (loss_uniform(stream_seed, step, cell), cell))[:budget]


def apply_exact_loss_targets(
    occupied: Set[Cell], birth_time: Dict[Cell, int], targets: Sequence[Cell]
) -> Tuple[Set[Cell], Dict[Cell, int]]:
    occupied_out = set(occupied)
    birth_out = dict(birth_time)
    for c in targets:
        occupied_out.discard(c)
        birth_out.pop(c, None)
    return occupied_out, birth_out


def growth_then_probability_loss(
    state: CrystalState,
    input_value: float,
    loss_rate: float,
    radius: int,
    params: CrystalParams,
    policy: str = "uniform",
    stream_seed: int = 0,
) -> Tuple[CrystalState, int, int]:
    """One update: canonical growth, then independent keyed probability loss."""
    grown, additions = advance_one_step(state, input_value, radius, params)
    occ, bt, losses = apply_probability_loss(
        grown.occupied, grown.birth_time, stream_seed, grown.step, loss_rate, policy
    )
    out = CrystalState(
        occupied=occ,
        birth_time=bt,
        step=grown.step,
        rng_state=grown.rng_state,
        attachments_by_step=grown.attachments_by_step,
        population_by_step=grown.population_by_step[:-1] + [len(occ)],
    )
    return out, additions, losses


def make_environment(steps: int, seed: int) -> np.ndarray:
    """Smooth stochastic forcing signal: two sinusoids + drift + noise, normalized to [-1, 1]."""
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)
    p1 = rng.uniform(11.0, 19.0)
    p2 = rng.uniform(23.0, 37.0)
    ph1 = rng.uniform(0.0, 2 * np.pi)
    ph2 = rng.uniform(0.0, 2 * np.pi)
    deterministic = 0.55 * np.sin(2 * np.pi * t / p1 + ph1) + 0.25 * np.sin(2 * np.pi * t / p2 + ph2)
    drift_raw = np.cumsum(rng.normal(0.0, 0.10, size=steps))
    drift = 0.18 * _normalize(drift_raw)
    noise = rng.normal(0.0, 0.08, size=steps)
    return _normalize(deterministic + drift + noise)


def _normalize(x: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(x)) if len(x) else 1.0
    if peak < 1e-12:
        return x
    return x / peak


def warm_checkpoint(env: np.ndarray, warmup_steps: int, seed: int, radius: int, params: CrystalParams) -> CrystalState:
    state = initial_state(seed)
    for t in range(warmup_steps):
        state, _ = advance_one_step(state, float(env[t]), radius, params)
    return state


def normalized_late_slope(population: Sequence[int], late_window: int) -> Tuple[float, float]:
    """Linear-fit slope over the last `late_window` steps, normalized by the window's mean population."""
    y = np.asarray(population[-late_window:], dtype=float)
    x = np.arange(len(y), dtype=float)
    if len(y) >= 2 and np.mean(y) > 0:
        slope = float(np.polyfit(x, y, 1)[0])
        return slope, slope / float(np.mean(y))
    return 0.0, 0.0
