from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def elementary_step(state: np.ndarray, rule: int) -> np.ndarray:
    """
    Advance one generation of an elementary cellular automaton.

    Periodic boundaries:
    the left and right edges wrap around.
    """
    left = np.roll(state, 1)
    centre = state
    right = np.roll(state, -1)

    neighborhood = (left << 2) | (centre << 1) | right

    return ((rule >> neighborhood) & 1).astype(np.uint8)


def run_rule(
    rule: int,
    width: int,
    generations: int,
) -> np.ndarray:
    """
    Start from one active cell and return the full spacetime history.
    """
    state = np.zeros(width, dtype=np.uint8)
    state[width // 2] = 1

    history = np.zeros((generations, width), dtype=np.uint8)
    history[0] = state

    for t in range(1, generations):
        state = elementary_step(state, rule)
        history[t] = state

    return history


def save_spacetime(
    history: np.ndarray,
    filename: str,
    title: str,
    figsize=(12, 7),
):
    """
    Render a clean spacetime diagram.
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(
        history,
        interpolation="nearest",
        aspect="auto",
        cmap="binary",
        vmin=0,
        vmax=1,
    )

    ax.set_title(title)
    ax.set_xlabel("Space")
    ax.set_ylabel("Time")

    fig.tight_layout()

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"saved: {path}")


def build_rule22():
    """
    Main Chapter 02 figure.

    A wide world prevents the expanding pattern from reaching the
    periodic boundary during the displayed interval.
    """
    history = run_rule(
        rule=22,
        width=181,
        generations=80,
    )

    save_spacetime(
        history,
        "ch02-rule22-spacetime.png",
        "Rule 22 from a Single Active Cell",
    )


def build_rule30_teaser():
    """
    Short Rule 30 teaser for the end of Chapter 02.
    Chapter 03 can later use a larger, more detailed Rule 30 figure.
    """
    history = run_rule(
        rule=30,
        width=181,
        generations=45,
    )

    save_spacetime(
        history,
        "ch02-rule30-teaser.png",
        "Change One Number: Rule 30",
        figsize=(12, 4.5),
    )


if __name__ == "__main__":
    build_rule22()
    build_rule30_teaser()