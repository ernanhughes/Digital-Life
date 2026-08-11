+++
date = '2026-08-08T22:27:00+01:00'
draft = false
title = 'Advanced Agents From First Principles 00: When Should You Use an Advanced Agent Architecture?'
categories = ['AI', 'Agents']
tags = ['AI Agents', 'Agentic AI', 'LLM', 'Python', 'Multi-Agent Systems', 'MCTS', 'Mixture of Experts', 'Tree of Thoughts', 'Agent Architecture']
series = ['Advanced Agents From First Principles']
+++

# Advanced Agents From First Principles 00: When Should You Use an Advanced Agent Architecture?

You built an agent.

It can:

- call tools,
- maintain state,
- plan,
- revise its own work,
- search over alternatives,
- remember useful information,
- and verify whether the requested outcome actually happened.

Now the temptation begins.

You add another model.

Then a critic.

Then a planner.

Then a judge.

Then a router.

Then three specialist agents.

Then a tree search.

Then a memory layer that stores every trajectory.

Then a learned scorer that decides which branch survives.

Eventually your architecture looks like this:

```text
                         task
                          |
                       router
                    /     |      \
                 agent   agent   agent
                   |       |       |
                search   critic   planner
                   \       |       /
                    \      |      /
                        judge
                          |
                       verifier
                          |
                       executor
```

It certainly looks more advanced.

But did it become better?

That is the question this series is going to keep asking.

The central rule of **Advanced Agents From First Principles** is:

> **Advanced orchestration is not a capability ladder. It is a collection of mechanisms for specific failure modes.**

A single model call can outperform an elaborate agent system when the task is simple enough.

A deterministic workflow can outperform an autonomous planner when the route is already known.

Best-of-N can outperform tree search when the whole solution can be judged cheaply at the end.

A small local model can outperform a frontier model for routing if the routing problem is narrow and repetitive.

And sometimes the best multi-agent architecture is no multi-agent architecture at all.

This opening post gives us the decision framework for the entire advanced series.

We will answer a common practical question:

> **When should I use an advanced AI agent architecture instead of a simple agent loop?**

And we will build the answer from mechanisms rather than labels.

---

## Where the first series stopped

The core **Agents From First Principles** series built a useful agent stack one mechanism at a time.

Conceptually, we moved through something like this:

```text
model call
   |
structured action
   |
validation
   |
Best-of-N
   |
critique + revision
   |
planning
   |
act / observe loop
   |
tools
   |
memory
   |
search
   |
external verification
```

Those mechanisms are enough to build many production agents.

That matters.

We should not treat the advanced series as the point where the "real" agents begin.

The earlier architecture already gives us:

```text
state
  |
policy
  |
action
  |
environment
  |
observation
  |
verification
```

That is a complete control loop.

The advanced techniques become useful when a **specific bottleneck remains**.

For example:

```text
one policy keeps choosing badly
        |
        +--> route between specialists

one trajectory commits too early
        |
        +--> search more intelligently

one evaluator is unreliable
        |
        +--> use independent critics / judges

one model is too expensive for every step
        |
        +--> route work across model tiers

one agent cannot cover all expertise well
        |
        +--> specialist agents / mixture of agents

search spends compute badly
        |
        +--> tree policies / MCTS

runs repeatedly solve similar problems
        |
        +--> learn from trajectories
```

That is the mindset for this series.

---

# The most important diagnostic: what failure are you fixing?

Before adding an advanced mechanism, write down the failure in one sentence.

Bad reason:

> We should add a critic because advanced agents use critics.

Better:

> The generator produces a correct candidate in 42% of runs, but the current selector chooses that candidate only 61% of the time when it is present.

Now we have a concrete problem.

We can test whether a critic or learned selector improves the selection stage.

Bad reason:

> We need multi-agent debate.

Better:

> On architecture reviews, the first model systematically misses security and operability concerns even when those concerns are present in the repository evidence.

Now specialist reviewers may make sense.

Bad reason:

> We need MCTS.

Better:

> Beam search repeatedly prunes branches that look weak after one step but become the best solution after two diagnostic actions.

Now exploration/exploitation policy may actually be the bottleneck.

This gives us our first advanced-agent equation:

```text
advanced mechanism
        =
identified failure
        +
mechanism capable of fixing it
        +
measurement showing that it did
```

Without all three, we mostly have architecture theatre.

---

# Advanced does not mean more agents

People often use "advanced agent" as shorthand for "more agents."

That is too narrow.

An advanced agent system may involve only one model.

Consider a single model embedded inside Monte Carlo Tree Search:

```text
                state
                  |
              tree policy
             /    |    \
           s1     s2    s3
            |           |
        evaluate     expand
            \           /
             backpropagate
                  |
               choose
```

That may be much more sophisticated than three LLMs sending messages to one another.

Likewise, a mixture-of-experts router may choose among models without any conversational multi-agent behavior:

```text
request
   |
router
   |
   +--> cheap local model
   +--> code specialist
   +--> retrieval specialist
   +--> frontier model
```

The sophistication is in the **control policy**, not the number of chat participants.

So throughout this series we will distinguish several axes.

```text
search sophistication
routing sophistication
specialization
verification strength
adaptation
memory / learning
coordination
compute allocation
```

An architecture can be advanced on one axis and simple on all the others.

---

# The escalation ladder

A useful default is to escalate from the simplest architecture that can plausibly solve the task.

```text
single model call
       |
       v
fixed workflow
       |
       v
simple agent loop
       |
       v
Best-of-N / revise
       |
       v
beam-style search
       |
       v
specialist routing
       |
       v
adaptive search / MCTS
       |
       v
multi-agent coordination
       |
       v
learning / self-adaptation
```

This is not a ranking of intelligence.

It is a ranking of **control complexity**.

Each step adds potential capability.

Each step also adds things that can go wrong.

---

# The complexity tax

Suppose a one-shot model call costs:

```text
1 model call
1 prompt
1 response
```

Now add a planner and executor:

```text
plan
 |
execute step 1
 |
observe
 |
execute step 2
 |
observe
 |
verify
```

Now add a critic:

```text
plan
 |
critic
 |
revise plan
 |
execute
 |
critic
 |
revise output
 |
verify
```

Now add three specialist agents and a judge.

Very quickly, the system accumulates:

- more model calls,
- more latency,
- more context transformations,
- more stochastic decisions,
- more opportunities for disagreement,
- more intermediate state,
- more failure recovery,
- more logging requirements,
- more cost,
- and more difficulty reproducing a run.

We can think of this as a **complexity tax**.

```text
net value
    =
verified capability gain
    -
latency
    -
compute cost
    -
operational complexity
    -
new failure modes
```

The architecture earns its place only when the first term dominates the rest.

---

# Problem 1: the agent gives inconsistent answers

We already solved the simplest version of this problem with Best-of-N.

```text
prompt
  |
  +--> candidate A
  +--> candidate B
  +--> candidate C
           |
        selector
           |
         winner
```

That is often enough.

Do not jump directly from inconsistent answers to multi-agent debate.

First ask:

```text
Does generating more independent candidates raise oracle success?
```

If yes, then candidate diversity is useful.

Then ask:

```text
Can a cheap selector identify the good candidate?
```

If yes, stop there.

Only escalate if the simple mechanism fails.

An advanced architecture becomes justified when, for example:

- candidates require different expertise,
- a single judge is systematically biased,
- evaluation requires multiple independent criteria,
- or candidates are partial trajectories rather than complete answers.

That is how we get from Best-of-N to advanced ensemble systems without skipping the evidence.

---

# Problem 2: one model is not good at every subtask

This is where agent-level **mixture of experts** becomes useful.

Do not confuse this with neural mixture-of-experts inside a transformer.

A neural MoE might look like:

```text
hidden state
    |
  router
 /  |  \
E1  E2  E3
 \  |  /
 combined
```

The experts are neural modules inside the model.

At the agent level, we can route work between complete capabilities:

```text
task
 |
router
 |
 +--> retrieval expert
 +--> code expert
 +--> data expert
 +--> cheap local model
 +--> expensive frontier model
 +--> deterministic program
```

That can solve several practical software problems.

### Coding assistant

```text
question
  |
classifier
  |
  +--> repository search
  +--> code-generation model
  +--> test/debug agent
  +--> documentation search
```

### Support platform

```text
customer request
  |
router
  |
  +--> billing workflow
  +--> account workflow
  +--> technical troubleshooting
  +--> human escalation
```

### Research system

```text
claim
 |
router
 |
 +--> web retrieval
 +--> paper retrieval
 +--> code/data analysis
 +--> contradiction checker
```

The routing problem itself becomes measurable:

```text
routing accuracy
cost per route
fallback rate
verified task success
latency
```

Later in the series we will build this from first principles.

---

# Problem 3: search keeps pruning the future winner

The first agents series introduced beam-style search.

Beam search keeps the highest-scoring partial states.

```text
level 0              root
                    / | \
level 1            A  B  C
                   |\   /|
level 2            ... ...
```

If we keep the best `k` at each layer, the system is simple and efficient.

But it has a weakness.

A branch can look mediocre now and become excellent later.

Suppose:

```text
branch A score now = 0.82
branch B score now = 0.77
branch C score now = 0.48
```

Beam search may discard C.

But perhaps C contains an expensive diagnostic step that reveals the actual root cause.

Two steps later:

```text
A final = 0.61
B final = 0.66
C final = 0.95
```

This is where exploration becomes important.

Monte Carlo Tree Search introduces a policy that balances:

```text
exploit branches that look good
              +
explore branches we know less about
```

Conceptually:

```text
select
  |
expand
  |
simulate / evaluate
  |
backpropagate value
  |
repeat
```

But MCTS is not automatically better than beam search.

It becomes useful when the environment has properties such as:

- long-horizon consequences,
- misleading early scores,
- meaningful state transitions,
- reusable branch statistics,
- and enough budget to explore.

If one-step scores are already very predictive, beam search may remain better and far simpler.

---

# Problem 4: the model needs independent opposition

Critique-and-revision already gave us:

```text
draft
  |
critic
  |
revision
  |
verification
```

Sometimes the critic and generator share the same blind spot.

Then we may introduce specialization.

```text
                  proposal
                /    |     \
          security  cost  correctness
              |      |       |
            review review   review
                \     |     /
                   judge
                     |
                 revision
```

This is a legitimate multi-agent architecture when the reviewers contribute **different evidence or different decision functions**.

It is much less compelling when we merely rename identical prompts:

```text
Agent 1: think carefully
Agent 2: think carefully
Agent 3: think carefully
```

Three copies of the same blind spot are still one blind spot.

Specialization should therefore be observable.

We should be able to ask:

```text
Which agent finds which class of defect?
```

For example:

```text
security reviewer recall:      0.88
performance reviewer recall:   0.81
correctness reviewer recall:   0.93
```

And importantly:

```text
marginal defects found after overlap
```

If the third reviewer adds almost nothing, remove it.

---

# Problem 5: the expensive model is being wasted

A common production architecture calls the strongest model for everything.

```text
easy request ------> frontier model
medium request ----> frontier model
hard request ------> frontier model
routing task ------> frontier model
formatting task ---> frontier model
```

That is easy to build.

It may also be economically irrational.

An advanced agent can allocate compute adaptively.

```text
request
  |
cheap classifier
  |
  +--> deterministic code
  +--> small local model
  +--> medium model
  +--> frontier model
```

Or use escalation:

```text
cheap model
   |
verify
   |
pass? ---- yes ---> done
   |
   no
   v
stronger model
```

This is one of the most commercially important forms of advanced agent control.

The intelligence is not merely in answering the task.

It is in deciding **how much intelligence to spend**.

Metrics become:

```text
verified success
cost per successful task
frontier-model invocation rate
latency
escalation precision
escalation recall
```

A router that saves 70% of expensive calls while losing 0.2% verified success may be extremely valuable.

A router that saves 10% while losing 8% success is not.

---

# Problem 6: the same failures recur across runs

Memory alone retrieves previous information.

Learning changes future policy.

That distinction becomes important in advanced systems.

Suppose a coding agent repeatedly encounters this pattern:

```text
symptom:
ImportError after package refactor

successful strategy:
inspect pyproject -> inspect package layout -> inspect imports -> run focused tests
```

A memory system may retrieve the old trajectory.

A learning system may go further and modify future behavior:

```text
if symptom resembles package-refactor import failure:
    raise probability of package-layout diagnostic strategy
```

This could be implemented through:

- learned routing,
- learned scorers,
- reusable procedures,
- preference updates,
- trajectory ranking,
- or offline policy optimization.

The key boundary is:

> **Remembering an experience and changing policy because of that experience are not the same thing.**

Later posts will examine that distinction carefully.

---

# Problem 7: agents disagree

Multi-agent systems inevitably create disagreement.

For example:

```text
planner:    deploy immediately
critic:     rollback
verifier:   evidence incomplete
operator:   retry canary
```

The naive solution is another agent:

```text
judge: decide who is right
```

But now the judge can be wrong.

Then perhaps we add another judge.

This can recurse forever.

The better design question is:

```text
Can disagreement be resolved by stronger evidence?
```

For software systems, often yes.

```text
models disagree about whether code works
                 |
               tests

models disagree about whether deployment succeeded
                 |
          health metrics

models disagree about whether record exists
                 |
             database
```

This preserves one of the strongest rules from the first series:

> **When reality can answer, ask reality before adding another model.**

Multi-agent debate is most interesting where objective verification is incomplete, expensive, delayed, or impossible.

---

# The architecture-selection question

We can turn all of this into a practical decision tree.

Start here:

```text
Can one model call solve the task reliably?
        |
   yes -+-> use one model call
        |
        no
        v
Is the sequence known in advance?
        |
   yes -+-> deterministic workflow
        |
        no
        v
Does the task need environment feedback?
        |
   yes -+-> agent loop
        |
        v
Is variance the main problem?
        |
   yes -+-> Best-of-N
        |
        v
Does an existing candidate need local improvement?
        |
   yes -+-> critique + revise
        |
        v
Are there multiple plausible trajectories?
        |
   yes -+-> search
        |
        v
Does simple search allocate compute badly?
        |
   yes -+-> adaptive tree search / MCTS
        |
        v
Are subtasks meaningfully specialized?
        |
   yes -+-> routing / mixture of agents
        |
        v
Do independent perspectives add measurable coverage?
        |
   yes -+-> multi-agent review / debate
        |
        v
Do repeated runs contain learnable signal?
        |
   yes -+-> adaptive / learning agent
```

Notice what is missing:

```text
"advanced sounds better"
```

That is never a branch in the decision tree.

---

# Application map: where advanced agent techniques actually show up

The same mechanisms look very different depending on the software.

| Software | Advanced mechanism | Why it may help | What to measure |
|---|---|---|---|
| Coding assistant | MCTS / search | multiple repair trajectories | tests passed per compute |
| Code review | specialist agents | security/performance/correctness coverage | marginal defect recall |
| Research system | multi-source specialists | different source types and evidence | supported-claim recall |
| Browser automation | hierarchical policy | long action sequences | task completion / recovery |
| Customer support | mixture-of-agents router | distinct case classes | route accuracy / resolution |
| Data analysis | model/tool routing | code vs SQL vs retrieval | verified answer / cost |
| DevOps | planner + verifier + escalation | high-risk actions | recovery success / false action rate |
| Incident response | tree search | competing diagnoses | time to verified root cause |
| Scheduling | search / MCTS | long-horizon choices | objective schedule score |
| Long-running automation | learned policy | repeated task families | success improvement over time |

The important pattern is that the **software problem chooses the mechanism**.

Not the other way around.

---

# Coding agents: a concrete example

Suppose we are building a coding agent that receives:

> Fix the failing tests in this repository.

A simple loop might do:

```text
inspect tests
   |
inspect code
   |
edit
   |
run tests
   |
repeat
```

That may already work extremely well.

Do not add six agents automatically.

Now suppose the benchmark shows a particular failure:

```text
73% of failures are solved

27% fail
  |
  +--> 18% wrong root-cause hypothesis
  +--> 5% bad edit
  +--> 2% test misinterpretation
  +--> 2% timeout / tooling
```

The largest problem is diagnosis.

We might introduce search over hypotheses:

```text
failing test
    |
    +--> dependency hypothesis
    +--> state bug hypothesis
    +--> API regression hypothesis
    +--> fixture hypothesis
             |
         cheap evidence
             |
        prune / expand
```

That is a targeted advanced mechanism.

If diagnosis rises from 82% to 94% while cost rises 20%, perhaps it earns its place.

If cost triples and success moves from 73% to 74%, remove it.

---

# Research agents: another example

Suppose the task is:

> Determine whether a technical claim is supported by primary evidence.

One generalist agent may search and summarize.

An advanced architecture might separate roles:

```text
claim
  |
retrieval router
  |
  +--> papers
  +--> official docs
  +--> source code
  +--> datasets
          |
      evidence graph
          |
   contradiction search
          |
       verifier
```

This is not valuable because "multiple agents are smarter."

It is valuable if different retrieval surfaces require different search strategies and the evidence can later be recombined under a shared verifier.

The metrics might include:

```text
primary-source recall
unsupported-claim rate
contradiction recall
citation precision
cost per verified claim
```

---

# DevOps agents: why control matters more than eloquence

A DevOps agent can produce excellent prose and still be dangerous.

Suppose it diagnoses elevated error rates.

Potential actions:

```text
inspect logs
inspect metrics
compare deploys
restart service
rollback
scale replicas
change configuration
```

The advanced architecture may need:

```text
observation
   |
diagnostic search
   |
risk-aware planner
   |
policy gate
   |
canary action
   |
external verification
   |
escalate / rollback
```

Here the main value of sophistication is not linguistic quality.

It is:

- uncertainty management,
- action-risk control,
- staged commitment,
- verification,
- and rollback.

This is an important theme for the entire advanced series:

> **Advanced agents are primarily advanced control systems around probabilistic models.**

---

# What we will not do in this series

We will not treat architecture diagrams as evidence.

We will not assume:

```text
more agents = smarter
```

We will not assume:

```text
more tokens = more reasoning
```

We will not assume:

```text
more search = better answer
```

We will not assume:

```text
specialists = diversity
```

We will not assume:

```text
self-reflection = self-correction
```

We will not assume:

```text
learning from runs = improvement
```

Every mechanism will have a baseline.

Every mechanism will have failure modes.

Every mechanism will have measurements.

---

# The benchmark ladder

For advanced agents, benchmarking needs to become architectural.

Imagine this task suite:

```text
100 coding tasks
```

Run progressively more complex systems:

```text
A: one-shot model
B: simple tool agent
C: + critique/revision
D: + beam search
E: + specialist router
F: + MCTS
G: + multi-agent review
```

Measure at minimum:

```text
verified success rate
model calls
input tokens
output tokens
tool calls
wall-clock latency
cost
failures by stage
```

Then derive:

```text
cost per verified success
latency per verified success
marginal success gain
marginal cost
```

For architecture `X` relative to baseline `B`:

```text
marginal_success(X)
    = success(X) - success(B)
```

And:

```text
marginal_cost(X)
    = cost(X) - cost(B)
```

The question is not:

> Did advanced architecture X work?

The question is:

> **What additional verified capability did X buy, and what did that capability cost?**

---

# Failure attribution becomes mandatory

Complex systems fail in more places.

Suppose a multi-agent system fails a task.

Possible causes include:

```text
router chose wrong expert
expert generated poor result
critic missed defect
judge selected wrong candidate
memory retrieved stale evidence
search pruned winning branch
planner chose impossible sequence
executor failed
verifier produced false pass
budget terminated too early
```

If the system only logs:

```text
TASK_FAILED
```

we learn almost nothing.

Advanced systems need trajectory-level observability.

A useful event might look like:

```python
@dataclass
class AgentEvent:
    run_id: str
    step: int
    component: str
    decision: str
    input_ref: str
    output_ref: str
    evidence_refs: list[str]
    latency_ms: float
    cost: float
```

Then the run becomes inspectable:

```text
run
 |
 +-- router decision
 |
 +-- expert output
 |
 +-- critic output
 |
 +-- branch score
 |
 +-- prune decision
 |
 +-- tool action
 |
 +-- verification evidence
```

This is not merely observability infrastructure.

It is how we determine whether an advanced mechanism actually helped.

---

# Advanced agents as compute allocation

There is another useful way to understand nearly every technique in this series.

They allocate computation.

Best-of-N:

```text
allocate compute across independent final candidates
```

Tree search:

```text
allocate compute across partial trajectories
```

MCTS:

```text
allocate compute using exploration/exploitation estimates
```

Mixture of experts:

```text
allocate compute across specialized capabilities
```

Critic/reviser systems:

```text
allocate compute to inspecting and improving an existing candidate
```

Escalation routers:

```text
allocate expensive models only when cheaper paths appear insufficient
```

Multi-agent debate:

```text
allocate compute to independent perspectives and reconciliation
```

This gives us a powerful unifying question:

> **Where should the next unit of inference compute go?**

That is much more useful than asking whether a system is "agentic enough."

---

# Advanced agents as uncertainty management

Another unifying lens is uncertainty.

A simple model call hides uncertainty inside one generated output.

Advanced architectures can expose it.

Best-of-N exposes:

```text
output variance
```

Search exposes:

```text
trajectory alternatives
```

Multi-agent systems expose:

```text
perspective disagreement
```

Mixture-of-experts routing exposes:

```text
which capability should handle the task
```

Verification exposes:

```text
whether the result is actually supported
```

An advanced agent becomes useful when explicitly representing that uncertainty lets the runtime make a better decision.

But representing uncertainty is not enough.

We also need a mechanism that can **resolve** it.

Otherwise we have merely generated more uncertainty at greater cost.

---

# When a simple agent is still the right answer

After reading about MCTS, mixtures, debate and adaptive agents, it is easy to feel that a simple loop is primitive.

It is not.

Use the simple loop when:

- the task has a narrow action space,
- verification is strong,
- failures are recoverable,
- the environment provides frequent feedback,
- one model handles the domain well,
- latency matters,
- and additional search has little marginal value.

For example:

```text
read failing test
inspect implementation
patch code
run focused test
run suite
```

If that succeeds on 96% of the benchmark, adding MCTS may be absurd.

The simple architecture has enormous advantages:

```text
fewer moving parts
cheaper runs
lower latency
easier debugging
better reproducibility
simpler observability
smaller attack surface
```

Do not give those away for free.

---

# When advanced architecture is justified

Advanced architecture becomes increasingly attractive when tasks have several of these properties:

```text
long horizon
high branching factor
weak intermediate signals
specialized subtasks
expensive mistakes
multiple evidence sources
uncertain routing
large variance between generations
high value per successful task
repeated task families
available verification
```

For example, autonomous repository repair may have:

```text
many plausible root causes
many possible edits
cheap tests for partial evidence
expensive full-suite verification
repeated patterns across repositories
```

That is fertile ground for advanced search and routing.

A single FAQ response is not.

---

# A minimal architecture-selection record

Before adding a mechanism, we can record the decision explicitly.

```python
from dataclasses import dataclass


@dataclass
class ArchitectureExperiment:
    failure_mode: str
    baseline: str
    proposed_mechanism: str
    expected_effect: str
    primary_metric: str
    max_cost_increase: float
```

Example:

```python
experiment = ArchitectureExperiment(
    failure_mode="beam search prunes delayed-payoff diagnostic branches",
    baseline="beam_width_4",
    proposed_mechanism="ucb_tree_search",
    expected_effect="increase verified repair success",
    primary_metric="verified_success_rate",
    max_cost_increase=0.40,
)
```

Now we have made the architectural hypothesis falsifiable.

That is exactly what we want.

---

# The roadmap for Advanced Agents From First Principles

This series will build the advanced mechanisms progressively.

The current plan is:

```text
00  When Should You Use an Advanced Agent Architecture?

01  Chain of Thought as Computation

02  Self-Consistency: When One Reasoning Path Is Not Enough

03  Tree of Thoughts: Search Over Intermediate Reasoning States

04  Beam Search for Agents

05  Monte Carlo Tree Search for Agents

06  Evolutionary Agents

07  Mixture of Experts at the Agent Level

08  Planner / Executor / Critic Architectures

09  Multi-Agent Debate and Adversarial Review

10  Verification-Driven Advanced Agents

11  Adaptive Agents and Dynamic Compute Allocation

12  Learning From Previous Runs

13  Building a Mixture-of-Agents System

14  Which Advanced Agent Architecture Should You Use?
```

The exact order may evolve as the mechanisms reveal cleaner dependencies.

But the progression is deliberate.

We will move from:

```text
one reasoning trajectory
```

to:

```text
multiple trajectories
```

to:

```text
structured search
```

to:

```text
adaptive search
```

to:

```text
specialization and routing
```

to:

```text
coordination
```

to:

```text
adaptation across runs
```

---

# Search-facing debugging guide

If you found this post because your agent architecture has become complicated and unreliable, start here.

## Your agent is slower after adding multiple agents

Measure:

```text
model calls per task
serial critical path
parallelizable calls
context size per call
verification latency
```

Then compare verified success against the simpler baseline.

If success barely changed, remove components.

## Your multi-agent system keeps disagreeing

Ask whether disagreement can be resolved through:

```text
tests
database state
source evidence
metrics
schema validation
simulation
```

Prefer external evidence over another judge when possible.

## Your router keeps choosing the wrong agent

Measure a routing confusion matrix.

Look for:

- overlapping expert scopes,
- vague route descriptions,
- missing task features,
- too many experts,
- class imbalance.

Try deterministic routing for obvious cases before adding a more sophisticated model.

## MCTS costs too much

Measure:

```text
nodes expanded
unique branches
verification calls
value-estimator accuracy
success gain per additional node
```

Reduce the search budget or return to beam search if additional exploration has low marginal value.

## Your critic and generator agree too often

Check whether they actually have independent prompts, evidence, objectives or models.

If they share all four, they may simply be correlated copies.

## Your architecture works in demos but not production

Look for distribution differences in:

```text
task length
tool availability
latency
permissions
repository size
context size
failure recovery
verification coverage
```

Advanced architectures amplify operational assumptions.

---

# The principle we will carry through the entire series

We can now state the governing rule.

```text
start with the simplest system
        |
measure the failure
        |
identify the mechanism that could fix it
        |
add only that mechanism
        |
measure verified improvement
        |
keep or remove it
```

That is how we avoid building an elaborate agent architecture whose only measurable achievement is becoming elaborate.

The goal is not maximum agent complexity.

The goal is maximum useful capability per unit of cost, latency, risk and engineering effort.

Or more simply:

> **Every advanced mechanism must earn its complexity.**

---

# Next: Chain of Thought as Computation

The first advanced mechanism we will examine is often described too casually.

People say:

> "Just make the model think step by step."

But intermediate reasoning can play several very different roles inside an agent system.

It can be:

- disposable scratch state,
- a structured plan,
- a search node,
- an evaluator input,
- a decomposition mechanism,
- a trajectory that can be sampled multiple times,
- or a state representation that should never be trusted as evidence by itself.

The next post will therefore ask a practical question:

> **Does your AI agent fail on complex reasoning tasks? Treat intermediate reasoning as computation, not as proof.**

And from there we can build self-consistency, Tree of Thoughts, beam search and MCTS without treating any of them as magic.