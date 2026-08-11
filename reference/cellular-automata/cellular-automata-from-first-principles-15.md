+++
date = '2026-08-10T18:48:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 15: Grow Terrain from Local Height Rules'
categories = ['Programming', 'Procedural Generation']
tags = ['Cellular Automata', 'Python', 'Terrain Generation', 'Procedural Generation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 15: Grow Terrain from Local Height Rules

Binary caves ask:

```text
wall or floor?
```

Terrain needs richer state.

Let each cell store a height:

```text
0.0 = low
1.0 = high
```

Now local rules can smooth, raise, erode and classify terrain.

The challenge is not creating a pretty array.

It is creating a process whose output we can explain and control.

---

## Start with a height field

```python
import numpy as np


def random_heightmap(
    rows=120,
    cols=160,
    seed=42,
):
    rng = np.random.default_rng(seed)

    return rng.random(
        (rows, cols)
    )
```

Raw independent noise contains variation but little large-scale geography.

---

## Add a local mean

```python
def local_mean(grid):
    total = np.zeros_like(grid)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            total += np.roll(
                np.roll(
                    grid,
                    dy,
                    axis=0,
                ),
                dx,
                axis=1,
            )

    return total / 9.0
```

Blend toward the neighborhood:

```python
def smooth_step(
    height,
    strength=0.35,
):
    mean = local_mean(height)

    return (
        (1 - strength) * height
        + strength * mean
    )
```

Repeated smoothing creates broad spatial regions.

But smoothing alone is not a terrain generator.

If we continue forever, it removes differences.

---

## Add a competing process

Introduce persistent uplift:

```python
uplift = np.zeros_like(height)

uplift[
    30:92,
    55:108,
] = 0.003
```

Then:

```python
def terrain_step(
    height,
    uplift,
):
    height = smooth_step(
        height,
        strength=0.35,
    )

    height = height + uplift

    return np.clip(
        height,
        0.0,
        1.0,
    )
```

Now two local/global influences compete:

```text
smoothing
    -> reduces sharp local differences

uplift
    -> continually creates elevation
```

The renderer also applies a gentle radial edge falloff so the demonstration develops an island-like boundary.

![Evolution of the terrain field](/images/cellular-automata/ca15-terrain-evolution.png)

---

## Inspect the final height field directly

![Generated continuous terrain height field](/images/cellular-automata/ca15-terrain-heightmap.png)

This is important: the primary generated object is the **height field**.

Water, plains, hills and mountains are interpretations derived from it.

---

## Derive semantic terrain classes

```python
WATER = 0
PLAINS = 1
HILLS = 2
MOUNTAINS = 3


def classify_height(height):
    terrain = np.zeros_like(
        height,
        dtype=np.uint8,
    )

    terrain[
        (height >= 0.35)
        & (height < 0.55)
    ] = PLAINS

    terrain[
        (height >= 0.55)
        & (height < 0.75)
    ] = HILLS

    terrain[
        height >= 0.75
    ] = MOUNTAINS

    return terrain
```

This separates:

```text
simulation / generation state:
continuous height

game-facing interpretation:
terrain class
```

That separation keeps the underlying process reusable.

---

## Add a second continuous field

Height alone does not determine every world property.

Add moisture:

```python
moisture = np.zeros_like(height)

moisture[:, :20] = 1.0
```

Diffuse it inland:

```python
for _ in range(100):
    moisture = (
        moisture
        + 0.1 * laplacian(moisture)
    )

    moisture[:, :20] = 1.0
```

Now each cell can be thought of as:

```text
[height, moisture]
```

and biome classification can depend on both.

The grid is becoming a layered local state machine.

---

## Global design goals should remain explicit

A game may require:

```text
30-45% water
one large connected continent
flat spawn region
mountains away from spawn
river reaches ocean
```

Do not force a cellular smoothing rule to guarantee all of those.

Use:

```text
local rules
    -> organic structure

measurement
    -> evaluate candidate

graph/search constraints
    -> guarantee global requirements
```

This is the same lesson we learned from cave generation.

---

## Measure the world

```python
def terrain_stats(
    height,
    water_level=0.35,
):
    return {
        "mean_height": float(
            height.mean()
        ),
        "height_std": float(
            height.std()
        ),
        "water_fraction": float(
            np.mean(
                height < water_level
            )
        ),
        "mountain_fraction": float(
            np.mean(
                height > 0.75
            )
        ),
    }
```

Now seeds and parameter sets can be searched instead of judged only by screenshots.

---

## One idea to keep

Terrain generation becomes easier to reason about when we separate three layers:

```text
continuous generated fields
       ↓
derived semantic classes
       ↓
global design constraints
```

Local CA-style rules are excellent at producing spatial texture.

They do not need to carry every high-level requirement themselves.

In the next chapter we will use the same local machinery without pretending to simulate a world at all: we will deliberately treat cellular rules as visual texture generators.
