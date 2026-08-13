# Chapter 24 — Does Recent Local Process History Determine Causal Gain? (V3)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-local-process-history-v3",
  "schema_version": 3,
  "base_model_version": "digital-crystal-v1-frozen",
  "parent_experiment_version": "digital-crystal-finite-update-budget-v3",
  "chapter": 24,
  "chapter_title": "Where Is Causal Gain Created?",
  "run_title": "Does Recent Local Process History Determine Causal Gain?",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 78,
    "warmup_steps": 20,
    "lossy_pre_steps": 20,
    "history_window": 6,
    "history_radius": 2,
    "horizon": 12,
    "loss_rate": 0.08,
    "budget": 96,
    "radial_bin_width": 3,
    "probability_tolerance": 0.05,
    "local_frontier_density_tolerance": 0.1,
    "fcp_tolerance": 1,
    "minimum_turnover_difference": 2,
    "minimum_gain_difference": 0.15,
    "minimum_turnover_contrast": 2.0,
    "minimum_group_coverage_fraction": 0.7,
    "max_pairs_per_group": 8,
    "bootstrap_reps": 3000,
    "signflip_permutations": 8000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260908,
  "previous_seed": 20260907,
  "fresh_seed": true,
  "classifier_used": false,
  "canonical_rules_modified": false,
  "started_at_unix": 1786579543.184059,
  "finished_at_unix": 1786579606.4852133,
  "final_status": "RECENT_PROCESS_HISTORY_GAIN_LINK_FAILED"
}
```

---

## Stage 0 — Frozen Chapter 24 V3 Protocol

```json
{
  "role": "RECENT LOCAL PROCESS HISTORY / TRANSIENT CAUSAL GAIN TEST",
  "fresh_seed": 20260908,
  "history_window": 6,
  "history_radius": 2,
  "primary_history_variable": "recent_turnover = recent_attachments + recent_losses",
  "target": "transient causal gain G_T(H)",
  "horizon": 12,
  "present_state_matching": {
    "same_canonical_motif": true,
    "same_radial_bin_width": 3,
    "max_baseline_p_difference": 0.05,
    "max_local_frontier_density_difference": 0.1,
    "max_FCP_difference": 1
  },
  "H1": {
    "quantity": "G_T(high recent turnover) - G_T(low recent turnover), one mean per independent group",
    "minimum_effect": 0.15,
    "alpha": 0.05,
    "minimum_group_coverage_fraction": 0.7
  },
  "H2": {
    "quantity": "recent_turnover(high) - recent_turnover(low)",
    "minimum_effect": 2.0,
    "role": "construct validity gate"
  },
  "stop_rule": "If H1 fails on a valid run, do not tune history radius/window or select another history component from the same run.",
  "classifier_used": false,
  "status": "FROZEN"
}
```

---

## Stage 1 — Present-State-Matched Process-History Interventions

```json
{
  "requested_groups": 48,
  "groups_with_pairs": 48,
  "coverage_fraction": 1.0,
  "minimum_coverage_fraction": 0.7,
  "coverage_gate_passed": true,
  "total_pairs": 384,
  "mean_pairs_per_group_with_pairs": 8.0,
  "pair_count_distribution": {
    "min": 8,
    "median": 8.0,
    "max": 8
  },
  "maximum_capacity_fraction": 0.03726943257424136,
  "capacity_gate_passed": true,
  "status": "MEASURED"
}
```

---

## Stage 2 — Primary Process-History Tests

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

---

## Stage 3 — Descriptive Local Process-History Map

```json
{
  "n_unique_intervention_sites": 768,
  "spearman_correlations_descriptive": {
    "recent_turnover": 0.0022762266882827547,
    "recent_attachments": 0.004558477569275881,
    "recent_losses": -0.002044943203936407,
    "recent_reoccupations": -0.020535292121172822,
    "recent_first_occupations": 0.05920443946793494,
    "recent_evaluations": 0.06378925165995437
  },
  "gain_by_recent_turnover": [
    {
      "recent_turnover": 0,
      "n": 1,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 1,
      "n": 13,
      "mean_transient_gain": 0.07692307692307693
    },
    {
      "recent_turnover": 2,
      "n": 38,
      "mean_transient_gain": 0.4473684210526316
    },
    {
      "recent_turnover": 3,
      "n": 34,
      "mean_transient_gain": -0.14705882352941177
    },
    {
      "recent_turnover": 4,
      "n": 36,
      "mean_transient_gain": 0.3611111111111111
    },
    {
      "recent_turnover": 5,
      "n": 27,
      "mean_transient_gain": -0.25925925925925924
    },
    {
      "recent_turnover": 6,
      "n": 40,
      "mean_transient_gain": 0.025
    },
    {
      "recent_turnover": 7,
      "n": 52,
      "mean_transient_gain": 0.07692307692307693
    },
    {
      "recent_turnover": 8,
      "n": 66,
      "mean_transient_gain": 0.030303030303030304
    },
    {
      "recent_turnover": 9,
      "n": 49,
      "mean_transient_gain": 0.04081632653061224
    },
    {
      "recent_turnover": 10,
      "n": 55,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 11,
      "n": 51,
      "mean_transient_gain": 0.0392156862745098
    },
    {
      "recent_turnover": 12,
      "n": 38,
      "mean_transient_gain": -0.07894736842105263
    },
    {
      "recent_turnover": 13,
      "n": 47,
      "mean_transient_gain": 0.1276595744680851
    },
    {
      "recent_turnover": 14,
      "n": 31,
      "mean_transient_gain": -0.03225806451612903
    },
    {
      "recent_turnover": 15,
      "n": 41,
      "mean_transient_gain": 0.21951219512195122
    },
    {
      "recent_turnover": 16,
      "n": 29,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 17,
      "n": 35,
      "mean_transient_gain": 0.42857142857142855
    },
    {
      "recent_turnover": 18,
      "n": 31,
      "mean_transient_gain": -0.03225806451612903
    },
    {
      "recent_turnover": 19,
      "n": 16,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 20,
      "n": 17,
      "mean_transient_gain": 0.058823529411764705
    },
    {
      "recent_turnover": 21,
      "n": 8,
      "mean_transient_gain": 0.125
    },
    {
      "recent_turnover": 22,
      "n": 5,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 23,
      "n": 3,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 24,
      "n": 3,
      "mean_transient_gain": 0.0
    },
    {
      "recent_turnover": 26,
      "n": 2,
      "mean_transient_gain": 0.0
    }
  ],
  "scope": "Descriptive only. No history component is promoted to a new hypothesis from V3."
}
```

---

## Stage 4 — Bounded Chapter 24 V3 Verdict

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
