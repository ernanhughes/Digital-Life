+++
date = '2026-08-10T20:59:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 56: Generate Figures and Animations'
categories = ['Programming', 'Visualization']
tags = ['Cellular Automata', 'Visualization', 'Matplotlib', 'Animation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 56: Generate Figures and Animations

Cellular automata are visual systems.

That makes figures and animations unusually important.

But a useful image is not merely a screenshot. It should be a reproducible output of an experiment.

---

## Save figures from data, not from memory

Suppose an experiment has produced a spacetime history:

```python
history = np.stack(states)
```

A figure generator should accept that result explicitly:

```python
import matplotlib.pyplot as plt


def save_spacetime(history, path):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(history, interpolation="nearest", aspect="auto")
    ax.set_xlabel("cell")
    ax.set_ylabel("time")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
```

Now the PNG is derived from recorded state rather than from an interactive session we cannot reproduce.

---

## Different phenomena need different views

For an elementary rule:

```text
spacetime diagram
```

For traffic:

```text
spacetime diagram
fundamental diagram: density vs flow
```

For reaction-diffusion:

```text
field snapshot
parameter sweep grid
```

For Lenia:

```text
state image
centroid path
mass/activity time series
animation
```

For NCA:

```text
growth animation
damage/recovery comparison
hidden-channel visualization
loss over time
```

The figure should expose the mechanism or evidence the chapter is discussing.

---

## Generate animations from stored frames

```python
from matplotlib.animation import FuncAnimation


def save_animation(frames, path, fps=20):
    fig, ax = plt.subplots()
    image = ax.imshow(frames[0], animated=True)
    ax.axis("off")

    def update(i):
        image.set_data(frames[i])
        return (image,)

    animation = FuncAnimation(fig, update, frames=len(frames), blit=True)
    animation.save(path, fps=fps)
    plt.close(fig)
```

The exact writer depends on the output format installed in the environment, so keep the rendering backend configurable.

---

## Do not store every simulation step unnecessarily

A 10,000-step, 1024×1024 float simulation can produce enormous histories.

Sample frames deliberately:

```python
if step % frame_interval == 0:
    frames.append(state.copy())
```

The frame interval is part of the artifact metadata.

---

## Build comparisons into the figure generator

Regeneration is clearer as:

```text
before damage | immediately after | recovered
```

than as three unrelated files.

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, image, title in zip(
    axes,
    [before, damaged, recovered],
    ["before", "damaged", "recovered"],
):
    ax.imshow(image)
    ax.set_title(title)
    ax.axis("off")
```

The comparison is the argument.

---

## Plot measurements next to appearance

A compelling animation can hide instability.

Pair visual evidence with quantitative traces:

```text
state image
mass over time
activity over time
centroid displacement
recovery error
```

This keeps the visual and analytical stories connected.

---

## Make artifact names stable

Instead of:

```text
final.png
final2.png
really-final.png
```

use names derived from experiment identity:

```text
rule184-density-0.30-seed-42-spacetime.png
lenia-run-a17-mass.png
nca-damage-square-recovery.gif
```

Better still, place them under a run ID.

---

## Save a manifest

```python
manifest = {
    "experiment_id": experiment_id,
    "figure": "traffic-flow.png",
    "source_result": "metrics.json",
    "generator": "plot_traffic_flow",
}
```

Now a publication artifact has lineage.

---

## Figures should be rebuildable

The ideal command is conceptually:

```text
run experiment
      ↓
save raw outputs
      ↓
generate figures
      ↓
generate animation
```

not:

```text
open notebook
click around
remember what looked good
save screenshot
```

That difference becomes critical when a book contains dozens of figures.

---

## This closes the loop with the publication layer

The website does not need to own every experiment.

It needs trustworthy assets that can be traced back to code and results.

That is the architecture we discussed earlier, and this chapter gives it a concrete technical form.

Next we will assemble all of these pieces into one coherent cellular-automata laboratory.