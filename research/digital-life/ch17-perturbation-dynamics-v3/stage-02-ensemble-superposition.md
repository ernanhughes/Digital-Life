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
