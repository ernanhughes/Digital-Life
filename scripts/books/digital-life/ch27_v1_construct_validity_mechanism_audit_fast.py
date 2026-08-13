#!/usr/bin/env python3
"""
Digital Life — Chapter 27 V1 Construct-Validity / Mechanism Audit — FAST
========================================================================

Drop-in performance wrapper around:

    ch27_v1_construct_validity_mechanism_audit.py

It preserves the existing audit logic and outputs, but replaces the slow
lag1_mechanics() implementation with a cached lag-1-only version.

Scientific role:
    ANALYSIS ONLY
    same V1 sample
    no fresh seed
    no V2
    no repair of the invalid V1 primary outcome
"""

from __future__ import annotations

from typing import Dict, Tuple

import ch18_digital_crystal_persistent_material_state_v7 as ch18
import ch27_digital_crystal_decaying_material_history_causal_response_v1 as ch27
import ch27_v1_construct_validity_mechanism_audit as audit


_TARGET_CACHE: Dict[Tuple[int, int], float] = {}
_MECH_CACHE: Dict[Tuple[int, int, str], audit.Lag1Mechanics] = {}

_CACHE_STATS = {
    "target_hits": 0,
    "target_misses": 0,
    "mechanics_hits": 0,
    "mechanics_misses": 0,
}


def fast_reference_target_lag1(
    bundle: audit.ProbeBundle,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> float:
    """
    Compute exactly the lag-1 erased PREVENT target without replaying all 12
    lags. This matches target[0] from ch27.build_reference_targets().
    """
    key = (
        int(bundle.group),
        int(bundle.probe_index),
    )

    if key in _TARGET_CACHE:
        _CACHE_STATS["target_hits"] += 1
        return _TARGET_CACHE[key]

    _CACHE_STATS["target_misses"] += 1

    erased_state = ch27.from_checkpoint(
        bundle.probe.checkpoint
    )

    input_value = float(
        bundle.probe.future_env[1]
    )

    radius = int(
        source_profile["radius"]
    )

    target = float(
        ch27.expected_attachments(
            erased_state,
            input_value,
            radius,
            crystal_params,
            0.0,
        )
    )

    _TARGET_CACHE[key] = target
    return target


def fast_lag1_mechanics(
    bundle: audit.ProbeBundle,
    arm: str,
    source_profile: dict,
    crystal_params: ch18.CrystalParams,
) -> audit.Lag1Mechanics:
    """
    Cached drop-in replacement for audit.lag1_mechanics().

    Original bottleneck:
        every call rebuilt a complete 12-lag erased reference trajectory.

    Fast path:
        direct lag-1 target + one calibration solve per probe x arm.
    """
    cache_key = (
        int(bundle.group),
        int(bundle.probe_index),
        str(arm),
    )

    if cache_key in _MECH_CACHE:
        _CACHE_STATS["mechanics_hits"] += 1
        return _MECH_CACHE[cache_key]

    _CACHE_STATS["mechanics_misses"] += 1

    if arm not in audit.ARMS:
        raise ValueError(
            f"Unknown history arm: {arm}"
        )

    history_state = bundle.histories[arm]

    branches = ch27.make_branches(
        history_state,
        bundle.cell,
    )

    target = fast_reference_target_lag1(
        bundle,
        source_profile,
        crystal_params,
    )

    input_value = float(
        bundle.probe.future_env[1]
    )

    radius = int(
        source_profile["radius"]
    )

    if arm == "erased":
        offset = 0.0

        achieved = float(
            ch27.expected_attachments(
                branches.prevent,
                input_value,
                radius,
                crystal_params,
                offset,
            )
        )

        if abs(
            achieved - target
        ) > audit.ASSERT_TOL:
            raise RuntimeError(
                "Fast erased target mismatch: "
                f"group={bundle.group} "
                f"probe={bundle.probe_index} "
                f"achieved={achieved} "
                f"target={target}"
            )

    else:
        (
            offset,
            achieved,
            solved,
        ) = ch27.solve_offset(
            branches.prevent,
            input_value,
            radius,
            crystal_params,
            target,
        )

        if not solved:
            raise RuntimeError(
                "Could not solve lag-1 offset: "
                f"group={bundle.group} "
                f"probe={bundle.probe_index} "
                f"arm={arm}"
            )

        rel_error = abs(
            achieved - target
        ) / max(
            target,
            1e-12,
        )

        if rel_error > ch27.MATCH_TOLERANCE:
            raise RuntimeError(
                "Lag-1 calibration outside Chapter 27 tolerance: "
                f"group={bundle.group} "
                f"probe={bundle.probe_index} "
                f"arm={arm} "
                f"relative_error={rel_error}"
            )

    mechanics = audit.Lag1Mechanics(
        arm=str(arm),
        force=branches.force,
        prevent=branches.prevent,
        offset=float(offset),
        target=float(target),
        input_value=float(input_value),
        radius=int(radius),
    )

    _MECH_CACHE[cache_key] = mechanics
    return mechanics


def print_cache_summary() -> None:
    print()
    print("-" * 78)
    print("FAST AUDIT CACHE SUMMARY")
    print(
        f"lag-1 targets constructed : "
        f"{_CACHE_STATS['target_misses']}"
    )
    print(
        f"lag-1 target cache hits   : "
        f"{_CACHE_STATS['target_hits']}"
    )
    print(
        f"mechanics constructed     : "
        f"{_CACHE_STATS['mechanics_misses']}"
    )
    print(
        f"mechanics cache hits      : "
        f"{_CACHE_STATS['mechanics_hits']}"
    )
    print(
        f"cached mechanics objects  : "
        f"{len(_MECH_CACHE)}"
    )
    print("-" * 78)


def main() -> None:
    # All original audit stages resolve lag1_mechanics from the audit module's
    # global namespace at call time, so this one monkeypatch accelerates every
    # stage without changing the report logic.
    audit.lag1_mechanics = fast_lag1_mechanics

    try:
        audit.main()
    finally:
        print_cache_summary()


if __name__ == "__main__":
    main()
