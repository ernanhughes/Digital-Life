# Stage 0 — Frozen Chapter 24 V4 Reset Protocol

```json
{
  "experiment_version": "digital-crystal-frontier-creation-causal-gain-v4-reset",
  "role": "RESET EXTREME-FCP CAUSAL MECHANISM TEST",
  "seed": 20260909,
  "mode": "run",
  "exposure": {
    "high": "FCP >= 2",
    "low": "FCP <= -1",
    "minimum_delta_FCP": 3,
    "FCP_identity": "FCP = promoted_frontier - 1",
    "promotion_status": "implementation invariant, not independent evidence"
  },
  "pairing": {
    "same_occupied_neighbor_count": true,
    "same_radial_bin_width": 4,
    "baseline_p_matched": false,
    "frontier_density_matched": false,
    "reason": "baseline p and density may lie on or summarize the geometry pathway; V4 estimates the total extreme-geometry contrast"
  },
  "H1_primary": {
    "outcome": "Delta exact E1_local",
    "SEI": 0.1,
    "status_space": [
      "SUPPORTED",
      "BOUNDED_BELOW_SEI",
      "UNRESOLVED",
      "INVALID"
    ],
    "precision_gate": "achieved one-sided 80% MDE must be <= SEI"
  },
  "H2_secondary": {
    "outcome": "Delta realized g1_local",
    "SEI": 0.1
  },
  "H3_mechanism": {
    "outcome": "Delta model-implied P(any lag1 local divergence)",
    "SEI": 0.05
  },
  "H4_downstream": {
    "outcome": "Delta G_T(H)",
    "SEI": 0.15
  },
  "zero_inflation_decomposition": [
    "P(lag1 realized divergence)",
    "P(G_T != 0)",
    "E[G_T | G_T != 0]"
  ],
  "support_gate": {
    "minimum_group_coverage_fraction": 0.5,
    "no_automatic_weaker_contrast": true,
    "design_audit_provenance": "Frozen at 0.50 after outcome-blind 48-group seed-20260909 support audit found 0.5417 coverage for exact Delta-FCP=3. No V4 causal outcomes were inspected."
  },
  "horizon": 12,
  "classifier_used": false,
  "scientific": true,
  "status": "FROZEN"
}
```
