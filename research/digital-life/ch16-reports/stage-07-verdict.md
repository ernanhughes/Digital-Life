# Stage 7 — Experimental Verdict

**Verdict: `CAUSAL_TRANSMISSION_SUPPORTED`**

> Within this protocol, inserting one received bit into an otherwise identical Digital Crystal continuation reliably changed receiver growth, but the real sender-generated event stream did not clear all controls required for a sender-specific signalling claim.

```json
{
  "verdict": "CAUSAL_TRANSMISSION_SUPPORTED",
  "bounded_claim": "Within this protocol, inserting one received bit into an otherwise identical Digital Crystal continuation reliably changed receiver growth, but the real sender-generated event stream did not clear all controls required for a sender-specific signalling claim.",
  "checks": {
    "single_bit_changes_receiver_reliably": true,
    "real_stream_beats_all_message_controls": false
  },
  "headline_metrics": {
    "single_bit_fraction_with_any_morphology_change": 0.9583333333333334,
    "single_bit_mean_normalized_final_difference": 0.16328068044830893,
    "real_vs_shuffled": {
      "real_minus_control_mean": 0.29395536343072454,
      "pairwise_superiority_probability": 0.9802777777777778
    },
    "real_vs_unrelated_replay_count_matched": {
      "real_minus_control_mean": -0.015078374230654057,
      "pairwise_superiority_probability": 0.45694444444444443
    },
    "real_vs_ipi_permutation_surrogate": {
      "real_minus_control_mean": 0.010373841437850362,
      "pairwise_superiority_probability": 0.4725
    },
    "real_vs_rate_matched_random": {
      "real_minus_control_mean": 0.2698870205697631,
      "pairwise_superiority_probability": 0.9772222222222222
    },
    "impulse_peak_lag": 0,
    "chain_real_source_to_node_corr": [
      1.0,
      0.5373421448225714,
      0.476502004766455,
      0.46214947215469776,
      0.4620092356556393,
      0.4578017794000673
    ],
    "board_real_minus_shuffled_neighbor_corr": 0.004826701878735018
  },
  "kill_conditions": {
    "decorative_channel": "Triggered if exact pulse/no-pulse checkpoint interventions do not reliably change the receiver.",
    "not_sender_specific": "Triggered if real sender timing does not beat shuffled, count-matched unrelated replay, exact-IPI surrogate, and rate-matched-random controls."
  },
  "explicit_nonclaims": [
    "language",
    "semantics",
    "meaning",
    "cooperation",
    "coordination",
    "planning",
    "learning",
    "intelligence",
    "agency",
    "individuality",
    "selfhood",
    "life",
    "channel capacity"
  ]
}
```
