+++
title = "Digital Life 04: When Does a Pattern Become a Thing?"
date = "2026-08-11T01:26:00+01:00"
draft = false
description = "Use Conway's Game of Life to ask whether a persistent moving pattern deserves to be treated as an entity."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Cellular Automata", "Conway's Game of Life", "Glider", "Emergence", "Pattern Identity"]
+++

# Digital Life 04: When Does a Pattern Become a Thing?

Rule 30 gave us structure.

But it did not obviously give us a **thing**.

The pattern expanded.

It changed.

Differences propagated.

Interesting global behavior appeared.

But if I pointed at one region and asked:

> Is that the same object ten generations later?

the answer was not obvious.

So let's change systems.

Not because Conway's Game of Life is more sophisticated.

It isn't.

But because it gives us something Rule 30 does not give us so easily:

> **a localized pattern that persists while moving through space.**

And that creates a much harder question.

---

# Start with five cells

Consider this pattern:

```text id="fthd5q"
.#.
..#
###
```

Five active cells.

Everything else is empty.

Nothing about those five cells says:

```text id="yhvegw"
move diagonally
```

There is no velocity vector.

No direction field.

No object controller.

No code such as:

```python id="9sjsgf"
glider.x += 1
glider.y += 1
```

And yet something happens.

Run Conway's Game of Life.

After several generations, a recognizable version of the pattern appears somewhere else.

![A Game of Life glider moving across a fixed lattice](/images/books/digital-life/ch04-glider.gif)

The pattern moves.

Or does it?

---

# The cells did not move

This is the first important distinction.

In Game of Life, cells occupy fixed positions on a grid.

A cell does not travel from one coordinate to another.

Instead, cells become active or inactive according to their local neighborhood.

So when we say:

> the glider moved one step

the underlying process is more like:

```text id="286ptt"
cells in one region change state
        ↓
new neighboring cells become active
        ↓
old cells disappear
        ↓
a similar organization exists nearby
```

No material object crossed the grid.

The **organization** did.

This should sound familiar.

It is the same conceptual problem we encountered with Lenia.

But now the mechanism is much simpler.

---

# The Game of Life rule

Conway's Game of Life uses a two-dimensional binary grid.

Each cell looks at its eight immediate neighbors.

An active cell remains active if it has two or three active neighbors.

Otherwise it becomes inactive.

An inactive cell becomes active if it has exactly three active neighbors.

That's the entire rule.

Usually written as:

```text id="9l0hfu"
Birth:    3
Survival: 2 or 3
```

or:

```text id="l81gi6"
B3/S23
```

There is no glider rule.

No block rule.

No oscillator rule.

No spaceship rule.

Just:

```text id="47lwfu"
count nearby active cells
        ↓
apply B3/S23
```

Yet many larger structures appear.

---

# Build the rule

A clear implementation is small.

```python id="rx3xse"
import numpy as np


def life_step(state):
    neighbors = (
        np.roll(np.roll(state,  1, axis=0),  1, axis=1)
        + np.roll(state,  1, axis=0)
        + np.roll(np.roll(state,  1, axis=0), -1, axis=1)
        + np.roll(state,  1, axis=1)
        + np.roll(state, -1, axis=1)
        + np.roll(np.roll(state, -1, axis=0),  1, axis=1)
        + np.roll(state, -1, axis=0)
        + np.roll(np.roll(state, -1, axis=0), -1, axis=1)
    )

    born = (state == 0) & (neighbors == 3)
    survive = (state == 1) & ((neighbors == 2) | (neighbors == 3))

    return (born | survive).astype(np.uint8)
```

Again:

```text id="1o7a22"
local state
+
local neighborhood
+
same rule everywhere
```

No global object model.

---

# Put a glider into the world

```python id="fqt9wz"
state = np.zeros((20, 20), dtype=np.uint8)

glider = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
], dtype=np.uint8)

state[2:5, 2:5] = glider
```

Then:

```python id="gzobm2"
for _ in range(4):
    state = life_step(state)
```

After four generations, the glider has reproduced its original orientation one cell diagonally away.

That gives us a natural period:

```text id="djru2n"
4 generations
```

and a displacement:

```text id="e1vbhm"
(+1, +1)
```

This is already stronger than saying:

> it looks like it moved.

We can measure the translation.

---

# But what is the glider?

Here is the strange part.

Suppose we label the active cells at time zero:

```text id="q0o4zs"
A
B
C
D
E
```

Four generations later, most or all of those original active locations are no longer active.

The pattern is composed of different grid cells.

And yet we still say:

> **the glider is over there now.**

So what exactly persisted?

Not the individual active cells.

Not the coordinates.

Not a fixed chunk of material.

What persisted was something closer to:

```text id="i8idp5"
shape
+
phase relationship
+
transition behavior
```

The glider is therefore not naturally identified with the cells currently composing it.

It is identified with a **recurring organization through time**.

---

# Material identity versus pattern identity

This gives us two different ways to define sameness.

## Material identity

Something is the same object because it consists of the same components.

Conceptually:

```text id="cq70mv"
same pieces
=
same thing
```

## Pattern identity

Something is the same because an organization persists, even if the underlying components change.

Conceptually:

```text id="tnht17"
same organization
through transformation
=
same thing
```

The glider strongly favors the second description.

But be careful.

We have not established that every persistent pattern is an entity.

We have only discovered that **material continuity is not required for useful identity in this system**.

That's a more defensible statement.

---

# Measure the center

We can make the idea less philosophical.

Take the active coordinates:

```python id="g1o5d8"
positions = np.argwhere(state == 1)
```

Then compute a centroid:

```python id="ib0ot6"
centroid = positions.mean(axis=0)
```

Track that through time.

For a glider, the centroid moves systematically.

![The measured centroid trajectory of a glider](/images/books/digital-life/ch04-glider-centroid.png)

Now:

> the glider moves

can become:

> the centroid of the localized active pattern changes approximately linearly through time.

Not as poetic.

Much more useful experimentally.

---

# Localized matters

Suppose every cell in the world were active.

That would certainly be a pattern.

But would it be a thing?

Probably not in the same useful sense.

The glider has a property that matters:

> **localization.**

Most of the world is not part of the pattern.

There is a region where activity is concentrated.

We can draw a bounding box around it.

```python id="6ihtpz"
positions = np.argwhere(state == 1)

minimum = positions.min(axis=0)
maximum = positions.max(axis=0)
```

That gives us:

```text id="t8h9zh"
top
bottom
left
right
```

A localized structure can therefore have measurable properties such as:

```text id="lt2han"
area
mass
centroid
velocity
shape
orientation
period
```

Now the word **entity** starts becoming operational rather than purely intuitive.

---

# A block does not move

Game of Life gives us another useful pattern.

```text id="96vraf"
##
##
```

This block remains unchanged.

Generation after generation.

![Fixed, periodic and translating persistence](/images/books/digital-life/ch04-persistence-types.png)

It persists.

But it doesn't move.

So persistence and movement are independent properties.

We now have:

```text id="u4au4z"
block
=
localized
+
persistent
+
stationary
```

and:

```text id="njalkn"
glider
=
localized
+
persistent
+
moving
+
periodic internal transformation
```

Already our vocabulary is becoming more precise.

---

# A blinker changes shape

Now:

```text id="e8m1dg"
###
```

After one update:

```text id="1zuv22"
#
#
#
```

Then back again.

This is a **blinker**.

Its exact shape does not persist from one generation to the next.

Yet its behavior is periodic.

So persistence does not require an unchanging appearance either.

We can have:

```text id="vyt0ri"
state persistence
```

versus:

```text id="6sn713"
dynamic persistence
```

A block persists by remaining unchanged.

A blinker persists by cycling.

A glider persists by cycling **and translating**.

These are different mechanisms producing something we casually call:

> the same pattern continuing to exist.

---

# Persistence has multiple forms

Let's make that explicit.

### Fixed persistence

```text id="cfqcc2"
state(t + 1)
=
state(t)
```

Example:

```text id="84kbdg"
block
```

### Periodic persistence

```text id="mnh5ea"
state(t + p)
=
state(t)
```

for some period `p`.

Example:

```text id="ph8koc"
blinker
```

### Translating persistence

```text id="a45ufi"
state(t + p)
≈
translated(state(t))
```

Example:

```text id="86i6ec"
glider
```

This is much better than one vague word.

Later, continuous systems will make these definitions fuzzier.

Then we will need similarity measures rather than exact equality.

But Game of Life gives us a clean laboratory first.

---

# What if we shift the glider?

Suppose the glider at time zero occupies one location.

Then after four generations it occupies the same pattern translated by:

```text id="s5jki5"
(+1, +1)
```

If we compare the raw grids directly:

```python id="k1jl6n"
np.array_equal(state_t0, state_t4)
```

the result is:

```text id="a9df80"
False
```

But if we compensate for translation:

```python id="c7ge5m"
shifted = np.roll(
    np.roll(state_t0, 1, axis=0),
    1,
    axis=1,
)
```

then the local patterns match.

So whether something counts as persistent depends on what transformations we consider irrelevant.

That is a deep experimental issue.

Do we care about:

```text id="ug7hog"
exact position?
orientation?
scale?
phase?
internal state?
```

Different questions imply different notions of identity.

---

# Identity requires invariants

We can think of identity as something that survives allowed transformations.

For the glider, position is not invariant.

The individual cells are not invariant.

The exact intermediate geometry is not invariant.

But something else is.

After every four generations:

```text id="ua9fru"
same local configuration
+
fixed displacement
```

That relationship is stable.

So one operational definition of glider identity might be:

> a localized pattern whose state recurs after a fixed period up to spatial translation.

Now we have something testable.

---

# The danger of naming things

The Game of Life community has names for many patterns:

```text id="vk75y2"
block
blinker
beacon
glider
lightweight spaceship
pulsar
gun
```

Naming is useful.

It lets us reason at a higher level.

Instead of describing dozens of coordinates, we say:

> glider.

But naming creates another danger.

Once we give a pattern a noun, our minds start treating it as an object automatically.

The noun does not prove the ontology.

Calling something a spaceship does not make it a machine in the biological or engineering sense.

This book will repeatedly exploit names for convenience while refusing to confuse them with evidence.

---

# Can patterns interact?

Now put two structures in the same world.

Depending on their trajectories, they may:

```text id="0m3yxx"
pass
collide
destroy each other
produce debris
produce another recognizable pattern
```

![Two localized Game of Life patterns interacting](/images/books/digital-life/ch04-collision.gif)

This matters because entity-like descriptions become more useful when patterns have identifiable consequences for one another.

We can now ask:

```text id="rnq95n"
Did A alter B?

Did both survive?

Was a new localized pattern produced?

Was information transferred?

Was the outcome predictable from isolated behavior?
```

Interaction gives us another layer.

But we're still not ready to call any of this life.

---

# A glider carries information

There is another way to look at it.

A glider begins in one region.

Later, a recognizable structure appears elsewhere.

Something about the earlier state influenced the later distant state.

The pattern therefore propagates information through the grid.

We don't have to anthropomorphize it.

We can say:

```text id="r3edlh"
localized state
        ↓
repeated local transformation
        ↓
localized correlated state elsewhere
```

This is one reason gliders are useful in computational constructions built inside Game of Life.

Patterns can act as signals.

But that's the next level of the argument.

For now, the important point is:

> persistence can carry organization through space and time.

---

# So is the glider a thing?

We can finally return to the question.

Biologically?

We have shown nothing close to enough.

Philosophically?

You can argue about it forever.

Experimentally?

We can say something precise.

A glider is:

* localized,
* dynamically persistent,
* periodic,
* translating,
* reproducible,
* describable independently of the exact grid cells currently composing it.

That is enough to justify treating it as a **pattern-level entity for analysis**.

Notice the wording.

Not:

> the glider is alive.

Not even:

> the glider is objectively an organism.

Instead:

> treating the glider as an entity is useful because measurable properties remain coherent across its transformation.

That is a bounded claim.

---

# Now we have something we can hurt

Rule 30 gave us distributed structure.

The glider gives us a localized persistent pattern.

That means we can finally perform a nastier experiment.

We can remove part of it.

We can alter one of its cells.

We can collide it with something.

Then ask:

```text id="91t6ju"
Does the pattern survive?

Does it remain recognizable?

Does it return to its previous organization?

Does it become something else?

Does it disappear?
```

And that gives us our next important distinction:

```text id="r1rswn"
persistence
≠
robustness
≠
regeneration
```

A pattern surviving in an undisturbed world tells us much less than a pattern surviving disturbance.

So next, we stop admiring the patterns.

We damage them.

Next: **Kill It.**
