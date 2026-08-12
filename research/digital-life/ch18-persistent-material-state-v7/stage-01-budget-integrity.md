# Stage 1 — Exact Copy-Quantity Integrity

```json
{
  "groups": 64,
  "all_groups_exact_cumulative_budget_match": true,
  "final_cumulative_transmissions": {
    "interior_biased": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.640625,
      "ci95_high": 28.805078124999998,
      "min": 13.0,
      "max": 46.0
    },
    "random_matched": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.5625,
      "ci95_high": 28.726953124999998,
      "min": 13.0,
      "max": 46.0
    },
    "surface_biased": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.632421875,
      "ci95_high": 28.71875,
      "min": 13.0,
      "max": 46.0
    }
  },
  "status": "MEASURED",
  "bounded_statement": "Every branch copied exactly the same number of cells in every paired group through the full V7 observation window."
}
```
