# Stage 5 — Can the Measuring Apparatus Recover a Known Effect?

```json
{
  "known_effect_calibration": true,
  "endpoint": 20,
  "feature_index": 7,
  "feature_name": "cov_anisotropy",
  "empirical_feature_sd": 0.047899972633380486,
  "spike_in_reps": 100,
  "results": [
    {
      "shift_sd_units": 0.0,
      "detection_rate_alpha_0_05": 0.04,
      "p_value_mean": 0.5323383084577114,
      "p_value_median": 0.5547263681592041
    },
    {
      "shift_sd_units": 0.25,
      "detection_rate_alpha_0_05": 0.05,
      "p_value_mean": 0.4499004975124377,
      "p_value_median": 0.40796019900497515
    },
    {
      "shift_sd_units": 0.5,
      "detection_rate_alpha_0_05": 0.04,
      "p_value_mean": 0.40601990049751235,
      "p_value_median": 0.36318407960199006
    },
    {
      "shift_sd_units": 1.0,
      "detection_rate_alpha_0_05": 0.2,
      "p_value_mean": 0.2217910447761194,
      "p_value_median": 0.1791044776119403
    }
  ],
  "interpretation": "This does not test the crystal. It measures whether the declared two-sample pipeline can recover synthetic effects of known size."
}
```
