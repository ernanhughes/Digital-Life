+++
date = '2026-08-10T20:38:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 45: Learn to Solve Mazes'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Mazes', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 45: Learn to Solve Mazes

A pathfinding NCA becomes interesting only when the training problem itself is disciplined.

If every maze has the same size, wall density and corridor style, the model may learn the dataset more than the algorithm.

So this chapter builds the training system around **procedural variation**.

---

## Generate mazes as data

Start with binary occupancy:

```text
0 = open
1 = wall
```

One simple generator begins with random walls and rejects disconnected examples.

```python
import numpy as np


def random_grid(size=32, wall_probability=0.28, seed=None):
    rng = np.random.default_rng(seed)
    grid = (rng.random((size, size)) < wall_probability).astype(np.uint8)

    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1

    return grid
```

This is not necessarily a beautiful human-style maze.

That is useful.

We want many local obstacle arrangements, not one generator's aesthetic signature.

---

## Sample start and goal positions

```python
def sample_open_cell(grid, rng):
    open_cells = np.argwhere(grid == 0)
    return tuple(open_cells[rng.integers(len(open_cells))])
```

Then choose start and goal far enough apart that the problem requires propagation.

```python
def sample_problem(grid, rng, minimum_manhattan=12):
    for _ in range(1000):
        start = sample_open_cell(grid, rng)
        goal = sample_open_cell(grid, rng)

        distance = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        if distance >= minimum_manhattan:
            return start, goal

    raise RuntimeError("could not sample distant start/goal")
```

---

## Use BFS as the teacher

We do not need human labels.

A classical algorithm can produce exact supervision.

```python
from collections import deque


def bfs_distance(grid, goal):
    distance = np.full(grid.shape, np.inf, dtype=np.float32)
    queue = deque([goal])
    distance[goal] = 0.0

    while queue:
        y, x = queue.popleft()

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx

            if not (0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1]):
                continue
            if grid[ny, nx] == 1:
                continue
            if np.isfinite(distance[ny, nx]):
                continue

            distance[ny, nx] = distance[y, x] + 1
            queue.append((ny, nx))

    return distance
```

This gives us a perfect target distance field for every reachable cell.

---

## Normalize without destroying semantics

Raw distances vary with maze size.

Normalize reachable values:

```python
def normalize_distance(distance):
    reachable = np.isfinite(distance)
    out = np.ones_like(distance, dtype=np.float32)

    if reachable.any():
        maximum = distance[reachable].max()
        if maximum > 0:
            out[reachable] = distance[reachable] / maximum
        else:
            out[reachable] = 0.0

    return out, reachable.astype(np.float32)
```

Keep the reachable mask separately.

Do not turn unreachable cells into ordinary high-distance targets and pretend the distinction disappeared.

---

## Train on batches of different mazes

```python
def training_step(model, batch, optimizer):
    optimizer.zero_grad()

    losses = []

    for state, target, mask, steps in batch:
        frozen = state.clone()

        for _ in range(steps):
            state = model(state)
            state[:, :3] = frozen[:, :3]

        prediction = state[:, 3:4]
        error = (prediction - target).pow(2)
        loss = (error * mask).sum() / mask.sum().clamp_min(1)
        losses.append(loss)

    loss = torch.stack(losses).mean()
    loss.backward()
    optimizer.step()

    return float(loss)
```

Sampling a different rollout length per problem discourages dependence on one exact stopping time.

---

## Curriculum can help

A useful curriculum is:

```text
stage 1: sparse obstacles
stage 2: moderate obstacle density
stage 3: longer routes
stage 4: dead ends and bottlenecks
stage 5: mixed generators
```

This does not mean the model must always be trained this way.

It means we can control task difficulty instead of treating failed optimization as mysterious.

---

## Measure more than pixel loss

A low distance-field MSE is not the actual application objective.

Evaluate:

```text
reachable classification accuracy
valid-path rate
shortest-path rate
mean excess path length
failure rate
steps required before solution stabilizes
```

For example:

```python
def excess_length(found, optimal):
    if found is None:
        return np.inf
    return len(found) - optimal
```

Then report solved and unsolved cases separately.

---

## Watch computation unfold

Save the predicted distance field at intermediate steps:

```python
snapshots = []

for step in range(64):
    state = model(state)

    if step in {0, 1, 2, 4, 8, 16, 32, 63}:
        snapshots.append(state[:, 3:4].detach().cpu())
```

This will later become one of the best visualizations in the book.

You should see information spreading through corridors rather than the final answer appearing all at once.

---

## A maze is a test of distributed memory

Dead ends reveal why hidden state matters.

A cell may need to distinguish:

```text
unvisited
frontier just arrived
visited earlier
reachable but not useful for final route
```

Those concepts do not all have to be explicit output channels.

The model can encode them in hidden state.

That makes maze solving a better probe of NCA computation than simple image growth.

---

## But solving familiar mazes is still not enough

Suppose training uses only 32×32 grids with 28% random walls.

A good validation score there tells us almost nothing about algorithmic generalization.

The next chapter deliberately changes the problem:

```text
larger grids
longer paths
higher wall density
new maze generators
more dead ends
narrower bottlenecks
```

If performance survives, we have stronger evidence that the NCA learned a reusable iterative computation.
