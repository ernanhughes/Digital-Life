+++
title = "14: How to Fail Correctly"
date = "2026-08-15T03:00:00+01:00"
draft = false
description = "Thirteen chapters of biological names failed under stronger controls, and something smaller survived each time. This chapter makes explicit the bookkeeping that kept the survivors intact."
weight = 14
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Experimental Method", "Epistemology"]
series = ["Digital Life From First Principles"]
+++

The most dangerous result in this book was not a noisy one. It was one of the cleanest.

```text
measurement        ✓   M = 0.4402, CI [0.419, 0.461]
precision          ✓   MDE 0.0268 against a 0.15 threshold
implementation     ✓   corrected intervention, known global channels removed
predeclaration     ✓   regions selected blind to outcome, threshold frozen
replication        ✓   0.4436 on the second run
interpretation     ✕
```

Every box that methodological hygiene knows how to check was checked. And the conclusion — that we had found a causal individual — was wrong, because arbitrary disks of the same size did the same thing.

That is worth sitting with, because it means the usual defences are not sufficient. Predeclaration stops us moving the goalposts; it cannot tell us we picked the right goal. Precision tells us exactly what we measured; it cannot tell us whether we measured the right thing.

So before the final chapter asks what survived this investigation, this one has to establish why the surviving list can be trusted. That requires answering a question the book has been answering implicitly for thirteen chapters:

> **When a claim fails, what exactly has failed?**

---

## Failure Is Not One Thing

The word compresses several situations that license completely different conclusions.

An experiment might not have implemented the contrast it claimed. It might have been valid but too imprecise to answer its own question. It might have been valid, precise, and able to rule out an effect large enough to matter. Or the measurement might be perfectly sound while the interpretation built on top of it collapses under a better control.

The book has now produced examples of all four, which is how the working vocabulary developed:

```text
INVALID              we did not run the experiment we described
UNRESOLVED           the experiment could not answer its question
BOUNDED NEGATIVE     a meaningful effect was precisely excluded
SUPPORTED            the claim survived
SUPPORTED BUT NARROWED   a lower level survived; a higher one did not
DESCRIPTIVE ONLY     an explanation, not a confirmation
```

And one governing rule that separates them from the loose word they replace:

> **Failure of a claim ≠ failure of an experiment ≠ absence of a phenomenon.**

Rather than presenting this as a taxonomy to memorize, it is easier to reach the same distinctions by asking four questions in order. Each has a different failure mode, and each fails a different thing.

---

## Did We Run the Experiment We Claimed?

Chapter 12 intended a clean contrast: FORCE occupies the probe cell for one causal exposure, PREVENT keeps it empty for that same exposure. What the implementation did was insert the cell in FORCE and merely *start* it empty in PREVENT — leaving it free to attach naturally during the first update.

Worse, the contamination correlated with the treatment. The accessible material trace included the probe's only occupied neighbour, so it raised the probability that the supposedly prevented cell would appear: 0.428 in the accessible condition against 0.377 and 0.378 in the others.

The downstream result was therefore **INVALID**, and the crucial point is that this verdict is independent of what the numbers said. If a broken intervention returns a large effect, it is tempting to salvage it. If it returns nothing, it is tempting to report no effect. Both are the same error. The intended estimand was never implemented, so the run is evidence neither for nor against the claim.

```text
INVALID  ≠  NEGATIVE
```

The productive question after an invalidation is not *what did we find* but *which parts were untouched by the defect*. In Chapter 12 the immediate expected causal response had been computed before the broken growth step, so it could not depend on what happened afterwards — and it survived, was replicated by the corrected run, and turned out to carry the chapter's mechanism.

---

## Could the Experiment Answer Its Question?

Chapter 10's first attempt at predicting causal gain from local geometry returned:

```text
+0.167     CI [−0.078, +0.431]     declared meaningful effect +0.15
```

Reporting that as evidence against the hypothesis would have been a straightforward misrepresentation. The interval comfortably contains effects twice the size of the one declared meaningful, and also contains effects in the opposite direction. The experiment did not answer its question; it lacked the precision to.

```text
UNRESOLVED  ≠  FAILED
```

The test is not whether the interval contains zero. It is *what effect sizes remain compatible with the data*. If effects large enough to matter are still on the table in either direction, nothing has been resolved, and the honest report says so.

The same distinction appeared in a more interesting form in Chapter 12, where two questions about the same number got different answers. Was the downstream effect negative? Both estimators excluded zero: supported. Did it reach the predeclared ±0.15 magnitude? The achieved MDE was around 0.357: unresolved. Those statements are compatible, and collapsing them in either direction — "the hypothesis passed" or "inconclusive" — would have thrown away real information.

```text
DIRECTION  ≠  MAGNITUDE
```

---

## Did We Exclude Something Worth Excluding?

The reverse error is just as common: reporting an interval near zero as *nothing happened*.

Chapter 11 compared strong candidate subsampling against exhaustive evaluation at dynamically matched background construction, and found a mean twelve-step difference of `+0.00130` with the whole interval inside the predeclared ±0.15 band. Chapter 13 compared selected regions against geometry-matched controls and found excess modularity of `−0.0123`, upper bound `+0.0072`, against a declared meaningful margin of `+0.10`.

Neither is an absence of evidence. Both are evidence of absence *at a stated scale* — which is a far stronger and more useful claim, and one that requires two things a bare non-significant result does not have: a threshold declared in advance, and enough precision to have detected it.

The distinction is old and still routinely ignored elsewhere. Clinical trials that fail to reach significance are habitually described as negative, when the honest reading is often that they were too small to detect a difference that would have mattered.[^altman] The remedy is the same one this book has been using: state what would count as meaningful before the data arrive, and report whether the experiment could have seen it.

[^altman]: D. G. Altman and J. M. Bland, "Absence of evidence is not evidence of absence", *BMJ* 311 (1995), 485.

```text
BOUNDED NEGATIVE  ≠  NOTHING HAPPENED
```

And a bounded negative earns its status only with both parts. Chapter 13's excess modularity was bounded because the achieved MDE was `0.0265` against a `+0.10` threshold — roughly four times the precision needed. Without that, the same point estimate would have been unresolved, not negative.

---

## Does the Measurement Identify the Construct?

Now the failure that none of the above would catch, and the reason this chapter exists.

Chapter 13's measurement was valid. Its mechanism was real: perturbations inside a region really did express most of their causal mass inside it, while external perturbations penetrated much less. What failed was the step from that mechanism to the concept it was taken to demonstrate.

The layers can be separated:

```text
MEASUREMENT       raw modularity M ≈ 0.44                        ✓
MECHANISM         local spatial causal containment               ✓
CONSTRUCT         a privileged causal region                     ✕
INTERPRETATION    an individual                          not established
```

A failure at one layer does not propagate downward. The containment survives; only the promotion dies. And Chapter 3 has exactly the same shape at the other end of the book:

```text
MEASUREMENT       nearby velocity coherence                      ✓
MECHANISM         short-range spatial coherence                  ✓
CONSTRUCT         ancestry-specific flocking                     ✕
```

This is what methodologists call a construct-validity problem: an instrument can measure something real, consistently and precisely, while the thing it measures is not the thing the theory named. The classic treatment makes the point that a construct is validated not by any single correlation but by the network of predictions it makes and the alternatives it excludes.[^cronbach] Statistical rigour applied to the wrong estimand produces a very confident wrong answer.

[^cronbach]: L. J. Cronbach and P. E. Meehl, "Construct validity in psychological tests", *Psychological Bulletin* 52(4) (1955), 281–302.

Which yields the rule this book most needed and did not have written down until now:

> **Do not promote a measurement into a richer construct until a simpler mechanism capable of producing the same measurement has been controlled.**

The recurring shape is unmistakable once listed:

```text
coherent motion       → flocking
refilled vacancies    → repair
persistent trace      → memory
retained influence    → individual
```

In every case the measurement was real and the promotion was premature. And in every case, what exposed the error was not a better statistic but a control that asked what else could produce the same number.

---

## The Null Is Part of the Claim

Chapter 13 makes a point sharper than any of the earlier cases.

Before the geometry-matched control, the operative claim was effectively `M > 0.15 → individual`. After it, the claim became `M_selected − M_matched > 0.10`. Those are not the same hypothesis with different rigour. They are different hypotheses, and only the second is about the crystal rather than about disks.

So the null is not a formality applied after the result to check it. It is part of what the statistic *means*. A modularity score with no null attached is not a weak measurement of individuality; it is not a measurement of individuality at all.

> **A measurement without its alternative explanation is not yet a construct.**

This reframes several earlier failures. Chapter 9's predictive-coherence result looked enormous at 0.2906 until a family-level permutation null produced maxima averaging 0.2569 — the statistic was measuring what any large chunk of a structured field does. Chapter 6's placement advantage looked decisive until the copy budget was equalized and most of it turned out to be quantity. Chapter 7's interior-loss advantage evaporated once the shared reoccupation effect was measured. Each time, the number stayed the same and its meaning changed, because the comparison changed.

---

## Fail the Smallest Claim

All of this collapses into one operating principle:

> **Fail the smallest claim the evidence actually defeats. Preserve everything that still survives.**

It rules out two opposite pathologies. **Over-rescue** takes a weakened claim and reinterprets the wreckage until the project still sounds successful. **Over-destruction** takes the same weakened claim and throws away the entire experiment, including results the evidence never touched. Both distort the record; the second is more respectable and equally wasteful.

The correct response is surgical, and mechanical enough to write down:

```text
implementation invalid          → invalidate the affected estimand only
precision insufficient          → leave the claim unresolved
meaningful effect excluded      → record a bounded negative
stronger control explains it    → narrow the construct
lower-level phenomenon intact   → keep it
follow-up analysis explanatory  → label it descriptive
```

Applied to Chapter 13, that means the individual disappears and the containment stays. Applied to Chapter 12, the invalid downstream result disappears and the immediate sensitivity effect stays. Applied to Chapter 3, ancestry-specific flocking disappears and short-range motion coherence stays.

---

## A Description Is Not a Confirmation

One category deserves separate attention because it is the most tempting.

Chapter 12's confirmatory magnitude claim stayed unresolved. Then a follow-up analysis of the same data showed something genuinely striking: about 75% of the cumulative causal difference accrued after the material trace had fallen below half its starting mass, and 36% after it fell below a quarter. That is the most interesting result in the chapter, and it is the reason the chapter has a mechanism at all.

It is also **descriptive**. It was not the frozen primary endpoint, it was found by looking at trajectories after the fact, and it cannot promote the unresolved magnitude claim into a supported one. An explanation can illuminate a result without rescuing it.

The rule holds in the other direction too. The descriptive status is not a demotion — the trajectory finding is allowed to be the chapter's headline idea. It is simply not allowed to change what the confirmatory test concluded.

---

## Corrections Are Not Rescues

If invalid experiments must be re-run, then re-running experiments cannot always be cheating. The distinction matters, and it is not subtle.

Chapter 12's second run repaired the PREVENT semantics, matched the remote carriers on background frontier influence, and replaced a noisy estimator with a lower-variance one — while freezing every scientific parameter: the material gain, the half-life, the history age, the horizon, the effect threshold. Chapter 11's corrected design fixed a calibration that controlled only the first frame of a twelve-lag process. Both repaired the instrument and left the question alone.

Compare the alternative. Adjusting the material gain, or the half-life, or the horizon, or the meaningful-effect threshold, until an effect appeared, would have been a different activity with the same outward appearance.

```text
CORRECTIVE EXPERIMENT   fixes validity; the question is unchanged
NEW EXPERIMENT          asks a different question, declared as such
RESCUE EXPERIMENT       changes the question without saying so
```

The first two are science. The third is the one that leaves no trace in the write-up, which is exactly why the parameters have to be frozen in advance and the corrections listed explicitly.

---

## Knowing When to Stop

The instinct after a weakened claim is to try one more variant. Another radius. Another feature. Another budget. Another history window. Another decoder. There is always one more, and the search has no natural end.

The book has stopped four times, each in a different way. Chapter 6 abandoned an entire line after three consecutive broad claims failed, rather than keeping whichever secondary metric survived in each. Chapter 9 refused to tune the radius after the family null failed, and changed the evidence type instead. Chapter 10 stopped adding local features and rebuilt the measurement. Chapter 13 changed the null rather than the disk.

The stop rule that emerges:

> **When the declared question has been answered, stop. Do not convert disappointment into a parameter search unless you are willing to declare a genuinely new experiment.**

And its companion, from Chapter 8, where a budget missed its frozen stationarity threshold by about `0.00002`:

> **A threshold that moves when the answer is inconvenient is not a threshold.**

That one is worth stating plainly because it feels petty in the moment. Two parts in a hundred thousand is nothing. But the alternative is a rule that binds only when it costs nothing, which is not a rule.

---

## Auditing the Bookkeeping

Rules stated in a chapter are cheap. The question is whether the project's actual evidence history obeys them.

So the recent experimental chains were encoded as a ledger. Each entry recorded the claim under test, whether the run was valid, its inferential status, the transition that occurred, the threshold where one existed, the achieved precision, and — the field that matters most — what evidence survived. Ten cases were registered across the three most recent chapters, all backed by source artifacts rather than recollection.

The audit then checked for the forbidden moves:

```text
did an INVALID run ever become evidence against a hypothesis?
did UNRESOLVED ever quietly become FAILED?
did any bounded negative lack a declared threshold or adequate precision?
did a stronger control erase valid lower-level evidence?
did a descriptive closeout upgrade a confirmatory claim?
did any estimand change after the result was seen?
```

Ten of ten cases passed, along with five predeclared cross-case checks — that the invalid intervention preserved the independently valid immediate effect; that direction and magnitude were kept separate; that the geometry-matched null narrowed the construct without erasing raw containment; that the bounded amplification result preserved the mechanistic rerouting finding; and that the trajectory closeout did not rescue the unresolved magnitude.

```text
FAILURE LEDGER CONSISTENT
```

That status needs reading narrowly, because it is easy to inflate. It does not establish that the project made no mistakes — it exists precisely because the project made several. It does not establish that the taxonomy is complete, that future results will classify cleanly, or that any conclusion in this book is true.

It establishes one thing:

> **The evidence history can be represented without converting one evidence class into another or deleting results that survived.**

That is a modest claim. It is also the only claim that makes the final chapter possible, because a list of survivors is worthless if the criteria for surviving moved.

---

## What All Those Failures Discovered

Here is the part that makes this chapter something other than an apology.

The failures were productive, and not in the consoling sense. Each one located a boundary between concepts that had been treated as synonyms:

```text
similarity            ≠  causal ancestry
state                 ≠  history
causal past           ≠  memory
persistent            ≠  accessible
accessible            ≠  differentially used
net change            ≠  gross process
reoccupation          ≠  repair
stable size           ≠  stable process
locality              ≠  privileged boundary
causal effect         ≠  stable local property
causal routing        ≠  causal amplification
past-dependent        ≠  past-readable
containment           ≠  individuation
```

None of these were available at the start. Every one required a promotion to fail against a control that was better than the one that came before.

> **A failed promotion is a successful distinction.**

Which suggests a way of reading the whole investigation. We kept asking the substrate biological questions, and it kept answering a different question — accurately, and in its own vocabulary.

```text
we asked                the crystal answered

flocking?               short-range motion coherence
memory?                 history-dependent causal sensitivity
repair?                 rapid reoccupation of vacated sites
a stable body size?     computation-dependent turnover
an individual?          spatial causal containment
```

None of those answers is disappointing. They are simply not the words we brought with us. The method's entire job has been to hear the answer the system actually gave rather than the one the question was shaped to receive — and the reason it took this much apparatus is that the temptation was never abstract. A trace that persists really does beg to be called memory. A hole that fills really does look like healing. A number like 0.44 really did look like an individual.

---

## What Survived

The book has now stripped away almost every biological name it started with. Flocking, readable memory, repair, a stable organism-like size, a privileged body boundary, causal amplification, individuality — each was tested, and each failed against a stronger control or a matched null.

What is left is not nothing. It is a list of phenomena that survived implementation audits, matched nulls, precision gates and failed interpretations:

```text
causal reproduction without a reproduction operator
short-range motion coherence
exact continuation from saved state; exact reconstruction from history
causal consequence without a readable record
persistent material state, causally active while it stays accessible
loss-generated construction interfaces and rapid reoccupation
gross turnover concealed beneath stable net population
process scale set by finite computational opportunity
selector-mediated coupling between distant regions
history-dependent causal sensitivity and trajectory redirection
strong spatial causal containment
```

Those are not fragments of failed hypotheses. They are what the evidence still supports after everything the investigation could throw at it, and they arrived in the substrate's vocabulary rather than biology's.

So the final question cannot be the one the book started with. *Which features of life can we reproduce?* was always going to produce a list of names that dissolve under controls — we have just watched thirteen chapters of it.

The question that the surviving evidence actually poses is different, and harder:

> **What do these computational phenomena add up to?**
