+++
title = "03: Look at This Thing"
date = "2026-08-14T09:30:00+01:00"
draft = false
description = "Calibrating the microscope. A continuous cellular automaton produces something that looks disturbingly like a creature. We strip it down to almost nothing, then rebuild a world in which the actors rewrite the conditions of their own future — and start deleting the parts to find out where the thing actually lives."
weight = 3
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Lenia", "Cellular Automata", "Physarum", "Agent-Based Models", "Pattern Identity", "History Dependence", "Emergence"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "final"
+++

Don't read anything yet.

Watch this.

{{< figure
src="/images/books/digital-life/ch01-lenia-organism.gif" alt="A localized continuous cellular automaton pattern evolving and moving through time." caption="One state of a continuous cellular automaton evolving through time."
>}}

Something is moving. It appears to have a boundary. Different parts of it seem to behave differently: an edge that ripples, an interior that stays denser, a leading region that seems to pull the rest along. Its shape changes as it travels, and yet some larger organization survives those changes. Watch it for thirty seconds and you will start predicting what it is about to do.

If you saw this without context, biological language would arrive immediately: a cell, a creature, an organism, perhaps even an animal.

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

Start with what is not in the program. There is no object exposing `creature.move()` or `creature.keep_shape()`, no animation path, no skeleton, no set of joints, no controller issuing instructions like *keep the left side attached, push the front forward, restore the outline*. There is no variable called `position_of_creature`, and no field named `head` or `tail`.

Underneath the apparent creature is a field of numbers. Each location changes according to nearby values, using the same rule everywhere, and the field simply changes step after step. The system is **Lenia**, a continuous cellular automaton famous partly because its localized patterns are so easy to describe biologically.[1]

We will resist that language for now. What we have actually observed is a persistent localized pattern — a description that is less exciting and also something we can test.

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

That reversal is a large part of why artificial life is so compelling, and it is also why it is so easy to fool ourselves. The object appears first in our perception. Only afterwards do we begin asking whether anything in the mechanism justifies treating that apparent boundary as a real unit of organization.

---

## What Is Actually Moving?

Look at the pattern travelling left to right.

{{< figure
src="/images/books/digital-life/ch01-lenia-fixed-grid-motion.png" alt="Four frames of a Lenia structure moving across a fixed coordinate grid while the lattice remains stationary." caption="The pattern moves across the field while the underlying lattice remains fixed."
>}}

The grid does not move. The individual locations do not travel. Location (40, 17) is exactly where it always was, holding whatever value the update rule most recently assigned it. Nothing is transported.

What happens instead is a chain of local reconstruction. State at one location influences nearby updates; a recognizable organization appears slightly farther over; those states influence the next updates; the recognizable organization appears farther over again. Nothing has travelled through the grid — the organization has propagated.

So when we say *the creature moved*, the operational description is:

> **a recognizable organization of state was repeatedly reconstructed at changing spatial coordinates**

Those two sentences describe the same visual event at different levels. One is intuitive and useful for noticing things. The other is operational and useful for measuring things. We will need both, all the way through this book. What matters is knowing, at any moment, which one we are using.

Waves already give us one familiar version of the problem: something recognizable can propagate without its material travelling with it. So two possibilities remain open. Perhaps identity does not require preserving the same material — or perhaps we are simply very good at seeing objects where no useful object exists.

The animation cannot decide between them.

---

## The Most Dangerous Word Is "It"

Look at the sentences already used in this chapter.

> It moved. It changed shape. It persisted.

The word **it** is carrying an enormous amount of unearned weight. Before saying that something persists, we need a rule for deciding that the pattern at time *t* and the pattern at time *t+1* are instances of the same continuing organization. That rule might be based on shape similarity, or location, or trajectory, or internal structure, or causal continuity, or something we have not thought of.

We do not have that rule yet. Visual continuity is enough to raise the question. It is nowhere near enough to settle it.

So we will use geometry while it works, and replace it if the experiments force us to.

A discipline that helps: keep two descriptions of the same event side by side.

| The tempting description | The operational description |
|---|---|
| It moves. | a localized organization is reconstructed at changing coordinates |
| It eats. | field quantity is redistributed toward a region and away from others |
| It heals. | a measured structural quantity returns toward its pre-perturbation value |
| It remembers. | a later response differs measurably because of an earlier state |
| It reproduces. | a second structure appears whose form causally depends on the first |

The left-hand column is how we notice phenomena worth investigating, and abandoning it would make us worse scientists, not better ones. The right-hand column is what we can actually test. Neither should quietly replace the other, and the failure mode of this entire field is the moment the first column starts getting reported as though it were the second.

---

## Now Take Almost Everything Away

Lenia leaves us an easy escape: perhaps the apparent creature depends on all that continuous state, smooth interaction and complicated morphology. If so, taking the richness away should take the creature with it.

It does not. Strip a computational system down almost absurdly far and simple local rules still produce global structure that no individual component represents. Five cells are enough to show it.

Conway's Game of Life is a binary lattice governed entirely by a local update rule. One five-cell pattern discovered in it is the glider.

![A Game of Life glider moving across a fixed lattice](/images/books/digital-life/ch04-glider.gif)

Nothing in the rule says *move diagonally*. There is no velocity variable and no object being transported. Yet the pattern repeatedly reconstructs itself one cell farther across the lattice.

Ask what persisted and the answer is striking. Not the same active cells, not the same coordinates, not even the same shape at every intermediate step. But every four generations the configuration is exactly the original again, displaced one cell diagonally.

What persisted was the organization. That separates two ideas ordinary language tends to weld together: **material identity** asks whether the same components persist, while **organizational identity** asks whether a recognizable pattern persists while the components change.

The glider gives us a small but important result:

> **Recognizable organization can persist without persistent material identity.**

We have not found an organism. We have found a kind of continuity that does not require one fixed body.

---

## What the Lattice Cannot Do

But the glider is missing something important. Where did it go last week?

Run it across an empty lattice and nothing marks the route; the world after its passage contains no trace that it was ever there. The lattice is a stage, and it records nothing. That prevents the past from exerting any grip on the future.

So we change one thing. Let simple components alter the world they move through, and let the altered world change what happens next.

---

## A World That Keeps What Happens To It

The new system is a **Physarum-inspired particle model**: a population of extremely simple mobile agents coupled to a field they can both read and alter.[2]

The biological name explains where the idea came from, not what the model is. *Physarum polycephalum* leaves extracellular traces that can affect later behaviour; that observation inspired computational models with a similar feedback structure.[3] Nothing established about the organism is thereby established about the model.

The mechanism is simple. Agents sense the field, turn, move and deposit into it. The field diffuses and fades.

So:

```text
agents
 ↓
change the field
 ↓
the field retains a trace
 ↓
the trace changes later behaviour
 ↓
agents change the field again
```

There is no network object, route planner or representation of the structure that eventually appears. There is only the loop.

> **The agents alter the conditions that determine their own future behaviour.**

This kind of coordination through traces left in a shared environment is often called **stigmergy**.[4] It is the feature we need: what happens now can leave something behind that changes what happens later.

---

## Watch the Network Appear

![Growth of the Physarum-inspired network from a uniform random start, with a no-feedback control](/images/books/digital-life/ch02-physarum-growth.png)

From a random scatter of agents and an empty field, a network appears — and the biological vocabulary arrives immediately: trail, foraging, coordination, memory, organism. Again, none of it has been earned.

First eliminate the dull explanation. Perhaps thousands of moving agents depositing material would produce something network-like regardless of feedback. Disable their ability to sense what previous agents deposited and the network disappears into a haze.

```text
concentration measure

feedback enabled      0.883
feedback disabled     0.153
```

So there really is a reproducible phenomenon here: the feedback loop produces macroscopic organization that largely disappears when the coupling is removed. Not memory, not foraging, not an organism — but something organized is happening, and that is enough to continue.

Now attack the obvious explanation.

---

## Where Is the Past?

The obvious hypothesis is that the network's history lives in the field. The field is what visibly accumulates, so delete it.

Keep every agent exactly where it is and erase the field completely.

```text
similarity to the old network, 25 steps later

field erased              0.897
undisturbed continuation  0.911
```

The network comes back. The natural explanation is that the agents were already standing in the channels they had helped create, so their spatial arrangement may itself have carried part of the earlier network, allowing them to redraw much of it once deposition resumed. That mechanism has not yet been isolated, and what the intervention establishes is narrower: the field was not the sole carrier of the history.

Now reverse the intervention. Keep the field, delete the entire population, and replace all twenty thousand agents with naive ones at random positions and headings. They inherit only a world shaped before any of them existed.

```text
similarity to the inherited network, 25 steps later

naive population, inherited field    0.658
naive population, empty field        0.304
```

The specificity control matters, because a population might simply respond to any mature field. It does not. Placed into network A, a naive population scored `0.658` against the network it inherited and `0.297` against an independently grown one; the mirror experiment with network B scored `0.619` and `0.339`. The effect is specific to the historical network the population was given.

The tempting sentence is that the new agents remembered. They did not — none of them existed when the network formed. The smaller statement is stranger:

> **The behaviour of a population depended on structure produced before any member of it existed.**

Erase both and the advantage disappears, as it should: the field and the agents together constitute the state of this model, so resetting both is effectively a fresh start. The informative result is that removing either candidate carrier *alone* was not enough. The agents can partly reconstruct the field; the field can partly recruit new agents back into the earlier organization. Neither intervention localized the historical effect to one subsystem, so whatever carries the history is distributed across the coupled system.

That is not yet memory. It is history dependence: something produced earlier measurably changes what happens later.

---

## Start Replacing the Material

A complete population swap is dramatic but artificial. So replace the material slowly instead.

Once the network has formed, every five steps delete 2% of the agents and introduce the same number of naive replacements at random positions. Continue for two thousand steps, and the original population drains away: by the end of the run only **7 of the original 20,000 agents remain**, more than 99.9% of the builders gone.

And yet an organized network remains.

The exact routes do not stay fixed — but neither do they in an undisturbed system, where channels migrate and loops rearrange on their own. So two kinds of continuity have to be separated. **Route identity** asks whether this is the same historical configuration. **Organizational continuity** asks whether the system is still maintaining the same broad kind of structure.

Under continual replacement, route identity gradually drifts while the organized regime survives in degraded form:

```text
concentration measure

continual replacement     0.49
undisturbed branch        0.93
feedback disabled         0.153
```

That degradation suggested an attractive explanation — perhaps replacement was progressively injuring the network. So stop replacing agents, and most of the deficit reverses:

```text
concentration after replacement stops

at stop            0.490
+100 steps         0.581
+500 steps         0.724
+1000 steps        0.798
```

It does not regain the undisturbed value inside the observation window. But in this run most of the degradation was a standing cost of continued replacement rather than accumulated damage.

The important result is smaller than *the network is unaffected by turnover*. It plainly is affected. What survives is narrower: the agents maintaining the network near the end are almost entirely not the agents that built it, and new components arrive into a world already shaped by earlier ones and are recruited into continuing organization.

> **Under this configuration, macroscopic organization persisted through replacement of more than 99.9% of the original population.**

The material changed. Something else continued.

---

## What Would We Have to Destroy?

Nothing in this chapter gives us a reason to call any of these systems alive. We did not establish an organism, memory, intelligence or individuality. But removing those interpretations did not remove the phenomena.

Some of what survived was visible directly in the mechanism: a pattern can propagate without its material travelling with it, and a glider can return to exactly the same configuration while its active cells change. The stronger results survived intervention. In the writable-world system, later behaviour remained dependent on earlier activity after we removed either of the two obvious places that history might reside — and organized structure persisted while more than 99.9% of the population that created it was replaced.

Those are different kinds of evidence and we should not blur them, and none of them is evidence of life. But *only a pattern* is not much of an explanation either. The explanation kept shrinking; the phenomenon kept not going away.

Which leaves a better question than the one we started with. Erasing the field alone was not enough. Replacing the population alone was not enough. The historical effect was not localized to either obvious subsystem. So instead of asking where the thing is, ask:

> **What would we have to destroy for it to stop being the same thing?**

This system can only take that question so far. It maintains an organization; it does not give us a clean second individual whose ancestry we can follow.

The next system does. It will not merely tempt us to invent an object — it will tempt us to invent an organism, and it will look like it is reproducing.

---

## Experimental Note

The Physarum-inspired results in this chapter come from one implementation under one configuration, with interventions branched from a common checkpoint. Most conditions were single-run demonstrations rather than population-level estimates across seeds.

Two distinct quantities are reported. *Concentration* measures how much structure the field carries at a given moment; *similarity* measures agreement between a current network and a stored reference network. They are not comparable to one another, and each fenced block in the chapter states which one it reports. The undisturbed concentration figures quoted in different experiments (`0.883` and `0.93`) are drawn from different runs and time points and should not be read as a discrepancy.

The numerical claims in the chapter should therefore be read exactly as stated: evidence about this configuration, not estimates of general robustness.

Full parameters, similarity definitions, null construction, intervention protocols, discarded parameterizations, additional measurements and failed runs are provided in the appendix and accompanying experimental material.

---

## References

**[1]** Chan, B. W-C. *Lenia: Biology of Artificial Life.* Complex Systems 28(3), 251–286 (2019).

**[2]** Jones, J. *Characteristics of Pattern Formation and Evolution in Approximations of Physarum Transport Networks.* Artificial Life 16(2), 127–153 (2010).

**[3]** Reid, C. R., Latty, T., Dussutour, A. & Beekman, M. *Slime mold uses an externalized spatial "memory" to navigate in complex environments.* PNAS 109(43), 17490–17494 (2012).

**[4]** Theraulaz, G. & Bonabeau, E. *A Brief History of Stigmergy.* Artificial Life 5(2), 97–116 (1999).
