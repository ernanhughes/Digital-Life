# Stage 4 — Late Ablation Under Exact Matched Copy Quantity

```json
{
  "late_ablation_step": 14,
  "followup_steps": 4,
  "results": {
    "interior_biased": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference": {
        "n": 48,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 2000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      }
    },
    "random_matched": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.08333333333333333,
        "median": 0.0,
        "std": 0.44876373392787533,
        "ci95_low": 0.0,
        "ci95_high": 0.25,
        "min": 0.0,
        "max": 3.0
      },
      "pathwise_symmetric_difference": {
        "n": 48,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 2000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      }
    },
    "surface_biased": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.3541666666666667,
        "median": 0.0,
        "std": 0.7770023416238131,
        "ci95_low": 0.14583333333333334,
        "ci95_high": 0.5833333333333334,
        "min": 0.0,
        "max": 4.0
      },
      "pathwise_symmetric_difference": {
        "n": 48,
        "mean": 1.71609006040637e-05,
        "median": 0.0,
        "std": 0.00011764920717327438,
        "ci95_low": 0.0,
        "ci95_high": 5.148270181219111e-05,
        "min": 0.0,
        "max": 0.0008237232289950577
      },
      "paired_ridge_test": {
        "statistic": 0.021057249396797456,
        "p_value": 1.0,
        "permutations": 2000,
        "null_mean": 0.021057249396797498,
        "null_q95": 0.02105724939679755,
        "null_q99": 0.02105724939679755
      }
    }
  },
  "interior_less_than_random_less_than_surface_symdiff": false,
  "status": "MEASURED",
  "interpretation": "This is a downstream corroboration of the exact matched-budget placement experiment."
}
```
