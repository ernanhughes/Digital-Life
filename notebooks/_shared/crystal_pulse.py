"""Pulse-signalling extension for the Digital Crystal substrate.

Adds exactly one new mechanism on top of ``digital_crystal.py``'s frozen growth
mechanics: a sender can deliver a one-bit "pulse" event to a receiver crystal
that perturbs the receiver's environmental forcing input by a fixed additive
bump for exactly one update (``+0.65`` by default, matching the book's own
description and the canonical ``ch16``/``ch17-perturbation-dynamics-v6``
message_gain parameter). No detector, no channel capacity, no semantics, and
no persistent "received message" state is added -- the pulse only ever
perturbs the single forcing value fed into the existing, unmodified
``attachment_probability`` / ``advance_one_step`` growth rule for the step in
which it lands.

This module also provides the *common random numbers* (CRN) branch-matching
helper used throughout current-book Chapter 8: two branches that should differ
only in whether/how they are pulsed are advanced using an RNG seeded
identically per step, so a naive comparison cannot pick up spurious
differences that are really just "the two branches happened to draw different
coin flips." The book narrates discovering that *without* this discipline,
sequential-RNG coupling between conditions is a major, confirmed measurement
artifact (DL-08-C06) -- this module bakes the fix in from the start rather
than reproducing the naive (broken) version.

Faithful, reduced re-implementation in the spirit of
``scripts/books/digital-life/ch16_digital_crystal_signalling*.py`` and the
terminal ``ch17-perturbation-dynamics-v6`` matched-codeword design. Does not
import those scripts directly (heavier, version-chained, DB-backed pipelines);
reimplements the core mechanism directly against ``_shared/digital_crystal.py``.
"""

from __future__ import annotations

import math
import random as _random
from dataclasses import dataclass
from typing import Dict, List, Sequence, Set, Tuple

import numpy as np

from digital_crystal import (
    Cell,
    CrystalParams,
    CrystalState,
    advance_one_step,
    axial_to_xy,
    hex_capacity,
    neighbors,
)

PULSE_GAIN_DEFAULT = 0.65  # additive forcing bump for one step; matches book + canonical message_gain


def matched_step_state(
    occupied: Set[Cell], birth_time: Dict[Cell, int], step: int, seed_for_step: int
) -> CrystalState:
    """Build a ``CrystalState`` whose RNG is freshly seeded from ``seed_for_step``.

    Two branches built from the same ``(occupied, birth_time, step,
    seed_for_step)`` and advanced with :func:`advance_one_step` will draw the
    *identical* sequence of growth coin-flips -- this is the common-random-
    numbers (CRN) coupling that lets a FORCE/PREVENT (or codeword A/B)
    comparison attribute any resulting difference to the intervention itself,
    not to independent randomness. This is the same idiom used in
    ``notebooks/10-material-loss-and-reoccupation.ipynb``'s ``_matched_state``
    helper for the surface/interior placement comparison.
    """
    r = _random.Random(seed_for_step)
    return CrystalState(
        occupied=set(occupied),
        birth_time=dict(birth_time),
        step=step,
        rng_state=r.getstate(),
        attachments_by_step=[],
        population_by_step=[len(occupied)],
    )


def advance_with_pulse(
    state: CrystalState,
    base_input: float,
    pulse: bool,
    radius: int,
    params: CrystalParams = CrystalParams(),
    gain: float = PULSE_GAIN_DEFAULT,
) -> Tuple[CrystalState, int]:
    """One growth update. If ``pulse`` is True, the forcing input for this step
    only is bumped by ``+gain``; otherwise ordinary forcing is used. Internally
    this is nothing but a call to the unmodified ``advance_one_step`` with a
    perturbed input value -- the growth rule itself is never touched."""
    input_value = float(base_input) + (gain if pulse else 0.0)
    return advance_one_step(state, input_value, radius, params)


def run_force_prevent_pair(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    base_seed: int,
    step_index: int,
    base_input: float,
    radius: int,
    params: CrystalParams = CrystalParams(),
    gain: float = PULSE_GAIN_DEFAULT,
) -> Tuple[CrystalState, CrystalState]:
    """Advance a FORCE (pulse delivered) and PREVENT (no pulse) branch one step
    from the same starting cells/birth-times, using CRN-matched growth
    randomness, differing only in whether the pulse bump is applied this step."""
    seed_for_step = base_seed * 1_000_003 + step_index
    force_state = matched_step_state(occupied, birth_time, step, seed_for_step)
    prevent_state = matched_step_state(occupied, birth_time, step, seed_for_step)
    force_next, _ = advance_with_pulse(force_state, base_input, True, radius, params, gain)
    prevent_next, _ = advance_with_pulse(prevent_state, base_input, False, radius, params, gain)
    return force_next, prevent_next


def deliver_pulse_pattern(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: int,
    base_seed: int,
    pattern: Sequence[bool],
    base_inputs: Sequence[float],
    radius: int,
    params: CrystalParams = CrystalParams(),
    gain: float = PULSE_GAIN_DEFAULT,
) -> CrystalState:
    """Deliver a sequence of pulse/no-pulse bits (``pattern``, one per step)
    starting from ``(occupied, birth_time, step)``, advancing via CRN keyed on
    ``(base_seed, step_index)`` so two different patterns delivered from the
    same checkpoint+seed see *identical* growth randomness at every step and
    differ only in which steps receive the pulse bump. Used for both the
    shuffled-timing control and the matched-codeword test."""
    occ, bt, st = set(occupied), dict(birth_time), step
    rng_state = None
    for i, bit in enumerate(pattern):
        seed_for_step = base_seed * 1_000_003 + i
        s = matched_step_state(occ, bt, st, seed_for_step)
        nxt, _ = advance_with_pulse(s, base_inputs[i], bool(bit), radius, params, gain)
        occ, bt, st, rng_state = nxt.occupied, nxt.birth_time, nxt.step, nxt.rng_state
    return CrystalState(
        occupied=occ, birth_time=bt, step=st, rng_state=rng_state,
        attachments_by_step=[], population_by_step=[len(occ)],
    )


def normalized_symdiff(a: Set[Cell], b: Set[Cell]) -> float:
    """Symmetric difference normalized by mean population (0 if both empty)."""
    denom = max(1.0, 0.5 * (len(a) + len(b)))
    return len(a ^ b) / denom


def feature_vector(occupied: Set[Cell], radius: int) -> np.ndarray:
    """Small population-level morphology feature vector used for the
    matched-history signature test:

    [population_fraction_of_capacity, mean_coordination_degree,
     boundary_fraction, mean cos(6*theta), mean sin(6*theta)]

    The last two are a simplified stand-in for the canonical
    ``ch17-perturbation-dynamics-v6`` run's 9-dimensional "angular9" feature
    subspace (cov_anisotropy + 6 angular sectors + harmonic6_cos/sin) -- here
    collapsed to the harmonic-6 anisotropy pair plus three scalar summaries,
    disclosed as a reduced, not identical, feature set.
    """
    n = len(occupied)
    if n == 0:
        return np.zeros(5)
    cap = hex_capacity(radius)
    degrees = []
    boundary = 0
    cos_sum = 0.0
    sin_sum = 0.0
    ang_n = 0
    for c in occupied:
        deg = sum(nb in occupied for nb in neighbors(c))
        degrees.append(deg)
        if deg < 6:
            boundary += 1
        if c != (0, 0):
            x, y = axial_to_xy(c)
            theta = math.atan2(y, x)
            cos_sum += math.cos(6.0 * theta)
            sin_sum += math.sin(6.0 * theta)
            ang_n += 1
    mean_degree = float(np.mean(degrees))
    boundary_fraction = boundary / n
    cos6 = cos_sum / ang_n if ang_n else 0.0
    sin6 = sin_sum / ang_n if ang_n else 0.0
    pop_fraction = n / cap
    return np.array([pop_fraction, mean_degree, boundary_fraction, cos6, sin6])


def paired_signature_test(
    features_a: np.ndarray, features_b: np.ndarray, n_perm: int = 2000, seed: int = 0
) -> Dict[str, float]:
    """Paired, permutation-based test for a population-level feature
    signature distinguishing condition A from condition B.

    ``features_a``/``features_b``: arrays of shape (n_replicates, k), paired
    by replicate (same starting checkpoint + CRN-matched growth randomness,
    differing only in which pattern -- A or B -- was delivered).

    Statistic: squared norm of the standardized mean paired-difference vector
    -- a simplified, un-ridged analogue of the canonical
    ``paired_ridge_hotelling_angular9`` statistic used in
    ``ch17-perturbation-dynamics-v6``. Null: independently flip the sign of
    each replicate's paired difference (valid under the null that A and B are
    exchangeable within a matched pair), matching the logic of the canonical
    matched-codeword permutation test.
    """
    diff = features_a - features_b
    std = diff.std(axis=0, ddof=1)
    std = np.where(std < 1e-12, 1.0, std)
    standardized = diff / std

    def _stat(d: np.ndarray) -> float:
        return float(np.sum(np.mean(d, axis=0) ** 2))

    observed = _stat(standardized)
    rng = np.random.default_rng(seed)
    n = standardized.shape[0]
    null = np.empty(n_perm)
    for i in range(n_perm):
        signs = rng.choice(np.array([-1.0, 1.0]), size=n)
        null[i] = _stat(standardized * signs[:, None])
    p_value = float(np.mean(null >= observed))
    return {
        "statistic": observed,
        "p_value": p_value,
        "null_mean": float(null.mean()),
        "null_q95": float(np.quantile(null, 0.95)),
        "n_replicates": n,
        "n_perm": n_perm,
    }


def validate_codeword_match(a: str, b: str) -> Dict[str, object]:
    """Confirm two bitstring codewords are matched on pulse count, first pulse
    position, and last pulse position (only interior arrangement differs) --
    mirrors the canonical run's ``matched_codeword_validation`` block."""
    count_a, count_b = a.count("1"), b.count("1")
    first_a, first_b = a.index("1"), b.index("1")
    last_a, last_b = len(a) - 1 - a[::-1].index("1"), len(b) - 1 - b[::-1].index("1")
    return {
        "pulse_count_a": count_a,
        "pulse_count_b": count_b,
        "first_pulse_a": first_a,
        "first_pulse_b": first_b,
        "last_pulse_a": last_a,
        "last_pulse_b": last_b,
        "same_pulse_count": count_a == count_b,
        "same_first_pulse": first_a == first_b,
        "same_last_pulse": last_a == last_b,
    }
