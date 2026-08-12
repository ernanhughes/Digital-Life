# Chapter 19 — Can the Crystal Tell Two Pasts Apart?

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-two-pasts-v1",
  "schema_version": 1,
  "chapter": 19,
  "chapter_title": "Can the Crystal Tell Two Pasts Apart?",
  "run_type": "TWO-PASTS COMMON-CHALLENGE TEST",
  "profile": "quick",
  "profile_config": {
    "groups": 96,
    "seed_noise_groups": 200,
    "radius": 64,
    "warmup_steps": 14,
    "experience_elapsed_step": 3,
    "retention_steps": 10,
    "challenge_elapsed_step": 14,
    "response_horizon": 4,
    "write_fraction": 0.2,
    "transmission_fraction": 0.5,
    "history_read_gain": 0.18,
    "challenge_gain": 0.65,
    "primary_sei_population_fraction": 0.01,
    "primary_sei_seed_noise_sd": 0.5,
    "bootstrap_reps": 2000,
    "permutations": 4000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85,
    "aperture_observation_steps": [
      1,
      2,
      4,
      6,
      8,
      10
    ]
  },
  "seed": 20260824,
  "canonical_ch18_substrate_modified": false,
  "chapter_19_extension": {
    "material_states": [
      "normal",
      "history_A",
      "history_B"
    ],
    "pre_challenge_A_B_geometry_identical": true,
    "pre_challenge_A_B_label_locations_identical": true,
    "history_identity_inert_until_challenge": true,
    "common_challenge": true
  },
  "scientific_boundary": "History discrimination only. No memory, learning, adaptation, recall, meaning, representation, self, or life claim.",
  "started_at_unix": 1786554838.0482683,
  "finished_at_unix": 1786554854.266625,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 19 did not establish that the identity of the earlier experience produces a scientifically meaningful difference in response to the later common challenge under this protocol."
}
```

---

## Stage 0 — Freeze the Chapter 19 Claim

```json
{
  "question": "Can two different prior experiences leave different retained material states that change response to the same later challenge?",
  "new_sentence_if_successful": "Under this minimal two-state material extension, the identity of an earlier experience remains locally encoded and alters the crystal's response to a later identical challenge.",
  "primary_outcome": "(A challenge response - A no-challenge response) - (B challenge response - B no-challenge response), normalized by pre-challenge population",
  "primary_direction": "A > B",
  "primary_sei_population_fraction": 0.01,
  "primary_sei_seed_noise_sd": 0.5,
  "alpha": 0.05,
  "forbidden_overclaims": [
    "memory",
    "learning",
    "adaptation",
    "recall",
    "recognition",
    "meaning",
    "representation",
    "self",
    "life"
  ],
  "status": "MEASURED"
}
```

---

## Stage 1 — Establish the Seed-Noise Scale

```json
{
  "role": "SEED-NOISE NULL",
  "groups": 200,
  "challenge_response_normalized": {
    "n": 200,
    "mean": 0.002737054555241073,
    "std": 0.011489778050706978,
    "q05": -0.018035109773175868,
    "q50": 0.002025577519772399,
    "q95": 0.021956087824351298
  },
  "status": "MEASURED"
}
```

---

## Stage 2 — Prove A and B Differ Only in Retained State Identity

```json
{
  "audit_groups": 24,
  "prechallenge_geometry_and_label_locations_exact_all": true,
  "no_challenge_A_B_exact_all": true,
  "erased_history_challenge_exact_all": true,
  "mean_labelled_cells_at_challenge": 110.33333333333333,
  "co_moving_aperture_diagnostic": {
    "1": {
      "mean_frontier_contact_fraction": 0.3366332244705564
    },
    "2": {
      "mean_frontier_contact_fraction": 0.3278507748717386
    },
    "4": {
      "mean_frontier_contact_fraction": 0.31011633164913177
    },
    "6": {
      "mean_frontier_contact_fraction": 0.2938708958544251
    },
    "8": {
      "mean_frontier_contact_fraction": 0.28187087533128996
    },
    "10": {
      "mean_frontier_contact_fraction": 0.27255323446815977
    }
  },
  "aperture_note": "Secondary only. This tracks whether retained history remains in contact with the moving growth frontier; it is not a wave claim.",
  "status": "MEASURED"
}
```

---

## Stage 3 — Does the Identity of the Past Change the Later Response?

```json
{
  "groups": 96,
  "primary_interaction_normalized": {
    "n": 96,
    "mean": 0.004400326347073426,
    "median": 0.0034146145762694318,
    "std": 0.005366395408627812,
    "ci95_low": 0.003313531299906489,
    "ci95_high": 0.0054829467327028696
  },
  "primary_directional_test": {
    "observed_mean": 0.004400326347073426,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "mean_raw_response_A_attachments": 2.5104166666666665,
  "mean_raw_response_B_attachments": -1.4166666666666667,
  "mean_prechallenge_population": 876.0833333333334,
  "mean_labelled_cells_at_challenge": 105.94791666666667,
  "all_prechallenge_invariants_pass": true,
  "all_no_challenge_A_B_exact": true,
  "all_erased_history_challenge_exact": true,
  "mean_challenge_attachments_by_response_step": {
    "A": [
      76.79166666666667,
      71.51041666666667,
      74.8125,
      78.0
    ],
    "B": [
      71.125,
      72.34375,
      75.5,
      78.21875
    ]
  },
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 19 Verdict

```json
{
  "experiment_role": "TWO-PASTS COMMON-CHALLENGE TEST",
  "question": "Can two different prior experiences leave different retained states that alter response to the same later challenge?",
  "invariant_gate_passed": true,
  "primary_p_value": 0.00024993751562109475,
  "primary_mean_normalized_interaction": 0.004400326347073426,
  "primary_ci95": [
    0.003313531299906489,
    0.0054829467327028696
  ],
  "predeclared_sei_population_fraction": 0.01,
  "seed_noise_sd": 0.011489778050706978,
  "effect_in_seed_noise_sd": 0.3829774890040343,
  "predeclared_sei_seed_noise_sd": 0.5,
  "significance_gate_passed": true,
  "raw_magnitude_gate_passed": false,
  "seed_noise_magnitude_gate_passed": false,
  "status": "FAILED",
  "bounded_claim": "Chapter 19 did not establish that the identity of the earlier experience produces a scientifically meaningful difference in response to the later common challenge under this protocol.",
  "forbidden_overclaims": [
    "memory",
    "learning",
    "adaptation",
    "recall",
    "recognition",
    "meaning",
    "representation",
    "self",
    "life"
  ],
  "next_question_if_supported": "Can a later experience overwrite, compete with, or transform the retained state left by an earlier experience?",
  "next_question_if_failed": "Do not tune significance. Diagnose whether failure came from loss of causal-aperture contact or insufficiently distinct material readout, then decide whether the mechanism itself should be redesigned."
}
```
