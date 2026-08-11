+++
title = "Digital Life 06: Can It Make Another One?"
date = "2026-08-11T01:46:00+01:00"
draft = false
description = "Ask what digital reproduction actually requires, from simple copying to inheritable variation and self-reproducing cellular structures."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Cellular Automata", "Self-Replication", "Self-Reproduction", "Evoloops", "Outlier", "Inheritance"]
+++

# Digital Life 06: Can It Make Another One?

We killed the glider.

That exposed an uncomfortable weakness.

A persistent pattern can disappear permanently after a tiny perturbation.

One possible solution is to make the original pattern harder to destroy.

Another is very different:

> **Don't require the original to survive forever.**

Make another one.

Then another.

Now persistence can move from:

```text
one structure surviving through time
```

to:

```text
information surviving through successors
```

That is a major transition.

And an extremely dangerous place to start using biological words too casually.

---

# Copy this

Suppose we begin with:

```text
.##.
####
.#..
```

and after some number of updates we have:

```text
.##.        .##.
####        ####
.#..        .#..
```

There are now two copies of the pattern.

That looks like reproduction.

But what exactly have we demonstrated?

At minimum:

> A dynamical process caused an additional instance of a recognizable configuration to appear.

That's interesting.

But let's make the problem deliberately stupid first.

---

# The world's worst self-reproducer

Consider:

```python
def reproduce(x):
    return x.copy()
```

Run:

```python
parent = [1, 0, 1, 1]

child = reproduce(parent)
```

Congratulations.

We now have:

```text
parent = 1011
child  = 1011
```

The system reproduced.

Or did it?

Technically, we copied some data.

But almost everything interesting was supplied from outside:

```text
where the object begins
what counts as the object
when copying occurs
where the child goes
how copying is performed
```

Calling the function:

```python
reproduce()
```

adds no scientific content.

This is exactly the cargo-cult problem we promised to avoid.

---

# Copying is cheap

Modern computers copy things constantly.

```text
files
memory pages
processes
database rows
containers
virtual machines
model checkpoints
```

If duplication alone were sufficient for digital life, your operating system would be overflowing with organisms.

The interesting question is not:

> Can software make another copy of some state?

Obviously it can.

The interesting question is:

> **Can reproduction arise from the dynamics of the system itself?**

Now we're asking something harder.

---

# Remove the reproduction function

Imagine a cellular automaton.

There is no:

```python
spawn_child()
```

There is only:

```text
cell state
+
neighborhood
+
local transition rule
+
time
```

Yet a localized pattern eventually produces another localized pattern resembling itself.

Now something different has happened.

The mechanism responsible for copying is embedded in the same local physics that governs everything else.

There is no privileged reproduction API.

That is why self-reproducing cellular automata became such an important Artificial Life problem.

---

# What exactly counts as a copy?

Before getting impressed, define it.

Suppose configuration `C` exists at one location.

After some time there are two spatially separate instances:

```text
C       C
```

How similar must they be?

For an exact binary system perhaps:

```text
child == parent
```

is enough.

But what if the child is rotated?

```text
parent       child

.##.          ....
####          ###.
.#..          .##.
....          .#..
```

Or translated?

Or one bit differs?

Or the parent has changed while constructing the child?

Once again, **identity becomes part of the measurement**.

---

# A useful classical criterion

A traditional way to formalize self-replication in cellular automata is to consider a bounded configuration surrounded by quiescent space and ask whether evolution can eventually produce arbitrarily many copies of that configuration.

The recent review of self-reproduction in cellular automata revisits precisely this problem and distinguishes several notions of replication and reproduction.

Conceptually:

```text
C

↓

C     C

↓

C     C     C

↓

...
```

But even this leaves an important question.

Did `C` do anything?

Or did the universe happen to create more `C`s around it?

---

# Causal reproduction

Suppose a world spontaneously produces this pattern every 100 generations:

```text
C
```

Eventually there will be many instances of `C`.

But removing one existing `C` changes nothing.

New copies continue appearing at exactly the same rate.

Calling the original pattern a parent would be misleading.

So we need something stronger.

Compare:

```text
WORLD A

contains C
    ↓
new C appears
```

against:

```text
WORLD B

C removed
    ↓
does new C still appear?
```

If eliminating the supposed parent eliminates or strongly reduces production of the supposed offspring, we have much stronger evidence for a reproductive relationship.

Notice how familiar this should feel.

Again:

> **intervention tells us whether the proposed mechanism matters.**

---

# Parent and offspring must separate

Another useful requirement is spatial individuality.

Imagine one pattern simply expanding:

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

Did it reproduce?

Probably not.

One structure became larger.

For reproduction, we generally want something more like:

```text
parent
   ↓
parent + distinct offspring
```

There must be some defensible boundary between them.

That returns us to the problem from Chapter 04.

Before talking about reproduction, we need some notion of:

```text
individual
```

Otherwise we cannot tell whether there are now two of anything.

---

# The old problem was harder than it looked

John von Neumann explored this question long before modern Artificial Life.

The goal was not merely to make a pattern that happened to duplicate.

The deeper problem was to understand how a machine could contain a description that participated in constructing another machine, including a copy of that description.

Later cellular-automata systems simplified and explored pieces of this problem.

Chris Langton's self-reproducing loops became one important milestone.

And then something more interesting happened.

The copies stopped being perfect.

---

# Replication versus reproduction

This distinction is worth locking into the book.

The recent Evoloops review uses:

```text
SELF-REPLICATION
```

for the production of essentially identical copies.

And:

```text
SELF-REPRODUCTION
```

when offspring can contain **inheritable variation**.

So:

```text
replication

parent
  ↓
identical child
```

while:

```text
reproduction

parent
  ↓
similar child
  ↓
variation may be inherited
```

![Recognized descendants increasing across generations](/images/books/digital-life/ch06-lineage-growth.png)

That second case opens the door to something replication alone cannot provide.

Evolution.

But we aren't there yet.

---

# Evoloops

Evoloops are particularly important for our argument.

They were derived from earlier self-reproducing loop systems but modified so reproduction could tolerate a broader range of local situations. Interactions and collisions during replication could create variations, and some of those variations remained capable of reproducing.

That changes the system fundamentally.

Instead of:

```text
A
↓
A
↓
A
↓
A
```

we can get something like:

```text
A
↓
A'
↓
A''
```

where the differences affect future reproductive success.

The Evoloops work demonstrated that variation and natural selection could occur inside a deterministic cellular automaton. The review emphasizes something especially relevant to this book: the implementation itself contained no global concept of an individual or selection, and differential reproductive success emerged from local interactions in the CA world.

That is a much stronger result than calling a function called `mutate()`.

---

# There is no fitness score

This is worth stopping on.

Many artificial evolutionary systems look like:

```python
for candidate in population:
    score = fitness(candidate)

keep_best_candidates()
```

There is nothing wrong with this.

We will use optimization later.

But Evoloops offer a different kind of experiment.

There is not necessarily some external system saying:

```text
you scored 0.82
you scored 0.51
therefore you reproduce
```

Instead:

```text
reproduce successfully
      ↓
more descendants
```

or:

```text
fail to reproduce
      ↓
lineage disappears
```

Fitness becomes connected to what actually happens in the environment.

That brings the implementation closer to the phenomenon being claimed.

---

# But deterministic evolution?

There is an apparent paradox here.

The CA is deterministic.

Given exactly the same starting configuration:

```text
same future
```

every time.

Yet variation and natural selection can still occur during the trajectory.

There is no contradiction.

Determinism describes how states follow from earlier states.

Evolution describes relationships between:

```text
variation
inheritance
differential reproduction
```

Those can exist inside a completely deterministic universe.

Randomness is not logically required for evolution.

Variation is.

---

# Then something stranger appeared

More recently, Bo Yang reported a binary cellular automaton rule called **Outlier**.

This is particularly interesting because the underlying cells are only binary, the rule acts on a two-dimensional Moore neighborhood, and the rule was discovered through genetic programming while searching for systems capable of open-ended evolutionary behavior.

From sparse random initial states, the rule can produce lower-level clusters that generate new clusters, including periodically self-duplicating structures. Under sufficiently sparse conditions, those structures can also combine into larger formations that themselves exhibit self-replication.

In other words, replication appears at more than one spatial scale.

![One localized digital pattern producing a second spatially distinct copy](/images/books/digital-life/ch06-self-replication.gif)

This is exactly the kind of result the opening of this book was designed to reach.

Remember how little machinery we needed in Chapter 02?

```text
local states
+
local neighborhoods
+
transition rules
```

Now systems built from the same general idea are producing structures that make more structures.

---

# But "replication" can fool us too

Suppose a blob divides:

```text
OOOOOO
```

into:

```text
OOO   OOO
```

It looks spectacular.

Before calling it reproduction, ask:

```text
Are these actually distinct persistent structures?

Do both continue independently?

Does the process happen repeatedly?

Does removing the parent alter child production?

Are the offspring sufficiently similar?

Does variation pass to descendants?
```

The picture is the beginning of the experiment.

Not the end.

---

# Build a replication test

Suppose we detect a candidate pattern `P`.

A minimal test could look like:

```text
1. identify P at time t₀

2. track P through time

3. detect a second spatially separate
   pattern sufficiently similar to P

4. verify both persist independently

5. repeat the observation

6. perturb or remove P

7. test whether offspring production changes
```

Now our claim is much stronger.

---

# Count descendants

A simple observable is:

```text
number of recognized copies through time
```

For example:

```text
t = 0      1
t = 100    1
t = 200    2
t = 300    4
t = 400    7
```

Plot:

```text
time
 ↓
number of copies
```

That tells us whether a pattern merely duplicated once or generated a proliferating lineage.

![Recognized descendants increasing across generations](/images/books/digital-life/ch06-lineage-growth.png)

Again, this is stronger than a cherry-picked GIF.

---

# Now make one copy different

Suppose reproduction produces:

```text
parent

101101
```

and:

```text
offspring

101001
```

One bit changed.

Wonderful.

We have variation.

But have we demonstrated inheritance?

Not necessarily.

To establish inheritance, the changed property must affect descendants.

Imagine:

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

Now the difference has persisted across reproduction.

That's much more interesting.

So:

```text
variation
```

is not enough.

We want:

```text
heritable variation
```

---

# Mutation is not evolution

This is perhaps the most important warning in the chapter.

It is easy to build:

```python
child = parent.copy()

if random.random() < mutation_rate:
    child[random_index] ^= 1
```

and announce:

> the organism evolves.

No.

We have implemented mutation.

Evolution requires a population-level process across generations.

At minimum, we are looking for relationships among:

```text
variation
+
inheritance
+
differential reproductive success
```

And even then, if we want the stronger result that motivates this book, we need something more.

---

# Evolution can go nowhere

Imagine 1,000 generations.

Every generation differs slightly.

The population continually changes.

But:

```text
performance does not improve
complexity does not increase
capabilities do not accumulate
adaptations disappear as quickly as they appear
```

Has evolution occurred?

Potentially, yes.

Has **progress** occurred?

Not necessarily.

This distinction is central to where this book is heading.

We're interested not merely in:

```text
change across generations
```

but eventually:

```text
useful change
+
inheritance
+
retention
+
further useful change
```

That is much harder.

---

# Replication gives us a new kind of persistence

Earlier we studied:

```text
one pattern
persisting through time
```

Now there is another possibility:

```text
pattern A
    ↓
pattern B
    ↓
pattern C
    ↓
pattern D
```

No single instance needs to survive indefinitely.

What persists is something distributed across the lineage.

Perhaps:

```text
structure
rule parameters
encoded description
behavior
learned information
```

This is the first appearance of one of the book's eventual central questions:

> **What exactly should survive when the individual does not?**

---

# The individual can die

This changes how we think about death.

Suppose:

```text
parent exists
    ↓
offspring produced
    ↓
parent disappears
```

Nothing necessarily failed.

If information important to future success passed forward, the lineage may continue.

That means we eventually need two different units of analysis:

```text
individual
```

and:

```text
lineage
```

A system can perform badly at one level and well at another.

An individual may disappear.

The lineage may improve.

---

# Now our vocabulary is dangerous

We have accumulated a lot of biological language:

```text
individual
parent
offspring
replication
reproduction
mutation
inheritance
selection
lineage
```

Every one of these terms can become cargo cult.

So keep translating them back into operational questions.

### Individual

Can we identify a persistent localized configuration independently of its environment?

### Parent

Does the existence or behavior of one instance causally contribute to production of another?

### Offspring

Is a distinct persistent instance produced?

### Replication

Is the offspring effectively identical under our identity criterion?

### Reproduction

Can offspring contain inheritable variation?

### Inheritance

Do properties of one instance predict corresponding properties in descendants beyond chance or environmental explanation?

### Selection

Do inherited differences affect reproductive success?

### Evolution

Do inherited variants change in frequency over generations?

That gives us something testable.

---

# And then comes the question we actually care about

Suppose all of this works.

We have:

```text
replication
variation
inheritance
selection
evolution
```

Is that enough?

Remember where this book is eventually going.

We don't merely want a population that keeps changing.

We want to know whether generations can **build on one another**.

Can generation `N` discover something useful?

Can that useful information survive reproduction?

Can generation `N + 1` begin from that advantage?

Can it then discover something further?

Can that survive too?

Conceptually:

```text
generation 0
    ↓
useful change A
    ↓
generation 1 inherits A
    ↓
useful change B
    ↓
generation 2 inherits A + B
    ↓
useful change C
```

That is stronger than reproduction.

Stronger than mutation.

Stronger even than evolution in the weakest sense.

It is the beginning of:

> **cumulative improvement across a lineage.**

We're not ready to build that yet.

But now we can finally see the path.

---

# So can it make another one?

Yes.

Cellular automata have demonstrated nontrivial self-replication for decades, and systems such as Evoloops demonstrated inheritable variation and Darwinian natural selection within deterministic CA dynamics.

More recent work such as Outlier shows that self-replicating organization can even emerge in a binary CA across multiple spatial scales from sparse initial conditions rather than requiring an explicitly handcrafted replicator as the starting object.

But those results do not let us collapse everything into:

> digital life achieved.

They give us a better sequence of questions:

```text
Can it make another one?

Can the copy differ?

Can the difference be inherited?

Does the difference affect reproductive success?

Does the population change?

Does anything useful accumulate?
```

That last question is the hard one.

Before answering it, however, we need to confront the machinery that connects reproduction to change across generations.

Next: **Evolution Without Life?**
