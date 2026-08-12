# Chapter 18 — Can Experience Change the Material? (V6 Exact Matched-Budget Placement)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v6",
  "schema_version": 6,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY EXACT-MATCHED-BUDGET MECHANISM TEST",
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
    "placement_policies": [
      "interior_biased",
      "random_matched",
      "surface_biased"
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
  "seed": 20260819,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "v5_issue_being_fixed": "V5 matched transmission fraction but not realized copy quantity. Surface placement created more eligible opportunities and therefore more cumulative transmissions.",
  "v6_design": "Run interior, random, and surface placement side-by-side. At every step compute one shared K from the minimum eligible count and force all branches to transmit exactly K cells. Assert equal cumulative transmission counts after every step.",
  "scientific_boundary": "Placement-only mechanism test. No claim of memory, learning, adaptation, self-maintenance, homeostasis, or life.",
  "started_at_unix": 1786539967.767887,
  "finished_at_unix": 1786539991.7443268,
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "stage_4_status": "MEASURED",
  "final_status": "FAILED",
  "next_question": "If exact-budget surface placement is supported, test whether a later experience can update, replace, or compete with the existing surface-associated state without increasing the propagation budget."
}
```

# Stage 0 — Exact Matched-Budget Audit

```json
{
  "role": "V6 EXACT MATCHED-CUMULATIVE-BUDGET AUDIT",
  "canonical_model_modified": false,
  "placement_policies": [
    "interior_biased",
    "random_matched",
    "surface_biased"
  ],
  "transmission_fraction": 0.5,
  "synthetic_eligible_counts": {
    "interior_biased": 4,
    "random_matched": 5,
    "surface_biased": 6
  },
  "shared_budget": 2,
  "selected_counts": {
    "interior_biased": 2,
    "random_matched": 2,
    "surface_biased": 2
  },
  "equal_selected_count": true,
  "all_selected_counts_equal_shared_budget": true,
  "scientific_role": "All placement policies receive exactly the same transmission count at every synchronized propagation step. The experiment isolates spatial allocation rather than realized copy quantity."
}
```


# Stage 1 — Did We Actually Hold Copy Quantity Fixed?

```json
{
  "groups": 48,
  "placement_policies": [
    "interior_biased",
    "random_matched",
    "surface_biased"
  ],
  "all_groups_exact_cumulative_budget_match": true,
  "summary": {
    "interior_biased": {
      "cumulative_transmissions": {
        "n": 48,
        "mean": 26.875,
        "median": 26.5,
        "std": 6.796521782009775,
        "ci95_low": 25.020833333333332,
        "ci95_high": 28.833854166666665,
        "min": 12.0,
        "max": 46.0
      },
      "eligible_count": {
        "n": 1056,
        "mean": 2.5,
        "median": 0.0,
        "std": 5.371431161922558,
        "ci95_low": 2.1846354166666666,
        "ci95_high": 2.832504734848485,
        "min": 0.0,
        "max": 37.0
      },
      "mean_selected_surface_exposure": {
        "n": 1056,
        "mean": 0.19231207949247722,
        "median": 0.0,
        "std": 0.4353727221667938,
        "ci95_low": 0.16569301033168218,
        "ci95_high": 0.21754646523378765,
        "min": 0.0,
        "max": 2.5
      }
    },
    "random_matched": {
      "cumulative_transmissions": {
        "n": 48,
        "mean": 26.875,
        "median": 26.5,
        "std": 6.796521782009775,
        "ci95_low": 25.1453125,
        "ci95_high": 28.896354166666665,
        "min": 12.0,
        "max": 46.0
      },
      "eligible_count": {
        "n": 1056,
        "mean": 3.4176136363636362,
        "median": 0.0,
        "std": 6.293999095034802,
        "ci95_low": 3.045407196969697,
        "ci95_high": 3.778432765151515,
        "min": 0.0,
        "max": 37.0
      },
      "mean_selected_surface_exposure": {
        "n": 1056,
        "mean": 0.4789713246034269,
        "median": 0.0,
        "std": 0.9305336456512127,
        "ci95_low": 0.4229383434195224,
        "ci95_high": 0.535916534045973,
        "min": 0.0,
        "max": 4.0
      }
    },
    "surface_biased": {
      "cumulative_transmissions": {
        "n": 48,
        "mean": 26.875,
        "median": 26.5,
        "std": 6.796521782009775,
        "ci95_low": 25.041666666666668,
        "ci95_high": 28.959374999999998,
        "min": 12.0,
        "max": 46.0
      },
      "eligible_count": {
        "n": 1056,
        "mean": 4.613636363636363,
        "median": 0.0,
        "std": 7.58589473286254,
        "ci95_low": 4.153361742424242,
        "ci95_high": 5.072277462121212,
        "min": 0.0,
        "max": 37.0
      },
      "mean_selected_surface_exposure": {
        "n": 1056,
        "mean": 0.9272099086729768,
        "median": 0.0,
        "std": 1.6655433884597395,
        "ci95_low": 0.8296940489802705,
        "ci95_high": 1.033854452904524,
        "min": 0.0,
        "max": 5.0
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "Every synchronized branch transmitted exactly the same number of cells at every step and therefore the same cumulative number of cells. Differences between policies are attributable to placement and its downstream consequences, not realized copy count."
}
```


# Stage 2 — Does Placement Alone Control Late Accessibility?

```json
{
  "groups": 48,
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
  "summary": {
    "interior_biased": {
      "4": {
        "modified_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.916666666666668,
          "ci95_high": 20.9171875,
          "min": 11.0,
          "max": 42.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.936979166666667,
          "ci95_high": 20.813020833333333,
          "min": 11.0,
          "max": 42.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 35.604166666666664,
          "median": 34.5,
          "std": 9.306672300320644,
          "ci95_low": 32.958333333333336,
          "ci95_high": 38.37552083333333,
          "min": 19.0,
          "max": 65.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.33709318092392887,
          "median": 0.33001373626373626,
          "std": 0.07657211491995308,
          "ci95_low": 0.31513828475345557,
          "ci95_high": 0.35822219046670306,
          "min": 0.15833333333333333,
          "max": 0.5652173913043478
        }
      },
      "5": {
        "modified_count": {
          "n": 48,
          "mean": 28.604166666666668,
          "median": 28.0,
          "std": 7.653266141908883,
          "ci95_low": 26.499479166666667,
          "ci95_high": 30.854166666666668,
          "min": 17.0,
          "max": 60.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 18.291666666666668,
          "median": 18.0,
          "std": 4.945361182180957,
          "ci95_low": 16.979166666666668,
          "ci95_high": 19.729166666666668,
          "min": 8.0,
          "max": 30.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 23.8125,
          "median": 22.5,
          "std": 6.827201262840677,
          "ci95_low": 21.916666666666668,
          "ci95_high": 25.666666666666668,
          "min": 9.0,
          "max": 43.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.213855395794039,
          "median": 0.20291800930898674,
          "std": 0.05744255032363956,
          "ci95_low": 0.19732511228787947,
          "ci95_high": 0.23030738457192665,
          "min": 0.08823529411764706,
          "max": 0.3739130434782609
        }
      },
      "6": {
        "modified_count": {
          "n": 48,
          "mean": 35.3125,
          "median": 35.0,
          "std": 8.756322120806962,
          "ci95_low": 32.936458333333334,
          "ci95_high": 37.854166666666664,
          "min": 23.0,
          "max": 68.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 13.8125,
          "median": 13.0,
          "std": 4.581012670069068,
          "ci95_low": 12.520312500000001,
          "ci95_high": 14.980208333333332,
          "min": 3.0,
          "max": 26.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 15.270833333333334,
          "median": 15.0,
          "std": 4.554025615382017,
          "ci95_low": 14.020833333333334,
          "ci95_high": 16.541666666666668,
          "min": 4.0,
          "max": 27.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.13137950897838904,
          "median": 0.13397459499263623,
          "std": 0.03761230460316476,
          "ci95_low": 0.12112459925224471,
          "ci95_high": 0.14216036722088915,
          "min": 0.03305785123966942,
          "max": 0.21951219512195122
        }
      },
      "7": {
        "modified_count": {
          "n": 48,
          "mean": 39.604166666666664,
          "median": 40.0,
          "std": 9.597611645902097,
          "ci95_low": 36.97864583333333,
          "ci95_high": 42.18802083333333,
          "min": 26.0,
          "max": 75.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 8.979166666666666,
          "median": 9.0,
          "std": 3.1057043171486165,
          "ci95_low": 8.145833333333334,
          "ci95_high": 9.875,
          "min": 3.0,
          "max": 16.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 9.6875,
          "median": 10.0,
          "std": 3.12354132623,
          "ci95_low": 8.791666666666666,
          "ci95_high": 10.604166666666666,
          "min": 2.0,
          "max": 17.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.07882737393711466,
          "median": 0.07752403846153846,
          "std": 0.026226495955776374,
          "ci95_low": 0.07164034561588369,
          "ci95_high": 0.0863136173485788,
          "min": 0.016,
          "max": 0.136
        }
      },
      "8": {
        "modified_count": {
          "n": 48,
          "mean": 42.520833333333336,
          "median": 43.5,
          "std": 10.386268144633194,
          "ci95_low": 39.74947916666667,
          "ci95_high": 45.521875,
          "min": 27.0,
          "max": 81.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 4.6875,
          "median": 4.0,
          "std": 2.44230296032249,
          "ci95_low": 4.020833333333333,
          "ci95_high": 5.375,
          "min": 1.0,
          "max": 13.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 4.958333333333333,
          "median": 5.0,
          "std": 2.4406141076012453,
          "ci95_low": 4.333333333333333,
          "ci95_high": 5.6875,
          "min": 1.0,
          "max": 12.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.038114220934876215,
          "median": 0.03676470588235294,
          "std": 0.01876408576559982,
          "ci95_low": 0.03323095575325884,
          "ci95_high": 0.043257742599909235,
          "min": 0.006578947368421052,
          "max": 0.08888888888888889
        }
      },
      "10": {
        "modified_count": {
          "n": 48,
          "mean": 44.708333333333336,
          "median": 45.0,
          "std": 10.984759012174802,
          "ci95_low": 41.583333333333336,
          "ci95_high": 47.626041666666666,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 1.125,
          "median": 1.0,
          "std": 1.1836560592784826,
          "ci95_low": 0.8125,
          "ci95_high": 1.4791666666666667,
          "min": 0.0,
          "max": 4.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 1.3541666666666667,
          "median": 1.0,
          "std": 1.4647181659130044,
          "ci95_low": 0.9583333333333334,
          "ci95_high": 1.7713541666666661,
          "min": 0.0,
          "max": 5.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.009467127232017,
          "median": 0.0070672260513435226,
          "std": 0.010141246390572569,
          "ci95_low": 0.006757008141352891,
          "ci95_high": 0.012387744837717264,
          "min": 0.0,
          "max": 0.03355704697986577
        }
      },
      "12": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 42.083333333333336,
          "ci95_high": 48.33385416666667,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 0.25,
          "median": 0.0,
          "std": 0.6291528696058958,
          "ci95_low": 0.08333333333333333,
          "ci95_high": 0.4375,
          "min": 0.0,
          "max": 3.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 0.2708333333333333,
          "median": 0.0,
          "std": 0.6993920971497716,
          "ci95_low": 0.08333333333333333,
          "ci95_high": 0.4791666666666667,
          "min": 0.0,
          "max": 3.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.0017700688009974087,
          "median": 0.0,
          "std": 0.004523402655460653,
          "ci95_low": 0.0006665411467892137,
          "ci95_high": 0.0031618487752476045,
          "min": 0.0,
          "max": 0.019230769230769232
        }
      },
      "14": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.915104166666666,
          "ci95_high": 48.04270833333333,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 0.041666666666666664,
          "median": 0.0,
          "std": 0.19982631347136331,
          "ci95_low": 0.0,
          "ci95_high": 0.10416666666666667,
          "min": 0.0,
          "max": 1.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 0.041666666666666664,
          "median": 0.0,
          "std": 0.19982631347136331,
          "ci95_low": 0.0,
          "ci95_high": 0.10416666666666667,
          "min": 0.0,
          "max": 1.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.0002529805710921401,
          "median": 0.0,
          "std": 0.0012143909490268548,
          "ci95_low": 0.0,
          "ci95_high": 0.0006378176822686684,
          "min": 0.0,
          "max": 0.006329113924050633
        }
      },
      "18": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.8328125,
          "ci95_high": 47.896875,
          "min": 28.0,
          "max": 86.0
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
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.9375,
          "ci95_high": 47.95885416666667,
          "min": 28.0,
          "max": 86.0
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
    "random_matched": {
      "4": {
        "modified_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.875,
          "ci95_high": 20.9171875,
          "min": 11.0,
          "max": 42.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.895833333333332,
          "ci95_high": 20.958333333333332,
          "min": 11.0,
          "max": 42.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 35.604166666666664,
          "median": 34.5,
          "std": 9.306672300320644,
          "ci95_low": 33.06197916666667,
          "ci95_high": 38.10572916666666,
          "min": 19.0,
          "max": 65.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.33709318092392887,
          "median": 0.33001373626373626,
          "std": 0.07657211491995308,
          "ci95_low": 0.31434722606527893,
          "ci95_high": 0.3581028912850297,
          "min": 0.15833333333333333,
          "max": 0.5652173913043478
        }
      },
      "5": {
        "modified_count": {
          "n": 48,
          "mean": 28.604166666666668,
          "median": 28.0,
          "std": 7.653266141908883,
          "ci95_low": 26.625,
          "ci95_high": 30.9375,
          "min": 17.0,
          "max": 60.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 19.375,
          "median": 19.0,
          "std": 4.948168853222372,
          "ci95_low": 17.979166666666668,
          "ci95_high": 20.750520833333333,
          "min": 9.0,
          "max": 32.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 29.6875,
          "median": 27.5,
          "std": 8.337056459966352,
          "ci95_low": 27.458333333333332,
          "ci95_high": 32.18802083333333,
          "min": 12.0,
          "max": 56.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.2665289801667459,
          "median": 0.2626690635165212,
          "std": 0.06951086445309314,
          "ci95_low": 0.24693007605486458,
          "ci95_high": 0.28529424778759727,
          "min": 0.09836065573770492,
          "max": 0.48695652173913045
        }
      },
      "6": {
        "modified_count": {
          "n": 48,
          "mean": 35.3125,
          "median": 35.0,
          "std": 8.756322120806962,
          "ci95_low": 32.93697916666667,
          "ci95_high": 37.958333333333336,
          "min": 23.0,
          "max": 68.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 16.75,
          "median": 16.0,
          "std": 4.8584119490494695,
          "ci95_low": 15.458333333333334,
          "ci95_high": 18.229166666666668,
          "min": 6.0,
          "max": 30.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 23.708333333333332,
          "median": 23.0,
          "std": 7.117930215698632,
          "ci95_low": 21.895833333333332,
          "ci95_high": 25.6671875,
          "min": 8.0,
          "max": 42.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.2033212113290123,
          "median": 0.19484323432343237,
          "std": 0.057603100844522755,
          "ci95_low": 0.1877939696097547,
          "ci95_high": 0.21804740436703884,
          "min": 0.06611570247933884,
          "max": 0.34710743801652894
        }
      },
      "7": {
        "modified_count": {
          "n": 48,
          "mean": 39.604166666666664,
          "median": 40.0,
          "std": 9.597611645902097,
          "ci95_low": 37.04114583333333,
          "ci95_high": 42.3125,
          "min": 26.0,
          "max": 75.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 13.25,
          "median": 12.5,
          "std": 4.018187817080398,
          "ci95_low": 12.104166666666666,
          "ci95_high": 14.375520833333333,
          "min": 6.0,
          "max": 25.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 17.541666666666668,
          "median": 16.5,
          "std": 5.6234565783767625,
          "ci95_low": 16.041666666666668,
          "ci95_high": 19.146354166666665,
          "min": 8.0,
          "max": 34.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.14240733310486434,
          "median": 0.13579661016949152,
          "std": 0.04562773083158848,
          "ci95_low": 0.13055696580314274,
          "ci95_high": 0.15432445971956257,
          "min": 0.06201550387596899,
          "max": 0.265625
        }
      },
      "8": {
        "modified_count": {
          "n": 48,
          "mean": 42.520833333333336,
          "median": 43.5,
          "std": 10.386268144633194,
          "ci95_low": 39.64479166666667,
          "ci95_high": 45.52135416666667,
          "min": 27.0,
          "max": 81.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 8.333333333333334,
          "median": 8.0,
          "std": 3.124722209875446,
          "ci95_low": 7.478645833333333,
          "ci95_high": 9.313020833333333,
          "min": 3.0,
          "max": 19.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 11.520833333333334,
          "median": 11.0,
          "std": 4.382681748148679,
          "ci95_low": 10.270833333333334,
          "ci95_high": 12.791666666666666,
          "min": 4.0,
          "max": 24.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.08926721116264602,
          "median": 0.08922056384742952,
          "std": 0.03476673195157632,
          "ci95_low": 0.07977260780729889,
          "ci95_high": 0.09969545378611384,
          "min": 0.029197080291970802,
          "max": 0.18604651162790697
        }
      },
      "10": {
        "modified_count": {
          "n": 48,
          "mean": 44.708333333333336,
          "median": 45.0,
          "std": 10.984759012174802,
          "ci95_low": 41.5828125,
          "ci95_high": 47.8546875,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 2.75,
          "median": 2.0,
          "std": 1.8427786989579984,
          "ci95_low": 2.25,
          "ci95_high": 3.2708333333333335,
          "min": 0.0,
          "max": 8.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 3.3958333333333335,
          "median": 3.0,
          "std": 2.2522172716878113,
          "ci95_low": 2.7708333333333335,
          "ci95_high": 4.083333333333333,
          "min": 0.0,
          "max": 9.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.024017205762723506,
          "median": 0.0207674619143432,
          "std": 0.016288499971760233,
          "ci95_low": 0.019564286041041698,
          "ci95_high": 0.028920693510217477,
          "min": 0.0,
          "max": 0.06428571428571428
        }
      },
      "12": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.852604166666666,
          "ci95_high": 48.1671875,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 0.5625,
          "median": 0.0,
          "std": 0.733321496116585,
          "ci95_low": 0.375,
          "ci95_high": 0.7916666666666666,
          "min": 0.0,
          "max": 2.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 0.6666666666666666,
          "median": 0.0,
          "std": 0.9860132971832694,
          "ci95_low": 0.3958333333333333,
          "ci95_high": 0.9583333333333334,
          "min": 0.0,
          "max": 4.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.004266858131877383,
          "median": 0.0,
          "std": 0.006372113131130698,
          "ci95_low": 0.002543167386334204,
          "ci95_high": 0.006240041339921846,
          "min": 0.0,
          "max": 0.02702702702702703
        }
      },
      "14": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.977604166666666,
          "ci95_high": 48.063541666666666,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.00011973180076628352,
          "median": 0.0,
          "std": 0.000820839870737673,
          "ci95_low": 0.0,
          "ci95_high": 0.00035919540229885057,
          "min": 0.0,
          "max": 0.005747126436781609
        }
      },
      "18": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.87447916666667,
          "ci95_high": 48.188541666666666,
          "min": 28.0,
          "max": 86.0
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
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.93541666666667,
          "ci95_high": 48.229166666666664,
          "min": 28.0,
          "max": 86.0
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
    "surface_biased": {
      "4": {
        "modified_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.8953125,
          "ci95_high": 21.0421875,
          "min": 11.0,
          "max": 42.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 19.333333333333332,
          "median": 18.0,
          "std": 5.3709610147740054,
          "ci95_low": 17.916666666666668,
          "ci95_high": 20.854166666666668,
          "min": 11.0,
          "max": 42.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 35.604166666666664,
          "median": 34.5,
          "std": 9.306672300320644,
          "ci95_low": 33.0203125,
          "ci95_high": 38.33385416666667,
          "min": 19.0,
          "max": 65.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.33709318092392887,
          "median": 0.33001373626373626,
          "std": 0.07657211491995308,
          "ci95_low": 0.31542524144460155,
          "ci95_high": 0.3601804588530494,
          "min": 0.15833333333333333,
          "max": 0.5652173913043478
        }
      },
      "5": {
        "modified_count": {
          "n": 48,
          "mean": 28.604166666666668,
          "median": 28.0,
          "std": 7.653266141908883,
          "ci95_low": 26.458333333333332,
          "ci95_high": 30.897916666666664,
          "min": 17.0,
          "max": 60.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 20.979166666666668,
          "median": 20.5,
          "std": 5.301295373669429,
          "ci95_low": 19.4578125,
          "ci95_high": 22.604166666666668,
          "min": 11.0,
          "max": 38.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 37.1875,
          "median": 35.5,
          "std": 9.799354251684138,
          "ci95_low": 34.333333333333336,
          "ci95_high": 39.979166666666664,
          "min": 16.0,
          "max": 67.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.3334869483078102,
          "median": 0.32825995365494,
          "std": 0.07957645914859092,
          "ci95_low": 0.31062428056432356,
          "ci95_high": 0.3568902357034926,
          "min": 0.13114754098360656,
          "max": 0.5826086956521739
        }
      },
      "6": {
        "modified_count": {
          "n": 48,
          "mean": 35.3125,
          "median": 35.0,
          "std": 8.756322120806962,
          "ci95_low": 33.041666666666664,
          "ci95_high": 37.813541666666666,
          "min": 23.0,
          "max": 68.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 20.208333333333332,
          "median": 20.0,
          "std": 5.346175943814627,
          "ci95_low": 18.708333333333332,
          "ci95_high": 21.75,
          "min": 8.0,
          "max": 36.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 34.479166666666664,
          "median": 32.0,
          "std": 8.784431264395486,
          "ci95_low": 32.03958333333333,
          "ci95_high": 36.8765625,
          "min": 14.0,
          "max": 57.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.29503681638587076,
          "median": 0.2916666666666667,
          "std": 0.07018194173046592,
          "ci95_low": 0.2753603576223416,
          "ci95_high": 0.31486268798671646,
          "min": 0.11570247933884298,
          "max": 0.475
        }
      },
      "7": {
        "modified_count": {
          "n": 48,
          "mean": 39.604166666666664,
          "median": 40.0,
          "std": 9.597611645902097,
          "ci95_low": 36.790104166666666,
          "ci95_high": 42.3546875,
          "min": 26.0,
          "max": 75.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 16.791666666666668,
          "median": 15.0,
          "std": 4.825964209933136,
          "ci95_low": 15.520312500000001,
          "ci95_high": 18.188020833333333,
          "min": 7.0,
          "max": 31.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 28.145833333333332,
          "median": 25.0,
          "std": 8.19804240691371,
          "ci95_low": 25.8125,
          "ci95_high": 30.438020833333333,
          "min": 10.0,
          "max": 48.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.2269831169183556,
          "median": 0.2162375790424571,
          "std": 0.06524649612233126,
          "ci95_low": 0.20866501891969932,
          "ci95_high": 0.2452887891398468,
          "min": 0.07751937984496124,
          "max": 0.375
        }
      },
      "8": {
        "modified_count": {
          "n": 48,
          "mean": 42.520833333333336,
          "median": 43.5,
          "std": 10.386268144633194,
          "ci95_low": 39.770833333333336,
          "ci95_high": 45.396875,
          "min": 27.0,
          "max": 81.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 12.270833333333334,
          "median": 12.0,
          "std": 3.5808494297985907,
          "ci95_low": 11.291666666666666,
          "ci95_high": 13.208333333333334,
          "min": 5.0,
          "max": 20.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 20.895833333333332,
          "median": 20.5,
          "std": 6.807592523956044,
          "ci95_low": 19.041666666666668,
          "ci95_high": 23.042708333333334,
          "min": 7.0,
          "max": 41.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.1611205947636191,
          "median": 0.15873015873015872,
          "std": 0.054827927040643036,
          "ci95_low": 0.14745298926994702,
          "ci95_high": 0.17760342928846398,
          "min": 0.051094890510948905,
          "max": 0.31297709923664124
        }
      },
      "10": {
        "modified_count": {
          "n": 48,
          "mean": 44.708333333333336,
          "median": 45.0,
          "std": 10.984759012174802,
          "ci95_low": 41.75,
          "ci95_high": 47.959375,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 5.291666666666667,
          "median": 5.0,
          "std": 3.0479387388127663,
          "ci95_low": 4.479166666666667,
          "ci95_high": 6.145833333333333,
          "min": 1.0,
          "max": 15.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 7.895833333333333,
          "median": 7.0,
          "std": 5.296380774222673,
          "ci95_low": 6.499479166666667,
          "ci95_high": 9.479687499999999,
          "min": 1.0,
          "max": 27.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.05522659435879895,
          "median": 0.04836284664216505,
          "std": 0.03673890610934178,
          "ci95_low": 0.04586851683042829,
          "ci95_high": 0.06747625889506953,
          "min": 0.006622516556291391,
          "max": 0.1888111888111888
        }
      },
      "12": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.87447916666667,
          "ci95_high": 47.916666666666664,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 1.1666666666666667,
          "median": 1.0,
          "std": 1.2638125740085917,
          "ci95_low": 0.8328125000000001,
          "ci95_high": 1.5421874999999996,
          "min": 0.0,
          "max": 6.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 1.4791666666666667,
          "median": 1.0,
          "std": 1.6581815257149086,
          "ci95_low": 1.0208333333333333,
          "ci95_high": 2.0208333333333335,
          "min": 0.0,
          "max": 7.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.00942030518360517,
          "median": 0.006432530818234467,
          "std": 0.010473781961203509,
          "ci95_low": 0.006460890885174256,
          "ci95_high": 0.012569961908194108,
          "min": 0.0,
          "max": 0.04516129032258064
        }
      },
      "14": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.99947916666667,
          "ci95_high": 48.3546875,
          "min": 28.0,
          "max": 86.0
        },
        "modified_boundary_count": {
          "n": 48,
          "mean": 0.10416666666666667,
          "median": 0.0,
          "std": 0.3673998351780916,
          "ci95_low": 0.020833333333333332,
          "ci95_high": 0.22916666666666666,
          "min": 0.0,
          "max": 2.0
        },
        "frontier_cells_with_modified_neighbor": {
          "n": 48,
          "mean": 0.10416666666666667,
          "median": 0.0,
          "std": 0.3673998351780916,
          "ci95_low": 0.020833333333333332,
          "ci95_high": 0.22916666666666666,
          "min": 0.0,
          "max": 2.0
        },
        "frontier_exposed_fraction": {
          "n": 48,
          "mean": 0.0006029866412603603,
          "median": 0.0,
          "std": 0.002134688108276446,
          "ci95_low": 0.00011446886446886448,
          "ci95_high": 0.0012303074085832997,
          "min": 0.0,
          "max": 0.011695906432748537
        }
      },
      "18": {
        "modified_count": {
          "n": 48,
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 41.99947916666667,
          "ci95_high": 48.25052083333333,
          "min": 28.0,
          "max": 86.0
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
          "mean": 44.916666666666664,
          "median": 45.0,
          "std": 10.944620697960355,
          "ci95_low": 42.06197916666667,
          "ci95_high": 47.85520833333333,
          "min": 28.0,
          "max": 86.0
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
    }
  },
  "late_step_frontier_contact": {
    "interior_biased": 0.041666666666666664,
    "random_matched": 0.020833333333333332,
    "surface_biased": 0.10416666666666667
  },
  "interior_less_than_random_less_than_surface": false,
  "status": "MEASURED",
  "bounded_statement": "V6 measures whether equal quantities of propagated state remain differentially accessible depending only on spatial placement."
}
```


# Stage 3 — Does Placement Alone Change Realized Causal Work?

```json
{
  "groups": 48,
  "audit_steps": [
    8,
    10,
    12,
    14,
    18
  ],
  "summary": {
    "interior_biased": {
      "8": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 4.875,
          "median": 5.0,
          "std": 3.1465920718559413,
          "ci95_low": 4.041666666666667,
          "ci95_high": 5.791666666666667,
          "min": 1.0,
          "max": 14.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.29438276192896673,
          "median": 0.2692569132157734,
          "std": 0.2197599995402573,
          "ci95_low": 0.2344824045820466,
          "ci95_high": 0.3597147753978329,
          "min": 0.05490780934852246,
          "max": 0.9818832794161163
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.05900483979273244,
          "median": 0.05832330311651293,
          "std": 0.012597137704667086,
          "ci95_low": 0.05565646903051897,
          "ci95_high": 0.06252036203839977,
          "min": 0.028784646462895535,
          "max": 0.08572552350121819
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.375,
          "median": 0.0,
          "std": 0.5636562191028618,
          "ci95_low": 0.22916666666666666,
          "ci95_high": 0.5416666666666666,
          "min": 0.0,
          "max": 2.0
        }
      },
      "10": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 1.2291666666666667,
          "median": 1.0,
          "std": 1.6487316252872153,
          "ci95_low": 0.8119791666666667,
          "ci95_high": 1.7083333333333333,
          "min": 0.0,
          "max": 7.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.06908161009213028,
          "median": 0.016413031460668026,
          "std": 0.10339582804742078,
          "ci95_low": 0.04141411268235985,
          "ci95_high": 0.10166394890171009,
          "min": 0.0,
          "max": 0.45202749088179206
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.027953691385588383,
          "median": 0.016413031460668026,
          "std": 0.031018651254274148,
          "ci95_low": 0.019412881966592566,
          "ci95_high": 0.03709542623361344,
          "min": 0.0,
          "max": 0.10293107498034151
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.08333333333333333,
          "median": 0.0,
          "std": 0.2763853991962833,
          "ci95_low": 0.020833333333333332,
          "ci95_high": 0.16666666666666666,
          "min": 0.0,
          "max": 1.0
        }
      },
      "12": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.20833333333333334,
          "median": 0.0,
          "std": 0.6441510347391795,
          "ci95_low": 0.0625,
          "ci95_high": 0.4166666666666667,
          "min": 0.0,
          "max": 4.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.009190591181265322,
          "median": 0.0,
          "std": 0.02834162030307465,
          "ci95_low": 0.0026227616629394125,
          "ci95_high": 0.01792020795132088,
          "min": 0.0,
          "max": 0.15733277263859463
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.006732266608787281,
          "median": 0.0,
          "std": 0.01894524261341262,
          "ci95_low": 0.0019466447691466593,
          "ci95_high": 0.012857718878018268,
          "min": 0.0,
          "max": 0.07470693888466945
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        }
      },
      "14": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.0015434750994018573,
          "median": 0.0,
          "std": 0.010581532165818799,
          "ci95_low": 0.0,
          "ci95_high": 0.004630425298205572,
          "min": 0.0,
          "max": 0.07408680477128915
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.0015434750994018573,
          "median": 0.0,
          "std": 0.010581532165818799,
          "ci95_low": 0.0,
          "ci95_high": 0.004630425298205572,
          "min": 0.0,
          "max": 0.07408680477128915
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
        }
      }
    },
    "random_matched": {
      "8": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 11.979166666666666,
          "median": 11.0,
          "std": 5.149796045044459,
          "ci95_low": 10.457812500000001,
          "ci95_high": 13.458854166666667,
          "min": 3.0,
          "max": 27.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.8452952327408175,
          "median": 0.742685671879072,
          "std": 0.4046553758670278,
          "ci95_low": 0.7344547664753063,
          "ci95_high": 0.9567097152155104,
          "min": 0.16818373425367616,
          "max": 1.9142926554643411
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.06915410508036231,
          "median": 0.0691123375533016,
          "std": 0.009960179877854249,
          "ci95_low": 0.06627186741345423,
          "ci95_high": 0.07197160268369569,
          "min": 0.04204593356341904,
          "max": 0.08759202865188245
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.8125,
          "median": 1.0,
          "std": 0.9049919428738946,
          "ci95_low": 0.5625,
          "ci95_high": 1.0833333333333333,
          "min": 0.0,
          "max": 4.0
        }
      },
      "10": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 3.8333333333333335,
          "median": 3.5,
          "std": 2.860167050288419,
          "ci95_low": 3.0416666666666665,
          "ci95_high": 4.645833333333333,
          "min": 0.0,
          "max": 12.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.2332955868602721,
          "median": 0.18572117971483254,
          "std": 0.20466981758306724,
          "ci95_low": 0.17823433862958904,
          "ci95_high": 0.29576358941110736,
          "min": 0.0,
          "max": 0.8470926769575122
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.04987200009007433,
          "median": 0.05681653483732692,
          "std": 0.022146036921885288,
          "ci95_low": 0.04338241119255778,
          "ci95_high": 0.056364966655588336,
          "min": 0.0,
          "max": 0.08155268928972015
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.20833333333333334,
          "median": 0.0,
          "std": 0.45452967144315476,
          "ci95_low": 0.08333333333333333,
          "ci95_high": 0.3333333333333333,
          "min": 0.0,
          "max": 2.0
        }
      },
      "12": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.6041666666666666,
          "median": 0.0,
          "std": 1.2372614809417701,
          "ci95_low": 0.2916666666666667,
          "ci95_high": 1.0208333333333333,
          "min": 0.0,
          "max": 7.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.0359489176674088,
          "median": 0.0,
          "std": 0.08658490123962641,
          "ci95_low": 0.014179617370634053,
          "ci95_high": 0.06186855262061479,
          "min": 0.0,
          "max": 0.48823538019079565
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.016400367017825646,
          "median": 0.0,
          "std": 0.027923631849474616,
          "ci95_low": 0.008975386326590866,
          "ci95_high": 0.024781415779306083,
          "min": 0.0,
          "max": 0.0922554466887595
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        }
      },
      "14": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.08333333333333333,
          "median": 0.0,
          "std": 0.3996526269427267,
          "ci95_low": 0.0,
          "ci95_high": 0.20833333333333334,
          "min": 0.0,
          "max": 2.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.005410078764505642,
          "median": 0.0,
          "std": 0.026214272165563275,
          "ci95_low": 0.0,
          "ci95_high": 0.013907107727815,
          "min": 0.0,
          "max": 0.1481736095425783
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.002705039382252821,
          "median": 0.0,
          "std": 0.013107136082781638,
          "ci95_low": 0.0,
          "ci95_high": 0.006571643047356607,
          "min": 0.0,
          "max": 0.07408680477128915
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
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
        }
      }
    },
    "surface_biased": {
      "8": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 20.333333333333332,
          "median": 20.0,
          "std": 7.439571373555214,
          "ci95_low": 18.311979166666667,
          "ci95_high": 22.416666666666668,
          "min": 4.0,
          "max": 39.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 1.6266460254391315,
          "median": 1.5276921913673673,
          "std": 0.6245433599448238,
          "ci95_low": 1.4594016177691682,
          "ci95_high": 1.8061851325168712,
          "min": 0.3082222557893476,
          "max": 3.125342326332454
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.07968964629879995,
          "median": 0.07934664893375865,
          "std": 0.006607867975338863,
          "ci95_low": 0.07765362663218198,
          "ci95_high": 0.08152836731016018,
          "min": 0.0654985016164867,
          "max": 0.09705608170475864
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 1.9166666666666667,
          "median": 2.0,
          "std": 1.5388487760516156,
          "ci95_low": 1.5,
          "ci95_high": 2.375,
          "min": 0.0,
          "max": 7.0
        }
      },
      "10": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 7.5625,
          "median": 7.0,
          "std": 4.348880363572522,
          "ci95_low": 6.395833333333333,
          "ci95_high": 8.854166666666666,
          "min": 1.0,
          "max": 19.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.5288777120976347,
          "median": 0.4665509996149906,
          "std": 0.32931399382848764,
          "ci95_low": 0.44143453970252117,
          "ci95_high": 0.6267109927027685,
          "min": 0.0851883016711047,
          "max": 1.3430767169228273
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.06933930832012415,
          "median": 0.06864450111087045,
          "std": 0.016816126206534263,
          "ci95_low": 0.06509691828530945,
          "ci95_high": 0.07435652345368389,
          "min": 0.04259415083555235,
          "max": 0.14852743484234116
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.75,
          "median": 1.0,
          "std": 0.82915619758885,
          "ci95_low": 0.5208333333333334,
          "ci95_high": 1.0,
          "min": 0.0,
          "max": 3.0
        }
      },
      "12": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 1.4375,
          "median": 1.0,
          "std": 1.9029171684547912,
          "ci95_low": 0.9578125000000001,
          "ci95_high": 2.0,
          "min": 0.0,
          "max": 10.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.08713900430680273,
          "median": 0.05552173406020472,
          "std": 0.12925857631437598,
          "ci95_low": 0.05471406760896025,
          "ci95_high": 0.12713034538583526,
          "min": 0.0,
          "max": 0.6458008489345101
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.037166523050541515,
          "median": 0.039961928356223336,
          "std": 0.03406102290792828,
          "ci95_low": 0.02784291934260882,
          "ci95_high": 0.046515565452143214,
          "min": 0.0,
          "max": 0.14887694666032025
        },
        "realized_causal_flips": {
          "n": 48,
          "mean": 0.08333333333333333,
          "median": 0.0,
          "std": 0.2763853991962833,
          "ci95_low": 0.020833333333333332,
          "ci95_high": 0.16666666666666666,
          "min": 0.0,
          "max": 1.0
        }
      },
      "14": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.14583333333333334,
          "median": 0.0,
          "std": 0.6120179508986825,
          "ci95_low": 0.020833333333333332,
          "ci95_high": 0.3333333333333333,
          "min": 0.0,
          "max": 4.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.0082239104042093,
          "median": 0.0,
          "std": 0.03674998060935927,
          "ci95_low": 0.0005308356951839593,
          "ci95_high": 0.020418803428747384,
          "min": 0.0,
          "max": 0.24333438412769595
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.004421810652214053,
          "median": 0.0,
          "std": 0.015561631204694571,
          "ci95_low": 0.0005308356951839593,
          "ci95_high": 0.0088091840553959,
          "min": 0.0,
          "max": 0.07485897150715182
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
        }
      },
      "18": {
        "exposed_frontier_count": {
          "n": 48,
          "mean": 0.020833333333333332,
          "median": 0.0,
          "std": 0.1428261375083551,
          "ci95_low": 0.0,
          "ci95_high": 0.0625,
          "min": 0.0,
          "max": 1.0
        },
        "sum_delta_p": {
          "n": 48,
          "mean": 0.0005318110298418629,
          "median": 0.0,
          "std": 0.0036459127332793845,
          "ci95_low": 0.0,
          "ci95_high": 0.0015954330895255886,
          "min": 0.0,
          "max": 0.025526929432409418
        },
        "mean_delta_p_exposed": {
          "n": 48,
          "mean": 0.0005318110298418629,
          "median": 0.0,
          "std": 0.0036459127332793845,
          "ci95_low": 0.0,
          "ci95_high": 0.0015954330895255886,
          "min": 0.0,
          "max": 0.025526929432409418
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
        }
      }
    }
  },
  "late_step_realized_flips": {
    "interior_biased": 0.0,
    "random_matched": 0.020833333333333332,
    "surface_biased": 0.0
  },
  "late_step_sum_delta_p": {
    "interior_biased": 0.0015434750994018573,
    "random_matched": 0.005410078764505642,
    "surface_biased": 0.0082239104042093
  },
  "interior_less_than_random_less_than_surface_flips": false,
  "status": "MEASURED",
  "bounded_statement": "Under identical cumulative transmission counts, V6 tests whether placement alone changes the amount of local causal work performed at the active frontier."
}
```


# Stage 4 — Late Ablation Under Exact Matched Copy Quantity

```json
{
  "late_ablation_step": 14,
  "followup_steps": 4,
  "results": {
    "interior_biased": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference": {
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
    "random_matched": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.08333333333333333,
        "median": 0.0,
        "std": 0.44876373392787533,
        "ci95_low": 0.0,
        "ci95_high": 0.25,
        "min": 0.0,
        "max": 3.0
      },
      "pathwise_symmetric_difference": {
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
    "surface_biased": {
      "frontier_contact": {
        "n": 48,
        "mean": 0.3541666666666667,
        "median": 0.0,
        "std": 0.7770023416238131,
        "ci95_low": 0.14583333333333334,
        "ci95_high": 0.5833333333333334,
        "min": 0.0,
        "max": 4.0
      },
      "pathwise_symmetric_difference": {
        "n": 48,
        "mean": 1.71609006040637e-05,
        "median": 0.0,
        "std": 0.00011764920717327438,
        "ci95_low": 0.0,
        "ci95_high": 5.148270181219111e-05,
        "min": 0.0,
        "max": 0.0008237232289950577
      },
      "paired_ridge_test": {
        "statistic": 0.021057249396797456,
        "p_value": 1.0,
        "permutations": 2000,
        "null_mean": 0.021057249396797498,
        "null_q95": 0.02105724939679755,
        "null_q99": 0.02105724939679755
      }
    }
  },
  "interior_less_than_random_less_than_surface_symdiff": false,
  "status": "MEASURED",
  "interpretation": "This is a downstream corroboration of the exact matched-budget placement experiment."
}
```


# Stage 5 — Bounded Chapter 18 V6 Verdict

```json
{
  "experiment_role": "EXPLORATORY EXACT-MATCHED-BUDGET MECHANISM TEST",
  "chapter": 18,
  "question": "Does the spatial placement of persistent material determine whether it remains causally active when the exact amount copied is held fixed?",
  "budget_invariant_valid": true,
  "predicted_order": "interior_biased < random_matched < surface_biased",
  "frontier_access_order_supported": false,
  "realized_causal_flip_order_supported": false,
  "late_ablation_order_supported": false,
  "status": "FAILED",
  "bounded_claim": "Under an exact matched cumulative copying budget, V6 did not establish the predicted interior < random < surface ordering.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "self-maintenance",
    "homeostasis",
    "attention",
    "active boundary",
    "information storage",
    "biological inheritance",
    "agency",
    "individuality",
    "reproduction",
    "life"
  ],
  "next_question": "If exact-budget surface placement is supported, test whether a later experience can update, replace, or compete with the existing surface-associated state without increasing the propagation budget."
}
```
