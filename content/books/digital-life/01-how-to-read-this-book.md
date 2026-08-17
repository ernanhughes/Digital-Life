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

You can follow the argument without reproducing every experiment.

You can understand what changed without inspecting every number.

And when you want to examine a result more closely, the implementation and experimental record are there to audit.

The book operates at several depths.

They are all part of the same investigation.

---

## Five Kinds of Material

Most of what follows belongs to one of five categories.

```text
CONCEPT

EVIDENCE

CONTROL AND CONFOUND

CLAIM BOUNDARY

DEEP DIVE
```

The **concept** is the intellectual step: what question changed, what assumption failed, what new distinction the experiment forced us to make.

For example:

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

The **evidence** is what made us change our mind: a measurement, intervention, ancestry graph, damage experiment or comparison against control.

A **control** attacks an interpretation. A **confound** is an alternative explanation we have not yet eliminated.

Sometimes the observation survives while the explanation does not:

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

A **claim boundary** says exactly what the evidence permits.

Compare:

> The system remembers.

with:

> A system exposed to condition A responds differently to condition B than an otherwise matched system without that prior exposure.

The second is narrower.

That is why it is useful.

Whenever you see phrases such as:

```text
under this measurement

in this configuration

within this observation window

we did not establish

this does not imply
```

those are not disclaimers around the result.

They are the edges of the result.

The **deep dive** is the forensic record: parameters, seeds, thresholds, implementation details, alternative metrics, discarded designs and failed controls. Most of that lives in the appendices.

The investigation was not clean.

The record should not pretend that it was.

---

## Three Ways Through the Book

You can therefore read at three useful depths.

The **conceptual reader** can follow what changed.

The **evidence reader** can see why it changed.

The **reproducing reader** can inspect exactly how the result was obtained.

```text
CONCEPT
what changed

EVIDENCE + CONTROLS
why it changed

APPENDICES + NOTEBOOKS
exactly how we tested it
```

These are not simplified and "real" versions of the book.

They are different depths of the same argument.

If a detailed protocol is not important to you, skip it.

If a result matters enough that you want to challenge it, follow it downward.

---

## The Shape of an Experiment

Most experimental chapters follow roughly the same sequence:

```text
WE SAW SOMETHING
↓
WE NAMED A HYPOTHESIS
↓
WE DEFINED WHAT WOULD COUNT AS EVIDENCE
↓
WE MEASURED IT
↓
WE ATTACKED THE INTERPRETATION
↓
SOMETHING FAILED
↓
SOMETHING SURVIVED
```

The interesting part is often the distance between the first noun and the final claim.

A system may look as though it recovered.

Then the untouched control may wander just as far.

A structure may look as though it reproduced.

Then its causal history may turn out to be one unbranching continuation.

A dose may cross a threshold declared in advance.

Then the rest of the dose-response curve may show that no transition occurred.

The book keeps the attractive interpretation only when it survives the inconvenient evidence.

---

## Numbers Are Local Until Proven Otherwise

Do not assume that two numbers from different experiments are directly comparable merely because they have the same name.

A recovery score may use a different normalization.

A control-drift estimate may come from different temporal blocks.

A similarity measure may allow rotations in one experiment and exact copies in another.

A causal graph may use a different counterfactual criterion.

So the default rule is:

> **A quantity belongs first to the experiment that defined it.**

Cross-experiment comparison has to be earned too.

There will be no final:

```text
LIFE SCORE = 0.83
```

because collapsing everything into one number would erase exactly the distinctions we are trying to discover.

---

## Failure Is Part of the Result

A finished scientific story often looks like this:

```text
question
↓
method
↓
result
↓
conclusion
```

The investigation usually looked more like:

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
smaller claim
```

The wrong metric matters when it explains why the better one exists.

The failed control matters when it destroys an attractive explanation.

And a negative result does not automatically mean the experiment failed.

If damaging a proposed mechanism produces no detectable change, several possibilities remain:

```text
the mechanism was not necessary

the intervention was too weak

the measurement was insensitive

another mechanism compensated

the hypothesis was wrong
```

The experiment does not choose among those automatically.

But it changes what we can honestly claim.

Sometimes the most important sentence in a chapter will be:

> **We could not claim what we expected to claim.**

That is often the discovery.

---

## What the Appendices Are For

The main text should let you understand:

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

the metric

the seeds

the thresholds

the failures

the provenance
```

The appendices are not where inconvenient detail goes to disappear.

They are where claims become inspectable.

If the narrative and the experimental record ever disagree, the experimental record wins.

The prose is an interpretation of the experiment.

The experiment is not an illustration of the prose.

---

## One Book, Several Depths

Read at the depth that serves your question.

Follow the concepts if you want the journey.

Follow the evidence and controls if you want the justification.

Follow the notebooks and appendices if you want to challenge the result.

The important thing is that those levels remain connected.

Every major conceptual turn should have evidence beneath it.

Every important control should attack a named alternative explanation.

Every major claim should have a visible boundary around it.

And every result important enough to carry the argument should leave enough of a trail that someone else can try to break it.

That is how to read the experiments.

It is also how the book was built.

---

The next chapter begins with the harder problem.

Before we can decide how strong the evidence is, we have to decide what would count as evidence at all.

Names will not be enough.

Resemblance will not be enough.

And biology, useful as it is, cannot simply hand us the specification.

So we begin with the question underneath everything that follows:

> **What would digital life mean?**