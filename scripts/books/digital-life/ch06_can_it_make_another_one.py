from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------

def save_array_gif(
    frames: list[np.ndarray],
    filename: str,
    title: str,
    fps: int = 3,
):
    fig, ax = plt.subplots(figsize=(8, 5))

    image = ax.imshow(
        frames[0],
        cmap="binary",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    height, width = frames[0].shape

    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)

    ax.grid(
        which="minor",
        linewidth=0.25,
        alpha=0.2,
    )

    ax.tick_params(
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    ax.set_title(title)

    time_text = ax.text(
        0.02,
        0.98,
        "t = 0",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )

    def update(frame_index):
        image.set_data(frames[frame_index])
        time_text.set_text(f"t = {frame_index}")
        return image, time_text

    animation = FuncAnimation(
        fig,
        update,
        frames=len(frames),
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
# Figure 1 — explanatory self-replication animation
# ---------------------------------------------------------------------

def stamp_pattern(
    canvas: np.ndarray,
    pattern: np.ndarray,
    row: int,
    col: int,
):
    h, w = pattern.shape
    canvas[row:row + h, col:col + w] = pattern


def build_replication_gif():
    """
    Conceptual CA-style replication sequence.

    Important:
    This is an explanatory visual, not a claim that this is
    Evoloops or Outlier.

    It demonstrates the observable we care about:
        one localized pattern
        ->
        two spatially distinct similar patterns
    """

    height = 28
    width = 56

    parent = np.array(
        [
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [0, 1, 0, 0],
        ],
        dtype=np.uint8,
    )

    frames = []

    # Phase 1: one parent.
    for _ in range(4):
        frame = np.zeros((height, width), dtype=np.uint8)
        stamp_pattern(frame, parent, 12, 8)
        frames.append(frame)

    # Phase 2: connection begins.
    for length in [2, 5, 8, 11, 14]:
        frame = np.zeros((height, width), dtype=np.uint8)

        stamp_pattern(frame, parent, 12, 8)

        frame[13, 12:12 + length] = 1

        frames.append(frame)

    # Phase 3: partial child appears.
    partials = [
        np.array(
            [
                [0, 1, 0, 0],
            ],
            dtype=np.uint8,
        ),
        np.array(
            [
                [0, 1, 1, 0],
                [1, 1, 0, 0],
            ],
            dtype=np.uint8,
        ),
        parent,
    ]

    for partial in partials:
        frame = np.zeros((height, width), dtype=np.uint8)

        stamp_pattern(frame, parent, 12, 8)

        frame[13, 12:30] = 1

        stamp_pattern(
            frame,
            partial,
            12,
            32,
        )

        frames.append(frame)

    # Phase 4: child separates.
    for gap in [0, 1, 2, 3, 4]:
        frame = np.zeros((height, width), dtype=np.uint8)

        stamp_pattern(frame, parent, 12, 8)
        stamp_pattern(frame, parent, 12, 32 + gap)

        if gap == 0:
            frame[13, 12:32] = 1

        frames.append(frame)

    # Hold final state.
    for _ in range(5):
        frame = np.zeros((height, width), dtype=np.uint8)

        stamp_pattern(frame, parent, 12, 8)
        stamp_pattern(frame, parent, 12, 36)

        frames.append(frame)

    save_array_gif(
        frames,
        "ch06-self-replication.gif",
        "From One Localized Pattern to Two",
        fps=3,
    )


# ---------------------------------------------------------------------
# Figure 2 — replication vs reproduction
# ---------------------------------------------------------------------

def build_replication_vs_reproduction():
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    ax.set_title(
        "Replication and Reproduction Are Not the Same Claim",
        pad=20,
    )

    # Replication side.
    ax.text(
        2.5,
        6.0,
        "SELF-REPLICATION",
        ha="center",
        va="center",
        fontsize=14,
        weight="bold",
    )

    ax.text(
        2.5,
        5.3,
        "offspring is effectively identical",
        ha="center",
        va="center",
    )

    ax.text(
        2.5,
        4.1,
        "101101",
        ha="center",
        va="center",
        fontsize=16,
    )

    ax.annotate(
        "",
        xy=(2.5, 2.7),
        xytext=(2.5, 3.7),
        arrowprops={"arrowstyle": "->"},
    )

    ax.text(
        2.5,
        2.2,
        "101101",
        ha="center",
        va="center",
        fontsize=16,
    )

    ax.text(
        2.5,
        1.2,
        "same inherited configuration",
        ha="center",
        va="center",
    )

    # Reproduction side.
    ax.text(
        9.0,
        6.0,
        "SELF-REPRODUCTION",
        ha="center",
        va="center",
        fontsize=14,
        weight="bold",
    )

    ax.text(
        9.0,
        5.3,
        "offspring may contain inheritable variation",
        ha="center",
        va="center",
    )

    ax.text(
        9.0,
        4.1,
        "101101",
        ha="center",
        va="center",
        fontsize=16,
    )

    ax.annotate(
        "",
        xy=(9.0, 2.7),
        xytext=(9.0, 3.7),
        arrowprops={"arrowstyle": "->"},
    )

    ax.text(
        9.0,
        2.2,
        "101001",
        ha="center",
        va="center",
        fontsize=16,
    )

    ax.text(
        9.0,
        1.2,
        "variation can persist into descendants",
        ha="center",
        va="center",
    )

    # Divider.
    ax.axvline(
        5.75,
        ymin=0.12,
        ymax=0.88,
        linewidth=1,
    )

    fig.tight_layout()

    path = OUTPUT_DIR / "ch06-replication-vs-reproduction.png"

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Figure 3 — lineage / descendant count
# ---------------------------------------------------------------------

def build_lineage_growth():
    """
    Explanatory descendant-count curve.

    This is intentionally synthetic and should be described
    in the chapter as a conceptual measurement example,
    not as empirical data from Evoloops or Outlier.
    """

    generations = np.arange(0, 13)

    descendants = np.array(
        [
            1,
            1,
            2,
            2,
            3,
            4,
            5,
            7,
            9,
            12,
            16,
            21,
            28,
        ]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        generations,
        descendants,
        marker="o",
    )

    ax.set_title(
        "A Reproductive Pattern Can Create a Growing Lineage"
    )

    ax.set_xlabel("Generation")
    ax.set_ylabel("Recognized descendants")

    ax.grid(alpha=0.25)

    fig.tight_layout()

    path = OUTPUT_DIR / "ch06-lineage-growth.png"

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
    build_replication_gif()
    build_replication_vs_reproduction()
    build_lineage_growth()