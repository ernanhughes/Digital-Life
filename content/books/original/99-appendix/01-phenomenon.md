+++
title = "Appendix: Phenomenon Ledger"
date = "2026-08-12T22:01:00+01:00"
draft = false
description = "A cross-chapter ledger of recurring phenomena discovered during the Digital Life experiments, including what survived failed hypotheses, where each phenomenon recurred, what mechanisms may explain it, and what remains unearned."
weight = 99
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Phenomena", "Evidence", "Experimental Method"]
series = ["Digital Life From First Principles"]
+++

## Appendix 01: Phenomenon Ledger

This appendix records something different from the chapter-by-chapter claim ledger.

The claim ledger asks:

```text
What did we predict?
Did the predeclared experiment pass?
What claim did the evidence earn?
```

The phenomenon ledger asks:

```text
What did the experiment reveal anyway?
Did the same pattern appear again elsewhere?
Is a substrate-level regularity beginning to emerge?
```

Those are not the same questions.

A primary hypothesis can fail while exposing a different phenomenon.

That does not rescue the failed hypothesis.

It means the experiment taught us something else.

The purpose of this appendix is to preserve those surviving observations across the entire book so that recurring mechanisms are not lost when a chapter moves on.

The standard is the same one used throughout the project:

```text
PROPERTY
↓
MECHANISM
↓
IMPLEMENTATION
↓
OBSERVATION
↓
MEASUREMENT
↓
CONTROLLED EXPERIMENT
↓
BOUNDED CLAIM
```

Nothing in this ledger becomes a biological property merely because it resembles one.

Nothing becomes a law merely because it recurs twice.

Nothing becomes evidence for life merely because it is interesting.

Each phenomenon remains bounded by the experiments that produced it.

---

# P001 — Interface Principle

**Status:** **SUPPORTED AS A RECURRING PHENOMENON**

**First clear appearance:** Chapter 18

**Strongest supporting chapters:** Chapters 18, 20 and 21

**Related chapters:** Chapter 19 and Chapter 22

---

## Short Description

> **In the Digital Crystal, causal relevance is concentrated around dynamically active construction interfaces: stored state matters while coupled to them, material loss can create them, and finite computation determines which of their opportunities are serviced.**

The important object is not simply:

```text
occupied material
```

and not simply:

```text
the outer edge of the crystal
```

It is the dynamically generated set of locations at which the current process can still change what happens next.

---

## Why This Phenomenon Was Not Obvious

The early Digital Crystal experiments treated the structure largely as accumulated material.

Once a site became occupied, it remained occupied.

Growth moved outward.

That made the visible outer boundary look like the obvious active region.

But later experiments broke that picture.

A historical state could remain physically present while becoming causally irrelevant.

Material loss could create new active boundaries inside old material.

A finite computational budget could leave some frontier opportunities unevaluated.

The experiments therefore began separating:

```text
MATERIAL EXISTS
```

from:

```text
MATERIAL CAN STILL PARTICIPATE
IN FUTURE CONSTRUCTION
```

That distinction is the foundation of the Interface Principle.

---

## Chapter 18 — Persistent State Was Not Enough

Chapter 18 introduced a local modified material state.

An experience could write the state.

The state could persist.

But when the modified cells were later buried behind new construction, removing the labels produced no detectable difference in future growth.

The state still existed.

The process could no longer reach it.

This produced the first major separation:

```text
PERSISTENCE
≠
CAUSAL ACCESSIBILITY
```

The experiment then measured the active construction region directly.

Modified material mattered when it remained adjacent to frontier sites where attachment decisions were still being made.

When it left that region, its causal effect disappeared even though the stored state remained intact.

This suggested that the active frontier was not merely geometric.

It was a **causal aperture**.

---

## Chapter 18 — Placement Changed Causal Lifetime

The stronger Chapter 18 experiment held the amount of propagated historical material constant.

Only spatial placement changed.

Three policies were compared:

```text
INTERIOR-BIASED
RANDOM
SURFACE-BIASED
```

With copy quantity controlled exactly, surface-biased placement produced substantially greater:

```text
integrated frontier access
integrated probability leverage
realized causal attachment flips
```

The important result was therefore not:

```text
more stored state
→ more effect
```

It was:

```text
same amount of state
+
different spatial placement
→
different causal lifetime
```

The strongest bounded result from that chapter was:

> A persistent local state can alter later construction while it remains causally accessible, and with state quantity held constant, spatial placement strongly changes the duration and magnitude of that causal availability.

This is the clearest experimental foundation for the Interface Principle.

---

## Chapter 20 — Loss Created New Interface

Chapter 20 removed the assumption that occupied material lasts forever.

A cell could become empty again.

The initial prediction treated construction opportunity as though it scaled mainly with the crystal's outer perimeter while loss scaled with occupied area.

That prediction failed.

The reason was geometric.

A lost occupied site often became a new local attachment opportunity.

The observed chain was:

```text
MATERIAL LOSS
↓
EMPTY SITE
↓
NEW LOCAL FRONTIER
↓
NEW ATTACHMENT OPPORTUNITY
```

Measured frontier creation was approximately:

```text
surface loss
~0.995 new frontier sites per loss

interior loss
~1.000 new frontier sites per loss
```

The interface therefore was not limited to the outside of the object.

Loss could create new active interface inside previously occupied material.

That substantially changed the interpretation of the crystal's geometry.

---

## Chapter 20 — Reoccupation Was Not Repair

More than ninety-three percent of lost sites were subsequently reoccupied under the tested exact-count conditions.

Most returned within one or two updates.

This looked superficially like repair.

But there was no:

```text
damage detector
repair objective
target morphology
special reconstruction pathway
```

The same ordinary growth rule acted on newly empty sites.

So the correct interpretation was:

```text
LOSS
→
CREATES INTERFACE

INTERFACE
→
CREATES ORDINARY CONSTRUCTION OPPORTUNITY
```

The system did not repair damage because it recognized damage.

Its geometry made loss available to the same mechanism that already fills eligible empty sites.

This is a strong substrate-level extension of the Interface Principle.

---

## Chapter 21 — Computation Selected the Interface

Chapter 21 added finite computational opportunity.

The crystal could no longer evaluate every eligible frontier site.

At most:

```text
B
```

frontier candidates could be evaluated per update.

This produced another separation.

The interface could contain many possible actions.

But only some could actually be serviced.

So:

```text
FRONTIER OPPORTUNITY
≠
EVALUATED OPPORTUNITY
```

Different local scheduling policies produced different material futures even at the same total budget.

High-support scheduling strongly favoured reoccupation.

Low-support scheduling favoured first occupation more strongly.

The crystal did not know whether a site was:

```text
old territory
```

or:

```text
new territory
```

The distinction emerged from geometry.

The result extended the Interface Principle again:

> The active interface is not merely where change is possible. Under computational scarcity, it is also where finite evaluation opportunity must be allocated.

---

## Chapter 19 — Accessibility Was Necessary but Not Sufficient

Chapter 19 provides an important limitation.

Two different historical traces remained:

```text
persistent
spatially distinguishable
causally accessible
```

and still failed to produce a scientifically meaningful difference under the common later challenge.

So:

```text
CAUSAL ACCESS
≠
FUNCTIONAL READOUT
```

This prevents the Interface Principle from becoming too strong.

Being coupled to the active interface is not enough to guarantee that a difference will matter.

It only means the current process has an opportunity to encounter it.

The later dynamics must still be sensitive to the particular degree of freedom in which the states differ.

---

## Chapter 22 — The Boundary Was Not Privileged

Chapter 22 tried to identify a privileged spatial boundary.

That failed.

The outer candidate boundary did not localize causal effects more strongly than an interior pseudo-boundary.

But local perturbations still produced stronger effects on nearby regions.

So Chapter 22 added:

```text
SPATIAL CAUSAL LOCALITY
```

without adding:

```text
PRIVILEGED OUTER BOUNDARY
```

This is consistent with the Interface Principle.

The causally active structure may be distributed across dynamically generated local interfaces rather than enclosed by one permanent boundary.

---

## Current Mechanistic Picture

The recurring mechanism can now be written as:

```text
CURRENT MATERIAL STATE
↓
DYNAMICALLY GENERATED INTERFACE
↓
LOCAL CONSTRUCTION OPPORTUNITIES
↓
FINITE EVALUATION / STOCHASTIC DECISION
↓
ATTACHMENT OR LOSS
↓
NEW MATERIAL STATE
↓
NEW INTERFACE
```

The process continually regenerates the conditions under which its next changes can occur.

The interface is therefore not a static object.

It is produced by the dynamics.

---

## Current Bounded Principle

The strongest cross-chapter statement currently justified is:

> **Across the tested Digital Crystal mechanisms, causal influence repeatedly depends on dynamically generated construction interfaces. Historical material exerts influence while coupled to active construction, loss creates new active interfaces, and finite computational opportunity determines which interface events can be evaluated.**

This is the current **Interface Principle**.

It is a recurring empirical pattern.

It is not yet a universal law of digital systems.

---

## What Would We Expect If the Principle Is Real?

If the Interface Principle continues to hold, future experiments should repeatedly find that measures based on active construction opportunity explain more causal behavior than measures based only on accumulated occupancy.

For example:

```text
ACTIVE INTERFACE STATE
```

should often be more informative about immediate future changes than:

```text
INTERIOR BULK STATE
```

after controlling for trivial geometry.

The relevant process may therefore be better represented by:

```text
where change can happen
```

than by:

```text
where material currently exists
```

This is a prediction for future work.

It has not yet been established generally.

---

## What Would Weaken or Falsify It?

The Interface Principle would weaken substantially if future experiments showed that:

```text
deep interior state
systematically controls future construction
without interface mediation
```

or that:

```text
active-interface measurements
provide no additional causal or predictive information
beyond static occupancy and geometry
```

or that:

```text
apparent interface effects disappear
under stronger matched controls
```

A stronger version would also fail if the apparent recurrence across Chapters 18–22 turned out to be an artifact of the particular frozen Digital Crystal growth rule rather than a more general computational phenomenon.

The principle should therefore be treated as specific to the tested substrate until replicated elsewhere.

---

## What This Does Not Establish

The Interface Principle does **not** establish:

```text
membrane
organism
self
individual
autonomy
homeostasis
repair
metabolism
agency
life
```

It does not establish that the Digital Crystal possesses a privileged boundary.

It does not establish that the active interface is one coherent entity.

It does not establish that the interface propagates as a wave.

It does not establish that every Digital Crystal phenomenon is controlled by the interface.

It establishes something smaller:

> **Where the Digital Crystal can currently act matters more than the mere persistence of material that can no longer participate in that action.**

---

## Relationship to Other Phenomena

The Interface Principle currently interacts with several other phenomena that will receive their own entries in this appendix.

```text
P002
LOSSY-HISTORY PRINCIPLE

history can survive in coarse form
without remaining exactly recoverable
```

```text
P003
FLUX PRINCIPLE

static material stock can conceal
large construction / loss / reoccupation traffic
```

```text
P004
SPATIAL CAUSAL LOCALITY

local interventions preferentially affect
nearby future dynamics
without establishing a privileged body boundary
```

```text
H001
PROPAGATING-FIELD HYPOTHESIS

active causal organization may move
through space-time in a measurable way
```

The relationships between these phenomena may eventually become more important than any one of them individually.

---

## Current Status

```text
PHENOMENON:
Interface Principle

STATUS:
SUPPORTED AS A RECURRING PHENOMENON

STRONGEST EVIDENCE:
Chapter 18 exact-quantity placement experiment

MECHANISTIC EXTENSIONS:
Chapter 20 loss-generated frontier
Chapter 21 finite evaluation allocation

IMPORTANT LIMIT:
Chapter 19 shows accessibility does not guarantee readout

BOUNDARY RESULT:
Chapter 22 found locality but no privileged outer boundary

GENERALITY:
UNTESTED OUTSIDE THE DIGITAL CRYSTAL SUBSTRATE
```

For now, that is where the evidence stops.
