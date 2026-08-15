+++
title = "02: Look at This Thing"
date = "2026-08-14T09:30:00+01:00"
draft = false
description = "Calibrating the microscope. A continuous cellular automaton produces something that looks disturbingly like a creature; we strip the machinery away until almost nothing remains, and find that the temptation survives the reduction."
weight = 2
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Lenia", "Cellular Automata", "Rule 30", "Conway's Game of Life", "Glider", "Pattern Identity", "Emergence"]
+++

Don't read anything yet.

Watch this.

{{< figure
    src="/images/books/digital-life/ch01-lenia-organism.gif"
    alt="A localized continuous cellular automaton pattern evolving and moving through time."
    caption="One state of a continuous cellular automaton evolving through time."
>}}

Something is moving.

It appears to have a boundary. Different parts of it seem to behave differently — an edge that ripples, an interior that stays denser, a leading region that seems to pull the rest along. Its shape changes as it travels, and yet some larger organization survives those changes. Watch it for thirty seconds and you will start predicting what it is about to do.

If you saw this without context, biological language would arrive immediately.

A cell. A creature. An organism. Perhaps even an animal.

That reaction is useful. It is also the first thing this book has to take apart.

---

## Your Brain Has Already Invented an Object

Before knowing anything about the mechanism, most of us have already run through something like this:

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
```

Notice how fast that happened, and notice how little was required to trigger it. Nothing in the simulation announced `I AM AN OBJECT`. Nothing marked where the supposed body begins or ends. Nothing certified that the pattern visible at one moment is the same individual as the pattern visible several moments later.

We supplied all of that.

So the first question of this book is not *is this alive?* — that question is far too large to be useful yet. The first question is much smaller, and much more answerable:

> **Why does this look so much like a thing at all?**

---

## There Is No Creature Variable

Start with what is not in the program.

There is no object exposing `creature.move()` or `creature.keep_shape()`. There is no animation path, no skeleton, no set of joints, no controller issuing instructions like *keep the left side attached, push the front forward, restore the outline*. There is no variable called `position_of_creature`, and no field named `head` or `tail`.

What exists is closer to a grid of numbers:

```text
0.00  0.00  0.01  0.04  0.08
0.00  0.03  0.18  0.42  0.27
0.01  0.14  0.61  0.83  0.39
0.00  0.09  0.47  0.64  0.21
0.00  0.01  0.08  0.11  0.03
```

Each location holds a value. At every step, each location is updated according to the values around it, using the same law everywhere. That is the whole mechanism:

```text
current field
      ↓
local interaction
      ↓
local response
      ↓
next field
```

Again, and again, and again.

The family of systems this figure comes from is called **Lenia** — a continuous cellular automaton in which each location holds a value between `0` and `1`, and interacts with a smooth weighted neighbourhood.

Lenia is famous precisely because many of the resulting patterns are extraordinarily easy to describe in biological language.

We will resist that language for now.

What we have actually observed is:

> **a persistent localized pattern**

That description is less exciting.

It is also something we can test.

They occupy regions of space. They change. Some persist, some move, some deform, some disappear. Those are observations, and we can make more of them whenever we like.

*Alive* would be an interpretation, and nothing so far has earned it.

The direction of explanation here is worth pausing on, because it runs backwards compared with ordinary software. Normally a programmer defines an object and the object then produces behaviour. Here:

```text
programmer defines local dynamics
        ↓
dynamics unfold
        ↓
localized organization appears
        ↓
we decide whether "object" is a useful description
```

That reversal is a large part of why artificial life is so compelling.

It is also why it is so easy to fool ourselves.

The object appears first in our perception. Only afterwards do we begin asking whether anything in the mechanism justifies treating that apparent boundary as a real unit of organization.

---

## What Is Actually Moving?

Look at the pattern travelling left to right.

{{< figure
    src="/images/books/digital-life/ch01-lenia-fixed-grid-motion.png"
    alt="Four frames of a Lenia structure moving across a fixed coordinate grid while the lattice remains stationary."
    caption="The pattern moves across the field while the underlying lattice remains fixed."
>}}

The grid does not move. The individual locations do not travel. Location (40, 17) is exactly where it always was, holding whatever value the update rule most recently assigned it. Nothing is transported.

What happens instead is a chain of local reconstruction. State at one location influences nearby updates; a recognizable organization appears slightly farther over; those states influence the next updates; the recognizable organization appears farther over again.

Nothing corresponding to the visible creature has travelled through the grid.

The organization has propagated.

So when we say *the creature moved*, the operational description is:

> **a recognizable organization of state was repeatedly reconstructed at changing spatial coordinates**

Those two sentences describe the same visual event at different levels. One is intuitive and useful for noticing things. The other is operational and useful for measuring things. We will need both, all the way through this book. What matters is knowing, at any moment, which one we are using.

This is not a quirk of artificial life. A wave crosses the ocean without the water crossing the ocean. A flame persists while its constituent matter is continuously replaced, and nobody finds *the flame* a controversial noun. So there is a genuinely open possibility here — that identity does not require preserving the same material, and that persistence of organization is enough.

There is also a second possibility, equally open: that we are simply very good at seeing objects where no useful object exists.

The mistake would be deciding between them from the animation.

---

## The Most Dangerous Word Is "It"

Look at the sentences already used in this chapter.

> It moved. It changed shape. It persisted.

The word **it** is carrying an enormous amount of unearned weight. Before saying that something persists, we need a rule for deciding that the pattern at time *t* and the pattern at time *t+1* are instances of the same continuing organization. That rule might be based on shape similarity, or location, or trajectory, or internal structure, or causal continuity, or something we have not thought of.

We do not have that rule yet. Visual continuity is enough to raise the question. It is nowhere near enough to settle it.

This matters more than it currently appears to.

What if connected geometry eventually turns out not to be the correct boundary?

What if two identical-looking structures have different histories?

What if one continuing process occupies several disconnected regions?

We do not know yet.

So our first definition of "the thing" will remain deliberately provisional. We will use geometry while it works, and replace it if the experiments force us to.

A discipline that helps: keep two descriptions of the same event side by side.

**The tempting description**

```text
It moves.
It eats.
It heals.
It competes.
It reproduces.
It flocks.
```

**The operational description**

The left-hand column is how we notice phenomena worth investigating, and abandoning it would make us worse scientists, not better ones. The right-hand column is what we can actually test. Neither should quietly replace the other, and the failure mode of this entire field is the moment the first column starts getting reported as though it were the second.

Flow-Lenia makes the example even more interesting by adding a conservation constraint: rather than allowing field quantity simply to appear or disappear, it redistributes it through the system.

That changes what we can ask. If a structure grows, there is now something meaningful to trace. If two structures collide, redistribution can be measured.

But conservation does not make the system more alive.

It makes the experiment better constrained.

That distinction — between adding a constraint that improves what we can measure and adding a property we wish to call life-like — will matter throughout the book.

---

## Now Take Almost Everything Away

Most treatments of this material start with the machinery — a cell, a neighbourhood, a rule, perhaps Conway's Game of Life — and work up to systems like Lenia as a reward at the end.

We are going the other way, and the reason is experimental rather than stylistic.

We have a mystery: repeated local transformations over a field produce something our perception insists on treating as a creature. The obvious hypothesis is that the mystery depends on the elaborate machinery. Continuous state. Two-dimensional geometry. Smooth kernels. Large neighbourhoods. Multiple parameters. Organism-like morphology.

If that hypothesis is right, stripping the machinery away should destroy the effect.

So let us strip it away, aggressively, and see what happens.

```text
continuous state       →  two states: 0 and 1
two dimensions         →  one line
large neighbourhood    →  three cells
smooth growth response →  an eight-entry lookup table
many parameters        →  one number
elaborate seed         →  a single active cell
```

Each of those removals is deliberate. The states become binary, so nothing can hide in the decimals — and we will avoid calling them *alive* and *dead*, because those names smuggle in the conclusion. The world becomes a single line, so there is no north, no south, no morphology, none of the geometry that made the previous section feel organism-like. Each location can see only its left neighbour, itself, and its right neighbour: that is its entire universe, and anything it ever learns about the wider world has to arrive through repeated local interaction.

With three binary neighbours there are only eight possible local situations. The entire law of this universe is therefore eight output bits.

One example is:

Now give it almost nothing to work with.

One active cell in an otherwise empty line.

No population. No agent. No memory. No objective. No fitness function. No hidden machinery waiting to unfold.

Then let the same tiny rule repeat through time, stacking each successive state underneath the last.

![Rule 22 spacetime diagram](/images/books/digital-life/ch02-rule22-spacetime.png)

Structure appears.

---

## Two Things That Picture Is Not

Before we react to it, two corrections — both of which are small here and will be large later.

Two cautions matter.

First, this is not a two-dimensional object. Horizontal position is space; vertical position is time. We have turned a history into a picture. Nothing is moving downward.

Second, the rule number does not specify the entire experiment. Initial state, boundary conditions, world size and update procedure all matter.

So instead of saying:

> Rule 22 does this.

the more honest description is:

> **Under this experimental configuration, Rule 22 produced this history.**

That qualification seems fussy now.

Later it will become essential.

So whenever we are tempted to write *Rule X does Y*, the honest statement is:

> Rule X, under this initial condition, boundary condition, world size and update process, produced Y.

Behaviour belongs to an experimental configuration, not to a mechanism in isolation. It costs nothing to say that here, where the configuration has five components. It will save us from a great deal of trouble later, when it has fifty.

---

## Change One Number

Our implementation says `rule=22`.

Change it to `rule=30`. Change nothing else — same world size, same single active cell, same three-cell neighbourhood, same synchronous update, same periodic boundary, same code. Only the eight-bit transition table is different.

![Rule 30 from a single active cell](/images/books/digital-life/ch03-rule30-hero.png)

There is regular structure on the left. Irregularity on the right. Repeating fragments that survive for a while and then break apart. Regions that look organized until they stop.

And every pixel of that history is fully determined by the row above it. No random numbers are involved anywhere. Rule 30 does not roll dice; its transition table is fixed, and starting from the same state gives exactly the same history every time.

This is the first genuine surprise of the book, and it is worth being precise about what is surprising.

Not merely that the picture looks complicated.

It is that:

> **a locally trivial rule can produce global behaviour that is difficult to anticipate from inspection of the rule itself.**

Determinism guarantees that the next state is fixed by the current one. It does not guarantee that a human looking at eight transition cases can intuit the long trajectory they generate.

The mechanism is tiny.

Its consequences are not correspondingly obvious.

Where, then, is the apparent complexity?

No individual cell contains it. The rule contains no picture of the future. The initial condition contains almost nothing.

What we see exists in the unfolding:

> **the trajectory produced by repeated interaction between rule and state**

That is already an important shift.

The interesting object may not be something stored anywhere.

It may be something that exists only by continuing to happen.

---

## A Word to Be Careful With

It is very tempting here to say *emergence* and feel that something has been explained.

The weak version of the word means little more than *something happened that I did not expect*, which makes it a fact about the observer rather than the system. A better working description is: a macroscopic pattern arises from local interactions without being explicitly represented in the individual components. Rule 30 does satisfy that. No cell contains a triangle. The rule contains no stored spacetime diagram. The structures appear anyway.

But notice what the label does and does not do. Calling this emergent gives us a name for the phenomenon; it tells us nothing about which property emerged, whether that property is stable, whether it is measurable, or whether it matters. The modest claim we have actually earned is:

> **Simple local mechanics can generate nontrivial global organization.**

Not life. Not intelligence. Not even, yet, deep complexity. Just enough to keep going.

---

## Make the Surprise Measurable

An image is a hypothesis generator. To get further we need an instrument.

Keep the rule fixed at 30 and perturb the world instead. Start one run from a single active cell, and another from the same world with one extra active cell beside it. Everything else is identical.

![A one-cell perturbation spreading under Rule 30](/images/books/digital-life/ch03-rule30-perturbation.png)

At first the two histories differ in one cell. Then that cell alters several neighbourhoods, those altered neighbourhoods alter later ones, and the difference spreads.

The useful move is to stop studying the two worlds and start studying the difference between them. Given states `A` and `B`, define the difference as the number of positions where they disagree — a Hamming distance:

```python
def difference_count(a, b):
    return sum(x != y for x, y in zip(a, b))
```

Run both worlds forward and record that number at every step:

![Measured growth of the perturbation](/images/books/digital-life/ch03-rule30-difference-growth.png)

Now *the disturbance seems to spread* has become something measurable:

> How much of the later world changes because one earlier cell was different?

That is a much more useful question.

And it immediately brings back the two disciplines established in the introduction: compared with what, and what is the smallest description the measurement actually earns?

**Compared with what?** A rapidly growing difference count is not evidence that Rule 30 is unusually sensitive until we have run the same perturbation protocol on other rules. The single-rule result is a measurement. The comparison is what makes it a claim.

**Don't reach for the bigger word.** It is tempting to say *chaotic*, but chaos has technical meanings in dynamical systems, and irregular, random, chaotic, complex and emergent are not synonyms. What we can safely say is that Rule 30 is deterministic, its history contains visually irregular regions, small changes to the initial state can spread through later states, and the divergence can be measured. If a stronger word requires a stronger definition, we should earn it later rather than borrow it now.

One result is worth carrying forward:

> **A small local difference can acquire a much larger future footprint through repeated interaction.**

We should not call that a theory of causation yet.

But it gives us something better than appearance: a difference we can create deliberately and then follow through time.

---

## But We Still Do Not Have a Thing

Rule 30 gives us structure, propagation, divergence, history.

It does not obviously give us an entity. If I point at one region of that spacetime diagram and ask whether it is the same object ten generations later, there is no good answer. The pattern expands, regions change, differences propagate — but nothing stays localized and recognizable long enough to be tracked.

So we change systems. Not because the next one is more sophisticated — it is not — but because it produces something Rule 30 does not produce cleanly: a localized pattern that appears to persist while moving through space.

Conway's Game of Life is a two-dimensional binary lattice where each cell looks at its eight immediate neighbours. An active cell stays active with two or three active neighbours; an inactive cell becomes active with exactly three. Written `B3/S23`. That is the entire rule, and there is no special case anywhere in it for any of the structures people have found in it.

Now consider five cells:

```text
.#.
..#
###
```

Nothing in that configuration says *move diagonally*. There is no velocity, no direction variable, no `glider.x += 1`.

![A Game of Life glider moving across a fixed lattice](/images/books/digital-life/ch04-glider.gif)

And yet a recognizable organization translates diagonally across the grid, repeating the same four-step cycle as it goes.

Now the word *thing* becomes much harder to dismiss.

---

## What Actually Persisted?

The same question as before, with a much cleaner answer available.

Game of Life cells occupy fixed coordinates. No cell travels. Cells become active and inactive according to their neighbourhoods, and the sequence looks like this:

```text
activity in one region
        ↓
changes nearby neighbourhoods
        ↓
different cells become active
        ↓
earlier cells become inactive
        ↓
a similar organization appears nearby
```

No material object crosses the grid. The organization does.

But now we can be quantitative in a way that Lenia made difficult. Run the glider for four generations and the same local configuration returns, displaced by one cell diagonally. So we can write down:

```text
period = 4 generations
displacement = (+1, +1)
```

That is a repeatable relationship, not an impression. And it lets us ask the question properly: after four generations, what persisted?

Not the same cells — most of the originally active coordinates are inactive. Not the same coordinates. Not even the same shape at every intermediate step, since the glider passes through four distinct configurations on its way round.

What persisted was a recurring sequence of local configurations, a stable transformation through time, and a fixed displacement.

This gives us the first genuinely useful distinction of the book.

Two notions of identity have separated.

**Material identity** asks whether the same components persist.

**Organizational identity** asks whether a recognizable pattern of relations persists through permitted changes.

The glider has almost no material identity across its motion. The active cells continually change.

But its organization recurs with extraordinary precision.

So we have earned a narrower claim:

> **In this system, recognizable organization can persist without persistent material identity.**

We have not found an organism.

We have found a kind of continuity that does not require one fixed body.

That is a small claim. It is also one of the load-bearing results of the entire book, and when it returns — in a very different system, under much more aggressive tests — it will not have changed.

---

## Persistence Comes in Kinds

The glider also lets us break a vague word into precise ones.

A **block** sits there:

```text
##
##
```

Under Life it never changes. `state(t+1) = state(t)`.

A **blinker** is three cells in a row, which becomes three cells in a column, which becomes three cells in a row. Its exact state does not persist; its behaviour does. `state(t+p) = state(t)`, with p=2.

A **glider** returns to its configuration only after translation: `state(t+p) = translate(state(t), Δ)`, with p=4 and Δ=(+1,+1).

![Fixed, periodic and translating persistence](/images/books/digital-life/ch04-persistence-types.png)

Fixed, periodic and translating persistence are three different properties, and a system can have one without the others. Persistence and movement have also come apart: the block persists without moving, the glider does both, and neither fact implies anything about the other.

This is the shape of most progress in this book. One word that felt like a single property turns out, on measurement, to be three — and the three behave differently.

There is a further subtlety hiding in the glider case. Compare the grid at t=0 and t=4 directly and they are not equal; compensate for the translation first and they match exactly. So identity here depends on which transformations we have decided to treat as irrelevant. Position? Orientation? Phase? Scale? The exact cells involved?

That is not merely philosophy.

It is an engineering decision.

Whatever transformations our detector is allowed to ignore — translation, rotation, phase, perhaps something else — determine what the detector will report as the same continuing pattern.

So even here, at the level of five cells, measurement and ontology are beginning to touch.

We should remember that before trusting any future boundary too quickly.

For now the operational definition is clean enough to test:

> **A glider is a localized dynamical pattern whose local state recurs after a fixed period up to spatial translation.**

We can also measure its motion without any of this vocabulary. Take the active coordinates, compute their centroid, and track it:

![The measured centroid trajectory of a glider](/images/books/digital-life/ch04-glider-centroid.png)

*The glider moved* becomes *the centroid of this localized pattern changes systematically through time*, which yields position, displacement, velocity and trajectory as observables. The noun starts becoming experimentally useful — not because we named it, but because several measurable quantities stay coherent across its transformations.

---

## Why the Glider Is Easier Than Rule 30

One word: localization.

Most of the world is not part of the glider. Activity stays concentrated in a bounded region, so we can draw a box around it, count its cells, compute its area and orientation and period, and follow it. Rule 30's structure fills the space it occupies and offers nothing to draw a box around.

That gives us a candidate operational boundary — and the word to mark is *candidate*.

Localized geometry works beautifully for the glider.

But we have not established that geometry is the universal boundary of a computational thing. It is simply the first definition that works well enough to measure.

The glider gives us a working instrument.

It does not yet tell us what an individual ultimately is.

---

## The Danger of Naming Things

Game of Life comes with a vocabulary: block, blinker, beacon, glider, spaceship, pulsar, gun. The names are genuinely useful, because saying *glider* is faster than listing coordinates and lets us reason at a higher level.

But naming has a side effect. Once a configuration has a noun, the mind starts treating it as an object automatically, and the noun begins to carry implications nobody measured. Calling a pattern a spaceship does not make it a vehicle. Calling one a gun does not make it analogous to a physical gun in any respect except a loose visual one.

We will use the names. We should also remember what they are:

> **Naming compresses description. It does not establish mechanism.**

Which is the same rule we set out in the introduction, now demonstrated with five cells:

> **Naming compresses description. It does not establish mechanism.**

---

## What Survived

We started with the most seductive system we could find and ended with five cells on a lattice. It is worth writing down what the reduction cost us and what it did not.

Here is what it looked like:

```text
something is moving
it is a creature
it persists
it is complicated
it might be alive
```

Here is what survived:

The gap between those two columns is the subject of this book.

But notice something equally important, because this chapter would be a failure if it read only as debunking. Every act of scepticism above left something behind:

Visual coherence is not objecthood — but localized organization is genuinely trackable, and the tracking produces numbers.

Complexity is not life — but a trivial deterministic mechanism really can generate a globally nontrivial trajectory, and that is a fact about computation rather than about our expectations.

Motion is not material transport — but organization really does propagate across space, carrying enough structure that other mechanisms can respond to it.

Persistence is not material identity — and the fact that these come apart is the most interesting thing in the chapter, because it means a computational substrate permits a kind of continuity that has no requirement of a stable body.

We began with something that looked like a creature.

By the time we stripped away the interpretation, the creature had disappeared.

But the phenomenon had not.

Something smaller and stranger remained:

> **persistent organization without persistent material identity**

That is the pattern to get used to.

We will repeatedly ask for one thing, lose the explanation that made it look familiar, and discover that something more precise survived underneath.

Those surviving pieces are what this book is really collecting.

---

## Now We Have Something We Can Hurt

Up to this point we have been extremely kind to these systems. We initialized them carefully, placed them in empty worlds, chose examples that behave interestingly, and then left them alone.

That is a poor way to understand a mechanism. A structure that persists under precisely the conditions that produce it has told us something, but not much. If we want to know what is actually maintaining the organization, we have to interfere with it.

The glider is now coherent enough that another question becomes possible:

> What happens if we hurt it?

Removing one of its five cells immediately separates three ideas we might otherwise have collapsed:

Everything in this chapter has been calibration.

We now have a microscope, a few simple measurements, and one useful habit: distrust the first noun that comes to mind without discarding the phenomenon that produced it.

So let us point the microscope at something much harder.

Not five cells moving across an empty lattice, but a computational world in which structures appear to produce descendants, form lineages and interact as a population.

If the glider tempted us to invent an object, the next system will tempt us to invent an organism.

That is exactly why we need to look at it.
