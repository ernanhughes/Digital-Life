# Chapter 17 — How Does the Crystal Respond to Perturbation?

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-perturbation-dynamics-v1",
  "schema_version": 1,
  "chapter": 17,
  "chapter_title": "How Does the Crystal Respond to Perturbation?",
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
    "max_capacity_fraction": 0.85
  },
  "seed": 20260812,
  "matched_codeword_A": "1110000000000001",
  "matched_codeword_B": "1000000110000001",
  "scientific_boundary": "Perturbation-response characterization only. The old information-survival question is deferred to Chapter 18.",
  "started_at_unix": 1786528656.0489523,
  "finished_at_unix": 1786528690.9552662,
  "reproducibility_passed": true,
  "final_status": "FAILED",
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


# Stage 1 — Measure One Pulse Before Calling Anything a Channel

A single isolated pulse is compared against an exact matched baseline:
same checkpoint, same RNG state, same future environment, pulse bit only changed.

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
  "summary": {
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
      },
      "attachment_delta": {
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
      },
      "attachment_delta": {
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
      },
      "attachment_delta": {
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
        "ci95_low": 2.5614583333333334,
        "ci95_high": 4.75,
        "min": -3.0,
        "max": 9.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 4.083333333333333,
        "median": 3.5,
        "std": 2.2157893000513886,
        "ci95_low": 3.269791666666667,
        "ci95_high": 4.896875,
        "min": 0.0,
        "max": 9.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.016157838252217806,
        "median": 0.013351349038845474,
        "std": 0.008973889868871928,
        "ci95_low": 0.012625354890855159,
        "ci95_high": 0.019373164497043092,
        "min": 0.004073319755600814,
        "max": 0.04025423728813559
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.026820487289267916,
        "median": 0.024977497364911106,
        "std": 0.012431515191164866,
        "ci95_low": 0.022124739359359852,
        "ci95_high": 0.03194721568273672,
        "min": 0.009657149388112612,
        "max": 0.05748886191975701
      },
      "attachment_delta": {
        "n": 24,
        "mean": 3.6666666666666665,
        "median": 3.5,
        "std": 2.852873794770615,
        "ci95_low": 2.5,
        "ci95_high": 4.877083333333331,
        "min": -3.0,
        "max": 9.0
      }
    },
    "6": {
      "population_delta": {
        "n": 24,
        "mean": 2.7083333333333335,
        "median": 3.5,
        "std": 5.247850088898839,
        "ci95_low": 0.2895833333333334,
        "ci95_high": 5.0,
        "min": -7.0,
        "max": 11.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 4.958333333333333,
        "median": 4.5,
        "std": 3.2077921621507146,
        "ci95_low": 3.6031250000000004,
        "ci95_high": 6.230208333333333,
        "min": 0.0,
        "max": 11.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.07109049693964477,
        "median": 0.07541967258601553,
        "std": 0.029253036117478728,
        "ci95_low": 0.059508381526808464,
        "ci95_high": 0.08261878155457297,
        "min": 0.012170385395537525,
        "max": 0.12080536912751678
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.04133515561367376,
        "median": 0.03877962275559663,
        "std": 0.019488405595233467,
        "ci95_low": 0.03367897927827465,
        "ci95_high": 0.04979328037955338,
        "min": 0.009439131013793333,
        "max": 0.09443566390619593
      },
      "attachment_delta": {
        "n": 24,
        "mean": -0.9583333333333334,
        "median": -0.5,
        "std": 3.834918150654877,
        "ci95_low": -2.4583333333333335,
        "ci95_high": 0.4604166666666648,
        "min": -8.0,
        "max": 5.0
      }
    },
    "8": {
      "population_delta": {
        "n": 24,
        "mean": 2.9166666666666665,
        "median": 2.0,
        "std": 7.889426820470265,
        "ci95_low": -0.08333333333333333,
        "ci95_high": 6.39895833333333,
        "min": -11.0,
        "max": 18.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 6.416666666666667,
        "median": 4.5,
        "std": 5.438417866336577,
        "ci95_low": 4.333333333333333,
        "ci95_high": 8.583333333333334,
        "min": 1.0,
        "max": 18.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.13215110342206302,
        "median": 0.12833524006347566,
        "std": 0.01972492440346995,
        "ci95_low": 0.1244389157986303,
        "ci95_high": 0.13971208802820628,
        "min": 0.09149277688603531,
        "max": 0.1724137931034483
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.05367048814050965,
        "median": 0.048458031186609636,
        "std": 0.012863489182283003,
        "ci95_low": 0.049073466924513434,
        "ci95_high": 0.05872820109596396,
        "min": 0.0337351931454601,
        "max": 0.08019324841709108
      },
      "attachment_delta": {
        "n": 24,
        "mean": -0.375,
        "median": -1.0,
        "std": 5.779363430920975,
        "ci95_low": -2.625,
        "ci95_high": 1.9802083333333325,
        "min": -12.0,
        "max": 12.0
      }
    },
    "12": {
      "population_delta": {
        "n": 24,
        "mean": 2.2083333333333335,
        "median": -0.5,
        "std": 21.737025184897977,
        "ci95_low": -6.690625,
        "ci95_high": 10.813541666666666,
        "min": -48.0,
        "max": 41.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 17.625,
        "median": 14.0,
        "std": 12.912566553555493,
        "ci95_low": 12.833333333333334,
        "ci95_high": 22.563541666666666,
        "min": 0.0,
        "max": 48.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1515875680323273,
        "median": 0.14934440316533354,
        "std": 0.015592125869166125,
        "ci95_low": 0.14523854548896167,
        "ci95_high": 0.15751398928482174,
        "min": 0.12049433573635428,
        "max": 0.1776061776061776
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.0642876435471522,
        "median": 0.06358037237516952,
        "std": 0.015176424988512245,
        "ci95_low": 0.058879602623941416,
        "ci95_high": 0.07027459265265255,
        "min": 0.04007797187273533,
        "max": 0.10451019273843064
      },
      "attachment_delta": {
        "n": 24,
        "mean": -2.0833333333333335,
        "median": -2.0,
        "std": 9.241738052023669,
        "ci95_low": -5.583333333333333,
        "ci95_high": 1.418749999999998,
        "min": -23.0,
        "max": 20.0
      }
    },
    "16": {
      "population_delta": {
        "n": 24,
        "mean": -4.416666666666667,
        "median": -11.0,
        "std": 34.35830402618202,
        "ci95_low": -17.646875,
        "ci95_high": 8.99062499999999,
        "min": -77.0,
        "max": 66.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 28.833333333333332,
        "median": 25.5,
        "std": 19.19997106479301,
        "ci95_low": 21.662499999999998,
        "ci95_high": 36.12916666666666,
        "min": 5.0,
        "max": 77.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.15338618718898753,
        "median": 0.15363494485676632,
        "std": 0.010926402008409237,
        "ci95_low": 0.14900506765653973,
        "ci95_high": 0.15734221961308767,
        "min": 0.13232963549920762,
        "max": 0.17558528428093645
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06388558089033386,
        "median": 0.05935376316745995,
        "std": 0.019522257295951074,
        "ci95_low": 0.05707778580246291,
        "ci95_high": 0.07178064128195304,
        "min": 0.03724971027264308,
        "max": 0.10901157326849294
      },
      "attachment_delta": {
        "n": 24,
        "mean": -1.5416666666666667,
        "median": -0.5,
        "std": 9.907821685696385,
        "ci95_low": -5.791666666666667,
        "ci95_high": 2.42083333333333,
        "min": -22.0,
        "max": 24.0
      }
    },
    "20": {
      "population_delta": {
        "n": 24,
        "mean": -2.875,
        "median": -3.5,
        "std": 48.27724835088816,
        "ci95_low": -21.240624999999998,
        "ci95_high": 15.44479166666666,
        "min": -80.0,
        "max": 102.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 37.375,
        "median": 28.5,
        "std": 30.693121514980085,
        "ci95_low": 25.186458333333334,
        "ci95_high": 49.21041666666667,
        "min": 1.0,
        "max": 102.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.14257306027149852,
        "median": 0.14213917076402693,
        "std": 0.014807111772026106,
        "ci95_low": 0.13677916558148842,
        "ci95_high": 0.14911641057411895,
        "min": 0.11626468769325912,
        "max": 0.18199867637326275
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06279480650330589,
        "median": 0.06207286325435221,
        "std": 0.01877985171615559,
        "ci95_low": 0.05514991139665323,
        "ci95_high": 0.07079757176218761,
        "min": 0.023673356551084775,
        "max": 0.10143914799550893
      },
      "attachment_delta": {
        "n": 24,
        "mean": 0.2916666666666667,
        "median": 1.0,
        "std": 11.465452333956225,
        "ci95_low": -4.708333333333333,
        "ci95_high": 4.855208333333333,
        "min": -24.0,
        "max": 16.0
      }
    },
    "24": {
      "population_delta": {
        "n": 24,
        "mean": -4.333333333333333,
        "median": -4.0,
        "std": 59.58863612766746,
        "ci95_low": -27.98645833333333,
        "ci95_high": 19.833333333333332,
        "min": -95.0,
        "max": 146.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 45.166666666666664,
        "median": 35.0,
        "std": 39.109532796436675,
        "ci95_low": 30.25,
        "ci95_high": 60.97499999999998,
        "min": 1.0,
        "max": 146.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.1411673881915211,
        "median": 0.14077104601044754,
        "std": 0.015561856633866842,
        "ci95_low": 0.13561637275120988,
        "ci95_high": 0.14753298880576626,
        "min": 0.12088428974600188,
        "max": 0.19004065040650406
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06343344651526404,
        "median": 0.059840144710040705,
        "std": 0.02112881347283392,
        "ci95_low": 0.055803182835590166,
        "ci95_high": 0.07229086292906733,
        "min": 0.03626554946587114,
        "max": 0.1286118041100905
      },
      "attachment_delta": {
        "n": 24,
        "mean": -0.4583333333333333,
        "median": 1.0,
        "std": 9.069082858199549,
        "ci95_low": -3.91875,
        "ci95_high": 2.9802083333333322,
        "min": -15.0,
        "max": 23.0
      }
    },
    "32": {
      "population_delta": {
        "n": 24,
        "mean": -9.166666666666666,
        "median": -25.0,
        "std": 89.64544358502307,
        "ci95_low": -45.7625,
        "ci95_high": 25.87708333333333,
        "min": -134.0,
        "max": 211.0
      },
      "absolute_population_delta": {
        "n": 24,
        "mean": 74.41666666666667,
        "median": 85.5,
        "std": 50.818235462829236,
        "ci95_low": 54.884375,
        "ci95_high": 97.08333333333333,
        "min": 2.0,
        "max": 211.0
      },
      "symdiff": {
        "n": 24,
        "mean": 0.12968415596747898,
        "median": 0.12714240357838047,
        "std": 0.014049783369147872,
        "ci95_low": 0.12441753415924002,
        "ci95_high": 0.13571490292726543,
        "min": 0.11002285341168788,
        "max": 0.16525974025974027
      },
      "feature_distance": {
        "n": 24,
        "mean": 0.06411730533411028,
        "median": 0.0663059119211224,
        "std": 0.018687649773859626,
        "ci95_low": 0.05630347570773738,
        "ci95_high": 0.07105445008436573,
        "min": 0.03335826127715101,
        "max": 0.10212078807670032
      },
      "attachment_delta": {
        "n": 24,
        "mean": 1.5416666666666667,
        "median": 1.5,
        "std": 11.489049738289452,
        "ci95_low": -2.901041666666666,
        "ci95_high": 6.127083333333331,
        "min": -21.0,
        "max": 36.0
      }
    }
  }
}
```


# Stage 2 — Does One-Pulse Physics Explain the Pulse Train?

```json
{
  "measurement_space": "24 normalized morphology features",
  "clustered_positions_zero_indexed": [
    0,
    1,
    2,
    15
  ],
  "dispersed_positions_zero_indexed": [
    0,
    7,
    8,
    15
  ],
  "same_onset": true,
  "same_offset": true,
  "same_pulse_count": true,
  "interpretation": "Relative superposition error near zero means additive single-pulse responses explain the measured multi-pulse feature response. Large residuals indicate non-additivity in this measurement space; they do not by themselves establish memory or information storage.",
  "summary": {
    "16": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 1.9556257579355905,
          "median": 1.8631228358306187,
          "std": 0.8046977395498305,
          "ci95_low": 1.6560046641666966,
          "ci95_high": 2.321420301440538,
          "min": 0.17023213844759888,
          "max": 4.742318721454558
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.0798488856872377,
          "median": 0.07492773636626188,
          "std": 0.025001718730416823,
          "ci95_low": 0.07000759393302858,
          "ci95_high": 0.09052555528416695,
          "min": 0.04021333064351147,
          "max": 0.1352099865554188
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 1.6989270222606676,
          "median": 1.7821686321745107,
          "std": 0.5857359864270107,
          "ci95_low": 1.4602211854626845,
          "ci95_high": 1.9311412545920414,
          "min": 0.6510155948934933,
          "max": 3.0364429437530847
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08447046391735698,
          "median": 0.08150893200616818,
          "std": 0.025807907207906503,
          "ci95_low": 0.07410141774778553,
          "ci95_high": 0.0950957343318358,
          "min": 0.04058008160113168,
          "max": 0.1422744530010382
        }
      }
    },
    "18": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.0387455736955507,
          "median": 2.106272643828378,
          "std": 0.7888209063128497,
          "ci95_low": 1.7507540493374665,
          "ci95_high": 2.366722575955076,
          "min": 0.5965616609230034,
          "max": 3.6031761598269236
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08349979215756499,
          "median": 0.07566741222107805,
          "std": 0.023094255497871526,
          "ci95_low": 0.07520177423142174,
          "ci95_high": 0.09365417680305987,
          "min": 0.04654279537679259,
          "max": 0.13004658096249538
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 1.9210846319661663,
          "median": 1.811024118379457,
          "std": 0.6485828900911216,
          "ci95_low": 1.6506178001638896,
          "ci95_high": 2.2045237704473566,
          "min": 0.7940553038792173,
          "max": 3.6394885448160688
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08270229016945897,
          "median": 0.08249579334606573,
          "std": 0.02598462848924535,
          "ci95_low": 0.07366276068763895,
          "ci95_high": 0.09264400169262581,
          "min": 0.04471421238231993,
          "max": 0.14593659951628982
        }
      }
    },
    "20": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.061408943446956,
          "median": 1.9716579507841103,
          "std": 1.0620750282622478,
          "ci95_low": 1.6761613561508553,
          "ci95_high": 2.457417870615587,
          "min": 0.6204711253539112,
          "max": 5.971405611941477
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08130381465654106,
          "median": 0.08196339511881641,
          "std": 0.02182771706270779,
          "ci95_low": 0.07347214610759112,
          "ci95_high": 0.09101231444806157,
          "min": 0.04178075857787029,
          "max": 0.1256345390781315
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 1.805493169735115,
          "median": 1.810783887337195,
          "std": 0.5157263048175068,
          "ci95_low": 1.6034583842019645,
          "ci95_high": 2.01144164197177,
          "min": 0.7870664614593007,
          "max": 2.909903395453096
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08162479193510863,
          "median": 0.07590327203890435,
          "std": 0.026090744394668346,
          "ci95_low": 0.0712660450574102,
          "ci95_high": 0.0932339373756884,
          "min": 0.04205836019904373,
          "max": 0.1425191277432725
        }
      }
    },
    "24": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.12459653388389,
          "median": 1.734544423428697,
          "std": 1.1202568421482648,
          "ci95_low": 1.7208615309589825,
          "ci95_high": 2.5629696418771175,
          "min": 0.6652298581097668,
          "max": 6.227671934116434
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08149400060090096,
          "median": 0.07783489284450305,
          "std": 0.01692861595913536,
          "ci95_low": 0.07514668842984991,
          "ci95_high": 0.08844695051399692,
          "min": 0.05699468790671653,
          "max": 0.11718627596511738
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 1.8935679021068754,
          "median": 1.6273184069120232,
          "std": 0.7628549384265688,
          "ci95_low": 1.6296890426484139,
          "ci95_high": 2.2371897850898486,
          "min": 0.9131340332083868,
          "max": 4.08070194468499
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.0853030141179721,
          "median": 0.08336976790203462,
          "std": 0.026101090189387458,
          "ci95_low": 0.07529777247430514,
          "ci95_high": 0.09685270154921227,
          "min": 0.04619645932344415,
          "max": 0.14322305630735713
        }
      }
    },
    "28": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.2125335876853316,
          "median": 1.958123510753642,
          "std": 1.0584037878808612,
          "ci95_low": 1.7965786551804648,
          "ci95_high": 2.691263138536946,
          "min": 0.5078692644184988,
          "max": 5.294432423272478
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08047278862026326,
          "median": 0.08029299550005198,
          "std": 0.018608748686242866,
          "ci95_low": 0.07317508104644163,
          "ci95_high": 0.0870750345616116,
          "min": 0.053913160528799846,
          "max": 0.118827456548317
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.022741534726078,
          "median": 1.861956501422782,
          "std": 0.7820317145085625,
          "ci95_low": 1.7232374997387645,
          "ci95_high": 2.3263797247071087,
          "min": 0.7470096830397257,
          "max": 3.587757398628302
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.08325781370913661,
          "median": 0.07973493614381877,
          "std": 0.025462064731590642,
          "ci95_low": 0.0743431176997549,
          "ci95_high": 0.0936129840608807,
          "min": 0.038223763578593827,
          "max": 0.14307780154612854
        }
      }
    },
    "32": {
      "clustered": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.1658658925706056,
          "median": 1.9188602536891763,
          "std": 0.9054356493389627,
          "ci95_low": 1.8067923367285204,
          "ci95_high": 2.529359598636555,
          "min": 0.8604029330605675,
          "max": 4.471970355501604
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.07944355000542103,
          "median": 0.07953823015486897,
          "std": 0.019627410908966088,
          "ci95_low": 0.07229398350543349,
          "ci95_high": 0.08755392558644536,
          "min": 0.04176369406520364,
          "max": 0.11934956481310253
        }
      },
      "dispersed": {
        "relative_superposition_error": {
          "n": 24,
          "mean": 2.2464577641881696,
          "median": 1.9203323582141438,
          "std": 1.2433728167256453,
          "ci95_low": 1.794942618967873,
          "ci95_high": 2.8207627241483615,
          "min": 0.7341702129594389,
          "max": 6.473594473590047
        },
        "actual_feature_delta_norm": {
          "n": 24,
          "mean": 0.07947454164967105,
          "median": 0.0769376368999615,
          "std": 0.030579587044529306,
          "ci95_low": 0.06805216808917403,
          "ci95_high": 0.09105111528125227,
          "min": 0.024189972207513052,
          "max": 0.1496590637491618
        }
      }
    }
  }
}
```


# Stage 3 — Match Count, Onset and Offset; Change Only Interior Timing

This stage directly removes the recency-of-last-pulse confound.

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
  "primary_measurement": "decoder-free multivariate energy distance on normalized morphology features with paired within-group swap permutation",
  "secondary_measurements": "paired morphology symmetric difference, feature distance, absolute population difference",
  "results": {
    "16": {
      "energy_distance_test": {
        "statistic": 0.35943103490325257,
        "permutations": 250,
        "p_value": 0.6932270916334662,
        "null_mean": 0.4095140194760422,
        "null_q95": 0.5652551985637833,
        "null_q99": 0.6826037773117031,
        "null_max": 0.7330168302026516
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
      "steps_since_last_pulse_A": 0,
      "steps_since_last_pulse_B": 0,
      "equal_time_since_last_pulse": true
    },
    "18": {
      "energy_distance_test": {
        "statistic": 0.3394683981072033,
        "permutations": 250,
        "p_value": 0.8167330677290837,
        "null_mean": 0.3911175356976446,
        "null_q95": 0.49042359018513815,
        "null_q99": 0.5896790512420516,
        "null_max": 0.6473824213369701
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
      "steps_since_last_pulse_A": 2,
      "steps_since_last_pulse_B": 2,
      "equal_time_since_last_pulse": true
    },
    "20": {
      "energy_distance_test": {
        "statistic": 0.3623684840958967,
        "permutations": 250,
        "p_value": 0.6733067729083665,
        "null_mean": 0.3943650269440433,
        "null_q95": 0.5039718554234137,
        "null_q99": 0.5564876874558079,
        "null_max": 0.5939627146515605
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
      "steps_since_last_pulse_A": 4,
      "steps_since_last_pulse_B": 4,
      "equal_time_since_last_pulse": true
    },
    "24": {
      "energy_distance_test": {
        "statistic": 0.48481520900336683,
        "permutations": 250,
        "p_value": 0.09561752988047809,
        "null_mean": 0.40535266579661117,
        "null_q95": 0.5158368291966476,
        "null_q99": 0.5651970004634391,
        "null_max": 0.5876040262143638
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
      "steps_since_last_pulse_A": 8,
      "steps_since_last_pulse_B": 8,
      "equal_time_since_last_pulse": true
    },
    "28": {
      "energy_distance_test": {
        "statistic": 0.3730406798904058,
        "permutations": 250,
        "p_value": 0.7649402390438247,
        "null_mean": 0.4189043446415624,
        "null_q95": 0.5142506647359025,
        "null_q99": 0.5705774494185635,
        "null_max": 0.6732293798218674
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
      "steps_since_last_pulse_A": 12,
      "steps_since_last_pulse_B": 12,
      "equal_time_since_last_pulse": true
    },
    "32": {
      "energy_distance_test": {
        "statistic": 0.45472506894370124,
        "permutations": 250,
        "p_value": 0.450199203187251,
        "null_mean": 0.4482077131027827,
        "null_q95": 0.5594359129311518,
        "null_q99": 0.616734983767571,
        "null_max": 0.6859251283235421
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
      "steps_since_last_pulse_A": 16,
      "steps_since_last_pulse_B": 16,
      "equal_time_since_last_pulse": true
    }
  }
}
```


# Stage 4 — Does the Measuring Apparatus Invent Effects?

Known-null sham pseudoexperiments use the same treatment in both arms.

```json
{
  "known_null": true,
  "endpoint": 20,
  "same_codeword_both_pseudoarms": "1110000000000001",
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
  "minimum_p_value": 0.055776892430278883,
  "maximum_energy_statistic": 0.7659941246632656
}
```


# Stage 5 — Can the Measuring Apparatus Recover a Known Effect?

```json
{
  "known_effect_calibration": true,
  "endpoint": 20,
  "feature_index": 7,
  "feature_name": "cov_anisotropy",
  "empirical_feature_sd": 0.047899972633380486,
  "spike_in_reps": 100,
  "results": [
    {
      "shift_sd_units": 0.0,
      "detection_rate_alpha_0_05": 0.04,
      "p_value_mean": 0.5323383084577114,
      "p_value_median": 0.5547263681592041
    },
    {
      "shift_sd_units": 0.25,
      "detection_rate_alpha_0_05": 0.05,
      "p_value_mean": 0.4499004975124377,
      "p_value_median": 0.40796019900497515
    },
    {
      "shift_sd_units": 0.5,
      "detection_rate_alpha_0_05": 0.04,
      "p_value_mean": 0.40601990049751235,
      "p_value_median": 0.36318407960199006
    },
    {
      "shift_sd_units": 1.0,
      "detection_rate_alpha_0_05": 0.2,
      "p_value_mean": 0.2217910447761194,
      "p_value_median": 0.1791044776119403
    }
  ],
  "interpretation": "This does not test the crystal. It measures whether the declared two-sample pipeline can recover synthetic effects of known size."
}
```


# Stage 6 — Bounded Experimental Verdict

```json
{
  "experiment_role": "EXPLORATORY / MECHANISM CHARACTERIZATION",
  "single_pulse_response": "MEASURED",
  "superposition_characterized": "MEASURED",
  "matched_endpoint_arrangement_status": "FAILED",
  "matched_endpoint_primary_endpoint": 20,
  "matched_endpoint_p_value": 0.6733067729083665,
  "sham_false_positive_rate": 0.0,
  "bounded_statement": "At the declared matched-endpoint observation, this protocol did not establish a receiver-state distribution difference attributable to interior temporal arrangement.",
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
    "if_matched_endpoint_effect_absent": "Treat the old Chapter 17 L3 candidate as consistent with recency/ordinary response dynamics and push the information-survival interpretation back.",
    "if_effect_present_but_superposition_error_small": "Interpret the difference primarily through ordinary additive response dynamics; do not promote an information-retention claim.",
    "if_effect_present_and_superposition_error_material": "Freeze the matched-endpoint condition and design a separate Chapter 18 confirmatory information-survival experiment.",
    "if_sham_false_positive_rate_suspicious": "Do not trust the scientific endpoint until the analysis pipeline is repaired and the sham calibration is repeated."
  }
}
```
