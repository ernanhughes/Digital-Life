# Stage 3 — Frozen V3 Hypothesis Verdicts

```json
{
  "validity": {
    "capacity_gate_passed": true,
    "group_coverage_gate_passed": true,
    "valid_for_scientific_interpretation": true
  },
  "H1_direct_causal_excitation": {
    "minimum_effect": 0.1,
    "summary": {
      "n": 48,
      "mean": 0.11458333333333333,
      "ci95_low": 0.0625,
      "ci95_high": 0.16666666666666666,
      "half_width": 0.05208333333333333
    },
    "signflip": {
      "n": 48,
      "observed_mean": 0.11458333333333333,
      "p_value": 0.0001999600079984003,
      "permutations": 5000,
      "null_mean": -0.0004666666666666667,
      "null_q95": 0.052083333333333336
    },
    "status": "SUPPORTED"
  },
  "H2_one_step_mechanical_accounting": {
    "quantity": "g1 - g_mech_1",
    "tolerance": 0.1,
    "summary": {
      "n": 48,
      "mean": 0.009921321450637541,
      "ci95_low": -0.034810472297115015,
      "ci95_high": 0.055131664126763,
      "half_width": 0.04497106821193901
    },
    "status": "CONSISTENT_WITH_MECHANICS",
    "interpretation": "Calibration/accounting check, not an emergence claim."
  },
  "H3_multistep_amplification": {
    "quantity": "G_H - g1",
    "minimum_effect": 0.2,
    "summary": {
      "n": 48,
      "mean": 0.46875,
      "ci95_low": 0.2864583333333333,
      "ci95_high": 0.6458333333333334,
      "half_width": 0.17968750000000003
    },
    "signflip": {
      "n": 48,
      "observed_mean": 0.46875,
      "p_value": 0.0001999600079984003,
      "permutations": 5000,
      "null_mean": -0.0017041666666666663,
      "null_q95": 0.1875
    },
    "status": "SUPPORTED"
  },
  "H4_branching_critical_reference": {
    "G_H_summary": {
      "n": 48,
      "mean": 0.5833333333333334,
      "ci95_low": 0.390625,
      "ci95_high": 0.7864583333333334,
      "half_width": 0.19791666666666669
    },
    "reference_value": 1.0,
    "status": "BELOW_ONE",
    "interpretation_boundary": "G_H is finite-horizon causal construction gain, not a formal branching ratio."
  }
}
```
