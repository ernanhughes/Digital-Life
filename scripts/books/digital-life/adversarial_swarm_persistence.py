from __future__ import annotations

"""
Digital Life — adversarial persistence experiment

Purpose
-------
Construct a deliberately nonliving, relation-driven particle system that can
display persistent macroscopic organization, then ask which layer of the
system actually carries that persistence.

The experiment separates three interventions:

A. MATERIAL DAMAGE
   Displace a fraction of particles while preserving the friend/enemy graph.

B. ORGANIZATIONAL DAMAGE
   Preserve particle positions/velocities but rewire a fraction of the
   friend/enemy graph.

C. MATERIAL REPLACEMENT
   Replace every material identity over time while preserving positions,
   velocities, and the relationship graph.

The key scientific distinction is:

    visible organization
    != material identity
    != generative organization

This script is intentionally self-contained and writes publication-friendly
CSV/JSON/PNG outputs.

Dependencies
------------
    pip install numpy scipy matplotlib

Example
-------
    python scripts/books/digital-life/adversarial_swarm_persistence.py

Quick smoke test:
    python scripts/books/digital-life/adversarial_swarm_persistence.py --quick

More replicates:
    python scripts/books/digital-life/adversarial_swarm_persistence.py \
        --replicates 12 --particles 256 --burn-in 10000 --post-steps 6000
"""

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wasserstein_distance


EPS = 1e-12


# =====================================================================
# Configuration / state
# =====================================================================


@dataclass(frozen=True)
class Config:
    particles: int = 256
    dt: float = 0.05
    damping: float = 0.94
    max_speed: float = 2.5

    # Relation-driven dynamics.
    centre_strength: float = 0.015
    friend_strength: float = 0.22
    enemy_strength: float = 0.28
    enemy_length_scale: float = 2.0

    # Weak all-particle soft-core repulsion prevents pathological collapse.
    # It is not an alignment/flocking rule.
    softcore_strength: float = 0.020
    softcore_length_scale: float = 0.55

    burn_in: int = 10_000
    reference_window: int = 1_000
    reference_stride: int = 20
    post_steps: int = 6_000
    sample_stride: int = 20

    damage_fraction: float = 0.30
    damage_scale: float = 2.5
    rewire_fraction: float = 0.30

    # Material replacement is completed gradually across this fraction
    # of the post-intervention run.
    replacement_finish_fraction: float = 0.60

    histogram_bins: int = 64


@dataclass
class SwarmState:
    position: np.ndarray        # [n, 2]
    velocity: np.ndarray        # [n, 2]
    friend: np.ndarray          # [n]
    enemy: np.ndarray           # [n]
    material_id: np.ndarray     # [n], causally inert identity labels
    next_material_id: int

    def clone(self) -> "SwarmState":
        return SwarmState(
            position=self.position.copy(),
            velocity=self.velocity.copy(),
            friend=self.friend.copy(),
            enemy=self.enemy.copy(),
            material_id=self.material_id.copy(),
            next_material_id=int(self.next_material_id),
        )


@dataclass
class ReferenceMacrostate:
    radial_samples: np.ndarray
    pair_samples: np.ndarray
    radius_mean: float
    radius_std: float
    anisotropy_mean: float
    anisotropy_std: float
    speed_mean: float
    speed_std: float
    friend: np.ndarray
    enemy: np.ndarray
    initial_material_ids: np.ndarray


# =====================================================================
# Dynamics
# =====================================================================


def _safe_unit(v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norm = np.linalg.norm(v, axis=1)
    unit = np.zeros_like(v)
    valid = norm > EPS
    unit[valid] = v[valid] / norm[valid, None]
    return unit, norm


def make_state(cfg: Config, rng: np.random.Generator) -> SwarmState:
    n = cfg.particles

    # Start as an unstructured cloud. No ring, flock, vortex, boundary, or
    # macroscopic object is encoded here.
    position = rng.normal(0.0, 3.0, size=(n, 2))
    velocity = rng.normal(0.0, 0.15, size=(n, 2))

    friend = np.empty(n, dtype=np.int64)
    enemy = np.empty(n, dtype=np.int64)

    for i in range(n):
        choices = np.delete(np.arange(n), i)
        f, e = rng.choice(choices, size=2, replace=False)
        friend[i] = int(f)
        enemy[i] = int(e)

    material_id = np.arange(n, dtype=np.int64)

    return SwarmState(
        position=position,
        velocity=velocity,
        friend=friend,
        enemy=enemy,
        material_id=material_id,
        next_material_id=n,
    )


def acceleration(state: SwarmState, cfg: Config) -> np.ndarray:
    pos = state.position
    n = len(pos)

    centroid = pos.mean(axis=0, keepdims=True)
    to_centre = centroid - pos

    friend_vec = pos[state.friend] - pos
    friend_unit, friend_dist = _safe_unit(friend_vec)

    enemy_vec = pos[state.enemy] - pos
    enemy_unit, enemy_dist = _safe_unit(enemy_vec)

    # Friend attraction gets stronger with distance but saturates.
    friend_mag = np.tanh(friend_dist / 2.0)
    a_friend = cfg.friend_strength * friend_mag[:, None] * friend_unit

    # Enemy repulsion matters mainly at short/medium range.
    enemy_mag = np.exp(-enemy_dist / cfg.enemy_length_scale)
    a_enemy = -cfg.enemy_strength * enemy_mag[:, None] * enemy_unit

    # Weak attraction to the instantaneous centre keeps the world bounded.
    a_centre = cfg.centre_strength * to_centre

    # Soft-core repulsion is deliberately non-aligning: it only prevents
    # particles occupying almost the same point.
    delta = pos[:, None, :] - pos[None, :, :]          # i - j
    dist2 = np.sum(delta * delta, axis=2)
    np.fill_diagonal(dist2, np.inf)
    mask = dist2 < (3.0 * cfg.softcore_length_scale) ** 2

    dist = np.sqrt(dist2, where=np.isfinite(dist2), out=np.full_like(dist2, np.inf))
    weight = np.zeros_like(dist)
    weight[mask] = np.exp(
        -dist[mask] / cfg.softcore_length_scale
    ) / np.maximum(dist[mask], 1e-6)

    a_soft = cfg.softcore_strength * np.sum(
        weight[:, :, None] * delta, axis=1
    )

    return a_centre + a_friend + a_enemy + a_soft


def step(state: SwarmState, cfg: Config) -> None:
    a = acceleration(state, cfg)

    state.velocity *= cfg.damping
    state.velocity += cfg.dt * a

    speed = np.linalg.norm(state.velocity, axis=1)
    too_fast = speed > cfg.max_speed
    if np.any(too_fast):
        state.velocity[too_fast] *= (
            cfg.max_speed / speed[too_fast]
        )[:, None]

    state.position += cfg.dt * state.velocity

    # Remove centre-of-mass drift. This is a coordinate choice, not a
    # flocking/alignment force.
    state.position -= state.position.mean(axis=0, keepdims=True)


# =====================================================================
# Measurements
# =====================================================================


def radial_distances(position: np.ndarray) -> np.ndarray:
    centred = position - position.mean(axis=0, keepdims=True)
    return np.linalg.norm(centred, axis=1)


def pairwise_distances(position: np.ndarray) -> np.ndarray:
    delta = position[:, None, :] - position[None, :, :]
    dist = np.linalg.norm(delta, axis=2)
    iu = np.triu_indices(len(position), k=1)
    return dist[iu]


def radius_of_gyration(position: np.ndarray) -> float:
    r = radial_distances(position)
    return float(np.sqrt(np.mean(r * r)))


def anisotropy(position: np.ndarray) -> float:
    centred = position - position.mean(axis=0, keepdims=True)
    cov = np.cov(centred.T)
    eig = np.linalg.eigvalsh(cov)
    eig = np.maximum(eig, EPS)
    return float(eig[-1] / eig[0])


def mean_speed(state: SwarmState) -> float:
    return float(np.mean(np.linalg.norm(state.velocity, axis=1)))


def _normalise_scale(values: np.ndarray, scale: float) -> np.ndarray:
    return np.asarray(values, dtype=np.float64) / max(float(scale), EPS)


def make_reference(
    snapshots: list[SwarmState],
    checkpoint: SwarmState,
) -> ReferenceMacrostate:
    radii = []
    pairs = []
    rg = []
    aniso = []
    speeds = []

    for s in snapshots:
        r = radial_distances(s.position)
        scale = max(radius_of_gyration(s.position), EPS)
        radii.append(_normalise_scale(r, scale))

        p = pairwise_distances(s.position)
        # Subsample pair distances deterministically to keep memory modest.
        if len(p) > 4096:
            idx = np.linspace(0, len(p) - 1, 4096, dtype=np.int64)
            p = np.sort(p)[idx]
        pairs.append(_normalise_scale(p, scale))

        rg.append(scale)
        aniso.append(anisotropy(s.position))
        speeds.append(mean_speed(s))

    return ReferenceMacrostate(
        radial_samples=np.concatenate(radii),
        pair_samples=np.concatenate(pairs),
        radius_mean=float(np.mean(rg)),
        radius_std=float(np.std(rg) + EPS),
        anisotropy_mean=float(np.mean(aniso)),
        anisotropy_std=float(np.std(aniso) + EPS),
        speed_mean=float(np.mean(speeds)),
        speed_std=float(np.std(speeds) + EPS),
        friend=checkpoint.friend.copy(),
        enemy=checkpoint.enemy.copy(),
        initial_material_ids=checkpoint.material_id.copy(),
    )


def graph_similarity(state: SwarmState, ref: ReferenceMacrostate) -> float:
    # Fraction of directed friend/enemy assignments that remain exactly as
    # they were at the checkpoint.
    friend_same = np.mean(state.friend == ref.friend)
    enemy_same = np.mean(state.enemy == ref.enemy)
    return float(0.5 * (friend_same + enemy_same))


def original_material_fraction(
    state: SwarmState, ref: ReferenceMacrostate
) -> float:
    original = set(int(x) for x in ref.initial_material_ids)
    return float(np.mean([int(x) in original for x in state.material_id]))


def visible_distance(
    state: SwarmState,
    ref: ReferenceMacrostate,
) -> dict[str, float]:
    """
    Distance from the pre-intervention macroscopic regime.

    All shape distributions are scale-normalized, so simple expansion or
    contraction cannot by itself dominate the score.
    """
    scale = max(radius_of_gyration(state.position), EPS)

    r = _normalise_scale(radial_distances(state.position), scale)
    p = pairwise_distances(state.position)
    if len(p) > 4096:
        idx = np.linspace(0, len(p) - 1, 4096, dtype=np.int64)
        p = np.sort(p)[idx]
    p = _normalise_scale(p, scale)

    radial_w1 = float(wasserstein_distance(r, ref.radial_samples))
    pair_w1 = float(wasserstein_distance(p, ref.pair_samples))

    # Keep dimensional summaries separate rather than hiding everything in
    # a single score.
    rg_z = abs(scale - ref.radius_mean) / ref.radius_std
    aniso_z = abs(anisotropy(state.position) - ref.anisotropy_mean) / ref.anisotropy_std
    speed_z = abs(mean_speed(state) - ref.speed_mean) / ref.speed_std

    # A bounded convenience score for plots. The raw components are always
    # written to CSV and should be used for scientific interpretation.
    composite_distance = (
        2.0 * radial_w1
        + 2.0 * pair_w1
        + 0.15 * min(rg_z, 10.0)
        + 0.10 * min(aniso_z, 10.0)
        + 0.05 * min(speed_z, 10.0)
    )
    similarity = math.exp(-composite_distance)

    return {
        "radial_w1": radial_w1,
        "pair_w1": pair_w1,
        "radius_gyration": scale,
        "radius_z": float(rg_z),
        "anisotropy": anisotropy(state.position),
        "anisotropy_z": float(aniso_z),
        "mean_speed": mean_speed(state),
        "speed_z": float(speed_z),
        "visible_similarity": float(similarity),
    }


# =====================================================================
# Interventions
# =====================================================================


def material_damage(
    state: SwarmState,
    cfg: Config,
    rng: np.random.Generator,
) -> np.ndarray:
    n_damage = max(1, int(round(cfg.damage_fraction * cfg.particles)))
    idx = rng.choice(cfg.particles, size=n_damage, replace=False)

    rg = max(radius_of_gyration(state.position), EPS)
    direction = rng.normal(size=(n_damage, 2))
    direction /= np.maximum(
        np.linalg.norm(direction, axis=1, keepdims=True), EPS
    )

    magnitude = rng.uniform(
        0.75 * cfg.damage_scale * rg,
        1.25 * cfg.damage_scale * rg,
        size=(n_damage, 1),
    )

    state.position[idx] += direction * magnitude

    # Reset damaged components' momentum so recovery cannot be attributed to
    # simply continuing their previous trajectories.
    state.velocity[idx] = 0.0
    state.position -= state.position.mean(axis=0, keepdims=True)
    return idx


def _draw_other(
    rng: np.random.Generator,
    n: int,
    i: int,
    forbidden: Iterable[int] = (),
) -> int:
    forbidden_set = {int(i), *(int(x) for x in forbidden)}
    choices = np.array(
        [x for x in range(n) if x not in forbidden_set], dtype=np.int64
    )
    return int(rng.choice(choices))


def organizational_damage(
    state: SwarmState,
    cfg: Config,
    rng: np.random.Generator,
) -> np.ndarray:
    n_rewire = max(1, int(round(cfg.rewire_fraction * cfg.particles)))
    idx = rng.choice(cfg.particles, size=n_rewire, replace=False)

    for i in idx:
        i = int(i)
        new_friend = _draw_other(rng, cfg.particles, i)
        new_enemy = _draw_other(
            rng, cfg.particles, i, forbidden=(new_friend,)
        )
        state.friend[i] = new_friend
        state.enemy[i] = new_enemy

    return idx


def replace_material_ids(
    state: SwarmState,
    indices: np.ndarray,
) -> None:
    for i in indices:
        state.material_id[int(i)] = state.next_material_id
        state.next_material_id += 1


# =====================================================================
# Trial
# =====================================================================


def replacement_schedule(cfg: Config) -> dict[int, np.ndarray]:
    """
    Return step -> particle indices for gradual total replacement.

    Every material identity is replaced exactly once; relationship slots,
    positions and velocities remain untouched.
    """
    finish_step = max(
        1, int(round(cfg.post_steps * cfg.replacement_finish_fraction))
    )
    all_idx = np.arange(cfg.particles, dtype=np.int64)
    chunks = min(cfg.particles, max(1, finish_step // cfg.sample_stride))

    schedule: dict[int, np.ndarray] = {}
    split = np.array_split(all_idx, chunks)
    steps = np.linspace(
        cfg.sample_stride,
        finish_step,
        len(split),
        dtype=np.int64,
    )
    for step_no, ids in zip(steps, split, strict=True):
        schedule[int(step_no)] = ids
    return schedule


def run_trial(
    cfg: Config,
    seed: int,
) -> tuple[list[dict], dict, dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    state = make_state(cfg, rng)

    reference_snapshots: list[SwarmState] = []
    ref_start = cfg.burn_in - cfg.reference_window

    for t in range(cfg.burn_in):
        step(state, cfg)
        if (
            t >= ref_start
            and (t - ref_start) % cfg.reference_stride == 0
        ):
            reference_snapshots.append(state.clone())

    checkpoint = state.clone()
    ref = make_reference(reference_snapshots, checkpoint)

    branches = {
        "control": checkpoint.clone(),
        "material_damage": checkpoint.clone(),
        "organizational_damage": checkpoint.clone(),
        "material_replacement": checkpoint.clone(),
    }

    # Independent intervention RNGs derived deterministically from seed.
    material_damage(
        branches["material_damage"],
        cfg,
        np.random.default_rng(seed + 10_001),
    )
    organizational_damage(
        branches["organizational_damage"],
        cfg,
        np.random.default_rng(seed + 20_001),
    )

    schedule = replacement_schedule(cfg)

    rows: list[dict] = []

    def record(branch_name: str, t: int) -> None:
        branch = branches[branch_name]
        metrics = visible_distance(branch, ref)
        rows.append(
            {
                "seed": seed,
                "branch": branch_name,
                "step": t,
                **metrics,
                "graph_similarity": graph_similarity(branch, ref),
                "original_material_fraction": original_material_fraction(
                    branch, ref
                ),
            }
        )

    for name in branches:
        record(name, 0)

    for t in range(1, cfg.post_steps + 1):
        if t in schedule:
            replace_material_ids(
                branches["material_replacement"], schedule[t]
            )

        for branch in branches.values():
            step(branch, cfg)

        if t % cfg.sample_stride == 0 or t == cfg.post_steps:
            for name in branches:
                record(name, t)

    # Final exact completion guard for any rounding in the replacement schedule.
    replacement_branch = branches["material_replacement"]
    still_original = np.isin(
        replacement_branch.material_id,
        ref.initial_material_ids,
    )
    if np.any(still_original):
        replace_material_ids(
            replacement_branch, np.flatnonzero(still_original)
        )
        # Record a final identity-only state at the same dynamical time.
        rows = [
            r for r in rows
            if not (
                r["branch"] == "material_replacement"
                and r["step"] == cfg.post_steps
            )
        ]
        record("material_replacement", cfg.post_steps)

    # Summaries compare late post-intervention behavior, not a single frame.
    late_start = int(cfg.post_steps * 0.75)
    summary: dict[str, dict] = {}

    for name in branches:
        branch_rows = [
            r for r in rows
            if r["branch"] == name and r["step"] >= late_start
        ]
        summary[name] = {
            "late_visible_similarity_mean": float(
                np.mean([r["visible_similarity"] for r in branch_rows])
            ),
            "late_visible_similarity_std": float(
                np.std([r["visible_similarity"] for r in branch_rows])
            ),
            "late_radial_w1_mean": float(
                np.mean([r["radial_w1"] for r in branch_rows])
            ),
            "late_pair_w1_mean": float(
                np.mean([r["pair_w1"] for r in branch_rows])
            ),
            "final_graph_similarity": float(
                graph_similarity(branches[name], ref)
            ),
            "final_original_material_fraction": float(
                original_material_fraction(branches[name], ref)
            ),
        }

    meta = {
        "seed": seed,
        "reference_snapshots": len(reference_snapshots),
        "reference_radius_mean": ref.radius_mean,
        "reference_anisotropy_mean": ref.anisotropy_mean,
        "reference_speed_mean": ref.speed_mean,
        "branches": summary,
    }

    final_positions = {
        name: branch.position.copy()
        for name, branch in branches.items()
    }
    return rows, meta, final_positions


# =====================================================================
# Aggregation / outputs
# =====================================================================


def write_timeseries(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize_replicates(
    trial_meta: list[dict],
) -> list[dict]:
    branches = [
        "control",
        "material_damage",
        "organizational_damage",
        "material_replacement",
    ]
    out = []

    for branch in branches:
        vals = [
            m["branches"][branch]["late_visible_similarity_mean"]
            for m in trial_meta
        ]
        graph = [
            m["branches"][branch]["final_graph_similarity"]
            for m in trial_meta
        ]
        material = [
            m["branches"][branch]["final_original_material_fraction"]
            for m in trial_meta
        ]
        pair_w1 = [
            m["branches"][branch]["late_pair_w1_mean"]
            for m in trial_meta
        ]
        radial_w1 = [
            m["branches"][branch]["late_radial_w1_mean"]
            for m in trial_meta
        ]

        out.append(
            {
                "branch": branch,
                "replicates": len(vals),
                "late_visible_similarity_mean": float(np.mean(vals)),
                "late_visible_similarity_sd": float(np.std(vals, ddof=1))
                if len(vals) > 1 else 0.0,
                "late_pair_w1_mean": float(np.mean(pair_w1)),
                "late_radial_w1_mean": float(np.mean(radial_w1)),
                "final_graph_similarity_mean": float(np.mean(graph)),
                "final_original_material_fraction_mean": float(
                    np.mean(material)
                ),
            }
        )

    return out


def write_summary_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def aggregate_timeseries(rows: list[dict]) -> dict[str, dict[int, tuple[float, float]]]:
    result: dict[str, dict[int, tuple[float, float]]] = {}
    branches = sorted({r["branch"] for r in rows})

    for branch in branches:
        by_step: dict[int, list[float]] = {}
        for r in rows:
            if r["branch"] != branch:
                continue
            by_step.setdefault(int(r["step"]), []).append(
                float(r["visible_similarity"])
            )

        result[branch] = {
            step_no: (float(np.mean(v)), float(np.std(v)))
            for step_no, v in sorted(by_step.items())
        }

    return result


def plot_similarity(path: Path, rows: list[dict]) -> None:
    agg = aggregate_timeseries(rows)

    fig, ax = plt.subplots(figsize=(10, 6))
    for branch, points in agg.items():
        steps = np.array(list(points.keys()))
        mean = np.array([points[t][0] for t in steps])
        sd = np.array([points[t][1] for t in steps])

        ax.plot(steps, mean, label=branch.replace("_", " "))
        ax.fill_between(steps, mean - sd, mean + sd, alpha=0.15)

    ax.set_xlabel("Steps after intervention")
    ax.set_ylabel("Visible macrostate similarity")
    ax.set_ylim(0.0, 1.02)
    ax.set_title("Adversarial swarm: recovery after different kinds of damage")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_final_states(
    path: Path,
    final_positions: dict[str, np.ndarray],
) -> None:
    names = [
        "control",
        "material_damage",
        "organizational_damage",
        "material_replacement",
    ]

    fig, axes = plt.subplots(2, 2, figsize=(9, 9))
    for ax, name in zip(axes.flat, names, strict=True):
        p = final_positions[name]
        ax.scatter(p[:, 0], p[:, 1], s=8)
        ax.set_title(name.replace("_", " "))
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("Final visible states from the first replicate")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def print_summary(rows: list[dict]) -> None:
    print()
    print("ADVERSARIAL SWARM PERSISTENCE EXPERIMENT")
    print("=" * 68)
    print(
        f"{'branch':24s} {'visible':>9s} {'graph':>9s} "
        f"{'orig.mat.':>10s} {'pair W1':>9s}"
    )
    print("-" * 68)

    for r in rows:
        print(
            f"{r['branch']:24s} "
            f"{r['late_visible_similarity_mean']:9.4f} "
            f"{r['final_graph_similarity_mean']:9.4f} "
            f"{r['final_original_material_fraction_mean']:10.4f} "
            f"{r['late_pair_w1_mean']:9.4f}"
        )

    print()
    print("Interpretation target:")
    print("  material damage       -> visible organization may recover")
    print("  organizational damage -> recovery should be impaired if graph matters")
    print("  material replacement  -> original material reaches 0 while")
    print("                           visible organization remains near control")
    print()
    print("Do not treat failure to obtain that ordering as a failed script.")
    print("It is an experimental result about this construction.")


# =====================================================================
# CLI
# =====================================================================


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the Digital Life adversarial swarm persistence experiment."
    )
    p.add_argument("--particles", type=int, default=256)
    p.add_argument("--burn-in", type=int, default=10_000)
    p.add_argument("--reference-window", type=int, default=1_000)
    p.add_argument("--post-steps", type=int, default=6_000)
    p.add_argument("--sample-stride", type=int, default=20)
    p.add_argument("--replicates", type=int, default=8)
    p.add_argument("--seed", type=int, default=20260817)

    p.add_argument("--damage-fraction", type=float, default=0.30)
    p.add_argument("--rewire-fraction", type=float, default=0.30)
    p.add_argument("--damage-scale", type=float, default=2.5)

    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/digital-life/adversarial-swarm"),
    )
    p.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )
    p.add_argument(
        "--quick",
        action="store_true",
        help="Small smoke test, not suitable for book claims.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.quick:
        args.particles = min(args.particles, 96)
        args.burn_in = min(args.burn_in, 1_500)
        args.reference_window = min(args.reference_window, 300)
        args.post_steps = min(args.post_steps, 1_000)
        args.replicates = min(args.replicates, 2)

    if args.reference_window >= args.burn_in:
        raise ValueError("--reference-window must be smaller than --burn-in")

    cfg = Config(
        particles=args.particles,
        burn_in=args.burn_in,
        reference_window=args.reference_window,
        post_steps=args.post_steps,
        sample_stride=args.sample_stride,
        damage_fraction=args.damage_fraction,
        rewire_fraction=args.rewire_fraction,
        damage_scale=args.damage_scale,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    all_meta: list[dict] = []
    first_final_positions: dict[str, np.ndarray] | None = None

    for replicate in range(args.replicates):
        seed = args.seed + replicate * 100_003
        print(
            f"[{replicate + 1}/{args.replicates}] "
            f"running seed={seed} ..."
        )
        rows, meta, final_positions = run_trial(cfg, seed)
        all_rows.extend(rows)
        all_meta.append(meta)
        if first_final_positions is None:
            first_final_positions = final_positions

    summary = summarize_replicates(all_meta)

    timeseries_path = args.output_dir / "timeseries.csv"
    summary_path = args.output_dir / "summary.csv"
    metadata_path = args.output_dir / "run.json"
    similarity_figure = (
        args.figure_dir / "adversarial-swarm-persistence.png"
    )
    state_figure = (
        args.figure_dir / "adversarial-swarm-final-states.png"
    )

    write_timeseries(timeseries_path, all_rows)
    write_summary_csv(summary_path, summary)

    metadata = {
        "experiment": "adversarial_swarm_persistence",
        "claim_status": "EXPERIMENTAL",
        "config": asdict(cfg),
        "base_seed": args.seed,
        "replicates": args.replicates,
        "trials": all_meta,
        "summary": summary,
        "notes": [
            "Material IDs are deliberately causally inert.",
            "Friend/enemy relationships are causally active.",
            "Visible similarity is measured independently of both identity labels and graph identity.",
            "The experiment is a deliberately nonliving adversarial baseline.",
        ],
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    plot_similarity(similarity_figure, all_rows)
    assert first_final_positions is not None
    plot_final_states(state_figure, first_final_positions)

    print_summary(summary)
    print("Outputs:")
    print(f"  {timeseries_path}")
    print(f"  {summary_path}")
    print(f"  {metadata_path}")
    print(f"  {similarity_figure}")
    print(f"  {state_figure}")


if __name__ == "__main__":
    main()
