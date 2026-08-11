+++
date = '2026-08-10T20:37:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 41: Train for Persistence'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata', 'Persistence']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 41: Train for Persistence

Growing a target once is not enough.

A useful self-organizing system should continue to satisfy its objective after it arrives.

That means the target should behave more like an **attractor** than a timestamped frame.

## The failure mode

Suppose training always evaluates at step 64.

The model can learn:

```text
seed
 ↓
grow
 ↓
target at step 64
 ↓
overshoot
 ↓
disintegrate
```

The loss never sees the failure after step 64.

So the model is not wrong according to the objective.

The objective is wrong according to us.

## Train over a time window

Instead of one terminal loss, evaluate multiple later states:

```python
def persistence_loss(model, initial, target, warmup=64, checks=8, interval=8):
    x = initial

    for _ in range(warmup):
        x = model(x)

    losses = []
    for _ in range(checks):
        for _ in range(interval):
            x = model(x)
        losses.append(F.mse_loss(x[:, :4], target))

    return torch.stack(losses).mean()
```

Now a transient match is not enough.

## Use a pool of states

Another powerful training pattern is to maintain states from previous rollouts.

```text
seed
partly grown state
nearly complete state
mature state
slightly degraded state
```

Sample from that pool, evolve for a random number of steps, compute loss, then put the resulting state back.

This exposes the rule to many positions along its own trajectory rather than restarting from the seed every time.

## Why a state pool changes the learning problem

Without a pool:

```text
learn seed -> target
```

With a pool:

```text
learn many nearby states -> target region
```

The latter encourages corrective dynamics.

If the state wanders slightly away from the desired morphology, the update rule has experience pushing it back.

## Measure persistence explicitly

Define a survival window:

```python
def persistence_curve(model, seed, target, total_steps=512):
    x = seed.clone()
    losses = []

    for step in range(total_steps):
        x = model(x)
        losses.append(float(F.mse_loss(x[:, :4], target)))

    return losses
```

Plot loss against time.

A persistent model should not merely hit one low point.

It should remain in a low-loss region for an extended interval.

## Persistence is dynamic maintenance

A mature organism-like pattern need not be frozen.

Hidden channels can continue changing while the visible structure remains approximately stable.

So persistence can mean:

```text
stable visible morphology
+
ongoing internal dynamics
```

That distinction is important. A fixed point is only one kind of attractor.

## What persists, exists

One of the most important lessons from the original Growing NCA experiments is that explicitly training systems to remain near their target can also improve their ability to recover from perturbations, even before strong damage training is introduced.

Further reading: [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/).

But incidental recovery is not enough.

If regeneration matters, damage needs to become part of the training distribution itself.

That is the next chapter.