+++
date = '2026-08-10T21:00:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 57: Build a Cellular Automata Laboratory'
categories = ['Programming', 'Software Design']
tags = ['Cellular Automata', 'Python', 'Experiments', 'Architecture']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 57: Build a Cellular Automata Laboratory

We now have enough pieces to stop thinking in terms of isolated scripts.

A useful cellular-automata laboratory should let us define, run, measure, replay and visualize experiments across many kinds of automata without hiding the mechanisms we spent the whole book learning.

---

## The laboratory is not the model

Keep these concerns separate:

```text
model definition
execution backend
experiment configuration
metrics
artifacts
analysis
```

A rule should not know where its PNG is saved.

A renderer should not decide how a cell updates.

---

## One possible project structure

```text
ca_lab/
├── models/
│   ├── elementary.py
│   ├── life.py
│   ├── lenia.py
│   └── nca.py
├── backends/
│   ├── numpy_backend.py
│   ├── torch_backend.py
│   └── fft_backend.py
├── experiments/
│   ├── config.py
│   ├── runner.py
│   └── sweep.py
├── metrics/
│   ├── activity.py
│   ├── entropy.py
│   ├── recurrence.py
│   └── robustness.py
├── render/
│   ├── figures.py
│   └── animation.py
├── artifacts/
├── tests/
└── cli.py
```

The exact folders are less important than the boundaries.

---

## A model contract

```python
class Model:
    def initial_state(self, config):
        raise NotImplementedError

    def step(self, state):
        raise NotImplementedError
```

A learned model can additionally expose parameters or checkpoints.

A deterministic classical rule does not need to pretend it has them.

---

## An experiment contract

```python
@dataclass
class Experiment:
    config: ExperimentConfig
    model: Model
    observers: list

    def run(self):
        state = self.model.initial_state(self.config)

        for step in range(self.config.steps):
            state = self.model.step(state)
            for observer in self.observers:
                observer(step, state)

        return state
```

This creates one execution path for:

```text
Rule 30
Life
traffic
forest fire
Lenia
NCA
```

without forcing their internal state to be identical.

---

## A command-line interface makes experiments concrete

Conceptually:

```bash
ca-lab run experiments/rule110.yaml
ca-lab sweep experiments/lenia-search.yaml
ca-lab replay runs/a81f2c
ca-lab render runs/a81f2c
ca-lab benchmark benchmarks/neighborhoods.yaml
```

A CLI is useful because it turns an experiment into something that can be executed outside a notebook.

---

## Keep notebooks at the edge

Notebooks are excellent for:

```text
exploration
explanation
plotting
interactive inspection
```

They are poor as the only location of core model logic.

Prefer:

```text
library code
    ↓
experiment runner
    ↓
notebook imports results
```

rather than copying the implementation between notebooks.

---

## Test the mechanisms

The laboratory should contain small invariant tests:

```python
def test_rule184_conserves_cars():
    before = state.sum()
    after = rule184_step(state).sum()
    assert before == after
```

and integration tests:

```text
saved config can replay
artifact manifest points to existing result
NumPy and PyTorch reference implementations agree within tolerance
```

Tests make the experimental infrastructure trustworthy.

---

## Store raw evidence before summaries

A good run might produce:

```text
config.json
metadata.json
metrics.csv
final_state.npy
checkpoints/
frames/
```

Then derived outputs:

```text
summary.json
plots/
animation.mp4
report.md
```

If a plot is wrong, regenerate it from raw output.

Do not rerun an expensive experiment merely because a label was misspelled.

---

## Make comparison a first-class operation

```bash
ca-lab compare runs/a81f2c runs/b114e9
```

A comparison might show:

```text
parameter differences
metric differences
runtime differences
final-state distance
behavioral fingerprints
```

Now changing an implementation or rule becomes an explicit experiment.

---

## The laboratory preserves what the book teaches

The architecture should not abstract away the subject until all automata look like generic black boxes.

The point is the opposite.

It should preserve inspectable concepts:

```text
state
neighborhood
rule
update schedule
measurement
search
perturbation
```

while removing accidental duplication around them.

---

## We are ready for the capstone

The final chapter will use the whole workflow:

```text
define a search space
run reproducible experiments
find a candidate
measure it
perturb it
compare alternatives
inspect its computation
produce publication artifacts
state only what the evidence supports
```

That is the complete journey of the book.