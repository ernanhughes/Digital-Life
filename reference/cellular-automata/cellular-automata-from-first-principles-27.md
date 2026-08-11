+++
date = '2026-08-10T19:43:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 27: From Discrete Cells to Continuous State'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Continuous Cellular Automata', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 27: From Discrete Cells to Continuous State

So far most of our cellular automata have used a small set of states:

```text
0 or 1
empty / prey / predator
ready / firing / refractory
```

That makes rules easy to inspect.

But it also forces every update to make a hard categorical decision.

What happens if a cell can instead hold **any value between 0 and 1**?

```text
0.0 -------------------------- 1.0
```

Now a cell can represent intensity, density, concentration, activation or some abstract amount of local material.

This single change opens the door to continuous cellular automata and, eventually, Lenia.

---

## A continuous state grid

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
state = rng.random((128, 128))
```

Every cell now contains a floating-point value:

```python
print(state.min(), state.max())
```

The state space is no longer:

```text
{0, 1}
```

but approximately:

```text
[0, 1]
```

That means the transition rule can change a cell by a small amount rather than replacing one symbol with another.

---

## Replace decisions with growth

A binary cellular automaton often computes:

```text
neighborhood -> next state
```

A continuous automaton can instead compute:

```text
neighborhood -> growth rate
```

Then:

```text
next state = current state + small growth
```

In code:

```python
def update(state, growth, dt=0.1):
    return np.clip(state + dt * growth, 0.0, 1.0)
```

The `dt` parameter matters.

It controls how much simulated time passes during one numerical step.

---

## A tiny continuous automaton

Let's use the local mean as our neighborhood signal:

```python
def local_mean(state):
    total = np.zeros_like(state)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            total += np.roll(np.roll(state, dy, axis=0), dx, axis=1)

    return total / 9.0
```

Now define a growth rule that prefers neighborhood values near `0.5`:

```python
def growth_function(u, target=0.5, width=0.15):
    return 2.0 * np.exp(-((u - target) ** 2) / (2 * width ** 2)) - 1.0
```

And one step:

```python
def step(state, dt=0.1):
    neighborhood = local_mean(state)
    growth = growth_function(neighborhood)
    return np.clip(state + dt * growth, 0.0, 1.0)
```

Run it:

```python
state = rng.random((128, 128)) * 0.3

for _ in range(200):
    state = step(state)

plt.imshow(state, cmap="viridis")
plt.axis("off")
plt.show()
```

This is deliberately crude.

But structurally it already contains the central ingredients we need later:

```text
continuous cell state
      ↓
continuous neighborhood signal
      ↓
continuous growth response
      ↓
small time update
```

---

## Why `np.clip` appears everywhere

Without a constraint, repeated growth could push values below zero or above one.

If the model defines state as bounded density, we enforce that explicitly:

```python
state = np.clip(state, 0.0, 1.0)
```

This is not merely a numerical trick.

It is part of the model semantics.

A bounded activation field is different from an unbounded concentration field.

---

## Discrete time versus smooth time

Conway's Life jumps:

```text
generation 0
    ↓
generation 1
    ↓
generation 2
```

With a small `dt`, our new system changes more gradually:

```text
t
↓
t + 0.1
↓
t + 0.2
```

We are still simulating in discrete computer steps.

But the rule is designed so those steps approximate smoother temporal evolution.

That distinction will matter when we tune the system.

A rule that behaves well with:

```python
dt = 0.1
```

may become unstable with:

```python
dt = 1.0
```

---

## Measure continuous state differently

Population count no longer makes much sense.

Instead measure total mass:

```python
def mass(state):
    return float(state.sum())
```

Mean activation:

```python
def mean_state(state):
    return float(state.mean())
```

Variance:

```python
def state_variance(state):
    return float(state.var())
```

And change per step:

```python
def mean_change(before, after):
    return float(np.mean(np.abs(after - before)))
```

Part III becomes immediately useful again.

We already know how to treat dynamics as data.

---

## Seed localized structure

Artificial-life systems are often easier to inspect when the initial state is localized:

```python
state = np.zeros((128, 128), dtype=np.float64)
state[48:80, 48:80] = rng.random((32, 32))
```

Now we can ask:

```text
does the pattern vanish?
does it explode?
does it stabilize?
does it move?
does it fragment?
```

These are exactly the behavioral questions we prepared for in the previous section.

---

## The important abstraction

The most useful way to think about this chapter is not:

> We replaced integers with floats.

The deeper shift is:

```text
old CA
local configuration -> categorical replacement

continuous CA
local field -> rate of change
```

That gives us much finer control over how local influence accumulates.

---

## But our neighborhood is still primitive

A 3x3 mean treats all nearby cells almost identically.

Artificial-life systems often need richer spatial structure.

We may want:

```text
close cells     -> strong influence
middle ring     -> strongest influence
far cells       -> weak influence
outside radius  -> no influence
```

Writing that manually as dozens or hundreds of coordinate checks would be ugly and slow.

Fortunately, we already have the right mathematical tool.

In the next chapter we will replace hand-coded neighborhood loops with **convolution kernels** and turn the neighborhood itself into a configurable spatial function.