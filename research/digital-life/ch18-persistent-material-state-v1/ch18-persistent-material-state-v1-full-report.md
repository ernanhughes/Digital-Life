# Chapter 18 — Can Experience Change the Material?

## Run metadata

```json
{
  "base_model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-persistent-material-state-v1",
  "schema_version": 1,
  "chapter": 18,
  "chapter_title": "Can Experience Change the Material?",
  "run_type": "EXPLORATORY MECHANISM DISCOVERY",
  "profile": "quick",
  "profile_config": {
    "groups": 32,
    "radius": 64,
    "warmup_steps": 14,
    "experience_horizon": 8,
    "experience_pulse_step": 3,
    "retention_delay": 6,
    "ablation_horizon": 4,
    "ablation_primary_endpoint": 4,
    "challenge_horizon": 4,
    "challenge_pulse_step": 0,
    "challenge_observation_steps": [
      1,
      2,
      4
    ],
    "challenge_primary_endpoint": 2,
    "message_gain": 0.65,
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3,
    "permutations": 1000,
    "bootstrap_reps": 1000,
    "alpha": 0.05,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260814,
  "canonical_model_modified": false,
  "counterfactual_coupling": "cell-keyed CRN from Chapter 17",
  "experimental_extension": {
    "cell_states": [
      "occupied-normal",
      "occupied-modified"
    ],
    "write_rule": "During an explicit pulse, each occupied boundary cell that is not already modified is independently written with fixed probability using a separate cell-keyed material RNG channel.",
    "persistence_rule": "modified remains modified",
    "causal_rule": "each modified occupied neighbour adds a fixed local growth-score bias to a frontier cell on later steps",
    "write_probability": 0.2,
    "modified_neighbor_gain": 0.3
  },
  "scientific_boundary": "Persistent local material state only. No global memory register, history buffer, learned parameter, target behaviour, or decoder.",
  "started_at_unix": 1786537257.9436862,
  "finished_at_unix": 1786537264.692557,
  "stage_1_status": "MEASURED",
  "stage_2_status": "FAILED",
  "stage_3_status": "FAILED",
  "final_status": "FAILED",
  "next_question": "Persistent labels existed but were not shown to causally alter later growth under the ablation protocol."
}
```

# Stage 0 — Extension Audit

```json
{
  "role": "EXTENSION AUDIT",
  "base_model_version": "digital-crystal-v1-frozen",
  "experimental_extension": "digital-crystal-persistent-material-state-v1",
  "canonical_model_modified": false,
  "exact_when_material_state_empty": true,
  "material_extension_exact_reproducibility": true,
  "write_probability": 0.2,
  "modified_neighbor_gain": 0.3,
  "interpretation": "The material-state extension leaves the Chapter 17 CRN growth process unchanged while no cells are modified. The extension becomes causally active only after experience writes local material state."
}
```


# Stage 1 — Can Experience Write Persistent Local State?

```json
{
  "experience_pulse_zero_index": 3,
  "pulse_free_retention_steps": 6,
  "groups": 32,
  "modified_cells_immediately_after_write": {
    "n": 32,
    "mean": 20.5,
    "median": 20.5,
    "std": 4.330127018922194,
    "ci95_low": 19.0,
    "ci95_high": 21.96875,
    "min": 13.0,
    "max": 30.0
  },
  "modified_cells_after_retention_delay": {
    "n": 32,
    "mean": 20.5,
    "median": 20.5,
    "std": 4.330127018922194,
    "ci95_low": 18.9375,
    "ci95_high": 22.03125,
    "min": 13.0,
    "max": 30.0
  },
  "modified_fraction_after_retention_delay": {
    "n": 32,
    "mean": 0.0220179141548971,
    "median": 0.023059198865650478,
    "std": 0.0045912025407808706,
    "ci95_low": 0.020375684519302936,
    "ci95_high": 0.023615690130856855,
    "min": 0.014388489208633094,
    "max": 0.030120481927710843
  },
  "all_groups_wrote_nonzero_state": true,
  "all_groups_retained_exact_modified_count": true,
  "status": "MEASURED",
  "bounded_statement": "A transient pulse wrote local modified-cell state that remained present through the declared pulse-free retention interval. This establishes persistent experimental material state by construction; it does not establish memory."
}
```


# Stage 2 — Does the Retained State Causally Alter Later Growth?

```json
{
  "groups": 32,
  "primary_endpoint_steps_after_ablation": 4,
  "ablation": "experienced retained material labels vs identical experienced morphology with labels erased",
  "visible_morphology_identical_at_ablation": true,
  "primary_test": {
    "statistic": 0.0,
    "p_value": 1.0,
    "permutations": 1000,
    "null_mean": 0.0,
    "null_q95": 0.0,
    "null_q99": 0.0
  },
  "mean_pathwise_symmetric_difference": {
    "n": 32,
    "mean": 0.0,
    "median": 0.0,
    "std": 0.0,
    "ci95_low": 0.0,
    "ci95_high": 0.0,
    "min": 0.0,
    "max": 0.0
  },
  "alpha": 0.05,
  "status": "FAILED",
  "bounded_statement": "Removing only the persistent material labels from an otherwise identical experienced crystal did not establish a systematic later-growth difference under the frozen paired protocol."
}
```


# Stage 3 — Does Past Experience Change Response to a Later Pulse?

```json
{
  "groups": 32,
  "challenge_pulse_zero_index": 0,
  "observation_steps": [
    1,
    2,
    4
  ],
  "primary_endpoint": 2,
  "primary_contrast": "difference in pulse response between experienced-retained and experienced-erased crystals",
  "primary_test": {
    "statistic": 0.0,
    "p_value": 1.0,
    "permutations": 1000,
    "null_mean": 0.0,
    "null_q95": 0.0,
    "null_q99": 0.0
  },
  "results": {
    "1": {
      "retained_vs_erased_primary": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "erased_vs_naive_secondary": {
        "statistic": 0.3813845957950321,
        "p_value": 0.8101898101898102,
        "permutations": 1000,
        "null_mean": 0.5412192890322347,
        "null_q95": 0.8709222030565986,
        "null_q99": 1.0716145160419692
      },
      "mean_response_norm_retained": {
        "n": 32,
        "mean": 0.015500974868261545,
        "median": 0.013076012957424565,
        "std": 0.006914306504474328,
        "ci95_low": 0.013195182495887843,
        "ci95_high": 0.018115956346057158,
        "min": 0.006062706202802673,
        "max": 0.028851991172275965
      },
      "mean_response_norm_erased": {
        "n": 32,
        "mean": 0.015500974868261545,
        "median": 0.013076012957424565,
        "std": 0.006914306504474328,
        "ci95_low": 0.013196977273989649,
        "ci95_high": 0.01799135679141127,
        "min": 0.006062706202802673,
        "max": 0.028851991172275965
      },
      "mean_response_norm_naive": {
        "n": 32,
        "mean": 0.015089488616657074,
        "median": 0.013226727046050513,
        "std": 0.006224785691834603,
        "ci95_low": 0.013098717153502831,
        "ci95_high": 0.017295109302435076,
        "min": 0.00533133347061063,
        "max": 0.0329434523026008
      }
    },
    "2": {
      "retained_vs_erased_primary": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "erased_vs_naive_secondary": {
        "statistic": 0.43160317780630525,
        "p_value": 0.6593406593406593,
        "permutations": 1000,
        "null_mean": 0.5210829593435558,
        "null_q95": 0.8377595948322861,
        "null_q99": 1.047484544385744
      },
      "mean_response_norm_retained": {
        "n": 32,
        "mean": 0.018407341885717257,
        "median": 0.01717294489600176,
        "std": 0.007538118112941817,
        "ci95_low": 0.01596421565265286,
        "ci95_high": 0.02109733403193734,
        "min": 0.007535730968995161,
        "max": 0.03824556916452358
      },
      "mean_response_norm_erased": {
        "n": 32,
        "mean": 0.018407341885717257,
        "median": 0.01717294489600176,
        "std": 0.007538118112941817,
        "ci95_low": 0.01582732771138531,
        "ci95_high": 0.021114854172064754,
        "min": 0.007535730968995161,
        "max": 0.03824556916452358
      },
      "mean_response_norm_naive": {
        "n": 32,
        "mean": 0.01876088536299063,
        "median": 0.01905560729239712,
        "std": 0.006955865433604355,
        "ci95_low": 0.016315085934955807,
        "ci95_high": 0.02138668801068985,
        "min": 0.007799148502099575,
        "max": 0.033146701876320114
      }
    },
    "4": {
      "retained_vs_erased_primary": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "erased_vs_naive_secondary": {
        "statistic": 0.19703332223892553,
        "p_value": 0.994005994005994,
        "permutations": 1000,
        "null_mean": 0.4827601379999661,
        "null_q95": 0.7310758635798873,
        "null_q99": 0.8783925227900732
      },
      "mean_response_norm_retained": {
        "n": 32,
        "mean": 0.020118468219256426,
        "median": 0.018378709352051867,
        "std": 0.011519297878469602,
        "ci95_low": 0.016174440832134172,
        "ci95_high": 0.02410027876765833,
        "min": 0.0029154089739187885,
        "max": 0.05584224750611892
      },
      "mean_response_norm_erased": {
        "n": 32,
        "mean": 0.020118468219256426,
        "median": 0.018378709352051867,
        "std": 0.011519297878469602,
        "ci95_low": 0.016448171479211418,
        "ci95_high": 0.023989215813901857,
        "min": 0.0029154089739187885,
        "max": 0.05584224750611892
      },
      "mean_response_norm_naive": {
        "n": 32,
        "mean": 0.0201889354379772,
        "median": 0.018398985789610176,
        "std": 0.00971393418376374,
        "ci95_low": 0.017151565582724668,
        "ci95_high": 0.02347132122064478,
        "min": 0.0041714558413901886,
        "max": 0.054199724333281525
      }
    }
  },
  "checkpoint_control": {
    "retained_vs_erased_visible_symdiff": {
      "n": 32,
      "mean": 0.0,
      "median": 0.0,
      "std": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "erased_vs_naive_visible_symdiff": {
      "n": 32,
      "mean": 0.023428442008011557,
      "median": 0.021317849473673336,
      "std": 0.0175836757781457,
      "ci95_low": 0.017367112127858776,
      "ci95_high": 0.02956121572015796,
      "min": 0.0,
      "max": 0.06505771248688352
    }
  },
  "alpha": 0.05,
  "status": "FAILED",
  "bounded_statement": "Past experience altered a persistent local material state, and the frozen experiment did not establish that retaining that state changed the receiver's response to a later identical pulse relative to erasing it while holding experienced morphology fixed."
}
```


# Stage 4 — Bounded Chapter 18 Verdict

```json
{
  "experiment_role": "EXPLORATORY MECHANISM DISCOVERY",
  "chapter": 18,
  "question": "Can experience change the material?",
  "stage_1_persistent_state": "MEASURED",
  "stage_2_material_state_causal": "FAILED",
  "stage_3_later_response_changed": "FAILED",
  "final_status": "FAILED",
  "bounded_claim": "This experiment tests whether a transient pulse can write a local persistent material state, whether that state is causally active, and whether it changes response to later perturbation. It does not by itself establish memory, learning, adaptation, signalling, semantics, agency, individuality, reproduction, or life.",
  "nonclaims": [
    "memory",
    "learning",
    "adaptation",
    "information storage",
    "semantics",
    "signalling",
    "agency",
    "individuality",
    "reproduction",
    "life"
  ],
  "next_question": "Persistent labels existed but were not shown to causally alter later growth under the ablation protocol."
}
```
