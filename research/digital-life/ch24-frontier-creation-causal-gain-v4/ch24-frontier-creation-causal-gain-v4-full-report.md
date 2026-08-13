# Chapter 24 — Frontier Creation, Divergence, and Causal Gain (V4)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-frontier-creation-causal-gain-v4-reset",
  "schema_version": 4,
  "chapter": 24,
  "chapter_title": "Where Is Causal Gain Created?",
  "run_title": "Frontier Creation, Divergence, and Causal Gain \u2014 Reset Experiment",
  "profile": "full",
  "profile_config": {
    "groups": 384,
    "radius": 110,
    "warmup_steps": 24,
    "lossy_pre_steps": 28,
    "horizon": 12,
    "loss_rate": 0.08,
    "budget": 96,
    "radial_bin_width": 4,
    "high_fcp_min": 2,
    "low_fcp_max": -1,
    "minimum_fcp_difference": 3,
    "minimum_group_coverage_fraction": 0.5,
    "max_pairs_per_group": 10,
    "sei_E1": 0.1,
    "sei_g1": 0.1,
    "sei_divergence_probability": 0.05,
    "sei_GT": 0.15,
    "bootstrap_reps": 7000,
    "signflip_permutations": 20000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "mode": "run",
  "seed": 20260909,
  "previous_ch24_seeds": [
    20260906,
    20260907,
    20260908
  ],
  "fresh_seed": true,
  "classifier_used": false,
  "canonical_rules_modified": false,
  "started_at_unix": 1786608375.9155962,
  "finished_at_unix": 1786608487.470432,
  "final_status": "EXTREME_FCP_EXPECTED_EFFECT_BOUNDED_BELOW_SEI"
}
```

---

## Stage 0 — Frozen Chapter 24 V4 Reset Protocol

```json
{
  "experiment_version": "digital-crystal-frontier-creation-causal-gain-v4-reset",
  "role": "RESET EXTREME-FCP CAUSAL MECHANISM TEST",
  "seed": 20260909,
  "mode": "run",
  "exposure": {
    "high": "FCP >= 2",
    "low": "FCP <= -1",
    "minimum_delta_FCP": 3,
    "FCP_identity": "FCP = promoted_frontier - 1",
    "promotion_status": "implementation invariant, not independent evidence"
  },
  "pairing": {
    "same_occupied_neighbor_count": true,
    "same_radial_bin_width": 4,
    "baseline_p_matched": false,
    "frontier_density_matched": false,
    "reason": "baseline p and density may lie on or summarize the geometry pathway; V4 estimates the total extreme-geometry contrast"
  },
  "H1_primary": {
    "outcome": "Delta exact E1_local",
    "SEI": 0.1,
    "status_space": [
      "SUPPORTED",
      "BOUNDED_BELOW_SEI",
      "UNRESOLVED",
      "INVALID"
    ],
    "precision_gate": "achieved one-sided 80% MDE must be <= SEI"
  },
  "H2_secondary": {
    "outcome": "Delta realized g1_local",
    "SEI": 0.1
  },
  "H3_mechanism": {
    "outcome": "Delta model-implied P(any lag1 local divergence)",
    "SEI": 0.05
  },
  "H4_downstream": {
    "outcome": "Delta G_T(H)",
    "SEI": 0.15
  },
  "zero_inflation_decomposition": [
    "P(lag1 realized divergence)",
    "P(G_T != 0)",
    "E[G_T | G_T != 0]"
  ],
  "support_gate": {
    "minimum_group_coverage_fraction": 0.5,
    "no_automatic_weaker_contrast": true,
    "design_audit_provenance": "Frozen at 0.50 after outcome-blind 48-group seed-20260909 support audit found 0.5417 coverage for exact Delta-FCP=3. No V4 causal outcomes were inspected."
  },
  "horizon": 12,
  "classifier_used": false,
  "scientific": true,
  "status": "FROZEN"
}
```

---

## Stage 1 — Extreme-FCP Design Support Audit

```json
{
  "requested_groups": 384,
  "groups_with_extreme_pairs": 275,
  "coverage_fraction": 0.7161458333333334,
  "minimum_coverage_fraction": 0.5,
  "coverage_gate_passed": true,
  "total_evaluated_usable_sites": 36864,
  "FCP_site_counts": {
    "-1": 23996,
    "0": 5261,
    "1": 4058,
    "2": 3549
  },
  "total_extreme_pairs": 471,
  "pair_count_distribution": {
    "min": 0,
    "median": 1.0,
    "max": 4
  },
  "achieved_pair_delta_FCP": {
    "mean": 3.0,
    "min": 3,
    "max": 3
  },
  "unmatched_possible_mediator_diagnostics": {
    "baseline_p_high_minus_low_mean": 6.116833861788283e-17,
    "frontier_density_high_minus_low_mean": -0.22672924349089285
  },
  "note": "No causal outcome data are used in this stage. No weaker FCP contrast is substituted if coverage fails."
}
```

---

## Stage 2 — Extreme-FCP Transient Interventions

```json
{
  "total_pairs_run": 471,
  "maximum_capacity_fraction": 0.023559280390925717,
  "capacity_gate_passed": true
}
```

---

## Stage 3 — Precision-Aware Causal Analysis

```json
{
  "H1_primary_exact_expected_lag1_gain": {
    "sei": 0.1,
    "summary": {
      "n": 275,
      "mean": -0.002580487051053025,
      "sd": 0.3115915739447761,
      "se": 0.01878967888383822,
      "ci95_low": -0.0395016984122971,
      "ci95_high": 0.03327085181727841,
      "half_width": 0.03638627511478776,
      "achieved_mde80_one_sided": 0.04672006418198964
    },
    "signflip_greater": {
      "n": 275,
      "observed_mean": -0.002580487051053025,
      "p_value": 0.5549722513874307,
      "permutations": 20000
    },
    "status": "BOUNDED_BELOW_SEI"
  },
  "H2_realized_lag1_gain": {
    "sei": 0.1,
    "summary": {
      "n": 275,
      "mean": -0.028181818181818176,
      "sd": 0.5423458471458873,
      "se": 0.03270468511982454,
      "ci95_low": -0.09242424242424241,
      "ci95_high": 0.03515151515151515,
      "half_width": 0.06378787878787878,
      "achieved_mde80_one_sided": 0.0813193773718097
    },
    "signflip_greater": {
      "n": 275,
      "observed_mean": -0.028181818181818176,
      "p_value": 0.8084595770211489,
      "permutations": 20000
    },
    "status": "BOUNDED_BELOW_SEI"
  },
  "H3_model_implied_lag1_divergence_probability": {
    "sei": 0.05,
    "summary": {
      "n": 275,
      "mean": 0.04981839455556556,
      "sd": 0.29083334328012184,
      "se": 0.017537910476087163,
      "ci95_low": 0.015929152658155924,
      "ci95_high": 0.08414020015922713,
      "half_width": 0.034105523750535605,
      "achieved_mde80_one_sided": 0.043607573504918
    },
    "signflip_greater": {
      "n": 275,
      "observed_mean": 0.04981839455556556,
      "p_value": 0.0031998400079996,
      "permutations": 20000
    },
    "status": "UNRESOLVED"
  },
  "H4_finite_horizon_transient_gain": {
    "sei": 0.15,
    "summary": {
      "n": 275,
      "mean": 0.059090909090909076,
      "sd": 1.3904538481045023,
      "se": 0.0838475218630628,
      "ci95_low": -0.10484848484848484,
      "ci95_high": 0.22424999999999992,
      "half_width": 0.16454924242424238,
      "achieved_mde80_one_sided": 0.2084847552297745
    },
    "signflip_greater": {
      "n": 275,
      "observed_mean": 0.059090909090909076,
      "p_value": 0.2382880855957202,
      "permutations": 20000
    },
    "status": "UNRESOLVED"
  }
}
```

---

## Stage 4 — Divergence, Zero Inflation, and Budget Diagnostics

```json
{
  "zero_inflation": {
    "high": {
      "lag1_realized_divergence_rate": {
        "n": 275,
        "mean": 0.2103030303030303,
        "sd": 0.3573536785203372,
        "se": 0.021549237620095352,
        "ci95_low": 0.16969696969696968,
        "ci95_high": 0.25334090909090895,
        "half_width": 0.041821969696969635,
        "achieved_mde80_one_sided": 0.05358163760583345
      },
      "GT_nonzero_rate": {
        "n": 275,
        "mean": 0.22121212121212122,
        "sd": 0.3524830031256014,
        "se": 0.021255524842641624,
        "ci95_low": 0.18060606060606063,
        "ci95_high": 0.2642424242424242,
        "half_width": 0.041818181818181796,
        "achieved_mde80_one_sided": 0.05285132816847996
      },
      "GT": {
        "n_all": 471,
        "nonzero_n": 103,
        "nonzero_fraction": 0.21868365180467092,
        "mean_all": 0.19957537154989385,
        "mean_given_nonzero": 0.912621359223301
      }
    },
    "low": {
      "lag1_realized_divergence_rate": {
        "n": 275,
        "mean": 0.16848484848484846,
        "sd": 0.319031265188554,
        "se": 0.019238309145869197,
        "ci95_low": 0.13242424242424242,
        "ci95_high": 0.20606060606060606,
        "half_width": 0.03681818181818182,
        "achieved_mde80_one_sided": 0.047835572050200136
      },
      "GT_nonzero_rate": {
        "n": 275,
        "mean": 0.14181818181818182,
        "sd": 0.29257977900229065,
        "se": 0.017643224512649117,
        "ci95_low": 0.10817424242424242,
        "ci95_high": 0.17787878787878786,
        "half_width": 0.03485227272727272,
        "achieved_mde80_one_sided": 0.04386943420928965
      },
      "GT": {
        "n_all": 471,
        "nonzero_n": 66,
        "nonzero_fraction": 0.14012738853503184,
        "mean_all": 0.12526539278131635,
        "mean_given_nonzero": 0.8939393939393939
      }
    }
  },
  "absolute_selection_displacement": {
    "high_mean_jaccard": {
      "n": 275,
      "mean": 0.9962871151627479,
      "sd": 0.006388805596941568,
      "se": 0.00038525947315595874,
      "ci95_low": 0.9954877869327088,
      "ci95_high": 0.9970085050013683,
      "half_width": 0.0007603590343297495,
      "achieved_mde80_one_sided": 0.000957937994781161
    },
    "low_mean_jaccard": {
      "n": 275,
      "mean": 0.9985786207167918,
      "sd": 0.0029190603291594616,
      "se": 0.0001760259609496957,
      "ci95_low": 0.9982199905190934,
      "ci95_high": 0.9988948609841634,
      "half_width": 0.0003374352325349883,
      "achieved_mde80_one_sided": 0.0004376841267010657
    },
    "high_mean_symdiff_count": {
      "n": 275,
      "mean": 0.3624747474747475,
      "sd": 0.6255440258058473,
      "se": 0.03772172406266166,
      "ci95_low": 0.2911098484848485,
      "ci95_high": 0.43914520202020196,
      "half_width": 0.07401767676767673,
      "achieved_mde80_one_sided": 0.09379411857744603
    },
    "low_mean_symdiff_count": {
      "n": 275,
      "mean": 0.13818181818181818,
      "sd": 0.2845154176361708,
      "se": 0.01715692522491716,
      "ci95_low": 0.10631186868686869,
      "ci95_high": 0.17313510101010096,
      "half_width": 0.033411616161616135,
      "achieved_mde80_one_sided": 0.042660263255653225
    }
  },
  "far_field_gain": {
    "high": {
      "n": 275,
      "mean": -0.25757575757575757,
      "sd": 1.3678686564179499,
      "se": 0.082485583560471,
      "ci95_low": -0.42454545454545456,
      "ci95_high": -0.09968939393939402,
      "half_width": 0.16242803030303027,
      "achieved_mde80_one_sided": 0.20509832987879476
    },
    "low": {
      "n": 275,
      "mean": 0.04272727272727272,
      "sd": 0.5473963629276575,
      "se": 0.03300924268065909,
      "ci95_low": -0.023340909090909093,
      "ci95_high": 0.10455303030303019,
      "half_width": 0.06394696969696964,
      "achieved_mde80_one_sided": 0.08207665209040743
    }
  }
}
```

---

## Stage 5 — Bounded Chapter 24 V4 Verdict

```json
{
  "validity": {
    "valid": true,
    "support_gate": true,
    "capacity_gate": true
  },
  "overall_status": "EXTREME_FCP_EXPECTED_EFFECT_BOUNDED_BELOW_SEI",
  "bounded_claim": "The full-precision V4 run bounded the high-minus-low extreme FCP difference in exact expected lag-1 local construction below the predeclared scientifically meaningful effect size.",
  "hypothesis_statuses": {
    "H1_primary_exact_expected_lag1_gain": "BOUNDED_BELOW_SEI",
    "H2_realized_lag1_gain": "BOUNDED_BELOW_SEI",
    "H3_model_implied_lag1_divergence_probability": "UNRESOLVED",
    "H4_finite_horizon_transient_gain": "UNRESOLVED"
  },
  "interpretation_rules": {
    "underpowered_non_significance_is_failure": false,
    "FCP_promotion_identity_is_independent_evidence": false,
    "baseline_p_was_conditioned_away": false,
    "realized_GT_is_only_outcome": false
  },
  "what_this_does_not_establish": [
    "FCP is an independent causal variable",
    "baseline p is not a mediator",
    "causal-gain field",
    "stable high-gain regions",
    "criticality",
    "percolation",
    "coherent structures",
    "individuality",
    "organism",
    "life"
  ],
  "next": "Regardless of outcome, use the absolute FORCE/PREVENT selection displacement measurements to design a dedicated finite-budget redistribution experiment with an unbounded-budget hard-zero control."
}
```
