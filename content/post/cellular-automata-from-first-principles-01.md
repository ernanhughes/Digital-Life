+++
date = '2026-08-10T18:21:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 01: Build Your First Automaton'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'NumPy', 'Simulation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 01: Build Your First Automaton

In the previous chapter we reduced a cellular automaton to four things:

```text
space
state
neighborhood
rule
```

Now we are going to build one.

Not a framework.

Not a library.

One update step.

That is enough to expose the whole mechanism.

---

## Start with a one-dimensional world

Create a row of cells and turn on the centre cell:

```python
import numpy as np

width = 41
state = np.zeros(width, dtype=np.uint8)
state[width // 2] = 1

print(state)
```

Conceptually:

```text
....................#....................
```

We will use `0` for an empty cell and `1` for an active cell.

---

## Define one local rule

Suppose a cell becomes active when exactly one of the three cells in its neighborhood is active.

That is not yet a named elementary rule. It is simply a transition we can understand immediately.

```python
def local_rule(left, centre, right):
    return int(left + centre + right == 1)
```

Now apply it across the row:

```python
def step(state):
    next_state = np.zeros_like(state)

    for i in range(len(state)):
        left = state[(i - 1) % len(state)]
        centre = state[i]
        right = state[(i + 1) % len(state)]

        next_state[i] = local_rule(left, centre, right)

    return next_state
```

The modulo operator gives us periodic boundaries:

```text
left edge <----------------> right edge
```

The world wraps around like a ring.

---

## Run several generations

```python
def run(initial_state, generations):
    history = [initial_state.copy()]
    state = initial_state.copy()

    for _ in range(generations - 1):
        state = step(state)
        history.append(state.copy())

    return np.array(history)
```

Now:

```python
history = run(state, generations=25)
```

The result is a two-dimensional array:

```text
rows    = time
columns = space
```

This is one of the useful tricks of 1D cellular automata.

A one-dimensional system evolving through time naturally becomes a two-dimensional image.

---

## Visualize the history

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.imshow(history, cmap="binary", interpolation="nearest")
plt.xlabel("cell")
plt.ylabel("generation")
plt.show()
```

You have now built a cellular automaton.

The entire runtime is:

```text
for every generation:
    for every cell:
        read neighborhood
        apply rule
        write next state
```

---

## Why we need two states of the world

A common implementation mistake is to update the current row in place.

For example:

```python
for i in range(len(state)):
    state[i] = local_rule(...)
```

That changes the meaning of the simulation.

Cells later in the loop would observe already-updated neighbors while earlier cells observed old neighbors.

Instead we need:

```text
current generation
        |
        v
compute every update
        |
        v
next generation
```

Only after the whole generation has been calculated do we replace the current state.

This is synchronous updating.

Later we will deliberately experiment with asynchronous updates, but they should be a model choice rather than an accidental bug.

---

## Boundary conditions are part of the model

Our modulo indexing created periodic boundaries.

We could instead use fixed zeros:

```python
def get_cell(state, i):
    if i < 0 or i >= len(state):
        return 0
    return state[i]
```

Or reflective boundaries.

Or an effectively infinite sparse world.

These choices matter.

The update rule is not the entire model. The geometry and boundary behavior also determine what patterns are possible.

---

## Separate mechanism from rule

We can make the engine accept any rule function:

```python
def step(state, rule):
    next_state = np.zeros_like(state)

    for i in range(len(state)):
        neighborhood = (
            state[(i - 1) % len(state)],
            state[i],
            state[(i + 1) % len(state)],
        )
        next_state[i] = rule(*neighborhood)

    return next_state
```

Now the architecture is cleaner:

```text
simulation engine
      |
      +--> neighborhood lookup
      +--> time stepping
      +--> boundary behavior

rule
      |
      +--> local transition only
```

That separation will become useful as soon as we want to explore hundreds of rules.

---

## A compact text renderer

Before reaching for plots, it is useful to have a tiny text view:

```python
def render_row(state):
    return "".join("#" if cell else "." for cell in state)

state = np.zeros(41, dtype=np.uint8)
state[len(state) // 2] = 1

for _ in range(20):
    print(render_row(state))
    state = step(state, local_rule)
```

Text output is excellent for debugging because it removes the visualization stack from the problem.

If a rule behaves unexpectedly, we can inspect the exact cells.

---

## What we have built

Our automaton now has a reusable execution loop:

```python
current = initial

for generation in range(n):
    observe(current)
    current = step(current, rule)
```

That shape will survive almost the entire book.

Even when the state becomes a tensor with many channels and the rule becomes a neural network, the conceptual loop remains:

```text
observe local state
apply shared transition
advance time
```

In the next chapter we will replace our hand-written rule with a more powerful idea: encode the complete rule table as a single integer.

That gives us all **256 elementary cellular automata** for free.