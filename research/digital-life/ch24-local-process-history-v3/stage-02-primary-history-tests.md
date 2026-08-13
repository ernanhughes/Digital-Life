# Stage 2 — Primary Process-History Tests

```json
{
  "H1_recent_turnover_predicts_transient_gain": {
    "group_gain_difference_high_minus_low": {
      "n": 48,
      "mean": -0.06510416666666667,
      "ci95_low": -0.22135416666666666,
      "ci95_high": 0.09635416666666667,
      "half_width": 0.15885416666666666
    },
    "minimum_effect": 0.15,
    "signflip": {
      "n": 48,
      "observed_mean": -0.06510416666666667,
      "p_value": 0.791151106111736,
      "permutations": 8000
    }
  },
  "H2_turnover_construct_validity": {
    "group_turnover_difference_high_minus_low": {
      "n": 48,
      "mean": 7.734375,
      "ci95_low": 7.364583333333333,
      "ci95_high": 8.1015625,
      "half_width": 0.3684895833333335
    },
    "minimum_effect": 2.0,
    "signflip": {
      "n": 48,
      "observed_mean": 7.734375,
      "p_value": 0.00012498437695288088,
      "permutations": 8000
    }
  },
  "history_component_differences": {
    "recent_attachments": {
      "n": 48,
      "mean": 3.7682291666666665,
      "ci95_low": 3.5052083333333335,
      "ci95_high": 4.036458333333333,
      "half_width": 0.2656249999999998
    },
    "recent_losses": {
      "n": 48,
      "mean": 3.9661458333333335,
      "ci95_low": 3.7030598958333334,
      "ci95_high": 4.216145833333333,
      "half_width": 0.2565429687499998
    },
    "recent_reoccupations": {
      "n": 48,
      "mean": 3.1822916666666665,
      "ci95_low": 2.9401041666666665,
      "ci95_high": 3.4427083333333335,
      "half_width": 0.2513020833333335
    },
    "recent_first_occupations": {
      "n": 48,
      "mean": 0.5859375,
      "ci95_low": 0.3462890625,
      "ci95_high": 0.84375,
      "half_width": 0.24873046875
    },
    "recent_evaluations": {
      "n": 48,
      "mean": 3.2760416666666665,
      "ci95_low": 2.7838541666666665,
      "ci95_high": 3.78125,
      "half_width": 0.49869791666666674
    }
  },
  "present_state_matching_diagnostics": {
    "baseline_probability": {
      "n": 48,
      "mean": -4.994558007916557e-17,
      "ci95_low": -1.0879968800892037e-16,
      "ci95_high": 3.254413521077329e-18,
      "half_width": 5.602705076499885e-17
    },
    "current_frontier_density": {
      "n": 48,
      "mean": 0.0060307017543859654,
      "ci95_low": 0.0008189418859649129,
      "ci95_high": 0.011239035087719298,
      "half_width": 0.005210046600877193
    },
    "FCP": {
      "n": 48,
      "mean": -0.1875,
      "ci95_low": -0.23177083333333334,
      "ci95_high": -0.14583333333333334,
      "half_width": 0.04296875
    },
    "radial_distance": {
      "n": 48,
      "mean": -0.22916666666666666,
      "ci95_low": -0.3541666666666667,
      "ci95_high": -0.11197916666666667,
      "half_width": 0.12109375
    }
  },
  "system_level_diagnostics": {
    "global_gain": {
      "n": 48,
      "mean": 0.044270833333333336,
      "ci95_low": -0.11458333333333333,
      "ci95_high": 0.21360677083333357,
      "half_width": 0.16409505208333344
    },
    "far_field_gain": {
      "n": 48,
      "mean": 0.109375,
      "ci95_low": -0.049479166666666664,
      "ci95_high": 0.2890625,
      "half_width": 0.16927083333333334
    },
    "eval_overlap": {
      "n": 48,
      "mean": 0.0006909350312441989,
      "ci95_low": -6.143810904706553e-05,
      "ci95_high": 0.0014079970919458067,
      "half_width": 0.0007347176004964361
    }
  }
}
```
