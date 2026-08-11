+++
date = '2026-08-10T20:35:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 39: Grow a Target From One Seed'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Morphogenesis', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 39: Grow a Target From One Seed

Now we can pose the central morphogenesis problem:

> Start from one cell and learn local rules that construct a target pattern.

## Prepare a target

Assume an RGBA image has been loaded into a tensor:

```python
# shape: [1, 4, H, W], values in [0, 1]
target = load_target("target.png").to(DEVICE)
```

The NCA state contains more channels than the image, so only the visible channels are compared:

```python
def target_loss(x, target):
    return F.mse_loss(x[:, :4], target)
```

## Randomize rollout length

Training at one exact step count encourages brittle timing tricks.

Instead sample a horizon:

```python
steps = torch.randint(64, 97, ()).item()
x = make_seed(size=target.shape[-1], channels=16)

for _ in range(steps):
    x = model(x)
```

Now the model must approach a useful region of state space across a range of times.

## Train the local rule

```python
optimizer = torch.optim.Adam(model.parameters(), lr=2e-3)

for iteration in range(8000):
    x = make_seed(size=target.shape[-1], channels=16)
    steps = torch.randint(64, 97, ()).item()

    for _ in range(steps):
        x = model(x)

    loss = target_loss(x, target)

    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
```

## Why growth from one seed is difficult

Every cell executes the same local rule, yet different regions must eventually play different roles.

The system has to create its own positional information through local interactions.

That is the real problem:

```text
identical rule
+ local communication
+ recurrent hidden state
        ↓
spatial differentiation
```

## Do not judge only the final frame

Record the entire trajectory:

```python
frames = []
x = make_seed()

for step in range(128):
    x = model(x)
    if step % 4 == 0:
        frames.append(x[:, :4].detach().cpu())
```

Later, the visual pass for this book should turn this trajectory into an animation. The process of becoming is more informative than the final image.

## A low final loss can still hide a bad dynamical system

Check what happens after the training horizon:

```python
for _ in range(500):
    x = model(x)
```

Does the organism:

```text
persist?
explode?
decay?
drift?
keep growing?
```

A model that reaches the target and then destroys it has learned growth, not homeostasis.

## Separate growth from persistence

This distinction gives us three different capabilities:

```text
growing      = reach the target
persistent   = remain near the target
regenerating = return after damage
```

They should be tested separately.

Further reading: [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/).

Before training persistence and regeneration, however, we need to remove another unrealistic assumption: that every cell updates at exactly the same instant.

In the next chapter we randomize the update schedule.