# Chapter 18 — Can Experience Change the Material? (V7 Integrated Causal Lifetime)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v7",
  "schema_version": 7,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY INTEGRATED CAUSAL-LIFETIME TEST",
  "profile": "quick",
  "profile_config": {
    "groups": 64,
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
    "window_start": 5,
    "window_end": 18,
    "sustained_zero_steps": 3,
    "descriptive_steps": [
      5,
      8,
      10,
      12,
      14,
      18
    ],
    "bootstrap_reps": 1500,
    "permutations": 2000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260820,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "v6_result_being_followed": "The exact matched-copy-quantity late t=14 endpoint failed, while an earlier exploratory t=8 pattern showed interior < random < surface for frontier access, probability leverage, and realized causal flips.",
  "v7_design": "Keep exact matched per-step and cumulative transmission counts, but replace a single late endpoint with predeclared integrated causal-lifetime measures over a frozen observation window.",
  "scientific_boundary": "Causal lifetime only. No claim of memory, learning, adaptation, self-maintenance, homeostasis, active boundary, or life.",
  "started_at_unix": 1786541522.9206185,
  "finished_at_unix": 1786541537.4539392,
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "SUPPORTED",
  "next_question": "If causal lifetime is supported, restore the opportunity feedback observed in v5 and test whether causal accessibility helps generate future opportunities for its own continuation, while keeping the claim below self-maintenance."
}
```

# Stage 0 — V7 Validity Gate

```json
{
  "role": "V7 EXACT MATCHED-BUDGET VALIDITY GATE",
  "canonical_model_modified": false,
  "placement_policies": [
    "interior_biased",
    "random_matched",
    "surface_biased"
  ],
  "transmission_fraction": 0.5,
  "shared_budget": 2,
  "selected_counts": {
    "interior_biased": 2,
    "random_matched": 2,
    "surface_biased": 2
  },
  "budget_unit_check_pass": true,
  "window_start": 5,
  "window_end": 18,
  "sustained_zero_steps": 3,
  "scientific_role": "V7 preserves the exact matched-copy-quantity control from v6 and changes only the outcome definition from a single late endpoint to predeclared integrated causal-lifetime measures."
}
```


# Stage 1 — Exact Copy-Quantity Integrity

```json
{
  "groups": 64,
  "all_groups_exact_cumulative_budget_match": true,
  "final_cumulative_transmissions": {
    "interior_biased": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.640625,
      "ci95_high": 28.805078124999998,
      "min": 13.0,
      "max": 46.0
    },
    "random_matched": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.5625,
      "ci95_high": 28.726953124999998,
      "min": 13.0,
      "max": 46.0
    },
    "surface_biased": {
      "n": 64,
      "mean": 27.1875,
      "median": 27.0,
      "std": 6.44901882071994,
      "ci95_low": 25.632421875,
      "ci95_high": 28.71875,
      "min": 13.0,
      "max": 46.0
    }
  },
  "status": "MEASURED",
  "bounded_statement": "Every branch copied exactly the same number of cells in every paired group through the full V7 observation window."
}
```


# Stage 2 — Does Placement Change Causal Lifetime?

```json
{
  "groups": 64,
  "window_start": 5,
  "window_end": 18,
  "sustained_zero_steps": 3,
  "summary": {
    "interior_biased": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 0.5153345498093818,
        "median": 0.5140525903182478,
        "std": 0.1644243737537399,
        "ci95_low": 0.4732249139839143,
        "ci95_high": 0.556814877227906,
        "min": 0.15630426330247907,
        "max": 0.8982471254348687
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 59.71875,
        "median": 58.0,
        "std": 19.596291701173975,
        "ci95_low": 55.015625,
        "ci95_high": 64.81328124999999,
        "min": 18.0,
        "max": 110.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 3.872219810237442,
        "median": 3.7139068446426906,
        "std": 1.3787061492406727,
        "ci95_low": 3.530967797187591,
        "ci95_high": 4.21129837331458,
        "min": 1.2399154985732,
        "max": 7.590361228102362
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 4.0625,
        "median": 4.0,
        "std": 2.8716012519150356,
        "ci95_low": 3.359375,
        "ci95_high": 4.796875,
        "min": 0.0,
        "max": 16.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 10.96875,
        "median": 11.0,
        "std": 1.357487914310842,
        "ci95_low": 10.640625,
        "ci95_high": 11.28125,
        "min": 8.0,
        "max": 14.0
      }
    },
    "random_matched": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 0.8471062884768128,
        "median": 0.8279617336700826,
        "std": 0.2563702930752315,
        "ci95_low": 0.7849830767562997,
        "ci95_high": 0.9111845449520846,
        "min": 0.3636780435872759,
        "max": 1.4237040939623467
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 100.28125,
        "median": 95.5,
        "std": 31.31167351703674,
        "ci95_low": 92.81171875,
        "ci95_high": 107.946484375,
        "min": 39.0,
        "max": 172.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 7.3322945605823096,
        "median": 7.1357407270495035,
        "std": 2.466239046268343,
        "ci95_low": 6.729675431136326,
        "ci95_high": 7.921675111026543,
        "min": 2.7622678109669097,
        "max": 14.173749871982151
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 7.515625,
        "median": 7.5,
        "std": 3.8283163217496803,
        "ci95_low": 6.640625,
        "ci95_high": 8.421875,
        "min": 0.0,
        "max": 19.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 12.171875,
        "median": 12.0,
        "std": 1.6541112370016111,
        "ci95_low": 11.796875,
        "ci95_high": 12.578125,
        "min": 10.0,
        "max": 19.0
      }
    },
    "surface_biased": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 1.2931645001216052,
        "median": 1.234182641387322,
        "std": 0.3660271772184895,
        "ci95_low": 1.2040533077898024,
        "ci95_high": 1.379134278748768,
        "min": 0.5724953999644466,
        "max": 2.1798977145260765
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 156.234375,
        "median": 157.0,
        "std": 47.411016054914654,
        "ci95_low": 145.084765625,
        "ci95_high": 168.875,
        "min": 68.0,
        "max": 281.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 12.25885816874764,
        "median": 11.79865480464414,
        "std": 3.8340048270034783,
        "ci95_low": 11.321373653849667,
        "ci95_high": 13.140764795338663,
        "min": 5.0819671286557675,
        "max": 22.590666442976183
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 12.390625,
        "median": 12.0,
        "std": 4.615250492592466,
        "ci95_low": 11.241796875,
        "ci95_high": 13.46875,
        "min": 2.0,
        "max": 23.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 13.421875,
        "median": 13.0,
        "std": 1.9023397394721586,
        "ci95_low": 12.984375,
        "ci95_high": 13.9375,
        "min": 10.0,
        "max": 19.0
      }
    }
  },
  "trajectory_summary": {
    "interior_biased": {
      "5": {
        "frontier_exposed_fraction": 0.22798813136351134,
        "frontier_contact": 24.796875,
        "sum_delta_p": 1.7030227420836277,
        "realized_flips": 1.640625
      },
      "6": {
        "frontier_exposed_fraction": 0.13820698163491407,
        "frontier_contact": 15.9375,
        "sum_delta_p": 1.0295220016666118,
        "realized_flips": 1.296875
      },
      "7": {
        "frontier_exposed_fraction": 0.07450644758303752,
        "frontier_contact": 9.03125,
        "sum_delta_p": 0.5590158124887622,
        "realized_flips": 0.546875
      },
      "8": {
        "frontier_exposed_fraction": 0.038564565782429165,
        "frontier_contact": 4.9375,
        "sum_delta_p": 0.2989695113236634,
        "realized_flips": 0.28125
      },
      "9": {
        "frontier_exposed_fraction": 0.020021712648436524,
        "frontier_contact": 2.703125,
        "sum_delta_p": 0.15705567638795725,
        "realized_flips": 0.203125
      },
      "10": {
        "frontier_exposed_fraction": 0.010111785682028078,
        "frontier_contact": 1.421875,
        "sum_delta_p": 0.07999204039502225,
        "realized_flips": 0.03125
      },
      "11": {
        "frontier_exposed_fraction": 0.004554908266542887,
        "frontier_contact": 0.671875,
        "sum_delta_p": 0.0334403943234194,
        "realized_flips": 0.015625
      },
      "12": {
        "frontier_exposed_fraction": 0.00119256174790751,
        "frontier_contact": 0.1875,
        "sum_delta_p": 0.009893873675041647,
        "realized_flips": 0.046875
      },
      "13": {
        "frontier_exposed_fraction": 0.00018745510057471265,
        "frontier_contact": 0.03125,
        "sum_delta_p": 0.001307757893336793,
        "realized_flips": 0.0
      },
      "14": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "15": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "16": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "17": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "18": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      }
    },
    "random_matched": {
      "5": {
        "frontier_exposed_fraction": 0.2941072243418595,
        "frontier_contact": 31.984375,
        "sum_delta_p": 2.396962690073349,
        "realized_flips": 2.640625
      },
      "6": {
        "frontier_exposed_fraction": 0.2124771005369623,
        "frontier_contact": 24.53125,
        "sum_delta_p": 1.826622434433327,
        "realized_flips": 1.8125
      },
      "7": {
        "frontier_exposed_fraction": 0.14718991624793065,
        "frontier_contact": 17.921875,
        "sum_delta_p": 1.3252194137395754,
        "realized_flips": 1.359375
      },
      "8": {
        "frontier_exposed_fraction": 0.09009490091664704,
        "frontier_contact": 11.484375,
        "sum_delta_p": 0.8328628281150874,
        "realized_flips": 0.6875
      },
      "9": {
        "frontier_exposed_fraction": 0.05553758835096805,
        "frontier_contact": 7.453125,
        "sum_delta_p": 0.5075259337354268,
        "realized_flips": 0.578125
      },
      "10": {
        "frontier_exposed_fraction": 0.027763841043943048,
        "frontier_contact": 3.90625,
        "sum_delta_p": 0.2582709323944713,
        "realized_flips": 0.296875
      },
      "11": {
        "frontier_exposed_fraction": 0.011603838658065628,
        "frontier_contact": 1.703125,
        "sum_delta_p": 0.11190002116498185,
        "realized_flips": 0.03125
      },
      "12": {
        "frontier_exposed_fraction": 0.005460730499565365,
        "frontier_contact": 0.828125,
        "sum_delta_p": 0.049140289730036896,
        "realized_flips": 0.03125
      },
      "13": {
        "frontier_exposed_fraction": 0.0019474910407690754,
        "frontier_contact": 0.3125,
        "sum_delta_p": 0.01538174519878712,
        "realized_flips": 0.078125
      },
      "14": {
        "frontier_exposed_fraction": 0.0005836014926145945,
        "frontier_contact": 0.09375,
        "sum_delta_p": 0.004422057626134856,
        "realized_flips": 0.0
      },
      "15": {
        "frontier_exposed_fraction": 0.00017513736263736264,
        "frontier_contact": 0.03125,
        "sum_delta_p": 0.002294913192733677,
        "realized_flips": 0.0
      },
      "16": {
        "frontier_exposed_fraction": 8.311170212765957e-05,
        "frontier_contact": 0.015625,
        "sum_delta_p": 0.0011614798564730106,
        "realized_flips": 0.0
      },
      "17": {
        "frontier_exposed_fraction": 8.18062827225131e-05,
        "frontier_contact": 0.015625,
        "sum_delta_p": 0.0005298213219252657,
        "realized_flips": 0.0
      },
      "18": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      }
    },
    "surface_biased": {
      "5": {
        "frontier_exposed_fraction": 0.3601046067317971,
        "frontier_contact": 39.15625,
        "sum_delta_p": 3.099437876277604,
        "realized_flips": 3.265625
      },
      "6": {
        "frontier_exposed_fraction": 0.3044468468512933,
        "frontier_contact": 35.125,
        "sum_delta_p": 2.8280319158808007,
        "realized_flips": 2.953125
      },
      "7": {
        "frontier_exposed_fraction": 0.23847520190103993,
        "frontier_contact": 29.03125,
        "sum_delta_p": 2.3538721311542115,
        "realized_flips": 2.3125
      },
      "8": {
        "frontier_exposed_fraction": 0.17034028143742258,
        "frontier_contact": 21.84375,
        "sum_delta_p": 1.7422594650311303,
        "realized_flips": 1.59375
      },
      "9": {
        "frontier_exposed_fraction": 0.10876257150198715,
        "frontier_contact": 14.734375,
        "sum_delta_p": 1.1121780212900156,
        "realized_flips": 1.125
      },
      "10": {
        "frontier_exposed_fraction": 0.059362334467814776,
        "frontier_contact": 8.421875,
        "sum_delta_p": 0.5867654880233701,
        "realized_flips": 0.734375
      },
      "11": {
        "frontier_exposed_fraction": 0.0287073940141035,
        "frontier_contact": 4.25,
        "sum_delta_p": 0.29247301417895233,
        "realized_flips": 0.28125
      },
      "12": {
        "frontier_exposed_fraction": 0.014141603390744092,
        "frontier_contact": 2.203125,
        "sum_delta_p": 0.1552793870792661,
        "realized_flips": 0.046875
      },
      "13": {
        "frontier_exposed_fraction": 0.005739725560995709,
        "frontier_contact": 0.9375,
        "sum_delta_p": 0.05704959291038276,
        "realized_flips": 0.0625
      },
      "14": {
        "frontier_exposed_fraction": 0.0021364658387408664,
        "frontier_contact": 0.359375,
        "sum_delta_p": 0.022725803328481134,
        "realized_flips": 0.0
      },
      "15": {
        "frontier_exposed_fraction": 0.0006216908173718315,
        "frontier_contact": 0.109375,
        "sum_delta_p": 0.005791381718236503,
        "realized_flips": 0.0
      },
      "16": {
        "frontier_exposed_fraction": 0.0002484261231457144,
        "frontier_contact": 0.046875,
        "sum_delta_p": 0.0018294733960521163,
        "realized_flips": 0.0
      },
      "17": {
        "frontier_exposed_fraction": 7.735148514851485e-05,
        "frontier_contact": 0.015625,
        "sum_delta_p": 0.0011646184791354606,
        "realized_flips": 0.015625
      },
      "18": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      }
    }
  },
  "mean_ordering": {
    "access_fraction_auc": true,
    "probability_leverage_auc": true,
    "total_realized_flips": true,
    "sustained_loss_time": true
  },
  "paired_directional_tests": {
    "access_fraction_auc": {
      "random_gt_interior": {
        "mean_difference_B_minus_A": 0.331771738667431,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.0006917360187925689,
        "null_q95": 0.07390875729948006
      },
      "surface_gt_random": {
        "mean_difference_B_minus_A": 0.4460582116447923,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.0005253531336865096,
        "null_q95": 0.09490093511046695
      }
    },
    "probability_leverage_auc": {
      "random_gt_interior": {
        "mean_difference_B_minus_A": 3.460074750344867,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.019794514659087062,
        "null_q95": 0.8005927736479703
      },
      "surface_gt_random": {
        "mean_difference_B_minus_A": 4.926563608165329,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": -0.01338671131864218,
        "null_q95": 1.0965172687746574
      }
    },
    "total_realized_flips": {
      "random_gt_interior": {
        "mean_difference_B_minus_A": 3.453125,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.012015625,
        "null_q95": 0.859375
      },
      "surface_gt_random": {
        "mean_difference_B_minus_A": 4.875,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": -0.00209375,
        "null_q95": 1.21875
      }
    },
    "sustained_loss_time": {
      "random_gt_interior": {
        "mean_difference_B_minus_A": 1.203125,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.00496875,
        "null_q95": 0.421875
      },
      "surface_gt_random": {
        "mean_difference_B_minus_A": 1.25,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": 0.005734375,
        "null_q95": 0.4703124999999986
      }
    }
  },
  "per_group_ordering": {
    "access_fraction_auc": {
      "n": 64,
      "strict_order_count": 64,
      "strict_order_fraction": 1.0,
      "nondecreasing_order_count": 64,
      "nondecreasing_order_fraction": 1.0
    },
    "probability_leverage_auc": {
      "n": 64,
      "strict_order_count": 64,
      "strict_order_fraction": 1.0,
      "nondecreasing_order_count": 64,
      "nondecreasing_order_fraction": 1.0
    },
    "total_realized_flips": {
      "n": 64,
      "strict_order_count": 57,
      "strict_order_fraction": 0.890625,
      "nondecreasing_order_count": 62,
      "nondecreasing_order_fraction": 0.96875
    },
    "sustained_loss_time": {
      "n": 64,
      "strict_order_count": 25,
      "strict_order_fraction": 0.390625,
      "nondecreasing_order_count": 50,
      "nondecreasing_order_fraction": 0.78125
    }
  },
  "status": "MEASURED",
  "bounded_statement": "V7 measures causal lifetime over a frozen observation window rather than choosing a single late endpoint after observing the trajectory."
}
```


# Stage 3 — Secondary Descriptive Checkpoints

```json
{
  "role": "SECONDARY DESCRIPTIVE",
  "steps": [
    5,
    8,
    10,
    12,
    14,
    18
  ],
  "results": {
    "5": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.22798813136351134,
        "frontier_contact": 24.796875,
        "sum_delta_p": 1.7030227420836277,
        "realized_flips": 1.640625
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.2941072243418595,
        "frontier_contact": 31.984375,
        "sum_delta_p": 2.396962690073349,
        "realized_flips": 2.640625
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.3601046067317971,
        "frontier_contact": 39.15625,
        "sum_delta_p": 3.099437876277604,
        "realized_flips": 3.265625
      }
    },
    "8": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.038564565782429165,
        "frontier_contact": 4.9375,
        "sum_delta_p": 0.2989695113236634,
        "realized_flips": 0.28125
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.09009490091664704,
        "frontier_contact": 11.484375,
        "sum_delta_p": 0.8328628281150874,
        "realized_flips": 0.6875
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.17034028143742258,
        "frontier_contact": 21.84375,
        "sum_delta_p": 1.7422594650311303,
        "realized_flips": 1.59375
      }
    },
    "10": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.010111785682028078,
        "frontier_contact": 1.421875,
        "sum_delta_p": 0.07999204039502225,
        "realized_flips": 0.03125
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.027763841043943048,
        "frontier_contact": 3.90625,
        "sum_delta_p": 0.2582709323944713,
        "realized_flips": 0.296875
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.059362334467814776,
        "frontier_contact": 8.421875,
        "sum_delta_p": 0.5867654880233701,
        "realized_flips": 0.734375
      }
    },
    "12": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.00119256174790751,
        "frontier_contact": 0.1875,
        "sum_delta_p": 0.009893873675041647,
        "realized_flips": 0.046875
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.005460730499565365,
        "frontier_contact": 0.828125,
        "sum_delta_p": 0.049140289730036896,
        "realized_flips": 0.03125
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.014141603390744092,
        "frontier_contact": 2.203125,
        "sum_delta_p": 0.1552793870792661,
        "realized_flips": 0.046875
      }
    },
    "14": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.0005836014926145945,
        "frontier_contact": 0.09375,
        "sum_delta_p": 0.004422057626134856,
        "realized_flips": 0.0
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.0021364658387408664,
        "frontier_contact": 0.359375,
        "sum_delta_p": 0.022725803328481134,
        "realized_flips": 0.0
      }
    },
    "18": {
      "interior_biased": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "random_matched": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      },
      "surface_biased": {
        "frontier_exposed_fraction": 0.0,
        "frontier_contact": 0.0,
        "sum_delta_p": 0.0,
        "realized_flips": 0.0
      }
    }
  },
  "cannot_change_primary_decision": true,
  "status": "MEASURED"
}
```


# Stage 4 — Bounded Chapter 18 V7 Verdict

```json
{
  "experiment_role": "EXPLORATORY INTEGRATED CAUSAL-LIFETIME TEST",
  "chapter": 18,
  "question": "Does spatial placement change how long an exactly fixed quantity of propagated material remains causally available to growth?",
  "window": {
    "start": 5,
    "end": 18
  },
  "budget_invariant_valid": true,
  "required_metrics": [
    "access_fraction_auc",
    "probability_leverage_auc",
    "total_realized_flips"
  ],
  "mean_ordering_supported_for_required_metrics": true,
  "paired_directional_tests_supported": true,
  "sustained_loss_time_order_supportive": true,
  "status": "SUPPORTED",
  "bounded_claim": "With exact per-step and cumulative copy quantity held fixed, interior, random, and surface placement showed the predeclared ordered difference in integrated frontier accessibility, integrated local probability leverage, and total realized causal attachment flips over the frozen observation window.",
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
  "next_question": "If causal lifetime is supported, restore the opportunity feedback observed in v5 and test whether causal accessibility helps generate future opportunities for its own continuation, while keeping the claim below self-maintenance."
}
```
