+++
date = '2026-08-10T20:52:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 49: Profile Before You Optimize'
categories = ['Programming', 'Performance']
tags = ['Cellular Automata', 'Python', 'Profiling', 'Performance']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 49: Profile Before You Optimize

By now we have built dozens of automata.

The natural temptation is to make them faster.

The wrong first question is:

> Which optimization trick should I use?

The right first question is:

> Where is the time actually going?

Performance work begins with measurement.

---

## Define the workload first

A benchmark is only meaningful if the workload is explicit.

For a cellular automaton, record at least:

```text
grid size
number of channels
neighborhood radius
number of steps
data type
boundary rule
backend
```

A 64×64 Conway grid and a 1024×1024 multi-channel Lenia system are not the same performance problem.

---

## Time one complete rollout

```python
from time import perf_counter


def benchmark(step_fn, state, steps=200):
    x = state.copy()

    start = perf_counter()
    for _ in range(steps):
        x = step_fn(x)
    elapsed = perf_counter() - start

    return {
        "seconds": elapsed,
        "steps_per_second": steps / elapsed,
        "seconds_per_step": elapsed / steps,
    }
```

Run the benchmark several times.

The first run may include allocation, cache warm-up, kernel compilation or other one-time costs.

---

## Measure scaling, not one number

```python
sizes = [64, 128, 256, 512, 1024]

for size in sizes:
    state = make_state(size)
    result = benchmark(step, state)
    print(size, result["steps_per_second"])
```

A scaling curve tells us much more than one headline number.

If doubling width and height gives roughly four times the work, that is expected for a local 2D update.

If runtime grows much faster, something else is happening.

---

## Separate the phases

A step often contains several operations:

```text
neighborhood construction
rule evaluation
conflict resolution
state update
measurement
rendering
```

Time them separately.

```python
start = perf_counter()
neighbors = compute_neighbors(state)
t_neighbors = perf_counter() - start

start = perf_counter()
next_state = apply_rule(state, neighbors)
t_rule = perf_counter() - start
```

This prevents us from optimizing the wrong layer.

---

## Rendering can dominate

A surprisingly common mistake is benchmarking simulation and visualization together.

```python
for _ in range(1000):
    state = step(state)
    plt.imshow(state)
    plt.pause(0.01)
```

This measures a graphics loop as much as it measures the automaton.

For simulation benchmarks:

```text
disable plotting
avoid disk writes
avoid animation encoding
avoid debug logging
```

Then benchmark visualization separately.

---

## Memory matters too

Fast code that allocates huge temporary arrays may fail at realistic sizes.

For a `(2048, 2048)` float32 field:

```python
bytes_used = 2048 * 2048 * 4
print(bytes_used / 1024**2, "MiB")
```

Now multiply that by:

```text
current state
next state
neighbor accumulators
kernel buffers
hidden channels
batch dimension
```

Performance is often a memory problem before it is an arithmetic problem.

---

## Benchmark correctness with speed

Every optimization should preserve a reference implementation.

```python
expected = slow_step(state)
actual = fast_step(state)

assert np.array_equal(expected, actual)
```

For floating-point systems:

```python
assert np.allclose(expected, actual, atol=1e-6)
```

A faster wrong automaton is not an optimization.

---

## Record benchmark metadata

Do not save only:

```text
523 steps/s
```

Save:

```text
implementation
commit
Python version
NumPy/PyTorch version
device
grid dimensions
channels
steps
seed
elapsed time
```

Now benchmark results become evidence rather than anecdotes.

---

## The engineering lesson

Performance work should follow the same philosophy we used throughout the book:

```text
observe
measure
form a hypothesis
change one thing
measure again
```

In the next chapter we will attack one of the most common bottlenecks directly: Python loops over cells.