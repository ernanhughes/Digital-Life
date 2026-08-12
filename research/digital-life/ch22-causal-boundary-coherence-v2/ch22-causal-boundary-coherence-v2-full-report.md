# Chapter 22 — When Does the Process Become One Thing? (V2)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-causal-boundary-coherence-v2",
  "schema_version": 2,
  "chapter": 22,
  "chapter_title": "When Does the Process Become One Thing?",
  "run_type": "CAUSAL BOUNDARY COHERENCE TEST",
  "profile": "quick",
  "profile_config": {
    "groups": 96,
    "radius": 72,
    "warmup_steps": 20,
    "checkpoint_after_warmup": 36,
    "response_horizon": 8,
    "loss_rate": 0.08,
    "budget": 96,
    "candidate_radius_fraction": 0.9,
    "control_radius_fraction": 0.6,
    "shell_width": 4.0,
    "distance_bin_width": 1.0,
    "intervention_k": 16,
    "primary_sei": 0.01,
    "bootstrap_reps": 3000,
    "permutations": 4000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75
  },
  "seed": 20260901,
  "v1_carry_forward_boundary": 0.9,
  "predeclared_interior_control_boundary": 0.6,
  "canonical_attachment_probability_modified": false,
  "common_random_numbers": "cell-keyed attachment, loss, and scheduling draws",
  "scientific_boundary": "Preferential causal localization only. No individual, individuality, autonomy, causal closure, self, agency, organism, or life claim.",
  "started_at_unix": 1786562520.5374033,
  "finished_at_unix": 1786562541.0442185,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 22 V2 did not establish all predeclared gates required for preferential causal localization at the V1 carry-forward boundary relative to the interior pseudo-boundary control."
}
```

---

## Stage 0 — Freeze the Causal-Boundary Test

```json
{
  "role": "CAUSAL BOUNDARY COHERENCE TEST",
  "v1_status": "FAILED predictive-coherence family test because the observed family maximum did not beat the frozen run-group future-permutation null at alpha=0.05.",
  "v1_control_note": "The V1 observer-null environment was not identical in geometry to the real annular environment. V2 does not reuse that predictive null as a causal control.",
  "question": "Does the V1 carry-forward boundary at 0.90 R_eff localize causal consequences more strongly than a predeclared interior pseudo-boundary at 0.60 R_eff?",
  "candidate_radius_fraction": 0.9,
  "control_radius_fraction": 0.6,
  "intervention": {
    "type": "occupied-cell removal",
    "k": 16,
    "shell_width": 4.0,
    "matching": [
      "occupied-neighbour count",
      "absolute distance-from-boundary bin",
      "exact intervention count"
    ]
  },
  "response_horizon": 8,
  "primary_statistic": "causal_localization(0.90 R_eff) - causal_localization(0.60 R_eff)",
  "causal_localization_definition": "(inside perturbation -> inner target - outside perturbation -> inner target) + (outside perturbation -> outer target - inside perturbation -> outer target)",
  "primary_sei": 0.01,
  "alpha": 0.05,
  "new_sentence_if_successful": "Perturbations on opposite sides of the V1 carry-forward spatial boundary produced preferentially boundary-localized causal consequences beyond those observed at the predeclared interior pseudo-boundary.",
  "forbidden_overclaims": [
    "individual",
    "individuality",
    "autonomy",
    "causal closure",
    "self",
    "agency",
    "organism",
    "life"
  ],
  "status": "MEASURED"
}
```

---

## Stage 1 — Run Fresh Paired Counterfactual Branches

```json
{
  "role": "FRESH PAIRED CAUSAL INTERVENTION DATASET",
  "requested_groups": 96,
  "usable_groups": 25,
  "skipped_groups": 71,
  "usable_fraction": 0.2604166666666667,
  "status": "MEASURED"
}
```

---

## Stage 2 — Measure Boundary-Localized Causal Effects

```json
{
  "role": "PRIMARY CAUSAL COHERENCE MEASUREMENT",
  "candidate_radius_fraction": 0.9,
  "control_radius_fraction": 0.6,
  "candidate_causal_localization": {
    "n": 25,
    "mean": 0.03772178756967181,
    "median": 0.0360727969348659,
    "std": 0.010954140345299993,
    "ci95_low": 0.03348340149697125,
    "ci95_high": 0.04193768432015537
  },
  "control_causal_localization": {
    "n": 25,
    "mean": 0.04496537516143774,
    "median": 0.0436036036036036,
    "std": 0.013515283818869578,
    "ci95_low": 0.0398285743807833,
    "ci95_high": 0.049927120638499925
  },
  "candidate_minus_control_excess": {
    "n": 25,
    "mean": -0.007243587591765921,
    "median": -0.007156548516842623,
    "std": 0.017924036311598106,
    "ci95_low": -0.013993531551683654,
    "ci95_high": -0.0002032319044114538
  },
  "paired_signflip_test": {
    "observed_mean": -0.007243587591765921,
    "p_value": 0.9692576855786054,
    "alternative": "greater",
    "permutations": 4000
  },
  "primary_sei": 0.01,
  "candidate_components": {
    "inside_to_inner": 0.02708837692176524,
    "outside_to_inner": 0.008961394064756857,
    "inside_to_outer": 0.005078354454627437,
    "outside_to_outer": 0.02467315916729087
  },
  "control_components": {
    "inside_to_inner": 0.028692947679528725,
    "outside_to_inner": 0.003585278581679406,
    "inside_to_outer": 0.005445702769232182,
    "outside_to_outer": 0.025303408832820597
  },
  "status": "MEASURED"
}
```

---

## Stage 3 — Bounded Chapter 22 V2 Verdict

```json
{
  "question": "Does the V1 carry-forward spatial boundary preferentially localize causal consequences relative to an ordinary interior pseudo-boundary?",
  "candidate_positive_gate_passed": true,
  "candidate_localization_mean": 0.03772178756967181,
  "excess_mean": -0.007243587591765921,
  "excess_ci95": [
    -0.013993531551683654,
    -0.0002032319044114538
  ],
  "primary_sei": 0.01,
  "magnitude_gate_passed": false,
  "paired_signflip_p_value": 0.9692576855786054,
  "significance_gate_passed": false,
  "status": "FAILED",
  "bounded_claim": "Chapter 22 V2 did not establish all predeclared gates required for preferential causal localization at the V1 carry-forward boundary relative to the interior pseudo-boundary control.",
  "forbidden_overclaims": [
    "individual",
    "individuality",
    "autonomy",
    "causal closure",
    "self",
    "agency",
    "organism",
    "life"
  ],
  "next_question_if_supported": "Does the same preferential causal boundary persist under a fresh starting-size and computational-budget robustness test without retuning the boundary?",
  "next_question_if_failed": "Do not tune radii, intervention count, shell width, or response horizon. Close the Chapter 22 causal-boundary hypothesis and treat the Digital Crystal as a spatially structured field unless a qualitatively new individuation mechanism is introduced."
}
```
