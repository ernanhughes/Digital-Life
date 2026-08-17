"""
Fast block-safe surgical edit applier.

Key performance changes:
- Builds the chapter block index once.
- Caches every candidate block-run once per run length.
- Uses RapidFuzz (C/C++) when available instead of difflib.SequenceMatcher.
- Keeps a difflib fallback so the script still runs without RapidFuzz.
- Exact matches are block-run matches, so they cannot bypass paragraph safety.
- Detects overlapping edits and skips the lower-confidence overlap.
- Accepts a chapter directory and resolves <dir>/index.md automatically.

Recommended:
    pip install rapidfuzz

Examples:
    python scripts/apply_edits_fast.py --edits test.md --chapter chapters/04
    python scripts/apply_edits_fast.py --edits test.md --chapter chapters/04 --apply
    python scripts/apply_edits_fast.py --edits test.md --chapter chapters/04 --apply --diff
    python scripts/apply_edits_fast.py --edits test.md --chapter chapters/04 --show-matches

Expected edit format:

    **Current Text:**
    ````
    text from the chapter, approximately
    ````

    **Recommended Change:**
    ````
    replacement text, or CUT THIS / DELETE THIS / REMOVE THIS
    ````
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

BACKUP_ROOT = Path(r"E:\writer")

try:
    from rapidfuzz import fuzz, process

    HAVE_RAPIDFUZZ = True
except ImportError:
    fuzz = None
    process = None
    HAVE_RAPIDFUZZ = False


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Edit:
    index: int
    current_raw: str
    replacement: str
    is_cut: bool = False
    is_noop: bool = False

    matched_text: str = field(default="", repr=False)
    match_ratio: float = 0.0
    match_start: int = -1
    match_end: int = -1
    skip_reason: str = ""


@dataclass(frozen=True)
class Candidate:
    start: int
    end: int
    text: str
    flat: str


class ChapterIndex:
    """
    Immutable block index plus lazy caches of contiguous block runs.

    The expensive work is done once per chapter, not once per edit.
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.blocks = _split_blocks(text)
        self._runs_by_length: dict[int, list[Candidate]] = {}
        self._groups: dict[tuple[int, ...], tuple[list[Candidate], list[str]]] = {}

    def runs(self, length: int) -> list[Candidate]:
        cached = self._runs_by_length.get(length)
        if cached is not None:
            return cached

        out: list[Candidate] = []
        n = len(self.blocks)

        if length <= 0 or length > n:
            self._runs_by_length[length] = out
            return out

        for i in range(0, n - length + 1):
            start = self.blocks[i][0]
            end = self.blocks[i + length - 1][1]
            text = self.text[start:end]
            out.append(
                Candidate(
                    start=start,
                    end=end,
                    text=text,
                    flat=_flat(text),
                )
            )

        self._runs_by_length[length] = out
        return out

    def group(self, lengths: Iterable[int]) -> tuple[list[Candidate], list[str]]:
        key = tuple(sorted(set(lengths)))
        cached = self._groups.get(key)
        if cached is not None:
            return cached

        candidates: list[Candidate] = []
        for length in key:
            candidates.extend(self.runs(length))

        flats = [c.flat for c in candidates]
        result = (candidates, flats)
        self._groups[key] = result
        return result


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


_BLOCK_RE = re.compile(
    r"""
    \*\*\s*current\s+text\s*:\*\*
    \s*
    (?P<fence1>`{3,})[^\n]*\n
    (?P<current>.*?)
    (?P=fence1)
    \s*
    \*\*\s*recommended\s+change\s*:\*\*
    \s*
    (?P<fence2>`{3,})[^\n]*\n
    (?P<replacement>.*?)
    (?P=fence2)
    """,
    re.DOTALL | re.VERBOSE | re.IGNORECASE,
)

_CUT_PHRASES = {
    "CUT THIS",
    "DELETE THIS",
    "REMOVE THIS",
    "CUT",
    "DELETE",
    "REMOVE",
}

_NOOP_PHRASES = {
    "KEEP EXACTLY AS WRITTEN",
    "KEEP AS WRITTEN",
    "KEEP THIS EXACTLY",
    "KEEP THIS",
    "KEEP",
    "NO CHANGE",
    "NO CHANGES",
    "UNCHANGED",
    "LEAVE UNCHANGED",
    "LEAVE AS IS",
    "LEAVE THIS AS IS",
    "KEEP AS IS",
    "DO NOT CHANGE",
    "DON'T CHANGE",
    "DO NOT ALTER",
    "DON'T ALTER",
    "PRESERVE",
    "PRESERVE THIS",
    "PRESERVE EXACTLY",
    "UNCHANGED TEXT",
}


def _normalize(text: str) -> str:
    return text.strip("\n\r")


def _directive_key(text: str) -> str:
    cleaned = text.strip().upper()
    cleaned = cleaned.strip("`*_ \n\r\t")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" .!;:\"'")
    return cleaned


def _is_cut(text: str) -> bool:
    return _directive_key(text) in _CUT_PHRASES


def _is_noop(text: str) -> bool:
    return _directive_key(text) in _NOOP_PHRASES


def parse_edits(markdown: str) -> list[Edit]:
    edits: list[Edit] = []

    for i, m in enumerate(_BLOCK_RE.finditer(markdown), start=1):
        current = _normalize(m.group("current"))
        replacement_raw = _normalize(m.group("replacement"))

        cut = _is_cut(replacement_raw)
        noop = _is_noop(replacement_raw)

        edits.append(
            Edit(
                index=i,
                current_raw=current,
                replacement="" if (cut or noop) else replacement_raw,
                is_cut=cut,
                is_noop=noop,
            )
        )

    return edits


def collapse_extra_blank_lines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Paths / backup
# ---------------------------------------------------------------------------


def resolve_chapter_path(path: Path) -> Path:
    """
    Allow either:
        --chapter chapters/04/index.md
    or:
        --chapter chapters/04
    """
    if path.is_dir():
        index_path = path / "index.md"
        if index_path.exists():
            return index_path
    return path


def make_backup_path(chapter_path: Path) -> Path:
    resolved = chapter_path.resolve()
    parts_lower = [p.lower() for p in resolved.parts]

    if "chapters" in parts_lower:
        chapters_index = parts_lower.index("chapters")
        if chapters_index > 0:
            book_name = resolved.parts[chapters_index - 1]
            relative_from_book = Path(*resolved.parts[chapters_index:])
            return BACKUP_ROOT / book_name / relative_from_book.with_suffix(
                relative_from_book.suffix + ".bak"
            )

    book_name = resolved.parent.name or "unknown-book"
    return BACKUP_ROOT / book_name / (resolved.name + ".bak")


# ---------------------------------------------------------------------------
# Block splitting / normalization
# ---------------------------------------------------------------------------


def _split_blocks(text: str) -> list[tuple[int, int]]:
    """
    Return block spans whose boundaries are always line boundaries.
    """
    blocks: list[tuple[int, int]] = []
    start: int | None = None
    offset = 0

    for line in text.splitlines(keepends=True):
        if line.strip() == "":
            if start is not None:
                blocks.append((start, offset))
                start = None
        else:
            if start is None:
                start = offset
        offset += len(line)

    if start is not None:
        blocks.append((start, offset))

    return blocks


def _flat(s: str) -> str:
    return " ".join(s.split())


def _count_blocks(needle: str) -> int:
    parts = re.split(r"\n[ \t]*\n", needle.strip())
    return max(1, len([p for p in parts if p.strip()]))


def _candidate_lengths(needle: str) -> tuple[int, ...]:
    k = _count_blocks(needle)
    return tuple(sorted({max(1, k + d) for d in (-1, 0, 1, 2)}))


# ---------------------------------------------------------------------------
# Fast block-run matching
# ---------------------------------------------------------------------------


def _max_possible_ratio(a_len: int, b_len: int) -> float:
    """
    Upper bound for SequenceMatcher-style 2*M/(len(a)+len(b)),
    since M cannot exceed min(len(a), len(b)).

    Used only by the difflib fallback.
    """
    if a_len == 0 and b_len == 0:
        return 1.0
    if a_len == 0 or b_len == 0:
        return 0.0
    return (2.0 * min(a_len, b_len)) / (a_len + b_len)


def _find_best_block_run_rapidfuzz(
    needle: str,
    index: ChapterIndex,
) -> tuple[float, int, int, str]:
    needle_flat = _flat(needle)
    candidates, choices = index.group(_candidate_lengths(needle))

    if not candidates:
        return 0.0, -1, -1, ""

    # Block-safe exact match. This is intentionally NOT haystack.find().
    # It can never produce a mid-paragraph splice.
    for i, choice in enumerate(choices):
        if choice == needle_flat:
            c = candidates[i]
            return 1.0, c.start, c.end, c.text

    result = process.extractOne(
        needle_flat,
        choices,
        scorer=fuzz.ratio,
    )
    if result is None:
        return 0.0, -1, -1, ""

    _choice, score, choice_index = result
    c = candidates[choice_index]
    return score / 100.0, c.start, c.end, c.text


def _find_best_block_run_difflib(
    needle: str,
    index: ChapterIndex,
    threshold: float,
) -> tuple[float, int, int, str]:
    """
    Safe fallback when RapidFuzz is unavailable.

    Still faster than the old implementation because candidate strings and
    whitespace-normalized forms are cached once.
    """
    needle_flat = _flat(needle)
    candidates, choices = index.group(_candidate_lengths(needle))

    if not candidates:
        return 0.0, -1, -1, ""

    for i, choice in enumerate(choices):
        if choice == needle_flat:
            c = candidates[i]
            return 1.0, c.start, c.end, c.text

    best_ratio = 0.0
    best_index = -1

    for i, candidate_flat in enumerate(choices):
        # Mathematically safe length pruning.
        if _max_possible_ratio(len(needle_flat), len(candidate_flat)) < max(
            threshold, best_ratio
        ):
            continue

        ratio = SequenceMatcher(
            None,
            needle_flat,
            candidate_flat,
            autojunk=False,
        ).ratio()

        if ratio > best_ratio:
            best_ratio = ratio
            best_index = i

    if best_index == -1:
        return 0.0, -1, -1, ""

    c = candidates[best_index]
    return best_ratio, c.start, c.end, c.text


def _find_best_block_run(
    needle: str,
    index: ChapterIndex,
    threshold: float,
    engine: str,
) -> tuple[float, int, int, str]:
    if engine == "rapidfuzz":
        return _find_best_block_run_rapidfuzz(needle, index)

    return _find_best_block_run_difflib(needle, index, threshold)


def match_edits(
    edits: list[Edit],
    chapter: str,
    threshold: float,
    engine: str,
) -> None:
    index = ChapterIndex(chapter)

    for edit in edits:
        if edit.is_noop:
            edit.match_ratio = 1.0
            edit.skip_reason = "no-op instruction"
            continue

        ratio, start, end, matched = _find_best_block_run(
            edit.current_raw,
            index,
            threshold,
            engine,
        )
        edit.match_ratio = ratio
        edit.match_start = start
        edit.match_end = end
        edit.matched_text = matched


def _boundaries_are_clean(haystack: str, start: int, end: int) -> bool:
    """
    Require true line boundaries, not merely arbitrary whitespace.
    """
    if start < 0 or end < 0 or start > end:
        return False

    if start > 0 and haystack[start - 1] != "\n":
        return False

    if end < len(haystack):
        if end == 0 or haystack[end - 1] != "\n":
            return False

    return True


# ---------------------------------------------------------------------------
# Applying edits
# ---------------------------------------------------------------------------


def _overlaps(a: Edit, b: Edit) -> bool:
    return a.match_start < b.match_end and b.match_start < a.match_end


def _remove_overlapping_edits(
    edits: list[Edit],
) -> tuple[list[Edit], list[Edit]]:
    """
    Prefer the higher-confidence match if two accepted edits target overlapping
    chapter spans. This prevents one replacement from corrupting another.
    """
    kept: list[Edit] = []
    rejected: list[Edit] = []

    for edit in sorted(
        edits,
        key=lambda e: (-e.match_ratio, e.match_start, e.index),
    ):
        conflict = next((k for k in kept if _overlaps(edit, k)), None)
        if conflict is None:
            kept.append(edit)
        else:
            edit.skip_reason = (
                f"overlaps edit {conflict.index} "
                f"(kept ratio {conflict.match_ratio:.3f})"
            )
            rejected.append(edit)

    return kept, rejected


def apply_edits(
    chapter: str,
    edits: list[Edit],
    threshold: float,
) -> tuple[str, list[str]]:
    logs: list[str] = []
    applicable: list[Edit] = []
    skipped: list[Edit] = []

    for e in edits:
        if e.is_noop:
            e.skip_reason = "no-op / keep-as-written instruction"
            skipped.append(e)
        elif e.match_start == -1:
            e.skip_reason = "no match found"
            skipped.append(e)
        elif e.match_ratio < threshold:
            e.skip_reason = f"ratio {e.match_ratio:.3f} < {threshold:.2f}"
            skipped.append(e)
        elif not _boundaries_are_clean(chapter, e.match_start, e.match_end):
            e.skip_reason = "unclean block boundary (refused to splice)"
            skipped.append(e)
        else:
            applicable.append(e)

    applicable, overlap_skips = _remove_overlapping_edits(applicable)
    skipped.extend(overlap_skips)

    for e in skipped:
        logs.append(
            f"SKIP  edit {e.index:>2}  ratio={e.match_ratio:.3f}  ({e.skip_reason})"
        )

    # Highest char offset first keeps earlier offsets valid.
    applicable_sorted = sorted(
        applicable,
        key=lambda e: e.match_start,
        reverse=True,
    )

    updated = chapter
    applied_count = 0

    for e in applicable_sorted:
        start, end = e.match_start, e.match_end

        if e.is_cut:
            e_end = end
            while e_end < len(updated) and updated[e_end] == "\n":
                e_end += 1
            updated = updated[:start] + updated[e_end:]
            action = "CUT "
        else:
            repl = e.replacement
            if not repl.endswith("\n"):
                repl += "\n"
            updated = updated[:start] + repl + updated[end:]
            action = "EDIT"

        applied_count += 1
        logs.append(
            f"OK    edit {e.index:>2}  ratio={e.match_ratio:.3f}  "
            f"{action}  blocks chars {start}-{end}"
        )

    def _idx(line: str) -> int:
        m = re.search(r"edit\s+(\d+)", line)
        return int(m.group(1)) if m else 1_000_000

    logs.sort(key=_idx)

    summary = f"\n{applied_count}/{len(edits)} edits applied."
    if skipped:
        summary += f"  {len(skipped)} skipped."
    logs.append(summary)

    return updated, logs


# ---------------------------------------------------------------------------
# Diff preview
# ---------------------------------------------------------------------------


def _show_diff_preview(original: str, updated: str, context: int = 3) -> None:
    import difflib

    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile="chapter (original)",
        tofile="chapter (updated)",
        n=context,
    )
    sys.stdout.writelines(diff)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--edits", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.82,
        help="Minimum similarity ratio to accept a match. Default: 0.82",
    )
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--show-matches", action="store_true")
    parser.add_argument(
        "--engine",
        choices=("auto", "rapidfuzz", "difflib"),
        default="auto",
        help="Matching engine. auto uses RapidFuzz when installed.",
    )

    args = parser.parse_args()

    chapter_path = resolve_chapter_path(Path(args.chapter))
    edits_path = Path(args.edits)

    if not chapter_path.exists():
        sys.exit(f"Error: chapter file not found: {chapter_path}")
    if chapter_path.is_dir():
        sys.exit(
            f"Error: chapter path is a directory and no index.md was found: "
            f"{chapter_path}"
        )
    if not edits_path.exists():
        sys.exit(f"Error: edits file not found: {edits_path}")

    engine = args.engine
    if engine == "auto":
        engine = "rapidfuzz" if HAVE_RAPIDFUZZ else "difflib"

    if engine == "rapidfuzz" and not HAVE_RAPIDFUZZ:
        sys.exit(
            "Error: --engine rapidfuzz requested but RapidFuzz is not installed.\n"
            "Install it with: pip install rapidfuzz"
        )

    chapter_text = chapter_path.read_text(encoding="utf-8")
    edits_markdown = edits_path.read_text(encoding="utf-8")

    edits = parse_edits(edits_markdown)
    if not edits:
        print("No edit pairs found in the review file.")
        print()
        print("Expected format:")
        print("  **Current Text:**")
        print("  ```")
        print("  ...")
        print("  ```")
        print("  **Recommended Change:**")
        print("  ```")
        print("  ...")
        print("  ```")
        return

    cut_count = sum(1 for e in edits if e.is_cut)
    noop_count = sum(1 for e in edits if e.is_noop)
    normal_count = len(edits) - cut_count - noop_count

    print(f"Parsed {len(edits)} edit pair(s) from: {edits_path.name}")
    print(f"  Normal replacements: {normal_count}")
    print(f"  Cuts/removals:       {cut_count}")
    print(f"  No-op skips:         {noop_count}")
    print(f"Chapter: {chapter_path}  ({len(chapter_text):,} chars)")
    print(f"Threshold: {args.threshold:.2f}")
    print(f"Matcher:   {engine}\n")

    match_edits(edits, chapter_text, args.threshold, engine)

    if args.show_matches:
        for e in edits:
            print(f"--- Edit {e.index}  ratio={e.match_ratio:.3f} ---")
            if e.is_noop:
                print("NO-OP instruction detected; no matching attempted.\n")
                continue

            print("NEEDLE (from review):")
            print(repr(e.current_raw[:500]))
            print("MATCHED (in chapter):")
            print(repr(e.matched_text[:500]))
            print()

    updated_text, logs = apply_edits(
        chapter_text,
        edits,
        args.threshold,
    )
    updated_text = collapse_extra_blank_lines(updated_text)

    for line in logs:
        print(line)

    if args.diff and updated_text != chapter_text:
        print("\n--- DIFF ---")
        _show_diff_preview(chapter_text, updated_text)

    if updated_text == chapter_text:
        print("\nNo changes would be made.")
        return

    if not args.apply:
        print("\nDry run - no files written. Re-run with --apply to save changes.")
        return

    if not args.no_backup:
        backup = make_backup_path(chapter_path)
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(chapter_text, encoding="utf-8")
        print(f"\nBackup: {backup}")

    chapter_path.write_text(updated_text, encoding="utf-8")
    print(f"Saved:  {chapter_path}")


if __name__ == "__main__":
    main()
