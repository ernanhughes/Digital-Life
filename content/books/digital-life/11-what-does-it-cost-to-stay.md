+++
title = "11: What Does It Cost to Stay?"
date = "2026-08-14T16:00:00+01:00"
draft = false
description = "Limit how many construction opportunities the Digital Crystal can evaluate per update and the population reached becomes budget-dependent. Scheduling changes the material future, while an apparent turnover invariant collapses under an accounting audit."
weight = 11
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Scarcity", "Turnover", "Computation", "Experiments"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "review"
+++

The last chapter ended with an impressive number and a suspicion about it. Under its exact-count experiment, roughly `0.94–0.96` reoccupation events were observed per loss event, and more than ninety-three percent of distinct lost locations returned at least once within the finite run. Among the returns we observed, the typical delay was only a step or two — and all of it happened through the ordinary growth rule encountering ordinary empty sites.

But those measurements came from a generous regime. Every eligible construction opportunity received an attachment evaluation. Vacancies inside the crystal and candidates at the outer edge never had to compete for capacity.

So one major question remained:

> **What happens when those construction opportunities must compete for computation?**

This chapter removes that luxury, and removes it in the smallest possible way.

---

## Not Everything Gets Evaluated

Instead of evaluating every eligible construction site, the process may now evaluate at most `B` candidate sites per update. A site that is not evaluated simply gets no attachment attempt on that step. It is not blocked, not penalized, not remembered; the opportunity passes and may return next update.

Nothing else changes. The attachment probability is what it always was, the loss rule is what it was in the previous chapter, and the crystal gains no new internal state whatsoever:

```text
no energy              no metabolism variable
no fuel                no maintenance controller
no resource counter    no target size
no record of what was neglected
```

The entire modification is that many transitions remain possible while only `B` of them may be looked at.

It is worth being precise about what kind of constraint this is. `B` is not the crystal's energy. It is a bound on how much of the currently available transition structure can be processed in one update. If that later resembles the way physical resource limits constrain biological action, the comparison will have to be earned separately.

The point here is simpler. Scarcity can matter enormously **without** pretending computation is ATP (adenosine triphosphate).

---

## The Budget Constrains the Population Reached

The first result arrived before any of the more interesting questions did. Holding the loss rate fixed and sweeping the budget under neutral scheduling gave these approximate late populations:

| budget `B` | late population |
|---:|---:|
| 64 | ~381 |
| 128 | ~829 |
| 256 | ~1717 |
| 512 | ~3092 |
| 1024 | ~3513 |
| unlimited | ~3462 |

The relationship is unmistakable in the binding part of the sweep: as available evaluation opportunity falls, so does the population reached within the tested horizon.

Above roughly `B = 512` the curve flattens, because the budget increasingly stops binding — once there are fewer eligible candidates than available evaluations, extra budget cannot do much. The exact ordering of the high-budget values is therefore not worth interpreting.

What matters is the binding end, where the crystal at `B = 64` reaches a late population roughly one ninth that of the unlimited reference.

Whether that is an asymptotic scale difference or partly a time-rescaled growth difference is **not established by this experiment**. What is established is narrower: available evaluation opportunity constrains the population reached within the tested horizon.

This is a new kind of constraint in the book. Previous experiments constrained which transitions were locally possible. Here many transitions remain perfectly eligible but never receive an evaluation on that update, which forces a distinction that had been experimentally invisible for as long as every eligible site was still being checked:

```text
eligible to happen
≠
given computational opportunity to happen
```

---

## Scarcity Creates Allocation

Once the budget binds, eligible transitions begin to compete for evaluation opportunity. Suppose an update presents five hundred eligible candidates and the budget is 128. Only 128 can be considered at all.

Which 128?

Some rule has to answer that question. Not because the crystal chooses, and not because it has priorities — it has neither. But the selection has to occur somehow, and different selection rules can produce different material futures. That is allocation in a strictly mechanical sense: finite computation forces a selection among possible transitions, and that selection has material consequences.

So we froze a budget and changed only the scheduling rule.

---

## Three Ways to Allocate the Same Budget

The three policies were deliberately simple:

```text
HIGH SUPPORT    sites with more occupied neighbours evaluated first
NEUTRAL         keyed-random ordering
LOW SUPPORT     sites with fewer occupied neighbours evaluated first
```

None of them can inspect the occupancy ledger. None knows whether a candidate is never-before-occupied territory or a location that was occupied and later lost; that distinction remains entirely observer-side. But local support carries information about geometry, because reoccupation candidates often sit inside more occupied neighbourhoods than candidates near the outer frontier. Support-biased scheduling can therefore alter which kinds of location receive evaluation, indirectly.

There is an important confound. Occupied-neighbour count also enters the attachment rule itself, so support does two things at once: it changes which candidates receive an evaluation, and it changes the attachment probability of the candidates that receive one. High-support scheduling does not merely select more reoccupation-like candidates — it selects candidates whose local geometry already makes attachment more likely.

This experiment is consequently a test of **support-biased allocation through local geometry**, not a clean causal test of **reuse versus expansion independent of support**. The stronger claim would require a support-matched control. We did not run one.

---

## Same Budget, Different Futures

At a loss rate of `δ = 0.08` and a budget of `B = 256`, the three scheduling policies produced:

| measure | high support | neutral | low support |
|---|---:|---:|---:|
| late population | 1923 | 1723 | 1131 |
| reoccupation per loss | 0.959 | 0.844 | 0.534 |
| first occupations per 1000 evaluations | 188 | 212 | 249 |
| late net growth | +24.3 | +10.0 | −1.5 |

The same evaluation budget, scheduled differently through local support, produces mean late populations differing by roughly seventy percent. The mean late net-growth statistic even changes sign across the policies. Reoccupation runs at roughly `0.96` events per loss under high-support scheduling and falls to roughly `0.53` under low-support scheduling — and the scheduling rule does not know what reoccupation is.

We do not need the stronger reuse-versus-expansion interpretation to keep this result. Finite computation has already done something important:

> **Which eligible opportunities receive evaluation has become causally consequential.**

---

## But the Predicted Tradeoff Fails

The hypothesis had been more specific than *scheduling matters*. It predicted a clean two-sided tradeoff: high-support scheduling should meaningfully increase reuse, and low-support scheduling should meaningfully increase first occupation. Both arms had to clear magnitude thresholds fixed before the result was inspected.

The reuse arm passed comfortably. High-support scheduling beat low-support scheduling by about `0.425` reoccupations per loss, against a required `0.150`.

The expansion arm did not. Low-support scheduling beat high-support scheduling by about `61.6` first occupations per thousand evaluations, against a required `100` — roughly sixty-two percent of the declared meaningful magnitude. The effect was statistically detectable. It did not clear the scientific gate.

Because the hypothesis required both arms, the two-sided allocation tradeoff is **FAILED**. We do not get to lower the threshold afterward, and we do not get to report the arm that passed as though it were the whole hypothesis.

What survives is narrower. A finite budget constrains the population reached; the same budget under different scheduling produces different material futures; and high-support scheduling strongly increases reoccupation. What fails is the tidy symmetric picture in which directing computation toward one side produces an equally strong opposite effect on the other. That asymmetry will matter later.

---

## Could It Simply Stay?

The budget sweep contained another suggestive regime. Under severe scarcity, late population change approached zero while loss, attachment and reoccupation continued — which revived a question that material loss alone had failed to answer.

The previous chapter found no finite sustainable size, because loss manufactured new construction opportunities. Loss plus a ceiling on how many of those opportunities can be evaluated is a different situation: now the replacement process itself is bounded. So the new question was:

> **Is there a finite budget at which population becomes approximately stationary while material turnover continues?**

That is much stronger than *growth becomes slow*. Freezing on death does not count. Freezing against the wall of the world does not count. A population with no material activity does not count. We wanted an approximately stationary population **with** continuing material turnover, and a qualifying regime had to satisfy every gate frozen before the run:

```text
|late normalized population slope|   ≤ 0.0025
late mean population                 ≥ 150
mean late losses                     ≥ 5 per update
mean late reoccupations              ≥ 2 per update
mean late first occupations          ≥ 2 per update
gross turnover / population          ≥ 0.05
|late net change|                    ≤ 3 cells per update
maximum capacity fraction            < 0.75
```

The candidate budgets — `B = 48, 64, 80, 96, 128` — were frozen before the run as well. No new candidate could be added after seeing the result.

---

## Almost

Nearly every gate passed at every tested budget. Populations survived, capacity was nowhere near binding, loss and reoccupation and first occupation all continued, gross turnover remained substantial, and late net growth was small.

One gate failed. The late normalized population slopes were:

```text
B = 48     -0.00319
B = 64     -0.00271
B = 80     -0.00252
B = 96     -0.00268
B = 128    -0.00280
```

against a frozen requirement of `|slope| ≤ 0.00250`. The best of them, at `B = 80`, missed by two hundred-thousandths.

Close enough to tempt reinterpretation. Not close enough to pass the declared criterion.

We could now search neighbouring budgets — 78, 79, 81, 82. We could alter the late window. We could declare `B = 80` "effectively stationary." Every one of those would be a new analysis chosen after seeing the result, so we do none of them. The stationarity hypothesis is **FAILED**: no tested budget satisfied the frozen operational criterion, and all five remained slowly declining.

The threshold protects us from moving the line after seeing the data. It does **not** imply that a slope of `-0.00249` and a slope of `-0.00252` are physically distinct natural regimes. The operational claim failed, and nothing stronger is required.

---

## A Stable-Looking Flow

The five failing budgets shared one striking numerical pattern. Their absolute populations differed substantially, yet gross material turnover as a fraction of population stayed close to `0.17` per update across the whole budget family.

At first this looked like a different kind of stability — as though population had failed to stabilize because population was not the relevant stable quantity. It is not. Most of that number is forced by the protocol's own arithmetic, and the arithmetic is worth walking through once.

Growth happens before loss, and the protocol fixes the per-cell loss probability at `δ = 0.08`. Write `A` for attachments during an update, `L` for losses, and `N` for the population surviving after loss. Net change is `A - L`, so gross turnover `A + L` can be rewritten as net change plus twice the losses, and dividing through by population gives:

$$
\frac{A+L}{N}
=
\frac{\Delta N}{N}
+
2\frac{L}{N}
$$

For proportional loss applied after construction, expected losses relative to the surviving population are about `0.08 / 0.92 ≈ 0.08696`, which puts the second term at roughly `0.1739` on its own. The tested low-budget regimes are also drifting slowly downward, so the first term subtracts a few thousandths. That already lands within a whisker of the measured `~0.171` range.

So much of the apparent turnover stability is mechanically induced by fixed proportional loss, post-loss normalization and small net population drift. The measurement is real. The strongest interpretation is not.

```text
MEASUREMENT IS STABLE
≠
SYSTEM REGULATES STABILITY
```

This is exactly why attractive regularities need controls too.

---

## Stable Stock Is Not Stable Flow

The previous chapter forced a distinction between a stock and a flow, and that distinction still holds: a stable stock is not a stable normalized flow. But this experiment adds a warning running the other way. A normalized flow can appear exceptionally stable because the protocol constrains its arithmetic, and gross turnover is the clearest example here.

So the near-constant aggregate is not evidence that the crystal has discovered a preferred turnover rate. There is no target value, no error signal, no controller and no mechanism resisting deviations — and therefore no basis for calling the result homeostasis.

But the decomposition leaves another question intact. If the aggregate is heavily constrained by accounting, do all of its **components** respond to scarcity and starting scale in the same way? That is what the next experiment tests.

---

## Start Small, Start Large

The next experiment crossed the same five budgets with three frozen starting conditions — small, medium and large — produced by different warmup lengths before scarcity was imposed. For each update we separated the process into five normalized components: loss, attachments, reoccupation, first occupation and gross turnover, each divided by population.

The question was no longer whether the crystal finds a stationary size. It was:

> **Do these normalized components respond similarly when the same scarcity is imposed at different starting scales?**

The claim was deliberately demanding. Every normalized process metric had to hold a coefficient of variation across starting sizes at or below `0.10`, at every tested budget. Gross turnover carried three further frozen requirements: a between-budget CV at or below `0.10`, an absolute late temporal slope at or below `0.0025`, and a gross-turnover fraction of at least `0.05`. Every gate was required.

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

The coefficient of variation across those budget means is `0.0030`. Numerically that is extraordinarily small — and after the accounting decomposition above, no longer mysterious. Fixed proportional loss and small net population drift strongly constrain the aggregate to live near this range, so the tiny CV is a measured property of the experiment and **not evidence for an independently regulated turnover invariant**.

The mechanically constrained aggregate also changes little across starting sizes. At the most severe budget, `B = 48`, it runs `0.17330` from a small start, `0.17267` from a medium one and `0.17089` from a large one. Several component fractions likewise stay within the frozen start-size sensitivity gate.

One does not. And that failure is more informative than the stability of the aggregate.

---

## Expansion Breaks the Pattern

The component that breaks the full invariance claim is first occupation per unit population. At `B = 48` it runs `0.01806` from a small start, `0.01689` from a medium one and `0.01356` from a large one — a coefficient of variation of `0.118` against a frozen maximum of `0.100`. That gate fails.

At gentler budgets the dependence weakens and the gate passes: `0.092` at `B = 64`, `0.077` at `B = 80`, `0.074` at `B = 96`, and `0.063` at `B = 128`.

But the hypothesis required every metric at every budget to clear the frozen criterion, and dropping `B = 48` now would be the same move we refused to make around `B = 80`. The complete normalized process-vector hypothesis is **FAILED**.

Once again, the identity of the failing component is more informative than the binary result.

---

## Reuse and Expansion Respond Differently

Sorted by how they behaved, the measured components fall into two groups. Loss, reoccupation, total attachment and gross turnover were relatively stable across the tested conditions. First occupation was more sensitive under severe scarcity.

The cleanest operational contrast is between reoccupation and first occupation, and it is convenient to call them **continuation** and **expansion**: turnover and reuse within previously occupied structure, against occupation of never-before-used locations. Neither term implies purpose, self-maintenance or biological function. The crystal does not represent either category, the scheduling policies cannot inspect them, and the growth rule treats both as empty sites. They are categories maintained by the observer ledger.

And yet under the tested scarcity regimes they do not respond identically. Reoccupation-related turnover is comparatively insensitive to starting scale; first occupation becomes more sensitive as scarcity deepens. That earns a bounded result:

> **Reuse and first occupation respond differently to computational scarcity under the tested conditions.**

And it gives us a stronger hypothesis worth carrying forward:

> **Staying and growing may be different computational problems.**

Operationally, in this substrate. Not biologically.

The interesting point is where the distinction came from. First occupation versus reoccupation began as bookkeeping — a way for the laboratory to classify events the crystal itself could not distinguish. Under scarcity, that observer-side distinction separates two different measured responses. That is worth keeping. It is not yet an ontology.

---

## What Does It Cost to Stay?

The chapter's title can now be answered, but the answer is not a substance. The scarce quantity **imposed by these experiments** is evaluation opportunity.

A candidate attachment can occur only if the candidate receives an evaluation, and under a binding budget, evaluating one candidate can mean another eligible candidate receives none on that update. That is a genuine opportunity cost in the formal sense. It requires no agent deciding to spend anything — only more eligible opportunities than available evaluations.

Reduce the budget and the population reached within the tested horizon changes dramatically. Hold the budget fixed and change support-biased scheduling, and the material future changes with it. The bounded claim is:

> **Finite evaluation opportunity strongly changes the population reached by the lossy Digital Crystal, and support-biased scheduling at fixed budget strongly changes reoccupation and the resulting material future. The experiments did not isolate a pure reuse-versus-expansion allocation effect.**

Biology pays for action through physical resource constraints, and that comparison will remain tempting. Resist it a little longer. What this substrate has exposed is a different primitive: a per-update bound on how many possible transitions can receive computation. It is not stored fuel, not an internal resource variable, not metabolism. It is simply a limit on action.

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

The first failure told us that finite scheduling effects are not a tidy two-sided exchange between reuse and expansion. The second told us that no tested budget met the frozen operational criterion for stationary population with continuing turnover. The third told us that even normalized process components do not all respond identically to starting scale.

And one apparent positive result weakened under inspection. The near-constant gross-turnover fraction of `~0.171` looked at first like an emergent stable process variable, and the accounting audit showed that much of that stability is mechanically induced by the fixed loss rate, the update order, the normalization convention and the small net drift.

That correction matters. A stable measurement is scientifically interesting only to the extent that its stability is not already forced by the parameters used to generate it.

Here, much of it was.

What remains is simpler. Finite evaluation means not every eligible transition is considered. Scheduling changes which opportunities receive computation. The same budget can therefore produce different material futures. And reoccupation and first occupation do not respond identically under severe scarcity.

That is enough.

---

## Experimental Note

All three experiments in this chapter run on the same lossy Digital Crystal substrate at a loss rate of `δ = 0.08`.

### V1 — Finite-Budget Allocation

The V1 quick profile used 48 independent groups at radius 72, with a warmup of 14 updates, 48 updates of continuation, a late window of the final 12 updates, and a primary budget of `B = 256`.

The neutral budget characterization tested `B = 64, 128, 256, 512, 1024, 2048` together with an unbounded reference. The main-text table stops at `B = 1024` because the scientific point concerns the binding part of the sweep; `B = 2048` remains in the complete experimental record as an additional non-binding reference.

The scheduling policies used current occupied-neighbour count together with keyed deterministic scheduling noise, and could not inspect occupancy history. Because occupied-neighbour count also enters the attachment rule, this experiment does not isolate reuse-versus-expansion allocation independently of local support. No support-matched scheduling control was run.

Two frozen primary magnitude gates were required for the two-sided tradeoff hypothesis: a high-support minus low-support reoccupation advantage of at least `0.15` reoccupations per loss, and a low-support minus high-support first-occupation advantage of at least `100` first occupations per 1000 evaluations. Both were required.

### V2 — Stationary Population With Turnover

V2 used 96 independent groups at radius 72, with a warmup of 14 updates, 72 updates of continuation, a late window of the final 20 updates, and neutral scheduling only, across `B = 48, 64, 80, 96, 128`.

For each run, late normalized population slope was obtained by fitting a line to population over the late window and dividing that slope by mean population over the same window. A candidate budget had to satisfy every frozen population, activity, turnover and capacity gate. No budget could be added after inspecting the V2 results.

### V3 — Normalized Process Components

V3 used 48 independent groups per condition at radius 72, with 72 updates of continuation and a late window of the final 20 updates, across `B = 48, 64, 80, 96, 128` and three starting scales set by warmup length: small at 8 updates, medium at 14, large at 20.

For every late-window update, each process count was divided by the post-loss population:

```text
loss fraction              losses / post-loss population
attachment fraction        attachments / post-loss population
reoccupation fraction      reoccupations / post-loss population
first-occupation fraction  first occupations / post-loss population
gross-turnover fraction    (attachments + losses) / post-loss population
```

Growth occurs before loss. That update order is what makes the accounting audit in the main text work.

Every normalized process metric at every budget was required to hold a CV across starting sizes at or below `0.10`. Gross turnover additionally required a between-budget CV at or below `0.10`, an absolute late temporal slope at or below `0.0025`, and a gross-turnover fraction of at least `0.05`. All gates were required. The complete process-invariance hypothesis failed because first occupation exceeded the start-size CV limit at `B = 48`.

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

We have been calling this *the crystal* since *The Digital Crystal*. But several easy candidates for what that noun might denote have now failed us. It is not a fixed collection of material, not a fixed morphology, not a stationary population, and not a permanently fixed geometric interface.

Something continues through all of those changes, and what remains is the continuing dynamics. But we have not yet shown whether those dynamics belong to one causally privileged region. Connected geometry is not enough. Turnover is not enough. A computational budget is not enough.

The next experiment has to ask whether the continuing dynamics form a causally coherent region with a natural boundary, or whether the noun *crystal* is imposing unity on something more diffuse.

> **Is there actually one causally coherent thing here?**
