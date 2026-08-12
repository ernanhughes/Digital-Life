# Stage 2 — Does Surface-Biased Transmission Keep State on the Active Surface?

```json
{
  "groups_per_policy": 48,
  "transmission_fraction": 0.5,
  "policies": [
    "none",
    "uniform_budget",
    "surface_biased_budget"
  ],
  "observation_steps": [
    4,
    5,
    6,
    7,
    8,
    10,
    12,
    14,
    18,
    22
  ],
  "results": {
    "none": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.7078125,
            "ci95_high": 21.6046875,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 11.958333333333334,
            "median": 12.5,
            "std": 4.046388993768257,
            "ci95_low": 10.854166666666666,
            "ci95_high": 13.1875,
            "min": 4.0,
            "max": 19.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 17.270833333333332,
            "median": 17.5,
            "std": 5.9851886051225565,
            "ci95_low": 15.603645833333333,
            "ci95_high": 19.125,
            "min": 5.0,
            "max": 29.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.1579942573783961,
            "median": 0.15743155149934812,
            "std": 0.05535856442893996,
            "ci95_low": 0.14247890392912113,
            "ci95_high": 0.1735339044383857,
            "min": 0.045454545454545456,
            "max": 0.27450980392156865
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.916145833333335,
            "ci95_high": 21.688020833333333,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 5.958333333333333,
            "median": 6.0,
            "std": 2.6611270586392943,
            "ci95_low": 5.25,
            "ci95_high": 6.729166666666667,
            "min": 2.0,
            "max": 12.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 7.479166666666667,
            "median": 7.0,
            "std": 3.889031495401165,
            "ci95_low": 6.354166666666667,
            "ci95_high": 8.645833333333334,
            "min": 2.0,
            "max": 18.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.06429434693793058,
            "median": 0.05785123966942149,
            "std": 0.03475174930121549,
            "ci95_low": 0.054838903761196836,
            "ci95_high": 0.07469951181603625,
            "min": 0.017094017094017096,
            "max": 0.17647058823529413
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.5,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 2.4166666666666665,
            "median": 2.0,
            "std": 1.8577914008006629,
            "ci95_low": 1.9369791666666667,
            "ci95_high": 2.9375,
            "min": 0.0,
            "max": 9.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 2.6666666666666665,
            "median": 2.0,
            "std": 2.084999333866134,
            "ci95_low": 2.125,
            "ci95_high": 3.25,
            "min": 0.0,
            "max": 9.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.021446431521033548,
            "median": 0.01652892561983471,
            "std": 0.017230173318250153,
            "ci95_low": 0.017015718832941326,
            "ci95_high": 0.02653173721330402,
            "min": 0.0,
            "max": 0.07964601769911504
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.74791666666667,
            "ci95_high": 21.6875,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.7916666666666666,
            "median": 1.0,
            "std": 0.840593375076334,
            "ci95_low": 0.5416666666666666,
            "ci95_high": 1.0416666666666667,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.7916666666666666,
            "median": 1.0,
            "std": 0.8650224788344456,
            "ci95_low": 0.5625,
            "ci95_high": 1.0416666666666667,
            "min": 0.0,
            "max": 4.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.006031626323591929,
            "median": 0.006872933396315541,
            "std": 0.006806823737821128,
            "ci95_low": 0.004218595925094516,
            "ci95_high": 0.007811997313790884,
            "min": 0.0,
            "max": 0.03225806451612903
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.708333333333332,
            "ci95_high": 21.708333333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.041666666666666664,
            "median": 0.0,
            "std": 0.19982631347136337,
            "ci95_low": 0.0,
            "ci95_high": 0.10416666666666667,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.041666666666666664,
            "median": 0.0,
            "std": 0.19982631347136337,
            "ci95_low": 0.0,
            "ci95_high": 0.10416666666666667,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0002997988446461729,
            "median": 0.0,
            "std": 0.0014405671314657376,
            "ci95_low": 0.0,
            "ci95_high": 0.0007586307681727529,
            "min": 0.0,
            "max": 0.007633587786259542
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.7703125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "14": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "18": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.875,
            "ci95_high": 21.583333333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        },
        "22": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8953125,
            "ci95_high": 21.645833333333332,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 10,
        "positive_contact_observed_through_final_step": false
      }
    },
    "uniform_budget": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 30.0,
            "median": 28.0,
            "std": 7.213991035943049,
            "ci95_low": 27.8328125,
            "ci95_high": 32.021875,
            "min": 15.0,
            "max": 48.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.208333333333332,
            "median": 19.5,
            "std": 5.431230421266335,
            "ci95_low": 18.75,
            "ci95_high": 21.7921875,
            "min": 8.0,
            "max": 33.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 31.020833333333332,
            "median": 32.0,
            "std": 8.120164159191747,
            "ci95_low": 28.666145833333335,
            "ci95_high": 33.25,
            "min": 10.0,
            "max": 48.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.2833130981545109,
            "median": 0.2832274758880263,
            "std": 0.06955614627943915,
            "ci95_low": 0.26313965937901457,
            "ci95_high": 0.30209509373744864,
            "min": 0.09090909090909091,
            "max": 0.42857142857142855
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 38.020833333333336,
            "median": 38.0,
            "std": 8.837631619324766,
            "ci95_low": 35.833333333333336,
            "ci95_high": 40.729166666666664,
            "min": 17.0,
            "max": 60.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 18.770833333333332,
            "median": 18.5,
            "std": 5.058983689657659,
            "ci95_low": 17.291666666666668,
            "ci95_high": 20.208333333333332,
            "min": 5.0,
            "max": 30.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 26.666666666666668,
            "median": 26.5,
            "std": 7.638535345353992,
            "ci95_low": 24.541145833333335,
            "ci95_high": 28.791666666666668,
            "min": 7.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.2293806858974594,
            "median": 0.22504347826086957,
            "std": 0.06565839298927652,
            "ci95_low": 0.21186850231914714,
            "ci95_high": 0.24739903427227108,
            "min": 0.0603448275862069,
            "max": 0.37254901960784315
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 45.375,
            "median": 45.0,
            "std": 10.75411742853251,
            "ci95_low": 42.395833333333336,
            "ci95_high": 48.522395833333334,
            "min": 18.0,
            "max": 72.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 16.958333333333332,
            "median": 16.5,
            "std": 5.2637056549756105,
            "ci95_low": 15.436979166666667,
            "ci95_high": 18.291666666666668,
            "min": 5.0,
            "max": 28.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 22.354166666666668,
            "median": 22.0,
            "std": 6.743792155670939,
            "ci95_low": 20.5203125,
            "ci95_high": 24.104166666666668,
            "min": 7.0,
            "max": 38.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.18113190545644176,
            "median": 0.18344751651578176,
            "std": 0.05485474631813467,
            "ci95_low": 0.1664459802765414,
            "ci95_high": 0.19740255002232002,
            "min": 0.05982905982905983,
            "max": 0.3157894736842105
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 51.729166666666664,
            "median": 52.0,
            "std": 12.272495642922655,
            "ci95_low": 48.2078125,
            "ci95_high": 55.39791666666667,
            "min": 20.0,
            "max": 82.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 13.729166666666666,
            "median": 13.0,
            "std": 4.689258929250501,
            "ci95_low": 12.332812500000001,
            "ci95_high": 15.083333333333334,
            "min": 4.0,
            "max": 24.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 17.75,
            "median": 17.5,
            "std": 6.219927652312364,
            "ci95_low": 16.061979166666667,
            "ci95_high": 19.605208333333334,
            "min": 6.0,
            "max": 32.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.13682277746862959,
            "median": 0.13427827306420914,
            "std": 0.04784008685967763,
            "ci95_low": 0.12327019251609986,
            "ci95_high": 0.1507037528535577,
            "min": 0.05084745762711865,
            "max": 0.2549019607843137
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 60.770833333333336,
            "median": 60.5,
            "std": 14.57057477608744,
            "ci95_low": 56.56197916666667,
            "ci95_high": 64.83489583333332,
            "min": 24.0,
            "max": 93.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 8.958333333333334,
            "median": 8.5,
            "std": 3.5937349033499335,
            "ci95_low": 7.9375,
            "ci95_high": 9.896354166666667,
            "min": 2.0,
            "max": 16.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 11.895833333333334,
            "median": 12.0,
            "std": 4.9801254307050895,
            "ci95_low": 10.520312500000001,
            "ci95_high": 13.292187499999999,
            "min": 3.0,
            "max": 22.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.08400472717788872,
            "median": 0.0870843865448182,
            "std": 0.035796464801178075,
            "ci95_low": 0.07438739500088422,
            "ci95_high": 0.09379723581165893,
            "min": 0.022900763358778626,
            "max": 0.16071428571428573
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 66.75,
            "median": 66.5,
            "std": 16.205066080293122,
            "ci95_low": 62.104166666666664,
            "ci95_high": 71.5421875,
            "min": 28.0,
            "max": 104.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 5.75,
            "median": 6.0,
            "std": 3.178705187126775,
            "ci95_low": 4.8125,
            "ci95_high": 6.625,
            "min": 0.0,
            "max": 13.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 7.416666666666667,
            "median": 7.5,
            "std": 4.127314165679931,
            "ci95_low": 6.3125,
            "ci95_high": 8.604166666666666,
            "min": 0.0,
            "max": 15.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.04727299777030209,
            "median": 0.04748150757308912,
            "std": 0.02622978285388272,
            "ci95_low": 0.03981014249850631,
            "ci95_high": 0.05483002661514331,
            "min": 0.0,
            "max": 0.09655172413793103
          }
        },
        "14": {
          "modified_count": {
            "n": 48,
            "mean": 70.52083333333333,
            "median": 71.0,
            "std": 17.53091267748361,
            "ci95_low": 65.70729166666666,
            "ci95_high": 75.54166666666667,
            "min": 32.0,
            "max": 110.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 3.625,
            "median": 3.0,
            "std": 2.32401412789739,
            "ci95_low": 2.9791666666666665,
            "ci95_high": 4.291666666666667,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 5.208333333333333,
            "median": 5.0,
            "std": 3.570471101814001,
            "ci95_low": 4.166145833333333,
            "ci95_high": 6.25,
            "min": 0.0,
            "max": 12.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.030297775460493292,
            "median": 0.028249489274770175,
            "std": 0.020590390237229507,
            "ci95_low": 0.02425659213283865,
            "ci95_high": 0.03608227120041982,
            "min": 0.0,
            "max": 0.07453416149068323
          }
        },
        "18": {
          "modified_count": {
            "n": 48,
            "mean": 75.20833333333333,
            "median": 74.5,
            "std": 19.86512682790847,
            "ci95_low": 69.6875,
            "ci95_high": 80.6875,
            "min": 34.0,
            "max": 118.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 1.75,
            "median": 1.0,
            "std": 2.0052015692526606,
            "ci95_low": 1.1666666666666667,
            "ci95_high": 2.3958333333333335,
            "min": 0.0,
            "max": 7.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 2.3958333333333335,
            "median": 1.0,
            "std": 2.9064553392214525,
            "ci95_low": 1.625,
            "ci95_high": 3.1875,
            "min": 0.0,
            "max": 11.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.012110015760376574,
            "median": 0.005353104514356053,
            "std": 0.014550286188052462,
            "ci95_low": 0.008381082868750686,
            "ci95_high": 0.01647371351589865,
            "min": 0.0,
            "max": 0.05045871559633028
          }
        },
        "22": {
          "modified_count": {
            "n": 48,
            "mean": 76.95833333333333,
            "median": 75.5,
            "std": 21.1137379579163,
            "ci95_low": 71.37447916666666,
            "ci95_high": 83.37708333333333,
            "min": 34.0,
            "max": 126.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 0.6875,
            "median": 0.0,
            "std": 1.2103072956898178,
            "ci95_low": 0.375,
            "ci95_high": 1.1041666666666667,
            "min": 0.0,
            "max": 5.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 0.7291666666666666,
            "median": 0.0,
            "std": 1.3499935699435344,
            "ci95_low": 0.375,
            "ci95_high": 1.1666666666666667,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.003187363097547483,
            "median": 0.0,
            "std": 0.005872395323466511,
            "ci95_low": 0.0017507130894940206,
            "ci95_high": 0.004949181249495169,
            "min": 0.0,
            "max": 0.026905829596412557
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "surface_biased_budget": {
      "summary": {
        "4": {
          "modified_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.8125,
            "ci95_high": 21.729166666666668,
            "min": 11.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 20.166666666666668,
            "median": 19.0,
            "std": 4.925838902043883,
            "ci95_low": 18.791145833333335,
            "ci95_high": 21.500520833333333,
            "min": 11.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 36.979166666666664,
            "median": 36.0,
            "std": 9.640387231445748,
            "ci95_low": 34.24947916666667,
            "ci95_high": 39.75052083333333,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3529194419973969,
            "median": 0.35465342679127726,
            "std": 0.07780522877532682,
            "ci95_low": 0.3294336783923166,
            "ci95_high": 0.37441496157870807,
            "min": 0.13725490196078433,
            "max": 0.5309734513274337
          }
        },
        "5": {
          "modified_count": {
            "n": 48,
            "mean": 30.0,
            "median": 28.0,
            "std": 7.213991035943049,
            "ci95_low": 27.8328125,
            "ci95_high": 32.021875,
            "min": 15.0,
            "max": 48.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 21.791666666666668,
            "median": 21.5,
            "std": 5.887693143800512,
            "ci95_low": 20.22760416666667,
            "ci95_high": 23.520833333333332,
            "min": 8.0,
            "max": 35.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 38.520833333333336,
            "median": 39.0,
            "std": 9.797936822220391,
            "ci95_low": 35.625,
            "ci95_high": 41.3125,
            "min": 14.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.351679707026851,
            "median": 0.36279854620976115,
            "std": 0.08226177545520746,
            "ci95_low": 0.3273894708827673,
            "ci95_high": 0.3733562573372996,
            "min": 0.12727272727272726,
            "max": 0.5357142857142857
          }
        },
        "6": {
          "modified_count": {
            "n": 48,
            "mean": 39.791666666666664,
            "median": 39.0,
            "std": 9.110338297170358,
            "ci95_low": 37.51927083333334,
            "ci95_high": 42.501041666666666,
            "min": 18.0,
            "max": 62.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 24.0,
            "median": 24.0,
            "std": 6.1169164345008555,
            "ci95_low": 22.3328125,
            "ci95_high": 25.75,
            "min": 9.0,
            "max": 36.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 40.1875,
            "median": 41.0,
            "std": 10.321208444266592,
            "ci95_low": 37.309895833333336,
            "ci95_high": 43.126041666666666,
            "min": 12.0,
            "max": 61.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.34514566623170745,
            "median": 0.34218442670369087,
            "std": 0.08480344392365849,
            "ci95_low": 0.3213210285405551,
            "ci95_high": 0.36855598013365054,
            "min": 0.10256410256410256,
            "max": 0.5267857142857143
          }
        },
        "7": {
          "modified_count": {
            "n": 48,
            "mean": 50.458333333333336,
            "median": 49.0,
            "std": 11.952960465461638,
            "ci95_low": 47.08229166666667,
            "ci95_high": 54.083333333333336,
            "min": 20.0,
            "max": 79.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 26.0625,
            "median": 27.0,
            "std": 6.684578801240958,
            "ci95_low": 24.1875,
            "ci95_high": 27.8125,
            "min": 9.0,
            "max": 41.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 41.9375,
            "median": 43.5,
            "std": 11.404323467439882,
            "ci95_low": 38.75,
            "ci95_high": 44.93802083333333,
            "min": 10.0,
            "max": 65.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.33886519517071284,
            "median": 0.333084442030953,
            "std": 0.08745959221099439,
            "ci95_low": 0.31387924718344956,
            "ci95_high": 0.36216403851636936,
            "min": 0.08547008547008547,
            "max": 0.5284552845528455
          }
        },
        "8": {
          "modified_count": {
            "n": 48,
            "mean": 62.125,
            "median": 62.0,
            "std": 14.862740045720596,
            "ci95_low": 58.0,
            "ci95_high": 66.64635416666667,
            "min": 24.0,
            "max": 98.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 27.145833333333332,
            "median": 28.0,
            "std": 7.4330051777341195,
            "ci95_low": 24.958333333333332,
            "ci95_high": 29.396354166666665,
            "min": 7.0,
            "max": 44.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 44.020833333333336,
            "median": 44.5,
            "std": 12.658148863040317,
            "ci95_low": 40.49947916666667,
            "ci95_high": 47.58385416666667,
            "min": 12.0,
            "max": 72.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3394309805989059,
            "median": 0.34307036247334755,
            "std": 0.09378107114189417,
            "ci95_low": 0.3126744613461368,
            "ci95_high": 0.3644205072343863,
            "min": 0.1016949152542373,
            "max": 0.5106382978723404
          }
        },
        "10": {
          "modified_count": {
            "n": 48,
            "mean": 85.625,
            "median": 87.0,
            "std": 21.417112511571986,
            "ci95_low": 79.62239583333333,
            "ci95_high": 91.7921875,
            "min": 32.0,
            "max": 142.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 29.729166666666668,
            "median": 29.5,
            "std": 8.56528746193352,
            "ci95_low": 27.3125,
            "ci95_high": 31.855729166666666,
            "min": 9.0,
            "max": 52.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 47.6875,
            "median": 47.0,
            "std": 14.607584003409553,
            "ci95_low": 43.72708333333333,
            "ci95_high": 51.938541666666666,
            "min": 15.0,
            "max": 82.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3354891468473215,
            "median": 0.32247453310696095,
            "std": 0.10376170360726342,
            "ci95_low": 0.3055957194747958,
            "ci95_high": 0.363671457955918,
            "min": 0.10869565217391304,
            "max": 0.5578231292517006
          }
        },
        "12": {
          "modified_count": {
            "n": 48,
            "mean": 110.89583333333333,
            "median": 110.0,
            "std": 28.728063793189328,
            "ci95_low": 103.02031249999999,
            "ci95_high": 119.7765625,
            "min": 42.0,
            "max": 182.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 32.5625,
            "median": 32.0,
            "std": 11.03008433406865,
            "ci95_low": 29.333333333333332,
            "ci95_high": 35.52135416666667,
            "min": 10.0,
            "max": 58.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 52.666666666666664,
            "median": 52.0,
            "std": 18.134145202413656,
            "ci95_low": 47.33229166666667,
            "ci95_high": 57.95885416666667,
            "min": 17.0,
            "max": 97.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3348142438399973,
            "median": 0.33630952380952384,
            "std": 0.11131842001783247,
            "ci95_low": 0.30206486382201364,
            "ci95_high": 0.3684826441059928,
            "min": 0.11643835616438356,
            "max": 0.5773809523809523
          }
        },
        "14": {
          "modified_count": {
            "n": 48,
            "mean": 138.85416666666666,
            "median": 135.5,
            "std": 38.595114966865374,
            "ci95_low": 127.85104166666667,
            "ci95_high": 149.88072916666667,
            "min": 53.0,
            "max": 236.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 35.479166666666664,
            "median": 35.5,
            "std": 12.677061935068217,
            "ci95_low": 32.0625,
            "ci95_high": 39.022395833333334,
            "min": 14.0,
            "max": 65.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 57.145833333333336,
            "median": 57.0,
            "std": 21.086122592174746,
            "ci95_low": 51.729166666666664,
            "ci95_high": 62.606249999999996,
            "min": 22.0,
            "max": 105.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.33290774816433316,
            "median": 0.34311988844080954,
            "std": 0.12231069341630908,
            "ci95_low": 0.29798164600103594,
            "ci95_high": 0.3672325640343462,
            "min": 0.12790697674418605,
            "max": 0.6104651162790697
          }
        },
        "18": {
          "modified_count": {
            "n": 48,
            "mean": 202.5625,
            "median": 197.5,
            "std": 61.232788823336584,
            "ci95_low": 185.62291666666667,
            "ci95_high": 220.04583333333332,
            "min": 80.0,
            "max": 350.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 40.875,
            "median": 39.5,
            "std": 16.435004563431068,
            "ci95_low": 36.0609375,
            "ci95_high": 45.709375,
            "min": 11.0,
            "max": 78.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 65.5,
            "median": 65.5,
            "std": 25.910905040156354,
            "ci95_low": 58.371875,
            "ci95_high": 73.171875,
            "min": 19.0,
            "max": 122.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3323449094024898,
            "median": 0.3335714285714286,
            "std": 0.12715369581500577,
            "ci95_low": 0.2975330734585149,
            "ci95_high": 0.3673413836441902,
            "min": 0.09090909090909091,
            "max": 0.6022727272727273
          }
        },
        "22": {
          "modified_count": {
            "n": 48,
            "mean": 273.25,
            "median": 271.0,
            "std": 86.79561720885835,
            "ci95_low": 249.04114583333333,
            "ci95_high": 298.89427083333334,
            "min": 106.0,
            "max": 480.0
          },
          "modified_boundary_count": {
            "n": 48,
            "mean": 45.791666666666664,
            "median": 46.0,
            "std": 17.597298956247677,
            "ci95_low": 41.041666666666664,
            "ci95_high": 50.91770833333333,
            "min": 9.0,
            "max": 84.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 48,
            "mean": 73.33333333333333,
            "median": 74.0,
            "std": 28.22183945497214,
            "ci95_low": 65.45833333333333,
            "ci95_high": 81.91927083333333,
            "min": 17.0,
            "max": 138.0
          },
          "frontier_exposed_fraction": {
            "n": 48,
            "mean": 0.3275569121300912,
            "median": 0.33270455489408834,
            "std": 0.12650711020725636,
            "ci95_low": 0.2928155778593804,
            "ci95_high": 0.3638555877380361,
            "min": 0.07555555555555556,
            "max": 0.5879396984924623
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    }
  },
  "status": "MEASURED",
  "bounded_statement": "V5 compares no transmission, equal-budget uniform transmission, and equal-budget surface-biased transmission on material abundance and active-frontier accessibility."
}
```
