+++
date = '2026-08-10T18:50:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 17: Measure a Cellular Automaton'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Metrics', 'Simulation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 17: Measure a Cellular Automaton

Up to this point we have mostly **looked at** cellular automata.

That is useful.

It is also limiting.

A human can inspect a handful of spacetime diagrams.

We cannot reliably inspect:

```text
256 elementary rules
× several initial conditions
× several widths
× hundreds of generations
× repeated stochastic runs
```

by eye.

If we want to compare rules, search for interesting behavior or eventually optimize a rule for some objective, we need to turn behavior into data.

This chapter builds the measurement layer.

---

## A simulation produces a trajectory

For a one-dimensional binary cellular automaton, a complete run can be stored as:

```python
history.shape
# (generations, cells)
```

Every row is one state of the world.

So:

```text
history[t]
```

means:

```text
the complete spatial state at generation t
```

The matrix is not merely something to plot.

It is a dataset.

We can ask:

```text
How many cells are active?

How much changes between generations?

How fragmented is the spatial pattern?

Does the system become fixed?

Does it repeat?

How sensitive is it to initial conditions?
```

No single answer defines complexity.

But each answer exposes one observable property of the dynamics.

---

## Density

The simplest measurement is the fraction of active cells:

```python
import numpy as np


def density(state):
    return float(np.mean(state))
```

For:

```text
00011101
```

four of eight cells are active:

```text
density = 0.5
```

Across an entire run:

```python
def density_curve(history):
    return np.mean(history, axis=1)
```

Now we have:

```text
generation -> active-cell fraction
```

Different systems can behave very differently.

A rule may:

```text
die out
    -> density approaches 0

saturate
    -> density approaches 1

remain mixed
    -> density stays between the extremes

oscillate
    -> density changes periodically
```

But density alone does not tell us whether the cells are actually changing.

---

## Change rate

Two generations can have exactly the same density while containing active cells in completely different positions.

So measure temporal change directly:

```python
def change_rate(previous, current):
    return float(
        np.mean(previous != current)
    )
```

Across a run:

```python
def change_curve(history):
    return np.mean(
        history[1:] != history[:-1],
        axis=1,
    )
```

Now:

```text
change rate = 0
```

means the state is unchanged from the previous generation.

A fixed point has:

```text
density = constant
change  = 0
```

But an oscillator may have:

```text
density = constant
change  > 0
```

That distinction is exactly why we need more than one observable.

---

## Spatial transition rate

Temporal change tells us what happens between generations.

We can also measure structure **inside one generation**.

Count how often neighboring cells differ:

```python
def transition_rate(state):
    right = np.roll(state, -1)

    return float(
        np.mean(state != right)
    )
```

Compare:

```text
0000000011111111
```

with:

```text
0101010101010101
```

Both contain equal numbers of zeros and ones.

So both have:

```text
density = 0.5
```

But their spatial organization is completely different.

The first has only a few boundaries.

The second changes almost every cell.

Transition rate gives us a crude measure of local spatial fragmentation.

---

## The same system needs several views

Consider three questions:

```text
How much is active?
    -> density

How much changes over time?
    -> change rate

How rough is the spatial arrangement?
    -> transition rate
```

These are different properties.

That is the key lesson of this chapter.

![Density, temporal change and spatial transition rate for several elementary rules](/images/cellular-automata/ca17-measurement-comparison.png)

The figure compares several rules from the same initial-condition protocol.

No single curve tells the full story.

Together they begin to form a behavioral fingerprint.

---

## Summarize one run

We can combine basic measurements:

```python
def summarize(history):
    changes = change_curve(history)

    transitions = np.array([
        transition_rate(state)
        for state in history
    ])

    return {
        "final_density": float(
            density(history[-1])
        ),
        "mean_density": float(
            np.mean(history)
        ),
        "mean_change": float(
            np.mean(changes)
        ) if len(changes) else 0.0,
        "mean_transition_rate": float(
            np.mean(transitions)
        ),
        "final_transition_rate": float(
            transitions[-1]
        ),
    }
```

Now a trajectory has a compact numerical description.

But that description is only meaningful if we also know how the trajectory was generated.

---

## A measurement without experiment context is incomplete

Rule 30 started from a single active cell is not the same experiment as Rule 30 started from random noise.

Likewise:

```text
periodic boundaries
```

and:

```text
fixed boundaries
```

can produce different trajectories.

So a measurement record should include its experimental context.

For example:

```python
result = {
    "rule": 30,
    "width": 201,
    "generations": 200,
    "initial_condition": "single",
    "boundary": "periodic",
    "seed": None,
    "metrics": summarize(history),
}
```

For a stochastic run we might instead record:

```python
"seed": 42
```

The rule is:

> **Never separate a metric from the experiment that produced it.**

---

## Turn every rule into a record

Now evaluate all elementary cellular automata:

```python
records = []

for rule_number in range(256):
    history = run_rule(
        rule_number,
        width=201,
        generations=200,
    )

    records.append({
        "rule": rule_number,
        **summarize(history),
    })
```

We have transformed:

```text
256 images
```

into:

```text
256 structured records
```

Now we can sort:

```python
most_active = sorted(
    records,
    key=lambda row: row["mean_change"],
    reverse=True,
)
```

Filter:

```python
candidates = [
    row
    for row in records
    if 0.2 < row["mean_density"] < 0.8
    and row["mean_change"] > 0.1
]
```

Or plot rules in measurement space.

This is the beginning of automated exploration.

---

## Preserve trajectories and summaries separately

The summary is convenient.

The trajectory is evidence.

Do not throw away the complete history simply because you calculated a few metrics.

A useful experimental record has two levels:

```text
raw trajectory
      ↓
derived measurements
```

If a metric later turns out to be misleading, we can calculate a better one from the original run.

That is much harder if only the summary survived.

---

## One metric is never enough

A checkerboard has:

```text
high transition rate
```

but it is extremely regular.

Random noise can have:

```text
high entropy
```

without having persistent structure.

An oscillator can have:

```text
high temporal activity
```

while remaining perfectly predictable.

So we are not searching for:

> **the complexity number**

There probably is no single scalar that captures everything we care about.

Instead we are building a collection of observables:

```text
density
activity
spatial variation
entropy
periodicity
attractor structure
sensitivity
persistence
```

Different questions require different measurements.

---

## The measurement pipeline

We now have a new architecture:

```text
experiment configuration
        ↓
simulation
        ↓
trajectory
        ↓
measurements
        ↓
result record
```

The next stages will add:

```text
comparison
classification
search
selection
```

This changes the role of the cellular automaton.

It is no longer only something we render.

It becomes something we can **experiment on systematically**.

---

## One idea to keep

A measurement does not explain a cellular automaton.

It gives us another way to interrogate it.

The strongest workflow is:

```text
look
    ↓
measure
    ↓
compare
    ↓
form hypothesis
    ↓
run another experiment
```

In the next chapter we will focus on the first two observables — **activity and density** — and use them to distinguish frozen, saturated and persistently changing systems.
