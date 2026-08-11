+++
date = '2026-08-10T18:59:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 26: Cellular Automata as Computation'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Computation', 'Rule 110']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 26: Cellular Automata as Computation

A cellular automaton is a state machine distributed across space.

Each cell reads local information, applies the same transition rule, and writes a new state.

That is already a form of computation.

The deeper question is whether local patterns can carry, transform and combine information in a way that supports general computation.

---

## Information needs carriers

In ordinary software, information lives in variables and memory addresses.

In a cellular automaton, information can be represented by patterns:

```text
stationary structures
moving structures
phase differences
collisions
```

A moving pattern can act like a signal.

Its position and phase can encode state.

---

## Signals and collisions

Imagine two localized structures moving toward one another.

Their collision may produce:

```text
nothing
one surviving structure
several new structures
a phase-shifted structure
```

If outcomes depend predictably on the inputs, collisions can implement logical transformations.

The physical-looking interaction is performing information processing.

---

## A tiny Boolean CA example

We can construct a deliberately simple local rule that computes XOR between two neighbors:

```python
def xor_step(state):
    left = np.roll(state, 1)
    right = np.roll(state, -1)
    return left ^ right
```

This is closely related to elementary Rule 90.

Run it:

```python
state = np.zeros(101, dtype=np.uint8)
state[50] = 1

history = []
for _ in range(60):
    history.append(state.copy())
    state = xor_step(state)
```

The famous triangular pattern is not merely decorative.

Every new bit is the result of a Boolean computation over local inputs.

---

## Computation can be spatial

Traditional code often looks like:

```text
instruction 1
instruction 2
instruction 3
```

Cellular automata instead compute through repeated spatial transformation:

```text
state(t)
   ↓ local parallel rule
state(t+1)
   ↓ local parallel rule
state(t+2)
```

There is no central instruction pointer.

The whole lattice advances together.

---

## Rule 110 revisited

Earlier we studied Rule 110 because simple local updates generate persistent interacting structures.

Those structures are central to why Rule 110 is important in computation theory: suitable patterns can encode and manipulate information, and Rule 110 has been shown to be computationally universal.

The important lesson for this book is not to reproduce the full universality proof.

It is to understand the architectural ingredients:

```text
stable background
    +
localized information carriers
    +
predictable interactions
    +
enough compositional structure
```

A rule does not need a CPU-shaped architecture to compute.

---

## Game of Life as a computer

Conway's Life provides another intuitive example.

Gliders can carry signals.

Glider streams can represent periodic signals.

Collisions and engineered structures can implement logical operations and memory.

Again, the same local Life rule continues everywhere.

The program lives in the arrangement of patterns, not in a changing rule table.

This gives us two layers:

```text
physics = cellular rule
program = initial configuration / structures
```

That separation is extremely powerful.

---

## Measure information flow experimentally

We can probe whether a perturbation influences a distant region.

Start two simulations differing by one bit:

```python
a = initial.copy()
b = initial.copy()
b[source] ^= 1
```

After `t` steps, test a target region:

```python
def region_difference(a, b, start, stop):
    return float(np.mean(a[start:stop] != b[start:stop]))
```

If the target eventually changes, information from the perturbation has propagated there.

This is a simple empirical causal experiment.

---

## Computation versus simulation

These concepts overlap but are not identical.

A forest-fire CA computes its next state, but we usually interpret it as simulation.

A logical construction in Life uses the same mechanism but we interpret patterns as symbols and operations.

The distinction comes from the mapping between physical states and an abstract task.

```text
cell dynamics
    ↓ interpretation
computation
```

---

## Why this matters for artificial life

Artificial-life systems sit at an interesting boundary.

A persistent organism-like structure must continually process information about its local environment:

```text
Where is my boundary?
Was I damaged?
What is around me?
How should local cells respond?
```

Neural cellular automata make that information processing explicit by replacing a hand-written transition rule with a learned local network.

But before neural rules, there is another remarkable step we should take.

We can remove the discrete binary state itself.

Instead of cells being simply alive or dead, let them take continuous values and interact through smooth kernels.

That is the road to **Lenia**.

---

## Part III complete

We began this section with a simple question:

> How do we compare cellular automata without relying entirely on our eyes?

We now have:

```text
measurement
  ↓
activity + density
  ↓
entropy + compression
  ↓
cycles + attractors
  ↓
sensitivity
  ↓
behavioral classification
  ↓
exhaustive search
  ↓
large-space search
  ↓
evolution
  ↓
computation
```

The next part changes the substrate itself.

We move from discrete cellular automata toward **continuous artificial life**: smooth state, convolution kernels, growth functions, Lenia, multi-channel systems and eventually Flow-Lenia.