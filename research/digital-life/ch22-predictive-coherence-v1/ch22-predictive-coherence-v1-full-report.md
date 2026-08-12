# Chapter 22 — When Does the Process Become One Thing? (V1)

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-predictive-coherence-v1",
  "schema_version": 1,
  "chapter": 22,
  "chapter_title": "When Does the Process Become One Thing?",
  "run_type": "PREDICTIVE COHERENCE SCREEN",
  "profile": "quick",
  "profile_config": {
    "groups": 96,
    "radius": 72,
    "warmup_steps": 20,
    "continuation_steps": 84,
    "loss_rate": 0.08,
    "budget": 96,
    "candidate_radius_fractions": [
      0.3,
      0.45,
      0.6,
      0.75,
      0.9
    ],
    "history_window": 4,
    "prediction_horizon": 4,
    "checkpoint_stride": 4,
    "first_checkpoint_after_warmup": 12,
    "sector_count": 6,
    "radial_null_bins": 6,
    "ridge_alpha": 10.0,
    "test_fraction": 0.25,
    "primary_sei_excess_r2": 0.02,
    "permutations": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.75
  },
  "seed": 20260831,
  "candidate_scale_family_frozen": [
    0.3,
    0.45,
    0.6,
    0.75,
    0.9
  ],
  "canonical_attachment_probability_modified": false,
  "observer_null_feeds_back_into_dynamics": false,
  "scientific_boundary": "Predictive coherence only. No individual, individuality, autonomy, causal closure, self, agency, organism, or life claim.",
  "started_at_unix": 1786560628.9354508,
  "finished_at_unix": 1786561745.9987078,
  "stage_0_status": "MEASURED",
  "stage_1_status": "MEASURED",
  "stage_2_status": "MEASURED",
  "stage_3_status": "MEASURED",
  "final_status": "FAILED",
  "bounded_claim": "Chapter 22 V1 did not establish the predeclared family-level excess predictive-coherence claim across the frozen candidate spatial scales."
}
```

---

## Stage 0 — Freeze the Predictive-Coherence Question

```json
{
  "role": "PREDICTIVE COHERENCE SCREEN",
  "question": "Does any predeclared spatial scale contain predictive information about its own future beyond the surrounding lattice and beyond a radial-geometry-matched observer null?",
  "substrate": {
    "loss_rate": 0.08,
    "evaluation_budget": 96,
    "scheduling": "neutral keyed scheduling"
  },
  "candidate_radius_fractions": [
    0.3,
    0.45,
    0.6,
    0.75,
    0.9
  ],
  "history_window": 4,
  "prediction_horizon": 4,
  "state_representation": "process-oriented region features: population/frontier density, recent attachment/loss/first/reoccupation/turnover flows, plus six-sector population and turnover decomposition",
  "primary_statistic": "max_R[(R2(S+E -> S_future)-R2(E -> S_future))_real - (R2(S+E -> S_future)-R2(E -> S_future))_null]",
  "primary_sei_excess_r2": 0.02,
  "family_null": "run-group future permutation preserving candidate-scale search",
  "alpha": 0.05,
  "geometry_null": "observer-only radial-bin-matched angular scrambling of region membership; null state never feeds back into dynamics",
  "new_sentence_if_successful": "At one or more predeclared spatial scales, the current Digital Crystal state contains predictive information about its own future beyond that available from the surrounding lattice and beyond the frozen geometry-matched observer null.",
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

## Stage 1 — Generate the Fresh Predictive Dataset

```json
{
  "role": "FRESH OBSERVATIONAL DATASET",
  "total_samples": 8160,
  "by_scale": {
    "0.3": {
      "samples": 1632,
      "groups": 96,
      "checkpoints": 17
    },
    "0.45": {
      "samples": 1632,
      "groups": 96,
      "checkpoints": 17
    },
    "0.6": {
      "samples": 1632,
      "groups": 96,
      "checkpoints": 17
    },
    "0.75": {
      "samples": 1632,
      "groups": 96,
      "checkpoints": 17
    },
    "0.9": {
      "samples": 1632,
      "groups": 96,
      "checkpoints": 17
    }
  },
  "status": "MEASURED"
}
```

---

## Stage 2 — Measure Excess Predictive Coherence

```json
{
  "role": "OBSERVED FROZEN SCALE FAMILY",
  "by_scale": [
    {
      "scale_index": 0,
      "radius_fraction": 0.3,
      "real": {
        "scale_index": 0,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.49342272731229075,
        "r2_system_plus_environment": 0.6898642016204759,
        "delta_self": 0.19644147430818515
      },
      "geometry_null": {
        "scale_index": 0,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.5576006643102627,
        "r2_system_plus_environment": 0.5849665926450123,
        "delta_self": 0.0273659283347496
      },
      "excess_predictive_coherence": 0.16907554597343555
    },
    {
      "scale_index": 1,
      "radius_fraction": 0.45,
      "real": {
        "scale_index": 1,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.6756143123473686,
        "r2_system_plus_environment": 0.81458474412011,
        "delta_self": 0.13897043177274138
      },
      "geometry_null": {
        "scale_index": 1,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.6997254707229144,
        "r2_system_plus_environment": 0.7940320062287117,
        "delta_self": 0.09430653550579737
      },
      "excess_predictive_coherence": 0.044663896266944
    },
    {
      "scale_index": 2,
      "radius_fraction": 0.6,
      "real": {
        "scale_index": 2,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.7021344338873146,
        "r2_system_plus_environment": 0.8726632977321568,
        "delta_self": 0.17052886384484223
      },
      "geometry_null": {
        "scale_index": 2,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.7615965177101839,
        "r2_system_plus_environment": 0.8710211330111504,
        "delta_self": 0.10942461530096648
      },
      "excess_predictive_coherence": 0.06110424854387575
    },
    {
      "scale_index": 3,
      "radius_fraction": 0.75,
      "real": {
        "scale_index": 3,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.6021378473262765,
        "r2_system_plus_environment": 0.8996988972527875,
        "delta_self": 0.297561049926511
      },
      "geometry_null": {
        "scale_index": 3,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.7119693653995034,
        "r2_system_plus_environment": 0.8429391764273038,
        "delta_self": 0.13096981102780036
      },
      "excess_predictive_coherence": 0.16659123889871064
    },
    {
      "scale_index": 4,
      "radius_fraction": 0.9,
      "real": {
        "scale_index": 4,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.39124846256205903,
        "r2_system_plus_environment": 0.897830270309026,
        "delta_self": 0.5065818077469669
      },
      "geometry_null": {
        "scale_index": 4,
        "train_groups": 72,
        "test_groups": 24,
        "train_samples": 1224,
        "test_samples": 408,
        "r2_environment_only": 0.6320504183906568,
        "r2_system_plus_environment": 0.848060288070503,
        "delta_self": 0.21600986967984626
      },
      "excess_predictive_coherence": 0.29057193806712067
    }
  ],
  "family_max_excess_predictive_coherence": 0.29057193806712067,
  "best_scale_radius_fraction": 0.9,
  "best_scale_index": 4,
  "primary_sei_excess_r2": 0.02,
  "status": "MEASURED"
}
```

---

## Stage 3 — Test the Frozen Scale Family Against Permuted Futures

```json
{
  "role": "FAMILY-WISE RUN-GROUP FUTURE-PERMUTATION NULL",
  "observed_family_max": 0.29057193806712067,
  "null_mean_family_max": 0.25686411603957493,
  "null_q95_family_max": 0.29471355745893557,
  "p_value": 0.08491508491508491,
  "permutations": 1000,
  "alternative": "observed family max greater than permuted future-pairing family max",
  "status": "MEASURED"
}
```

---

## Stage 4 — Bounded Chapter 22 V1 Verdict

```json
{
  "question": "Does any predeclared Digital Crystal spatial scale carry unique predictive information about its own future beyond its environment and beyond a geometry-matched observer null?",
  "best_scale_radius_fraction": 0.9,
  "family_max_excess_predictive_coherence": 0.29057193806712067,
  "primary_sei": 0.02,
  "magnitude_gate_passed": true,
  "family_permutation_p_value": 0.08491508491508491,
  "permutation_gate_passed": false,
  "status": "FAILED",
  "bounded_claim": "Chapter 22 V1 did not establish the predeclared family-level excess predictive-coherence claim across the frozen candidate spatial scales.",
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
  "next_question_if_supported": "Does perturbing the predictively coherent candidate region have preferential causal leverage over that region's own subsequent dynamics relative to matched external and null-region interventions?",
  "next_question_if_failed": "Do not tune candidate radii or decoder complexity. Close the predictive-boundary screen and test causal coherence directly only if a qualitatively new intervention design is justified."
}
```
