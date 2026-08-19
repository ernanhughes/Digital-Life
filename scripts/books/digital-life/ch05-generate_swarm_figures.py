from __future__ import annotations

"""
Generate two book figures for Chapter 05 — So We Built the Wrong Thing on Purpose.

Outputs
-------
1. ch05-canonical-dose-response.png
   A clean book-facing plot of the canonical rewiring dose-response curve.

2. ch05-control-vs-100pct-overlap.png
   A descriptive overlap plot showing late control states and late 100%-rewired
   states projected into the same control-derived 2D PCA space.

This script prefers archived canonical data if it exists locally. If the
canonical macrostate time series for the dose-response experiment is missing,
it can reconstruct it by re-running the historical canonical experiment through
the existing module:

    scripts/books/digital-life/adversarial_swarm_rewire_dose_response.py

Expected repository layout
--------------------------
repo_root/
    scripts/books/digital-life/
        adversarial_swarm_regimes.py
        adversarial_swarm_rewire_dose_response.py
    research/digital-life/adversarial-swarm-rewire-dose/
        dose_response_summary.csv
        macrostate_timeseries.csv   # optional; if absent we can rerun
    static/images/books/digital-life/

Usage
-----
python scripts/books/digital-life/generate_ch05_swarm_figures.py

Optional:
    --repo-root PATH
    --output-dir PATH
    --no-rerun
"""

import argparse
import csv
import math
import sys
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------
# Canonical values cited in the chapter. These are used as a fallback
# for the dose-response plot if the archived CSV is unavailable.
# ---------------------------------------------------------------------

CANONICAL_DOSE_RESPONSE = [
    {"dose_percent": 0, "median_distance_over_control_drift": 0.0, "fraction_above_control_drift": 0.0},
    {"dose_percent": 10, "median_distance_over_control_drift": 1.052, "fraction_above_control_drift": math.nan},
    {"dose_percent": 20, "median_distance_over_control_drift": 1.135, "fraction_above_control_drift": math.nan},
    {"dose_percent": 30, "median_distance_over_control_drift": 1.185, "fraction_above_control_drift": math.nan},
    {"dose_percent": 40, "median_distance_over_control_drift": 1.068, "fraction_above_control_drift": math.nan},
    {"dose_percent": 50, "median_distance_over_control_drift": 1.430, "fraction_above_control_drift": 0.75},
    {"dose_percent": 60, "median_distance_over_control_drift": 1.216, "fraction_above_control_drift": math.nan},
    {"dose_percent": 70, "median_distance_over_control_drift": 0.855, "fraction_above_control_drift": math.nan},
    {"dose_percent": 80, "median_distance_over_control_drift": 1.073, "fraction_above_control_drift": math.nan},
    {"dose_percent": 90, "median_distance_over_control_drift": 1.163, "fraction_above_control_drift": math.nan},
    {"dose_percent": 100, "median_distance_over_control_drift": 0.949, "fraction_above_control_drift": 0.50},
]


# ---------------------------------------------------------------------
# Repository discovery / imports
# ---------------------------------------------------------------------


def find_repo_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    candidates = [start, *start.parents]

    for root in candidates:
        scripts_dir = root / "scripts" / "books" / "digital-life"
        if scripts_dir.exists():
            return root

    raise FileNotFoundError(
        "Could not locate the Digital-Life repository root. "
        "Pass --repo-root explicitly."
    )


def import_historical_modules(repo_root: Path):
    scripts_dir = repo_root / "scripts" / "books" / "digital-life"
    sys.path.insert(0, str(scripts_dir))

    import adversarial_swarm_regimes as regimes
    import adversarial_swarm_rewire_dose_response as dose_resp

    return regimes, dose_resp


# ---------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def maybe_float(value: object) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, float):
        return value
    text = str(value).strip()
    if text == "":
        return float("nan")
    return float(text)


def normalize_dose_percent(row: dict) -> int:
    if "dose_percent" in row and str(row["dose_percent"]).strip() != "":
        return int(round(maybe_float(row["dose_percent"])))
    if "dose" in row and str(row["dose"]).strip() != "":
        dose = maybe_float(row["dose"])
        if dose <= 1.0 + 1e-12:
            return int(round(dose * 100))
        return int(round(dose))
    raise KeyError("Could not determine dose percentage from row.")


def load_dose_summary(data_dir: Path) -> list[dict]:
    summary_path = data_dir / "dose_response_summary.csv"
    if summary_path.exists():
        rows = read_csv_rows(summary_path)
        out = []
        for row in rows:
            out.append(
                {
                    "dose_percent": normalize_dose_percent(row),
                    "median_distance_over_control_drift": maybe_float(
                        row.get("median_distance_over_control_drift")
                    ),
                    "fraction_above_control_drift": maybe_float(
                        row.get("fraction_above_control_drift")
                    ),
                }
            )
        out.sort(key=lambda r: r["dose_percent"])
        return out

    return CANONICAL_DOSE_RESPONSE.copy()


def find_macrostate_timeseries(data_dir: Path) -> Path | None:
    candidates = [
        data_dir / "macrostate_timeseries.csv",
        data_dir / "macrostate_timeseries_canonical.csv",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


# ---------------------------------------------------------------------
# Canonical rerun (only if needed for overlap figure)
# ---------------------------------------------------------------------


def reconstruct_macrostate_timeseries(
    repo_root: Path,
    data_dir: Path,
    regimes,
    dose_resp,
) -> Path:
    print("Canonical macrostate time series not found.")
    print("Reconstructing it by re-running the historical canonical dose-response experiment...")
    print("This may take a while.")

    cfg = dose_resp.DoseConfig()  # historical canonical defaults
    all_rows: list[dict] = []

    for replicate in range(cfg.replicates):
        seed = cfg.base_seed + replicate * 100_003
        print(f"  running canonical replicate {replicate + 1}/{cfg.replicates} | seed={seed}")
        rows, _meta = dose_resp.run_replicate(cfg, seed)
        all_rows.extend(rows)

    data_dir.mkdir(parents=True, exist_ok=True)
    out_path = data_dir / "macrostate_timeseries.csv"

    fieldnames = list(all_rows[0].keys())
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Saved reconstructed canonical macrostate time series to: {out_path}")
    return out_path


# ---------------------------------------------------------------------
# Figure 1 — canonical dose-response
# ---------------------------------------------------------------------


def plot_canonical_dose_response(rows: list[dict], output_path: Path) -> None:
    rows = sorted(rows, key=lambda r: r["dose_percent"])
    x = np.asarray([r["dose_percent"] for r in rows], dtype=float)
    y = np.asarray(
        [r["median_distance_over_control_drift"] for r in rows],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(x, y, marker="o", linewidth=2)

    ax.axhline(
        1.0,
        linestyle="--",
        linewidth=1.5,
        label="ordinary variation",
    )

    # Highlight the 50% episode because that is the interpretive pivot.
    if 50 in set(int(v) for v in x):
        i = list(int(v) for v in x).index(50)
        ax.annotate(
            "50%: isolated criterion crossing",
            xy=(x[i], y[i]),
            xytext=(x[i] + 7, y[i] + 0.12),
            arrowprops=dict(arrowstyle="->"),
        )

    ax.set_title("Canonical rewiring dose-response")
    ax.set_xlabel("Relationship graph rewired (%)")
    ax.set_ylabel("Median normalized regime shift")
    ax.set_xticks(x)
    ax.set_xlim(min(x) - 2, max(x) + 2)

    y_top = max(1.6, float(np.nanmax(y)) + 0.15)
    ax.set_ylim(0.0, y_top)

    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


# ---------------------------------------------------------------------
# Figure 2 — control vs 100% rewired overlap
# ---------------------------------------------------------------------


def late_rows_by_seed(rows: list[dict], target_dose_percent: int) -> list[dict]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        if normalize_dose_percent(row) == target_dose_percent:
            grouped[int(maybe_float(row["seed"]))].append(row)

    out: list[dict] = []
    for seed, seed_rows in grouped.items():
        seed_rows.sort(key=lambda r: maybe_float(r["step"]))
        start = len(seed_rows) // 2
        out.extend(seed_rows[start:])
    return out


def pca_fit_2d(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    xc = x - mean
    _u, _s, vt = np.linalg.svd(xc, full_matrices=False)
    components = vt[:2]
    return mean, components


def pca_transform(x: np.ndarray, mean: np.ndarray, components: np.ndarray) -> np.ndarray:
    return (x - mean) @ components.T


def plot_overlap_from_macrostate_timeseries(
    csv_path: Path,
    output_path: Path,
    regimes,
) -> None:
    rows = read_csv_rows(csv_path)

    control_rows = late_rows_by_seed(rows, 0)
    rewired_rows = late_rows_by_seed(rows, 100)

    if not control_rows or not rewired_rows:
        raise RuntimeError(
            "Could not find both 0% and 100% dose branches in the macrostate time series."
        )

    feature_names = list(regimes.FEATURE_NAMES)

    def matrix(selected_rows: list[dict]) -> np.ndarray:
        return np.asarray(
            [
                [maybe_float(row[name]) for name in feature_names]
                for row in selected_rows
            ],
            dtype=np.float64,
        )

    control_raw = matrix(control_rows)
    rewired_raw = matrix(rewired_rows)

    standardizer = regimes.fit_standardizer(control_raw)
    control_std = standardizer.transform(control_raw)
    rewired_std = standardizer.transform(rewired_raw)

    pca_mean, pca_components = pca_fit_2d(control_std)
    control_xy = pca_transform(control_std, pca_mean, pca_components)
    rewired_xy = pca_transform(rewired_std, pca_mean, pca_components)

    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    ax.scatter(
        control_xy[:, 0],
        control_xy[:, 1],
        alpha=0.45,
        s=18,
        label="late control states",
    )
    ax.scatter(
        rewired_xy[:, 0],
        rewired_xy[:, 1],
        alpha=0.45,
        s=18,
        label="late 100% rewired states",
    )

    ax.set_title("Control vs 100% rewired overlap in control-derived PCA space")
    ax.set_xlabel("PC1 (control-derived)")
    ax.set_ylabel("PC2 (control-derived)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate Chapter 05 swarm figures."
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the Digital-Life repository root.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory to save the generated figures. "
            "Default: repo_root/static/images/books/digital-life"
        ),
    )
    p.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help=(
            "Directory containing the canonical archived dose-response data. "
            "Default: repo_root/research/digital-life/adversarial-swarm-rewire-dose"
        ),
    )
    p.add_argument(
        "--no-rerun",
        action="store_true",
        help=(
            "Do not reconstruct canonical macrostate time series if it is missing; "
            "fail instead."
        ),
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo_root / "static" / "images" / "books" / "digital-life"
    )
    data_dir = (
        args.data_dir.resolve()
        if args.data_dir
        else repo_root / "research" / "digital-life" / "adversarial-swarm-rewire-dose"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    regimes, dose_resp = import_historical_modules(repo_root)

    dose_rows = load_dose_summary(data_dir)

    dose_fig = output_dir / "ch05-canonical-dose-response.png"
    overlap_fig = output_dir / "ch05-control-vs-100pct-overlap.png"

    plot_canonical_dose_response(dose_rows, dose_fig)

    macrostate_csv = find_macrostate_timeseries(data_dir)
    if macrostate_csv is None:
        if args.no_rerun:
            raise FileNotFoundError(
                "Canonical macrostate time series not found and --no-rerun was set."
            )
        macrostate_csv = reconstruct_macrostate_timeseries(
            repo_root=repo_root,
            data_dir=data_dir,
            regimes=regimes,
            dose_resp=dose_resp,
        )

    plot_overlap_from_macrostate_timeseries(
        csv_path=macrostate_csv,
        output_path=overlap_fig,
        regimes=regimes,
    )

    print()
    print("Generated figures:")
    print(f"  {dose_fig}")
    print(f"  {overlap_fig}")


if __name__ == "__main__":
    main()
