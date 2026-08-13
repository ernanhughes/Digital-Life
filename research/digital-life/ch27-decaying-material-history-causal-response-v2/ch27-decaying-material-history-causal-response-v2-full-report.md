# Chapter 27 — Stored Material History and Downstream Causal Consequence (V2)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-decaying-material-history-causal-response-v2",
  "schema_version": 2,
  "chapter": 27,
  "chapter_title": "Can Stored Material History Change Downstream Causal Consequence?",
  "profile": "full",
  "seed": 20260915,
  "fresh_seed": true,
  "horizon": 12,
  "primary_SEI": 0.15,
  "history_k": 2,
  "local_history_radius": 3,
  "remote_min_distance": 15,
  "remote_influence_mass_tolerance": 0.05,
  "history_half_life": 6.0,
  "history_age": 3.0,
  "material_gain": 0.3,
  "primary_estimator": "lag-wise Rao-Blackwellized expected local causal consequence",
  "realized_secondary": true,
  "started_at_unix": 1786644336.8968437,
  "finished_at_unix": 1786647787.7911239,
  "final_status": "DOWNSTREAM_MATERIAL_HISTORY_EFFECT_UNRESOLVED"
}
```

---

## Stage 0 — Frozen V2 Protocol

```json
{
  "status": "FROZEN",
  "primary_contrast": "RB_G_local(accessible) - RB_G_local(remote)",
  "SEI_abs": 0.15,
  "construct_validity_fixes": [
    "PREVENT explicitly blocks x during lag 1",
    "FORCE contains x for exactly lag-1 growth exposure",
    "remote carrier influence matched to accessible carriers",
    "Rao-Blackwellized local expected consequence is primary"
  ],
  "frozen_from_v1": {
    "history_k": 2,
    "half_life": 6.0,
    "age": 3.0,
    "material_gain": 0.3,
    "horizon": 12,
    "allocation": "true_unbounded",
    "dynamic_prevent_matching": true
  },
  "stop_rule": "No parameter changes after full run. Increase groups only if unresolved solely from MDE."
}
```

---

## Stage 1 — Probe and Remote-Matching Support

```json
{
  "requested_groups": 192,
  "initial_probe_support": {
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
  },
  "groups_with_supported_probe": 192,
  "coverage_fraction": 1.0,
  "supported_probes": 564,
  "remote_matching_outcome_blind": true
}
```

---

## Stage 2 — Construct and Dynamic-Matching Validity

```json
{
  "record_level_match_pass_fraction": 1.0,
  "required_record_level_fraction": 0.95,
  "population_mean_every_arm_lag_within_2pct": true,
  "intervention_assertions_pass": true,
  "remote_matching_pass": true,
  "group_coverage_fraction": 1.0,
  "required_group_coverage": 0.9,
  "per_arm_lag": {
    "accessible": {
      "1": {
        "mean_relative_error": -5.040894383451536e-15,
        "within_2pct": true
      },
      "2": {
        "mean_relative_error": 4.592919462642848e-15,
        "within_2pct": true
      },
      "3": {
        "mean_relative_error": 4.180602240342749e-15,
        "within_2pct": true
      },
      "4": {
        "mean_relative_error": -5.574980745561663e-15,
        "within_2pct": true
      },
      "5": {
        "mean_relative_error": 3.5386936786193317e-15,
        "within_2pct": true
      },
      "6": {
        "mean_relative_error": -1.1365222794989272e-14,
        "within_2pct": true
      },
      "7": {
        "mean_relative_error": -3.601283785370351e-15,
        "within_2pct": true
      },
      "8": {
        "mean_relative_error": -3.469471613852763e-15,
        "within_2pct": true
      },
      "9": {
        "mean_relative_error": 5.528061180389841e-15,
        "within_2pct": true
      },
      "10": {
        "mean_relative_error": 9.290359472816345e-15,
        "within_2pct": true
      },
      "11": {
        "mean_relative_error": 5.45111151918441e-15,
        "within_2pct": true
      },
      "12": {
        "mean_relative_error": -1.2237955122988991e-14,
        "within_2pct": true
      }
    },
    "remote": {
      "1": {
        "mean_relative_error": 3.272568879285024e-15,
        "within_2pct": true
      },
      "2": {
        "mean_relative_error": 2.623256890033701e-15,
        "within_2pct": true
      },
      "3": {
        "mean_relative_error": -1.9024780094380018e-14,
        "within_2pct": true
      },
      "4": {
        "mean_relative_error": -1.7805481624669827e-15,
        "within_2pct": true
      },
      "5": {
        "mean_relative_error": -2.3658255428321325e-16,
        "within_2pct": true
      },
      "6": {
        "mean_relative_error": -2.464687010308767e-15,
        "within_2pct": true
      },
      "7": {
        "mean_relative_error": 6.7144670057806025e-15,
        "within_2pct": true
      },
      "8": {
        "mean_relative_error": -8.96832161137192e-15,
        "within_2pct": true
      },
      "9": {
        "mean_relative_error": 1.1863840554142322e-14,
        "within_2pct": true
      },
      "10": {
        "mean_relative_error": 1.3541799710910834e-14,
        "within_2pct": true
      },
      "11": {
        "mean_relative_error": 1.486716909264722e-14,
        "within_2pct": true
      },
      "12": {
        "mean_relative_error": -4.2534926008167266e-15,
        "within_2pct": true
      }
    }
  },
  "scientific_valid": true,
  "status": "PASS"
}
```

---

## Stage 3 — Arm Profiles

```json
{
  "accessible": {
    "RB_G_local": {
      "n": 192,
      "mean": 4.7876824193318,
      "sd": 6.177330683628526,
      "se": 0.44581044163328304,
      "ci95_low": 3.947771953123811,
      "ci95_high": 5.696142614268376,
      "achieved_mde80_one_sided": 1.1084964556804324
    },
    "G_local_realized": {
      "n": 192,
      "mean": 5.029079861111112,
      "sd": 6.932488421676853,
      "se": 0.5003092570511368,
      "ci95_low": 4.069010416666667,
      "ci95_high": 6.0360351562500005,
      "achieved_mde80_one_sided": 1.2440063901452847
    },
    "E1_ring1": {
      "n": 192,
      "mean": 1.1465554461483725,
      "sd": 0.28042292210524544,
      "se": 0.020237781195550614,
      "ci95_low": 1.1073403530603956,
      "ci95_high": 1.1854711934363413,
      "achieved_mde80_one_sided": 0.050320734175529756
    },
    "mean_offset": {
      "n": 192,
      "mean": -0.0009529390063325563,
      "sd": 0.006184641982463192,
      "se": 0.00044633808917707307,
      "ci95_low": -0.001826605346736016,
      "ci95_high": -0.00011618106496237011,
      "achieved_mde80_one_sided": 0.0011098084380332838
    }
  },
  "remote": {
    "RB_G_local": {
      "n": 192,
      "mean": 5.184927672087172,
      "sd": 6.727011241077159,
      "se": 0.48548021885969206,
      "ci95_low": 4.264315106814413,
      "ci95_high": 6.178372445517077,
      "achieved_mde80_one_sided": 1.2071343594765014
    },
    "G_local_realized": {
      "n": 192,
      "mean": 5.386284722222222,
      "sd": 7.404492918873032,
      "se": 0.5343732474905029,
      "ci95_low": 4.353244357638889,
      "ci95_high": 6.464008246527778,
      "achieved_mde80_one_sided": 1.3287056460219113
    },
    "E1_ring1": {
      "n": 192,
      "mean": 1.161540541097229,
      "sd": 0.2808554379625576,
      "se": 0.020268995338881608,
      "ci95_low": 1.1214032857424052,
      "ci95_high": 1.2006709400261875,
      "achieved_mde80_one_sided": 0.050398347358215086
    },
    "mean_offset": {
      "n": 192,
      "mean": 0.0001956404629547147,
      "sd": 0.004490253768868985,
      "se": 0.00032405615277328,
      "ci95_low": -0.0004334265107390839,
      "ci95_high": 0.0008268496758868303,
      "achieved_mde80_one_sided": 0.0008057574772690106
    }
  },
  "erased": {
    "RB_G_local": {
      "n": 192,
      "mean": 5.237338239936313,
      "sd": 6.570038737082578,
      "se": 0.474151704180112,
      "ci95_low": 4.334648463489264,
      "ci95_high": 6.184521267292055,
      "achieved_mde80_one_sided": 1.178966292518644
    },
    "G_local_realized": {
      "n": 192,
      "mean": 5.4578993055555545,
      "sd": 7.272544721984392,
      "se": 0.5248507066164101,
      "ci95_low": 4.4756835937499995,
      "ci95_high": 6.498296440972222,
      "achieved_mde80_one_sided": 1.3050280875301639
    },
    "E1_ring1": {
      "n": 192,
      "mean": 1.1614588565506534,
      "sd": 0.28078535055713194,
      "se": 0.020263937216082946,
      "ci95_low": 1.1233861950679243,
      "ci95_high": 1.2013346208429314,
      "achieved_mde80_one_sided": 0.05038577046303476
    },
    "mean_offset": {
      "n": 192,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    }
  }
}
```

---

## Stage 4 — Primary Rao-Blackwellized History Effect

```json
{
  "contrast": "RB_G_local(accessible) - RB_G_local(remote)",
  "SEI_abs": 0.15,
  "result": {
    "n": 192,
    "mean": -0.397245252755372,
    "sd": 1.9897764490744279,
    "se": 0.14359974606253734,
    "ci95_low": -0.678591722502727,
    "ci95_high": -0.11921972580277079,
    "achieved_mde80_one_sided": 0.3570571585621848
  },
  "status": "UNRESOLVED"
}
```

---

## Stage 5 — Secondary Realized and Immediate Effects

```json
{
  "realized_G_local_accessible_minus_remote": {
    "n": 192,
    "mean": -0.35720486111111116,
    "sd": 2.1964429702654176,
    "se": 0.15851461751780002,
    "ci95_low": -0.6727539062499999,
    "ci95_high": -0.04035373263888905,
    "achieved_mde80_one_sided": 0.39414261148364826
  },
  "E1_ring1_accessible_minus_remote": {
    "n": 192,
    "mean": -0.014985094948856631,
    "sd": 0.015943333723453842,
    "se": 0.0011506110021270144,
    "ci95_low": -0.017246777088205826,
    "ci95_high": -0.012809363612800682,
    "achieved_mde80_one_sided": 0.0028609653310315924
  },
  "CRN_pairing_realized_G": {
    "corr_accessible_remote": 0.9551779319759569
  },
  "remote_minus_erased": {
    "RB_G_local": {
      "n": 192,
      "mean": -0.05241056784914141,
      "sd": 0.9611165747125021,
      "se": 0.06936261414160927,
      "ci95_low": -0.2132761248818769,
      "ci95_high": 0.051369120138130914,
      "achieved_mde80_one_sided": 0.17246839632336472
    },
    "E1_ring1": {
      "n": 192,
      "mean": 8.168454657566202e-05,
      "sd": 0.0002442856635732462,
      "se": 1.762979920289751e-05,
      "ci95_low": 4.77062255049645e-05,
      "ci95_high": 0.00011621312756190798,
      "achieved_mde80_one_sided": 4.383605251409752e-05
    }
  },
  "accessible_minus_erased": {
    "RB_G_local": {
      "n": 192,
      "mean": -0.4496558206045134,
      "sd": 1.686771448013722,
      "se": 0.12173224369651216,
      "ci95_low": -0.7046776509621193,
      "ci95_high": -0.2270226258465292,
      "achieved_mde80_one_sided": 0.30268416366660567
    }
  }
}
```

---

## Stage 6 — Remote Carrier Matching Quality

```json
{
  "n_supported_probes": 564,
  "max_probability_mass_error": 0.049926890734826035,
  "mean_probability_mass_error": 0.01039771344866863,
  "tolerance": 0.05
}
```

---

## Stage 7 — Chapter 27 V2 Verdict

```json
{
  "validity": {
    "record_level_match_pass_fraction": 1.0,
    "required_record_level_fraction": 0.95,
    "population_mean_every_arm_lag_within_2pct": true,
    "intervention_assertions_pass": true,
    "remote_matching_pass": true,
    "group_coverage_fraction": 1.0,
    "required_group_coverage": 0.9,
    "per_arm_lag": {
      "accessible": {
        "1": {
          "mean_relative_error": -5.040894383451536e-15,
          "within_2pct": true
        },
        "2": {
          "mean_relative_error": 4.592919462642848e-15,
          "within_2pct": true
        },
        "3": {
          "mean_relative_error": 4.180602240342749e-15,
          "within_2pct": true
        },
        "4": {
          "mean_relative_error": -5.574980745561663e-15,
          "within_2pct": true
        },
        "5": {
          "mean_relative_error": 3.5386936786193317e-15,
          "within_2pct": true
        },
        "6": {
          "mean_relative_error": -1.1365222794989272e-14,
          "within_2pct": true
        },
        "7": {
          "mean_relative_error": -3.601283785370351e-15,
          "within_2pct": true
        },
        "8": {
          "mean_relative_error": -3.469471613852763e-15,
          "within_2pct": true
        },
        "9": {
          "mean_relative_error": 5.528061180389841e-15,
          "within_2pct": true
        },
        "10": {
          "mean_relative_error": 9.290359472816345e-15,
          "within_2pct": true
        },
        "11": {
          "mean_relative_error": 5.45111151918441e-15,
          "within_2pct": true
        },
        "12": {
          "mean_relative_error": -1.2237955122988991e-14,
          "within_2pct": true
        }
      },
      "remote": {
        "1": {
          "mean_relative_error": 3.272568879285024e-15,
          "within_2pct": true
        },
        "2": {
          "mean_relative_error": 2.623256890033701e-15,
          "within_2pct": true
        },
        "3": {
          "mean_relative_error": -1.9024780094380018e-14,
          "within_2pct": true
        },
        "4": {
          "mean_relative_error": -1.7805481624669827e-15,
          "within_2pct": true
        },
        "5": {
          "mean_relative_error": -2.3658255428321325e-16,
          "within_2pct": true
        },
        "6": {
          "mean_relative_error": -2.464687010308767e-15,
          "within_2pct": true
        },
        "7": {
          "mean_relative_error": 6.7144670057806025e-15,
          "within_2pct": true
        },
        "8": {
          "mean_relative_error": -8.96832161137192e-15,
          "within_2pct": true
        },
        "9": {
          "mean_relative_error": 1.1863840554142322e-14,
          "within_2pct": true
        },
        "10": {
          "mean_relative_error": 1.3541799710910834e-14,
          "within_2pct": true
        },
        "11": {
          "mean_relative_error": 1.486716909264722e-14,
          "within_2pct": true
        },
        "12": {
          "mean_relative_error": -4.2534926008167266e-15,
          "within_2pct": true
        }
      }
    },
    "scientific_valid": true,
    "status": "PASS"
  },
  "primary_status": "UNRESOLVED",
  "overall_status": "DOWNSTREAM_MATERIAL_HISTORY_EFFECT_UNRESOLVED",
  "bounded_claim": "The corrected experiment did not resolve the finite-horizon expected local causal consequence at the frozen +/-0.15 scale.",
  "V1_immediate_result_role": "Prior valid evidence; not re-promoted by V2.",
  "not_established": [
    "self-generated memory",
    "learning",
    "adaptation",
    "semantic memory",
    "individuality",
    "organism",
    "life"
  ],
  "stop_rule": "No parameter rescue. Increase groups only if unresolved solely because achieved MDE exceeds the frozen SEI."
}
```
