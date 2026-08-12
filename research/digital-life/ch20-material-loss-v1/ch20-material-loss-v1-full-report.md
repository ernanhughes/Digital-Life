# Chapter 20 — What Happens When the Crystal Can Lose Material?

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-material-loss-v1",
  "schema_version": 1,
  "chapter": 20,
  "chapter_title": "What Happens When the Crystal Can Lose Material?",
  "run_type": "MATERIAL-LOSS CHARACTERIZATION",
  "profile": "quick",
  "profile_config": {
    "groups": 24,
    "seed_noise_groups": 96,
    "radius": 72,
    "warmup_steps": 14,
    "continuation_steps": 48,
    "late_window": 12,
    "loss_rates": [
      0.0,
      0.02,
      0.04,
      0.06,
      0.08,
      0.12,
      0.16
    ],
    "bounded_normalized_slope_max": 0.0025,
    "baseline_expanding_normalized_slope_min": 0.004,
    "minimum_sustainable_population": 100,
    "max_capacity_fraction": 0.75,
    "minimum_size_reduction_fraction": 0.25,
    "placement_groups": 32,
    "placement_steps": 32,
    "loss_budget_fraction_of_min_eligible": 0.1,
    "placement_sei_population_fraction": 0.1,
    "bootstrap_reps": 2000,
    "permutations": 4000,
    "alpha": 0.05
  },
  "seed": 20260826,
  "canonical_growth_rule_modified": false,
  "new_substrate_rule": "Post-growth occupied-cell removal with independent keyed probability delta.",
  "scientific_boundary": "Construction/loss dynamics only. No death, aging, repair, homeostasis, metabolism, energy, organism, or life claim.",
  "started_at_unix": 1786556281.0963094,
  "finished_at_unix": 1786556429.3904533,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 20 V1 did not establish a finite dynamic construction/loss regime under the frozen loss sweep and predeclared late-window criteria."
}
```

---

## Stage 0 — Freeze the Material-Loss Question

```json
{
  "role": "MATERIAL-LOSS CHARACTERIZATION",
  "new_substrate_rule": "After each ordinary growth update, eligible occupied cells are removed independently with probability delta.",
  "question": "Does background material loss create a finite dynamic regime where ordinary construction no longer yields irreversible monotone expansion?",
  "candidate_scaling_argument": "If construction opportunity is dominated by a boundary-like set while uniform loss acts throughout occupied material, increasing size should eventually increase expected loss faster than construction. This is a hypothesis, not assumed truth.",
  "primary_loss_sweep": [
    0.0,
    0.02,
    0.04,
    0.06,
    0.08,
    0.12,
    0.16
  ],
  "bounded_regime_definition": {
    "abs_late_normalized_population_slope_max": 0.0025,
    "minimum_late_population": 100,
    "maximum_capacity_fraction": 0.75,
    "minimum_size_reduction_vs_decay_off": 0.25
  },
  "baseline_requirement": {
    "decay_off_normalized_slope_min": 0.004
  },
  "secondary_exact_count_test": "Compare surface-biased versus interior-biased loss while holding the number of removed cells exactly equal each step.",
  "forbidden_overclaims": [
    "death",
    "aging",
    "repair",
    "homeostasis",
    "metabolism",
    "energy",
    "organism",
    "life"
  ],
  "status": "MEASURED"
}
```

---

## Stage 1 — Measure the Irreversible Baseline

```json
{
  "role": "DECAY-OFF SEED-NOISE BASELINE",
  "groups": 96,
  "final_population": {
    "mean": 5090.020833333333,
    "std": 242.7560169633903,
    "q05": 4653.75,
    "q95": 5475.0
  },
  "late_normalized_population_slope": {
    "mean": 0.03696129666400604,
    "std": 0.002141269707033286,
    "q05": 0.032923403121907904,
    "q95": 0.03974296120382371
  },
  "late_mean_net_growth": {
    "mean": 154.3125,
    "std": 8.116422598009155
  },
  "status": "MEASURED"
}
```

---

## Stage 2 — Sweep Background Material Loss

```json
{
  "groups_per_rate": 24,
  "loss_rates": [
    0.0,
    0.02,
    0.04,
    0.06,
    0.08,
    0.12,
    0.16
  ],
  "by_rate": {
    "0.0": {
      "loss_rate": 0.0,
      "late_mean_population": {
        "n": 24,
        "mean": 4196.118055555556,
        "median": 4234.0,
        "std": 171.12321625926344,
        "ci95_low": 4130.470312500001,
        "ci95_high": 4263.003472222223
      },
      "final_population": {
        "n": 24,
        "mean": 5057.791666666667,
        "median": 5083.5,
        "std": 197.9545356601,
        "ci95_low": 4982.995833333333,
        "ci95_high": 5135.3375
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.036456346808999666,
        "median": 0.03685034063505503,
        "std": 0.002243656949122638,
        "ci95_low": 0.03557429567541632,
        "ci95_high": 0.03734489183547652
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 152.38541666666666,
        "median": 150.66666666666666,
        "std": 8.508656167135408,
        "ci95_low": 149.1418402777778,
        "ci95_high": 155.72638888888886
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "late_mean_net": {
        "n": 24,
        "mean": 152.38541666666666,
        "median": 150.66666666666666,
        "std": 8.508656167135408,
        "ci95_low": 149.1418402777778,
        "ci95_high": 155.72638888888886
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 371.7291666666667,
        "median": 374.125,
        "std": 11.566580263219867,
        "ci95_low": 367.3159722222222,
        "ci95_high": 376.10460069444446
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 4.701388888888888,
        "median": 4.666666666666667,
        "std": 0.5861302856492178,
        "ci95_low": 4.482638888888888,
        "ci95_high": 4.934114583333333
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.32074270192571924,
        "median": 0.32237301033673665,
        "std": 0.01255339816475997,
        "ci95_low": 0.31599948210624224,
        "ci95_high": 0.3256603145411884
      },
      "collapsed_fraction": 0.0
    },
    "0.02": {
      "loss_rate": 0.02,
      "late_mean_population": {
        "n": 24,
        "mean": 3979.961805555555,
        "median": 3988.0416666666665,
        "std": 183.90891035036898,
        "ci95_low": 3909.9246527777777,
        "ci95_high": 4048.855208333333
      },
      "final_population": {
        "n": 24,
        "mean": 4814.25,
        "median": 4825.0,
        "std": 210.27233893629264,
        "ci95_low": 4734.994791666667,
        "ci95_high": 4894.459374999999
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.03682580873753368,
        "median": 0.037339297680494384,
        "std": 0.0021407118637132754,
        "ci95_low": 0.03597134321491289,
        "ci95_high": 0.03759621581258538
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 227.1701388888889,
        "median": 226.375,
        "std": 11.57717955519828,
        "ci95_low": 222.74296875,
        "ci95_high": 231.72595486111112
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 80.99305555555556,
        "median": 81.75,
        "std": 5.223906668927793,
        "ci95_low": 78.91657986111112,
        "ci95_high": 82.97934027777778
      },
      "late_mean_net": {
        "n": 24,
        "mean": 146.17708333333334,
        "median": 146.20833333333331,
        "std": 7.5404029488108115,
        "ci95_low": 143.33645833333333,
        "ci95_high": 149.0347222222222
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 806.8402777777778,
        "median": 813.0416666666666,
        "std": 40.487607072899884,
        "ci95_low": 791.3946180555556,
        "ci95_high": 821.9205729166666
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 74.70833333333333,
        "median": 75.58333333333334,
        "std": 5.302332911041789,
        "ci95_low": 72.68046875,
        "ci95_high": 76.73289930555555
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.305298370220052,
        "median": 0.30598008751347583,
        "std": 0.013334538584329548,
        "ci95_low": 0.3002723566279832,
        "ci95_high": 0.31038489282769993
      },
      "collapsed_fraction": 0.0
    },
    "0.04": {
      "loss_rate": 0.04,
      "late_mean_population": {
        "n": 24,
        "mean": 3810.9513888888887,
        "median": 3792.9583333333335,
        "std": 177.47282046222753,
        "ci95_low": 3741.1837673611108,
        "ci95_high": 3883.0546874999995
      },
      "final_population": {
        "n": 24,
        "mean": 4620.166666666667,
        "median": 4611.0,
        "std": 200.06252645798918,
        "ci95_low": 4542.458333333333,
        "ci95_high": 4700.223958333333
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.03758276955095493,
        "median": 0.03761280911049661,
        "std": 0.0020306253104627856,
        "ci95_low": 0.03676349485321506,
        "ci95_high": 0.038341050905896484
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 299.375,
        "median": 299.0,
        "std": 12.341238163988649,
        "ci95_low": 294.5065104166667,
        "ci95_high": 304.1947916666666
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 158.35069444444443,
        "median": 158.375,
        "std": 8.218630125470513,
        "ci95_low": 155.2463541666667,
        "ci95_high": 161.72743055555554
      },
      "late_mean_net": {
        "n": 24,
        "mean": 141.02430555555557,
        "median": 140.58333333333331,
        "std": 6.635182866409369,
        "ci95_low": 138.35364583333333,
        "ci95_high": 143.60451388888887
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 1167.2395833333333,
        "median": 1167.625,
        "std": 53.66561633964085,
        "ci95_low": 1147.1872395833334,
        "ci95_high": 1189.2052083333333
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 124.22569444444446,
        "median": 122.625,
        "std": 6.719063978919836,
        "ci95_low": 121.80138888888888,
        "ci95_high": 127.01736111111113
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.29299046652715244,
        "median": 0.29240915720717864,
        "std": 0.012687077586276185,
        "ci95_low": 0.2880625488828292,
        "ci95_high": 0.29806734468471896
      },
      "collapsed_fraction": 0.0
    },
    "0.06": {
      "loss_rate": 0.06,
      "late_mean_population": {
        "n": 24,
        "mean": 3570.107638888889,
        "median": 3590.583333333333,
        "std": 192.2438497146787,
        "ci95_low": 3493.4914930555556,
        "ci95_high": 3645.499913194444
      },
      "final_population": {
        "n": 24,
        "mean": 4332.0,
        "median": 4381.5,
        "std": 216.85198317907,
        "ci95_low": 4245.416666666667,
        "ci95_high": 4415.365624999999
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.03702883157097249,
        "median": 0.03714249286858571,
        "std": 0.002431620833104071,
        "ci95_low": 0.036045840157605584,
        "ci95_high": 0.037943235099666135
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 358.1180555555555,
        "median": 363.16666666666663,
        "std": 18.99003229300922,
        "ci95_low": 350.37109375,
        "ci95_high": 365.2407986111111
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 226.79166666666666,
        "median": 228.45833333333331,
        "std": 12.822247234965849,
        "ci95_low": 221.7638888888889,
        "ci95_high": 231.71918402777777
      },
      "late_mean_net": {
        "n": 24,
        "mean": 131.32638888888889,
        "median": 132.33333333333331,
        "std": 8.229861846133337,
        "ci95_low": 127.92309027777777,
        "ci95_high": 134.41328125
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 1429.8680555555557,
        "median": 1446.5,
        "std": 74.86937463914522,
        "ci95_low": 1399.3884548611113,
        "ci95_high": 1459.0319444444444
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 153.64583333333334,
        "median": 154.625,
        "std": 9.412938533515915,
        "ci95_low": 149.81588541666667,
        "ci95_high": 157.20850694444445
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.27471621535924917,
        "median": 0.2778552856871076,
        "std": 0.013751790422922825,
        "ci95_low": 0.26922548460058765,
        "ci95_high": 0.28000289333502437
      },
      "collapsed_fraction": 0.0
    },
    "0.08": {
      "loss_rate": 0.08,
      "late_mean_population": {
        "n": 24,
        "mean": 3511.788194444444,
        "median": 3483.916666666667,
        "std": 147.263338714863,
        "ci95_low": 3454.945659722222,
        "ci95_high": 3570.8414930555555
      },
      "final_population": {
        "n": 24,
        "mean": 4239.166666666667,
        "median": 4264.5,
        "std": 183.30769254160487,
        "ci95_low": 4164.083333333333,
        "ci95_high": 4311.753125
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.03664188039252118,
        "median": 0.036833590390983266,
        "std": 0.0029739309303973486,
        "ci95_low": 0.03556387870538037,
        "ci95_high": 0.037825949033580365
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 429.8576388888889,
        "median": 435.58333333333337,
        "std": 20.05658479651204,
        "ci95_low": 422.17282986111115,
        "ci95_high": 437.9551215277778
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 302.60763888888886,
        "median": 303.625,
        "std": 13.301580832249826,
        "ci95_low": 297.4301215277778,
        "ci95_high": 307.76258680555554
      },
      "late_mean_net": {
        "n": 24,
        "mean": 127.25,
        "median": 127.54166666666666,
        "std": 9.128676216659185,
        "ci95_low": 123.79140625000001,
        "ci95_high": 130.89635416666667
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 1695.46875,
        "median": 1690.4166666666665,
        "std": 68.7667362698721,
        "ci95_low": 1668.9047743055555,
        "ci95_high": 1721.8717881944442
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 177.17708333333334,
        "median": 178.33333333333334,
        "std": 9.194303283137817,
        "ci95_low": 173.5276041666667,
        "ci95_high": 180.69513888888886
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.26882913733696917,
        "median": 0.2704356649121694,
        "std": 0.011624560374253589,
        "ci95_low": 0.2640676855433657,
        "ci95_high": 0.273432248398757
      },
      "collapsed_fraction": 0.0
    },
    "0.12": {
      "loss_rate": 0.12,
      "late_mean_population": {
        "n": 24,
        "mean": 3074.7777777777774,
        "median": 3056.916666666667,
        "std": 135.6345519503409,
        "ci95_low": 3022.2657118055554,
        "ci95_high": 3127.817708333334
      },
      "final_population": {
        "n": 24,
        "mean": 3709.7083333333335,
        "median": 3686.5,
        "std": 160.05256722515364,
        "ci95_low": 3649.5229166666663,
        "ci95_high": 3773.3343750000004
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.036080962930881325,
        "median": 0.03605699265189101,
        "std": 0.002906355628863503,
        "ci95_low": 0.034879543710772114,
        "ci95_high": 0.03721714966747496
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 529.6076388888888,
        "median": 528.7083333333333,
        "std": 20.919755230811596,
        "ci95_low": 521.4165798611111,
        "ci95_high": 537.7051215277778
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 419.6319444444445,
        "median": 417.4583333333333,
        "std": 17.647872773964988,
        "ci95_low": 412.56571180555557,
        "ci95_high": 426.28828124999995
      },
      "late_mean_net": {
        "n": 24,
        "mean": 109.97569444444444,
        "median": 109.875,
        "std": 7.5384873659979545,
        "ci95_low": 107.07265625000001,
        "ci95_high": 113.14253472222224
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 1940.3506944444446,
        "median": 1933.1666666666665,
        "std": 85.43417451948186,
        "ci95_low": 1906.7828125,
        "ci95_high": 1973.254253472222
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 178.66319444444446,
        "median": 177.16666666666669,
        "std": 8.906806791788403,
        "ci95_low": 175.1596354166667,
        "ci95_high": 182.0660590277778
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.23525323947830132,
        "median": 0.2337814699727313,
        "std": 0.010149823528768698,
        "ci95_low": 0.23143654744540973,
        "ci95_high": 0.23928812067981484
      },
      "collapsed_fraction": 0.0
    },
    "0.16": {
      "loss_rate": 0.16,
      "late_mean_population": {
        "n": 24,
        "mean": 2789.9583333333335,
        "median": 2798.125,
        "std": 112.76672085918493,
        "ci95_low": 2747.1502604166667,
        "ci95_high": 2832.784982638889
      },
      "final_population": {
        "n": 24,
        "mean": 3365.9583333333335,
        "median": 3389.5,
        "std": 138.13146830549468,
        "ci95_low": 3312.117708333333,
        "ci95_high": 3418.5510416666666
      },
      "late_normalized_population_slope": {
        "n": 24,
        "mean": 0.036291937953875274,
        "median": 0.036917639471477186,
        "std": 0.003217343851898235,
        "ci95_low": 0.035047128011772295,
        "ci95_high": 0.03750406482528417
      },
      "late_mean_attachments": {
        "n": 24,
        "mean": 632.2534722222223,
        "median": 630.9166666666667,
        "std": 23.170986449077862,
        "ci95_low": 623.4187499999999,
        "ci95_high": 640.9658854166668
      },
      "late_mean_losses": {
        "n": 24,
        "mean": 530.8368055555555,
        "median": 531.5,
        "std": 19.751834122116374,
        "ci95_low": 523.3400173611111,
        "ci95_high": 538.3517361111111
      },
      "late_mean_net": {
        "n": 24,
        "mean": 101.41666666666667,
        "median": 100.91666666666667,
        "std": 6.535438510286753,
        "ci95_low": 98.93038194444443,
        "ci95_high": 104.03888888888889
      },
      "late_mean_boundary": {
        "n": 24,
        "mean": 2068.0798611111113,
        "median": 2072.916666666667,
        "std": 78.53778237489485,
        "ci95_low": 2038.4861979166667,
        "ci95_high": 2097.734201388889
      },
      "late_mean_holes": {
        "n": 24,
        "mean": 160.7847222222222,
        "median": 160.125,
        "std": 8.139258824917757,
        "ci95_low": 157.71519097222225,
        "ci95_high": 163.8787326388889
      },
      "max_capacity_fraction": {
        "n": 24,
        "mean": 0.21345413997928428,
        "median": 0.21494704800558057,
        "std": 0.00875968471719796,
        "ci95_low": 0.21003980647684276,
        "ci95_high": 0.2167893361447566
      },
      "collapsed_fraction": 0.0
    }
  },
  "classifications": {
    "0.0": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.0,
      "meaningful_size_reduction": false,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.02": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.05151338621510304,
      "meaningful_size_reduction": false,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.04": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.09179118927712626,
      "meaningful_size_reduction": false,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.06": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.14918798956045676,
      "meaningful_size_reduction": false,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.08": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.16308641750559805,
      "meaningful_size_reduction": false,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.12": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.2672327763260025,
      "meaningful_size_reduction": true,
      "qualifies_as_finite_dynamic_regime": false
    },
    "0.16": {
      "bounded_slope": false,
      "sustainable_population": true,
      "unsaturated": true,
      "size_reduction_fraction_vs_decay_off": 0.33510966650723795,
      "meaningful_size_reduction": true,
      "qualifies_as_finite_dynamic_regime": false
    }
  },
  "qualifying_nonzero_rates": [],
  "status": "MEASURED"
}
```

---

## Stage 3 — Does the Location of Equal Loss Matter?

```json
{
  "role": "EXACT-COUNT LOSS-PLACEMENT CONTROL",
  "groups": 32,
  "all_loss_budgets_exactly_matched": true,
  "mean_cumulative_losses_each_policy": 621.09375,
  "late_population_advantage_interior_minus_surface": {
    "n": 32,
    "mean": 0.11089400874021672,
    "median": 0.1117418104845193,
    "std": 0.030547156523448867,
    "ci95_low": 0.10072288882180856,
    "ci95_high": 0.12115979258808934
  },
  "directional_test": {
    "observed_mean": 0.11089400874021672,
    "p_value": 0.00024993751562109475,
    "permutations": 4000,
    "alternative": "greater"
  },
  "predeclared_sei_population_fraction": 0.1,
  "mean_late_holes_surface": 2.690104166666667,
  "mean_late_holes_interior": 29.825520833333332,
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 20 Verdict

```json
{
  "question": "Does background material loss create a finite dynamic regime rather than irreversible monotone expansion?",
  "decay_off_baseline_expanding": true,
  "decay_off_mean_normalized_slope": 0.03696129666400604,
  "qualifying_nonzero_loss_rates": [],
  "finite_dynamic_regime_supported": false,
  "exact_count_loss_location_test": {
    "supported_at_predeclared_SEI": true,
    "mean_interior_minus_surface_population_advantage_norm": 0.11089400874021672,
    "p_value": 0.00024993751562109475,
    "sei": 0.1
  },
  "status": "FAILED",
  "bounded_claim": "Chapter 20 V1 did not establish a finite dynamic construction/loss regime under the frozen loss sweep and predeclared late-window criteria.",
  "forbidden_overclaims": [
    "death",
    "aging",
    "repair",
    "homeostasis",
    "metabolism",
    "energy",
    "organism",
    "life"
  ],
  "next_question_if_supported": "What computational budget is required to remain in the construction/loss regime, and how does sustainable size scale with that budget?",
  "next_question_if_failed": "Do not tune loss rates to force a plateau. Diagnose whether the finite observation window, geometry, or construction law makes the perimeter/occupied-material scaling hypothesis inapplicable."
}
```
