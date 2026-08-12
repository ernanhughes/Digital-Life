# Stage 0 — Reproducibility Invariant

The stochastic model must not depend on accidental Python container layout.

Digital Crystal history v3 therefore consumes RNG draws over a canonical
`sorted(frontier)` order.

A checkpoint was reconstructed through fresh serialized/deserialized
`set`, `dict`, and RNG-state objects and compared with the original checkpoint.

```json
{
  "implementation_invariant": "RNG-consuming candidate traversal is canonicalized with sorted(frontier); equivalent mathematical states must not depend on Python set/hash-table layout.",
  "state_identity_after_roundtrip": {
    "occupied_equal": true,
    "birth_time_equal": true,
    "step_equal": true,
    "signal_cursor_equal": true,
    "rng_state_equal": true,
    "process_hash_equal": true
  },
  "one_step_exact_after_container_roundtrip": true,
  "one_step_additions_equal": true,
  "full_remaining_horizon_exact_after_container_roundtrip": true,
  "remaining_steps_checked": 48,
  "passed": true
}
```

A pass means two mathematically identical states produce the same one-step and
remaining-horizon continuation even when their Python containers were rebuilt
independently.
