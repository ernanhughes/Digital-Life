+++
date = '2026-08-10T20:41:00+01:00'
draft = false
title = 'Cellular Automata From First Principles 48: What Did the Neural CA Actually Learn?'
categories = ['Programming', 'Machine Learning']
tags = ['Cellular Automata', 'Python', 'PyTorch', 'Interpretability', 'Neural Cellular Automata']
series = ['Cellular Automata From First Principles']
+++

# Cellular Automata From First Principles 48: What Did the Neural CA Actually Learn?

Visualization gives us hypotheses.

Intervention gives us evidence.

If we suspect a hidden channel carries useful information, the next question is simple:

```text
what happens if we remove it?
```

This chapter turns NCA interpretability into controlled experimentation.

---

## Establish the behavioral baseline

Before touching the model, record its normal performance.

```python
baseline = evaluate_suite(model, test_mazes)
```

Keep metrics such as:

```text
valid-path rate
optimal-path rate
mean excess path length
unreachable-maze accuracy
stabilization time
```

Every intervention will be compared with this baseline.

---

## Zero one hidden channel

During every recurrent step, force one channel to zero.

```python
@torch.no_grad()
def rollout_with_zeroed_channel(model, state, frozen, steps, channel):
    for _ in range(steps):
        state = model(state)
        state[:, :3] = frozen[:, :3]
        state[:, channel] = 0.0
    return state
```

Evaluate every hidden channel separately.

```python
results = {}

for channel in range(5, state.shape[1]):
    results[channel] = evaluate_with_intervention(
        model,
        test_mazes,
        zero_channel=channel,
    )
```

A sharp performance drop tells us the channel is functionally important under this intervention.

It does not yet tell us exactly what it represents.

---

## Rank channels by causal importance

For each metric compute a delta from baseline:

```python
importance = baseline["valid_path_rate"] - result["valid_path_rate"]
```

Then rank channels.

You may find:

```text
some channels appear almost unused
some have mild redundant roles
one or two are critical
```

That reveals whether the learned computation is distributed broadly or bottlenecked through a few internal variables.

---

## Shuffle a channel spatially

Zeroing removes both content and magnitude.

A different intervention preserves the value distribution while destroying spatial organization.

```python
def spatial_shuffle(x, channel):
    flat = x[:, channel].flatten(1)

    for batch in range(flat.shape[0]):
        order = torch.randperm(flat.shape[1], device=x.device)
        flat[batch] = flat[batch, order]

    x[:, channel] = flat.view_as(x[:, channel])
    return x
```

If zeroing has little effect but spatial shuffling destroys performance, the pattern of the signal matters more than its average level.

---

## Freeze a channel in time

Another intervention asks whether a channel must keep evolving.

Capture it after a few steps:

```python
frozen_value = state[:, channel].clone()
```

Then restore that value after every later update.

```python
state[:, channel] = frozen_value
```

Try freezing at:

```text
t = 0
t = 4
t = 8
t = 16
t = 32
```

This can reveal temporal roles.

A channel may matter only during early frontier propagation and become irrelevant after the global field is established.

---

## Perturb local regions

Do not only intervene globally.

Erase a hidden channel inside one spatial region:

```python
def erase_patch(x, channel, y0, y1, x0, x1):
    x[:, channel, y0:y1, x0:x1] = 0.0
    return x
```

Compare damage near:

```text
start
goal
branch point
bottleneck
irrelevant open region
```

Now the intervention can reveal where an internal signal is needed.

---

## Swap hidden state between mazes

This is a stronger test.

Take two mazes `A` and `B` after the same number of recurrent steps.

Copy one hidden channel from A into B:

```python
state_b[:, channel] = state_a[:, channel]
```

Then continue B's rollout.

If the result degrades badly, that channel contains problem-specific spatial information.

If behavior barely changes, the channel may carry generic dynamics or may be redundant.

---

## Ablate groups, not only individuals

Neural representations are often redundant.

Two channels may compensate for one another.

So after individual ablations, test pairs and groups:

```python
critical_groups = [
    [6, 9],
    [7, 8, 11],
]
```

But combinatorics grow rapidly.

Use the individual results to prioritize combinations instead of exhaustively trying every subset.

---

## Test whether the visible output is doing hidden work

Sometimes a channel we think is merely an output participates in recurrence.

For example, if the distance prediction channel is fed back into perception at the next step, it is part of the computation.

Zero it after each step and evaluate again.

This separates:

```text
readout-only representation
```

from:

```text
recurrent working state
```

That distinction matters whenever outputs are embedded inside the automaton state.

---

## Compare learned propagation with hand-coded BFS

Now we can ask a deeper question.

Does the internal dynamics resemble a classical wavefront algorithm?

Evidence might include:

```text
activation arrival time tracks graph distance
critical channels move outward from the goal
freezing early propagation breaks distant cells first
spatial shuffling destroys pathfinding
larger mazes work with more recurrent steps
```

Together, those observations support an interpretation of iterative local propagation.

But do not overstate it.

The learned rule may implement a hybrid strategy unlike literal BFS.

---

## Build an evidence table

For each interpretability claim, record its support.

```text
claim:
"channel 7 carries goal-distance information"

observations:
- strong correlation with BFS distance
- linear probe predicts distance accurately
- zero ablation reduces valid-path rate
- spatial shuffle damages performance
- activation propagates outward from goal
```

This is much stronger than naming a heatmap by eye.

---

## What the NCA taught us

Across this section, the NCA has forced us to revisit nearly every theme in the book:

```text
locality
state
neighborhoods
repeated updates
emergence
computation
measurement
robustness
search
generalization
```

The difference is that the update rule is now learned.

Yet learning did not remove the need to understand the system.

It made careful experiments more important.

---

## We now have the full conceptual spine

We started with a binary row and an explicit rule table.

We ended with a learned recurrent distributed computer whose hidden states can be probed and perturbed.

The remaining work is no longer about introducing a fundamentally new kind of cellular automaton.

It is about turning everything we built into a **reusable, efficient and reproducible laboratory**.

The next part will therefore focus on engineering:

```text
performance
vectorization
GPU execution
experiment configuration
reproducibility
visualization
animation
benchmarking
reusable CA abstractions
end-to-end projects
```

That final engineering arc will make the book something readers can actually build on rather than merely finish.
