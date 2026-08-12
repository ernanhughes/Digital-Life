# Stage 8 — Does the Effect Survive Modest Parameter Change?

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
