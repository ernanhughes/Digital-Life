+++
date = '2026-08-10T20:57:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 54: Make Experiments Reproducible'
categories = ['Programming', 'Research']
tags = ['Cellular Automata', 'Reproducibility', 'Experiments', 'Python']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 54: Make Experiments Reproducible

By this stage the book contains many systems whose behavior depends on parameters, seeds and implementation choices.

If we cannot reconstruct a run, we cannot really compare it.

---

## Treat configuration as data

```python
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ExperimentConfig:
    model: str
    width: int
    height: int
    steps: int
    seed: int
    backend: str
    dtype: str
```

Then extend with model-specific parameters rather than hiding them in notebook cells.

---

## Seed every relevant source of randomness

```python
import random
import numpy as np
import torch


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
```

Determinism can still depend on backend and operation, but explicit seeding is the minimum contract.

---

## Save the exact configuration

```python
import json
from pathlib import Path


def save_config(config, path):
    Path(path).write_text(
        json.dumps(asdict(config), indent=2),
        encoding="utf-8",
    )
```

A figure without the parameters that generated it is a dead artifact.

---

## Record software context

Useful experiment metadata includes:

```text
Git commit
Python version
library versions
device
operating system
random seed
input data hash
```

This does not guarantee identical results forever.

It makes discrepancies explainable.

---

## Give each run an identity

A simple run directory might look like:

```text
runs/
  2026-08-10T205700_rule110_seed42/
      config.json
      metrics.json
      final.npy
      frames/
      benchmark.json
```

Better still, derive a stable ID from normalized configuration plus code version.

---

## Separate inputs, outputs and derived artifacts

```text
inputs     → seeds, maps, targets
outputs    → raw states, checkpoints, metrics
derived    → plots, animations, summary tables
```

That distinction matters because a graph should be regenerable from raw results.

---

## Replay should be a first-class operation

```python
def replay(config):
    seed_everything(config.seed)
    model = build_model(config)
    state = build_initial_state(config)
    return run(model, state, config.steps)
```

The strongest test is simple:

```text
Can another process reconstruct this run from the saved configuration?
```

---

## Reproducibility enables debugging

When an interesting organism disappears after a code change, compare:

```text
same config
old commit
new commit
```

Now the change in behavior is evidence about the implementation.

Without replay, it is merely a memory that something once looked different.

---

## Reproducibility enables search

Search produces thousands of candidates.

A candidate record should contain enough information to recreate it:

```python
candidate = {
    "score": 0.812,
    "seed": 3917,
    "parameters": params,
    "steps": 800,
    "model": "lenia",
}
```

Never save only the top PNG.

---

## The experiment is the unit of knowledge

A useful mental model is:

```text
claim
  ↓
configuration
  ↓
execution
  ↓
raw result
  ↓
metric / figure
```

That chain is what lets the book move from demonstrations toward real computational experiments.

Next we will use this structure to run parameter sweeps and benchmarks systematically.