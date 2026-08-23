"""Residual automata profiles: raw, semantic, Myhill–Nerode, sample.

Never label a sample LSD signature as ``M_k``. Compression is
``3^k / M_k(f)`` against the trivial input-word bound, not a claim of
a small automaton from prefix locality.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from bt.calculus.jet_locality import minimized_count
from bt.calculus.myhill_nerode import (
    all_reachable,
    levelled_mealy_count,
    mealy_width,
    myhill_nerode_count,
    raw_count,
    reachable_layers,
    semantic_count,
)
from bt.calculus.residual import TRITS, delta
from bt.calculus.section import IntPoly, parse_poly


@dataclass(frozen=True)
class StateProfile:
    poly: str
    depth: int
    raw: int
    raw_closed: int
    semantic: int
    myhill_nerode: int
    levelled_mealy: int
    sample: int
    trie: int
    width: int
    compression: float | None
    max_coeff: int
    max_degree: int
    lc_abs: int
    avg_fanout: float
    runtime_ms: float

    def as_dict(self) -> dict[str, object]:
        return {
            "poly": self.poly,
            "depth": self.depth,
            "raw": self.raw,
            "raw_closed": self.raw_closed,
            "semantic": self.semantic,
            "myhill_nerode": self.myhill_nerode,
            "levelled_mealy": self.levelled_mealy,
            "sample": self.sample,
            "trie": self.trie,
            "width": self.width,
            "compression": self.compression,
            "max_coeff": self.max_coeff,
            "max_degree": self.max_degree,
            "lc_abs": self.lc_abs,
            "avg_fanout": self.avg_fanout,
            "runtime_ms": self.runtime_ms,
        }


def trie_count(k: int) -> int:
    """Number of emitting prefixes ``|w| < k`` in the complete trit tree."""
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return 1
    return (3**k - 1) // 2


def average_fanout(f: IntPoly, k: int) -> float:
    if k <= 0:
        return 0.0
    layers = reachable_layers(f, max(k - 1, 0))
    nodes = 0
    edges = 0
    for depth in range(k):
        if depth not in layers:
            break
        for poly in layers[depth]:
            nodes += 1
            succs = {delta(poly, a).coeffs for a in TRITS}
            edges += len(succs)
    return edges / nodes if nodes else 0.0


def profile_states(f: IntPoly, k: int) -> StateProfile:
    t0 = time.perf_counter()
    states = all_reachable(f, max(k - 1, 0)) if k else [f]
    max_c = max((max(abs(c) for c in p.coeffs) for p in states), default=0)
    max_d = max((p.degree for p in states), default=-1)
    lc = max((abs(p.lc()) for p in states if p.degree >= 0), default=0)
    mn = myhill_nerode_count(f, k)
    sample = minimized_count(f, k) if k else 1
    elapsed = (time.perf_counter() - t0) * 1000.0
    return StateProfile(
        poly=f.render(),
        depth=k,
        raw=raw_count(f, k),
        raw_closed=raw_count(f, k, closed=True),
        semantic=semantic_count(f, k),
        myhill_nerode=mn,
        levelled_mealy=levelled_mealy_count(f, k),
        sample=sample,
        trie=trie_count(k),
        width=mealy_width(f, k),
        compression=(3**k / mn) if mn else None,
        max_coeff=max_c,
        max_degree=max_d,
        lc_abs=lc,
        avg_fanout=average_fanout(f, k),
        runtime_ms=elapsed,
    )


BENCHMARK_FAMILY: tuple[tuple[str, IntPoly], ...] = (
    ("x", parse_poly("x")),
    ("x+1", parse_poly("x+1")),
    ("2x+1", parse_poly("2x+1")),
    ("3x+1", parse_poly("3x+1")),
    ("x^2", parse_poly("x^2")),
    ("x^3", parse_poly("x^3")),
    ("x^4", parse_poly("x^4")),
    ("x^5", parse_poly("x^5")),
    ("2-3x", parse_poly("2-3x")),
    ("x^2+x", parse_poly("x^2+x")),
)


def profile_family(k: int) -> list[StateProfile]:
    return [profile_states(p, k) for _name, p in BENCHMARK_FAMILY]


def sequence_mn(f: IntPoly, max_k: int, *, uniform: bool = False) -> list[int]:
    return [myhill_nerode_count(f, k) for k in range(0, max_k + 1)]
