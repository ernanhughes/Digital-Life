# Chapter 24 — Causal Accounting: Probability Shift, Selector Swap, and Divergence (V5)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-causal-accounting-v5",
  "schema_version": 5,
  "chapter": 24,
  "run_title": "Causal Accounting: Probability Shift, Selector Swap, and Divergence",
  "profile": "full",
  "profile_config": {
    "groups": 384,
    "source_profile": "full",
    "equivalence_far_accounting": 0.02,
    "dilution_residual_tolerance": 0.05,
    "sei_realized_divergence": 0.05,
    "sei_nonzero_GT": 0.05,
    "bootstrap_reps": 7000,
    "signflip_permutations": 20000,
    "alpha": 0.05,
    "scientific": true
  },
  "source_v4_profile": {
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
  "seed": 20260910,
  "fresh_seed": true,
  "started_at_unix": 1786609550.3724864,
  "finished_at_unix": 1786609670.217361,
  "final_status": "FIXED_BUDGET_SELECTOR_ACCOUNTING_SUPPORTED"
}
```

---

## Stage 0 — Frozen V5 Causal Accounting Protocol

```json
{
  "experiment_version": "digital-crystal-causal-accounting-v5",
  "role": "MECHANISTIC ACCOUNTING OF V4 EXTREME-FCP EFFECT",
  "seed": 20260910,
  "source_profile": "full",
  "groups": 384,
  "exposure": {
    "high": "FCP >= 2",
    "low": "FCP <= -1",
    "minimum_delta_FCP": 3
  },
  "primary_accounting_identity": "E1 = shared_shift + force_only_swap + prevent_only_swap",
  "C1_causal_cone_correctness": {
    "quantity": "E1_far_exact - swap_total_far = shared_shift_far",
    "role": "hard lag-1 causal-cone correctness control",
    "equivalence_tolerance": 0.02
  },
  "H1_selector_dilution": {
    "prediction": "-(DeltaF / F_prevent) * expected PREVENT far attachments",
    "residual_tolerance": 0.05
  },
  "H3_realized_divergence": {
    "SEI": 0.05
  },
  "H4_nonzero_GT_rate": {
    "SEI": 0.05
  },
  "occupied_neighbor_distribution": "mandatory scope diagnostic",
  "absolute_E1_high_low": "mandatory mechanism discriminator",
  "status": "FROZEN",
  "stop_rule": "V5 closes Chapter 24; no threshold or formula tuning after run."
}
```

---

## Stage 1 — V5 Extreme-Pair Support and n Distribution

```json
{
  "requested_groups": 384,
  "groups_with_pairs": 281,
  "coverage_fraction": 0.7317708333333334,
  "total_pairs": 467,
  "total_interventions": 934,
  "occupied_neighbor_site_distribution": {
    "1": 934
  },
  "occupied_neighbor_pair_distribution": {
    "1": 467
  }
}
```

---

## Stage 2 — Absolute E1 and Shared-vs-Swap Accounting

```json
{
  "absolute_E1": {
    "local": {
      "high": {
        "n": 281,
        "mean": 0.15859931195367935,
        "sd": 0.23674972000368605,
        "se": 0.014123304221807355,
        "ci95_low": 0.130928680656514,
        "ci95_high": 0.18679695031141136,
        "half_width": 0.02793413482744868,
        "achieved_mde80_one_sided": 0.03511724089506192
      },
      "low": {
        "n": 281,
        "mean": 0.12804205212429803,
        "sd": 0.20427739150579402,
        "se": 0.012186167509843965,
        "ci95_low": 0.10477470833774184,
        "ci95_high": 0.152654329621905,
        "half_width": 0.02393981064208158,
        "achieved_mde80_one_sided": 0.03030059915936608
      },
      "high_minus_low": {
        "n": 281,
        "mean": 0.030557259829381327,
        "sd": 0.29975007417531646,
        "se": 0.01788159026342841,
        "ci95_low": -0.004560052217796665,
        "ci95_high": 0.06657128307988004,
        "half_width": 0.03556566764883835,
        "achieved_mde80_one_sided": 0.04446212465621238
      }
    },
    "far": {
      "high": {
        "n": 281,
        "mean": -0.11703353990264478,
        "sd": 0.2992106679471454,
        "se": 0.01784941198562737,
        "ci95_low": -0.1523485227255516,
        "ci95_high": -0.08307878451486089,
        "half_width": 0.034634869105345356,
        "achieved_mde80_one_sided": 0.044382114177405126
      },
      "low": {
        "n": 281,
        "mean": 0.0628899107580078,
        "sd": 0.17720699535302334,
        "se": 0.010571283064512958,
        "ci95_low": 0.04292014716619603,
        "ci95_high": 0.08415054774862561,
        "half_width": 0.020615200291214792,
        "achieved_mde80_one_sided": 0.026285229583398663
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.17992345066065255,
        "sd": 0.33309838588912494,
        "se": 0.019870983752934737,
        "ci95_low": -0.21847674581960574,
        "ci95_high": -0.13968751748307617,
        "half_width": 0.039394614168264785,
        "achieved_mde80_one_sided": 0.04940870155556075
      }
    },
    "global": {
      "high": {
        "n": 281,
        "mean": 0.04156577205103457,
        "sd": 0.25033284880796114,
        "se": 0.014933605751979323,
        "ci95_low": 0.013369718011710205,
        "ci95_high": 0.07104504965318569,
        "half_width": 0.02883766582073774,
        "achieved_mde80_one_sided": 0.03713203527927896
      },
      "low": {
        "n": 281,
        "mean": 0.19093196288230582,
        "sd": 0.25260322010377756,
        "se": 0.01506904474851446,
        "ci95_low": 0.16225335326220053,
        "ci95_high": 0.22063053310492436,
        "half_width": 0.029188589921361918,
        "achieved_mde80_one_sided": 0.037468800939298226
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.14936619083127126,
        "sd": 0.323738368299274,
        "se": 0.019312611916461712,
        "ci95_low": -0.18642751500909724,
        "ci95_high": -0.11137197736282949,
        "half_width": 0.03752776882313388,
        "achieved_mde80_one_sided": 0.048020324021345734
      }
    }
  },
  "shared_vs_swap_components": {
    "shared_shift_local": {
      "high": {
        "n": 281,
        "mean": 0.017473691049873265,
        "sd": 0.14484907554606238,
        "se": 0.008640971402849999,
        "ci95_low": 0.001288230718378798,
        "ci95_high": 0.03436037919130122,
        "half_width": 0.016536074236461213,
        "achieved_mde80_one_sided": 0.021485558163696662
      },
      "low": {
        "n": 281,
        "mean": 0.1226637586259084,
        "sd": 0.20204766958174866,
        "se": 0.012053153451526025,
        "ci95_low": 0.09928379345810331,
        "ci95_high": 0.14703573134015394,
        "half_width": 0.02387596894102531,
        "achieved_mde80_one_sided": 0.0299698630472622
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.1051900675760351,
        "sd": 0.23077325829645354,
        "se": 0.01376677840686695,
        "ci95_low": -0.13249511668701158,
        "ci95_high": -0.07859548897212762,
        "half_width": 0.02694981385744198,
        "achieved_mde80_one_sided": 0.03423074841908463
      }
    },
    "swap_total_local": {
      "high": {
        "n": 281,
        "mean": 0.1411256209038061,
        "sd": 0.18921995868595873,
        "se": 0.011287916375647696,
        "ci95_low": 0.11958753543501227,
        "ci95_high": 0.16349871965332183,
        "half_width": 0.02195559210915478,
        "achieved_mde80_one_sided": 0.02806712029574954
      },
      "low": {
        "n": 281,
        "mean": 0.005378293498389642,
        "sd": 0.044822148702510334,
        "se": 0.002673865219315931,
        "ci95_low": 0.0009684327849598377,
        "ci95_high": 0.011238757088339607,
        "half_width": 0.005135162151689884,
        "achieved_mde80_one_sided": 0.006648498648259587
      },
      "high_minus_low": {
        "n": 281,
        "mean": 0.13574732740541645,
        "sd": 0.19717512863587056,
        "se": 0.011762482028088743,
        "ci95_low": 0.11265637297857332,
        "ci95_high": 0.15854267319486623,
        "half_width": 0.022943150108146453,
        "achieved_mde80_one_sided": 0.029247115860212558
      }
    },
    "shared_shift_far": {
      "high": {
        "n": 281,
        "mean": 0.0,
        "sd": 0.0,
        "se": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0,
        "achieved_mde80_one_sided": 0.0
      },
      "low": {
        "n": 281,
        "mean": 0.0,
        "sd": 0.0,
        "se": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0,
        "achieved_mde80_one_sided": 0.0
      },
      "high_minus_low": {
        "n": 281,
        "mean": 0.0,
        "sd": 0.0,
        "se": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "half_width": 0.0,
        "achieved_mde80_one_sided": 0.0
      }
    },
    "swap_total_far": {
      "high": {
        "n": 281,
        "mean": -0.11703353990264478,
        "sd": 0.2992106679471454,
        "se": 0.01784941198562737,
        "ci95_low": -0.15217577752509226,
        "ci95_high": -0.0820031590617651,
        "half_width": 0.03508630923166358,
        "achieved_mde80_one_sided": 0.044382114177405126
      },
      "low": {
        "n": 281,
        "mean": 0.0628899107580078,
        "sd": 0.17720699535302334,
        "se": 0.010571283064512958,
        "ci95_low": 0.04327736671798572,
        "ci95_high": 0.08402823157715386,
        "half_width": 0.020375432429584072,
        "achieved_mde80_one_sided": 0.026285229583398663
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.17992345066065255,
        "sd": 0.33309838588912494,
        "se": 0.019870983752934737,
        "ci95_low": -0.2181046133823064,
        "ci95_high": -0.14170656850530972,
        "half_width": 0.03819902243849835,
        "achieved_mde80_one_sided": 0.04940870155556075
      }
    },
    "shared_shift_global": {
      "high": {
        "n": 281,
        "mean": 0.017473691049873265,
        "sd": 0.14484907554606238,
        "se": 0.008640971402849999,
        "ci95_low": 0.0012657490405801326,
        "ci95_high": 0.03507220314646119,
        "half_width": 0.016903227052940527,
        "achieved_mde80_one_sided": 0.021485558163696662
      },
      "low": {
        "n": 281,
        "mean": 0.1226637586259084,
        "sd": 0.20204766958174866,
        "se": 0.012053153451526025,
        "ci95_low": 0.09935854611253069,
        "ci95_high": 0.14648696671458783,
        "half_width": 0.023564210301028572,
        "achieved_mde80_one_sided": 0.0299698630472622
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.1051900675760351,
        "sd": 0.23077325829645354,
        "se": 0.01376677840686695,
        "ci95_low": -0.13335603053466066,
        "ci95_high": -0.07849885648800116,
        "half_width": 0.027428587023329752,
        "achieved_mde80_one_sided": 0.03423074841908463
      }
    },
    "swap_total_global": {
      "high": {
        "n": 281,
        "mean": 0.024092081001161312,
        "sd": 0.1961794429547317,
        "se": 0.011703084400147291,
        "ci95_low": 0.0013741695931658458,
        "ci95_high": 0.047145675831727296,
        "half_width": 0.022885753119280726,
        "achieved_mde80_one_sided": 0.029099425151561355
      },
      "low": {
        "n": 281,
        "mean": 0.06826820425639744,
        "sd": 0.17171870554213572,
        "se": 0.01024387914337884,
        "ci95_low": 0.04903782190137792,
        "ci95_high": 0.0885004778070879,
        "half_width": 0.019731327952854993,
        "achieved_mde80_one_sided": 0.02547114796426157
      },
      "high_minus_low": {
        "n": 281,
        "mean": -0.044176123255236115,
        "sd": 0.24688920561459726,
        "se": 0.014728175222006671,
        "ci95_low": -0.07312523983505607,
        "ci95_high": -0.01558474773524654,
        "half_width": 0.028770246049904767,
        "achieved_mde80_one_sided": 0.03662123743091776
      }
    }
  },
  "H1_far_field_accounting": {
    "discrepancy_E1_far_minus_swap_far": {
      "n": 281,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "half_width": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "equivalence_tolerance": 0.02,
    "status": "CONSISTENT_WITH_MECHANICAL_ACCOUNTING"
  }
}
```

---

## Stage 3 — First-Order Selector-Dilution Law

```json
{
  "prediction": "predicted_far = -(DeltaF/F_prevent) * (B/F_prevent) * sum_far_frontier p_prevent",
  "raw_intervention_count": 934,
  "correlation_predicted_vs_exact_swap": 0.3325872638115836,
  "slope_through_origin": 0.8822278459344334,
  "mean_residual_exact_swap_minus_prediction": {
    "n": 281,
    "mean": 0.014042167858383659,
    "sd": 0.18013750188460934,
    "se": 0.010746102427631691,
    "ci95_low": -0.006811488039742103,
    "ci95_high": 0.03528118096976141,
    "half_width": 0.021046334504751758,
    "achieved_mde80_one_sided": 0.02671991353492628
  },
  "frozen_residual_tolerance": 0.05,
  "status": "CONSISTENT_WITH_SIMPLE_DILUTION_LAW",
  "note": "Correlation/slope are descriptive model checks. The frozen practical criterion is the group-level residual interval."
}
```

---

## Stage 4 — Realized Divergence and Conditional Cascade

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

---

## Stage 5 — Occupied-Neighbour Support and Baseline-p Scope

```json
{
  "pair_distribution_by_occupied_neighbors": {
    "1": 467
  },
  "dominant_n": "1",
  "dominant_n_fraction": 1.0,
  "baseline_p_by_n": {
    "1": {
      "interventions": 934,
      "pairs": 467,
      "high_baseline_p_mean": 0.38041146423796446,
      "low_baseline_p_mean": 0.38041146423796446,
      "raw_pair_baseline_p_difference": {
        "n": 467,
        "mean": 3.358008613025768e-17,
        "sd": 5.275744418057095e-16,
        "se": 2.4413233661889024e-17,
        "ci95_low": -1.5038232377183094e-17,
        "ci95_high": 8.166201476632575e-17,
        "half_width": 4.835012357175443e-17,
        "achieved_mde80_one_sided": 6.070289176439476e-17
      }
    }
  },
  "scope_warning": "If one n stratum dominates, scientific prose must explicitly scope the extreme-FCP result to that supported stratum."
}
```

---

## Stage 6 — Bounded Chapter 24 V5 Verdict

```json
{
  "overall_status": "FIXED_BUDGET_SELECTOR_ACCOUNTING_SUPPORTED",
  "bounded_claim": "At B=96, the lag-1 far-field expected attachment difference was accounted for by FORCE/PREVENT selector swaps within the frozen equivalence tolerance, and the simple frontier-dilution law matched the selector-swap term within its predeclared residual tolerance. Realized divergence and downstream nonzero-rate results are reported separately.",
  "C1_causal_cone_correctness": "CONSISTENT_WITH_MECHANICAL_ACCOUNTING",
  "H1_simple_dilution": "CONSISTENT_WITH_SIMPLE_DILUTION_LAW",
  "H3_realized_divergence": "UNRESOLVED",
  "H4_nonzero_transient_rate": "UNRESOLVED",
  "dominant_n": "1",
  "dominant_n_fraction": 1.0,
  "chapter24_stop_rule": "STOP. No V6. Rewrite Chapter 24 using V4/V5 and then move to the dedicated finite-budget sweep.",
  "next": "Chapter 25: B in {24,48,96,192,unbounded}, outside-causal-cone selection/attachment displacement, analytic mechanical reference, and unbounded hard-zero correctness control."
}
```
