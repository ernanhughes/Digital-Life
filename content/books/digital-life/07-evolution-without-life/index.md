+++
title = "Digital Life 07: Evolution Without Life?"
date = "2026-08-11T09:48:00+01:00"
draft = false
description = "Variation, inheritance and selection can produce evolution in digital systems. But evolution is not the same thing as progress."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Evolution", "Artificial Life", "Cellular Automata", "Selection", "Open-Ended Evolution", "Cumulative Improvement"]
+++

# Digital Life 07: Evolution Without Life?

We ended the last chapter with three ingredients:

```text
variation
+
inheritance
+
differential reproductive success
```

Put those together across generations and something familiar begins to appear.

Evolution.

But that word creates a new trap.

Because once we say:

> the system evolves

it is very easy to imagine:

```text
better
smarter
more complex
more capable
more alive
```

None of those follows automatically.

Evolution can happen without progress.

Selection can happen without intelligence.

Novelty can happen without usefulness.

A population can change forever and accomplish almost nothing.

So this chapter asks a more difficult question:

> **What exactly has to improve before evolution becomes relevant to our search for digital life?**

---

# Start with two lineages

Suppose two digital patterns reproduce.

Call them:

```text
A
B
```

They occupy the same environment.

During one interval:

```text
A produces 4 surviving offspring
B produces 1 surviving offspring
```

If this continues, the future population will contain more descendants of `A`.

No external programmer has to announce:

```python
fitness(A) = 4
fitness(B) = 1
```

The reproductive outcome itself supplies a measure.

Conceptually:

```text
heritable property
      ↓
affects reproduction
      ↓
changes descendant frequencies
```

That is enough to make selection possible.

---

# Fitness is not a number written by nature

In optimization code we often define:

```python
def fitness(candidate):
    return score(candidate)
```

Then:

```python
population = sorted(
    population,
    key=fitness,
    reverse=True,
)
```

That is useful engineering.

But it can obscure what biological fitness means.

In an evolving population, fitness is tied to **reproductive success in an environment**.

A useful digital approximation might therefore be:

```text
fitness
≈
expected contribution to future generations
```

Not:

```text
fitness
=
whatever number we happened to invent
```

Those are different things.

---

# The environment matters

Suppose lineage `A` reproduces faster than lineage `B`.

Then we change the world.

Perhaps resources become scarce.

Perhaps space becomes crowded.

Perhaps collisions become common.

Perhaps reproduction becomes more expensive.

Now `B` reproduces more successfully.

So:

```text
A is fitter
```

is incomplete.

A better statement is:

```text
A had greater reproductive success
under environment E
during interval T
```

Fitness is relational.

```text
organism
+
environment
+
competition
+
time
```

matter together.

This will become extremely important later when we evaluate learned and evolved systems.

---

# A minimal evolutionary experiment

We can build a deliberately simple model.

Each individual contains one inheritable number:

```python
replication_rate
```

Begin with:

```text
parent replication rate = 0.50
```

When an offspring is produced:

```python
child_rate = parent_rate + mutation
```

Now place individuals under a resource constraint.

Higher replication rate initially produces more descendants.

Run many generations.

We might see:

```text
generation 0     0.50
generation 10    0.58
generation 20    0.66
generation 30    0.74
```

<!--
TODO VISUAL:
Animated or static population experiment.

Show:
- multiple inherited variants
- frequencies changing across generations
- one variant becoming common

Purpose:
make selection visible before introducing metrics.
-->

It looks like improvement.

But improvement in what?

Only:

```text
replication rate
```

And even that conclusion depends on the environment.

---

# Selection discovers loopholes too

Suppose replication consumes a shared finite resource.

Our intended behavior is:

```text
find resources
use resources efficiently
reproduce
```

But the evolving system discovers another strategy:

```text
replicate immediately
consume everything
collapse the environment
```

That lineage may dominate in the short term.

Was evolution successful?

Yes, in one sense.

Selection happened.

Was the outcome useful?

No.

This is the evolutionary version of objective hacking.

An evolutionary process does not know what we meant.

It only responds to what affects persistence and reproduction.

---

# Evolution is not optimization toward our goal

This distinction deserves to be explicit.

```text
selection
```

does not imply:

```text
selection toward something humans value
```

Nor does:

```text
more descendants
```

imply:

```text
better digital organism
```

A parasite can out-reproduce its host.

A lineage can exploit a measurement.

A population can drive itself into collapse.

A simpler organism can displace a more complicated one.

Selection has no obligation to produce our preferred direction.

---

# Now let the environment change

This creates a much stronger experiment.

Imagine two phases.

## Environment A

Resources are abundant.

Fast reproduction wins.

Then at generation 100:

## Environment B

Resources become scarce.

Efficiency becomes more important.

<!--
TODO VISUAL:
Time-series animation or plot.

x-axis:
generation

show:
- environmental transition
- lineage frequencies
- perhaps mean trait value

Purpose:
show adaptation as a population response to changed conditions.
-->

Now watch the population.

If inherited variants suited to the new environment become more common, we have evidence of **adaptation**.

Not because individuals decided to adapt.

But because:

```text
variation
+
inheritance
+
environment-dependent reproduction
```

changed the composition of the population.

---

# Adaptation needs a comparison

Again, the word is cheap.

If performance rises after the environment changes, we might say:

> the population adapted.

But perhaps performance would have risen anyway.

So compare:

```text
EVOLUTION CONDITION

variation enabled
inheritance enabled
selection operating
```

against:

```text
CONTROL CONDITION

variation disabled
```

or:

```text
inheritance shuffled
```

or:

```text
selection neutralized
```

Now ask:

```text
Which population recovers performance faster?
```

This is much stronger evidence.

The pattern throughout this book should be familiar by now.

To test a mechanism:

> **remove it.**

---

# Inheritance must do work

Suppose offspring resemble parents.

But the inherited information has no relationship to performance.

Then inheritance exists structurally but accomplishes nothing useful.

A more interesting experiment compares:

```text
inherited offspring
```

with:

```text
offspring initialized from scratch
```

under the same evaluation budget.

If inheritance matters, successors should gain some measurable advantage.

For example:

```text
evaluations required to reach performance threshold
```

might be:

```text
scratch successor      1,000
inheriting successor     620
```

Now inherited information is doing measurable work.

This is getting closer to the question that motivated this entire book.

---

# But selection can stop

Imagine an environment with one obvious optimum.

Evolution begins.

Performance rises:

```text
0.30
0.48
0.71
0.89
0.96
0.99
```

Then:

```text
0.99
0.99
0.99
0.99
```

The system has converged.

Nothing surprising happens afterward.

This may be excellent optimization.

It is not what researchers generally mean when they seek **open-ended evolution**.

---

# Open-ended evolution

Artificial Life researchers have long pursued systems that continue generating evolutionary novelty rather than simply converging to one optimum.

A useful way to think about the ambition is:

```text
not merely:

search
↓
solution
↓
stop
```

but:

```text
innovation
↓
new possibilities
↓
new pressures
↓
new innovation
↓
new possibilities
↓
...
```

The MODES framework, for example, proposed measuring open-ended systems using dimensions including change potential, novelty potential, complexity potential and ecological potential.

That already tells us something important.

Open-endedness is not one observable.

---

# Novelty is not enough

Here is the uncomfortable part.

A system could generate something new forever.

Imagine:

```text
000001
000002
000003
000004
000005
...
```

Every state is technically novel.

Nothing repeats.

Yet almost nothing interesting is happening.

This is not merely a hypothetical objection.

Research on open-ended evolution has demonstrated simple systems capable of satisfying proposed open-endedness conditions while exposing that those definitions can still permit behavior far below the complexity researchers ultimately want.

So:

```text
never repeats
```

is not enough.

And:

```text
continually produces novelty
```

is not enough either.

---

# Complexity is not enough

Fine.

Let's require complexity to increase.

But now we inherit another problem:

> What is complexity?

Length?

Entropy?

Compression ratio?

Number of components?

Number of interactions?

Algorithmic description length?

Behavioral repertoire?

Each captures something different.

A system can increase one complexity metric while becoming less useful.

For example:

```text
100-line useful program
```

could mutate into:

```text
10,000 lines of useless noise
```

It is larger.

It may even be harder to compress.

Calling that evolutionary progress would be absurd.

---

# Genelife exposes the distinction

Recent work on **Genelife**, an evolutionary extension of Conway's Game of Life in which live cells possess inheritable genomes affecting their local dynamics, reported conditions exhibiting open-ended genetic and spatial innovation. But the authors explicitly note that the observed innovation still falls short of functional biological innovation.

That distinction is incredibly useful for us.

A system can demonstrate:

```text
continuing novelty
```

without demonstrating:

```text
continuing acquisition of useful capability
```

Those are different experimental targets.

---

# Flow-Lenia pushes the problem further

Flow-Lenia gives another contemporary example.

It extends Lenia with mass-conservative dynamics and can support localized patterns with complex behavior, while allowing rule parameters associated with emerging patterns to exist within the dynamics of the world itself. Recent experiments have analyzed the resulting system using evolutionary-activity and related metrics.

This matters because it moves us away from:

```text
external optimizer
manipulates candidates
```

toward:

```text
world dynamics
contain variation
contain interaction
contain population structure
```

The evolutionary process becomes increasingly endogenous.

But the same question remains:

> What accumulates?

---

# Outlier raises the same question

The binary CA rule Outlier is fascinating precisely because surprisingly rich self-replicating structures emerge from sparse random initial states, including replication at multiple spatial scales. The rule itself was discovered while searching for cellular automata conducive to open-ended evolution.

That is an extraordinary emergence result.

But even spectacular replication leaves open the next question.

Does a lineage:

```text
retain useful innovations
```

and then:

```text
build further innovations on top of them?
```

Replication gives evolution something to work with.

It does not guarantee cumulative progress.

---

# Evoloops really do evolve

We should also be precise about what has already been achieved.

Evoloops constructively demonstrated Darwinian evolution of self-reproducing patterns through inheritable variation and natural selection inside a deterministic cellular automaton.

That is not metaphorical evolution.

It satisfies the core mechanism we have been building toward:

```text
reproduction
+
heritable variation
+
differential reproductive success
```

The same review notes a persistent challenge, however: many spatially distributed evolutionary systems eventually become dominated by one or a few successful species and settle into pseudo-equilibrium rather than continuing indefinitely into richer evolutionary possibilities.

Evolution exists.

Open-endedness remains difficult.

---

# Evolution and progress are different axes

Let's make this explicit.

Imagine four systems.

## System A

```text
no inherited variation
no population change
```

No evolution.

## System B

```text
inherited variation
+
selection
+
population changes
```

Evolution.

## System C

```text
evolution
+
continual novelty
```

Potentially open-ended innovation.

## System D

```text
evolution
+
useful innovations
+
retention
+
new innovations built on retained ones
```

This last system is the one we care about most.

Call it, provisionally:

> **heritable progress**

---

# Heritable progress

We need to be very careful here.

This is not a universal biological definition.

It is an experimental target for this book.

A lineage exhibits **heritable progress** when:

```text
1. a generation acquires a useful capability or advantage

2. information responsible for some of that advantage
   survives into successors

3. successors measurably benefit from that inheritance

4. successors can acquire further useful improvements

5. those further improvements can also persist
```

Conceptually:

```text
Generation 0
    ↓
learns A
    ↓
leaves A

Generation 1
    ↓
inherits A
    ↓
starts ahead
    ↓
learns B
    ↓
leaves A + B

Generation 2
    ↓
inherits A + B
    ↓
starts further ahead
    ↓
learns C
```

That is qualitatively different from:

```text
Generation 0 learns A

Generation 1 starts over

Generation 2 starts over

Generation 3 starts over
```

Even if every generation individually performs useful work.

---

# The ratchet

A useful metaphor is a ratchet.

Progress can move forward but does not fall completely backward at every generation.

```text
A
↓
A + B
↓
A + B + C
↓
A + B + C + D
```

Reality will not be this clean.

Some improvements will disappear.

Some will conflict.

Some will only matter in specific environments.

Some inheritance will be harmful.

But if nothing persists long enough for later generations to build on it, cumulative improvement cannot occur.

So the real requirement is not perfection.

It is:

```text
retention sufficient for further construction
```

---

# How would we prove this?

Now we can design the experiment.

Give a lineage a task.

Give every generation a finite resource budget.

For example:

```text
100 evaluations
```

Generation 0 starts from scratch.

It searches.

It improves.

Then it ends.

Before ending, it may leave an inheritable state:

```text
parameters
memory
strategy
model
rules
archive
environmental representation
```

Generation 1 receives that state.

Then compare it with a control lineage that starts from scratch.

Measure:

```text
initial performance
performance after fixed budget
time to threshold
best capability reached
```

Repeat across generations.

<!--
TODO VISUAL:
Central chapter figure.

Two lineage trajectories:

SCRATCH LINEAGE
each generation resets to baseline

HERITABLE LINEAGE
each generation begins from inherited state

x-axis:
generation

y-axis:
performance / solved difficulty

Purpose:
visualize the exact destination of the book.
-->

If the inherited lineage systematically begins ahead and continues extending the frontier, we finally have evidence for something stronger than mere persistence or reproduction.

---

# The environment must not stay identical

There is an obvious loophole.

Suppose Generation 0 discovers the exact answer:

```text
42
```

Generation 1 inherits:

```text
42
```

and solves the identical problem instantly.

That's inheritance.

But it is not impressive cumulative adaptation.

We may simply have cached an answer.

So future generations should encounter:

```text
related but non-identical problems
```

or:

```text
held-out environments
```

or:

```text
progressively harder conditions
```

Now inherited knowledge must be reusable rather than merely replayed.

---

# A stronger experiment

Imagine a sequence of environments:

```text
E0
E1
E2
E3
```

Each shares underlying structure but introduces new difficulty.

Then compare:

```text
LINEAGE A

starts from scratch
at every environment
```

against:

```text
LINEAGE B

inherits useful state
from previous environments
```

If Lineage B increasingly outperforms Lineage A, something is accumulating.

Better still:

```text
gap(B, A)
```

should grow.

That would suggest inheritance is not merely preserving old answers.

It is enabling faster future learning.

---

# This is where digital life becomes useful

Notice how far we've moved.

We began with:

```text
one bit
```

Then:

```text
local rules
```

Then:

```text
unexpected structure
```

Then:

```text
persistent patterns
```

Then:

```text
entities
```

Then:

```text
perturbation
```

Then:

```text
reproduction
```

Now:

```text
evolution
```

But the destination isn't simply:

> create a digital organism.

The more interesting engineering possibility is:

> **create computational lineages that leave useful work behind.**

An individual process can stop.

A model can be replaced.

A worker can exhaust its compute budget.

But the next one should not have to rediscover everything.

---

# Death becomes less important

This changes the meaning of failure.

Suppose a digital worker receives a hard problem.

It gets only:

```text
10 minutes
```

or:

```text
one million tokens
```

or:

```text
100 model calls
```

It fails to solve the entire task.

That does not mean its existence was wasted.

If it leaves:

```text
tested hypotheses
failed approaches
partial models
useful representations
verified facts
candidate solutions
measurements
```

then its successor can begin farther ahead.

The individual failed.

The lineage progressed.

That is exactly the distinction we have been building toward.

---

# But we are getting ahead of ourselves

Look at what we have now claimed across seven chapters.

We have used words such as:

```text
emergence
complexity
entity
persistence
robustness
regeneration
reproduction
inheritance
fitness
adaptation
evolution
open-endedness
progress
```

That is a dangerous pile of nouns.

Some have been demonstrated carefully.

Some have only been illustrated.

Some have only been defined.

Some remain future experimental targets.

If we keep going without auditing them, we will eventually commit exactly the error this book began by warning against.

So before building anything more ambitious, we need to turn around.

Look at every impressive thing we have seen.

And ask:

> **What did we actually prove?**

Next: **Now Prove It.**
