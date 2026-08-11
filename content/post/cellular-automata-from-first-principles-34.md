+++
date = '2026-08-10T20:03:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 34: Damage, Robustness and Persistence'
categories = ['Programming', 'Artificial Life']
tags = ['Cellular Automata', 'Python', 'Lenia', 'Robustness', 'Regeneration']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 34: Damage, Robustness and Persistence

A pattern that survives in perfect conditions is only the beginning.

A stronger artificial-life question is:

> What happens when the pattern is disturbed?

We can turn that into an experiment.

---

## Define damage explicitly

Start with a rectangular ablation:

```python
def damage_rectangle(state, y0, y1, x0, x1):
    damaged = state.copy()
    damaged[..., y0:y1, x0:x1] = 0.0
    return damaged
```

For a single-channel state:

```python
damaged = damage_rectangle(state, 55, 70, 55, 70)
```

For multi-channel state, the ellipsis damages all channels in the same spatial region.

---

## Compare damaged and undamaged controls

Always keep a control run:

```python
control = state.copy()
damaged = damage_rectangle(state, 55, 70, 55, 70)

for _ in range(500):
    control = lenia_step(control, kernel_f, config)
    damaged = lenia_step(damaged, kernel_f, config)
```

Without the control, we might mistake ordinary evolution for damage response.

---

## Measure recovery of mass

```python
def relative_mass(state, reference):
    return float(state.sum() / max(reference.sum(), 1e-12))
```

Track:

```text
immediately after damage
100 steps later
500 steps later
```

Mass recovery alone does not prove morphological recovery, but it is one useful signal.

---

## Compare shape

Threshold the field:

```python
def binary_mask(state, threshold=0.05):
    return state > threshold
```

Then use intersection-over-union:

```python
def iou(a, b):
    a = binary_mask(a)
    b = binary_mask(b)

    intersection = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()

    if union == 0:
        return 1.0

    return float(intersection / union)
```

For moving organisms, direct pixel alignment is unfair.

We may need translation alignment before comparing shape.

---

## Align by center of mass

```python
def shift_to_center(state):
    centre = center_of_mass(state)
    if centre is None:
        return state.copy()

    target_y = state.shape[-2] // 2
    target_x = state.shape[-1] // 2

    y, x = centre
    dy = int(round(target_y - y))
    dx = int(round(target_x - x))

    return np.roll(np.roll(state, dy, axis=-2), dx, axis=-1)
```

Then compare aligned states.

This separates:

```text
shape changed
```

from:

```text
shape merely moved
```

---

## Noise perturbations

Damage does not have to delete a chunk.

Add noise:

```python
def add_noise(state, amount=0.05, seed=42):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, amount, size=state.shape)
    return np.clip(state + noise, 0.0, 1.0)
```

Or randomly erase cells:

```python
def dropout_damage(state, probability=0.1, seed=42):
    rng = np.random.default_rng(seed)
    keep = rng.random(state.shape[-2:]) > probability
    return state * keep
```

Different perturbations test different forms of robustness.

---

## Parameter perturbations

The environment itself can change.

For example:

```python
perturbed = LeniaConfig(
    radius=config.radius,
    ring_center=config.ring_center,
    ring_width=config.ring_width,
    mu=config.mu + 0.005,
    sigma=config.sigma,
    dt=config.dt,
)
```

Ask whether the organism still persists.

This distinguishes a broad stable basin from an exact brittle parameter point.

---

## A robustness matrix

Run many perturbation levels:

```text
damage fraction:  0%  10%  20%  30%  40%
noise level:       0  .01  .03  .05  .10
parameter shift:   0  .002 .005 .010 .020
```

For each combination record:

```text
survival
recovery time
final mass ratio
aligned shape similarity
sustained activity
```

Now robustness becomes a surface, not a yes/no anecdote.

---

## Define recovery time

```python
def recovery_time(simulator, damaged, reference_shape, threshold=0.8, max_steps=1000):
    state = damaged.copy()

    for step_index in range(max_steps):
        state = simulator(state)
        aligned = shift_to_center(state)

        if iou(aligned, reference_shape) >= threshold:
            return step_index

    return None
```

The exact metric depends on the pattern, but the experimental structure is reusable.

---

## Robustness is not regeneration

Be careful with language.

A pattern might:

```text
survive damage while staying deformed
```

or:

```text
regrow mass but not original morphology
```

or:

```text
return to a close version of its previous form
```

Those are different outcomes.

Use the evidence to decide which claim is justified.

---

## Collisions are perturbations too

Place two structures near each other.

Possible outcomes:

```text
annihilation
fusion
scattering
capture
stable coexistence
fragmentation
```

Track both morphology and mass through the event.

Collision experiments can expose dynamics invisible in isolated runs.

---

## Robustness becomes a search objective

Instead of selecting candidates only for survival, evaluate them under a perturbation suite:

```python
def robust_candidate_score(candidate, perturbations):
    scores = []

    for perturb in perturbations:
        outcome = evaluate_perturbation(candidate, perturb)
        scores.append(outcome["recovery_score"])

    return float(np.mean(scores))
```

Now evolution/search can explicitly seek systems that withstand damage.

---

## A deeper limitation remains

Ordinary Lenia can create and remove local state through the growth function:

```text
A(t + dt) = clip(A(t) + dt * G(U))
```

Total mass is not conserved.

That makes beautiful self-organizing dynamics possible, but it also means growth can appear locally without material being transported from somewhere else.

What happens if we impose a stronger physical-style constraint?

In the next chapter we will examine **Flow-Lenia**, where the update is reformulated around transport and mass conservation, and see why that changes the possibilities for interacting artificial organisms.