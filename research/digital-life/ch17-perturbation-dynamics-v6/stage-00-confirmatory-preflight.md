# Stage 0 — Confirmatory CRN Preflight

```json
{
  "role": "CONFIRMATORY PREFLIGHT",
  "sequential_exact": true,
  "crn_exact": true,
  "canonical_substrate_modified": false,
  "preflight_groups_per_runner": 96,
  "omnibus_marginal_feature_test": {
    "energy_distance": 0.10172773061997553,
    "p_value": 0.9220389805097451,
    "null_q95": 0.2010539055337569,
    "gross_mismatch_screen_passed": true
  },
  "practical_equivalence_checks": {
    "population_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -0.0007127500467377229,
      "ci95_low": -0.002972643417995353,
      "ci95_high": 0.0015280935355073174,
      "predeclared_margin": 0.05,
      "passed": true
    },
    "max_radius_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -0.00048828125,
      "ci95_low": -0.00651041666666663,
      "ci95_high": 0.005208333333333315,
      "predeclared_margin": 0.05,
      "passed": true
    },
    "attachment_rate_fraction": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": -1.50123194063434e-07,
      "ci95_low": -6.058232446135881e-07,
      "ci95_high": 2.8117571919455607e-07,
      "predeclared_margin": 0.1,
      "passed": true
    },
    "cov_anisotropy": {
      "n_x": 96,
      "n_y": 96,
      "difference_crn_minus_sequential": 0.0025817919873005607,
      "ci95_low": -0.009326873219986064,
      "ci95_high": 0.014564883026005813,
      "predeclared_margin": 0.1,
      "passed": true
    }
  },
  "all_equivalence_checks_passed": true,
  "preflight_passed": true,
  "interpretation": "Passing is practical compatibility evidence for using the keyed-CRN runner as the declared counterfactual coupling. It is not proof of identical stochastic laws."
}
```
