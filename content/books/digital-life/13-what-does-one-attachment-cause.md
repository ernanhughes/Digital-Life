+++
title = "13: What Does One Attachment Cause?"
date = "2026-08-14T20:00:00+01:00"
draft = false
description = "Force one cell to attach, prevent it in the counterfactual, and measure everything else. The immediate effect matches the local rule; persistent occupancy produces larger finite-horizon consequences, while transient accumulation does not continue."
weight = 13
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Intervention", "Experimental Method"]
series = ["Digital Life From First Principles"]
+++

The last chapter took away the body's privilege.

Two supplied spatial boundaries failed to earn causal privilege. Comparable same-side localization appeared at both tested radial cuts, but under a local update rule and an eight-update horizon that was not evidence of an individual hiding inside either one.

So stop drawing the object first.

Start with an event.

One event.

What does it cause?

That question turns out to conceal several different causal claims.

This chapter is the attempt to force them apart.

---

## Does Activity Propagate?

The first instinct, having lost the body, is to look for something else with an outline.

If connected material is not yet an earned experimental object, perhaps the activity itself has spatial organization — something that propagates through the construction interface and generates a recognizable distance-lag structure as it goes.

That is testable. If activity genuinely propagates, then activity near one location at time `t` should predict activity farther away at later times, in a structured way:

```text
near distance  →  early lag
far distance   →  later lag
```

A moving ridge through space and time.

So we built an event field from material-changing events and measured future event density by distance and lag.

Each source event was compared with matched non-event locations sharing local geometric context, and a cross-run control was added because ordinary developmental progression could generate a distance-lag pattern without anything propagating from the source event.

The frozen primary statistic asked whether the lag of excess activity shifted outward with distance strongly enough to clear its declared gate.

It did not.

```text
PROPAGATION CLAIM
FAILED
```

Two secondary shape statistics nevertheless looked suggestive: distance and estimated ridge lag were positively associated.

That made the underlying distance-lag surface worth inspecting.

It did not make the failed primary claim positive.

Then we looked at the surface itself.

---

## The Estimator Invents a Wave

At distance one, the real event field had a small positive excess at the first lag and negative excess afterwards. The statistic weighted positive values only, so its centroid collapsed onto lag one.

At larger distances there was no real structure — just weak noise scattered across the lag grid. Weight noise positively and average it and you get a centroid somewhere in the middle of the grid.

Put those two facts together and the estimator reports:

```text
distance 1     →  early lag
far distances  →  middle lags
```

which is exactly the shape of a ridge moving outward. There was no ridge. There was one strongly anchored near-distance row and a field of noise, and the measurement device turned that into apparent motion.

The danger is obvious in retrospect. A statistic designed to summarize a travelling ridge produced the expected shape even when the underlying surface contained no travelling ridge.

A positive result on that statistic could therefore have become a result about the estimator rather than the Crystal.

> **An estimator can manufacture the shape of the phenomenon it was designed to summarize.**

There is a second lesson buried in the same failure. The strongest structure in the surface was not positive at all. It was a persistent negative band at short range.

The positive-only estimator had discarded it before inference began.

So the instrument had made two mistakes at once:

```text
noise acquired the shape we were looking for

AND

real signed structure was removed
because it had the wrong sign
```

So we closed the propagation claim, kept the signed structure the estimator had been suppressing, and looked at it directly.

---

## Look at the Signs Instead

Separating events by type and keeping the sign gives a much simpler picture — but only after removing a confound sitting at the origin.

At distance zero, a source and its control are definitionally different states. An attachment source is occupied where its control is empty; a loss source is empty where its control is occupied. Those differences mechanically determine what can happen at that same site later. They are not neighbourhood dynamics at all, and including them contaminates everything.

Exclude distance zero and a much simpler neighbourhood pattern remains.

At distances one and two, the observational signed analysis showed:

```text
ATTACHMENT  →  MORE nearby attachment
LOSS        →  LESS nearby attachment
```

with the strongest signed differences concentrated at the shortest tested neighbourhood distances.

These are observational associations.

The attachment side is tested causally below.

No equivalent forced-loss intervention is performed in this chapter.

That is the wrong sign for the simple source/sink interpretation we had been carrying.

But it is exactly the sign predicted by the ordinary local attachment rule.

---

## The Rule Already Predicts This

The attachment rule rewards occupied neighbours. That term is positive. So:

```text
x attaches
↓
nearby empty cells gain an occupied neighbour
↓
their attachment probability rises
```

and symmetrically, a cell disappearing lowers the probabilities around it.

The observation is precisely what the rule says should happen. Which is almost embarrassing as a discovery, and exactly why it needs an intervention rather than an observation.

Because the observational version has a serious confound: the sites that actually attached were not randomly chosen. They attached because they were probable, which means they already sat in favourable local geometry, which means their neighbourhoods may have been on their way somewhere regardless. Correlating what happened after real attachments with what happened after matched non-attachments cannot fully separate the attachment's effect from the conditions that produced it.

So stop watching. Intervene.

---

## Force One Attachment

Take a checkpoint. Take one eligible frontier cell `x`. Take the same environment and the same cell-keyed randomness from the *The Crystal Gets a Past* chapter. Then split the future:

```text
FORCE      x attaches
PREVENT    x does not attach
```

and measure everything **except `x` itself**.

That exclusion is the whole design. We are not asking whether two states that differ at `x` still differ at `x` later — that is trivially true and tells us nothing. We are asking what happens *around* `x` because the state at `x` was changed.

One more thing before looking at any outcome: calculate what the frozen rule mechanically predicts the immediate neighbouring effect should be.

For each affected neighbouring candidate, compute its attachment probability in the FORCE branch and in the PREVENT branch before any Bernoulli draw is taken.

Summing those probability differences gives:

```text
g_mech_1
=
mechanically expected neighbouring
construction difference at lag one
```

Then measure the corresponding realized difference in neighbouring attachment outcomes:

```text
g1
=
realized neighbouring
construction difference at lag one
```

For the first time in the book, zero is not the most informative benchmark. The frozen mechanism itself predicts a specific nonzero effect.

This matters more than it sounds. Almost every experiment in this book has compared a measurement against zero. Here the mechanism already predicts a specific nonzero value, so zero is the wrong benchmark. The real question is not *did something happen* but *did what happened match what the rule says should happen*.

---

## The First Effect Matches the Mechanics

```text
mechanically expected one-step gain     g_mech_1 ≈ 0.105
realized one-step neighbouring gain     g1       ≈ 0.115
```

The discrepancy interval included zero and stayed inside the frozen accounting tolerance. A later fresh-seed experiment replicated it:

```text
g_mech_1        0.0883    [0.0676, 0.1095]
g1              0.1016    [0.0677, 0.1380]
g1 − g_mech_1   0.0132    [−0.0160, 0.0411]
```

```text
CONSISTENT WITH MECHANICS
```

> **Forcing one eligible frontier attachment causes additional neighbouring construction on the next update, at a magnitude consistent with the frozen local attachment rule.**

This is an unusually clean causal result.

We have a controlled intervention, a fresh-seed replication, and an immediate effect whose measured magnitude is consistent with the effect predicted by the frozen rule.

The result is valuable precisely because no additional one-step amplification needs to be invoked to explain it.

Everything that follows is about what happens after the first update, where the accounting stops being easy.

---

## Then the Futures Keep Separating

Ten updates after the intervention, the cumulative construction difference was around:

```text
G_10 ≈ 0.58
```

That is a descriptive finite-horizon total.

Only part of it appeared at the first step, so the FORCE and PREVENT branches continued to accumulate differences after the immediate mechanical effect.

It was tempting to call that accumulation a cascade — one attachment causing others, which cause others, and so on.

The two-branch experiment could not yet justify that interpretation.

It was also tempting to compare 0.58 against the obvious reference value of one additional event per initiating event, note that it sits below, and start reaching for vocabulary about branching and subcriticality.

But there is a confound sitting in the middle of the design, and it is the same shape as the confound that ruined the surface-versus-interior comparison in the *Can Experience Change the Material?* chapter.

In the FORCE branch, `x` is still there. It did not merely happen; it remains occupied, and it goes on being an occupied neighbour to everything around it on every subsequent update. So the accumulating difference could be either of two quite different things:

```text
a free-running cascade
    the consequence propagating on its own

or

the continuing consequence
    of one cell being permanently different
```

Those are not the same phenomenon, and the experiment as built could not tell them apart.

---

## Remove the Cause

The fix is a third branch.

```text
PREVENT      x does not attach

PERSISTENT   x is forced to attach, then remains under normal dynamics

TRANSIENT    x is forced to attach, gets one full causal update,
             and is then removed
```

The transient arm is the critical control.

It allows the forced attachment to influence one complete subsequent update. Then the initiating occupancy difference is removed.

From that point onward, any remaining divergence has to be carried by consequences already created downstream rather than by the continued presence of `x`.

> **Can a causal consequence sustain itself after the material difference that started it is gone?**

That is a far better question than asking whether FORCE and PREVENT still differ later. It also required a correction to the intervention timing: force and prevent now happen inside the canonical growth update, with the ordinary loss step applied to every branch afterwards, so that the forced cell faces the same background loss as any other newly attached cell.

The fresh-seed run used 96 independent groups and 384 interventions across four predeclared frontier-probability strata, with the observation window extended to thirty updates.

---

## The Transient Accumulation Stops Growing

```text
G_transient(30)   0.198    [−0.026, 0.440]
```

More informative than the total is the late-time rate. Across updates 21 through 30:

```text
transient late gain   −0.0081 per update    [−0.0201, 0.0039]
```

which passed the frozen practical-convergence criterion. Within the tested late window, the transient branch shows no continuing positive accumulation rate.

The late accumulation rate satisfies the predeclared practical-convergence criterion.

That earns a narrower statement:

> **Once the initiating occupancy is removed, no continuing positive accumulation rate is established over the tested late window.**

A residual branch difference may remain.

What the experiment rules out under this criterion is continuing positive accumulation, not the existence of every downstream difference.

The thirty-update transient total also sits below the descriptive reference value of one, and it is worth stating plainly what we are *not* saying. This is not a branching ratio. We have not established subcriticality, criticality, or any position relative to a phase transition. Those terms come from theories with structure this experiment has not tested — a branching ratio presumes a well-defined offspring distribution, and we have measured a construction difference under one intervention, one horizon and one substrate. The number is below one. That is all it means.

---

## Leave the Cause in Place

The persistent arm behaves very differently.

```text
G_persistent(30)                  1.164    [0.786, 1.542]
G_transient(30)                   0.198
difference                        0.966    [0.612, 1.333]
```

The thirty-step consequence is substantially larger when the initiating state difference remains present than when it is removed after one causal update.

```text
PERSISTENT STATE DIFFERENCE
≠
TRANSIENT CAUSAL CASCADE
```

This is the same lesson the *Can Experience Change the Material?* chapter taught about material traces, arriving now at the scale of a single cell. There, persistent material mattered while it stayed coupled to the interface, and the persistence was doing the work rather than any propagating consequence. Here, the continued state difference carries substantially more cumulative consequence than the transient residue left after that difference is removed.

But persistent does not mean permanent, and the obvious next interpretation dies too. If keeping `x` gave the branch a standing growth advantage, cumulative gain would rise roughly linearly with horizon forever. It does not:

```text
H=1     0.156
H=5     0.539
H=10    0.839
H=17    1.008
H=22    1.190
H=30    1.164
```

and the late-window rate was:

```text
persistent late gain   0.0057 per update    [−0.0159, 0.0281]
```

An interval spanning zero, far below the predeclared offset threshold. The persistent trajectory rises early, flattens, and then wanders. No permanent positive growth offset was established.

So under this intervention and thirty-update horizon, one attachment produces:

```text
an immediate mechanically accounted effect
↓
a transient downstream difference
whose positive accumulation stops
under the late-window criterion
↓
a substantially larger cumulative consequence
when the initiating state remains present
```

Neither branch established a permanent positive growth-rate offset.

---

## Four Different Claims

It is worth separating what has now become four distinct causal statements, because ordinary language collapses them into "the attachment mattered":

DIRECT MECHANICAL EFFECT
measured and consistent with the frozen rule

TRANSIENT DOWNSTREAM CONSEQUENCE
measured; no continuing positive late accumulation established

CONSEQUENCE OF PERSISTENT STATE
measured; substantially larger over the tested horizon

PERMANENT GROWTH-RATE CHANGE
not established

Only the first three have evidence. They are not interchangeable, and an experiment that measures one and reports another — which is what the ten-update version was doing — will get the story wrong in a way no amount of extra precision would fix.

---

## The Same Attachment Changes Opportunity Differently

One more result from the intervention runs, and it is the one that generates the second half of the chapter.

The four probability strata sit in visibly different geometry. The lowest-probability probes were sparse sites — mean baseline attachment probability around 0.372, with almost exactly one occupied neighbour. The highest-probability probes were dense — baseline around 0.798, with roughly 4.07 occupied neighbours.

Force an attachment in those different geometries and the immediate effect on frontier opportunity changes sign.

```text
                            SPARSE      DENSE

newly promoted frontier      2.23        0.031
total frontier change       +1.23       −0.969
```

At a sparse interface, occupying one cell gives several previously unsupported empty neighbours their first occupied neighbour, and new frontier appears. At a dense interface, almost everything nearby is already occupied or already eligible, so the only substantial change is that the focal site itself leaves the frontier — the attachment consumes opportunity rather than creating it.

The paired difference in frontier creation was about 2.20 sites, interval [1.99, 2.41], `p = 0.000125`.

> **The same one-cell attachment can create or consume very different amounts of immediate frontier opportunity depending on local geometry.**

That result is established under the frozen frontier measurement.

It immediately suggests a stronger question: does that immediate opportunity transformation predict what the intervention causes later?

---

## But Geometry Did Not Predict Long-Run Gain

The obvious stronger hypothesis is that sites creating more immediate frontier opportunity should also produce larger downstream causal consequences.

The point estimates encourage it:

```text
sparse probe    G_transient(30) ≈ 0.677
dense probe     G_transient(30) ≈ 0.073
```

The predeclared paired comparison does not:

```text
difference   0.604    [−0.031, 1.271]    p = 0.0777
```

and the persistent-arm version is worse still (difference 0.156, `p = 0.810`).

So we have established that sparse and dense geometry differ, and we have *not* established that sparse geometry produces reliably higher long-run gain. The point estimates make the relationship interesting. They do not make it true.

---

## Surely We Can Map Causal Gain

The immediate geometric contrast is strong enough to motivate a more ambitious hypothesis:

> **perhaps downstream causal consequence can be predicted from local state before the intervention occurs.**

If so, causal leverage might be predictable across the frontier rather than measured only after intervention.

That is an attractive hypothesis.

If a reproducible relationship survived prospective testing, we could construct an observer-side map assigning different predicted consequences to different frontier locations.

But the map would remain a measurement model.

The crystal would not thereby be shown to contain or represent a scalar quantity called causal leverage.

The natural candidate is the geometric one:

```text
FCP(x) = |frontier after forcing x occupied| − |frontier before|
```

Frontier Creation Potential — positive when occupying `x` creates net opportunity, negative when it consumes it. An observer-defined quantity, not energy, not fitness, nothing hidden. And the hypothesis writes itself:

> **Sites that create more frontier opportunity produce more transient causal gain.**

---

## Three Attempts, and What They Could Actually Resolve

The first FCP experiment looked promising and could not answer the question. With 48 groups, the high-minus-low transient gain came out at:

```text
+0.167    [−0.078, +0.431]
```

against a declared meaningful effect of `+0.15`. An interval that wide cannot distinguish an effect at that scale from nothing, in either direction. That is not a failed hypothesis; it is an experiment without the precision to test the hypothesis it declared. The distinction matters enormously, and reporting it as a negative result would have been a straightforward misrepresentation.

> **A missed significance gate is not a negative result unless the experiment could have resolved the effect it said mattered.**

The second attempt asked whether FCP was simply too compressed a description. A frontier cell on the hexagonal lattice has six neighbours, each occupied or empty, so the exact ring is six bits. Perhaps the precise arrangement matters in ways a scalar count destroys. That experiment was even less precise — a primary interval half-width around 0.50 attachments against a declared effect of 0.20. Inconclusive again.

It did expose a design problem worth keeping. The comparison matched tightly on baseline attachment probability, but the frozen rule computes attachment probability *from* local exposure geometry. Conditioning on it holds fixed one of the main pathways through which geometry could act, converting a broad question into a narrow one about residual effects. A control is not automatically conservative.

If it conditions on a variable lying on the causal pathway under investigation, it can remove part of the mechanism the experiment was supposed to measure.

The third attempt moved from geometry to process history. Two sites can look identical now and have arrived there through very different recent activity, so this compared high and low recent turnover while matching present local state. The manipulation was large — about 7.73 events of difference — and the transient-gain difference was:

```text
−0.065    [−0.221, +0.096]
```

whose positive side genuinely excludes the declared `+0.15`.

But the scope of that result is narrower than it looks, and the reason is structural. Persistent material modification was disabled in that substrate, so the operative dynamics were determined by current occupancy, current input and keyed randomness. Past turnover could only influence the future through the present state it had already produced — and the present state was exactly what the matching held fixed. That experiment asked whether recent turnover proxies for present information the matching missed. It is not a test of whether history can matter in a substrate built to carry it.

---

## Stop Searching Features

At this point the path forward is obvious and wrong. Bigger motifs. A longer history window. A learned predictor over some richer feature set. Keep going until something correlates with gain.

That procedure has no stopping rule and produces no knowledge, and we have declined it twice already — after the placement experiments in the *Can Experience Change the Material?* chapter and the budget experiments in the *What Does It Cost to Stay?* chapter. So instead of another feature, rebuild the measurement.

The reset kept the frozen crystal and the FORCE/PREVENT intervention and changed what was measured. Rather than starting from the noisy realized cascade, start from the rule: for every candidate, compute the attachment probability in each branch and take the difference, before any Bernoulli draw turns those probabilities into a single bit. A realized attachment discards almost all the information the rule provides; the expected construction difference keeps it.

The contrast was made extreme:

```text
HIGH
FCP ≥ +2

LOW
FCP ≤ −1

minimum pair difference
ΔFCP ≥ 3
```

Pairs were matched on occupied-neighbour count and radial band.

They were deliberately **not** matched on baseline attachment probability or local frontier density, because those variables may lie on the pathway through which geometry acts.

The run requested 384 independent groups.

Of those, 275 contained at least one usable extreme matched comparison:

```text
coverage = 275 / 384 = 71.6%
```

Across those supported groups, the design produced 471 extreme pairs.

This time the precision was adequate: an achieved minimum detectable effect around 0.047 against a declared meaningful effect of `+0.10`. And the result was:

```text
ΔE1 = −0.0026    [−0.0395, +0.0333]
```

> **Under this protocol, even an extreme difference in Frontier Creation Potential did not produce the predeclared scientifically meaningful positive difference in expected lag-one local construction.**

That is a bounded negative, not another inconclusive run.

But it resolves a **different endpoint** from the earlier FCP experiments.

The earlier tests asked whether local representations predicted realized finite-horizon transient gain.

This experiment asks whether an extreme FCP contrast predicts the expected **lag-one** local construction difference before Bernoulli realization.

Its bounded conclusion is therefore:

```text
UNDER THE EXTREME MATCHED FCP PROTOCOL

MORE FRONTIER CREATION
↛
THE PREDECLARED MEANINGFUL INCREASE IN
EXPECTED LAG-ONE LOCAL CONSTRUCTION
```

It does not retroactively resolve the earlier long-horizon FCP question.

---

## No Stable Local Predictor Yet

Put the two halves of the chapter together.

A local intervention has measurable causal consequences.

Its immediate neighbouring effect is replicated and quantitatively consistent with the frozen rule.

After the initiating occupancy is removed, no continuing positive accumulation rate is established over the tested late window.

When the initiating state remains present, the cumulative thirty-update consequence is substantially larger, but no permanent positive growth-rate offset is established.

And the same forced attachment can create or consume very different amounts of immediate frontier opportunity depending on local geometry.

What we could not establish was a stable local representation that prospectively predicted the causal outcomes we tested.

Three candidate descriptions were investigated:

```text
Frontier Creation Potential
exact local motif
recent local history
```

But they were not all tested against the same endpoint.

The first FCP test and the exact-motif test were too imprecise to resolve their declared transient-gain effects.

The recent-history experiment was precise enough to exclude its declared positive transient-gain effect, but only in a substrate with no independent history state once present geometry was matched.

The final extreme-FCP experiment asked a narrower question again: whether a large difference in immediate frontier creation produced a scientifically meaningful difference in **expected lag-one local construction**. It did not.

So we have not shown that downstream consequence is unpredictable.

We have shown that the tested local descriptions did not yield a stable predictive relationship across these predeclared endpoints.

But the word *gain* has been quietly encouraging a stronger picture than the experiments have earned.

It invites us to imagine that each frontier site carries a stable scalar property:

```text
this site has high causal gain
that site has low causal gain
```

waiting to be released by intervention.

The experiments do not establish that picture for any of the local representations we tested.

They establish causal consequences of interventions.

Whether those consequences can eventually be summarized by some stable response field remains open.

```text
intervention
↓
changes local occupancy
↓
changes which opportunities exist
↓
changes what gets evaluated
↓
changes some attachments
↓
changes later opportunities
↓
the difference dissipates, or goes somewhere
```

This makes an interaction-generated account plausible: the consequence may depend on what the intervention changes in the subsequent process rather than on a scalar property stored at the intervention site.

That is an interpretation to test, not yet a demonstrated mechanism.
 The analogy is useful if kept narrow: asking where the causal consequence is stored beforehand may be like asking where a traffic jam is stored before the interacting traffic produces it.

The safest version of the chapter's conclusion, and the one fully earned:

> **We found a causal effect before we found a stable local variable that predicts its downstream size.**

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Local process activity propagates as a distance-lag ridge | **FAILED** | primary statistic missed its gate; estimator shown able to manufacture the shape |
| The interface behaves as a loss-source / attachment-sink field | **FAILED** | neighbourhood signs opposite, once distance zero was excluded |
| Attachment raises, and loss lowers, nearby attachment at distances 1–2 | **SUPPORTED** | signed event analysis, decaying by distance 3 |
| Forcing one attachment causes additional neighbouring construction | **SUPPORTED** | replicated across two runs; `g1 ≈ 0.102` on fresh seed |
| The immediate effect matches the frozen local rule | **SUPPORTED** | discrepancy `0.0132`, interval `[−0.0160, 0.0411]` |
| The transient cascade sustains itself after the cause is removed | **FAILED** | late rate `−0.0081` per update, interval spanning zero |
| Persistent initiating occupancy produces a larger thirty-update cumulative consequence than the transient intervention | **SUPPORTED** | persistent-minus-transient difference `0.966`, interval `[0.612, 1.333]` |
| The persistent branch retains a positive late growth-rate offset | **FAILED** | late rate `0.0057`, interval spanning zero |
| Sparse and dense probe geometries differ in immediate frontier-opportunity transformation | **SUPPORTED** | sparse-minus-dense frontier-creation difference `2.20`, interval `[1.99, 2.41]`, `p = 0.000125` |
| Sparse geometry produces reliably greater long-run gain | **NOT ESTABLISHED** | difference `0.604`, `p = 0.0777`; persistent arm `p = 0.810` |
| Frontier Creation Potential predicts transient gain (first test) | **INCONCLUSIVE** | interval `[−0.078, +0.431]` against declared `+0.15` |
| Exact local motif predicts transient gain | **INCONCLUSIVE** | half-width `0.50` against declared `0.20` |
| Recent turnover predicts transient gain | **NOT SUPPORTED (narrow scope)** | `−0.065`, `[−0.221, +0.096]`; substrate had no independent history state |
| Extreme Frontier Creation Potential produces the declared positive increase in expected lag-one local construction | **FAILED** | `ΔE1 = −0.0026`, interval `[−0.0395, +0.0333]`; achieved precision sufficient to exclude the declared `+0.10` effect |
| Downstream consequence is unpredictable in principle | **NOT CLAIMED** | three representations tested, not all possible ones |
| Branching ratio, criticality, propagating wave, self-sustaining cascade | **NOT CLAIMED** | no such structure tested |

---

## Where Does the Difference Go?

There is one measurement left over, and it does not fit anywhere in this chapter.

Throughout the intervention runs we tracked causal gain twice: locally, around the intervention, and globally, across the whole crystal excluding the intervention site. For the persistent arm those measurements were approximately `1.164` locally and `1.036` globally. For the transient arm they were approximately `0.198` and `0.044`.

Their differences have intervals spanning zero.

So there is no established far-field causal effect here.

The unresolved local-versus-global comparison suggests one concrete mechanism worth testing next, but it does not establish it.

The selected candidate sets remained more than 99% overlapping between branches, so there is no evidence here of a wholesale rewriting of the global evaluation schedule.

The point estimates for global cumulative difference are smaller than the corresponding local estimates, but their local-minus-global differences have intervals spanning zero.

So we do not yet have evidence of a compensating far-field effect.

What we do have is a mechanism capable of producing one.

*What Does It Cost to Stay?* established that active candidates compete for a finite evaluation budget.

A local attachment can also change the frontier candidate set.

Those two facts create a specific causal possibility:

```text
local intervention
↓
changes candidate opportunities
↓
changes competition for finite evaluation
↓
could alter which distant candidates are evaluated
```

That possibility has not yet been tested directly.

Change the frontier and you change the candidate population competing for a fixed evaluation budget.

That creates a concrete route by which a local intervention **could** affect distant opportunities without any local causal chain connecting the two sites.

That possibility has not yet been tested directly.

The previous chapter failed to find a privileged enclosing body.

This chapter found a local causal effect but no stable local gain variable that predicts its downstream size.

Together, the results suggest one concrete mechanism worth isolating next: competition for the finite evaluation budget shared by active candidates.

> **Does competition for a shared finite evaluation budget create measurable causal effects between locations too far apart to interact through the local rule?**
