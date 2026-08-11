+++
date = '2026-08-11T12:48:00+01:00'
draft = false
title = 'Digital Life 11: Is It Really Reproducing?'
categories = ['Programming', 'Artificial Life']
tags = ['Digital Life', 'Artificial Life', 'Cellular Automata', 'Outlier', 'Causality', 'Collective Motion', 'Experiments']
series = ['Digital Life From First Principles']
+++

# Digital Life From First Principles 11: Is It Really Reproducing?

Something strange happened while we were looking at Outlier.

We had started with a question about reproduction.

Then I watched the simulation.

And I thought:

> That looks like flocking.

That is exactly the kind of observation that can get us into trouble.

Humans are extraordinarily good at seeing things in motion and assigning meaning to them.

We see:

```text
a shape
another shape
movement
coordination
````

and very quickly turn that into:

```text
organisms
offspring
groups
flocks
```

But this book has one rule that matters more than almost any other:

```text
appearance
is not
evidence
```

So instead of calling it flocking, we stopped.

And measured it.

That led us into a much deeper investigation than I expected.

---

## The problem with watching artificial life

Here is the Outlier simulation again.

{{< figure src="/images/books/digital-life/ch10-outlier-growth.gif" caption="The published Outlier cellular automaton running from its small initial seed." >}}

It is very difficult to watch something like this without inventing nouns.

You start saying:

```text
that thing moved

that thing split

those things are travelling together

that one produced another one
```

But every noun contains a hypothesis.

What is a **thing**?

What counts as the same thing at a later time?

What makes one structure the parent of another?

What makes two nearby structures separate individuals rather than components of one larger structure?

These are not philosophical decorations.

They are experimental questions.

---

# First question: is it really reproducing?

In the previous chapter we introduced Outlier because it gives us something unusually valuable.

It is extremely simple at the substrate level.

The world is a binary cellular automaton.

Each cell sees a `3 × 3` neighborhood.

That neighborhood gives us one of:

```text
512
```

possible local configurations.

A fixed rule determines whether the centre cell will be alive or dead on the next step.

There is no class called:

```python
Organism
```

There is no method called:

```python
reproduce()
```

There is no explicit genome object.

And yet large structures appear.

Some structures recur.

Some appear to produce more structures.

That makes Outlier ideal for our purposes.

If reproduction occurs here, it cannot be because the programmer wrote:

```python
if organism.ready:
    organism.reproduce()
```

Something more interesting must be happening.

---

## Similarity is not reproduction

Suppose we see this:

```text
time t

    A

time t + 500

    A     A
```

It is tempting to say:

> A reproduced.

But that observation alone does not establish reproduction.

Perhaps both copies were produced independently by the surrounding environment.

Perhaps the second structure would have appeared even if the first one had never existed.

Perhaps what we are calling two structures are actually parts of a larger repeating process.

So reproduction is not merely a question of similarity.

It is a **causal claim**.

We want something closer to:

```text
parent existed
↓
parent participated causally in a process
↓
later candidate appeared
↓
without the relevant earlier structure,
the later structure would not have appeared in the same way
```

That is a much stronger statement.

---

# Counterfactual causality

Because Outlier is a cellular automaton, we have an unusually clean opportunity.

For every live cell at time:

```text
t + 1
```

we know exactly which `3 × 3` neighborhood produced it.

So we can ask:

> Which live cells in the preceding neighborhood were actually necessary for this cell to become alive?

Our simplified test works like this.

Take a live child cell.

Then, one at a time, remove each live predecessor from its local neighborhood.

Re-evaluate the cellular automaton rule.

If removing a predecessor changes the child from:

```text
alive
```

to:

```text
dead
```

then that predecessor was positively necessary under this counterfactual test.

Conceptually:

```python
original = rule(neighborhood)

for predecessor in live_predecessors:

    modified = neighborhood.copy()
    modified[predecessor] = 0

    counterfactual = rule(modified)

    if original == 1 and counterfactual == 0:
        record_causal_dependency(predecessor, child)
```

This is not a complete theory of causality.

But it gives us something much stronger than visual resemblance.

It gives us a causal graph.

---

# From cells to structures

Cell-level causality produces a huge amount of information.

So we aggregate cells into connected clusters.

Then causal dependencies between cells become causal relationships between clusters.

The result looks approximately like:

```text
cluster at t
     ↓
cluster at t+1
     ↓
cluster at t+2
     ↓
...
```

with branching where one earlier organization contributes to multiple later structures.

For our `512 × 512` experiment over `1600` generations we found:

```text
138,891 clusters
196,466 causal edges
```

That is already a useful warning.

The visual animation looks as though it contains a collection of fairly obvious moving objects.

The causal graph tells us that underneath that appearance is a very large network of dependencies.

---

# Finding c2 again

The published Outlier seed starts as a tiny configuration:

```text
.1.
111
..1
```

After two updates it produces a small structure we call `c2`.

In our simulation that structure had:

```text
area = 6
bounding box = 3 × 3
```

Instead of searching for arbitrary repeating shapes, we derived the actual `c2` signature directly from the known initial seed.

Then we searched the entire run for later occurrences of that structure, allowing translation and rotation.

We found:

```text
144 c2 occurrences
```

between:

```text
t = 2
```

and:

```text
t = 1598
```

But recurrence still does not prove reproduction.

So we combined recurrence with the causal graph.

---

# A causal family tree

For every `c2`, we searched forward through the causal graph for later `c2` structures reachable through that causal history.

The original `c2` at:

```text
t = 2
```

produced a branching causal structure with four later `c2` descendants.

The complete return graph contained:

```text
99 visible c2 return edges
```

The full graph was too complicated to use as an illustration, so the figure shows a deliberately pruned family.

{{< figure src="/images/books/digital-life/ch10-outlier-causal-lineage.png" caption="A readable subset of the Outlier c2 causal family tree. The visual is pruned; the analysis uses the full causal graph." >}}

This is much stronger evidence than:

> I saw one shape and later saw several similar shapes.

We can now say something closer to:

> Later occurrences of the c2 structure are reachable through a measurable causal ancestry originating in earlier c2 structures.

That is the kind of evidence we need before using words such as reproduction.

---

# Then I saw the flock

While looking at the same simulation, another visual pattern became difficult to ignore.

Groups of structures appeared to move together.

Not merely outward.

Together.

It looked remarkably like:

```text
flocking
```

But we had just spent several chapters warning ourselves against doing exactly this.

So we made the visual impression into a hypothesis.

---

# What would flocking mean?

We did not begin by trying to reproduce every formal definition from swarm biology or active-matter physics.

We started with a much narrower question:

> Do nearby persistent moving structures travel in unusually similar directions?

That can be measured.

First we needed persistent motion tracks.

Using the causal graph, we followed plausible continuations of clusters through time.

The run produced:

```text
13,635 persistent motion tracks
```

using a minimum track length of:

```text
8 generations
```

Across those tracks we obtained:

```text
633,808 motion observations
```

Now each observation could give us:

```text
position
velocity
time
causal identity
```

That was enough to perform a first test.

---

# Measuring directional alignment

For two velocity vectors:

[
v_i
]

and:

[
v_j
]

we normalize them and take their dot product:

[
A_{ij}
======

\frac{v_i}{|v_i|}
\cdot
\frac{v_j}{|v_j|}
]

The result lies between:

[
-1
]

and:

[
1
]

where:

```text
 1  = same direction
 0  = no directional agreement
-1  = opposite directions
```

Then we compare simultaneously moving structures at different spatial separations.

For performance, we do not compare every object with every other object.

We use a spatial index and examine nearby pairs.

That is also a better experiment.

If we are asking about local collective motion, structures on opposite sides of the universe are not particularly useful comparisons.

---

# The first result

The first experiment produced a striking result.

At short distances, observed velocity alignment was approximately:

```text
0.74
```

while a velocity-shuffled control was much lower.

{{< figure src="/images/books/digital-life/ch10-outlier-flocking-test.png" caption="Nearby persistent structures exhibit much stronger directional alignment than a shuffled velocity control." >}}

So the visual observation was not completely imaginary.

There really was a measurable short-range motion coherence.

But this still did not prove flocking.

We had immediately created another problem.

---

# Maybe everything is simply moving outward

Outlier develops as an expanding structure.

Suppose nearby clusters sit on the same expanding front.

They might move in similar directions simply because both are being carried outward.

Imagine two pieces of debris on the same expanding circular wave.

They could have very similar velocity vectors without interacting with one another at all.

So we needed another control.

---

# Removing radial expansion

For each position:

[
x_i
]

we calculate its radial direction relative to the centre:

[
r_i
===

\frac{x_i-c}
{|x_i-c|}
]

Then decompose its velocity into:

```text
radial motion
+
non-radial motion
```

and remove the radial component.

If the apparent flocking was really just expansion, the alignment should collapse.

Instead we found:

```text
raw short-range alignment        = 0.7373
radial-subtracted alignment      = 0.7427
shuffled residual control        = 0.1933
```

The alignment did not disappear.

It barely changed.

{{< figure src="/images/books/digital-life/ch11-outlier-radial-family-flocking.png" caption="Short-range motion coherence survives subtraction of the global radial expansion field." >}}

So we could rule out one simple explanation:

> The observed coherence is not explained merely by every structure moving radially away from the original seed.

That made the result more interesting.

And then the causal analysis gave us another possibility.

---

# What if these are not separate individuals?

This is where digital life starts becoming stranger than our biological intuition.

Several spatially disconnected clusters can participate in the same causal organization.

So what looks like:

```text
thing A

thing B

thing C
```

might actually be:

```text
component A
component B
component C

        ↓

one distributed causal process
```

If those components travel together, calling the behavior flocking may be completely wrong.

A flock is normally imagined as several individuals moving collectively.

But these structures might instead be parts of **one distributed individual**.

So we asked another question.

> Do structures belonging to the same causal lineage move more coherently?

---

# Giving structures causal families

Our first family definition was too narrow.

It started with four branches descending from one early `c2`.

That produced strong same-family alignment:

```text
0.768
```

but no useful different-family comparison.

So we strengthened the definition.

Every cluster was assigned its **most recent identifiable c2 ancestor**.

If a cluster itself was `c2`, it began a new family.

Otherwise we propagated ancestry through the causal graph.

If equally close causal paths disagreed, we marked the assignment ambiguous rather than inventing an answer.

The coverage was remarkable.

Among:

```text
138,891 clusters
```

we assigned a recent c2 ancestor to:

```text
138,132
```

Only:

```text
10
```

were ambiguous and:

```text
749
```

were unassigned.

Among our motion observations:

```text
633,696 / 633,808
```

received a recent-c2 family label.

{{< figure src="/images/books/digital-life/ch11-outlier-family-coverage.png" caption="Almost every tracked moving structure in this single-seed experiment can be associated with a recent c2 causal ancestor." >}}

That alone tells us something important about this experiment.

The world is not naturally decomposing into a collection of unrelated particles.

Almost everything we are tracking belongs to a branching causal history.

---

# A very exciting result

When we compared nearby structures after subtracting a local background flow, we initially found:

```text
same recent-c2 family        = 0.828
different recent-c2 family   = -0.349
```

That looked spectacular.

Perhaps causal relatives really were moving together.

Perhaps different families were even moving against one another.

But there was a problem.

The control itself could create the negative result.

---

# Our experiment was wrong

This is worth slowing down for.

To estimate the local environmental flow around object `A`, we averaged nearby velocity vectors after excluding structures from `A`'s own family.

When comparing two different families:

```text
A
B
```

`B` could therefore contribute to the estimate of `A`'s background.

And `A` could contribute to the estimate of `B`'s background.

In the simplest case:

[
r_A \approx v_A-v_B
]

and:

[
r_B \approx v_B-v_A
]

which means:

[
r_B \approx -r_A
]

We had accidentally built an anti-correlation into the estimator.

So the:

```text
-0.349
```

result was not trustworthy.

This is exactly why experiments need controls.

And why controls themselves need criticism.

---

# Pair-excluded background flow

We fixed the problem.

When testing a pair from families:

```text
α
β
```

we estimated local background motion while excluding:

```text
family α
family β
```

from both estimates.

Now neither member of the tested pair could create the other's residual.

Using this stronger control we obtained:

```text
Same recent c2 ancestor          0.746
Very close c2 ancestry           0.101
Close c2 ancestry                0.032
Distant c2 ancestry              0.135
Very distant c2 ancestry         0.081
```

{{< figure src="/images/books/digital-life/ch11-outlier-relatedness-coherence.png" caption="Motion coherence is extremely high for structures sharing the same recent c2 ancestor, while more distant genealogical relationships show much weaker coherence." >}}

That looked like strong evidence for causal individuality.

But there was another problem.

---

# The four-and-a-half-cell problem

The structures sharing the same recent `c2` ancestor were also extremely close together.

Their mean separation was only about:

```text
4.5 cells
```

Other causal groups were typically tens of cells apart.

So we had confounded:

```text
causal relatedness
```

with:

```text
spatial proximity
```

Perhaps structures sharing a family move together because they are parts of the same tiny local formation.

Perhaps any two structures that close together would show similar motion.

Once again, the exciting interpretation had outrun the evidence.

So we performed one more experiment.

---

# Distance-matched causal coherence

We constructed a matched dataset.

For a same-family pair, we searched for different-family comparisons occurring under approximately the same conditions.

We matched on:

```text
simulation time
spatial distance
local density
```

and continued to use the stronger pair-excluded background-flow correction.

The question was now very precise:

> At similar times, at similar distances, and in similar local environments, do members of the same c2 causal family move more coherently than members of different families?

We used:

```text
2,617,077
```

usable pair records.

From those we constructed:

```text
65,021
```

matched pairs per comparison group across:

```text
668
```

matched strata.

Then we measured the result.

---

# The effect disappeared

The final matched means were:

```text
same-family        = 0.1515
different-family   = 0.1588
```

The difference was:

```text
-0.0073
```

The mean matched-stratum effect was:

```text
-0.0148
```

with a bootstrap interval of approximately:

```text
[-0.0547, +0.0280]
```

{{< figure src="/images/books/digital-life/ch11-outlier-distance-matched-coherence.png" caption="After matching spatial distance, simulation time and local density, same-family and different-family motion coherence become essentially indistinguishable." >}}

The interval crosses zero comfortably.

So we do **not** have evidence that causal-family membership independently predicts stronger motion coherence.

The dramatic earlier result disappeared when the spatial confound was controlled.

---

# Look at the effect by distance

The matched analysis is even clearer when split by distance.

{{< figure src="/images/books/digital-life/ch11-outlier-distance-matched-effect-by-distance.png" caption="Same-family minus different-family motion coherence after matching. Well-populated distance ranges show no consistent family advantage." >}}

Some individual bins fluctuate:

```text
0–4      +0.769
4–8      -0.188
8–12     -0.039
12–16    -0.030
16–24    +0.006
24–32    +0.049
32–48    -0.016
48–64    -0.070
64–96    +0.067
```

But the extreme bins contain very few matched examples.

For example:

```text
0–4 cells
13 matched pairs
```

is not comparable with:

```text
16–24 cells
26,228 matched pairs
```

The well-populated middle ranges show no systematic advantage for shared causal ancestry.

So the simplest current conclusion is:

> The apparent family-level motion coherence was largely explained by spatial organization.

---

# So was it flocking?

Not on the evidence we currently have.

But the original observation was not worthless.

We learned several things.

First:

```text
Outlier exhibits strong
short-range velocity coherence.
```

That is measurable.

Second:

```text
the coherence is not explained
by simple global radial expansion.
```

Third:

```text
shared c2 ancestry initially appears
to predict much stronger coherence.
```

But fourth:

```text
that apparent causal-family effect
disappears after matching spatial context.
```

So the bounded claim is:

> **Our Outlier reproduction exhibits strong local velocity coherence, but we do not find evidence in this experiment that shared c2 causal ancestry contributes additional coherence once spatial distance, simulation time, local density and local background motion are controlled.**

That is not as exciting as:

> We discovered flocking.

It is much better.

Because we have some idea what the evidence actually supports.

---

# What might the motion be?

Our best current interpretation is not:

```text
causal relatives
recognize one another
and flock
```

It is closer to:

```text
local geometry
+
local cellular dynamics
+
spatial organization
↓
coherent motion
```

That still matters.

Remember what Outlier is.

There are no explicit moving objects.

No velocity variable.

No steering force.

No alignment rule.

No flocking controller.

At the substrate level there are only:

```text
binary cells
local neighborhoods
one deterministic update rule
```

Yet from those rules emerge structures with coherent local motion.

That is already remarkable.

We simply should not give that phenomenon a stronger name than our measurements justify.

---

# The most important result may be methodological

This investigation began with five words:

> That looks like flocking.

If we had stopped there, we would have had a nice animation and a bad claim.

Instead:

```text
visual impression
↓
operational definition
↓
tracking
↓
velocity measurement
↓
shuffled control
↓
radial-flow control
↓
causal-family hypothesis
↓
local-flow control
↓
discover estimator bug
↓
pair-excluded control
↓
discover spatial confound
↓
distance/time/density matching
↓
bounded conclusion
```

This is exactly the process we need if we are going to talk seriously about digital life.

Interesting pictures are where questions begin.

Not where claims end.

---

# The database changed how we could work

There was another practical lesson.

Our simulation produced:

```text
138,891 clusters
196,466 causal edges
633,808 motion observations
```

Initially we recomputed these quantities every time we asked a new question.

That quickly became absurd.

So we created a SQLite database.

The expensive simulation became a reusable experimental dataset.

Conceptually:

```text
OUTLIER RUN
↓
SQLite
├── clusters
├── causal edges
├── c2 occurrences
├── causal return edges
├── motion tracks
├── motion observations
└── analysis results
```

Now a new hypothesis does not necessarily require another simulation.

It can begin with:

```text
SELECT ...
```

This matters beyond performance.

It changes how we investigate these systems.

The simulation becomes something closer to an experimental specimen.

We can ask multiple questions of the same run while preserving exactly which data each conclusion came from.

---

# Reproduction still survives the investigation

The flocking hypothesis weakened.

The reproduction story did not disappear with it.

We still observed:

```text
144 c2 occurrences
```

and constructed causal paths between recurring `c2` structures.

The original `c2` at:

```text
t = 2
```

lies at the root of a branching causal return structure.

So the evidence for reproduction is not:

```text
it looks like one object became several
```

It is:

```text
structural recurrence
+
causal ancestry
+
branching lineage
```

That distinction matters.

One of the deepest lessons from Outlier may therefore be this:

> **Geometry is not enough to tell us what an individual is.**

Two disconnected clusters may participate in the same causal process.

Two visually similar structures may not share the causal relationship we assume.

Several nearby structures may move coherently because of local dynamics rather than because they form a flock.

The visible world and the causal world do not have to divide themselves into objects in the same way.

---

# Perhaps individuality is causal

Biology makes physical boundaries extremely salient.

Skin.

Cell membranes.

Shells.

Bodies.

So we naturally begin digital life by looking for connected regions.

But a digital substrate does not owe us a membrane.

An individual might instead be something more like:

```text
a persistent causal organization
```

whose components can be:

```text
separated
rearranged
copied
distributed
```

That possibility is more interesting than whether Outlier happens to satisfy a biological checklist.

It asks us to reconsider the primitive concept itself.

Instead of:

> Where is the body?

we may need to ask:

> Which parts of this world participate in the same continuing causal organization?

That question will return later.

---

# What we did not prove

We should be explicit.

We have **not** shown that:

```text
Outlier is alive.
```

We have not shown classical flocking.

We have not shown that `c2` is necessarily the uniquely correct unit of individuality.

We have not shown that our counterfactual causal test captures every meaningful dependency.

We have not shown that connected clusters correspond to organisms.

And we have not shown open-ended evolution.

What we have shown in this experiment is narrower.

---

# Bounded claims

From this chapter we can reasonably claim:

### 1. Causal recurrence

Later `c2` structures can be connected to earlier `c2` structures through measured counterfactual dependencies in our reproduction of Outlier.

### 2. Branching lineage

The resulting causal return graph contains branching ancestry rather than mere isolated recurrence.

### 3. Local motion coherence

Persistent moving structures exhibit strong short-range directional alignment relative to a shuffled-velocity control.

### 4. Not merely radial expansion

Removing the global radial component does not eliminate that short-range coherence.

### 5. No demonstrated independent causal-family motion effect

Once pairs are matched for spatial distance, simulation time and local density, we find no detectable additional motion coherence associated with sharing the same recent `c2` ancestor.

That is where the evidence currently stops.

---

# And that is enough

There is a temptation in artificial life to treat every surprising pattern as a sign that we are almost there.

Almost alive.

Almost intelligent.

Almost social.

Almost evolutionary.

But that is backwards.

The interesting work begins when we stop rewarding the system for looking familiar.

Outlier gave us something that looked like reproduction.

So we asked whether the apparent descendants were causally connected.

Then it gave us something that looked like flocking.

So we measured the motion.

Then we tried to destroy our own explanation.

Again.

And again.

That is the method.

```text
SEE SOMETHING

↓ 

NAME THE HYPOTHESIS

↓

DEFINE THE MEASUREMENT

↓

BUILD THE CONTROL

↓

LOOK FOR THE CONFOUND

↓

BUILD A BETTER CONTROL

↓

KEEP ONLY WHAT SURVIVES
```

Digital life will not be discovered by finding the right metaphor.

It will be discovered by finding which properties survive this process.

---

# The deeper question

Outlier has now forced us to distinguish several ideas that initially looked like one:

```text
shape
identity
causal continuity
reproduction
collective motion
individuality
```

They are not the same thing.

A shape can recur without reproducing.

A structure can reproduce without having an obvious body.

Several disconnected structures can participate in one causal organization.

Nearby structures can move together without being a flock.

And genealogical relatedness does not necessarily determine current dynamical organization.

That suggests a different direction for digital life.

Perhaps we should stop asking:

> Which biological properties can we reproduce digitally?

And instead ask:

> What kinds of persistent causal organization become possible when the substrate is computation?

That is a much larger space.

And we have barely entered it.

