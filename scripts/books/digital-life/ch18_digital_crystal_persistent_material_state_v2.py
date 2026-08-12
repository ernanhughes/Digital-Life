from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt

from tqdm import tqdm


# ============================================================================
# Chapter 18 — Can Experience Change the Material?
# ============================================================================

BASE_MODEL_VERSION = "digital-crystal-v1-frozen"
EXPERIMENT_VERSION = "digital-crystal-persistent-material-state-v2"
SCHEMA_VERSION = 2

Cell = Tuple[int, int]

HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)


# ============================================================================
# Frozen Digital Crystal v1 parameters
# ============================================================================

@dataclass(frozen=True)
class CrystalParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22


# ============================================================================
# Chapter 18 experimental material-state extension
# ============================================================================

@dataclass(frozen=True)
class MaterialParams:
    """
    Minimal experimental extension.

    A cell is either:
        occupied-normal
        occupied-modified

    Modification:
        - can be written only by an explicit pulse;
        - is local to already-occupied boundary cells;
        - persists irreversibly in this first experiment;
        - changes later growth only through modified neighbours.

    No history list, last-signal register, decoder, target morphology,
    learned parameter, or global memory variable is introduced.
    """
    write_probability: float = 0.20
    modified_neighbor_gain: float = 0.30


@dataclass
class CrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    step: int
    rng_state: object
    attachments_by_step: List[int]
    population_by_step: List[int]


@dataclass
class MaterialCrystalState:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    modified: Set[Cell]
    step: int
    stream_seed: int
    attachments_by_step: List[int]
    population_by_step: List[int]
    modified_count_by_step: List[int]


# ============================================================================
# Geometry and frozen growth mechanics
# ============================================================================

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


def logistic_scalar(x: float) -> float:
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


def hex_disk_capacity(radius: int) -> int:
    return 1 + 3 * radius * (radius + 1)


def capacity_fraction_occupied(occupied: Set[Cell], radius: int) -> float:
    return len(occupied) / float(hex_disk_capacity(radius))


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

    drift = 0.18 * normalize_signal(
        np.cumsum(rng.normal(0.0, 0.10, size=steps))
    )
    noise = rng.normal(0.0, 0.08, size=steps)

    return normalize_signal(deterministic + drift + noise)


# ============================================================================
# Frozen canonical sequential-RNG implementation
# ============================================================================

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


def advance_one_step(
    state: CrystalState,
    input_value: float,
    max_radius: int,
    params: CrystalParams,
) -> Tuple[CrystalState, int]:
    """
    Frozen Digital Crystal v1 implementation.
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

        if rng.random() < logistic_scalar(score):
            additions.append(cell)

    next_step = state.step + 1
    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    return CrystalState(
        occupied=occupied,
        birth_time=birth_time,
        step=next_step,
        rng_state=rng.getstate(),
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
    ), len(additions)


# ============================================================================
# Cell-keyed CRN runner retained from Chapter 17
# ============================================================================

def cell_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Stable U[0,1) draw keyed by (seed, absolute step, cell).

    This is the Chapter 17 counterfactual coupling. It keeps corresponding
    cell-step opportunities aligned across branches.
    """
    q, r = cell
    payload = f"{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def material_uniform(stream_seed: int, step: int, cell: Cell) -> float:
    """
    Separate deterministic random channel for material-state writing.

    The 'material:' namespace prevents the material write decision from
    consuming or correlating with the frozen CRN growth draw.
    """
    q, r = cell
    payload = (
        f"material:{int(stream_seed)}:{int(step)}:{int(q)}:{int(r)}"
    ).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64)


def initial_material_state(stream_seed: int) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        modified=set(),
        step=0,
        stream_seed=int(stream_seed),
        attachments_by_step=[1],
        population_by_step=[1],
        modified_count_by_step=[0],
    )


def clone_material_state(state: MaterialCrystalState) -> MaterialCrystalState:
    return MaterialCrystalState(
        occupied=set(state.occupied),
        birth_time=dict(state.birth_time),
        modified=set(state.modified),
        step=int(state.step),
        stream_seed=int(state.stream_seed),
        attachments_by_step=list(state.attachments_by_step),
        population_by_step=list(state.population_by_step),
        modified_count_by_step=list(state.modified_count_by_step),
    )


def erase_material_labels(state: MaterialCrystalState) -> MaterialCrystalState:
    """
    Causal ablation: preserve visible morphology, birth times, step, stream seed,
    and execution history while deleting only the experimental material state.
    """
    out = clone_material_state(state)
    out.modified = set()
    out.modified_count_by_step = list(out.modified_count_by_step)
    if out.modified_count_by_step:
        out.modified_count_by_step[-1] = 0
    return out


def advance_one_step_material(
    state: MaterialCrystalState,
    input_value: float,
    pulse_bit: int,
    max_radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> Tuple[MaterialCrystalState, int, int]:
    """
    Chapter 18 material-state growth step.

    Ordering is deliberate:

      1. growth decisions use the material state that existed BEFORE this step;
      2. new cells are attached;
      3. if pulse_bit == 1, already-occupied boundary material may be modified;
      4. newly written state can affect growth only on later steps.

    This prevents the write event from affecting growth in the same update.
    """
    occupied = set(state.occupied)
    birth_time = dict(state.birth_time)
    modified = set(state.modified)

    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions: List[Cell] = []
    next_step = state.step + 1

    for cell in sorted(frontier):
        n = sum(nb in occupied for nb in neighbors(cell))
        modified_n = sum(nb in modified for nb in neighbors(cell))

        theta = local_exposure_angle(cell, occupied)
        phase = crystal_params.signal_phase_gain * float(input_value)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)

        score = (
            crystal_params.base_bias
            + crystal_params.neighbor_gain * n
            + crystal_params.signal_rate_gain * float(input_value)
            + crystal_params.anisotropy_gain * anisotropy
            - crystal_params.crowding_penalty * crowding
            + material_params.modified_neighbor_gain * modified_n
        )

        if cell_uniform(state.stream_seed, next_step, cell) < logistic_scalar(score):
            additions.append(cell)

    for cell in additions:
        occupied.add(cell)
        birth_time[cell] = next_step

    newly_modified = 0

    if int(pulse_bit) != 0:
        # Write only to occupied boundary cells. This is a local material event.
        candidates: List[Cell] = []
        for cell in sorted(occupied):
            degree = sum(nb in occupied for nb in neighbors(cell))
            if degree < 6:
                candidates.append(cell)

        for cell in candidates:
            if cell in modified:
                continue
            if (
                material_uniform(state.stream_seed, next_step, cell)
                < material_params.write_probability
            ):
                modified.add(cell)
                newly_modified += 1

    out = MaterialCrystalState(
        occupied=occupied,
        birth_time=birth_time,
        modified=modified,
        step=next_step,
        stream_seed=state.stream_seed,
        attachments_by_step=state.attachments_by_step + [len(additions)],
        population_by_step=state.population_by_step + [len(occupied)],
        modified_count_by_step=state.modified_count_by_step + [len(modified)],
    )
    return out, len(additions), newly_modified


def warm_material_checkpoint(
    env: np.ndarray,
    warmup_steps: int,
    stream_seed: int,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
) -> MaterialCrystalState:
    state = initial_material_state(stream_seed)

    for t in range(warmup_steps):
        state, _, _ = advance_one_step_material(
            state=state,
            input_value=float(env[t]),
            pulse_bit=0,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )

    return state


def advance_material_sequence(
    checkpoint: MaterialCrystalState,
    env_future: np.ndarray,
    pulse_bits: Sequence[int],
    message_gain: float,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    observation_steps: Sequence[int],
    guard: float,
) -> Dict[int, MaterialCrystalState]:
    state = clone_material_state(checkpoint)
    wanted = set(map(int, observation_steps))
    observations: Dict[int, MaterialCrystalState] = {}

    for i in range(max(wanted)):
        bit = int(pulse_bits[i]) if i < len(pulse_bits) else 0
        forcing = float(env_future[i]) + message_gain * bit

        state, _, _ = advance_one_step_material(
            state=state,
            input_value=forcing,
            pulse_bit=bit,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )

        frac = capacity_fraction_occupied(state.occupied, radius)
        if frac >= guard:
            raise RuntimeError(
                f"Saturation guard reached at elapsed step {i + 1}: "
                f"{frac:.3f} >= {guard:.3f}"
            )

        elapsed = i + 1
        if elapsed in wanted:
            observations[elapsed] = clone_material_state(state)

    return observations


# ============================================================================
# Measurement model
# ============================================================================

FEATURE_NAMES = [
    "population_fraction",
    "max_radius_fraction",
    "mean_radius_fraction",
    "std_radius_fraction",
    "centroid_x_scaled",
    "centroid_y_scaled",
    "cov_trace_scaled",
    "cov_anisotropy",
    "boundary_fraction",
    "mean_degree",
    "degree_1",
    "degree_2",
    "degree_3",
    "degree_4",
    "degree_5",
    "degree_6",
    "sector_0",
    "sector_1",
    "sector_2",
    "sector_3",
    "sector_4",
    "sector_5",
    "harmonic6_cos",
    "harmonic6_sin",
]


def morphology_features_from_occupied(
    occupied: Set[Cell],
    radius: int,
) -> np.ndarray:
    occ = occupied
    xy = np.asarray([axial_to_xy(c) for c in occ], dtype=float)
    rs = np.asarray([hex_distance(c) for c in occ], dtype=float)

    centroid = np.mean(xy, axis=0)
    centered = xy - centroid

    if len(xy) >= 2:
        cov = np.cov(centered.T, bias=True)
        eig = np.sort(np.maximum(np.linalg.eigvalsh(cov), 0.0))
        cov_trace = float(np.sum(eig))
        cov_aniso = float(
            (eig[-1] - eig[0]) / max(1e-12, eig[-1] + eig[0])
        )
    else:
        cov_trace = 0.0
        cov_aniso = 0.0

    degrees = np.asarray(
        [sum(nb in occ for nb in neighbors(c)) for c in occ],
        dtype=int,
    )
    boundary_fraction = float(np.mean(degrees < 6))
    degree_fracs = [float(np.mean(degrees == k)) for k in range(1, 7)]

    angles = np.arctan2(xy[:, 1], xy[:, 0])
    sector_idx = ((angles + np.pi) / (2 * np.pi) * 6).astype(int) % 6
    sectors = [float(np.mean(sector_idx == k)) for k in range(6)]
    harmonic6 = np.mean(np.exp(1j * 6.0 * angles))

    scale_xy = max(1.0, 1.5 * radius)
    scale_cov = max(1.0, scale_xy * scale_xy)

    return np.asarray([
        len(occ) / float(hex_disk_capacity(radius)),
        float(np.max(rs)) / max(1.0, radius),
        float(np.mean(rs)) / max(1.0, radius),
        float(np.std(rs)) / max(1.0, radius),
        float(centroid[0]) / scale_xy,
        float(centroid[1]) / scale_xy,
        cov_trace / scale_cov,
        cov_aniso,
        boundary_fraction,
        float(np.mean(degrees)),
        *degree_fracs,
        *sectors,
        float(np.real(harmonic6)),
        float(np.imag(harmonic6)),
    ], dtype=float)


def normalized_symmetric_difference(a: Set[Cell], b: Set[Cell]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a ^ b) / float(len(union))


def pooled_feature_scale(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    pooled = np.vstack([X, Y])
    sd = np.std(pooled, axis=0)
    return np.where(sd < 1e-12, 1.0, sd)


def paired_standardized_deltas(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    if X.shape != Y.shape:
        raise ValueError("Paired statistics require equal shapes.")
    return (X - Y) / pooled_feature_scale(X, Y)


def stat_paired_ridge_hotelling(
    X: np.ndarray,
    Y: np.ndarray,
    ridge_fraction: float = 0.25,
) -> float:
    D = paired_standardized_deltas(X, Y)
    mean = np.mean(D, axis=0)

    if len(D) <= 1:
        return float(mean @ mean)

    cov = np.cov(D, rowvar=False, bias=True)
    diag_scale = float(np.mean(np.diag(cov)))
    ridge = max(1e-8, ridge_fraction * max(diag_scale, 1e-8))
    reg = cov + ridge * np.eye(cov.shape[0])
    inv = np.linalg.pinv(reg)

    return float(mean @ inv @ mean)


def paired_ridge_test(
    X: np.ndarray,
    Y: np.ndarray,
    permutations: int,
    seed: int,
) -> dict:
    if X.shape != Y.shape:
        raise ValueError("Paired test requires equal paired shapes.")

    observed = stat_paired_ridge_hotelling(X, Y)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for i in range(permutations):
        swap = rng.integers(0, 2, size=len(X)).astype(bool)
        Xp = X.copy()
        Yp = Y.copy()
        Xp[swap], Yp[swap] = Y[swap], X[swap]
        null[i] = stat_paired_ridge_hotelling(Xp, Yp)

    p = (1 + float(np.sum(null >= observed))) / (permutations + 1)

    return {
        "statistic": float(observed),
        "p_value": float(p),
        "permutations": int(permutations),
        "null_mean": float(np.mean(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
    }


def bootstrap_mean_ci(
    values: Sequence[float],
    reps: int,
    seed: int,
) -> dict:
    x = np.asarray(values, dtype=float)

    if len(x) == 0:
        return {"n": 0}

    rng = np.random.default_rng(seed)
    means = np.empty(reps, dtype=float)

    for i in range(reps):
        sample = x[rng.integers(0, len(x), size=len(x))]
        means[i] = np.mean(sample)

    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "std": float(np.std(x)),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def response_delta(
    pulse_state: MaterialCrystalState,
    no_pulse_state: MaterialCrystalState,
    radius: int,
) -> np.ndarray:
    return (
        morphology_features_from_occupied(pulse_state.occupied, radius)
        - morphology_features_from_occupied(no_pulse_state.occupied, radius)
    )


def frontier_cells(occupied: Set[Cell], radius: int) -> Set[Cell]:
    frontier: Set[Cell] = set()
    for cell in occupied:
        for nb in neighbors(cell):
            if nb not in occupied and hex_distance(nb) <= radius:
                frontier.add(nb)
    return frontier


def material_accessibility_metrics(
    state: MaterialCrystalState,
    radius: int,
) -> dict:
    """
    Measure whether persistent modified material remains reachable by the active
    growth frontier.

    Persistent state is dynamically accessible only if current frontier cells
    have at least one modified occupied neighbour.
    """
    frontier = frontier_cells(state.occupied, radius)

    modified_boundary = []
    for cell in state.modified:
        degree = sum(nb in state.occupied for nb in neighbors(cell))
        if degree < 6:
            modified_boundary.append(cell)

    exposed_frontier = []
    modified_neighbor_counts = []

    for cell in frontier:
        m = sum(nb in state.modified for nb in neighbors(cell))
        if m > 0:
            exposed_frontier.append(cell)
            modified_neighbor_counts.append(m)

    frontier_n = len(frontier)
    exposed_n = len(exposed_frontier)

    return {
        "modified_count": int(len(state.modified)),
        "modified_boundary_count": int(len(modified_boundary)),
        "frontier_count": int(frontier_n),
        "frontier_cells_with_modified_neighbor": int(exposed_n),
        "frontier_exposed_fraction": (
            float(exposed_n / frontier_n) if frontier_n else 0.0
        ),
        "mean_modified_neighbors_among_exposed_frontier": (
            float(np.mean(modified_neighbor_counts))
            if modified_neighbor_counts
            else 0.0
        ),
        "max_modified_neighbors_on_frontier": (
            int(max(modified_neighbor_counts))
            if modified_neighbor_counts
            else 0
        ),
    }


def continue_material_no_pulse(
    checkpoint: MaterialCrystalState,
    env_future: np.ndarray,
    steps: int,
    radius: int,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    guard: float,
) -> MaterialCrystalState:
    state = clone_material_state(checkpoint)
    for i in range(steps):
        state, _, _ = advance_one_step_material(
            state=state,
            input_value=float(env_future[i]),
            pulse_bit=0,
            max_radius=radius,
            crystal_params=crystal_params,
            material_params=material_params,
        )
        frac = capacity_fraction_occupied(state.occupied, radius)
        if frac >= guard:
            raise RuntimeError(
                f"Saturation guard reached during no-pulse continuation at "
                f"step {i+1}: {frac:.3f} >= {guard:.3f}"
            )
    return state


# ============================================================================
# Experiment profiles
# ============================================================================

PROFILES = {
    "quick": {
        "groups": 32,
        "radius": 64,
        "warmup_steps": 14,

        # Experience/write phase.
        "experience_horizon": 8,
        "experience_pulse_step": 3,

        # Observe accessibility from the pulse onward.
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 9, 10, 12, 14],

        # Probe causal accessibility before, near, and after burial.
        "ablation_probe_steps": [5, 7, 10, 14],
        "ablation_followup_horizon": 3,
        "ablation_primary_endpoint": 3,

        # Retained for direct comparability to v1.
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,

        "permutations": 1000,
        "bootstrap_reps": 1000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "standard": {
        "groups": 64,
        "radius": 64,
        "warmup_steps": 14,
        "experience_horizon": 8,
        "experience_pulse_step": 3,
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 9, 10, 12, 14],
        "ablation_probe_steps": [5, 7, 10, 14],
        "ablation_followup_horizon": 3,
        "ablation_primary_endpoint": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "permutations": 3000,
        "bootstrap_reps": 2000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
    "full": {
        "groups": 128,
        "radius": 64,
        "warmup_steps": 14,
        "experience_horizon": 8,
        "experience_pulse_step": 3,
        "accessibility_observation_steps": [4, 5, 6, 7, 8, 9, 10, 12, 14],
        "ablation_probe_steps": [5, 7, 10, 14],
        "ablation_followup_horizon": 3,
        "ablation_primary_endpoint": 3,
        "message_gain": 0.65,
        "write_probability": 0.20,
        "modified_neighbor_gain": 0.30,
        "permutations": 5000,
        "bootstrap_reps": 4000,
        "alpha": 0.05,
        "max_capacity_fraction": 0.85,
    },
}


# ============================================================================
# Reporter
# ============================================================================

class Reporter:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.sections: List[str] = []

    def json(self, name: str, payload):
        (self.root / name).write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    def stage(self, filename: str, title: str, body: str):
        text = f"# {title}\n\n{body.strip()}\n"
        (self.root / filename).write_text(text, encoding="utf-8")
        self.sections.append(text)

    def full_report(self, metadata: dict) -> Path:
        path = self.root / "ch18-persistent-material-state-v2-full-report.md"
        header = (
            "# Chapter 18 — Can Experience Change the Material? (V2 Autopsy)\n\n"
            "## Run metadata\n\n```json\n"
            + json.dumps(metadata, indent=2)
            + "\n```\n\n"
        )
        path.write_text(
            header + "\n\n".join(self.sections),
            encoding="utf-8",
        )
        return path


# ============================================================================
# Stage 0 — extension audit
# ============================================================================

def stage_0_extension_audit(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
) -> dict:
    """
    Verify the extension does not alter growth while material state is empty.

    The CRN material runner with pulse_bit=0 and zero modified cells must match
    a direct CRN implementation of the frozen growth law exactly.
    """
    radius = profile["radius"]
    steps = profile["warmup_steps"] + 8
    env = make_environment(steps, seed + 1)

    # Direct frozen-CRN state represented using MaterialCrystalState, but with
    # modified-neighbour gain set to zero and no write channel.
    base_params = MaterialParams(
        write_probability=0.0,
        modified_neighbor_gain=0.0,
    )

    a = initial_material_state(seed + 2)
    b = initial_material_state(seed + 2)

    for t in range(steps):
        a, _, _ = advance_one_step_material(
            a, float(env[t]), 0, radius,
            crystal_params, material_params,
        )
        b, _, _ = advance_one_step_material(
            b, float(env[t]), 0, radius,
            crystal_params, base_params,
        )

    exact_when_unmodified = (
        a.occupied == b.occupied
        and a.birth_time == b.birth_time
        and a.modified == set()
        and b.modified == set()
        and a.attachments_by_step == b.attachments_by_step
    )

    # Re-run exact reproducibility for the full material extension.
    c = initial_material_state(seed + 3)
    d = initial_material_state(seed + 3)
    pulse_step = profile["experience_pulse_step"]

    for t in range(steps):
        bit = int(t == pulse_step)
        forcing = float(env[t]) + profile["message_gain"] * bit
        c, _, _ = advance_one_step_material(
            c, forcing, bit, radius,
            crystal_params, material_params,
        )
        d, _, _ = advance_one_step_material(
            d, forcing, bit, radius,
            crystal_params, material_params,
        )

    material_exact_reproducibility = (
        c.occupied == d.occupied
        and c.modified == d.modified
        and c.birth_time == d.birth_time
        and c.attachments_by_step == d.attachments_by_step
    )

    if not exact_when_unmodified:
        raise RuntimeError(
            "Stage 0 failed: material extension changes growth while material "
            "state is empty."
        )
    if not material_exact_reproducibility:
        raise RuntimeError(
            "Stage 0 failed: material extension is not exactly reproducible."
        )

    result = {
        "role": "EXTENSION AUDIT",
        "base_model_version": BASE_MODEL_VERSION,
        "experimental_extension": EXPERIMENT_VERSION,
        "canonical_model_modified": False,
        "exact_when_material_state_empty": exact_when_unmodified,
        "material_extension_exact_reproducibility": (
            material_exact_reproducibility
        ),
        "write_probability": material_params.write_probability,
        "modified_neighbor_gain": material_params.modified_neighbor_gain,
        "interpretation": (
            "The material-state extension leaves the Chapter 17 CRN growth "
            "process unchanged while no cells are modified. The extension becomes "
            "causally active only after experience writes local material state."
        ),
    }

    reporter.json("stage-00-extension-audit.json", result)
    reporter.stage(
        "stage-00-extension-audit.md",
        "Stage 0 — Extension Audit",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


# ============================================================================
# Shared construction of experienced / erased / naive checkpoints
# ============================================================================

def build_experience_checkpoints(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
) -> dict:
    """
    Construct three related states.

    experienced_retained:
        received first pulse and keeps material labels.

    experienced_erased:
        exact same visible morphology as experienced_retained, but material
        labels are deleted at the retention checkpoint.

    naive:
        received no first pulse and therefore has no experience-written labels.
        Its morphology is allowed to differ and is secondary/descriptive only.
    """
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    exp_horizon = profile["experience_horizon"]
    retention = profile["retention_delay"]

    total = warmup + exp_horizon + retention + max(
        profile["ablation_horizon"],
        profile["challenge_horizon"],
    ) + 2

    gseed = seed + 100_000 + group_index * 1009
    env = make_environment(total, gseed + 1)

    cp = warm_material_checkpoint(
        env=env,
        warmup_steps=warmup,
        stream_seed=gseed + 2,
        radius=radius,
        crystal_params=crystal_params,
        material_params=material_params,
    )

    future = env[warmup:]
    exp_bits = [0] * (exp_horizon + retention)
    exp_bits[profile["experience_pulse_step"]] = 1
    naive_bits = [0] * (exp_horizon + retention)

    end_step = exp_horizon + retention

    exp_obs = advance_material_sequence(
        checkpoint=cp,
        env_future=future,
        pulse_bits=exp_bits,
        message_gain=profile["message_gain"],
        radius=radius,
        crystal_params=crystal_params,
        material_params=material_params,
        observation_steps=[end_step],
        guard=profile["max_capacity_fraction"],
    )

    naive_obs = advance_material_sequence(
        checkpoint=cp,
        env_future=future,
        pulse_bits=naive_bits,
        message_gain=profile["message_gain"],
        radius=radius,
        crystal_params=crystal_params,
        material_params=material_params,
        observation_steps=[end_step],
        guard=profile["max_capacity_fraction"],
    )

    experienced_retained = exp_obs[end_step]
    experienced_erased = erase_material_labels(experienced_retained)
    naive = naive_obs[end_step]

    env_after_retention = future[end_step:]

    return {
        "experienced_retained": experienced_retained,
        "experienced_erased": experienced_erased,
        "naive": naive,
        "env_after_retention": env_after_retention,
        "gseed": gseed,
    }


# ============================================================================
# Stage 1 — can experience write persistent local state?
# ============================================================================

def stage_1_write_and_accessibility(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    image_dir: Path,
) -> dict:
    """
    Reproduce material writing and measure whether the written state remains in
    contact with the active growth frontier.

    This stage is the v2 autopsy of the v1 exact-zero retained-vs-erased result.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    pulse_step = profile["experience_pulse_step"]
    observations = sorted(set(profile["accessibility_observation_steps"]))

    max_elapsed = max(observations)
    total = warmup + max_elapsed + 2

    metrics_by_t = {
        t: {
            "modified_count": [],
            "modified_boundary_count": [],
            "frontier_count": [],
            "frontier_cells_with_modified_neighbor": [],
            "frontier_exposed_fraction": [],
            "mean_modified_neighbors_among_exposed_frontier": [],
            "max_modified_neighbors_on_frontier": [],
        }
        for t in observations
    }

    write_counts = []
    accessibility_loss_step = []

    for g in tqdm(range(groups), desc="Stage 1 material accessibility audit"):
        gseed = seed + 200_000 + g * 1013
        env = make_environment(total, gseed + 1)

        state = warm_material_checkpoint(
            env, warmup, gseed + 2, radius,
            crystal_params, material_params,
        )
        future = env[warmup:]

        first_zero_after_write = None

        for i in range(max_elapsed):
            bit = int(i == pulse_step)
            forcing = float(future[i]) + profile["message_gain"] * bit

            state, _, _ = advance_one_step_material(
                state, forcing, bit, radius,
                crystal_params, material_params,
            )
            elapsed = i + 1

            if i == pulse_step:
                write_counts.append(len(state.modified))

            if elapsed in observations:
                m = material_accessibility_metrics(state, radius)
                for key, value in m.items():
                    metrics_by_t[elapsed][key].append(value)

            if i >= pulse_step:
                m_now = material_accessibility_metrics(state, radius)
                if (
                    first_zero_after_write is None
                    and m_now["frontier_cells_with_modified_neighbor"] == 0
                ):
                    first_zero_after_write = elapsed

        accessibility_loss_step.append(
            first_zero_after_write if first_zero_after_write is not None else max_elapsed + 1
        )

    summary = {}
    for t in observations:
        summary[str(t)] = {
            key: bootstrap_mean_ci(
                vals,
                profile["bootstrap_reps"],
                seed + 210_000 + t * 100 + j,
            )
            for j, (key, vals) in enumerate(metrics_by_t[t].items())
        }

    result = {
        "groups": groups,
        "experience_pulse_zero_index": pulse_step,
        "experience_pulse_elapsed_step": pulse_step + 1,
        "observation_steps": observations,
        "modified_cells_immediately_after_write": bootstrap_mean_ci(
            write_counts,
            profile["bootstrap_reps"],
            seed + 211_000,
        ),
        "first_step_with_zero_frontier_contact": bootstrap_mean_ci(
            accessibility_loss_step,
            profile["bootstrap_reps"],
            seed + 212_000,
        ),
        "summary": summary,
        "status": "MEASURED",
        "bounded_statement": (
            "V2 directly measures whether experience-written material remains "
            "adjacent to current growth opportunities. Persistent labels are not "
            "treated as causally accessible once no frontier cell has a modified "
            "occupied neighbour."
        ),
    }

    reporter.json("stage-01-material-accessibility.json", result)
    reporter.stage(
        "stage-01-material-accessibility.md",
        "Stage 1 — Does Persistent Material Remain Reachable?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )

    xs = observations
    ys = [
        summary[str(t)]["frontier_exposed_fraction"]["mean"]
        for t in xs
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(xs, ys, marker="o")
    ax.axvline(pulse_step + 1, linestyle="--", linewidth=1)
    ax.set_xlabel("Elapsed step after warm checkpoint")
    ax.set_ylabel("Mean frontier fraction exposed to modified material")
    ax.set_title("Causal accessibility of experience-written material")
    fig.tight_layout()
    image_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        image_dir / "ch18-v2-01-material-accessibility.png",
        dpi=160,
    )
    plt.close(fig)

    return result


def build_experienced_checkpoint_at_elapsed(
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
    group_index: int,
    elapsed_step: int,
) -> Tuple[MaterialCrystalState, np.ndarray]:
    """
    Build one experienced state exactly at the requested elapsed step after the
    warm checkpoint, then return the untouched future environment.
    """
    radius = profile["radius"]
    warmup = profile["warmup_steps"]
    pulse_step = profile["experience_pulse_step"]

    total = (
        warmup
        + elapsed_step
        + profile["ablation_followup_horizon"]
        + 3
    )

    gseed = seed + 300_000 + group_index * 1019
    env = make_environment(total, gseed + 1)

    state = warm_material_checkpoint(
        env, warmup, gseed + 2, radius,
        crystal_params, material_params,
    )

    future = env[warmup:]

    for i in range(elapsed_step):
        bit = int(i == pulse_step)
        forcing = float(future[i]) + profile["message_gain"] * bit
        state, _, _ = advance_one_step_material(
            state, forcing, bit, radius,
            crystal_params, material_params,
        )

    return state, future[elapsed_step:]


def stage_2_timed_erase_ablation(
    reporter: Reporter,
    profile: dict,
    crystal_params: CrystalParams,
    material_params: MaterialParams,
    seed: int,
) -> dict:
    """
    Perform the same retained-vs-erased causal ablation at multiple times.

    The prediction generated by the v1 autopsy is specific:
        causal effect should be possible while modified material contacts the
        growth frontier, and should disappear when contact vanishes.

    This stage measures that relation rather than merely rerunning a late erase.
    """
    groups = profile["groups"]
    radius = profile["radius"]
    probes = profile["ablation_probe_steps"]
    followup = profile["ablation_followup_horizon"]
    endpoint = profile["ablation_primary_endpoint"]

    by_probe = {}

    for probe in probes:
        retained_features = []
        erased_features = []
        symdiff = []
        contact_counts = []
        contact_fractions = []

        for g in tqdm(
            range(groups),
            desc=f"Stage 2 erase probe t={probe}",
        ):
            retained, future = build_experienced_checkpoint_at_elapsed(
                profile, crystal_params, material_params,
                seed + probe * 10_000, g, probe,
            )
            erased = erase_material_labels(retained)

            if retained.occupied != erased.occupied:
                raise RuntimeError(
                    "Erase ablation changed visible morphology."
                )

            access = material_accessibility_metrics(retained, radius)
            contact_counts.append(
                access["frontier_cells_with_modified_neighbor"]
            )
            contact_fractions.append(
                access["frontier_exposed_fraction"]
            )

            A = continue_material_no_pulse(
                retained, future, followup,
                radius, crystal_params, material_params,
                profile["max_capacity_fraction"],
            )
            B = continue_material_no_pulse(
                erased, future, followup,
                radius, crystal_params, material_params,
                profile["max_capacity_fraction"],
            )

            retained_features.append(
                morphology_features_from_occupied(A.occupied, radius)
            )
            erased_features.append(
                morphology_features_from_occupied(B.occupied, radius)
            )
            symdiff.append(
                normalized_symmetric_difference(
                    A.occupied, B.occupied
                )
            )

        X = np.asarray(retained_features, dtype=float)
        Y = np.asarray(erased_features, dtype=float)

        test = paired_ridge_test(
            X, Y,
            permutations=profile["permutations"],
            seed=seed + 320_000 + probe,
        )

        by_probe[str(probe)] = {
            "probe_elapsed_step": probe,
            "followup_steps": followup,
            "frontier_contact_count": bootstrap_mean_ci(
                contact_counts,
                profile["bootstrap_reps"],
                seed + 321_000 + probe,
            ),
            "frontier_exposed_fraction": bootstrap_mean_ci(
                contact_fractions,
                profile["bootstrap_reps"],
                seed + 322_000 + probe,
            ),
            "pathwise_symmetric_difference_after_followup": bootstrap_mean_ci(
                symdiff,
                profile["bootstrap_reps"],
                seed + 323_000 + probe,
            ),
            "paired_ridge_test": test,
            "causal_effect_detected": bool(
                test["p_value"] < profile["alpha"]
            ),
        }

    result = {
        "groups": groups,
        "probe_steps": probes,
        "followup_horizon": followup,
        "alpha": profile["alpha"],
        "results": by_probe,
        "status": "MEASURED",
        "bounded_statement": (
            "The erase ablation is evaluated before, near, and after loss of "
            "frontier contact. This tests whether causal efficacy tracks "
            "accessibility of the persistent material state."
        ),
    }

    reporter.json("stage-02-timed-erase-ablation.json", result)
    reporter.stage(
        "stage-02-timed-erase-ablation.md",
        "Stage 2 — When Does Persistent State Stop Mattering?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_3_accessibility_causality_relation(
    reporter: Reporter,
    profile: dict,
    stage1: dict,
    stage2: dict,
) -> dict:
    """
    Synthesize the autopsy without introducing a new mechanism.

    We do not claim burial merely because a late effect is zero. The autopsy
    asks whether the observed frontier-contact curve and timed ablations are
    directionally consistent with the accessibility hypothesis.
    """
    probes = profile["ablation_probe_steps"]

    rows = []
    for probe in probes:
        r = stage2["results"][str(probe)]
        rows.append({
            "probe": probe,
            "mean_frontier_contact_count": (
                r["frontier_contact_count"]["mean"]
            ),
            "mean_frontier_exposed_fraction": (
                r["frontier_exposed_fraction"]["mean"]
            ),
            "mean_post_ablation_symdiff": (
                r["pathwise_symmetric_difference_after_followup"]["mean"]
            ),
            "ablation_p_value": r["paired_ridge_test"]["p_value"],
            "causal_effect_detected": r["causal_effect_detected"],
        })

    contact_present = [
        row for row in rows
        if row["mean_frontier_contact_count"] > 0
    ]
    contact_absent = [
        row for row in rows
        if row["mean_frontier_contact_count"] == 0
    ]

    positive_while_contact = any(
        row["causal_effect_detected"]
        for row in contact_present
    )
    zero_effect_after_loss = all(
        not row["causal_effect_detected"]
        for row in contact_absent
    ) if contact_absent else False

    if positive_while_contact and zero_effect_after_loss:
        status = "SUPPORTED"
        bounded = (
            "Timed ablations are consistent with the hypothesis that persistent "
            "material state matters only while it remains causally accessible "
            "to the active growth frontier."
        )
    elif contact_absent and zero_effect_after_loss:
        status = "PROVISIONAL"
        bounded = (
            "Frontier contact disappears and late erase ablations remain null, "
            "which is consistent with causal inaccessibility after burial, but "
            "an earlier positive ablation was not established."
        )
    else:
        status = "UNTESTED"
        bounded = (
            "The v2 autopsy did not produce the predicted relation between "
            "frontier contact and causal effect strongly enough to support the "
            "burial/accessibility mechanism."
        )

    result = {
        "hypothesis": (
            "Persistent labels become causally inert when growth moves beyond "
            "them and current frontier cells no longer contact modified material."
        ),
        "probe_summary": rows,
        "positive_ablation_while_contact_present": positive_while_contact,
        "all_tested_post_contact_ablation_effects_absent": zero_effect_after_loss,
        "status": status,
        "bounded_statement": bounded,
    }

    reporter.json("stage-03-accessibility-causality-relation.json", result)
    reporter.stage(
        "stage-03-accessibility-causality-relation.md",
        "Stage 3 — Does Causal Effect Track Frontier Accessibility?",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result


def stage_4_verdict(
    reporter: Reporter,
    stage0: dict,
    stage1: dict,
    stage2: dict,
    stage3: dict,
) -> dict:
    if not (
        stage0["exact_when_material_state_empty"]
        and stage0["material_extension_exact_reproducibility"]
    ):
        final_status = "UNTESTED"
        next_question = (
            "Fix extension validity before interpreting the autopsy."
        )
    elif stage3["status"] == "SUPPORTED":
        final_status = "SUPPORTED"
        next_question = (
            "Design, but do not yet assume, the smallest local mechanism that "
            "keeps experience-written material in causal contact with the active "
            "growth surface."
        )
    elif stage3["status"] == "PROVISIONAL":
        final_status = "PROVISIONAL"
        next_question = (
            "Increase resolution around the contact-loss transition before "
            "introducing inheritance or propagation of material state."
        )
    else:
        final_status = "UNTESTED"
        next_question = (
            "The burial/accessibility explanation was not established. Do not "
            "add inheritance yet; inspect how and where modified material can "
            "influence growth."
        )

    result = {
        "experiment_role": "EXPLORATORY MECHANISM AUTOPSY",
        "chapter": 18,
        "question": (
            "Why did persistent material state become causally inert?"
        ),
        "stage_1_accessibility_measured": stage1["status"],
        "stage_2_timed_ablation_measured": stage2["status"],
        "stage_3_accessibility_hypothesis": stage3["status"],
        "final_status": final_status,
        "bounded_claim": (
            "V2 does not add a new memory mechanism. It tests whether the v1 "
            "failure occurred because experience-written material persisted "
            "physically but lost causal access to the active growth frontier."
        ),
        "nonclaims": [
            "memory",
            "learning",
            "adaptation",
            "information storage",
            "inheritance",
            "epigenetics",
            "signalling",
            "semantics",
            "agency",
            "individuality",
            "reproduction",
            "life",
        ],
        "next_question": next_question,
    }

    reporter.json("stage-04-verdict.json", result)
    reporter.stage(
        "stage-04-verdict.md",
        "Stage 4 — Bounded Chapter 18 V2 Verdict",
        f"```json\n{json.dumps(result, indent=2)}\n```",
    )
    return result




# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--seed", type=int, default=20260815)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/ch18-persistent-material-state-v2"
        ),
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    args = parser.parse_args()

    profile = dict(PROFILES[args.profile])

    crystal_params = CrystalParams()
    material_params = MaterialParams(
        write_probability=profile["write_probability"],
        modified_neighbor_gain=profile["modified_neighbor_gain"],
    )

    args.report_dir.mkdir(parents=True, exist_ok=True)
    args.image_dir.mkdir(parents=True, exist_ok=True)

    reporter = Reporter(args.report_dir)

    metadata = {
        "base_model_version": BASE_MODEL_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": 18,
        "chapter_title": "Can Experience Change the Material?",
        "run_type": "EXPLORATORY MECHANISM AUTOPSY",
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "canonical_model_modified": False,
        "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
        "experimental_extension_unchanged_from_v1": True,
        "material_mechanism": {
            "write_probability": material_params.write_probability,
            "modified_neighbor_gain": material_params.modified_neighbor_gain,
            "persistence_rule": "modified remains modified",
            "causal_rule": (
                "modified occupied neighbours bias later frontier attachment"
            ),
        },
        "v1_result_being_autopsied": (
            "Persistent labels were written and retained, but retained-vs-erased "
            "continuations were exactly identical at the late ablation."
        ),
        "v2_hypothesis": (
            "Persistent material becomes causally inert when growth buries the "
            "modified cells and the active frontier no longer has modified "
            "occupied neighbours."
        ),
        "scientific_boundary": (
            "No new propagation, inheritance, memory, learning, or adaptation "
            "mechanism is introduced in v2."
        ),
        "started_at_unix": time.time(),
    }

    print("=" * 78)
    print("CHAPTER 18 V2 — WHY DID PERSISTENT STATE BECOME INERT?")
    print(
        f"profile={args.profile} "
        f"version={EXPERIMENT_VERSION} "
        f"groups={profile['groups']}"
    )
    print("=" * 78)

    s0 = stage_0_extension_audit(
        reporter, profile, crystal_params, material_params, args.seed
    )

    s1 = stage_1_write_and_accessibility(
        reporter, profile, crystal_params, material_params,
        args.seed, args.image_dir,
    )

    s2 = stage_2_timed_erase_ablation(
        reporter, profile, crystal_params, material_params, args.seed
    )

    s3 = stage_3_accessibility_causality_relation(
        reporter, profile, s1, s2
    )

    s4 = stage_4_verdict(
        reporter, s0, s1, s2, s3
    )

    metadata.update({
        "finished_at_unix": time.time(),
        "stage_1_status": s1["status"],
        "stage_2_status": s2["status"],
        "stage_3_status": s3["status"],
        "final_status": s4["final_status"],
        "next_question": s4["next_question"],
    })

    reporter.json("run-metadata.json", metadata)
    report_path = reporter.full_report(metadata)

    print("\n" + "=" * 78)
    print("CHAPTER 18 V2 COMPLETE")
    print(f"accessibility_measured={s1['status']}")
    print(f"timed_ablation_measured={s2['status']}")
    print(f"accessibility_hypothesis={s3['status']}")
    print(f"final_status={s4['final_status']}")
    print(f"report={report_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
