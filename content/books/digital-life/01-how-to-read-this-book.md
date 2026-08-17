+++
title = "01: How to Read the Experiments"
date = "2026-08-14T08:30:00+01:00"
draft = false
description = "This book can be read at several depths. A guide to the concepts, evidence, controls, claim boundaries and experimental record that make up the investigation."
weight = 1
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Experimental Method", "Evidence", "Controls", "Reproducibility", "Scientific Method"]
+++

This book can be read in more than one way.

You do not need to reproduce every experiment to follow the argument.

You do not need to inspect every number to understand what changed.

And you should not have to take the author's word for any result merely because you chose not to read the implementation.

The book operates at several depths.

They are all part of the same investigation.

**---**

## Five Kinds of Material

Most of what follows belongs to one of five categories.

```text
CONCEPT

EVIDENCE

CONTROL AND CONFOUND

CLAIM BOUNDARY

DEEP DIVE
```

They do different jobs.

### Concept

The **concept** is the intellectual step.

Why are we asking this question?

What assumption has become doubtful?

What new distinction has the previous experiment forced us to make?

A conceptual result might be:

```text
persistence
≠
reproduction
```

or:

```text
same visible state
≠
same dynamical regime
```

The concept tells you what changed in the argument.

It does not, by itself, tell you why you should believe the change.

That belongs to the evidence.

### Evidence

The **evidence** is the measurement that supports the step.

It may be a causal ancestry graph.

A damage-and-recovery experiment.

A population-turnover run.

A dose-response curve.

A comparison against an untouched control.

A number is not included merely because we measured it. It earns space when it bears directly on a claim.

The evidence reader should always be able to ask:

> **What observation made us change our mind?**

and find an answer.

### Control and Confound

The most important experiment is often not the experiment that produced the interesting result.

It is the one that tried to make the result go away.

A **control** asks whether an alternative explanation can produce the same observation.

A **confound** is the explanation we failed to remove.

Sometimes the first control works.

Often it does not.

Sometimes a control destroys the interpretation we wanted.

Those failures remain in the book because they are part of the result.

```text
observation
↓
interpretation
↓
control
↓
interpretation fails
↓
observation remains
```

That sequence will occur repeatedly.

### Claim Boundary

A **claim boundary** is where we state exactly what the evidence licenses.

These sentences are often less exciting than the idea that motivated the experiment.

That is deliberate.

Compare:

> The system remembers.

with:

> A system exposed to condition A responds differently to condition B than an otherwise matched system without that prior exposure.

The second sentence is narrower.

It is also something we can attack.

Throughout the book, pay special attention whenever the prose says:

```text
under this measurement

in this configuration

within this observation window

under this causal criterion

we did not establish

this does not imply
```

Those are not disclaimers pasted around a result.

They are the edges of the result.

### Deep Dive

The **deep dive** is the forensic record.

This is where the appendices live.

Parameters.

Seeds.

Thresholds.

Exact feature definitions.

Alternative metrics.

Discarded designs.

Implementation failures.

Runs that turned out to be incomparable.

Controls that failed.

Criteria frozen before results were inspected.

And sometimes the experiment we should have run first but did not think of until the third attempt.

That material is intentionally less clean than the main narrative.

The investigation was less clean.

**---**

## Three Ways Through the Book

You can therefore read the book at three useful depths.

### The conceptual path

Follow the argument.

Read the observations, the conceptual turns and the claim boundaries.

Skip a detailed protocol when you do not need it.

You should still understand:

```text
what we thought

what happened

what changed

what survived
```

without reproducing the experiment yourself.

### The evidence path

Read the experiments and the controls.

Stay with the numbers long enough to understand why the interpretation survived or failed.

This is where the scientific claim is actually earned.

The conceptual path tells you:

> we changed our mind.

The evidence path tells you:

> here is why.

### The reproduction path

Follow the experiment into the appendices and notebooks.

Inspect the configuration.

Check the implementation.

Re-run the seeds.

Change the threshold.

Try another metric.

Attack the result differently.

This is the level at which the book stops being something to read and becomes something to audit.

These are not the simplified and "real" versions of the book.

They are different depths of the same argument.

The conceptual reader can follow what changed.

The evidence reader can see why it changed.

The reproducing reader can inspect exactly how the result was obtained.

**---**

## The Shortest Version of Every Experiment

Almost every experimental chapter can be reduced to the same shape.

```text
WE SAW SOMETHING
↓
WE GAVE IT A NAME
↓
WE DEFINED WHAT THAT NAME WOULD REQUIRE
↓
WE MEASURED IT
↓
WE ATTACKED THE INTERPRETATION
↓
SOMETHING FAILED
↓
SOMETHING SURVIVED
```

The interesting part is usually the distance between the first noun and the final sentence.

A system may look as though it recovered.

The measurement may show that its untouched control wandered just as far.

A structure may look as though it reproduced.

The causal history may show only one continuing chain.

A dose may cross a threshold we declared in advance.

The rest of the dose-response curve may show that the apparent threshold was not a transition at all.

The book keeps the attractive interpretation only when it survives the inconvenient evidence.

**---**

## Numbers Are Local Until Proven Otherwise

One convention will save a great deal of confusion later.

**Do not assume that two numbers from different experiments are directly comparable merely because they have the same name.**

A "recovery score" may depend on a particular normalization.

A "control drift" may be estimated from different temporal blocks.

A "similarity" may use exact copies in one experiment and allow rotations in another.

A causal graph may be built under one counterfactual criterion while a published result uses another.

When those differences matter, the chapter should say so.

The default rule is:

> **A quantity belongs first to the experiment that defined it.**

Cross-experiment comparison has to be earned too.

This is one reason the appendices retain the exact measurement definitions rather than reducing everything to a single book-wide score.

There will be no:

```text
LIFE SCORE = 0.83
```

at the end.

That would hide exactly the distinctions we are trying to discover.

**---**

## Failure Is Part of the Record

The appendices are deliberately unclean.

That needs saying because scientific writing often creates the opposite impression.

A finished paper usually presents a straight line:

```text
question
↓
method
↓
result
↓
conclusion
```

The investigation rarely looked like that.

It looked more like:

```text
question
↓
bad metric
↓
interesting result
↓
confound
↓
better metric
↓
different result
↓
new hypothesis
↓
stronger control
↓
smaller claim
```

The wrong metric matters when it explains why the better one exists.

The failed control matters when it exposes an alternative explanation.

The discarded run matters when its failure changes the protocol.

We will not preserve every typo, debugging session or dead end.

But when a failure changed the scientific interpretation, it belongs to the record.

Otherwise the reader sees a conclusion without seeing what it survived.

**---**

## A Negative Result Is Not an Empty Result

There is another convention worth establishing before the experiments begin.

When an interpretation fails, the experiment has not necessarily failed.

Suppose we predict that damaging a particular mechanism will destroy a capability.

We damage it.

Nothing detectable happens.

That result may mean:

```text
the mechanism was not necessary

the intervention was too weak

the measurement was insensitive

another mechanism compensated

the hypothesis was wrong
```

The experiment has not selected among those possibilities automatically.

But it has changed what we know.

Sometimes the most important sentence in a chapter will be:

> **We could not claim what we expected to claim.**

That is not a narrative problem to be repaired.

It is often the discovery.

**---**

## Where to Slow Down

If you are reading quickly, there are three places where I would not skim.

### When the definition changes

If a chapter stops using one meaning of persistence, reproduction, identity or memory and replaces it with another, that change is usually the chapter.

### When the control changes the story

The first interpretation is often the attractive one.

The control is where we find out whether it was also the correct one.

### When the claim becomes smaller

A smaller claim after a stronger test is generally more valuable than a larger claim before one.

If the chapter begins with:

> it reproduced

and ends with:

> recurring structures participate in a branching causal ancestry graph under this criterion

the book has not retreated.

It has learned what it can actually say.

**---**

## What the Appendices Are For

The appendices are not where inconvenient detail goes to disappear.

They are where claims become inspectable.

A main chapter should tell you enough to understand:

```text
the question

the intervention

the measurement

the control

the result

the boundary
```

The appendix should let you inspect:

```text
the implementation

the parameters

the exact metric

the run structure

the seeds

the thresholds

the alternatives

the failures

the provenance
```

If the narrative and the experimental record ever disagree, the experimental record wins.

The prose is an interpretation of the experiment.

The experiment is not an illustration of the prose.

**---**

## One Book, Several Depths

So read at the depth that serves the question you have.

If you want the journey, follow the concepts.

If you want the justification, follow the evidence and controls.

If you want to challenge the work, follow it into the appendices.

You can move between those levels whenever something catches your attention.

The important thing is that they remain connected.

Every major conceptual turn should have evidence beneath it.

Every major claim should have a visible boundary around it.

Every important control should target a named alternative explanation.

And every result important enough to carry the argument should leave enough of a trail that someone else can attack it.

That is how to read the experiments.

It is also how the book was built.

**---**

The next chapter begins with the harder problem.

Before we can decide how strong the evidence is, we have to decide what would count as evidence at all.

Names will not be enough.

Resemblance will not be enough.

And biology, useful as it is, cannot simply hand us the specification.

So we begin with the question underneath everything that follows:

> **What would digital life mean?**