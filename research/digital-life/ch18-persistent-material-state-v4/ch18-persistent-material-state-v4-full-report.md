# Chapter 18 — Can Experience Change the Material? (V4 Propagation Mechanics)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v4",
  "schema_version": 4,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY MECHANISM CHARACTERIZATION",
  "profile": "quick",
  "profile_config": {
    "groups": 40,
    "radius": 64,
    "warmup_steps": 14,
    "experience_pulse_step": 3,
    "message_gain": 0.65,
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "inheritance_sweep": [
      0.0,
      0.25,
      0.5,
      0.75,
      1.0
    ],
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
    "cell_audit_steps": [
      8,
      10,
      12,
      14,
      18
    ],
    "late_ablation_step": 14,
    "late_ablation_followup": 4,
    "permutations": 1500,
    "bootstrap_reps": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260817,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "v3_result_being_explained": "Local inheritance extended frontier contact, but the late retained-vs-erased whole-crystal ablation did not establish a systematic population-level effect.",
  "v4_design": "Predeclared inheritance-probability sweep plus direct cell-level frontier causal audit. The sweep characterizes propagation regimes and is not used to select a winner by significance.",
  "scientific_boundary": "Mechanistic characterization only. No claim of memory, learning, adaptation, phase transition, criticality, or biological inheritance.",
  "started_at_unix": 1786538935.7575896,
  "finished_at_unix": 1786538962.089829,
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "MEASURED",
  "next_question": "Use the mechanism map to decide whether the next intervention should target propagation availability, local causal gain, or surface-biased state transmission. Do not choose solely from a significance result."
}
```

# Stage 0 — V4 Mechanism Characterization Audit

```json
{
  "role": "V4 MECHANISM CHARACTERIZATION AUDIT",
  "canonical_model_modified": false,
  "inheritance_sweep": [
    0.0,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "exact_reproducibility_by_inheritance_probability": {
    "0.0": true,
    "0.25": true,
    "0.5": true,
    "0.75": true,
    "1.0": true
  },
  "all_sweep_regimes_exactly_reproducible": true,
  "zero_inheritance_limiting_case": {
    "inheritance_probability": 0.0,
    "interpretation": "At p=0, material may still be written by the original pulse and affect nearby growth, but no newly attached cell inherits state."
  },
  "scientific_role": "Characterize accessibility and direct causal leverage across a predeclared inheritance sweep; do not select the best regime by significance."
}
```


# Stage 1 — How Does Local Inheritance Change Frontier Access?

```json
{
  "groups_per_regime": 40,
  "inheritance_sweep": [
    0.0,
    0.25,
    0.5,
    0.75,
    1.0
  ],
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
  "results": {
    "0.0": {
      "inheritance_probability": 0.0,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.2,
            "ci95_high": 22.625625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.125,
            "ci95_high": 22.526874999999997,
            "min": 10.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.7,
            "median": 36.0,
            "std": 9.368030742904295,
            "ci95_low": 34.824375,
            "ci95_high": 40.75125,
            "min": 21.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.361760715820698,
            "median": 0.3574705111402359,
            "std": 0.08400739267131417,
            "ci95_low": 0.3369356265012413,
            "ci95_high": 0.3878350756013021,
            "min": 0.2,
            "max": 0.5727272727272728
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.174375,
            "ci95_high": 22.65,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 12.55,
            "median": 12.0,
            "std": 3.535180334862707,
            "ci95_low": 11.55,
            "ci95_high": 13.6,
            "min": 6.0,
            "max": 22.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 17.425,
            "median": 17.0,
            "std": 4.6951437677668615,
            "ci95_low": 16.0,
            "ci95_high": 18.875625,
            "min": 8.0,
            "max": 32.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.15807925387286156,
            "median": 0.1581140350877193,
            "std": 0.04018771463351347,
            "ci95_low": 0.14586108092452296,
            "ci95_high": 0.17108158999591302,
            "min": 0.07766990291262135,
            "max": 0.2882882882882883
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.249375,
            "ci95_high": 22.55125,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 6.0,
            "median": 6.0,
            "std": 2.3021728866442674,
            "ci95_low": 5.35,
            "ci95_high": 6.675,
            "min": 1.0,
            "max": 11.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 7.225,
            "median": 7.5,
            "std": 2.919653232834338,
            "ci95_low": 6.399375,
            "ci95_high": 8.1,
            "min": 1.0,
            "max": 13.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.06144386312307568,
            "median": 0.061629589437511303,
            "std": 0.02348192741622716,
            "ci95_low": 0.054133786647006216,
            "ci95_high": 0.06869909130073092,
            "min": 0.008547008547008548,
            "max": 0.1111111111111111
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.175,
            "ci95_high": 22.725625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 2.575,
            "median": 2.0,
            "std": 1.464368464560747,
            "ci95_low": 2.15,
            "ci95_high": 3.0256249999999993,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 2.75,
            "median": 2.0,
            "std": 1.6545392107774297,
            "ci95_low": 2.224375,
            "ci95_high": 3.2256249999999995,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.022189609531411934,
            "median": 0.017869964100518547,
            "std": 0.013123937798737252,
            "ci95_low": 0.01828240536559533,
            "ci95_high": 0.026523672723336677,
            "min": 0.0,
            "max": 0.05
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.125,
            "ci95_high": 22.7,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.675,
            "median": 0.5,
            "std": 0.7870038119348597,
            "ci95_low": 0.45,
            "ci95_high": 0.925,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.7,
            "median": 0.5,
            "std": 0.812403840463596,
            "ci95_low": 0.45,
            "ci95_high": 0.9506249999999994,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0052947804386228505,
            "median": 0.003246753246753247,
            "std": 0.006338867610576577,
            "ci95_low": 0.003356675735024252,
            "ci95_high": 0.00734636667631254,
            "min": 0.0,
            "max": 0.023809523809523808
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.249375,
            "ci95_high": 22.675,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.33071891388307384,
            "ci95_low": 0.025,
            "ci95_high": 0.225,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.33071891388307384,
            "ci95_low": 0.025,
            "ci95_high": 0.225,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0008678277405795392,
            "median": 0.0,
            "std": 0.002299305863681815,
            "ci95_low": 0.0001851851851851852,
            "ci95_high": 0.001721232083979386,
            "min": 0.0,
            "max": 0.007407407407407408
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.15,
            "ci95_high": 22.650624999999998,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.0,
            "ci95_high": 22.525,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.075,
            "ci95_high": 22.425625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.2,
            "ci95_high": 22.55125,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 10,
        "positive_contact_observed_through_final_step": false
      }
    },
    "0.25": {
      "inheritance_probability": 0.25,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.8,
            "median": 20.0,
            "std": 5.3535035257296695,
            "ci95_low": 19.173750000000002,
            "ci95_high": 22.5,
            "min": 12.0,
            "max": 36.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.8,
            "median": 20.0,
            "std": 5.3535035257296695,
            "ci95_low": 19.224375000000002,
            "ci95_high": 22.425625,
            "min": 12.0,
            "max": 36.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.475,
            "median": 38.0,
            "std": 9.24929051333128,
            "ci95_low": 34.874375,
            "ci95_high": 40.525625,
            "min": 22.0,
            "max": 57.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3475478429889579,
            "median": 0.353461738677772,
            "std": 0.06930253674030037,
            "ci95_low": 0.3244936513984902,
            "ci95_high": 0.3693309894342022,
            "min": 0.1896551724137931,
            "max": 0.49019607843137253
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 25.775,
            "median": 24.0,
            "std": 6.582125416611264,
            "ci95_low": 23.575,
            "ci95_high": 27.776874999999997,
            "min": 16.0,
            "max": 43.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 16.55,
            "median": 16.0,
            "std": 4.329838334164452,
            "ci95_low": 15.27375,
            "ci95_high": 18.025624999999998,
            "min": 9.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 24.575,
            "median": 23.0,
            "std": 6.335958885598927,
            "ci95_low": 22.724375000000002,
            "ci95_high": 26.700625,
            "min": 14.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.21689010019043878,
            "median": 0.21588702559576345,
            "std": 0.04728831164968044,
            "ci95_low": 0.2023921054764732,
            "ci95_high": 0.2317782542339687,
            "min": 0.12903225806451613,
            "max": 0.3161764705882353
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 29.225,
            "median": 28.5,
            "std": 7.558066882477291,
            "ci95_low": 26.8,
            "ci95_high": 31.550625,
            "min": 17.0,
            "max": 49.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 10.925,
            "median": 11.0,
            "std": 2.9102190639194156,
            "ci95_low": 10.025,
            "ci95_high": 11.775,
            "min": 5.0,
            "max": 17.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 14.85,
            "median": 14.5,
            "std": 4.2340878592679205,
            "ci95_low": 13.624375,
            "ci95_high": 16.1,
            "min": 6.0,
            "max": 23.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.1256703988873918,
            "median": 0.12784849913562785,
            "std": 0.035408797780417146,
            "ci95_low": 0.1143095238123652,
            "ci95_high": 0.1369484883071072,
            "min": 0.05128205128205128,
            "max": 0.20224719101123595
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 31.675,
            "median": 30.5,
            "std": 7.991831767498613,
            "ci95_low": 29.225,
            "ci95_high": 34.2,
            "min": 19.0,
            "max": 53.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 7.4,
            "median": 7.0,
            "std": 2.4269322199023193,
            "ci95_low": 6.649375,
            "ci95_high": 8.15,
            "min": 3.0,
            "max": 13.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 9.7,
            "median": 9.0,
            "std": 3.6482872693909396,
            "ci95_low": 8.574375,
            "ci95_high": 10.975,
            "min": 2.0,
            "max": 18.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.07751669587087825,
            "median": 0.07200460829493088,
            "std": 0.02769113997997241,
            "ci95_low": 0.06930837799747097,
            "ci95_high": 0.0864758930338925,
            "min": 0.017241379310344827,
            "max": 0.14285714285714285
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 33.45,
            "median": 33.0,
            "std": 8.58181216294088,
            "ci95_low": 30.849375000000002,
            "ci95_high": 36.3,
            "min": 20.0,
            "max": 57.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 4.85,
            "median": 4.0,
            "std": 2.5937424698685874,
            "ci95_low": 4.1743749999999995,
            "ci95_high": 5.650625,
            "min": 1.0,
            "max": 12.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 6.35,
            "median": 5.5,
            "std": 3.8700775186034706,
            "ci95_low": 5.274375,
            "ci95_high": 7.5,
            "min": 1.0,
            "max": 17.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.04814847966514973,
            "median": 0.040884438881935756,
            "std": 0.029057108895310983,
            "ci95_low": 0.039801402935838386,
            "ci95_high": 0.05749318944044632,
            "min": 0.007462686567164179,
            "max": 0.12781954887218044
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 35.1,
            "median": 35.0,
            "std": 9.248783703817491,
            "ci95_low": 32.125,
            "ci95_high": 38.125,
            "min": 20.0,
            "max": 59.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 1.6,
            "median": 1.0,
            "std": 1.7146428199482249,
            "ci95_low": 1.125,
            "ci95_high": 2.15,
            "min": 0.0,
            "max": 7.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 2.1,
            "median": 1.0,
            "std": 2.211334438749598,
            "ci95_low": 1.45,
            "ci95_high": 2.825,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.014396448582310428,
            "median": 0.00766384778012685,
            "std": 0.015304573315389357,
            "ci95_low": 0.009937254190633047,
            "ci95_high": 0.019721341217510194,
            "min": 0.0,
            "max": 0.056338028169014086
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 35.475,
            "median": 35.0,
            "std": 9.646210395797928,
            "ci95_low": 32.499375,
            "ci95_high": 38.302499999999995,
            "min": 20.0,
            "max": 62.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.45,
            "median": 0.0,
            "std": 0.6689544080129827,
            "ci95_low": 0.25,
            "ci95_high": 0.675,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.5,
            "median": 0.0,
            "std": 0.7745966692414834,
            "ci95_low": 0.275,
            "ci95_high": 0.75,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.003048209625534355,
            "median": 0.0,
            "std": 0.004660046047940022,
            "ci95_low": 0.0016934849742615173,
            "ci95_high": 0.004524303871388102,
            "min": 0.0,
            "max": 0.016853932584269662
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.675,
            "ci95_high": 38.675625,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.3992179855667828,
            "ci95_low": 0.025,
            "ci95_high": 0.275,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.3992179855667828,
            "ci95_low": 0.025,
            "ci95_high": 0.275,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0007026083227689283,
            "median": 0.0,
            "std": 0.002222963478596978,
            "ci95_low": 0.00012690355329949237,
            "ci95_high": 0.0013979426911898737,
            "min": 0.0,
            "max": 0.010810810810810811
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.59875,
            "ci95_high": 38.55437499999999,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.7,
            "ci95_high": 38.350625,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 14,
        "positive_contact_observed_through_final_step": false
      }
    },
    "0.5": {
      "inheritance_probability": 0.5,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.075,
            "median": 20.0,
            "std": 3.7241609793348083,
            "ci95_low": 18.9,
            "ci95_high": 21.25,
            "min": 13.0,
            "max": 29.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.075,
            "median": 20.0,
            "std": 3.7241609793348083,
            "ci95_low": 19.05,
            "ci95_high": 21.15,
            "min": 13.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.525,
            "median": 37.0,
            "std": 7.338213338408744,
            "ci95_low": 34.175,
            "ci95_high": 38.77625,
            "min": 19.0,
            "max": 51.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3462007510950557,
            "median": 0.35764235764235763,
            "std": 0.0648669700674378,
            "ci95_low": 0.32410848372497125,
            "ci95_high": 0.36604949339973036,
            "min": 0.1919191919191919,
            "max": 0.4434782608695652
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 29.575,
            "median": 30.5,
            "std": 5.826180137963466,
            "ci95_low": 27.649375,
            "ci95_high": 31.47625,
            "min": 16.0,
            "max": 41.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.275,
            "median": 20.0,
            "std": 4.549656580446484,
            "ci95_low": 18.925,
            "ci95_high": 21.650624999999998,
            "min": 10.0,
            "max": 31.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 30.375,
            "median": 31.5,
            "std": 7.488950193451683,
            "ci95_low": 28.19875,
            "ci95_high": 32.7,
            "min": 13.0,
            "max": 44.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.27120995451174457,
            "median": 0.2758130081300813,
            "std": 0.06721460523330179,
            "ci95_low": 0.25090284276689345,
            "ci95_high": 0.2910462576554872,
            "min": 0.11607142857142858,
            "max": 0.4077669902912621
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 37.85,
            "median": 40.0,
            "std": 7.808809128157764,
            "ci95_low": 35.374375,
            "ci95_high": 40.325,
            "min": 19.0,
            "max": 55.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 18.375,
            "median": 18.0,
            "std": 5.829611908180509,
            "ci95_low": 16.624375,
            "ci95_high": 20.2,
            "min": 6.0,
            "max": 35.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 25.825,
            "median": 26.0,
            "std": 7.469563240243702,
            "ci95_low": 23.599375000000002,
            "ci95_high": 28.225,
            "min": 11.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.21843994026565933,
            "median": 0.21008403361344535,
            "std": 0.0626062192376864,
            "ci95_low": 0.1992858979437625,
            "ci95_high": 0.23682320705156115,
            "min": 0.09166666666666666,
            "max": 0.3706896551724138
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 45.125,
            "median": 47.5,
            "std": 9.836634332941324,
            "ci95_low": 42.15,
            "ci95_high": 47.9,
            "min": 22.0,
            "max": 68.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 15.875,
            "median": 16.0,
            "std": 5.670923646109159,
            "ci95_low": 14.124375,
            "ci95_high": 17.725625,
            "min": 6.0,
            "max": 31.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 21.875,
            "median": 21.0,
            "std": 8.179815095709682,
            "ci95_low": 19.173125000000002,
            "ci95_high": 24.526249999999997,
            "min": 9.0,
            "max": 41.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.17674697099027975,
            "median": 0.16613508442776737,
            "std": 0.06743808991847347,
            "ci95_low": 0.15614938548797058,
            "ci95_high": 0.1981276873354824,
            "min": 0.07874015748031496,
            "max": 0.33064516129032256
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 51.4,
            "median": 54.5,
            "std": 11.410083259994206,
            "ci95_low": 47.84875,
            "ci95_high": 54.975,
            "min": 27.0,
            "max": 79.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 14.225,
            "median": 14.0,
            "std": 5.565462694152212,
            "ci95_low": 12.55,
            "ci95_high": 16.05,
            "min": 4.0,
            "max": 26.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 18.6,
            "median": 18.5,
            "std": 7.611832893594027,
            "ci95_low": 16.324375,
            "ci95_high": 20.92625,
            "min": 5.0,
            "max": 33.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.1432114382157458,
            "median": 0.13194205885720828,
            "std": 0.060111768632458415,
            "ci95_low": 0.12550232666024388,
            "ci95_high": 0.1598471583686987,
            "min": 0.03875968992248062,
            "max": 0.25984251968503935
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 60.675,
            "median": 63.5,
            "std": 14.455773068224333,
            "ci95_low": 56.52375,
            "ci95_high": 65.375625,
            "min": 29.0,
            "max": 94.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 9.725,
            "median": 9.0,
            "std": 5.044737356889851,
            "ci95_low": 8.199375,
            "ci95_high": 11.425,
            "min": 1.0,
            "max": 19.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 12.65,
            "median": 12.0,
            "std": 6.941001368678729,
            "ci95_low": 10.42375,
            "ci95_high": 14.925,
            "min": 2.0,
            "max": 24.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0895245912099216,
            "median": 0.0871309443317557,
            "std": 0.05039136769357663,
            "ci95_low": 0.07341023389167922,
            "ci95_high": 0.10430521643988283,
            "min": 0.013513513513513514,
            "max": 0.17518248175182483
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 66.85,
            "median": 67.5,
            "std": 17.355906775504415,
            "ci95_low": 61.5,
            "ci95_high": 72.125625,
            "min": 31.0,
            "max": 102.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 6.3,
            "median": 5.0,
            "std": 4.1844951905815355,
            "ci95_low": 5.0,
            "ci95_high": 7.675,
            "min": 0.0,
            "max": 17.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 8.9,
            "median": 7.0,
            "std": 5.847221562417487,
            "ci95_low": 7.074375,
            "ci95_high": 10.75,
            "min": 0.0,
            "max": 22.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.05802481262704477,
            "median": 0.046052631578947366,
            "std": 0.03834306532434202,
            "ci95_low": 0.04684894956123461,
            "ci95_high": 0.07024177991473286,
            "min": 0.0,
            "max": 0.14666666666666667
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 71.35,
            "median": 70.0,
            "std": 19.79715888707266,
            "ci95_low": 65.0975,
            "ci95_high": 77.575,
            "min": 32.0,
            "max": 108.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 4.15,
            "median": 4.0,
            "std": 2.9372606285449034,
            "ci95_low": 3.225,
            "ci95_high": 5.050624999999999,
            "min": 0.0,
            "max": 10.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 5.825,
            "median": 4.5,
            "std": 4.247867111857432,
            "ci95_low": 4.5493749999999995,
            "ci95_high": 7.150625,
            "min": 0.0,
            "max": 14.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.034138697552143646,
            "median": 0.028853344412131283,
            "std": 0.02450950314556512,
            "ci95_low": 0.026158899862608442,
            "ci95_high": 0.04182495684613217,
            "min": 0.0,
            "max": 0.08139534883720931
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 75.975,
            "median": 78.0,
            "std": 22.033483042860016,
            "ci95_low": 68.99875,
            "ci95_high": 82.925625,
            "min": 34.0,
            "max": 119.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 1.25,
            "median": 0.5,
            "std": 1.7571283390805579,
            "ci95_low": 0.725,
            "ci95_high": 1.825,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 1.4,
            "median": 0.5,
            "std": 2.1071307505705477,
            "ci95_low": 0.775,
            "ci95_high": 2.05,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.007166952885266411,
            "median": 0.0024271844660194173,
            "std": 0.010739223817368427,
            "ci95_low": 0.004013807475842895,
            "ci95_high": 0.01060018094782162,
            "min": 0.0,
            "max": 0.043010752688172046
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 76.975,
            "median": 78.0,
            "std": 22.73817000112366,
            "ci95_low": 69.52187500000001,
            "ci95_high": 83.92625,
            "min": 34.0,
            "max": 123.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.425,
            "median": 0.0,
            "std": 0.9457140159688869,
            "ci95_low": 0.17437500000000003,
            "ci95_high": 0.7256249999999994,
            "min": 0.0,
            "max": 4.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.6,
            "median": 0.0,
            "std": 1.3564659966250536,
            "ci95_low": 0.22437500000000005,
            "ci95_high": 1.025,
            "min": 0.0,
            "max": 5.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.002646748542028629,
            "median": 0.0,
            "std": 0.0059569890393780175,
            "ci95_low": 0.0009075667307714587,
            "ci95_high": 0.004594108870338635,
            "min": 0.0,
            "max": 0.02127659574468085
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "0.75": {
      "inheritance_probability": 0.75,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.0,
            "median": 19.0,
            "std": 5.371219600798314,
            "ci95_low": 18.225,
            "ci95_high": 21.8,
            "min": 10.0,
            "max": 30.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.0,
            "median": 19.0,
            "std": 5.371219600798314,
            "ci95_low": 18.375,
            "ci95_high": 21.675,
            "min": 10.0,
            "max": 30.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.85,
            "median": 37.0,
            "std": 10.011368537817395,
            "ci95_low": 33.85,
            "ci95_high": 39.825625,
            "min": 19.0,
            "max": 64.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.34738285078540515,
            "median": 0.354502688172043,
            "std": 0.07316301905555381,
            "ci95_low": 0.3244745186281786,
            "ci95_high": 0.3691423194669471,
            "min": 0.21839080459770116,
            "max": 0.5039370078740157
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 34.625,
            "median": 33.0,
            "std": 10.221759877829257,
            "ci95_low": 31.274375,
            "ci95_high": 37.9,
            "min": 15.0,
            "max": 60.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 24.575,
            "median": 25.0,
            "std": 7.422558521156974,
            "ci95_low": 22.374375,
            "ci95_high": 26.925625,
            "min": 14.0,
            "max": 44.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.8,
            "median": 37.0,
            "std": 11.238772174930853,
            "ci95_low": 34.375,
            "ci95_high": 41.45,
            "min": 23.0,
            "max": 65.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.33424643576514657,
            "median": 0.32366946778711486,
            "std": 0.0818358580385646,
            "ci95_low": 0.3096100258706744,
            "ci95_high": 0.3610951551406001,
            "min": 0.20175438596491227,
            "max": 0.52
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 49.625,
            "median": 48.0,
            "std": 14.848716274479758,
            "ci95_low": 45.175,
            "ci95_high": 54.251875,
            "min": 25.0,
            "max": 91.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.125,
            "median": 26.5,
            "std": 9.423872611617796,
            "ci95_low": 25.249375,
            "ci95_high": 30.92625,
            "min": 14.0,
            "max": 54.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 38.5,
            "median": 36.0,
            "std": 12.216791722870616,
            "ci95_low": 34.899375,
            "ci95_high": 42.501875,
            "min": 19.0,
            "max": 67.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.31901027612690436,
            "median": 0.3170712729536259,
            "std": 0.08541925063394994,
            "ci95_low": 0.2909404382831104,
            "ci95_high": 0.34598615412957,
            "min": 0.17272727272727273,
            "max": 0.5275590551181102
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 65.175,
            "median": 62.0,
            "std": 18.100949560727468,
            "ci95_low": 59.774375,
            "ci95_high": 70.725,
            "min": 36.0,
            "max": 109.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.95,
            "median": 27.0,
            "std": 9.211270270706423,
            "ci95_low": 26.298750000000002,
            "ci95_high": 32.100625,
            "min": 14.0,
            "max": 54.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.475,
            "median": 35.0,
            "std": 11.48039089055769,
            "ci95_low": 34.249375,
            "ci95_high": 41.300625,
            "min": 19.0,
            "max": 71.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3003617875609548,
            "median": 0.2898134354827268,
            "std": 0.08480429042329078,
            "ci95_low": 0.2751931645017873,
            "ci95_high": 0.3258541697609168,
            "min": 0.16101694915254236,
            "max": 0.5867768595041323
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 80.725,
            "median": 76.5,
            "std": 22.770581349627417,
            "ci95_low": 74.19875,
            "ci95_high": 88.275,
            "min": 45.0,
            "max": 138.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 29.0,
            "median": 26.5,
            "std": 9.818350166906862,
            "ci95_low": 26.075,
            "ci95_high": 32.550625,
            "min": 15.0,
            "max": 59.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.875,
            "median": 33.0,
            "std": 12.215128939147553,
            "ci95_low": 33.424375,
            "ci95_high": 40.62625,
            "min": 18.0,
            "max": 78.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2818112448020319,
            "median": 0.26072337331879314,
            "std": 0.09216462918301724,
            "ci95_low": 0.2551908939580435,
            "ci95_high": 0.31332006444297594,
            "min": 0.13768115942028986,
            "max": 0.6290322580645161
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 111.2,
            "median": 105.5,
            "std": 31.928983698201232,
            "ci95_low": 101.6,
            "ci95_high": 121.829375,
            "min": 62.0,
            "max": 182.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.825,
            "median": 26.0,
            "std": 10.384814634840623,
            "ci95_low": 25.473750000000003,
            "ci95_high": 32.100625,
            "min": 12.0,
            "max": 55.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 35.575,
            "median": 32.0,
            "std": 12.90326993440035,
            "ci95_low": 31.849375000000002,
            "ci95_high": 39.625,
            "min": 14.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2483835640520417,
            "median": 0.22428571428571428,
            "std": 0.08934520381401347,
            "ci95_low": 0.22103871482570983,
            "ci95_high": 0.2774281149529019,
            "min": 0.08333333333333333,
            "max": 0.4632352941176471
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 139.075,
            "median": 131.0,
            "std": 42.128605186974795,
            "ci95_low": 126.4,
            "ci95_high": 152.23,
            "min": 75.0,
            "max": 240.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 26.125,
            "median": 25.0,
            "std": 11.106726565464731,
            "ci95_low": 22.675,
            "ci95_high": 29.775,
            "min": 6.0,
            "max": 48.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 32.775,
            "median": 30.5,
            "std": 13.374392509568425,
            "ci95_low": 28.725,
            "ci95_high": 37.300625,
            "min": 7.0,
            "max": 61.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2111649760664962,
            "median": 0.19535465192788526,
            "std": 0.08866085715589539,
            "ci95_low": 0.1845433745230467,
            "ci95_high": 0.23869950356023417,
            "min": 0.051094890510948905,
            "max": 0.44696969696969696
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 165.3,
            "median": 157.0,
            "std": 50.35583382290477,
            "ci95_low": 150.574375,
            "ci95_high": 181.156875,
            "min": 91.0,
            "max": 286.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 24.65,
            "median": 22.5,
            "std": 10.460760010630201,
            "ci95_low": 21.524375,
            "ci95_high": 27.675625,
            "min": 3.0,
            "max": 47.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 29.55,
            "median": 25.5,
            "std": 12.391428489080667,
            "ci95_low": 25.749375,
            "ci95_high": 33.450625,
            "min": 4.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.17587378773939083,
            "median": 0.15350347327091513,
            "std": 0.07742017801051847,
            "ci95_low": 0.1521652053012979,
            "ci95_high": 0.201869193387911,
            "min": 0.026143790849673203,
            "max": 0.39473684210526316
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 214.925,
            "median": 201.0,
            "std": 69.01282036694342,
            "ci95_low": 194.773125,
            "ci95_high": 239.2275,
            "min": 109.0,
            "max": 399.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 21.3,
            "median": 19.0,
            "std": 11.303096920755832,
            "ci95_low": 18.125,
            "ci95_high": 24.825,
            "min": 5.0,
            "max": 59.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 26.2,
            "median": 23.5,
            "std": 12.649505919204907,
            "ci95_low": 22.3725,
            "ci95_high": 29.903749999999995,
            "min": 7.0,
            "max": 70.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.13379520043206433,
            "median": 0.11618544600938968,
            "std": 0.06521415829667544,
            "ci95_low": 0.11483147419005031,
            "ci95_high": 0.15448703686159068,
            "min": 0.03825136612021858,
            "max": 0.37433155080213903
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 255.675,
            "median": 241.0,
            "std": 83.10216227632107,
            "ci95_low": 231.08625,
            "ci95_high": 281.010625,
            "min": 123.0,
            "max": 493.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 17.6,
            "median": 17.0,
            "std": 8.952094726934027,
            "ci95_low": 14.87375,
            "ci95_high": 20.525,
            "min": 3.0,
            "max": 39.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 21.725,
            "median": 22.0,
            "std": 10.693426719251411,
            "ci95_low": 18.474375000000002,
            "ci95_high": 24.975,
            "min": 4.0,
            "max": 48.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.09678742363362122,
            "median": 0.09913056978730012,
            "std": 0.04790244584915415,
            "ci95_low": 0.08375106406869474,
            "ci95_high": 0.11167717980766638,
            "min": 0.01680672268907563,
            "max": 0.2191780821917808
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "1.0": {
      "inheritance_probability": 1.0,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 19.775,
            "median": 21.0,
            "std": 3.9842659298796814,
            "ci95_low": 18.599375000000002,
            "ci95_high": 20.925625,
            "min": 12.0,
            "max": 29.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 19.775,
            "median": 21.0,
            "std": 3.9842659298796814,
            "ci95_low": 18.574375,
            "ci95_high": 20.975625,
            "min": 12.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 34.875,
            "median": 35.0,
            "std": 7.057575716915831,
            "ci95_low": 32.65,
            "ci95_high": 36.900625,
            "min": 19.0,
            "max": 49.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3352281348476909,
            "median": 0.32868672046955244,
            "std": 0.06808161006518071,
            "ci95_low": 0.3143707390500136,
            "ci95_high": 0.35648375846590796,
            "min": 0.19791666666666666,
            "max": 0.47
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 38.65,
            "median": 38.0,
            "std": 7.564885987243958,
            "ci95_low": 36.324375,
            "ci95_high": 40.925625,
            "min": 24.0,
            "max": 55.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 27.325,
            "median": 27.0,
            "std": 5.845457638200794,
            "ci95_low": 25.525,
            "ci95_high": 29.225,
            "min": 15.0,
            "max": 41.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 41.0,
            "median": 40.0,
            "std": 9.31933474020544,
            "ci95_low": 38.1,
            "ci95_high": 43.7,
            "min": 21.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3730098582001807,
            "median": 0.37226071543667416,
            "std": 0.08315494736944008,
            "ci95_low": 0.3471577281626002,
            "ci95_high": 0.39934280030877545,
            "min": 0.20192307692307693,
            "max": 0.5431034482758621
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 61.125,
            "median": 60.0,
            "std": 12.225357867972617,
            "ci95_low": 57.024375,
            "ci95_high": 64.95,
            "min": 34.0,
            "max": 90.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 35.45,
            "median": 35.5,
            "std": 9.148633777783434,
            "ci95_low": 32.774375,
            "ci95_high": 38.250625,
            "min": 16.0,
            "max": 56.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 46.85,
            "median": 47.0,
            "std": 11.678077752781062,
            "ci95_low": 43.324375,
            "ci95_high": 50.4,
            "min": 23.0,
            "max": 72.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4036352485798368,
            "median": 0.4105263157894737,
            "std": 0.09902371146485782,
            "ci95_low": 0.37083439925280554,
            "ci95_high": 0.43282103890830637,
            "min": 0.20175438596491227,
            "max": 0.5849056603773585
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 87.3,
            "median": 86.0,
            "std": 18.9,
            "ci95_low": 81.65,
            "ci95_high": 92.925625,
            "min": 44.0,
            "max": 132.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 43.275,
            "median": 42.0,
            "std": 11.063425102562045,
            "ci95_low": 39.924375,
            "ci95_high": 46.900625,
            "min": 22.0,
            "max": 68.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 53.0,
            "median": 52.5,
            "std": 13.171939872319491,
            "ci95_low": 49.123125,
            "ci95_high": 56.9,
            "min": 24.0,
            "max": 81.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4324343496013679,
            "median": 0.436309177136201,
            "std": 0.10645914799279534,
            "ci95_low": 0.39928619039695507,
            "ci95_high": 0.465158914888891,
            "min": 0.20512820512820512,
            "max": 0.6136363636363636
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 116.25,
            "median": 115.0,
            "std": 24.89251895650579,
            "ci95_low": 109.02312500000001,
            "ci95_high": 123.900625,
            "min": 63.0,
            "max": 173.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 48.975,
            "median": 48.0,
            "std": 12.616432736712863,
            "ci95_low": 45.074375,
            "ci95_high": 52.65125,
            "min": 16.0,
            "max": 73.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 57.625,
            "median": 60.0,
            "std": 14.669164086613797,
            "ci95_low": 53.17375,
            "ci95_high": 62.203125,
            "min": 21.0,
            "max": 88.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4491073182293935,
            "median": 0.4439408396946565,
            "std": 0.1149146683386463,
            "ci95_low": 0.41237876433028514,
            "ci95_high": 0.4860119503741235,
            "min": 0.1640625,
            "max": 0.676923076923077
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 183.1,
            "median": 182.0,
            "std": 39.51695838497695,
            "ci95_low": 170.44062499999998,
            "ci95_high": 195.12687499999998,
            "min": 93.0,
            "max": 266.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 61.45,
            "median": 60.0,
            "std": 17.804423607631897,
            "ci95_low": 56.14875,
            "ci95_high": 66.825,
            "min": 16.0,
            "max": 95.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 68.925,
            "median": 67.5,
            "std": 19.176010403626716,
            "ci95_low": 63.09875,
            "ci95_high": 75.07625,
            "min": 16.0,
            "max": 106.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.48551001136753624,
            "median": 0.48343143666884675,
            "std": 0.1367362671977677,
            "ci95_low": 0.44158551581761785,
            "ci95_high": 0.5249913887107337,
            "min": 0.11940298507462686,
            "max": 0.7464788732394366
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 261.975,
            "median": 262.0,
            "std": 58.82367189320979,
            "ci95_low": 244.77125,
            "ci95_high": 279.055,
            "min": 115.0,
            "max": 385.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 71.6,
            "median": 72.5,
            "std": 20.003499693803583,
            "ci95_low": 65.274375,
            "ci95_high": 77.35,
            "min": 20.0,
            "max": 116.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 78.65,
            "median": 79.0,
            "std": 21.00660610379506,
            "ci95_low": 72.49875,
            "ci95_high": 84.925625,
            "min": 24.0,
            "max": 126.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5124198128725554,
            "median": 0.5047985438901299,
            "std": 0.1373058283619192,
            "ci95_low": 0.46845254128184227,
            "ci95_high": 0.5531473364298962,
            "min": 0.16326530612244897,
            "max": 0.7682926829268293
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 349.1,
            "median": 353.0,
            "std": 80.18254174070563,
            "ci95_low": 322.59062500000005,
            "ci95_high": 374.051875,
            "min": 144.0,
            "max": 510.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 81.5,
            "median": 80.5,
            "std": 21.243822631532208,
            "ci95_low": 75.573125,
            "ci95_high": 87.7,
            "min": 26.0,
            "max": 116.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 87.975,
            "median": 86.5,
            "std": 22.60031802873579,
            "ci95_low": 80.47375,
            "ci95_high": 94.9525,
            "min": 30.0,
            "max": 128.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5336078729441771,
            "median": 0.5300290603810138,
            "std": 0.14407293974385085,
            "ci95_low": 0.48456661052369976,
            "ci95_high": 0.5773624601221421,
            "min": 0.17857142857142858,
            "max": 0.8311688311688312
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 556.225,
            "median": 547.0,
            "std": 133.3177571631026,
            "ci95_low": 516.198125,
            "ci95_high": 594.953125,
            "min": 228.0,
            "max": 847.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 102.775,
            "median": 104.0,
            "std": 30.103560835887837,
            "ci95_low": 93.97375,
            "ci95_high": 112.08,
            "min": 40.0,
            "max": 178.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 107.475,
            "median": 108.0,
            "std": 29.512698538086955,
            "ci95_low": 98.424375,
            "ci95_high": 116.878125,
            "min": 45.0,
            "max": 182.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.567828959215826,
            "median": 0.5651022188980304,
            "std": 0.15251645916943082,
            "ci95_low": 0.5194345328601087,
            "ci95_high": 0.6151274989619901,
            "min": 0.25280898876404495,
            "max": 0.9191919191919192
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 808.175,
            "median": 815.0,
            "std": 198.6749716874272,
            "ci95_low": 744.738125,
            "ci95_high": 867.284375,
            "min": 342.0,
            "max": 1294.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 123.375,
            "median": 123.5,
            "std": 34.63862547792565,
            "ci95_low": 113.07000000000001,
            "ci95_high": 134.05375,
            "min": 49.0,
            "max": 215.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 128.6,
            "median": 128.5,
            "std": 35.12890547682919,
            "ci95_low": 118.29875,
            "ci95_high": 139.003125,
            "min": 51.0,
            "max": 208.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5912980276425659,
            "median": 0.5883720930232559,
            "std": 0.1626868518167941,
            "ci95_low": 0.54210978661474,
            "ci95_high": 0.6386885644476149,
            "min": 0.2361111111111111,
            "max": 0.9327354260089686
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "The inheritance sweep characterizes how local propagation changes material abundance and contact with the active growth surface. It is not used to optimize or select a significance result."
}
```


# Stage 2 — What Does Modified Material Do to a Frontier Cell?

```json
{
  "groups_per_regime": 40,
  "inheritance_sweep": [
    0.0,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "audit_steps": [
    8,
    10,
    12,
    14,
    18
  ],
  "results": {
    "0.0": {
      "inheritance_probability": 0.0,
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 1.075,
            "median": 1.0,
            "std": 0.9845684333757608,
            "ci95_low": 0.75,
            "ci95_high": 1.375,
            "min": 0.0,
            "max": 3.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.008250285594518524,
            "median": 0.007326105624731644,
            "std": 0.007685642779887914,
            "ci95_low": 0.006029695247581308,
            "ci95_high": 0.010553249155846446,
            "min": 0.0,
            "max": 0.025423728813559324
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.05597649454440916,
            "median": 0.05560867347926951,
            "std": 0.05298825142320227,
            "ci95_low": 0.04035870330647941,
            "ci95_high": 0.07244640383500875,
            "min": 0.0,
            "max": 0.17545152327282126
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.03481050100382167,
            "median": 0.03644027918552967,
            "std": 0.029373358586252646,
            "ci95_low": 0.025108000596700073,
            "ci95_high": 0.04409231500647845,
            "min": 0.0,
            "max": 0.07472492797554381
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.03867923435284211,
            "median": 0.04067376313809899,
            "std": 0.032244144232132836,
            "ci95_low": 0.02875652435719822,
            "ci95_high": 0.048500156012112286,
            "min": 0.0,
            "max": 0.07484578086626126
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.33071891388307384,
            "ci95_low": 0.025,
            "ci95_high": 0.225,
            "min": 0.0,
            "max": 1.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.06666666666666667,
            "median": 0.0,
            "std": 0.19649710204252663,
            "ci95_low": 0.0125,
            "ci95_high": 0.13333333333333333,
            "min": 0.0,
            "max": 1.0
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.075,
            "median": 0.0,
            "std": 0.34550687402713137,
            "ci95_low": 0.0,
            "ci95_high": 0.2,
            "min": 0.0,
            "max": 2.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0005600106923282545,
            "median": 0.0,
            "std": 0.002623871741933694,
            "ci95_low": 0.0,
            "ci95_high": 0.0015076182838813152,
            "min": 0.0,
            "max": 0.015503875968992248
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.0031773495928787256,
            "median": 0.0,
            "std": 0.016032199592654044,
            "ci95_low": 0.0,
            "ci95_high": 0.00884625801064905,
            "min": 0.0,
            "max": 0.09966235299566395
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.001931570180432926,
            "median": 0.0,
            "std": 0.008784079320866204,
            "ci95_low": 0.0,
            "ci95_high": 0.005108919773311652,
            "min": 0.0,
            "max": 0.049831176497831975
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.001931570180432926,
            "median": 0.0,
            "std": 0.008784079320866204,
            "ci95_low": 0.0,
            "ci95_high": 0.005108919773311652,
            "min": 0.0,
            "max": 0.049831176497831975
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.05,
            "median": 0.0,
            "std": 0.3122498999199199,
            "ci95_low": 0.0,
            "ci95_high": 0.15,
            "min": 0.0,
            "max": 2.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.00034965034965034965,
            "median": 0.0,
            "std": 0.0021835657337057335,
            "ci95_low": 0.0,
            "ci95_high": 0.001048951048951049,
            "min": 0.0,
            "max": 0.013986013986013986
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.0028274134871031963,
            "median": 0.0,
            "std": 0.017657191567604095,
            "ci95_low": 0.0,
            "ci95_high": 0.008482240461309588,
            "min": 0.0,
            "max": 0.11309653948412784
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0014137067435515981,
            "median": 0.0,
            "std": 0.008828595783802047,
            "ci95_low": 0.0,
            "ci95_high": 0.004241120230654794,
            "min": 0.0,
            "max": 0.05654826974206392
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.0014314064761531784,
            "median": 0.0,
            "std": 0.008939130578471104,
            "ci95_low": 0.0,
            "ci95_high": 0.004294219428459535,
            "min": 0.0,
            "max": 0.057256259046127134
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
      }
    },
    "0.25": {
      "inheritance_probability": 0.25,
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 5.775,
            "median": 5.0,
            "std": 3.5106089215405354,
            "ci95_low": 4.725,
            "ci95_high": 6.9,
            "min": 1.0,
            "max": 17.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.043979777381777434,
            "median": 0.03571610796469207,
            "std": 0.02724962745483609,
            "ci95_low": 0.035893623215555365,
            "ci95_high": 0.05298174699074685,
            "min": 0.007692307692307693,
            "max": 0.136
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.38173491103287294,
            "median": 0.2922756906352537,
            "std": 0.2554425058945597,
            "ci95_low": 0.30646697212112606,
            "ci95_high": 0.4592925247234546,
            "min": 0.06316926411379575,
            "max": 1.2220933193862114
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.06539844508496336,
            "median": 0.0657079882886861,
            "std": 0.01464407473181665,
            "ci95_low": 0.06100032734849114,
            "ci95_high": 0.07008664542840036,
            "min": 0.040108470384932836,
            "max": 0.1046689592442505
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.09777242854011584,
            "median": 0.07438172294750903,
            "std": 0.0361659858069603,
            "ci95_low": 0.08789969297704792,
            "ci95_high": 0.1090508230587899,
            "min": 0.05477026707950261,
            "max": 0.22113103646113091
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.35,
            "median": 0.0,
            "std": 0.6144102863722254,
            "ci95_low": 0.175,
            "ci95_high": 0.55,
            "min": 0.0,
            "max": 3.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.060438842203548095,
            "median": 0.0,
            "std": 0.10910610244746641,
            "ci95_low": 0.028149305555555556,
            "ci95_high": 0.09432341269841268,
            "min": 0.0,
            "max": 0.5
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 2.1,
            "median": 1.0,
            "std": 2.1656407827707715,
            "ci95_low": 1.4743750000000002,
            "ci95_high": 2.8,
            "min": 0.0,
            "max": 8.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.014313647784643696,
            "median": 0.007144315166360482,
            "std": 0.014912309956479809,
            "ci95_low": 0.010152395483759171,
            "ci95_high": 0.019444026820233957,
            "min": 0.0,
            "max": 0.058823529411764705
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.13440957438195755,
            "median": 0.07443481158002926,
            "std": 0.15754151607700478,
            "ci95_low": 0.09103436062748116,
            "ci95_high": 0.1873442492608432,
            "min": 0.0,
            "max": 0.6947641934200295
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.041799636912662703,
            "median": 0.05504487341846644,
            "std": 0.031131689044574022,
            "ci95_low": 0.03244166101161758,
            "ci95_high": 0.05119142647345973,
            "min": 0.0,
            "max": 0.1002248737945112
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.05074727810359975,
            "median": 0.0579332021493455,
            "std": 0.04275074743138241,
            "ci95_low": 0.0375208495378888,
            "ci95_high": 0.06404670896179801,
            "min": 0.0,
            "max": 0.18014560358252418
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.05,
            "median": 0.0,
            "std": 0.21794494717703367,
            "ci95_low": 0.0,
            "ci95_high": 0.125,
            "min": 0.0,
            "max": 1.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.015625,
            "median": 0.0,
            "std": 0.0799780243254358,
            "ci95_low": 0.0,
            "ci95_high": 0.04375,
            "min": 0.0,
            "max": 0.5
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.525,
            "median": 0.0,
            "std": 0.8656644846590392,
            "ci95_low": 0.275,
            "ci95_high": 0.8,
            "min": 0.0,
            "max": 3.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.003272261359038774,
            "median": 0.0,
            "std": 0.005326041737433917,
            "ci95_low": 0.0018092915671837745,
            "ci95_high": 0.004921489638339353,
            "min": 0.0,
            "max": 0.018404907975460124
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.029638107489453835,
            "median": 0.0,
            "std": 0.054966509272953976,
            "ci95_low": 0.014645200229381773,
            "ci95_high": 0.048371463927740874,
            "min": 0.0,
            "max": 0.25543726670641737
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.017525536422538467,
            "median": 0.0,
            "std": 0.02761163749593973,
            "ci95_low": 0.008913086461595441,
            "ci95_high": 0.02620203475994451,
            "min": 0.0,
            "max": 0.08514575556880578
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.020260260036748384,
            "median": 0.0,
            "std": 0.03256449661505575,
            "ci95_low": 0.010940246955471756,
            "ci95_high": 0.031041926819994497,
            "min": 0.0,
            "max": 0.1154685441230548
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.025,
            "median": 0.0,
            "std": 0.15612494995995996,
            "ci95_low": 0.0,
            "ci95_high": 0.075,
            "min": 0.0,
            "max": 1.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0125,
            "median": 0.0,
            "std": 0.07806247497997998,
            "ci95_low": 0.0,
            "ci95_high": 0.0375,
            "min": 0.0,
            "max": 0.5
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.175,
            "median": 0.0,
            "std": 0.4408798022137099,
            "ci95_low": 0.05,
            "ci95_high": 0.325,
            "min": 0.0,
            "max": 2.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0009922488383605859,
            "median": 0.0,
            "std": 0.0024936213299793747,
            "ci95_low": 0.0002810846560846561,
            "ci95_high": 0.0018444375200559584,
            "min": 0.0,
            "max": 0.0111731843575419
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.011720098053282125,
            "median": 0.0,
            "std": 0.038063229241560095,
            "ci95_low": 0.0025517456072812416,
            "ci95_high": 0.025391664560198462,
            "min": 0.0,
            "max": 0.22037721421665485
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.00896538287557394,
            "median": 0.0,
            "std": 0.02439625674838186,
            "ci95_low": 0.0024371812203059615,
            "ci95_high": 0.01681190597174491,
            "min": 0.0,
            "max": 0.11018860710832742
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.009907774857638689,
            "median": 0.0,
            "std": 0.028646068777947224,
            "ci95_low": 0.0023879755262940614,
            "ci95_high": 0.018782302623550483,
            "min": 0.0,
            "max": 0.14788428639091739
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
      }
    },
    "0.5": {
      "inheritance_probability": 0.5,
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 17.65,
            "median": 17.0,
            "std": 5.556752648804875,
            "ci95_low": 15.949375,
            "ci95_high": 19.350625,
            "min": 6.0,
            "max": 32.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.1363872779666433,
            "median": 0.13844875675034124,
            "std": 0.04286302643145421,
            "ci95_low": 0.12277143323879293,
            "ci95_high": 0.14971807225598557,
            "min": 0.04477611940298507,
            "max": 0.25196850393700787
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 1.3679646741905915,
            "median": 1.3688461752640788,
            "std": 0.5160361300140861,
            "ci95_low": 1.2172483606465905,
            "ci95_high": 1.5405986643756187,
            "min": 0.35803943373272873,
            "max": 2.6966202786108204
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.07632271792358566,
            "median": 0.07674859031698046,
            "std": 0.010024187765172877,
            "ci95_low": 0.073396464644089,
            "ci95_high": 0.07959688521669504,
            "min": 0.05753727234841248,
            "max": 0.10042935379147536
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.1684208341709029,
            "median": 0.1488701050635703,
            "std": 0.056346032060597066,
            "ci95_low": 0.1507224828738772,
            "ci95_high": 0.18680667972342335,
            "min": 0.073748546839766,
            "max": 0.28868358041766723
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 1.55,
            "median": 2.0,
            "std": 1.0712142642814275,
            "ci95_low": 1.25,
            "ci95_high": 1.875,
            "min": 0.0,
            "max": 4.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.09490737844650883,
            "median": 0.08712121212121213,
            "std": 0.07933019524813002,
            "ci95_low": 0.07087969927443129,
            "ci95_high": 0.1208650714896614,
            "min": 0.0,
            "max": 0.375
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 11.2,
            "median": 11.5,
            "std": 5.404627646748664,
            "ci95_low": 9.375,
            "ci95_high": 12.900625,
            "min": 2.0,
            "max": 24.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.0786231440156745,
            "median": 0.08198924731182795,
            "std": 0.03824514336425302,
            "ci95_low": 0.06758918954009428,
            "ci95_high": 0.09007174094867756,
            "min": 0.013986013986013986,
            "max": 0.17142857142857143
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.8518807619172968,
            "median": 0.8427589091499157,
            "std": 0.43380809287644734,
            "ci95_low": 0.7144246909166876,
            "ci95_high": 0.9910459744466555,
            "min": 0.13198871975501492,
            "max": 1.7894116013103338
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.07531465418813468,
            "median": 0.07503448873425467,
            "std": 0.012113792431194936,
            "ci95_low": 0.0714908096283471,
            "ci95_high": 0.07910201980253144,
            "min": 0.041397574058350664,
            "max": 0.09923773190376971
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.14155296613304053,
            "median": 0.14838805311541148,
            "std": 0.04640117145997644,
            "ci95_low": 0.12812113396040412,
            "ci95_high": 0.15664607974609407,
            "min": 0.048535494360222864,
            "max": 0.2828248616579013
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.8,
            "median": 0.0,
            "std": 1.0049875621120892,
            "ci95_low": 0.5,
            "ci95_high": 1.15,
            "min": 0.0,
            "max": 3.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.07113403033118001,
            "median": 0.0,
            "std": 0.08794884913461418,
            "ci95_low": 0.04560514673146547,
            "ci95_high": 0.09896720739621238,
            "min": 0.0,
            "max": 0.3333333333333333
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 6.725,
            "median": 7.0,
            "std": 4.652888887562221,
            "ci95_low": 5.34875,
            "ci95_high": 8.25,
            "min": 0.0,
            "max": 20.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.043500802126240065,
            "median": 0.042618059159315,
            "std": 0.030630446532246537,
            "ci95_low": 0.0342876253760845,
            "ci95_high": 0.053426241201959476,
            "min": 0.0,
            "max": 0.136986301369863
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.5095520034681074,
            "median": 0.4197630585976222,
            "std": 0.3941619391252663,
            "ci95_low": 0.38441984573068055,
            "ci95_high": 0.6360396917799497,
            "min": 0.0,
            "max": 1.6951028210810688
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.06808670395829898,
            "median": 0.07027294601763678,
            "std": 0.02063041416886722,
            "ci95_low": 0.06081591717577993,
            "ci95_high": 0.07408089075711381,
            "min": 0.0,
            "max": 0.10859269062969235
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.11730124258779025,
            "median": 0.1121417374592204,
            "std": 0.05711273144716772,
            "ci95_low": 0.10055470887433514,
            "ci95_high": 0.13368445936201923,
            "min": 0.0,
            "max": 0.2661257175246605
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.45,
            "median": 0.0,
            "std": 0.6304760106459246,
            "ci95_low": 0.25,
            "ci95_high": 0.65,
            "min": 0.0,
            "max": 2.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.057361111111111106,
            "median": 0.0,
            "std": 0.08796872395305017,
            "ci95_low": 0.032002976190476186,
            "ci95_high": 0.08482614087301586,
            "min": 0.0,
            "max": 0.3333333333333333
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 4.725,
            "median": 4.0,
            "std": 3.814364298280908,
            "ci95_low": 3.675,
            "ci95_high": 5.975,
            "min": 0.0,
            "max": 15.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.028299021233801635,
            "median": 0.024206523328945444,
            "std": 0.02354822176205328,
            "ci95_low": 0.021259309121611596,
            "ci95_high": 0.03638217239758346,
            "min": 0.0,
            "max": 0.0949367088607595
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.36397442499603894,
            "median": 0.29048199875002406,
            "std": 0.3116581370898128,
            "ci95_low": 0.2756965049362962,
            "ci95_high": 0.4660387685148152,
            "min": 0.0,
            "max": 1.08570985287016
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.062380664544406925,
            "median": 0.06952918016573134,
            "std": 0.033608121548445495,
            "ci95_low": 0.0520379531695638,
            "ci95_high": 0.07224261200915058,
            "min": 0.0,
            "max": 0.12023779784112759
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.10345310555110014,
            "median": 0.10401940262322529,
            "std": 0.07090078415379378,
            "ci95_low": 0.08188403258257237,
            "ci95_high": 0.12649929036476995,
            "min": 0.0,
            "max": 0.2876155338499252
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.375,
            "median": 0.0,
            "std": 0.6199798383818622,
            "ci95_low": 0.2,
            "ci95_high": 0.575,
            "min": 0.0,
            "max": 3.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.05641955266955266,
            "median": 0.0,
            "std": 0.09791889942577241,
            "ci95_low": 0.028552218614718614,
            "ci95_high": 0.09031367243867243,
            "min": 0.0,
            "max": 0.3333333333333333
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 2.425,
            "median": 0.5,
            "std": 3.247210341200582,
            "ci95_low": 1.5,
            "ci95_high": 3.5006249999999994,
            "min": 0.0,
            "max": 12.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.01234842505404575,
            "median": 0.0024875621890547263,
            "std": 0.01643884812534633,
            "ci95_low": 0.007497899082234015,
            "ci95_high": 0.017454010438931623,
            "min": 0.0,
            "max": 0.055299539170506916
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 0.1812601778430123,
            "median": 0.028845294154370205,
            "std": 0.26288208275948394,
            "ci95_low": 0.10518984737847921,
            "ci95_high": 0.2754968801244017,
            "min": 0.0,
            "max": 1.0762178775279296
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.03528427078110509,
            "median": 0.020177995864092857,
            "std": 0.03664347429001958,
            "ci95_low": 0.024214734576744633,
            "ci95_high": 0.04624012977863059,
            "min": 0.0,
            "max": 0.08968482312732746
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.05641045489750862,
            "median": 0.027511596724852316,
            "std": 0.06987625594989406,
            "ci95_low": 0.036460142662028114,
            "ci95_high": 0.07908242537972095,
            "min": 0.0,
            "max": 0.2883373276444923
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 0.15,
            "median": 0.0,
            "std": 0.3570714214271425,
            "ci95_low": 0.05,
            "ci95_high": 0.275,
            "min": 0.0,
            "max": 1.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.04444444444444444,
            "median": 0.0,
            "std": 0.1626601774661928,
            "ci95_low": 0.007621527777777777,
            "ci95_high": 0.10210069444444445,
            "min": 0.0,
            "max": 1.0
          }
        }
      }
    },
    "0.75": {
      "inheritance_probability": 0.75,
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 36.225,
            "median": 36.5,
            "std": 11.453138216227027,
            "ci95_low": 32.799375,
            "ci95_high": 39.775,
            "min": 17.0,
            "max": 66.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.27914142326798064,
            "median": 0.27860254499598763,
            "std": 0.080432015654984,
            "ci95_low": 0.2519481244836157,
            "ci95_high": 0.3034748173255082,
            "min": 0.14285714285714285,
            "max": 0.45517241379310347
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 3.113697722678615,
            "median": 3.0464987205498923,
            "std": 1.1002658778342937,
            "ci95_low": 2.7886215226468676,
            "ci95_high": 3.4757995338849934,
            "min": 1.534333574553499,
            "max": 6.241067374539821
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.08522823991625902,
            "median": 0.08536678644052485,
            "std": 0.007129013859598443,
            "ci95_low": 0.08309565436571524,
            "ci95_high": 0.08735728137370904,
            "min": 0.07062732142613806,
            "max": 0.09823577599870989
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.2145006224113984,
            "median": 0.2200002409182746,
            "std": 0.05324755785567789,
            "ci95_low": 0.1975996601231937,
            "ci95_high": 0.23055161044136185,
            "min": 0.13717612469057122,
            "max": 0.2886555601219441
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 2.975,
            "median": 2.5,
            "std": 2.2077986774160365,
            "ci95_low": 2.325,
            "ci95_high": 3.725,
            "min": 0.0,
            "max": 8.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.08260836435697567,
            "median": 0.07229965156794424,
            "std": 0.05955154924609107,
            "ci95_low": 0.06423444977103628,
            "ci95_high": 0.10155208577492185,
            "min": 0.0,
            "max": 0.25806451612903225
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 34.55,
            "median": 33.0,
            "std": 12.395462879618492,
            "ci95_low": 30.7,
            "ci95_high": 38.525,
            "min": 14.0,
            "max": 64.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.24496148107596297,
            "median": 0.2409914712153518,
            "std": 0.08363335998354056,
            "ci95_low": 0.21944640254824324,
            "ci95_high": 0.2716471193825245,
            "min": 0.09655172413793103,
            "max": 0.4266666666666667
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 3.0924566871380046,
            "median": 2.8495190074491776,
            "std": 1.215877970527633,
            "ci95_low": 2.7153363968419195,
            "ci95_high": 3.510589210536561,
            "min": 1.1284335196692428,
            "max": 6.367003009552981
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.08877595439359993,
            "median": 0.08890237585445093,
            "std": 0.008135855716751218,
            "ci95_low": 0.08633831051104031,
            "ci95_high": 0.09120950935388497,
            "min": 0.06928106143501438,
            "max": 0.10160721232624541
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.22438680439624994,
            "median": 0.2210906697604042,
            "std": 0.050858376279834215,
            "ci95_low": 0.2100089003877723,
            "ci95_high": 0.24076264893099172,
            "min": 0.13943661806680574,
            "max": 0.28869800176408794
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 2.75,
            "median": 2.0,
            "std": 1.9072231122760652,
            "ci95_low": 2.15,
            "ci95_high": 3.3256249999999996,
            "min": 0.0,
            "max": 7.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.07854877236655763,
            "median": 0.07692307692307693,
            "std": 0.05044869357697783,
            "ci95_low": 0.06210201972804587,
            "ci95_high": 0.09450888197373969,
            "min": 0.0,
            "max": 0.23529411764705882
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 32.475,
            "median": 30.0,
            "std": 12.22903818785435,
            "ci95_low": 28.82375,
            "ci95_high": 36.175,
            "min": 15.0,
            "max": 55.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.21103165148552616,
            "median": 0.19731543624161074,
            "std": 0.07996489564978851,
            "ci95_low": 0.18650320563772513,
            "ci95_high": 0.23658768364709729,
            "min": 0.09803921568627451,
            "max": 0.3691275167785235
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 2.940510359028875,
            "median": 2.8742118809468433,
            "std": 1.2010690333549316,
            "ci95_low": 2.5558834378563398,
            "ci95_high": 3.3151259836072664,
            "min": 1.0826123686300413,
            "max": 5.317146828357509
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0895286143773766,
            "median": 0.08961582386880117,
            "std": 0.007148987428220254,
            "ci95_low": 0.08736865191704261,
            "ci95_high": 0.09157284658866358,
            "min": 0.07217415790866942,
            "max": 0.10528587008052419
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.22217688570654753,
            "median": 0.22030363039657375,
            "std": 0.05557554076208105,
            "ci95_low": 0.2042229284988478,
            "ci95_high": 0.23946898268240455,
            "min": 0.1306344243098726,
            "max": 0.2886268995051424
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 2.95,
            "median": 3.0,
            "std": 2.073041244162788,
            "ci95_low": 2.35,
            "ci95_high": 3.6,
            "min": 0.0,
            "max": 8.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.08733264961771428,
            "median": 0.09232954545454546,
            "std": 0.053125531017909726,
            "ci95_low": 0.07019590503446702,
            "ci95_high": 0.10400305469905188,
            "min": 0.0,
            "max": 0.20689655172413793
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 31.85,
            "median": 31.0,
            "std": 13.866416263764766,
            "ci95_low": 27.548125000000002,
            "ci95_high": 35.975625,
            "min": 11.0,
            "max": 65.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.19077462017587093,
            "median": 0.18832320162107397,
            "std": 0.08249323538130864,
            "ci95_low": 0.16638363812160528,
            "ci95_high": 0.21490479999212173,
            "min": 0.06626506024096386,
            "max": 0.38011695906432746
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 2.8545491874308633,
            "median": 2.8067567624342082,
            "std": 1.3247285509080526,
            "ci95_low": 2.462331050687717,
            "ci95_high": 3.279368907744568,
            "min": 0.9410170277338604,
            "max": 6.529717705821057
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.08930523238855723,
            "median": 0.08879091617328946,
            "std": 0.009980941494448716,
            "ci95_low": 0.08609619384973131,
            "ci95_high": 0.09254627796369913,
            "min": 0.0724989050385788,
            "max": 0.11569758458779482
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.22604317960573644,
            "median": 0.22076837162177024,
            "std": 0.05545521357814121,
            "ci95_low": 0.20963511719669528,
            "ci95_high": 0.2428096478091756,
            "min": 0.14208796717894234,
            "max": 0.2886633161866029
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 2.675,
            "median": 2.0,
            "std": 2.054111730164647,
            "ci95_low": 2.1,
            "ci95_high": 3.375,
            "min": 0.0,
            "max": 9.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.08080518700823683,
            "median": 0.08571428571428572,
            "std": 0.045280950884882806,
            "ci95_low": 0.06686106735807962,
            "ci95_high": 0.09428224584786608,
            "min": 0.0,
            "max": 0.17647058823529413
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 29.475,
            "median": 28.0,
            "std": 15.631678572693337,
            "ci95_low": 24.849375000000002,
            "ci95_high": 34.65,
            "min": 10.0,
            "max": 79.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.15201111173289653,
            "median": 0.1425828970331588,
            "std": 0.08031489241705422,
            "ci95_low": 0.12825325441236113,
            "ci95_high": 0.17610590123092731,
            "min": 0.05,
            "max": 0.4030612244897959
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 2.6731572844674267,
            "median": 2.4087885694321716,
            "std": 1.485329127857259,
            "ci95_low": 2.221203743135006,
            "ci95_high": 3.1979384538153885,
            "min": 0.9311743676390493,
            "max": 7.405116255323207
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.0902801629572709,
            "median": 0.09028788592775505,
            "std": 0.007539202165723818,
            "ci95_low": 0.08779711026595083,
            "ci95_high": 0.09260248155636727,
            "min": 0.07256417782999193,
            "max": 0.10442591949772598
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.21648419504510658,
            "median": 0.21901557447245432,
            "std": 0.060467456016250455,
            "ci95_low": 0.1974101646625148,
            "ci95_high": 0.2350947657936031,
            "min": 0.145727520769244,
            "max": 0.28863045424053224
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 2.9,
            "median": 2.0,
            "std": 2.6627053911388696,
            "ci95_low": 2.125,
            "ci95_high": 3.8,
            "min": 0.0,
            "max": 10.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.08864809518783923,
            "median": 0.08333333333333333,
            "std": 0.06564689401704099,
            "ci95_low": 0.06981997613758936,
            "ci95_high": 0.10882666341998622,
            "min": 0.0,
            "max": 0.3076923076923077
          }
        }
      }
    },
    "1.0": {
      "inheritance_probability": 1.0,
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 57.325,
            "median": 57.0,
            "std": 15.561792152576773,
            "ci95_low": 52.624375,
            "ci95_high": 62.12625,
            "min": 28.0,
            "max": 89.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.44598652032178093,
            "median": 0.4492673992673993,
            "std": 0.12764918967819333,
            "ci95_low": 0.406974675881975,
            "ci95_high": 0.4836896916961418,
            "min": 0.2204724409448819,
            "max": 0.7007874015748031
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 5.845366413650915,
            "median": 5.801975611023259,
            "std": 1.6468622925654057,
            "ci95_low": 5.303091263289409,
            "ci95_high": 6.359389115204983,
            "min": 2.5689289961544683,
            "max": 8.750790400752413
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.10162893578904417,
            "median": 0.10150927288807965,
            "std": 0.005147808805654223,
            "ci95_low": 0.10002422598769277,
            "ci95_high": 0.10314477389882593,
            "min": 0.09002489210233366,
            "max": 0.11225468629216367
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.2760299808595888,
            "median": 0.28491276423358936,
            "std": 0.03081356916583894,
            "ci95_low": 0.2657602548731558,
            "ci95_high": 0.28369427444915213,
            "min": 0.14223276928248796,
            "max": 0.2886981120255417
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 5.2,
            "median": 5.5,
            "std": 2.776688675382964,
            "ci95_low": 4.324375,
            "ci95_high": 6.026249999999999,
            "min": 0.0,
            "max": 12.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.09035649747054797,
            "median": 0.09307359307359307,
            "std": 0.04158332013657041,
            "ci95_low": 0.07754880182142898,
            "ci95_high": 0.10339705622610755,
            "min": 0.0,
            "max": 0.1951219512195122
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 67.7,
            "median": 69.0,
            "std": 18.22800043888523,
            "ci95_low": 61.899375,
            "ci95_high": 73.60125,
            "min": 27.0,
            "max": 107.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.47903468340490923,
            "median": 0.4897959183673469,
            "std": 0.13503870815864832,
            "ci95_low": 0.4365060740476739,
            "ci95_high": 0.52049906240098,
            "min": 0.2076923076923077,
            "max": 0.7588652482269503
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 7.30266686955365,
            "median": 7.246713828156542,
            "std": 2.110815012035873,
            "ci95_low": 6.707704952817179,
            "ci95_high": 7.956899028767533,
            "min": 2.76128585166871,
            "max": 11.872530799639204
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.10723504044974967,
            "median": 0.10756698589306116,
            "std": 0.005489786350466453,
            "ci95_low": 0.10551289883111675,
            "ci95_high": 0.1089722227318716,
            "min": 0.09691961317907821,
            "max": 0.12055993903590607
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.2806266730878825,
            "median": 0.2846265997100431,
            "std": 0.011791721231819033,
            "ci95_low": 0.2765949410100353,
            "ci95_high": 0.28378298088652626,
            "min": 0.23075786606953008,
            "max": 0.2886973478332756
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 6.95,
            "median": 7.0,
            "std": 3.049180217697865,
            "ci95_low": 6.05,
            "ci95_high": 7.850624999999999,
            "min": 1.0,
            "max": 13.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.10423807714201394,
            "median": 0.1094820205479452,
            "std": 0.0422639339556125,
            "ci95_low": 0.09170079081136731,
            "ci95_high": 0.11800169111575122,
            "min": 0.034482758620689655,
            "max": 0.19402985074626866
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 76.35,
            "median": 79.5,
            "std": 21.499476737818526,
            "ci95_low": 69.795625,
            "ci95_high": 82.97749999999999,
            "min": 30.0,
            "max": 121.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.5059962356164472,
            "median": 0.529037092544024,
            "std": 0.14494074672181118,
            "ci95_low": 0.4616462365589563,
            "ci95_high": 0.5532227687219278,
            "min": 0.19607843137254902,
            "max": 0.8013245033112583
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 8.437722467651025,
            "median": 8.451203265116234,
            "std": 2.483292192880038,
            "ci95_low": 7.645192674358018,
            "ci95_high": 9.177424841746536,
            "min": 3.2951211031072223,
            "max": 13.911254829300054
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.11030061061256588,
            "median": 0.11080230002920674,
            "std": 0.005065542444554496,
            "ci95_low": 0.10872231187288572,
            "ci95_high": 0.11182449550876614,
            "min": 0.09642231535628693,
            "max": 0.11935066671961879
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.27419615551438586,
            "median": 0.28576176230389805,
            "std": 0.026067005063831295,
            "ci95_low": 0.26565070461761436,
            "ci95_high": 0.28121849147590117,
            "min": 0.1487051905002863,
            "max": 0.28869187670501445
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 8.55,
            "median": 8.0,
            "std": 3.8206674809514634,
            "ci95_low": 7.45,
            "ci95_high": 9.675625,
            "min": 4.0,
            "max": 21.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.11461484038827179,
            "median": 0.1026500638569604,
            "std": 0.04286463316337238,
            "ci95_low": 0.10166729384966104,
            "ci95_high": 0.12916439696559398,
            "min": 0.05128205128205128,
            "max": 0.23333333333333334
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 86.9,
            "median": 89.5,
            "std": 24.38011484796575,
            "ci95_low": 79.421875,
            "ci95_high": 94.125,
            "min": 30.0,
            "max": 130.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.5303893526617897,
            "median": 0.5603673031209263,
            "std": 0.15339547526436992,
            "ci95_low": 0.4864595808831458,
            "ci95_high": 0.5806751859975852,
            "min": 0.18867924528301888,
            "max": 0.8111888111888111
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 9.699991217051641,
            "median": 10.103188508357524,
            "std": 2.8830304097854187,
            "ci95_low": 8.824877141677723,
            "ci95_high": 10.642137174254954,
            "min": 3.2690096847692454,
            "max": 14.77149993541865
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.11099371374224813,
            "median": 0.11132191147297621,
            "std": 0.004959805757102044,
            "ci95_low": 0.10942395733909532,
            "ci95_high": 0.11247208101616812,
            "min": 0.09779838177824739,
            "max": 0.12260714614088368
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.2787756669837694,
            "median": 0.2846836065463423,
            "std": 0.013733607902714023,
            "ci95_low": 0.27411736447575424,
            "ci95_high": 0.2825481974228547,
            "min": 0.22660881737645866,
            "max": 0.2886639175763512
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 10.25,
            "median": 11.0,
            "std": 4.542851527399943,
            "ci95_low": 8.95,
            "ci95_high": 11.675625,
            "min": 0.0,
            "max": 24.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.11472458943599254,
            "median": 0.11180555555555555,
            "std": 0.04067635203352611,
            "ci95_low": 0.10169746748056935,
            "ci95_high": 0.1277076371181671,
            "min": 0.0,
            "max": 0.2
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 40,
            "mean": 108.35,
            "median": 108.0,
            "std": 30.564317430624886,
            "ci95_low": 98.64500000000001,
            "ci95_high": 117.68062499999999,
            "min": 39.0,
            "max": 175.0
          },
          "exposed_frontier_fraction": {
            "n": 40,
            "mean": 0.5650041848280815,
            "median": 0.5827284571003164,
            "std": 0.16315006056842665,
            "ci95_low": 0.5154106259547822,
            "ci95_high": 0.6151428698355699,
            "min": 0.21910112359550563,
            "max": 0.9067357512953368
          },
          "sum_delta_p": {
            "n": 40,
            "mean": 12.26427554963501,
            "median": 12.369319395101355,
            "std": 3.561986641196206,
            "ci95_low": 11.183584605067454,
            "ci95_high": 13.385681925964095,
            "min": 3.995830015554368,
            "max": 19.638716390448266
          },
          "mean_delta_p_exposed": {
            "n": 40,
            "mean": 0.11278531293929024,
            "median": 0.11417789009773616,
            "std": 0.004527147284626174,
            "ci95_low": 0.11131933854026158,
            "ci95_high": 0.1140894344608658,
            "min": 0.09895561771910762,
            "max": 0.1185309319791715
          },
          "max_delta_p_exposed": {
            "n": 40,
            "mean": 0.27883085121244233,
            "median": 0.28545082585492904,
            "std": 0.014393370520062045,
            "ci95_low": 0.274244553246407,
            "ci95_high": 0.2828983433627382,
            "min": 0.23232224373878685,
            "max": 0.28867709066433617
          },
          "realized_causal_flips": {
            "n": 40,
            "mean": 11.825,
            "median": 12.0,
            "std": 4.206468233566016,
            "ci95_low": 10.425,
            "ci95_high": 13.05,
            "min": 2.0,
            "max": 19.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 40,
            "mean": 0.10889886285617316,
            "median": 0.10940809968847352,
            "std": 0.028558421376041806,
            "ci95_low": 0.10015495836677189,
            "ci95_high": 0.11766261877883191,
            "min": 0.02247191011235955,
            "max": 0.16964285714285715
          }
        }
      }
    }
  },
  "status": "MEASURED",
  "causal_definition": "For an exposed frontier cell under common random numbers, a realized causal flip occurs when p_erased <= u < p_retained.",
  "bounded_statement": "V4 separates frontier availability, probability leverage, and realized attachment flips caused by retained material state."
}
```


# Stage 3 — Secondary Late Ablation Across Propagation Regimes

```json
{
  "late_ablation_step": 14,
  "followup_steps": 4,
  "results": {
    "0.0": {
      "inheritance_probability": 0.0,
      "frontier_contact_at_ablation": {
        "n": 40,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 40,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1500,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      }
    },
    "0.25": {
      "inheritance_probability": 0.25,
      "frontier_contact_at_ablation": {
        "n": 40,
        "mean": 0.15,
        "median": 0.0,
        "std": 0.653834841531101,
        "ci95_low": 0.0,
        "ci95_high": 0.425,
        "min": 0.0,
        "max": 4.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 40,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1500,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      }
    },
    "0.5": {
      "inheritance_probability": 0.5,
      "frontier_contact_at_ablation": {
        "n": 40,
        "mean": 6.9,
        "median": 6.0,
        "std": 5.756735185849702,
        "ci95_low": 5.1743749999999995,
        "ci95_high": 8.95,
        "min": 0.0,
        "max": 26.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 40,
        "mean": 0.0006848588957245686,
        "median": 0.0,
        "std": 0.0012203533674365126,
        "ci95_low": 0.00037476194092343393,
        "ci95_high": 0.0011039249819210378,
        "min": 0.0,
        "max": 0.005568814638027049
      },
      "paired_ridge_test": {
        "statistic": 0.3202509662008302,
        "p_value": 0.020652898067954697,
        "permutations": 1500,
        "null_mean": 0.15860074654909811,
        "null_q95": 0.27341430038862646,
        "null_q99": 0.3663588032232651
      }
    },
    "0.75": {
      "inheritance_probability": 0.75,
      "frontier_contact_at_ablation": {
        "n": 40,
        "mean": 31.65,
        "median": 28.0,
        "std": 14.208360215028334,
        "ci95_low": 27.2,
        "ci95_high": 36.000625,
        "min": 3.0,
        "max": 68.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 40,
        "mean": 0.007967821029106708,
        "median": 0.007222811927048153,
        "std": 0.005345088005746953,
        "ci95_low": 0.006345032900919417,
        "ci95_high": 0.009730301767464186,
        "min": 0.0,
        "max": 0.022708158116063918
      },
      "paired_ridge_test": {
        "statistic": 1.6354356440969227,
        "p_value": 0.0006662225183211193,
        "permutations": 1500,
        "null_mean": 0.24933235218964045,
        "null_q95": 0.4580955436401872,
        "null_q99": 0.59874428902509
      }
    },
    "1.0": {
      "inheritance_probability": 1.0,
      "frontier_contact_at_ablation": {
        "n": 40,
        "mean": 93.975,
        "median": 94.5,
        "std": 22.94720843588605,
        "ci95_low": 86.675,
        "ci95_high": 101.3025,
        "min": 51.0,
        "max": 138.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 40,
        "mean": 0.03042161697710045,
        "median": 0.028996859571838195,
        "std": 0.00997013339477966,
        "ci95_low": 0.02750853917647301,
        "ci95_high": 0.03382269100993558,
        "min": 0.015006821282401092,
        "max": 0.056024558710667687
      },
      "paired_ridge_test": {
        "statistic": 9.299875483312654,
        "p_value": 0.0006662225183211193,
        "permutations": 1500,
        "null_mean": 0.22368841306564954,
        "null_q95": 0.4052430627107341,
        "null_q99": 0.5740502177908746
      }
    }
  },
  "status": "MEASURED",
  "interpretation": "Late whole-crystal ablation is secondary corroboration. V4 does not select an inheritance probability by the smallest p-value."
}
```


# Stage 4 — Bounded Chapter 18 V4 Mechanism Map

```json
{
  "experiment_role": "EXPLORATORY MECHANISM CHARACTERIZATION",
  "chapter": 18,
  "question": "Why can propagated material remain present near the frontier yet fail to produce a strong late whole-crystal effect?",
  "inheritance_sweep_is_descriptive_not_selection": true,
  "mechanistic_classification_at_late_step": {
    "0.0": {
      "inheritance_probability": 0.0,
      "late_step": 14,
      "mean_exposed_frontier_count": 0.0,
      "mean_sum_delta_p": 0.0,
      "mean_realized_causal_flips": 0.0,
      "mechanistic_classification": "NO_ACCESS"
    },
    "0.25": {
      "inheritance_probability": 0.25,
      "late_step": 14,
      "mean_exposed_frontier_count": 0.175,
      "mean_sum_delta_p": 0.011720098053282125,
      "mean_realized_causal_flips": 0.0,
      "mechanistic_classification": "ACCESS_WITH_PROBABILITY_LEVERAGE_BUT_NO_MEAN_REALIZED_FLIPS"
    },
    "0.5": {
      "inheritance_probability": 0.5,
      "late_step": 14,
      "mean_exposed_frontier_count": 4.725,
      "mean_sum_delta_p": 0.36397442499603894,
      "mean_realized_causal_flips": 0.375,
      "mechanistic_classification": "ACCESS_WITH_REALIZED_FLIPS"
    },
    "0.75": {
      "inheritance_probability": 0.75,
      "late_step": 14,
      "mean_exposed_frontier_count": 31.85,
      "mean_sum_delta_p": 2.8545491874308633,
      "mean_realized_causal_flips": 2.675,
      "mechanistic_classification": "ACCESS_WITH_REALIZED_FLIPS"
    },
    "1.0": {
      "inheritance_probability": 1.0,
      "late_step": 14,
      "mean_exposed_frontier_count": 86.9,
      "mean_sum_delta_p": 9.699991217051641,
      "mean_realized_causal_flips": 10.25,
      "mechanistic_classification": "ACCESS_WITH_REALIZED_FLIPS"
    }
  },
  "any_regime_with_realized_late_causal_flips": true,
  "final_status": "MEASURED",
  "bounded_claim": "V4 characterizes three separable quantities: whether modified material reaches the frontier, how strongly it changes attachment probabilities there, and whether those probability shifts produce realized CRN attachment flips.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "phase transition",
    "critical threshold",
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
  "next_question": "Use the mechanism map to decide whether the next intervention should target propagation availability, local causal gain, or surface-biased state transmission. Do not choose solely from a significance result."
}
```
