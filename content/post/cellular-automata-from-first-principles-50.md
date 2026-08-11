+++
date = '2026-08-10T20:53:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 50: Vectorize the Update Loop'
categories = ['Programming', 'Performance']
tags = ['Cellular Automata', 'Python', 'NumPy', 'Vectorization']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 50: Vectorize the Update Loop

A cellular automaton is local.

That does **not** mean we should update it cell by cell in Python.

For dense grids, the same local rule is applied everywhere. That regularity is exactly what array programming is good at.

---

## Start with the obvious implementation

```python
def life_step_slow(grid):
    height, width = grid.shape
    next_grid = np.zeros_like(grid)

    for y in range(height):
        for x in range(width):
            total = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    total += grid[(y + dy) % height, (x + dx) % width]

            alive = grid[y, x] == 1
            next_grid[y, x] = (
                total == 3 or (alive and total == 2)
            )

    return next_grid
```

This is useful because it states the mechanism clearly.

It is also expensive because Python interprets every nested loop.

---

## Express the neighborhood as array operations

```python
def life_neighbors(grid):
    total = np.zeros_like(grid, dtype=np.int16)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            total += np.roll(np.roll(grid, dy, axis=0), dx, axis=1)

    return total
```

The two tiny Python loops now iterate over **eight directions**, not millions of cells.

Then the rule becomes boolean array logic:

```python
def life_step(grid):
    n = life_neighbors(grid)
    return ((n == 3) | ((grid == 1) & (n == 2))).astype(np.uint8)
```

---

## Vectorize 1D elementary automata

```python
def elementary_step(state, rule):
    left = np.roll(state, 1)
    right = np.roll(state, -1)

    index = (left << 2) | (state << 1) | right
    bits = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)

    return bits[index]
```

No per-cell Python loop is required.

---

## Be aware of temporary arrays

Vectorized code can be faster while allocating more memory.

This expression:

```python
np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
```

creates temporaries.

For moderate grids that may be fine.

For very large grids or many channels, allocation can become the bottleneck.

Optimization is always workload-dependent.

---

## Use slices when the boundary allows it

If we do not need periodic boundaries, explicit slices can avoid some rolling:

```python
center = grid[1:-1, 1:-1]

neighbors = (
    grid[:-2, :-2] + grid[:-2, 1:-1] + grid[:-2, 2:] +
    grid[1:-1, :-2]                    + grid[1:-1, 2:] +
    grid[2:, :-2]  + grid[2:, 1:-1]  + grid[2:, 2:]
)
```

The important point is not that slices are universally superior.

It is that **boundary semantics and performance strategy interact**.

---

## Batch independent worlds

Suppose we want to evaluate 1,000 rules or seeds.

Instead of:

```python
for world in worlds:
    run(world)
```

we can add a batch axis:

```text
(batch, height, width)
```

and update many independent worlds in one array operation.

That matters enormously for parameter sweeps and training workloads.

---

## Check equivalence

```python
rng = np.random.default_rng(42)
state = rng.integers(0, 2, size=(64, 64), dtype=np.uint8)

slow = life_step_slow(state)
fast = life_step(state)

assert np.array_equal(slow, fast)
```

Optimization should be tested against the simplest correct implementation.

---

## The larger lesson

Cellular automata have an unusually regular computational structure:

```text
same neighborhood operation
same rule
many cells
many steps
```

That makes them natural candidates for vectorization.

The same structure also makes them natural candidates for GPUs, which is where we go next.