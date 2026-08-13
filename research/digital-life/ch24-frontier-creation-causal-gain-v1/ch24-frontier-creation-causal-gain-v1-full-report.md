# Chapter 24 — Where Is Causal Gain Created? (V1)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-frontier-creation-causal-gain-v1",
  "schema_version": 1,
  "base_model_version": "digital-crystal-v1-frozen",
  "parent_experiment_version": "digital-crystal-finite-update-budget-v3",
  "chapter": 24,
  "chapter_title": "Where Is Causal Gain Created?",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 76,
    "warmup_steps": 20,
    "lossy_pre_steps": 20,
    "horizon": 12,
    "loss_rate": 0.08,
    "budget": 96,
    "radial_bin_width": 3,
    "probability_tolerance": 0.05,
    "local_frontier_density_tolerance": 0.1,
    "minimum_fcp_difference": 1,
    "minimum_pair_gain_difference": 0.15,
    "minimum_promoted_difference": 1.0,
    "minimum_group_coverage_fraction": 0.7,
    "max_pairs_per_group": 8,
    "bootstrap_reps": 3000,
    "signflip_permutations": 8000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260906,
  "previous_ch23_seeds": [
    20260902,
    20260903,
    20260904,
    20260905
  ],
  "fresh_seed": true,
  "target": "transient causal gain",
  "classifier_used": false,
  "canonical_rules_modified": false,
  "started_at_unix": 1786578476.80408,
  "finished_at_unix": 1786578533.5920386,
  "final_status": "FRONTIER_GEOMETRY_CONTRAST_SUPPORTED_GAIN_LINK_FAILED"
}
```

---

## Stage 0 — Frozen Chapter 24 V1 Protocol

```json
{
  "role": "FRONTIER CREATION POTENTIAL / TRANSIENT CAUSAL GAIN TEST",
  "fresh_seed": 20260906,
  "target": "transient causal gain G_T(H), force x then remove after one causal update",
  "horizon": 12,
  "FCP_definition": "|frontier after forcing x occupied| - |frontier before forcing x|",
  "matching": {
    "same_occupied_neighbor_count": true,
    "same_radial_bin_width": 3,
    "max_baseline_probability_difference": 0.05,
    "max_local_frontier_density_difference": 0.1,
    "minimum_fcp_difference": 1
  },
  "H1": {
    "quantity": "G_T(high-FCP) - G_T(low-FCP), averaged to one value/group",
    "minimum_effect": 0.15,
    "requires_ci_low_above_zero": true,
    "alpha": 0.05
  },
  "H2": {
    "quantity": "ring1 newly promoted frontier(high) - low",
    "minimum_effect": 1.0,
    "requires_ci_low_above_zero": true
  },
  "coverage_gate": 0.7,
  "descriptive_only": [
    "Spearman correlations",
    "scatter plots",
    "binned means"
  ],
  "no_classifier": true,
  "scientific_boundary": "Local frontier geometry as a causal predictor of transient construction gain only.",
  "status": "FROZEN"
}
```

---

## Stage 1 — Matched High/Low FCP Interventions

```json
{
  "requested_groups": 48,
  "groups_with_pairs": 48,
  "coverage_fraction": 1.0,
  "minimum_coverage_fraction": 0.7,
  "coverage_gate_passed": true,
  "total_pairs": 356,
  "mean_pairs_per_group_with_pairs": 7.416666666666667,
  "pair_count_distribution": {
    "min": 4,
    "median": 8.0,
    "max": 8
  },
  "maximum_capacity_fraction": 0.03833228911545253,
  "capacity_gate_passed": true,
  "status": "MEASURED"
}
```

---

## Stage 2 — Primary Matched FCP Tests

```json
{
  "H1_high_fcp_greater_transient_gain": {
    "group_delta_G_local": {
      "n": 48,
      "mean": 0.16674107142857142,
      "ci95_low": -0.07830109126984128,
      "ci95_high": 0.43116691468253976,
      "half_width": 0.25473400297619053
    },
    "minimum_effect": 0.15,
    "signflip": {
      "n": 48,
      "observed_mean": 0.16674107142857142,
      "p_value": 0.10536182977127859,
      "permutations": 8000
    }
  },
  "H2_frontier_promotion_contrast": {
    "group_delta_promoted_frontier": {
      "n": 48,
      "mean": 1.2588293650793652,
      "ci95_low": 1.1960987103174603,
      "ci95_high": 1.3249410962301589,
      "half_width": 0.0644211929563493
    },
    "minimum_effect": 1.0,
    "signflip": {
      "n": 48,
      "observed_mean": 1.2588293650793652,
      "p_value": 0.00012498437695288088,
      "permutations": 8000
    }
  },
  "matching_diagnostics": {
    "fcp_difference": {
      "n": 48,
      "mean": 1.2588293650793652,
      "ci95_low": 1.196924603174603,
      "ci95_high": 1.3297712053571429,
      "half_width": 0.06642330109126993
    },
    "baseline_probability_difference_high_minus_low": {
      "n": 48,
      "mean": 1.9716646745606233e-17,
      "ci95_low": -1.4303449022643922e-17,
      "ci95_high": 5.453540369513747e-17,
      "half_width": 3.44194263588907e-17
    },
    "local_frontier_density_difference_high_minus_low": {
      "n": 48,
      "mean": -0.020230263157894734,
      "ci95_low": -0.024308884189640764,
      "ci95_high": -0.016147040779030907,
      "half_width": 0.0040809217053049286
    }
  },
  "system_level_diagnostics": {
    "global_gain_difference_high_minus_low": {
      "n": 48,
      "mean": -0.04593253968253969,
      "ci95_low": -0.320102306547619,
      "ci95_high": 0.23035404265873025,
      "half_width": 0.2752281746031746
    },
    "far_field_gain_difference_high_minus_low": {
      "n": 48,
      "mean": -0.21267361111111108,
      "ci95_low": -0.4424627976190476,
      "ci95_high": 0.030564236111111146,
      "half_width": 0.23651351686507938
    }
  }
}
```

---

## Stage 3 — Descriptive Local Causal-Gain Map

```json
{
  "n_intervention_sites": 712,
  "spearman_correlations_descriptive": {
    "FCP_vs_gain": 0.04302610755645206,
    "promoted_frontier_vs_gain": 0.04302610755645206,
    "occupied_neighbors_vs_gain": -0.0678966294764339,
    "baseline_probability_vs_gain": -0.021212355810904866,
    "local_frontier_density_vs_gain": -0.07684601606056014
  },
  "gain_by_FCP": [
    {
      "FCP": -1,
      "n": 147,
      "mean_transient_gain": 0.013605442176870748
    },
    {
      "FCP": 0,
      "n": 186,
      "mean_transient_gain": 0.14516129032258066
    },
    {
      "FCP": 1,
      "n": 220,
      "mean_transient_gain": 0.17272727272727273
    },
    {
      "FCP": 2,
      "n": 159,
      "mean_transient_gain": 0.5345911949685535
    }
  ],
  "scope": "Descriptive only. Sites within checkpoints are repeated measures and are not treated as independent confirmatory replicates."
}
```

---

## Stage 4 — Bounded Chapter 24 V1 Verdict

```json
{
  "validity": {
    "valid": true,
    "coverage_gate": true,
    "capacity_gate": true
  },
  "H1": {
    "status": "FAILED",
    "result": {
      "group_delta_G_local": {
        "n": 48,
        "mean": 0.16674107142857142,
        "ci95_low": -0.07830109126984128,
        "ci95_high": 0.43116691468253976,
        "half_width": 0.25473400297619053
      },
      "minimum_effect": 0.15,
      "signflip": {
        "n": 48,
        "observed_mean": 0.16674107142857142,
        "p_value": 0.10536182977127859,
        "permutations": 8000
      }
    }
  },
  "H2": {
    "status": "SUPPORTED",
    "result": {
      "group_delta_promoted_frontier": {
        "n": 48,
        "mean": 1.2588293650793652,
        "ci95_low": 1.1960987103174603,
        "ci95_high": 1.3249410962301589,
        "half_width": 0.0644211929563493
      },
      "minimum_effect": 1.0,
      "signflip": {
        "n": 48,
        "observed_mean": 1.2588293650793652,
        "p_value": 0.00012498437695288088,
        "permutations": 8000
      }
    }
  },
  "overall_status": "FRONTIER_GEOMETRY_CONTRAST_SUPPORTED_GAIN_LINK_FAILED",
  "bounded_claim": "The matched high-FCP sites created more frontier opportunity as designed, but the frozen experiment did not establish a scientifically meaningful increase in transient causal gain.",
  "what_this_does_not_establish": [
    "FCP is the only determinant of causal gain",
    "causal-gain field is a physical field",
    "high-gain regions",
    "spatial clustering",
    "temporal persistence",
    "percolation",
    "criticality",
    "phase transition",
    "coherent structure",
    "natural boundary",
    "individuality",
    "organism",
    "life"
  ],
  "next_if_supported": "Map a validated local gain proxy across whole frontiers and test whether high-gain locations cluster in space beyond matched radial/density controls.",
  "next_if_failed": "Do not add a classifier. Audit which local geometric term actually distinguishes causal gain before attempting spatial maps."
}
```
