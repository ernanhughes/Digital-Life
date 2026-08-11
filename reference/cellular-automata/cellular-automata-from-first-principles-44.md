+++
date = '2026-08-10T20:37:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 44: Neural Cellular Automata for Pathfinding'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Pathfinding', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 44: Neural Cellular Automata for Pathfinding

Until now our neural cellular automata have learned to **make and maintain shapes**.

Now we will ask them to compute something.

Given:

```text
walls
start
finish
```

can a shared local update rule discover a path?

This is an unusually good task for an NCA because classical pathfinding already has a local interpretation.

Breadth-first search expands a frontier:

```text
start
  ↓
nearby reachable cells
  ↓
next layer of reachable cells
  ↓
...
  ↓
goal
```

That looks remarkably like information propagating through a cellular system.

---

## Represent the maze as channels

Instead of one integer grid, keep semantics separate:

```text
channel 0 = wall mask
channel 1 = start mask
channel 2 = goal mask
channel 3 = predicted reachable field
channel 4 = predicted path field
channels 5+ = hidden state
```

In PyTorch:

```python
import torch

CHANNELS = 16


def make_state(walls, start, goal):
    h, w = walls.shape
    state = torch.zeros(1, CHANNELS, h, w)
    state[:, 0] = torch.as_tensor(walls, dtype=torch.float32)
    state[:, 1] = torch.as_tensor(start, dtype=torch.float32)
    state[:, 2] = torch.as_tensor(goal, dtype=torch.float32)
    return state
```

The first three channels are immutable problem inputs.

The other channels are working memory.

---

## Preserve the maze while updating state

Our learned rule should not rewrite the walls.

```python
def clamp_inputs(next_state, original_state):
    next_state[:, :3] = original_state[:, :3]
    return next_state
```

That gives the model a stable environment while its hidden channels evolve.

---

## A wavefront is already local computation

Classical BFS can be expressed as repeated local propagation.

Suppose `frontier` marks cells reached on the previous step.

```python
import torch.nn.functional as F

CROSS = torch.tensor(
    [[0.0, 1.0, 0.0],
     [1.0, 1.0, 1.0],
     [0.0, 1.0, 0.0]]
)[None, None]


def expand(frontier, blocked):
    neighbors = F.conv2d(frontier, CROSS, padding=1)
    reachable = (neighbors > 0).float()
    return reachable * (1.0 - blocked)
```

Repeated expansion spreads information one local neighborhood at a time.

An NCA does not need to invent locality.

It needs to learn what local information should propagate and how to store enough history to reconstruct a useful solution.

---

## Train on distance-to-goal first

Asking for a thin exact path immediately is difficult.

A smoother training target is a **distance field**.

For every reachable cell, precompute its shortest-path distance to the goal with BFS.

Normalize it:

```text
0.0 = goal
1.0 = farthest reachable cell
```

Then train one output channel to reproduce this field.

```python
def distance_loss(state, target_distance, reachable_mask):
    prediction = state[:, 3:4]
    error = (prediction - target_distance).pow(2)
    return (error * reachable_mask).sum() / reachable_mask.sum().clamp_min(1)
```

Why is this useful?

Because a shortest path can later be recovered by descending the distance field.

Instead of learning:

```text
which exact one-cell-wide route should I draw?
```

we first learn:

```text
how far is each location from the goal?
```

That is a more local, redundant representation.

---

## Roll out until information has time to travel

A maze cell cannot instantly know about a goal forty cells away.

With a radius-one neighborhood, information can move only a limited distance per update.

So training must respect the computational diameter of the problem.

```python
def rollout(model, state, steps, frozen_inputs):
    for _ in range(steps):
        state = model(state)
        state = clamp_inputs(state, frozen_inputs)
    return state
```

For a 32×32 maze we might sample:

```python
steps = torch.randint(32, 65, ()).item()
```

For larger mazes, allow longer rollouts.

This is not merely a training hyperparameter.

**Iteration count is computational depth.**

---

## Extract a path by local descent

Once a distance-like field exists, path extraction can be completely deterministic.

```python
def descend_path(distance, start, goal, walls):
    y, x = start
    path = [(y, x)]

    for _ in range(distance.size):
        if (y, x) == goal:
            break

        choices = []
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < distance.shape[0] and 0 <= nx < distance.shape[1]:
                if not walls[ny, nx]:
                    choices.append((distance[ny, nx], ny, nx))

        if not choices:
            break

        _, y, x = min(choices)
        path.append((y, x))

    return path
```

This deliberately separates:

```text
learn distributed value propagation
            ↓
use a simple deterministic decoder
```

We do not force the NCA to learn machinery that ordinary code already handles reliably.

---

## Compare against BFS

The baseline is not optional.

For every test maze record:

```text
BFS reachable?
BFS shortest distance
NCA reachable prediction
NCA extracted path length
NCA valid path?
NCA excess path length
```

A useful metric is:

```python
path_ratio = nca_path_length / bfs_path_length
```

with `1.0` meaning shortest-path performance.

Also measure outright failures separately.

A mean ratio that ignores unsolved mazes can be badly misleading.

---

## Why learn BFS-like computation at all?

For ordinary mazes, you should simply use BFS, Dijkstra or A*.

They are explicit, efficient and exact.

The purpose of this experiment is different.

We want to discover whether a **single shared local learned rule** can acquire an iterative algorithm whose computation scales across a grid.

That makes pathfinding a laboratory for:

```text
algorithmic learning
local communication
recurrent computation
generalization across spatial size
hidden-state analysis
```

---

## The critical test is not the training maze

A network can memorize distributions in subtle ways.

So the important experiment begins after training.

In the next chapter we will train on small mazes and evaluate on **larger, denser and structurally different mazes**.

That will tell us whether the NCA learned a transferable local procedure or merely adapted to the geometry of its training set.
