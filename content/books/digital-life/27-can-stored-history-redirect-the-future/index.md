+++
title = "27: Can Stored Material History Redirect the Future?"
date = "2026-08-13T20:38:00+01:00"
draft = false
description = "Chapter 27 tests whether hidden material state can change the causal response of identical visible geometry, and whether that effect persists after the original trace has decayed."
weight = 27
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Causality", "Finite Computation", "Experimental Method", "Cellular Automata"]
series = ["Digital Life From First Principles"]
+++

By the end of the previous chapters, the Digital Crystal had become harder to describe with ordinary biological language.

It could grow.

It could lose material.

It could rapidly reuse vacated sites.

Finite computation could couple distant regions by redistributing evaluation slots.

Local causal influence could be measured directly.

But none of those results required an organism.

None required an individual.

And none required memory.

That distinction mattered.

It would have been easy to look at a persistent alteration inside the crystal and call it memory simply because the present depended on something that had happened before.

Chapter 19 had already shown why that would be too fast.

Two different pasts could leave persistent, spatially distinguishable traces, yet those traces did not produce a scientifically meaningful common-challenge response beyond the erasure control.

A trace could persist without being usefully read.

A past could leave structure without that structure functioning as a causal history channel.

So Chapter 27 asked a narrower question.

Not:

> Does the Digital Crystal have memory?

But:

> **Can two states with the same visible geometry respond differently to the same perturbation because they contain different hidden material state?**

That question is much more primitive.

And much more testable.

---

## Same shape, different state

The experiment introduced a second kind of state into the crystal.

Visible occupancy remained the same.

The occupied cells were identical.

The probe geometry was identical.

The future environment was identical.

The random-number stream was identical.

The allocation policy was identical.

But some occupied cells carried a decaying internal material value.

That value was invisible if we looked only at occupancy.

The important comparison was therefore:

```text
SAME VISIBLE GEOMETRY
+
DIFFERENT MATERIAL STATE
```

The material state did one simple thing.

For a frontier candidate \(y\), attachment probability depended not only on the ordinary Digital Crystal terms, but also on the material stored in neighbouring occupied cells.

Conceptually:

\[
\text{score}(y)
=
\text{ordinary crystal score}(y)
+
g_m \sum_{z \in N(y)} m(z)
\]

where:

- \(m(z)\) is the stored material value on neighbour \(z\),
- \(g_m = 0.30\),
- and the final attachment probability is obtained through the same logistic response used elsewhere in the crystal.

The material was not permanent.

Its half-life was frozen at six updates.

The trace had already aged three updates before the test began.

Each stored cell therefore started the experiment with strength:

\[
2^{-3/6}
=
2^{-1/2}
\approx 0.707
\]

Two cells carried the trace.

The total starting material mass was therefore approximately:

\[
2 \times 0.707
=
1.414
\]

Newly attached cells did not inherit it.

The material did not propagate.

It simply decayed.

This was deliberately weak.

We were not building a memory system.

We were giving the crystal one hidden state variable and asking whether that variable could matter causally.

---

# Accessible and remote history

The experiment used three material-state conditions.

### Accessible

Two occupied cells close to the probe carried the decaying material trace.

The sole occupied neighbour of the probe cell was always included.

This guaranteed that the stored state was locally causally accessible.

### Remote

The same number of occupied cells carried the same amount of material, but those carriers were placed beyond the twelve-step local causal reach of the probe.

### Erased

No material state was present.

The primary comparison was:

\[
\text{ACCESSIBLE}
-
\text{REMOTE}
\]

not accessible versus erased.

The remote arm mattered because it separated:

> material exists somewhere

from:

> material is causally positioned to affect the probe.

---

# What went wrong in V1

The first full experiment looked promising.

The immediate causal response differed strongly between accessible and remote material states.

The twelve-step causal consequence also appeared lower under accessible history.

But inspection of the implementation exposed a construct-validity failure.

The intended intervention was:

```text
FORCE:
x is occupied for one causal exposure

PREVENT:
x is kept empty for that same exposure
```

The implementation did something different.

`FORCE` inserted \(x\).

`PREVENT` merely began with \(x\) empty.

During the first growth update, the PREVENT branch was still allowed to attach \(x\) naturally.

That is not prevention.

And because the accessible material trace deliberately included \(x\)'s sole occupied neighbour, it changed the probability that \(x\) would attach.

The audit recovered that probability exactly.

Mean probability that PREVENT would naturally attach \(x\):

```text
accessible   0.428
remote       0.377
erased       0.378
```

The accessible treatment increased the probability of the supposedly prevented cell appearing by about five percentage points.

That contaminated the twelve-step intervention.

The formal V1 downstream result was therefore invalid.

This was not a statistical problem.

It was not lack of power.

It was not an inconvenient confidence interval.

It was an intervention that did not implement the experiment we thought we were running.

That distinction is worth preserving.

> **An empty cell at the start of a control branch is not the same thing as a cell being prevented from appearing.**

---

# Something survived V1

The V1 failure did not destroy everything.

The immediate expected causal response had been calculated before realized growth occurred.

It therefore did not depend on whether \(x\) later attached in PREVENT.

That immediate quantity was:

\[
E_1
=
\text{expected FORCE attachment}
-
\text{expected PREVENT attachment}
\]

over the local ring around the probe.

Accessible material reduced that immediate causal response.

The accessible-minus-remote difference was approximately:

\[
\Delta E_1
\approx -0.0182
\]

with a narrow confidence interval entirely below zero.

That effect was real.

But why would a positive material term reduce causal response?

The material gain was positive.

Material increased attachment probability.

It seemed at first that the response should therefore increase.

The mechanism audit showed the opposite.

---

# Stored state can reduce sensitivity

The attachment function is logistic.

A candidate's probability does not increase linearly with score.

The derivative is:

\[
p(1-p)
\]

which means the same score increment produces different probability changes depending on where the candidate already sits on the sigmoid.

The accessible material raised the baseline attachment probability of shared frontier candidates.

Those candidates were therefore pushed toward a flatter part of the response curve.

Then the FORCE intervention added its own local causal input.

But because the candidate was already further along the sigmoid, the additional probability increase caused by FORCE became smaller.

So:

```text
material raises baseline probability
↓
candidate moves toward saturation
↓
same perturbation produces smaller Δp
```

The candidate-level accounting made this mechanism unusually clean.

For accessible versus erased history, the shared-candidate saturation contribution was approximately:

\[
-0.01814
\]

while the total immediate difference was approximately:

\[
-0.01930
\]

Almost the entire immediate effect was explained by reduced sensitivity on the shared frontier opportunities.

This gave us a sharper statement than:

> history changes response.

The actual result was:

> **Stored material state changed the response function itself.**

More precisely:

> **Locally accessible material state raised baseline attachment probability and thereby reduced the incremental causal sensitivity of shared frontier opportunities to the same perturbation.**

That is not memory.

But it is hidden-state causal modulation.

---

# Remote state was not automatically a clean null

The V1 audit uncovered another problem.

Remote material was physically beyond the local causal reach of the probe.

Yet remote and erased states still produced a tiny difference in local \(E_1\).

The reason was not material propagation.

It was calibration.

The protocol dynamically matched expected background construction.

If remote material changed expected construction somewhere else in the crystal, the calibration system compensated by changing a global score offset.

That offset applied everywhere.

So:

```text
remote material
↓
global expected construction changes
↓
calibration offset changes
↓
local probabilities change slightly
```

The remote state's entire V1 local effect could be attributed to that calibration pathway.

This was another useful lesson.

> **A global compensator can create a causal channel between regions that are otherwise locally separated.**

That is not a property of the material state.

It is a property of the experimental controller.

For V2, the remote control therefore needed to be better matched.

---

# Correcting the experiment

Chapter 27 V2 kept the material parameters frozen.

No gain was changed.

No half-life was changed.

No history age was changed.

No horizon was changed.

No effect threshold was changed.

The changes were construct-validity corrections.

The first correction was simple:

```text
PREVENT explicitly blocks x during lag 1.
FORCE explicitly contains x during lag 1.
```

After one causal growth exposure, \(x\) was removed from FORCE.

Both branches then continued normally.

The second correction improved the remote control.

Instead of choosing remote carriers simply because they were far away, remote material carriers were matched to accessible carriers on baseline frontier influence.

For each accessible carrier, the experiment measured:

- how many frontier cells it touched,
- and the total baseline attachment-probability mass of those adjacent frontier cells.

A remote carrier had to match the frontier count exactly and the probability mass within a frozen tolerance.

It also had to remain beyond the twelve-step local causal reach of the probe.

This produced a much cleaner remote control.

The remote-minus-erased immediate effect fell to approximately:

\[
8.2 \times 10^{-5}
\]

effectively removing the calibration leakage that had complicated V1.

---

# The primary estimator changed too

The realized twelve-step attachment difference was noisy.

That was obvious in V1.

So V2 used a Rao-Blackwellized estimator as the primary quantity.

At every lag, before realized Bernoulli attachment decisions were drawn, the experiment calculated the expected local causal difference:

\[
\Delta_t
=
\sum_{y \in L}
p_{\text{FORCE}}(y,t)
-
\sum_{y \in L}
p_{\text{PREVENT}}(y,t)
\]

where \(L\) was the same local spatial support used for the realized outcome, and the intervention cell itself was always excluded.

The cumulative expected causal consequence was then:

\[
G_{\mathrm{RB}}
=
\sum_{t=1}^{12} \Delta_t
\]

This did not freeze the trajectory into expectation.

The FORCE and PREVENT branches still evolved through realized stochastic events.

Their states could diverge.

Material could decay.

Cells could be lost.

Geometry could change.

The estimator merely removed the extra Bernoulli noise from measuring each lag's consequence.

The realized twelve-step result remained as a secondary outcome.

---

# V2 passed

The corrected experiment used 192 independent groups.

All 192 groups remained represented after the stricter remote-matching rule.

There were 564 supported probes.

Every major validity gate passed:

```text
group coverage                     100%
dynamic matching records           100%
population matching gate           PASS
intervention assertions            PASS
remote carrier matching            PASS
```

The corrected experiment was valid.

---

# The immediate effect replicated

The immediate accessible-minus-remote causal difference was:

\[
\Delta E_1
=
-0.01499
\]

with 95% confidence interval approximately:

\[
[-0.01725,\,-0.01281]
\]

The sign matched V1.

The magnitude was slightly smaller, which was expected after removing control asymmetries.

But the effect survived.

This mattered.

The local sensitivity reduction was not an artifact of the V1 PREVENT bug.

It was not an artifact of the old remote-carrier placement rule.

The hidden material state genuinely changed the immediate causal response of identical visible geometry.

---

# The downstream effect was negative too

The primary twelve-step Rao-Blackwellized comparison was:

\[
\Delta G_{\mathrm{RB}}
=
G_{\mathrm{accessible}}
-
G_{\mathrm{remote}}
=
-0.397
\]

with 95% confidence interval approximately:

\[
[-0.679,\,-0.119]
\]

The realized secondary result pointed in the same direction:

\[
\Delta G_{\mathrm{realized}}
\approx -0.357
\]

with 95% confidence interval approximately:

\[
[-0.673,\,-0.040]
\]

So both estimators agreed.

Accessible material state reduced the later causal consequence of the same perturbation.

But the frozen decision rule contained another requirement.

The predeclared smallest effect of interest was:

\[
\pm 0.15
\]

To call the magnitude **SUPPORTED**, the experiment required not only a confidence interval excluding zero, but enough precision to resolve the predeclared threshold.

The achieved MDE was still around:

\[
0.357
\]

So the formal minimum-magnitude claim remained:

```text
UNRESOLVED
```

That does not mean the direction was unresolved.

It means two different questions had different answers.

```text
Is the effect negative?
SUPPORTED

Can we establish with the frozen precision rule
that the mean effect is at least 0.15 in magnitude?
UNRESOLVED
```

Those statements are compatible.

And keeping them separate is important.

---

# Did the effect simply track the material?

At this point Chapter 27 still had one unresolved mechanistic question.

The material trace decayed.

The downstream causal consequence accumulated.

Was the later effect merely proportional to the amount of material still present?

Or did the material alter the trajectory early, after which the changed trajectory continued under its own dynamics?

The V2 raw results already contained enough information to answer that descriptively.

No new experiment was needed.

---

# The material weakened. The causal difference kept growing.

The material began with total mass:

\[
M_0
\approx 1.414
\]

Half that value was:

\[
0.707
\]

The accessible material mass fell below that threshold at lag 4.

By the previous lag, cumulative expected causal difference was only:

\[
-0.0995
\]

The final twelve-step difference was:

\[
-0.3972
\]

Therefore approximately:

\[
75\%
\]

of the final causal difference accumulated after the material had already fallen below half of its initial mass.

The trace fell below one quarter of its starting mass around lag 8.

Even after that point, another approximately:

\[
-0.141
\]

of cumulative causal difference accrued.

That was about:

\[
36\%
\]

of the final effect.

The material was disappearing.

The causal consequence was still accumulating.

---

# Early, middle and late

Dividing the twelve-step continuation into three descriptive epochs made the pattern even clearer.

```text
EARLY    lags 1–4     -0.120
MIDDLE   lags 5–8     -0.158
LATE     lags 9–12    -0.119
```

The effect was not concentrated in the first few updates.

The middle epoch contributed more than the early epoch.

Even the late epoch, when mean accessible material mass had fallen to roughly:

\[
0.183
\]

still contributed an average negative increment.

The late-period interval was wide enough to include zero, so this was not promoted as a separate confirmatory finding.

But descriptively the trajectory did not look like a direct material-dose response.

The system had already been redirected.

---

# Material amount did not predict the causal increment

The closeout analysis also asked whether more surviving material simply produced a larger causal effect.

It did not.

The pooled correlation between accessible material mass and the accessible-minus-remote causal increment was approximately:

\[
r \approx -0.001
\]

essentially zero.

At the group level, final causal difference was also only weakly related to average surviving material or to the difference in material mass between accessible and remote arms.

So the simplest dose model failed descriptively:

```text
more material
≠
larger downstream causal effect
```

The more plausible sequence was:

```text
material state
↓
changes immediate local sensitivity
↓
changes which construction events occur
↓
changes later geometry and state
↓
later causal response changes
even after original material weakens
```

The material did not need to remain strong forever.

It only needed to alter the path.

---

# Material-State Trajectory Redirection

This gives us a new phenomenon.

Not memory.

Not learning.

Not adaptation.

A more primitive property.

We can state it operationally:

> **A locally accessible decaying material state can alter the causal sensitivity of otherwise identical visible geometry, and the resulting construction differences can redirect later system evolution so that additional causal consequences accumulate after the original material trace has substantially weakened.**

Call this:

## **Material-State Trajectory Redirection**

The name matters less than the distinction it captures.

A hidden state variable does not merely need to persist physically to matter.

Its effect can be converted into later geometry.

Once that happens, the consequences may continue after much of the original hidden state has disappeared.

This is one way a past can matter without the present containing a complete record of that past.

---

# What this is not

The temptation now is obvious.

The system has hidden state.

The hidden state changes later response.

Its consequences outlive much of the original trace.

Why not call that memory?

Because the material was experimentally written.

The crystal did not acquire it from an endogenous experience encoder.

It did not decide what to store.

It did not reconstruct past events.

It did not use the state to choose among remembered alternatives.

It did not demonstrate learning.

It did not demonstrate adaptation.

What we have shown is more basic:

```text
PAST-DEPENDENT HIDDEN STATE
↓
CAUSAL RESPONSE MODULATION
↓
TRAJECTORY REDIRECTION
```

A memory system would need to build on that.

But this result does not yet earn the word.

---

# What survived the hypothesis?

The Chapter 27 evidence can be separated cleanly.

### Immediate hidden-state modulation — SUPPORTED

With occupancy geometry held fixed, locally accessible material state changed the immediate expected causal response to the same perturbation.

### Mechanism — SUPPORTED

The immediate reduction was primarily explained by shared frontier candidates being shifted toward a flatter region of the logistic attachment response.

### Corrected downstream direction — SUPPORTED NEGATIVE

In V2, both expected and realized twelve-step causal consequences were lower under accessible material state than under matched remote material state.

### Frozen \(\pm0.15\) minimum-magnitude claim — UNRESOLVED

The experiment did not achieve enough precision to establish the predeclared minimum meaningful magnitude under the frozen decision rule.

### Trajectory-redirection interpretation — DESCRIPTIVELY SUPPORTED

Most of the cumulative expected causal difference accrued after the material trace had fallen below half its starting mass, and substantial additional difference accrued after it had fallen below one quarter.

### Memory — NOT ESTABLISHED

The stored material state was experimentally written.

---

# The broader lesson

Chapter 27 began with a small question.

Can hidden state matter if visible geometry is the same?

The answer is yes.

But the more interesting result came afterward.

The hidden state did not merely bias one attachment decision.

It changed sensitivity.

That changed construction.

Changed construction altered later state.

And later state carried forward consequences after the original hidden trace had substantially decayed.

The causal chain was therefore not:

```text
stored material
→ persistent force
```

It was:

```text
stored material
→ altered response
→ altered events
→ altered trajectory
```

That distinction will matter later.

A digital system does not necessarily need a durable biological-style memory object to let the past shape the future.

It may need something more primitive:

> **a state difference that can alter the path strongly enough for the path itself to carry the consequence forward.**

That is what the Digital Crystal has now demonstrated.

The next question is no longer whether hidden material state can matter.

It can.

The harder question is whether those causal histories can become organized into something with a boundary of its own.

Not merely a process that has a past.

But a process whose internal causal structure becomes more strongly coupled to itself than to the rest of the world.

That is where individuality begins.
