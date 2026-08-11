+++
date = '2026-08-08T15:40:00+01:00'
draft = false
title = 'Agents From First Principles 00: What Is an Agent, Really?'
categories = ['AI', 'Agents']
tags = ['agents', 'AI agents', 'LLM agents', 'agentic systems', 'tool use', 'reasoning', 'AI']
series = ['Agents From First Principles']
+++

# What Is an Agent, Really?

This is the first post in **Agents From First Principles**.

It follows two earlier series.

In **PyTorch: Zero to Hero**, we worked upward from tensors, autograd and neural-network building blocks until we could build a small language model ourselves.

In **Models From First Principles**, we moved one level higher. We looked at how learned components can be composed into scorers, value models, policy heads, recurrent models, hierarchical models and compact recursive systems.

Now we move one level higher again.

We are going to build systems **around** models.

Not bigger neural networks.

Not another transformer.

Not another architecture hidden behind a model name.

Agents.

But before we build planners, tool users, memory systems, search trees, critics and verifiers, we need to remove a lot of ambiguity from the word itself.

The term *agent* is currently used for almost everything.

A script that calls an LLM is called an agent.

A chatbot is called an agent.

A workflow is called an agent.

A tool-using loop is called an agent.

A collection of twenty LLMs passing messages to one another is called a multi-agent system.

If the word means all of those things, it stops being useful.

So this post starts with the smallest useful definition and builds upward.

By the end, we will have this progression:

```text
model call
   ↓
model wrapped in a program
   ↓
stateful workflow
   ↓
observe → decide → act
   ↓
observe the result
   ↓
choose what to do next
   ↓
agent loop
```

The important idea is simple:

> **A model produces an output. An agent uses outputs to decide what happens next.**

That distinction will drive the entire series.

---

## 1. Start with a model call

The smallest possible LLM program looks something like this:

```python
answer = llm("Explain gradient descent")
print(answer)
```

There is nothing wrong with this.

In fact, for many problems this is exactly what we should use.

The program supplies an input.

The model returns an output.

The program ends.

We can describe it as:

```text
input
  ↓
model
  ↓
output
```

There is no loop.

There is no external action.

There is no observation of a changed environment.

There is no decision about what to do next.

Calling this an "agent" does not buy us much conceptually.

It is a **model invocation**.

That distinction matters because one of the recurring mistakes in agent design is to introduce an elaborate runtime where a single model call would have solved the problem more cheaply, quickly and reliably.

We will return to that point repeatedly throughout this series.

---

## 2. Put a program around the model

Now let us add a little structure.

```python
class Assistant:
    def __init__(self, model):
        self.model = model

    def run(self, task):
        prompt = f"Solve this task:\n\n{task}"
        return self.model(prompt)
```

We now have:

- configuration;
- a reusable object;
- a `run()` method;
- a prompt-building step;
- a model call.

That looks more agent-like.

But the computation is still:

```text
task
 ↓
build prompt
 ↓
model
 ↓
answer
```

The wrapper did not create agency.

It created **software structure**.

That software structure is useful. Real agent runtimes usually need things such as:

- configuration;
- logging;
- model selection;
- prompt loading;
- context passing;
- persistence;
- retries;
- telemetry;
- caching.

But those facilities are infrastructure around the computation.

They are not the core mechanism that makes the system agentic.

This is an important distinction:

> **An agent class is not necessarily an agent loop.**

A class called `Agent` may still just perform one deterministic pipeline of operations and return.

---

## 3. What changes when the system can act?

Suppose our model can choose an operation.

```python
result = llm("Should I search the web or answer directly?")
```

The output might be:

```text
SEARCH
```

Now the program interprets that output:

```python
if result == "SEARCH":
    observation = search_web(query)
else:
    observation = None
```

Something important has changed.

The model output is no longer merely the final answer.

It is being used as a **control signal**.

The program has separated:

```text
reason about action
       ↓
choose action
       ↓
execute action
```

This is much closer to the idea of an agent.

We now have two different kinds of output:

1. **world-facing output** — the final answer or result;
2. **control output** — an instruction that changes what the program does next.

That second category is fundamental.

---

## 4. The smallest useful agent loop

Let us make the structure explicit.

```python
while True:
    observation = observe()
    action = decide(observation)
    result = act(action)

    if finished(result):
        break
```

That gives us the classic loop:

```text
observe
   ↓
decide
   ↓
act
   ↓
observe
   ↓
decide
   ↓
act
   ↓
...
```

This is the core structure we will build on throughout the series.

The model might implement `decide()`.

But the **agent is the loop** that connects decision-making to actions and observations.

The model is one component inside that loop.

This is the same decomposition habit we used throughout Models From First Principles.

There, a "model" turned out to contain smaller models, heads, blocks and operations.

Here, an "agent" turns out to contain:

```text
agent
├── state
├── observations
├── decision mechanism
├── action space
├── executor
├── stopping rule
└── history
```

No magic is required.

---

## 5. Build the smallest agent in Python

Let us create an agent with only two actions:

```text
CALCULATE
FINAL
```

The agent is given a task.

It may either ask a calculator for help or produce the final answer.

```python
from dataclasses import dataclass, field


@dataclass
class AgentState:
    task: str
    history: list[dict] = field(default_factory=list)
    done: bool = False
    final_answer: str | None = None
```

The state is deliberately boring.

That is good.

Now define an action:

```python
@dataclass
class Action:
    name: str
    argument: str
```

Our decision function might ask an LLM for a structured action:

```python
def decide(model, state: AgentState) -> Action:
    prompt = f"""
Task:
{state.task}

History:
{state.history}

Choose exactly one action:

CALCULATE <expression>
FINAL <answer>
"""

    output = model(prompt).strip()

    name, argument = output.split(" ", 1)
    return Action(name=name, argument=argument)
```

Then execute it:

```python
def execute(action: Action):
    if action.name == "CALCULATE":
        return {
            "type": "calculation",
            "value": safe_calculate(action.argument),
        }

    if action.name == "FINAL":
        return {
            "type": "final",
            "value": action.argument,
        }

    return {
        "type": "error",
        "value": f"Unknown action: {action.name}",
    }
```

And finally build the loop:

```python
def run_agent(model, task, max_steps=5):
    state = AgentState(task=task)

    for step in range(max_steps):
        action = decide(model, state)
        observation = execute(action)

        state.history.append({
            "step": step,
            "action": action,
            "observation": observation,
        })

        if observation["type"] == "final":
            state.done = True
            state.final_answer = observation["value"]
            break

    return state
```

That is already enough to expose most of the important pieces.

```text
task
 ↓
state
 ↓
model chooses action
 ↓
executor runs action
 ↓
observation added to state
 ↓
model chooses again
 ↓
...
```

The model did not become more intelligent.

We changed the **computation around it**.

---

## 6. The environment matters

An agent does not act in a vacuum.

The thing receiving actions is usually called the **environment**.

That word can sound more exotic than it is.

For a robot, the environment might literally be the physical world.

For a coding agent, it might be:

```text
filesystem
Git repository
compiler
unit tests
terminal
CI system
```

For a research agent:

```text
search engine
web pages
papers
database
notes
```

For a writing agent:

```text
document
outline
style rules
source material
revision history
```

For a customer-support agent:

```text
conversation
CRM
knowledge base
ticket system
```

The environment is simply the system whose state can be observed and changed.

This gives us a more complete picture:

```text
                  ┌───────────────┐
                  │  environment  │
                  └───────┬───────┘
                          │ observation
                          ▼
                    ┌───────────┐
                    │   agent   │
                    └─────┬─────┘
                          │ action
                          ▼
                  ┌───────────────┐
                  │  environment  │
                  └───────────────┘
```

If the environment never changes and the system never observes new information, then the "agent" may simply be a complicated prompt pipeline.

Sometimes that is fine.

But we should be precise about what mechanism we have actually built.

---

## 7. State is not the same thing as memory

Agents need state.

That does not necessarily mean they need long-term memory.

State is simply the information required to continue the current computation.

For example:

```python
state = {
    "task": task,
    "step": 3,
    "last_action": "run_tests",
    "last_observation": "2 tests failed",
}
```

That is working state.

A more complete state might include:

```python
state = {
    "task": task,
    "plan": plan,
    "history": history,
    "files_changed": files_changed,
    "test_results": test_results,
    "budget_remaining": budget,
}
```

Long-term memory is different.

It asks whether information survives beyond this run and can influence future runs.

We will dedicate a later post to memory.

For now, the important distinction is:

```text
state
= what this run currently knows

memory
= information preserved for later retrieval
```

---

## 8. History changes the next decision

Why keep history at all?

Because an agent should usually avoid making each decision as though nothing happened before it.

Consider:

```text
Step 1
Action: RUN_TESTS
Observation: test_parse_date failed

Step 2
Action: EDIT parse_date()
Observation: file changed

Step 3
Action: RUN_TESTS
Observation: all tests pass
```

Each observation changes what should happen next.

Without state, we repeatedly ask:

```text
What should I do?
```

With state, we ask:

```text
Given what has already happened, what should I do next?
```

That is a much richer computation.

---

## 9. A workflow is not necessarily an agent

Now consider this program:

```python
research = researcher(task)
plan = planner(task, research)
draft = writer(task, plan)
review = critic(draft)
final = reviser(draft, review)
```

This might be sophisticated.

It might call five different models.

It might even use five classes named `ResearchAgent`, `PlannerAgent`, `WriterAgent`, `CriticAgent` and `RevisionAgent`.

But structurally it is still:

```text
A
↓
B
↓
C
↓
D
↓
E
```

The route is predetermined.

The system does not inspect an observation and decide whether B, C, D or E should run next.

That makes it closer to a **workflow**.

A workflow can be excellent engineering.

In many applications it is preferable to a free agent loop because it is:

- predictable;
- easier to test;
- easier to reproduce;
- easier to budget;
- easier to secure.

So this is not a hierarchy where "agent" means better.

It is a distinction in control flow.

---

## 10. The control-flow test

A useful diagnostic is to ask:

> **Who decides what happens next?**

If the answer is:

> the programmer already hard-coded the next step

then we probably have a workflow.

If the answer is:

> the system inspects the current state or observation and selects the next action

then we are moving into agentic control.

Compare these two examples.

### Fixed workflow

```python
research()
plan()
write()
review()
```

### Agentic loop

```python
while not done:
    action = choose_action(state)
    observation = execute(action)
    state = update_state(state, action, observation)
```

That second form is the basic architecture we care about in this series.

---

## 11. The action space defines what the agent can do

The model may be extremely capable.

But the agent can only affect the environment through the actions exposed to it.

Suppose we define:

```python
ACTIONS = {
    "SEARCH": search,
    "READ_FILE": read_file,
    "WRITE_FILE": write_file,
    "RUN_TESTS": run_tests,
    "FINAL": finish,
}
```

Then the agent's effective capabilities are bounded by those operations.

This is valuable for both design and safety.

Instead of giving a model arbitrary code execution, we may expose narrow operations such as:

```text
read_file(path)
search_docs(query)
run_test(test_name)
propose_patch(diff)
```

The action interface becomes a contract between:

```text
model decision
      ↓
agent runtime
      ↓
external system
```

This is one reason tool design matters so much in practical agent systems.

A weak tool interface can make a strong model look incompetent.

A precise tool interface can make a modest model surprisingly effective.

---

## 12. Actions should be structured

We could ask a model to emit arbitrary text:

```text
I think maybe you should search for PyTorch documentation.
```

Then our program has to guess what that means.

A better design is:

```json
{
  "action": "search",
  "query": "PyTorch autograd documentation"
}
```

Now the boundary is explicit.

```python
def dispatch(action):
    if action["action"] == "search":
        return search(action["query"])
```

The exact serialization could be JSON, a typed object, a function call or another schema.

The important concept is **structured control**.

The model proposes an action inside a constrained grammar.

The runtime validates it.

Only then is anything executed.

---

## 13. Never confuse proposing an action with executing it

This separation is critical:

```text
MODEL
  ↓
proposes action
  ↓
VALIDATOR
  ↓
checks action
  ↓
EXECUTOR
  ↓
changes environment
```

The model should not automatically be trusted merely because it produced something that looks executable.

For example:

```python
action = model_decision(state)

validated = validate(action)
if not validated.ok:
    return validated.error

observation = execute(validated.action)
```

This gives us a place to enforce:

- allowed tools;
- argument schemas;
- path restrictions;
- timeouts;
- budgets;
- permissions;
- confirmation boundaries;
- sandboxing.

Agent design is therefore not only a prompting problem.

It is a software architecture problem.

---

## 14. The model is a policy over actions

In the previous series we discussed explicit policy heads.

The same idea appears here at a different level.

Given current state `s`, the agent needs to choose an action `a`.

Conceptually:

```text
state
  ↓
policy
  ↓
action
```

The policy might be:

- an LLM;
- a small learned classifier;
- deterministic rules;
- a search policy;
- a mixture of those things.

This is useful because it breaks the assumption that every decision inside an agent must be made by a frontier language model.

For example:

```python
def choose_action(state):
    if state["tests_failed"]:
        return "DEBUG"

    if not state["tests_run"]:
        return "RUN_TESTS"

    return llm_choose_action(state)
```

That is still an agent loop.

Some control is deterministic.

Some is learned.

This hybrid approach is often better than asking the model to rediscover obvious control rules every time.

---

## 15. Agents need stopping conditions

Any loop needs a way to stop.

This seems trivial until an LLM repeatedly decides that one more search, one more rewrite or one more attempt might help.

A minimal stopping rule might be:

```python
if action.name == "FINAL":
    stop()
```

But practical systems usually need more.

```python
if step >= max_steps:
    stop("step budget exhausted")

if cost >= max_cost:
    stop("cost budget exhausted")

if elapsed >= timeout:
    stop("time budget exhausted")

if verified_success:
    stop("goal achieved")
```

This gives us a general form:

```text
continue while
    goal not satisfied
AND step budget remains
AND time budget remains
AND cost budget remains
AND safety constraints remain satisfied
```

Without explicit stopping conditions, "autonomy" can simply become uncontrolled iteration.

---

## 16. Success should be observable when possible

Suppose an agent is asked:

```text
Fix the failing unit test.
```

How does it know when the task is complete?

One weak answer is:

```text
The model thinks the code looks correct.
```

A stronger answer is:

```text
The previously failing test passes.
```

Even stronger:

```text
The failing test passes,
the complete test suite passes,
and no forbidden files changed.
```

The more the environment exposes measurable success signals, the less we need to rely on self-assessment.

This will become a major theme later in the series when we build verification-driven agents.

For now, remember:

> **An agent loop becomes much stronger when success can be observed rather than narrated.**

---

## 17. Failure is an observation too

Suppose an action fails:

```text
READ_FILE /missing/config.yaml
```

The result might be:

```json
{
  "ok": false,
  "error": "FileNotFoundError"
}
```

A useful agent does not hide that failure.

It feeds it back into the loop:

```text
action
 ↓
error
 ↓
observation
 ↓
new decision
```

Now the agent may choose:

```text
LIST_DIRECTORY
```

then discover the correct path and continue.

This is one of the most concrete differences between a one-shot model call and an agent loop.

A model call fails when the answer is wrong.

An agent may be able to **observe the failure and recover**.

---

## 18. Retries are not the same thing as agency

A simple retry loop looks like:

```python
for _ in range(3):
    try:
        return call_api()
    except TimeoutError:
        pass
```

That is useful resilience.

But the decision is predetermined:

```text
if timeout → retry same thing
```

An agentic recovery loop might instead choose among:

```text
retry
change query
use different tool
inspect error
change plan
ask for help
stop
```

So we should distinguish:

```text
retry policy
```

from:

```text
adaptive action selection
```

Again, neither is inherently better.

The simplest mechanism that solves the problem is usually the right one.

---

## 19. Context is the agent's working world model

A practical agent typically passes a context object through the loop.

```python
context = {
    "goal": goal,
    "history": [],
    "observations": [],
    "artifacts": {},
    "step": 0,
}
```

Each component reads what it needs and writes what it produces.

For example:

```python
context["plan"] = make_plan(context)
context["search_results"] = search(context["query"])
context["test_results"] = run_tests()
```

This is one reason a shared context dictionary appears so often in real agent frameworks.

It functions as a lightweight state bus.

But it can also become dangerous.

If every component can read and mutate every key, then after enough growth we get:

```text
mystery state
+ hidden dependencies
+ accidental overwrites
+ impossible debugging
```

So even something as simple as a context object eventually needs contracts.

We will revisit that as the series grows.

---

## 20. The agent runtime is not the intelligence

Real systems quickly accumulate infrastructure:

```text
BaseAgent
PromptLoader
ModelClient
MemoryStore
ScoringService
Logger
ToolRegistry
Context
RetryPolicy
Telemetry
```

That infrastructure matters enormously.

But we should keep the conceptual layers separate.

```text
AGENT TECHNIQUE
    what computation are we performing?

RUNTIME
    how do we execute that computation reliably?

MODEL
    what learned function participates in the computation?
```

This separation keeps us from attributing capability to the wrong layer.

If a system improves after adding best-of-N generation, the improvement may come from **more sampled computation**, not from a better model.

If it improves after adding retrieval, the improvement may come from **better information**, not from better reasoning.

If it improves after adding tests, the improvement may come from **external verification**, not self-reflection.

These distinctions are exactly what we want to understand in this series.

---

## 21. A useful taxonomy: model, workflow, agent

Let us create a simple working taxonomy.

### Model call

```text
input → model → output
```

Example:

```python
summary = llm(document)
```

### Workflow

```text
A → B → C → D
```

The route is predetermined by code.

Example:

```python
research = research_step(task)
plan = plan_step(research)
draft = draft_step(plan)
review = review_step(draft)
```

### Agent

```text
state
 ↓
choose next action
 ↓
execute
 ↓
observe
 ↓
update state
 ↓
choose next action
```

The route can change based on observations.

This taxonomy is deliberately pragmatic rather than philosophical.

It gives us useful engineering questions.

---

## 22. There is a spectrum, not a binary switch

Real systems are often hybrids.

Consider:

```text
fixed preprocessing
      ↓
agent loop
      ↓
fixed verification pipeline
```

Or:

```text
planner
  ↓
fixed list of plan steps
  ↓
agentic recovery only when a step fails
```

Or:

```text
workflow
  ↓
router chooses one of three branches
  ↓
workflow continues
```

So it is not useful to argue endlessly about whether a system "really counts" as an agent.

What matters more is identifying exactly where adaptive control exists.

Ask:

```text
What state is observed?
What decisions are adaptive?
What actions are available?
What changes in the environment?
What feedback comes back?
What causes the loop to stop?
```

Those questions tell us far more than the label.

---

## 23. The agent loop can be deterministic

We often associate agents with LLMs because current AI systems use them heavily.

But nothing about the loop requires a language model.

```python
def decide(state):
    if state.temperature > 25:
        return Action("TURN_ON_FAN", "")
    return Action("WAIT", "")
```

This is an agent in the broad computational sense.

The policy is deterministic.

Why does that matter for our series?

Because it prevents us from accidentally teaching:

```text
agent = LLM + prompt
```

A better formulation is:

```text
agent = state + policy + actions + feedback loop
```

An LLM is one possible policy implementation.

---

## 24. LLMs are useful because the action policy can generalize

A deterministic policy is excellent when we can enumerate the rules.

But suppose the agent sees:

```text
The build failed because generated protobuf bindings are stale.
```

The correct next action may require interpreting a novel error and relating it to repository structure.

A language model can map rich observations to actions without us writing an explicit branch for every possible sentence.

Conceptually:

```text
unstructured observation
          ↓
         LLM
          ↓
 structured action
```

That is where LLMs become extremely useful inside agent loops.

They act as flexible policies over complicated state.

But flexibility brings uncertainty.

So we surround them with contracts, tools, validators and verification.

---

## 25. The first important design trade-off: freedom vs control

Suppose an agent can choose any shell command:

```text
RUN_SHELL <anything>
```

That gives it enormous flexibility.

It also makes validation, reproducibility and safety much harder.

Now compare:

```text
READ_FILE(path)
WRITE_PATCH(diff)
RUN_TEST(name)
SEARCH_CODE(query)
```

The action space is narrower.

But each action has clearer semantics.

This gives us a recurring trade-off:

```text
broad action space
    ↑ flexibility
    ↓ controllability

narrow action space
    ↓ flexibility
    ↑ controllability
```

Good agent systems usually do not maximize autonomy blindly.

They expose the smallest useful action space for the task.

---

## 26. The second trade-off: autonomy vs determinism

Consider two systems.

### System A

```text
research
 ↓
write
 ↓
review
```

### System B

```text
agent decides:
research more?
write?
review?
search?
restart?
finish?
```

System B has greater autonomy.

But it also has more possible trajectories.

That means:

- harder testing;
- harder reproduction;
- more variable latency;
- more variable token cost;
- more failure modes.

Autonomy is therefore not free capability.

It is an architectural trade-off.

---

## 27. The third trade-off: more inference vs better inference

One of the themes of the advanced agent series later will be that many agent techniques increase capability by spending more inference-time computation.

For example:

```text
one answer
```

becomes:

```text
8 answers
+ scoring
+ revision
```

Or:

```text
one reasoning trajectory
```

becomes:

```text
search tree of 50 trajectories
```

The underlying model may be identical.

This matters because when an agent system improves, we should ask:

> Did the architecture improve the quality of computation, or did we simply buy more samples and more tokens?

Both can be useful.

But they are different claims.

---

## 28. A minimal reusable agent abstraction

Let us now write a cleaner interface.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Observation:
    kind: str
    data: Any


@dataclass
class Action:
    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class State:
    goal: str
    history: list[tuple[Action, Observation]] = field(default_factory=list)
    step: int = 0
    done: bool = False


class Agent(ABC):
    @abstractmethod
    def decide(self, state: State) -> Action:
        raise NotImplementedError
```

The runtime owns execution:

```python
class AgentRuntime:
    def __init__(self, agent, tools, max_steps=10):
        self.agent = agent
        self.tools = tools
        self.max_steps = max_steps

    def execute(self, action: Action) -> Observation:
        if action.name == "FINAL":
            return Observation("final", action.args["answer"])

        tool = self.tools.get(action.name)
        if tool is None:
            return Observation("error", f"Unknown action {action.name}")

        try:
            value = tool(**action.args)
            return Observation("tool_result", value)
        except Exception as exc:
            return Observation("error", repr(exc))

    def run(self, goal: str) -> State:
        state = State(goal=goal)

        while not state.done and state.step < self.max_steps:
            action = self.agent.decide(state)
            observation = self.execute(action)

            state.history.append((action, observation))
            state.step += 1

            if observation.kind == "final":
                state.done = True

        return state
```

Notice what happened.

The runtime itself does not care whether `decide()` uses:

- an LLM;
- rules;
- a small neural model;
- a search algorithm;
- several experts.

That is a powerful separation.

---

## 29. Now put an LLM inside the policy

```python
import json


class LLMAgent(Agent):
    def __init__(self, model):
        self.model = model

    def decide(self, state: State) -> Action:
        history = [
            {
                "action": action.name,
                "args": action.args,
                "observation": observation.data,
            }
            for action, observation in state.history
        ]

        prompt = f"""
Goal:
{state.goal}

History:
{json.dumps(history, indent=2)}

Choose the next action as JSON.

Allowed actions:
- SEARCH {{"query": "..."}}
- CALCULATE {{"expression": "..."}}
- FINAL {{"answer": "..."}}
"""

        raw = self.model(prompt)
        data = json.loads(raw)

        return Action(
            name=data["action"],
            args=data.get("args", {}),
        )
```

Now we have a complete conceptual agent:

```text
goal
 ↓
state
 ↓
LLM policy
 ↓
structured action
 ↓
runtime validation / dispatch
 ↓
tool or environment
 ↓
observation
 ↓
state update
 ↓
repeat
```

Everything in the later series is an extension of this diagram.

---

## 30. Where do prompts fit?

Prompts matter.

But prompts are not the whole architecture.

A prompt might define:

- role;
- task;
- action schema;
- constraints;
- available tools;
- examples;
- output format.

That is the policy interface presented to the model.

But changing this:

```text
You are a helpful coding agent.
```

into this:

```text
You are an expert autonomous software-engineering agent.
```

has not added a tool, a verifier, a search tree, memory or feedback.

Agent capability comes from the **system computation**, not from agent-like adjectives in the prompt.

---

## 31. Where do models from the previous series fit?

This is where the learning path joins together.

Suppose our agent generates five candidate actions.

We need to choose one.

We could ask another LLM.

Or we could use a learned scorer.

```text
state
 ↓
generate candidate actions
 ├→ A
 ├→ B
 ├→ C
 ├→ D
 └→ E
      ↓
   scorer
      ↓
  best action
```

Now MR.Q suddenly has a concrete role.

A multi-head architecture such as EBT or SICQL might provide several signals.

A recursive model such as Tiny might spend extra computation on hard candidates.

An HRM-style model might be evaluated as a more expensive decision layer.

The important point is that the **model series and agent series are different layers of the same system**.

```text
PyTorch
 ↓
models
 ↓
agent policies / scorers
 ↓
agent runtime
 ↓
environment
```

---

## 32. Caching is an agent-runtime optimization, not a reasoning technique

Suppose an agent repeatedly sees the same prompt or equivalent state.

We could call the model every time.

Or we could reuse a previous result.

```python
key = hash_prompt(prompt)

if key in cache:
    return cache[key]

result = model(prompt)
cache[key] = result
return result
```

This can massively reduce:

- latency;
- token cost;
- local inference time.

But again, we should classify it correctly.

Caching changes **execution economics**.

It does not necessarily improve reasoning quality.

This is exactly why separating runtime from agent technique is valuable.

---

## 33. Logging is part of the architecture if you want to understand failures

Agent loops are stochastic programs with branching control flow.

If we log only the final answer, debugging becomes painful.

A useful trace should contain at least:

```text
run id
step
state summary
action proposed
action validated
action executed
observation
latency
cost
termination reason
```

For example:

```json
{
  "step": 4,
  "action": "RUN_TESTS",
  "args": {"target": "tests/test_parser.py"},
  "observation": {
    "passed": 17,
    "failed": 1
  }
}
```

This is not glamorous agent research.

It is what makes agent systems debuggable.

And as systems become more agentic, traceability becomes more—not less—important.

---

## 34. The agent should know why it stopped

A final state should record a termination reason.

```python
state.termination = "verified_success"
```

Possible values might include:

```text
verified_success
model_finished
step_budget_exhausted
timeout
cost_budget_exhausted
invalid_action
permission_denied
unrecoverable_error
```

Why bother?

Because these are not equivalent outcomes.

A system that returns an answer because tests passed is different from one that returns because it ran out of steps.

If both are simply labelled `completed`, we destroy useful information.

---

## 35. Agents introduce new failure modes

A model can hallucinate.

An agent can hallucinate **and then act on the hallucination**.

That changes the risk profile.

Common agent-specific failure modes include:

### Repetition

```text
search
search
search
search
```

### Thrashing

```text
edit A
undo A
edit A differently
undo again
```

### Goal drift

The agent gradually optimizes something adjacent to the original task.

### Tool misuse

The selected action is semantically wrong even though the tool call is syntactically valid.

### Premature completion

The model declares success without verifying it.

### Budget blindness

The agent spends more time or tokens chasing diminishing improvements.

### State corruption

Later decisions depend on stale or incorrectly updated context.

These are system-level failures.

A better base model may reduce some of them, but architecture matters too.

---

## 36. A tiny loop can already outperform a larger prompt

Imagine a coding task.

### One-shot approach

```text
Read this error and give me the fixed code.
```

### Agent loop

```text
inspect error
 ↓
read relevant file
 ↓
propose patch
 ↓
run test
 ↓
observe failure
 ↓
inspect new error
 ↓
revise patch
 ↓
run test
```

The same underlying model may perform much better in the second system because it receives **fresh evidence after each action**.

This is one of the central ideas of agentic computation.

We do not require the model to predict the entire future correctly in one shot.

We allow it to interact with reality.

---

## 37. But loops can also make things worse

More steps mean more opportunities to fail.

Suppose each independently risky decision succeeds 95% of the time.

A twenty-decision process does not magically become more reliable because it has more reasoning steps.

The exact probabilities in real agents are not independent, but the intuition matters:

```text
more decisions
→ more opportunities for recovery
AND
→ more opportunities for error
```

So we should never equate:

```text
more agent steps
```

with:

```text
better agent
```

The loop should exist because the environment can provide useful feedback.

---

## 38. When should you use a single call instead?

Use a single model call when:

- the task is self-contained;
- the required information is already in context;
- there is no useful external feedback;
- one output is sufficient;
- latency matters;
- determinism matters;
- failure can be handled by the caller.

Examples:

```text
rewrite this paragraph
classify this message
extract these fields
summarize this document
translate this text
```

Do not build an autonomous loop merely because agents are fashionable.

---

## 39. When is a workflow enough?

Use a fixed workflow when the steps are known in advance.

For example:

```text
transcribe audio
 ↓
extract entities
 ↓
summarize
 ↓
format report
```

There is no strong reason for a model to rediscover this sequence on every run.

Hard-code it.

You gain:

- predictable execution;
- easier tests;
- clearer ownership;
- simpler failure recovery.

---

## 40. When does an agent loop become useful?

Use adaptive control when the correct next action genuinely depends on what happens during execution.

Examples:

### Debugging

```text
run test
 ↓
inspect actual failure
 ↓
choose what to inspect next
```

### Research

```text
search
 ↓
read results
 ↓
decide whether evidence is sufficient
 ↓
search differently if needed
```

### Repository work

```text
inspect repository
 ↓
decide relevant files
 ↓
change code
 ↓
run validation
 ↓
respond to failures
```

### Investigation

```text
form hypothesis
 ↓
collect evidence
 ↓
update hypothesis
 ↓
choose next experiment
```

The common property is **information arrives during the task that should change future actions**.

That is where the loop earns its cost.

---

## 41. A practical definition

For this series, we will use the following working definition:

> **An agent is a stateful system that selects actions, executes them against an environment, observes the results, and uses those observations to influence subsequent decisions.**

This definition is intentionally engineering-focused.

It does not require consciousness.

It does not require long-term memory.

It does not require an LLM.

It does not require unrestricted autonomy.

It gives us a concrete architecture to build and test.

---

## 42. The anatomy of an agent

From now on, when we inspect an agent system, we can decompose it into these questions.

### Goal

What is the system trying to accomplish?

### State

What information persists during the run?

### Observation

What can the system learn from the environment?

### Policy

How is the next action selected?

### Action space

What operations are allowed?

### Executor

What actually performs the action?

### Feedback

How does the result return to the decision system?

### Termination

What stops the loop?

### Verification

How do we know whether the goal was achieved?

### Trace

What evidence do we preserve about the trajectory?

That checklist will be reused throughout the rest of the series.

---

## 43. The same agent can use different policies

Because the runtime and policy are separated, we can perform a useful experiment.

Keep everything constant:

```text
tools
state
budget
environment
verification
```

Then swap only the decision mechanism.

```text
rules
vs
small local model
vs
frontier LLM
vs
search policy
```

Now we can ask whether a more expensive policy actually improves task completion.

This is exactly the kind of controlled comparison we used in the Models From First Principles series.

---

## 44. The same model can support different agent techniques

We can also hold the model constant and change the surrounding algorithm.

For example:

```text
same model
   ├→ one-shot
   ├→ best-of-N
   ├→ critique/revise
   ├→ planner/executor
   ├→ tool loop
   └→ search tree
```

Now we can measure what the **agent technique** contributes independently of model improvements.

This separation will become especially important once we reach advanced agents.

---

## 45. Do not benchmark agents only by final quality

Suppose two agents both solve 80% of tasks.

Agent A uses:

```text
2 model calls
1 tool call
3 seconds
```

Agent B uses:

```text
47 model calls
19 tool calls
2 minutes
```

Those are not equivalent systems.

Useful agent metrics include:

```text
success rate
verified success rate
steps per task
model calls per task
tool calls per task
tokens per task
wall-clock latency
cost per successful task
recovery rate after failure
invalid-action rate
premature-stop rate
```

The denominator **per successful task** is especially important.

A cheap agent that fails constantly may not be cheap at all.

---

## 46. The trajectory is part of the result

For a simple model call, the result is usually the output.

For an agent, we often need both:

```text
final result
+
trajectory
```

For example:

```json
{
  "result": "patch applied and tests pass",
  "trajectory": [
    "read parser.py",
    "read failing test",
    "edit parser.py",
    "run test",
    "observe failure",
    "edit parser.py",
    "run full suite"
  ]
}
```

Why preserve the trajectory?

Because it enables:

- debugging;
- auditing;
- replay;
- cost analysis;
- failure classification;
- training data;
- future strategy learning.

Later, those traces can themselves become memory or evidence.

---

## 47. A simple experiment: one-shot vs loop

Before building sophisticated agents, run a small controlled experiment.

Choose tasks with external verification.

For example, ten small Python bugs with unit tests.

### Condition A

```text
one prompt
one model call
produce patch
```

### Condition B

```text
same model
same task
agent can:
- read files
- edit patch
- run tests
- retry up to 5 steps
```

Measure:

```text
verified success
model calls
wall time
tokens
number of edits
number of recovered failures
```

This tells us whether the loop itself adds useful capability for that task distribution.

That is much stronger than saying:

> agents are better because they are agentic.

---

## 48. Another experiment: fixed workflow vs adaptive routing

Suppose every task could use:

```text
search → plan → answer → review
```

Compare that fixed workflow against an agent that chooses whether each stage is necessary.

The adaptive version might skip research for trivial questions or trigger a second review only when confidence is low.

Measure:

```text
quality
latency
cost
steps
```

If adaptive routing gives the same quality for half the cost, agency earned its complexity.

If it gives the same route almost every time, the workflow was probably enough.

---

## 49. Real systems usually combine deterministic and agentic control

A serious system might look like:

```text
validate input             deterministic
      ↓
retrieve repository state   deterministic
      ↓
choose investigation action agentic
      ↓
execute tool                deterministic
      ↓
validate tool result         deterministic
      ↓
choose next action           agentic
      ↓
run final tests              deterministic
      ↓
accept only if tests pass    deterministic
```

This pattern is extremely important.

We do not have to choose between:

```text
fully scripted
```

and:

```text
fully autonomous
```

The strongest architecture may put adaptive decisions only where uncertainty genuinely exists.

---

## 50. Autonomy should be earned one boundary at a time

A useful engineering progression is:

```text
model proposes text
 ↓
model proposes structured action
 ↓
program validates action
 ↓
program executes narrow tool
 ↓
model observes result
 ↓
model chooses another action
```

Then, only if evidence supports it, expand:

```text
more tools
more steps
more write permissions
more planning freedom
more search depth
```

This is safer and easier to debug than beginning with arbitrary shell access and a prompt saying "complete the task autonomously."

---

## 51. What Stephanie teaches us without making this a Stephanie series

The real Stephanie agent runtime contains many of the infrastructural pieces we have just separated conceptually:

- a shared base agent;
- model configuration;
- synchronous and asynchronous model calls;
- prompt loading and persistence;
- context propagation;
- prompt/result caching;
- scoring hooks;
- logging;
- an abstract `run()` contract.

Those are useful real-world implementation examples.

But they are not the curriculum.

The curriculum is the underlying technique.

So throughout this series we will do the same thing we did with the model series:

```text
real implementation
      ↓
extract mechanism
      ↓
rebuild independently
      ↓
understand trade-offs
      ↓
test contribution
```

That keeps the material useful even if the reader never installs Stephanie.

---

## 52. What comes next

This introductory post has deliberately kept the agent primitive small.

```text
state
 ↓
choose action
 ↓
execute
 ↓
observe
 ↓
repeat
```

Now we can start adding techniques one at a time.

The planned progression is roughly:

```text
00  What Is an Agent, Really?

01  The Simplest Agent:
    Prompt → Model → Structured Action

02  Best-of-N:
    Generate Several Candidates and Select One

03  Critique and Revise:
    Let the System Improve Its Own Draft

04  Planning:
    Separate Deciding What to Do From Doing It

05  Act → Observe → Correct:
    Build a Real Feedback Loop

06  Tool-Using Agents:
    Give the Model a Controlled Action Space

07  Memory:
    Working State, Retrieval and Reusing Past Work

08  Search:
    Explore More Than One Trajectory

09  Verification:
    Use Reality, Tests and Measurements as Feedback
```

We will stop the first series there.

Then **Advanced Agents From First Principles** can take over with techniques such as:

```text
self-consistency
tree of thought
beam search
MCTS
evolutionary search
mixture of experts
multi-agent debate
adaptive routing
self-tuning systems
```

That separation is deliberate.

First learn the loop.

Then learn how to make the loop search.

---

## 53. The entire learning ladder

We can now see the larger structure.

### Level 1 — PyTorch

```text
tensor
 ↓
autograd
 ↓
module
 ↓
attention
 ↓
transformer
 ↓
language model
```

### Level 2 — Models

```text
embeddings
 ↓
pair scorer
 ↓
Q / V / policy
 ↓
modular heads
 ↓
recurrence
 ↓
hierarchical recurrence
 ↓
recursive models
```

### Level 3 — Agents

```text
model call
 ↓
state
 ↓
action
 ↓
environment
 ↓
observation
 ↓
feedback loop
 ↓
tools
 ↓
memory
 ↓
verification
```

### Level 4 — Advanced agents

```text
multiple trajectories
 ↓
search
 ↓
experts
 ↓
routing
 ↓
coordination
 ↓
adaptation
```

Each level is built from the previous one.

That is the point of doing this from first principles.

---

## 54. The central rule for this series

There is one rule I want to carry through every post:

> **Do not add an agent mechanism because it sounds more intelligent. Add it because you can identify the failure it is supposed to fix and measure whether it fixes it.**

If one model call solves the task, use one model call.

If a fixed workflow solves it, use a fixed workflow.

If fresh observations genuinely need to change the next action, introduce an agent loop.

If the loop still fails because one trajectory is brittle, then later we can introduce search.

The progression should always be:

```text
observe failure
      ↓
identify missing mechanism
      ↓
add smallest useful mechanism
      ↓
measure again
```

That is how we keep agents understandable.

And that is where we will start in the next post: by building the simplest structured-action agent we can possibly make.
