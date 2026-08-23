"""Small rewrite graphs and distance to the unique normal form.

Geodesic length need not equal ``excess`` or Hamming-like digit scores.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.rewrite import successors
from bt.normtheory.strategies import normal_form


@dataclass(frozen=True)
class RewriteGraph:
    start: CoeffWord
    nodes: tuple[tuple[int, ...], ...]
    edges: tuple[tuple[tuple[int, ...], int, tuple[int, ...]], ...]
    normal_form: CoeffWord
    distance: int | None

    def as_dict(self) -> dict[str, object]:
        return {
            "start": list(self.start.coeffs),
            "nodes": [list(n) for n in self.nodes],
            "edge_count": len(self.edges),
            "normal_form": list(self.normal_form.coeffs),
            "distance": self.distance,
        }


def _key(word: CoeffWord) -> tuple[int, ...]:
    return word.coeffs


def rewrite_graph(word: CoeffWord, max_nodes: int = 2000) -> RewriteGraph:
    """Forward-reachable rewrite graph from ``word``."""
    start_key = _key(word)
    seen: dict[tuple[int, ...], CoeffWord] = {start_key: word}
    edges: list[tuple[tuple[int, ...], int, tuple[int, ...]]] = []
    queue = deque([word])
    while queue and len(seen) < max_nodes:
        current = queue.popleft()
        for i, nxt in successors(current):
            k = _key(nxt)
            edges.append((_key(current), i, k))
            if k not in seen:
                seen[k] = nxt
                queue.append(nxt)
    nf = normal_form(word)
    dist = distance_to_normal_form(word)
    return RewriteGraph(
        start=word,
        nodes=tuple(seen.keys()),
        edges=tuple(edges),
        normal_form=nf,
        distance=dist,
    )


def distance_to_normal_form(word: CoeffWord, max_nodes: int = 4000) -> int | None:
    """Shortest ``->`` path length to the unique irreducible form."""
    target = normal_form(word).coeffs
    start = word.coeffs
    if start == target:
        return 0
    seen = {start}
    queue: deque[tuple[CoeffWord, int]] = deque([(word, 0)])
    while queue and len(seen) < max_nodes:
        current, dist = queue.popleft()
        for _i, nxt in successors(current):
            k = nxt.coeffs
            if k == target:
                return dist + 1
            if k not in seen:
                seen.add(k)
                queue.append((nxt, dist + 1))
    return None


def excess_score(word: CoeffWord) -> int:
    return word.excess()


def geodesic_equals_excess(word: CoeffWord) -> bool | None:
    dist = distance_to_normal_form(word)
    if dist is None:
        return None
    return dist == word.excess()
