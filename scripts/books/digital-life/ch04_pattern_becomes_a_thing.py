from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Game of Life core
# ---------------------------------------------------------------------

def life_step(state: np.ndarray) -> np.ndarray:
    """
    Advance Conway's Game of Life by one synchronous generation.

    Uses periodic boundary conditions.
    """
    neighbors = (
        np.roll(np.roll(state,  1, axis=0),  1, axis=1)
        + np.roll(state,  1, axis=0)
        + np.roll(np.roll(state,  1, axis=0), -1, axis=1)
        + np.roll(state,  1, axis=1)
        + np.roll(state, -1, axis=1)
        + np.roll(np.roll(state, -1, axis=0),  1, axis=1)
        + np.roll(state, -1, axis=0)
        + np.roll(np.roll(state, -1, axis=0), -1, axis=1)
    )

    born = (state == 0) & (neighbors == 3)
    survive = (state == 1) & ((neighbors == 2) | (neighbors == 3))

    return (born | survive).astype(np.uint8)


def run_life(initial_state: np.ndarray, generations: int) -> np.ndarray:
    """
    Return full history including generation zero.
    """
    state = initial_state.copy()

    history = np.zeros(
        (generations, *state.shape),
        dtype=np.uint8,
    )

    history[0] = state

    for t in range(1, generations):
        state = life_step(state)
        history[t] = state

    return history


# ---------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------

GLIDER = np.array(
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
    ],
    dtype=np.uint8,
)


BLOCK = np.array(
    [
        [1, 1],
        [1, 1],
    ],
    dtype=np.uint8,
)


BLINKER = np.array(
    [
        [1, 1, 1],
    ],
    dtype=np.uint8,
)


def empty_world(size: int = 40) -> np.ndarray:
    return np.zeros((size, size), dtype=np.uint8)


def place_pattern(
    world: np.ndarray,
    pattern: np.ndarray,
    row: int,
    col: int,
) -> None:
    h, w = pattern.shape

    world[
        row : row + h,
        col : col + w,
    ] = pattern


# ---------------------------------------------------------------------
# Utility measurements
# ---------------------------------------------------------------------

def centroid(state: np.ndarray) -> tuple[float, float] | None:
    """
    Return row/column centroid of all active cells.
    """
    positions = np.argwhere(state == 1)

    if len(positions) == 0:
        return None

    row, col = positions.mean(axis=0)
    return float(row), float(col)


def active_count(state: np.ndarray) -> int:
    return int(state.sum())


# ---------------------------------------------------------------------
# GIF helper
# ---------------------------------------------------------------------

def save_gif(
    history: np.ndarray,
    filename: str,
    title: str,
    fps: int = 4,
    figsize=(7, 7),
):
    fig, ax = plt.subplots(figsize=figsize)

    image = ax.imshow(
        history[0],
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Make the fixed lattice visible.
    height, width = history.shape[1:]

    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)

    ax.grid(
        which="minor",
        linewidth=0.25,
        alpha=0.25,
    )

    ax.tick_params(
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    time_text = ax.text(
        0.02,
        0.98,
        "t = 0",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )

    def update(frame):
        image.set_data(history[frame])
        time_text.set_text(f"t = {frame}")
        return image, time_text

    animation = FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=1000 / fps,
        blit=False,
    )

    path = OUTPUT_DIR / filename

    animation.save(
        path,
        writer=PillowWriter(fps=fps),
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 1 — glider animation
# ---------------------------------------------------------------------

def build_glider_gif():
    world = empty_world(32)

    place_pattern(
        world,
        GLIDER,
        row=4,
        col=4,
    )

    history = run_life(
        world,
        generations=25,
    )

    save_gif(
        history,
        "ch04-glider.gif",
        "A Glider: Pattern Motion on a Fixed Grid",
        fps=4,
        figsize=(7, 7),
    )


# ---------------------------------------------------------------------
# Figure 2 — glider centroid trajectory
# ---------------------------------------------------------------------

def build_glider_centroid():
    world = empty_world(60)

    place_pattern(
        world,
        GLIDER,
        row=5,
        col=5,
    )

    history = run_life(
        world,
        generations=100,
    )

    rows = []
    cols = []
    generations = []

    for t, state in enumerate(history):
        c = centroid(state)

        if c is None:
            continue

        row, col = c

        generations.append(t)
        rows.append(row)
        cols.append(col)

    rows = np.asarray(rows)
    cols = np.asarray(cols)

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.plot(cols, rows, marker="o", markersize=2)

    ax.scatter(
        cols[0],
        rows[0],
        marker="o",
        s=70,
        label="Start",
    )

    ax.scatter(
        cols[-1],
        rows[-1],
        marker="x",
        s=70,
        label="End",
    )

    ax.set_title("Glider Centroid Through Time")
    ax.set_xlabel("x centroid")
    ax.set_ylabel("y centroid")

    ax.invert_yaxis()
    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()

    path = OUTPUT_DIR / "ch04-glider-centroid.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 3 — persistence types
# ---------------------------------------------------------------------

def build_persistence_types():
    size = 21
    generations = 8

    patterns = [
        ("Block — fixed persistence", BLOCK),
        ("Blinker — periodic persistence", BLINKER),
        ("Glider — translating persistence", GLIDER),
    ]

    rows = []

    for _, pattern in patterns:
        world = empty_world(size)

        row = size // 2 - pattern.shape[0] // 2
        col = size // 2 - pattern.shape[1] // 2

        place_pattern(
            world,
            pattern,
            row,
            col,
        )

        rows.append(
            run_life(
                world,
                generations=generations,
            )
        )

    # Create a filmstrip-like image:
    # each row corresponds to a pattern;
    # selected time points run horizontally.
    selected_times = [0, 1, 2, 4]

    cell_height = size
    cell_width = size

    vertical_gap = 3
    horizontal_gap = 3

    canvas_height = (
        len(patterns) * cell_height
        + (len(patterns) - 1) * vertical_gap
    )

    canvas_width = (
        len(selected_times) * cell_width
        + (len(selected_times) - 1) * horizontal_gap
    )

    canvas = np.zeros(
        (canvas_height, canvas_width),
        dtype=np.uint8,
    )

    for pattern_index, history in enumerate(rows):
        y0 = pattern_index * (cell_height + vertical_gap)

        for time_index, t in enumerate(selected_times):
            x0 = time_index * (cell_width + horizontal_gap)

            canvas[
                y0 : y0 + cell_height,
                x0 : x0 + cell_width,
            ] = history[t]

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.imshow(
        canvas,
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    # Column labels.
    for time_index, t in enumerate(selected_times):
        x = (
            time_index * (cell_width + horizontal_gap)
            + cell_width / 2
        )

        ax.text(
            x,
            -3,
            f"t = {t}",
            ha="center",
            va="bottom",
        )

    # Row labels.
    for pattern_index, (label, _) in enumerate(patterns):
        y = (
            pattern_index * (cell_height + vertical_gap)
            + cell_height / 2
        )

        ax.text(
            -4,
            y,
            label,
            ha="right",
            va="center",
        )

    ax.set_title("Three Forms of Persistence in Conway's Game of Life")
    ax.axis("off")

    fig.tight_layout()

    path = OUTPUT_DIR / "ch04-persistence-types.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 4 — glider collision animation
# ---------------------------------------------------------------------

def build_collision_gif():
    """
    Two gliders on intersecting trajectories.

    This is mainly a qualitative interaction example:
    the important point is that persistent patterns can alter
    one another when their trajectories intersect.
    """
    size = 50
    world = empty_world(size)

    # Standard southeast-moving glider.
    glider_a = GLIDER

    # Rotated pattern for a different trajectory.
    glider_b = np.rot90(GLIDER, 2)

    place_pattern(
        world,
        glider_a,
        row=10,
        col=10,
    )

    place_pattern(
        world,
        glider_b,
        row=28,
        col=28,
    )

    history = run_life(
        world,
        generations=55,
    )

    save_gif(
        history,
        "ch04-collision.gif",
        "Interaction Between Two Localized Patterns",
        fps=5,
        figsize=(7, 7),
    )


# ---------------------------------------------------------------------
# Build everything
# ---------------------------------------------------------------------

if __name__ == "__main__":
    build_glider_gif()
    build_glider_centroid()
    build_persistence_types()
    build_collision_gif()