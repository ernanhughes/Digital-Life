+++
title = "10: What Does It Cost to Stay?"
date = "2026-08-14T16:00:00+01:00"
draft = false
description = "Limit how many construction opportunities the Digital Crystal can evaluate per update and it never finds a stable size. What becomes stable instead is the traffic flowing through it."
weight = 10
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Scarcity", "Turnover", "Computation", "Experiments"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with an impressive number and a suspicion about it.

More than ninety-three percent of everything the crystal lost came back, usually within a step or two, through nothing more than the ordinary growth rule encountering ordinary empty sites. No repair mechanism, no damage detector, no target shape.

But the crystal had never once had to decide whether rebuilding was worth doing. Every update, every eligible site received an attachment evaluation — the vacancies carved through its interior and the frontier at its outer edge, all of them, simultaneously. Reoccupation was cheap because nothing else was competing for the chance to happen.

So this chapter removes that luxury, and it removes it in the smallest possible way.

---

## Not Everything Gets Evaluated

Instead of evaluating every eligible frontier site, the process may evaluate at most:

```text
B
```

candidate sites per update. A site that is not evaluated simply gets no attachment attempt on that step. It is not blocked, not penalized, not remembered; the opportunity passes and may return next update.

Nothing else changes. The attachment probability is what it always was. The loss rule is what it was in Chapter 7. The crystal gains no new internal state whatsoever — no energy, no fuel, no resource counter, no metabolism variable, no maintenance controller, no target size, no record of what has been neglected.

```text
many possible transitions
↓
only B may be evaluated
```

That is the whole modification, and it is worth being precise about what kind of constraint it is. `B` is not the crystal's energy. It is a bound on how much of the currently available transition structure can be processed in one update. If that later resembles the way physical resource limits constrain biological action, that is a comparison to be drawn carefully, not an identity to be assumed. The point of this chapter is that scarcity turns out to matter enormously **without** having to pretend computation is ATP.

---

## The Budget Sets the Scale

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

The scale of the process is strongly constrained by the amount of computation available to it.

Across the binding part of the sweep, increasing the evaluation budget produces a large increase in late population. A sixteen-fold change in budget corresponds to roughly a nine-fold difference in scale.

That the curve flattens somewhere above `B = 512` is unsurprising: past some point the budget stops binding, because there are not that many eligible sites to evaluate. The exact ordering at the top end is not worth interpreting. What matters is the bottom end, where the crystal at `B = 64` is not a slower version of the unlimited crystal. It is roughly a tenth of the size, indefinitely.

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

Each policy sees only current local geometry. None of them can inspect the occupancy ledger. None of them knows whether a site is new territory or a place that used to be occupied and was lost — that distinction remains, as it was in Chapter 7, entirely observer-side.

But current geometry carries statistical consequences of how a site arose.

Reoccupation candidates often sit inside more occupied local neighbourhoods than candidates at the outer frontier.
 So support-biased scheduling can indirectly shift evaluation opportunity between reoccupation-like and expansion-like candidates without ever reading the observer's occupancy history.

That is exactly what makes the experiment interesting.

That is the mechanism worth watching. If the allocation shifts, it will shift because of local geometry, not because we told anything to prefer repair.

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

The same evaluation budget, allocated differently, produces late populations differing by roughly seventy percent — and even changes the sign of late net growth.

```text
SAME COMPUTATIONAL BUDGET
≠
SAME MATERIAL FUTURE
```

Under high-support scheduling, reoccupation runs at roughly `0.96` events per loss.

Under low-support scheduling it falls to roughly `0.53`.

The scheduling rule does not know what reoccupation is, yet it changes it dramatically.
 Neither policy knows that anything was ever lost.

---

## But the Predicted Tradeoff Fails

The hypothesis had been more specific than *allocation matters*. It predicted a clean two-sided tradeoff: high-support scheduling should meaningfully increase reuse, **and** low-support scheduling should meaningfully increase expansion, each clearing a magnitude threshold fixed in advance.

The first arm passed comfortably:

```text
high-support reoccupation advantage    ≈ 0.425     required 0.150
```

The second did not:

```text
low-support first-occupation advantage ≈ 61.6      required 100
                                       (per 1000 evaluations)
```

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

That raised a stronger question.

Which revives a hypothesis that failed in Chapter 7 for reasons that may no longer apply. Material loss alone did not produce a finite sustainable size, because loss manufactured the very opportunities that replaced it. But loss plus a ceiling on how many of those opportunities can be serviced is a different situation entirely. Now the replacement mechanism has a hard limit.

> **Is there a finite budget at which population becomes approximately stationary while material turnover continues?**

That is a much stronger claim than *growth becomes slow*, so it needed gates that a trivially stationary system could not pass. A qualifying regime had to keep a nonzero population, hold a late population slope near zero, and continue to exhibit loss, reoccupation, first occupation and substantial gross turnover, all without approaching simulation capacity. Freezing on death does not count. Freezing against the wall of the world does not count. We wanted approximately stationary population together with continuing material turnover.

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

At `B = 80`, the measured slope was `-0.00252` against a frozen limit of `±0.00250`.

Close enough to tempt reinterpretation.

Not close enough to pass.

We could now search neighbouring budgets, adjust the late window, or redefine `B = 80` as effectively stationary.

Every one of those would be a new analysis chosen after seeing the result.

So we do none of them.

```text
FAILED
```

The crystal was not stationary. It was very slowly declining, at every budget we had committed to testing.

---

## The Wrong Kind of Stability

But the five failing budgets were failing in a peculiar way.

Their absolute populations differed substantially.

Yet their normalized decline rates were similar, and one quantity was more stable still: gross material turnover as a fraction of population remained close to `0.17` per update across the entire budget family.

Different scale.

Remarkably similar proportional traffic.

Which raises an uncomfortable possibility about the experiment we had just run. We had asked whether population would become stationary because population was the obvious candidate state variable.

The experiment suggested that another class of quantities might be more stable than population itself.
 The substrate had been answering a different question all along, in a quantity we had been treating as a diagnostic.

> **Is population the thing that should have been stable?**

---

## Stable Size Is Not Stable Process

Chapter 7 forced a distinction between a stock and a flow: net population change versus gross material turnover, with more than ninety percent of the crystal's activity invisible in the former.

This is the same distinction arriving with an additional twist. There, the flow was larger than the stock suggested. Here, the flow is *steadier* than the stock — and steadier across conditions that change the stock by a factor of three.

```text
STABLE STOCK
≠
STABLE NORMALIZED FLOW
```

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

The claim was demanding: every flow, at every budget, had to stay within a frozen sensitivity threshold across starting sizes.

---

## Turnover Barely Moves

The gross turnover result is the most striking measurement in this chapter.

```text
B = 48     0.17229
B = 64     0.17150
B = 80     0.17066
B = 96     0.17147
B = 128    0.17132
```

The coefficient of variation across those budget means is:

```text
0.0030
```

Three tenths of one percent, across a budget family that produces populations differing by a factor of three. And the quantity is not merely similar across budgets; it is nearly flat within each run. The worst late temporal slope across the family was around `0.00024`, against a frozen tolerance of `0.0025` — an order of magnitude inside it.

Starting size barely matters either. At `B = 48`:

```text
small     0.17330
medium    0.17267
large     0.17089
```

Loss fraction, attachment fraction and reoccupation fraction cluster the same way, at this budget and the others.

Across these tested starting sizes and budgets, gross material-event traffic remains close to the same fraction of population per update.
 Absolute population is changing.

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

## Two Processes Hiding Inside One

Sort the measurements by how they behaved.

```text
RELATIVELY STABLE ACROSS TESTED CONDITIONS
loss fraction
reoccupation fraction
gross turnover fraction
total attachment fraction

MORE SENSITIVE UNDER SEVERE SCARCITY
first-occupation fraction

```

The cleanest asymmetry is between:

```text
REOCCUPATION
```

Call them **continuation** and **expansion**, with the caveat that continuation here means nothing more than ongoing turnover and reuse within existing structure. It is not self-maintenance, and nothing is being maintained on purpose.

Under the tested scarcity regimes, reoccupation-related turnover is comparatively stable across starting scales and budgets.

First occupation is more sensitive, especially under the harshest scarcity.

So continuation and expansion respond differently to finite computation.

> **Staying and growing are not the same computational problem.**

Operationally, in this substrate — not biologically. And note where the distinction came from. The scheduling policies cannot see it; they sort by neighbour count. The growth rule cannot see it; it treats every empty site alike. Chapter 7 introduced first occupation versus reoccupation as an observer's bookkeeping device, a way for us to classify events the crystal cannot distinguish. This chapter finds that the two categories respond differently to a constraint neither of them knows about.

The observer-side distinction introduced for bookkeeping has turned out to separate two dynamical responses.

---

## What Does It Cost to Stay?

The chapter's title can now be answered, and the answer is not a substance.

The measured cost of continuing is **evaluation opportunity**. A candidate attachment can only occur where computation is spent on it, and under a binding budget, spending computation on one site means not spending it on another. Evaluating one candidate can therefore mean leaving another unevaluated on that update.

That is a genuine opportunity cost created by finite computation.

Reduce the allowance and the scale of the process falls with it. Change how it is divided and the balance between reuse and expansion moves. Neither effect requires the crystal to know anything, want anything, or hold any resource.

The bounded claim:

> **Continued material turnover in the lossy Digital Crystal depends strongly on finite computational opportunity, and the allocation of that opportunity changes whether construction tends toward reuse of previously occupied locations or occupation of new territory.**

Biology pays for action through physical resource constraints, and that comparison will be tempting for the rest of the book. Resist it a little longer. This substrate has exposed a different primitive: a per-update limit on how many possible transitions can receive computation.

It is neither stored fuel nor an internal resource variable.

It is simply a bound on action.
 Whatever digital life turns out to require, it is worth knowing that a hard constraint on action can exist without energy having to be invented.

---

## What Survived the Three Tests

Three increasingly simple descriptions failed:

```text
finite computation
↛ clean symmetric stay/grow tradeoff

finite computation
↛ stationary population

normalized process
↛ complete invariance
```

One honest caution before this becomes a principle. The near-constant turnover fraction may be less mysterious than it looks. The loss rate is frozen at `δ = 0.08`, and Chapter 7 established that lost sites are reoccupied rapidly and almost universally. A system losing a fixed fraction of itself and putting most of it back promptly will produce a turnover fraction in the neighbourhood of that loss rate more or less mechanically. The stability is real and measured. Its explanation is open, and the audit that would settle it — comparing observed turnover against the turnover mechanically expected from the loss rate and the known replacement dynamics — has not been run.

That distinction matters more here than almost anywhere else in the book. A stable measurement is scientifically interesting only to the extent that its stability is not already forced by the parameters used to generate it.

Until that subtraction is done, `0.171` is a strikingly stable measurement and not yet a law.

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
| Gross normalized turnover is stable across budgets | **MEASURED** | `0.17066–0.17229`; CV `0.0030`; worst late slope `0.00024` |
| Loss, attachment and reoccupation fractions are start-size insensitive | **MEASURED** | tightly clustered across small/medium/large starts |
| First occupation is start-size insensitive under severe scarcity | **FAILED** | CV `0.118` at `B=48` against maximum `0.100` |
| The complete normalized process vector is invariant | **FAILED** | one metric at one budget breaks the frozen criterion |
| Continuation and expansion respond differently to scarcity | **SUPPORTED** | stable turnover flows versus contingent first occupation |
| Turnover stability reflects a substrate law rather than the loss rate | **UNTESTED** | observed-minus-expected audit not yet performed |
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

We have been calling this *the crystal* since Chapter 4.

But it is no longer obvious what that noun refers to.

Not a fixed collection of material.

Not a stable size.

And, after material loss, not even a permanently fixed geometric interface.

Something continues.

We have not yet shown what its natural boundary is.

Connected geometry is not enough to answer that question.

Neither is turnover stability.

The next experiment has to ask directly whether the continuing dynamics form a causally coherent region with a natural boundary, or whether our noun is imposing unity on something more diffuse.

> **Is there actually one causally coherent thing here?**
