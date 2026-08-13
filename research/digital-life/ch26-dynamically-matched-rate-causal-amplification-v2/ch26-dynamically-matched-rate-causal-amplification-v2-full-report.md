# Chapter 26 — Dynamically Matched Causal Amplification (V2)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-dynamically-matched-rate-causal-amplification-v2",
  "schema_version": 2,
  "chapter": 26,
  "chapter_title": "Does Candidate Subsampling Change Causal Amplification?",
  "profile": "full",
  "profile_config": {
    "groups": 192,
    "source_profile": "full",
    "probes_per_group": 4,
    "bootstrap_reps": 7000,
    "scientific": true
  },
  "seed": 20260913,
  "fresh_seed": true,
  "fractions": [
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "reference_fraction": 0.1,
  "horizon": 12,
  "primary_SEI": 0.15,
  "match_tolerance": 0.02,
  "started_at_unix": 1786622049.485707,
  "finished_at_unix": 1786626679.8811185,
  "final_status": "CAUSAL_AMPLIFICATION_BOUNDED_NEAR_ZERO_AT_MATCHED_RATE"
}
```

---

## Stage 0 — Frozen Chapter 26 V2 Protocol

```json
{
  "role": "DYNAMICALLY MATCHED BACKGROUND CONSTRUCTION-RATE CAUSAL AMPLIFICATION TEST",
  "question": "At dynamically matched background expected construction rate, does strong candidate subsampling change finite-horizon causal amplification relative to true exhaustive evaluation?",
  "primary_contrast": "G_T(f=0.10) - G_T(unbounded)",
  "primary_SEI_abs": 0.15,
  "two_sided": true,
  "same_checkpoint_across_arms": true,
  "same_probe_across_arms": true,
  "same_post_intervention_states_across_arms": true,
  "intervention_budget": 96,
  "dynamic_matching": {
    "reference_policy": "dedicated PREVENT-only f=0.10 trajectory, base offset 0",
    "target": "lag-specific exact expected attachments from reference PREVENT",
    "arm_calibration": "solve offset on each arm's PREVENT state every lag; apply same offset to FORCE",
    "relative_tolerance": 0.02,
    "minimum_record_pass_fraction": 0.95,
    "population_mean_every_arm_lag_must_pass": true
  },
  "arms": {
    "f=0.10": "primary strong-subsampling arm",
    "f=0.25": "secondary",
    "f=0.50": "secondary",
    "f=0.75": "secondary",
    "f=1.00": "secondary fixed-budget arm; NOT dynamically exhaustive",
    "unbounded": "primary true exhaustive reference"
  },
  "supported_probe_scope": "occupied_neighbors = 1",
  "forbidden_overclaims": [
    "formal branching ratio",
    "subcritical",
    "supercritical",
    "critical point",
    "phase transition",
    "directed percolation",
    "coherent structure",
    "individuality",
    "organism",
    "life"
  ],
  "status": "FROZEN"
}
```

---

## Stage 1 — Probe Support

```json
{
  "requested_groups": 192,
  "groups_with_probes": 192,
  "coverage_fraction": 1.0,
  "total_probes": 768,
  "probe_count_distribution": {
    "min": 4,
    "median": 4.0,
    "max": 4
  },
  "supported_scope": "occupied_neighbors = 1"
}
```

---

## Stage 2 — Dynamic Construction-Rate Matching Validity

```json
{
  "dynamic_matching": {
    "record_level_pass_fraction": 1.0,
    "required_record_pass_fraction": 0.95,
    "population_mean_every_arm_lag_within_2pct": true,
    "per_arm_lag": {
      "f=0.10": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": 0.0,
          "within_2pct": true
        }
      },
      "f=0.25": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": 9.669152024159778e-14,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 2.2311653711381602e-13,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 9.907495225531018e-14,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": 4.4730584018908155e-14,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.5709838789377522e-13,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": -3.6887168243446173e-14,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": 5.1243974979936694e-14,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.4535710269920236e-13,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": -2.6034625434379525e-14,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.837560322097474e-14,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": -8.132024147318641e-14,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": -7.266061446971659e-14,
          "within_2pct": true
        }
      },
      "f=0.50": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": -2.975850658307305e-14,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.6001032602289276e-14,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 9.15273268641626e-15,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": 2.962034582288137e-14,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.613799145118344e-13,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.248382663804088e-13,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": -5.43393334451317e-14,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": 3.15708137027084e-14,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.1683927723442203e-13,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.225486194903681e-13,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": 3.4655776946579466e-15,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": -8.407159534229207e-14,
          "within_2pct": true
        }
      },
      "f=0.75": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": 4.373561780471484e-14,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 9.739552205150685e-14,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.688904336300459e-14,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": 8.141369982748177e-14,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.2086351137573486e-13,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": -2.7468676091380985e-15,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.6300910175021055e-14,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": -9.326658479684374e-14,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.3190783744811418e-14,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.951325270938805e-13,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": 5.026209195655041e-14,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.391097473756982e-14,
          "within_2pct": true
        }
      },
      "f=1.00": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.997026760293054e-14,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 4.576959465051964e-14,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.0164918446420486e-13,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": -4.0435116294124496e-14,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.1485999362189043e-13,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": -2.0723167420924024e-14,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.7513701212938413e-14,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": -8.032035870908886e-14,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.2827865693739571e-13,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.5306452583296888e-13,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": -3.850087610672969e-14,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.1042041596237608e-13,
          "within_2pct": true
        }
      },
      "unbounded": {
        "1": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.997026760293054e-14,
          "within_2pct": true
        },
        "2": {
          "n_groups": 192,
          "mean_prevent_relative_error": 4.576959465051964e-14,
          "within_2pct": true
        },
        "3": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.0164918446420486e-13,
          "within_2pct": true
        },
        "4": {
          "n_groups": 192,
          "mean_prevent_relative_error": -4.0435116294124496e-14,
          "within_2pct": true
        },
        "5": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.1485999362189043e-13,
          "within_2pct": true
        },
        "6": {
          "n_groups": 192,
          "mean_prevent_relative_error": -2.0723167420924024e-14,
          "within_2pct": true
        },
        "7": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.7513701212938413e-14,
          "within_2pct": true
        },
        "8": {
          "n_groups": 192,
          "mean_prevent_relative_error": -8.032035870908886e-14,
          "within_2pct": true
        },
        "9": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.2827865693739571e-13,
          "within_2pct": true
        },
        "10": {
          "n_groups": 192,
          "mean_prevent_relative_error": 1.5306452583296888e-13,
          "within_2pct": true
        },
        "11": {
          "n_groups": 192,
          "mean_prevent_relative_error": -3.850087610672969e-14,
          "within_2pct": true
        },
        "12": {
          "n_groups": 192,
          "mean_prevent_relative_error": -1.1042041596237608e-13,
          "within_2pct": true
        }
      }
    },
    "status": "PASS",
    "scientific_valid": true
  },
  "probe_coverage_fraction": 1.0,
  "probe_coverage_valid": true,
  "scientific_valid": true
}
```

---

## Stage 3 — Dynamically Matched Arm Profiles

```json
{
  "f=0.10": {
    "fraction": 0.1,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.14973958333333334,
      "sd": 0.5663213108439906,
      "se": 0.040870720157949965,
      "ci95_low": 0.0703125,
      "ci95_high": 0.22916666666666666,
      "achieved_mde80_one_sided": 0.10162401820426986
    },
    "G_global": {
      "n": 192,
      "mean": 0.08072916666666667,
      "sd": 0.5255199266259818,
      "se": 0.03792613388775287,
      "ci95_low": 0.006510416666666667,
      "ci95_high": 0.15625,
      "achieved_mde80_one_sided": 0.09430237846877952
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.11304689592775367,
      "sd": 0.11540359463298334,
      "se": 0.008328537053350423,
      "ci95_low": 0.09669900618010999,
      "ci95_high": 0.12967715025410156,
      "achieved_mde80_one_sided": 0.020708698008101677
    },
    "E1_far": {
      "n": 192,
      "mean": -0.03867992365513344,
      "sd": 0.14666976479143756,
      "se": 0.010584978523039447,
      "ci95_low": -0.05972711230619143,
      "ci95_high": -0.01854832194604625,
      "achieved_mde80_one_sided": 0.026319282996728133
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.1640625,
      "sd": 0.17285758520932168,
      "se": 0.012474921669008819,
      "ci95_low": 0.140625,
      "ci95_high": 0.18880208333333334,
      "achieved_mde80_one_sided": 0.031018579117001347
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.16927083333333334,
      "sd": 0.1808748072529128,
      "se": 0.01305351483213636,
      "ci95_low": 0.14453125,
      "ci95_high": 0.1953125,
      "achieved_mde80_one_sided": 0.03245723647158926
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 130,
      "nonzero_fraction": 0.16927083333333334,
      "mean_given_nonzero": 0.8846153846153846
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.9976012310092396,
      "sd": 0.002812156674420074,
      "se": 0.0002029499266224791,
      "ci95_low": 0.9971873043306566,
      "ci95_high": 0.9979920322207627,
      "achieved_mde80_one_sided": 0.0005046298904920632
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.18055555555555555,
      "sd": 0.2190869209283242,
      "se": 0.01581123659673678,
      "ci95_low": 0.1508246527777778,
      "ci95_high": 0.21332465277777776,
      "achieved_mde80_one_sided": 0.039314242311589156
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    }
  },
  "f=0.25": {
    "fraction": 0.25,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.11197916666666667,
      "sd": 0.3569977188882984,
      "se": 0.02576409113753018,
      "ci95_low": 0.0625,
      "ci95_high": 0.1640625,
      "achieved_mde80_one_sided": 0.06406176491772793
    },
    "G_global": {
      "n": 192,
      "mean": 0.024739583333333332,
      "sd": 0.5042748511926559,
      "se": 0.036392902635204796,
      "ci95_low": -0.048177083333333336,
      "ci95_high": 0.09375,
      "achieved_mde80_one_sided": 0.09049003750394842
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10860140995846458,
      "sd": 0.08137380027052628,
      "se": 0.005872648186396399,
      "ci95_low": 0.09709998303237662,
      "ci95_high": 0.12025829098409202,
      "achieved_mde80_one_sided": 0.014602192080178775
    },
    "E1_far": {
      "n": 192,
      "mean": -0.042307428417741204,
      "sd": 0.10134595092571289,
      "se": 0.007314014006029867,
      "ci95_low": -0.057067681324044085,
      "ci95_high": -0.028046248555186178,
      "achieved_mde80_one_sided": 0.01818611195551652
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.13020833333333334,
      "sd": 0.14907729585559318,
      "se": 0.010758727111536026,
      "ci95_low": 0.109375,
      "ci95_high": 0.15234375,
      "achieved_mde80_one_sided": 0.026751304494076474
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.12760416666666666,
      "sd": 0.1491458739298432,
      "se": 0.01076367630773962,
      "ci95_low": 0.10677083333333333,
      "ci95_high": 0.1484375,
      "achieved_mde80_one_sided": 0.026763610546016513
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 98,
      "nonzero_fraction": 0.12760416666666666,
      "mean_given_nonzero": 0.8775510204081632
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.99829700878439,
      "sd": 0.0018111255525150218,
      "se": 0.0001307067281600947,
      "ci95_low": 0.9980301440398919,
      "ci95_high": 0.9985427630339843,
      "achieved_mde80_one_sided": 0.00032499899367147036
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.3059895833333333,
      "sd": 0.33414104392938604,
      "se": 0.0241145527074917,
      "ci95_low": 0.26019965277777773,
      "ci95_high": 0.35525173611111116,
      "achieved_mde80_one_sided": 0.05996022907996839
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 2.3958885076629424e-12,
      "sd": 3.1377666608122555e-13,
      "se": 2.264488032842736e-14,
      "ci95_low": 2.3531596722350125e-12,
      "ci95_high": 2.440095425898637e-12,
      "achieved_mde80_one_sided": 5.630592565621784e-14
    }
  },
  "f=0.50": {
    "fraction": 0.5,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.12239583333333333,
      "sd": 0.36087225565844483,
      "se": 0.026043711743433822,
      "ci95_low": 0.07291666666666667,
      "ci95_high": 0.17447916666666666,
      "achieved_mde80_one_sided": 0.06475703452479194
    },
    "G_global": {
      "n": 192,
      "mean": 0.0078125,
      "sd": 0.569689367226465,
      "se": 0.04111378869033339,
      "ci95_low": -0.07682291666666667,
      "ci95_high": 0.08333333333333333,
      "achieved_mde80_one_sided": 0.10222840199942582
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10572655905270567,
      "sd": 0.05497798751442123,
      "se": 0.003967694486369373,
      "ci95_low": 0.09792042592703111,
      "ci95_high": 0.11362168477083927,
      "achieved_mde80_one_sided": 0.009865572594598662
    },
    "E1_far": {
      "n": 192,
      "mean": -0.04051226908295281,
      "sd": 0.07348339711309225,
      "se": 0.005303207388026498,
      "ci95_low": -0.05113416667434624,
      "ci95_high": -0.030392139167507264,
      "achieved_mde80_one_sided": 0.013186291850475082
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.14453125,
      "sd": 0.1666070055738435,
      "se": 0.012023824939617005,
      "ci95_low": 0.12109375,
      "ci95_high": 0.16796875,
      "achieved_mde80_one_sided": 0.02989693843970383
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.13541666666666666,
      "sd": 0.17507166321262532,
      "se": 0.012634708985410593,
      "ci95_low": 0.11197916666666667,
      "ci95_high": 0.16015625,
      "achieved_mde80_one_sided": 0.03141588626226501
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 104,
      "nonzero_fraction": 0.13541666666666666,
      "mean_given_nonzero": 0.9038461538461539
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.9983799009213086,
      "sd": 0.0018938970490512208,
      "se": 0.00013668024638589503,
      "ci95_low": 0.9980999183174439,
      "ci95_high": 0.9986342666283411,
      "achieved_mde80_one_sided": 0.0003398519965688071
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.574001736111111,
      "sd": 0.6640804561471783,
      "se": 0.04792587876501786,
      "ci95_low": 0.4832845052083334,
      "ci95_high": 0.6710123697916667,
      "achieved_mde80_one_sided": 0.11916649271775642
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 2.369906333297472e-12,
      "sd": 3.0620137709127963e-13,
      "se": 2.209818093623555e-14,
      "ci95_low": 2.3265427768247458e-12,
      "ci95_high": 2.411842808901052e-12,
      "achieved_mde80_one_sided": 5.4946571361268943e-14
    }
  },
  "f=0.75": {
    "fraction": 0.75,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.125,
      "sd": 0.4765440597024543,
      "se": 0.034391605143741136,
      "ci95_low": 0.059895833333333336,
      "ci95_high": 0.19270833333333334,
      "achieved_mde80_one_sided": 0.0855138616029935
    },
    "G_global": {
      "n": 192,
      "mean": -0.014322916666666666,
      "sd": 0.6543175653539461,
      "se": 0.047221302811575175,
      "ci95_low": -0.11067708333333333,
      "ci95_high": 0.07682291666666667,
      "achieved_mde80_one_sided": 0.1174145823221912
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10756676918211616,
      "sd": 0.04868403923550224,
      "se": 0.00351346789473194,
      "ci95_low": 0.10081548499484629,
      "ci95_high": 0.11463472099314653,
      "achieved_mde80_one_sided": 0.00873614959351051
    },
    "E1_far": {
      "n": 192,
      "mean": -0.041995590019547634,
      "sd": 0.06524338372738021,
      "se": 0.004708535644730627,
      "ci95_low": -0.051436695943146336,
      "ci95_high": -0.03308987362279701,
      "achieved_mde80_one_sided": 0.011707655510505687
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.15755208333333334,
      "sd": 0.1954528836672841,
      "se": 0.014105596874899387,
      "ci95_low": 0.13020833333333334,
      "ci95_high": 0.18489583333333334,
      "achieved_mde80_one_sided": 0.03507321202212867
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.14713541666666666,
      "sd": 0.1935602572568922,
      "se": 0.013969008328959991,
      "ci95_low": 0.11979166666666667,
      "ci95_high": 0.17447916666666666,
      "achieved_mde80_one_sided": 0.034733588036414784
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 113,
      "nonzero_fraction": 0.14713541666666666,
      "mean_given_nonzero": 0.8495575221238938
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.9983680088070604,
      "sd": 0.001883900393549844,
      "se": 0.00013595879991780554,
      "ci95_low": 0.9980820790943642,
      "ci95_high": 0.9986251538463294,
      "achieved_mde80_one_sided": 0.0003380581380626885
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.8661024305555555,
      "sd": 1.0100041541651912,
      "se": 0.07289077128623918,
      "ci95_low": 0.7308973524305554,
      "ci95_high": 1.0164930555555556,
      "achieved_mde80_one_sided": 0.1812410703674665
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 2.3751538217374193e-12,
      "sd": 2.83037541769766e-13,
      "se": 2.0426475116443043e-14,
      "ci95_low": 2.336280022759335e-12,
      "ci95_high": 2.415054603910819e-12,
      "achieved_mde80_one_sided": 5.0789916866162565e-14
    }
  },
  "f=1.00": {
    "fraction": 1.0,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.10026041666666667,
      "sd": 0.4235074622383332,
      "se": 0.03056401841588962,
      "ci95_low": 0.0390625,
      "ci95_high": 0.16015625,
      "achieved_mde80_one_sided": 0.07599666342771391
    },
    "G_global": {
      "n": 192,
      "mean": -0.045572916666666664,
      "sd": 0.599033851184344,
      "se": 0.04323154440437241,
      "ci95_low": -0.13411458333333334,
      "ci95_high": 0.037760416666666664,
      "achieved_mde80_one_sided": 0.10749414834311569
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.1081047725539036,
      "sd": 0.04397017258351194,
      "se": 0.0031732738721756155,
      "ci95_low": 0.10208971071859298,
      "ci95_high": 0.11423462187230023,
      "achieved_mde80_one_sided": 0.007890265708723542
    },
    "E1_far": {
      "n": 192,
      "mean": -0.05672629219714178,
      "sd": 0.04727750121847814,
      "se": 0.003411959756887652,
      "ci95_low": -0.06355306524757143,
      "ci95_high": -0.050130399132673795,
      "achieved_mde80_one_sided": 0.008483752160622044
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.15494791666666666,
      "sd": 0.1727934862665852,
      "se": 0.01247029572627836,
      "ci95_low": 0.13151041666666666,
      "ci95_high": 0.1796875,
      "achieved_mde80_one_sided": 0.031007076826695835
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.13671875,
      "sd": 0.15932831546002688,
      "se": 0.011498530727547017,
      "ci95_low": 0.11458333333333333,
      "ci95_high": 0.16015625,
      "achieved_mde80_one_sided": 0.02859080758701284
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 105,
      "nonzero_fraction": 0.13671875,
      "mean_given_nonzero": 0.7333333333333333
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.9987781691006784,
      "sd": 0.001577736029260786,
      "se": 0.00011386329015048577,
      "ci95_low": 0.99853575863743,
      "ci95_high": 0.9989858814107306,
      "achieved_mde80_one_sided": 0.0002831182084957768
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.8583984375,
      "sd": 1.1226150692093566,
      "se": 0.08101776405054406,
      "ci95_low": 0.7133192274305554,
      "ci95_high": 1.0315782335069443,
      "achieved_mde80_one_sided": 0.20144863356757417
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 2.352726517663842e-12,
      "sd": 2.368417467913295e-13,
      "se": 1.7092580783164407e-14,
      "ci95_low": 2.3186558842032428e-12,
      "ci95_high": 2.386221079444975e-12,
      "achieved_mde80_one_sided": 4.250027241882053e-14
    }
  },
  "unbounded": {
    "fraction": null,
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.1484375,
      "sd": 0.38471810071233564,
      "se": 0.02776463737604857,
      "ci95_low": 0.09505208333333333,
      "ci95_high": 0.20572916666666666,
      "achieved_mde80_one_sided": 0.06903607284712053
    },
    "G_global": {
      "n": 192,
      "mean": 0.1484375,
      "sd": 0.38471810071233564,
      "se": 0.02776463737604857,
      "ci95_low": 0.09635416666666667,
      "ci95_high": 0.20442708333333334,
      "achieved_mde80_one_sided": 0.06903607284712053
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10823831018156888,
      "sd": 0.044074402124761033,
      "se": 0.003180795991387825,
      "ci95_low": 0.10191690007160294,
      "ci95_high": 0.11444597150246141,
      "achieved_mde80_one_sided": 0.00790896926904257
    },
    "E1_far": {
      "n": 192,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.14322916666666666,
      "sd": 0.1647812752519153,
      "se": 0.01189206420301289,
      "ci95_low": 0.12109375,
      "ci95_high": 0.16666666666666666,
      "achieved_mde80_one_sided": 0.029569318680533523
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.12890625,
      "sd": 0.15556130948231764,
      "se": 0.011226670488138347,
      "ci95_low": 0.10677083333333333,
      "ci95_high": 0.15104166666666666,
      "achieved_mde80_one_sided": 0.02791483393614704
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 99,
      "nonzero_fraction": 0.12890625,
      "mean_given_nonzero": 1.1515151515151516
    },
    "mean_selected_jaccard": {
      "n": 192,
      "mean": 0.999327597898902,
      "sd": 0.0006022926040358332,
      "se": 4.3466724633876124e-05,
      "ci95_low": 0.9992403453114392,
      "ci95_high": 0.9994096835652947,
      "achieved_mde80_one_sided": 0.00010807891807146904
    },
    "mean_selected_symdiff": {
      "n": 192,
      "mean": 0.4697265625,
      "sd": 0.43206068290451355,
      "se": 0.031181293947646807,
      "ci95_low": 0.4090711805555556,
      "ci95_high": 0.5334201388888888,
      "achieved_mde80_one_sided": 0.07753150351944499
    },
    "max_prevent_relative_error": {
      "n": 192,
      "mean": 2.352726517663842e-12,
      "sd": 2.368417467913295e-13,
      "se": 1.7092580783164407e-14,
      "ci95_low": 2.319078618384828e-12,
      "ci95_high": 2.386127937267765e-12,
      "achieved_mde80_one_sided": 4.250027241882053e-14
    }
  }
}
```

---

## Stage 4 — Primary Strong-Subsampling vs True-Unbounded Test

```json
{
  "contrast": "G_T(f=0.10) - G_T(unbounded)",
  "SEI_abs": 0.15,
  "result": {
    "n": 192,
    "mean": 0.0013020833333333333,
    "sd": 0.6428713992833865,
    "se": 0.046395246928821826,
    "ci95_low": -0.08984375,
    "ci95_high": 0.08854166666666667,
    "achieved_mde80_one_sided": 0.1153606151363367
  },
  "status": "BOUNDED_NEAR_ZERO"
}
```

---

## Stage 5 — Secondary Allocation-Concentration Contrasts

```json
{
  "f=0.10": {
    "G_local_minus_unbounded": {
      "n": 192,
      "mean": 0.0013020833333333333,
      "sd": 0.6428713992833865,
      "se": 0.046395246928821826,
      "ci95_low": -0.08854166666666667,
      "ci95_high": 0.09114583333333333,
      "achieved_mde80_one_sided": 0.1153606151363367
    },
    "E1_ring1_minus_unbounded": {
      "n": 192,
      "mean": 0.004808585746184806,
      "sd": 0.11875250638036083,
      "se": 0.00857022394070551,
      "ci95_low": -0.011275437184878176,
      "ci95_high": 0.02174081277760008,
      "achieved_mde80_one_sided": 0.02130964637762849
    },
    "E1_far_minus_unbounded": {
      "n": 192,
      "mean": -0.03867992365513344,
      "sd": 0.14666976479143756,
      "se": 0.010584978523039447,
      "ci95_low": -0.059543733948892424,
      "ci95_high": -0.01807275302823249,
      "achieved_mde80_one_sided": 0.026319282996728133
    },
    "G_nonzero_rate_minus_unbounded": {
      "n": 192,
      "mean": 0.040364583333333336,
      "sd": 0.23165322611267875,
      "se": 0.016718131556850042,
      "ci95_low": 0.0078125,
      "ci95_high": 0.07161458333333333,
      "achieved_mde80_one_sided": 0.04156921383104705
    }
  },
  "f=0.25": {
    "G_local_minus_unbounded": {
      "n": 192,
      "mean": -0.036458333333333336,
      "sd": 0.5128954439987692,
      "se": 0.037015040332352755,
      "ci95_low": -0.109375,
      "ci95_high": 0.036458333333333336,
      "achieved_mde80_one_sided": 0.09203696724769135
    },
    "E1_ring1_minus_unbounded": {
      "n": 192,
      "mean": 0.000363099776895716,
      "sd": 0.07078741126534557,
      "se": 0.005108641368660502,
      "ci95_low": -0.009612436000569335,
      "ci95_high": 0.010102527618751621,
      "achieved_mde80_one_sided": 0.012702508334609232
    },
    "E1_far_minus_unbounded": {
      "n": 192,
      "mean": -0.042307428417741204,
      "sd": 0.10134595092571289,
      "se": 0.007314014006029867,
      "ci95_low": -0.056915062364507926,
      "ci95_high": -0.02830207566957929,
      "achieved_mde80_one_sided": 0.01818611195551652
    },
    "G_nonzero_rate_minus_unbounded": {
      "n": 192,
      "mean": -0.0013020833333333333,
      "sd": 0.20385261177007255,
      "se": 0.014711795035057458,
      "ci95_low": -0.029947916666666668,
      "ci95_high": 0.02737630208333286,
      "achieved_mde80_one_sided": 0.03658050850785785
    }
  },
  "f=0.50": {
    "G_local_minus_unbounded": {
      "n": 192,
      "mean": -0.026041666666666668,
      "sd": 0.4960302709194388,
      "se": 0.03579790130519263,
      "ci95_low": -0.09765625,
      "ci95_high": 0.044270833333333336,
      "achieved_mde80_one_sided": 0.08901058165489459
    },
    "E1_ring1_minus_unbounded": {
      "n": 192,
      "mean": -0.0025117511288632066,
      "sd": 0.0413312497821366,
      "se": 0.0029828260234575285,
      "ci95_low": -0.008523618975652443,
      "ci95_high": 0.003364574636910491,
      "achieved_mde80_one_sided": 0.007416721920645068
    },
    "E1_far_minus_unbounded": {
      "n": 192,
      "mean": -0.04051226908295281,
      "sd": 0.07348339711309225,
      "se": 0.005303207388026498,
      "ci95_low": -0.05071441227611976,
      "ci95_high": -0.03021161814613077,
      "achieved_mde80_one_sided": 0.013186291850475082
    },
    "G_nonzero_rate_minus_unbounded": {
      "n": 192,
      "mean": 0.006510416666666667,
      "sd": 0.2131705555530578,
      "se": 0.0153842597039825,
      "ci95_low": -0.0234375,
      "ci95_high": 0.036490885416666195,
      "achieved_mde80_one_sided": 0.03825257500173082
    }
  },
  "f=0.75": {
    "G_local_minus_unbounded": {
      "n": 192,
      "mean": -0.0234375,
      "sd": 0.46412971675928877,
      "se": 0.033495677113735016,
      "ci95_low": -0.08984375,
      "ci95_high": 0.040364583333333336,
      "achieved_mde80_one_sided": 0.08328615907954415
    },
    "E1_ring1_minus_unbounded": {
      "n": 192,
      "mean": -0.0006715409994527216,
      "sd": 0.025013794179226452,
      "se": 0.0018052151003537858,
      "ci95_low": -0.004290420320795911,
      "ci95_high": 0.0028208270060193523,
      "achieved_mde80_one_sided": 0.004488621964868695
    },
    "E1_far_minus_unbounded": {
      "n": 192,
      "mean": -0.041995590019547634,
      "sd": 0.06524338372738021,
      "se": 0.004708535644730627,
      "ci95_low": -0.05158919420335988,
      "ci95_high": -0.03297620507545927,
      "achieved_mde80_one_sided": 0.011707655510505687
    },
    "G_nonzero_rate_minus_unbounded": {
      "n": 192,
      "mean": 0.018229166666666668,
      "sd": 0.18177711910377614,
      "se": 0.013118633580884978,
      "ci95_low": -0.006510416666666667,
      "ci95_high": 0.044270833333333336,
      "achieved_mde80_one_sided": 0.032619152603301504
    }
  },
  "f=1.00": {
    "G_local_minus_unbounded": {
      "n": 192,
      "mean": -0.048177083333333336,
      "sd": 0.24528925097698775,
      "se": 0.017702226885110695,
      "ci95_low": -0.08854166666666667,
      "ci95_high": -0.01953125,
      "achieved_mde80_one_sided": 0.04401614212512665
    },
    "E1_ring1_minus_unbounded": {
      "n": 192,
      "mean": -0.00013353762766526813,
      "sd": 0.0007725073856393205,
      "se": 5.575091838122947e-05,
      "ci95_low": -0.0002512407848984386,
      "ci95_high": -3.445448922498477e-05,
      "achieved_mde80_one_sided": 0.000138623257006074
    },
    "E1_far_minus_unbounded": {
      "n": 192,
      "mean": -0.05672629219714178,
      "sd": 0.04727750121847814,
      "se": 0.003411959756887652,
      "ci95_low": -0.06359407480590289,
      "ci95_high": -0.05038931603553444,
      "achieved_mde80_one_sided": 0.008483752160622044
    },
    "G_nonzero_rate_minus_unbounded": {
      "n": 192,
      "mean": 0.0078125,
      "sd": 0.07193224160415795,
      "se": 0.005191262381696724,
      "ci95_low": -0.0013020833333333333,
      "ci95_high": 0.018229166666666668,
      "achieved_mde80_one_sided": 0.012907943406474855
    }
  }
}
```

---

## Stage 6 — Per-Lag Background Construction Matching

```json
{
  "1": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.58190861491069,
        "ci95_high": 37.56330626523252,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.58930123910253,
        "ci95_high": 37.5710586187639,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "force_expected": {
        "n": 192,
        "mean": 37.11997520114821,
        "sd": 3.4762618062836985,
        "se": 0.2508775862039385,
        "ci95_low": 36.63837407148647,
        "ci95_high": 37.604396822352086,
        "achieved_mde80_one_sided": 0.6238008111651328
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.57416703149452,
        "ci95_high": 37.569763926379125,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.07857598232237,
        "sd": 3.4764410281056555,
        "se": 0.25089052042483245,
        "ci95_low": 36.602552474838554,
        "ci95_high": 37.55975296790167,
        "achieved_mde80_one_sided": 0.623832971780226
      },
      "force_expected": {
        "n": 192,
        "mean": 37.12396035910583,
        "sd": 3.498372429170957,
        "se": 0.25247328296342714,
        "ci95_low": 36.625427403435246,
        "ci95_high": 37.60844117173729,
        "achieved_mde80_one_sided": 0.6277684710426213
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.58099761777544,
        "ci95_high": 37.566990489734366,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.0785759823182,
        "sd": 3.4764410281104907,
        "se": 0.2508905204251814,
        "ci95_low": 36.59192606775166,
        "ci95_high": 37.56922691083625,
        "achieved_mde80_one_sided": 0.6238329717810936
      },
      "force_expected": {
        "n": 192,
        "mean": 37.126851504436964,
        "sd": 3.486880143564292,
        "se": 0.25164389868985065,
        "ci95_low": 36.638815235129854,
        "ci95_high": 37.60259328536872,
        "achieved_mde80_one_sided": 0.6257062278966592
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.588153752594316,
        "ci95_high": 37.569179189463064,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.07857598232107,
        "sd": 3.4764410281126557,
        "se": 0.25089052042533766,
        "ci95_low": 36.57292841973806,
        "ci95_high": 37.560170834548686,
        "achieved_mde80_one_sided": 0.6238329717814821
      },
      "force_expected": {
        "n": 192,
        "mean": 37.127909336345745,
        "sd": 3.4910188948181937,
        "se": 0.25194258733366925,
        "ci95_low": 36.64005098674168,
        "ci95_high": 37.63063367863577,
        "achieved_mde80_one_sided": 0.6264489097006383
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.59635489754627,
        "ci95_high": 37.56966344254675,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.07857598232024,
        "sd": 3.476441028112207,
        "se": 0.2508905204253053,
        "ci95_low": 36.59311967629101,
        "ci95_high": 37.57725639310372,
        "achieved_mde80_one_sided": 0.6238329717814016
      },
      "force_expected": {
        "n": 192,
        "mean": 37.11430759042505,
        "sd": 3.4902599986430256,
        "se": 0.2518878187197917,
        "ci95_low": 36.63652767454274,
        "ci95_high": 37.600309990099234,
        "achieved_mde80_one_sided": 0.626312728919086
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 37.07857598231933,
        "sd": 3.476441028110785,
        "se": 0.25089052042520266,
        "ci95_low": 36.58963209003353,
        "ci95_high": 37.56563842259866,
        "achieved_mde80_one_sided": 0.6238329717811465
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.07857598232024,
        "sd": 3.476441028112207,
        "se": 0.2508905204253053,
        "ci95_low": 36.58538687252188,
        "ci95_high": 37.56112013728387,
        "achieved_mde80_one_sided": 0.6238329717814016
      },
      "force_expected": {
        "n": 192,
        "mean": 37.17116742024985,
        "sd": 3.4888650647337247,
        "se": 0.25178714803628716,
        "ci95_low": 36.675959986087555,
        "ci95_high": 37.65652622108156,
        "achieved_mde80_one_sided": 0.6260624137953601
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 4.170885858911788e-12,
      "relative_range": 1.1248775737505519e-13,
      "cv": 3.520010726796172e-14
    }
  },
  "2": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.87473628415609,
        "ci95_high": 37.88783334474112,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.86022693854979,
        "ci95_high": 37.877773623065735,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "force_expected": {
        "n": 192,
        "mean": 37.38259968956935,
        "sd": 3.578508689921565,
        "se": 0.25825661942795386,
        "ci95_low": 36.87223158784092,
        "ci95_high": 37.879969332456234,
        "achieved_mde80_one_sided": 0.6421485917716211
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.87820695436887,
        "ci95_high": 37.87558691572284,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.37975201526685,
        "sd": 3.583078111157182,
        "se": 0.2585863890005069,
        "ci95_low": 36.86911227085749,
        "ci95_high": 37.873623095527684,
        "achieved_mde80_one_sided": 0.64296855552354
      },
      "force_expected": {
        "n": 192,
        "mean": 37.38202817810008,
        "sd": 3.585440468199239,
        "se": 0.2587568774347761,
        "ci95_low": 36.87541617259303,
        "ci95_high": 37.89280747161383,
        "achieved_mde80_one_sided": 0.6433924707293606
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.861635825994426,
        "ci95_high": 37.87671581256247,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.37975201525952,
        "sd": 3.583078111161247,
        "se": 0.2585863890008002,
        "ci95_low": 36.87547898094267,
        "ci95_high": 37.875845186413635,
        "achieved_mde80_one_sided": 0.6429685555242695
      },
      "force_expected": {
        "n": 192,
        "mean": 37.38106846138051,
        "sd": 3.5827267805291436,
        "se": 0.2585610338964228,
        "ci95_low": 36.868580724178734,
        "ci95_high": 37.887481294695824,
        "achieved_mde80_one_sided": 0.6429055106946491
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.8635992247181,
        "ci95_high": 37.8900194829174,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.3797520152626,
        "sd": 3.5830781111612615,
        "se": 0.2585863890008013,
        "ci95_low": 36.866971997492605,
        "ci95_high": 37.87850079754812,
        "achieved_mde80_one_sided": 0.642968555524272
      },
      "force_expected": {
        "n": 192,
        "mean": 37.38147666076005,
        "sd": 3.581837761396826,
        "se": 0.25849687446700303,
        "ci95_low": 36.874661650186695,
        "ci95_high": 37.87831897957856,
        "achieved_mde80_one_sided": 0.6427459798863312
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.87693382064931,
        "ci95_high": 37.88280140160208,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.37975201526117,
        "sd": 3.5830781111659182,
        "se": 0.25858638900113734,
        "ci95_low": 36.884510338428704,
        "ci95_high": 37.880770515342505,
        "achieved_mde80_one_sided": 0.6429685555251077
      },
      "force_expected": {
        "n": 192,
        "mean": 37.37828053514833,
        "sd": 3.5805619114562792,
        "se": 0.2584047979286755,
        "ci95_low": 36.86997343678969,
        "ci95_high": 37.876635960739755,
        "achieved_mde80_one_sided": 0.6425170338885356
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 37.37975201525932,
        "sd": 3.583078111164386,
        "se": 0.25858638900102676,
        "ci95_low": 36.88155440985314,
        "ci95_high": 37.87897173525186,
        "achieved_mde80_one_sided": 0.6429685555248327
      },
      "prevent_expected": {
        "n": 192,
        "mean": 37.37975201526117,
        "sd": 3.5830781111659182,
        "se": 0.25858638900113734,
        "ci95_low": 36.8911360298438,
        "ci95_high": 37.87941494491606,
        "achieved_mde80_one_sided": 0.6429685555251077
      },
      "force_expected": {
        "n": 192,
        "mean": 37.3865902957669,
        "sd": 3.5812286840496217,
        "se": 0.2584529180957073,
        "ci95_low": 36.88468054948395,
        "ci95_high": 37.89354864087422,
        "achieved_mde80_one_sided": 0.6426366834741445
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 7.531752999057062e-12,
      "relative_range": 2.0149285623890507e-13,
      "cv": 6.760271594560861e-14
    }
  },
  "3": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.70443201599953,
        "ci95_high": 38.63412758533327,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.68867209966218,
        "ci95_high": 38.63237849034082,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "force_expected": {
        "n": 192,
        "mean": 38.160764021115604,
        "sd": 3.3370807120021913,
        "se": 0.24083305592274665,
        "ci95_low": 37.70135000253471,
        "ci95_high": 38.631206008572306,
        "achieved_mde80_one_sided": 0.5988253391351732
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.67345903392734,
        "ci95_high": 38.61977135398989,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.15950167016118,
        "sd": 3.3387313143454276,
        "se": 0.24095217788614573,
        "ci95_low": 37.68342914472846,
        "ci95_high": 38.63004152292165,
        "achieved_mde80_one_sided": 0.5991215329025014
      },
      "force_expected": {
        "n": 192,
        "mean": 38.1659420068188,
        "sd": 3.346322102315505,
        "se": 0.24149999582088144,
        "ci95_low": 37.69245731505677,
        "ci95_high": 38.634230746591776,
        "achieved_mde80_one_sided": 0.600483668425366
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.68307390679213,
        "ci95_high": 38.625811607215304,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.159501670157645,
        "sd": 3.338731314344044,
        "se": 0.24095217788604587,
        "ci95_low": 37.669201996227365,
        "ci95_high": 38.61821067711213,
        "achieved_mde80_one_sided": 0.599121532902253
      },
      "force_expected": {
        "n": 192,
        "mean": 38.16106725466428,
        "sd": 3.33052752039062,
        "se": 0.24036012005512267,
        "ci95_low": 37.690411087571874,
        "ci95_high": 38.62761736381822,
        "achieved_mde80_one_sided": 0.5976493959896859
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.67172583783818,
        "ci95_high": 38.623111450920184,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.159501670158,
        "sd": 3.3387313143452086,
        "se": 0.2409521778861299,
        "ci95_low": 37.682985834566345,
        "ci95_high": 38.614003339656016,
        "achieved_mde80_one_sided": 0.599121532902462
      },
      "force_expected": {
        "n": 192,
        "mean": 38.16283515973326,
        "sd": 3.339421179016461,
        "se": 0.2410019645803364,
        "ci95_low": 37.69092575790502,
        "ci95_high": 38.63990321905055,
        "achieved_mde80_one_sided": 0.599245326265995
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.68445131331421,
        "ci95_high": 38.63151481511304,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.15950167016137,
        "sd": 3.338731314346363,
        "se": 0.2409521778862132,
        "ci95_low": 37.67474297043509,
        "ci95_high": 38.6206281342709,
        "achieved_mde80_one_sided": 0.5991215329026691
      },
      "force_expected": {
        "n": 192,
        "mean": 38.15577052943863,
        "sd": 3.333692609963325,
        "se": 0.24058854071972396,
        "ci95_low": 37.67362919398449,
        "ci95_high": 38.62642299438952,
        "achieved_mde80_one_sided": 0.5982173582298412
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.15950167015736,
        "sd": 3.338731314344925,
        "se": 0.24095217788610945,
        "ci95_low": 37.68377807823488,
        "ci95_high": 38.623109746143285,
        "achieved_mde80_one_sided": 0.5991215329024111
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.15950167016137,
        "sd": 3.338731314346363,
        "se": 0.2409521778862132,
        "ci95_low": 37.68537415126298,
        "ci95_high": 38.61355723138019,
        "achieved_mde80_one_sided": 0.5991215329026691
      },
      "force_expected": {
        "n": 192,
        "mean": 38.167176696581954,
        "sd": 3.338677549454415,
        "se": 0.24094829773935833,
        "ci95_low": 37.690057786289884,
        "ci95_high": 38.62586681413376,
        "achieved_mde80_one_sided": 0.5991118850150593
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 4.007461029686965e-12,
      "relative_range": 1.0501869401561856e-13,
      "cv": 4.7912612255730124e-14
    }
  },
  "4": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.656914324462214,
        "ci95_high": 38.65550238968912,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.65738297771418,
        "ci95_high": 38.64506851431444,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "force_expected": {
        "n": 192,
        "mean": 38.16576276394483,
        "sd": 3.5235934344023576,
        "se": 0.2542934522333749,
        "ci95_low": 37.677062242193195,
        "ci95_high": 38.660658567994446,
        "achieved_mde80_one_sided": 0.6322942761742455
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.67108646420591,
        "ci95_high": 38.6633539338322,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.16398391132072,
        "sd": 3.5289252752387936,
        "se": 0.25467824470114897,
        "ci95_low": 37.65801921126803,
        "ci95_high": 38.644357423033696,
        "achieved_mde80_one_sided": 0.6332510529718849
      },
      "force_expected": {
        "n": 192,
        "mean": 38.166335885991934,
        "sd": 3.531143694207001,
        "se": 0.2548383452997077,
        "ci95_low": 37.66197411016289,
        "ci95_high": 38.64982773049736,
        "achieved_mde80_one_sided": 0.6336491390853561
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.67910464080634,
        "ci95_high": 38.65575866523422,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.16398391132082,
        "sd": 3.528925275246245,
        "se": 0.2546782447016867,
        "ci95_low": 37.667608778022256,
        "ci95_high": 38.67318599966884,
        "achieved_mde80_one_sided": 0.6332510529732219
      },
      "force_expected": {
        "n": 192,
        "mean": 38.1715479235489,
        "sd": 3.525101792878114,
        "se": 0.25440230862987645,
        "ci95_low": 37.65776757256727,
        "ci95_high": 38.65668287767137,
        "achieved_mde80_one_sided": 0.6325649448675539
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.66776137219178,
        "ci95_high": 38.666752893100444,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.16398391132226,
        "sd": 3.528925275240576,
        "se": 0.25467824470127765,
        "ci95_low": 37.68127537547159,
        "ci95_high": 38.67227852001832,
        "achieved_mde80_one_sided": 0.6332510529722049
      },
      "force_expected": {
        "n": 192,
        "mean": 38.163148243926294,
        "sd": 3.5267021925772224,
        "se": 0.25451780752951286,
        "ci95_low": 37.66676175000508,
        "ci95_high": 38.66129586779021,
        "achieved_mde80_one_sided": 0.6328521299779181
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.67258835918224,
        "ci95_high": 38.66344391961718,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.16398391131762,
        "sd": 3.5289252752405744,
        "se": 0.2546782447012775,
        "ci95_low": 37.65762425308771,
        "ci95_high": 38.64844248624184,
        "achieved_mde80_one_sided": 0.6332510529722044
      },
      "force_expected": {
        "n": 192,
        "mean": 38.15933962089338,
        "sd": 3.530148945142037,
        "se": 0.2547665554696536,
        "ci95_low": 37.65839039261947,
        "ci95_high": 38.66262024571765,
        "achieved_mde80_one_sided": 0.6334706354776852
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.163983911319455,
        "sd": 3.52892527524315,
        "se": 0.2546782447014634,
        "ci95_low": 37.66054337360891,
        "ci95_high": 38.66120931593259,
        "achieved_mde80_one_sided": 0.6332510529726667
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.16398391131762,
        "sd": 3.5289252752405744,
        "se": 0.2546782447012775,
        "ci95_low": 37.66122710572463,
        "ci95_high": 38.65835625914138,
        "achieved_mde80_one_sided": 0.6332510529722044
      },
      "force_expected": {
        "n": 192,
        "mean": 38.16962030759146,
        "sd": 3.5285670352055214,
        "se": 0.25465239095369346,
        "ci95_low": 37.671624847199254,
        "ci95_high": 38.65734126379824,
        "achieved_mde80_one_sided": 0.6331867682787864
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 4.639844064513454e-12,
      "relative_range": 1.2157651243368328e-13,
      "cv": 4.4797770829120346e-14
    }
  },
  "5": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.89634043471191,
        "ci95_high": 38.886397328065,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.908961639322,
        "ci95_high": 38.89246007194352,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "force_expected": {
        "n": 192,
        "mean": 38.394034732059446,
        "sd": 3.492724250014196,
        "se": 0.2520656607438537,
        "ci95_low": 37.89481694775601,
        "ci95_high": 38.892158108854964,
        "achieved_mde80_one_sided": 0.626754928641061
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.89660826031827,
        "ci95_high": 38.885928254318976,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.3956976894286,
        "sd": 3.496424183584533,
        "se": 0.252332680449206,
        "ci95_low": 37.9030887558117,
        "ci95_high": 38.90996851725332,
        "achieved_mde80_one_sided": 0.627418866425684
      },
      "force_expected": {
        "n": 192,
        "mean": 38.39749486926715,
        "sd": 3.4950691736622796,
        "se": 0.252234891031285,
        "ci95_low": 37.901715405398186,
        "ci95_high": 38.89570550317257,
        "achieved_mde80_one_sided": 0.6271757154963982
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.91461041934518,
        "ci95_high": 38.8894586344782,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.39569768942901,
        "sd": 3.496424183586427,
        "se": 0.25233268044934265,
        "ci95_low": 37.909020255446165,
        "ci95_high": 38.88755437904452,
        "achieved_mde80_one_sided": 0.6274188664260238
      },
      "force_expected": {
        "n": 192,
        "mean": 38.40147264667629,
        "sd": 3.4907115854295805,
        "se": 0.2519204091888892,
        "ci95_low": 37.91105047271667,
        "ci95_high": 38.890495445903035,
        "achieved_mde80_one_sided": 0.6263937643011895
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.91542158213562,
        "ci95_high": 38.903628053839796,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.39569768941795,
        "sd": 3.4964241835840006,
        "se": 0.25233268044916757,
        "ci95_low": 37.889882848617994,
        "ci95_high": 38.89901167683271,
        "achieved_mde80_one_sided": 0.6274188664255884
      },
      "force_expected": {
        "n": 192,
        "mean": 38.39531219245708,
        "sd": 3.496001524692843,
        "se": 0.2523021776710944,
        "ci95_low": 37.903684548312306,
        "ci95_high": 38.888701937486,
        "achieved_mde80_one_sided": 0.6273430220347335
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.89661506020024,
        "ci95_high": 38.906882229320594,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.395697689418796,
        "sd": 3.4964241835906185,
        "se": 0.25233268044964513,
        "ci95_low": 37.8974757047415,
        "ci95_high": 38.88887649394875,
        "achieved_mde80_one_sided": 0.6274188664267759
      },
      "force_expected": {
        "n": 192,
        "mean": 38.38568578756472,
        "sd": 3.4914620034016313,
        "se": 0.25197456594116024,
        "ci95_low": 37.896687593148386,
        "ci95_high": 38.86877818629231,
        "achieved_mde80_one_sided": 0.6265284237042392
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.39569768942303,
        "sd": 3.4964241835887857,
        "se": 0.2523326804495129,
        "ci95_low": 37.90317645263384,
        "ci95_high": 38.87536956702711,
        "achieved_mde80_one_sided": 0.6274188664264472
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.395697689418796,
        "sd": 3.4964241835906185,
        "se": 0.25233268044964513,
        "ci95_low": 37.90587266900348,
        "ci95_high": 38.8957377998643,
        "achieved_mde80_one_sided": 0.6274188664267759
      },
      "force_expected": {
        "n": 192,
        "mean": 38.39919251899064,
        "sd": 3.4958469577055276,
        "se": 0.2522910227596276,
        "ci95_low": 37.90474852445821,
        "ci95_high": 38.89340378318931,
        "achieved_mde80_one_sided": 0.6273152856277998
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 1.1056044968427159e-11,
      "relative_range": 2.8795009945796335e-13,
      "cv": 1.20177026856616e-13
    }
  },
  "6": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.340446254950535,
        "ci95_high": 39.31187796863489,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.338210690029996,
        "ci95_high": 39.30686017494473,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "force_expected": {
        "n": 192,
        "mean": 38.82580035635082,
        "sd": 3.451793029303518,
        "se": 0.24911170433190752,
        "ci95_low": 38.33157905359057,
        "ci95_high": 39.31887147138368,
        "achieved_mde80_one_sided": 0.6194099902836719
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.349789042708586,
        "ci95_high": 39.303295346148325,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.83314375114187,
        "sd": 3.4583472781127114,
        "se": 0.24958471649619796,
        "ci95_low": 38.33413025363065,
        "ci95_high": 39.30918153251012,
        "achieved_mde80_one_sided": 0.6205861231389023
      },
      "force_expected": {
        "n": 192,
        "mean": 38.833535477898174,
        "sd": 3.4506757485627517,
        "se": 0.24903107153985227,
        "ci95_low": 38.36032373886033,
        "ci95_high": 39.31283773297669,
        "achieved_mde80_one_sided": 0.6192094988732926
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.35217960786568,
        "ci95_high": 39.30771258773641,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.8331437511387,
        "sd": 3.4583472781152635,
        "se": 0.24958471649638214,
        "ci95_low": 38.35297049649,
        "ci95_high": 39.32527112048551,
        "achieved_mde80_one_sided": 0.6205861231393602
      },
      "force_expected": {
        "n": 192,
        "mean": 38.838705117993754,
        "sd": 3.452435730326889,
        "se": 0.24915808728301397,
        "ci95_low": 38.34379433203026,
        "ci95_high": 39.3230674547167,
        "achieved_mde80_one_sided": 0.6195253203255551
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.32649343013065,
        "ci95_high": 39.33085006974993,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.83314375114322,
        "sd": 3.458347278113541,
        "se": 0.24958471649625782,
        "ci95_low": 38.33991370118687,
        "ci95_high": 39.30625773251363,
        "achieved_mde80_one_sided": 0.6205861231390511
      },
      "force_expected": {
        "n": 192,
        "mean": 38.831935546979125,
        "sd": 3.464816110992558,
        "se": 0.25005156429676323,
        "ci95_low": 38.338018344687924,
        "ci95_high": 39.31731305465777,
        "achieved_mde80_one_sided": 0.6217469284586989
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.33549243009219,
        "ci95_high": 39.32330751885529,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.83314375114243,
        "sd": 3.458347278111813,
        "se": 0.24958471649613312,
        "ci95_low": 38.341652774748844,
        "ci95_high": 39.31356709134041,
        "achieved_mde80_one_sided": 0.6205861231387411
      },
      "force_expected": {
        "n": 192,
        "mean": 38.822866303902174,
        "sd": 3.459080077094501,
        "se": 0.24963760170737273,
        "ci95_low": 38.33597996509489,
        "ci95_high": 39.30573044385219,
        "achieved_mde80_one_sided": 0.6207176208869819
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.83314375114327,
        "sd": 3.4583472781121003,
        "se": 0.24958471649615385,
        "ci95_low": 38.34116683499867,
        "ci95_high": 39.319703553037805,
        "achieved_mde80_one_sided": 0.6205861231387927
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.83314375114243,
        "sd": 3.458347278111813,
        "se": 0.24958471649613312,
        "ci95_low": 38.34410973428355,
        "ci95_high": 39.313256290692934,
        "achieved_mde80_one_sided": 0.6205861231387411
      },
      "force_expected": {
        "n": 192,
        "mean": 38.83699286468924,
        "sd": 3.4590639030511485,
        "se": 0.2496364344463373,
        "ci95_low": 38.3458221879178,
        "ci95_high": 39.323345002589285,
        "achieved_mde80_one_sided": 0.6207147185217616
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 4.568789790937444e-12,
      "relative_range": 1.1765181362127262e-13,
      "cv": 3.985535600868344e-14
    }
  },
  "7": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.143269636346936,
        "ci95_high": 39.21221872658322,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.120362810590585,
        "ci95_high": 39.21800987480298,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "force_expected": {
        "n": 192,
        "mean": 38.68414820369393,
        "sd": 3.8133875284218655,
        "se": 0.2752075395073407,
        "ci95_low": 38.14626783128588,
        "ci95_high": 39.21685534527222,
        "achieved_mde80_one_sided": 0.6842966284117745
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.11970170791542,
        "ci95_high": 39.219773361564584,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.684592510344224,
        "sd": 3.8161407419209215,
        "se": 0.2754062355766928,
        "ci95_low": 38.14132162112856,
        "ci95_high": 39.215578789983525,
        "achieved_mde80_one_sided": 0.6847906811931035
      },
      "force_expected": {
        "n": 192,
        "mean": 38.68362419083441,
        "sd": 3.807066182241431,
        "se": 0.2747513356424764,
        "ci95_low": 38.14849317213206,
        "ci95_high": 39.20964906849001,
        "achieved_mde80_one_sided": 0.6831622889705153
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.1409902279726,
        "ci95_high": 39.21636561001422,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.68459251033996,
        "sd": 3.8161407419188023,
        "se": 0.27540623557653987,
        "ci95_low": 38.128364578592176,
        "ci95_high": 39.220969278714605,
        "achieved_mde80_one_sided": 0.6847906811927232
      },
      "force_expected": {
        "n": 192,
        "mean": 38.682156715888965,
        "sd": 3.808029105474863,
        "se": 0.27482082864098023,
        "ci95_low": 38.141760409544524,
        "ci95_high": 39.210665718995294,
        "achieved_mde80_one_sided": 0.6833350815642776
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.136093242153926,
        "ci95_high": 39.199361699485785,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.68459251034153,
        "sd": 3.8161407419202336,
        "se": 0.2754062355766431,
        "ci95_low": 38.13178168953573,
        "ci95_high": 39.19559336998578,
        "achieved_mde80_one_sided": 0.6847906811929799
      },
      "force_expected": {
        "n": 192,
        "mean": 38.680432385640295,
        "sd": 3.8154039998514246,
        "se": 0.2753530657976744,
        "ci95_low": 38.13068448146906,
        "ci95_high": 39.21422166355672,
        "achieved_mde80_one_sided": 0.6846584758742346
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.140596451726516,
        "ci95_high": 39.22756459508575,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.68459251034131,
        "sd": 3.816140741918534,
        "se": 0.2754062355765205,
        "ci95_low": 38.15087381968048,
        "ci95_high": 39.219881967325016,
        "achieved_mde80_one_sided": 0.684790681192675
      },
      "force_expected": {
        "n": 192,
        "mean": 38.67624935389522,
        "sd": 3.815793287552013,
        "se": 0.27538116021751524,
        "ci95_low": 38.142163687254275,
        "ci95_high": 39.20344347909728,
        "achieved_mde80_one_sided": 0.6847283319428898
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.68459251034189,
        "sd": 3.816140741917827,
        "se": 0.2754062355764695,
        "ci95_low": 38.145385644990576,
        "ci95_high": 39.21931643753111,
        "achieved_mde80_one_sided": 0.6847906811925483
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.68459251034131,
        "sd": 3.816140741918534,
        "se": 0.2754062355765205,
        "ci95_low": 38.129454196196384,
        "ci95_high": 39.21653800934013,
        "achieved_mde80_one_sided": 0.684790681192675
      },
      "force_expected": {
        "n": 192,
        "mean": 38.68870679535721,
        "sd": 3.816323911558063,
        "se": 0.27541945470660667,
        "ci95_low": 38.149154325012,
        "ci95_high": 39.22184498784777,
        "achieved_mde80_one_sided": 0.6848235502273123
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 4.263256414560601e-12,
      "relative_range": 1.1020554018814825e-13,
      "cv": 3.297694355008515e-14
    }
  },
  "8": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.50723783856079,
        "ci95_high": 39.4683108778284,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.50814097965832,
        "ci95_high": 39.44706819945625,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "force_expected": {
        "n": 192,
        "mean": 38.97904669832145,
        "sd": 3.3701467126067453,
        "se": 0.2432193889665046,
        "ci95_low": 38.51925719866005,
        "ci95_high": 39.447400088476456,
        "achieved_mde80_one_sided": 0.604758896257316
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.492585222301585,
        "ci95_high": 39.4515384663859,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.982000377594055,
        "sd": 3.3716312738339824,
        "se": 0.24332652794452633,
        "ci95_low": 38.51056837727989,
        "ci95_high": 39.45776264638846,
        "achieved_mde80_one_sided": 0.6050252946327493
      },
      "force_expected": {
        "n": 192,
        "mean": 38.986843808359886,
        "sd": 3.372442854909003,
        "se": 0.2433850987635429,
        "ci95_low": 38.507952208660676,
        "ci95_high": 39.47730667256424,
        "achieved_mde80_one_sided": 0.6051709295017943
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.52006638394291,
        "ci95_high": 39.456458305933985,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.982000377601274,
        "sd": 3.3716312738382834,
        "se": 0.24332652794483672,
        "ci95_low": 38.521491086495665,
        "ci95_high": 39.452495963765145,
        "achieved_mde80_one_sided": 0.6050252946335211
      },
      "force_expected": {
        "n": 192,
        "mean": 38.98421581029162,
        "sd": 3.373924064268665,
        "se": 0.24349199584135878,
        "ci95_low": 38.50659859225866,
        "ci95_high": 39.4555371394097,
        "achieved_mde80_one_sided": 0.605436726398447
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.50781384351147,
        "ci95_high": 39.451770547839644,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.982000377595966,
        "sd": 3.371631273833462,
        "se": 0.24332652794448878,
        "ci95_low": 38.51488566398172,
        "ci95_high": 39.455156972678225,
        "achieved_mde80_one_sided": 0.6050252946326559
      },
      "force_expected": {
        "n": 192,
        "mean": 38.97913747169471,
        "sd": 3.368350157576414,
        "se": 0.24308973377520765,
        "ci95_low": 38.5018197954597,
        "ci95_high": 39.44430559946758,
        "achieved_mde80_one_sided": 0.6044365118836197
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.509681132051746,
        "ci95_high": 39.4391022834288,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.9820003775968,
        "sd": 3.3716312738366847,
        "se": 0.24332652794472134,
        "ci95_low": 38.491897782815464,
        "ci95_high": 39.44363956156694,
        "achieved_mde80_one_sided": 0.6050252946332342
      },
      "force_expected": {
        "n": 192,
        "mean": 38.97065474998553,
        "sd": 3.3705941924956244,
        "se": 0.24325168304579228,
        "ci95_low": 38.49714716002303,
        "ci95_high": 39.4580399527464,
        "achieved_mde80_one_sided": 0.6048391946736086
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.982000377599825,
        "sd": 3.3716312738352743,
        "se": 0.24332652794461956,
        "ci95_low": 38.51932249860708,
        "ci95_high": 39.463185225969475,
        "achieved_mde80_one_sided": 0.6050252946329812
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.9820003775968,
        "sd": 3.3716312738366847,
        "se": 0.24332652794472134,
        "ci95_low": 38.49937563682313,
        "ci95_high": 39.458473300788285,
        "achieved_mde80_one_sided": 0.6050252946332342
      },
      "force_expected": {
        "n": 192,
        "mean": 38.98522884330153,
        "sd": 3.3713720671447334,
        "se": 0.24330782131304962,
        "ci95_low": 38.50618498438666,
        "ci95_high": 39.44674022849498,
        "achieved_mde80_one_sided": 0.6049787810638574
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 7.219114195322618e-12,
      "relative_range": 1.8519096314696481e-13,
      "cv": 6.181647954473002e-14
    }
  },
  "9": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.447760637069784,
        "ci95_high": 39.38833031019609,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.458716972774575,
        "ci95_high": 39.39424490946317,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "force_expected": {
        "n": 192,
        "mean": 38.92168594368522,
        "sd": 3.3433487564771114,
        "se": 0.24128541306835763,
        "ci95_low": 38.444501041862594,
        "ci95_high": 39.37150319911362,
        "achieved_mde80_one_sided": 0.5999501138057135
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.45818785034669,
        "ci95_high": 39.38926510789809,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.924157289921986,
        "sd": 3.3423083475982596,
        "se": 0.24121032802507356,
        "ci95_low": 38.433146228161135,
        "ci95_high": 39.39402355810377,
        "achieved_mde80_one_sided": 0.5997634167331862
      },
      "force_expected": {
        "n": 192,
        "mean": 38.92129017166638,
        "sd": 3.3433944866694443,
        "se": 0.2412887133607143,
        "ci95_low": 38.435677095722696,
        "ci95_high": 39.39528271548004,
        "achieved_mde80_one_sided": 0.5999583198996907
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.44161342663491,
        "ci95_high": 39.3862741914329,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.92415728991909,
        "sd": 3.3423083476046664,
        "se": 0.24121032802553594,
        "ci95_low": 38.44983806680376,
        "ci95_high": 39.39103067377419,
        "achieved_mde80_one_sided": 0.599763416734336
      },
      "force_expected": {
        "n": 192,
        "mean": 38.920457943867206,
        "sd": 3.3377161301029057,
        "se": 0.2408789132741836,
        "ci95_low": 38.43638015563467,
        "ci95_high": 39.389568825721106,
        "achieved_mde80_one_sided": 0.5989393622866914
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.458365256050726,
        "ci95_high": 39.38948007406936,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.92415728992345,
        "sd": 3.3423083475978124,
        "se": 0.2412103280250413,
        "ci95_low": 38.451974075391895,
        "ci95_high": 39.396500707325565,
        "achieved_mde80_one_sided": 0.5997634167331061
      },
      "force_expected": {
        "n": 192,
        "mean": 38.91842795870968,
        "sd": 3.34590152966929,
        "se": 0.24146964360456818,
        "ci95_low": 38.448680362349336,
        "ci95_high": 39.38400628083582,
        "achieved_mde80_one_sided": 0.6004081984025419
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.44014239810022,
        "ci95_high": 39.405230134357666,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.92415728991809,
        "sd": 3.3423083475984017,
        "se": 0.24121032802508383,
        "ci95_low": 38.446073279548116,
        "ci95_high": 39.37385880046326,
        "achieved_mde80_one_sided": 0.5997634167332118
      },
      "force_expected": {
        "n": 192,
        "mean": 38.91916281319144,
        "sd": 3.3342959154720737,
        "se": 0.24063208054445895,
        "ci95_low": 38.44716750153211,
        "ci95_high": 39.38591000221664,
        "achieved_mde80_one_sided": 0.5983256189094764
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.92415728992291,
        "sd": 3.3423083475967315,
        "se": 0.24121032802496328,
        "ci95_low": 38.44475744177133,
        "ci95_high": 39.39083248577485,
        "achieved_mde80_one_sided": 0.599763416732912
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.92415728991809,
        "sd": 3.3423083475984017,
        "se": 0.24121032802508383,
        "ci95_low": 38.439989476024955,
        "ci95_high": 39.38395388938218,
        "achieved_mde80_one_sided": 0.5997634167332118
      },
      "force_expected": {
        "n": 192,
        "mean": 38.92868652478983,
        "sd": 3.33851338129774,
        "se": 0.24093644992317725,
        "ci95_low": 38.463488762567124,
        "ci95_high": 39.397803438781516,
        "achieved_mde80_one_sided": 0.599082425717973
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 5.357492227631155e-12,
      "relative_range": 1.3763926056835854e-13,
      "cv": 5.767973695194343e-14
    }
  },
  "10": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.43149266371074,
        "ci95_high": 39.45362306810756,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.45388860040523,
        "ci95_high": 39.44346547052125,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "force_expected": {
        "n": 192,
        "mean": 38.94451653103737,
        "sd": 3.584785921505641,
        "se": 0.2587096395960578,
        "ci95_low": 38.43998360273646,
        "ci95_high": 39.436498326026,
        "achieved_mde80_one_sided": 0.6432750150309221
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.43321584679544,
        "ci95_high": 39.44891026833948,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.9462067138822,
        "sd": 3.584200468816325,
        "se": 0.258667388187586,
        "ci95_low": 38.45299105597175,
        "ci95_high": 39.45191646606168,
        "achieved_mde80_one_sided": 0.6431699579659352
      },
      "force_expected": {
        "n": 192,
        "mean": 38.94503103493225,
        "sd": 3.5925997610863414,
        "se": 0.25927355489422305,
        "ci95_low": 38.44371055101366,
        "ci95_high": 39.44068290345005,
        "achieved_mde80_one_sided": 0.644677176243275
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.445142600524875,
        "ci95_high": 39.448729054002946,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.94620671388771,
        "sd": 3.584200468817197,
        "se": 0.25866738818764895,
        "ci95_low": 38.441880627350244,
        "ci95_high": 39.446574643618696,
        "achieved_mde80_one_sided": 0.6431699579660917
      },
      "force_expected": {
        "n": 192,
        "mean": 38.941587792910106,
        "sd": 3.582692794517447,
        "se": 0.25855858116729763,
        "ci95_low": 38.42923366270975,
        "ci95_high": 39.43777378991427,
        "achieved_mde80_one_sided": 0.6428994120453396
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.43093448286595,
        "ci95_high": 39.44340107430298,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.94620671387611,
        "sd": 3.5842004688244997,
        "se": 0.258667388188176,
        "ci95_low": 38.43315197569117,
        "ci95_high": 39.43982191072163,
        "achieved_mde80_one_sided": 0.6431699579674022
      },
      "force_expected": {
        "n": 192,
        "mean": 38.93867796941021,
        "sd": 3.583305655497208,
        "se": 0.2586028105987527,
        "ci95_low": 38.43453904031948,
        "ci95_high": 39.456985617303275,
        "achieved_mde80_one_sided": 0.6430093874147479
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.44915628546326,
        "ci95_high": 39.443999146846025,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.9462067138889,
        "sd": 3.5842004688167464,
        "se": 0.2586673881876164,
        "ci95_low": 38.42539596559034,
        "ci95_high": 39.445641923216435,
        "achieved_mde80_one_sided": 0.6431699579660108
      },
      "force_expected": {
        "n": 192,
        "mean": 38.93930752674615,
        "sd": 3.5790233418069253,
        "se": 0.2582937612285228,
        "ci95_low": 38.43750776538729,
        "ci95_high": 39.44660755496369,
        "achieved_mde80_one_sided": 0.6422409439250104
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 38.94620671388322,
        "sd": 3.584200468819634,
        "se": 0.2586673881878248,
        "ci95_low": 38.44675205139479,
        "ci95_high": 39.44394273253802,
        "achieved_mde80_one_sided": 0.643169957966529
      },
      "prevent_expected": {
        "n": 192,
        "mean": 38.9462067138889,
        "sd": 3.5842004688167464,
        "se": 0.2586673881876164,
        "ci95_low": 38.44312062982938,
        "ci95_high": 39.455515359781955,
        "achieved_mde80_one_sided": 0.6431699579660108
      },
      "force_expected": {
        "n": 192,
        "mean": 38.951714287116125,
        "sd": 3.5828930089718605,
        "se": 0.2585730304009415,
        "ci95_low": 38.443368399265296,
        "ci95_high": 39.44516123186372,
        "achieved_mde80_one_sided": 0.6429353397015488
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 1.2789769243681803e-11,
      "relative_range": 3.283957623303578e-13,
      "cv": 1.1783082810547403e-13
    }
  },
  "11": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.55647921094624,
        "ci95_high": 39.4998673387528,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.55611711475305,
        "ci95_high": 39.51119004006241,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "force_expected": {
        "n": 192,
        "mean": 39.03136834484466,
        "sd": 3.3336546067438713,
        "se": 0.24058579807360128,
        "ci95_low": 38.55628138931249,
        "ci95_high": 39.49708553994215,
        "achieved_mde80_one_sided": 0.5982105387092059
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.546133418329056,
        "ci95_high": 39.5130579627872,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.033698827080634,
        "sd": 3.340200666304456,
        "se": 0.24105821922978063,
        "ci95_low": 38.555113180601445,
        "ci95_high": 39.49622805898979,
        "achieved_mde80_one_sided": 0.5993852020376257
      },
      "force_expected": {
        "n": 192,
        "mean": 39.03304497230554,
        "sd": 3.3434123510572,
        "se": 0.24129000261184927,
        "ci95_low": 38.578005240970136,
        "ci95_high": 39.50393980673616,
        "achieved_mde80_one_sided": 0.5999615255902268
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.582084354012466,
        "ci95_high": 39.51090106310351,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.033698827083704,
        "sd": 3.340200666301419,
        "se": 0.24105821922956147,
        "ci95_low": 38.55740001715423,
        "ci95_high": 39.507162639386785,
        "achieved_mde80_one_sided": 0.5993852020370808
      },
      "force_expected": {
        "n": 192,
        "mean": 39.026251834910596,
        "sd": 3.3365988500537216,
        "se": 0.240798280532039,
        "ci95_low": 38.54981820904739,
        "ci95_high": 39.50735837745071,
        "achieved_mde80_one_sided": 0.5987388710004137
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.55435618854,
        "ci95_high": 39.51055432619828,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.03369882708582,
        "sd": 3.3402006663053316,
        "se": 0.24105821922984383,
        "ci95_low": 38.54890771909549,
        "ci95_high": 39.50370931350051,
        "achieved_mde80_one_sided": 0.5993852020377829
      },
      "force_expected": {
        "n": 192,
        "mean": 39.028290952302534,
        "sd": 3.3399183385717226,
        "se": 0.24103784398071898,
        "ci95_low": 38.53960595808345,
        "ci95_high": 39.49903952141664,
        "achieved_mde80_one_sided": 0.599334539493057
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.555409019618395,
        "ci95_high": 39.51107183535639,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.03369882708241,
        "sd": 3.340200666306087,
        "se": 0.24105821922989834,
        "ci95_low": 38.57446900063467,
        "ci95_high": 39.50138454580324,
        "achieved_mde80_one_sided": 0.5993852020379185
      },
      "force_expected": {
        "n": 192,
        "mean": 39.026186729699475,
        "sd": 3.33815489225431,
        "se": 0.2409105782049615,
        "ci95_low": 38.56912985689242,
        "ci95_high": 39.494115865862845,
        "achieved_mde80_one_sided": 0.5990180963410309
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 39.033698827083796,
        "sd": 3.340200666304656,
        "se": 0.2410582192297951,
        "ci95_low": 38.572895248962276,
        "ci95_high": 39.495713962573056,
        "achieved_mde80_one_sided": 0.5993852020376617
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.03369882708241,
        "sd": 3.340200666306087,
        "se": 0.24105821922989834,
        "ci95_low": 38.57509014444787,
        "ci95_high": 39.497289790531056,
        "achieved_mde80_one_sided": 0.5993852020379185
      },
      "force_expected": {
        "n": 192,
        "mean": 39.03729549541115,
        "sd": 3.340559021087568,
        "se": 0.24108408125859251,
        "ci95_low": 38.56267982234989,
        "ci95_high": 39.51170376939744,
        "achieved_mde80_one_sided": 0.5994495073221087
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 5.186961971048731e-12,
      "relative_range": 1.3288420331433746e-13,
      "cv": 4.088289329385209e-14
    }
  },
  "12": {
    "f=0.10": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.692961122694214,
        "ci95_high": 39.76392422001522,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.70056131947473,
        "ci95_high": 39.77077411735398,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "force_expected": {
        "n": 192,
        "mean": 39.244458410015206,
        "sd": 3.8506346755453658,
        "se": 0.27789562080962804,
        "ci95_low": 38.70401083908164,
        "ci95_high": 39.78571322163662,
        "achieved_mde80_one_sided": 0.6909804749929577
      }
    },
    "f=0.25": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.70645488185714,
        "ci95_high": 39.75997840741789,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.23789346256285,
        "sd": 3.846322131157453,
        "se": 0.27758438972672134,
        "ci95_low": 38.69607785381532,
        "ci95_high": 39.769410730085454,
        "achieved_mde80_one_sided": 0.6902066067294963
      },
      "force_expected": {
        "n": 192,
        "mean": 39.23024197230953,
        "sd": 3.849230779160228,
        "se": 0.2777943033151438,
        "ci95_low": 38.70439085035072,
        "ci95_high": 39.76723454237778,
        "achieved_mde80_one_sided": 0.6907285515899912
      }
    },
    "f=0.50": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.69459022081426,
        "ci95_high": 39.77620546882593,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.237893462563434,
        "sd": 3.8463221311669518,
        "se": 0.27758438972740684,
        "ci95_low": 38.70512740138854,
        "ci95_high": 39.76372162339546,
        "achieved_mde80_one_sided": 0.6902066067312008
      },
      "force_expected": {
        "n": 192,
        "mean": 39.23612542459563,
        "sd": 3.8450562636170007,
        "se": 0.27749303360606653,
        "ci95_low": 38.69633008455718,
        "ci95_high": 39.766546755117254,
        "achieved_mde80_one_sided": 0.6899794520321331
      }
    },
    "f=0.75": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.6792838087249,
        "ci95_high": 39.762733560293356,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.23789346256739,
        "sd": 3.846322131169033,
        "se": 0.27758438972755706,
        "ci95_low": 38.6950625441661,
        "ci95_high": 39.787324470675046,
        "achieved_mde80_one_sided": 0.6902066067315743
      },
      "force_expected": {
        "n": 192,
        "mean": 39.234157993546,
        "sd": 3.850061291550144,
        "se": 0.27785424038412926,
        "ci95_low": 38.68196755143827,
        "ci95_high": 39.771704531668654,
        "achieved_mde80_one_sided": 0.6908775836052371
      }
    },
    "f=1.00": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.689014277959494,
        "ci95_high": 39.79471219418123,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.23789346256215,
        "sd": 3.846322131163933,
        "se": 0.27758438972718896,
        "ci95_low": 38.68024911968273,
        "ci95_high": 39.762114337842505,
        "achieved_mde80_one_sided": 0.690206606730659
      },
      "force_expected": {
        "n": 192,
        "mean": 39.234085278022185,
        "sd": 3.8438700085165873,
        "se": 0.2774074230183726,
        "ci95_low": 38.68102562363892,
        "ci95_high": 39.76678581709932,
        "achieved_mde80_one_sided": 0.6897665834580375
      }
    },
    "unbounded": {
      "target": {
        "n": 192,
        "mean": 39.23789346256653,
        "sd": 3.8463221311656794,
        "se": 0.27758438972731503,
        "ci95_low": 38.699467106587036,
        "ci95_high": 39.76609465097763,
        "achieved_mde80_one_sided": 0.6902066067309726
      },
      "prevent_expected": {
        "n": 192,
        "mean": 39.23789346256215,
        "sd": 3.846322131163933,
        "se": 0.27758438972718896,
        "ci95_low": 38.686701595614544,
        "ci95_high": 39.779630126077535,
        "achieved_mde80_one_sided": 0.690206606730659
      },
      "force_expected": {
        "n": 192,
        "mean": 39.24197932779648,
        "sd": 3.8485226170777223,
        "se": 0.27774319611902326,
        "ci95_low": 38.70738030178405,
        "ci95_high": 39.77690845110648,
        "achieved_mde80_one_sided": 0.6906014748316456
      }
    },
    "cross_arm_prevent_dispersion": {
      "range": 5.243805389909539e-12,
      "relative_range": 1.336413585737605e-13,
      "cv": 5.343101641637293e-14
    }
  }
}
```

---

## Stage 7 — Bounded Chapter 26 V2 Verdict

```json
{
  "validity": {
    "dynamic_rate_match": "PASS",
    "probe_coverage_fraction": 1.0,
    "scientific_valid": true
  },
  "primary_status": "BOUNDED_NEAR_ZERO",
  "overall_status": "CAUSAL_AMPLIFICATION_BOUNDED_NEAR_ZERO_AT_MATCHED_RATE",
  "bounded_claim": "At dynamically matched background expected construction rate, the strong-subsampling versus true-unbounded difference in finite-horizon transient causal amplification was bounded within the frozen +/-0.15 attachment equivalence region.",
  "what_this_does_not_establish": [
    "formal branching ratio",
    "subcriticality",
    "supercriticality",
    "criticality",
    "phase transition",
    "coherent structure",
    "individuality",
    "organism",
    "life"
  ],
  "stop_rule": "Do not alter SEI, horizon, probe geometry, fraction grid, reference policy or dynamic calibration to rescue the result.",
  "next_if_supported": "Map amplification across allocation concentration while retaining dynamic rate matching.",
  "next_if_bounded": "Close the finite-selection amplification question at this scale and treat finite-budget effects as redistribution rather than material amplification in the tested regime.",
  "next_if_unresolved": "Increase independent groups only if achieved MDE exceeds the frozen SEI."
}
```
