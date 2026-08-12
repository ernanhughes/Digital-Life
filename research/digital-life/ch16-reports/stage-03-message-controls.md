# Stage 3 — Correlation Is Not Communication

The receiver is tested against six streams:

```text
REAL sender events

SHUFFLED
same bits, chronology destroyed

UNRELATED REPLAY — COUNT MATCHED
different sender of the same Digital Crystal class,
forced to exactly the same pulse count as the real stream

IPI-PERMUTATION SURROGATE
same pulse count and exact multiset of inter-pulse intervals,
but interval order is permuted

RATE-MATCHED RANDOM
same number of bits, random times

NO CHANNEL
```

Every replicate first finds the longest **common** receiver horizon for which
all six conditions remain below the predeclared hard-radius saturation guard of
`0.85`. Every condition in that replicate is then evaluated
at exactly that same horizon. Saturation therefore cannot make one control run
for less time than another or collapse all endpoint morphologies onto the same
filled disk.

```json
{
  "replicates": 60,
  "message_gain": 0.65,
  "saturation_guard": 0.85,
  "hard_radius_capacity": 9577,
  "requested_steps": 90,
  "common_safe_horizon_summary": {
    "n": 60,
    "mean": 75.5,
    "std": 1.1761519176251567,
    "median": 76.0,
    "q05": 73.95,
    "q25": 75.0,
    "q75": 76.0,
    "q95": 77.0,
    "min": 73.0,
    "max": 78.0
  },
  "all_replicates_used_equal_horizon_across_conditions": true,
  "control_summary": {
    "real": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.3672576243656597,
        "std": 0.08830823801523097,
        "median": 0.36823195150536003,
        "q05": 0.20610711012075747,
        "q25": 0.31692903422462015,
        "q75": 0.41832914893351564,
        "q95": 0.5002644280510793,
        "min": 0.17097560675968193,
        "max": 0.5678506771802312
      },
      "post_message_growth": {
        "n": 60,
        "mean": 118.33456671747186,
        "std": 4.793864829417774,
        "median": 118.04217076901682,
        "q05": 111.21161067193674,
        "q25": 114.83195200395843,
        "q75": 121.42276324289406,
        "q95": 125.26300366300366,
        "min": 109.59259259259258,
        "max": 131.04761904761907
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09942738025111161,
        "std": 0.010460074526400957,
        "median": 0.0989472445274697,
        "q05": 0.08608343600893557,
        "q25": 0.09181040830674139,
        "q75": 0.10740292432368564,
        "q95": 0.11572561137915068,
        "min": 0.07956356503616525,
        "max": 0.12840285080032715
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8176481848874038,
        "std": 0.026547748294444902,
        "median": 0.827921060875013,
        "q05": 0.7788921374125509,
        "q25": 0.8032525843165919,
        "q75": 0.8365354495144617,
        "q95": 0.847248616476976,
        "min": 0.7300824892972747,
        "max": 0.8498485955936097
      },
      "pulse_count": {
        "n": 60,
        "mean": 47.46666666666667,
        "std": 2.4729649321321876,
        "median": 48.0,
        "q05": 43.0,
        "q25": 46.0,
        "q75": 49.0,
        "q95": 51.05,
        "min": 42.0,
        "max": 52.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.883333333333334,
        "std": 3.979496059664953,
        "median": 9.0,
        "q05": 0.0,
        "q25": 5.75,
        "q75": 11.25,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "shuffled": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.07330226093493512,
        "std": 0.1202878632956531,
        "median": 0.0889440798346463,
        "q05": -0.13842222981098137,
        "q25": -0.0010428130187523162,
        "q75": 0.1617040741938104,
        "q95": 0.2484407616239922,
        "min": -0.19606859976570434,
        "max": 0.26696862931348997
      },
      "post_message_growth": {
        "n": 60,
        "mean": 106.3279892473885,
        "std": 7.28577419699968,
        "median": 107.33430458430458,
        "q05": 93.53242242242241,
        "q25": 101.80148809523808,
        "q75": 112.49166666666667,
        "q95": 117.14910287081341,
        "min": 85.41085271317829,
        "max": 119.03875968992247
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.10862395180180859,
        "std": 0.016727631403359585,
        "median": 0.1053072602884958,
        "q05": 0.08660292456065675,
        "q25": 0.0969966766828286,
        "q75": 0.12085432347851761,
        "q95": 0.13183992113992277,
        "min": 0.06987237334020885,
        "max": 0.16908884114747882
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8166649263861334,
        "std": 0.023797462699489593,
        "median": 0.823170095019317,
        "q05": 0.7729925864049285,
        "q25": 0.8017124360446903,
        "q75": 0.8357784274825102,
        "q95": 0.844110890675577,
        "min": 0.7593192022554036,
        "max": 0.8466116738018169
      },
      "pulse_count": {
        "n": 60,
        "mean": 41.3,
        "std": 2.9737742572921255,
        "median": 41.0,
        "q05": 35.95,
        "q25": 40.0,
        "q75": 43.0,
        "q95": 46.0,
        "min": 35.0,
        "max": 48.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 4.833333333333333,
        "std": 4.879093722768149,
        "median": 4.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 9.25,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "unrelated_replay_count_matched": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.38233599859631373,
        "std": 0.08721820539751232,
        "median": 0.37006883165601523,
        "q05": 0.22310898441264745,
        "q25": 0.3298002587747973,
        "q75": 0.44682529747433514,
        "q95": 0.5167164460816047,
        "min": 0.17500858815082412,
        "max": 0.5841725831914119
      },
      "post_message_growth": {
        "n": 60,
        "mean": 118.28250048225715,
        "std": 5.7588731374962014,
        "median": 118.48731884057969,
        "q05": 108.49634259259257,
        "q25": 114.93720147633522,
        "q75": 121.5656429238362,
        "q95": 128.53387295713847,
        "min": 106.00694444444444,
        "max": 129.12015503875966
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09739943211326677,
        "std": 0.011345830424237225,
        "median": 0.09549240927002622,
        "q05": 0.08164266896189828,
        "q25": 0.0880656233347802,
        "q75": 0.10540727886528789,
        "q95": 0.11981249724843343,
        "min": 0.07269179168191243,
        "max": 0.12265178328341955
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.814780202568654,
        "std": 0.022831624964018325,
        "median": 0.8175837945076747,
        "q05": 0.7688942257491908,
        "q25": 0.8036963558525634,
        "q75": 0.8305053774668476,
        "q95": 0.8439699279523859,
        "min": 0.7420904249765062,
        "max": 0.84828234311371
      },
      "pulse_count": {
        "n": 60,
        "mean": 47.333333333333336,
        "std": 2.7426669907632286,
        "median": 47.0,
        "q05": 43.0,
        "q25": 45.75,
        "q75": 49.0,
        "q95": 51.05,
        "min": 43.0,
        "max": 56.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.6,
        "std": 4.131989028704376,
        "median": 9.0,
        "q05": 0.0,
        "q25": 4.0,
        "q75": 11.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "ipi_permutation_surrogate": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.3568837829278093,
        "std": 0.24906804992006232,
        "median": 0.39908724952423164,
        "q05": -0.04662407700122897,
        "q25": 0.18517475041604387,
        "q75": 0.5352533331507222,
        "q95": 0.7149744304522527,
        "min": -0.28686194011280447,
        "max": 0.760898571184882
      },
      "post_message_growth": {
        "n": 60,
        "mean": 116.77985379986605,
        "std": 17.19332719166506,
        "median": 116.11307919394172,
        "q05": 88.89274231678488,
        "q25": 103.51444444444445,
        "q75": 129.1187510811278,
        "q95": 144.81104166666665,
        "min": 83.17307692307693,
        "max": 151.70731707317074
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09901520137424781,
        "std": 0.012682144519349096,
        "median": 0.09503778947432479,
        "q05": 0.08118215758814697,
        "q25": 0.09095302937505673,
        "q75": 0.1063123981387548,
        "q95": 0.12025246660196375,
        "min": 0.07818088911599387,
        "max": 0.1383890834440285
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8161236991403015,
        "std": 0.025122521185842912,
        "median": 0.8191500469875744,
        "q05": 0.7665552887125404,
        "q25": 0.8056280672444398,
        "q75": 0.8392241829382896,
        "q95": 0.8462984233058369,
        "min": 0.7439699279523859,
        "max": 0.8485955936096898
      },
      "pulse_count": {
        "n": 60,
        "mean": 46.583333333333336,
        "std": 4.375277768959996,
        "median": 47.0,
        "q05": 39.0,
        "q25": 44.0,
        "q75": 50.0,
        "q95": 53.0,
        "min": 34.0,
        "max": 56.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.35,
        "std": 4.05308524460071,
        "median": 8.0,
        "q05": 0.0,
        "q25": 3.75,
        "q75": 11.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "rate_matched_random": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.09737060379589658,
        "std": 0.10691832357113344,
        "median": 0.11082465742557349,
        "q05": -0.07262456915797011,
        "q25": 0.02081175934988306,
        "q75": 0.1750820537841149,
        "q95": 0.26444665033916187,
        "min": -0.16792758465860294,
        "max": 0.28060997237438867
      },
      "post_message_growth": {
        "n": 60,
        "mean": 108.41278488548718,
        "std": 6.827834030544102,
        "median": 108.95670045045044,
        "q05": 97.46068665377176,
        "q25": 103.5093984962406,
        "q75": 113.91948621553885,
        "q95": 117.89989233419466,
        "min": 94.31818181818181,
        "max": 122.02916666666665
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.10580153987731428,
        "std": 0.017390779759052528,
        "median": 0.10202646276910096,
        "q05": 0.08543835697295755,
        "q25": 0.09259653574805683,
        "q75": 0.1144357053484759,
        "q95": 0.13731105766024143,
        "min": 0.07899440009531752,
        "max": 0.16606045403235922
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8185496502036129,
        "std": 0.02005882061839006,
        "median": 0.823639970763287,
        "q05": 0.7810692283596116,
        "q25": 0.8033308969405868,
        "q75": 0.8338728202986322,
        "q95": 0.8456614806306777,
        "min": 0.7652709616790226,
        "max": 0.8499530124256031
      },
      "pulse_count": {
        "n": 60,
        "mean": 41.05,
        "std": 3.106042498099471,
        "median": 41.5,
        "q05": 35.0,
        "q25": 39.0,
        "q75": 44.0,
        "q95": 46.0,
        "min": 35.0,
        "max": 47.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 4.683333333333334,
        "std": 4.720493147495879,
        "median": 4.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 9.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "no_channel": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "post_message_growth": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.7982109916118478,
        "std": 0.026298745840089177,
        "median": 0.7976923880129477,
        "q05": 0.7630259997911664,
        "q25": 0.7856844523337162,
        "q75": 0.8139292053879085,
        "q95": 0.8363892659496711,
        "min": 0.697922105043333,
        "max": 0.8481779262817166
      },
      "pulse_count": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      }
    }
  },
  "real_vs_controls": {
    "shuffled": {
      "real_minus_control_mean": 0.29395536343072454,
      "pairwise_superiority_probability": 0.9802777777777778
    },
    "unrelated_replay_count_matched": {
      "real_minus_control_mean": -0.015078374230654057,
      "pairwise_superiority_probability": 0.45694444444444443
    },
    "ipi_permutation_surrogate": {
      "real_minus_control_mean": 0.010373841437850362,
      "pairwise_superiority_probability": 0.4725
    },
    "rate_matched_random": {
      "real_minus_control_mean": 0.2698870205697631,
      "pairwise_superiority_probability": 0.9772222222222222
    }
  },
  "figure": "static\\images\\books\\digital-life\\ch16-03-message-controls.png"
}
```

Figure: `static\images\books\digital-life\ch16-03-message-controls.png`

The real stream must beat not only naive timing controls but also a count-matched
unrelated sender and an exact-IPI-distribution surrogate before sender-specific
signalling is supported.
