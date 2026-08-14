from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

PROFILE = "quick"
EXPORT = True
EXPORT_HERO = True
EXPORT_FILMSTRIP = True
EXPORT_GIF = True
EXPORT_MP4 = False
SEED = 3001


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
    COLORS,
    draw_cells,
    draw_intensity,
    draw_markers,
    draw_outlines,
    draw_ring,
    draw_title,
    fig_to_image,
    frame,
    save_filmstrip,
    save_gif,
    save_png,
    setup_figure,
    write_provenance,
)

OUT = ROOT / "static" / "images" / "books" / "digital-life" / "visuals"


def load_json(path: str):
    full = ROOT / path
    if not full.exists():
        raise FileNotFoundError(f"required artifact missing: {full}")
    return json.loads(full.read_text(encoding="utf-8"))


def distance(a, b):
    aq, ar = a
    bq, br = b
    return max(abs(aq - bq), abs(ar - br), abs((-aq - ar) - (-bq - br)))


def choose_frontier_site(cells, max_radius):
    candidates = frontier(cells, max_radius)
    return sorted(candidates, key=lambda c: (-sum(nb in cells for nb in neighbors(c)), hex_distance(c), c))[0]


def representative_states():
    current = run_crystal([0.19] * 18, seed=SEED, max_radius=14)
    past = run_crystal([0.19] * 11, seed=SEED, max_radius=14)
    future = run_crystal([0.19] * 23, seed=SEED, max_radius=14)
    return set(past.occupied), set(current.occupied), set(future.occupied)


def make_layers(cells, max_radius=14):
    front = frontier(cells, max_radius)
    x = choose_frontier_site(cells, max_radius)
    finite = set(sorted(front, key=lambda c: (hex_distance(c), c))[: max(8, len(front) // 7)])
    hidden = {c: 1.0 / (1 + hex_distance(c)) for c in cells if hex_distance(c) <= 4}
    module = {c for c in cells if hex_distance(c) <= 4}
    turnover = set(sorted(cells, key=lambda c: (-hex_distance(c), c))[: max(10, len(cells) // 12)])
    causal = {c for c in front if distance(c, x) <= 2}
    return front, x, finite, hidden, module, turnover, causal


def draw_process(ax, past, current, future, *, stage="synthesis", title="PROCESS BEFORE ORGANISM", subtitle=None):
    front, x, finite, hidden, module, turnover, causal = make_layers(current)
    draw_cells(ax, past, fill="occupied", edge="occupied_edge", alpha=0.16)
    draw_cells(ax, future, fill="positive", edge="occupied_edge", alpha=0.12)
    draw_cells(ax, current, alpha=0.82)
    draw_outlines(ax, front, color="frontier", alpha=0.25)
    if stage in {"turnover", "synthesis"}:
        draw_markers(ax, turnover, color="negative", size=0.16, alpha=0.55)
    if stage in {"finite", "coupling", "synthesis"}:
        draw_markers(ax, finite, color="evaluated", size=0.16, alpha=0.72)
    if stage in {"coupling", "synthesis"}:
        draw_ring(ax, x, 2, color="intervention", alpha=0.32)
        draw_markers(ax, [x], color="intervention", size=0.45)
        draw_markers(ax, causal, color="swapped_in", size=0.18, alpha=0.65)
    if stage in {"history", "redirected", "synthesis"}:
        draw_intensity(ax, hidden, color="hidden", max_radius=0.62)
    if stage in {"no_boundary", "synthesis"}:
        draw_cells(ax, module, fill="module", edge="occupied_edge", alpha=0.23, zorder=2)
    draw_title(ax, title, subtitle)
    frame(ax, sorted(past | current | future | front), pad=2.9)


def render_hero(evidence):
    past, current, future = representative_states()
    fig, axes = setup_figure(2, width=13.2, height=6.0, title="Chapter 30: digital life as a continuing computational process, not a declared organism")
    draw_process(
        axes[0],
        past,
        current,
        future,
        stage="synthesis",
        title="PROCESS BEFORE ORGANISM",
        subtitle="past trace, active frontier, finite opportunity, hidden state, possible future",
    )
    ax = axes[1]
    ax.set_facecolor(COLORS["panel"])
    statuses = [
        ("construction", "SUPPORTED"),
        ("turnover", "SUPPORTED"),
        ("finite coupling", "SUPPORTED"),
        ("history effect", "DIRECTION"),
        ("routing", "BOUNDED"),
        ("raw containment", "SUPPORTED"),
        ("individuality", "NOT EST."),
        ("digital life", "PROVISIONAL"),
    ]
    y = list(range(len(statuses)))[::-1]
    colors = [COLORS["swapped_in"], COLORS["swapped_in"], COLORS["positive"], COLORS["hidden"], COLORS["intervention"], COLORS["module"], COLORS["negative"], COLORS["text"]]
    ax.barh(y, [1] * len(statuses), color=colors, alpha=0.75)
    ax.set_xlim(0, 1.08)
    ax.set_yticks(y, [s[0] for s in statuses], color=COLORS["text"])
    ax.set_xticks([])
    for yi, (_, status), color in zip(y, statuses, colors):
        ax.text(1.02, yi, status, color=color, va="center", fontsize=8.8, fontweight="bold")
    ax.set_title("evidence synthesis, not proof of life", color=COLORS["text"], fontsize=12, loc="left")
    for spine in ax.spines.values():
        spine.set_color(COLORS["grid"])
        spine.set_visible(True)
    ax.text(0.02, -0.15, "DIGITAL LIFE - PROVISIONAL SPECIFICATION", transform=ax.transAxes, color=COLORS["muted"], fontsize=9)
    return fig


def render_stage(title, subtitle, stage):
    past, current, future = representative_states()
    fig, axes = setup_figure(1, width=5.35, height=4.45)
    draw_process(axes[0], past, current, future, stage=stage, title=title, subtitle=subtitle)
    return fig


def main():
    ch20 = load_json("research/digital-life/ch20-material-loss-v1/stage-02-loss-sweep.json")
    ch25 = load_json("research/digital-life/ch25-finite-budget-redistribution-v1/stage-09-verdict.json")
    ch26 = load_json("research/digital-life/ch26-dynamically-matched-rate-causal-amplification-v2/stage-04-primary-test.json")
    ch27 = load_json("research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-04-primary.json")
    ch28_v1 = load_json("research/digital-life/ch28-causal-modularity-v1/stage-03-primary.json")
    ch28_v2 = load_json("research/digital-life/ch28-causal-modularity-v2/stage-04-primary.json")
    ch29 = load_json("research/digital-life/ch29-how-to-fail-correctly-v1/stage-05-verdict.json")

    evidence = {
        "ch20_loss_sweep_keys": list(ch20)[:5],
        "ch25_status": ch25["overall_status"],
        "ch26_status": ch26["status"],
        "ch27_status": ch27["status"],
        "ch28_raw_status": ch28_v1["status"],
        "ch28_excess_status": ch28_v2["status"],
        "ch29_status": ch29["status"],
    }

    hero = OUT / "ch30-what-is-digital-life-hero.png"
    if EXPORT_HERO:
        save_png(render_hero(evidence), hero)

    frames = [
        fig_to_image(render_stage("CONTINUED CONSTRUCTION", "active frontier remains open", "construction")),
        fig_to_image(render_stage("TURNOVER", "loss/replacement creates opportunity", "turnover")),
        fig_to_image(render_stage("FINITE COMPUTATION", "limited frontier opportunities are evaluated", "finite")),
        fig_to_image(render_stage("CAUSAL COUPLING", "local perturbation redirects opportunity", "coupling")),
        fig_to_image(render_stage("HIDDEN HISTORY", "same geometry can carry different material state", "history")),
        fig_to_image(render_stage("REDIRECTED TRAJECTORY", "past state constrains future possibilities", "redirected")),
        fig_to_image(render_stage("NO PRIVILEGED INDIVIDUAL", "containment is not individuality", "no_boundary")),
    ]
    labels = ["t0 construction", "t1 turnover", "t2 finite slots", "t3 coupling", "t4 history", "t5 trajectory", "t6 no boundary"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch30-what-is-digital-life-filmstrip.png", columns=7)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch30-what-is-digital-life.gif", duration=760)

    write_provenance(hero, {
        "chapter": "30: What Is Digital Life?",
        "chapter_file": "content/books/digital-life/30-what-is-digital-life/index.md",
        "generator_script": "scripts/books/digital-life/ch30_digital_life_synthesis_visual.py",
        "research_scripts": [
            "scripts/books/digital-life/ch20_digital_crystal_material_loss_v1.py",
            "scripts/books/digital-life/ch25_digital_crystal_finite_budget_redistribution_v1.py",
            "scripts/books/digital-life/ch26_digital_crystal_dynamically_matched_rate_causal_amplification_v2.py",
            "scripts/books/digital-life/ch27_digital_crystal_decaying_material_history_causal_response_v2.py",
            "scripts/books/digital-life/ch28_digital_crystal_causal_modularity_v1.py",
            "scripts/books/digital-life/ch28_digital_crystal_causal_modularity_v2.py",
            "scripts/books/digital-life/ch29_how_to_fail_correctly_v1.py",
        ],
        "artifacts": [
            "research/digital-life/ch20-material-loss-v1/stage-02-loss-sweep.json",
            "research/digital-life/ch25-finite-budget-redistribution-v1/stage-09-verdict.json",
            "research/digital-life/ch26-dynamically-matched-rate-causal-amplification-v2/stage-04-primary-test.json",
            "research/digital-life/ch27-decaying-material-history-causal-response-v2/stage-04-primary.json",
            "research/digital-life/ch28-causal-modularity-v1/stage-03-primary.json",
            "research/digital-life/ch28-causal-modularity-v2/stage-04-primary.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/stage-05-verdict.json",
        ],
        "source": "evidence-grounded synthesis montage using representative Digital Crystal states and canonical artifact statuses",
        "measured_values": evidence,
        "states": "synthesis montage; frames combine representative simulation states with artifact-backed phenomena from different chapter protocols, not one literal continuous experiment",
        "visual_encoding": "occupied/current cells, frontier, finite evaluation slots, hidden-history overlay, causal coupling and soft containment are shown together to summarize process-level evidence",
        "scientific_caveats": [
            "The visual does not claim that the Digital Crystal is alive.",
            "The visual does not encode causal containment as individuality.",
            "The visual does not encode path dependence as readable memory, turnover as repair, finite computation as metabolism, or causal transmission as signalling.",
        ],
        "profile": PROFILE,
        "outputs": ["ch30-what-is-digital-life-hero.png", "ch30-what-is-digital-life-filmstrip.png", "ch30-what-is-digital-life.gif"],
    })
    print(hero)


if __name__ == "__main__":
    main()
