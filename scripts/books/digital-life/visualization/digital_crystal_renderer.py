"""Reusable renderer for Digital Crystal lattice figures.

The renderer draws actual axial hex-cell coordinates and overlays measured or
computed chapter evidence without changing cell positions for aesthetics.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
from PIL import Image, ImageDraw, ImageFont

from .digital_crystal_layout import Cell, axial_to_xy, bounds, hex_vertices
from .digital_crystal_palettes import COLORS


def repo_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists() and (p / "content").exists():
            return p
    raise RuntimeError("Could not locate repository root")


def setup_figure(ncols: int = 1, *, width: float = 12.0, height: float = 7.0, title: str | None = None):
    fig, axes = plt.subplots(1, ncols, figsize=(width, height), facecolor=COLORS["background"])
    if ncols == 1:
        axes = [axes]
    for ax in axes:
        ax.set_facecolor(COLORS["panel"])
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    if title:
        fig.suptitle(title, color=COLORS["text"], fontsize=18, fontweight="bold", y=0.98)
    return fig, axes


def draw_cells(
    ax,
    occupied: Iterable[Cell],
    *,
    fill: str = "occupied",
    edge: str = "occupied_edge",
    alpha: float = 0.92,
    radius: float = 0.92,
    linewidth: float = 0.35,
    zorder: int = 1,
):
    patches = [Polygon(hex_vertices(c, radius=radius), closed=True) for c in occupied]
    if not patches:
        return
    collection = PatchCollection(
        patches,
        facecolor=COLORS[fill],
        edgecolor=COLORS[edge],
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_collection(collection)


def draw_outlines(ax, cells: Iterable[Cell], *, color: str = "frontier", linewidth: float = 0.7, alpha: float = 0.8):
    for c in cells:
        ax.add_patch(
            Polygon(
                hex_vertices(c, radius=0.96),
                closed=True,
                facecolor="none",
                edgecolor=COLORS[color],
                linewidth=linewidth,
                alpha=alpha,
                zorder=3,
            )
        )


def draw_markers(ax, cells: Iterable[Cell], *, color: str, size: float = 0.42, alpha: float = 0.9, zorder: int = 6):
    for c in cells:
        x, y = axial_to_xy(c)
        ax.add_patch(Circle((x, y), size, facecolor=COLORS[color], edgecolor="none", alpha=alpha, zorder=zorder))


def draw_intensity(ax, values: Mapping[Cell, float], *, color: str = "modified", max_radius: float = 0.75):
    if not values:
        return
    vmax = max(abs(v) for v in values.values()) or 1.0
    for c, v in values.items():
        x, y = axial_to_xy(c)
        a = min(0.85, 0.18 + 0.67 * abs(v) / vmax)
        r = max_radius * (0.35 + 0.65 * abs(v) / vmax)
        ax.add_patch(Circle((x, y), r, facecolor=COLORS[color], edgecolor="none", alpha=a, zorder=5))


def draw_ring(ax, center: Cell, radius_cells: int, *, color: str = "intervention", alpha: float = 0.28):
    cx, cy = axial_to_xy(center)
    ax.add_patch(
        Circle((cx, cy), radius_cells * 1.72, facecolor="none", edgecolor=COLORS[color], linewidth=1.5, alpha=alpha, zorder=4)
    )


def draw_title(ax, title: str, subtitle: str | None = None):
    ax.text(0.02, 0.98, title, transform=ax.transAxes, color=COLORS["text"], fontsize=13, fontweight="bold", va="top")
    if subtitle:
        ax.text(0.02, 0.91, subtitle, transform=ax.transAxes, color=COLORS["muted"], fontsize=9, va="top", linespacing=1.2)


def frame(ax, cells: Sequence[Cell], *, pad: float = 2.6):
    xmin, xmax, ymin, ymax = bounds(cells, pad=pad)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymax, ymin)


def save_png(fig, path: Path, *, dpi: int = 180):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def fig_to_image(fig, *, dpi: int = 150) -> Image.Image:
    fig.canvas.draw()
    width, height = fig.get_size_inches()
    fig.set_dpi(dpi)
    fig.canvas.draw()
    rgba = fig.canvas.buffer_rgba()
    image = Image.frombuffer("RGBA", fig.canvas.get_width_height(), rgba, "raw", "RGBA", 0, 1)
    result = image.copy()
    plt.close(fig)
    return result


def save_filmstrip(frames: Sequence[Image.Image], labels: Sequence[str], path: Path, *, columns: int | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not frames:
        raise ValueError("filmstrip requires at least one frame")
    columns = columns or len(frames)
    rows = (len(frames) + columns - 1) // columns
    w = max(frame.width for frame in frames)
    h = max(frame.height for frame in frames)
    label_h = 34
    canvas = Image.new("RGBA", (columns * w, rows * (h + label_h)), COLORS["background"])
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for i, frame in enumerate(frames):
        row, col = divmod(i, columns)
        x = col * w
        y = row * (h + label_h)
        canvas.alpha_composite(frame.resize((w, h)), (x, y + label_h))
        draw.text((x + 12, y + 10), labels[i], fill=COLORS["text"], font=font)
    canvas.convert("RGB").save(path)


def save_gif(frames: Sequence[Image.Image], path: Path, *, duration: int = 650):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not frames:
        raise ValueError("gif requires at least one frame")
    normalized = [frame.convert("P", palette=Image.Palette.ADAPTIVE) for frame in frames]
    normalized[0].save(
        path,
        save_all=True,
        append_images=normalized[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )


def write_provenance(path: Path, provenance: dict):
    path.with_suffix(".json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
