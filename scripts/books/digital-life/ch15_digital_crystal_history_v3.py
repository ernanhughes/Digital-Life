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

    What information is sufficient for a Digital Crystal to continue faithfully,
    and what additional record is sufficient to reconstruct its formation past?

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
        - wrong signal cursor at a fixed continuation horizon
        - birth-time metadata only
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

Stage 6 — Counterfactual branching + stochastic null
    Restore the same checkpoint repeatedly.
    Compare different-future/same-RNG divergence against a same-future/
    different-RNG stochastic null.

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
EXPERIMENT_VERSION = "digital-crystal-history-v3"
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
        "branch_null_reps": 12,
    },
    "standard": {
        "steps": 72,
        "max_radius": 44,
        "checkpoint_step": 36,
        "replicates": 12,
        "branch_null_reps": 30,
    },
    "full": {
        "steps": 96,
        "max_radius": 56,
        "checkpoint_step": 48,
        "replicates": 30,
        "branch_null_reps": 60,
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
        # Reproducibility invariant:
        #
        # RNG draws must be assigned to candidate cells in a canonical order.
        # Iterating a Python set directly makes the scientific trajectory depend
        # on the set's accidental internal/hash-table layout. A checkpoint that
        # serializes and reconstructs the same mathematical occupied set can
        # otherwise resume with a different frontier iteration order, causing
        # identical RNG state to be consumed by different cells.
        #
        # Sorting removes that hidden implementation state from the model.
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
# 7B. REPRODUCIBILITY INVARIANT CHECK
# =============================================================================

def canonical_roundtrip_state(state: CrystalState) -> CrystalState:
    """
    Reconstruct the same mathematical state through the same canonical
    serialization representations used by the checkpoint layer.

    This deliberately creates fresh Python set/dict objects. Before v3, that
    could change set iteration order and therefore change which frontier cell
    received which RNG draw.
    """
    occupied = deserialize_cells(serialize_cells(state.occupied))
    birth_time = deserialize_birth(serialize_birth(state.birth_time))
    rng_state = deserialize_rng_state(serialize_rng_state(state.rng_state))

    return CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=state.step,
        rng_state=rng_state,
        signal_cursor=state.signal_cursor,
        population_by_step=list(state.population_by_step),
        attachments_by_step=list(state.attachments_by_step),
    )


def run_reproducibility_invariant_check(
    reporter: Reporter,
    spec: ExperimentSpec,
    checkpoint: CrystalState,
    reference_signal: np.ndarray,
):
    """
    Scientific implementation check.

    Two states that are mathematically identical but have independently
    reconstructed Python containers must receive identical RNG decisions and
    therefore produce identical one-step and full-horizon continuations.

    This guards against accidental dependence on Python set/hash-table layout.
    """
    print("\n=== REPRODUCIBILITY INVARIANT — CANONICAL RNG TRAVERSAL ===")

    reconstructed = canonical_roundtrip_state(checkpoint)

    state_identity = {
        "occupied_equal": reconstructed.occupied == checkpoint.occupied,
        "birth_time_equal": reconstructed.birth_time == checkpoint.birth_time,
        "step_equal": reconstructed.step == checkpoint.step,
        "signal_cursor_equal": reconstructed.signal_cursor == checkpoint.signal_cursor,
        "rng_state_equal": reconstructed.rng_state == checkpoint.rng_state,
        "process_hash_equal": (
            process_state_hash(reconstructed) == process_state_hash(checkpoint)
        ),
    }

    # One-step check: catches ordering dependence at the first RNG-consuming step.
    input_value_a = float(reference_signal[checkpoint.signal_cursor])
    input_value_b = float(reference_signal[reconstructed.signal_cursor])

    one_a, additions_a = advance_one_step(
        checkpoint,
        input_value_a,
        spec.max_radius,
        spec.model_params,
    )
    one_b, additions_b = advance_one_step(
        reconstructed,
        input_value_b,
        spec.max_radius,
        spec.model_params,
    )

    one_step_exact = (
        one_a.occupied == one_b.occupied
        and one_a.birth_time == one_b.birth_time
        and one_a.rng_state == one_b.rng_state
        and one_a.signal_cursor == one_b.signal_cursor
        and additions_a == additions_b
    )

    # Full remaining-horizon check.
    remaining = spec.steps - checkpoint.step

    full_a = run_from_state(
        checkpoint,
        reference_signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
        stop_after=remaining,
    ).state

    full_b = run_from_state(
        reconstructed,
        reference_signal,
        max_radius=spec.max_radius,
        params=spec.model_params,
        stop_after=remaining,
    ).state

    full_horizon_exact = (
        full_a.occupied == full_b.occupied
        and full_a.birth_time == full_b.birth_time
        and process_state_hash(full_a) == process_state_hash(full_b)
        and full_a.population_by_step == full_b.population_by_step
        and full_a.attachments_by_step == full_b.attachments_by_step
    )

    result = {
        "implementation_invariant": (
            "RNG-consuming candidate traversal is canonicalized with "
            "sorted(frontier); equivalent mathematical states must not depend "
            "on Python set/hash-table layout."
        ),
        "state_identity_after_roundtrip": state_identity,
        "one_step_exact_after_container_roundtrip": one_step_exact,
        "one_step_additions_equal": additions_a == additions_b,
        "full_remaining_horizon_exact_after_container_roundtrip": full_horizon_exact,
        "remaining_steps_checked": remaining,
        "passed": (
            all(state_identity.values())
            and one_step_exact
            and full_horizon_exact
        ),
    }

    reporter.write_json(
        "stage-00-reproducibility-invariant.json",
        result,
    )
    reporter.write_stage(
        "stage-00-reproducibility-invariant.md",
        "Stage 0 — Reproducibility Invariant",
        f"""
The stochastic model must not depend on accidental Python container layout.

Digital Crystal history v3 therefore consumes RNG draws over a canonical
`sorted(frontier)` order.

A checkpoint was reconstructed through fresh serialized/deserialized
`set`, `dict`, and RNG-state objects and compared with the original checkpoint.

```json
{json.dumps(result, indent=2)}
```

A pass means two mathematically identical states produce the same one-step and
remaining-horizon continuation even when their Python containers were rebuilt
independently.
""",
    )

    if not result["passed"]:
        raise RuntimeError(
            "Reproducibility invariant failed: equivalent mathematical states "
            "do not continue identically."
        )

    return result


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
    print("\n=== STAGE 3 — WHAT BELONGS TO CONTINUATION STATE? ===")

    # IMPORTANT: every variant below is advanced for exactly the same number of
    # update steps. This prevents the signal-cursor ablation from accidentally
    # changing the continuation horizon.
    continuation_steps = spec.steps - checkpoint.step

    variants: Dict[str, CrystalState] = {}

    # Full-state positive control.
    variants["full_state"] = checkpoint

    # RNG-only ablation: preserve everything else, substitute another valid RNG
    # state. If morphology diverges, RNG state is causally required for exact
    # continuation under this representation.
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

    # Cursor-only ablation. The prior v1 script accidentally allowed a changed
    # cursor to change the number of updates because run_from_state normally runs
    # to the end of the signal. v2 forces the SAME continuation step count for
    # every variant, isolating signal position from continuation horizon.
    wrong_cursor = max(0, checkpoint.signal_cursor - 3)
    variants["wrong_signal_cursor_fixed_horizon"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=checkpoint.rng_state,
        signal_cursor=wrong_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )

    # Birth-time-only ablation. This isolates birth metadata while preserving the
    # exact occupied set, RNG state, timestep and signal cursor. In Digital
    # Crystal v1, advance_one_step does not consult birth_time when deciding new
    # attachment, so this test should tell us whether birth metadata is merely
    # historical/observational or actually part of causal continuation state.
    altered_birth = {
        cell: (0 if cell == (0, 0) else checkpoint.step)
        for cell in checkpoint.occupied
    }
    variants["birth_times_only"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=altered_birth,
        step=checkpoint.step,
        rng_state=checkpoint.rng_state,
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )

    # Visible-morphology-only stress test. This deliberately removes multiple
    # hidden continuation variables at once. It can establish only that visible
    # morphology is insufficient; it must NOT be used to attribute necessity to
    # any one omitted field.
    morph_rng = random.Random(spec.crystal_seed)
    variants["morphology_only"] = CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=altered_birth,
        step=checkpoint.step,
        rng_state=morph_rng.getstate(),
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=[len(checkpoint.occupied)],
        attachments_by_step=[0],
    )

    results = {}
    for name, state in variants.items():
        start_step = state.step
        start_cursor = state.signal_cursor
        continued = run_from_state(
            state,
            reference.signal,
            max_radius=spec.max_radius,
            params=spec.model_params,
            stop_after=continuation_steps,
        )
        got = continued.state
        diff = normalized_state_difference(
            reference.state.occupied,
            got.occupied,
        )
        results[name] = {
            "starting_step": int(start_step),
            "starting_signal_cursor": int(start_cursor),
            "requested_continuation_steps": int(continuation_steps),
            "executed_steps": int(got.step - start_step),
            "final_step": int(got.step),
            "final_signal_cursor": int(got.signal_cursor),
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
            "exact_process_hash": (
                process_state_hash(got) == process_state_hash(reference.state)
            ),
        }

    # Explicit assertions make the cursor test scientifically auditable.
    for name, values in results.items():
        if values["executed_steps"] != continuation_steps:
            raise AssertionError(
                f"{name}: continuation horizon changed: "
                f"expected {continuation_steps}, got {values['executed_steps']}"
            )
        if values["final_step"] != spec.steps:
            raise AssertionError(
                f"{name}: final logical step changed: "
                f"expected {spec.steps}, got {values['final_step']}"
            )

    birth_is_growth_causal = not results["birth_times_only"]["exact_occupied_set"]
    cursor_changes_growth = not results[
        "wrong_signal_cursor_fixed_horizon"
    ]["exact_occupied_set"]
    rng_changes_growth = not results["no_rng_state"]["exact_occupied_set"]
    visible_morphology_sufficient = results["morphology_only"]["exact_occupied_set"]

    interpretation = {
        "full_checkpoint_is_sufficient": results["full_state"]["exact_process_hash"],
        "rng_state_changes_exact_growth_continuation": rng_changes_growth,
        "signal_cursor_changes_growth_at_fixed_horizon": cursor_changes_growth,
        "birth_times_change_growth_continuation": birth_is_growth_causal,
        "birth_times_are_historical_metadata_if_false_above": not birth_is_growth_causal,
        "visible_morphology_alone_is_sufficient": visible_morphology_sufficient,
        "minimum_state_identified": False,
        "note": (
            "These ablations identify sufficiency and specific causal omissions; "
            "they do not prove that the stored checkpoint is a minimal sufficient state."
        ),
    }

    fig = image_dir / "ch15-03-state-omission.png"
    save_omission_plot(results, fig)

    reporter.write_json(
        "stage-03-state-omission.json",
        {"variants": results, "interpretation": interpretation},
    )
    reporter.write_stage(
        "stage-03-state-omission.md",
        "Stage 3 — What Information Is Actually Part of Continuation State?",
        f"""
All variants were continued for exactly **{continuation_steps} updates**.
This fixes the v1 cursor confound: changing the signal cursor no longer changes
how many continuation updates execute.

```json
{json.dumps({"variants": results, "interpretation": interpretation}, indent=2)}
```

Figure: `{fig}`

Interpretation rules:

- the **full checkpoint** tests sufficiency for exact continuation;
- the **RNG-only** ablation isolates stochastic continuation state;
- the **cursor-only** ablation isolates environmental sequence position while
  holding the continuation horizon fixed;
- the **birth-time-only** ablation tests birth metadata independently;
- the **morphology-only** condition is a combined stress test and establishes
  only whether visible morphology is sufficient.

The experiment does **not** claim that the checkpoint representation is the
minimum possible sufficient state.
""",
    )
    return {"variants": results, "interpretation": interpretation}


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


def _copy_checkpoint_with_rng(checkpoint: CrystalState, rng_state) -> CrystalState:
    return CrystalState(
        occupied=set(checkpoint.occupied),
        birth_time=dict(checkpoint.birth_time),
        step=checkpoint.step,
        rng_state=rng_state,
        signal_cursor=checkpoint.signal_cursor,
        population_by_step=list(checkpoint.population_by_step),
        attachments_by_step=list(checkpoint.attachments_by_step),
    )


def _run_branch_pair(
    checkpoint: CrystalState,
    future_a: np.ndarray,
    future_b: np.ndarray,
    spec: ExperimentSpec,
    rng_state_a=None,
    rng_state_b=None,
):
    """Run two futures from the same visible/process checkpoint for equal steps."""
    future_len = len(future_a)
    if len(future_b) != future_len:
        raise ValueError("Branch futures must have equal length")

    prefix = np.zeros(checkpoint.signal_cursor, dtype=float)
    signal_a = np.concatenate([prefix, future_a])
    signal_b = np.concatenate([prefix, future_b])

    a_state = _copy_checkpoint_with_rng(
        checkpoint,
        checkpoint.rng_state if rng_state_a is None else rng_state_a,
    )
    b_state = _copy_checkpoint_with_rng(
        checkpoint,
        checkpoint.rng_state if rng_state_b is None else rng_state_b,
    )

    divergence = []
    for _ in range(future_len):
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

    return a_state, b_state, divergence


def _summary(values: List[float]) -> dict:
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return {"n": 0}
    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "std": float(np.std(x, ddof=1)) if len(x) > 1 else 0.0,
        "median": float(np.median(x)),
        "q05": float(np.quantile(x, 0.05)),
        "q25": float(np.quantile(x, 0.25)),
        "q75": float(np.quantile(x, 0.75)),
        "q95": float(np.quantile(x, 0.95)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def save_branch_null_figure(
    treatment: List[float],
    stochastic_null: List[float],
    path: Path,
):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    positions = [1, 2]
    ax.boxplot(
        [stochastic_null, treatment],
        positions=positions,
        tick_labels=["same future\ndifferent RNG", "different futures\nsame RNG"],
        showmeans=True,
    )
    ax.set_ylabel("final normalized morphology difference")
    ax.set_title("Counterfactual environmental divergence vs stochastic null")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def run_stage_6(
    reporter: Reporter,
    spec: ExperimentSpec,
    checkpoint: CrystalState,
    image_dir: Path,
    branch_null_reps: int,
):
    print("\n=== STAGE 6 — COUNTERFACTUAL BRANCHING + STOCHASTIC NULL ===")

    future_len = spec.steps - checkpoint.step
    if future_len <= 0:
        raise RuntimeError("Checkpoint leaves no future to branch")

    # ------------------------------------------------------------------
    # A. Illustrative branch pair retained from v1
    # ------------------------------------------------------------------
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

    a_state, b_state, divergence = _run_branch_pair(
        checkpoint,
        future_a,
        future_b,
        spec,
    )

    figure = image_dir / "ch15-06-counterfactual-branches.png"
    save_branch_figure(checkpoint, a_state, b_state, figure)

    div_fig = image_dir / "ch15-06-counterfactual-divergence.png"
    save_branch_divergence(divergence, div_fig)

    # ------------------------------------------------------------------
    # B. Replicated treatment vs stochastic null
    #
    # Treatment:
    #   same exact checkpoint + same RNG state + two different future signals.
    #
    # Null:
    #   same exact checkpoint morphology/process position + same future signal
    #   + two different valid RNG states.
    #
    # This tells us whether environmental branching produces divergence beyond
    # the scale expected from ordinary stochastic continuation variation.
    # ------------------------------------------------------------------
    treatment_diffs: List[float] = []
    null_diffs: List[float] = []
    treatment_cells: List[int] = []
    null_cells: List[int] = []

    for i in tqdm(range(branch_null_reps), desc="Branch/null replicates"):
        base = spec.signal_seed + 10_000 + i * 17
        fa = make_branch_future("future_a", future_len, seed=base + 1)
        fb = make_branch_future("future_b", future_len, seed=base + 2)

        # Treatment: environmental difference only; same historical RNG state.
        ta, tb, _ = _run_branch_pair(
            checkpoint,
            fa,
            fb,
            spec,
            rng_state_a=checkpoint.rng_state,
            rng_state_b=checkpoint.rng_state,
        )
        treatment_diffs.append(
            normalized_state_difference(ta.occupied, tb.occupied)
        )
        treatment_cells.append(
            symmetric_difference_count(ta.occupied, tb.occupied)
        )

        # Stochastic null: same future forcing, different RNG states.
        rng_a = random.Random(spec.crystal_seed + 20_000_000 + i * 1009)
        rng_b = random.Random(spec.crystal_seed + 30_000_000 + i * 2003)
        na, nb, _ = _run_branch_pair(
            checkpoint,
            fa,
            fa,
            spec,
            rng_state_a=rng_a.getstate(),
            rng_state_b=rng_b.getstate(),
        )
        null_diffs.append(
            normalized_state_difference(na.occupied, nb.occupied)
        )
        null_cells.append(
            symmetric_difference_count(na.occupied, nb.occupied)
        )

    treatment_summary = _summary(treatment_diffs)
    null_summary = _summary(null_diffs)

    # Distribution-free descriptive comparison. We deliberately avoid a strong
    # causal significance claim from a small Monte Carlo sample; the empirical
    # probability is transparent and easy to report.
    null_arr = np.asarray(null_diffs, dtype=float)
    treatment_arr = np.asarray(treatment_diffs, dtype=float)
    pairwise_superiority = float(
        np.mean(treatment_arr[:, None] > null_arr[None, :])
    )
    treatment_minus_null_mean = float(
        np.mean(treatment_arr) - np.mean(null_arr)
    )
    treatment_median_over_null_q95 = bool(
        np.median(treatment_arr) > np.quantile(null_arr, 0.95)
    )

    null_fig = image_dir / "ch15-06-counterfactual-null.png"
    save_branch_null_figure(treatment_diffs, null_diffs, null_fig)

    result = {
        "shared_checkpoint_morphology_hash": morphology_hash(
            checkpoint.occupied, checkpoint.birth_time
        ),
        "illustrative_branch": {
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
        },
        "replicated_environment_treatment": {
            "definition": (
                "same checkpoint + same RNG state + different future forcing"
            ),
            "normalized_difference": treatment_summary,
            "symmetric_difference_cells": _summary(
                [float(x) for x in treatment_cells]
            ),
            "values": treatment_diffs,
        },
        "stochastic_null": {
            "definition": (
                "same checkpoint + same future forcing + different valid RNG states"
            ),
            "normalized_difference": null_summary,
            "symmetric_difference_cells": _summary(
                [float(x) for x in null_cells]
            ),
            "values": null_diffs,
        },
        "comparison": {
            "treatment_minus_null_mean": treatment_minus_null_mean,
            "pairwise_superiority_probability": pairwise_superiority,
            "treatment_median_exceeds_null_q95": treatment_median_over_null_q95,
            "interpretation": (
                "The checkpoint is an executable branch point regardless of effect size. "
                "Environmental divergence is unusually large only if the treatment "
                "distribution clearly exceeds the stochastic-null distribution."
            ),
        },
        "figure_branches": str(figure),
        "figure_divergence": str(div_fig),
        "figure_stochastic_null": str(null_fig),
    }

    reporter.write_json("stage-06-counterfactual-branch.json", result)
    reporter.write_stage(
        "stage-06-counterfactual-branch.md",
        "Stage 6 — One Past, Alternative Futures, and a Stochastic Null",
        f"""
The exact same checkpoint can be restored repeatedly and used as an executable
counterfactual branch point.

The stronger question is whether changing future forcing produces divergence
larger than ordinary stochastic continuation variation.

Treatment:

```text
same checkpoint
same RNG state
different future forcing
```

Stochastic null:

```text
same checkpoint
same future forcing
different valid RNG states
```

Replicates per condition: **{branch_null_reps}**

```json
{json.dumps(result, indent=2)}
```

Figures:
- `{figure}`
- `{div_fig}`
- `{null_fig}`

The branch-point capability is supported whenever the checkpoint can be restored
and deliberately driven into alternative futures. A stronger claim that the
environmental treatment creates *unusually large* divergence should be made only
if the treatment distribution clearly exceeds the stochastic null.
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

    variants = stage3["variants"]
    state_interpretation = stage3["interpretation"]

    morphology_insufficient = not state_interpretation[
        "visible_morphology_alone_is_sufficient"
    ]
    rng_matters = state_interpretation[
        "rng_state_changes_exact_growth_continuation"
    ]
    cursor_matters = state_interpretation[
        "signal_cursor_changes_growth_at_fixed_horizon"
    ]
    birth_growth_causal = state_interpretation[
        "birth_times_change_growth_continuation"
    ]

    illustrative_branch_real = (
        stage6["illustrative_branch"]["final_normalized_difference"] > 0.0
    )

    branch_comparison = stage6["comparison"]
    env_divergence_exceeds_null = (
        branch_comparison["treatment_minus_null_mean"] > 0.0
        and branch_comparison["pairwise_superiority_probability"] >= 0.75
    )

    # The chapter's central result does not require environmental divergence to
    # exceed the stochastic null. A checkpoint is an executable branch point if
    # it can be restored exactly and deliberately supplied with alternative
    # futures. The null only controls the stronger effect-size interpretation.
    if (
        exact_restore
        and replay_ok
        and state_history_separated
        and illustrative_branch_real
        and morphology_insufficient
    ):
        verdict = "RECOVERABLE_PAST_SUPPORTED"
        claim = (
            "Within Digital Crystal v1, a complete checkpoint is sufficient "
            "for exact continuation, an explicit event log reconstructs the "
            "exact morphology trajectory, and the same checkpoint can be used "
            "as an executable branch point for controlled alternative futures. "
            "Visible morphology alone is not sufficient continuation state. "
            "These experiments do not establish that the checkpoint is minimal."
        )
    elif exact_restore and replay_ok:
        verdict = "PARTIALLY_SUPPORTED"
        claim = (
            "Checkpoint restoration and morphology-history replay succeeded, "
            "but one or more stronger state/history separation or branching "
            "tests did not behave as expected."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        claim = (
            "This implementation did not establish reliable exact checkpoint "
            "continuation and/or exact morphology-history reconstruction."
        )

    result = {
        "verdict": verdict,
        "bounded_claim": claim,
        "exact_checkpoint_restore": exact_restore,
        "history_replay_exact_morphology_trajectory": replay_ok,
        "state_history_operationally_distinct": state_history_separated,
        "visible_morphology_is_not_sufficient_state": morphology_insufficient,
        "rng_state_matters_for_exact_growth_continuation": rng_matters,
        "signal_cursor_matters_at_fixed_horizon": cursor_matters,
        "birth_times_change_growth_continuation": birth_growth_causal,
        "birth_time_interpretation": (
            "causal continuation variable"
            if birth_growth_causal
            else "historical metadata under Digital Crystal v1 growth rule"
        ),
        "minimum_sufficient_state_identified": False,
        "counterfactual_branching_produces_divergence": illustrative_branch_real,
        "environmental_divergence_exceeds_stochastic_null_descriptively": (
            env_divergence_exceeds_null
        ),
        "branch_null_comparison": branch_comparison,
        "event_log_scope": (
            "reconstructs morphology/birth trajectory; does not reconstruct "
            "historical RNG state from additions alone"
        ),
        "explicit_nonclaims": [
            "minimum state",
            "learning",
            "adaptation",
            "agency",
            "selfhood",
            "understanding",
            "biological memory",
            "environmental divergence beyond stochastic null unless supported",
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

```json
{json.dumps(result, indent=2)}
```

Key interpretation:

- **state** is operationally sufficient information for faithful continuation;
- **history** here is an explicit record sufficient to reconstruct the morphology
  trajectory;
- the experiment identifies some necessary continuation variables but does not
  prove a mathematically minimal state representation;
- a saved checkpoint is an executable counterfactual branch point;
- whether changed future forcing causes *more* divergence than ordinary
  stochastic variation is assessed separately against the stochastic null.
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

    reproducibility_invariant = run_reproducibility_invariant_check(
        reporter,
        spec,
        checkpoint,
        reference.signal,
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
        reporter, spec, checkpoint, image_dir, profile["branch_null_reps"]
    )

    stage7 = run_stage_7(
        reporter, stage2, stage3, stage4, stage5, stage6
    )

    metadata["finished_at_unix"] = time.time()
    metadata["final_verdict"] = stage7["verdict"]
    metadata["replicate_restore_all_exact"] = replicate_result["all_exact"]
    metadata["canonical_rng_traversal"] = "sorted(frontier)"
    metadata["reproducibility_invariant_passed"] = (
        reproducibility_invariant["passed"]
    )

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
