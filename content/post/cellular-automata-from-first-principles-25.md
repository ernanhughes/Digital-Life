+++
date = '2026-08-10T18:58:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 25: Evolve Rules for Desired Behaviour'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Evolutionary Search', 'Optimization']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 25: Evolve Rules for Desired Behaviour

Once we can represent a rule, mutate it and measure its behavior, we can evolve cellular automata.

The key idea is simple:

```text
population of rules
      ↓
simulate
      ↓
measure
      ↓
select
      ↓
mutate
      ↓
repeat
```

This chapter builds that loop without hiding it behind an optimization framework.

---

## Represent a rule as bits

For an elementary CA, eight output bits completely define the rule:

```python
import numpy as np


def rule_bits(rule_number):
    return np.array(
        [int(bit) for bit in f"{rule_number:08b}"],
        dtype=np.uint8,
    )
```

For larger rules, the same idea still works: the genome is simply larger.

---

## Define a target behavior

Suppose we want sustained activity without saturation.

A simple fitness function might reward:

- density near 0.5,
- persistent change,
- and non-trivial entropy.

```python
def fitness(metrics):
    density_term = 1.0 - abs(metrics["mean_density"] - 0.5)
    activity_term = metrics["tail_activity"]
    entropy_term = metrics["mean_entropy"]

    return (
        0.35 * density_term
        + 0.35 * activity_term
        + 0.30 * entropy_term
    )
```

This objective is not "the definition of complexity."

It is merely a design goal.

---

## Mutation

```python
def mutate(genome, rng, rate=0.05):
    child = genome.copy()
    mask = rng.random(len(child)) < rate
    child[mask] ^= 1
    return child
```

Mutation creates nearby rules.

---

## Selection

Keep the strongest candidates:

```python
def select(evaluated, survivors):
    evaluated = sorted(
        evaluated,
        key=lambda item: item[0],
        reverse=True,
    )
    return [genome for score, genome in evaluated[:survivors]]
```

Then refill the population with mutated offspring.

---

## A complete evolutionary loop

```python
def evolve(initial_population, evaluate_genome, generations=50, survivors=8, seed=42):
    rng = np.random.default_rng(seed)
    population = [g.copy() for g in initial_population]

    for generation in range(generations):
        evaluated = []

        for genome in population:
            metrics = evaluate_genome(genome)
            evaluated.append((fitness(metrics), genome))

        parents = select(evaluated, survivors)
        best_score = max(score for score, _ in evaluated)
        print(generation, best_score)

        next_population = [p.copy() for p in parents]

        while len(next_population) < len(population):
            parent = parents[rng.integers(len(parents))]
            next_population.append(mutate(parent, rng))

        population = next_population

    return population
```

The algorithm is small because most of the intellectual work happened earlier:

```text
representation
measurement
fitness
```

---

## Evaluate across several worlds

Never optimize against one initial condition if you want general behavior.

```python
def robust_fitness(genome, seeds):
    scores = []

    for seed in seeds:
        history = run_genome(genome, seed=seed)
        scores.append(fitness(fingerprint(history)))

    return float(np.mean(scores))
```

You can also penalize variance:

```python
return np.mean(scores) - 0.25 * np.std(scores)
```

Now rules are rewarded for working consistently rather than getting lucky once.

---

## Watch for objective hacking

Optimization finds loopholes.

If we reward activity alone, a rule that flips every bit every step may score extremely well.

If we reward entropy alone, noise-like behavior may dominate.

This is a useful lesson that reaches far beyond cellular automata:

> An optimizer will satisfy the measurement you gave it, not the intention you had in mind.

Use several measurements, inspect winners and test them out of distribution.

---

## Preserve diversity

Selecting only the highest score can collapse the population around one family of similar rules.

One simple improvement is to combine fitness and novelty:

```python
combined = 0.8 * normalized_fitness + 0.2 * normalized_novelty
```

Or maintain several behavior niches separately.

This lets evolution explore instead of only climbing one local hill.

---

## Store lineage

Keep parent-child relationships:

```python
record = {
    "generation": generation,
    "genome": genome.tolist(),
    "parent": parent_id,
    "fitness": score,
    "metrics": metrics,
}
```

Then an evolved rule is not a mysterious final artifact.

We can reconstruct how it emerged.

---

## From evolved rules to learned rules

Evolution changes the rule **between simulations**.

Later, neural cellular automata will use gradient descent to learn parameters of the local rule.

The optimization mechanism changes, but the surrounding experimental architecture remains recognizable:

```text
parameterized local rule
        ↓
simulation
        ↓
objective
        ↓
update rule parameters
```

Before we get there, we need one more conceptual piece.

Cellular automata are not only simulations. Some of them can perform computation.

The next chapter looks at information processing, universality and how to think about a cellular automaton as a computer.