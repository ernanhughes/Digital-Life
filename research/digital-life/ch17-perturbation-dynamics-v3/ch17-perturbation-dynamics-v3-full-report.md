# Chapter 17 — How Does the Crystal Respond to Perturbation?

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-perturbation-dynamics-v3",
  "schema_version": 3,
  "chapter": 17,
  "chapter_title": "How Does the Crystal Respond to Perturbation?",
  "version_3_focus": "Measurement resolution: compare paired and marginal instruments using synthetic known-null/known-effect calibration before judging matched temporal arrangement.",
  "run_type": "EXPLORATORY",
  "profile": "quick",
  "profile_config": {
    "groups": 24,
    "radius": 64,
    "warmup_steps": 14,
    "horizon": 32,
    "pulse_step": 4,
    "message_gain": 0.65,
    "observation_steps": [
      1,
      2,
      4,
      6,
      8,
      12,
      16,
      20,
      24,
      32
    ],
    "matched_observation_steps": [
      16,
      18,
      20,
      24,
      28,
      32
    ],
    "permutations": 250,
    "bootstrap_reps": 500,
    "sham_reps": 20,
    "spike_in_reps": 100,
    "spike_in_strengths": [
      0.0,
      0.25,
      0.5,
      0.75,
      1.0,
      1.5,
      2.0
    ],
    "sensitivity_target_sd": 1.0,
    "sensitivity_target_power": 0.8,
    "instrument_calibration_reps": 40,
    "instrument_calibration_permutations": 100,
    "instrument_null_fpr_max": 0.1,
    "instrument_target_power": 0.8,
    "instrument_target_shift_norm": 1.0,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260812,
  "matched_codeword_A": "1110000000000001",
  "matched_codeword_B": "1000000110000001",
  "scientific_boundary": "Perturbation-response characterization only. The old information-survival question is deferred to Chapter 18.",
  "started_at_unix": 1786530856.4261742,
  "finished_at_unix": 1786530912.7392714,
  "reproducibility_passed": true,
  "final_status": "UNTESTED",
  "measurement_ready": false,
  "selected_instrument": null,
  "primary_matched_endpoint": 20
}
```

# Stage 0 — Freeze the Substrate

```json
{
  "canonical_rng_traversal": "sorted(frontier)",
  "exact": true,
  "hash_a": "5fd54c923adbc247272c7ada",
  "hash_b": "5fd54c923adbc247272c7ada"
}
```


# Stage 1 — One Pulse, and the Background Divergence Scale

The pulse effect is measured against an exact matched continuation,
and separately compared with the spread of independent no-pulse stochastic forks.

```json
{
  "pulse_zero_index": 4,
  "pulse_elapsed_step": 5,
  "message_gain": 0.65,
  "groups": 24,
  "observation_steps": [
    1,
    2,
    4,
    5,
    6,
    8,
    12,
    16,
    20,
    24,
    32
  ],
  "max_capacity_fraction_observed": 0.24813716849611409,
  "exact_causal_fork": {
    "1": {
      "population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
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
      }
    },
    "2": {
      "population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
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
      }
    },
    "4": {
      "population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
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
      }
    },
    "5": {
      "population_delta": {
        "n": 24,
        "mean": 3.6666666666666665,
        "median": 3.5,
        "std": 2.852873794770615,
        "ci95_low": 2.5416666666666665,
        "ci95_high": 4.791666666666667,
        "min": -3.0,
        "max": 9.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 4.083333333333333,
        "median": 3.5,
        "std": 2.2157893000513886,
        "ci95_low": 3.2281250000000004,
        "ci95_high": 5.041666666666667,
        "min": 0.0,
        "max": 9.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.016157838252217806,
        "median": 0.013351349038845474,
        "std": 0.008973889868871928,
        "ci95_low": 0.012868706452723309,
        "ci95_high": 0.01972848339411866,
        "min": 0.004073319755600814,
        "max": 0.04025423728813559
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.026820487289267916,
        "median": 0.024977497364911106,
        "std": 0.012431515191164866,
        "ci95_low": 0.02229270282821569,
        "ci95_high": 0.0317687912963677,
        "min": 0.009657149388112612,
        "max": 0.05748886191975701
      }
    },
    "6": {
      "population_delta": {
        "n": 24,
        "mean": 2.7083333333333335,
        "median": 3.5,
        "std": 5.247850088898839,
        "ci95_low": 0.625,
        "ci95_high": 4.458333333333333,
        "min": -7.0,
        "max": 11.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 4.958333333333333,
        "median": 4.5,
        "std": 3.2077921621507146,
        "ci95_low": 3.7083333333333335,
        "ci95_high": 6.105208333333333,
        "min": 0.0,
        "max": 11.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.07109049693964477,
        "median": 0.07541967258601553,
        "std": 0.029253036117478728,
        "ci95_low": 0.059062188100858136,
        "ci95_high": 0.0844835523809047,
        "min": 0.012170385395537525,
        "max": 0.12080536912751678
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.04133515561367376,
        "median": 0.03877962275559663,
        "std": 0.019488405595233467,
        "ci95_low": 0.03308897975419233,
        "ci95_high": 0.049304897727986345,
        "min": 0.009439131013793333,
        "max": 0.09443566390619593
      }
    },
    "8": {
      "population_delta": {
        "n": 24,
        "mean": 2.9166666666666665,
        "median": 2.0,
        "std": 7.889426820470265,
        "ci95_low": 0.1447916666666667,
        "ci95_high": 6.541666666666667,
        "min": -11.0,
        "max": 18.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 6.416666666666667,
        "median": 4.5,
        "std": 5.438417866336577,
        "ci95_low": 4.375,
        "ci95_high": 8.855208333333332,
        "min": 1.0,
        "max": 18.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.13215110342206302,
        "median": 0.12833524006347566,
        "std": 0.01972492440346995,
        "ci95_low": 0.12416028362481997,
        "ci95_high": 0.14037578481642546,
        "min": 0.09149277688603531,
        "max": 0.1724137931034483
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.05367048814050965,
        "median": 0.048458031186609636,
        "std": 0.012863489182283003,
        "ci95_low": 0.048690901696020604,
        "ci95_high": 0.05886381663956151,
        "min": 0.0337351931454601,
        "max": 0.08019324841709108
      }
    },
    "12": {
      "population_delta": {
        "n": 24,
        "mean": 2.2083333333333335,
        "median": -0.5,
        "std": 21.737025184897977,
        "ci95_low": -6.004166666666666,
        "ci95_high": 11.087499999999995,
        "min": -48.0,
        "max": 41.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 17.625,
        "median": 14.0,
        "std": 12.912566553555493,
        "ci95_low": 12.702083333333334,
        "ci95_high": 22.75,
        "min": 0.0,
        "max": 48.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1515875680323273,
        "median": 0.14934440316533354,
        "std": 0.015592125869166125,
        "ci95_low": 0.14569368286262463,
        "ci95_high": 0.1578635853555856,
        "min": 0.12049433573635428,
        "max": 0.1776061776061776
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.0642876435471522,
        "median": 0.06358037237516952,
        "std": 0.015176424988512245,
        "ci95_low": 0.05821680739389017,
        "ci95_high": 0.07113150363342201,
        "min": 0.04007797187273533,
        "max": 0.10451019273843064
      }
    },
    "16": {
      "population_delta": {
        "n": 24,
        "mean": -4.416666666666667,
        "median": -11.0,
        "std": 34.35830402618202,
        "ci95_low": -18.924999999999997,
        "ci95_high": 9.482291666666663,
        "min": -77.0,
        "max": 66.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 28.833333333333332,
        "median": 25.5,
        "std": 19.19997106479301,
        "ci95_low": 21.13854166666667,
        "ci95_high": 36.953124999999986,
        "min": 5.0,
        "max": 77.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.15338618718898753,
        "median": 0.15363494485676632,
        "std": 0.010926402008409237,
        "ci95_low": 0.1490063252030028,
        "ci95_high": 0.15759797259865135,
        "min": 0.13232963549920762,
        "max": 0.17558528428093645
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06388558089033386,
        "median": 0.05935376316745995,
        "std": 0.019522257295951074,
        "ci95_low": 0.0576078261198903,
        "ci95_high": 0.07300410576577845,
        "min": 0.03724971027264308,
        "max": 0.10901157326849294
      }
    },
    "20": {
      "population_delta": {
        "n": 24,
        "mean": -2.875,
        "median": -3.5,
        "std": 48.27724835088816,
        "ci95_low": -21.002083333333335,
        "ci95_high": 16.462499999999956,
        "min": -80.0,
        "max": 102.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 37.375,
        "median": 28.5,
        "std": 30.693121514980085,
        "ci95_low": 26.38854166666667,
        "ci95_high": 49.984375,
        "min": 1.0,
        "max": 102.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.14257306027149852,
        "median": 0.14213917076402693,
        "std": 0.014807111772026106,
        "ci95_low": 0.13706606112969552,
        "ci95_high": 0.14848872893777695,
        "min": 0.11626468769325912,
        "max": 0.18199867637326275
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06279480650330589,
        "median": 0.06207286325435221,
        "std": 0.01877985171615559,
        "ci95_low": 0.05528915971207093,
        "ci95_high": 0.07101402711675395,
        "min": 0.023673356551084775,
        "max": 0.10143914799550893
      }
    },
    "24": {
      "population_delta": {
        "n": 24,
        "mean": -4.333333333333333,
        "median": -4.0,
        "std": 59.58863612766746,
        "ci95_low": -25.627083333333335,
        "ci95_high": 20.02604166666666,
        "min": -95.0,
        "max": 146.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 45.166666666666664,
        "median": 35.0,
        "std": 39.109532796436675,
        "ci95_low": 30.144791666666666,
        "ci95_high": 60.24270833333332,
        "min": 1.0,
        "max": 146.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1411673881915211,
        "median": 0.14077104601044754,
        "std": 0.015561856633866842,
        "ci95_low": 0.13574727258627997,
        "ci95_high": 0.14756995676767404,
        "min": 0.12088428974600188,
        "max": 0.19004065040650406
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06343344651526404,
        "median": 0.059840144710040705,
        "std": 0.02112881347283392,
        "ci95_low": 0.05551520727863213,
        "ci95_high": 0.07234439798267836,
        "min": 0.03626554946587114,
        "max": 0.1286118041100905
      }
    },
    "32": {
      "population_delta": {
        "n": 24,
        "mean": -9.166666666666666,
        "median": -25.0,
        "std": 89.64544358502307,
        "ci95_low": -44.44479166666667,
        "ci95_high": 26.867708333333322,
        "min": -134.0,
        "max": 211.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 74.41666666666667,
        "median": 85.5,
        "std": 50.818235462829236,
        "ci95_low": 52.25729166666667,
        "ci95_high": 94.02604166666666,
        "min": 2.0,
        "max": 211.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.12968415596747898,
        "median": 0.12714240357838047,
        "std": 0.014049783369147872,
        "ci95_low": 0.12460550968062147,
        "ci95_high": 0.13500569186746592,
        "min": 0.11002285341168788,
        "max": 0.16525974025974027
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06411730533411028,
        "median": 0.0663059119211224,
        "std": 0.018687649773859626,
        "ci95_low": 0.05709226133078657,
        "ci95_high": 0.07102408602420006,
        "min": 0.03335826127715101,
        "max": 0.10212078807670032
      }
    }
  },
  "independent_no_pulse_stochastic_baseline": {
    "1": {
      "population_delta": {
        "n": 24,
        "mean": 0.75,
        "median": 1.0,
        "std": 5.494315243958978,
        "ci95_low": -1.375,
        "ci95_high": 3.0833333333333335,
        "min": -9.0,
        "max": 10.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 4.916666666666667,
        "median": 5.0,
        "std": 2.5644470922381863,
        "ci95_low": 3.894791666666667,
        "ci95_high": 5.958333333333333,
        "min": 0.0,
        "max": 10.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.12557950704399523,
        "median": 0.12720974677496416,
        "std": 0.020218730787895777,
        "ci95_low": 0.11734111942647445,
        "ci95_high": 0.13369307496929977,
        "min": 0.07523510971786834,
        "max": 0.167420814479638
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.07805722324028562,
        "median": 0.07777043230543684,
        "std": 0.02484825376440252,
        "ci95_low": 0.0692555008300822,
        "ci95_high": 0.08754955139185272,
        "min": 0.03294122362164944,
        "max": 0.12682458253416376
      }
    },
    "2": {
      "population_delta": {
        "n": 24,
        "mean": -0.125,
        "median": 0.5,
        "std": 9.518895681747962,
        "ci95_low": -3.8374999999999995,
        "ci95_high": 3.7322916666666637,
        "min": -22.0,
        "max": 14.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 7.708333333333333,
        "median": 6.0,
        "std": 5.5862865324133,
        "ci95_low": 5.708333333333333,
        "ci95_high": 10.041666666666666,
        "min": 0.0,
        "max": 22.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.17168380260825802,
        "median": 0.16297613754261153,
        "std": 0.022978561038565465,
        "ci95_low": 0.1633369923907135,
        "ci95_high": 0.1813033274052024,
        "min": 0.14136125654450263,
        "max": 0.23722627737226276
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.09150783019649945,
        "median": 0.08643391458497199,
        "std": 0.03177964875124602,
        "ci95_low": 0.07846523428929345,
        "ci95_high": 0.10429394680053461,
        "min": 0.05078211996786471,
        "max": 0.1460232160169455
      }
    },
    "4": {
      "population_delta": {
        "n": 24,
        "mean": -1.5833333333333333,
        "median": 3.0,
        "std": 14.671164083178796,
        "ci95_low": -7.861458333333333,
        "ci95_high": 3.8968749999999988,
        "min": -41.0,
        "max": 22.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 12.083333333333334,
        "median": 9.0,
        "std": 8.470127245535071,
        "ci95_low": 8.976041666666667,
        "ci95_high": 15.627083333333331,
        "min": 3.0,
        "max": 41.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1912678039858747,
        "median": 0.19031927631948212,
        "std": 0.02110744362867076,
        "ci95_low": 0.18268081310351933,
        "ci95_high": 0.2000006032815853,
        "min": 0.15833333333333333,
        "max": 0.24802110817941952
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.11031099347460609,
        "median": 0.11113078612498012,
        "std": 0.030251675333203124,
        "ci95_low": 0.09852827561697149,
        "ci95_high": 0.1248590404297758,
        "min": 0.06278356152149231,
        "max": 0.18579064305173923
      }
    },
    "5": {
      "population_delta": {
        "n": 24,
        "mean": -2.1666666666666665,
        "median": 1.5,
        "std": 19.036514620299823,
        "ci95_low": -9.545833333333333,
        "ci95_high": 4.855208333333333,
        "min": -55.0,
        "max": 29.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 13.833333333333334,
        "median": 8.5,
        "std": 13.256025883432116,
        "ci95_low": 8.642708333333335,
        "ci95_high": 19.021875,
        "min": 0.0,
        "max": 55.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.19516945185704726,
        "median": 0.20100013110332815,
        "std": 0.027952743275229733,
        "ci95_low": 0.18448213182706757,
        "ci95_high": 0.20622706210367325,
        "min": 0.13539651837524178,
        "max": 0.24305555555555555
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.10557572268373235,
        "median": 0.10418282175441274,
        "std": 0.027871801118712188,
        "ci95_low": 0.09553543480347289,
        "ci95_high": 0.11847866066617252,
        "min": 0.05915122518575273,
        "max": 0.19925882616148488
      }
    },
    "6": {
      "population_delta": {
        "n": 24,
        "mean": -1.0833333333333333,
        "median": -1.0,
        "std": 23.13171824333179,
        "ci95_low": -11.023958333333333,
        "ci95_high": 7.876041666666646,
        "min": -45.0,
        "max": 37.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 18.5,
        "median": 14.0,
        "std": 13.92838827718412,
        "ci95_low": 12.892708333333335,
        "ci95_high": 23.629166666666663,
        "min": 1.0,
        "max": 45.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.19750262067486676,
        "median": 0.19856630824372762,
        "std": 0.02645934603326862,
        "ci95_low": 0.18676344702696684,
        "ci95_high": 0.2088974065239276,
        "min": 0.15461847389558234,
        "max": 0.24688796680497926
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.10168926694034129,
        "median": 0.10568513654071562,
        "std": 0.031048704081108006,
        "ci95_low": 0.08882364528223936,
        "ci95_high": 0.11426137970036257,
        "min": 0.04374581519935289,
        "max": 0.17058025782192776
      }
    },
    "8": {
      "population_delta": {
        "n": 24,
        "mean": -2.625,
        "median": 1.5,
        "std": 31.51165459000844,
        "ci95_low": -14.688541666666667,
        "ci95_high": 9.863541666666658,
        "min": -64.0,
        "max": 69.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 23.541666666666668,
        "median": 18.0,
        "std": 21.110777592394733,
        "ci95_low": 15.164583333333333,
        "ci95_high": 31.543749999999996,
        "min": 0.0,
        "max": 69.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.19340608469266987,
        "median": 0.19416366322824752,
        "std": 0.023730086264296783,
        "ci95_low": 0.18444926241000065,
        "ci95_high": 0.20267285887258743,
        "min": 0.15326251896813353,
        "max": 0.24571428571428572
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.10042144339851271,
        "median": 0.09618073571903768,
        "std": 0.033997789314908315,
        "ci95_low": 0.088673249975598,
        "ci95_high": 0.11405530721850739,
        "min": 0.039024918376410346,
        "max": 0.19463078512265272
      }
    },
    "12": {
      "population_delta": {
        "n": 24,
        "mean": 1.0833333333333333,
        "median": 12.5,
        "std": 46.542021037146874,
        "ci95_low": -19.271875,
        "ci95_high": 18.732291666666665,
        "min": -94.0,
        "max": 73.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 39.166666666666664,
        "median": 39.5,
        "std": 25.16556288970218,
        "ci95_low": 28.728125,
        "ci95_high": 49.33541666666667,
        "min": 2.0,
        "max": 94.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1806334853072379,
        "median": 0.17574454200284767,
        "std": 0.02240573617781182,
        "ci95_low": 0.17151827609494452,
        "ci95_high": 0.18977641549414614,
        "min": 0.14431082331174838,
        "max": 0.2356687898089172
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.09453407514623167,
        "median": 0.08251523436419612,
        "std": 0.03645547262487616,
        "ci95_low": 0.08128167181954783,
        "ci95_high": 0.1097276840748281,
        "min": 0.04834541187347658,
        "max": 0.21595018894543286
      }
    },
    "16": {
      "population_delta": {
        "n": 24,
        "mean": -2.0416666666666665,
        "median": 5.5,
        "std": 58.50746331784424,
        "ci95_low": -24.35729166666667,
        "ci95_high": 19.82187499999999,
        "min": -153.0,
        "max": 95.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 45.791666666666664,
        "median": 31.0,
        "std": 36.474853400055714,
        "ci95_low": 32.184375,
        "ci95_high": 59.39895833333333,
        "min": 5.0,
        "max": 153.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1732666935365533,
        "median": 0.17186143879291843,
        "std": 0.026064428337767936,
        "ci95_low": 0.1629529123377445,
        "ci95_high": 0.18335897175193272,
        "min": 0.11901081916537867,
        "max": 0.23083941605839417
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.09536628815248116,
        "median": 0.09868944642904517,
        "std": 0.02442312723948011,
        "ci95_low": 0.08695575410994373,
        "ci95_high": 0.10423500835873459,
        "min": 0.0582929282577792,
        "max": 0.1366207390845113
      }
    },
    "20": {
      "population_delta": {
        "n": 24,
        "mean": 1.7916666666666667,
        "median": -0.5,
        "std": 69.0959352197283,
        "ci95_low": -25.5125,
        "ci95_high": 31.383333333333326,
        "min": -154.0,
        "max": 153.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 52.791666666666664,
        "median": 39.5,
        "std": 44.61500043582751,
        "ci95_low": 35.89270833333334,
        "ci95_high": 69.43124999999998,
        "min": 1.0,
        "max": 154.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.16547835247734502,
        "median": 0.16051858272835626,
        "std": 0.019365658015580225,
        "ci95_low": 0.15795962091850885,
        "ci95_high": 0.17262085512781308,
        "min": 0.1316270566727605,
        "max": 0.20980615735461802
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.09618686644215857,
        "median": 0.09476239487683018,
        "std": 0.027209945546540028,
        "ci95_low": 0.08587606065919665,
        "ci95_high": 0.10585239074622452,
        "min": 0.057925590704471945,
        "max": 0.14530245632868646
      }
    },
    "24": {
      "population_delta": {
        "n": 24,
        "mean": 4.5,
        "median": -1.5,
        "std": 84.74373133158582,
        "ci95_low": -26.771875,
        "ci95_high": 38.022916666666646,
        "min": -180.0,
        "max": 216.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 63.583333333333336,
        "median": 45.0,
        "std": 56.20417886796516,
        "ci95_low": 42.223958333333336,
        "ci95_high": 86.34375,
        "min": 0.0,
        "max": 216.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.15325190330359978,
        "median": 0.15402625300173514,
        "std": 0.018049021809436,
        "ci95_low": 0.14572020956852877,
        "ci95_high": 0.16021273070828804,
        "min": 0.12291760468257541,
        "max": 0.20157189089227925
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.09280821257669063,
        "median": 0.09453250926370285,
        "std": 0.030619221484498665,
        "ci95_low": 0.0815869307481538,
        "ci95_high": 0.10436034877317704,
        "min": 0.04995657379882762,
        "max": 0.16035847370609918
      }
    },
    "32": {
      "population_delta": {
        "n": 24,
        "mean": -3.5833333333333335,
        "median": -1.0,
        "std": 122.56899984181247,
        "ci95_low": -46.83229166666666,
        "ci95_high": 45.27708333333331,
        "min": -189.0,
        "max": 301.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 96.41666666666667,
        "median": 81.0,
        "std": 75.7616419363314,
        "ci95_low": 68.30520833333334,
        "ci95_high": 127.70104166666665,
        "min": 1.0,
        "max": 301.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1387010895940292,
        "median": 0.13754282764304432,
        "std": 0.01524173215050141,
        "ci95_low": 0.1333238108224455,
        "ci95_high": 0.1452373409515995,
        "min": 0.10851063829787234,
        "max": 0.18610421836228289
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.08396430690373252,
        "median": 0.07935745686380075,
        "std": 0.020704659188073005,
        "ci95_low": 0.07648939543645907,
        "ci95_high": 0.09261360030180477,
        "min": 0.05304969762779218,
        "max": 0.1369181750393875
      }
    }
  },
  "excess_over_stochastic_baseline": {
    "1": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.12557950704399523,
        "median": -0.12720974677496416,
        "std": 0.020218730787895777,
        "ci95_low": -0.13377719051006745,
        "ci95_high": -0.11751181841676704,
        "min": -0.167420814479638,
        "max": -0.07523510971786834
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.07805722324028562,
        "median": -0.07777043230543684,
        "std": 0.02484825376440252,
        "ci95_low": -0.08826765312391038,
        "ci95_high": -0.06739576850383941,
        "min": -0.12682458253416376,
        "max": -0.03294122362164944
      }
    },
    "2": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.17168380260825802,
        "median": -0.16297613754261153,
        "std": 0.022978561038565465,
        "ci95_low": -0.18175878705042145,
        "ci95_high": -0.1630365997351541,
        "min": -0.23722627737226276,
        "max": -0.14136125654450263
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.09150783019649945,
        "median": -0.08643391458497199,
        "std": 0.03177964875124602,
        "ci95_low": -0.1040882189971585,
        "ci95_high": -0.08004057973519803,
        "min": -0.1460232160169455,
        "max": -0.05078211996786471
      }
    },
    "4": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.1912678039858747,
        "median": -0.19031927631948212,
        "std": 0.02110744362867076,
        "ci95_low": -0.19983394432355586,
        "ci95_high": -0.1830356410023213,
        "min": -0.24802110817941952,
        "max": -0.15833333333333333
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.11031099347460609,
        "median": -0.11113078612498012,
        "std": 0.030251675333203124,
        "ci95_low": -0.12277879505271984,
        "ci95_high": -0.09771801779652177,
        "min": -0.18579064305173923,
        "max": -0.06278356152149231
      }
    },
    "5": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.17901161360482942,
        "median": -0.18621664282407674,
        "std": 0.030103046150364108,
        "ci95_low": -0.19018323765915987,
        "ci95_high": -0.16775416468499196,
        "min": -0.22975768321513002,
        "max": -0.1129932597194373
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.07875523539446444,
        "median": -0.07570747111416026,
        "std": 0.030751806643052895,
        "ci95_low": -0.09119090015924576,
        "ci95_high": -0.06838983934999464,
        "min": -0.18755830334251727,
        "max": -0.03714387363059707
      }
    },
    "6": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.12641212373522195,
        "median": -0.12757333927148515,
        "std": 0.03787488632271858,
        "ci95_low": -0.14130463516523523,
        "ci95_high": -0.10975744835417052,
        "min": -0.2101434503181228,
        "max": -0.06912662090007626
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.060354111326667535,
        "median": -0.05828805040787581,
        "std": 0.0358749445999759,
        "ci95_low": -0.07460063918997838,
        "ci95_high": -0.0449912954652898,
        "min": -0.13975886254791944,
        "max": -0.00809249660798933
      }
    },
    "8": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.061254981270606884,
        "median": -0.05830518959540941,
        "std": 0.0298273954548349,
        "ci95_low": -0.07419501071226785,
        "ci95_high": -0.04901258249814554,
        "min": -0.11903353890343836,
        "max": 0.00394979869799289
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.04675095525800307,
        "median": -0.04442581098211083,
        "std": 0.0313628220500035,
        "ci95_low": -0.05923300823335794,
        "ci95_high": -0.033732840504882664,
        "min": -0.11900489364642966,
        "max": 0.007926497319030251
      }
    },
    "12": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.029045917274910574,
        "median": -0.029627556463983643,
        "std": 0.02414848961471932,
        "ci95_low": -0.038409647322542685,
        "ci95_high": -0.020384779200541363,
        "min": -0.07353551500991438,
        "max": 0.011449545351846085
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.03024643159907946,
        "median": -0.0268190855098287,
        "std": 0.04035537685258751,
        "ci95_low": -0.047129339646639394,
        "ci95_high": -0.01599043097392042,
        "min": -0.16219884983723115,
        "max": 0.037938984670196
      }
    },
    "16": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.0198805063475658,
        "median": -0.019765473515412565,
        "std": 0.024367128430297025,
        "ci95_low": -0.030079236493751518,
        "ci95_high": -0.010403588723573038,
        "min": -0.06652168152525642,
        "max": 0.02736822551875076
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.0314807072621473,
        "median": -0.027741140325394553,
        "std": 0.022645127025847166,
        "ci95_low": -0.041052591776479276,
        "ci95_high": -0.022602914017772213,
        "min": -0.07643382314122947,
        "max": -0.0002797439545134395
      }
    },
    "20": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.0229052922058465,
        "median": -0.024555806214290363,
        "std": 0.02198690196220971,
        "ci95_low": -0.031579900329422664,
        "ci95_high": -0.015167458141097006,
        "min": -0.07585554007066742,
        "max": 0.029532308660258272
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.03339205993885266,
        "median": -0.03558028027937186,
        "std": 0.028325866742110482,
        "ci95_low": -0.044319322684133175,
        "ci95_high": -0.022505675512859993,
        "min": -0.08683151268058323,
        "max": 0.024368169013095145
      }
    },
    "24": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.01208451511207865,
        "median": -0.016371951372725096,
        "std": 0.02218373002640641,
        "ci95_low": -0.01996725701923983,
        "ci95_high": -0.0029993483970821495,
        "min": -0.060108476258132926,
        "max": 0.0313891878383335
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.029374766061426586,
        "median": -0.0295810591505652,
        "std": 0.03443543347160516,
        "ci95_low": -0.042227744085984,
        "ci95_high": -0.015032454968825224,
        "min": -0.08436114169433581,
        "max": 0.07081211219240033
      }
    },
    "32": {
      "symdiff_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.00901693362655019,
        "median": -0.014224435266266641,
        "std": 0.020118859390247084,
        "ci95_low": -0.016872608495960777,
        "ci95_high": -0.000692965984492795,
        "min": -0.05158233829745307,
        "max": 0.025408874722080324
      },
      "feature_distance_causal_minus_stochastic": {
        "n": 24,
        "mean": -0.019847001569622245,
        "median": -0.027247268146582168,
        "std": 0.0225632710936628,
        "ci95_low": -0.0286020147264215,
        "ci95_high": -0.01087701627661314,
        "min": -0.05237412434100505,
        "max": 0.026572008732741112
      }
    }
  },
  "interpretation": "The exact causal fork measures the effect of changing the pulse while holding checkpoint RNG state and future environment fixed. The independent no-pulse fork is only a reference scale for stochastic continuation spread; it is not an exact counterfactual."
}
```


# Stage 2 — Can Ensemble Single-Pulse Responses Predict the Pulse Train?

```json
{
  "measurement_space": "24 normalized morphology features",
  "model": "ensemble-mean isolated-pulse additive prediction",
  "patterns_zero_indexed": {
    "clustered": [
      0,
      1,
      2,
      15
    ],
    "dispersed": [
      0,
      7,
      8,
      15
    ]
  },
  "same_onset": true,
  "same_offset": true,
  "same_pulse_count": true,
  "summary": {
    "16": {
      "clustered": {
        "residual_norm": {
          "value": 0.023321437846284414,
          "bootstrap_ci95_low": 0.02167641035467634,
          "bootstrap_ci95_high": 0.059751590235049425
        },
        "actual_mean_delta_norm": {
          "value": 0.020752729461729756,
          "bootstrap_ci95_low": 0.0189525779851096,
          "bootstrap_ci95_high": 0.035939746949100404
        },
        "predicted_mean_delta_norm": {
          "value": 0.0385354208293336,
          "bootstrap_ci95_low": 0.033897286290356085,
          "bootstrap_ci95_high": 0.07868720687485947
        },
        "relative_superposition_error": {
          "value": 1.1237768935065449,
          "bootstrap_ci95_low": 0.8254508462258088,
          "bootstrap_ci95_high": 2.3349757066652597
        },
        "cosine_actual_vs_predicted": {
          "value": 0.8576584755242016,
          "bootstrap_ci95_low": 0.4277338425962796,
          "bootstrap_ci95_high": 0.9095713985654107
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.021698224478168063,
          "bootstrap_ci95_low": 0.02073965393727992,
          "bootstrap_ci95_high": 0.05372334066436131
        },
        "actual_mean_delta_norm": {
          "value": 0.02120193807522071,
          "bootstrap_ci95_low": 0.018751118131351698,
          "bootstrap_ci95_high": 0.03788818424169153
        },
        "predicted_mean_delta_norm": {
          "value": 0.036932546426484365,
          "bootstrap_ci95_low": 0.030846251652590292,
          "bootstrap_ci95_high": 0.07304487345450798
        },
        "relative_superposition_error": {
          "value": 1.0234075960974236,
          "bootstrap_ci95_low": 0.7067267699355638,
          "bootstrap_ci95_high": 2.361609690379092
        },
        "cosine_actual_vs_predicted": {
          "value": 0.857376085025669,
          "bootstrap_ci95_low": 0.17366133309911796,
          "bootstrap_ci95_high": 0.9380262590732497
        }
      }
    },
    "18": {
      "clustered": {
        "residual_norm": {
          "value": 0.0282244066984098,
          "bootstrap_ci95_low": 0.024309077767781476,
          "bootstrap_ci95_high": 0.06377260378185794
        },
        "actual_mean_delta_norm": {
          "value": 0.017606194761157386,
          "bootstrap_ci95_low": 0.016974718469449503,
          "bootstrap_ci95_high": 0.037064529285969976
        },
        "predicted_mean_delta_norm": {
          "value": 0.03434407005467668,
          "bootstrap_ci95_low": 0.031977897437044905,
          "bootstrap_ci95_high": 0.07691897374779262
        },
        "relative_superposition_error": {
          "value": 1.603095221954389,
          "bootstrap_ci95_low": 0.852122441143791,
          "bootstrap_ci95_high": 3.1738121113270847
        },
        "cosine_actual_vs_predicted": {
          "value": 0.5729389233338728,
          "bootstrap_ci95_low": 0.10342099814789488,
          "bootstrap_ci95_high": 0.8854056361795684
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.01587362814531411,
          "bootstrap_ci95_low": 0.018328031340913098,
          "bootstrap_ci95_high": 0.05834702728347833
        },
        "actual_mean_delta_norm": {
          "value": 0.017456117126612908,
          "bootstrap_ci95_low": 0.015796096857027996,
          "bootstrap_ci95_high": 0.034943119517196815
        },
        "predicted_mean_delta_norm": {
          "value": 0.026341045122327475,
          "bootstrap_ci95_low": 0.02634324505874338,
          "bootstrap_ci95_high": 0.07116508359772826
        },
        "relative_superposition_error": {
          "value": 0.9093447317166429,
          "bootstrap_ci95_low": 0.6644194353758825,
          "bootstrap_ci95_high": 2.613456821863549
        },
        "cosine_actual_vs_predicted": {
          "value": 0.8118470307537154,
          "bootstrap_ci95_low": 0.17302511136317425,
          "bootstrap_ci95_high": 0.9223696431763945
        }
      }
    },
    "20": {
      "clustered": {
        "residual_norm": {
          "value": 0.03312221202183783,
          "bootstrap_ci95_low": 0.025554067798170228,
          "bootstrap_ci95_high": 0.0670259702303073
        },
        "actual_mean_delta_norm": {
          "value": 0.0185626719873035,
          "bootstrap_ci95_low": 0.016029105415486907,
          "bootstrap_ci95_high": 0.03511571879385847
        },
        "predicted_mean_delta_norm": {
          "value": 0.04114640257190737,
          "bootstrap_ci95_low": 0.03508983352145563,
          "bootstrap_ci95_high": 0.08181706791222619
        },
        "relative_superposition_error": {
          "value": 1.7843450578932154,
          "bootstrap_ci95_low": 0.9086161355833893,
          "bootstrap_ci95_high": 3.3309795439817576
        },
        "cosine_actual_vs_predicted": {
          "value": 0.6156939643802718,
          "bootstrap_ci95_low": 0.06357379864417345,
          "bootstrap_ci95_high": 0.8768292209206673
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.029760694144829087,
          "bootstrap_ci95_low": 0.02276989906901781,
          "bootstrap_ci95_high": 0.06115976775074555
        },
        "actual_mean_delta_norm": {
          "value": 0.01817067599339885,
          "bootstrap_ci95_low": 0.016266851103182003,
          "bootstrap_ci95_high": 0.034925955221719186
        },
        "predicted_mean_delta_norm": {
          "value": 0.039563625951107934,
          "bootstrap_ci95_low": 0.03228614951595558,
          "bootstrap_ci95_high": 0.07564216275266744
        },
        "relative_superposition_error": {
          "value": 1.637841880821645,
          "bootstrap_ci95_low": 0.9328397217616509,
          "bootstrap_ci95_high": 2.8478250167553694
        },
        "cosine_actual_vs_predicted": {
          "value": 0.7022938509133,
          "bootstrap_ci95_low": 0.27261380055170226,
          "bootstrap_ci95_high": 0.8892308098458784
        }
      }
    },
    "24": {
      "clustered": {
        "residual_norm": {
          "value": 0.03511319513026694,
          "bootstrap_ci95_low": 0.028921004484294358,
          "bootstrap_ci95_high": 0.07686272859490167
        },
        "actual_mean_delta_norm": {
          "value": 0.013357599293190534,
          "bootstrap_ci95_low": 0.01266324278996083,
          "bootstrap_ci95_high": 0.03291336921267001
        },
        "predicted_mean_delta_norm": {
          "value": 0.04044977876351507,
          "bootstrap_ci95_low": 0.03502012895924827,
          "bootstrap_ci95_high": 0.09462244419046625
        },
        "relative_superposition_error": {
          "value": 2.628705530054867,
          "bootstrap_ci95_low": 1.2616659013266251,
          "bootstrap_ci95_high": 4.3355266241963735
        },
        "cosine_actual_vs_predicted": {
          "value": 0.5382757159749089,
          "bootstrap_ci95_low": 0.151601622018005,
          "bootstrap_ci95_high": 0.8901244794701578
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.03826258284880841,
          "bootstrap_ci95_low": 0.023686325690921013,
          "bootstrap_ci95_high": 0.07790230766371938
        },
        "actual_mean_delta_norm": {
          "value": 0.01950984487987742,
          "bootstrap_ci95_low": 0.016752003760315028,
          "bootstrap_ci95_high": 0.03970401371332935
        },
        "predicted_mean_delta_norm": {
          "value": 0.04277594051674058,
          "bootstrap_ci95_low": 0.029200588267904705,
          "bootstrap_ci95_high": 0.09188539975908726
        },
        "relative_superposition_error": {
          "value": 1.9611935965863412,
          "bootstrap_ci95_low": 0.8719070276169414,
          "bootstrap_ci95_high": 3.5334497301021135
        },
        "cosine_actual_vs_predicted": {
          "value": 0.4471799960930078,
          "bootstrap_ci95_low": -0.06170195974308428,
          "bootstrap_ci95_high": 0.9022297821480671
        }
      }
    },
    "28": {
      "clustered": {
        "residual_norm": {
          "value": 0.03785538747609185,
          "bootstrap_ci95_low": 0.030201858144749707,
          "bootstrap_ci95_high": 0.08646381645486573
        },
        "actual_mean_delta_norm": {
          "value": 0.01087392454419598,
          "bootstrap_ci95_low": 0.012356927025278446,
          "bootstrap_ci95_high": 0.03073598323890459
        },
        "predicted_mean_delta_norm": {
          "value": 0.04169413302565222,
          "bootstrap_ci95_low": 0.0344027086032157,
          "bootstrap_ci95_high": 0.09982076170997313
        },
        "relative_superposition_error": {
          "value": 3.481299444577936,
          "bootstrap_ci95_low": 1.3739900436056314,
          "bootstrap_ci95_high": 5.093312115816685
        },
        "cosine_actual_vs_predicted": {
          "value": 0.46717286961653737,
          "bootstrap_ci95_low": 0.039025582128672416,
          "bootstrap_ci95_high": 0.8900348851690679
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.05220488321018754,
          "bootstrap_ci95_low": 0.03276475115019102,
          "bootstrap_ci95_high": 0.0878520966142928
        },
        "actual_mean_delta_norm": {
          "value": 0.014540842470416428,
          "bootstrap_ci95_low": 0.013804855284560722,
          "bootstrap_ci95_high": 0.03369289239666473
        },
        "predicted_mean_delta_norm": {
          "value": 0.05497063618024383,
          "bootstrap_ci95_low": 0.03564050991826553,
          "bootstrap_ci95_high": 0.10730665897158588
        },
        "relative_superposition_error": {
          "value": 3.5902241095314245,
          "bootstrap_ci95_low": 1.3008505011363318,
          "bootstrap_ci95_high": 5.045821140810027
        },
        "cosine_actual_vs_predicted": {
          "value": 0.3176809767633444,
          "bootstrap_ci95_low": -0.1429597301574134,
          "bootstrap_ci95_high": 0.8595089679079977
        }
      }
    },
    "32": {
      "clustered": {
        "residual_norm": {
          "value": 0.035188072186095105,
          "bootstrap_ci95_low": 0.029127078812640907,
          "bootstrap_ci95_high": 0.07269994690396157
        },
        "actual_mean_delta_norm": {
          "value": 0.014470306802583799,
          "bootstrap_ci95_low": 0.013794129871450567,
          "bootstrap_ci95_high": 0.029827724085035916
        },
        "predicted_mean_delta_norm": {
          "value": 0.041341255749543726,
          "bootstrap_ci95_low": 0.035920663891722396,
          "bootstrap_ci95_high": 0.08649487863818191
        },
        "relative_superposition_error": {
          "value": 2.431743339388766,
          "bootstrap_ci95_low": 1.1859500127199714,
          "bootstrap_ci95_high": 3.913776435271779
        },
        "cosine_actual_vs_predicted": {
          "value": 0.5685935255213646,
          "bootstrap_ci95_low": 0.23622570351773708,
          "bootstrap_ci95_high": 0.8664955972080417
        }
      },
      "dispersed": {
        "residual_norm": {
          "value": 0.04182294022736119,
          "bootstrap_ci95_low": 0.030331655763880333,
          "bootstrap_ci95_high": 0.07544079845744038
        },
        "actual_mean_delta_norm": {
          "value": 0.014932873939379964,
          "bootstrap_ci95_low": 0.014531535519217757,
          "bootstrap_ci95_high": 0.03390200232696455
        },
        "predicted_mean_delta_norm": {
          "value": 0.04733723978968733,
          "bootstrap_ci95_low": 0.03539975867250382,
          "bootstrap_ci95_high": 0.09111500715480103
        },
        "relative_superposition_error": {
          "value": 2.8007294776036757,
          "bootstrap_ci95_low": 1.177352989138455,
          "bootstrap_ci95_high": 4.2497865337461205
        },
        "cosine_actual_vs_predicted": {
          "value": 0.5054928841902939,
          "bootstrap_ci95_low": 0.05537969686153196,
          "bootstrap_ci95_high": 0.8588351489908501
        }
      }
    }
  },
  "interpretation": "Small ensemble-mean residuals support this declared additive mean-response approximation. Large residuals reject that approximation in the measured feature space, but do not establish memory, storage, or a special information-processing mechanism."
}
```


# Stage 3 — Matched Timing, Multiple Candidate Measurement Instruments

```json
{
  "codeword_A": "1110000000000001",
  "codeword_B": "1000000110000001",
  "pulse_positions_A_zero_indexed": [
    0,
    1,
    2,
    15
  ],
  "pulse_positions_B_zero_indexed": [
    0,
    7,
    8,
    15
  ],
  "same_pulse_count": true,
  "same_first_pulse": true,
  "same_last_pulse": true,
  "groups": 24,
  "candidate_instruments": [
    "energy_distance",
    "paired_mean_l2",
    "paired_max_abs_mean",
    "paired_ridge_hotelling"
  ],
  "instrument_selection_rule": "No real-data p-value may select the instrument. Selection occurs only in Stage 5 from known-null/known-effect calibration.",
  "results": {
    "16": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.35943103490325257,
          "permutations": 250,
          "p_value": 0.749003984063745,
          "null_mean": 0.409686159014244,
          "null_q95": 0.5353303105868542,
          "null_q99": 0.6398649218150747
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 0.8619517314706564,
          "permutations": 250,
          "p_value": 0.7928286852589641,
          "null_mean": 1.0300804290371919,
          "null_q95": 1.3900969113050143,
          "null_q99": 1.5486976869724591
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.32117612361222647,
          "permutations": 250,
          "p_value": 0.900398406374502,
          "null_mean": 0.4897869891995395,
          "null_q95": 0.7556296522150436,
          "null_q99": 0.8565679414733308
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 0.9993857555223344,
          "permutations": 250,
          "p_value": 0.29880478087649404,
          "null_mean": 0.8713330419051383,
          "null_q95": 1.5573632809708327,
          "null_q99": 2.4516501926430903
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.16467868261105809,
          "median": 0.16342068569036772,
          "std": 0.014779933924678745,
          "ci95_low": 0.15852104037110623,
          "ci95_high": 0.1703152429549012,
          "min": 0.13473684210526315,
          "max": 0.18993993993993993
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0844978007755401,
          "median": 0.07873291095397367,
          "std": 0.030113824077832998,
          "ci95_low": 0.0735900447111711,
          "ci95_high": 0.09684184670672269,
          "min": 0.04579729240016265,
          "max": 0.17713357559655268
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 38.791666666666664,
          "median": 34.0,
          "std": 25.116361146117924,
          "ci95_low": 28.041666666666668,
          "ci95_high": 48.58541666666667,
          "min": 1.0,
          "max": 97.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 17,
          "feature_name": "sector_1",
          "mean_standardized_delta_A_minus_B": 0.32117612361222647
        },
        {
          "feature_index": 7,
          "feature_name": "cov_anisotropy",
          "mean_standardized_delta_A_minus_B": 0.32053873322884363
        },
        {
          "feature_index": 15,
          "feature_name": "degree_6",
          "mean_standardized_delta_A_minus_B": -0.26312717724917606
        },
        {
          "feature_index": 8,
          "feature_name": "boundary_fraction",
          "mean_standardized_delta_A_minus_B": 0.2631271772491757
        },
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": 0.25101422056949013
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": -0.24511426298818353
        }
      ],
      "steps_since_last_pulse_A": 0,
      "steps_since_last_pulse_B": 0,
      "equal_time_since_last_pulse": true
    },
    "18": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.3394683981072033,
          "permutations": 250,
          "p_value": 0.8446215139442231,
          "null_mean": 0.39155565411024895,
          "null_q95": 0.492336233144707,
          "null_q99": 0.5601587916081391
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 0.7823038666927595,
          "permutations": 250,
          "p_value": 0.8326693227091634,
          "null_mean": 0.9756921909538179,
          "null_q95": 1.2761460994851572,
          "null_q99": 1.4666889511480592
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.33430064086120553,
          "permutations": 250,
          "p_value": 0.8764940239043825,
          "null_mean": 0.474344049250601,
          "null_q95": 0.7083517327599511,
          "null_q99": 0.7706898967074273
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 0.5690824926914075,
          "permutations": 250,
          "p_value": 0.8087649402390438,
          "null_mean": 0.9359434180272566,
          "null_q95": 1.804841437540816,
          "null_q99": 2.147070574626762
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.16184973874543726,
          "median": 0.16243992995221546,
          "std": 0.014981426431153072,
          "ci95_low": 0.1562026112823256,
          "ci95_high": 0.1680981246709162,
          "min": 0.1288732394366197,
          "max": 0.18572524942440521
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.08073152159927428,
          "median": 0.07018793617526632,
          "std": 0.02663001195384179,
          "ci95_low": 0.07114256873992689,
          "ci95_high": 0.0916783494531122,
          "min": 0.04900708813807656,
          "max": 0.1586959850210877
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 43.833333333333336,
          "median": 39.0,
          "std": 28.632246777987152,
          "ci95_low": 33.469791666666666,
          "ci95_high": 57.19270833333333,
          "min": 2.0,
          "max": 116.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": -0.33430064086120553
        },
        {
          "feature_index": 17,
          "feature_name": "sector_1",
          "mean_standardized_delta_A_minus_B": 0.31519209130113296
        },
        {
          "feature_index": 7,
          "feature_name": "cov_anisotropy",
          "mean_standardized_delta_A_minus_B": 0.2778344869351252
        },
        {
          "feature_index": 12,
          "feature_name": "degree_3",
          "mean_standardized_delta_A_minus_B": 0.20702624765895125
        },
        {
          "feature_index": 11,
          "feature_name": "degree_2",
          "mean_standardized_delta_A_minus_B": 0.20339126223719362
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": -0.2023333996529242
        }
      ],
      "steps_since_last_pulse_A": 2,
      "steps_since_last_pulse_B": 2,
      "equal_time_since_last_pulse": true
    },
    "20": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.3623684840958967,
          "permutations": 250,
          "p_value": 0.7051792828685259,
          "null_mean": 0.39749982329946953,
          "null_q95": 0.4903121759289184,
          "null_q99": 0.52675542133018
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 0.9349158071177601,
          "permutations": 250,
          "p_value": 0.5418326693227091,
          "null_mean": 0.9595722003860097,
          "null_q95": 1.264015777086986,
          "null_q99": 1.3738350878896062
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.41348648517476444,
          "permutations": 250,
          "p_value": 0.7211155378486056,
          "null_mean": 0.4847864513122711,
          "null_q95": 0.7020470071250389,
          "null_q99": 0.7951585661968554
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 0.8380789453014661,
          "permutations": 250,
          "p_value": 0.6334661354581673,
          "null_mean": 1.0401533779828833,
          "null_q95": 1.819885135766918,
          "null_q99": 2.6295271884484226
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.15800254063469765,
          "median": 0.16037246760285,
          "std": 0.014007376388062952,
          "ci95_low": 0.15249440518220014,
          "ci95_high": 0.16333999207313762,
          "min": 0.12407862407862408,
          "max": 0.18118869013271782
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.07967235955937337,
          "median": 0.07938685296248985,
          "std": 0.02351596422202716,
          "ci95_low": 0.06996290612203417,
          "ci95_high": 0.08926497531025436,
          "min": 0.04656309150438273,
          "max": 0.14521086552298443
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 43.5,
          "median": 36.5,
          "std": 26.567524034680638,
          "ci95_low": 33.89479166666666,
          "ci95_high": 54.66875,
          "min": 2.0,
          "max": 113.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 10,
          "feature_name": "degree_1",
          "mean_standardized_delta_A_minus_B": 0.41348648517476444
        },
        {
          "feature_index": 17,
          "feature_name": "sector_1",
          "mean_standardized_delta_A_minus_B": 0.38438797698840593
        },
        {
          "feature_index": 13,
          "feature_name": "degree_4",
          "mean_standardized_delta_A_minus_B": 0.336360238457843
        },
        {
          "feature_index": 16,
          "feature_name": "sector_0",
          "mean_standardized_delta_A_minus_B": -0.23765604846263078
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": -0.19889824161420921
        },
        {
          "feature_index": 7,
          "feature_name": "cov_anisotropy",
          "mean_standardized_delta_A_minus_B": 0.19812847381449342
        }
      ],
      "steps_since_last_pulse_A": 4,
      "steps_since_last_pulse_B": 4,
      "equal_time_since_last_pulse": true
    },
    "24": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.48481520900336683,
          "permutations": 250,
          "p_value": 0.10358565737051793,
          "null_mean": 0.40654031943121777,
          "null_q95": 0.5101977613491893,
          "null_q99": 0.5254309403834438
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 1.2371799470640061,
          "permutations": 250,
          "p_value": 0.10756972111553785,
          "null_mean": 0.9973018562409642,
          "null_q95": 1.299874193427852,
          "null_q99": 1.452154057154944
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.7038978437044433,
          "permutations": 250,
          "p_value": 0.055776892430278883,
          "null_mean": 0.4908682605081302,
          "null_q95": 0.7021437001542746,
          "null_q99": 0.7794636129968835
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 1.7443643613892605,
          "permutations": 250,
          "p_value": 0.08764940239043825,
          "null_mean": 0.9951443568999466,
          "null_q95": 2.012253619242549,
          "null_q99": 2.9315649438427003
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.1477327960928597,
          "median": 0.15071627043994001,
          "std": 0.014831560279621599,
          "ci95_low": 0.14162528256113247,
          "ci95_high": 0.15342732710948573,
          "min": 0.1171634121274409,
          "max": 0.17982708933717578
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.07584857191608148,
          "median": 0.06696120771753056,
          "std": 0.027923060682172585,
          "ci95_low": 0.06609782232957391,
          "ci95_high": 0.08730983771755739,
          "min": 0.03856887308755746,
          "max": 0.16776022624494694
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 56.625,
          "median": 45.0,
          "std": 36.231676403390445,
          "ci95_low": 43.95625,
          "ci95_high": 72.91562499999999,
          "min": 16.0,
          "max": 143.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 11,
          "feature_name": "degree_2",
          "mean_standardized_delta_A_minus_B": 0.7038978437044433
        },
        {
          "feature_index": 12,
          "feature_name": "degree_3",
          "mean_standardized_delta_A_minus_B": -0.4274703395062203
        },
        {
          "feature_index": 17,
          "feature_name": "sector_1",
          "mean_standardized_delta_A_minus_B": 0.3585092690204956
        },
        {
          "feature_index": 9,
          "feature_name": "mean_degree",
          "mean_standardized_delta_A_minus_B": -0.34090823734183706
        },
        {
          "feature_index": 15,
          "feature_name": "degree_6",
          "mean_standardized_delta_A_minus_B": -0.31637830687144614
        },
        {
          "feature_index": 8,
          "feature_name": "boundary_fraction",
          "mean_standardized_delta_A_minus_B": 0.31637830687144564
        }
      ],
      "steps_since_last_pulse_A": 8,
      "steps_since_last_pulse_B": 8,
      "equal_time_since_last_pulse": true
    },
    "28": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.3730406798904058,
          "permutations": 250,
          "p_value": 0.749003984063745,
          "null_mean": 0.4139351221493124,
          "null_q95": 0.5342998871731445,
          "null_q99": 0.5724516891782487
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 0.8537736737839021,
          "permutations": 250,
          "p_value": 0.7888446215139442,
          "null_mean": 1.0177754996008335,
          "null_q95": 1.3611587771637843,
          "null_q99": 1.5627145107973452
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.38831181758333694,
          "permutations": 250,
          "p_value": 0.8725099601593626,
          "null_mean": 0.5127901180346811,
          "null_q95": 0.7250799474680658,
          "null_q99": 0.8818419223802688
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 0.5833611615635642,
          "permutations": 250,
          "p_value": 0.796812749003984,
          "null_mean": 0.9691362093164082,
          "null_q95": 1.8055728125923893,
          "null_q99": 2.4192137555489643
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.14112053163773305,
          "median": 0.14266615737203972,
          "std": 0.01395703898307453,
          "ci95_low": 0.13519655092875396,
          "ci95_high": 0.14676064972872171,
          "min": 0.11235471373224279,
          "max": 0.17141564902758932
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.0752158442040656,
          "median": 0.07180861469876372,
          "std": 0.025848843257307758,
          "ci95_low": 0.06510609758492415,
          "ci95_high": 0.08494769986086587,
          "min": 0.03713188625353285,
          "max": 0.1532493705413328
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 71.0,
          "median": 59.5,
          "std": 38.68893037205,
          "ci95_low": 55.72604166666667,
          "ci95_high": 84.80208333333333,
          "min": 14.0,
          "max": 161.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 12,
          "feature_name": "degree_3",
          "mean_standardized_delta_A_minus_B": -0.38831181758333694
        },
        {
          "feature_index": 22,
          "feature_name": "harmonic6_cos",
          "mean_standardized_delta_A_minus_B": -0.30019290826513023
        },
        {
          "feature_index": 17,
          "feature_name": "sector_1",
          "mean_standardized_delta_A_minus_B": 0.2898689024111549
        },
        {
          "feature_index": 10,
          "feature_name": "degree_1",
          "mean_standardized_delta_A_minus_B": 0.2884980597868742
        },
        {
          "feature_index": 7,
          "feature_name": "cov_anisotropy",
          "mean_standardized_delta_A_minus_B": 0.2662857432189159
        },
        {
          "feature_index": 21,
          "feature_name": "sector_5",
          "mean_standardized_delta_A_minus_B": -0.20984482516139802
        }
      ],
      "steps_since_last_pulse_A": 12,
      "steps_since_last_pulse_B": 12,
      "equal_time_since_last_pulse": true
    },
    "32": {
      "candidate_instruments": {
        "energy_distance": {
          "instrument": "energy_distance",
          "statistic": 0.45472506894370124,
          "permutations": 250,
          "p_value": 0.42231075697211157,
          "null_mean": 0.44689342512643765,
          "null_q95": 0.5563573412327896,
          "null_q99": 0.6042769270706704
        },
        "paired_mean_l2": {
          "instrument": "paired_mean_l2",
          "statistic": 1.2204479285185645,
          "permutations": 250,
          "p_value": 0.2749003984063745,
          "null_mean": 1.0918157599146516,
          "null_q95": 1.4853513883312233,
          "null_q99": 1.5870661759029723
        },
        "paired_max_abs_mean": {
          "instrument": "paired_max_abs_mean",
          "statistic": 0.5242109108207714,
          "permutations": 250,
          "p_value": 0.5338645418326693,
          "null_mean": 0.5473601852375148,
          "null_q95": 0.8055598588300081,
          "null_q99": 0.9575308062709029
        },
        "paired_ridge_hotelling": {
          "instrument": "paired_ridge_hotelling",
          "statistic": 0.8496710567763983,
          "permutations": 250,
          "p_value": 0.5258964143426295,
          "null_mean": 0.9797793670416481,
          "null_q95": 1.8973885102968926,
          "null_q99": 2.3011028145647248
        }
      },
      "paired_state_difference": {
        "symdiff": {
          "n": 24,
          "mean": 0.13732167198202702,
          "median": 0.14073126550229625,
          "std": 0.01421844212483485,
          "ci95_low": 0.13116006044772982,
          "ci95_high": 0.1426999819585852,
          "min": 0.11050663039782387,
          "max": 0.1787812041116006
        },
        "feature_distance": {
          "n": 24,
          "mean": 0.07499682200289116,
          "median": 0.06757717933697692,
          "std": 0.02308529559424737,
          "ci95_low": 0.06629283627237427,
          "ci95_high": 0.08490814251418749,
          "min": 0.03734898900341557,
          "max": 0.1436567063144855
        },
        "abs_population_difference": {
          "n": 24,
          "mean": 73.16666666666667,
          "median": 70.5,
          "std": 44.602565945121235,
          "ci95_low": 55.202083333333334,
          "ci95_high": 91.64895833333333,
          "min": 2.0,
          "max": 177.0
        }
      },
      "top_directional_features": [
        {
          "feature_index": 10,
          "feature_name": "degree_1",
          "mean_standardized_delta_A_minus_B": 0.5242109108207714
        },
        {
          "feature_index": 23,
          "feature_name": "harmonic6_sin",
          "mean_standardized_delta_A_minus_B": 0.4153369591068828
        },
        {
          "feature_index": 14,
          "feature_name": "degree_5",
          "mean_standardized_delta_A_minus_B": 0.4069794530964665
        },
        {
          "feature_index": 9,
          "feature_name": "mean_degree",
          "mean_standardized_delta_A_minus_B": -0.3833628519834154
        },
        {
          "feature_index": 15,
          "feature_name": "degree_6",
          "mean_standardized_delta_A_minus_B": -0.33246984243508654
        },
        {
          "feature_index": 8,
          "feature_name": "boundary_fraction",
          "mean_standardized_delta_A_minus_B": 0.33246984243508326
        }
      ],
      "steps_since_last_pulse_A": 16,
      "steps_since_last_pulse_B": 16,
      "equal_time_since_last_pulse": true
    }
  },
  "interpretation": "Paired trajectories may diverge strongly even when there is no consistent directional arrangement signature. V3 records candidate tests but defers scientific interpretation until their sensitivity has been calibrated."
}
```


# Stage 4 — Known-Null Calibration

```json
{
  "known_null": true,
  "endpoint": 20,
  "sham_reps": 20,
  "alpha": 0.05,
  "false_positive_count": 0,
  "false_positive_rate": 0.0,
  "p_value_summary": {
    "n": 20,
    "mean": 0.5388446215139442,
    "median": 0.46812749003984067,
    "std": 0.2957449575552664,
    "ci95_low": 0.41761454183266933,
    "ci95_high": 0.667808764940239,
    "min": 0.055776892430278883,
    "max": 1.0
  },
  "interpretation": "A small sham set can reveal gross anti-conservatism but cannot certify a nominal 5% false-positive rate."
}
```


# Stage 5 — Which Measurement Can Actually Resolve a Known Difference?

```json
{
  "endpoint": 20,
  "calibration_reps": 40,
  "permutations_per_test": 100,
  "candidate_instruments": [
    "energy_distance",
    "paired_mean_l2",
    "paired_max_abs_mean",
    "paired_ridge_hotelling"
  ],
  "effect_families": [
    "single_feature",
    "sparse_three",
    "dense_pc1"
  ],
  "strengths_are_standardized_multivariate_shift_norms": true,
  "selection_thresholds": {
    "max_null_fpr": 0.1,
    "target_shift_norm": 1.0,
    "min_power_at_target": 0.8
  },
  "instruments": {
    "energy_distance": {
      "families": {
        "single_feature": {
          "description": "single feature: cov_anisotropy",
          "feature_indices": [
            7
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "sparse_three": {
          "description": "equal standardized shift across top-variance features",
          "feature_indices": [
            7,
            19,
            1
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "dense_pc1": {
          "description": "leading principal direction of standardized baseline features",
          "feature_indices": null,
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.010148514851485154
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        }
      },
      "worst_null_fpr": 1.0,
      "worst_target_power": 1.0,
      "mean_target_power": 1.0,
      "eligible": false
    },
    "paired_mean_l2": {
      "families": {
        "single_feature": {
          "description": "single feature: cov_anisotropy",
          "feature_indices": [
            7
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.575,
              "mean_p_value": 0.06237623762376241
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.625,
              "mean_p_value": 0.05569306930693071
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.65,
              "mean_p_value": 0.053712871287128726
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.85,
              "mean_p_value": 0.041089108910891105
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 0.9,
              "mean_p_value": 0.029702970297029712
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 0.95,
              "mean_p_value": 0.01806930693069308
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.011633663366336639
            }
          ]
        },
        "sparse_three": {
          "description": "equal standardized shift across top-variance features",
          "feature_indices": [
            7,
            19,
            1
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.6,
              "mean_p_value": 0.06460396039603963
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.6,
              "mean_p_value": 0.05792079207920795
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.8,
              "mean_p_value": 0.0415841584158416
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.925,
              "mean_p_value": 0.024504950495049516
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 0.925,
              "mean_p_value": 0.017574257425742583
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01163366336633664
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "dense_pc1": {
          "description": "leading principal direction of standardized baseline features",
          "feature_indices": null,
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.55,
              "mean_p_value": 0.06831683168316835
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.55,
              "mean_p_value": 0.05148514851485151
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.725,
              "mean_p_value": 0.03465346534653467
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.975,
              "mean_p_value": 0.02425742574257427
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.013366336633663373
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.010396039603960402
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        }
      },
      "worst_null_fpr": 0.6,
      "worst_target_power": 0.9,
      "mean_target_power": 0.9416666666666668,
      "eligible": false
    },
    "paired_max_abs_mean": {
      "families": {
        "single_feature": {
          "description": "single feature: cov_anisotropy",
          "feature_indices": [
            7
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.325,
              "mean_p_value": 0.1487623762376238
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.275,
              "mean_p_value": 0.14628712871287133
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.375,
              "mean_p_value": 0.12054455445544558
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.55,
              "mean_p_value": 0.09282178217821786
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 0.675,
              "mean_p_value": 0.05544554455445546
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 0.925,
              "mean_p_value": 0.019059405940594066
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "sparse_three": {
          "description": "equal standardized shift across top-variance features",
          "feature_indices": [
            7,
            19,
            1
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.3,
              "mean_p_value": 0.15049504950495055
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.325,
              "mean_p_value": 0.1398514851485149
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.375,
              "mean_p_value": 0.1076732673267327
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.675,
              "mean_p_value": 0.06559405940594062
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 0.85,
              "mean_p_value": 0.029455445544554464
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.011138613861386145
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "dense_pc1": {
          "description": "leading principal direction of standardized baseline features",
          "feature_indices": null,
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 0.3,
              "mean_p_value": 0.16138613861386145
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 0.375,
              "mean_p_value": 0.13217821782178224
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 0.425,
              "mean_p_value": 0.10495049504950496
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 0.45,
              "mean_p_value": 0.09331683168316834
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 0.575,
              "mean_p_value": 0.07178217821782182
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 0.75,
              "mean_p_value": 0.04084158415841585
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 0.925,
              "mean_p_value": 0.021287128712871296
            }
          ]
        }
      },
      "worst_null_fpr": 0.325,
      "worst_target_power": 0.575,
      "mean_target_power": 0.6999999999999998,
      "eligible": false
    },
    "paired_ridge_hotelling": {
      "families": {
        "single_feature": {
          "description": "single feature: cov_anisotropy",
          "feature_indices": [
            7
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.014108910891089116
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.012871287128712874
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01064356435643565
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01064356435643565
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01163366336633664
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "sparse_three": {
          "description": "equal standardized shift across top-variance features",
          "feature_indices": [
            7,
            19,
            1
          ],
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01361386138613862
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.011881188118811887
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.01163366336633664
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.010148514851485154
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.010148514851485154
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        },
        "dense_pc1": {
          "description": "leading principal direction of standardized baseline features",
          "feature_indices": null,
          "results": [
            {
              "shift_norm": 0.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.013366336633663373
            },
            {
              "shift_norm": 0.25,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.012376237623762382
            },
            {
              "shift_norm": 0.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.012871287128712878
            },
            {
              "shift_norm": 0.75,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.011881188118811887
            },
            {
              "shift_norm": 1.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.010396039603960402
            },
            {
              "shift_norm": 1.5,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            },
            {
              "shift_norm": 2.0,
              "detection_rate_alpha_0_05": 1.0,
              "mean_p_value": 0.009900990099009906
            }
          ]
        }
      },
      "worst_null_fpr": 1.0,
      "worst_target_power": 1.0,
      "mean_target_power": 1.0,
      "eligible": false
    }
  },
  "selected_instrument": null,
  "measurement_ready": false,
  "selection_note": "Instrument selection uses only synthetic calibration. Real matched-arrangement p-values from Stage 3 are not used to choose the winner."
}
```


# Stage 6 — Bounded V3 Verdict

```json
{
  "experiment_role": "EXPLORATORY / MEASUREMENT-RESOLUTION",
  "single_pulse_response": "MEASURED",
  "single_pulse_latest_observation": 32,
  "single_pulse_causal_symdiff_mean": 0.12968415596747898,
  "independent_stochastic_symdiff_mean": 0.1387010895940292,
  "single_pulse_exceeds_stochastic_spread_descriptively": false,
  "ensemble_superposition": "MEASURED",
  "measurement_ready": false,
  "selected_instrument": null,
  "matched_endpoint_arrangement_status": "UNTESTED",
  "matched_endpoint_primary_endpoint": 20,
  "selected_real_test": null,
  "pipeline_sham_false_positive_rate": 0.0,
  "bounded_statement": "No candidate measurement instrument met the predeclared null-control and sensitivity requirements. The matched interior-timing hypothesis therefore remains unresolved under this quick protocol.",
  "nonclaims": [
    "information storage",
    "memory",
    "signalling",
    "semantics",
    "sender identity",
    "coordination",
    "learning",
    "agency",
    "individuality",
    "life",
    "Shannon channel capacity"
  ],
  "next_decision_logic": {
    "if_no_instrument_is_ready": "Do not scale the real matched-arrangement experiment blindly. Improve sample size or measurement design using the synthetic calibration benchmark first.",
    "if_instrument_ready_and_real_positive": "Freeze the selected instrument, endpoint, codewords and analysis plan, then run an independent confirmatory Chapter 17 replication before using the result in Chapter 18.",
    "if_instrument_ready_and_real_negative": "Record matched interior timing as FAILED under the calibrated protocol; do not reinterpret the old L3 decoder result as temporal retention.",
    "if_superposition_residual_large": "Investigate why the ensemble additive response model fails before using information-processing language."
  }
}
```
