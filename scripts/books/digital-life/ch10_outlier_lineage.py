from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover - graceful fallback
    def tqdm(iterable=None, **kwargs):
        return iterable if iterable is not None else range(kwargs.get("total", 0))


OUTPUT_DIR = Path("static/images/books/digital-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Published Outlier rule + c0 seed
# ---------------------------------------------------------------------

OUTLIER_MAP = (
    "ERETQB4eHWkQ7xD4eYZosBQZFixOBHmtFeehExrKVhURLRAq"
    "GxeIlSO1JYZP6DRi69rop7TQCkvWTIag7kAS8g"
)

SEED_C0 = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 1],
    ],
    dtype=np.uint8,
)

OFFSETS = [
    (-1, -1, 256),
    (-1, 0, 128),
    (-1, 1, 64),
    (0, -1, 32),
    (0, 0, 16),
    (0, 1, 8),
    (1, -1, 4),
    (1, 0, 2),
    (1, 1, 1),
]

CONNECTIVITY_8 = np.ones((3, 3), dtype=np.uint8)


@dataclass(frozen=True)
class Cluster:
    uid: int
    time: int
    label: int
    area: int
    centroid: tuple[float, float]
    bbox: tuple[int, int, int, int]
    bitmap: np.ndarray
    signature: bytes


@dataclass(frozen=True)
class Edge:
    parent: int
    child: int
    causal_cells: int


@dataclass
class TrackPoint:
    time: int
    uid: int
    centroid: np.ndarray
    velocity: np.ndarray | None = None


# ---------------------------------------------------------------------
# Rule decoding / CA
# ---------------------------------------------------------------------


def decode_map_rule(encoded: str) -> np.ndarray:
    padding = "=" * ((4 - len(encoded) % 4) % 4)
    raw = base64.b64decode(encoded + padding)
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    if bits.size < 512:
        raise ValueError(f"MAP rule has only {bits.size} bits")
    return bits[:512].astype(np.uint8)


RULE = decode_map_rule(OUTLIER_MAP)


def make_world(size: int = 512) -> np.ndarray:
    world = np.zeros((size, size), dtype=np.uint8)
    r = size // 2 - 1
    c = size // 2 - 1
    world[r : r + 3, c : c + 3] = SEED_C0
    return world


def neighborhood_codes(state: np.ndarray) -> np.ndarray:
    code = np.zeros(state.shape, dtype=np.uint16)
    for dr, dc, weight in OFFSETS:
        shifted = np.roll(np.roll(state, -dr, axis=0), -dc, axis=1)
        code |= shifted.astype(np.uint16) * np.uint16(weight)
    return code


def outlier_step(state: np.ndarray) -> np.ndarray:
    return RULE[neighborhood_codes(state)]


# ---------------------------------------------------------------------
# Shape handling
# ---------------------------------------------------------------------


def crop_bitmap(labels: np.ndarray, label_id: int) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    positions = np.argwhere(labels == label_id)
    r0, c0 = positions.min(axis=0)
    r1, c1 = positions.max(axis=0)
    bitmap = (labels[r0 : r1 + 1, c0 : c1 + 1] == label_id).astype(np.uint8)
    return bitmap, (int(r0), int(c0), int(r1), int(c1))


def rotational_signature(bitmap: np.ndarray) -> bytes:
    """Translation invariant through cropping; rotation invariant, not reflection invariant."""
    variants: list[bytes] = []
    current = bitmap
    for _ in range(4):
        header = np.asarray(current.shape, dtype=np.uint16).tobytes()
        payload = np.packbits(current).tobytes()
        variants.append(header + payload)
        current = np.rot90(current)
    return min(variants)


def detect_clusters(
    state: np.ndarray,
    time: int,
    first_uid: int,
) -> tuple[dict[int, Cluster], np.ndarray, int]:
    labels, count = ndimage.label(state, structure=CONNECTIVITY_8)
    clusters: dict[int, Cluster] = {}
    uid = first_uid

    for label_id in range(1, count + 1):
        positions = np.argwhere(labels == label_id)
        if len(positions) == 0:
            continue

        bitmap, bbox = crop_bitmap(labels, label_id)
        centroid = positions.mean(axis=0)
        clusters[label_id] = Cluster(
            uid=uid,
            time=time,
            label=label_id,
            area=int(len(positions)),
            centroid=(float(centroid[0]), float(centroid[1])),
            bbox=bbox,
            bitmap=bitmap,
            signature=rotational_signature(bitmap),
        )
        uid += 1

    return clusters, labels, uid


def derive_c2_signature(size: int) -> tuple[bytes, np.ndarray]:
    """
    Anchor on the published trajectory rather than guessing.

    c0 is the supplied 3x3 seed. Advance exactly two ticks and select the
    connected component nearest the original seed centre. Its canonical
    rotational bitmap is the c2 signature used throughout the analysis.
    """
    state = make_world(size)
    state = outlier_step(state)  # c1
    state = outlier_step(state)  # c2

    clusters, _, _ = detect_clusters(state, time=2, first_uid=1)
    centre = np.array([size / 2, size / 2], dtype=float)

    if not clusters:
        raise RuntimeError("No clusters exist at t=2; cannot derive c2")

    c2 = min(
        clusters.values(),
        key=lambda c: np.linalg.norm(np.asarray(c.centroid) - centre),
    )

    print(
        "derived c2:",
        f"area={c2.area}",
        f"bbox={c2.bitmap.shape}",
        f"centroid=({c2.centroid[0]:.2f}, {c2.centroid[1]:.2f})",
    )

    return c2.signature, c2.bitmap.copy()


# ---------------------------------------------------------------------
# Cell-level counterfactual causality -> cluster edges
# ---------------------------------------------------------------------


def causal_edges_between_steps(
    before: np.ndarray,
    after: np.ndarray,
    before_labels: np.ndarray,
    after_labels: np.ndarray,
    before_clusters: dict[int, Cluster],
    after_clusters: dict[int, Cluster],
) -> list[Edge]:
    """
    Positive counterfactual causal dependency.

    For each live cell at t+1, switch each live input bit in its 3x3
    neighbourhood from 1 -> 0. If the child would become 0, that predecessor
    cell is treated as necessary for the observed child under this local
    counterfactual. Dependencies are aggregated cluster -> cluster.
    """
    code = neighborhood_codes(before)
    observed = RULE[code]
    if not np.array_equal(observed, after):
        raise AssertionError("CA step and causal reconstruction disagree")

    edge_counts: Counter[tuple[int, int]] = Counter()
    live_children = after == 1

    for dr, dc, weight in OFFSETS:
        predecessor_state = np.roll(np.roll(before, -dr, axis=0), -dc, axis=1)
        candidate = live_children & (predecessor_state == 1)
        if not np.any(candidate):
            continue

        counterfactual_code = code ^ np.uint16(weight)
        counterfactual_output = RULE[counterfactual_code]
        necessary = candidate & (counterfactual_output == 0)
        if not np.any(necessary):
            continue

        child_rows, child_cols = np.nonzero(necessary)
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
        Edge(parent=p, child=c, causal_cells=count)
        for (p, c), count in edge_counts.items()
    ]


# ---------------------------------------------------------------------
# Simulation / graph construction
# ---------------------------------------------------------------------


def run_causal_experiment(size: int, generations: int):
    state = make_world(size)
    all_clusters: dict[int, Cluster] = {}
    all_edges: list[Edge] = []
    clusters_by_time: dict[int, list[int]] = defaultdict(list)

    clusters, labels, next_uid = detect_clusters(state, time=0, first_uid=1)
    for cluster in clusters.values():
        all_clusters[cluster.uid] = cluster
        clusters_by_time[0].append(cluster.uid)

    for t in range(generations):
        next_state = outlier_step(state)
        next_clusters, next_labels, next_uid = detect_clusters(
            next_state,
            time=t + 1,
            first_uid=next_uid,
        )

        for cluster in next_clusters.values():
            all_clusters[cluster.uid] = cluster
            clusters_by_time[t + 1].append(cluster.uid)

        all_edges.extend(
            causal_edges_between_steps(
                before=state,
                after=next_state,
                before_labels=labels,
                after_labels=next_labels,
                before_clusters=clusters,
                after_clusters=next_clusters,
            )
        )

        state = next_state
        clusters = next_clusters
        labels = next_labels

    return all_clusters, all_edges, clusters_by_time


def build_graph(edges: list[Edge]):
    children: dict[int, list[int]] = defaultdict(list)
    parents: dict[int, list[int]] = defaultdict(list)
    weights: dict[tuple[int, int], int] = {}

    for edge in edges:
        children[edge.parent].append(edge.child)
        parents[edge.child].append(edge.parent)
        weights[(edge.parent, edge.child)] = edge.causal_cells

    return children, parents, weights


# ---------------------------------------------------------------------
# c2 lineage: explicit anchor + first-return causal search
# ---------------------------------------------------------------------


def c2_occurrences(clusters: dict[int, Cluster], signature: bytes) -> list[int]:
    result = [uid for uid, c in clusters.items() if c.signature == signature]
    result.sort(key=lambda uid: (clusters[uid].time, clusters[uid].centroid))
    return result


def first_return_c2_children(
    source: int,
    targets: set[int],
    clusters: dict[int, Cluster],
    children: dict[int, list[int]],
    min_dt: int = 100,
    max_dt: int = 900,
) -> list[int]:
    """
    Follow the full causal graph from one c2 occurrence.

    A branch stops when it first reaches another c2 occurrence. Multiple
    first-return targets mean the source's causal future has branched into
    multiple recurrences of the c2 organization.
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
            # First return on this branch: do not continue past it.
            continue

        for child in children.get(node, []):
            queue.append(child)

    return sorted(found, key=lambda uid: (clusters[uid].time, clusters[uid].centroid))


def build_c2_return_graph(
    clusters: dict[int, Cluster],
    edges: list[Edge],
    c2_signature: bytes,
    max_generations: int = 4,
):
    children, _, _ = build_graph(edges)
    occurrences = c2_occurrences(clusters, c2_signature)
    targets = set(occurrences)

    print(f"c2 occurrences in run: {len(occurrences)}")
    if occurrences:
        print(
            "c2 time span:",
            clusters[occurrences[0]].time,
            "..",
            clusters[occurrences[-1]].time,
        )

    if not occurrences:
        raise RuntimeError("No c2 occurrences found after anchoring at t=2")

    # Precompute first-return children for c2 occurrences.
    returns: dict[int, list[int]] = {}
    for uid in tqdm(
        occurrences,
        desc="Finding c2 causal returns",
        unit="c2",
        dynamic_ncols=True,
    ):
        # Skip the huge cost for late nodes that cannot produce a useful return.
        if clusters[uid].time + 100 > max(c.time for c in clusters.values()):
            continue
        kids = first_return_c2_children(
            source=uid,
            targets=targets,
            clusters=clusters,
            children=children,
        )
        if kids:
            returns[uid] = kids

    # Prefer an actual branching source; otherwise fall back to earliest c2.
    branching = [uid for uid, kids in returns.items() if len(kids) >= 2]
    if branching:
        root = min(branching, key=lambda uid: clusters[uid].time)
        print(
            "found branching c2 source:",
            f"uid={root}",
            f"t={clusters[root].time}",
            f"children={len(returns[root])}",
        )
    else:
        root = occurrences[0]
        print(
            "WARNING: no branching c2 first-return source found in this run; "
            "the figure will show causal recurrence, not demonstrated replication."
        )

    visible: dict[int, set[int]] = defaultdict(set)
    queue = deque([(root, 0)])
    seen = {root}

    while queue:
        node, depth = queue.popleft()
        if depth >= max_generations:
            continue

        kids = returns.get(node, [])[:4]
        for child in kids:
            visible[node].add(child)
            if child not in seen:
                seen.add(child)
                queue.append((child, depth + 1))

    return visible, root, returns


# ---------------------------------------------------------------------
# Lineage figure
# ---------------------------------------------------------------------


def readable_lineage_subgraph(
    graph: dict[int, set[int]],
    root: int,
    max_depth: int = 3,
    max_children: int = 2,
) -> dict[int, set[int]]:
    """Return a deliberately small family tree for a readable book figure.

    The full causal graph is evidence; the figure is an explanation.  Showing
    every first-return node made the previous image unreadable, so the book
    graphic keeps at most two branches per parent and three generations.
    """
    visible: dict[int, set[int]] = defaultdict(set)
    queue = deque([(root, 0)])
    seen = {root}

    while queue:
        parent, depth = queue.popleft()
        if depth >= max_depth:
            continue

        children = list(graph.get(parent, set()))[:max_children]
        for child in children:
            visible[parent].add(child)
            if child not in seen:
                seen.add(child)
                queue.append((child, depth + 1))

    return visible


def graph_depths(graph: dict[int, set[int]], root: int) -> dict[int, int]:
    depth = {root: 0}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in graph.get(node, set()):
            if child not in depth:
                depth[child] = depth[node] + 1
                queue.append(child)
    return depth


def build_lineage_figure(
    clusters: dict[int, Cluster],
    graph: dict[int, set[int]],
    root: int,
):
    """Create a sparse, readable causal family tree.

    Each node gets its own tiny inset axes.  This prevents the bitmap from
    being stretched across the whole plotting coordinate system and keeps
    labels/arrows away from one another.
    """
    graph = readable_lineage_subgraph(
        graph,
        root,
        max_depth=3,
        max_children=2,
    )

    depths = graph_depths(graph, root)
    by_depth: dict[int, list[int]] = defaultdict(list)
    for uid, depth in depths.items():
        by_depth[depth].append(uid)

    max_depth = max(by_depth) if by_depth else 0
    positions: dict[int, tuple[float, float]] = {}

    # Large vertical gaps and a capped node count make the causal story clear.
    y_levels = np.linspace(0.80, 0.18, max_depth + 1)
    for depth in range(max_depth + 1):
        nodes = sorted(
            by_depth[depth],
            key=lambda uid: clusters[uid].centroid,
        )
        if len(nodes) == 1:
            xs = [0.5]
        else:
            xs = np.linspace(0.16, 0.84, len(nodes))
        for x, uid in zip(xs, nodes):
            positions[uid] = (float(x), float(y_levels[depth]))

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.84])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Arrows first, ending outside the thumbnails.
    for parent, child_set in graph.items():
        if parent not in positions:
            continue
        x1, y1 = positions[parent]
        for child in child_set:
            if child not in positions:
                continue
            x2, y2 = positions[child]
            ax.annotate(
                "",
                xy=(x2, y2 + 0.085),
                xytext=(x1, y1 - 0.085),
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=1.5,
                    shrinkA=0,
                    shrinkB=0,
                ),
                zorder=1,
            )

    # Give every CA pattern a separate inset axes.
    thumb_w = 0.12
    thumb_h = 0.12
    for uid, (x, y) in positions.items():
        cluster = clusters[uid]
        inset = fig.add_axes([
            0.04 + (x - thumb_w / 2) * 0.92,
            0.06 + (y - thumb_h / 2) * 0.84,
            thumb_w * 0.92,
            thumb_h * 0.84,
        ])
        inset.imshow(
            cluster.bitmap,
            cmap="binary",
            interpolation="nearest",
            vmin=0,
            vmax=1,
            aspect="equal",
        )
        inset.set_xticks([])
        inset.set_yticks([])
        for spine in inset.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.8)

        ax.text(
            x,
            y - 0.085,
            f"t={cluster.time}",
            ha="center",
            va="top",
            fontsize=9,
            zorder=5,
        )

    branch_count = max((len(v) for v in graph.values()), default=0)
    if branch_count >= 2:
        subtitle = "One c2 organization has causal first-returns along more than one branch"
    else:
        subtitle = "Causal first-return of the published c2 organization"

    fig.suptitle("Outlier c2: A Readable Causal Family Tree", fontsize=18, y=0.97)
    fig.text(0.5, 0.925, subtitle, ha="center", va="center", fontsize=11)
    fig.text(
        0.5,
        0.025,
        "c2 is anchored from the published seed at t=2. Arrows follow counterfactual cell-level causal paths. "
        "The display is intentionally pruned; the analysis uses the full graph.",
        ha="center",
        va="bottom",
        fontsize=9,
        wrap=True,
    )

    path = OUTPUT_DIR / "ch10-outlier-causal-lineage.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Persistent moving-cluster tracking for flocking test
# ---------------------------------------------------------------------


def periodic_displacement(a: np.ndarray, b: np.ndarray, size: int) -> np.ndarray:
    delta = b - a
    return (delta + size / 2) % size - size / 2


def best_causal_successor(
    uid: int,
    clusters: dict[int, Cluster],
    children: dict[int, list[int]],
    weights: dict[tuple[int, int], int],
    world_size: int,
    max_step_distance: float = 12.0,
) -> int | None:
    """
    Pick one plausible continuation of a cluster into the next tick.

    Preference order:
      1. highest causal-cell support,
      2. closest centroid under periodic distance,
      3. most similar area.

    This is for *motion tracking*, not lineage/reproduction claims.
    """
    parent = clusters[uid]
    candidates = [
        child
        for child in children.get(uid, [])
        if clusters[child].time == parent.time + 1
    ]
    if not candidates:
        return None

    scored = []
    ppos = np.asarray(parent.centroid)

    for child_uid in candidates:
        child = clusters[child_uid]
        delta = periodic_displacement(ppos, np.asarray(child.centroid), world_size)
        dist = float(np.linalg.norm(delta))
        if dist > max_step_distance:
            continue
        support = weights.get((uid, child_uid), 0)
        area_ratio = min(parent.area, child.area) / max(parent.area, child.area)
        scored.append((support, -dist, area_ratio, child_uid))

    if not scored:
        return None

    scored.sort(reverse=True)
    return scored[0][-1]


def build_persistent_tracks(
    clusters: dict[int, Cluster],
    edges: list[Edge],
    world_size: int,
    min_area: int = 3,
    max_area: int = 200,
    min_length: int = 8,
) -> list[list[TrackPoint]]:
    children, parents, weights = build_graph(edges)

    # Precompute one-step motion continuation.
    successor: dict[int, int] = {}
    predecessor_count: Counter[int] = Counter()

    for uid, cluster in tqdm(
        clusters.items(),
        total=len(clusters),
        desc="Building motion continuations",
        unit="cluster",
        dynamic_ncols=True,
    ):
        if not (min_area <= cluster.area <= max_area):
            continue
        child = best_causal_successor(
            uid,
            clusters,
            children,
            weights,
            world_size,
        )
        if child is not None and min_area <= clusters[child].area <= max_area:
            successor[uid] = child
            predecessor_count[child] += 1

    # Start tracks where this selected continuation does not have exactly one
    # selected predecessor, so we avoid repeatedly starting in the middle.
    starts = [uid for uid in successor if predecessor_count[uid] != 1]
    visited: set[int] = set()
    tracks: list[list[TrackPoint]] = []

    for start in starts:
        if start in visited:
            continue

        track: list[TrackPoint] = []
        uid = start
        local_seen: set[int] = set()

        while uid in clusters and uid not in local_seen:
            local_seen.add(uid)
            visited.add(uid)
            cluster = clusters[uid]
            track.append(
                TrackPoint(
                    time=cluster.time,
                    uid=uid,
                    centroid=np.asarray(cluster.centroid, dtype=float),
                )
            )
            if uid not in successor:
                break
            uid = successor[uid]

        if len(track) >= min_length:
            # Velocity from centred differences where possible; this smooths
            # one-tick centroid jitter from shape changes.
            for i in range(len(track)):
                if i == 0:
                    dt = track[1].time - track[0].time
                    delta = periodic_displacement(track[0].centroid, track[1].centroid, world_size)
                elif i == len(track) - 1:
                    dt = track[-1].time - track[-2].time
                    delta = periodic_displacement(track[-2].centroid, track[-1].centroid, world_size)
                else:
                    dt = track[i + 1].time - track[i - 1].time
                    delta = periodic_displacement(track[i - 1].centroid, track[i + 1].centroid, world_size)
                track[i].velocity = delta / max(dt, 1)

            tracks.append(track)

    print(
        "persistent motion tracks:",
        len(tracks),
        f"(min_length={min_length})",
    )
    return tracks


def contemporaneous_points(tracks: list[list[TrackPoint]]):
    by_time: dict[int, list[TrackPoint]] = defaultdict(list)
    for track in tracks:
        for point in track:
            if point.velocity is not None and np.linalg.norm(point.velocity) > 1e-12:
                by_time[point.time].append(point)
    return by_time


def prepare_local_flocking_pairs(
    tracks: list[list[TrackPoint]],
    world_size: int,
    bins: np.ndarray,
    max_distance: float,
):
    """
    Build the expensive spatial geometry ONCE.

    For each tick:
      * create a periodic cKDTree over moving-cluster centroids;
      * find only pairs within max_distance;
      * compute each pair's distance bin once;
      * normalize velocity vectors once.

    The returned cache is reused by both the observed statistic and every
    shuffled control. This avoids O(n^2) all-pairs scans and avoids repeating
    geometry work for each shuffle.
    """
    by_time = contemporaneous_points(tracks)
    prepared = []
    total_pairs = 0

    for time, points in tqdm(
        sorted(by_time.items()),
        desc="Indexing local flocking pairs",
        unit="tick",
        dynamic_ncols=True,
    ):
        if len(points) < 2:
            continue

        positions = np.asarray([p.centroid for p in points], dtype=np.float64)
        velocities = np.asarray([p.velocity for p in points], dtype=np.float64)

        # cKDTree(boxsize=...) implements toroidal / periodic distances.
        # Centroids should already lie inside [0, world_size), but modulo keeps
        # this invariant explicit and robust.
        positions %= float(world_size)

        speeds = np.linalg.norm(velocities, axis=1)
        valid_velocity = speeds > 1e-12
        if np.count_nonzero(valid_velocity) < 2:
            continue

        unit_velocities = np.zeros_like(velocities)
        unit_velocities[valid_velocity] = (
            velocities[valid_velocity] / speeds[valid_velocity, None]
        )

        tree = cKDTree(
            positions,
            boxsize=float(world_size),
        )

        pairs = tree.query_pairs(
            r=max_distance,
            output_type="ndarray",
        )

        if pairs.size == 0:
            continue

        # Remove any pair involving an effectively stationary point.
        pair_valid = valid_velocity[pairs[:, 0]] & valid_velocity[pairs[:, 1]]
        pairs = pairs[pair_valid]
        if pairs.size == 0:
            continue

        # Compute periodic pair distance vectorized.
        delta = positions[pairs[:, 1]] - positions[pairs[:, 0]]
        delta = (delta + world_size / 2.0) % world_size - world_size / 2.0
        distances = np.linalg.norm(delta, axis=1)

        bin_indices = np.searchsorted(
            bins,
            distances,
            side="right",
        ) - 1

        in_bins = (bin_indices >= 0) & (bin_indices < len(bins) - 1)
        pairs = pairs[in_bins]
        bin_indices = bin_indices[in_bins].astype(np.int16, copy=False)

        if pairs.size == 0:
            continue

        prepared.append(
            {
                "time": time,
                "unit_velocities": unit_velocities,
                "pairs": pairs.astype(np.int32, copy=False),
                "bins": bin_indices,
            }
        )
        total_pairs += len(pairs)

    print(
        "cached local flocking pairs:",
        f"{total_pairs:,}",
        f"across {len(prepared):,} ticks",
        f"(radius={max_distance:g})",
    )

    return prepared


def observed_alignment_from_cache(prepared, n_bins: int):
    """Vectorized observed alignment using cached local neighbor pairs."""
    sums = np.zeros(n_bins, dtype=np.float64)
    counts = np.zeros(n_bins, dtype=np.int64)

    for frame in tqdm(
        prepared,
        desc="Measuring observed flocking",
        unit="tick",
        dynamic_ncols=True,
    ):
        velocities = frame["unit_velocities"]
        pairs = frame["pairs"]
        bin_indices = frame["bins"]

        scores = np.einsum(
            "ij,ij->i",
            velocities[pairs[:, 0]],
            velocities[pairs[:, 1]],
        )

        sums += np.bincount(
            bin_indices,
            weights=scores,
            minlength=n_bins,
        )[:n_bins]
        counts += np.bincount(
            bin_indices,
            minlength=n_bins,
        )[:n_bins]

    means = np.full(n_bins, np.nan, dtype=np.float64)
    valid = counts > 0
    means[valid] = sums[valid] / counts[valid]
    return means, counts


def shuffled_control_from_cache(
    prepared,
    n_bins: int,
    repeats: int = 100,
    seed: int = 42,
):
    """
    Null model with cached geometry.

    Positions, local-neighbor pairs and distance bins stay fixed. At each tick
    the velocity vectors are permuted among the simultaneously moving
    structures. Only dot products are recomputed.

    This is vastly cheaper than rebuilding all pair distances on every shuffle.
    """
    rng = np.random.default_rng(seed)
    replicate_means = np.full(
        (repeats, n_bins),
        np.nan,
        dtype=np.float64,
    )

    for repeat in tqdm(
        range(repeats),
        desc="Shuffling flocking control",
        unit="shuffle",
        dynamic_ncols=True,
    ):
        sums = np.zeros(n_bins, dtype=np.float64)
        counts = np.zeros(n_bins, dtype=np.int64)

        for frame in prepared:
            velocities = frame["unit_velocities"]
            pairs = frame["pairs"]
            bin_indices = frame["bins"]

            permutation = rng.permutation(len(velocities))
            shuffled = velocities[permutation]

            scores = np.einsum(
                "ij,ij->i",
                shuffled[pairs[:, 0]],
                shuffled[pairs[:, 1]],
            )

            sums += np.bincount(
                bin_indices,
                weights=scores,
                minlength=n_bins,
            )[:n_bins]
            counts += np.bincount(
                bin_indices,
                minlength=n_bins,
            )[:n_bins]

        valid = counts > 0
        replicate_means[repeat, valid] = sums[valid] / counts[valid]

    null_mean = np.full(n_bins, np.nan)
    null_low = np.full(n_bins, np.nan)
    null_high = np.full(n_bins, np.nan)

    for idx in range(n_bins):
        values = replicate_means[:, idx]
        values = values[np.isfinite(values)]
        if values.size:
            null_mean[idx] = float(np.mean(values))
            null_low[idx] = float(np.percentile(values, 5))
            null_high[idx] = float(np.percentile(values, 95))

    return null_mean, null_low, null_high


def build_flocking_figure(
    clusters: dict[int, Cluster],
    edges: list[Edge],
    world_size: int,
    min_pairs: int = 25,
    max_distance: float = 96.0,
    distance_bins: int = 6,
    shuffle_repeats: int = 100,
):
    tracks = build_persistent_tracks(
        clusters,
        edges,
        world_size,
        min_area=3,
        max_area=200,
        min_length=8,
    )

    if len(tracks) < 2:
        print("Not enough persistent tracks for flocking analysis")
        return

    # We are testing LOCAL collective motion. Looking all the way across half
    # the world was both computationally wasteful and scientifically weaker.
    max_distance = min(float(max_distance), world_size / 2.0)
    bins = np.linspace(0.0, max_distance, distance_bins + 1)
    centres = (bins[:-1] + bins[1:]) / 2.0

    prepared = prepare_local_flocking_pairs(
        tracks,
        world_size,
        bins,
        max_distance,
    )

    if not prepared:
        print(
            "No local moving-cluster pairs were found. "
            "Try a larger --flock-radius or a longer run."
        )
        return

    observed_means, counts = observed_alignment_from_cache(
        prepared,
        n_bins=distance_bins,
    )

    null_mean, null_low, null_high = shuffled_control_from_cache(
        prepared,
        n_bins=distance_bins,
        repeats=shuffle_repeats,
    )

    valid = (
        (counts >= min_pairs)
        & np.isfinite(observed_means)
        & np.isfinite(null_mean)
        & np.isfinite(null_low)
        & np.isfinite(null_high)
    )

    if not np.any(valid):
        print(
            "No distance bin had enough local moving-cluster pairs. "
            "Try --flock-min-pairs 10 or increase --flock-radius."
        )
        return

    xs = centres[valid]
    obs = observed_means[valid]
    ctl = null_mean[valid]
    lo = null_low[valid]
    hi = null_high[valid]
    pair_counts = counts[valid]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(xs, obs, marker="o", label="Observed")
    ax.plot(xs, ctl, linestyle="--", label="Velocity-shuffled control")
    ax.fill_between(xs, lo, hi, alpha=0.2, label="Control 5–95%")
    ax.axhline(0, linewidth=1)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel("Distance between simultaneously moving clusters")
    ax.set_ylabel("Velocity alignment (1=same direction, -1=opposite)")
    ax.set_title("Outlier: Is the Apparent Flocking Measurable?")
    ax.legend()
    ax.grid(alpha=0.25)

    for x, y, count in zip(xs, obs, pair_counts):
        ax.annotate(
            f"n={int(count):,}",
            (x, y),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    fig.tight_layout()
    path = OUTPUT_DIR / "ch10-outlier-flocking-test.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser(
        description="Outlier c2 causal lineage + independent flocking test"
    )
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument(
        "--generations",
        type=int,
        default=1600,
        help="Longer than the first script so c2 branching has room to appear.",
    )
    parser.add_argument("--lineage-depth", type=int, default=4)
    parser.add_argument("--flock-min-pairs", type=int, default=25)
    parser.add_argument(
        "--flock-radius",
        type=float,
        default=96.0,
        help="Only compare simultaneously moving clusters within this periodic-grid distance.",
    )
    parser.add_argument(
        "--flock-bins",
        type=int,
        default=6,
        help="Number of local-distance bins used in the flocking plot.",
    )
    parser.add_argument(
        "--flock-shuffles",
        type=int,
        default=100,
        help="Velocity-shuffle null replicates. Geometry is cached, so these are relatively cheap.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    c2_signature, _ = derive_c2_signature(args.size)

    clusters, edges, _ = run_causal_experiment(
        size=args.size,
        generations=args.generations,
    )

    print()
    print(f"total clusters: {len(clusters)}")
    print(f"causal edges:   {len(edges)}")

    lineage, root, returns = build_c2_return_graph(
        clusters,
        edges,
        c2_signature,
        max_generations=args.lineage_depth,
    )

    collapsed_edges = sum(len(v) for v in lineage.values())
    print(f"visible c2 return edges: {collapsed_edges}")

    build_lineage_figure(clusters, lineage, root)

    build_flocking_figure(
        clusters,
        edges,
        world_size=args.size,
        min_pairs=args.flock_min_pairs,
        max_distance=args.flock_radius,
        distance_bins=args.flock_bins,
        shuffle_repeats=args.flock_shuffles,
    )


if __name__ == "__main__":
    main()
