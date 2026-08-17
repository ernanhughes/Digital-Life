+++
title = "04: So We Built the Wrong Thing on Purpose"
date = "2026-08-14T10:30:00+01:00"
draft = false
description = "Before trusting our own tests, we built a deliberately simple decoy and attacked it with them. Visible form wandered, heavy positional damage failed to separate cleanly from ordinary variation, and every exact relationship could be replaced without producing a reliably larger macrostate shift than the control's own variation."
weight = 4
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Adversarial Calibration", "Swarm", "Persistence", "Dose Response", "Pre-declared Criteria", "Experimental Method", "Confounds"]
+++

The previous chapter ended with a specification.

Known rules, controlled interventions, one mechanism varied at a time, a history we can follow. That is the laboratory we will eventually need, and building it is most of the work still ahead.

Before building it, there is a cheaper question.

Are our tests any good?

That is not an idle worry. The last chapter produced the first positive result in this book. A bounded one, but a real one: structural recurrence intersected with causal ancestry, and a causal claim survived a test we had not designed to make it pass.

Which is exactly the moment at which standards slip.

Once one exciting claim has passed a test, the next exciting claim arrives with that test's reputation already attached to it. The instrument acquires authority it has not separately earned, and it becomes easier to overlook when it reads high.

There is a standard laboratory response to this kind of problem, and it is not merely to be more careful.

Challenge the instrument with something that should not support the interpretation you care about.

---

## The Decoy

In experimental biology the move is routine. Alongside the sample you care about, you run a **negative control**: a preparation in which the target condition is independently expected to be absent, processed through the same assay. If it comes back positive, you have learned something important about the assay. The same logic has been adapted in observational epidemiology to detect confounding and bias.[1]

We cannot construct that kind of negative control for digital life.

We do not possess an independent test proving that a computational system is not alive.

But we can borrow the logic.

We can build a deliberately simple system whose striking appearances are known consequences of explicit local rules, then ask whether the evidence we were tempted to treat as discriminating can distinguish it.

So we built a decoy.

We constructed a simple swarm of particles. Each particle had a position and a velocity, one designated friend and one designated enemy. Friends attracted. Enemies repelled. A weak pull toward the centre kept the world bounded, and a weak soft-core repulsion stopped pathological collapse.

The specific inspiration was Simon Woods' friend-and-enemy particle model, in which each particle moves toward one designated particle and away from another.[2]

Nothing in our implementation represented a flock, a ring, a vortex, an organism, a body, a boundary, an individual, a population, reproduction or life.

The broader point is older than this particular construction. Simple local interaction rules are well known to generate coherent macroscopic order, from Reynolds' distributed flocking model to Vicsek and colleagues' self-propelled particles.[3][4]

The point was to turn that fact against our own method.

The status of the swarm needs to remain precise.

We are not claiming to have proven that it is not alive. We have no procedure that would establish that, and inventing one for a case we already have an opinion about would violate the method of this book.

Its role is narrower.

> **If a deliberately simple, fully specified decoy can exhibit a property we intended to treat as evidence of digital life, then that property cannot, by itself, distinguish the systems we care about from the decoy.**

The swarm is therefore not a negative control for life itself.

It is an adversarial calibration system for our evidence.

We built it to expose tests that were too easy to pass.

It did not fail them.

---

## Four Branches

We ran the swarm until it produced visible large-scale organization, then took one evolved state and split it into four identical branches.

```text
control

material damage

organizational damage

identity-label replacement
```

**Material damage** displaced 30% of the particles violently while leaving every friend-and-enemy relationship intact. If persistence belonged to one particular visible arrangement of matter, this should hurt.

**Organizational damage** did the reverse. Positions and velocities were left exactly where they were, while 30% of the friend-and-enemy relationships were rewired. If persistence required the exact relationship graph, this should hurt more.

**Identity-label replacement** was the strange one.

Every particle carried an identity label that had no causal role. Nothing in the update law read it. We progressively replaced those labels until none of the original labels remained.

This was not component replacement.

The same dynamical particles, positions and velocities continued through the run.

The intervention tested the measurement itself.

If changing a causally inert bookkeeping label changed our persistence score, then the score was secretly encoding nominal identity.

It did not.

The branch tracked the untouched control while the original labels disappeared.

> **Our persistence measurement did not depend on preservation of causally inert identity labels.**

That establishes almost nothing about the swarm.

It establishes that one trivial definition of persistence had not leaked into the measurement.

Then the longer runs exposed a problem the short runs had hidden.

---

## The Control Would Not Stay Still

The first runs were encouraging in the way that should always be suspicious.

Damaged branches appeared to return toward a recognizable macroscopic form.

Then we ran it longer.

Over a longer window the untouched control also travelled far from the reference configuration — the very state against which we had been scoring everybody else's recovery.

For a while this looked like the experiment failing.

It was the experiment working.

It had found an assumption we had never declared, never justified and never noticed making:

> **We had defined persistence as return to one preferred picture.**

Nothing licensed that.

The control did not return to its own picture either, and the control was not damaged.

A definition of persistence that an undamaged system fails is not a strict definition.

It is a broken one.

So the question changed.

We had been asking whether the same **picture** came back.

Why should persistence require that?

---

## Persistence Might Not Be a Shape

We stopped measuring distance from a privileged configuration and described each state instead by nineteen macroscopic features: log radius of gyration, log anisotropy, mean speed, and quantiles of radial distance, pair distance, friend distance and enemy distance.

The conceptual change matters more than the feature list.

Do not ask whether the system returns to one picture.

Ask whether the system remains within a characteristic distribution of macroscopic states.

That requires a baseline.

How much does an untouched system's own macrostate distribution move around simply as a function of time?

So we watched the control alone and cut its trajectory into temporal blocks. If the system were progressively wandering into new kinds of behaviour, the first and last blocks should sit much farther apart than neighbouring blocks do.

They did not.

```text
median distance, adjacent blocks     2.397

median distance, first to last       2.284

ratio                                0.953 ×
```

The pictures changed radically.

The statistical regime did not show corresponding cumulative drift over the observed window.

```text
same visible state
≠
same dynamical regime
```

What our measurement could now treat as persistent was no longer one shape.

It was a region of macroscopic states through which the system moved.

And that gave us the comparison the rest of the chapter depends on.

Instead of asking whether an intervention returns to a snapshot, ask whether the distribution of states after intervention differs from the distribution an untouched copy explores on its own.

Then express that difference in units of the control's own variation.

From here on, **ordinary control self-variation** means the median distance across pairs of blocks drawn from the control's own trajectory. The adjacent-block and first-to-last values above serve a different purpose: they test for cumulative drift.

A damaged system whose long-run distribution differs from control by no more than that baseline has not, by this measurement, been shown to leave the measured regime.

---

## Material Damage Disappears Into Ordinary Variation

Under that measurement, throwing 30% of the particles violently out of position produced a median intervention-to-control distance of about:

```text
0.622 × ordinary control self-variation
```

The ratios reported in this experiment use their own control baseline and should not be compared numerically with the later dose-response sweep, which constructs that baseline differently.

One of eight independent runs exceeded the ordinary self-variation baseline.

None exceeded twice it.

> **Displacing 30% of the particles did not produce a long-run macrostate shift reliably larger, by this measurement, than the control's ordinary self-variation.**

That is a stronger statement than *the shape recovered*, and a different one.

The shape did not need to recover.

Under this feature representation and distance measure, we did not detect a long-run departure larger than the control's ordinary self-variation.

---

## The Result We Wanted Failed

Now the interesting branch.

We expected organizational damage to behave differently, and the expectation was not unreasonable.

The specific friend-and-enemy assignments participate directly in the dynamics. Attraction and repulsion between those pairs help generate every trajectory in the system. Rewiring 30% of them therefore attacks causal structure while initially leaving positions and velocities untouched.

And the effect was larger:

```text
mean distance from control

material damage          1.84

organizational damage    2.72
```

Which is not the comparison we had declared.

The declared comparison was against ordinary control self-variation.

By that standard organizational damage did not separate cleanly either:

```text
median      0.766 × ordinary control self-variation

mean        0.949 ×
```

Two of eight runs exceeded ordinary self-variation.

One exceeded twice it.

So the attractive sentence died:

```text
visible material can be disrupted
but
persistence is in the relationship graph
```

Nearly a third of the exact relationship assignments had been replaced, yet the resulting macrostate distributions did not reliably separate from ordinary control self-variation under our measurement.

That is not what we built the experiment hoping to find.

Which is why it is useful.

---

## We Had Chosen Another Noun Too Early

The pattern by this point was becoming difficult to miss.

One privileged visible configuration had already failed.

Thirty-percent positional damage had failed to produce a reliable departure.

Now substantial exact relationship identity looked too specific as well.

```text
causally inert identity labels     irrelevant to the measurement

particular visible configuration   not fixed

30% positional displacement        did not reliably separate

substantial exact edge identity    replaceable

measured dynamical regime          persistent so far
```

There are many available explanations for that final line, and they are not equivalent.

Perhaps only some relationships matter.

Perhaps what matters is a distribution of interaction lengths rather than particular pairs.

Perhaps graph motifs matter.

Perhaps only the balance of attraction against repulsion matters.

Perhaps the particular relationship network is largely interchangeable and the relevant constraint lies mostly in the update law.

We do not get to pick one because it sounds good.

The experiment had earned a new question, not an answer:

> **How much of the exact relationship graph can be replaced before the measured dynamical regime changes?**

That is measurable.

So we measured it.

---

## So We Swept the Graph

The next controlled experiment swept exact friend-and-enemy rewiring from 0% to 100% in ten-point increments across eight matched seeds.

The microscopic system, feature representation and standardization procedure remained fixed.

Only intervention strength changed.

The full configuration belongs in the Experimental Note.

One comparison needs ruling out before any number appears.

The 30% row below is not a numerical replication of the earlier 30% result, because the sweep constructs its control self-variation denominator differently.

Compare doses within this sweep, not ratios across the two experiments.

Before inspecting the full sweep, we froze the break criterion.

A dose would count as regime-breaking only if:

```text
median normalized shift > 1.0

AND

at least 75% of replicates exceed ordinary control self-variation
```

Declaring that in advance is a defence against one of the most ordinary forms of self-deception in experimental work: choosing, after seeing the data, which analysis counts as the analysis.[5]

So we froze it.

One dose passed.

---

## Fifty Percent Looked Like a Threshold

At 50% rewiring:

```text
median normalized shift                 1.430

fraction above control self-variation   0.75

fraction above 2 × self-variation       0.375
```

Both clauses were satisfied.

The metadata recorded a first operational break dose of 50%.

If we had tested only that dose — and testing one intermediate dose is an entirely reasonable-sounding experiment — we could have written a confident sentence about locating the organizational breaking point of the system, with a pre-declared criterion standing behind it.

Two things should have slowed us down even then.

The first is that the criterion was met exactly at its boundary.

Six of eight replicates exceeded ordinary self-variation.

The rule required at least six.

One of those six falling below the baseline and the dose fails.

A pre-declared threshold does not become more robust by being pre-declared.

It merely becomes honest about where it sits.

The second problem was simpler.

We had nine other doses.

---

## Then We Looked at the Rest of the Curve

```text
rewired     median shift / control self-variation

 10%              1.052
 20%              1.135
 30%              1.185
 40%              1.068
 50%              1.430
 60%              1.216
 70%              0.855
 80%              1.073
 90%              1.163
100%              0.949
```

A simple graph-destruction threshold story predicts that once increasing rewiring pushes the system out of its measured regime, stronger interventions should preserve or strengthen that departure.

The curve does not do that.

Normalized shift ranges from 0.855 to 1.430 without a monotonic relationship to dose.

The strongest intervention does not produce the strongest effect.

The largest value sits in the middle of the range, while two of the smallest occur at 70% and 100% rewiring.

The curve is not centred cleanly below the self-variation baseline either. Several doses produce shifts of roughly one control-self-variation unit or more, so the data do not support the stronger claim that rewiring has no effect.

What they fail to show is a monotonic dose-response.

The measured departure does not increase as more exact relationships are replaced.

So the responsible conclusions are both negative and both worth having:

> **The sweep does not identify a monotonic graph-destruction threshold.**

> **The isolated criterion crossing at 50% should not be promoted into a mechanistic claim, because stronger interventions do not preserve the effect.**

Freezing a criterion in advance protects against one specific failure: choosing the test after seeing the answer.

It does not protect against another:

treating a single crossing of that criterion as though it described a mechanism.

A pre-declared threshold can tell you that one result crossed a line.

It cannot tell you that the system underwent a transition.

For that stronger interpretation, the whole intervention series matters.

Here it does not support a monotonic transition.

---

## Every Relationship Replaced

Which leaves the final row.

First, the manipulation check.

Exact graph similarity fell as specified from:

```text
1.0
```

at zero rewiring to:

```text
0.0
```

at complete rewiring.

That is not a finding.

It confirms that the intervention did what it claimed.

At the final dose, not one original friend-or-enemy assignment remained.

The median normalized macrostate shift was:

```text
0.949 × ordinary control self-variation
```

Four of eight replicates exceeded ordinary self-variation.

None exceeded twice it.

> **In this configuration and under this macrostate measurement, complete replacement of every exact friend-and-enemy relationship did not produce a long-run macrostate shift reliably larger than the control's ordinary self-variation.**

---

## What This Does Not Mean

It does not mean relationships are irrelevant.

The difference is not a quibble.

At 100% rewiring, all of this remained:

```text
every particle still has one friend

every particle still has one enemy

the attraction rule

the repulsion rule

the interaction strengths

the particle count

the class of network

the microscopic update law
```

What disappeared was one thing:

> which specific particle was linked to which specific other particle.

So the result does not say that relationships do not matter.

It says something narrower:

> **Exact edge identity was not required for persistence of the measured dynamical regime under this configuration.**

Whatever supports that measured persistence is therefore not tied to preservation of particular edges.

It may be coarser.

It may lie elsewhere in the system.

It may be distributed across several levels at once.

Candidates are not in short supply: graph statistics, the distribution of interaction lengths, network motifs, the symmetry of the interaction law, the balance of attraction against repulsion, the ensemble of possible relationship graphs, the update law itself, or some joint coarse-graining generated by several of them.

We have not distinguished among those.

Nothing here entitles us to.

That is an earned open question rather than a gap in the writing.

We know what the next experiments are.

We also know that we have not run them.

---

## Why It Was Worth Building the Wrong Thing

We built the swarm to expose evidence that was too easy to pass.

It produced object-like forms and coherent-looking collective motion.

Thirty-percent positional damage failed to separate reliably from ordinary control self-variation.

The untouched control showed no corresponding cumulative drift in our nineteen-feature representation over the observed window.

Causally inert identity labels could be replaced without affecting the metric.

And every exact friend-and-enemy relationship could be replaced without producing a reliably larger macrostate shift than ordinary control self-variation.

None of those properties, by itself, distinguishes the systems we care about from a deliberately simple system built to generate complex collective behaviour.

That makes each of them weak evidence by itself.

That is the return on the whole exercise.

Not a candidate.

A raised bar.

> **From here on, any property we propose as evidence has to discriminate against a system built specifically to counterfeit it.**

Which sharpens the previous chapters rather than undermining them.

The Physarum result remains different. There we actually replaced more than 99.9% of the population. This swarm experiment did not replace components: it displaced some particles, verified that inert identity labels were irrelevant to the metric, and later replaced every exact relationship assignment.

It therefore does not make the Physarum turnover result disappear.

It tells us that robustness alone is less discriminating than it first appeared.

Chapter 3 survives for a different reason.

This swarm has no operational descendant relation and no branching reproductive lineage of the kind measured there.

It was never in a position to counterfeit causal reproduction.

That is what the decoy was for.

It cannot tell us which results are real.

It can tell us which proposed pieces of evidence were too easy to counterfeit.

The visible configuration would not stay fixed.

The exact relationship graph could be replaced completely.

Under our measurement, the long-run dynamical regime still did not reliably separate from ordinary control self-variation.

We had learned more about what the measured persistence did not require.

We were still much less certain what carried it.

---

## Experimental Note

The swarm results come from one implementation.

The four-branch damage study and the later rewiring sweep share a microscopic configuration: 256 particles, 10,000 burn-in steps, 12,000 post-intervention steps, sampling every 20 steps, and eight independent seeds. Every branch for a seed was cloned from one common post-burn-in checkpoint.

Burn-in is a settling period only. No claim is made that a stationary state was reached.

The macrostate is a nineteen-feature vector: log radius of gyration, log anisotropy, mean speed, and quantiles of radial distance, pairwise distance, friend distance and enemy distance.

All distances except radius of gyration itself are expressed relative to that radius, so the description is scale-relative by construction.

The feature representation contains no particle identity label and no node-identity feature. The metric therefore cannot score persistence merely by following nominal identity, and exact relationship assignments are free to change without being encoded directly as features.

Feature vectors are z-scored using a standardizer fit only on pooled control states.

Distribution distance is the multivariate energy distance between the late halves of two trajectories, computed on deterministically subsampled points.

Normalized shift is that distance divided by the control's own internal spread.

The four-branch study and the rewiring sweep construct that denominator differently: the former uses the late half of the control cut into three blocks; the latter uses the full control trajectory cut into six.

Ratios are therefore comparable within each experiment and not numerically across the two.

The adjacent-block and first-to-last values reported earlier are a separate diagnostic for cumulative drift and are not the denominator used for intervention ratios.

Regime-persistence claims in this chapter are bounded to this feature representation, normalization procedure and distance metric.

A different description could produce a different answer.

Failure to detect a departure is not evidence that no underlying change occurred.

Eight replicates per dose is a small sample. The dose-response curve supports an absence of detected monotonic dose-dependence under this analysis; it should not be read as a precise estimate of effect size. Bootstrap confidence intervals on each dose's median ratio belong with the per-dose results in the appendix.

The break criterion was frozen in the configuration before the sweep was inspected.

Graph-similarity values are manipulation checks fixed by the intervention arithmetic rather than empirical outcomes: the rewiring operation forbids reassignment to the previous target, so exact similarity is determined by dose.

Full parameters, feature definitions, standardizer construction, intervention protocols, per-seed results and discarded runs are provided in the appendix.

---

## References

**[1]** Lipsitch, M., Tchetgen Tchetgen, E. & Cohen, T. *Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies.* Epidemiology 21(3), 383–388 (2010). doi:10.1097/EDE.0b013e3181d61eeb

**[2]** Woods, S. *Dancing with friends and enemies: boids' swarm intelligence.* Wolfram Community (2012).

**[3]** Reynolds, C. W. *Flocks, Herds, and Schools: A Distributed Behavioral Model.* Computer Graphics 21(4), 25–34 (1987). doi:10.1145/37402.37406

**[4]** Vicsek, T., Czirók, A., Ben-Jacob, E., Cohen, I. & Shochet, O. *Novel Type of Phase Transition in a System of Self-Driven Particles.* Physical Review Letters 75(6), 1226–1229 (1995). doi:10.1103/PhysRevLett.75.1226

**[5]** Simmons, J. P., Nelson, L. D. & Simonsohn, U. *False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant.* Psychological Science 22(11), 1359–1366 (2011). doi:10.1177/0956797611417632
