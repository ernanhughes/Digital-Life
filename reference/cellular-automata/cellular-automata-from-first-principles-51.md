+++
date = '2026-08-10T20:54:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 51: Run Cellular Automata on the GPU'
categories = ['Programming', 'Machine Learning', 'Performance']
tags = ['Cellular Automata', 'PyTorch', 'GPU', 'CUDA']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 51: Run Cellular Automata on the GPU

Once the update is expressed as tensor operations, moving to a GPU becomes straightforward.

But a GPU is not automatically faster.

It wins when there is enough parallel work to amortize transfer and launch overhead.

---

## A tensor implementation of Life

```python
import torch
import torch.nn.functional as F

LIFE_KERNEL = torch.tensor(
    [[1.0, 1.0, 1.0],
     [1.0, 0.0, 1.0],
     [1.0, 1.0, 1.0]]
).view(1, 1, 3, 3)


def life_step(x):
    kernel = LIFE_KERNEL.to(x.device)
    neighbors = F.conv2d(x, kernel, padding=1)
    alive = x > 0.5
    born = neighbors == 3
    survive = alive & (neighbors == 2)
    return (born | survive).float()
```

Represent a batch as:

```text
(batch, channel, height, width)
```

---

## Move state once

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
state = state.to(device)

for _ in range(1000):
    state = life_step(state)
```

Do not copy state back to the CPU every step unless you need it there.

A bad loop is:

```text
CPU → GPU → step → CPU → GPU → step → CPU
```

A better loop is:

```text
CPU → GPU → many steps → CPU
```

---

## Synchronize when timing CUDA

GPU kernels execute asynchronously relative to the host.

So this benchmark can lie:

```python
start = perf_counter()
state = life_step(state)
elapsed = perf_counter() - start
```

For CUDA timing:

```python
torch.cuda.synchronize()
start = perf_counter()

for _ in range(steps):
    state = life_step(state)

torch.cuda.synchronize()
elapsed = perf_counter() - start
```

Without synchronization, we may measure kernel submission rather than completion.

---

## Batch experiments

The GPU becomes especially useful when evaluating many worlds at once.

```python
state = torch.rand(256, 1, 256, 256, device=device) > 0.5
state = state.float()
```

Now 256 simulations share the same kernel launches.

This is ideal for:

```text
seed search
parameter sweeps
robustness testing
NCA training
benchmark ensembles
```

---

## Continuous systems fit naturally

Lenia-style updates use convolutions and pointwise functions, both GPU-friendly operations.

```python
field = F.conv2d(state, kernel, padding="same")
growth = 2 * torch.exp(-((field - mu) ** 2) / (2 * sigma**2)) - 1
state = torch.clamp(state + dt * growth, 0.0, 1.0)
```

Neural cellular automata are even more natural because their update rule is already built from convolutions and neural-network layers.

---

## Precision is part of the model

Moving from float64 to float32, float16 or bfloat16 can change performance substantially.

It can also change dynamics.

For chaotic or sensitive systems, tiny numerical differences may amplify.

So benchmark precision together with behavioral equivalence.

---

## CPU versus GPU is an experiment

Measure both.

A small 64×64 automaton may be faster on a CPU.

A large batched NCA rollout may strongly favor the GPU.

The useful question is not:

> Are GPUs faster?

It is:

> At what workload does this implementation cross over?

That is an engineering result we can record and reproduce.