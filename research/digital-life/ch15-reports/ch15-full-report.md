# Chapter 15 — Digital Crystal History: Full Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "experiment_version": "digital-crystal-history-v3",
  "profile": "full",
  "profile_config": {
    "steps": 96,
    "max_radius": 56,
    "checkpoint_step": 48,
    "replicates": 30,
    "branch_null_reps": 60
  },
  "seed": 20260811,
  "database": "research\\digital-life\\ch15-digital-crystal-history.sqlite3",
  "images": "static\\images\\books\\digital-life",
  "reports": "research\\digital-life\\ch15-reports",
  "started_at_unix": 1786494570.0950832,
  "spec": {
    "run_name": "chapter-15-primary",
    "signal_seed": 20260911,
    "crystal_seed": 20261011,
    "steps": 96,
    "max_radius": 56,
    "checkpoint_step": 48,
    "signal_kind": "composite",
    "model_params": {
      "base_bias": -2.1,
      "neighbor_gain": 0.78,
      "signal_rate_gain": 0.28,
      "anisotropy_gain": 0.95,
      "signal_phase_gain": 1.15,
      "crowding_penalty": 0.22
    },
    "model_version": "digital-crystal-v1-frozen",
    "experiment_version": "digital-crystal-history-v3"
  },
  "finished_at_unix": 1786494738.4893937,
  "final_verdict": "RECOVERABLE_PAST_SUPPORTED",
  "replicate_restore_all_exact": true,
  "canonical_rng_traversal": "sorted(frontier)",
  "reproducibility_invariant_passed": true
}
```

## Stage 1 — Continuous Reference Run

A continuous Digital Crystal v1 run provides the reference trajectory.

- Run key: `adc090ec883a9a61fd69188c`
- Checkpoint step: **48**
- Population at checkpoint: **2702**
- Final population: **9574**
- Final morphology hash: `bc8e6d8c9783431f1459bf17`
- Final process-state hash: `bd33c9aa0a510803be6ce6bf`
- Recorded history events: **96**
- Cached reference reused: **False**

Figure: `static\images\books\digital-life\ch15-01-reference-and-checkpoint.png`

This stage establishes the exact trajectory against which restore and replay
experiments are compared.

## Stage 0 — Reproducibility Invariant

The stochastic model must not depend on accidental Python container layout.

Digital Crystal history v3 therefore consumes RNG draws over a canonical
`sorted(frontier)` order.

A checkpoint was reconstructed through fresh serialized/deserialized
`set`, `dict`, and RNG-state objects and compared with the original checkpoint.

```json
{
  "implementation_invariant": "RNG-consuming candidate traversal is canonicalized with sorted(frontier); equivalent mathematical states must not depend on Python set/hash-table layout.",
  "state_identity_after_roundtrip": {
    "occupied_equal": true,
    "birth_time_equal": true,
    "step_equal": true,
    "signal_cursor_equal": true,
    "rng_state_equal": true,
    "process_hash_equal": true
  },
  "one_step_exact_after_container_roundtrip": true,
  "one_step_additions_equal": true,
  "full_remaining_horizon_exact_after_container_roundtrip": true,
  "remaining_steps_checked": 48,
  "passed": true
}
```

A pass means two mathematically identical states produce the same one-step and
remaining-horizon continuation even when their Python containers were rebuilt
independently.

## Stage 2 — Save, Restore, Continue

The midpoint state was serialized to SQLite, loaded into a new runtime state,
and continued using the remaining input.

Results:

- Exact final morphology: **True**
- Exact final process state: **True**
- Population trajectory identical: **True**
- Attachment trajectory identical: **True**
- Symmetric-difference cells: **0**

Reference morphology hash: `bc8e6d8c9783431f1459bf17`  
Restored morphology hash: `bc8e6d8c9783431f1459bf17`

Reference process hash: `bd33c9aa0a510803be6ce6bf`  
Restored process hash: `bd33c9aa0a510803be6ce6bf`

Figure: `static\images\books\digital-life\ch15-02-exact-restore.png`

An exact pass means the checkpoint preserved sufficient process state to resume
the stochastic growth process without changing its future.

## Stage 2B — Checkpoint Restore Across Independent Runs

Independent exact-restore validation:

- Replicates: **30**
- Exact morphology + process state: **30/30**
- All exact: **True**

This reduces the chance that exact restoration was peculiar to one random run.

## Stage 3 — What Information Is Actually Part of Continuation State?

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

## Stage 4 — Can the Past Be Reconstructed?

Two different notions of replay were tested.

### Procedural replay

Start from the original seed and replay the same input through the same frozen
rule.

- Exact final morphology: **True**
- Exact final process state: **True**

### Event-log replay

Ignore stochastic re-execution and instead replay the recorded cell-addition
events.

- Exact final morphology: **True**
- All trajectory hashes match: **True**
- Matching trajectory hashes: **96/96**

Figure: `static\images\books\digital-life\ch15-04-history-replay.png`

The event log is a genuine formation record only if it can reconstruct every
recorded state, not merely something visually similar.

## Stage 5 — State Is Not History

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

## Stage 6 — One Past, Alternative Futures, and a Stochastic Null

The exact same checkpoint can be restored repeatedly and used as an executable
counterfactual branch point.

The stronger question is whether changing future forcing produces divergence
larger than ordinary stochastic continuation variation.

Treatment:

```text
same checkpoint
same RNG state
different future forcing
```

Stochastic null:

```text
same checkpoint
same future forcing
different valid RNG states
```

Replicates per condition: **60**

```json
{
  "shared_checkpoint_morphology_hash": "05ef23114bf84b4d304cc46b",
  "illustrative_branch": {
    "future_a_final_morphology_hash": "867ceffae3249248102b373d",
    "future_b_final_morphology_hash": "12c951fdc17bb69fe12ca617",
    "final_normalized_difference": 0.0036545891197661065,
    "final_symmetric_difference_cells": 35,
    "branch_a_population": 9550,
    "branch_b_population": 9569,
    "divergence_series": [
      0.0007077140835102619,
      0.029830957905203844,
      0.0521875,
      0.06466923761495105,
      0.06816245384833854,
      0.07286568787384448,
      0.07964601769911504,
      0.07825,
      0.08247174801635009,
      0.0875,
      0.08655781704316708,
      0.08923941227312014,
      0.09394442140190792,
      0.08875976758164697,
      0.08336572094830937,
      0.07685080796692972,
      0.07614028711611848,
      0.07530279094260137,
      0.07574987290289781,
      0.07457293035479633,
      0.07442231075697212,
      0.07047084502650452,
      0.07341541267669859,
      0.07469309273776069,
      0.07815198618307427,
      0.07634228187919463,
      0.07669376693766938,
      0.07363013698630137,
      0.0767067246228586,
      0.07914650787743456,
      0.07505144655610702,
      0.0717239749497814,
      0.0654086594119009,
      0.05985434683659536,
      0.05562395075545607,
      0.05193516374462454,
      0.04768644529123571,
      0.043797195253505936,
      0.03597815611949887,
      0.028623111300276654,
      0.022151563328033915,
      0.0185673594260998,
      0.015332913253518168,
      0.011841140102693073,
      0.008791208791208791,
      0.007107023411371237,
      0.005535826195947357,
      0.0036545891197661065
    ]
  },
  "replicated_environment_treatment": {
    "definition": "same checkpoint + same RNG state + different future forcing",
    "normalized_difference": {
      "n": 60,
      "mean": 0.0038154447344304503,
      "std": 0.0010023837597526344,
      "median": 0.0036547799400000122,
      "q05": 0.002709913382237142,
      "q25": 0.0031064798058980944,
      "q75": 0.004203104608132004,
      "q95": 0.005539342378081572,
      "min": 0.0021961932650073207,
      "max": 0.0074159181115521205
    },
    "symmetric_difference_cells": {
      "n": 60,
      "mean": 36.53333333333333,
      "std": 9.597786938888246,
      "median": 35.0,
      "q05": 25.95,
      "q25": 29.75,
      "q75": 40.25,
      "q95": 53.05,
      "min": 21.0,
      "max": 71.0
    },
    "values": [
      0.0029245874242740757,
      0.0034464751958224542,
      0.003760183831209526,
      0.004072256447739376,
      0.004176673279732693,
      0.003028088127806202,
      0.0029239766081871343,
      0.004281537176274018,
      0.0074159181115521205,
      0.0053252584316591835,
      0.002508361204013378,
      0.003760576621748668,
      0.004177109440267335,
      0.0036561161600334275,
      0.003968253968253968,
      0.005220841599665866,
      0.003864229765013055,
      0.003133486526007938,
      0.003028088127806202,
      0.0027151211361737676,
      0.004072681704260651,
      0.0021961932650073207,
      0.0045943406077059625,
      0.0036545891197661065,
      0.003446115288220551,
      0.0032409827496079455,
      0.0037593984962406013,
      0.0027159720045962605,
      0.0033413386237861544,
      0.0035509138381201043,
      0.004386881136411114,
      0.0031325049597995197,
      0.003341687552213868,
      0.005639097744360902,
      0.0030284043441938177,
      0.0030284043441938177,
      0.004699248120300752,
      0.002819548872180451,
      0.003446115288220551,
      0.0026109660574412533,
      0.0029239766081871343,
      0.0055340920956458185,
      0.003028088127806202,
      0.003654970760233918,
      0.004490861618798955,
      0.0034457554557794715,
      0.005439330543933054,
      0.0037593984962406013,
      0.005430242272347535,
      0.0036545891197661065,
      0.004595300261096605,
      0.0032372598162071844,
      0.003132832080200501,
      0.003236921791792837,
      0.003863422783752741,
      0.003967839615746058,
      0.00428109011172601,
      0.0028198433420365534,
      0.0037593984962406013,
      0.006578947368421052
    ]
  },
  "stochastic_null": {
    "definition": "same checkpoint + same future forcing + different valid RNG states",
    "normalized_difference": {
      "n": 60,
      "mean": 0.005290080802535975,
      "std": 0.0017328646814632274,
      "median": 0.004811718850663574,
      "q05": 0.003342152030782086,
      "q25": 0.0039727137375259285,
      "q75": 0.0063732040221056874,
      "q95": 0.008801561768492125,
      "min": 0.0009399477806788512,
      "max": 0.00909756352609014
    },
    "symmetric_difference_cells": {
      "n": 60,
      "mean": 50.6,
      "std": 16.571570509536578,
      "median": 46.0,
      "q05": 31.95,
      "q25": 38.0,
      "q75": 61.0,
      "q95": 84.1,
      "min": 9.0,
      "max": 87.0
    },
    "values": [
      0.003868269733403032,
      0.004597220771079302,
      0.0037621486048698923,
      0.004807692307692308,
      0.0038690787409808637,
      0.00909756352609014,
      0.005955490544352732,
      0.0032447142558090854,
      0.0044960267670430785,
      0.008792128951224618,
      0.0052328623757195184,
      0.0009399477806788512,
      0.005014625992478061,
      0.0047130289065772935,
      0.007422895974908521,
      0.004914775698002719,
      0.005433079093093721,
      0.004181913225300575,
      0.009091859128435574,
      0.003972817564035547,
      0.005952380952380952,
      0.006176070344394431,
      0.006693860474845727,
      0.003766084318443352,
      0.0038686741948975325,
      0.007320644216691069,
      0.004177982034677251,
      0.0058503969912244045,
      0.0069959277435522604,
      0.003972402257997073,
      0.0035509138381201043,
      0.006792058516196447,
      0.00490912889074577,
      0.004815745393634841,
      0.00282190635451505,
      0.004497907949790795,
      0.006902321690023008,
      0.008697474588703761,
      0.006797030220642058,
      0.00439146800501882,
      0.004387339392040113,
      0.00898078529657477,
      0.004708097928436911,
      0.005437624176513646,
      0.0033476305052829794,
      0.007322941730306517,
      0.004709576138147566,
      0.00804345555207354,
      0.003760183831209526,
      0.004497907949790795,
      0.005226298735235706,
      0.004178418468609631,
      0.0035520267446719597,
      0.005642633228840125,
      0.005858353384245214,
      0.0038662486938349006,
      0.004703177257525084,
      0.006266318537859008,
      0.007210031347962382,
      0.0033472803347280333
    ]
  },
  "comparison": {
    "treatment_minus_null_mean": -0.0014746360681055248,
    "pairwise_superiority_probability": 0.1975,
    "treatment_median_exceeds_null_q95": false,
    "interpretation": "The checkpoint is an executable branch point regardless of effect size. Environmental divergence is unusually large only if the treatment distribution clearly exceeds the stochastic-null distribution."
  },
  "figure_branches": "static\\images\\books\\digital-life\\ch15-06-counterfactual-branches.png",
  "figure_divergence": "static\\images\\books\\digital-life\\ch15-06-counterfactual-divergence.png",
  "figure_stochastic_null": "static\\images\\books\\digital-life\\ch15-06-counterfactual-null.png"
}
```

Figures:
- `static\images\books\digital-life\ch15-06-counterfactual-branches.png`
- `static\images\books\digital-life\ch15-06-counterfactual-divergence.png`
- `static\images\books\digital-life\ch15-06-counterfactual-null.png`

The branch-point capability is supported whenever the checkpoint can be restored
and deliberately driven into alternative futures. A stronger claim that the
environmental treatment creates *unusually large* divergence should be made only
if the treatment distribution clearly exceeds the stochastic null.

## Stage 7 — Experimental Verdict

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
