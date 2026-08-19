+++
title = "11: What Does It Cost to Stay?"
date = "2026-08-14T16:00:00+01:00"
draft = false
description = "Limit how many construction opportunities the Digital Crystal can evaluate per update and the population reached becomes budget-dependent. Scheduling changes the material future, while an apparent turnover invariant collapses under an accounting audit."
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

So one major question remained:

> **What happens when those construction opportunities must compete for computation?**

This chapter removes that luxury, and it removes it in the smallest possible way.

---

## Not Everything Gets Evaluated

Instead of evaluating every eligible construction site, the process may evaluate at most:

```text
B
```

candidate sites per update. A site that is not evaluated simply gets no attachment attempt on that step. It is not blocked, not penalized, not remembered; the opportunity passes and may return next update.


Nothing else changes.

The attachment probability is what it always was.

The loss rule is what it was in the previous chapter.

The crystal gains no new internal state whatsoever:

```text
no energy
no fuel
no resource counter
no metabolism variable
no maintenance controller
no target size
no record of what was neglected
```

The entire modification is:

```text
many possible transitions
↓
only B may be evaluated
```

It is worth being precise about what kind of constraint this is.

`B` is not the crystal's energy.

It is a bound on how much of the currently available transition structure can be processed in one update.

If that later resembles the way physical resource limits constrain biological action, that comparison will have to be earned separately.

The point here is simpler.

Scarcity can matter enormously **without** pretending computation is ATP.

---

## The Budget Constrains the Population Reached

The first result arrived before any of the more interesting questions did.

Holding the loss rate fixed and sweeping the budget under neutral scheduling gave approximate late populations:

| budget `B` | late population |
|---:|---:|
| 64 | ~381 |
| 128 | ~829 |
| 256 | ~1717 |
| 512 | ~3092 |
| 1024 | ~3513 |
| unlimited | ~3462 |

The relationship is unmistakable in the binding part of the sweep.

As available evaluation opportunity falls, so does the population reached within the tested horizon.

Above roughly `B = 512`, the curve begins to flatten because the budget increasingly stops binding. Once there are fewer eligible candidates than available evaluations, additional budget cannot do much.

The exact ordering of the high-budget values is therefore not worth interpreting.

What matters is the binding end.

At the tested horizon, the crystal at `B = 64` has a late population roughly one ninth that of the unlimited reference.

Whether this is an asymptotic scale difference or partly a time-rescaled growth difference is **not established by this experiment**.

What is established is narrower:

```text
AVAILABLE EVALUATION OPPORTUNITY
↓
POPULATION REACHED WITHIN THE TESTED HORIZON
```

This is a new kind of constraint in the book.

Previous experiments constrained which transitions were locally possible.

Here many transitions remain perfectly eligible but never receive an evaluation on that update.

The new distinction is:

```text
eligible to happen
≠
given computational opportunity to happen
```

The realized dynamics are no longer determined only by:

```text
what can happen
```

but also by:

```text
what gets computational opportunity to happen
```

Until now, every eligible site received an evaluation.

The distinction had been experimentally invisible.

---

## Scarcity Creates Allocation

Once the budget binds, eligible transitions begin to compete for evaluation opportunity.

Suppose an update presents:

```text
500 eligible candidates
```

and:

```text
B = 128
```

Only 128 can be considered at all.

Which 128?

Some rule has to answer that question.

Not because the crystal chooses.

Not because it has priorities.

It has neither.

But the selection has to occur somehow, and different selection rules can produce different material futures.

That is allocation in a strictly mechanical sense:

```text
FINITE COMPUTATION
↓
SELECTION AMONG POSSIBLE TRANSITIONS
↓
DIFFERENT MATERIAL FUTURES
```

So we froze a budget and changed only the scheduling rule.

---

## Three Ways to Allocate the Same Budget

The three policies were deliberately simple:

```text
HIGH SUPPORT
sites with more occupied neighbours evaluated first

NEUTRAL
keyed-random ordering

LOW SUPPORT
sites with fewer occupied neighbours evaluated first
```

None of them can inspect the occupancy ledger.

None knows whether a candidate is:

```text
never-before-occupied territory
```

or:

```text
a location that was occupied and later lost
```

That distinction remains entirely observer-side.

But local support carries information about geometry.

Reoccupation candidates often sit inside more occupied neighbourhoods than candidates near the outer frontier.

So support-biased scheduling can indirectly alter which kinds of locations receive evaluation.

There is an important confound, however.

Occupied-neighbour count also enters the attachment rule itself.

So support affects two things at once:

```text
support
→
changes which candidates receive evaluation

AND

support
→
changes attachment probability
for evaluated candidates
```

High-support scheduling therefore does not merely select more reoccupation-like candidates.

It also selects candidates whose local geometry can make attachment more likely.

This experiment is consequently a test of:

> **support-biased allocation through local geometry**

not a clean causal test of:

> **reuse versus expansion independent of support**

That stronger claim would require a support-matched control.

We did not run one.

---

## Same Budget, Different Futures

At:

```text
loss rate δ = 0.08
budget B = 256
```

the three scheduling policies produced:

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

Under high-support scheduling, reoccupation runs at roughly:

```text
0.96 events per loss
```

Under low-support scheduling it falls to roughly:

```text
0.53 events per loss
```

The scheduling rule does not know what reoccupation is.

Yet it changes reoccupation dramatically.

We do not need the stronger reuse-versus-expansion interpretation to keep this result.

Finite computation has already done something important:

> **Which eligible opportunities receive evaluation has become causally consequential.**

---

## But the Predicted Tradeoff Fails

The hypothesis had been more specific than:

```text
scheduling matters
```

It predicted a clean two-sided tradeoff.

High-support scheduling should meaningfully increase reuse.

Low-support scheduling should meaningfully increase first occupation.

Both arms had to clear magnitude thresholds fixed before the result was inspected.

The first arm compared high support against low support:

```text
reoccupation / loss

high support - low support
≈ 0.425

required
≥ 0.150
```

That passed comfortably.

The second arm used the opposite contrast:

```text
first occupations / 1000 evaluations

low support - high support
≈ 61.6

required
≥ 100
```

The observed expansion-side effect reached only about:

```text
61.6%
```

of the predeclared meaningful magnitude.

It was statistically detectable.

It did not clear the scientific gate.

Because the hypothesis required both arms:

```text
FAILED
```

We do not get to lower the threshold afterward.

And we do not get to report the arm that passed as though it were the whole hypothesis.

What survives is narrower:

```text
finite budget
→ constrains what population is reached

same budget + different scheduling
→ different material futures

high-support scheduling
→ strongly increases reoccupation
```

What fails is the tidy symmetric picture in which directing computation toward one side produces an equally strong opposite effect on the other.

That asymmetry will matter later.

For now, the two-sided allocation hypothesis stays failed.

---

## Could It Simply Stay?

The budget sweep contained another suggestive regime.

Under severe scarcity, late population change approached zero while loss, attachment and reoccupation continued.

That revived a question that material loss alone had failed to answer.

The previous chapter found no finite sustainable size because loss manufactured new construction opportunities.

But loss plus a ceiling on how many of those opportunities can be evaluated is different.

Now the replacement process itself is bounded.

So the new question was:

> **Is there a finite budget at which population becomes approximately stationary while material turnover continues?**

That is much stronger than:

```text
growth becomes slow
```

A qualifying regime had to satisfy every frozen gate:

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

Freezing on death does not count.

Freezing against the wall of the world does not count.

A population with no material activity does not count.

We wanted:

```text
approximately stationary population
+
continuing material turnover
```

The candidate budgets were frozen before the run:

```text
B = 48, 64, 80, 96, 128
```

No new candidate could be added after seeing the result.

---

## Almost

Nearly every gate passed at every tested budget.

Populations survived.

Capacity was nowhere near binding.

Loss continued.

Reoccupation continued.

First occupation continued.

Gross turnover remained substantial.

Late net growth was small.

One gate failed.

The late normalized population slopes were:

```text
B = 48     -0.00319
B = 64     -0.00271
B = 80     -0.00252
B = 96     -0.00268
B = 128    -0.00280
```

against:

```text
|slope| ≤ 0.00250
```

At `B = 80`:

```text
measured     -0.00252
required     within ±0.00250
```

Close enough to tempt reinterpretation.

Not close enough to pass the declared criterion.

We could now search neighbouring budgets.

We could try:

```text
78
79
81
82
```

We could alter the late window.

We could declare `B = 80` "effectively stationary."

Every one of those would be a new analysis chosen after seeing the result.

So we do none of them.

```text
FAILED
```

No tested budget satisfied the frozen operational criterion for stationarity.

All five remained slowly declining.

The threshold protects us from moving the line after seeing the data.

It does **not** imply that:

```text
-0.00249
```

and:

```text
-0.00252
```

are physically distinct natural regimes.

The operational claim failed.

Nothing stronger is required.

---

## A Stable-Looking Flow

The five failing budgets shared one striking numerical pattern.

Their absolute populations differed substantially.

Yet gross material turnover as a fraction of population remained close to:

```text
0.17 per update
```

across the whole budget family.

At first, this looked like a different kind of stability.

Perhaps we had asked the wrong question.

Perhaps population did not stabilize because population was not the relevant stable quantity.

Before promoting that interpretation, however, there is an accounting identity we have to notice.

Let:

```text
A = attachments during an update
L = losses during the update
N = population after loss
ΔN = net population change
```

Since:

```text
ΔN = A - L
```

then:

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

The protocol fixes the per-cell loss probability at:

```text
δ = 0.08
```

and applies loss after construction.

For proportional loss at `δ = 0.08`, expected loss relative to the surviving post-loss population is approximately:

$$
\frac{\delta}{1-\delta}
=
\frac{0.08}{0.92}
\approx 0.08696
$$

So even before invoking an interesting process-level regularity:

$$
2\frac{L}{N}
\approx 0.1739
$$

The tested low-budget regimes are also drifting downward slowly, subtracting a few thousandths through the:

```text
ΔN / N
```

term.

That already places expected gross turnover very near the measured:

```text
~0.171
```

range.

So much of the apparent turnover stability is mechanically induced by:

```text
fixed proportional loss
+
post-loss normalization
+
small net population drift
```

The measurement is real.

The strongest interpretation is not.

```text
MEASUREMENT IS STABLE
≠
SYSTEM REGULATES STABILITY
```

This is exactly why attractive regularities need controls too.

---

## Stable Stock Is Not Stable Flow

The previous chapter forced a distinction between a stock and a flow.

That distinction still matters:

```text
STABLE STOCK
≠
STABLE NORMALIZED FLOW
```

But this experiment adds a warning.

A normalized flow can appear exceptionally stable because the protocol constrains its arithmetic.

Gross turnover is the clearest example here.

So the near-constant aggregate is not evidence that the crystal has discovered a preferred turnover rate.

There is:

```text
no target value
no error signal
no controller
no mechanism resisting deviations
```

and therefore no basis for calling the result homeostasis.

But the decomposition leaves another question intact.

If the aggregate is heavily constrained by accounting, do all of its **components** respond to scarcity and starting scale in the same way?

That is what the next experiment tests.

---

## Start Small, Start Large

The next experiment crossed the same five budgets:

```text
B = 48, 64, 80, 96, 128
```

with three frozen starting conditions:

```text
small
medium
large
```

produced by different warmup lengths before scarcity was imposed.

For each update, we separated the process into:

```text
loss / population
attachments / population
reoccupation / population
first occupation / population
gross turnover / population
```

The question was no longer:

> Does the crystal find a stationary size?

It was:

> **Do these normalized components respond similarly when the same scarcity is imposed at different starting scales?**

The claim was deliberately demanding.

For every normalized process metric, the coefficient of variation across starting sizes had to remain at or below:

```text
0.10
```

at every tested budget.

For gross turnover specifically, the frozen protocol also required:

```text
between-budget CV ≤ 0.10

absolute late temporal slope ≤ 0.0025

gross turnover fraction ≥ 0.05
```

Every gate was required.

---

## The Aggregate Barely Moves

The measured gross-turnover fractions were:

| budget `B` | gross turnover / population |
|---:|---:|
| 48 | 0.17229 |
| 64 | 0.17150 |
| 80 | 0.17066 |
| 96 | 0.17147 |
| 128 | 0.17132 |

The coefficient of variation across those budget means was:

```text
0.0030
```

Numerically, that is extraordinarily small.

But after the accounting decomposition above, it is no longer mysterious.

Fixed proportional loss and small net population drift strongly constrain the aggregate gross-turnover fraction to live near this range.

So:

```text
CV = 0.0030
```

is a measured property of the experiment.

It is **not evidence for an independently regulated turnover invariant**.

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

---

## Expansion Breaks the Pattern

The component that breaks the full invariance claim is:

```text
first occupation / population
```

At `B = 48`:

```text
small     0.01806
medium    0.01689
large     0.01356
```

Its coefficient of variation is:

```text
0.118
```

against a frozen maximum of:

```text
0.100
```

So that gate fails.

At gentler budgets, the dependence weakens:

```text
B = 64      CV ≈ 0.092
B = 80      CV ≈ 0.077
B = 96      CV ≈ 0.074
B = 128     CV ≈ 0.063
```

Those pass.

But the hypothesis required:

```text
every metric
at every budget
```

to clear the frozen criterion.

Dropping `B = 48` now would be the same move we refused to make around `B = 80`.

So:

```text
FAILED
```

The complete normalized process-vector hypothesis does not survive.

But once again, the identity of the failing component is more informative than the binary result.

---

## Reuse and Expansion Respond Differently

Sort the measured components by how they behaved:

```text
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

We can use **continuation** and **expansion** as shorthand for those observer-defined measurements:

```text
continuation
→ turnover and reuse within previously occupied structure

expansion
→ occupation of never-before-used locations
```

Neither term implies:

```text
purpose
self-maintenance
biological function
```

The crystal does not represent either category.

The scheduling policies cannot inspect them.

The growth rule treats both as empty sites.

They are categories maintained by the observer ledger.

And yet under the tested scarcity regimes, those categories do not respond identically.

Reoccupation-related turnover is comparatively insensitive to starting scale.

First occupation becomes more sensitive under severe scarcity.

That earns a bounded result:

> **Reuse and first occupation respond differently to computational scarcity under the tested conditions.**

And it gives us a stronger hypothesis worth carrying forward:

> **Staying and growing may be different computational problems.**

Operationally, in this substrate.

Not biologically.

The interesting point is where the distinction came from.

First occupation versus reoccupation began as bookkeeping — a way for the laboratory to classify events the crystal itself could not distinguish.

Under scarcity, that observer-side distinction separates two different measured responses.

That is worth keeping.

It is not yet an ontology.

---

## What Does It Cost to Stay?

The chapter's title can now be answered, but the answer is not a substance.

The scarce quantity **imposed by these experiments** is:

> **evaluation opportunity**

A candidate attachment can occur only if the candidate receives an evaluation.

Under a binding budget, evaluating one candidate can mean that another eligible candidate receives no evaluation on that update.

That is a genuine opportunity cost in the formal sense.

It requires no agent deciding to spend anything.

It requires only:

```text
more eligible opportunities
than available evaluations
```

Reduce the budget and the population reached within the tested horizon changes dramatically.

Hold the budget fixed and change support-biased scheduling, and the material future changes with it.

The bounded claim is:

> **Finite evaluation opportunity strongly changes the population reached by the lossy Digital Crystal, and support-biased scheduling at fixed budget strongly changes reoccupation and the resulting material future. The experiments did not isolate a pure reuse-versus-expansion allocation effect.**

Biology pays for action through physical resource constraints, and that comparison will remain tempting.

Resist it a little longer.

This substrate has exposed a different primitive:

```text
a per-update bound
on how many possible transitions
can receive computation
```

It is not stored fuel.

It is not an internal resource variable.

It is not metabolism.

It is simply a limit on action.

Whatever digital life eventually requires, it is useful to know that scarcity can exist in a computational substrate without energy having to be invented first.

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

The first failure told us that finite scheduling effects are not a tidy two-sided exchange between reuse and expansion.

The second told us that no tested budget met the frozen operational criterion for stationary population with continuing turnover.

The third told us that even normalized process components do not all respond identically to starting scale.

And one apparent positive result weakened under inspection.

The near-constant gross-turnover fraction:

```text
~0.171
```

looked at first like an emergent stable process variable.

The accounting audit showed that much of that apparent stability is mechanically induced by the fixed loss rate, the update order, the normalization convention and the small net drift.

That correction matters.

A stable measurement is scientifically interesting only to the extent that its stability is not already forced by the parameters used to generate it.

Here, much of it was.

What remains is simpler:

```text
FINITE EVALUATION
↓
NOT EVERY ELIGIBLE TRANSITION IS CONSIDERED

SCHEDULING
↓
CHANGES WHICH OPPORTUNITIES RECEIVE COMPUTATION

SAME BUDGET
↓
CAN PRODUCE DIFFERENT MATERIAL FUTURES

REOCCUPATION AND FIRST OCCUPATION
↓
DO NOT RESPOND IDENTICALLY UNDER SEVERE SCARCITY
```

That is enough.

---

## Experimental Note

This chapter combines three frozen experiments under the same lossy Digital Crystal substrate:

```text
loss rate δ = 0.08
```

### V1 — Finite-Budget Allocation

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

The main-text table stops at `B = 1024` because the scientific point concerns the binding part of the sweep.

`B = 2048` remains in the complete experimental record as an additional non-binding reference.

The scheduling policies used current occupied-neighbour count together with keyed deterministic scheduling noise.

They could not inspect occupancy history.

Because occupied-neighbour count also enters the attachment rule, this experiment does not isolate reuse-versus-expansion allocation independently of local support.

No support-matched scheduling control was run.

The two frozen primary magnitude gates were:

```text
high-support minus low-support
reoccupation advantage

≥ 0.15 reoccupations per loss
```

and:

```text
low-support minus high-support
first-occupation advantage

≥ 100 first occupations
per 1000 evaluations
```

Both were required for the two-sided tradeoff hypothesis.

### V2 — Stationary Population With Turnover

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

For each run, late normalized population slope was obtained by fitting a line to population over the late window and dividing that slope by mean population over the same window.

A candidate budget had to satisfy every frozen population, activity, turnover and capacity gate.

No budget could be added after inspecting the V2 results.

### V3 — Normalized Process Components

V3 used:

```text
48 independent groups per condition

radius                 72
continuation           72 updates
late window            final 20 updates

B = 48, 64, 80, 96, 128

small start            warmup 8
medium start           warmup 14
large start            warmup 20
```

For every late-window update:

```text
loss fraction
=
losses / post-loss population

attachment fraction
=
attachments / post-loss population

reoccupation fraction
=
reoccupations / post-loss population

first-occupation fraction
=
first occupations / post-loss population

gross-turnover fraction
=
(attachments + losses) / post-loss population
```

Growth occurs before loss.

That update order is important to the accounting audit in the main text.

For every normalized process metric and every budget:

```text
CV across starting sizes ≤ 0.10
```

was required.

Gross turnover also had to satisfy:

```text
between-budget CV ≤ 0.10

absolute late temporal slope ≤ 0.0025

gross-turnover fraction ≥ 0.05
```

All gates were required.

The complete process-invariance hypothesis failed because first occupation exceeded the start-size CV limit at:

```text
B = 48
```

Full confidence intervals, bootstrap summaries, randomization tests and per-run records remain in the accompanying experimental reports.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Finite evaluation opportunity constrains the population reached within the tested horizon | **SUPPORTED** | late population ~381 at `B=64` to ~3513 at `B=1024` |
| Scheduling changes the material future at fixed budget | **SUPPORTED** | population 1131–1923 and reoccupation/loss 0.534–0.959 at `B=256` |
| Evaluation opportunity was allocated between reuse and expansion independently of local-support effects | **NOT CLAIMED** | neighbour support enters both scheduling and attachment probability; no support-matched control was run |
| High-support scheduling meaningfully increases reoccupation | **SUPPORTED** | high-minus-low advantage `0.425` against required `0.150` |
| Low-support scheduling produces the required expansion advantage | **FAILED** | low-minus-high advantage `61.6` against required `100` per 1000 evaluations |
| The full two-sided allocation tradeoff holds | **FAILED** | one required arm failed |
| Some tested finite budget produces stationary population with continuing turnover | **FAILED** | best slope `-0.00252` against frozen `±0.00250` criterion |
| Measured gross normalized turnover lies in a narrow band across tested budgets | **SUPPORTED** | `0.17066–0.17229`; between-budget CV `0.0030` |
| That narrow band constitutes an independent substrate stability law | **NOT SUPPORTED** | much of the aggregate is predicted by fixed `δ = 0.08`, post-loss normalization and small net drift |
| Loss, attachment and reoccupation fractions satisfy the frozen start-size sensitivity gate | **SUPPORTED** | each remains within the `0.10` CV threshold across tested start sizes and budgets |
| First occupation is start-size insensitive under severe scarcity | **FAILED** | CV `0.118` at `B=48` against maximum `0.100` |
| The complete normalized process vector is invariant | **FAILED** | first occupation at `B=48` breaks the frozen criterion |
| Reoccupation-related turnover and first occupation respond identically to scarcity | **NOT SUPPORTED** | first occupation shows greater start-size sensitivity under severe scarcity |
| The crystal has metabolism, homeostasis or a sustainable body size | **NOT CLAIMED** | no target, controller, internal resource or set point exists |

---

## Is There Actually a Thing Here?

Put the surviving results together:

```text
population reached depends strongly on available computation

scheduling changes the material future

material turns over continuously

no tested budget produces stationary population

the prettiest apparent flow invariant
is largely an accounting consequence

reoccupation and first occupation
do not respond identically to scarcity
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

But we have not yet shown whether those dynamics belong to one causally privileged region.

Connected geometry is not enough.

Turnover is not enough.

A computational budget is not enough.

The next experiment has to ask whether the continuing dynamics form a causally coherent region with a natural boundary, or whether the noun *crystal* is imposing unity on something more diffuse.

> **Is there actually one causally coherent thing here?**