# Digital Crystal Visualization Layer

This directory contains reusable rendering code for canonical Digital Crystal
figures used by the Digital Life book.

The visualization layer sits after the research scripts and notebooks:

- research scripts produce full experimental evidence and artifacts;
- notebooks audit the chapter argument in executable form;
- these scripts turn real simulation states and canonical artifacts into
  consistent book/web images.

The figures are not generic illustrations. Each chapter script loads the
chapter's research artifacts and renders a representative Digital Crystal state
from the frozen substrate mechanics.

Run a visual script directly from the repository root, for example:

```bash
python scripts/books/digital-life/ch25_budget_redistribution_visual.py
```

Each script writes PNG files to:

```text
static/images/books/digital-life/visuals/
```

and writes a JSON sidecar describing chapter, research lineage, source
artifacts, and which parts are measured evidence versus visual encoding.

`PROFILE = "quick"` uses a compact representative state plus canonical artifact
values. `PROFILE = "canonical"` is reserved for future scripts that rerun full
canonical simulations; current scripts are canonical-artifact-based and do not
rerun expensive experiments by default.
