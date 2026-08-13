from __future__ import annotations

import json
import sys
from pathlib import Path

PROFILE = "quick"
EXPORT = True
EXPORT_HERO = True
EXPORT_FILMSTRIP = True
EXPORT_GIF = True
EXPORT_MP4 = False
SEED = 2701


def find_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists():
            return p
    raise RuntimeError("repo root not found")


ROOT = find_root()
sys.path.insert(0, str(ROOT / "notebooks" / "_shared"))
sys.path.insert(0, str(ROOT / "scripts" / "books" / "digital-life"))

from digital_crystal import frontier, hex_distance, neighbors, run_crystal  # noqa: E402
from visualization.digital_crystal_renderer import (  # noqa: E402
    draw_cells,
    draw_intensity,
    draw_markers,
    draw_outlines,
    draw_ring,
    draw_title,
    fig_to_image,
    frame,
    save_png,
    save_filmstrip,
    save_gif,
    setup_figure,
    write_provenance,
)

OUT = ROOT / "static" / "images" / "books" / "digital-life" / "visuals"


def load_json(path: str):
    full = ROOT / path
    if not full.exists():
        raise FileNotFoundError(f"required artifact missing: {full}")
    return json.loads(full.read_text(encoding="utf-8"))


def choose_challenge(cells):
    candidates = frontier(cells, 10)
    return sorted(candidates, key=lambda c: (-sum(nb in cells for nb in neighbors(c)), hex_distance(c), c))[0]


def main():
    profiles = load_json("research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-03-arm-profiles.json")
    primary = load_json("research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-04-primary.json")
    secondary = load_json("research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-05-secondary.json")
    closeout = load_json("research/digital-life/ch27-v2-trajectory-closeout-audit/ch27-v2-trajectory-closeout-audit.json")

    state = run_crystal([0.2] * 20, seed=SEED, max_radius=10)
    occupied = set(state.occupied)
    x = choose_challenge(occupied)
    near_cells = {c for c in occupied if max(abs(c[0] - x[0]), abs(c[1] - x[1]), abs((-c[0]-c[1]) - (-x[0]-x[1]))) <= 3}
    remote_cells = sorted(occupied - near_cells, key=lambda c: -hex_distance(c))[: len(near_cells)]
    accessible_intensity = {c: 1.0 / (1 + max(abs(c[0] - x[0]), abs(c[1] - x[1]))) for c in near_cells}
    remote_intensity = {c: 0.75 for c in remote_cells[: max(6, len(remote_cells) // 2)]}
    front = frontier(occupied, 10)

    panels = [
        ("ACCESSIBLE HISTORY", accessible_intensity, f"RB_G_local = {profiles['accessible']['RB_G_local']['mean']:.2f}"),
        ("REMOTE / MATCHED HISTORY", remote_intensity, f"RB_G_local = {profiles['remote']['RB_G_local']['mean']:.2f}"),
    ]

    def render_stage(title, subtitle, intensity=None, show_challenge=False, response=None):
        fig, axes = setup_figure(1, width=5.2, height=4.4)
        ax = axes[0]
        draw_cells(ax, occupied)
        draw_outlines(ax, front, color="frontier", alpha=0.25)
        if intensity:
            draw_intensity(ax, intensity, color="hidden")
        if show_challenge:
            draw_ring(ax, x, 1, color="intervention", alpha=0.5)
            draw_markers(ax, [x], color="intervention", size=0.55)
        if response:
            draw_markers(ax, response, color="negative", size=0.25, alpha=0.75)
        draw_title(ax, title, subtitle)
        frame(ax, sorted(occupied | front))
        return fig

    path = OUT / "ch27-hidden-material-hero.png"
    if EXPORT_HERO:
        fig, axes = setup_figure(2, width=12.5, height=5.8, title="Chapter 27: the same visible geometry can carry different hidden material history")
        for ax, (title, intensity, subtitle) in zip(axes, panels):
            draw_cells(ax, occupied)
            draw_outlines(ax, front, color="frontier", alpha=0.25)
            draw_intensity(ax, intensity, color="hidden")
            draw_ring(ax, x, 1, color="intervention", alpha=0.5)
            draw_markers(ax, [x], color="intervention", size=0.55)
            draw_title(ax, title, subtitle + "\nvisible occupied cells held identical")
            frame(ax, sorted(occupied | front))
        save_png(fig, path)

    response_cells = set(sorted(front, key=lambda c: (abs(c[0] - x[0]) + abs(c[1] - x[1]), c))[:12])
    frames = [
        fig_to_image(render_stage("VISIBLE GEOMETRY", "same occupied cells")),
        fig_to_image(render_stage("HIDDEN STATE", "accessible material overlay", accessible_intensity)),
        fig_to_image(render_stage("SAME CHALLENGE", "same perturbation site", accessible_intensity, show_challenge=True)),
        fig_to_image(render_stage("DIVERGING RESPONSE", f"accessible - remote = {primary['result']['mean']:.3f}", accessible_intensity, show_challenge=True, response=response_cells)),
    ]
    labels = ["t0 visible same", "t1 hidden state", "t2 same challenge", "t3 response contrast"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch27-hidden-material-filmstrip.png", columns=4)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch27-hidden-material.gif", duration=780)
    write_provenance(path, {
        "chapter": "27: Can Stored History Redirect the Future?",
        "chapter_file": "content/books/digital-life/27-can-stored-history-redirect-the-future/index.md",
        "research_scripts": [
            "ch27_digital_crystal_decaying_material_history_causal_response_v2.py",
            "ch27_v2_trajectory_closeout_audit.py",
        ],
        "artifacts": [
            "research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-03-arm-profiles.json",
            "stage-04-primary.json",
            "stage-05-secondary.json",
            "research/digital-life/ch27-v2-trajectory-closeout-audit/ch27-v2-trajectory-closeout-audit.json",
        ],
        "source": "identical representative visible geometry plus canonical V2 material-history response artifacts",
        "measured_values": {
            "primary_status": primary["status"],
            "RB_G_accessible_minus_remote": primary["result"]["mean"],
            "E1_ring1_accessible_minus_remote": secondary["E1_ring1_accessible_minus_remote"]["mean"],
            "formal_V2_primary_status_unchanged": closeout["metadata"]["formal_V2_primary_status_unchanged"],
        },
        "visual_encoding": "hidden material intensity is an overlay on identical occupied geometry; response values come from canonical artifact",
        "outputs": ["ch27-hidden-material-hero.png", "ch27-hidden-material-filmstrip.png", "ch27-hidden-material.gif"],
    })
    print(path)


if __name__ == "__main__":
    main()
