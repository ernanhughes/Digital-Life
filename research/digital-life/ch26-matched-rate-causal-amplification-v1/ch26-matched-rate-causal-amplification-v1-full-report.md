# Chapter 26 — Does Candidate Subsampling Change Causal Amplification? (V1)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-matched-rate-causal-amplification-v1",
  "schema_version": 1,
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
  "source_checkpoint_profile": {
    "groups": 192,
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
  "seed": 20260912,
  "fractions": [
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "reference_fraction": 0.1,
  "construction_match_tolerance": 0.02,
  "primary_SEI": 0.15,
  "fresh_seed": true,
  "started_at_unix": 1786615938.7978883,
  "finished_at_unix": 1786616662.0975566,
  "final_status": "CAUSAL_AMPLIFICATION_INVARIANT_WITHIN_SEI"
}
```

---

## Stage 0 — Frozen Chapter 26 V1 Protocol

```json
{
  "role": "MATCHED-CONSTRUCTION-RATE CAUSAL AMPLIFICATION TEST",
  "question": "At matched expected construction rate, does stronger candidate subsampling change transient causal amplification?",
  "same_checkpoint_across_arms": true,
  "same_probe_across_arms": true,
  "same_post_intervention_force_prevent_states_across_arms": true,
  "intervention_budget_fixed_at": 96,
  "same_future_environment": true,
  "same_random_keys": true,
  "control_parameter": "fraction of frontier candidates evaluated",
  "fractions": [
    0.1,
    0.25,
    0.5,
    0.75,
    1.0
  ],
  "unbounded_arm": true,
  "reference_fraction_for_target": 0.1,
  "construction_rate_match": {
    "target": "checkpoint-specific expected attachments under f=0.10 with base offset 0 on the common post-intervention PREVENT state",
    "relative_tolerance": 0.02,
    "required_arm_pass_fraction": 0.95
  },
  "primary_H1": {
    "contrast": "G_T(f=0.10) - G_T(f=1.00)",
    "SEI_abs": 0.15,
    "two_sided": true,
    "statuses": [
      "SUPPORTED",
      "BOUNDED_NEAR_ZERO",
      "UNRESOLVED",
      "INVALID"
    ]
  },
  "supported_probe_scope": "occupied_neighbors = 1",
  "horizon": 12,
  "forbidden_overclaims": [
    "formal branching ratio",
    "critical point",
    "supercriticality",
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

## Stage 1 — Frozen Probe Support

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

## Stage 2 — Expected Construction-Rate Matching

```json
{
  "total_arms": 4608,
  "valid_arms": 4608,
  "pass_fraction": 1.0,
  "required_pass_fraction": 0.95,
  "construction_match_valid": true,
  "relative_tolerance": 0.02
}
```

---

## Stage 3 — Matched-Rate Budget Arm Profiles

```json
{
  "f=0.10": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.1953125,
      "sd": 0.4607686569587846,
      "se": 0.03325311351616208,
      "ci95_low": 0.1328125,
      "ci95_high": 0.26171875,
      "achieved_mde80_one_sided": 0.0826830307921007
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10488979896251283,
      "sd": 0.1043790744492359,
      "se": 0.0075329108413787925,
      "ci95_low": 0.09037422581288916,
      "ci95_high": 0.11978025524123824,
      "achieved_mde80_one_sided": 0.01873039343365997
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.16015625,
      "sd": 0.18107727823699274,
      "se": 0.013068126916781567,
      "ci95_low": 0.13541666666666666,
      "ci95_high": 0.18619791666666666,
      "achieved_mde80_one_sided": 0.032493569052719426
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.15364583333333334,
      "sd": 0.17675741231918146,
      "se": 0.012756367447967636,
      "ci95_low": 0.12890625,
      "ci95_high": 0.1796875,
      "achieved_mde80_one_sided": 0.03171838697098315
    },
    "E1_far": {
      "n": 192,
      "mean": -0.04687754701502791,
      "sd": 0.1178899303810071,
      "se": 0.008507972880027586,
      "ci95_low": -0.06351261404508857,
      "ci95_high": -0.03017239491342911,
      "achieved_mde80_one_sided": 0.021154860680211853
    },
    "selected_jaccard": {
      "n": 192,
      "mean": 0.997899779225655,
      "sd": 0.002897061694796632,
      "se": 0.00020907741866872364,
      "ci95_low": 0.9974743465892474,
      "ci95_high": 0.9982920279520632,
      "achieved_mde80_one_sided": 0.0005198657454231133
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.14388020833333331,
      "sd": 0.19407064108393643,
      "se": 0.014005842108951744,
      "ci95_low": 0.11740451388888888,
      "ci95_high": 0.1725314670138888,
      "achieved_mde80_one_sided": 0.03482517430438237
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.6148602885318,
      "sd": 3.449586262022665,
      "se": 0.24895244462145258,
      "ci95_low": 36.126309768536174,
      "ci95_high": 37.089366053625575,
      "achieved_mde80_one_sided": 0.6190139950173313
    },
    "calibration_offset": {
      "n": 192,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "descriptive_G_over_E1": {
      "n": 165,
      "mean": 1.9756319824025441,
      "sd": 6.288482646479223,
      "se": 0.48955771006621346,
      "ci95_low": 1.1832174693076452,
      "ci95_high": 3.087971750716953,
      "achieved_mde80_one_sided": 1.2172729388555261
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 118,
      "nonzero_fraction": 0.15364583333333334,
      "mean_given_nonzero": 1.271186440677966
    }
  },
  "f=0.25": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.14322916666666666,
      "sd": 0.48436928232283755,
      "se": 0.034956341942034515,
      "ci95_low": 0.07682291666666667,
      "ci95_high": 0.21223958333333334,
      "achieved_mde80_one_sided": 0.08691806545476302
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.11395671359698507,
      "sd": 0.08153314163501481,
      "se": 0.005884147658856461,
      "ci95_low": 0.10255220136865402,
      "ci95_high": 0.12567844483046012,
      "achieved_mde80_one_sided": 0.014630785229360012
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.15494791666666666,
      "sd": 0.1689635711406466,
      "se": 0.0121938954101616,
      "ci95_low": 0.13151041666666666,
      "ci95_high": 0.1796875,
      "achieved_mde80_one_sided": 0.03031981438923052
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.14583333333333334,
      "sd": 0.17413460922270693,
      "se": 0.012567082938745018,
      "ci95_low": 0.12109375,
      "ci95_high": 0.17057291666666666,
      "achieved_mde80_one_sided": 0.03124773579731441
    },
    "E1_far": {
      "n": 192,
      "mean": -0.04510044305297195,
      "sd": 0.09553403499120183,
      "se": 0.006894575102367688,
      "ci95_low": -0.05852162648666113,
      "ci95_high": -0.032157275994247274,
      "achieved_mde80_one_sided": 0.017143187666034603
    },
    "selected_jaccard": {
      "n": 192,
      "mean": 0.9980627196520802,
      "sd": 0.002223782913300873,
      "se": 0.00016048770795169367,
      "ci95_low": 0.9977315597372826,
      "ci95_high": 0.998351155255644,
      "achieved_mde80_one_sided": 0.00039904865124506595
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.3294270833333333,
      "sd": 0.378153702474114,
      "se": 0.027290892739810422,
      "ci95_low": 0.2799479166666667,
      "ci95_high": 0.38519965277777773,
      "achieved_mde80_one_sided": 0.0678581187188061
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.614860288531595,
      "sd": 3.4495862620199125,
      "se": 0.24895244462125393,
      "ci95_low": 36.12800969444614,
      "ci95_high": 37.090536903299274,
      "achieved_mde80_one_sided": 0.6190139950168374
    },
    "calibration_offset": {
      "n": 192,
      "mean": -1.7544797365421516,
      "sd": 0.11787989861008534,
      "se": 0.008507248899322322,
      "ci95_low": -1.7712653171710542,
      "ci95_high": -1.737614837745076,
      "achieved_mde80_one_sided": 0.02115306052038871
    },
    "descriptive_G_over_E1": {
      "n": 190,
      "mean": 0.2193419943741067,
      "sd": 13.803173455944812,
      "se": 1.0013874518436892,
      "ci95_low": -2.072601506805892,
      "ci95_high": 1.7071231501250794,
      "achieved_mde80_one_sided": 2.4899247246539074
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 112,
      "nonzero_fraction": 0.14583333333333334,
      "mean_given_nonzero": 0.9821428571428571
    }
  },
  "f=0.50": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.10286458333333333,
      "sd": 0.3583771192149254,
      "se": 0.02586364078126747,
      "ci95_low": 0.05078125,
      "ci95_high": 0.15494791666666666,
      "achieved_mde80_one_sided": 0.06430929260425486
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.11177619313791083,
      "sd": 0.060477654413016085,
      "se": 0.004364598756913999,
      "ci95_low": 0.10330560047973855,
      "ci95_high": 0.12043189156396716,
      "achieved_mde80_one_sided": 0.010852465085342647
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.13671875,
      "sd": 0.17120810050348223,
      "se": 0.012355880364141246,
      "ci95_low": 0.11328125,
      "ci95_high": 0.16145833333333334,
      "achieved_mde80_one_sided": 0.03072258590508411
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.13151041666666666,
      "sd": 0.17526139011415764,
      "se": 0.012648401345119617,
      "ci95_low": 0.10677083333333333,
      "ci95_high": 0.15755208333333334,
      "achieved_mde80_one_sided": 0.03144993197046276
    },
    "E1_far": {
      "n": 192,
      "mean": -0.04989399485379017,
      "sd": 0.07641127146984249,
      "se": 0.005514508519029392,
      "ci95_low": -0.0608613516848503,
      "ci95_high": -0.03943902596065555,
      "achieved_mde80_one_sided": 0.013711686800714147
    },
    "selected_jaccard": {
      "n": 192,
      "mean": 0.9985126652029548,
      "sd": 0.0017007800008153108,
      "se": 0.00012274322391288145,
      "ci95_low": 0.9982669549224357,
      "ci95_high": 0.9987459756744302,
      "achieved_mde80_one_sided": 0.00030519794055909545
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.5067274305555555,
      "sd": 0.5806626315621864,
      "se": 0.041905715830098104,
      "ci95_low": 0.4283799913194445,
      "ci95_high": 0.5907118055555556,
      "achieved_mde80_one_sided": 0.10419750892381775
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.614860288527716,
      "sd": 3.449586262020206,
      "se": 0.2489524446212751,
      "ci95_low": 36.111862744906816,
      "ci95_high": 37.098521921791864,
      "achieved_mde80_one_sided": 0.61901399501689
    },
    "calibration_offset": {
      "n": 192,
      "mean": -2.701482342128749,
      "sd": 0.13654695936323877,
      "se": 0.009854427968173849,
      "ci95_low": -2.720781175395281,
      "ci95_high": -2.682121044474801,
      "achieved_mde80_one_sided": 0.02450278740771268
    },
    "descriptive_G_over_E1": {
      "n": 192,
      "mean": 1.0876339228891465,
      "sd": 9.01089716903247,
      "se": 0.6503054882726167,
      "ci95_low": -0.11349379432805436,
      "ci95_high": 2.4686872417228822,
      "achieved_mde80_one_sided": 1.6169682482508976
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 101,
      "nonzero_fraction": 0.13151041666666666,
      "mean_given_nonzero": 0.7821782178217822
    }
  },
  "f=0.75": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.14453125,
      "sd": 0.3397855638263885,
      "se": 0.024521910842739275,
      "ci95_low": 0.09765625,
      "ci95_high": 0.19401041666666666,
      "achieved_mde80_one_sided": 0.06097311484249157
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.11045709862927428,
      "sd": 0.048360839356643766,
      "se": 0.003490142952599316,
      "ci95_low": 0.10357149234070405,
      "ci95_high": 0.1171933683465156,
      "achieved_mde80_one_sided": 0.008678152711274555
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.12109375,
      "sd": 0.1512958045825898,
      "se": 0.010918834187877405,
      "ci95_low": 0.10026041666666667,
      "ci95_high": 0.14322916666666666,
      "achieved_mde80_one_sided": 0.02714940671439137
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.09895833333333333,
      "sd": 0.14002228070023584,
      "se": 0.010105237681853313,
      "ci95_low": 0.07942708333333333,
      "ci95_high": 0.11848958333333333,
      "achieved_mde80_one_sided": 0.02512641945555199
    },
    "E1_far": {
      "n": 192,
      "mean": -0.04142324860824435,
      "sd": 0.06134524492869022,
      "se": 0.004427211709135353,
      "ci95_low": -0.05013585668683167,
      "ci95_high": -0.03280909177667571,
      "achieved_mde80_one_sided": 0.011008150616984257
    },
    "selected_jaccard": {
      "n": 192,
      "mean": 0.9988216905648718,
      "sd": 0.001196023160689154,
      "se": 8.631553672261377e-05,
      "ci95_low": 0.9986450357193128,
      "ci95_high": 0.9989837065738795,
      "achieved_mde80_one_sided": 0.00021462141213344862
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.6050347222222222,
      "sd": 0.6267784228432448,
      "se": 0.045233836393849564,
      "ci95_low": 0.5188802083333334,
      "ci95_high": 0.6983506944444443,
      "achieved_mde80_one_sided": 0.11247279703838
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.6148602885339,
      "sd": 3.449586262021466,
      "se": 0.24895244462136604,
      "ci95_low": 36.13842808432715,
      "ci95_high": 37.087555515579275,
      "achieved_mde80_one_sided": 0.6190139950171161
    },
    "calibration_offset": {
      "n": 192,
      "mean": -3.185802510902718,
      "sd": 0.13813333523280835,
      "se": 0.00996891478509034,
      "ci95_low": -3.204489464091611,
      "ci95_high": -3.166138853318623,
      "achieved_mde80_one_sided": 0.024787455999836998
    },
    "descriptive_G_over_E1": {
      "n": 192,
      "mean": -0.06324519074460062,
      "sd": 17.29627106159151,
      "se": 1.2482508441733242,
      "ci95_low": -2.847714174164861,
      "ci95_high": 1.8016638277553785,
      "achieved_mde80_one_sided": 3.103744343665314
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 76,
      "nonzero_fraction": 0.09895833333333333,
      "mean_given_nonzero": 1.4605263157894737
    }
  },
  "f=1.00": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.1328125,
      "sd": 0.34121956550704524,
      "se": 0.024625400999782464,
      "ci95_low": 0.0859375,
      "ci95_high": 0.18229166666666666,
      "achieved_mde80_one_sided": 0.06123044051629118
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.10816959058602434,
      "sd": 0.039437141991345945,
      "se": 0.0028461305680966345,
      "ci95_low": 0.1026995569369833,
      "ci95_high": 0.11380360570767001,
      "achieved_mde80_one_sided": 0.007076832107342271
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.13802083333333334,
      "sd": 0.16527698339179747,
      "se": 0.011927838856512947,
      "ci95_low": 0.11458333333333333,
      "ci95_high": 0.16145833333333334,
      "achieved_mde80_one_sided": 0.029658271457105385
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.125,
      "sd": 0.15561060274243485,
      "se": 0.011230227922763085,
      "ci95_low": 0.10416666666666667,
      "ci95_high": 0.14713541666666666,
      "achieved_mde80_one_sided": 0.02792367940790941
    },
    "E1_far": {
      "n": 192,
      "mean": -0.05312912277081333,
      "sd": 0.04391918028783393,
      "se": 0.0031695938202210786,
      "ci95_low": -0.05943688768258245,
      "ci95_high": -0.04720866333321073,
      "achieved_mde80_one_sided": 0.007881115352053164
    },
    "selected_jaccard": {
      "n": 192,
      "mean": 0.9987420201268353,
      "sd": 0.0012740377849980542,
      "se": 9.194575726579765e-05,
      "ci95_low": 0.9985518539504726,
      "ci95_high": 0.9989170058067606,
      "achieved_mde80_one_sided": 0.0002286208139732833
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.8541666666666666,
      "sd": 0.8724720400866635,
      "se": 0.06296524590055715,
      "ci95_low": 0.7360026041666666,
      "ci95_high": 0.9816650390625,
      "achieved_mde80_one_sided": 0.15656150101847152
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.614860288527844,
      "sd": 3.449586262020757,
      "se": 0.24895244462131488,
      "ci95_low": 36.11910130288273,
      "ci95_high": 37.09586256638405,
      "achieved_mde80_one_sided": 0.619013995016989
    },
    "calibration_offset": {
      "n": 192,
      "mean": -3.5128747083379714,
      "sd": 0.13869081372764738,
      "se": 0.010009147329973184,
      "ci95_low": -3.532593496847896,
      "ci95_high": -3.4932796908475985,
      "achieved_mde80_one_sided": 0.024887493211263104
    },
    "descriptive_G_over_E1": {
      "n": 192,
      "mean": 2.380702450207458,
      "sd": 68.1249690632696,
      "se": 4.916496153401704,
      "ci95_low": -4.657656375999801,
      "ci95_high": 13.400913784722677,
      "achieved_mde80_one_sided": 12.224744087298184
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 96,
      "nonzero_fraction": 0.125,
      "mean_given_nonzero": 1.0625
    }
  },
  "unbounded": {
    "groups": 192,
    "probes": 768,
    "G_local": {
      "n": 192,
      "mean": 0.14453125,
      "sd": 0.3675428372832477,
      "se": 0.026525119505525236,
      "ci95_low": 0.09244791666666667,
      "ci95_high": 0.1953125,
      "achieved_mde80_one_sided": 0.06595404282289354
    },
    "E1_ring1": {
      "n": 192,
      "mean": 0.1082433744848047,
      "sd": 0.03942368788667872,
      "se": 0.0028451596017277187,
      "ci95_low": 0.10288105855618138,
      "ci95_high": 0.11392703308297074,
      "achieved_mde80_one_sided": 0.007074417823875548
    },
    "lag1_realized_divergence": {
      "n": 192,
      "mean": 0.12760416666666666,
      "sd": 0.1597396100508487,
      "se": 0.011528213357887918,
      "ci95_low": 0.10546875,
      "ci95_high": 0.15104166666666666,
      "achieved_mde80_one_sided": 0.028664612701149728
    },
    "G_nonzero_rate": {
      "n": 192,
      "mean": 0.11848958333333333,
      "sd": 0.15547363843091183,
      "se": 0.011220343374997187,
      "ci95_low": 0.09765625,
      "ci95_high": 0.140625,
      "achieved_mde80_one_sided": 0.02789910172838185
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
    "selected_jaccard": {
      "n": 192,
      "mean": 0.9993255228115862,
      "sd": 0.0006300992803514443,
      "se": 4.547349864088698e-05,
      "ci95_low": 0.9992373803764646,
      "ci95_high": 0.9994095637620583,
      "achieved_mde80_one_sided": 0.00011306871119065533
    },
    "selected_symdiff": {
      "n": 192,
      "mean": 0.47374131944444436,
      "sd": 0.45996896781141733,
      "se": 0.03319540092309951,
      "ci95_low": 0.4103732638888889,
      "ci95_high": 0.5418836805555555,
      "achieved_mde80_one_sided": 0.08253952988031495
    },
    "matched_expected_attachments": {
      "n": 192,
      "mean": 36.614860288527844,
      "sd": 3.449586262020757,
      "se": 0.24895244462131488,
      "ci95_low": 36.12251834600374,
      "ci95_high": 37.10788905750021,
      "achieved_mde80_one_sided": 0.619013995016989
    },
    "calibration_offset": {
      "n": 192,
      "mean": -3.5128747083379714,
      "sd": 0.13869081372764738,
      "se": 0.010009147329973184,
      "ci95_low": -3.5322560389170934,
      "ci95_high": -3.4931535357070627,
      "achieved_mde80_one_sided": 0.024887493211263104
    },
    "descriptive_G_over_E1": {
      "n": 192,
      "mean": 2.3580843809911056,
      "sd": 68.21017811829385,
      "se": 4.92264558725866,
      "ci95_low": -4.773868010386982,
      "ci95_high": 13.368739716481482,
      "achieved_mde80_one_sided": 12.240034499989962
    },
    "conditional_G_given_nonzero": {
      "n_all": 768,
      "n_nonzero": 91,
      "nonzero_fraction": 0.11848958333333333,
      "mean_given_nonzero": 1.2197802197802199
    }
  }
}
```

---

## Stage 4 — Primary Matched-Rate Amplification Test

```json
{
  "contrast": "G_T(f=0.10) - G_T(f=1.00)",
  "SEI_abs": 0.15,
  "result": {
    "n": 192,
    "mean": 0.0625,
    "sd": 0.5794247011417392,
    "se": 0.041816375897412696,
    "ci95_low": -0.016927083333333332,
    "ci95_high": 0.14716796874999952,
    "achieved_mde80_one_sided": 0.10397536742715453
  },
  "status": "BOUNDED_NEAR_ZERO"
}
```

---

## Stage 5 — Secondary Budget-to-Full Contrasts

```json
{
  "f=0.10": {
    "G_local_minus_full": {
      "n": 192,
      "mean": 0.0625,
      "sd": 0.5794247011417392,
      "se": 0.041816375897412696,
      "ci95_low": -0.018229166666666668,
      "ci95_high": 0.14713541666666666,
      "achieved_mde80_one_sided": 0.10397536742715453
    },
    "E1_ring1_minus_full": {
      "n": 192,
      "mean": -0.003279791623511496,
      "sd": 0.1006758569200173,
      "se": 0.007265654136708531,
      "ci95_low": -0.01748606596020032,
      "ci95_high": 0.011382656631460148,
      "achieved_mde80_one_sided": 0.018065866356190775
    },
    "lag1_divergence_minus_full": {
      "n": 192,
      "mean": 0.022135416666666668,
      "sd": 0.23963786464924,
      "se": 0.017294373207908227,
      "ci95_low": -0.01171875,
      "ci95_high": 0.0546875,
      "achieved_mde80_one_sided": 0.04300202420999029
    },
    "far_effect_minus_full": {
      "n": 192,
      "mean": 0.006251575755785425,
      "sd": 0.12874236931308744,
      "se": 0.009291180197377657,
      "ci95_low": -0.011896629499315591,
      "ci95_high": 0.024670784670456632,
      "achieved_mde80_one_sided": 0.02310228598538155
    }
  },
  "f=0.25": {
    "G_local_minus_full": {
      "n": 192,
      "mean": 0.010416666666666666,
      "sd": 0.6052958545647151,
      "se": 0.043683465571537856,
      "ci95_low": -0.07552083333333333,
      "ci95_high": 0.09505208333333333,
      "achieved_mde80_one_sided": 0.10861783896421143
    },
    "E1_ring1_minus_full": {
      "n": 192,
      "mean": 0.005787123010960748,
      "sd": 0.07229608541376042,
      "se": 0.0052175205468738455,
      "ci95_low": -0.004269399411107948,
      "ci95_high": 0.015908769978451982,
      "achieved_mde80_one_sided": 0.012973233674071265
    },
    "lag1_divergence_minus_full": {
      "n": 192,
      "mean": 0.016927083333333332,
      "sd": 0.2427750448543136,
      "se": 0.01752077968739518,
      "ci95_low": -0.016927083333333332,
      "ci95_high": 0.05078125,
      "achieved_mde80_one_sided": 0.04356497822949443
    },
    "far_effect_minus_full": {
      "n": 192,
      "mean": 0.008028679717841382,
      "sd": 0.10413907476343537,
      "se": 0.0075155903559784975,
      "ci95_low": -0.006245522512124372,
      "ci95_high": 0.022841929115951683,
      "achieved_mde80_one_sided": 0.018687326482140058
    }
  },
  "f=0.50": {
    "G_local_minus_full": {
      "n": 192,
      "mean": -0.029947916666666668,
      "sd": 0.4053974811120218,
      "se": 0.02925704310610275,
      "ci95_low": -0.08723958333333333,
      "ci95_high": 0.026041666666666668,
      "achieved_mde80_one_sided": 0.07274690217660279
    },
    "E1_ring1_minus_full": {
      "n": 192,
      "mean": 0.0036066025518865126,
      "sd": 0.04322625553468044,
      "se": 0.003119586283625913,
      "ci95_low": -0.002522753474325269,
      "ci95_high": 0.009637374964193039,
      "achieved_mde80_one_sided": 0.00775677286947253
    },
    "lag1_divergence_minus_full": {
      "n": 192,
      "mean": -0.0013020833333333333,
      "sd": 0.20861265088872305,
      "se": 0.015055321268370711,
      "ci95_low": -0.03125,
      "ci95_high": 0.028645833333333332,
      "achieved_mde80_one_sided": 0.03743467785092189
    },
    "far_effect_minus_full": {
      "n": 192,
      "mean": 0.003235127917023163,
      "sd": 0.08522884711018285,
      "se": 0.006150862227723191,
      "ci95_low": -0.0088990884276638,
      "ci95_high": 0.015086615181660351,
      "achieved_mde80_one_sided": 0.015293964299782737
    }
  },
  "f=0.75": {
    "G_local_minus_full": {
      "n": 192,
      "mean": 0.01171875,
      "sd": 0.3146603987755555,
      "se": 0.022708658242047746,
      "ci95_low": -0.03125,
      "ci95_high": 0.05859375,
      "achieved_mde80_one_sided": 0.056464507835091625
    },
    "E1_ring1_minus_full": {
      "n": 192,
      "mean": 0.0022875080432499403,
      "sd": 0.0239360796114975,
      "se": 0.0017274377508802994,
      "ci95_low": -0.0011355944133899123,
      "ci95_high": 0.00569803274620715,
      "achieved_mde80_one_sided": 0.004295230540684652
    },
    "lag1_divergence_minus_full": {
      "n": 192,
      "mean": -0.016927083333333332,
      "sd": 0.14485029244281106,
      "se": 0.010453669416756623,
      "ci95_low": -0.037760416666666664,
      "ci95_high": 0.00390625,
      "achieved_mde80_one_sided": 0.025992786204997967
    },
    "far_effect_minus_full": {
      "n": 192,
      "mean": 0.011705874162568993,
      "sd": 0.06897339232347137,
      "se": 0.004977725828109733,
      "ci95_low": 0.0015971417177139567,
      "ci95_high": 0.02141342097697314,
      "achieved_mde80_one_sided": 0.012376990134177784
    }
  }
}
```

---

## Stage 6 — Bounded Chapter 26 V1 Verdict

```json
{
  "validity": {
    "scientific_valid": true,
    "construction_match_valid": true,
    "probe_coverage_fraction": 1.0
  },
  "primary_status": "BOUNDED_NEAR_ZERO",
  "overall_status": "CAUSAL_AMPLIFICATION_INVARIANT_WITHIN_SEI",
  "bounded_claim": "At matched expected construction rate, the f=0.10 versus full evaluation difference in finite-horizon causal amplification was bounded within the predeclared \u00b10.15 attachment equivalence region.",
  "what_this_does_not_establish": [
    "formal branching ratio",
    "criticality",
    "supercriticality",
    "phase transition",
    "coherent structure",
    "individuality",
    "organism",
    "life"
  ],
  "stop_rule": "Do not alter budget fractions, horizon, construction target, calibration method or SEI to rescue the primary result.",
  "next_if_supported": "Map causal amplification over matched-rate selection concentration and test whether any regime approaches sustained amplification.",
  "next_if_bounded": "Treat finite-budget redistribution as a spatial allocation law rather than an amplification mechanism, then move to persistent material memory or individuation.",
  "next_if_unresolved": "Increase independent groups only if achieved MDE exceeds the frozen SEI; otherwise preserve the unresolved result."
}
```
