+++
date = '2026-08-10T18:42:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 12: Reaction-Diffusion and Pattern Formation'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Reaction Diffusion', 'Gray Scott']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 12: Reaction-Diffusion and Pattern Formation

Diffusion smooths differences.

Reaction can amplify them.

Put the two processes together and a nearly uniform field can develop persistent spots, stripes and fronts.

We will use a discrete Gray-Scott reaction-diffusion simulation because it gives us a compact bridge from local cellular updates to continuous pattern-forming dynamics.

Each lattice cell stores two values:

```text
U = concentration of chemical U
V = concentration of chemical V
```

So our cell state is now a vector:

```python
state[y, x] = [u, v]
```

---

## Initialize two fields

```python
import numpy as np

size = 128
rng = np.random.default_rng(42)

u = np.ones(
    (size, size),
    dtype=np.float64,
)

v = np.zeros(
    (size, size),
    dtype=np.float64,
)

u += rng.normal(
    0,
    0.002,
    u.shape,
)

v += rng.normal(
    0,
    0.002,
    v.shape,
)

r = 10
c = size // 2

u[c-r:c+r, c-r:c+r] = 0.50
v[c-r:c+r, c-r:c+r] = 0.25
```

The localized disturbance gives the dynamics a seed to amplify.

---

## Reuse the periodic Laplacian

```python
def laplacian(grid):
    return (
        np.roll(grid, 1, axis=0)
        + np.roll(grid, -1, axis=0)
        + np.roll(grid, 1, axis=1)
        + np.roll(grid, -1, axis=1)
        - 4 * grid
    )
```

Each chemical diffuses according to its own rate.

---

## Add local reaction terms

```python
def gray_scott_step(
    u,
    v,
    *,
    du=0.16,
    dv=0.08,
    feed=0.055,
    kill=0.062,
    dt=1.0,
):
    uvv = u * v * v

    delta_u = (
        du * laplacian(u)
        - uvv
        + feed * (1 - u)
    )

    delta_v = (
        dv * laplacian(v)
        + uvv
        - (feed + kill) * v
    )

    next_u = u + dt * delta_u
    next_v = v + dt * delta_v

    return next_u, next_v
```

Structurally this is still familiar:

```text
local state
+
local neighborhood
+
shared update
=
next local state
```

What changed is the mathematics inside the shared update.

---

## Run a controlled parameter comparison

A single attractive image tells us very little about the parameter space.

Instead, hold constant:

```text
initial field
random seed
diffusion rates
grid size
number of steps
```

and vary only:

```text
feed
kill
```

For example:

```python
parameter_sets = [
    (0.022, 0.051),
    (0.030, 0.055),
    (0.037, 0.060),
    (0.055, 0.062),
]
```

![Gray-Scott patterns from controlled feed/kill changes](/images/cellular-automata/ca12-reaction-diffusion-patterns.png)

The point is not merely that the pictures differ.

The point is that **small parameter changes move the same local dynamical system into different pattern regimes**.

---

## Keep numerical failure visible

Continuous-state simulations can fail numerically.

Check for invalid values:

```python
def validate_fields(u, v):
    assert np.isfinite(u).all()
    assert np.isfinite(v).all()
```

Do not silently clip `NaN` or exploding values and then continue as though the result were meaningful.

If an update becomes unstable, that is evidence about the discretization or parameter choice.

---

## Pattern formation comes from competition

There is no spot detector.

There is no stripe template.

No cell knows what the final image should look like.

The global structure emerges from competition among:

```text
diffusion
reaction
feed
removal
```

One mechanism spreads local differences.

Another locally creates or suppresses them.

Persistent structure can appear where those processes balance.

That is an important conceptual step toward continuous artificial-life systems later in the book.

---

## Perturb after the pattern forms

Once a stable-looking pattern appears, damage part of the field:

```python
v[45:75, 45:75] = 0.0
u[45:75, 45:75] = 1.0
```

Then continue.

Possible outcomes include:

```text
pattern reinvades
new structure forms
damage persists
global state reorganizes
```

Do not call this regeneration automatically.

At this point it is simply a perturbation-response experiment.

Later, when we train neural cellular automata specifically for recovery, we will define regeneration much more carefully.

---

## Measure more than the mean

Simple statistics:

```python
def field_stats(v):
    return {
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
    }
```

are useful sanity checks, but very different spatial patterns can share similar means and variances.

Later we will add spatial measurements:

```text
connected components
spatial frequency
entropy
persistence
autocorrelation
```

The image reveals structure.

The measurements let us compare it.

---

## Is Gray-Scott a cellular automaton?

Terminology varies.

A Gray-Scott lattice implementation can also be described as a finite-difference reaction-diffusion simulation or lattice dynamical system.

For this book the architectural continuity is what matters:

```text
discrete spatial lattice
local neighborhood operator
shared local update
repeated time steps
```

We are extending the same local-computation viewpoint rather than claiming that every lattice PDE discretization belongs to one strict historical CA definition.

---

## One idea to keep

Continuous fields do not remove emergence.

They give local rules more expressive state.

We now have cells that carry multiple interacting quantities and can create persistent spatial structure through local competition.

In the next chapter we will move from chemical fields to local populations and confront a new problem: what happens when multiple agents want to act on the same space?
