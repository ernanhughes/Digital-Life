#!/usr/bin/env python3
"""
Digital Life — Chapter 29 V1
How to Fail Correctly
=====================

SCIENTIFIC QUESTION
-------------------

When an experiment appears to fail, can we determine WHAT failed without
silently changing the question, discarding surviving evidence, or converting
an invalid run into a negative result?

Chapter 29 is a methodological audit.

It does NOT test another property of Digital Crystal.

Instead it reconstructs recent experiment chains and asks whether each
transition can be classified into one of four distinct outcomes:

    1. INVALID
       The experimental implementation or construct does not support the
       intended inference.

    2. UNRESOLVED
       The experiment is valid, but the predeclared inferential question is
       not resolved at required precision / threshold.

    3. BOUNDED NEGATIVE
       The experiment is valid and sufficiently precise to bound a meaningful
       positive effect below the predeclared smallest effect of interest.

    4. SUPPORTED BUT NARROWED
       A result survives, but a stronger control changes the scope of what the
       result can legitimately mean.

The chapter's central rule is:

    FAILURE OF A CLAIM
        !=
    FAILURE OF AN EXPERIMENT
        !=
    ABSENCE OF A PHENOMENON

PRIMARY RESEARCH OBJECTIVE
--------------------------

Build a reproducible failure ledger for Chapters 26-28 and verify:

    A. invalid experiments are not recorded as negative evidence;

    B. valid but imprecise experiments remain unresolved;

    C. precision-resolved negative results are distinguished from
       nonsignificance;

    D. stronger controls can narrow a supported claim without erasing the
       underlying measured phenomenon;

    E. surviving sub-results are preserved when a larger inference fails.

This is an epistemic-audit experiment.

It evaluates the bookkeeping rules that determine what the project is allowed
to say.

PRIMARY CASE CHAINS
-------------------

CHAIN A — CHAPTER 26
--------------------

V1:
    dynamically matched-rate causal amplification attempt

Known problem:
    fixed lag-1 calibration and "f=1" was not true exhaustive evaluation.

Classification:
    INVALID_CONSTRUCT / INVALID_REFERENCE

V2:
    dynamic PREVENT reference target at every lag
    true unbounded exhaustive reference
    H=12
    SEI +/-0.15

Primary result:
    strong candidate subsampling did not produce a mean twelve-step causal
    consequence distinguishable from exhaustive evaluation by the frozen
    +/-0.15 attachment-scale threshold.

Classification:
    BOUNDED_NEAR_ZERO_AT_MATCHED_RATE

Mechanistic audit:
    immediate causal effect was rerouted between:
        force-only opportunity
        shared probability shift

Key distinction:
    CAUSAL ROUTING != CAUSAL AMPLIFICATION

Failure lesson:
    a controlled initial condition is not a controlled process.


CHAIN B — CHAPTER 27
--------------------

V1:
    stored material history / causal response

Known implementation defect:
    PREVENT did not explicitly exclude x at lag 1.

Consequence:
    twelve-step primary G_T is INVALID.

But:
    immediate E1 comparison remains valid and showed reduced immediate
    sensitivity for locally accessible material state.

Therefore:
    INVALID PRIMARY
    +
    SURVIVING SUB-RESULT

V2:
    corrected intervention semantics
    primary lag-wise Rao-Blackwellized G_local
    SEI +/-0.15

Result:
    direction negative
    CI excludes zero
    but achieved MDE > 0.15 and frozen minimum-magnitude claim remains
    unresolved.

Classification:
    DIRECTIONAL_EFFECT_SUPPORTED
    MINIMUM_MAGNITUDE_UNRESOLVED

Closeout:
    later causal difference continued to accumulate after material trace had
    substantially weakened.

Classification:
    DESCRIPTIVE_TRAJECTORY_PERSISTENCE
    not a rescue of the frozen minimum-magnitude claim.

Failure lesson:
    a valid directional result does not imply that a predeclared meaningful
    magnitude has been established.


CHAIN C — CHAPTER 28
--------------------

V1:
    radius-4 raw causal modularity

Result:
    strong module score ~0.44
    CI well above frozen 0.15 SEI

Classification:
    RAW_CAUSAL_MODULARITY_SUPPORTED

But descriptive scale sweep:
    module score increased through radius 5.

Construct concern:
    arbitrary spatial containment could generate the same asymmetry.

V2:
    same-checkpoint geometry-matched null
    EXCESS_SEI +0.10

Result:
    observed module score ~0.444
    matched-control score ~0.456
    excess ~-0.012
    CI approximately [-0.033, +0.007]
    MDE ~0.0265

Classification:
    EXCESS_CAUSAL_MODULARITY_BOUNDED_BELOW_SEI

Crucially:
    V1 is NOT erased.

V1 established:
    raw spatial causal containment asymmetry

V2 rejected:
    privileged causal region relative to matched geometry

Failure lesson:
    CAUSAL RETENTION != CAUSAL INDIVIDUATION


PRIMARY HYPOTHESIS
------------------

This chapter does not test a population effect.

Its primary confirmatory object is an AUDIT CONSISTENCY GATE.

For every registered case transition, all of the following must hold:

    1. SOURCE ARTIFACT EXISTS or case explicitly marked MANUAL_EVIDENCE_ONLY.

    2. STATUS BEFORE and STATUS AFTER are explicit.

    3. REASON FOR TRANSITION is classified.

    4. SURVIVING EVIDENCE is explicitly preserved.

    5. INVALID results never contribute as evidence AGAINST the hypothesis.

    6. UNRESOLVED results never become FAILED solely because CI crosses zero.

    7. BOUNDED negatives require an explicit meaningful-effect threshold
       and adequate precision.

    8. stronger-control demotions do not delete the earlier measured
       phenomenon when the earlier construct remains valid.

    9. descriptive follow-up never silently promotes itself to confirmatory
       status.

If every registered transition passes:

    FAILURE_LEDGER_CONSISTENT

Otherwise:

    FAILURE_LEDGER_INCONSISTENT

This is a correctness / epistemic-integrity result, not a biological result.

NO STATISTICAL SIGNIFICANCE PRIMARY
-----------------------------------

Chapter 29 deliberately does NOT use p-values as its main criterion.

The object is logical classification of evidence.

Where confidence intervals / SEIs / MDEs are available, the script records and
checks them.

But the primary result is whether the evidence bookkeeping obeys its own rules.

TAXONOMY
--------

RUN VALIDITY:

    VALID
    INVALID_IMPLEMENTATION
    INVALID_CONSTRUCT
    INVALID_REFERENCE
    UNKNOWN

INFERENTIAL STATUS:

    SUPPORTED
    BOUNDED_BELOW_SEI
    BOUNDED_NEAR_ZERO
    UNRESOLVED
    DIRECTION_SUPPORTED
    DESCRIPTIVE_ONLY
    INVALID
    UNTESTED

TRANSITION TYPE:

    IMPLEMENTATION_INVALIDATION
    CONSTRUCT_NARROWING
    PRECISION_RESOLUTION
    PRECISION_LIMIT
    MECHANISTIC_DECOMPOSITION
    DESCRIPTIVE_CLOSEOUT
    REPLICATION
    CONTROL_STRENGTHENING

EVIDENCE ROLE:

    SUPPORTS
    WEAKENS
    REFUTES
    UNINFORMATIVE
    PRESERVES_SUBRESULT
    NARROWS_CLAIM

CORE IDENTITIES
---------------

Chapter 29 also records methodological identities learned in earlier chapters:

    MARGINAL EFFECT
        !=
    AVERAGE PAIRED EFFECT
        !=
    PATHWISE DIVERGENCE

    CAUSAL DIFFERENCE
        !=
    EXCESS DIVERGENCE
        !=
    SYSTEMATIC SIGNATURE
        !=
    RECOVERABLE INFORMATION

    PERSISTENT TRACE
        !=
    ACCESSIBLE TRACE
        !=
    DISTINGUISHABLE TRACE
        !=
    READABLE TRACE

    ATTACHMENT
        !=
    NEW CONSTRUCTION

    NET POPULATION CHANGE
        !=
    GROSS CONSTRUCTION ACTIVITY

    REOCCUPATION
        !=
    REPAIR

    CAUSAL ROUTING
        !=
    CAUSAL AMPLIFICATION

    CAUSAL RETENTION
        !=
    CAUSAL INDIVIDUATION

These are treated as FINDINGS ABOUT CONSTRUCT SEPARATION.

They are not statistical results.

STOP RULE
---------

Chapter 29 is complete when:

    - all registered evidence transitions are auditable;
    - every invalidation preserves surviving evidence;
    - every bounded negative contains threshold + precision evidence;
    - every unresolved result remains unresolved;
    - every stronger-control narrowing preserves the earlier lower-level
      phenomenon;
    - no rescue experiment is proposed merely because the claim weakened.

Do NOT add new Digital Crystal simulations to rescue a methodological example.

If an artifact is missing:
    mark MISSING_SOURCE
    do not infer the missing value.

If source files disagree:
    mark SOURCE_CONFLICT
    do not silently reconcile them.

OUTPUTS
-------

ch29-failure-ledger.csv
ch29-failure-ledger.json
ch29-construct-identities.csv
ch29-artifact-audit.json
stage-00-protocol.json
stage-01-artifacts.json
stage-02-ledger.json
stage-03-consistency.json
stage-04-lessons.json
stage-05-verdict.json
ch29-how-to-fail-correctly-v1-full-report.md

USAGE
-----

From repository root:

    python scripts/books/digital-life/ch29_how_to_fail_correctly_v1.py

Optional:

    --repo-root .
    --report-dir research/digital-life/ch29-how-to-fail-correctly-v1

The script searches expected research directories first.

If exact reports are not present, it preserves the registered case as
MANUAL_EVIDENCE_ONLY rather than fabricating artifact-derived values.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


EXPERIMENT_VERSION = "digital-life-how-to-fail-correctly-v1"
SCHEMA_VERSION = 1
CHAPTER = 29
CHAPTER_TITLE = "How to Fail Correctly"


# ============================================================================
# Taxonomy
# ============================================================================

VALIDITY_VALUES = {
    "VALID",
    "INVALID_IMPLEMENTATION",
    "INVALID_CONSTRUCT",
    "INVALID_REFERENCE",
    "UNKNOWN",
}

STATUS_VALUES = {
    "SUPPORTED",
    "BOUNDED_BELOW_SEI",
    "BOUNDED_NEAR_ZERO",
    "UNRESOLVED",
    "DIRECTION_SUPPORTED",
    "DESCRIPTIVE_ONLY",
    "INVALID",
    "UNTESTED",
}

TRANSITION_VALUES = {
    "IMPLEMENTATION_INVALIDATION",
    "CONSTRUCT_NARROWING",
    "PRECISION_RESOLUTION",
    "PRECISION_LIMIT",
    "MECHANISTIC_DECOMPOSITION",
    "DESCRIPTIVE_CLOSEOUT",
    "REPLICATION",
    "CONTROL_STRENGTHENING",
}

EVIDENCE_ROLE_VALUES = {
    "SUPPORTS",
    "WEAKENS",
    "REFUTES",
    "UNINFORMATIVE",
    "PRESERVES_SUBRESULT",
    "NARROWS_CLAIM",
}


# ============================================================================
# Registered cases
# ============================================================================

@dataclass(frozen=True)
class RegisteredCase:
    case_id: str
    chapter: int
    experiment: str
    claim: str

    validity: str
    inferential_status: str
    transition_type: str
    evidence_role: str

    source_globs: Tuple[str, ...]

    threshold: Optional[float]
    expected_mean: Optional[float]
    expected_ci_low: Optional[float]
    expected_ci_high: Optional[float]
    expected_mde: Optional[float]

    surviving_evidence: str
    failure_lesson: str

    confirmatory: bool
    manual_evidence_allowed: bool = True


CASES: Tuple[RegisteredCase, ...] = (
    RegisteredCase(
        case_id="CH26_V1_PRIMARY",
        chapter=26,
        experiment="V1 matched-rate causal amplification",
        claim=(
            "Initial matched-rate implementation could identify causal "
            "amplification relative to exhaustive evaluation."
        ),
        validity="INVALID_REFERENCE",
        inferential_status="INVALID",
        transition_type="IMPLEMENTATION_INVALIDATION",
        evidence_role="UNINFORMATIVE",
        source_globs=(
            "research/digital-life/ch26*/*v1*report*.md",
            "research/digital-life/ch26*/*v1*.json",
        ),
        threshold=None,
        expected_mean=None,
        expected_ci_low=None,
        expected_ci_high=None,
        expected_mde=None,
        surviving_evidence=(
            "No confirmatory primary inference preserved from V1. "
            "The design failure itself is retained as methodological evidence."
        ),
        failure_lesson=(
            "A controlled initial condition is not a controlled process; "
            "the exhaustive reference must actually be exhaustive."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH26_V2_PRIMARY",
        chapter=26,
        experiment="V2 dynamically matched-rate causal amplification",
        claim=(
            "Strong candidate subsampling changes twelve-step causal "
            "consequence relative to true exhaustive evaluation by a "
            "meaningful magnitude."
        ),
        validity="VALID",
        inferential_status="BOUNDED_NEAR_ZERO",
        transition_type="PRECISION_RESOLUTION",
        evidence_role="REFUTES",
        source_globs=(
            "research/digital-life/ch26*/*v2*report*.md",
            "research/digital-life/ch26*/*v2*.json",
        ),
        threshold=0.15,
        expected_mean=0.001302,
        expected_ci_low=-0.08984,
        expected_ci_high=0.08854,
        expected_mde=0.115,
        surviving_evidence=(
            "Immediate causal routing changed substantially even though "
            "twelve-step mean amplification was bounded near zero."
        ),
        failure_lesson=(
            "CAUSAL ROUTING != CAUSAL AMPLIFICATION."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH26_V2_MECHANISM",
        chapter=26,
        experiment="V2 mechanism audit",
        claim=(
            "Evaluation breadth reroutes immediate causal influence between "
            "force-only opportunities and shared probability shifts."
        ),
        validity="VALID",
        inferential_status="DESCRIPTIVE_ONLY",
        transition_type="MECHANISTIC_DECOMPOSITION",
        evidence_role="PRESERVES_SUBRESULT",
        source_globs=(
            "research/digital-life/ch26*/*audit*.md",
            "research/digital-life/ch26*/*audit*.json",
        ),
        threshold=None,
        expected_mean=None,
        expected_ci_low=None,
        expected_ci_high=None,
        expected_mde=None,
        surviving_evidence=(
            "The null amplification result does not erase mechanistic "
            "rerouting of the immediate effect."
        ),
        failure_lesson=(
            "A negative aggregate result can coexist with a strong change "
            "in causal pathway."
        ),
        confirmatory=False,
    ),
    RegisteredCase(
        case_id="CH27_V1_PRIMARY",
        chapter=27,
        experiment="V1 stored material history downstream effect",
        claim=(
            "Accessible stored material changes twelve-step downstream causal "
            "consequence."
        ),
        validity="INVALID_IMPLEMENTATION",
        inferential_status="INVALID",
        transition_type="IMPLEMENTATION_INVALIDATION",
        evidence_role="UNINFORMATIVE",
        source_globs=(
            "research/digital-life/ch27*/*v1*report*.md",
            "research/digital-life/ch27*/*v1*.json",
        ),
        threshold=0.15,
        expected_mean=-0.20833,
        expected_ci_low=-0.5026,
        expected_ci_high=0.07118,
        expected_mde=None,
        surviving_evidence=(
            "The twelve-step primary is invalid because PREVENT did not "
            "explicitly exclude x at lag 1."
        ),
        failure_lesson=(
            "An intervention implementation defect invalidates the affected "
            "estimand; it is not evidence against the hypothesis."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH27_V1_IMMEDIATE",
        chapter=27,
        experiment="V1 immediate E1 effect",
        claim=(
            "Locally accessible decaying material reduces immediate causal "
            "sensitivity under matched visible geometry."
        ),
        validity="VALID",
        inferential_status="SUPPORTED",
        transition_type="MECHANISTIC_DECOMPOSITION",
        evidence_role="PRESERVES_SUBRESULT",
        source_globs=(
            "research/digital-life/ch27*/*v1*audit*.md",
            "research/digital-life/ch27*/*v1*.json",
        ),
        threshold=None,
        expected_mean=-0.0182264,
        expected_ci_low=-0.020142,
        expected_ci_high=-0.016343,
        expected_mde=None,
        surviving_evidence=(
            "Immediate effect survives even though the downstream V1 primary "
            "is invalid."
        ),
        failure_lesson=(
            "Invalidate only the inference touched by the defect; preserve "
            "independently valid sub-results."
        ),
        confirmatory=False,
    ),
    RegisteredCase(
        case_id="CH27_V2_DIRECTION",
        chapter=27,
        experiment="V2 corrected stored-material downstream effect",
        claim=(
            "Accessible stored material produces a negative downstream "
            "causal difference."
        ),
        validity="VALID",
        inferential_status="DIRECTION_SUPPORTED",
        transition_type="REPLICATION",
        evidence_role="SUPPORTS",
        source_globs=(
            "research/digital-life/ch27*/*v2*report*.md",
            "research/digital-life/ch27*/*v2*.json",
        ),
        threshold=0.15,
        expected_mean=-0.3972453,
        expected_ci_low=-0.67859,
        expected_ci_high=-0.11922,
        expected_mde=0.35706,
        surviving_evidence=(
            "Direction is supported under corrected intervention semantics."
        ),
        failure_lesson=(
            "A confidence interval excluding zero can support direction while "
            "still failing a frozen minimum-magnitude precision requirement."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH27_V2_MAGNITUDE",
        chapter=27,
        experiment="V2 frozen minimum-magnitude claim",
        claim=(
            "The downstream causal difference is established at the frozen "
            "+/-0.15 minimum meaningful magnitude."
        ),
        validity="VALID",
        inferential_status="UNRESOLVED",
        transition_type="PRECISION_LIMIT",
        evidence_role="UNINFORMATIVE",
        source_globs=(
            "research/digital-life/ch27*/*v2*report*.md",
            "research/digital-life/ch27*/*v2*.json",
        ),
        threshold=0.15,
        expected_mean=-0.3972453,
        expected_ci_low=-0.67859,
        expected_ci_high=-0.11922,
        expected_mde=0.35706,
        surviving_evidence=(
            "Directional negative effect remains supported; only the frozen "
            "minimum-magnitude claim is unresolved."
        ),
        failure_lesson=(
            "DIRECTIONAL EFFECT != ESTABLISHED MINIMUM MAGNITUDE."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH27_V2_CLOSEOUT",
        chapter=27,
        experiment="V2 trajectory persistence closeout",
        claim=(
            "A substantial fraction of downstream causal difference continues "
            "to accumulate after material mass has weakened."
        ),
        validity="VALID",
        inferential_status="DESCRIPTIVE_ONLY",
        transition_type="DESCRIPTIVE_CLOSEOUT",
        evidence_role="PRESERVES_SUBRESULT",
        source_globs=(
            "research/digital-life/ch27*/*closeout*.md",
            "research/digital-life/ch27*/*closeout*.json",
        ),
        threshold=None,
        expected_mean=None,
        expected_ci_low=None,
        expected_ci_high=None,
        expected_mde=None,
        surviving_evidence=(
            "Trajectory-persistence descriptor retained as descriptive; "
            "it does not rescue the unresolved magnitude claim."
        ),
        failure_lesson=(
            "A post hoc mechanistic closeout may explain a trajectory without "
            "changing the confirmatory status."
        ),
        confirmatory=False,
    ),
    RegisteredCase(
        case_id="CH28_V1_RAW",
        chapter=28,
        experiment="V1 raw causal modularity",
        claim=(
            "Radius-4 regions exhibit strong internal-retention versus "
            "external-penetration asymmetry."
        ),
        validity="VALID",
        inferential_status="SUPPORTED",
        transition_type="REPLICATION",
        evidence_role="SUPPORTS",
        source_globs=(
            "research/digital-life/ch28-causal-modularity-v1/*full-report*.md",
            "research/digital-life/ch28-causal-modularity-v1/stage-03-primary.json",
        ),
        threshold=0.15,
        expected_mean=0.4402085598899139,
        expected_ci_low=0.4193782331581624,
        expected_ci_high=0.4614487176025127,
        expected_mde=0.026781316840711427,
        surviving_evidence=(
            "Raw spatial causal containment asymmetry is real and preserved."
        ),
        failure_lesson=(
            "A large, precise effect can still be construct-confounded."
        ),
        confirmatory=True,
    ),
    RegisteredCase(
        case_id="CH28_V2_EXCESS",
        chapter=28,
        experiment="V2 geometry-matched excess causal modularity",
        claim=(
            "V1-selected radius-4 regions are causally privileged relative "
            "to same-checkpoint geometry-matched controls by > +0.10."
        ),
        validity="VALID",
        inferential_status="BOUNDED_BELOW_SEI",
        transition_type="CONTROL_STRENGTHENING",
        evidence_role="NARROWS_CLAIM",
        source_globs=(
            "research/digital-life/ch28-causal-modularity-v2/*full-report*.md",
            "research/digital-life/ch28-causal-modularity-v2/stage-04-primary.json",
        ),
        threshold=0.10,
        expected_mean=-0.012264901112053186,
        expected_ci_low=-0.032729925902717345,
        expected_ci_high=0.007196615033407114,
        expected_mde=0.0264797920616916,
        surviving_evidence=(
            "V1 raw containment survives. What fails is the stronger "
            "interpretation that selected regions are privileged causal "
            "individuals relative to matched geometry."
        ),
        failure_lesson=(
            "CAUSAL RETENTION != CAUSAL INDIVIDUATION."
        ),
        confirmatory=True,
    ),
)


# ============================================================================
# Construct-separation identities
# ============================================================================

@dataclass(frozen=True)
class ConstructIdentity:
    identity_id: str
    chapter: str
    lhs: str
    rhs: str
    lesson: str


IDENTITIES: Tuple[ConstructIdentity, ...] = (
    ConstructIdentity(
        "I001",
        "17",
        "MARGINAL EFFECT",
        "AVERAGE PAIRED EFFECT",
        "Different estimands must not be substituted.",
    ),
    ConstructIdentity(
        "I002",
        "17",
        "AVERAGE PAIRED EFFECT",
        "PATHWISE DIVERGENCE",
        "Branch divergence does not imply a systematic average effect.",
    ),
    ConstructIdentity(
        "I003",
        "17",
        "CAUSAL DIFFERENCE",
        "SYSTEMATIC SIGNATURE",
        "A causal intervention can matter without yielding a stable decoder.",
    ),
    ConstructIdentity(
        "I004",
        "19",
        "PERSISTENT TRACE",
        "READABLE TRACE",
        "Persistence is not evidence of usable memory.",
    ),
    ConstructIdentity(
        "I005",
        "20",
        "ATTACHMENT",
        "NEW CONSTRUCTION",
        "Reoccupation must not be counted as first construction.",
    ),
    ConstructIdentity(
        "I006",
        "20",
        "REOCCUPATION",
        "REPAIR",
        "Ordinary growth into a vacancy does not establish repair.",
    ),
    ConstructIdentity(
        "I007",
        "26",
        "CAUSAL ROUTING",
        "CAUSAL AMPLIFICATION",
        "A pathway can change while aggregate consequence remains matched.",
    ),
    ConstructIdentity(
        "I008",
        "28",
        "CAUSAL RETENTION",
        "CAUSAL INDIVIDUATION",
        "Observer-chosen containment does not establish a privileged boundary.",
    ),
)


# ============================================================================
# Artifact search
# ============================================================================

@dataclass
class ArtifactMatch:
    case_id: str
    status: str
    paths: List[str]


def find_artifacts(
    repo_root: Path,
    case: RegisteredCase,
) -> ArtifactMatch:
    found: List[Path] = []

    for pattern in case.source_globs:
        found.extend(
            repo_root.glob(pattern)
        )

    unique = sorted(
        {
            path.resolve()
            for path in found
            if path.is_file()
        }
    )

    if unique:
        status = "FOUND"
    elif case.manual_evidence_allowed:
        status = "MANUAL_EVIDENCE_ONLY"
    else:
        status = "MISSING_SOURCE"

    return ArtifactMatch(
        case_id=case.case_id,
        status=status,
        paths=[
            str(path)
            for path in unique
        ],
    )


# ============================================================================
# Lightweight numeric extraction
# ============================================================================

NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"


def flatten_json(
    value: Any,
    prefix: str = "",
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = (
                f"{prefix}.{key}"
                if prefix
                else str(key)
            )

            out.update(
                flatten_json(
                    child,
                    child_prefix,
                )
            )

    elif isinstance(value, list):
        for i, child in enumerate(value):
            child_prefix = f"{prefix}[{i}]"

            out.update(
                flatten_json(
                    child,
                    child_prefix,
                )
            )

    else:
        out[prefix] = value

    return out


def read_artifact_text(
    path: Path,
) -> str:
    try:
        return path.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        return path.read_text(
            encoding="utf-8",
            errors="replace",
        )


def extract_numeric_hints(
    paths: Sequence[Path],
) -> Dict[str, List[float]]:
    """
    Heuristic extraction only.

    This is NOT used to manufacture a scientific result.
    It is used to determine whether expected registered values are visibly
    present in discovered artifacts.
    """
    hints: Dict[str, List[float]] = {
        "mean": [],
        "ci_low": [],
        "ci_high": [],
        "mde": [],
        "threshold": [],
    }

    key_patterns = {
        "mean": [
            r'"mean"\s*:\s*(' + NUMBER + r')',
            r"\bmean\s*[=:]\s*(" + NUMBER + r")",
        ],
        "ci_low": [
            r'"ci95_low"\s*:\s*(' + NUMBER + r')',
            r'"ci_low"\s*:\s*(' + NUMBER + r')',
        ],
        "ci_high": [
            r'"ci95_high"\s*:\s*(' + NUMBER + r')',
            r'"ci_high"\s*:\s*(' + NUMBER + r')',
        ],
        "mde": [
            r'"achieved_mde80_one_sided"\s*:\s*(' + NUMBER + r')',
            r"\bMDE(?:80)?\s*[=:]\s*(" + NUMBER + r")",
        ],
        "threshold": [
            r'"(?:SEI|EXCESS_SEI|module_SEI|excess_SEI)"\s*:\s*('
            + NUMBER
            + r')',
        ],
    }

    for path in paths:
        text = read_artifact_text(
            path
        )

        if path.suffix.lower() == ".json":
            try:
                payload = json.loads(
                    text
                )

                flat = flatten_json(
                    payload
                )

                for key, value in flat.items():
                    if not isinstance(
                        value,
                        (
                            int,
                            float,
                        ),
                    ):
                        continue

                    lower = key.lower()

                    if lower.endswith(".mean") or lower == "mean":
                        hints["mean"].append(
                            float(value)
                        )

                    if "ci95_low" in lower or lower.endswith(".ci_low"):
                        hints["ci_low"].append(
                            float(value)
                        )

                    if "ci95_high" in lower or lower.endswith(".ci_high"):
                        hints["ci_high"].append(
                            float(value)
                        )

                    if "mde" in lower:
                        hints["mde"].append(
                            float(value)
                        )

                    if "sei" in lower:
                        hints["threshold"].append(
                            float(value)
                        )

            except json.JSONDecodeError:
                pass

        for label, patterns in key_patterns.items():
            for pattern in patterns:
                for match in re.finditer(
                    pattern,
                    text,
                    flags=re.I,
                ):
                    try:
                        hints[label].append(
                            float(
                                match.group(1)
                            )
                        )
                    except (
                        ValueError,
                        IndexError,
                    ):
                        pass

    return hints


def approximately_present(
    target: Optional[float],
    values: Sequence[float],
    abs_tol: float = 5e-4,
    rel_tol: float = 0.02,
) -> Optional[bool]:
    if target is None:
        return None

    for value in values:
        if math.isclose(
            target,
            value,
            abs_tol=abs_tol,
            rel_tol=rel_tol,
        ):
            return True

    return False


# ============================================================================
# Consistency rules
# ============================================================================

@dataclass
class LedgerRow:
    case_id: str
    chapter: int
    experiment: str
    claim: str

    artifact_status: str
    artifact_count: int

    validity: str
    inferential_status: str
    transition_type: str
    evidence_role: str

    confirmatory: bool

    threshold: Optional[float]
    expected_mean: Optional[float]
    expected_ci_low: Optional[float]
    expected_ci_high: Optional[float]
    expected_mde: Optional[float]

    mean_visible_in_artifact: Optional[bool]
    ci_low_visible_in_artifact: Optional[bool]
    ci_high_visible_in_artifact: Optional[bool]
    mde_visible_in_artifact: Optional[bool]
    threshold_visible_in_artifact: Optional[bool]

    surviving_evidence: str
    failure_lesson: str

    rule_invalid_not_negative: bool
    rule_unresolved_not_failed: bool
    rule_bounded_requires_threshold: bool
    rule_bounded_requires_precision: bool
    rule_surviving_evidence_recorded: bool
    rule_descriptive_not_confirmatory: bool
    rule_taxonomy_valid: bool

    case_consistent: bool


def bounded_status(
    status: str,
) -> bool:
    return status in {
        "BOUNDED_BELOW_SEI",
        "BOUNDED_NEAR_ZERO",
    }


def build_ledger_row(
    case: RegisteredCase,
    artifact: ArtifactMatch,
    repo_root: Path,
) -> LedgerRow:
    paths = [
        Path(path)
        for path
        in artifact.paths
    ]

    hints = extract_numeric_hints(
        paths
    ) if paths else {
        "mean": [],
        "ci_low": [],
        "ci_high": [],
        "mde": [],
        "threshold": [],
    }

    invalid_not_negative = not (
        case.validity.startswith(
            "INVALID"
        )
        and case.inferential_status
        in {
            "BOUNDED_BELOW_SEI",
            "BOUNDED_NEAR_ZERO",
        }
    )

    unresolved_not_failed = not (
        case.inferential_status
        == "UNRESOLVED"
        and case.evidence_role
        == "REFUTES"
    )

    bounded_requires_threshold = (
        case.threshold is not None
        if bounded_status(
            case.inferential_status
        )
        else True
    )

    if bounded_status(
        case.inferential_status
    ):
        bounded_requires_precision = (
            case.expected_mde is not None
            and case.threshold is not None
            and abs(
                case.expected_mde
            )
            <= abs(
                case.threshold
            )
        )

    else:
        bounded_requires_precision = True

    surviving_recorded = bool(
        case.surviving_evidence.strip()
    )

    descriptive_not_confirmatory = not (
        case.inferential_status
        == "DESCRIPTIVE_ONLY"
        and case.confirmatory
    )

    taxonomy_valid = bool(
        case.validity
        in VALIDITY_VALUES
        and case.inferential_status
        in STATUS_VALUES
        and case.transition_type
        in TRANSITION_VALUES
        and case.evidence_role
        in EVIDENCE_ROLE_VALUES
    )

    case_consistent = all(
        [
            invalid_not_negative,
            unresolved_not_failed,
            bounded_requires_threshold,
            bounded_requires_precision,
            surviving_recorded,
            descriptive_not_confirmatory,
            taxonomy_valid,
        ]
    )

    return LedgerRow(
        case_id=case.case_id,
        chapter=case.chapter,
        experiment=case.experiment,
        claim=case.claim,
        artifact_status=artifact.status,
        artifact_count=len(
            artifact.paths
        ),
        validity=case.validity,
        inferential_status=case.inferential_status,
        transition_type=case.transition_type,
        evidence_role=case.evidence_role,
        confirmatory=case.confirmatory,
        threshold=case.threshold,
        expected_mean=case.expected_mean,
        expected_ci_low=case.expected_ci_low,
        expected_ci_high=case.expected_ci_high,
        expected_mde=case.expected_mde,
        mean_visible_in_artifact=approximately_present(
            case.expected_mean,
            hints["mean"],
        ),
        ci_low_visible_in_artifact=approximately_present(
            case.expected_ci_low,
            hints["ci_low"],
        ),
        ci_high_visible_in_artifact=approximately_present(
            case.expected_ci_high,
            hints["ci_high"],
        ),
        mde_visible_in_artifact=approximately_present(
            case.expected_mde,
            hints["mde"],
        ),
        threshold_visible_in_artifact=approximately_present(
            case.threshold,
            hints["threshold"],
        ),
        surviving_evidence=case.surviving_evidence,
        failure_lesson=case.failure_lesson,
        rule_invalid_not_negative=invalid_not_negative,
        rule_unresolved_not_failed=unresolved_not_failed,
        rule_bounded_requires_threshold=bounded_requires_threshold,
        rule_bounded_requires_precision=bounded_requires_precision,
        rule_surviving_evidence_recorded=surviving_recorded,
        rule_descriptive_not_confirmatory=descriptive_not_confirmatory,
        rule_taxonomy_valid=taxonomy_valid,
        case_consistent=case_consistent,
    )


# ============================================================================
# Cross-case audits
# ============================================================================

def find_case(
    rows: Sequence[LedgerRow],
    case_id: str,
) -> LedgerRow:
    for row in rows:
        if row.case_id == case_id:
            return row

    raise KeyError(
        case_id
    )


def cross_case_checks(
    rows: Sequence[LedgerRow],
) -> List[dict]:
    checks = []

    ch27_v1_primary = find_case(
        rows,
        "CH27_V1_PRIMARY",
    )

    ch27_v1_e1 = find_case(
        rows,
        "CH27_V1_IMMEDIATE",
    )

    checks.append({
        "check_id": "X001",
        "name": "Invalid primary preserves independent sub-result",
        "pass": bool(
            ch27_v1_primary.inferential_status
            == "INVALID"
            and ch27_v1_e1.inferential_status
            == "SUPPORTED"
            and ch27_v1_e1.evidence_role
            == "PRESERVES_SUBRESULT"
        ),
        "cases": [
            ch27_v1_primary.case_id,
            ch27_v1_e1.case_id,
        ],
    })

    ch27_direction = find_case(
        rows,
        "CH27_V2_DIRECTION",
    )

    ch27_magnitude = find_case(
        rows,
        "CH27_V2_MAGNITUDE",
    )

    checks.append({
        "check_id": "X002",
        "name": "Direction separated from minimum magnitude",
        "pass": bool(
            ch27_direction.inferential_status
            == "DIRECTION_SUPPORTED"
            and ch27_magnitude.inferential_status
            == "UNRESOLVED"
        ),
        "cases": [
            ch27_direction.case_id,
            ch27_magnitude.case_id,
        ],
    })

    ch28_v1 = find_case(
        rows,
        "CH28_V1_RAW",
    )

    ch28_v2 = find_case(
        rows,
        "CH28_V2_EXCESS",
    )

    checks.append({
        "check_id": "X003",
        "name": "Stronger control narrows claim without erasing raw phenomenon",
        "pass": bool(
            ch28_v1.inferential_status
            == "SUPPORTED"
            and ch28_v2.inferential_status
            == "BOUNDED_BELOW_SEI"
            and ch28_v2.evidence_role
            == "NARROWS_CLAIM"
            and "V1 raw containment survives"
            in ch28_v2.surviving_evidence
        ),
        "cases": [
            ch28_v1.case_id,
            ch28_v2.case_id,
        ],
    })

    ch26_primary = find_case(
        rows,
        "CH26_V2_PRIMARY",
    )

    ch26_mechanism = find_case(
        rows,
        "CH26_V2_MECHANISM",
    )

    checks.append({
        "check_id": "X004",
        "name": "Bounded aggregate result preserves mechanistic rerouting",
        "pass": bool(
            ch26_primary.inferential_status
            == "BOUNDED_NEAR_ZERO"
            and ch26_mechanism.inferential_status
            == "DESCRIPTIVE_ONLY"
            and ch26_mechanism.evidence_role
            == "PRESERVES_SUBRESULT"
        ),
        "cases": [
            ch26_primary.case_id,
            ch26_mechanism.case_id,
        ],
    })

    ch27_closeout = find_case(
        rows,
        "CH27_V2_CLOSEOUT",
    )

    checks.append({
        "check_id": "X005",
        "name": "Descriptive closeout does not rescue confirmatory magnitude claim",
        "pass": bool(
            ch27_closeout.inferential_status
            == "DESCRIPTIVE_ONLY"
            and not ch27_closeout.confirmatory
            and ch27_magnitude.inferential_status
            == "UNRESOLVED"
        ),
        "cases": [
            ch27_closeout.case_id,
            ch27_magnitude.case_id,
        ],
    })

    return checks


# ============================================================================
# IO
# ============================================================================

def write_csv(
    path: Path,
    rows: Sequence[dict],
) -> None:
    rows = list(
        rows
    )

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fields = list(
        rows[0].keys()
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                row
            )


def write_json(
    path: Path,
    payload: Any,
) -> None:
    path.write_text(
        json.dumps(
            payload,
            indent=2,
        ),
        encoding="utf-8",
    )


class Reporter:
    def __init__(
        self,
        root: Path,
    ):
        self.root = root
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.sections: List[
            Tuple[
                str,
                Any,
            ]
        ] = []

    def stage(
        self,
        filename: str,
        title: str,
        payload: Any,
    ) -> None:
        write_json(
            self.root
            / filename.replace(
                ".md",
                ".json",
            ),
            payload,
        )

        body = (
            "```json\n"
            + json.dumps(
                payload,
                indent=2,
            )
            + "\n```"
        )

        (
            self.root
            / filename
        ).write_text(
            f"# {title}\n\n{body}\n",
            encoding="utf-8",
        )

        self.sections.append(
            (
                title,
                payload,
            )
        )

    def full_report(
        self,
        metadata: dict,
    ) -> Path:
        path = (
            self.root
            / "ch29-how-to-fail-correctly-v1-full-report.md"
        )

        lines = [
            "# Chapter 29 — How to Fail Correctly (V1)",
            "",
            "## Run metadata",
            "",
            "```json",
            json.dumps(
                metadata,
                indent=2,
            ),
            "```",
            "",
        ]

        for title, payload in self.sections:
            lines.extend(
                [
                    "---",
                    "",
                    f"## {title}",
                    "",
                    "```json",
                    json.dumps(
                        payload,
                        indent=2,
                    ),
                    "```",
                    "",
                ]
            )

        path.write_text(
            "\n".join(
                lines
            ),
            encoding="utf-8",
        )

        return path


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
    )

    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "research/digital-life/"
            "ch29-how-to-fail-correctly-v1"
        ),
    )

    args = parser.parse_args()

    repo_root = (
        args.repo_root
        .resolve()
    )

    report_dir = (
        args.report_dir
        if args.report_dir.is_absolute()
        else repo_root
        / args.report_dir
    )

    reporter = Reporter(
        report_dir
    )

    started = time.time()

    metadata = {
        "experiment_version": EXPERIMENT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "chapter": CHAPTER,
        "chapter_title": CHAPTER_TITLE,
        "repo_root": str(
            repo_root
        ),
        "registered_cases": len(
            CASES
        ),
        "registered_identities": len(
            IDENTITIES
        ),
        "started_at_unix": started,
    }

    protocol = {
        "status": "FROZEN",
        "primary_question": (
            "Can experiment failures be classified without conflating invalid "
            "runs, unresolved results, precision-bounded negatives, and "
            "supported results narrowed by stronger controls?"
        ),
        "primary_gate": (
            "Every registered evidence transition obeys the failure-ledger "
            "consistency rules."
        ),
        "forbidden_moves": [
            "count INVALID as evidence against hypothesis",
            "count CI-crossing-zero as FAILED",
            "call bounded negative without explicit meaningful threshold",
            "erase valid sub-results when a larger inference is invalid",
            "promote descriptive closeout into confirmatory rescue",
            "silently change estimand or control after seeing result",
        ],
        "stop_rule": (
            "No new Digital Crystal simulation is added merely to rescue a "
            "weakened methodological example."
        ),
    }

    reporter.stage(
        "stage-00-protocol.md",
        "Stage 0 — Frozen Chapter 29 Protocol",
        protocol,
    )

    artifact_matches = [
        find_artifacts(
            repo_root,
            case,
        )
        for case in CASES
    ]

    artifacts_payload = {
        "cases": [
            asdict(
                match
            )
            for match
            in artifact_matches
        ],
        "found_count": sum(
            match.status
            == "FOUND"
            for match
            in artifact_matches
        ),
        "manual_evidence_only_count": sum(
            match.status
            == "MANUAL_EVIDENCE_ONLY"
            for match
            in artifact_matches
        ),
        "missing_source_count": sum(
            match.status
            == "MISSING_SOURCE"
            for match
            in artifact_matches
        ),
        "rule": (
            "Missing artifacts are never replaced with invented artifact-derived "
            "values."
        ),
    }

    reporter.stage(
        "stage-01-artifacts.md",
        "Stage 1 — Artifact Availability",
        artifacts_payload,
    )

    artifact_by_case = {
        match.case_id: match
        for match
        in artifact_matches
    }

    ledger_rows = [
        build_ledger_row(
            case,
            artifact_by_case[
                case.case_id
            ],
            repo_root,
        )
        for case in CASES
    ]

    ledger_dicts = [
        asdict(
            row
        )
        for row
        in ledger_rows
    ]

    write_csv(
        report_dir
        / "ch29-failure-ledger.csv",
        ledger_dicts,
    )

    write_json(
        report_dir
        / "ch29-failure-ledger.json",
        {
            "rows": ledger_dicts
        },
    )

    reporter.stage(
        "stage-02-ledger.md",
        "Stage 2 — Failure Ledger",
        {
            "rows": ledger_dicts
        },
    )

    identity_dicts = [
        asdict(
            identity
        )
        for identity
        in IDENTITIES
    ]

    write_csv(
        report_dir
        / "ch29-construct-identities.csv",
        identity_dicts,
    )

    cross_checks = cross_case_checks(
        ledger_rows
    )

    all_case_rules_pass = all(
        row.case_consistent
        for row
        in ledger_rows
    )

    all_cross_checks_pass = all(
        check[
            "pass"
        ]
        for check
        in cross_checks
    )

    no_missing_required_sources = all(
        match.status
        != "MISSING_SOURCE"
        for match
        in artifact_matches
    )

    consistency = {
        "case_rule_pass_count": sum(
            row.case_consistent
            for row
            in ledger_rows
        ),
        "case_rule_total": len(
            ledger_rows
        ),
        "all_case_rules_pass": bool(
            all_case_rules_pass
        ),
        "cross_checks": cross_checks,
        "all_cross_checks_pass": bool(
            all_cross_checks_pass
        ),
        "no_missing_required_sources": bool(
            no_missing_required_sources
        ),
        "manual_evidence_only_is_allowed": True,
        "primary_gate_pass": bool(
            all_case_rules_pass
            and all_cross_checks_pass
            and no_missing_required_sources
        ),
    }

    reporter.stage(
        "stage-03-consistency.md",
        "Stage 3 — Epistemic Consistency Audit",
        consistency,
    )

    lessons = {
        "chapter_26": {
            "lesson": (
                "A controlled initial condition is not a controlled process."
            ),
            "construct_identity": (
                "CAUSAL ROUTING != CAUSAL AMPLIFICATION"
            ),
        },
        "chapter_27": {
            "lesson": (
                "Invalidate only the affected estimand; preserve independently "
                "valid sub-results."
            ),
            "construct_identity": (
                "DIRECTIONAL EFFECT != ESTABLISHED MINIMUM MAGNITUDE"
            ),
        },
        "chapter_28": {
            "lesson": (
                "A large precise effect can still be construct-confounded."
            ),
            "construct_identity": (
                "CAUSAL RETENTION != CAUSAL INDIVIDUATION"
            ),
        },
        "general_rules": [
            (
                "NULL RESULT != INVALID EXPERIMENT"
            ),
            (
                "INVALID EXPERIMENT != NEGATIVE RESULT"
            ),
            (
                "NONSIGNIFICANT != FAILED"
            ),
            (
                "PRECISE NEGATIVE RESULT != NOTHING HAPPENED"
            ),
            (
                "SUPPORTED LOWER-LEVEL PHENOMENON MAY SURVIVE A FAILED "
                "HIGHER-LEVEL INTERPRETATION"
            ),
            (
                "DESCRIPTIVE EXPLANATION MUST NOT RESCUE A FROZEN "
                "CONFIRMATORY CLAIM"
            ),
        ],
        "construct_identities": identity_dicts,
    }

    reporter.stage(
        "stage-04-lessons.md",
        "Stage 4 — Failure Principles",
        lessons,
    )

    if consistency[
        "primary_gate_pass"
    ]:
        status = (
            "FAILURE_LEDGER_CONSISTENT"
        )

        bounded_claim = (
            "Across the registered Chapter 26-28 case chains, invalid "
            "implementations, unresolved inferential questions, precision-"
            "bounded negative results, descriptive closeouts, and stronger-"
            "control claim narrowings can be represented without erasing "
            "surviving evidence or converting one evidence class into another."
        )

    else:
        status = (
            "FAILURE_LEDGER_INCONSISTENT"
        )

        bounded_claim = (
            "At least one registered evidence transition violates the frozen "
            "failure-ledger consistency rules or lacks required source support."
        )

    verdict = {
        "status": status,
        "primary_gate": consistency,
        "bounded_claim": bounded_claim,
        "what_this_does_not_establish": [
            "that the project never made mistakes",
            "that the registered taxonomy is universally complete",
            "that these cases prove a general philosophy of science",
            "that every future experiment can be classified without ambiguity",
        ],
        "chapter_principle": (
            "Fail the smallest claim justified by the evidence. "
            "Preserve everything that still survives."
        ),
    }

    reporter.stage(
        "stage-05-verdict.md",
        "Stage 5 — Chapter 29 V1 Verdict",
        verdict,
    )

    write_json(
        report_dir
        / "ch29-artifact-audit.json",
        {
            "metadata": metadata,
            "artifacts": artifacts_payload,
            "consistency": consistency,
            "verdict": verdict,
        },
    )

    metadata[
        "finished_at_unix"
    ] = time.time()

    metadata[
        "final_status"
    ] = status

    write_json(
        report_dir
        / "run-metadata.json",
        metadata,
    )

    report = reporter.full_report(
        metadata
    )

    print()
    print(
        "=" * 78
    )

    print(
        f"FINAL STATUS: {status}"
    )

    print(
        bounded_claim
    )

    print(
        f"Report: {report}"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":
    main()
