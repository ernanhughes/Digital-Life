from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

from scripts import build_book

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "books.yaml"
DEFAULT_OUTPUT_ROOT = ROOT / "book-build"


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, dict[str, Any]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    books = raw.get("books")
    if not isinstance(books, dict) or not books:
        raise ValueError(f"No books defined in {path}")
    return books


def publication_config(book_key: str, catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    try:
        book = catalog[book_key]
    except KeyError as exc:
        raise ValueError(f"Unknown book '{book_key}'") from exc

    publication = book.get("publication")
    if not isinstance(publication, dict):
        raise ValueError(f"{book_key}: publication metadata is not configured")

    epub = publication.get("epub")
    if not isinstance(epub, dict) or not epub.get("enabled"):
        raise ValueError(f"{book_key}: EPUB publication is not enabled")

    required = ("author", "language", "rights")
    missing = [field for field in required if not publication.get(field)]
    if missing:
        raise ValueError(f"{book_key}: publication metadata missing {', '.join(missing)}")

    if not epub.get("css"):
        raise ValueError(f"{book_key}: EPUB CSS is not configured")
    return publication


def write_pandoc_metadata(
    *,
    book_key: str,
    book: dict[str, Any],
    publication: dict[str, Any],
    book_dir: Path,
) -> Path:
    metadata = {
        "title": book["title"],
        "subtitle": book.get("subtitle", ""),
        "author": publication["author"],
        "lang": publication["language"],
        "rights": publication["rights"],
        "description": book.get("description", ""),
        "identifier": f"programmer.ie:{book_key}",
    }
    path = book_dir / "publication-metadata.yaml"
    path.write_text(
        yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def resolve_optional_cover(epub: dict[str, Any]) -> Path | None:
    cover = epub.get("cover")
    if not cover:
        return None
    path = (ROOT / str(cover)).resolve()
    if not path.exists():
        raise ValueError(f"Configured EPUB cover does not exist: {path}")
    return path


def build_pandoc_command(
    *,
    manuscript: Path,
    output: Path,
    metadata_path: Path,
    css_path: Path,
    resource_path: Path,
    toc_depth: int,
    cover_path: Path | None,
    pandoc_command: str = "pandoc",
) -> list[str]:
    command = [
        pandoc_command,
        str(manuscript),
        "-o",
        str(output),
        "--metadata-file",
        str(metadata_path),
        "--css",
        str(css_path),
        "--toc",
        f"--toc-depth={toc_depth}",
        "--resource-path",
        str(resource_path),
    ]
    if cover_path is not None:
        command.extend(["--epub-cover-image", str(cover_path)])
    return command


def publish_epub(
    book_key: str,
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    pandoc_command: str = "pandoc",
    mermaid_command: str = build_book.DEFAULT_MERMAID_COMMAND,
    prepare: bool = True,
    render_mermaid: bool = True,
    execute: bool = True,
) -> tuple[Path, list[str]]:
    output_root = output_root.resolve()
    catalog = load_catalog()
    publication = publication_config(book_key, catalog)
    book = catalog[book_key]
    definitions = build_book.load_book_definitions()
    definition = definitions[book_key]

    if prepare:
        manuscript = build_book.build_book(
            definition,
            output_root=output_root,
            render=render_mermaid,
            mermaid_command=mermaid_command,
        )
    else:
        manuscript = output_root / book_key / f"{book_key}.md"
        if not manuscript.exists():
            raise ValueError(f"Prepared manuscript does not exist: {manuscript}")

    book_dir = output_root / book_key
    release_dir = book_dir / "releases"
    release_dir.mkdir(parents=True, exist_ok=True)

    epub = publication["epub"]
    css_path = (ROOT / str(epub["css"])).resolve()
    if not css_path.exists():
        raise ValueError(f"Configured EPUB CSS does not exist: {css_path}")

    metadata_path = write_pandoc_metadata(
        book_key=book_key,
        book=book,
        publication=publication,
        book_dir=book_dir,
    )
    cover_path = resolve_optional_cover(epub)
    output = release_dir / f"{book_key}.epub"
    command = build_pandoc_command(
        manuscript=manuscript,
        output=output,
        metadata_path=metadata_path,
        css_path=css_path,
        resource_path=book_dir,
        toc_depth=int(epub.get("toc_depth", 2)),
        cover_path=cover_path,
        pandoc_command=pandoc_command,
    )

    if execute:
        executable = shutil.which(pandoc_command)
        if not executable:
            raise RuntimeError(
                f"Pandoc executable '{pandoc_command}' was not found on PATH."
            )
        command[0] = executable
        subprocess.run(command, cwd=book_dir, check=True)
        if not output.exists():
            raise RuntimeError(f"Pandoc completed without creating {output}")

    return output, command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a prepared Programmer.ie book edition.")
    parser.add_argument("book", help="Book key from data/books.yaml")
    parser.add_argument("--format", choices=("epub",), default="epub")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--pandoc-command", default="pandoc")
    parser.add_argument(
        "--mermaid-command",
        default=build_book.DEFAULT_MERMAID_COMMAND,
        help=(
            "Mermaid renderer executable. Default: npx, which invokes the official "
            "@mermaid-js/mermaid-cli package."
        ),
    )
    parser.add_argument("--skip-prepare", action="store_true")
    parser.add_argument("--skip-mermaid-render", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prepare metadata and print the Pandoc command without running Pandoc.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output, command = publish_epub(
        args.book,
        output_root=args.output_root,
        pandoc_command=args.pandoc_command,
        mermaid_command=args.mermaid_command,
        prepare=not args.skip_prepare,
        render_mermaid=not args.skip_mermaid_render,
        execute=not args.dry_run,
    )
    print("\nPandoc command:")
    print(" ".join(str(part) for part in command))
    if args.dry_run:
        print(f"\nDry run: would create {output}")
    else:
        print(f"\nPublished EPUB: {output}")


if __name__ == "__main__":
    main()
