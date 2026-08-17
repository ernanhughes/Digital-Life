from __future__ import annotations

"""
Digital Life — Experiment 3: organizational damage dose-response

Question
--------
Experiment 2 found that 30% rewiring of the friend/enemy relationship graph
usually did NOT move the swarm farther from its matched control than ordinary
control self-drift.

This experiment asks:

    How much organizational damage is required before the long-run
    macrostate distribution leaves the system's ordinary dynamical regime?

Sweep:
    0%, 10%, 20%, ..., 100% exact relationship rewiring.

For each seed:
    1. build one swarm;
    2. burn it in once;
    3. clone the exact same checkpoint into every dose branch;
    4. rewire the requested fraction of friend/enemy assignments;
    5. evolve every branch for the same post-intervention horizon;
    6. compare each late-state macrostate distribution with the 0% control;
    7. normalize that distance by ordinary temporal drift inside the 0% control.

This script reuses the microscopic dynamics and macrostate features from
Experiments 1 and 2.

Frozen operational break criterion
----------------------------------
A dose is called "regime-breaking" only if BOTH are true:

    median normalized shift > 1.0
    AND
    >= 75% of replicates exceed ordinary control drift

This is an operational criterion, not an ontological definition.

Dependencies
------------
    pip install numpy scipy matplotlib

Expected beside this script
---------------------------
    adversarial_swarm_persistence.py
    adversarial_swarm_regimes.py

Run
---
    python scripts/books/digital-life/adversarial_swarm_rewire_dose_response.py

Quick smoke test
----------------
    python scripts/books/digital-life/adversarial_swarm_rewire_dose_response.py --quick
"""

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import adversarial_swarm_persistence as swarm
import adversarial_swarm_regimes as regimes


EPS = 1e-12


@dataclass(frozen=True)
class DoseConfig:
    particles: int = 256
    burn_in: int = 10_000
    post_steps: int = 12_000
    sample_stride: int = 20
    replicates: int = 8
    base_seed: int = 20260817
    doses: tuple[float, ...] = (
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 0.9, 1.0,
    )
    control_blocks: int = 6
    max_energy_samples: int = 400
    late_fraction: float = 0.50
    bootstrap_iterations: int = 10_000
    break_median_ratio: float = 1.0
    break_fraction_above_drift: float = 0.75


def _draw_other(
    rng: np.random.Generator,
    n: int,
    i: int,
    forbidden: tuple[int, ...] = (),
) -> int:
    forbidden_set = {int(i), *(int(x) for x in forbidden)}
    choices = np.asarray(
        [x for x in range(n) if x not in forbidden_set],
        dtype=np.int64,
    )
    return int(rng.choice(choices))


def rewire_exact_fraction(
    state: swarm.SwarmState,
    fraction: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if not (0.0 <= fraction <= 1.0):
        raise ValueError("fraction must be in [0, 1]")

    n = len(state.friend)
    n_rewire = int(round(fraction * n))
    if n_rewire == 0:
        return np.empty(0, dtype=np.int64)

    idx = rng.choice(n, size=n_rewire, replace=False)

    for raw_i in idx:
        i = int(raw_i)
        old_friend = int(state.friend[i])
        old_enemy = int(state.enemy[i])

        new_friend = _draw_other(
            rng,
            n,
            i,
            forbidden=(old_friend,),
        )
        new_enemy = _draw_other(
            rng,
            n,
            i,
            forbidden=(new_friend, old_enemy),
        )

        state.friend[i] = new_friend
        state.enemy[i] = new_enemy

    return idx


def graph_similarity(
    state: swarm.SwarmState,
    checkpoint: swarm.SwarmState,
) -> float:
    return float(
        0.5
        * (
            np.mean(state.friend == checkpoint.friend)
            + np.mean(state.enemy == checkpoint.enemy)
        )
    )


def make_world_config(cfg: DoseConfig) -> swarm.Config:
    return swarm.Config(
        particles=cfg.particles,
        burn_in=cfg.burn_in,
        reference_window=min(1_000, max(100, cfg.burn_in // 5)),
        post_steps=cfg.post_steps,
        sample_stride=cfg.sample_stride,
    )


def dose_name(dose: float) -> str:
    return f"{int(round(dose * 100)):03d}"


def run_replicate(
    cfg: DoseConfig,
    seed: int,
) -> tuple[list[dict], dict]:
    world_cfg = make_world_config(cfg)
    rng = np.random.default_rng(seed)
    state = swarm.make_state(world_cfg, rng)

    for _ in range(cfg.burn_in):
        swarm.step(state, world_cfg)

    checkpoint = state.clone()

    branches: dict[float, swarm.SwarmState] = {
        dose: checkpoint.clone()
        for dose in cfg.doses
    }

    rewired_nodes: dict[float, int] = {}

    for dose in cfg.doses:
        if dose <= 0.0:
            rewired_nodes[dose] = 0
            continue

        idx = rewire_exact_fraction(
            branches[dose],
            dose,
            np.random.default_rng(
                seed + 50_000 + int(round(dose * 10_000))
            ),
        )
        rewired_nodes[dose] = len(idx)

    rows: list[dict] = []

    def record(dose: float, t: int) -> None:
        branch = branches[dose]
        feat = regimes.macrostate_features(branch)

        row = {
            "seed": seed,
            "dose": float(dose),
            "dose_percent": int(round(dose * 100)),
            "step": t,
            "rewired_nodes": rewired_nodes[dose],
            "graph_similarity": graph_similarity(branch, checkpoint),
        }
        row.update(
            {
                name: float(value)
                for name, value in zip(
                    regimes.FEATURE_NAMES,
                    feat,
                    strict=True,
                )
            }
        )
        rows.append(row)

    for dose in cfg.doses:
        record(dose, 0)

    for t in range(1, cfg.post_steps + 1):
        for branch in branches.values():
            swarm.step(branch, world_cfg)

        if t % cfg.sample_stride == 0 or t == cfg.post_steps:
            for dose in cfg.doses:
                record(dose, t)

    meta = {
        "seed": seed,
        "samples_per_dose": sum(
            1 for r in rows if abs(float(r["dose"])) < EPS
        ),
        "actual_final_graph_similarity": {
            dose_name(dose): graph_similarity(branches[dose], checkpoint)
            for dose in cfg.doses
        },
        "rewired_nodes": {
            dose_name(dose): rewired_nodes[dose]
            for dose in cfg.doses
        },
    }
    return rows, meta


def feature_matrix(rows: list[dict]) -> np.ndarray:
    return np.asarray(
        [
            [r[name] for name in regimes.FEATURE_NAMES]
            for r in rows
        ],
        dtype=np.float64,
    )


def rows_for(
    rows: list[dict],
    seed: int,
    dose: float,
) -> list[dict]:
    return [
        r
        for r in rows
        if int(r["seed"]) == seed
        and abs(float(r["dose"]) - dose) < EPS
    ]


def control_baseline(
    control_x: np.ndarray,
    cfg: DoseConfig,
) -> dict:
    blocks = regimes.split_blocks(control_x, cfg.control_blocks)

    pair_distances: list[float] = []
    adjacent_distances: list[float] = []

    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            d = regimes.energy_distance_mv(
                blocks[i],
                blocks[j],
                cfg.max_energy_samples,
            )
            pair_distances.append(d)
            if j == i + 1:
                adjacent_distances.append(d)

    first_last = regimes.energy_distance_mv(
        blocks[0],
        blocks[-1],
        cfg.max_energy_samples,
    )

    return {
        "all_pair_median": float(np.median(pair_distances)),
        "all_pair_mean": float(np.mean(pair_distances)),
        "adjacent_median": float(np.median(adjacent_distances)),
        "adjacent_mean": float(np.mean(adjacent_distances)),
        "first_last": float(first_last),
    }


def analyse_seed(
    all_rows: list[dict],
    seed: int,
    cfg: DoseConfig,
    standardizer: regimes.Standardizer,
) -> tuple[list[dict], dict]:
    control_rows = rows_for(all_rows, seed, 0.0)
    control_x = standardizer.transform(feature_matrix(control_rows))

    baseline = control_baseline(control_x, cfg)
    drift = max(baseline["all_pair_median"], EPS)

    late_control = regimes.late_slice(
        control_x,
        cfg.late_fraction,
    )

    result_rows: list[dict] = []

    for dose in cfg.doses:
        branch_rows = rows_for(all_rows, seed, dose)
        branch_x = standardizer.transform(feature_matrix(branch_rows))
        late_branch = regimes.late_slice(
            branch_x,
            cfg.late_fraction,
        )

        if dose == 0.0:
            distance = 0.0
            ratio = 0.0
        else:
            distance = regimes.energy_distance_mv(
                late_branch,
                late_control,
                cfg.max_energy_samples,
            )
            ratio = distance / drift

        result_rows.append(
            {
                "seed": seed,
                "dose": float(dose),
                "dose_percent": int(round(dose * 100)),
                "late_energy_distance_to_control": float(distance),
                "control_drift_median": float(drift),
                "distance_over_control_drift": float(ratio),
                "final_graph_similarity": float(
                    branch_rows[-1]["graph_similarity"]
                ),
            }
        )

    return result_rows, baseline


def bootstrap_median_ci(
    values: np.ndarray,
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    values = np.asarray(values, dtype=np.float64)
    if len(values) == 0:
        return float("nan"), float("nan")
    if len(values) == 1:
        return float(values[0]), float(values[0])

    rng = np.random.default_rng(seed)
    medians = np.empty(iterations, dtype=np.float64)

    for i in range(iterations):
        sample = rng.choice(values, size=len(values), replace=True)
        medians[i] = np.median(sample)

    lo, hi = np.quantile(medians, [0.025, 0.975])
    return float(lo), float(hi)


def summarize_doses(
    per_seed_rows: list[dict],
    cfg: DoseConfig,
) -> list[dict]:
    out: list[dict] = []

    for dose in cfg.doses:
        subset = [
            r
            for r in per_seed_rows
            if abs(float(r["dose"]) - dose) < EPS
        ]

        ratios = np.asarray(
            [float(r["distance_over_control_drift"]) for r in subset],
            dtype=np.float64,
        )
        distances = np.asarray(
            [float(r["late_energy_distance_to_control"]) for r in subset],
            dtype=np.float64,
        )
        graph_sim = np.asarray(
            [float(r["final_graph_similarity"]) for r in subset],
            dtype=np.float64,
        )

        ci_lo, ci_hi = bootstrap_median_ci(
            ratios,
            cfg.bootstrap_iterations,
            cfg.base_seed + 700_000 + int(round(dose * 10_000)),
        )

        fraction_above_1 = float(np.mean(ratios > 1.0))
        fraction_above_2 = float(np.mean(ratios > 2.0))

        regime_break = bool(
            np.median(ratios) > cfg.break_median_ratio
            and fraction_above_1 >= cfg.break_fraction_above_drift
        )

        out.append(
            {
                "dose": float(dose),
                "dose_percent": int(round(dose * 100)),
                "replicates": len(subset),
                "mean_energy_distance": float(np.mean(distances)),
                "median_energy_distance": float(np.median(distances)),
                "mean_distance_over_control_drift": float(np.mean(ratios)),
                "median_distance_over_control_drift": float(np.median(ratios)),
                "median_ratio_ci_low": ci_lo,
                "median_ratio_ci_high": ci_hi,
                "fraction_above_control_drift": fraction_above_1,
                "fraction_above_2x_control_drift": fraction_above_2,
                "mean_final_graph_similarity": float(np.mean(graph_sim)),
                "operational_regime_break": regime_break,
            }
        )

    return out


def first_break_dose(summary_rows: list[dict]) -> int | None:
    qualifying = [
        int(r["dose_percent"])
        for r in summary_rows
        if bool(r["operational_regime_break"])
    ]
    return min(qualifying) if qualifying else None


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def plot_dose_response(
    path: Path,
    summary_rows: list[dict],
) -> None:
    dose = np.asarray(
        [r["dose_percent"] for r in summary_rows],
        dtype=float,
    )
    median = np.asarray(
        [r["median_distance_over_control_drift"] for r in summary_rows],
        dtype=float,
    )
    lo = np.asarray(
        [r["median_ratio_ci_low"] for r in summary_rows],
        dtype=float,
    )
    hi = np.asarray(
        [r["median_ratio_ci_high"] for r in summary_rows],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        dose,
        median,
        marker="o",
        label="median normalized regime shift",
    )
    ax.fill_between(
        dose,
        lo,
        hi,
        alpha=0.20,
        label="bootstrap 95% interval",
    )
    ax.axhline(
        1.0,
        linestyle="--",
        linewidth=1.5,
        label="ordinary control drift",
    )
    ax.axhline(
        2.0,
        linestyle=":",
        linewidth=1.5,
        label="2× ordinary control drift",
    )

    ax.set_xlabel("Relationship graph rewired (%)")
    ax.set_ylabel("Late distribution distance / ordinary control drift")
    ax.set_title("Organizational damage dose-response")
    ax.set_xticks(dose)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_replicate_scatter(
    path: Path,
    per_seed_rows: list[dict],
) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))

    doses = sorted(
        {int(r["dose_percent"]) for r in per_seed_rows}
    )

    for dose in doses:
        vals = [
            float(r["distance_over_control_drift"])
            for r in per_seed_rows
            if int(r["dose_percent"]) == dose
        ]
        x = np.full(len(vals), float(dose))
        ax.scatter(x, vals, s=32, alpha=0.65)

    ax.axhline(
        1.0,
        linestyle="--",
        linewidth=1.5,
        label="ordinary control drift",
    )
    ax.axhline(
        2.0,
        linestyle=":",
        linewidth=1.5,
        label="2× ordinary control drift",
    )

    ax.set_xlabel("Relationship graph rewired (%)")
    ax.set_ylabel("Late distribution distance / ordinary control drift")
    ax.set_title("Independent replicate responses to organizational damage")
    ax.set_xticks(doses)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_fraction_breaking(
    path: Path,
    summary_rows: list[dict],
) -> None:
    dose = np.asarray(
        [r["dose_percent"] for r in summary_rows],
        dtype=float,
    )
    above1 = np.asarray(
        [r["fraction_above_control_drift"] for r in summary_rows]
    )
    above2 = np.asarray(
        [r["fraction_above_2x_control_drift"] for r in summary_rows]
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        dose,
        above1,
        marker="o",
        label="replicates > ordinary drift",
    )
    ax.plot(
        dose,
        above2,
        marker="o",
        label="replicates > 2× ordinary drift",
    )
    ax.axhline(
        0.75,
        linestyle="--",
        linewidth=1.5,
        label="75% break criterion",
    )

    ax.set_xlabel("Relationship graph rewired (%)")
    ax.set_ylabel("Fraction of independent replicates")
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks(dose)
    ax.set_title(
        "How consistently does rewiring move the swarm outside normal drift?"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_graph_similarity(
    path: Path,
    summary_rows: list[dict],
) -> None:
    dose = np.asarray(
        [r["dose_percent"] for r in summary_rows],
        dtype=float,
    )
    similarity = np.asarray(
        [r["mean_final_graph_similarity"] for r in summary_rows],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dose, similarity, marker="o")
    ax.set_xlabel("Requested rewiring (%)")
    ax.set_ylabel("Exact friend/enemy graph similarity to checkpoint")
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks(dose)
    ax.set_title("Actual organizational identity retained after intervention")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def print_report(
    summary_rows: list[dict],
    break_dose: int | None,
) -> None:
    print()
    print("EXPERIMENT 3 — ORGANIZATIONAL DAMAGE DOSE RESPONSE")
    print("=" * 96)

    print(
        f"{'dose':>6s} {'graph':>8s} {'median':>9s} "
        f"{'95% CI':>21s} {'> drift':>9s} {'> 2x':>8s} {'break':>7s}"
    )
    print("-" * 96)

    for r in summary_rows:
        ci = (
            f"[{r['median_ratio_ci_low']:.2f}, "
            f"{r['median_ratio_ci_high']:.2f}]"
        )
        print(
            f"{r['dose_percent']:5d}% "
            f"{r['mean_final_graph_similarity']:8.3f} "
            f"{r['median_distance_over_control_drift']:9.3f} "
            f"{ci:>21s} "
            f"{r['fraction_above_control_drift']:9.3f} "
            f"{r['fraction_above_2x_control_drift']:8.3f} "
            f"{str(r['operational_regime_break']):>7s}"
        )

    print()
    print("Frozen operational break criterion:")
    print("  median normalized shift > 1.0")
    print("  AND >= 75% of replicates exceed ordinary control drift")

    print()
    if break_dose is None:
        print(
            "RESULT STATUS: no tested rewiring dose met the operational "
            "regime-break criterion."
        )
    else:
        print(
            f"RESULT STATUS: first tested dose meeting the operational "
            f"criterion = {break_dose}%."
        )

    print()
    print("Important:")
    print(
        "  This tests robustness to exact relationship identity."
    )
    print(
        "  Failure even at 100% rewiring would not mean organization is irrelevant."
    )
    print(
        "  It would mean the exact graph is not the persistent carrier;"
    )
    print(
        "  the interaction law or coarser graph statistics may be."
    )


def parse_doses(text: str) -> tuple[float, ...]:
    values = []

    for part in text.split(","):
        part = part.strip()
        if not part:
            continue

        value = float(part)
        if value > 1.0:
            value /= 100.0

        if not (0.0 <= value <= 1.0):
            raise ValueError(
                "Each dose must be in [0,1] or [0,100] percent form."
            )

        values.append(value)

    values = sorted(set(values))

    if 0.0 not in values:
        values.insert(0, 0.0)

    return tuple(values)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Sweep relationship-graph rewiring from 0 to 100 percent "
            "and measure where the long-run macrostate regime changes."
        )
    )

    p.add_argument("--particles", type=int, default=256)
    p.add_argument("--burn-in", type=int, default=10_000)
    p.add_argument("--post-steps", type=int, default=12_000)
    p.add_argument("--sample-stride", type=int, default=20)
    p.add_argument("--replicates", type=int, default=8)
    p.add_argument("--seed", type=int, default=20260817)

    p.add_argument(
        "--doses",
        type=str,
        default="0,10,20,30,40,50,60,70,80,90,100",
    )

    p.add_argument("--control-blocks", type=int, default=6)
    p.add_argument("--late-fraction", type=float, default=0.50)
    p.add_argument("--bootstrap-iterations", type=int, default=10_000)

    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/digital-life/adversarial-swarm-rewire-dose"
        ),
    )
    p.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
    )

    p.add_argument(
        "--quick",
        action="store_true",
        help="Reduced smoke test; not suitable for book claims.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    doses = parse_doses(args.doses)

    if args.quick:
        args.particles = min(args.particles, 96)
        args.burn_in = min(args.burn_in, 1_500)
        args.post_steps = min(args.post_steps, 2_000)
        args.replicates = min(args.replicates, 2)
        args.control_blocks = min(args.control_blocks, 4)
        args.bootstrap_iterations = min(
            args.bootstrap_iterations,
            1_000,
        )

        if args.doses == "0,10,20,30,40,50,60,70,80,90,100":
            doses = (0.0, 0.3, 0.6, 1.0)

    if not (0.10 <= args.late_fraction <= 1.0):
        raise ValueError("--late-fraction must be in [0.10, 1.0]")

    cfg = DoseConfig(
        particles=args.particles,
        burn_in=args.burn_in,
        post_steps=args.post_steps,
        sample_stride=args.sample_stride,
        replicates=args.replicates,
        base_seed=args.seed,
        doses=doses,
        control_blocks=args.control_blocks,
        late_fraction=args.late_fraction,
        bootstrap_iterations=args.bootstrap_iterations,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    trial_meta: list[dict] = []

    for replicate in range(cfg.replicates):
        seed = cfg.base_seed + replicate * 100_003
        print(
            f"[{replicate + 1}/{cfg.replicates}] "
            f"running seed={seed} ..."
        )

        rows, meta = run_replicate(cfg, seed)
        all_rows.extend(rows)
        trial_meta.append(meta)

    control_rows = [
        r
        for r in all_rows
        if abs(float(r["dose"])) < EPS
    ]
    control_raw = feature_matrix(control_rows)
    standardizer = regimes.fit_standardizer(control_raw)

    per_seed_results: list[dict] = []
    baseline_by_seed: dict[str, dict] = {}

    for seed in sorted({int(r["seed"]) for r in all_rows}):
        result_rows, baseline = analyse_seed(
            all_rows,
            seed,
            cfg,
            standardizer,
        )
        per_seed_results.extend(result_rows)
        baseline_by_seed[str(seed)] = baseline

    summary_rows = summarize_doses(
        per_seed_results,
        cfg,
    )
    break_dose = first_break_dose(summary_rows)

    write_csv(
        args.output_dir / "macrostate_timeseries.csv",
        all_rows,
    )
    write_csv(
        args.output_dir / "per_seed_dose_response.csv",
        per_seed_results,
    )
    write_csv(
        args.output_dir / "dose_response_summary.csv",
        summary_rows,
    )

    metadata = {
        "experiment": "adversarial_swarm_rewire_dose_response",
        "claim_status": "EXPERIMENTAL",
        "question": (
            "How much exact friend/enemy relationship rewiring is required "
            "before the long-run macrostate distribution departs from "
            "ordinary control self-drift?"
        ),
        "config": asdict(cfg),
        "feature_names": regimes.FEATURE_NAMES,
        "standardization": {
            "fit_on": "pooled 0%-rewiring control states only",
            "mean": standardizer.mean.tolist(),
            "scale": standardizer.scale.tolist(),
        },
        "operational_break_criterion": {
            "median_distance_over_control_drift_gt": cfg.break_median_ratio,
            "fraction_replicates_above_control_drift_gte": (
                cfg.break_fraction_above_drift
            ),
            "status": "frozen before inspecting the full-run result",
        },
        "control_baseline_by_seed": baseline_by_seed,
        "dose_response_summary": summary_rows,
        "first_operational_break_dose_percent": break_dose,
        "trials": trial_meta,
        "interpretation": [
            (
                "A dose below the operational break criterion is not evidence "
                "that exact graph identity is irrelevant."
            ),
            (
                "If high rewiring doses break the regime, the curve measures "
                "robustness to exact relationship identity."
            ),
            (
                "If even 100% rewiring does not break the regime, the "
                "persistent carrier is likely coarser than exact edge identity."
            ),
            (
                "The microscopic interaction law is held fixed at every dose."
            ),
        ],
    }

    (args.output_dir / "run.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    plot_dose_response(
        args.figure_dir
        / "adversarial-swarm-rewire-dose-response.png",
        summary_rows,
    )
    plot_replicate_scatter(
        args.figure_dir
        / "adversarial-swarm-rewire-dose-replicates.png",
        per_seed_results,
    )
    plot_fraction_breaking(
        args.figure_dir
        / "adversarial-swarm-rewire-dose-fractions.png",
        summary_rows,
    )
    plot_graph_similarity(
        args.figure_dir
        / "adversarial-swarm-rewire-graph-similarity.png",
        summary_rows,
    )

    print_report(summary_rows, break_dose)

    print()
    print("Outputs:")
    for name in (
        "macrostate_timeseries.csv",
        "per_seed_dose_response.csv",
        "dose_response_summary.csv",
        "run.json",
    ):
        print(f"  {args.output_dir / name}")

    for name in (
        "adversarial-swarm-rewire-dose-response.png",
        "adversarial-swarm-rewire-dose-replicates.png",
        "adversarial-swarm-rewire-dose-fractions.png",
        "adversarial-swarm-rewire-graph-similarity.png",
    ):
        print(f"  {args.figure_dir / name}")


if __name__ == "__main__":
    main()
