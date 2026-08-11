+++
date = '2026-08-10T20:39:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 43: Test Generalization Beyond Training'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata', 'Generalization']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 43: Test Generalization Beyond Training

A model can look robust while still depending on the exact conditions used during training.

So after growth, persistence and regeneration, we need a harder question:

> what happens when the world changes?

## Build a generalization matrix

Vary dimensions independently:

```text
canvas size
seed position
update rate
rollout length
damage geometry
damage severity
noise level
boundary conditions
```

Then evaluate combinations that were not used during training.

## Shift the seed

If training always starts at the centre, test elsewhere:

```python
def make_seed_at(y, x, size=96, channels=16):
    state = torch.zeros(1, channels, size, size, device=DEVICE)
    state[:, 3:, y, x] = 1.0
    return state
```

Because the rule is local and shared spatially, translation should be a natural capability when boundaries do not interfere. But we should measure it, not assume it.

## Change the canvas size

Train on `64×64` and evaluate on larger grids:

```python
seed = make_seed_at(48, 48, size=96)
```

If the target still develops correctly, that is evidence the system has not simply encoded one fixed array position.

## Inject state noise

```python
def add_noise(x, sigma=0.02):
    return x + sigma * torch.randn_like(x)
```

Test several noise levels and report performance curves rather than one anecdotal example.

## Change update rates

A model trained around a 50% firing rate may fail at 20% or 90%.

```python
rates = [0.2, 0.35, 0.5, 0.65, 0.8, 1.0]
```

This tests whether local coordination survives a different effective timescale.

## Hold out perturbations

If training uses circular wounds, evaluate rectangles and slices.

If training uses small wounds, evaluate larger ones.

This separates:

```text
robustness to familiar corruption
```

from:

```text
robustness to new corruption
```

## Report a table, not a victory image

For example:

```text
condition             final loss   recovery time   survived
-------------------------------------------------------------
centre seed           ...          ...             yes
shifted seed          ...          ...             yes
96x96 canvas          ...          ...             yes
20% fire rate         ...          ...             no
large slice damage    ...          ...             partial
noise sigma=0.05      ...          ...             yes
```

This is much more informative than selecting the best animation.

## Generalization has a boundary

A local learned rule may generalize impressively within one family of dynamics while failing abruptly outside it.

That boundary is scientifically interesting.

Do not hide it.

Map it.

## The next transition

We have now learned neural rules that can:

```text
grow
persist
repair
survive some distribution shift
```

But target morphogenesis is only one use for neural cellular automata.

The same architecture can perform **distributed computation over a grid**.

In the next chapters we will use NCA for pathfinding and maze-like reasoning, then inspect what the learned system is actually doing internally.

Further reading: [Pathfinding Neural Cellular Automata](https://arxiv.org/abs/2301.06820).