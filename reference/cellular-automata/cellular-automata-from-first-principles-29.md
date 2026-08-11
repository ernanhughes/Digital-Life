+++
date = '2026-08-10T19:48:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 29: Growth Functions'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Growth Functions', 'Lenia', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 29: Growth Functions

We now have two pieces:

```text
continuous state
      ↓
weighted neighborhood
```

But a neighborhood value does not tell us what should happen next.

We need a response curve.

In Lenia-style systems that curve is usually called a **growth function**.

It converts neighborhood potential into local growth or decay.

---

## A Gaussian-shaped preference

A useful starting point is:

```python
import numpy as np


def gaussian_growth(u, mu=0.15, sigma=0.03):
    return 2.0 * np.exp(
        -((u - mu) ** 2) / (2 * sigma ** 2)
    ) - 1.0
```

The output is approximately:

```text
-1   strong decay
 0   neutral
+1   strong growth
```

Plot it:

```python
import matplotlib.pyplot as plt

u = np.linspace(0.0, 0.4, 500)
g = gaussian_growth(u)

plt.plot(u, g)
plt.axhline(0.0, linewidth=1)
plt.xlabel("neighborhood potential")
plt.ylabel("growth")
plt.show()
```

The rule prefers a particular local density around `mu`.

Too little activity decays.

Too much activity also decays.

Only a band around the preferred neighborhood produces positive growth.

---

## Why this can create boundaries

Imagine a blob of active cells.

Inside the blob:

```text
neighborhood potential may be too high
→ decay
```

Far outside:

```text
neighborhood potential is too low
→ decay
```

Near a certain boundary region:

```text
neighborhood potential is just right
→ growth
```

That creates a feedback mechanism capable of maintaining spatial structure.

The rule does not explicitly say:

> Make an organism-shaped boundary.

It only rewards a certain local field value.

---

## Growth is not next state

This distinction matters:

```python
growth = gaussian_growth(neighborhood)
```

is not the next state.

We integrate it:

```python
def integrate(state, growth, dt=0.1):
    return np.clip(state + dt * growth, 0.0, 1.0)
```

So the full step becomes:

```python
def lenia_like_step(state, kernel, dt=0.1, mu=0.15, sigma=0.03):
    neighborhood = fft_convolve(state, kernel)
    growth = gaussian_growth(neighborhood, mu=mu, sigma=sigma)
    return np.clip(state + dt * growth, 0.0, 1.0)
```

---

## Parameters now have clear meanings

We can interpret each parameter:

```text
mu      preferred neighborhood density
sigma   tolerance around that preference
dt      speed of change
kernel  spatial scale of perception
```

This is much better than hiding everything inside a single opaque update function.

---

## Narrow versus broad growth

Try:

```python
for sigma in [0.01, 0.03, 0.08]:
    plt.plot(u, gaussian_growth(u, mu=0.15, sigma=sigma), label=str(sigma))

plt.legend(title="sigma")
plt.show()
```

A narrow function is selective.

A broad function tolerates many neighborhood values.

That can radically change the stability of patterns.

---

## Growth fields are worth visualizing

During debugging, show all three layers:

```python
state
neighborhood
local growth
```

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(state, cmap="viridis")
axes[1].imshow(neighborhood, cmap="magma")
axes[2].imshow(growth, cmap="coolwarm", vmin=-1, vmax=1)
plt.show()
```

A pattern that mysteriously dies becomes much easier to explain when you can see that almost every cell is receiving negative growth.

---

## Growth and decay balance

A localized pattern survives only if growth and decay balance over time.

Track total mass:

```python
masses = []

for _ in range(500):
    masses.append(state.sum())
    state = lenia_like_step(state, kernel)
```

Possible outcomes:

```text
mass -> 0
pattern dies

mass -> grid maximum
pattern floods world

mass oscillates in bounded range
persistent dynamics
```

Persistence does not require exact mass conservation.

It requires long-term balance between local creation and removal.

Later Flow-Lenia will deliberately change this assumption.

---

## Growth curves can be different shapes

A Gaussian is convenient, not mandatory.

For example:

```python
def triangular_growth(u, center=0.15, width=0.05):
    score = 1.0 - np.abs(u - center) / width
    return np.clip(2 * score - 1, -1, 1)
```

Or a smooth polynomial bump.

Different response families create different dynamical systems.

---

## Inspect local causality

Pick one cell:

```python
y, x = 64, 64

print("state:", state[y, x])
print("neighborhood:", neighborhood[y, x])
print("growth:", growth[y, x])
```

This gives a local causal chain:

```text
surrounding state
      ↓
weighted perception
      ↓
growth response
      ↓
state increment
```

Even when the global pattern becomes astonishingly complex, the local mechanism remains inspectable.

---

## We now have almost all of Lenia's skeleton

At the highest level:

```text
A(t)
  ↓ convolution K
U(t)
  ↓ growth G
G(U)
  ↓ small integration step
A(t + dt)
```

The next chapter will put those components together into a reusable implementation.

We will not begin by copying a mysterious Lenia codebase.

We will build **Lenia from first principles**, component by component, using the machinery we already understand.