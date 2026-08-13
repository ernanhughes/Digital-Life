# Stage 4 — Realized Divergence and Conditional Cascade

```json
{
  "H3_realized_lag1_divergence": {
    "high_absolute": {
      "n": 281,
      "mean": 0.2117437722419929,
      "sd": 0.3500205265887947,
      "se": 0.02088047403314264,
      "ci95_low": 0.1711150652431791,
      "ci95_high": 0.2529655990510083,
      "half_width": 0.0409252669039146,
      "achieved_mde80_one_sided": 0.051918773759241414
    },
    "low_absolute": {
      "n": 281,
      "mean": 0.2057532621589561,
      "sd": 0.35825790459471807,
      "se": 0.02137187480677764,
      "ci95_low": 0.16512158956109135,
      "ci95_high": 0.24899317912218266,
      "half_width": 0.041935794780545654,
      "achieved_mde80_one_sided": 0.053140629429327076
    },
    "high_minus_low": {
      "n": 281,
      "mean": 0.005990510083036775,
      "sd": 0.5084257307799672,
      "se": 0.03033013627170669,
      "ci95_low": -0.05272835112692764,
      "ci95_high": 0.06583778173190982,
      "half_width": 0.05928306642941873,
      "achieved_mde80_one_sided": 0.07541512135587752
    },
    "SEI": 0.05,
    "signflip": {
      "n": 281,
      "observed_mean": 0.005990510083036775,
      "p_value": 0.4153292335383231,
      "permutations": 20000
    },
    "status": "UNRESOLVED"
  },
  "H4_nonzero_transient_rate": {
    "high_absolute": {
      "n": 281,
      "mean": 0.20551601423487545,
      "sd": 0.3458917343697689,
      "se": 0.02063417093898471,
      "ci95_low": 0.16548042704626334,
      "ci95_high": 0.24704181494661906,
      "half_width": 0.04078069395017786,
      "achieved_mde80_one_sided": 0.05130634730754835
    },
    "low_absolute": {
      "n": 281,
      "mean": 0.19217081850533807,
      "sd": 0.3568935538953677,
      "se": 0.021290484467680892,
      "ci95_low": 0.15154211150652433,
      "ci95_high": 0.23398576512455516,
      "half_width": 0.04122182680901541,
      "achieved_mde80_one_sided": 0.05293825439727346
    },
    "high_minus_low": {
      "n": 281,
      "mean": 0.013345195729537363,
      "sd": 0.5041935646678086,
      "se": 0.03007766640809583,
      "ci95_low": -0.045966785290628705,
      "ci95_high": 0.07087781731909845,
      "half_width": 0.058422301304863575,
      "achieved_mde80_one_sided": 0.07478736138696909
    },
    "SEI": 0.05,
    "signflip": {
      "n": 281,
      "observed_mean": 0.013345195729537363,
      "p_value": 0.32523373831308433,
      "permutations": 20000
    },
    "status": "UNRESOLVED"
  },
  "conditional_transient_magnitude": {
    "high": {
      "n": 467,
      "nonzero_n": 99,
      "nonzero_fraction": 0.21199143468950749,
      "mean_all": 0.3468950749464668,
      "mean_given_nonzero": 1.6363636363636365
    },
    "low": {
      "n": 467,
      "nonzero_n": 84,
      "nonzero_fraction": 0.17987152034261242,
      "mean_all": 0.11563169164882227,
      "mean_given_nonzero": 0.6428571428571429
    },
    "difference_of_raw_conditional_means": 0.9935064935064936,
    "scope": "Descriptive mechanism decomposition; no directional claim frozen."
  }
}
```
