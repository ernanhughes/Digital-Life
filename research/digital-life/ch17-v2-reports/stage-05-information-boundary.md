# Stage 5 — Find the Simplest Surviving Distinction

```json
{
  "exploratory_threshold": "raw combined accuracy > grouped permutation q95 AND >= 0.075 absolute accuracy above chance",
  "first_supported_level": "L1",
  "first_supported_elapsed_step": 8,
  "levels": {
    "L1": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.625,
        "chance": 0.5,
        "margin_above_chance": 0.125,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.5854166666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L2": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.16666666666666663,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.5833333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.020833333333333315,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      }
    ],
    "L3": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.5427083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6875,
        "chance": 0.5,
        "margin_above_chance": 0.1875,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.16666666666666663,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L4": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.625,
        "chance": 0.5,
        "margin_above_chance": 0.125,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.020833333333333315,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.4166666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.08333333333333331,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L5": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.2916666666666667,
        "chance": 0.25,
        "margin_above_chance": 0.041666666666666685,
        "null_q95": 0.3020833333333333,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "margin_above_chance": 0.010416666666666685,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.3958333333333333,
        "chance": 0.25,
        "margin_above_chance": 0.14583333333333331,
        "null_q95": 0.3130208333333333,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.375,
        "chance": 0.25,
        "margin_above_chance": 0.125,
        "null_q95": 0.3234375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "margin_above_chance": -0.010416666666666657,
        "null_q95": 0.3234375,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.19791666666666666,
        "chance": 0.25,
        "margin_above_chance": -0.05208333333333334,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "margin_above_chance": -0.010416666666666657,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.21875,
        "chance": 0.25,
        "margin_above_chance": -0.03125,
        "null_q95": 0.3130208333333333,
        "passes_exploratory_threshold": false
      }
    ],
    "L6": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "margin_above_chance": -0.005208333333333329,
        "null_q95": 0.15104166666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.17708333333333334,
        "chance": 0.125,
        "margin_above_chance": 0.05208333333333334,
        "null_q95": 0.15651041666666665,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.16145833333333334,
        "chance": 0.125,
        "margin_above_chance": 0.03645833333333334,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.18229166666666666,
        "chance": 0.125,
        "margin_above_chance": 0.05729166666666666,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.171875,
        "chance": 0.125,
        "margin_above_chance": 0.046875,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.140625,
        "chance": 0.125,
        "margin_above_chance": 0.015625,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.171875,
        "chance": 0.125,
        "margin_above_chance": 0.046875,
        "null_q95": 0.171875,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "margin_above_chance": -0.005208333333333329,
        "null_q95": 0.16718749999999996,
        "passes_exploratory_threshold": false
      }
    ]
  },
  "interpretation": "v2 is a boundary-finding experiment. Any positive rung discovered here should be frozen and rerun in a separate confirmatory version."
}
```
