# Stage 3 — History-Arm Profiles

```json
{
  "accessible": {
    "groups": 8,
    "probes": 16,
    "G_local": {
      "n": 8,
      "mean": 6.0,
      "sd": 10.05342869728674,
      "se": 3.5544238030134463,
      "ci95_low": 1.125,
      "ci95_high": 13.440624999999997,
      "achieved_mde80_one_sided": 8.837985429842417
    },
    "G_global": {
      "n": 8,
      "mean": 6.0,
      "sd": 10.05342869728674,
      "se": 3.5544238030134463,
      "ci95_low": 0.8421875000000001,
      "ci95_high": 13.157812499999999,
      "achieved_mde80_one_sided": 8.837985429842417
    },
    "E1_ring1": {
      "n": 8,
      "mean": 1.007471382590336,
      "sd": 0.3071563461524181,
      "se": 0.10859616762442867,
      "ci95_low": 0.8038358339889058,
      "ci95_high": 1.174605279227664,
      "achieved_mde80_one_sided": 0.2700216407474341
    },
    "E1_global": {
      "n": 8,
      "mean": 1.007471382590336,
      "sd": 0.3071563461524181,
      "se": 0.10859616762442867,
      "ci95_low": 0.8138037858746476,
      "ci95_high": 1.1860677122614591,
      "achieved_mde80_one_sided": 0.2700216407474341
    },
    "force_material_exposure_ring1": {
      "n": 8,
      "mean": 0.38890872965260115,
      "sd": 0.0534522483824849,
      "se": 0.018898223650461368,
      "ci95_low": 0.3535533905932738,
      "ci95_high": 0.41542523394709674,
      "achieved_mde80_one_sided": 0.046989958015439585
    },
    "prevent_material_exposure_ring1": {
      "n": 8,
      "mean": 0.7446718289370828,
      "sd": 0.17688714622606136,
      "se": 0.0625390503005922,
      "ci95_low": 0.6440748407698405,
      "ci95_high": 0.860736777942781,
      "achieved_mde80_one_sided": 0.15550177637349258
    },
    "G_nonzero_rate": {
      "n": 8,
      "mean": 0.5625,
      "sd": 0.32043497223082784,
      "se": 0.1132908708968707,
      "ci95_low": 0.375,
      "ci95_high": 0.75,
      "achieved_mde80_one_sided": 0.28169490241198286
    },
    "conditional_G_given_nonzero": {
      "n_all": 16,
      "n_nonzero": 9,
      "nonzero_fraction": 0.5625,
      "mean_given_nonzero": 10.666666666666666
    },
    "mean_offset": {
      "n": 8,
      "mean": 0.0025206100951464805,
      "sd": 0.013158525843894686,
      "se": 0.004652241427318185,
      "ci95_low": -0.006306839531219311,
      "ci95_high": 0.010915612264450657,
      "achieved_mde80_one_sided": 0.011567681354116755
    }
  },
  "remote": {
    "groups": 8,
    "probes": 16,
    "G_local": {
      "n": 8,
      "mean": 5.75,
      "sd": 9.942692937888753,
      "se": 3.5152727998183666,
      "ci95_low": 0.8093750000000002,
      "ci95_high": 13.125,
      "achieved_mde80_one_sided": 8.740637444633542
    },
    "G_global": {
      "n": 8,
      "mean": 5.75,
      "sd": 9.942692937888753,
      "se": 3.5152727998183666,
      "ci95_low": 0.875,
      "ci95_high": 12.907812499999999,
      "achieved_mde80_one_sided": 8.740637444633542
    },
    "E1_ring1": {
      "n": 8,
      "mean": 1.031852467498587,
      "sd": 0.3143442520188143,
      "se": 0.11113747611475831,
      "ci95_low": 0.8085387539391743,
      "ci95_high": 1.219857453911004,
      "achieved_mde80_one_sided": 0.276340540421476
    },
    "E1_global": {
      "n": 8,
      "mean": 1.031852467498587,
      "sd": 0.3143442520188143,
      "se": 0.11113747611475831,
      "ci95_low": 0.8310607450563953,
      "ci95_high": 1.2127131025902749,
      "achieved_mde80_one_sided": 0.276340540421476
    },
    "force_material_exposure_ring1": {
      "n": 8,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "prevent_material_exposure_ring1": {
      "n": 8,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "G_nonzero_rate": {
      "n": 8,
      "mean": 0.5,
      "sd": 0.2672612419124244,
      "se": 0.0944911182523068,
      "ci95_low": 0.3125,
      "ci95_high": 0.6875,
      "achieved_mde80_one_sided": 0.23494979007719785
    },
    "conditional_G_given_nonzero": {
      "n_all": 16,
      "n_nonzero": 8,
      "nonzero_fraction": 0.5,
      "mean_given_nonzero": 11.5
    },
    "mean_offset": {
      "n": 8,
      "mean": -0.00492221662477732,
      "sd": 0.01256874227481203,
      "se": 0.0044437214467528095,
      "ci95_low": -0.013874169875778008,
      "ci95_high": 0.0016964903524385724,
      "achieved_mde80_one_sided": 0.011049201664523917
    }
  },
  "erased": {
    "groups": 8,
    "probes": 16,
    "G_local": {
      "n": 8,
      "mean": 5.8125,
      "sd": 9.985480530679103,
      "se": 3.5304004983247195,
      "ci95_low": 1.125,
      "ci95_high": 12.782812499999999,
      "achieved_mde80_one_sided": 8.77825208666718
    },
    "G_global": {
      "n": 8,
      "mean": 5.8125,
      "sd": 9.985480530679103,
      "se": 3.5304004983247195,
      "ci95_low": 0.7171875000000001,
      "ci95_high": 12.535937499999996,
      "achieved_mde80_one_sided": 8.77825208666718
    },
    "E1_ring1": {
      "n": 8,
      "mean": 1.0349484619945606,
      "sd": 0.31523235988547277,
      "se": 0.11145146966222799,
      "ci95_low": 0.8018439735841847,
      "ci95_high": 1.2146152029103143,
      "achieved_mde80_one_sided": 0.2771212774836262
    },
    "E1_global": {
      "n": 8,
      "mean": 1.0349484619945606,
      "sd": 0.31523235988547277,
      "se": 0.11145146966222799,
      "ci95_low": 0.8238417846611424,
      "ci95_high": 1.2091231223764756,
      "achieved_mde80_one_sided": 0.2771212774836262
    },
    "force_material_exposure_ring1": {
      "n": 8,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "prevent_material_exposure_ring1": {
      "n": 8,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "G_nonzero_rate": {
      "n": 8,
      "mean": 0.5,
      "sd": 0.2672612419124244,
      "se": 0.0944911182523068,
      "ci95_low": 0.3125,
      "ci95_high": 0.6875,
      "achieved_mde80_one_sided": 0.23494979007719785
    },
    "conditional_G_given_nonzero": {
      "n_all": 16,
      "n_nonzero": 8,
      "nonzero_fraction": 0.5,
      "mean_given_nonzero": 11.625
    },
    "mean_offset": {
      "n": 8,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    }
  }
}
```
