from __future__ import annotations

"""
Upgraded Chapter 01 visual — the pattern moves, the lattice does not.

This version fixes the main issues in the earlier script:
  * captures MANY candidate frames instead of four fixed-timing frames
  * detects the main Lenia organism and rejects edge-clipped candidates
  * selects four cleaner frames automatically
  * builds ONE fixed crop shared by all selected frames
  * avoids the official HUD/scale overlay by cropping around the organism region
  * uses a stronger visible grid and a clearer highlighted stationary patch

The field frames come directly from Bert Chan's official Lenia demo:
    https://chakazul.github.io/Lenia/JavaScript/Lenia.html

Output:
    static/images/books/digital-life/ch01-lenia-fixed-grid-motion.png

Requirements:
    pip install pillow numpy playwright
    playwright install chromium

Run:
    python scripts/books/digital-life/ch01_lenia_fixed_grid.py

Optional:
    python scripts/books/digital-life/ch01_lenia_fixed_grid.py --headful
    python scripts/books/digital-life/ch01_lenia_fixed_grid.py --captures 72 --interval 0.25
"""

import argparse
import base64
import io
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OFFICIAL_LENIA_URL = "https://chakazul.github.io/Lenia/JavaScript/Lenia.html"
OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_PATH = OUTPUT_DIR / "ch01-lenia-fixed-grid-motion.png"


@dataclass
class Component:
    area: int
    bbox: tuple[int, int, int, int]  # x0, y0, x1, y1 inclusive
    centroid: tuple[float, float]


@dataclass
class Candidate:
    index: int
    image: Image.Image
    width: int
    height: int
    component: Component
    score: float


def parse_args():
    parser = argparse.ArgumentParser(
        description="Capture better Lenia frames and render a fixed-grid explanatory figure.",
    )
    parser.add_argument("--settle", type=float, default=2.0)
    parser.add_argument("--interval", type=float, default=0.28)
    parser.add_argument("--captures", type=int, default=56)
    parser.add_argument("--headful", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--grid-step", type=int, default=16)
    parser.add_argument("--panel-size", type=int, default=330)
    parser.add_argument("--edge-margin", type=int, default=18)
    return parser.parse_args()


def require_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        print(
            "\nPlaywright is required.\n\n"
            "Install with:\n"
            "    pip install playwright pillow numpy\n"
            "    playwright install chromium\n",
            file=sys.stderr,
        )
        raise SystemExit(2)


def canvas_png_bytes(page) -> bytes:
    data_url = page.eval_on_selector(
        "#canvas1",
        """canvas => canvas.toDataURL('image/png')""",
    )
    prefix = "data:image/png;base64,"
    if not data_url.startswith(prefix):
        raise RuntimeError("Unexpected canvas data URL")
    return base64.b64decode(data_url[len(prefix):])


def image_from_canvas(page) -> Image.Image:
    raw = canvas_png_bytes(page)
    return Image.open(io.BytesIO(raw)).convert("RGB")


def safe_font(size: int, bold: bool = False):
    candidates = []
    if sys.platform.startswith("win"):
        candidates = [
            Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        ]
    else:
        candidates = [
            Path(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                if bold
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            )
        ]
    for path in candidates:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def lenia_mask(image: Image.Image) -> np.ndarray:
    """
    Heuristic mask for the official Lenia palette.

    Organism colours in the official demo are mainly cyan / blue / magenta,
    while the unwanted HUD/scale marker is orange.
    """
    arr = np.asarray(image, dtype=np.uint8)
    r = arr[..., 0].astype(np.int16)
    g = arr[..., 1].astype(np.int16)
    b = arr[..., 2].astype(np.int16)

    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    sat = maxc - minc

    # Accept saturated cyan/blue/magenta tones; reject orange HUD.
    cyan_or_blue = (b > 135) & (sat > 35)
    magenta = (r > 135) & (b > 135) & (sat > 35)
    not_orange = ~((r > 170) & (g > 90) & (b < 120))
    not_nearly_white = maxc < 252

    mask = (cyan_or_blue | magenta) & not_orange & not_nearly_white

    # Trim 1-pixel noise by requiring a small local neighbourhood support.
    # Simple 3x3 population count with rolls.
    support = np.zeros(mask.shape, dtype=np.uint8)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            support += np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
    mask &= support >= 2

    return mask


def largest_component(mask: np.ndarray) -> Component | None:
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=bool)

    best_area = 0
    best_bbox = None
    best_centroid = None

    for y0 in range(h):
        row = mask[y0]
        for x0 in np.flatnonzero(row & ~visited[y0]):
            stack = [(int(x0), int(y0))]
            visited[y0, x0] = True
            area = 0
            xmin = xmax = int(x0)
            ymin = ymax = int(y0)
            sx = 0.0
            sy = 0.0

            while stack:
                x, y = stack.pop()
                area += 1
                sx += x
                sy += y
                if x < xmin:
                    xmin = x
                if x > xmax:
                    xmax = x
                if y < ymin:
                    ymin = y
                if y > ymax:
                    ymax = y

                x_prev = max(0, x - 1)
                x_next = min(w - 1, x + 1)
                y_prev = max(0, y - 1)
                y_next = min(h - 1, y + 1)
                for ny in range(y_prev, y_next + 1):
                    for nx in range(x_prev, x_next + 1):
                        if not visited[ny, nx] and mask[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((nx, ny))

            if area > best_area:
                best_area = area
                best_bbox = (xmin, ymin, xmax, ymax)
                best_centroid = (sx / area, sy / area)

    if best_bbox is None:
        return None

    return Component(
        area=best_area,
        bbox=best_bbox,
        centroid=best_centroid,
    )


def frame_score(component: Component, width: int, height: int, edge_margin: int) -> float:
    x0, y0, x1, y1 = component.bbox
    margin = min(x0, y0, width - 1 - x1, height - 1 - y1)
    bw = x1 - x0 + 1
    bh = y1 - y0 + 1
    compactness = component.area / max(1.0, bw * bh)
    return margin * 3.0 + math.sqrt(component.area) * 0.8 + compactness * 25.0


def capture_candidates(args) -> list[Candidate]:
    sync_playwright = require_playwright()
    out: list[Candidate] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headful)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})

        print("opening official Lenia demo ...")
        page.goto(OFFICIAL_LENIA_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_selector("#canvas1", state="attached", timeout=30_000)
        print(f"settling for {args.settle:.1f}s ...")
        page.wait_for_timeout(int(args.settle * 1000))

        for i in range(args.captures):
            image = image_from_canvas(page)
            width, height = image.size
            mask = lenia_mask(image)
            component = largest_component(mask)
            if component is not None and component.area >= 100:
                score = frame_score(component, width, height, args.edge_margin)
                out.append(
                    Candidate(
                        index=i,
                        image=image,
                        width=width,
                        height=height,
                        component=component,
                        score=score,
                    )
                )
            page.wait_for_timeout(int(args.interval * 1000))

        browser.close()

    print(f"captured usable candidates: {len(out)} / {args.captures}")
    return out


def acceptable(candidate: Candidate, edge_margin: int) -> bool:
    x0, y0, x1, y1 = candidate.component.bbox
    return (
        x0 >= edge_margin
        and y0 >= edge_margin
        and x1 <= candidate.width - 1 - edge_margin
        and y1 <= candidate.height - 1 - edge_margin
        and candidate.component.area >= 140
    )


def choose_frames(candidates: list[Candidate], edge_margin: int) -> list[Candidate]:
    good = [c for c in candidates if acceptable(c, edge_margin)]
    if len(good) < 4:
        # Fall back to best-scoring candidates if the strict filter is too harsh.
        print("warning: fewer than 4 strictly acceptable frames, relaxing filter")
        good = sorted(candidates, key=lambda c: c.score, reverse=True)
    else:
        good = sorted(good, key=lambda c: c.index)

    # Split into four chronological buckets and pick the best candidate in each.
    if len(good) >= 4:
        buckets: list[list[Candidate]] = [[] for _ in range(4)]
        idxs = [c.index for c in good]
        min_i = min(idxs)
        max_i = max(idxs)
        span = max(1, max_i - min_i + 1)
        for c in good:
            b = min(3, int(4 * (c.index - min_i) / span))
            buckets[b].append(c)

        chosen: list[Candidate] = []
        for bucket in buckets:
            if bucket:
                chosen.append(max(bucket, key=lambda c: c.score))

        # If some buckets were empty, fill remaining spots with best non-duplicate frames.
        if len(chosen) < 4:
            used = {c.index for c in chosen}
            for c in sorted(good, key=lambda c: c.score, reverse=True):
                if c.index not in used:
                    chosen.append(c)
                    used.add(c.index)
                if len(chosen) == 4:
                    break
    else:
        chosen = good[:4]

    # Ensure four unique, sorted frames.
    unique = {}
    for c in chosen:
        unique[c.index] = c
    chosen = [unique[k] for k in sorted(unique)]

    if len(chosen) < 4:
        raise RuntimeError("Could not find four suitable Lenia frames. Try --captures 80 or --headful.")

    # Keep the four earliest unique sorted by time if more than 4 slipped in.
    chosen = chosen[:4]

    print("selected frame indices:", [c.index for c in chosen])
    for c in chosen:
        print(
            f"  frame {c.index}: area={c.component.area} bbox={c.component.bbox} centroid=({c.component.centroid[0]:.1f}, {c.component.centroid[1]:.1f})"
        )
    return chosen


def compute_fixed_crop(selected: list[Candidate]) -> tuple[int, int, int, int]:
    x0s = [c.component.bbox[0] for c in selected]
    y0s = [c.component.bbox[1] for c in selected]
    x1s = [c.component.bbox[2] for c in selected]
    y1s = [c.component.bbox[3] for c in selected]

    width = selected[0].width
    height = selected[0].height

    xmin = min(x0s)
    ymin = min(y0s)
    xmax = max(x1s)
    ymax = max(y1s)

    # Add generous margin so motion is visible and the crop stays explanatory.
    pad_x = 36
    pad_y = 36
    xmin -= pad_x
    ymin -= pad_y
    xmax += pad_x
    ymax += pad_y

    # Force a square crop.
    crop_w = xmax - xmin + 1
    crop_h = ymax - ymin + 1
    side = max(crop_w, crop_h)
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0

    xmin = int(round(cx - side / 2.0))
    ymin = int(round(cy - side / 2.0))
    xmax = xmin + side - 1
    ymax = ymin + side - 1

    # Clamp to field bounds.
    if xmin < 0:
        xmax -= xmin
        xmin = 0
    if ymin < 0:
        ymax -= ymin
        ymin = 0
    if xmax >= width:
        shift = xmax - (width - 1)
        xmin -= shift
        xmax -= shift
    if ymax >= height:
        shift = ymax - (height - 1)
        ymin -= shift
        ymax -= shift

    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(width - 1, xmax)
    ymax = min(height - 1, ymax)

    print(f"fixed crop: {(xmin, ymin, xmax, ymax)}")
    return xmin, ymin, xmax, ymax


def choose_stationary_patch(crop_box: tuple[int, int, int, int], selected: list[Candidate]) -> tuple[int, int, int, int]:
    xmin, ymin, xmax, ymax = crop_box
    side = xmax - xmin + 1

    # Use the union of selected organism bboxes in crop coordinates to avoid overlap.
    ux0 = min(c.component.bbox[0] for c in selected) - xmin
    uy0 = min(c.component.bbox[1] for c in selected) - ymin
    ux1 = max(c.component.bbox[2] for c in selected) - xmin
    uy1 = max(c.component.bbox[3] for c in selected) - ymin

    patch_side = max(10, side // 10)
    candidate_patches = [
        (int(side * 0.08), int(side * 0.08)),
        (int(side * 0.72), int(side * 0.08)),
        (int(side * 0.08), int(side * 0.72)),
        (int(side * 0.72), int(side * 0.72)),
        (int(side * 0.08), int(side * 0.42)),
    ]

    def overlap(a, b):
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        return not (ax1 < bx0 or bx1 < ax0 or ay1 < by0 or by1 < ay0)

    union_box = (ux0, uy0, ux1, uy1)

    for px, py in candidate_patches:
        patch = (px, py, px + patch_side, py + patch_side)
        if not overlap(patch, union_box):
            return patch

    # Last resort: top-left.
    return (int(side * 0.08), int(side * 0.08), int(side * 0.08) + patch_side, int(side * 0.08) + patch_side)


def crop_image(image: Image.Image, crop_box: tuple[int, int, int, int]) -> Image.Image:
    xmin, ymin, xmax, ymax = crop_box
    return image.crop((xmin, ymin, xmax + 1, ymax + 1))


def draw_overlay(
    crop: Image.Image,
    panel_size: int,
    grid_step_cells: int,
    patch_box_crop: tuple[int, int, int, int],
    panel_index: int,
) -> Image.Image:
    crop = crop.resize((panel_size, panel_size), Image.Resampling.NEAREST).convert("RGBA")
    overlay = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    side_px = crop.size[0]
    # The crop itself is the fixed lattice view; grid step is proportional to crop width.
    crop_field_side = max(1, patch_box_crop[2] - patch_box_crop[0])  # not actually field side, just to keep lints happy
    del crop_field_side

    # Use panel-space grid divisions based on the original 128-cell field idea but adapted to crop.
    divisions = 8
    step = side_px / divisions
    for k in range(divisions + 1):
        p = int(round(k * step))
        draw.line([(p, 0), (p, side_px)], fill=(90, 90, 90, 155), width=1)
        draw.line([(0, p), (side_px, p)], fill=(90, 90, 90, 155), width=1)

    px0, py0, px1, py1 = patch_box_crop
    # patch_box_crop is in crop coordinates. Rescale to panel.
    scale = side_px / crop.size[0]
    # Since crop has already been resized, use the original crop pixel dimensions before resize.
    # We recover it from patch_box directly relative to original crop side through current size ratio.
    # Easier approach: store crop side in closure would be cleaner, but this works if we pass original coords.
    # Instead compute by assuming patch coords already refer to original crop pixels and original side == current side/scale.
    # So we need the original side. We infer from the max patch coord not enough; better use simple ratio externally.
    # To avoid that complexity, we reinterpret patch_box_crop as fractions already computed in caller. But current caller
    # passes original crop coords. So here we use the hidden fact that crop was resized from a square image of width original_side.
    # PIL doesn't preserve it, so compute from panel and patch fractions outside is better. We'll instead rescale by the original
    # crop dimensions passed through image info if present.
    original_side = crop.info.get("original_side", None)
    if original_side is None:
        original_side = panel_size
    scale = side_px / float(original_side)

    x0 = int(round(px0 * scale))
    y0 = int(round(py0 * scale))
    x1 = int(round(px1 * scale))
    y1 = int(round(py1 * scale))

    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 28), outline=(255, 255, 255, 245), width=3)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.line([(cx - 8, cy), (cx + 8, cy)], fill=(255, 255, 255, 245), width=2)
    draw.line([(cx, cy - 8), (cx, cy + 8)], fill=(255, 255, 255, 245), width=2)

    crop = Image.alpha_composite(crop, overlay).convert("RGB")

    label_height = 54
    composed = Image.new("RGB", (panel_size, panel_size + label_height), (248, 248, 248))
    composed.paste(crop, (0, label_height))
    draw = ImageDraw.Draw(composed)
    font = safe_font(21, bold=True)
    small = safe_font(15)
    draw.text((16, 9), f"Frame {panel_index + 1}", fill=(22, 22, 22), font=font)
    draw.text((panel_size - 114, 15), "fixed lattice", fill=(70, 70, 70), font=small)
    return composed


def compose_figure(selected: list[Candidate], args):
    args.output.parent.mkdir(parents=True, exist_ok=True)
    crop_box = compute_fixed_crop(selected)
    xmin, ymin, xmax, ymax = crop_box
    original_crop_side = xmax - xmin + 1
    patch_box = choose_stationary_patch(crop_box, selected)
    print(f"stationary patch in crop coords: {patch_box}")

    rendered = []
    for idx, candidate in enumerate(selected):
        crop = crop_image(candidate.image, crop_box)
        # Smuggle original side through PIL info for overlay scaling.
        crop.info["original_side"] = original_crop_side
        rendered.append(
            draw_overlay(
                crop=crop,
                panel_size=args.panel_size,
                grid_step_cells=args.grid_step,
                patch_box_crop=patch_box,
                panel_index=idx,
            )
        )

    gap = 16
    top = 92
    bottom = 78
    margin = 28
    panel_h = rendered[0].height
    width = margin * 2 + args.panel_size * 4 + gap * 3
    height = top + panel_h + bottom
    canvas = Image.new("RGB", (width, height), (252, 252, 252))

    for idx, panel in enumerate(rendered):
        x = margin + idx * (args.panel_size + gap)
        canvas.paste(panel, (x, top))

    draw = ImageDraw.Draw(canvas)
    title_font = safe_font(33, bold=True)
    subtitle_font = safe_font(19)
    footer_font = safe_font(17)

    draw.text((margin, 18), "The pattern moves. The lattice does not.", fill=(18, 18, 18), font=title_font)
    draw.text(
        (margin, 58),
        "Four frames from the same fixed Lenia field view; grid coordinates and highlighted patch remain fixed.",
        fill=(70, 70, 70),
        font=subtitle_font,
    )

    footer = (
        "White square = the same stationary region of the field in every frame. "
        "Only the field state changes."
    )
    draw.text((margin, height - 47), footer, fill=(55, 55, 55), font=footer_font)

    canvas.save(args.output, dpi=(200, 200))
    print(f"saved: {args.output}")


def main():
    args = parse_args()
    candidates = capture_candidates(args)
    if not candidates:
        raise RuntimeError("No usable Lenia candidates captured. Try --headful.")
    selected = choose_frames(candidates, args.edge_margin)
    compose_figure(selected, args)


if __name__ == "__main__":
    main()
