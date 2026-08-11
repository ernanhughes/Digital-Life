+++
date = '2026-08-08T14:27:00+01:00'
draft = false
title = 'Models From First Principles 00: The Model Inside the Model'
categories = ['AI', 'PyTorch']
tags = ['pytorch', 'neural networks', 'model architecture', 'reasoning models', 'machine learning', 'AI']
series = ['Models From First Principles']
+++

# The Model Inside the Model

This is the first post in **Models From First Principles**.

The previous **PyTorch: Zero to Hero** series worked from the bottom up.

We started with tensors.

Then gradients.

Then `nn.Module`.

Then data pipelines, convolution, attention, debugging, performance and finally a small GPT-style language model built from scratch.

That series answered:

> What are the pieces?

This series asks a different question:

> What happens when we start composing those pieces into increasingly sophisticated models?

The central idea is simple:

> A complicated model is usually a collection of smaller models, and those smaller models are themselves collections of simpler operations.

If we keep decomposing, the mystery disappears.

A model becomes a few heads.

A head becomes a few linear layers.

A recurrent reasoning system becomes a state update repeated several times.

A hierarchical model becomes two state-update mechanisms running at different rates.

A custom optimizer becomes a pair of moving averages and a parameter update.

The point of this series is not to memorize architectures.

It is to learn how to **read, decompose, build and reason about them**.

---

## 1. Why another model series?

The term **model** has become almost uselessly broad.

When someone says "model", they might mean:

- a frontier language model with hundreds of billions of parameters;
- a convolutional classifier;
- a tiny MLP that predicts a scalar;
- a value function;
- a policy head;
- a recurrent reasoning block;
- a sparse autoencoder;
- an ensemble;
- a calibration network;
- or a small learned component buried inside a much larger system.

That can make model architecture feel harder than it really is.

The word suggests one monolithic object.

The code usually tells a different story.

Consider this:

```text
large model
    ↓
smaller sub-models
    ↓
blocks
    ↓
layers
    ↓
tensor operations
```

Once you can move up and down that hierarchy, a model stops being a black box.

That is the skill we are going to practise.

---

## 2. This series builds on PyTorch Zero to Hero

I am not going to re-explain every PyTorch primitive from scratch in every article.

When we see:

```python
nn.Linear(256, 128)
```

we will assume you know what a linear layer is.

When we see:

```python
loss.backward()
```

we will assume you understand autograd.

When we see:

```python
class Model(nn.Module):
    ...
```

we will assume you understand parameter registration and `state_dict()`.

When we see:

```python
nn.MultiheadAttention(...)
```

we will not treat Q, K and V as magic.

The earlier series exists precisely so we can now work one level higher.

Instead of asking:

> What does `nn.Linear` do?

we can ask:

> Why is this linear layer here?

Instead of asking:

> How does autograd work?

we can ask:

> What objective is this model actually learning?

Instead of asking:

> What shape does attention expect?

we can ask:

> Why does this architecture need attention at all?

That is the shift.

---

## 3. The architecture lineage we will study

We are going to follow a sequence of increasingly sophisticated ideas.

The implementations that motivated this series grew out of real evaluation and reasoning models, but every article will stand independently.

You do not need the original system.

You do not need its database.

You do not need its agents.

You only need PyTorch and the willingness to inspect what the model is actually doing.

Our roadmap is roughly:

```text
MR.Q
  ↓
EBT
  ↓
SICQL
  ↓
HRM
  ↓
Tiny
  ↓
PACS
```

This is not Python inheritance.

It is an **evolution of modelling ideas**.

Each step asks what the previous step could not express cleanly enough.

---

## 4. Stage one: turn two embeddings into one judgement

Suppose we have two pieces of text:

```text
prompt
response
```

An embedding model turns each into a vector:

```text
prompt   → context embedding
response → response embedding
```

Now imagine that our job is to answer one question:

> How good is this response for this prompt?

A very small model is enough to begin.

Conceptually:

```text
context embedding
        +
response embedding
        ↓
      encoder
        ↓
     predictor
        ↓
      score
```

We can express that in PyTorch with almost nothing:

```python
import torch
from torch import nn


class PairEncoder(nn.Module):
    def __init__(self, embedding_dim: int, hidden_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, context, response):
        pair = torch.cat([context, response], dim=-1)
        return self.net(pair)


class QualityPredictor(nn.Module):
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, z):
        return self.net(z).squeeze(-1)
```

Then compose them:

```python
class QualityModel(nn.Module):
    def __init__(self, embedding_dim=1024, hidden_dim=256):
        super().__init__()
        self.encoder = PairEncoder(embedding_dim, hidden_dim)
        self.predictor = QualityPredictor(hidden_dim)

    def forward(self, context, response):
        z = self.encoder(context, response)
        return self.predictor(z)
```

That is already a useful model.

But notice what happened.

We said we had **one model**.

The code immediately decomposed into:

```text
QualityModel
    │
    ├── PairEncoder
    │      ├── Linear
    │      ├── ReLU
    │      └── Linear
    │
    └── QualityPredictor
           ├── Linear
           ├── ReLU
           └── Linear
```

The model contains models.

And those models contain layers.

And those layers contain tensor operations.

This is the pattern for the whole series.

---

## 5. The first important question: what does the representation mean?

The most important tensor in the previous example is not necessarily the final score.

It may be this one:

```python
z = self.encoder(context, response)
```

Why?

Because `z` is the shared representation from which we can ask more questions.

A scalar predictor throws information away.

The representation can support many predictions.

That immediately suggests the next architecture.

Instead of:

```text
representation
     ↓
   score
```

we can do:

```text
                 representation
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Q head        V head      policy head
```

Now our model is no longer answering just one question.

It is producing a small **decision surface**.

---

## 6. Stage two: one representation, multiple heads

Here is a stripped-down version:

```python
class MultiHeadEvaluator(nn.Module):
    def __init__(self, embedding_dim=1024, hidden_dim=256, num_actions=3):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
        )

        self.q_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

        self.v_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, num_actions),
        )
```

The forward pass is still simple:

```python
def forward(self, context, response):
    pair = torch.cat([context, response], dim=-1)
    z = self.encoder(pair)

    q = self.q_head(z).squeeze(-1)
    v = self.v_head(z).squeeze(-1)
    policy_logits = self.policy_head(z)

    return {
        "q": q,
        "v": v,
        "advantage": q - v,
        "policy_logits": policy_logits,
    }
```

The architecture sounds more sophisticated.

But recursively decompose it:

```text
MultiHeadEvaluator
       │
       ├── encoder
       │
       ├── Q model
       │
       ├── V model
       │
       └── policy model
```

Each head is tiny.

The sophistication comes from **what the heads mean together**.

That distinction matters.

---

## 7. Architecture is often semantics plus composition

A common mistake when reading neural-network code is to look only for exotic layers.

But many meaningful model improvements use ordinary layers differently.

These two networks might both be:

```python
nn.Sequential(
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Linear(128, 1),
)
```

One might estimate:

```text
Q(s, a)
```

while the other estimates:

```text
V(s)
```

Same primitive architecture.

Different semantic role.

Then:

```text
advantage = Q - V
```

creates another useful signal without adding a neural layer at all.

This is one of the recurring lessons of the series:

> Architectural sophistication is not the same thing as architectural novelty.

Sometimes the breakthrough is a new component.

Sometimes it is a new objective.

Sometimes it is a new relationship between familiar components.

Sometimes it is simply running the same component repeatedly.

---

## 8. Stage three: make the heads first-class models

Once Q, V and policy become important enough, it becomes useful to make them explicit modules.

For example:

```python
class QHead(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, z):
        return self.net(z).squeeze(-1)
```

And:

```python
class VHead(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, z):
        return self.net(z).squeeze(-1)
```

And:

```python
class PolicyHead(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_actions):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_actions),
        )

    def forward(self, z):
        return self.net(z)
```

Then composition becomes explicit:

```python
class DecisionModel(nn.Module):
    def __init__(self, encoder, q_head, v_head, policy_head):
        super().__init__()
        self.encoder = encoder
        self.q_head = q_head
        self.v_head = v_head
        self.policy_head = policy_head

    def forward(self, context, response):
        z = self.encoder(context, response)

        q = self.q_head(z)
        v = self.v_head(z)
        policy_logits = self.policy_head(z)

        return {
            "q": q,
            "v": v,
            "advantage": q - v,
            "policy_logits": policy_logits,
        }
```

This is worth pausing on.

We have gone from:

```text
one model
```

to:

```text
model = encoder + Q model + V model + policy model
```

That is not complication for its own sake.

It gives us independent components that can be:

- trained differently;
- inspected independently;
- frozen independently;
- loaded independently;
- tested independently;
- replaced independently;
- compared independently.

Composition creates experimental freedom.

---

## 9. Stage four: what if one forward pass is not enough?

So far every architecture has been fundamentally feed-forward.

We produce a representation and immediately predict from it.

But suppose we want the model to **refine internal state**.

Then instead of:

```text
input → representation → output
```

we can think in terms of:

```text
input + previous state → new state
```

Repeated:

```text
z0
 ↓
f(input, z0)
 ↓
z1
 ↓
f(input, z1)
 ↓
z2
 ↓
f(input, z2)
 ↓
z3
```

Now the model has something resembling an internal computational trajectory.

Not consciousness.

Not magic reasoning.

A sequence of learned state transitions.

That distinction is important.

---

## 10. A recurrent block is still small

A recurrent reasoning block might look like:

```python
class RecurrentBlock(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.cell = nn.GRUCell(input_dim, hidden_dim)
        self.norm = nn.RMSNorm(hidden_dim)

    def forward(self, previous_state, current_input):
        state = self.cell(current_input, previous_state)
        return self.norm(state)
```

That is it.

The new ability comes from **iteration**.

For example:

```python
state = torch.zeros(batch_size, hidden_dim, device=x.device)

for _ in range(6):
    state = block(state, x)
```

Now compare that to the feed-forward version:

```python
state = encoder(x)
```

The primitive block is not dramatically more complicated.

The computation strategy changed.

This is why reading only the layer list can be misleading.

You also need to understand the **control flow around the layers**.

---

## 11. Stage five: two reasoning speeds

Now take recursion one step further.

Instead of one state, maintain two:

```text
low-level state
high-level state
```

Let the low-level state update several times for every high-level update.

Conceptually:

```text
input
  │
  ▼
projected representation
  │
  ├──────────────────────────┐
  │                          │
  ▼                          │
low-level state              │
  │                          │
  ├─ update                  │
  ├─ update                  │
  ├─ update                  │
  └─ update                  │
  │                          │
  ▼                          │
high-level state ────────────┘
```

In pseudocode:

```python
for cycle in range(num_cycles):
    for step in range(low_level_steps):
        low_state = low_block(
            low_state,
            torch.cat([x, high_state], dim=-1),
        )

    high_state = high_block(
        high_state,
        torch.cat([low_state, high_state], dim=-1),
    )
```

That sounds like a "hierarchical reasoning model".

And it is.

But look at what it is made from:

```text
2 recurrent blocks
+
2 state tensors
+
a nested loop
```

Again:

> The model becomes understandable when we decompose it.

---

## 12. The prediction surface can evolve independently of the reasoning core

Once we have a richer internal representation, we can ask more questions of it.

For example:

```text
                         hidden state
                              │
          ┌───────────┬───────┼─────────┬───────────┐
          ↓           ↓       ↓         ↓           ↓
        score     uncertainty OOD   consistency reconstruction
```

A model can therefore evolve along at least two dimensions:

```text
How does it compute a representation?
```

and:

```text
What predictions does it make from that representation?
```

Those are different architectural decisions.

For example, a score head might be:

```python
self.score_head = nn.Linear(hidden_dim, 1)
```

An uncertainty head might also be:

```python
self.logvar_head = nn.Linear(hidden_dim, 1)
```

An OOD head:

```python
self.ood_head = nn.Linear(hidden_dim, 1)
```

Three identical layer shapes.

Three completely different meanings.

Again, semantics matter.

---

## 13. Uncertainty is a model output too

A scalar quality score gives us:

```text
0.82
```

But it does not tell us whether the model thinks:

```text
I am very sure this is 0.82
```

or:

```text
I barely know what I am looking at, but 0.82 is my best guess
```

One approach is to learn a second quantity representing uncertainty.

For example:

```python
score_logit = self.score_head(z)
log_variance = self.logvar_head(z)
```

The architecture has not suddenly become enormous.

We added another tiny head.

But the **information surface** became much richer.

This pattern will appear repeatedly.

---

## 14. Calibration is another small model

Suppose our score logits are systematically overconfident.

We might learn a temperature:

```python
temperature_raw = self.temperature_head(z)
temperature = 0.5 + 0.5 * torch.nn.functional.softplus(temperature_raw)
score = torch.sigmoid(score_logit / temperature)
```

Now the model contains a learned calibration mechanism.

Again, recursively:

```text
calibration system
      ↓
Linear(hidden_dim, 1)
      ↓
softplus
      ↓
scale logits
```

The label sounds large.

The implementation may be tiny.

---

## 15. Reconstruction turns representation quality into something measurable

Another useful trick is to ask the hidden state to reconstruct part of the input representation.

For example:

```python
self.reconstruction_head = nn.Linear(hidden_dim, hidden_dim)
```

Then:

```python
reconstructed = self.reconstruction_head(z)
```

Compare it to the original projected input:

```python
similarity = torch.nn.functional.cosine_similarity(
    reconstructed,
    projected_input,
    dim=-1,
)
```

Now the model is not only asked:

> What is the score?

It is also asked:

> Did the representation preserve enough information about the thing being judged?

The diagnostic head becomes a probe into the model's internal representation.

---

## 16. Stage six: simplify the recursion

Hierarchical recurrence is useful, but perhaps we can get much of the benefit from a smaller recursive state machine.

Imagine three vectors:

```text
x = goal

y = response

z = current latent state
```

Fuse them:

```python
fused = torch.cat([x, y, z], dim=-1)
```

Project:

```python
z_next = torch.tanh(self.z_projection(fused))
```

Process:

```python
z_next = self.core(z_next)
```

Then make a small residual update:

```python
z = z + 0.1 * z_next
```

Repeat.

```python
for _ in range(num_recursions):
    fused = torch.cat([x, y, z], dim=-1)
    z_next = torch.tanh(self.z_projection(fused))
    z_next = self.core(z_next)
    z = z + step_scale * z_next
```

That is a recursive model.

The model is repeatedly reconsidering the same goal/response pair while carrying forward a learned latent state.

Still no magic.

Just tensors and a loop.

---

## 17. What is the core inside that recursive model?

Maybe this:

```python
class TinyBlock(nn.Module):
    def __init__(self, d_model, dropout=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_model * 4, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return x + self.mlp(self.norm(x))
```

That should look familiar if you completed the PyTorch series.

It is just:

```text
LayerNorm
   ↓
Linear expansion
   ↓
GELU
   ↓
Linear projection
   ↓
residual
```

The recursive model is made from residual blocks.

The residual blocks are made from familiar PyTorch layers.

That is exactly why we did the first series first.

---

## 18. Add attention without changing the idea

We can replace the core with an attention-enhanced block:

```python
class TinyAttentionBlock(nn.Module):
    def __init__(self, d_model, num_heads=4, dropout=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.attention = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.ff = TinyBlock(d_model, dropout)

    def forward(self, x):
        h = self.norm(x)
        attended, _ = self.attention(h, h, h, need_weights=False)
        x = x + attended
        return self.ff(x)
```

Now the core can model interactions across a sequence.

But the outer recursion is unchanged.

This is another powerful architectural principle:

> If components have clean interfaces, you can replace the inside without rewriting the outside.

---

## 19. A sparse autoencoder is another model inside the model

Suppose the final latent state is dense:

```text
z = [0.71, -0.13, 0.42, 0.09, ...]
```

We might want a smaller sparse concept representation.

One simple approach is a sparse autoencoder-style bottleneck:

```python
class SparseBottleneck(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.LayerNorm(d_model // 2),
        )
        self.decoder = nn.Linear(d_model // 2, d_model)

    def forward(self, z):
        concepts = self.encoder(z)
        reconstruction = self.decoder(concepts)
        return concepts, reconstruction
```

Now our recursive model contains:

```text
recursive state model
        ↓
core neural blocks
        ↓
sparse autoencoder
        ↓
prediction heads
```

A model inside a model inside a model.

And every layer is still something we already know how to inspect.

---

## 20. Stage seven: go below the model

Eventually we reach another layer of the stack.

So far we have asked:

> What architecture should compute the prediction?

But the model also has to learn.

That means parameter updates.

The default answer is often AdamW.

But optimizers are code too.

They can be decomposed too.

Suppose we maintain two statistics for every parameter:

```text
moving average of gradients
moving average of squared gradients
```

In simplified form:

```python
grad_avg = beta * grad_avg + (1 - beta) * grad

precond = decay * precond + (1 - decay) * grad.square()
```

Then normalize the averaged gradient:

```python
step = grad_avg / (precond.sqrt() + eps)
```

And update:

```python
parameter -= learning_rate * step
```

That is already the heart of an adaptive, preconditioned optimizer.

The optimizer sounded like a completely different kind of thing.

But the same first-principles method works:

```text
optimizer
   ↓
state variables
   ↓
update equations
   ↓
tensor operations
```

Nothing gets a black-box exemption.

---

## 21. The complete evolutionary picture

Now step back.

The progression looks something like this:

```text
1. Pair scorer

context + response
       ↓
 representation
       ↓
     score
```

Then:

```text
2. Multi-head evaluator

context + response
       ↓
 representation
       ↓
 ┌─────┼─────┐
 Q     V   Policy
```

Then:

```text
3. Explicit compositional model

encoder
  +
Q model
  +
V model
  +
policy model
```

Then:

```text
4. Recurrent reasoning

input + state
      ↓
state update
      ↓
repeat
```

Then:

```text
5. Hierarchical recurrence

fast state updates
        ↓
slow state update
        ↓
repeat
```

Then:

```text
6. Compact recursive model

x + y + z
    ↓
small core
    ↓
residual state update
    ↓
repeat
```

Then:

```text
7. Rich diagnostics

latent state
  ↓
score / uncertainty / OOD / consistency / calibration / reconstruction
```

Then:

```text
8. Interpretable bottleneck

latent state
   ↓
sparse concepts
   ↓
reconstruction
```

Then:

```text
9. Learning machinery

gradient
  ↓
moving statistics
  ↓
preconditioned step
  ↓
parameter update
```

At no point did we need to jump from "simple neural network" to "incomprehensible intelligence machine".

We added capabilities one architectural decision at a time.

---

## 22. This is how I want you to read model code

When you open an unfamiliar PyTorch model, do not start by reading every line.

First ask:

### What are the inputs?

For example:

```text
context embedding
response embedding
latent state
sequence length
```

### What are the persistent states?

For example:

```text
parameters
recurrent state
optimizer state
```

### What is the main representation?

Look for tensors like:

```text
z
hidden
state
features
encoded
```

### What transforms that representation?

Look for:

```text
MLP
attention
GRU
convolution
projection
normalization
```

### Is computation repeated?

Look for:

```python
for step in range(...):
```

or recurrent calls.

### What outputs come from the representation?

Look for heads:

```text
score_head
q_head
v_head
policy_head
uncertainty_head
ood_head
```

### What objectives train those outputs?

An output head without its loss tells you only half the architecture.

### What is diagnostic rather than primary?

Not every output is the main decision.

Some exist to regularize or inspect the representation.

### How do parameters move?

Finally inspect:

```text
optimizer
learning rate
weight decay
gradient clipping
schedulers
custom update rules
```

That sequence is much easier than reading top-to-bottom.

---

## 23. Draw the model before you explain it

For every post in this series, we are going to draw the architecture as a data-flow graph.

Not because diagrams are decorative.

Because diagrams expose misunderstanding.

If you cannot reduce a model to something like:

```text
input
  ↓
encoder
  ↓
latent state
  ↓
heads
```

then you probably do not understand it yet.

For recurrent models, the arrows should show recurrence.

For hierarchical models, the arrows should show update rates.

For multi-head models, the shared representation should be obvious.

For optimizers, the state variables should be visible.

The diagram becomes a test of our explanation.

---

## 24. Then prove the diagram with tensor shapes

Suppose the architecture says:

```text
context [B, 1024]
response [B, 1024]
       ↓ concatenate
pair [B, 2048]
       ↓ encoder
z [B, 256]
       ↓ Q head
q [B]
```

The code should prove exactly that.

```python
B = 8

context = torch.randn(B, 1024)
response = torch.randn(B, 1024)

pair = torch.cat([context, response], dim=-1)
assert pair.shape == (B, 2048)

z = encoder(pair)
assert z.shape == (B, 256)

q = q_head(z)
assert q.shape == (B,)
```

This is where the previous debugging-heavy PyTorch series pays off.

The architecture diagram is a hypothesis.

The runtime tensor shapes are evidence.

---

## 25. Parameter counts tell another part of the story

A model can sound sophisticated while still being tiny.

Always count parameters.

```python
def parameter_count(model):
    return sum(p.numel() for p in model.parameters())
```

And by component:

```python
def parameter_report(model):
    for name, module in model.named_children():
        count = sum(p.numel() for p in module.parameters())
        print(f"{name:24s} {count:12,d}")
```

A multi-head architecture might reveal:

```text
encoder                  590,000
q_head                    33,000
v_head                    33,000
policy_head               33,500
```

The conceptual richness may come mostly from adding several very cheap heads to one expensive representation.

That matters when designing real systems.

---

## 26. Activation counts matter too

Parameters are not the whole cost.

A recurrent model may reuse the same parameters several times.

For example:

```python
for _ in range(8):
    z = block(z)
```

The parameter count did not increase eightfold.

The compute did.

Likewise, attention may use a modest number of parameters but expensive activations as sequence length grows.

So throughout the series we will separate:

```text
parameter complexity
compute complexity
activation memory
training-state memory
```

These are not interchangeable.

---

## 27. A recurring experiment: remove the new idea

Whenever a model introduces something new, one of the best ways to understand it is to remove it.

If we add a V head:

```text
What changes if we train without V?
```

If we add recurrence:

```text
What happens with one recursion instead of six?
```

If we add hierarchy:

```text
What happens if low and high state update at the same rate?
```

If we add a sparse bottleneck:

```text
What changes when the bottleneck is bypassed?
```

If we add a custom optimizer:

```text
What changes against AdamW under the same budget?
```

That is an ablation.

And it turns architecture discussion into evidence.

---

## 28. Another recurring experiment: replace the component

Composition also lets us ask:

```text
What if this component were different?
```

For example:

```text
MLP core
   ↓ replace with
attention core
```

Or:

```text
GRUCell
   ↓ replace with
simple MLP state update
```

Or:

```text
learned temperature
   ↓ replace with
fixed temperature
```

Or:

```text
custom optimizer
   ↓ compare with
AdamW
```

The interface remains fixed while the implementation changes.

That is one reason modular architecture is powerful.

---

## 29. Small models are useful precisely because we can inspect them

There is another reason for this series.

Large language models dominate AI discussion, but many useful decisions do not require a large generative model.

Examples include:

```text
ranking
quality scoring
classification
routing
uncertainty estimation
out-of-distribution detection
policy selection
preference prediction
calibration
```

A small model has several advantages:

- cheap inference;
- local execution;
- deterministic latency;
- easier retraining;
- clearer inputs and outputs;
- easier ablation;
- easier instrumentation;
- easier failure analysis.

This series is not arguing that small models replace LLMs.

It is arguing that **not every learned decision should automatically become an LLM call**.

---

## 30. LLMs can generate the code. You still need the model in your head.

This connects directly to the debugging philosophy of the previous series.

An LLM can generate:

```python
class RecurrentEvaluator(nn.Module):
    ...
```

It can generate the heads.

It can generate the optimizer.

It can generate a training loop.

What you still need to know is:

```text
What is this model claiming to represent?

Which tensor carries that representation?

Which outputs depend on it?

Which loss teaches each output?

What is recurrent?

What is shared?

What is merely diagnostic?

What is actually being optimized?
```

Generated code without an architectural model in your head is just a larger debugging surface.

First principles give you that architectural model.

---

## 31. The series roadmap

Here is the working plan.

### Step 00 — The Model Inside the Model

This article.

How to recursively decompose neural architectures and how the model lineage we are going to study evolves.

### Step 01 — MR.Q: Building a Neural Quality Model From Two Embeddings

We will build the smallest useful evaluator:

```text
context + response → representation → Q value
```

We will inspect every tensor and loss.

### Step 02 — Inside MR.Q: Encoders, Predictors and Pair Representations

We zoom into the apparently simple model and treat the encoder and predictor as independent learned systems.

We will test alternative pair representations and show exactly what information is lost or preserved.

### Step 03 — EBT: From One Score to Q, V, Policy and Advantage

We turn one prediction into a multi-head decision surface.

We will explain why Q and V are different, why their difference matters, and what a policy head contributes.

### Step 04 — SICQL: Building a Decision Model From Smaller Models

We make Q, V and policy explicit modules and explore independent training, loading, replacement and inspection.

### Step 05 — HRM: Hierarchical Reasoning With Fast and Slow Recurrent State

We introduce recurrence and then hierarchy.

The focus will be state evolution, not mystique.

### Step 06 — Inside HRM: GRUs, RMSNorm, Calibration and Diagnostic Heads

We decompose the hierarchy into its smallest reusable components and examine uncertainty, OOD, consistency and reconstruction heads.

### Step 07 — Tiny: Recursive Reasoning With a Small Neural Network

We simplify hierarchical recurrence into a compact latent-state loop.

### Step 08 — Inside Tiny: Residual Blocks, Attention and Sparse Autoencoders

We open the recursive core and then open the model inside that model: the sparse bottleneck.

### Step 09 — PACS: Building an Optimizer From Gradient Statistics

We move beneath architecture and implement the learning rule itself.

### Step 10 — What Each Architecture Adds

We compare the lineage under the same conceptual task and ask what we actually gain at each step.

Not by name.

By capability, cost and evidence.

---

## 32. One important rule for the whole series

We will not use architecture names as explanations.

This sentence is not enough:

> The model uses hierarchical recurrence.

We need:

```text
what state exists;
how it is initialized;
what enters the update;
how often it updates;
what parameters are shared;
what tensor leaves the loop;
what losses act on that tensor.
```

Likewise:

> The model has uncertainty estimation.

is not enough.

We need to find:

```text
which head predicts it;
what the output means;
what target trains it;
how it affects the final decision;
how it is calibrated;
how we know it works.
```

Names are useful handles.

They are not explanations.

---

## 33. Another rule: separate architecture from training

A PyTorch class tells us the forward computation.

It does not automatically tell us how the model learns.

For every architecture we will distinguish:

```text
ARCHITECTURE
what computes what
```

from:

```text
OBJECTIVE
what losses define success
```

from:

```text
OPTIMIZATION
how gradients change parameters
```

from:

```text
DATA
what examples teach the model
```

Those four things are often blurred together in model discussions.

We will keep them separate.

---

## 34. And another rule: outputs are not evidence that they mean what their names say

If I write:

```python
self.uncertainty_head = nn.Linear(hidden_dim, 1)
```

I have not created uncertainty estimation.

I have created a scalar output called `uncertainty_head`.

For it to mean uncertainty, I need:

- an appropriate target or objective;
- training data that contains relevant information;
- validation showing the output tracks uncertainty;
- calibration tests;
- failure analysis.

The same applies to:

```text
reasoning
agreement
consistency
OOD
quality
preference
confidence
```

Model names are hypotheses.

Evaluation decides whether the hypotheses survived contact with data.

That scientific boundary will matter throughout the series.

---

## 35. Start from the tensor, not the branding

Here is a useful habit.

If someone tells you:

> This is a hierarchical recursive uncertainty-aware reasoning model.

translate it immediately into questions:

```text
What tensor goes in?

What tensor represents state?

What operation updates it?

How many times?

Where is the hierarchy?

Where is uncertainty produced?

What target trains uncertainty?

What makes the process reasoning rather than repeated transformation?
```

The point is not cynicism.

The point is precision.

Good architecture survives decomposition.

---

## 36. The final mental model

If you remember one picture from this introduction, make it this one:

```text
MODEL
  │
  ├── representation model
  │      │
  │      ├── projection
  │      ├── normalization
  │      └── learned transforms
  │
  ├── reasoning/state model
  │      │
  │      ├── recurrent update
  │      ├── attention
  │      └── residual processing
  │
  ├── prediction models
  │      │
  │      ├── score
  │      ├── value
  │      ├── policy
  │      ├── uncertainty
  │      └── diagnostics
  │
  └── learning system
         │
         ├── losses
         ├── gradients
         ├── optimizer state
         └── parameter updates
```

Every box can be opened.

Every arrow can be inspected.

Every tensor can be printed.

Every claim can be tested.

That is what **Models From First Principles** means.

---

# Next: build the smallest useful model

In **Step 01**, we will build MR.Q from scratch.

Not as a named architecture to memorize.

As a problem:

> Given a context and a candidate response, can a small neural model learn a useful scalar quality estimate?

We will start with two embeddings and build upward:

```text
context embedding
       +
response embedding
       ↓
pair representation
       ↓
encoder
       ↓
Q predictor
       ↓
scalar estimate
```

We will inspect:

- what the encoder is actually learning;
- whether concatenation is enough;
- logits versus probabilities;
- regression versus ranking objectives;
- parameter counts;
- gradient flow;
- overfitting a tiny dataset;
- calibration;
- failure cases;
- and how to prove the model is learning the relationship we think it is learning.

The model will be small.

That is the point.

We are going to understand all of it.
