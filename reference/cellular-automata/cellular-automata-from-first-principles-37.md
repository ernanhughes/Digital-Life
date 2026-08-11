+++
date = '2026-08-10T20:32:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 37: Learn the Local Update Rule'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 37: Learn the Local Update Rule

A neural cellular automaton does not need a large neural network.

It needs a **small local network applied everywhere**.

That distinction matters.

The intelligence of the system comes less from the size of one cell's computation and more from the repeated interaction of many cells over time.

---

## Perception first

Each cell needs information about itself and nearby cells.

For a single visible channel we can compute several local features:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

IDENTITY = torch.tensor(
    [[0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0]]
)

SOBEL_X = torch.tensor(
    [[-1.0, 0.0, 1.0],
     [-2.0, 0.0, 2.0],
     [-1.0, 0.0, 1.0]]
) / 8.0

SOBEL_Y = SOBEL_X.T
```

These represent:

```text
current value
horizontal gradient
vertical gradient
```

Now every cell can sense both local state and local direction.

---

## Apply perception channel-wise

```python
def perceive(x):
    channels = x.shape[1]

    kernels = torch.stack([IDENTITY, SOBEL_X, SOBEL_Y]).to(x.device)
    kernels = kernels[:, None]
    kernels = kernels.repeat(channels, 1, 1, 1)

    y = F.conv2d(x, kernels, padding=1, groups=channels)

    batch, _, height, width = y.shape
    return y.view(batch, channels * 3, height, width)
```

The operation is still local.

Every output feature depends only on a 3×3 neighborhood.

---

## A tiny neural rule

We can now process those local features using `1×1` convolutions.

A `1×1` convolution is useful here because it mixes feature channels **within each cell** without expanding the spatial neighborhood.

```python
class LocalRule(nn.Module):
    def __init__(self, channels, hidden=128):
        super().__init__()
        self.fc1 = nn.Conv2d(channels * 3, hidden, kernel_size=1)
        self.fc2 = nn.Conv2d(hidden, channels, kernel_size=1, bias=False)

        nn.init.zeros_(self.fc2.weight)

    def forward(self, x):
        p = perceive(x)
        h = F.relu(self.fc1(p))
        return self.fc2(h)
```

That final zero initialization is deliberate.

At the beginning of training:

```text
predicted update ≈ 0
```

so the automaton starts close to an identity process instead of immediately exploding.

---

## Residual updates

The network predicts a **change**, not a replacement state.

```python
class NeuralCA(nn.Module):
    def __init__(self, channels=16, hidden=128):
        super().__init__()
        self.rule = LocalRule(channels, hidden)

    def forward(self, x):
        dx = self.rule(x)
        return x + dx
```

This gives us:

```text
state_(t+1) = state_t + delta_t
```

Residual dynamics are a natural fit for systems that evolve gradually.

---

## The rule is shared across the whole world

The exact same network parameters are applied at every cell.

There is no separate model for:

```text
cell (10, 20)
cell (10, 21)
cell (10, 22)
```

The rule is translation-equivariant.

A cell's action depends on local state, not absolute position.

That constraint is not a limitation to work around.

It is the mechanism that forces self-organization.

---

## Repeated application creates depth in time

One update step is a tiny network.

But after 64 updates:

```text
local network
local network
local network
...
64 times
```

information can propagate across much larger distances.

A one-cell-radius neighborhood does not mean the system can only solve one-cell-radius problems.

It means long-range coordination must emerge through repeated local communication.

---

## Train through a rollout

```python
def rollout(model, state, steps):
    for _ in range(steps):
        state = model(state)
    return state
```

Then:

```python
final = rollout(model, initial, steps=64)
loss = loss_fn(final, target)
loss.backward()
```

PyTorch differentiates through the entire sequence.

The local update network receives learning signal from the global final objective.

---

## One rule, many cells, one objective

This architecture creates a fascinating inversion:

```text
centralized training
        ↓
shared local rule
        ↓
decentralized execution
```

During training we can use a global loss.

During execution every cell only needs local information.

That separation will become increasingly important when we study robustness and regeneration.

---

## Why this resembles biology without being biology

It is tempting to say:

```text
cell = biological cell
hidden state = chemicals
network = genome
```

Those analogies can be useful intuition, but they are analogies.

This model is a computational system, not a validated biological model.

The useful structural similarity is narrower:

> many locally interacting units share the same update machinery yet can collectively produce global organization.

That is enough to make the architecture interesting.

---

## We still need richer state

If every cell stores only RGB values, it must simultaneously use those values to:

```text
represent appearance
communicate
store memory
coordinate growth
```

That is restrictive.

The classic Growing Neural Cellular Automata setup uses additional hidden channels whose meaning is not specified in advance. The learned rule is free to use them as internal signals.

Further reading: [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/).

In the next chapter we will add those hidden channels and turn each cell from a visible pixel into a small local state machine.