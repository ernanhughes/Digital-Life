# Chapter 21 — What Does It Cost to Stay?

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-finite-update-budget-v1",
  "schema_version": 1,
  "chapter": 21,
  "chapter_title": "What Does It Cost to Stay?",
  "run_type": "FINITE CONSTRUCTION-EVALUATION BUDGET",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "seed_noise_groups": 96,
    "radius": 72,
    "warmup_steps": 14,
    "continuation_steps": 48,
    "late_window": 12,
    "loss_rate": 0.08,
    "primary_budget": 256,
    "budget_sweep": [
      64,
      128,
      256,
      512,
      1024,
      2048,
      null
    ],
    "sei_reoccupation_per_loss": 0.15,
    "sei_first_occupations_per_1000_evals": 100.0,
    "bootstrap_reps": 2000,
    "permutations": 4000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75
  },
  "seed": 20260828,
  "canonical_attachment_probability_modified": false,
  "new_constraint": "At most B frontier candidates receive canonical attachment evaluation per update.",
  "loss_process": "Uniform keyed background loss after growth at frozen delta.",
  "scientific_boundary": "Allocation under computational scarcity only. No maintenance, homeostasis, metabolism, energy, repair, adaptation, agency, organism, or life claim.",
  "started_at_unix": 1786557710.4326587,
  "finished_at_unix": 1786557875.792059,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 21 V1 did not establish both predeclared arms of the construction-allocation tradeoff under the fixed finite evaluation budget."
}
```

---

## Stage 0 — Freeze the Scarcity Question

```json
{
  "role": "FINITE CONSTRUCTION-EVALUATION BUDGET",
  "chapter_20_bridge": "Chapter 20 measured rapid reoccupation under effectively unlimited frontier evaluation. Chapter 21 limits how many frontier candidates can receive an attachment evaluation.",
  "new_constraint": "At most B frontier candidates are evaluated for attachment per update.",
  "loss_rate": 0.08,
  "primary_budget": 256,
  "primary_policies": [
    "high_support",
    "low_support"
  ],
  "policy_information_boundary": "Policies use only current occupied-neighbour count plus keyed scheduling noise. They do not know occupancy history or whether a candidate is a reoccupation site.",
  "primary_tradeoff_requirements": {
    "high_support_reoccupation_per_loss_advantage_min": 0.15,
    "low_support_first_occupations_per_1000_evals_advantage_min": 100.0,
    "alpha": 0.05,
    "both_required": true
  },
  "secondary_budget_sweep": [
    64,
    128,
    256,
    512,
    1024,
    2048,
    "unlimited"
  ],
  "new_sentence_if_primary_succeeds": "With computational opportunity held fixed, local scheduling changes the tradeoff between reusing lost material and occupying new sites.",
  "forbidden_overclaims": [
    "maintenance",
    "homeostasis",
    "metabolism",
    "energy",
    "repair",
    "adaptation",
    "agency",
    "choice",
    "organism",
    "life"
  ],
  "status": "MEASURED"
}
```

---

## Stage 1 — Measure the Unlimited-Opportunity Reference

```json
{
  "role": "UNLIMITED-EVALUATION REFERENCE",
  "groups": 96,
  "mean_late_population": 3454.0138888888887,
  "mean_evaluation_fraction": 1.0,
  "mean_first_occupations_per_1000_evals": 233.82065461575954,
  "mean_reoccupations_per_1000_evals": 372.39276802644827,
  "mean_reoccupation_per_loss": 0.9427964035453686,
  "mean_lost_site_reoccupied_fraction": 0.9521823560267864,
  "mean_reoccupation_delay": 1.185749227489976,
  "collapsed_fraction": 0.0,
  "status": "MEASURED"
}
```

---

## Stage 2 — What Changes as Evaluation Budget Shrinks?

```json
{
  "role": "NEUTRAL-POLICY BUDGET CHARACTERIZATION",
  "loss_rate": 0.08,
  "by_budget": {
    "64": {
      "budget": "64",
      "late_mean_population": {
        "n": 48,
        "mean": 380.53298611111114,
        "median": 377.41666666666663,
        "std": 18.470743427405196,
        "ci95_low": 375.3292100694444,
        "ci95_high": 385.6470920138889
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 0.24941278059334815,
        "median": 0.2479810486841621,
        "std": 0.019424367014248288,
        "ci95_low": 0.24408542106177553,
        "ci95_high": 0.2551559970004042
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 182.44086371527774,
        "median": 182.45442708333334,
        "std": 9.894511462174133,
        "ci95_low": 179.59933810763889,
        "ci95_high": 185.1742214626736
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 347.6494683159722,
        "median": 348.7955729166667,
        "std": 12.78203312192611,
        "ci95_low": 344.08840603298614,
        "ci95_high": 351.2641059027778
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.7286228478705183,
        "median": 0.728282780227022,
        "std": 0.019371766300391384,
        "ci95_low": 0.7235764479922864,
        "ci95_high": 0.7343426890638565
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.8035772614566751,
        "median": 0.803426942172415,
        "std": 0.024486385874970214,
        "ci95_low": 0.7969289784425547,
        "ci95_high": 0.8103719267830816
      },
      "late_mean_net": {
        "n": 48,
        "mean": -0.4392361111111111,
        "median": -0.25,
        "std": 2.244887781931938,
        "ci95_low": -1.1008680555555554,
        "ci95_high": 0.21011284722222198
      },
      "collapsed_fraction": 0.0
    },
    "128": {
      "budget": "128",
      "late_mean_population": {
        "n": 48,
        "mean": 829.2482638888888,
        "median": 833.7916666666667,
        "std": 28.470965725749046,
        "ci95_low": 820.8465711805555,
        "ci95_high": 837.1367621527777
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 0.41956255947466675,
        "median": 0.4216878963586239,
        "std": 0.023870283705829165,
        "ci95_low": 0.41321786790873544,
        "ci95_high": 0.4261335640349586
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 198.2301213634803,
        "median": 199.178070291428,
        "std": 6.888161902051148,
        "ci95_low": 196.3018647017572,
        "ci95_high": 200.19756340214326
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 366.8902278644038,
        "median": 367.7568576037613,
        "std": 9.521384275919994,
        "ci95_low": 364.18892140175456,
        "ci95_high": 369.54608949636344
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.789826020268853,
        "median": 0.7908630580712802,
        "std": 0.013284606487064069,
        "ci95_low": 0.7860237440500604,
        "ci95_high": 0.7934803927219214
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.8475925057442435,
        "median": 0.8471749607917809,
        "std": 0.013802367440312166,
        "ci95_low": 0.8436018041138503,
        "ci95_high": 0.8513959550099263
      },
      "late_mean_net": {
        "n": 48,
        "mean": 0.2829861111111111,
        "median": 0.375,
        "std": 2.5648641768456044,
        "ci95_low": -0.41848958333333325,
        "ci95_high": 1.0225694444444444
      },
      "collapsed_fraction": 0.0
    },
    "256": {
      "budget": "256",
      "late_mean_population": {
        "n": 48,
        "mean": 1717.079861111111,
        "median": 1712.8333333333335,
        "std": 40.12691876330106,
        "ci95_low": 1705.685677083333,
        "ci95_high": 1727.7893229166668
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 0.6539213262395367,
        "median": 0.6542634898760316,
        "std": 0.02325261541941781,
        "ci95_low": 0.6468028458334724,
        "ci95_high": 0.6604770992195761
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 210.77937138581453,
        "median": 210.21621919353834,
        "std": 5.039982215410084,
        "ci95_low": 209.3753174653219,
        "ci95_high": 212.2104856887907
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 379.85422998975764,
        "median": 380.22091316269643,
        "std": 7.482274405959414,
        "ci95_low": 377.76157934479284,
        "ci95_high": 381.90349223820346
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.8458768089911515,
        "median": 0.8477238561533087,
        "std": 0.008093549163357885,
        "ci95_low": 0.8435993004448145,
        "ci95_high": 0.8481628278498995
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.8901338112388254,
        "median": 0.890512592147676,
        "std": 0.009278060262819065,
        "ci95_low": 0.8875265065260931,
        "ci95_high": 0.8927204919766746
      },
      "late_mean_net": {
        "n": 48,
        "mean": 10.034722222222223,
        "median": 10.5,
        "std": 4.429271900277501,
        "ci95_low": 8.751649305555556,
        "ci95_high": 11.29878472222222
      },
      "collapsed_fraction": 0.0
    },
    "512": {
      "budget": "512",
      "late_mean_population": {
        "n": 48,
        "mean": 3092.3246527777774,
        "median": 3079.5,
        "std": 89.56825823938762,
        "ci95_low": 3067.814973958333,
        "ci95_high": 3118.6036892361108
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 0.9143749329153268,
        "median": 0.9156791567417923,
        "std": 0.014267857664399055,
        "ci95_low": 0.9103329648954688,
        "ci95_high": 0.918340620344261
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 228.91681085665564,
        "median": 229.03701561988663,
        "std": 4.5714787952456035,
        "ci95_low": 227.6577951999675,
        "ci95_high": 230.19609770923296
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 376.80665827565326,
        "median": 377.3724038724654,
        "std": 6.78567596362654,
        "ci95_low": 374.9422571541798,
        "ci95_high": 378.7162659760458
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.905336078116762,
        "median": 0.9057539044323314,
        "std": 0.005231718517378476,
        "ci95_low": 0.9039273937181624,
        "ci95_high": 0.9067544919899627
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.9256206551439815,
        "median": 0.9257521719618373,
        "std": 0.0059810414608748455,
        "ci95_low": 0.9240265833998883,
        "ci95_high": 0.9272777983780356
      },
      "late_mean_net": {
        "n": 48,
        "mean": 63.670138888888886,
        "median": 63.91666666666667,
        "std": 7.243750023372095,
        "ci95_low": 61.55017361111112,
        "ci95_high": 65.59036458333333
      },
      "collapsed_fraction": 0.0
    },
    "1024": {
      "budget": "1024",
      "late_mean_population": {
        "n": 48,
        "mean": 3513.046875,
        "median": 3499.9583333333335,
        "std": 163.39765424268617,
        "ci95_low": 3467.2559461805563,
        "ci95_high": 3559.1674045138893
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 1.0,
        "median": 1.0,
        "std": 0.0,
        "ci95_low": 1.0,
        "ci95_high": 1.0
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 232.6678907451801,
        "median": 233.45401169001656,
        "std": 5.335131918015914,
        "ci95_low": 231.1555438155751,
        "ci95_high": 234.14083813493767
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 374.00955131027007,
        "median": 373.82185881656727,
        "std": 6.414434698645691,
        "ci95_low": 372.15019365294285,
        "ci95_high": 375.85001984506613
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.9429317945362966,
        "median": 0.9428250238520893,
        "std": 0.002640801572254398,
        "ci95_low": 0.9421791365488446,
        "ci95_high": 0.9436931786173441
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.9523832933161716,
        "median": 0.9526745015263572,
        "std": 0.004129546333032278,
        "ci95_low": 0.9512449889627096,
        "ci95_high": 0.9535210652117657
      },
      "late_mean_net": {
        "n": 48,
        "mean": 126.09027777777779,
        "median": 126.0,
        "std": 7.480033180080053,
        "ci95_low": 124.01002604166668,
        "ci95_high": 128.059375
      },
      "collapsed_fraction": 0.0
    },
    "2048": {
      "budget": "2048",
      "late_mean_population": {
        "n": 48,
        "mean": 3516.586805555556,
        "median": 3483.4583333333335,
        "std": 179.3364435240836,
        "ci95_low": 3469.3605902777776,
        "ci95_high": 3570.298567708333
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 1.0,
        "median": 1.0,
        "std": 0.0,
        "ci95_low": 1.0,
        "ci95_high": 1.0
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 232.06964108538386,
        "median": 232.06770202572767,
        "std": 4.6793760443232015,
        "ci95_low": 230.73244572328952,
        "ci95_high": 233.42057984280368
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 373.5466512812098,
        "median": 373.5784255853839,
        "std": 5.466477691087547,
        "ci95_low": 372.06183786375055,
        "ci95_high": 375.0720019062423
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.942586013490205,
        "median": 0.9430120669071054,
        "std": 0.003226838541657203,
        "ci95_low": 0.9416922085584146,
        "ci95_high": 0.9434624597295777
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.9524017588140353,
        "median": 0.9517134621543717,
        "std": 0.004148888482813396,
        "ci95_low": 0.9512491611108946,
        "ci95_high": 0.9536200554179776
      },
      "late_mean_net": {
        "n": 48,
        "mean": 126.2326388888889,
        "median": 126.33333333333334,
        "std": 8.102639413483303,
        "ci95_low": 124.08125000000001,
        "ci95_high": 128.50911458333334
      },
      "collapsed_fraction": 0.0
    },
    "unlimited": {
      "budget": "unlimited",
      "late_mean_population": {
        "n": 48,
        "mean": 3462.446180555555,
        "median": 3479.791666666667,
        "std": 174.49503851453466,
        "ci95_low": 3414.192795138889,
        "ci95_high": 3514.731987847222
      },
      "mean_evaluation_fraction": {
        "n": 48,
        "mean": 1.0,
        "median": 1.0,
        "std": 0.0,
        "ci95_low": 1.0,
        "ci95_high": 1.0
      },
      "first_occupations_per_1000_evals": {
        "n": 48,
        "mean": 233.07187914488122,
        "median": 232.63995229999503,
        "std": 4.8797783382357744,
        "ci95_low": 231.69927170938334,
        "ci95_high": 234.4113954402787
      },
      "reoccupations_per_1000_evals": {
        "n": 48,
        "mean": 371.7425264436418,
        "median": 372.6567733909569,
        "std": 5.586113747096199,
        "ci95_low": 370.22707184285593,
        "ci95_high": 373.3283167099382
      },
      "reoccupation_per_loss": {
        "n": 48,
        "mean": 0.9424364380734397,
        "median": 0.942516133371448,
        "std": 0.0027608961204389102,
        "ci95_low": 0.9416783045869599,
        "ci95_high": 0.9432194051798323
      },
      "lost_site_reoccupied_fraction": {
        "n": 48,
        "mean": 0.9512815795525448,
        "median": 0.9517775927690543,
        "std": 0.0039523523990342225,
        "ci95_low": 0.9502209062242793,
        "ci95_high": 0.9524094644574661
      },
      "late_mean_net": {
        "n": 48,
        "mean": 126.35069444444446,
        "median": 127.41666666666667,
        "std": 8.051914121529647,
        "ci95_low": 123.99787326388888,
        "ci95_high": 128.66497395833332
      },
      "collapsed_fraction": 0.0
    }
  },
  "finite_budget_late_population_monotone_non_decreasing": true,
  "interpretation_boundary": "This sweep characterizes computational opportunity. It does not establish a universal scaling law.",
  "status": "MEASURED"
}
```

---

## Stage 3 — At Equal Budget, What Gets Built?

```json
{
  "role": "PRIMARY FIXED-BUDGET ALLOCATION TRADEOFF",
  "budget": 256,
  "loss_rate": 0.08,
  "policies_use_history": false,
  "policy_summary": {
    "high_support": {
      "mean_late_population": 1923.1649305555554,
      "mean_reoccupation_per_loss": 0.9587803634787203,
      "mean_first_occupations_per_1000_evals": 187.5623346430792,
      "mean_reoccupations_per_1000_evals": 456.1111659406393,
      "mean_lost_site_reoccupied_fraction": 0.9757026466405115,
      "mean_evaluation_fraction": 0.8409969058995337,
      "mean_late_net": 24.272569444444446,
      "collapsed_fraction": 0.0
    },
    "neutral": {
      "mean_late_population": 1722.7569444444443,
      "mean_reoccupation_per_loss": 0.8439579238175184,
      "mean_first_occupations_per_1000_evals": 212.15684919727119,
      "mean_reoccupations_per_1000_evals": 379.45303942824984,
      "mean_lost_site_reoccupied_fraction": 0.8878280180013007,
      "mean_evaluation_fraction": 0.6526805146628013,
      "mean_late_net": 10.041666666666666,
      "collapsed_fraction": 0.0
    },
    "low_support": {
      "mean_late_population": 1130.779513888889,
      "mean_reoccupation_per_loss": 0.533529684606526,
      "mean_first_occupations_per_1000_evals": 249.14525447081232,
      "mean_reoccupations_per_1000_evals": 189.65040888951148,
      "mean_lost_site_reoccupied_fraction": 0.5423924058963626,
      "mean_evaluation_fraction": 0.5264750798162504,
      "mean_late_net": -1.5399305555555556,
      "collapsed_fraction": 0.0
    }
  },
  "high_minus_low_reoccupation_per_loss": {
    "n": 48,
    "mean": 0.42525067887219437,
    "median": 0.4242884192440429,
    "std": 0.010958624535401987,
    "ci95_low": 0.4223096370669325,
    "ci95_high": 0.4284771275434652
  },
  "reoccupation_directional_test": {
    "observed_mean": 0.42525067887219437,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "reoccupation_sei": 0.15,
  "low_minus_high_first_occupations_per_1000_evals": {
    "n": 48,
    "mean": 61.582919827733086,
    "median": 61.52668206393129,
    "std": 5.90981717974606,
    "ci95_low": 59.90029819126394,
    "ci95_high": 63.15771837751961
  },
  "first_occupation_directional_test": {
    "observed_mean": 61.582919827733086,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "first_occupation_sei": 100.0,
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 21 Verdict

```json
{
  "question": "When attachment evaluations are scarce, does local scheduling change the tradeoff between reusing lost material and occupying new sites?",
  "reoccupation_gate_passed": true,
  "reoccupation_advantage": 0.42525067887219437,
  "reoccupation_ci95": [
    0.4223096370669325,
    0.4284771275434652
  ],
  "reoccupation_p_value": 0.00024993751562109475,
  "reoccupation_sei": 0.15,
  "first_occupation_gate_passed": false,
  "first_occupation_advantage_per_1000_evals": 61.582919827733086,
  "first_occupation_ci95": [
    59.90029819126394,
    63.15771837751961
  ],
  "first_occupation_p_value": 0.00024993751562109475,
  "first_occupation_sei": 100.0,
  "status": "FAILED",
  "bounded_claim": "Chapter 21 V1 did not establish both predeclared arms of the construction-allocation tradeoff under the fixed finite evaluation budget.",
  "forbidden_overclaims": [
    "maintenance",
    "homeostasis",
    "metabolism",
    "energy",
    "repair",
    "adaptation",
    "agency",
    "choice",
    "organism",
    "life"
  ],
  "next_question_if_supported": "Can a local rule allocate scarce construction opportunity in a way that preserves a bounded process without an externally selected scheduling policy?",
  "next_question_if_failed": "Do not tune B or the neighbour-count thresholds to force a tradeoff. Use the budget sweep to determine whether candidate evaluation scarcity itself is the wrong resource abstraction."
}
```
