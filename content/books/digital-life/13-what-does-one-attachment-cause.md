+++
title = "13: What Does One Attachment Cause?"
date = "2026-08-14T20:00:00+01:00"
draft = false
description = "Force one cell to attach, prevent it in the counterfactual, and measure everything else. The immediate effect matches the local rule, retaining the initiating cell produces a larger finite-horizon consequence than removing it, and a negative construction difference appears beyond the local region."
weight = 13
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Intervention", "Experimental Method"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "review"
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

The discrepancy interval included zero and stayed inside the frozen accounting tolerance. The corrected fresh-seed experiment described below replicated it:

```text
g_mech_1        0.1027    [0.0782, 0.1276]
g1              0.1094    [0.0703, 0.1510]
g1 − g_mech_1   0.0066    [−0.0210, 0.0356]
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

In the first, two-branch version of this experiment, ten updates after the intervention the cumulative construction difference was around:

```text
G_10 ≈ 0.58
```

That is a descriptive finite-horizon total.

Only part of it appeared at the first step, so the FORCE and PREVENT branches continued to accumulate differences after the immediate mechanical effect.

It was tempting to call that accumulation a cascade — one attachment causing others, which cause others, and so on.

The two-branch experiment could not yet justify that interpretation.

It was also tempting to compare 0.58 against the obvious reference value of one additional event per initiating event, note that it sits below, and start reaching for vocabulary about branching and subcriticality.

But there is a confound sitting in the middle of the design, and it is the same shape as the confound that ruined the surface-versus-interior comparison in the *Can Experience Change the Material?* chapter.

In the FORCE branch, `x` was never taken away. It did not merely happen; it goes on being available as an occupied neighbour to everything around it on every subsequent update. So the accumulating difference could be either of two quite different things:

```text
a free-running cascade
    the consequence propagating on its own

or

the continuing consequence
    of one cell being left unremoved
```

Those are not the same phenomenon, and the experiment as built could not tell them apart.

---

## Remove the Cause

The fix is a third branch.

```text
PREVENT      x is held absent through the causal exposure

RETAINED     x is forced to attach and is not experimentally
             removed; its later fate follows ordinary dynamics

TRANSIENT    x is forced to attach, gets one full causal update,
             and is then removed
```

The transient arm is the critical control.

It allows the forced attachment to influence one complete subsequent update. Then the initiating occupancy difference is removed from both branches.

From that point onward, any remaining divergence has to be carried by consequences already created downstream rather than by the continued presence of `x`.

> **Can a causal consequence sustain itself after the material difference that started it is gone?**

That is a far better question than asking whether FORCE and PREVENT still differ later. Getting the experiment to actually ask it took two attempts.

An earlier version of this control left the PREVENT branch free to reacquire the focal cell during the first exposure, and deleted `x` from the transient branch only. The focal states were therefore not guaranteed equal when the measurement window opened, and on a minority of probes the control ended up holding the cell the treatment branch had just been stripped of — the intervention's own sign, reversed. Background loss could also destroy the forced cell before it had influenced anything.

The corrected intervention closes both routes. `x` is placed directly into the forced branches at the checkpoint, with no loss step before the exposure, so the intervention is always delivered. During the single exposure update, PREVENT removes `x` from the frontier before finite-budget selection, so it cannot attach. Immediately after that update, `x` is deleted from both the transient and the prevent branch and their agreement is asserted rather than assumed. From the next update onward neither branch treats `x` specially: it may reoccupy naturally in either, and when it does, that reoccupation is part of the downstream process rather than a failure of the control. Throughout, `x` itself stays excluded from every measured outcome.

Those three conditions are checked on every probe:

```text
FORCE present through the exposure      1.000
PREVENT blocked through the exposure    1.000
focal states equal after the exposure   1.000
```

The corrected fresh-seed run used 96 independent groups and 384 interventions across four predeclared frontier-probability strata, with the observation window extended to thirty updates.

---

## What Survives Removing the Cause

Two different questions live inside the transient arm, and the corrected experiment answers only one of them.

The first is whether any positive consequence accumulates at all:

```text
G_transient(30)   0.042    [−0.135, 0.216]
```

The interval spans zero. A positive thirty-update transient total is not established. Whatever residue remains after the initiating occupancy is equalized away is too small for this design to separate from nothing.

The second question is about the *rate*, and that one is answerable. Across updates 21 through 30:

```text
transient late gain   −0.0026 per update    [−0.0141, 0.0091]
```

which satisfies the frozen practical-convergence criterion.

> **After one controlled causal exposure and focal-state equalization, no continuing positive transient accumulation is established over the tested late window.**

Those are not the same result, and collapsing them would be an error in either direction. A total unresolved around zero is not a total shown to be zero. A late rate consistent with no continuing growth is not a claim that every downstream difference has vanished, or that the transient branch has returned exactly to PREVENT.

The thirty-update transient total also sits below the descriptive reference value of one, and it is worth stating plainly what we are *not* saying. This is not a branching ratio. We have not established subcriticality, criticality, or any position relative to a phase transition. Those terms come from theories with structure this experiment has not tested — a branching ratio presumes a well-defined offspring distribution, and we have measured a construction difference under one intervention, one horizon and one substrate. The number is below one. That is all it means.

---

## Leave the Cause in Place

The retained arm behaves very differently.

```text
G_retained(30)                    0.740    [0.294, 1.188]
G_transient(30)                   0.042
difference                        0.698    [0.299, 1.102]
```

The thirty-step consequence is substantially larger when the initiating cell is left unremoved than when it is deleted after one causal update.

```text
RETAINED STATE DIFFERENCE
≠
TRANSIENT CAUSAL CASCADE
```

This is the same lesson the *Can Experience Change the Material?* chapter taught about material traces, arriving now at the scale of a single cell. There, retained material mattered while it stayed coupled to the interface, and the retention was doing the work rather than any propagating consequence. Here, not removing the initiating cell carries substantially more cumulative consequence than the transient residue left after removal.

Retained is not the same word as permanent, and the experiment now measures exactly how far apart they are. `x` is not clamped occupied in this arm. It faces the same background loss as any other cell:

```text
updates x occupied, of 30        18.28    [17.54, 19.01]
occupancy fraction               0.609    [0.585, 0.634]
still present at update 30       0.445
```

So this is not a branch in which one cell stays different for thirty updates. It is a branch in which the experiment declines to remove that cell and lets ordinary dynamics decide the rest. The comparison is between removal and non-removal, not between presence and absence.

The behaviour after equalization is worth recording too. `x` reoccupies naturally in 88.5% of transient branches and 87.8% of prevent branches, first returning around update nine in both. Once the focal state is equalized, the site behaves almost identically in the two branches — which is what a working control should look like.

The obvious next interpretation dies as well. If not removing `x` gave the branch a standing growth advantage, cumulative gain would rise roughly linearly with horizon forever. It does not:

```text
H=1     0.039
H=5     0.448
H=10    0.646
H=17    0.875
H=22    0.898
H=30    0.740
```

and the late-window rate was:

```text
retained late gain   −0.0130 per update    [−0.0393, 0.0133]
```

An interval spanning zero with a negative point estimate, failing the predeclared positive-offset threshold. The retained trajectory rises early, flattens, and then declines. No permanent positive growth offset was established.

So under this intervention and thirty-update horizon, one attachment produces:

```text
an immediate mechanically accounted effect
↓
a transient downstream difference
whose positive total is unresolved
and whose late accumulation does not continue
↓
a substantially larger cumulative consequence
when the initiating cell is left unremoved
```

Neither branch established a permanent positive growth-rate offset.

---

## Four Different Claims

It is worth separating what has now become five distinct causal statements, because ordinary language collapses them all into "the attachment mattered":

DIRECT MECHANICAL EFFECT
supported; consistent with the frozen rule

POSITIVE TRANSIENT CUMULATIVE CONSEQUENCE
not established; the thirty-update interval spans zero

CONTINUING POSITIVE TRANSIENT ACCUMULATION
failed; the late rate satisfies the convergence criterion

CONSEQUENCE OF RETAINING THE INITIATING CELL
supported; substantially larger than the transient arm over the tested horizon

PERMANENT POSITIVE GROWTH-RATE OFFSET
not established

The fourth and fifth rows used to be one row, and so did the second and third. Splitting them is the whole benefit of the corrected control. An experiment that measures one of these and reports another — which is what the ten-update version was doing — will get the story wrong in a way no amount of extra precision would fix.

---

## The Same Attachment Changes Opportunity Differently

One more result from the intervention runs, and it is the one that generates the second half of the chapter.

The four probability strata sit in visibly different geometry. The lowest-probability probes were sparse sites — mean baseline attachment probability around 0.367, with almost exactly one occupied neighbour. The highest-probability probes were dense — baseline around 0.818, with roughly 4.26 occupied neighbours.

Force an attachment in those different geometries and the immediate effect on frontier opportunity changes sign.

```text
                            SPARSE      DENSE

newly promoted frontier      2.21        0.00
total frontier change       +1.21       −1.00
```

At a sparse interface, occupying one cell gives several previously unsupported empty neighbours their first occupied neighbour, and new frontier appears. At a dense interface, almost everything nearby is already occupied or already eligible, so the only substantial change is that the focal site itself leaves the frontier — the attachment consumes opportunity rather than creating it.

The paired difference in frontier creation was about 2.21 sites, interval [2.02, 2.41], `p = 0.000125`.

> **The same one-cell attachment can create or consume very different amounts of immediate frontier opportunity depending on local geometry.**

That result is established under the frozen frontier measurement.

It immediately suggests a stronger question: does that immediate opportunity transformation predict what the intervention causes later?

---

## But Geometry Did Not Predict Long-Run Gain

The obvious stronger hypothesis is that sites creating more immediate frontier opportunity should also produce larger downstream causal consequences.

The point estimates encourage it:

```text
sparse probe    G_transient(30) ≈ 0.219
dense probe     G_transient(30) ≈ −0.073
```

The predeclared paired comparison does not:

```text
difference   0.292    [−0.292, 0.917]    p = 0.371
```

and the retained-arm version does not either (difference 0.854, interval `[−0.625, 2.282]`, `p = 0.258`).

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

After the initiating occupancy is equalized away, the positive transient total is unresolved and no continuing positive accumulation is established over the tested late window.

When the initiating cell is left unremoved, the cumulative thirty-update consequence is substantially larger, but no permanent positive growth-rate offset is established.

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

## Experimental Note

The corrected decomposition, in enough detail to audit it.

```text
groups                   96
probes per group          4
total probes            384
horizon                  30 updates
late window       updates 21–30
loss rate                0.08
evaluation budget        96
fresh seed         20260906
```

The intervention, update by update:

```text
CHECKPOINT
    RETAINED, TRANSIENT   x inserted as occupied
    PREVENT               x absent
    no loss step before the exposure

LAG 1  — one controlled causal exposure
    forced branches       x present as an occupied neighbour
    PREVENT               x removed from the frontier before
                          finite-budget selection, so it cannot attach

AFTER LAG 1 GROWTH AND LOSS
    TRANSIENT             x removed
    PREVENT               x removed
    RETAINED              not touched
    absence asserted in both equalized branches

LAG 2 ONWARD
    ordinary dynamics in every branch
    x may reoccupy naturally; reoccupation is downstream
    x excluded from all measured outcomes
```

The measured quantities:

```text
g_mech_1      expected neighbouring construction difference at lag one,
              computed from branch probabilities before any Bernoulli draw

g1            realized neighbouring construction difference at lag one

G_A(H)        cumulative local construction difference for arm A,
              summed over H updates, excluding x

late mean     mean per-update local gain across updates 21–30

difference    retained minus transient, computed per probe before
              any aggregation, so the PREVENT term cancels

far field     cumulative global minus cumulative local difference
```

One definition carries weight throughout: **RETAINED does not mean clamped occupancy.** It means the initiating cell was not experimentally removed. Its subsequent fate follows the ordinary loss and reoccupation dynamics, and the focal-state diagnostics above report what that fate actually was.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Local process activity propagates as a distance-lag ridge | **FAILED** | primary statistic missed its gate; estimator shown able to manufacture the shape |
| The interface behaves as a loss-source / attachment-sink field | **FAILED** | neighbourhood signs opposite, once distance zero was excluded |
| Attachment raises, and loss lowers, nearby attachment at distances 1–2 | **SUPPORTED** | signed event analysis, decaying by distance 3 |
| Forcing one attachment causes additional neighbouring construction | **SUPPORTED** | replicated across runs; `g1 ≈ 0.109` on the corrected fresh seed |
| The immediate effect matches the frozen local rule | **SUPPORTED** | discrepancy `0.0066`, interval `[−0.0210, 0.0356]` |
| A positive transient cumulative consequence exists at thirty updates | **NOT ESTABLISHED** | `G_transient(30) = 0.042`, interval `[−0.135, 0.216]` |
| The transient branch sustains continuing positive late accumulation | **FAILED** | late rate `−0.0026` per update, interval spanning zero |
| Leaving the initiating cell unremoved produces a larger thirty-update cumulative consequence than the transient intervention | **SUPPORTED** | retained-minus-transient difference `0.698`, interval `[0.299, 1.102]` |
| The retained branch holds a positive late growth-rate offset | **FAILED** | late rate `−0.0130`, interval spanning zero, below the declared floor |
| The retained cell stays occupied across the horizon | **FAILED** | occupied `18.28` of `30` updates; present at `H=30` on `44.5%` of probes |
| Sparse and dense probe geometries differ in immediate frontier-opportunity transformation | **SUPPORTED** | sparse-minus-dense frontier-creation difference `2.21`, interval `[2.02, 2.41]`, `p = 0.000125` |
| Sparse geometry produces reliably greater long-run gain | **NOT ESTABLISHED** | transient difference `0.292`, `p = 0.371`; retained arm `p = 0.258` |
| Frontier Creation Potential predicts transient gain (first test) | **INCONCLUSIVE** | interval `[−0.078, +0.431]` against declared `+0.15` |
| Exact local motif predicts transient gain | **INCONCLUSIVE** | half-width `0.50` against declared `0.20` |
| Recent turnover predicts transient gain | **NOT SUPPORTED (narrow scope)** | `−0.065`, `[−0.221, +0.096]`; substrate had no independent history state |
| Extreme Frontier Creation Potential produces the declared positive increase in expected lag-one local construction | **FAILED** | `ΔE1 = −0.0026`, interval `[−0.0395, +0.0333]`; achieved precision sufficient to exclude the declared `+0.10` effect |
| Downstream consequence is unpredictable in principle | **NOT CLAIMED** | three representations tested, not all possible ones |
| A negative cumulative construction difference appears outside the local measurement region | **SUPPORTED** | retained `−0.318`, interval `[−0.583, −0.068]`; transient `−0.177`, interval `[−0.362, −0.029]` |
| The shared finite evaluation budget is the mechanism producing that far-field difference | **NOT CLAIMED** | not isolated in this chapter |
| Branching ratio, criticality, propagating wave, self-sustaining cascade | **NOT CLAIMED** | no such structure tested |

---

## Where Does the Difference Go?

There is one measurement left over, and under the corrected intervention it becomes the most consequential thing in the chapter.

Throughout the intervention runs we tracked causal gain twice: locally, in the region around the intervention, and globally, across the whole crystal excluding the intervention site. Subtracting one from the other gives the construction difference arising outside the local measurement region.

```text
              local     global    far field

RETAINED      0.740     0.422     −0.318   [−0.583, −0.068]
TRANSIENT     0.042    −0.135     −0.177   [−0.362, −0.029]
```

Both far-field intervals lie below zero.

So the experiment establishes something the local story does not contain. Forcing one attachment is accompanied by *less* construction beyond the region where its local effect is measured, in both arms — and the effect survives in the transient arm, where the initiating cell was removed after a single exposure.

> **Under this finite-budget protocol, forcing one attachment produces a negative cumulative construction difference outside the local measurement region.**

That is an established difference. It is not an established mechanism, and the gap between those two things matters more here than usual, because a candidate mechanism is already sitting in the substrate.

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

The selected candidate sets remained more than 99% overlapping between branches, so whatever produces the far-field difference is not a wholesale rewriting of the global evaluation schedule.

But nothing in this chapter isolates the budget as the cause. The difference could route through the shared selector, through ordinary geometric spillover that the local region failed to enclose, or through something not yet named. Establishing that a difference exists beyond the local region is a much weaker claim than identifying what carries it there, and this experiment did only the first.

The previous chapter failed to find a privileged enclosing body.

This chapter found a local causal effect, no stable local gain variable that predicts its downstream size, and a negative construction difference appearing outside the region where the local effect lives.

That last result names its own next experiment.

> **Does competition for a shared finite evaluation budget create measurable causal effects between locations too far apart to interact through the local rule?**
