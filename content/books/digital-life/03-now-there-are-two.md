+++
title = "03: Now There Are Two"
date = "2026-08-14T10:00:00+01:00"
draft = false
description = "Persistence is not reproduction. In a binary cellular automaton nobody designed for the purpose, structures appear to make copies of themselves — and this time, when we attack the interpretation, it survives."
weight = 3
series = ["Digital Life From First Principles"]
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Outlier", "Cellular Automata", "Self-Replication", "Causality", "Ancestry", "Experimental Method"]
+++

We have learned not to trust the first noun.

Fine.

---

In the previous chapter an organization survived while nearly everything participating in it was taken away and replaced. By the end of the turnover window, only 7 of the original 20,000 agents remained.

The exact routes had drifted. The broader organized network had not disappeared.

That was persistence, and it was hard-won.

It was also not reproduction, and the gap between those two words is wider than it looks.

A process can persist throughout an observation without ever producing a descendant. Our Physarum experiment did exactly that. It formed, degraded, recovered and remained organized at the end of the run.

But we never defined or observed a descendant relation.

Continuation is one capability. Producing another causally descended organization is a different one, and nothing measured in the previous chapter establishes it.
 Continuation is one capability. Making another one is a different capability, and nothing we measured in the last chapter bears on it at all.

The glider looks like the harder case, and it is worth spending a moment on, because it is where the distinction becomes precise instead of merely rhetorical.

Every four generations the glider's configuration recurs one cell diagonally along, built from active cells at different coordinates. New material participation, recurring organization, generation after generation.
 If anything in the previous chapter deserved the word *reproduction*, surely that did.

It does not qualify, and the reason is not our invention. In the causal analysis we are about to rely on, Hintze and Bohm set out a criterion for calling a structure a self-replicator: it must produce at least two copies of itself, each causally traceable back to the original, and not to each other.[6] The glider fails it. Each glider copy descends from the copy immediately before it, in a single unbranching chain. Nothing ever forks. A glider gun fails for a different reason — it produces gliders, not glider guns.

That criterion is doing real work, so it is worth stating on its own:

> **An earlier organization must give rise to at least two later organizations of the same kind, each causally dependent on the original and not on one another.**

Chains are not enough. The history has to branch.

We did not construct that standard to fit a result we already had, which is exactly why it is useful to us. It comes from the literature we are about to test our own run against, and it disqualifies the most charismatic object in the previous chapter.

Now look at this.

![The published Outlier cellular automaton evolving from its tiny seed](/images/books/digital-life/ch10-outlier-growth.gif)

---

## The Rule Was Searched. The Replicator Wasn't.

Artificial life already contains systems that reproduce, evolve, conserve material and generate structures nobody explicitly designed. Evoloops, Flow-Lenia, Genelife and more recent computational-life experiments each cover different parts of that territory, and there are other books for surveying them.[1–4] For our purposes one system is unusually useful, and it is called **Outlier**.

The mechanism will take one paragraph, because the previous chapter has already done the teaching.

Every cell is `0` or `1`. Each cell reads its `3 × 3` Moore neighbourhood, itself included, which gives 512 possible local configurations, and the rule specifies an output for each. That is the entire law of this universe: 512 output bits. The published rule is rotationally symmetric but not mirror-symmetric, and 220 of its 512 entries produce an active centre cell, which makes it a good deal denser than the 140 of Conway's Game of Life.[5]

Note what is absent. No `Organism`. No genome, no energy budget, no `reproduce()`, no fitness function, no population manager, no representation of an individual anywhere. There is binary state, a neighbourhood, a transition rule and time.

The provenance matters, and the sloppy version of it is false.

Outlier was found by an automated search — genetic programming across cellular-automaton rules, looking for dynamics that might support open-ended evolution.[5] Humans wrote the search. Humans defined the rule space, the substrate and the selection criteria. Nothing here appeared independently of human design in any absolute sense, and anyone claiming otherwise is selling something.

But the search was for a universe, not for a replicator. Self-replication was not an explicit objective.[5] What the search returned was a local transition rule. The particular replicating organizations later observed were not explicitly represented in that rule or specified as the target of the search.

That distinction is the whole reason Outlier is worth our time:

```mermaid
flowchart LR
    subgraph Designed
        A1["Programmer writes reproduction"] --> A2["Structure reproduces"]
        A2 --> A3["Emergence of reproduction remains untested"]
    end

    subgraph Outlier
        B1["Search finds local physics"] --> B2["Physics runs"]
        B2 --> B3["Structures appear"]
        B3 --> B4["Some of them replicate"]
    end
```

In the first route, observing reproduction tells us only that somebody implemented it. In the second there is no reproduction operator to point at. If a structure reproduces here, the mechanism has to be realized through the unfolding dynamics, because there is nowhere else for it to live.

That does not establish life. It establishes something we need before the question of life is worth asking at all:

> **the behaviour is not the execution of an operation we named in advance.**

---

## It Looks Like Reproduction, Which Is the Problem

Run the published rule from sparse random conditions, or from a tiny seed, and the world fills with activity.[5]

Small shape-shifting clusters appear. Some of them produce further clusters. Some periodically duplicate. Smaller structures assemble into larger formations, and those formations duplicate too. Collections of them eventually form the boundary of a still larger expanding complex.

![Outlier at successive generations from the same initial seed](/images/books/digital-life/ch10-outlier-snapshots.png)

So there is organization at several levels simultaneously:

```text
cells
  ↓
clusters
  ↓
replicating formations
  ↓
larger expanding complex
```

Yang classified structures at more than one of those scales as self-replicating, under the operational criterion used in that work.[5] Duplication-like recurrence really does appear at multiple scales, and that alone is stranger than anything in the previous chapter. The glider gave us one localized organization persisting through time. Here we have organizations built out of organizations, with apparent duplication at more than one level of the hierarchy.

It is worth being honest about the effect this has on a viewer.

The glider was easy to hold at arm's length. Outlier is not. Structures appear, collide, leave debris and produce further structures, and regions of the world acquire recognizable histories. The vocabulary we spent two chapters restraining comes back within seconds — parent, offspring, population, lineage, organism.

But those words smuggle in different claims. Parent, offspring and lineage assert causal descent. Organism asserts a boundary and an individual. Population assumes we already know which things should be counted together.

The animation establishes none of them.

Consider the entire evidential content of the observation:

```text
time t

    A

time t + 500

    A     A
```

The sentence that arrives unbidden is *A reproduced*. But the same image is produced by at least three other stories. Both structures may have been generated independently by the surrounding dynamics. The second may have appeared for reasons that had nothing to do with the first, and would have appeared even if the first had never existed. Or what we are calling two structures may be two parts of one larger repeating process that our detector happened to split.

Nothing in the geometry distinguishes these.

```text
similarity
≠
ancestry
```

That is the load-bearing sentence of this chapter, and it is the sharpened form of the rule from Chapter 1 that appearance is not mechanism. Reproduction cannot be established from the final picture, because reproduction is a claim about causation and the picture contains no causation. It contains only the outcome.

---

## What Determinism Buys Us

Here Outlier gives us something almost no interesting system gives us.

It is deterministic and completely specified. For every live cell at time `t+1` we know exactly which `3 × 3` neighbourhood produced it, and we know the full mapping from neighbourhoods to outcomes. There is no learned function, no hidden state, no floating-point drift and no stochastic component. For any modified neighbourhood, the next cell state can therefore be computed exactly from the rule.

That does not make causality automatic.

The update is exact. Which counterfactuals we choose to treat as causal evidence, and how we aggregate those cell-level dependencies into ancestry between larger structures, remain methodological decisions.

So a question that is usually unanswerable becomes mechanical:

> Which live cells in the preceding neighbourhood were actually necessary for this cell to be alive?

The published framework answers it carefully, and the care matters. Rather than asking whether removing any single predecessor changes the outcome, Hintze and Bohm identify the *minimal subset* of live neighbours that the transition actually requires, and exclude the rest from the causal trace.[6] This handles a real problem: update rules contain redundancy, and a neighbour that happens to be alive is not thereby a cause of anything. Where more than one minimal subset exists, their method conservatively includes all contributing clusters — a case they report not encountering in Outlier, though the method is built to handle it.[6]

Cell-level dependencies are far too numerous to reason about individually, so they are aggregated. Cells are grouped into clusters by adjacency, and a cluster is counted as causally derived from an earlier one if any of its cells depends on a cell belonging to that ancestor.[6]

The result is a graph rather than an impression.

```text
cluster at t
     ↓
cluster at t+1
     ↓
cluster at t+2
     ↓
...
```

with branching wherever one earlier organization contributes to several later ones. And the question has changed completely. Not *does this later structure resemble the earlier one*, but:

> **Can we trace a causal path by which the earlier organization contributed to producing the later one?**

One restriction is worth carrying forward, because it makes the published result more conservative rather than less. The causal work counts only exact copies, where the earlier study allowed rotational variants.[6] Whatever it finds, it is not finding it by relaxing what counts as the same structure.

---

## Three Replicators, Three Fates

Applied to a `1024 × 1024` periodic world run for 20,000 ticks, that method produced a causal ancestry graph of **31,959,320 cluster instances and 65,552,995 directed causal edges**, across 966,208 distinct clusters.[6]

Underneath an animation that reads as a few dozen things moving around.

The interesting part is what happens when three specific structures are followed through it. Within the first 10,000 ticks:[6]

```text
c0    433 copies         no second generation
c1  1,677 offspring      reached a second generation
c2  2,439 appearances    15 generations
```

The seed cluster `c0` produced 433 copies, every one of them causally traceable to the original. On the criterion above it is a genuine self-replicator, and it is also an almost complete failure: not one of those 433 offspring went on to produce a `c0` of its own inside the window. The second cluster, `c1`, did better — 1,677 offspring, and near tick 10,000 one of them produced three more, which is a second generation and not much else. The third, `c2`, replicated more often than either and, crucially, its offspring kept replicating: fifteen generations of causal descent, growing at a fitted factor of roughly 1.5 per generation over the first ten.[6]

So a word we were treating as one thing turns out to be three:

```text
recurrence
≠
replication
≠
sustained lineage
```

`c0` is the instructive case, because 433 is a spectacular-sounding number attached to a lineage that went nowhere. Producing copies and founding a dynasty are different achievements, and the first can be reported in a way that strongly implies the second. Biology would have taught us that distinction eventually. It is startling to meet it in 512 bits.

---

## The Fast Ones Did Worse

The original `c2` does not neatly divide in two. It produces many offspring, of which four go on to replicate themselves. Two of those complete the process in 675 ticks; the other two take 778.[6]

The obvious expectation is that the faster replicators win. Shorter generation time, more descendants, straightforward.

The opposite happened. Over the full phylogeny the 675-tick lineage produced 96 replication events and the slower 778-tick lineage produced 125.[6]

The authors attribute the difference to geometry. The faster branches expand in roughly horizontal directions, while the slower pair travel obliquely and interfere with one another less. In the observed phylogeny, the faster paths therefore encounter more collisions while the slower paths retain more room in which to continue.[6]

The measurement is solid: shorter replication time did not correspond to greater realized lineage output. The proposed explanation — spatial interference — is strongly suggested by the trajectories, but it was not isolated here by an intervention. We should keep those two things separate.

Even with that boundary, the result is valuable. A familiar expectation — shorter generation time should produce more descendants, other things being equal — failed in this environment. Spatial direction and available room became candidate constraints on reproductive success.

That is exactly the kind of substrate-specific constraint Chapter 1 told us to look for: not a biological requirement copied into software, but a consequence of the computational world in which the process happens.

The same run offers a second, quieter surprise. Three of the four developmental pathways diverge substantially at the start and then converge, passing through an identical sequence of cluster states for their final 143 ticks before producing offspring.[6]

Different beginnings can therefore enter the same terminal developmental sequence.

That makes the mechanism harder to describe as a body simply being copied. Replication here is an extended dynamical process through intermediate organizations, some of which bear little resemblance to the eventual offspring.

---

## The Replicator Might Not Be a Body

Which brings us to the finding that puts the most pressure on intuition.

A self-replicating organization in Outlier does not necessarily correspond to one compact connected cluster. The replication process frequently unfolds across multiple spatially disjoint patterns, which stay disconnected for a number of ticks before merging or branching further, and which coordinate well enough to complete a replication between them.[6] The published work reads this as distributed, multi-component selfhood.[6]

We do not need the stronger noun. The narrower statement is enough, and it is quite strong enough:

> **Causal self-replication can involve multiple spatially separated components.**

Notice what that does and does not say. It does not say those components constitute one natural individual. It says connectedness is not a sufficient criterion for locating the reproducing unit — that a detector built to look only for compact connected bodies would have missed reproduction that was demonstrably occurring.

The previous chapter left us with a version of this problem already. Every intervention there failed to localize the continuing organization to either the agents or the field, and what the experiments kept pointing at was the relationship between them. Outlier now produces the same discomfort from the opposite direction: here we can follow ancestry exactly, and the thing with the ancestry still refuses to be a single object.

> **If reproduction can be causally real while the reproducing unit is not a neat connected body, what exactly is the thing that reproduces?**

Resist the urge to answer. The temptation is to jump from *distributed causal reproduction* to *one distributed individual*, and no experiment here licenses that jump. Individuality would need a criterion we do not have, and inventing one to fit the case in front of us is how this field produces its worst results.

The question stays open. It gets considerably harder later.

---

## 144 Copies Prove Nothing

Published evidence tells us what Outlier has been shown to do. We also wanted a specimen we controlled.

So we reconstructed the rule and verified it before asking it anything: all 512 transition cases decoded, exactly 220 active outputs, published rotational symmetry confirmed. The details belong in the experimental record. The principle belongs here.

> **Verify the world before interpreting anything that happens inside it.**

A wrong decoder still produces extraordinary animations. It cannot produce evidence about Outlier.

Scale is part of the experimental condition, and ours is smaller: a `512 × 512` world over 1,600 generations, against the published `1024 × 1024` over 20,000 ticks. That is not cosmetic. Yang reports a strong scale effect in this rule, and the published causal run behaves differently after about tick 10,000, when the expanding front meets the periodic boundary and the uninterrupted leading edge disappears.[5][6] Our run never reaches that regime.

So everything below carries its scope with it, and does not generalize upward by default.

Now the experiment. We wanted to avoid the failure mode where you hunt through a large run for shapes that seem to repeat, because that guarantees a result: among a hundred thousand clusters, *something* recurs, and whatever recurs most strikingly will feel like a discovery. Instead we derived the target signature in advance from the known seed — the small structure the published work designates `c2`, six cells in a `3 × 3` bounding box in our run — and only then searched for later occurrences of that structure.

Our detector treats translation and quarter-turn rotation as equivalent, so the 144 matches below are occurrences of the same `c2` equivalence class under that identity convention.

That is deliberately broader than Hintze and Bohm's later causal study, which restricted its replication analysis to perfect copies rather than rotational variants.[6]

The search found **144 `c2`-equivalent occurrences** between `t = 2` and `t = 1598`.

That is an observation. It is not reproduction, and the gap is the whole point of the chapter. One hundred and forty-four copies are entirely compatible with one hundred and forty-four independent products of the same underlying dynamics, none of which had anything to do with any other.

Encouragingly, this is not a scruple we invented. The authors of the causal study raise precisely the same possibility about their own result: that `c2` patterns might simply arise often, with descent being a correlate of the dynamics rather than a cause.[6] Their answer is the causal trace, and so is ours.

So we built the graph for our own run:

```text
138,891 clusters
196,466 causal edges
```

That number is itself a correction. The animation looks like a modest collection of discrete moving objects. Underneath it is a network of nearly two hundred thousand dependencies, and our visual impression of *a few things moving around* was never a description of the mechanism.

Then we intersected recurrence with ancestry, searching forward from each `c2`-equivalent occurrence for later members of the same equivalence class reachable through the causal graph.

Our search stops a causal branch at its first return to `c2`. In this run, at least one `c2` occurrence has multiple such first returns, and the complete return graph contains 99 causal return edges.

That establishes branching causal recurrence under our detector.

There is one further condition if we want to claim that this run satisfies Hintze and Bohm's stricter self-replication definition: two candidate offspring must each depend causally on the parent while not depending causally on one another. The current first-return construction does not explicitly test that final independence condition.

![A readable subset of the Outlier c2 causal family tree](/images/books/digital-life/ch10-outlier-causal-lineage.png)

The figure shows a deliberately pruned family, because the full graph is unreadable as an illustration. The analysis uses all of it.

---

## This Time, the Interpretation Survives

It is worth being explicit about what just happened, because it has not happened before in this book.

We began with a criterion set independently of our result, one that had already disqualified the most persuasive object we had. We fixed the target structure in advance rather than choosing it after seeing which shapes recurred. Then we asked how much of that criterion our own causal reconstruction could actually establish.

It established more than resemblance:

structural recurrence
+
causal ancestry
+
multiple causal first returns

Bounded to what was actually run:

> **In our 512 × 512, 1,600-generation run, recurring `c2` structures participate in a branching causal return graph: later occurrences of `c2` are reachable through measurable causal ancestry originating in earlier `c2` structures.**

That sentence is narrow, hedged and specific. It is also the strongest positive result in the book so far, and it deserves to be stated without apology.

Earlier `c2` organization participates measurably in producing later `c2` organization, and the resulting history branches. No reproduction function was written anywhere. The capability arises from a local rule applied repeatedly, in a universe found by a search that was not looking for it.

This matters for the method as much as for the result.

The purpose of the procedure is not to make interesting interpretations disappear. It is to discriminate between claims that survive a stated test and claims that do not. A negative result would have been perfectly acceptable.

What matters is that a positive result is possible when the evidence supports one.

```text
appearance
↓
stronger criterion
↓
causal test
↓
claim survives
```

---

## What We Did Not Earn

Discipline now, while the result is fresh and most attractive.

Causal self-replication is a strong result. It is also only causal self-replication. By itself it establishes nothing about self-maintenance, adaptation, agency, memory, autonomy, individuality, open-ended evolution or life. Those remain separate questions, and they remain separate precisely because reproduction has now earned the right to stand on its own rather than be smuggled in alongside them.

Note also what the multi-component finding did to our vocabulary. We can say that reproduction occurred. We cannot yet say *what* reproduced, because the reproducing organization need not correspond to anything our eyes or our connected-component detector would isolate as an object.

The supported statement is narrower than any single word we might reach for:

> **Very simple digital physics can support emergent structures that satisfy a defined causal criterion for branching self-replication, including replication processes that involve multiple spatially separated components.**

That is already remarkable. Embellishing it would cost us the only property that makes it worth reporting.

---

## Two Instruments, Each Missing Something

There is a failure mode available here, and it should be named before we walk into it.

Having found a system that does something remarkable, the obvious move is to start bolting capabilities onto it. Give Outlier a memory. Give it an energy budget. Give it goals. That would build a new cargo cult on a more respectable foundation.

```text
Outlier is evidence, not specification
```

We are not going to copy its rule, its structures or its geometry. Its value is as a demonstration of what a substrate can support without anyone specifying the resulting organization. The demonstration is the transferable part.

The specific 512 bits remain a valuable specimen, but they are not a blueprint for what we build next.

But there is a second reason not to build on it, and it is more interesting than the first.

Outlier is extraordinary evidence partly because it is rich. Structures interact, recombine, produce debris and build hierarchies.

That same richness makes higher-level mechanisms difficult to isolate.

We can intervene on cells, seeds and even the transition rule itself. What Outlier does not give us is a clean higher-level parameterization: there is no independent dial for coupling, interaction range, memory, turnover or reproductive mechanism that we can vary while holding the rest fixed.
 Suppose we want to know why one process continues while another stops, or whether stored history changes a later response, or what finite computational scarcity does to interaction. Outlier offers no dial for any of it. There is no parameter marked *coupling*, nothing governing how far influence travels, nothing to hold fixed while varying something else. There are 512 bits that produce this universe or a different one.

Now put that beside the previous chapter, and the shape of the problem becomes clear.

```text
Physarum model    separable higher-level interventions, no operational lineage
Outlier           reconstructible causal lineage, no clean higher-level dials

```

The Physarum system let us delete the field, replace the population, run a specificity control and switch turnover off again — but the model supplied no operational descendant relation to follow.

Outlier gives us something complementary: a deterministic substrate from which causal ancestry can be reconstructed at cell level, but few clean ways to vary one interpretable higher-level mechanism while leaving the rest untouched.

The two systems therefore expose complementary strengths rather than forming opposites.
 Neither is the laboratory this book eventually needs, which would have both at once: every rule known, every intervention controllable, one mechanism variable at a time, and a history that can be followed rather than inferred.

That is a specification for something we will have to build.

---

## And Then We Noticed Something Else

We had just earned our strongest positive result. The obvious interpretation had survived the stronger test.

Which matters psychologically as well as scientifically, and not in a good way. Once one exciting claim survives, the next exciting claim becomes much easier to believe.

That is where the trouble starts.

Watching the same simulation, another pattern became difficult to ignore. Structures seemed to move together — not merely outward, as fragments carried on one expanding front would, but with an apparent directional coherence that looked strongest among structures sharing recent causal history.

The biological noun arrived immediately.

**Flocking.**

We knew better than to trust it. Unfortunately we also had a reason to think it might be real, and worse, we had the causal graph, which meant shared ancestry could be identified independently of motion. The hypothesis was testable.

So we did what the method requires.

```text
observation
↓
hypothesis
↓
measurement
↓
control
```

---

## Experimental Note

Our own measurements come from one implementation under one configuration: a `512 × 512` world run for 1,600 generations from the published seed, with the rule decoded and verified against all 512 transition cases, 220 active outputs and the published rotational symmetry. The `c2` signature was fixed in advance from the seed rather than selected from the run, and matching allowed translation and rotation. Causal reconstruction is at cell level, aggregated to clusters by adjacency.

Our implementation does not use the full minimal-subset reconstruction of Hintze and Bohm. For each live child cell, it removes each live predecessor individually and records a dependency when that single removal changes the child from live to dead.

That is a legitimate local but-for test, but it is not equivalent to the published method. In particular, redundant causal sets can be missed, and because the Outlier rule is non-monotonic there is no general basis for describing the resulting graph simply as a lower bound on the published causal graph.

The measurements reported from our run should therefore be interpreted under this explicitly stated causal criterion. Reproducing the published minimal-subset procedure is a separate validation step.

Our indexing places the initial seed at `t = 0`, which puts the first `c2` occurrence at `t = 2`; the published causal study refers to the original `c2` at `t = 3`. We treat this as a difference in indexing convention rather than a disagreement about the structure. Published figures throughout are from the 1024 × 1024, 20,000-tick run and are reported as such; nothing from our smaller run is generalized to that regime. Full protocols, the decoder verification and the discarded runs are in the appendix.

---

## References

**[1]** Sayama, H. & Nehaniv, C. L. *Self-Reproduction and Evolution in Cellular Automata: 25 Years After Evoloops.* Artificial Life 31(1), 81–95 (2025).

**[2]** Plantec, E., Hamon, G., Etcheverry, M., Chan, B. W-C., Oudeyer, P-Y. & Moulin-Frier, C. *Flow-Lenia: Emergent Evolutionary Dynamics in Mass Conservative Continuous Cellular Automata.* Artificial Life 31(2), 228–250 (2025). doi:10.1162/artl_a_00471

**[3]** Packard, N. H. & McCaskill, J. S. *Open-Endedness in Genelife.* Artificial Life 30(3), 356–389 (2024). doi:10.1162/artl_a_00426

**[4]** Agüera y Arcas, B. et al. *Computational Life: How Well-formed, Self-replicating Programs Emerge from Simple Interaction.* arXiv:2406.19108 (2024).

**[5]** Yang, B. *Emergence of Self-Replicating Hierarchical Structures in a Binary Cellular Automaton.* Artificial Life 31(1), 96–105 (2025). doi:10.1162/artl_a_00449

**[6]** Hintze, A. & Bohm, C. *Rethinking self-replication: detecting distributed selfhood in the Outlier cellular automaton.* npj Complexity 3, 11 (2026). doi:10.1038/s44260-026-00074-2
