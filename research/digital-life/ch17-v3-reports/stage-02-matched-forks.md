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
  "raw_and_paired_delta_features": "Raw receiver features are primary. Matched no-channel feature deltas are reported as a mechanistic diagnostic, not the headline decoder.",
  "equal_exposure_eligibility": {
    "L1": {
      "level": "L1",
      "title": "One pulse: early vs late",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            1,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            1,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            1,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            1,
            1
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            1,
            1
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            1,
            1
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            1,
            1
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            1,
            1
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    },
    "L2": {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            2,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            2,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            2,
            0
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            2,
            2
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            2,
            2
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            2,
            2
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            2,
            2
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            2,
            2
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    },
    "L3": {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            2,
            1
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            4,
            2
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            4,
            4
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    },
    "L4": {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            1,
            4
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            1,
            5
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            2,
            5
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    },
    "L5": {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            1,
            4,
            1,
            2
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            1,
            5,
            4,
            3
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            2,
            5,
            5,
            5
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    },
    "L6": {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "observations": [
        {
          "elapsed_step": 4,
          "cumulative_pulses_by_codeword": [
            1,
            4,
            1,
            2,
            2,
            2,
            1,
            2
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 8,
          "cumulative_pulses_by_codeword": [
            1,
            5,
            4,
            3,
            3,
            3,
            2,
            2
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 12,
          "cumulative_pulses_by_codeword": [
            2,
            5,
            5,
            5,
            5,
            4,
            4,
            4
          ],
          "equal_exposure": false,
          "eligible_for_information_survival_claim": false,
          "role": "causal_onset_diagnostic_only"
        },
        {
          "elapsed_step": 16,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6,
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 20,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6,
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 24,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6,
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 32,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6,
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        },
        {
          "elapsed_step": 40,
          "cumulative_pulses_by_codeword": [
            6,
            6,
            6,
            6,
            6,
            6,
            6,
            6
          ],
          "equal_exposure": true,
          "eligible_for_information_survival_claim": true,
          "role": "information_survival"
        }
      ]
    }
  },
  "eligibility_rule": "An observation can support temporal-information survival only when all competing codewords have delivered the same cumulative pulse count by that observation time. Unequal-prefix observations are causal-onset diagnostics only."
}
```
