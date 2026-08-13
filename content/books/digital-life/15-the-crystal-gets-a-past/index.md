+++
title = "15: The Crystal Gets a Past"
date = "2026-08-11T21:52:00+01:00"
draft = false
description = "A Digital Crystal can preserve source statistics in morphology but not temporal order. We add state, checkpointing, event history, replay and branching to discover what a recoverable digital past actually requires."
weight = 15
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "State", "History", "Checkpointing", "Replay", "Counterfactuals"]
series = ["Digital Life From First Principles"]
+++

At the end of the last chapter, our Digital Crystal could tell us something about the world that formed it.

But not enough.

Different forcing processes produced different morphologies.

We could hide the source and recover its family substantially better than chance.

Then we asked a harder question:

> What happened first?

We took exactly the same environmental values and rearranged them in time.

Smooth.

Bursting.

Periodic.

Alternating.

Random.

The final morphology could not reliably tell them apart.

```text
SAME VALUES
+
DIFFERENT ORDER
↓
NO RECOVERABLE TEMPORAL SIGNATURE
```

The crystal had accumulated a state.

It had not preserved a usable history.

That gives us the next experiment.

Not intelligence.

Not learning.

Not adaptation.

Something much smaller.

> **What must a digital process preserve if we want its past to survive?**

---

## The Present Is Not the Past

Our Digital Crystal already has a present state.

At any moment, (C_t) contains the cells that currently exist.

Those cells are consequences of earlier growth.

So the past clearly mattered.

But Chapter 14 taught us an important distinction:

> **Past contributed to present does not imply present contains a recoverable record of the past.**

A footprint exists because someone walked there.

The footprint is not the walk.

A crater exists because something struck the ground.

The crater is not the complete trajectory of the object that made it.

Our crystal is similar.

Its current shape contains consequences.

That does not mean it contains the sequence that produced them.

So we need to separate two ideas:

```text
STATE
and
HISTORY
```

---

## State

We begin with an operational definition:

> **A state representation is sufficient if it contains enough information to continue the process faithfully from here.**

That wording matters.

We are **not** claiming that we already know the mathematically smallest possible state.

We are asking whether a particular stored representation is sufficient.

Perhaps the picture itself is enough.

Perhaps:

```text
occupied cells
```

is the complete state.

We can test that.

Digital Crystal v1 is stochastic.

Its continuation depends on random attachment decisions.

Its continuation also depends on where the process currently is in the environmental input.

So a candidate checkpoint might contain:

```text
occupied cells
birth-time metadata
current timestep
current signal position
random-number-generator state
model parameters
```

But we should not declare all of those necessary merely because they sound plausible.

We should remove them.

One at a time.

---

## Run the Crystal Continuously

We take frozen Digital Crystal v1 from Chapter 14.

The local growth rule does not change.

The experiment runs for:

```text
96 steps
```

with a checkpoint halfway through:

```text
t = 48
```

In the full v3 experiment:

```text
population at checkpoint    2,702
final population            9,574
```

The final morphology receives a hash:

```text
bc8e6d8c9783431f1459bf17
```

and the full process state receives another:

```text
bd33c9aa0a510803be6ce6bf
```

{{< figure
src="/images/books/digital-life/ch15-01-reference-and-checkpoint.png"
alt="The Chapter 15 Digital Crystal input signal with a checkpoint at step 48, together with the crystal at the checkpoint and its final state at step 96."
caption="The continuous reference trajectory. The midpoint checkpoint will be restored, damaged and replayed in later experiments."

>}}

Now we can demand something much stronger than visual similarity.

If the checkpoint is sufficient, then restoring it should produce:

> **exactly the same future.**

---

## Before We Could Save the State, We Found a Hidden One

Our first implementation failed this experiment.

The checkpoint appeared complete.

We saved:

```text
occupied cells
birth metadata
timestep
signal cursor
RNG state
```

Then we restored it.

The future changed.

At first that looked like evidence that something important was missing from our checkpoint.

But another result contradicted that interpretation.

When we reconstructed the same checkpoint **without passing through serialization**, continuation was exact.

So something was happening at the implementation boundary.

The culprit was surprisingly mundane.

Candidate attachment sites were held in a Python `set`.

The growth loop effectively did:

```python
for cell in frontier:
    ...
    rng.random()
```

A set has no scientific ordering.

Its internal iteration order is an implementation detail.

Two sets can contain exactly the same cells but iterate them in different orders after reconstruction.

That meant:

```text
same mathematical cells
+
same RNG state
+
same signal
```

could still become:

```text
RNG draw #1 → different candidate
RNG draw #2 → different candidate
...
```

The simulation had accidentally acquired an undeclared state variable:

```text
PYTHON CONTAINER LAYOUT
```

That is not a property of the Digital Crystal.

It is a property of the implementation.

So we removed it.

The growth rule now consumes stochastic decisions in a canonical order:

```python
for cell in sorted(frontier):
```

Then we reran the experiment.

---

## State Belonging to the Model vs State Belonging to the Program

Before trusting checkpointing again, we added a stronger invariant.

Take a checkpoint.

Serialize and deserialize:

```text
occupied cells
birth metadata
RNG state
```

into fresh Python objects.

Then compare the original state and reconstructed state.

They must produce:

```text
same one-step continuation
and
same complete remaining continuation
```

The v3 reproducibility invariant passed:

```text
occupied state equal                   True
birth metadata equal                   True
signal cursor equal                    True
RNG state equal                        True
process hash equal                     True

one-step continuation exact            True
full remaining horizon exact           True
remaining steps checked                48
```

The implementation no longer depends on accidental set layout.

That gives us a methodological rule worth keeping:

> **An experimental model must distinguish state belonging to the phenomenon from state accidentally belonging to its implementation.**

Only after that did checkpointing become a meaningful experiment.

---

## Stop It

At step `48` we serialize the operating state.

Not a screenshot.

Not a rendered image.

The actual continuation representation.

Then we terminate that runtime state.

Load the checkpoint from SQLite.

Continue.

If our checkpoint representation is sufficient, the restored process should not merely resemble the uninterrupted one.

It should become:

```text
the same cells
the same attachment decisions
the same population trajectory
the same final process state
```

---

## Save, Restore, Continue

After the reproducibility fix:

```text
exact final morphology            True
exact final process state         True
population trajectory identical   True
attachment trajectory identical   True
symmetric-difference cells        0
```

The morphology hashes match:

```text
REFERENCE   bc8e6d8c9783431f1459bf17
RESTORED    bc8e6d8c9783431f1459bf17
```

The complete process hashes match too.

{{< figure
src="/images/books/digital-life/ch15-02-exact-restore.png"
alt="The final continuously run Digital Crystal beside the final crystal produced after checkpoint, SQLite restore and continuation."
caption="After canonicalizing stochastic candidate traversal, continuous execution and checkpoint → restore → continue produce the exact same trajectory."

>}}

And this was not a one-run accident.

We repeated the checkpoint experiment across:

```text
30 independent runs
```

Result:

```text
30 / 30 exact
```

So we have earned the first major claim:

> **The stored Digital Crystal checkpoint representation is sufficient for exact continuation of the stochastic process.**

Notice what we have **not** claimed.

We have not proven that this is the smallest possible state representation.

That question remains open.

---

## What Actually Matters for Continuation?

Now we deliberately damage the checkpoint.

But this time the experiments are carefully isolated.

Every variant receives exactly:

```text
48 continuation updates
```

So altering the environmental cursor does not accidentally alter the length of the experiment.

---

## Remove the Random State

First:

```text
same morphology
same birth metadata
same timestep
same signal position
different RNG continuation state
```

The final result becomes:

```text
final population                 9,550
symmetric-difference cells          28
normalized difference          0.002924
```

The difference is small.

But it is not zero.

Exact continuation fails.

So:

> **RNG continuation state matters for exact continuation of Digital Crystal v1.**

That is not philosophical speculation.

We removed it.

The future changed.

---

## Move the Environmental Cursor

Next:

```text
same morphology
same RNG state
same timestep
same continuation horizon
```

but move the signal cursor:

```text
48 → 45
```

Both conditions still execute exactly `48` future updates.

The result:

```text
final population                 9,549
symmetric-difference cells          27
normalized difference          0.002820
```

So we can now say:

> **Where the process currently sits in the environmental sequence affects exact continuation.**

The environment is not merely historical context.

Its current position is part of the continuation conditions.

---

## Remove the Birth Times

Now we perform a cleaner test.

Preserve:

```text
occupied cells
RNG state
signal cursor
timestep
```

but replace the birth-time metadata.

What happens?

```text
final population                 9,574
symmetric-difference cells           0
normalized difference          0.000000
```

The final occupied set is exact.

Only the birth-time metadata differs.

That gives us an extremely useful distinction.

Under the current Digital Crystal v1 growth rule:

> **Birth times are part of the historical record, but they are not required for the same geometric continuation.**

This is the first place where state and history begin to separate experimentally.

Birth time tells us:

```text
how the current structure formed
```

but the growth mechanism does not consult it when deciding the next attachment.

So birth time can matter to history without mattering to future growth.

---

## Save Only the Morphology

Now perform the brutal test.

Preserve only the visible occupied structure.

Reconstruct other process details incorrectly.

Continue.

The result:

```text
final population                 9,548
symmetric-difference cells          30
normalized difference          0.003133
```

The visible shape at the checkpoint was identical.

The future was not.

{{< figure
src="/images/books/digital-life/ch15-03-state-omission.png"
alt="Comparison of final-state divergence after restoring the full checkpoint, changing RNG state, shifting the signal cursor, changing birth metadata, or restoring morphology only."
caption="Visible morphology is insufficient for exact continuation. RNG state and environmental sequence position affect future growth, while birth-time metadata does not affect the occupied-set continuation under Digital Crystal v1."

>}}

This gives us another version of a lesson that has followed us through the book:

> **Appearance is not state.**

Two systems can look identical and still have different futures.

---

## What We Have Actually Identified

We need to be careful here.

We have not discovered:

> the unique minimal state of Digital Crystal v1.

We have discovered something narrower.

The experiments establish:

```text
FULL CHECKPOINT
→ sufficient

VISIBLE MORPHOLOGY ALONE
→ insufficient

RNG CONTINUATION STATE
→ causally relevant to exact continuation

SIGNAL POSITION
→ causally relevant to exact continuation

BIRTH-TIME METADATA
→ not required for geometric continuation
```

That is enough.

The useful operational idea is:

> **State is whatever information the future actually needs.**

Not whatever information happens to exist in our data structures.

And not whatever information sounds philosophically important.

---

## Now Give It History

Checkpointing solves one problem:

> Where are we now, and what do we need to continue?

It does not answer:

> How did we get here?

For that, we create an explicit event history.

At every growth step we preserve:

```text
step
input value
cells added
population
resulting morphology hash
```

So the history becomes:

```text
STEP 1
input = ...
added = [...]
state hash = ...

STEP 2
input = ...
added = [...]
state hash = ...

STEP 3
...
```

This is not memory in any cognitive sense.

The crystal does not inspect this record.

It does not learn from it.

It does not use it to make decisions.

It is an explicit formation history.

Now we ask whether the record is sufficient to reconstruct what happened.

---

## Replay the Process

There are two different ways to replay a past.

The distinction matters.

---

## Procedural Replay

First:

```text
same initial seed
+
same environmental signal
+
same frozen growth rule
+
same stochastic initialization
↓
run again
```

The result:

```text
exact final morphology     True
exact final process state  True
```

That establishes reproducibility of the computational procedure.

But it does not yet establish that the **stored event history** is sufficient.

So we perform a stronger test.

---

## Replay the Events

This time we do **not** rerun the stochastic growth rule.

Instead, take the recorded event stream.

At every step:

```text
read cells that appeared
↓
apply those additions
↓
recompute morphology hash
↓
compare with original recorded hash
```

There are:

```text
96 recorded steps
```

Result:

```text
96 / 96 morphology hashes match
```

Final morphology:

```text
exact
```

{{< figure
src="/images/books/digital-life/ch15-04-history-replay.png"
alt="Step-by-step comparison showing that every morphology hash produced by replaying the Digital Crystal event log matches the recorded original trajectory."
caption="The event history reconstructs the recorded morphology trajectory exactly: 96 matching hashes out of 96."

>}}

Now we have earned a second claim:

> **The explicit event history is sufficient to reconstruct the exact recorded morphology trajectory.**

Not the hidden historical RNG state.

Not every internal implementation detail.

The formation trajectory.

That is the correct scope.

---

## State Is Not History

We can now make the distinction operational.

A checkpoint and an event history both describe the same process.

But they answer different questions.

```text
STATE
=
enough information for faithful continuation

HISTORY
=
enough information to reconstruct how the present morphology was formed
```

A checkpoint can continue forward exactly.

An event log can reconstruct backward through the morphology trajectory.

But those capabilities are not interchangeable.

The history reconstructed from cell additions does **not** restore the historical RNG state.

And if we take reconstructed geometry without the correct stochastic continuation state, exact future continuation fails.

In the full experiment:

```text
history reconstructs checkpoint morphology    True
checkpoint continues exactly                  True

history-derived geometry without RNG
continues exactly                             False
```

The final difference in that last condition was:

```text
0.003133
```

So:

```text
CHECKPOINT
→ FUTURE

EVENT HISTORY
→ PAST MORPHOLOGY
```

They overlap.

But they are different mechanisms.

---

## The Digital Answer Was Not Biological

There is something important about how we solved this.

We could have tried to build a special region inside the crystal whose geometry somehow encoded its entire formation history.

A biological analogy might tempt us toward:

```text
memory organ
genome-like store
special history structure
```

But computation gives us another possibility.

```text
serialization
checkpoint
event log
replay
branch
```

These are native computational affordances.

We do not need to imitate a biological storage mechanism if the substrate gives us a different way to preserve the same capability.

This is exactly the rule we established earlier:

> **Do not import a biological mechanism unless the digital substrate actually requires it.**

The crystal's past does not need to look biological.

It only needs to be recoverable.

---

## A Digital Advantage

Biological systems generally do not offer us cheap, exact, executable copies of an earlier complete physical state.

Digital systems often can.

Our checkpoint is executable.

That changes what a saved past can be.

It is not merely evidence that something happened.

It can become:

```text
an experimental starting point
```

from which alternative futures are generated.

---

## Restore the Same Past Twice

Take the exact checkpoint at step `48`.

Restore it twice.

Both copies begin with:

```text
same occupied cells
same timestep
same signal cursor
same RNG state
same continuation state
```

Nothing differs.

Then deliberately provide different future environments.

```text
              ┌── FUTURE A
SAVED PAST ───┤
              └── FUTURE B
```

The resulting morphologies diverge.

In one illustrative branch:

```text
final symmetric difference    35 cells
normalized difference         0.003655
```

{{< figure
src="/images/books/digital-life/ch15-06-counterfactual-branches.png"
alt="One saved Digital Crystal checkpoint shown beside two different final morphologies generated from different prescribed future forcing."
caption="One exact checkpoint serves as a shared executable starting condition for two controlled future environments."

>}}

And we can watch that divergence develop.

{{< figure
src="/images/books/digital-life/ch15-06-counterfactual-divergence.png"
alt="A line plot showing morphology divergence through time between two Digital Crystal futures starting from the same checkpoint."
caption="Alternative prescribed futures starting from the same saved state generate measurable divergence."

>}}

So one capability is clearly established:

> **A complete digital checkpoint can act as an executable counterfactual branch point.**

But there is a trap here.

---

## Different Futures Always Diverge — But Why?

Suppose two continuations end differently.

It is tempting to say:

> The different environments caused the divergence.

But Digital Crystal v1 is stochastic.

Different random continuation states also produce different futures.

So the number:

```text
35 different cells
```

means nothing by itself.

We need a null.

---

## The Stochastic Null

We compare two experiments.

### Environmental treatment

```text
same checkpoint
same RNG state
different future forcing
```

### Stochastic null

```text
same checkpoint
same future forcing
different valid RNG states
```

We run:

```text
60 replicates
```

for each condition.

Now compare final normalized morphology divergence.

---

## The Environment Did Not Win

Different future environments produced:

```text
mean divergence      0.003815
median               0.003655
```

The stochastic null produced:

```text
mean divergence      0.005290
median               0.004812
```

So:

```text
treatment - null mean    -0.001475
```

The environmental treatment was not larger.

The pairwise superiority probability was:

```text
0.1975
```

and the treatment median did not exceed the stochastic-null 95th percentile.

{{< figure
src="/images/books/digital-life/ch15-06-counterfactual-null.png"
alt="Comparison of final Digital Crystal divergence under different future environments versus divergence produced by ordinary stochastic continuation variation."
caption="Changing future forcing produces alternative futures, but the resulting divergence is not larger than ordinary stochastic continuation divergence under this experiment."

>}}

This kills a stronger interpretation.

We cannot say:

> **Environmental differences dominate future divergence.**

They did not.

In fact, under this protocol ordinary stochastic variation produced somewhat greater divergence on average.

That leaves a smaller, cleaner result:

> **The checkpoint is an executable branch point, but branchability does not imply that one chosen environmental manipulation dominates the system's intrinsic stochastic variation.**

That is exactly why the null matters.

---

## This Is Not Reproduction

We should resist that word.

We can restore the same checkpoint many times.

That resembles copying.

But the copying is performed by our experimental infrastructure.

Nothing here establishes autonomous reproduction.

The useful property is narrower:

> **Digital state can be duplicated as an exact starting condition for controlled counterfactual experiments.**

That is already powerful enough.

---

## The Crystal Now Has a Recoverable Past

Chapter 14 ended with:

```text
PRESENT MORPHOLOGY
→ SOME SOURCE INFORMATION SURVIVES

TEMPORAL ORDER
→ NOT RECOVERABLE
```

We did not solve that by forcing more temporal information into morphology.

We introduced a separate historical mechanism.

Now we have:

```text
CURRENT PROCESS STATE
+
EVENT HISTORY
```

which provides two complementary capabilities:

```text
STATE
→ CONTINUE

HISTORY
→ RECONSTRUCT
```

Together:

```text
PAST
↓
PRESENT
↓
POSSIBLE FUTURES
```

But those arrows mean different things.

The past can be reconstructed.

The present can be resumed.

The future can be branched.

That is something Digital Crystal v1 did not possess in Chapter 14.

---

## A Past Without Memory

It is tempting to call this memory.

I do not think we have earned that yet.

We have built:

```text
storage
checkpointing
history
replay
restore
branching
```

But the crystal itself does not inspect the record.

It does not ask:

> What happened before?

It does not change its behavior because of an earlier event stored in the log.

The history exists.

The process does not yet consult it.

So for now:

> **The Digital Crystal has a recoverable past.**

Not memory.

Not learning.

A past.

That is enough.

---

## What Survived the Hypothesis?

The chapter began with a simple problem:

```text
the crystal has a present
but
the present does not preserve chronology
```

Chapter 14 had already shown that final morphology contains some information about the conditions under which the crystal formed, but not enough to reconstruct temporal ordering.

Chapter 15 asked a different question:

> What information must survive if the process is to continue exactly, and what information must survive if its formation history is to be reconstructed?

The answer turned out to contain two distinct mechanisms.

### The checkpoint phenomenon

A complete checkpoint can be serialized, restored and continued exactly.

Across the validation runs:

```text
30 / 30 exact restores
```

The restored process reproduced:

```text
the same cells
the same attachment decisions
the same population trajectory
the same final process state
```

But visible morphology alone was not sufficient.

The same occupied structure could lead to a different future when hidden continuation variables differed.

So:

```text
VISIBLE FORM
≠
EXECUTABLE STATE
```

This is not merely an implementation lesson.

It tells us that the future of the Digital Crystal depends on information that is not necessarily visible in the current morphology.

### Phenomenon record

**Phenomenon:** Executable hidden state

**Status:** **SUPPORTED**

**Current bounded description:**

> Digital Crystal v1 requires continuation-relevant state beyond visible morphology for exact future replay. A complete checkpoint is sufficient for exact continuation, while morphology alone is not.

The experimentally identified continuation-relevant components include:

```text
occupied structure
RNG continuation state
environmental sequence position
```

while birth-time metadata behaves differently:

```text
birth time
→ historical information

birth time
→ not required for same occupied-set continuation
```

That gives us another important distinction:

```text
HISTORICAL INFORMATION
≠
CAUSALLY ACTIVE CONTINUATION STATE
```

### State and history are different computational objects

The event-log experiment exposes the other half of the chapter.

The stored history reconstructs:

```text
96 / 96 morphology states exactly
```

but that event history does not restore the historical RNG state required for exact stochastic continuation.

So the two representations answer different questions:

```text
CHECKPOINT
→ what is required to continue from here?

EVENT HISTORY
→ how did the present morphology arise?
```

or more compactly:

```text
STATE
→ FUTURE

HISTORY
→ PAST
```

They overlap, but they are not interchangeable.

This gives us a second project-wide distinction:

> **A process can preserve enough information to reconstruct its past without preserving the continuation state required to regenerate its exact future from that reconstruction alone.**

### The implementation failure revealed a deeper rule

The accidental dependence on Python `set` iteration order matters here too.

Before canonicalization, the simulation contained an undeclared continuation variable:

```text
Python container traversal order
```

Two mathematically equivalent reconstructed states could consume the same random draws in different orders and diverge.

That was not Digital Crystal physics.

It was implementation state leaking into the experiment.

Once frontier traversal was canonicalized, exact restore became reproducible.

This gives us a methodological phenomenon worth carrying across the project:

> **Scientific state must be separated from implementation state.**

If hidden program details influence outcomes, they must either be promoted into the declared model or eliminated.

### Connection to the Lossy-History Principle

Chapter 15 also sharpens the result from Chapter 14.

Chapter 14 showed:

```text
coarse source characteristics
survive in morphology

exact temporal order
does not
```

Chapter 15 shows that this loss is not inevitable to the digital substrate as a whole.

The chronology can be preserved perfectly if we use an explicit event history.

So the stronger cross-chapter picture becomes:

```text
MORPHOLOGY
→ lossy historical integration

EVENT LOG
→ exact formation-history reconstruction

CHECKPOINT
→ exact continuation
```

That matters because it tells us that different representations preserve different slices of the past.

The substrate gives us several native computational affordances:

```text
serialization
checkpointing
event logging
replay
branching
```

We do not need to force all historical information into visible form.

### Counterfactual branchability survives, dominance does not

The checkpoint also provides an executable branch point.

One exact saved state can be restored into multiple controlled futures.

That property survives.

But the stronger environmental-divergence interpretation does not.

Different prescribed future environments produced measurable divergence, yet that divergence did not exceed ordinary stochastic continuation variation under the frozen comparison.

So:

```text
EXECUTABLE BRANCHABILITY
SUPPORTED

ENVIRONMENTAL MANIPULATION
DOMINATES STOCHASTIC DIVERGENCE
NOT SUPPORTED
```

Again, the failed interpretation does not erase the underlying capability.

### What this phenomenon does not establish

The surviving phenomena do **not** establish:

- cognitive memory,
- learning,
- adaptation,
- autonomous reproduction,
- a mathematically minimal state representation,
- a biological genome analogue,
- or life.

They establish something narrower and more computationally native:

> **A Digital Crystal can possess hidden executable state sufficient for exact continuation, an explicit history sufficient for exact morphology reconstruction, and a checkpoint that functions as a reusable counterfactual branch point. These are distinct capabilities carried by distinct representations.**

This phenomenon should now be tracked independently of the chapter's stronger historical or environmental interpretations.

---

## Evidence Ledger

| Claim                                                             | Status            | Evidence                                              |
| ----------------------------------------------------------------- | ----------------- | ----------------------------------------------------- |
| Canonicalized model survives state serialization/reconstruction   | **SUPPORTED**     | one-step and 48-step invariant pass                   |
| Complete checkpoint resumes exact trajectory                      | **SUPPORTED**     | identical process and morphology hashes               |
| Exact restore generalizes across tested seeds                     | **SUPPORTED**     | `30/30` exact                                         |
| Visible morphology alone is sufficient continuation state         | **FAILED**        | 30-cell divergence                                    |
| RNG state matters for exact continuation                          | **SUPPORTED**     | 28-cell divergence                                    |
| Signal cursor matters at fixed horizon                            | **SUPPORTED**     | 27-cell divergence                                    |
| Birth-time metadata affects future occupied-set growth            | **FAILED**        | 0 differing occupied cells                            |
| Birth times function as historical metadata in v1                 | **SUPPORTED**     | history differs while geometric continuation does not |
| Event log reconstructs morphology trajectory                      | **SUPPORTED**     | `96/96` trajectory hashes                             |
| Event log reconstructs historical RNG state                       | **NOT SUPPORTED** | additions alone do not contain RNG history            |
| State and history are operationally distinct                      | **SUPPORTED**     | one continues; one reconstructs                       |
| Checkpoint is an executable branch point                          | **SUPPORTED**     | controlled alternative continuations                  |
| Different forcing produces divergence beyond stochastic variation | **NOT SUPPORTED** | treatment mean `<` stochastic-null mean               |
| Checkpoint representation is mathematically minimal               | **UNTESTED**      | only sufficiency/ablations tested                     |
| Stored history is cognitive memory                                | **NOT CLAIMED**   | process does not consult history                      |
| Crystal learns or adapts from history                             | **NOT CLAIMED**   | no such mechanism                                     |
| Crystal is alive                                                  | **NOT CLAIMED**   | evidence insufficient                                 |

---

## Bounded Claims

From this chapter we can reasonably claim:

1. **Exact continuation** — A complete Digital Crystal v1 checkpoint can be serialized, restored and continued without altering the stochastic trajectory.

2. **Reproducibility across runs** — Exact restore succeeded in `30/30` independent validation runs.

3. **Morphology is not complete state** — Identical visible structure can produce a different future if relevant hidden continuation variables differ.

4. **RNG state matters** — Stochastic continuation state affects exact future growth.

5. **Environmental position matters** — Signal position affects exact continuation even when the number of future updates is held fixed.

6. **Birth time is history, not growth state in v1** — Changing birth metadata alone does not alter the future occupied-cell trajectory.

7. **History can reconstruct morphology** — The explicit event log reconstructs the recorded formation trajectory exactly across `96/96` states.

8. **State and history are operationally distinct** — The checkpoint supports continuation; the event log supports reconstruction.

9. **A checkpoint is an executable counterfactual branch point** — One saved state can be reused to generate controlled alternative continuations.

10. **Environmental branching did not exceed stochastic divergence** — Under the tested protocol, changing future forcing did not produce more divergence than ordinary stochastic continuation variation.

That is where the evidence stops.

---

## Something Else Has Happened

There is one more consequence.

Our history is made from events.

Until now those events stay inside the experimental record.

```text
CRYSTAL
↓
EVENT
↓
HISTORY
```

But an event does not have to remain internal.

One process can emit one.

Another process can receive it.

The event does not need to contain language.

It does not need semantics.

It may contain almost nothing.

```text
one bit
a pulse
a number
```

And if one process can change the conditions experienced by another, then the environment no longer needs to come entirely from outside the system.

Something generated inside one process can become part of another process's world.

```text
CRYSTAL A
↓
EVENT
↓
CRYSTAL B
```

But Chapter 13 taught us to be careful with correlation.

Chapter 14 taught us that state is not history.

And this chapter taught us that a branch can diverge without the environment being the dominant cause.

So we should not call the next thing communication merely because we connect two systems.

The next question has to be smaller:

> **Can an event emitted by one Digital Crystal reliably change another?**

The crystal has a past.

**Next, we let the crystals hear each other.**
