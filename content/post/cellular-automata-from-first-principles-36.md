+++
date = '2026-08-10T20:31:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 36: Make the Automaton Differentiable'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Differentiable Programming']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 36: Make the Automaton Differentiable

So far every rule in this book has been chosen by us.

Even Lenia still asks us to decide the neighborhood kernel, the growth function and the parameters that connect them.

What if we stop designing the local rule directly?

What if we define only the **goal**, then let gradient descent discover a local update rule that achieves it?

That requires one major change:

> the cellular automaton must become differentiable.

---

## A cellular automaton is already a repeated function

Every system we have built can be written as:

```text
state_t
   ↓
local perception
   ↓
local update rule
   ↓
state_t+1
```

Or mathematically:

```text
x_(t+1) = F(x_t)
```

If `F` contains trainable parameters `theta`:

```text
x_(t+1) = F_theta(x_t)
```

then after many steps:

```text
x_T = F_theta(F_theta(...F_theta(x_0)))
```

If those operations are differentiable, a loss measured at `x_T` can send gradients all the way back into `theta`.

The automaton becomes a recurrent neural system.

---

## Start with PyTorch tensors

```python
import torch
import torch.nn.functional as F

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

state = torch.zeros(1, 1, 64, 64, device=DEVICE)
state[:, :, 32, 32] = 1.0
```

The dimensions are:

```text
batch
channel
height
width
```

This is already a useful change from our earlier NumPy examples because PyTorch can record the operations used to transform the state.

---

## Differentiable neighborhood perception

A classical automaton might explicitly count neighbors.

A differentiable automaton can perceive its neighborhood with convolution.

```python
kernel = torch.tensor(
    [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    device=DEVICE,
).view(1, 1, 3, 3)

perception = F.conv2d(state, kernel, padding=1)
```

Nothing here requires a hard decision such as:

```text
if neighbors == 3:
    become alive
```

The perception is a real-valued tensor that can flow into smooth functions.

---

## Replace hard thresholds with smooth functions

A hard threshold:

```python
alive = (perception > 2.5).float()
```

is awkward for gradient-based learning because the output changes abruptly.

Instead we can use a sigmoid:

```python
alive = torch.sigmoid(8.0 * (perception - 2.5))
```

The output still behaves like a threshold, but now small changes in the input create small changes in the output.

That creates useful derivatives.

---

## A trainable local rule

Let us make the threshold itself learnable.

```python
threshold = torch.nn.Parameter(torch.tensor(2.5, device=DEVICE))
sharpness = torch.nn.Parameter(torch.tensor(5.0, device=DEVICE))


def step(state):
    perception = F.conv2d(state, kernel, padding=1)
    return torch.sigmoid(sharpness * (perception - threshold))
```

Now the local rule has parameters.

We can optimize them.

---

## Define a target

Suppose we want the automaton to produce a ring.

```python
y, x = torch.meshgrid(
    torch.arange(64, device=DEVICE),
    torch.arange(64, device=DEVICE),
    indexing="ij",
)

r = torch.sqrt((x - 32) ** 2 + (y - 32) ** 2)
target = ((r > 10) & (r < 14)).float()[None, None]
```

The loss can simply compare the final state to the target:

```python
def loss_fn(state):
    return F.mse_loss(state, target)
```

---

## Unroll the automaton

```python
def rollout(initial_state, steps):
    state = initial_state
    for _ in range(steps):
        state = step(state)
    return state
```

Then train:

```python
optimizer = torch.optim.Adam([threshold, sharpness], lr=1e-2)

for iteration in range(1000):
    initial = torch.zeros_like(target)
    initial[:, :, 32, 32] = 1.0

    final = rollout(initial, steps=20)
    loss = loss_fn(final)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

This tiny example is deliberately restricted.

Two scalar parameters are nowhere near enough to learn rich morphogenesis.

But the important mechanism is already visible:

```text
target behavior
      ↓
loss
      ↓
backpropagation through time
      ↓
local rule parameters
```

---

## The global objective can train a local rule

This is the key idea.

The loss sees the **whole final pattern**.

But the update rule is applied locally and identically to every cell.

No cell receives coordinates saying:

```text
you are the top-left corner of the target
```

The system must learn a local process whose repeated application causes the global structure to emerge.

That is why neural cellular automata are interesting.

They combine:

```text
locality
weight sharing
recurrence
self-organization
learning
```

---

## Differentiability changes what can be specified

With hand-written CA we specify:

```text
rule
```

and observe:

```text
behavior
```

With differentiable CA we can specify:

```text
desired behavior
```

and optimize:

```text
rule
```

That reverses the direction of the design problem.

---

## But differentiable does not mean easy

Training through many recurrent steps creates familiar problems:

```text
vanishing gradients
exploding gradients
unstable dynamics
short-horizon solutions
fragile attractors
```

A model may learn to produce the target at exactly step 32 and then immediately destroy it.

That is not persistent morphogenesis.

It is merely trajectory fitting.

We will solve these problems progressively rather than hiding them.

---

## What we need next

A serious neural cellular automaton needs more expressive local computation than two trainable scalars.

The natural next step is:

```text
neighborhood perception
       ↓
small neural network
       ↓
state update
```

The same tiny network is applied independently at every cell.

That gives us a learned local rule.

In the next chapter we will build exactly that.