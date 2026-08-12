# Stage 4 — How Fast Does One Bit Matter?

The exact checkpoint intervention from Stage 2 gives an impulse response.

```json
{
  "impulse_response": [
    1.8083333333333333,
    0.0,
    -0.3416666666666667,
    -0.075,
    -0.3,
    -0.31666666666666665,
    -0.39166666666666666,
    -0.35,
    -0.6083333333333333,
    -0.25833333333333336,
    -0.25,
    -0.75
  ],
  "peak_effect_lag_steps": 0,
  "peak_effect": 1.8083333333333333,
  "lag_containing_90pct_absolute_effect_mass": 11,
  "interpretation": "Finite-horizon impulse-response description only. The peak lag is not claimed as a stable characteristic latency, and this is not a channel-capacity result."
}
```

This describes the finite-horizon response of growth to a one-bit causal
perturbation. The largest observed lag is not yet treated as a stable latency
law, and this does not establish information-theoretic capacity.
