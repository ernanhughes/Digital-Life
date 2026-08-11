+++
date = '2026-08-10T20:38:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 42: Regenerate After Damage'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata', 'Regeneration']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 42: Regenerate After Damage

Persistence asks whether the organism can remain near its target.

Regeneration asks a different question:

> after part of the state is destroyed, can local rules reconstruct the missing structure?

This is a much stronger test.

## Damage the state, not just the image

If we erase only visible RGBA channels but leave hidden channels untouched, the model may retain a perfect invisible blueprint.

A harder test removes **all channels** inside the damaged region.

```python
def damage(x, centre_y, centre_x, radius):
    y, z = torch.meshgrid(
        torch.arange(x.shape[-2], device=x.device),
        torch.arange(x.shape[-1], device=x.device),
        indexing="ij",
    )

    mask = ((y - centre_y) ** 2 + (z - centre_x) ** 2) > radius ** 2
    return x * mask[None, None]
```

Now the missing region loses appearance and internal state together.

## Put damage inside training

```python
def train_regeneration_step(model, x, target):
    x = damage(
        x,
        centre_y=torch.randint(20, 44, ()).item(),
        centre_x=torch.randint(20, 44, ()).item(),
        radius=torch.randint(6, 14, ()).item(),
    )

    steps = torch.randint(32, 65, ()).item()

    for _ in range(steps):
        x = model(x)

    return x, F.mse_loss(x[:, :4], target)
```

Different locations and sizes prevent the rule from memorizing one fixed wound.

## Train from mature states too

A useful pool now contains:

```text
seed
partial growth
mature organism
recently damaged organism
recovering organism
```

This broadens the states from which the rule must return toward the target.

## Measure recovery as a trajectory

Do not report only a post-damage screenshot.

```python
def recovery_curve(model, damaged, target, steps=128):
    x = damaged.clone()
    curve = []

    for step in range(steps):
        x = model(x)
        curve.append(float(F.mse_loss(x[:, :4], target)))

    return curve
```

Useful metrics include:

```text
peak damage error
minimum recovered error
steps to 50% recovery
steps to 90% recovery
final residual error
```

## Test multiple damage geometries

A robust evaluation suite should include more than circles:

```text
central deletion
edge deletion
horizontal slice
vertical slice
random rectangular cut
multiple small wounds
large catastrophic wound
```

The training distribution and evaluation distribution should be recorded separately.

Otherwise we can accidentally call memorized repair "general regeneration".

## Regeneration is evidence of corrective dynamics

A regenerating NCA is not simply replaying its original growth trajectory.

After damage, the remaining cells are in a state that may never have appeared during clean growth.

The rule must use local context to steer the system back toward an acceptable global configuration.

That is why regeneration is such an interesting property of local learned systems.

## But do not overclaim

Successful recovery of one image under one family of masks does not establish biological regeneration, universal self-repair or general intelligence.

It establishes something precise and still remarkable:

> a learned local rule can maintain and reconstruct a distributed target morphology under specified perturbations.

Further reading: [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/).

The next test is whether these dynamics survive conditions that were not exactly present during training.