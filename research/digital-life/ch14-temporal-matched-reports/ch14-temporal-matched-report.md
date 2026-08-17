# Chapter 14 — Matched-Distribution Temporal Experiment

## Question

If source processes contain **exactly the same values** but arrange those values
differently in time, can final Digital Crystal v1 morphology recover the temporal
organization?

## Design

- Frozen model: `digital-crystal-v1-frozen`
- Temporal classes: random, block, alternating, smooth, burst, periodic
- Replicates: **10**
- Crystals: **60**
- Steps per crystal: **72**
- Exact multiset validation: **True**
- Train/test split by matched-value replicate group: **True**
- Cached runs reused: **0/60**

The group split is critical: all six orderings created from one base multiset
remain entirely in train or entirely in test. There is no matched-multiset leakage.

## Held-out classification

Six-way chance: **0.167**

- Random forest: **0.111**
- Logistic regression: **0.111**

## Permutation-label null

- Repeats: **30**
- Mean RF accuracy: **0.133**
- Std: **0.077**
- 95th percentile: **0.222**
- Maximum observed null accuracy: **0.333**

## Verdict

**`TEMPORAL_ORGANIZATION_NOT_RECOVERABLE`**

> With the Digital Crystal v1 growth rule frozen and input value distributions exactly matched, this experiment did not establish recoverable information about temporal organization in final morphology.

## Interpretation

A positive result would strengthen the Chapter 14 claim from
"morphology carries source-family information" to the narrower but stronger
claim that morphology can retain information about temporal organization even
when source-value distributions are exactly matched.

A negative result is equally useful: it would indicate that Digital Crystal v1
primarily encodes distributional/statistical characteristics of forcing rather
than temporal order, giving the next state/history chapter a concrete missing
capability to solve.

## Figures

- `static\images\books\digital-life\ch14-09-matched-temporal-signals.png`
- `static\images\books\digital-life\ch14-09-matched-temporal-crystals.png`
- `static\images\books\digital-life\ch14-09-matched-temporal-confusion.png`
- `static\images\books\digital-life\ch14-09-matched-temporal-accuracy.png`
