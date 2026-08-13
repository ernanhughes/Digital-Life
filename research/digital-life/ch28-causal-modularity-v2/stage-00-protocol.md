# Stage 0 — Frozen Chapter 28 V2 Protocol

```json
{
  "status": "FROZEN",
  "primary_question": "Do V1-selected radius-4 regions exceed geometry-matched same-checkpoint controls in causal modularity?",
  "primary_estimand": "mean_group(observed_module_score - matched_control_module_score)",
  "excess_SEI": 0.1,
  "region_radius": 4,
  "horizon": 8,
  "matching": {
    "same_checkpoint": true,
    "outcome_blind": true,
    "controls_per_observed": 2,
    "features": [
      "occupancy_fraction",
      "center_radial_distance",
      "occupied_count",
      "internal_frontier_count",
      "external_frontier_count",
      "internal_probe_depth_mean",
      "external_probe_depth_mean",
      "boundary_occupied_fraction"
    ],
    "max_occupancy_diff": 0.08,
    "max_radial_diff": 6,
    "max_occupied_count_diff": 8,
    "max_internal_frontier_diff": 4,
    "max_external_frontier_diff": 4,
    "max_standardized_distance": 4.0
  },
  "stop_rule": "No metric/radius/matching rescue. Increase groups only if UNRESOLVED solely because MDE exceeds 0.10."
}
```
