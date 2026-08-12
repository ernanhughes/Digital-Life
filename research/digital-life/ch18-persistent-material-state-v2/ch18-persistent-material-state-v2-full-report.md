# Chapter 18 — Can Experience Change the Material? (V2 Autopsy)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v2",
  "schema_version": 2,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY MECHANISM AUTOPSY",
  "profile": "quick",
  "profile_config": {
    "groups": 32,
    "radius": 64,
    "warmup_steps": 14,
    "experience_horizon": 8,
    "experience_pulse_step": 3,
    "accessibility_observation_steps": [
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      12,
      14
    ],
    "ablation_probe_steps": [
      5,
      7,
      10,
      14
    ],
    "ablation_followup_horizon": 3,
    "ablation_primary_endpoint": 3,
    "message_gain": 0.65,
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "permutations": 1000,
    "bootstrap_reps": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260815,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "experimental_extension_unchanged_from_v1": true,
  "material_mechanism": {
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "persistence_rule": "modified remains modified",
    "causal_rule": "modified occupied neighbours bias later frontier attachment"
  },
  "v1_result_being_autopsied": "Persistent labels were written and retained, but retained-vs-erased continuations were exactly identical at the late ablation.",
  "v2_hypothesis": "Persistent material becomes causally inert when growth buries the modified cells and the active frontier no longer has modified occupied neighbours.",
  "scientific_boundary": "No new propagation, inheritance, memory, learning, or adaptation mechanism is introduced in v2.",
  "started_at_unix": 1786537635.3227508,
  "finished_at_unix": 1786537640.3051827,
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "SUPPORTED",
  "final_status": "SUPPORTED",
  "next_question": "Design, but do not yet assume, the smallest local mechanism that keeps experience-written material in causal contact with the active growth surface."
}
```

# Stage 0 — Extension Audit

```json
{
  "role": "EXTENSION AUDIT",
  "base_model_version": "digital-crystal-v1-frozen",
  "experimental_extension": "digital-crystal-persistent-material-state-v2",
  "canonical_model_modified": false,
  "exact_when_material_state_empty": true,
  "material_extension_exact_reproducibility": true,
  "write_probability": 0.2,
  "modified_neighbor_gain": 0.3,
  "interpretation": "The material-state extension leaves the Chapter 17 CRN growth process unchanged while no cells are modified. The extension becomes causally active only after experience writes local material state."
}
```


# Stage 1 — Does Persistent Material Remain Reachable?

```json
{
  "groups": 32,
  "experience_pulse_zero_index": 3,
  "experience_pulse_elapsed_step": 4,
  "observation_steps": [
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    12,
    14
  ],
  "modified_cells_immediately_after_write": {
    "n": 32,
    "mean": 19.625,
    "median": 19.5,
    "std": 3.838538133196022,
    "ci95_low": 18.21875,
    "ci95_high": 21.0,
    "min": 10.0,
    "max": 28.0
  },
  "first_step_with_zero_frontier_contact": {
    "n": 32,
    "mean": 8.78125,
    "median": 9.0,
    "std": 1.1383753500054365,
    "ci95_low": 8.40625,
    "ci95_high": 9.21875,
    "min": 7.0,
    "max": 13.0
  },
  "summary": {
    "4": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.25,
        "ci95_high": 21.03125,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.31171875,
        "ci95_high": 20.90703125,
        "min": 10.0,
        "max": 28.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 106.46875,
        "median": 105.5,
        "std": 8.422382289916554,
        "ci95_low": 103.49921875,
        "ci95_high": 109.190625,
        "min": 86.0,
        "max": 123.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 36.4375,
        "median": 35.5,
        "std": 7.684958929623502,
        "ci95_low": 33.8421875,
        "ci95_high": 39.15625,
        "min": 20.0,
        "max": 55.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.3429608340728929,
        "median": 0.32857142857142857,
        "std": 0.0701106621623176,
        "ci95_low": 0.3190892218955405,
        "ci95_high": 0.3653010352689152,
        "min": 0.19642857142857142,
        "max": 0.46296296296296297
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 1.169112409322028,
        "median": 1.176206896551724,
        "std": 0.05638638733885192,
        "ci95_low": 1.149467395460988,
        "ci95_high": 1.1878028139704706,
        "min": 1.0512820512820513,
        "max": 1.2727272727272727
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 2.46875,
        "median": 2.0,
        "std": 0.4990224819584785,
        "ci95_low": 2.28125,
        "ci95_high": 2.625,
        "min": 2.0,
        "max": 3.0
      }
    },
    "5": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.31171875,
        "ci95_high": 20.81328125,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 11.875,
        "median": 12.0,
        "std": 3.266783586342995,
        "ci95_low": 10.7171875,
        "ci95_high": 13.0,
        "min": 6.0,
        "max": 20.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 111.21875,
        "median": 111.0,
        "std": 6.720929878930445,
        "ci95_low": 108.90625,
        "ci95_high": 113.4703125,
        "min": 89.0,
        "max": 126.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 17.0,
        "median": 16.0,
        "std": 4.993746088859544,
        "ci95_low": 15.31171875,
        "ci95_high": 18.8125,
        "min": 10.0,
        "max": 31.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.15307921936800858,
        "median": 0.14494179373667815,
        "std": 0.04442686782919896,
        "ci95_low": 0.13839481214286023,
        "ci95_high": 0.1696214986662937,
        "min": 0.08771929824561403,
        "max": 0.26956521739130435
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 1.1157460660605145,
        "median": 1.108187134502924,
        "std": 0.0661747588003225,
        "ci95_low": 1.092574871798001,
        "ci95_high": 1.1385418881182134,
        "min": 1.0,
        "max": 1.25
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 2.09375,
        "median": 2.0,
        "std": 0.5787580992953792,
        "ci95_low": 1.90625,
        "ci95_high": 2.28125,
        "min": 1.0,
        "max": 3.0
      }
    },
    "6": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.28046875,
        "ci95_high": 20.96875,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 5.875,
        "median": 6.0,
        "std": 2.057759704144291,
        "ci95_low": 5.18671875,
        "ci95_high": 6.65625,
        "min": 2.0,
        "max": 10.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 117.75,
        "median": 118.0,
        "std": 8.329165624478842,
        "ci95_low": 114.7796875,
        "ci95_high": 120.50078125,
        "min": 99.0,
        "max": 131.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 7.375,
        "median": 8.0,
        "std": 2.858649156507318,
        "ci95_low": 6.375,
        "ci95_high": 8.34375,
        "min": 2.0,
        "max": 14.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.06269751971314191,
        "median": 0.06350806451612903,
        "std": 0.023646642458204456,
        "ci95_low": 0.05444752094244392,
        "ci95_high": 0.0710234887729428,
        "min": 0.015384615384615385,
        "max": 0.109375
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 1.0644852543290044,
        "median": 1.0,
        "std": 0.09467228427667508,
        "ci95_low": 1.0334195752164501,
        "ci95_high": 1.0985878596230159,
        "min": 1.0,
        "max": 1.3333333333333333
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 1.46875,
        "median": 1.0,
        "std": 0.6115745559619039,
        "ci95_low": 1.25,
        "ci95_high": 1.6875,
        "min": 1.0,
        "max": 3.0
      }
    },
    "7": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.34375,
        "ci95_high": 21.00078125,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 2.53125,
        "median": 2.0,
        "std": 1.6390617552429194,
        "ci95_low": 1.96875,
        "ci95_high": 3.09375,
        "min": 0.0,
        "max": 7.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 124.375,
        "median": 124.5,
        "std": 7.967708265241644,
        "ci95_low": 121.53125,
        "ci95_high": 126.84375,
        "min": 105.0,
        "max": 140.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 2.75,
        "median": 2.0,
        "std": 1.7320508075688772,
        "ci95_low": 2.125,
        "ci95_high": 3.375,
        "min": 0.0,
        "max": 7.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.02185859902713763,
        "median": 0.016677089847821555,
        "std": 0.013238731466990271,
        "ci95_low": 0.01736425084308263,
        "ci95_high": 0.026319846650916225,
        "min": 0.0,
        "max": 0.05
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.9784226190476191,
        "median": 1.0,
        "std": 0.2743336969619886,
        "ci95_low": 0.8786737351190477,
        "ci95_high": 1.0599237351190478,
        "min": 0.0,
        "max": 1.5
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 1.09375,
        "median": 1.0,
        "std": 0.45821494683172437,
        "ci95_low": 0.9375,
        "ci95_high": 1.25,
        "min": 0.0,
        "max": 2.0
      }
    },
    "8": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.37421875,
        "ci95_high": 20.9375,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 0.625,
        "median": 1.0,
        "std": 0.649519052838329,
        "ci95_low": 0.40625,
        "ci95_high": 0.84375,
        "min": 0.0,
        "max": 2.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 131.65625,
        "median": 131.0,
        "std": 8.145586899511907,
        "ci95_low": 128.7484375,
        "ci95_high": 134.375,
        "min": 118.0,
        "max": 146.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 0.6875,
        "median": 1.0,
        "std": 0.7680128579652817,
        "ci95_low": 0.4375,
        "ci95_high": 0.96875,
        "min": 0.0,
        "max": 3.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.005170492147210361,
        "median": 0.00709362579866177,
        "std": 0.005623234787084077,
        "ci95_low": 0.0033933808393415373,
        "ci95_high": 0.007089579171650803,
        "min": 0.0,
        "max": 0.02054794520547945
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.53125,
        "median": 1.0,
        "std": 0.4990224819584785,
        "ci95_low": 0.34375,
        "ci95_high": 0.6882812499999993,
        "min": 0.0,
        "max": 1.0
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 0.53125,
        "median": 1.0,
        "std": 0.4990224819584785,
        "ci95_low": 0.34375,
        "ci95_high": 0.6875,
        "min": 0.0,
        "max": 1.0
      }
    },
    "9": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.3125,
        "ci95_high": 20.96875,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 0.21875,
        "median": 0.0,
        "std": 0.41339864235384227,
        "ci95_low": 0.09375,
        "ci95_high": 0.375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 139.875,
        "median": 140.0,
        "std": 8.727650027355589,
        "ci95_low": 136.9375,
        "ci95_high": 143.0625,
        "min": 124.0,
        "max": 158.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 0.21875,
        "median": 0.0,
        "std": 0.41339864235384227,
        "ci95_low": 0.09375,
        "ci95_high": 0.375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0015629581312017115,
        "median": 0.0,
        "std": 0.002956165113002334,
        "ci95_low": 0.00046472241642177774,
        "ci95_high": 0.0026866949694981978,
        "min": 0.0,
        "max": 0.007575757575757576
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.21875,
        "median": 0.0,
        "std": 0.41339864235384227,
        "ci95_low": 0.09375,
        "ci95_high": 0.375,
        "min": 0.0,
        "max": 1.0
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 0.21875,
        "median": 0.0,
        "std": 0.41339864235384227,
        "ci95_low": 0.09375,
        "ci95_high": 0.375,
        "min": 0.0,
        "max": 1.0
      }
    },
    "10": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.21875,
        "ci95_high": 21.0,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 147.4375,
        "median": 149.0,
        "std": 7.377912560473999,
        "ci95_low": 144.9375,
        "ci95_high": 150.1890625,
        "min": 133.0,
        "max": 160.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.00021551724137931034,
        "median": 0.0,
        "std": 0.0011999492161271599,
        "ci95_low": 0.0,
        "ci95_high": 0.000646551724137931,
        "min": 0.0,
        "max": 0.006896551724137931
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      }
    },
    "12": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.34296875,
        "ci95_high": 20.9375,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 161.03125,
        "median": 159.0,
        "std": 11.060866757967027,
        "ci95_low": 157.62421875,
        "ci95_high": 164.875,
        "min": 142.0,
        "max": 195.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0001893939393939394,
        "median": 0.0,
        "std": 0.001054500826293565,
        "ci95_low": 0.0,
        "ci95_high": 0.0005681818181818182,
        "min": 0.0,
        "max": 0.006060606060606061
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
        "mean": 0.03125,
        "median": 0.0,
        "std": 0.17399263633843817,
        "ci95_low": 0.0,
        "ci95_high": 0.09375,
        "min": 0.0,
        "max": 1.0
      }
    },
    "14": {
      "modified_count": {
        "n": 32,
        "mean": 19.625,
        "median": 19.5,
        "std": 3.838538133196022,
        "ci95_low": 18.28125,
        "ci95_high": 20.90625,
        "min": 10.0,
        "max": 28.0
      },
      "modified_boundary_count": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_count": {
        "n": 32,
        "mean": 172.25,
        "median": 169.0,
        "std": 10.108783309577865,
        "ci95_low": 169.0,
        "ci95_high": 175.96953125,
        "min": 158.0,
        "max": 203.0
      },
      "frontier_cells_with_modified_neighbor": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "mean_modified_neighbors_among_exposed_frontier": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "max_modified_neighbors_on_frontier": {
        "n": 32,
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
  "status": "MEASURED",
  "bounded_statement": "V2 directly measures whether experience-written material remains adjacent to current growth opportunities. Persistent labels are not treated as causally accessible once no frontier cell has a modified occupied neighbour."
}
```


# Stage 2 — When Does Persistent State Stop Mattering?

```json
{
  "groups": 32,
  "probe_steps": [
    5,
    7,
    10,
    14
  ],
  "followup_horizon": 3,
  "alpha": 0.05,
  "results": {
    "5": {
      "probe_elapsed_step": 5,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 16.6875,
        "median": 17.0,
        "std": 4.433096406576333,
        "ci95_low": 15.15546875,
        "ci95_high": 18.21875,
        "min": 6.0,
        "max": 24.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.15183491971224217,
        "median": 0.16015449227538622,
        "std": 0.03707545293448811,
        "ci95_low": 0.13851772530915882,
        "ci95_high": 0.16447911286907058,
        "min": 0.061224489795918366,
        "max": 0.21100917431192662
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 0.002984307758185673,
        "median": 0.0019052042923345465,
        "std": 0.00366245376339345,
        "ci95_low": 0.0018481959104609332,
        "ci95_high": 0.004222762106131355,
        "min": 0.0,
        "max": 0.01669195751138088
      },
      "paired_ridge_test": {
        "statistic": 0.574540597133495,
        "p_value": 0.014985014985014986,
        "permutations": 1000,
        "null_mean": 0.27608527264697186,
        "null_q95": 0.48983669554776227,
        "null_q99": 0.6353019722699024
      },
      "causal_effect_detected": true
    },
    "7": {
      "probe_elapsed_step": 7,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 2.25,
        "median": 2.0,
        "std": 1.7320508075688772,
        "ci95_low": 1.625,
        "ci95_high": 2.875,
        "min": 0.0,
        "max": 8.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.017590920226151323,
        "median": 0.01626123744050767,
        "std": 0.013114346359260646,
        "ci95_low": 0.013181825835561272,
        "ci95_high": 0.022089999918106805,
        "min": 0.0,
        "max": 0.057971014492753624
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 8.890469416785207e-05,
        "median": 0.0,
        "std": 0.0004950003878760688,
        "ci95_low": 0.0,
        "ci95_high": 0.0002667140825035562,
        "min": 0.0,
        "max": 0.002844950213371266
      },
      "paired_ridge_test": {
        "statistic": 0.03192550714998349,
        "p_value": 0.5014985014985015,
        "permutations": 1000,
        "null_mean": 0.03192550714998343,
        "null_q95": 0.03192550714998354,
        "null_q99": 0.03192550714998354
      },
      "causal_effect_detected": false
    },
    "10": {
      "probe_elapsed_step": 10,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
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
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "causal_effect_detected": false
    },
    "14": {
      "probe_elapsed_step": 14,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
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
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "causal_effect_detected": false
    }
  },
  "status": "MEASURED",
  "bounded_statement": "The erase ablation is evaluated before, near, and after loss of frontier contact. This tests whether causal efficacy tracks accessibility of the persistent material state."
}
```


# Stage 3 — Does Causal Effect Track Frontier Accessibility?

```json
{
  "hypothesis": "Persistent labels become causally inert when growth moves beyond them and current frontier cells no longer contact modified material.",
  "probe_summary": [
    {
      "probe": 5,
      "mean_frontier_contact_count": 16.6875,
      "mean_frontier_exposed_fraction": 0.15183491971224217,
      "mean_post_ablation_symdiff": 0.002984307758185673,
      "ablation_p_value": 0.014985014985014986,
      "causal_effect_detected": true
    },
    {
      "probe": 7,
      "mean_frontier_contact_count": 2.25,
      "mean_frontier_exposed_fraction": 0.017590920226151323,
      "mean_post_ablation_symdiff": 8.890469416785207e-05,
      "ablation_p_value": 0.5014985014985015,
      "causal_effect_detected": false
    },
    {
      "probe": 10,
      "mean_frontier_contact_count": 0.0,
      "mean_frontier_exposed_fraction": 0.0,
      "mean_post_ablation_symdiff": 0.0,
      "ablation_p_value": 1.0,
      "causal_effect_detected": false
    },
    {
      "probe": 14,
      "mean_frontier_contact_count": 0.0,
      "mean_frontier_exposed_fraction": 0.0,
      "mean_post_ablation_symdiff": 0.0,
      "ablation_p_value": 1.0,
      "causal_effect_detected": false
    }
  ],
  "positive_ablation_while_contact_present": true,
  "all_tested_post_contact_ablation_effects_absent": true,
  "status": "SUPPORTED",
  "bounded_statement": "Timed ablations are consistent with the hypothesis that persistent material state matters only while it remains causally accessible to the active growth frontier."
}
```


# Stage 4 — Bounded Chapter 18 V2 Verdict

```json
{
  "experiment_role": "EXPLORATORY MECHANISM AUTOPSY",
  "chapter": 18,
  "question": "Why did persistent material state become causally inert?",
  "stage_1_accessibility_measured": "MEASURED",
  "stage_2_timed_ablation_measured": "MEASURED",
  "stage_3_accessibility_hypothesis": "SUPPORTED",
  "final_status": "SUPPORTED",
  "bounded_claim": "V2 does not add a new memory mechanism. It tests whether the v1 failure occurred because experience-written material persisted physically but lost causal access to the active growth frontier.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "information storage",
    "inheritance",
    "epigenetics",
    "signalling",
    "semantics",
    "agency",
    "individuality",
    "reproduction",
    "life"
  ],
  "next_question": "Design, but do not yet assume, the smallest local mechanism that keeps experience-written material in causal contact with the active growth surface."
}
```
