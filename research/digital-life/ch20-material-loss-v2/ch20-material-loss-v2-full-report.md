# Chapter 20 — What Happens When the Crystal Can Lose Material? (V2)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-material-loss-v2",
  "schema_version": 2,
  "chapter": 20,
  "chapter_title": "What Happens When the Crystal Can Lose Material?",
  "run_type": "LOSS-CREATED-CONSTRUCTION-OPPORTUNITY AUTOPSY",
  "profile": "quick",
  "profile_config": {
    "groups": 48,
    "seed_noise_groups": 96,
    "radius": 72,
    "warmup_steps": 14,
    "continuation_steps": 40,
    "loss_budget_fraction_of_min_eligible": 0.1,
    "primary_sei_reoccupation_per_loss": 0.15,
    "secondary_sei_reoccupied_lost_site_fraction": 0.15,
    "bootstrap_reps": 2000,
    "permutations": 4000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75
  },
  "seed": 20260827,
  "canonical_growth_rule_modified": false,
  "v1_result": "FAILED finite-regime hypothesis; exact-count placement test showed interior loss retained substantially larger late population and many more holes.",
  "v2_new_measurement": "Observer-only distinction between first occupation and reoccupation after material loss.",
  "scientific_boundary": "Reoccupation mechanism only. No repair, regeneration, maintenance, homeostasis, metabolism, death, organism, or life claim.",
  "started_at_unix": 1786556771.7746801,
  "finished_at_unix": 1786556812.1897664,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 20 V2 did not establish the predeclared increase in reoccupation per loss for interior-biased versus surface-biased material removal under the exact-count protocol."
}
```

---

## Stage 0 — Freeze the V2 Mechanism Question

```json
{
  "role": "LOSS-CREATED-CONSTRUCTION-OPPORTUNITY AUTOPSY",
  "v1_status": "FAILED: no tested loss rate produced the predeclared finite near-stationary construction/loss regime.",
  "new_question": "When material is lost, how much subsequent attachment is first occupation and how much is reoccupation of previously occupied material?",
  "primary_comparison": "Interior-biased versus surface-biased loss with exactly matched loss count every update.",
  "primary_outcome": "reoccupation_count / cumulative_loss_count, interior minus surface",
  "primary_sei": 0.15,
  "secondary_outcome": "fraction of unique lost sites subsequently reoccupied, interior minus surface",
  "secondary_sei": 0.15,
  "mechanism_chain": [
    "material loss",
    "new empty location",
    "changed frontier",
    "ordinary attachment opportunity",
    "reoccupation or first occupation"
  ],
  "observer_only_history_ledger": true,
  "forbidden_overclaims": [
    "repair",
    "regeneration",
    "maintenance",
    "homeostasis",
    "metabolism",
    "death",
    "aging",
    "organism",
    "life"
  ],
  "status": "MEASURED"
}
```

---

## Stage 1 — Verify the Reoccupation Null

```json
{
  "groups": 96,
  "reoccupation_count_all_groups": 0,
  "mean_first_occupations": 3588.5520833333335,
  "std_first_occupations": 167.98946519548977,
  "mean_final_population": 3806.3645833333335,
  "std_final_population": 191.61480658048634,
  "role": "NO-LOSS STRUCTURAL NULL",
  "interpretation": "With no material removal, reoccupation must be zero by construction; all attachments are first occupations.",
  "status": "MEASURED"
}
```

---

## Stage 2 — Separate First Occupation from Reoccupation

```json
{
  "groups": 48,
  "all_exact_loss_counts_matched": true,
  "mean_cumulative_loss_count_each": 889.6875,
  "surface": {
    "mean_reoccupation_per_loss": 0.9363695679658072,
    "mean_lost_site_reoccupied_fraction": 0.9363924617160245,
    "mean_reoccupation_delay": 1.563724089992582,
    "mean_first_occupation_count": 3134.5833333333335,
    "mean_reoccupation_count": 833.125,
    "mean_new_frontier_sites_per_loss": 0.9952131148647402,
    "mean_late_population": 2762.025,
    "mean_late_holes": 3.2000000000000006
  },
  "interior": {
    "mean_reoccupation_per_loss": 0.9561405127844184,
    "mean_lost_site_reoccupied_fraction": 0.9566387868384768,
    "mean_reoccupation_delay": 1.0852403967101567,
    "mean_first_occupation_count": 3589.7291666666665,
    "mean_reoccupation_count": 850.6875,
    "mean_new_frontier_sites_per_loss": 1.0,
    "mean_late_population": 3141.2000000000003,
    "mean_late_holes": 37.606249999999996
  },
  "primary_interior_minus_surface_reoccupation_per_loss": {
    "n": 48,
    "mean": 0.01977094481861134,
    "median": 0.018988579059803945,
    "std": 0.00546280234735747,
    "ci95_low": 0.0182876320058967,
    "ci95_high": 0.021231648457244182
  },
  "primary_directional_test": {
    "observed_mean": 0.01977094481861134,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "primary_sei": 0.15,
  "secondary_interior_minus_surface_lost_site_reoccupied_fraction": {
    "n": 48,
    "mean": 0.020246325122452145,
    "median": 0.01990747204633192,
    "std": 0.007417463806539942,
    "ci95_low": 0.01813058928884506,
    "ci95_high": 0.02231884249283206
  },
  "secondary_directional_test": {
    "observed_mean": 0.020246325122452145,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "secondary_sei": 0.15,
  "status": "MEASURED"
}
```

---

## Stage 3 — Trace Loss to Frontier to Reoccupation

```json
{
  "mechanism_chain": {
    "surface": {
      "new_frontier_sites_per_loss": 0.9952131148647402,
      "reoccupation_per_loss": 0.9363695679658072,
      "lost_site_reoccupied_fraction": 0.9363924617160245,
      "late_holes": 3.2000000000000006
    },
    "interior": {
      "new_frontier_sites_per_loss": 1.0,
      "reoccupation_per_loss": 0.9561405127844184,
      "lost_site_reoccupied_fraction": 0.9566387868384768,
      "late_holes": 37.606249999999996
    }
  },
  "bounded_interpretation": "This stage is descriptive. It checks whether equal-count interior loss creates more new frontier and more subsequent reoccupation than equal-count surface loss. It does not label reoccupation as repair.",
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 20 V2 Verdict

```json
{
  "question": "Does material loss create new construction opportunity that is used as reoccupation by ordinary Digital Crystal growth?",
  "primary_gate_passed": false,
  "primary_mean_interior_minus_surface_reoccupation_per_loss": 0.01977094481861134,
  "primary_ci95": [
    0.0182876320058967,
    0.021231648457244182
  ],
  "primary_p_value": 0.00024993751562109475,
  "primary_sei": 0.15,
  "secondary_gate_passed": false,
  "secondary_mean_interior_minus_surface_lost_site_reoccupied_fraction": 0.020246325122452145,
  "secondary_p_value": 0.00024993751562109475,
  "secondary_sei": 0.15,
  "status": "FAILED",
  "bounded_claim": "Chapter 20 V2 did not establish the predeclared increase in reoccupation per loss for interior-biased versus surface-biased material removal under the exact-count protocol.",
  "forbidden_overclaims": [
    "repair",
    "regeneration",
    "maintenance",
    "homeostasis",
    "metabolism",
    "death",
    "aging",
    "organism",
    "life"
  ],
  "next_question_if_supported": "Does reoccupation merely refill local vacancies, or can a finite computational update budget force a tradeoff between outward construction and preservation of already-built material?",
  "next_question_if_failed": "Do not tune placement fractions. Close the reoccupation mechanism and move to a qualitatively different maintenance constraint."
}
```
