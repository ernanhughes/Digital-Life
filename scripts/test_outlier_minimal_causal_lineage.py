#!/usr/bin/env python
"""
Outlier minimal-causal-set validation.

This is the second validation layer for Chapter 3.

Question
--------
Does the strict c2 reproduction result survive when the cell-level causal
graph is rebuilt from exhaustive minimal live-input causal sets rather than
the repository's current one-at-a-time predecessor-removal test?

The paper describes its method as:
- trace causation through live predecessor cells;
- remove redundant live inputs;
- retain the minimal causal set;
- if multiple minimal causal sets exist, conservatively include all
  contributing clusters.

This script implements an explicit, inspectable interpretation:

For an observed live output with neighbourhood code C:
1. consider every live-only submask S ⊆ C;
2. keep S if RULE[S] == 1;
3. call S inclusion-minimal if no proper live-only submask of S also
   produces 1;
4. if several inclusion-minimal sets exist, use the union of their
   contributing live cells when building cluster-level causal edges.

Because the published paper also states that no multiple minimal causal sets
were encountered in Outlier, this script treats that statement as a
VALIDATION TARGET rather than silently assuming our interpretation is exact.
It reports:
- multiple-minimal rule-table cases;
- which such neighbourhoods are actually encountered during the run;
- disagreement between the old but-for selector and the minimal-set selector.

If those diagnostics conflict with the published implementation, do NOT call
this a reproduction of the published causal algorithm.  The lineage result
is still valid under the explicitly stated causal criterion implemented here.

Canonical run
-------------
    python scripts/books/digital-life/test_outlier_minimal_causal_lineage.py

Fast rule-table-only diagnostic
--------------------------------
    python scripts/books/digital-life/test_outlier_minimal_causal_lineage.py --truth-table-only

Outputs
-------
    research/digital-life/ch03-outlier-minimal-causality.json

Exit codes
----------
0  strict exact-copy independent-offspring reproduction survives the
   minimal-set graph AND canonical structural sanity checks pass.
1  no strict reproduction event found on the minimal-set graph.
2  structural sanity check / import failure.
3  diagnostic warning: lineage may pass, but our minimal-set interpretation
   conflicts with the paper's reported "no multiple minimal causal sets"
   observation.  Inspect the JSON/notebook before using the result as a
   published-method replication.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np


DEFAULT_MODULE = Path("scripts/books/digital-life/ch10_outlier_lineage.py")
DEFAULT_REPORT = Path(
    "research/digital-life/ch03-outlier-minimal-causality.json"
)

CANONICAL_SIZE = 512
CANONICAL_GENERATIONS = 1600
EXPECTED_CLUSTERS = 138_891
EXPECTED_ROTATIONAL_C2 = 144


def load_module(path: Path):
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Outlier lineage module not found: {path}")
    spec = importlib.util.spec_from_file_location(
        "outlier_lineage_minimal_validation", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def iter_submasks(mask: int):
    """Yield every submask of mask, including mask and 0."""
    sub = mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask


def is_inclusion_minimal_sufficient(
    candidate: int,
    rule: np.ndarray,
) -> bool:
    """Candidate must output 1 and have no proper submask that also outputs 1."""
    if int(rule[candidate]) != 1:
        return False

    sub = (candidate - 1) & candidate
    while True:
        if int(rule[sub]) == 1:
            return False
        if sub == 0:
            break
        sub = (sub - 1) & candidate
    return True


def minimal_sufficient_sets_for_code(
    code: int,
    rule: np.ndarray,
) -> tuple[int, ...]:
    """All inclusion-minimal live-only sufficient submasks of observed code."""
    if int(rule[code]) != 1:
        return tuple()

    result = [
        sub
        for sub in iter_submasks(code)
        if is_inclusion_minimal_sufficient(sub, rule)
    ]
    # deterministic ordering: smaller sets first, then numeric mask
    result.sort(key=lambda x: (int(x).bit_count(), int(x)))
    return tuple(int(x) for x in result)


def but_for_mask_for_code(
    code: int,
    rule: np.ndarray,
) -> int:
    """Current repository criterion: a live input is causal iff removing it kills child."""
    if int(rule[code]) != 1:
        return 0

    mask = 0
    bit = 1
    for _ in range(9):
        if code & bit:
            if int(rule[code ^ bit]) == 0:
                mask |= bit
        bit <<= 1
    return mask


def build_causal_lookup(rule: np.ndarray):
    """Precompute all causal selectors for the 512 possible neighbourhoods."""
    minimal_sets: list[tuple[int, ...]] = [tuple() for _ in range(512)]
    minimal_union = np.zeros(512, dtype=np.uint16)
    but_for = np.zeros(512, dtype=np.uint16)

    for code in range(512):
        if int(rule[code]) != 1:
            continue

        sets = minimal_sufficient_sets_for_code(code, rule)
        minimal_sets[code] = sets

        union = 0
        for s in sets:
            union |= int(s)
        minimal_union[code] = np.uint16(union)
        but_for[code] = np.uint16(but_for_mask_for_code(code, rule))

    return minimal_sets, minimal_union, but_for


def truth_table_diagnostics(
    rule: np.ndarray,
    minimal_sets,
    minimal_union: np.ndarray,
    but_for: np.ndarray,
):
    live_codes = [code for code in range(512) if int(rule[code]) == 1]
    multiple = [code for code in live_codes if len(minimal_sets[code]) > 1]
    agree = [
        code
        for code in live_codes
        if int(minimal_union[code]) == int(but_for[code])
    ]
    minimal_only = [
        code
        for code in live_codes
        if int(minimal_union[code]) & ~int(but_for[code])
    ]
    but_for_only = [
        code
        for code in live_codes
        if int(but_for[code]) & ~int(minimal_union[code])
    ]

    examples = []
    for code in sorted(
        set(multiple + minimal_only + but_for_only),
        key=lambda c: (
            len(minimal_sets[c]) <= 1,
            c,
        ),
    )[:25]:
        examples.append(
            {
                "code": int(code),
                "code_binary": f"{code:09b}",
                "live_inputs": int(code).bit_count(),
                "minimal_sets": [
                    {
                        "mask": int(s),
                        "binary": f"{int(s):09b}",
                        "size": int(s).bit_count(),
                    }
                    for s in minimal_sets[code]
                ],
                "minimal_union_mask": int(minimal_union[code]),
                "minimal_union_binary": f"{int(minimal_union[code]):09b}",
                "but_for_mask": int(but_for[code]),
                "but_for_binary": f"{int(but_for[code]):09b}",
            }
        )

    return {
        "rule_entries": 512,
        "live_output_entries": len(live_codes),
        "multiple_minimal_set_codes": len(multiple),
        "methods_agree_exactly": len(agree),
        "minimal_union_has_extra_inputs": len(minimal_only),
        "but_for_has_extra_inputs": len(but_for_only),
        "multiple_minimal_codes": [int(x) for x in multiple],
        "examples": examples,
    }


def causal_edges_with_selector(
    before: np.ndarray,
    after: np.ndarray,
    before_labels: np.ndarray,
    after_labels: np.ndarray,
    before_clusters: dict,
    after_clusters: dict,
    selector_by_code: np.ndarray,
    outlier,
):
    """Build cluster edges using a precomputed contributing-live-bit selector."""
    code = outlier.neighborhood_codes(before)
    observed = outlier.RULE[code]
    if not np.array_equal(observed, after):
        raise AssertionError("CA step and causal reconstruction disagree")

    causal_mask = selector_by_code[code]
    edge_counts: Counter[tuple[int, int]] = Counter()

    for dr, dc, weight in outlier.OFFSETS:
        causal_here = (causal_mask & np.uint16(weight)) != 0
        if not np.any(causal_here):
            continue

        child_rows, child_cols = np.nonzero(causal_here)
        parent_rows = (child_rows + dr) % before.shape[0]
        parent_cols = (child_cols + dc) % before.shape[1]

        parent_labels = before_labels[parent_rows, parent_cols]
        child_labels = after_labels[child_rows, child_cols]

        for plabel, clabel in zip(parent_labels, child_labels):
            if plabel == 0 or clabel == 0:
                continue
            parent = before_clusters.get(int(plabel))
            child = after_clusters.get(int(clabel))
            if parent is None or child is None:
                continue
            edge_counts[(parent.uid, child.uid)] += 1

    return [
        outlier.Edge(parent=p, child=c, causal_cells=count)
        for (p, c), count in edge_counts.items()
    ]


def run_dual_experiment(
    outlier,
    size: int,
    generations: int,
    minimal_union: np.ndarray,
    but_for: np.ndarray,
):
    """One CA simulation, two causal reconstructions."""
    state = outlier.make_world(size)

    all_clusters = {}
    minimal_edges = []
    but_for_edges = []
    clusters_by_time = defaultdict(list)
    encountered_live_codes = Counter()

    clusters, labels, next_uid = outlier.detect_clusters(
        state, time=0, first_uid=1
    )
    for cluster in clusters.values():
        all_clusters[cluster.uid] = cluster
        clusters_by_time[0].append(cluster.uid)

    for t in range(generations):
        next_state = outlier.outlier_step(state)
        next_clusters, next_labels, next_uid = outlier.detect_clusters(
            next_state,
            time=t + 1,
            first_uid=next_uid,
        )

        for cluster in next_clusters.values():
            all_clusters[cluster.uid] = cluster
            clusters_by_time[t + 1].append(cluster.uid)

        codes = outlier.neighborhood_codes(state)
        live_codes = codes[next_state == 1]
        unique, counts = np.unique(live_codes, return_counts=True)
        for u, n in zip(unique, counts):
            encountered_live_codes[int(u)] += int(n)

        minimal_edges.extend(
            causal_edges_with_selector(
                before=state,
                after=next_state,
                before_labels=labels,
                after_labels=next_labels,
                before_clusters=clusters,
                after_clusters=next_clusters,
                selector_by_code=minimal_union,
                outlier=outlier,
            )
        )
        but_for_edges.extend(
            causal_edges_with_selector(
                before=state,
                after=next_state,
                before_labels=labels,
                after_labels=next_labels,
                before_clusters=clusters,
                after_clusters=next_clusters,
                selector_by_code=but_for,
                outlier=outlier,
            )
        )

        state = next_state
        clusters = next_clusters
        labels = next_labels

    return (
        all_clusters,
        minimal_edges,
        but_for_edges,
        clusters_by_time,
        encountered_live_codes,
    )


def exact_same_bitmap(a: np.ndarray, b: np.ndarray) -> bool:
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
    source_time = clusters[source].time
    queue = deque(children.get(source, []))
    visited = {source}
    found = set()

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

        if clusters[node].time > target_time:
            continue
        if node == target:
            return True

        for child in children.get(node, []):
            if clusters[child].time <= target_time:
                queue.append(child)

    return False


def strict_replication_events(
    clusters: dict,
    edges: list,
    c2_bitmap: np.ndarray,
    outlier,
    min_dt: int,
    max_dt: int,
):
    children, _, _ = outlier.build_graph(edges)
    exact = exact_c2_occurrences(clusters, c2_bitmap)
    targets = set(exact)

    events = []
    for parent in exact:
        offspring = first_return_children(
            source=parent,
            targets=targets,
            clusters=clusters,
            children=children,
            min_dt=min_dt,
            max_dt=max_dt,
        )
        if len(offspring) < 2:
            continue

        independent = []
        for i, a in enumerate(offspring):
            for b in offspring[i + 1 :]:
                if not reachable(a, b, clusters, children) and not reachable(
                    b, a, clusters, children
                ):
                    independent.append((a, b))

        if independent:
            events.append(
                {
                    "parent_uid": int(parent),
                    "parent_time": int(clusters[parent].time),
                    "offspring_count": len(offspring),
                    "offspring": [
                        {
                            "uid": int(uid),
                            "time": int(clusters[uid].time),
                            "dt": int(
                                clusters[uid].time - clusters[parent].time
                            ),
                        }
                        for uid in offspring
                    ],
                    "independent_pair_count": len(independent),
                    "independent_pairs": [
                        {
                            "a_uid": int(a),
                            "a_time": int(clusters[a].time),
                            "b_uid": int(b),
                            "b_time": int(clusters[b].time),
                        }
                        for a, b in independent[:25]
                    ],
                }
            )

    return exact, events


def edge_set(edges):
    return {(int(e.parent), int(e.child)) for e in edges}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=Path, default=DEFAULT_MODULE)
    parser.add_argument("--size", type=int, default=CANONICAL_SIZE)
    parser.add_argument("--generations", type=int, default=CANONICAL_GENERATIONS)
    parser.add_argument("--min-dt", type=int, default=100)
    parser.add_argument("--max-dt", type=int, default=900)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--truth-table-only", action="store_true")
    args = parser.parse_args()

    try:
        outlier = load_module(args.module)
    except Exception as exc:
        print(f"ERROR loading module: {exc}", file=sys.stderr)
        return 2

    rule = np.asarray(outlier.RULE, dtype=np.uint8)
    if rule.shape != (512,) or int(rule.sum()) != 220:
        print(
            f"ERROR: unexpected rule shape/sum: {rule.shape}, {int(rule.sum())}",
            file=sys.stderr,
        )
        return 2

    minimal_sets, minimal_union, but_for = build_causal_lookup(rule)
    truth = truth_table_diagnostics(
        rule, minimal_sets, minimal_union, but_for
    )

    report = {
        "method": {
            "candidate_minimal_method": (
                "all inclusion-minimal live-only sufficient submasks; "
                "union contributors across multiple minimal sets"
            ),
            "current_method": (
                "single live-predecessor removal from observed neighbourhood"
            ),
            "paper_validation_target": (
                "paper reports minimal causal subsets and states that no "
                "multiple minimal causal sets were found in Outlier"
            ),
        },
        "truth_table": truth,
    }

    print("=== RULE-TABLE DIAGNOSTIC ===")
    print(
        json.dumps(
            {
                k: v
                for k, v in truth.items()
                if k not in {"examples", "multiple_minimal_codes"}
            },
            indent=2,
        )
    )

    if args.truth_table_only:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nReport written to: {args.report}")
        return 3 if truth["multiple_minimal_set_codes"] else 0

    _, c2_bitmap = outlier.derive_c2_signature(args.size)

    print(
        f"\n=== RUNNING DUAL CAUSAL RECONSTRUCTION "
        f"{args.size}x{args.size} x {args.generations} ==="
    )
    (
        clusters,
        minimal_edges,
        but_for_edges,
        _clusters_by_time,
        encountered_codes,
    ) = run_dual_experiment(
        outlier=outlier,
        size=args.size,
        generations=args.generations,
        minimal_union=minimal_union,
        but_for=but_for,
    )

    rotational_signature, _ = outlier.derive_c2_signature(args.size)
    rotational_occurrences = outlier.c2_occurrences(
        clusters, rotational_signature
    )

    multiple_codes = set(truth["multiple_minimal_codes"])
    encountered_multiple = sorted(
        code for code in multiple_codes if encountered_codes.get(code, 0) > 0
    )

    min_set = edge_set(minimal_edges)
    old_set = edge_set(but_for_edges)

    exact_minimal, minimal_events = strict_replication_events(
        clusters=clusters,
        edges=minimal_edges,
        c2_bitmap=c2_bitmap,
        outlier=outlier,
        min_dt=args.min_dt,
        max_dt=args.max_dt,
    )
    exact_old, old_events = strict_replication_events(
        clusters=clusters,
        edges=but_for_edges,
        c2_bitmap=c2_bitmap,
        outlier=outlier,
        min_dt=args.min_dt,
        max_dt=args.max_dt,
    )

    canonical = (
        args.size == CANONICAL_SIZE
        and args.generations == CANONICAL_GENERATIONS
    )

    full = {
        "configuration": {
            "size": args.size,
            "generations": args.generations,
            "min_dt": args.min_dt,
            "max_dt": args.max_dt,
        },
        "sanity": {
            "clusters": len(clusters),
            "rotation_equivalent_c2_occurrences": len(rotational_occurrences),
            "canonical_expected_clusters": (
                EXPECTED_CLUSTERS if canonical else None
            ),
            "canonical_expected_rotation_equivalent_c2": (
                EXPECTED_ROTATIONAL_C2 if canonical else None
            ),
            "clusters_match_canonical": (
                len(clusters) == EXPECTED_CLUSTERS if canonical else None
            ),
            "rotational_c2_match_canonical": (
                len(rotational_occurrences) == EXPECTED_ROTATIONAL_C2
                if canonical
                else None
            ),
        },
        "encountered_rule_states": {
            "distinct_live_output_codes_encountered": len(encountered_codes),
            "multiple_minimal_codes_encountered": len(encountered_multiple),
            "codes": encountered_multiple,
            "total_uses_of_multiple_minimal_codes": int(
                sum(encountered_codes[c] for c in encountered_multiple)
            ),
        },
        "graph_comparison": {
            "current_but_for_edges": len(old_set),
            "minimal_set_edges": len(min_set),
            "shared_edges": len(old_set & min_set),
            "minimal_only_edges": len(min_set - old_set),
            "but_for_only_edges": len(old_set - min_set),
        },
        "strict_exact_c2": {
            "exact_occurrences_minimal_graph": len(exact_minimal),
            "exact_occurrences_but_for_graph": len(exact_old),
            "qualifying_parents_minimal_graph": len(minimal_events),
            "qualifying_parents_but_for_graph": len(old_events),
            "minimal_graph_pass": bool(minimal_events),
            "but_for_graph_pass": bool(old_events),
            "minimal_graph_events": minimal_events[:20],
        },
    }

    report["full_run"] = full

    paper_method_warning = bool(encountered_multiple)
    report["decision"] = {
        "strict_reproduction_survives_candidate_minimal_graph": bool(
            minimal_events
        ),
        "paper_method_warning": paper_method_warning,
        "statement": (
            "The strict exact-copy independent-offspring lineage criterion "
            "survives the candidate minimal-set causal graph."
            if minimal_events
            else
            "The strict lineage criterion did not survive the candidate "
            "minimal-set causal graph."
        ),
        "method_status": (
            "DIAGNOSTIC MISMATCH: multiple minimal causal sets were encountered "
            "under this implementation, whereas the paper reports none. Treat "
            "this as an explicit alternative causal reconstruction until the "
            "published code is matched."
            if paper_method_warning
            else
            "No multiple-minimal-set conflict was encountered; this candidate "
            "implementation is consistent with that reported paper property."
        ),
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== RESULT ===")
    print(
        json.dumps(
            {
                "sanity": full["sanity"],
                "encountered_rule_states": full["encountered_rule_states"],
                "graph_comparison": full["graph_comparison"],
                "strict_exact_c2": {
                    k: v
                    for k, v in full["strict_exact_c2"].items()
                    if k != "minimal_graph_events"
                },
                "decision": report["decision"],
            },
            indent=2,
        )
    )
    print(f"\nReport written to: {args.report}")

    if canonical:
        if (
            len(clusters) != EXPECTED_CLUSTERS
            or len(rotational_occurrences) != EXPECTED_ROTATIONAL_C2
        ):
            return 2

    if not minimal_events:
        return 1

    if paper_method_warning:
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
