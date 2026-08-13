# Chapter 25 — How Does Finite Computation Create Non-Local Coupling? (V1)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-finite-budget-redistribution-v1",
  "schema_version": 1,
  "chapter": 25,
  "chapter_title": "How Does Finite Computation Create Non-Local Coupling?",
  "profile": "full",
  "profile_config": {
    "groups": 384,
    "source_profile": "full",
    "max_sites_per_fcp_per_group": 4,
    "bootstrap_reps": 7000,
    "scientific": true
  },
  "source_checkpoint_profile": {
    "groups": 384,
    "radius": 110,
    "warmup_steps": 24,
    "lossy_pre_steps": 28,
    "horizon": 12,
    "loss_rate": 0.08,
    "budget": 96,
    "radial_bin_width": 4,
    "high_fcp_min": 2,
    "low_fcp_max": -1,
    "minimum_fcp_difference": 3,
    "minimum_group_coverage_fraction": 0.5,
    "max_pairs_per_group": 10,
    "sei_E1": 0.1,
    "sei_g1": 0.1,
    "sei_divergence_probability": 0.05,
    "sei_GT": 0.15,
    "bootstrap_reps": 7000,
    "signflip_permutations": 20000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260911,
  "fresh_seed": true,
  "fractions": [
    0.05,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "low_budget_fractions": [
    0.05,
    0.1,
    0.25
  ],
  "supported_n": 1,
  "started_at_unix": 1786613024.8582716,
  "finished_at_unix": 1786613322.7212508,
  "final_status": "LOW_BUDGET_SCALING_SUPPORTED_EXTREME_RATIO_UNRESOLVED"
}
```

---

## Stage 0 — Frozen Chapter 25 V1 Protocol

```json
{
  "role": "FINITE-BUDGET CONTROL-PARAMETER EXPERIMENT",
  "same_checkpoint_across_budget_arms": true,
  "same_intervention_state_across_budget_arms": true,
  "budget_varies_only_at_lag1": true,
  "control_parameter": "B / max(F_force, F_prevent)",
  "fractions": [
    0.05,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "unbounded_arm": true,
  "primary_region": "outside nearest-neighbour causal cone: d > 1 at lag 1",
  "supported_scope": "occupied_neighbors = 1",
  "FCP_levels": [
    -1,
    0,
    1,
    2
  ],
  "H1": {
    "claim": "Low-budget outside-cone E_far scales with -DeltaF",
    "fractions": [
      0.05,
      0.1,
      0.25
    ],
    "relative_residual_tolerance": 0.25
  },
  "extreme_ratio": {
    "FCP_levels": [
      2,
      -1
    ],
    "target": -2.0,
    "relative_tolerance": 0.25
  },
  "FCP0_control": "composition substitution with size change removed",
  "full_evaluation_control": {
    "f=1.00": "hard outside-cone zero",
    "unbounded": "hard outside-cone zero",
    "tolerance": 1e-12
  },
  "scientific": true,
  "status": "FROZEN"
}
```

---

## Stage 1 — Frozen n=1 Site Support

```json
{
  "requested_groups": 384,
  "total_sites": 5375,
  "site_counts_by_FCP": {
    "-1": 1252,
    "0": 1200,
    "1": 1392,
    "2": 1531
  },
  "groups_with_level": {
    "-1": 369,
    "0": 375,
    "1": 380,
    "2": 384
  },
  "supported_regime": "occupied_neighbors = 1"
}
```

---

## Stage 2 — Same-Checkpoint Budget Sweep

```json
{
  "sites": 5375,
  "rows": 37625,
  "fractions": [
    0.05,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "unbounded_arm": true,
  "hard_full_evaluation_controls_checked": 10750,
  "status": "MEASURED"
}
```

---

## Stage 3 — FCP-Class Far-Field Effects by Budget Fraction

```json
{
  "f=0.05": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.011694082764280554,
        "ci95_low": 0.0061914245045421295,
        "ci95_high": 0.017531403855130256
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8084914182475159,
        "ci95_high": -0.7452574525745257
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.03545618789521228,
        "ci95_low": 0.025519421860885273,
        "ci95_high": 0.04652213188798554
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": -0.0018731076722308592,
        "ci95_low": -0.013445240612172178,
        "ci95_high": 0.010164010286772685
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.036444444444444446,
        "ci95_high": 0.12533888888888883
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.09911111111111111,
        "ci95_low": 0.07955,
        "ci95_high": 0.12022222222222222
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": -0.023461030601911338,
        "ci95_low": -0.036147895945005115,
        "ci95_high": -0.011623828227985572
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9517543859649121
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.13223684210526315,
        "ci95_low": 0.11359649122807017,
        "ci95_high": 0.15175986842105255
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": -0.04905015097664067,
        "ci95_low": -0.06171591898922925,
        "ci95_high": -0.03720115255687017
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.79296875,
        "ci95_high": 1.8865017361111114
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.17317708333333334,
        "ci95_low": 0.15234375,
        "ci95_high": 0.19596354166666666
      }
    }
  },
  "f=0.10": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.030609922645323397,
        "ci95_low": 0.0218277433116407,
        "ci95_high": 0.03985192048263831
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8091689250225835,
        "ci95_high": -0.7457091237579043
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.07971996386630532,
        "ci95_low": 0.06481481481481481,
        "ci95_high": 0.09575429087624208
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": -0.005436600214801799,
        "ci95_low": -0.019057469221049575,
        "ci95_high": 0.008720497583271248
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.03666666666666667,
        "ci95_high": 0.12377777777777778
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.172,
        "ci95_low": 0.1482222222222222,
        "ci95_high": 0.19755555555555554
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": -0.05377229109648131,
        "ci95_low": -0.06962265266482463,
        "ci95_high": -0.038490986090003135
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8738925438596491,
        "ci95_high": 0.9521984649122808
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.24100877192982456,
        "ci95_low": 0.21732456140350875,
        "ci95_high": 0.26535087719298245
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": -0.10982773521018312,
        "ci95_low": -0.12661762650111805,
        "ci95_high": -0.09285695576565456
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7936197916666667,
        "ci95_high": 1.8862901475694445
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.3274739583333333,
        "ci95_low": 0.2994791666666667,
        "ci95_high": 0.3541666666666667
      }
    }
  },
  "f=0.25": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.11795462409633418,
        "ci95_low": 0.10174119511579684,
        "ci95_high": 0.13417089800467108
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8091689250225836,
        "ci95_high": -0.7452518066847336
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.24367660343270098,
        "ci95_low": 0.2181571815718157,
        "ci95_high": 0.2692016711833784
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": 0.00019692339240604301,
        "ci95_low": -0.021099002221284035,
        "ci95_high": 0.02228266910716376
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.037111111111111116,
        "ci95_high": 0.12400555555555548
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.35311111111111115,
        "ci95_low": 0.32066666666666666,
        "ci95_high": 0.38467222222222214
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": -0.12391584293158382,
        "ci95_low": -0.14610894277797346,
        "ci95_high": -0.10125400254768788
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8739035087719298,
        "ci95_high": 0.9537280701754386
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.481578947368421,
        "ci95_low": 0.450438596491228,
        "ci95_high": 0.5136019736842106
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": -0.26141535457075316,
        "ci95_low": -0.2874887281730716,
        "ci95_high": -0.23687833075583029
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7918836805555554,
        "ci95_high": 1.8860677083333333
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.6753472222222222,
        "ci95_low": 0.6399739583333334,
        "ci95_high": 0.7105034722222222
      }
    }
  },
  "f=0.50": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.21272089879725478,
        "ci95_low": 0.19203389177084307,
        "ci95_high": 0.2338481871987206
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8109756097560976,
        "ci95_high": -0.7452574525745257
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.4464769647696477,
        "ci95_low": 0.41779019873532064,
        "ci95_high": 0.4749322493224932
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": -0.013038184328936178,
        "ci95_low": -0.03831757509923625,
        "ci95_high": 0.012473145795970732
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.036444444444444446,
        "ci95_high": 0.1257777777777778
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.4828888888888888,
        "ci95_low": 0.4491111111111112,
        "ci95_high": 0.5155555555555555
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": -0.2577732195288693,
        "ci95_low": -0.28560314089422795,
        "ci95_high": -0.22963475763171662
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8721491228070176,
        "ci95_high": 0.9513157894736842
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.7105263157894737,
        "ci95_low": 0.6719298245614035,
        "ci95_high": 0.7491228070175437
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": -0.49232224710933226,
        "ci95_low": -0.5268537617338124,
        "ci95_high": -0.458786566450495
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7929633246527779,
        "ci95_high": 1.8851996527777777
      },
      "far_symdiff": {
        "n": 384,
        "mean": 1.0336371527777777,
        "ci95_low": 0.9906684027777777,
        "ci95_high": 1.0776963975694442
      }
    }
  },
  "f=0.75": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.29354403154531816,
        "ci95_low": 0.26948571837016116,
        "ci95_high": 0.3175032417667066
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8084914182475158,
        "ci95_high": -0.7454832881662151
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.6542457091237579,
        "ci95_low": 0.6242095754290876,
        "ci95_high": 0.6829268292682927
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": -0.026063078322412135,
        "ci95_low": -0.052248542385290114,
        "ci95_high": 0.0004205956923392249
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.036222222222222225,
        "ci95_high": 0.12555555555555556
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.4673333333333333,
        "ci95_low": 0.43155,
        "ci95_high": 0.503561111111111
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": -0.3480616256861702,
        "ci95_low": -0.3769679238484583,
        "ci95_high": -0.31979925238004214
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9515405701754387
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.7916666666666667,
        "ci95_low": 0.7506578947368421,
        "ci95_high": 0.8335581140350876
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": -0.7145365420954978,
        "ci95_low": -0.7532302507018146,
        "ci95_high": -0.6770271979249894
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7936197916666667,
        "ci95_high": 1.8856336805555554
      },
      "far_symdiff": {
        "n": 384,
        "mean": 1.4010416666666667,
        "ci95_low": 1.3487358940972223,
        "ci95_high": 1.4559461805555554
      }
    }
  },
  "f=1.00": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8089430894308943,
        "ci95_high": -0.7450316169828364
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.03666666666666667,
        "ci95_high": 0.12511111111111112
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9528508771929824
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.791232638888889,
        "ci95_high": 1.8856391059027777
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    }
  },
  "unbounded": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8091689250225835,
        "ci95_high": -0.7459349593495935
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.03755555555555556,
        "ci95_high": 0.12644444444444447
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9517543859649124
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7925347222222223,
        "ci95_high": 1.8856336805555554
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    }
  }
}
```

---

## Stage 4 — Low-Budget -DeltaF Scaling

```json
{
  "fractions": {
    "f=0.05": {
      "beta_through_origin": 0.025090131345602402,
      "R2_through_origin": 0.977997543537707,
      "weighted_mean_absolute_residual": 0.0037287341836898173,
      "weighted_mean_absolute_predicted_magnitude": 0.029677809083552355,
      "relative_residual": 0.1256404801713044,
      "passes_25_percent_relative_residual": true,
      "classes": {
        "-1": {
          "minus_mean_deltaF": 0.7784552845528455,
          "observed_E_far": 0.011694082764280554,
          "predicted_E_far": 0.019531545336109186,
          "relative_residual": 0.401272015959691
        },
        "1": {
          "minus_mean_deltaF": -0.9125,
          "observed_E_far": -0.023461030601911338,
          "predicted_E_far": -0.022894744852862192,
          "relative_residual": 0.02473431141899583
        },
        "2": {
          "minus_mean_deltaF": -1.8389756944444444,
          "observed_E_far": -0.04905015097664067,
          "predicted_E_far": -0.0461401417149815,
          "relative_residual": 0.06306892769499892
        }
      }
    },
    "f=0.10": {
      "beta_through_origin": 0.05710454463812957,
      "R2_through_origin": 0.9867245379325175,
      "weighted_mean_absolute_residual": 0.006698334630762875,
      "weighted_mean_absolute_predicted_magnitude": 0.06754599050238304,
      "relative_residual": 0.0991670205876477,
      "passes_25_percent_relative_residual": true,
      "classes": {
        "-1": {
          "minus_mean_deltaF": 0.7784552845528455,
          "observed_E_far": 0.030609922645323397,
          "predicted_E_far": 0.04445333454553582,
          "relative_residual": 0.3114144763658148
        },
        "1": {
          "minus_mean_deltaF": -0.9125,
          "observed_E_far": -0.05377229109648131,
          "predicted_E_far": -0.052107896982293234,
          "relative_residual": 0.0319413027693989
        },
        "2": {
          "minus_mean_deltaF": -1.8389756944444444,
          "observed_E_far": -0.10982773521018312,
          "predicted_E_far": -0.1050138696318381,
          "relative_residual": 0.045840283718918816
        }
      }
    },
    "f=0.25": {
      "beta_through_origin": 0.14219886777379342,
      "R2_through_origin": 0.9991290071747312,
      "weighted_mean_absolute_residual": 0.004351873710953869,
      "weighted_mean_absolute_predicted_magnitude": 0.16819963162239968,
      "relative_residual": 0.025873265410733017,
      "passes_25_percent_relative_residual": true,
      "classes": {
        "-1": {
          "minus_mean_deltaF": 0.7784552845528455,
          "observed_E_far": 0.11795462409633418,
          "predicted_E_far": 0.11069546007594082,
          "relative_residual": 0.06557779348324977
        },
        "1": {
          "minus_mean_deltaF": -0.9125,
          "observed_E_far": -0.12391584293158382,
          "predicted_E_far": -0.1297564668435865,
          "relative_residual": 0.04501219903778042
        },
        "2": {
          "minus_mean_deltaF": -1.8389756944444444,
          "observed_E_far": -0.26141535457075316,
          "predicted_E_far": -0.26150026161352546,
          "relative_residual": 0.00032469199934413007
        }
      }
    }
  },
  "relative_residual_tolerance": 0.25,
  "status": "SUPPORTED"
}
```

---

## Stage 5 — Parameter-Free FCP +2 : -1 Ratio

```json
{
  "target_ratio": -2.0,
  "relative_tolerance": 0.25,
  "fractions": {
    "f=0.05": {
      "n_groups": 369,
      "ratio": -4.145023715213438,
      "ci95_low": -7.850415219958954,
      "ci95_high": -2.6160993508142436,
      "target": -2.0,
      "relative_error_from_minus2": 1.072511857606719,
      "within_25_percent_target": false
    },
    "f=0.10": {
      "n_groups": 369,
      "ratio": -3.5392194853490384,
      "ci95_low": -5.138516769032389,
      "ci95_high": -2.5670782965542664,
      "target": -2.0,
      "relative_error_from_minus2": 0.7696097426745192,
      "within_25_percent_target": false
    },
    "f=0.25": {
      "n_groups": 369,
      "ratio": -2.214602750781784,
      "ci95_low": -2.63364810547894,
      "ci95_high": -1.8851441626460792,
      "target": -2.0,
      "relative_error_from_minus2": 0.10730137539089202,
      "within_25_percent_target": true
    }
  },
  "status": "UNRESOLVED"
}
```

---

## Stage 6 — FCP=0 Composition-Only Control

```json
{
  "f=0.05": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.03755555555555556,
      "ci95_high": 0.12511111111111112
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.09911111111111111,
      "ci95_low": 0.07955555555555555,
      "ci95_high": 0.11933333333333333
    },
    "E_far": {
      "n": 375,
      "mean": -0.0018731076722308592,
      "ci95_low": -0.013522708034707651,
      "ci95_high": 0.01028663784581496
    }
  },
  "f=0.10": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.03555555555555556,
      "ci95_high": 0.12533333333333332
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.172,
      "ci95_low": 0.14910555555555555,
      "ci95_high": 0.19644444444444445
    },
    "E_far": {
      "n": 375,
      "mean": -0.005436600214801799,
      "ci95_low": -0.01914815065325503,
      "ci95_high": 0.008380042120966526
    }
  },
  "f=0.25": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.036444444444444446,
      "ci95_high": 0.1271166666666666
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.35311111111111115,
      "ci95_low": 0.32133333333333336,
      "ci95_high": 0.38533333333333336
    },
    "E_far": {
      "n": 375,
      "mean": 0.00019692339240604301,
      "ci95_low": -0.021194275253908056,
      "ci95_high": 0.021699860855788112
    }
  },
  "f=0.50": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.037555555555555564,
      "ci95_high": 0.12577777777777777
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.4828888888888888,
      "ci95_low": 0.4493333333333333,
      "ci95_high": 0.5157833333333333
    },
    "E_far": {
      "n": 375,
      "mean": -0.013038184328936178,
      "ci95_low": -0.039221427433277695,
      "ci95_high": 0.011767174084789112
    }
  },
  "f=0.75": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.036222222222222225,
      "ci95_high": 0.12688888888888888
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.4673333333333333,
      "ci95_low": 0.43266666666666664,
      "ci95_high": 0.5026666666666667
    },
    "E_far": {
      "n": 375,
      "mean": -0.026063078322412135,
      "ci95_low": -0.053811326413572426,
      "ci95_high": -0.00044644996550331295
    }
  },
  "f=1.00": {
    "actual_deltaF": {
      "n": 375,
      "mean": 0.08044444444444446,
      "ci95_low": 0.035555555555555556,
      "ci95_high": 0.12511111111111112
    },
    "far_symdiff": {
      "n": 375,
      "mean": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0
    },
    "E_far": {
      "n": 375,
      "mean": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0
    }
  }
}
```

---

## Stage 7 — Breakdown of the Low-Budget Linear Approximation

```json
{
  "-1": {
    "reference_E_far_at_0.10": 0.030609922645323397,
    "first_fraction_exceeding_25_percent_error": 0.25,
    "points": [
      {
        "fraction": 0.05,
        "observed_E_far": 0.011694082764280554,
        "linear_extrapolation_from_0.10": 0.015304961322661698,
        "relative_error": 0.23592863008641526
      },
      {
        "fraction": 0.1,
        "observed_E_far": 0.030609922645323397,
        "linear_extrapolation_from_0.10": 0.030609922645323397,
        "relative_error": 0.0
      },
      {
        "fraction": 0.25,
        "observed_E_far": 0.11795462409633418,
        "linear_extrapolation_from_0.10": 0.07652480661330849,
        "relative_error": 0.5413906851457577
      },
      {
        "fraction": 0.5,
        "observed_E_far": 0.21272089879725478,
        "linear_extrapolation_from_0.10": 0.15304961322661698,
        "relative_error": 0.38988197560671994
      },
      {
        "fraction": 0.75,
        "observed_E_far": 0.29354403154531816,
        "linear_extrapolation_from_0.10": 0.22957441983992546,
        "relative_error": 0.2786443356798922
      },
      {
        "fraction": 1.0,
        "observed_E_far": 0.0,
        "linear_extrapolation_from_0.10": 0.30609922645323395,
        "relative_error": 1.0
      }
    ]
  },
  "1": {
    "reference_E_far_at_0.10": -0.05377229109648131,
    "first_fraction_exceeding_25_percent_error": 1.0,
    "points": [
      {
        "fraction": 0.05,
        "observed_E_far": -0.023461030601911338,
        "linear_extrapolation_from_0.10": -0.026886145548240654,
        "relative_error": 0.12739330523163986
      },
      {
        "fraction": 0.1,
        "observed_E_far": -0.05377229109648131,
        "linear_extrapolation_from_0.10": -0.05377229109648131,
        "relative_error": 0.0
      },
      {
        "fraction": 0.25,
        "observed_E_far": -0.12391584293158382,
        "linear_extrapolation_from_0.10": -0.13443072774120327,
        "relative_error": 0.0782178671967169
      },
      {
        "fraction": 0.5,
        "observed_E_far": -0.2577732195288693,
        "linear_extrapolation_from_0.10": -0.26886145548240653,
        "relative_error": 0.04124144881103209
      },
      {
        "fraction": 0.75,
        "observed_E_far": -0.3480616256861702,
        "linear_extrapolation_from_0.10": -0.4032921832236098,
        "relative_error": 0.1369492388768081
      },
      {
        "fraction": 1.0,
        "observed_E_far": 0.0,
        "linear_extrapolation_from_0.10": -0.5377229109648131,
        "relative_error": 1.0
      }
    ]
  },
  "2": {
    "reference_E_far_at_0.10": -0.10982773521018312,
    "first_fraction_exceeding_25_percent_error": 1.0,
    "points": [
      {
        "fraction": 0.05,
        "observed_E_far": -0.04905015097664067,
        "linear_extrapolation_from_0.10": -0.05491386760509156,
        "relative_error": 0.10678025213265453
      },
      {
        "fraction": 0.1,
        "observed_E_far": -0.10982773521018312,
        "linear_extrapolation_from_0.10": -0.10982773521018312,
        "relative_error": 0.0
      },
      {
        "fraction": 0.25,
        "observed_E_far": -0.26141535457075316,
        "linear_extrapolation_from_0.10": -0.2745693380254578,
        "relative_error": 0.04790769264077484
      },
      {
        "fraction": 0.5,
        "observed_E_far": -0.49232224710933226,
        "linear_extrapolation_from_0.10": -0.5491386760509156,
        "relative_error": 0.10346462818859144
      },
      {
        "fraction": 0.75,
        "observed_E_far": -0.7145365420954978,
        "linear_extrapolation_from_0.10": -0.8237080140763734,
        "relative_error": 0.13253661505684142
      },
      {
        "fraction": 1.0,
        "observed_E_far": 0.0,
        "linear_extrapolation_from_0.10": -1.0982773521018312,
        "relative_error": 1.0
      }
    ]
  }
}
```

---

## Stage 8 — Full-Evaluation Hard-Zero Correctness Control

```json
{
  "f=1.00": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8089430894308943,
        "ci95_high": -0.7450316169828364
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.03666666666666667,
        "ci95_high": 0.12511111111111112
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9528508771929824
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.791232638888889,
        "ci95_high": 1.8856391059027777
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    }
  },
  "unbounded": {
    "-1": {
      "groups": 369,
      "E_far": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 369,
        "mean": -0.7784552845528455,
        "ci95_low": -0.8091689250225835,
        "ci95_high": -0.7459349593495935
      },
      "far_symdiff": {
        "n": 369,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "0": {
      "groups": 375,
      "E_far": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 375,
        "mean": 0.08044444444444446,
        "ci95_low": 0.03755555555555556,
        "ci95_high": 0.12644444444444447
      },
      "far_symdiff": {
        "n": 375,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "1": {
      "groups": 380,
      "E_far": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 380,
        "mean": 0.9125,
        "ci95_low": 0.8730263157894737,
        "ci95_high": 0.9517543859649124
      },
      "far_symdiff": {
        "n": 380,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    },
    "2": {
      "groups": 384,
      "E_far": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "actual_deltaF": {
        "n": 384,
        "mean": 1.8389756944444444,
        "ci95_low": 1.7925347222222223,
        "ci95_high": 1.8856336805555554
      },
      "far_symdiff": {
        "n": 384,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      }
    }
  },
  "assertion": "Every intervention passed exact outside-cone zero controls.",
  "tolerance": 1e-12,
  "status": "PASS"
}
```

---

## Stage 9 — Bounded Chapter 25 V1 Verdict

```json
{
  "overall_status": "LOW_BUDGET_SCALING_SUPPORTED_EXTREME_RATIO_UNRESOLVED",
  "bounded_claim": "Low-budget outside-cone effects followed the broader -DeltaF scaling criterion, but the parameter-free extreme-class ratio did not clear its frozen tolerance at every low-budget fraction.",
  "H1_low_budget_linearity": "SUPPORTED",
  "extreme_ratio": "UNRESOLVED",
  "full_evaluation_hard_zero": "PASS",
  "next_if_supported": "Use the measured breakdown curve as the finite-computation control law, then ask whether changing this control parameter changes downstream causal amplification / branching behaviour.",
  "next_if_unresolved": "Inspect exact finite-sampling combinatorics and composition substitution. Do not retune the FCP classes or fraction grid.",
  "stop_rule": "No rescue by changing the frozen fraction grid, FCP levels, n, or 25% residual criterion."
}
```
