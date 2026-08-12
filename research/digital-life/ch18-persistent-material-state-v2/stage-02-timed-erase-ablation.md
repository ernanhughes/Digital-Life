# Stage 2 — When Does Persistent State Stop Mattering?

```json
{
  "groups": 32,
  "probe_steps": [
    5,
    7,
    10,
    14
  ],
  "followup_horizon": 3,
  "alpha": 0.05,
  "results": {
    "5": {
      "probe_elapsed_step": 5,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 16.6875,
        "median": 17.0,
        "std": 4.433096406576333,
        "ci95_low": 15.15546875,
        "ci95_high": 18.21875,
        "min": 6.0,
        "max": 24.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.15183491971224217,
        "median": 0.16015449227538622,
        "std": 0.03707545293448811,
        "ci95_low": 0.13851772530915882,
        "ci95_high": 0.16447911286907058,
        "min": 0.061224489795918366,
        "max": 0.21100917431192662
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 0.002984307758185673,
        "median": 0.0019052042923345465,
        "std": 0.00366245376339345,
        "ci95_low": 0.0018481959104609332,
        "ci95_high": 0.004222762106131355,
        "min": 0.0,
        "max": 0.01669195751138088
      },
      "paired_ridge_test": {
        "statistic": 0.574540597133495,
        "p_value": 0.014985014985014986,
        "permutations": 1000,
        "null_mean": 0.27608527264697186,
        "null_q95": 0.48983669554776227,
        "null_q99": 0.6353019722699024
      },
      "causal_effect_detected": true
    },
    "7": {
      "probe_elapsed_step": 7,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 2.25,
        "median": 2.0,
        "std": 1.7320508075688772,
        "ci95_low": 1.625,
        "ci95_high": 2.875,
        "min": 0.0,
        "max": 8.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.017590920226151323,
        "median": 0.01626123744050767,
        "std": 0.013114346359260646,
        "ci95_low": 0.013181825835561272,
        "ci95_high": 0.022089999918106805,
        "min": 0.0,
        "max": 0.057971014492753624
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 8.890469416785207e-05,
        "median": 0.0,
        "std": 0.0004950003878760688,
        "ci95_low": 0.0,
        "ci95_high": 0.0002667140825035562,
        "min": 0.0,
        "max": 0.002844950213371266
      },
      "paired_ridge_test": {
        "statistic": 0.03192550714998349,
        "p_value": 0.5014985014985015,
        "permutations": 1000,
        "null_mean": 0.03192550714998343,
        "null_q95": 0.03192550714998354,
        "null_q99": 0.03192550714998354
      },
      "causal_effect_detected": false
    },
    "10": {
      "probe_elapsed_step": 10,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "causal_effect_detected": false
    },
    "14": {
      "probe_elapsed_step": 14,
      "followup_steps": 3,
      "frontier_contact_count": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "frontier_exposed_fraction": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "pathwise_symmetric_difference_after_followup": {
        "n": 32,
        "mean": 0.0,
        "median": 0.0,
        "std": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "paired_ridge_test": {
        "statistic": 0.0,
        "p_value": 1.0,
        "permutations": 1000,
        "null_mean": 0.0,
        "null_q95": 0.0,
        "null_q99": 0.0
      },
      "causal_effect_detected": false
    }
  },
  "status": "MEASURED",
  "bounded_statement": "The erase ablation is evaluated before, near, and after loss of frontier contact. This tests whether causal efficacy tracks accessibility of the persistent material state."
}
```
