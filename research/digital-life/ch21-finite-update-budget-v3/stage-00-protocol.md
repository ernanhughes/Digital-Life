# Stage 0 — Freeze the Stable-Process Question

```json
{
  "role": "NORMALIZED PROCESS-STABILITY TEST",
  "v2_status": "FAILED bounded-population hypothesis because every candidate missed the frozen population-slope gate. V3 does not retry population stationarity.",
  "question": "Can normalized construction/loss flows remain stable across different starting sizes and finite budgets even while total population drifts?",
  "candidate_budgets": [
    48,
    64,
    80,
    96,
    128
  ],
  "start_conditions": {
    "small": 8,
    "medium": 14,
    "large": 20
  },
  "process_metrics": [
    "loss_fraction",
    "attachment_fraction",
    "reoccupation_fraction",
    "first_fraction",
    "gross_turnover_fraction"
  ],
  "primary_gates": {
    "max_start_size_cv_per_metric_per_budget": 0.1,
    "max_budget_cv_for_gross_turnover_fraction": 0.1,
    "max_abs_late_gross_turnover_fraction_slope": 0.0025,
    "minimum_gross_turnover_fraction": 0.05,
    "minimum_late_population": 100,
    "max_capacity_fraction": 0.75,
    "all_required": true
  },
  "new_sentence_if_successful": "Across different starting sizes and finite evaluation budgets, the Digital Crystal converges to a stable normalized turnover regime even though absolute population size may drift.",
  "forbidden_overclaims": [
    "homeostasis",
    "maintenance",
    "metabolism",
    "energy",
    "attractor",
    "self-preservation",
    "adaptation",
    "agency",
    "organism",
    "life"
  ],
  "status": "MEASURED"
}
```
