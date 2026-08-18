+++
title = "17: How to Fail Correctly"
date = "2026-08-15T03:00:00+01:00"
draft = false
description = "The strongest controls in this investigation repeatedly destroyed richer interpretations while leaving smaller phenomena intact. This chapter makes explicit the bookkeeping required to fail one claim without erasing what the evidence still supports."
weight = 17
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Experimental Method", "Epistemology"]
series = ["Digital Life From First Principles"]
+++

The most dangerous result in this book was not a noisy one.

It was one of the cleanest.

```text
measurement            ✓    M = 0.4402
                            CI [0.419, 0.461]

precision              ✓    MDE80 = 0.0268
                            against a +0.15 threshold

implementation         ✓    corrected transient intervention
                            known global channels removed

predeclaration         ✓    regions selected blind to outcome
                            threshold frozen

fresh reproduction     ✓    selected regions scored 0.4436
                            in an independent matched-null run

individuation          ✕    not established
````

The two numbers come from different runs.

V1 measured raw causal containment on seed `20260916`.

V2 regenerated the selected regions on fresh seed `20260917`, reproduced the
raw score at `0.4436`, and then asked the stronger question: did those regions
exceed same-checkpoint matched controls?

Many of the safeguards we had learned to trust were satisfied.

The number was large.

The interval was narrow.

The intervention was correct.

The region selection was outcome-blind.

The raw phenomenon appeared again on a fresh seed.

And the inference from strong causal containment to causal individuality still did not survive the geometry-matched control.

The measurement was right.

What we thought it meant was not.

That is worth sitting with because it exposes the limits of procedural rigour.

Predeclaration can stop us moving a threshold after seeing the answer. It cannot guarantee that we chose the right threshold, the right estimand, or the right null.

Precision can tell us how tightly we measured a quantity. It cannot tell us whether that quantity identifies the construct we care about.

A corrected implementation can make an experiment internally valid. It cannot guarantee that the valid experiment asks the scientifically important question.

So before the final chapter asks what survived this investigation, this one has to make explicit the bookkeeping that determined what was allowed to survive.

The book has been doing that bookkeeping implicitly for most of its experimental life.

Now it needs to be stated.

> **When a claim fails, what exactly has failed?**

---

## Failure Is Not One Thing

The word *failure* compresses several situations that license completely different conclusions.

An experiment may never have implemented the contrast it claimed to test.

A valid experiment may have been too imprecise to answer its own question.

A valid and sufficiently precise experiment may exclude an effect large enough to matter.

A lower-level phenomenon may be measured cleanly while the richer interpretation attached to it collapses under a stronger control.

A follow-up analysis may explain something interesting without being allowed to alter the status of the confirmatory test.

These are not different degrees of the same outcome.

They live at different logical levels.

```text
RUN VALIDITY

INVALID
the run cannot support the intended estimand because
its intervention, implementation, operationalization or reference contrast
is defective

INFERENTIAL STATUS

UNRESOLVED
the declared question remains open at the required precision

SUPPORTED
the tested claim survived

BOUNDED
a predeclared effect region was excluded with adequate precision

EVIDENCE ROLE

DESCRIPTIVE ONLY
informative follow-up that does not alter confirmatory status

CLAIM TRANSITION

NARROWED
a lower-level result survived while a richer interpretation did not
```

Even `BOUNDED` is not one thing.

Two cases in this book used different forms of it:

```text
BOUNDED NEAR ZERO

a declared two-sided meaningful band is resolved around zero

BOUNDED BELOW SEI

a declared positive effect of meaningful size is excluded
```

Those are not interchangeable.

Nor is `INVALID` merely another inferential status. An invalid experiment does not produce a weak answer to the original question. It fails to instantiate the question correctly.

And `NARROWED` is not a statistical verdict at all. It describes what happens when a stronger control leaves a smaller claim intact while removing permission for a larger one.

The reason for keeping these categories separate is simple:

> **A failed claim, an invalid experiment and an absent phenomenon are three different things.**

The easiest way to use the distinctions is not to memorize a taxonomy.

It is to ask a sequence of questions.

---

## Did We Run the Experiment We Claimed?

The *Can the Past Redirect the Future?* chapter intended a clean contrast.

```text
FORCE
x is present for one controlled causal exposure

PREVENT
x is prevented from appearing during that same exposure
```

The first implementation did not do that.

FORCE inserted `x`.

PREVENT merely *started* with `x` empty.

The supposedly prevented cell remained eligible to attach naturally during the first update.

Worse, the probability of that contamination depended on the treatment arm.

```text
natural PREVENT attachment of x

ACCESSIBLE    0.428
REMOTE        0.377
ERASED        0.378
```

The hidden material state altered the probability that the supposedly prevented event would occur.

So the intended causal contrast had not been implemented.

The downstream result was therefore:

```text
INVALID
```

The crucial point is that this verdict is logically prior to the numerical outcome.

If a broken intervention returns a large effect, it is tempting to salvage it.

If it returns nothing, it is tempting to report a negative result.

Both are the same error.

The affected estimand was never correctly instantiated.

```text
INVALID
≠
NEGATIVE
≠
UNRESOLVED
```

An invalid result is evidence neither for nor against the claim it failed to test.

That sounds obvious when written down.

It is much harder when the invalid run contains a result you want.

The productive question after invalidation is therefore not:

> *Can we keep the conclusion?*

It is:

> **Which quantities were causally upstream of the defect?**

In that experiment, the immediate expected causal response had been computed before the contaminated growth step.

Its value could not depend on whether PREVENT later allowed `x` to attach.

That immediate quantity therefore survived the invalidation.

It was audited separately.

Its negative sign was reproduced after the intervention was repaired.

And it supplied the operating-point mechanism that made the otherwise surprising sign intelligible.

The downstream result disappeared.

The independent immediate result stayed.

That is what failing correctly looks like.

---

## Could the Experiment Answer Its Question?

A valid experiment can still fail to resolve the question it was built to answer.

Earlier, while trying to predict downstream causal consequence from local geometry, one estimate came back approximately:

```text
+0.167

95% CI
[-0.078, +0.431]

declared meaningful scale
0.15
```

Reporting that as evidence against the hypothesis would have been a straightforward misrepresentation.

The interval contains zero.

But that is not the important fact.

It also contains substantial positive effects well beyond the declared meaningful scale.

The experiment could not distinguish:

```text
meaningful positive effect

from

small effect

from

zero

from

effect in the opposite direction
```

The correct status was:

```text
UNRESOLVED
```

not:

```text
FAILED
```

The test is not simply whether an interval contains zero.

The more useful question is:

> **What scientifically meaningful effects remain compatible with the data?**

If effects at or beyond the predeclared scale of interest remain compatible with the observations—and the achieved precision cannot resolve that scale—then the magnitude question remains open.

Whether the interval excludes zero can answer the directional question.

Whether it excludes the predeclared effect threshold answers a different,
magnitude question.

The distinction became especially clear in *Can the Past Redirect the Future?*

The corrected experiment produced:

```text
ACCESSIBLE − REMOTE

mean       −0.397
95% CI     [−0.679, −0.119]
```

The entire interval lay below zero.

So one question had an answer:

```text
IS THE EFFECT NEGATIVE?

SUPPORTED
```

But the frozen smallest effect of interest was `±0.15`, and the achieved one-sided MDE80 was about `0.357`.

The interval also extended to `−0.119`, a magnitude smaller than the declared `0.15` threshold.

So another question remained open:

```text
CAN WE ESTABLISH THE PREDECLARED
MINIMUM MAGNITUDE?

UNRESOLVED
```

Those statements are compatible.

```text
DIRECTION
≠
MAGNITUDE
```

Calling the whole result *supported* would have promoted a magnitude the experiment did not resolve.

Calling the whole result *inconclusive* would have thrown away a direction the experiment did establish.

Failure bookkeeping is partly the discipline of refusing both simplifications.

---

## Did We Exclude Something Worth Excluding?

The reverse mistake is just as common.

An estimate close to zero is reported as:

> *nothing happened.*

But a small point estimate means little by itself.

To make a useful negative statement, the experiment has to define what would count as meaningful and then demonstrate enough precision to exclude it.

Two recent experiments did this in different ways.

In *Can Finite Computation Couple Distant Events?*, strong candidate subsampling was compared with true exhaustive evaluation under dynamically matched background construction.

At twelve updates:

```text
mean difference      +0.00130
95% CI               [−0.08984, +0.08854]
frozen band          ±0.15
MDE80                 ≈ 0.115
```

The question there was two-sided.

Could the mean consequence differ from exhaustive evaluation by at least `0.15` in either direction?

The answer was no at the achieved precision.

```text
BOUNDED NEAR ZERO
AT THE DECLARED ±0.15 SCALE
```

The previous chapter asked a different question.

Selected regions were compared with geometry-matched controls:

```text
M_excess    −0.0123
95% CI      [−0.0327, +0.0072]
SEI         +0.10
MDE80       0.0265
```

The scientific claim was directional in a different sense.

Did the selected regions show **positive excess modularity** of at least `+0.10` beyond the matched null?

The upper confidence bound was only `+0.0072`, and the achieved precision was far tighter than the declared threshold.

So:

```text
MEANINGFUL POSITIVE EXCESS
BOUNDED BELOW SEI
```

But:

```text
DIRECTION AROUND ZERO
UNRESOLVED
```

because the interval still crossed zero.

Those two experiments therefore earned different negative claims:

```text
BOUNDED NEAR ZERO
≠
BOUNDED BELOW A POSITIVE THRESHOLD
≠
NOT SIGNIFICANT
```

Neither is merely an absence of evidence.

Each excludes a predeclared effect region at a stated scale.

That is much stronger than a bare failure to reject zero.

It also explains why precision belongs in the status.

The same point estimate could be:

```text
BOUNDED
```

under one standard error and:

```text
UNRESOLVED
```

under another.

A negative result is not the absence of a positive point estimate.

It is an inference about what effect sizes the experiment has actually ruled out.

[^altman]: D. G. Altman and J. M. Bland, "Absence of evidence is not evidence of absence", *BMJ* 311 (1995), 485.

---

## Does the Measurement Identify the Construct?

Now the failure that none of the previous checks can catch.

And the reason this chapter exists.

The previous chapter's **raw containment measurement** was valid.

The measured phenomenon was real.

At radius four:

```text
internal retention       ≈ 0.776
external penetration     ≈ 0.335

raw modularity M         ≈ 0.440
```

Perturbations initiated inside the selected regions really did express much more accumulated causal effect inside those regions than comparable external perturbations expressed inward.

The number was not an artifact of a broken intervention.

It was not underpowered.

It was not selected after looking at the outcome.

It appeared again on a fresh seed.

What failed was the promotion from that measured phenomenon to the richer construct.

The layers are easier to see when separated:

```text
MEASUREMENT

raw modularity
M ≈ 0.44
✓

PHENOMENON

strong spatial causal containment
✓

CONSTRUCT

system-privileged causal region
NOT ESTABLISHED

INTERPRETATION

individual
NOT ESTABLISHED
```

A failure at the upper layer does not propagate automatically downward.

The containment survives.

The privilege claim does not.

The early flocking result had the same logical shape:

```text
MEASUREMENT

nearby velocity coherence
✓

PHENOMENON

short-range spatial motion coherence
✓

CONSTRUCT

ancestry-specific flocking
NOT ESTABLISHED
```

This is a construct-validity problem.

An operational quantity can be measured accurately and reproducibly while failing to uniquely identify the richer theoretical construct attached to it.

The classic construct-validity literature makes the broader point that a construct is not validated by one successful association. It earns meaning through its relations to other observables and through the theoretical network of predictions surrounding it.[^cronbach]

Statistical rigour can make an estimate extremely precise.

It cannot, by itself, validate the promotion from that estimate to a richer concept.

[^cronbach]: L. J. Cronbach and P. E. Meehl, "Construct validity in psychological tests", *Psychological Bulletin* 52(4) (1955), 281–302.

The experimental version of that lesson, learned repeatedly here, is:

> **Do not promote a measurement into a richer construct until a simpler mechanism capable of producing the same measurement has been controlled.**

Consider the recurring pattern:

```text
coherent motion
→ flocking

refilled vacancies
→ repair

experimentally written persistent hidden state
→ memory

retained causal influence
→ individual
```

In every case something real was measured.

In every case the promotion was stronger than the evidence.

And what exposed the mismatch was not usually a better statistic.

It was a better alternative explanation.

---

## The Null Is Part of the Claim

The previous chapter makes this point sharper than any earlier example.

Before the geometry-matched control, the operative inference was effectively:

```text
large raw causal modularity
→
privileged region
```

The missing object in that inference was the null.

How large would the same statistic be in other regions with comparable spatial and interface geometry?

Once those controls were built:

```text
selected regions     M ≈ 0.444

matched controls     M ≈ 0.456

excess               ≈ −0.012
```

the raw measurement did not disappear.

Its interpretation changed.

A null is therefore not merely a ceremonial calculation applied after a result.

It is part of what the result is allowed to mean.

> **A measurement is not yet evidence for a richer construct until plausible alternative generators of that measurement have been controlled.**

That pattern was already visible elsewhere.

Predictive coherence weakened when ordinary structured regions were admitted
into the null.

Material placement weakened when copy quantity was equalized.

Ancestry-specific flocking weakened when distance was matched.

Different experiments, same bookkeeping:

```text
PHENOMENON SURVIVES

PROMOTION NARROWS
````

---

## Fail the Smallest Claim

All of this collapses into one operating principle:

> **Fail the smallest claim the evidence actually defeats. Preserve everything that still survives.**

It rules out two opposite pathologies.

The first is **over-rescue**.

A rich claim weakens, so the language keeps changing until whatever remains is presented as though it were what we meant all along.

That destroys the distinction between prediction and retrospective interpretation.

The second is **over-destruction**.

A rich claim fails, so everything associated with it is thrown away—including measurements and mechanisms the stronger control never defeated.

That feels stricter.

It is not more scientific.

It is simply wasteful.

The response should be surgical:

```text
implementation invalid
→
invalidate the affected estimand only

precision insufficient
→
leave the declared question unresolved

meaningful effect region excluded
→
record the appropriate bounded result

stronger control defeats richer interpretation
→
narrow the claim

lower-level phenomenon remains valid
→
keep it

follow-up analysis explains or contextualizes
→
label it descriptive
```

Applied to the previous chapter:

```text
individual
disappears

causal containment
stays
```

Applied to *Can the Past Redirect the Future?*:

```text
invalid V1 downstream inference
disappears

valid immediate hidden-state sensitivity
stays
```

Applied to the flocking experiment:

```text
ancestry-specific flocking
disappears

short-range motion coherence
stays
```

This is not rhetorical moderation.

It is evidence accounting.

---

## A Description Is Not a Confirmation

One category deserves separate attention because it is the most tempting.

The corrected hidden-state experiment ended with:

```text
negative direction
SUPPORTED

predeclared minimum magnitude
UNRESOLVED
```

Then we inspected how the effect accumulated through time.

The closeout was striking.

Roughly 75% of the final cumulative difference accrued after the written material trace had fallen below half its starting mass.

About 36% accrued after it had fallen below a quarter.

That temporal pattern motivates a plausible interpretation:

early hidden-state modulation changes events;

those events alter later states;

later divergence may therefore depend partly on trajectory as well as on whatever material remains.

That is interesting.

It is also:

```text
DESCRIPTIVE
```

The closeout was not the frozen confirmatory endpoint.

It did not isolate a mediation pathway.

Its pooled group-by-lag diagnostics were not independent confirmatory observations.

And it cannot upgrade the unresolved minimum-magnitude claim into a supported one.

An explanation can illuminate a result without rescuing it.

Calling an analysis descriptive is therefore not a dismissal.

It records how the evidence was obtained and what inferential work it is allowed to do.

```text
DESCRIPTIVE
≠
UNIMPORTANT

DESCRIPTIVE
≠
CONFIRMATORY
```

Both distinctions matter.

---

## Corrections Are Not Rescues

If invalid experiments must be repaired and rerun, then rerunning an experiment cannot automatically be cheating.

The distinction is in what changes.

The corrected hidden-state experiment repaired the PREVENT semantics.

It repaired the contaminated REMOTE comparator.

It froze a lag-wise expected local causal-difference estimator before the corrected run.

And it kept the scientific parameters fixed:

```text
material gain
half-life
history age
horizon
effect threshold
```

The scientific question remained recognizable.

The instrument changed because the original instrument had not implemented that question correctly.

The computational-coupling experiment had a similar correction.

A calibration scheme that controlled only the beginning of a multi-lag process was replaced by one that controlled the trajectory dynamically.

Again, the repair targeted the instrument.

It did not tune the scientific parameters until the desired effect appeared.

The distinctions are:

```text
CORRECTIVE EXPERIMENT

repairs a defect in implementation, construct or reference
while preserving the declared scientific question

NEW EXPERIMENT

asks a materially different question
and declares that change before interpreting its result

RESCUE

changes the estimand, threshold, parameter regime or interpretation
because the original answer was inconvenient,
while presenting the new result as though it answered the old question
```

The first two are legitimate scientific moves.

The third is dangerous because it lets a question mutate invisibly.

---

## Knowing When to Stop

After a weakened claim, there is always another variant available.

Another radius.

Another feature.

Another budget.

Another history window.

Another matching rule.

Another decoder.

Another horizon.

The search space has no natural end.

That makes stopping a scientific act.

Several chapters reached points where continuing the same search would have turned disappointment into parameter hunting.

The material-placement experiments abandoned a broad line after repeated controls collapsed its richer interpretations rather than continuing until one secondary metric looked favourable.

The boundary experiments did not retune the radius after the geometric null weakened the claim.

The causal-gain work stopped adding local predictors when the local prediction programme stopped earning information and changed the measurement instead.

The previous chapter changed the null rather than changing the modularity statistic until the selected regions won.

The stop rule that emerges is:

> **When the declared question has been answered, stop. Do not convert disappointment into a parameter search unless you are willing to declare a genuinely new experiment.**

The companion rule came from an earlier stationarity threshold that missed by roughly:

```text
0.00002
```

Scientifically tiny.

Procedurally decisive.

> **A threshold that moves when the answer is inconvenient is not a threshold.**

That can feel absurdly rigid when the miss is microscopic.

But a frozen boundary is useful precisely because it prevents us deciding, after seeing the number, whether this particular miss *really counts*.

The correct response is not to pretend `0.00002` matters biologically.

It is to report:

```text
near miss
```

and keep the rule intact.

---

## Auditing the Bookkeeping

Rules written in prose are cheap.

The question is whether the project actually followed them.

So the most recent experimental chains were encoded into an executable failure ledger.

This chapter does not introduce another Digital Crystal simulation.

Its experimental object is the evidence history itself.

Ten cases were registered across three recent experimental chains:

```text
finite-selector / amplification
hidden-state causal response
causal modularity / individuation

Every registered case resolved to source artifacts.

```text
registered cases             10

source-backed cases          10

manual-evidence-only          0

missing required sources      0
```

Each entry records:

```text
claim under test

run validity

inferential status

transition type

evidence role

threshold, where applicable

achieved precision, where applicable

what evidence survived
```

The audit then checks for the forbidden moves:

```text
did an INVALID run ever become evidence against a hypothesis?

did UNRESOLVED quietly become FAILED?

did a bounded result lack a declared threshold or adequate precision?

did a stronger control erase valid lower-level evidence?

did a descriptive closeout upgrade a confirmatory claim?

did a materially changed estimand masquerade as the original one?
```

All ten registered cases passed the bookkeeping rules.

```text
10 / 10
```

Five cross-case checks were declared as well.

They asked whether:

```text
1.
the invalid hidden-state primary preserved
the independently valid immediate result

2.
direction and minimum magnitude
remained separate

3.
the geometry-matched null narrowed
the individuation claim without erasing raw containment

4.
the bounded amplification result preserved
the mechanistic routing result

5.
the trajectory closeout remained descriptive
and did not rescue the unresolved magnitude claim
```

All five passed.

```text
FAILURE-LEDGER BOOKKEEPING
CONSISTENT
```

That status is narrow.

The ledger does not certify the truth of the conclusions, the completeness of
the taxonomy, the completeness of the underlying case record, or the absence
of mistakes.

It checks one thing: whether the registered evidence transitions were carried
forward without silently changing their logical status.

> **Across the registered Chapters 26–28 case chains, the recorded invalidations, unresolved questions, bounded results, descriptive closeouts and claim narrowings can be represented without silently converting one evidence class into another or deleting surviving evidence.**

That is enough.

A final chapter built from “what survived” is meaningless if the survival criteria changed every time a result became inconvenient.

The ledger does not certify the conclusions.

It certifies the bookkeeping used to carry them forward.

---

## What All Those Failures Discovered

Here is the part that makes this chapter something other than an apology.

The failures were productive.

Not in the consoling sense that every setback teaches us something.

They were productive because each one forced a distinction between concepts that had previously been allowed to blur together.

```text
similarity
≠
causal ancestry

visible state
≠
complete causal state

causal state difference
≠
readable record of a past

persistent
≠
locally accessible

accessible
≠
differentially used

net population change
≠
gross construction and loss

reoccupation
≠
repair

stable population size
≠
absence of turnover

locality
≠
privileged boundary

causal effect
≠
stable local predictor of downstream consequence

causal routing
≠
causal amplification

hidden-state conditioning
≠
record reading

causal containment
≠
causal individuation
```

Most of those distinctions were not part of the vocabulary we started with.

They became necessary when a richer interpretation encountered a control that left a smaller phenomenon intact.

> **A failed promotion is a successful distinction.**

That may be the most useful way to read the investigation.

We repeatedly asked questions in biological vocabulary.

The controls kept forcing the answers into narrower computational terms.

```text
we asked                 what survived

flocking?                short-range motion coherence

memory?                  hidden-state causal sensitivity

repair?                  rapid reoccupation after vacancy

stable body size?        compute-constrained scale
                         with substantial turnover

individual?              strong spatial causal containment
```

The right-hand column is not a list of consolation prizes.

Those are the measurements that remained after the stronger names stopped being defensible.

The method's job was never to preserve the biological vocabulary.

It was to discover when that vocabulary stopped earning its keep.

And the temptation was never abstract.

A trace that persists really does beg to be called memory.

A hole that fills really does look like healing.

A population that stays roughly stable really does resemble a maintained body.

A modularity score of `0.44` really did look like an individual.

The richer words were not foolish hypotheses.

They were hypotheses.

The mistake would have been refusing to give them up when the controls said otherwise.

---

## What Survived

Many of the stronger biological or organism-like promotions have now been removed, bounded, narrowed or left unestablished.

Among them:

```text
ancestry-specific flocking

readable memory

repair

stable organism-like body size

a privileged body boundary

causal amplification

causal individuality
```

Their scientific statuses are not identical.

Some failed specific controls.

Some were never established in the first place.

Some became unresolved at the declared magnitude.

Some were replaced by narrower descriptions.

What they share is only this:

none survived in the richer form initially suggested by the measurement.

What remains is not nothing.

It is a list of phenomena that survived implementation audits, matched nulls, precision gates and failed interpretations:

```text
causal reproduction without an explicit reproduction operator

short-range motion coherence

counterfactual continuation from complete saved state

hidden state that can modulate causal response
without evidence that the state is a readable record

persistent material state that remains causally active
while locally accessible

loss-generated construction interfaces
and rapid reoccupation

large gross turnover concealed beneath
much smaller net population change

process scale strongly constrained
by finite computational opportunity

selector-mediated coupling between distant regions

causal sensitivity to experimentally written hidden state,
with trajectory redirection remaining a descriptive interpretation

strong spatial causal containment
```

Those are not fragments left over after failed experiments.

They are the positive content of the investigation.

They survived because the controls did not remove them.

And they arrived increasingly in the substrate's vocabulary rather than biology's.

That changes the question.

*Which features of life can we reproduce?* turned out to be an increasingly poor organizing principle for this investigation.

Not because the biological questions were useless.

They were extraordinarily productive.

They gave us hypotheses sharp enough to fail.

But they repeatedly encouraged us to name the phenomenon before discovering what the substrate itself was doing.

The final chapter therefore has to begin from the survivors rather than from the names we hoped to recover.

Not:

```text
Which biological property comes next?
```

but:

> **What do these computational phenomena add up to?**
