from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

PROFILE = "quick"
EXPORT = True
EXPORT_HERO = True
EXPORT_FILMSTRIP = True
EXPORT_GIF = True
EXPORT_MP4 = False
SEED = 2901


def find_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "hugo.toml").exists():
            return p
    raise RuntimeError("repo root not found")


ROOT = find_root()
sys.path.insert(0, str(ROOT / "notebooks" / "_shared"))
sys.path.insert(0, str(ROOT / "scripts" / "books" / "digital-life"))

from digital_crystal import frontier, run_crystal  # noqa: E402
from visualization.digital_crystal_renderer import (  # noqa: E402
    COLORS,
    draw_cells,
    draw_markers,
    draw_outlines,
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

STATUS_COLORS = {
    "INVALID": "negative",
    "UNRESOLVED": "module",
    "BOUNDED_NEAR_ZERO": "intervention",
    "BOUNDED_BELOW_SEI": "intervention",
    "SUPPORTED": "swapped_in",
    "DIRECTION_SUPPORTED": "positive",
    "DESCRIPTIVE_ONLY": "hidden",
}


def load_json(path: str):
    full = ROOT / path
    if not full.exists():
        raise FileNotFoundError(f"required artifact missing: {full}")
    return json.loads(full.read_text(encoding="utf-8"))


def status_color(status: str) -> str:
    return COLORS[STATUS_COLORS.get(status, "muted")]


def add_box(ax, xy, width, height, title, subtitle, *, status=None, alpha=0.95):
    color = status_color(status) if status else COLORS["grid"]
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        facecolor=COLORS["panel"],
        edgecolor=color,
        linewidth=1.8,
        alpha=alpha,
    )
    ax.add_patch(box)
    ax.text(xy[0] + 0.04, xy[1] + height - 0.08, title, color=COLORS["text"], fontsize=10.5, fontweight="bold", va="top")
    if subtitle:
        ax.text(xy[0] + 0.04, xy[1] + height - 0.22, subtitle, color=COLORS["muted"], fontsize=8.0, va="top", linespacing=1.1)
    if status:
        ax.text(xy[0] + width - 0.04, xy[1] + 0.055, status.replace("_", " "), color=color, fontsize=7.2, ha="right", va="bottom", fontweight="bold")


def add_arrow(ax, start, end, *, color="muted", alpha=0.75):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.3, color=COLORS[color], alpha=alpha))


def ledger_summary(rows):
    return Counter(r["inferential_status"] for r in rows)


def draw_status_bar(ax, rows, *, y=0.08, show_caption=True):
    counts = ledger_summary(rows)
    order = ["INVALID", "UNRESOLVED", "BOUNDED_NEAR_ZERO", "BOUNDED_BELOW_SEI", "SUPPORTED", "DIRECTION_SUPPORTED", "DESCRIPTIVE_ONLY"]
    x0 = 0.08
    total = sum(counts.values())
    cursor = x0
    for status in order:
        n = counts.get(status, 0)
        if not n:
            continue
        w = 0.78 * n / total
        ax.add_patch(FancyBboxPatch((cursor, y), w, 0.055, boxstyle="round,pad=0.01", facecolor=status_color(status), edgecolor="none", alpha=0.82))
        ax.text(cursor + w / 2, y + 0.076, str(n), color=COLORS["text"], ha="center", va="bottom", fontsize=7.5, fontweight="bold")
        cursor += w + 0.008
    if show_caption:
        ax.text(x0, y - 0.035, "10 registered cases, multiple inferential statuses", color=COLORS["muted"], fontsize=8, va="top")


def draw_crystal_anchor(ax, chapter: int, title: str, status: str, *, steps: int):
    state = run_crystal([0.18 + 0.01 * (chapter % 3)] * steps, seed=SEED + chapter, max_radius=9)
    occupied = set(state.occupied)
    front = frontier(occupied, 9)
    draw_cells(ax, occupied, alpha=0.78)
    draw_outlines(ax, front, color="frontier", alpha=0.22)
    sample = sorted(front)[: max(7, len(front) // 10)]
    draw_markers(ax, sample, color=STATUS_COLORS.get(status, "intervention"), size=0.15, alpha=0.75)
    draw_title(ax, title, status.replace("_", " "))
    frame(ax, sorted(occupied | front))


def render_hero(rows, verdict):
    fig, axes = setup_figure(4, width=13.6, height=5.25, title="Chapter 29: failing correctly preserves the evidence that still survives")
    anchors = [
        (26, "Ch26 control", "BOUNDED_NEAR_ZERO", 17),
        (27, "Ch27 intervention", "UNRESOLVED", 19),
        (28, "Ch28 stronger control", "BOUNDED_BELOW_SEI", 21),
    ]
    for ax, (chapter, title, status, steps) in zip(axes[:3], anchors):
        draw_crystal_anchor(ax, chapter, title, status, steps=steps)
    ax = axes[3]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_box(ax, (0.07, 0.74), 0.80, 0.15, "EXPERIMENT", "evidence enters")
    add_box(ax, (0.04, 0.52), 0.37, 0.14, "INVALID", "not negative", status="INVALID")
    add_box(ax, (0.51, 0.52), 0.40, 0.14, "UNRESOLVED", "needs precision", status="UNRESOLVED")
    add_box(ax, (0.04, 0.31), 0.42, 0.14, "BOUNDED", "threshold met", status="BOUNDED_NEAR_ZERO")
    add_box(ax, (0.52, 0.31), 0.40, 0.14, "SURVIVES", "evidence kept", status="SUPPORTED")
    for end in [(0.23, 0.63), (0.71, 0.63), (0.25, 0.40), (0.72, 0.40)]:
        add_arrow(ax, (0.47, 0.72), end, color="muted")
    draw_status_bar(ax, rows, y=0.09)
    ax.text(0.06, 0.94, verdict["status"], color=COLORS["text"], fontsize=10, fontweight="bold")
    return fig


def render_stage(title, subtitle, visible_statuses, rows, *, show_removed=False):
    fig, axes = setup_figure(1, width=5.25, height=4.35)
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    draw_title(ax, title, subtitle)
    x_positions = [0.18, 0.50, 0.82]
    labels = ["Ch26", "Ch27", "Ch28"]
    for x, label in zip(x_positions, labels):
        ax.add_patch(FancyBboxPatch((x - 0.11, 0.58), 0.22, 0.18, boxstyle="round,pad=0.02", facecolor=COLORS["grid"], edgecolor=COLORS["frontier"], linewidth=1.0))
        ax.text(x, 0.67, label, color=COLORS["text"], ha="center", va="center", fontsize=11, fontweight="bold")
        add_arrow(ax, (x, 0.57), (x, 0.43), color="muted")
    for i, status in enumerate(visible_statuses):
        x = x_positions[i % 3]
        y = 0.24 if i < 3 else 0.07
        add_box(ax, (x - 0.135, y), 0.27, 0.13, status.replace("_", " "), "", status=status)
    if show_removed:
        ax.plot([0.11, 0.89], [0.52, 0.52], color=COLORS["negative"], linewidth=1.6, alpha=0.7)
        ax.text(0.5, 0.49, "failed inference removed", color=COLORS["negative"], fontsize=8, ha="center", va="top")
    draw_status_bar(ax, rows)
    return fig


def main():
    ledger = load_json("research/digital-life/ch29-how-to-fail-correctly-v1/ch29-failure-ledger.json")
    artifact_audit = load_json("research/digital-life/ch29-how-to-fail-correctly-v1/ch29-artifact-audit.json")
    consistency = load_json("research/digital-life/ch29-how-to-fail-correctly-v1/stage-03-consistency.json")
    verdict = load_json("research/digital-life/ch29-how-to-fail-correctly-v1/stage-05-verdict.json")
    rows = ledger["rows"]

    hero = OUT / "ch29-how-to-fail-correctly-hero.png"
    if EXPORT_HERO:
        save_png(render_hero(rows, verdict), hero)

    frames = [
        fig_to_image(render_stage("CLAIM APPEARS", "registered Ch26-Ch28 evidence enters", ["SUPPORTED", "DIRECTION_SUPPORTED", "SUPPORTED"], rows)),
        fig_to_image(render_stage("VALIDITY CHECK", "implementation/control defects are isolated", ["INVALID", "INVALID", "SUPPORTED"], rows, show_removed=True)),
        fig_to_image(render_stage("SURVIVING EVIDENCE", "valid sub-results remain visible", ["DESCRIPTIVE_ONLY", "SUPPORTED", "SUPPORTED"], rows)),
        fig_to_image(render_stage("STRONGER CONTROL", "interpretation narrows without erasure", ["BOUNDED_NEAR_ZERO", "UNRESOLVED", "BOUNDED_BELOW_SEI"], rows)),
        fig_to_image(render_stage("FINAL LEDGER", verdict["status"], ["INVALID", "UNRESOLVED", "BOUNDED_NEAR_ZERO", "SUPPORTED", "DIRECTION_SUPPORTED", "DESCRIPTIVE_ONLY"], rows)),
    ]
    labels = ["t0 claim", "t1 validity", "t2 survives", "t3 stronger control", "t4 ledger"]
    if EXPORT_FILMSTRIP:
        save_filmstrip(frames, labels, OUT / "ch29-how-to-fail-correctly-filmstrip.png", columns=5)
    if EXPORT_GIF:
        save_gif(frames, OUT / "ch29-how-to-fail-correctly.gif", duration=760)

    write_provenance(hero, {
        "chapter": "29: How to Fail Correctly",
        "chapter_file": "content/books/digital-life/29-how-to-fail-correctly/index.md",
        "generator_script": "scripts/books/digital-life/ch29_fail_correctly_visual.py",
        "research_scripts": ["scripts/books/digital-life/ch29_how_to_fail_correctly_v1.py"],
        "artifacts": [
            "research/digital-life/ch29-how-to-fail-correctly-v1/ch29-failure-ledger.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/ch29-artifact-audit.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/stage-01-artifacts.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/stage-02-ledger.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/stage-03-consistency.json",
            "research/digital-life/ch29-how-to-fail-correctly-v1/stage-05-verdict.json",
        ],
        "source": "evidence-ledger-derived epistemic audit representation; not a new Digital Crystal simulation",
        "measured_values": {
            "registered_cases": len(rows),
            "artifact_cases": artifact_audit["metadata"]["registered_cases"],
            "case_rule_pass_count": consistency["case_rule_pass_count"],
            "case_rule_total": consistency["case_rule_total"],
            "cross_check_pass_count": sum(c["pass"] for c in consistency["cross_checks"]),
            "cross_check_total": len(consistency["cross_checks"]),
            "status": verdict["status"],
            "status_counts": dict(ledger_summary(rows)),
        },
        "states": "representative Digital Crystal states provide chapter anchors only; statuses and transitions are actual ledger entries",
        "visual_encoding": "ledger statuses are color-coded; invalid inferences are removed while surviving evidence remains highlighted",
        "scientific_caveats": [
            "Chapter 29 is an epistemic audit representation, not a new behavior experiment.",
            "INVALID is not encoded as negative evidence.",
            "DESCRIPTIVE_ONLY is not encoded as confirmatory rescue.",
        ],
        "profile": PROFILE,
        "outputs": ["ch29-how-to-fail-correctly-hero.png", "ch29-how-to-fail-correctly-filmstrip.png", "ch29-how-to-fail-correctly.gif"],
    })
    print(hero)


if __name__ == "__main__":
    main()
