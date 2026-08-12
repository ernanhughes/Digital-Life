# Chapter 17 — How Does the Crystal Respond to Perturbation?

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-perturbation-dynamics-v5",
  "schema_version": 5,
  "chapter": 17,
  "chapter_title": "How Does the Crystal Respond to Perturbation?",
  "version_5_focus": "Randomness-coupling audit: preserve the canonical sequential-RNG substrate, add a separate cell-keyed CRN counterfactual runner, audit marginal compatibility, shorten the matched codewords, add a mean-estimation noise floor, and report paired ridge MDE curves.",
  "run_type": "EXPLORATORY",
  "profile": "quick",
  "profile_config": {
    "groups": 24,
    "radius": 64,
    "warmup_steps": 14,
    "horizon": 20,
    "pulse_step": 4,
    "message_gain": 0.65,
    "observation_steps": [
      1,
      2,
      4,
      5,
      6,
      8,
      10,
      12,
      16,
      20
    ],
    "matched_observation_steps": [
      8,
      9,
      10,
      12
    ],
    "bootstrap_reps": 500,
    "permutations": 500,
    "coupling_validation_groups": 48,
    "calibration_reps": 200,
    "calibration_permutations": 500,
    "mde_strengths": [
      0.0,
      0.25,
      0.5,
      0.75,
      1.0,
      1.25,
      1.5,
      2.0
    ],
    "mde_target_power": 0.8,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260812,
  "canonical_model_modified": false,
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
  "angular_subspace": [
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
  "scientific_boundary": "Perturbation-response and counterfactual-coupling characterization only. Chapter 18 information-survival remains deferred.",
  "started_at_unix": 1786534428.519806,
  "finished_at_unix": 1786534641.1956217,
  "reproducibility_passed": true,
  "marginal_compatibility_p_value": 0.9301397205588823,
  "final_status": "UNTESTED",
  "chapter18_status": "DEFERRED"
}
```

# Stage 0 — Canonical Sequential RNG vs Counterfactual CRN

```json
{
  "sequential_exact": true,
  "crn_exact": true,
  "canonical_runner": "sequential RNG over sorted(frontier)",
  "counterfactual_runner": "cell-keyed CRN U(seed, step, q, r)",
  "canonical_substrate_modified": false,
  "validation_groups_per_runner": 48,
  "marginal_feature_test": {
    "energy_distance": 0.2060020932718798,
    "p_value": 0.9301397205588823,
    "null_q95": 0.38643619995954437,
    "interpretation": "Failure to reject is compatibility evidence only; it does not prove equality of the two stochastic laws."
  },
  "population": {
    "sequential": {
      "n": 48,
      "mean": 1430.875,
      "median": 1431.5,
      "std": 99.73791175709799,
      "ci95_low": 1404.0057291666667,
      "ci95_high": 1461.825,
      "min": 1079.0,
      "max": 1652.0
    },
    "crn": {
      "n": 48,
      "mean": 1423.5,
      "median": 1428.0,
      "std": 92.0740191367793,
      "ci95_low": 1396.9333333333334,
      "ci95_high": 1448.6046875,
      "min": 1232.0,
      "max": 1598.0
    }
  }
}
```


# Stage 1 — Randomness Coupling Audit

```json
{
  "pulse_zero_index": 4,
  "pulse_elapsed_step": 5,
  "observation_steps": [
    1,
    2,
    4,
    5,
    6,
    8,
    10,
    12,
    16,
    20
  ],
  "summary": {
    "sequential_causal": {
      "1": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "2": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "4": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "5": {
        "symdiff": {
          "n": 24,
          "mean": 0.021705780573560585,
          "median": 0.021148808382850937,
          "std": 0.01305240978608022,
          "ci95_low": 0.016331675953317283,
          "ci95_high": 0.02750725195449474,
          "min": 0.0,
          "max": 0.05865921787709497
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.031660023757558,
          "median": 0.026185993239951195,
          "std": 0.01952142594641401,
          "ci95_low": 0.024214243102609466,
          "ci95_high": 0.03962451963689684,
          "min": 0.0,
          "max": 0.08495478577885675
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 3.125,
          "median": 3.0,
          "std": 2.587026929379231,
          "ci95_low": 2.1031250000000004,
          "ci95_high": 4.188541666666666,
          "min": 0.0,
          "max": 9.0
        }
      },
      "6": {
        "symdiff": {
          "n": 24,
          "mean": 0.07940188905630442,
          "median": 0.08378420932096645,
          "std": 0.026664052721290417,
          "ci95_low": 0.06896362533432732,
          "ci95_high": 0.0890471090890833,
          "min": 0.0,
          "max": 0.125
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.05055920836943323,
          "median": 0.04501031383564516,
          "std": 0.025008135192510487,
          "ci95_low": 0.041485019663391576,
          "ci95_high": 0.05958231623523603,
          "min": 0.0,
          "max": 0.1160193004099162
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 5.375,
          "median": 5.0,
          "std": 3.1598061649411346,
          "ci95_low": 4.25,
          "ci95_high": 6.666666666666667,
          "min": 0.0,
          "max": 13.0
        }
      },
      "8": {
        "symdiff": {
          "n": 24,
          "mean": 0.13372068038128698,
          "median": 0.13851509444729784,
          "std": 0.03137484373862834,
          "ci95_low": 0.12013515262383577,
          "ci95_high": 0.14449701655471459,
          "min": 0.0,
          "max": 0.1621212121212121
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.05766623222379271,
          "median": 0.05097193254266627,
          "std": 0.025823556222923833,
          "ci95_low": 0.047335606694156734,
          "ci95_high": 0.06864956222692417,
          "min": 0.0,
          "max": 0.1186545943615003
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 7.166666666666667,
          "median": 6.5,
          "std": 4.6338129248192805,
          "ci95_low": 5.311458333333333,
          "ci95_high": 9.146874999999998,
          "min": 0.0,
          "max": 14.0
        }
      },
      "10": {
        "symdiff": {
          "n": 24,
          "mean": 0.14509008265871673,
          "median": 0.15224745711144455,
          "std": 0.03314692221839135,
          "ci95_low": 0.12940484036046887,
          "ci95_high": 0.1555929587073021,
          "min": 0.0,
          "max": 0.17476851851851852
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.06012462673023311,
          "median": 0.05925568574320596,
          "std": 0.020899447432997733,
          "ci95_low": 0.052162679540811115,
          "ci95_high": 0.06930621727124336,
          "min": 0.0,
          "max": 0.11538140087540877
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 11.166666666666666,
          "median": 9.5,
          "std": 7.057305119913376,
          "ci95_low": 8.019791666666666,
          "ci95_high": 14.230208333333332,
          "min": 0.0,
          "max": 27.0
        }
      },
      "12": {
        "symdiff": {
          "n": 24,
          "mean": 0.14801030475527144,
          "median": 0.15278302272741578,
          "std": 0.033609714041286626,
          "ci95_low": 0.13234937397183671,
          "ci95_high": 0.1579528338979736,
          "min": 0.0,
          "max": 0.1796875
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.07092595557578642,
          "median": 0.07302050271126387,
          "std": 0.02432705987291392,
          "ci95_low": 0.0616085364760389,
          "ci95_high": 0.07967931365767324,
          "min": 0.0,
          "max": 0.12475205110936649
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 15.208333333333334,
          "median": 14.5,
          "std": 10.8319710681954,
          "ci95_low": 11.206249999999999,
          "ci95_high": 19.583333333333332,
          "min": 0.0,
          "max": 43.0
        }
      },
      "16": {
        "symdiff": {
          "n": 24,
          "mean": 0.15086888844279142,
          "median": 0.15573606122935862,
          "std": 0.035338506523868315,
          "ci95_low": 0.13351892844196464,
          "ci95_high": 0.16265666744885277,
          "min": 0.0,
          "max": 0.1980802792321117
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0723116659874259,
          "median": 0.07046726133394746,
          "std": 0.027296623013854788,
          "ci95_low": 0.06166024071723229,
          "ci95_high": 0.08244846596085348,
          "min": 0.0,
          "max": 0.14185322135278225
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 19.583333333333332,
          "median": 16.0,
          "std": 19.191831306284683,
          "ci95_low": 12.467708333333334,
          "ci95_high": 27.984374999999993,
          "min": 0.0,
          "max": 66.0
        }
      },
      "20": {
        "symdiff": {
          "n": 24,
          "mean": 0.144831677442239,
          "median": 0.15018745377962123,
          "std": 0.03553752814430171,
          "ci95_low": 0.12862262930651588,
          "ci95_high": 0.15643361981712145,
          "min": 0.0,
          "max": 0.1889655172413793
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.07267303598744874,
          "median": 0.07856780944772525,
          "std": 0.02666585900484059,
          "ci95_low": 0.062387360706951715,
          "ci95_high": 0.08271290881734256,
          "min": 0.0,
          "max": 0.11954391750229694
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 28.666666666666668,
          "median": 21.5,
          "std": 21.53614532722965,
          "ci95_low": 20.561458333333334,
          "ci95_high": 37.27812499999999,
          "min": 0.0,
          "max": 84.0
        }
      }
    },
    "crn_causal": {
      "1": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "2": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "4": {
        "symdiff": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 0.0,
          "median": 0.0,
          "std": 0.0,
          "ci95_low": 0.0,
          "ci95_high": 0.0,
          "min": 0.0,
          "max": 0.0
        }
      },
      "5": {
        "symdiff": {
          "n": 24,
          "mean": 0.02115916060008299,
          "median": 0.019119286510590857,
          "std": 0.010078474733728169,
          "ci95_low": 0.01728715781953737,
          "ci95_high": 0.02553620134352256,
          "min": 0.006622516556291391,
          "max": 0.044543429844097995
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.029040522292968024,
          "median": 0.026843034593505618,
          "std": 0.01389761577439255,
          "ci95_low": 0.023535989440479174,
          "ci95_high": 0.03406436789050914,
          "min": 0.009267617505653596,
          "max": 0.058398763496007436
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 3.625,
          "median": 4.0,
          "std": 1.653594569415369,
          "ci95_low": 3.0416666666666665,
          "ci95_high": 4.333333333333333,
          "min": 1.0,
          "max": 7.0
        }
      },
      "6": {
        "symdiff": {
          "n": 24,
          "mean": 0.02555003922164498,
          "median": 0.028398033286016994,
          "std": 0.012475044045163261,
          "ci95_low": 0.020432000800063105,
          "ci95_high": 0.0299957111139971,
          "min": 0.005940594059405941,
          "max": 0.047619047619047616
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.031192815226308096,
          "median": 0.026403591707712674,
          "std": 0.017177716677110298,
          "ci95_low": 0.024573979180409614,
          "ci95_high": 0.0386030132216787,
          "min": 0.006014323282119188,
          "max": 0.08411106556163124
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 4.416666666666667,
          "median": 3.0,
          "std": 3.510895738823483,
          "ci95_low": 3.2916666666666665,
          "ci95_high": 5.916666666666667,
          "min": 0.0,
          "max": 15.0
        }
      },
      "8": {
        "symdiff": {
          "n": 24,
          "mean": 0.026659918107908614,
          "median": 0.024794021843264992,
          "std": 0.013856556690386799,
          "ci95_low": 0.021435926885085894,
          "ci95_high": 0.032404584303672136,
          "min": 0.00398406374501992,
          "max": 0.05410122164048865
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0325877968915405,
          "median": 0.03164870305516685,
          "std": 0.01388231406423587,
          "ci95_low": 0.02774606802162395,
          "ci95_high": 0.038156606785239036,
          "min": 0.013126605567765258,
          "max": 0.06951030797768912
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 7.333333333333333,
          "median": 7.5,
          "std": 4.515405728048022,
          "ci95_low": 5.666666666666667,
          "ci95_high": 9.230208333333332,
          "min": 2.0,
          "max": 23.0
        }
      },
      "10": {
        "symdiff": {
          "n": 24,
          "mean": 0.02439550629403435,
          "median": 0.022076474622770917,
          "std": 0.013846919362123027,
          "ci95_low": 0.019565386178375117,
          "ci95_high": 0.030089600706398732,
          "min": 0.004573170731707317,
          "max": 0.06714285714285714
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.029654424087802247,
          "median": 0.0284821061226503,
          "std": 0.011336859404405394,
          "ci95_low": 0.025608741432803377,
          "ci95_high": 0.034597956308796425,
          "min": 0.011529394284558146,
          "max": 0.06362789403442418
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 9.208333333333334,
          "median": 8.5,
          "std": 5.8664240006630575,
          "ci95_low": 6.958333333333333,
          "ci95_high": 11.416666666666666,
          "min": 2.0,
          "max": 23.0
        }
      },
      "12": {
        "symdiff": {
          "n": 24,
          "mean": 0.02140043613237702,
          "median": 0.0198651268190133,
          "std": 0.013395133814109485,
          "ci95_low": 0.016064630577769808,
          "ci95_high": 0.027016240831343567,
          "min": 0.0028089887640449437,
          "max": 0.05748502994011976
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.029003795005862282,
          "median": 0.02926744069317261,
          "std": 0.012330831532040539,
          "ci95_low": 0.023935235972440797,
          "ci95_high": 0.03408279311744885,
          "min": 0.009704908567337873,
          "max": 0.050618401404665433
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 10.416666666666666,
          "median": 9.0,
          "std": 7.146774719332413,
          "ci95_low": 7.684375,
          "ci95_high": 13.5,
          "min": 2.0,
          "max": 28.0
        }
      },
      "16": {
        "symdiff": {
          "n": 24,
          "mean": 0.01945679185555997,
          "median": 0.014553475315026279,
          "std": 0.014574773278443526,
          "ci95_low": 0.014071719397003413,
          "ci95_high": 0.02564848060598179,
          "min": 0.0,
          "max": 0.048983364140480594
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.02706467425644868,
          "median": 0.024243678584307055,
          "std": 0.018775454100189732,
          "ci95_low": 0.019583201207016773,
          "ci95_high": 0.03382072875436154,
          "min": 0.0,
          "max": 0.07227112270757137
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 15.083333333333334,
          "median": 13.0,
          "std": 13.674540414783802,
          "ci95_low": 10.160416666666666,
          "ci95_high": 20.458333333333332,
          "min": 0.0,
          "max": 49.0
        }
      },
      "20": {
        "symdiff": {
          "n": 24,
          "mean": 0.01792165493210945,
          "median": 0.014909299342470733,
          "std": 0.014154972831344828,
          "ci95_low": 0.012685248492970178,
          "ci95_high": 0.023806464029686763,
          "min": 0.0,
          "max": 0.05452035886818495
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.022924058142378495,
          "median": 0.020714645235399523,
          "std": 0.016738390262082525,
          "ci95_low": 0.016615413175262987,
          "ci95_high": 0.02965079165957601,
          "min": 0.0,
          "max": 0.06869161610903127
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 16.416666666666668,
          "median": 10.5,
          "std": 17.046301325768262,
          "ci95_low": 9.997916666666667,
          "ci95_high": 24.129166666666663,
          "min": 0.0,
          "max": 75.0
        }
      }
    },
    "independent_reseed_reference": {
      "1": {
        "symdiff": {
          "n": 24,
          "mean": 0.13442289261340976,
          "median": 0.13124018838304552,
          "std": 0.016497385821309662,
          "ci95_low": 0.12790974532710234,
          "ci95_high": 0.1409425409881164,
          "min": 0.09774436090225563,
          "max": 0.17110266159695817
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.08908842562795961,
          "median": 0.08252336011960251,
          "std": 0.035634486189117236,
          "ci95_low": 0.07505380479809515,
          "ci95_high": 0.10380554135718284,
          "min": 0.03493512900457296,
          "max": 0.15593381110753762
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 4.333333333333333,
          "median": 3.5,
          "std": 3.8369548110737792,
          "ci95_low": 2.875,
          "ci95_high": 5.9187499999999975,
          "min": 0.0,
          "max": 12.0
        }
      },
      "2": {
        "symdiff": {
          "n": 24,
          "mean": 0.17600887058605177,
          "median": 0.1726266496381439,
          "std": 0.02176537104454852,
          "ci95_low": 0.16836657768195773,
          "ci95_high": 0.18533928431297034,
          "min": 0.13858695652173914,
          "max": 0.23873873873873874
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10728637360088528,
          "median": 0.09849686870925486,
          "std": 0.03657954720677054,
          "ci95_low": 0.09300905927490802,
          "ci95_high": 0.1218582834491085,
          "min": 0.0589699159108026,
          "max": 0.20628667122648897
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 8.291666666666666,
          "median": 8.0,
          "std": 5.630861143930138,
          "ci95_low": 6.208333333333333,
          "ci95_high": 10.629166666666663,
          "min": 0.0,
          "max": 23.0
        }
      },
      "4": {
        "symdiff": {
          "n": 24,
          "mean": 0.19378593772307848,
          "median": 0.1912059294871795,
          "std": 0.01646987657839084,
          "ci95_low": 0.18672663353275373,
          "ci95_high": 0.19935983530672632,
          "min": 0.16,
          "max": 0.22392638036809817
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.11372084841738513,
          "median": 0.09658639944898598,
          "std": 0.04154349489931071,
          "ci95_low": 0.09735258603551494,
          "ci95_high": 0.13076626160659893,
          "min": 0.06317358511690448,
          "max": 0.19099848136500217
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 12.708333333333334,
          "median": 11.0,
          "std": 8.080218472018906,
          "ci95_low": 9.894791666666666,
          "ci95_high": 15.75,
          "min": 0.0,
          "max": 32.0
        }
      },
      "5": {
        "symdiff": {
          "n": 24,
          "mean": 0.19401174585524772,
          "median": 0.19424694189602448,
          "std": 0.01512281746262575,
          "ci95_low": 0.18771893552966318,
          "ci95_high": 0.1995225772592948,
          "min": 0.16129032258064516,
          "max": 0.22554347826086957
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10693010597368598,
          "median": 0.09827644394060212,
          "std": 0.03387784809740449,
          "ci95_low": 0.09535692763249368,
          "ci95_high": 0.1210921786026379,
          "min": 0.045851099875328025,
          "max": 0.19428912561555114
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 14.416666666666666,
          "median": 12.0,
          "std": 9.737884210078127,
          "ci95_low": 10.853125,
          "ci95_high": 18.416666666666668,
          "min": 1.0,
          "max": 38.0
        }
      },
      "6": {
        "symdiff": {
          "n": 24,
          "mean": 0.19512114092165392,
          "median": 0.18896221031899424,
          "std": 0.019814994264443126,
          "ci95_low": 0.18813002919515476,
          "ci95_high": 0.20276605895628347,
          "min": 0.16089965397923875,
          "max": 0.22830188679245284
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10913562389195225,
          "median": 0.09961652886447077,
          "std": 0.043038951029476934,
          "ci95_low": 0.09448816041788252,
          "ci95_high": 0.12583251548486063,
          "min": 0.0616526448146784,
          "max": 0.2612279268687346
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 16.916666666666668,
          "median": 13.5,
          "std": 11.76476613546662,
          "ci95_low": 12.436458333333333,
          "ci95_high": 22.3375,
          "min": 0.0,
          "max": 46.0
        }
      },
      "8": {
        "symdiff": {
          "n": 24,
          "mean": 0.1900555136268495,
          "median": 0.18926893497321723,
          "std": 0.0220389449483813,
          "ci95_low": 0.18190190756775707,
          "ci95_high": 0.19883617759401645,
          "min": 0.14104372355430184,
          "max": 0.23709369024856597
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10982229817171436,
          "median": 0.10659858560211088,
          "std": 0.03389831767244462,
          "ci95_low": 0.09743227756024485,
          "ci95_high": 0.12467823274057493,
          "min": 0.06523499998197156,
          "max": 0.2028801074312369
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 21.083333333333332,
          "median": 14.5,
          "std": 15.895273581232324,
          "ci95_low": 14.995833333333334,
          "ci95_high": 27.375,
          "min": 3.0,
          "max": 62.0
        }
      },
      "10": {
        "symdiff": {
          "n": 24,
          "mean": 0.1885897264772188,
          "median": 0.18476809116809118,
          "std": 0.02255839231792809,
          "ci95_low": 0.17947218532200962,
          "ci95_high": 0.19762684476748607,
          "min": 0.1557377049180328,
          "max": 0.2434915773353752
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10683708986235818,
          "median": 0.101474083420586,
          "std": 0.03868920956710267,
          "ci95_low": 0.09256153880670395,
          "ci95_high": 0.1235734661023062,
          "min": 0.05063243722353842,
          "max": 0.20956951602509286
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 29.666666666666668,
          "median": 26.0,
          "std": 23.57552874392334,
          "ci95_low": 20.829166666666666,
          "ci95_high": 39.85520833333333,
          "min": 0.0,
          "max": 104.0
        }
      },
      "12": {
        "symdiff": {
          "n": 24,
          "mean": 0.18331942507789123,
          "median": 0.18376194149008146,
          "std": 0.02111409396259687,
          "ci95_low": 0.17458839359128256,
          "ci95_high": 0.19183994622378245,
          "min": 0.15132924335378323,
          "max": 0.22860791826309068
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.10403480462132597,
          "median": 0.09644343440867184,
          "std": 0.036176884634662926,
          "ci95_low": 0.09011174419997528,
          "ci95_high": 0.11814951417313119,
          "min": 0.051353604563649076,
          "max": 0.1852680226693603
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 36.041666666666664,
          "median": 30.5,
          "std": 30.45554022760975,
          "ci95_low": 25.622916666666665,
          "ci95_high": 48.988541666666656,
          "min": 1.0,
          "max": 123.0
        }
      },
      "16": {
        "symdiff": {
          "n": 24,
          "mean": 0.17862018414022754,
          "median": 0.17994477911646586,
          "std": 0.019413173044569368,
          "ci95_low": 0.1706743398630383,
          "ci95_high": 0.18694347197023073,
          "min": 0.1393188854489164,
          "max": 0.21319388576025744
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.09421198450932482,
          "median": 0.0957072607650909,
          "std": 0.03014635879649969,
          "ci95_low": 0.08109747312171778,
          "ci95_high": 0.10512442717697677,
          "min": 0.05514934167724088,
          "max": 0.15632969997101165
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 57.75,
          "median": 53.5,
          "std": 40.81998081005592,
          "ci95_low": 43.686458333333334,
          "ci95_high": 73.11562499999998,
          "min": 2.0,
          "max": 149.0
        }
      },
      "20": {
        "symdiff": {
          "n": 24,
          "mean": 0.1669903299805571,
          "median": 0.16262614545876347,
          "std": 0.021134546055494117,
          "ci95_low": 0.15894172080539481,
          "ci95_high": 0.17542000043319372,
          "min": 0.12761904761904763,
          "max": 0.22266401590457258
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.08949018945052001,
          "median": 0.08882092578307492,
          "std": 0.02762152575251219,
          "ci95_low": 0.07969412716552687,
          "ci95_high": 0.1012823567564377,
          "min": 0.04904670907547658,
          "max": 0.16224227169434507
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 72.95833333333333,
          "median": 54.0,
          "std": 53.05223775257322,
          "ci95_low": 51.202083333333334,
          "ci95_high": 94.23437499999999,
          "min": 1.0,
          "max": 200.0
        }
      }
    }
  },
  "ratios": {
    "1": {
      "sequential_to_independent": 0.0,
      "crn_to_independent": 0.0
    },
    "2": {
      "sequential_to_independent": 0.0,
      "crn_to_independent": 0.0
    },
    "4": {
      "sequential_to_independent": 0.0,
      "crn_to_independent": 0.0
    },
    "5": {
      "sequential_to_independent": 0.11187869310631987,
      "crn_to_independent": 0.10906123496187624
    },
    "6": {
      "sequential_to_independent": 0.40693637132936966,
      "crn_to_independent": 0.1309444947941544
    },
    "8": {
      "sequential_to_independent": 0.7035874825701243,
      "crn_to_independent": 0.1402743735193711
    },
    "10": {
      "sequential_to_independent": 0.7693424523644096,
      "crn_to_independent": 0.1293575570087126
    },
    "12": {
      "sequential_to_independent": 0.8073901862412171,
      "crn_to_independent": 0.11673850778925428
    },
    "16": {
      "sequential_to_independent": 0.8446351635398064,
      "crn_to_independent": 0.10892829357003252
    },
    "20": {
      "sequential_to_independent": 0.8673057742870616,
      "crn_to_independent": 0.10732151337263716
    }
  },
  "interpretation": "Pathwise divergence is compared under two declared couplings. A difference between them is evidence that pathwise counterfactual distance is coupling-dependent, not a coupling-invariant property."
}
```


# Stage 2 — CRN Superposition With Mean-Estimation Floor

```json
{
  "coupling": "cell-keyed CRN",
  "patterns_zero_indexed": {
    "clustered": [
      0,
      1,
      2,
      7
    ],
    "dispersed": [
      0,
      4,
      5,
      7
    ]
  },
  "summary": {
    "8": {
      "zero_response_population_mean_noise_floor": {
        "n": 500,
        "mean": 0.04518632890073799,
        "median": 0.043494880932385654,
        "std": 0.012966454781232303,
        "ci95_low": 0.04410653113894475,
        "ci95_high": 0.0462921631283189,
        "min": 0.01433600759124493,
        "max": 0.09983594534584443
      },
      "clustered": {
        "residual_norm": {
          "value": 0.007462343876518504,
          "bootstrap_ci95_low": 0.005400009121490107,
          "bootstrap_ci95_high": 0.018208046990984047
        },
        "actual_mean_delta_norm": {
          "value": 0.014817469615979954,
          "bootstrap_ci95_low": 0.00985928005718223,
          "bootstrap_ci95_high": 0.030546886000165707
        },
        "predicted_mean_delta_norm": {
          "value": 0.014401381616894257,
          "bootstrap_ci95_low": 0.012051697832372362,
          "bootstrap_ci95_high": 0.03231684653634328
        },
        "relative_superposition_error": {
          "value": 0.5036179637898979,
          "bootstrap_ci95_low": 0.22467106210547194,
          "bootstrap_ci95_high": 1.3932590104493878
        },
        "cosine_actual_vs_predicted": {
          "value": 0.8699261501746816,
          "bootstrap_ci95_low": 0.5531058970673092,
          "bootstrap_ci95_high": 0.9824773374916348
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.0068433829632679735,
          "bootstrap_ci95_low": 0.004635446333420294,
          "bootstrap_ci95_high": 0.01765188839531209
        },
        "actual_mean_delta_norm": {
          "value": 0.015220836011259283,
          "bootstrap_ci95_low": 0.010596114974501082,
          "bootstrap_ci95_high": 0.02612839134960347
        },
        "predicted_mean_delta_norm": {
          "value": 0.019325903742149562,
          "bootstrap_ci95_low": 0.014340135130325093,
          "bootstrap_ci95_high": 0.03240279447790045
        },
        "relative_superposition_error": {
          "value": 0.449606247528436,
          "bootstrap_ci95_low": 0.23807332277608886,
          "bootstrap_ci95_high": 1.001992729479272
        },
        "cosine_actual_vs_predicted": {
          "value": 0.9490401906578217,
          "bootstrap_ci95_low": 0.721553572465607,
          "bootstrap_ci95_high": 0.9889866888724659
        }
      }
    },
    "9": {
      "zero_response_population_mean_noise_floor": {
        "n": 500,
        "mean": 0.043764715479273575,
        "median": 0.04159227908268522,
        "std": 0.012790858056122685,
        "ci95_low": 0.042605507990769745,
        "ci95_high": 0.04472148366039348,
        "min": 0.01685078091027472,
        "max": 0.10348993206337871
      },
      "clustered": {
        "residual_norm": {
          "value": 0.007135404205570454,
          "bootstrap_ci95_low": 0.004207807868547402,
          "bootstrap_ci95_high": 0.01742101379764776
        },
        "actual_mean_delta_norm": {
          "value": 0.0135414127135121,
          "bootstrap_ci95_low": 0.009198035942990561,
          "bootstrap_ci95_high": 0.031018017268290485
        },
        "predicted_mean_delta_norm": {
          "value": 0.013230678659624453,
          "bootstrap_ci95_low": 0.011099486476233211,
          "bootstrap_ci95_high": 0.03275050820599165
        },
        "relative_superposition_error": {
          "value": 0.5269320385199172,
          "bootstrap_ci95_low": 0.22336029700708962,
          "bootstrap_ci95_high": 1.358364651134001
        },
        "cosine_actual_vs_predicted": {
          "value": 0.8581802648609835,
          "bootstrap_ci95_low": 0.505769941101529,
          "bootstrap_ci95_high": 0.9788671534229105
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.006952894492884378,
          "bootstrap_ci95_low": 0.004350261258053685,
          "bootstrap_ci95_high": 0.016155944743310148
        },
        "actual_mean_delta_norm": {
          "value": 0.01630644742617354,
          "bootstrap_ci95_low": 0.010432805643998979,
          "bootstrap_ci95_high": 0.030996055178583774
        },
        "predicted_mean_delta_norm": {
          "value": 0.022609314166280748,
          "bootstrap_ci95_low": 0.01411824653695299,
          "bootstrap_ci95_high": 0.04031451009624725
        },
        "relative_superposition_error": {
          "value": 0.4263892870818852,
          "bootstrap_ci95_low": 0.2279695268846287,
          "bootstrap_ci95_high": 0.9913017248411978
        },
        "cosine_actual_vs_predicted": {
          "value": 0.9883141627616628,
          "bootstrap_ci95_low": 0.8432227897595895,
          "bootstrap_ci95_high": 0.9911038178172261
        }
      }
    },
    "10": {
      "zero_response_population_mean_noise_floor": {
        "n": 500,
        "mean": 0.041290101624588016,
        "median": 0.04007144648541444,
        "std": 0.011334927861809289,
        "ci95_low": 0.04035718912736331,
        "ci95_high": 0.042448315512590234,
        "min": 0.016456348329332814,
        "max": 0.08384264333282809
      },
      "clustered": {
        "residual_norm": {
          "value": 0.007870776112344005,
          "bootstrap_ci95_low": 0.006051692226619798,
          "bootstrap_ci95_high": 0.01702395536294167
        },
        "actual_mean_delta_norm": {
          "value": 0.01250621028427185,
          "bootstrap_ci95_low": 0.007501892356296625,
          "bootstrap_ci95_high": 0.03173090572529293
        },
        "predicted_mean_delta_norm": {
          "value": 0.013417179190678082,
          "bootstrap_ci95_low": 0.009353913078226896,
          "bootstrap_ci95_high": 0.03567085679859265
        },
        "relative_superposition_error": {
          "value": 0.629349413886196,
          "bootstrap_ci95_low": 0.2950809687767889,
          "bootstrap_ci95_high": 1.5764273004231362
        },
        "cosine_actual_vs_predicted": {
          "value": 0.8178785539395239,
          "bootstrap_ci95_low": 0.3639133554562131,
          "bootstrap_ci95_high": 0.9685401334586683
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.008385561140272939,
          "bootstrap_ci95_low": 0.005041924483442233,
          "bootstrap_ci95_high": 0.01776857066555376
        },
        "actual_mean_delta_norm": {
          "value": 0.016212653513217618,
          "bootstrap_ci95_low": 0.01155860118400016,
          "bootstrap_ci95_high": 0.029195018501918368
        },
        "predicted_mean_delta_norm": {
          "value": 0.023746136855119067,
          "bootstrap_ci95_low": 0.015281445384129056,
          "bootstrap_ci95_high": 0.04166146437095977
        },
        "relative_superposition_error": {
          "value": 0.5172232376049041,
          "bootstrap_ci95_low": 0.26528723596885967,
          "bootstrap_ci95_high": 0.9580176823175142
        },
        "cosine_actual_vs_predicted": {
          "value": 0.9823835180816676,
          "bootstrap_ci95_low": 0.8664918141344827,
          "bootstrap_ci95_high": 0.9879411366526631
        }
      }
    },
    "12": {
      "zero_response_population_mean_noise_floor": {
        "n": 500,
        "mean": 0.03614461435197613,
        "median": 0.03531444582207117,
        "std": 0.009455218883905553,
        "ci95_low": 0.03536461183506213,
        "ci95_high": 0.03692631739969028,
        "min": 0.016110366774549776,
        "max": 0.06665633902590055
      },
      "clustered": {
        "residual_norm": {
          "value": 0.004332289075299454,
          "bootstrap_ci95_low": 0.003976414014684085,
          "bootstrap_ci95_high": 0.016053027321844576
        },
        "actual_mean_delta_norm": {
          "value": 0.014634852759995588,
          "bootstrap_ci95_low": 0.010066049342811053,
          "bootstrap_ci95_high": 0.027801835502587965
        },
        "predicted_mean_delta_norm": {
          "value": 0.014495551531400924,
          "bootstrap_ci95_low": 0.010554697226503349,
          "bootstrap_ci95_high": 0.03595555620873783
        },
        "relative_superposition_error": {
          "value": 0.29602546375743377,
          "bootstrap_ci95_low": 0.2173938640970399,
          "bootstrap_ci95_high": 1.045482388640808
        },
        "cosine_actual_vs_predicted": {
          "value": 0.9558091340297109,
          "bootstrap_ci95_low": 0.5677967552608859,
          "bootstrap_ci95_high": 0.986853032082482
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.009888983984264575,
          "bootstrap_ci95_low": 0.005352718005827541,
          "bootstrap_ci95_high": 0.019203575168922002
        },
        "actual_mean_delta_norm": {
          "value": 0.01726357772627148,
          "bootstrap_ci95_low": 0.010785864933112605,
          "bootstrap_ci95_high": 0.028083901460371322
        },
        "predicted_mean_delta_norm": {
          "value": 0.02584282057710193,
          "bootstrap_ci95_low": 0.0174163248100038,
          "bootstrap_ci95_high": 0.03956650192920246
        },
        "relative_superposition_error": {
          "value": 0.5728235561053867,
          "bootstrap_ci95_low": 0.22900883309779918,
          "bootstrap_ci95_high": 1.293790241773331
        },
        "cosine_actual_vs_predicted": {
          "value": 0.9728912211464081,
          "bootstrap_ci95_low": 0.8142149620007787,
          "bootstrap_ci95_high": 0.9896097511259526
        }
      }
    }
  },
  "interpretation": "Superposition residuals are compared with a finite-sample baseline mean-difference floor before being described as non-additivity."
}
```


# Stage 3 — Short Matched Timing Under Sequential RNG and CRN

```json
{
  "codeword_A": "11100001",
  "codeword_B": "10001101",
  "pulse_positions_A_zero_indexed": [
    0,
    1,
    2,
    7
  ],
  "pulse_positions_B_zero_indexed": [
    0,
    4,
    5,
    7
  ],
  "codeword_invariants": {
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
  "last_pulse_elapsed_step": 8,
  "observation_steps": [
    8,
    9,
    10,
    12
  ],
  "angular_subspace": {
    "basis": "mechanism-derived before v5 data",
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
    ]
  },
  "results": {
    "sequential": {
      "8": {
        "steps_since_last_pulse": 0,
        "symdiff": {
          "n": 24,
          "mean": 0.16719929823866306,
          "median": 0.1642813330607238,
          "std": 0.017278094399511973,
          "ci95_low": 0.16116023597504903,
          "ci95_high": 0.17348038952296949,
          "min": 0.1378809869375907,
          "max": 0.2076923076923077
        },
        "ridge_all24": {
          "statistic": 1.1379361022522057,
          "p_value": 0.21956087824351297,
          "null_q95": 1.767071341802788,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.15953994681915026,
          "p_value": 0.8642714570858283,
          "null_q95": 0.7507782674230847,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 11,
            "feature_name": "degree_2",
            "mean_standardized_delta_A_minus_B": 0.9223326485630036
          },
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": -0.6787400132900204
          },
          {
            "feature_index": 10,
            "feature_name": "degree_1",
            "mean_standardized_delta_A_minus_B": -0.30796610837031296
          },
          {
            "feature_index": 17,
            "feature_name": "sector_1",
            "mean_standardized_delta_A_minus_B": -0.17747935507049054
          },
          {
            "feature_index": 5,
            "feature_name": "centroid_y_scaled",
            "mean_standardized_delta_A_minus_B": 0.1472679219120659
          },
          {
            "feature_index": 9,
            "feature_name": "mean_degree",
            "mean_standardized_delta_A_minus_B": -0.12963955138886585
          }
        ]
      },
      "9": {
        "steps_since_last_pulse": 1,
        "symdiff": {
          "n": 24,
          "mean": 0.16951304512333176,
          "median": 0.17108505826394732,
          "std": 0.018040937720880508,
          "ci95_low": 0.16230542879077162,
          "ci95_high": 0.17716267062223118,
          "min": 0.13009198423127463,
          "max": 0.19681620839363242
        },
        "ridge_all24": {
          "statistic": 0.37289340423914963,
          "p_value": 0.9580838323353293,
          "null_q95": 1.6811891251675273,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.11521847172464902,
          "p_value": 0.9401197604790419,
          "null_q95": 0.8049299212544716,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 14,
            "feature_name": "degree_5",
            "mean_standardized_delta_A_minus_B": 0.39547338060951254
          },
          {
            "feature_index": 9,
            "feature_name": "mean_degree",
            "mean_standardized_delta_A_minus_B": -0.2463696997972168
          },
          {
            "feature_index": 10,
            "feature_name": "degree_1",
            "mean_standardized_delta_A_minus_B": 0.23451356971075024
          },
          {
            "feature_index": 8,
            "feature_name": "boundary_fraction",
            "mean_standardized_delta_A_minus_B": 0.23366487007415238
          },
          {
            "feature_index": 15,
            "feature_name": "degree_6",
            "mean_standardized_delta_A_minus_B": -0.23366487007415107
          },
          {
            "feature_index": 11,
            "feature_name": "degree_2",
            "mean_standardized_delta_A_minus_B": 0.22288493853301375
          }
        ]
      },
      "10": {
        "steps_since_last_pulse": 2,
        "symdiff": {
          "n": 24,
          "mean": 0.16990522704428415,
          "median": 0.16757289143698073,
          "std": 0.019030693950313878,
          "ci95_low": 0.16262811820753412,
          "ci95_high": 0.1778240011657909,
          "min": 0.13080684596577016,
          "max": 0.20504731861198738
        },
        "ridge_all24": {
          "statistic": 0.5023131758842763,
          "p_value": 0.8423153692614771,
          "null_q95": 1.547146528335512,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.15799382442499832,
          "p_value": 0.8762475049900199,
          "null_q95": 0.6641644603410422,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": 0.6167179321194763
          },
          {
            "feature_index": 13,
            "feature_name": "degree_4",
            "mean_standardized_delta_A_minus_B": -0.28284216685164626
          },
          {
            "feature_index": 10,
            "feature_name": "degree_1",
            "mean_standardized_delta_A_minus_B": -0.2750998845844215
          },
          {
            "feature_index": 17,
            "feature_name": "sector_1",
            "mean_standardized_delta_A_minus_B": -0.18459432451383243
          },
          {
            "feature_index": 22,
            "feature_name": "harmonic6_cos",
            "mean_standardized_delta_A_minus_B": 0.17339990230689936
          },
          {
            "feature_index": 11,
            "feature_name": "degree_2",
            "mean_standardized_delta_A_minus_B": 0.13952110249763905
          }
        ]
      },
      "12": {
        "steps_since_last_pulse": 4,
        "symdiff": {
          "n": 24,
          "mean": 0.17475408456286998,
          "median": 0.17593888980398614,
          "std": 0.017012594241146116,
          "ci95_low": 0.16848483460476507,
          "ci95_high": 0.1813287144633646,
          "min": 0.14332247557003258,
          "max": 0.20662100456621005
        },
        "ridge_all24": {
          "statistic": 0.42794353978755345,
          "p_value": 0.9301397205588823,
          "null_q95": 1.736698914269882,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.23720857106855134,
          "p_value": 0.688622754491018,
          "null_q95": 0.7584964331164874,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 13,
            "feature_name": "degree_4",
            "mean_standardized_delta_A_minus_B": 0.29968031057029604
          },
          {
            "feature_index": 4,
            "feature_name": "centroid_x_scaled",
            "mean_standardized_delta_A_minus_B": -0.2593961559202746
          },
          {
            "feature_index": 16,
            "feature_name": "sector_0",
            "mean_standardized_delta_A_minus_B": 0.25429188592650026
          },
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": -0.24185114506852345
          },
          {
            "feature_index": 23,
            "feature_name": "harmonic6_sin",
            "mean_standardized_delta_A_minus_B": 0.17902370509499702
          },
          {
            "feature_index": 1,
            "feature_name": "max_radius_fraction",
            "mean_standardized_delta_A_minus_B": 0.16384638410380806
          }
        ]
      }
    },
    "crn": {
      "8": {
        "steps_since_last_pulse": 0,
        "symdiff": {
          "n": 24,
          "mean": 0.06000690611492588,
          "median": 0.0599886851038076,
          "std": 0.027254917525942193,
          "ci95_low": 0.049304093367581216,
          "ci95_high": 0.06971549944499034,
          "min": 0.012216404886561954,
          "max": 0.12581699346405228
        },
        "ridge_all24": {
          "statistic": 0.5694318645602444,
          "p_value": 0.656686626746507,
          "null_q95": 1.3060511370962216,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.06376911590113155,
          "p_value": 0.9860279441117764,
          "null_q95": 0.6885936073861416,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 10,
            "feature_name": "degree_1",
            "mean_standardized_delta_A_minus_B": -0.2990452001876169
          },
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": -0.28321375521373926
          },
          {
            "feature_index": 9,
            "feature_name": "mean_degree",
            "mean_standardized_delta_A_minus_B": 0.2356792170334242
          },
          {
            "feature_index": 1,
            "feature_name": "max_radius_fraction",
            "mean_standardized_delta_A_minus_B": -0.20348923188911994
          },
          {
            "feature_index": 15,
            "feature_name": "degree_6",
            "mean_standardized_delta_A_minus_B": 0.1272874765185327
          },
          {
            "feature_index": 8,
            "feature_name": "boundary_fraction",
            "mean_standardized_delta_A_minus_B": -0.12728747651853253
          }
        ]
      },
      "9": {
        "steps_since_last_pulse": 1,
        "symdiff": {
          "n": 24,
          "mean": 0.05799848879974164,
          "median": 0.05262842759792491,
          "std": 0.03119211698735732,
          "ci95_low": 0.04724044777126201,
          "ci95_high": 0.07105481325460121,
          "min": 0.0064,
          "max": 0.13037037037037036
        },
        "ridge_all24": {
          "statistic": 0.6582837305537967,
          "p_value": 0.6027944111776448,
          "null_q95": 1.3250794778650958,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.11051447445748348,
          "p_value": 0.9660678642714571,
          "null_q95": 0.730394922313651,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": 0.3734610259582662
          },
          {
            "feature_index": 11,
            "feature_name": "degree_2",
            "mean_standardized_delta_A_minus_B": -0.34768601565985063
          },
          {
            "feature_index": 1,
            "feature_name": "max_radius_fraction",
            "mean_standardized_delta_A_minus_B": -0.24194335156365354
          },
          {
            "feature_index": 9,
            "feature_name": "mean_degree",
            "mean_standardized_delta_A_minus_B": 0.16160571647004138
          },
          {
            "feature_index": 22,
            "feature_name": "harmonic6_cos",
            "mean_standardized_delta_A_minus_B": -0.14073001522712938
          },
          {
            "feature_index": 14,
            "feature_name": "degree_5",
            "mean_standardized_delta_A_minus_B": -0.13870369984760997
          }
        ]
      },
      "10": {
        "steps_since_last_pulse": 2,
        "symdiff": {
          "n": 24,
          "mean": 0.05481352389709728,
          "median": 0.05508532462062135,
          "std": 0.032300211385991706,
          "ci95_low": 0.04298029763865749,
          "ci95_high": 0.06780199781835404,
          "min": 0.00583941605839416,
          "max": 0.13829787234042554
        },
        "ridge_all24": {
          "statistic": 0.6151665547963838,
          "p_value": 0.6666666666666666,
          "null_q95": 1.4309237466912799,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.06899158362261912,
          "p_value": 0.9880239520958084,
          "null_q95": 0.656886125481105,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 1,
            "feature_name": "max_radius_fraction",
            "mean_standardized_delta_A_minus_B": -0.2508726030021273
          },
          {
            "feature_index": 14,
            "feature_name": "degree_5",
            "mean_standardized_delta_A_minus_B": -0.2462375632709286
          },
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": -0.1991086390390477
          },
          {
            "feature_index": 15,
            "feature_name": "degree_6",
            "mean_standardized_delta_A_minus_B": 0.16035854047928666
          },
          {
            "feature_index": 8,
            "feature_name": "boundary_fraction",
            "mean_standardized_delta_A_minus_B": -0.160358540479286
          },
          {
            "feature_index": 22,
            "feature_name": "harmonic6_cos",
            "mean_standardized_delta_A_minus_B": -0.14192217465175141
          }
        ]
      },
      "12": {
        "steps_since_last_pulse": 4,
        "symdiff": {
          "n": 24,
          "mean": 0.05332187399025767,
          "median": 0.046025021460591994,
          "std": 0.03590999923620204,
          "ci95_low": 0.03907842051774997,
          "ci95_high": 0.0657788088968141,
          "min": 0.0,
          "max": 0.1425462459194777
        },
        "ridge_all24": {
          "statistic": 0.825673504796549,
          "p_value": 0.43912175648702595,
          "null_q95": 1.5550532300789532,
          "permutations": 500
        },
        "ridge_angular9": {
          "statistic": 0.17073672452098523,
          "p_value": 0.8502994011976048,
          "null_q95": 0.6960901740069352,
          "permutations": 500
        },
        "top_directional_features": [
          {
            "feature_index": 1,
            "feature_name": "max_radius_fraction",
            "mean_standardized_delta_A_minus_B": -0.35416880166057313
          },
          {
            "feature_index": 12,
            "feature_name": "degree_3",
            "mean_standardized_delta_A_minus_B": -0.22236964712569218
          },
          {
            "feature_index": 11,
            "feature_name": "degree_2",
            "mean_standardized_delta_A_minus_B": 0.16642942867358268
          },
          {
            "feature_index": 22,
            "feature_name": "harmonic6_cos",
            "mean_standardized_delta_A_minus_B": -0.15242228559428592
          },
          {
            "feature_index": 20,
            "feature_name": "sector_4",
            "mean_standardized_delta_A_minus_B": 0.12047264958157539
          },
          {
            "feature_index": 6,
            "feature_name": "cov_trace_scaled",
            "mean_standardized_delta_A_minus_B": -0.11949567442039226
          }
        ]
      }
    }
  },
  "scientific_status": "EXPLORATORY ONLY"
}
```


# Stages 4–5 — End-to-End Paired Sham and MDE Calibration

```json
{
  "endpoint": 8,
  "calibration_role": "EXPLORATORY INSTRUMENT DEVELOPMENT",
  "noise_model": "centered + sign-symmetrized CRN matched-pair deltas from this v5 pilot; therefore this same pilot is not confirmatory evidence",
  "calibration_reps": 200,
  "permutations_per_test": 500,
  "instruments": {
    "ridge_all24": {
      "feature_names": [
        "population_fraction",
        "max_radius_fraction",
        "mean_radius_fraction",
        "std_radius_fraction",
        "centroid_x_scaled",
        "centroid_y_scaled",
        "cov_trace_scaled",
        "cov_anisotropy",
        "boundary_fraction",
        "mean_degree",
        "degree_1",
        "degree_2",
        "degree_3",
        "degree_4",
        "degree_5",
        "degree_6",
        "sector_0",
        "sector_1",
        "sector_2",
        "sector_3",
        "sector_4",
        "sector_5",
        "harmonic6_cos",
        "harmonic6_sin"
      ],
      "null_fpr": 0.045,
      "target_power": 0.8,
      "mde80_grid_estimate": 0.5,
      "power_curve": [
        {
          "shift_norm": 0.0,
          "detection_rate_alpha_0_05": 0.045,
          "mean_p_value": 0.4846906187624751
        },
        {
          "shift_norm": 0.25,
          "detection_rate_alpha_0_05": 0.43,
          "mean_p_value": 0.07527944111776447
        },
        {
          "shift_norm": 0.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.002634730538922156
        },
        {
          "shift_norm": 0.75,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.25,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 2.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        }
      ]
    },
    "ridge_angular9": {
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
      "null_fpr": 0.085,
      "target_power": 0.8,
      "mde80_grid_estimate": 0.25,
      "power_curve": [
        {
          "shift_norm": 0.0,
          "detection_rate_alpha_0_05": 0.085,
          "mean_p_value": 0.5013872255489022
        },
        {
          "shift_norm": 0.25,
          "detection_rate_alpha_0_05": 0.995,
          "mean_p_value": 0.006806387225548902
        },
        {
          "shift_norm": 0.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 0.75,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.25,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 2.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        }
      ]
    }
  },
  "interpretation": "MDE grid values describe instrument resolution for the declared synthetic direction. They are not upper bounds on the real effect."
}
```


# Stage 6 — Bounded V5 Verdict

```json
{
  "experiment_role": "EXPLORATORY / RANDOMNESS-COUPLING AUDIT",
  "canonical_substrate_modified": false,
  "crn_is_separate_counterfactual_runner": true,
  "marginal_compatibility_not_rejected_at_0_05": true,
  "marginal_compatibility_p_value": 0.9301397205588823,
  "short_codeword_first_observation": 8,
  "short_codeword_sequential_symdiff_mean": 0.16719929823866306,
  "short_codeword_crn_symdiff_mean": 0.06000690611492588,
  "matched_arrangement_status": "UNTESTED",
  "chapter18_status": "DEFERRED",
  "bounded_statement": "V5 audits how randomness coupling changes pathwise perturbation response. The short matched-arrangement experiment remains an exploratory instrument-development pilot, not a memory or information-survival claim.",
  "decision_logic": {
    "if_crn_marginals_disagree": "Do not use CRN as a variance-reduction coupling until the marginal discrepancy is understood.",
    "if_crn_marginals_compatible_and_coherence_improves": "Freeze the CRN runner, short codewords, observation schedule and chosen ridge instrument; choose N from MDE/power curves before a new-seed confirmatory run.",
    "if_crn_does_not_improve_coherence": "Treat rapid decorrelation as robust to coupling choice and reconsider temporal-arrangement recoverability."
  },
  "nonclaims": [
    "memory",
    "information storage",
    "sender-specific signalling",
    "semantics",
    "Shannon channel capacity",
    "life"
  ]
}
```
