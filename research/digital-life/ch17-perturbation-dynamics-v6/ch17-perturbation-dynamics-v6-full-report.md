# Chapter 17 — How Does the Crystal Respond to Perturbation?

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-perturbation-dynamics-v6",
  "schema_version": 6,
  "chapter": 17,
  "chapter_title": "How Does the Crystal Respond to Perturbation?",
  "run_type": "CONFIRMATORY",
  "version_6_focus": "Independent confirmation of the frozen short matched temporal-arrangement design under cell-keyed CRN. Primary endpoint t=8, primary instrument paired ridge Hotelling on the predeclared angular9 feature subspace. Secondary endpoints and all24 cannot change the primary decision.",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 64,
    "warmup_steps": 14,
    "horizon": 20,
    "message_gain": 0.65,
    "primary_endpoint": 8,
    "secondary_endpoints": [
      9,
      10,
      12
    ],
    "matched_observation_steps": [
      8,
      9,
      10,
      12
    ],
    "primary_alpha": 0.05,
    "permutations": 2000,
    "bootstrap_reps": 1000,
    "preflight_groups": 96,
    "preflight_permutations": 2000,
    "equivalence_margin_population_fraction": 0.05,
    "equivalence_margin_max_radius_fraction": 0.05,
    "equivalence_margin_attachment_rate_fraction": 0.1,
    "equivalence_margin_cov_anisotropy": 0.1,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260813,
  "seed_note": "Different from v5 exploratory seed 20260812. Stage 0 and Stage 1 also use disjoint internal seed namespaces.",
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN",
  "matched_codeword_A": "11100001",
  "matched_codeword_B": "10001101",
  "matched_codeword_validation": {
    "pulse_count_A": 4,
    "pulse_count_B": 4,
    "first_pulse_A": 0,
    "first_pulse_B": 0,
    "last_pulse_A": 7,
    "last_pulse_B": 7,
    "same_pulse_count": true,
    "same_first_pulse": true,
    "same_last_pulse": true
  },
  "primary_endpoint": 8,
  "primary_alpha": 0.05,
  "primary_feature_subspace": [
    "cov_anisotropy",
    "sector_0",
    "sector_1",
    "sector_2",
    "sector_3",
    "sector_4",
    "sector_5",
    "harmonic6_cos",
    "harmonic6_sin"
  ],
  "scientific_boundary": "Confirmatory test of a systematic matched temporal-arrangement morphology signature only. No memory, semantics, signalling, or information-storage claim is licensed by this experiment alone.",
  "started_at_unix": 1786535233.986204,
  "finished_at_unix": 1786535249.2133389,
  "reproducibility_passed": true,
  "preflight_passed": true,
  "primary_p_value": 0.736631684157921,
  "final_status": "FAILED",
  "chapter18_status": "DEFERRED"
}
```

# Stage 0 — Confirmatory CRN Preflight

```json
{
  "role": "CONFIRMATORY PREFLIGHT",
  "sequential_exact": true,
  "crn_exact": true,
  "canonical_substrate_modified": false,
  "preflight_groups_per_runner": 96,
  "omnibus_marginal_feature_test": {
    "energy_distance": 0.10172773061997553,
    "p_value": 0.9220389805097451,
    "null_q95": 0.2010539055337569,
    "gross_mismatch_screen_passed": true
  },
  "practical_equivalence_checks": {
    "population_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -0.0007127500467377229,
      "ci95_low": -0.002972643417995353,
      "ci95_high": 0.0015280935355073174,
      "predeclared_margin": 0.05,
      "passed": true
    },
    "max_radius_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -0.00048828125,
      "ci95_low": -0.00651041666666663,
      "ci95_high": 0.005208333333333315,
      "predeclared_margin": 0.05,
      "passed": true
    },
    "attachment_rate_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -1.50123194063434e-07,
      "ci95_low": -6.058232446135881e-07,
      "ci95_high": 2.8117571919455607e-07,
      "predeclared_margin": 0.1,
      "passed": true
    },
    "cov_anisotropy": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": 0.0025817919873005607,
      "ci95_low": -0.009326873219986064,
      "ci95_high": 0.014564883026005813,
      "predeclared_margin": 0.1,
      "passed": true
    }
  },
  "all_equivalence_checks_passed": true,
  "preflight_passed": true,
  "interpretation": "Passing is practical compatibility evidence for using the keyed-CRN runner as the declared counterfactual coupling. It is not proof of identical stochastic laws."
}
```


# Stage 1 — Confirmatory Matched Temporal Arrangement

```json
{
  "role": "CONFIRMATORY MATCHED TEMPORAL-ARRANGEMENT TEST",
  "groups": 48,
  "coupling": "cell-keyed CRN",
  "codeword_A": "11100001",
  "codeword_B": "10001101",
  "codeword_validation": {
    "pulse_count_A": 4,
    "pulse_count_B": 4,
    "first_pulse_A": 0,
    "first_pulse_B": 0,
    "last_pulse_A": 7,
    "last_pulse_B": 7,
    "same_pulse_count": true,
    "same_first_pulse": true,
    "same_last_pulse": true
  },
  "primary_endpoint": 8,
  "secondary_endpoints": [
    9,
    10,
    12
  ],
  "primary_alpha": 0.05,
  "primary_instrument": {
    "name": "paired_ridge_hotelling_angular9",
    "feature_names": [
      "cov_anisotropy",
      "sector_0",
      "sector_1",
      "sector_2",
      "sector_3",
      "sector_4",
      "sector_5",
      "harmonic6_cos",
      "harmonic6_sin"
    ],
    "feature_indices": [
      7,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23
    ],
    "frozen_before_run": true
  },
  "secondary_instrument": {
    "name": "paired_ridge_hotelling_all24",
    "frozen_before_run": true
  },
  "results": {
    "8": {
      "steps_since_last_pulse": 0,
      "symdiff": {
        "n": 48,
        "mean": 0.053237679546849624,
        "median": 0.05063673707062971,
        "std": 0.020440065222084025,
        "ci95_low": 0.0476240957588782,
        "ci95_high": 0.05923017294113615,
        "min": 0.007366482504604052,
        "max": 0.12849162011173185
      },
      "primary_angular9": {
        "statistic": 0.09436977108685499,
        "p_value": 0.736631684157921,
        "permutations": 2000,
        "null_mean": 0.14862723325215785,
        "null_q95": 0.29878336103110953,
        "null_q99": 0.3754371900659374
      },
      "secondary_all24": {
        "statistic": 0.15094666432685586,
        "p_value": 0.9320339830084957,
        "permutations": 2000,
        "null_mean": 0.29693114457980513,
        "null_q95": 0.5073410045819493,
        "null_q99": 0.6228469611528435
      },
      "top_directional_features_descriptive_only": [
        {
          "feature_index": 12,
          "feature_name": "degree_3",
          "mean_standardized_delta_A_minus_B": 0.11221166657284382
        },
        {
          "feature_index": 14,
          "feature_name": "degree_5",
          "mean_standardized_delta_A_minus_B": 0.11192504698594415
        },
        {
          "feature_index": 8,
          "feature_name": "boundary_fraction",
          "mean_standardized_delta_A_minus_B": 0.09172243920233587
        },
        {
          "feature_index": 15,
          "feature_name": "degree_6",
          "mean_standardized_delta_A_minus_B": -0.0917224392023357
        },
        {
          "feature_index": 9,
          "feature_name": "mean_degree",
          "mean_standardized_delta_A_minus_B": -0.07821945544065527
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": 0.07729027985214038
        }
      ]
    },
    "9": {
      "steps_since_last_pulse": 1,
      "symdiff": {
        "n": 48,
        "mean": 0.051065809159499674,
        "median": 0.051925925925925924,
        "std": 0.021190489043998957,
        "ci95_low": 0.045667466982534224,
        "ci95_high": 0.05702922127634595,
        "min": 0.005110732538330494,
        "max": 0.1345514950166113
      },
      "primary_angular9": {
        "statistic": 0.10462253153981567,
        "p_value": 0.6761619190404797,
        "permutations": 2000,
        "null_mean": 0.1468849773415163,
        "null_q95": 0.291831403070761,
        "null_q99": 0.3935468236506865
      },
      "secondary_all24": {
        "statistic": 0.3593705775507411,
        "p_value": 0.2463768115942029,
        "permutations": 2000,
        "null_mean": 0.29680435754184537,
        "null_q95": 0.5129490007797877,
        "null_q99": 0.6585531445192501
      },
      "top_directional_features_descriptive_only": [
        {
          "feature_index": 12,
          "feature_name": "degree_3",
          "mean_standardized_delta_A_minus_B": -0.35379498656117586
        },
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": 0.1896689683771923
        },
        {
          "feature_index": 1,
          "feature_name": "max_radius_fraction",
          "mean_standardized_delta_A_minus_B": 0.1474469027925834
        },
        {
          "feature_index": 11,
          "feature_name": "degree_2",
          "mean_standardized_delta_A_minus_B": 0.12743416556162304
        },
        {
          "feature_index": 10,
          "feature_name": "degree_1",
          "mean_standardized_delta_A_minus_B": 0.09042706148590109
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": 0.08963248738941478
        }
      ]
    },
    "10": {
      "steps_since_last_pulse": 2,
      "symdiff": {
        "n": 48,
        "mean": 0.049045302396830366,
        "median": 0.04915712054152564,
        "std": 0.021024693406423767,
        "ci95_low": 0.04318223268090699,
        "ci95_high": 0.05545740686080129,
        "min": 0.001579778830963665,
        "max": 0.12425149700598802
      },
      "primary_angular9": {
        "statistic": 0.13967129449472848,
        "p_value": 0.4927536231884058,
        "permutations": 2000,
        "null_mean": 0.15340971992836622,
        "null_q95": 0.3063221837227403,
        "null_q99": 0.39276757004580704
      },
      "secondary_all24": {
        "statistic": 0.31263968967941824,
        "p_value": 0.39780109945027486,
        "permutations": 2000,
        "null_mean": 0.29823847644726165,
        "null_q95": 0.5048573272561033,
        "null_q99": 0.6275202623181775
      },
      "top_directional_features_descriptive_only": [
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": -0.17773593436907484
        },
        {
          "feature_index": 1,
          "feature_name": "max_radius_fraction",
          "mean_standardized_delta_A_minus_B": 0.11819081390361119
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": 0.11531611811934737
        },
        {
          "feature_index": 11,
          "feature_name": "degree_2",
          "mean_standardized_delta_A_minus_B": 0.1089112141308975
        },
        {
          "feature_index": 18,
          "feature_name": "sector_2",
          "mean_standardized_delta_A_minus_B": 0.08222037542930782
        },
        {
          "feature_index": 5,
          "feature_name": "centroid_y_scaled",
          "mean_standardized_delta_A_minus_B": -0.0815952404223006
        }
      ]
    },
    "12": {
      "steps_since_last_pulse": 4,
      "symdiff": {
        "n": 48,
        "mean": 0.04719156948278908,
        "median": 0.04490043590251634,
        "std": 0.02106858398113281,
        "ci95_low": 0.041415059105212836,
        "ci95_high": 0.05322767479261429,
        "min": 0.0,
        "max": 0.11677018633540373
      },
      "primary_angular9": {
        "statistic": 0.10729927364073981,
        "p_value": 0.6881559220389805,
        "permutations": 2000,
        "null_mean": 0.1533947703973613,
        "null_q95": 0.2959314430175617,
        "null_q99": 0.410059161498157
      },
      "secondary_all24": {
        "statistic": 0.3765933256681049,
        "p_value": 0.27436281859070466,
        "permutations": 2000,
        "null_mean": 0.3144835065444021,
        "null_q95": 0.5322185687734629,
        "null_q99": 0.6695757084413488
      },
      "top_directional_features_descriptive_only": [
        {
          "feature_index": 11,
          "feature_name": "degree_2",
          "mean_standardized_delta_A_minus_B": -0.22443345195347
        },
        {
          "feature_index": 10,
          "feature_name": "degree_1",
          "mean_standardized_delta_A_minus_B": 0.19522847584620937
        },
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": 0.1452259741643702
        },
        {
          "feature_index": 14,
          "feature_name": "degree_5",
          "mean_standardized_delta_A_minus_B": -0.1053508820220503
        },
        {
          "feature_index": 1,
          "feature_name": "max_radius_fraction",
          "mean_standardized_delta_A_minus_B": 0.10279338877026702
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": 0.08670747691822346
        }
      ]
    }
  },
  "primary_positive": false,
  "decision_rule": "Primary angular9 paired-ridge test at t=8 only. p < 0.05 => PROVISIONAL matched-arrangement signature. p >= 0.05 => FAILED under this frozen calibrated protocol. Secondary endpoints and all24 may not rescue or overturn the primary."
}
```


# Stage 2 — Bounded V6 Confirmatory Verdict

```json
{
  "experiment_role": "CONFIRMATORY",
  "preflight_passed": true,
  "matched_arrangement_status": "FAILED",
  "primary_endpoint": 8,
  "primary_instrument": "paired_ridge_hotelling_angular9",
  "primary_p_value": 0.736631684157921,
  "primary_alpha": 0.05,
  "bounded_statement": "Under the frozen CRN coupling, short matched codewords, t=8 endpoint, angular9 feature set, and paired ridge statistic, the independent v6 sample did not establish a systematic temporal-arrangement signature. Secondary endpoints or all24 results do not alter this primary decision.",
  "secondary_results_cannot_change_primary_decision": true,
  "chapter18_status": "DEFERRED",
  "nonclaims": [
    "memory",
    "information storage",
    "semantics",
    "sender identity",
    "coordination",
    "learning",
    "agency",
    "individuality",
    "life",
    "Shannon channel capacity"
  ]
}
```
