+++
title = "13: We Found an Individual. Then We Didn't."
date = "2026-08-15T01:00:00+01:00"
draft = false
description = "A region of the Digital Crystal retains its own causal influence and resists influence from outside — strongly, precisely, reproducibly. Then arbitrary regions of the same size do exactly the same thing."
weight = 13
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Individuality", "Experimental Method"]
series = ["Digital Life From First Principles"]
+++

Chapter 9 asked whether the connected occupied crystal had a privileged boundary, and failed twice to find one. But the object it was testing was a shape: a centered disk, drawn on the material, tested afterwards for whether it behaved like a thing.

Since then the book has been doing what that failure recommended. Chapter 10 measured what one local event causes. Chapter 11 found that finite computation routes those consequences, coupling regions the local rule cannot connect. Chapter 12 showed that hidden past-dependent state changes the crystal's causal sensitivity, and that the resulting difference in trajectory outlives most of the trace that produced it.

So the candidate has changed. What we have now is not a blob of occupied cells. It is a causal process with a history, whose events are conditioned by state that does not appear in its shape.

That makes the individuation question worth asking again, and worth asking properly:

> **Is there a spatial region whose internal causal coupling exceeds its coupling to the surrounding crystal, in a way that geometry alone cannot explain?**

The last clause is the whole chapter.

---

## What Would a Causal Individual Do?

Set biology aside. Membranes and skins make individuality feel obvious in organisms, but a computational substrate owes us nothing of the kind, and importing a biological definition would prejudge the answer.

Operationally, one plausible signature of a causal module is asymmetric containment. Influence beginning inside should preferentially remain inside, while comparable influence beginning outside should penetrate less strongly.

That is not yet a definition of individuality. It is a candidate measurement of causal privilege.

Both are measurable. Perturb a frontier cell **inside** a region and measure what fraction of the resulting causal influence is expressed within the region:

$$
\text{internal retention} = \frac{A_{\text{inside}}}{A_{\text{inside}} + A_{\text{outside}}}
$$

Then perturb a comparable cell just **outside** the same region and measure what fraction of *that* influence lands inside:

$$
\text{external penetration} = \frac{A_{\text{inside}}}{A_{\text{inside}} + A_{\text{outside}}}
$$

and take the difference:

$$
M = \text{internal retention} - \text{external penetration}
$$

A large positive `M` says: perturbations initiated inside preferentially express their causal mass inside, while comparable perturbations initiated outside penetrate less strongly.

That is a plausible operational signature of causal containment.

Whether it identifies an individual is the question the rest of the chapter has to answer.

One estimator detail matters. `A` is summed **absolute** expected causal mass — the accumulated size of the probability shifts, not their signed total. Chapter 11 showed that a perturbation can raise some probabilities and lower others; if we summed signed values, a region full of large opposing causal shifts could cancel to nearly zero and appear causally empty. The question here is where the influence went, not what it netted out to.

---

## Remove the Channels We Already Know About

Two long-range mechanisms have already been discovered in this substrate, and both would contaminate a modularity measurement.

Chapter 11 established that a finite evaluation budget couples distant regions: a local frontier change alters which faraway candidates receive slots, producing effects outside the local causal cone. A region measured under a binding budget would appear less modular for reasons having nothing to do with its own organization.

Chapter 12 found a second channel by accident: a global construction-rate calibrator compensating for local changes applies its offset everywhere, coupling regions the physics keeps apart.

So this experiment removes both by design. **True unbounded evaluation** — every frontier candidate evaluated, no competition for slots. **No dynamic construction-rate calibration.** With both known global channels removed, causal influence under this protocol is limited by the local transition dynamics over the eight-step horizon.

That gives a structural check for free: beyond the corresponding causal reach, the expected effect must be exactly zero.
 It was, in every run — an assertion about the code rather than a finding, but a useful one.

The experiment therefore inherits something useful from earlier failures.

Chapter 11 identified one global coupling channel.

Chapter 12 exposed another.

Both can now be removed deliberately before testing causal containment.

---

## Draw the Regions Before Looking at the Answer

The most obvious way to fake this result would be to run the crystal, look for a patch that seems coherent, draw a boundary around it, and announce that the patch is an individual. That is not an experiment; it is a drawing exercise with statistics attached.

So the regions are fixed-radius hexagonal disks, with the primary radius frozen at `r = 4` and a descriptive sweep across `r ∈ {2,3,4,5}`. Candidates are centered on occupied cells and must satisfy support rules stated in advance: enough occupied cells, occupancy between 20% and 80%, at least two supported internal frontier probes and two supported external-shell probes, where a supported probe is a frontier cell with exactly one occupied neighbour.

The candidates are then ranked using only pre-outcome properties — occupancy fraction closest to 0.50, then radial position, then axial coordinates — and the first three are taken.

No region is selected because it scored well. Nothing about causal outcome enters the selection.

The perturbation is the corrected transient intervention from Chapters 10 and 12: FORCE explicitly occupies `x` at lag one, PREVENT explicitly blocks it, and after one full causal exposure `x` is removed from FORCE so that both branches continue without a permanent state difference. At each of eight lags, before any realized attachment, the expected probability shift is computed for every candidate and its absolute mass accumulated inside and outside the region.

---

## We Found One

At the frozen radius:

```text
M = 0.4402     95% CI [0.419, 0.461]
```

against a predeclared meaningful threshold of `0.15`, with an achieved MDE of `0.0268`.

```text
SUPPORTED
```

This is not marginal. It is nearly three times the declared threshold, with an interval an order of magnitude tighter than the effect. And the decomposition is more compelling still:

```text
internal retention     0.7755
external penetration   0.3353
```

Roughly 78% of the measured causal mass generated by internal perturbations remained inside the region.

For comparable external perturbations, about 34% of the measured causal mass penetrated inward.

The retention fraction was therefore more than twice the penetration fraction.

That is exactly the profile we had hoped a causally privileged region might show.

After twelve chapters in which a privileged boundary, a stable body and stronger organism-like interpretations had repeatedly failed to materialize, the number finally looked compelling.

For a while, this was the chapter where the book found an individual.

---

## Then the Circle Got Bigger

The scale sweep was a descriptive secondary, run for completeness rather than out of suspicion.

```text
radius 2     M ≈ 0.197
radius 3     M ≈ 0.374
radius 4     M ≈ 0.440
radius 5     M ≈ 0.504
```

The score climbs almost monotonically with radius. There is no peak or obvious characteristic scale in the tested range.

That does not prove that no natural scale exists, but it creates an immediate problem for the interpretation of `r = 4`: the supposedly special score increases further when the observer simply draws a larger disk.
 Instead the pattern is simpler and much less flattering:

```text
BIGGER DISK  →  BIGGER MODULE SCORE
```

Which is a warning that the measurement may be responding strongly to the geometry of the ruler itself.

---

## Geometry Can Manufacture a Module

The explanation requires no special structure in the crystal at all — only that influence spreads locally, which we already know it does.

A perturbation inside the disk generates a spatially local causal cone over the eight-step horizon.

As the enclosing disk becomes larger, more of that local influence can fall within the observer-defined region.

So internal retention can rise with radius even without any system-privileged boundary.

An external perturbation generates the same kind of local causal neighbourhood, but the imposed boundary cuts through that neighbourhood.

Only part of its causal mass therefore falls inside the disk.

The exact fraction depends on geometry, but the important point is that this asymmetry can arise from locality plus the observer's partition alone.

```text
INTERNAL PROBE            EXTERNAL PROBE
cone centred inside       cone straddling the boundary
↓                         ↓
retention grows with      penetration stays near
disk size                 the fraction that points inward
↓                         ↓
              M = retention − penetration grows
```

Even a spatially homogeneous local process with no privileged region can therefore produce substantial internal retention and lower external penetration when an observer draws a disk around the perturbation.
 The asymmetry is generated by where the boundary is placed relative to the perturbation, not by anything the system is doing.

The observer's circle can manufacture the appearance of a module.

---

## The Measurement Was Real

It would be a mistake to conclude that the first result was wrong. It was not.

At radius 4, perturbations initiated inside the selected regions genuinely did express far more causal mass inside those regions than external perturbations expressed into them. The number is accurate, the interval is tight, and it reproduces. Nothing about the scale sweep erases that measured containment.

What the sweep undermines is not the measurement but an equation we had made without noticing:

```text
raw causal containment  =  causal individuation
```

The measurement supports the left side. The chapter's claim was about the right side. A stronger control should narrow an interpretation, not retroactively delete a phenomenon — and the phenomenon here is real containment, which will still be true at the end of the chapter.

So the question is not whether to keep the result. It is what comparison would tell us what the result means.

---

## Change the Null, Not the Statistic

There are several tempting moves available at this point, and all of them are wrong.

We could sweep the radius more finely, looking for a scale where the score peaks. We could redefine the modularity statistic to normalize out disk size. We could add features to the region-selection rule until the selected regions score better than the rest. Every one of those adjusts the thing being measured until it produces the answer we wanted.

The actual missing piece is much simpler:

> **Would an arbitrary region with the same geometry produce the same score?**

If matched disks produce the same score, geometry is sufficient to explain the observed containment.

If the selected regions substantially exceed them, then we have evidence of causal privilege beyond geometry — a necessary step toward an individuation claim, though not yet a complete definition of individuality.

The interpretation of a modularity statistic depends critically on its null.

A large score tells us little about privileged organization if the same score is routinely generated by the spatial structure already present in the null.
 A similar problem appears in spatial network analysis: apparent community structure can largely reflect the fact that nearby nodes interact more often unless the null already contains that spatial dependence.[^expert]

The methodological parallel is the part that matters here: to interpret excess organization, the null must already reproduce the simpler geometry capable of generating the raw statistic.

[^expert]: P. Expert, T. S. Evans, V. D. Blondel and R. Lambiotte, "Uncovering space-independent communities in spatial networks", *PNAS* 108(19) (2011), 7663–7668.

That is a comparison, not a method we borrowed — we are not doing community detection and have no networks here. But the structure of the problem is identical, and it says exactly what our null has to contain: geometry.

---

## Regions From the Same Crystal

Everything about the measurement is held frozen: radius 4, eight-step horizon, the same transient intervention, the same absolute causal-mass estimator, unbounded evaluation, no calibration, outcome-blind region selection. The only new ingredient is what the selected regions are compared against.

For each selected region, the experiment searches the **same checkpoint** for other supported radius-4 regions to serve as controls. Using the same checkpoint removes several obvious alternatives at once: selected and control regions share the same global morphology, developmental stage, density, environmental history, crystal extent and random-stream family.
 Whatever differs between a selected region and its control, it is not the crystal they live in.

Controls are matched on pre-outcome geometry — occupancy fraction, center radial position, occupied count, internal and external frontier counts, probe depths, boundary occupied fraction — and cannot reuse a center or be one of the observed regions. Crucially, **no causal outcome is used in matching**. A null constructed by selecting controls that scored low would be a null with the answer already inside it.

The matching worked. Across 192 groups and 1,151 selected-control pairs, every group was covered, the mean standardized match distance was 1.18 against a frozen limit of 4 (maximum 3.06), mean occupancy-fraction difference was 0.027 and mean radial difference 1.78. The frozen matching-quality criteria were comfortably satisfied.

The estimand is now different:

$$
M_{\text{excess}} = M_{\text{selected}} - M_{\text{matched control}}
$$

---

## A New Question Needs a New Threshold

The raw threshold of 0.15 belonged to raw modularity. Excess modularity is a different quantity, so it needs its own smallest effect of interest, frozen before the result: **+0.10**.

The selected regions have to beat matched arbitrary geometry by more than ten percentage points before we are willing to call that causal privilege. This is the same discipline Chapter 6 applied to its magnitude gate and Chapter 11 to its ±0.15 band — and it matters more here than anywhere, because without it any small positive residual could be narrated into an individual.

---

## The Controls Look Just as Modular

The selected regions reproduce the large raw result:

```text
M_selected   0.4436
M_control    0.4559
M_excess    −0.0123     95% CI [−0.0327, +0.0072]
```

The controls score slightly higher. The interval crosses zero, so there is no basis for claiming that arbitrary regions are *more* modular than the selected ones — that direction is unresolved and should stay that way.

But the question we actually asked is fully resolved. The upper bound of the interval is `+0.0072`, against a declared meaningful threshold of `+0.10`, with an achieved MDE of `0.0265`. The achieved MDE was about `0.0265` against a declared meaningful excess of `0.10`, so the experiment had substantially more precision than required to resolve that target.

The upper confidence bound was only `+0.0072`.

```text
BOUNDED BELOW THE MEANINGFUL THRESHOLD
```

This is not merely a failure to reach significance.

It is a precision-bounded negative for the declared claim: scientifically meaningful positive excess modularity of `+0.10` is incompatible with the observed interval under this test.

Geometry-matched control disks of the same radius, drawn from the same crystal without reference to causal outcome, exhibit essentially the same raw containment as the selected regions.

---

## Nothing Was Hiding in the Components

A combined score can conceal two opposing effects. Perhaps the selected regions retained internal influence better but also admitted external influence more freely, with the difference cancelling.

They did not.

```text
excess internal retention     −0.0066     [−0.0222, +0.0093]
excess external penetration   +0.0057     [−0.0101, +0.0216]
```

Neither component shows a privileged region. The selected regions do not hold onto their own causal influence better than matched controls, and they do not keep outside influence out better either. The combined score is therefore not hiding an opposing component-level advantage for the selected regions.

---

## The Observer Can Create an Inside

The deeper lesson is about what a boundary does to a measurement before it does anything to a system.

Draw a circle and the analysis immediately acquires observer-defined categories: inside, outside, crossing, retention and penetration.
 Every one is now measurable, and the resulting statistics can be large, precise and reproducible without demonstrating that the dynamics themselves privilege the imposed boundary.

```text
OBSERVER-DEFINED BOUNDARY
a partition we impose, which organizes our measurement

SYSTEM-PRIVILEGED BOUNDARY
a partition the dynamics themselves distinguish
```

The experiment certainly contains the first.

Under this operational test, it did not establish the second.

> **A boundary can organize our measurement without organizing the system.**

That distinction has been quietly implicated in several earlier failures. Chapter 9's predictive-coherence result was large because any sizeable chunk of a structured field predicts itself. Its localization result was strong at an arbitrary interior circle as well as at the candidate boundary. In both cases, an observer-defined partition plus ordinary spatial structure could explain the apparent privilege.

Chapter 13 exposes the same problem with a much stronger-looking causal statistic.

---

## Containment Is Not Individuation

The bounded conclusion:

> **At frozen radius 4, selected Digital Crystal regions exhibited strong raw causal containment — internal retention around 0.78 against external penetration around 0.34 — but this asymmetry did not exceed same-checkpoint regions matched on occupancy, radial position, frontier structure and boundary geometry. The 95% interval for excess modularity ran from about −0.033 to +0.007, far below the predeclared +0.10 margin.**

Which gives the distinction the chapter exists to earn:

```text
CAUSAL CONTAINMENT
≠
CAUSAL INDIVIDUATION
```

A local process automatically produces spatial asymmetry. Influence spreads locally, so a region drawn around a source contains some of that influence; a larger region contains more; a source outside the region overlaps it less. Containment can arise from locality plus an imposed boundary.

For this statistic to support causal individuation, the selected region must exhibit organization beyond what comparable geometry already produces.

Under the tested radius-4 criterion, that meaningful excess was not found.

Scope that carefully. This is one operational criterion, at one radius, with circular regions, under an eight-step horizon, using this modularity statistic. It does not establish that no individual can exist here. Non-circular or time-varying regions, process-defined boundaries and other operational criteria for individuation were untested
 — and this chapter is not the place to start proposing them, because listing alternative rescues is the reflex the book has spent twelve chapters declining.

Notice, too, what did not save us. The candidate object was much stronger than Chapter 9's. It had history-dependent sensitivity, trajectory redirection, turnover, local causal structure, and a huge raw containment asymmetry. Every one of those is real. None of them adds up to an individual.

```text
history-dependent process
+
strong causal containment
≠
individuality established

```

---

## What Exactly Failed?

It is worth being precise about what went wrong, because the answer is unusual.

The first experiment was not underpowered — its MDE was `0.0268` against a threshold of `0.15`. It was not badly implemented; the corrected transient intervention from earlier chapters was used, the known global channels were removed, and the structural far-field assertion held. It was not p-hacked; the regions were selected blind to outcome and the threshold was frozen. It replicated: the selected regions scored 0.4402 the first time and 0.4436 the second.

Large. Precise. Predeclared. Replicated.

And the inference from that result to individuation still failed.

Not because the number was wrong.

The number accurately measured causal containment.

The mistake was treating that containment score as evidence of privileged individuation before asking how much of the same score ordinary matched geometry could generate.
 No amount of additional precision on raw `M` could answer the missing question.

The individuation claim required a different estimand:

```text
raw modularity
→ measures containment

excess modularity over matched geometry
→ tests causal privilege beyond geometry
 What caught it was a descriptive secondary — a scale sweep run for completeness — showing the score doing something a real boundary would not do.

That is the most dangerous kind of failure this book has encountered, and it is worth asking how many earlier results could have been the same thing wearing better clothes. Reoccupation tempted us toward repair.

Persistent historical traces tempted us toward memory.

Non-local redistribution tempted us toward amplification.

Strong causal containment tempted us toward individuality.

Each time the phenomenon survived, while a stronger control narrowed what we were allowed to call it.

The problem is no longer how to extract another property from the Crystal.

It is how to tell the difference between:

```text
a failed phenomenon
a failed hypothesis
a failed measurement
and
a real measurement attached to the wrong claim
