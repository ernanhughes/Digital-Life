+++
date = '2026-08-10T19:51:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 30: Build Lenia From First Principles'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Lenia', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 30: Build Lenia From First Principles

We now have every conceptual component needed for a minimal Lenia implementation:

```text
continuous state
radial kernel
convolution
smooth growth function
small time step
bounded update
```

This chapter assembles them into one runnable system.

---

## Represent the model parameters explicitly

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class LeniaConfig:
    radius: int = 13
    ring_center: float = 0.5
    ring_width: float = 0.15
    mu: float = 0.15
    sigma: float = 0.03
    dt: float = 0.1
```

Keeping parameters in one object makes experiments reproducible.

---

## Build the kernel

```python
import numpy as np


def build_kernel(config: LeniaConfig):
    r = config.radius
    y, x = np.mgrid[-r:r+1, -r:r+1]
    distance = np.sqrt(x*x + y*y) / r

    kernel = np.exp(
        -((distance - config.ring_center) ** 2)
        / (2 * config.ring_width ** 2)
    )

    kernel[distance > 1.0] = 0.0
    kernel[distance == 0.0] = 0.0
    kernel /= kernel.sum()
    return kernel
```

---

## Precompute the frequency-domain kernel

```python
def kernel_fft(kernel, shape):
    padded = np.zeros(shape, dtype=np.float64)
    kh, kw = kernel.shape
    padded[:kh, :kw] = kernel
    padded = np.roll(padded, -(kh // 2), axis=0)
    padded = np.roll(padded, -(kw // 2), axis=1)
    return np.fft.fft2(padded)
```

We only need to transform the kernel once while its parameters stay fixed.

---

## Growth function

```python
def growth(u, mu, sigma):
    return 2.0 * np.exp(
        -((u - mu) ** 2) / (2 * sigma ** 2)
    ) - 1.0
```

---

## The complete step

```python
def lenia_step(state, kernel_f, config):
    potential = np.fft.ifft2(
        np.fft.fft2(state) * kernel_f
    ).real

    delta = growth(potential, config.mu, config.sigma)

    next_state = state + config.dt * delta
    return np.clip(next_state, 0.0, 1.0)
```

That is the core engine.

The remarkable thing is how small it is.

---

## Seed a localized pattern

```python
def random_seed(shape=(128, 128), patch=24, seed=42):
    rng = np.random.default_rng(seed)
    state = np.zeros(shape, dtype=np.float64)

    y0 = shape[0] // 2 - patch // 2
    x0 = shape[1] // 2 - patch // 2
    state[y0:y0+patch, x0:x0+patch] = rng.random((patch, patch))

    return state
```

Run the model:

```python
config = LeniaConfig()
kernel = build_kernel(config)
kernel_f = kernel_fft(kernel, (128, 128))
state = random_seed()

for _ in range(500):
    state = lenia_step(state, kernel_f, config)
```

Visualize:

```python
import matplotlib.pyplot as plt

plt.imshow(state, cmap="viridis", vmin=0, vmax=1)
plt.axis("off")
plt.show()
```

---

## Most seeds will not become organisms

This is important.

Possible outcomes include:

```text
dies out
explodes
becomes uniform
oscillates chaotically
forms transient blobs
settles into localized structure
```

Interesting life-like patterns occupy restricted regions of both initial-condition space and parameter space.

That turns discovery into a search problem.

---

## Instrument the run

```python
def run(state, kernel_f, config, steps=500):
    history = []

    for step_index in range(steps):
        before = state
        state = lenia_step(state, kernel_f, config)

        history.append({
            "step": step_index,
            "mass": float(state.sum()),
            "mean": float(state.mean()),
            "activity": float(np.mean(np.abs(state - before))),
        })

    return state, history
```

The metrics from Part III now plug directly into the artificial-life engine.

---

## Detect localization

One useful first test is whether most activity remains concentrated in a small region.

```python
def active_fraction(state, threshold=0.05):
    return float(np.mean(state > threshold))
```

A world-filling soup might have:

```text
active_fraction ≈ 1
```

while a localized creature-like pattern may occupy only a small fraction of the board.

No single threshold proves an organism exists, but it gives search infrastructure something to work with.

---

## Detect motion with a center of mass

```python
def center_of_mass(state):
    total = state.sum()
    if total <= 1e-12:
        return None

    y, x = np.indices(state.shape)
    return (
        float((y * state).sum() / total),
        float((x * state).sum() / total),
    )
```

Compare positions over time.

A persistent localized pattern whose center moves may be behaving like a mobile artificial organism.

Periodic boundaries make center-of-mass tracking near edges trickier, so production analysis should unwrap trajectories or keep organisms away from boundaries during evaluation.

---

## Save a parameterized experiment

A Lenia result without its parameters is barely reproducible.

Store at least:

```text
config
initial seed
board dimensions
step count
metric history
final state
```

For example:

```python
np.savez_compressed(
    "lenia_run.npz",
    initial=initial_state,
    final=state,
    kernel=kernel,
)
```

Store the config separately as JSON or structured metadata.

---

## From automaton to laboratory

Notice how far we have come from Rule 30.

The architecture is still recognizable:

```text
state
  ↓
local perception
  ↓
transition rule
  ↓
next state
```

But every component has become continuous and parameterized.

This is exactly why the first-principles route matters.

Lenia no longer looks like magic.

It looks like a sequence of understandable design choices.

---

## The hard part starts now

We can run Lenia.

That is not the same as discovering interesting life.

The next challenge is experimental:

```text
Which seeds survive?
Which parameter settings create localized structure?
Which patterns move?
Which regenerate?
Which are genuinely different rather than tiny variations?
```

In the next chapter we will turn Lenia into a **discovery system** and begin searching for persistent artificial organisms instead of manually guessing parameters forever.