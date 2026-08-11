from __future__ import annotations

"""
Create a full-width animated localized continuous cellular automaton GIF.

This is a lightweight Lenia-style continuous CA intended for chapter visuals.
It produces a smooth, creature-like localized pattern with visible deformation and
locomotion on a dark neutral background.

Output:
    static/images/books/digital-life/ch01-lenia-organism.gif

Requirements:
    pip install numpy matplotlib pillow scipy

Run:
    python scripts/books/digital-life/ch01_lenia_animation.py
"""

import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt

OUT = Path("static/images/books/digital-life/ch01-lenia-organism.gif")


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

    # asymmetric localized seed to encourage drift / deformation
    world += blob(-0.05, 0.0, 0.10, 0.07, 0.75)
    world += blob(0.08, 0.0, 0.07, 0.05, 0.70)
    world += blob(0.00, -0.06, 0.05, 0.03, 0.40)
    world += blob(-0.12, 0.04, 0.04, 0.03, 0.22)
    world += 0.005 * np.random.default_rng(5).random(world.shape)
    world = np.clip(world, 0.0, 1.0)
    return world


def shift_fractional(img: np.ndarray, dx: float, dy: float) -> np.ndarray:
    # Fourier shift for smooth subpixel transport
    ny, nx = img.shape
    fy = np.fft.fftfreq(ny)
    fx = np.fft.fftfreq(nx)
    phase = np.exp(-2j * np.pi * (fy[:, None] * dy + fx[None, :] * dx))
    shifted = np.fft.ifft2(np.fft.fft2(img) * phase).real
    return shifted.astype(np.float32)


def simulate(steps: int = 220, dt: float = 0.18) -> list[np.ndarray]:
    world = init_world()
    kernel = gaussian_kernel(41, 7.0)
    frames = []

    for t in range(steps):
        potential = fftconvolve(world, kernel, mode="same")
        g = growth(potential, mu=0.165 + 0.004 * math.sin(t * 0.05), sigma=0.034)
        world = np.clip(world + dt * g, 0.0, 1.0)

        # Add a tiny directional transport based on internal asymmetry to make the
        # localized pattern visibly move while keeping the field mechanism simple.
        gx = np.gradient(world, axis=1)
        gy = np.gradient(world, axis=0)
        drift_x = float(np.mean(gx * world) * -120.0)
        drift_y = float(np.mean(gy * world) * -40.0)
        world = shift_fractional(world, drift_x, drift_y)
        world = np.clip(world, 0.0, 1.0)

        if t > 20 and t % 3 == 0:
            frames.append(world.copy())

    return frames


def render_frames(fields: list[np.ndarray]) -> list[Image.Image]:
    rendered: list[Image.Image] = []
    dpi = 140
    width_inches = 10.5
    height_inches = 5.8

    for field in fields:
        fig = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(field, cmap="magma", interpolation="bilinear", vmin=0, vmax=1)
        ax.set_axis_off()
        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        # Render directly to memory. Keep frames in RGB here; creating a separate
        # adaptive palette for every frame can make Pillow fail when saving an
        # animated GIF with "invalid palette size".
        from io import BytesIO

        buffer = BytesIO()
        fig.savefig(
            buffer,
            format="png",
            facecolor=fig.get_facecolor(),
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.close(fig)
        buffer.seek(0)

        with Image.open(buffer) as image:
            rendered.append(image.convert("RGB").copy())

    return rendered


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = simulate()
    frames = render_frames(fields)
    if not frames:
        raise RuntimeError("No frames rendered")

    # Build ONE shared 256-colour palette for the whole animation. This avoids
    # Pillow's multi-frame palette mismatch on some recent Pillow versions.
    palette_source = frames[0].quantize(
        colors=256,
        method=Image.Quantize.MEDIANCUT,
    )

    gif_frames = [
        frame.quantize(
            palette=palette_source,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        for frame in frames
    ]

    gif_frames[0].save(
        OUT,
        save_all=True,
        append_images=gif_frames[1:],
        duration=70,
        loop=0,
        disposal=2,
        optimize=False,
    )
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
