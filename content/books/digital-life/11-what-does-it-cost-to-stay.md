+++
title = "11: What Does It Cost to Stay?"
date = "2026-08-14T16:00:00+01:00"
draft = false
description = "Limit how many construction opportunities the Digital Crystal can evaluate per update and scale becomes budget-dependent. No tested budget satisfies the frozen stationarity criterion, while normalized material turnover remains strikingly stable across the tested regimes."
weight = 11
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Scarcity", "Turnover", "Computation", "Experiments"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with an impressive number and a suspicion about it.

Under the previous chapter's exact-count experiment, roughly `0.94–0.96` reoccupation events were observed per loss event, and more than ninety-three percent of distinct lost locations returned at least once within the finite run.

Among the returns that were observed, the typical delay was only a step or two.

All of that happened through the ordinary growth rule encountering ordinary empty sites.

But those measurements came from a regime in which every eligible construction opportunity could receive an attachment evaluation.

Vacancies inside the crystal and candidates at the outer edge did not have to compete for evaluation capacity.

So one major question remained open:

> **How much of that rapid reoccupation survives when computational opportunity becomes finite?**

So this chapter removes that luxury, and it removes it in the smallest possible way.

---

## Not Everything Gets Evaluated

Instead of evaluating every eligible frontier site, the process may evaluate at most:

```text
B
```

candidate sites per update. A site that is not evaluated simply gets no attachment attempt on that step. It is not blocked, not penalized, not remembered; the opportunity passes and may return next update.

Nothing else changes. The attachment probability is what it always was. The loss rule is what it was in the previous chapter. The crystal gains no new internal state whatsoever — no energy, no fuel, no resource counter, no metabolism variable, no maintenance controller, no target size, no record of what has been neglected.

```text
many possible transitions
↓
only B may be evaluated
```

That is the whole modification, and it is worth being precise about what kind of constraint it is. `B` is not the crystal's energy. It is a bound on how much of the currently available transition structure can be processed in one update. If that later resembles the way physical resource limits constrain biological action, that is a comparison to be drawn carefully, not an identity to be assumed. The point of this chapter is that scarcity turns out to matter enormously **without** having to pretend computation is ATP.

---

## The Budget Constrains the Scale

The first result arrived before any of the interesting questions did.

Holding the loss rate fixed and sweeping the budget under neutral scheduling, the late populations were approximately:

```text
B = 64        ~381
B = 128       ~829
B = 256      ~1717
B = 512      ~3092
B = 1024     ~3513
unlimited    ~3462
```

Under this loss regime and observation window, the population reached by the process is strongly budget-dependent.

Across the binding part of the sweep, increasing the evaluation budget produces a large increase in late population.

That the curve flattens somewhere above `B = 512` is unsurprising: past some point the budget stops binding because there are not enough eligible sites to use all available evaluations. The exact ordering at the top end is not worth interpreting.

What matters is the binding end. At the tested horizon, the crystal at `B = 64` has a late population roughly one ninth that of the unlimited reference.

Whether this is an asymptotic scale difference or partly a time-rescaled growth difference is not established by this experiment.

Under the tested horizon and loss regime, the crystal at `B = 64` reaches a late population roughly one tenth that of the unlimited reference.

Finite evaluation opportunity has changed the scale of the process, not merely delayed its growth.

```text
AVAILABLE EVALUATION OPPORTUNITY
↓
PROCESS SCALE
```

This is a genuinely new kind of constraint in the book.

Previous experiments constrained which transitions were locally possible.

Here many sites remain perfectly eligible for attachment but never receive an evaluation on that update.

The new distinction is:

```text
eligible to happen
≠
given computational opportunity to happen
```

So the realized dynamics are no longer determined only by:

```text
what can happen
```

but also by:

```text
what gets computational opportunity to happen
```

Until now, every eligible site received an evaluation, so the distinction had been experimentally invisible.

---

## Scarcity Creates Allocation

Once the budget binds, eligible transitions begin to compete for evaluation opportunity.

Suppose an update presents 500 eligible sites and `B = 128`. Only 128 can be considered at all. Which 128?

Any rule answering that question becomes consequential — not because the crystal is choosing, and not because it has priorities. It has neither. But the selection has to be made somehow, and different ways of making it lead to different material futures. That is allocation in a strictly mechanical sense:

```text
FINITE COMPUTATION
↓
SELECTION AMONG POSSIBLE TRANSITIONS
↓
DIFFERENT MATERIAL FUTURES
```

So we froze a budget and varied only the order of evaluation.

---

## Three Ways to Spend the Same Budget

The three scheduling policies are deliberately simple, and deliberately blind:

```text
HIGH SUPPORT     sites with more occupied neighbours evaluated first
NEUTRAL          keyed-random ordering
LOW SUPPORT      sites with fewer occupied neighbours evaluated first
```

Each policy sees only current local geometry. None can inspect the occupancy ledger. None knows whether a site is new territory or a location that was previously occupied and lost.

But local support has two consequences at once.

Reoccupation candidates often have more occupied neighbours than outer-frontier candidates.

And occupied-neighbour count already enters the attachment rule itself.

So high-support scheduling does not merely select more reoccupation-like candidates:

```text
support
→
changes which sites receive evaluation

AND

support
→
changes the attachment probability
of those evaluated sites
```

The experiment therefore tests **support-biased allocation through local geometry**.

It does not isolate a pure causal tradeoff between reoccupation and expansion.

That stronger interpretation would require a comparison matched on local support.

---

## Same Budget, Different Futures

At a fixed loss rate of `δ = 0.08` and a fixed budget of `B = 256`, the three policies produced:

```text
                        HIGH SUPPORT   NEUTRAL   LOW SUPPORT

late population                 1923      1723          1131
reoccupation / loss            0.959     0.844         0.534
first occupations / 1000 evals   188       212           249
late net growth                +24.3     +10.0          -1.5
```

The same evaluation budget, scheduled differently through local support, produces mean late populations differing by roughly seventy percent.

The mean late net-growth statistic even changes sign across the policies.

```text
SAME COMPUTATIONAL BUDGET
≠
SAME MATERIAL FUTURE
```

That result does not depend on interpreting the schedules as reuse-versus-expansion policies.

It is already enough to establish that, under finite computation, **which eligible opportunities receive evaluation matters**.

Under high-support scheduling, reoccupation runs at roughly `0.96` events per loss.

Under low-support scheduling it falls to roughly `0.53`.

The scheduling rule does not know what reoccupation is, yet it changes it dramatically.
 Neither policy knows that anything was ever lost.

---

## But the Predicted Tradeoff Fails

The hypothesis had been more specific than *allocation matters*. It predicted a clean two-sided tradeoff: high-support scheduling should meaningfully increase reuse, **and** low-support scheduling should meaningfully increase expansion, each clearing a magnitude threshold fixed in advance.

The first arm passed comfortably.

The frozen contrast was high support minus low support:

```text
reoccupation / loss

high support - low support
≈ 0.425

required
≥ 0.150
```

The second arm used the opposite contrast:

```text
first occupations / 1000 evaluations

low support - high support
≈ 61.6

required
≥ 100
```

The observed expansion-side effect reached only about `61.6%` of the predeclared meaningful magnitude.

The first-occupation effect is statistically detectable, but it remains below the magnitude we had committed to calling scientifically meaningful.

Because the hypothesis required both arms, the full tradeoff fails.

```text
FAILED
```

We do not get to lower the threshold afterward, and we do not get to report the arm that passed as though it were the hypothesis. What survives is narrower and stronger:

```text
finite budget
→ strongly constrains scale

same budget + different scheduling
→ different material futures

high-support scheduling
→ strongly increases reoccupation
```

What fails is the tidy symmetric picture in which pushing computation toward reuse pushes it away from expansion by a comparable amount.

That asymmetry is a hint, though we did not recognize it as one until much later in the chapter.

---

## Could It Simply Stay?

The budget sweep contained a suggestive regime.

Under severe scarcity, late population change approached zero while loss, attachment and reoccupation continued.

That raised a stronger question and revived a hypothesis that had failed in the previous chapter for reasons that might no longer apply. Material loss alone did not produce a finite sustainable size, because loss manufactured the very opportunities that replaced it. But loss plus a ceiling on how many of those opportunities can be serviced is a different situation entirely. Now the replacement mechanism has a hard limit.

> **Is there a finite budget at which population becomes approximately stationary while material turnover continues?**

That is a much stronger claim than *growth becomes slow*, so it needed gates that a trivially stationary system could not pass.

A qualifying regime had to satisfy all of the following:

```text
|late normalized population slope| ≤ 0.0025

late mean population ≥ 150

mean late losses ≥ 5 per update

mean late reoccupations ≥ 2 per update

mean late first occupations ≥ 2 per update

gross turnover / population ≥ 0.05

|late net change| ≤ 3 cells per update

maximum capacity fraction < 0.75
```

Freezing on death does not count. Freezing against the wall of the world does not count. We wanted approximately stationary population together with continuing material turnover.

The candidate budgets were frozen before the run:

```text
B = 48, 64, 80, 96, 128
```

with no possibility of adding another afterwards.

---

## Almost

Nearly every gate passed at every budget. Populations survived. Capacity was nowhere near binding. Loss, reoccupation and first occupation all continued. Gross turnover stayed substantial. Late net growth was small at every budget in the family.

One gate failed. The late normalized population slopes were:

```text
B = 48     -0.00319
B = 64     -0.00271
B = 80     -0.00252
B = 96     -0.00268
B = 128    -0.00280
```

against a frozen requirement of `|slope| ≤ 0.00250`.

At `B = 80`, the measured slope was `-0.00252` against the frozen operational limit of `±0.00250`.

Close enough to tempt reinterpretation.

Not close enough to pass the declared criterion.

We could now search neighbouring budgets, adjust the late window, or redefine `B = 80` as effectively stationary.

Every one of those would be a new analysis chosen after seeing the result.

So we do none of them.

```text
FAILED
```

No tested budget satisfied the frozen operational criterion for stationarity.

All five remained slowly declining.

The threshold protects us from moving the line after seeing the data. It does not imply that `-0.00249` and `-0.00252` are physically different regimes.

---

## A Stable-Looking Flow

The five failing budgets shared one striking numerical pattern.

Their absolute populations differed substantially, yet gross material turnover as a fraction of population remained close to `0.17` per update across the entire budget family.

At first this looked like a different kind of stability.

But before treating it that way, there is an accounting identity we have to notice.

Let:

```text
A = attachments
L = losses
N = population after loss
ΔN = A - L
```

Then:

```text
A + L
=
ΔN + 2L
```

and therefore:

```text
gross turnover / N
=
ΔN / N
+
2L / N
```

The experiment fixes the loss probability at:

```text
δ = 0.08
```

and applies loss after construction.

For proportional loss at `δ = 0.08`, the expected loss count relative to the surviving post-loss population is approximately:

```text
δ / (1 - δ)
=
0.08 / 0.92
≈ 0.08696
```

So before any interesting dynamics enter:

```text
2L / N
≈
0.1739
```

The tested budgets are also declining only slowly, subtracting roughly a few thousandths from that number.

That already predicts a gross-turnover fraction very close to the `0.171` we measured.

So the near-constant turnover fraction is not, by itself, evidence for a new stable process regime.

Much of its apparent stability is mechanically induced by the fixed proportional loss rule and the accounting of material replacement.

That does not make V3 unnecessary.

It changes what V3 is allowed to teach us.

The interesting question becomes:

> **Which components depart from the mechanically constrained aggregate, and which remain sensitive to starting scale and computational scarcity?**

---

## Stable Stock Is Not Stable Flow

The previous chapter forced a distinction between a stock and a flow.

That distinction still matters:

```text
STABLE STOCK
≠
STABLE NORMALIZED FLOW
```

But V3 adds a warning.

A normalized flow can appear extremely stable because the experimental rules constrain its arithmetic.

Gross turnover is the clearest example here.

So V3 is not evidence that the crystal has discovered a preferred turnover rate.

Its value is comparative: it lets us ask whether the **components** of material traffic respond alike to changes in budget and starting scale.

They do not.

A process can drift in size while the traffic passing through each unit of it stays remarkably constant. Nothing about the first requires or prevents the second. They are separate properties of the same system, and we had been using one as a proxy for the other without noticing.

So the next experiment does not retry the failed one. It tests the hypothesis the failure generated.

---

## Start Small, Start Large

If normalized flow is genuinely a stable property of this regime, it should be relatively insensitive to the process's starting scale.

So we measured the full set of per-update flows:

```text
loss / population
attachments / population
reoccupation / population
first occupation / population
gross turnover / population
```

and crossed the same five budgets with three frozen starting conditions — small, medium and large crystals, produced by different warmup lengths before the budget was imposed.

So the test is straightforward:

under the same budget, do crystals started at different scales converge toward similar normalized material traffic even when their absolute populations remain different?

The claim was deliberately demanding.

For every normalized process metric, the coefficient of variation across starting sizes had to remain at or below:

```text
0.10
```

at every tested budget.

For gross turnover specifically, the coefficient of variation across budget means also had to remain at or below `0.10`, and its absolute late-window temporal slope had to remain at or below `0.0025`.

Every gate was required.

---

## The Aggregate Barely Moves

The measured gross-turnover fractions are:

| budget `B` | gross turnover / population |
|---:|---:|
| 48 | 0.17229 |
| 64 | 0.17150 |
| 80 | 0.17066 |
| 96 | 0.17147 |
| 128 | 0.17132 |

The coefficient of variation across those budget means is:

```text
0.0030
```

That is extraordinarily small numerically.

But after the accounting decomposition above, it is no longer mysterious.

With fixed proportional loss and small net population drift, the aggregate gross-turnover fraction is strongly constrained to live near this range.

So the `0.0030` CV is a measured property of the experiment, but it is **not evidence for an independently regulated turnover invariant**.

```text
0.0030
```

Three tenths of one percent, across a budget family that produces populations differing by a factor of three. And the quantity is not merely similar across budgets; it is nearly flat within each run. The worst late temporal slope across the family was around `0.00024`, against a frozen tolerance of `0.0025` — an order of magnitude inside it.

The mechanically constrained aggregate also changes little across starting sizes.

At `B = 48`:

```text
small     0.17330
medium    0.17267
large     0.17089
```

Several component fractions also remain within the frozen start-size sensitivity gate.

But one does not.

And that failure is more informative than the stability of the aggregate.

Across these tested starting sizes and budgets, gross material-event traffic remains close to the same fraction of population per update.

Absolute population is still changing.

This normalized traffic measure changes remarkably little.

That deserves a careful sentence rather than an excited one. It is a striking descriptive regularity across the tested conditions. It is not yet an invariant, and it is certainly not homeostasis: there is no target value anywhere in the substrate, no error signal, no controller, and nothing that would resist a change in it. We will come back to how much of it might be arithmetic rather than discovery.

---

## Expansion Breaks the Pattern

One component broke the full invariance claim.

```text
first occupation / population, at B = 48

small     0.01806
medium    0.01689
large     0.01356
```

Coefficient of variation: `0.118`, against a frozen maximum of `0.100`.

At the harshest tested budget, first occupation remains sensitive to the starting scale at which scarcity was imposed.
 At gentler budgets the dependence weakens and passes the gate — `0.092` at `B = 64`, down to `0.063` at `B = 128` — but the hypothesis required every metric at every budget, and dropping the one condition that broke it would be the same move we declined to make at `B = 80`.

```text
FAILED
```

The full process-vector hypothesis therefore fails.

But the identity of the failing component matters more than the binary verdict.

---

## Reuse and Expansion Respond Differently

Sort the measurements by how they behaved.

RELATIVELY STABLE ACROSS TESTED CONDITIONS
loss fraction
reoccupation fraction
gross turnover fraction
total attachment fraction

MORE SENSITIVE UNDER SEVERE SCARCITY
first-occupation fraction
```

The cleanest operational contrast is:

```text
REOCCUPATION
        versus
FIRST OCCUPATION
```

We can use **continuation** and **expansion** as shorthand for those two measured responses, with an important caveat:

```text
continuation
→ turnover and reuse within previously occupied structure

expansion
→ occupation of never-before-used locations
```

Neither term implies purpose, self-maintenance or a biological function.

Under the tested scarcity regimes, reoccupation-related turnover is comparatively stable across starting scales and budgets.

First occupation is more sensitive, especially under the harshest scarcity.

So the two observer-defined categories do not respond identically to finite computation.

Reoccupation-related turnover is comparatively insensitive to starting scale across these tested regimes.

First occupation becomes more sensitive under severe scarcity.

That earns a narrower result:

> **Reuse and first occupation respond differently to computational scarcity under the tested conditions.**

And it gives us a stronger hypothesis worth carrying forward:

> **Staying and growing may be different computational problems.**

Operationally, in this substrate — not biologically.

And note where the distinction came from.

The scheduling policies cannot see it; they sort by neighbour count.

The growth rule cannot see it; it treats every empty site alike.

The previous chapter introduced first occupation versus reoccupation as an observer-side bookkeeping distinction, a way for us to classify events the crystal itself cannot distinguish. This chapter finds that the two categories respond differently to a constraint neither of them knows about.

The observer-side distinction introduced for bookkeeping has turned out to separate two dynamical responses.

---

## What Does It Cost to Stay?

The chapter's title can now be answered, and the answer is not a substance.

The scarce quantity exposed by these experiments is **evaluation opportunity**. A candidate attachment can only occur where computation is spent on it, and under a binding budget, spending computation on one site means not spending it on another. Evaluating one candidate can therefore mean leaving another unevaluated on that update.

That is a genuine opportunity cost created by finite computation.

Reduce the allowance and the scale of the process falls with it. Change how it is divided and the balance between reuse and expansion moves. Neither effect requires the crystal to know anything, want anything, or hold any resource.

The bounded claim:

> **Finite evaluation opportunity strongly changes the population reached by the lossy Digital Crystal, and support-biased scheduling at fixed budget strongly changes reoccupation and the resulting material future. The experiments did not isolate a pure reuse-versus-expansion allocation effect.**

Biology pays for action through physical resource constraints, and that comparison will be tempting for the rest of the book. Resist it a little longer. This substrate has exposed a different primitive: a per-update limit on how many possible transitions can receive computation.

It is neither stored fuel nor an internal resource variable.

It is simply a bound on action.
 Whatever digital life turns out to require, it is worth knowing that a hard constraint on action can exist without energy having to be invented.

---

## What Survived the Three Tests

Three increasingly refined hypotheses failed:

```text
same finite budget
↛ clean symmetric reuse/expansion tradeoff

finite computation
↛ stationary population with turnover

normalized process flows
↛ complete invariance across size and budget
```

The arithmetic audit no longer needs to remain an open question.

Under the implemented update order:

```text
growth
↓
loss at δ = 0.08
↓
measure surviving population
```

and with:

```text
gross turnover = attachments + losses
```

the near-`0.171` aggregate is largely expected from the fixed proportional loss rate plus the small net population drift.

So the strongest conclusion is not:

```text
THE PROCESS MAINTAINS A TURNOVER RATE
```

It is:

```text
THE AGGREGATE TURNOVER RATE
IS STRONGLY CONSTRAINED BY THE PROTOCOL
```

The scientifically useful residue is the **asymmetry among its components**, especially the greater start-size sensitivity of first occupation under severe scarcity.

A stable measurement is scientifically interesting only to the extent that its stability is not already forced by the parameters used to generate it.

Here, much of the apparent stability was.

---

## Experimental Note

This chapter combines three frozen experiments under the same lossy Digital Crystal substrate with:

```text
loss rate δ = 0.08
```

### V1 — finite-budget allocation

The V1 quick profile used:

```text
48 independent groups
radius                 72
warmup                 14 updates
continuation           48 updates
late window            final 12 updates
primary budget         B = 256
```

The neutral budget characterization tested:

```text
B = 64, 128, 256, 512, 1024, 2048
and an unbounded reference
```

The scheduling policies used only current occupied-neighbour count plus keyed scheduling noise.

They could not inspect occupancy history.

The two frozen primary magnitude gates were:

```text
high-support reoccupation advantage
≥ 0.15 reoccupations per loss

low-support first-occupation advantage
≥ 100 first occupations per 1000 evaluations
```

Both were required for the two-sided tradeoff hypothesis.

### V2 — stationary population with turnover

V2 used:

```text
96 independent groups
radius                 72
warmup                 14 updates
continuation           72 updates
late window            final 20 updates

B = 48, 64, 80, 96, 128
```

with neutral scheduling only.

A candidate regime had to satisfy every frozen population, activity, turnover and capacity gate. No budget could be added after observing the V2 results.

### V3 — normalized process stability

V3 used:

```text
48 independent groups per condition
72 continuation updates
late window = 20

B = 48, 64, 80, 96, 128

small start     warmup 8
medium start    warmup 14
large start     warmup 20
```

The normalized process vector was:

```text
loss / population
attachments / population
reoccupation / population
first occupation / population
gross turnover / population
```

For every metric and budget, the coefficient of variation across starting sizes had to be at most `0.10`.

Gross turnover also had to satisfy:

```text
between-budget CV ≤ 0.10
absolute late temporal slope ≤ 0.0025
gross turnover fraction ≥ 0.05
```

All V3 gates were required.

The V3 full process-invariance hypothesis failed because first occupation exceeded the start-size CV limit at `B = 48`.

Full confidence intervals, randomization tests and per-run records remain in the accompanying experiment reports.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Finite evaluation opportunity constrains process scale | **SUPPORTED** | late population ~381 at `B=64` to ~3513 at `B=1024` |
| Scheduling changes the material future at fixed budget | **SUPPORTED** | population 1131–1923 and reoccupation/loss 0.534–0.959 at `B=256` |
| High-support scheduling meaningfully increases reuse | **SUPPORTED** | advantage `0.425` against required `0.150` |
| Low-support scheduling meaningfully increases expansion | **FAILED** | advantage `61.6` against required `100` per 1000 evaluations |
| The full two-sided allocation tradeoff holds | **FAILED** | one arm below its declared magnitude |
| Some finite budget yields stationary population with turnover | **FAILED** | best slope `-0.00252` against a required absolute slope of `0.00250` |
| Gross normalized turnover remains numerically stable across the tested budgets | **SUPPORTED** | `0.17066–0.17229`; between-budget CV `0.0030` |
| Near-constant gross turnover constitutes an independent substrate stability law | **NOT SUPPORTED** | the aggregate is largely predicted by fixed `δ = 0.08`, post-loss normalization and small net drift |
| Loss, attachment and reoccupation fractions satisfy the frozen start-size sensitivity gate | **SUPPORTED** | each remains within the `0.10` CV threshold across tested start sizes and budgets |
| First occupation is start-size insensitive under severe scarcity | **FAILED** | CV `0.118` at `B=48` against maximum `0.100` |
| The complete normalized process vector is invariant | **FAILED** | first occupation at `B=48` breaks the frozen criterion |
| Reoccupation-related turnover and first occupation respond identically to scarcity | **NOT SUPPORTED** | first occupation shows greater start-size sensitivity under severe scarcity |
| The crystal has metabolism, homeostasis or a sustainable body size | **NOT CLAIMED** | no target, controller, resource or set point exists |

---

## Is There Actually a Thing Here?

Put the results together:

```text
size depends strongly on available computation
allocation changes the material future
material turns over continuously
population does not settle
some normalized process rates remain surprisingly stable
```

We have been calling this *the crystal* since *The Digital Crystal*.

But several easy candidates for what that noun might denote have now failed us.

It is not:

```text
a fixed collection of material

a fixed morphology

a stationary population

a permanently fixed geometric interface
```

Something continues through all of those changes.

What remains is the continuing dynamics.

We have not yet shown whether those dynamics belong to one causally privileged region or whether the noun *crystal* is imposing unity where the dynamics themselves do not.

Connected geometry is not enough to answer that question.

Neither is turnover stability.

The next experiment has to ask directly whether the continuing dynamics form a causally coherent region with a natural boundary, or whether our noun is imposing unity on something more diffuse.

> **Is there actually one causally coherent thing here?**
