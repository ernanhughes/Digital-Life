+++
title = "7: What Survives Material Loss?"
date = "2026-08-14T14:00:00+01:00"
draft = false
description = "Remove the guarantee that occupied material stays occupied, and the Digital Crystal does not slow down. It builds faster — because every lost cell manufactures a new place to build."
weight = 7
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Material Loss", "Turnover", "Reoccupation", "Experiments"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with a mechanism and a constraint.

Experience could write a persistent local change into the material of the crystal, and that change could bias what got built nearby — but only while it remained inside the moving causal aperture. Growth advanced outward, the aperture advanced with it, and material left behind stayed perfectly preserved and perfectly irrelevant. Every attempt to fix that was an attempt to keep the trace near the surface.

None of those attempts questioned why the surface only ever moves one way.

Since the Digital Crystal was first defined, one transition has existed:

```text
EMPTY → OCCUPIED
```

and its reverse has not. Cells appear and never leave. The frontier advances and never retreats. Material accumulates behind it and nothing ever exposes it again. That assumption is so basic that it has never appeared in an evidence ledger, and it has silently shaped every result in this book since the crystal was built.

So this chapter adds exactly one rule:

```text
OCCUPIED → EMPTY
```

with some small probability, applied uniformly.

Nothing else. No repair mechanism. No maintenance controller. No damage detector. No energy, no resources, no metabolism, no target morphology. The growth rule is untouched. The crystal gains no new state and no new ability to notice anything.

Just loss.

Then we find out what ordinary Digital Crystal dynamics do in a world where material is no longer guaranteed to stay.

---

## Surely Loss Eventually Wins

The obvious prediction is almost embarrassingly clean, which is exactly why it deserves to be written down before running anything.

Suppose the crystal has an effective radius $r$. New construction happens around its boundary, so construction opportunity should scale like the perimeter:

$$
\text{construction} \sim r
$$

Loss, by contrast, applies to every occupied cell, so expected loss should scale like the occupied area:

$$
\text{loss} \sim r^2
$$

One term grows linearly, the other quadratically. Whatever the constants, the quadratic term wins eventually.

```text
small crystal    →  construction > loss
larger crystal   →  loss catches up
some scale       →  balance
```

Which predicts something genuinely interesting: a **finite sustainable size**. Not a size we imposed, not a boundary condition, but a scale at which two independent processes happen to cancel. That would be the first quantity in this book that the substrate chose for itself.

Because the argument is so plausible, we fixed the conditions for believing it in advance. A finite dynamic regime had to satisfy all of the following:

```text
late population slope approximately zero
population substantially above extinction
world far from simulation capacity
population meaningfully smaller than the no-loss baseline
```

A plateau caused by the crystal dying does not count. A plateau caused by the crystal hitting the edge of the world does not count. We wanted an actual balance between construction and loss, not a ceiling.

The baseline behaved as expected. With loss switched off, the late normalized population slope was about 0.037 per update, late net growth was around 154 cells per update, and the crystal was nowhere near capacity. A clean, expanding reference.

Then we turned loss on, and swept it:

```text
δ = 0.00, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16
```

---

## It Doesn't

The late normalized slopes across the entire sweep stayed at roughly:

```text
0.036 – 0.038
```

That is the no-loss slope. At the highest tested loss rate, where sixteen percent of all occupied material was being removed on every update, the crystal was still expanding at essentially the same normalized rate as a crystal losing nothing at all.

Loss did have an effect on scale: at `δ = 0.16` the late mean population was about a third smaller than the baseline. But smaller is not stationary. Nothing flattened. No tested non-zero loss rate came close to satisfying the predeclared finite-regime condition.

```text
FAILED
```

The perimeter-versus-area argument did not survive contact with the substrate. Which is more interesting than being right would have been, because the argument is not obviously wrong. Something in it is false, and finding out which part is the actual experiment.

---

## The Crystal Builds Faster When We Take Material Away

The scaling argument has two terms. We had checked the loss term carefully and assumed the construction term was fixed at roughly 150 cells per update, so that adding loss would simply subtract from it:

```text
+150 construction
 -80 loss
 = +70 net
```

So we looked at the gross rates, expecting to see the subtraction. The late averages looked like this:

| δ | attachments | losses | net |
|---|---|---|---|
| 0.00 | 152 | 0 | +152 |
| 0.02 | 227 | 81 | +146 |
| 0.04 | 299 | 158 | +141 |
| 0.06 | 358 | 227 | +131 |
| 0.08 | 430 | 303 | +127 |
| 0.12 | 530 | 420 | +110 |
| 0.16 | 632 | 531 | +101 |

Read the first column again. The construction rate is not holding at 152 while losses eat into it. It has more than quadrupled.

At `δ = 0.16` the crystal is losing over five hundred cells per update and attaching over six hundred. We removed material from the process, and the process responded by building four times as fast.

It is worth being clear about how odd that sentence is. We did not give the crystal a response. Nothing in the growth rule changed between the first row of that table and the last. Nothing in the crystal noticed that anything had been removed, because nothing in it can notice anything. The word *responded* is doing no work at all — and yet the construction rate rose monotonically with the destruction rate across every step of the sweep.

Meanwhile the net column, which is the only column a population graph would ever have shown us, declines gently and unremarkably from +152 to +101. Had we plotted population and moved on, the entire phenomenon would have been invisible, and the finite-regime hypothesis would simply have looked like a hypothesis that failed for no reason.

---

## Loss Manufactures Frontier

The mechanism, once you look for it, is almost too simple.

The scaling argument imagined a solid interior with an outer perimeter, and asked how each term scaled with radius. That geometry is only correct in a world where material never disappears.

Remove an occupied cell from the middle of existing material and you do not get a smaller crystal. You get an empty site surrounded by occupied neighbours — which is precisely the configuration the growth rule was written to act on. The vacancy is not damage. It is an attachment opportunity, indistinguishable from any other.

```text
MATERIAL LOST
↓
EMPTY LOCATION
↓
NEW LOCAL INTERFACE
↓
NEW ATTACHMENT OPPORTUNITY
```

> **Loss does not merely remove material. It changes where the process can act.**

The boundary measurements show this directly. Late mean boundary counts across the sweep:

```text
δ = 0.00      372
δ = 0.04     1167
δ = 0.08     1695
δ = 0.16     2068
```

The crystal at high loss has more than five times as much active interface as the crystal at zero loss — not because it is larger (it is smaller) but because it is riddled with vacancies, each one carrying its own local frontier.

So the failed premise was never the loss term. It was this:

```text
construction opportunity  ~  outer perimeter
```

Once material can disappear, construction opportunity is not a perimeter at all. Vacancies are generated wherever occupied material exists, which is to say throughout the area — so the quantity of places available for construction now scales with the same thing the loss rate scales with. Both terms of the original argument sit on the same footing, and the prediction that one must eventually overtake the other simply dissolves. There is no crossing point because the curves were never diverging.

That also explains why the slope was so insensitive to the loss rate. Raising δ removes more material *and* manufactures proportionally more places to rebuild it, and the two effects largely track each other. What changes is the amount of traffic; what stays roughly fixed is the rate at which the crystal advances into new territory.

---

## The Interface Was Never the Outer Edge

This is worth stopping on, because it changes a concept the previous chapter depended on.

Chapter 6 treated the causal aperture as the outer surface of a growing object: a window that moves outward and leaves everything behind it inert. That description was accurate for the world it described, and it was accurate for the wrong reason. The aperture was on the outside because the outside was the only place a state transition could occur.

The better definition is not geometric at all:

> **The active interface is the dynamically generated set of locations where the process currently has an opportunity to change state.**

Under irreversible growth those two definitions coincide, which is why the distinction never mattered. Once material can vanish, they come apart completely. The interface can now appear in the middle of solid material, split, multiply, and close again. It is a property of available transitions, not of shape.

That has a striking implication for the previous chapter. Buried material became causally inert because construction moved past it and nothing could ever bring it back into contact with a decision. In a world with loss, that is no longer permanent. A vacancy opening near old material puts old material back on an active interface.

Be careful with what that does and does not mean. It does not mean we have recovered history readout — nothing in Chapter 6 failed because access was theoretically impossible, and re-exposing a region does not make its arrangement legible to anything. What it means is narrower and still important:

> **The active interface is dynamically re-creatable.**

Burial is a consequence of irreversibility, not a law of the substrate.

---

## Where the Material Disappears

If vacancies are what matter, then it should matter where they appear.

So hold the number of removed cells exactly equal on every update and change only their placement: one branch removes cells preferentially from the surface, the other preferentially from the interior. Same loss budget, different geometry.

The result was strong. Late population under interior-biased loss ran about 11.1% higher than under surface-biased loss, clearing the predeclared 10% threshold. And the visible structure differed enormously:

```text
surface loss     ~2.7 late holes
interior loss   ~29.8 late holes
```

Equal loss, unequal consequences. The interpretation offered itself immediately: a vacancy in the interior is surrounded on all sides by occupied material, a vacancy at the surface is not, and the growth rule cares about exactly that. Interior loss should therefore produce vacancies that are unusually easy to fill — which would explain both the higher population and, indirectly, the higher hole count.

That is a plausible story about a mechanism nobody had yet measured. Note what it is really claiming: that a large fraction of the population difference comes from vacancies being *refilled*, an event that the population curve cannot distinguish from ordinary growth and that our instruments, at this point in the chapter, could not see at all.

To measure it we needed to be able to see something the crystal itself cannot.

---

## An Attachment Is No Longer What It Was

Before this chapter, one word covered every event of interest. A cell was empty, then it was occupied, and that was an attachment. There was no other kind.

Now a location can follow a longer path:

```text
occupied → lost → empty → occupied again
```

Which means the word has quietly split in two:

```text
FIRST OCCUPATION
a location becomes occupied for the first time ever

REOCCUPATION
a location was occupied, became empty, and is occupied again
```

So we added an **observer-only occupancy ledger**: a record, kept outside the simulation, of whether each lattice position has ever been occupied before. It changes nothing about the crystal's behaviour, adds no state the growth rule can read, and exists solely so that we can classify events the crystal cannot distinguish.

That distinction immediately reframes the earlier numbers. `632 attachments per update` does not mean 632 new places added to the crystal. It means first occupations plus reoccupations, in an unknown ratio — and the population curve cannot tell us which.

Before trusting the ledger we checked its null. With loss switched off, reoccupation is structurally impossible, since nothing ever becomes empty. Across 96 no-loss runs the reoccupation count was zero, exactly. Every attachment was a first occupation. The instrument reads zero when the phenomenon cannot occur.

---

## Almost Everything Came Back

Now return to the matched surface-versus-interior design, with loss counts synchronized on every update — a mean cumulative loss of roughly 890 cells in each branch — and ask the question the ledger was built for.

What fraction of lost sites are subsequently occupied again?

```text
surface   ≈ 93.6% of unique lost sites reoccupied
interior  ≈ 95.7% of unique lost sites reoccupied
```

And how long do they stay empty?

```text
surface   ≈ 1.56 updates
interior  ≈ 1.09 updates
```

Over ninety-three percent of everything the crystal lost came back, typically after being empty for one or two steps.

This is the point in the experiment where a word arrives uninvited and starts trying to explain everything. The crystal is damaged. The damage is repaired. Almost completely, almost immediately.

---

## Do Not Call It Repair

There is no damage detector. There is no target morphology. There is no repair pathway, no maintenance objective, no preference for previously occupied locations, and no representation anywhere in the substrate of the fact that something was lost.

A lost site becomes empty. The ordinary growth rule encounters an empty site with occupied neighbours and does what it has always done with empty sites that have occupied neighbours. The identical rule runs whether the location is new territory at the outer edge or a hole punched through the middle of existing material. The crystal cannot tell the two apart, because nothing in it stores the distinction.

The observer knows a site is being reoccupied. The crystal does not.

```text
REOCCUPATION
≠
REPAIR
```

We have been here before, at the very beginning of this book, when a hole was cut out of an early deterministic crystal and closed up again within a few generations. It looked like healing, and we declined to call it healing on the grounds that the same rule fills interiors and exteriors alike. That was an argument from the source code. This is the same conclusion reached from measurement, in a much harder setting — with stochastic growth, continuous background loss, and matched controls — and it now comes with a quantity attached rather than an assertion.

The bounded claim:

> **Material removal creates attachment opportunities that the ordinary growth rule rapidly reuses.**

That is a smaller sentence than *the crystal repairs itself*, and it has the advantage of being what happened.

---

## The Second Hypothesis Fails Too

The reoccupation experiment had not predicted merely that reoccupation would occur. It predicted that interior loss would produce a scientifically large reoccupation advantage over surface loss — the mechanism the 11.1% population difference had suggested.

The predeclared minimum meaningful difference was 0.15 additional reoccupations per loss. The observed difference was:

```text
0.0198
```

Statistically clear, with a narrow interval and a tiny directional p-value, and roughly an order of magnitude below the effect size we had committed to in advance. The same shape as the failures in the last chapter, and the same verdict:

```text
FAILED
```

Two primary hypotheses, two failures, in one chapter. Neither was foolish. Both were the obvious inference from the geometry, and the substrate simply answered a different question than the one we asked.

Because the reason this one failed is that the shared effect had almost nowhere left to go. Interior vacancies were not special; they were marginally faster in a process where nearly every vacancy was already being refilled. The frontier-creation measurement makes the point exactly:

```text
surface loss    ≈ 0.995 new frontier sites per lost cell
interior loss   ≈ 1.000 new frontier sites per lost cell
```

Essentially one-for-one, in both conditions. The general mechanism is not *interior loss creates special opportunity*. It is:

```text
LOCAL MATERIAL LOSS → NEW ATTACHMENT OPPORTUNITY
```

everywhere, almost without exception. The specific hypothesis failed because the shared phenomenon was already close to saturation — which is a much larger result than the one we were testing for.

---

## Population Was Hiding the Process

The most consequential thing in this chapter is not about loss at all. It is about measurement.

For six chapters, population has been our summary statistic: occupied cells at time $t$, plotted against time. That number is a **stock**. Once material can both appear and disappear, a stock is compatible with wildly different underlying traffic.

Consider two systems finishing an update at the same net figure:

```text
System A     +100 first occupations,     0 losses     →  +100
System B     +600 attachments,        -500 losses     →  +100
```

A population curve draws the same line through both. Dynamically they are not remotely the same system. System A is building. System B is churning, and would empty and refill most of itself given enough time.

Our crystal at high loss is System B, more extremely than the illustration:

```text
+632 attachments
-531 losses
----------------
+101 net
```

The population graph records a change of 101. The process executed 1,163 material events to produce it. More than ninety percent of the crystal's activity is invisible in the quantity we had been using to describe it.

```text
NET POPULATION CHANGE
≠
GROSS MATERIAL TURNOVER
```

The distinction between a stock and a flow is ancient outside this book — national accounts, hydrology, and physiology all learned to separate the level in the reservoir from the volume passing through it, and every one of them learned it the hard way. What matters here is that the Digital Crystal has just crossed the line where the distinction becomes mandatory. Before this chapter, population and activity were the same measurement. After it, they never are again.

The old chapter gave this a name — the **Flux Principle** — and it is worth keeping as a working label for a phenomenon we will meet repeatedly:

> **Static population or morphology can conceal large ongoing construction, loss and reoccupation flows.**

With the reminder that this is currently an observation about one substrate under tested conditions, not a law about digital systems in general.

---

## The Hole Paradox

One result looked contradictory at first, and its resolution is the same lesson from another direction.

Interior-biased loss produced far more visible holes — roughly 37.6 against 3.2 for surface loss in the exact-count runs — while its individual lost sites were reoccupied slightly more often and considerably faster.

How can a process that refills faster be full of more holes?

Because a snapshot counts how many vacancies exist right now. It says nothing about how long any one of them lasts.

```text
lose A
lose B
refill A
lose C
refill B
lose D
refill C
...
```

A process generating vacancies faster than it closes them will display many vacancies at every instant while every individual vacancy is short-lived. The hole count is a stock. The reoccupation delay is a flow. They can move in opposite directions without any contradiction at all.

> **State is not dynamics.**

The book keeps rediscovering that sentence. This is the first time it has been forced on us by a measurement that looks like a paradox until you check which kind of quantity you are holding.

---

## Loss and Construction Are Coupled

We can now say precisely what was wrong with the opening argument.

It was not the arithmetic. It was the assumption of independence. Writing:

```text
growth ~ r
loss ~ r²
```

treats construction and loss as two separate processes competing over a fixed geometry, so that increasing one leaves the other untouched. But loss does not act on the geometry from outside. It *is* a change to the geometry, and the geometry is what determines where construction can occur.

```text
loss
↓
changes local state
↓
creates new transition opportunities
↓
ordinary construction acts on them
↓
some loss is reversed
```

That loop is genuine feedback in the strict mechanistic sense: an output of the system alters the conditions that generate its own inputs. It requires no sensing, no goal, and no representation of the loss it counteracts. Call it **structural compensation** — with emphasis on *structural*, because the compensation is done by geometry rather than by anything resembling intent.

The crystal does not want to stay intact. Nothing in it prefers occupation to vacancy. The rule that fills a hole is the same rule that would have expanded outward, spending its attention on the nearest available opportunity — and loss keeps producing nearby opportunities.

---

## Turnover Without Repair

Both primary hypotheses in this chapter failed, and the chapter is one of the most productive in the book.

What survived:

```text
material loss creates new local construction interfaces        ≈ 1 per lost cell
ordinary growth reuses them rapidly                            >93% reoccupied
reoccupation typically occurs within one or two updates
gross construction rises steeply with loss rate
loss and construction are dynamically coupled
large material turnover hides beneath modest net population change
```

What did not:

```text
a finite sustainable size under background loss
a scientifically large interior-over-surface reoccupation advantage
repair, healing, maintenance, homeostasis, metabolism, death
```

And the distinctions this chapter forced into existence, none of which could even be stated in a world of permanent material:

```text
MATERIAL LOSS      ≠  PERMANENT LOSS
ATTACHMENT         ≠  FIRST OCCUPATION
REOCCUPATION       ≠  REPAIR
NET POPULATION     ≠  GROSS TURNOVER
STATE              ≠  DYNAMICS
```

There is something worth noticing about the direction of that list. The crystal did not become more capable in this chapter; the growth rule is exactly what it was six chapters ago. What changed is that a single removed guarantee exposed how much of our description had been resting on it. Our summary statistic stopped summarizing. Our word for a construction event stopped naming one thing. Our concept of an interface stopped being geometric.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Background loss produces a finite near-stationary regime | **FAILED** | late slopes `0.036–0.038` across the full sweep |
| Loss reduces crystal scale | **SUPPORTED** | late population ~⅓ smaller at `δ = 0.16` |
| Gross construction increases with loss rate | **SUPPORTED** | 152 → 632 attachments per update across the sweep |
| Loss creates new local frontier | **SUPPORTED** | ≈ `0.995` / `1.000` new frontier sites per lost cell |
| Active interface increases with loss | **SUPPORTED** | boundary count 372 → 2068 across the sweep |
| Loss placement affects late population | **SUPPORTED** | interior-biased ≈ 11.1% higher at matched loss count |
| Reoccupation occurs without loss | **FAILED** (null verified) | 0 reoccupations across 96 no-loss runs |
| Most lost sites are reoccupied | **SUPPORTED** | `93.6%` surface, `95.7%` interior at matched loss counts |
| Reoccupation is rapid | **SUPPORTED** | mean delay `1.56` / `1.09` updates |
| Interior loss gives a large reoccupation advantage | **FAILED** | observed `0.0198` against declared `0.15` |
| Gross turnover exceeds net population change | **SUPPORTED** | 1,163 material events for +101 net |
| Reoccupation constitutes repair or maintenance | **NOT CLAIMED** | no damage detector, target state, or special pathway |
| The crystal has a sustainable size, ages, or dies | **NOT CLAIMED** | no such quantity was demonstrated |

---

## Rebuilding Has Been Free

There is one more thing wrong with the world we just built, and it has been sitting quietly under every result in this chapter.

Every update, the crystal evaluates every eligible frontier site. All of them. When loss carved two thousand vacancies into its interior, it did not have to decide which of them were worth attending to. It attempted all of them, and also continued expanding outward, at no cost.

So the crystal has never once faced this choice:

```text
EXPAND OUTWARD
        or
REOCCUPY WHAT WAS LOST
```

It has never had to trade one against the other, because nothing has ever limited how much construction it can consider in a single step. Under unlimited computational opportunity, rebuilding what disappeared is nearly free — and the impressive reoccupation figures in this chapter are, in part, a measurement of that freedom rather than of anything the crystal does.

That is why this chapter must not end with the word repair. It ends with an unexamined luxury.

Suppose the process can evaluate only a limited number of construction opportunities per update. Nothing else changes: same growth rule, same loss rule, no new state, no energy, no maintenance controller. Just a ceiling on how many of the available opportunities can be considered at all.

Then, for the first time, an attachment somewhere has a cost measured in an attachment somewhere else. Outward construction competes with reoccupation. The crystal cannot have both, and nothing in it knows the difference between them.

> **When computational action is limited, what gets built and what gets preserved?**
