# Stage 7 — Experimental Verdict

**Verdict: `RECOVERABLE_PAST_SUPPORTED`**

> Within Digital Crystal v1, a complete checkpoint is sufficient for exact continuation, an explicit event log reconstructs the exact morphology trajectory, and the same checkpoint can be used as an executable branch point for controlled alternative futures. Visible morphology alone is not sufficient continuation state. These experiments do not establish that the checkpoint is minimal.

```json
{
  "verdict": "RECOVERABLE_PAST_SUPPORTED",
  "bounded_claim": "Within Digital Crystal v1, a complete checkpoint is sufficient for exact continuation, an explicit event log reconstructs the exact morphology trajectory, and the same checkpoint can be used as an executable branch point for controlled alternative futures. Visible morphology alone is not sufficient continuation state. These experiments do not establish that the checkpoint is minimal.",
  "exact_checkpoint_restore": true,
  "history_replay_exact_morphology_trajectory": true,
  "state_history_operationally_distinct": true,
  "visible_morphology_is_not_sufficient_state": true,
  "rng_state_matters_for_exact_growth_continuation": true,
  "signal_cursor_matters_at_fixed_horizon": true,
  "birth_times_change_growth_continuation": false,
  "birth_time_interpretation": "historical metadata under Digital Crystal v1 growth rule",
  "minimum_sufficient_state_identified": false,
  "counterfactual_branching_produces_divergence": true,
  "environmental_divergence_exceeds_stochastic_null_descriptively": false,
  "branch_null_comparison": {
    "treatment_minus_null_mean": -0.0014746360681055248,
    "pairwise_superiority_probability": 0.1975,
    "treatment_median_exceeds_null_q95": false,
    "interpretation": "The checkpoint is an executable branch point regardless of effect size. Environmental divergence is unusually large only if the treatment distribution clearly exceeds the stochastic-null distribution."
  },
  "event_log_scope": "reconstructs morphology/birth trajectory; does not reconstruct historical RNG state from additions alone",
  "explicit_nonclaims": [
    "minimum state",
    "learning",
    "adaptation",
    "agency",
    "selfhood",
    "understanding",
    "biological memory",
    "environmental divergence beyond stochastic null unless supported",
    "life"
  ]
}
```

Key interpretation:

- **state** is operationally sufficient information for faithful continuation;
- **history** here is an explicit record sufficient to reconstruct the morphology
  trajectory;
- the experiment identifies some necessary continuation variables but does not
  prove a mathematically minimal state representation;
- a saved checkpoint is an executable counterfactual branch point;
- whether changed future forcing causes *more* divergence than ordinary
  stochastic variation is assessed separately against the stochastic null.
