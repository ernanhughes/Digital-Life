+++
date = '2026-08-10T18:44:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 13: Build a Predator-Prey Ecosystem'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Predator Prey', 'Ecosystem Simulation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 13: Build a Predator-Prey Ecosystem

A forest fire mostly transforms cells in place.

Rule 184 moves occupancy in one constrained direction.

An ecosystem adds a harder problem:

```text
organisms move
organisms reproduce
predators consume prey
several organisms may want one destination
```

Now local intentions can conflict.

That means update semantics become part of the model.

---

## Separate visible kind from internal state

Start with:

```text
0 = empty
1 = prey
2 = predator
```

```python
import numpy as np

EMPTY = 0
PREY = 1
PREDATOR = 2

kind = np.zeros(
    (100, 100),
    dtype=np.uint8,
)
```

A richer model may need predator energy, age or reproduction state.

Do not overload one integer with every concept.

Use additional fields:

```python
energy = np.zeros(
    kind.shape,
    dtype=np.float32,
)
```

Now a cell's state is layered:

```text
visible occupancy
+
internal organism state
```

---

## Why naive in-place movement is dangerous

Suppose two predators both target the same prey.

If we mutate the grid immediately, whichever predator happens to be processed first wins.

Then Python loop order has become part of the ecology.

Sometimes sequential updates are a deliberate model choice.

But if they are not deliberate, they are a hidden source of causality.

A cleaner synchronous architecture is:

```text
current world
      ↓
propose actions
      ↓
resolve conflicting targets
      ↓
apply accepted actions
      ↓
next world
```

That is very close to transaction processing.

---

## Make conflict resolution explicit

A prey movement proposal might look like:

```python
(source, target, PREY)
```

Group proposals by target:

```python
from collections import defaultdict


def resolve_targets(
    proposals,
    rng,
):
    by_target = defaultdict(list)

    for proposal in proposals:
        by_target[
            proposal[1]
        ].append(proposal)

    accepted = []

    for target, choices in by_target.items():
        choice = choices[
            rng.integers(len(choices))
        ]

        accepted.append(choice)

    return accepted
```

Now the collision policy is part of the experiment.

We could instead choose:

```text
first proposal
highest-energy organism
random proposal
no proposal
priority by species
```

Those are different models.

---

## Give predators persistent state

A predator can lose energy every step and gain energy when it eats.

```python
MOVE_COST = 1.0
FOOD_ENERGY = 4.0
```

Conceptually:

```text
choose local action
      ↓
pay movement cost
      ↓
gain food energy if predation succeeds
      ↓
die if energy <= 0
```

Now the future depends on local history.

State has become memory.

---

## Track the world and the populations separately

A spatial snapshot tells us where interactions occur.

A population curve tells us what happens globally.

Those are complementary observables.

![Predator-prey spatial evolution](/images/cellular-automata/ca13-predator-prey-world.png)

![Predator and prey populations through time](/images/cellular-automata/ca13-predator-prey-populations.png)

The figure generator uses a deliberately compact local predator-prey CA to visualize the population-level phenomenon.

The chapter's propose/resolve architecture is the richer implementation pattern to use when explicit movement and target conflicts matter.

That distinction is useful:

```text
figure model:
demonstrate spatial population dynamics

engineering model:
make agent intentions and conflicts inspectable
```

---

## Oscillation is not guaranteed

It is tempting to draw this loop:

```text
prey increase
      ↓
predators increase
      ↓
prey decrease
      ↓
predators starve
      ↓
prey recover
```

That mechanism can produce oscillatory population dynamics.

But not every parameter choice will.

Possible outcomes include:

```text
prey extinction
predator extinction
both extinction
persistent coexistence
oscillation
spatial patchiness
```

So the existence and character of oscillation should be measured rather than assumed.

---

## Treat hidden choices as parameters

Important choices include:

```text
neighborhood shape
movement policy
collision resolution
predation probability
reproduction probability
energy gain
energy cost
boundary conditions
update synchrony
```

If those remain buried inside code, two ecosystem runs are difficult to compare meaningfully.

Make them explicit configuration.

---

## Keep causality inspectable

When an organism disappears, we should know why.

A lightweight event record can help:

```python
from dataclasses import dataclass


@dataclass
class Event:
    kind: str
    source: tuple[int, int] | None
    target: tuple[int, int] | None
```

Possible event kinds:

```text
move
eat
birth
starve
collision_lost
```

Now debugging does not require reconstructing every causal decision from snapshots after the fact.

This becomes increasingly important as cellular systems start to resemble local agents.

---

## One idea to keep

The difficult part of multi-agent cellular worlds is not merely writing more transition rules.

It is defining what simultaneous local action means.

Once several cells compete for shared resources or destinations, conflict resolution becomes part of the model.

In the next chapter we will use local updates for a different purpose: not to simulate an ongoing world, but to construct an organic cave map and then validate whether the result is actually usable.
