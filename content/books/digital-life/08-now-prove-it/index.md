+++
title = "Digital Life 08: Now Prove It"
date = "2026-08-11T14:49:00+01:00"
draft = false
description = "Turn appealing observations into experiments by defining properties, measurements, interventions, controls, confounds and bounded claims."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Experimental Method", "Evidence", "Controls", "Causality", "Artificial Life"]
+++

We have accumulated a dangerous number of impressive words.

So far we have talked about:

```text
emergence
complexity
entity
persistence
movement
robustness
regeneration
reproduction
inheritance
selection
adaptation
evolution
open-endedness
progress
````

Some of those words were earned carefully.

Some were only provisional.

Some described observations.

Some described mechanisms.

Some described measurements.

Some described aspirations.

And some may eventually turn out not to be useful at all.

That is exactly how a project like this gets into trouble.

We start with:

```text
interesting pattern
```

and gradually upgrade it in language:

```text
pattern
↓
structure
↓
entity
↓
organism
↓
life
```

without necessarily adding evidence at each step.

So before we move any further, we need a rule.

Not a cellular-automaton rule.

An experimental rule.

> **From this point onward, naming a property does not count as demonstrating it.**

If we say a system:

```text
moves
repairs
remembers
reproduces
inherits
adapts
evolves
```

then we need to say what observation would make that claim true.

And what observation would make it false.

---

# The central problem

Artificial-life systems are unusually easy to overinterpret.

They are visual.

They move.

They deform.

They split.

They collide.

They produce structures that our visual system immediately turns into objects.

Then our language does the rest.

A blob becomes:

> an organism.

A split becomes:

> reproduction.

A return toward an earlier shape becomes:

> healing.

Two nearby moving objects become:

> flocking.

A changing population becomes:

> evolution.

A recurring state becomes:

> memory.

The system may indeed possess some of those properties.

But the animation does not decide that.

We do.

So we need a process that stands between:

```text
what we see
```

and:

```text
what we claim
```

---

# Observation is the beginning

The first step is still observation.

That matters.

A spectacular image can be scientifically valuable.

A strange animation can reveal something nobody thought to measure.

Human pattern recognition is not the enemy.

It is often how hypotheses begin.

Suppose we see:

```text
a localized structure
moving across the field
```

The wrong response is:

> Don't trust your eyes, therefore ignore it.

The better response is:

> Interesting. What exactly do I think I am seeing?

Observation generates the hypothesis.

It does not establish it.

---

# Name the hypothesis

Suppose an animation appears to show:

> movement.

Turn that into a hypothesis.

For example:

> **A localized organization changes position through time while preserving a defined identity criterion.**

That is already much better than:

> It moves.

Now we can ask what must be measured.

For a localized pattern we might track:

```text
centroid
bounding box
orientation
phase
shape similarity
```

Movement becomes a relationship between observations across time.

The word now has experimental content.

---

# Define what would count as evidence

Suppose we claim:

> the pattern persists.

What would count?

Maybe:

```text
the same state exists after every update
```

for a block.

Maybe:

```text
the state recurs after period p
```

for an oscillator.

Maybe:

```text
the state recurs after period p
up to translation Δ
```

for a glider.

There is no universal persistence metric.

The measurement depends on the proposed identity criterion.

That is not a weakness.

It is the experiment.

---

# The evidence ladder

We can now make the core structure of this book explicit.

A strong claim should move through something like:

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

Those levels matter.

Consider:

> The system regenerates.

We can unpack it.

## Property

```text
regeneration
```

## Candidate mechanism

```text
local dynamics restore lost organization
```

## Implementation

```text
specific transition rule
or learned local update process
```

## Observation

```text
pattern looks damaged
then later resembles earlier form
```

## Measurement

```text
IoU / shape similarity / functional performance
```

## Controlled experiment

```text
defined perturbation
+
matched undamaged control
+
multiple damage locations
+
repeated trials
```

## Bounded claim

> Under this perturbation protocol, the system returned to at least 0.90 structural similarity within 50 updates in 78% of trials.

That is what “regeneration” looks like when translated into evidence.

---

# Implemented is not demonstrated

This distinction is critical.

Suppose we write:

```python
class Organism:
    def heal(self):
        ...
```

Have we demonstrated healing?

No.

Suppose we add:

```python
memory = []
```

Have we demonstrated memory?

No.

Suppose offspring receive:

```python
child.genome = parent.genome.copy()
```

Have we demonstrated meaningful inheritance?

Not necessarily.

We have implemented mechanisms that we believe may support those properties.

That gives us:

```text
candidate mechanism
```

not:

```text
established phenomenon
```

A class name is not evidence.

A function name is not evidence.

A variable name is not evidence.

The implementation has to survive contact with measurement.

---

# Correlation is not mechanism

Suppose two things happen together.

```text
event A
+
event B
```

We observe:

```text
A occurs
then B occurs
```

It is tempting to say:

```text
A caused B
```

But perhaps both were caused by:

```text
C
```

Or perhaps B would have occurred anyway.

This is why intervention matters.

Consider reproduction.

We see:

```text
pattern P
```

and later:

```text
pattern P
pattern P
```

Similarity and temporal order are not enough.

A stronger question is:

> If the supposed parent had not been present, would the supposed offspring still have appeared?

That is a causal question.

We can approximate it with a counterfactual experiment.

---

# Remove the mechanism

A general rule keeps appearing throughout this book:

> **If you think a mechanism causes a capability, remove or disrupt the mechanism.**

Suppose we think:

```text
memory state
```

is responsible for improved future behavior.

Run:

```text
memory intact
```

against:

```text
memory removed
```

Suppose we think inheritance gives successors an advantage.

Compare:

```text
inherited successor
```

against:

```text
scratch successor
```

Suppose we think a candidate parent produced an offspring.

Compare:

```text
parent present
```

against:

```text
parent removed
```

Suppose we think local communication causes coordination.

Disrupt communication.

Then measure the difference.

Mechanisms become convincing when the capability depends on them.

---

# The control is part of the claim

A measurement by itself often tells us very little.

Suppose after damage we measure:

```text
recovery score = 0.87
```

Is that impressive?

Compared with what?

Perhaps an undamaged pattern scores:

```text
0.99
```

Perhaps a random process scores:

```text
0.82
```

Perhaps a frozen copy scores:

```text
0.88
```

Without a control, the number floats without meaning.

So every strong experiment should ask:

> **What alternative explanation does this control eliminate?**

That question is more useful than simply adding controls mechanically.

---

# Controls should attack explanations

Consider a claim:

> The system adapted to a changed environment.

Possible alternative explanations include:

```text
performance was already improving
the environment became easier
random variation happened to help
the metric itself changed
the system memorized one answer
```

So useful controls might include:

```text
no inheritance
shuffled inheritance
no variation
unchanged environment
held-out environment
scratch restart
```

Each control attacks a different explanation.

A control is not decoration.

It exists because there is something specific we are trying to rule out.

---

# The first control can be wrong

This is worth saying explicitly.

You can design a control.

Run it.

Get a beautiful result.

And still be wrong.

Perhaps the control introduces its own bias.

Perhaps the comparison groups differ in some hidden variable.

Perhaps the metric accidentally uses information from the thing it is supposed to control for.

Perhaps the intervention changes more than one mechanism.

That does not invalidate the method.

It is the method.

The next step is:

```text
LOOK FOR THE CONFOUND
```

---

# The confound is often the real discovery

Suppose two groups differ.

We conclude:

```text
ancestry causes coordinated movement
```

Then we notice:

```text
same-family individuals are also much closer together
```

Now the interpretation changes.

Maybe:

```text
proximity
```

causes the apparent coordination.

So we match groups by distance.

If the effect disappears, the result is not:

> the experiment failed.

The result is:

> **the proposed explanation failed.**

That is useful knowledge.

A good experiment can destroy the hypothesis that motivated it.

---

# Build the better control

This gives us a stronger experimental loop:

```text
SEE SOMETHING
↓
NAME THE HYPOTHESIS
↓
DEFINE THE MEASUREMENT
↓
BUILD A CONTROL
↓
LOOK FOR A CONFOUND
↓
BUILD A BETTER CONTROL
↓
KEEP ONLY WHAT SURVIVES
```

That is the method we are going to use from here onward.

Not:

```text
see something
↓
find a metric that supports it
↓
publish the impressive sentence
```

But:

```text
try to kill the explanation
```

and see what remains.

---

# A claim should have a failure condition

This is one of the simplest protections against self-deception.

Before running the experiment, ask:

> What result would make me stop using this claim?

Suppose our hypothesis is:

> inherited state improves later learning.

A failure condition might be:

```text
after equalizing compute,
inheriting successors do not outperform
scratch successors on held-out environments
```

Suppose our hypothesis is:

> a pattern regenerates after damage.

Failure might be:

```text
recovered morphology is no better
than matched damaged controls
```

Suppose our hypothesis is:

> local ancestry predicts motion coherence.

Failure might be:

```text
after matching spatial distance and local context,
same-ancestry pairs are no more aligned
than different-ancestry pairs
```

If no possible result can weaken the claim, we do not yet have an experiment.

---

# Bounded claims are stronger claims

This sounds backwards.

Compare:

> The system heals.

with:

> Under deletion of up to 10% of active cells in the tested regions, the system returned to at least 0.90 morphology similarity within 50 updates in 83% of trials.

The second sentence sounds less exciting.

It is much stronger.

Why?

Because we know exactly what it means.

We know:

```text
intervention
measurement
threshold
time window
scope
success rate
```

We also know what it does not mean.

A bounded claim survives scrutiny better because its edges are visible.

---

# Do not generalize past the experiment

Suppose Rule 30 from one initial state generates a visually irregular spacetime diagram.

We can say:

> Rule 30 produced this trajectory under this initial condition.

We should be cautious about:

> Rule 30 always produces complex behavior.

Suppose a glider survives one perturbation.

We can say:

> This glider survived this perturbation.

Not:

> gliders are robust.

Suppose one evolving population improves in one environment.

We can say:

> this population improved under this environment and protocol.

Not:

> evolution produces progress.

The scale of the claim should match the scale of the evidence.

---

# One example discovers; a distribution establishes

A single compelling example is often how we find something.

That is valuable.

But general claims require repeated observations.

If we care about damage tolerance, test:

```text
many damage locations
many severities
multiple phases
multiple trials
```

If we care about inheritance, test:

```text
many descendants
many generations
multiple environments
multiple lineages
```

If we care about reproduction, test:

```text
many candidate parents
many offspring events
counterfactual removals
repeatability
```

The question changes from:

```text
Can this happen?
```

to:

```text
Under what conditions does this happen?
```

That is a major scientific transition.

---

# Search can create its own illusion

Suppose we search 10,000 cellular-automaton rules.

We find one extraordinary pattern.

We show it.

It looks miraculous.

But we need to remember:

```text
10,000 attempts
↓
1 spectacular result
```

is not equivalent to:

```text
1 attempt
↓
1 spectacular result
```

Search changes the evidence.

The interesting example still matters.

But we should record:

```text
search space
selection criteria
number of attempts
how the candidate was chosen
```

Otherwise selection bias gets hidden inside the presentation.

---

# The screenshot has a provenance

Every visual in this book should be mentally accompanied by questions such as:

```text
Which run?

Which seed?

Which parameters?

Which crop?

Which timestep?

Which preprocessing?

Which selection rule?
```

The image is not raw reality.

It is the result of an experimental pipeline.

That does not make it invalid.

It means the pipeline belongs to the evidence.

A good visual should be reproducible from code.

---

# The metric can lie

Metrics are not neutral.

Suppose two mostly empty cellular grids are compared using:

```python
np.mean(a == b)
```

They may score:

```text
0.99
```

even if the actual structures are completely different.

The background dominates.

So we switch to IoU.

Better.

But perhaps translation causes equivalent moving objects to score poorly.

So we align them first.

Better.

Then perhaps rotation matters.

Or phase.

Or distributed structure.

Every metric embeds assumptions about what differences matter.

So when we choose a metric, we should ask:

> **What notion of identity does this metric assume?**

That question is going to become increasingly important.

---

# Measurement creates the object

This is subtle.

Suppose we define an entity as:

```text
one connected component
```

Our tracking algorithm now sees:

```text
component A
component B
component C
```

But perhaps A and B are actually pieces of one distributed causal process.

Or perhaps one connected component contains two causally independent organizations.

Our detector did not merely observe the world.

It imposed an ontology.

That does not mean detection is impossible.

It means entity definitions must remain provisional.

The objects we measure may eventually need to be redefined by causal structure rather than visual connectedness.

---

# Geometry is a hypothesis

For the glider, geometry worked beautifully.

A localized connected pattern had:

```text
clear boundary
stable recurrence
coherent motion
```

So treating it as one object was useful.

But we should not assume:

```text
connected geometry
=
individual
```

universally.

Future digital systems may be:

```text
distributed
fragmented
multi-scale
temporally intermittent
```

Their identity may be better defined by:

```text
causal continuity
```

than by:

```text
spatial connectedness
```

We do not yet know.

That is a question for experiments.

---

# Reproduction needs ancestry, not just similarity

Suppose two shapes look identical.

Call them:

```text
A
B
```

Did A produce B?

Similarity cannot answer that.

Temporal order cannot answer that.

Spatial proximity cannot answer that.

A stronger analysis asks whether the state associated with A contributed causally to the appearance of B.

Conceptually:

```text
A present
↓
B appears
```

versus:

```text
A counterfactually removed
↓
does B still appear?
```

If B disappears under the intervention, the parenthood hypothesis becomes stronger.

That is the direction reproduction experiments need to move.

From:

```text
shape matching
```

toward:

```text
causal lineage
```

---

# Positive counterfactual causality

For a local deterministic system, we can sometimes test causality at very small scales.

Suppose a cell is active at:

```text
t + 1
```

and several cells in its neighborhood were active at:

```text
t
```

Take one predecessor cell.

Remove it.

Recompute the update.

If the child cell now disappears, the predecessor was positively necessary for that child state under this intervention.

Conceptually:

```text
original neighborhood
↓
child = 1

remove predecessor x
↓
child = 0
```

Then:

```text
x
```

has a measurable causal contribution under this criterion.

Do this repeatedly and we can begin constructing:

```text
cell → cell
```

causal edges.

Aggregate those and we may obtain:

```text
pattern → pattern
```

relationships.

Now ancestry becomes something we can calculate rather than merely eyeball.

We will return to this later.

---

# Causality also has limits

Even counterfactual tests need care.

Suppose removing either of two cells individually leaves an outcome unchanged, but removing both prevents it.

Then neither appears individually necessary.

Yet together they matter.

Or perhaps one predecessor is sufficient but not necessary because another pathway can compensate.

Causality can involve:

```text
redundancy
synergy
multiple sufficient causes
```

So a simple cell-removal test is not a complete theory of causation.

But it is vastly stronger than:

> those shapes look related.

Again, the claim must match the method.

---

# Evidence has levels

We can make this explicit.

Suppose we claim:

> pattern P reproduces.

Evidence might progress through levels.

## Level 1 — visual similarity

```text
one P
↓
two things that look like P
```

Interesting.

Weak.

---

## Level 2 — measured similarity

```text
identity criterion satisfied
```

Better.

---

## Level 3 — persistence

```text
the second instance remains independently detectable
```

Better again.

---

## Level 4 — repeatability

```text
the process happens multiple times
```

Stronger.

---

## Level 5 — intervention

```text
removing the proposed parent changes offspring production
```

Now we have causal evidence.

---

## Level 6 — lineage

```text
offspring themselves produce descendants
```

Now reproduction forms an ancestry structure.

---

## Level 7 — inheritance

```text
measured parent differences predict descendant differences
```

Now we can discuss heritable variation.

The word did not change.

The evidence did.

---

# An evidence ledger

From this point onward, every chapter should maintain a small ledger.

Something like:

```text
WHAT WE SAW

WHAT WE MEASURED

WHAT SURVIVED THE CONTROL

WHAT DID NOT SURVIVE

WHAT WE CAN CLAIM

WHAT WE CANNOT CLAIM
```

This is deliberately repetitive.

The repetition is useful.

It prevents a spectacular result in one chapter from silently becoming a stronger claim three chapters later.

---

# Audit the book so far

Let's do that now.

---

# Rule 30

## What we saw

A tiny deterministic rule produced a visually irregular spacetime history.

## What we measured

A one-bit perturbation can create an expanding difference between trajectories.

## What survived

The irregular behavior did not require injected randomness.

## What we can claim

Simple deterministic local mechanics can generate globally nontrivial trajectories.

## What we cannot claim

We have not established life, intelligence or a general theory of complexity.

---

# The glider

## What we saw

A localized pattern appeared to move through the Game of Life lattice.

## What we measured

Its configuration recurs after four generations with a fixed translation.

Its centroid follows a systematic trajectory.

## What survived

The organizational relationship persists despite changes in constituent cells.

## What we can claim

Material continuity is not required for a useful operational notion of pattern identity in this system.

## What we cannot claim

We have not established that connected geometry is the universal boundary of a digital individual.

---

# Damage

## What we saw

Persistent structures can collapse after small perturbations.

## What we measured

Survival and structural similarity can be tracked as damage changes.

## What survived

Undisturbed persistence does not imply robustness or regeneration.

## What we can claim

Persistence, robustness and regeneration are experimentally distinct.

## What we cannot claim

A surviving pattern has not necessarily recovered.

A pattern returning visually has not necessarily demonstrated a general regenerative mechanism.

---

# Reproduction

## What we saw

Digital systems can produce additional recognizable patterns.

## What we learned

Copying alone is cheap and scientifically weak.

Similarity alone does not establish ancestry.

## What stronger evidence requires

```text
distinct entity
+
identity criterion
+
persistence
+
repeated production
+
causal dependence
```

## What we can claim

Causal reproduction is a stronger property than simple duplication.

## What we cannot claim

Two similar structures are not automatically parent and offspring.

---

# Evolution

## What we established

Heritable variation plus differential reproductive success can change populations.

## What controls matter

```text
remove variation
shuffle inheritance
neutralize selection
change environment
```

## What we can claim

Evolution can occur in deterministic digital systems.

## What we cannot claim

Evolution does not imply progress.

Novelty does not imply usefulness.

Complexity does not imply improvement.

---

# Cumulative improvement

## What we proposed

Later processes may inherit useful state from earlier ones and start from a measurable advantage.

## What would demonstrate it

```text
inherited successor
>
scratch successor
```

under:

```text
equal budget
+
related but non-identical conditions
```

across repeated generations.

## Current status

Experimental target.

Not yet established.

That distinction matters.

---

# Our words now have statuses

We should stop treating every term as either:

```text
true
```

or:

```text
false
```

A more useful vocabulary is:

```text
OBSERVED
MEASURED
SUPPORTED
PROVISIONAL
FAILED
UNTESTED
```

For example:

```text
Rule 30 irregularity
OBSERVED

perturbation spreading
MEASURED

glider translating persistence
SUPPORTED

connected geometry = individuality
PROVISIONAL

glider regeneration
FAILED under tested perturbations

cumulative heritable improvement
UNTESTED
```

That tells us much more than simply collecting nouns.

---

# Failed hypotheses belong in the book

This is important.

Suppose we see what looks like flocking.

We build a metric.

It shows strong local alignment.

We remove global expansion.

Alignment remains.

We propose that relatives move together.

Initial analysis supports it.

Then we discover a confound.

We improve the control.

The family effect disappears.

What belongs in the final chapter?

All of it.

Because the important result is not merely:

```text
family effect = no evidence
```

The important result is:

```text
visual impression
↓
measurement
↓
plausible explanation
↓
confound
↓
better control
↓
explanation rejected
```

That is exactly what scientific progress looks like.

A failed explanation can be more valuable than an unchallenged exciting claim.

---

# Do not clean the history too much

There is a temptation when writing a book to present:

```text
question
↓
correct experiment
↓
correct answer
```

as though we knew the path from the beginning.

But that hides the most useful part.

Real investigation often looks like:

```text
question
↓
bad metric
↓
better metric
↓
wrong explanation
↓
confound
↓
better control
↓
smaller claim
```

That history teaches the reader how to investigate.

Not merely what answer we eventually accepted.

So this book should preserve some of the mistakes.

Not because mistakes are virtuous.

Because corrections reveal the method.

---

# Negative results are results

Suppose we test:

> shared ancestry independently predicts local motion coherence.

After controlling for:

```text
distance
time
local density
background flow
```

the effect disappears.

That is not:

```text
nothing happened
```

It tells us:

```text
ancestry was not required
for the measured coherence
under this experiment
```

That narrows the mechanism.

Perhaps:

```text
local geometry
+
local dynamics
```

is enough.

That is knowledge.

The experiment succeeded.

The hypothesis did not.

---

# The strongest result may be smaller than the original idea

We may begin with:

> This system flocks.

After measurement we end with:

> Nearby moving structures have strongly aligned velocity.

Then after a better control:

> Local velocity coherence survives removal of global radial expansion.

Then after matching:

> We find no additional coherence attributable to shared causal ancestry.

The final statement is narrower.

It is also far more informative.

We now know something about:

```text
what the phenomenon is
```

and:

```text
what it probably is not
```

That is progress.

---

# Every claim should carry its scope

A useful habit is to imagine every sentence with hidden metadata.

For example:

```text
CLAIM:
same-family pairs move coherently

SYSTEM:
Outlier

RUN:
specified rule / seed / size / duration

MEASUREMENT:
velocity alignment

CONTROL:
distance / density / local flow matched

SCOPE:
tested observations only

RESULT:
effect not distinguishable from control
```

The published sentence may be short.

The evidence behind it should not be.

---

# Reproducibility is part of the architecture

Our experiments should leave artifacts.

At minimum:

```text
code
parameters
seed
outputs
plots
measurements
claims
```

For larger experiments:

```text
database
lineage records
event tables
cached analyses
```

The experiment should not disappear when the animation closes.

We should be able to ask later:

```text
Which run produced this figure?

Which entities contributed?

Which measurement version?

Which control?

Which threshold?
```

That makes the experiment inspectable.

---

# Store the specimen

For complicated digital-life systems, a database can become part of the experimental apparatus.

Instead of merely storing:

```text
final image
```

we can store:

```text
runs
entities
states
causal edges
lineages
measurements
analysis versions
```

Then one simulation becomes a specimen we can interrogate repeatedly.

We can ask one month later:

```text
Which descendants came from this ancestor?

Which entities moved persistently?

Which pairs were spatially close?

Which causal relationships survived?
```

without rerunning the entire world.

That changes how we can do research.

---

# But cached analysis has provenance too

If we store analysis results, we need to know:

```text
which algorithm produced them?
which parameters?
which source run?
which metric version?
```

Otherwise stale or incompatible results can silently contaminate later experiments.

A cache is useful.

A cache without identity is dangerous.

Evidence must remain traceable through the analysis stack.

---

# This is not bureaucracy

At first this can feel excessive.

Why store:

```text
run ID
analysis ID
metric version
control version
```

for a cellular automaton?

Because eventually our questions will become difficult enough that we will not remember which result came from which experiment.

And because we are using AI systems to help us write code, run experiments and interpret results.

That makes provenance more important, not less.

Fast generation creates more candidate analyses.

We therefore need stronger mechanisms for knowing which ones survived validation.

---

# AI makes this method more necessary

An AI assistant can produce:

```text
a hypothesis
a metric
a graph
an explanation
```

very quickly.

That is powerful.

It is also dangerous.

The bottleneck shifts.

The hard part is no longer:

> Can we generate a plausible experiment?

It becomes:

> **Can we distinguish the experiment that actually tests the claim from one that merely appears to?**

AI increases the rate of hypothesis generation.

Our evidence process has to increase the rate of hypothesis destruction.

---

# Use AI to attack the experiment

A useful workflow is to ask an AI system:

```text
What alternative explanation could produce this result?
```

Then:

```text
Design a control that separates those explanations.
```

Then:

```text
What does this metric accidentally condition on?
```

Then:

```text
How could this intervention contaminate the control group?
```

Then:

```text
What result would falsify the claim?
```

The assistant should not merely help us make the result impressive.

It should help us make the claim difficult to keep.

---

# The book's experimental constitution

We can now write the rules explicitly.

Whenever we encounter an interesting phenomenon:

```text
1. SEE SOMETHING

2. NAME THE HYPOTHESIS

3. DEFINE THE OBJECT OR PROPERTY

4. DEFINE THE MEASUREMENT

5. STATE WHAT RESULT WOULD COUNT

6. BUILD A CONTROL

7. RUN THE EXPERIMENT

8. LOOK FOR CONFOUNDS

9. BUILD A BETTER CONTROL IF NEEDED

10. KEEP ONLY WHAT SURVIVES

11. WRITE THE BOUNDED CLAIM

12. RECORD WHAT REMAINS UNRESOLVED
```

That is the constitution for the rest of this project.

---

# And one more rule

There is one final protection.

> **Never introduce a mechanism merely because biology has one.**

Suppose we think digital life needs:

```text
metabolism
death
reproduction
homeostasis
body
genome
```

Before implementing it, ask:

> What problem is this mechanism solving?

Then:

> Does the digital substrate actually have that problem?

If yes, build the mechanism and test it.

If no, do not import it simply because biological organisms use it.

This is where our investigation is about to change direction.

---

# We have been asking a biological question

Look at the sequence so far:

```text
persistence
robustness
regeneration
reproduction
inheritance
evolution
```

It is a sensible sequence.

But notice something.

It is also suspiciously biological.

We have been asking:

> How many properties associated with biological life can we reproduce digitally?

That question has been useful.

It got us here.

But it may now be limiting us.

Because digital systems do not live in biological matter.

---

# What if the constraints are different?

Biological organisms face constraints such as:

```text
finite bodies
slow communication
expensive copying
limited memory
material metabolism
irreversible physical damage
aging
death
```

Digital systems may face very different constraints:

```text
compute
memory
bandwidth
latency
coordination
attention
trust
energy cost of computation
```

They may also possess capabilities biology does not naturally provide:

```text
exact copying
checkpointing
restoration
forking
merging
fast communication
external memory
self-modification
distributed execution
```

If those differences matter, then simply rebuilding biology digitally may be the wrong objective.

---

# Birds are evidence, not the blueprint

Birds prove that heavier-than-air controlled flight is possible.

But an aircraft does not need:

```text
feathers
bones
muscles
a beak
```

It needs mechanisms that satisfy the actual requirements of flight.

Lift.

Control.

Propulsion.

Structural integrity.

The lesson is not:

> Ignore birds.

The lesson is:

> **Study the phenomenon, then derive the mechanism from the substrate you actually have.**

Artificial life deserves the same treatment.

Biology is evidence.

It is not automatically the specification.

---

# The question changes

We began by asking:

> What would digital life mean?

Then we borrowed biological concepts because they were the best examples we had.

That was useful.

But now we have an experimental method strong enough to ask a better question:

> **Which properties of life survive when we remove the biological constraints that produced them?**

And then:

> **What new properties become possible because the substrate is digital?**

That is where the book needs to go next.

Not toward a longer checklist.

Toward a more fundamental derivation.
