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

{{< figure
    src="/images/books/digital-life/ch01-lenia-organism.gif"
    alt="A localized continuous cellular automaton pattern evolving and moving through time."
    caption="One state of a continuous cellular automaton evolving through time."
>}}

Something is moving.

It appears to have a boundary.

Different parts of it seem to behave differently.

Its shape changes as it travels, yet some larger organization survives those changes.

If you watched it without context, you could easily reach for biological language.

A cell.

A creature.

An organism.

Perhaps even an animal.

That reaction is useful.

But don't trust it.

---

# Your brain has already invented an object

Before we know anything about the mechanism, we have probably done something like this:

```text
pattern
↓
persistent pattern
↓
moving persistent pattern
↓
thing
↓
creature
````

Notice how quickly that happened.

Nothing in the simulation announced:

```text
I AM AN OBJECT
```

Nothing told us where the supposed body begins or ends.

Nothing told us that the pattern at one moment is the same individual as the pattern several moments later.

We inferred all of that.

That is the mystery we are going to begin with.

Not:

> Is this alive?

That question is much too large.

The first question is smaller:

> **Why does this look so much like a thing at all?**

---

# What exactly are you looking at?

There is no little creature hidden inside the simulation.

There is no object containing:

```python
creature.move()
creature.turn()
creature.keep_shape()
```

There is no animation path specifying where it should travel.

No skeleton.

No muscles.

No controller deciding:

```text
keep the left side attached
move the front forward
bend here
restore the outline
```

At the level that matters to us, there is something much simpler:

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

The thing you perceive as an object is an **ongoing organization in that process**.

That distinction will matter throughout this book.

---

# Meet Lenia

The family of systems we are looking at is called **Lenia**.

Lenia is a continuous cellular automaton.

Unlike a binary cellular automaton, where a cell may be only:

```text
0
or
1
```

Lenia uses continuously varying state.

The original Lenia work reported hundreds of recurring forms found through exploration of the system.

The paper refers to these patterns as *lifeforms*.

We are going to be more cautious.

For now, call them:

> **persistent localized patterns**

That gives us something we can investigate without deciding what they are.

They occupy regions of space.

They change.

Some persist.

Some move.

Some deform.

Some disappear.

Those are observations.

"Alive" would be an interpretation.

---

# There is no creature variable

Consider what is not represented explicitly.

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
head
tail
left_leg
right_leg
```

The word `creature` does not have to occur anywhere in the mechanism.

Instead we have something more like a field:

```text
0.00  0.00  0.01  0.04  0.08
0.00  0.03  0.18  0.42  0.27
0.01  0.14  0.61  0.83  0.39
0.00  0.09  0.47  0.64  0.21
0.00  0.01  0.08  0.11  0.03
```

Each location is updated according to the state around it.

Yet when those numbers evolve, we perceive something larger than the individual values.

A coherent structure appears.

It may travel across the grid even though the grid locations themselves never move.

That gives us an important possibility:

> **An apparent entity may persist as organization rather than as a fixed collection of material.**

Notice the wording.

May.

We have not yet earned:

```text
entity
```

But we have found a question worth pursuing.

---

# What is actually moving?

Look again at the animation.

{{< figure
    src="/images/books/digital-life/ch01-lenia-fixed-grid-motion.png"
    alt="Four frames of a Lenia structure moving across a fixed coordinate grid while the lattice remains stationary."
    caption="The pattern moves across the field while the underlying lattice remains fixed."
>}}

Suppose the pattern travels from left to right.

The grid does not move.

The individual locations in the grid do not travel with it.

Instead:

```text
state here
↓
changes nearby state
↓
new organization appears slightly to the right
↓
that organization changes nearby state
↓
organization appears farther right
```

So when we say:

> the creature moved

the underlying description is closer to:

> **a recognizable organization of state was repeatedly reconstructed at changing spatial coordinates**

Those descriptions refer to the same visual event at different levels.

One is intuitive.

One is operational.

We will need both.

But we must know when we have crossed from one into the other.

---

# Is a wave a thing?

This problem is not unique to artificial life.

Consider a wave crossing water.

The water molecules do not travel across the ocean with the wave.

The organization does.

Consider a flame.

Its constituent matter is continually changing.

Yet we comfortably refer to:

> the flame

Now consider our Lenia pattern.

Its local state is continually changing.

Nevertheless something remains recognizable.

Perhaps identity does not require preserving the same material.

Perhaps persistence of organization is enough.

Or perhaps we are simply very good at seeing objects where no useful object exists.

Both possibilities remain open.

The mistake would be deciding from the animation alone.

---

# The most dangerous word may be "it"

Look at the sentences we have already used:

> It moved.

> It changed shape.

> It persisted.

The word **it** is doing a lot of work.

Before we can say that something persists, we need some rule for deciding that:

```text
pattern at t
```

and:

```text
pattern at t + 1
```

are instances of the same continuing organization.

That might be based on:

```text
shape similarity
location
causal continuity
internal structure
trajectory
```

or something else entirely.

We do not know yet.

For now, visual continuity is enough to generate the question.

It is not enough to settle it.

Later in this book we will discover why this matters.

A connected shape may not always be the right boundary of a digital individual.

Several disconnected structures may participate in one causal process.

Two identical-looking structures may have completely different histories.

So our first intuition about "the thing" is deliberately provisional.

---

# It gets more convincing

Lenia was only the beginning.

Later work expanded the basic system through additional dimensions, kernels and channels, producing increasingly elaborate localized dynamics.

Some reported patterns appear to:

```text
move
change morphology
interact
emit structures
produce similar structures
```

Again, the language matters.

If something produces another similar pattern, we can say:

```text
a second similar pattern appeared
```

We should not immediately jump to:

```text
reproduction
```

because reproduction is a causal claim.

If one region behaves differently from another, we can say:

```text
different regions exhibit different dynamics
```

We should not silently turn those regions into:

```text
organs
```

The recurring distinction is:

```text
WHAT HAPPENED
```

versus:

```text
WHAT WE CALL WHAT HAPPENED
```

Artificial life becomes much more interesting once we stop pretending those are the same thing.

---

# Then came Flow-Lenia

Lenia also raises another issue.

Its ordinary dynamics do not require conservation of the quantity represented in the field.

State can increase or decrease under the update rule.

A later system called **Flow-Lenia** changes that.

Flow-Lenia introduces mass-conserving dynamics.

Instead of allowing state simply to appear or disappear through the ordinary Lenia growth process, the system transports the field while conserving total mass.

Conceptually, ordinary growth-like dynamics can permit something like:

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

A conserving system instead forces us toward:

```text
something here
      ↓
something somewhere else
```

Material has to go somewhere.

That gives us a useful example of how **one constraint can change the questions we are able to ask**.

---

# Follow the material

Imagine this toy field:

```text
0 0 0 0 0
0 0 3 0 0
0 2 5 2 0
0 0 3 0 0
0 0 0 0 0
```

Its total is:

```text
3 + 2 + 5 + 2 + 3 = 15
```

After an update, the distribution might change:

```text
0 0 1 0 0
0 2 3 1 0
0 1 2 3 0
0 0 2 0 0
0 0 0 0 0
```

but the total could remain:

```text
15
```

These numbers are illustrative, not a literal Flow-Lenia update.

The important point is the constraint:

```text
shape changes
position changes
internal distribution changes

but

total material remains constrained
```

Now new questions become possible.

If a structure grows here:

> Where did that material come from?

If two structures collide:

> Where did their state go?

If one expands while another disappears:

> Did material transfer between them?

Conservation gives us fewer places to hide sloppy interpretations.

That is useful.

---

# But conservation is not life either

This is important.

It would be easy to say:

> Ah. Now we have something more biological because mass is conserved.

But remember the rule from Chapter 00.

We do not add a biological-looking mechanism and then declare victory.

Mass conservation is interesting because it imposes a measurable constraint.

It may change what kinds of stable structures can exist.

It may change how interactions work.

It may make some interpretations easier to test.

But:

```text
mass conservation
≠
metabolism
≠
organism
≠
life
```

We are studying consequences.

Not awarding biological labels.

---

# There is still no creature

Even in Flow-Lenia, we do not begin with:

```python
class Organism:
    energy: float
    position: Vector2
    velocity: Vector2
    genome: Genome
```

We still begin with a field and update dynamics.

Then localized organization appears.

The direction of explanation is backwards compared with ordinary object-oriented software.

Normally:

```text
programmer defines object
        ↓
object produces behavior
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

That reversal is one of the reasons artificial life is so compelling.

And so dangerous.

Because the object appears to us before we know whether our object boundary means anything.

---

# Don't fall in love with the animation

Humans are extremely willing to see agency.

Something moves toward something else:

> It wants it.

Something moves away:

> It is afraid.

Something restores its shape:

> It healed.

Something produces a similar structure:

> It reproduced.

Several structures travel together:

> They are flocking.

Something persists:

> It wants to survive.

None of those conclusions follows automatically from the image.

A beautiful animation can produce a terrible scientific argument.

So throughout this book we will keep two descriptions side by side.

## The tempting description

```text
It moves.

It eats.

It heals.

It competes.

It reproduces.

It flocks.
```

## The operational description

```text
Its centroid changes.

State transfers between localized regions.

Similarity to an earlier morphology increases after perturbation.

One pattern changes the future persistence of another.

A second pattern satisfying a defined similarity criterion appears.

Nearby velocity vectors show directional correlation.
```

The first language helps us notice interesting phenomena.

The second gives us something to measure.

Neither should silently replace the other.

---

# Try to kill the interpretation

Suppose the animation appears to show healing.

Don't write:

> It heals.

Damage it.

{{< figure
    src="/images/books/digital-life/ch01-lenia-damage-triptych.png"
    alt="A Lenia pattern before perturbation, immediately after damage, and at a later time."
    caption="Before, perturbation, and a later state. We have not yet earned the word healed."
>}}

Several things could happen.

## Outcome A — collapse

```text
structure
   ↓
damage
   ↓
disintegration
```

## Outcome B — persistence without recovery

```text
structure
   ↓
damage
   ↓
altered persistent structure
```

## Outcome C — structural return

```text
structure
   ↓
damage
   ↓
temporary disruption
   ↓
later morphology resembles prior morphology
```

Only the third case even gives us a reason to investigate regeneration.

And then we still have to ask:

```text
How much damage?

Compared with what control?

How similar is the later structure?

How long does recovery take?

Does recovery occur from different damage locations?

Does it work repeatedly?

Would the same morphology have returned without the perturbation?
```

The animation gives us the hypothesis.

The experiment has to do the rest.

---

# This book begins at the wrong end

Most explanations of cellular automata begin with the machinery.

A cell.

A neighborhood.

A rule.

Perhaps Conway's Game of Life.

Eventually, after enough explanation, they show you something like Lenia.

We are going to do the opposite.

We started with the spectacle because this is the mystery we actually care about.

Something disturbingly creature-like can arise from repeated local transformations over a field.

Our eyes immediately invent:

```text
body
identity
motion
agency
```

Now we are going to remove almost everything that made the spectacle convincing.

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

If all the mystery depends on the elaborate machinery of systems such as Lenia, then stripping that machinery away should destroy it.

That is our next experiment.

Because before we ask what digital life might be, we need to answer something simpler:

> **How little computation is required before our intuition starts seeing organization?**

Next: **Remove Almost Everything.**

---

## What survived this chapter?

**What we saw**

Localized patterns can move, deform and persist in systems built from repeated local field updates.

**What we are tempted to say**

Creatures exist and move through the simulation.

**What we can currently claim**

Recognizable localized organization can persist while the underlying state changes.

**What remains unresolved**

Whether the apparent pattern deserves to be treated as an individual entity at all.

**What we do next**

Remove almost every mechanism that made the phenomenon look life-like.

---

## Sources

This chapter draws primarily on Bert Wang-Chak Chan's original **Lenia — Biology of Artificial Life**, the later **Lenia and Expanded Universe**, and Plantec and colleagues' work on **Flow-Lenia** and its mass-conserving, parameter-localized extension.
