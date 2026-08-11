+++
title = "Digital Life 12: The Closest Thing We Have"
date = "2026-08-11T10:43:00+01:00"
draft = false
description = "What is the strongest existing example of digital life? We examine Outlier, a binary cellular automaton in which distributed self-replicators emerge from simple local dynamics."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Outlier", "Cellular Automata", "Self-Replication", "Open-Ended Evolution"]
+++

Before inventing our digital life, we should steal everything we can.

Not code.

Ideas.

Experiments.

Failures.

Mechanisms.

So let's ask the obvious question:

> **What is the closest thing to digital life that anyone has actually built?**

There is no objective answer.

Different Artificial Life systems demonstrate different properties.

Evoloops demonstrated genuine Darwinian evolution of self-reproducing structures inside a deterministic cellular automaton.

Flow-Lenia produces extraordinary localized continuous structures and allows parameters defining different pattern dynamics to exist inside the world itself, producing multispecies systems and measurable emergent evolutionary dynamics.

Genelife adds inheritable genomes to cellular dynamics and has demonstrated continuing genetic and spatial innovation, although its authors explicitly distinguish this from the stronger functional innovation seen in biology.

A 2025 "guideless" Artificial Life model deliberately combines reproduction, development and interactions without relying on a predefined global fitness function or predefined organism morphology.

All of those matter.

But for what we are trying to do, one system stands out.

It is called:

# Outlier

And initially it looks almost absurdly small.

---

# Two states

The universe contains cells.

Every cell is either:

```text
0
```

or:

```text
1
```

Dead or alive if we want convenient terminology.

Although even those words are unnecessary.

We could equally call them:

```text
OFF
ON
```

Each cell examines a `3 × 3` neighborhood:

```text
a b c
d e f
g h i
```

including itself.

Nine bits.

That means:

```text
2⁹ = 512
```

possible neighborhood configurations.

For each one, the rule says:

```text
next state = 0 or 1
```

That's the universe.

No organisms.

No energy.

No genome.

No reproduction function.

No notion of an individual.

No `Life` class.

Just:

```text
binary state
+
local neighborhood
+
transition rule
+
time
```

The original Outlier work describes it as a rotationally symmetric binary two-dimensional cellular automaton using a Moore neighborhood. Its transition function contains 220 live outputs among the 512 possible neighborhoods.

---

# Nobody designed the organism

This distinction matters.

Outlier itself was discovered during an automated search through cellular-automaton rules intended to find dynamics conducive to open-ended evolution.

Self-replication was not explicitly programmed into a candidate organism.

In fact, there was no candidate organism.

The search found a **rule for the universe**.

Then something appeared inside that universe.

![The published Outlier cellular automaton evolving from its tiny seed](/images/books/digital-life/ch10-outlier-growth.gif)

That is much closer to what we want.

Compare:

```text
DESIGNED REPLICATOR

programmer
    ↓
design organism
    ↓
design reproduction mechanism
    ↓
organism reproduces
```

with:

```text
OUTLIER

search discovers local physics
    ↓
local physics runs
    ↓
structures emerge
    ↓
some structures replicate
```

The second case does not prove life.

But it removes an enormous amount of cargo cult.

---

# Start almost from nothing

The published rule can produce interesting behavior from sparse random initial states.

Under appropriate sparse conditions, small shape-changing clusters emerge.

Some clusters produce other clusters.

Some periodically duplicate.

Multiple smaller structures can assemble into larger formations.

Those larger formations can themselves replicate.

And collections of those formations can become boundaries of still larger expanding structures.

So we get something like:

```text
cells
  ↓
clusters
  ↓
replicating formations
  ↓
larger expanding complex
```

That is already strange.

Replication appears at more than one scale.

![Outlier at successive generations from the same initial seed](/images/books/digital-life/ch10-outlier-snapshots.png)

---

# There was still a problem

The original experiments looked like replication.

But we have spent enough of this book learning not to trust appearances.

Imagine:

```text
A appears
```

and later:

```text
A     A
```

Did the first `A` create the second?

Or did the dynamics simply happen to create another identical pattern nearby?

Those are completely different claims.

So in 2026, Arend Hintze and Clifford Bohm returned to Outlier with a much stronger test.

They reconstructed **causal ancestry**.

---

# Who caused whom?

Their idea is exactly the sort of thing we want in this book.

For every new live cell, ask:

> Which cells in the previous state were actually necessary for this cell to appear?

Then connect those dependencies.

At the cell level:

```text
previous cells
     ↓
causal contribution
     ↓
new cell
```

Aggregate those links into clusters:

```text
cluster A
     ↓
cluster B
     ↓
cluster C
```

Now we can construct an ancestry graph.

Not merely:

```text
these patterns look similar
```

but:

```text
this pattern causally contributed
to the existence of that pattern
```

The 2026 study used this framework to reconstruct causal lineages in Outlier and found genuine branching replication: a parent structure could produce multiple causally distinct offspring, which could themselves produce descendants.

Now the claim is considerably stronger.

---

# 433 copies

The 2026 experiment ran Outlier for 20,000 updates on a `1024 × 1024` periodic grid.

The resulting causal ancestry graph contained tens of millions of cluster instances and causal relationships, with nearly a million unique cluster configurations observed during the run.

Take the original seed cluster, called `c0`.

Within the first 10,000 updates the researchers found:

```text
433
```

copies causally descending from that seed.

Interestingly, those copies did not themselves continue the same `c0` lineage indefinitely.

So `c0` replicated, but poorly.

Already we have something useful:

```text
replication
≠
successful lineage
```

---

# Then they found better replicators

Other structures did produce multi-generation branching lineages.

The researchers traced one replicating cluster type called `c2` and found hundreds of replicating instances.

Even more interestingly, additional replicators appeared through debris, collisions and recombinations generated by earlier replicators.

Some surviving structures continued producing descendants despite interference from the surrounding chaotic environment.

Think about what that means.

The world is not doing:

```text
copy parent
```

cleanly.

Instead:

```text
replicator
    ↓
interaction
    ↓
fragments
    ↓
collisions
    ↓
recombination
    ↓
new replicating structures
```

Now we are approaching something much more interesting than crystallization.

---

# The organism may not be connected

Then comes perhaps the most important observation for us.

Some Outlier self-replicators were not one compact connected blob.

They consisted of **multiple spatially separated components whose causal dynamics collectively produced replication**.

The 2026 paper describes this as distributed, multi-component selfhood and argues that it challenges the usual assumption that a self-replicating individual has to be a single connected object.

This connects directly to the question from the previous chapter.

We were already asking whether digital life really needs:

```text
one body
one place
one boundary
```

Outlier gives us experimental evidence that even something as fundamental as a replicator may be **distributed**.

Conceptually:

```text
     A

 B        C

     D
```

may collectively behave as one replicating organization.

The "thing" is in the relationships.

Not necessarily in one body.

---

# This is why Outlier is our starting point

For this book, Outlier has an unusually attractive combination.

It is:

```text
binary

local

deterministic

spatial

minimal

reproducible
```

Yet it supports:

```text
emergent structures

hierarchical organization

causal self-replication

multiple generations

interaction

recombination

distributed individuality
```

The researchers argue that the 2026 causal analysis provides the first complete description of a non-engineered multi-component self-replicator in a two-dimensional discrete cellular automaton, while explicitly encouraging extension of the method to other ALife systems.

That makes it an extraordinary reference point for what we are attempting.

---

# But Outlier is not life

Absolutely not.

At least, the research does not establish that.

We have not demonstrated:

```text
learning

understanding

external information access

deliberate self-modification

cumulative capability acquisition

general-purpose adaptation

knowledge transfer

open-ended functional improvement
```

Nor does self-replication alone establish life.

This is the distinction we need to preserve throughout the book.

Outlier demonstrates something narrower and more useful:

> **Very simple digital physics can spontaneously support causally genuine, distributed, hierarchical self-replication.**

That is already remarkable.

---

# What about Flow-Lenia?

It is tempting to choose Flow-Lenia instead.

Visually, Flow-Lenia is much closer to what we intuitively imagine as an organism.

Its mass-conserving continuous dynamics generate localized structures with complex behaviors, and its rule parameters can themselves become localized within the world's dynamics, allowing multiple kinds of structures to coexist and interact. Researchers have measured emergent evolutionary activity inside the system.

For studying:

```text
morphology
movement
continuous bodies
mass flow
multispecies interactions
```

Flow-Lenia may be the better substrate.

We will absolutely return to it.

But Outlier has one enormous advantage for us.

We can see almost all the machinery.

There are only:

```text
two cell states
512 neighborhood cases
one deterministic transition table
```

No neural network.

No hidden model.

No floating-point organism representation.

No complicated controller.

That makes it a superb first object to reproduce ourselves.

---

# Let's implement it

Even better: the exact rule is published.

The Outlier paper provides the complete `512`-entry rule encoded as a standard cellular-automaton `MAP` string. It also provides a tiny `3 × 3` seed that can reproduce the published dynamics.

The rule is:

```text
ERETQB4eHWkQ7xD4eYZosBQZFixOBHmtFeehExrKVhURLRAqGxeIlSO1JYZP6DRi69rop7TQCkvWTIag7kAS8g
```

And the seed is:

```text
.1.
111
..1
```

That's it.

Let's build the universe.

---

# Decode the rule

A Moore neighborhood has nine cells.

We number them:

```text
256 128  64
 32  16   8
  4   2   1
```

This convention is used by the `MAP` rule representation: every possible `3 × 3` binary neighborhood therefore maps to an integer from `0` through `511`, and the corresponding bit in the 512-entry table gives the next center-cell state.

The published string is Base64 encoding those 512 bits.

```python
import base64

import numpy as np


OUTLIER_MAP = (
    "ERETQB4eHWkQ7xD4eYZosBQZFixOBHmtFeehExrKVhURLRAq"
    "GxeIlSO1JYZP6DRi69rop7TQCkvWTIag7kAS8g"
)


def decode_map_rule(encoded: str) -> np.ndarray:
    """
    Decode a 512-bit LifeViewer/Golly MAP rule.
    """

    padding = "=" * ((4 - len(encoded) % 4) % 4)

    raw = base64.b64decode(encoded + padding)

    bits = np.unpackbits(
        np.frombuffer(raw, dtype=np.uint8)
    )

    if len(bits) < 512:
        raise ValueError("MAP rule contains fewer than 512 bits")

    return bits[:512].astype(np.uint8)
```

Now:

```python
RULE = decode_map_rule(OUTLIER_MAP)
```

is the entire local physics of our universe.

---

# One update

Next we convert every `3 × 3` neighborhood into its corresponding integer.

```python
def outlier_step(
    state: np.ndarray,
    rule: np.ndarray,
) -> np.ndarray:

    nw = np.roll(
        np.roll(state, 1, axis=0),
        1,
        axis=1,
    )

    north = np.roll(state, 1, axis=0)

    ne = np.roll(
        np.roll(state, 1, axis=0),
        -1,
        axis=1,
    )

    west = np.roll(state, 1, axis=1)

    centre = state

    east = np.roll(state, -1, axis=1)

    sw = np.roll(
        np.roll(state, -1, axis=0),
        1,
        axis=1,
    )

    south = np.roll(state, -1, axis=0)

    se = np.roll(
        np.roll(state, -1, axis=0),
        -1,
        axis=1,
    )

    neighborhood = (
          (nw.astype(np.uint16) << 8)
        | (north.astype(np.uint16) << 7)
        | (ne.astype(np.uint16) << 6)
        | (west.astype(np.uint16) << 5)
        | (centre.astype(np.uint16) << 4)
        | (east.astype(np.uint16) << 3)
        | (sw.astype(np.uint16) << 2)
        | (south.astype(np.uint16) << 1)
        |  se.astype(np.uint16)
    )

    return rule[neighborhood]
```

Look carefully at what is missing.

There is no:

```python
replicate()
```

No:

```python
organism()
```

No:

```python
find_child()
```

No:

```python
evolve()
```

Only the transition rule.

---

# Add the seed

The published `c0` seed is:

```python
SEED = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 1],
    ],
    dtype=np.uint8,
)
```

Place it at the center.

```python
def make_world(size: int = 512) -> np.ndarray:

    world = np.zeros(
        (size, size),
        dtype=np.uint8,
    )

    row = size // 2 - 1
    col = size // 2 - 1

    world[
        row:row + 3,
        col:col + 3,
    ] = SEED

    return world
```

Now run it.

```python
RULE = decode_map_rule(OUTLIER_MAP)

world = make_world(512)

for tick in range(5000):

    world = outlier_step(
        world,
        RULE,
    )

    if tick % 100 == 0:
        print(
            tick,
            int(world.sum()),
        )
```

That is our first Outlier implementation.

---

# The real experiment is larger

We should distinguish our teaching implementation from the published experiment.

The 2026 causal study used:

```text
grid       1024 × 1024
boundary   periodic
duration   20,000 ticks
```

with the same seed pattern.

The earlier Outlier work also reports an important size effect: sparse random worlds smaller than roughly `512 × 512` did not produce the larger replicating formations observed in the main experiments.

That immediately tells us something relevant to digital life.

Scale matters.

A phenomenon may not exist at all until the universe is large enough.

---

# And now we have something to steal

Outlier gives us several ideas for Special Creation.

### 1. Do not design the organism

Design or discover:

```text
the universe
```

and let candidate entities form within it.

### 2. Allow multiple scales

Do not assume:

```text
cell
→ organism
```

Perhaps:

```text
cell
→ cluster
→ formation
→ colony
→ superstructure
```

with life-like properties appearing at different levels.

### 3. Do not require connected bodies

An individual may be:

```text
distributed
```

rather than one contiguous structure.

### 4. Track causation

Appearance is not enough.

If we claim reproduction, inheritance or influence, reconstruct:

```text
who actually caused whom
```

### 5. Let interaction generate novelty

Collision and recombination may be more interesting than injecting random mutation from outside.

These are enormously useful lessons.

---

# But we can go further

Outlier knows nothing about the internet.

It cannot read.

It cannot understand a description of itself.

It cannot deliberately run an experiment.

It cannot fork itself into a thousand versions to test alternatives.

It cannot inspect its own rule.

It cannot decide what knowledge should survive.

It cannot combine its knowledge with another lineage.

Those are properties available to the computational substrate we actually care about.

So perhaps Outlier is not the destination.

Perhaps it is the **floor**.

It tells us how much can happen before intelligence enters the system at all.

---

# The closest thing we have

So is Outlier digital life?

We will not make that claim.

Instead:

> **Outlier is one of the strongest current demonstrations that extremely minimal digital physics can spontaneously produce causally genuine, hierarchical and distributed self-replication.**

The 2025 work showed the surprising structures.

The 2026 work showed that the replication was causal rather than merely visual.

And importantly for us, the entire universe can be expressed as:

```text
512 bits of local law
+
one tiny seed
+
space
+
time
```

That is where we're going to begin.

Not with an animal.

Not with hunger.

Not with DNA.

Not with simulated biology.

With one of the strangest things computation has already shown us.

Then we will ask:

> **What is missing?**

And build from there.
