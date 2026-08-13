# Stage 2 — Primary Matched FCP Tests

```json
{
  "H1_high_fcp_greater_transient_gain": {
    "group_delta_G_local": {
      "n": 48,
      "mean": 0.16674107142857142,
      "ci95_low": -0.07830109126984128,
      "ci95_high": 0.43116691468253976,
      "half_width": 0.25473400297619053
    },
    "minimum_effect": 0.15,
    "signflip": {
      "n": 48,
      "observed_mean": 0.16674107142857142,
      "p_value": 0.10536182977127859,
      "permutations": 8000
    }
  },
  "H2_frontier_promotion_contrast": {
    "group_delta_promoted_frontier": {
      "n": 48,
      "mean": 1.2588293650793652,
      "ci95_low": 1.1960987103174603,
      "ci95_high": 1.3249410962301589,
      "half_width": 0.0644211929563493
    },
    "minimum_effect": 1.0,
    "signflip": {
      "n": 48,
      "observed_mean": 1.2588293650793652,
      "p_value": 0.00012498437695288088,
      "permutations": 8000
    }
  },
  "matching_diagnostics": {
    "fcp_difference": {
      "n": 48,
      "mean": 1.2588293650793652,
      "ci95_low": 1.196924603174603,
      "ci95_high": 1.3297712053571429,
      "half_width": 0.06642330109126993
    },
    "baseline_probability_difference_high_minus_low": {
      "n": 48,
      "mean": 1.9716646745606233e-17,
      "ci95_low": -1.4303449022643922e-17,
      "ci95_high": 5.453540369513747e-17,
      "half_width": 3.44194263588907e-17
    },
    "local_frontier_density_difference_high_minus_low": {
      "n": 48,
      "mean": -0.020230263157894734,
      "ci95_low": -0.024308884189640764,
      "ci95_high": -0.016147040779030907,
      "half_width": 0.0040809217053049286
    }
  },
  "system_level_diagnostics": {
    "global_gain_difference_high_minus_low": {
      "n": 48,
      "mean": -0.04593253968253969,
      "ci95_low": -0.320102306547619,
      "ci95_high": 0.23035404265873025,
      "half_width": 0.2752281746031746
    },
    "far_field_gain_difference_high_minus_low": {
      "n": 48,
      "mean": -0.21267361111111108,
      "ci95_low": -0.4424627976190476,
      "ci95_high": 0.030564236111111146,
      "half_width": 0.23651351686507938
    }
  }
}
```
