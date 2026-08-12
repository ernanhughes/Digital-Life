# Chapter 17 — What Survives the Channel? Full Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-information-survival-v1.2",
  "schema_version": 1,
  "profile": "quick",
  "profile_config": {
    "groups": 24,
    "radius": 64,
    "warmup_steps": 14,
    "codeword_length": 16,
    "codeword_weight": 6,
    "retention_lags": [
      0,
      4,
      8,
      16,
      24
    ],
    "recent_growth_window": 8,
    "message_gain": 0.65,
    "cv_splits": 4,
    "null_permutations": 100,
    "rf_trees": 160,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260812,
  "started_at_unix": 1786500682.9030013,
  "scientific_boundary": "Recoverable receiver-side codeword distinction only. No semantics, sender identity, coordination, agency, individuality, or life claim.",
  "canvas_policy": "The hard-radius lattice is treated as an experimental canvas boundary, not as the phenomenon under test. Profiles deliberately use a larger radius than Chapter 16 so the retention window remains well inside the boundary; any branch reaching 85% capacity still aborts.",
  "primary_decoder": "standardized logistic regression",
  "cross_validation_boundary": "GroupKFold by receiver checkpoint group",
  "runtime_policy": {
    "matplotlib_backend": "Agg",
    "random_forest_n_jobs": 1,
    "reason": "Headless plotting and single-process RF execution avoid Windows Tk/Tcl finalization from worker threads. This changes runtime behavior only, not the experimental protocol."
  },
  "finished_at_unix": 1786500741.944981,
  "stage0_reproducibility_passed": true,
  "final_verdict": "NOT_SUPPORTED_AS_TESTED",
  "largest_recoverable_nested_codebook_by_lag": {
    "0": 0,
    "4": 0,
    "8": 0,
    "16": 0,
    "24": 0
  }
}
```

# Stage 0 — Freeze the Substrate

Digital Crystal v1 is unchanged from Chapter 16.

```json
{
  "canonical_rng_traversal": "sorted(frontier)",
  "repeat_from_identical_state_exact": true,
  "morphology_hash_a": "64f495acbf56a8f839800c44",
  "morphology_hash_b": "64f495acbf56a8f839800c44"
}
```

No information-survival result is interpreted unless this invariant passes.


# Stage 1 — Different Inputs Without Different Energy

The experiment uses a nested constant-weight codebook.

Every word has:
* the same length;
* the same number of 1 bits;
* the same first bit;
* the same last bit.

Only temporal arrangement distinguishes one word from another.

```json
{
  "count": 8,
  "length": 16,
  "weight_each": [
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    6
  ],
  "first_bit_each": [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  ],
  "last_bit_each": [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  ],
  "pairwise_hamming": {
    "min": 6,
    "mean": 6.428571428571429,
    "max": 8
  },
  "codewords": [
    "1000000010001111",
    "1111100000000001",
    "1000011101000001",
    "1100010000110001",
    "1010001010100001",
    "1001000100011001",
    "1000100001100101",
    "1010000001010011"
  ],
  "nested_tests": {
    "2_codewords": [
      "1000000010001111",
      "1111100000000001"
    ],
    "4_codewords": [
      "1000000010001111",
      "1111100000000001",
      "1000011101000001",
      "1100010000110001"
    ],
    "8_codewords": [
      "1000000010001111",
      "1111100000000001",
      "1000011101000001",
      "1100010000110001",
      "1010001010100001",
      "1001000100011001",
      "1000100001100101",
      "1010000001010011"
    ]
  },
  "encoded_bits": {
    "2": 1,
    "4": 2,
    "8": 3
  },
  "design_rule": "All words have equal length, equal Hamming weight, and identical first/last bits. Only temporal arrangement carries codeword identity.",
  "figure": "static\\images\\books\\digital-life\\ch17-01-codebook.png"
}
```

Figure: `static\images\books\digital-life\ch17-01-codebook.png`


# Stage 2 — Same Receiver, Different Codeword

Each receiver group creates one checkpoint and eight exact forks.

The only deliberate difference between those forks is the temporal codeword.

```json
{
  "groups": 24,
  "radius": 64,
  "hard_radius_capacity": 12481,
  "checkpoint_hash_unique_count": 24,
  "max_capacity_fraction_observed": 0.33426808749298936,
  "saturation_guard": 0.85,
  "canvas_boundary_role": "Experimental truncation boundary only; no boundary interaction is intended in the information-survival protocol.",
  "rows": 960,
  "codewords_per_group": 8,
  "retention_lags": [
    0,
    4,
    8,
    16,
    24
  ],
  "checkpoint_control": "Within each group all eight codewords begin from the same receiver checkpoint, RNG state, and future environmental forcing.",
  "train_test_boundary": "Decoder folds are grouped by receiver group; one checkpoint never appears in both train and test.",
  "feature_csv": "research\\digital-life\\ch17\\ch17-receiver-features.csv"
}
```

The decoder never receives the transmitted bits.


# Stage 3 — Can the Receiver Reveal Which Codeword Was Sent?

The primary decoder is fixed in advance: standardized logistic regression.

A random forest is reported only as a secondary nonlinear diagnostic.

Every held-out fold contains receiver checkpoints absent from training.

```json
{
  "primary_decoder_predeclared": "standardized logistic regression",
  "secondary_decoder": "random forest",
  "cross_validation": "GroupKFold by receiver checkpoint group",
  "results": [
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03159591814810947,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005015171814029898,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020131243348847278,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 4,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.062382379446441205,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 4,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834727,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020275412630502608,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 4,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020275412630502608,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 8,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0013096289721030857,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.012367681043545325,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 8,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4166666666666667,
      "secondary_decoder_mi_bits": 0.020131243348847278,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 8,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834727,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.375,
      "secondary_decoder_mi_bits": 0.045902532833148865,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 16,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03159591814810947,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.375,
      "secondary_decoder_mi_bits": 0.04694410794048544,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 16,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0013096289721030857,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0014580808896303091,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 16,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4166666666666667,
      "secondary_decoder_mi_bits": 0.020275412630502608,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          16,
          8
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 24,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.011320505517606903,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 24,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.375,
      "primary_decoder_mi_bits": 0.04556599707503506,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "n_classes": 2,
      "encoded_bits": 1.0,
      "chance_accuracy": 0.5,
      "lag": 24,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.3333333333333333,
      "secondary_decoder_mi_bits": 0.0823355921058051,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 0,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.05117641917593702,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.04478931956274361,
      "primary_confusion_matrix": [
        [
          5,
          8,
          6,
          5
        ],
        [
          6,
          7,
          5,
          6
        ],
        [
          2,
          6,
          9,
          7
        ],
        [
          8,
          7,
          5,
          4
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 0,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.06372348319836774,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.04193962281300724,
      "primary_confusion_matrix": [
        [
          9,
          7,
          4,
          4
        ],
        [
          9,
          3,
          5,
          7
        ],
        [
          9,
          2,
          5,
          8
        ],
        [
          6,
          2,
          8,
          8
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 0,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.25,
      "primary_decoder_mi_bits": 0.03181117419407736,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.3229166666666667,
      "secondary_decoder_mi_bits": 0.0975106069117379,
      "primary_confusion_matrix": [
        [
          8,
          7,
          5,
          4
        ],
        [
          10,
          3,
          6,
          5
        ],
        [
          7,
          5,
          8,
          4
        ],
        [
          6,
          7,
          6,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 4,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.033855624588275776,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.2604166666666667,
      "secondary_decoder_mi_bits": 0.015722870866515283,
      "primary_confusion_matrix": [
        [
          7,
          5,
          6,
          6
        ],
        [
          6,
          6,
          5,
          7
        ],
        [
          5,
          9,
          7,
          3
        ],
        [
          8,
          5,
          6,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 4,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.22916666666666666,
      "primary_decoder_mi_bits": 0.014736058246785352,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.03751471373400033,
      "primary_confusion_matrix": [
        [
          6,
          9,
          5,
          4
        ],
        [
          8,
          6,
          6,
          4
        ],
        [
          9,
          6,
          5,
          4
        ],
        [
          7,
          6,
          6,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 4,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.03672954775346489,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.2604166666666667,
      "secondary_decoder_mi_bits": 0.028547065277464125,
      "primary_confusion_matrix": [
        [
          7,
          4,
          6,
          7
        ],
        [
          5,
          8,
          6,
          5
        ],
        [
          4,
          9,
          6,
          5
        ],
        [
          8,
          7,
          5,
          4
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 8,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.21875,
      "primary_decoder_mi_bits": 0.07304610010998704,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.23958333333333334,
      "secondary_decoder_mi_bits": 0.044906061886664274,
      "primary_confusion_matrix": [
        [
          5,
          12,
          5,
          2
        ],
        [
          7,
          4,
          7,
          6
        ],
        [
          3,
          7,
          8,
          6
        ],
        [
          4,
          8,
          8,
          4
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 8,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2916666666666667,
      "primary_decoder_mi_bits": 0.08408234603270102,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.22916666666666666,
      "secondary_decoder_mi_bits": 0.050810516806130177,
      "primary_confusion_matrix": [
        [
          4,
          9,
          5,
          6
        ],
        [
          6,
          9,
          2,
          7
        ],
        [
          4,
          5,
          8,
          7
        ],
        [
          9,
          3,
          5,
          7
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 8,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.0213091012891114,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.04502024416419999,
      "primary_confusion_matrix": [
        [
          6,
          8,
          6,
          4
        ],
        [
          7,
          7,
          7,
          3
        ],
        [
          5,
          6,
          7,
          6
        ],
        [
          8,
          5,
          6,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 16,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.16666666666666666,
      "primary_decoder_mi_bits": 0.08739146124888603,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.25,
      "secondary_decoder_mi_bits": 0.04618463297595112,
      "primary_confusion_matrix": [
        [
          3,
          8,
          8,
          5
        ],
        [
          8,
          2,
          8,
          6
        ],
        [
          7,
          7,
          6,
          4
        ],
        [
          7,
          9,
          3,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 16,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.22916666666666666,
      "primary_decoder_mi_bits": 0.030140499191818524,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.12827540698928838,
      "primary_confusion_matrix": [
        [
          6,
          5,
          8,
          5
        ],
        [
          7,
          2,
          8,
          7
        ],
        [
          4,
          3,
          9,
          8
        ],
        [
          5,
          5,
          9,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 16,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.12309680461531279,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.23958333333333334,
      "secondary_decoder_mi_bits": 0.034087822268976865,
      "primary_confusion_matrix": [
        [
          7,
          9,
          5,
          3
        ],
        [
          5,
          3,
          7,
          9
        ],
        [
          8,
          1,
          10,
          5
        ],
        [
          8,
          7,
          4,
          5
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 24,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.2916666666666667,
      "primary_decoder_mi_bits": 0.0699518446492929,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.2604166666666667,
      "secondary_decoder_mi_bits": 0.07596124243529866,
      "primary_confusion_matrix": [
        [
          5,
          8,
          6,
          5
        ],
        [
          7,
          6,
          3,
          8
        ],
        [
          3,
          5,
          10,
          6
        ],
        [
          6,
          8,
          3,
          7
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 24,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.04987269169132878,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.05560641010931397,
      "primary_confusion_matrix": [
        [
          2,
          6,
          7,
          9
        ],
        [
          6,
          3,
          10,
          5
        ],
        [
          4,
          7,
          7,
          6
        ],
        [
          5,
          5,
          6,
          8
        ]
      ]
    },
    {
      "n_classes": 4,
      "encoded_bits": 2.0,
      "chance_accuracy": 0.25,
      "lag": 24,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.3020833333333333,
      "primary_decoder_mi_bits": 0.04481177056734052,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.25,
      "secondary_decoder_mi_bits": 0.09481564875602248,
      "primary_confusion_matrix": [
        [
          4,
          8,
          6,
          6
        ],
        [
          7,
          8,
          5,
          4
        ],
        [
          5,
          4,
          10,
          5
        ],
        [
          5,
          7,
          5,
          7
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 0,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.13020833333333334,
      "primary_decoder_mi_bits": 0.13108394353780084,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.109375,
      "secondary_decoder_mi_bits": 0.12328747939543377,
      "primary_confusion_matrix": [
        [
          3,
          5,
          2,
          2,
          2,
          4,
          1,
          5
        ],
        [
          2,
          5,
          5,
          3,
          2,
          4,
          1,
          2
        ],
        [
          2,
          4,
          7,
          1,
          4,
          2,
          2,
          2
        ],
        [
          4,
          5,
          3,
          2,
          2,
          2,
          4,
          2
        ],
        [
          0,
          2,
          3,
          3,
          2,
          5,
          4,
          5
        ],
        [
          3,
          3,
          4,
          4,
          4,
          2,
          1,
          3
        ],
        [
          3,
          5,
          2,
          4,
          3,
          2,
          1,
          4
        ],
        [
          4,
          2,
          4,
          3,
          5,
          2,
          1,
          3
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 0,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.32160486702317753,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.27854986597679826,
      "primary_confusion_matrix": [
        [
          7,
          4,
          1,
          3,
          3,
          1,
          4,
          1
        ],
        [
          5,
          2,
          3,
          2,
          2,
          5,
          2,
          3
        ],
        [
          4,
          0,
          3,
          4,
          1,
          4,
          6,
          2
        ],
        [
          3,
          1,
          4,
          4,
          4,
          3,
          0,
          5
        ],
        [
          3,
          2,
          2,
          1,
          8,
          1,
          4,
          3
        ],
        [
          6,
          3,
          2,
          3,
          2,
          2,
          5,
          1
        ],
        [
          2,
          5,
          1,
          1,
          3,
          3,
          9,
          0
        ],
        [
          4,
          1,
          3,
          3,
          1,
          1,
          0,
          11
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 0,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.18229166666666666,
      "primary_decoder_mi_bits": 0.22448462072054043,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.16145833333333334,
      "secondary_decoder_mi_bits": 0.18929271628800703,
      "primary_confusion_matrix": [
        [
          8,
          4,
          2,
          2,
          4,
          1,
          2,
          1
        ],
        [
          3,
          2,
          1,
          2,
          5,
          4,
          3,
          4
        ],
        [
          5,
          2,
          3,
          2,
          3,
          3,
          5,
          1
        ],
        [
          3,
          4,
          3,
          3,
          5,
          3,
          2,
          1
        ],
        [
          3,
          1,
          5,
          4,
          5,
          2,
          2,
          2
        ],
        [
          6,
          5,
          2,
          2,
          2,
          2,
          5,
          0
        ],
        [
          4,
          6,
          1,
          1,
          3,
          5,
          4,
          0
        ],
        [
          2,
          2,
          1,
          4,
          5,
          2,
          0,
          8
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 4,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.09895833333333333,
      "primary_decoder_mi_bits": 0.16097842643270618,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.16145833333333334,
      "secondary_decoder_mi_bits": 0.20371200848798224,
      "primary_confusion_matrix": [
        [
          4,
          3,
          5,
          1,
          3,
          2,
          4,
          2
        ],
        [
          5,
          2,
          3,
          1,
          1,
          3,
          6,
          3
        ],
        [
          3,
          6,
          3,
          0,
          2,
          4,
          3,
          3
        ],
        [
          4,
          2,
          4,
          0,
          1,
          6,
          2,
          5
        ],
        [
          3,
          3,
          4,
          2,
          1,
          1,
          4,
          6
        ],
        [
          5,
          4,
          7,
          0,
          2,
          1,
          2,
          3
        ],
        [
          1,
          2,
          4,
          2,
          0,
          4,
          6,
          5
        ],
        [
          5,
          2,
          6,
          2,
          3,
          2,
          2,
          2
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 4,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.19270833333333334,
      "primary_decoder_mi_bits": 0.19086932496539435,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.15104166666666666,
      "secondary_decoder_mi_bits": 0.2125788720551771,
      "primary_confusion_matrix": [
        [
          7,
          2,
          2,
          2,
          0,
          3,
          5,
          3
        ],
        [
          4,
          2,
          3,
          1,
          3,
          4,
          5,
          2
        ],
        [
          6,
          1,
          2,
          2,
          0,
          6,
          4,
          3
        ],
        [
          7,
          2,
          3,
          2,
          0,
          4,
          3,
          3
        ],
        [
          4,
          2,
          1,
          1,
          2,
          4,
          4,
          6
        ],
        [
          3,
          2,
          3,
          3,
          2,
          6,
          3,
          2
        ],
        [
          2,
          5,
          1,
          3,
          2,
          2,
          7,
          2
        ],
        [
          2,
          4,
          3,
          2,
          1,
          3,
          0,
          9
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 4,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.1375711284532423,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.15625,
      "secondary_decoder_mi_bits": 0.23812737141499263,
      "primary_confusion_matrix": [
        [
          5,
          3,
          4,
          2,
          2,
          2,
          4,
          2
        ],
        [
          3,
          2,
          2,
          2,
          3,
          3,
          5,
          4
        ],
        [
          3,
          5,
          2,
          1,
          3,
          6,
          2,
          2
        ],
        [
          6,
          4,
          3,
          2,
          0,
          5,
          3,
          1
        ],
        [
          2,
          3,
          3,
          1,
          4,
          2,
          4,
          5
        ],
        [
          3,
          3,
          4,
          4,
          2,
          4,
          1,
          3
        ],
        [
          2,
          3,
          2,
          3,
          3,
          4,
          5,
          2
        ],
        [
          3,
          3,
          2,
          2,
          6,
          2,
          1,
          5
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 8,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.125,
      "primary_decoder_mi_bits": 0.21371486544040524,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.1932604836819497,
      "primary_confusion_matrix": [
        [
          2,
          1,
          5,
          1,
          2,
          5,
          3,
          5
        ],
        [
          2,
          0,
          6,
          2,
          3,
          4,
          3,
          4
        ],
        [
          2,
          3,
          6,
          4,
          3,
          2,
          1,
          3
        ],
        [
          5,
          4,
          4,
          0,
          4,
          2,
          2,
          3
        ],
        [
          2,
          1,
          5,
          4,
          2,
          2,
          0,
          8
        ],
        [
          2,
          4,
          2,
          3,
          3,
          5,
          2,
          3
        ],
        [
          1,
          5,
          2,
          4,
          1,
          6,
          2,
          3
        ],
        [
          4,
          1,
          4,
          0,
          4,
          4,
          0,
          7
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 8,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.125,
      "primary_decoder_mi_bits": 0.24345595725853558,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.08854166666666667,
      "secondary_decoder_mi_bits": 0.16786908907585263,
      "primary_confusion_matrix": [
        [
          4,
          5,
          3,
          3,
          3,
          1,
          4,
          1
        ],
        [
          5,
          7,
          0,
          3,
          2,
          2,
          5,
          0
        ],
        [
          2,
          2,
          5,
          1,
          5,
          5,
          4,
          0
        ],
        [
          5,
          1,
          2,
          2,
          2,
          6,
          5,
          1
        ],
        [
          3,
          6,
          9,
          3,
          0,
          1,
          2,
          0
        ],
        [
          2,
          1,
          4,
          2,
          4,
          4,
          5,
          2
        ],
        [
          3,
          5,
          2,
          4,
          1,
          5,
          2,
          2
        ],
        [
          2,
          4,
          5,
          5,
          1,
          4,
          3,
          0
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 8,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.211345496655308,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.2186149260384227,
      "primary_confusion_matrix": [
        [
          5,
          5,
          4,
          2,
          2,
          0,
          3,
          3
        ],
        [
          4,
          0,
          6,
          1,
          2,
          4,
          4,
          3
        ],
        [
          2,
          3,
          5,
          3,
          3,
          3,
          1,
          4
        ],
        [
          4,
          2,
          2,
          2,
          3,
          2,
          5,
          4
        ],
        [
          3,
          2,
          6,
          4,
          3,
          2,
          1,
          3
        ],
        [
          2,
          5,
          2,
          3,
          3,
          7,
          1,
          1
        ],
        [
          1,
          6,
          2,
          3,
          0,
          7,
          4,
          1
        ],
        [
          3,
          3,
          4,
          2,
          4,
          4,
          1,
          3
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 16,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.078125,
      "primary_decoder_mi_bits": 0.16518489228786418,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.08333333333333333,
      "secondary_decoder_mi_bits": 0.2435637964894567,
      "primary_confusion_matrix": [
        [
          4,
          2,
          3,
          2,
          2,
          6,
          1,
          4
        ],
        [
          4,
          1,
          5,
          1,
          3,
          3,
          2,
          5
        ],
        [
          3,
          2,
          3,
          1,
          2,
          3,
          3,
          7
        ],
        [
          3,
          4,
          2,
          1,
          5,
          3,
          2,
          4
        ],
        [
          2,
          3,
          1,
          5,
          2,
          2,
          4,
          5
        ],
        [
          3,
          3,
          4,
          2,
          2,
          1,
          6,
          3
        ],
        [
          4,
          3,
          4,
          6,
          1,
          3,
          2,
          1
        ],
        [
          1,
          3,
          6,
          2,
          3,
          5,
          3,
          1
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 16,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.14583333333333334,
      "primary_decoder_mi_bits": 0.1579516178141817,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.10416666666666667,
      "secondary_decoder_mi_bits": 0.13551813595178927,
      "primary_confusion_matrix": [
        [
          2,
          4,
          2,
          4,
          3,
          2,
          3,
          4
        ],
        [
          2,
          0,
          3,
          4,
          2,
          5,
          4,
          4
        ],
        [
          3,
          1,
          4,
          4,
          5,
          3,
          3,
          1
        ],
        [
          4,
          3,
          3,
          2,
          4,
          2,
          4,
          2
        ],
        [
          2,
          1,
          4,
          1,
          7,
          2,
          4,
          3
        ],
        [
          1,
          1,
          4,
          4,
          4,
          6,
          3,
          1
        ],
        [
          3,
          4,
          1,
          4,
          3,
          2,
          5,
          2
        ],
        [
          4,
          2,
          5,
          3,
          6,
          2,
          0,
          2
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 16,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.11979166666666667,
      "primary_decoder_mi_bits": 0.19299492663265155,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.11458333333333333,
      "secondary_decoder_mi_bits": 0.1819729391842645,
      "primary_confusion_matrix": [
        [
          5,
          4,
          5,
          3,
          1,
          3,
          0,
          3
        ],
        [
          4,
          1,
          3,
          3,
          3,
          4,
          3,
          3
        ],
        [
          3,
          3,
          4,
          1,
          4,
          1,
          3,
          5
        ],
        [
          3,
          4,
          3,
          2,
          2,
          6,
          1,
          3
        ],
        [
          2,
          1,
          4,
          4,
          2,
          2,
          4,
          5
        ],
        [
          1,
          3,
          7,
          4,
          1,
          5,
          2,
          1
        ],
        [
          2,
          5,
          3,
          4,
          2,
          4,
          3,
          1
        ],
        [
          4,
          0,
          7,
          1,
          6,
          3,
          2,
          1
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 24,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.16145833333333334,
      "primary_decoder_mi_bits": 0.18577024309833967,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.09375,
      "secondary_decoder_mi_bits": 0.17107073428858594,
      "primary_confusion_matrix": [
        [
          4,
          2,
          5,
          3,
          2,
          5,
          0,
          3
        ],
        [
          3,
          5,
          0,
          5,
          2,
          4,
          2,
          3
        ],
        [
          4,
          1,
          6,
          3,
          3,
          3,
          2,
          2
        ],
        [
          5,
          2,
          1,
          5,
          3,
          1,
          3,
          4
        ],
        [
          2,
          2,
          3,
          7,
          2,
          1,
          1,
          6
        ],
        [
          5,
          3,
          3,
          3,
          1,
          2,
          3,
          4
        ],
        [
          5,
          5,
          0,
          2,
          3,
          3,
          2,
          4
        ],
        [
          3,
          1,
          6,
          2,
          3,
          2,
          2,
          5
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 24,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.11979166666666667,
      "primary_decoder_mi_bits": 0.1557530791867636,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.09895833333333333,
      "secondary_decoder_mi_bits": 0.21196538180078428,
      "primary_confusion_matrix": [
        [
          1,
          5,
          3,
          3,
          2,
          4,
          3,
          3
        ],
        [
          1,
          2,
          3,
          3,
          2,
          1,
          6,
          6
        ],
        [
          2,
          1,
          2,
          2,
          3,
          5,
          4,
          5
        ],
        [
          1,
          3,
          1,
          3,
          2,
          6,
          3,
          5
        ],
        [
          0,
          4,
          3,
          4,
          2,
          8,
          1,
          2
        ],
        [
          1,
          3,
          5,
          3,
          3,
          2,
          5,
          2
        ],
        [
          0,
          1,
          4,
          5,
          1,
          4,
          4,
          5
        ],
        [
          0,
          5,
          1,
          3,
          2,
          2,
          4,
          7
        ]
      ]
    },
    {
      "n_classes": 8,
      "encoded_bits": 3.0,
      "chance_accuracy": 0.125,
      "lag": 24,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "primary_model": "standardized_logistic_regression",
      "primary_accuracy": 0.13541666666666666,
      "primary_decoder_mi_bits": 0.20319936822552126,
      "secondary_model": "random_forest",
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.15708690117230834,
      "primary_confusion_matrix": [
        [
          3,
          4,
          2,
          2,
          1,
          9,
          1,
          2
        ],
        [
          2,
          2,
          1,
          4,
          2,
          1,
          6,
          6
        ],
        [
          3,
          1,
          4,
          2,
          4,
          4,
          1,
          5
        ],
        [
          3,
          4,
          2,
          5,
          3,
          4,
          2,
          1
        ],
        [
          1,
          1,
          4,
          5,
          1,
          4,
          2,
          6
        ],
        [
          4,
          3,
          2,
          5,
          3,
          3,
          2,
          2
        ],
        [
          2,
          5,
          1,
          7,
          2,
          3,
          2,
          2
        ],
        [
          0,
          4,
          3,
          3,
          5,
          2,
          1,
          6
        ]
      ]
    }
  ]
}
```

Accuracy above chance is evidence of decoder-accessible codeword distinction,
not semantics and not channel capacity.


# Stage 4 — Could the Decoder Be Inventing the Signal?

Two nulls attack the decoding result.

1. Labels are permuted independently inside each receiver group.
2. The no-channel receiver outcome is duplicated across all codeword labels.

```json
{
  "groupwise_label_permutation": {
    "2": {
      "0": {
        "n": 100,
        "mean": 0.49875,
        "std": 0.07469963000057112,
        "q95": 0.6052083333333332,
        "q99": 0.6460416666666668,
        "max": 0.6666666666666666
      },
      "4": {
        "n": 100,
        "mean": 0.48687499999999995,
        "std": 0.07340047825684336,
        "q95": 0.6052083333333332,
        "q99": 0.6666666666666666,
        "max": 0.6666666666666666
      },
      "8": {
        "n": 100,
        "mean": 0.49458333333333343,
        "std": 0.07474609800295041,
        "q95": 0.6052083333333332,
        "q99": 0.6668750000000001,
        "max": 0.6875
      },
      "16": {
        "n": 100,
        "mean": 0.5122916666666666,
        "std": 0.07694779751017354,
        "q95": 0.6458333333333334,
        "q99": 0.6881250000000003,
        "max": 0.75
      },
      "24": {
        "n": 100,
        "mean": 0.5035416666666667,
        "std": 0.07342412703298253,
        "q95": 0.6041666666666666,
        "q99": 0.6472916666666675,
        "max": 0.7916666666666666
      }
    },
    "4": {
      "0": {
        "n": 100,
        "mean": 0.25354166666666667,
        "std": 0.04861850142235521,
        "q95": 0.3229166666666667,
        "q99": 0.34447916666666706,
        "max": 0.4166666666666667
      },
      "4": {
        "n": 100,
        "mean": 0.25322916666666667,
        "std": 0.043418760945970504,
        "q95": 0.3229166666666667,
        "q99": 0.3650000000000002,
        "max": 0.40625
      },
      "8": {
        "n": 100,
        "mean": 0.25031250000000005,
        "std": 0.04459635226581504,
        "q95": 0.3229166666666667,
        "q99": 0.3337500000000002,
        "max": 0.375
      },
      "16": {
        "n": 100,
        "mean": 0.2594791666666667,
        "std": 0.05122405762784818,
        "q95": 0.34375,
        "q99": 0.3545833333333336,
        "max": 0.3958333333333333
      },
      "24": {
        "n": 100,
        "mean": 0.251875,
        "std": 0.04803834189131289,
        "q95": 0.3333333333333333,
        "q99": 0.3542708333333334,
        "max": 0.3645833333333333
      }
    },
    "8": {
      "0": {
        "n": 100,
        "mean": 0.12760416666666669,
        "std": 0.024356964481437336,
        "q95": 0.17213541666666665,
        "q99": 0.1875,
        "max": 0.1875
      },
      "4": {
        "n": 100,
        "mean": 0.1221875,
        "std": 0.021148911926963155,
        "q95": 0.15625,
        "q99": 0.1719791666666667,
        "max": 0.18229166666666666
      },
      "8": {
        "n": 100,
        "mean": 0.12390624999999998,
        "std": 0.024231851295092994,
        "q95": 0.16666666666666666,
        "q99": 0.18239583333333337,
        "max": 0.19270833333333334
      },
      "16": {
        "n": 100,
        "mean": 0.12114583333333333,
        "std": 0.023715023587380212,
        "q95": 0.15625,
        "q99": 0.17723958333333342,
        "max": 0.19270833333333334
      },
      "24": {
        "n": 100,
        "mean": 0.12114583333333334,
        "std": 0.024044455716327715,
        "q95": 0.16145833333333334,
        "q99": 0.1668750000000001,
        "max": 0.1875
      }
    }
  },
  "no_channel": {
    "2": {
      "0": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      }
    },
    "4": {
      "0": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      }
    },
    "8": {
      "0": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      }
    }
  },
  "observed_vs_null": {
    "2:0": {
      "accuracy": 0.4583333333333333,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:4": {
      "accuracy": 0.5833333333333334,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:8": {
      "accuracy": 0.4791666666666667,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:16": {
      "accuracy": 0.3958333333333333,
      "chance": 0.5,
      "null_q95": 0.6458333333333334,
      "beats_null_q95": false
    },
    "2:24": {
      "accuracy": 0.4583333333333333,
      "chance": 0.5,
      "null_q95": 0.6041666666666666,
      "beats_null_q95": false
    },
    "4:0": {
      "accuracy": 0.25,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:4": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:8": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:16": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.34375,
      "beats_null_q95": false
    },
    "4:24": {
      "accuracy": 0.3020833333333333,
      "chance": 0.25,
      "null_q95": 0.3333333333333333,
      "beats_null_q95": false
    },
    "8:0": {
      "accuracy": 0.18229166666666666,
      "chance": 0.125,
      "null_q95": 0.17213541666666665,
      "beats_null_q95": true
    },
    "8:4": {
      "accuracy": 0.15104166666666666,
      "chance": 0.125,
      "null_q95": 0.15625,
      "beats_null_q95": false
    },
    "8:8": {
      "accuracy": 0.15104166666666666,
      "chance": 0.125,
      "null_q95": 0.16666666666666666,
      "beats_null_q95": false
    },
    "8:16": {
      "accuracy": 0.11979166666666667,
      "chance": 0.125,
      "null_q95": 0.15625,
      "beats_null_q95": false
    },
    "8:24": {
      "accuracy": 0.13541666666666666,
      "chance": 0.125,
      "null_q95": 0.16145833333333334,
      "beats_null_q95": false
    }
  }
}
```

A surviving claim requires the primary decoder to beat the 95th percentile of
the grouped label-permutation null.


# Stage 5 — How Long Does the Difference Survive?

Transmission ends before every positive retention lag.

The decoder is then asked to identify the original codeword from the receiver.

```json
{
  "retention_curves": {
    "2": [
      {
        "lag": 0,
        "accuracy": 0.4583333333333333,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "survives_null": false,
        "decoder_mi_bits": 0.005015171814029898
      },
      {
        "lag": 4,
        "accuracy": 0.5833333333333334,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "survives_null": false,
        "decoder_mi_bits": 0.020131243348847278
      },
      {
        "lag": 8,
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "survives_null": false,
        "decoder_mi_bits": 0.0012548838431834727
      },
      {
        "lag": 16,
        "accuracy": 0.3958333333333333,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "survives_null": false,
        "decoder_mi_bits": 0.03205907716826763
      },
      {
        "lag": 24,
        "accuracy": 0.4583333333333333,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "survives_null": false,
        "decoder_mi_bits": 0.005159341095685475
      }
    ],
    "4": [
      {
        "lag": 0,
        "accuracy": 0.25,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "survives_null": false,
        "decoder_mi_bits": 0.03181117419407736
      },
      {
        "lag": 4,
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "survives_null": false,
        "decoder_mi_bits": 0.03672954775346489
      },
      {
        "lag": 8,
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "survives_null": false,
        "decoder_mi_bits": 0.0213091012891114
      },
      {
        "lag": 16,
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "null_q95": 0.34375,
        "survives_null": false,
        "decoder_mi_bits": 0.12309680461531279
      },
      {
        "lag": 24,
        "accuracy": 0.3020833333333333,
        "chance": 0.25,
        "null_q95": 0.3333333333333333,
        "survives_null": false,
        "decoder_mi_bits": 0.04481177056734052
      }
    ],
    "8": [
      {
        "lag": 0,
        "accuracy": 0.18229166666666666,
        "chance": 0.125,
        "null_q95": 0.17213541666666665,
        "survives_null": true,
        "decoder_mi_bits": 0.22448462072054043
      },
      {
        "lag": 4,
        "accuracy": 0.15104166666666666,
        "chance": 0.125,
        "null_q95": 0.15625,
        "survives_null": false,
        "decoder_mi_bits": 0.1375711284532423
      },
      {
        "lag": 8,
        "accuracy": 0.15104166666666666,
        "chance": 0.125,
        "null_q95": 0.16666666666666666,
        "survives_null": false,
        "decoder_mi_bits": 0.211345496655308
      },
      {
        "lag": 16,
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "null_q95": 0.15625,
        "survives_null": false,
        "decoder_mi_bits": 0.19299492663265155
      },
      {
        "lag": 24,
        "accuracy": 0.13541666666666666,
        "chance": 0.125,
        "null_q95": 0.16145833333333334,
        "survives_null": false,
        "decoder_mi_bits": 0.20319936822552126
      }
    ]
  },
  "figure": "static\\images\\books\\digital-life\\ch17-05-retention.png",
  "interpretation_boundary": "This measures decoder-accessible codeword identity after the channel is off. It is not a Shannon capacity estimate."
}
```

Figure: `static\images\books\digital-life\ch17-05-retention.png`


# Stage 6 — Where Does Recoverable Information Live?

The decoder is split into receiver-only measurement families.

```json
{
  "eight_codeword_feature_comparison": {
    "0": {
      "morphology": {
        "primary_accuracy": 0.13020833333333334,
        "primary_decoder_mi_bits": 0.13108394353780084,
        "secondary_accuracy": 0.109375
      },
      "recent_growth": {
        "primary_accuracy": 0.23958333333333334,
        "primary_decoder_mi_bits": 0.32160486702317753,
        "secondary_accuracy": 0.1875
      },
      "combined": {
        "primary_accuracy": 0.18229166666666666,
        "primary_decoder_mi_bits": 0.22448462072054043,
        "secondary_accuracy": 0.16145833333333334
      }
    },
    "4": {
      "morphology": {
        "primary_accuracy": 0.09895833333333333,
        "primary_decoder_mi_bits": 0.16097842643270618,
        "secondary_accuracy": 0.16145833333333334
      },
      "recent_growth": {
        "primary_accuracy": 0.19270833333333334,
        "primary_decoder_mi_bits": 0.19086932496539435,
        "secondary_accuracy": 0.15104166666666666
      },
      "combined": {
        "primary_accuracy": 0.15104166666666666,
        "primary_decoder_mi_bits": 0.1375711284532423,
        "secondary_accuracy": 0.15625
      }
    },
    "8": {
      "morphology": {
        "primary_accuracy": 0.125,
        "primary_decoder_mi_bits": 0.21371486544040524,
        "secondary_accuracy": 0.125
      },
      "recent_growth": {
        "primary_accuracy": 0.125,
        "primary_decoder_mi_bits": 0.24345595725853558,
        "secondary_accuracy": 0.08854166666666667
      },
      "combined": {
        "primary_accuracy": 0.15104166666666666,
        "primary_decoder_mi_bits": 0.211345496655308,
        "secondary_accuracy": 0.125
      }
    },
    "16": {
      "morphology": {
        "primary_accuracy": 0.078125,
        "primary_decoder_mi_bits": 0.16518489228786418,
        "secondary_accuracy": 0.08333333333333333
      },
      "recent_growth": {
        "primary_accuracy": 0.14583333333333334,
        "primary_decoder_mi_bits": 0.1579516178141817,
        "secondary_accuracy": 0.10416666666666667
      },
      "combined": {
        "primary_accuracy": 0.11979166666666667,
        "primary_decoder_mi_bits": 0.19299492663265155,
        "secondary_accuracy": 0.11458333333333333
      }
    },
    "24": {
      "morphology": {
        "primary_accuracy": 0.16145833333333334,
        "primary_decoder_mi_bits": 0.18577024309833967,
        "secondary_accuracy": 0.09375
      },
      "recent_growth": {
        "primary_accuracy": 0.11979166666666667,
        "primary_decoder_mi_bits": 0.1557530791867636,
        "secondary_accuracy": 0.09895833333333333
      },
      "combined": {
        "primary_accuracy": 0.13541666666666666,
        "primary_decoder_mi_bits": 0.20319936822552126,
        "secondary_accuracy": 0.125
      }
    }
  },
  "feature_definitions": {
    "morphology": "current occupied-cell geometry only; no birth-time history",
    "recent_growth": "recent receiver attachment and population window only",
    "combined": "morphology + recent growth"
  },
  "figure": "static\\images\\books\\digital-life\\ch17-06-feature-location.png"
}
```

Figure: `static\images\books\digital-life\ch17-06-feature-location.png`

Birth-time metadata is deliberately excluded from the morphology features.


# Stage 7 — Experimental Verdict

**Verdict: `NOT_SUPPORTED_AS_TESTED`**

> This protocol did not establish reliable receiver-only recovery of constant-weight temporal codeword identity.

```json
{
  "verdict": "NOT_SUPPORTED_AS_TESTED",
  "bounded_claim": "This protocol did not establish reliable receiver-only recovery of constant-weight temporal codeword identity.",
  "predeclared_threshold": "primary combined accuracy > grouped permutation q95 AND at least 0.10 absolute accuracy above chance",
  "tests": {
    "2": {
      "0": {
        "accuracy": 0.4583333333333333,
        "chance": 0.5,
        "margin_above_chance": -0.041666666666666685,
        "null_q95": 0.6052083333333332,
        "passes_predeclared_threshold": false
      },
      "4": {
        "accuracy": 0.5833333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.08333333333333337,
        "null_q95": 0.6052083333333332,
        "passes_predeclared_threshold": false
      },
      "8": {
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.020833333333333315,
        "null_q95": 0.6052083333333332,
        "passes_predeclared_threshold": false
      },
      "16": {
        "accuracy": 0.3958333333333333,
        "chance": 0.5,
        "margin_above_chance": -0.10416666666666669,
        "null_q95": 0.6458333333333334,
        "passes_predeclared_threshold": false
      },
      "24": {
        "accuracy": 0.4583333333333333,
        "chance": 0.5,
        "margin_above_chance": -0.041666666666666685,
        "null_q95": 0.6041666666666666,
        "passes_predeclared_threshold": false
      }
    },
    "4": {
      "0": {
        "accuracy": 0.25,
        "chance": 0.25,
        "margin_above_chance": 0.0,
        "null_q95": 0.3229166666666667,
        "passes_predeclared_threshold": false
      },
      "4": {
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "margin_above_chance": 0.010416666666666685,
        "null_q95": 0.3229166666666667,
        "passes_predeclared_threshold": false
      },
      "8": {
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "margin_above_chance": 0.010416666666666685,
        "null_q95": 0.3229166666666667,
        "passes_predeclared_threshold": false
      },
      "16": {
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "margin_above_chance": 0.010416666666666685,
        "null_q95": 0.34375,
        "passes_predeclared_threshold": false
      },
      "24": {
        "accuracy": 0.3020833333333333,
        "chance": 0.25,
        "margin_above_chance": 0.052083333333333315,
        "null_q95": 0.3333333333333333,
        "passes_predeclared_threshold": false
      }
    },
    "8": {
      "0": {
        "accuracy": 0.18229166666666666,
        "chance": 0.125,
        "margin_above_chance": 0.05729166666666666,
        "null_q95": 0.17213541666666665,
        "passes_predeclared_threshold": false
      },
      "4": {
        "accuracy": 0.15104166666666666,
        "chance": 0.125,
        "margin_above_chance": 0.026041666666666657,
        "null_q95": 0.15625,
        "passes_predeclared_threshold": false
      },
      "8": {
        "accuracy": 0.15104166666666666,
        "chance": 0.125,
        "margin_above_chance": 0.026041666666666657,
        "null_q95": 0.16666666666666666,
        "passes_predeclared_threshold": false
      },
      "16": {
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "margin_above_chance": -0.005208333333333329,
        "null_q95": 0.15625,
        "passes_predeclared_threshold": false
      },
      "24": {
        "accuracy": 0.13541666666666666,
        "chance": 0.125,
        "margin_above_chance": 0.010416666666666657,
        "null_q95": 0.16145833333333334,
        "passes_predeclared_threshold": false
      }
    }
  },
  "largest_recoverable_nested_codebook_by_lag": {
    "0": 0,
    "4": 0,
    "8": 0,
    "16": 0,
    "24": 0
  },
  "explicit_nonclaims": [
    "language",
    "semantics",
    "meaning",
    "understanding",
    "sender identity",
    "coordination",
    "learning",
    "intelligence",
    "agency",
    "individuality",
    "selfhood",
    "life",
    "Shannon channel capacity"
  ],
  "evidence_ledger": [
    {
      "claim": "Distinct constant-weight temporal inputs can alter receiver state differently",
      "status": "FAILED"
    },
    {
      "claim": "Codeword identity is recoverable after transmission has ended",
      "status": "FAILED"
    },
    {
      "claim": "The receiver understands message meaning",
      "status": "UNTESTED"
    },
    {
      "claim": "Sender identity survives the channel",
      "status": "UNTESTED"
    },
    {
      "claim": "Shannon channel capacity has been measured",
      "status": "UNTESTED"
    }
  ]
}
```
