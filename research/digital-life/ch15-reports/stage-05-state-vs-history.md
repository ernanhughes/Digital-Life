# Stage 5 — State Is Not History

Results:

```json
{
  "history_reconstructs_checkpoint_morphology": true,
  "checkpoint_contains_explicit_event_sequence": false,
  "checkpoint_state_continues_exactly": true,
  "history_reconstructed_geometry_without_rng_continues_exactly": false,
  "history_geometry_only_final_difference": 0.003132832080200501
}
```

The distinction is operational:

- A **checkpoint state** can continue the process exactly if it contains the
  required continuation variables.
- A **history log** can reconstruct the route to a prior morphology.
- The checkpoint does not, by itself, contain an ordered list of events.
- Reconstructed geometry alone does not necessarily reproduce the exact future,
  because continuation state includes more than visible morphology.

This is the chapter's central separation:

```text
STATE
= enough information to continue from here

HISTORY
= enough information to reconstruct how here was reached
```
