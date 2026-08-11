+++
date = '2026-08-10T20:40:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 47: Inspect Hidden-State Propagation'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Interpretability', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 47: Inspect Hidden-State Propagation

A neural cellular automaton can solve a maze while most of its computation remains invisible.

The visible output might be one distance channel.

The internal state may contain twelve more channels evolving underneath it.

This chapter asks:

> what is moving through those hidden channels while the answer is being computed?

---

## Capture the entire state trajectory

Instead of saving only the final output:

```python
@torch.no_grad()
def trace_rollout(model, state, steps, frozen_inputs):
    trace = [state.detach().cpu()]

    for _ in range(steps):
        state = model(state)
        state[:, :3] = frozen_inputs[:, :3]
        trace.append(state.detach().cpu())

    return torch.stack(trace)
```

The resulting tensor has a conceptual shape like:

```text
time × batch × channel × height × width
```

Now the recurrent computation is data we can analyze.

---

## Plot one hidden channel through time

```python
import matplotlib.pyplot as plt


def show_channel(trace, channel, times):
    fig, axes = plt.subplots(1, len(times), figsize=(3 * len(times), 3))

    for ax, t in zip(axes, times):
        ax.imshow(trace[t, 0, channel], cmap="coolwarm")
        ax.set_title(f"t={t}")
        ax.axis("off")

    plt.tight_layout()
```

Try:

```python
show_channel(trace, channel=7, times=[0, 4, 8, 16, 32, 64])
```

Some channels may look like noise.

Others may reveal striking spatial waves, boundary responses or persistent local markers.

Do not assign semantic names too quickly.

---

## Measure where a channel becomes active

A simple activity map:

```python
def channel_activity(trace, channel, threshold=0.1):
    values = trace[:, 0, channel].abs()
    return (values > threshold).float().mean(dim=0)
```

This answers:

```text
which cells used this channel frequently?
```

Compare activity with:

```text
walls
frontiers
goal distance
branch points
final path
```

Spatial alignment can suggest hypotheses.

It does not prove function.

---

## Track information arrival time

For each cell, record when a hidden channel first crosses a threshold.

```python
def first_activation_time(trace, channel, threshold=0.1):
    active = trace[:, 0, channel].abs() > threshold
    times = torch.full(active.shape[1:], -1, dtype=torch.long)

    for t in range(active.shape[0]):
        new = active[t] & (times < 0)
        times[new] = t

    return times
```

Plot that map.

If activation time grows with distance from the goal or start, the channel may participate in a propagating signal.

That is much more informative than one final heatmap.

---

## Compare hidden channels with BFS quantities

We have exact classical reference signals available:

```text
distance from goal
distance from start
reachable mask
BFS frontier arrival time
shortest-path membership
```

For each hidden channel, compute simple correlations.

```python
def correlation(a, b, mask=None):
    if mask is not None:
        a = a[mask]
        b = b[mask]

    a = a.float().flatten()
    b = b.float().flatten()

    a = a - a.mean()
    b = b - b.mean()

    return (a * b).mean() / (a.std() * b.std() + 1e-8)
```

A channel strongly correlated with BFS distance is interesting.

But correlation still does not mean the model explicitly represents "distance" in that channel.

---

## Probe hidden state with a simple decoder

Freeze the NCA.

Collect hidden states from many mazes.

Then train a small linear probe to predict a known quantity such as BFS distance.

Conceptually:

```python
probe = torch.nn.Conv2d(hidden_channels, 1, kernel_size=1)
```

Only train the probe.

If a linear decoder can recover distance, then distance-related information is accessible in the hidden representation.

Again, be precise:

```text
linearly decodable
```

is not the same as:

```text
used causally by the NCA
```

---

## Look at temporal phase changes

The hidden computation may not have one stationary meaning.

A channel can behave differently during:

```text
early propagation
mid-rollout conflict resolution
late stabilization
```

So compute statistics by time window:

```python
def temporal_energy(trace, channel):
    x = trace[:, 0, channel]
    return x.pow(2).mean(dim=(1, 2))
```

Plot energy versus step.

A channel that peaks early and disappears may be carrying transient frontier information.

A channel that remains active may encode persistent structure.

---

## Visualize gradients too

Another question is:

```text
which cells and channels can influence the final decision?
```

Keep one rollout differentiable and backpropagate from the output at a selected location.

```python
state.requires_grad_(True)
final = rollout(model, state, steps=64)
score = final[0, 3, query_y, query_x]
score.backward()

influence = state.grad.abs().sum(dim=1)[0]
```

This gives a local sensitivity map of the initial state.

For recurrent systems, such maps should be interpreted cautiously: gradients can vanish, explode or reflect only local linear sensitivity around one trajectory.

Still, they provide another view.

---

## Hidden states are not explanations by themselves

A colorful channel is easy to narrate.

That is dangerous.

A responsible workflow is:

```text
observe pattern
      ↓
form hypothesis
      ↓
compare with known quantities
      ↓
probe representation
      ↓
intervene on state
      ↓
measure behavioral change
```

The intervention step is crucial.

That is what we do next.

In the final NCA chapter we will zero, shuffle, freeze and perturb hidden channels to ask which internal signals are actually necessary for the learned computation.
