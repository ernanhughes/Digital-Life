# Stage 0 — Exact Matched-Budget Audit

```json
{
  "role": "V6 EXACT MATCHED-CUMULATIVE-BUDGET AUDIT",
  "canonical_model_modified": false,
  "placement_policies": [
    "interior_biased",
    "random_matched",
    "surface_biased"
  ],
  "transmission_fraction": 0.5,
  "synthetic_eligible_counts": {
    "interior_biased": 4,
    "random_matched": 5,
    "surface_biased": 6
  },
  "shared_budget": 2,
  "selected_counts": {
    "interior_biased": 2,
    "random_matched": 2,
    "surface_biased": 2
  },
  "equal_selected_count": true,
  "all_selected_counts_equal_shared_budget": true,
  "scientific_role": "All placement policies receive exactly the same transmission count at every synchronized propagation step. The experiment isolates spatial allocation rather than realized copy quantity."
}
```
