# Stage 6 — Bounded V4 Verdict

```json
{
  "experiment_role": "EXPLORATORY / MEASUREMENT-RESOLUTION",
  "calibration_version": "symmetric-paired-null-v4",
  "single_pulse_response": "MEASURED",
  "single_pulse_latest_observation": 32,
  "single_pulse_causal_symdiff_mean": 0.12968415596747898,
  "independent_stochastic_symdiff_mean": 0.1387010895940292,
  "single_pulse_exceeds_stochastic_spread_descriptively": false,
  "ensemble_superposition": "MEASURED",
  "measurement_ready": false,
  "selected_instrument": null,
  "instrument_validity_summary": {
    "energy_distance": {
      "instrument_class": "MARGINAL_DISTRIBUTION",
      "null_valid": true,
      "sensitive_at_target": false,
      "eligible": false,
      "failure_reason": "INSUFFICIENT_POWER",
      "worst_null_fpr": 0.025,
      "worst_target_power": 0.125
    },
    "paired_mean_l2": {
      "instrument_class": "PAIRED_DIRECTIONAL",
      "null_valid": true,
      "sensitive_at_target": false,
      "eligible": false,
      "failure_reason": "INSUFFICIENT_POWER",
      "worst_null_fpr": 0.05,
      "worst_target_power": 0.15
    },
    "paired_max_abs_mean": {
      "instrument_class": "PAIRED_DIRECTIONAL",
      "null_valid": true,
      "sensitive_at_target": false,
      "eligible": false,
      "failure_reason": "INSUFFICIENT_POWER",
      "worst_null_fpr": 0.025,
      "worst_target_power": 0.05
    },
    "paired_ridge_hotelling": {
      "instrument_class": "PAIRED_DIRECTIONAL",
      "null_valid": true,
      "sensitive_at_target": false,
      "eligible": false,
      "failure_reason": "INSUFFICIENT_POWER",
      "worst_null_fpr": 0.1,
      "worst_target_power": 0.425
    }
  },
  "null_invalid_instruments": [],
  "valid_but_underpowered_instruments": [
    "energy_distance",
    "paired_mean_l2",
    "paired_max_abs_mean",
    "paired_ridge_hotelling"
  ],
  "matched_endpoint_arrangement_status": "UNTESTED",
  "matched_endpoint_primary_endpoint": 20,
  "selected_real_test": null,
  "separate_stage4_sham_false_positive_rate": 0.0,
  "bounded_statement": "No candidate measurement instrument met both the predeclared known-null validity and known-effect sensitivity requirements. The matched interior-timing hypothesis therefore remains unresolved under this quick protocol.",
  "nonclaims": [
    "information storage",
    "memory",
    "signalling",
    "semantics",
    "sender identity",
    "coordination",
    "learning",
    "agency",
    "individuality",
    "life",
    "Shannon channel capacity"
  ],
  "next_decision_logic": {
    "if_null_calibration_fails": "Reject the instrument as invalid for this calibration design; do not interpret its real-data p-value.",
    "if_null_valid_but_power_fails": "The instrument is not grossly anti-conservative but is too weak at the declared target effect. Improve sample size or measurement design before judging the real matched-arrangement result.",
    "if_instrument_ready_and_real_positive": "Freeze instrument, endpoint, codewords, analysis plan and a new seed; run an independent confirmatory Chapter 17 replication before carrying the result into Chapter 18.",
    "if_instrument_ready_and_real_negative": "Record matched interior timing as FAILED under this calibrated protocol; do not reinterpret the old Chapter 18 candidate as temporal retention.",
    "if_superposition_residual_large": "Continue mechanistic work on why the ensemble additive response model fails before using information-processing language."
  }
}
```
