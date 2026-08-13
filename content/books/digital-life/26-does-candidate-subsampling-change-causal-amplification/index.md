+++
title = "26: How Does Finite Selection Route Causality?"
date = "2026-08-13T15:46:00+01:00"
draft = false
description = "Chapter 26 tests how finite candidate selection changes the computational pathway of a local causal perturbation, while dynamically matching expected background construction."
weight = 26
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Finite Computation", "Experimental Method", "Cellular Automata"]
series = ["Digital Life From First Principles"]
+++

Chapter 25 established a non-local effect in a system whose transition rule was local.

A perturbation at one frontier site changed which distant candidates received evaluation slots.

When candidate subsampling disappeared, the far-field effect disappeared with it.

The mechanism was:

```text
LOCAL FRONTIER CHANGE
↓
FINITE EVALUATION SLOTS
↓
CANDIDATE SUBSTITUTION
↓
FAR-FIELD REDISTRIBUTION
```

That result answered one question.

It created another.

If finite selection changes **where** causal opportunity is expressed, does it also change **how much** causal consequence accumulates?

Or does it merely route the same perturbation through different computational pathways?

That distinction became Chapter 26.

And the eventual answer was more interesting than either alternative alone.

---

# Redistribution Is Not Amplification

The obvious experiment would have been to vary the evaluation budget.

But that experiment would have been confounded immediately.

A larger budget evaluates more candidates.

More evaluated candidates produce more expected attachments.

More attachments can create more downstream attachments.

So an apparent increase in causal amplification could reduce to:

```text
MORE COMPUTATION
↓
MORE CONSTRUCTION
```

rather than:

```text
DIFFERENT ALLOCATION
↓
DIFFERENT CAUSAL AMPLIFICATION
```

Chapter 26 therefore had to control construction quantity while changing allocation structure.

The primary scientific question became:

> **At matched expected background construction rate, does strong candidate subsampling produce a larger finite downstream causal consequence than true exhaustive evaluation?**

The stronger mechanistic question emerged only later:

> **If the downstream consequence does not change much, does finite selection nevertheless change the pathway through which the immediate causal effect is realized?**

---

# The Perturbation

As in the previous chapters, we started from the same checkpoint and the same frontier probe `x`.

Two branches were created:

```text
FORCE
x is occupied

PREVENT
x remains empty
```

Both branches used:

```text
same checkpoint
same probe
same future environment
same cell-keyed randomness
```

The intervention was transient.

After one continuation update, `x` was removed from FORCE if it remained occupied.

The finite-horizon outcome was:

```text
G_T(H)
```

with:

```text
H = 12
```

where `G_T` is the cumulative FORCE-minus-PREVENT realized construction difference within the chosen local horizon.

This is not a formal branching ratio.

It can contain overlapping pathways, substitutions, descendants of descendants, and branch-specific frontier changes.

So Chapter 26 calls it:

> **finite-horizon causal amplification**

and nothing stronger.

No criticality claim follows from it.

---

# The Allocation Arms

The continuation compared:

```text
f = 0.10
f = 0.25
f = 0.50
f = 0.75
f = 1.00
unbounded
```

where `f` controls the fraction of the PREVENT frontier used to determine the finite evaluation budget.

The true unbounded arm is different.

It evaluates the complete current frontier of each branch.

That distinction turned out to matter.

But before we could interpret any amplification result, we first had to solve a harder control problem.

---

# V1 — We Matched a State, Not a Process

The first version of the experiment calibrated each allocation arm to the same expected construction rate at lag 1.

The natural reference policy was:

```text
f = 0.10
offset = 0
```

For broader evaluation arms, an additive score offset lowered individual attachment probabilities until the PREVENT branch matched the same expected attachment count.

At lag 1, the calibration worked extremely well.

It looked as if we had separated:

```text
HOW MANY CANDIDATES ARE EVALUATED
```

from:

```text
HOW MUCH CONSTRUCTION IS EXPECTED
```

But the offset was solved once.

Then the crystal evolved.

Different selected candidates produced different attachments.

Different attachments produced different morphologies.

Different morphologies produced different frontiers and different probability distributions.

The single calibration no longer represented the changing process.

The V1 audit showed exactly that.

```text
LAG 1
matched expected construction

↓

LAGS 2–12
construction rates drift apart
```

The lesson was simple:

> **A controlled initial condition is not a controlled dynamical process.**

V1 remained part of the scientific record.

But it was not the experiment we intended.

So we built V2.

---

# V2 — Match the Trajectory

V2 recalibrated the background process at every continuation lag.

A dedicated PREVENT-only reference trajectory used the natural:

```text
f = 0.10
offset = 0
```

policy.

At each lag `τ`, that trajectory defined:

```text
C_target(τ)
```

the expected background construction target.

Then every allocation arm solved a fresh offset on its own current PREVENT state:

```text
FOR EACH LAG τ
↓
reference PREVENT defines C_target(τ)
↓
arm PREVENT state chooses its candidate set
↓
solve offset so:
E[attachments_PREVENT] = C_target(τ)
↓
apply SAME offset to FORCE
↓
execute both branches
```

FORCE was deliberately **not** calibrated independently.

That would have normalized away part of the causal response.

Instead:

```text
PREVENT
defines background policy

FORCE
receives the same policy
and remains free to differ causally
```

This gave us the control we actually wanted.

---

# The Calibration Itself Became Part of the Experiment

The manipulation was not merely:

```text
same rule
different allocation
```

That description is too loose.

Expected construction was held constant by trading:

```text
FEW EVALUATED OPPORTUNITIES
with relatively high per-candidate probability

against

MANY EVALUATED OPPORTUNITIES
with much lower per-candidate probability
```

The broader the evaluation policy, the more negative the calibration offset had to become.

Across the V2 trajectory, the approximate mean offsets were:

```text
f=.10        0.000
f=.25       -1.59
f=.50       -2.49
f=.75       -2.96
f=1.00      -3.28
unbounded   -3.28
```

The reference `f=.10` offset is zero by definition.

That is not a measurement.

It is an assertion about the reference policy.

The broader-arm offsets are measurements of how strongly the native attachment rule had to be suppressed to preserve the same PREVENT construction expectation.

The offset also moved over time.

For the broadest arms it became less negative as the trajectory evolved.

That is another reminder that:

> **Controlling a process requires a moving control when the state itself moves.**

---

# The Validity Gate Passed

The full V2 run used:

```text
192 independent groups
768 probes
4 probes per group
12 continuation lags
6 allocation arms
```

with fresh seed:

```text
20260913
```

The supported probe regime remained:

```text
occupied_neighbors = 1
```

The dynamic matching validity gate required:

```text
>= 95% of group × probe × arm × lag records
within 2% of target
```

and:

```text
every population-level arm × lag mean
within ±2%
```

Both gates passed.

The record-level pass fraction was:

```text
1.0
```

and cross-arm PREVENT expected-construction dispersion was effectively numerical zero.

So V2 really did compare different allocation regimes under dynamically matched background construction.

---

# The Frozen Amplification Test

The primary contrast was:

```text
G_T(f=.10)
-
G_T(unbounded)
```

Strong candidate subsampling versus true exhaustive evaluation.

The predeclared smallest scientifically meaningful effect was:

```text
±0.15 attachments
```

The result was:

```text
mean difference
+0.00130

95% CI
[-0.08984, +0.08854]

achieved MDE80
0.11536
```

The complete confidence interval lies inside:

```text
[-0.15, +0.15]
```

So the result is:

```text
BOUNDED_NEAR_ZERO
```

at the frozen effect scale.

This is stronger than a nonsignificant result.

It is also narrower than saying the two regimes are equivalent.

The experiment resolves the predeclared:

```text
±0.15
```

scale.

It would have been:

```text
UNRESOLVED
```

under a:

```text
±0.10
```

smallest-effect threshold.

That precision boundary matters.

The scientifically bounded sentence is:

> **At dynamically matched PREVENT background construction rate, strong candidate subsampling did not produce a mean twelve-step causal consequence differing from true exhaustive evaluation by the predeclared ±0.15 attachment scale.**

---

# The Same Mean Outcome Does Not Mean the Same Computation

The primary arm means were:

```text
f=.10       0.1497
unbounded   0.1484
```

Almost identical.

But the mechanism audit showed that these similar outcomes were **not** produced in the same way.

To understand why, we had to look inside the immediate ring-one causal effect.

---

# First Filter: Did the Perturbation Survive?

The FORCE intervention can disappear before the continuation even begins.

The intervention-step background loss rate is:

```text
δ = 0.08
```

If `x` is removed by that loss draw, FORCE and PREVENT collapse back to the same occupancy state.

Then:

```text
FORCE = PREVENT
↓
E1 = 0
G_T = 0
```

structurally.

The realized survival fraction was:

```text
0.9141
```

against the expected:

```text
0.92
```

So roughly eight to nine percent of recruited probes were not weak causal responses.

The perturbation itself had been annihilated.

That is the first source of structural zero inflation.

---

# Second Filter: Did the Selector Expose the Difference?

Even when `x` survives, a finite selector may fail to evaluate any ring-one opportunity affected by the intervention.

For an affected frontier set of size `k`, frontier size `F`, and finite budget `B`, the without-replacement protocol expectation is:

```text
P(any affected candidate selected)
=
1 - C(F-k, B) / C(F, B)
```

So the probability that an immediate ring-one causal effect can be expressed is approximately:

```text
P(E1 active)
=
P(x survives)
×
P(any affected ring-1 candidate selected)
```

No fitted parameter is required.

The prediction matched the observed active-`E1` fraction closely:

```text
arm        predicted    observed

f=.10       0.363        0.401
f=.25       0.679        0.698
f=.50       0.876        0.880
f=.75       0.914        0.913
f=1.00      0.918        0.910
unbounded   0.918        0.910
```

The largest discrepancy was under the strongest subsampling arm.

By `f=.50` and above, prediction and observation were within about one percentage point.

This explains something that originally looked like an estimator problem.

At `f=.10`:

```text
~60% of probes
have effectively zero E1
```

not because the causal system is simply noisy, but because the protocol often prevents the causal difference from becoming expressible.

That gives us a new hierarchy:

```text
PERTURBATION DELIVERED
≠
PERTURBATION SURVIVES
≠
IMMEDIATE CAUSAL DIFFERENCE EXPRESSED
≠
DOWNSTREAM CONSEQUENCE REALIZED
```

The primary `f=.10` arm had:

```text
E1 ≈ 0 for ~59.9% of probes

G_T = 0 for ~83.1% of probes
```

So most delivered perturbations did not produce a realized twelve-step construction difference.

---

# Why the Immediate Mean Stayed Nearly Flat

Before the mechanism audit, the arm-level ring-one means looked almost invariant:

```text
f=.10        0.11305
f=.25        0.10860
f=.50        0.10573
f=.75        0.10757
f=1.00       0.10810
unbounded    0.10824
```

It was tempting to say that dynamic construction matching mathematically pinned the immediate causal input.

That was wrong.

We tested that hypothesis.

The simple probe-level law failed.

The apparent stability came from something more interesting.

There were **two causal channels** whose relative weights changed in opposite directions.

---

# Two Ways the Same Local Intervention Can Matter

For an `n=1` frontier probe, `x` has one occupied neighbour and five empty neighbours.

Some of those empty neighbours are not frontier cells before FORCE occupies `x`.

When `x` is present, they become new frontier candidates.

Those contribute through a:

```text
FORCE-ONLY / PROMOTION CHANNEL
```

Other empty neighbours were already frontier cells in PREVENT.

When `x` becomes occupied, their local neighbourhood changes.

Those contribute through a:

```text
SHARED PROBABILITY-SHIFT CHANNEL
```

The exact ring-one accounting is:

```text
E1_ring1
=
FORCE-only contribution
+
PREVENT-only selector contribution
+
shared probability-shift contribution
```

The equality itself is a code-level accounting identity.

We asserted it across:

```text
4,608 probe × arm rows
```

to floating tolerance.

The scientific result is not that the sum equals itself.

The scientific result is how the channel weights change.

---

# The Causal Pathway Rotates with Evaluation Breadth

Conditioning on the 702 probes where `x` survived, the mean contributions were:

```text
           FORCE-only      shared shift      total E1

f=.10        0.0694           0.0542           0.1237
f=.25        0.0433           0.0761           0.1188
f=.50        0.0361           0.0798           0.1157
f=.75        0.0337           0.0840           0.1177
f=1.00       0.0330           0.0853           0.1183
unbounded    0.0332           0.0853           0.1184
```

That is the mechanism Chapter 26 was missing.

As evaluation becomes broader:

```text
FORCE-ONLY / PROMOTION CONTRIBUTION
falls

while

SHARED PROBABILITY-SHIFT CONTRIBUTION
rises
```

The two compensate.

The total immediate causal input stays near the same arm-level scale even though the computational route changes substantially.

So the correct conclusion is not:

```text
allocation does not change E1
```

and not:

```text
construction matching algebraically fixes E1
```

It is:

> **Changing evaluation breadth reroutes the immediate causal effect between selector-mediated promotion and probability modification of already-shared opportunities. Those pathways compensate strongly enough that the arm-level mean ring-one effect remains nearly stable.**

That is a genuine mechanistic finding.

---

# Strong Subsampling Makes Selection Matter More

A compressed two-term model reinforces the same picture.

Conditioned on intervention survival, the fitted promotion proxy declines systematically as evaluation broadens, while the shared-shift proxy rises:

```text
arm        promotion proxy    shared proxy

f=.10          0.580             0.379
f=.25          0.224             0.565
f=.50          0.121             0.608
f=.75          0.038             0.669
f=1.00         0.015             0.686
unbounded      0.017             0.686
```

These coefficients are descriptive.

They are not literal attachment probabilities.

The exact selected-set decomposition is the mechanistic object.

But the progression is clear:

```text
STRONG SUBSAMPLING
↓
which opportunities receive evaluation
carries more of the causal effect

BROAD EVALUATION
↓
probability changes on already-shared opportunities
carry more of the causal effect
```

The same intervention can matter because:

```text
a new opportunity receives computation
```

or because:

```text
an existing opportunity becomes more likely to construct
```

Finite selection changes the mixture.

---

# Redistribution Still Exists

None of this removes the Chapter 25 result.

Under strong subsampling:

```text
E1_far(f=.10)
≈ -0.0387
```

True unbounded evaluation has:

```text
E1_far = 0
```

by construction.

That zero is not an empirical finding.

When every far frontier candidate is evaluated in both branches and their far probabilities are identical, the expected selector-mediated far difference must be zero.

So:

```text
unbounded E1_far = 0
```

is a correctness assertion.

The experiment's scientific evidence comes from the contrast:

```text
finite selection
→ nonzero selector-mediated far redistribution

true exhaustive evaluation
→ selector pathway absent
```

The non-local allocation effect remains real.

---

# But Redistribution Did Not Become Additional Mean Amplification

Now we can interpret the frozen primary result more precisely.

Finite selection changed:

```text
where evaluation slots were spent
how the ring-one effect was divided between causal channels
whether the immediate effect became expressible
```

Yet the mean twelve-step causal consequence remained bounded near the exhaustive result at the predeclared scale.

A post-hoc analysis asked whether residual differences in immediate causal input could be masking an allocation effect.

At group level:

```text
ΔG
=
α
+
β ΔE1
```

gave:

```text
α ≈ -0.0063

95% bootstrap CI
[-0.0944, +0.0794]
```

This does not replace the frozen primary test.

It is interpretive evidence.

And it points in the same direction.

So the stronger distinction is now:

# **CAUSAL REDISTRIBUTION ≠ ADDITIONAL DOWNSTREAM AMPLIFICATION**

Finite selection can reroute causal influence without producing a scientifically meaningful additional mean downstream consequence at the tested scale.

---

# `f=1.00` and Unbounded Mean Different Things

In V2:

```text
B = |PREVENT frontier|
```

for the `f=1.00` arm at each lag.

So PREVENT is exhaustively evaluated.

But that same evaluation count is handed to FORCE.

If FORCE has a larger frontier, some FORCE opportunities still compete for a finite number of slots.

Thus `f=1.00` is not stale-budget V1 behaviour.

It is a different resource-allocation convention.

Finite arms conserve approximately:

```text
EVALUATION COUNT ACROSS BRANCHES
```

True unbounded evaluation instead conserves:

```text
COVERAGE
```

because each branch evaluates its own entire frontier:

```text
B_PREVENT = F_PREVENT
B_FORCE   = F_FORCE
```

That distinction appears directly in FORCE expected construction.

At lag 1:

```text
FORCE expected surplus over target

f=.10        +0.041
f=.25        +0.045
f=.50        +0.048
f=.75        +0.049
f=1.00       +0.036
unbounded    +0.093
```

The unbounded arm lets FORCE evaluate all of the extra opportunities created by the perturbation.

Finite arms hold the evaluation count to the PREVENT-defined budget.

So the `f=1.00` versus unbounded difference is best understood as a methodological contrast between two resource-allocation semantics:

```text
FINITE POLICY
matches evaluation count

UNBOUNDED POLICY
matches evaluation coverage
```

---

# What Happened to Common Random Numbers?

Every arm used the same keyed random numbers.

But pairing only reduces variance if the two arms tend to put the same cells on the same side of their probability thresholds.

The calibration offsets differ greatly.

So the same random uniforms are being compared against very different probabilities.

The group-level correlations with unbounded `G_T` were approximately:

```text
f=.10       0.13
f=.25       0.05
f=.50       0.12
f=.75       0.44
f=1.00      0.82
```

The closer the allocation/calibration policy gets to unbounded, the stronger the pairing becomes.

That explains why the primary contrast did not receive the dramatic variance reduction we might have expected from common random numbers.

Again, this does not invalidate the result.

It defines its precision.

The experiment resolved:

```text
±0.15
```

not:

```text
±0.10
```

---

# What Finite Selection Actually Controls

The picture is now more specific than the original Chapter 26 question.

Finite selection controls at least three things.

First:

```text
SPATIAL ALLOCATION
```

It creates outside-cone redistribution by making distant candidates compete for finite evaluation slots.

Second:

```text
CAUSAL PATHWAY
```

Under strong subsampling, selector-mediated promotion carries a larger share of the immediate local effect.

Under broad evaluation, shared-neighbour probability shifts carry more.

Third:

```text
CAUSAL EXPRESSIBILITY
```

A perturbation must survive loss and gain access to an affected evaluated opportunity before an immediate causal difference can appear at all.

What finite selection did **not** do, at the frozen resolution, was create a large additional mean twelve-step causal consequence.

That gives us a much better substrate statement:

> **Finite computational selection changes where causal influence is expressed, how that influence is routed through local computational pathways, and how often it becomes immediately expressible. Under dynamically matched background construction, those changes did not produce an additional mean twelve-step causal consequence of ±0.15 attachments or greater relative to true exhaustive evaluation.**

---

# Chapter 26 Status

```text
CHAPTER 26
STATUS: COMPLETE
```

Primary frozen result:

```text
BOUNDED_NEAR_ZERO
at ±0.15 attachments
```

Best bounded claim:

> **At dynamically matched PREVENT background construction rate, strong candidate subsampling did not produce a mean twelve-step causal consequence differing from true exhaustive evaluation by the predeclared ±0.15 attachment scale.**

Mechanistic finding:

> **Evaluation breadth changes the mixture of immediate causal pathways: strong subsampling increases the FORCE-only promotion contribution, while broader evaluation shifts causal weight toward probability changes on already-shared opportunities. The two pathways compensate strongly at the arm-average level.**

Protocol-level zero-inflation result:

> **Immediate causal expression is gated first by intervention survival and then by whether finite selection exposes an affected ring-one opportunity.**

Measured:

> **Finite candidate subsampling continues to produce selector-mediated far-field redistribution.**

Structural assertions:

```text
ring-one channel accounting sums exactly to E1
unbounded E1_far = 0
reference f=.10 offset = 0
```

Not established:

```text
formal branching process
criticality
subcriticality
supercriticality
phase transition
self-sustaining propagation
coherent structure
individuality
organism
life
```

No V3.

No further Chapter 26 audit.

---

# What Survived the Hypothesis?

The original hypothesis asked whether candidate subsampling amplified causality.

At the tested scale, it did not.

But the experiment revealed more than a null.

```text
FINITE SELECTION
↓
changes which opportunities receive computation
↓
changes whether the perturbation becomes expressible
↓
changes the mixture of local causal pathways
↓
creates non-local redistribution

BUT

does not produce additional mean
12-step causal consequence
above the frozen ±0.15 scale
```

That gives us a clearer distinction than the chapter began with:

```text
CAUSAL ROUTING
≠
CAUSAL AMPLIFICATION
```

And another:

```text
PERTURBATION DELIVERED
≠
PERTURBATION SURVIVES
≠
CAUSAL DIFFERENCE EXPRESSED
≠
DOWNSTREAM CONSEQUENCE REALIZED
```

Those are not biological categories imported into the model.

They came from the computational substrate itself.

---

# The Next Missing Ingredient Is History

Chapter 18 showed that persistent material state can alter later construction while it remains causally accessible.

Chapter 19 showed that different experiences can leave distinguishable persistent organization without establishing a meaningful common-challenge response.

Chapter 24 briefly attempted to use recent process history, but the tested substrate had no independent material-history state.

Now we can build the missing experiment deliberately.

The next chapter should hold constant:

```text
present occupancy geometry
occupied-neighbour count
promoted-neighbour count
shared-neighbour count
allocation policy
background construction rate
perturbation
```

while changing:

```text
PERSISTENT MATERIAL STATE
```

And the perturbation should survive its intended causal exposure **by design**, rather than recruiting probes and later discarding the roughly eight percent whose intervention is annihilated by loss.

Then the question becomes:

> **Can two states with the same visible geometry route the same perturbation differently because their material histories differ?**

That would be genuinely new.

Not history inferred from geometry.

Not a variable named `memory`.

A separate persistent state channel whose causal consequence can be measured.

If history changes the promotion channel, the shared probability-shift channel, the total immediate effect, or the downstream consequence under matched present geometry, then the past has become causally active.

If it does not, stored state remains storage without demonstrated use.

That is Chapter 27.

---

# Where We Are Now

The path from Chapters 24 through 26 has become unexpectedly coherent.

```text
CHAPTER 24
A local intervention can alter distant expected construction
through a finite selector.

↓

CHAPTER 25
The effect scales with finite allocation
and vanishes when subsampling disappears.

↓

CHAPTER 26
Finite selection changes:
- spatial redistribution
- causal expressibility
- causal pathway mixture

but not additional mean downstream
causal consequence above ±0.15
under dynamically matched construction.
```

We started by asking whether finite computation could make a perturbation grow.

Instead we learned how finite computation **routes** a perturbation.

That is a better answer.

And it gives us a clean next experiment:

> **What changes when the material itself can remember?**
