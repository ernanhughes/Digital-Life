# Stage 1 — How Does Local Inheritance Change Frontier Access?

```json
{
  "groups_per_regime": 40,
  "inheritance_sweep": [
    0.0,
    0.25,
    0.5,
    0.75,
    1.0
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
    "0.0": {
      "inheritance_probability": 0.0,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.2,
            "ci95_high": 22.625625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.125,
            "ci95_high": 22.526874999999997,
            "min": 10.0,
            "max": 34.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.7,
            "median": 36.0,
            "std": 9.368030742904295,
            "ci95_low": 34.824375,
            "ci95_high": 40.75125,
            "min": 21.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.361760715820698,
            "median": 0.3574705111402359,
            "std": 0.08400739267131417,
            "ci95_low": 0.3369356265012413,
            "ci95_high": 0.3878350756013021,
            "min": 0.2,
            "max": 0.5727272727272728
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.174375,
            "ci95_high": 22.65,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 12.55,
            "median": 12.0,
            "std": 3.535180334862707,
            "ci95_low": 11.55,
            "ci95_high": 13.6,
            "min": 6.0,
            "max": 22.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 17.425,
            "median": 17.0,
            "std": 4.6951437677668615,
            "ci95_low": 16.0,
            "ci95_high": 18.875625,
            "min": 8.0,
            "max": 32.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.15807925387286156,
            "median": 0.1581140350877193,
            "std": 0.04018771463351347,
            "ci95_low": 0.14586108092452296,
            "ci95_high": 0.17108158999591302,
            "min": 0.07766990291262135,
            "max": 0.2882882882882883
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.249375,
            "ci95_high": 22.55125,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 6.0,
            "median": 6.0,
            "std": 2.3021728866442674,
            "ci95_low": 5.35,
            "ci95_high": 6.675,
            "min": 1.0,
            "max": 11.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 7.225,
            "median": 7.5,
            "std": 2.919653232834338,
            "ci95_low": 6.399375,
            "ci95_high": 8.1,
            "min": 1.0,
            "max": 13.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.06144386312307568,
            "median": 0.061629589437511303,
            "std": 0.02348192741622716,
            "ci95_low": 0.054133786647006216,
            "ci95_high": 0.06869909130073092,
            "min": 0.008547008547008548,
            "max": 0.1111111111111111
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.175,
            "ci95_high": 22.725625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 2.575,
            "median": 2.0,
            "std": 1.464368464560747,
            "ci95_low": 2.15,
            "ci95_high": 3.0256249999999993,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 2.75,
            "median": 2.0,
            "std": 1.6545392107774297,
            "ci95_low": 2.224375,
            "ci95_high": 3.2256249999999995,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.022189609531411934,
            "median": 0.017869964100518547,
            "std": 0.013123937798737252,
            "ci95_low": 0.01828240536559533,
            "ci95_high": 0.026523672723336677,
            "min": 0.0,
            "max": 0.05
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.125,
            "ci95_high": 22.7,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.675,
            "median": 0.5,
            "std": 0.7870038119348597,
            "ci95_low": 0.45,
            "ci95_high": 0.925,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.7,
            "median": 0.5,
            "std": 0.812403840463596,
            "ci95_low": 0.45,
            "ci95_high": 0.9506249999999994,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0052947804386228505,
            "median": 0.003246753246753247,
            "std": 0.006338867610576577,
            "ci95_low": 0.003356675735024252,
            "ci95_high": 0.00734636667631254,
            "min": 0.0,
            "max": 0.023809523809523808
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.249375,
            "ci95_high": 22.675,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.33071891388307384,
            "ci95_low": 0.025,
            "ci95_high": 0.225,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.33071891388307384,
            "ci95_low": 0.025,
            "ci95_high": 0.225,
            "min": 0.0,
            "max": 1.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0008678277405795392,
            "median": 0.0,
            "std": 0.002299305863681815,
            "ci95_low": 0.0001851851851851852,
            "ci95_high": 0.001721232083979386,
            "min": 0.0,
            "max": 0.007407407407407408
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.15,
            "ci95_high": 22.650624999999998,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.0,
            "ci95_high": 22.525,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.075,
            "ci95_high": 22.425625,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
            "n": 40,
            "mean": 20.875,
            "median": 20.0,
            "std": 5.639980053156217,
            "ci95_low": 19.2,
            "ci95_high": 22.55125,
            "min": 10.0,
            "max": 34.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
    "0.25": {
      "inheritance_probability": 0.25,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.8,
            "median": 20.0,
            "std": 5.3535035257296695,
            "ci95_low": 19.173750000000002,
            "ci95_high": 22.5,
            "min": 12.0,
            "max": 36.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.8,
            "median": 20.0,
            "std": 5.3535035257296695,
            "ci95_low": 19.224375000000002,
            "ci95_high": 22.425625,
            "min": 12.0,
            "max": 36.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.475,
            "median": 38.0,
            "std": 9.24929051333128,
            "ci95_low": 34.874375,
            "ci95_high": 40.525625,
            "min": 22.0,
            "max": 57.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3475478429889579,
            "median": 0.353461738677772,
            "std": 0.06930253674030037,
            "ci95_low": 0.3244936513984902,
            "ci95_high": 0.3693309894342022,
            "min": 0.1896551724137931,
            "max": 0.49019607843137253
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 25.775,
            "median": 24.0,
            "std": 6.582125416611264,
            "ci95_low": 23.575,
            "ci95_high": 27.776874999999997,
            "min": 16.0,
            "max": 43.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 16.55,
            "median": 16.0,
            "std": 4.329838334164452,
            "ci95_low": 15.27375,
            "ci95_high": 18.025624999999998,
            "min": 9.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 24.575,
            "median": 23.0,
            "std": 6.335958885598927,
            "ci95_low": 22.724375000000002,
            "ci95_high": 26.700625,
            "min": 14.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.21689010019043878,
            "median": 0.21588702559576345,
            "std": 0.04728831164968044,
            "ci95_low": 0.2023921054764732,
            "ci95_high": 0.2317782542339687,
            "min": 0.12903225806451613,
            "max": 0.3161764705882353
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 29.225,
            "median": 28.5,
            "std": 7.558066882477291,
            "ci95_low": 26.8,
            "ci95_high": 31.550625,
            "min": 17.0,
            "max": 49.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 10.925,
            "median": 11.0,
            "std": 2.9102190639194156,
            "ci95_low": 10.025,
            "ci95_high": 11.775,
            "min": 5.0,
            "max": 17.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 14.85,
            "median": 14.5,
            "std": 4.2340878592679205,
            "ci95_low": 13.624375,
            "ci95_high": 16.1,
            "min": 6.0,
            "max": 23.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.1256703988873918,
            "median": 0.12784849913562785,
            "std": 0.035408797780417146,
            "ci95_low": 0.1143095238123652,
            "ci95_high": 0.1369484883071072,
            "min": 0.05128205128205128,
            "max": 0.20224719101123595
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 31.675,
            "median": 30.5,
            "std": 7.991831767498613,
            "ci95_low": 29.225,
            "ci95_high": 34.2,
            "min": 19.0,
            "max": 53.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 7.4,
            "median": 7.0,
            "std": 2.4269322199023193,
            "ci95_low": 6.649375,
            "ci95_high": 8.15,
            "min": 3.0,
            "max": 13.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 9.7,
            "median": 9.0,
            "std": 3.6482872693909396,
            "ci95_low": 8.574375,
            "ci95_high": 10.975,
            "min": 2.0,
            "max": 18.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.07751669587087825,
            "median": 0.07200460829493088,
            "std": 0.02769113997997241,
            "ci95_low": 0.06930837799747097,
            "ci95_high": 0.0864758930338925,
            "min": 0.017241379310344827,
            "max": 0.14285714285714285
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 33.45,
            "median": 33.0,
            "std": 8.58181216294088,
            "ci95_low": 30.849375000000002,
            "ci95_high": 36.3,
            "min": 20.0,
            "max": 57.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 4.85,
            "median": 4.0,
            "std": 2.5937424698685874,
            "ci95_low": 4.1743749999999995,
            "ci95_high": 5.650625,
            "min": 1.0,
            "max": 12.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 6.35,
            "median": 5.5,
            "std": 3.8700775186034706,
            "ci95_low": 5.274375,
            "ci95_high": 7.5,
            "min": 1.0,
            "max": 17.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.04814847966514973,
            "median": 0.040884438881935756,
            "std": 0.029057108895310983,
            "ci95_low": 0.039801402935838386,
            "ci95_high": 0.05749318944044632,
            "min": 0.007462686567164179,
            "max": 0.12781954887218044
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 35.1,
            "median": 35.0,
            "std": 9.248783703817491,
            "ci95_low": 32.125,
            "ci95_high": 38.125,
            "min": 20.0,
            "max": 59.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 1.6,
            "median": 1.0,
            "std": 1.7146428199482249,
            "ci95_low": 1.125,
            "ci95_high": 2.15,
            "min": 0.0,
            "max": 7.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 2.1,
            "median": 1.0,
            "std": 2.211334438749598,
            "ci95_low": 1.45,
            "ci95_high": 2.825,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.014396448582310428,
            "median": 0.00766384778012685,
            "std": 0.015304573315389357,
            "ci95_low": 0.009937254190633047,
            "ci95_high": 0.019721341217510194,
            "min": 0.0,
            "max": 0.056338028169014086
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 35.475,
            "median": 35.0,
            "std": 9.646210395797928,
            "ci95_low": 32.499375,
            "ci95_high": 38.302499999999995,
            "min": 20.0,
            "max": 62.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.45,
            "median": 0.0,
            "std": 0.6689544080129827,
            "ci95_low": 0.25,
            "ci95_high": 0.675,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.5,
            "median": 0.0,
            "std": 0.7745966692414834,
            "ci95_low": 0.275,
            "ci95_high": 0.75,
            "min": 0.0,
            "max": 3.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.003048209625534355,
            "median": 0.0,
            "std": 0.004660046047940022,
            "ci95_low": 0.0016934849742615173,
            "ci95_high": 0.004524303871388102,
            "min": 0.0,
            "max": 0.016853932584269662
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.675,
            "ci95_high": 38.675625,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.3992179855667828,
            "ci95_low": 0.025,
            "ci95_high": 0.275,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.125,
            "median": 0.0,
            "std": 0.3992179855667828,
            "ci95_low": 0.025,
            "ci95_high": 0.275,
            "min": 0.0,
            "max": 2.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0007026083227689283,
            "median": 0.0,
            "std": 0.002222963478596978,
            "ci95_low": 0.00012690355329949237,
            "ci95_high": 0.0013979426911898737,
            "min": 0.0,
            "max": 0.010810810810810811
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.59875,
            "ci95_high": 38.55437499999999,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
            "n": 40,
            "mean": 35.575,
            "median": 35.0,
            "std": 9.797671917348529,
            "ci95_low": 32.7,
            "ci95_high": 38.350625,
            "min": 20.0,
            "max": 63.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
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
        "last_observed_step_with_positive_mean_frontier_contact": 14,
        "positive_contact_observed_through_final_step": false
      }
    },
    "0.5": {
      "inheritance_probability": 0.5,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.075,
            "median": 20.0,
            "std": 3.7241609793348083,
            "ci95_low": 18.9,
            "ci95_high": 21.25,
            "min": 13.0,
            "max": 29.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.075,
            "median": 20.0,
            "std": 3.7241609793348083,
            "ci95_low": 19.05,
            "ci95_high": 21.15,
            "min": 13.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.525,
            "median": 37.0,
            "std": 7.338213338408744,
            "ci95_low": 34.175,
            "ci95_high": 38.77625,
            "min": 19.0,
            "max": 51.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3462007510950557,
            "median": 0.35764235764235763,
            "std": 0.0648669700674378,
            "ci95_low": 0.32410848372497125,
            "ci95_high": 0.36604949339973036,
            "min": 0.1919191919191919,
            "max": 0.4434782608695652
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 29.575,
            "median": 30.5,
            "std": 5.826180137963466,
            "ci95_low": 27.649375,
            "ci95_high": 31.47625,
            "min": 16.0,
            "max": 41.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.275,
            "median": 20.0,
            "std": 4.549656580446484,
            "ci95_low": 18.925,
            "ci95_high": 21.650624999999998,
            "min": 10.0,
            "max": 31.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 30.375,
            "median": 31.5,
            "std": 7.488950193451683,
            "ci95_low": 28.19875,
            "ci95_high": 32.7,
            "min": 13.0,
            "max": 44.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.27120995451174457,
            "median": 0.2758130081300813,
            "std": 0.06721460523330179,
            "ci95_low": 0.25090284276689345,
            "ci95_high": 0.2910462576554872,
            "min": 0.11607142857142858,
            "max": 0.4077669902912621
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 37.85,
            "median": 40.0,
            "std": 7.808809128157764,
            "ci95_low": 35.374375,
            "ci95_high": 40.325,
            "min": 19.0,
            "max": 55.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 18.375,
            "median": 18.0,
            "std": 5.829611908180509,
            "ci95_low": 16.624375,
            "ci95_high": 20.2,
            "min": 6.0,
            "max": 35.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 25.825,
            "median": 26.0,
            "std": 7.469563240243702,
            "ci95_low": 23.599375000000002,
            "ci95_high": 28.225,
            "min": 11.0,
            "max": 43.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.21843994026565933,
            "median": 0.21008403361344535,
            "std": 0.0626062192376864,
            "ci95_low": 0.1992858979437625,
            "ci95_high": 0.23682320705156115,
            "min": 0.09166666666666666,
            "max": 0.3706896551724138
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 45.125,
            "median": 47.5,
            "std": 9.836634332941324,
            "ci95_low": 42.15,
            "ci95_high": 47.9,
            "min": 22.0,
            "max": 68.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 15.875,
            "median": 16.0,
            "std": 5.670923646109159,
            "ci95_low": 14.124375,
            "ci95_high": 17.725625,
            "min": 6.0,
            "max": 31.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 21.875,
            "median": 21.0,
            "std": 8.179815095709682,
            "ci95_low": 19.173125000000002,
            "ci95_high": 24.526249999999997,
            "min": 9.0,
            "max": 41.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.17674697099027975,
            "median": 0.16613508442776737,
            "std": 0.06743808991847347,
            "ci95_low": 0.15614938548797058,
            "ci95_high": 0.1981276873354824,
            "min": 0.07874015748031496,
            "max": 0.33064516129032256
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 51.4,
            "median": 54.5,
            "std": 11.410083259994206,
            "ci95_low": 47.84875,
            "ci95_high": 54.975,
            "min": 27.0,
            "max": 79.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 14.225,
            "median": 14.0,
            "std": 5.565462694152212,
            "ci95_low": 12.55,
            "ci95_high": 16.05,
            "min": 4.0,
            "max": 26.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 18.6,
            "median": 18.5,
            "std": 7.611832893594027,
            "ci95_low": 16.324375,
            "ci95_high": 20.92625,
            "min": 5.0,
            "max": 33.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.1432114382157458,
            "median": 0.13194205885720828,
            "std": 0.060111768632458415,
            "ci95_low": 0.12550232666024388,
            "ci95_high": 0.1598471583686987,
            "min": 0.03875968992248062,
            "max": 0.25984251968503935
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 60.675,
            "median": 63.5,
            "std": 14.455773068224333,
            "ci95_low": 56.52375,
            "ci95_high": 65.375625,
            "min": 29.0,
            "max": 94.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 9.725,
            "median": 9.0,
            "std": 5.044737356889851,
            "ci95_low": 8.199375,
            "ci95_high": 11.425,
            "min": 1.0,
            "max": 19.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 12.65,
            "median": 12.0,
            "std": 6.941001368678729,
            "ci95_low": 10.42375,
            "ci95_high": 14.925,
            "min": 2.0,
            "max": 24.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.0895245912099216,
            "median": 0.0871309443317557,
            "std": 0.05039136769357663,
            "ci95_low": 0.07341023389167922,
            "ci95_high": 0.10430521643988283,
            "min": 0.013513513513513514,
            "max": 0.17518248175182483
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 66.85,
            "median": 67.5,
            "std": 17.355906775504415,
            "ci95_low": 61.5,
            "ci95_high": 72.125625,
            "min": 31.0,
            "max": 102.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 6.3,
            "median": 5.0,
            "std": 4.1844951905815355,
            "ci95_low": 5.0,
            "ci95_high": 7.675,
            "min": 0.0,
            "max": 17.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 8.9,
            "median": 7.0,
            "std": 5.847221562417487,
            "ci95_low": 7.074375,
            "ci95_high": 10.75,
            "min": 0.0,
            "max": 22.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.05802481262704477,
            "median": 0.046052631578947366,
            "std": 0.03834306532434202,
            "ci95_low": 0.04684894956123461,
            "ci95_high": 0.07024177991473286,
            "min": 0.0,
            "max": 0.14666666666666667
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 71.35,
            "median": 70.0,
            "std": 19.79715888707266,
            "ci95_low": 65.0975,
            "ci95_high": 77.575,
            "min": 32.0,
            "max": 108.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 4.15,
            "median": 4.0,
            "std": 2.9372606285449034,
            "ci95_low": 3.225,
            "ci95_high": 5.050624999999999,
            "min": 0.0,
            "max": 10.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 5.825,
            "median": 4.5,
            "std": 4.247867111857432,
            "ci95_low": 4.5493749999999995,
            "ci95_high": 7.150625,
            "min": 0.0,
            "max": 14.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.034138697552143646,
            "median": 0.028853344412131283,
            "std": 0.02450950314556512,
            "ci95_low": 0.026158899862608442,
            "ci95_high": 0.04182495684613217,
            "min": 0.0,
            "max": 0.08139534883720931
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 75.975,
            "median": 78.0,
            "std": 22.033483042860016,
            "ci95_low": 68.99875,
            "ci95_high": 82.925625,
            "min": 34.0,
            "max": 119.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 1.25,
            "median": 0.5,
            "std": 1.7571283390805579,
            "ci95_low": 0.725,
            "ci95_high": 1.825,
            "min": 0.0,
            "max": 6.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 1.4,
            "median": 0.5,
            "std": 2.1071307505705477,
            "ci95_low": 0.775,
            "ci95_high": 2.05,
            "min": 0.0,
            "max": 8.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.007166952885266411,
            "median": 0.0024271844660194173,
            "std": 0.010739223817368427,
            "ci95_low": 0.004013807475842895,
            "ci95_high": 0.01060018094782162,
            "min": 0.0,
            "max": 0.043010752688172046
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 76.975,
            "median": 78.0,
            "std": 22.73817000112366,
            "ci95_low": 69.52187500000001,
            "ci95_high": 83.92625,
            "min": 34.0,
            "max": 123.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 0.425,
            "median": 0.0,
            "std": 0.9457140159688869,
            "ci95_low": 0.17437500000000003,
            "ci95_high": 0.7256249999999994,
            "min": 0.0,
            "max": 4.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 0.6,
            "median": 0.0,
            "std": 1.3564659966250536,
            "ci95_low": 0.22437500000000005,
            "ci95_high": 1.025,
            "min": 0.0,
            "max": 5.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.002646748542028629,
            "median": 0.0,
            "std": 0.0059569890393780175,
            "ci95_low": 0.0009075667307714587,
            "ci95_high": 0.004594108870338635,
            "min": 0.0,
            "max": 0.02127659574468085
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "0.75": {
      "inheritance_probability": 0.75,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 20.0,
            "median": 19.0,
            "std": 5.371219600798314,
            "ci95_low": 18.225,
            "ci95_high": 21.8,
            "min": 10.0,
            "max": 30.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 20.0,
            "median": 19.0,
            "std": 5.371219600798314,
            "ci95_low": 18.375,
            "ci95_high": 21.675,
            "min": 10.0,
            "max": 30.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.85,
            "median": 37.0,
            "std": 10.011368537817395,
            "ci95_low": 33.85,
            "ci95_high": 39.825625,
            "min": 19.0,
            "max": 64.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.34738285078540515,
            "median": 0.354502688172043,
            "std": 0.07316301905555381,
            "ci95_low": 0.3244745186281786,
            "ci95_high": 0.3691423194669471,
            "min": 0.21839080459770116,
            "max": 0.5039370078740157
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 34.625,
            "median": 33.0,
            "std": 10.221759877829257,
            "ci95_low": 31.274375,
            "ci95_high": 37.9,
            "min": 15.0,
            "max": 60.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 24.575,
            "median": 25.0,
            "std": 7.422558521156974,
            "ci95_low": 22.374375,
            "ci95_high": 26.925625,
            "min": 14.0,
            "max": 44.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.8,
            "median": 37.0,
            "std": 11.238772174930853,
            "ci95_low": 34.375,
            "ci95_high": 41.45,
            "min": 23.0,
            "max": 65.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.33424643576514657,
            "median": 0.32366946778711486,
            "std": 0.0818358580385646,
            "ci95_low": 0.3096100258706744,
            "ci95_high": 0.3610951551406001,
            "min": 0.20175438596491227,
            "max": 0.52
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 49.625,
            "median": 48.0,
            "std": 14.848716274479758,
            "ci95_low": 45.175,
            "ci95_high": 54.251875,
            "min": 25.0,
            "max": 91.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.125,
            "median": 26.5,
            "std": 9.423872611617796,
            "ci95_low": 25.249375,
            "ci95_high": 30.92625,
            "min": 14.0,
            "max": 54.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 38.5,
            "median": 36.0,
            "std": 12.216791722870616,
            "ci95_low": 34.899375,
            "ci95_high": 42.501875,
            "min": 19.0,
            "max": 67.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.31901027612690436,
            "median": 0.3170712729536259,
            "std": 0.08541925063394994,
            "ci95_low": 0.2909404382831104,
            "ci95_high": 0.34598615412957,
            "min": 0.17272727272727273,
            "max": 0.5275590551181102
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 65.175,
            "median": 62.0,
            "std": 18.100949560727468,
            "ci95_low": 59.774375,
            "ci95_high": 70.725,
            "min": 36.0,
            "max": 109.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.95,
            "median": 27.0,
            "std": 9.211270270706423,
            "ci95_low": 26.298750000000002,
            "ci95_high": 32.100625,
            "min": 14.0,
            "max": 54.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 37.475,
            "median": 35.0,
            "std": 11.48039089055769,
            "ci95_low": 34.249375,
            "ci95_high": 41.300625,
            "min": 19.0,
            "max": 71.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3003617875609548,
            "median": 0.2898134354827268,
            "std": 0.08480429042329078,
            "ci95_low": 0.2751931645017873,
            "ci95_high": 0.3258541697609168,
            "min": 0.16101694915254236,
            "max": 0.5867768595041323
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 80.725,
            "median": 76.5,
            "std": 22.770581349627417,
            "ci95_low": 74.19875,
            "ci95_high": 88.275,
            "min": 45.0,
            "max": 138.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 29.0,
            "median": 26.5,
            "std": 9.818350166906862,
            "ci95_low": 26.075,
            "ci95_high": 32.550625,
            "min": 15.0,
            "max": 59.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 36.875,
            "median": 33.0,
            "std": 12.215128939147553,
            "ci95_low": 33.424375,
            "ci95_high": 40.62625,
            "min": 18.0,
            "max": 78.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2818112448020319,
            "median": 0.26072337331879314,
            "std": 0.09216462918301724,
            "ci95_low": 0.2551908939580435,
            "ci95_high": 0.31332006444297594,
            "min": 0.13768115942028986,
            "max": 0.6290322580645161
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 111.2,
            "median": 105.5,
            "std": 31.928983698201232,
            "ci95_low": 101.6,
            "ci95_high": 121.829375,
            "min": 62.0,
            "max": 182.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 28.825,
            "median": 26.0,
            "std": 10.384814634840623,
            "ci95_low": 25.473750000000003,
            "ci95_high": 32.100625,
            "min": 12.0,
            "max": 55.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 35.575,
            "median": 32.0,
            "std": 12.90326993440035,
            "ci95_low": 31.849375000000002,
            "ci95_high": 39.625,
            "min": 14.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2483835640520417,
            "median": 0.22428571428571428,
            "std": 0.08934520381401347,
            "ci95_low": 0.22103871482570983,
            "ci95_high": 0.2774281149529019,
            "min": 0.08333333333333333,
            "max": 0.4632352941176471
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 139.075,
            "median": 131.0,
            "std": 42.128605186974795,
            "ci95_low": 126.4,
            "ci95_high": 152.23,
            "min": 75.0,
            "max": 240.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 26.125,
            "median": 25.0,
            "std": 11.106726565464731,
            "ci95_low": 22.675,
            "ci95_high": 29.775,
            "min": 6.0,
            "max": 48.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 32.775,
            "median": 30.5,
            "std": 13.374392509568425,
            "ci95_low": 28.725,
            "ci95_high": 37.300625,
            "min": 7.0,
            "max": 61.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.2111649760664962,
            "median": 0.19535465192788526,
            "std": 0.08866085715589539,
            "ci95_low": 0.1845433745230467,
            "ci95_high": 0.23869950356023417,
            "min": 0.051094890510948905,
            "max": 0.44696969696969696
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 165.3,
            "median": 157.0,
            "std": 50.35583382290477,
            "ci95_low": 150.574375,
            "ci95_high": 181.156875,
            "min": 91.0,
            "max": 286.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 24.65,
            "median": 22.5,
            "std": 10.460760010630201,
            "ci95_low": 21.524375,
            "ci95_high": 27.675625,
            "min": 3.0,
            "max": 47.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 29.55,
            "median": 25.5,
            "std": 12.391428489080667,
            "ci95_low": 25.749375,
            "ci95_high": 33.450625,
            "min": 4.0,
            "max": 60.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.17587378773939083,
            "median": 0.15350347327091513,
            "std": 0.07742017801051847,
            "ci95_low": 0.1521652053012979,
            "ci95_high": 0.201869193387911,
            "min": 0.026143790849673203,
            "max": 0.39473684210526316
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 214.925,
            "median": 201.0,
            "std": 69.01282036694342,
            "ci95_low": 194.773125,
            "ci95_high": 239.2275,
            "min": 109.0,
            "max": 399.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 21.3,
            "median": 19.0,
            "std": 11.303096920755832,
            "ci95_low": 18.125,
            "ci95_high": 24.825,
            "min": 5.0,
            "max": 59.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 26.2,
            "median": 23.5,
            "std": 12.649505919204907,
            "ci95_low": 22.3725,
            "ci95_high": 29.903749999999995,
            "min": 7.0,
            "max": 70.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.13379520043206433,
            "median": 0.11618544600938968,
            "std": 0.06521415829667544,
            "ci95_low": 0.11483147419005031,
            "ci95_high": 0.15448703686159068,
            "min": 0.03825136612021858,
            "max": 0.37433155080213903
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 255.675,
            "median": 241.0,
            "std": 83.10216227632107,
            "ci95_low": 231.08625,
            "ci95_high": 281.010625,
            "min": 123.0,
            "max": 493.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 17.6,
            "median": 17.0,
            "std": 8.952094726934027,
            "ci95_low": 14.87375,
            "ci95_high": 20.525,
            "min": 3.0,
            "max": 39.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 21.725,
            "median": 22.0,
            "std": 10.693426719251411,
            "ci95_low": 18.474375000000002,
            "ci95_high": 24.975,
            "min": 4.0,
            "max": 48.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.09678742363362122,
            "median": 0.09913056978730012,
            "std": 0.04790244584915415,
            "ci95_low": 0.08375106406869474,
            "ci95_high": 0.11167717980766638,
            "min": 0.01680672268907563,
            "max": 0.2191780821917808
          }
        }
      },
      "lifetime": {
        "last_observed_step_with_positive_mean_frontier_contact": 22,
        "positive_contact_observed_through_final_step": true
      }
    },
    "1.0": {
      "inheritance_probability": 1.0,
      "summary": {
        "4": {
          "modified_count": {
            "n": 40,
            "mean": 19.775,
            "median": 21.0,
            "std": 3.9842659298796814,
            "ci95_low": 18.599375000000002,
            "ci95_high": 20.925625,
            "min": 12.0,
            "max": 29.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 19.775,
            "median": 21.0,
            "std": 3.9842659298796814,
            "ci95_low": 18.574375,
            "ci95_high": 20.975625,
            "min": 12.0,
            "max": 29.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 34.875,
            "median": 35.0,
            "std": 7.057575716915831,
            "ci95_low": 32.65,
            "ci95_high": 36.900625,
            "min": 19.0,
            "max": 49.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3352281348476909,
            "median": 0.32868672046955244,
            "std": 0.06808161006518071,
            "ci95_low": 0.3143707390500136,
            "ci95_high": 0.35648375846590796,
            "min": 0.19791666666666666,
            "max": 0.47
          }
        },
        "5": {
          "modified_count": {
            "n": 40,
            "mean": 38.65,
            "median": 38.0,
            "std": 7.564885987243958,
            "ci95_low": 36.324375,
            "ci95_high": 40.925625,
            "min": 24.0,
            "max": 55.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 27.325,
            "median": 27.0,
            "std": 5.845457638200794,
            "ci95_low": 25.525,
            "ci95_high": 29.225,
            "min": 15.0,
            "max": 41.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 41.0,
            "median": 40.0,
            "std": 9.31933474020544,
            "ci95_low": 38.1,
            "ci95_high": 43.7,
            "min": 21.0,
            "max": 63.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.3730098582001807,
            "median": 0.37226071543667416,
            "std": 0.08315494736944008,
            "ci95_low": 0.3471577281626002,
            "ci95_high": 0.39934280030877545,
            "min": 0.20192307692307693,
            "max": 0.5431034482758621
          }
        },
        "6": {
          "modified_count": {
            "n": 40,
            "mean": 61.125,
            "median": 60.0,
            "std": 12.225357867972617,
            "ci95_low": 57.024375,
            "ci95_high": 64.95,
            "min": 34.0,
            "max": 90.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 35.45,
            "median": 35.5,
            "std": 9.148633777783434,
            "ci95_low": 32.774375,
            "ci95_high": 38.250625,
            "min": 16.0,
            "max": 56.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 46.85,
            "median": 47.0,
            "std": 11.678077752781062,
            "ci95_low": 43.324375,
            "ci95_high": 50.4,
            "min": 23.0,
            "max": 72.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4036352485798368,
            "median": 0.4105263157894737,
            "std": 0.09902371146485782,
            "ci95_low": 0.37083439925280554,
            "ci95_high": 0.43282103890830637,
            "min": 0.20175438596491227,
            "max": 0.5849056603773585
          }
        },
        "7": {
          "modified_count": {
            "n": 40,
            "mean": 87.3,
            "median": 86.0,
            "std": 18.9,
            "ci95_low": 81.65,
            "ci95_high": 92.925625,
            "min": 44.0,
            "max": 132.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 43.275,
            "median": 42.0,
            "std": 11.063425102562045,
            "ci95_low": 39.924375,
            "ci95_high": 46.900625,
            "min": 22.0,
            "max": 68.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 53.0,
            "median": 52.5,
            "std": 13.171939872319491,
            "ci95_low": 49.123125,
            "ci95_high": 56.9,
            "min": 24.0,
            "max": 81.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4324343496013679,
            "median": 0.436309177136201,
            "std": 0.10645914799279534,
            "ci95_low": 0.39928619039695507,
            "ci95_high": 0.465158914888891,
            "min": 0.20512820512820512,
            "max": 0.6136363636363636
          }
        },
        "8": {
          "modified_count": {
            "n": 40,
            "mean": 116.25,
            "median": 115.0,
            "std": 24.89251895650579,
            "ci95_low": 109.02312500000001,
            "ci95_high": 123.900625,
            "min": 63.0,
            "max": 173.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 48.975,
            "median": 48.0,
            "std": 12.616432736712863,
            "ci95_low": 45.074375,
            "ci95_high": 52.65125,
            "min": 16.0,
            "max": 73.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 57.625,
            "median": 60.0,
            "std": 14.669164086613797,
            "ci95_low": 53.17375,
            "ci95_high": 62.203125,
            "min": 21.0,
            "max": 88.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.4491073182293935,
            "median": 0.4439408396946565,
            "std": 0.1149146683386463,
            "ci95_low": 0.41237876433028514,
            "ci95_high": 0.4860119503741235,
            "min": 0.1640625,
            "max": 0.676923076923077
          }
        },
        "10": {
          "modified_count": {
            "n": 40,
            "mean": 183.1,
            "median": 182.0,
            "std": 39.51695838497695,
            "ci95_low": 170.44062499999998,
            "ci95_high": 195.12687499999998,
            "min": 93.0,
            "max": 266.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 61.45,
            "median": 60.0,
            "std": 17.804423607631897,
            "ci95_low": 56.14875,
            "ci95_high": 66.825,
            "min": 16.0,
            "max": 95.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 68.925,
            "median": 67.5,
            "std": 19.176010403626716,
            "ci95_low": 63.09875,
            "ci95_high": 75.07625,
            "min": 16.0,
            "max": 106.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.48551001136753624,
            "median": 0.48343143666884675,
            "std": 0.1367362671977677,
            "ci95_low": 0.44158551581761785,
            "ci95_high": 0.5249913887107337,
            "min": 0.11940298507462686,
            "max": 0.7464788732394366
          }
        },
        "12": {
          "modified_count": {
            "n": 40,
            "mean": 261.975,
            "median": 262.0,
            "std": 58.82367189320979,
            "ci95_low": 244.77125,
            "ci95_high": 279.055,
            "min": 115.0,
            "max": 385.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 71.6,
            "median": 72.5,
            "std": 20.003499693803583,
            "ci95_low": 65.274375,
            "ci95_high": 77.35,
            "min": 20.0,
            "max": 116.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 78.65,
            "median": 79.0,
            "std": 21.00660610379506,
            "ci95_low": 72.49875,
            "ci95_high": 84.925625,
            "min": 24.0,
            "max": 126.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5124198128725554,
            "median": 0.5047985438901299,
            "std": 0.1373058283619192,
            "ci95_low": 0.46845254128184227,
            "ci95_high": 0.5531473364298962,
            "min": 0.16326530612244897,
            "max": 0.7682926829268293
          }
        },
        "14": {
          "modified_count": {
            "n": 40,
            "mean": 349.1,
            "median": 353.0,
            "std": 80.18254174070563,
            "ci95_low": 322.59062500000005,
            "ci95_high": 374.051875,
            "min": 144.0,
            "max": 510.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 81.5,
            "median": 80.5,
            "std": 21.243822631532208,
            "ci95_low": 75.573125,
            "ci95_high": 87.7,
            "min": 26.0,
            "max": 116.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 87.975,
            "median": 86.5,
            "std": 22.60031802873579,
            "ci95_low": 80.47375,
            "ci95_high": 94.9525,
            "min": 30.0,
            "max": 128.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5336078729441771,
            "median": 0.5300290603810138,
            "std": 0.14407293974385085,
            "ci95_low": 0.48456661052369976,
            "ci95_high": 0.5773624601221421,
            "min": 0.17857142857142858,
            "max": 0.8311688311688312
          }
        },
        "18": {
          "modified_count": {
            "n": 40,
            "mean": 556.225,
            "median": 547.0,
            "std": 133.3177571631026,
            "ci95_low": 516.198125,
            "ci95_high": 594.953125,
            "min": 228.0,
            "max": 847.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 102.775,
            "median": 104.0,
            "std": 30.103560835887837,
            "ci95_low": 93.97375,
            "ci95_high": 112.08,
            "min": 40.0,
            "max": 178.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 107.475,
            "median": 108.0,
            "std": 29.512698538086955,
            "ci95_low": 98.424375,
            "ci95_high": 116.878125,
            "min": 45.0,
            "max": 182.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.567828959215826,
            "median": 0.5651022188980304,
            "std": 0.15251645916943082,
            "ci95_low": 0.5194345328601087,
            "ci95_high": 0.6151274989619901,
            "min": 0.25280898876404495,
            "max": 0.9191919191919192
          }
        },
        "22": {
          "modified_count": {
            "n": 40,
            "mean": 808.175,
            "median": 815.0,
            "std": 198.6749716874272,
            "ci95_low": 744.738125,
            "ci95_high": 867.284375,
            "min": 342.0,
            "max": 1294.0
          },
          "modified_boundary_count": {
            "n": 40,
            "mean": 123.375,
            "median": 123.5,
            "std": 34.63862547792565,
            "ci95_low": 113.07000000000001,
            "ci95_high": 134.05375,
            "min": 49.0,
            "max": 215.0
          },
          "frontier_cells_with_modified_neighbor": {
            "n": 40,
            "mean": 128.6,
            "median": 128.5,
            "std": 35.12890547682919,
            "ci95_low": 118.29875,
            "ci95_high": 139.003125,
            "min": 51.0,
            "max": 208.0
          },
          "frontier_exposed_fraction": {
            "n": 40,
            "mean": 0.5912980276425659,
            "median": 0.5883720930232559,
            "std": 0.1626868518167941,
            "ci95_low": 0.54210978661474,
            "ci95_high": 0.6386885644476149,
            "min": 0.2361111111111111,
            "max": 0.9327354260089686
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
  "bounded_statement": "The inheritance sweep characterizes how local propagation changes material abundance and contact with the active growth surface. It is not used to optimize or select a significance result."
}
```
