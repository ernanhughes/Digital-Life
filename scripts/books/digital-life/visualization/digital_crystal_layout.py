"""Hex lattice layout helpers used by Digital Crystal visualizations."""

from __future__ import annotations

import math
from typing import Iterable, Tuple

Cell = Tuple[int, int]


def axial_to_xy(cell: Cell, scale: float = 1.0) -> tuple[float, float]:
    q, r = cell
    return scale * math.sqrt(3.0) * (q + r / 2.0), scale * 1.5 * r


def hex_vertices(cell: Cell, radius: float = 0.92, scale: float = 1.0) -> list[tuple[float, float]]:
    cx, cy = axial_to_xy(cell, scale)
    return [
        (
            cx + radius * scale * math.cos(math.radians(60 * i + 30)),
            cy + radius * scale * math.sin(math.radians(60 * i + 30)),
        )
        for i in range(6)
    ]


def bounds(cells: Iterable[Cell], scale: float = 1.0, pad: float = 2.0) -> tuple[float, float, float, float]:
    pts = [axial_to_xy(c, scale) for c in cells]
    if not pts:
        return -1, 1, -1, 1
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad

