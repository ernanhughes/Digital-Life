+++
date = '2026-08-10T20:55:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 52: Use FFTs for Large Neighborhoods'
categories = ['Programming', 'Performance']
tags = ['Cellular Automata', 'FFT', 'Lenia', 'Convolution']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 52: Use FFTs for Large Neighborhoods

Small local neighborhoods are cheap to evaluate directly.

Large smooth kernels are different.

Lenia taught us that a neighborhood may cover dozens of cells in every direction. At that scale, direct convolution can become expensive.

The Fourier transform gives us another route.

---

## Convolution becomes multiplication

For periodic domains:

```text
convolution in space
        ↕
multiplication in frequency
```

So instead of sliding a large kernel over every location, we can transform both arrays, multiply them, and transform back.

```python
import numpy as np


def fft_convolve_periodic(state, kernel):
    kernel_fft = np.fft.fft2(kernel)
    state_fft = np.fft.fft2(state)
    return np.fft.ifft2(state_fft * kernel_fft).real
```

The kernel must be aligned correctly for circular convolution. A convenient construction is to place its center at the origin with `ifftshift` before transforming.

```python
kernel_fft = np.fft.fft2(np.fft.ifftshift(kernel))
```

---

## Precompute static kernels

If the kernel does not change during a rollout, do not transform it every step.

```python
kernel_fft = np.fft.fft2(np.fft.ifftshift(kernel))


def step(state):
    field = np.fft.ifft2(np.fft.fft2(state) * kernel_fft).real
    return update_from_field(state, field)
```

This turns repeated neighborhood evaluation into:

```text
FFT(state)
pointwise multiply
inverse FFT
```

---

## When does FFT win?

Not always.

For a 3×3 kernel, direct convolution is usually the natural choice.

For a large radius, FFT methods can become attractive because their cost scales roughly with:

```text
N log N
```

rather than with the number of kernel taps per output cell.

The crossover depends on:

```text
grid size
kernel size
backend
batch size
CPU/GPU
precision
```

Measure it.

---

## Compare implementations

```python
def compare(a, b):
    error = np.max(np.abs(a - b))
    print("max error:", error)

field_direct = direct_convolve(state, kernel)
field_fft = fft_convolve_periodic(state, kernel)
compare(field_direct, field_fft)
```

Boundary semantics must match.

A circular FFT convolution is naturally periodic. Comparing it with zero-padded direct convolution is comparing different models.

---

## Multi-channel systems

For several channels and kernels, frequency-domain computation can be batched.

Conceptually:

```text
state channel FFTs
        ↓
frequency-domain kernel mixing
        ↓
inverse FFTs
        ↓
growth/update functions
```

This is useful for multi-kernel Lenia and related systems.

---

## GPU FFTs

PyTorch exposes FFT operations directly:

```python
state_f = torch.fft.fft2(state)
kernel_f = torch.fft.fft2(kernel)
field = torch.fft.ifft2(state_f * kernel_f).real
```

Again, keep tensors on the device throughout the rollout.

---

## Numerical differences are expected

Direct and FFT-based convolution can differ slightly because floating-point operations occur in a different order.

For continuous dynamical systems, tiny differences may grow over long rollouts.

Therefore validate at two levels:

```text
local numerical agreement
behavioral agreement over time
```

The second is often more important than expecting bit-identical trajectories.

---

## Choose the algorithm from the structure

We now have three broad neighborhood strategies:

```text
small stencil          → shifts/slices/direct convolution
learned local kernels  → standard tensor convolution
large periodic kernels → FFT convolution
```

A reusable cellular-automata system should make those choices explicit rather than burying them inside each chapter's code.

That is what we build next.