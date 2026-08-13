# Stage 0 — Frozen Chapter 26 V1 Protocol

```json
{
  "role": "MATCHED-CONSTRUCTION-RATE CAUSAL AMPLIFICATION TEST",
  "question": "At matched expected construction rate, does stronger candidate subsampling change transient causal amplification?",
  "same_checkpoint_across_arms": true,
  "same_probe_across_arms": true,
  "same_post_intervention_force_prevent_states_across_arms": true,
  "intervention_budget_fixed_at": 96,
  "same_future_environment": true,
  "same_random_keys": true,
  "control_parameter": "fraction of frontier candidates evaluated",
  "fractions": [
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "unbounded_arm": true,
  "reference_fraction_for_target": 0.1,
  "construction_rate_match": {
    "target": "checkpoint-specific expected attachments under f=0.10 with base offset 0 on the common post-intervention PREVENT state",
    "relative_tolerance": 0.02,
    "required_arm_pass_fraction": 0.95
  },
  "primary_H1": {
    "contrast": "G_T(f=0.10) - G_T(f=1.00)",
    "SEI_abs": 0.15,
    "two_sided": true,
    "statuses": [
      "SUPPORTED",
      "BOUNDED_NEAR_ZERO",
      "UNRESOLVED",
      "INVALID"
    ]
  },
  "supported_probe_scope": "occupied_neighbors = 1",
  "horizon": 12,
  "forbidden_overclaims": [
    "formal branching ratio",
    "critical point",
    "supercriticality",
    "phase transition",
    "directed percolation",
    "coherent structure",
    "individuality",
    "organism",
    "life"
  ],
  "status": "FROZEN"
}
```
