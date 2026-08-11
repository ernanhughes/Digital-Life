+++
date = '2026-08-10T18:54:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 21: Sensitivity to Initial Conditions'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Sensitivity', 'Chaos']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 21: Sensitivity to Initial Conditions

Change one cell.

Then run the same rule twice.

If the two futures remain almost identical, the rule is insensitive to that perturbation.

If the difference spreads, the rule amplifies local uncertainty.

That is one of the cleanest experiments we can perform on a cellular automaton.

---

## Create two nearby initial states

```python
import numpy as np

width = 201
base = np.zeros(width, dtype=np.uint8)
base[width // 2] = 1

perturbed = base.copy()
perturbed[width // 2 + 1] ^= 1
```

The two states differ by exactly one bit.

---

## Hamming distance

Measure the fraction of positions that differ:

```python
def hamming_fraction(a, b):
    return float(np.mean(a != b))
```

At time zero:

```python
hamming_fraction(base, perturbed)
# about 1 / 201
```

Now evolve both worlds with the same rule.

---

## Divergence curve

```python
def divergence_curve(history_a, history_b):
    return np.array([
        hamming_fraction(a, b)
        for a, b in zip(history_a, history_b)
    ])
```

Plot it over time.

Different rules produce very different shapes:

```text
perturbation disappears
perturbation stays localized
perturbation spreads linearly
perturbation rapidly contaminates much of the world
```

---

## The difference field

Instead of reducing everything to one number, visualize where the runs differ:

```python
difference = history_a ^ history_b
```

For binary states, XOR gives us a complete perturbation map.

This can reveal a causal cone spreading away from the changed cell.

---

## A spreading-speed estimate

Track the leftmost and rightmost differing cells:

```python
def difference_width(a, b):
    positions = np.flatnonzero(a != b)
    if len(positions) == 0:
        return 0
    return int(positions[-1] - positions[0] + 1)
```

Run this at each time step to estimate how quickly perturbations expand.

The neighborhood radius imposes a maximum propagation speed, so cellular automata make causal limits explicit.

---

## Repeat the experiment

One perturbation is not enough.

```python
def sensitivity_trials(rule_number, trials=50, width=201, generations=200):
    scores = []
    rng = np.random.default_rng(42)

    for _ in range(trials):
        base = rng.integers(0, 2, size=width, dtype=np.uint8)
        changed = base.copy()
        i = rng.integers(width)
        changed[i] ^= 1

        a = run_rule(rule_number, initial_state=base, generations=generations)
        b = run_rule(rule_number, initial_state=changed, generations=generations)

        scores.append(float(np.mean(a[-1] != b[-1])))

    return float(np.mean(scores))
```

Now sensitivity becomes a property we can estimate statistically.

---

## Sensitivity is not automatically useful

Extreme sensitivity can mean chaotic noise.

Very low sensitivity can mean a frozen system.

Again, the interesting regime may lie between extremes:

```text
perturbations matter
but structure survives
```

That is particularly relevant later when we study artificial-life systems that should respond to damage without dissolving into randomness.

---

## Robustness is the complementary question

Sensitivity asks:

> How much does a small change alter the future?

Robustness asks:

> Can the system recover or preserve useful structure despite a disturbance?

Those are related but not identical.

A neural cellular automaton that regrows after damage can be locally sensitive while globally robust.

We will return to that distinction later.

---

## Next: classification

We now measure:

- occupancy,
- activity,
- entropy,
- recurrence,
- and sensitivity.

The next question is whether these measurements can help organize rules into broad behavioral families instead of relying only on visual intuition.