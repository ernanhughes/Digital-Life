+++
date = '2026-08-10T18:56:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 23: Search All 256 Elementary Rules'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Search', 'Elementary Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 23: Search All 256 Elementary Rules

Elementary cellular automata give us a rare luxury.

The complete rule space is tiny.

There are only:

```text
256 rules
```

So we do not need sampling, intuition or famous examples.

We can evaluate every rule.

---

## Build an experiment runner

Assume we already have:

```python
run_rule(rule_number, width, generations, initial_state)
fingerprint(history)
```

Then exhaustive search is simple:

```python
def scan_rules(initial_state, width=201, generations=200):
    records = []

    for rule in range(256):
        history = run_rule(
            rule,
            width=width,
            generations=generations,
            initial_state=initial_state,
        )

        records.append({
            "rule": rule,
            **fingerprint(history),
        })

    return records
```

The hard part is no longer execution.

It is deciding what to look for.

---

## Rank by different questions

Most active rules:

```python
sorted(records, key=lambda r: r["mean_activity"], reverse=True)[:10]
```

Most persistent:

```python
sorted(records, key=lambda r: r["tail_activity"], reverse=True)[:10]
```

Most compressible:

```python
sorted(records, key=lambda r: r["compression_ratio"])[:10]
```

Highest estimated sensitivity:

```python
sorted(records, key=lambda r: r["sensitivity"], reverse=True)[:10]
```

Each ranking answers a different question.

---

## Search for a region, not a maximum

If we maximize entropy alone, we may mostly find noise-like behavior.

Instead define constraints:

```python
candidates = [
    row for row in records
    if 0.35 < row["mean_entropy"] < 0.95
    and row["tail_activity"] > 0.05
    and row["compression_ratio"] < 0.9
]
```

This searches for a behavioral region rather than a single extreme.

---

## Multiple initial conditions

One single-cell experiment strongly favors rules that respond to sparse seeds.

Run several protocols:

```text
single active cell
random density 10%
random density 50%
periodic pattern
structured perturbation
```

Store a record per `(rule, protocol, seed)`.

Then aggregate by rule.

This prevents one arbitrary setup from becoming the definition of the rule.

---

## Save the catalog

Python's standard library is enough:

```python
import csv

with open("eca-catalog.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
```

Now rule exploration becomes repeatable data analysis.

---

## Generate contact sheets

Numbers should guide inspection, not eliminate it.

Take the top candidates and render them together:

```python
fig, axes = plt.subplots(4, 4, figsize=(12, 12))

for ax, row in zip(axes.flat, candidates[:16]):
    history = run_rule(row["rule"], width=151, generations=120)
    ax.imshow(history, cmap="binary", interpolation="nearest")
    ax.set_title(f"Rule {row['rule']}")
    ax.axis("off")
```

The workflow is now:

```text
exhaustive execution
        ↓
measurement
        ↓
filter/rank
        ↓
visual inspection
        ↓
hypothesis
```

That is much stronger than browsing rules at random.

---

## Validate famous examples

Our pipeline should rediscover familiar behavioral differences among rules such as 0, 4, 30, 90, 110 and 184.

If it cannot separate obviously different cases, the measurement suite needs work.

Known examples become tests for our instrumentation rather than answers we hard-code.

---

## The luxury disappears quickly

Elementary CA are unusually small.

Increase the neighborhood radius, number of states or dimensions and the number of possible rules explodes.

Then exhaustive search becomes impossible.

The next chapter asks what to do when we can no longer evaluate everything.