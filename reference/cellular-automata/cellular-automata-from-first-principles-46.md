+++
date = '2026-08-10T20:39:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 46: Generalize to Harder and Larger Mazes'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Generalization', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 46: Generalize to Harder and Larger Mazes

Training accuracy answers the easiest question:

```text
Can the model solve problems drawn from the training distribution?
```

The more interesting question is:

```text
Did the local rule learn a reusable computation?
```

This chapter turns that into an explicit evaluation protocol.

---

## Hold out dimensions of difficulty

Instead of one validation set, create several test families.

For example:

```text
A: 32×32, familiar wall density
B: 48×48, familiar wall density
C: 64×64, familiar wall density
D: 32×32, denser obstacles
E: 32×32, longer required paths
F: different procedural maze generator
G: narrow bottlenecks and many dead ends
```

The point is not to maximize one aggregate score.

The point is to identify **where the learned procedure breaks**.

---

## Scale rollout length with problem size

A local system cannot solve a larger maze in the same number of recurrent updates if information has farther to travel.

So separate two questions:

```text
Does the learned rule work on a larger maze?
Does it work with the same compute budget?
```

Those are not equivalent.

Evaluate both fixed and scaled rollout budgets:

```python
def rollout_budget(height, width, multiplier=2.0):
    return int(multiplier * max(height, width))
```

Then compare:

```text
64×64 with 64 steps
64×64 with 128 steps
64×64 with 256 steps
```

If longer recurrence restores performance, the rule may generalize while requiring more computational depth.

---

## Build a generalization matrix

A useful report is a table like:

```text
condition          solved   valid path   optimal   mean excess
32×32 familiar      0.98       0.97        0.91       0.08
48×48                ...        ...         ...        ...
64×64                ...        ...         ...        ...
dense                 ...        ...         ...        ...
new generator          ...        ...         ...        ...
```

Do not collapse this into one number too early.

The pattern of degradation is evidence.

---

## Test path length separately from grid size

A 64×64 open room may be easier than a 32×32 labyrinth.

So stratify examples by the optimal BFS path length:

```python
def path_length_bucket(length):
    if length < 16:
        return "short"
    if length < 32:
        return "medium"
    if length < 64:
        return "long"
    return "very-long"
```

Now we can distinguish spatial scale from computational horizon.

---

## Change the maze generator

Random occupancy grids can leave recognizable statistical fingerprints.

Train on one generator and test on another:

```text
training: random obstacle fields
held out: recursive backtracker mazes
held out: cellular-automata caves
held out: rooms connected by corridors
```

This is much stronger than merely changing the random seed.

If performance collapses, that is useful information.

The network may have learned useful local heuristics without learning a generator-independent shortest-path procedure.

---

## Evaluate impossible problems too

Some start/goal pairs are disconnected.

The model should not hallucinate a path through walls.

Track:

```text
true unreachable rate
predicted unreachable accuracy
false-path rate on disconnected mazes
```

A model that solves reachable examples beautifully but invents solutions for impossible ones is not a reliable pathfinder.

---

## Test update-rate robustness

Because the NCA uses randomized local firing, vary the update probability at evaluation:

```text
0.35
0.50
0.65
0.80
1.00
```

A model that only works at exactly the training fire rate has learned a fragile dynamical regime.

A broader stable region is stronger evidence of a robust local computation.

---

## Measure time to convergence

Instead of always running a fixed number of steps, watch the output stabilize.

```python
def stabilization_step(predictions, tolerance=1e-4, patience=5):
    stable = 0

    for i in range(1, len(predictions)):
        delta = (predictions[i] - predictions[i - 1]).abs().mean().item()

        if delta < tolerance:
            stable += 1
            if stable >= patience:
                return i
        else:
            stable = 0

    return None
```

Then ask whether larger mazes converge later in a roughly sensible way.

That reveals the temporal structure of the learned computation.

---

## Failure maps are more useful than anecdotes

For failed mazes, record characteristics:

```text
grid size
wall density
optimal path length
number of branches
number of dead ends
minimum corridor width
rollout steps
fire rate
```

Then look for clusters.

Maybe failures are concentrated in:

```text
long corridors
tight bottlenecks
loops
very long paths
new generator styles
```

That is a much better research workflow than collecting a few screenshots of failures.

---

## Generalization is graded, not binary

There is rarely one moment where we can declare:

```text
the NCA learned BFS
```

Evidence accumulates.

A stronger statement might be:

> the learned local rule retains high valid-path performance on larger grids when given proportionally more recurrent steps, but degrades on mazes generated by a different topology process.

That is more informative and more defensible.

---

## Now inspect the internal computation

Behavior tells us **that** the model works.

It does not tell us **how**.

The next chapter opens the hidden channels and tracks information propagation through space and time.
