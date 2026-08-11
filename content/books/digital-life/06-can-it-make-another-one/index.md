+++
title = "Digital Life 06: Can It Make Another One?"
date = "2026-08-11T01:46:00+01:00"
draft = false
description = "Ask what digital reproduction actually requires, from simple copying to causal reproduction, inheritance and lineage."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Cellular Automata", "Self-Replication", "Self-Reproduction", "Evoloops", "Outlier", "Inheritance"]
+++

In the last chapter, we damaged persistent patterns.

That gave us:

```text
persistence
≠
robustness
≠
regeneration
````

Now consider a different possibility.

Instead of asking whether one organization can continue forever, ask:

> **Can one organization cause another recognizable organization to appear?**

That is reproduction in its weakest interesting form.

But we should be careful immediately.

Digital systems make copying cheap.

So cheap, in fact, that:

```text
copying
```

by itself tells us almost nothing.

The real question is not:

> Can digital state be duplicated?

Obviously it can.

The interesting question is:

> **Can the dynamics of the system itself produce another instance, and can we demonstrate a causal relationship between them?**

That is much harder.

---

# The world's worst self-reproducer

Start with the stupidest possible example.

```python
def reproduce(x):
    return x.copy()
```

Then:

```python
parent = [1, 0, 1, 1]
child = reproduce(parent)
```

Now:

```text
parent = 1011
child  = 1011
```

Did the system reproduce?

In one trivial sense, yes.

Some state was copied.

But nearly everything interesting came from outside the supposed organism:

```text
where the object begins
what counts as the object
when copying happens
how copying works
where the new copy goes
```

The function name:

```python
reproduce()
```

does not establish reproduction as an internal property of the system.

That would be exactly the mistake this book is trying to avoid.

---

# Copying is native to the digital substrate

Computers already duplicate things constantly:

```text
files
memory pages
processes
database rows
containers
virtual machines
model checkpoints
```

This matters because the digital substrate differs fundamentally from biology.

Copying digital state is often:

```text
cheap
fast
exact
```

So we should not automatically treat duplication itself as a profound achievement.

The interesting part is where the mechanism lives.

Compare:

```text
external copier
     ↓
duplicate state
```

with:

```text
local dynamics
     ↓
new recognizable instance
```

Those are very different claims.

---

# Remove the reproduction function

Imagine a cellular automaton.

There is no:

```python
spawn_child()
```

No object constructor.

No hidden supervisor identifying parents and children.

There is only:

```text
local state
+
neighborhood
+
transition rule
+
time
```

Yet eventually:

```text
one localized organization
```

is followed by:

```text
two spatially separated recognizable organizations
```

Now something more interesting has happened.

The mechanism that produces the second structure is embedded in the same local dynamics governing everything else.

There is no privileged reproduction API.

That is the kind of reproduction we care about.

---

# What counts as another one?

Suppose a configuration `C` appears here:

```text
C
```

Later:

```text
C        C
```

Have we demonstrated reproduction?

Not yet.

We immediately need an identity criterion.

How similar must the new configuration be?

Exactly identical?

Translated?

Rotated?

At another internal phase?

Slightly different?

What if the original changes while the second appears?

Again, the question:

> Did it make another one?

contains another question inside it:

> **What counts as the same kind of thing?**

Chapter 04 has returned.

Identity is not an optional philosophical decoration.

It determines whether our detector reports:

```text
1 entity
```

or:

```text
2 entities
```

---

# Growth is not necessarily reproduction

Suppose:

```text
###
```

becomes:

```text
######
```

and then:

```text
#########
```

The structure became larger.

Did it reproduce?

Probably not.

There may still be only one continuing organization.

So reproduction usually requires something stronger:

```text
one candidate entity
        ↓
two defensibly distinct candidate entities
```

That means we need some separation criterion.

Perhaps:

```text
spatial separation
```

Perhaps later:

```text
causal separation
```

For now, geometry gives us a first approximation.

But we should already mark it as provisional.

A digital individual may eventually turn out not to correspond neatly to one connected blob.

---

# Similarity is not parenthood

Now suppose the world spontaneously creates the same pattern every 100 generations.

```text
C
```

Then later:

```text
C    C    C    C
```

We might see many copies.

But imagine removing the first one.

The later copies still appear at exactly the same times.

Was the first `C` their parent?

No useful evidence supports that.

So:

```text
similarity
+
later appearance
```

is not enough.

We need causality.

---

# Causal reproduction

Compare two worlds.

## World A

```text
candidate parent present
        ↓
candidate offspring appears
```

## World B

```text
candidate parent removed
        ↓
does candidate offspring still appear?
```

If removing the supposed parent prevents, delays or substantially changes production of the supposed offspring, then the parent hypothesis becomes much stronger.

This is the same principle we introduced in the previous chapter:

> **Intervention tests whether the proposed mechanism is doing real work.**

That gives us a much stronger reproductive claim:

```text
parent-like organization
        ↓
causally contributes
        ↓
production of distinct offspring-like organization
```

Now the word:

```text
parent
```

starts earning its meaning.

---

# A minimal reproduction test

Suppose we detect candidate pattern `P`.

A useful first protocol might be:

```text
1. identify P at time t₀

2. track P through time

3. detect another spatially distinct
   pattern satisfying the identity criterion

4. verify that the new pattern persists
   independently for some minimum time

5. repeat the observation

6. remove or perturb P

7. measure whether production
   of the new pattern changes
```

Notice how much more demanding this is than:

> Look! Two blobs!

That is deliberate.

---

# Replication and reproduction are not identical questions

Suppose the parent produces:

```text
101101
```

and the child is:

```text
101101
```

That is an exact copy under this representation.

Call that:

```text
replication
```

Now suppose offspring can differ:

```text
parent
101101

child
101001
```

Now we have:

```text
variation
```

But variation alone is still not enough to tell us much.

The next question is whether the difference survives into further descendants.

---

# Variation is not inheritance

Suppose:

```text
Generation 0
101101

Generation 1
101001

Generation 2
101001

Generation 3
101001
```

Now the altered property has persisted through reproduction.

That is much closer to:

```text
inheritance
```

So:

```text
variation
```

is not the same as:

```text
heritable variation
```

A one-generation error may be noise.

An inherited difference can alter the future of a lineage.

---

# Parenthood becomes a graph

Once offspring can produce offspring, the experiment changes again.

Instead of merely counting objects, we can represent:

```text
A
├── B
│   ├── D
│   └── E
└── C
    └── F
```

Now we have a:

> **lineage graph**

This is important.

We are no longer only measuring:

```text
how many patterns exist?
```

We can ask:

```text
who descended from whom?

which branches persist?

which properties recur within branches?

which variants spread?

which branches disappear?
```

Reproduction introduces history with structure.

---

# Count descendants, but do not stop there

A simple measurement is:

```text
recognized descendants through time
```

For example:

```text
t = 0      1
t = 100    1
t = 200    2
t = 300    4
t = 400    7
```

![Recognized descendants increasing across generations](/images/books/digital-life/ch06-lineage-growth.png)

This tells us whether a structure duplicated once or participated in a growing lineage.

But raw counts are not enough.

A lineage graph tells us far more than population size alone.

Two systems may both contain:

```text
100 copies
```

while one came from:

```text
one deep branching ancestry
```

and another came from:

```text
100 independent spontaneous appearances
```

Those are completely different mechanisms.

---

# Self-reproducing cellular automata

This problem has a long history.

Von Neumann's work on self-reproducing automata was not merely about making shapes duplicate.

The deeper problem involved a machine participating in the construction of another machine while also propagating the information needed for that construction.

Later cellular-automaton systems simplified the machinery.

Langton's loops became one famous example of local dynamics producing self-reproducing structures.

Then systems such as Evoloops pushed the idea further by allowing variation among reproducing structures.

The important lesson for us is not the historical sequence itself.

It is the mechanism:

```text
local rules
+
localized organization
+
reproduction
+
variation
```

without requiring an external function to identify and copy the object.

---

# Evoloops: reproduction without a fitness function

Evoloops are especially interesting because reproduction occurs inside the world.

Interactions and collisions can create variation.

Some variants remain able to reproduce.

So instead of:

```text
A
↓
A
↓
A
```

we may obtain:

```text
A
↓
A'
↓
A''
```

and those differences can alter what happens later.

That matters because there need not be an external loop saying:

```python
score = fitness(candidate)
if score > threshold:
    reproduce(candidate)
```

Instead:

```text
successfully reproduce
        ↓
more descendants
```

or:

```text
fail to reproduce
        ↓
lineage disappears
```

The environment and dynamics produce differential reproductive success directly.

That is a very different architecture from ordinary optimization.

---

# Determinism does not prevent evolution

There is a temptation to think:

```text
deterministic universe
```

means:

```text
no evolution
```

But those ideas address different questions.

Determinism says:

> Given the complete present state, the future state is fixed.

Evolution concerns relationships among:

```text
variation
inheritance
differential reproduction
```

Those relationships can exist inside a deterministic trajectory.

Randomness is not logically required.

Variation is.

---

# Outlier makes the problem stranger

More recent cellular-automaton work gives us an even more interesting case.

In the system called **Outlier**, simple binary local dynamics can generate structures that appear to replicate at more than one spatial scale.

![One localized digital pattern producing a second spatially distinct copy](/images/books/digital-life/ch06-self-replication.gif)

That is exactly the kind of observation that should make us suspicious.

Not dismissive.

Suspicious.

Because the image invites the sentence:

> It reproduced.

But now we know what that sentence requires.

We must ask:

```text
Are there really distinct entities?

Are they persistent?

Are they related by ancestry?

Does the supposed parent matter causally?

Does the process repeat?

Do descendants themselves produce descendants?
```

The visual phenomenon is only the start.

This will matter later.

A lot.

---

# The most dangerous word here is "offspring"

Suppose a blob divides:

```text
OOOOOO
```

into:

```text
OOO    OOO
```

Our eyes immediately construct:

```text
parent
+
child
```

But several alternatives may explain the same image.

Perhaps:

```text
one object fragmented
```

Perhaps:

```text
two structures emerged from a shared surrounding process
```

Perhaps:

```text
the apparent parent was not causally necessary
```

Perhaps:

```text
our entity detector split one distributed organization into two pieces
```

So the word:

```text
offspring
```

must be earned by ancestry evidence.

Geometry alone is not enough.

---

# Mutation is not evolution

Now suppose we explicitly implement:

```python
child = parent.copy()

if random.random() < mutation_rate:
    child[random_index] ^= 1
```

Have we built evolution?

No.

We have implemented:

```text
copying
+
mutation
```

Evolution requires a population-level process over generations.

At minimum:

```text
heritable variation
+
differential reproductive success
+
change in variant frequencies through time
```

That distinction is crucial.

A mutation operator is not an evolutionary result.

---

# And evolution is not progress

Suppose a population changes for 10,000 generations.

Variants arise.

Variants disappear.

Lineages branch.

Different forms dominate at different times.

Evolution may certainly be occurring.

But perhaps:

```text
capability does not increase

useful structure does not accumulate

each useful change is later lost

later generations do not begin ahead of earlier ones
```

Then we should not automatically say:

```text
progress
```

Evolution and cumulative improvement are different claims.

This is going to matter in the next chapter.

---

# A lineage creates a new kind of persistence

Earlier, persistence meant:

```text
one organization
continuing through time
```

Reproduction allows another possibility:

```text
organization A
      ↓
organization B
      ↓
organization C
      ↓
organization D
```

No individual needs to continue indefinitely.

Some relationship may persist across successors.

That relationship could involve:

```text
shape
internal state
parameters
encoded description
behavior
learned information
```

But we must not assume in advance which of these matters.

The experimental question is:

> **What remains correlated across ancestry?**

That is a much cleaner formulation of inheritance.

---

# Digital lineages may not resemble biological lineages

This is where we need to resist importing biology too quickly.

Biological lineage is usually drawn as a tree:

```text
parent
├── child
└── child
```

Digital systems may allow stranger possibilities.

A digital entity might:

```text
fork
copy
checkpoint
restore
exchange state
merge
```

So ancestry could eventually look more like:

```text
graph
```

than:

```text
tree
```

Two descendants might exchange information.

Two branches might merge.

A restored checkpoint might create another continuation from an earlier state.

That means even the concept:

```text
lineage
```

may need a digital version rather than a biological copy.

For now, simple parent-child reproduction gives us a clean starting laboratory.

But it may not be the final architecture.

---

# Our vocabulary is becoming dangerous

We now have words such as:

```text
individual
parent
offspring
replication
reproduction
variation
inheritance
selection
lineage
evolution
```

Every one can become cargo cult.

So translate them back into operational questions.

## Individual

Can we define a pattern or causal organization sufficiently well to track it through time?

## Parent

Does one candidate entity causally contribute to the appearance of another?

## Offspring

Does a distinct continuing organization appear as a consequence of that process?

## Replication

Does the offspring satisfy an identity criterion equivalent to the parent's?

## Variation

Does the offspring differ on some measured property?

## Inheritance

Do parental properties predict corresponding descendant properties across generations?

## Selection

Do inherited differences alter expected reproductive success under the environment being tested?

## Evolution

Do inherited variants change in prevalence across generations?

Those are questions we can test.

---

# Reproduction may not be fundamental

There is one more thing we should refuse to assume.

Biology depends heavily on reproduction.

But biology also contains:

```text
finite bodies
aging
damage
death
limited individual growth
```

A digital system may not inherit those constraints.

It might instead:

```text
continue growing
self-modify
expand memory
repair indefinitely
fork only when useful
checkpoint and restore
distribute itself across machines
```

So reproduction may eventually turn out to be:

```text
important
```

without being:

```text
fundamental
```

We are studying it because it enables ancestry, inheritance and population dynamics.

Not because we have already decided that every digital life-form must reproduce.

---

# So can it make another one?

Yes.

Digital systems can certainly produce copies.

More interestingly, cellular automata can contain local dynamics from which new recognizable structures arise without an external reproduction API.

And systems such as Evoloops and Outlier give us increasingly challenging cases in which reproduction, variation and ancestry become serious experimental questions.

But the useful sequence is not:

```text
looks like replication
↓
therefore reproduction
↓
therefore life
```

It is:

```text
candidate entity
↓
distinct second entity
↓
similarity
↓
causal dependence
↓
repeated production
↓
lineage
↓
heritable variation
↓
differential reproduction
```

And only after that do we get to ask about evolution.

---

# The question changes again

Suppose we establish all of this.

We have:

```text
reproduction
variation
inheritance
selection
```

What happens over generations?

Do variants simply churn?

Do lineages remain static?

Does one type replace another?

Does the population adapt to its environment?

Does anything accumulate?

And perhaps most importantly:

> **Can later generations begin from something genuinely better than earlier generations?**

That is no longer a question about reproduction.

It is a question about evolution.

Next: **Evolution Without Life?**
