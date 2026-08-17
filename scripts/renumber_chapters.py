#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


CHAPTERS_DIR = Path("content/books/digital-life")
METADATA_DIR = Path("metadata")

CHAPTER_RE = re.compile(
    r"^(?P<num>\d{2})-(?P<slug>.+?)(?P<suffix>\.md)$"
)

TITLE_RE = re.compile(
    r'^(?P<prefix>\s*title\s*=\s*")'
    r'(?P<number>\d{1,2})'
    r'(?P<separator>:\s*)'
    r'(?P<title>.*?)'
    r'(?P<suffix>"\s*)$'
)

WEIGHT_RE = re.compile(
    r"^(?P<prefix>\s*weight\s*=\s*)"
    r"(?P<number>\d+)"
    r"(?P<suffix>\s*)$"
)

Direction = Literal["up", "down"]


@dataclass(frozen=True)
class RenameOp:
    src: Path
    temp: Path
    dst: Path
    label: str
    old_number: int
    new_number: int

    @property
    def src_name(self) -> str:
        return self.src.name

    @property
    def dst_name(self) -> str:
        return self.dst.name


@dataclass(frozen=True)
class ChapterFile:
    path: Path
    number: int
    slug: str
    suffix: str

    def new_number(self, direction: Direction, amount: int) -> int:
        if direction == "up":
            return self.number + amount

        if direction == "down":
            return self.number - amount

        raise ValueError(f"Unsupported direction: {direction}")

    def new_name(self, direction: Direction, amount: int) -> str:
        number = self.new_number(direction, amount)
        return f"{number:02d}-{self.slug}{self.suffix}"

    @property
    def temp_name(self) -> str:
        return (
            f"__renumber_tmp__"
            f"{self.number:02d}-{self.slug}{self.suffix}"
        )


def run(cmd: list[str], dry_run: bool) -> None:
    print("$", " ".join(cmd))

    if dry_run:
        return

    result = subprocess.run(cmd, text=True)

    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ensure_git_repo() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0 or result.stdout.strip() != "true":
        raise SystemExit(
            "ERROR: This script must be run inside a Git repository."
        )


def ensure_directory(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(
            f"ERROR: {label} directory does not exist: {path}"
        )

    if not path.is_dir():
        raise SystemExit(
            f"ERROR: {label} path is not a directory: {path}"
        )


def discover_chapters(
    chapters_dir: Path,
    from_number: int,
    direction: Direction,
    exclude_slugs: set[str],
) -> list[ChapterFile]:
    ensure_directory(chapters_dir, "Chapters")

    chapters: list[ChapterFile] = []

    for path in chapters_dir.iterdir():
        if not path.is_file():
            continue

        match = CHAPTER_RE.match(path.name)

        if not match:
            continue

        number = int(match.group("num"))
        slug = match.group("slug")

        if number < from_number:
            continue

        if slug in exclude_slugs:
            print(f"Skipping excluded chapter: {path.name}")
            continue

        chapters.append(
            ChapterFile(
                path=path,
                number=number,
                slug=slug,
                suffix=match.group("suffix"),
            )
        )

    # Temp names make ordering technically unnecessary, but stable output
    # makes dry runs easier to inspect.
    if direction == "up":
        return sorted(
            chapters,
            key=lambda chapter: chapter.number,
            reverse=True,
        )

    return sorted(
        chapters,
        key=lambda chapter: chapter.number,
    )


def discover_matching_metadata_files(
    metadata_dir: Path,
    chapter: ChapterFile,
) -> list[Path]:
    if not metadata_dir.exists():
        return []

    if not metadata_dir.is_dir():
        raise SystemExit(
            f"ERROR: Metadata path is not a directory: {metadata_dir}"
        )

    prefix = f"{chapter.number:02d}-{chapter.slug}"
    matches: list[Path] = []

    for path in metadata_dir.iterdir():
        if not path.is_file():
            continue

        if path.name.startswith(prefix):
            matches.append(path)

    return sorted(matches)


def make_chapter_rename_op(
    chapter: ChapterFile,
    direction: Direction,
    amount: int,
) -> RenameOp:
    new_number = chapter.new_number(direction, amount)

    if new_number < 1 or new_number > 99:
        raise SystemExit(
            f"ERROR: Renumbering {chapter.path.name} would produce "
            f"invalid chapter number: {new_number:02d}"
        )

    return RenameOp(
        src=chapter.path,
        temp=chapter.path.with_name(chapter.temp_name),
        dst=chapter.path.with_name(
            chapter.new_name(direction, amount)
        ),
        label="chapter",
        old_number=chapter.number,
        new_number=new_number,
    )


def make_metadata_rename_op(
    metadata_file: Path,
    chapter: ChapterFile,
    direction: Direction,
    amount: int,
) -> RenameOp:
    new_number = chapter.new_number(direction, amount)

    old_prefix = f"{chapter.number:02d}-{chapter.slug}"
    new_prefix = f"{new_number:02d}-{chapter.slug}"

    if not metadata_file.name.startswith(old_prefix):
        raise SystemExit(
            "ERROR: Metadata file does not match chapter prefix: "
            f"{metadata_file}"
        )

    new_name = (
        new_prefix
        + metadata_file.name[len(old_prefix):]
    )

    temp_name = f"__renumber_tmp__{metadata_file.name}"

    return RenameOp(
        src=metadata_file,
        temp=metadata_file.with_name(temp_name),
        dst=metadata_file.with_name(new_name),
        label="metadata",
        old_number=chapter.number,
        new_number=new_number,
    )


def build_rename_plan(
    chapters_dir: Path,
    metadata_dir: Path,
    from_number: int,
    direction: Direction,
    amount: int,
    exclude_slugs: set[str],
) -> list[RenameOp]:
    chapters = discover_chapters(
        chapters_dir=chapters_dir,
        from_number=from_number,
        direction=direction,
        exclude_slugs=exclude_slugs,
    )

    if not chapters:
        print(
            f"No chapters found at or after "
            f"{from_number:02d} in {chapters_dir}"
        )
        return []

    ops: list[RenameOp] = []

    for chapter in chapters:
        ops.append(
            make_chapter_rename_op(
                chapter,
                direction,
                amount,
            )
        )

        for metadata_file in discover_matching_metadata_files(
            metadata_dir,
            chapter,
        ):
            ops.append(
                make_metadata_rename_op(
                    metadata_file,
                    chapter,
                    direction,
                    amount,
                )
            )

    return ops


def validate_no_temp_conflicts(
    ops: list[RenameOp],
) -> None:
    for op in ops:
        if op.temp.exists():
            raise SystemExit(
                f"ERROR: Temporary file already exists: {op.temp}\n"
                "Delete or rename it before running this script."
            )


def validate_no_duplicate_targets(
    ops: list[RenameOp],
) -> None:
    targets: dict[Path, RenameOp] = {}

    for op in ops:
        resolved_target = op.dst.resolve()

        if resolved_target in targets:
            other = targets[resolved_target]

            raise SystemExit(
                "ERROR: Duplicate rename target detected:\n"
                f"  {other.src} -> {other.dst}\n"
                f"  {op.src} -> {op.dst}"
            )

        targets[resolved_target] = op


def validate_no_target_conflicts(
    ops: list[RenameOp],
) -> None:
    original_paths = {
        op.src.resolve()
        for op in ops
    }

    for op in ops:
        if (
            op.dst.exists()
            and op.dst.resolve() not in original_paths
        ):
            raise SystemExit(
                "ERROR: Target file already exists and is "
                f"not part of the renumber set: {op.dst}"
            )


def validate_plan(
    ops: list[RenameOp],
) -> None:
    validate_no_temp_conflicts(ops)
    validate_no_duplicate_targets(ops)
    validate_no_target_conflicts(ops)


def git_mv(
    src: Path,
    dst: Path,
    dry_run: bool,
) -> None:
    run(
        ["git", "mv", str(src), str(dst)],
        dry_run=dry_run,
    )


def update_frontmatter_text(
    text: str,
    new_number: int,
) -> tuple[str, bool, bool]:
    """
    Update only TOML front matter between the opening +++ markers.

    Changes:

        title = "04: Some Title"
        weight = 4

    to:

        title = "05: Some Title"
        weight = 5

    The title text itself is preserved.
    """

    lines = text.splitlines(keepends=True)

    if not lines:
        return text, False, False

    if lines[0].strip() != "+++":
        raise ValueError(
            "Markdown file does not start with TOML front matter."
        )

    frontmatter_end: int | None = None

    for index in range(1, len(lines)):
        if lines[index].strip() == "+++":
            frontmatter_end = index
            break

    if frontmatter_end is None:
        raise ValueError(
            "Could not find closing +++ front matter marker."
        )

    title_updated = False
    weight_updated = False

    for index in range(1, frontmatter_end):
        line = lines[index]

        # Preserve the original newline separately.
        if line.endswith("\r\n"):
            newline = "\r\n"
            content = line[:-2]
        elif line.endswith("\n"):
            newline = "\n"
            content = line[:-1]
        else:
            newline = ""
            content = line

        title_match = TITLE_RE.match(content)

        if title_match:
            lines[index] = (
                f'{title_match.group("prefix")}'
                f'{new_number:02d}'
                f'{title_match.group("separator")}'
                f'{title_match.group("title")}'
                f'{title_match.group("suffix")}'
                f'{newline}'
            )

            title_updated = True
            continue

        weight_match = WEIGHT_RE.match(content)

        if weight_match:
            lines[index] = (
                f'{weight_match.group("prefix")}'
                f'{new_number}'
                f'{weight_match.group("suffix")}'
                f'{newline}'
            )

            weight_updated = True

    return (
        "".join(lines),
        title_updated,
        weight_updated,
    )


def update_chapter_frontmatter(
    path: Path,
    old_number: int,
    new_number: int,
    dry_run: bool,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )

    try:
        new_text, title_updated, weight_updated = (
            update_frontmatter_text(
                text=text,
                new_number=new_number,
            )
        )
    except ValueError as exc:
        raise SystemExit(
            f"ERROR: Could not update front matter in {path}: "
            f"{exc}"
        ) from exc

    if not title_updated:
        raise SystemExit(
            f"ERROR: No title = \"NN: ...\" field found "
            f"in front matter: {path}"
        )

    if not weight_updated:
        raise SystemExit(
            f"ERROR: No weight = N field found "
            f"in front matter: {path}"
        )

    print(
        f"  [frontmatter] {path.name}: "
        f"title {old_number:02d} -> {new_number:02d}, "
        f"weight {old_number} -> {new_number}"
    )

    if dry_run:
        return

    path.write_text(
        new_text,
        encoding="utf-8",
    )


def direction_label(
    direction: Direction,
    amount: int,
) -> str:
    sign = "+" if direction == "up" else "-"

    return f"{direction} by {sign}{amount}"


def renumber(
    from_number: int,
    direction: Direction,
    amount: int,
    dry_run: bool,
    exclude_slugs: set[str],
) -> None:
    ensure_git_repo()

    chapters_dir = CHAPTERS_DIR.resolve()
    metadata_dir = METADATA_DIR.resolve()

    ops = build_rename_plan(
        chapters_dir=chapters_dir,
        metadata_dir=metadata_dir,
        from_number=from_number,
        direction=direction,
        amount=amount,
        exclude_slugs=exclude_slugs,
    )

    if not ops:
        return

    validate_plan(ops)

    print()
    print(
        f"Renumbering chapters in: "
        f"{chapters_dir}"
    )

    if metadata_dir.exists():
        print(
            f"Renumbering matching metadata in: "
            f"{metadata_dir}"
        )
    else:
        print(
            "Metadata directory does not exist; "
            f"skipping metadata: {metadata_dir}"
        )

    print(
        f"Renumbering chapters >= {from_number:02d} "
        f"{direction_label(direction, amount)}"
    )

    if exclude_slugs:
        print(
            "Excluded slugs: "
            + ", ".join(sorted(exclude_slugs))
        )

    print()

    print("Planned changes:")

    for op in sorted(
        ops,
        key=lambda item: str(item.src),
    ):
        print(
            f"  [{op.label}] "
            f"{op.src.relative_to(Path.cwd())} "
            f"-> {op.dst.name}"
        )

        if op.label == "chapter":
            print(
                f"      title prefix: "
                f"{op.old_number:02d} -> "
                f"{op.new_number:02d}"
            )
            print(
                f"      weight: "
                f"{op.old_number} -> "
                f"{op.new_number}"
            )

    print()

    #
    # Dry-run front matter validation.
    #
    # Validate the current chapter files before doing any git mv.
    #
    print("Checking chapter front matter")

    for op in ops:
        if op.label != "chapter":
            continue

        text = op.src.read_text(
            encoding="utf-8"
        )

        try:
            _, title_updated, weight_updated = (
                update_frontmatter_text(
                    text=text,
                    new_number=op.new_number,
                )
            )
        except ValueError as exc:
            raise SystemExit(
                f"ERROR: Invalid front matter in "
                f"{op.src}: {exc}"
            ) from exc

        if not title_updated:
            raise SystemExit(
                f"ERROR: No title = \"NN: ...\" "
                f"found in {op.src}"
            )

        if not weight_updated:
            raise SystemExit(
                f"ERROR: No weight = N "
                f"found in {op.src}"
            )

    print("Front matter checks passed.")
    print()

    print("Step 1: move files to temporary names")

    for op in ops:
        git_mv(
            op.src,
            op.temp,
            dry_run=dry_run,
        )

    print()
    print(
        "Step 2: move temporary files "
        "to final names"
    )

    for op in ops:
        git_mv(
            op.temp,
            op.dst,
            dry_run=dry_run,
        )

    print()
    print(
        "Step 3: update chapter title numbers "
        "and weights"
    )

    for op in ops:
        if op.label != "chapter":
            continue

        # In dry-run mode no git mv actually happened,
        # so inspect the original path.
        path = (
            op.src
            if dry_run
            else op.dst
        )

        update_chapter_frontmatter(
            path=path,
            old_number=op.old_number,
            new_number=op.new_number,
            dry_run=dry_run,
        )

    print()

    if dry_run:
        print(
            "Dry run complete. "
            "No files were changed."
        )
    else:
        print("Renumbering complete.")
        print()
        print("Next recommended commands:")
        print("  git status")
        print("  git diff --stat")
        print("  git diff")
        print(
            '  git commit -m '
            '"Renumber chapters and update front matter"'
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Renumber numbered chapter markdown files in "
            "chapters/, rename matching metadata files, "
            "and update each chapter's TOML title number "
            "and weight."
        )
    )

    parser.add_argument(
        "from_number",
        type=int,
        help=(
            "First chapter number to renumber. "
            "Example: 4 --direction up turns "
            "04 -> 05, 05 -> 06, ..."
        ),
    )

    parser.add_argument(
        "--direction",
        choices=["up", "down"],
        default="up",
        help=(
            "Renumber direction. "
            "Default: up."
        ),
    )

    parser.add_argument(
        "--amount",
        type=int,
        default=1,
        help=(
            "How many chapter numbers to move. "
            "Default: 1. "
            "Example: --amount 2 turns "
            "04 -> 06 when moving up."
        ),
    )

    parser.add_argument(
        "--exclude-slug",
        action="append",
        default=[],
        help=(
            "Chapter slug to leave untouched. "
            "May be supplied more than once. "
            "Example: "
            "--exclude-slug "
            "so-we-built-the-wrong-thing-on-purpose"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Preview file renames and front matter "
            "updates without changing anything."
        ),
    )

    args = parser.parse_args()

    if (
        args.from_number < 1
        or args.from_number > 99
    ):
        raise SystemExit(
            "ERROR: from_number must be "
            "between 1 and 99."
        )

    if args.amount < 1:
        raise SystemExit(
            "ERROR: --amount must be at least 1."
        )

    renumber(
        from_number=args.from_number,
        direction=args.direction,
        amount=args.amount,
        dry_run=args.dry_run,
        exclude_slugs=set(
            args.exclude_slug
        ),
    )


if __name__ == "__main__":
    main()