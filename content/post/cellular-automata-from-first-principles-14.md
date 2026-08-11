+++
date = '2026-08-10T18:46:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 14: Generate Caves from Noise'
categories = ['Programming', 'Procedural Generation']
tags = ['Cellular Automata', 'Python', 'Procedural Generation', 'Cave Generation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 14: Generate Caves from Noise

A cave generator can be built from a mechanism we already understand:

```text
random initial cells
       ↓
count nearby walls
       ↓
apply local smoothing rule
       ↓
repeat a few times
       ↓
stop and use the result
```

Unlike a forest-fire simulation, we are not trying to model an indefinitely evolving world.

Here the cellular automaton is a **construction process**.

---

## Represent wall and floor

```python
import numpy as np

FLOOR = 0
WALL = 1
```

Create a random map:

```python
def random_cave(
    rows=90,
    cols=140,
    wall_probability=0.45,
    seed=42,
):
    rng = np.random.default_rng(seed)

    grid = (
        rng.random((rows, cols))
        < wall_probability
    ).astype(np.uint8)

    return grid
```

At generation zero the image is only binary noise.

The structure comes from repeated local filtering.

---

## Count nearby walls with fixed boundaries

For game maps, wrapping the left edge onto the right edge is usually undesirable.

Use fixed boundaries rather than `np.roll` wraparound.

```python
def shift_fixed(
    a,
    dy,
    dx,
):
    out = np.zeros_like(a)

    # Copy the overlapping region only.
    ...

    return out
```

Then count the eight-cell Moore neighborhood:

```python
def wall_count(grid):
    count = np.zeros_like(
        grid,
        dtype=np.uint8,
    )

    walls = grid == WALL

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue

            count += shift_fixed(
                walls,
                dy,
                dx,
            )

    return count
```

---

## Apply a majority-like smoothing rule

```python
def cave_step(
    grid,
    threshold=5,
):
    nearby = wall_count(grid)

    next_grid = (
        nearby >= threshold
    ).astype(np.uint8)

    return solid_border(next_grid)
```

Run several generations.

![Cave structure emerging from random noise](/images/cellular-automata/ca14-cave-generation-stages.png)

The transformation is easy to understand:

```text
high-frequency isolated detail
       ↓
local majority-like smoothing
       ↓
larger contiguous wall/floor regions
```

---

## The parameter set defines a generator family

The main controls are:

```text
initial wall probability
neighbor threshold
number of smoothing steps
seed
```

That means there is no single "cave generator."

There is a parameterized family of generators.

A good workflow is:

```text
generate
measure
reject or retain
```

rather than manually editing bad outputs.

---

## Pretty does not mean playable

A cave can look organic and still fail every practical requirement.

Typical failures:

```text
most floor disconnected
spawn isolated
exit unreachable
tiny inaccessible pockets
too little floor
too much open space
```

So generation needs validation.

---

## Find connected floor regions

Use flood fill or breadth-first search over floor cells.

```python
from collections import deque


def reachable_floor(
    grid,
    start,
):
    rows, cols = grid.shape

    seen = np.zeros_like(
        grid,
        dtype=bool,
    )

    queue = deque([start])
    seen[start] = True

    while queue:
        y, x = queue.popleft()

        for dy, dx in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            ny = y + dy
            nx = x + dx

            if not (
                0 <= ny < rows
                and 0 <= nx < cols
            ):
                continue

            if (
                seen[ny, nx]
                or grid[ny, nx] == WALL
            ):
                continue

            seen[ny, nx] = True
            queue.append((ny, nx))

    return seen
```

Now connectivity becomes measurable.

---

## Combine local emergence with global constraints

One common cleanup strategy is to keep only the largest connected floor component.

![CA cave output before and after global connectivity filtering](/images/cellular-automata/ca14-cave-connectivity-comparison.png)

This illustrates an important procedural-generation principle:

```text
cellular automaton
    -> organic local geometry

graph algorithm
    -> explicit global guarantee
```

The CA does not need to solve every design constraint.

Use each algorithm where it is strongest.

---

## Build a cave score

Useful measurements include:

```text
floor fraction
largest connected floor fraction
number of floor components
boundary length
shortest path between endpoints
minimum local width
```

Then search seeds:

```python
for seed in range(10_000):
    cave = build_cave(seed)

    score = evaluate_cave(cave)

    if score >= threshold:
        keep(cave)
```

Now procedural generation becomes:

```text
generator
+
evaluator
+
search
```

That pattern will return repeatedly throughout the book.

---

## One idea to keep

The CA gives us local texture and organic geometry.

Global graph analysis gives us usability constraints.

Combining them is more powerful than asking one mechanism to do everything.

In the next chapter we will move from binary wall/floor cells to continuous height fields and build terrain from local smoothing, persistent uplift and layered state.
