# Stage 0 — Canonical Sequential RNG vs Counterfactual CRN

```json
{
  "sequential_exact": true,
  "crn_exact": true,
  "canonical_runner": "sequential RNG over sorted(frontier)",
  "counterfactual_runner": "cell-keyed CRN U(seed, step, q, r)",
  "canonical_substrate_modified": false,
  "validation_groups_per_runner": 48,
  "marginal_feature_test": {
    "energy_distance": 0.2060020932718798,
    "p_value": 0.9301397205588823,
    "null_q95": 0.38643619995954437,
    "interpretation": "Failure to reject is compatibility evidence only; it does not prove equality of the two stochastic laws."
  },
  "population": {
    "sequential": {
      "n": 48,
      "mean": 1430.875,
      "median": 1431.5,
      "std": 99.73791175709799,
      "ci95_low": 1404.0057291666667,
      "ci95_high": 1461.825,
      "min": 1079.0,
      "max": 1652.0
    },
    "crn": {
      "n": 48,
      "mean": 1423.5,
      "median": 1428.0,
      "std": 92.0740191367793,
      "ci95_low": 1396.9333333333334,
      "ci95_high": 1448.6046875,
      "min": 1232.0,
      "max": 1598.0
    }
  }
}
```
