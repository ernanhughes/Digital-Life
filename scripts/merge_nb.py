from copy import deepcopy
from pathlib import Path

import nbformat


NOTEBOOK_DIR = Path("notebooks")


def merge_notebooks(output_name, parts):
    notebooks = [
        nbformat.read(NOTEBOOK_DIR / filename, as_version=4)
        for filename in parts
    ]

    merged = nbformat.v4.new_notebook()
    merged.metadata = deepcopy(notebooks[0].metadata)

    cells = []

    for index, (filename, notebook) in enumerate(zip(parts, notebooks)):
        if index > 0:
            cells.append(
                nbformat.v4.new_markdown_cell(
                    f"---\n\n## Continued experiment\n\n"
                    f"This section was originally reconstructed separately as "
                    f"`{filename}` and is now part of this chapter's canonical notebook."
                )
            )

        cells.extend(deepcopy(notebook.cells))

    merged.cells = cells

    output = NOTEBOOK_DIR / output_name
    nbformat.write(merged, output)

    print(f"Wrote {output}")


merge_notebooks(
    "03-look-at-this-thing.ipynb",
    [
        "03a-lenia-persistent-pattern.ipynb",
        "03b-physarum-stigmergy-turnover.ipynb",
    ],
)

merge_notebooks(
    "08-the-crystal-gets-a-past.ipynb",
    [
        "08a-checkpoint-state-vs-history.ipynb",
        "08b-pulse-signalling-and-matched-history.ipynb",
    ],
)