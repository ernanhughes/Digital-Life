from __future__ import annotations

import base64
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Published Outlier rule + seed
# ---------------------------------------------------------------------

OUTLIER_MAP = (
    "ERETQB4eHWkQ7xD4eYZosBQZFixOBHmtFeehExrKVhURLRAq"
    "GxeIlSO1JYZP6DRi69rop7TQCkvWTIag7kAS8g"
)

SEED = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 1],
    ],
    dtype=np.uint8,
)


# ---------------------------------------------------------------------
# Rule decoding
# ---------------------------------------------------------------------

def decode_map_rule(encoded: str) -> np.ndarray:
    """
    Decode the Base64 MAP rule into a 512-entry binary lookup table.

    A 3x3 binary Moore neighborhood has 2^9 = 512 possible states.
    """

    padding = "=" * ((4 - len(encoded) % 4) % 4)
    raw = base64.b64decode(encoded + padding)

    bits = np.unpackbits(
        np.frombuffer(raw, dtype=np.uint8)
    )

    if len(bits) < 512:
        raise ValueError(
            f"Expected at least 512 bits, got {len(bits)}"
        )

    return bits[:512].astype(np.uint8)


RULE = decode_map_rule(OUTLIER_MAP)


# ---------------------------------------------------------------------
# World construction
# ---------------------------------------------------------------------

def make_world(size: int = 512) -> np.ndarray:
    world = np.zeros(
        (size, size),
        dtype=np.uint8,
    )

    row = size // 2 - SEED.shape[0] // 2
    col = size // 2 - SEED.shape[1] // 2

    world[
        row:row + SEED.shape[0],
        col:col + SEED.shape[1],
    ] = SEED

    return world


# ---------------------------------------------------------------------
# Cellular automaton
# ---------------------------------------------------------------------

def outlier_step(state: np.ndarray) -> np.ndarray:
    """
    Advance one synchronous generation using periodic boundaries.

    Neighborhood weights:

        256 128  64
         32  16   8
          4   2   1
    """

    nw = np.roll(
        np.roll(state, 1, axis=0),
        1,
        axis=1,
    )

    north = np.roll(state, 1, axis=0)

    ne = np.roll(
        np.roll(state, 1, axis=0),
        -1,
        axis=1,
    )

    west = np.roll(state, 1, axis=1)
    centre = state
    east = np.roll(state, -1, axis=1)

    sw = np.roll(
        np.roll(state, -1, axis=0),
        1,
        axis=1,
    )

    south = np.roll(state, -1, axis=0)

    se = np.roll(
        np.roll(state, -1, axis=0),
        -1,
        axis=1,
    )

    neighborhood = (
          (nw.astype(np.uint16) << 8)
        | (north.astype(np.uint16) << 7)
        | (ne.astype(np.uint16) << 6)
        | (west.astype(np.uint16) << 5)
        | (centre.astype(np.uint16) << 4)
        | (east.astype(np.uint16) << 3)
        | (sw.astype(np.uint16) << 2)
        | (south.astype(np.uint16) << 1)
        | se.astype(np.uint16)
    )

    return RULE[neighborhood]


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_experiment(
    size: int = 512,
    generations: int = 5000,
    capture_every: int = 25,
):
    """
    Run Outlier and retain periodic snapshots.

    We keep the full population count at every generation but only
    store image frames periodically to avoid unnecessary memory use.
    """

    state = make_world(size)

    frames = []
    frame_times = []
    population = np.zeros(
        generations + 1,
        dtype=np.int64,
    )

    population[0] = state.sum()

    frames.append(state.copy())
    frame_times.append(0)

    for t in range(1, generations + 1):
        state = outlier_step(state)

        population[t] = state.sum()

        if t % capture_every == 0:
            frames.append(state.copy())
            frame_times.append(t)

        if t % 500 == 0:
            print(
                f"generation={t:5d} "
                f"live_cells={population[t]:8d}"
            )

    return frames, frame_times, population


# ---------------------------------------------------------------------
# Cropping helper
# ---------------------------------------------------------------------

def crop_active_region(
    state: np.ndarray,
    padding: int = 20,
    minimum_size: int = 80,
) -> np.ndarray:
    """
    Crop around all live cells while keeping enough surrounding space
    to make the dynamics readable.
    """

    positions = np.argwhere(state == 1)

    if len(positions) == 0:
        return state

    r0, c0 = positions.min(axis=0)
    r1, c1 = positions.max(axis=0)

    r0 = max(0, r0 - padding)
    c0 = max(0, c0 - padding)

    r1 = min(state.shape[0] - 1, r1 + padding)
    c1 = min(state.shape[1] - 1, c1 + padding)

    # Ensure a useful minimum viewport.
    height = r1 - r0 + 1
    width = c1 - c0 + 1

    if height < minimum_size:
        extra = minimum_size - height
        r0 = max(0, r0 - extra // 2)
        r1 = min(
            state.shape[0] - 1,
            r0 + minimum_size - 1,
        )

    if width < minimum_size:
        extra = minimum_size - width
        c0 = max(0, c0 - extra // 2)
        c1 = min(
            state.shape[1] - 1,
            c0 + minimum_size - 1,
        )

    return state[r0:r1 + 1, c0:c1 + 1]


# ---------------------------------------------------------------------
# Figure 1 — snapshot sequence
# ---------------------------------------------------------------------

def build_snapshot_figure(
    frames,
    frame_times,
):
    """
    Pick representative stages from the run.
    """

    desired_times = [
        0,
        250,
        750,
        1500,
        3000,
        5000,
    ]

    selected = []

    for target in desired_times:
        index = min(
            range(len(frame_times)),
            key=lambda i: abs(frame_times[i] - target),
        )

        selected.append(
            (
                frame_times[index],
                frames[index],
            )
        )

    # Use one common crop based on the latest selected state,
    # so visual scale remains comparable.
    final_state = selected[-1][1]

    positions = np.argwhere(final_state == 1)

    if len(positions):
        r0, c0 = positions.min(axis=0)
        r1, c1 = positions.max(axis=0)

        padding = 25

        r0 = max(0, r0 - padding)
        c0 = max(0, c0 - padding)
        r1 = min(final_state.shape[0], r1 + padding + 1)
        c1 = min(final_state.shape[1], c1 + padding + 1)
    else:
        r0 = c0 = 0
        r1, c1 = final_state.shape

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(12, 8),
    )

    for ax, (t, state) in zip(
        axes.flat,
        selected,
    ):
        ax.imshow(
            state[r0:r1, c0:c1],
            cmap="binary",
            interpolation="nearest",
            vmin=0,
            vmax=1,
        )

        ax.set_title(f"t = {t}")
        ax.axis("off")

    fig.suptitle(
        "Outlier: One Tiny Seed Under One Local Rule"
    )

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch10-outlier-snapshots.png"
    )

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 2 — population through time
# ---------------------------------------------------------------------

def build_population_plot(
    population: np.ndarray,
):
    generations = np.arange(
        len(population)
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        generations,
        population,
    )

    ax.set_title(
        "Outlier: Live Cells Through Time"
    )

    ax.set_xlabel("Generation")
    ax.set_ylabel("Live cells")

    ax.grid(alpha=0.25)

    fig.tight_layout()

    path = (
        OUTPUT_DIR
        / "ch10-outlier-population.png"
    )

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 3 — hero animation
# ---------------------------------------------------------------------

def build_growth_gif(
    frames,
    frame_times,
    fps: int = 12,
):
    """
    Render a cropped animation centered on the active region.

    The crop is fixed across the animation so that apparent motion
    isn't caused by the camera constantly rescaling.
    """

    final_state = frames[-1]

    positions = np.argwhere(
        final_state == 1
    )

    if len(positions):
        r0, c0 = positions.min(axis=0)
        r1, c1 = positions.max(axis=0)

        padding = 30

        r0 = max(0, r0 - padding)
        c0 = max(0, c0 - padding)

        r1 = min(
            final_state.shape[0],
            r1 + padding + 1,
        )

        c1 = min(
            final_state.shape[1],
            c1 + padding + 1,
        )

    else:
        r0 = c0 = 0
        r1, c1 = final_state.shape

    cropped = [
        frame[r0:r1, c0:c1]
        for frame in frames
    ]

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    image = ax.imshow(
        cropped[0],
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    ax.axis("off")

    label = ax.text(
        0.02,
        0.98,
        f"t = {frame_times[0]}",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )

    ax.set_title(
        "Outlier: Emergent Structure From a 3×3 Seed"
    )

    def update(i):
        image.set_data(cropped[i])

        label.set_text(
            f"t = {frame_times[i]}"
        )

        return image, label

    animation = FuncAnimation(
        fig,
        update,
        frames=len(cropped),
        interval=1000 / fps,
        blit=False,
    )

    path = (
        OUTPUT_DIR
        / "ch10-outlier-growth.gif"
    )

    animation.save(
        path,
        writer=PillowWriter(fps=fps),
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    frames, frame_times, population = (
        run_experiment(
            size=512,
            generations=5000,
            capture_every=25,
        )
    )

    build_snapshot_figure(
        frames,
        frame_times,
    )

    build_population_plot(
        population,
    )

    build_growth_gif(
        frames,
        frame_times,
    )
