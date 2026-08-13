# Stage 4 — Bounded Chapter 24 V3 Verdict

```json
{
  "validity": {
    "valid": true,
    "coverage_gate": true,
    "capacity_gate": true
  },
  "H1": {
    "status": "FAILED",
    "result": {
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
    }
  },
  "H2": {
    "status": "SUPPORTED",
    "result": {
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
    }
  },
  "overall_status": "RECENT_PROCESS_HISTORY_GAIN_LINK_FAILED",
  "bounded_claim": "The frozen V3 pairs differed strongly in recent local material turnover, but the experiment did not establish a scientifically meaningful corresponding increase in transient causal gain after matching present local geometry.",
  "what_this_does_not_establish": [
    "memory",
    "learning",
    "adaptation",
    "history is the only determinant of causal gain",
    "causal-gain field",
    "high-gain regions",
    "spatial clustering",
    "temporal persistence",
    "coherent structure",
    "criticality",
    "percolation",
    "natural boundary",
    "individuality",
    "autonomy",
    "organism",
    "life"
  ],
  "stop_rule_if_failed": "Do not tune history radius/window or select a different history component from this run. Chapter 24 should close unless a qualitatively new causal property is proposed.",
  "next_if_supported": "Freshly confirm the process-history effect before mapping any history-derived high-gain regions through space-time."
}
```
