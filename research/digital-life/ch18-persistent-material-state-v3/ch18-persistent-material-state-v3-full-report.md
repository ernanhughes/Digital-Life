# Chapter 18 — Can Experience Change the Material? (V3 Propagation)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v3",
  "schema_version": 3,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY MECHANISM EXTENSION",
  "profile": "quick",
  "profile_config": {
    "groups": 40,
    "radius": 64,
    "warmup_steps": 14,
    "experience_pulse_step": 3,
    "message_gain": 0.65,
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "inheritance_probability": 0.5,
    "accessibility_observation_steps": [
      4,
      5,
      6,
      7,
      8,
      10,
      12,
      14,
      18,
      22
    ],
    "late_ablation_step": 14,
    "late_ablation_followup": 4,
    "challenge_step": 14,
    "challenge_horizon": 4,
    "challenge_pulse_step": 0,
    "challenge_observation_steps": [
      1,
      2,
      4
    ],
    "challenge_primary_endpoint": 2,
    "permutations": 1500,
    "bootstrap_reps": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260816,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "v2_supported_result": "Persistent material was causally active while it contacted the growth frontier and became inert after growth moved beyond it.",
  "v3_new_mechanism": "A newly attached cell adjacent to pre-existing modified material inherits modified state with fixed probability.",
  "material_parameters": {
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "inheritance_probability": 0.5
  },
  "scientific_boundary": "Local propagation of material state only. No global memory register, history buffer, learned parameter, target behaviour, decoder, or biological inheritance claim.",
  "started_at_unix": 1786538429.2619684,
  "finished_at_unix": 1786538436.7570426,
  "stage_1_status": "SUPPORTED",
  "stage_2_status": "FAILED",
  "stage_3_status": "FAILED",
  "final_status": "FAILED",
  "next_question": "Propagation preserved frontier contact but the late retained state was not shown to be causally active."
}
```

# Stage 0 — Propagation Extension Audit

```json
{
  "role": "V3 PROPAGATION EXTENSION AUDIT",
  "base_model_version": "digital-crystal-v1-frozen",
  "experimental_extension": "digital-crystal-persistent-material-state-v3",
  "canonical_model_modified": false,
  "exact_when_material_state_empty": true,
  "material_extension_exact_reproducibility": true,
  "write_probability": 0.2,
  "modified_neighbor_gain": 0.3,
  "inheritance_probability": 0.5,
  "new_mechanism": "newly attached cells adjacent to pre-existing modified material inherit modified state with fixed probability",
  "interpretation": "Inheritance is local and inert until experience-written modified material exists."
}
```


# Stage 1 — Can Material State Travel With the Growth Front?

```json
{
  "groups": 40,
  "inheritance_probability": 0.5,
  "observation_steps": [
    4,
    5,
    6,
    7,
    8,
    10,
    12,
    14,
    18,
    22
  ],
  "late_target_step": 14,
  "summary": {
    "4": {
      "modified_count": {
        "n": 40,
        "mean": 21.1,
        "median": 20.5,
        "std": 5.083306010855534,
        "ci95_low": 19.525,
        "ci95_high": 22.725,
        "min": 7.0,
        "max": 33.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 21.1,
        "median": 20.5,
        "std": 5.083306010855534,
        "ci95_low": 19.375,
        "ci95_high": 22.675,
        "min": 7.0,
        "max": 33.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 37.85,
        "median": 38.5,
        "std": 8.710769196804607,
        "ci95_low": 35.024375,
        "ci95_high": 40.525,
        "min": 12.0,
        "max": 57.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.36094387159339214,
        "median": 0.36803571428571424,
        "std": 0.0793689984779892,
        "ci95_low": 0.33530356094426983,
        "ci95_high": 0.38510549261426713,
        "min": 0.13186813186813187,
        "max": 0.5181818181818182
      }
    },
    "5": {
      "modified_count": {
        "n": 40,
        "mean": 30.65,
        "median": 29.0,
        "std": 7.747741606429579,
        "ci95_low": 28.3,
        "ci95_high": 33.075,
        "min": 11.0,
        "max": 50.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 20.75,
        "median": 21.0,
        "std": 5.668994619859856,
        "ci95_low": 18.975,
        "ci95_high": 22.425625,
        "min": 7.0,
        "max": 35.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 31.225,
        "median": 32.5,
        "std": 7.818207914861308,
        "ci95_low": 28.77375,
        "ci95_high": 33.575625,
        "min": 11.0,
        "max": 44.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.2836454021738381,
        "median": 0.29523809523809524,
        "std": 0.07315142215992138,
        "ci95_low": 0.26075166577931397,
        "ci95_high": 0.30658593280323826,
        "min": 0.10476190476190476,
        "max": 0.42574257425742573
      }
    },
    "6": {
      "modified_count": {
        "n": 40,
        "mean": 39.775,
        "median": 39.5,
        "std": 9.850095177205143,
        "ci95_low": 36.675,
        "ci95_high": 42.65,
        "min": 15.0,
        "max": 65.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 19.0,
        "median": 19.0,
        "std": 5.486346689738081,
        "ci95_low": 17.424375,
        "ci95_high": 20.675,
        "min": 6.0,
        "max": 30.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 26.225,
        "median": 27.0,
        "std": 6.879271400373734,
        "ci95_low": 24.124375,
        "ci95_high": 28.4,
        "min": 7.0,
        "max": 38.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.22759051154732052,
        "median": 0.22868061142397425,
        "std": 0.06415223586572401,
        "ci95_low": 0.20778223222397882,
        "ci95_high": 0.24705107652514782,
        "min": 0.06481481481481481,
        "max": 0.35185185185185186
      }
    },
    "7": {
      "modified_count": {
        "n": 40,
        "mean": 47.0,
        "median": 48.0,
        "std": 12.320714265009151,
        "ci95_low": 43.35,
        "ci95_high": 51.075625,
        "min": 15.0,
        "max": 77.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 15.875,
        "median": 17.0,
        "std": 5.395310463726809,
        "ci95_low": 14.25,
        "ci95_high": 17.475625,
        "min": 2.0,
        "max": 25.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 21.5,
        "median": 23.0,
        "std": 7.214568594171102,
        "ci95_low": 19.298750000000002,
        "ci95_high": 23.775,
        "min": 3.0,
        "max": 36.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.17612122926842685,
        "median": 0.1891528060308723,
        "std": 0.06060169402246876,
        "ci95_low": 0.15682505442239048,
        "ci95_high": 0.19457970309571215,
        "min": 0.025423728813559324,
        "max": 0.308411214953271
      }
    },
    "8": {
      "modified_count": {
        "n": 40,
        "mean": 53.25,
        "median": 52.0,
        "std": 13.827056809024834,
        "ci95_low": 49.02375,
        "ci95_high": 57.300625,
        "min": 16.0,
        "max": 81.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 12.875,
        "median": 14.0,
        "std": 5.541604009670847,
        "ci95_low": 11.15,
        "ci95_high": 14.6,
        "min": 1.0,
        "max": 28.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 17.5,
        "median": 18.0,
        "std": 7.566372975210778,
        "ci95_low": 15.05,
        "ci95_high": 19.875625,
        "min": 1.0,
        "max": 32.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.13527123152009096,
        "median": 0.1383823032759203,
        "std": 0.06024793863663213,
        "ci95_low": 0.11799197267930837,
        "ci95_high": 0.15495027034731726,
        "min": 0.007936507936507936,
        "max": 0.2782608695652174
      }
    },
    "10": {
      "modified_count": {
        "n": 40,
        "mean": 61.825,
        "median": 61.0,
        "std": 16.33537189659299,
        "ci95_low": 56.349375,
        "ci95_high": 66.676875,
        "min": 16.0,
        "max": 92.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 8.425,
        "median": 8.0,
        "std": 4.454702571440657,
        "ci95_low": 7.074375,
        "ci95_high": 9.775,
        "min": 0.0,
        "max": 17.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 11.25,
        "median": 11.0,
        "std": 5.893852729751567,
        "ci95_low": 9.449375,
        "ci95_high": 12.975624999999999,
        "min": 0.0,
        "max": 24.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.07856507879543455,
        "median": 0.0772167487684729,
        "std": 0.04055671712569507,
        "ci95_low": 0.0660796496386496,
        "ci95_high": 0.09056862458712821,
        "min": 0.0,
        "max": 0.1643835616438356
      }
    },
    "12": {
      "modified_count": {
        "n": 40,
        "mean": 67.675,
        "median": 69.0,
        "std": 18.15679969047409,
        "ci95_low": 62.071875000000006,
        "ci95_high": 73.60187499999999,
        "min": 16.0,
        "max": 98.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 5.175,
        "median": 5.0,
        "std": 3.169286197237479,
        "ci95_low": 4.249375,
        "ci95_high": 6.2,
        "min": 0.0,
        "max": 13.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 7.075,
        "median": 7.0,
        "std": 4.326589303365875,
        "ci95_low": 5.749375,
        "ci95_high": 8.400625,
        "min": 0.0,
        "max": 19.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.04485224219042207,
        "median": 0.047115688666034244,
        "std": 0.027433125821362498,
        "ci95_low": 0.03708142789246283,
        "ci95_high": 0.053728729032813914,
        "min": 0.0,
        "max": 0.12179487179487179
      }
    },
    "14": {
      "modified_count": {
        "n": 40,
        "mean": 71.4,
        "median": 72.0,
        "std": 19.355619339096332,
        "ci95_low": 64.6,
        "ci95_high": 77.125,
        "min": 16.0,
        "max": 106.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 3.375,
        "median": 3.0,
        "std": 2.556242359401784,
        "ci95_low": 2.525,
        "ci95_high": 4.15,
        "min": 0.0,
        "max": 10.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 4.7,
        "median": 4.0,
        "std": 3.854867053479277,
        "ci95_low": 3.424375,
        "ci95_high": 5.875,
        "min": 0.0,
        "max": 14.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.02773034013625183,
        "median": 0.024169404892296457,
        "std": 0.022595517838093403,
        "ci95_low": 0.020667825097564783,
        "ci95_high": 0.03480337765192018,
        "min": 0.0,
        "max": 0.08092485549132948
      }
    },
    "18": {
      "modified_count": {
        "n": 40,
        "mean": 75.875,
        "median": 75.0,
        "std": 21.953573171581887,
        "ci95_low": 69.198125,
        "ci95_high": 82.450625,
        "min": 16.0,
        "max": 119.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 1.925,
        "median": 1.0,
        "std": 2.3599523300270286,
        "ci95_low": 1.2,
        "ci95_high": 2.7,
        "min": 0.0,
        "max": 7.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 2.5,
        "median": 1.0,
        "std": 3.24037034920393,
        "ci95_low": 1.5493750000000002,
        "ci95_high": 3.65,
        "min": 0.0,
        "max": 11.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.012757066014316943,
        "median": 0.004777869002006933,
        "std": 0.01652695254858357,
        "ci95_low": 0.007912587533627655,
        "ci95_high": 0.01799152222258289,
        "min": 0.0,
        "max": 0.05851063829787234
      }
    },
    "22": {
      "modified_count": {
        "n": 40,
        "mean": 78.275,
        "median": 76.0,
        "std": 23.842176389751,
        "ci95_low": 70.875,
        "ci95_high": 85.15125,
        "min": 16.0,
        "max": 125.0
      },
      "modified_boundary_count": {
        "n": 40,
        "mean": 0.6,
        "median": 0.0,
        "std": 1.2206555615733703,
        "ci95_low": 0.275,
        "ci95_high": 0.9756249999999994,
        "min": 0.0,
        "max": 6.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 40,
        "mean": 0.975,
        "median": 0.0,
        "std": 2.1152718501412533,
        "ci95_low": 0.425,
        "ci95_high": 1.675,
        "min": 0.0,
        "max": 10.0
      },
      "frontier_exposed_fraction": {
        "n": 40,
        "mean": 0.004243225746982282,
        "median": 0.0,
        "std": 0.009321638886160787,
        "ci95_low": 0.0018437690302589899,
        "ci95_high": 0.0074994067868272155,
        "min": 0.0,
        "max": 0.04608294930875576
      }
    }
  },
  "status": "SUPPORTED",
  "bounded_statement": "Local inheritance kept experience-written material in contact with the active growth frontier beyond the v2 burial window."
}
```


# Stage 2 — Is Propagated State Still Causally Active Late?

```json
{
  "groups": 40,
  "late_ablation_step": 14,
  "followup_steps": 4,
  "frontier_contact_at_ablation": {
    "n": 40,
    "mean": 6.075,
    "median": 5.0,
    "std": 5.492665564186482,
    "ci95_low": 4.425,
    "ci95_high": 7.800624999999999,
    "min": 0.0,
    "max": 22.0
  },
  "visible_morphology_identical_at_ablation": true,
  "pathwise_symmetric_difference_after_followup": {
    "n": 40,
    "mean": 0.0007642023215024619,
    "median": 0.0,
    "std": 0.0011213398838817025,
    "ci95_low": 0.0004600717169017786,
    "ci95_high": 0.001107079351174459,
    "min": 0.0,
    "max": 0.0037369207772795215
  },
  "primary_test": {
    "statistic": 0.2510651899941352,
    "p_value": 0.16189207195203198,
    "permutations": 1500,
    "null_mean": 0.17968337432074818,
    "null_q95": 0.31668064803729146,
    "null_q99": 0.39737106062715766
  },
  "alpha": 0.05,
  "status": "FAILED",
  "bounded_statement": "At a late step beyond the v2 burial window, erasing only propagated material state did not establish a systematic change in subsequent growth."
}
```


# Stage 3 — Does Propagated Experience Alter Later Response?

```json
{
  "groups": 40,
  "challenge_step": 14,
  "challenge_pulse_zero_index": 0,
  "observation_steps": [
    1,
    2,
    4
  ],
  "primary_endpoint": 2,
  "primary_contrast": "difference in later-pulse response between propagated-state retained and propagated-state erased branches with identical visible morphology",
  "results": {
    "1": {
      "statistic": 0.1619246714875878,
      "p_value": 0.9826782145236509,
      "permutations": 1500,
      "null_mean": 0.3012599491305881,
      "null_q95": 0.4083174701648819,
      "null_q99": 0.4414184120919785
    },
    "2": {
      "statistic": 0.20254827531668212,
      "p_value": 0.8001332445036642,
      "permutations": 1500,
      "null_mean": 0.2558175923246884,
      "null_q95": 0.36159631001696013,
      "null_q99": 0.3984155962499989
    },
    "4": {
      "statistic": 0.19443949612510714,
      "p_value": 0.3251165889407062,
      "permutations": 1500,
      "null_mean": 0.1773820435001114,
      "null_q95": 0.24879782050051547,
      "null_q99": 0.26431874013262757
    }
  },
  "primary_test": {
    "statistic": 0.20254827531668212,
    "p_value": 0.8001332445036642,
    "permutations": 1500,
    "null_mean": 0.2558175923246884,
    "null_q95": 0.36159631001696013,
    "null_q99": 0.3984155962499989
  },
  "alpha": 0.05,
  "status": "FAILED",
  "bounded_statement": "Retained propagated material state did not establish a changed morphology response to a later identical pulse under this exploratory protocol."
}
```


# Stage 4 — Bounded Chapter 18 V3 Verdict

```json
{
  "experiment_role": "EXPLORATORY MECHANISM EXTENSION",
  "chapter": 18,
  "question": "Can experience-written material state propagate with growth and remain causally accessible?",
  "stage_1_propagated_accessibility": "SUPPORTED",
  "stage_2_late_causal_ablation": "FAILED",
  "stage_3_later_response_modulation": "FAILED",
  "final_status": "FAILED",
  "bounded_claim": "V3 tests one local propagation rule: newly attached material may inherit experience-written state from adjacent modified material. It tests whether that keeps the state causally accessible beyond the v2 burial window and whether retained propagated state matters later.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "information storage",
    "genetic inheritance",
    "epigenetics",
    "signalling",
    "semantics",
    "agency",
    "individuality",
    "reproduction",
    "life"
  ],
  "next_question": "Propagation preserved frontier contact but the late retained state was not shown to be causally active."
}
```
