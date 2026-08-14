+++
title = "04: The Digital Crystal"
date = "2026-08-14T11:00:00+01:00"
draft = false
description = "We build the smallest laboratory that will hold an experiment: one seed, a hexagonal lattice, local attachment. Then we let an environment touch it and ask what the finished structure still knows."
weight = 4
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Crystal Growth", "Hexagonal Lattice", "Morphology", "Information", "Experimental Method"]
+++

Outlier was the wrong laboratory.

Not a wrong choice — the last two chapters were worth every page, and nothing in them is retracted. But by the end of the flocking investigation the problem was unmistakable. Geometry, ancestry, distance, expansion, local environment and interaction all arrive together in that world, arising from the same 512 bits, moving together, entangled beyond separation. Every control we built was an attempt to statistically undo an entanglement we could not experimentally prevent, and one entire regime stayed unresolved because the comparison we needed simply did not exist in the data.

Matching is what you do when you cannot intervene.

So we are going to build something we can intervene on. A world where the comparison is constructed rather than discovered — where we can run a system, run it again with exactly one thing changed, and attribute the difference to that thing.

There is one idea worth carrying across from Outlier, and it is much smaller than an organism:

```text
local computation
↓
repeated interaction
↓
characteristic larger-scale structure
```

That is the whole import. No reproduction, no individuality, no hierarchy. Just the observation that repeated local computation can produce persistent large-scale form.

What we want from the new system is a short list:

```text
every rule is known
every state can be inspected
one mechanism can be changed at a time
counterfactual worlds can be rerun
the full history can be preserved
```

And an equally important list of what we refuse to build:

```text
organism
memory
repair
reproduction
metabolism
individual
```

Not because those are uninteresting. Because implementing them and then discovering them is the cargo cult, and it would make everything downstream worthless.

The result is going to be almost embarrassingly small.

---

## One Seed

A hexagonal lattice. Every location holds `0` or `1`. Every location has six immediate neighbours.

At the centre, one occupied location:

```text
●
```

Everything else is empty.

The rule:

> **An empty location becomes occupied if at least one neighbouring location is occupied. Once occupied, it stays occupied.**

That is the entire system. There is no organism, no genome, no stored target shape, no energy, no resources, no reproduction, no death, no memory variable, no objective.

Hexagonal geometry is a convenience rather than a claim: six equidistant neighbours make local reasoning cleaner than a square grid's awkward mix of edge and corner adjacency. Represent locations as axial coordinates `(q, r)` and the six directions are just six offsets. The world is a set of occupied coordinates, and one update collects every empty location adjacent to something occupied and fills it.

Run it and the structure grows in expanding hexagonal shells.

{{< figure
    src="/images/books/digital-life/ch11-crystal-growth.gif"
    alt="A single occupied seed expanding across a fixed hexagonal lattice under one irreversible local growth rule."
    caption="A single occupied seed expands under one irreversible local growth rule."
>}}

Nothing anywhere says *make a hexagon*. After `t` updates, every location within hexagonal graph distance `t` of the seed is occupied, and the global shape follows from the neighbourhood topology plus uniform local propagation. No cell holds a blueprint. No controller measures the radius. Nobody draws the six sides.

That is the first small result, and it is worth naming precisely:

> **A single seed under a uniform local irreversible rule produces ordered growth whose global geometry is determined by the topology of the neighbourhood.**

---

## Growth Is Cheap

Now measure it rather than admiring it, because the population has a closed form. For a perfect hexagonal ball of radius `r`:

$$
N(r) = 1 + 3r(r + 1)
$$

giving 1, 7, 19, 37, 61 for the first five radii. The radius grows linearly with time; the area grows quadratically. The measured population tracks the law exactly.

{{< figure
    src="/images/books/digital-life/ch11-crystal-growth-curve.png"
    alt="Measured occupied-cell count of the growing crystal compared with the theoretical hexagonal growth law."
    caption="The apparent growth complexity has a simple explanation: the measured population follows the hexagonal-ball growth law."
>}}

So the structure gets steadily larger and not one bit more interesting. A million-cell structure from this rule is no more conceptually complicated than a seven-cell one; the generative description is identical, and only the number changes.

```text
larger
≠
more complex
```

Which is useful to establish early, because size is the cheapest possible impressive-looking result.

There is a second observation here that matters more than it appears to. This system can grow indefinitely. No mature size appears, no reproduction becomes necessary, no ageing emerges, nothing dies. In this toy world, at least:

```text
continued construction
≠
reproduction
```

A structure can persist and extend from one seed forever without producing anything resembling offspring. Chapter 00 asked whether reproduction might be a solution to a biological constraint rather than a requirement for organized persistence, and here is the smallest possible existence proof that continued process does not need it.

That is a substrate-first move, and it is the reason this laboratory is built around growth rather than around anything more ambitious. We get to study **continued process before reproduction** instead of assuming the biological ordering.

---

## The Laboratory Immediately Starts Lying to Us

Before adding anything, it is worth noting how quickly even this system tempts biological language — because it happens within one experiment.

Let the structure grow for twenty generations, then erase a region from its interior. Resume the same rule. The empty cells inside the hole touch occupied cells, so they become occupied; then their neighbours do; and soon the hole is gone.

{{< figure
    src="/images/books/digital-life/ch11-crystal-damage-triptych.png"
    alt="The digital crystal before perturbation, immediately after an interior region is removed, and several generations later."
    caption="Before, perturbation, and a later state. The missing region returns, but we have not yet earned the word repair."
>}}

It looks like healing. It is not.

The rule says any empty location adjacent to occupied structure becomes occupied, and that rule operates identically outside the structure and inside a hole. The system does not distinguish damage from ordinary frontier — there is no target morphology anywhere, nothing that could represent what the structure is supposed to look like. The hole closes because continued growth plus available empty space closes holes.

The control is straightforward: create a hole inside the structure and a matched empty region just outside it, with comparable occupied boundaries, and compare their filling rates. If the two are treated identically, there is no evidence of a damage response. Under this rule they are.

The observation survives; the interpretation does not:

> **The same local growth dynamics that expand the exterior also refill newly emptied interior regions.**

Less exciting, more informative, and a good reminder that a laboratory built specifically to avoid biological assumptions will still generate biological-sounding descriptions within about five minutes of being switched on.

Two other things this prototype showed, in passing, which later chapters will do properly. Permanent obstacles leave persistent structural traces while temporary ones get erased by continued growth — so a growing structure can be history-dependent without anything resembling memory. And when two seeds grow until their fronts meet, the merged binary state retains no record of which seed produced which region: multiple growth histories can produce a geometry that no longer reveals those histories.

Both of those get dedicated experiments later, with far better controls than a prototype deserves. What matters here is the third thing, which we are going to leave alone deliberately.

Growth that never stops eventually meets a limit. Put the structure in a bounded world and it fills it. Beyond space, our own implementation cost rises with the number of active locations, which hints at something less obvious — that a growing computational organization might run out of *attention* before it runs out of room. That question turns out to matter enormously.

We are not going to answer it here. Just note that continued growth will eventually force us to ask what becomes scarce, and move on.

---

## Can the Environment Leave a Mark?

The prototype answers its own question and then stops being interesting, which is the correct behaviour for a control. What we want next is genuinely different:

> **Can changing external conditions influence growth strongly enough to leave a persistent, measurable signature in the finished structure?**

That question is not askable of the prototype. Its rule is deterministic and saturating — every available location fills, every time. There is no room for an external signal to change which locally available events actually happen, because all of them happen.

So the model has to change, and this needs stating plainly rather than slipped in:

```text
PROTOTYPE

binary occupancy + hexagonal neighbourhood
+ irreversible growth + deterministic local attachment
```

```text
DIGITAL CRYSTAL v1

binary occupancy + hexagonal neighbourhood
+ irreversible growth + stochastic attachment
+ environmental forcing + fixed lattice anisotropy
+ crowding penalty
```

Each addition earns its place through the experiment we want to run. Stochastic attachment gives the forcing somewhere to act — if attachment is probabilistic, the environment can shift the odds. Anisotropy gives the lattice persistent directional structure. The crowding penalty stops attachment probability rising without bound simply because a location has many occupied neighbours.

These mechanisms are introduced *for* this experiment. They are not discoveries carried over from the prototype, and that has a consequence worth being strict about:

> **Results from the prototype do not automatically transfer to Digital Crystal v1.**

The hole-filling result above tells us nothing about how this stochastic model responds to damage. Different model, different claims, and everything from here has to be earned again.

The name arrives here as a label rather than an achievement. **Digital Crystal.** It cannot mean *a thing that looks like quartz*, and it cannot mean *anything arranged on a hexagonal grid* — those are visual definitions, and we know what happens when appearance substitutes for mechanism. A physical crystal acquires structure through repeated local interactions during formation, with the large-scale structure following from those interactions. So try the analogous idea computationally, as a provisional working definition:

> **A Digital Crystal is a local computational growth process in which characteristics of an external input become expressed as persistent, measurable morphology.**

Deliberately narrow. It says nothing about life, memory, learning, adaptation, reproduction, intelligence or agency. Its only virtue is that it can be tested, and might be false.

---

## Influence, Not Instruction

The prototype was:

$$
C_{t+1}=G(C_t)
$$

Now introduce an environmental forcing signal:

$$
C_{t+1}=G(C_t,E_t)
$$

The distinction that makes this an experiment rather than a graphics demo is what the signal is *not* allowed to do. It does not draw. Nowhere does anything say:

```python
if signal == "sine":
    draw_sine_shape()
```

That would be a strange plotting library with extra steps. The same growth mechanism operates under every source; the signal only changes the conditions under which individual local attachment events occur.

For a candidate frontier cell, attachment probability takes a form like:

$$
P(\text{attach})
=
\sigma\left(
a + bn + cE_t + dA - q
\right)
$$

where `n` is the occupied-neighbour count, `E_t` is the current environmental value, `A` is the fixed local anisotropy term, `q` is the crowding penalty, and σ maps the result into a probability. The growth parameters stay frozen throughout. There is still no target morphology, no global drawing routine, no stored description of what the structure should become.

The experimental constraint that makes the whole thing work:

> **The growth mechanism remains fixed while the source changes.**

Otherwise recovering the source would tell us nothing except that we had changed the machine.

The contrast with a conventional visualization is the cleanest way to see what is going on. A graph does:

```text
value → coordinate → pixel
```

The Digital Crystal does:

```text
value → local attachment conditions → many stochastic interactions → persistent morphology
```

The picture is not drawn from the signal. It is **grown under its influence**, through thousands of local events, none of which knows anything about the signal beyond the single scalar presented at that moment.

First, the least interesting possible check: does the generalized model still grow? Give it a constant signal, `E(t) = 0`, and run it. The baseline reached approximately 5,924 occupied cells at a maximum hex radius of 44, with 552 boundary edges.

{{< figure
src="/images/books/digital-life/ch14-01-baseline.png"
alt="Baseline Digital Crystal grown under a constant zero-valued environmental signal, shown alongside its input signal and population growth."
caption="Digital Crystal v1 produces a growing structure under constant forcing. This establishes only that the generalized model grows."
>}}

That proves nothing except that the machine runs. Which is all it needs to prove.

---

## Six Environments

Now hand exactly the same growth rule six different kinds of forcing:

```text
constant
sine
square
sawtooth
white noise
random walk
```

Within each family the individual instances vary — periods, phases, noise realizations, random-walk trajectories. At each growth step the structure receives only the scalar value currently presented to it. Not the family name, not the history, not the shape of the signal. One number.

{{< figure
src="/images/books/digital-life/ch14-02-source-signals.png"
alt="Example environmental signals used to drive Digital Crystal growth: constant, sine, square, sawtooth, white noise and random walk."
caption="Six forcing-process families. Digital Crystal v1 receives only the current scalar environmental value."
>}}

Then grow them.

{{< figure
src="/images/books/digital-life/ch14-02-source-gallery.png"
alt="Six Digital Crystals grown using the same local rule but driven by constant, sine, square, sawtooth, white-noise and random-walk signals."
caption="Same local growth mechanism, different forcing processes. The morphologies appear different, but appearance is only the start of the experiment."
>}}

They look different.

So what?

This is the same trap that has followed us since Chapter 1, and it is no less inviting for being familiar. *Different signals generate different crystals* would make an attractive demonstration and establish nothing. Perhaps one random seed happened to produce a larger structure. Perhaps square waves simply produce a higher mean attachment probability, and we are looking at area. Perhaps our eyes are busily categorizing noise, which they are extremely good at.

We need populations, not specimens.

---

## Six Hundred Crystals

One hundred each of constant, sine, square, sawtooth, white noise and random walk. Six hundred structures, all grown with the same rule, the same experimental horizon and the same measurement system, differing only in source instance and stochastic realization.

For each finished structure, 42 morphological measurements: area, perimeter, maximum radius, compactness, boundary roughness, bounding-box aspect, centroid displacement, radial and angular distributions, six-fold angular structure, boundary-radius variation, and so on.

The source signal is not among them. The measurement describes the finished object and nothing else.

Then hide the labels.

The question becomes concrete and slightly unnerving: hand over one finished crystal, say nothing about what grew it, and ask whether the forcing family can be recovered from morphology alone. Six classes, so random guessing succeeds 16.7% of the time. Train on part of the population, test on structures never seen before.

```mermaid
flowchart TD
    S1["Constant ×100"] --> G["Same fixed growth rule"]
    S2["Sine ×100"] --> G
    S3["Square ×100"] --> G
    S4["Sawtooth ×100"] --> G
    S5["White noise ×100"] --> G
    S6["Random walk ×100"] --> G
    G --> M["Morphology: 42 measured features"]
    M --> H["Hide source labels"]
    H --> C["Train on one subset"]
    C --> T["Test on unseen crystals"]
```

The held-out result:

```text
chance                 16.7%

random forest           52.2%
logistic regression     53.9%
```

{{< figure
src="/images/books/digital-life/ch14-06-source-accuracy.png"
alt="Held-out classification accuracy for recovering the source process from Digital Crystal morphology compared with the six-way chance baseline."
caption="Source-process family can be recovered from held-out Digital Crystal morphology substantially above the 16.7% chance baseline."
>}}

Roughly three times chance, on structures the model has never encountered.

Two things about this deserve attention. First, two very different classifier families land in the same region, which means we are not relying on one unusual model finding one unusual boundary. Second, the confusion matrix shows the retained information is uneven — some forcing families leave far more distinctive morphological signatures than others.

{{< figure
src="/images/books/digital-life/ch14-06-source-confusion.png"
alt="Confusion matrix showing predictions of source-process family from final Digital Crystal morphology."
caption="Source recovery is substantial but incomplete. Some forcing families leave more distinctive morphological signatures than others."
>}}

The claim to keep is smaller than the excitement it produces:

> **The final morphology contains information that makes forcing-process family recoverable substantially above chance.**

Not *the crystal remembers its history*. Not *the crystal understands the environment*. Something happened during formation, and the finished structure still carries enough of it to be read.

---

## Attack the Boring Explanation

The obvious deflation is that the classifier is not detecting anything about the *process* at all — merely some trivial aggregate. Square waves might spend more time at high values, raise mean attachment probability, and produce larger structures. Then all we would have discovered is that bigger signals make bigger crystals.

So normalize the varying signals to approximately the same mean, leave the constant control at zero, and check whether the morphology populations still separate. Standardized distances of each class centroid from the constant population:

```text
sine          4.45
square       13.82
saw           2.44
white noise   2.40
random walk   1.40
```

They remain measurably distinct. Mean forcing alone cannot explain the source-family result — variation matters, not just level.

One more obvious worry: perhaps recovery works only at one carefully chosen forcing strength, and we happened to find it. Varying the forcing strength while leaving the rest of the growth mechanism untouched, held-out random-forest accuracy was:

```text
forcing         accuracy

0.75             34.1%
0.85             43.2%
0.95             50.0%
1.00             52.3%
1.05             52.3%
1.15             63.6%
1.25             43.2%
```

against a 16.7% chance baseline throughout.

Discipline here, because this sweep is noisy and it would be easy to over-read. There is no clean monotonic trend; 1.15 outperforms 1.25 substantially, and a seven-point sweep cannot tell us the shape of a response curve. We are not entitled to say that increasing forcing predictably increases recoverability, and we do not know the optimum.

What survives is narrow and sufficient:

> **Source-family information remains recoverable above chance at every tested forcing strength in this sweep.**

The phenomenon is not an artefact of one lucky parameter.

---

## Maybe It Recorded What Happened

Here is where it becomes tempting.

We have a fixed local process, an external environment, and a finished structure from which the character of that environment can be recovered well above chance. The mean does not explain it. The result holds across forcing strengths. It survives on structures the classifier has never seen.

The available sentence is *the crystal has recorded its environmental history*, and it is not an absurd thing to think. Something about what happened during formation is still present in the finished object. That is what a record is.

Notice how little distance there is between the result we have and the claim we want. The result says information about the *kind* of environment survives. The claim says the *history* survives. Those feel like the same statement, and the whole book so far suggests they are not.

There is also a specific reason for suspicion. Consider sine and square forcing. They differ in temporal ordering — but they also differ in value distribution, time spent near extrema, autocorrelation and transition structure. If the classifier is picking up broad statistical properties of the values experienced during growth, that is still a real result. It is a different result.

So we test the promotion rather than accepting it.

---

## Destroy Time

Take a source sequence and shuffle it.

```text
0.7   0.2  -0.3   0.9  -0.8  ...

becomes

-0.3   0.9   0.7  -0.8   0.2  ...
```

The shuffled version preserves the same values, mean, variance, minimum, maximum and histogram. Only the temporal ordering is destroyed.

If the finished morphology retains recoverable information about chronology, crystals grown from ordered and shuffled sequences should be distinguishable. Binary chance is 50%.

```text
chance                 50.0%

random forest           51.3%
logistic regression     51.7%
```

{{< figure
src="/images/books/digital-life/ch14-07-order-accuracy.png"
alt="Classification accuracy for distinguishing crystals grown from ordered signals versus shuffled versions containing the same signal values."
caption="Ordered-versus-shuffled source histories cannot be recovered above chance in this experiment."
>}}

Nothing. Neither classifier reaches beyond roughly 52%, and the confusion matrix tells the same story with no useful separation anywhere in it.

Be precise about what this does and does not establish. It does not prove that no conceivable measurement could ever recover temporal information from this model. It establishes:

> **Our morphology representation and classifiers do not recover ordered-versus-shuffled history above chance under this protocol.**

Which is already enough to kill the claim we were drifting toward.

But the control can be stronger, and should be. A sine wave and a square wave do not merely differ in ordering — their distributions differ too, so the successful source-family classifier may be leaning primarily on distributional structure. We can remove even that.

Construct one fixed multiset of 72 values. Every condition receives **exactly the same values** — not approximately the same distribution, not merely matched mean and variance, the identical multiset. Only the temporal arrangement changes:

```text
RANDOM        random permutation
BLOCK         low values grouped, then high values grouped
ALTERNATING   low, high, low, high...
SMOOTH        neighbouring values change gradually
BURST         quiet periods interrupted by concentrated excursions
PERIODIC      values arranged into a repeating temporal motif
```

{{< figure
src="/images/books/digital-life/ch14-09-matched-temporal-signals.png"
alt="Six temporal organizations built from exactly the same set of input values: random, block, alternating, smooth, burst and periodic."
caption="Exactly the same values, reorganized in time. Distribution is held fixed; temporal organization changes."
>}}

This is the comparison Outlier could never have given us. Same values, same growth rule, same everything — one variable changed deliberately, and the counterfactual world constructed rather than found.

Then grow them, with the model frozen. No parameter tuning, no attempts to rescue the hypothesis.

{{< figure
src="/images/books/digital-life/ch14-09-matched-temporal-crystals.png"
alt="Digital Crystals grown from six differently ordered signals containing exactly the same input values."
caption="The temporal forcing histories differ radically, but their final morphologies are much harder to distinguish."
>}}

One safeguard matters enough to state. All temporal arrangements built from a single value set stay together during the train/test split, so the classifier cannot train on one ordering of a value set and then be tested on a different ordering of that same set. Held-out value sets are genuinely unseen. Without that, a subtle leakage path would let the model recognize the values rather than the ordering.

With the multiset held exactly constant, temporal organization is not recoverable above chance under the tested classifiers.

The stronger experiment fails as well.

---

## A Crystal Is Not a Tape Recorder

This is the point where the result becomes better than the idea we started with.

We had imagined:

```text
environmental history
↓
crystal
↓
history written into morphology
```

What the experiments support is narrower:

```text
environmental statistics
↓
local dynamics
↓
persistent morphology
```

The exact sequence is largely lost under the measurements and classifiers we tested. Some broader characteristics survive.

Which is, when you look at it, strangely appropriate. Inspect a physical crystal and its structure may reveal a great deal about the conditions under which it formed — temperature regime, rate, impurities, pressure. It does not contain a frame-by-frame movie of formation. Nobody expects to read Tuesday off a quartz sample.

Our Digital Crystal turns out to be closer to that than to a recording device. A morphological statistic, not a tape recorder.

Which means the failure has told us something the success could not: what *kind* of information this substrate preferentially preserves.

---

## State Is Not History

The crystal obviously has state. At time `t`, the structure depends on earlier attachment events; a cell added at step 10 may still be there at step 70; past events contributed causally to the present in the most direct way possible.

None of that implies the present is a useful record of the past.

Consider two sequences, `A B C D` and `D B A C`. Both influence the process. Both alter the final state. But if the final state contains no recoverable information distinguishing which ordering occurred, then the process has accumulated consequences without retaining chronology.

That is where Digital Crystal v1 stands, and it separates two things our vocabulary bundles together:

```text
past contributed to present
        SUPPORTED

source family recoverable
        SUPPORTED

mean alone explains source effect
        FAILED

exact temporal order recoverable
        NOT SUPPORTED

complete chronology retained
        NOT ESTABLISHED
```

So:

```text
HISTORY-DEPENDENT
≠
HISTORY-READABLE
```

A process can be thoroughly shaped by its past without being a record of it.

The best current description of what this substrate does is *lossy integration*:

```text
external forcing
↓
many irreversible local attachment events
↓
aggregate structural bias
↓
persistent morphology
```

The process integrates the consequences of the past, and the integration discards information — apparently preserving broad statistics of the forcing more readily than exact chronology. Which suggests a provisional principle, offered for comparison with later experiments rather than as a law:

> **Irreversible growth can preserve coarse historical structure while discarding fine temporal identity.**

One boundary statement, once, and then we trust the reader with it: nothing here establishes memory in the strong sense, learning, adaptation, interpretation of the environment, a stored event log, reproduction, individuality, or life. What it establishes is that a fixed local growth process can turn differences in environment into persistent, measurable, recoverable differences in form.

That is a real result. It does not need help.

---

## The Digital Crystal

The name was a label at the start of the experiment. It has now earned a little weight, and the definition it earned is the modest one:

> **A Digital Crystal is a local computational growth process in which characteristics of an external input become expressed as persistent, measurable morphology.**

```mermaid
flowchart TD
    A["ENVIRONMENTAL INPUT"] --> B["FIXED LOCAL DYNAMICS"]
    B --> C["DIGITAL CRYSTAL"]
    C --> D["PERSISTENT MORPHOLOGY"]
    D --> E["SOURCE-FAMILY INFORMATION RECOVERABLE"]
    D --> F["TEMPORAL ORDER NOT RECOVERED"]
```

The definition is small because the stronger version failed, and the failure is what makes the small version trustworthy. We tried to establish that the crystal records its temporal history, ran the strongest test we could construct, and did not get it.

It is worth noticing what just happened procedurally, because it is the thing Outlier could not offer. We wanted to know whether temporal order mattered. So we built two worlds identical in every respect except temporal order, and looked at the difference. No matching. No searching a complicated world for naturally occurring comparisons. No unresolved regime where the data happened not to contain what we needed.

That is what the laboratory is for, and it worked on its first serious question.

---

## Give It a Past

We asked the crystal what happened to it.

It could answer something weaker: *I can tell you something about the kind of conditions under which I formed.*

So we asked what happened first, and under every experiment we ran the answer was effectively: *I don't know.*

That is not a disappointing end to the Digital Crystal. It identifies the next missing capability with unusual precision. The crystal has a present, and the present carries information about the conditions that produced it. What it does not have is a past that can be distinguished from another possible past.

So the next step is not to make it intelligent. Not to give it goals. Not reproduction. Not learning.

Something much smaller.

Give it a way to **keep what happened**. Not to interpret it, not to learn from it, not to decide what it means — merely to preserve enough that one history remains distinguishable from another.

Because before a process can do anything with its past, there has to be a past left to do anything with.
