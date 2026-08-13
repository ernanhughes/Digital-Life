+++
title = "24: Where Is Causal Gain Created?"
date = "2026-08-13T01:10:00+01:00"
draft = false
description = "Chapter 24 tests whether causal gain can be localized to frontier geometry, exact motif, or recent process history—and finds that causal effect exists without becoming a stable local property."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Cellular Automata", "Experimental Method"]
series = ["Digital Life From First Principles"]
+++

Chapter 23 ended with a result that looked promising.

One forced frontier attachment could change what happened next.

The immediate neighbouring effect was measurable.

It was consistent with the local rule.

And after the initiating cell was removed, a small transient cascade remained before fading away.

That gave us a real causal quantity.

Not a metaphor.

Not a visual impression.

Not a classifier score.

A controlled intervention:

```text
SAME CHECKPOINT
SAME CELL
SAME FUTURE RANDOMNESS

FORCE x
vs
PREVENT x

↓
MEASURE DIFFERENCE
```

The obvious next question was:

> **Where in the crystal is that causal gain created?**

If some parts of the active interface were more causally potent than others, perhaps we could map them.

Perhaps the crystal contained high-gain and low-gain regions.

Perhaps those regions persisted.

Perhaps they connected.

And perhaps, much later, a stable organization could emerge from them.

That was the hope.

Chapter 24 tested it three different ways.

Each time, the local description became richer.

Each time, the gain relationship failed.

What survived was not a causal-gain field.

It was a more uncomfortable result:

> **Causal effect exists without becoming a stable local property under the representations we tested.**

That is the chapter.

---

# From Causal Effect to Causal Location

Chapter 23 had already warned us not to confuse several different quantities.

A local intervention could produce:

```text
IMMEDIATE MECHANICAL EFFECT
```

then:

```text
SHORT-RANGE DOWNSTREAM CONSEQUENCE
```

while finite computational budget could redistribute construction elsewhere.

So even before Chapter 24 began, we knew:

```text
LOCAL GAIN
≠
GLOBAL GAIN
```

and:

```text
TRANSIENT CASCADE
≠
PERSISTENT STATE EFFECT
```

But the Chapter 23 experiments had also shown something striking.

Sparse and dense frontier locations reacted very differently to the same forced attachment.

A sparse frontier cell could create new construction opportunity.

A dense frontier cell could consume an existing frontier position while creating almost nothing new.

That suggested a possible causal substrate law:

```text
LOCAL GEOMETRY
↓
OPPORTUNITY TRANSFORMATION
↓
CAUSAL GAIN
```

Chapter 24 began there.

---

# V1 — Frontier Creation Potential

The first experiment introduced a deliberately simple observer quantity.

For an eligible frontier site `x`, define:

```text
FCP(x)
=
|frontier after forcing x occupied|
-
|frontier before forcing x|
```

We called this:

# **Frontier Creation Potential**

The interpretation was direct.

If:

```text
FCP > 0
```

then forcing `x` expanded the set of currently available construction opportunities.

If:

```text
FCP = 0
```

then the intervention rearranged opportunity without changing its total count.

If:

```text
FCP < 0
```

then occupying `x` consumed more frontier opportunity than it created.

This was not a claim about energy.

Not metabolism.

Not fitness.

Just a count of how one local state change altered the next available construction surface.

---

## The Frozen Question

The experiment did not simply correlate FCP with later growth.

That would have been too weak.

High-FCP and low-FCP sites were matched within the same independent checkpoint on:

```text
same occupied-neighbour count
same radial bin
baseline attachment probability within 0.05
local frontier density within 0.10
```

and required to differ by at least one unit of FCP.

Each site then received the same transient intervention used at the end of Chapter 23:

```text
FORCE x
vs
PREVENT x

↓
one full causal update

↓
remove x from FORCE

↓
continue ordinary dynamics
```

The primary target was:

```text
G_T(12)
```

the cumulative local transient construction gain over twelve future updates.

The frozen hypothesis was:

> **Among locally comparable frontier sites, forcing a site that creates more frontier opportunity will produce greater transient causal gain.**

The required mean effect was:

```text
+0.15 attachments
```

with a bootstrap interval entirely above zero and a one-sided group-level sign-flip test below `0.05`.

---

# The Geometry Manipulation Worked

The run was exceptionally clean.

All:

```text
48 / 48
```

groups produced matched pairs.

There were:

```text
356 matched high/low pairs
```

with roughly:

```text
7.4 pairs per group
```

and the lattice remained far from its hard capacity boundary.

The construct-validity result was strong.

High-FCP sites promoted:

```text
+1.259
```

more ring-one frontier cells than matched low-FCP sites.

The 95% interval was:

```text
[1.196, 1.325]
```

and the sign-flip probability was approximately:

```text
0.000125
```

So Frontier Creation Potential was not empty bookkeeping.

It identified a real and reproducible difference in how an attachment transformed immediate construction opportunity.

That claim survived.

---

# But the Gain Link Failed

The primary result was:

```text
G_T(high FCP)
-
G_T(low FCP)

mean
= +0.167
```

The point estimate was just above the frozen minimum effect of `+0.15`.

But the uncertainty was large:

```text
95% CI
[-0.078, +0.431]
```

and:

```text
p = 0.105
```

The hypothesis failed.

That distinction matters.

We did not say:

> The effect was nearly significant.

We said:

> **The frozen experiment did not establish the claim.**

The manipulation succeeded.

The predicted causal consequence did not.

That is exactly what a useful experiment should be able to show.

---

## The Descriptive Map Looked Tempting

The descriptive FCP bins looked much more exciting:

```text
FCP     mean transient gain

-1      0.014
 0      0.145
+1      0.173
+2      0.535
```

At first glance, that looked like a strong gradient.

But the rank correlation across sites was almost zero:

```text
Spearman(FCP, gain)
≈ 0.043
```

The same pattern appeared in the other simple local variables.

None provided a strong monotonic map of transient gain.

So the descriptive result suggested something more irregular.

Perhaps FCP was not a continuously meaningful field.

Perhaps particular local geometries mattered.

That led to V2.

---

# V2 — Exact Local Frontier Motifs

A frontier cell on a hexagonal lattice has six immediate neighbours.

Each neighbour can be:

```text
occupied
or
empty
```

so the ring around the cell can be represented as six bits:

```text
b0 b1 b2 b3 b4 b5
```

There are:

```text
2^6 = 64
```

raw patterns.

After accounting for rotation and reflection, far fewer distinct local motifs remain.

The idea was simple.

Two frontier sites could have the same number of occupied neighbours but arrange them differently.

For example, two occupied neighbours could be:

```text
adjacent
```

or:

```text
separated by one gap
```

or:

```text
opposite
```

Those geometries can transform frontier opportunity differently even when the occupied-neighbour count is identical.

So perhaps the scalar summaries in V1 had compressed away the real causal object.

---

## The V2 Question

V2 again avoided asking which motif happened to have the largest average gain.

Instead it used an omnibus test.

Sites were matched on:

```text
same occupied-neighbour count
same radial bin
baseline attachment probability within 0.05
local frontier density within 0.10
```

Then two pair families were built.

One pair family contained:

```text
SAME-MOTIF PAIRS
```

The other contained:

```text
CROSS-MOTIF PAIRS
```

The primary statistic was:

```text
mean |gain difference| across cross-motif pairs

minus

mean |gain difference| across same-motif pairs
```

If exact local arrangement mattered beyond the matched scalar state, cross-motif pairs should diverge more strongly.

The frozen minimum effect was:

```text
+0.20 attachments
```

---

# V2 Failed Harder Than V1

The run was again valid.

Out of 48 groups:

```text
45
```

contained both same-motif and cross-motif pairs.

Coverage was:

```text
93.75%
```

The experiment measured:

```text
1,536 intervention sites
95 cross-motif pairs
145 same-motif pairs
```

across:

```text
12 observed canonical motif classes
```

The primary result was:

```text
cross-motif |Δ gain|
-
same-motif |Δ gain|

mean
= -0.225
```

with:

```text
95% CI
[-0.692, +0.307]

p
= 0.802
```

The predicted effect did not merely fail to clear the threshold.

The point estimate went in the opposite direction.

The opportunity-transformation test also failed:

```text
cross-motif |Δ promoted frontier|
-
same-motif |Δ promoted frontier|

mean
= +0.040
```

with:

```text
95% CI
[-0.092, +0.170]

p
= 0.272
```

So the exact six-neighbour motif did not add detectable information beyond the scalar state variables we had already matched.

---

# But V2 Taught Us Something About Conditioning

The descriptive motif atlas looked more interesting than the omnibus result.

For the three `n = 2` arrangements:

```text
motif type       FCP       promoted     transient G

adjacent        +0.174      1.174         0.391
one-gap         -0.580      0.420         0.094
opposite        -1.000      0.000         0.043
```

That looked almost exactly like the motif story.

But there was a catch.

Their baseline attachment probabilities were very different.

The adjacent configuration had a mean probability near:

```text
0.212
```

while the one-gap and opposite configurations were both near:

```text
0.57
```

The exact geometry was already influencing the frozen attachment rule.

That meant our V2 matching did something very specific.

It did not ask:

> Does local motif affect the system?

It asked:

> **Does motif add a residual effect after holding tightly fixed a quantity that motif itself may already help determine?**

That is still a valid causal question.

But it is narrower.

The answer was:

> **No detectable residual effect under this protocol.**

We had not discovered that geometry was irrelevant.

We had discovered that exact motif was not an independent local gain variable once the measured present-state summaries were controlled.

That left one qualitatively different possibility.

Perhaps the present snapshot itself was insufficient.

---

# V3 — Recent Local Process History

Two frontier sites can look the same now while having arrived there differently.

One region may have recently experienced:

```text
attachment
loss
reoccupation
evaluation
turnover
```

while another geometrically similar region may have been quiet.

If causal leverage depended on active process rather than instantaneous geometry, then present-state matching could erase the evidence.

So V3 stopped adding more spatial features.

It added time.

---

## The Process-History Variable

For every evaluated frontier site, V3 looked backward over the previous:

```text
6 updates
```

within a local hex radius of:

```text
2 cells
```

It measured:

```text
recent attachments
recent losses
recent reoccupations
recent first occupations
recent evaluations
```

The predeclared primary history variable was:

```text
RECENT TURNOVER
=
recent attachments
+
recent losses
```

No classifier was allowed.

No post-hoc selection of whichever history feature worked best.

No changing the time window after seeing the result.

---

## Present State Was Matched Even More Tightly

High-turnover and low-turnover sites had to share:

```text
the same canonical six-neighbour motif
the same radial bin
baseline attachment probability within 0.05
current local frontier density within 0.10
FCP within 1
```

and they had to differ by at least:

```text
2 recent material events
```

The causal intervention remained unchanged:

```text
FORCE
vs
PREVENT

one causal update

remove x

continue to H = 12
```

The primary hypothesis was:

> **Among sites with comparable present geometry, regions with greater recent material turnover will produce greater transient causal gain.**

Again, the frozen minimum effect was:

```text
+0.15 attachments
```

---

# The History Manipulation Was Enormous

All:

```text
48 / 48
```

groups produced pairs.

There were:

```text
384 matched pairs
```

exactly:

```text
8 per group
```

The high-turnover sites exceeded the low-turnover sites by:

```text
7.734 recent events
```

on average.

The 95% interval was:

```text
[7.365, 8.102]
```

with:

```text
p ≈ 0.000125
```

This was not a subtle history contrast.

It was large.

The components showed the same separation.

High-turnover sites had approximately:

```text
+3.77 recent attachments
+3.97 recent losses
+3.18 recent reoccupations
+0.59 recent first occupations
+3.28 recent evaluations
```

relative to the matched low-turnover sites.

The construct-validity test passed decisively.

Then H1 failed.

---

# Recent Process History Did Not Predict Gain

The primary result was:

```text
G_T(high turnover)
-
G_T(low turnover)

mean
= -0.065
```

with:

```text
95% CI
[-0.221, +0.096]

p
= 0.791
```

The point estimate was again in the wrong direction.

This was not a weak manipulation failing to produce a measurable consequence.

The recent histories differed dramatically.

The gain did not.

---

## The Descriptive Results Were Almost Flat

Across:

```text
768 intervention sites
```

the descriptive rank correlation between recent turnover and transient gain was:

```text
0.0023
```

Essentially zero.

The other history components were also tiny:

```text
recent attachments       +0.0046
recent losses            -0.0020
recent reoccupations     -0.0205
recent first occupation  +0.0592
recent evaluations       +0.0638
```

The binned turnover means bounced above and below zero without a coherent trend.

For example:

```text
turnover 2   → +0.447
turnover 3   → -0.147
turnover 4   → +0.361
turnover 5   → -0.259
turnover 12  → -0.079
turnover 15  → +0.220
turnover 17  → +0.429
turnover 18  → -0.032
```

There was no monotonic process-history law hiding underneath the failed matched test.

---

# The Stop Rule Fired

Before V3 ran, the rule was explicit.

If recent turnover failed on a valid run:

```text
do not change the history radius
do not change the history window
do not drop motif matching
do not select another history component
do not add a classifier
```

That rule now applies.

No V4.

Chapter 24 is complete.

---

# Three Ways to Localize Gain

We have now tried three increasingly rich local descriptions.

## V1 — Scalar Opportunity Geometry

```text
Frontier Creation Potential
```

Question:

> Does creating more frontier opportunity produce greater transient causal gain?

**FAILED**

The geometry contrast itself was strongly supported.

The gain link was not.

---

## V2 — Exact Present Motif

```text
canonical six-neighbour arrangement
```

Question:

> Does exact local arrangement add gain information beyond matched scalar state?

**FAILED**

Neither transient gain nor immediate opportunity transformation showed the frozen cross-motif excess.

---

## V3 — Recent Local Process History

```text
six-step local material turnover
```

Question:

> Does recent local process history add gain information beyond matched present state?

**FAILED**

The history contrast was enormous.

The gain difference was slightly negative.

---

# What Survived the Hypothesis?

The chapter did not end empty.

Several claims survived.

## Frontier geometry changes immediate opportunity

> **Matched frontier sites can differ strongly in how one attachment transforms the immediate construction frontier.**

**Status: SUPPORTED**

V1 showed a large, reproducible difference in promoted frontier opportunity.

---

## Exact motif adds residual gain information

> **Exact six-neighbour motif predicts transient causal gain beyond matched present-state summaries.**

**Status: FAILED**

V2 produced no such effect.

---

## Recent turnover adds gain information

> **Recent local material turnover predicts transient causal gain beyond matched present geometry.**

**Status: FAILED**

V3 produced no such effect.

---

## Local causal effect exists

This claim comes from Chapter 23 and remains intact:

> **Forcing one frontier attachment changes subsequent local construction.**

**Status: SUPPORTED**

Chapter 24 did not undo that.

It changed what we can say about where that causal leverage belongs.

---

# Causal Effect Is Not a Local Property

This is the central distinction Chapter 24 earned:

```text
A LOCAL CAUSAL EFFECT EXISTS
```

does not imply:

```text
THERE EXISTS A STABLE LOCAL
CAUSAL-GAIN PROPERTY
```

The first is interventional.

The second is representational.

Chapter 23 established the intervention.

Chapter 24 tried to construct the representation.

It failed.

That failure matters.

We cannot currently point at a frontier site and say:

```text
this is a high-gain location
```

using:

```text
how much frontier it would create
its exact six-neighbour motif
its recent local turnover
```

with the level of evidence required by this project.

That does not mean gain is random in some metaphysical sense.

It means the local descriptions we tested do not carry a stable enough relationship to transient causal consequence.

The future depends on more than the present local label.

---

# Perhaps Gain Is Not Stored Anywhere

The wording of the chapter title now looks suspicious.

> Where is causal gain created?

Maybe that assumes too much.

The experiment increasingly suggests:

```text
INTERVENTION
↓
enters a stochastic finite-budget process
↓
changes local opportunity
↓
changes which candidates are evaluated
↓
changes some attachments
↓
changes later opportunity
↓
effect dissipates or redistributes
```

The causal consequence may be generated through that unfolding interaction rather than residing in a stable local state beforehand.

In that picture, asking:

```text
where is the gain?
```

is like asking where a traffic jam is stored before the cars meet.

The ingredients may exist locally.

The consequence emerges from their interaction under shared constraints.

That is not yet a claim about emergence.

It is simply a warning against reifying an observer quantity that the experiments have not recovered.

---

# A Recurring Pattern: Local Gain, Far-Field Compensation

One phenomenon kept appearing while the local-predictor hypotheses failed.

Some interventions showed:

```text
positive local construction difference
```

together with:

```text
negative far-field construction difference
```

In V1, for example, the high-versus-low FCP comparison produced approximately:

```text
local difference      +0.167
far-field difference  -0.213
global difference     -0.046
```

The intervals were wide.

So that particular contrast did not establish a new quantitative law.

But the pattern had appeared before.

Several sparse motifs in V2 showed the same structure.

For the one-neighbour motif:

```text
local gain      ≈ +0.335
far-field gain  ≈ -0.252
global gain     ≈ +0.083
```

For one adjacent two-neighbour motif:

```text
local gain      ≈ +0.431
far-field gain  ≈ -0.333
global gain     ≈ +0.097
```

A local intervention can apparently change where construction happens much more strongly than it changes total construction.

That points away from a local gain reservoir.

And toward a shared resource.

---

# Finite Computation Is a Global Constraint

The Digital Crystal does not evaluate every available frontier cell at every update.

Chapter 21 introduced a finite evaluation budget.

At each step, only a bounded number of candidate opportunities are considered.

That means distant locations are coupled even if the attachment rule itself is local.

Not because a signal travels between them.

Because they compete for access to the same finite computational process.

Schematically:

```text
LOCAL OPPORTUNITY A
        ↓
FINITE EVALUATION BUDGET
        ↑
LOCAL OPPORTUNITY B
```

If one intervention creates more attractive or more numerous nearby opportunities, those opportunities can consume evaluations that would otherwise occur elsewhere.

Then:

```text
LOCAL POSITIVE EFFECT
```

can coexist with:

```text
FAR-FIELD NEGATIVE EFFECT
```

without requiring any travelling influence between the two regions.

That is a substrate-level coupling.

And it may be much more important than the local gain map we originally went looking for.

---

# A New Candidate Phenomenon

The phenomenon ledger should now carry a new candidate:

# **Finite-Budget Redistribution**

Operational form:

> **Local interventions can alter where construction occurs without producing a corresponding increase in total construction, because spatially separated opportunities compete for a finite global evaluation budget.**

For now, this should remain bounded.

The repeated local/far-field pattern motivates it.

But Chapter 24 did not freeze a dedicated redistribution hypothesis.

So we should not upgrade it into a law yet.

The chapter has earned the question.

Not the answer.

---

# What Chapter 24 Does Not Establish

It does not establish:

```text
a causal-gain field
high-gain regions
stable gain states
coherent structures
criticality
percolation
a phase transition
a natural boundary
autonomy
individuality
an organism
life
```

It also does not establish that gain is fundamentally unpredictable.

We tested specific local representations.

Those representations failed.

That boundary must remain explicit.

The correct statement is:

> **Under the tested Digital Crystal protocol, transient causal gain was not reliably localized by Frontier Creation Potential, exact six-neighbour motif, or recent local material turnover after the corresponding controls were applied.**

Nothing larger is required.

---

# What We Have Earned

Chapter 23 gave us:

```text
LOCAL CAUSAL EFFECT
```

Chapter 24 tried to turn that into:

```text
LOCAL CAUSAL PROPERTY
```

and failed.

That gives us a new progression:

```text
LOCAL INTERVENTION
↓
MEASURABLE LOCAL CONSEQUENCE
↓
NO STABLE LOCAL GAIN VARIABLE FOUND
↓
CONSEQUENCE DEPENDS ON UNFOLDING PROCESS
AND SHARED COMPUTATIONAL CONSTRAINT
```

This may be more useful than the high-gain-region story we expected.

Because now the next question changes scale.

Not upward toward an organism.

Sideways toward constraint.

---

# Next: Where Does the Causal Effect Go?

If local construction can increase while distant construction decreases, then the next experiment should stop asking:

> Which location has more gain?

and ask:

> **When one region gains construction, where is the corresponding difference expressed elsewhere?**

That is a new causal question.

The experiment should partition the crystal into spatial bands around an intervention:

```text
INTERVENTION SITE
↓
RING 1–2
RING 3–5
RING 6–10
FAR FIELD
```

and separately measure:

```text
attachment difference
evaluation difference
loss difference
reoccupation difference
net population difference
```

Then vary the global evaluation budget:

```text
B = 24
B = 48
B = 96
B = 192
unbounded reference
```

The key question becomes:

> **Does finite computation induce long-range competition between otherwise local construction processes?**

If the redistribution weakens as the budget rises and disappears in the unbounded reference, that would identify a genuine substrate mechanism.

Not a metaphorical energy.

Not biological metabolism.

A computational constraint creating non-local coupling.

The path forward is now:

```text
LOCAL CAUSAL EFFECT
↓
NO STABLE LOCAL GAIN STATE
↓
FINITE GLOBAL COMPUTATIONAL CONSTRAINT
↓
DO LOCAL PROCESSES COMPETE?
↓
DOES COMPETITION CREATE
SYSTEM-LEVEL ORGANIZATION?
```

Chapter 24 began by asking where causal gain was created.

The answer is not that we found the wrong place.

The stronger result is:

> **We did not find evidence that transient causal gain belongs to a stable local place at all.**

The effect exists.

The location does not yet.
