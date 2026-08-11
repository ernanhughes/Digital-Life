+++
date = '2026-08-10T20:06:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 35: Flow-Lenia and Mass-Conserving Artificial Life'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Flow-Lenia', 'Lenia', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 35: Flow-Lenia and Mass-Conserving Artificial Life

Ordinary Lenia updates local state by adding growth:

```text
A(t + dt) = clip(A(t) + dt × G(U))
```

That means state can be created in one region and destroyed in another.

For many artificial-life experiments that is perfectly acceptable.

But it leaves a major question:

> What changes if local structure must reorganize **existing mass** instead of creating or deleting it?

Flow-Lenia explores exactly that direction.

---

## Why conservation changes the problem

Imagine a grid whose values represent material density.

In a non-conservative update:

```text
0.2 -> 0.7
```

can happen because the growth function says so.

In a conservative model, an increase here must be balanced by movement from somewhere else.

Conceptually:

```text
mass leaves neighboring cells
        ↓
flows through local transport
        ↓
arrives here
```

The total remains approximately constant:

```python
state.sum()
```

before and after the update.

---

## Start with a transport field

We can build a simple pedagogical mass-conserving model before attempting anything Flow-Lenia-specific.

Suppose every cell has a scalar density field:

```python
import numpy as np

state = np.zeros((128, 128), dtype=np.float64)
state[48:80, 48:80] = np.random.default_rng(42).random((32, 32))
```

Create a local potential:

```python
def potential(state, kernel_f):
    return np.fft.ifft2(
        np.fft.fft2(state) * kernel_f
    ).real
```

Now use differences in potential to define directional flow.

---

## A minimal conservative flow step

This is not a full Flow-Lenia implementation.

It is a small transport model that makes the conservation principle explicit.

```python
def conservative_flow_step(state, rate=0.1):
    next_state = state.copy()

    for axis in (0, 1):
        neighbor = np.roll(state, -1, axis=axis)
        gradient = state - neighbor

        flow = rate * gradient

        next_state -= flow
        next_state += np.roll(flow, 1, axis=axis)

    return np.clip(next_state, 0.0, None)
```

Check total mass:

```python
before = state.sum()
after_state = conservative_flow_step(state)
after = after_state.sum()

print(before, after, after - before)
```

Numerical details matter, but the intended invariant is clear:

```text
mass moved
mass was not invented
```

---

## Conservation gives us a testable invariant

We can write:

```python
def assert_mass_conserved(before, after, atol=1e-9):
    assert np.isclose(before.sum(), after.sum(), atol=atol)
```

This is stronger than merely looking at an animation.

A conserved quantity gives the simulation a hard correctness property.

---

## From growth field to flow field

In ordinary Lenia:

```text
local perception
      ↓
growth or decay
```

In a flow-based system we instead want something closer to:

```text
local perception
      ↓
preferred direction / transport tendency
      ↓
redistribute existing material
```

That is a much deeper change than replacing one equation with another.

The update semantics themselves have changed.

---

## Think of material as particles without particles

We still store a continuous density field.

But conceptually we can imagine each cell asking:

```text
where should my local mass move?
```

The grid remains Eulerian:

```text
fixed spatial cells
```

while state moves through it.

That gives us organism-like motion without needing to explicitly simulate millions of individual particles.

---

## Local parameters can become part of state

A second important Flow-Lenia idea is that rule parameters can be localized.

Instead of one world-wide parameter:

```python
mu = 0.15
```

we can imagine a field:

```python
mu = np.full((128, 128), 0.15)
```

Different regions can carry different local rule values.

Now an artificial organism can potentially carry aspects of its own update dynamics with it.

Conceptually:

```text
matter field
parameter field
      ↓
local dynamics
```

This creates the possibility of several locally coherent rule regimes coexisting in one world.

---

## A toy localized-parameter field

```python
mu = np.full(state.shape, 0.15)
mu[40:70, 40:70] = 0.12
mu[70:100, 70:100] = 0.20
```

A local response function can then use:

```python
def local_growth(u, mu_field, sigma=0.03):
    return 2.0 * np.exp(
        -((u - mu_field) ** 2) / (2 * sigma ** 2)
    ) - 1.0
```

Again, this is an explanatory stepping stone rather than a complete Flow-Lenia reproduction.

The important conceptual shift is that **rule identity no longer has to be globally fixed**.

---

## Multi-species becomes a systems question

If two structures carry different local parameters, then when they meet we must decide how parameter fields interact.

Possible mechanisms include:

```text
mix
compete
average
remain spatially separated
inherit during redistribution
```

Now the model can support questions closer to ecology and evolution:

```text
Can multiple persistent forms coexist?
Can one displace another?
Can local rule information spread?
Can new combinations appear?
```

---

## Measure evolutionary activity carefully

A changing picture is not necessarily evolution.

To make stronger claims we would want to track things such as:

```text
persistent lineages
heritable parameter differences
variation over time
selection-like differential persistence
novel stable forms
```

The exact definitions are research questions.

The important engineering lesson is familiar:

> instrument the phenomena you intend to claim.

---

## Reuse the experimental laboratory

Everything from Part III and the previous Lenia chapters still applies:

```text
mass
activity
localization
center of mass
compression
entropy
perturbation recovery
behavioral descriptors
novelty archives
```

Now we add conservative invariants:

```text
total mass drift
local transport magnitude
parameter-field diversity
```

---

## A conservation diagnostic

```python
def mass_drift(history):
    masses = np.asarray(history, dtype=float)
    return float(np.max(np.abs(masses - masses[0])))
```

During development:

```python
masses = []

for _ in range(1000):
    masses.append(state.sum())
    state = conservative_flow_step(state)

print("max drift:", mass_drift(masses))
```

A conservation claim should be checked every run, not assumed because the algorithm was intended to conserve mass.

---

## Lenia is now a family of design choices

We began with Conway:

```text
binary state
fixed neighborhood
hard rule
integer generations
```

Then moved toward Lenia:

```text
continuous state
smooth kernels
smooth growth
small time steps
```

And now toward Flow-Lenia:

```text
continuous density
local transport
mass conservation
localized rule parameters
```

Each transition changes what kinds of emergent organization the model can support.

---

## The next leap is different again

Every rule so far was designed by us.

Even when search selected parameters, the **form of the local update rule** remained hand-written.

What if we make the local update rule a neural network and train it from examples or objectives?

Then the cellular automaton becomes differentiable end-to-end:

```text
cell state
      ↓
local perception
      ↓
learned neural update
      ↓
next cell state
```

That is the bridge to **neural cellular automata**.

In Part V we will build that system from first principles, train patterns to grow from a seed, damage them, test regeneration, and investigate what it means for morphology itself to become learned behavior.