+++
title = "10: What Survives Material Loss?"
date = "2026-08-14T14:00:00+01:00"
draft = false
description = "Remove the guarantee that occupied material stays occupied, and gross construction accelerates — because material loss creates new places where construction can occur."
weight = 10
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Material Loss", "Turnover", "Reoccupation", "Experiments"]
series = ["Digital Life From First Principles"]
+++

The last chapter ended with a mechanism and a constraint.

Experience could write a persistent local change into the material of the crystal, and that change could bias what got built nearby — but only while it remained inside the moving causal aperture.

Growth advanced outward, the aperture advanced with it, and material left behind stayed perfectly preserved and perfectly irrelevant. Every attempt to fix that was an attempt to keep the trace near the surface.

None of those attempts questioned why the surface only ever moved one way.

Since the Digital Crystal was first defined, one transition has existed:

```text
EMPTY → OCCUPIED
```

and its reverse has not.

Cells appear and never leave. The frontier advances and never retreats. Material accumulates behind it and nothing ever exposes it again.

That assumption is so basic that we barely treated it as an assumption at all.

And yet it has shaped every Crystal experiment since the substrate was introduced.

So this chapter adds exactly one rule:

```text
OCCUPIED → EMPTY
```

with some small probability.

Nothing else.

No repair mechanism.

No maintenance controller.

No damage detector.

No energy, no resources, no metabolism, no target morphology.

The growth rule is untouched.

The crystal gains no new state and no new ability to notice anything.

Just loss.

Then we find out what ordinary Digital Crystal dynamics do in a world where material is no longer guaranteed to stay.

---

## Surely Loss Eventually Wins

The obvious prediction is almost embarrassingly clean, which is exactly why it deserves to be written down before running anything.

Suppose the crystal has an effective radius \(r\).

New construction happens around its boundary, so construction opportunity should scale roughly like the perimeter:

$$
\text{construction} \sim r
$$

Loss, by contrast, applies throughout occupied material, so expected loss should scale roughly like occupied area:

$$
\text{loss} \sim r^2
$$

If those scaling assumptions remain valid as the crystal grows, the conclusion follows.

The quadratic loss term eventually dominates the linear construction term.

```text
small crystal    → construction > loss
larger crystal   → loss catches up
some scale       → balance
```

Which predicts something genuinely interesting: a finite sustainable size.

Not a size imposed by the simulation boundary, but a scale emerging from the interaction between construction and loss.

If it existed, it would be one of the first characteristic scales in the Crystal produced by the dynamics rather than specified directly by us.

But notice what the argument assumes.

It is not only that loss scales with occupied material.

It assumes that construction opportunity continues to scale mainly with the **outer perimeter**, even after loss begins changing the geometry.

Because the prediction is so plausible, we fixed the conditions for believing it in advance.

A finite dynamic regime had to satisfy all four gates:

```text
|late normalized slope| ≤ 0.0025

late mean population ≥ 100 cells

maximum occupied capacity fraction < 0.75

late mean population at least 25% below
the no-loss condition
```

The no-loss baseline also had to be demonstrably expanding:

```text
normalized slope ≥ 0.004
```

A plateau caused by the crystal dying does not count.

A plateau caused by the crystal hitting the edge of the world does not count.

We wanted an actual balance between construction and loss, not a ceiling.

The baseline behaved as expected.

With loss switched off, the late normalized population slope was about `0.037` per update, late net growth was around `154` cells per update, and the crystal was nowhere near capacity.

Here `normalized slope` has a specific definition.

We fit a straight line to population over the final twelve updates and divide that fitted slope, in cells per update, by mean population over the same window.

A clean, expanding reference.

Then we turned loss on and swept:

```text
δ = 0.00, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16
```

---

## It Doesn't

The late normalized slopes across the entire sweep stayed at roughly:

```text
0.036 – 0.038
```

At the highest tested loss rate, `δ = 0.16`, every occupied cell faced a 16% loss probability on each update, yet the crystal retained essentially the same **normalized population slope** as the no-loss condition.

Absolute net growth did fall.

What exploded was gross construction.

Loss also reduced scale: late population fell as loss increased.

But smaller is not stationary.

Nothing flattened.

No tested non-zero loss rate satisfied the predeclared finite-regime criteria.

```text
FAILED
```

The perimeter-versus-area prediction failed.

But the reasoning was not absurd.

One of its assumptions about how construction opportunity scales had become wrong once loss was introduced.

Finding that assumption is now the experiment.

---

## Gross Construction Rises When We Take Material Away

The scaling argument has two terms.

We had checked the loss term carefully and assumed gross construction would remain around 150 cells per update, so that adding loss would simply subtract from it:

```text
+150 construction
 -80 loss
 = +70 net
```

So we looked at the gross rates, expecting to see the subtraction.

The late averages looked like this:

| δ | attachments | losses | net |
|---|---:|---:|---:|
| 0.00 | 152 | 0 | +152 |
| 0.02 | 227 | 81 | +146 |
| 0.04 | 299 | 158 | +141 |
| 0.06 | 358 | 227 | +131 |
| 0.08 | 430 | 303 | +127 |
| 0.12 | 530 | 420 | +110 |
| 0.16 | 632 | 531 | +101 |

Read the attachments column again.

Construction is not holding at `152` while losses eat into it.

It has more than quadrupled.

At `δ = 0.16` the crystal is losing more than five hundred cells per update and attaching more than six hundred.

We increased material loss, and gross construction rose by more than fourfold.

Nothing in the growth rule changed across that sweep.

There is no damage response and no mechanism that detects loss.

Yet increasing loss systematically changed the geometry on which the unchanged growth rule operated, and gross construction rose with it.

So the explanation cannot be a new behaviour added to the Crystal.

It has to be a consequence of the state transitions already present.

Meanwhile the net column — the only column a population graph would have shown us — declines gently from `+152` to `+101`.

Had we plotted population and moved on, the entire phenomenon would have been invisible.

The finite-regime hypothesis would simply have looked like a hypothesis that failed for no reason.

---

## Loss Manufactures Frontier

The mechanism, once you look for it, is almost too simple.

The scaling argument imagined a largely solid interior with an outer perimeter, then asked how construction and loss scaled with radius.

That picture is only useful while material never disappears.

Remove an occupied cell and two things happen at once:

```text
occupied material decreases
+
an empty site with occupied neighbours appears
```

The vacancy is not represented as damage.

To the growth rule it is simply an empty site with occupied neighbours — the same kind of candidate used everywhere else.

Its local geometry may differ from another candidate's.

Its history does not exist as a separate category.

```text
MATERIAL LOST
↓
EMPTY LOCATION
↓
NEW LOCAL INTERFACE
↓
NEW ATTACHMENT OPPORTUNITY
```

> **Loss removes material and creates new places where construction can occur.**

A first geometric measurement points in the same direction.

The V1 sweep counted occupied cells with fewer than all six neighbours occupied:

```text
δ = 0.00       372
δ = 0.04      1167
δ = 0.08      1695
δ = 0.16      2068
```

So the high-loss crystal contains more than five times as much occupied material exposed to empty neighbouring space despite being smaller overall.

That is not yet the same quantity as the number of eligible empty attachment sites.

The later exact-count experiment measures newly created attachment candidates directly.

But already the geometry is clear.

Loss creates internal empty space in material that would otherwise have remained occupied.

The failed premise was never the loss term.

It was this:

```text
construction opportunity
~
outer perimeter only
```

Once material can disappear, construction opportunity is no longer determined only by the visible outer perimeter.

Loss generates additional attachment opportunities inside the occupied structure.

Increasing `δ` therefore does two things at once:

```text
removes material
+
creates new places where the unchanged growth rule can act
```

The gross traffic changes dramatically even though normalized population expansion changes much less.

---

## The Interface Was Never the Outer Edge

This is worth stopping on because it changes a concept the previous chapter depended on.

Under irreversible growth, the places where construction could occur sat almost entirely near the outer surface.

That made a geometric frontier look more fundamental than it really was.

Material loss exposes the more general object.

> **The construction interface is the dynamically generated set of empty locations currently eligible for attachment.**

This is the set earlier experiments and the implementation called **frontier candidates**.

The new name matters here because, once loss exists, those candidates no longer belong only to an outward-moving geometric frontier.

The distinction from the previous chapter now becomes useful:

```text
CONSTRUCTION INTERFACE
→ empty locations at which occupation can occur

CAUSAL APERTURE
→ existing material whose state can influence
  decisions at those locations
```

Under irreversible outward growth, both computational objects sit beside the visible outer surface.

They are easy to confuse with the outline itself.

Loss pulls both away from that visible outline.

A vacancy can create construction interface deep inside the crystal, with surrounding occupied material becoming causally relevant to that interface.

The interface can appear internally, split into disconnected regions, and disappear again when vacancies are filled.

The relevant boundary is therefore generated by available **construction transitions**, not by the visible outline of the Crystal.

That has a striking implication for the previous chapter.

Buried material became causally inert because construction moved past it and nothing could bring it back into contact with a decision.

In a world with loss, that need not be permanent.

A vacancy opening beside old material can make that material locally relevant again.

Be precise about what this does and does not mean.

It does not recover history readout.

Re-exposing retained material does not make its arrangement legible to anything.

The narrower result is:

> **The causal aperture can be re-created around material that had previously fallen outside it.**

Permanent burial was a consequence of irreversible growth.

It was not a necessary property of the substrate.

---

## Where the Material Disappears

If vacancies matter, then perhaps it matters where they appear.

So hold the number of removed cells equal on every update and change only their placement.

One branch removes cells preferentially near the surface.

The other removes cells preferentially from the interior.

Same loss budget.

Different geometry.

The first result looked strong.

Across `32` paired V1 placement runs, late population under interior-biased loss was about `11.1%` higher than under surface-biased loss.

The predeclared meaningful population advantage was `10%`.

So the placement effect cleared its frozen gate.

Its mechanism had not.

That distinction matters.

The population difference is real under this protocol.

We do not yet know why it occurs.

Visible structure also differed strongly:

```text
surface loss      ~2.7 late holes
interior loss    ~29.8 late holes
```

Equal loss produced unequal population outcomes.

The obvious candidate explanation was reoccupation.

Interior vacancies generally have more occupied neighbours and therefore might be easier for the ordinary growth rule to refill.

If that explanation is doing substantial work, interior loss should produce a meaningfully larger reoccupation rate than surface loss.

Plausible.

Still unmeasured.

And it does not, by itself, explain the higher visible hole count.

Faster individual refilling and more simultaneous holes appear at first to point in opposite directions.

We will return to that apparent contradiction once we can distinguish vacancy creation from vacancy lifetime.

For now, the mechanistic hypothesis is clear:

```text
INTERIOR LOSS
↓
VACANCIES EASIER TO REOCCUPY
↓
HIGHER RETAINED POPULATION
```

But a population curve cannot tell us whether a newly occupied cell is new territory or an old site returning.

To test the hypothesis, we needed an instrument that could.

---

## An Attachment Is No Longer What It Was

Before material loss, one word covered every occupation event.

A cell was empty.

Then it was occupied.

That was an attachment.

Now a location can follow a longer path:

```text
occupied
→ lost
→ empty
→ occupied again
```

So the word quietly splits in two:

```text
FIRST OCCUPATION

a location becomes occupied
for the first time ever


REOCCUPATION

a location was occupied,
became empty,
and becomes occupied again
```

We therefore added an **observer-only occupancy ledger**.

It records whether each lattice location has previously been occupied.

It changes nothing about the crystal's behaviour.

The growth rule cannot read it.

The distinction exists only for us.

That changes the meaning of every attachment count in this chapter.

`632 attachments per update` no longer means 632 previously unused locations entered the crystal.

It means:

```text
first occupations
+
reoccupations
```

Before trusting the ledger, we checked its null.

With loss switched off, reoccupation is structurally impossible because nothing ever becomes empty.

Across `96` no-loss runs:

```text
reoccupation count = 0
```

exactly.

Every attachment was a first occupation.

The instrument reads zero when the event it was built to detect cannot occur.

---

## Almost Everything Came Back

Now return to the matched surface-versus-interior experiment.

The V2 experiment used `48` paired runs, with loss counts synchronized between the two branches.

Mean cumulative loss was roughly `890` cells per branch.

The observer ledger lets us ask two related but different questions.

First, at the **loss-episode level**:

```text
observed reoccupations / loss episodes

surface     ≈ 0.936
interior    ≈ 0.956
```

Then at the **unique-site level**:

```text
fraction of distinct lost locations
reoccupied at least once within the run

surface     ≈ 93.6%
interior    ≈ 95.7%
```

Those numbers happen to be very similar here.

They do not have the same denominator.

A single lattice position can be lost, reoccupied, lost again, and reoccupied again.

The event-level ledger keeps those episodes separate.

It also records the delay from each loss episode to its observed reoccupation:

```text
surface     ≈ 1.56 updates
interior    ≈ 1.09 updates
```

These delay means need one qualification.

They are calculated only for reoccupations that are actually observed before the finite run ends.

An episode still open at the horizon contributes a loss but no completed delay.

So `1.56` and `1.09` describe **observed return times**.

They are not uncensored estimates of the lifetime of every vacancy.

Within those bounds, the result is still striking.

Roughly `0.94–0.96` reoccupation events were observed per loss event.

More than 93% of distinct lost locations were observed to return at least once.

And among the returns we saw, the delay was usually only one or two updates.

The biological interpretation is almost irresistible:

```text
material disappears
↓
the vacancy closes
↓
repair
```

---

## Do Not Call It Repair

There is no damage detector.

There is no target morphology.

There is no repair pathway, maintenance objective, or preference for previously occupied locations.

There is no representation anywhere in the substrate of the fact that a location was occupied before.

A lost site becomes empty.

The ordinary growth rule encounters an empty site with occupied neighbours and does what it has always done with empty sites that have occupied neighbours.

The same rule acts whether the location is new territory at the outer edge or a hole inside existing material.

The observer knows that the location was occupied before.

The crystal does not.

The growth rule receives current geometry, not an occupancy-history label.

```text
REOCCUPATION
≠
REPAIR
```

We encountered an early version of this temptation when a hole cut from the prototype Crystal closed again.

Then, our reason for refusing the word *healing* was mechanistic: the same growth rule filled interior and exterior empty space.

Now the stronger experiment reaches the same boundary quantitatively.

Under stochastic material loss and matched controls, previously occupied sites are indeed reused rapidly.

What still does not appear is a special mechanism that treats them as damage.

The bounded claim is:

> **Material removal creates attachment opportunities that the ordinary growth rule rapidly reuses.**

That is a smaller sentence than *the crystal repairs itself*.

It also has the advantage of being what happened.

---

## The Second Hypothesis Fails Too

The reoccupation experiment did not merely predict that reoccupation would occur.

It predicted that interior loss would produce a **scientifically large reoccupation advantage** over surface loss — the mechanism suggested by the earlier `11.1%` population difference.

The predeclared minimum meaningful difference was:

```text
0.15 additional reoccupations per loss
```

The observed interior-minus-surface difference was:

```text
0.0198 additional reoccupations per loss
```

About `1.98` percentage points against a declared meaningful difference of `15` percentage points.

The difference was statistically detectable.

The scientific magnitude claim failed.

```text
STATISTICALLY DETECTABLE
≠
SCIENTIFICALLY LARGE ENOUGH
```

The predeclared large interior-reoccupation advantage was therefore:

```text
FAILED
```

And that matters for the earlier `11.1%` population difference.

The population effect remains.

This proposed mechanism is too small to serve as its demonstrated explanation.

Two predeclared primary hypotheses.

Two failures.

Neither was foolish.

Both were plausible consequences of the geometry.

The substrate simply answered different questions from the ones we asked.

The failure redirected attention from the small difference between the groups to the much larger phenomenon they shared.

Interior vacancies were reoccupied somewhat faster.

But both conditions were already reoccupying almost everything within the tested horizon.

The large placement-dependent population difference therefore remains mechanistically unresolved here.

What the next measurement establishes much more cleanly is the shared mechanism.

For every exact-count loss operation, compare the construction candidates immediately before loss with those immediately afterwards.

The result:

```text
surface loss     ≈ 0.995 newly created frontier candidates per loss
interior loss    ≈ 1.000 newly created frontier candidates per loss
```

Essentially one-for-one under both tested placement policies.

Here a `new frontier candidate` means an empty lattice location that was **not eligible for attachment before the loss operation but was eligible immediately afterwards**.

The instrument computes:

```text
frontier after loss
MINUS
frontier before loss
```

and divides the number of newly eligible sites by the number of removed cells.

The general mechanism supported by these experiments is therefore not:

```text
INTERIOR LOSS
→
SPECIAL OPPORTUNITY
```

but:

```text
LOCAL MATERIAL LOSS
→
NEW ATTACHMENT OPPORTUNITY
```

almost every time it was measured under these conditions.

The specific interior-advantage explanation failed.

What survived was broader:

> **Under both tested loss placements, material removal generated attachment opportunities that were reused at very high rates.**

---

## Population Was Hiding the Process

The most consequential thing in this chapter may not be about loss at all.

It is about measurement.

Population has been one of our simplest summaries:

```text
number of occupied cells at time t
```

That number is a **stock**.

Once material can both appear and disappear, a stock can hide radically different amounts of underlying traffic.

Consider two systems ending an update at the same net change:

```text
System A    +100 occupations      0 losses    → +100 net

System B    +600 occupations   -500 losses    → +100 net
```

A population curve draws the same net movement through both.

Dynamically they are not remotely the same process.

System A changes one hundred locations.

System B undergoes eleven hundred material events while producing the same net change.

Our high-loss crystal is an even clearer example:

```text
+632 attachments
-531 losses
----------------
+101 net
```

The population graph records:

```text
+101
```

and discards the rest.

```text
NET POPULATION CHANGE
≠
GROSS MATERIAL TURNOVER
```

The distinction between stocks and flows is ancient outside this book.

National accounts, hydrology, physiology and countless other fields already know that the level in a reservoir is not the same quantity as the volume moving through it.

There is no reason to pretend we discovered that distinction here.

What changed is the substrate.

Before material loss, population change tracked construction much more directly.

After turnover appears, it no longer does.

The experimentally important statement is simply:

> **Static population or morphology can conceal large ongoing construction, loss and reoccupation flows.**

No new Principle required.

The old measurement has reached the point where it is no longer sufficient on its own.

---

## The Hole Paradox

One result looked contradictory at first.

Its resolution is the same measurement lesson from another direction.

In the later V2 reoccupation experiment, interior-biased loss produced far more fully enclosed single-cell vacancies:

```text
surface     ≈ 3.2
interior   ≈ 37.6
```

while observed interior reoccupations occurred somewhat more often and more quickly.

These are not the earlier:

```text
surface     ≈ 2.7
interior   ≈ 29.8
```

values from the first placement experiment.

The earlier values came from the separate `32`-pair, `32`-update V1 placement experiment.

The later values came from the `48`-pair, `40`-update V2 reoccupation experiment.

In both experiments, a `hole` is defined narrowly:

> an empty lattice cell whose six immediate neighbours are occupied.

How can a condition that refills individual vacancies faster also contain more holes?

Because those measurements ask different questions.

A snapshot hole count measures vacancy **prevalence**:

```text
how many vacancies exist now?
```

Reoccupation delay measures vacancy **duration**:

```text
how long does this vacancy remain open?
```

A process can create vacancies rapidly enough to maintain many holes at a snapshot even when individual vacancies are short-lived.

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

Many vacancies pass through the system.

Few need to persist for long.

There is no contradiction.

> **State is not dynamics.**

Here the apparent paradox disappears as soon as we separate a snapshot quantity from an event-duration quantity.

---

## Loss and Construction Are Coupled

We can now say precisely what was wrong with the opening argument.

It was not the arithmetic.

It was the assumption of independence.

Writing:

```text
growth ~ r
loss ~ r²
```

treated construction and loss as two separate processes competing over a fixed geometry.

Increasing one was assumed to leave the opportunities available to the other unchanged.

But loss does not act on geometry from outside.

It **is** a change to geometry.

And geometry determines where construction can occur.

```text
loss
↓
changes local state
↓
creates new transition opportunities
↓
ordinary construction acts on them
↓
some lost occupation is replaced
```

That gives a local dynamical feedback:

```text
loss
→
new attachment opportunity
→
construction
```

No sensing is required.

No goal is required.

No representation of damage is required.

A useful descriptive phrase is **structural compensation**.

In the exact-count experiment, roughly `0.94–0.96` reoccupation events were observed per loss event.

Some of the material removed by loss is replaced because loss itself changes the geometry on which the unchanged construction rule operates.

The word *compensation* describes that dynamical counter-effect.

It does not imply sensing, intention, homeostasis or repair.

The crystal does not want to stay intact.

Nothing in it knows what was removed.

Loss changes the set of opportunities available to the rule.

The rule acts.

---

## Turnover Without Repair

Both primary hypotheses failed.

But underneath them a cleaner process became visible:

```text
material loss
↓
new transition opportunity
↓
ordinary construction
↓
rapid reoccupation
↓
continued turnover
```

The growth rule did not become more sophisticated.

We removed one guarantee, and the existing rule began operating on a different geometry.

That was enough to change the meaning of several quantities we had treated as straightforward:

```text
attachment
population
interface
persistence
```

---

## Experimental Note

This chapter uses two related material-loss experiments.

### V1 — Background Loss and Placement

The V1 quick profile used:

```text
24 independent runs per loss rate
96 no-loss baseline runs

radius                 72
warmup                 14 updates
continuation           48 updates
late window            final 12 updates

δ ∈ {0, .02, .04, .06, .08, .12, .16}
```

Ordinary growth occurs first on each update.

Material loss is then applied to the resulting occupied state.

`Late normalized population slope` is calculated by fitting a linear regression to population over the final twelve updates and dividing the fitted slope by mean population over that same window.

The frozen finite-regime gates were:

```text
|normalized slope|       ≤ 0.0025
late mean population     ≥ 100
maximum capacity fraction < 0.75
size reduction vs δ=0    ≥ 0.25
```

The no-loss baseline also had to satisfy:

```text
normalized slope ≥ 0.004
```

The V1 surface/interior placement experiment used:

```text
32 paired runs
32 continuation updates
```

Each pair removed exactly the same number of occupied cells on every update.

Only the placement policy differed.

Its predeclared meaningful late-population advantage was:

```text
10%
```

The V1 `surface` measurement reported in the loss sweep is the number of occupied cells with fewer than six occupied neighbours.

It should not be confused with the number of empty construction-interface candidates.

### V2 — Reoccupation Mechanism

The V2 exact-count experiment used:

```text
48 paired surface/interior runs
40 continuation updates

96 no-loss runs
for the observer-ledger null
```

Growth occurs before loss on each update.

A location removed during one update therefore cannot be reoccupied until a later growth update.

The observer-only ledger records both:

```text
loss episodes
reoccupation episodes
```

and:

```text
distinct locations ever lost
distinct lost locations ever reoccupied
```

so these are separate measurements:

```text
reoccupation events / loss events
```

and:

```text
fraction of unique lost sites
ever reoccupied within the run
```

A location can contribute multiple loss/reoccupation episodes.

Reoccupation delay is measured from the most recent loss episode to its observed subsequent occupation.

The reported mean delay is therefore conditional on a reoccupation being observed before the finite experimental horizon.

A `hole` is a fully enclosed one-cell vacancy:

```text
empty centre cell
+
all six immediate neighbours occupied
```

`New frontier candidates per loss` measures construction opportunities created by the loss operation itself.

For each loss step:

```text
frontier before loss
↓
apply matched loss
↓
frontier after loss
```

A candidate contributes to the numerator only if it was not eligible before loss and became eligible immediately afterwards.

The count is then divided by the number of removed cells.

The frozen V2 meaningful-effect threshold for the interior-minus-surface reoccupation comparison was:

```text
0.15 additional reoccupations per loss
```

The observed difference was:

```text
0.0198
```

Full per-run distributions, bootstrap intervals, randomization tests and raw occupancy-ledger records remain in the accompanying experimental record.

---

## Evidence Ledger

| Claim | Status | Evidence |
|---|---|---|
| Background loss produces a finite near-stationary regime in the tested sweep | **FAILED** | no non-zero `δ` satisfied the frozen four-gate regime definition |
| Loss reduces crystal scale across the tested sweep | **SUPPORTED** | late mean population declines as `δ` increases |
| Gross construction increases with loss rate | **SUPPORTED** | 152 → 632 attachments per update across the sweep |
| Occupied material becomes increasingly exposed to empty neighbourhood space as loss rises | **SUPPORTED** | V1 occupied-surface count 372 → 2068 |
| Individual loss events create new construction opportunities | **SUPPORTED** | V2 ≈ `0.995` / `1.000` newly created frontier candidates per loss |
| Loss placement affects late population under matched loss count | **SUPPORTED** | interior-biased ≈ `11.1%` higher against a `10%` frozen gate |
| No-loss control produces zero reoccupation events | **SUPPORTED** | structurally required; 0 observed across 96 runs |
| Most loss episodes are followed by observed reoccupation within the finite run | **SUPPORTED** | reoccupations/loss ≈ `0.936` surface, `0.956` interior |
| Most distinct lost locations return at least once within the run | **SUPPORTED** | unique-site fraction ≈ `93.6%` / `95.7%` |
| Observed reoccupations occur rapidly | **SUPPORTED** | conditional mean delay ≈ `1.56` / `1.09` updates |
| Interior loss produces the predeclared large reoccupation advantage | **FAILED** | observed `0.0198` reoccupations/loss against declared `0.15` |
| The 11.1% placement-dependent population advantage is explained by that reoccupation advantage | **NOT SUPPORTED** | measured reoccupation-rate difference is far below the declared meaningful scale |
| Mechanism of the remaining placement-dependent population difference | **NOT RESOLVED** | no alternative mechanism was isolated as a primary claim here |
| Gross material traffic can greatly exceed net population change | **SUPPORTED** | 632 attachments + 531 losses = 1,163 material events for +101 net |
| Reoccupation constitutes repair or maintenance | **NOT CLAIMED** | no damage detector, target state, history label or special pathway |
| The crystal has a sustainable size, ages, or dies | **NOT CLAIMED** | no such property was established |

---

## Rebuilding Has Been Free

There is one more assumption underneath every result in this chapter.

Every update, the crystal evaluates every eligible construction opportunity.

All of them.

When loss created thousands of eligible sites, the process never had to choose which ones to consider.

It could evaluate reoccupation opportunities and outward-growth opportunities in the same update.

So the crystal has never faced this choice:

```text
EXPAND OUTWARD
        or
REOCCUPY WHAT WAS LOST
```

It has never had to trade one against the other.

Nothing has limited how many available construction opportunities can be evaluated in a single step.

Under unlimited evaluation, reoccupation does not have to compete with outward construction for computational opportunity.

That means the extraordinarily high reoccupation rates in this chapter were measured under a computational regime in which every eligible candidate could be considered.

How much of the result survives once those opportunities must compete is unknown.

That is why this chapter must not end with the word *repair*.

It ends with an unexamined luxury.

Suppose the process can evaluate only a limited number of construction opportunities per update.

Nothing else changes.

Same growth rule.

Same loss rule.

No new internal state.

No energy.

No maintenance controller.

Just a ceiling on how many available transitions can be considered.

Then, for the first time, evaluating one construction opportunity can mean not evaluating another.

```text
OUTWARD CONSTRUCTION
        competes with
REOCCUPATION
```

> **When computation becomes scarce, what gets built — and what gets left undone?**
