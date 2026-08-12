# Stage 2 — Does Opportunity Feedback Extend Causal Accessibility?

```json
{
  "groups": 64,
  "window": {
    "start": 5,
    "end": 24
  },
  "summary": {
    "natural_feedback": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 6.570424375171614,
        "median": 6.271008972063322,
        "std": 1.872161058786317,
        "ci95_low": 6.116847125411917,
        "ci95_high": 7.045105437618863,
        "min": 3.098199665631315,
        "max": 11.30892493228149
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 1141.03125,
        "median": 1075.5,
        "std": 335.56333086831387,
        "ci95_low": 1057.573828125,
        "ci95_high": 1221.2937499999998,
        "min": 522.0,
        "max": 1887.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 101.15680891173673,
        "median": 95.25820796384079,
        "std": 30.363153219306742,
        "ci95_low": 93.63405142926803,
        "ci95_high": 108.33258984733783,
        "min": 45.36253328673109,
        "max": 172.07033104629213
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 101.125,
        "median": 96.5,
        "std": 31.48139331414669,
        "ci95_low": 93.460546875,
        "ci95_high": 108.523828125,
        "min": 48.0,
        "max": 168.0
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
      "cumulative_transmissions": {
        "n": 64,
        "mean": 288.5625,
        "median": 273.5,
        "std": 82.32516986772636,
        "ci95_low": 269.59296875,
        "ci95_high": 309.416015625,
        "min": 140.0,
        "max": 480.0
      }
    },
    "clamped_schedule": {
      "access_fraction_auc": {
        "n": 64,
        "mean": 6.087766924912971,
        "median": 6.031185665208994,
        "std": 0.6493051797870265,
        "ci95_low": 5.920361320065435,
        "ci95_high": 6.238539739018349,
        "min": 3.860752923403941,
        "max": 7.641022574391508
      },
      "contact_count_auc": {
        "n": 64,
        "mean": 1049.25,
        "median": 1055.0,
        "std": 99.23472804416808,
        "ci95_low": 1024.802734375,
        "ci95_high": 1073.654296875,
        "min": 671.0,
        "max": 1209.0
      },
      "probability_leverage_auc": {
        "n": 64,
        "mean": 93.90411500575206,
        "median": 93.73053902495244,
        "std": 6.771534645844426,
        "ci95_low": 92.25819837423927,
        "ci95_high": 95.48318010840715,
        "min": 66.44779423872184,
        "max": 106.28654244432389
      },
      "total_realized_flips": {
        "n": 64,
        "mean": 94.625,
        "median": 93.5,
        "std": 9.728341328304635,
        "ci95_low": 92.32734375,
        "ci95_high": 96.930859375,
        "min": 67.0,
        "max": 113.0
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
      "cumulative_transmissions": {
        "n": 64,
        "mean": 274.734375,
        "median": 275.0,
        "std": 0.8703840298253409,
        "ci95_low": 274.484375,
        "ci95_high": 274.90625,
        "min": 270.0,
        "max": 275.0
      }
    }
  },
  "trajectory_summary": {
    "natural_feedback": {
      "5": {
        "frontier_exposed_fraction": 0.345735522191119,
        "frontier_contact": 38.671875,
        "sum_delta_p": 3.0300289599606334,
        "realized_flips": 2.78125
      },
      "6": {
        "frontier_exposed_fraction": 0.33999022524017686,
        "frontier_contact": 40.03125,
        "sum_delta_p": 3.353295552401129,
        "realized_flips": 3.359375
      },
      "7": {
        "frontier_exposed_fraction": 0.33714573528614,
        "frontier_contact": 41.484375,
        "sum_delta_p": 3.5587126844084938,
        "realized_flips": 3.109375
      },
      "8": {
        "frontier_exposed_fraction": 0.33464392248842584,
        "frontier_contact": 43.1875,
        "sum_delta_p": 3.7882339052965213,
        "realized_flips": 3.8125
      },
      "9": {
        "frontier_exposed_fraction": 0.33230810638864255,
        "frontier_contact": 44.96875,
        "sum_delta_p": 3.9598294023738836,
        "realized_flips": 4.078125
      },
      "10": {
        "frontier_exposed_fraction": 0.3267892206874521,
        "frontier_contact": 46.703125,
        "sum_delta_p": 4.1697490154537125,
        "realized_flips": 4.09375
      },
      "11": {
        "frontier_exposed_fraction": 0.32717320432112335,
        "frontier_contact": 48.90625,
        "sum_delta_p": 4.290302310627986,
        "realized_flips": 5.109375
      },
      "12": {
        "frontier_exposed_fraction": 0.32671271181809586,
        "frontier_contact": 51.234375,
        "sum_delta_p": 4.545251068099416,
        "realized_flips": 4.5625
      },
      "13": {
        "frontier_exposed_fraction": 0.32394080402655456,
        "frontier_contact": 53.21875,
        "sum_delta_p": 4.764670132779225,
        "realized_flips": 4.40625
      },
      "14": {
        "frontier_exposed_fraction": 0.3259035736092254,
        "frontier_contact": 55.59375,
        "sum_delta_p": 4.991656221145075,
        "realized_flips": 4.90625
      },
      "15": {
        "frontier_exposed_fraction": 0.3251075957158356,
        "frontier_contact": 57.46875,
        "sum_delta_p": 5.121874928679904,
        "realized_flips": 5.4375
      },
      "16": {
        "frontier_exposed_fraction": 0.3251364141413705,
        "frontier_contact": 59.8125,
        "sum_delta_p": 5.318771413217763,
        "realized_flips": 5.34375
      },
      "17": {
        "frontier_exposed_fraction": 0.3234169767688855,
        "frontier_contact": 61.9375,
        "sum_delta_p": 5.513548217370291,
        "realized_flips": 5.59375
      },
      "18": {
        "frontier_exposed_fraction": 0.3215680986925267,
        "frontier_contact": 63.890625,
        "sum_delta_p": 5.637456431582679,
        "realized_flips": 5.75
      },
      "19": {
        "frontier_exposed_fraction": 0.3205637381445243,
        "frontier_contact": 66.046875,
        "sum_delta_p": 5.952547332614193,
        "realized_flips": 6.03125
      },
      "20": {
        "frontier_exposed_fraction": 0.3256974194633818,
        "frontier_contact": 68.953125,
        "sum_delta_p": 6.217827265878549,
        "realized_flips": 5.890625
      },
      "21": {
        "frontier_exposed_fraction": 0.32717508420227503,
        "frontier_contact": 71.5,
        "sum_delta_p": 6.453670227634204,
        "realized_flips": 6.84375
      },
      "22": {
        "frontier_exposed_fraction": 0.3271081546584758,
        "frontier_contact": 73.65625,
        "sum_delta_p": 6.683986616004736,
        "realized_flips": 6.1875
      },
      "23": {
        "frontier_exposed_fraction": 0.3269154393060703,
        "frontier_contact": 75.59375,
        "sum_delta_p": 6.768863972674634,
        "realized_flips": 6.90625
      },
      "24": {
        "frontier_exposed_fraction": 0.32739242802131163,
        "frontier_contact": 78.171875,
        "sum_delta_p": 7.036533253533706,
        "realized_flips": 6.921875
      }
    },
    "clamped_schedule": {
      "5": {
        "frontier_exposed_fraction": 0.3426053508754795,
        "frontier_contact": 38.28125,
        "sum_delta_p": 3.00840771086869,
        "realized_flips": 2.75
      },
      "6": {
        "frontier_exposed_fraction": 0.3358047683613362,
        "frontier_contact": 39.421875,
        "sum_delta_p": 3.309007726430303,
        "realized_flips": 3.265625
      },
      "7": {
        "frontier_exposed_fraction": 0.3238068410621825,
        "frontier_contact": 39.78125,
        "sum_delta_p": 3.42256765773777,
        "realized_flips": 3.046875
      },
      "8": {
        "frontier_exposed_fraction": 0.31509738496447004,
        "frontier_contact": 40.578125,
        "sum_delta_p": 3.5481051422837324,
        "realized_flips": 3.546875
      },
      "9": {
        "frontier_exposed_fraction": 0.31662522960013006,
        "frontier_contact": 42.828125,
        "sum_delta_p": 3.7915028066947776,
        "realized_flips": 3.84375
      },
      "10": {
        "frontier_exposed_fraction": 0.294951684745268,
        "frontier_contact": 42.125,
        "sum_delta_p": 3.720543477851493,
        "realized_flips": 3.828125
      },
      "11": {
        "frontier_exposed_fraction": 0.2978573929465353,
        "frontier_contact": 44.734375,
        "sum_delta_p": 3.9439972090216333,
        "realized_flips": 4.65625
      },
      "12": {
        "frontier_exposed_fraction": 0.2951286951510631,
        "frontier_contact": 46.3125,
        "sum_delta_p": 4.081548769819953,
        "realized_flips": 4.171875
      },
      "13": {
        "frontier_exposed_fraction": 0.2965227039823929,
        "frontier_contact": 48.75,
        "sum_delta_p": 4.422215468734387,
        "realized_flips": 4.078125
      },
      "14": {
        "frontier_exposed_fraction": 0.30274089128849274,
        "frontier_contact": 51.453125,
        "sum_delta_p": 4.743637339525698,
        "realized_flips": 4.546875
      },
      "15": {
        "frontier_exposed_fraction": 0.30880997312060043,
        "frontier_contact": 54.5625,
        "sum_delta_p": 5.008609458763935,
        "realized_flips": 5.546875
      },
      "16": {
        "frontier_exposed_fraction": 0.3000311652849179,
        "frontier_contact": 54.828125,
        "sum_delta_p": 4.971564776747991,
        "realized_flips": 5.359375
      },
      "17": {
        "frontier_exposed_fraction": 0.291024254621994,
        "frontier_contact": 55.390625,
        "sum_delta_p": 4.945764359686989,
        "realized_flips": 4.953125
      },
      "18": {
        "frontier_exposed_fraction": 0.29436389241533517,
        "frontier_contact": 58.390625,
        "sum_delta_p": 5.252861975172847,
        "realized_flips": 5.40625
      },
      "19": {
        "frontier_exposed_fraction": 0.2936526566027233,
        "frontier_contact": 60.359375,
        "sum_delta_p": 5.497832039471763,
        "realized_flips": 5.46875
      },
      "20": {
        "frontier_exposed_fraction": 0.29431850850416824,
        "frontier_contact": 62.140625,
        "sum_delta_p": 5.616521787306411,
        "realized_flips": 5.578125
      },
      "21": {
        "frontier_exposed_fraction": 0.2955911777565662,
        "frontier_contact": 64.234375,
        "sum_delta_p": 5.838970779828717,
        "realized_flips": 6.125
      },
      "22": {
        "frontier_exposed_fraction": 0.2963800443690381,
        "frontier_contact": 66.546875,
        "sum_delta_p": 6.14621249698342,
        "realized_flips": 5.734375
      },
      "23": {
        "frontier_exposed_fraction": 0.2964116954446573,
        "frontier_contact": 68.1875,
        "sum_delta_p": 6.212240465964419,
        "realized_flips": 6.421875
      },
      "24": {
        "frontier_exposed_fraction": 0.29604261381562,
        "frontier_contact": 70.34375,
        "sum_delta_p": 6.422003556857135,
        "realized_flips": 6.296875
      }
    }
  },
  "paired_tests_natural_gt_clamped": {
    "access_fraction_auc": {
      "mean_difference_B_minus_A": 0.4826574502586417,
      "p_value": 0.0069965017491254375,
      "permutations": 2000,
      "null_mean": 0.0004780085767394384,
      "null_q95": 0.3105500331568312
    },
    "probability_leverage_auc": {
      "mean_difference_B_minus_A": 7.252693905984672,
      "p_value": 0.018490754622688656,
      "permutations": 2000,
      "null_mean": 0.09731027884254208,
      "null_q95": 5.601391045106011
    },
    "total_realized_flips": {
      "mean_difference_B_minus_A": 6.5,
      "p_value": 0.030984507746126936,
      "permutations": 2000,
      "null_mean": -0.0816875,
      "null_q95": 5.626562499999999
    },
    "sustained_loss_time": {
      "mean_difference_B_minus_A": 0.0,
      "p_value": 1.0,
      "permutations": 2000,
      "null_mean": 0.0,
      "null_q95": 0.0
    }
  },
  "natural_gt_clamped_cumulative_transmissions_test": {
    "mean_difference_B_minus_A": 13.828125,
    "p_value": 0.09495252373813093,
    "permutations": 2000,
    "null_mean": -0.058875,
    "null_q95": 16.831249999999997
  },
  "clamped_schedule_truncation_rate": 0.006510416666666667,
  "status": "MEASURED",
  "bounded_statement": "V8 compares an endogenous opportunity-feedback branch with a branch whose propagation opportunity is clamped to a frozen exogenous schedule."
}
```
