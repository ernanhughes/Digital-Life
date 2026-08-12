# Chapter 17 — What Survives the Channel? v2 Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-information-survival-v2",
  "schema_version": 2,
  "profile": "quick",
  "profile_config": {
    "groups": 24,
    "radius": 64,
    "warmup_steps": 14,
    "codeword_length": 16,
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
  "started_at_unix": 1786501270.991578,
  "scientific_boundary": "Exploratory boundary-finding for receiver-side temporal codeword distinction. No semantics, sender identity, coordination, agency, individuality, life, or Shannon-capacity claim.",
  "primary_headline_measurement": "raw combined receiver features",
  "paired_delta_measurement_role": "diagnostic only",
  "cross_validation_boundary": "GroupKFold by receiver checkpoint group",
  "matplotlib_backend": "Agg",
  "finished_at_unix": 1786501468.6088636,
  "stage0_reproducibility_passed": true,
  "final_verdict": "TEMPORAL_INFORMATION_BOUNDARY_LOCATED",
  "first_supported_level": "L1",
  "first_supported_elapsed_step": 8,
  "accuracy_figure": "static\\images\\books\\digital-life\\ch17-v2-05-information-boundary.png"
}
```

# Stage 0 — Freeze the Substrate

```json
{
  "canonical_rng_traversal": "sorted(frontier)",
  "repeat_from_identical_state_exact": true,
  "morphology_hash_a": "64f495acbf56a8f839800c44",
  "morphology_hash_b": "64f495acbf56a8f839800c44"
}
```


# Stage 1 — Start With the Simplest Distinction

The ladder does not begin with eight hard codewords.

It begins with one early pulse versus one late pulse and increases difficulty
only after simpler distinctions are measured.

```json
{
  "levels": [
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        1,
        1
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 2,
      "pairwise_hamming_mean": 2.0,
      "pairwise_hamming_max": 2,
      "codewords": [
        "0010000000000000",
        "0000000000000100"
      ],
      "interpretation": "Same pulse count and energy; only coarse pulse timing differs."
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        2,
        2
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 4,
      "pairwise_hamming_mean": 4.0,
      "pairwise_hamming_max": 4,
      "codewords": [
        "0011000000000000",
        "0000000000001100"
      ],
      "interpretation": "Same two adjacent pulses; only burst location differs."
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        4,
        4
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 4,
      "pairwise_hamming_mean": 4.0,
      "pairwise_hamming_max": 4,
      "codewords": [
        "0011110000000000",
        "0010010010010000"
      ],
      "interpretation": "Same four pulses; temporal concentration differs strongly."
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        6,
        6
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 8,
      "pairwise_hamming_mean": 8.0,
      "pairwise_hamming_max": 8,
      "codewords": [
        "1000000010001111",
        "1111100000000001"
      ],
      "interpretation": "Same length, weight, first bit and last bit; finer chronology differs."
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_codewords": 4,
      "encoded_bits": 2.0,
      "length": 16,
      "weight_each": [
        6,
        6,
        6,
        6
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 6,
      "pairwise_hamming_mean": 7.333333333333333,
      "pairwise_hamming_max": 8,
      "codewords": [
        "1000000010001111",
        "1111100000000001",
        "1000011101000001",
        "1100010000110001"
      ],
      "interpretation": "Two encoded bits in a constant-weight temporal codebook."
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_codewords": 8,
      "encoded_bits": 3.0,
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
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 6,
      "pairwise_hamming_mean": 6.428571428571429,
      "pairwise_hamming_max": 8,
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
      "interpretation": "Three encoded bits in the hard constant-weight codebook from v1."
    }
  ],
  "figure": "static\\images\\books\\digital-life\\ch17-v2-01-information-ladder.png"
}
```

Figure: `static\images\books\digital-life\ch17-v2-01-information-ladder.png`


# Stage 2 — During the Message and After It

```json
{
  "levels": [
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "groups": 24,
      "n_codewords": 2,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.3358705231952568,
      "saturation_guard": 0.85
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "groups": 24,
      "n_codewords": 2,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.3440429452768208,
      "saturation_guard": 0.85
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "groups": 24,
      "n_codewords": 2,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.33891515102956493,
      "saturation_guard": 0.85
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "groups": 24,
      "n_codewords": 2,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.33282589536094864,
      "saturation_guard": 0.85
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "groups": 24,
      "n_codewords": 4,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.33579040141014344,
      "saturation_guard": 0.85
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "groups": 24,
      "n_codewords": 8,
      "observation_steps": [
        4,
        8,
        12,
        16,
        20,
        24,
        32,
        40
      ],
      "max_capacity_fraction_observed": 0.34580562454931496,
      "saturation_guard": 0.85
    }
  ],
  "measurement_schedule": {
    "during_transmission": [
      4,
      8,
      12
    ],
    "end_of_transmission": [
      16
    ],
    "after_transmission": [
      0,
      4,
      8,
      16,
      24
    ]
  },
  "checkpoint_control": "Within each level and receiver group all codewords begin from the same checkpoint, RNG state, and future environmental forcing.",
  "raw_and_paired_delta_features": "Raw receiver features are primary. Matched no-channel feature deltas are reported as a mechanistic diagnostic, not the headline decoder."
}
```


# Stage 3 — Where Does Recoverability First Appear?

The primary headline remains raw receiver `combined` features.

`delta_combined` subtracts the matched no-channel receiver and is reported only
as a causal-localization diagnostic.

```json
{
  "primary_headline_feature_set": "combined",
  "paired_delta_feature_set": "delta_combined",
  "primary_decoder": "standardized logistic regression",
  "secondary_decoder": "random forest",
  "cross_validation": "GroupKFold by receiver checkpoint group",
  "results": [
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005159341095685478,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011820677639932345,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012726158699361643,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011320505517606903,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.7916666666666666,
      "primary_decoder_mi_bits": 0.38093009090978813,
      "secondary_accuracy": 1.0,
      "secondary_decoder_mi_bits": 1.0,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4166666666666667,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.625,
      "primary_decoder_mi_bits": 0.04556599707503506,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011320505517606903,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.75,
      "primary_decoder_mi_bits": 0.3112781244591328,
      "secondary_accuracy": 1.0,
      "secondary_decoder_mi_bits": 1.0,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03302877414247969,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005159341095685475,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.7083333333333334,
      "primary_decoder_mi_bits": 0.24835048781787405,
      "secondary_accuracy": 0.9791666666666666,
      "secondary_decoder_mi_bits": 0.8738061515195756,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005015171814029898,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3541666666666667,
      "primary_decoder_mi_bits": 0.06333279534523893,
      "secondary_accuracy": 0.3541666666666667,
      "secondary_decoder_mi_bits": 0.06333279534523893,
      "primary_confusion_matrix": [
        [
          7,
          17
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020131243348847278,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.04562564681741727,
      "secondary_accuracy": 0.9791666666666666,
      "secondary_decoder_mi_bits": 0.8738061515195756,
      "primary_confusion_matrix": [
        [
          8,
          16
        ],
        [
          3,
          21
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005015171814029898,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005159341095685478,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0015865803549901993,
      "secondary_accuracy": 0.75,
      "secondary_decoder_mi_bits": 0.195709628799731,
      "primary_confusion_matrix": [
        [
          6,
          18
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0013096289721030857,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005050449860393498,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834727,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.0056465979743246415,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          7,
          17
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.3333333333333333,
      "secondary_decoder_mi_bits": 0.08170416594551039,
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
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.062382379446441205,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020720839623908215,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03205907716826763,
      "primary_confusion_matrix": [
        [
          8,
          16
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4166666666666667,
      "primary_decoder_mi_bits": 0.020275412630502608,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.011320505517606903,
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
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.01436752710326896,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0013096289721030857,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          19,
          5
        ]
      ]
    },
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005050449860393498,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005050449860393498,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.06333279534523892,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          17,
          7
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020720839623908215,
      "secondary_accuracy": 0.6875,
      "secondary_decoder_mi_bits": 0.11523066906964193,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6666666666666666,
      "primary_decoder_mi_bits": 0.0823355921058051,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.022722393499346537,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.875,
      "primary_decoder_mi_bits": 0.5487949406953987,
      "secondary_accuracy": 0.9583333333333334,
      "secondary_decoder_mi_bits": 0.7880764030341532,
      "primary_confusion_matrix": [
        [
          18,
          6
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005050449860393498,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0013096289721030857,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.045902532833148865,
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
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03205907716826763,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.7291666666666666,
      "primary_decoder_mi_bits": 0.2790633713514752,
      "secondary_accuracy": 0.9583333333333334,
      "secondary_decoder_mi_bits": 0.7880764030341532,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020275412630502608,
      "secondary_accuracy": 0.6458333333333334,
      "secondary_decoder_mi_bits": 0.062382379446441205,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.0050504498603934946,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.04556599707503506,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6666666666666666,
      "primary_decoder_mi_bits": 0.1908745046211096,
      "secondary_accuracy": 1.0,
      "secondary_decoder_mi_bits": 1.0,
      "primary_confusion_matrix": [
        [
          8,
          16
        ],
        [
          0,
          24
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0013096289721030874,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020275412630502608,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.9791666666666666,
      "secondary_decoder_mi_bits": 0.8738061515195756,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.005050449860393498,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834727,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834727,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834727,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005015171814029898,
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
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0013096289721030874,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03302877414247969,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.0050504498603934946,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005159341095685475,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.6875,
      "secondary_decoder_mi_bits": 0.1093841973628604,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03302877414247969,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011820677639932345,
      "primary_confusion_matrix": [
        [
          17,
          7
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020275412630502608,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020720839623908215,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03159591814810947,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.045902532833148865,
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
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.01148240682601498,
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
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012726158699361643,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.04556599707503506,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
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
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03159591814810947,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005159341095685475,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03159591814810947,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.625,
      "primary_decoder_mi_bits": 0.04694410794048544,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03302877414247969,
      "primary_confusion_matrix": [
        [
          17,
          7
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.021509354214297588,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011320505517606903,
      "primary_confusion_matrix": [
        [
          17,
          7
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005015171814029898,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020720839623908215,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.06333279534523892,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.02711899660771097,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.06333279534523892,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020131243348847278,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03205907716826763,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6875,
      "primary_decoder_mi_bits": 0.10584334459644848,
      "secondary_accuracy": 0.6875,
      "secondary_decoder_mi_bits": 0.10584334459644848,
      "primary_confusion_matrix": [
        [
          18,
          6
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.062382379446441205,
      "secondary_accuracy": 0.75,
      "secondary_decoder_mi_bits": 0.19041016049656256,
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
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005015171814029898,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005050449860393498,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.062382379446441205,
      "secondary_accuracy": 0.6666666666666666,
      "secondary_decoder_mi_bits": 0.08170416594551039,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6666666666666666,
      "primary_decoder_mi_bits": 0.08429531609600996,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005015171814029898,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          6,
          18
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.75,
      "secondary_decoder_mi_bits": 0.19041016049656256,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0013096289721030874,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3333333333333333,
      "primary_decoder_mi_bits": 0.08779915576025464,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          19,
          5
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005159341095685475,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005015171814029898,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.045902532833148865,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012726158699361643,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03159591814810947,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0013096289721030874,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03302877414247969,
      "secondary_accuracy": 0.375,
      "secondary_decoder_mi_bits": 0.045902532833148865,
      "primary_confusion_matrix": [
        [
          7,
          17
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020720839623908215,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0015865803549901976,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.4166666666666667,
      "secondary_decoder_mi_bits": 0.020275412630502608,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.01148240682601498,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.01148240682601498,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005351707572143805,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0013096289721030874,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834727,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.6458333333333334,
      "secondary_decoder_mi_bits": 0.062382379446441205,
      "primary_confusion_matrix": [
        [
          14,
          10
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.005159341095685475,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03302877414247969,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03159591814810947,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03159591814810947,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.034602817664252716,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.01148240682601498,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          9,
          15
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.0050504498603934946,
      "secondary_accuracy": 0.5833333333333334,
      "secondary_decoder_mi_bits": 0.020275412630502608,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6458333333333334,
      "primary_decoder_mi_bits": 0.062382379446441205,
      "secondary_accuracy": 0.6041666666666666,
      "secondary_decoder_mi_bits": 0.03159591814810947,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4583333333333333,
      "primary_decoder_mi_bits": 0.0050504498603934946,
      "secondary_accuracy": 0.4375,
      "secondary_decoder_mi_bits": 0.01148240682601498,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6041666666666666,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.04694410794048544,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.625,
      "primary_decoder_mi_bits": 0.04694410794048544,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          7,
          17
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.6875,
      "primary_decoder_mi_bits": 0.1041671462912413,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012726158699361643,
      "primary_confusion_matrix": [
        [
          17,
          7
        ],
        [
          8,
          16
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.3958333333333333,
      "secondary_decoder_mi_bits": 0.03205907716826763,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_accuracy": 0.625,
      "secondary_decoder_mi_bits": 0.051660986889779284,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4166666666666667,
      "primary_decoder_mi_bits": 0.020275412630502608,
      "secondary_accuracy": 0.4791666666666667,
      "secondary_decoder_mi_bits": 0.0012548838431834745,
      "primary_confusion_matrix": [
        [
          11,
          13
        ],
        [
          15,
          9
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5208333333333334,
      "secondary_decoder_mi_bits": 0.0013693754970769047,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012726158699361643,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012548838431834727,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011320505517606903,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0014580808896303091,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.0050504498603934946,
      "primary_confusion_matrix": [
        [
          16,
          8
        ],
        [
          17,
          7
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5416666666666666,
      "primary_decoder_mi_bits": 0.0050504498603934946,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.011320505517606903,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          10,
          14
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5625,
      "primary_decoder_mi_bits": 0.01148240682601498,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          15,
          9
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5208333333333334,
      "primary_decoder_mi_bits": 0.0012548838431834745,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005351707572143805,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          11,
          13
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005050449860393498,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4791666666666667,
      "primary_decoder_mi_bits": 0.0012726158699361643,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          13,
          11
        ],
        [
          14,
          10
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.3958333333333333,
      "secondary_decoder_mi_bits": 0.03159591814810947,
      "primary_confusion_matrix": [
        [
          10,
          14
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5,
      "primary_decoder_mi_bits": 0.0,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005159341095685475,
      "primary_confusion_matrix": [
        [
          12,
          12
        ],
        [
          12,
          12
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4375,
      "primary_decoder_mi_bits": 0.011320505517606903,
      "secondary_accuracy": 0.5416666666666666,
      "secondary_decoder_mi_bits": 0.005351707572143805,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.5833333333333334,
      "primary_decoder_mi_bits": 0.020131243348847278,
      "secondary_accuracy": 0.5625,
      "secondary_decoder_mi_bits": 0.01148240682601498,
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
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.4166666666666667,
      "primary_decoder_mi_bits": 0.020275412630502615,
      "secondary_accuracy": 0.4583333333333333,
      "secondary_decoder_mi_bits": 0.005159341095685478,
      "primary_confusion_matrix": [
        [
          9,
          15
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_classes": 2,
      "encoded_bits": 1.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 48,
      "groups": 24,
      "chance_accuracy": 0.5,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.03205907716826763,
      "secondary_accuracy": 0.5,
      "secondary_decoder_mi_bits": 0.0,
      "primary_confusion_matrix": [
        [
          8,
          16
        ],
        [
          13,
          11
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.2916666666666667,
      "primary_decoder_mi_bits": 0.1412287917424625,
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.03610250496394422,
      "primary_confusion_matrix": [
        [
          5,
          12,
          2,
          5
        ],
        [
          9,
          8,
          4,
          3
        ],
        [
          5,
          12,
          2,
          5
        ],
        [
          1,
          9,
          1,
          13
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3125,
      "primary_decoder_mi_bits": 0.028456583367270263,
      "secondary_accuracy": 0.3125,
      "secondary_decoder_mi_bits": 0.02843806842874624,
      "primary_confusion_matrix": [
        [
          7,
          5,
          6,
          6
        ],
        [
          4,
          7,
          5,
          8
        ],
        [
          7,
          5,
          6,
          6
        ],
        [
          4,
          5,
          5,
          10
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.2916666666666667,
      "primary_decoder_mi_bits": 0.0349980978868983,
      "secondary_accuracy": 0.25,
      "secondary_decoder_mi_bits": 0.0756302582634346,
      "primary_confusion_matrix": [
        [
          5,
          8,
          5,
          6
        ],
        [
          7,
          8,
          4,
          5
        ],
        [
          5,
          8,
          5,
          6
        ],
        [
          6,
          4,
          4,
          10
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3125,
      "primary_decoder_mi_bits": 0.0882598259705679,
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.03415814650221259,
      "primary_confusion_matrix": [
        [
          3,
          9,
          4,
          8
        ],
        [
          4,
          10,
          5,
          5
        ],
        [
          3,
          9,
          4,
          8
        ],
        [
          1,
          3,
          7,
          13
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.045963496204398435,
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.11840154891219656,
      "primary_confusion_matrix": [
        [
          7,
          6,
          3,
          8
        ],
        [
          5,
          4,
          5,
          10
        ],
        [
          7,
          6,
          4,
          7
        ],
        [
          4,
          9,
          6,
          5
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3854166666666667,
      "primary_decoder_mi_bits": 0.1375458290393034,
      "secondary_accuracy": 0.3958333333333333,
      "secondary_decoder_mi_bits": 0.11120155900543194,
      "primary_confusion_matrix": [
        [
          5,
          6,
          8,
          5
        ],
        [
          3,
          8,
          4,
          9
        ],
        [
          6,
          3,
          11,
          4
        ],
        [
          4,
          5,
          2,
          13
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.06733140583608554,
      "secondary_accuracy": 0.3125,
      "secondary_decoder_mi_bits": 0.064229003876409,
      "primary_confusion_matrix": [
        [
          7,
          8,
          6,
          3
        ],
        [
          2,
          7,
          6,
          9
        ],
        [
          5,
          9,
          5,
          5
        ],
        [
          2,
          11,
          5,
          6
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3020833333333333,
      "primary_decoder_mi_bits": 0.04877542511458226,
      "secondary_accuracy": 0.2916666666666667,
      "secondary_decoder_mi_bits": 0.09935031721005264,
      "primary_confusion_matrix": [
        [
          6,
          4,
          8,
          6
        ],
        [
          6,
          3,
          6,
          9
        ],
        [
          4,
          3,
          12,
          5
        ],
        [
          4,
          6,
          6,
          8
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.28125,
      "primary_decoder_mi_bits": 0.06241720105556088,
      "secondary_accuracy": 0.3229166666666667,
      "secondary_decoder_mi_bits": 0.049539833453472834,
      "primary_confusion_matrix": [
        [
          5,
          5,
          3,
          11
        ],
        [
          5,
          7,
          3,
          9
        ],
        [
          7,
          2,
          8,
          7
        ],
        [
          6,
          6,
          5,
          7
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3854166666666667,
      "primary_decoder_mi_bits": 0.10812726262202128,
      "secondary_accuracy": 0.375,
      "secondary_decoder_mi_bits": 0.11369300101601865,
      "primary_confusion_matrix": [
        [
          7,
          4,
          7,
          6
        ],
        [
          6,
          6,
          6,
          6
        ],
        [
          3,
          3,
          15,
          3
        ],
        [
          5,
          6,
          4,
          9
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.10366861603072552,
      "secondary_accuracy": 0.40625,
      "secondary_decoder_mi_bits": 0.15474090854500372,
      "primary_confusion_matrix": [
        [
          7,
          6,
          5,
          6
        ],
        [
          3,
          9,
          5,
          7
        ],
        [
          2,
          7,
          12,
          3
        ],
        [
          4,
          6,
          4,
          10
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.34375,
      "primary_decoder_mi_bits": 0.10808205764905336,
      "secondary_accuracy": 0.3229166666666667,
      "secondary_decoder_mi_bits": 0.09463187336060719,
      "primary_confusion_matrix": [
        [
          10,
          2,
          7,
          5
        ],
        [
          3,
          5,
          6,
          10
        ],
        [
          5,
          6,
          10,
          3
        ],
        [
          8,
          4,
          4,
          8
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.25,
      "primary_decoder_mi_bits": 0.07229086832351153,
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.11809788409616444,
      "primary_confusion_matrix": [
        [
          7,
          6,
          8,
          3
        ],
        [
          8,
          3,
          6,
          7
        ],
        [
          6,
          6,
          5,
          7
        ],
        [
          4,
          8,
          3,
          9
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.28125,
      "primary_decoder_mi_bits": 0.054688633826981636,
      "secondary_accuracy": 0.4479166666666667,
      "secondary_decoder_mi_bits": 0.14841738788984546,
      "primary_confusion_matrix": [
        [
          5,
          8,
          7,
          4
        ],
        [
          7,
          5,
          9,
          3
        ],
        [
          3,
          7,
          8,
          6
        ],
        [
          4,
          5,
          6,
          9
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.375,
      "primary_decoder_mi_bits": 0.09320870024898659,
      "secondary_accuracy": 0.23958333333333334,
      "secondary_decoder_mi_bits": 0.060565811124475497,
      "primary_confusion_matrix": [
        [
          9,
          5,
          8,
          2
        ],
        [
          6,
          5,
          8,
          5
        ],
        [
          3,
          5,
          12,
          4
        ],
        [
          4,
          3,
          7,
          10
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.3958333333333333,
      "primary_decoder_mi_bits": 0.137243177512157,
      "secondary_accuracy": 0.3541666666666667,
      "secondary_decoder_mi_bits": 0.09434373830340756,
      "primary_confusion_matrix": [
        [
          10,
          4,
          5,
          5
        ],
        [
          6,
          7,
          5,
          6
        ],
        [
          3,
          8,
          8,
          5
        ],
        [
          1,
          6,
          4,
          13
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.04390340285281066,
      "secondary_accuracy": 0.15625,
      "secondary_decoder_mi_bits": 0.08621860029194824,
      "primary_confusion_matrix": [
        [
          4,
          5,
          8,
          7
        ],
        [
          6,
          7,
          2,
          9
        ],
        [
          4,
          5,
          5,
          10
        ],
        [
          5,
          6,
          6,
          7
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.25,
      "primary_decoder_mi_bits": 0.06280491439184863,
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.05869388312325536,
      "primary_confusion_matrix": [
        [
          8,
          7,
          7,
          2
        ],
        [
          6,
          7,
          6,
          5
        ],
        [
          9,
          7,
          3,
          5
        ],
        [
          4,
          5,
          9,
          6
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.07962022563477902,
      "secondary_accuracy": 0.23958333333333334,
      "secondary_decoder_mi_bits": 0.05739225717300853,
      "primary_confusion_matrix": [
        [
          7,
          8,
          6,
          3
        ],
        [
          3,
          8,
          3,
          10
        ],
        [
          7,
          5,
          4,
          8
        ],
        [
          5,
          8,
          7,
          4
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.2708333333333333,
      "primary_decoder_mi_bits": 0.07299487152871117,
      "secondary_accuracy": 0.3125,
      "secondary_decoder_mi_bits": 0.15504487317413562,
      "primary_confusion_matrix": [
        [
          9,
          5,
          3,
          7
        ],
        [
          7,
          7,
          7,
          3
        ],
        [
          8,
          6,
          4,
          6
        ],
        [
          3,
          6,
          9,
          6
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.05231128721655152,
      "secondary_accuracy": 0.19791666666666666,
      "secondary_decoder_mi_bits": 0.08863694238029976,
      "primary_confusion_matrix": [
        [
          7,
          5,
          6,
          6
        ],
        [
          5,
          7,
          8,
          4
        ],
        [
          8,
          9,
          2,
          5
        ],
        [
          6,
          6,
          5,
          7
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.054909553342766454,
      "secondary_accuracy": 0.3333333333333333,
      "secondary_decoder_mi_bits": 0.05968484130270618,
      "primary_confusion_matrix": [
        [
          8,
          6,
          7,
          3
        ],
        [
          7,
          6,
          4,
          7
        ],
        [
          8,
          5,
          3,
          8
        ],
        [
          7,
          9,
          5,
          3
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.19791666666666666,
      "primary_decoder_mi_bits": 0.056345107172363885,
      "secondary_accuracy": 0.2708333333333333,
      "secondary_decoder_mi_bits": 0.05399506919051973,
      "primary_confusion_matrix": [
        [
          7,
          8,
          4,
          5
        ],
        [
          5,
          6,
          6,
          7
        ],
        [
          7,
          6,
          2,
          9
        ],
        [
          6,
          6,
          8,
          4
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.05156937837340937,
      "secondary_accuracy": 0.25,
      "secondary_decoder_mi_bits": 0.03192166662384486,
      "primary_confusion_matrix": [
        [
          7,
          3,
          8,
          6
        ],
        [
          4,
          4,
          7,
          9
        ],
        [
          8,
          7,
          3,
          6
        ],
        [
          7,
          5,
          6,
          6
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.08027291684142236,
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.05994107329347875,
      "primary_confusion_matrix": [
        [
          7,
          4,
          7,
          6
        ],
        [
          4,
          6,
          7,
          7
        ],
        [
          9,
          10,
          2,
          3
        ],
        [
          6,
          6,
          7,
          5
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.06383623678431777,
      "secondary_accuracy": 0.2604166666666667,
      "secondary_decoder_mi_bits": 0.02869692715579956,
      "primary_confusion_matrix": [
        [
          6,
          4,
          9,
          5
        ],
        [
          6,
          5,
          5,
          8
        ],
        [
          10,
          4,
          6,
          4
        ],
        [
          7,
          9,
          5,
          3
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.041639217825657646,
      "secondary_accuracy": 0.2916666666666667,
      "secondary_decoder_mi_bits": 0.07654142296548117,
      "primary_confusion_matrix": [
        [
          6,
          5,
          7,
          6
        ],
        [
          9,
          7,
          4,
          4
        ],
        [
          8,
          6,
          3,
          7
        ],
        [
          8,
          3,
          6,
          7
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.25,
      "primary_decoder_mi_bits": 0.04578257694892774,
      "secondary_accuracy": 0.3020833333333333,
      "secondary_decoder_mi_bits": 0.05349482632226963,
      "primary_confusion_matrix": [
        [
          6,
          5,
          7,
          6
        ],
        [
          4,
          10,
          4,
          6
        ],
        [
          6,
          8,
          3,
          7
        ],
        [
          4,
          7,
          8,
          5
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.23958333333333334,
      "primary_decoder_mi_bits": 0.06320309290756158,
      "secondary_accuracy": 0.13541666666666666,
      "secondary_decoder_mi_bits": 0.20748620103465856,
      "primary_confusion_matrix": [
        [
          8,
          5,
          6,
          5
        ],
        [
          4,
          5,
          6,
          9
        ],
        [
          6,
          10,
          4,
          4
        ],
        [
          9,
          6,
          3,
          6
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.2604166666666667,
      "primary_decoder_mi_bits": 0.047159138753312874,
      "secondary_accuracy": 0.21875,
      "secondary_decoder_mi_bits": 0.10819195864116087,
      "primary_confusion_matrix": [
        [
          8,
          5,
          9,
          2
        ],
        [
          4,
          8,
          6,
          6
        ],
        [
          7,
          6,
          6,
          5
        ],
        [
          5,
          7,
          9,
          3
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.21875,
      "primary_decoder_mi_bits": 0.042230843459021686,
      "secondary_accuracy": 0.19791666666666666,
      "secondary_decoder_mi_bits": 0.08663715038324499,
      "primary_confusion_matrix": [
        [
          7,
          4,
          8,
          5
        ],
        [
          4,
          6,
          6,
          8
        ],
        [
          7,
          7,
          3,
          7
        ],
        [
          6,
          6,
          7,
          5
        ]
      ]
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_classes": 4,
      "encoded_bits": 2.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 96,
      "groups": 24,
      "chance_accuracy": 0.25,
      "primary_accuracy": 0.21875,
      "primary_decoder_mi_bits": 0.08967780673049514,
      "secondary_accuracy": 0.25,
      "secondary_decoder_mi_bits": 0.04333802124665564,
      "primary_confusion_matrix": [
        [
          4,
          7,
          9,
          4
        ],
        [
          6,
          6,
          8,
          4
        ],
        [
          5,
          6,
          2,
          11
        ],
        [
          5,
          5,
          5,
          9
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.20404537827222197,
      "secondary_accuracy": 0.10416666666666667,
      "secondary_decoder_mi_bits": 0.13471547535923176,
      "primary_confusion_matrix": [
        [
          1,
          3,
          5,
          3,
          2,
          4,
          3,
          3
        ],
        [
          0,
          4,
          0,
          3,
          8,
          3,
          4,
          2
        ],
        [
          1,
          3,
          5,
          3,
          2,
          4,
          3,
          3
        ],
        [
          2,
          5,
          1,
          2,
          2,
          6,
          2,
          4
        ],
        [
          1,
          6,
          2,
          1,
          5,
          8,
          1,
          0
        ],
        [
          0,
          2,
          3,
          2,
          2,
          9,
          2,
          4
        ],
        [
          1,
          3,
          5,
          3,
          2,
          4,
          3,
          3
        ],
        [
          1,
          6,
          2,
          1,
          5,
          8,
          1,
          0
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.1875,
      "primary_decoder_mi_bits": 0.11764656703236756,
      "secondary_accuracy": 0.16145833333333334,
      "secondary_decoder_mi_bits": 0.14535341981476532,
      "primary_confusion_matrix": [
        [
          3,
          5,
          0,
          7,
          1,
          3,
          2,
          3
        ],
        [
          0,
          7,
          0,
          8,
          3,
          2,
          0,
          4
        ],
        [
          3,
          5,
          0,
          7,
          1,
          3,
          2,
          3
        ],
        [
          0,
          4,
          0,
          10,
          2,
          4,
          1,
          3
        ],
        [
          0,
          4,
          0,
          8,
          3,
          2,
          1,
          6
        ],
        [
          2,
          4,
          0,
          8,
          2,
          5,
          1,
          2
        ],
        [
          3,
          5,
          0,
          7,
          1,
          3,
          2,
          3
        ],
        [
          0,
          4,
          0,
          8,
          3,
          2,
          1,
          6
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.11979166666666667,
      "primary_decoder_mi_bits": 0.11245859901221708,
      "secondary_accuracy": 0.15625,
      "secondary_decoder_mi_bits": 0.14425617096233057,
      "primary_confusion_matrix": [
        [
          4,
          6,
          0,
          9,
          2,
          1,
          1,
          1
        ],
        [
          3,
          4,
          0,
          10,
          3,
          1,
          0,
          3
        ],
        [
          4,
          6,
          0,
          9,
          2,
          1,
          1,
          1
        ],
        [
          4,
          4,
          0,
          7,
          3,
          2,
          1,
          3
        ],
        [
          1,
          8,
          1,
          5,
          2,
          3,
          1,
          3
        ],
        [
          3,
          7,
          0,
          9,
          2,
          2,
          1,
          0
        ],
        [
          4,
          6,
          0,
          9,
          2,
          1,
          1,
          1
        ],
        [
          1,
          8,
          1,
          5,
          2,
          3,
          1,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 4,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.11551979220935667,
      "secondary_accuracy": 0.16145833333333334,
      "secondary_decoder_mi_bits": 0.16343390400888583,
      "primary_confusion_matrix": [
        [
          1,
          6,
          2,
          4,
          3,
          7,
          1,
          0
        ],
        [
          1,
          6,
          1,
          7,
          3,
          2,
          2,
          2
        ],
        [
          1,
          6,
          2,
          4,
          3,
          7,
          1,
          0
        ],
        [
          2,
          6,
          1,
          6,
          3,
          3,
          1,
          2
        ],
        [
          2,
          8,
          1,
          3,
          4,
          2,
          2,
          2
        ],
        [
          0,
          7,
          1,
          3,
          3,
          7,
          2,
          1
        ],
        [
          1,
          6,
          2,
          4,
          3,
          7,
          1,
          0
        ],
        [
          2,
          8,
          1,
          3,
          4,
          2,
          2,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.140625,
      "primary_decoder_mi_bits": 0.18532141714536338,
      "secondary_accuracy": 0.16666666666666666,
      "secondary_decoder_mi_bits": 0.18130532988049022,
      "primary_confusion_matrix": [
        [
          6,
          0,
          3,
          0,
          0,
          6,
          7,
          2
        ],
        [
          3,
          3,
          2,
          1,
          0,
          3,
          7,
          5
        ],
        [
          2,
          4,
          4,
          1,
          3,
          4,
          3,
          3
        ],
        [
          3,
          4,
          5,
          0,
          2,
          2,
          5,
          3
        ],
        [
          4,
          3,
          3,
          2,
          0,
          3,
          5,
          4
        ],
        [
          2,
          2,
          4,
          1,
          2,
          5,
          6,
          2
        ],
        [
          6,
          3,
          2,
          3,
          3,
          2,
          4,
          1
        ],
        [
          2,
          4,
          1,
          2,
          2,
          5,
          3,
          5
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.1386855521032289,
      "secondary_accuracy": 0.18229166666666666,
      "secondary_decoder_mi_bits": 0.12266118285076472,
      "primary_confusion_matrix": [
        [
          0,
          1,
          5,
          6,
          4,
          2,
          5,
          1
        ],
        [
          0,
          4,
          3,
          3,
          5,
          3,
          3,
          3
        ],
        [
          1,
          2,
          4,
          7,
          5,
          1,
          3,
          1
        ],
        [
          1,
          3,
          5,
          4,
          0,
          4,
          3,
          4
        ],
        [
          0,
          4,
          4,
          4,
          5,
          1,
          3,
          3
        ],
        [
          0,
          4,
          3,
          7,
          1,
          2,
          4,
          3
        ],
        [
          0,
          3,
          3,
          5,
          3,
          2,
          4,
          4
        ],
        [
          0,
          4,
          3,
          4,
          4,
          1,
          2,
          6
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.17708333333333334,
      "primary_decoder_mi_bits": 0.1164561521723621,
      "secondary_accuracy": 0.16666666666666666,
      "secondary_decoder_mi_bits": 0.1797667490815388,
      "primary_confusion_matrix": [
        [
          2,
          4,
          4,
          5,
          1,
          1,
          7,
          0
        ],
        [
          1,
          7,
          1,
          4,
          3,
          2,
          4,
          2
        ],
        [
          1,
          3,
          5,
          6,
          1,
          2,
          5,
          1
        ],
        [
          2,
          6,
          4,
          5,
          1,
          1,
          5,
          0
        ],
        [
          2,
          5,
          2,
          5,
          2,
          1,
          5,
          2
        ],
        [
          1,
          3,
          4,
          4,
          2,
          2,
          6,
          2
        ],
        [
          2,
          5,
          2,
          5,
          0,
          2,
          7,
          1
        ],
        [
          0,
          6,
          3,
          3,
          2,
          2,
          4,
          4
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 8,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.140625,
      "primary_decoder_mi_bits": 0.09500335784477376,
      "secondary_accuracy": 0.13020833333333334,
      "secondary_decoder_mi_bits": 0.16163087098251142,
      "primary_confusion_matrix": [
        [
          4,
          3,
          3,
          3,
          4,
          3,
          3,
          1
        ],
        [
          1,
          6,
          3,
          4,
          1,
          3,
          1,
          5
        ],
        [
          3,
          4,
          2,
          6,
          3,
          3,
          1,
          2
        ],
        [
          2,
          3,
          5,
          4,
          4,
          4,
          1,
          1
        ],
        [
          3,
          5,
          2,
          4,
          2,
          4,
          2,
          2
        ],
        [
          3,
          5,
          2,
          4,
          3,
          4,
          2,
          1
        ],
        [
          3,
          4,
          1,
          2,
          2,
          7,
          3,
          2
        ],
        [
          2,
          6,
          4,
          3,
          2,
          4,
          1,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.140625,
      "primary_decoder_mi_bits": 0.2371048606237547,
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.20863430366923208,
      "primary_confusion_matrix": [
        [
          3,
          2,
          4,
          1,
          6,
          1,
          2,
          5
        ],
        [
          4,
          3,
          2,
          2,
          3,
          4,
          4,
          2
        ],
        [
          2,
          4,
          3,
          4,
          4,
          1,
          4,
          2
        ],
        [
          2,
          1,
          6,
          0,
          7,
          3,
          1,
          4
        ],
        [
          3,
          1,
          6,
          2,
          9,
          2,
          0,
          1
        ],
        [
          4,
          5,
          2,
          0,
          5,
          1,
          2,
          5
        ],
        [
          1,
          3,
          4,
          2,
          7,
          0,
          6,
          1
        ],
        [
          4,
          2,
          6,
          1,
          1,
          5,
          3,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.20833333333333334,
      "primary_decoder_mi_bits": 0.19016598680268998,
      "secondary_accuracy": 0.19791666666666666,
      "secondary_decoder_mi_bits": 0.24908576637633403,
      "primary_confusion_matrix": [
        [
          5,
          3,
          3,
          4,
          3,
          2,
          3,
          1
        ],
        [
          2,
          2,
          2,
          4,
          2,
          6,
          3,
          3
        ],
        [
          3,
          3,
          5,
          3,
          3,
          1,
          2,
          4
        ],
        [
          1,
          3,
          3,
          5,
          5,
          3,
          2,
          2
        ],
        [
          5,
          1,
          2,
          2,
          7,
          5,
          2,
          0
        ],
        [
          0,
          4,
          1,
          5,
          3,
          5,
          1,
          5
        ],
        [
          3,
          3,
          3,
          3,
          5,
          1,
          3,
          3
        ],
        [
          1,
          3,
          3,
          3,
          2,
          2,
          2,
          8
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.16145833333333334,
      "primary_decoder_mi_bits": 0.20194349141004073,
      "secondary_accuracy": 0.203125,
      "secondary_decoder_mi_bits": 0.2552803643359724,
      "primary_confusion_matrix": [
        [
          4,
          4,
          4,
          1,
          3,
          3,
          4,
          1
        ],
        [
          3,
          2,
          2,
          3,
          3,
          5,
          3,
          3
        ],
        [
          6,
          2,
          5,
          3,
          2,
          3,
          2,
          1
        ],
        [
          4,
          3,
          6,
          1,
          6,
          2,
          2,
          0
        ],
        [
          6,
          3,
          3,
          1,
          6,
          2,
          2,
          1
        ],
        [
          4,
          5,
          2,
          1,
          2,
          2,
          3,
          5
        ],
        [
          1,
          5,
          5,
          1,
          4,
          2,
          5,
          1
        ],
        [
          5,
          0,
          3,
          0,
          1,
          5,
          4,
          6
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 12,
      "phase": "during",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.17708333333333334,
      "primary_decoder_mi_bits": 0.21431543031994493,
      "secondary_accuracy": 0.1875,
      "secondary_decoder_mi_bits": 0.19640024227729105,
      "primary_confusion_matrix": [
        [
          3,
          1,
          2,
          2,
          6,
          2,
          3,
          5
        ],
        [
          4,
          2,
          3,
          2,
          3,
          4,
          1,
          5
        ],
        [
          0,
          4,
          7,
          3,
          3,
          1,
          1,
          5
        ],
        [
          0,
          1,
          7,
          3,
          5,
          2,
          0,
          6
        ],
        [
          3,
          2,
          3,
          2,
          8,
          4,
          1,
          1
        ],
        [
          2,
          4,
          3,
          1,
          4,
          1,
          2,
          7
        ],
        [
          0,
          2,
          5,
          1,
          5,
          3,
          5,
          3
        ],
        [
          0,
          2,
          5,
          4,
          2,
          4,
          2,
          5
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15625,
      "primary_decoder_mi_bits": 0.14345631479100518,
      "secondary_accuracy": 0.109375,
      "secondary_decoder_mi_bits": 0.2062436009199331,
      "primary_confusion_matrix": [
        [
          5,
          3,
          3,
          1,
          4,
          4,
          3,
          1
        ],
        [
          3,
          3,
          2,
          0,
          4,
          4,
          3,
          5
        ],
        [
          2,
          4,
          5,
          2,
          3,
          2,
          2,
          4
        ],
        [
          2,
          4,
          4,
          1,
          3,
          3,
          4,
          3
        ],
        [
          4,
          2,
          3,
          1,
          4,
          3,
          1,
          6
        ],
        [
          3,
          6,
          4,
          2,
          1,
          5,
          3,
          0
        ],
        [
          3,
          5,
          3,
          3,
          1,
          4,
          4,
          1
        ],
        [
          5,
          4,
          5,
          2,
          2,
          1,
          2,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.19270833333333334,
      "primary_decoder_mi_bits": 0.19284894909584255,
      "secondary_accuracy": 0.17708333333333334,
      "secondary_decoder_mi_bits": 0.22705237218817326,
      "primary_confusion_matrix": [
        [
          5,
          3,
          3,
          0,
          5,
          5,
          2,
          1
        ],
        [
          5,
          1,
          3,
          5,
          4,
          2,
          3,
          1
        ],
        [
          4,
          4,
          4,
          2,
          2,
          2,
          3,
          3
        ],
        [
          3,
          2,
          3,
          4,
          3,
          2,
          3,
          4
        ],
        [
          4,
          2,
          1,
          1,
          5,
          5,
          3,
          3
        ],
        [
          2,
          3,
          2,
          2,
          5,
          6,
          0,
          4
        ],
        [
          3,
          3,
          3,
          2,
          3,
          2,
          5,
          3
        ],
        [
          3,
          1,
          3,
          2,
          0,
          7,
          1,
          7
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.18229166666666666,
      "primary_decoder_mi_bits": 0.1834309494336034,
      "secondary_accuracy": 0.16666666666666666,
      "secondary_decoder_mi_bits": 0.22522682078433573,
      "primary_confusion_matrix": [
        [
          6,
          2,
          2,
          2,
          7,
          1,
          1,
          3
        ],
        [
          2,
          0,
          3,
          1,
          3,
          3,
          7,
          5
        ],
        [
          5,
          1,
          4,
          1,
          2,
          3,
          3,
          5
        ],
        [
          3,
          1,
          4,
          1,
          7,
          2,
          1,
          5
        ],
        [
          4,
          2,
          1,
          1,
          8,
          3,
          3,
          2
        ],
        [
          2,
          4,
          2,
          1,
          3,
          7,
          3,
          2
        ],
        [
          1,
          3,
          2,
          3,
          6,
          2,
          3,
          4
        ],
        [
          2,
          3,
          3,
          3,
          2,
          2,
          3,
          6
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 16,
      "phase": "end",
      "after_lag": 0,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.203125,
      "primary_decoder_mi_bits": 0.1716834520207828,
      "secondary_accuracy": 0.171875,
      "secondary_decoder_mi_bits": 0.17803819560110246,
      "primary_confusion_matrix": [
        [
          5,
          1,
          1,
          3,
          3,
          3,
          3,
          5
        ],
        [
          3,
          3,
          5,
          3,
          1,
          3,
          3,
          3
        ],
        [
          4,
          3,
          6,
          2,
          1,
          1,
          5,
          2
        ],
        [
          3,
          4,
          2,
          3,
          1,
          4,
          3,
          4
        ],
        [
          2,
          5,
          2,
          2,
          6,
          3,
          3,
          1
        ],
        [
          2,
          2,
          1,
          2,
          5,
          8,
          2,
          2
        ],
        [
          1,
          3,
          3,
          3,
          4,
          2,
          5,
          3
        ],
        [
          2,
          5,
          5,
          4,
          1,
          1,
          3,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.18229166666666666,
      "primary_decoder_mi_bits": 0.17008079955349356,
      "secondary_accuracy": 0.13020833333333334,
      "secondary_decoder_mi_bits": 0.12102618790039844,
      "primary_confusion_matrix": [
        [
          7,
          0,
          5,
          5,
          2,
          2,
          1,
          2
        ],
        [
          3,
          5,
          2,
          2,
          4,
          5,
          2,
          1
        ],
        [
          6,
          3,
          4,
          2,
          4,
          3,
          1,
          1
        ],
        [
          5,
          6,
          3,
          1,
          3,
          2,
          2,
          2
        ],
        [
          6,
          3,
          2,
          2,
          3,
          4,
          0,
          4
        ],
        [
          2,
          3,
          2,
          2,
          2,
          9,
          1,
          3
        ],
        [
          3,
          3,
          2,
          3,
          3,
          4,
          4,
          2
        ],
        [
          3,
          4,
          3,
          6,
          1,
          3,
          2,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.16666666666666666,
      "primary_decoder_mi_bits": 0.17419963617611656,
      "secondary_accuracy": 0.11979166666666667,
      "secondary_decoder_mi_bits": 0.13523678413514365,
      "primary_confusion_matrix": [
        [
          2,
          4,
          3,
          2,
          3,
          5,
          3,
          2
        ],
        [
          3,
          2,
          5,
          5,
          2,
          2,
          2,
          3
        ],
        [
          3,
          6,
          1,
          3,
          2,
          4,
          2,
          3
        ],
        [
          1,
          6,
          3,
          3,
          1,
          2,
          3,
          5
        ],
        [
          6,
          1,
          2,
          4,
          3,
          3,
          1,
          4
        ],
        [
          5,
          2,
          3,
          1,
          1,
          8,
          1,
          3
        ],
        [
          5,
          3,
          3,
          1,
          0,
          2,
          6,
          4
        ],
        [
          4,
          2,
          2,
          2,
          1,
          3,
          3,
          7
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.171875,
      "primary_decoder_mi_bits": 0.17633016270354698,
      "secondary_accuracy": 0.15104166666666666,
      "secondary_decoder_mi_bits": 0.22370304996471552,
      "primary_confusion_matrix": [
        [
          3,
          1,
          4,
          4,
          3,
          3,
          2,
          4
        ],
        [
          1,
          1,
          2,
          2,
          4,
          6,
          3,
          5
        ],
        [
          4,
          3,
          2,
          1,
          5,
          2,
          5,
          2
        ],
        [
          2,
          4,
          3,
          3,
          4,
          1,
          3,
          4
        ],
        [
          4,
          3,
          1,
          6,
          5,
          3,
          1,
          1
        ],
        [
          2,
          2,
          1,
          1,
          4,
          10,
          3,
          1
        ],
        [
          2,
          2,
          4,
          0,
          4,
          3,
          6,
          3
        ],
        [
          3,
          2,
          2,
          3,
          4,
          4,
          3,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 20,
      "phase": "after",
      "after_lag": 4,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.18229166666666666,
      "primary_decoder_mi_bits": 0.1899168662297656,
      "secondary_accuracy": 0.16145833333333334,
      "secondary_decoder_mi_bits": 0.24031702712110792,
      "primary_confusion_matrix": [
        [
          3,
          3,
          4,
          2,
          5,
          1,
          4,
          2
        ],
        [
          0,
          6,
          3,
          2,
          3,
          4,
          1,
          5
        ],
        [
          4,
          3,
          4,
          4,
          2,
          2,
          3,
          2
        ],
        [
          0,
          5,
          1,
          4,
          2,
          3,
          3,
          6
        ],
        [
          2,
          3,
          4,
          2,
          4,
          4,
          3,
          2
        ],
        [
          1,
          4,
          0,
          2,
          2,
          6,
          5,
          4
        ],
        [
          3,
          3,
          3,
          1,
          3,
          2,
          5,
          4
        ],
        [
          1,
          5,
          3,
          4,
          0,
          6,
          2,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.13020833333333334,
      "primary_decoder_mi_bits": 0.16718648983336779,
      "secondary_accuracy": 0.11979166666666667,
      "secondary_decoder_mi_bits": 0.25963942379054006,
      "primary_confusion_matrix": [
        [
          2,
          2,
          2,
          4,
          5,
          3,
          4,
          2
        ],
        [
          3,
          5,
          3,
          1,
          2,
          5,
          2,
          3
        ],
        [
          6,
          5,
          4,
          3,
          2,
          1,
          1,
          2
        ],
        [
          4,
          3,
          2,
          2,
          4,
          1,
          6,
          2
        ],
        [
          4,
          2,
          2,
          1,
          3,
          4,
          2,
          6
        ],
        [
          6,
          3,
          2,
          2,
          4,
          3,
          2,
          2
        ],
        [
          2,
          0,
          3,
          7,
          3,
          5,
          2,
          2
        ],
        [
          3,
          5,
          2,
          3,
          3,
          3,
          1,
          4
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15104166666666666,
      "primary_decoder_mi_bits": 0.20836149063606574,
      "secondary_accuracy": 0.11979166666666667,
      "secondary_decoder_mi_bits": 0.1913087649423199,
      "primary_confusion_matrix": [
        [
          8,
          0,
          1,
          5,
          5,
          1,
          3,
          1
        ],
        [
          2,
          6,
          1,
          3,
          2,
          1,
          5,
          4
        ],
        [
          6,
          4,
          1,
          4,
          4,
          1,
          3,
          1
        ],
        [
          3,
          2,
          1,
          7,
          3,
          2,
          2,
          4
        ],
        [
          5,
          4,
          3,
          4,
          1,
          6,
          0,
          1
        ],
        [
          3,
          4,
          3,
          3,
          4,
          3,
          4,
          0
        ],
        [
          6,
          3,
          4,
          4,
          2,
          3,
          1,
          1
        ],
        [
          3,
          4,
          1,
          7,
          3,
          2,
          2,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.140625,
      "primary_decoder_mi_bits": 0.2107907899866095,
      "secondary_accuracy": 0.14583333333333334,
      "secondary_decoder_mi_bits": 0.16697377373711325,
      "primary_confusion_matrix": [
        [
          5,
          2,
          5,
          4,
          2,
          3,
          3,
          0
        ],
        [
          2,
          5,
          2,
          5,
          1,
          2,
          3,
          4
        ],
        [
          7,
          3,
          1,
          2,
          3,
          2,
          3,
          3
        ],
        [
          2,
          4,
          3,
          4,
          2,
          2,
          4,
          3
        ],
        [
          5,
          3,
          0,
          4,
          3,
          5,
          1,
          3
        ],
        [
          5,
          6,
          0,
          1,
          6,
          3,
          3,
          0
        ],
        [
          4,
          3,
          5,
          4,
          3,
          1,
          2,
          2
        ],
        [
          1,
          2,
          1,
          5,
          4,
          4,
          3,
          4
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 24,
      "phase": "after",
      "after_lag": 8,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.11979166666666667,
      "primary_decoder_mi_bits": 0.1944147153736884,
      "secondary_accuracy": 0.08333333333333333,
      "secondary_decoder_mi_bits": 0.20695192176182176,
      "primary_confusion_matrix": [
        [
          4,
          3,
          3,
          2,
          3,
          5,
          4,
          0
        ],
        [
          2,
          6,
          1,
          2,
          2,
          5,
          2,
          4
        ],
        [
          2,
          3,
          1,
          2,
          2,
          2,
          8,
          4
        ],
        [
          1,
          5,
          3,
          3,
          1,
          1,
          8,
          2
        ],
        [
          3,
          3,
          7,
          1,
          1,
          5,
          3,
          1
        ],
        [
          4,
          4,
          2,
          0,
          5,
          4,
          2,
          3
        ],
        [
          2,
          4,
          5,
          4,
          1,
          3,
          2,
          3
        ],
        [
          1,
          5,
          4,
          2,
          1,
          5,
          4,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.13020833333333334,
      "primary_decoder_mi_bits": 0.16604100231531854,
      "secondary_accuracy": 0.11979166666666667,
      "secondary_decoder_mi_bits": 0.17526291865869925,
      "primary_confusion_matrix": [
        [
          3,
          3,
          3,
          3,
          2,
          7,
          2,
          1
        ],
        [
          2,
          5,
          3,
          5,
          2,
          4,
          2,
          1
        ],
        [
          4,
          5,
          4,
          1,
          2,
          2,
          1,
          5
        ],
        [
          4,
          5,
          1,
          1,
          2,
          2,
          7,
          2
        ],
        [
          3,
          1,
          4,
          1,
          4,
          4,
          5,
          2
        ],
        [
          5,
          4,
          1,
          1,
          3,
          3,
          3,
          4
        ],
        [
          2,
          2,
          2,
          5,
          3,
          4,
          2,
          4
        ],
        [
          3,
          3,
          3,
          5,
          3,
          1,
          3,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.15625,
      "primary_decoder_mi_bits": 0.2094563995690734,
      "secondary_accuracy": 0.10416666666666667,
      "secondary_decoder_mi_bits": 0.17941065978445644,
      "primary_confusion_matrix": [
        [
          4,
          5,
          3,
          4,
          3,
          2,
          1,
          2
        ],
        [
          3,
          6,
          2,
          1,
          3,
          6,
          0,
          3
        ],
        [
          4,
          2,
          2,
          1,
          5,
          0,
          6,
          4
        ],
        [
          4,
          3,
          2,
          2,
          6,
          2,
          4,
          1
        ],
        [
          2,
          3,
          2,
          4,
          8,
          2,
          2,
          1
        ],
        [
          2,
          8,
          1,
          1,
          7,
          2,
          3,
          0
        ],
        [
          1,
          3,
          2,
          2,
          7,
          2,
          4,
          3
        ],
        [
          0,
          5,
          4,
          4,
          5,
          2,
          2,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.171875,
      "primary_decoder_mi_bits": 0.2514919176640876,
      "secondary_accuracy": 0.11979166666666667,
      "secondary_decoder_mi_bits": 0.227882667173489,
      "primary_confusion_matrix": [
        [
          5,
          2,
          4,
          2,
          3,
          5,
          0,
          3
        ],
        [
          0,
          6,
          1,
          3,
          4,
          7,
          1,
          2
        ],
        [
          4,
          3,
          2,
          0,
          6,
          4,
          1,
          4
        ],
        [
          4,
          3,
          2,
          1,
          5,
          1,
          5,
          3
        ],
        [
          2,
          1,
          4,
          3,
          9,
          2,
          2,
          1
        ],
        [
          5,
          6,
          0,
          2,
          4,
          4,
          2,
          1
        ],
        [
          4,
          2,
          1,
          2,
          4,
          2,
          4,
          5
        ],
        [
          2,
          2,
          5,
          6,
          3,
          3,
          1,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 32,
      "phase": "after",
      "after_lag": 16,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.171875,
      "primary_decoder_mi_bits": 0.13309019207482453,
      "secondary_accuracy": 0.19270833333333334,
      "secondary_decoder_mi_bits": 0.261123584909049,
      "primary_confusion_matrix": [
        [
          5,
          6,
          1,
          3,
          4,
          1,
          3,
          1
        ],
        [
          5,
          6,
          3,
          2,
          3,
          4,
          1,
          0
        ],
        [
          4,
          5,
          2,
          1,
          6,
          2,
          2,
          2
        ],
        [
          6,
          5,
          1,
          3,
          4,
          1,
          3,
          1
        ],
        [
          2,
          5,
          2,
          3,
          7,
          0,
          3,
          2
        ],
        [
          5,
          3,
          2,
          1,
          5,
          3,
          3,
          2
        ],
        [
          3,
          3,
          1,
          5,
          5,
          2,
          5,
          0
        ],
        [
          4,
          4,
          1,
          4,
          2,
          4,
          3,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "morphology",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.11458333333333333,
      "primary_decoder_mi_bits": 0.163091391356278,
      "secondary_accuracy": 0.14583333333333334,
      "secondary_decoder_mi_bits": 0.2802995722113775,
      "primary_confusion_matrix": [
        [
          2,
          2,
          0,
          1,
          5,
          7,
          4,
          3
        ],
        [
          3,
          4,
          3,
          1,
          3,
          3,
          4,
          3
        ],
        [
          4,
          1,
          4,
          4,
          3,
          2,
          2,
          4
        ],
        [
          5,
          3,
          5,
          4,
          2,
          3,
          1,
          1
        ],
        [
          3,
          5,
          5,
          4,
          1,
          0,
          3,
          3
        ],
        [
          4,
          4,
          4,
          2,
          2,
          3,
          2,
          3
        ],
        [
          4,
          3,
          5,
          2,
          3,
          2,
          1,
          4
        ],
        [
          3,
          2,
          6,
          4,
          3,
          1,
          2,
          3
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "recent_growth",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.10416666666666667,
      "primary_decoder_mi_bits": 0.19429522185661013,
      "secondary_accuracy": 0.09375,
      "secondary_decoder_mi_bits": 0.17692770691049917,
      "primary_confusion_matrix": [
        [
          0,
          5,
          7,
          1,
          2,
          4,
          4,
          1
        ],
        [
          2,
          3,
          4,
          2,
          2,
          3,
          3,
          5
        ],
        [
          5,
          5,
          3,
          0,
          1,
          5,
          4,
          1
        ],
        [
          1,
          5,
          3,
          1,
          0,
          5,
          5,
          4
        ],
        [
          1,
          5,
          2,
          0,
          1,
          7,
          4,
          4
        ],
        [
          2,
          8,
          2,
          1,
          1,
          4,
          4,
          2
        ],
        [
          4,
          2,
          1,
          0,
          1,
          3,
          8,
          5
        ],
        [
          3,
          4,
          2,
          1,
          1,
          5,
          8,
          0
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.11979166666666667,
      "primary_decoder_mi_bits": 0.15971103553039923,
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.14987910059842724,
      "primary_confusion_matrix": [
        [
          1,
          4,
          3,
          2,
          6,
          6,
          0,
          2
        ],
        [
          3,
          2,
          6,
          3,
          2,
          4,
          3,
          1
        ],
        [
          5,
          3,
          3,
          1,
          3,
          3,
          4,
          2
        ],
        [
          1,
          6,
          3,
          2,
          2,
          5,
          2,
          3
        ],
        [
          4,
          3,
          3,
          4,
          3,
          2,
          4,
          1
        ],
        [
          6,
          3,
          3,
          1,
          1,
          4,
          4,
          2
        ],
        [
          5,
          2,
          3,
          2,
          2,
          1,
          6,
          3
        ],
        [
          3,
          1,
          5,
          2,
          5,
          4,
          2,
          2
        ]
      ]
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_classes": 8,
      "encoded_bits": 3.0,
      "elapsed_step": 40,
      "phase": "after",
      "after_lag": 24,
      "feature_set": "delta_combined",
      "samples": 192,
      "groups": 24,
      "chance_accuracy": 0.125,
      "primary_accuracy": 0.109375,
      "primary_decoder_mi_bits": 0.1561287682099049,
      "secondary_accuracy": 0.125,
      "secondary_decoder_mi_bits": 0.14082903906769226,
      "primary_confusion_matrix": [
        [
          3,
          2,
          1,
          2,
          7,
          4,
          3,
          2
        ],
        [
          4,
          1,
          3,
          3,
          5,
          2,
          4,
          2
        ],
        [
          7,
          1,
          2,
          1,
          5,
          2,
          5,
          1
        ],
        [
          3,
          1,
          5,
          2,
          4,
          3,
          3,
          3
        ],
        [
          6,
          0,
          3,
          5,
          2,
          3,
          3,
          2
        ],
        [
          4,
          2,
          4,
          2,
          3,
          5,
          3,
          1
        ],
        [
          5,
          3,
          3,
          2,
          1,
          3,
          4,
          3
        ],
        [
          6,
          0,
          0,
          1,
          9,
          2,
          4,
          2
        ]
      ]
    }
  ]
}
```


# Stage 4 — Attack Every Rung of the Ladder

```json
{
  "groupwise_label_permutation": {
    "L1": {
      "4": {
        "n": 100,
        "mean": 0.5002083333333333,
        "std": 0.05747093166211168,
        "q95": 0.6041666666666666,
        "q99": 0.625,
        "max": 0.625
      },
      "8": {
        "n": 100,
        "mean": 0.49520833333333336,
        "std": 0.06087149202760408,
        "q95": 0.6041666666666666,
        "q99": 0.6252083333333335,
        "max": 0.6458333333333334
      },
      "12": {
        "n": 100,
        "mean": 0.50125,
        "std": 0.07051521703386676,
        "q95": 0.625,
        "q99": 0.6666666666666666,
        "max": 0.6666666666666666
      },
      "16": {
        "n": 100,
        "mean": 0.506875,
        "std": 0.07471328297416582,
        "q95": 0.6458333333333334,
        "q99": 0.6668750000000001,
        "max": 0.6875
      },
      "20": {
        "n": 100,
        "mean": 0.4954166666666667,
        "std": 0.08351958353184799,
        "q95": 0.625,
        "q99": 0.6458333333333334,
        "max": 0.6458333333333334
      },
      "24": {
        "n": 100,
        "mean": 0.5177083333333333,
        "std": 0.06695089151758922,
        "q95": 0.6260416666666666,
        "q99": 0.6666666666666666,
        "max": 0.6666666666666666
      },
      "32": {
        "n": 100,
        "mean": 0.4883333333333333,
        "std": 0.06980379247895091,
        "q95": 0.6052083333333332,
        "q99": 0.6460416666666668,
        "max": 0.6666666666666666
      },
      "40": {
        "n": 100,
        "mean": 0.48229166666666673,
        "std": 0.07863720979211361,
        "q95": 0.5854166666666666,
        "q99": 0.6670833333333335,
        "max": 0.7083333333333334
      }
    },
    "L2": {
      "4": {
        "n": 100,
        "mean": 0.5039583333333334,
        "std": 0.06664680693776709,
        "q95": 0.6041666666666666,
        "q99": 0.6252083333333335,
        "max": 0.6458333333333334
      },
      "8": {
        "n": 100,
        "mean": 0.501875,
        "std": 0.05536299092253677,
        "q95": 0.5833333333333334,
        "q99": 0.6252083333333335,
        "max": 0.6458333333333334
      },
      "12": {
        "n": 100,
        "mean": 0.48958333333333326,
        "std": 0.0829941011960087,
        "q95": 0.6052083333333332,
        "q99": 0.6254166666666668,
        "max": 0.6666666666666666
      },
      "16": {
        "n": 100,
        "mean": 0.4962500000000001,
        "std": 0.07605622006851978,
        "q95": 0.625,
        "q99": 0.6458333333333334,
        "max": 0.6458333333333334
      },
      "20": {
        "n": 100,
        "mean": 0.505,
        "std": 0.06712860791048776,
        "q95": 0.6041666666666666,
        "q99": 0.625,
        "max": 0.625
      },
      "24": {
        "n": 100,
        "mean": 0.4922916666666666,
        "std": 0.07262770123108063,
        "q95": 0.584375,
        "q99": 0.6879166666666668,
        "max": 0.7291666666666666
      },
      "32": {
        "n": 100,
        "mean": 0.5,
        "std": 0.07027969913930417,
        "q95": 0.6041666666666666,
        "q99": 0.6466666666666672,
        "max": 0.7291666666666666
      },
      "40": {
        "n": 100,
        "mean": 0.4962499999999999,
        "std": 0.07819469113835173,
        "q95": 0.6052083333333332,
        "q99": 0.6258333333333338,
        "max": 0.7083333333333334
      }
    },
    "L3": {
      "4": {
        "n": 100,
        "mean": 0.49375,
        "std": 0.0369754986443726,
        "q95": 0.5427083333333332,
        "q99": 0.5833333333333334,
        "max": 0.5833333333333334
      },
      "8": {
        "n": 100,
        "mean": 0.49770833333333336,
        "std": 0.06325207232002585,
        "q95": 0.6041666666666666,
        "q99": 0.6460416666666668,
        "max": 0.6666666666666666
      },
      "12": {
        "n": 100,
        "mean": 0.49583333333333335,
        "std": 0.07850601533923655,
        "q95": 0.6458333333333334,
        "q99": 0.6875,
        "max": 0.6875
      },
      "16": {
        "n": 100,
        "mean": 0.4929166666666668,
        "std": 0.06469882147303767,
        "q95": 0.584375,
        "q99": 0.6462500000000002,
        "max": 0.6875
      },
      "20": {
        "n": 100,
        "mean": 0.485625,
        "std": 0.07026086066699344,
        "q95": 0.6052083333333332,
        "q99": 0.625,
        "max": 0.625
      },
      "24": {
        "n": 100,
        "mean": 0.494375,
        "std": 0.08248816202946942,
        "q95": 0.6260416666666666,
        "q99": 0.6675000000000004,
        "max": 0.75
      },
      "32": {
        "n": 100,
        "mean": 0.5008333333333334,
        "std": 0.0712560913575503,
        "q95": 0.6052083333333332,
        "q99": 0.6462500000000002,
        "max": 0.6875
      },
      "40": {
        "n": 100,
        "mean": 0.49999999999999994,
        "std": 0.0907147544044885,
        "q95": 0.6260416666666666,
        "q99": 0.6877083333333335,
        "max": 0.7083333333333334
      }
    },
    "L4": {
      "4": {
        "n": 100,
        "mean": 0.509375,
        "std": 0.06083725729353683,
        "q95": 0.584375,
        "q99": 0.6670833333333335,
        "max": 0.7083333333333334
      },
      "8": {
        "n": 100,
        "mean": 0.5120833333333333,
        "std": 0.0734905984160937,
        "q95": 0.6458333333333334,
        "q99": 0.6875,
        "max": 0.6875
      },
      "12": {
        "n": 100,
        "mean": 0.5066666666666667,
        "std": 0.0662015021648972,
        "q95": 0.6052083333333332,
        "q99": 0.6252083333333335,
        "max": 0.6458333333333334
      },
      "16": {
        "n": 100,
        "mean": 0.5085416666666667,
        "std": 0.08176094685456838,
        "q95": 0.6458333333333334,
        "q99": 0.7293750000000001,
        "max": 0.75
      },
      "20": {
        "n": 100,
        "mean": 0.5039583333333334,
        "std": 0.08633625920074242,
        "q95": 0.6458333333333334,
        "q99": 0.6462500000000002,
        "max": 0.6875
      },
      "24": {
        "n": 100,
        "mean": 0.4977083333333333,
        "std": 0.07282106828460504,
        "q95": 0.6052083333333332,
        "q99": 0.6460416666666668,
        "max": 0.6666666666666666
      },
      "32": {
        "n": 100,
        "mean": 0.4889583333333334,
        "std": 0.0750263263979903,
        "q95": 0.6041666666666666,
        "q99": 0.6252083333333335,
        "max": 0.6458333333333334
      },
      "40": {
        "n": 100,
        "mean": 0.5008333333333334,
        "std": 0.07222409185614205,
        "q95": 0.6041666666666666,
        "q99": 0.6462500000000002,
        "max": 0.6875
      }
    },
    "L5": {
      "4": {
        "n": 100,
        "mean": 0.253125,
        "std": 0.03465792658252943,
        "q95": 0.3020833333333333,
        "q99": 0.3542708333333334,
        "max": 0.3645833333333333
      },
      "8": {
        "n": 100,
        "mean": 0.24645833333333336,
        "std": 0.03884229599719014,
        "q95": 0.3229166666666667,
        "q99": 0.34385416666666674,
        "max": 0.3541666666666667
      },
      "12": {
        "n": 100,
        "mean": 0.24989583333333332,
        "std": 0.04232539193065237,
        "q95": 0.3130208333333333,
        "q99": 0.3645833333333333,
        "max": 0.3645833333333333
      },
      "16": {
        "n": 100,
        "mean": 0.25541666666666674,
        "std": 0.041207890964932645,
        "q95": 0.3234375,
        "q99": 0.35447916666666685,
        "max": 0.3854166666666667
      },
      "20": {
        "n": 100,
        "mean": 0.25385416666666666,
        "std": 0.04110704923158287,
        "q95": 0.3234375,
        "q99": 0.3645833333333333,
        "max": 0.3645833333333333
      },
      "24": {
        "n": 100,
        "mean": 0.2521875,
        "std": 0.04208887649136712,
        "q95": 0.3229166666666667,
        "q99": 0.3645833333333333,
        "max": 0.3645833333333333
      },
      "32": {
        "n": 100,
        "mean": 0.239375,
        "std": 0.04407074883386687,
        "q95": 0.3229166666666667,
        "q99": 0.3542708333333334,
        "max": 0.3645833333333333
      },
      "40": {
        "n": 100,
        "mean": 0.24312500000000004,
        "std": 0.047168525434516884,
        "q95": 0.3130208333333333,
        "q99": 0.3541666666666667,
        "max": 0.3541666666666667
      }
    },
    "L6": {
      "4": {
        "n": 100,
        "mean": 0.12421875,
        "std": 0.015029900031779245,
        "q95": 0.15104166666666666,
        "q99": 0.15625,
        "max": 0.15625
      },
      "8": {
        "n": 100,
        "mean": 0.12432291666666666,
        "std": 0.018555925580038966,
        "q95": 0.15651041666666665,
        "q99": 0.171875,
        "max": 0.171875
      },
      "12": {
        "n": 100,
        "mean": 0.12401041666666668,
        "std": 0.021945508885488522,
        "q95": 0.16145833333333334,
        "q99": 0.17203125000000008,
        "max": 0.1875
      },
      "16": {
        "n": 100,
        "mean": 0.12770833333333334,
        "std": 0.01946662920943885,
        "q95": 0.16145833333333334,
        "q99": 0.17192708333333337,
        "max": 0.17708333333333334
      },
      "20": {
        "n": 100,
        "mean": 0.12380208333333333,
        "std": 0.021472676739385955,
        "q95": 0.16145833333333334,
        "q99": 0.1771354166666667,
        "max": 0.18229166666666666
      },
      "24": {
        "n": 100,
        "mean": 0.12494791666666666,
        "std": 0.021905918130312285,
        "q95": 0.16145833333333334,
        "q99": 0.171875,
        "max": 0.171875
      },
      "32": {
        "n": 100,
        "mean": 0.12145833333333333,
        "std": 0.026708950850895575,
        "q95": 0.171875,
        "q99": 0.19817708333333345,
        "max": 0.22395833333333334
      },
      "40": {
        "n": 100,
        "mean": 0.13020833333333334,
        "std": 0.02418372242967479,
        "q95": 0.16718749999999996,
        "q99": 0.18244791666666674,
        "max": 0.19791666666666666
      }
    }
  },
  "headline_observed_vs_null": {
    "L1": {
      "4": {
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      },
      "8": {
        "accuracy": 0.625,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": true
      },
      "12": {
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "null_q95": 0.625,
        "beats_null_q95": false
      },
      "16": {
        "accuracy": 0.4375,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "beats_null_q95": false
      },
      "20": {
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "null_q95": 0.625,
        "beats_null_q95": false
      },
      "24": {
        "accuracy": 0.5,
        "chance": 0.5,
        "null_q95": 0.6260416666666666,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.4375,
        "chance": 0.5,
        "null_q95": 0.5854166666666666,
        "beats_null_q95": false
      }
    },
    "L2": {
      "4": {
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": true
      },
      "8": {
        "accuracy": 0.5,
        "chance": 0.5,
        "null_q95": 0.5833333333333334,
        "beats_null_q95": false
      },
      "12": {
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      },
      "16": {
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "null_q95": 0.625,
        "beats_null_q95": false
      },
      "20": {
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      },
      "24": {
        "accuracy": 0.5,
        "chance": 0.5,
        "null_q95": 0.584375,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.5625,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      }
    },
    "L3": {
      "4": {
        "accuracy": 0.5625,
        "chance": 0.5,
        "null_q95": 0.5427083333333332,
        "beats_null_q95": true
      },
      "8": {
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      },
      "12": {
        "accuracy": 0.6875,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "beats_null_q95": true
      },
      "16": {
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "null_q95": 0.584375,
        "beats_null_q95": true
      },
      "20": {
        "accuracy": 0.5,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      },
      "24": {
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "null_q95": 0.6260416666666666,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.4375,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.5625,
        "chance": 0.5,
        "null_q95": 0.6260416666666666,
        "beats_null_q95": false
      }
    },
    "L4": {
      "4": {
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "null_q95": 0.584375,
        "beats_null_q95": true
      },
      "8": {
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "beats_null_q95": false
      },
      "12": {
        "accuracy": 0.625,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": true
      },
      "16": {
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "beats_null_q95": false
      },
      "20": {
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "null_q95": 0.6458333333333334,
        "beats_null_q95": false
      },
      "24": {
        "accuracy": 0.5625,
        "chance": 0.5,
        "null_q95": 0.6052083333333332,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.4375,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.4166666666666667,
        "chance": 0.5,
        "null_q95": 0.6041666666666666,
        "beats_null_q95": false
      }
    },
    "L5": {
      "4": {
        "accuracy": 0.2916666666666667,
        "chance": 0.25,
        "null_q95": 0.3020833333333333,
        "beats_null_q95": false
      },
      "8": {
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "beats_null_q95": false
      },
      "12": {
        "accuracy": 0.3958333333333333,
        "chance": 0.25,
        "null_q95": 0.3130208333333333,
        "beats_null_q95": true
      },
      "16": {
        "accuracy": 0.375,
        "chance": 0.25,
        "null_q95": 0.3234375,
        "beats_null_q95": true
      },
      "20": {
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "null_q95": 0.3234375,
        "beats_null_q95": false
      },
      "24": {
        "accuracy": 0.19791666666666666,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "null_q95": 0.3229166666666667,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.21875,
        "chance": 0.25,
        "null_q95": 0.3130208333333333,
        "beats_null_q95": false
      }
    },
    "L6": {
      "4": {
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "null_q95": 0.15104166666666666,
        "beats_null_q95": false
      },
      "8": {
        "accuracy": 0.17708333333333334,
        "chance": 0.125,
        "null_q95": 0.15651041666666665,
        "beats_null_q95": true
      },
      "12": {
        "accuracy": 0.16145833333333334,
        "chance": 0.125,
        "null_q95": 0.16145833333333334,
        "beats_null_q95": false
      },
      "16": {
        "accuracy": 0.18229166666666666,
        "chance": 0.125,
        "null_q95": 0.16145833333333334,
        "beats_null_q95": true
      },
      "20": {
        "accuracy": 0.171875,
        "chance": 0.125,
        "null_q95": 0.16145833333333334,
        "beats_null_q95": true
      },
      "24": {
        "accuracy": 0.140625,
        "chance": 0.125,
        "null_q95": 0.16145833333333334,
        "beats_null_q95": false
      },
      "32": {
        "accuracy": 0.171875,
        "chance": 0.125,
        "null_q95": 0.171875,
        "beats_null_q95": false
      },
      "40": {
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "null_q95": 0.16718749999999996,
        "beats_null_q95": false
      }
    }
  }
}
```


# Stage 5 — Find the Simplest Surviving Distinction

```json
{
  "exploratory_threshold": "raw combined accuracy > grouped permutation q95 AND >= 0.075 absolute accuracy above chance",
  "first_supported_level": "L1",
  "first_supported_elapsed_step": 8,
  "levels": {
    "L1": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.625,
        "chance": 0.5,
        "margin_above_chance": 0.125,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.5854166666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L2": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.16666666666666663,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.5833333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.625,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.020833333333333315,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      }
    ],
    "L3": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.5427083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6875,
        "chance": 0.5,
        "margin_above_chance": 0.1875,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.6666666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.16666666666666663,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.5,
        "chance": 0.5,
        "margin_above_chance": 0.0,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6260416666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L4": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.6041666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.10416666666666663,
        "null_q95": 0.584375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.5416666666666666,
        "chance": 0.5,
        "margin_above_chance": 0.04166666666666663,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.625,
        "chance": 0.5,
        "margin_above_chance": 0.125,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.5208333333333334,
        "chance": 0.5,
        "margin_above_chance": 0.02083333333333337,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.4791666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.020833333333333315,
        "null_q95": 0.6458333333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.5625,
        "chance": 0.5,
        "margin_above_chance": 0.0625,
        "null_q95": 0.6052083333333332,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.4375,
        "chance": 0.5,
        "margin_above_chance": -0.0625,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.4166666666666667,
        "chance": 0.5,
        "margin_above_chance": -0.08333333333333331,
        "null_q95": 0.6041666666666666,
        "passes_exploratory_threshold": false
      }
    ],
    "L5": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.2916666666666667,
        "chance": 0.25,
        "margin_above_chance": 0.041666666666666685,
        "null_q95": 0.3020833333333333,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.2604166666666667,
        "chance": 0.25,
        "margin_above_chance": 0.010416666666666685,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.3958333333333333,
        "chance": 0.25,
        "margin_above_chance": 0.14583333333333331,
        "null_q95": 0.3130208333333333,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.375,
        "chance": 0.25,
        "margin_above_chance": 0.125,
        "null_q95": 0.3234375,
        "passes_exploratory_threshold": true
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "margin_above_chance": -0.010416666666666657,
        "null_q95": 0.3234375,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.19791666666666666,
        "chance": 0.25,
        "margin_above_chance": -0.05208333333333334,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.23958333333333334,
        "chance": 0.25,
        "margin_above_chance": -0.010416666666666657,
        "null_q95": 0.3229166666666667,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.21875,
        "chance": 0.25,
        "margin_above_chance": -0.03125,
        "null_q95": 0.3130208333333333,
        "passes_exploratory_threshold": false
      }
    ],
    "L6": [
      {
        "elapsed_step": 4,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "margin_above_chance": -0.005208333333333329,
        "null_q95": 0.15104166666666666,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 8,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.17708333333333334,
        "chance": 0.125,
        "margin_above_chance": 0.05208333333333334,
        "null_q95": 0.15651041666666665,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 12,
        "phase": "during",
        "after_lag": 0,
        "accuracy": 0.16145833333333334,
        "chance": 0.125,
        "margin_above_chance": 0.03645833333333334,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 16,
        "phase": "end",
        "after_lag": 0,
        "accuracy": 0.18229166666666666,
        "chance": 0.125,
        "margin_above_chance": 0.05729166666666666,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 20,
        "phase": "after",
        "after_lag": 4,
        "accuracy": 0.171875,
        "chance": 0.125,
        "margin_above_chance": 0.046875,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 24,
        "phase": "after",
        "after_lag": 8,
        "accuracy": 0.140625,
        "chance": 0.125,
        "margin_above_chance": 0.015625,
        "null_q95": 0.16145833333333334,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 32,
        "phase": "after",
        "after_lag": 16,
        "accuracy": 0.171875,
        "chance": 0.125,
        "margin_above_chance": 0.046875,
        "null_q95": 0.171875,
        "passes_exploratory_threshold": false
      },
      {
        "elapsed_step": 40,
        "phase": "after",
        "after_lag": 24,
        "accuracy": 0.11979166666666667,
        "chance": 0.125,
        "margin_above_chance": -0.005208333333333329,
        "null_q95": 0.16718749999999996,
        "passes_exploratory_threshold": false
      }
    ]
  },
  "interpretation": "v2 is a boundary-finding experiment. Any positive rung discovered here should be frozen and rerun in a separate confirmatory version."
}
```


# Stage 6 — Exploratory Verdict

**Verdict: `TEMPORAL_INFORMATION_BOUNDARY_LOCATED`**

> The exploratory ladder first recovered codeword identity at L1, elapsed step 8. This is a candidate boundary, not yet a confirmatory claim.

```json
{
  "verdict": "TEMPORAL_INFORMATION_BOUNDARY_LOCATED",
  "bounded_claim": "The exploratory ladder first recovered codeword identity at L1, elapsed step 8. This is a candidate boundary, not yet a confirmatory claim.",
  "next_action": "Freeze the simplest positive rung and its observation time, then run a new confirmatory version with larger independent groups and a predeclared endpoint.",
  "explicit_nonclaims": [
    "semantics",
    "meaning",
    "understanding",
    "sender identity",
    "coordination",
    "learning",
    "agency",
    "individuality",
    "life",
    "Shannon channel capacity"
  ]
}
```
