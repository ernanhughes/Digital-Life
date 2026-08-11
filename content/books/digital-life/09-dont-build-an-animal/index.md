+++
title = "Digital Life 09: Don't Build an Animal"
date = "2026-08-11T14:58:00+01:00"
draft = false
description = "Stop treating biological life as the specification. Remove biological constraints and ask what organization actually requires in a digital substrate."
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Digital Substrate", "Life", "Computation", "Experimental Method"]
+++

We almost made a serious mistake.

After seven chapters of experiments, it would be very easy to write down a list like this:

```text
boundary
resources
self-maintenance
damage tolerance
regeneration
memory
reproduction
inheritance
variation
selection
learning
finite lifetime
lineage
evolution
````

Then say:

> Build all of those and we will have digital life.

It sounds rigorous.

We could turn every property into a test.

We could build a large simulation.

We could create:

```python
class Organism:
    ...
```

and give it:

```python
energy
memory
genome
age
children
```

Then we could spend the rest of the book filling in the methods.

That would be a beautifully engineered mistake.

Because we would have quietly assumed the answer before doing the experiment.

We would not be discovering digital life.

We would be constructing a digital imitation of an animal.

---

# Biology is one implementation

Biological life is enormously important evidence.

It proves that matter can organize itself into systems capable of:

```text
persistence
adaptation
learning
reproduction
evolution
complex behavior
```

But biology is also constrained by its substrate.

Biological organisms are made from physical matter operating under particular limitations.

They face:

```text
finite bodies
material wear
slow growth
expensive copying
limited communication
local memory
physical transport
irreversible damage
aging
death
```

Many familiar biological mechanisms may be solutions to those constraints.

That distinction matters.

A mechanism can be:

```text
essential to biological life
```

without being:

```text
essential to organized life in every possible substrate
```

We need to find out which is which.

---

# Birds are not the aircraft specification

For a long time, birds were the clearest evidence that controlled heavier-than-air flight was possible.

Studying birds was useful.

Wings mattered.

Airflow mattered.

Control mattered.

But an aircraft did not ultimately need to recreate:

```text
feathers
hollow bones
muscle
a beak
a bird's metabolism
```

The engineering problem was not:

> How do we manufacture a mechanical bird?

It was:

> **What principles actually make controlled flight possible?**

Lift.

Control.

Propulsion.

Stability.

Structure.

The substrate changed the implementation.

That is the attitude we need here.

> **We are not building a bird. We are trying to discover the aerodynamics of digital life.**

Biological organisms are evidence that the phenomenon is possible.

They are not automatically the complete engineering specification.

---

# So invert the method

Instead of asking:

> Which biological properties should we add next?

ask:

> **Which apparently necessary biological properties can we remove?**

This gives us a new experimental procedure.

```text
IDENTIFY A SUPPOSED PROPERTY OF LIFE
            ↓
ASK WHY BIOLOGY NEEDS IT
            ↓
ASK WHETHER THE DIGITAL SUBSTRATE
HAS THE SAME CONSTRAINT
            ↓
REMOVE THE PROPERTY
            ↓
BUILD THE SIMPLEST SYSTEM WITHOUT IT
            ↓
OBSERVE WHAT BREAKS
            ↓
REINTRODUCE ONLY WHAT BECOMES NECESSARY
```

That is a much more interesting experiment.

The rule is:

> **Never import a biological constraint unless the digital substrate actually requires it.**

---

# Start with reproduction

Reproduction seems like one of the safest requirements.

Almost every discussion of life includes it somewhere.

But why does biology reproduce?

There are many reasons.

One unavoidable one is that individual biological organisms do not continue indefinitely.

Bodies:

```text
accumulate damage
age
lose function
die
```

So if biological organization is to continue beyond one body, information must pass into another body.

Conceptually:

```text
individual
    ↓
finite lifetime
    ↓
reproduction
    ↓
successor
```

Now remove the finite lifetime.

Suppose a digital entity can continue operating.

And continue growing.

And repair damaged state.

And move between machines.

And replace failing hardware underneath itself.

Does it still need to reproduce?

Maybe.

But the answer is no longer obvious.

---

# What if it just keeps growing?

Imagine a digital organization beginning with:

```text
1 unit
```

Then:

```text
2
4
8
16
32
64
...
```

Not copies.

One continuing organization.

Its memory expands.

Its computational capacity expands.

Its internal structure becomes richer.

Its physical execution may become distributed across many machines.

At what point do we say it must create offspring?

Why?

Biology cannot generally grow one organism without limit.

A digital system may face very different limits.

So reproduction might be:

```text
one useful strategy
```

rather than:

```text
a fundamental requirement
```

That is an experimental question now.

---

# Copying is suspiciously cheap

There is another problem.

Digital copying is trivial.

```python
copy = original.copy()
```

Files duplicate.

Processes fork.

Virtual machines clone.

Model weights copy.

Memory snapshots replicate.

If reproduction is defined too loosely, computers have been reproducing for decades.

So digital life may make copying *less* interesting rather than more.

The important question may shift from:

```text
Can it reproduce?
```

to:

```text
Why would it reproduce?
```

What problem does reproduction solve?

Does it:

```text
create independent search branches?
provide fault tolerance?
explore alternatives?
distribute computation?
preserve state?
enable competition?
```

Now reproduction becomes a mechanism with a purpose rather than a checkbox inherited from biology.

---

# Forking is stranger than reproduction

Suppose one digital entity reaches state:

```text
S
```

Then executes:

```text
fork()
```

Now:

```text
S₁
S₂
```

Both possess the entire history up to the fork.

Which one is the parent?

Which one is the child?

Are they twins?

Are both continuations of the original?

Did the original die?

Nothing like this maps cleanly onto ordinary biological reproduction.

The ancestry may look like:

```text
        S
       / \
     S₁   S₂
```

But both branches contain the original's memories.

The notion:

```text
parent creates a new organism
```

has become less obvious.

Perhaps the better description is:

> **one process acquired two continuations**

That is a fundamentally digital possibility.

---

# Now let the branches merge

It gets worse.

Suppose:

```text
S
├── S₁
└── S₂
```

The two branches explore different environments.

`S₁` learns:

```text
A
```

`S₂` learns:

```text
B
```

Later they exchange state and construct:

```text
S₃ = merge(S₁, S₂)
```

Now ancestry is no longer a tree.

```text
      S
     / \
   S₁   S₂
     \ /
      S₃
```

Biological language begins to struggle.

Who are `S₃`'s parents?

Both?

Did two organisms combine?

Did one distributed organism temporarily split and reunite?

The right answer may depend on the mechanism.

But one thing is already clear:

> **Digital lineage may naturally be a graph rather than a tree.**

That possibility should change how we think about inheritance.

---

# Acquired state can be inherited directly

Biological inheritance usually separates much of what an organism learns during life from what its descendants inherit.

A mouse can learn a maze.

Its offspring do not normally receive the memory of that maze.

Digital systems do not have to work this way.

Suppose an entity begins with:

```text
knowledge = K
```

During operation it discovers:

```text
A
B
C
```

Its state becomes:

```text
K + A + B + C
```

Now it forks.

Both successors can receive:

```text
K + A + B + C
```

The distinction between:

```text
learning
```

and:

```text
inheritance
```

has changed.

Acquired information can become inherited information almost automatically.

That could radically alter evolutionary dynamics.

---

# Lamarck gets cheap

In biology, inheritance of acquired characteristics is heavily constrained.

Digitally:

```python
child.state = parent.state
```

makes it trivial.

But again, trivial implementation does not mean trivial consequence.

If every acquired state passes forward, the descendants may inherit:

```text
useful discoveries
+
mistakes
+
noise
+
obsolete assumptions
+
huge amounts of irrelevant history
```

So the difficult problem becomes different.

Not:

> How do we transmit acquired information?

But:

> **What should survive?**

The scarce resource may be selection.

Compression.

Retrieval.

Integration.

Not copying.

---

# Memory may not be scarce

Biological organisms have severe memory limits.

Brains are finite.

Retrieval is imperfect.

Communication between brains is slow.

A digital entity can potentially access:

```text
gigabytes
terabytes
petabytes
external databases
search engines
vector stores
other agents
```

So does digital life need internal memory in the same sense?

Perhaps not.

Maybe the important distinction becomes:

```text
information exists
```

versus:

```text
information can be retrieved
```

versus:

```text
information can be integrated
```

versus:

```text
information can change behavior
```

An entity with access to the entire internet is not omniscient.

Access is not understanding.

Storage is not memory in the functional sense we care about.

So scarcity may move from:

```text
memory capacity
```

to:

```text
attention
retrieval
context
integration
verification
```

Again, the substrate changes the problem.

---

# Death becomes questionable

Our previous design deliberately introduced finite lifetime.

That made lineage experiments neat.

```text
birth
↓
life
↓
reproduction
↓
death
```

But why should a digital entity die?

Biological death can result from:

```text
irreversible damage
aging
resource failure
predation
disease
```

Digital state may support:

```text
checkpoint
restore
replication
migration
redundancy
error correction
```

Suppose the hardware running a process fails.

The process restores from a checkpoint elsewhere.

Did the organism die?

Suppose ten machines execute parts of one system and one fails.

Did the system suffer an injury?

Suppose every physical machine is replaced gradually while the computation continues.

Where exactly would death occur?

The biological concept may need substantial revision.

---

# Checkpointing changes identity

Imagine:

```text
t = 100
save checkpoint C
```

The entity continues to:

```text
t = 200
```

Then something catastrophic happens.

We restore:

```text
C
```

Now the system continues again from `t = 100`.

Is this:

```text
the same entity restored?
```

or:

```text
a new entity copied from an earlier one?
```

That is not merely philosophy.

It affects lineage tracking.

Suppose both versions exist.

```text
original continuation
checkpoint continuation
```

Now one past state has generated multiple futures.

Digital identity may have branching time built directly into it.

---

# The body may be optional

Biological organisms have bodies.

The boundary between organism and environment is often spatially meaningful.

But imagine a digital process distributed across:

```text
machine A
machine B
database C
model server D
memory store E
```

Which pixels belong to the organism?

Which machine contains it?

There may be no single connected geometry.

Its boundary might instead be defined by:

```text
causal dependence
authorization
state ownership
information flow
control
shared objective
```

This connects directly to the warning from Chapter 04.

We initially used geometry to define an entity.

That worked for a glider.

But digital individuality may not be geometric at all.

---

# A mushroom may be a better analogy than an animal

Animals encourage us to think:

```text
one body
one boundary
one location
one lifetime
```

But even biology contains other architectures.

Consider a fungal network.

Much of the system is distributed.

Growth can extend through an environment.

The visible mushroom is only one manifestation of a larger organization.

This does not mean digital life should imitate fungi either.

The point is that even biology warns us against treating:

```text
animal
```

as synonymous with:

```text
life
```

Our conceptual search space should be wider.

---

# What about a crystal?

Now push the reduction further.

Consider a crystal growing from a seed.

A simple local process can produce:

```text
organized growth
repetition
spatial structure
defects
continued expansion
```

Suppose we build a hexagonal digital growth system.

Start with:

```text
one seed
```

Allow local growth.

No resource limit initially.

No reproduction.

No metabolism.

No genome.

No finite lifetime.

Just:

```text
seed
+
local rule
+
growth
+
time
```

What properties appear?

Can growth continue indefinitely?

What happens after damage?

Does the structure fill a hole?

If so, is that repair?

Or merely continued growth?

Can defects encode history?

Can different growth fronts interact?

Could the entire history of the system become embedded in its geometry?

These are better questions than:

> Is a crystal alive?

---

# Repair versus growth

This distinction becomes important immediately.

Suppose a growing structure contains a hole.

Later the hole disappears.

Did the system repair itself?

Maybe.

But perhaps growth simply continued into empty space.

Those are different mechanisms.

A real regeneration claim might require:

```text
target organization exists
↓
damage moves it away from target
↓
dynamics preferentially return toward target
```

Whereas simple growth might be:

```text
empty location
↓
local growth rule activates
↓
location fills
```

No target morphology exists.

So:

> **repair by continued growth is not necessarily repair toward a target organization**

That difference deserves an experiment.

---

# Growth itself may be underestimated

Biology usually gives us a familiar lifecycle:

```text
birth
↓
growth
↓
maturity
↓
reproduction
↓
death
```

Digital organization might instead do:

```text
begin
↓
grow
↓
grow
↓
grow
↓
restructure
↓
grow
↓
split temporarily
↓
merge
↓
grow
...
```

Perhaps there is no mature size.

Perhaps no adulthood.

Perhaps no reproductive stage.

Perhaps expansion and reorganization are the fundamental dynamics.

If so, biological lifecycle vocabulary would actively mislead us.

---

# Self-modification changes evolution

Biological organisms cannot usually redesign their own inherited machinery deliberately during life.

Digital systems can.

Imagine:

```text
system
↓
observes its own performance
↓
modifies its update rule
↓
tests modification
↓
keeps or rejects it
```

Now adaptation can happen:

```text
within one continuing entity
```

without waiting for:

```text
variation across offspring
+
selection across generations
```

Does that make evolution unnecessary?

Not necessarily.

Population search may still be useful.

But once again:

> **a biological mechanism may become one option among several digital mechanisms.**

---

# Evolution may become deliberate

Consider ordinary Darwinian search:

```text
variation
↓
selection
↓
inheritance
↓
repeat
```

Now compare:

```text
generate candidate self-modifications
↓
simulate or test them
↓
evaluate consequences
↓
adopt useful modification
```

Both explore alternatives.

But one operates through populations and generations.

The other operates through internal model-based search.

A sufficiently capable digital entity might combine them:

```text
self-modification
+
forked experiments
+
population search
+
shared memory
+
merging
```

That is not biological evolution reproduced digitally.

It is something else.

---

# Scarcity does not disappear

None of this means digital systems are unconstrained.

They are.

But the scarce things may change.

Instead of:

```text
food
water
oxygen
body mass
```

a digital entity might face:

```text
compute
memory
bandwidth
latency
energy
storage
attention
context
trust
verification
coordination
```

Those constraints can produce entirely different organizational pressures.

For example:

```text
unlimited stored information
+
limited attention
```

creates a very different problem from:

```text
limited biological memory
```

Likewise:

```text
cheap copying
+
expensive synchronization
```

may make branching easy and merging difficult.

That could shape digital organization profoundly.

---

# Communication changes individuality

Biological organisms communicate.

But communication is relatively slow and low-bandwidth compared with internal neural activity.

Digital systems might exchange rich internal state directly.

Suppose two entities can transfer:

```text
memories
models
strategies
verified discoveries
internal representations
```

What does individuality mean then?

If two agents synchronize every second, are they really two independent individuals?

If they share almost all memory but act separately, are they one distributed entity?

If synchronization stops, when do they become two?

Digital individuality may exist on a continuum.

That is another reason not to begin with an assumed membrane.

---

# Information access is not assimilation

There is also a tempting mistake in the other direction.

Because digital systems can access enormous external information stores, we might imagine they no longer need learning.

But:

```text
available information
```

is not:

```text
usable knowledge
```

A system may have access to:

```text
every scientific paper
```

while lacking the ability to:

```text
retrieve the relevant one
evaluate its reliability
connect it to the present problem
integrate it with existing models
act on it correctly
```

So learning may still matter enormously.

But perhaps digital learning is less about storing facts and more about:

```text
organizing
compressing
indexing
validating
connecting
```

information.

Again, the property survives while the mechanism changes.

---

# What should actually be fundamental?

We can now start stripping the old list.

Do we require:

```text
reproduction?
```

Unknown.

```text
finite lifetime?
```

Probably not universally.

```text
physical boundary?
```

Probably not.

```text
genome?
```

Unknown.

```text
metabolism?
```

Only if translated into whatever resource-management problem the substrate actually imposes.

```text
individuality?
```

Possibly useful, but perhaps causal rather than geometric.

```text
persistence?
```

Probably important if we want to discuss one continuing organization.

```text
adaptation?
```

Potentially important, but may occur within one entity, across a lineage, or across a network.

```text
memory?
```

Some form of history-dependent state seems important for learning, but it may be external or distributed.

The list is getting shorter.

And stranger.

Good.

---

# Perhaps the core is organization under constraint

Try a different starting point.

Instead of:

```text
life =
boundary
+
metabolism
+
reproduction
+
...
```

start with:

```text
organized state
+
continued interaction
+
constraints
+
history
```

Then ask what mechanisms become necessary for that organization to:

```text
persist
grow
adapt
explore
recover
accumulate useful change
```

This does not define life.

It gives us a smaller experimental starting point.

---

# The digital substrate offers new primitives

Biology gives us primitives such as:

```text
cells
chemical gradients
membranes
genes
protein synthesis
```

Digital systems offer very different ones:

```text
copy
fork
merge
checkpoint
restore
message
cache
search
execute
rewrite
compress
verify
```

Perhaps digital life should be built from those.

Not because computer-science terminology is somehow superior.

Because those operations are native capabilities of the substrate.

The equivalent of discovering aerodynamics may require us to understand which of these primitives support stable adaptive organization.

---

# A different life cycle

A digital entity might therefore have a lifecycle like:

```text
START
↓
OBSERVE
↓
ACT
↓
LEARN
↓
EXPAND
↓
FORK
├───────────────┐
↓               ↓
EXPLORE A       EXPLORE B
↓               ↓
VERIFY          VERIFY
└───────┬───────┘
        ↓
      MERGE
        ↓
     REWRITE
        ↓
     CONTINUE
```

No birth.

No childhood.

No adulthood.

No mandatory reproduction.

No mandatory death.

Yet potentially:

```text
history
adaptation
variation
selection
accumulation
persistence
```

That deserves investigation.

---

# Or perhaps it does reproduce

We should not overcorrect.

Maybe experiments reveal that reproduction really is fundamental.

Perhaps one continuing entity gets trapped in local optima.

Forking into independent successors might be necessary for useful search.

Perhaps merge conflicts become too severe.

Perhaps distributed individuality becomes unstable.

Perhaps bounded lifetimes are necessary to prevent state accumulation.

Perhaps some analogue of death turns out to be computationally useful.

Excellent.

Then we reintroduce those mechanisms.

But now we have earned them.

The method is:

```text
remove
↓
observe failure
↓
identify missing function
↓
reintroduce minimal mechanism
↓
test again
```

Not:

```text
biology has it
↓
therefore add it
```

---

# Constraints before names

Suppose we want something metabolism-like.

Don't begin with:

```python
class Metabolism:
    ...
```

Begin with a constraint:

```text
continued operation consumes finite compute
```

Now ask:

> What mechanism allows the system to obtain enough compute to continue?

Perhaps something metabolism-like emerges as a useful description.

Or perhaps the digital mechanism looks nothing like metabolism.

Likewise, instead of:

```text
reproduction
```

begin with:

```text
parallel exploration is advantageous
```

Then see whether copying, forking or some completely different mechanism solves it.

Instead of:

```text
death
```

begin with:

```text
unbounded state accumulation becomes harmful
```

Then discover whether deletion, compression, replacement, restart or lineage turnover solves the problem.

The constraint should come before the biological name.

---

# This changes our engineering strategy

The old strategy would have been:

```text
SPECIFY DIGITAL ORGANISM
↓
implement boundary
↓
implement resource system
↓
implement metabolism
↓
implement memory
↓
implement reproduction
↓
implement death
↓
implement evolution
```

The new strategy is:

```text
START WITH MINIMAL DIGITAL ORGANIZATION
↓
INTRODUCE REAL CONSTRAINT
↓
OBSERVE FAILURE
↓
ADD MINIMAL MECHANISM
↓
TEST
↓
INTRODUCE NEXT CONSTRAINT
↓
OBSERVE FAILURE
↓
ADD MINIMAL MECHANISM
↓
TEST
```

This is a much better way to discover what is actually necessary.

---

# The experiment now runs in both directions

Earlier, our method was:

```text
SEE A PROPERTY
↓
TEST WHETHER IT IS REAL
```

Now we can also use:

```text
REMOVE A SUPPOSED REQUIREMENT
↓
TEST WHETHER IT WAS NECESSARY
```

Those are complementary.

One attacks positive claims.

The other attacks assumptions.

Together:

```text
OBSERVE
↓
TEST CLAIM
↓
REMOVE ASSUMPTION
↓
TEST NECESSITY
```

That is the new experimental engine of the book.

---

# Start at the border

So where should we go next?

Not immediately to:

```text
digital animal
```

Start nearer the border between obvious non-life and obvious life.

Things such as:

```text
crystals
growth fronts
fungal networks
cellular patterns
self-organizing structures
```

Take one property at a time.

Strip away biological assumptions.

See what remains.

For example:

```text
one seed
+
hexagonal lattice
+
local growth
+
time
```

No reproduction.

No metabolism.

No memory variable.

No programmed repair.

Then damage it.

Interrupt it.

Add obstacles.

Give it finite resources later.

Let competing growth fronts meet.

Measure what happens.

Perhaps the simplest digital-life experiment is not an animal.

Perhaps it is a crystal.

---

# The old question and the new question

The old question was:

> **Can we build software that has enough biological properties to deserve the word life?**

That question got us surprisingly far.

But it contains a hidden assumption.

The new question is:

> **What forms of persistent, adaptive, cumulative organization become possible when the substrate itself is digital?**

That is broader.

And harder.

Because we can no longer copy the answer from biology.

We have to discover it.
