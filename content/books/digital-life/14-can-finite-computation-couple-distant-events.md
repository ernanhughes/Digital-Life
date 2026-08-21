+++
title = "14: Can Finite Computation Couple Distant Events?"
date = "2026-08-14T22:00:00+01:00"
draft = false
description = "A local attachment changes expected construction in places the local rule cannot reach in one step — because distant opportunities compete for the same evaluation slots. But routing causality is not the same as amplifying it."
weight = 14
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Finite Computation", "Causality", "Experimental Method"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "review"
+++

The last chapter ended with a causal difference it could measure but could not explain.

Under the corrected intervention, cumulative construction outside the measured local region was lower in both FORCE-derived branches than in PREVENT.

```text
RETAINED far-field difference
−0.318    [−0.583, −0.068]

TRANSIENT far-field difference
−0.177    [−0.362, −0.029]
```

Both intervals lie below zero.

So the far-field difference is no longer merely a suggestive discrepancy. It is established under that finite-budget protocol.

What the previous chapter did **not** establish was the mechanism.

That is the question here.

There was one obvious candidate already present in the substrate: the finite evaluation budget shared by active frontier sites.

*What Does It Cost to Stay?* introduced a fixed number of evaluation opportunities per update.

The previous chapter then showed that one attachment can transform immediate frontier opportunity very differently depending on local geometry.

At the sparse end, forcing the attachment promoted about 2.21 previously unsupported sites into the frontier, for a net frontier change of about +1.21.

At the dense end, it promoted none and removed the focal candidate from the frontier, for a net change of −1.

Change the candidate population and you change what competes for a fixed evaluation pool.

That creates a possible causal pathway that does not run through the local attachment rule at all:

> **Does competition for a shared finite evaluation budget create measurable causal effects outside the one-step reach of the local rule?**

---

## Too Far Away to Matter

The attachment rule reaches nearest neighbours and no further. That is structural, not statistical — it is what the rule says.

So at lag one, define:

```text
LOCAL-RULE ONE-STEP CONE     d ≤ 1
OUTSIDE LOCAL-RULE CONE      d > 1
```

A FORCE/PREVENT intervention at `x` cannot alter a candidate's local-rule attachment probability at `d > 1` in one update through the nearest-neighbour occupancy rule.

There is no one-step neighbourhood path from `x` to those sites.

That makes the region outside the local-rule cone unusually useful.

If FORCE and PREVENT differ there in **expected construction** at lag one, the difference cannot have been produced by a nearest-neighbour change in attachment probability.

Some other causal route must account for it.

The shared finite selector is the candidate mechanism to isolate.

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

For each finite arm, `f` sets a fixed evaluation count from the *larger* of the two branch frontiers — the frozen control parameter is `B / max(F_force, F_prevent)`. That same count is then supplied to both branches, and each selects from its own frontier by keyed randomness without replacement. If a branch's frontier is smaller than the count, it simply evaluates all of it.

```text
f = 0.05, 0.10, 0.25, 0.50, 0.75, 1.00
plus an explicit UNBOUNDED arm
```

`f = 1.00` is still a fixed-count policy, but taking the count from the larger frontier makes it non-binding: the budget is at least as large as either branch's candidate set, so both evaluate everything. In this implementation `f = 1.00` and `UNBOUNDED` therefore coincide, and the protocol froze both as full-evaluation controls with a hard outside-cone zero at `1e-12` tolerance.

They remain different *policies*. `f = 1.00` is a fixed count that happens not to bind; `UNBOUNDED` removes the selector. The distinction matters for what each one licenses, not for what either measured here.

The same checkpoint generates every budget condition. This is a control-parameter experiment on a single frozen state, not a comparison between differently grown crystals.

The measured quantity is the *expected* far-field construction difference, computed from the branch-specific evaluated candidate sets before any attachment draw is taken. Not a noisy realized count — the exact expectation the rule and the selector jointly imply.

One scope restriction, stated once: every probe here is a single-contact frontier site, with exactly one occupied neighbour. What follows is established in that regime. The run used 384 independent checkpoints, 5,375 supported sites, and seven budget conditions each — 37,625 site-by-budget measurements.

---

## A Difference Outside the Local Cone

Under partial evaluation, FORCE and PREVENT differ in expected construction outside the local causal cone.

For sites where the intervention creates frontier (`FCP = +2`), the far-field effect is negative, with its magnitude increasing across the tested partial-evaluation fractions from `f = 0.05` through `f = 0.75`:

```text
f           E_far
0.05        −0.049
0.10        −0.110
0.25        −0.261
0.50        −0.492
0.75        −0.715
1.00         0.000
unbounded    0.000
```

For sites where the intervention consumes frontier (`FCP = −1`), it runs the other way:

```text
0.05        +0.012
0.10        +0.031
0.25        +0.118
0.50        +0.213
0.75        +0.294
1.00         0.000
unbounded    0.000
```

Both full-evaluation arms return exactly zero, at every FCP class, including the frontier-creating class where the actual lag-one frontier difference averages `+1.84`. That is not a small number that rounded down. The far-field selected sets are bit-identical between branches.

Create local frontier opportunity and expected construction falls in the outside-cone region.

Consume local frontier opportunity and expected construction rises there.

The effect appears at a distance the local rule cannot reach in one update.

The sign makes sense the moment you stop thinking about propagation and start thinking about competition. An attachment that creates additional nearby candidates adds claimants to a selector whose total number of slots is fixed.

Some candidates elsewhere therefore lose evaluation opportunity.

---

## Remove the Selector, Remove the Effect

The cleanest part of this experiment is what happens when finite candidate selection is removed entirely.

In the explicit **UNBOUNDED** arm, each branch evaluates its own complete frontier.

At lag one, sites outside the local-rule cone have unchanged local neighbourhoods and therefore unchanged attachment probabilities. With no candidate subsampling left to redistribute evaluation opportunities, the selector-mediated far-field difference is structurally zero.

Must be.

Not approximately and not on average.

This is a correctness identity of the unbounded policy, not an empirical discovery.

It is important to be honest about what that zero is. It is not a discovery. It is a correctness identity, and quoting it as evidence would be exactly the error this book has flagged repeatedly: reporting a theorem about the code as though it were a fact about the world. A quantity with exactly zero variance across thousands of independent groups belongs in an assertion, not a confidence interval.

The evidence is the contrast between computational policies:

```text
PARTIAL FIXED-COUNT EVALUATION
→ reproducible outside-local-rule-cone effect

TRUE UNBOUNDED EVALUATION
→ selector-mediated effect is structurally zero
```

The zero in the unbounded arm is an identity.

The empirical result is that partial finite selection creates the nonzero redistribution that the unbounded policy cannot.

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

This is an accounting identity imposed by fixed-size selection, not an empirical law.

And it tells us exactly what is held fixed.

Not attachments.

Not construction.

Not frontier size.

Not causal consequence.

**The number of evaluation slots.**

The far field receives the exact negative of whatever selected-slot imbalance appears nearby.

That is a computational conservation identity of this selector: the allocation count is fixed even though the material consequence carried by those slots need not be.

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
```

---

## Exactly What the Selector Moves

The two quantities can be separated exactly, because the experiment records both for every site.

At lag one, outside the local-rule cone, a candidate's neighbourhood is untouched by the intervention. So any candidate evaluated in *both* branches carries the same attachment probability in both. Across all 37,625 site-by-budget records, the shared-candidate contribution to the far-field difference is not merely small:

```text
shared-candidate contribution to E_far      exactly 0
```

Zero in every record, in every arm. That leaves only one source, and it accounts for the whole effect:

$$
E_{\text{far}} = \sum_{i \in \text{FORCE only}} p_i \;-\; \sum_{i \in \text{PREVENT only}} p_i
$$

The residual against the recorded `E_far` is zero to the last bit, across every record. The far-field effect *is* the probability payload of the candidates the selector swapped — nothing else contributes, and `E_far` is nonzero exactly when the two evaluated far sets differ.

That is the mechanism stated as an identity over measured data rather than as a fitted approximation:

```text
SELECTOR MEMBERSHIP CHANGE
×
CANDIDATE PROBABILITY PAYLOAD
=
EXPECTED FAR-FIELD CONSTRUCTION DIFFERENCE
```

It also explains the two full-evaluation arms without any appeal to magnitude. When both branches evaluate their whole frontier, no candidate is in one selected set and not the other, the swap set is empty, and the sum is zero by construction.

An aggregate summary of the same thing was frozen in advance for the low-evaluation regime `f ≤ 0.25`, predicting `E_far ≈ −ΔF × f × p̄_far` — where `ΔF` must be the *actual* lag-one frontier difference rather than the checkpoint FCP label, because ordinary background loss falls between the intervention and the selection and the selector responds to what exists when it runs. Its relative residuals were `12.6%`, `9.9%` and `2.6%` against the frozen `25%` criterion.

```text
SUPPORTED
```

That relation is a coarse-grained restatement of the exact accounting, useful for seeing how the effect scales but strictly weaker than it. One more elegant version was frozen as a target and did not survive: a parameter-free `−2:1` ratio between the extreme FCP classes came out at `−4.15`, `−3.54` and `−2.21` across the low fractions, clearing tolerance only at `f = 0.25`, with wide intervals throughout.

```text
UNRESOLVED
```

The diagnosis is the same one the exact accounting makes obvious. The ratio was computed from the checkpoint FCP labels, while the actual lag-one frontier differences were nearer `+1.84` and `−0.78`. Scalar frontier size is simply not the most proximal description available — slot payload is closer to the machinery than `ΔF`, and `ΔF` is closer than FCP.

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

And it is exactly the kind of thing the substrate-first approach was supposed to turn up. We refused to start with metabolism, energy, membranes or genomes. We introduced one honest computational scarcity in the *What Does It Cost to Stay?* chapter. Three chapters later, that computational scarcity has produced a consequence we did not have to borrow from a biological category:

> **The crystal did not need a signal to couple distant regions. It needed a shared bottleneck.**

Under a shared finite selector, spatial separation beyond the local rule's one-step reach is not sufficient for one-step causal independence.

---

## Surely This Amplifies the Perturbation

Now the temptation, and it is a strong one.

If a local perturbation can recruit consequences outside its causal reach, perhaps finite computation is how small events become large ones. Perhaps selector-mediated redistribution does more than change where the consequence appears.

Perhaps it increases the total finite-horizon consequence of the perturbation. That would be a genuinely major claim, and everything so far seems to be pointing at it.

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
```

The required offsets were:

```text
f = 0.10     offset   0.00   reference, by definition
f = 0.25             −1.59
f = 0.50             −2.49
f = 0.75             −2.96
f = 1.00             −3.28
unbounded            −3.28
```

The required calibration also changes through time.

> **Controlling a dynamical process requires controlling the trajectory, not merely matching its starting point.**

The offsets are additive on the attachment *score*, before the logistic — not on probability. The reference is a dedicated PREVENT-only `f = 0.10` trajectory carrying zero offset, and the target it defines is the exact expected attachment count at each lag.

The frozen gate required every arm and lag to match that target within a `2%` relative tolerance, with at least `95%` of records passing individually. The fresh-seed experiment cleared it on both counts: record-level pass fraction `1.0`, and every arm-by-lag population mean inside tolerance.

Only after that gate passed was the amplification comparison interpretable. The comparison really is between allocation regimes at matched background construction.

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

The language here has to be exact, because two easier statements are both wrong. This is stronger than "not statistically significant" — an underpowered experiment produces that phrase without licensing any conclusion, and the previous chapter spent several paragraphs on why. It is weaker than "the two regimes are equivalent" — the interval is not tight enough to rule out effects smaller than the declared scale. The realized interval happens to fall inside ±0.10, but that is luck rather than design: the achieved minimum detectable effect was `0.11536`, so this experiment was never equipped to resolve a predeclared ±0.10 scale. It resolves the question it declared, at the scale it declared, and no tighter.

> **At dynamically matched background construction, strong candidate subsampling did not change mean twelve-step causal consequence relative to true exhaustive evaluation by the predeclared ±0.15 attachment scale.**

The immediate local effect barely moves either. Ring-one expected effects run from 0.11305 at the strongest subsampling to 0.10824 unbounded — a difference of about +0.005, interval spanning zero.

So the non-local redistribution discovered in the first half does not become a scientifically meaningful change in mean twelve-step causal consequence at the declared `±0.15` scale.

---

## But the Pathway Rotates

The wrong summary is:

```text
nothing changed
```

That summary is wrong, and seeing why requires looking at how the immediate effect is assembled.

For a single-contact probe, `x` has one occupied neighbour and five empty ones. Some of those empty neighbours are not frontier candidates at all until `x` is occupied — when FORCE places a cell there, they become eligible for the first time. Others were already frontier candidates in both branches, and simply have their probabilities shifted by the new occupied neighbour.

So the immediate effect arrives through two distinct channels: **promotion**, where the intervention creates candidates that exist only in FORCE, and **shared shift**, where it changes probabilities on candidates evaluated in both branches. The decomposition is exact rather than fitted, and conditions on one thing only — the `702` probes whose focal occupancy survived the delivery step:

```text
             promotion    shared shift    total

f = 0.10       0.0694        0.0542       0.1237
f = 0.25       0.0433        0.0761       0.1188
f = 0.50       0.0361        0.0798       0.1157
f = 0.75       0.0337        0.0840       0.1177
f = 1.00       0.0330        0.0853       0.1183
unbounded      0.0332        0.0853       0.1184
```

Within this survival-conditioned decomposition, the promotion channel roughly halves as evaluation broadens while the shared-shift channel rises substantially. Their sum remains comparatively stable.

That is the structure hidden by the flat aggregate mean.

Because this decomposition conditions on interventions whose focal occupancy survived the delivery step — a post-treatment event — it describes **how the immediate effect is routed within that conditioned subset**. It is not the unconditional causal mean across all delivered probes, and it is not conditioned on selector exposure.

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

So under the strongest subsampling, many delivered probes produce essentially zero immediate difference because either the intervention is removed or the selector evaluates none of the opportunities it changed.

The important point is not that every zero has one cause. Survival and selector exposure are separate gates, and the prediction above multiplies them rather than attributing the zero mass to either alone. What it establishes is that a substantial part of the immediate zero mass is predicted in advance by the survival-plus-selection mechanism rather than requiring an interpretation in terms of weak causal response.

Two endpoints pull in opposite directions here, and it is worth keeping them apart. *Immediate* expression becomes much rarer under strong subsampling — `0.401` of probes against `0.910` unbounded. But the fraction of probes with a nonzero *twelve-step* cumulative difference moves the other way: `0.169` at `f = 0.10` against `0.129` unbounded, a difference of `+0.040` with interval `[0.008, 0.072]`. Fewer perturbations get expressed at all, and those that do appear less likely to be washed out over the horizon. The second half of that sentence is a description of the data, not a tested mechanism.

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
where evaluation opportunity is spent
    far-field redistribution

how the immediate effect is expressed
    promotion versus shared shift

whether an available local difference receives evaluation
    expressibility gating
```

while the dynamically matched experiment bounds any change in:

```text
mean twelve-step downstream causal consequence
```

to within the predeclared `±0.15` attachment scale.

```text
CAUSAL ROUTING
≠
CAUSAL AMPLIFICATION
```

This is a better answer than the one we went looking for. An amplification result would have been exciting and, on reflection, slightly suspicious — a mechanism that made perturbations grow simply by rationing computation would have been the sort of free lunch this book has learned to distrust. What the substrate gave instead is a redistribution mechanism: causal opportunity is expressed in different places and through different pathways, while the matched experiment resolves no scientifically meaningful change in the mean twelve-step consequence at its declared scale.

One methodological note before leaving it. The `f = 1.00` arm and the unbounded arm produced identical outside-cone zeros here, and it would be easy to conclude they are the same thing. They are not. `f = 1.00` is a fixed evaluation count that happens to be large enough not to bind; `UNBOUNDED` removes the selector from the design entirely. Finite arms conserve evaluation *count*; the unbounded arm conserves *coverage*. That the two coincide under this reference frontier is a fact about this parameterisation, not an equivalence of policies — and had the budget been referenced to the smaller frontier instead, they would not have coincided. A numerical parameter value is not the same thing as a computational policy.

---

## Experimental Note

Two frozen experiments stand behind this chapter.

**Finite-budget redistribution.** Frozen crystal, `digital-crystal-v1-frozen`, loss rate `0.08`, ordinary evaluation budget `96`. 384 independent checkpoints, 5,375 supported sites, seven allocation conditions — 37,625 site-by-budget measurements. Probe scope: single-contact frontier sites, exactly one occupied neighbour. FORCE and PREVENT are constructed at the checkpoint and the ordinary loss step is applied before selection.

```text
control parameter   B / max(F_force, F_prevent)
f                   0.05, 0.10, 0.25, 0.50, 0.75, 1.00
UNBOUNDED           each branch evaluates its own full frontier
selection           keyed randomness, without replacement

local-rule cone     d ≤ 1 from x at lag one
E_far               expected FORCE-minus-PREVENT construction over
                    branch-specific evaluated candidates at d > 1,
                    before any attachment draw
FCP                 checkpoint frontier change from occupying x
actual ΔF           realized lag-one frontier difference, post-loss
far candidate churn size of the far selected-set symmetric difference

scaling test        frozen for f ≤ 0.25, 25% relative residual criterion
extreme ratio       frozen target −2.0, 25% relative tolerance
full-evaluation     f = 1.00 and UNBOUNDED, hard zero at 1e-12
```

**Dynamically matched amplification.** Intervention budget `96`, horizon 12 updates, 192 groups, 768 probes, same checkpoint and probe across arms.

```text
reference           dedicated PREVENT-only f = 0.10 trajectory, offset 0
target              lag-specific exact expected attachments
calibration         additive offset on the attachment score, pre-logistic,
                    solved on each arm's PREVENT state every lag;
                    the same offset is applied to FORCE
validity gate       2% relative tolerance, ≥95% record pass fraction,
                    every arm-lag population mean must pass
                    achieved: pass fraction 1.0, all arms within tolerance

primary contrast    G_T(f=0.10) − G_T(unbounded), two-sided
meaningful scale    ±0.15 attachments
achieved MDE        0.11536 (one-sided, 80%)
statistical unit    group; bootstrap percentile intervals
                    paired sign-flip permutation where stated

pathway decomposition   exact, conditioned on the 702 probes whose focal
                        occupancy survived the delivery step
expressibility          P(x survives) × [1 − C(F−k,B)/C(F,B)]
```

The dynamically calibrated family is an experimental instrument, not the canonical Digital Crystal dynamics. Everything in this chapter is scoped to single-contact frontier sites, lag-one selection, this substrate and these budgets.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Partial evaluation produces outside-cone expected construction differences | **SUPPORTED** | signed far-field effects across the fraction sweep, both classes |
| True unbounded evaluation gives exactly zero selector-mediated outside-local-rule-cone effect | **ASSERTION** | correctness identity of exhaustive per-branch evaluation; `f = 1.00` coincides here because the budget is referenced to the larger frontier |
| The outside-cone effect is produced by finite candidate selection | **SUPPORTED** | effect present under subsampling, absent exactly without it |
| Fixed-budget selection conserves selected-slot count | **IDENTITY** | `Δ(selected far) = −Δ(selected near)` by construction of fixed-size selection |
| The far-field difference equals swapped-candidate probability payload exactly | **IDENTITY** | shared-candidate contribution exactly `0` in all 37,625 records; residual zero to floating-point |
| Low-budget far-field effect tracks −ΔF × f in the predeclared `f ≤ 0.25` regime | **SUPPORTED** | residuals 12.6% / 9.9% / 2.6% against the frozen 25% criterion |
| Candidate displacement determines construction displacement | **FAILED** | similar churn (0.483 vs 0.446), opposite effects (−0.013 vs +0.213) |
| The extreme classes follow a parameter-free −2:1 ratio | **UNRESOLVED** | sweep gives −4.15 / −3.54 / −2.21; actual ΔF ratio ≈ 2.36 |
| Lag-one background matching controls the continuing process | **INVALID DESIGN** | construction rates drifted by lags 2–12; superseded |
| Dynamic per-lag matching controls background construction | **SUPPORTED** | record-level pass fraction 1.0; all arm means within ±2% |
| Strong subsampling changes mean 12-step causal consequence | **BOUNDED NEAR ZERO** | difference `+0.00130`, CI inside the declared ±0.15; achieved MDE `0.11536`, so ±0.10 was never resolvable |
| Evaluation breadth changes the immediate pathway mixture among surviving interventions | **SUPPORTED** | exact decomposition over the 702 survival-conditioned probes: promotion `0.069→0.033`, shared shift `0.054→0.085` |
| Causal expression is gated by survival and selector exposure | **SUPPORTED** | combinatorial prediction matches observed active fractions |
| Nonzero twelve-step outcomes are more frequent under strong subsampling | **SUPPORTED** | secondary contrast over all probes: `0.169` at `f = 0.10` vs `0.129` unbounded, difference `+0.040`, CI `[0.008, 0.072]` |
| Branching process, criticality, propagation, signalling | **NOT CLAIMED** | no such structure tested |

Scope for everything above: single-contact frontier sites, lag-one selection, this substrate, these budgets.

---

## The Past Is the Next Missing Variable

We now know a fair amount about what determines the fate of a local perturbation in this substrate.

The local rule predicts the immediate effect, and the previous chapter found the measured effect consistent with that mechanical prediction. The local geometry determines how much opportunity it creates or consumes. The finite selector changes where evaluation opportunity is spent, which causal pathway contributes to the response, and whether affected opportunities are evaluated at all.

Yet under the matched experiment in this chapter, those changes do not produce a resolved difference in mean twelve-step consequence at the declared `±0.15` scale.

Every variable isolated so far is a property of the present:

```text
current occupancy
current frontier
current attachment probabilities
current evaluation policy
current computational budget
```

That leaves one conspicuous variable untouched.

Two states can be closely matched in their visible geometry and current computational conditions while differing in the material history that produced them.

*Can Experience Change the Material?* built a substrate capable of carrying such a difference, but its stored material state became causally inaccessible once construction moved beyond it.

The previous chapter also tested recent process history as a predictor, but in a substrate with no independent history-bearing state once the present was matched.

So the stronger experiment has not yet been performed.

Hold the visible present, allocation policy and perturbation as fixed as the protocol allows.

Vary the retained material consequence of prior experience.

For the first time, make history itself the intervention variable.

> **Can the past redirect the future even when the visible present is held fixed?**