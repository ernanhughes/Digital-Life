import re
import yaml
import os
from pathlib import Path

def split_metadata_to_yaml(input_file, output_dir="."):
    """
    Read the Digital Life Metadata.txt file, split by "---" separators,
    extract each chapter's metadata, and write it to a YAML file
    named after the chapter slug (e.g., 01-how-to-read-this-book.yaml).
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split on lines that are exactly "---" (possibly with surrounding newlines)
    chunks = re.split(r'\n---\n', content)

    # The first chunk is the README / header; skip it.
    for chunk in chunks[1:]:
        chunk = chunk.strip()
        if not chunk:
            continue

        lines = chunk.splitlines()
        if not lines:
            continue

        # Find the first line that starts with "# " (the chapter heading)
        heading_line = None
        heading_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("# "):
                heading_line = line.strip()
                heading_idx = i
                break

        if heading_line is None:
            print(f"Skipping chunk without heading: {chunk[:50]}...")
            continue

        # Extract the slug: everything after "# " (trim whitespace)
        slug = heading_line[2:].strip()  # remove "# " prefix

        # Remove the heading line from the chunk
        yaml_lines = lines[:heading_idx] + lines[heading_idx+1:]
        yaml_text = "\n".join(yaml_lines).strip()

        try:
            data = yaml.safe_load(yaml_text)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML for {slug}: {e}")
            continue

        # Use slug as filename, but we can also verify with document_id
        if "document_id" in data and data["document_id"] != slug:
            print(f"Warning: slug '{slug}' differs from document_id '{data['document_id']}'. Using slug.")

        filename = f"{slug}.yaml"
        output_path = Path(output_dir) / filename

        with open(output_path, 'w', encoding='utf-8') as out_f:
            yaml.dump(data, out_f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"Written: {output_path}")

if __name__ == "__main__":
    # Adjust input file name if needed
    input_file = "test.md"  # or the actual file path
    output_dir = "./metadata/books/digital-life"  # change to your desired output directory
    split_metadata_to_yaml(input_file, output_dir)