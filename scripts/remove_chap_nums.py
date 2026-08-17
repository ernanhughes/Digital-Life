#!/usr/bin/env python3
"""
fix_chapter_references.py

Remove fragile hard-coded "Chapter N" references from the Digital Life
manuscript.

Strategy
--------
* Immediate predecessor:
      Chapter N -> the previous chapter

* Current chapter:
      Chapter N -> this chapter

* Earlier non-adjacent chapter:
      Chapter N -> the *Chapter Title* chapter

* Old chapter that no longer resolves:
      Chapter N -> an earlier chapter

* Explicit "Old Chapter N":
      Old Chapter N -> an earlier draft

The script knows about the legacy numbering still present in the current
manuscript. Everything else is resolved against the current chapter numbers.

SAFE BY DEFAULT:
    Running without --apply only prints a diff.

WITH --apply:
    Creates a timestamped backup before modifying anything.

Usage
-----

Preview:

    python fix_chapter_references.py

Apply:

    python fix_chapter_references.py --apply

Different book directory:

    python fix_chapter_references.py \
        --root content/books/digital-life \
        --apply
"""

from __future__ import annotations

import argparse
import csv
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


DEFAULT_ROOT = Path("content/books/digital-life")


# ---------------------------------------------------------------------------
# Legacy reference resolution
# ---------------------------------------------------------------------------
#
# Key:
#     (CURRENT SOURCE CHAPTER, OLD REFERENCED NUMBER)
#
# Value:
#     CURRENT TARGET CHAPTER
#
# These are deliberately source-specific because the manuscript has passed
# through more than one numbering scheme. There is NOT one global offset.
#
# Add entries here if the report exposes another old-number reference whose
# target you know.
#

LEGACY_TARGETS: dict[tuple[int, int], int] = {
    # Early restructuring
    (4, 1): 2,

    # Current Chapter 9 was old Chapter 6-ish material, etc.
    (9, 5): 8,

    (10, 6): 9,

    (11, 4): 7,
    (11, 7): 10,

    (12, 3): 6,
    (12, 5): 8,
    (12, 6): 9,
    (12, 7): 10,
    (12, 8): 11,
    (12, 9): 12,

    (13, 5): 8,
    (13, 6): 9,
    (13, 8): 11,
    (13, 9): 12,

    (14, 6): 9,
    (14, 8): 11,
    (14, 10): 13,
    (14, 11): 14,

    (15, 5): 8,
    (15, 6): 9,
    (15, 9): 12,
    (15, 10): 13,
    (15, 11): 14,

    (16, 6): 9,
    (16, 9): 12,
    (16, 10): 13,
    (16, 11): 14,
    (16, 12): 15,
    (16, 13): 16,

    (17, 3): 6,
    (17, 6): 9,
    (17, 8): 11,
    (17, 9): 12,
    (17, 10): 13,
    (17, 11): 14,
    (17, 12): 15,
    (17, 13): 16,

    # Most of Ch18 still uses the +3 legacy numbering,
    # but its Outlier reproduction reference is an older exception.
    (18, 2): 4,
    (18, 9): 12,
    (18, 13): 16,
    (18, 14): 17,
}


# Chapter references sometimes work adjectivally:
#
#     Chapter 11 experiment
#     Chapter 6 result
#
# Blind substitution would produce:
#
#     this chapter experiment
#
# So these get special handling.
REFERENCE_NOUNS = {
    "analysis",
    "argument",
    "claim",
    "comparison",
    "control",
    "correction",
    "design",
    "experiment",
    "failure",
    "finding",
    "measurement",
    "mechanism",
    "method",
    "null",
    "result",
    "rule",
    "test",
}


CHAPTER_FILE_RE = re.compile(r"^(?P<number>\d+)-.+\.md$", re.I)

TITLE_RE = re.compile(
    r'^\s*title\s*=\s*"(?P<title>.*?)"\s*$',
    re.MULTILINE,
)

OLD_CHAPTER_RE = re.compile(
    r"\bOld\s+Chapter\s+\d+\b",
    re.IGNORECASE,
)

CHAPTER_RE = re.compile(
    r"\bChapter\s+(?P<number>\d+)(?P<possessive>['’]s)?\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Directory containing the Digital Life markdown chapters.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually modify files. Without this flag only a diff is shown.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("chapter-reference-report.csv"),
        help="CSV report written after scanning.",
    )
    return parser.parse_args()


def chapter_number(path: Path) -> int | None:
    match = CHAPTER_FILE_RE.match(path.name)
    if not match:
        return None
    return int(match.group("number"))


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")

    match = TITLE_RE.search(text)
    if not match:
        return path.stem

    title = match.group("title").strip()

    # Turn:
    #
    #     07: The Digital Crystal
    #
    # into:
    #
    #     The Digital Crystal
    #
    title = re.sub(r"^\d+\s*:\s*", "", title)

    return title


def discover_chapters(root: Path) -> dict[int, tuple[Path, str]]:
    chapters: dict[int, tuple[Path, str]] = {}

    for path in sorted(root.glob("*.md")):
        number = chapter_number(path)
        if number is None:
            continue

        chapters[number] = (path, extract_title(path))

    return chapters


def resolve_target(
    source_number: int,
    cited_number: int,
    chapters: dict[int, tuple[Path, str]],
) -> tuple[int | None, str]:
    """
    Return:

        (current target chapter number, resolution method)
    """

    override = LEGACY_TARGETS.get((source_number, cited_number))
    if override is not None:
        return override, "legacy-map"

    # Otherwise assume this reference is already using current numbering.
    if cited_number in chapters:
        return cited_number, "current-number"

    return None, "unresolved"


def reference_phrase(
    source_number: int,
    target_number: int | None,
    chapters: dict[int, tuple[Path, str]],
) -> str:
    if target_number is None:
        return "an earlier chapter"

    if target_number == source_number:
        return "this chapter"

    if target_number == source_number - 1:
        return "the previous chapter"

    if target_number < source_number:
        target = chapters.get(target_number)

        if target is None:
            return "an earlier chapter"

        _, title = target
        return f"the *{title}* chapter"

    # We should rarely have forward references in this manuscript.
    target = chapters.get(target_number)

    if target is not None:
        _, title = target
        return f"the later *{title}* chapter"

    return "a later chapter"


def capitalize_like_original(original: str, replacement: str) -> str:
    if original and original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def rewrite_line(
    line: str,
    source_number: int,
    chapters: dict[int, tuple[Path, str]],
    line_number: int,
    filename: str,
    changes: list[dict[str, object]],
) -> str:

    # ------------------------------------------------------------------
    # "Old Chapter 27"
    # ------------------------------------------------------------------

    def replace_old(match: re.Match[str]) -> str:
        old = match.group(0)

        replacement = "an earlier draft"

        if old[0].isupper():
            replacement = "An earlier draft"

        changes.append(
            {
                "file": filename,
                "line": line_number,
                "old": old,
                "new": replacement,
                "source_chapter": source_number,
                "cited_number": "",
                "target_chapter": "",
                "resolution": "old-draft",
            }
        )

        return replacement

    line = OLD_CHAPTER_RE.sub(replace_old, line)

    # ------------------------------------------------------------------
    # Normal "Chapter N"
    # ------------------------------------------------------------------

    def replace_chapter(match: re.Match[str]) -> str:
        old = match.group(0)

        cited_number = int(match.group("number"))
        possessive = match.group("possessive")

        target_number, resolution = resolve_target(
            source_number,
            cited_number,
            chapters,
        )

        phrase = reference_phrase(
            source_number,
            target_number,
            chapters,
        )

        if possessive:
            phrase += "'s"

        # Preserve sentence-start capitalization reasonably well.
        start = match.start()
        before = line[:start]

        if not before.strip():
            phrase = phrase[0].upper() + phrase[1:]

        changes.append(
            {
                "file": filename,
                "line": line_number,
                "old": old,
                "new": phrase,
                "source_chapter": source_number,
                "cited_number": cited_number,
                "target_chapter": target_number or "",
                "resolution": resolution,
            }
        )

        return phrase

    line = CHAPTER_RE.sub(replace_chapter, line)

    # ------------------------------------------------------------------
    # Repair common adjectival constructions caused by substitution.
    #
    # Example:
    #
    #     the matched this chapter experiment
    #
    # becomes:
    #
    #     the matched experiment in this chapter
    #
    # We deliberately keep this limited rather than trying to become a
    # natural-language rewriting engine.
    # ------------------------------------------------------------------

    noun_alt = "|".join(sorted(REFERENCE_NOUNS, key=len, reverse=True))

    line = re.sub(
        rf"\bthis chapter (?P<noun>{noun_alt})\b",
        lambda m: f"{m.group('noun')} in this chapter",
        line,
        flags=re.IGNORECASE,
    )

    line = re.sub(
        rf"\bthe previous chapter (?P<noun>{noun_alt})\b",
        lambda m: f"{m.group('noun')} in the previous chapter",
        line,
        flags=re.IGNORECASE,
    )

    return line


def rewrite_file(
    path: Path,
    source_number: int,
    chapters: dict[int, tuple[Path, str]],
    changes: list[dict[str, object]],
) -> tuple[str, str]:
    old_text = path.read_text(encoding="utf-8")

    new_lines: list[str] = []

    for line_number, line in enumerate(old_text.splitlines(keepends=True), start=1):
        new_lines.append(
            rewrite_line(
                line=line,
                source_number=source_number,
                chapters=chapters,
                line_number=line_number,
                filename=str(path),
                changes=changes,
            )
        )

    new_text = "".join(new_lines)

    return old_text, new_text


def print_diff(path: Path, old: str, new: str) -> None:
    if old == new:
        return

    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=str(path),
        tofile=str(path),
        lineterm="",
    )

    print("\n".join(diff))
    print()


def write_report(path: Path, changes: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file",
        "line",
        "source_chapter",
        "cited_number",
        "target_chapter",
        "resolution",
        "old",
        "new",
    ]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(changes)


def make_backup(
    root: Path,
    changed_paths: list[Path],
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    backup_root = (
        root.parent
        / f".digital-life-chapter-ref-backup-{timestamp}"
    )

    backup_root.mkdir(parents=True, exist_ok=True)

    for source in changed_paths:
        target = backup_root / source.name
        shutil.copy2(source, target)

    return backup_root


def remaining_numeric_references(root: Path) -> list[tuple[Path, int, str]]:
    remaining = []

    for path in sorted(root.glob("*.md")):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if CHAPTER_RE.search(line) or OLD_CHAPTER_RE.search(line):
                remaining.append((path, line_number, line.strip()))

    return remaining


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    if not root.exists():
        raise SystemExit(f"Book directory does not exist: {root}")

    chapters = discover_chapters(root)

    if not chapters:
        raise SystemExit(f"No numbered markdown chapters found in {root}")

    print("Current chapter map:\n")

    for number, (_, title) in sorted(chapters.items()):
        print(f"  {number:02d}  {title}")

    changes: list[dict[str, object]] = []
    rewrites: dict[Path, tuple[str, str]] = {}

    print("\nProposed changes:\n")

    for source_number, (path, _) in sorted(chapters.items()):
        old_text, new_text = rewrite_file(
            path,
            source_number,
            chapters,
            changes,
        )

        if old_text != new_text:
            rewrites[path] = (old_text, new_text)
            print_diff(path, old_text, new_text)

    write_report(args.report, changes)

    print(f"\nReference report: {args.report}")
    print(f"References found: {len(changes)}")
    print(f"Files affected: {len(rewrites)}")

    unresolved = [
        c for c in changes
        if c["resolution"] == "unresolved"
    ]

    if unresolved:
        print(
            f"\nWARNING: {len(unresolved)} references could not be "
            "mapped to a current chapter."
        )
        print(
            "They have been neutralized to 'an earlier chapter'. "
            "Review them in the CSV."
        )

    if not args.apply:
        print(
            "\nDRY RUN ONLY — no files changed.\n"
            "Run again with --apply after reviewing the diff."
        )
        return 0

    changed_paths = list(rewrites)

    backup_root = make_backup(root, changed_paths)

    print(f"\nBackup: {backup_root}")

    for path, (_, new_text) in rewrites.items():
        path.write_text(new_text, encoding="utf-8")

    remaining = remaining_numeric_references(root)

    if remaining:
        print("\nRemaining hard-coded numeric references:\n")

        for path, line_number, text in remaining:
            print(f"{path}:{line_number}: {text}")

        print(
            "\nSome numeric references remain. Review these manually."
        )
    else:
        print("\nNo 'Chapter N' references remain.")

    print("\nDone.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())