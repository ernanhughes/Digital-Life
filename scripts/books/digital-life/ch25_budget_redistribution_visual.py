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
SEED = 2501


def find_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists():
            return p
    raise RuntimeError("repo root not found")


ROOT = find_root()
sys.path.insert(0, str(ROOT / "notebooks" / "_shared"))
sys.path.insert(0, str(ROOT / "scripts" / "books" / "digital-life"))

from digital_crystal import cell_keyed_uniform, frontier, neighbors, run_crystal  # noqa: E402
from visualization.digital_crystal_renderer import (  # noqa: E402
    COLORS,
    draw_cells,
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


def selected(candidates, budget, seed):
    return set(sorted(candidates, key=lambda c: cell_keyed_uniform(seed, 1, c))[:budget])


def fcp(cells, x, max_radius):
    before = frontier(cells, max_radius)
    after = frontier(set(cells) | {x}, max_radius)
    return len(after) - len(before)


def choose_x(cells, max_radius):
    candidates = list(frontier(cells, max_radius))
    scored = []
    for c in candidates:
        n = sum(nb in cells for nb in neighbors(c))
        if n == 1:
            scored.append((fcp(cells, c, max_radius), abs(c[0]) + abs(c[1]), c))
    positives = [s for s in scored if s[0] >= 2]
    return sorted(positives, reverse=True)[0][2] if positives else sorted(scored, reverse=True)[0][2]


def main():
    classes = load_json("research/digital-life/ch25-finite-budget-redistribution-v1/stage-03-class-summaries.json")
    low = load_json("research/digital-life/ch25-finite-budget-redistribution-v1/stage-04-low-budget-linearity.json")
    zero = load_json("research/digital-life/ch25-finite-budget-redistribution-v1/stage-08-full-evaluation-hard-zero.json")
    verdict = load_json("research/digital-life/ch25-finite-budget-redistribution-v1/stage-09-verdict.json")

    max_radius = 11
    best = None
    for seed in range(SEED, SEED + 60):
        for steps in range(5, 24):
            state = run_crystal([0.18] * steps, seed=seed, max_radius=max_radius)
            candidate_occupied = set(state.occupied)
            try:
                candidate_x = choose_x(candidate_occupied, max_radius)
            except IndexError:
                continue
            pf = frontier(candidate_occupied, max_radius)
            ff = frontier(candidate_occupied | {candidate_x}, max_radius)
            f_ref0 = max(len(pf), len(ff))
            b0 = max(1, int(0.25 * f_ref0))
            ps = selected(pf, b0, seed)
            fs = selected(ff, b0, seed)
            far0 = {
                c
                for c in (pf | ff)
                if max(abs(c[0] - candidate_x[0]), abs(c[1] - candidate_x[1]), abs((-c[0] - c[1]) - (-candidate_x[0] - candidate_x[1]))) > 1
            }
            score = len((fs ^ ps) & far0)
            if best is None or score > best[0]:
                best = (score, seed, candidate_occupied, candidate_x)
    if best is None:
        raise RuntimeError("could not find representative n=1 frontier site for Ch25 visual")
    _, representative_seed, occupied, x = best
    prevent_frontier = frontier(occupied, max_radius)
    force_frontier = frontier(occupied | {x}, max_radius)
    union_frontier = prevent_frontier | force_frontier
    f_ref = max(len(prevent_frontier), len(force_frontier))
    b = max(1, int(0.25 * f_ref))
    prevent_selected = selected(prevent_frontier, b, representative_seed)
    force_selected = selected(force_frontier, b, representative_seed)
    swapped_in = force_selected - prevent_selected
    swapped_out = prevent_selected - force_selected
    far = {c for c in union_frontier if max(abs(c[0] - x[0]), abs(c[1] - x[1]), abs((-c[0]-c[1]) - (-x[0]-x[1]))) > 1}
    local = union_frontier - far

    def render_stage(title, subtitle, *, show_x=False, show_force_frontier=False, show_swaps=False, full_zero=False):
        fig, axes = setup_figure(1, width=5.1, height=4.4)
        ax = axes[0]
        draw_cells(ax, occupied | ({x} if show_x else set()))
        draw_outlines(ax, force_frontier if show_force_frontier else prevent_frontier, color="frontier", alpha=0.3)
        if show_x:
            draw_ring(ax, x, 1, color="intervention", alpha=0.55)
            draw_markers(ax, [x], color="intervention", size=0.58)
        if show_swaps:
            draw_markers(ax, swapped_in & far, color="swapped_in", size=0.26)
            draw_markers(ax, swapped_out & far, color="swapped_out", size=0.26)
            draw_outlines(ax, local, color="intervention", alpha=0.45)
        if full_zero:
            ax.text(0.03, 0.06, "far E = 0\nfar symdiff = 0", transform=ax.transAxes, color=COLORS["text"], fontsize=10)
        draw_title(ax, title, subtitle)
        frame(ax, sorted(occupied | union_frontier))
        return fig

    path = OUT / "ch25-budget-redistribution-hero.png"
    if EXPORT_HERO:
        fig, axes = setup_figure(2, width=13.5, height=6.0, title="Chapter 25: finite evaluation slots couple a local intervention to distant candidate selection")
        for ax, title, subtitle, show_swaps, full_zero in [
            (axes[0], "FINITE BUDGET", "B = ceil(.25 * F_ref); far slots swap outside the one-step causal cone", True, False),
            (axes[1], "FULL / UNBOUNDED", "all candidates evaluated; far selector displacement is structurally zero", False, True),
        ]:
            draw_cells(ax, occupied)
            draw_outlines(ax, union_frontier, color="frontier", alpha=0.25)
            draw_ring(ax, x, 1, color="intervention", alpha=0.55)
            draw_markers(ax, [x], color="intervention", size=0.58)
            if show_swaps:
                draw_markers(ax, swapped_in & far, color="swapped_in", size=0.26)
                draw_markers(ax, swapped_out & far, color="swapped_out", size=0.26)
                draw_outlines(ax, local, color="intervention", alpha=0.45)
            if full_zero:
                ax.text(0.03, 0.06, "far E = 0\nfar symdiff = 0", transform=ax.transAxes, color=COLORS["text"], fontsize=10)
            draw_title(ax, title, subtitle)
            frame(ax, sorted(occupied | union_frontier))
        save_png(fig, path)
    frames = [
        fig_to_image(render_stage("CHECKPOINT", "same crystal before focal intervention")),
        fig_to_image(render_stage("FORCE x", "local frontier changes", show_x=True, show_force_frontier=True)),
        fig_to_image(render_stage("FINITE B", "fixed slots displace far candidates", show_x=True, show_force_frontier=True, show_swaps=True)),
        fig_to_image(render_stage("FULL", "all far selector displacement is zero", show_x=True, show_force_frontier=True, full_zero=True)),
    ]
    labels = ["t0 checkpoint", "t1 local intervention", "t2 finite-B swaps", "t3 full evaluation"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch25-budget-redistribution-filmstrip.png", columns=4)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch25-budget-redistribution.gif", duration=760)
    write_provenance(path, {
        "chapter": "25: How Does Finite Computation Create Non-Local Coupling?",
        "chapter_file": "content/books/digital-life/25-how-does-finite-computation-create-non-local-coupling/index.md",
        "research_scripts": ["ch25_digital_crystal_finite_budget_redistribution_v1.py"],
        "artifacts": [
            "research/digital-life/ch25-finite-budget-redistribution-v1/stage-03-class-summaries.json",
            "stage-04-low-budget-linearity.json",
            "stage-08-full-evaluation-hard-zero.json",
            "stage-09-verdict.json",
        ],
        "source": "representative frozen-substrate state plus canonical artifact values",
        "measured_values": {
            "f_025_E_far_FCP_plus_2": classes["f=0.25"]["2"]["E_far"]["mean"],
            "f_025_actual_deltaF_plus_2": classes["f=0.25"]["2"]["actual_deltaF"]["mean"],
            "low_budget_status": low["status"],
            "full_zero_status": zero["status"],
            "overall_status": verdict["overall_status"],
        },
        "representative_seed": representative_seed,
        "visual_encoding": "green/orange far cells are actual selector swaps in a representative finite-budget branch comparison; full-evaluation zero uses canonical hard-zero artifact",
        "outputs": ["ch25-budget-redistribution-hero.png", "ch25-budget-redistribution-filmstrip.png", "ch25-budget-redistribution.gif"],
    })
    print(path)


if __name__ == "__main__":
    main()
