+++
date = '2026-08-10T18:52:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 19: Entropy and Information'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Entropy', 'Information Theory']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 19: Entropy and Information

A row with almost all zeros is highly predictable.

A row containing a balanced mixture of zeros and ones is less predictable.

Shannon entropy gives us a precise way to measure that uncertainty.

---

## Binary entropy

If a binary state contains a fraction `p` of ones, then:

```text
H = -p log2(p) - (1-p) log2(1-p)
```

In Python:

```python
import math
import numpy as np


def binary_entropy(state):
    p = float(np.mean(state))

    if p in (0.0, 1.0):
        return 0.0

    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
```

The maximum is `1` bit when zeros and ones occur equally often.

---

## Entropy is not complexity

Consider random coin flips.

They can have nearly maximal entropy.

But random noise has little reusable structure.

So:

```text
high entropy != complex organization
```

Entropy measures uncertainty in a distribution.

It does not tell us whether patterns persist, interact or compute.

---

## Neighborhood entropy

Instead of counting individual cells, count local patterns.

For a radius-1 elementary automaton, collect neighborhoods of length three:

```python
from collections import Counter


def neighborhood_entropy(state, width=3):
    patterns = []
    n = len(state)

    for i in range(n):
        pattern = tuple(state[(i + j) % n] for j in range(width))
        patterns.append(pattern)

    counts = Counter(patterns)
    total = len(patterns)

    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy
```

Now we measure diversity of local structures rather than only the global proportion of ones.

---

## Entropy over time

```python
def entropy_curve(history):
    return np.array([binary_entropy(row) for row in history])
```

Useful questions include:

```text
Does entropy collapse?
Does it remain high?
Does it oscillate?
Does it rise from a simple seed?
```

That last case is particularly interesting: simple initial conditions producing sustained informational diversity.

---

## Compare entropy with activity

Create a joint record:

```python
def information_summary(history):
    entropies = entropy_curve(history)
    activities = np.array([
        np.mean(history[t] != history[t - 1])
        for t in range(1, len(history))
    ])

    return {
        "mean_entropy": float(entropies.mean()),
        "tail_entropy": float(entropies[-50:].mean()),
        "mean_activity": float(activities.mean()),
    }
```

Rules can now occupy different regions:

```text
low entropy / low activity
high entropy / high activity
high entropy / low activity
moderate entropy / sustained activity
```

Those regions often correspond to qualitatively different dynamics.

---

## Compression as another lens

Structured data often compresses well.

Random data usually does not.

Python gives us a quick experiment:

```python
import zlib


def compression_ratio(history):
    raw = np.packbits(history.astype(np.uint8)).tobytes()
    compressed = zlib.compress(raw)
    return len(compressed) / len(raw)
```

This is not a formal complexity measure, but it can expose repeated structure that simple cell entropy misses.

---

## The interesting middle

A recurring idea in complex systems is that interesting behavior often appears between two extremes:

```text
perfect order <------> random disorder
```

Cellular automata make that idea visible.

Some rules freeze.

Some become repetitive.

Some behave almost chaotically.

A smaller set supports persistent structures and interactions.

Our metrics will help us search that middle rather than selecting purely by eye.

---

## Next: repetition

Entropy tells us about uncertainty.

But a system can have a rich-looking state and still repeat exactly every few generations.

The next chapter adds explicit detection of fixed points, cycles and attractors.