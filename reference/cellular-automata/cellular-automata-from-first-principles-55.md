+++
date = '2026-08-10T20:58:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 55: Run Parameter Sweeps and Benchmarks'
categories = ['Programming', 'Research']
tags = ['Cellular Automata', 'Benchmarking', 'Parameter Search', 'Experiments']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 55: Run Parameter Sweeps and Benchmarks

Once experiments are reproducible, we can stop treating parameters as one-off choices and start mapping behavior systematically.

A parameter sweep is not merely a convenience.

It is a way to turn a model into a measurable landscape.

---

## Build a grid of experiments

```python
from itertools import product

mus = [0.12, 0.14, 0.16]
sigmas = [0.01, 0.02, 0.03]

configs = [
    {"mu": mu, "sigma": sigma, "seed": seed}
    for mu, sigma, seed in product(mus, sigmas, range(10))
]
```

Notice the seed axis.

One run per parameter setting is rarely enough for stochastic systems.

---

## Collect structured results

```python
results = []

for config in configs:
    outcome = run_experiment(config)
    results.append({
        **config,
        "mass": outcome.mass,
        "activity": outcome.activity,
        "entropy": outcome.entropy,
        "survived": outcome.survived,
    })
```

The output is now a dataset.

---

## Summarize across seeds

```python
import pandas as pd

frame = pd.DataFrame(results)
summary = frame.groupby(["mu", "sigma"]).agg(
    mean_mass=("mass", "mean"),
    mean_activity=("activity", "mean"),
    survival_rate=("survived", "mean"),
)
```

Averages are useful, but so are distributions.

A parameter setting with mean score `0.8` and huge variance behaves differently from one with the same mean and tiny variance.

---

## Benchmark implementations fairly

Suppose we compare:

```text
NumPy shifts
SciPy convolution
PyTorch CPU
PyTorch GPU
FFT NumPy
FFT PyTorch
```

Hold the workload fixed.

For example:

```text
512×512 grid
32-cell kernel radius
float32
500 steps
same initial state
no rendering
```

Then repeat enough times to understand variance.

---

## Report throughput and latency

For interactive simulation, latency per step may matter.

For large sweeps, total throughput may matter more.

Record both when useful:

```python
{
    "seconds_per_step": elapsed / steps,
    "steps_per_second": steps / elapsed,
    "world_steps_per_second": batch * steps / elapsed,
}
```

Batch throughput can reveal advantages hidden by single-world benchmarks.

---

## Use coarse-to-fine search

Dense exhaustive sweeps become expensive quickly.

A practical strategy is:

```text
coarse grid
   ↓
identify promising regions
   ↓
refine locally
   ↓
evaluate robustness
```

This is exactly the search philosophy we introduced earlier for rule spaces and Lenia organisms.

---

## Do not optimize a single metric blindly

Suppose we search for:

```text
high activity
```

The easiest solution may be unstructured flicker.

Suppose we search for:

```text
high entropy
```

The easiest solution may be noise.

Useful search usually combines constraints and measurements:

```text
persist
remain bounded
move
recover
avoid saturation
retain morphology
```

There is no universal interestingness function.

---

## Preserve the failures

Search pipelines often save only winners.

That throws away valuable information.

Failures can reveal:

```text
parameter cliffs
unstable regions
collapsed states
explosive dynamics
implementation bugs
```

A map of failure modes is part of the result.

---

## Sweep visualization

For two parameters, make heatmaps.

For more, use slices, parallel coordinates, scatter matrices or dimensionality reduction cautiously.

The visualization should answer a question such as:

> Where does stable persistence occur?

not merely display every available number.

---

## Benchmarks become regression tests

If an optimization changes runtime from:

```text
100 steps/s → 600 steps/s
```

record it.

If a later change drops it back to 250, the benchmark should make that visible.

Performance results can be versioned just like behavioral results.

---

## From result tables to publication artifacts

We now have reproducible configurations and structured result datasets.

The next step is to turn those results into figures and animations without losing the chain back to the experiment that produced them.