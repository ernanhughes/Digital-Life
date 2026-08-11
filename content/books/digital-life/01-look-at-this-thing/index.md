+++
title = "Digital Life 01: Look at This Thing"
date = "2026-08-11T01:06:00+01:00"
draft = false
description = "Before we learn how artificial life works, look at what a few local rules can already produce."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Lenia", "Flow-Lenia", "Cellular Automata", "Emergence"]
+++

# Digital Life 01: Look at This Thing

Don't read anything yet.

Watch this.

<!--
TODO VISUAL:
Full-width animated Lenia or Flow-Lenia organism.

Prefer:
- localized organism
- visible locomotion or deformation
- no explanatory labels
- dark/neutral background
- several seconds of uninterrupted motion

Caption should initially be minimal:
"One state of a continuous cellular automaton evolving through time."
-->

Something is moving.

It appears to have a boundary.

Different parts of it seem to behave differently.

Its shape changes as it travels, yet some larger organization survives those changes.

If you watched it without context, you could easily reach for biological language.

A cell.

A creature.

An organism.

Maybe even an animal.

That reaction is useful.

But don't trust it.

---

## What exactly are you looking at?

There is no little creature hidden inside the simulation.

There is no object with code resembling:

```python
creature.move()
creature.turn()
creature.keep_shape()
```

There is no animation path telling it where to travel.

There is no skeleton.

No muscles.

No collision controller deciding how the body should deform.

At the level that matters to us, there is a spatial field of values and a rule repeatedly transforming that field.

Something closer to:

```text
current field
      ↓
local interaction
      ↓
local response
      ↓
next field
```

Again.

And again.

And again.

The thing you perceive as an object is an **ongoing pattern in that process**.

That distinction will matter throughout this book.

---

# Meet Lenia

The family of systems we are looking at is called **Lenia**.

Bert Wang-Chak Chan introduced Lenia as a continuous cellular automaton: rather than restricting cells to states such as dead or alive, the state varies continuously, and the local update process is generalized accordingly. The original work reported more than 400 identified recurring forms across 18 families, many found through interactive evolutionary search.

The paper calls these patterns *lifeforms*.

We are going to be more cautious.

For now, call them:

> **persistent localized patterns.**

That phrase tells us something we can investigate without deciding what they *are*.

They occupy a region of space.

They have structure.

They change through time.

Some persist.

Some move.

Some deform.

Some disappear.

Those are observations.

"Alive" would be an interpretation.

---

## This is already strange

Consider what isn't represented explicitly.

There is no variable containing:

```text
position_of_creature
```

No variable containing:

```text
creature_outline
```

No object containing:

```text
left_leg
right_leg
head
tail
```

Indeed, the word `creature` does not have to occur anywhere in the mechanism.

Instead, there is something like a field:

```text
0.00  0.00  0.01  0.04  0.08
0.00  0.03  0.18  0.42  0.27
0.01  0.14  0.61  0.83  0.39
0.00  0.09  0.47  0.64  0.21
0.00  0.01  0.08  0.11  0.03
```

and each location is updated according to its surrounding field.

Yet when those numbers evolve, we perceive something larger than the numbers.

A coherent structure appears.

That structure can move through the grid even though individual locations in the grid remain exactly where they are.

Already we have encountered one of the deepest ideas in this book:

> **An entity can potentially be represented by persistence of organization rather than persistence of material.**

We have not proved that the Lenia pattern deserves to be called an entity.

But now we have a question worth investigating.

---

# It gets worse

The original Lenia system was only the beginning.

Later work generalized Lenia into higher dimensions, multiple kernels and multiple channels. Those experiments reported phenomena including self-replication, emission, ingestion-like growth and patterns with differentiated internal regions.

Again, be careful with those words.

If something copies itself, we have observed copying.

Whether that deserves to be called reproduction will require a stronger test.

If one region behaves differently from another, we have differentiated dynamics.

Calling those regions organs would add an interpretation we have not yet earned.

This difference between:

```text
what happened
```

and:

```text
what we call what happened
```

is going to become increasingly important.

---

# Then came Flow-Lenia

There was another problem.

Ordinary Lenia can create remarkable localized structures, but its dynamics do not impose conservation of the material represented in the field.

Values can grow and disappear according to the growth rule.

That makes some biological analogies particularly tempting and particularly dangerous.

A newer system called **Flow-Lenia** changes this assumption.

Flow-Lenia is a mass-conserving extension of Lenia. Instead of allowing state simply to appear or disappear through the usual Lenia growth process, the update mechanism transports the field while conserving its total mass. The system was also designed so that rule parameters can become localized within the dynamics rather than existing only as one global external rule.

That sounds like a small technical adjustment.

It isn't.

Consider the difference.

Ordinary growth-like dynamics can effectively do:

```text
nothing
  ↓
something
```

or:

```text
something
  ↓
nothing
```

A mass-conserving system has to do something more like:

```text
something here
     ↓
something somewhere else
```

Material has to move.

---

## Follow the material

Imagine this simplified field:

```text
0 0 0 0 0
0 0 3 0 0
0 2 5 2 0
0 0 3 0 0
0 0 0 0 0
```

Suppose its total mass is:

```text
3 + 2 + 5 + 2 + 3 = 15
```

After an update, the shape might become:

```text
0 0 1 0 0
0 2 3 1 0
0 1 2 3 0
0 0 2 0 0
0 0 0 0 0
```

but the total remains:

```text
15
```

The numbers above are illustrative, not Flow-Lenia itself.

The important idea is conservation:

```text
shape changes
position changes
internal distribution changes

but

total material remains constrained
```

That one constraint changes the kind of questions we can ask.

If a structure grows somewhere, where did that material come from?

If two structures collide, how is their material redistributed?

If one structure dominates another, what actually happened to the state that composed the losing structure?

The simulation starts giving us fewer places to hide sloppy biological metaphors.

That's useful.

---

# There is still no creature

This is worth repeating.

Even in Flow-Lenia, we do not begin with:

```python
class Organism:
    energy: float
    position: Vector2
    velocity: Vector2
    genome: Genome
```

We begin with a field and local dynamics.

Then spatially localized structures emerge from it.

Researchers have demonstrated Flow-Lenia configurations containing complex localized patterns and have optimized update-rule parameters to produce behaviours of interest. More recent experiments also examine evolutionary activity within the system rather than merely displaying visually interesting patterns.

The direction of explanation is therefore unusual.

In ordinary software:

```text
programmer defines object
        ↓
object produces behaviour
```

Here:

```text
programmer defines local dynamics
        ↓
dynamics unfold
        ↓
localized organization appears
        ↓
we decide whether "object" is a useful description
```

That reversal is one of the reasons artificial life is so interesting.

---

# What is doing the moving?

Look again at the animation.

<!--
TODO VISUAL:
Second sequence.

Three or four frames of the same organism moving.

Overlay either:
- fixed grid coordinates, or
- a highlighted stationary patch of grid.

Purpose:
make clear that the lattice does not move while the pattern does.
-->

Suppose the structure moves from left to right.

The grid does not move.

Individual grid locations do not travel with the structure.

The pattern at one location alters nearby state.

Those altered neighborhoods alter the next state.

The organization reappears slightly displaced.

Then again.

And again.

So when we say:

> **the creature moved**

the underlying description is more like:

> **a recognizable organization of state was repeatedly reconstructed at changing spatial coordinates.**

Those two descriptions refer to the same observation at different levels.

One feels biological.

One feels mechanical.

We need both.

But we should know when we have switched between them.

---

# Is a wave an object?

This problem isn't unique to artificial life.

Consider a wave travelling across water.

The water molecules do not travel across the ocean with the wave.

The organization does.

Or consider a flame.

Its constituent molecules continually change.

Yet we have no difficulty referring to:

> the flame.

Now consider the thing on our screen.

Its underlying state is continually changing.

Nevertheless, something remains recognizable through time.

Perhaps identity does not always require keeping the same material.

Perhaps persistence of organization can sometimes be enough.

Or perhaps we are just very good at seeing objects where none exist.

Both possibilities remain open.

We'll test them.

---

# Don't fall in love with the animation

This is where artificial life can deceive us.

Humans are exceptionally willing to see agency.

Something moves toward something else:

> It wants it.

Something avoids something:

> It is afraid.

Something restores its shape:

> It healed.

Something produces a copy:

> It reproduced.

Something persists:

> It wants to survive.

None of those conclusions follows automatically from the image.

A beautiful animation can produce a terrible scientific argument.

So throughout this book we will keep two descriptions side by side.

### The tempting description

```text
It moves.

It eats.

It heals.

It competes.

It reproduces.
```

### The operational description

```text
Its centroid changes.

Mass transfers between localized regions.

Similarity to a prior morphology increases after perturbation.

One pattern changes the future persistence of another.

A second pattern satisfying a defined similarity criterion appears.
```

The first language helps us notice interesting phenomena.

The second gives us something to measure.

Neither should silently replace the other.

---

# Now damage it

Suppose we remove part of the pattern.

<!--
TODO VISUAL:
before → damage → after

Do NOT label the last frame "healed".

Label:
t = 0
perturbation
t = N
-->

Several things could happen.

### Outcome A

It collapses.

```text
structure
   ↓
damage
   ↓
disintegration
```

### Outcome B

It survives but remains damaged.

```text
structure
   ↓
damage
   ↓
altered persistent structure
```

### Outcome C

Its later state becomes similar to its earlier organization.

```text
structure
   ↓
damage
   ↓
temporary disruption
   ↓
structural recovery
```

Only the third case even gives us a reason to investigate regeneration.

And even then we need questions:

```text
How much damage?

Recovery compared with what?

How similar is the recovered structure?

How long does recovery take?

Does it work from different damage locations?

Does it work repeatedly?
```

The animation gives us the hypothesis.

The experiment has to do the rest.

---

# This book begins at the wrong end

Most explanations of cellular automata begin with a cell.

Then a neighborhood.

Then a rule.

Then perhaps Conway's Game of Life.

Eventually, after enough machinery, they show you systems like Lenia.

We are going to do the opposite.

We started here because this is the mystery we actually care about.

Something that looks disturbingly creature-like can arise from repeated local transformations over a field.

Now we are going to remove almost all of it.

Take away:

```text
continuous state
two dimensions
smooth kernels
large neighborhoods
multiple parameters
mass transport
creature-like morphology
```

Keep reducing until almost nothing remains.

Our target is this:

```text
000000000010000000000
```

One line.

Two possible states.

One active cell.

A neighborhood of three cells.

One tiny deterministic rule.

If the apparent complexity of systems such as Lenia depends on all their elaborate machinery, then stripping that machinery away should destroy the mystery.

That's our next experiment.

Because before we ask how close computation can get to life, we need to answer something simpler:

> **How little computation is required before unexpected organization begins to appear?**

Next: **Remove Almost Everything.**

---

## Sources

This chapter draws primarily on Bert Wang-Chak Chan's original **Lenia — Biology of Artificial Life**, the later **Lenia and Expanded Universe**, and Plantec and colleagues' work on **Flow-Lenia** and its mass-conserving, parameter-localized extension.
