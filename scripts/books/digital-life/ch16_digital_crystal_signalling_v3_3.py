#!/usr/bin/env python3
"""
Digital Life — Chapter 16
Before There Are Messages, There Are Pulses
===========================================

Experiment version: digital-crystal-signalling-v3.3

Question
--------
Can an event produced by one Digital Crystal cause a measurable change in
another Digital Crystal, and can that effect be distinguished from timing-
destroyed and unrelated message controls?

This deliberately does NOT test language, semantics, cooperation, planning,
coordination, agency, individuality, learning, intelligence, or life.

The experiment is staged:

    Stage 0  Freeze Digital Crystal v1 and check reproducibility invariants.
    Stage 1  Build an endogenous one-bit sender stream from sender growth events.
    Stage 2  Exact receiver counterfactual: one received bit vs no bit.
    Stage 3  Compare real stream with no-channel, shuffled, unrelated-replay,
             and rate-matched-random controls.
    Stage 4  Estimate a causal impulse-response curve and latency/decay.
    Stage 5  Test propagation through a six-crystal nearest-neighbour chain.
    Stage 6  Run a 2-D local "Crystal Board" with no target/task.
    Stage 7  Emit a bounded verdict.

Kill conditions
---------------
A. If inserting one bit into an otherwise identical receiver checkpoint does
   not reliably alter subsequent Digital Crystal growth, the channel is
   decorative.

B. If the real sender-generated message stream is not distinguishable from
   shuffled, count-matched unrelated-replay, exact-IPI-surrogate, and
   rate-matched-random controls, we do NOT call the result sender-specific
   signalling.

The strongest possible verdict is therefore intentionally narrow:

    SENDER_SPECIFIC_SIGNALLING_SUPPORTED

A weaker but still useful result is:

    CAUSAL_TRANSMISSION_SUPPORTED

meaning a received bit causally changes the receiver, but the sender's actual
event timing has not been shown to matter beyond generic forcing.

Recommended:
    python ch16_digital_crystal_signalling_v2.py --profile quick
    python ch16_digital_crystal_signalling_v2.py --profile standard
    python ch16_digital_crystal_signalling_v2.py --profile full

Use --force only to document intent; this script recomputes by default.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from tqdm import tqdm


MODEL_VERSION = "digital-crystal-v1-frozen"
SIGNALLING_VERSION = "digital-crystal-signalling-v3.3"
SCHEMA_VERSION = 3

Cell = Tuple[int, int]
HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)

PROFILES = {
    "quick": {
        "pair_steps": 48,
        "crystal_radius": 34,
        "pair_replicates": 12,
        "intervention_replicates": 24,
        "impulse_horizon": 8,
        "message_gain": 0.65,
        "pulse_window": 8,
        "pulse_sigma": 0.65,
        "min_pulse_attachments": 2,
        "chain_length": 6,
        "chain_steps": 48,
        "chain_replicates": 6,
        "board_width": 6,
        "board_height": 6,
        "board_steps": 48,
        "board_replicates": 3,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "pair_steps": 72,
        "crystal_radius": 48,
        "pair_replicates": 30,
        "intervention_replicates": 60,
        "impulse_horizon": 10,
        "message_gain": 0.65,
        "pulse_window": 10,
        "pulse_sigma": 0.75,
        "min_pulse_attachments": 3,
        "chain_length": 6,
        "chain_steps": 72,
        "chain_replicates": 15,
        "board_width": 6,
        "board_height": 6,
        "board_steps": 72,
        "board_replicates": 8,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "pair_steps": 90,
        "crystal_radius": 56,
        "pair_replicates": 60,
        "intervention_replicates": 120,
        "impulse_horizon": 12,
        "message_gain": 0.65,
        "pulse_window": 12,
        "pulse_sigma": 0.75,
        "min_pulse_attachments": 3,
        "chain_length": 6,
        "chain_steps": 90,
        "chain_replicates": 30,
        "board_width": 6,
        "board_height": 6,
        "board_steps": 90,
        "board_replicates": 15,
        "max_capacity_fraction": 0.85,
    },
}


# ---------------------------------------------------------------------------
# Digital Crystal v1 — frozen growth rule
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CrystalParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


@dataclass
class CrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    attachments_by_step: List[int]
    population_by_step: List[int]


@dataclass
class RunResult:
    state: CrystalState
    attachments: np.ndarray
    population: np.ndarray


@dataclass
class PulseRule:
    window: int
    sigma: float
    min_attachments: int


def neighbors(cell: Cell) -> Iterable[Cell]:
    q, r = cell
    for dq, dr in HEX_DIRECTIONS:
        yield q + dq, r + dr


def hex_distance(cell: Cell) -> int:
    q, r = cell
    s = -q - r
    return max(abs(q), abs(r), abs(s))


def axial_to_xy(cell: Cell) -> Tuple[float, float]:
    q, r = cell
    return math.sqrt(3.0) * (q + r / 2.0), 1.5 * r


def logistic(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def local_exposure_angle(cell: Cell, occupied: Set[Cell]) -> float:
    x, y = axial_to_xy(cell)
    vx = 0.0
    vy = 0.0
    count = 0
    for nb in neighbors(cell):
        if nb in occupied:
            nx, ny = axial_to_xy(nb)
            vx += x - nx
            vy += y - ny
            count += 1
    if count == 0 or abs(vx) + abs(vy) < 1e-12:
        return 0.0
    return math.atan2(vy, vx)


def initial_state(seed: int) -> CrystalState:
    rng = random.Random(seed)
    return CrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        step=0,
        rng_state=rng.getstate(),
        attachments_by_step=[1],
        population_by_step=[1],
    )


def clone_state(state: CrystalState) -> CrystalState:
    return CrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        step=state.step,
        rng_state=copy.deepcopy(state.rng_state),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
    )


def morphology_hash(state: CrystalState) -> str:
    payload = json.dumps(
        sorted((int(q), int(r)) for q, r in state.occupied),
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def normalized_state_difference(a: Set[Cell], b: Set[Cell]) -> float:
    union = a.union(b)
    return len(a.symmetric_difference(b)) / max(1, len(union))


def advance_one_step(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: CrystalParams,
) -> Tuple[CrystalState, int]:
    """
    Frozen Digital Crystal v1 growth rule.

    Reproducibility invariant inherited from Chapter 15:
    RNG-consuming frontier traversal is canonicalized with sorted(frontier).
    """
    rng = random.Random()
    rng.setstate(state.rng_state)

    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)

    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions: List[Cell] = []
    for cell in sorted(frontier):
        n = sum(nb in occupied for nb in neighbors(cell))
        theta = local_exposure_angle(cell, occupied)
        phase = params.signal_phase_gain * float(input_value)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)
        score = (
            params.base_bias
            + params.neighbor_gain * n
            + params.signal_rate_gain * float(input_value)
            + params.anisotropy_gain * anisotropy
            - params.crowding_penalty * crowding
        )
        if rng.random() < logistic(score):
            additions.append(cell)

    next_step = state.step + 1
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    next_state = CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=next_step,
        rng_state=rng.getstate(),
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
    )
    return next_state, len(additions)


def run_signal(
    state: CrystalState,
    signal: np.ndarray,
    max_radius: int,
    params: CrystalParams,
) -> RunResult:
    current = clone_state(state)
    attachments: List[int] = []
    for value in signal:
        current, n = advance_one_step(current, float(value), max_radius, params)
        attachments.append(n)
    return RunResult(
        state=current,
        attachments=np.asarray(attachments, dtype=float),
        population=np.asarray(current.population_by_step, dtype=float),
    )


# ---------------------------------------------------------------------------
# Signals and endogenous pulse extraction
# ---------------------------------------------------------------------------

def normalize_signal(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if len(x) == 0:
        return x
    x = x - float(np.mean(x))
    m = float(np.max(np.abs(x)))
    if m > 0:
        x = x / m
    return np.clip(x, -1.0, 1.0)


def make_environment(steps: int, seed: int) -> np.ndarray:
    """
    Composite external environment. Sender and receiver use independently seeded
    versions so raw environmental correlation cannot masquerade as signalling.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)
    p1 = rng.uniform(11.0, 19.0)
    p2 = rng.uniform(23.0, 37.0)
    ph1 = rng.uniform(0.0, 2 * np.pi)
    ph2 = rng.uniform(0.0, 2 * np.pi)
    deterministic = (
        0.55 * np.sin((2 * np.pi * t / p1) + ph1)
        + 0.25 * np.sin((2 * np.pi * t / p2) + ph2)
    )
    drift = 0.18 * normalize_signal(np.cumsum(rng.normal(0.0, 0.10, size=steps)))
    noise = rng.normal(0.0, 0.08, size=steps)
    return normalize_signal(deterministic + drift + noise)


def pulses_from_attachments(
    attachments: np.ndarray,
    rule: PulseRule,
) -> np.ndarray:
    """
    Endogenous one-bit event:

        pulse_t = 1

    when the current attachment count is unusually high relative to the
    sender's own recent attachment history.

    The rule uses only sender-generated growth activity. No global timer or
    receiver state enters emission.
    """
    x = np.asarray(attachments, dtype=float)
    pulses = np.zeros(len(x), dtype=np.int8)

    for t in range(len(x)):
        if t < rule.window:
            continue
        hist = x[t - rule.window:t]
        mu = float(np.mean(hist))
        sd = float(np.std(hist))
        threshold = max(
            float(rule.min_attachments),
            mu + rule.sigma * max(sd, 1.0),
        )
        if x[t] >= threshold:
            pulses[t] = 1

    return pulses


def deliver_with_one_step_delay(pulses: np.ndarray) -> np.ndarray:
    out = np.zeros_like(pulses)
    if len(pulses) > 1:
        out[1:] = pulses[:-1]
    return out


def message_forcing(
    base_environment: np.ndarray,
    messages: np.ndarray,
    gain: float,
) -> np.ndarray:
    return np.asarray(base_environment, dtype=float) + gain * np.asarray(messages, dtype=float)


def shuffled_stream(stream: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = np.array(stream, copy=True)
    rng.shuffle(out)
    return out


def rate_matched_random_stream(stream: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(stream)
    k = int(np.sum(stream))
    out = np.zeros(n, dtype=np.int8)
    if k > 0:
        idx = rng.choice(n, size=min(k, n), replace=False)
        out[idx] = 1
    return out


def hex_disk_capacity(radius: int) -> int:
    """Number of cells in a completely filled axial hex disk of radius r."""
    return 1 + 3 * radius * (radius + 1)


def capacity_fraction(state: CrystalState, radius: int) -> float:
    return len(state.occupied) / float(hex_disk_capacity(radius))


def assert_not_saturated(
    label: str,
    state: CrystalState,
    radius: int,
    max_fraction: float,
) -> float:
    """
    Endpoint morphology is scientifically uninformative once the hard growth
    disk is nearly full: different trajectories collapse onto the same disk.

    Fail loudly rather than silently interpret a saturated endpoint.
    """
    frac = capacity_fraction(state, radius)
    if frac >= max_fraction:
        raise RuntimeError(
            f"{label} reached {frac:.3f} of hard-radius capacity "
            f"(guard={max_fraction:.3f}). Reduce steps or increase radius."
        )
    return frac


def pulse_positions(stream: np.ndarray) -> np.ndarray:
    return np.flatnonzero(np.asarray(stream, dtype=np.int8))


def inter_pulse_intervals(stream: np.ndarray) -> np.ndarray:
    pos = pulse_positions(stream)
    if len(pos) < 2:
        return np.asarray([], dtype=int)
    return np.diff(pos)


def pulse_structure(stream: np.ndarray) -> dict:
    """
    Diagnostics for the temporal structure of a one-bit stream.
    """
    x = np.asarray(stream, dtype=np.int8)
    pos = pulse_positions(x)
    gaps = inter_pulse_intervals(x)
    if len(x) > 1 and float(np.std(x[:-1])) > 0 and float(np.std(x[1:])) > 0:
        lag1 = float(np.corrcoef(x[:-1], x[1:])[0, 1])
    else:
        lag1 = 0.0
    return {
        "length": int(len(x)),
        "pulse_count": int(np.sum(x)),
        "pulse_rate": float(np.mean(x)) if len(x) else 0.0,
        "first_pulse": int(pos[0]) if len(pos) else None,
        "last_pulse": int(pos[-1]) if len(pos) else None,
        "ipi_mean": float(np.mean(gaps)) if len(gaps) else None,
        "ipi_std": float(np.std(gaps)) if len(gaps) else None,
        "ipi_median": float(np.median(gaps)) if len(gaps) else None,
        "lag1_autocorrelation": lag1,
    }


def count_match_unrelated_stream(
    real_stream: np.ndarray,
    unrelated_stream: np.ndarray,
    seed: int,
) -> np.ndarray:
    """
    Preserve the broad timing geometry of an unrelated sender while forcing
    its pulse count to exactly equal the real sender's pulse count.

    If too many unrelated pulses exist, subsample them.
    If too few exist, add pulses preferentially near existing unrelated
    pulse neighbourhoods before filling any remaining deficit randomly.

    This is stricter than raw unrelated replay because pulse count cannot
    explain a real-vs-unrelated difference.
    """
    rng = np.random.default_rng(seed)
    real = np.asarray(real_stream, dtype=np.int8)
    other = np.asarray(unrelated_stream, dtype=np.int8)
    n = len(real)
    target = int(np.sum(real))
    out = np.zeros(n, dtype=np.int8)
    pos = list(map(int, np.flatnonzero(other)))

    if len(pos) >= target:
        if target:
            keep = rng.choice(np.asarray(pos, dtype=int), size=target, replace=False)
            out[keep] = 1
        return out

    for p in pos:
        out[p] = 1

    deficit = target - len(pos)
    if deficit <= 0:
        return out

    candidates = []
    for p in pos:
        for d in (-2, -1, 1, 2):
            q = p + d
            if 0 <= q < n and out[q] == 0:
                candidates.append(q)
    candidates = list(dict.fromkeys(candidates))
    rng.shuffle(candidates)

    for q in candidates[:deficit]:
        out[q] = 1
    deficit = target - int(np.sum(out))

    if deficit > 0:
        remaining = np.flatnonzero(out == 0)
        if len(remaining):
            add = rng.choice(remaining, size=min(deficit, len(remaining)), replace=False)
            out[add] = 1
    return out


def ipi_permutation_surrogate(stream: np.ndarray, seed: int) -> np.ndarray:
    """
    Preserve pulse count and the exact multiset of inter-pulse intervals while
    destroying their original order.

    This is a strong temporal-structure control:
        same number of bits
        same IPI distribution exactly
        different chronology
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(stream, dtype=np.int8)
    n = len(x)
    pos = pulse_positions(x)
    out = np.zeros(n, dtype=np.int8)

    if len(pos) == 0:
        return out
    if len(pos) == 1:
        out[int(pos[0])] = 1
        return out

    gaps = list(map(int, np.diff(pos)))
    rng.shuffle(gaps)

    span = int(sum(gaps))
    max_start = max(0, n - 1 - span)
    start = int(rng.integers(0, max_start + 1)) if max_start > 0 else 0

    p = start
    out[p] = 1
    for gap in gaps:
        p += gap
        if p >= n:
            break
        out[p] = 1
    return out


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) != len(b) or len(a) < 3:
        return 0.0
    if float(np.std(a)) < 1e-12 or float(np.std(b)) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def lagged_corr(messages: np.ndarray, response: np.ndarray, max_lag: int) -> List[float]:
    out = []
    m = np.asarray(messages, dtype=float)
    r = np.asarray(response, dtype=float)
    for lag in range(max_lag + 1):
        if lag == 0:
            out.append(safe_corr(m, r))
        elif len(m) > lag:
            out.append(safe_corr(m[:-lag], r[lag:]))
        else:
            out.append(0.0)
    return out


def summarize(values: Sequence[float]) -> dict:
    x = np.asarray(list(values), dtype=float)
    if len(x) == 0:
        return {
            "n": 0, "mean": 0.0, "std": 0.0, "median": 0.0,
            "q05": 0.0, "q25": 0.0, "q75": 0.0, "q95": 0.0,
            "min": 0.0, "max": 0.0,
        }
    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "std": float(np.std(x)),
        "median": float(np.median(x)),
        "q05": float(np.quantile(x, 0.05)),
        "q25": float(np.quantile(x, 0.25)),
        "q75": float(np.quantile(x, 0.75)),
        "q95": float(np.quantile(x, 0.95)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def pairwise_superiority(a: Sequence[float], b: Sequence[float]) -> float:
    """P(A > B) over all observed cross-pairs, ties count as 0.5."""
    aa = np.asarray(list(a), dtype=float)
    bb = np.asarray(list(b), dtype=float)
    if len(aa) == 0 or len(bb) == 0:
        return 0.5
    gt = 0.0
    total = 0
    for x in aa:
        gt += float(np.sum(x > bb))
        gt += 0.5 * float(np.sum(x == bb))
        total += len(bb)
    return gt / max(1, total)


def post_message_response(
    messages: np.ndarray,
    attachments: np.ndarray,
    horizon: int = 3,
) -> float:
    vals: List[float] = []
    for t in np.flatnonzero(messages):
        start = int(t)
        end = min(len(attachments), start + horizon)
        if end > start:
            vals.append(float(np.mean(attachments[start:end])))
    return float(np.mean(vals)) if vals else 0.0


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections: List[str] = []

    def json(self, name: str, obj: object) -> None:
        (self.root / name).write_text(
            json.dumps(obj, indent=2, sort_keys=False),
            encoding="utf-8",
        )

    def stage(self, name: str, title: str, body: str) -> None:
        text = f"# {title}\n\n{body.strip()}\n"
        (self.root / name).write_text(text, encoding="utf-8")
        self.sections.append(text)

    def full(self, metadata: dict) -> Path:
        path = self.root / "ch16-full-experimental-report.md"
        text = (
            "# Chapter 16 — Before There Are Messages: Full Experimental Report\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
            + "\n\n".join(self.sections)
            + "\n"
        )
        path.write_text(text, encoding="utf-8")
        return path


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def draw_crystal(ax, state: CrystalState, title: str) -> None:
    if not state.occupied:
        ax.set_title(title)
        ax.axis("off")
        return
    births = np.asarray(list(state.birth_time.values()), dtype=float)
    bmin = float(np.min(births))
    bmax = float(np.max(births))
    denom = max(1.0, bmax - bmin)

    for cell in state.occupied:
        x, y = axial_to_xy(cell)
        value = (state.birth_time.get(cell, 0) - bmin) / denom
        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=0.92,
            orientation=np.pi / 6,
            facecolor=plt.cm.viridis(value),
            edgecolor="none",
        )
        ax.add_patch(patch)

    pts = np.asarray([axial_to_xy(c) for c in state.occupied], dtype=float)
    margin = 2.5
    ax.set_xlim(float(pts[:, 0].min() - margin), float(pts[:, 0].max() + margin))
    ax.set_ylim(float(pts[:, 1].min() - margin), float(pts[:, 1].max() + margin))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)


def save_sender_receiver_figure(
    sender_attachments: np.ndarray,
    pulses: np.ndarray,
    receiver_attachments: np.ndarray,
    path: Path,
) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(sender_attachments)
    axes[0].set_ylabel("sender additions")
    axes[0].set_title("Endogenous sender growth")

    axes[1].step(np.arange(len(pulses)), pulses, where="post")
    axes[1].set_ylabel("pulse")
    axes[1].set_ylim(-0.1, 1.1)
    axes[1].set_title("One-bit message stream (delivered with one-step delay)")

    axes[2].plot(receiver_attachments)
    axes[2].set_ylabel("receiver additions")
    axes[2].set_xlabel("step")
    axes[2].set_title("Receiver growth activity")

    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_intervention_figure(impulse: np.ndarray, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(impulse))
    ax.axhline(0.0, linestyle="--")
    ax.plot(x, impulse, marker="o")
    ax.set_xlabel("steps after inserted bit")
    ax.set_ylabel("mean attachment difference: pulse - no pulse")
    ax.set_title("Receiver causal impulse response")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_control_figure(control_summary: dict, path: Path) -> None:
    labels = list(control_summary)
    vals = [control_summary[k]["peak_lagged_corr"]["mean"] for k in labels]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, vals)
    ax.set_ylabel("mean peak lagged message→growth correlation")
    ax.set_title("Does real sender timing beat message controls?")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_chain_figure(chain_summary: dict, path: Path) -> None:
    real = chain_summary["real"]["mean_source_to_node_pulse_corr"]
    control = chain_summary["shuffled_edges"]["mean_source_to_node_pulse_corr"]
    x = np.arange(len(real))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, real, marker="o", label="real chain")
    ax.plot(x, control, marker="o", label="shuffled-edge control")
    ax.set_xlabel("node index / distance from source")
    ax.set_ylabel("source-to-node pulse correlation")
    ax.set_title("Does one-bit influence propagate through a chain?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_board_figure(
    pulse_rate: np.ndarray,
    activity: np.ndarray,
    width: int,
    height: int,
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    im0 = axes[0].imshow(pulse_rate.reshape(height, width))
    axes[0].set_title("Pulse rate per crystal")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    fig.colorbar(im0, ax=axes[0], fraction=0.046)

    im1 = axes[1].imshow(activity.reshape(height, width))
    axes[1].set_title("Mean growth activity per crystal")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    fig.colorbar(im1, ax=axes[1], fraction=0.046)

    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Stage helpers
# ---------------------------------------------------------------------------

def generate_sender(
    steps: int,
    max_radius: int,
    params: CrystalParams,
    pulse_rule: PulseRule,
    env_seed: int,
    crystal_seed: int,
) -> Tuple[np.ndarray, RunResult, np.ndarray]:
    env = make_environment(steps, env_seed)
    sender = run_signal(initial_state(crystal_seed), env, max_radius, params)
    raw_pulses = pulses_from_attachments(sender.attachments, pulse_rule)
    delivered = deliver_with_one_step_delay(raw_pulses)
    return env, sender, delivered


def run_receiver_condition(
    base_env: np.ndarray,
    messages: np.ndarray,
    gain: float,
    seed: int,
    max_radius: int,
    params: CrystalParams,
) -> RunResult:
    forcing = message_forcing(base_env, messages, gain)
    return run_signal(initial_state(seed), forcing, max_radius, params)


def evaluate_condition(
    messages: np.ndarray,
    receiver: RunResult,
    no_channel: RunResult,
    max_lag: int,
    radius: int,
) -> dict:
    corrs = lagged_corr(messages, receiver.attachments, max_lag=max_lag)
    return {
        "pulse_count": int(np.sum(messages)),
        "pulse_rate": float(np.mean(messages)) if len(messages) else 0.0,
        "peak_lagged_corr": float(max(corrs)) if corrs else 0.0,
        "peak_lag": int(np.argmax(corrs)) if corrs else 0,
        "lagged_corr": corrs,
        "post_message_growth": post_message_response(messages, receiver.attachments, 3),
        "final_population": int(len(receiver.state.occupied)),
        "capacity_fraction": capacity_fraction(receiver.state, radius),
        "final_difference_vs_no_channel": normalized_state_difference(
            receiver.state.occupied,
            no_channel.state.occupied,
        ),
    }


# ---------------------------------------------------------------------------
# Stages
# ---------------------------------------------------------------------------

def stage_0_reproducibility(
    reporter: Reporter,
    params: CrystalParams,
    max_radius: int,
    seed: int,
) -> dict:
    print("\n=== STAGE 0 — REPRODUCIBILITY INVARIANT ===")
    env = make_environment(24, seed + 1)
    state = initial_state(seed + 2)
    a = run_signal(clone_state(state), env, max_radius, params)
    b = run_signal(clone_state(state), env, max_radius, params)
    exact = (
        a.state.occupied == b.state.occupied
        and a.state.rng_state == b.state.rng_state
        and np.array_equal(a.attachments, b.attachments)
    )
    result = {
        "canonical_rng_traversal": "sorted(frontier)",
        "repeat_from_identical_state_exact": bool(exact),
        "morphology_hash_a": morphology_hash(a.state),
        "morphology_hash_b": morphology_hash(b.state),
    }
    if not exact:
        raise RuntimeError("Stage 0 reproducibility invariant failed.")
    reporter.json("stage-00-reproducibility.json", result)
    reporter.stage(
        "stage-00-reproducibility.md",
        "Stage 0 — Freeze the Substrate",
        f"""
Digital Crystal v1 is unchanged from Chapter 15. RNG-consuming frontier
traversal remains canonicalized with `sorted(frontier)`.

```json
{json.dumps(result, indent=2)}
```

This stage must pass before any message experiment is interpreted.
""",
    )
    return result


def stage_1_endogenous_sender(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 1 — ENDOGENOUS ONE-BIT SENDER ===")

    rule = PulseRule(
        window=profile["pulse_window"],
        sigma=profile["pulse_sigma"],
        min_attachments=profile["min_pulse_attachments"],
    )

    requested_steps = profile["pair_steps"]
    radius = profile["crystal_radius"]
    gain = profile["message_gain"]
    guard = profile["max_capacity_fraction"]

    sender_env = make_environment(requested_steps, seed + 100)
    receiver_env = make_environment(requested_steps, seed + 300)

    sender_state = initial_state(seed + 200)
    receiver_state = initial_state(seed + 400)

    sender_hist: List[int] = []
    receiver_hist: List[int] = []
    messages = np.zeros(requested_steps, dtype=np.int8)

    safe_steps = 0
    first_unsafe_step = None
    sender_capacity_at_safe = capacity_fraction(sender_state, radius)
    receiver_capacity_at_safe = capacity_fraction(receiver_state, radius)

    for t in range(requested_steps):
        # Sender advances first and emits from its own growth history.
        next_sender, sender_added = advance_one_step(
            sender_state,
            float(sender_env[t]),
            radius,
            params,
        )

        trial_sender_hist = sender_hist + [sender_added]
        emitted_now = 0
        arr = np.asarray(trial_sender_hist, dtype=float)
        if len(arr) > rule.window:
            p = pulses_from_attachments(arr, rule)
            emitted_now = int(p[-1])

        # One-step delivery delay: receiver at t receives sender pulse from t-1.
        incoming = int(messages[t - 1]) if t > 0 else 0

        next_receiver, receiver_added = advance_one_step(
            receiver_state,
            float(receiver_env[t]) + gain * incoming,
            radius,
            params,
        )

        sender_frac = capacity_fraction(next_sender, radius)
        receiver_frac = capacity_fraction(next_receiver, radius)

        # Keep one common safe prefix for sender and receiver.
        if max(sender_frac, receiver_frac) >= guard:
            first_unsafe_step = t + 1
            break

        sender_state = next_sender
        receiver_state = next_receiver
        sender_hist = trial_sender_hist
        receiver_hist.append(receiver_added)
        messages[t] = emitted_now
        safe_steps = t + 1
        sender_capacity_at_safe = sender_frac
        receiver_capacity_at_safe = receiver_frac

    minimum_steps = max(rule.window + 6, 16)
    if safe_steps < minimum_steps:
        raise RuntimeError(
            "No scientifically usable common Stage-1 sender/receiver horizon "
            f"before saturation: safe_steps={safe_steps}, "
            f"minimum_steps={minimum_steps}, guard={guard:.3f}. "
            "Increase radius or reduce message gain."
        )

    sender_attachments = np.asarray(sender_hist, dtype=float)
    receiver_attachments = np.asarray(receiver_hist, dtype=float)
    messages = messages[:safe_steps]

    fig = image_dir / "ch16-01-sender-pulses-receiver.png"
    save_sender_receiver_figure(
        sender_attachments,
        messages,
        receiver_attachments,
        fig,
    )

    result = {
        "pulse_rule": asdict(rule),
        "requested_steps": requested_steps,
        "common_safe_horizon": safe_steps,
        "first_unsafe_step": first_unsafe_step,
        "sender_final_population": int(len(sender_state.occupied)),
        "sender_capacity_fraction": float(sender_capacity_at_safe),
        "message_count": int(np.sum(messages)),
        "message_rate": float(np.mean(messages)) if len(messages) else 0.0,
        "message_structure": pulse_structure(messages),
        "receiver_final_population": int(len(receiver_state.occupied)),
        "receiver_capacity_fraction": float(receiver_capacity_at_safe),
        "saturation_guard": guard,
        "figure": str(fig),
    }

    reporter.json("stage-01-endogenous-sender.json", result)
    reporter.stage(
        "stage-01-endogenous-sender.md",
        "Stage 1 — Before There Are Messages, There Are Pulses",
        f"""
A sender Digital Crystal emits one bit only when its own current attachment
activity exceeds a threshold derived from its recent attachment history.

The sender and receiver are advanced together and the stage stops at the
longest **common** horizon for which both remain below the hard-radius
saturation guard of `{guard:.2f}`.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`

The pulse has no semantics. It means only: an endogenous sender event occurred.
""",
    )
    return result


def stage_2_single_bit_intervention(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 2 — ONE BIT VS NO BIT ===")
    horizon = profile["impulse_horizon"]
    nrep = profile["intervention_replicates"]
    gain = profile["message_gain"]
    max_radius = profile["crystal_radius"]

    differences: List[float] = []
    symmetric_cells: List[int] = []
    changed: List[int] = []
    impulse_matrix: List[List[float]] = []

    for rep in tqdm(range(nrep), desc="Single-bit interventions"):
        total_steps = max(28, horizon + 18)
        checkpoint_step = 12 + (rep % 8)
        env = make_environment(total_steps, seed + 10_000 + rep * 101)
        base_seed = seed + 20_000 + rep * 103

        # Build exact receiver checkpoint under no-message environment.
        before = run_signal(
            initial_state(base_seed),
            env[:checkpoint_step],
            max_radius,
            params,
        ).state

        pulse_state = clone_state(before)
        no_state = clone_state(before)
        step_deltas: List[float] = []

        for h in range(horizon):
            base_val = float(env[checkpoint_step + h])
            pval = base_val + (gain if h == 0 else 0.0)

            pulse_state, pn = advance_one_step(
                pulse_state, pval, max_radius, params
            )
            no_state, nn = advance_one_step(
                no_state, base_val, max_radius, params
            )
            step_deltas.append(float(pn - nn))

        diff = normalized_state_difference(
            pulse_state.occupied, no_state.occupied
        )
        sym = len(pulse_state.occupied.symmetric_difference(no_state.occupied))
        differences.append(diff)
        symmetric_cells.append(sym)
        changed.append(int(sym > 0))
        impulse_matrix.append(step_deltas)

    impulse = np.mean(np.asarray(impulse_matrix, dtype=float), axis=0)
    fig = image_dir / "ch16-02-single-bit-impulse-response.png"
    save_intervention_figure(impulse, fig)

    result = {
        "definition": (
            "same receiver checkpoint + same RNG state + same external forcing; "
            "only one received bit differs at the intervention step"
        ),
        "replicates": nrep,
        "message_gain": gain,
        "horizon": horizon,
        "normalized_final_difference": summarize(differences),
        "symmetric_difference_cells": summarize(symmetric_cells),
        "fraction_with_any_morphology_change": float(np.mean(changed)),
        "mean_attachment_impulse_response": [float(x) for x in impulse],
        "figure": str(fig),
    }
    reporter.json("stage-02-single-bit-intervention.json", result)
    reporter.stage(
        "stage-02-single-bit-intervention.md",
        "Stage 2 — Does One Received Bit Actually Matter?",
        f"""
Every replicate forks an exact receiver checkpoint.

```text
same receiver state
same RNG state
same external environment
same future horizon

ONLY DIFFERENCE:
one branch receives one bit
```

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`

If this stage does not produce repeatable receiver differences, the channel is
decorative and no stronger signalling claim is allowed.
""",
    )
    return result



def common_safe_receiver_horizon(
    base_env: np.ndarray,
    streams: Dict[str, np.ndarray],
    gain: float,
    seed: int,
    radius: int,
    params: CrystalParams,
    max_capacity_fraction: float,
    minimum_steps: int,
) -> dict:
    """
    Advance every Stage-3 receiver condition in lockstep and find the longest
    common prefix for which ALL conditions remain below the saturation guard.

    This is preferable to dropping only a saturated condition or changing one
    condition's horizon: every control in a replicate is evaluated over exactly
    the same number of updates.

    Returns:
        safe_steps
        first_unsafe_step (None if full horizon is safe)
        capacity_fraction_at_safe_horizon per condition
    """
    states = {name: initial_state(seed) for name in streams}
    safe_steps = 0
    first_unsafe_step = None
    safe_fractions = {name: capacity_fraction(st, radius) for name, st in states.items()}

    for t in range(len(base_env)):
        trial_states = {}
        trial_fractions = {}

        for name, stream in streams.items():
            forcing = float(base_env[t]) + gain * float(stream[t])
            next_state, _ = advance_one_step(
                states[name],
                forcing,
                radius,
                params,
            )
            trial_states[name] = next_state
            trial_fractions[name] = capacity_fraction(next_state, radius)

        if any(frac >= max_capacity_fraction for frac in trial_fractions.values()):
            first_unsafe_step = t + 1
            break

        states = trial_states
        safe_fractions = trial_fractions
        safe_steps = t + 1

    if safe_steps < minimum_steps:
        raise RuntimeError(
            "No scientifically usable common Stage-3 horizon before saturation: "
            f"safe_steps={safe_steps}, minimum_steps={minimum_steps}, "
            f"guard={max_capacity_fraction:.3f}. Increase radius or reduce "
            "message gain."
        )

    return {
        "safe_steps": safe_steps,
        "first_unsafe_step": first_unsafe_step,
        "capacity_fraction_at_safe_horizon": {
            k: float(v) for k, v in safe_fractions.items()
        },
    }



def stage_3_message_controls(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 3 — HARDENED MESSAGE CONTROLS ===")
    steps = profile["pair_steps"]
    reps = profile["pair_replicates"]
    gain = profile["message_gain"]
    radius = profile["crystal_radius"]
    max_lag = profile["impulse_horizon"]
    saturation_guard = profile["max_capacity_fraction"]
    rule = PulseRule(
        window=profile["pulse_window"],
        sigma=profile["pulse_sigma"],
        min_attachments=profile["min_pulse_attachments"],
    )

    rows: Dict[str, List[dict]] = {
        "real": [],
        "shuffled": [],
        "unrelated_replay_count_matched": [],
        "ipi_permutation_surrogate": [],
        "rate_matched_random": [],
        "no_channel": [],
    }
    structure_rows: List[dict] = []

    for rep in tqdm(range(reps), desc="Message controls"):
        _, sender, real = generate_sender(
            steps, radius, params, rule,
            seed + 30_000 + rep * 401,
            seed + 40_000 + rep * 409,
        )
        _, other_sender, unrelated_raw = generate_sender(
            steps, radius, params, rule,
            seed + 50_000 + rep * 419,
            seed + 60_000 + rep * 421,
        )

        unrelated_matched = count_match_unrelated_stream(
            real,
            unrelated_raw,
            seed + 85_000 + rep,
        )
        ipi_surrogate = ipi_permutation_surrogate(
            real,
            seed + 86_000 + rep,
        )

        receiver_env = make_environment(steps, seed + 70_000 + rep * 431)
        receiver_seed = seed + 80_000 + rep * 433

        streams = {
            "real": real,
            "shuffled": shuffled_stream(real, seed + 90_000 + rep),
            "unrelated_replay_count_matched": unrelated_matched,
            "ipi_permutation_surrogate": ipi_surrogate,
            "rate_matched_random": rate_matched_random_stream(
                real, seed + 100_000 + rep
            ),
            "no_channel": np.zeros(steps, dtype=np.int8),
        }

        structure_rows.append({
            "replicate": rep,
            "real": pulse_structure(real),
            "unrelated_raw": pulse_structure(unrelated_raw),
            "unrelated_count_matched": pulse_structure(unrelated_matched),
            "ipi_permutation_surrogate": pulse_structure(ipi_surrogate),
        })

        # Saturation is handled by selecting one COMMON safe horizon for every
        # condition in this replicate. We never let one control run for fewer
        # steps than another and we never silently discard only the saturated
        # condition.
        horizon_info = common_safe_receiver_horizon(
            receiver_env,
            streams,
            gain,
            receiver_seed,
            radius,
            params,
            saturation_guard,
            minimum_steps=max(rule.window + 6, max_lag + 6),
        )
        safe_steps = int(horizon_info["safe_steps"])

        # Record the chosen horizon in the structure diagnostics.
        structure_rows[-1]["common_safe_horizon"] = horizon_info

        env_eval = receiver_env[:safe_steps]
        streams_eval = {
            name: np.asarray(stream[:safe_steps], dtype=np.int8)
            for name, stream in streams.items()
        }

        baseline = run_receiver_condition(
            env_eval,
            streams_eval["no_channel"],
            gain,
            receiver_seed,
            radius,
            params,
        )

        for name, stream in streams_eval.items():
            receiver = (
                baseline
                if name == "no_channel"
                else run_receiver_condition(
                    env_eval,
                    stream,
                    gain,
                    receiver_seed,
                    radius,
                    params,
                )
            )

            rows[name].append(
                evaluate_condition(
                    stream,
                    receiver,
                    baseline,
                    max_lag=min(max_lag, max(0, safe_steps - 2)),
                    radius=radius,
                )
            )
            rows[name][-1]["common_safe_horizon"] = safe_steps
            rows[name][-1]["full_requested_horizon"] = steps

    summary = {}
    for name, vals in rows.items():
        summary[name] = {
            "peak_lagged_corr": summarize(v["peak_lagged_corr"] for v in vals),
            "post_message_growth": summarize(v["post_message_growth"] for v in vals),
            "final_difference_vs_no_channel": summarize(
                v["final_difference_vs_no_channel"] for v in vals
            ),
            "capacity_fraction": summarize(v["capacity_fraction"] for v in vals),
            "pulse_count": summarize(v["pulse_count"] for v in vals),
            "peak_lag": summarize(v["peak_lag"] for v in vals),
        }

    real_peak = [v["peak_lagged_corr"] for v in rows["real"]]
    comparison = {}
    control_names = (
        "shuffled",
        "unrelated_replay_count_matched",
        "ipi_permutation_surrogate",
        "rate_matched_random",
    )
    for ctrl in control_names:
        ctrl_peak = [v["peak_lagged_corr"] for v in rows[ctrl]]
        comparison[ctrl] = {
            "real_minus_control_mean": float(np.mean(real_peak) - np.mean(ctrl_peak)),
            "pairwise_superiority_probability": pairwise_superiority(
                real_peak, ctrl_peak
            ),
        }

    safe_horizons = [
        int(row["common_safe_horizon"]["safe_steps"])
        for row in structure_rows
    ]

    result = {
        "replicates": reps,
        "message_gain": gain,
        "saturation_guard": saturation_guard,
        "hard_radius_capacity": hex_disk_capacity(radius),
        "requested_steps": steps,
        "common_safe_horizon_summary": summarize(safe_horizons),
        "all_replicates_used_equal_horizon_across_conditions": True,
        "control_summary": summary,
        "real_vs_controls": comparison,
        "stream_structure_diagnostics": structure_rows,
        "raw_rows": rows,
    }

    fig = image_dir / "ch16-03-message-controls.png"
    save_control_figure(summary, fig)
    result["figure"] = str(fig)

    reporter.json("stage-03-message-controls.json", result)
    reporter.stage(
        "stage-03-message-controls.md",
        "Stage 3 — Correlation Is Not Communication",
        f"""
The receiver is tested against six streams:

```text
REAL sender events

SHUFFLED
same bits, chronology destroyed

UNRELATED REPLAY — COUNT MATCHED
different sender of the same Digital Crystal class,
forced to exactly the same pulse count as the real stream

IPI-PERMUTATION SURROGATE
same pulse count and exact multiset of inter-pulse intervals,
but interval order is permuted

RATE-MATCHED RANDOM
same number of bits, random times

NO CHANNEL
```

Every replicate first finds the longest **common** receiver horizon for which
all six conditions remain below the predeclared hard-radius saturation guard of
`{saturation_guard:.2f}`. Every condition in that replicate is then evaluated
at exactly that same horizon. Saturation therefore cannot make one control run
for less time than another or collapse all endpoint morphologies onto the same
filled disk.

```json
{json.dumps({k: v for k, v in result.items() if k not in ("raw_rows", "stream_structure_diagnostics")}, indent=2)}
```

Figure: `{fig}`

The real stream must beat not only naive timing controls but also a count-matched
unrelated sender and an exact-IPI-distribution surrogate before sender-specific
signalling is supported.
""",
    )
    return result


def stage_4_impulse_latency(
    reporter: Reporter,
    stage2: dict,
) -> dict:
    print("\n=== STAGE 4 — LATENCY AND DECAY ===")
    impulse = np.asarray(stage2["mean_attachment_impulse_response"], dtype=float)
    abs_impulse = np.abs(impulse)
    if len(abs_impulse) and float(np.max(abs_impulse)) > 0:
        peak_lag = int(np.argmax(abs_impulse))
        peak_effect = float(impulse[peak_lag])
        total_abs = float(np.sum(abs_impulse))
        cumulative = np.cumsum(abs_impulse)
        decay_lag = int(np.searchsorted(cumulative, 0.90 * total_abs)) if total_abs > 0 else 0
    else:
        peak_lag = 0
        peak_effect = 0.0
        decay_lag = 0

    result = {
        "impulse_response": [float(x) for x in impulse],
        "peak_effect_lag_steps": peak_lag,
        "peak_effect": peak_effect,
        "lag_containing_90pct_absolute_effect_mass": decay_lag,
        "interpretation": (
            "Finite-horizon impulse-response description only. The peak lag is not claimed as a stable characteristic latency, and this is not a channel-capacity result."
        ),
    }
    reporter.json("stage-04-latency-decay.json", result)
    reporter.stage(
        "stage-04-latency-decay.md",
        "Stage 4 — How Fast Does One Bit Matter?",
        f"""
The exact checkpoint intervention from Stage 2 gives an impulse response.

```json
{json.dumps(result, indent=2)}
```

This describes the finite-horizon response of growth to a one-bit causal
perturbation. The largest observed lag is not yet treated as a stable latency
law, and this does not establish information-theoretic capacity.
""",
    )
    return result


def run_chain_once(
    length: int,
    steps: int,
    gain: float,
    radius: int,
    params: CrystalParams,
    pulse_rule: PulseRule,
    seed: int,
    shuffled_edges: bool,
    max_capacity_fraction: float,
) -> dict:
    crystals = [initial_state(seed + 1000 + i * 97) for i in range(length)]
    envs = [
        make_environment(steps, seed + 2000 + i * 101)
        for i in range(length)
    ]
    attachment_hist: List[List[int]] = [[] for _ in range(length)]
    pulses = np.zeros((steps, length), dtype=np.int8)
    incoming = np.zeros(length, dtype=np.int8)

    source_of = np.arange(length, dtype=int) - 1
    if shuffled_edges and length > 2:
        rng = np.random.default_rng(seed + 9999)
        donors = np.arange(length - 1, dtype=int)
        rng.shuffle(donors)
        source_of[1:] = donors

    safe_steps = 0
    first_unsafe_step = None
    safe_fractions = [capacity_fraction(c, radius) for c in crystals]

    for t in range(steps):
        next_crystals = []
        next_histories = []
        emitted = np.zeros(length, dtype=np.int8)

        for i in range(length):
            forcing = float(envs[i][t]) + gain * float(incoming[i])
            next_state, added = advance_one_step(
                crystals[i],
                forcing,
                radius,
                params,
            )
            next_crystals.append(next_state)

            hist = list(attachment_hist[i])
            hist.append(added)
            next_histories.append(hist)

            arr = np.asarray(hist, dtype=float)
            if len(arr) > pulse_rule.window:
                p = pulses_from_attachments(arr, pulse_rule)
                emitted[i] = int(p[-1])

        fractions = [capacity_fraction(c, radius) for c in next_crystals]
        if max(fractions) >= max_capacity_fraction:
            first_unsafe_step = t + 1
            break

        next_incoming = np.zeros(length, dtype=np.int8)
        for i in range(1, length):
            donor = int(source_of[i])
            if donor >= 0:
                next_incoming[i] = emitted[donor]

        crystals = next_crystals
        attachment_hist = next_histories
        pulses[t, :] = emitted
        incoming = next_incoming
        safe_steps = t + 1
        safe_fractions = fractions

    minimum_steps = max(pulse_rule.window + 6, 16)
    if safe_steps < minimum_steps:
        raise RuntimeError(
            "No scientifically usable Stage-5 chain horizon before saturation: "
            f"safe_steps={safe_steps}, minimum_steps={minimum_steps}, "
            f"guard={max_capacity_fraction:.3f}."
        )

    pulses = pulses[:safe_steps, :]
    source = pulses[:, 0].astype(float)

    corrs = []
    for i in range(length):
        if i == 0:
            corrs.append(1.0)
        else:
            best = max(
                lagged_corr(
                    source,
                    pulses[:, i],
                    max_lag=min(12, max(1, safe_steps // 4)),
                )
            )
            corrs.append(float(best))

    return {
        "source_to_node_pulse_corr": corrs,
        "pulse_rate_by_node": [
            float(np.mean(pulses[:, i])) for i in range(length)
        ],
        "final_population_by_node": [len(c.occupied) for c in crystals],
        "capacity_fraction_by_node": [float(x) for x in safe_fractions],
        "safe_steps": safe_steps,
        "first_unsafe_step": first_unsafe_step,
    }


def stage_5_chain(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 5 — SIX-CRYSTAL CHAIN ===")
    length = profile["chain_length"]
    reps = profile["chain_replicates"]
    rule = PulseRule(
        window=profile["pulse_window"],
        sigma=profile["pulse_sigma"],
        min_attachments=profile["min_pulse_attachments"],
    )

    real_rows = []
    shuf_rows = []
    for rep in tqdm(range(reps), desc="Chain replicates"):
        real_rows.append(
            run_chain_once(
                length, profile["chain_steps"], profile["message_gain"],
                profile["crystal_radius"], params, rule,
                seed + 110_000 + rep * 503, False,
                profile["max_capacity_fraction"],
            )
        )
        shuf_rows.append(
            run_chain_once(
                length, profile["chain_steps"], profile["message_gain"],
                profile["crystal_radius"], params, rule,
                seed + 110_000 + rep * 503, True,
                profile["max_capacity_fraction"],
            )
        )

    def mean_vector(rows: List[dict], key: str) -> List[float]:
        return [
            float(x)
            for x in np.mean(
                np.asarray([row[key] for row in rows], dtype=float),
                axis=0,
            )
        ]

    chain_safe_horizons_real = [r["safe_steps"] for r in real_rows]
    chain_safe_horizons_shuffled = [r["safe_steps"] for r in shuf_rows]

    result = {
        "length": length,
        "replicates": reps,
        "requested_steps": profile["chain_steps"],
        "real_safe_horizon_summary": summarize(chain_safe_horizons_real),
        "shuffled_safe_horizon_summary": summarize(chain_safe_horizons_shuffled),
        "real": {
            "mean_source_to_node_pulse_corr": mean_vector(
                real_rows, "source_to_node_pulse_corr"
            ),
            "mean_pulse_rate_by_node": mean_vector(
                real_rows, "pulse_rate_by_node"
            ),
        },
        "shuffled_edges": {
            "mean_source_to_node_pulse_corr": mean_vector(
                shuf_rows, "source_to_node_pulse_corr"
            ),
            "mean_pulse_rate_by_node": mean_vector(
                shuf_rows, "pulse_rate_by_node"
            ),
        },
        "topology_contrast": {
            "mean_absolute_real_minus_shuffled_by_distance": float(
                np.mean(
                    np.abs(
                        np.asarray(mean_vector(real_rows, "source_to_node_pulse_corr")[1:])
                        - np.asarray(mean_vector(shuf_rows, "source_to_node_pulse_corr")[1:])
                    )
                )
            )
        },
        "interpretation": (
            "Exploratory propagation test. High source-to-node correlations are "
            "not treated as topology-specific propagation unless they separate "
            "from the shuffled-edge control. No coordination claim is made."
        ),
    }

    fig = image_dir / "ch16-05-chain-propagation.png"
    save_chain_figure(result, fig)
    result["figure"] = str(fig)

    reporter.json("stage-05-chain.json", result)
    reporter.stage(
        "stage-05-chain.md",
        "Stage 5 — Can the Pulse Travel?",
        f"""
Six independently evolving Digital Crystals are connected in a one-way nearest-
neighbour chain. A receiver's own growth can subsequently produce another pulse.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`

This stage asks only whether measurable causal influence propagates with
distance. It does not test cooperation or a shared task.
""",
    )
    return result


def board_neighbors(width: int, height: int) -> List[List[int]]:
    out: List[List[int]] = []
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            neigh: List[int] = []
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < width and 0 <= yy < height:
                    neigh.append(yy * width + xx)
            out.append(neigh)
    return out


def run_board_pair_common_horizon(
    width: int,
    height: int,
    steps: int,
    gain: float,
    radius: int,
    params: CrystalParams,
    pulse_rule: PulseRule,
    seed: int,
    max_capacity_fraction: float,
) -> dict:
    """
    Run REAL and SHUFFLED board topologies in lockstep from identical crystal
    seeds and environmental inputs.

    The replicate stops at the longest COMMON horizon for which every crystal
    in both board conditions remains below the saturation guard.

    This avoids two invalid alternatives:
      1. letting one topology run longer than the other;
      2. allowing endpoint morphology to collapse onto the hard-radius disk.
    """
    n = width * height

    def init_condition():
        return {
            "crystals": [
                initial_state(seed + 1000 + i * 113)
                for i in range(n)
            ],
            "histories": [[] for _ in range(n)],
            "pulses": np.zeros((steps, n), dtype=np.int8),
            "incoming": np.zeros(n, dtype=np.int8),
        }

    real = init_condition()
    shuffled = init_condition()

    envs = [
        make_environment(steps, seed + 3000 + i * 127)
        for i in range(n)
    ]

    real_neigh = board_neighbors(width, height)

    rng = np.random.default_rng(seed + 8888)
    perm = rng.permutation(n)
    shuffled_neigh = [
        [int(perm[j]) for j in lst]
        for lst in real_neigh
    ]

    safe_steps = 0
    first_unsafe_step = None
    safe_capacity = {
        "real": [capacity_fraction(c, radius) for c in real["crystals"]],
        "shuffled": [capacity_fraction(c, radius) for c in shuffled["crystals"]],
    }

    for t in range(steps):
        trial = {}

        for label, condition, neigh in (
            ("real", real, real_neigh),
            ("shuffled", shuffled, shuffled_neigh),
        ):
            next_crystals = []
            next_histories = []
            emitted = np.zeros(n, dtype=np.int8)

            for i in range(n):
                forcing = (
                    float(envs[i][t])
                    + gain * float(condition["incoming"][i])
                )

                next_state, added = advance_one_step(
                    condition["crystals"][i],
                    forcing,
                    radius,
                    params,
                )
                next_crystals.append(next_state)

                hist = list(condition["histories"][i])
                hist.append(added)
                next_histories.append(hist)

                arr = np.asarray(hist, dtype=float)
                if len(arr) > pulse_rule.window:
                    p = pulses_from_attachments(arr, pulse_rule)
                    emitted[i] = int(p[-1])

            next_incoming = np.zeros(n, dtype=np.int8)
            for i in range(n):
                next_incoming[i] = int(
                    any(emitted[j] for j in neigh[i])
                )

            fractions = np.asarray(
                [capacity_fraction(c, radius) for c in next_crystals],
                dtype=float,
            )

            trial[label] = {
                "crystals": next_crystals,
                "histories": next_histories,
                "emitted": emitted,
                "incoming": next_incoming,
                "fractions": fractions,
            }

        max_real = float(np.max(trial["real"]["fractions"]))
        max_shuf = float(np.max(trial["shuffled"]["fractions"]))

        if max(max_real, max_shuf) >= max_capacity_fraction:
            first_unsafe_step = t + 1
            break

        for label, condition in (("real", real), ("shuffled", shuffled)):
            condition["crystals"] = trial[label]["crystals"]
            condition["histories"] = trial[label]["histories"]
            condition["pulses"][t, :] = trial[label]["emitted"]
            condition["incoming"] = trial[label]["incoming"]

        safe_capacity = {
            "real": [float(x) for x in trial["real"]["fractions"]],
            "shuffled": [float(x) for x in trial["shuffled"]["fractions"]],
        }
        safe_steps = t + 1

    minimum_steps = max(pulse_rule.window + 6, 16)
    if safe_steps < minimum_steps:
        raise RuntimeError(
            "No scientifically usable common Stage-6 board horizon before "
            f"saturation: safe_steps={safe_steps}, minimum_steps={minimum_steps}, "
            f"guard={max_capacity_fraction:.3f}. Increase radius or reduce "
            "message gain."
        )

    def summarize_condition(condition, base_neigh):
        pulses = condition["pulses"][:safe_steps, :]
        pulse_rate = np.mean(pulses, axis=0)
        activity = np.asarray(
            [
                float(np.mean(h[:safe_steps])) if h[:safe_steps] else 0.0
                for h in condition["histories"]
            ],
            dtype=float,
        )

        pair_corrs = []
        seen = set()
        for i, lst in enumerate(base_neigh):
            for j in lst:
                key = tuple(sorted((i, j)))
                if key in seen:
                    continue
                seen.add(key)
                pair_corrs.append(
                    safe_corr(pulses[:, i], pulses[:, j])
                )

        return {
            "pulse_rate": pulse_rate,
            "activity": activity,
            "mean_real_grid_neighbor_pulse_corr": (
                float(np.mean(pair_corrs)) if pair_corrs else 0.0
            ),
            "final_populations": np.asarray(
                [len(c.occupied) for c in condition["crystals"]],
                dtype=float,
            ),
        }

    return {
        "real": summarize_condition(real, real_neigh),
        "shuffled": summarize_condition(shuffled, real_neigh),
        "common_safe_horizon": safe_steps,
        "requested_steps": steps,
        "first_unsafe_step": first_unsafe_step,
        "capacity_fraction_at_safe_horizon": safe_capacity,
        "max_capacity_fraction_at_safe_horizon": {
            "real": float(max(safe_capacity["real"])),
            "shuffled": float(max(safe_capacity["shuffled"])),
        },
    }


def stage_6_board(
    reporter: Reporter,
    image_dir: Path,
    profile: dict,
    params: CrystalParams,
    seed: int,
) -> dict:
    print("\n=== STAGE 6 — CRYSTAL BOARD ===")
    width = profile["board_width"]
    height = profile["board_height"]
    reps = profile["board_replicates"]
    rule = PulseRule(
        window=profile["pulse_window"],
        sigma=profile["pulse_sigma"],
        min_attachments=profile["min_pulse_attachments"],
    )

    real_rows = []
    shuf_rows = []
    horizon_rows = []

    for rep in tqdm(range(reps), desc="Board replicates"):
        paired = run_board_pair_common_horizon(
            width,
            height,
            profile["board_steps"],
            profile["message_gain"],
            profile["crystal_radius"],
            params,
            rule,
            seed + 140_000 + rep * 607,
            profile["max_capacity_fraction"],
        )

        real_rows.append(paired["real"])
        shuf_rows.append(paired["shuffled"])
        horizon_rows.append({
            "replicate": rep,
            "common_safe_horizon": paired["common_safe_horizon"],
            "requested_steps": paired["requested_steps"],
            "first_unsafe_step": paired["first_unsafe_step"],
            "max_capacity_fraction_at_safe_horizon": paired[
                "max_capacity_fraction_at_safe_horizon"
            ],
        })

    real_corr = [r["mean_real_grid_neighbor_pulse_corr"] for r in real_rows]
    shuf_corr = [r["mean_real_grid_neighbor_pulse_corr"] for r in shuf_rows]

    pulse_rate = np.mean(
        np.asarray([r["pulse_rate"] for r in real_rows], dtype=float),
        axis=0,
    )
    activity = np.mean(
        np.asarray([r["activity"] for r in real_rows], dtype=float),
        axis=0,
    )

    fig = image_dir / "ch16-06-crystal-board.png"
    save_board_figure(pulse_rate, activity, width, height, fig)

    common_horizons = [r["common_safe_horizon"] for r in horizon_rows]
    max_capacity_observed = max(
        max(
            r["max_capacity_fraction_at_safe_horizon"]["real"],
            r["max_capacity_fraction_at_safe_horizon"]["shuffled"],
        )
        for r in horizon_rows
    )

    result = {
        "board_shape": [height, width],
        "replicates": reps,
        "requested_steps": profile["board_steps"],
        "common_safe_horizon_summary": summarize(common_horizons),
        "all_replicates_used_equal_horizon_across_topologies": True,
        "horizon_diagnostics": horizon_rows,
        "real_topology_neighbor_pulse_corr": summarize(real_corr),
        "shuffled_topology_neighbor_pulse_corr": summarize(shuf_corr),
        "real_minus_shuffled_mean": float(np.mean(real_corr) - np.mean(shuf_corr)),
        "pairwise_superiority_probability": pairwise_superiority(real_corr, shuf_corr),
        "mean_pulse_rate_by_crystal": [float(x) for x in pulse_rate],
        "mean_growth_activity_by_crystal": [float(x) for x in activity],
        "max_capacity_fraction_observed_at_safe_horizon": float(
            max_capacity_observed
        ),
        "saturation_guard": profile["max_capacity_fraction"],
        "figure": str(fig),
        "explicit_nonclaim": (
            "The board has no shared target and does not test coordination."
        ),
    }

    reporter.json("stage-06-crystal-board.json", result)
    reporter.stage(
        "stage-06-crystal-board.md",
        "Stage 6 — The Crystal Board",
        f"""
A {width}×{height} board of separate Digital Crystal processes is connected by
local one-bit neighbour events.

Real and shuffled topologies are advanced in lockstep from identical crystal
seeds and environmental inputs. Each replicate stops at the longest **common**
horizon for which every crystal in both topologies remains below the saturation
guard of `{profile["max_capacity_fraction"]:.2f}`.

This prevents topology comparisons from being contaminated by one condition
running longer or by endpoint morphologies collapsing onto the same filled disk.

```json
{json.dumps(result, indent=2)}
```

Figure: `{fig}`

The board exists only to observe local propagation and topology effects.
No coordination claim is made.
""",
    )
    return result


def stage_7_verdict(
    reporter: Reporter,
    stage2: dict,
    stage3: dict,
    stage4: dict,
    stage5: dict,
    stage6: dict,
) -> dict:
    print("\n=== STAGE 7 — VERDICT ===")

    # Predeclared descriptive thresholds. These are engineering thresholds, not
    # p-values. They ensure we do not promote a tiny visual difference.
    causal_fraction = stage2["fraction_with_any_morphology_change"]
    causal_mean_diff = stage2["normalized_final_difference"]["mean"]

    causal_transmission = (
        causal_fraction >= 0.70
        and causal_mean_diff > 0.0
    )

    comparisons = stage3["real_vs_controls"]
    sender_specific = causal_transmission and all(
        comparisons[name]["real_minus_control_mean"] >= 0.03
        and comparisons[name]["pairwise_superiority_probability"] >= 0.70
        for name in (
            "shuffled",
            "unrelated_replay_count_matched",
            "ipi_permutation_surrogate",
            "rate_matched_random",
        )
    )

    if sender_specific:
        verdict = "SENDER_SPECIFIC_SIGNALLING_SUPPORTED"
        bounded_claim = (
            "Within this protocol, an endogenous one-bit event emitted by one "
            "Digital Crystal causally changed another Digital Crystal, and the "
            "real sender-event timing produced a stronger receiver relationship "
            "than shuffled, count-matched unrelated-replay, exact-IPI-surrogate, "
            "and rate-matched-random controls."
        )
    elif causal_transmission:
        verdict = "CAUSAL_TRANSMISSION_SUPPORTED"
        bounded_claim = (
            "Within this protocol, inserting one received bit into an otherwise "
            "identical Digital Crystal continuation reliably changed receiver "
            "growth, but the real sender-generated event stream did not clear "
            "all controls required for a sender-specific signalling claim."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        bounded_claim = (
            "This one-bit mechanism did not establish reliable causal "
            "transmission into Digital Crystal growth under the predeclared "
            "checkpoint intervention criterion."
        )

    result = {
        "verdict": verdict,
        "bounded_claim": bounded_claim,
        "checks": {
            "single_bit_changes_receiver_reliably": causal_transmission,
            "real_stream_beats_all_message_controls": sender_specific,
        },
        "headline_metrics": {
            "single_bit_fraction_with_any_morphology_change": causal_fraction,
            "single_bit_mean_normalized_final_difference": causal_mean_diff,
            "real_vs_shuffled": comparisons["shuffled"],
            "real_vs_unrelated_replay_count_matched": comparisons[
                "unrelated_replay_count_matched"
            ],
            "real_vs_ipi_permutation_surrogate": comparisons[
                "ipi_permutation_surrogate"
            ],
            "real_vs_rate_matched_random": comparisons["rate_matched_random"],
            "impulse_peak_lag": stage4["peak_effect_lag_steps"],
            "chain_real_source_to_node_corr": stage5["real"][
                "mean_source_to_node_pulse_corr"
            ],
            "board_real_minus_shuffled_neighbor_corr": stage6[
                "real_minus_shuffled_mean"
            ],
        },
        "kill_conditions": {
            "decorative_channel": (
                "Triggered if exact pulse/no-pulse checkpoint interventions do "
                "not reliably change the receiver."
            ),
            "not_sender_specific": (
                "Triggered if real sender timing does not beat shuffled, "
                "count-matched unrelated replay, exact-IPI surrogate, and "
                "rate-matched-random controls."
            ),
        },
        "explicit_nonclaims": [
            "language",
            "semantics",
            "meaning",
            "cooperation",
            "coordination",
            "planning",
            "learning",
            "intelligence",
            "agency",
            "individuality",
            "selfhood",
            "life",
            "channel capacity",
        ],
    }

    reporter.json("ch16-summary.json", result)
    reporter.stage(
        "stage-07-verdict.md",
        "Stage 7 — Experimental Verdict",
        f"""
**Verdict: `{verdict}`**

> {bounded_claim}

```json
{json.dumps(result, indent=2)}
```
""",
    )
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chapter 16 — one-bit Digital Crystal signalling experiment"
    )
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILES),
        default="quick",
    )
    parser.add_argument(
        "--reports",
        default="research/digital-life/ch16-reports",
    )
    parser.add_argument(
        "--images",
        default="static/images/books/digital-life",
    )
    parser.add_argument("--seed", type=int, default=20260812)
    parser.add_argument(
        "--message-gain",
        type=float,
        default=None,
        help="Override profile message gain.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Accepted for workflow symmetry; this script recomputes by default.",
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])
    if args.message_gain is not None:
        profile["message_gain"] = float(args.message_gain)

    report_dir = Path(args.reports)
    image_dir = Path(args.images)
    report_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    reporter = Reporter(report_dir)
    params = CrystalParams()

    metadata = {
        "model_version": MODEL_VERSION,
        "signalling_version": SIGNALLING_VERSION,
        "schema_version": SCHEMA_VERSION,
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "started_at_unix": time.time(),
        "scientific_boundary": (
            "Primitive causal transmission only. No semantics, coordination, "
            "agency, individuality, or life claim."
        ),
        "message_definition": (
            "One bit emitted by sender growth when attachment activity exceeds "
            "a threshold derived from the sender's own recent history."
        ),
        "receiver_coupling": (
            "Received bit directly perturbs the Digital Crystal environmental "
            "forcing used by the frozen attachment rule."
        ),
        "saturation_policy": (
            "Stages 1, 3, 5, and 6 stop before hard-radius saturation. "
            "Stages comparing controls use matched/common horizons so endpoint "
            "morphology remains informative."
        ),
        "sender_specificity_controls": [
            "shuffled chronology",
            "count-matched unrelated sender replay",
            "exact inter-pulse-interval multiset permutation",
            "rate-matched random timing",
        ],
    }

    print("=" * 78)
    print("CHAPTER 16 — BEFORE THERE ARE MESSAGES, THERE ARE PULSES")
    print(f"profile={args.profile}  version={SIGNALLING_VERSION}")
    print("=" * 78)

    s0 = stage_0_reproducibility(
        reporter, params, profile["crystal_radius"], args.seed
    )
    s1 = stage_1_endogenous_sender(
        reporter, image_dir, profile, params, args.seed
    )
    s2 = stage_2_single_bit_intervention(
        reporter, image_dir, profile, params, args.seed
    )
    s3 = stage_3_message_controls(
        reporter, image_dir, profile, params, args.seed
    )
    s4 = stage_4_impulse_latency(reporter, s2)
    s5 = stage_5_chain(
        reporter, image_dir, profile, params, args.seed
    )
    s6 = stage_6_board(
        reporter, image_dir, profile, params, args.seed
    )
    s7 = stage_7_verdict(reporter, s2, s3, s4, s5, s6)

    metadata["finished_at_unix"] = time.time()
    metadata["final_verdict"] = s7["verdict"]
    metadata["stage0_reproducibility_passed"] = s0[
        "repeat_from_identical_state_exact"
    ]
    metadata["stage1_message_count"] = s1["message_count"]

    reporter.json("ch16-metadata.json", metadata)
    full = reporter.full(metadata)

    print("\n" + "=" * 78)
    print(f"FINAL VERDICT: {s7['verdict']}")
    print(s7["bounded_claim"])
    print(f"Report: {full}")
    print("=" * 78)


if __name__ == "__main__":
    main()
