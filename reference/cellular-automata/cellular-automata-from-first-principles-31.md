+++
date = '2026-08-10T19:54:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 31: Discover Your First Lenia Organisms'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Lenia', 'Artificial Life', 'Search']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 31: Discover Your First Lenia Organisms

Running Lenia is easy.

Finding persistent, localized, non-trivial structures is the hard part.

This chapter turns that problem into a repeatable search pipeline.

---

## Define what counts as a candidate

We should not start with the vague objective:

> Find something that looks alive.

Instead define measurable properties.

A useful first candidate might be:

```text
survives for 1,000 steps
stays localized
keeps non-zero mass
continues changing
avoids filling the whole board
```

Each condition removes a different failure mode.

---

## Evaluate persistence

```python
def survives(state, threshold=1e-3):
    return state.sum() > threshold
```

Track it over a run:

```python
def survival_time(state, kernel_f, config, max_steps=1000):
    for step_index in range(max_steps):
        state = lenia_step(state, kernel_f, config)
        if not survives(state):
            return step_index

    return max_steps
```

---

## Evaluate localization

```python
def localization_score(state, threshold=0.05):
    active = state > threshold
    fraction = active.mean()
    return float(1.0 - fraction)
```

A completely active board scores poorly.

A very small localized pattern scores highly.

But a single dying pixel would also score highly.

That is why objectives must be combined.

---

## Measure sustained activity

```python
def sustained_activity(history, tail=100):
    values = [row["activity"] for row in history[-tail:]]
    return float(np.mean(values))
```

A static blob may be persistent but dynamically uninteresting.

A pattern that remains active without exploding is a stronger candidate.

---

## Evaluate a seed

```python
def evaluate_seed(initial, config, steps=1000):
    kernel = build_kernel(config)
    kernel_f = kernel_fft(kernel, initial.shape)

    final, history = run(
        initial.copy(),
        kernel_f,
        config,
        steps=steps,
    )

    return {
        "final_mass": float(final.sum()),
        "active_fraction": active_fraction(final),
        "activity": sustained_activity(history),
        "final": final,
        "history": history,
    }
```

Now discovery can be automated.

---

## Generate many initial conditions

```python
def seed_bank(count, shape=(128, 128), patch=24, base_seed=1000):
    for index in range(count):
        yield random_seed(
            shape=shape,
            patch=patch,
            seed=base_seed + index,
        )
```

Evaluate them:

```python
results = []

for index, initial in enumerate(seed_bank(100)):
    result = evaluate_seed(initial, config)
    result["seed_index"] = index
    results.append(result)
```

---

## Reject obvious failures first

Simulation is expensive.

Use staged evaluation:

```text
100 steps
  ↓
reject dead / exploded
  ↓
500 steps
  ↓
reject unstable
  ↓
2,000 steps
  ↓
inspect survivors
```

This is the same principle used in many search systems:

```text
cheap filter before expensive evaluation
```

---

## Build a candidate score

For ranking only, we can combine several normalized properties:

```python
def candidate_score(result):
    mass_ok = min(result["final_mass"] / 100.0, 1.0)
    localized = 1.0 - result["active_fraction"]
    active = min(result["activity"] / 0.02, 1.0)

    return 0.3 * mass_ok + 0.4 * localized + 0.3 * active
```

Do not confuse this with a scientific definition of life.

It is an engineering ranking function for one search task.

---

## Keep diversity

If we simply keep the top twenty candidates, they may all be near-duplicates.

Compute simple descriptors:

```python
def descriptors(result):
    final = result["final"]
    return np.array([
        final.sum(),
        final.mean(),
        final.var(),
        result["active_fraction"],
        result["activity"],
    ])
```

Then prefer candidates far apart in descriptor space.

This is the beginning of novelty search and quality-diversity methods.

---

## Save everything required to replay

For every promising candidate, save:

```text
parameter config
initial seed
random seed
simulation length
metrics
final state
optional frames
```

A screenshot without lineage is not a scientific result.

---

## Human judgment still matters

Automated metrics can remove obvious failures.

They cannot fully capture properties such as:

```text
interesting symmetry
coherent locomotion
repeated appendages
collision behavior
regeneration
morphological novelty
```

A productive workflow is:

```text
automated search
      ↓
rank + diversify
      ↓
human inspection
      ↓
label interesting behaviors
      ↓
improve search objectives
```

That creates a feedback loop between computation and observation.

---

## Make discovery visual

Save thumbnails for the best candidates:

```python
def save_candidate_image(state, filename):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(4, 4))
    plt.imshow(state, cmap="viridis", vmin=0, vmax=1)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
```

An atlas of discovered forms is often more useful than a terminal full of scores.

---

## Discovery is now an engineering problem

We have converted:

> Maybe tweak `mu` until something cool happens.

into:

```text
candidate generator
      ↓
simulator
      ↓
measurements
      ↓
filters
      ↓
ranking
      ↓
diversity preservation
      ↓
replayable archive
```

That architecture scales far beyond Lenia.

---

## Next: search the parameter space too

So far we held the Lenia rule fixed and varied initial conditions.

But interesting structures also depend strongly on:

```text
mu
sigma
kernel radius
ring geometry
time step
```

In the next chapter we will search **both the organism seed and the world parameters**, and use the experimental machinery from Part III to keep that search reproducible instead of turning it into random parameter roulette.