import os
import re
import argparse
from pathlib import Path

# --- Configuration ---
TARGET_WORD_COUNT = 50000
TARGET_CHAPTERS = 33
TARGET_PER_CHAPTER = TARGET_WORD_COUNT / TARGET_CHAPTERS
# ---------------------

HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)


def natural_sort_key(text):
    """
    Sorts strings containing numbers naturally.
    Example: ['Chapter 1', 'Chapter 2', 'Chapter 10']
    instead of ['Chapter 1', 'Chapter 10', 'Chapter 2']
    """
    def atoi(value):
        return int(value) if value.isdigit() else value

    return [atoi(c) for c in re.split(r'(\d+)', text)]


def extract_leading_metadata(content):
    """
    Extracts the leading HTML comment block from the top of the file, if present.
    """
    stripped_content = content.lstrip()

    if not stripped_content.startswith('<!--'):
        return ''

    end_idx = stripped_content.find('-->')
    if end_idx == -1:
        return ''

    metadata_block = stripped_content[4:end_idx].strip()
    return metadata_block


def strip_front_matter(content):
    """
    Converts Hugo TOML front matter at the top of a chapter:

        +++
        title = "15: What Is Digital Life?"
        ...
        +++

    into:

        ## 15: What Is Digital Life?

    Also supports the older leading HTML-comment metadata format
    and removes remaining HTML comments from the chapter.
    """
    stripped_content = content.lstrip()

    # ------------------------------------------------------------
    # 1. Hugo TOML front matter: +++ ... +++
    # ------------------------------------------------------------
    if stripped_content.startswith("+++"):
        lines = stripped_content.splitlines()

        end_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "+++":
                end_index = i
                break

        if end_index is not None:
            front_matter = "\n".join(lines[1:end_index])

            # Extract title from:
            # title = "15: What Is Digital Life?"
            title_match = re.search(
                r'^\s*title\s*=\s*["\'](.+?)["\']\s*$',
                front_matter,
                flags=re.MULTILINE,
            )

            body = "\n".join(lines[end_index + 1:]).lstrip()

            if title_match:
                title = title_match.group(1).strip()
                stripped_content = f"## {title}\n\n{body}"
            else:
                stripped_content = body

    # ------------------------------------------------------------
    # 2. Older HTML-comment front matter
    # ------------------------------------------------------------
    elif stripped_content.startswith("<!--"):
        end_idx = stripped_content.find("-->")
        if end_idx != -1:
            stripped_content = stripped_content[end_idx + 3:].lstrip()

    # ------------------------------------------------------------
    # 3. Remove any remaining HTML comments
    # ------------------------------------------------------------
    stripped_content = HTML_COMMENT_RE.sub("", stripped_content)

    # Normalize excessive blank lines
    stripped_content = re.sub(r"\n{3,}", "\n\n", stripped_content).strip()

    return stripped_content


def count_words(text):
    """
    Rough word count based on whitespace splitting.
    """
    return len(text.split())


def write_metadata_entry(outfile, file_path, metadata):
    """
    Writes one chapter's metadata into the merged metadata file.
    """
    outfile.write(f"# {file_path.stem}\n\n")

    if metadata.strip():
        outfile.write(metadata.strip())
        outfile.write("\n\n")
    else:
        outfile.write("_No metadata found._\n\n")

    outfile.write("---\n\n")


def find_metadata_file(chapter_path, metadata_dir):
    """
    Attempts to find a corresponding .yaml metadata file for a given chapter.
    """
    stem = chapter_path.stem
    
    # 1. Exact stem match (e.g., chapters/05-molt.md -> metadata/05-molt.yaml)
    exact_match = metadata_dir / f"{stem}.yaml"
    if exact_match.exists():
        return exact_match
        
    # 2. Try removing common prefixes like 'chapter-' or 'ch_'
    clean_stem = re.sub(r'^(chapter[-_]?|ch[-_]?)', '', stem, flags=re.IGNORECASE)
    clean_match = metadata_dir / f"{clean_stem}.yaml"
    if clean_match.exists():
        return clean_match
        
    # 3. Fallback: extract numbers to find the right chapter 
    # (e.g., "05" from "chapter-05-molt" matching "05-molt.yaml")
    chapter_nums = re.findall(r'\d+', stem)
    if chapter_nums:
        target_num = chapter_nums[0] 
        for yaml_file in metadata_dir.glob("*.yaml"):
            if target_num in yaml_file.stem:
                return yaml_file
                
    return None


def read_optional_readme(base_dir):
    """
    Reads README.md from the base directory if present.
    """
    readme_path = base_dir / "TOP.md"

    if not readme_path.exists():
        return "", ""

    with open(readme_path, "r", encoding="utf-8") as infile:
        content = infile.read()

    metadata = extract_leading_metadata(content)
    clean_content = strip_front_matter(content)

    return clean_content, metadata


def merge_and_count():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Merge and count words for book chapters.")
    parser.add_argument(
        "--up-to", 
        type=int, 
        help="Merge chapters only up to this chapter number (e.g., 13). If omitted, merges all chapters."
    )
    args = parser.parse_args()
    # ------------------------

    base_dir = Path(".")
    chapters_dir = base_dir / "content/books/digital-life"
    metadata_dir = base_dir / "metadata"

    output_file = base_dir / "digital-life.md"
    output_metadata_file = base_dir / "digital-life_metadata.md"

    if not chapters_dir.exists():
        print(f"Error: Directory '{chapters_dir}' not found.")
        print("Please ensure this script is run from the base directory.")
        return

    md_files = [f for f in chapters_dir.iterdir() if f.suffix.lower() == ".md"]
    md_files.sort(key=lambda p: natural_sort_key(p.name))

    # --- Filter chapters if --up-to is provided ---
    if args.up_to is not None:
        filtered_files = []
        for f in md_files:
            nums = re.findall(r'\d+', f.stem)
            if nums:
                chapter_num = int(nums[0])
                if chapter_num <= args.up_to:
                    filtered_files.append(f)
            else:
                # Keep files without numbers (e.g., prologue, intro, appendix)
                filtered_files.append(f)
        md_files = filtered_files
        print(f"--- Partial Build Mode: Merging up to Chapter {args.up_to} ---\n")
    # ----------------------------------------------

    if not md_files:
        print(f"No markdown files found in '{chapters_dir}' matching the criteria.")
        return

    readme_content, readme_metadata = read_optional_readme(base_dir)
    has_readme = bool(readme_content.strip())

    print(f"Processing {len(md_files)} chapter(s)...\n")
    print(f"README found: {'yes' if has_readme else 'no'}")
    print(f"Metadata directory: '{metadata_dir}' ({'found' if metadata_dir.exists() else 'not found'})")
    print(f"Target per chapter: {TARGET_PER_CHAPTER:,.0f} words\n")

    print(
        f"{'CHAPTER':<30} {'WORDS':>10} {'% TARGET':>10} "
        f"{'DELTA':>10} {'CUMULATIVE':>12} {'META':>8}"
    )
    print("-" * 88)

    total_words = 0
    cumulative_words = 0

    with (
        open(output_file, "w", encoding="utf-8") as book_outfile,
        open(output_metadata_file, "w", encoding="utf-8") as metadata_outfile,
    ):
        metadata_outfile.write("# Coin Metadata\n\n")

        # ------------------------------------------------------------
        # 1. Write README first, before all chapters
        # ------------------------------------------------------------
        if has_readme:
            readme_words = count_words(readme_content)

            book_outfile.write(readme_content)
            book_outfile.write("\n\n---\n\n")

            metadata_outfile.write("# README\n\n")
            if readme_metadata.strip():
                metadata_outfile.write(readme_metadata.strip())
                metadata_outfile.write("\n\n")
            else:
                metadata_outfile.write("_No metadata found._\n\n")
            metadata_outfile.write("---\n\n")

            print(
                f"{'README.md':<30} "
                f"{readme_words:>10,} "
                f"{'':>10} "
                f"{'':>10} "
                f"{cumulative_words:>12,} "
                f"{'yes' if readme_metadata.strip() else 'no':>8}"
            )

        # ------------------------------------------------------------
        # 2. Then write chapters and chapter metadata
        # ------------------------------------------------------------
        for file_path in md_files:
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()

            clean_content = strip_front_matter(content)
            
            # Try to find metadata in the metadata directory first
            metadata = ""
            if metadata_dir.exists():
                meta_file = find_metadata_file(file_path, metadata_dir)
                if meta_file:
                    with open(meta_file, "r", encoding="utf-8") as meta_infile:
                        metadata = meta_infile.read()
            
            # Fallback to HTML comment if no yaml file was found
            if not metadata.strip():
                metadata = extract_leading_metadata(content)

            chapter_words = count_words(clean_content)
            total_words += chapter_words
            cumulative_words += chapter_words

            chapter_pct = (chapter_words / TARGET_PER_CHAPTER) * 100
            chapter_delta = chapter_words - TARGET_PER_CHAPTER
            has_metadata = "yes" if metadata.strip() else "no"

            book_outfile.write(clean_content)
            book_outfile.write("\n\n---\n\n")

            write_metadata_entry(metadata_outfile, file_path, metadata)

            print(
                f"{file_path.name:<30} "
                f"{chapter_words:>10,} "
                f"{chapter_pct:>9.1f}% "
                f"{chapter_delta:>+10.0f} "
                f"{cumulative_words:>12,} "
                f"{has_metadata:>8}"
            )

    print("-" * 88)
    print(
        f"{'TOTAL CHAPTER WORDS':<30} "
        f"{total_words:>10,} "
        f"{'':>10} "
        f"{'':>10} "
        f"{cumulative_words:>12,}"
    )
    print("-" * 88)

    progress_pct = (total_words / TARGET_WORD_COUNT) * 100

    print(f"\nTarget: {TARGET_WORD_COUNT:,} words")
    print(f"Current Chapter Progress: {progress_pct:.1f}%")

    if total_words >= TARGET_WORD_COUNT:
        print("Status: Target Met!")
    else:
        remaining = TARGET_WORD_COUNT - total_words
        # Calculate remaining chapters based on whether we are in partial build mode
        effective_target_chapters = args.up_to if args.up_to is not None else TARGET_CHAPTERS
        remaining_chapters = effective_target_chapters - len(md_files)

        print(f"Remaining: {remaining:,} words")

        if remaining_chapters > 0:
            avg_needed = remaining / remaining_chapters
            print(f"Avg words needed per remaining chapter: {avg_needed:,.0f}")
        elif args.up_to is not None:
            print("Note: All requested chapters for this partial build have been processed.")

    print("\nSuccess!")
    print(f"Book with separators: '{output_file}'")
    print(f"Merged metadata: '{output_metadata_file}'")


if __name__ == '__main__':
    merge_and_count()