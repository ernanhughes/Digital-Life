"""
apply_edits.

python scripts/apply_edits.py --edits test.md --apply --chapter chapters/04 


Each edit must look like this (headings are case-insensitive):

    **Current Text:**
    ```
    The text as it appears (approximately) in the chapter.
    ```

    **Recommended Change:**
    ```
    The replacement text, or one of: CUT THIS / DELETE THIS / REMOVE THIS
    ```

==============
Parse surgical edit suggestions from an AI review response and apply them
to a chapter file using fuzzy, BLOCK-LEVEL matching.

Why block-level?
----------------
The previous version matched at the character level with a sliding window,
then spliced at whatever character offsets scored best. Because
SequenceMatcher.ratio() rewards overall overlap (not boundary correctness),
the best-scoring window could start or end in the middle of a word, and the
splice would then jam the replacement into the middle of a line, e.g.:

    "In theo"In theory, a body could be a sequence of ...

This version never operates below a paragraph boundary. It splits the chapter
into blocks (runs of non-blank lines separated by blank lines), finds the
contiguous RUN of blocks that best matches the "Current Text", and replaces
those whole blocks. Boundaries are therefore always at blank-line edges, so a
mid-line splice is structurally impossible.

Usage
-----
Dry run (shows what would change, writes nothing):
    python apply_edits.py --chapter ch04.md --edits review.md

Apply with default threshold (0.82 similarity):
    python apply_edits.py --chapter ch04.md --edits review.md --apply

Stricter / looser matching:
    python apply_edits.py --chapter ch04.md --edits review.md --apply --threshold 0.90
    python apply_edits.py --chapter ch04.md --edits review.md --apply --threshold 0.70

Disable backup (not recommended):
    python apply_edits.py --chapter ch04.md --edits review.md --apply --no-backup

See exactly what was matched:
    python apply_edits.py --chapter ch04.md --edits review.md --show-matches

Output format expected in the review file
------------------------------------------
Each edit must look like this (headings are case-insensitive):

    **Current Text:**
    ```
    The text as it appears (approximately) in the chapter.
    ```

    **Recommended Change:**
    ```
    The replacement text, or one of: CUT THIS / DELETE THIS / REMOVE THIS
    ```

IMPORTANT — embedded code fences:
If the chapter text you are quoting (or your replacement) itself contains a
```fenced``` block — which happens often in these chapters, e.g. ```text ...```
log blocks — wrap the edit in a LONGER fence than anything inside it. Use four
backticks outside when the content contains three, five when it contains four,
and so on. The parser matches the closing fence to the exact length of the
opening fence, so a four-backtick edit will correctly contain three-backtick
blocks without being truncated.

The script finds ALL such pairs in the file, in order.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

BACKUP_ROOT = Path(r"E:\writer")

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Edit:
    index: int
    current_raw: str       # as extracted from the review
    replacement: str       # empty string means "delete" or "no-op"
    is_cut: bool = False
    is_noop: bool = False  # true means "keep as written / skip"

    # filled in during matching
    matched_text: str = field(default="", repr=False)
    match_ratio: float = 0.0
    match_start: int = -1
    match_end: int = -1
    skip_reason: str = ""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# Variable-length fence: capture the opening run of >=3 backticks, then require
# the closing fence to match that exact length via the (?P=fence) backreference.
# This lets a four-backtick edit block safely contain three-backtick code blocks.
_BLOCK_RE = re.compile(
    r"""
    \*\*\s*current\s+text\s*:\*\*           # **Current Text:**
    \s*
    (?P<fence1>`{3,})[^\n]*\n               # opening fence (>=3 backticks) + optional info
    (?P<current>.*?)                        # content
    (?P=fence1)                             # closing fence of identical length
    \s*
    \*\*\s*recommended\s+change\s*:\*\*     # **Recommended Change:**
    \s*
    (?P<fence2>`{3,})[^\n]*\n               # opening fence
    (?P<replacement>.*?)                    # content
    (?P=fence2)                             # closing fence of identical length
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
    """Strip outer blank lines; keep internal whitespace intact."""
    return text.strip("\n\r")


def _directive_key(text: str) -> str:
    """
    Normalize short directive-style replacement text.

    Examples:
        "KEEP EXACTLY AS WRITTEN." -> "KEEP EXACTLY AS WRITTEN"
        "  cut this  "             -> "CUT THIS"

    This intentionally only recognizes short, exact directive phrases. A real
    replacement paragraph that merely contains the words "keep" or "change" will
    not be treated as a directive.
    """
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
    """
    Collapse excessive blank lines across the whole file.

    Turns:
        line one\n\n\nline two

    into:
        line one\n\nline two

    This preserves normal paragraph spacing while removing extra blank lines.
    """
    # Normalize Windows/Mac line endings first.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace any run of 3+ newlines with exactly 2 newlines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Keep a single final newline, normal for text files.
    return text.rstrip("\n") + "\n"

# ---------------------------------------------------------------------------
# Backup path
# ---------------------------------------------------------------------------


def make_backup_path(chapter_path: Path) -> Path:
    """
    Write backups under E:\writer\<book>\...

    If the chapter path contains a 'chapters' directory, infer the book as the
    folder immediately before 'chapters' and preserve the path from there.
    Otherwise fall back to the parent folder name.
    """
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
# Block splitting
# ---------------------------------------------------------------------------


def _split_blocks(text: str) -> list[tuple[int, int]]:
    """
    Return (start, end) char offsets for each non-blank block.

    A block is a maximal run of consecutive non-blank lines. Blocks are
    separated by one or more blank lines. Each returned span includes the
    trailing newline of its last content line, so every boundary sits exactly
    at a line edge — which is what guarantees clean splices.
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
    """Collapse all runs of whitespace to single spaces for robust scoring."""
    return " ".join(s.split())


# ---------------------------------------------------------------------------
# Fuzzy matching (block-run based)
# ---------------------------------------------------------------------------


def _similarity(a: str, b: str) -> float:
    """SequenceMatcher ratio between two strings (0.0 – 1.0)."""
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def _count_blocks(needle: str) -> int:
    """How many blank-line-separated blocks does the needle look like?"""
    parts = re.split(r"\n[ \t]*\n", needle.strip())
    return max(1, len([p for p in parts if p.strip()]))


def _find_best_block_run(needle: str, haystack: str) -> tuple[float, int, int, str]:
    """
    Find the contiguous run of chapter blocks that best matches the needle.

    Returns (best_ratio, start_char, end_char, matched_substring). Boundaries
    are always block (paragraph) edges, so applying a replacement at these
    offsets can never split a line.
    """
    # Exact-match fast path (still snapped to nothing; exact is exact).
    pos = haystack.find(needle)
    if pos != -1:
        return 1.0, pos, pos + len(needle), needle

    blocks = _split_blocks(haystack)
    if not blocks:
        return 0.0, -1, -1, ""

    needle_flat = _flat(needle)
    k = _count_blocks(needle)

    # Try run lengths around the needle's apparent block count, since the AI's
    # paragraph breaks may not line up exactly with the chapter's.
    run_lengths = sorted({max(1, k + d) for d in (-1, 0, 1, 2)})

    best_ratio = 0.0
    best_start = -1
    best_end = -1

    n = len(blocks)
    for i in range(n):
        for L in run_lengths:
            if i + L > n:
                continue

            run_start = blocks[i][0]
            run_end = blocks[i + L - 1][1]
            candidate = haystack[run_start:run_end]
            ratio = _similarity(needle_flat, _flat(candidate))

            if ratio > best_ratio:
                best_ratio = ratio
                best_start = run_start
                best_end = run_end

    matched = haystack[best_start:best_end] if best_start != -1 else ""
    return best_ratio, best_start, best_end, matched


def match_edits(edits: list[Edit], chapter: str, threshold: float) -> None:
    """Populate each Edit's match_* fields in-place."""
    for edit in edits:
        if edit.is_noop:
            edit.match_ratio = 1.0
            edit.match_start = -1
            edit.match_end = -1
            edit.matched_text = ""
            edit.skip_reason = "no-op instruction"
            continue

        ratio, start, end, matched = _find_best_block_run(edit.current_raw, chapter)
        edit.match_ratio = ratio
        edit.match_start = start
        edit.match_end = end
        edit.matched_text = matched


def _boundaries_are_clean(haystack: str, start: int, end: int) -> bool:
    """Defensive assertion: block runs should always satisfy this."""
    if start < 0 or end < 0:
        return False
    if start > 0 and not haystack[start - 1].isspace():
        return False
    if end < len(haystack) and not haystack[end].isspace():
        return False
    return True


# ---------------------------------------------------------------------------
# Applying edits
# ---------------------------------------------------------------------------


def apply_edits(
    chapter: str,
    edits: list[Edit],
    threshold: float,
) -> tuple[str, list[str]]:
    """
    Apply edits in reverse order (highest char offset first) so that earlier
    offsets remain valid after each substitution.

    Returns (updated_chapter, log_lines).
    """
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
            e.skip_reason = "unclean boundary (refused to splice)"
            skipped.append(e)
        else:
            applicable.append(e)

    for e in skipped:
        logs.append(
            f"SKIP  edit {e.index:>2}  ratio={e.match_ratio:.3f}  ({e.skip_reason})"
        )

    applicable_sorted = sorted(applicable, key=lambda e: e.match_start, reverse=True)

    updated = chapter
    applied_count = 0

    for e in applicable_sorted:
        start, end = e.match_start, e.match_end

        if e.is_cut:
            # Swallow the following blank-line separator so we don't leave a gap.
            e_end = end
            while e_end < len(updated) and updated[e_end] == "\n":
                e_end += 1
            updated = updated[:start] + updated[e_end:]
            action = "CUT "
        else:
            # The matched block span includes the trailing newline of its last
            # content line; restore one so paragraph separation is preserved.
            repl = e.replacement
            if not repl.endswith("\n"):
                repl = repl + "\n"
            updated = updated[:start] + repl + updated[end:]
            action = "EDIT"

        applied_count += 1
        logs.append(
            f"OK    edit {e.index:>2}  ratio={e.match_ratio:.3f}  "
            f"{action}  blocks chars {start}-{end}"
        )

    # Re-sort OK/SKIP lines by edit index for readability.
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
    """Print a compact unified diff to stdout."""
    import difflib

    orig_lines = original.splitlines(keepends=True)
    upd_lines = updated.splitlines(keepends=True)
    diff = difflib.unified_diff(
        orig_lines,
        upd_lines,
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
    parser.add_argument(
        "--chapter",
        required=True,
        help="Path to the chapter Markdown file.",
    )
    parser.add_argument(
        "--edits",
        required=True,
        help="Path to the AI review Markdown file.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to disk. Default is dry-run only.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.82,
        help="Minimum similarity ratio to accept a match (0-1). Default 0.82.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip writing a .bak backup when --apply is used.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print a unified diff of changes to stdout.",
    )
    parser.add_argument(
        "--show-matches",
        action="store_true",
        help="Print what text was matched in the chapter for each edit.",
    )

    args = parser.parse_args()

    chapter_path = Path(args.chapter)
    edits_path = Path(args.edits)

    if not chapter_path.exists():
        sys.exit(f"Error: chapter file not found: {chapter_path}")
    if not edits_path.exists():
        sys.exit(f"Error: edits file not found: {edits_path}")

    chapter_text = chapter_path.read_text(encoding="utf-8")
    edits_markdown = edits_path.read_text(encoding="utf-8")

    edits = parse_edits(edits_markdown)
    if not edits:
        print("No edit pairs found in the review file.")
        print()
        print("Expected format in the review file:")
        print("  **Current Text:**")
        print("  ```")
        print("  ...text from chapter...")
        print("  ```")
        print("  **Recommended Change:**")
        print("  ```")
        print("  ...replacement text, or CUT THIS / KEEP EXACTLY AS WRITTEN...")
        print("  ```")
        return

    cut_count = sum(1 for e in edits if e.is_cut)
    noop_count = sum(1 for e in edits if e.is_noop)
    normal_count = len(edits) - cut_count - noop_count

    print(f"Parsed {len(edits)} edit pair(s) from: {edits_path.name}")
    print(f"  Normal replacements: {normal_count}")
    print(f"  Cuts/removals:       {cut_count}")
    print(f"  No-op skips:         {noop_count}")
    print(f"Chapter: {chapter_path.name}  ({len(chapter_text):,} chars)")
    print(f"Threshold: {args.threshold:.2f}\n")

    if noop_count:
        print(
            f"Detected {noop_count} no-op / keep-as-written instruction(s); "
            "these will be skipped safely.\n"
        )

    match_edits(edits, chapter_text, args.threshold)

    if args.show_matches:
        for e in edits:
            print(f"--- Edit {e.index}  ratio={e.match_ratio:.3f} ---")
            if e.is_noop:
                print("NO-OP instruction detected; no matching attempted.")
                print("DIRECTIVE:")
                print(repr(_directive_key(e.current_raw)))
                print()
                continue

            print("NEEDLE (from review):")
            print(repr(e.current_raw[:500]))
            print("MATCHED (in chapter):")
            print(repr(e.matched_text[:500]))
            print()

    updated_text, logs = apply_edits(chapter_text, edits, args.threshold)

    # Final formatting cleanup: remove excessive blank lines introduced by edits.
    cleaned_text = collapse_extra_blank_lines(updated_text)
    updated_text = cleaned_text

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
