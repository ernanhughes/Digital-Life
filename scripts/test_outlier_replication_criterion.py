#!/usr/bin/env python
"""
Outlier lineage replication-criterion validation.

Purpose
-------
Test the missing condition in the Chapter 3 claim:

A candidate parent c2 must have at least two later *exact* c2 copies that
are causally reachable from the parent, while neither offspring is causally
reachable from the other.

This is intentionally stricter than the existing rotational c2 detector.
It uses the causal graph produced by ch10_outlier_lineage.py, so rerun this
after upgrading the causal tracer.

Recommended canonical run:

    python scripts/books/digital-life/test_outlier_replication_criterion.py

The canonical configuration is 512x512 for 1600 generations.  A JSON report
is written to:

    research/digital-life/ch03-outlier-replication-criterion.json

Exit status:
    0 = at least one strict independent-offspring replication event found
    1 = no event found
    2 = canonical sanity check failed / module could not be loaded

Important
---------
This test does NOT prove that the cell-level causal tracer matches Hintze &
Bohm's published minimal-causal-subset implementation.  It tests the lineage
criterion *on the graph supplied by the module*.  Validate the upgraded
cell-level tracer separately against the published/reference implementation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np


DEFAULT_MODULE = Path("scripts/books/digital-life/ch10_outlier_lineage.py")
DEFAULT_REPORT = Path(
    "research/digital-life/ch03-outlier-replication-criterion.json"
)


def load_module(path: Path):
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Outlier lineage module not found: {path}")

    spec = importlib.util.spec_from_file_location("outlier_lineage_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def exact_same_bitmap(a: np.ndarray, b: np.ndarray) -> bool:
    """Translation-invariant because Cluster.bitmap is already cropped.

    Rotation is NOT normalized here.  This is deliberate: the 2026 causal
    paper's replication analysis used perfect copies rather than rotational
    variants.
    """
    return a.shape == b.shape and np.array_equal(a, b)


def exact_c2_occurrences(clusters: dict, c2_bitmap: np.ndarray) -> list[int]:
    result = [
        uid
        for uid, cluster in clusters.items()
        if exact_same_bitmap(cluster.bitmap, c2_bitmap)
    ]
    result.sort(key=lambda uid: (clusters[uid].time, clusters[uid].centroid))
    return result


def first_return_children(
    source: int,
    targets: set[int],
    clusters: dict,
    children: dict[int, list[int]],
    min_dt: int,
    max_dt: int,
) -> list[int]:
    """Return first exact-c2 hits on each causal branch.

    Once a branch reaches another exact c2 after min_dt, that branch stops.
    This prevents a grandchild reached only through a child c2 from being
    misclassified as a direct offspring on that same branch.
    """
    source_time = clusters[source].time
    queue = deque(children.get(source, []))
    visited = {source}
    found: set[int] = set()

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        dt = clusters[node].time - source_time
        if dt > max_dt:
            continue

        if node in targets and node != source and dt >= min_dt:
            found.add(node)
            continue

        for child in children.get(node, []):
            queue.append(child)

    return sorted(
        found,
        key=lambda uid: (clusters[uid].time, clusters[uid].centroid),
    )


def reachable(
    source: int,
    target: int,
    clusters: dict,
    children: dict[int, list[int]],
) -> bool:
    """True iff target lies anywhere in source's forward causal graph."""
    if source == target:
        return True

    target_time = clusters[target].time
    if clusters[source].time >= target_time:
        return False

    queue = deque(children.get(source, []))
    visited = {source}

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        node_time = clusters[node].time
        if node_time > target_time:
            continue
        if node == target:
            return True

        for child in children.get(node, []):
            if clusters[child].time <= target_time:
                queue.append(child)

    return False


def independent_pairs(
    offspring: list[int],
    clusters: dict,
    children: dict[int, list[int]],
) -> list[tuple[int, int]]:
    """Pairs satisfying the paper's 'not causally dependent on one another' test."""
    pairs: list[tuple[int, int]] = []

    for i, a in enumerate(offspring):
        for b in offspring[i + 1 :]:
            if not reachable(a, b, clusters, children) and not reachable(
                b, a, clusters, children
            ):
                pairs.append((a, b))

    return pairs


def event_record(
    parent: int,
    offspring: list[int],
    pairs: list[tuple[int, int]],
    clusters: dict,
) -> dict:
    return {
        "parent_uid": int(parent),
        "parent_time": int(clusters[parent].time),
        "offspring": [
            {
                "uid": int(uid),
                "time": int(clusters[uid].time),
                "dt": int(clusters[uid].time - clusters[parent].time),
            }
            for uid in offspring
        ],
        "independent_pairs": [
            {
                "a_uid": int(a),
                "a_time": int(clusters[a].time),
                "b_uid": int(b),
                "b_time": int(clusters[b].time),
            }
            for a, b in pairs
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=Path, default=DEFAULT_MODULE)
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--generations", type=int, default=1600)
    parser.add_argument(
        "--min-dt",
        type=int,
        default=100,
        help="Ignore immediate persistence/recurrence shorter than this.",
    )
    parser.add_argument(
        "--max-dt",
        type=int,
        default=900,
        help="Maximum parent->first-return window. 675/778-tick c2 paths fit here.",
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    try:
        outlier = load_module(args.module)
    except Exception as exc:
        print(f"ERROR loading module: {exc}", file=sys.stderr)
        return 2

    required = [
        "derive_c2_signature",
        "run_causal_experiment",
        "build_graph",
        "c2_occurrences",
    ]
    missing = [name for name in required if not hasattr(outlier, name)]
    if missing:
        print(
            "ERROR: lineage module is missing required API: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    print(
        f"[1/5] deriving c2 target on {args.size}x{args.size} world "
        f"(strict orientation will be tested)"
    )
    c2_rotational_signature, c2_bitmap = outlier.derive_c2_signature(args.size)

    print(
        f"[2/5] running causal experiment: "
        f"{args.size}x{args.size}, {args.generations} generations"
    )
    clusters, edges, _clusters_by_time = outlier.run_causal_experiment(
        args.size,
        args.generations,
    )

    print("[3/5] building causal graph")
    children, parents, _weights = outlier.build_graph(edges)

    # Existing detector: translation + rotation equivalence.
    rotational_occurrences = outlier.c2_occurrences(
        clusters,
        c2_rotational_signature,
    )

    # Strict detector: translation only; orientation must match exactly.
    exact_occurrences = exact_c2_occurrences(clusters, c2_bitmap)
    exact_targets = set(exact_occurrences)

    sanity = {
        "size": args.size,
        "generations": args.generations,
        "clusters": len(clusters),
        "causal_edges": len(edges),
        "rotation_equivalent_c2_occurrences": len(rotational_occurrences),
        "exact_c2_occurrences": len(exact_occurrences),
    }

    if args.size == 512 and args.generations == 1600:
        sanity["expected_clusters_from_previous_run"] = 138_891
        sanity["expected_rotation_equivalent_c2_from_previous_run"] = 144
        sanity["clusters_match_previous_run"] = len(clusters) == 138_891
        sanity["rotation_equivalent_c2_match_previous_run"] = (
            len(rotational_occurrences) == 144
        )

    print("[4/5] searching exact-c2 first returns and sibling independence")
    events: list[dict] = []
    candidate_parents = 0
    parents_with_multiple_first_returns = 0

    for parent in exact_occurrences:
        # There must be enough future left in the run to search usefully.
        if clusters[parent].time + args.min_dt > args.generations:
            continue

        offspring = first_return_children(
            source=parent,
            targets=exact_targets,
            clusters=clusters,
            children=children,
            min_dt=args.min_dt,
            max_dt=args.max_dt,
        )

        if offspring:
            candidate_parents += 1

        if len(offspring) < 2:
            continue

        parents_with_multiple_first_returns += 1
        pairs = independent_pairs(offspring, clusters, children)
        if pairs:
            events.append(event_record(parent, offspring, pairs, clusters))

    result = {
        "criterion": {
            "identity": "exact cropped bitmap; translation allowed; rotation NOT allowed",
            "parent_to_offspring": "causal reachability in supplied lineage graph",
            "direct_offspring": "first return to exact c2 on each causal branch",
            "offspring_independence": (
                "no directed causal path from offspring A to B or B to A"
            ),
            "min_dt": args.min_dt,
            "max_dt": args.max_dt,
        },
        "sanity": sanity,
        "search": {
            "exact_c2_parents_with_any_first_return": candidate_parents,
            "exact_c2_parents_with_multiple_first_returns": (
                parents_with_multiple_first_returns
            ),
            "strict_replication_events": len(events),
            "events": events[:20],
        },
        "pass": bool(events),
        "interpretation": (
            "PASS: at least one exact c2 parent has two or more causal "
            "first-return offspring with at least one pair that is not "
            "causally dependent on one another."
            if events
            else
            "FAIL/INCONCLUSIVE: no exact-c2 parent satisfied the full "
            "independent-offspring criterion in this run under this graph."
        ),
        "caveat": (
            "This validates the lineage criterion on the causal graph supplied "
            "by ch10_outlier_lineage.py. It does not by itself validate that "
            "the cell-level causal tracer matches the published minimal-causal-"
            "subset implementation."
        ),
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("[5/5] result")
    print(json.dumps(result, indent=2))
    print(f"\nReport written to: {args.report}")

    # Canonical configuration should at least reproduce non-causal structure counts.
    if args.size == 512 and args.generations == 1600:
        if len(clusters) != 138_891 or len(rotational_occurrences) != 144:
            print(
                "\nSANITY CHECK FAILED: this is not reproducing the prior "
                "canonical structural run.",
                file=sys.stderr,
            )
            return 2

    return 0 if events else 1


if __name__ == "__main__":
    raise SystemExit(main())
