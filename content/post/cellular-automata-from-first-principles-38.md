+++
date = '2026-08-10T20:34:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 38: Hidden Cell Channels and Local Memory'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata', 'Hidden State']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 38: Hidden Cell Channels and Local Memory

A visible pixel is not enough state for a cell that must also coordinate growth.

So give every cell a vector.

```text
[R, G, B, alpha, h1, h2, ... h12]
```

The first channels can be rendered. The rest are private internal state.

```python
CHANNELS = 16
VISIBLE = 4

state = torch.zeros(1, CHANNELS, 64, 64, device=DEVICE)
```

The hidden channels have no labels. We do not tell the model that channel 8 means "distance from the centre" or channel 11 means "grow east". If useful internal signals exist, training must discover them.

## A seed becomes a full cell state

```python
def make_seed(size=64, channels=16):
    x = torch.zeros(1, channels, size, size, device=DEVICE)
    c = size // 2
    x[:, 3:, c, c] = 1.0
    return x
```

Only one location starts alive, but it already contains several internal values.

## Visible state is only a projection

```python
def rgba(x):
    return x[:, :4]
```

This is a useful mental model:

```text
full cellular state
        ↓ projection
visible organism
```

The thing we see is not the whole dynamical system.

## Local perception across every channel

The same identity and gradient filters can be applied independently to all channels. A 16-channel state with three perception filters becomes 48 local features per cell.

```python
perceived = perceive(state)
print(perceived.shape)
# [batch, 48, height, width]
```

Those features then enter the shared `1×1` neural rule.

## Hidden state gives the system memory

A cell can change a hidden channel now and read it many updates later. Nearby cells can sense gradients in that channel. Information can therefore propagate without appearing directly in the rendered image.

Possible learned uses include:

```text
local phase
boundary signal
growth readiness
orientation cue
repair signal
internal timer
```

Those are hypotheses, not guaranteed interpretations.

## Living-cell masks

Growing NCA systems often distinguish cells that belong to the organism from empty space using an alpha-like channel.

```python
def living_mask(x):
    alpha = x[:, 3:4]
    return F.max_pool2d(alpha, kernel_size=3, stride=1, padding=1) > 0.1
```

After an update we can remove state from cells that are not near living cells:

```python
def apply_life_mask(before, after):
    pre = living_mask(before)
    post = living_mask(after)
    return after * (pre & post)
```

That prevents arbitrary hidden activity from spreading infinitely through empty space.

## The cell is now a tiny recurrent machine

Each cell has:

```text
private state
local perception
shared transition function
```

That is already enough for surprisingly rich distributed computation.

The next question is whether this system can coordinate itself from one seed into a prescribed global structure.

In the next chapter we train it to grow a target image.