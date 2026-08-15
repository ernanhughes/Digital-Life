+++
title = "12: Can Finite Computation Couple Distant Events?"
date = "2026-08-14T22:00:00+01:00"
draft = false
description = "A local attachment changes expected construction in places the local rule cannot reach in one step — because distant opportunities compete for the same evaluation slots. But routing causality is not the same as amplifying it."
weight = 12
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Finite Computation", "Causality", "Experimental Method"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with an accounting oddity it could not resolve.

Forcing one attachment produced a measurable local causal effect. Measured globally — the whole crystal, minus the intervention site — the effect came out *smaller* than the local one. Persistent arm: 1.164 locally, 1.036 globally. Transient arm: 0.198 locally, 0.044 globally. The implied far-field differences were negative in both cases, with intervals overlapping zero, so nothing was established.

The local/global discrepancy was not itself evidence of a far-field effect — its interval still included zero.

But it suggested a mechanism worth isolating.

There was one obvious candidate already present in the substrate: the finite evaluation budget shared by every active frontier site.
 Chapter 8 gave every active location a constraint it shares with every other active location: a fixed number of evaluation slots per update. Chapter 10 established, beyond argument, that a single attachment changes the frontier — by roughly +2 sites in sparse geometry, by about −1 in dense.

Change the frontier and you change the population of candidates competing for a fixed evaluation pool.

That creates a possible causal pathway that does not run through the local attachment rule at all:

> **Can two regions too far apart to interact through the local rule nevertheless affect one another because both compete for the same finite computation?**

---

## Too Far Away to Matter

The attachment rule reaches nearest neighbours and no further. That is structural, not statistical — it is what the rule says.

So at lag one, define:

```text
LOCAL CAUSAL CONE     d ≤ 1
OUTSIDE THE CONE      d > 1
```

A FORCE/PREVENT intervention at `x` cannot alter attachment probabilities at `d > 1` after a single update through the ordinary transition rule. There is no path. Whatever the crystal does out there, the intervention has not reached it.

At lag one, the intervention cannot reach `d > 1` through the nearest-neighbour attachment rule.

That makes the outside-cone region unusually useful.

If FORCE and PREVENT differ there at lag one, the ordinary local transition pathway cannot explain the difference. The finite selector then becomes the mechanism to isolate.

---

## But They Share a Scheduler

Picture two frontier regions far apart on the lattice, with no chain of neighbours connecting them in one step. Both feed candidates into the same selector, and the selector has `B` slots.

Now let one region gain two extra eligible candidates. The budget does not grow. The same `B` evaluations must be distributed over a slightly larger candidate population — so some opportunities that would have been evaluated elsewhere are not, and the expected construction in those distant places changes.

```text
MORE OPPORTUNITY HERE
↓
SAME TOTAL EVALUATION CAPACITY
↓
DIFFERENT OPPORTUNITIES EVALUATED THERE
```

Nothing travels from one region to the other through the attachment rule.

No long-range term is added.

The local transition rule remains nearest-neighbour.

What the distant regions share is the selector.

> **The rule is local. The computational constraint is global.**

---

## Freeze the Crystal, Change Only the Budget

The obvious experiment — grow crystals under different budgets and compare — would be worthless. Budget changes morphology, population, frontier size, history and turnover all at once, and any difference could be attributed to any of them.

So freeze everything. Same checkpoint, same probe `x`, same FORCE/PREVENT intervention, same environment, same cell-keyed randomness, same geometry. Let the intervention create its two lag-one states under the ordinary budget. Then stop the world and vary exactly one thing: what fraction of the frontier is allowed to receive evaluation on that next update.

```text
f = 0.05, 0.10, 0.25, 0.50, 0.75, 1.00
plus an explicit UNBOUNDED arm
```

The same checkpoint generates every budget condition. This is a control-parameter experiment on a single frozen state, not a comparison between differently grown crystals.

The measured quantity is the *expected* far-field construction difference, computed from the branch-specific evaluated candidate sets before any attachment draw is taken. Not a noisy realized count — the exact expectation the rule and the selector jointly imply.

One scope restriction, stated once: every probe here is a single-contact frontier site, with exactly one occupied neighbour. What follows is established in that regime. The run used 384 independent checkpoints, 5,375 supported sites, and seven budget conditions each — 37,625 site-by-budget measurements.

---

## A Difference Outside the Local Cone

Under partial evaluation, FORCE and PREVENT differ in expected construction outside the local causal cone.

For sites where the intervention creates frontier (`FCP = +2`), the far-field effect is negative and grows with evaluation fraction:

```text
f      E_far
0.05   −0.049
0.10   −0.110
0.25   −0.261
0.50   −0.492
0.75   −0.715
```

For sites where the intervention consumes frontier (`FCP = −1`), it runs the other way:

```text
0.05   +0.012
0.10   +0.031
0.25   +0.118
0.50   +0.213
0.75   +0.294
```

Create local frontier opportunity and expected construction falls in the outside-cone region.

Consume local frontier opportunity and expected construction rises there.

The effect appears at a distance the local rule cannot reach in one update.

The sign makes sense the moment you stop thinking about propagation and start thinking about competition. An attachment that creates additional nearby candidates adds claimants to a selector whose total number of slots is fixed.

Some candidates elsewhere therefore lose evaluation opportunity.

---

## Remove the Selector, Remove the Effect

The cleanest part of this experiment is what happens when subsampling disappears.

At `f = 1.00` and in the unbounded arm, every eligible frontier candidate is evaluated. Outside the causal cone, FORCE and PREVENT then have identical candidate sets carrying identical probabilities, so the selector-mediated far-field difference must be exactly zero.

Must be. Not approximately, not on average — the mechanism requires it. The implementation asserts it on every exhaustive intervention, and across the full run that assertion was checked 10,750 times without a violation.

It is important to be honest about what that zero is. It is not a discovery. It is a correctness identity, and quoting it as evidence would be exactly the error this book has flagged repeatedly: reporting a theorem about the code as though it were a fact about the world. A quantity with exactly zero variance across thousands of independent groups belongs in an assertion, not a confidence interval.

The evidence is the *contrast*:

```text
PARTIAL EVALUATION     →  reproducible outside-cone effect
EXHAUSTIVE EVALUATION  →  effect vanishes exactly
```

Under partial evaluation the outside-cone effect appears.

Under exhaustive evaluation the selector-mediated difference is structurally zero.

That intervention on the computational regime identifies finite candidate selection as the mechanism responsible for the measured outside-cone redistribution.

> **The outside-cone coupling is produced by finite candidate selection.**

---

## What Is Actually Conserved

The mechanism becomes sharper once you ask what the selector holds fixed.

When both branches are budget-limited, both select exactly `B` candidates. Split the selected cells into those inside the causal cone and those outside it, and the arithmetic is forced:

```text
Δ(selected near) + Δ(selected far) = 0

therefore

Δ(selected far) = −Δ(selected near)
```

This is an accounting identity of fixed-size selection, not an empirical law — but it says precisely what the constraint conserves. Not attachments. Not construction. Not frontier. Not causal consequence.

**Evaluation slots.**

The far field receives the exact negative of whatever slot imbalance the local intervention creates nearby. That is a conservation law native to the substrate, and it is worth noticing that it has no obvious biological counterpart. A cell does not skip a chemical reaction because a distant cell used too much of a shared quantity of *attention*.

---

## Allocation Is Not Payload

But slots are not equivalent to construction, and conflating them would produce a badly wrong model.

A slot spent on a candidate with attachment probability 0.8 carries four times the expected construction of a slot spent on one at 0.2. So displacing slots and displacing expected construction are different quantities, and the experiment contains a control that separates them cleanly.

At `f = 0.50`, two site classes moved almost identical numbers of far candidates:

```text
                far candidate churn     E_far

FCP =  0            0.483              −0.013
FCP = −1            0.446              +0.213
```

The amount of candidate substitution is similar.

The expected construction consequences are not.

Candidate count alone therefore cannot determine the material effect.

```text
CANDIDATE DISPLACEMENT
≠
CONSTRUCTION DISPLACEMENT
```

The mechanism therefore has two distinct quantities:

```text
ALLOCATION
which candidates receive evaluation

PAYLOAD
the attachment probability carried by those candidates

---

## The Scaling Law

If the mechanism is really slot competition, the far-field effect should follow a specific form. Roughly, it should scale with how much frontier imbalance the intervention created, how large a fraction of the frontier is being evaluated, and how much attachment probability the displaced far candidates carry:

$$
E_{\text{far}} \approx -\Delta F \times f \times \bar{p}_{\text{far}}
$$

which predicts, at any fixed evaluation fraction:

```text
E_far  ∝  −ΔF
```

One subtlety decides whether this works. `ΔF` must be the *actual* lag-one frontier difference, not the checkpoint-level FCP label. Ordinary background loss occurs between the intervention and the selection, so the frontier the selector actually sees is not the frontier we labelled one step earlier. The selector responds to what exists when it runs.

Fitting through the origin at the three low fractions:

```text
f       β        relative residual
0.05    0.0251        12.6%
0.10    0.0571         9.9%
0.25    0.1422         2.6%
```

all inside the frozen 25% aggregate criterion, and tightening as evaluation broadens.

```text
SUPPORTED
```

The high `R²` from fitting three class means through an origin is not the result — three points and a fixed intercept can fit almost anything. The result is that the scaling relation the mechanism predicts is the one the data follow.

There is a further check available. If the model is right, dividing the fitted coefficient by the evaluation fraction should recover the mean probability carried by the far frontier:

```text
f       β/f
0.05    0.502
0.10    0.571
0.25    0.569
```

Across a fivefold change in evaluation fraction, the last two converge near 0.57 — which is what the mechanism says should be sitting there. Worth stating carefully: the far-frontier probability mass was not independently measured here, so this is not a verified parameter recovery. The bounded claim is that the coefficient *behaves like* the payload the finite-selection model predicts.

---

## The Ratio That Didn't Survive

There was a more elegant claim on the table, and it did not hold up.

An earlier single-budget experiment had produced far-field effects of about −0.117 for the frontier-creating class and +0.063 for the frontier-consuming class. Those classes differ by +2 and −1 in nominal frontier change, so a pure slot model predicts a ratio of exactly −2:1, and the observed ratio was −1.86. A parameter-free prediction, nearly hit, with no fitted slope anywhere. It was an unusually attractive result because the prediction contained no fitted parameter.

Frozen as a target across the budget sweep, it fell apart:

```text
f = 0.05    −4.15
f = 0.10    −3.54
f = 0.25    −2.21
```

Only the last comes within tolerance of −2.

```text
UNRESOLVED
```

And the reason is instructive rather than embarrassing. The −2:1 prediction used the checkpoint FCP labels; the actual lag-one frontier differences were closer to +1.84 and −0.78, a magnitude ratio nearer 2.36. The elegant ratio was computed from a descriptor one update upstream of the quantity the selector actually consumes.

So the general scaling survives and the specific ratio does not — the same pattern as several earlier chapters. The broader selector-mediated scaling survives.

The cleaner parameter-free ratio does not.
 Which also tells us that the scalar frontier-size model is not the most proximal description available: slot displacement is closer to the machinery than `ΔF` is, and `ΔF` is closer than FCP.

The per-class residuals point the same way. The frontier-creating classes tracked the model closely at every low fraction; the frontier-consuming class deviated well past the per-class scale at the two smallest fractions before falling into line at 0.25. The aggregate criterion passed. The scalar model is not equally good everywhere.

---

## Distant Without Propagation

What has been established, stated carefully:

> **When the Digital Crystal evaluates only part of its frontier, a local frontier change reallocates a fixed number of global evaluation slots, producing expected construction differences outside the nearest-neighbour causal cone. The effect disappears exactly when evaluation becomes exhaustive.**

Call the phenomenon **finite-budget redistribution**, and note what it is not. It is not communication: nothing is sent and nothing is received. It is not signalling: no structure about the source survives at the destination. It is not propagation: nothing travelled, and the effect appears at lag one in places a signal could not have reached. There is nothing exotic about the causal pathway.

The two regions are coupled indirectly because both feed opportunities into the same finite selector.

That structure is entirely familiar in computer systems, where it is a practical nuisance rather than a philosophical puzzle. Two programs that never exchange a byte, running on separate cores, degrade each other's performance by competing for shared cache and memory bandwidth — and the interference is large and predictable enough that datacenter operators model it explicitly when deciding what to co-locate.[^bubbleup] The processes are causally coupled through the resource, not through any channel between them.

[^bubbleup]: J. Mars, L. Tang, R. Hundt, K. Skadron and M. L. Soffa, "Bubble-Up: Increasing Utilization in Modern Warehouse Scale Computers via Sensible Co-Locations", *MICRO-44* (2011), 248–259.

That is a comparison, not evidence — our crystal is not a datacenter and we have measured nothing about caches. The comparison shows that shared computational bottlenecks can create indirect interference between otherwise separate workloads.

It does not establish that the Digital Crystal result generalizes to every finite computational system.

And it is exactly the kind of thing the substrate-first approach was supposed to turn up. We refused to start with metabolism, energy, membranes or genomes. We introduced one honest computational scarcity in Chapter 8. Three chapters later, that computational scarcity has produced a consequence we did not have to borrow from a biological category:

> **The crystal did not need a signal to couple distant regions. It needed a shared bottleneck.**

Under a shared finite selector, spatial separation beyond the local rule's one-step reach is not sufficient for one-step causal independence.

---

## Surely This Amplifies the Perturbation

Now the temptation, and it is a strong one.

If a local perturbation can recruit consequences outside its causal reach, perhaps finite computation is how small events become large ones. Perhaps selector-mediated redistribution does more than change where the consequence appears.

Perhaps it increases the total finite-horizon consequence of the perturbation.
 That would be a genuinely major claim, and everything so far seems to be pointing at it.

The obvious experiment is to sweep the budget and see whether tighter budgets produce more downstream causal consequence.

That experiment would be worthless, for a reason that should be familiar by now. More evaluation produces more expected attachments, and more attachments produce more downstream attachments. Sweep the budget and any difference in causal consequence could simply be a difference in how much construction is happening. We would be measuring the crystal's growth rate and calling it amplification.

So the background construction has to be held fixed while evaluation breadth changes.

---

## Match the Process, Not the First Frame

The first attempt controlled the wrong object.

It calibrated each allocation arm to the same expected construction at lag one, by applying an additive offset that lowered per-candidate probabilities in the broader arms until their expected attachment count matched. At lag one the calibration was excellent.

Then the crystal evolved. Different selected candidates produced different attachments, different attachments produced different morphologies, different morphologies produced different frontiers and different probability distributions. The single offset, solved once, no longer described the system it was supposed to be controlling. By lags two through twelve the construction rates had drifted apart, and the comparison was no longer between allocation regimes at matched construction.

> **A controlled initial condition is not a controlled dynamical process.**

The corrected design recalibrates continuously. A dedicated PREVENT-only reference trajectory defines the target expected construction at every lag. At each lag, every allocation arm solves a fresh offset on its own current PREVENT state so that its expected PREVENT construction matches that target.

FORCE receives the same offset and is deliberately *not* calibrated independently — normalizing FORCE to a target would erase the causal response we are trying to measure. PREVENT defines the background policy; FORCE inherits it and remains free to differ.

Dynamic calibration creates the comparison we actually need:

```text
similar background expected construction
+
different evaluation breadth

```text
f = 0.10     offset  0.00  (reference, by definition)
f = 0.25            −1.59
f = 0.50            −2.49
f = 0.75            −2.96
f = 1.00            −3.28
unbounded           −3.28
```

The required calibration also changes through time.

> **Controlling a dynamical process requires controlling the trajectory, not merely matching its starting point.**

The fresh-seed experiment passed its frozen validity gate: the dynamically recalibrated PREVENT trajectories remained within the required tolerance of the reference construction process across allocation arms and lags.

Only after that gate passed was the amplification comparison interpretable.
 The comparison really is between allocation regimes at matched background construction.

---

## The Mean Barely Moves

The primary contrast is strong subsampling against true exhaustive evaluation, with the outcome being cumulative FORCE-minus-PREVENT construction over twelve updates.

```text
f = 0.10     0.1497
unbounded    0.1484

difference   +0.00130
95% CI       [−0.08984, +0.08854]
achieved MDE  0.11536
```

The predeclared scientifically meaningful effect was ±0.15 attachments, and the entire confidence interval lies inside it.

```text
BOUNDED NEAR ZERO
```

The language here has to be exact, because two easier statements are both wrong. This is stronger than "not statistically significant" — an underpowered experiment produces that phrase without licensing any conclusion, and Chapter 10 spent several paragraphs on why. It is weaker than "the two regimes are equivalent" — the interval is not tight enough to rule out effects smaller than the declared scale. At a ±0.10 threshold this same result would have been **unresolved**. It resolves the question it declared, at the scale it declared.

> **At dynamically matched background construction, strong candidate subsampling did not change mean twelve-step causal consequence relative to true exhaustive evaluation by the predeclared ±0.15 attachment scale.**

The immediate local effect barely moves either. Ring-one expected effects run from 0.11305 at the strongest subsampling to 0.10824 unbounded — a difference of about +0.005, interval spanning zero.

So the non-local redistribution discovered in the first half does not become a scientifically meaningful change in mean twelve-step causal consequence at the declared `±0.15` scale.

---

## But the Pathway Rotates

The wrong summary is:

```text
nothing changed

For a single-contact probe, `x` has one occupied neighbour and five empty ones. Some of those empty neighbours are not frontier candidates at all until `x` is occupied — when FORCE places a cell there, they become eligible for the first time. Others were already frontier candidates in both branches, and simply have their probabilities shifted by the new occupied neighbour.

So the immediate effect arrives through two distinct channels: **promotion**, where the intervention creates candidates that exist only in FORCE, and **shared shift**, where it changes probabilities on candidates evaluated in both branches. Conditioning on probes where the intervention survived:

```text
             promotion    shared shift    total

f = 0.10       0.0694        0.0542       0.1237
f = 0.25       0.0433        0.0761       0.1188
f = 0.50       0.0361        0.0798       0.1157
f = 0.75       0.0337        0.0840       0.1177
f = 1.00       0.0330        0.0853       0.1183
unbounded      0.0332        0.0853       0.1184
```

The promotion channel halves as evaluation broadens. The shared-shift channel rises by more than half. The total stays nearly flat.

That is the finding hiding under the flat mean. Under strong subsampling, an intervention matters largely because it puts a *new* opportunity in front of the selector. Under broad evaluation, it matters largely because it changes the *probability* of opportunities that were going to be evaluated anyway. Those are different computational routes to the same aggregate effect, and their weights move in opposite directions with almost exactly compensating magnitudes.

```text
SAME MEAN CONSEQUENCE
≠
SAME CAUSAL PATHWAY
```

An experiment measuring only the aggregate mean would miss that evaluation breadth changes how the immediate effect is expressed.

The mean is stable while the mixture of causal pathways changes.

---

## Some Perturbations Are Never Expressed

There is one more thing finite selection controls, and it explains a feature of the data that looked at first like noise.

A delivered perturbation has to clear two filters before it can produce any immediate causal difference at all.

First, it has to survive. The intervention step applies the ordinary background loss rule, and if `x` is removed, FORCE and PREVENT collapse to the same state and the effect is structurally zero. The realized survival fraction was 0.9141 against an expected 0.92 — so roughly eight or nine percent of probes are not weak responses. They are annihilated interventions.

Second, the selector has to evaluate something the intervention affected. With `k` affected candidates, frontier size `F` and budget `B`, sampling without replacement gives:

$$
P(\text{any affected candidate selected}) = 1 - \frac{\binom{F-k}{B}}{\binom{F}{B}}
$$

Multiply by survival and you have a parameter-free prediction of how often an immediate causal difference can be expressed at all:

```text
arm         predicted    observed
f = 0.10      0.363        0.401
f = 0.25      0.679        0.698
f = 0.50      0.876        0.880
f = 0.75      0.914        0.913
f = 1.00      0.918        0.910
unbounded     0.918        0.910
```

Close everywhere, and within about a percentage point from `f = 0.50` upward.

So at the strongest subsampling, roughly sixty percent of probes show essentially zero immediate effect — not because the causal system is noisy, but because the selector never looked at anything the intervention touched. And 83% of probes produce no realized twelve-step difference whatsoever. The zero inflation is a property of the computational regime, predictable in advance from combinatorics.

That gives a hierarchy the substrate produced on its own:

```text
PERTURBATION DELIVERED
≠  PERTURBATION SURVIVES
≠  CAUSAL DIFFERENCE EXPRESSED
≠  DOWNSTREAM CONSEQUENCE REALIZED
```

Finite selection therefore controls whether an available causal difference receives a computational opportunity to become expressed.

That is distinct from controlling the eventual mean magnitude of the perturbation's downstream consequence.

---

## Routing Is Not Amplification

Put the halves together and the chapter's result is sharper than either alone.

Finite computational selection changes:

```text
where causal opportunity is spent      (far-field redistribution)
which route the effect travels         (promotion vs shared shift)
whether the effect appears at all      (expressibility gating)
```

while the matched experiment bounds any change in:

mean twelve-step downstream causal consequence

to within the predeclared ±0.15 attachment scale

```text
CAUSAL ROUTING
≠
CAUSAL AMPLIFICATION
```

This is a better answer than the one we went looking for. An amplification result would have been exciting and, on reflection, slightly suspicious — a mechanism that made perturbations grow simply by rationing computation would have been the sort of free lunch this book has learned to distrust. What the substrate gave instead is a redistribution mechanism: causal opportunity is expressed in different places and through different pathways, while the matched experiment resolves no scientifically meaningful change in the mean twelve-step consequence at its declared scale.

One methodological note before leaving it. The `f = 1.00` arm and the unbounded arm are not the same policy, despite the fraction suggesting they should be. A budget set to the size of the PREVENT frontier is still a fixed count handed to both branches, so FORCE — which may have a larger frontier — still competes for slots. The unbounded arm instead lets each branch evaluate its own entire frontier. Finite arms conserve evaluation *count*; the unbounded arm conserves *coverage*. A numerical parameter value is not the same thing as a computational policy.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Partial evaluation produces outside-cone expected construction differences | **SUPPORTED** | signed far-field effects across the fraction sweep, both classes |
| Exhaustive evaluation gives exactly zero outside-cone effect | **ASSERTION** | correctness identity; checked 10,750 times, not empirical evidence |
| The outside-cone effect is produced by finite candidate selection | **SUPPORTED** | effect present under subsampling, absent exactly without it |
| Fixed-budget selection conserves evaluation slots | **IDENTITY** | Δ(far) = −Δ(near) by construction of fixed-size selection |
| Low-budget far-field effect tracks −ΔF × f | **SUPPORTED** | residuals 12.6% / 9.9% / 2.6% against 25% criterion |
| The fitted coefficient behaves like far-frontier probability payload | **CONSISTENT** | β/f ≈ 0.50–0.57; far probability mass not independently measured |
| Candidate displacement determines construction displacement | **FAILED** | similar churn (0.483 vs 0.446), opposite effects (−0.013 vs +0.213) |
| The extreme classes follow a parameter-free −2:1 ratio | **UNRESOLVED** | sweep gives −4.15 / −3.54 / −2.21; actual ΔF ratio ≈ 2.36 |
| Lag-one background matching controls the continuing process | **INVALID DESIGN** | construction rates drifted by lags 2–12; superseded |
| Dynamic per-lag matching controls background construction | **SUPPORTED** | record-level pass fraction 1.0; all arm means within ±2% |
| Strong subsampling changes mean 12-step causal consequence | **BOUNDED NEAR ZERO** | difference `+0.00130`, CI inside ±0.15; unresolved at ±0.10 |
| Evaluation breadth changes the causal pathway mixture | **SUPPORTED** | promotion 0.069→0.033, shared shift 0.054→0.085 |
| Causal expression is gated by survival and selector exposure | **SUPPORTED** | combinatorial prediction matches observed active fractions |
| Nonzero outcomes are more frequent under strong subsampling | **DESCRIPTIVE** | post-treatment conditional analysis, not promoted |
| Branching process, criticality, propagation, signalling | **NOT CLAIMED** | no such structure tested |

Scope for everything above: single-contact frontier sites, lag-one selection, this substrate, these budgets.

---

## The Past Is the Next Missing Variable

We now know a fair amount about what determines the fate of a local perturbation in this substrate.

The local rule predicts the immediate effect, and Chapter 10 found the measured effect consistent with that mechanical prediction.
 The local geometry determines how much opportunity it creates or consumes. The finite selector changes where evaluation opportunity is spent, which causal pathway contributes to the response, and whether affected opportunities are evaluated at all.

Yet under the matched Chapter 11 experiment, those changes do not produce a resolved difference in mean twelve-step consequence at the declared `±0.15` scale.

Every one of those variables is a fact about the present. The current occupancy, the current frontier, the current budget.

Which leaves an obvious gap. Two states can be matched on visible geometry and current computational conditions while differing in the material history that produced them.
 Chapter 6 built material that could carry such a difference and found it went causally inert once construction moved past it. Chapter 10 tried to use recent process history as a predictor and could not, in a substrate that had no independent history state to carry anything.

So the experiment has never actually been run. So the next experiment holds the present geometry, allocation policy and perturbation fixed as tightly as possible and varies the retained material consequence of prior experience.

For the first time, history itself becomes the intervention variable.

> **Can the past redirect the future even when the visible present is held fixed?**
