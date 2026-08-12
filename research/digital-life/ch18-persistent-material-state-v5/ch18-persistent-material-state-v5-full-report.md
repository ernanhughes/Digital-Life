# Chapter 18 — Can Experience Change the Material? (V5 Surface-Biased Transmission)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v5",
  "schema_version": 5,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY MECHANISM COMPARISON",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 64,
    "warmup_steps": 14,
    "experience_pulse_step": 3,
    "message_gain": 0.65,
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "transmission_fraction": 0.5,
    "transmission_policies": [
      "none",
      "uniform_budget",
      "surface_biased_budget"
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
    "permutations": 2000,
    "bootstrap_reps": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260818,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "v4_supported_mechanism_map": "Late causal work increased with successful propagation. Local causal gain was sufficient when modified material remained available at the active frontier.",
  "v5_new_mechanism": "Matched-budget propagation allocation: uniform placement versus preferential placement on newly attached cells with greater outward surface exposure.",
  "scientific_boundary": "V5 tests placement of propagated local state at a fixed nominal copying budget. It does not claim memory, learning, adaptation, attention, homeostasis, or an active biological boundary.",
  "started_at_unix": 1786539365.7783284,
  "finished_at_unix": 1786539388.7513041,
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "stage_4_status": "MEASURED",
  "final_status": "SUPPORTED",
  "next_question": "If surface-biased placement is supported, test whether the state can be updated or displaced by a later experience while the copying budget remains fixed. If not, return to the local propagation rule rather than increasing causal gain."
}
```

# Stage 0 — V5 Surface-Placement Audit

```json
{
  "role": "V5 SURFACE-PLACEMENT AUDIT",
  "canonical_model_modified": false,
  "transmission_fraction": 0.5,
  "transmission_policies": [
    "none",
    "uniform_budget",
    "surface_biased_budget"
  ],
  "exact_reproducibility_by_policy": {
    "none": true,
    "uniform_budget": true,
    "surface_biased_budget": true
  },
  "all_policies_exactly_reproducible": true,
  "synthetic_equal_budget_check": {
    "uniform": {
      "eligible_count": 4,
      "budget": 2,
      "selected_count": 2,
      "mean_selected_surface_exposure": 3.5,
      "mean_eligible_surface_exposure": 3.5
    },
    "surface_biased": {
      "eligible_count": 4,
      "budget": 2,
      "selected_count": 2,
      "mean_selected_surface_exposure": 4.0,
      "mean_eligible_surface_exposure": 3.5
    },
    "equal_selected_count": true
  },
  "scientific_role": "Compare transmission placement at a matched per-step copying budget. The experiment asks whether placing state on more exposed new material improves long-term causal accessibility."
}
```


# Stage 1 — Does Surface Bias Change Placement Rather Than Copy Count?

```json
{
  "groups": 48,
  "transmission_fraction": 0.5,
  "policies": [
    "uniform_budget",
    "surface_biased_budget"
  ],
  "summary": {
    "uniform_budget": {
      "eligible_count": {
        "n": 864,
        "mean": 6.33912037037037,
        "median": 4.0,
        "std": 6.694701274304751,
        "ci95_low": 5.872627314814815,
        "ci95_high": 6.777864583333333,
        "min": 0.0,
        "max": 34.0
      },
      "transmitted_count": {
        "n": 864,
        "mean": 3.1550925925925926,
        "median": 2.0,
        "std": 3.3814611665752197,
        "ci95_low": 2.9420717592592593,
        "ci95_high": 3.380787037037037,
        "min": 0.0,
        "max": 17.0
      },
      "mean_eligible_surface_exposure": {
        "n": 864,
        "mean": 1.5181212760215947,
        "median": 1.8181818181818181,
        "std": 1.0067897074779057,
        "ci95_low": 1.449299110716447,
        "ci95_high": 1.5839826914203663,
        "min": 0.0,
        "max": 5.0
      },
      "mean_transmitted_surface_exposure": {
        "n": 864,
        "mean": 1.3611156466574155,
        "median": 1.5,
        "std": 1.093258397109103,
        "ci95_low": 1.292329967590129,
        "ci95_high": 1.4335521817459878,
        "min": 0.0,
        "max": 4.0
      }
    },
    "surface_biased_budget": {
      "eligible_count": {
        "n": 864,
        "mean": 27.247685185185187,
        "median": 25.0,
        "std": 10.863153156127563,
        "ci95_low": 26.533362268518516,
        "ci95_high": 28.038194444444443,
        "min": 8.0,
        "max": 72.0
      },
      "transmitted_count": {
        "n": 864,
        "mean": 13.625,
        "median": 12.0,
        "std": 5.436981137440968,
        "ci95_low": 13.256799768518519,
        "ci95_high": 14.018605324074075,
        "min": 4.0,
        "max": 36.0
      },
      "mean_eligible_surface_exposure": {
        "n": 864,
        "mean": 2.4277356472681673,
        "median": 2.4285714285714284,
        "std": 0.3008807870799873,
        "ci95_low": 2.408056114503084,
        "ci95_high": 2.4469524858020373,
        "min": 1.4666666666666666,
        "max": 3.1578947368421053
      },
      "mean_transmitted_surface_exposure": {
        "n": 864,
        "mean": 3.510924528095521,
        "median": 3.5384615384615383,
        "std": 0.31826103886358814,
        "ci95_low": 3.4895391256854476,
        "ci95_high": 3.532058591447023,
        "min": 2.25,
        "max": 4.3
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "V5 verifies that surface-biased allocation changes where propagated state is placed while holding the nominal per-step transmission budget fixed."
}
```


# Stage 2 — Does Surface-Biased Transmission Keep State on the Active Surface?

```json
{
  "groups_per_policy": 48,
  "transmission_fraction": 0.5,
  "policies": [
    "none",
    "uniform_budget",
    "surface_biased_budget"
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
    "none": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.7078125,
            "ci95_high": 21.6046875,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 11.958333333333334,
            "median": 12.5,
            "std": 4.046388993768257,
            "ci95_low": 10.854166666666666,
            "ci95_high": 13.1875,
            "min": 4.0,
            "max": 19.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 17.270833333333332,
            "median": 17.5,
            "std": 5.9851886051225565,
            "ci95_low": 15.603645833333333,
            "ci95_high": 19.125,
            "min": 5.0,
            "max": 29.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.1579942573783961,
            "median": 0.15743155149934812,
            "std": 0.05535856442893996,
            "ci95_low": 0.14247890392912113,
            "ci95_high": 0.1735339044383857,
            "min": 0.045454545454545456,
            "max": 0.27450980392156865
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.916145833333335,
            "ci95_high": 21.688020833333333,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 5.958333333333333,
            "median": 6.0,
            "std": 2.6611270586392943,
            "ci95_low": 5.25,
            "ci95_high": 6.729166666666667,
            "min": 2.0,
            "max": 12.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 7.479166666666667,
            "median": 7.0,
            "std": 3.889031495401165,
            "ci95_low": 6.354166666666667,
            "ci95_high": 8.645833333333334,
            "min": 2.0,
            "max": 18.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.06429434693793058,
            "median": 0.05785123966942149,
            "std": 0.03475174930121549,
            "ci95_low": 0.054838903761196836,
            "ci95_high": 0.07469951181603625,
            "min": 0.017094017094017096,
            "max": 0.17647058823529413
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.5,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 2.4166666666666665,
            "median": 2.0,
            "std": 1.8577914008006629,
            "ci95_low": 1.9369791666666667,
            "ci95_high": 2.9375,
            "min": 0.0,
            "max": 9.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 2.6666666666666665,
            "median": 2.0,
            "std": 2.084999333866134,
            "ci95_low": 2.125,
            "ci95_high": 3.25,
            "min": 0.0,
            "max": 9.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.021446431521033548,
            "median": 0.01652892561983471,
            "std": 0.017230173318250153,
            "ci95_low": 0.017015718832941326,
            "ci95_high": 0.02653173721330402,
            "min": 0.0,
            "max": 0.07964601769911504
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.74791666666667,
            "ci95_high": 21.6875,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.7916666666666666,
            "median": 1.0,
            "std": 0.840593375076334,
            "ci95_low": 0.5416666666666666,
            "ci95_high": 1.0416666666666667,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.7916666666666666,
            "median": 1.0,
            "std": 0.8650224788344456,
            "ci95_low": 0.5625,
            "ci95_high": 1.0416666666666667,
            "min": 0.0,
            "max": 4.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.006031626323591929,
            "median": 0.006872933396315541,
            "std": 0.006806823737821128,
            "ci95_low": 0.004218595925094516,
            "ci95_high": 0.007811997313790884,
            "min": 0.0,
            "max": 0.03225806451612903
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.708333333333332,
            "ci95_high": 21.708333333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.041666666666666664,
            "median": 0.0,
            "std": 0.19982631347136337,
            "ci95_low": 0.0,
            "ci95_high": 0.10416666666666667,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.041666666666666664,
            "median": 0.0,
            "std": 0.19982631347136337,
            "ci95_low": 0.0,
            "ci95_high": 0.10416666666666667,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0002997988446461729,
            "median": 0.0,
            "std": 0.0014405671314657376,
            "ci95_low": 0.0,
            "ci95_high": 0.0007586307681727529,
            "min": 0.0,
            "max": 0.007633587786259542
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.7703125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
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
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
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
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.875,
            "ci95_high": 21.583333333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
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
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8953125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
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
    "uniform_budget": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 30.0,
            "median": 28.0,
            "std": 7.213991035943049,
            "ci95_low": 27.8328125,
            "ci95_high": 32.021875,
            "min": 15.0,
            "max": 48.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.208333333333332,
            "median": 19.5,
            "std": 5.431230421266335,
            "ci95_low": 18.75,
            "ci95_high": 21.7921875,
            "min": 8.0,
            "max": 33.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 31.020833333333332,
            "median": 32.0,
            "std": 8.120164159191747,
            "ci95_low": 28.666145833333335,
            "ci95_high": 33.25,
            "min": 10.0,
            "max": 48.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.2833130981545109,
            "median": 0.2832274758880263,
            "std": 0.06955614627943915,
            "ci95_low": 0.26313965937901457,
            "ci95_high": 0.30209509373744864,
            "min": 0.09090909090909091,
            "max": 0.42857142857142855
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 38.020833333333336,
            "median": 38.0,
            "std": 8.837631619324766,
            "ci95_low": 35.833333333333336,
            "ci95_high": 40.729166666666664,
            "min": 17.0,
            "max": 60.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 18.770833333333332,
            "median": 18.5,
            "std": 5.058983689657659,
            "ci95_low": 17.291666666666668,
            "ci95_high": 20.208333333333332,
            "min": 5.0,
            "max": 30.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 26.666666666666668,
            "median": 26.5,
            "std": 7.638535345353992,
            "ci95_low": 24.541145833333335,
            "ci95_high": 28.791666666666668,
            "min": 7.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.2293806858974594,
            "median": 0.22504347826086957,
            "std": 0.06565839298927652,
            "ci95_low": 0.21186850231914714,
            "ci95_high": 0.24739903427227108,
            "min": 0.0603448275862069,
            "max": 0.37254901960784315
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 45.375,
            "median": 45.0,
            "std": 10.75411742853251,
            "ci95_low": 42.395833333333336,
            "ci95_high": 48.522395833333334,
            "min": 18.0,
            "max": 72.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 16.958333333333332,
            "median": 16.5,
            "std": 5.2637056549756105,
            "ci95_low": 15.436979166666667,
            "ci95_high": 18.291666666666668,
            "min": 5.0,
            "max": 28.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 22.354166666666668,
            "median": 22.0,
            "std": 6.743792155670939,
            "ci95_low": 20.5203125,
            "ci95_high": 24.104166666666668,
            "min": 7.0,
            "max": 38.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.18113190545644176,
            "median": 0.18344751651578176,
            "std": 0.05485474631813467,
            "ci95_low": 0.1664459802765414,
            "ci95_high": 0.19740255002232002,
            "min": 0.05982905982905983,
            "max": 0.3157894736842105
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 51.729166666666664,
            "median": 52.0,
            "std": 12.272495642922655,
            "ci95_low": 48.2078125,
            "ci95_high": 55.39791666666667,
            "min": 20.0,
            "max": 82.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 13.729166666666666,
            "median": 13.0,
            "std": 4.689258929250501,
            "ci95_low": 12.332812500000001,
            "ci95_high": 15.083333333333334,
            "min": 4.0,
            "max": 24.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 17.75,
            "median": 17.5,
            "std": 6.219927652312364,
            "ci95_low": 16.061979166666667,
            "ci95_high": 19.605208333333334,
            "min": 6.0,
            "max": 32.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.13682277746862959,
            "median": 0.13427827306420914,
            "std": 0.04784008685967763,
            "ci95_low": 0.12327019251609986,
            "ci95_high": 0.1507037528535577,
            "min": 0.05084745762711865,
            "max": 0.2549019607843137
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 60.770833333333336,
            "median": 60.5,
            "std": 14.57057477608744,
            "ci95_low": 56.56197916666667,
            "ci95_high": 64.83489583333332,
            "min": 24.0,
            "max": 93.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 8.958333333333334,
            "median": 8.5,
            "std": 3.5937349033499335,
            "ci95_low": 7.9375,
            "ci95_high": 9.896354166666667,
            "min": 2.0,
            "max": 16.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 11.895833333333334,
            "median": 12.0,
            "std": 4.9801254307050895,
            "ci95_low": 10.520312500000001,
            "ci95_high": 13.292187499999999,
            "min": 3.0,
            "max": 22.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.08400472717788872,
            "median": 0.0870843865448182,
            "std": 0.035796464801178075,
            "ci95_low": 0.07438739500088422,
            "ci95_high": 0.09379723581165893,
            "min": 0.022900763358778626,
            "max": 0.16071428571428573
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 66.75,
            "median": 66.5,
            "std": 16.205066080293122,
            "ci95_low": 62.104166666666664,
            "ci95_high": 71.5421875,
            "min": 28.0,
            "max": 104.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 5.75,
            "median": 6.0,
            "std": 3.178705187126775,
            "ci95_low": 4.8125,
            "ci95_high": 6.625,
            "min": 0.0,
            "max": 13.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 7.416666666666667,
            "median": 7.5,
            "std": 4.127314165679931,
            "ci95_low": 6.3125,
            "ci95_high": 8.604166666666666,
            "min": 0.0,
            "max": 15.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.04727299777030209,
            "median": 0.04748150757308912,
            "std": 0.02622978285388272,
            "ci95_low": 0.03981014249850631,
            "ci95_high": 0.05483002661514331,
            "min": 0.0,
            "max": 0.09655172413793103
          }
        },
        "14": {
          "modified_count": {
            "n": 48,
            "mean": 70.52083333333333,
            "median": 71.0,
            "std": 17.53091267748361,
            "ci95_low": 65.70729166666666,
            "ci95_high": 75.54166666666667,
            "min": 32.0,
            "max": 110.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 3.625,
            "median": 3.0,
            "std": 2.32401412789739,
            "ci95_low": 2.9791666666666665,
            "ci95_high": 4.291666666666667,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 5.208333333333333,
            "median": 5.0,
            "std": 3.570471101814001,
            "ci95_low": 4.166145833333333,
            "ci95_high": 6.25,
            "min": 0.0,
            "max": 12.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.030297775460493292,
            "median": 0.028249489274770175,
            "std": 0.020590390237229507,
            "ci95_low": 0.02425659213283865,
            "ci95_high": 0.03608227120041982,
            "min": 0.0,
            "max": 0.07453416149068323
          }
        },
        "18": {
          "modified_count": {
            "n": 48,
            "mean": 75.20833333333333,
            "median": 74.5,
            "std": 19.86512682790847,
            "ci95_low": 69.6875,
            "ci95_high": 80.6875,
            "min": 34.0,
            "max": 118.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 1.75,
            "median": 1.0,
            "std": 2.0052015692526606,
            "ci95_low": 1.1666666666666667,
            "ci95_high": 2.3958333333333335,
            "min": 0.0,
            "max": 7.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 2.3958333333333335,
            "median": 1.0,
            "std": 2.9064553392214525,
            "ci95_low": 1.625,
            "ci95_high": 3.1875,
            "min": 0.0,
            "max": 11.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.012110015760376574,
            "median": 0.005353104514356053,
            "std": 0.014550286188052462,
            "ci95_low": 0.008381082868750686,
            "ci95_high": 0.01647371351589865,
            "min": 0.0,
            "max": 0.05045871559633028
          }
        },
        "22": {
          "modified_count": {
            "n": 48,
            "mean": 76.95833333333333,
            "median": 75.5,
            "std": 21.1137379579163,
            "ci95_low": 71.37447916666666,
            "ci95_high": 83.37708333333333,
            "min": 34.0,
            "max": 126.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.6875,
            "median": 0.0,
            "std": 1.2103072956898178,
            "ci95_low": 0.375,
            "ci95_high": 1.1041666666666667,
            "min": 0.0,
            "max": 5.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.7291666666666666,
            "median": 0.0,
            "std": 1.3499935699435344,
            "ci95_low": 0.375,
            "ci95_high": 1.1666666666666667,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.003187363097547483,
            "median": 0.0,
            "std": 0.005872395323466511,
            "ci95_low": 0.0017507130894940206,
            "ci95_high": 0.004949181249495169,
            "min": 0.0,
            "max": 0.026905829596412557
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "surface_biased_budget": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 30.0,
            "median": 28.0,
            "std": 7.213991035943049,
            "ci95_low": 27.8328125,
            "ci95_high": 32.021875,
            "min": 15.0,
            "max": 48.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 21.791666666666668,
            "median": 21.5,
            "std": 5.887693143800512,
            "ci95_low": 20.22760416666667,
            "ci95_high": 23.520833333333332,
            "min": 8.0,
            "max": 35.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 38.520833333333336,
            "median": 39.0,
            "std": 9.797936822220391,
            "ci95_low": 35.625,
            "ci95_high": 41.3125,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.351679707026851,
            "median": 0.36279854620976115,
            "std": 0.08226177545520746,
            "ci95_low": 0.3273894708827673,
            "ci95_high": 0.3733562573372996,
            "min": 0.12727272727272726,
            "max": 0.5357142857142857
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 39.791666666666664,
            "median": 39.0,
            "std": 9.110338297170358,
            "ci95_low": 37.51927083333334,
            "ci95_high": 42.501041666666666,
            "min": 18.0,
            "max": 62.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 24.0,
            "median": 24.0,
            "std": 6.1169164345008555,
            "ci95_low": 22.3328125,
            "ci95_high": 25.75,
            "min": 9.0,
            "max": 36.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 40.1875,
            "median": 41.0,
            "std": 10.321208444266592,
            "ci95_low": 37.309895833333336,
            "ci95_high": 43.126041666666666,
            "min": 12.0,
            "max": 61.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.34514566623170745,
            "median": 0.34218442670369087,
            "std": 0.08480344392365849,
            "ci95_low": 0.3213210285405551,
            "ci95_high": 0.36855598013365054,
            "min": 0.10256410256410256,
            "max": 0.5267857142857143
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 50.458333333333336,
            "median": 49.0,
            "std": 11.952960465461638,
            "ci95_low": 47.08229166666667,
            "ci95_high": 54.083333333333336,
            "min": 20.0,
            "max": 79.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 26.0625,
            "median": 27.0,
            "std": 6.684578801240958,
            "ci95_low": 24.1875,
            "ci95_high": 27.8125,
            "min": 9.0,
            "max": 41.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 41.9375,
            "median": 43.5,
            "std": 11.404323467439882,
            "ci95_low": 38.75,
            "ci95_high": 44.93802083333333,
            "min": 10.0,
            "max": 65.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.33886519517071284,
            "median": 0.333084442030953,
            "std": 0.08745959221099439,
            "ci95_low": 0.31387924718344956,
            "ci95_high": 0.36216403851636936,
            "min": 0.08547008547008547,
            "max": 0.5284552845528455
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 62.125,
            "median": 62.0,
            "std": 14.862740045720596,
            "ci95_low": 58.0,
            "ci95_high": 66.64635416666667,
            "min": 24.0,
            "max": 98.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 27.145833333333332,
            "median": 28.0,
            "std": 7.4330051777341195,
            "ci95_low": 24.958333333333332,
            "ci95_high": 29.396354166666665,
            "min": 7.0,
            "max": 44.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 44.020833333333336,
            "median": 44.5,
            "std": 12.658148863040317,
            "ci95_low": 40.49947916666667,
            "ci95_high": 47.58385416666667,
            "min": 12.0,
            "max": 72.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3394309805989059,
            "median": 0.34307036247334755,
            "std": 0.09378107114189417,
            "ci95_low": 0.3126744613461368,
            "ci95_high": 0.3644205072343863,
            "min": 0.1016949152542373,
            "max": 0.5106382978723404
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 85.625,
            "median": 87.0,
            "std": 21.417112511571986,
            "ci95_low": 79.62239583333333,
            "ci95_high": 91.7921875,
            "min": 32.0,
            "max": 142.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 29.729166666666668,
            "median": 29.5,
            "std": 8.56528746193352,
            "ci95_low": 27.3125,
            "ci95_high": 31.855729166666666,
            "min": 9.0,
            "max": 52.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 47.6875,
            "median": 47.0,
            "std": 14.607584003409553,
            "ci95_low": 43.72708333333333,
            "ci95_high": 51.938541666666666,
            "min": 15.0,
            "max": 82.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3354891468473215,
            "median": 0.32247453310696095,
            "std": 0.10376170360726342,
            "ci95_low": 0.3055957194747958,
            "ci95_high": 0.363671457955918,
            "min": 0.10869565217391304,
            "max": 0.5578231292517006
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 110.89583333333333,
            "median": 110.0,
            "std": 28.728063793189328,
            "ci95_low": 103.02031249999999,
            "ci95_high": 119.7765625,
            "min": 42.0,
            "max": 182.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 32.5625,
            "median": 32.0,
            "std": 11.03008433406865,
            "ci95_low": 29.333333333333332,
            "ci95_high": 35.52135416666667,
            "min": 10.0,
            "max": 58.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 52.666666666666664,
            "median": 52.0,
            "std": 18.134145202413656,
            "ci95_low": 47.33229166666667,
            "ci95_high": 57.95885416666667,
            "min": 17.0,
            "max": 97.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3348142438399973,
            "median": 0.33630952380952384,
            "std": 0.11131842001783247,
            "ci95_low": 0.30206486382201364,
            "ci95_high": 0.3684826441059928,
            "min": 0.11643835616438356,
            "max": 0.5773809523809523
          }
        },
        "14": {
          "modified_count": {
            "n": 48,
            "mean": 138.85416666666666,
            "median": 135.5,
            "std": 38.595114966865374,
            "ci95_low": 127.85104166666667,
            "ci95_high": 149.88072916666667,
            "min": 53.0,
            "max": 236.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 35.479166666666664,
            "median": 35.5,
            "std": 12.677061935068217,
            "ci95_low": 32.0625,
            "ci95_high": 39.022395833333334,
            "min": 14.0,
            "max": 65.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 57.145833333333336,
            "median": 57.0,
            "std": 21.086122592174746,
            "ci95_low": 51.729166666666664,
            "ci95_high": 62.606249999999996,
            "min": 22.0,
            "max": 105.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.33290774816433316,
            "median": 0.34311988844080954,
            "std": 0.12231069341630908,
            "ci95_low": 0.29798164600103594,
            "ci95_high": 0.3672325640343462,
            "min": 0.12790697674418605,
            "max": 0.6104651162790697
          }
        },
        "18": {
          "modified_count": {
            "n": 48,
            "mean": 202.5625,
            "median": 197.5,
            "std": 61.232788823336584,
            "ci95_low": 185.62291666666667,
            "ci95_high": 220.04583333333332,
            "min": 80.0,
            "max": 350.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 40.875,
            "median": 39.5,
            "std": 16.435004563431068,
            "ci95_low": 36.0609375,
            "ci95_high": 45.709375,
            "min": 11.0,
            "max": 78.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 65.5,
            "median": 65.5,
            "std": 25.910905040156354,
            "ci95_low": 58.371875,
            "ci95_high": 73.171875,
            "min": 19.0,
            "max": 122.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3323449094024898,
            "median": 0.3335714285714286,
            "std": 0.12715369581500577,
            "ci95_low": 0.2975330734585149,
            "ci95_high": 0.3673413836441902,
            "min": 0.09090909090909091,
            "max": 0.6022727272727273
          }
        },
        "22": {
          "modified_count": {
            "n": 48,
            "mean": 273.25,
            "median": 271.0,
            "std": 86.79561720885835,
            "ci95_low": 249.04114583333333,
            "ci95_high": 298.89427083333334,
            "min": 106.0,
            "max": 480.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 45.791666666666664,
            "median": 46.0,
            "std": 17.597298956247677,
            "ci95_low": 41.041666666666664,
            "ci95_high": 50.91770833333333,
            "min": 9.0,
            "max": 84.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 73.33333333333333,
            "median": 74.0,
            "std": 28.22183945497214,
            "ci95_low": 65.45833333333333,
            "ci95_high": 81.91927083333333,
            "min": 17.0,
            "max": 138.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3275569121300912,
            "median": 0.33270455489408834,
            "std": 0.12650711020725636,
            "ci95_low": 0.2928155778593804,
            "ci95_high": 0.3638555877380361,
            "min": 0.07555555555555556,
            "max": 0.5879396984924623
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
  "bounded_statement": "V5 compares no transmission, equal-budget uniform transmission, and equal-budget surface-biased transmission on material abundance and active-frontier accessibility."
}
```


# Stage 3 — Does Surface Placement Increase Realized Causal Work?

```json
{
  "groups_per_policy": 48,
  "audit_steps": [
    8,
    10,
    12,
    14,
    18
  ],
  "results": {
    "none": {
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 0.8541666666666666,
            "median": 1.0,
            "std": 1.0406244786451815,
            "ci95_low": 0.5833333333333334,
            "ci95_high": 1.1666666666666667,
            "min": 0.0,
            "max": 4.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.00640050345759726,
            "median": 0.00673591581239227,
            "std": 0.00783888785031557,
            "ci95_low": 0.004313586523086979,
            "ci95_high": 0.00866395615327632,
            "min": 0.0,
            "max": 0.03007518796992481
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.043098986423630546,
            "median": 0.022965905668409614,
            "std": 0.059521293516133125,
            "ci95_low": 0.027004902554709966,
            "ci95_high": 0.06080795177579923,
            "min": 0.0,
            "max": 0.2493444122139853
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.025238915416035058,
            "median": 0.022958575506910495,
            "std": 0.027679403886065372,
            "ci95_low": 0.017650413428471307,
            "ci95_high": 0.03337247627229813,
            "min": 0.0,
            "max": 0.07428134106868273
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.0625,
            "median": 0.0,
            "std": 0.24206145913796356,
            "ci95_low": 0.0,
            "ci95_high": 0.14583333333333334,
            "min": 0.0,
            "max": 1.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.03472222222222222,
            "median": 0.0,
            "std": 0.15574764925004028,
            "ci95_low": 0.0,
            "ci95_high": 0.08333333333333333,
            "min": 0.0,
            "max": 1.0
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 0.10416666666666667,
            "median": 0.0,
            "std": 0.30547663122114954,
            "ci95_low": 0.020833333333333332,
            "ci95_high": 0.1875,
            "min": 0.0,
            "max": 1.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.0007189630407168909,
            "median": 0.0,
            "std": 0.0021150105086908343,
            "ci95_low": 0.00014977528466737102,
            "ci95_high": 0.0013333419612743978,
            "min": 0.0,
            "max": 0.007246376811594203
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.0036243503548059053,
            "median": 0.0,
            "std": 0.012573798393118235,
            "ci95_low": 0.0006702595796329406,
            "ci95_high": 0.007936915039491094,
            "min": 0.0,
            "max": 0.07381680683638658
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.0036243503548059053,
            "median": 0.0,
            "std": 0.012573798393118235,
            "ci95_low": 0.0007791556011684034,
            "ci95_high": 0.0074931152750967395,
            "min": 0.0,
            "max": 0.07381680683638658
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
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
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
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
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
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
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
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
    "uniform_budget": {
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 19.0625,
            "median": 19.0,
            "std": 6.39793667911773,
            "ci95_low": 17.229166666666668,
            "ci95_high": 20.917708333333334,
            "min": 4.0,
            "max": 36.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.14660562582891115,
            "median": 0.1447272727272727,
            "std": 0.04905662835681619,
            "ci95_low": 0.1332190721822746,
            "ci95_high": 0.16148104401870947,
            "min": 0.03125,
            "max": 0.26277372262773724
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 1.475056858206501,
            "median": 1.367323229576966,
            "std": 0.5086787137672016,
            "ci95_low": 1.3388545372201737,
            "ci95_high": 1.613713188148924,
            "min": 0.43593908219728694,
            "max": 2.755453837005767
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.07843416443090487,
            "median": 0.0788113839467483,
            "std": 0.010465270429957192,
            "ci95_low": 0.07559601464111643,
            "ci95_high": 0.08158633781356076,
            "min": 0.05947174098082087,
            "max": 0.10898477054932174
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 1.5208333333333333,
            "median": 1.0,
            "std": 1.3538461159066624,
            "ci95_low": 1.1666666666666667,
            "ci95_high": 1.9166666666666667,
            "min": 0.0,
            "max": 6.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.08081918348868779,
            "median": 0.06066176470588235,
            "std": 0.08389563812664343,
            "ci95_low": 0.05804726608989148,
            "ci95_high": 0.10457167549338033,
            "min": 0.0,
            "max": 0.5
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 12.166666666666666,
            "median": 11.5,
            "std": 5.3359368645273735,
            "ci95_low": 10.666145833333333,
            "ci95_high": 13.6875,
            "min": 1.0,
            "max": 25.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.08447301875782136,
            "median": 0.0821406665303619,
            "std": 0.03766517015907,
            "ci95_low": 0.0744678685082902,
            "ci95_high": 0.0954505175582383,
            "min": 0.0072992700729927005,
            "max": 0.17006802721088435
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.920825744982587,
            "median": 0.876956034668356,
            "std": 0.4382422132152103,
            "ci95_low": 0.7913184869562531,
            "ci95_high": 1.0387910963833016,
            "min": 0.0439407679007674,
            "max": 2.073704274151562
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.07411648311928126,
            "median": 0.07401105252507216,
            "std": 0.013060553113389564,
            "ci95_low": 0.07046982652924841,
            "ci95_high": 0.07775021593254791,
            "min": 0.0439407679007674,
            "max": 0.11191846787164435
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.875,
            "median": 1.0,
            "std": 0.8569568250501305,
            "ci95_low": 0.6458333333333334,
            "ci95_high": 1.1046874999999996,
            "min": 0.0,
            "max": 3.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.06898782196656238,
            "median": 0.05718954248366013,
            "std": 0.07373379660386067,
            "ci95_low": 0.04858118819689712,
            "ci95_high": 0.09133674681518753,
            "min": 0.0,
            "max": 0.25
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 8.145833333333334,
            "median": 7.5,
            "std": 4.128102789283339,
            "ci95_low": 7.0203125,
            "ci95_high": 9.333333333333334,
            "min": 0.0,
            "max": 19.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.05233291498616418,
            "median": 0.04624542124542125,
            "std": 0.027424613202914987,
            "ci95_low": 0.04522354280369371,
            "ci95_high": 0.05979618066318604,
            "min": 0.0,
            "max": 0.1292517006802721
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.617371639497271,
            "median": 0.5357731239472654,
            "std": 0.3555051070928034,
            "ci95_low": 0.5183184615158978,
            "ci95_high": 0.7216145717959116,
            "min": 0.0,
            "max": 1.5647683341838265
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.07213645331734145,
            "median": 0.0716705929281998,
            "std": 0.01839988629808989,
            "ci95_low": 0.06675988156652128,
            "ci95_high": 0.0772057119985521,
            "min": 0.0,
            "max": 0.11929066550444285
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.6041666666666666,
            "median": 0.0,
            "std": 0.7836767864085011,
            "ci95_low": 0.3958333333333333,
            "ci95_high": 0.8333333333333334,
            "min": 0.0,
            "max": 3.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.06762955182072829,
            "median": 0.0,
            "std": 0.08644651901329188,
            "ci95_low": 0.04477892545907251,
            "ci95_high": 0.09198705697556799,
            "min": 0.0,
            "max": 0.3333333333333333
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 5.583333333333333,
            "median": 5.5,
            "std": 3.258535799336192,
            "ci95_low": 4.6453125,
            "ci95_high": 6.5421875,
            "min": 0.0,
            "max": 16.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.03316887873807645,
            "median": 0.03202761826633853,
            "std": 0.019397577353726377,
            "ci95_low": 0.027659225057597152,
            "ci95_high": 0.038955836196245965,
            "min": 0.0,
            "max": 0.09195402298850575
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.4167423852738776,
            "median": 0.3992182340994414,
            "std": 0.2556762626572753,
            "ci95_low": 0.346628176590925,
            "ci95_high": 0.49736976246931724,
            "min": 0.0,
            "max": 1.173944315908174
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.07019614514187766,
            "median": 0.07042368195781351,
            "std": 0.02486130486686968,
            "ci95_low": 0.0631463327397036,
            "ci95_high": 0.07732887438936949,
            "min": 0.0,
            "max": 0.14872102096792927
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.3958333333333333,
            "median": 0.0,
            "std": 0.567875548768292,
            "ci95_low": 0.25,
            "ci95_high": 0.5625,
            "min": 0.0,
            "max": 2.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.07505787037037036,
            "median": 0.0,
            "std": 0.15793021372456917,
            "ci95_low": 0.03797825727513227,
            "ci95_high": 0.12735697751322747,
            "min": 0.0,
            "max": 1.0
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 1.9166666666666667,
            "median": 1.0,
            "std": 2.089989367330742,
            "ci95_low": 1.3333333333333333,
            "ci95_high": 2.4583333333333335,
            "min": 0.0,
            "max": 7.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.009898802526943926,
            "median": 0.0051422377326565145,
            "std": 0.01070898646716881,
            "ci95_low": 0.0067843089434819264,
            "ci95_high": 0.013023409145564043,
            "min": 0.0,
            "max": 0.035175879396984924
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 0.13611574139769209,
            "median": 0.08920958969397777,
            "std": 0.16108879724755534,
            "ci95_low": 0.09038918622677097,
            "ci95_high": 0.18283296788774547,
            "min": 0.0,
            "max": 0.6248842982655647
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.04325913734001979,
            "median": 0.05325189039989548,
            "std": 0.038168907682479,
            "ci95_low": 0.03208314781086699,
            "ci95_high": 0.05361962487638025,
            "min": 0.0,
            "max": 0.14569281868706496
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 0.16666666666666666,
            "median": 0.0,
            "std": 0.42491829279939874,
            "ci95_low": 0.0625,
            "ci95_high": 0.2916666666666667,
            "min": 0.0,
            "max": 2.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.05109126984126985,
            "median": 0.0,
            "std": 0.13378427706007073,
            "ci95_low": 0.015625,
            "ci95_high": 0.09152405753968253,
            "min": 0.0,
            "max": 0.5
          }
        }
      }
    },
    "surface_biased_budget": {
      "summary": {
        "8": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 44.4375,
            "median": 45.0,
            "std": 12.63082580105777,
            "ci95_low": 41.06197916666667,
            "ci95_high": 48.20885416666667,
            "min": 20.0,
            "max": 84.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.33995657222494957,
            "median": 0.33829057938965057,
            "std": 0.0906383666829593,
            "ci95_low": 0.31566549061828003,
            "ci95_high": 0.3680740044703534,
            "min": 0.15503875968992248,
            "max": 0.6461538461538462
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 3.9281855972442457,
            "median": 3.9946942437798576,
            "std": 1.1412493997196844,
            "ci95_low": 3.6119104590722584,
            "ci95_high": 4.255559184864686,
            "min": 1.7230601104326286,
            "max": 8.161515631118172
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.0885588345110524,
            "median": 0.08860349661549928,
            "std": 0.004813222260913388,
            "ci95_low": 0.08721649055625033,
            "ci95_high": 0.08998045661522651,
            "min": 0.07959156451144879,
            "max": 0.10160813637935562
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 4.229166666666667,
            "median": 4.0,
            "std": 2.152900982137564,
            "ci95_low": 3.6875,
            "ci95_high": 4.833333333333333,
            "min": 1.0,
            "max": 9.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.0968309317389704,
            "median": 0.09838709677419355,
            "std": 0.046536269358640324,
            "ci95_low": 0.08456507338951048,
            "ci95_high": 0.11098031468840551,
            "min": 0.020833333333333332,
            "max": 0.225
          }
        },
        "10": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 48.541666666666664,
            "median": 51.0,
            "std": 14.205278263925544,
            "ci95_low": 44.602604166666666,
            "ci95_high": 52.39895833333333,
            "min": 16.0,
            "max": 98.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.3354080705511832,
            "median": 0.33332635106828656,
            "std": 0.0933633223213378,
            "ci95_low": 0.30971162597683854,
            "ci95_high": 0.3616766216392635,
            "min": 0.11764705882352941,
            "max": 0.6805555555555556
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 4.333867810586423,
            "median": 4.467903549614956,
            "std": 1.3247007878026629,
            "ci95_low": 3.9548934125276434,
            "ci95_high": 4.721431703151648,
            "min": 1.2066060801003942,
            "max": 9.32211745540775
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.08905695037284844,
            "median": 0.08944224871864168,
            "std": 0.005153706594857468,
            "ci95_low": 0.0876970142298639,
            "ci95_high": 0.09049028000741925,
            "min": 0.07541288000627464,
            "max": 0.10203994029957929
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 4.104166666666667,
            "median": 4.0,
            "std": 2.0024941045828046,
            "ci95_low": 3.5416666666666665,
            "ci95_high": 4.645833333333333,
            "min": 0.0,
            "max": 8.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.08493186348192798,
            "median": 0.07814407814407814,
            "std": 0.03716975829167837,
            "ci95_low": 0.07453326314686763,
            "ci95_high": 0.09565081228093371,
            "min": 0.0,
            "max": 0.17647058823529413
          }
        },
        "12": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 52.333333333333336,
            "median": 54.0,
            "std": 15.181311610734502,
            "ci95_low": 47.74947916666667,
            "ci95_high": 56.376041666666666,
            "min": 15.0,
            "max": 104.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.33206008231430983,
            "median": 0.3427062296100668,
            "std": 0.09320198963508766,
            "ci95_low": 0.30557438273023674,
            "ci95_high": 0.3589269184387927,
            "min": 0.0949367088607595,
            "max": 0.65
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 4.629451785171358,
            "median": 4.787805253203482,
            "std": 1.3412678323496328,
            "ci95_low": 4.272189329488499,
            "ci95_high": 5.021740770638436,
            "min": 1.2859517040260986,
            "max": 8.68602663446476
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.08844997958959833,
            "median": 0.08850591321145493,
            "std": 0.0049705570855764335,
            "ci95_low": 0.08702376178552786,
            "ci95_high": 0.0898488250301908,
            "min": 0.07616450867045381,
            "max": 0.09691822993463367
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 4.145833333333333,
            "median": 4.0,
            "std": 2.0513164810812485,
            "ci95_low": 3.5625,
            "ci95_high": 4.708333333333333,
            "min": 0.0,
            "max": 11.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.07779051734535648,
            "median": 0.07335007173601148,
            "std": 0.03786135868349087,
            "ci95_low": 0.06819488270626525,
            "ci95_high": 0.08877174769757286,
            "min": 0.0,
            "max": 0.2
          }
        },
        "14": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 57.145833333333336,
            "median": 59.0,
            "std": 17.321698318550894,
            "ci95_low": 52.228125,
            "ci95_high": 62.166666666666664,
            "min": 16.0,
            "max": 121.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.33331851899591003,
            "median": 0.34911028346782536,
            "std": 0.09732208824295269,
            "ci95_low": 0.30575265853370415,
            "ci95_high": 0.36252840384266627,
            "min": 0.0963855421686747,
            "max": 0.6836158192090396
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 5.148468225431696,
            "median": 5.354650002173269,
            "std": 1.6161252979038534,
            "ci95_low": 4.695597046300383,
            "ci95_high": 5.6173606708318475,
            "min": 1.43874703881706,
            "max": 11.260269671215527
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.08987771620559824,
            "median": 0.08962171906067434,
            "std": 0.0053326434621557926,
            "ci95_low": 0.0883130719352207,
            "ci95_high": 0.09141929232322293,
            "min": 0.07561428247409198,
            "max": 0.10042439289616333
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 5.395833333333333,
            "median": 5.0,
            "std": 2.261448497214906,
            "ci95_low": 4.75,
            "ci95_high": 5.979166666666667,
            "min": 0.0,
            "max": 10.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.09429446461440393,
            "median": 0.09602212855637512,
            "std": 0.03552870021170784,
            "ci95_low": 0.0839661045995473,
            "ci95_high": 0.10438503675749566,
            "min": 0.0,
            "max": 0.2
          }
        },
        "18": {
          "exposed_frontier_count": {
            "n": 48,
            "mean": 65.64583333333333,
            "median": 64.5,
            "std": 22.29021607429791,
            "ci95_low": 59.56041666666667,
            "ci95_high": 72.35625,
            "min": 15.0,
            "max": 152.0
          },
          "exposed_frontier_fraction": {
            "n": 48,
            "mean": 0.33285273674946386,
            "median": 0.32550254623425356,
            "std": 0.10786296526579062,
            "ci95_low": 0.3041174058350127,
            "ci95_high": 0.3633938605580207,
            "min": 0.0797872340425532,
            "max": 0.7238095238095238
          },
          "sum_delta_p": {
            "n": 48,
            "mean": 5.99165161150606,
            "median": 5.7893229426064945,
            "std": 2.1353090210728105,
            "ci95_low": 5.402958440962602,
            "ci95_high": 6.599841022300655,
            "min": 1.288675494716244,
            "max": 14.746465582205484
          },
          "mean_delta_p_exposed": {
            "n": 48,
            "mean": 0.09104198894324415,
            "median": 0.0915909687969764,
            "std": 0.0049583778944227875,
            "ci95_low": 0.08958327768565023,
            "ci95_high": 0.09240746449047442,
            "min": 0.07841628022543576,
            "max": 0.10480675705762713
          },
          "realized_causal_flips": {
            "n": 48,
            "mean": 6.291666666666667,
            "median": 6.0,
            "std": 3.4638510200193204,
            "ci95_low": 5.354166666666667,
            "ci95_high": 7.291666666666667,
            "min": 0.0,
            "max": 19.0
          },
          "realized_flip_fraction_of_exposed": {
            "n": 48,
            "mean": 0.09368391028546451,
            "median": 0.09111111111111111,
            "std": 0.04019707876942881,
            "ci95_low": 0.08193149428359074,
            "ci95_high": 0.10529268842015063,
            "min": 0.0,
            "max": 0.18518518518518517
          }
        }
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "V5 measures whether matched-budget surface placement increases frontier availability, total probability leverage, and realized CRN-controlled causal attachment flips."
}
```


# Stage 4 — Late Causal Ablation by Transmission Policy

```json
{
  "late_ablation_step": 14,
  "followup_steps": 4,
  "results": {
    "none": {
      "frontier_contact_at_ablation": {
        "n": 48,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 48,
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
        "permutations": 2000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      }
    },
    "uniform_budget": {
      "frontier_contact_at_ablation": {
        "n": 48,
        "mean": 5.979166666666667,
        "median": 5.0,
        "std": 4.10025194009127,
        "ci95_low": 4.9578125,
        "ci95_high": 7.208333333333333,
        "min": 0.0,
        "max": 18.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 48,
        "mean": 0.0009044039577559641,
        "median": 0.0,
        "std": 0.0014725933717068508,
        "ci95_low": 0.0005080193639551659,
        "ci95_high": 0.0013660440822213216,
        "min": 0.0,
        "max": 0.005979073243647235
      },
      "paired_ridge_test": {
        "statistic": 0.3286774809164163,
        "p_value": 0.0069965017491254375,
        "permutations": 2000,
        "null_mean": 0.16950879855108567,
        "null_q95": 0.2615652213908785,
        "null_q99": 0.313753161426542
      }
    },
    "surface_biased_budget": {
      "frontier_contact_at_ablation": {
        "n": 48,
        "mean": 57.1875,
        "median": 54.5,
        "std": 18.27185477950537,
        "ci95_low": 51.854166666666664,
        "ci95_high": 62.291666666666664,
        "min": 21.0,
        "max": 108.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 48,
        "mean": 0.01646926134295169,
        "median": 0.015554434183118582,
        "std": 0.007481259413434953,
        "ci95_low": 0.014351552383882677,
        "ci95_high": 0.018660379908805272,
        "min": 0.0031520882584712374,
        "max": 0.03802008608321377
      },
      "paired_ridge_test": {
        "statistic": 2.8023255402213767,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.23187688156589215,
        "null_q95": 0.40977907943024533,
        "null_q99": 0.5262037587951967
      }
    }
  },
  "status": "MEASURED",
  "interpretation": "Whole-crystal ablation is corroborative. The primary mechanistic question is whether matched-budget surface placement produces more accessible and causally active state than uniform placement."
}
```


# Stage 5 — Bounded Chapter 18 V5 Verdict

```json
{
  "experiment_role": "EXPLORATORY MECHANISM COMPARISON",
  "chapter": 18,
  "question": "Can historical material be preferentially preserved where future growth occurs, without increasing the nominal copying budget?",
  "matched_transmission_fraction": 0.5,
  "surface_targets_more_exposed_material": true,
  "surface_improves_late_frontier_access": true,
  "surface_improves_late_realized_causal_flips": true,
  "late_step_summary": {
    "uniform_budget": {
      "mean_frontier_contact": 5.208333333333333,
      "mean_realized_causal_flips": 0.3958333333333333
    },
    "surface_biased_budget": {
      "mean_frontier_contact": 57.145833333333336,
      "mean_realized_causal_flips": 5.395833333333333
    }
  },
  "status": "SUPPORTED",
  "bounded_claim": "At the same nominal transmission fraction, preferentially placing propagated material on more exposed newly attached cells increased late frontier accessibility and realized local causal attachment flips relative to uniform allocation.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "attention",
    "homeostasis",
    "active boundary",
    "phase transition",
    "critical threshold",
    "information storage",
    "genetic inheritance",
    "epigenetics",
    "agency",
    "individuality",
    "reproduction",
    "life"
  ],
  "next_question": "If surface-biased placement is supported, test whether the state can be updated or displaced by a later experience while the copying budget remains fixed. If not, return to the local propagation rule rather than increasing causal gain."
}
```
