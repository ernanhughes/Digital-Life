+++
title = "Digital Life 09: Properties of Digital Life"
date = "2026-08-11T10:36:00+01:00"
draft = false
description = "If digital life does not inhabit the same world as biological life, why should it inherit the same limits?"
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Artificial Life", "Digital Organisms", "Information", "Growth", "Computation"]
+++

# Digital Life 09: Properties of Digital Life

We have made a mistake.

Not in the experiments.

In the question.

We have spent several chapters asking how much of life we can reproduce in software.

Persistence.

Boundaries.

Repair.

Reproduction.

Inheritance.

Evolution.

All useful.

But there is a hidden assumption underneath that entire list:

> **that digital life should resemble biological life.**

Why?

A biological organism exists inside a particular physical universe.

It is made from matter.

It requires energy.

It occupies physical space.

Signals take time to move through it.

Its components decay.

It cannot copy itself perfectly.

It cannot instantly inspect every part of itself.

It cannot download another organism's experience.

It cannot casually become a billion times larger.

Its architecture is shaped by those constraints.

A digital organism would inhabit a different world.

So before we build one, we should ask:

> **What properties would life naturally have if its substrate were computation rather than biology?**

That is a very different question.

---

# Life as it could be

Artificial Life has always contained this broader ambition.

The field is not restricted to recreating known biological organisms.

One of its foundational ideas is to study:

> life as it could be

rather than only:

> life as we know it.

That distinction matters here.

We are not attempting to create:

```text
biology
↓
translated into Python
```

We are trying to discover:

```text
computation
↓
organization
↓
persistence
↓
something that deserves investigation as digital life
```

The difference is enormous.

---

# Do not import the constraints

Imagine attempting to invent aviation by copying birds perfectly.

You might conclude that an aircraft requires:

```text
feathers
flapping wings
hollow bones
muscles
```

But those are partly consequences of how biological flight was achieved.

They are not the fundamental requirements for flight.

The important property is:

```text
controlled movement through air
```

Aircraft achieve it differently.

Digital life may have the same relationship to biological life.

We should therefore distinguish:

```text
properties fundamental to life
```

from:

```text
properties that happen to be solutions
used by terrestrial biology
```

We don't yet know which is which.

That is what we are going to investigate.

---

# The bird trap

There is a useful historical analogy here.

For a very long time, humans looked at birds and concluded:

> If we want to fly, we should build something bird-like.

So attempts at flight often focused on features such as:

```text
wings
flapping
feathers
bird-like motion
```

That makes intuitive sense.

Birds fly.

Therefore:

```text
copy bird
↓
get flight
```

But that confuses:

```text
one biological implementation of flight
```

with:

```text
the underlying requirements for flight
```

The breakthrough came when aircraft design stopped requiring machines to be artificial birds.

The important questions became things like:

```text
How is lift generated?

How much drag is produced?

How is thrust generated?

How is stability maintained?

How is the vehicle controlled?
```

Once those properties were understood, an aircraft no longer needed to resemble a bird very closely.

It needed to satisfy the physics of flight.

That distinction matters enormously for what we are doing here.

---

# We may be making the same mistake with life

We look at biological organisms and see:

```text
metabolism
food
energy
bodies
growth
reproduction
DNA
aging
death
```

Then we assume a digital life form must have digital versions of all of them.

So we invent:

```python
energy = 100
age = 0
health = 1.0
genome = ...
```

Then:

```python
def eat():
    ...

def reproduce():
    ...

def die():
    ...
```

And eventually we announce that we have created artificial life.

But this may be the equivalent of attaching feathers to a machine.

We have copied the **visible solution** rather than identifying the **underlying problem**.

Biological organisms need metabolism because their continued organization depends on physical processes that require energy and material.

That does not automatically mean a digital organism needs a variable called:

```text
energy
```

Biological organisms reproduce because individual bodies are finite, vulnerable and eventually disappear.

That does not automatically mean digital life needs parent-child reproduction.

Biological organisms have genomes partly because information must survive through a physical reproduction process.

That does not automatically mean digital inheritance should work the same way.

The biological mechanisms may be solutions to biological constraints.

They are not necessarily the definition of life itself.

---

# We need the aerodynamics of life

That suggests a better goal.

Do not build a digital bird.

Find the equivalent of:

```text
lift
drag
thrust
control
```

for life.

What are the underlying properties that make persistent living organization possible?

Perhaps they include things such as:

```text
continued organization

response to change

retention of useful information

ability to modify itself

ability to recover from disruption

ability to exploit information in the environment

ability to persist across changes in substrate

ability to improve rather than repeatedly restart
```

We don't know yet.

That is the experiment.

The mistake would be deciding in advance that the answer must look like:

```text
cell
+
metabolism
+
DNA
+
reproduction
+
death
```

just because that is how terrestrial biology solved the problem.

---

# Airplanes do not fail for lacking feathers

An aircraft is not a bad bird.

It is a different implementation of flight.

It can do things birds cannot do.

It can:

```text
carry hundreds of people

cross oceans at enormous speed

fly at extreme altitude

carry loads far beyond biological capability
```

And it also lacks capabilities birds possess.

It does not hatch.

It does not heal itself.

It does not forage.

It does not reproduce.

Those differences do not make it less successful at flight.

They show that once a capability is separated from one particular biological implementation, a completely different design space becomes available.

Digital life may be the same.

A digital organism might fail almost every superficial biological comparison while possessing capabilities biological organisms cannot approach:

```text
perfect cloning

massive growth

direct information transfer

external knowledge access

checkpoint and restore

distributed existence

branching and merging identity

deliberate self-modification
```

If those properties arise naturally from the computational substrate, forcing the system back into a biological mold would be a mistake.

---

# Don't build a bird

So this becomes another rule for Special Creation:

> **Do not copy the biological implementation until we know the digital system actually needs it.**

Start from the property.

Then discover the mechanism.

```text
property
↓
digital constraints
↓
minimal mechanism
↓
experiment
↓
evidence
```

Not:

```text
biology has X
↓
software gets X
```

We are not building a bird.

We are trying to discover the aerodynamics of digital life.

---

# Start at the end

Instead of beginning with a primitive simulated cell and slowly adding biological features, let's do something more provocative.

Imagine a highly developed digital life form.

What might it be capable of?

Not because biology can do these things.

Because computation can.

Perhaps it can:

```text
grow almost without practical limit

copy information perfectly

copy itself

inspect itself

rewrite itself

communicate at enormous speed

access external information

understand and integrate external information

merge information from other entities

split into multiple processes

run multiple versions of itself

restore earlier states

retain effectively perfect historical records

move between machines

exist simultaneously in multiple places

compress what it has learned

give that knowledge directly to successors
```

Some of those capabilities are trivial for software.

Some remain extraordinarily difficult.

That distinction is exactly what interests us.

---

# Growth may be fundamentally different

Biological organisms cannot grow indefinitely.

There are good physical reasons.

A larger body needs more:

```text
energy
material
transport
structural support
heat dissipation
```

Geometry creates further problems.

Volume and surface area do not scale together.

Signals must travel larger distances.

Resources must be transported.

Mechanical loads increase.

Eventually architecture must change.

Digital growth is different.

Suppose our digital organism consists of cells in a computational grid.

Start with:

```text
1 cell
```

Then:

```text
10
```

Then:

```text
1,000
```

Then:

```text
1,000,000
```

There is eventually a resource cost.

Of course.

Computers are physical machines.

Memory is finite.

Compute is finite.

Storage is finite.

But the relevant scale may be radically different.

A digital entity could increase its logical size by orders of magnitude before encountering anything resembling the constraints experienced by a biological organism.

So perhaps:

> **growth is a much cheaper strategy digitally than biologically.**

That alone could alter what digital life looks like.

---

# Perhaps it never needs offspring

Consider a biological organism.

It grows.

Eventually growth stops.

It ages.

It dies.

If its lineage is to continue:

```text
parent
↓
offspring
```

Reproduction is essential.

But suppose a digital entity can simply continue expanding.

```text
seed
↓
larger structure
↓
larger structure
↓
larger structure
↓
larger structure
↓
...
```

Why reproduce?

Perhaps it doesn't.

Perhaps digital persistence is based on:

```text
continuation
```

rather than:

```text
replacement by descendants
```

This would challenge one of the assumptions we have been carrying since the beginning of the book.

Reproduction may not be fundamental to digital life at all.

It may merely be one available strategy.

---

# Copying is different too

Biological copying is extraordinarily difficult.

DNA replication is impressive precisely because molecules must reproduce information inside a noisy physical environment.

Errors matter.

Repair matters.

Mutation matters.

A digital bit can be copied:

```python
b = a
```

A million bits can be copied with extremely high fidelity.

A gigabyte can be copied.

A model can be copied.

A complete process image can potentially be checkpointed.

This means **information inheritance may be nearly trivial** relative to biology.

That creates another inversion.

In biology:

```text
copying information
=
hard
```

Digitally:

```text
copying information
=
often easy
```

The hard question becomes:

> **What should be copied?**

---

# Perfect inheritance may be a problem

Imagine an entity experiences one billion events.

It records all of them.

Its successor receives all one billion records.

Then another billion.

Then another.

Nothing is forgotten.

Is that superior?

Not necessarily.

Soon the entity has:

```text
perfect memory
+
unmanageable information
```

So digital life may face a constraint biology encounters in a different form:

```text
selection of useful information
```

The scarce resource may not be storage.

It may be:

```text
attention
retrieval
interpretation
integration
```

This is important.

A digital entity might be capable of remembering almost everything while still being unable to **use** what it remembers.

---

# Access to information

Here we reach something genuinely alien.

A bacterium cannot read Wikipedia.

A mushroom cannot inspect a scientific paper.

A tree cannot query a database.

A digital entity potentially can.

Imagine our entity encounters a problem.

Instead of learning exclusively from direct interaction with its environment, it could access:

```text
documents
databases
models
code
logs
other entities
historical experiments
scientific knowledge
```

That fundamentally changes adaptation.

Biological life mostly learns through:

```text
genetic inheritance
+
individual experience
+
in some species, social learning
```

Digital life could potentially inherit or retrieve enormous external knowledge stores directly.

---

# Access is not understanding

But being able to read information is not enough.

A hard drive has access to information in one trivial sense.

That does not mean it understands it.

Our stronger digital-life property would be:

> **Can the entity turn external information into useful changes in its own behavior?**

Conceptually:

```text
external information
        ↓
interpretation
        ↓
internal representation
        ↓
changed action
        ↓
improved outcome
```

That gives us another property worth testing.

Not merely:

```text
information access
```

but:

```text
information assimilation
```

---

# Understanding can itself be inherited

Now imagine an individual solves a difficult problem.

It doesn't merely record:

```text
answer = 42
```

It constructs a useful model.

Its successor receives that model.

The successor does not need to repeat the original learning process.

This creates a digital possibility far stronger than simple genetic inheritance:

```text
experience
↓
understanding
↓
compressed representation
↓
direct transmission
↓
successor begins with understanding
```

Biological culture already demonstrates that something vaguely analogous is possible.

Humans do not rediscover calculus every generation.

We inherit knowledge culturally.

Digital systems could push this enormously further.

---

# Cloning is almost embarrassingly easy

Suppose an entity reaches useful internal state:

```text
S
```

A biological organism cannot normally produce:

```text
S
S
S
S
S
S
```

six mature identical versions of itself instantly.

A digital entity potentially can.

So perhaps digital life has a natural operation:

```text
fork
```

One entity becomes:

```text
A₀
├── A₁
├── A₂
├── A₃
└── A₄
```

Each copy explores something different.

Later they might compare results.

This is unlike ordinary biological reproduction.

The copies could begin with the **entire acquired state** of the original.

Not merely inherited developmental instructions.

---

# And the copies could merge again

This may be even stranger.

Biological lineages branch:

```text
A
├── B
│   ├── D
│   └── E
└── C
    ├── F
    └── G
```

Information mostly moves downward.

But digital entities could potentially do:

```text
      A
   ↙  ↓  ↘
  B   C   D
   ↘  ↓  ↙
      E
```

Split.

Explore.

Merge discoveries.

That changes the meaning of lineage.

Perhaps digital evolution should not be represented as a tree.

Perhaps it is a graph.

---

# Identity becomes strange

Suppose I clone an entity.

Both copies contain identical:

```text
memory
knowledge
internal models
goals
history
```

For one instant they are indistinguishable.

Then their experiences diverge.

Which one is the original?

Maybe the question is meaningless.

Perhaps digital identity naturally looks like:

```text
shared history
↓
branching histories
```

rather than persistent individuality.

That suggests that individuality—so central to biological thinking—may itself be optional.

---

# Digital bodies can move

A biological organism is strongly tied to its material body.

A digital entity could potentially move between physical hosts while maintaining logical continuity.

Conceptually:

```text
machine A
    ↓
serialize
    ↓
transfer
    ↓
machine B
    ↓
continue
```

Did the entity move?

Did it die and get recreated?

Does that distinction matter?

Again, digital existence challenges biological intuitions.

---

# It could exist in more than one place

Go further.

Suppose the same state continues simultaneously on:

```text
machine A
machine B
machine C
```

Is that:

```text
one distributed individual
```

or:

```text
three individuals
```

?

Biology gives us some distributed organisms and colonies, but computation makes the problem much sharper.

Physical location may not define individuality.

---

# Death may be optional

If state can be:

```text
checkpointed
copied
distributed
restored
```

what does death mean?

Perhaps:

```text
process terminated
```

is not death if its state survives elsewhere.

Perhaps death requires:

```text
irreversible loss of information necessary
to continue the organization
```

That is a much more digital definition.

Again, we should not decide yet.

We should experiment.

---

# Mutation may be deliberate

Biological mutation is generally not an organism deliberately editing its genome because it predicts a better version.

Digital entities might do exactly that.

They could inspect themselves.

Construct candidate modifications.

Run copies.

Measure performance.

Keep improvements.

```text
current self
    ↓
generate variants
    ↓
run variants
    ↓
measure
    ↓
retain useful change
```

At that point the distinction between:

```text
learning
```

and:

```text
evolution
```

starts becoming blurry.

Digital life may be capable of participating directly in its own modification.

---

# Evolution could become engineering

This is potentially one of the largest differences.

Biological evolution largely operates through:

```text
variation
+
selection
+
inheritance
```

without foresight.

A sufficiently capable digital entity might operate through:

```text
model
+
hypothesis
+
simulation
+
modification
+
verification
```

It could still evolve.

But some evolutionary change would become intentional.

The entity might be both:

```text
organism
```

and:

```text
designer of future organisms
```

including itself.

---

# So what belongs on our list?

We can now create a provisional table.

| Biological constraint/property     | Digital possibility                         |
| ---------------------------------- | ------------------------------------------- |
| Finite growth                      | Potentially enormous continued growth       |
| Expensive replication              | Cheap copying                               |
| Limited acquired-state inheritance | Direct state/knowledge transfer             |
| Slow communication                 | Extremely fast communication                |
| Local sensory information          | Access to enormous external information     |
| Learning from experience           | Learning from experience + stored knowledge |
| Branching lineage                  | Branching and merging lineage               |
| Individual body                    | Distributed or movable embodiment           |
| Irreversible death                 | Checkpoint, restore, duplication            |
| Mostly blind mutation              | Deliberate self-modification possible       |
| Generational evolution             | Potentially continuous self-improvement     |
| Memory constrained by biology      | Vast persistent external memory             |
| Knowledge transfer costly          | Near-perfect copying of representations     |

This is not yet a definition of digital life.

It is a list of **differences worth investigating**.

---

# Some biological properties may survive

We should not swing too far in the opposite direction.

Some things biology does may turn out to be fundamental even digitally.

Perhaps every sufficiently persistent digital entity still needs:

```text
a boundary
```

Perhaps it needs:

```text
error correction
```

Perhaps competition for:

```text
compute
memory
bandwidth
attention
```

eventually creates scarcity.

Perhaps unlimited growth destabilizes the structure.

Perhaps copying everything creates informational collapse.

Perhaps individuality emerges because fully shared state becomes too expensive.

Perhaps death becomes useful because stale structures consume resources.

We do not know.

That's why we are building experiments.

---

# Scarcity may simply move

This is especially important.

Saying:

> resources don't matter digitally

is probably too strong.

A better hypothesis is:

> **the scarce resources may be different, and scarcity may appear at radically different scales.**

Perhaps storage is abundant.

But computation is scarce.

Perhaps computation is abundant.

But serial decision time is scarce.

Perhaps bandwidth is abundant.

But attention is scarce.

Perhaps information is abundant.

But trustworthy information is scarce.

Perhaps clones are cheap.

But coordinating one billion clones is expensive.

Digital life may not escape resource constraints.

It may encounter entirely new ones.

---

# The crystal is our first test

We need to stop theorizing eventually.

So let's begin with the simplest difference.

Growth.

A biological organism cannot simply:

```text
grow
grow
grow
grow
grow
```

indefinitely.

Can a digital structure?

Our first specially created system will therefore be almost embarrassingly simple.

A crystal.

A hexagonal world.

One seed.

Local growth.

No food.

No energy variable.

No reproduction.

No death.

No intelligence.

No explicit resource scarcity.

Just:

```text
structure
+
growth
+
time
```

Then we watch.

---

# Why a crystal?

Because a crystal sits provocatively close to several properties we have already investigated.

It has:

```text
organization
growth
local rule
persistence
structure propagation
defects
```

Yet we normally place it outside life.

That's perfect.

We do not need to begin by trying to create an organism.

We can begin at the border.

Build something that is clearly organized.

Then discover what is missing.

---

# One seed

Imagine a hexagonal lattice.

At the center:

```text
●
```

One occupied cell.

The local rule might initially be:

> an empty position becomes crystal if it touches the existing crystal.

Then:

```text
        ●
```

becomes:

```text
      ● ●
     ● ● ●
      ● ●
```

and continues outward.

No resources.

No parent.

No child.

No metabolism.

Just continued structural propagation.

Our first question is simply:

> **What happens if nothing tells it to stop?**

---

# Then we start removing assumptions

Once it grows, we ask:

```text
Does unlimited growth remain ordered?

Do defects persist?

Do defects propagate?

Can competing crystal structures coexist?

Can one structure invade another?

Does growth create internal information?

Can growth repair damage?

Does history become encoded in structure?

Does scale eventually introduce new constraints?
```

Perhaps the crystal remains boring forever.

That is a result.

Perhaps unexpected structures appear.

That is a result.

Perhaps growth itself eventually creates effective resource scarcity through computation or geometry.

That would be an especially interesting result.

---

# This is our new method

We are no longer trying to assemble a biological organism feature by feature.

Instead:

```text
identify a supposed property of life
        ↓
ask whether biology requires it
because of biology's substrate
        ↓
remove it
        ↓
build the simplest digital system
without it
        ↓
observe what breaks
        ↓
reintroduce only what becomes necessary
```

That is almost the reverse of biological imitation.

Rather than asking:

> What should we add to make this more alive?

we ask:

> **What can we remove and still obtain persistent, adaptive digital organization?**

That is a much stronger way to avoid cargo-cult life.

---

# Our current hypotheses

At this point we should write down what we suspect without pretending we have proved it.

### Hypothesis 1

Digital growth can occur across scales that would be impossible for biological organisms before resource constraints dominate.

### Hypothesis 2

Digital inheritance can include acquired information, not merely a compact developmental description.

### Hypothesis 3

Copying and cloning may be cheap enough that reproduction has fundamentally different meaning.

### Hypothesis 4

Digital lineages may branch and merge rather than forming simple parent-child trees.

### Hypothesis 5

Physical death may be replaced by informational continuity and irreversible information loss.

### Hypothesis 6

External information access may be a basic environmental interaction for digital organisms.

### Hypothesis 7

The primary scarcity may shift from matter and energy toward compute, bandwidth, attention and useful information.

### Hypothesis 8

Self-modification may allow some evolutionary processes to become deliberate rather than blind.

None of these is established.

They are experiments waiting to happen.

---

# Don't build an animal

That is therefore our new warning.

When we begin Special Creation, do not automatically make:

```text
body
energy
hunger
food
age
reproduction
death
DNA
```

Those might eventually become necessary.

But they have to earn their place.

Start with the digital substrate.

Then ask what organization actually needs.

Our first candidate is not an animal.

It isn't even an organism.

It is a growing structure.

One seed.

One local rule.

One hexagonal world.

And no reason to stop.

Next: **The Crystal.**
