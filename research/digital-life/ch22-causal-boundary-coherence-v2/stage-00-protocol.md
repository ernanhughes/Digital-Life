# Stage 0 — Freeze the Causal-Boundary Test

```json
{
  "role": "CAUSAL BOUNDARY COHERENCE TEST",
  "v1_status": "FAILED predictive-coherence family test because the observed family maximum did not beat the frozen run-group future-permutation null at alpha=0.05.",
  "v1_control_note": "The V1 observer-null environment was not identical in geometry to the real annular environment. V2 does not reuse that predictive null as a causal control.",
  "question": "Does the V1 carry-forward boundary at 0.90 R_eff localize causal consequences more strongly than a predeclared interior pseudo-boundary at 0.60 R_eff?",
  "candidate_radius_fraction": 0.9,
  "control_radius_fraction": 0.6,
  "intervention": {
    "type": "occupied-cell removal",
    "k": 16,
    "shell_width": 4.0,
    "matching": [
      "occupied-neighbour count",
      "absolute distance-from-boundary bin",
      "exact intervention count"
    ]
  },
  "response_horizon": 8,
  "primary_statistic": "causal_localization(0.90 R_eff) - causal_localization(0.60 R_eff)",
  "causal_localization_definition": "(inside perturbation -> inner target - outside perturbation -> inner target) + (outside perturbation -> outer target - inside perturbation -> outer target)",
  "primary_sei": 0.01,
  "alpha": 0.05,
  "new_sentence_if_successful": "Perturbations on opposite sides of the V1 carry-forward spatial boundary produced preferentially boundary-localized causal consequences beyond those observed at the predeclared interior pseudo-boundary.",
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
