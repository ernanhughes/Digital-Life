# Chapter 24 — Do Local Frontier Motifs Determine Causal Gain? (V2)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-local-frontier-motifs-v2",
  "schema_version": 2,
  "base_model_version": "digital-crystal-v1-frozen",
  "parent_experiment_version": "digital-crystal-finite-update-budget-v3",
  "chapter": 24,
  "chapter_title": "Where Is Causal Gain Created?",
  "run_title": "Do Local Frontier Motifs Determine Causal Gain?",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 76,
    "warmup_steps": 20,
    "lossy_pre_steps": 20,
    "horizon": 12,
    "loss_rate": 0.08,
    "budget": 96,
    "radial_bin_width": 3,
    "probability_tolerance": 0.05,
    "local_frontier_density_tolerance": 0.1,
    "max_sites_per_group": 32,
    "max_cross_pairs_per_group": 10,
    "max_same_pairs_per_group": 10,
    "minimum_motif_gain_contrast": 0.2,
    "minimum_motif_promoted_contrast": 0.5,
    "minimum_group_coverage_fraction": 0.7,
    "bootstrap_reps": 3000,
    "signflip_permutations": 8000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260907,
  "previous_seed": 20260906,
  "fresh_seed": true,
  "classifier_used": false,
  "canonical_rules_modified": false,
  "started_at_unix": 1786579006.1831093,
  "finished_at_unix": 1786579118.0278115,
  "final_status": "LOCAL_MOTIF_HYPOTHESIS_FAILED"
}
```

---

## Stage 0 — Frozen Chapter 24 V2 Protocol

```json
{
  "role": "EXACT LOCAL FRONTIER MOTIF / TRANSIENT CAUSAL GAIN TEST",
  "fresh_seed": 20260907,
  "motif": "six-neighbour occupancy pattern canonicalized under D6 rotation/reflection symmetry",
  "target": "transient causal gain G_T(H)",
  "horizon": 12,
  "pair_matching": {
    "same_occupied_neighbor_count": true,
    "same_radial_bin_width": 3,
    "max_baseline_p_difference": 0.05,
    "max_local_frontier_density_difference": 0.1
  },
  "H1": {
    "statistic": "mean abs gain difference cross-motif minus same-motif, one value per group",
    "minimum_effect": 0.2,
    "coverage": 0.7
  },
  "H2": {
    "statistic": "mean abs promoted-frontier difference cross-motif minus same-motif",
    "minimum_effect": 0.5
  },
  "classifier_used": false,
  "motif_specific_outcomes": "descriptive only in V2",
  "status": "FROZEN"
}
```

---

## Stage 1 — Exact Motif Interventions and Matched Pairs

```json
{
  "requested_groups": 48,
  "groups_with_cross_and_same_pairs": 45,
  "coverage_fraction": 0.9375,
  "minimum_coverage_fraction": 0.7,
  "coverage_gate_passed": true,
  "total_sites": 1536,
  "total_cross_pairs": 95,
  "total_same_pairs": 145,
  "motif_counts": {
    "000001": 169,
    "000011": 161,
    "000101": 138,
    "000111": 152,
    "001001": 70,
    "001011": 146,
    "001111": 144,
    "010101": 49,
    "010111": 140,
    "011011": 117,
    "011111": 136,
    "111111": 114
  },
  "number_of_observed_canonical_motifs": 12,
  "maximum_capacity_fraction": 0.03799054508173378,
  "capacity_gate_passed": true,
  "status": "MEASURED"
}
```

---

## Stage 2 — Primary Exact-Motif Tests

```json
{
  "H1_exact_motif_gain_contrast": {
    "cross_minus_same_abs_gain_difference": {
      "n": 45,
      "mean": -0.22518518518518513,
      "ci95_low": -0.6915,
      "ci95_high": 0.3071574074074079,
      "half_width": 0.49932870370370397
    },
    "minimum_effect": 0.2,
    "signflip": {
      "n": 45,
      "observed_mean": -0.22518518518518513,
      "p_value": 0.8018997625296838,
      "permutations": 8000
    }
  },
  "H2_exact_motif_opportunity_contrast": {
    "cross_minus_same_abs_promoted_frontier_difference": {
      "n": 45,
      "mean": 0.03962962962962964,
      "ci95_low": -0.09224074074074072,
      "ci95_high": 0.17039814814814824,
      "half_width": 0.1313194444444445
    },
    "minimum_effect": 0.5,
    "signflip": {
      "n": 45,
      "observed_mean": 0.03962962962962964,
      "p_value": 0.2723409573803275,
      "permutations": 8000
    }
  }
}
```

---

## Stage 3 — Descriptive Frontier-Motif Atlas

```json
{
  "canonical_motif_atlas": [
    {
      "motif": "000001",
      "occupied_neighbors": 1,
      "raw_site_count": 169,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.3822091405226513,
        "ci95_low": 0.37013971712490434,
        "ci95_high": 0.393107882482862,
        "half_width": 0.011484082678978824
      },
      "FCP": {
        "n": 48,
        "mean": 0.9652777777777778,
        "ci95_low": 0.7934027777777778,
        "ci95_high": 1.1319444444444444,
        "half_width": 0.16927083333333331
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 1.9652777777777777,
        "ci95_low": 1.8003472222222223,
        "ci95_high": 2.123307291666667,
        "half_width": 0.16148003472222228
      },
      "g1": {
        "n": 48,
        "mean": 0.234375,
        "ci95_low": 0.15277777777777776,
        "ci95_high": 0.3211805555555555,
        "half_width": 0.08420138888888888
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.3350694444444444,
        "ci95_low": 0.1284722222222222,
        "ci95_high": 0.5434027777777778,
        "half_width": 0.2074652777777778
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.08333333333333333,
        "ci95_low": -0.17191840277777776,
        "ci95_high": 0.31948784722222234,
        "half_width": 0.24570312500000005
      },
      "far_field_gain": {
        "n": 48,
        "mean": -0.2517361111111111,
        "ci95_low": -0.5416666666666666,
        "ci95_high": 0.04166666666666666,
        "half_width": 0.29166666666666663
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.994738828977341,
        "ci95_low": 0.9929750882960808,
        "ci95_high": 0.9961953930895849,
        "half_width": 0.0016101523967520515
      }
    },
    {
      "motif": "000011",
      "occupied_neighbors": 2,
      "raw_site_count": 161,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.21218815837429783,
        "ci95_low": 0.20005249177518705,
        "ci95_high": 0.225764939224466,
        "half_width": 0.012856223724639473
      },
      "FCP": {
        "n": 48,
        "mean": 0.18055555555555558,
        "ci95_low": 0.008680555555555561,
        "ci95_high": 0.35590277777777773,
        "half_width": 0.17361111111111108
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 1.1805555555555556,
        "ci95_low": 1.0016927083333331,
        "ci95_high": 1.3524305555555554,
        "half_width": 0.17536892361111112
      },
      "g1": {
        "n": 48,
        "mean": 0.16319444444444445,
        "ci95_low": 0.08155381944444445,
        "ci95_high": 0.24652777777777776,
        "half_width": 0.08248697916666665
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.4305555555555555,
        "ci95_low": 0.2013454861111111,
        "ci95_high": 0.7240017361111113,
        "half_width": 0.2613281250000001
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.09722222222222222,
        "ci95_low": -0.20486111111111108,
        "ci95_high": 0.3888888888888889,
        "half_width": 0.296875
      },
      "far_field_gain": {
        "n": 48,
        "mean": -0.3333333333333333,
        "ci95_low": -0.7309461805555555,
        "ci95_high": -0.010416666666666676,
        "half_width": 0.36026475694444443
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9946973113209467,
        "ci95_low": 0.992743521042115,
        "ci95_high": 0.9964122647658676,
        "half_width": 0.0018343718618762939
      }
    },
    {
      "motif": "000101",
      "occupied_neighbors": 2,
      "raw_site_count": 138,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.5728701978278978,
        "ci95_low": 0.5593373099689721,
        "ci95_high": 0.5845901592815421,
        "half_width": 0.012626424656284996
      },
      "FCP": {
        "n": 48,
        "mean": -0.5972222222222222,
        "ci95_low": -0.6909722222222223,
        "ci95_high": -0.5034722222222222,
        "half_width": 0.09375000000000006
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.40277777777777773,
        "ci95_low": 0.3107204861111111,
        "ci95_high": 0.49657118055555577,
        "half_width": 0.09292534722222234
      },
      "g1": {
        "n": 48,
        "mean": 0.10243055555555554,
        "ci95_low": 0.012152777777777781,
        "ci95_high": 0.20143229166666685,
        "half_width": 0.09463975694444453
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.10763888888888885,
        "ci95_low": -0.09375,
        "ci95_high": 0.34375,
        "half_width": 0.21875
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.08506944444444443,
        "ci95_low": -0.07638888888888888,
        "ci95_high": 0.2552083333333333,
        "half_width": 0.1657986111111111
      },
      "far_field_gain": {
        "n": 48,
        "mean": -0.022569444444444444,
        "ci95_low": -0.21701388888888884,
        "ci95_high": 0.15625000000000003,
        "half_width": 0.18663194444444442
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9976274568482398,
        "ci95_low": 0.9963137472342244,
        "ci95_high": 0.9986391305015315,
        "half_width": 0.0011626916336535675
      }
    },
    {
      "motif": "000111",
      "occupied_neighbors": 3,
      "raw_site_count": 152,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.7003529593133044,
        "ci95_low": 0.6877491206493481,
        "ci95_high": 0.7108905272991182,
        "half_width": 0.011570703324885023
      },
      "FCP": {
        "n": 48,
        "mean": -0.6128472222222222,
        "ci95_low": -0.6875,
        "ci95_high": -0.5381944444444444,
        "half_width": 0.07465277777777779
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.3871527777777777,
        "ci95_low": 0.3141927083333333,
        "ci95_high": 0.46184895833333345,
        "half_width": 0.07382812500000008
      },
      "g1": {
        "n": 48,
        "mean": 0.17708333333333334,
        "ci95_low": 0.1111111111111111,
        "ci95_high": 0.25,
        "half_width": 0.06944444444444445
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.12847222222222224,
        "ci95_low": -0.0034722222222222285,
        "ci95_high": 0.27777777777777773,
        "half_width": 0.14062499999999997
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.24479166666666666,
        "ci95_low": 0.09895833333333333,
        "ci95_high": 0.4062934027777779,
        "half_width": 0.1536675347222223
      },
      "far_field_gain": {
        "n": 48,
        "mean": 0.11631944444444443,
        "ci95_low": 0.029513888888888895,
        "ci95_high": 0.21875,
        "half_width": 0.09461805555555555
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9982906677110776,
        "ci95_low": 0.9975871462586953,
        "ci95_high": 0.9988704882905338,
        "half_width": 0.0006416710159192762
      }
    },
    {
      "motif": "001001",
      "occupied_neighbors": 2,
      "raw_site_count": 70,
      "groups_represented": 39,
      "baseline_p": {
        "n": 39,
        "mean": 0.5765057395950622,
        "ci95_low": 0.5645259298757949,
        "ci95_high": 0.5873173903398337,
        "half_width": 0.011395730232019396
      },
      "FCP": {
        "n": 39,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 39,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 39,
        "mean": 0.13247863247863245,
        "ci95_low": -0.00427350427350427,
        "ci95_high": 0.2863247863247863,
        "half_width": 0.14529914529914528
      },
      "G_transient_local": {
        "n": 39,
        "mean": 0.17521367521367523,
        "ci95_low": -0.09829059829059829,
        "ci95_high": 0.6324786324786325,
        "half_width": 0.36538461538461536
      },
      "G_transient_global": {
        "n": 39,
        "mean": 0.24358974358974358,
        "ci95_low": -0.08130341880341876,
        "ci95_high": 0.6923076923076923,
        "half_width": 0.3868055555555555
      },
      "far_field_gain": {
        "n": 39,
        "mean": 0.06837606837606837,
        "ci95_low": -0.038461538461538464,
        "ci95_high": 0.20512820512820512,
        "half_width": 0.12179487179487179
      },
      "mean_eval_overlap": {
        "n": 39,
        "mean": 0.9979643894715079,
        "ci95_low": 0.9967285600815302,
        "ci95_high": 0.999031673203249,
        "half_width": 0.0011515565608594125
      }
    },
    {
      "motif": "001011",
      "occupied_neighbors": 3,
      "raw_site_count": 146,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.700352959313304,
        "ci95_low": 0.6883852526341422,
        "ci95_high": 0.711035131976143,
        "half_width": 0.0113249396710004
      },
      "FCP": {
        "n": 48,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 48,
        "mean": 0.06249999999999999,
        "ci95_low": 0.006944444444444443,
        "ci95_high": 0.125,
        "half_width": 0.059027777777777776
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.03472222222222223,
        "ci95_low": -0.07638888888888888,
        "ci95_high": 0.17361111111111108,
        "half_width": 0.12499999999999997
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.060763888888888895,
        "ci95_low": -0.1024739583333333,
        "ci95_high": 0.23615451388888906,
        "half_width": 0.16931423611111118
      },
      "far_field_gain": {
        "n": 48,
        "mean": 0.026041666666666668,
        "ci95_low": -0.05559895833333332,
        "ci95_high": 0.1111111111111111,
        "half_width": 0.08335503472222222
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9984544823040467,
        "ci95_low": 0.9977393837060321,
        "ci95_high": 0.999072807448329,
        "half_width": 0.0006667118711484732
      }
    },
    {
      "motif": "001111",
      "occupied_neighbors": 4,
      "raw_site_count": 144,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.44806545523772773,
        "ci95_low": 0.4316766828515454,
        "ci95_high": 0.4662048426059862,
        "half_width": 0.017264079877220395
      },
      "FCP": {
        "n": 48,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 48,
        "mean": 0.10416666666666667,
        "ci95_low": 0.03472222222222222,
        "ci95_high": 0.18055555555555555,
        "half_width": 0.07291666666666667
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.0069444444444444475,
        "ci95_low": -0.15277777777777776,
        "ci95_high": 0.15277777777777776,
        "half_width": 0.15277777777777776
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.03472222222222221,
        "ci95_low": -0.2640625,
        "ci95_high": 0.284895833333334,
        "half_width": 0.274479166666667
      },
      "far_field_gain": {
        "n": 48,
        "mean": 0.02777777777777778,
        "ci95_low": -0.1666666666666667,
        "ci95_high": 0.18055555555555558,
        "half_width": 0.17361111111111116
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9986643425984368,
        "ci95_low": 0.9980920858463661,
        "ci95_high": 0.9991416240035532,
        "half_width": 0.0005247690785935566
      }
    },
    {
      "motif": "010101",
      "occupied_neighbors": 3,
      "raw_site_count": 49,
      "groups_represented": 31,
      "baseline_p": {
        "n": 31,
        "mean": 0.696112044057266,
        "ci95_low": 0.6813419231680848,
        "ci95_high": 0.7088165629643698,
        "half_width": 0.013737319898142475
      },
      "FCP": {
        "n": 31,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 31,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 31,
        "mean": 0.04838709677419355,
        "ci95_low": -0.04879032258064502,
        "ci95_high": 0.14516129032258066,
        "half_width": 0.09697580645161284
      },
      "G_transient_local": {
        "n": 31,
        "mean": 0.03225806451612903,
        "ci95_low": -0.12903225806451613,
        "ci95_high": 0.1774193548387097,
        "half_width": 0.1532258064516129
      },
      "G_transient_global": {
        "n": 31,
        "mean": -0.010752688172043015,
        "ci95_low": -0.2795698924731183,
        "ci95_high": 0.22580645161290322,
        "half_width": 0.25268817204301075
      },
      "far_field_gain": {
        "n": 31,
        "mean": -0.043010752688172046,
        "ci95_low": -0.22580645161290322,
        "ci95_high": 0.13440860215053763,
        "half_width": 0.18010752688172044
      },
      "mean_eval_overlap": {
        "n": 31,
        "mean": 0.9984147563477359,
        "ci95_low": 0.9964541774051779,
        "ci95_high": 0.9996304918153938,
        "half_width": 0.0015881572051079096
      }
    },
    {
      "motif": "010111",
      "occupied_neighbors": 4,
      "raw_site_count": 140,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.802976102337778,
        "ci95_low": 0.7933668456091985,
        "ci95_high": 0.8111082998709072,
        "half_width": 0.00887072713085435
      },
      "FCP": {
        "n": 48,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 48,
        "mean": 0.10763888888888888,
        "ci95_low": 0.05555555555555555,
        "ci95_high": 0.16675347222222253,
        "half_width": 0.05559895833333349
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.06597222222222221,
        "ci95_low": -0.03125,
        "ci95_high": 0.16666666666666666,
        "half_width": 0.09895833333333333
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.1909722222222222,
        "ci95_low": 0.017274305555555577,
        "ci95_high": 0.4166666666666666,
        "half_width": 0.1996961805555555
      },
      "far_field_gain": {
        "n": 48,
        "mean": 0.125,
        "ci95_low": -0.041666666666666664,
        "ci95_high": 0.375,
        "half_width": 0.20833333333333334
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9979368290757589,
        "ci95_low": 0.9968038471714834,
        "ci95_high": 0.9989341383575628,
        "half_width": 0.001065145593039718
      }
    },
    {
      "motif": "011011",
      "occupied_neighbors": 4,
      "raw_site_count": 117,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.8029761023377784,
        "ci95_low": 0.7939530202626769,
        "ci95_high": 0.8115518631919361,
        "half_width": 0.008799421464629587
      },
      "FCP": {
        "n": 48,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 48,
        "mean": 0.09027777777777778,
        "ci95_low": 0.03125,
        "ci95_high": 0.15277777777777776,
        "half_width": 0.06076388888888888
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.003472222222222219,
        "ci95_low": -0.1840277777777778,
        "ci95_high": 0.13888888888888887,
        "half_width": 0.16145833333333331
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.03472222222222222,
        "ci95_low": -0.16319444444444445,
        "ci95_high": 0.17361111111111113,
        "half_width": 0.1684027777777778
      },
      "far_field_gain": {
        "n": 48,
        "mean": 0.03125,
        "ci95_low": 0.0,
        "ci95_high": 0.08333333333333333,
        "half_width": 0.041666666666666664
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9991307766988915,
        "ci95_low": 0.9985974656445937,
        "ci95_high": 0.9995764127529592,
        "half_width": 0.0004894735541827178
      }
    },
    {
      "motif": "011111",
      "occupied_neighbors": 5,
      "raw_site_count": 136,
      "groups_represented": 48,
      "baseline_p": {
        "n": 48,
        "mean": 0.8767453348210497,
        "ci95_low": 0.8701013146950084,
        "ci95_high": 0.8823819200345351,
        "half_width": 0.006140302669763342
      },
      "FCP": {
        "n": 48,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 48,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 48,
        "mean": 0.07291666666666667,
        "ci95_low": 0.013888888888888888,
        "ci95_high": 0.13888888888888887,
        "half_width": 0.062499999999999986
      },
      "G_transient_local": {
        "n": 48,
        "mean": 0.07291666666666666,
        "ci95_low": -0.027777777777777776,
        "ci95_high": 0.2014756944444448,
        "half_width": 0.1146267361111113
      },
      "G_transient_global": {
        "n": 48,
        "mean": 0.048611111111111105,
        "ci95_low": -0.07638888888888888,
        "ci95_high": 0.18055555555555555,
        "half_width": 0.1284722222222222
      },
      "far_field_gain": {
        "n": 48,
        "mean": -0.024305555555555556,
        "ci95_low": -0.1042534722222222,
        "ci95_high": 0.05902777777777778,
        "half_width": 0.081640625
      },
      "mean_eval_overlap": {
        "n": 48,
        "mean": 0.9987490696406995,
        "ci95_low": 0.9982120797267153,
        "ci95_high": 0.9992266010134659,
        "half_width": 0.0005072606433753069
      }
    },
    {
      "motif": "111111",
      "occupied_neighbors": 6,
      "raw_site_count": 114,
      "groups_represented": 46,
      "baseline_p": {
        "n": 46,
        "mean": 0.9257095646765648,
        "ci95_low": 0.9210284649350696,
        "ci95_high": 0.9295115765454619,
        "half_width": 0.00424155580519614
      },
      "FCP": {
        "n": 46,
        "mean": -1.0,
        "ci95_low": -1.0,
        "ci95_high": -1.0,
        "half_width": 0.0
      },
      "promoted_frontier": {
        "n": 46,
        "mean": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0
      },
      "g1": {
        "n": 46,
        "mean": 0.05072463768115942,
        "ci95_low": 0.010869565217391304,
        "ci95_high": 0.09420289855072463,
        "half_width": 0.04166666666666666
      },
      "G_transient_local": {
        "n": 46,
        "mean": 0.03985507246376812,
        "ci95_low": -0.036231884057971,
        "ci95_high": 0.13768115942028986,
        "half_width": 0.08695652173913043
      },
      "G_transient_global": {
        "n": 46,
        "mean": 0.05072463768115942,
        "ci95_low": -0.05072463768115942,
        "ci95_high": 0.15217391304347824,
        "half_width": 0.10144927536231883
      },
      "far_field_gain": {
        "n": 46,
        "mean": 0.010869565217391302,
        "ci95_low": -0.05434782608695652,
        "ci95_high": 0.07971014492753624,
        "half_width": 0.06702898550724638
      },
      "mean_eval_overlap": {
        "n": 46,
        "mean": 0.9991159918322624,
        "ci95_low": 0.9986677623387618,
        "ci95_high": 0.9995019672294437,
        "half_width": 0.00041710244534098884
      }
    }
  ],
  "n2_subtypes_descriptive": {
    "adjacent": {
      "raw_site_count": 161,
      "mean_FCP": 0.17391304347826086,
      "mean_promoted_frontier": 1.173913043478261,
      "mean_G_transient_local": 0.391304347826087
    },
    "one_gap": {
      "raw_site_count": 138,
      "mean_FCP": -0.5797101449275363,
      "mean_promoted_frontier": 0.42028985507246375,
      "mean_G_transient_local": 0.09420289855072464
    },
    "opposite": {
      "raw_site_count": 70,
      "mean_FCP": -1.0,
      "mean_promoted_frontier": 0.0,
      "mean_G_transient_local": 0.04285714285714286
    }
  },
  "scope": "Motif-specific outcomes are descriptive in V2. No motif is promoted to a directional claim from this atlas."
}
```

---

## Stage 4 — Bounded Chapter 24 V2 Verdict

```json
{
  "validity": {
    "valid": true,
    "coverage_gate": true,
    "capacity_gate": true
  },
  "H1": {
    "status": "FAILED",
    "result": {
      "cross_minus_same_abs_gain_difference": {
        "n": 45,
        "mean": -0.22518518518518513,
        "ci95_low": -0.6915,
        "ci95_high": 0.3071574074074079,
        "half_width": 0.49932870370370397
      },
      "minimum_effect": 0.2,
      "signflip": {
        "n": 45,
        "observed_mean": -0.22518518518518513,
        "p_value": 0.8018997625296838,
        "permutations": 8000
      }
    }
  },
  "H2": {
    "status": "FAILED",
    "result": {
      "cross_minus_same_abs_promoted_frontier_difference": {
        "n": 45,
        "mean": 0.03962962962962964,
        "ci95_low": -0.09224074074074072,
        "ci95_high": 0.17039814814814824,
        "half_width": 0.1313194444444445
      },
      "minimum_effect": 0.5,
      "signflip": {
        "n": 45,
        "observed_mean": 0.03962962962962964,
        "p_value": 0.2723409573803275,
        "permutations": 8000
      }
    }
  },
  "overall_status": "LOCAL_MOTIF_HYPOTHESIS_FAILED",
  "bounded_claim": "V2 did not establish that exact six-neighbour motif contributes scientifically meaningful causal-gain or opportunity differences beyond the matched scalar summaries.",
  "what_this_does_not_establish": [
    "which motif is high-gain",
    "motif is the only determinant of gain",
    "causal-gain field",
    "high-gain regions",
    "spatial clustering",
    "temporal persistence",
    "coherent structure",
    "criticality",
    "percolation",
    "natural boundary",
    "individuality",
    "organism",
    "life"
  ],
  "next_if_supported": "Freshly confirm specific predeclared motif contrasts before mapping motif-derived high-gain regions in space-time.",
  "next_if_failed": "Do not add a classifier. Treat immediate motif geometry as insufficient and move toward larger local state/history features only if they earn a qualitatively new hypothesis."
}
```
