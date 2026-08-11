+++
date = '2026-08-10T19:57:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 32: Search Lenia Parameter Space'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Lenia', 'Search', 'Parameter Search']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 32: Search Lenia Parameter Space

A Lenia pattern is not defined by its initial state alone.

It also lives inside a particular dynamical world.

Change the kernel or growth function slightly and the same seed may:

```text
die
explode
freeze
oscillate
move
split
stabilize into a different morphology
```

So discovery has two coupled search spaces:

```text
initial condition
      +
world parameters
```

---

## Define parameter ranges

```python
PARAM_RANGES = {
    "radius": (8, 24),
    "ring_center": (0.25, 0.75),
    "ring_width": (0.05, 0.25),
    "mu": (0.05, 0.30),
    "sigma": (0.01, 0.08),
    "dt": (0.03, 0.20),
}
```

These ranges are experimental choices.

They define which region of Lenia space we are willing to explore.

---

## Sample a configuration

```python
def sample_config(rng):
    return LeniaConfig(
        radius=int(rng.integers(8, 25)),
        ring_center=float(rng.uniform(0.25, 0.75)),
        ring_width=float(rng.uniform(0.05, 0.25)),
        mu=float(rng.uniform(0.05, 0.30)),
        sigma=float(rng.uniform(0.01, 0.08)),
        dt=float(rng.uniform(0.03, 0.20)),
    )
```

A random search is not sophisticated.

But it gives us a baseline.

Never build an elaborate optimizer before measuring what random search can already find.

---

## Evaluate configurations and seeds together

```python
def evaluate_trial(config, seed_value, shape=(128, 128), steps=500):
    initial = random_seed(shape=shape, seed=seed_value)
    result = evaluate_seed(initial, config, steps=steps)

    return {
        "config": config,
        "seed": seed_value,
        "score": candidate_score(result),
        "result": result,
    }
```

Then:

```python
rng = np.random.default_rng(1234)
trials = []

for trial_id in range(200):
    config = sample_config(rng)
    seed_value = int(rng.integers(0, 1_000_000))
    trials.append(evaluate_trial(config, seed_value))
```

---

## Separate failure categories

A single low score hides useful information.

Record explicit outcomes:

```python
def classify_outcome(result):
    final = result["final"]
    mass = final.sum()
    fraction = result["active_fraction"]
    activity = result["activity"]

    if mass < 1e-3:
        return "dead"
    if fraction > 0.8:
        return "world-filling"
    if activity < 1e-5:
        return "static"
    return "persistent-dynamic"
```

Now we can ask:

```text
Which parameters tend to die?
Which explode?
Where do persistent structures cluster?
```

Failure becomes data.

---

## Plot the search landscape

```python
import matplotlib.pyplot as plt

x = [t["config"].mu for t in trials]
y = [t["config"].sigma for t in trials]
c = [t["score"] for t in trials]

plt.scatter(x, y, c=c)
plt.xlabel("mu")
plt.ylabel("sigma")
plt.colorbar(label="candidate score")
plt.show()
```

This is only a two-dimensional projection of a larger parameter space.

But projections can reveal regions worth exploring more densely.

---

## Local refinement

Once a promising configuration appears, mutate around it:

```python
def mutate_config(config, rng):
    return LeniaConfig(
        radius=max(3, config.radius + int(rng.integers(-2, 3))),
        ring_center=float(np.clip(config.ring_center + rng.normal(0, 0.03), 0.05, 0.95)),
        ring_width=float(np.clip(config.ring_width + rng.normal(0, 0.02), 0.01, 0.40)),
        mu=float(np.clip(config.mu + rng.normal(0, 0.015), 0.01, 0.50)),
        sigma=float(np.clip(config.sigma + rng.normal(0, 0.008), 0.005, 0.20)),
        dt=float(np.clip(config.dt + rng.normal(0, 0.01), 0.01, 0.30)),
    )
```

The strategy becomes:

```text
explore broadly
      ↓
find promising region
      ↓
search locally
```

---

## Robustness matters more than one lucky run

A configuration that works for one exact seed may be extremely fragile.

Evaluate multiple nearby seeds:

```python
def robustness_score(config, seeds, steps=500):
    scores = []

    for seed_value in seeds:
        initial = random_seed(seed=seed_value)
        result = evaluate_seed(initial, config, steps=steps)
        scores.append(candidate_score(result))

    return {
        "mean": float(np.mean(scores)),
        "minimum": float(np.min(scores)),
        "std": float(np.std(scores)),
    }
```

A robust region should not collapse under tiny changes in initialization.

---

## Search for niches, not just champions

The highest score may not be the most interesting result.

Imagine three candidates:

```text
A: stationary pulsing blob
B: fast translating crescent
C: branching structure that repeatedly repairs itself
```

A single score may rank one highest and discard the others.

Instead maintain an archive indexed by behavioral descriptors:

```text
speed
mass
size
activity
symmetry
oscillation period
```

Keep the best candidate in each region of behavior space.

This is the quality-diversity idea in practical form.

---

## Search produces maps of possibility

A good search system does more than return one organism.

It can reveal:

```text
stable regions
fragile borders
extinction zones
world-filling zones
mobile-pattern niches
oscillatory niches
```

That changes the scientific question from:

> What creature did we find?

into:

> What kinds of behavior are possible in this family of worlds?

---

## Store the complete experiment table

Save every trial, not just winners.

A tabular record might contain:

```text
trial_id
seed
radius
ring_center
ring_width
mu
sigma
dt
survival
mass
activity
active_fraction
classification
score
artifact_path
```

Then later analysis does not require rerunning every simulation.

---

## The rule itself can become richer

So far one kernel produces one perception field and one growth response.

But biological systems rarely operate at only one spatial scale.

We can have:

```text
several kernels
several channels
several growth responses
cross-channel influence
```

That is the next major expansion.

In the next chapter we will build **multi-kernel and multi-channel Lenia**, where a cell's state becomes a vector again and different local fields can interact.