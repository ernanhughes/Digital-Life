+++
title = "16: We Found an Individual. Then We Didn't."
date = "2026-08-15T01:00:00+01:00"
draft = false
description = "A region of the Digital Crystal shows strong, precise causal containment. Then same-checkpoint regions matched on spatial geometry show essentially the same containment."
weight = 16
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Individuality", "Experimental Method"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "review"
+++

The *Is There Actually One Thing Here?* chapter asked whether visible geometry marked a privileged boundary, and failed twice to establish one.

Its candidate regions were defined primarily by geometry.

That left open a stronger possibility: perhaps a boundary that is unremarkable as shape could still be privileged causally.

Since then the book has been replacing geometric intuition with causal tests.

*What Does One Attachment Cause?* measured the consequence of one local event.

*Can Finite Computation Couple Distant Events?* showed that a shared finite selector can route those consequences outside the one-step reach of the local rule.

The previous chapter then established something different: visible occupancy does not exhaust causal state. Experimentally written hidden material can change how the same perturbation is expressed.

That result makes a purely visual definition of individuality even less attractive.

But this chapter does **not** carry the previous chapter's hidden material into the individuation experiment. The causal-modularity runs deliberately clear material state and remove the two known global coupling channels.

The question here is narrower:

Can ordinary local dynamics privilege one spatial partition over comparable geometry?

That makes the individuation question worth asking again, and worth asking properly:

> **Is there a spatial region whose causal containment exceeds what comparable spatial geometry already produces?**

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

Then perturb a supported frontier cell just **outside** the same region, from the same one-occupied-neighbour probe class, and measure what fraction of *that* influence lands inside:

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

One estimator detail matters.

For each probe and lag, the experiment computes

$$
\Delta p(y,t)
=
p_{\mathrm{FORCE}}(y,t)
-
p_{\mathrm{PREVENT}}(y,t).
$$

It then accumulates `|Δp|` over the eight-update horizon, excluding the intervention cell itself.

`A_inside` is that absolute expected causal mass inside the candidate region.

The phrase is shorthand and should not be read as physics. Accumulated `|Δp|` is not a conserved substance: nothing is transported, nothing is depleted, and the same evolving causal consequence can contribute at several lags. It is a bookkeeping quantity for where expected probability shifts appear, not a stuff that moves.

`A_outside` is the corresponding mass outside it.

The retention or penetration fraction is computed per probe, and the relevant probe fractions are then averaged within the region.

Absolute mass matters because the question is **where causal influence is expressed**, not whether positive and negative probability shifts happen to cancel. the *Can Finite Computation Couple Distant Events?* chapter showed that a perturbation can raise some probabilities and lower others; if we summed signed values, a region full of large opposing causal shifts could cancel to nearly zero and appear causally empty. The question here is where the influence went, not what it netted out to.

---

## Remove the Channels We Already Know About

Two long-range mechanisms have already been discovered in this substrate, and both would contaminate a modularity measurement.

The *Can Finite Computation Couple Distant Events?* chapter established that a finite evaluation budget couples distant regions: a local frontier change alters which faraway candidates receive slots, producing effects outside the local causal cone. A region measured under a binding budget would appear less modular for reasons having nothing to do with its own organization.

The previous chapter found a second channel by accident: a global construction-rate calibrator compensating for local changes applies its offset everywhere, coupling regions the physics keeps apart.

So this experiment removes both known global channels by design.

**True unbounded evaluation:** every frontier candidate is evaluated, so there is no competition for evaluation slots.

**No dynamic construction-rate calibration:** no global compensator links spatially separated regions.

The hidden material introduced in the previous chapter is also absent from these runs.

What remains is the ordinary local transition system, observed over an eight-update horizon.

That gives a structural check for free: beyond the eight-step nearest-neighbour causal reach, the expected effect must be exactly zero under this protocol.

The maximum measured absolute far-field expectation was exactly zero and satisfied the frozen `1e-12` assertion tolerance.

That is a correctness assertion, not empirical evidence.

The experiment therefore inherits something useful from earlier failures.

The *Can Finite Computation Couple Distant Events?* chapter identified one global coupling channel.

The previous chapter exposed another.

Both can now be removed deliberately before testing causal containment.

---

## Draw the Regions Before Looking at the Answer

The most obvious way to fake this result would be to run the crystal, look for a patch that seems coherent, draw a boundary around it, and announce that the patch is an individual. That is not an experiment; it is a drawing exercise with statistics attached.

So the regions are fixed-radius hexagonal disks, with the primary radius frozen at `r = 4` and a descriptive sweep across `r ∈ {2,3,4,5}`. Candidates are centered on occupied cells and must satisfy support rules stated in advance: enough occupied cells, occupancy between 20% and 80%, at least two supported internal frontier probes and two supported external-shell probes, where a supported probe is a frontier cell with exactly one occupied neighbour.

The candidates are then ranked using only pre-outcome properties — occupancy fraction closest to 0.50, then radial position, then axial coordinates — and the first three are taken.

No region is selected because it scored well. Nothing about causal outcome enters the selection.

The perturbation reuses the corrected one-exposure intervention developed earlier in the book.

At lag one:

```text
FORCE
x is explicitly occupied

PREVENT
x is blocked from the frontier before growth
```

After lag-one growth, `x` is removed from **both** branches and its absence is asserted. From lag two onward ordinary dynamics resume.

There is therefore one controlled causal exposure without a permanent experimentally maintained focal-state difference. At each of eight lags, before any realized attachment, the expected probability shift is computed for every candidate and its absolute mass accumulated inside and outside the region.

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

The frozen V1 hypothesis passed comfortably:

```text
RAW CAUSAL CONTAINMENT ASYMMETRY
SUPPORTED
```

For a while, it was very tempting to read that as individuation.

That temptation is the subject of the rest of the chapter.

---

## Then the Circle Got Bigger

The scale sweep was a descriptive secondary, run for completeness rather than out of suspicion.

```text
radius 2     M ≈ 0.197
radius 3     M ≈ 0.374
radius 4     M ≈ 0.440
radius 5     M ≈ 0.504
```

The mean score rises at every tested radius:

```text
r = 2    0.197
r = 3    0.374
r = 4    0.440
r = 5    0.504
```

There is no peak or obvious characteristic scale within the tested range.

That does not establish that no natural scale exists.

It does show that the raw statistic is strongly sensitive to the observer's choice of radius, which weakens any attempt to interpret the `r = 4` value itself as evidence of a privileged boundary.

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

Locality plus an imposed partition is therefore a sufficient **candidate explanation** for a large raw containment score.

An internal probe begins inside the observer's disk; an external probe begins across its boundary. Even without a system-privileged boundary, those two geometries can produce different fractions of locally spreading causal mass on either side of the partition.

The scale sweep does not by itself prove that geometry explains V1.

It tells us what the next control must contain.

> **The observer's circle can manufacture the appearance of privilege unless the null already contains the same spatial geometry.**

---

## The Measurement Was Real

It would be a mistake to conclude that the first result was wrong. It was not.

At radius 4, perturbations initiated inside the selected regions genuinely did express far more causal mass inside those regions than external perturbations expressed into them. The number is accurate, the interval is tight, and it reproduces. Nothing about the scale sweep erases that measured containment.

What the sweep undermines is not the measurement but an equation we had made without noticing:

```text
raw causal containment  =  causal individuation
```

V1 supports the left side:

```text
RAW CAUSAL CONTAINMENT
SUPPORTED
```

What remained untested was the inference:

```text
RAW CAUSAL CONTAINMENT
→
SYSTEM-PRIVILEGED REGION
```

That inference requires a spatial null. A stronger control should narrow an interpretation, not retroactively delete a phenomenon — and the phenomenon here is real containment, which will still be true at the end of the chapter.

So the question is not whether to keep the result. It is what comparison would tell us what the result means.

---

## Change the Null, Not the Statistic

There are several tempting moves available at this point, and all of them are wrong.

We could sweep the radius more finely, looking for a scale where the score peaks. We could redefine the modularity statistic to normalize out disk size. We could add features to the region-selection rule until the selected regions score better than the rest. Every one of those adjusts the thing being measured until it produces the answer we wanted.

The actual missing piece is much simpler:

> **Would an arbitrary region with the same geometry produce the same score?**

If selected regions do not exceed same-checkpoint regions closely matched on the predeclared spatial features, then this experiment has no evidence for causal privilege **beyond that matched spatial null**.

If selected regions substantially exceed those controls, then we have evidence of causal privilege not captured by the matched geometry — a necessary step toward an individuation claim, though still not a complete definition of individuality.

The interpretation of a modularity statistic depends critically on its null.

A large score tells us little about privileged organization if the same score is routinely generated by the spatial structure already present in the null.
A similar problem appears in spatial network analysis: apparent community structure can largely reflect the fact that nearby nodes interact more often unless the null already contains that spatial dependence.[^expert]

The methodological parallel is the part that matters here: to interpret excess organization, the null must already reproduce the simpler geometry capable of generating the raw statistic.

[^expert]: P. Expert, T. S. Evans, V. D. Blondel and R. Lambiotte, "Uncovering space-independent communities in spatial networks", *PNAS* 108(19) (2011), 7663–7668.

That is a comparison, not a method we borrowed — we are not doing community detection and have no networks here. But the structure of the problem is identical, and it says exactly what our null has to contain: geometry.

---

## Regions From the Same Crystal

Everything about the measurement is held frozen: radius 4, eight-step horizon, the same transient intervention, the same absolute causal-mass estimator, unbounded evaluation, no calibration, outcome-blind region selection. The only new ingredient is what the selected regions are compared against.

For each selected region, the experiment searches the **same checkpoint** for other supported radius-4 regions to serve as controls. Using the same checkpoint removes several obvious alternatives at once: selected and control regions share the same global morphology, developmental stage, density, environmental history, crystal extent and random-stream family. Whatever differs between a selected region and its control, it is not the crystal they live in.

Controls are matched on pre-outcome geometry — occupancy fraction, center radial position, occupied count, internal and external frontier counts, probe depths, boundary occupied fraction — and cannot reuse a center or be one of the observed regions. Crucially, **no causal outcome is used in matching**. A null constructed by selecting controls that scored low would be a null with the answer already inside it.

The matching worked. Across 192 groups and 1,151 selected-control pairs, every group was covered, the mean standardized match distance was 1.18 against a frozen limit of 4 (maximum 3.06), mean occupancy-fraction difference was 0.027 and mean radial difference 1.78. The frozen matching-quality criteria were comfortably satisfied.

The estimand is now different:

$$
M_{\text{excess}} = M_{\text{selected}} - M_{\text{matched control}}
$$

---

## A New Question Needs a New Threshold

The raw threshold of 0.15 belonged to raw modularity. Excess modularity is a different quantity, so it needs its own smallest effect of interest, frozen before the result: **+0.10**.

The selected regions have to beat geometry-matched controls by more than ten percentage points before we are willing to call that causal privilege. This is the same discipline the *Can Experience Change the Material?* chapter applied to its magnitude gate and the *Can Finite Computation Couple Distant Events?* chapter to its ±0.15 band — and it matters more here than anywhere, because without it any small positive residual could be narrated into an individual.

The number itself carries no deeper theory. It was frozen before the result as the operational smallest effect of interest for this new estimand, and it should be read that way rather than as a boundary where individuality begins.

---

## The Controls Look Just as Modular

The selected regions reproduce the large raw result:

```text
M_selected   0.4436
M_control    0.4559
M_excess    −0.0123     95% CI [−0.0327, +0.0072]
```

The matched controls score slightly higher.

The interval crosses zero, so there is no basis for claiming that the controls are more modular than the selected regions. The directional difference around zero is unresolved and should stay that way.

But the meaningful-margin question is resolved.

```text
M_excess        −0.0123
95% CI          [−0.0327, +0.0072]

meaningful positive excess
                 +0.10

achieved MDE80    0.0265
```

The upper confidence bound sits less than one percentage point above zero and far below the predeclared `+0.10` margin, while the achieved MDE is comfortably smaller than that margin. So this is not merely a failure to reach significance. It is a precision-bounded negative for the declared claim.

```text
MEANINGFUL POSITIVE EXCESS
BOUNDED OUT

DIRECTION AROUND ZERO
UNRESOLVED
```

Those two lines have to stay separate. The experiment excludes positive excess modularity of the declared size; it does not establish that the controls are better.

Geometry-matched control disks of the same radius, drawn from the same crystal without reference to causal outcome, exhibit essentially the same raw containment as the selected regions.

---

## Was the Null Too Close to the Regions?

One concern surfaced after the frozen result, and it was a real one.

The matcher required a different control centre, but it did not require the selected and control disks to be spatially separate. Some matched controls were therefore nearby translations of the selected region — and a null dominated by near-duplicates would be a weak test of whether the result survives spatially distinct comparison regions.

The prevalence was substantial. Across all 1,151 frozen pairs the median radius-four disk overlap was about 33%, the median centre separation was 5, and only 339 pairs — under 30% — were strictly non-overlapping.

So we ran a **post-hoc spatial-overlap audit**, progressively removing the overlapping comparisons to see whether positive privilege emerged once the null was made spatially distinct.

```text
                                      mean excess M       95% CI      groups

all frozen pairs                         −0.012      [−0.033, +0.008]   192

centre distance ≥ 6                      −0.019      [−0.051, +0.015]   183

strictly non-overlapping disks           −0.012      [−0.050, +0.028]   140

zero shared occupied cells               −0.006      [−0.047, +0.032]   150
```

Nothing appears. Every filter leaves the estimate near zero and far below the `+0.10` threshold, and the strictest ones — exact disk non-overlap, zero shared occupied cells — sit closest to zero of all.

These are **post-hoc robustness analyses**, not a replacement for the frozen V2 test, and the stricter subsets cover fewer independent groups than the confirmatory design required. They cannot promote themselves into a new result.

What they can do is test one specific alternative explanation. Across progressively more spatially distinct subsets, the estimate does not move toward positive privilege, so the audit provides no support for the idea that the near-zero excess was produced merely by matching selected regions to near-duplicate copies of themselves.

---

## Nothing Was Hiding in the Components

A combined score can conceal two opposing effects. Perhaps the selected regions retained internal influence better but also admitted external influence more freely, with the difference cancelling.

They did not.

```text
excess internal retention     −0.0066     [−0.0222, +0.0093]
excess external penetration   +0.0057     [−0.0101, +0.0216]
```

The sign convention matters here, because the two components run in opposite directions. Privilege would show up as *greater* internal retention — a positive excess — and as *reduced* external penetration, which is a negative excess. Selected regions delivered neither. Retention came out marginally lower and penetration marginally higher, both intervals crossing zero.

So the near-zero combined score is not concealing an opposing component-level advantage. There is no advantage in either component to conceal.

---

## The Observer Can Create an Inside

The deeper lesson is about what a boundary does to a measurement before it does anything to a system.

Draw a circle and the analysis immediately acquires observer-defined categories: inside, outside, crossing, retention and penetration. Every one is now measurable, and the resulting statistics can be large, precise and reproducible without demonstrating that the dynamics themselves privilege the imposed boundary.

```text
OBSERVER-DEFINED BOUNDARY
a partition we impose, which organizes our measurement

SYSTEM-PRIVILEGED BOUNDARY
a partition the dynamics themselves distinguish
```

The experiment certainly contains the first.

Under this operational test, the selected regions did not establish privilege beyond the matched spatial null.

That scope is worth stating exactly, because the null is a specific one. It controls the declared spatial and interface features — occupancy, radial position, occupied count, frontier structure, probe depth, boundary composition. Matching on interface structure is a double-edged instrument: if a genuinely privileged region expressed its privilege *through* that interface structure, a null matched on it would absorb the very thing under test. So the result bounds privilege relative to this null. It does not exhaust every geometric variable a different null might leave free.

> **A boundary can organize our measurement without organizing the system.**

That distinction has been quietly implicated in several earlier failures. The *Is There Actually One Thing Here?* chapter's predictive-coherence result was large because any sizeable chunk of a structured field predicts itself. Its localization result was strong at an arbitrary interior circle as well as at the candidate boundary. In both cases, an observer-defined partition plus ordinary spatial structure could explain the apparent privilege.

This chapter exposes the same problem with a much stronger-looking causal statistic.

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

Scope that carefully. This is one operational criterion, at one radius, with circular regions, under an eight-step horizon, using this modularity statistic. It does not establish that no individual can exist here. Non-circular or time-varying regions, process-defined boundaries and other operational criteria for individuation were untested — and this chapter is not the place to start proposing them, because listing alternative rescues is the reflex the book has spent twelve chapters declining.

Notice, too, what did not save the individuation claim.

By this point in the book we had established local causal effects, turnover, computational routing, and the causal sufficiency of experimentally written hidden state.

But the Chapter 16 modularity experiment deliberately stripped away hidden material, finite-selector coupling and global calibration before asking whether the remaining local dynamics privileged one spatial region over matched controls.

It still produced a huge raw containment asymmetry.

And that asymmetry still did not establish causal privilege beyond the matched spatial null.

```text
STRONG CAUSAL CONTAINMENT
≠
CAUSAL INDIVIDUATION
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

excess modularity over matched spatial null
→ tests privilege beyond that null
```

What caught the problem was a descriptive secondary — the scale sweep — showing that the score changed strongly with an observer-controlled quantity that the primary `r = 4` result had treated as fixed.

That did not prove the boundary was unreal.

It exposed a simpler explanation that the primary test had not controlled.

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
```

How do you fail correctly?

## Experimental Note

Both experiments deliberately remove the hidden material state used in the previous chapter.

```text
material state              cleared
evaluation                  true unbounded
dynamic calibration         none
loss rate                   0.08
horizon                     8 updates
primary region radius       4
secondary V1 radii          2, 3, 4, 5
V1 seed                     20260916
V2 seed                     20260917
```

The horizon is shorter than elsewhere in the book by design. This is a test of spatial causal containment rather than long-run morphology, and eight updates keeps the nearest-neighbour causal cone interpretable, limits the number of boundary crossings available, and holds down stochastic accumulation. It is part of this operational test, not a privileged timescale.

Each update proceeds in a fixed order:

```text
current realized branch state
↓
expected Δp measured
↓
candidate probabilities computed synchronously from the pre-growth state
↓
Bernoulli attachment draws
↓
additions applied
↓
background loss applied
↓
next state
```

Candidate regions are occupied-cell-centred hexagonal disks. Before any causal outcome is measured, a supported region must contain at least 12 occupied cells, have occupancy fraction between `0.20` and `0.80`, and contain at least two supported internal and two supported external-shell probes. Supported probes are frontier cells with exactly one occupied neighbour.

At the primary radius, up to three internal and three external probes are used per region. Candidate regions are selected outcome-blind by:

```text
1. occupancy fraction closest to 0.50
2. center radial distance
3. axial coordinates
```

The corrected transient intervention is:

```text
lag 1
FORCE       x occupied
PREVENT     x blocked before growth

after lag-1 growth
x removed from both branches
absence asserted

lag 2+
ordinary dynamics
```

For every probe and lag,

$$
\Delta p(y,t)
=
p_{\mathrm{FORCE}}(y,t)
-
p_{\mathrm{PREVENT}}(y,t).
$$

The intervention site itself is excluded. Absolute expected causal mass `|Δp|` is accumulated over the eight-update horizon.

For an internal probe,

$$
R_{\mathrm{in}}
=
\frac{A_{\mathrm{inside}}}
{A_{\mathrm{inside}} + A_{\mathrm{outside}}}.
$$

For an external-shell probe,

$$
P_{\mathrm{in}}
=
\frac{A_{\mathrm{inside}}}
{A_{\mathrm{inside}} + A_{\mathrm{outside}}}.
$$

Region-level values average the relevant probe fractions, and

$$
M = R_{\mathrm{in}} - P_{\mathrm{in}}.
$$

### V1

```text
independent groups         192
primary radius             4
raw-module SEI             +0.15
M                          0.4402
95% CI                     [0.4194, 0.4614]
MDE80                      0.0268
status                     SUPPORTED
```

The radius sweep was descriptive.

### V2

V2 retains the frozen radius-4 statistic but replaces the interpretation with a same-checkpoint spatial null. It runs on a fresh seed (`20260917` against V1's `20260916`), so its selected-region score is an independent regeneration of the V1 phenomenon rather than a re-analysis of the same sample.

For every selected region, controls are drawn without replacement from other supported radius-4 regions in the same checkpoint and matched outcome-blind on:

```text
occupancy fraction
center radial distance
occupied count
internal n=1 frontier count
external n=1 frontier count
internal probe depth
external probe depth
boundary occupied fraction
```

Hard match gates include occupancy difference `≤0.08`, radial difference `≤6`, occupied-count difference `≤8`, internal/external frontier-count differences `≤4`, and standardized match distance `≤4`.

```text
independent groups         192
matched pairs              1,151
group coverage             1.0
median observed/group      3
median controls/observed   2
far-effect assertion       exactly 0
excess SEI                 +0.10

M_selected                 0.4436
M_control                  0.4559
M_excess                  −0.0123
95% CI                    [−0.0327, +0.0072]
MDE80                       0.0265

primary status             BOUNDED_BELOW_SEI
directional status         DIRECTION_UNRESOLVED
```

The independent statistical unit is the group; region measurements are averaged within group before chapter-level inference.

The structural far-field zero is a correctness assertion, not experimental evidence.

### Post-hoc spatial-overlap audit

Run after the frozen V2 result, in response to review. **Post-hoc robustness only; it does not modify V2's frozen status.**

```text
frozen pairs                   1,151
median centre distance             5
median disk overlap             0.33
strictly non-overlapping         339  (29.5%)

                          M_excess          95% CI        groups  coverage
all frozen pairs           −0.0122   [−0.0331, +0.0081]     192     1.000
centre distance ≥ 6        −0.0185   [−0.0514, +0.0147]     183     0.953
strict disk non-overlap    −0.0120   [−0.0502, +0.0277]     140     0.729
zero occupied overlap      −0.0061   [−0.0467, +0.0320]     150     0.781
```

The stricter subsets fall below the confirmatory design's 90% group-coverage requirement and have wider achieved MDEs (about `0.050`). They are sensitivity checks on the frozen conclusion, not confirmatory results in their own right.

**Statistics.** The independent unit is the group throughout; region and pair measurements are averaged within group before inference. Intervals are bootstrap percentile intervals. SEI is the predeclared smallest effect of interest. MDE80 is the achieved one-sided minimum detectable effect at 80% power, computed as `SE × (z₀.₉₅ + z₀.₈₀)` with `z₀.₉₅ = 1.64485` and `z₀.₈₀ = 0.84162`.

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Radius-4 selected regions show strong raw causal containment asymmetry | **SUPPORTED** | `M = 0.4402`, CI `[0.4194, 0.4614]`, SEI `0.15`, MDE80 `0.0268` |
| Internal perturbations have high raw retention at radius 4 | **SUPPORTED AS MEASUREMENT** | mean retention `0.7755` |
| External perturbations show lower raw inward penetration at radius 4 | **SUPPORTED AS MEASUREMENT** | mean penetration `0.3353` |
| Radius 4 is a privileged or characteristic spatial scale | **NOT ESTABLISHED** | descriptive score rises from `0.197` at `r=2` to `0.504` at `r=5` |
| The scale sweep alone proves geometry caused V1 | **NOT CLAIMED** | sweep motivates the spatial null; it does not identify the cause by itself |
| V2 matching is scientifically valid | **SUPPORTED / GATE PASSED** | all 192 groups covered, 1,151 pairs, outcome-blind same-checkpoint matching, match-quality gates passed |
| Selected regions have positive excess modularity over the matched spatial null of at least `+0.10` | **BOUNDED BELOW SEI** | `M_excess = −0.0123`, CI `[−0.0327,+0.0072]`, MDE80 `0.0265` |
| Selected regions are less modular than matched controls | **DIRECTION UNRESOLVED** | excess interval crosses zero |
| Internal retention shows positive excess over matched controls | **NOT ESTABLISHED** | `−0.0066 [−0.0222,+0.0093]` |
| Resistance to external penetration shows positive privilege over matched controls | **NOT ESTABLISHED** | excess penetration `+0.0057 [−0.0101,+0.0216]` |
| A system-privileged causal boundary was established | **NOT ESTABLISHED** | no meaningful excess over this frozen geometry-matched null |
| Causal containment is the same thing as individuation | **FAILED AS INTERPRETATION** | matched controls reproduce the raw containment |
| No individual can exist in this substrate | **NOT CLAIMED** | one disk geometry, one radius for the confirmatory null, one horizon and one statistic |
| Chapter 16 tests the hidden material state from Chapter 15 | **NO** | V1/V2 clear material state before causal-modularity measurement |
| Organism, self, agent, autonomy, life | **NOT ESTABLISHED** | outside the operational claim |
| Near-overlap between selected and matched regions explains the near-zero V2 excess | **NOT SUPPORTED — POST-HOC ROBUSTNESS** | `M_excess` remains near zero under increasing center separation, strict disk non-overlap (`−0.0120 [−0.0502,+0.0277]`) and zero occupied-cell overlap (`−0.0061 [−0.0467,+0.0320]`); stricter subsets have reduced group coverage |
