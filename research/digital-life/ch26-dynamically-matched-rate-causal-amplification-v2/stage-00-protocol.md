# Stage 0 — Frozen Chapter 26 V2 Protocol

```json
{
  "role": "DYNAMICALLY MATCHED BACKGROUND CONSTRUCTION-RATE CAUSAL AMPLIFICATION TEST",
  "question": "At dynamically matched background expected construction rate, does strong candidate subsampling change finite-horizon causal amplification relative to true exhaustive evaluation?",
  "primary_contrast": "G_T(f=0.10) - G_T(unbounded)",
  "primary_SEI_abs": 0.15,
  "two_sided": true,
  "same_checkpoint_across_arms": true,
  "same_probe_across_arms": true,
  "same_post_intervention_states_across_arms": true,
  "intervention_budget": 96,
  "dynamic_matching": {
    "reference_policy": "dedicated PREVENT-only f=0.10 trajectory, base offset 0",
    "target": "lag-specific exact expected attachments from reference PREVENT",
    "arm_calibration": "solve offset on each arm's PREVENT state every lag; apply same offset to FORCE",
    "relative_tolerance": 0.02,
    "minimum_record_pass_fraction": 0.95,
    "population_mean_every_arm_lag_must_pass": true
  },
  "arms": {
    "f=0.10": "primary strong-subsampling arm",
    "f=0.25": "secondary",
    "f=0.50": "secondary",
    "f=0.75": "secondary",
    "f=1.00": "secondary fixed-budget arm; NOT dynamically exhaustive",
    "unbounded": "primary true exhaustive reference"
  },
  "supported_probe_scope": "occupied_neighbors = 1",
  "forbidden_overclaims": [
    "formal branching ratio",
    "subcritical",
    "supercritical",
    "critical point",
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
