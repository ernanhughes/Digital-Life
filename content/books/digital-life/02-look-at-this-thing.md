+++
title = "02: Look at This Thing"
date = "2026-08-14T09:30:00+01:00"
draft = false
description = "Calibrating the microscope. A continuous cellular automaton produces something that looks disturbingly like a creature. We strip it down to almost nothing, then rebuild a world in which the actors rewrite the conditions of their own future — and start deleting the parts to find out where the thing actually lives."
weight = 2
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Lenia", "Cellular Automata", "Physarum", "Agent-Based Models", "Pattern Identity", "History Dependence", "Emergence"]
+++

Don't read anything yet.

Watch this.

{{< figure
    src="/images/books/digital-life/ch01-lenia-organism.gif"
    alt="A localized continuous cellular automaton pattern evolving and moving through time."
    caption="One state of a continuous cellular automaton evolving through time."
>}}

Something is moving.

It appears to have a boundary. Different parts of it seem to behave differently: an edge that ripples, an interior that stays denser, a leading region that seems to pull the rest along. Its shape changes as it travels, and yet some larger organization survives those changes. Watch it for thirty seconds and you will start predicting what it is about to do.

If you saw this without context, biological language would arrive immediately.

A cell. A creature. An organism. Perhaps even an animal.

That reaction is useful. It is also the first thing this book has to take apart.

---

## Your Brain Has Already Invented an Object

Before knowing anything about the mechanism, most of us have already run through something like this:

```text
pattern
↓
persistent pattern
↓
moving persistent pattern
↓
thing
↓
creature
```

Notice how fast that happened, and notice how little was required to trigger it. Nothing in the simulation announced `I AM AN OBJECT`. Nothing marked where the supposed body begins or ends. Nothing certified that the pattern visible at one moment is the same individual as the pattern visible several moments later.

We supplied all of that.

So the first question of this book is not *is this alive?* That question is far too large to be useful yet. The first question is much smaller, and much more answerable:

> **Why does this look so much like a thing at all?**

---

## There Is No Creature Variable

Start with what is not in the program.

There is no object exposing `creature.move()` or `creature.keep_shape()`. There is no animation path, no skeleton, no set of joints, no controller issuing instructions like *keep the left side attached, push the front forward, restore the outline*. There is no variable called `position_of_creature`, and no field named `head` or `tail`.

Underneath the apparent creature is a field of numbers. Each location changes according to nearby values, using the same rule everywhere.

Nothing corresponding to the creature moves through that mechanism. The field simply changes, step after step.

The system is **Lenia**, a continuous cellular automaton famous partly because its localized patterns are so easy to describe biologically.[1]

We will resist that language for now.

What we have actually observed is a persistent localized pattern. That description is less exciting. It is also something we can test.

The direction of explanation here is worth pausing on, because it runs backwards compared with ordinary software. Normally a programmer defines an object and the object then produces behaviour. Here:

```text
programmer defines local dynamics
        ↓
dynamics unfold
        ↓
localized organization appears
        ↓
we decide whether "object" is a useful description
```

That reversal is a large part of why artificial life is so compelling.

It is also why it is so easy to fool ourselves.

The object appears first in our perception. Only afterwards do we begin asking whether anything in the mechanism justifies treating that apparent boundary as a real unit of organization.

---

## What Is Actually Moving?

Look at the pattern travelling left to right.

{{< figure
    src="/images/books/digital-life/ch01-lenia-fixed-grid-motion.png"
    alt="Four frames of a Lenia structure moving across a fixed coordinate grid while the lattice remains stationary."
    caption="The pattern moves across the field while the underlying lattice remains fixed."
>}}

The grid does not move. The individual locations do not travel. Location (40, 17) is exactly where it always was, holding whatever value the update rule most recently assigned it. Nothing is transported.

What happens instead is a chain of local reconstruction. State at one location influences nearby updates; a recognizable organization appears slightly farther over; those states influence the next updates; the recognizable organization appears farther over again.

Nothing corresponding to the visible creature has travelled through the grid.

The organization has propagated.

So when we say *the creature moved*, the operational description is:

> **a recognizable organization of state was repeatedly reconstructed at changing spatial coordinates**

Those two sentences describe the same visual event at different levels. One is intuitive and useful for noticing things. The other is operational and useful for measuring things. We will need both, all the way through this book. What matters is knowing, at any moment, which one we are using.

Waves already give us one familiar version of the problem: something recognizable can propagate without its material travelling with it.

So two possibilities remain open. Perhaps identity does not require preserving the same material. Or perhaps we are simply very good at seeing objects where no useful object exists.

The animation cannot decide between them.

---

## The Most Dangerous Word Is "It"

Look at the sentences already used in this chapter.

> It moved. It changed shape. It persisted.

The word **it** is carrying an enormous amount of unearned weight. Before saying that something persists, we need a rule for deciding that the pattern at time *t* and the pattern at time *t+1* are instances of the same continuing organization. That rule might be based on shape similarity, or location, or trajectory, or internal structure, or causal continuity, or something we have not thought of.

We do not have that rule yet. Visual continuity is enough to raise the question. It is nowhere near enough to settle it.

And the question has teeth. What if connected geometry turns out not to be the correct boundary? What if two identical-looking structures have different histories? What if one continuing process occupies several disconnected regions?

So our first definition of *the thing* will remain deliberately provisional. We will use geometry while it works, and replace it if the experiments force us to.

A discipline that helps: keep two descriptions of the same event side by side.

**The tempting description**

```text
It moves.
It eats.
It heals.
It remembers.
It reproduces.
```

**The operational description**

```text
a localized organization is reconstructed at changing coordinates

field quantity is redistributed toward a region and away from others

a measured structural quantity returns toward its pre-perturbation value

a later response differs measurably because of an earlier state

a second structure appears whose form causally depends on the first
```

The left-hand column is how we notice phenomena worth investigating, and abandoning it would make us worse scientists, not better ones. The right-hand column is what we can actually test. Neither should quietly replace the other, and the failure mode of this entire field is the moment the first column starts getting reported as though it were the second.

---

## Now Take Almost Everything Away

Lenia leaves us an easy escape: perhaps the apparent creature depends on all that continuous state, smooth interaction and complicated morphology.

It does not.

Strip computational systems down almost absurdly far and simple local rules still produce global structure that no individual component represents. We do not need a tour of cellular automata to establish that. One much smaller example matters for the question we are asking.

For that, five cells are enough.

Conway's Game of Life is a binary lattice governed entirely by a local update rule. One five-cell pattern discovered in it is the glider.

![A Game of Life glider moving across a fixed lattice](/images/books/digital-life/ch04-glider.gif)

Nothing in the rule says *move diagonally*. There is no velocity variable and no object being transported. Yet the pattern repeatedly reconstructs itself one cell farther across the lattice.

Ask what persisted and the answer is striking. Not the same active cells. Not the same coordinates. Not even the same shape at every intermediate step.

What persisted was the organization.

That separates two ideas ordinary language tends to weld together.

**Material identity** asks whether the same components persist.

**Organizational identity** asks whether a recognizable pattern persists while the components change.

The glider gives us a small but important result:

> **Recognizable organization can persist without persistent material identity.**

We have not found an organism.

We have found a kind of continuity that does not require one fixed body.

---

## What the Lattice Cannot Do

But the glider is missing something important.

Where did it go last week?

Run it across an empty lattice and nothing marks the route. The world after its passage contains no trace that it was ever there.

The lattice is a stage. It records nothing.

That prevents the past from exerting any grip on the future. So we change one thing.

Let simple components alter the world they move through, and let the altered world change what happens next.

---

## A World That Keeps What Happens To It

The new system is a **Physarum-inspired particle model**: a population of extremely simple mobile agents coupled to a field they can both read and alter.[2]

The biological name explains where the idea came from, not what the model is. *Physarum polycephalum* leaves extracellular traces that can affect later behaviour; that observation inspired computational models with a similar feedback structure.[3] Nothing established about the organism is thereby established about the model.

The mechanism is simple. Agents sense the field, turn, move and deposit into it. The field diffuses and fades.

So:

agents
 ↓
change the field
 ↓
the field retains a trace
 ↓
the trace changes later behaviour
 ↓
agents change the field again

There is no network object, route planner or representation of the structure that eventually appears.

There is only the loop.

> **The agents alter the conditions that determine their own future behaviour.**

That is the feature we need. What happens now can leave something behind that changes what happens later.

---

## Watch the Network Appear

![Growth of the Physarum-inspired network from a uniform random start, with a no-feedback control](/images/books/digital-life/ch02-physarum-growth.png)

From a random scatter of agents and an empty field, a network appears.

The biological vocabulary arrives immediately:

trail
foraging
coordination
memory
organism

Again, none of it has been earned.

First eliminate the dull explanation. Perhaps thousands of moving agents depositing material would produce something network-like regardless of feedback.

Disable their ability to sense what previous agents deposited and the network disappears into a haze. With sensing enabled, the concentration measure is **0.883**. With it disabled, **0.153**.

So there really is a reproducible phenomenon here. The feedback loop produces macroscopic organization that largely disappears when the coupling is removed.

That is enough to continue.

Not memory. Not foraging. Not an organism.

Something organized is happening.

Now attack the obvious explanation.

---

## Where Is the Past?

The obvious hypothesis is that the network's history lives in the field. The field is what visibly accumulates, so delete it.

Keep every agent exactly where it is and erase the field completely.

Twenty-five steps later, similarity to the old network is **0.897**, against **0.911** for an undisturbed continuation.

The network comes back.

Why? Because the agents were already standing in the channels they had helped create. Their spatial arrangement was itself a trace of the earlier network. Once they began depositing again, they redrew much of it.

So the history was not only in the field.

Reverse the intervention.

Keep the field, delete the entire population, and replace all twenty thousand agents with naive ones at random positions and headings.

They inherit only a world shaped before any of them existed.

The new population reconstructs substantially more of that old network than an equivalent population starting from an empty field: **0.658 against 0.304** after twenty-five steps. A specificity control shows that populations are drawn back toward the particular historical network they inherit, not merely toward any old network.

The tempting sentence is that the new agents remembered.

They did not. None of them existed when the network formed.

The smaller statement is stranger:

> **The behaviour of a population depended on structure produced before any member of it existed.**

Erase both the field and the population and the advantage disappears. So the history is not nowhere. But neither intervention that removed only one subsystem localized it to that subsystem alone.

The agents can partly reconstruct the field.

The field can partly recruit new agents back into the earlier organization.

Whatever carries the history is distributed across the coupled system.

That is not yet memory.

It is history dependence: something produced earlier measurably changes what happens later.

---

## Start Replacing the Material

A complete population swap is dramatic but artificial. So replace the material slowly instead.

Once the network has formed, continually delete small groups of agents and introduce naive replacements at random positions.

The original population drains away.

By the end of this run, only **7 of the original 20,000 agents remain**. More than 99.9% of the population that built the network is gone.

And yet an organized network remains.

The exact routes do not remain fixed — but neither do they in an undisturbed system. Even without intervention, channels migrate and loops rearrange. So two kinds of continuity have to be separated:

**route identity** — is this the same historical configuration?

**organizational continuity** — is the system still maintaining the same broad kind of structure?

Under continual replacement, route identity gradually drifts, while the organized regime survives in degraded form. Its concentration settles around **0.49**, compared with **0.93** for the undisturbed branch and **0.153** when feedback is disabled.

That degradation suggested an attractive explanation: perhaps replacement was progressively injuring the network.

So stop replacing agents.

Most of the deficit reverses.

The network recovers substantially once the continuous influx of naive agents ends. In this run, most of the degradation was therefore a standing cost of replacement rather than accumulated damage.

The important result is smaller than “the network is unaffected by turnover.” It plainly is affected.

But the agents maintaining the network near the end are almost entirely not the agents that built it. New components arrive into a world already shaped by earlier components and are recruited into continuing organization.

> **Under this configuration, macroscopic organization persisted through replacement of more than 99.9% of the original population.**

The material changed.

Something else continued.

---

## What Survived

Nothing in this chapter gives us a reason to call any of these systems alive.

We did not establish an organism, memory, intelligence or individuality.

But removing those interpretations did not remove the phenomena.

A pattern really can propagate without its material travelling with it.

Organization really can persist while its components change.

A writable environment really can make later behaviour depend on earlier activity.

And in the final system, organized structure persisted while almost the entire population that created it was replaced.

Those are reproducible phenomena. They are not evidence of life.

That distinction matters.

If we merely say *it looked alive*, we have learned almost nothing. But if we respond by saying *it was only a pattern*, we may throw away the interesting part with the bad explanation.

There is something here.

We do not yet know what kind of thing it is.

The explanation kept shrinking.

The phenomenon kept not going away.

---

## What Would We Have to Destroy?

We began with something that looked like a creature.

Then we looked closer.

The Lenia pattern did not carry its material with it. The glider persisted while its active cells changed. In the final system, almost the entire population was replaced and organized structure remained.

None of that makes any of these systems alive.

But neither does the failure of the biological interpretation make the underlying phenomenon disappear.

And the interventions leave us with a better question.

Erasing the field alone was not enough. Replacing the population alone was not enough. Erasing both did reduce the system to a fresh start, so the continuity is not magical and it is not nowhere. But it was not localized to either obvious component.

So instead of asking where the thing is, ask:

> **What would we have to destroy for it to stop being the same thing?**

That is now an experimental question.

The next system will let us attack it directly.

It will not merely tempt us to invent an object.

It will tempt us to invent an organism.

And it will look like it is reproducing.

---

## Experimental Note

The Physarum-inspired results in this chapter come from one implementation under one configuration, with interventions branched from a common checkpoint. Most conditions were single-run demonstrations rather than population-level estimates across seeds.

The numerical claims in the chapter should therefore be read exactly as stated: evidence about this configuration, not estimates of general robustness.

Full parameters, similarity definitions, null construction, intervention protocols, discarded parameterizations, additional measurements and failed runs are provided in the appendix and accompanying experimental material.

---

## References

**[1]** Chan, B. W-C. *Lenia: Biology of Artificial Life.* Complex Systems 28(3), 251–286 (2019).

**[2]** Jones, J. *Characteristics of Pattern Formation and Evolution in Approximations of Physarum Transport Networks.* Artificial Life 16(2), 127–153 (2010).

**[3]** Reid, C. R., Latty, T., Dussutour, A. & Beekman, M. *Slime mold uses an externalized spatial "memory" to navigate in complex environments.* PNAS 109(43), 17490–17494 (2012).

**[4]** Theraulaz, G. & Bonabeau, E. *A Brief History of Stigmergy.* Artificial Life 5(2), 97–116 (1999).
