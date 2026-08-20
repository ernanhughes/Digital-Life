+++
title = "12: Is There Actually One Thing Here?"
date = "2026-08-14T18:00:00+01:00"
draft = false
description = "We have said 'the crystal' for six chapters without testing whether the noun refers to anything. Two experiments test a privileged spatial boundary. Neither supports one, while both tested radial cuts show comparable same-side causal localization."
weight = 12
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Boundaries", "Process", "Experiments"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with a suspicion about a word.

We have been saying *the crystal* comfortably since *The Digital Crystal*, and the noun has been doing quiet work ever since. We kept using it after material became impermanent. We kept using it after large material turnover appeared beneath the visible state. We kept using it after computational opportunity was shown to strongly constrain its scale, and after no tested budget produced a stationary population.

Through all of that, the sentence "the crystal is doing X" kept seeming like a sentence about something.

The justification has always been the same, and it has never been tested:

```text
there is a connected occupied structure
↓
therefore there is one natural object
```

That inference deserves an experiment. Not the largest possible one — this chapter does not attempt to decide whether the Digital Crystal is an individual. It tests two operationally defined ways a spatial region might earn causal privilege.

Failure of both criteria would not prove that no natural boundary exists. It would mean only that connected occupied geometry has not earned one under these tests.

The question is prior and weaker:

> **Does the connected occupied crystal have a privileged causal boundary or region that justifies treating it as one natural object?**

Or, more operationally: is there a spatial region whose future belongs especially to itself?

---

## Why We Should Already Be Suspicious

Humans look for boundaries when identifying things. Biology and engineering give us many visually compelling ones — membranes, skin, shells, chassis — and they make inside and outside feel like natural places to begin looking for a thing.

The Digital Crystal owes us nothing of the kind, and the last three chapters have been quietly making the boundary assumption harder to hold.

*Can Experience Change the Material?* found that retained material matters only while it remains coupled to the causal aperture. *What Survives Material Loss?* then separated two ideas we had previously allowed to blur together:

```text
CONSTRUCTION INTERFACE
→ empty locations currently eligible for attachment

CAUSAL APERTURE
→ existing material whose state can influence
  decisions at those locations
```

Loss showed that both can reappear deep inside material that had previously fallen behind the visible outer surface. The previous chapter then removed one more assumption: even an eligible construction opportunity need not receive computation, because under a finite evaluation budget only some of those opportunities are evaluated.

So a site can sit in inactive bulk on one update and return to an active interface on the next, because nearby material disappeared. That already makes a fixed geometric shell a less obvious candidate for the system's causal boundary — which should have made us suspicious of any definition based on a centered radius.

We tried one anyway, because the obvious hypothesis is the one that has to be tested first.

---

## What Would Make a Region Special?

Start with something weaker than causality and easier to measure: prediction.

If some region of the crystal deserves special causal attention, one possible signature is that its present state contributes unusual predictive information about its own future beyond what its surroundings already provide. If adding the region's own state contributes nothing beyond the environment, this criterion gives us no reason to privilege that region.

So define, at each measurement point, `S_t` as the candidate region's process state, and `E_t` as the process state of the surrounding annulus running from the candidate radius out to the frozen active outer measurement radius. The question is whether the candidate region contributes predictive information beyond that annulus.

Call the improvement from adding the region's own state the **self-prediction gain**:

```text
Δ_self
=
R²(S_t + E_t → S_future)
-
R²(E_t → S_future)
```

That is not yet the primary statistic. The same calculation is performed on an observer-only spatially scrambled representation, producing `Δ_self,null`, and the quantity reported below is the difference between the two:

```text
EXCESS PREDICTIVE COHERENCE
=
Δ_self,real
-
Δ_self,null
```

So the question is not merely whether a region predicts itself. It is whether it does so more strongly than the frozen observer-null construction.

One detail matters more than it looks. The state representation is not a bitmap of occupied cells. For each region, the predictor receives a 19-dimensional process vector:

```text
population density                 frontier density

recent attachment fraction         recent loss fraction
recent first-occupation fraction   recent reoccupation fraction
recent gross-turnover fraction

6 angular-sector population densities
6 angular-sector turnover densities
```

The recent-flow terms are accumulated over a frozen four-update history window. The prediction models standardize these features on the training data and are evaluated on held-out run groups.

By this point in the book, describing a region by its occupancy alone would be repeating a mistake we have already made twice. Visible form turned out to be an incomplete description of executable state in *The Crystal Gets a Past*, and net population turned out to hide almost all the activity in *What Survives Material Loss?*

The substrate was frozen at a loss rate of `δ = 0.08` and a neutral evaluation budget of `B = 96`. Five candidate scales were frozen in advance as fractions of the crystal's effective radius `R_eff` — the maximum Euclidean distance from the origin to any currently occupied cell, computed separately at each checkpoint:

```text
R / R_eff

0.30
0.45
0.60
0.75
0.90
```

A minimum effect of `0.02` was declared before running, together with a family-level permutation null — because testing five scales and reporting the best one is a search, and the null has to know that.

---

## It Looks Like We Found One

The excess predictive coherence came out as:

| candidate scale | excess predictive coherence |
|---|---:|
| 0.30 `R_eff` | 0.1691 |
| 0.45 `R_eff` | 0.0447 |
| 0.60 `R_eff` | 0.0611 |
| 0.75 `R_eff` | 0.1666 |
| 0.90 `R_eff` | 0.2906 |

The outermost candidate looks striking. An excess R² of `0.2906` is far above the declared minimum, and it appears at exactly the scale that would make an enclosing boundary interesting.

For a moment it looked as though we had found a privileged outer region.

---

## The Null Finds Them Too

Then the family null.

```text
observed family maximum       0.2906
permutation null mean         0.2569
null 95th percentile          0.2947
one-sided                     p ≈ 0.0849
```

The family-level future-permutation null produces maxima of nearly the same size. Its mean maximum is already `0.2569`.

That matters because this is a second control beyond the observer-side spatial scramble used inside the predictive-coherence statistic. The family permutation preserves the fact that we searched five frozen scales and then selected the maximum, and under that search-aware null a maximum near the observed value is no longer unusual.

The observed `0.2906` does not clear the family-level test. We did not tune the radius, add new candidate scales or replace the decoder after seeing the result. The frozen predictive-boundary criterion is **FAILED**.

That is already enough to prevent `0.90 R_eff` from being promoted on the strength of this experiment.

---

## Predictability Is Not a Boundary

The interesting thing here is not the failure. It is why the null was so strong.

Large regions of this system share growth phase, population scale, turnover regime, frontier geometry and stochastic context. Those shared variables can make a region highly predictive of its own future without making that region a privileged causal object. High predictability is real; its interpretation is the problem.

```text
PREDICTIVE COHERENCE
≠
PRIVILEGED BOUNDARY
```

Which is worth stating in its general form, because it is a trap the whole field of this book walks into repeatedly:

> **Predictive coherence alone does not identify a natural boundary.**

There is an echo of *It Looked Like Flocking* here. The flocking result was large until the control showed how much geometry could generate on its own; here the predictive statistic is large until the family null shows how much structured shared dynamics can generate on its own. In both cases, the magnitude of a statistic is not enough. The control determines what the statistic means.

---

## The Geometry Was Suspect Anyway

A post-run audit of this experiment found several things wrong with it, and it is worth recording them without using them as an escape hatch.

The candidate system was defined as a centered region, when the last three chapters all point at causal activity living near dynamically generated interfaces rather than around a geometric center. The observer-null environment was not exactly geometry-matched to the real annular environment, which muddies the comparison.

One piece of the measurement geometry also depended on future extent. The outer measurement radius was constructed using the larger of the present and future effective radii, so part of the support used to define the predictive measurement had access to information that would not have been available at the present checkpoint.

And the scrambled candidate region was regenerated independently at different times, so the null never preserved a stable temporal identity for the region it was standing in for.

None of that rescues the hypothesis. The correct status is both things at once: the primary predictive hypothesis is **FAILED**, and the protocol was **not clean enough for a strong claim**.

An experiment can fail its declared hypothesis while also revealing weaknesses in the way that hypothesis was operationalized. Those are separate results. Neither rescues the other, but the protocol audit tells us what kind of experiment not to run next.

What not to do next is obvious: try 0.87, 0.88, 0.91. Add a scale. Change the feature set. Use a bigger model. Every one of those would be a search for a number, and by now we know exactly where that road goes.

Change the evidence type instead. If a boundary is real in any causal sense, then perturbations should care about it.

---

## Stop Predicting. Perturb It.

Carry the strongest predictive candidate forward — the outer boundary at `0.90 R_eff` — and compare it with an ordinary interior pseudo-boundary at `0.60 R_eff`. The outer candidate now has to demonstrate something the arbitrary interior line does not.

> **Does the outer candidate boundary localize causal consequences more strongly than an arbitrary interior boundary?**

The intervention: at a checkpoint, remove exactly 16 occupied cells, either just inside or just outside the boundary in question. Intervention sites are matched on occupied-neighbour count, absolute distance from the boundary, and exact count, so the two conditions differ in which side they hit rather than in what they hit.

Both branches then run forward under the cell-keyed common-random-number coupling from *The Crystal Gets a Past*, so that the comparison is a paired counterfactual and not an accumulation of reassigned random draws.

Eight updates later, we measure occupancy divergence from the unperturbed control in an inner target shell and an outer target shell, each normalized by the number of lattice sites in that target shell. For each proposed boundary, define:

```text
CAUSAL LOCALIZATION
=
(inside perturbation → inner response
 - outside perturbation → inner response)

+

(outside perturbation → outer response
 - inside perturbation → outer response)
```

A positive score means that perturbations have larger consequences on the same side of the boundary from which they originated. The primary statistic is then the candidate localization at `0.90 R_eff` minus the control localization at `0.60 R_eff`. If the outer candidate boundary is privileged under this criterion, that difference should be positive and scientifically large enough to clear the frozen gate.

One limitation matters more than the nominal sample size suggests. The experiment requested `96` independent groups, but only `25` satisfied the frozen matching requirements for both the candidate and control comparisons. The remaining `71` were excluded because suitable inside/outside perturbation sets could not be matched on the required local geometry.

So the causal estimand is not all Digital Crystal states. It is the subset of tested states in which the frozen matched intervention could actually be constructed.

That restriction reduces precision and may also restrict generalizability, because the 25 usable groups are not guaranteed to be a random sample of the 96 requested groups. The direction of the supported comparison can still be reported; its magnitude should not be generalized beyond that region of experimental support.

But the measured direction does not support the hypothesis either. The candidate boundary scores lower than the control.

---

## The Outer Boundary Does Not Win

| measure | value |
|---|---:|
| candidate boundary localization, `0.90 R_eff` | ≈ 0.03772 |
| interior control localization, `0.60 R_eff` | ≈ 0.04497 |
| candidate − control | ≈ −0.00724 |
| 95% interval | [−0.01399, −0.00020] |
| one-sided test for candidate superiority | p ≈ 0.9693 |

The candidate boundary did not localize causal consequences more strongly than a circle we drew through the interior on purpose to be unremarkable. If anything it did slightly worse. The frozen causal-localization criterion is **FAILED**.

Resist the obvious next move. This is not evidence that `0.60 R_eff` is the real boundary — it is a control, chosen precisely because nothing distinguishes it, and promoting it would be exactly the maneuver we refused in the previous two chapters.

Within the 25 matched groups the measured direction is negative, with a bootstrap interval of `[−0.01399, −0.00020]`. But those 25 groups are only the subset for which the frozen match existed. The result therefore gives us no reason to rescue candidate superiority, and it does not justify turning the small negative magnitude into a general claim that the interior control is "better." The result says one thing:

> **The proposed outer boundary was not privileged under this causal-localization test.**

This is a considerably harder failure than the first one. Predictive coherence could be dismissed as an indirect, observational measure — perhaps the boundary was real and prediction was simply the wrong instrument.

This experiment intervened directly. It changed material on one side of a candidate boundary and measured where the downstream difference appeared, and under the frozen localization measurement the candidate outer boundary was no more privileged than the interior control.

---

## But Same-Side Localization Survives

Now look underneath the failed comparison, at the components that went into it.

| component | candidate (0.90) | control (0.60) |
|---|---:|---:|
| inside perturbation → inner response | 0.02709 | 0.02869 |
| outside perturbation → inner response | 0.00896 | 0.00359 |
| inside perturbation → outer response | 0.00508 | 0.00545 |
| outside perturbation → outer response | 0.02467 | 0.02530 |

Every reported component mean points in the same direction. At both tested radial cuts, an inside perturbation produces the larger inner response, and an outside perturbation produces the larger outer response.

So under this intervention and eight-update measurement window, the experiment measured positive **same-side causal localization** at both boundaries. And that is exactly why it does not distinguish the outer candidate from the interior control. The useful result is not that localization is uniquely strong at the proposed boundary. It is that comparable localization appears at both tested cuts.

```text
SAME-SIDE CAUSAL LOCALIZATION
MEASURED AT BOTH TESTED RADIAL CUTS

PRIVILEGED OUTER BOUNDARY
NOT SUPPORTED BY THIS TEST
```

What survives is a same-side localization pattern. What fails is boundary privilege. The failed hypothesis and the surviving phenomenon are the same measurement read two ways.

---

## Local Does Not Mean Individual

The temptation now is to treat locality as a consolation prize that quietly means the same thing. It does not.

Spatial locality by itself is a weak criterion for individuality. Many locally coupled systems produce stronger nearby than distant consequences without possessing a privileged enclosing object, so locality cannot do the work the failed boundary hypothesis was supposed to do.

What we measured here is narrower: perturbations produced stronger effects on the same side of each tested boundary than across it. That establishes same-side causal localization under this protocol. It does not establish a general distance-decay law, propagation velocity, causal closure or a privileged inside/outside decomposition.

What we have not shown, and should not be read as having shown, is causal closure, autonomy, a privileged inside and outside, or an individual. There are stronger formal notions of causal boundary that these experiments did not test.

So keep the negative result scoped precisely:

| Criterion | Status |
|---|---|
| one predictive boundary criterion | **FAILED** |
| one causal-localization boundary criterion | **FAILED** |
| no natural boundary exists | **NOT ESTABLISHED** |

---

## Look Backward

Two failures at the same question is usually a sign to look at the question rather than the answers. So we went back through what the previous chapters had actually established, and something lined up that had not been visible chapter by chapter.

*Can Experience Change the Material?* found that retained material matters only while it remains coupled to an active causal aperture. *What Survives Material Loss?* found that loss can create new construction interface inside material that had previously become causally remote. *What Does It Cost to Stay?* found that finite computation determines which eligible construction opportunities receive evaluation.

And this chapter finds same-side causal localization at both tested radial cuts, with neither cut earning boundary privilege.

Read separately, these are four experimental findings. Read together, they point toward the same dynamical question:

```text
where are transitions available?
which receive computation?
where do their consequences remain local?
```

There is another recurring pattern further back.

*The Digital Crystal* recovered broad source-family information without establishing recoverable temporal order. *The Crystal Gets a Past* found causal pulse consequences without sender identity or exact chronology, and different particular futures without a stable population-level history signature. *Can Experience Change the Material?* produced persistent and accessible material distinctions without establishing scientifically meaningful differential use of those pasts under a common challenge.

That does not establish a process ontology. But it adds another reason to investigate the dynamics directly rather than infer organization from the accumulated material alone.

---

## The Bulk and the Flux

Here is one way to say what may have gone wrong with the framing. If we define the system as *occupied cells inside radius R*, we are defining it by what has accumulated.

*What Survives Material Loss?* showed that large gross material traffic can hide beneath comparatively modest net population change. The previous chapter then showed something subtler: finite computation can strongly change the population reached, while an apparently stable gross-turnover aggregate turned out to be largely constrained by the loss protocol and accounting identity.

What remained informative was the behaviour of the component flows, especially the different response of reoccupation and first occupation under severe scarcity.

```text
BULK      what remains occupied
FLUX      where material transitions are actually occurring
```

Both are real, and it would be wrong to say the bulk is meaningless — occupied material is exactly what determines where the next opportunities appear, so the flux is generated by the bulk it is rearranging.

The narrower claim is this: occupied material alone may not pick out the natural causal object. The analogy is imperfect, but useful. Defining the Crystal only by its current occupied material may be like defining a river only by the particular water present at one moment.

The material matters. It may simply not be the whole object we need to measure.

---

## A Thing or a Flow?

The question that has been hanging over this chapter deserves an honest and unsatisfying answer.

Is the crystal one natural thing? These experiments did not establish that. Is it instead one coherent flow or process? They did not establish that either.

Replacing *thing* with *process* would merely exchange one unearned ontology for another. Everything measured in this chapter is also compatible with a spatially structured stochastic field whose local dynamics do not pick out one privileged individual.

So these measurements cannot decide the question by themselves. And even a stable flux would not be sufficient evidence of coherent organization — persistence of a dynamical pattern does not, by itself, establish a natural individual.

So the honest position is that both nouns remain unearned, and the process-oriented description is now the more promising *candidate* rather than the answer. That is a smaller conclusion than either side of the title, and it is the one the evidence supports.

---

## Stop Drawing the Body First

What the chapter really produced is a change in method. Both experiments begin the same way:

```text
draw candidate region
↓
ask whether it is special
```

Reverse it.

| OLD | NEW |
|---|---|
| choose a region | measure the causal process |
| ask if it behaves like a thing | find coherent organization |
| impose a boundary | only then ask whether a boundary emerges |

There are mature examples of this reversal elsewhere. In fluid dynamics, coherent structures can be identified from the dynamics of transport rather than selected from snapshot geometry.[^haller] The analogy goes no further — we have not applied that machinery here — but its methodological lesson is enough: a candidate object can be sought in dynamics rather than drawn first and justified afterwards.

[^haller]: G. Haller, "Lagrangian Coherent Structures", Annual Review of Fluid Mechanics 47, 137–162 (2015).

If a natural boundary exists here, the next strategy should allow it to emerge from measured causal organization rather than require us to specify its geometry in advance.

That changes the experimental object.

---

## Experimental Note

This chapter contains two frozen experiments under the same lossy, finite-budget Digital Crystal substrate, at a loss rate of `δ = 0.08` and a neutral evaluation budget of `B = 96`.

### V1 — Predictive Coherence Screen

The V1 quick profile used:

| parameter | value |
|---|---:|
| independent run groups | 96 |
| radius | 72 |
| warmup | 20 updates |
| continuation | 84 updates |
| prediction horizon | 4 updates |
| history window | 4 updates |
| checkpoint stride | 4 updates |
| held-out fraction | 0.25 |
| ridge alpha | 10.0 |
| family permutations | 1000 |
| alpha | 0.05 |
| meaningful excess R² | 0.02 |

The five candidate spatial scales were frozen at `0.30`, `0.45`, `0.60`, `0.75` and `0.90` of `R_eff`, and for each scale the self-prediction gain was:

```text
Δ_self
=
R²(S_t + E_t → S_future)
-
R²(E_t → S_future)
```

The observer-null region preserves how many lattice locations belong to the candidate in each of six radial bins, but reassigns which angular locations receive that membership using keyed observer-only randomness. It therefore preserves approximate radial scale while destroying the centered contiguous region assignment. The null does not alter the Digital Crystal itself.

The reported scale statistic was excess predictive coherence, `Δ_self,real − Δ_self,null`. The primary family statistic was the maximum across all five frozen scales, and a run-group current/future permutation test preserved the full five-scale selection procedure.

The post-run V1 audit identified four protocol limitations: the candidate geometry was centered; the observer-null environment was not exactly matched to the real annulus; future extent entered part of the measurement-support bookkeeping; and the scrambled region lacked stable temporal identity across checkpoints. Those limitations do not rescue the failed frozen family test. They limit the strength of any interpretation built from V1.

### V2 — Causal Boundary Localization

V2 changed evidence type rather than tuning V1. The quick profile used:

| parameter | value |
|---|---:|
| requested groups | 96 |
| usable matched groups | 25 |
| radius | 72 |
| warmup | 20 updates |
| checkpoint after warmup | 36 |
| response horizon | 8 updates |
| candidate radius | 0.90 `R_eff` |
| control radius | 0.60 `R_eff` |
| boundary shell width | 4 |
| distance matching bin | 1 |
| removed cells | 16 |
| meaningful candidate excess | 0.01 |
| bootstrap repetitions | 3000 |
| sign-flip permutations | 4000 |
| alpha | 0.05 |

Inside and outside interventions were matched on occupied-neighbour count, absolute distance from the boundary, and exact removal count. Future stochastic draws were cell-keyed across counterfactual branches. Occupancy divergence from the unperturbed control was measured in inner and outer target shells and normalized by target-shell size.

For each boundary:

```text
causal localization
=
(inside → inner - outside → inner)
+
(outside → outer - inside → outer)
```

and the primary statistic was `localization(0.90 R_eff) − localization(0.60 R_eff)`.

The `0.60 R_eff` region is a predeclared interior pseudo-boundary control. It is not claimed to be a geometry-perfect null or an alternative candidate individual.

Full per-group results and lower-level protocol details remain in the accompanying experimental record.

---

## Evidence Ledger

| Claim | Status | Evidence / limitation |
|---|---|---|
| Some frozen spatial scale shows excess predictive coherence large enough to beat the family null | **FAILED** | family maximum `0.2906`, null 95th percentile `0.2947`, `p ≈ 0.0849` |
| `0.90 R_eff` is a privileged predictive boundary | **NOT SUPPORTED** | frozen family test failed; post-run audit also identified protocol weaknesses |
| Within the matched V2 support region, `0.90 R_eff` localizes causal effects more strongly than the `0.60 R_eff` pseudo-boundary | **FAILED** | 25/96 groups were matchable; candidate-minus-control `−0.00724`, 95% interval `[−0.01399, −0.00020]`, one-sided superiority `p ≈ 0.9693` |
| Same-side causal localization appears at both tested radial cuts | **SUPPORTED** | all four reported component means are larger on the same side than across the cut; component-wise uncertainty was not separately used as a hypothesis gate |
| Same-side localization identifies a privileged boundary | **NOT SUPPORTED** | the same qualitative pattern appears at the arbitrary interior control and is consistent with short-horizon local propagation |
| V2 result generalizes to all tested crystal states | **NOT CLAIMED** | only 25 of 96 requested groups satisfied the frozen geometry-matching requirements |
| No privileged natural boundary exists anywhere in the Digital Crystal | **NOT CLAIMED** | only two operational boundary criteria and a limited set of spatial candidates were tested |
| Stronger formal boundary criteria hold or fail | **NOT CLAIMED** | conditional-independence, closure and related criteria were not tested |
| Dynamically generated construction interfaces repeatedly mediate causal opportunity | **SUPPORTED** | Chapters *Can Experience Change the Material?*, *What Survives Material Loss?*, and *What Does It Cost to Stay?* provide distinct mechanisms |
| Stable normalized flow defines a natural individual | **NOT CLAIMED** | flow stability is neither established as an independent invariant nor tested as an individuation criterion |
| The crystal is a coherent process rather than a thing | **NOT CLAIMED** | the measurements are also compatible with a structured local stochastic field |

Note the sample limitation attached to the second failure: 25 usable groups out of 96 requested. The direction of that result does not support the hypothesis, but its magnitude should not be quoted as though it were precise.

---

## Measure One Event

We spent this chapter testing whether two proposed spatial descriptions deserved causal privilege.

Neither did.

That is more useful than it sounds, because the thing that failed was not a measurement. It was an assumption we had been carrying since the crystal was first drawn on a screen: that a connected region of material is the object, and the process is something happening inside it.

Both experiments inherited that body-first assumption in their design. They could test whether the regions we supplied were privileged. They could not discover a differently shaped organization we never proposed.

What survived is smaller and more useful:

> **local interventions produce spatially localized consequences.**

That is a statement about events and effects rather than about bodies and edges, and it suggests that we have been starting at the wrong end of the problem.

So stop drawing the object first. Start with one event. Change one attachment. Then follow what that change actually causes.

If coherent organization exists, perhaps its structure will emerge from those causal consequences rather than from a boundary we supplied in advance.

> **What does one local event actually cause, and where is causal leverage created?**
