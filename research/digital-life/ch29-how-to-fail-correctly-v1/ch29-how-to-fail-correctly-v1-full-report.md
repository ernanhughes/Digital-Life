# Chapter 29 — How to Fail Correctly (V1)

## Run metadata

```json
{
  "experiment_version": "digital-life-how-to-fail-correctly-v1",
  "schema_version": 1,
  "chapter": 29,
  "chapter_title": "How to Fail Correctly",
  "repo_root": "C:\\Projects\\working-book",
  "registered_cases": 10,
  "registered_identities": 8,
  "started_at_unix": 1786662583.4070964,
  "finished_at_unix": 1786662583.629123,
  "final_status": "FAILURE_LEDGER_CONSISTENT"
}
```

---

## Stage 0 — Frozen Chapter 29 Protocol

```json
{
  "status": "FROZEN",
  "primary_question": "Can experiment failures be classified without conflating invalid runs, unresolved results, precision-bounded negatives, and supported results narrowed by stronger controls?",
  "primary_gate": "Every registered evidence transition obeys the failure-ledger consistency rules.",
  "forbidden_moves": [
    "count INVALID as evidence against hypothesis",
    "count CI-crossing-zero as FAILED",
    "call bounded negative without explicit meaningful threshold",
    "erase valid sub-results when a larger inference is invalid",
    "promote descriptive closeout into confirmatory rescue",
    "silently change estimand or control after seeing result"
  ],
  "stop_rule": "No new Digital Crystal simulation is added merely to rescue a weakened methodological example."
}
```

---

## Stage 1 — Artifact Availability

```json
{
  "cases": [
    {
      "case_id": "CH26_V1_PRIMARY",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-matched-rate-causal-amplification-v1\\ch26-matched-rate-causal-amplification-v1-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\ch26-v1-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\ch26-v1-audit-report.md"
      ]
    },
    {
      "case_id": "CH26_V2_PRIMARY",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-dynamically-matched-rate-causal-amplification-v2\\ch26-dynamically-matched-rate-causal-amplification-v2-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-analytic-audit\\ch26-v2-analytic-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-analytic-audit\\ch26-v2-analytic-audit-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-mechanism-audit\\ch26-v2-mechanism-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-mechanism-audit\\ch26-v2-mechanism-audit-report.md"
      ]
    },
    {
      "case_id": "CH26_V2_MECHANISM",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\audit-a-true-unbounded-contrast.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\audit-b-per-lag-rate-drift.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\ch26-v1-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v1-audit\\ch26-v1-audit-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-analytic-audit\\ch26-v2-analytic-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-analytic-audit\\ch26-v2-analytic-audit-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-mechanism-audit\\ch26-v2-mechanism-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch26-v2-mechanism-audit\\ch26-v2-mechanism-audit-report.md"
      ]
    },
    {
      "case_id": "CH27_V1_PRIMARY",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-decaying-material-history-causal-response-v1\\ch27-decaying-material-history-causal-response-v1-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v1-construct-validity-audit\\ch27-v1-construct-validity-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v1-construct-validity-audit\\ch27-v1-construct-validity-audit-report.md"
      ]
    },
    {
      "case_id": "CH27_V1_IMMEDIATE",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v1-construct-validity-audit\\ch27-v1-construct-validity-audit-report.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v1-construct-validity-audit\\ch27-v1-construct-validity-audit-report.md"
      ]
    },
    {
      "case_id": "CH27_V2_DIRECTION",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-decaying-material-history-causal-response-v2\\ch27-decaying-material-history-causal-response-v2-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v2-trajectory-closeout-audit\\ch27-v2-trajectory-closeout-audit.json"
      ]
    },
    {
      "case_id": "CH27_V2_MAGNITUDE",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-decaying-material-history-causal-response-v2\\ch27-decaying-material-history-causal-response-v2-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v2-trajectory-closeout-audit\\ch27-v2-trajectory-closeout-audit.json"
      ]
    },
    {
      "case_id": "CH27_V2_CLOSEOUT",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v2-trajectory-closeout-audit\\ch27-v2-trajectory-closeout-audit.json",
        "C:\\Projects\\working-book\\research\\digital-life\\ch27-v2-trajectory-closeout-audit\\ch27-v2-trajectory-closeout-audit.md"
      ]
    },
    {
      "case_id": "CH28_V1_RAW",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch28-causal-modularity-v1\\ch28-causal-modularity-v1-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch28-causal-modularity-v1\\stage-03-primary.json"
      ]
    },
    {
      "case_id": "CH28_V2_EXCESS",
      "status": "FOUND",
      "paths": [
        "C:\\Projects\\working-book\\research\\digital-life\\ch28-causal-modularity-v2\\ch28-causal-modularity-v2-full-report.md",
        "C:\\Projects\\working-book\\research\\digital-life\\ch28-causal-modularity-v2\\stage-04-primary.json"
      ]
    }
  ],
  "found_count": 10,
  "manual_evidence_only_count": 0,
  "missing_source_count": 0,
  "rule": "Missing artifacts are never replaced with invented artifact-derived values."
}
```

---

## Stage 2 — Failure Ledger

```json
{
  "rows": [
    {
      "case_id": "CH26_V1_PRIMARY",
      "chapter": 26,
      "experiment": "V1 matched-rate causal amplification",
      "claim": "Initial matched-rate implementation could identify causal amplification relative to exhaustive evaluation.",
      "artifact_status": "FOUND",
      "artifact_count": 3,
      "validity": "INVALID_REFERENCE",
      "inferential_status": "INVALID",
      "transition_type": "IMPLEMENTATION_INVALIDATION",
      "evidence_role": "UNINFORMATIVE",
      "confirmatory": true,
      "threshold": null,
      "expected_mean": null,
      "expected_ci_low": null,
      "expected_ci_high": null,
      "expected_mde": null,
      "mean_visible_in_artifact": null,
      "ci_low_visible_in_artifact": null,
      "ci_high_visible_in_artifact": null,
      "mde_visible_in_artifact": null,
      "threshold_visible_in_artifact": null,
      "surviving_evidence": "No confirmatory primary inference preserved from V1. The design failure itself is retained as methodological evidence.",
      "failure_lesson": "A controlled initial condition is not a controlled process; the exhaustive reference must actually be exhaustive.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH26_V2_PRIMARY",
      "chapter": 26,
      "experiment": "V2 dynamically matched-rate causal amplification",
      "claim": "Strong candidate subsampling changes twelve-step causal consequence relative to true exhaustive evaluation by a meaningful magnitude.",
      "artifact_status": "FOUND",
      "artifact_count": 5,
      "validity": "VALID",
      "inferential_status": "BOUNDED_NEAR_ZERO",
      "transition_type": "PRECISION_RESOLUTION",
      "evidence_role": "REFUTES",
      "confirmatory": true,
      "threshold": 0.15,
      "expected_mean": 0.001302,
      "expected_ci_low": -0.08984,
      "expected_ci_high": 0.08854,
      "expected_mde": 0.115,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": true,
      "threshold_visible_in_artifact": true,
      "surviving_evidence": "Immediate causal routing changed substantially even though twelve-step mean amplification was bounded near zero.",
      "failure_lesson": "CAUSAL ROUTING != CAUSAL AMPLIFICATION.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH26_V2_MECHANISM",
      "chapter": 26,
      "experiment": "V2 mechanism audit",
      "claim": "Evaluation breadth reroutes immediate causal influence between force-only opportunities and shared probability shifts.",
      "artifact_status": "FOUND",
      "artifact_count": 8,
      "validity": "VALID",
      "inferential_status": "DESCRIPTIVE_ONLY",
      "transition_type": "MECHANISTIC_DECOMPOSITION",
      "evidence_role": "PRESERVES_SUBRESULT",
      "confirmatory": false,
      "threshold": null,
      "expected_mean": null,
      "expected_ci_low": null,
      "expected_ci_high": null,
      "expected_mde": null,
      "mean_visible_in_artifact": null,
      "ci_low_visible_in_artifact": null,
      "ci_high_visible_in_artifact": null,
      "mde_visible_in_artifact": null,
      "threshold_visible_in_artifact": null,
      "surviving_evidence": "The null amplification result does not erase mechanistic rerouting of the immediate effect.",
      "failure_lesson": "A negative aggregate result can coexist with a strong change in causal pathway.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH27_V1_PRIMARY",
      "chapter": 27,
      "experiment": "V1 stored material history downstream effect",
      "claim": "Accessible stored material changes twelve-step downstream causal consequence.",
      "artifact_status": "FOUND",
      "artifact_count": 3,
      "validity": "INVALID_IMPLEMENTATION",
      "inferential_status": "INVALID",
      "transition_type": "IMPLEMENTATION_INVALIDATION",
      "evidence_role": "UNINFORMATIVE",
      "confirmatory": true,
      "threshold": 0.15,
      "expected_mean": -0.20833,
      "expected_ci_low": -0.5026,
      "expected_ci_high": 0.07118,
      "expected_mde": null,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": false,
      "mde_visible_in_artifact": null,
      "threshold_visible_in_artifact": false,
      "surviving_evidence": "The twelve-step primary is invalid because PREVENT did not explicitly exclude x at lag 1.",
      "failure_lesson": "An intervention implementation defect invalidates the affected estimand; it is not evidence against the hypothesis.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH27_V1_IMMEDIATE",
      "chapter": 27,
      "experiment": "V1 immediate E1 effect",
      "claim": "Locally accessible decaying material reduces immediate causal sensitivity under matched visible geometry.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "SUPPORTED",
      "transition_type": "MECHANISTIC_DECOMPOSITION",
      "evidence_role": "PRESERVES_SUBRESULT",
      "confirmatory": false,
      "threshold": null,
      "expected_mean": -0.0182264,
      "expected_ci_low": -0.020142,
      "expected_ci_high": -0.016343,
      "expected_mde": null,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": null,
      "threshold_visible_in_artifact": null,
      "surviving_evidence": "Immediate effect survives even though the downstream V1 primary is invalid.",
      "failure_lesson": "Invalidate only the inference touched by the defect; preserve independently valid sub-results.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH27_V2_DIRECTION",
      "chapter": 27,
      "experiment": "V2 corrected stored-material downstream effect",
      "claim": "Accessible stored material produces a negative downstream causal difference.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "DIRECTION_SUPPORTED",
      "transition_type": "REPLICATION",
      "evidence_role": "SUPPORTS",
      "confirmatory": true,
      "threshold": 0.15,
      "expected_mean": -0.3972453,
      "expected_ci_low": -0.67859,
      "expected_ci_high": -0.11922,
      "expected_mde": 0.35706,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": true,
      "threshold_visible_in_artifact": false,
      "surviving_evidence": "Direction is supported under corrected intervention semantics.",
      "failure_lesson": "A confidence interval excluding zero can support direction while still failing a frozen minimum-magnitude precision requirement.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH27_V2_MAGNITUDE",
      "chapter": 27,
      "experiment": "V2 frozen minimum-magnitude claim",
      "claim": "The downstream causal difference is established at the frozen +/-0.15 minimum meaningful magnitude.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "UNRESOLVED",
      "transition_type": "PRECISION_LIMIT",
      "evidence_role": "UNINFORMATIVE",
      "confirmatory": true,
      "threshold": 0.15,
      "expected_mean": -0.3972453,
      "expected_ci_low": -0.67859,
      "expected_ci_high": -0.11922,
      "expected_mde": 0.35706,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": true,
      "threshold_visible_in_artifact": false,
      "surviving_evidence": "Directional negative effect remains supported; only the frozen minimum-magnitude claim is unresolved.",
      "failure_lesson": "DIRECTIONAL EFFECT != ESTABLISHED MINIMUM MAGNITUDE.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH27_V2_CLOSEOUT",
      "chapter": 27,
      "experiment": "V2 trajectory persistence closeout",
      "claim": "A substantial fraction of downstream causal difference continues to accumulate after material mass has weakened.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "DESCRIPTIVE_ONLY",
      "transition_type": "DESCRIPTIVE_CLOSEOUT",
      "evidence_role": "PRESERVES_SUBRESULT",
      "confirmatory": false,
      "threshold": null,
      "expected_mean": null,
      "expected_ci_low": null,
      "expected_ci_high": null,
      "expected_mde": null,
      "mean_visible_in_artifact": null,
      "ci_low_visible_in_artifact": null,
      "ci_high_visible_in_artifact": null,
      "mde_visible_in_artifact": null,
      "threshold_visible_in_artifact": null,
      "surviving_evidence": "Trajectory-persistence descriptor retained as descriptive; it does not rescue the unresolved magnitude claim.",
      "failure_lesson": "A post hoc mechanistic closeout may explain a trajectory without changing the confirmatory status.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH28_V1_RAW",
      "chapter": 28,
      "experiment": "V1 raw causal modularity",
      "claim": "Radius-4 regions exhibit strong internal-retention versus external-penetration asymmetry.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "SUPPORTED",
      "transition_type": "REPLICATION",
      "evidence_role": "SUPPORTS",
      "confirmatory": true,
      "threshold": 0.15,
      "expected_mean": 0.4402085598899139,
      "expected_ci_low": 0.4193782331581624,
      "expected_ci_high": 0.4614487176025127,
      "expected_mde": 0.026781316840711427,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": true,
      "threshold_visible_in_artifact": true,
      "surviving_evidence": "Raw spatial causal containment asymmetry is real and preserved.",
      "failure_lesson": "A large, precise effect can still be construct-confounded.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    },
    {
      "case_id": "CH28_V2_EXCESS",
      "chapter": 28,
      "experiment": "V2 geometry-matched excess causal modularity",
      "claim": "V1-selected radius-4 regions are causally privileged relative to same-checkpoint geometry-matched controls by > +0.10.",
      "artifact_status": "FOUND",
      "artifact_count": 2,
      "validity": "VALID",
      "inferential_status": "BOUNDED_BELOW_SEI",
      "transition_type": "CONTROL_STRENGTHENING",
      "evidence_role": "NARROWS_CLAIM",
      "confirmatory": true,
      "threshold": 0.1,
      "expected_mean": -0.012264901112053186,
      "expected_ci_low": -0.032729925902717345,
      "expected_ci_high": 0.007196615033407114,
      "expected_mde": 0.0264797920616916,
      "mean_visible_in_artifact": true,
      "ci_low_visible_in_artifact": true,
      "ci_high_visible_in_artifact": true,
      "mde_visible_in_artifact": true,
      "threshold_visible_in_artifact": true,
      "surviving_evidence": "V1 raw containment survives. What fails is the stronger interpretation that selected regions are privileged causal individuals relative to matched geometry.",
      "failure_lesson": "CAUSAL RETENTION != CAUSAL INDIVIDUATION.",
      "rule_invalid_not_negative": true,
      "rule_unresolved_not_failed": true,
      "rule_bounded_requires_threshold": true,
      "rule_bounded_requires_precision": true,
      "rule_surviving_evidence_recorded": true,
      "rule_descriptive_not_confirmatory": true,
      "rule_taxonomy_valid": true,
      "case_consistent": true
    }
  ]
}
```

---

## Stage 3 — Epistemic Consistency Audit

```json
{
  "case_rule_pass_count": 10,
  "case_rule_total": 10,
  "all_case_rules_pass": true,
  "cross_checks": [
    {
      "check_id": "X001",
      "name": "Invalid primary preserves independent sub-result",
      "pass": true,
      "cases": [
        "CH27_V1_PRIMARY",
        "CH27_V1_IMMEDIATE"
      ]
    },
    {
      "check_id": "X002",
      "name": "Direction separated from minimum magnitude",
      "pass": true,
      "cases": [
        "CH27_V2_DIRECTION",
        "CH27_V2_MAGNITUDE"
      ]
    },
    {
      "check_id": "X003",
      "name": "Stronger control narrows claim without erasing raw phenomenon",
      "pass": true,
      "cases": [
        "CH28_V1_RAW",
        "CH28_V2_EXCESS"
      ]
    },
    {
      "check_id": "X004",
      "name": "Bounded aggregate result preserves mechanistic rerouting",
      "pass": true,
      "cases": [
        "CH26_V2_PRIMARY",
        "CH26_V2_MECHANISM"
      ]
    },
    {
      "check_id": "X005",
      "name": "Descriptive closeout does not rescue confirmatory magnitude claim",
      "pass": true,
      "cases": [
        "CH27_V2_CLOSEOUT",
        "CH27_V2_MAGNITUDE"
      ]
    }
  ],
  "all_cross_checks_pass": true,
  "no_missing_required_sources": true,
  "manual_evidence_only_is_allowed": true,
  "primary_gate_pass": true
}
```

---

## Stage 4 — Failure Principles

```json
{
  "chapter_26": {
    "lesson": "A controlled initial condition is not a controlled process.",
    "construct_identity": "CAUSAL ROUTING != CAUSAL AMPLIFICATION"
  },
  "chapter_27": {
    "lesson": "Invalidate only the affected estimand; preserve independently valid sub-results.",
    "construct_identity": "DIRECTIONAL EFFECT != ESTABLISHED MINIMUM MAGNITUDE"
  },
  "chapter_28": {
    "lesson": "A large precise effect can still be construct-confounded.",
    "construct_identity": "CAUSAL RETENTION != CAUSAL INDIVIDUATION"
  },
  "general_rules": [
    "NULL RESULT != INVALID EXPERIMENT",
    "INVALID EXPERIMENT != NEGATIVE RESULT",
    "NONSIGNIFICANT != FAILED",
    "PRECISE NEGATIVE RESULT != NOTHING HAPPENED",
    "SUPPORTED LOWER-LEVEL PHENOMENON MAY SURVIVE A FAILED HIGHER-LEVEL INTERPRETATION",
    "DESCRIPTIVE EXPLANATION MUST NOT RESCUE A FROZEN CONFIRMATORY CLAIM"
  ],
  "construct_identities": [
    {
      "identity_id": "I001",
      "chapter": "17",
      "lhs": "MARGINAL EFFECT",
      "rhs": "AVERAGE PAIRED EFFECT",
      "lesson": "Different estimands must not be substituted."
    },
    {
      "identity_id": "I002",
      "chapter": "17",
      "lhs": "AVERAGE PAIRED EFFECT",
      "rhs": "PATHWISE DIVERGENCE",
      "lesson": "Branch divergence does not imply a systematic average effect."
    },
    {
      "identity_id": "I003",
      "chapter": "17",
      "lhs": "CAUSAL DIFFERENCE",
      "rhs": "SYSTEMATIC SIGNATURE",
      "lesson": "A causal intervention can matter without yielding a stable decoder."
    },
    {
      "identity_id": "I004",
      "chapter": "19",
      "lhs": "PERSISTENT TRACE",
      "rhs": "READABLE TRACE",
      "lesson": "Persistence is not evidence of usable memory."
    },
    {
      "identity_id": "I005",
      "chapter": "20",
      "lhs": "ATTACHMENT",
      "rhs": "NEW CONSTRUCTION",
      "lesson": "Reoccupation must not be counted as first construction."
    },
    {
      "identity_id": "I006",
      "chapter": "20",
      "lhs": "REOCCUPATION",
      "rhs": "REPAIR",
      "lesson": "Ordinary growth into a vacancy does not establish repair."
    },
    {
      "identity_id": "I007",
      "chapter": "26",
      "lhs": "CAUSAL ROUTING",
      "rhs": "CAUSAL AMPLIFICATION",
      "lesson": "A pathway can change while aggregate consequence remains matched."
    },
    {
      "identity_id": "I008",
      "chapter": "28",
      "lhs": "CAUSAL RETENTION",
      "rhs": "CAUSAL INDIVIDUATION",
      "lesson": "Observer-chosen containment does not establish a privileged boundary."
    }
  ]
}
```

---

## Stage 5 — Chapter 29 V1 Verdict

```json
{
  "status": "FAILURE_LEDGER_CONSISTENT",
  "primary_gate": {
    "case_rule_pass_count": 10,
    "case_rule_total": 10,
    "all_case_rules_pass": true,
    "cross_checks": [
      {
        "check_id": "X001",
        "name": "Invalid primary preserves independent sub-result",
        "pass": true,
        "cases": [
          "CH27_V1_PRIMARY",
          "CH27_V1_IMMEDIATE"
        ]
      },
      {
        "check_id": "X002",
        "name": "Direction separated from minimum magnitude",
        "pass": true,
        "cases": [
          "CH27_V2_DIRECTION",
          "CH27_V2_MAGNITUDE"
        ]
      },
      {
        "check_id": "X003",
        "name": "Stronger control narrows claim without erasing raw phenomenon",
        "pass": true,
        "cases": [
          "CH28_V1_RAW",
          "CH28_V2_EXCESS"
        ]
      },
      {
        "check_id": "X004",
        "name": "Bounded aggregate result preserves mechanistic rerouting",
        "pass": true,
        "cases": [
          "CH26_V2_PRIMARY",
          "CH26_V2_MECHANISM"
        ]
      },
      {
        "check_id": "X005",
        "name": "Descriptive closeout does not rescue confirmatory magnitude claim",
        "pass": true,
        "cases": [
          "CH27_V2_CLOSEOUT",
          "CH27_V2_MAGNITUDE"
        ]
      }
    ],
    "all_cross_checks_pass": true,
    "no_missing_required_sources": true,
    "manual_evidence_only_is_allowed": true,
    "primary_gate_pass": true
  },
  "bounded_claim": "Across the registered Chapter 26-28 case chains, invalid implementations, unresolved inferential questions, precision-bounded negative results, descriptive closeouts, and stronger-control claim narrowings can be represented without erasing surviving evidence or converting one evidence class into another.",
  "what_this_does_not_establish": [
    "that the project never made mistakes",
    "that the registered taxonomy is universally complete",
    "that these cases prove a general philosophy of science",
    "that every future experiment can be classified without ambiguity"
  ],
  "chapter_principle": "Fail the smallest claim justified by the evidence. Preserve everything that still survives."
}
```
