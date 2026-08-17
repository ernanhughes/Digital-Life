+++
title = "08: The Crystal Gets a Past"
date = "2026-08-14T10:00:00+01:00"
draft = false
description = "A saved state can continue the Digital Crystal exactly, an event history can reconstruct how it formed, and a single received bit can redirect its future. None of that is memory yet."
weight = 8
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "State", "History", "Checkpointing", "Causality", "Counterfactuals"]
series = ["Digital Life From First Principles"]
+++

At the end of the last chapter the Digital Crystal could tell us something about the world that formed it.

Hide the forcing process, show only the final shape, and the family of that process could be recovered well above chance.

Then we asked a harder question.

> What happened first?

We took exactly the same environmental values and rearranged them in time. Smooth. Bursting. Periodic. Alternating. Random.

The final morphology could not reliably tell them apart.

SAME VALUES
+
DIFFERENT ORDER
↓
TEMPORAL ORGANIZATION
NOT RECOVERED UNDER THE TESTED READOUT
```

The crystal had accumulated consequences of its past. Its final morphology had not given us a reliable readout of temporal order.

So the previous chapter ended with an instruction rather than a conclusion: give the process a way to keep what happened.

That sounds like a storage problem.

But storing more information would be easy. The difficult question is deciding which information actually constitutes a computational past.

Before we build memory, we need to discover what a future can still depend on.

So the question for this chapter is deliberately small:

> **What must a computational process preserve before its past can become available to its future?**

Notice that this is not the same as asking how to build memory. We have not earned that word, and we do not yet know what it would mean here. What we can do is take the words that ordinary language collapses into one — state, history, record, influence, signal, message, memory — and pull them apart until each of them names a different computational property.

The experiments will force those words apart.

---

## The Present Is Not the Past

The Digital Crystal already has a present. At any moment its occupied set contains the cells that currently exist, and every one of those cells exists because of something that happened earlier.

So the past clearly mattered.

But the previous chapter taught us a distinction that is easy to state and easy to forget:

> **Past contributed to present does not imply present contains a recoverable record of the past.**

A footprint exists because someone walked there. The footprint is not the walk.

Likewise, the crystal's current shape contains consequences of earlier events without necessarily preserving the sequence of those events.

A consequence of the past is not yet a record of the past.

Two ideas are tangled together here, and the rest of the chapter depends on separating them:

```text
STATE
→ what must I know to continue from here?

HISTORY
→ what must I know to reconstruct how I got here?
```

Those are different questions. There is no guarantee that the same information answers both. There is no guarantee that either of them is visible in the picture.

We can test all of that.

---

## Stop It

Begin with state, because state has an operational definition available:

> **A state representation is sufficient if it contains enough information to continue the process faithfully from here.**

That wording is careful. We are not claiming to know the smallest possible state of a Digital Crystal. We are asking whether a particular stored representation is sufficient — a question an experiment can answer.

Take the frozen Digital Crystal from Chapter 4 and run it for 96 steps. At step 48, save everything we currently believe the process needs in order to continue:

```text
occupied cells
birth-time metadata
current timestep
current signal position
random-number-generator state
model parameters
```

Not a screenshot. Not merely the visible crystal.

Save the process, destroy the running instance, reconstruct it from the saved state, and continue.

{{< figure
src="/images/books/digital-life/ch15-01-reference-and-checkpoint.png"
alt="The Digital Crystal input signal with a checkpoint at step 48, together with the crystal at the checkpoint and its final state at step 96."
caption="The continuous reference trajectory. The midpoint checkpoint will be restored, damaged and replayed in the experiments that follow."

>}}

Then demand something much stronger than visual similarity.

If the checkpoint is sufficient, the restored process should not resemble the uninterrupted one. It should reproduce it:

```text
the same cells
the same attachment decisions
the same population trajectory
the same final process state
```

Exact continuation, or the representation was incomplete.

---

## The State We Had Not Declared

The first attempt failed.

The checkpoint restored a crystal that looked identical.

Then its future diverged.

The obvious reading was that something important was missing from the checkpoint. But a second result contradicted that. When the same state was rebuilt *without* passing through serialization, continuation was exact. Whatever was going wrong was happening at the implementation boundary, not in the model.

The culprit was mundane. Candidate attachment sites were held in a Python `set`, and the growth loop walked that set drawing one pseudo-random value per candidate. A set has no scientific ordering. Two sets can contain exactly the same cells and iterate them in different orders after reconstruction.

Which meant that:

```text
same mathematical cells
+
same RNG state
+
same signal
```

could still send random draw #1 to a different candidate in each run, and every draw after it to a different candidate again.

The experiment had quietly acquired an undeclared variable: implementation order.

That was not part of the Digital Crystal we intended to study. It was an accidental property of the program running it.
 We removed it by canonicalizing the traversal — candidates are visited in sorted order — and added an invariant that serializing and reconstructing a state must produce both the same one-step continuation and the same complete remaining continuation before any experiment is allowed to run.

The debugging detail belongs to the research layer. The lesson does not:

> **If future behaviour depends on hidden implementation state, that state belongs in the experimental definition whether or not it appears in the visualization.**

Either declare such state as part of the model or remove its influence.

What cannot remain is a variable that is absent from the scientific description and decisive in the result.

---

## Start Again

With traversal canonicalized, the checkpoint experiment becomes meaningful.

Save at step 48. Destroy the running process. Load from storage. Continue to step 96.

```text
exact final morphology            True
exact final process state         True
population trajectory identical   True
attachment trajectory identical   True
symmetric-difference cells        0
```

{{< figure
src="/images/books/digital-life/ch15-02-exact-restore.png"
alt="The final continuously run Digital Crystal beside the final crystal produced after checkpoint, storage, restore and continuation."
caption="Continuous execution and checkpoint → restore → continue produce the same trajectory, cell for cell."

>}}

And this was not one lucky run. Repeated across 30 independent runs, the result was 30 out of 30 exact.

So we have earned the first claim of the chapter:

> **The stored checkpoint representation is sufficient for exact continuation of the stochastic process.**

Note what is *not* claimed. We have not shown this is the minimal such representation. Sufficiency is what the experiment tested, so sufficiency is what we get.

There is something distinctly computational about this result.

We stopped the process, wrote down its state, destroyed the running instance, restored it, and recovered exactly the future it would otherwise have had.

Not approximately.

Not statistically.

Exactly.

That is not a biological mechanism copied into software. It is an affordance of the computational substrate itself.

---

## What the Picture Cannot Show

Now damage the checkpoint deliberately, one component at a time, and see which damage the future notices.

Every variant gets exactly 48 continuation updates, so that moving the environmental cursor does not accidentally shorten the experiment.

**Remove the random state.** Same morphology, same birth metadata, same timestep, same signal position, different stochastic continuation state:

```text
symmetric-difference cells    28
```

Small, but not zero. Exact continuation fails.

**Move the environmental cursor.** Same morphology, same RNG state, same number of remaining updates, but the process now sits at position 45 in the signal instead of 48:

```text
symmetric-difference cells    27
```

So where the process sits in its environment is part of its continuation conditions, not merely historical context.

**Replace the birth times.** Keep occupied cells, RNG state, signal cursor and timestep; scramble the metadata recording when each cell appeared:

```text
symmetric-difference cells     0
```

Exact. The growth rule never consults birth times when deciding the next attachment, so they can be wrong without the geometry noticing.

**Save only the picture.** Preserve the visible occupied structure and reconstruct everything else incorrectly:

```text
symmetric-difference cells    30
```

The visible shape at the checkpoint was identical. The future was not.

{{< figure
src="/images/books/digital-life/ch15-03-state-omission.png"
alt="Comparison of final-state divergence after restoring the full checkpoint, changing RNG state, shifting the signal cursor, changing birth metadata, or restoring morphology only."
caption="Visible morphology is insufficient for exact continuation. Stochastic state and environmental position affect future growth; birth-time metadata does not affect the occupied-set continuation."

>}}

Two distinctions fall out immediately.

The first:

```text
VISIBLE FORM
≠
EXECUTABLE STATE
```

Two Digital Crystals can be pixel-for-pixel identical and still be in different states, because the information that decides their futures is not all information that appears in the rendering. Anything looking at the picture — including us, including any classifier we train — is looking at a projection of the state, not the state.

The second is subtler:

```text
HISTORICAL INFORMATION
≠
CAUSALLY ACTIVE CONTINUATION STATE
```

Birth times are real information about the past. They are stored, they are accurate, and the future is entirely indifferent to them. Information about history can sit inside a process without being part of what the process does next.

That distinction will matter when we eventually ask whether stored history has causal leverage.

So the useful operational idea is:

> **Continuation state is the information required to reproduce the process's future under the same later conditions.**

Not whatever information happens to exist in our data structures, and not whatever information sounds philosophically important.

---

## Replay What Happened

The checkpoint answers *where are we now*. It says nothing about *how did we get here*.

For that we record events. At each growth step we store the step index, the input value, the cells that appeared, the resulting population and a hash of the resulting morphology:

```text
t1 → these cells attached
t2 → these cells attached
t3 → these cells attached
...
```

Then we test the record the way we tested the checkpoint — by demanding that it be sufficient for something.

Do not rerun the growth rule. Instead take the recorded event stream, apply each step's additions to a bare lattice, recompute the morphology hash, and compare it against the hash recorded at the time.

Across 96 recorded steps:

```text
96 / 96 morphology hashes match
```

{{< figure
src="/images/books/digital-life/ch15-04-history-replay.png"
alt="Step-by-step comparison showing that every morphology hash produced by replaying the Digital Crystal event log matches the recorded original trajectory."
caption="The event history reconstructs the recorded morphology trajectory exactly: 96 matching hashes out of 96."

>}}

The second claim of the chapter:

> **The explicit event history is sufficient to reconstruct the exact recorded morphology trajectory.**

And now the two mechanisms can be compared, which is the point of having built both.

The event history does not contain the historical stochastic state. Reconstruct the geometry from the log, hand it forward without the correct RNG continuation state, and exact continuation fails — by the same margin as the morphology-only checkpoint, because that is effectively what it is.

So the two representations answer different questions:

```text
CHECKPOINT
→ sufficient for exact continuation

EVENT HISTORY
→ sufficient for exact reconstruction of recorded morphology
```

or more compactly:

```text
STATE
→ FUTURE

HISTORY
→ PAST
```

They overlap. They are not interchangeable. A process can preserve enough information to reconstruct its past without preserving what it would need to regenerate its exact future from that reconstruction — and, as the birth-time result showed, the reverse holds too.

Notice what we have *not* done.

We have not invented a memory organ or searched for a special geometric region containing the past. We used computational affordances — checkpointing, event recording and replay — to separate continuation from reconstruction.

That is useful instrumentation.

It is not yet a property of the crystal itself.

---

## Whose Past Is This?

Here is the moment to be careful, because we have just built an impressive amount of machinery and none of it belongs to the crystal.

We have checkpointing, serialization, event logs, replay, restore, branching. The Digital Crystal has none of these. It does not read the log. It does not ask what happened earlier. Its attachment rule contains no term that consults a stored record, and if we deleted the entire database mid-run the growth would proceed exactly as before.

> **A system having a recorded history is not the same thing as the system possessing that history.**

The distinction to keep is between:

```text
WE CAN RECOVER ITS PAST
```

and:

```text
ITS PAST IS CAUSALLY AVAILABLE TO IT
```

Those are different claims, and only the first is supported. What we have built is instrumentation. Excellent instrumentation — it will carry the next six chapters — but instrumentation is a property of the laboratory, not of the specimen.

So **we** now have a recoverable account of the crystal's past.

The distinction in that pronoun matters.

The laboratory can recover it.

The crystal cannot yet use it.

---

## Fork the Future

The checkpoint has one more consequence, and it changes what kind of experiments become possible.

Restore the same saved state twice. Both copies begin with identical occupied cells, timestep, signal cursor and stochastic state. Nothing whatsoever differs. Then change what happens next in one of them.

```text
             SAME CHECKPOINT
                  |
          ┌───────┴───────┐
          |               |
     FUTURE A         FUTURE B
```

Here the computational substrate gives us something experimentally unusual: an exact executable branch point.

From one saved state we can construct alternative futures directly rather than search the world for approximately matched cases.

This is the single most valuable thing the checkpoint gives us, and everything in the second half of this chapter depends on it.

The branch point gives us control, but stochasticity immediately adds a warning.

Two futures can diverge even when we do not manipulate the mechanism we care about.

So from this point onward, every measure of counterfactual divergence needs a stochastic baseline.

That problem will become considerably more important later in the chapter.

---

## Before There Are Messages

Now the machinery gets pointed somewhere new.

Our history is made of events, and until now every event has stayed inside the experimental record. But an event does not have to remain internal. One process can emit one. Another process can receive it.

The temptation is immediate and enormous: two crystals, one event, therefore communication.

That word arrives carrying far more than we have earned. A sender. A receiver. A message. A channel. Meaning. Perhaps intention. We have established none of it.

So we begin with something smaller than a message.

> **Before there are messages, there are events that can alter another process.**

Call it a pulse.

The Digital Crystal itself stays frozen — same lattice, same local growth rule, same dependence on a scalar environmental input.

We add one coupling mechanism outside that rule: the laboratory derives a one-bit pulse from the sender's own growth dynamics, and that pulse perturbs the scalar forcing already used by the receiver.

```mermaid
flowchart LR
    S["Sender growth"] --> E["Endogenous one-bit event"]
    E --> R["Receiver forcing changes"]
    R --> P["Attachment probabilities change"]
    P --> M["Receiver morphology may diverge"]
```

The receiver does not get a sentence, a symbol, a sender identifier, a goal or an instruction. It gets a perturbation to a number it was already reading.

That design decision is the whole point. An earlier version of this experiment had coupled auxiliary oscillators to each crystal and looked for synchronization between them — which might have produced a perfectly interesting dynamical system while leaving the growth process we actually care about almost untouched. The question that matters is whether the bit reaches the thing we are studying.

---

## The Sender Does Not Fire on a Clock

It would be easy to build a trivial version of this:

```python
if step % 10 == 0:
    send(1)
```

Then every receiver responds to a programmer-supplied metronome, and the experiment demonstrates the existence of the programmer.

Instead the pulse is derived from the sender's own dynamics. At each step the coupling layer counts how many cells the sender attached and compares that value with its recent attachment activity. When current growth is unusually high relative to that recent baseline, the coupling emits a bit.

The pulse means only, operationally:

> an event derived from the sender's own changing growth dynamics occurred.

We assign it no semantics.

At this stage a `1` is a laboratory-defined event coupled from one process into another, and nothing more.

A practical confound appeared immediately: if both branches are allowed to approach lattice saturation, different trajectories collapse toward the same filled boundary.

That is not convergence of the process. It is information loss caused by the container.

So the experiment predeclared a saturation guard and stopped before the endpoint became boundary-dominated.

The detailed horizon calculation belongs in the reproducibility record. The principle is enough here:

> **Do not let the container erase the effect you are trying to measure.**

---

## One Bit Changes the Future

Now the intervention, and it is as clean as this book gets.

Take a receiver checkpoint. Fork it. Both branches begin with the same morphology, birth metadata, stochastic state, environmental forcing, timestep and remaining horizon. Change exactly one thing: one branch receives a bit, the other does not.

```mermaid
flowchart TD
    CK["Checkpoint: identical receiver state"] --> BIT1["BIT = 1"]
    CK --> BIT0["BIT = 0"]
    BIT1 --> FUT_A["Future A"]
    BIT0 --> FUT_B["Future B"]
    FUT_A --> COMP["Compare final morphology"]
    FUT_B --> COMP
```

This is an intervention rather than a correlation.

The bit is the only deliberately changed input between the paired branches.

If their outcome distributions differ, the intervention has causal effect.

How large the pathwise difference should be credited to that bit will turn out to require more care.

Repeated 120 times:

```text
paired interventions              120
produced morphology divergence  95.8%
mean normalized difference     0.1633
```

Five of the 120 interventions produced no final morphological difference.

That constrains the result usefully: the claim is not that every bit deterministically changes the receiver.
 The result is not *every received bit changes the receiver*. It is:

> **Changing one received bit, while holding receiver state, stochastic state and external forcing fixed, usually altered the receiver's subsequent morphology.**

The bit reaches the actual growth process.

We have established primitive causal transmission.

---

## The Crystal Can Hear a Pulse

Let that be exciting for a moment, because it should be.

One process generates an event out of its own activity. The event enters a second process. The second process develops differently as a result. Written down like that, it is very hard not to reach for the word communication.

So attack it.

The question we have answered is *can an event cause a change*, and the answer is yes. The question that would justify the stronger word is much harder:

> **Does something specific about the actual sender survive transmission in a way the receiver distinguishes?**

That takes a ladder of controls, each one removing a cheaper explanation than the last.

**Destroy the timing.** Keep the same number of bits, move them to different steps. If sender timing matters, the real stream should win. It does, and comfortably: the mean peak message-to-growth correlation for the real stream exceeded the shuffled stream by about 0.294, with a pairwise superiority near 0.980.

**Replace the sender with randomness.** Preserve the pulse count, place the pulses at random times. Real wins again — a difference of about 0.270, superiority about 0.977. So the receiver is not merely responding to how many bits arrived. Something about their arrangement matters.

At this point the story is going very well. Timing structure is real. The next control is the one that decides the chapter.

**Replace the sender with another sender.** Generate the pulse stream from a different Digital Crystal of the same type, with its own independent environment and its own growth trajectory, then force its pulse count to match the real sender exactly. Now the receiver sees either the actual sender's stream, or a same-class stranger's stream with the same number of pulses.

If anything about the actual sender is surviving transmission, the real stream should win.

```text
real minus unrelated      -0.015
pairwise superiority       0.457
```

It does not win. If anything the stranger is fractionally ahead, and the difference is small enough to be nothing at all.

**Preserve the intervals, destroy their order.** One more turn of the screw. Take the real sender's pulse stream, measure every gap between pulses, keep that exact multiset of intervals and permute their order. Same pulse count, same collection of gaps, same coarse burstiness, different chronology.

```text
real minus surrogate       0.010
pairwise superiority       0.473
```

Again, effectively nothing.

We also tried to rescue the claim with structure rather than statistics. Six crystals in a line, each one's pulses feeding the next, produced source-to-node correlations that looked convincingly like a signal travelling down a chain — until the shuffled-edge control produced almost the same pattern, with a mean absolute real-versus-shuffled difference of about 0.0164. A 6×6 board of thirty-six locally connected crystals told the same story: real minus shuffled neighbour correlation, about 0.0048. We had built connectivity. We had not built coordination.

```text
causal transmission
↓
sender-specific signalling?      NO
↓
chain-specific propagation?      NO
↓
board-level coordination?        NO
```

The bounded result:

> Within Digital Crystal v1, changing one received bit while holding receiver state, stochastic state and external forcing fixed can alter the receiver's subsequent morphology. Real sender-generated pulse timing produces stronger receiver relationships than shuffled or rate-matched random timing, but it does not outperform count-matched same-class sender replay or an interval-preserving surrogate. This supports primitive causal transmission, not sender-specific signalling.

Or, more briefly:

> **The crystal can hear a pulse. It cannot yet tell who spoke.**

---

## What the Failure Was Actually Telling Us

It would be lazy to summarize that as *communication failed*.

Look at what the control ladder actually mapped.

The receiver is sensitive to something destroyed by shuffled and rate-matched timing controls, but whatever that property is, it is also preserved well enough by a count-matched same-class sender and by an interval-preserving surrogate to erase the apparent advantage of the actual sender.

The experiment therefore does not isolate whether the surviving cue is burstiness, interval distribution, local pulse density or some other coarse temporal property.

What it does show is narrower: coarse timing structure matters, while sender identity and exact interval chronology were not established as recoverable.

The transmission is lossy.

And it rhymes with the experiment that brought us here:

```text
PREVIOUS CHAPTER

broad source characteristics
        RECOVERABLE

temporal organization
        NOT ESTABLISHED

THIS CHAPTER

coarse pulse-stream structure
        MATTERS

sender identity and exact chronology
        NOT ESTABLISHED
```

Twice now, different experiments have produced the same suggestive pattern:

```text
coarse temporal structure survives
fine temporal identity does not
```

---

## What Counts as the Same Random World?

There is a problem underneath everything we have just done, and it took us a while to see it.

Digital Crystal growth is stochastic. When we fork a checkpoint into a treated and an untreated branch, we hold the random-number state fixed and assume that gives us two versions of the same random world.

It does not. It gives us two versions of the same random *stream*.

Here is the mechanism. At each step the process builds a frontier of candidate cells, sorts it, and hands each candidate the next value from the stream. Perfectly reproducible — as long as both branches present the same candidates in the same order. But the intervention changes an attachment, which changes the frontier, which changes the sorted list. From that moment the two branches are consuming the same sequence of numbers in different places. Random value 27 lands on a different cell in each world, and every value after it is misassigned relative to its counterpart.

Imagine two identical card tables, each being dealt from an identically ordered deck. Remove one player from one table. That table does not merely lose a player: every card after the gap now lands in a different hand. Compare the two tables afterwards and you will measure an enormous difference — but much of it is not the consequence of the missing player. It is the consequence of the reshuffle you caused by removing them.

So some of the dramatic pathwise divergence in our early perturbation experiments could come from reassigned stochastic opportunities rather than from downstream amplification of the intervention itself.

The causal effect remained real.

Its apparent cascade had become suspect.

```text
SAME RANDOM STREAM
≠
SAME RANDOM OPPORTUNITIES
```

---

## The Cascade Shrinks

The fix is to key randomness to the event rather than to the sequence.

We built a second experimental runner in which each possible attachment opportunity draws its random value from a function of the seed, the absolute step and the cell coordinate. A cell at a given position at a given step then sees the same random value in both branches. If a cell exists in one branch and not the other, only *that* opportunity differs; a change to the frontier somewhere else no longer shifts every subsequent draw.

This is a common-random-number coupling, and it needs a clear label:

> **The cell-keyed runner is an experimental coupling, not a replacement for the canonical Digital Crystal.**

The canonical model remains the sequential stochastic process from Chapter 4. The keyed runner exists only to define a cleaner paired counterfactual — and before using it, we had to check we had not quietly built a different crystal. Across 96 runs per implementation, the omnibus morphology comparison between the two found no evidence of a gross distributional discrepancy (`p ≈ 0.922`), and four predeclared practical-compatibility margins all passed. That is not proof that the two processes are mathematically identical. It is enough to use the instrument for the experiment it was declared for.

Then repeat the pulse experiment under both couplings and compare like with like: how far apart do the two branches drift, relative to the drift you get from two entirely independent stochastic continuations?

```text
sequential RNG coupling      ≈ 87% of independent-divergence scale
cell-keyed CRN coupling      ≈ 11% of independent-divergence scale
```

```mermaid
flowchart TD
    A1["Pulse branch, sequential RNG"] --> B1["Frontier changes"]
    B1 --> C1["Stream misaligns"]
    C1 --> D1["Large apparent divergence"]
    A2["Pulse branch, cell-keyed CRN"] --> B2["Frontier changes"]
    B2 --> C2["Same cell sees same draw"]
    C2 --> D2["Small residual divergence"]
    D1 --> E["Much of the cascade was coupling artifact"]
    D2 --> F["Causal effect is real and much smaller"]
```

The pulse did not stop mattering. The intervention remains causal under both couplings. What collapsed was the apparent explosion of consequences that followed it.

This is not a footnote about random-number generators. It changes what a counterfactual trajectory *is* in a stochastic computational system:

```text
CAUSAL EFFECT
≠
COUPLING-INVARIANT PATHWISE DIVERGENCE
```

This forces another separation.

```text
difference between outcome distributions
≠
paired difference under a declared stochastic coupling
≠
distance between two particular trajectories
```

A related correction belongs here too. Before the coupling was fixed, four-pulse sequences appeared to produce a response that was substantially different from the sum of the individually measured pulse responses — an attractive result, since nonlinear integration of input history would be a genuinely interesting property. After the coupling fix we added a measurement-noise floor: how large a mean feature difference appears when you compare two finite samples drawn from the *same* unperturbed population? The floor came out around 0.045. The superposition residual was around 0.007.

The effect was several times smaller than our ability to see it. So:

```text
OBSERVED DISCREPANCY
≠
RESOLVED MECHANISTIC NONLINEARITY
```

Within the resolution of this experiment, the multi-pulse response stayed compatible with the sum of the isolated responses. The discrepancy existed.

The experiment could not resolve it as a mechanistic effect.

---

## Two Histories

Now, finally, the question the chapter has been walking toward.

We know a pulse changes the future. Does the *arrangement* of pulses leave a trace?

The naive comparison is too easy. Compare `11110000` against `10010010` and a classifier might succeed merely because one crystal was perturbed more recently than the other. That would be recency detection, not history retention.

So the confirmatory experiment used two codewords built to remove the cheap cues:

```text
A = 11100001      pulses at {0, 1, 2, 7}
B = 10001101      pulses at {0, 4, 5, 7}
```

Same number of pulses. Same first pulse. Same last pulse. Only the interior arrangement differs.

The confirmatory experiment was frozen before the result was inspected: codewords, stochastic coupling, primary endpoint and primary morphology measurement.

Secondary measurements were recorded but were not allowed to rescue a failed primary test.

That matters because otherwise every negative result becomes permission to keep searching until some alternative statistic succeeds.

Forty-eight independently generated receiver checkpoints. Two histories each. One question:

> **Does temporal arrangement leave a stable, reproducible morphological signature across independently generated receivers?**

---

## Different Futures, No Stable Signature

The two histories did not produce identical crystals. Immediately after the final pulse, the average normalized symmetric difference between paired futures was about:

```text
0.053     [0.048, 0.059]
```

So the interior arrangement of the pulses had real causal consequences. Rearranging when the bits arrived changed what the receiver became.

The population-level test asked for something stronger, and got nothing.

```text
primary angular test (9 features)     p = 0.7366
secondary test (24 features)          p = 0.9320
```

This was not a near miss.

The predeclared primary statistic showed no evidence of a stable history signature, and the wider secondary measurement did not recover one either.

The predeclared test did not support the hypothesis.

Not because the software failed.

Not because the preflight failed.

Not because the coupling failed.

The primary measurement simply did not recover the predicted population-level signature, and the secondary measurement did not rescue it.

The bounded result is:

> **Under the frozen protocol, changing the interior timing of four pulses while holding pulse count, onset and offset fixed did not yield evidence of a reproducible population-level morphology signature detectable by the predeclared angular measurement at the primary endpoint.**

That is a clean negative result for the predeclared test.

It is not evidence that temporal arrangement can never matter, and it does not mean the two histories had no consequences.

DIFFERENT HISTORY → DIFFERENT PARTICULAR FUTURE
SUPPORTED

DIFFERENT HISTORY → STABLE POPULATION-LEVEL SIGNATURE
NOT SUPPORTED UNDER THE PREDECLARED TEST

There is a tempting sentence here: *the crystal forgot the sequence*. We cannot say that. Forgetting presupposes something like memory to lose. What we can say is stranger and more useful:

> **A history can contribute causally to the present without remaining legible in the present.**

---

## A Past With Consequences

Put the three experiments side by side and a hierarchy appears that was not visible from any one of them.

```text
CAUSAL CONSEQUENCE
        ↓
PERSISTENT CONSEQUENCE
        ↓
SYSTEMATIC SIGNATURE
        ↓
RECOVERABLE INFORMATION

```

Every arrow is a new empirical claim.

The Crystal has crossed the first threshold repeatedly.

The experiments in this chapter show why none of the later thresholds follows automatically.

That is the shape of the chapter, and it is worth being clear that this is a chapter with a great deal in it. Several strong interpretations died. The phenomena underneath them did not.

The strongest surviving progression is:

```text
complete state
→ exact continuation

recorded events
→ exact reconstruction

earlier intervention
→ later causal consequence

different histories
→ different particular futures
```

Three distinctions now matter more than the rest:

```text
VISIBLE FORM
≠
EXECUTABLE STATE

RECORDED PAST
≠
CAUSALLY AVAILABLE PAST

CAUSAL CONSEQUENCE
≠
MEMORY
```

The single sentence the chapter has earned:

> **The past has become causally real before it has become memory.**

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Complete checkpoint resumes the exact trajectory | **SUPPORTED** | `30/30` exact restores; symmetric difference `0` |
| Visible morphology alone is sufficient continuation state | **FAILED** | 30-cell divergence |
| Stochastic continuation state matters for exact continuation | **SUPPORTED** | 28-cell divergence when removed |
| Environmental sequence position matters at fixed horizon | **SUPPORTED** | 27-cell divergence when shifted |
| Birth-time metadata affects occupied-set continuation | **FAILED** | 0 differing cells |
| Event history reconstructs the recorded morphology trajectory | **SUPPORTED** | `96/96` trajectory hashes |
| Event history restores historical stochastic state | **NOT SUPPORTED** | additions alone do not contain it |
| Checkpoint is an executable counterfactual branch point | **SUPPORTED** | controlled alternative continuations |
| A received one-bit event can alter receiver morphology | **SUPPORTED** | 120 paired interventions; 95.8% diverged |
| Real pulse timing beats shuffled and rate-matched timing | **SUPPORTED** | differences ≈ `0.294` and `0.270` |
| The actual sender matters more than a same-class sender | **FAILED** | difference `-0.015`; superiority `0.457` |
| Exact chronology matters beyond the same interval multiset | **FAILED** | difference `0.010`; superiority `0.473` |
| Influence propagates specifically through chain topology | **FAILED** | real-vs-shuffled ≈ `0.0164` |
| Local 6×6 topology produces organized signalling | **FAILED** | real-vs-shuffled ≈ `0.0048` |
| Pathwise divergence depends on stochastic coupling | **SUPPORTED** | ≈87% sequential vs ≈11% cell-keyed |
| Multi-pulse response is nonlinear | **FAILED** | residual `0.007` below measurement floor `0.045` |
| Matched pulse histories produce different particular futures | **SUPPORTED** | normalized difference `0.053` |
| Matched pulse histories leave a population-level signature | **FAILED** | `p = 0.7366`; secondary `p = 0.9320` |
| The crystal possesses or consults its recorded history | **NOT CLAIMED** | no mechanism consults the record |
| The crystal remembers, learns, communicates or coordinates | **NOT CLAIMED** | evidence insufficient |

---

## Put the Past Into the Material

So where, exactly, is the crystal's past?

Not in our checkpoint — that belongs to the laboratory. Not in our event log — the growth rule never reads it. Not in the morphology, which turned out to be a projection of the state rather than the state itself, and which could not be made to give up the arrangement of the pulses that shaped it.

And yet the past is unmistakably doing something.

A pulse changes an attachment.
That attachment changes the frontier.
The changed frontier alters later opportunities.
The process follows a different trajectory.

```text
event
↓
local consequence
↓
changed possibility
↓
later consequence
```

Which suggests the next experiment, and it is smaller than memory and more concrete than history.

So far, an occupied Crystal cell has almost no internal state.

It cannot be changed by experience and remain changed afterwards.

It cannot carry a persistent local distinction such as:

```text
this happened here
≠
this did not happen here
```

Any detailed record we currently possess lives outside the material:

```text
checkpoint
database
event log
```

What if experience changed the material itself?

Change the material.

Then remove the event that changed it.

If the material difference persists, remains accessible to later computation, and changes what the process does next, then the past will have acquired something it has not had anywhere in this chapter:

**an internal carrier.**

Not memory.

Not yet.

But finally a place inside the process where experience can remain causally available after the original event is gone.

> **Can experience change the material itself?**
