# Stage 3 — What Information Is Actually Part of Continuation State?

All variants were continued for exactly **48 updates**.
This fixes the v1 cursor confound: changing the signal cursor no longer changes
how many continuation updates execute.

```json
{
  "variants": {
    "full_state": {
      "starting_step": 48,
      "starting_signal_cursor": 48,
      "requested_continuation_steps": 48,
      "executed_steps": 48,
      "final_step": 96,
      "final_signal_cursor": 96,
      "final_population": 9574,
      "morphology_hash": "bc8e6d8c9783431f1459bf17",
      "process_hash": "bd33c9aa0a510803be6ce6bf",
      "normalized_difference": 0.0,
      "symmetric_difference_cells": 0,
      "exact_occupied_set": true,
      "exact_birth_times": true,
      "exact_process_hash": true
    },
    "no_rng_state": {
      "starting_step": 48,
      "starting_signal_cursor": 48,
      "requested_continuation_steps": 48,
      "executed_steps": 48,
      "final_step": 96,
      "final_signal_cursor": 96,
      "final_population": 9550,
      "morphology_hash": "192a330f71d5612fcbcb4a7c",
      "process_hash": "c09e7e2a1607b0caec14a285",
      "normalized_difference": 0.0029239766081871343,
      "symmetric_difference_cells": 28,
      "exact_occupied_set": false,
      "exact_birth_times": false,
      "exact_process_hash": false
    },
    "wrong_signal_cursor_fixed_horizon": {
      "starting_step": 48,
      "starting_signal_cursor": 45,
      "requested_continuation_steps": 48,
      "executed_steps": 48,
      "final_step": 96,
      "final_signal_cursor": 93,
      "final_population": 9549,
      "morphology_hash": "2b7a47d85853732aadc8f505",
      "process_hash": "dece38fbfd2f743fbd32532d",
      "normalized_difference": 0.0028198433420365534,
      "symmetric_difference_cells": 27,
      "exact_occupied_set": false,
      "exact_birth_times": false,
      "exact_process_hash": false
    },
    "birth_times_only": {
      "starting_step": 48,
      "starting_signal_cursor": 48,
      "requested_continuation_steps": 48,
      "executed_steps": 48,
      "final_step": 96,
      "final_signal_cursor": 96,
      "final_population": 9574,
      "morphology_hash": "cc840819ddb33fa38d9dcb97",
      "process_hash": "a60757aee507ff40eb03234d",
      "normalized_difference": 0.0,
      "symmetric_difference_cells": 0,
      "exact_occupied_set": true,
      "exact_birth_times": false,
      "exact_process_hash": false
    },
    "morphology_only": {
      "starting_step": 48,
      "starting_signal_cursor": 48,
      "requested_continuation_steps": 48,
      "executed_steps": 48,
      "final_step": 96,
      "final_signal_cursor": 96,
      "final_population": 9548,
      "morphology_hash": "bc83bb01676137c11b053d1d",
      "process_hash": "c883c613cf146f5bc588af5e",
      "normalized_difference": 0.003132832080200501,
      "symmetric_difference_cells": 30,
      "exact_occupied_set": false,
      "exact_birth_times": false,
      "exact_process_hash": false
    }
  },
  "interpretation": {
    "full_checkpoint_is_sufficient": true,
    "rng_state_changes_exact_growth_continuation": true,
    "signal_cursor_changes_growth_at_fixed_horizon": true,
    "birth_times_change_growth_continuation": false,
    "birth_times_are_historical_metadata_if_false_above": true,
    "visible_morphology_alone_is_sufficient": false,
    "minimum_state_identified": false,
    "note": "These ablations identify sufficiency and specific causal omissions; they do not prove that the stored checkpoint is a minimal sufficient state."
  }
}
```

Figure: `static\images\books\digital-life\ch15-03-state-omission.png`

Interpretation rules:

- the **full checkpoint** tests sufficiency for exact continuation;
- the **RNG-only** ablation isolates stochastic continuation state;
- the **cursor-only** ablation isolates environmental sequence position while
  holding the continuation horizon fixed;
- the **birth-time-only** ablation tests birth metadata independently;
- the **morphology-only** condition is a combined stress test and establishes
  only whether visible morphology is sufficient.

The experiment does **not** claim that the checkpoint representation is the
minimum possible sufficient state.
