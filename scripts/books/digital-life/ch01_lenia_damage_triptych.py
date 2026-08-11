from __future__ import annotations

"""
Create a before -> perturbation -> after figure for a localized continuous CA.

This script simulates a small Lenia-style continuous cellular automaton,
records a stable-ish pattern, applies a visible perturbation, then continues
simulation and captures a later frame.

Output:
    static/images/books/digital-life/ch01-lenia-damage-triptych.png

Requirements:
    pip install numpy matplotlib pillow scipy

Run:
    python scripts/books/digital-life/ch01_lenia_damage_triptych.py
"""

import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt

OUT = Path("static/images/books/digital-life/ch01-lenia-damage-triptych.png")


def gaussian_kernel(size: int = 33, sigma: float = 6.0) -> np.ndarray:
    ax = np.arange(-(size // 2), size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    k = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    k /= k.sum()
    return k


def growth(u: np.ndarray, mu: float = 0.17, sigma: float = 0.035) -> np.ndarray:
    return 2.0 * np.exp(-((u - mu) ** 2) / (2 * sigma**2)) - 1.0


def init_world(n: int = 220) -> np.ndarray:
    x = np.linspace(-1, 1, n)
    y = np.linspace(-1, 1, n)
    xx, yy = np.meshgrid(x, y)

    world = np.zeros((n, n), dtype=np.float32)

    def blob(cx, cy, sx, sy, amp=1.0):
        return amp * np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2) / 2)

    world += blob(-0.05, 0.0, 0.10, 0.07, 0.75)
    world += blob(0.08, 0.0, 0.07, 0.05, 0.70)
    world += blob(0.00, -0.06, 0.05, 0.03, 0.40)
    world += blob(-0.12, 0.04, 0.04, 0.03, 0.22)
    world += 0.004 * np.random.default_rng(5).random(world.shape)
    return np.clip(world, 0.0, 1.0)


def shift_fractional(img: np.ndarray, dx: float, dy: float) -> np.ndarray:
    ny, nx = img.shape
    fy = np.fft.fftfreq(ny)
    fx = np.fft.fftfreq(nx)
    phase = np.exp(-2j * np.pi * (fy[:, None] * dy + fx[None, :] * dx))
    shifted = np.fft.ifft2(np.fft.fft2(img) * phase).real
    return shifted.astype(np.float32)


def step(world: np.ndarray, kernel: np.ndarray, t: int, dt: float = 0.18) -> np.ndarray:
    potential = fftconvolve(world, kernel, mode="same")
    g = growth(potential, mu=0.165 + 0.004 * math.sin(t * 0.05), sigma=0.034)
    world = np.clip(world + dt * g, 0.0, 1.0)
    gx = np.gradient(world, axis=1)
    gy = np.gradient(world, axis=0)
    drift_x = float(np.mean(gx * world) * -120.0)
    drift_y = float(np.mean(gy * world) * -40.0)
    world = shift_fractional(world, drift_x, drift_y)
    return np.clip(world, 0.0, 1.0)


def perturb(world: np.ndarray) -> np.ndarray:
    h, w = world.shape
    yy, xx = np.ogrid[:h, :w]
    cx, cy = int(w * 0.55), int(h * 0.47)
    rx, ry = int(w * 0.09), int(h * 0.06)
    mask = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
    damaged = world.copy()
    damaged[mask] *= 0.0
    return damaged


def render_panel(ax, field: np.ndarray, label: str) -> None:
    ax.imshow(field, cmap="magma", interpolation="bilinear", vmin=0, vmax=1)
    ax.set_axis_off()
    ax.text(
        0.02,
        0.04,
        label,
        transform=ax.transAxes,
        fontsize=13,
        color="white",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=(0, 0, 0, 0.45), edgecolor="none"),
    )


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    kernel = gaussian_kernel(41, 7.0)
    world = init_world()

    before = None
    damaged = None
    after = None

    for t in range(90):
        world = step(world, kernel, t)
    before = world.copy()

    damaged = perturb(before)
    world = damaged.copy()

    for t in range(90, 190):
        world = step(world, kernel, t)
    after = world.copy()

    fig = plt.figure(figsize=(12.0, 4.2), dpi=160)
    axes = [fig.add_subplot(1, 3, i + 1) for i in range(3)]
    fig.patch.set_facecolor("#111111")

    render_panel(axes[0], before, "t = 0")
    render_panel(axes[1], damaged, "perturbation")
    render_panel(axes[2], after, "t = N")

    fig.subplots_adjust(left=0.015, right=0.985, top=0.98, bottom=0.02, wspace=0.04)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
