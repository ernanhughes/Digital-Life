from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def elementary_step(state: np.ndarray, rule: int) -> np.ndarray:
    """
    Advance one generation of an elementary cellular automaton
    using periodic boundary conditions.
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
    initial_state: np.ndarray | None = None,
) -> np.ndarray:
    """
    Run an elementary cellular automaton and return its spacetime history.
    """
    if initial_state is None:
        state = np.zeros(width, dtype=np.uint8)
        state[width // 2] = 1
    else:
        state = initial_state.astype(np.uint8).copy()

    history = np.zeros((generations, width), dtype=np.uint8)
    history[0] = state

    for t in range(1, generations):
        state = elementary_step(state, rule)
        history[t] = state

    return history


def single_seed(width: int) -> np.ndarray:
    state = np.zeros(width, dtype=np.uint8)
    state[width // 2] = 1
    return state


def perturbed_seed(width: int) -> np.ndarray:
    """
    Same as the single seed, except for one additional active cell.
    """
    state = single_seed(width)
    state[width // 2 + 1] = 1
    return state


def render_spacetime(
    history: np.ndarray,
    filename: str,
    title: str,
    figsize=(12, 8),
):
    fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(
        history,
        cmap="binary",
        interpolation="nearest",
        aspect="auto",
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


def build_rule30_hero():
    """
    Large hero figure for Chapter 03.
    """
    history = run_rule(
        rule=30,
        width=301,
        generations=150,
    )

    render_spacetime(
        history,
        "ch03-rule30-hero.png",
        "Rule 30 from a Single Active Cell",
        figsize=(13, 9),
    )


def build_rule_comparison():
    """
    Controlled comparison:
    same initial condition, same dimensions, different local rule.
    """
    width = 241
    generations = 110

    initial = single_seed(width)

    rule22 = run_rule(
        rule=22,
        width=width,
        generations=generations,
        initial_state=initial,
    )

    rule30 = run_rule(
        rule=30,
        width=width,
        generations=generations,
        initial_state=initial,
    )

    combined = np.concatenate([rule22, rule30], axis=1)

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.imshow(
        combined,
        cmap="binary",
        interpolation="nearest",
        aspect="auto",
        vmin=0,
        vmax=1,
    )

    ax.axvline(width - 0.5, linewidth=1)

    ax.text(
        width * 0.5,
        -6,
        "Rule 22",
        ha="center",
        va="bottom",
    )

    ax.text(
        width * 1.5,
        -6,
        "Rule 30",
        ha="center",
        va="bottom",
    )

    ax.set_title("Same Initial State, Different Local Rule")
    ax.set_xlabel("Space")
    ax.set_ylabel("Time")
    ax.set_xticks([])

    fig.tight_layout()

    path = OUTPUT_DIR / "ch03-rule22-vs-rule30.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"saved: {path}")


def build_perturbation_experiment():
    """
    Compare two nearly identical Rule 30 initial conditions
    and visualize where their histories differ.
    """
    width = 301
    generations = 130

    seed_a = single_seed(width)
    seed_b = perturbed_seed(width)

    history_a = run_rule(
        rule=30,
        width=width,
        generations=generations,
        initial_state=seed_a,
    )

    history_b = run_rule(
        rule=30,
        width=width,
        generations=generations,
        initial_state=seed_b,
    )

    difference = np.not_equal(history_a, history_b).astype(np.uint8)

    # Stack the three panels vertically with small blank separators.
    separator = np.zeros((8, width), dtype=np.uint8)

    combined = np.concatenate(
        [
            history_a,
            separator,
            history_b,
            separator,
            difference,
        ],
        axis=0,
    )

    fig, ax = plt.subplots(figsize=(13, 11))

    ax.imshow(
        combined,
        cmap="binary",
        interpolation="nearest",
        aspect="auto",
        vmin=0,
        vmax=1,
    )

    first_end = generations
    second_start = generations + len(separator)
    second_end = second_start + generations
    diff_start = second_end + len(separator)

    ax.text(
        -8,
        generations / 2,
        "A\nsingle seed",
        ha="right",
        va="center",
    )

    ax.text(
        -8,
        second_start + generations / 2,
        "B\none extra cell",
        ha="right",
        va="center",
    )

    ax.text(
        -8,
        diff_start + generations / 2,
        "Difference",
        ha="right",
        va="center",
    )

    ax.set_title("Rule 30: A One-Cell Perturbation Spreads Through Time")
    ax.set_xlabel("Space")
    ax.set_ylabel("Time / experiment panel")
    ax.set_yticks([])

    fig.tight_layout()

    path = OUTPUT_DIR / "ch03-rule30-perturbation.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"saved: {path}")


def build_difference_growth():
    """
    Optional evidence figure:
    measure how many cells differ at each generation.
    """
    width = 501
    generations = 180

    history_a = run_rule(
        rule=30,
        width=width,
        generations=generations,
        initial_state=single_seed(width),
    )

    history_b = run_rule(
        rule=30,
        width=width,
        generations=generations,
        initial_state=perturbed_seed(width),
    )

    difference = np.not_equal(history_a, history_b)
    differing_cells = difference.sum(axis=1)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(np.arange(generations), differing_cells)

    ax.set_title("Growth of a One-Cell Perturbation Under Rule 30")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Differing cells")
    ax.grid(alpha=0.25)

    fig.tight_layout()

    path = OUTPUT_DIR / "ch03-rule30-difference-growth.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"saved: {path}")


if __name__ == "__main__":
    build_rule30_hero()
    build_rule_comparison()
    build_perturbation_experiment()

    # Optional, but useful because it starts converting the visual
    # perturbation experiment into an actual measurement.
    build_difference_growth()