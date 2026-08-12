# Stages 4–5 — End-to-End Paired Sham and MDE Calibration

```json
{
  "endpoint": 8,
  "calibration_role": "EXPLORATORY INSTRUMENT DEVELOPMENT",
  "noise_model": "centered + sign-symmetrized CRN matched-pair deltas from this v5 pilot; therefore this same pilot is not confirmatory evidence",
  "calibration_reps": 200,
  "permutations_per_test": 500,
  "instruments": {
    "ridge_all24": {
      "feature_names": [
        "population_fraction",
        "max_radius_fraction",
        "mean_radius_fraction",
        "std_radius_fraction",
        "centroid_x_scaled",
        "centroid_y_scaled",
        "cov_trace_scaled",
        "cov_anisotropy",
        "boundary_fraction",
        "mean_degree",
        "degree_1",
        "degree_2",
        "degree_3",
        "degree_4",
        "degree_5",
        "degree_6",
        "sector_0",
        "sector_1",
        "sector_2",
        "sector_3",
        "sector_4",
        "sector_5",
        "harmonic6_cos",
        "harmonic6_sin"
      ],
      "null_fpr": 0.045,
      "target_power": 0.8,
      "mde80_grid_estimate": 0.5,
      "power_curve": [
        {
          "shift_norm": 0.0,
          "detection_rate_alpha_0_05": 0.045,
          "mean_p_value": 0.4846906187624751
        },
        {
          "shift_norm": 0.25,
          "detection_rate_alpha_0_05": 0.43,
          "mean_p_value": 0.07527944111776447
        },
        {
          "shift_norm": 0.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.002634730538922156
        },
        {
          "shift_norm": 0.75,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.25,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 2.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        }
      ]
    },
    "ridge_angular9": {
      "feature_names": [
        "cov_anisotropy",
        "sector_0",
        "sector_1",
        "sector_2",
        "sector_3",
        "sector_4",
        "sector_5",
        "harmonic6_cos",
        "harmonic6_sin"
      ],
      "null_fpr": 0.085,
      "target_power": 0.8,
      "mde80_grid_estimate": 0.25,
      "power_curve": [
        {
          "shift_norm": 0.0,
          "detection_rate_alpha_0_05": 0.085,
          "mean_p_value": 0.5013872255489022
        },
        {
          "shift_norm": 0.25,
          "detection_rate_alpha_0_05": 0.995,
          "mean_p_value": 0.006806387225548902
        },
        {
          "shift_norm": 0.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 0.75,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.25,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 1.5,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        },
        {
          "shift_norm": 2.0,
          "detection_rate_alpha_0_05": 1.0,
          "mean_p_value": 0.001996007984031937
        }
      ]
    }
  },
  "interpretation": "MDE grid values describe instrument resolution for the declared synthetic direction. They are not upper bounds on the real effect."
}
```
