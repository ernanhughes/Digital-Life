+++
date = '2026-08-10T18:53:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 20: Periodicity and Attractors'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Attractors', 'Cycles']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 20: Periodicity and Attractors

Many cellular automata eventually repeat.

A fixed point repeats every generation.

An oscillator repeats after several generations.

On a finite grid, deterministic cellular automata must eventually revisit a previous state because only finitely many states exist.

That makes cycle detection a fundamental measurement.

---

## Hash each state

For binary arrays we can store the bytes:

```python
def state_key(state):
    return state.tobytes()
```

Then track when each state first appeared:

```python
def find_cycle(history):
    seen = {}

    for t, state in enumerate(history):
        key = state_key(state)

        if key in seen:
            start = seen[key]
            return {
                "transient": start,
                "period": t - start,
                "repeat_at": t,
            }

        seen[key] = t

    return None
```

---

## Fixed points

A fixed point has period one:

```text
state(t+1) = state(t)
```

Detect it cheaply:

```python
def is_fixed(previous, current):
    return bool(np.array_equal(previous, current))
```

Examples include empty worlds and stable Life still lifes.

---

## Oscillators

A period-two oscillator satisfies:

```text
A -> B -> A -> B ...
```

But there is no reason to restrict ourselves to period two.

Cycle detection lets us discover arbitrary periods within our observation window.

---

## Transients matter too

Two rules may both settle into period-one states.

One may do so after three generations.

Another may spend thousands of generations generating structure before settling.

So record both:

```text
transient length
cycle period
```

The pair contains much more information than final state alone.

---

## Finite worlds can mislead us

A finite periodic grid guarantees eventual recurrence.

That does **not** imply the corresponding infinite cellular automaton is globally periodic.

Our measurements always belong to an experimental setup:

```text
rule + initial state + world size + boundary conditions
```

This is another reason to store experiment metadata alongside metrics.

---

## Detecting recurrence without storing everything

For long simulations, keeping every full state may be expensive.

One option is hashing:

```python
import hashlib


def digest_state(state):
    return hashlib.blake2b(state.tobytes(), digest_size=16).digest()
```

Store digests first and retain occasional checkpoints if you need exact reconstruction.

For very long runs, classic algorithms such as Floyd's tortoise-and-hare cycle detector can find cycles with constant memory, provided the transition function is deterministic.

---

## Attractor basins

Run the same rule from many random initial conditions:

```python
from collections import Counter

periods = Counter()

for seed in range(100):
    history = run_rule(90, seed=seed, initial="random")
    cycle = find_cycle(history)
    periods[cycle["period"] if cycle else None] += 1
```

Now we can ask whether many starting states converge to the same type of attractor.

This begins to reveal the structure of the rule's state space.

---

## A useful behavioral record

```python
def recurrence_metrics(history):
    cycle = find_cycle(history)

    if cycle is None:
        return {
            "cycle_found": False,
            "transient": None,
            "period": None,
        }

    return {
        "cycle_found": True,
        "transient": cycle["transient"],
        "period": cycle["period"],
    }
```

Combine this with density, activity and entropy.

We are gradually building a multi-dimensional description of behavior.

---

## Next: sensitivity

A rule can also be characterized by what happens when we change **one bit** of its initial state.

Do the two futures remain similar?

Or does the difference spread across the world?

That question leads us directly to sensitivity to initial conditions.