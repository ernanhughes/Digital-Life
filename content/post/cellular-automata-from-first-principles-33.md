+++
date = '2026-08-10T20:00:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 33: Multi-Kernel and Multi-Channel Lenia'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Lenia', 'Multi Channel', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 33: Multi-Kernel and Multi-Channel Lenia

Our Lenia implementation has one scalar field:

```text
A(x, y)
```

and one kernel:

```text
K
```

That is enough for rich behavior.

But it also forces every local process to share the same spatial scale and the same state variable.

A richer model can use multiple channels:

```text
A0(x, y)
A1(x, y)
A2(x, y)
```

and multiple kernels linking them.

---

## Represent state as channels

```python
import numpy as np

channels = 3
state = np.zeros((channels, 128, 128), dtype=np.float64)
```

Now each cell has a vector state:

```text
[cell_0, cell_1, cell_2]
```

The channels do not need literal biological meanings.

They are interacting local fields.

---

## A connection describes influence

We can describe one interaction as:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Connection:
    source: int
    target: int
    kernel: np.ndarray
    mu: float
    sigma: float
    weight: float = 1.0
```

This says:

```text
read source channel
      ↓
apply this spatial kernel
      ↓
apply this growth response
      ↓
add weighted change to target channel
```

That is a small local network.

---

## Compute several influences

```python
def multi_channel_step(state, connections, dt=0.1):
    delta = np.zeros_like(state)

    for connection in connections:
        kernel_f = kernel_fft(connection.kernel, state.shape[1:])

        potential = np.fft.ifft2(
            np.fft.fft2(state[connection.source]) * kernel_f
        ).real

        response = growth(
            potential,
            connection.mu,
            connection.sigma,
        )

        delta[connection.target] += connection.weight * response

    return np.clip(state + dt * delta, 0.0, 1.0)
```

For repeated simulation we should precompute each kernel FFT rather than rebuilding it every step.

---

## Cross-channel interaction

Suppose:

```text
channel 0 encourages channel 1
channel 1 suppresses channel 0
```

We can express that with two connections.

The result can create feedback loops:

```text
A grows B
B suppresses A
A falls
B loses support
B falls
A can recover
```

Local feedback creates temporal structure as well as spatial structure.

---

## Multiple spatial scales

Different kernels can operate at different radii:

```text
short-range excitation
long-range inhibition
```

This is a recurring pattern in self-organizing systems.

For example:

```python
short_kernel = ring_kernel(radius=8, ring_center=0.4, ring_width=0.12)
long_kernel = ring_kernel(radius=20, ring_center=0.6, ring_width=0.18)
```

Now a cell can respond differently to nearby and distant activity.

---

## Think in terms of a graph

With several channels and connections, the rule can be visualized as a graph:

```text
channel 0 ──K0──▶ channel 0
    │
    └──K1──▶ channel 1

channel 1 ──K2──▶ channel 0
```

Each edge carries:

```text
kernel
growth parameters
weight
```

That is much easier to inspect than one giant function containing all interactions.

---

## Precompute an execution plan

```python
@dataclass
class PreparedConnection:
    source: int
    target: int
    kernel_f: np.ndarray
    mu: float
    sigma: float
    weight: float


def prepare_connections(connections, shape):
    return [
        PreparedConnection(
            source=c.source,
            target=c.target,
            kernel_f=kernel_fft(c.kernel, shape),
            mu=c.mu,
            sigma=c.sigma,
            weight=c.weight,
        )
        for c in connections
    ]
```

The simulation loop should execute prepared data, not repeatedly reconstruct model structure.

This is the same distinction between configuration and runtime representation that appears in larger software systems.

---

## Visualize channels separately

```python
import matplotlib.pyplot as plt

for channel in range(state.shape[0]):
    plt.figure(figsize=(4, 4))
    plt.imshow(state[channel], vmin=0, vmax=1)
    plt.title(f"channel {channel}")
    plt.axis("off")
    plt.show()
```

Also create composites:

```python
rgb = np.moveaxis(state[:3], 0, -1)
plt.imshow(np.clip(rgb, 0, 1))
plt.axis("off")
plt.show()
```

A combined image can hide important internal dynamics, so always retain per-channel inspection.

---

## Search becomes structural

Our earlier parameter search varied numbers.

Now we might also vary:

```text
number of channels
number of connections
source/target topology
kernel radii
connection weights
```

The search space is no longer just numerical.

It includes **architecture**.

That is a useful preview of neural cellular automata, where the local update rule itself will become learned.

---

## Avoid unnecessary biological claims

Multiple channels can produce behaviors that look tissue-like or organism-like.

That does not mean each channel corresponds to a chemical, cell type or biological pathway.

Keep the interpretation disciplined:

```text
observed:
multiple interacting local fields produce persistent morphology

not automatically established:
biological equivalence
```

Artificial life becomes more interesting when we are precise about what has actually emerged.

---

## Richer systems create a new question

A pattern may survive indefinitely under perfect conditions.

But is it robust?

What happens if we:

```text
delete part of it
inject noise
change parameters slightly
collide it with another structure
```

Persistence under no disturbance is a weak test.

In the next chapter we will turn **damage and recovery** into measurable experiments and separate genuine robustness from lucky stability.