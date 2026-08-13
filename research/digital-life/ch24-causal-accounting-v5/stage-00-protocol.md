# Stage 0 — Frozen V5 Causal Accounting Protocol

```json
{
  "experiment_version": "digital-crystal-causal-accounting-v5",
  "role": "MECHANISTIC ACCOUNTING OF V4 EXTREME-FCP EFFECT",
  "seed": 20260910,
  "source_profile": "full",
  "groups": 384,
  "exposure": {
    "high": "FCP >= 2",
    "low": "FCP <= -1",
    "minimum_delta_FCP": 3
  },
  "primary_accounting_identity": "E1 = shared_shift + force_only_swap + prevent_only_swap",
  "C1_causal_cone_correctness": {
    "quantity": "E1_far_exact - swap_total_far = shared_shift_far",
    "role": "hard lag-1 causal-cone correctness control",
    "equivalence_tolerance": 0.02
  },
  "H1_selector_dilution": {
    "prediction": "-(DeltaF / F_prevent) * expected PREVENT far attachments",
    "residual_tolerance": 0.05
  },
  "H3_realized_divergence": {
    "SEI": 0.05
  },
  "H4_nonzero_GT_rate": {
    "SEI": 0.05
  },
  "occupied_neighbor_distribution": "mandatory scope diagnostic",
  "absolute_E1_high_low": "mandatory mechanism discriminator",
  "status": "FROZEN",
  "stop_rule": "V5 closes Chapter 24; no threshold or formula tuning after run."
}
```
