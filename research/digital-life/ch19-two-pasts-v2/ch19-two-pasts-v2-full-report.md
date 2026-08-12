# Chapter 19 — Can the Crystal Tell Two Pasts Apart? (V2)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-two-pasts-v2",
  "schema_version": 2,
  "chapter": 19,
  "chapter_title": "Can the Crystal Tell Two Pasts Apart?",
  "run_type": "NON-SYMBOLIC TWO-HISTORY MATERIAL TEST",
  "profile": "quick",
  "profile_config": {
    "groups": 96,
    "seed_noise_groups": 200,
    "radius": 64,
    "warmup_steps": 14,
    "pre_experience_steps": 3,
    "retention_steps": 10,
    "response_horizon": 4,
    "write_fraction": 0.2,
    "transmission_fraction": 0.5,
    "modified_neighbor_gain": 0.3,
    "challenge_gain": 0.65,
    "experience_angle_A": 0.0,
    "experience_angle_B": 0.5235987755982988,
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
  "seed": 20260825,
  "canonical_ch18_substrate_modified": false,
  "v1_result": "FAILED: explicit A/B label decoder produced a statistically detectable but sub-SEI effect.",
  "v2_design": "Remove symbolic A/B states. Use one MODIFIED state written to different directional boundary locations, exact-match subsequent propagation quantity, then test one common later challenge with a geometry-preserving label-erasure control.",
  "scientific_boundary": "History-dependent material response only. No memory, learning, adaptation, recall, representation, wave, flocking, self, or life claim.",
  "started_at_unix": 1786555462.986172,
  "finished_at_unix": 1786555479.905168,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 19 V2 did not establish that different spatial organizations produced by two prior directional experiences contribute a scientifically meaningful difference in response to the later common challenge beyond the geometry-only erasure control."
}
```

---

## Stage 0 — Freeze the V2 Mechanism Redesign

```json
{
  "role": "FROZEN MECHANISM-REDESIGN PROTOCOL",
  "v1_failure_being_respected": "V1 detected a directional A/B effect but failed both predeclared scientific-effect gates. V2 does not increase N, lower the SEI, increase the old decoder gain, or promote the first response step.",
  "question": "Can two different directional experiences create different spatial organizations of the SAME material state such that retained material contributes to a different response to one identical later challenge?",
  "history_encoding": "Same MODIFIED state; same initial write count; different spatial write direction only.",
  "no_symbolic_decoder": true,
  "exact_matched_propagation_quantity": true,
  "primary_outcome": "[(A challenge-A no)-(B challenge-B no)] retained minus the same interaction after geometry-preserving material erasure, normalized by mean pre-challenge population.",
  "primary_direction": "greater than zero",
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
    "wave",
    "flocking",
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
    "mean": 0.005435612182138765,
    "std": 0.013053561923406115,
    "q05": -0.01729797266328882,
    "q50": 0.004633616931080649,
    "q95": 0.025252450980392145
  },
  "status": "MEASURED"
}
```

---

## Stage 2 — Audit Quantity, Placement, and Causal Aperture

```json
{
  "audit_groups": 24,
  "initial_write_quantity_equal_by_construction": true,
  "mean_initial_write_count": 19.583333333333332,
  "exact_cumulative_propagation_quantity_match_all_groups": true,
  "mean_cumulative_propagation_A": 78.5,
  "mean_cumulative_propagation_B": 78.5,
  "mean_prechallenge_modified_A": 98.08333333333333,
  "mean_prechallenge_modified_B": 98.08333333333333,
  "mean_prechallenge_population_difference_A_minus_B": 0.20833333333333334,
  "co_moving_aperture_diagnostic": {
    "1": {
      "A_mean_contact_fraction": 0.29338793592699525,
      "B_mean_contact_fraction": 0.27399565003862897
    },
    "2": {
      "A_mean_contact_fraction": 0.28401792964440503,
      "B_mean_contact_fraction": 0.2659984528302501
    },
    "4": {
      "A_mean_contact_fraction": 0.2560767937481002,
      "B_mean_contact_fraction": 0.2498493197994802
    },
    "6": {
      "A_mean_contact_fraction": 0.24070418751721892,
      "B_mean_contact_fraction": 0.23409319735673184
    },
    "8": {
      "A_mean_contact_fraction": 0.219193439681709,
      "B_mean_contact_fraction": 0.22579537898866683
    },
    "10": {
      "A_mean_contact_fraction": 0.21472737047160306,
      "B_mean_contact_fraction": 0.21920787250111515
    }
  },
  "modified_orientation_diagnostic": {
    "1": {
      "A_mean_angle": -0.06272776527034385,
      "B_mean_angle": 0.3306070129083787
    },
    "2": {
      "A_mean_angle": -0.07310913183066034,
      "B_mean_angle": 0.32906957260646036
    },
    "4": {
      "A_mean_angle": -0.09716029154043092,
      "B_mean_angle": 0.3180182172808387
    },
    "6": {
      "A_mean_angle": -0.10745110777347269,
      "B_mean_angle": 0.32962495675364517
    },
    "8": {
      "A_mean_angle": -0.11870252395189224,
      "B_mean_angle": 0.32648980733287464
    },
    "10": {
      "A_mean_angle": -0.13234586899419715,
      "B_mean_angle": 0.32975807443831245
    }
  },
  "diagnostic_note": "Aperture/orientation summaries are secondary mechanism diagnostics. They do not establish a wave, phase code, or representation.",
  "status": "MEASURED"
}
```

---

## Stage 3 — Does Material Organization Mediate Different Later Response?

```json
{
  "groups": 96,
  "primary_material_mediated_interaction": {
    "n": 96,
    "mean": 0.00043128008849873355,
    "median": 0.0,
    "std": 0.004181411365405477,
    "ci95_low": -0.0003797564791826701,
    "ci95_high": 0.0012347116998084528
  },
  "primary_directional_test": {
    "observed_mean": 0.00043128008849873355,
    "p_value": 0.16320919770057485,
    "alternative": "greater",
    "permutations": 4000
  },
  "retained_history_interaction": {
    "n": 96,
    "mean": -0.0003542455497144991,
    "median": 0.0,
    "std": 0.006048833937579394,
    "ci95_low": -0.0015542464777679125,
    "ci95_high": 0.0008142977025564279
  },
  "erased_geometry_only_interaction": {
    "n": 96,
    "mean": -0.0007855256382132327,
    "median": 0.0,
    "std": 0.00581965117047307,
    "ci95_low": -0.0018822701387430213,
    "ci95_high": 0.00034523345745732155
  },
  "mean_raw_retained_response_A": 2.09375,
  "mean_raw_retained_response_B": 2.4583333333333335,
  "mean_raw_erased_response_A": 1.6145833333333333,
  "mean_raw_erased_response_B": 2.4166666666666665,
  "mean_prechallenge_population_A": 899.875,
  "mean_prechallenge_population_B": 900.8541666666666,
  "mean_prechallenge_modified_A": 96.17708333333333,
  "mean_prechallenge_modified_B": 96.17708333333333,
  "exact_propagation_quantity_match_all_groups": true,
  "mean_challenge_attachments_by_response_step": {
    "A": [
      77.02083333333333,
      73.29166666666667,
      75.5625,
      80.46875
    ],
    "B": [
      77.25,
      73.76041666666667,
      76.1875,
      81.14583333333333
    ]
  },
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 19 V2 Verdict

```json
{
  "experiment_role": "NON-SYMBOLIC TWO-HISTORY MATERIAL TEST",
  "question": "Can different experiences create different spatial material organizations that materially mediate different later responses?",
  "mechanism_validity_gate_passed": true,
  "primary_p_value": 0.16320919770057485,
  "primary_mean_material_mediated_interaction": 0.00043128008849873355,
  "primary_ci95": [
    -0.0003797564791826701,
    0.0012347116998084528
  ],
  "predeclared_sei_population_fraction": 0.01,
  "seed_noise_sd": 0.013053561923406115,
  "effect_in_seed_noise_sd": 0.0330392647638506,
  "predeclared_sei_seed_noise_sd": 0.5,
  "significance_gate_passed": false,
  "raw_magnitude_gate_passed": false,
  "seed_noise_magnitude_gate_passed": false,
  "status": "FAILED",
  "bounded_claim": "Chapter 19 V2 did not establish that different spatial organizations produced by two prior directional experiences contribute a scientifically meaningful difference in response to the later common challenge beyond the geometry-only erasure control.",
  "forbidden_overclaims": [
    "memory",
    "learning",
    "adaptation",
    "recall",
    "recognition",
    "meaning",
    "representation",
    "wave",
    "flocking",
    "self",
    "life"
  ],
  "next_question_if_supported": "Can a later experience rewrite or compete with the spatial material organization left by an earlier experience?",
  "next_question_if_failed": "Do not tune the effect threshold or promote a secondary endpoint. Close this specific history-discrimination mechanism unless a qualitatively different material encoding mechanism is proposed."
}
```
