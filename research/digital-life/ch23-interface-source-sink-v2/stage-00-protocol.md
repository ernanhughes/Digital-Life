# Stage 0 — Frozen V2 Source/Sink Protocol

```json
{
  "role": "INTERFACE SOURCE/SINK TRANSITION FIELD",
  "fresh_seed": 20260903,
  "v1_status": "FAILED. Do not retune the V1 ridge statistic.",
  "measurement_change": "Signed source-class x target-class transition surfaces with negative lags; no positive-weighted centroid.",
  "source_classes": [
    "attachment",
    "loss"
  ],
  "target_classes": [
    "attachment",
    "loss",
    "reoccupation",
    "first_occupation"
  ],
  "subset_note": "reoccupation and first_occupation are subsets of attachment",
  "distances": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
  ],
  "lags": [
    -16,
    -15,
    -14,
    -13,
    -12,
    -11,
    -10,
    -9,
    -8,
    -7,
    -6,
    -5,
    -4,
    -3,
    -2,
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16
  ],
  "uniform_grid": true,
  "max_lag_at_least_twice_max_distance": true,
  "common_source_window": [
    16,
    79
  ],
  "band_width": 4,
  "formal_representation": "raw signed excess surface",
  "offset_corrected_surface_role": "diagnostic only",
  "h1": "Fresh-seed attachment -> attachment excess at d in {1,2} is negative by at least the frozen 5e-4 directional effect floor.",
  "h2": "Fresh-seed loss -> attachment excess at d in {0,1} is positive by at least the frozen 5e-4 directional effect floor.",
  "h3": "At d=1, late attachment -> attachment excess remains negative over the frozen late window and retains at least 50% of the absolute early deficit.",
  "h4_validity": "Future per-eligible-cell loss hazard around loss sources versus matched survivor controls remains within the frozen null tolerance.",
  "positive_control": "loss -> reoccupation must be positive at short range/lag; this recovers the independently established Chapter 20 mechanism.",
  "propagation_test": "attachment -> attachment forward/backward asymmetry at d>=3, compared with four-partner cross-run future null. Separate from short-range source/sink findings.",
  "mde_signed_excess": 0.0005,
  "mde_propagation_asymmetry": 0.0005,
  "scientific_boundary": "Interface source/sink dynamics only. Local opportunity consumption is a candidate mechanism until causal intervention. No refractory, wave, excitable-medium, individuality, autonomy, organism, agency, or life claim.",
  "status": "FROZEN"
}
```
