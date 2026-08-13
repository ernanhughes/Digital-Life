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
SEED = 2301


def find_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists():
            return p
    raise RuntimeError("repo root not found")


ROOT = find_root()
sys.path.insert(0, str(ROOT / "notebooks" / "_shared"))
sys.path.insert(0, str(ROOT / "scripts" / "books" / "digital-life"))

from digital_crystal import frontier, neighbors, run_crystal  # noqa: E402
from visualization.digital_crystal_renderer import (  # noqa: E402
    COLORS,
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


def choose_focal(cells, candidates):
    scored = []
    for c in candidates:
        n = sum(nb in cells for nb in neighbors(c))
        if n >= 1:
            scored.append((n, abs(c[0]) + abs(c[1]), c))
    return sorted(scored, reverse=True)[0][2]


def main():
    decomp = load_json("research/digital-life/ch23-persistent-transient-causal-gain-v4/stage-02-decomposition.json")
    verdict = load_json("research/digital-life/ch23-persistent-transient-causal-gain-v4/stage-04-verdict.json")

    state = run_crystal([0.22] * 18, seed=SEED, max_radius=9)
    occupied = set(state.occupied)
    front = frontier(occupied, 9)
    x = choose_focal(occupied, front)
    local = {x, *neighbors(x)}

    persistent = set(occupied) | {x}
    transient = set(occupied)
    positive = {c for c in neighbors(x) if c not in occupied}
    negative = (front - positive)

    all_cells = sorted(occupied | front | local)
    panels = [
        ("PREVENT", occupied, {}, "x does not attach"),
        ("TRANSIENT", transient, {x: 1.0}, f"G_transient(30) = {decomp['transient_G_H_local']['mean']:.3f}"),
        ("PERSISTENT", persistent, {x: 1.0}, f"G_persistent(30) = {decomp['persistent_G_H_local']['mean']:.3f}"),
    ]

    def render_stage(stage_title, cells, intensity, subtitle):
        fig, axes = setup_figure(1, width=4.6, height=4.1)
        ax = axes[0]
        draw_cells(ax, cells)
        draw_outlines(ax, front, color="frontier", alpha=0.45)
        draw_ring(ax, x, 1, color="intervention")
        draw_markers(ax, [x], color="intervention", size=0.56)
        draw_markers(ax, positive, color="positive", size=0.28, alpha=0.85)
        draw_outlines(ax, negative, color="negative", alpha=0.18, linewidth=0.4)
        draw_intensity(ax, intensity, color="modified")
        draw_title(ax, stage_title, subtitle)
        frame(ax, all_cells)
        return fig, ax

    path = OUT / "ch23-one-attachment-hero.png"
    if EXPORT_HERO:
        fig, axes = setup_figure(3, width=13.5, height=5.4, title="Chapter 23: one attachment has local mechanics, transient consequences, and persistent state")
        for ax, (title, cells, intensity, subtitle) in zip(axes, panels):
            draw_cells(ax, cells)
            draw_outlines(ax, front, color="frontier", alpha=0.45)
            draw_ring(ax, x, 1, color="intervention")
            draw_markers(ax, [x], color="intervention", size=0.56)
            draw_markers(ax, positive, color="positive", size=0.28, alpha=0.85)
            draw_outlines(ax, negative, color="negative", alpha=0.18, linewidth=0.4)
            draw_intensity(ax, intensity, color="modified")
            draw_title(ax, title, subtitle)
            frame(ax, all_cells)
        axes[1].text(0.02, 0.06, f"g_mech_1 = {decomp['g_mech_1']['mean']:.3f}\ng1 = {decomp['persistent_g1']['mean']:.3f}", transform=axes[1].transAxes, color=COLORS["text"], fontsize=9)
        save_png(fig, path)

    frames = [fig_to_image(render_stage(*panel)[0]) for panel in [("CHECKPOINT", occupied, {}, "same state before intervention"), *panels]]
    labels = ["t0 checkpoint", "t1 prevent", "t2 transient", "t3 persistent"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch23-one-attachment-filmstrip.png", columns=4)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch23-one-attachment.gif", duration=760)
    write_provenance(OUT / "ch23-one-attachment-hero.png", {
        "chapter": "23: What Does One Attachment Cause?",
        "chapter_file": "content/books/digital-life/23-what-does-one-attachment-cause/index.md",
        "research_scripts": ["ch23_digital_crystal_causal_attachment_gain_v3.py", "ch23_digital_crystal_persistent_transient_causal_gain_v4.py"],
        "artifacts": ["research/digital-life/ch23-persistent-transient-causal-gain-v4/stage-02-decomposition.json", "stage-04-verdict.json"],
        "source": "representative frozen-substrate state plus canonical artifact values",
        "measured_values": {
            "g_mech_1": decomp["g_mech_1"]["mean"],
            "persistent_g1": decomp["persistent_g1"]["mean"],
            "transient_G_H_local": decomp["transient_G_H_local"]["mean"],
            "persistent_G_H_local": decomp["persistent_G_H_local"]["mean"],
            "overall_status": verdict["overall_status"],
        },
        "visual_encoding": "cell positions are simulated; colors encode intervention, local opportunity, and persistent/transient material state",
        "outputs": ["ch23-one-attachment-hero.png", "ch23-one-attachment-filmstrip.png", "ch23-one-attachment.gif"],
    })
    print(OUT / "ch23-one-attachment-hero.png")


if __name__ == "__main__":
    main()
