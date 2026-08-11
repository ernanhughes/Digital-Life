#!/usr/bin/env python3
"""
Digital Life Chapter 15 — The Crystal Gets a Past
=================================================

Purpose
-------
Continue directly from the frozen Chapter 14 Digital Crystal v1 model.

Chapter 14 established:
    - source-family information can survive in final morphology;
    - temporal ordering does NOT survive reliably in final morphology.

Chapter 15 asks a narrower engineering/scientific question:

    What is the minimum persistent information required for a Digital Crystal
    to have a recoverable, reproducible past?

This script does NOT add learning, adaptation, agency, goals, selfhood, or
decision-making.

It adds only:
    1. exact state checkpointing,
    2. explicit event history,
    3. exact restoration,
    4. replay,
    5. deliberate omission tests,
    6. counterfactual branching from a shared saved past.

Core experiments
----------------
Stage 1 — Continuous reference run
    Produce a reference trajectory with frozen Digital Crystal v1.

Stage 2 — Exact checkpoint/restore
    Save at a midpoint, restore, continue, and demand exact final identity.

Stage 3 — What belongs to state?
    Restore deliberately incomplete checkpoints:
        - no RNG state
        - wrong signal cursor
        - morphology only
    Measure divergence from the exact reference.

Stage 4 — History replay
    Test two forms of replay:
        A. procedural replay from initial seed + signal,
        B. event-log replay using recorded additions.
    Demand exact trajectory/state hashes where appropriate.

Stage 5 — State vs history
    Demonstrate:
        - state can continue without reconstructing how it got there;
        - history can reconstruct how it got there;
        - neither concept is identical to the other.

Stage 6 — Counterfactual branching
    Restore the same checkpoint twice.
    Feed two different future signals.
    Measure divergence from the shared past.

Stage 7 — Coalesced verdict
    Decide whether "the crystal has a recoverable past" is supported.

Caching
-------
SQLite stores runs, checkpoints, history events, analyses, and reports.
Completed expensive simulations are reused on rerun.

Recommended usage
-----------------
First:
    python scripts/books/digital-life/ch15_digital_crystal_history.py --profile quick

Then:
    python scripts/books/digital-life/ch15_digital_crystal_history.py --profile full

Dependencies
------------
    pip install numpy matplotlib tqdm
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import pickle
import random
import sqlite3
import time
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from tqdm import tqdm


# =============================================================================
# 0. CONSTANTS / FROZEN CHAPTER 14 MODEL
# =============================================================================

MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "digital-crystal-history-v1"
SCHEMA_VERSION = 1

Cell = Tuple[int, int]

HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)

PROFILES = {
    "quick": {
        "steps": 48,
        "max_radius": 30,
        "checkpoint_step": 24,
        "replicates": 4,
    },
    "standard": {
        "steps": 72,
        "max_radius": 44,
        "checkpoint_step": 36,
        "replicates": 12,
    },
    "full": {
        "steps": 96,
        "max_radius": 56,
        "checkpoint_step": 48,
        "replicates": 30,
    },
}


@dataclass(frozen=True)
class ModelParams:
    # EXACT frozen defaults from Chapter 14.
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


@dataclass(frozen=True)
class ExperimentSpec:
    run_name: str
    signal_seed: int
    crystal_seed: int
    steps: int
    max_radius: int
    checkpoint_step: int
    signal_kind: str = "composite"
    model_params: ModelParams = ModelParams()

    def key_dict(self) -> dict:
        d = asdict(self)
        d["model_version"] = MODEL_VERSION
        d["experiment_version"] = EXPERIMENT_VERSION
        return d

    def run_key(self) -> str:
        raw = json.dumps(self.key_dict(), sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:24]


# =============================================================================
# 1. HEX GRID + LOCAL GROWTH
# =============================================================================

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
    vec_x = 0.0
    vec_y = 0.0
    count = 0
    for nb in neighbors(cell):
        if nb in occupied:
            nx, ny = axial_to_xy(nb)
            vec_x += x - nx
            vec_y += y - ny
            count += 1
    if count == 0 or (abs(vec_x) + abs(vec_y) < 1e-12):
        return 0.0
    return math.atan2(vec_y, vec_x)


# =============================================================================
# 2. INPUT SIGNALS
# =============================================================================

def normalize_signal(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    x = x - float(np.mean(x))
    m = float(np.max(np.abs(x))) if len(x) else 0.0
    if m > 0:
        x = x / m
    return np.clip(x, -1.0, 1.0)


def make_signal(kind: str, steps: int, seed: int) -> np.ndarray:
    """
    Composite is intentionally richer than a pure sine so the saved cursor matters.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(steps, dtype=float)

    if kind == "constant":
        return np.zeros(steps, dtype=float)

    if kind == "sine":
        period = rng.uniform(11.0, 17.0)
        phase = rng.uniform(0.0, 2 * np.pi)
        return normalize_signal(np.sin((2 * np.pi * t / period) + phase))

    if kind == "random_walk":
        return normalize_signal(np.cumsum(rng.normal(0.0, 0.2, size=steps)))

    if kind == "composite":
        p1 = rng.uniform(10.0, 16.0)
        p2 = rng.uniform(17.0, 29.0)
        ph1 = rng.uniform(0.0, 2 * np.pi)
        ph2 = rng.uniform(0.0, 2 * np.pi)
        deterministic = (
            0.60 * np.sin((2 * np.pi * t / p1) + ph1)
            + 0.30 * np.sin((2 * np.pi * t / p2) + ph2)
        )
        drift = 0.20 * normalize_signal(np.cumsum(rng.normal(0.0, 0.08, size=steps)))
        impulses = np.zeros(steps, dtype=float)
        for _ in range(max(2, steps // 24)):
            idx = int(rng.integers(2, max(3, steps - 2)))
            impulses[idx] += float(rng.choice([-0.8, 0.8]))
        return normalize_signal(deterministic + drift + impulses)

    raise ValueError(f"Unknown signal kind: {kind}")


def make_branch_future(kind: str, length: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(length, dtype=float)

    if kind == "future_a":
        # Smooth oscillatory future.
        return normalize_signal(
            np.sin(2 * np.pi * t / 13.0) + 0.20 * np.sin(2 * np.pi * t / 5.0)
        )

    if kind == "future_b":
        # Burst/noisy future.
        x = rng.uniform(-0.25, 0.25, size=length)
        for i in range(3, length, 9):
            x[i:i+2] += rng.choice([-1.0, 1.0])
        return normalize_signal(x)

    raise ValueError(kind)


# =============================================================================
# 3. STATE, HISTORY, HASHES
# =============================================================================

@dataclass
class CrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    signal_cursor: int
    population_by_step: List[int]
    attachments_by_step: List[int]


@dataclass
class HistoryEvent:
    step: int
    input_value: float
    added_cells: List[Cell]
    population: int
    state_hash: str


@dataclass
class RunResult:
    state: CrystalState
    history: List[HistoryEvent]
    signal: np.ndarray


def canonical_state_payload(
    occupied: Set[Cell],
    birth_time: Dict[Cell, int],
    step: Optional[int] = None,
    signal_cursor: Optional[int] = None,
) -> bytes:
    cells = sorted((int(q), int(r), int(birth_time[(q, r)])) for q, r in occupied)
    payload = {
        "cells": cells,
        "step": step,
        "signal_cursor": signal_cursor,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def morphology_hash(occupied: Set[Cell], birth_time: Dict[Cell, int]) -> str:
    return hashlib.sha256(
        canonical_state_payload(occupied, birth_time)
    ).hexdigest()[:24]


def process_state_hash(state: CrystalState) -> str:
    h = hashlib.sha256()
    h.update(
        canonical_state_payload(
            state.occupied,
            state.birth_time,
            step=state.step,
            signal_cursor=state.signal_cursor,
        )
    )
    h.update(pickle.dumps(state.rng_state, protocol=pickle.HIGHEST_PROTOCOL))
    return h.hexdigest()[:24]


def symmetric_difference_count(a: Set[Cell], b: Set[Cell]) -> int:
    return len(a.symmetric_difference(b))


def normalized_state_difference(a: Set[Cell], b: Set[Cell]) -> float:
    denom = max(1, len(a.union(b)))
    return len(a.symmetric_difference(b)) / denom


# =============================================================================
# 4. SIMULATION ENGINE
# =============================================================================

def initial_state(seed: int) -> CrystalState:
    rng = random.Random(seed)
    return CrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        step=0,
        rng_state=rng.getstate(),
        signal_cursor=0,
        population_by_step=[1],
        attachments_by_step=[1],
    )


def advance_one_step(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: ModelParams,
) -> Tuple[CrystalState, List[Cell]]:
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

    if frontier:
        for cell in frontier:
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

    new_step = state.step + 1
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = new_step

    return CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=new_step,
        rng_state=rng.getstate(),
        signal_cursor=state.signal_cursor + 1,
        population_by_step=state.population_by_step + [len(occupied)],
        attachments_by_step=state.attachments_by_step + [len(additions)],
    ), additions


def run_from_state(
    state: CrystalState,
    signal: np.ndarray,
    max_radius: int,
    params: ModelParams,
    stop_after: Optional[int] = None,
    record_history: bool = True,
) -> RunResult:
    history: List[HistoryEvent] = []
    current = state

    remaining = len(signal) - current.signal_cursor
    count = remaining if stop_after is None else min(remaining, stop_after)

    for _ in range(count):
        input_value = float(signal[current.signal_cursor])
        next_state, additions = advance_one_step(
            current,
            input_value,
            max_radius=max_radius,
            params=params,
        )

        if record_history:
            history.append(
                HistoryEvent(
                    step=next_state.step,
                    input_value=input_value,
                    added_cells=sorted(additions),
                    population=len(next_state.occupied),
                    state_hash=morphology_hash(
                        next_state.occupied,
                        next_state.birth_time,
                    ),
                )
            )
        current = next_state

    return RunResult(state=current, history=history, signal=np.asarray(signal, dtype=float))


def run_reference(spec: ExperimentSpec) -> RunResult:
    signal = make_signal(spec.signal_kind, spec.steps, spec.signal_seed)
    state = initial_state(spec.crystal_seed)
    return run_from_state(
        state,
        signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
    )


# =============================================================================
# 5. CHECKPOINT SERIALIZATION
# =============================================================================

def serialize_rng_state(rng_state: object) -> bytes:
    return zlib.compress(pickle.dumps(rng_state, protocol=pickle.HIGHEST_PROTOCOL), 6)


def deserialize_rng_state(blob: bytes) -> object:
    return pickle.loads(zlib.decompress(blob))


def serialize_cells(cells: Set[Cell]) -> bytes:
    obj = [[int(q), int(r)] for q, r in sorted(cells)]
    return zlib.compress(json.dumps(obj).encode("utf-8"), 6)


def deserialize_cells(blob: bytes) -> Set[Cell]:
    return {tuple(x) for x in json.loads(zlib.decompress(blob).decode("utf-8"))}


def serialize_birth(birth: Dict[Cell, int]) -> bytes:
    obj = {f"{q},{r}": int(t) for (q, r), t in birth.items()}
    return zlib.compress(json.dumps(obj).encode("utf-8"), 6)


def deserialize_birth(blob: bytes) -> Dict[Cell, int]:
    raw = json.loads(zlib.decompress(blob).decode("utf-8"))
    return {
        tuple(map(int, k.split(","))): int(v)
        for k, v in raw.items()
    }


# =============================================================================
# 6. SQLITE CACHE
# =============================================================================

class Cache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS runs (
            run_key TEXT PRIMARY KEY,
            spec_json TEXT NOT NULL,
            signal_blob BLOB NOT NULL,
            final_occupied_blob BLOB NOT NULL,
            final_birth_blob BLOB NOT NULL,
            final_rng_blob BLOB NOT NULL,
            final_step INTEGER NOT NULL,
            final_signal_cursor INTEGER NOT NULL,
            population_json TEXT NOT NULL,
            attachments_json TEXT NOT NULL,
            final_morphology_hash TEXT NOT NULL,
            final_process_hash TEXT NOT NULL,
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS history_events (
            run_key TEXT NOT NULL,
            step INTEGER NOT NULL,
            input_value REAL NOT NULL,
            added_cells_blob BLOB NOT NULL,
            population INTEGER NOT NULL,
            state_hash TEXT NOT NULL,
            PRIMARY KEY (run_key, step)
        );

        CREATE TABLE IF NOT EXISTS checkpoints (
            checkpoint_key TEXT PRIMARY KEY,
            run_key TEXT NOT NULL,
            label TEXT NOT NULL,
            step INTEGER NOT NULL,
            signal_cursor INTEGER NOT NULL,
            occupied_blob BLOB NOT NULL,
            birth_blob BLOB NOT NULL,
            rng_blob BLOB NOT NULL,
            population_json TEXT NOT NULL,
            attachments_json TEXT NOT NULL,
            process_hash TEXT NOT NULL,
            morphology_hash TEXT NOT NULL,
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS analyses (
            analysis_key TEXT PRIMARY KEY,
            analysis_type TEXT NOT NULL,
            config_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        self.conn.execute(
            "INSERT OR REPLACE INTO metadata(key,value) VALUES('schema_version',?)",
            (str(SCHEMA_VERSION),),
        )
        self.conn.commit()

    @staticmethod
    def _pack_json(obj) -> bytes:
        return zlib.compress(json.dumps(obj).encode("utf-8"), 6)

    @staticmethod
    def _unpack_json(blob: bytes):
        return json.loads(zlib.decompress(blob).decode("utf-8"))

    def close(self):
        self.conn.close()

    def put_reference_run(self, spec: ExperimentSpec, result: RunResult):
        state = result.state
        self.conn.execute("""
        INSERT OR REPLACE INTO runs(
            run_key, spec_json, signal_blob,
            final_occupied_blob, final_birth_blob, final_rng_blob,
            final_step, final_signal_cursor,
            population_json, attachments_json,
            final_morphology_hash, final_process_hash, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            spec.run_key(),
            json.dumps(spec.key_dict(), sort_keys=True),
            self._pack_json(result.signal.tolist()),
            serialize_cells(state.occupied),
            serialize_birth(state.birth_time),
            serialize_rng_state(state.rng_state),
            state.step,
            state.signal_cursor,
            json.dumps(state.population_by_step),
            json.dumps(state.attachments_by_step),
            morphology_hash(state.occupied, state.birth_time),
            process_state_hash(state),
            time.time(),
        ))

        self.conn.execute(
            "DELETE FROM history_events WHERE run_key=?",
            (spec.run_key(),),
        )
        for ev in result.history:
            self.conn.execute("""
            INSERT INTO history_events(
                run_key, step, input_value, added_cells_blob,
                population, state_hash
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                spec.run_key(),
                ev.step,
                ev.input_value,
                self._pack_json([[q, r] for q, r in ev.added_cells]),
                ev.population,
                ev.state_hash,
            ))
        self.conn.commit()

    def get_reference_run(self, spec: ExperimentSpec) -> Optional[RunResult]:
        row = self.conn.execute("""
        SELECT signal_blob, final_occupied_blob, final_birth_blob, final_rng_blob,
               final_step, final_signal_cursor, population_json, attachments_json
        FROM runs WHERE run_key=?
        """, (spec.run_key(),)).fetchone()

        if row is None:
            return None

        signal = np.asarray(self._unpack_json(row[0]), dtype=float)
        state = CrystalState(
            occupied=deserialize_cells(row[1]),
            birth_time=deserialize_birth(row[2]),
            rng_state=deserialize_rng_state(row[3]),
            step=int(row[4]),
            signal_cursor=int(row[5]),
            population_by_step=list(json.loads(row[6])),
            attachments_by_step=list(json.loads(row[7])),
        )

        events = []
        for erow in self.conn.execute("""
        SELECT step, input_value, added_cells_blob, population, state_hash
        FROM history_events
        WHERE run_key=?
        ORDER BY step
        """, (spec.run_key(),)):
            added = [tuple(x) for x in self._unpack_json(erow[2])]
            events.append(
                HistoryEvent(
                    step=int(erow[0]),
                    input_value=float(erow[1]),
                    added_cells=added,
                    population=int(erow[3]),
                    state_hash=str(erow[4]),
                )
            )

        return RunResult(state=state, history=events, signal=signal)

    def get_or_run_reference(self, spec: ExperimentSpec) -> Tuple[RunResult, bool]:
        cached = self.get_reference_run(spec)
        if cached is not None:
            return cached, True
        result = run_reference(spec)
        self.put_reference_run(spec, result)
        return result, False

    def put_checkpoint(self, run_key: str, label: str, state: CrystalState) -> str:
        checkpoint_key = hashlib.sha256(
            f"{run_key}|{label}|{state.step}".encode("utf-8")
        ).hexdigest()[:24]

        self.conn.execute("""
        INSERT OR REPLACE INTO checkpoints(
            checkpoint_key, run_key, label, step, signal_cursor,
            occupied_blob, birth_blob, rng_blob,
            population_json, attachments_json,
            process_hash, morphology_hash, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            checkpoint_key,
            run_key,
            label,
            state.step,
            state.signal_cursor,
            serialize_cells(state.occupied),
            serialize_birth(state.birth_time),
            serialize_rng_state(state.rng_state),
            json.dumps(state.population_by_step),
            json.dumps(state.attachments_by_step),
            process_state_hash(state),
            morphology_hash(state.occupied, state.birth_time),
            time.time(),
        ))
        self.conn.commit()
        return checkpoint_key

    def get_checkpoint(self, checkpoint_key: str) -> CrystalState:
        row = self.conn.execute("""
        SELECT step, signal_cursor, occupied_blob, birth_blob, rng_blob,
               population_json, attachments_json
        FROM checkpoints WHERE checkpoint_key=?
        """, (checkpoint_key,)).fetchone()

        if row is None:
            raise KeyError(checkpoint_key)

        return CrystalState(
            step=int(row[0]),
            signal_cursor=int(row[1]),
            occupied=deserialize_cells(row[2]),
            birth_time=deserialize_birth(row[3]),
            rng_state=deserialize_rng_state(row[4]),
            population_by_step=list(json.loads(row[5])),
            attachments_by_step=list(json.loads(row[6])),
        )

    def put_analysis(self, key: str, kind: str, config: dict, result: dict):
        self.conn.execute("""
        INSERT OR REPLACE INTO analyses(
            analysis_key, analysis_type, config_json, result_json, created_at
        ) VALUES (?, ?, ?, ?, ?)
        """, (
            key,
            kind,
            json.dumps(config, sort_keys=True),
            json.dumps(result),
            time.time(),
        ))
        self.conn.commit()


# =============================================================================
# 7. CHECKPOINT CONSTRUCTION + REPLAY
# =============================================================================

def state_at_step_from_history(
    crystal_seed: int,
    history: List[HistoryEvent],
    target_step: int,
) -> CrystalState:
    """
    Reconstruct geometry and birth times by replaying recorded additions only.
    RNG state cannot be recovered from additions alone.
    """
    occupied = {(0, 0)}
    birth = {(0, 0): 0}
    population = [1]
    attachments = [1]

    for ev in history:
        if ev.step > target_step:
            break
        for cell in ev.added_cells:
            occupied.add(cell)
            birth[cell] = ev.step
        population.append(len(occupied))
        attachments.append(len(ev.added_cells))

    rng = random.Random(crystal_seed)
    # This RNG state is intentionally not the historical state.
    return CrystalState(
        occupied=occupied,
        birth_time=birth,
        step=target_step,
        rng_state=rng.getstate(),
        signal_cursor=target_step,
        population_by_step=population,
        attachments_by_step=attachments,
    )


def replay_event_log(
    history: List[HistoryEvent],
    target_step: Optional[int] = None,
) -> Tuple[Set[Cell], Dict[Cell, int], List[str]]:
    occupied = {(0, 0)}
    birth = {(0, 0): 0}
    hashes = []

    for ev in history:
        if target_step is not None and ev.step > target_step:
            break
        for cell in ev.added_cells:
            occupied.add(cell)
            birth[cell] = ev.step
        hashes.append(morphology_hash(occupied, birth))

    return occupied, birth, hashes


def exact_checkpoint_from_reference(
    spec: ExperimentSpec,
    reference_signal: np.ndarray,
) -> CrystalState:
    state = initial_state(spec.crystal_seed)
    partial = run_from_state(
        state,
        reference_signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
        stop_after=spec.checkpoint_step,
    )
    return partial.state


# =============================================================================
# 8. VISUALS
# =============================================================================

def draw_crystal(ax, occupied: Set[Cell], birth: Dict[Cell, int], title: str):
    births = np.asarray(list(birth.values()), dtype=float)
    bmin = float(births.min()) if len(births) else 0.0
    bmax = float(births.max()) if len(births) else 1.0
    denom = max(1.0, bmax - bmin)

    for cell in occupied:
        x, y = axial_to_xy(cell)
        value = (birth.get(cell, 0) - bmin) / denom
        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=0.94,
            orientation=np.pi / 6,
            facecolor=plt.cm.viridis(value),
            edgecolor="none",
        )
        ax.add_patch(patch)

    if occupied:
        pts = np.array([axial_to_xy(c) for c in occupied], dtype=float)
        margin = 2.5
        ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
        ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)


def save_reference_figure(
    signal: np.ndarray,
    checkpoint: CrystalState,
    final_state: CrystalState,
    path: Path,
):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    axes[0].plot(signal)
    axes[0].axvline(checkpoint.step, linestyle="--")
    axes[0].set_title("Input signal + checkpoint")
    axes[0].set_xlabel("step")
    axes[0].set_ylabel("forcing")
    draw_crystal(
        axes[1],
        checkpoint.occupied,
        checkpoint.birth_time,
        f"Checkpoint t={checkpoint.step}",
    )
    draw_crystal(
        axes[2],
        final_state.occupied,
        final_state.birth_time,
        f"Final t={final_state.step}",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_restore_comparison(
    reference: CrystalState,
    restored: CrystalState,
    path: Path,
):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    draw_crystal(
        axes[0], reference.occupied, reference.birth_time,
        "Continuous reference"
    )
    draw_crystal(
        axes[1], restored.occupied, restored.birth_time,
        "Checkpoint → restore → continue"
    )
    fig.suptitle("Exact restoration should produce identical final states")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_omission_plot(results: dict, path: Path):
    labels = list(results.keys())
    vals = [results[k]["normalized_difference"] for k in labels]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, vals)
    ax.set_ylabel("normalized final-state difference")
    ax.set_title("What happens when checkpoint information is omitted?")
    ax.set_ylim(0, max(0.05, max(vals) * 1.15 if vals else 0.05))
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_replay_hash_plot(
    reference_hashes: List[str],
    replay_hashes: List[str],
    path: Path,
):
    matches = [
        1 if a == b else 0
        for a, b in zip(reference_hashes, replay_hashes)
    ]
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(range(1, len(matches) + 1), matches)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("step")
    ax.set_ylabel("hash match")
    ax.set_title("Event-log replay vs recorded trajectory")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_branch_figure(
    checkpoint: CrystalState,
    branch_a: CrystalState,
    branch_b: CrystalState,
    path: Path,
):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    draw_crystal(
        axes[0], checkpoint.occupied, checkpoint.birth_time,
        "Shared saved past"
    )
    draw_crystal(
        axes[1], branch_a.occupied, branch_a.birth_time,
        "Future A"
    )
    draw_crystal(
        axes[2], branch_b.occupied, branch_b.birth_time,
        "Future B"
    )
    fig.suptitle("One saved past, two controlled futures")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_branch_divergence(
    divergence: List[float],
    path: Path,
):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(1, len(divergence) + 1), divergence)
    ax.set_xlabel("steps after branch")
    ax.set_ylabel("normalized state difference")
    ax.set_title("Counterfactual divergence after identical checkpoint")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


# =============================================================================
# 9. REPORTER
# =============================================================================

class Reporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.sections: List[Tuple[str, str]] = []

    def write_json(self, filename: str, data: dict):
        path = self.report_dir / filename
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[report] {path}")

    def write_stage(self, filename: str, title: str, body: str):
        text = f"# {title}\n\n{body.strip()}\n"
        path = self.report_dir / filename
        path.write_text(text, encoding="utf-8")
        self.sections.append((title, body.strip()))
        print(f"[report] {path}")

    def write_full(self, metadata: dict) -> Path:
        chunks = [
            "# Chapter 15 — Digital Crystal History: Full Experimental Report",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(metadata, indent=2),
            "```",
            "",
        ]
        for title, body in self.sections:
            chunks += [f"## {title}", "", body, ""]
        path = self.report_dir / "ch15-full-report.md"
        path.write_text("\n".join(chunks), encoding="utf-8")
        print(f"[report] {path}")
        return path


# =============================================================================
# 10. EXPERIMENT STAGES
# =============================================================================

def run_stage_1(
    cache: Cache,
    reporter: Reporter,
    spec: ExperimentSpec,
    image_dir: Path,
):
    print("\n=== STAGE 1 — CONTINUOUS REFERENCE RUN ===")
    reference, cached = cache.get_or_run_reference(spec)

    checkpoint = exact_checkpoint_from_reference(spec, reference.signal)
    checkpoint_key = cache.put_checkpoint(
        spec.run_key(),
        "reference-midpoint",
        checkpoint,
    )

    fig = image_dir / "ch15-01-reference-and-checkpoint.png"
    save_reference_figure(
        reference.signal,
        checkpoint,
        reference.state,
        fig,
    )

    result = {
        "cached": cached,
        "run_key": spec.run_key(),
        "checkpoint_key": checkpoint_key,
        "checkpoint_step": checkpoint.step,
        "checkpoint_population": len(checkpoint.occupied),
        "final_population": len(reference.state.occupied),
        "final_morphology_hash": morphology_hash(
            reference.state.occupied,
            reference.state.birth_time,
        ),
        "final_process_hash": process_state_hash(reference.state),
        "history_events": len(reference.history),
        "figure": str(fig),
    }
    reporter.write_json("stage-01-reference.json", result)
    reporter.write_stage(
        "stage-01-reference.md",
        "Stage 1 — Continuous Reference Run",
        f"""
A continuous Digital Crystal v1 run provides the reference trajectory.

- Run key: `{result['run_key']}`
- Checkpoint step: **{checkpoint.step}**
- Population at checkpoint: **{len(checkpoint.occupied)}**
- Final population: **{len(reference.state.occupied)}**
- Final morphology hash: `{result['final_morphology_hash']}`
- Final process-state hash: `{result['final_process_hash']}`
- Recorded history events: **{len(reference.history)}**
- Cached reference reused: **{cached}**

Figure: `{fig}`

This stage establishes the exact trajectory against which restore and replay
experiments are compared.
""",
    )
    return reference, checkpoint, checkpoint_key, result


def run_stage_2(
    cache: Cache,
    reporter: Reporter,
    spec: ExperimentSpec,
    reference: RunResult,
    checkpoint_key: str,
    image_dir: Path,
):
    print("\n=== STAGE 2 — EXACT CHECKPOINT / RESTORE ===")
    restored_checkpoint = cache.get_checkpoint(checkpoint_key)

    continued = run_from_state(
        restored_checkpoint,
        reference.signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
    )

    ref_state = reference.state
    got = continued.state

    exact_morphology = (
        ref_state.occupied == got.occupied
        and ref_state.birth_time == got.birth_time
    )
    exact_process = process_state_hash(ref_state) == process_state_hash(got)
    population_equal = ref_state.population_by_step == got.population_by_step
    attachments_equal = ref_state.attachments_by_step == got.attachments_by_step

    fig = image_dir / "ch15-02-exact-restore.png"
    save_restore_comparison(ref_state, got, fig)

    result = {
        "exact_morphology": exact_morphology,
        "exact_process_state": exact_process,
        "population_trajectory_equal": population_equal,
        "attachment_trajectory_equal": attachments_equal,
        "reference_morphology_hash": morphology_hash(
            ref_state.occupied, ref_state.birth_time
        ),
        "restored_morphology_hash": morphology_hash(
            got.occupied, got.birth_time
        ),
        "reference_process_hash": process_state_hash(ref_state),
        "restored_process_hash": process_state_hash(got),
        "symmetric_difference_cells": symmetric_difference_count(
            ref_state.occupied, got.occupied
        ),
        "figure": str(fig),
    }

    reporter.write_json("stage-02-exact-restore.json", result)
    reporter.write_stage(
        "stage-02-exact-restore.md",
        "Stage 2 — Save, Restore, Continue",
        f"""
The midpoint state was serialized to SQLite, loaded into a new runtime state,
and continued using the remaining input.

Results:

- Exact final morphology: **{exact_morphology}**
- Exact final process state: **{exact_process}**
- Population trajectory identical: **{population_equal}**
- Attachment trajectory identical: **{attachments_equal}**
- Symmetric-difference cells: **{result['symmetric_difference_cells']}**

Reference morphology hash: `{result['reference_morphology_hash']}`  
Restored morphology hash: `{result['restored_morphology_hash']}`

Reference process hash: `{result['reference_process_hash']}`  
Restored process hash: `{result['restored_process_hash']}`

Figure: `{fig}`

An exact pass means the checkpoint preserved sufficient process state to resume
the stochastic growth process without changing its future.
""",
    )
    return result


def run_stage_3(
    reporter: Reporter,
    spec: ExperimentSpec,
    reference: RunResult,
    checkpoint: CrystalState,
    image_dir: Path,
):
    print("\n=== STAGE 3 — WHAT BELONGS TO STATE? ===")

    variants: Dict[str, CrystalState] = {}

    # Full state control.
    variants["full_state"] = checkpoint

    # Omit RNG state by resetting it to a new generator at same nominal seed.
    reset_rng = random.Random(spec.crystal_seed + 987654321)
    variants["no_rng_state"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=reset_rng.getstate(),
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )

    # Wrong signal cursor: replay future from three steps earlier if possible.
    wrong_cursor = max(0, checkpoint.signal_cursor - 3)
    variants["wrong_signal_cursor"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=checkpoint.rng_state,
        signal_cursor=wrong_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )

    # Morphology only: correct occupied cells, but reconstruct birth times as if
    # all non-seed cells appeared at checkpoint. Also resets RNG.
    morph_birth = {
        cell: (0 if cell == (0, 0) else checkpoint.step)
        for cell in checkpoint.occupied
    }
    morph_rng = random.Random(spec.crystal_seed)
    variants["morphology_only"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=morph_birth,
        step=checkpoint.step,
        rng_state=morph_rng.getstate(),
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=[len(checkpoint.occupied)],
        attachments_by_step=[0],
    )

    results = {}
    for name, state in variants.items():
        continued = run_from_state(
            state,
            reference.signal,
            max_radius=spec.max_radius,
            params=spec.model_params,
        )
        got = continued.state
        diff = normalized_state_difference(
            reference.state.occupied,
            got.occupied,
        )
        results[name] = {
            "final_population": len(got.occupied),
            "morphology_hash": morphology_hash(
                got.occupied, got.birth_time
            ),
            "process_hash": process_state_hash(got),
            "normalized_difference": diff,
            "symmetric_difference_cells": symmetric_difference_count(
                reference.state.occupied,
                got.occupied,
            ),
            "exact_occupied_set": got.occupied == reference.state.occupied,
            "exact_birth_times": got.birth_time == reference.state.birth_time,
        }

    fig = image_dir / "ch15-03-state-omission.png"
    save_omission_plot(results, fig)

    reporter.write_json("stage-03-state-omission.json", results)
    reporter.write_stage(
        "stage-03-state-omission.md",
        "Stage 3 — What Information Is Actually Part of State?",
        f"""
The checkpoint was deliberately damaged before continuation.

```json
{json.dumps(results, indent=2)}
```

Figure: `{fig}`

The purpose is not to define state philosophically. It is to discover which
stored variables are causally required for faithful continuation.

A variable belongs to operational process state when omitting or corrupting it
changes the continuation.
""",
    )
    return results


def run_stage_4(
    reporter: Reporter,
    spec: ExperimentSpec,
    reference: RunResult,
    image_dir: Path,
):
    print("\n=== STAGE 4 — HISTORY REPLAY ===")

    # A. Procedural replay from seed + signal.
    procedural = run_reference(spec)

    procedural_exact_morphology = (
        procedural.state.occupied == reference.state.occupied
        and procedural.state.birth_time == reference.state.birth_time
    )
    procedural_exact_process = (
        process_state_hash(procedural.state)
        == process_state_hash(reference.state)
    )

    # B. Event-log replay from recorded additions.
    replay_occupied, replay_birth, replay_hashes = replay_event_log(
        reference.history
    )
    event_exact = (
        replay_occupied == reference.state.occupied
        and replay_birth == reference.state.birth_time
    )

    reference_hashes = [ev.state_hash for ev in reference.history]
    trajectory_hash_matches = [
        a == b for a, b in zip(reference_hashes, replay_hashes)
    ]
    all_trajectory_hashes_match = (
        len(reference_hashes) == len(replay_hashes)
        and all(trajectory_hash_matches)
    )

    fig = image_dir / "ch15-04-history-replay.png"
    save_replay_hash_plot(reference_hashes, replay_hashes, fig)

    result = {
        "procedural_replay_exact_morphology": procedural_exact_morphology,
        "procedural_replay_exact_process": procedural_exact_process,
        "event_log_replay_exact_final_morphology": event_exact,
        "event_log_all_trajectory_hashes_match": all_trajectory_hashes_match,
        "trajectory_steps": len(reference_hashes),
        "trajectory_hash_match_count": int(sum(trajectory_hash_matches)),
        "figure": str(fig),
    }

    reporter.write_json("stage-04-history-replay.json", result)
    reporter.write_stage(
        "stage-04-history-replay.md",
        "Stage 4 — Can the Past Be Reconstructed?",
        f"""
Two different notions of replay were tested.

### Procedural replay

Start from the original seed and replay the same input through the same frozen
rule.

- Exact final morphology: **{procedural_exact_morphology}**
- Exact final process state: **{procedural_exact_process}**

### Event-log replay

Ignore stochastic re-execution and instead replay the recorded cell-addition
events.

- Exact final morphology: **{event_exact}**
- All trajectory hashes match: **{all_trajectory_hashes_match}**
- Matching trajectory hashes: **{sum(trajectory_hash_matches)}/{len(reference_hashes)}**

Figure: `{fig}`

The event log is a genuine formation record only if it can reconstruct every
recorded state, not merely something visually similar.
""",
    )
    return result


def run_stage_5(
    reporter: Reporter,
    spec: ExperimentSpec,
    reference: RunResult,
    checkpoint: CrystalState,
):
    print("\n=== STAGE 5 — STATE VS HISTORY ===")

    # Can history reconstruct the checkpoint morphology?
    hist_state = state_at_step_from_history(
        spec.crystal_seed,
        reference.history,
        checkpoint.step,
    )
    history_reconstructs_checkpoint = (
        hist_state.occupied == checkpoint.occupied
        and hist_state.birth_time == checkpoint.birth_time
    )

    # Can checkpoint tell us exact event sequence? Not inherently.
    # We quantify this structurally: checkpoint stores no ordered event rows.
    checkpoint_has_explicit_event_sequence = False

    # Can state continue exactly?
    state_continued = run_from_state(
        checkpoint,
        reference.signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
    ).state
    state_continues_exactly = (
        state_continued.occupied == reference.state.occupied
        and state_continued.birth_time == reference.state.birth_time
        and process_state_hash(state_continued) == process_state_hash(reference.state)
    )

    # Can history-only reconstructed geometry continue exactly WITHOUT historical RNG?
    hist_continued = run_from_state(
        hist_state,
        reference.signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
    ).state
    history_geometry_only_continues_exactly = (
        hist_continued.occupied == reference.state.occupied
        and hist_continued.birth_time == reference.state.birth_time
    )
    history_geometry_only_difference = normalized_state_difference(
        hist_continued.occupied,
        reference.state.occupied,
    )

    result = {
        "history_reconstructs_checkpoint_morphology": history_reconstructs_checkpoint,
        "checkpoint_contains_explicit_event_sequence": checkpoint_has_explicit_event_sequence,
        "checkpoint_state_continues_exactly": state_continues_exactly,
        "history_reconstructed_geometry_without_rng_continues_exactly": (
            history_geometry_only_continues_exactly
        ),
        "history_geometry_only_final_difference": history_geometry_only_difference,
    }

    reporter.write_json("stage-05-state-vs-history.json", result)
    reporter.write_stage(
        "stage-05-state-vs-history.md",
        "Stage 5 — State Is Not History",
        f"""
Results:

```json
{json.dumps(result, indent=2)}
```

The distinction is operational:

- A **checkpoint state** can continue the process exactly if it contains the
  required continuation variables.
- A **history log** can reconstruct the route to a prior morphology.
- The checkpoint does not, by itself, contain an ordered list of events.
- Reconstructed geometry alone does not necessarily reproduce the exact future,
  because continuation state includes more than visible morphology.

This is the chapter's central separation:

```text
STATE
= enough information to continue from here

HISTORY
= enough information to reconstruct how here was reached
```
""",
    )
    return result


def run_stage_6(
    reporter: Reporter,
    spec: ExperimentSpec,
    checkpoint: CrystalState,
    image_dir: Path,
):
    print("\n=== STAGE 6 — COUNTERFACTUAL BRANCHING ===")

    future_len = spec.steps - checkpoint.signal_cursor
    future_a = make_branch_future(
        "future_a",
        future_len,
        seed=spec.signal_seed + 1111,
    )
    future_b = make_branch_future(
        "future_b",
        future_len,
        seed=spec.signal_seed + 2222,
    )

    # Build branch-specific full signal arrays so current cursor points into them.
    prefix = np.zeros(checkpoint.signal_cursor, dtype=float)
    signal_a = np.concatenate([prefix, future_a])
    signal_b = np.concatenate([prefix, future_b])

    # Same exact checkpoint and same RNG state for both branches.
    a_state = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=checkpoint.rng_state,
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )
    b_state = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=checkpoint.rng_state,
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )

    # Run step by step to measure divergence through time.
    divergence = []
    for _ in tqdm(range(future_len), desc="Branch divergence"):
        a_val = float(signal_a[a_state.signal_cursor])
        b_val = float(signal_b[b_state.signal_cursor])

        a_state, _ = advance_one_step(
            a_state, a_val, spec.max_radius, spec.model_params
        )
        b_state, _ = advance_one_step(
            b_state, b_val, spec.max_radius, spec.model_params
        )
        divergence.append(
            normalized_state_difference(a_state.occupied, b_state.occupied)
        )

    figure = image_dir / "ch15-06-counterfactual-branches.png"
    save_branch_figure(checkpoint, a_state, b_state, figure)

    div_fig = image_dir / "ch15-06-counterfactual-divergence.png"
    save_branch_divergence(divergence, div_fig)

    result = {
        "shared_checkpoint_morphology_hash": morphology_hash(
            checkpoint.occupied, checkpoint.birth_time
        ),
        "future_a_final_morphology_hash": morphology_hash(
            a_state.occupied, a_state.birth_time
        ),
        "future_b_final_morphology_hash": morphology_hash(
            b_state.occupied, b_state.birth_time
        ),
        "final_normalized_difference": (
            divergence[-1] if divergence else 0.0
        ),
        "final_symmetric_difference_cells": symmetric_difference_count(
            a_state.occupied, b_state.occupied
        ),
        "branch_a_population": len(a_state.occupied),
        "branch_b_population": len(b_state.occupied),
        "divergence_series": divergence,
        "figure_branches": str(figure),
        "figure_divergence": str(div_fig),
    }

    reporter.write_json("stage-06-counterfactual-branch.json", result)
    reporter.write_stage(
        "stage-06-counterfactual-branch.md",
        "Stage 6 — One Past, Two Futures",
        f"""
The exact same checkpoint was restored twice.

Both branches begin with:

- identical morphology,
- identical birth-time map,
- identical RNG state,
- identical timestep,
- identical signal cursor.

Only the future input differs.

Results:

- Shared checkpoint hash: `{result['shared_checkpoint_morphology_hash']}`
- Future A hash: `{result['future_a_final_morphology_hash']}`
- Future B hash: `{result['future_b_final_morphology_hash']}`
- Final normalized state difference: **{result['final_normalized_difference']:.6f}**
- Final symmetric-difference cells: **{result['final_symmetric_difference_cells']}**

Figures:
- `{figure}`
- `{div_fig}`

A saved state is therefore not merely an archival snapshot. It is an executable
branch point from which controlled alternative futures can be generated.
""",
    )
    return result


def run_stage_7(
    reporter: Reporter,
    stage2: dict,
    stage3: dict,
    stage4: dict,
    stage5: dict,
    stage6: dict,
):
    print("\n=== STAGE 7 — COALESCED VERDICT ===")

    exact_restore = (
        stage2["exact_morphology"]
        and stage2["exact_process_state"]
        and stage2["population_trajectory_equal"]
        and stage2["attachment_trajectory_equal"]
    )

    replay_ok = (
        stage4["procedural_replay_exact_morphology"]
        and stage4["procedural_replay_exact_process"]
        and stage4["event_log_replay_exact_final_morphology"]
        and stage4["event_log_all_trajectory_hashes_match"]
    )

    state_history_separated = (
        stage5["history_reconstructs_checkpoint_morphology"]
        and stage5["checkpoint_state_continues_exactly"]
        and not stage5[
            "history_reconstructed_geometry_without_rng_continues_exactly"
        ]
    )

    branch_real = stage6["final_normalized_difference"] > 0.0

    omission_has_effect = any(
        (
            name != "full_state"
            and (
                not values["exact_occupied_set"]
                or not values["exact_birth_times"]
            )
        )
        for name, values in stage3.items()
    )

    if (
        exact_restore
        and replay_ok
        and state_history_separated
        and branch_real
        and omission_has_effect
    ):
        verdict = "RECOVERABLE_PAST_SUPPORTED"
        claim = (
            "Within Digital Crystal v1, a complete checkpoint can resume the "
            "stochastic process exactly, an explicit event history can "
            "reconstruct its formation trajectory exactly, and the same saved "
            "past can be used as a controlled branch point for different futures. "
            "Operational state and operational history are distinct."
        )
    elif exact_restore and replay_ok:
        verdict = "PARTIALLY_SUPPORTED"
        claim = (
            "Checkpoint restoration and history replay succeeded, but one or "
            "more stronger state/history separation or branching tests did not "
            "behave as expected."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        claim = (
            "This implementation did not establish reliable exact checkpoint "
            "continuation and/or history reconstruction. The history model "
            "should be revised before the chapter makes a positive claim."
        )

    result = {
        "verdict": verdict,
        "bounded_claim": claim,
        "exact_checkpoint_restore": exact_restore,
        "history_replay": replay_ok,
        "state_history_operationally_distinct": state_history_separated,
        "incomplete_state_changes_future": omission_has_effect,
        "counterfactual_branching_produces_divergence": branch_real,
        "explicit_nonclaims": [
            "learning",
            "adaptation",
            "agency",
            "selfhood",
            "understanding",
            "biological memory",
            "life",
        ],
    }

    reporter.write_json("ch15-summary.json", result)
    reporter.write_stage(
        "stage-07-verdict.md",
        "Stage 7 — Experimental Verdict",
        f"""
**Verdict: `{verdict}`**

> {claim}

Checks:

- Exact checkpoint/restore: **{exact_restore}**
- Exact history replay: **{replay_ok}**
- State/history operationally distinct: **{state_history_separated}**
- Incomplete state changes continuation: **{omission_has_effect}**
- Same past can branch into different futures: **{branch_real}**

This does **not** establish learning, adaptation, agency, selfhood, understanding,
or life.

It establishes only a smaller digital capability:

```text
PRESENT STATE
+
RECOVERABLE FORMATION HISTORY
+
EXACT RESTORATION
+
COUNTERFACTUAL BRANCHING
```
""",
    )
    return result


# =============================================================================
# 11. OPTIONAL REPLICATE VALIDATION
# =============================================================================

def replicate_validation(
    cache: Cache,
    base_seed: int,
    profile: dict,
    reporter: Reporter,
):
    """
    Small repeated exact-restore validation across independent seeds.
    This is not expensive enough to need elaborate analysis but catches
    accidental one-run success.
    """
    print("\n=== REPLICATE VALIDATION ===")
    rows = []

    for i in tqdm(range(profile["replicates"]), desc="Restore replicates"):
        spec = ExperimentSpec(
            run_name=f"replicate-{i}",
            signal_seed=base_seed + i * 1009,
            crystal_seed=base_seed + 5_000_000 + i * 2003,
            steps=profile["steps"],
            max_radius=profile["max_radius"],
            checkpoint_step=profile["checkpoint_step"],
            signal_kind="composite",
        )

        ref, cached = cache.get_or_run_reference(spec)
        cp = exact_checkpoint_from_reference(spec, ref.signal)
        restored = run_from_state(
            cp,
            ref.signal,
            max_radius=spec.max_radius,
            params=spec.model_params,
        ).state

        rows.append({
            "replicate": i,
            "cached": cached,
            "exact_morphology": (
                restored.occupied == ref.state.occupied
                and restored.birth_time == ref.state.birth_time
            ),
            "exact_process": (
                process_state_hash(restored)
                == process_state_hash(ref.state)
            ),
            "difference": normalized_state_difference(
                restored.occupied,
                ref.state.occupied,
            ),
        })

    exact_count = sum(
        1 for r in rows
        if r["exact_morphology"] and r["exact_process"]
    )
    result = {
        "replicates": len(rows),
        "exact_count": exact_count,
        "all_exact": exact_count == len(rows),
        "rows": rows,
    }

    reporter.write_json("stage-02b-restore-replicates.json", result)
    reporter.write_stage(
        "stage-02b-restore-replicates.md",
        "Stage 2B — Checkpoint Restore Across Independent Runs",
        f"""
Independent exact-restore validation:

- Replicates: **{len(rows)}**
- Exact morphology + process state: **{exact_count}/{len(rows)}**
- All exact: **{result['all_exact']}**

This reduces the chance that exact restoration was peculiar to one random run.
""",
    )
    return result


# =============================================================================
# 12. MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Chapter 15 — Digital Crystal state/history experiment"
    )
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILES),
        default="quick",
    )
    parser.add_argument(
        "--db",
        default="research/digital-life/ch15-digital-crystal-history.sqlite3",
    )
    parser.add_argument(
        "--images",
        default="static/images/books/digital-life",
    )
    parser.add_argument(
        "--reports",
        default="research/digital-life/ch15-reports",
    )
    parser.add_argument("--seed", type=int, default=20260811)
    parser.add_argument("--force-recompute", action="store_true")
    args = parser.parse_args()

    profile = PROFILES[args.profile]
    db_path = Path(args.db)
    image_dir = Path(args.images)
    report_dir = Path(args.reports)

    image_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    if args.force_recompute and db_path.exists():
        db_path.unlink()

    cache = Cache(db_path)
    reporter = Reporter(report_dir)

    spec = ExperimentSpec(
        run_name="chapter-15-primary",
        signal_seed=args.seed + 100,
        crystal_seed=args.seed + 200,
        steps=profile["steps"],
        max_radius=profile["max_radius"],
        checkpoint_step=profile["checkpoint_step"],
        signal_kind="composite",
    )

    metadata = {
        "model_version": MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "database": str(db_path),
        "images": str(image_dir),
        "reports": str(report_dir),
        "started_at_unix": time.time(),
        "spec": spec.key_dict(),
    }

    reference, checkpoint, checkpoint_key, stage1 = run_stage_1(
        cache, reporter, spec, image_dir
    )

    stage2 = run_stage_2(
        cache, reporter, spec, reference, checkpoint_key, image_dir
    )

    replicate_result = replicate_validation(
        cache, args.seed + 20_000_000, profile, reporter
    )

    stage3 = run_stage_3(
        reporter, spec, reference, checkpoint, image_dir
    )

    stage4 = run_stage_4(
        reporter, spec, reference, image_dir
    )

    stage5 = run_stage_5(
        reporter, spec, reference, checkpoint
    )

    stage6 = run_stage_6(
        reporter, spec, checkpoint, image_dir
    )

    stage7 = run_stage_7(
        reporter, stage2, stage3, stage4, stage5, stage6
    )

    metadata["finished_at_unix"] = time.time()
    metadata["final_verdict"] = stage7["verdict"]
    metadata["replicate_restore_all_exact"] = replicate_result["all_exact"]

    full_report = reporter.write_full(metadata)

    print("\n" + "=" * 80)
    print("CHAPTER 15 DIGITAL CRYSTAL HISTORY EXPERIMENT COMPLETE")
    print("=" * 80)
    print(f"Verdict:       {stage7['verdict']}")
    print(stage7["bounded_claim"])
    print()
    print(f"SQLite cache:  {db_path}")
    print(f"Full report:   {full_report}")
    print(f"Summary JSON:  {report_dir / 'ch15-summary.json'}")
    print(f"Figures:       {image_dir}")
    print("=" * 80)

    cache.close()


if __name__ == "__main__":
    main()
