# Chapter 23 — Does the Process Move? (V1)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "parent_experiment_version": "digital-crystal-finite-update-budget-v3",
  "experiment_version": "digital-crystal-active-process-propagation-v1",
  "schema_version": 1,
  "chapter": 23,
  "chapter_title": "Does the Process Move?",
  "run_type": "SPATIOTEMPORAL ACTIVE-PROCESS PROPAGATION SCREEN",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "radius": 72,
    "warmup_steps": 20,
    "continuation_steps": 84,
    "loss_rate": 0.08,
    "budget": 96,
    "distances": [
      1,
      2,
      3,
      4,
      6,
      8
    ],
    "lags": [
      1,
      2,
      3,
      4,
      6,
      8
    ],
    "near_distances": [
      1,
      2
    ],
    "far_distances": [
      4,
      6,
      8
    ],
    "radial_bin_width": 3,
    "minimum_match_fraction": 0.6,
    "minimum_real_ridge_shift": 1.0,
    "minimum_null_excess_shift": 0.5,
    "minimum_ridge_slope": 0.15,
    "minimum_spearman": 0.6,
    "alpha": 0.05,
    "signflip_permutations": 5000,
    "bootstrap_reps": 2000,
    "max_capacity_fraction": 0.75,
    "scientific": true
  },
  "seed": 20260902,
  "canonical_attachment_rule_modified": false,
  "canonical_loss_rule_modified": false,
  "canonical_budget_rule_modified": false,
  "scientific_boundary": "Propagation-like spatiotemporal process organization only. No wave, phase, dispersion, individuality, autonomy, self, organism, agency, or life claim.",
  "started_at_unix": 1786570222.45369,
  "finished_at_unix": 1786570465.1812506,
  "final_status": "FAILED",
  "plot_manifest": {
    "real_surface": "ch23-v1-01-real-lag-distance.png",
    "cross_run_null_surface": "ch23-v1-02-cross-run-null.png",
    "ridge_centers": "ch23-v1-03-ridge-centers.png"
  }
}
```

---

## Stage 0 — Frozen Propagation Screen

```json
{
  "role": "SPATIOTEMPORAL ACTIVE-PROCESS PROPAGATION SCREEN",
  "question": "Does local Digital Crystal material-event activity show a reproducible lag-distance displacement beyond current geometry, radial position, opportunity class, and a cross-run future null?",
  "active_process_field_v1": {
    "material_event": [
      "attachment",
      "loss"
    ],
    "supporting_channels_recorded": [
      "evaluated frontier",
      "attachment",
      "loss",
      "reoccupation",
      "first occupation"
    ]
  },
  "source_control_design": {
    "attachment_event_control": "evaluated-but-not-attached frontier candidate",
    "loss_event_control": "occupied cell surviving the same loss step",
    "matching": [
      "occupied-neighbour count",
      "radial-distance bin",
      "same event opportunity class",
      "one-to-one without replacement"
    ]
  },
  "cross_run_future_null": "Sources and matched controls from group g are evaluated against future event frames from a different group at the same relative time, preserving target-frame event burden while destroying within-process space-time continuity.",
  "distances": [
    1,
    2,
    3,
    4,
    6,
    8
  ],
  "lags": [
    1,
    2,
    3,
    4,
    6,
    8
  ],
  "near_distances": [
    1,
    2
  ],
  "far_distances": [
    4,
    6,
    8
  ],
  "ridge_center": "positive-excess-weighted mean lag at each exact hex distance",
  "primary_group_statistic": "mean ridge center over frozen far distances minus mean ridge center over frozen near distances",
  "primary_success_gates": {
    "minimum_match_fraction": 0.6,
    "minimum_real_ridge_shift": 1.0,
    "minimum_real_minus_null_shift": 0.5,
    "minimum_population_ridge_slope": 0.15,
    "minimum_population_spearman": 0.6,
    "paired_signflip_alpha": 0.05
  },
  "new_sentence_if_successful": "Under the frozen Chapter 23 V1 measurement, local Digital Crystal material-event activity exhibits reproducible spatiotemporal lag-distance displacement beyond matched local opportunity and a cross-run future null.",
  "scientific_boundary": "Propagation-like process organization only. No wave, phase, dispersion, individuality, autonomy, self, organism, agency, or life claim.",
  "status": "FROZEN"
}
```

---

## Stage 1 — Generate Active-Process Event Fields

```json
{
  "groups": 48,
  "total_material_events": 401203,
  "matched_event_sources": 288313,
  "unmatched_event_sources": 112890,
  "match_fraction": 0.7186212466008479,
  "minimum_match_fraction": 0.6,
  "match_gate_passed": true,
  "maximum_capacity_fraction": 0.043059166719512966,
  "max_allowed_capacity_fraction": 0.75,
  "capacity_gate_passed": true,
  "collapsed_groups": 0,
  "status": "MEASURED"
}
```

---

## Stage 2 — Lag-Distance Propagation Measurement

```json
{
  "distances": [
    1,
    2,
    3,
    4,
    6,
    8
  ],
  "lags": [
    1,
    2,
    3,
    4,
    6,
    8
  ],
  "population_real_excess_surface": [
    [
      0.0002835964346053546,
      -0.0005182665532807376,
      -0.0008599969341760869,
      -0.0006026879806468235,
      -0.001125734704185195,
      -0.0012072985130971003
    ],
    [
      0.00025408854379911525,
      0.0003885543083216878,
      0.000307318281980012,
      0.00027145661198577027,
      0.0005059499974811608,
      0.0003019393596540469
    ],
    [
      0.00012892715547703897,
      3.516108487402591e-05,
      0.00031847561136803094,
      -6.186326564122484e-05,
      0.00030689951750225916,
      0.0002522051220534942
    ],
    [
      1.8716243984810584e-06,
      0.00012418142669391526,
      0.0002819114516804831,
      -1.0744332641300243e-05,
      7.885316508795167e-06,
      0.00015964500184923366
    ],
    [
      -1.209471002794945e-05,
      0.00011664210109944174,
      0.00015835486102069472,
      0.00010982681378122608,
      9.098220291616421e-05,
      -2.591006119885061e-05
    ],
    [
      2.606772314896373e-05,
      -4.978940925189657e-05,
      2.6037199649700006e-05,
      -9.374854184028877e-05,
      2.8702566954334416e-06,
      0.00010569875301865985
    ]
  ],
  "population_cross_run_null_surface": [
    [
      -9.72125760469042e-05,
      0.0003345954611100807,
      0.00010953802073132597,
      0.0002358475830767353,
      -0.00031623505378369717,
      -0.000514047512735127
    ],
    [
      -0.0001500580236640011,
      0.00036655579351624914,
      0.00024211101267258348,
      -9.859858292051518e-05,
      -6.366774654054874e-05,
      0.00010258774628930066
    ],
    [
      2.1972497005351827e-05,
      -3.8718465728783315e-05,
      7.709537344907545e-05,
      0.00013702591186464728,
      8.616083737473341e-05,
      -6.63352268744181e-05
    ],
    [
      5.9432092905406346e-05,
      5.229208223280181e-05,
      5.5442561977594975e-05,
      -7.885637916668182e-05,
      6.537213969407304e-05,
      4.730831946564545e-05
    ],
    [
      1.0911565691619437e-06,
      -0.00011555098730592639,
      5.1127788868662004e-05,
      7.037279484575284e-05,
      -2.932641562881719e-05,
      5.5696866210443403e-05
    ],
    [
      2.6866053092150424e-05,
      -2.6276533917392784e-06,
      7.119932132874885e-05,
      -3.155915732828727e-05,
      -7.766298518878795e-05,
      0.00021842759183933526
    ]
  ],
  "population_real_minus_null_surface": [
    [
      0.00038080901065225877,
      -0.0008528620143908183,
      -0.0009695349549074129,
      -0.0008385355637235588,
      -0.0008094996504014978,
      -0.0006932510003619732
    ],
    [
      0.00040414656746311635,
      2.1998514805438637e-05,
      6.52072693074285e-05,
      0.00037005519490628544,
      0.0005696177440217096,
      0.00019935161336474626
    ],
    [
      0.00010695465847168714,
      7.387955060280922e-05,
      0.0002413802379189555,
      -0.00019888917750587212,
      0.00022073868012752575,
      0.0003185403489279123
    ],
    [
      -5.756046850692529e-05,
      7.188934446111344e-05,
      0.00022646888970288812,
      6.811204652538158e-05,
      -5.748682318527787e-05,
      0.00011233668238358821
    ],
    [
      -1.3185866597111394e-05,
      0.00023219308840536813,
      0.00010722707215203272,
      3.9454018935473244e-05,
      0.0001203086185449814,
      -8.160692740929402e-05
    ],
    [
      -7.983299431866923e-07,
      -4.716175586015729e-05,
      -4.516212167904885e-05,
      -6.218938451200149e-05,
      8.053324188422139e-05,
      -0.0001127288388206754
    ]
  ],
  "population_real_ridge_centers": [
    1.0,
    4.183789285991089,
    4.813157240298823,
    4.205842794411215,
    3.5593274008276787,
    6.018343307450741
  ],
  "population_null_ridge_centers": [
    2.8547784885080105,
    3.2058094917216784,
    4.090949232356029,
    3.934444767884586,
    4.944458592037251,
    6.280976083868329
  ],
  "population_real_ridge_slope": 0.44150859468168596,
  "population_real_ridge_spearman": 0.6,
  "real_group_ridge_shift": {
    "mean": 0.5395049482094026,
    "ci95_low": 0.11471562167533075,
    "ci95_high": 0.9621883088886244,
    "n": 48
  },
  "null_group_ridge_shift": {
    "mean": 0.18171855515588833,
    "ci95_low": -0.24222346460599994,
    "ci95_high": 0.629220818594174,
    "n": 48
  },
  "real_minus_null_group_ridge_shift": {
    "mean": 0.3577863930535143,
    "ci95_low": -0.17082541149805638,
    "ci95_high": 0.9067326379485354,
    "n": 48
  },
  "paired_signflip_test": {
    "observed_mean": 0.3577863930535143,
    "p_value": 0.10717856428714258,
    "permutations": 5000,
    "n": 48,
    "null_mean": -0.0016608000391929586,
    "null_q95": 0.4810038263274218
  },
  "groups_with_finite_paired_shift": 48,
  "status": "MEASURED"
}
```

---

## Stage 3 — Bounded Chapter 23 V1 Verdict

```json
{
  "question": "Does local material-event activity exhibit propagation-like lag-distance displacement beyond matched local opportunity and a cross-run future null?",
  "validity": {
    "match_gate_passed": true,
    "capacity_gate_passed": true,
    "finite_group_gate_passed": true,
    "all_validity_gates_passed": true
  },
  "real_ridge_shift_mean": 0.5395049482094026,
  "minimum_real_ridge_shift": 1.0,
  "real_ridge_shift_gate_passed": false,
  "real_minus_null_shift_mean": 0.3577863930535143,
  "minimum_real_minus_null_shift": 0.5,
  "real_minus_null_gate_passed": false,
  "paired_signflip_p_value": 0.10717856428714258,
  "alpha": 0.05,
  "significance_gate_passed": false,
  "population_ridge_slope": 0.44150859468168596,
  "minimum_ridge_slope": 0.15,
  "ridge_slope_gate_passed": true,
  "population_ridge_spearman": 0.6,
  "minimum_spearman": 0.6,
  "spearman_gate_passed": true,
  "status": "FAILED",
  "bounded_claim": "Chapter 23 V1 did not satisfy all frozen gates required to claim propagation-like spatiotemporal organization of Digital Crystal material-event activity beyond matched local opportunity and the cross-run future null. Spatial causal locality from Chapter 22 remains measured; propagation is not established by this screen.",
  "forbidden_overclaims": [
    "wave",
    "wave equation",
    "phase",
    "dispersion relation",
    "individual",
    "individuality",
    "autonomy",
    "causal closure",
    "self",
    "organism",
    "agency",
    "life"
  ],
  "next_question_if_supported": "Run a fresh causal intervention on the measured active-process field: perturb an upstream activity patch and test whether the predicted downstream lag-distance region changes preferentially. Do not yet use individuality terminology.",
  "next_question_if_failed": "Do not retune distances, lags, matching strata, or success thresholds. Record local causal structure without demonstrated propagation and reconsider whether the active field is locally persistent, dispersive, or only geometry-driven."
}
```
