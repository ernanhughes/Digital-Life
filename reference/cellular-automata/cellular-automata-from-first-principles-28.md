+++
date = '2026-08-10T19:45:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 28: Neighborhoods as Convolution Kernels'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Convolution', 'Kernels', 'Artificial Life']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 28: Neighborhoods as Convolution Kernels

A neighborhood does not have to be a list of nearby coordinates.

It can be a **spatial weighting function**.

That lets us say:

```text
cells near this radius matter a lot
cells closer in matter less
cells farther away do not matter at all
```

The standard programming tool for applying that same weighted neighborhood everywhere is convolution.

---

## Start with a small kernel

```python
import numpy as np

kernel = np.array([
    [0.0, 0.1, 0.0],
    [0.1, 0.6, 0.1],
    [0.0, 0.1, 0.0],
])
```

Normalize it:

```python
kernel = kernel / kernel.sum()
```

A neighborhood value is now a weighted sum rather than a count.

---

## Convolution with periodic boundaries

For teaching purposes, we can write convolution directly:

```python
def periodic_convolve(state, kernel):
    kh, kw = kernel.shape
    cy, cx = kh // 2, kw // 2

    result = np.zeros_like(state, dtype=np.float64)

    for ky in range(kh):
        for kx in range(kw):
            weight = kernel[ky, kx]
            if weight == 0:
                continue

            dy = ky - cy
            dx = kx - cx
            shifted = np.roll(np.roll(state, dy, axis=0), dx, axis=1)
            result += weight * shifted

    return result
```

This makes the mechanics explicit.

Later we can replace it with FFT convolution for speed without changing the model.

---

## Build a radial kernel

Lenia-style neighborhoods are usually easier to describe in terms of distance from the center.

```python
def radial_coordinates(radius):
    y, x = np.mgrid[-radius:radius+1, -radius:radius+1]
    r = np.sqrt(x*x + y*y) / radius
    return r
```

Now define a ring-shaped weighting function:

```python
def ring_kernel(radius=15, ring_center=0.5, ring_width=0.15):
    r = radial_coordinates(radius)

    kernel = np.exp(
        -((r - ring_center) ** 2) / (2 * ring_width ** 2)
    )

    kernel[r > 1.0] = 0.0
    kernel[r == 0.0] = 0.0
    kernel /= kernel.sum()

    return kernel
```

Visualize it:

```python
import matplotlib.pyplot as plt

kernel = ring_kernel()
plt.imshow(kernel, cmap="magma")
plt.colorbar()
plt.show()
```

The neighborhood is now a smooth ring rather than a 3x3 stencil.

---

## Why a ring?

A ring creates a preferred interaction scale.

Instead of asking:

```text
what is immediately adjacent?
```

we ask:

```text
how much activity exists around this characteristic radius?
```

That encourages spatial structures with a natural size.

This is one reason continuous artificial-life patterns can look organism-like rather than pixel-like.

---

## Neighborhood response

Given a state field:

```python
state = np.zeros((128, 128))
state[60:68, 60:68] = 1.0
```

compute the neighborhood field:

```python
neighborhood = periodic_convolve(state, kernel)
```

Now every cell has a continuous perception value.

```text
state(x, y)
    ↓
convolution kernel
    ↓
neighborhood potential U(x, y)
```

This `U` field is what our growth rule will inspect.

---

## Separate perception from reaction

This architecture is crucial:

```text
state
  ↓
kernel
  ↓
perception field
  ↓
growth function
  ↓
state update
```

The kernel answers:

> What local information reaches this cell?

The growth function answers:

> Given that information, should this cell increase or decrease?

Keeping these separate makes the system much easier to reason about and search.

---

## Multiple rings

A kernel can have more than one preferred distance.

```python
def multi_ring_kernel(radius=20):
    r = radial_coordinates(radius)

    inner = np.exp(-((r - 0.35) ** 2) / (2 * 0.08 ** 2))
    outer = 0.6 * np.exp(-((r - 0.72) ** 2) / (2 * 0.10 ** 2))

    kernel = inner + outer
    kernel[r > 1.0] = 0.0
    kernel /= kernel.sum()
    return kernel
```

Now local interaction has multiple spatial scales.

---

## FFT convolution

The direct implementation costs roughly:

```text
grid cells × kernel cells
```

That becomes expensive when both are large.

Convolution can also be computed in the frequency domain:

```text
convolution(a, b)
=
IFFT( FFT(a) * FFT(b) )
```

A compact periodic implementation is:

```python
def fft_convolve(state, kernel):
    padded = np.zeros_like(state)
    kh, kw = kernel.shape
    padded[:kh, :kw] = kernel

    padded = np.roll(padded, -kh // 2, axis=0)
    padded = np.roll(padded, -kw // 2, axis=1)

    return np.fft.ifft2(
        np.fft.fft2(state) * np.fft.fft2(padded)
    ).real
```

For production code we would test alignment carefully and probably precompute the kernel FFT.

The important point is architectural:

```text
same model
faster implementation
```

---

## Test the implementation

Never trust a fast convolution until it agrees with a simple reference implementation.

```python
small_state = np.random.default_rng(1).random((32, 32))
small_kernel = ring_kernel(radius=3)

a = periodic_convolve(small_state, small_kernel)
b = fft_convolve(small_state, small_kernel)

print(np.max(np.abs(a - b)))
```

Performance work should preserve semantics.

---

## The neighborhood is now part of the genome

When we search continuous CA, we are no longer searching only a transition table.

We may search:

```text
kernel radius
ring positions
ring widths
ring weights
growth center
growth width
time step
```

That is a much richer rule space.

Part III's search machinery is about to become essential.

---

## We still need a response function

The kernel gives us perception.

But perception alone does nothing.

We need to decide which neighborhood values produce growth and which produce decay.

That mapping is the next major component of Lenia.

In the next chapter we will build **growth functions**, inspect their geometry, and see how a narrow preference curve can stabilize patterns that would otherwise either disappear or flood the entire world.