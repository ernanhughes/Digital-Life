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
SEED = 2801


def find_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists():
            return p
    raise RuntimeError("repo root not found")


ROOT = find_root()
sys.path.insert(0, str(ROOT / "notebooks" / "_shared"))
sys.path.insert(0, str(ROOT / "scripts" / "books" / "digital-life"))

from digital_crystal import frontier, hex_distance, run_crystal  # noqa: E402
from visualization.digital_crystal_renderer import (  # noqa: E402
    COLORS,
    draw_cells,
    draw_markers,
    draw_outlines,
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


def main():
    primary = load_json("research/digital-life/ch28-causal-modularity-v1/stage-03-primary.json")
    sweep = load_json("research/digital-life/ch28-causal-modularity-v1/stage-04-scale-sweep.json")
    verdict = load_json("research/digital-life/ch28-causal-modularity-v1/stage-06-verdict.json")

    state = run_crystal([0.19] * 22, seed=SEED, max_radius=11)
    occupied = set(state.occupied)
    front = frontier(occupied, 11)
    center = sorted(occupied, key=lambda c: (hex_distance(c), c))[0]
    radius = primary["primary_radius"]
    module = {c for c in occupied if hex_distance(c) <= radius}
    shell = {c for c in occupied if radius < hex_distance(c) <= radius + 2}
    external = set(sorted(occupied - module - shell, key=lambda c: hex_distance(c))[:80])

    def draw_mass_chart(ax, *, upto=3):
        labels = ["internal", "inward", "outward"]
        values = [
            primary["internal_retention"]["mean"],
            primary["external_penetration"]["mean"],
            max(0.0, primary["module_score"]["mean"]),
        ]
        colors = [COLORS["module"], COLORS["negative"], COLORS["positive"]]
        ax.set_facecolor(COLORS["panel"])
        for i, (label, value, color) in enumerate(zip(labels[:upto], values[:upto], colors[:upto])):
            ax.bar(i, value, color=color, alpha=0.85)
            ax.text(i, value + 0.025, f"{value:.2f}", color=COLORS["text"], ha="center", fontsize=9)
        ax.set_ylim(0, 0.75)
        ax.set_xticks(range(upto), labels[:upto], color=COLORS["muted"])
        ax.tick_params(axis="y", colors=COLORS["muted"])
        ax.set_ylabel("measured mean", color=COLORS["muted"])
        for spine in ax.spines.values():
            spine.set_color(COLORS["grid"])
            spine.set_visible(True)
        ax.grid(axis="y", color=COLORS["grid"], alpha=0.4)

    def render_stage(title, subtitle, *, show_module=True, show_shell=False, show_external=False, chart_upto=0):
        fig, axes = setup_figure(2, width=8.8, height=4.3)
        ax = axes[0]
        draw_cells(ax, occupied, alpha=0.55)
        if show_module:
            draw_cells(ax, module, fill="module", edge="occupied_edge", alpha=0.75)
        draw_outlines(ax, front, color="frontier", alpha=0.18)
        if show_shell:
            draw_markers(ax, shell, color="negative", size=0.16, alpha=0.35)
        if show_external:
            draw_markers(ax, external, color="positive", size=0.13, alpha=0.25)
        draw_title(ax, title, subtitle)
        frame(ax, sorted(occupied | front))
        if chart_upto:
            draw_mass_chart(axes[1], upto=chart_upto)
        else:
            axes[1].axis("off")
        return fig

    path = OUT / "ch28-causal-modularity-hero.png"
    if EXPORT_HERO:
        fig, axes = setup_figure(2, width=12.8, height=5.8, title="Chapter 28: causal modularity as measured mass partitioning, not a hard organism boundary")
        ax = axes[0]
        draw_cells(ax, occupied, alpha=0.55)
        draw_cells(ax, module, fill="module", edge="occupied_edge", alpha=0.75)
        draw_outlines(ax, front, color="frontier", alpha=0.18)
        draw_markers(ax, shell, color="negative", size=0.16, alpha=0.35)
        draw_markers(ax, external, color="positive", size=0.13, alpha=0.25)
        draw_title(ax, "candidate region r=4", f"internal retention {primary['internal_retention']['mean']:.2f}\nexternal penetration {primary['external_penetration']['mean']:.2f}")
        frame(ax, sorted(occupied | front))

        ax = axes[1]
        radii = [2, 3, 4, 5]
        internal = [sweep[str(r)]["internal_retention"]["mean"] for r in radii]
        external_pen = [sweep[str(r)]["external_penetration"]["mean"] for r in radii]
        score = [sweep[str(r)]["module_score"]["mean"] for r in radii]
        ax.set_facecolor(COLORS["panel"])
        ax.plot(radii, internal, marker="o", color=COLORS["positive"], label="internal retention")
        ax.plot(radii, external_pen, marker="o", color=COLORS["negative"], label="external penetration")
        ax.plot(radii, score, marker="o", color=COLORS["module"], label="module score")
        ax.axvline(radius, color=COLORS["muted"], lw=1)
        ax.set_title("measured causal mass by candidate radius", color=COLORS["text"], fontsize=12, loc="left")
        ax.set_xlabel("region radius", color=COLORS["muted"])
        ax.set_ylabel("mean fraction / score", color=COLORS["muted"])
        ax.tick_params(colors=COLORS["muted"])
        for spine in ax.spines.values():
            spine.set_color(COLORS["grid"])
            spine.set_visible(True)
        ax.grid(color=COLORS["grid"], alpha=0.45)
        ax.legend(facecolor=COLORS["panel"], edgecolor=COLORS["grid"], labelcolor=COLORS["text"], fontsize=8)
        ax.text(0.02, 0.06, f"status: {primary['status']}\nvalidity: {verdict['validity']['status']}", transform=ax.transAxes, color=COLORS["muted"], fontsize=9)
        save_png(fig, path)

    frames = [
        fig_to_image(render_stage("PERTURB REGION", "candidate region selected", chart_upto=0)),
        fig_to_image(render_stage("INTERNAL RETENTION", "causal mass retained inside", chart_upto=1)),
        fig_to_image(render_stage("INWARD / OUTWARD", "mass also crosses the region", show_shell=True, chart_upto=2)),
        fig_to_image(render_stage("PARTITION", "engineering smoke profile only", show_shell=True, show_external=True, chart_upto=3)),
    ]
    labels = ["t0 perturb", "t1 internal", "t2 inward", "t3 partition"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch28-causal-modularity-filmstrip.png", columns=4)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch28-causal-modularity.gif", duration=780)
    write_provenance(path, {
        "chapter": "28: causal modularity / internal vs external influence",
        "chapter_file": "no current local chapter directory found during generation; visual is research-artifact based",
        "research_scripts": ["ch28_digital_crystal_causal_modularity_v1.py"],
        "artifacts": [
            "research/digital-life/ch28-causal-modularity-v1/stage-03-primary.json",
            "stage-04-scale-sweep.json",
            "stage-06-verdict.json",
        ],
        "source": "representative frozen-substrate state plus canonical engineering-smoke artifact values",
        "measured_values": {
            "module_score": primary["module_score"]["mean"],
            "internal_retention": primary["internal_retention"]["mean"],
            "external_penetration": primary["external_penetration"]["mean"],
            "primary_status": primary["status"],
            "overall_status": verdict["overall_status"],
            "scientific_valid": verdict["validity"]["scientific_valid"],
        },
        "visual_encoding": "candidate region is shown as a soft measured region, not a hard organism-like boundary",
        "outputs": ["ch28-causal-modularity-hero.png", "ch28-causal-modularity-filmstrip.png", "ch28-causal-modularity.gif"],
    })
    print(path)


if __name__ == "__main__":
    main()
