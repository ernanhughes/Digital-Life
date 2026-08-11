#!/usr/bin/env python3
"""
Digital Life Chapter 16 — Before There Are Messages, There Are Pulses
====================================================================

Purpose
-------
Test whether independently evolving Digital Crystals can become measurably
synchronized using only low-bandwidth one-bit local events.

This script continues from frozen Digital Crystal v1. It adds:
- a weak oscillator per crystal,
- one-bit pulse emission on phase wrap,
- global/local/shuffled coupling controls,
- delay/noise robustness,
- crystal-growth consequences,
- SQLite caching,
- staged Markdown/JSON reports,
- Matplotlib figures,
- final bounded verdict.

No learning, language, semantics, planning, cooperation, coordination,
intelligence, agency, or life is claimed.

Recommended:
    python ch16_digital_crystal_signalling.py --profile quick
    python ch16_digital_crystal_signalling.py --profile standard
    python ch16_digital_crystal_signalling.py --profile full
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
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

MODEL_VERSION = "digital-crystal-v1-frozen"
SIGNALLING_VERSION = "digital-crystal-signalling-v1"
SCHEMA_VERSION = 1

Cell = Tuple[int, int]
HEX_DIRECTIONS: Sequence[Cell] = (
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1),
)

PROFILES = {
    "quick": dict(
        population=36, steps=120, grid_width=6, grid_height=6,
        crystal_radius=14, replicates=4,
        coupling_values=(0.0, 0.03, 0.06, 0.10),
        delay_values=(0, 1, 3), noise_values=(0.0, 0.03),
    ),
    "standard": dict(
        population=100, steps=220, grid_width=10, grid_height=10,
        crystal_radius=18, replicates=12,
        coupling_values=(0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.14),
        delay_values=(0, 1, 3, 5), noise_values=(0.0, 0.02, 0.05),
    ),
    "full": dict(
        population=144, steps=320, grid_width=12, grid_height=12,
        crystal_radius=22, replicates=30,
        coupling_values=(0.0, 0.015, 0.03, 0.045, 0.06, 0.08, 0.10, 0.14, 0.18),
        delay_values=(0, 1, 2, 4, 8), noise_values=(0.0, 0.01, 0.03, 0.06),
    ),
}

@dataclass(frozen=True)
class CrystalParams:
    base_bias: float = -2.10
    neighbor_gain: float = 0.78
    signal_rate_gain: float = 0.28
    anisotropy_gain: float = 0.95
    signal_phase_gain: float = 1.15
    crowding_penalty: float = 0.22

@dataclass(frozen=True)
class NetworkSpec:
    mode: str
    population: int
    steps: int
    grid_width: int
    grid_height: int
    crystal_radius: int
    coupling_strength: float
    local_radius: float
    phase_noise: float
    pulse_delay: int
    seed: int
    crystal_params: CrystalParams = CrystalParams()

    def key_dict(self) -> dict:
        d = asdict(self)
        d["model_version"] = MODEL_VERSION
        d["signalling_version"] = SIGNALLING_VERSION
        return d

    def run_key(self) -> str:
        raw = json.dumps(self.key_dict(), sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()[:24]

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
    vx = vy = 0.0
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

@dataclass
class CrystalProcess:
    occupied: Set[Cell]
    birth_time: Dict[Cell, int]
    rng: random.Random
    attachments: List[int]
    population: List[int]

def new_crystal(seed: int) -> CrystalProcess:
    return CrystalProcess(
        occupied={(0, 0)},
        birth_time={(0, 0): 0},
        rng=random.Random(seed),
        attachments=[1],
        population=[1],
    )

def advance_crystal(
    crystal: CrystalProcess,
    step: int,
    phase_signal: float,
    max_radius: int,
    params: CrystalParams,
) -> int:
    frontier: Set[Cell] = set()
    for cell in crystal.occupied:
        for nb in neighbors(cell):
            if nb not in crystal.occupied and hex_distance(nb) <= max_radius:
                frontier.add(nb)

    additions = []
    for cell in frontier:
        n = sum(nb in crystal.occupied for nb in neighbors(cell))
        theta = local_exposure_angle(cell, crystal.occupied)
        phase = params.signal_phase_gain * float(phase_signal)
        anisotropy = math.cos(6.0 * theta + phase)
        crowding = max(0, n - 2)
        score = (
            params.base_bias
            + params.neighbor_gain * n
            + params.signal_rate_gain * float(phase_signal)
            + params.anisotropy_gain * anisotropy
            - params.crowding_penalty * crowding
        )
        if crystal.rng.random() < logistic(score):
            additions.append(cell)

    for cell in additions:
        crystal.occupied.add(cell)
        crystal.birth_time[cell] = step

    crystal.attachments.append(len(additions))
    crystal.population.append(len(crystal.occupied))
    return len(additions)

@dataclass
class OscillatorState:
    phase: np.ndarray
    omega: np.ndarray
    positions: np.ndarray
    last_phase: np.ndarray

def make_positions(width: int, height: int) -> np.ndarray:
    return np.asarray(
        [(float(x), float(y)) for y in range(height) for x in range(width)],
        dtype=float,
    )

def make_oscillators(spec: NetworkSpec) -> OscillatorState:
    rng = np.random.default_rng(spec.seed)
    positions = make_positions(spec.grid_width, spec.grid_height)
    if len(positions) != spec.population:
        raise ValueError("population must equal grid_width * grid_height")
    phase = rng.uniform(0.0, 2 * np.pi, size=spec.population)
    omega = rng.normal(
        loc=2 * np.pi / 18.0,
        scale=2 * np.pi / 220.0,
        size=spec.population,
    )
    return OscillatorState(
        phase=phase,
        omega=omega,
        positions=positions,
        last_phase=np.array(phase, copy=True),
    )

def order_parameter(phases: np.ndarray) -> float:
    return float(abs(np.mean(np.exp(1j * phases))))

def neighbor_indices(positions: np.ndarray, radius: float) -> List[np.ndarray]:
    out = []
    for i, pos in enumerate(positions):
        d = np.linalg.norm(positions - pos, axis=1)
        out.append(np.where((d > 0.0) & (d <= radius))[0])
    return out

def local_order_parameter(phases: np.ndarray, positions: np.ndarray, radius: float) -> float:
    neigh = neighbor_indices(positions, radius)
    vals = []
    for i, idx in enumerate(neigh):
        if len(idx) == 0:
            continue
        vals.append(abs(np.mean(np.exp(1j * np.concatenate([[phases[i]], phases[idx]])))))
    return float(np.mean(vals)) if vals else 0.0

def detect_pulses(last_phase: np.ndarray, phase: np.ndarray) -> np.ndarray:
    return phase < last_phase

def apply_pulse_coupling(
    phases: np.ndarray,
    emitters: Sequence[int],
    neigh: List[np.ndarray],
    mode: str,
    coupling_strength: float,
    shuffled_map: Optional[np.ndarray],
) -> Tuple[np.ndarray, int]:
    if coupling_strength <= 0 or len(emitters) == 0:
        return phases, 0

    out = np.array(phases, copy=True)
    delivered = 0
    n = len(phases)

    for sender in emitters:
        if mode == "global":
            receivers = np.asarray([i for i in range(n) if i != sender], dtype=int)
        elif mode in ("local", "shuffled"):
            receivers = neigh[sender]
        elif mode == "uncoupled":
            continue
        else:
            raise ValueError(mode)

        if mode == "shuffled" and shuffled_map is not None:
            receivers = shuffled_map[receivers]

        for r in receivers:
            # One bit only: a pulse occurred.
            # Receiver does not know sender phase.
            response = math.sin(float(out[r]))
            out[r] += coupling_strength * response
            delivered += 1

    return np.mod(out, 2 * np.pi), delivered

@dataclass
class NetworkResult:
    spec: NetworkSpec
    global_r: List[float]
    local_r: List[float]
    pulse_emit_count: List[int]
    pulse_delivery_count: List[int]
    mean_attachment: List[float]
    phases_final: np.ndarray
    crystals: List[CrystalProcess]
    total_emitted: int
    total_delivered: int

def run_network(spec: NetworkSpec) -> NetworkResult:
    osc = make_oscillators(spec)
    rng = np.random.default_rng(spec.seed + 999_983)
    crystals = [
        new_crystal(spec.seed + 1_000_003 + i * 7919)
        for i in range(spec.population)
    ]
    neigh = neighbor_indices(osc.positions, spec.local_radius)

    shuffled_map = np.arange(spec.population)
    rng.shuffle(shuffled_map)

    global_r = [order_parameter(osc.phase)]
    local_r = [local_order_parameter(osc.phase, osc.positions, spec.local_radius)]
    pulse_emit_count = [0]
    pulse_delivery_count = [0]
    mean_attachment = [1.0]
    pulse_queue: Dict[int, List[int]] = {}
    total_emitted = total_delivered = 0

    for step in range(1, spec.steps + 1):
        osc.last_phase = np.array(osc.phase, copy=True)
        osc.phase = np.mod(
            osc.phase
            + osc.omega
            + rng.normal(0.0, spec.phase_noise, size=spec.population),
            2 * np.pi,
        )

        emitters_bool = detect_pulses(osc.last_phase, osc.phase)
        emit_count = int(np.sum(emitters_bool))
        total_emitted += emit_count

        arrival_step = step + max(0, spec.pulse_delay)
        pulse_queue.setdefault(arrival_step, []).extend(
            map(int, np.where(emitters_bool)[0])
        )

        arriving = pulse_queue.pop(step, [])
        osc.phase, delivered = apply_pulse_coupling(
            osc.phase,
            arriving,
            neigh,
            spec.mode,
            spec.coupling_strength,
            shuffled_map,
        )
        total_delivered += delivered

        attachments = []
        for i in range(spec.population):
            forcing = math.sin(float(osc.phase[i]))
            attachments.append(
                advance_crystal(
                    crystals[i],
                    step,
                    forcing,
                    spec.crystal_radius,
                    spec.crystal_params,
                )
            )

        global_r.append(order_parameter(osc.phase))
        local_r.append(local_order_parameter(osc.phase, osc.positions, spec.local_radius))
        pulse_emit_count.append(emit_count)
        pulse_delivery_count.append(delivered)
        mean_attachment.append(float(np.mean(attachments)))

    return NetworkResult(
        spec=spec,
        global_r=global_r,
        local_r=local_r,
        pulse_emit_count=pulse_emit_count,
        pulse_delivery_count=pulse_delivery_count,
        mean_attachment=mean_attachment,
        phases_final=np.array(osc.phase, copy=True),
        crystals=crystals,
        total_emitted=total_emitted,
        total_delivered=total_delivered,
    )

def crystal_boundary_variation(crystal: CrystalProcess) -> float:
    boundary = [
        c for c in crystal.occupied
        if any(nb not in crystal.occupied for nb in neighbors(c))
    ]
    if not boundary:
        return 0.0
    xy = np.asarray([axial_to_xy(c) for c in boundary], dtype=float)
    r = np.sqrt((xy ** 2).sum(axis=1))
    mean = float(np.mean(r))
    return float(np.std(r) / max(mean, 1e-9))

def population_morphology_summary(result: NetworkResult) -> dict:
    final_pop = np.asarray([len(c.occupied) for c in result.crystals], dtype=float)
    rough = np.asarray([crystal_boundary_variation(c) for c in result.crystals], dtype=float)
    attach = np.asarray([c.attachments[1:] for c in result.crystals], dtype=float)

    mean_pairwise_growth_corr = 0.0
    if attach.shape[1] > 2:
        corr = np.corrcoef(attach)
        upper = corr[np.triu_indices_from(corr, k=1)]
        upper = upper[np.isfinite(upper)]
        if len(upper):
            mean_pairwise_growth_corr = float(np.mean(upper))

    return {
        "mean_final_population": float(np.mean(final_pop)),
        "std_final_population": float(np.std(final_pop)),
        "mean_boundary_cv": float(np.mean(rough)),
        "std_boundary_cv": float(np.std(rough)),
        "mean_pairwise_growth_correlation": mean_pairwise_growth_corr,
    }

class Cache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS runs (
            run_key TEXT PRIMARY KEY,
            spec_json TEXT NOT NULL,
            global_r_json TEXT NOT NULL,
            local_r_json TEXT NOT NULL,
            pulse_emit_json TEXT NOT NULL,
            pulse_delivery_json TEXT NOT NULL,
            mean_attachment_json TEXT NOT NULL,
            phase_final_json TEXT NOT NULL,
            crystal_blob BLOB NOT NULL,
            total_emitted INTEGER NOT NULL,
            total_delivered INTEGER NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    @staticmethod
    def _pack_crystals(crystals: List[CrystalProcess]) -> bytes:
        obj = []
        for c in crystals:
            obj.append({
                "occupied": [[q, r] for q, r in sorted(c.occupied)],
                "birth": {f"{q},{r}": int(t) for (q, r), t in c.birth_time.items()},
                "attachments": c.attachments,
                "population": c.population,
            })
        return zlib.compress(json.dumps(obj).encode(), 6)

    @staticmethod
    def _unpack_crystals(blob: bytes) -> List[CrystalProcess]:
        raw = json.loads(zlib.decompress(blob).decode())
        out = []
        for i, d in enumerate(raw):
            birth = {
                tuple(map(int, k.split(","))): int(v)
                for k, v in d["birth"].items()
            }
            out.append(
                CrystalProcess(
                    occupied={tuple(x) for x in d["occupied"]},
                    birth_time=birth,
                    rng=random.Random(i),
                    attachments=list(d["attachments"]),
                    population=list(d["population"]),
                )
            )
        return out

    def get(self, spec: NetworkSpec) -> Optional[NetworkResult]:
        row = self.conn.execute("""
        SELECT global_r_json, local_r_json, pulse_emit_json, pulse_delivery_json,
               mean_attachment_json, phase_final_json, crystal_blob,
               total_emitted, total_delivered
        FROM runs WHERE run_key=?
        """, (spec.run_key(),)).fetchone()
        if row is None:
            return None

        return NetworkResult(
            spec=spec,
            global_r=list(json.loads(row[0])),
            local_r=list(json.loads(row[1])),
            pulse_emit_count=list(json.loads(row[2])),
            pulse_delivery_count=list(json.loads(row[3])),
            mean_attachment=list(json.loads(row[4])),
            phases_final=np.asarray(json.loads(row[5]), dtype=float),
            crystals=self._unpack_crystals(row[6]),
            total_emitted=int(row[7]),
            total_delivered=int(row[8]),
        )

    def put(self, result: NetworkResult):
        self.conn.execute("""
        INSERT OR REPLACE INTO runs(
            run_key, spec_json, global_r_json, local_r_json,
            pulse_emit_json, pulse_delivery_json, mean_attachment_json,
            phase_final_json, crystal_blob, total_emitted, total_delivered,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.spec.run_key(),
            json.dumps(result.spec.key_dict(), sort_keys=True),
            json.dumps(result.global_r),
            json.dumps(result.local_r),
            json.dumps(result.pulse_emit_count),
            json.dumps(result.pulse_delivery_count),
            json.dumps(result.mean_attachment),
            json.dumps(result.phases_final.tolist()),
            self._pack_crystals(result.crystals),
            result.total_emitted,
            result.total_delivered,
            time.time(),
        ))
        self.conn.commit()

    def get_or_run(self, spec: NetworkSpec) -> Tuple[NetworkResult, bool]:
        cached = self.get(spec)
        if cached is not None:
            return cached, True
        result = run_network(spec)
        self.put(result)
        return result, False

def tail_mean(values: Sequence[float], fraction: float = 0.35) -> float:
    start = int(len(values) * (1.0 - fraction))
    return float(np.mean(values[start:]))

def result_summary(result: NetworkResult) -> dict:
    return {
        "mean_global_r_tail": tail_mean(result.global_r),
        "mean_local_r_tail": tail_mean(result.local_r),
        "final_global_r": float(result.global_r[-1]),
        "final_local_r": float(result.local_r[-1]),
        "total_emitted": int(result.total_emitted),
        "total_delivered": int(result.total_delivered),
        "morphology": population_morphology_summary(result),
    }

def aggregate(rows: List[dict]) -> dict:
    out = {}
    for key in ("mean_global_r_tail", "mean_local_r_tail", "final_global_r", "final_local_r"):
        vals = np.asarray([r[key] for r in rows], dtype=float)
        out[key] = {
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
        }

    corr = np.asarray(
        [r["morphology"]["mean_pairwise_growth_correlation"] for r in rows],
        dtype=float,
    )
    out["mean_pairwise_growth_correlation"] = {
        "mean": float(np.mean(corr)),
        "std": float(np.std(corr)),
    }
    return out

def draw_crystal(ax, crystal: CrystalProcess, title: str):
    births = np.asarray(list(crystal.birth_time.values()), dtype=float)
    bmin = float(births.min()) if len(births) else 0.0
    bmax = float(births.max()) if len(births) else 1.0
    denom = max(1.0, bmax - bmin)

    for cell in crystal.occupied:
        x, y = axial_to_xy(cell)
        v = (crystal.birth_time.get(cell, 0) - bmin) / denom
        ax.add_patch(
            RegularPolygon(
                (x, y), 6, radius=0.94, orientation=np.pi / 6,
                facecolor=plt.cm.viridis(v), edgecolor="none"
            )
        )

    pts = np.asarray([axial_to_xy(c) for c in crystal.occupied], dtype=float)
    if len(pts):
        margin = 2.0
        ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
        ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)

class Reporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        report_dir.mkdir(parents=True, exist_ok=True)
        self.sections = []

    def json(self, name: str, data: dict):
        p = self.report_dir / name
        p.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[report] {p}")

    def stage(self, name: str, title: str, body: str):
        p = self.report_dir / name
        p.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")
        self.sections.append((title, body.strip()))
        print(f"[report] {p}")

    def full(self, metadata: dict) -> Path:
        chunks = [
            "# Chapter 16 — Digital Crystal Signalling: Full Experimental Report",
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
        p = self.report_dir / "ch16-full-report.md"
        p.write_text("\n".join(chunks), encoding="utf-8")
        return p

def make_spec(profile, seed, mode, coupling, delay=0, noise=0.0, local_radius=1.5):
    return NetworkSpec(
        mode=mode,
        population=profile["population"],
        steps=profile["steps"],
        grid_width=profile["grid_width"],
        grid_height=profile["grid_height"],
        crystal_radius=profile["crystal_radius"],
        coupling_strength=float(coupling),
        local_radius=float(local_radius),
        phase_noise=float(noise),
        pulse_delay=int(delay),
        seed=int(seed),
    )

def run_replicates(cache, profile, base_seed, mode, coupling, delay=0, noise=0.0, local_radius=1.5, desc="runs"):
    rows = []
    exemplar = None
    cached = 0
    for rep in tqdm(range(profile["replicates"]), desc=desc):
        spec = make_spec(
            profile,
            base_seed + rep * 1009,
            mode,
            coupling,
            delay,
            noise,
            local_radius,
        )
        result, was_cached = cache.get_or_run(spec)
        cached += int(was_cached)
        rows.append(result_summary(result))
        exemplar = exemplar or result
    return rows, exemplar, cached

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=tuple(PROFILES), default="quick")
    ap.add_argument("--db", default="research/digital-life/ch16-digital-crystal-signalling.sqlite3")
    ap.add_argument("--images", default="static/images/books/digital-life")
    ap.add_argument("--reports", default="research/digital-life/ch16-reports")
    ap.add_argument("--seed", type=int, default=20260811)
    ap.add_argument("--force-recompute", action="store_true")
    args = ap.parse_args()

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
    metadata = {
        "model_version": MODEL_VERSION,
        "signalling_version": SIGNALLING_VERSION,
        "profile": args.profile,
        "profile_config": profile,
        "seed": args.seed,
        "started_at_unix": time.time(),
    }

    # Stage 1
    print("\n=== STAGE 1 — UNCOUPLED BASELINE ===")
    base_rows, base_ex, _ = run_replicates(
        cache, profile, args.seed + 100_000,
        "uncoupled", 0.0, desc="baseline"
    )
    base_agg = aggregate(base_rows)
    fig1 = image_dir / "ch16-01-uncoupled-baseline.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(base_ex.global_r, label="global r")
    ax.plot(base_ex.local_r, label="local r")
    ax.set_ylim(0, 1); ax.set_xlabel("step"); ax.set_ylabel("coherence")
    ax.set_title("Uncoupled baseline"); ax.legend()
    fig.tight_layout(); fig.savefig(fig1, dpi=180); plt.close(fig)

    reporter.json("stage-01-baseline.json", base_agg)
    reporter.stage("stage-01-baseline.md", "Stage 1 — Independent Crystals",
        f"""Uncoupled population baseline.

```json
{json.dumps(base_agg, indent=2)}
```

Figure: `{fig1}`
""")

    # Stage 2 coupling sweep
    print("\n=== STAGE 2 — GLOBAL COUPLING SWEEP ===")
    sweep = {}
    sweep_ex = {}
    for k in profile["coupling_values"]:
        mode = "uncoupled" if k == 0 else "global"
        rows, ex, _ = run_replicates(
            cache, profile,
            args.seed + 200_000 + int(k * 100_000),
            mode, k, desc=f"K={k:.3f}"
        )
        sweep[float(k)] = aggregate(rows)
        sweep_ex[float(k)] = ex

    fig2 = image_dir / "ch16-02-global-coupling-sweep.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = sorted(sweep)
    ax.plot(xs, [sweep[x]["mean_global_r_tail"]["mean"] for x in xs], marker="o", label="global")
    ax.plot(xs, [sweep[x]["mean_local_r_tail"]["mean"] for x in xs], marker="o", label="local")
    ax.set_ylim(0, 1); ax.set_xlabel("coupling K"); ax.set_ylabel("tail mean r")
    ax.set_title("One-bit pulse coupling sweep"); ax.legend()
    fig.tight_layout(); fig.savefig(fig2, dpi=180); plt.close(fig)

    reporter.json("stage-02-global-coupling.json", {str(k): v for k, v in sweep.items()})
    reporter.stage("stage-02-global-coupling.md", "Stage 2 — One-Bit Global Pulse Coupling",
        f"""Each process emits only a pulse when its phase wraps.

```json
{json.dumps({str(k): v for k, v in sweep.items()}, indent=2)}
```

Figure: `{fig2}`
""")

    best_k = max(sweep, key=lambda k: sweep[k]["mean_global_r_tail"]["mean"])
    best_global = sweep[best_k]["mean_global_r_tail"]["mean"]

    # Stage 3 local
    print("\n=== STAGE 3 — LOCAL COUPLING ===")
    local_rows, local_ex, _ = run_replicates(
        cache, profile, args.seed + 300_000,
        "local", best_k, local_radius=1.5, desc="local"
    )
    local_agg = aggregate(local_rows)
    reporter.json("stage-03-local-coupling.json", local_agg)
    reporter.stage("stage-03-local-coupling.md", "Stage 3 — Local Pulse Coupling",
        f"""Local-neighbour coupling at K={best_k:.3f}.

```json
{json.dumps(local_agg, indent=2)}
```""")

    # Stage 4 shuffled control + matched fresh controls
    print("\n=== STAGE 4 — SHUFFLED CONTROL ===")
    shuf_rows, shuf_ex, _ = run_replicates(
        cache, profile, args.seed + 400_000,
        "shuffled", best_k, local_radius=1.5, desc="shuffled"
    )
    shuf_agg = aggregate(shuf_rows)

    unc_rows, unc_ex, _ = run_replicates(
        cache, profile, args.seed + 410_000,
        "uncoupled", 0.0, desc="matched uncoupled"
    )
    unc_agg = aggregate(unc_rows)

    glob_rows, glob_ex, _ = run_replicates(
        cache, profile, args.seed + 420_000,
        "global", best_k, desc="matched global"
    )
    glob_agg = aggregate(glob_rows)

    modes = {
        "uncoupled": unc_agg,
        "global": glob_agg,
        "local": local_agg,
        "shuffled": shuf_agg,
    }

    fig4 = image_dir / "ch16-04-mode-comparison.png"
    labels = list(modes)
    x = np.arange(len(labels)); width = 0.38
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x-width/2, [modes[k]["mean_global_r_tail"]["mean"] for k in labels], width, label="global")
    ax.bar(x+width/2, [modes[k]["mean_local_r_tail"]["mean"] for k in labels], width, label="local")
    ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylim(0, 1)
    ax.set_ylabel("tail mean r"); ax.set_title("Control comparison"); ax.legend()
    fig.tight_layout(); fig.savefig(fig4, dpi=180); plt.close(fig)

    reporter.json("stage-04-shuffled-control.json", modes)
    reporter.stage("stage-04-shuffled-control.md", "Stage 4 — Break the Communication Topology",
        f"""Real and topology-broken event delivery are compared.

```json
{json.dumps(modes, indent=2)}
```

Figure: `{fig4}`
""")

    # Stage 5 delay/noise robustness
    print("\n=== STAGE 5 — DELAY / NOISE ROBUSTNESS ===")
    robustness = []
    for noise in profile["noise_values"]:
        for delay in profile["delay_values"]:
            rows, _, _ = run_replicates(
                cache, profile,
                args.seed + 500_000 + int(noise*1_000_000) + delay*10_000,
                "local", best_k, delay=delay, noise=noise,
                local_radius=1.5,
                desc=f"delay={delay} noise={noise:.3f}"
            )
            a = aggregate(rows)
            robustness.append({
                "pulse_delay": delay,
                "phase_noise": noise,
                "mean_global_r_tail": a["mean_global_r_tail"]["mean"],
                "mean_local_r_tail": a["mean_local_r_tail"]["mean"],
            })

    fig5 = image_dir / "ch16-05-delay-noise-robustness.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    for noise in sorted(set(r["phase_noise"] for r in robustness)):
        rr = sorted(
            [r for r in robustness if r["phase_noise"] == noise],
            key=lambda r: r["pulse_delay"]
        )
        ax.plot(
            [r["pulse_delay"] for r in rr],
            [r["mean_local_r_tail"] for r in rr],
            marker="o",
            label=f"noise={noise}"
        )
    ax.set_ylim(0, 1); ax.set_xlabel("pulse delay"); ax.set_ylabel("tail mean local r")
    ax.set_title("Delay/noise robustness"); ax.legend()
    fig.tight_layout(); fig.savefig(fig5, dpi=180); plt.close(fig)

    reporter.json("stage-05-delay-noise.json", {"rows": robustness})
    reporter.stage("stage-05-delay-noise.md", "Stage 5 — Delay and Noise",
        f"""Robustness sweep.

```json
{json.dumps(robustness, indent=2)}
```

Figure: `{fig5}`
""")

    # Stage 6 growth consequences
    print("\n=== STAGE 6 — MORPHOLOGICAL CONSEQUENCE ===")
    growth = {
        k: v["mean_pairwise_growth_correlation"]
        for k, v in modes.items()
    }

    fig6a = image_dir / "ch16-06-growth-correlation.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(list(growth), [growth[k]["mean"] for k in growth])
    ax.set_ylabel("mean pairwise growth correlation")
    ax.set_title("Does pulse coupling reach crystal growth?")
    fig.tight_layout(); fig.savefig(fig6a, dpi=180); plt.close(fig)

    fig6b = image_dir / "ch16-06-crystal-gallery.png"
    ids = [0, len(unc_ex.crystals)//3, 2*len(unc_ex.crystals)//3]
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    for j, i in enumerate(ids):
        draw_crystal(axes[0, j], unc_ex.crystals[i], f"Uncoupled #{i}")
        draw_crystal(axes[1, j], local_ex.crystals[i], f"Local coupled #{i}")
    fig.tight_layout(); fig.savefig(fig6b, dpi=180); plt.close(fig)

    reporter.json("stage-06-morphological-consequence.json", growth)
    reporter.stage("stage-06-morphological-consequence.md", "Stage 6 — Does Signalling Reach the Crystal?",
        f"""Mean pairwise growth-activity correlation:

```json
{json.dumps(growth, indent=2)}
```

Figures:
- `{fig6a}`
- `{fig6b}`
""")

    # Stage 7 verdict
    print("\n=== STAGE 7 — VERDICT ===")
    unc_global = unc_agg["mean_global_r_tail"]["mean"]
    unc_local = unc_agg["mean_local_r_tail"]["mean"]
    local_local = local_agg["mean_local_r_tail"]["mean"]
    shuf_local = shuf_agg["mean_local_r_tail"]["mean"]
    unc_growth = unc_agg["mean_pairwise_growth_correlation"]["mean"]
    local_growth = local_agg["mean_pairwise_growth_correlation"]["mean"]

    h1 = best_global >= unc_global + 0.10
    h2 = local_local >= unc_local + 0.08
    h3 = local_local >= shuf_local + 0.03
    h4 = local_growth >= unc_growth + 0.03

    if h1 and h2 and h3 and h4:
        verdict = "LOW_BANDWIDTH_SIGNALLING_SUPPORTED"
        claim = (
            "Within this Digital Crystal population, one-bit pulse events increased "
            "phase coherence, real local topology outperformed a shuffled control, "
            "and the coupling propagated into correlated crystal growth."
        )
    elif h1 and h2:
        verdict = "PARTIALLY_SUPPORTED"
        claim = (
            "One-bit pulse coupling increased oscillator coherence, but one or more "
            "stronger topology-control or crystal-growth consequences did not clear "
            "the predeclared margins."
        )
    else:
        verdict = "NOT_SUPPORTED_AS_TESTED"
        claim = (
            "This one-bit pulse mechanism did not establish robust inter-crystal "
            "synchronization above the uncoupled controls."
        )

    summary = {
        "verdict": verdict,
        "bounded_claim": claim,
        "selected_coupling_strength": best_k,
        "checks": {
            "global_coupling_increases_coherence": h1,
            "local_coupling_increases_local_coherence": h2,
            "real_local_topology_beats_shuffled_control": h3,
            "coupling_reaches_crystal_growth": h4,
        },
        "headline_metrics": {
            "uncoupled_global_r": unc_global,
            "best_global_r": best_global,
            "uncoupled_local_r": unc_local,
            "local_local_r": local_local,
            "shuffled_local_r": shuf_local,
            "uncoupled_growth_correlation": unc_growth,
            "local_growth_correlation": local_growth,
        },
        "explicit_nonclaims": [
            "language", "semantics", "cooperation", "coordination",
            "planning", "learning", "intelligence", "agency", "life",
        ],
    }
    reporter.json("ch16-summary.json", summary)
    reporter.stage("stage-07-verdict.md", "Stage 7 — Experimental Verdict",
        f"""**Verdict: `{verdict}`**

> {claim}

```json
{json.dumps(summary, indent=2)}
```""")

    metadata["finished_at_unix"] = time.time()
    metadata["final_verdict"] = verdict
    metadata["selected_coupling_strength"] = best_k
    full = reporter.full(metadata)

    print("\n" + "="*80)
    print("CHAPTER 16 DIGITAL CRYSTAL SIGNALLING EXPERIMENT COMPLETE")
    print("="*80)
    print(f"Verdict:      {verdict}")
    print(claim)
    print(f"SQLite cache: {db_path}")
    print(f"Full report:  {full}")
    print(f"Summary:      {report_dir / 'ch16-summary.json'}")
    print(f"Figures:      {image_dir}")
    print("="*80)

    cache.close()

if __name__ == "__main__":
    main()
