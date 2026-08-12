# Chapter 14 — Digital Crystal: Full Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1",
  "profile": "full",
  "profile_config": {
    "runs_per_class": 100,
    "steps": 72,
    "max_radius": 44,
    "robustness_runs": 24,
    "robustness_levels": [
      0.75,
      0.85,
      0.95,
      1.0,
      1.05,
      1.15,
      1.25
    ]
  },
  "seed": 20260811,
  "database": "research\\digital-life\\ch14-digital-crystal.sqlite3",
  "images": "static\\images\\books\\digital-life",
  "reports": "research\\digital-life\\ch14-reports",
  "started_at_unix": 1786475511.170469,
  "finished_at_unix": 1786475997.0099638,
  "final_verdict": "PARTIALLY_SUPPORTED"
}
```

## Stage 1 — Baseline Crystal

The generalized harness first runs with a constant zero-valued environment.

- Final occupied cells: **5924**
- Maximum hex radius reached: **44**
- Boundary edge count: **552**
- Cached run: **False**

Interpretation: this is only a plumbing check. The generalized model must still
produce a coherent growing structure before source-dependent experiments mean
anything.

Figure: `static\images\books\digital-life\ch14-01-baseline.png`

## Stage 2 — Different Sources, Same Rule

Generated **600** crystals across six source families with one fixed
local-growth rule.

Counts: `{'constant': 100, 'sine': 100, 'square': 100, 'saw': 100, 'white_noise': 100, 'random_walk': 100}`

Cached runs reused: **0/600**

At this stage visual differences are only hypotheses. They are not yet evidence
that source information survives in morphology.

Figures:
- `static\images\books\digital-life\ch14-02-source-gallery.png`
- `static\images\books\digital-life\ch14-02-source-signals.png`

## Stage 3 — Same-Mean Control

All varying source families are centered to approximately zero mean, while the
constant control is exactly zero.

Standardized morphology-centroid distances from the constant control:

```json
{
  "sine": 4.451706629124484,
  "square": 13.822931715214354,
  "saw": 2.444362701759997,
  "white_noise": 2.3999727265983846,
  "random_walk": 1.3963110150395102
}
```

These distances are descriptive only. They ask whether time variation leaves a
morphological difference beyond the mean input level. Classification and
temporal-order controls provide the stronger tests later.

## Stage 4 — Destroy Temporal Order

For each nonconstant source, the exact sampled values are shuffled before
growth. This preserves the value distribution while destroying temporal order.

Standardized morphology-centroid shifts, ordered vs shuffled:

```json
{
  "sine": 0.48957346226750753,
  "square": 1.6077134021692885,
  "saw": 0.3744639997402444,
  "white_noise": 0.27005595279400363,
  "random_walk": 0.24750345227751006
}
```

Cached shuffled runs reused: **0/600**

A nonzero descriptive shift is not enough by itself. Stage 7 asks whether
ordered and shuffled crystals can actually be distinguished on held-out runs.

## Stage 5 — Stop Trusting the Pictures

Measured **42** morphology features per final crystal.

Feature set includes:
- area and perimeter
- compactness and roughness
- bounding-box aspect
- centroid offset
- radial statistics/profile
- angular profile
- six-fold angular harmonic
- boundary-radius variation

The measurements intentionally exclude the original signal values.

Figure: `static\images\books\digital-life\ch14-05-morphology-metrics.png`

Pairwise standardized class-centroid distances are saved in
`stage-05-feature-distances.json`.

## Stage 6 — Can We Recover the Source?

Six-way chance accuracy is **0.167**.

Held-out results:
- Random forest: **0.522**
- Logistic regression: **0.539**

Interpretation rule decided in advance:
source recovery supports the working hypothesis only if held-out performance is
materially above chance across more than one classifier and later robustness
checks do not immediately destroy it.

Figures:
- `static\images\books\digital-life\ch14-06-source-confusion.png`
- `static\images\books\digital-life\ch14-06-source-accuracy.png`

## Stage 7 — Does Temporal Order Survive?

Binary chance accuracy is **0.500**.

Held-out ordered-vs-shuffled results:
- Random forest: **0.513**
- Logistic regression: **0.517**

This is the stronger control because ordered and shuffled cases contain the
same source values but in different temporal order.

Figures:
- `static\images\books\digital-life\ch14-07-order-confusion.png`
- `static\images\books\digital-life\ch14-07-order-accuracy.png`

## Stage 8 — Does the Effect Survive Modest Parameter Change?

The forcing amplitude is varied while the local growth rule remains otherwise
unchanged.

```json
{
  "0.75": {
    "random_forest_accuracy": 0.3409090909090909,
    "logistic_accuracy": 0.3409090909090909,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "0.85": {
    "random_forest_accuracy": 0.4318181818181818,
    "logistic_accuracy": 0.4318181818181818,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "0.95": {
    "random_forest_accuracy": 0.5,
    "logistic_accuracy": 0.5,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "1.00": {
    "random_forest_accuracy": 0.5227272727272727,
    "logistic_accuracy": 0.45454545454545453,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "1.05": {
    "random_forest_accuracy": 0.5227272727272727,
    "logistic_accuracy": 0.5454545454545454,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "1.15": {
    "random_forest_accuracy": 0.6363636363636364,
    "logistic_accuracy": 0.5681818181818182,
    "chance": 0.16666666666666666,
    "n_test": 44
  },
  "1.25": {
    "random_forest_accuracy": 0.4318181818181818,
    "logistic_accuracy": 0.4772727272727273,
    "chance": 0.16666666666666666,
    "n_test": 44
  }
}
```

Figure: `static\images\books\digital-life\ch14-08-robustness.png`

This is not a universal robustness proof. It only asks whether source recovery
is a knife-edge effect of one forcing amplitude.

## Stage 9 — Experimental Verdict

**Verdict: `PARTIALLY_SUPPORTED`**

> Within this model, source family is recoverable from final morphology, but stronger temporal-order and/or robustness tests did not all survive. The Digital Crystal idea remains useful but the stronger history-encoding interpretation is not yet earned.

Primary held-out source recovery:
- chance: **0.167**
- random forest: **0.522**
- logistic regression: **0.539**

Temporal-order recovery:
- chance: **0.500**
- random forest: **0.513**
- logistic regression: **0.517**

Robustness forcing levels above the predeclared RF margin:
**7/7**

The verdict logic is intentionally simple and printed in the script. It is a
book-development gate, not a formal statistical theorem.
