+++
date = '2026-08-10T20:36:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 40: Randomize the Update Schedule'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Neural Cellular Automata', 'Asynchronous Updates']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 40: Randomize the Update Schedule

Most cellular automata in this book have used synchronous updates:

```text
all cells observe state_t
all cells update
state_t+1 appears
```

Neural cellular automata become more robust when we stop assuming perfect global synchronization.

## Stochastic firing

Instead of applying every predicted update, sample a binary mask:

```python
def stochastic_update(x, dx, fire_rate=0.5):
    mask = (
        torch.rand(
            x.shape[0], 1, x.shape[2], x.shape[3],
            device=x.device,
        ) <= fire_rate
    )
    return x + dx * mask
```

Half the cells update on average.

Which half changes every step.

## Put it inside the NCA

```python
class NeuralCA(nn.Module):
    def __init__(self, channels=16, hidden=128, fire_rate=0.5):
        super().__init__()
        self.rule = LocalRule(channels, hidden)
        self.fire_rate = fire_rate

    def forward(self, x):
        dx = self.rule(x)

        mask = (
            torch.rand(
                x.shape[0], 1, x.shape[2], x.shape[3],
                device=x.device,
            ) <= self.fire_rate
        )

        y = x + dx * mask
        return apply_life_mask(x, y)
```

The rule itself remains deterministic for a given local state.

The execution schedule is stochastic.

## Why this matters

A synchronized model can accidentally rely on exact phase relationships:

```text
step 20: everybody emits signal A
step 21: everybody interprets signal A
```

Randomized updates make that fragile strategy unreliable.

The learned process must tolerate cells being slightly out of phase.

That pushes the system toward more local, self-correcting coordination.

## Measure update-rate robustness

Do not train with `fire_rate=0.5` and assume the model works everywhere.

Test:

```python
for rate in [0.25, 0.4, 0.5, 0.6, 0.75, 1.0]:
    result = evaluate(model, fire_rate=rate)
    print(rate, result.loss)
```

This creates an update-schedule robustness curve.

## Stochastic does not mean nondeterministic experiments

For reproducible evaluation, seed the generator:

```python
torch.manual_seed(42)
```

For stronger experiment isolation, use explicit `torch.Generator` instances where practical and store the seed with the run metadata.

The book's recurring rule still applies:

> randomness should be part of the experiment definition, not an invisible source of variance.

## Local synchronization without a clock

The deeper idea is that coordination does not require a global scheduler.

Repeated local interactions can create enough effective synchronization for a global pattern to emerge.

This connects back to everything we have studied:

```text
local information
local state
local update
        ↓
global organization
```

But now the organization has to survive timing noise too.

The next problem is harder still.

Once the target has grown, can the same local dynamics **keep it there**?