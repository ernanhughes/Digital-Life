+++
title = "29: How to Fail Correctly"
date = "2026-08-14T00:12:00+01:00"
draft = false
description = "Chapter 29 turns the recent experiment failures into a reproducible epistemic method: distinguish invalid runs, unresolved questions, bounded negative results, and supported findings narrowed by stronger controls."
weight = 29
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Finite Computation", "Experimental Method", "Cellular Automata"]
series = ["Digital Life From First Principles"]
+++

By the time we reached Chapter 28, the Digital Crystal had accumulated an uncomfortable history.

Several experiments had looked convincing.

Some had even produced large effects.

Then a stronger control arrived.

Or an implementation defect was discovered.

Or the original question turned out to contain two different questions.

Or a result remained directionally clear but failed the predeclared magnitude requirement.

The easy response would have been to describe all of these as failures.

That would have been wrong.

A failed implementation is not the same thing as evidence against a hypothesis.

An unresolved result is not the same thing as a negative result.

A precise negative result is not the same thing as nothing happening.

A stronger control that narrows an interpretation does not erase the lower-level phenomenon that survived.

Those distinctions had become important enough that they could no longer remain informal.

So Chapter 29 stopped asking another question about the crystal.

Instead, it asked a question about the investigation itself:

> **When an experiment appears to fail, can we determine exactly what failed without silently changing the question, erasing surviving evidence, or converting an invalid run into a negative result?**

This chapter is about epistemic bookkeeping.

Not as administration.

As science.

---

# Failure is not one thing

The word *failure* compresses several very different situations.

Suppose an experiment does not support the claim we wanted.

At least four possibilities immediately exist.

The implementation may have been invalid.

The experiment may have been valid but too imprecise.

The experiment may have been valid and precise enough to bound the effect below a meaningful threshold.

Or the lower-level result may still be supported while a stronger interpretation fails under a better control.

Those are not stylistic differences.

They imply different things about what we are allowed to conclude.

The working taxonomy became:

```text
INVALID

UNRESOLVED

BOUNDED NEGATIVE

SUPPORTED BUT NARROWED
```

Later we also needed:

```text
DESCRIPTIVE CLOSEOUT
```

because a post hoc mechanism can explain a result without changing its confirmatory status.

The core rule was simple:

> **FAILURE OF A CLAIM ≠ FAILURE OF AN EXPERIMENT ≠ ABSENCE OF A PHENOMENON**

Chapter 29 tested whether our own recent experiment history actually respected that distinction.

---

# Building the failure ledger

The audit registered ten cases from Chapters 26 through 28.

Each case recorded:

- the claim being tested,
- whether the run itself was valid,
- the inferential status,
- the kind of transition that occurred,
- the role of the evidence,
- the relevant threshold where one existed,
- the expected mean, interval and MDE where available,
- and, critically, what evidence survived.

The registered validity categories were:

```text
VALID
INVALID_IMPLEMENTATION
INVALID_CONSTRUCT
INVALID_REFERENCE
UNKNOWN
```

The inferential statuses were:

```text
SUPPORTED
BOUNDED_BELOW_SEI
BOUNDED_NEAR_ZERO
UNRESOLVED
DIRECTION_SUPPORTED
DESCRIPTIVE_ONLY
INVALID
UNTESTED
```

And the transitions included:

```text
IMPLEMENTATION_INVALIDATION
CONSTRUCT_NARROWING
PRECISION_RESOLUTION
PRECISION_LIMIT
MECHANISTIC_DECOMPOSITION
DESCRIPTIVE_CLOSEOUT
REPLICATION
CONTROL_STRENGTHENING
```

The point was not to create vocabulary for its own sake.

The point was to make illegal moves visible.

---

# The forbidden moves

The Chapter 29 protocol explicitly banned six common forms of epistemic slippage.

We could not:

```text
count INVALID as evidence against the hypothesis
```

We could not:

```text
count CI-crossing-zero as FAILED
```

We could not:

```text
call a result bounded negative without an explicit meaningful threshold
```

We could not:

```text
erase valid sub-results when a larger inference became invalid
```

We could not:

```text
promote a descriptive closeout into confirmatory rescue
```

And we could not:

```text
silently change the estimand or control after seeing the result
```

This is less glamorous than generating a strange new Digital Crystal behavior.

It is also more important.

Because without these rules, every later claim can be rewritten after the fact until the project appears cleaner than it really was.

---

# Chapter 26: when the reference is wrong

Chapter 26 began with a plausible question.

If finite computation forces the system to subsample its frontier, does that amplify the downstream causal consequence of a local perturbation?

The first design tried to match background construction rate between bounded and effectively exhaustive evaluation.

But the matching was incomplete.

The calibration was fixed from an early condition rather than dynamically matched across the process.

Worse, the supposedly exhaustive `f = 1` reference was not actually the same thing as true unbounded evaluation.

The comparison was therefore not the comparison the experiment claimed to make.

That made the V1 primary:

```text
INVALID_REFERENCE
```

The correct conclusion was not:

> no causal amplification exists.

The correct conclusion was:

> this experiment does not establish the answer.

That distinction matters.

An invalid reference arm provides no clean negative evidence against the hypothesis.

The failure belongs to the experiment design.

Not to the phenomenon.

The lesson became:

> **A controlled initial condition is not a controlled process.**

---

# Correcting Chapter 26

V2 rebuilt the comparison properly.

The PREVENT branch was dynamically matched at every lag.

The exhaustive comparison became genuinely unbounded.

The frozen horizon remained twelve steps.

The smallest meaningful difference was:

\[
\pm 0.15
\]

The result was:

\[
\Delta G
\approx
0.0013
\]

with confidence interval approximately:

\[
[-0.0898,\ 0.0885]
\]

The achieved MDE was approximately:

\[
0.115
\]

which was inside the frozen 0.15 meaningful threshold.

So the result was not merely nonsignificant.

It was precision-resolved.

Strong candidate subsampling did not produce a mean twelve-step causal consequence differing meaningfully from exhaustive evaluation under the matched-rate protocol.

That became:

```text
BOUNDED_NEAR_ZERO
```

But something else survived.

---

# A negative aggregate can hide a changed mechanism

The Chapter 26 mechanism audit decomposed the immediate causal effect.

Under strong subsampling, much of the local effect came from:

```text
force-only opportunities
```

Under exhaustive evaluation, more of it came from:

```text
shared probability shifts
```

The aggregate consequence stayed matched.

The pathway changed.

That produced another construct separation:

> **CAUSAL ROUTING ≠ CAUSAL AMPLIFICATION**

This is exactly the kind of evidence that gets lost if we summarize Chapter 26 as:

> the experiment failed.

It did not fail.

The first design was invalid.

The corrected primary bounded amplification near zero.

And the mechanism audit revealed a genuine change in causal routing.

Three different epistemic outcomes existed inside one chapter.

The ledger had to preserve all three.

---

# Chapter 27: when the intervention itself is wrong

Chapter 27 made the distinction even sharper.

V1 tested whether hidden material state could redirect future causal response.

The design compared:

```text
FORCE
```

against:

```text
PREVENT
```

But the PREVENT branch contained a defect.

At lag 1, the supposedly prevented site was not explicitly excluded from ordinary attachment.

That meant the intervention could partially undo itself.

The twelve-step primary effect was therefore:

```text
INVALID_IMPLEMENTATION
```

Again, the invalid run was not negative evidence.

But this time something stronger happened.

Not every part of the experiment depended on the defective downstream intervention semantics.

The immediate expected causal effect remained interpretable.

And that immediate result was strong.

Locally accessible decaying material reduced immediate causal sensitivity.

So Chapter 27 V1 simultaneously contained:

```text
INVALID PRIMARY
```

and:

```text
SUPPORTED SUB-RESULT
```

This forced a more precise rule:

> **Invalidate only the inference touched by the defect. Preserve independently valid sub-results.**

That is harder than throwing the run away.

It is also more honest.

---

# Correcting Chapter 27

V2 fixed the intervention.

PREVENT explicitly blocked the target at lag 1.

FORCE exposed the target for exactly one growth step.

Both branches then removed it and resumed ordinary dynamics.

The corrected primary used a Rao-Blackwellized downstream causal consequence.

The mean accessible-versus-remote difference was approximately:

\[
-0.397
\]

with 95% confidence interval:

\[
[-0.679,\ -0.119]
\]

The interval excluded zero.

So the direction was supported.

But the achieved MDE was approximately:

\[
0.357
\]

against a frozen meaningful threshold of:

\[
0.15
\]

That meant the experiment could support the sign without establishing the predeclared minimum magnitude.

The correct classification was therefore split:

```text
DIRECTION_SUPPORTED
```

and:

```text
MINIMUM_MAGNITUDE_UNRESOLVED
```

This gave us another identity:

> **DIRECTIONAL EFFECT ≠ ESTABLISHED MINIMUM MAGNITUDE**

A conventional summary might have called the experiment successful because the interval excluded zero.

Our protocol would not allow that shortcut.

The scientific question had included a magnitude requirement.

So the magnitude question remained unresolved.

---

# The closeout did not rescue the claim

The Chapter 27 trajectory audit found something fascinating.

A substantial share of the downstream causal difference continued to accumulate after the material trace had fallen below half of its initial mass.

The result was consistent with:

```text
early material-state modulation
→ early construction difference
→ redirected later trajectory
```

rather than a purely contemporaneous bias.

That was useful.

But it was descriptive.

It did not change the frozen confirmatory magnitude status.

The ledger therefore recorded:

```text
DESCRIPTIVE_TRAJECTORY_PERSISTENCE
```

while leaving:

```text
MINIMUM_MAGNITUDE_UNRESOLVED
```

untouched.

This protects against a subtle rescue pattern.

When the primary result weakens, it is tempting to run another analysis, find something interesting, and let the interesting mechanism retroactively improve the original claim.

Chapter 29 forbids that.

> **A descriptive explanation can illuminate a result without rescuing its confirmatory status.**

---

# Chapter 28: when a strong result is still the wrong construct

Chapter 28 was the most dangerous case because the first result was not weak.

It was extremely strong.

The raw causal modularity score at radius 4 was approximately:

\[
0.440
\]

with confidence interval:

\[
[0.419,\ 0.461]
\]

against a frozen meaningful threshold of:

\[
0.15
\]

The result was precise.

It was supported.

Internal perturbations expressed much more causal mass inside the selected region than external perturbations penetrated into it.

Nothing about the raw measurement was wrong.

The problem was construct validity.

The module score increased as the disk radius increased.

That suggested a simple alternative explanation:

```text
local causal propagation
+
observer-drawn containment
```

could generate the same effect.

The issue was no longer:

> is the module score real?

It was:

> does the module score indicate a privileged causal individual?

Those are different claims.

---

# The stronger control

Chapter 28 V2 kept the same radius, same intervention, same causal-mass definition and same unbounded dynamics.

It added same-checkpoint geometry-matched controls.

Each selected region was compared against other radius-4 regions matched on:

```text
occupancy fraction
radial position
occupied count
internal frontier count
external frontier count
probe depth
boundary occupancy
```

The observed regions still showed a large module score:

\[
0.4436
\]

The matched controls showed:

\[
0.4559
\]

The excess was:

\[
-0.0123
\]

with 95% confidence interval:

\[
[-0.0327,\ 0.0072]
\]

The frozen meaningful excess threshold was:

\[
+0.10
\]

The achieved MDE was only:

\[
0.0265
\]

This was a precision-bounded negative result.

The selected regions were not meaningfully more modular than matched arbitrary regions.

So the stronger interpretation failed.

But the V1 phenomenon remained.

This is the key distinction:

```text
RAW CAUSAL CONTAINMENT
SUPPORTED
```

while:

```text
PRIVILEGED CAUSAL REGION
NOT ESTABLISHED
```

The resulting identity was:

> **CAUSAL RETENTION ≠ CAUSAL INDIVIDUATION**

A stronger control narrowed the claim.

It did not erase the earlier measurement.

---

# The audit

Chapter 29 then ran the ledger against the actual project artifacts.

All ten registered cases had source artifacts.

No case required invented values.

No case depended on manual evidence alone.

The audit checked:

```text
10 registered cases
```

and:

```text
10 / 10 passed their consistency rules
```

Five cross-case checks were also predeclared.

All five passed.

The checks verified that:

1. Chapter 27's invalid V1 primary preserved the independently valid immediate effect.
2. Chapter 27 separated directional support from minimum-magnitude support.
3. Chapter 28's stronger control narrowed the claim without erasing raw containment.
4. Chapter 26's bounded aggregate result preserved mechanistic rerouting.
5. Chapter 27's descriptive closeout did not rescue the unresolved confirmatory magnitude claim.

The final status was:

```text
FAILURE_LEDGER_CONSISTENT
```

That status does not mean the project never made mistakes.

It means the mistakes and weakened claims can be represented without turning one evidence class into another.

That is a much more modest result.

And a much more useful one.

---

# Construct separation

The failure ledger also made visible a pattern that had been accumulating throughout the book.

Again and again, two things that initially seemed interchangeable turned out not to be.

Earlier chapters had already established distinctions such as:

```text
MARGINAL EFFECT
≠
AVERAGE PAIRED EFFECT

AVERAGE PAIRED EFFECT
≠
PATHWISE DIVERGENCE

CAUSAL DIFFERENCE
≠
SYSTEMATIC SIGNATURE

PERSISTENT TRACE
≠
READABLE TRACE

ATTACHMENT
≠
NEW CONSTRUCTION

REOCCUPATION
≠
REPAIR
```

The recent chapters added:

```text
CAUSAL ROUTING
≠
CAUSAL AMPLIFICATION

CAUSAL RETENTION
≠
CAUSAL INDIVIDUATION
```

These are not failures in the ordinary sense.

They are discoveries about where our concepts split.

A useful experimental system does not merely tell us whether a phenomenon exists.

It tells us which concepts we had incorrectly bundled together.

---

# Invalid is not negative

This deserves its own rule.

Suppose an experiment contains a broken intervention.

The result is invalid.

It does not matter whether the measured effect is:

```text
positive
negative
zero
large
small
significant
nonsignificant
```

The intended estimand was not correctly implemented.

Therefore the experiment cannot serve as evidence for or against that intended claim.

This seems obvious when stated abstractly.

In practice, it is easy to violate.

Especially when the invalid result is convenient.

If a broken experiment produces zero, people are tempted to say:

> we found no effect.

If it produces a large effect, they are tempted to salvage it.

Both are mistakes.

The correct status is:

```text
INVALID
```

and then the question becomes:

> which parts, if any, were not touched by the defect?

That is exactly what happened in Chapter 27.

---

# Unresolved is not failed

Now consider a valid experiment.

Suppose the interval crosses zero.

That alone does not tell us the result is negative.

The experiment may simply lack precision.

The correct question is:

> What effect sizes are still compatible with the data?

If scientifically meaningful positive and negative effects both remain plausible, the result is:

```text
UNRESOLVED
```

Not:

```text
FAILED
```

Chapter 27's magnitude question is a good example.

The direction was supported.

But the MDE remained too wide for the frozen ±0.15 magnitude claim.

So the magnitude remained unresolved.

The fact that another inferential layer was supported did not make the unresolved layer disappear.

---

# A bounded negative is a real result

The reverse mistake is equally common.

A result with an interval near zero is sometimes summarized as:

> nothing happened.

That discards information.

If the experiment is precise enough to exclude effects larger than a predeclared meaningful threshold, then the negative result is substantive.

Chapter 26 V2 did this for amplification.

Chapter 28 V2 did it for excess modularity.

In both cases, the claim was not merely unsupported.

A meaningful positive effect was bounded away.

That is stronger.

The correct language is:

```text
BOUNDED BELOW SEI
```

or:

```text
BOUNDED NEAR ZERO
```

depending on the estimand.

The threshold matters because zero is rarely the only scientifically interesting boundary.

---

# Preserve the surviving phenomenon

Perhaps the most important rule emerged from Chapters 27 and 28.

When a higher-level interpretation fails, do not automatically delete the lower-level observation.

Chapter 27 V1's broken downstream intervention did not erase the valid immediate material-state effect.

Chapter 28 V2's matched null did not erase raw spatial causal containment.

This gives us a hierarchy:

```text
measurement
↓
mechanism
↓
construct
↓
interpretation
```

A failure higher in that hierarchy need not propagate all the way down.

If the measurement remains valid, keep it.

If the mechanism remains supported, keep it.

Fail only the layer the evidence actually defeats.

That leads to the central rule of the chapter.

---

# Fail the smallest claim

The final Chapter 29 principle is:

> **Fail the smallest claim justified by the evidence. Preserve everything that still survives.**

This prevents two opposite errors.

The first is over-rescue:

```text
the main claim weakened
→ reinterpret until something sounds successful
```

The second is over-destruction:

```text
the main claim weakened
→ throw away the entire experiment
```

Both distort the evidence.

The correct response is surgical.

If the implementation is invalid, invalidate the affected estimand.

If precision is insufficient, leave the claim unresolved.

If the confidence interval and MDE bound the effect below the SEI, record a bounded negative.

If a stronger control removes a higher-level interpretation, preserve the lower-level phenomenon that still survives.

If a descriptive audit explains the mechanism, label it descriptive.

Do not use it as retroactive rescue.

---

# Why this matters for Digital Life

The project began with a risk.

We were deliberately searching for properties associated with life.

That makes us vulnerable to seeing them everywhere.

Growth looks like reproduction.

Refill looks like repair.

Persistence looks like memory.

Coherent motion looks like flocking.

Causal containment looks like individuality.

The danger is not merely false positives.

The deeper danger is conceptual compression.

We see one measurable phenomenon and immediately promote it into a richer biological category.

The failure ledger is a defense against that.

It forces every promotion to survive:

```text
construct definition
implementation
measurement
control
precision
alternative explanation
```

And when a promotion fails, it tells us what remains underneath.

That is why the negative results have become some of the most useful results in the book.

They tell us where one concept stops and another begins.

---

# What the audit does not prove

The Chapter 29 audit passed.

But its scope is deliberately bounded.

It does not establish that:

```text
the project never made mistakes
```

It does not establish that:

```text
the taxonomy is universally complete
```

It does not establish that:

```text
every future experiment will classify cleanly
```

And it does not establish a general philosophy of science.

It establishes something narrower:

> **Across the registered Chapter 26–28 experiment chains, invalid implementations, unresolved questions, precision-bounded negative results, descriptive closeouts and stronger-control claim narrowings can be represented without erasing surviving evidence or converting one evidence class into another.**

That is enough.

Because Chapter 30 now has a foundation.

We can finally ask what survived the entire investigation.

Not what looked alive.

Not what we hoped would be alive.

Not what received a biological name.

What survived.

After every invalidation.

Every null.

Every stronger control.

Every distinction.

Every failed interpretation.

What remains?

That is the question for the final chapter.
