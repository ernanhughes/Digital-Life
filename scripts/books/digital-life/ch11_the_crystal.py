#!/usr/bin/env python3
"""
Digital Life 11: The Crystal
Generate the visual assets for the substrate-first crystal chapter.

Outputs:
    static/images/books/digital-life/ch11-crystal-growth.gif
    static/images/books/digital-life/ch11-crystal-growth-curve.png
    static/images/books/digital-life/ch11-crystal-damage-triptych.png
    static/images/books/digital-life/ch11-crystal-defects.png
    static/images/books/digital-life/ch11-crystal-collision.gif
    static/images/books/digital-life/ch11-crystal-collision-ancestry.png

Dependencies:
    pip install numpy matplotlib pillow
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter
from matplotlib.patches import RegularPolygon

Coord = Tuple[int, int]

HEX_DIRECTIONS: Tuple[Coord, ...] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)


def neighbors(cell: Coord) -> Iterable[Coord]:
    q, r = cell
    for dq, dr in HEX_DIRECTIONS:
        yield q + dq, r + dr


def hex_distance(a: Coord, b: Coord = (0, 0)) -> int:
    aq, ar = a
    bq, br = b

    ax, az = aq, ar
    ay = -ax - az

    bx, bz = bq, br
    by = -bx - bz

    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def axial_to_xy(cell: Coord) -> Tuple[float, float]:
    q, r = cell
    x = math.sqrt(3.0) * (q + r / 2.0)
    y = 1.5 * r
    return x, y


def grow_once(
    occupied: Set[Coord],
    *,
    blocked: Optional[Set[Coord]] = None,
    min_neighbors: int = 1,
    allowed_counts: Optional[Set[int]] = None,
) -> Set[Coord]:
    blocked = blocked or set()
    candidate_counts: Dict[Coord, int] = {}

    for cell in occupied:
        for nxt in neighbors(cell):
            if nxt in occupied or nxt in blocked:
                continue
            candidate_counts[nxt] = candidate_counts.get(nxt, 0) + 1

    born: Set[Coord] = set()

    for cell, count in candidate_counts.items():
        if allowed_counts is not None:
            if count in allowed_counts:
                born.add(cell)
        elif count >= min_neighbors:
            born.add(cell)

    return occupied | born


def run_growth(
    generations: int,
    *,
    seeds: Sequence[Coord] = ((0, 0),),
    blocked: Optional[Set[Coord]] = None,
    min_neighbors: int = 1,
    allowed_counts: Optional[Set[int]] = None,
) -> List[Set[Coord]]:
    occupied = set(seeds)
    history = [set(occupied)]

    for _ in range(generations):
        occupied = grow_once(
            occupied,
            blocked=blocked,
            min_neighbors=min_neighbors,
            allowed_counts=allowed_counts,
        )
        history.append(set(occupied))

    return history


def draw_hex_cells(
    ax,
    cells: Iterable[Coord],
    *,
    radius: float = 0.95,
    edgecolor=None,
    linewidth: float = 0.35,
    alpha: float = 1.0,
) -> None:
    for cell in cells:
        x, y = axial_to_xy(cell)
        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=radius,
            orientation=math.radians(30),
            fill=True,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
        )
        ax.add_patch(patch)


def draw_hex_outline(
    ax,
    cells: Iterable[Coord],
    *,
    radius: float = 0.95,
    linewidth: float = 1.5,
) -> None:
    for cell in cells:
        x, y = axial_to_xy(cell)
        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=radius,
            orientation=math.radians(30),
            fill=False,
            linewidth=linewidth,
        )
        ax.add_patch(patch)


def set_limits(ax, cells: Iterable[Coord], padding: float = 2.5) -> None:
    pts = [axial_to_xy(c) for c in cells]

    if not pts:
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
    else:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.set_xlim(min(xs) - padding, max(xs) + padding)
        ax.set_ylim(min(ys) - padding, max(ys) + padding)

    ax.set_aspect("equal")
    ax.axis("off")


def save_growth_gif(out_dir: Path, frames: int = 18, fps: int = 4) -> None:
    history = run_growth(frames)
    all_cells = history[-1]

    fig, ax = plt.subplots(figsize=(7, 7))
    writer = PillowWriter(fps=fps)

    path = out_dir / "ch11-crystal-growth.gif"
    with writer.saving(fig, path, dpi=110):
        for t, state in enumerate(history):
            ax.clear()
            draw_hex_cells(ax, state)
            set_limits(ax, all_cells, padding=3.0)
            ax.set_title(f"generation {t}")
            writer.grab_frame()

    plt.close(fig)


def save_growth_curve(out_dir: Path, generations: int = 40) -> None:
    history = run_growth(generations)

    measured = np.array([len(state) for state in history], dtype=float)
    r = np.arange(generations + 1)
    theoretical = 1 + 3 * r * (r + 1)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(r, measured, label="measured occupied cells")
    ax.plot(r, theoretical, linestyle="--", label=r"$1 + 3r(r+1)$")
    ax.set_xlabel("generation")
    ax.set_ylabel("occupied cells")
    ax.set_title("Crystal growth follows the hexagonal-ball count")
    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_dir / "ch11-crystal-growth-curve.png", dpi=180)
    plt.close(fig)


def save_damage_triptych(out_dir: Path) -> None:
    before = run_growth(15)[-1]

    damage_region = {
        cell
        for cell in before
        if hex_distance(cell, (2, -1)) <= 2
    }

    damaged = before - damage_region

    later = set(damaged)
    for _ in range(5):
        later = grow_once(later)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    panels = [
        ("t = 0", before),
        ("perturbation", damaged),
        ("t = N", later),
    ]

    frame = before | later

    for ax, (title, state) in zip(axes, panels):
        draw_hex_cells(ax, state)
        set_limits(ax, frame, padding=2.5)
        ax.set_title(title)

    fig.suptitle("Interior removal followed by unchanged growth dynamics")
    fig.tight_layout()
    fig.savefig(out_dir / "ch11-crystal-damage-triptych.png", dpi=180)
    plt.close(fig)


def save_defects_figure(out_dir: Path) -> None:
    blocked = {
        (2, -1),
        (3, -1),
        (3, -2),
        (0, 4),
        (-1, 4),
        (-4, 1),
    }

    history = run_growth(18, blocked=blocked)
    times = [4, 9, 18]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    frame = history[-1] | blocked

    for ax, t in zip(axes, times):
        draw_hex_cells(ax, history[t])
        draw_hex_outline(ax, blocked)
        set_limits(ax, frame, padding=2.5)
        ax.set_title(f"generation {t}")

    fig.suptitle("Growth around persistent defects")
    fig.tight_layout()
    fig.savefig(out_dir / "ch11-crystal-defects.png", dpi=180)
    plt.close(fig)


@dataclass(frozen=True)
class ProvenanceCell:
    owner: str
    birth_time: int


def collision_step(
    state: Dict[Coord, ProvenanceCell],
    seeds: Dict[str, Coord],
    t: int,
) -> Dict[Coord, ProvenanceCell]:
    proposals: Dict[Coord, Set[str]] = {}

    for cell, meta in state.items():
        for nxt in neighbors(cell):
            if nxt in state:
                continue
            proposals.setdefault(nxt, set()).add(meta.owner)

    new_state = dict(state)

    for cell, owners in proposals.items():
        owners = set(owners)

        if len(owners) == 1:
            owner = next(iter(owners))
        else:
            ranked = sorted(
                (hex_distance(cell, seeds[o]), o)
                for o in owners
                if o in seeds
            )
            if len(ranked) >= 2 and ranked[0][0] == ranked[1][0]:
                owner = "M"
            else:
                owner = ranked[0][1] if ranked else "M"

        new_state[cell] = ProvenanceCell(owner=owner, birth_time=t)

    return new_state


def run_collision(generations: int = 16):
    seeds = {"A": (-9, 0), "B": (9, 0)}

    state = {
        seeds["A"]: ProvenanceCell("A", 0),
        seeds["B"]: ProvenanceCell("B", 0),
    }

    history = [dict(state)]

    for t in range(1, generations + 1):
        state = collision_step(state, seeds, t)
        history.append(dict(state))

    return seeds, history


def draw_collision_state(ax, state: Dict[Coord, ProvenanceCell], *, provenance: bool) -> None:
    if not provenance:
        draw_hex_cells(ax, state.keys())
        return

    groups: Dict[str, List[Coord]] = {}
    for cell, meta in state.items():
        groups.setdefault(meta.owner, []).append(cell)

    for owner in ("A", "B", "M"):
        cells = groups.get(owner, [])
        if not cells:
            continue

        points = [axial_to_xy(c) for c in cells]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        ax.scatter(
            xs,
            ys,
            s=46,
            marker="h",
            alpha=0.9,
            label=owner,
        )


def save_collision_gif(out_dir: Path, generations: int = 16, fps: int = 4) -> None:
    _, history = run_collision(generations)
    frame = set(history[-1].keys())

    fig, ax = plt.subplots(figsize=(9, 5.5))
    writer = PillowWriter(fps=fps)

    path = out_dir / "ch11-crystal-collision.gif"

    with writer.saving(fig, path, dpi=110):
        for t, state in enumerate(history):
            ax.clear()
            draw_collision_state(ax, state, provenance=False)
            set_limits(ax, frame, padding=3.0)
            ax.set_title(f"generation {t}")
            writer.grab_frame()

    plt.close(fig)


def save_collision_ancestry(out_dir: Path, generations: int = 16) -> None:
    _, history = run_collision(generations)
    state = history[-1]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))

    draw_collision_state(axes[0], state, provenance=False)
    set_limits(axes[0], state.keys(), padding=2.5)
    axes[0].set_title("state view")

    draw_collision_state(axes[1], state, provenance=True)
    set_limits(axes[1], state.keys(), padding=2.5)
    axes[1].set_title("provenance view")
    axes[1].legend(title="ancestry")

    fig.suptitle("One merged state can contain multiple growth histories")
    fig.tight_layout()
    fig.savefig(out_dir / "ch11-crystal-collision-ancestry.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("static/images/books/digital-life"),
        help="Output directory.",
    )
    parser.add_argument("--growth-frames", type=int, default=18)
    parser.add_argument("--collision-generations", type=int, default=16)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating Digital Life 11 crystal visuals...")

    save_growth_gif(args.out_dir, frames=args.growth_frames)
    print("  ✓ ch11-crystal-growth.gif")

    save_growth_curve(args.out_dir)
    print("  ✓ ch11-crystal-growth-curve.png")

    save_damage_triptych(args.out_dir)
    print("  ✓ ch11-crystal-damage-triptych.png")

    save_defects_figure(args.out_dir)
    print("  ✓ ch11-crystal-defects.png")

    save_collision_gif(
        args.out_dir,
        generations=args.collision_generations,
    )
    print("  ✓ ch11-crystal-collision.gif")

    save_collision_ancestry(
        args.out_dir,
        generations=args.collision_generations,
    )
    print("  ✓ ch11-crystal-collision-ancestry.png")

    print(f"\nSaved all outputs to: {args.out_dir}")


if __name__ == "__main__":
    main()
