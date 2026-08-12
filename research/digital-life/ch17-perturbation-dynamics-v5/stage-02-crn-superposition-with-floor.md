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
