+++
date = '2026-08-10T18:57:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 24: Search Larger Rule Spaces'
categories = ['Programming', 'Simulation']
tags = ['Cellular Automata', 'Python', 'Search', 'Rule Space']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 24: Search Larger Rule Spaces

The 256 elementary rules are small enough to enumerate.

Most interesting cellular-automata design spaces are not.

Add more states, a larger neighborhood, continuous parameters, or several channels and exhaustive search quickly becomes impossible.

So we need search strategies.

---

## Why the rule space explodes

For `k` possible cell states and a neighborhood containing `n` cells, there are:

```text
k^n possible neighborhood configurations
```

A deterministic rule chooses one of `k` outputs for every configuration, giving:

```text
k^(k^n) possible rules
```

For elementary CA:

```text
k = 2
n = 3
2^(2^3) = 256
```

Increase the neighborhood to five cells:

```text
2^(2^5) = 4,294,967,296
```

Enumeration is already unattractive.

---

## Parameterized rules

One way to make a huge rule space tractable is to define a lower-dimensional family.

For a totalistic binary rule, the next state might depend only on the number of active neighbors:

```python
def totalistic_step(neighbor_count, birth_counts, survive_counts, alive):
    if alive:
        return int(neighbor_count in survive_counts)
    return int(neighbor_count in birth_counts)
```

Instead of specifying every neighborhood separately, we search sets of counts.

This introduces inductive bias, but also makes exploration manageable.

---

## Random search

The simplest strategy is often underrated:

```python
def random_rules(sample_rule, evaluate, trials, seed=42):
    rng = np.random.default_rng(seed)
    results = []

    for _ in range(trials):
        rule = sample_rule(rng)
        score = evaluate(rule)
        results.append((score, rule))

    return sorted(results, reverse=True)
```

Random search provides a baseline.

Any clever strategy should beat it under an equal evaluation budget.

---

## Local mutation search

Start from a promising rule and perturb it:

```python
def mutate_bits(rule_bits, rng, flips=1):
    child = rule_bits.copy()
    positions = rng.choice(len(child), size=flips, replace=False)
    child[positions] ^= 1
    return child
```

Then keep a child if it improves the objective.

```text
parent
  ↓ mutate
child
  ↓ evaluate
better? -> keep
worse?  -> reject
```

This is hill climbing over rule space.

---

## Novelty instead of a fixed objective

Sometimes we do not know what behavior we want.

Then search for rules that are behaviorally different from those already seen.

Represent each run using the fingerprints from previous chapters:

```python
vector = np.array([
    metrics["mean_density"],
    metrics["mean_activity"],
    metrics["mean_entropy"],
    metrics["compression_ratio"],
    metrics["sensitivity"],
])
```

A simple novelty score is distance to the nearest archived behaviors:

```python
def novelty(candidate, archive):
    if not archive:
        return float("inf")
    return min(np.linalg.norm(candidate - old) for old in archive)
```

Now search rewards new kinds of behavior rather than one predefined target.

---

## Cache evaluations

Search repeatedly revisits candidates.

Do not rerun deterministic experiments unnecessarily.

```python
cache = {}


def cached_evaluate(rule_key, evaluate):
    if rule_key not in cache:
        cache[rule_key] = evaluate()
    return cache[rule_key]
```

For stochastic rules, cache by the complete experiment identity:

```text
rule
seed
initial condition
world size
number of steps
metric version
```

This turns reproducibility into a performance feature.

---

## Search needs budgets

Make the resource limit explicit:

```python
MAX_EVALUATIONS = 10_000
```

Then compare algorithms under the same budget.

Without this, a more expensive search strategy can appear better simply because it performed more simulations.

---

## Search is now part of the subject

Once rule spaces become large, the object of study is no longer only:

```text
cellular automaton
```

It is:

```text
rule representation
    +
simulator
    +
measurements
    +
search strategy
    +
selection criterion
```

That architecture will carry directly into continuous and learned cellular automata later in the book.

In the next chapter we will turn local mutation into a full evolutionary search process and evolve rules toward explicit behavioral goals.