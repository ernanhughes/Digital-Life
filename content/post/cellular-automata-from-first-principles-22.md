+++
date = '2026-08-10T18:55:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 22: Classify Rule Behaviour'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Classification', 'Wolfram Classes']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 22: Classify Rule Behaviour

Cellular automata are often described using four broad behavioral classes:

```text
Class I   -> settles to homogeneous behavior
Class II  -> settles to simple stable or periodic structures
Class III -> chaotic or apparently random behavior
Class IV  -> persistent local structures and complex interactions
```

These labels are useful vocabulary.

But if we want to use them experimentally, we should connect them to measurable evidence rather than treating them as magic categories.

---

## Start with features

For each rule, collect a behavioral fingerprint:

```python
features = {
    "mean_density": ...,
    "mean_activity": ...,
    "tail_activity": ...,
    "mean_entropy": ...,
    "compression_ratio": ...,
    "cycle_period": ...,
    "sensitivity": ...,
}
```

Each feature captures a different aspect of the dynamics.

---

## Heuristics before machine learning

A first classifier can be explicit and inspectable:

```python
def rough_class(metrics):
    if metrics["tail_activity"] < 0.01:
        if metrics["mean_entropy"] < 0.1:
            return "I"
        return "II"

    if metrics["sensitivity"] > 0.35 and metrics["compression_ratio"] > 0.85:
        return "III"

    return "IV-candidate"
```

This is deliberately approximate.

The point is not that these thresholds define the canonical classes.

The point is to make our assumptions visible.

---

## Why Class IV is hard

Class IV behavior is often described in terms of localized structures, interactions and long transients.

Those are harder to capture with simple global statistics.

A rule can have moderate entropy and activity without containing coherent objects.

So a useful Class IV detector may need richer features:

```text
localized persistence
moving motifs
collision diversity
long transient lengths
spatial mutual information
compressible background + irregular structures
```

This is a research problem, not a one-line threshold.

---

## Plot feature space

Even two features can reveal clusters:

```python
import matplotlib.pyplot as plt

x = [row["mean_entropy"] for row in records]
y = [row["tail_activity"] for row in records]
labels = [row["rule"] for row in records]

plt.scatter(x, y)
plt.xlabel("mean entropy")
plt.ylabel("tail activity")
plt.show()
```

Add sensitivity or compression as a third dimension in separate plots.

Rules that looked unrelated by rule number may sit close together behaviorally.

---

## Standardize before comparing distances

Metrics have different ranges.

If we calculate Euclidean distance directly, one large-scale feature can dominate.

Standardize them:

```python
X = np.array([
    [
        row["mean_density"],
        row["mean_activity"],
        row["mean_entropy"],
        row["compression_ratio"],
        row["sensitivity"],
    ]
    for row in records
])

X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)
```

Now nearest-neighbor comparisons become more meaningful.

---

## Classification versus discovery

Classification asks:

> Which known category does this rule resemble?

Discovery asks:

> Which rules behave unusually relative to the rest?

The second question may be more interesting.

Compute distance from the feature-space mean or from nearby clusters and inspect outliers.

An unexpected rule is often more valuable than a rule that cleanly fits a label.

---

## Keep the evidence

If a program labels Rule 110 as a Class IV candidate, store the measurements that caused the decision.

```python
classification = {
    "rule": 110,
    "label": "IV-candidate",
    "evidence": metrics,
    "classifier": "rough-v1",
}
```

This makes the classification reproducible and revisable.

---

## Next: exhaustive search

For elementary cellular automata, the entire rule space contains only 256 rules.

That is tiny enough to evaluate exhaustively.

In the next chapter we will stop choosing famous rules by name and let Python run **every rule**, measure every run, rank candidates and generate an experimental catalog.