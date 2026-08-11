+++
date = '2026-08-10T20:56:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 53: Build a Reusable Cellular Automata Engine'
categories = ['Programming', 'Software Design']
tags = ['Cellular Automata', 'Python', 'Architecture', 'Simulation']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 53: Build a Reusable Cellular Automata Engine

Across this book we repeatedly rebuilt the same pieces:

```text
state
neighborhood
rule
step loop
measurements
rendering
```

That repetition was useful while learning.

Now it is time to turn those concepts into interfaces.

---

## Keep the engine small

A useful engine does not need to know what Conway's Life, Lenia or an NCA is.

It only needs to orchestrate state transitions.

```python
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Automaton:
    state: Any
    step_fn: Callable[[Any], Any]

    def step(self):
        self.state = self.step_fn(self.state)
        return self.state

    def run(self, steps):
        for _ in range(steps):
            self.step()
        return self.state
```

That is intentionally boring.

Boring infrastructure is good infrastructure.

---

## Separate rule from execution

A Conway rule can be one function.

A Lenia rule can be another.

A neural CA can be an object with learned parameters.

The engine should not care.

```text
engine
  ↓
step(state)
```

That boundary gives us freedom to change implementations without rewriting the experiment layer.

---

## Make neighborhoods explicit

For more reusable systems we can separate neighborhood perception from transition logic:

```python
@dataclass
class Rule:
    perceive: Callable
    transition: Callable

    def __call__(self, state):
        local = self.perceive(state)
        return self.transition(state, local)
```

Now different systems can share the same neighborhood machinery.

---

## Add hooks instead of hard-coding features

```python
@dataclass
class Runner:
    automaton: Automaton
    observers: list

    def run(self, steps):
        for t in range(steps):
            state = self.automaton.step()
            for observer in self.observers:
                observer(t, state)
```

Observers might:

```text
measure density
save frames
record hashes
collect loss
track centroid
write checkpoints
```

The simulation does not need to know which are enabled.

---

## Keep rendering outside the state transition

Do not write:

```python
def step(state):
    ...
    save_png(state)
    return next_state
```

That couples scientific computation to presentation.

Instead:

```text
simulation produces state
observer records state
renderer turns records into artifacts
```

Now we can benchmark simulation without accidentally benchmarking image encoding.

---

## State types can differ

Classical CA might use:

```text
uint8 NumPy array
```

Lenia might use:

```text
float32 NumPy array
```

NCA might use:

```text
PyTorch tensor with batch and channel axes
```

A reusable engine should avoid forcing all systems into one representation unless there is a real reason.

---

## Define invariants per model

Generic infrastructure does not eliminate model-specific tests.

Examples:

```text
Rule 184 conserves car count
Life state remains binary
Lenia state remains in [0, 1]
Flow-style model conserves mass approximately
NCA tensor shape remains stable
```

The engine executes transitions.

The model contract defines what valid transitions mean.

---

## A useful architecture

```text
Experiment
   ↓
Runner
   ↓
Automaton
   ↓
Rule / Model
   ↓
Neighborhood backend
```

Alongside it:

```text
Observers
Metrics
Renderers
Artifact store
```

This is enough structure to support everything we have built without turning a teaching project into a giant framework.

---

## The goal is substitution

We should be able to change:

```text
NumPy → PyTorch
rolls → convolution
convolution → FFT
hand rule → neural rule
```

without changing the surrounding experiment definition.

Once execution is separated this way, reproducibility becomes much easier to formalize.

That is the next chapter.