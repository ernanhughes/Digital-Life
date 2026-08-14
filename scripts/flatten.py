#!/usr/bin/env python3

"""
Flatten chapter directories into Markdown files.

Before:

digital-life/
├── 00-what-is-digital-life/
│   └── index.md
├── 01-look-at-this-thing/
│   └── index.md

After:

digital-life/
├── 00-what-is-digital-life.md
├── 01-look-at-this-thing.md

Only immediate child directories containing index.md are transformed.

Usage:

    python flatten_chapters.py digital-life

Preview only:

    python flatten_chapters.py digital-life --dry-run
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def flatten_chapters(root: Path, dry_run: bool = False) -> None:
    root = root.resolve()

    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    converted = 0
    skipped = 0

    # Take a snapshot because we will modify the directory as we iterate.
    directories = sorted(
        path for path in root.iterdir()
        if path.is_dir()
    )

    for chapter_dir in directories:
        index_file = chapter_dir / "index.md"

        if not index_file.is_file():
            continue

        target = root / f"{chapter_dir.name}.md"

        if target.exists():
            print(f"SKIP   {chapter_dir.name}")
            print(f"       target already exists: {target.name}")
            skipped += 1
            continue

        print(f"MOVE   {chapter_dir.name}/index.md")
        print(f"   ->  {target.name}")

        if dry_run:
            continue

        shutil.move(str(index_file), str(target))

        # Only remove the chapter directory if it is now empty.
        try:
            chapter_dir.rmdir()
            print(f"REMOVE {chapter_dir.name}/")
        except OSError:
            print(
                f"KEEP   {chapter_dir.name}/ "
                "(contains additional files or directories)"
            )

        converted += 1

    print()
    if dry_run:
        print("Dry run complete. No files were changed.")
    else:
        print(f"Converted: {converted}")
        print(f"Skipped:   {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flatten chapter/index.md directories into chapter.md files."
    )

    parser.add_argument(
        "root",
        type=Path,
        help="Root directory containing chapter directories.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without changing anything.",
    )

    args = parser.parse_args()

    flatten_chapters(args.root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()