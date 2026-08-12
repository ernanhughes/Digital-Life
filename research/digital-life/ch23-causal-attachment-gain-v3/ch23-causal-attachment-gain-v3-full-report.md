# Chapter 23 — Causal Gain of One Attachment (V3)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "parent_experiment_version": "digital-crystal-finite-update-budget-v3",
  "experiment_version": "digital-crystal-causal-attachment-gain-v3",
  "schema_version": 3,
  "chapter": 23,
  "chapter_title": "Does the Process Move?",
  "run_title": "Causal Gain of One Attachment",
  "run_type": "FRESH FORCE/PREVENT COUNTERFACTUAL CAUSAL-GAIN EXPERIMENT",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "probes_per_group": 4,
    "probe_quantiles": [
      0.2,
      0.4,
      0.6,
      0.8
    ],
    "radius": 72,
    "initial_warmup_steps": 20,
    "lossy_pre_steps": 20,
    "horizon": 10,
    "loss_rate": 0.08,
    "budget": 96,
    "interior_margin": 12,
    "minimum_frontier_candidates": 24,
    "minimum_direct_gain": 0.1,
    "minimum_multistep_amplification": 0.2,
    "mechanical_consistency_tolerance": 0.1,
    "alpha": 0.05,
    "bootstrap_reps": 2500,
    "signflip_permutations": 5000,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260904,
  "previous_seeds": {
    "v1": 20260902,
    "v2": 20260903
  },
  "fresh_seed": true,
  "frozen_model_parameters": {
    "base_bias": -2.1,
    "neighbor_gain": 0.78,
    "signal_rate_gain": 0.28,
    "anisotropy_gain": 0.95,
    "signal_phase_gain": 1.15,
    "crowding_penalty": 0.22,
    "loss_rate": 0.08,
    "budget": 96
  },
  "canonical_rules_modified": false,
  "intervention_only": "One frontier cell inserted in FORCE between completed updates; same checkpoint unchanged in PREVENT.",
  "started_at_unix": 1786576397.9895563,
  "finished_at_unix": 1786576411.1791916,
  "final_status": "DIRECT_CAUSAL_GAIN_WITH_MULTISTEP_AMPLIFICATION",
  "critical_reference": "BELOW_ONE"
}
```

---

## Stage 0 — Frozen V3 Causal-Gain Protocol

```json
{
  "role": "FRESH COUNTERFACTUAL CAUSAL-GAIN EXPERIMENT",
  "fresh_seed": 20260904,
  "v2_interpretive_correction": "d=0 source/control effects are definitional and excluded. V3 tests the same frontier cell in force/prevent branches.",
  "intervention": "Insert one eligible frontier cell into FORCE between completed updates; leave the same cell empty in PREVENT.",
  "d0_rule": "Intervention site excluded from every causal-gain claim.",
  "probe_quantiles": [
    0.2,
    0.4,
    0.6,
    0.8
  ],
  "probes_per_group": 4,
  "horizon": 10,
  "g_mech_1": "Exact branch-specific expected next-update ring-1 attachment difference under frozen probabilities and exact finite-budget evaluated sets.",
  "g1": "Realized force-minus-prevent next-update ring-1 attachments.",
  "G_H": "Finite-horizon force-minus-prevent attachments over d=1..H, lags=1..H. Not called a formal branching ratio.",
  "G_H_global": "Whole-lattice attachment difference excluding intervention site; diagnostic for finite-budget substitutions.",
  "H1_direct_causal_excitation": {
    "minimum_mean_g1": 0.1,
    "alpha": 0.05
  },
  "H2_mechanical_accounting": {
    "comparison": "g1 - g_mech_1",
    "consistency_tolerance": 0.1,
    "requires_ci_include_zero": true
  },
  "H3_multistep_amplification": {
    "quantity": "G_H - g1",
    "minimum_mean_amplification": 0.2,
    "alpha": 0.05
  },
  "H4_branching_critical_reference": "Compare 95% CI of G_H with 1.0 descriptively. G_H is not asserted to be a formal branching ratio.",
  "scientific_boundary": "Causal construction gain only. No formal branching ratio, critical point, phase transition, directed percolation, Hawkes, excitable medium, wave, individuality, autonomy, organism, or life claim.",
  "status": "FROZEN"
}
```

---

## Stage 1 — Force/Prevent Attachment Interventions

```json
{
  "requested_groups": 48,
  "groups_used": 48,
  "skipped_groups": 0,
  "total_probes": 192,
  "probes_per_used_group": 4.0,
  "maximum_capacity_fraction": 0.04350307565476568,
  "max_allowed_capacity_fraction": 0.75,
  "capacity_gate_passed": true,
  "minimum_group_coverage_gate": true,
  "status": "MEASURED"
}
```

---

## Stage 2 — Causal-Gain Measurements

```json
{
  "g_mech_1": {
    "n": 48,
    "mean": 0.10466201188269579,
    "ci95_low": 0.07483862529547736,
    "ci95_high": 0.13521847583827848,
    "half_width": 0.03018992527140056
  },
  "g1_realized_ring1": {
    "n": 48,
    "mean": 0.11458333333333333,
    "ci95_low": 0.0625,
    "ci95_high": 0.16666666666666666,
    "half_width": 0.05208333333333333
  },
  "g1_minus_g_mech_1": {
    "n": 48,
    "mean": 0.009921321450637541,
    "ci95_low": -0.034810472297115015,
    "ci95_high": 0.055131664126763,
    "half_width": 0.04497106821193901
  },
  "G_H_local": {
    "n": 48,
    "mean": 0.5833333333333334,
    "ci95_low": 0.390625,
    "ci95_high": 0.7864583333333334,
    "half_width": 0.19791666666666669
  },
  "G_H_global": {
    "n": 48,
    "mean": 0.5364583333333334,
    "ci95_low": 0.2552083333333333,
    "ci95_high": 0.828125,
    "half_width": 0.28645833333333337
  },
  "multistep_amplification_GH_minus_g1": {
    "n": 48,
    "mean": 0.46875,
    "ci95_low": 0.2864583333333333,
    "ci95_high": 0.6458333333333334,
    "half_width": 0.17968750000000003
  },
  "immediate_frontier_opportunity_delta": {
    "n": 48,
    "mean": -0.390625,
    "ci95_low": -0.4739583333333333,
    "ci95_high": -0.3020833333333333,
    "half_width": 0.0859375
  },
  "scope": "Statistics use one mean per independent group; multiple probes within a group are not treated as independent replicates.",
  "population_distance_lag_gain": [
    [
      0.0,
      0.11458333333333333,
      0.010416666666666666,
      0.005208333333333333,
      0.0,
      0.005208333333333333,
      0.005208333333333333,
      0.0,
      0.0,
      0.005208333333333333,
      0.0
    ],
    [
      0.0,
      0.08333333333333333,
      0.0,
      0.005208333333333333,
      0.010416666666666666,
      0.005208333333333333,
      -0.005208333333333333,
      0.0,
      0.0,
      0.005208333333333333,
      -0.005208333333333333
    ],
    [
      0.0,
      0.046875,
      0.0,
      0.010416666666666666,
      0.0,
      0.005208333333333333,
      0.0,
      0.005208333333333333,
      0.0,
      0.010416666666666666,
      0.0
    ],
    [
      0.0,
      0.020833333333333332,
      0.0,
      0.0,
      0.0,
      0.0,
      0.005208333333333333,
      0.0,
      0.0,
      -0.005208333333333333,
      0.0
    ],
    [
      0.0,
      0.041666666666666664,
      0.005208333333333333,
      0.0,
      0.005208333333333333,
      0.0,
      0.005208333333333333,
      -0.010416666666666666,
      -0.005208333333333333,
      -0.005208333333333333,
      0.0
    ],
    [
      0.0,
      0.005208333333333333,
      0.0,
      0.010416666666666666,
      0.005208333333333333,
      0.005208333333333333,
      0.0,
      0.0,
      0.015625,
      0.0,
      0.0
    ],
    [
      0.0,
      0.020833333333333332,
      0.036458333333333336,
      0.015625,
      -0.005208333333333333,
      0.0,
      0.005208333333333333,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    [
      0.0,
      0.010416666666666666,
      0.005208333333333333,
      0.015625,
      0.005208333333333333,
      0.005208333333333333,
      -0.005208333333333333,
      -0.005208333333333333,
      0.0,
      -0.005208333333333333,
      0.005208333333333333
    ],
    [
      0.0,
      0.03125,
      0.020833333333333332,
      0.0,
      0.010416666666666666,
      0.0,
      -0.005208333333333333,
      0.010416666666666666,
      -0.005208333333333333,
      -0.005208333333333333,
      0.010416666666666666
    ],
    [
      0.0,
      -0.020833333333333332,
      0.020833333333333332,
      -0.005208333333333333,
      -0.005208333333333333,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ]
  ],
  "population_gain_by_lag": [
    0.14583333333333334,
    0.09895833333333333,
    0.078125,
    0.020833333333333332,
    0.036458333333333336,
    0.041666666666666664,
    0.07291666666666667,
    0.031249999999999997,
    0.06770833333333333,
    -0.010416666666666666
  ],
  "population_gain_by_distance": [
    0.0,
    0.3541666666666667,
    0.09895833333333333,
    0.057291666666666664,
    0.026041666666666668,
    0.026041666666666664,
    0.005208333333333335,
    0.0,
    0.005208333333333335,
    1.734723475976807e-18,
    0.010416666666666666
  ],
  "probe_probability_strata": [
    {
      "probe": 0,
      "quantile": 0.2,
      "mean_baseline_probability": 0.382388082073806,
      "mean_g_mech_1": 0.26067284193048534,
      "mean_g1": 0.3333333333333333,
      "mean_G_H": 1.5833333333333333
    },
    {
      "probe": 1,
      "quantile": 0.4,
      "mean_baseline_probability": 0.43590827848380337,
      "mean_g_mech_1": 0.07276106945465499,
      "mean_g1": 0.041666666666666664,
      "mean_G_H": 0.2708333333333333
    },
    {
      "probe": 2,
      "quantile": 0.6,
      "mean_baseline_probability": 0.6999909148469724,
      "mean_g_mech_1": 0.08278968456801589,
      "mean_g1": 0.08333333333333333,
      "mean_G_H": 0.25
    },
    {
      "probe": 3,
      "quantile": 0.8,
      "mean_baseline_probability": 0.816089358663605,
      "mean_g_mech_1": 0.0024244515776269716,
      "mean_g1": 0.0,
      "mean_G_H": 0.22916666666666666
    }
  ]
}
```

---

## Stage 3 — Frozen V3 Hypothesis Verdicts

```json
{
  "validity": {
    "capacity_gate_passed": true,
    "group_coverage_gate_passed": true,
    "valid_for_scientific_interpretation": true
  },
  "H1_direct_causal_excitation": {
    "minimum_effect": 0.1,
    "summary": {
      "n": 48,
      "mean": 0.11458333333333333,
      "ci95_low": 0.0625,
      "ci95_high": 0.16666666666666666,
      "half_width": 0.05208333333333333
    },
    "signflip": {
      "n": 48,
      "observed_mean": 0.11458333333333333,
      "p_value": 0.0001999600079984003,
      "permutations": 5000,
      "null_mean": -0.0004666666666666667,
      "null_q95": 0.052083333333333336
    },
    "status": "SUPPORTED"
  },
  "H2_one_step_mechanical_accounting": {
    "quantity": "g1 - g_mech_1",
    "tolerance": 0.1,
    "summary": {
      "n": 48,
      "mean": 0.009921321450637541,
      "ci95_low": -0.034810472297115015,
      "ci95_high": 0.055131664126763,
      "half_width": 0.04497106821193901
    },
    "status": "CONSISTENT_WITH_MECHANICS",
    "interpretation": "Calibration/accounting check, not an emergence claim."
  },
  "H3_multistep_amplification": {
    "quantity": "G_H - g1",
    "minimum_effect": 0.2,
    "summary": {
      "n": 48,
      "mean": 0.46875,
      "ci95_low": 0.2864583333333333,
      "ci95_high": 0.6458333333333334,
      "half_width": 0.17968750000000003
    },
    "signflip": {
      "n": 48,
      "observed_mean": 0.46875,
      "p_value": 0.0001999600079984003,
      "permutations": 5000,
      "null_mean": -0.0017041666666666663,
      "null_q95": 0.1875
    },
    "status": "SUPPORTED"
  },
  "H4_branching_critical_reference": {
    "G_H_summary": {
      "n": 48,
      "mean": 0.5833333333333334,
      "ci95_low": 0.390625,
      "ci95_high": 0.7864583333333334,
      "half_width": 0.19791666666666669
    },
    "reference_value": 1.0,
    "status": "BELOW_ONE",
    "interpretation_boundary": "G_H is finite-horizon causal construction gain, not a formal branching ratio."
  }
}
```

---

## Stage 4 — Bounded Chapter 23 V3 Verdict

```json
{
  "status": "DIRECT_CAUSAL_GAIN_WITH_MULTISTEP_AMPLIFICATION",
  "bounded_claim": "Forcing one eligible Digital Crystal attachment caused a positive next-update increase in neighbouring construction and the causal effect accumulated additional positive gain over the frozen horizon. The finite-horizon gain must not yet be called a formal branching ratio.",
  "critical_reference": "BELOW_ONE",
  "critical_reference_note": "BELOW_ONE means only that the 95% CI of finite-horizon causal construction gain lies below 1. It does not establish a formal subcritical branching process.",
  "what_this_does_not_establish": [
    "formal branching ratio",
    "critical point",
    "phase transition",
    "directed percolation",
    "Hawkes process",
    "excitable medium",
    "wave",
    "individuality",
    "autonomy",
    "organism",
    "life"
  ],
  "next_if_gain_below_one": "Close Chapter 23 around measured local causal gain and rapid attenuation. Chapter 24 can then freeze a neighbor_gain sweep, with budget fixed, to ask whether a causal-gain transition exists.",
  "next_if_gain_above_one": "Freshly confirm causal gain before any criticality language, then map spatial/temporal persistence and define direct descendant semantics."
}
```
