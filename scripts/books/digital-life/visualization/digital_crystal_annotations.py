"""Small annotation helpers for static Digital Crystal figures."""

from __future__ import annotations

from .digital_crystal_palettes import COLORS


def label(ax, text: str, xy, *, color: str = "text", size: int = 10, weight: str = "normal"):
    ax.text(
        xy[0],
        xy[1],
        text,
        color=COLORS[color],
        fontsize=size,
        fontweight=weight,
        ha="center",
        va="center",
    )


def corner_note(ax, text: str, *, loc: str = "upper left", size: int = 9):
    x = 0.02 if "left" in loc else 0.98
    y = 0.96 if "upper" in loc else 0.04
    ha = "left" if "left" in loc else "right"
    va = "top" if "upper" in loc else "bottom"
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        color=COLORS["muted"],
        fontsize=size,
        ha=ha,
        va=va,
        linespacing=1.25,
    )

