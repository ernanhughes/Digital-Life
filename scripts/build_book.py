from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "post"
CONFIG_PATH = ROOT / "data" / "books.yaml"
DEFAULT_OUTPUT_ROOT = ROOT / "book-build"
DEFAULT_MERMAID_COMMAND = "npx"
OFFICIAL_MERMAID_PACKAGE = "@mermaid-js/mermaid-cli"

MERMAID_RE = re.compile(
    r"```mermaid\s*\n(?P<body>.*?)\n```",
    re.DOTALL | re.IGNORECASE,
)
NUMBER_SUFFIX_RE = re.compile(r"-(\d+)\.md$", re.IGNORECASE)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass(frozen=True)
class BookDefinition:
    key: str
    title: str
    pattern: str
    expected_chapters: int


def natural_sort_key(text: str) -> list[object]:
    """Sort strings containing numbers naturally: 2 before 10."""
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", text)]


def load_book_definitions(config_path: Path = CONFIG_PATH) -> dict[str, BookDefinition]:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    books = raw.get("books")
    if not isinstance(books, dict) or not books:
        raise ValueError(f"No books defined in {config_path}")

    result: dict[str, BookDefinition] = {}
    for key, value in books.items():
        if not isinstance(value, dict):
            raise ValueError(f"Book '{key}' must be a mapping")
        result[key] = BookDefinition(
            key=key,
            title=str(value["title"]),
            pattern=str(value["pattern"]),
            expected_chapters=int(value["expected_chapters"]),
        )
    return result


def strip_hugo_front_matter(content: str) -> str:
    """Remove leading TOML (+++), YAML (---), or legacy HTML-comment metadata."""
    text = content.lstrip("\ufeff\n\r\t ")

    for marker in ("+++", "---"):
        if text.startswith(marker):
            lines = text.splitlines(keepends=True)
            if lines and lines[0].strip() == marker:
                for idx in range(1, len(lines)):
                    if lines[idx].strip() == marker:
                        text = "".join(lines[idx + 1 :]).lstrip()
                        break
                else:
                    raise ValueError(f"Unclosed Hugo front matter block beginning with {marker}")
                break

    if text.startswith("<!--"):
        end = text.find("-->")
        if end != -1:
            text = text[end + 3 :].lstrip()

    text = HTML_COMMENT_RE.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def chapter_number(path: Path) -> int:
    match = NUMBER_SUFFIX_RE.search(path.name)
    if not match:
        raise ValueError(f"Chapter filename has no numeric suffix: {path.name}")
    return int(match.group(1))


def select_chapters(book: BookDefinition, content_dir: Path = CONTENT_DIR) -> list[Path]:
    files = sorted(content_dir.glob(book.pattern), key=lambda p: natural_sort_key(p.name))
    if len(files) != book.expected_chapters:
        raise ValueError(
            f"{book.key}: expected {book.expected_chapters} chapters matching "
            f"'{book.pattern}', found {len(files)}"
        )

    numbers = [chapter_number(path) for path in files]
    expected_numbers = list(range(book.expected_chapters))
    if numbers != expected_numbers:
        raise ValueError(
            f"{book.key}: chapter sequence must be {expected_numbers[0]:02d}.."
            f"{expected_numbers[-1]:02d}; found {numbers}"
        )
    return files


def count_words(text: str) -> int:
    return len(text.split())


def build_mermaid_command(
    executable: str,
    source_path: Path,
    output_path: Path,
) -> list[str]:
    """Build a renderer command, preferring the official Mermaid CLI through npx."""
    command_name = Path(executable).stem.lower()
    if command_name in {"npx", "npx.cmd"}:
        return [
            executable,
            "--yes",
            OFFICIAL_MERMAID_PACKAGE,
            "-i",
            str(source_path),
            "-o",
            str(output_path),
            "-b",
            "transparent",
        ]

    return [
        executable,
        "-i",
        str(source_path),
        "-o",
        str(output_path),
        "-b",
        "transparent",
    ]


def render_mermaid(
    source_path: Path,
    output_path: Path,
    command: str = DEFAULT_MERMAID_COMMAND,
) -> None:
    executable = shutil.which(command)
    if not executable:
        if command == DEFAULT_MERMAID_COMMAND:
            raise RuntimeError(
                "Official Mermaid renderer could not be started because 'npx' was not found on PATH. "
                "Install Node.js, then use the default @mermaid-js/mermaid-cli renderer, or pass "
                "--mermaid-command with an explicit compatible executable."
            )
        raise RuntimeError(f"Mermaid renderer '{command}' was not found on PATH.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    renderer_command = build_mermaid_command(executable, source_path, output_path)

    try:
        subprocess.run(renderer_command, check=True)
    except subprocess.CalledProcessError as exc:
        rendered_command = " ".join(str(part) for part in renderer_command)
        raise RuntimeError(
            f"Mermaid rendering failed for '{source_path}'.\n"
            f"Renderer command: {rendered_command}\n"
            "The .mmd source has been preserved for direct reproduction."
        ) from exc


def transform_mermaid(
    markdown: str,
    *,
    chapter_index: int,
    images_dir: Path,
    render: bool,
    mermaid_command: str,
) -> tuple[str, int]:
    diagram_index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal diagram_index
        diagram_index += 1
        stem = f"chapter-{chapter_index:02d}-diagram-{diagram_index:02d}"
        mermaid_path = images_dir / f"{stem}.mmd"
        png_path = images_dir / f"{stem}.png"
        mermaid_path.parent.mkdir(parents=True, exist_ok=True)
        mermaid_path.write_text(match.group("body").strip() + "\n", encoding="utf-8")

        if render:
            render_mermaid(mermaid_path, png_path, mermaid_command)

        relative_png = Path("..") / "images" / png_path.name
        return f"![Diagram for chapter {chapter_index:02d}]({relative_png.as_posix()})"

    return MERMAID_RE.sub(replace, markdown), diagram_index


def merge_manuscript(chapters: Iterable[Path], output_path: Path) -> None:
    parts = []
    for path in chapters:
        text = path.read_text(encoding="utf-8").strip()
        text = text.replace("](../images/", "](images/")
        parts.append(text)
    output_path.write_text("\n\n---\n\n".join(parts) + "\n", encoding="utf-8")


def build_book(
    book: BookDefinition,
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    render: bool = True,
    mermaid_command: str = DEFAULT_MERMAID_COMMAND,
) -> Path:
    source_chapters = select_chapters(book)
    book_dir = output_root / book.key
    manuscript_dir = book_dir / "manuscript"
    images_dir = book_dir / "images"

    if book_dir.exists():
        shutil.rmtree(book_dir)
    manuscript_dir.mkdir(parents=True)
    images_dir.mkdir(parents=True)

    generated_chapters: list[Path] = []
    total_words = 0
    total_diagrams = 0

    print(f"\n{book.title}")
    print("-" * 76)
    print(f"{'CHAPTER':<48} {'WORDS':>10} {'DIAGRAMS':>10}")
    print("-" * 76)

    for source_path in source_chapters:
        number = chapter_number(source_path)
        clean = strip_hugo_front_matter(source_path.read_text(encoding="utf-8"))
        transformed, diagram_count = transform_mermaid(
            clean,
            chapter_index=number,
            images_dir=images_dir,
            render=render,
            mermaid_command=mermaid_command,
        )

        destination = manuscript_dir / f"{number:02d}.md"
        destination.write_text(transformed.strip() + "\n", encoding="utf-8")
        generated_chapters.append(destination)

        words = count_words(transformed)
        total_words += words
        total_diagrams += diagram_count
        print(f"{source_path.name:<48} {words:>10,} {diagram_count:>10}")

    merged_path = book_dir / f"{book.key}.md"
    merge_manuscript(generated_chapters, merged_path)

    print("-" * 76)
    print(f"{'TOTAL':<48} {total_words:>10,} {total_diagrams:>10}")
    print(f"\nBook build: {book_dir}")
    print(f"Merged manuscript: {merged_path}")
    return merged_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare Programmer.ie Hugo tutorial series as book manuscripts."
    )
    parser.add_argument("book", nargs="?", help="Book key from data/books.yaml")
    parser.add_argument("--all", action="store_true", help="Build every configured book")
    parser.add_argument("--list", action="store_true", help="List configured books and exit")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Generated book-build directory",
    )
    parser.add_argument(
        "--skip-mermaid-render",
        action="store_true",
        help="Extract/replace Mermaid blocks but do not render them (useful for validation)",
    )
    parser.add_argument(
        "--mermaid-command",
        default=DEFAULT_MERMAID_COMMAND,
        help=(
            "Mermaid renderer executable. Default: npx, which invokes the official "
            "@mermaid-js/mermaid-cli package."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    definitions = load_book_definitions()

    if args.list:
        for key, book in definitions.items():
            print(f"{key:<40} {book.expected_chapters:>3} chapters  {book.title}")
        return

    if args.all:
        selected = list(definitions.values())
    elif args.book:
        try:
            selected = [definitions[args.book]]
        except KeyError as exc:
            raise SystemExit(
                f"Unknown book '{args.book}'. Use --list to see configured books."
            ) from exc
    else:
        raise SystemExit("Specify a book key or use --all / --list")

    for book in selected:
        build_book(
            book,
            output_root=args.output_root,
            render=not args.skip_mermaid_render,
            mermaid_command=args.mermaid_command,
        )


if __name__ == "__main__":
    main()
