# Stage 2 — Does Timing Change Causal Efficiency?

```json
{
  "groups": 64,
  "window": {
    "start": 5,
    "end": 24
  },
  "primary_metrics": [
    "leverage_per_contact",
    "flips_per_contact",
    "flips_per_transmission"
  ],
  "raw_mechanism_summary": {
    "aligned": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 6.310151793130461,
        "median": 6.271437038696723,
        "std": 0.6641923266336,
        "ci95_low": 6.140932580764223,
        "ci95_high": 6.466688426617286,
        "min": 4.294509087643406,
        "max": 7.736005445585047
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 1106.046875,
        "median": 1115.0,
        "std": 114.294224166116,
        "ci95_low": 1075.3109375,
        "ci95_high": 1133.945703125,
        "min": 671.0,
        "max": 1316.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 99.39430729203374,
        "median": 99.22993732811608,
        "std": 7.771914660900022,
        "ci95_low": 97.34111612487524,
        "ci95_high": 101.24415122640505,
        "min": 68.85609772004078,
        "max": 112.57741383548958
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 99.5625,
        "median": 101.0,
        "std": 12.996243447627473,
        "ci95_low": 96.351171875,
        "ci95_high": 102.76640624999999,
        "min": 57.0,
        "max": 127.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 25.0,
        "median": 25.0,
        "std": 0.0,
        "ci95_low": 25.0,
        "ci95_high": 25.0,
        "min": 25.0,
        "max": 25.0
      },
      "applied_transmissions": {
        "n": 64,
        "mean": 291.6875,
        "median": 292.0,
        "std": 1.7666617531378213,
        "ci95_low": 291.171875,
        "ci95_high": 292.0,
        "min": 279.0,
        "max": 292.0
      },
      "truncation_rate": 0.0078125
    },
    "shuffled": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 6.4863715008589455,
        "median": 6.512712940624391,
        "std": 0.709259260325353,
        "ci95_low": 6.312462111775302,
        "ci95_high": 6.652777072420381,
        "min": 4.3309934175701965,
        "max": 8.017784491031353
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 1097.765625,
        "median": 1123.5,
        "std": 116.1699646783082,
        "ci95_low": 1067.451953125,
        "ci95_high": 1126.414453125,
        "min": 697.0,
        "max": 1299.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 97.40413022980844,
        "median": 98.31792460528612,
        "std": 8.404998294088264,
        "ci95_low": 95.27588595428452,
        "ci95_high": 99.41462523604265,
        "min": 70.48043652959234,
        "max": 111.5678327299643
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 97.09375,
        "median": 98.0,
        "std": 13.430048806221816,
        "ci95_low": 93.882421875,
        "ci95_high": 100.30664062499999,
        "min": 55.0,
        "max": 125.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 25.0,
        "median": 25.0,
        "std": 0.0,
        "ci95_low": 25.0,
        "ci95_high": 25.0,
        "min": 25.0,
        "max": 25.0
      },
      "applied_transmissions": {
        "n": 64,
        "mean": 289.09375,
        "median": 292.0,
        "std": 5.705585941645258,
        "ci95_low": 287.703125,
        "ci95_high": 290.421875,
        "min": 259.0,
        "max": 292.0
      },
      "truncation_rate": 0.0375
    },
    "shifted": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 6.250426065736674,
        "median": 6.301791134719636,
        "std": 0.6610672315351549,
        "ci95_low": 6.085289759020618,
        "ci95_high": 6.4062289553315725,
        "min": 4.282318249671773,
        "max": 7.6729089747372266
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 1064.703125,
        "median": 1080.5,
        "std": 108.51017804904006,
        "ci95_low": 1036.046875,
        "ci95_high": 1089.39140625,
        "min": 670.0,
        "max": 1261.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 95.02943459526321,
        "median": 95.84184356129356,
        "std": 7.903317890812939,
        "ci95_low": 93.0322667110801,
        "ci95_high": 96.8792214733451,
        "min": 67.55973252859313,
        "max": 107.5726386976708
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 96.609375,
        "median": 97.0,
        "std": 13.64232520904611,
        "ci95_low": 93.125,
        "ci95_high": 99.758203125,
        "min": 54.0,
        "max": 126.0
      },
      "sustained_loss_time": {
        "n": 64,
        "mean": 25.0,
        "median": 25.0,
        "std": 0.0,
        "ci95_low": 25.0,
        "ci95_high": 25.0,
        "min": 25.0,
        "max": 25.0
      },
      "applied_transmissions": {
        "n": 64,
        "mean": 288.625,
        "median": 292.0,
        "std": 6.608469943943152,
        "ci95_low": 286.87421875,
        "ci95_high": 290.125,
        "min": 260.0,
        "max": 292.0
      },
      "truncation_rate": 0.04375
    }
  },
  "efficiency_summary": {
    "aligned": {
      "leverage_per_contact": {
        "n": 64,
        "mean": 0.09016140826173447,
        "median": 0.0897922327916976,
        "std": 0.003373515204646242,
        "ci95_low": 0.08937330676829533,
        "ci95_high": 0.0909888895383062,
        "min": 0.08326198067424725,
        "max": 0.10261713520125303
      },
      "flips_per_contact": {
        "n": 64,
        "mean": 0.09008524191561934,
        "median": 0.08943261948289372,
        "std": 0.00830665608140951,
        "ci95_low": 0.08812738720968442,
        "ci95_high": 0.09208410676643942,
        "min": 0.07301066447908121,
        "max": 0.11284046692607004
      },
      "flips_per_transmission": {
        "n": 64,
        "mean": 0.3411961025514738,
        "median": 0.3458904109589041,
        "std": 0.043843911610293905,
        "ci95_low": 0.3300313225405987,
        "ci95_high": 0.35225880544690336,
        "min": 0.20430107526881722,
        "max": 0.4349315068493151
      }
    },
    "shuffled": {
      "leverage_per_contact": {
        "n": 64,
        "mean": 0.08897047081234108,
        "median": 0.08852539061091558,
        "std": 0.0029383571160163367,
        "ci95_low": 0.0882739691306391,
        "ci95_high": 0.0897614599455369,
        "min": 0.08439770193219072,
        "max": 0.10111970807689001
      },
      "flips_per_contact": {
        "n": 64,
        "mean": 0.08850866865231685,
        "median": 0.08705282133521129,
        "std": 0.008941133950277064,
        "ci95_low": 0.08634586163361363,
        "ci95_high": 0.09077117658204975,
        "min": 0.07078189300411522,
        "max": 0.11401673640167365
      },
      "flips_per_transmission": {
        "n": 64,
        "mean": 0.33540087951005115,
        "median": 0.3373287671232877,
        "std": 0.04353907661270112,
        "ci95_low": 0.32407345326114223,
        "ci95_high": 0.3460189152781316,
        "min": 0.21235521235521235,
        "max": 0.42955326460481097
      }
    },
    "shifted": {
      "leverage_per_contact": {
        "n": 64,
        "mean": 0.08948252192180772,
        "median": 0.08899100144661767,
        "std": 0.0029879045479476664,
        "ci95_low": 0.08881459064399827,
        "ci95_high": 0.09025098301524528,
        "min": 0.08470331989236798,
        "max": 0.10083542168446735
      },
      "flips_per_contact": {
        "n": 64,
        "mean": 0.09073783709264979,
        "median": 0.09030842218510882,
        "std": 0.009393912396779133,
        "ci95_low": 0.08849290606223875,
        "ci95_high": 0.09310159802201917,
        "min": 0.07335907335907337,
        "max": 0.12418300653594772
      },
      "flips_per_transmission": {
        "n": 64,
        "mean": 0.3342673846994712,
        "median": 0.3333333333333333,
        "std": 0.044271936481860036,
        "ci95_low": 0.3234139368791409,
        "ci95_high": 0.3445119807864559,
        "min": 0.20300751879699247,
        "max": 0.4315068493150685
      }
    }
  },
  "paired_tests": {
    "leverage_per_contact": {
      "aligned_gt_shuffled": {
        "mean_difference_B_minus_A": 0.0011909374493933825,
        "p_value": 0.0004997501249375312,
        "permutations": 2000,
        "null_mean": -4.284764065898396e-07,
        "null_q95": 0.0005147724691731142
      },
      "aligned_gt_shifted": {
        "mean_difference_B_minus_A": 0.0006788863399267433,
        "p_value": 0.0034982508745627187,
        "permutations": 2000,
        "null_mean": -2.8341572642507945e-06,
        "null_q95": 0.00040744027680275104
      }
    },
    "flips_per_contact": {
      "aligned_gt_shuffled": {
        "mean_difference_B_minus_A": 0.0015765732633025043,
        "p_value": 0.027486256871564217,
        "permutations": 2000,
        "null_mean": 1.2940319241822144e-05,
        "null_q95": 0.0013803326542860953
      },
      "aligned_gt_shifted": {
        "mean_difference_B_minus_A": -0.0006525951770304415,
        "p_value": 0.8025987006496752,
        "permutations": 2000,
        "null_mean": -3.984325926486947e-08,
        "null_q95": 0.001209882010116486
      }
    },
    "flips_per_transmission": {
      "aligned_gt_shuffled": {
        "mean_difference_B_minus_A": 0.005795223041422709,
        "p_value": 0.06646676661669165,
        "permutations": 2000,
        "null_mean": 5.271738606279615e-05,
        "null_q95": 0.006149605477714687
      },
      "aligned_gt_shifted": {
        "mean_difference_B_minus_A": 0.006928717852002624,
        "p_value": 0.02498750624687656,
        "permutations": 2000,
        "null_mean": -0.0001138066172344189,
        "null_q95": 0.005946272529888532
      }
    }
  },
  "per_group_direction": {
    "leverage_per_contact": {
      "aligned_gt_shuffled_fraction": 0.703125,
      "aligned_gt_shifted_fraction": 0.625,
      "aligned_gt_both_fraction": 0.484375
    },
    "flips_per_contact": {
      "aligned_gt_shuffled_fraction": 0.59375,
      "aligned_gt_shifted_fraction": 0.453125,
      "aligned_gt_both_fraction": 0.359375
    },
    "flips_per_transmission": {
      "aligned_gt_shuffled_fraction": 0.53125,
      "aligned_gt_shifted_fraction": 0.5625,
      "aligned_gt_both_fraction": 0.375
    }
  },
  "trajectory_summary": {
    "aligned": {
      "5": {
        "frontier_exposed_fraction": 0.334496062151257,
        "frontier_contact": 37.421875,
        "sum_delta_p": 2.975928029801504,
        "realized_flips": 2.921875
      },
      "6": {
        "frontier_exposed_fraction": 0.33065086825090967,
        "frontier_contact": 39.03125,
        "sum_delta_p": 3.248724888338428,
        "realized_flips": 3.75
      },
      "7": {
        "frontier_exposed_fraction": 0.3172703460749705,
        "frontier_contact": 39.640625,
        "sum_delta_p": 3.331006151631371,
        "realized_flips": 3.203125
      },
      "8": {
        "frontier_exposed_fraction": 0.3177110066854688,
        "frontier_contact": 42.046875,
        "sum_delta_p": 3.6304630863299376,
        "realized_flips": 3.34375
      },
      "9": {
        "frontier_exposed_fraction": 0.318080903043388,
        "frontier_contact": 44.078125,
        "sum_delta_p": 3.920146560512822,
        "realized_flips": 3.953125
      },
      "10": {
        "frontier_exposed_fraction": 0.31720917346991256,
        "frontier_contact": 46.1875,
        "sum_delta_p": 4.100866553028275,
        "realized_flips": 4.328125
      },
      "11": {
        "frontier_exposed_fraction": 0.31210643725905873,
        "frontier_contact": 47.34375,
        "sum_delta_p": 4.20499969666367,
        "realized_flips": 4.515625
      },
      "12": {
        "frontier_exposed_fraction": 0.3055595556215168,
        "frontier_contact": 48.65625,
        "sum_delta_p": 4.332983863715134,
        "realized_flips": 4.421875
      },
      "13": {
        "frontier_exposed_fraction": 0.31239977040360467,
        "frontier_contact": 51.859375,
        "sum_delta_p": 4.67754430004225,
        "realized_flips": 4.625
      },
      "14": {
        "frontier_exposed_fraction": 0.31595218126646807,
        "frontier_contact": 54.4375,
        "sum_delta_p": 4.952378467538697,
        "realized_flips": 4.859375
      },
      "15": {
        "frontier_exposed_fraction": 0.30894926394319755,
        "frontier_contact": 55.015625,
        "sum_delta_p": 5.010575866379683,
        "realized_flips": 5.21875
      },
      "16": {
        "frontier_exposed_fraction": 0.3130234493852019,
        "frontier_contact": 57.75,
        "sum_delta_p": 5.244610527633537,
        "realized_flips": 5.015625
      },
      "17": {
        "frontier_exposed_fraction": 0.3112994128588874,
        "frontier_contact": 60.21875,
        "sum_delta_p": 5.500678972441953,
        "realized_flips": 5.0625
      },
      "18": {
        "frontier_exposed_fraction": 0.31015741156997856,
        "frontier_contact": 62.40625,
        "sum_delta_p": 5.658702844786998,
        "realized_flips": 5.140625
      },
      "19": {
        "frontier_exposed_fraction": 0.3075038521512975,
        "frontier_contact": 63.53125,
        "sum_delta_p": 5.693114210083595,
        "realized_flips": 5.59375
      },
      "20": {
        "frontier_exposed_fraction": 0.3135329886932982,
        "frontier_contact": 66.5625,
        "sum_delta_p": 6.105885254615436,
        "realized_flips": 6.359375
      },
      "21": {
        "frontier_exposed_fraction": 0.3109148433622346,
        "frontier_contact": 67.890625,
        "sum_delta_p": 6.277674533674591,
        "realized_flips": 5.890625
      },
      "22": {
        "frontier_exposed_fraction": 0.3182550207628694,
        "frontier_contact": 71.90625,
        "sum_delta_p": 6.6870839525754135,
        "realized_flips": 6.421875
      },
      "23": {
        "frontier_exposed_fraction": 0.31956886155777064,
        "frontier_contact": 74.25,
        "sum_delta_p": 6.939056019869852,
        "realized_flips": 7.515625
      },
      "24": {
        "frontier_exposed_fraction": 0.3155103846191699,
        "frontier_contact": 75.8125,
        "sum_delta_p": 6.9018835123705955,
        "realized_flips": 7.421875
      }
    },
    "shuffled": {
      "5": {
        "frontier_exposed_fraction": 0.378690844364867,
        "frontier_contact": 42.4375,
        "sum_delta_p": 3.525357802783682,
        "realized_flips": 3.53125
      },
      "6": {
        "frontier_exposed_fraction": 0.40817567510011044,
        "frontier_contact": 48.1875,
        "sum_delta_p": 4.364023586389374,
        "realized_flips": 5.15625
      },
      "7": {
        "frontier_exposed_fraction": 0.40435545114913246,
        "frontier_contact": 50.3125,
        "sum_delta_p": 4.573052229788436,
        "realized_flips": 4.3125
      },
      "8": {
        "frontier_exposed_fraction": 0.4041018955875997,
        "frontier_contact": 53.234375,
        "sum_delta_p": 4.762965047134378,
        "realized_flips": 4.640625
      },
      "9": {
        "frontier_exposed_fraction": 0.3712833516504232,
        "frontier_contact": 51.21875,
        "sum_delta_p": 4.512022220155922,
        "realized_flips": 4.5
      },
      "10": {
        "frontier_exposed_fraction": 0.3708358742480579,
        "frontier_contact": 53.953125,
        "sum_delta_p": 4.7291357168651835,
        "realized_flips": 4.703125
      },
      "11": {
        "frontier_exposed_fraction": 0.32653984273931164,
        "frontier_contact": 49.453125,
        "sum_delta_p": 4.227653021559095,
        "realized_flips": 4.40625
      },
      "12": {
        "frontier_exposed_fraction": 0.33329475115101814,
        "frontier_contact": 52.984375,
        "sum_delta_p": 4.672330977836655,
        "realized_flips": 4.75
      },
      "13": {
        "frontier_exposed_fraction": 0.3583901170845901,
        "frontier_contact": 59.53125,
        "sum_delta_p": 5.592274751785,
        "realized_flips": 5.53125
      },
      "14": {
        "frontier_exposed_fraction": 0.3515634555878282,
        "frontier_contact": 60.609375,
        "sum_delta_p": 5.591392097270524,
        "realized_flips": 5.671875
      },
      "15": {
        "frontier_exposed_fraction": 0.31554944570431664,
        "frontier_contact": 56.015625,
        "sum_delta_p": 4.887301397922885,
        "realized_flips": 5.0
      },
      "16": {
        "frontier_exposed_fraction": 0.33051562113709365,
        "frontier_contact": 60.90625,
        "sum_delta_p": 5.46059087327732,
        "realized_flips": 5.421875
      },
      "17": {
        "frontier_exposed_fraction": 0.32357568183302254,
        "frontier_contact": 62.734375,
        "sum_delta_p": 5.677587565500994,
        "realized_flips": 5.5
      },
      "18": {
        "frontier_exposed_fraction": 0.2892077762013921,
        "frontier_contact": 58.234375,
        "sum_delta_p": 5.089431504702716,
        "realized_flips": 4.96875
      },
      "19": {
        "frontier_exposed_fraction": 0.2666461731406493,
        "frontier_contact": 55.34375,
        "sum_delta_p": 4.758138511061409,
        "realized_flips": 4.78125
      },
      "20": {
        "frontier_exposed_fraction": 0.2788590436801197,
        "frontier_contact": 59.15625,
        "sum_delta_p": 5.220191683676729,
        "realized_flips": 5.375
      },
      "21": {
        "frontier_exposed_fraction": 0.2933905492634722,
        "frontier_contact": 64.25,
        "sum_delta_p": 6.062433367768299,
        "realized_flips": 5.484375
      },
      "22": {
        "frontier_exposed_fraction": 0.24691821699571914,
        "frontier_contact": 56.078125,
        "sum_delta_p": 4.982955473141796,
        "realized_flips": 4.546875
      },
      "23": {
        "frontier_exposed_fraction": 0.22831782759266273,
        "frontier_contact": 53.265625,
        "sum_delta_p": 4.560904553069935,
        "realized_flips": 5.0
      },
      "24": {
        "frontier_exposed_fraction": 0.2061599066475583,
        "frontier_contact": 49.859375,
        "sum_delta_p": 4.1543878481181125,
        "realized_flips": 3.8125
      }
    },
    "shifted": {
      "5": {
        "frontier_exposed_fraction": 0.378690844364867,
        "frontier_contact": 42.4375,
        "sum_delta_p": 3.525357802783682,
        "realized_flips": 3.53125
      },
      "6": {
        "frontier_exposed_fraction": 0.40817567510011044,
        "frontier_contact": 48.1875,
        "sum_delta_p": 4.364023586389374,
        "realized_flips": 5.15625
      },
      "7": {
        "frontier_exposed_fraction": 0.42227892599672445,
        "frontier_contact": 52.578125,
        "sum_delta_p": 4.91713765234186,
        "realized_flips": 4.640625
      },
      "8": {
        "frontier_exposed_fraction": 0.4368447317093158,
        "frontier_contact": 57.515625,
        "sum_delta_p": 5.404414050760879,
        "realized_flips": 5.25
      },
      "9": {
        "frontier_exposed_fraction": 0.3620742135163242,
        "frontier_contact": 49.796875,
        "sum_delta_p": 4.421717257543765,
        "realized_flips": 4.46875
      },
      "10": {
        "frontier_exposed_fraction": 0.3252228915894129,
        "frontier_contact": 47.265625,
        "sum_delta_p": 4.005797499747711,
        "realized_flips": 4.078125
      },
      "11": {
        "frontier_exposed_fraction": 0.2993153280851588,
        "frontier_contact": 45.375,
        "sum_delta_p": 3.8415714548229243,
        "realized_flips": 4.0
      },
      "12": {
        "frontier_exposed_fraction": 0.29224779314169913,
        "frontier_contact": 46.609375,
        "sum_delta_p": 4.0345263939270755,
        "realized_flips": 4.28125
      },
      "13": {
        "frontier_exposed_fraction": 0.29279986581457207,
        "frontier_contact": 48.765625,
        "sum_delta_p": 4.282006309877243,
        "realized_flips": 4.28125
      },
      "14": {
        "frontier_exposed_fraction": 0.28385261365803366,
        "frontier_contact": 49.15625,
        "sum_delta_p": 4.289193185195392,
        "realized_flips": 4.34375
      },
      "15": {
        "frontier_exposed_fraction": 0.2742349141835428,
        "frontier_contact": 48.921875,
        "sum_delta_p": 4.28588579369608,
        "realized_flips": 4.40625
      },
      "16": {
        "frontier_exposed_fraction": 0.26958298660319485,
        "frontier_contact": 50.03125,
        "sum_delta_p": 4.354396253400168,
        "realized_flips": 4.171875
      },
      "17": {
        "frontier_exposed_fraction": 0.2717504481512112,
        "frontier_contact": 52.875,
        "sum_delta_p": 4.721152795653573,
        "realized_flips": 4.515625
      },
      "18": {
        "frontier_exposed_fraction": 0.27604714684854026,
        "frontier_contact": 55.609375,
        "sum_delta_p": 5.016210854614663,
        "realized_flips": 5.140625
      },
      "19": {
        "frontier_exposed_fraction": 0.2715415327532225,
        "frontier_contact": 56.328125,
        "sum_delta_p": 5.06722427581139,
        "realized_flips": 5.015625
      },
      "20": {
        "frontier_exposed_fraction": 0.2793186312667785,
        "frontier_contact": 59.375,
        "sum_delta_p": 5.399653567873896,
        "realized_flips": 5.734375
      },
      "21": {
        "frontier_exposed_fraction": 0.2790829626875597,
        "frontier_contact": 60.953125,
        "sum_delta_p": 5.592956602920705,
        "realized_flips": 5.671875
      },
      "22": {
        "frontier_exposed_fraction": 0.27780273622959784,
        "frontier_contact": 62.765625,
        "sum_delta_p": 5.728880462121911,
        "realized_flips": 5.578125
      },
      "23": {
        "frontier_exposed_fraction": 0.27301661199262983,
        "frontier_contact": 63.5625,
        "sum_delta_p": 5.797947012983223,
        "realized_flips": 6.21875
      },
      "24": {
        "frontier_exposed_fraction": 0.2765452120441779,
        "frontier_contact": 66.59375,
        "sum_delta_p": 5.979381782797688,
        "realized_flips": 6.125
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "V10 asks whether temporal arrangement changes causal productivity per unit of accessible frontier opportunity and per realized transmission, rather than whether it increases gross accessibility."
}
```
