# Stage 2 — Same Receiver, Different Codeword

Each receiver group creates one checkpoint and eight exact forks.

The only deliberate difference between those forks is the temporal codeword.

```json
{
  "groups": 24,
  "radius": 64,
  "hard_radius_capacity": 12481,
  "checkpoint_hash_unique_count": 24,
  "max_capacity_fraction_observed": 0.33426808749298936,
  "saturation_guard": 0.85,
  "canvas_boundary_role": "Experimental truncation boundary only; no boundary interaction is intended in the information-survival protocol.",
  "rows": 960,
  "codewords_per_group": 8,
  "retention_lags": [
    0,
    4,
    8,
    16,
    24
  ],
  "checkpoint_control": "Within each group all eight codewords begin from the same receiver checkpoint, RNG state, and future environmental forcing.",
  "train_test_boundary": "Decoder folds are grouped by receiver group; one checkpoint never appears in both train and test.",
  "feature_csv": "research\\digital-life\\ch17\\ch17-receiver-features.csv"
}
```

The decoder never receives the transmitted bits.
