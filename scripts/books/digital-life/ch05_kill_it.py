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


def empty_world(size: int = 40) -> np.ndarray:
    return np.zeros((size, size), dtype=np.uint8)


def place_pattern(
    world: np.ndarray,
    pattern: np.ndarray,
    row: int,
    col: int,
) -> None:
    h, w = pattern.shape
    world[row:row + h, col:col + w] = pattern


# ---------------------------------------------------------------------
# Damage helpers
# ---------------------------------------------------------------------

def active_positions(state: np.ndarray) -> np.ndarray:
    return np.argwhere(state == 1)


def delete_active_cell(
    state: np.ndarray,
    active_index: int = 0,
) -> np.ndarray:
    damaged = state.copy()

    positions = active_positions(damaged)

    if len(positions) == 0:
        return damaged

    row, col = positions[active_index % len(positions)]
    damaged[row, col] = 0

    return damaged


def random_damage(
    state: np.ndarray,
    fraction: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Delete a fraction of currently active cells.
    """
    damaged = state.copy()

    positions = active_positions(damaged)

    if len(positions) == 0:
        return damaged

    count = int(round(len(positions) * fraction))
    count = min(count, len(positions))

    if count == 0:
        return damaged

    chosen = rng.choice(
        len(positions),
        size=count,
        replace=False,
    )

    for index in chosen:
        row, col = positions[index]
        damaged[row, col] = 0

    return damaged


# ---------------------------------------------------------------------
# Similarity / survival measures
# ---------------------------------------------------------------------

def active_iou(a: np.ndarray, b: np.ndarray) -> float:
    """
    Intersection-over-union for active cells.
    """
    a_active = a.astype(bool)
    b_active = b.astype(bool)

    intersection = np.logical_and(a_active, b_active).sum()
    union = np.logical_or(a_active, b_active).sum()

    if union == 0:
        return 1.0

    return float(intersection / union)


def survives(state: np.ndarray) -> bool:
    return bool(state.sum() > 0)


# ---------------------------------------------------------------------
# GIF helper
# ---------------------------------------------------------------------

def save_gif(
    history: np.ndarray,
    filename: str,
    title: str,
    damage_frame: int | None = None,
    fps: int = 4,
):
    fig, ax = plt.subplots(figsize=(7, 7))

    image = ax.imshow(
        history[0],
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    height, width = history.shape[1:]

    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which="minor", linewidth=0.25, alpha=0.2)

    ax.tick_params(
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    ax.set_title(title)

    status = ax.text(
        0.02,
        0.98,
        "t = 0",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )

    def update(frame):
        image.set_data(history[frame])

        label = f"t = {frame}"

        if damage_frame is not None:
            if frame == damage_frame:
                label += " — damage"
            elif frame > damage_frame:
                label += " — post-perturbation"

        status.set_text(label)

        return image, status

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
# Figure 1 — intact vs damaged glider
# ---------------------------------------------------------------------

def build_glider_damage_comparison():
    size = 35
    generations = 24

    intact = empty_world(size)
    place_pattern(intact, GLIDER, 5, 5)

    damaged = delete_active_cell(
        intact,
        active_index=1,
    )

    intact_history = run_life(
        intact,
        generations=generations,
    )

    damaged_history = run_life(
        damaged,
        generations=generations,
    )

    selected = [0, 1, 4, 8, 16, 23]

    rows = [
        ("Intact glider", intact_history),
        ("One cell removed", damaged_history),
    ]

    cell_size = size
    gap = 3

    canvas_height = (
        len(rows) * cell_size
        + (len(rows) - 1) * gap
    )

    canvas_width = (
        len(selected) * cell_size
        + (len(selected) - 1) * gap
    )

    canvas = np.zeros(
        (canvas_height, canvas_width),
        dtype=np.uint8,
    )

    for row_index, (_, history) in enumerate(rows):
        y0 = row_index * (cell_size + gap)

        for col_index, t in enumerate(selected):
            x0 = col_index * (cell_size + gap)

            canvas[
                y0:y0 + cell_size,
                x0:x0 + cell_size,
            ] = history[t]

    fig, ax = plt.subplots(figsize=(15, 6))

    ax.imshow(
        canvas,
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    for col_index, t in enumerate(selected):
        x = col_index * (cell_size + gap) + cell_size / 2

        ax.text(
            x,
            -3,
            f"t = {t}",
            ha="center",
            va="bottom",
        )

    for row_index, (label, _) in enumerate(rows):
        y = row_index * (cell_size + gap) + cell_size / 2

        ax.text(
            -4,
            y,
            label,
            ha="right",
            va="center",
        )

    ax.set_title("Persistence Does Not Imply Recovery")
    ax.axis("off")

    fig.tight_layout()

    path = OUTPUT_DIR / "ch05-glider-damage-comparison.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 2 — damage event GIF
# ---------------------------------------------------------------------

def build_damage_gif():
    size = 40
    damage_time = 12
    total_generations = 36

    state = empty_world(size)
    place_pattern(state, GLIDER, 5, 5)

    frames = []

    for t in range(total_generations):
        if t == damage_time:
            state = delete_active_cell(
                state,
                active_index=0,
            )

        frames.append(state.copy())
        state = life_step(state)

    history = np.asarray(frames)

    save_gif(
        history,
        "ch05-glider-damage.gif",
        "A Persistent Pattern Under Perturbation",
        damage_frame=damage_time,
        fps=4,
    )


# ---------------------------------------------------------------------
# Figure 3 — block fragility
# ---------------------------------------------------------------------

def build_block_damage():
    size = 17

    intact = empty_world(size)
    place_pattern(
        intact,
        BLOCK,
        row=7,
        col=7,
    )

    damaged = delete_active_cell(
        intact,
        active_index=0,
    )

    damaged_history = run_life(
        damaged,
        generations=5,
    )

    selected = [0, 1, 2, 4]

    canvas = np.concatenate(
        [damaged_history[t] for t in selected],
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(10, 3))

    ax.imshow(
        canvas,
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    for index, t in enumerate(selected):
        x = index * size + size / 2

        ax.text(
            x,
            -2,
            f"t = {t}",
            ha="center",
            va="bottom",
        )

    ax.set_title(
        "A Stable Block Collapses After One Cell Is Removed"
    )

    ax.axis("off")

    fig.tight_layout()

    path = OUTPUT_DIR / "ch05-block-damage.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 4 — damage severity curve
# ---------------------------------------------------------------------

def build_damage_severity_curve():
    """
    This deliberately measures SURVIVAL, not regeneration.

    Game of Life gliders are not regenerative structures, so this
    figure should not pretend that they are.

    For each damage severity:
    - remove a fraction of active cells
    - run the damaged system
    - measure whether any active structure survives

    Repeated trials produce a simple robustness-style curve.
    """
    rng = np.random.default_rng(42)

    size = 50
    evaluation_steps = 20
    trials = 300

    damage_levels = np.array(
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    )

    base = empty_world(size)

    # Use several nearby gliders to create a somewhat larger
    # localized active structure for a smoother damage experiment.
    place_pattern(base, GLIDER, 18, 18)
    place_pattern(base, GLIDER, 18, 25)
    place_pattern(base, GLIDER, 25, 18)
    place_pattern(base, GLIDER, 25, 25)

    survival_rates = []

    for damage_fraction in damage_levels:
        survived = 0

        for _ in range(trials):
            damaged = random_damage(
                base,
                fraction=float(damage_fraction),
                rng=rng,
            )

            history = run_life(
                damaged,
                generations=evaluation_steps,
            )

            if survives(history[-1]):
                survived += 1

        survival_rates.append(
            survived / trials
        )

    survival_rates = np.asarray(survival_rates)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        damage_levels,
        survival_rates,
        marker="o",
    )

    ax.set_title(
        "Survival Falls as More Active Cells Are Removed"
    )

    ax.set_xlabel(
        "Fraction of active cells removed"
    )

    ax.set_ylabel(
        "Fraction of trials with surviving activity"
    )

    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.25)

    fig.tight_layout()

    path = OUTPUT_DIR / "ch05-damage-survival-curve.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Build all
# ---------------------------------------------------------------------

if __name__ == "__main__":
    build_glider_damage_comparison()
    build_damage_gif()
    build_block_damage()
    build_damage_severity_curve()