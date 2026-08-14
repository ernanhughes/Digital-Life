#!/usr/bin/env python3
"""
Extract ## and ### headings from the Digital Life manuscript.

Outputs:

    digital-life-sections.md
    digital-life-sections.csv

The CSV is designed to become the structural migration ledger:

    source_chapter
    source_file
    line
    level
    heading
    target_part
    target_chapter
    target_section
    disposition
    notes

Usage:

    python extract_digital_life_sections.py path/to/content/books/digital-life

Example:

    python extract_digital_life_sections.py content/books/digital-life
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(##|###)\s+(.+?)\s*$")

# Files at the root of digital-life that are not manuscript chapters.
ROOT_EXCLUDES = {
    "_index.md",
    "digital-life.codebase.md",
}


@dataclass
class Section:
    chapter: str
    source_file: str
    line: int
    level: int
    heading: str


def sort_key(path: Path) -> tuple:
    """
    Natural-ish ordering for chapter directories:

        00-...
        01-...
        ...
        30-...
        99-appendix
    """
    name = path.parent.name

    match = re.match(r"^(\d+)", name)
    if match:
        return int(match.group(1)), name, path.name

    return 9999, name, path.name


def find_manuscript_files(root: Path) -> list[Path]:
    files: list[Path] = []

    # Normal chapter directories.
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)

        # Skip root-level support files.
        if len(relative.parts) == 1 and path.name in ROOT_EXCLUDES:
            continue

        files.append(path)

    return sorted(files, key=sort_key)


def chapter_name(root: Path, path: Path) -> str:
    relative = path.relative_to(root)

    # Normal chapters:
    # 11-the-crystal/index.md
    if len(relative.parts) >= 2:
        if relative.parts[0] == "99-appendix":
            return f"99-appendix/{path.stem}"
        return relative.parts[0]

    return path.stem


def extract_sections(root: Path, path: Path) -> list[Section]:
    sections: list[Section] = []

    in_fence = False
    fence_marker: str | None = None

    text = path.read_text(encoding="utf-8")

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()

        # Ignore headings occurring inside fenced code blocks.
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]

            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None

            continue

        if in_fence:
            continue

        match = HEADING_RE.match(raw_line)

        if not match:
            continue

        hashes, heading = match.groups()

        sections.append(
            Section(
                chapter=chapter_name(root, path),
                source_file=str(path.relative_to(root)),
                line=line_number,
                level=len(hashes),
                heading=heading.strip(),
            )
        )

    return sections


def write_csv(sections: list[Section], destination: Path) -> None:
    columns = [
        "source_chapter",
        "source_file",
        "line",
        "level",
        "heading",
        "target_part",
        "target_chapter",
        "target_section",
        "disposition",
        "notes",
    ]

    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()

        for section in sections:
            writer.writerow(
                {
                    "source_chapter": section.chapter,
                    "source_file": section.source_file,
                    "line": section.line,
                    "level": section.level,
                    "heading": section.heading,

                    # Filled in during structural editing.
                    "target_part": "",
                    "target_chapter": "",
                    "target_section": "",
                    "disposition": "",
                    "notes": "",
                }
            )


def write_markdown(sections: list[Section], destination: Path) -> None:
    lines = [
        "# Digital Life — Existing Section Map",
        "",
        "Generated from the current manuscript.",
        "",
        "Only `##` and `###` headings are included.",
        "",
    ]

    current_chapter: str | None = None

    for section in sections:
        if section.chapter != current_chapter:
            current_chapter = section.chapter

            lines.extend(
                [
                    "",
                    f"# {current_chapter}",
                    "",
                    f"`{section.source_file}`",
                    "",
                ]
            )

        indent = "  " if section.level == 3 else ""
        marker = "-" if section.level == 2 else "  -"

        lines.append(
            f"{indent}{marker} "
            f"**{section.heading}** "
            f"`L{section.line}`"
        )

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract ## and ### headings from Digital Life."
    )

    parser.add_argument(
        "root",
        type=Path,
        help="Path to content/books/digital-life",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for generated files (default: current directory)",
    )

    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir.resolve()

    if not root.exists():
        raise SystemExit(f"Directory does not exist: {root}")

    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    output_dir.mkdir(parents=True, exist_ok=True)

    manuscript_files = find_manuscript_files(root)

    sections: list[Section] = []

    for path in manuscript_files:
        sections.extend(extract_sections(root, path))

    markdown_path = output_dir / "digital-life-sections.md"
    csv_path = output_dir / "digital-life-sections.csv"

    write_markdown(sections, markdown_path)
    write_csv(sections, csv_path)

    print(f"Scanned {len(manuscript_files)} manuscript files")
    print(f"Found {len(sections)} ## / ### sections")
    print()
    print(f"Markdown: {markdown_path}")
    print(f"CSV:      {csv_path}")


if __name__ == "__main__":
    main()