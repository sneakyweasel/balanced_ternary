"""Layer D: labelled graph ``w --k--> w'`` on odd balanced ternary words.

Exact realization:

    k  = v2(3n+1)
    w' = odd_part(append_plus(w)) = BT(T(n))

The truncated graph on ``odd n <= N`` is a finite sample, not the Collatz
dynamics. Forbidden valuation patterns come from Layer C (2-adic graph) and
are **PROVED** absent relative to that automaton, not merely unseen in the
sample.

Synchronizing digit contexts: finite strings that send every odd state of
``TwoAdicDigitAutomaton(K)`` to one valuation class via the MSD Horner step
``r -> 3r+a`` (append a displayed digit on the right / new LSD).

Structural restriction already **PROVED**: ``T(n) not≡ 0 (mod 3)``, so no
image vertex is divisible by 3.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import product

from balanced_ternary.representation import decode, encode
from research.collatz.automata.two_adic import TwoAdicDigitAutomaton
from research.collatz.automata.valuation_shift import (
    AdmissibleValuationAutomaton,
    forbidden_patterns,
)
from research.collatz.core import collatz_step
from research.collatz.theorems import append_plus
from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.valuation import v2


DIGIT_CHARS: tuple[str, str, str] = ("-", "0", "+")
CHAR_TO_DIGIT: dict[str, int] = {"-": -1, "0": 0, "+": 1}


@dataclass(frozen=True)
class JointEdge:
    n: int
    w: str
    k: int
    n_prime: int
    w_prime: str


def collatz_word_step(w: str) -> tuple[int, str]:
    """``(k, w')`` from ``odd_part(append_plus(w))``."""
    plus = append_plus(w)
    k = v2(decode(plus))
    assert k is not None
    return k, odd_part_word(plus).word()


def build_joint_graph(limit: int, k_max: int | None = None) -> "JointGraph":
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError(f"limit must be an integer >= 1, got {limit!r}")
    edges: list[JointEdge] = []
    for n in range(1, limit + 1, 2):
        w = encode(n).word()
        k, w_prime = collatz_word_step(w)
        if k_max is not None and k > k_max:
            continue
        t = collatz_step(n)
        edges.append(JointEdge(n=n, w=w, k=k, n_prime=t, w_prime=w_prime))
    return JointGraph(limit=limit, k_max=k_max, edges=tuple(edges))


@dataclass
class JointGraph:
    limit: int
    k_max: int | None
    edges: tuple[JointEdge, ...]

    def out_degree_by_k(self) -> dict[int, int]:
        counts: dict[int, int] = defaultdict(int)
        for e in self.edges:
            counts[e.k] += 1
        return dict(sorted(counts.items()))

    def images_divisible_by_three(self) -> tuple[int, ...]:
        return tuple(e.n_prime for e in self.edges if e.n_prime % 3 == 0)

    def format(self) -> str:
        by_k = self.out_degree_by_k()
        lines = [
            f"Joint digit/valuation graph  odd n <= {self.limit}  "
            f"k_max={self.k_max}",
            f"vertices/edges: {len(self.edges)}",
            f"out-count by k: {by_k}",
            f"images ≡ 0 (mod 3): {len(self.images_divisible_by_three())}  "
            f"(PROVED: must be 0)",
            "",
            "sample edges w --k--> w':",
        ]
        for e in self.edges[:15]:
            lines.append(
                f"  {e.w}  --{e.k}-->  {e.w_prime}   ({e.n} -> {e.n_prime})"
            )
        if len(self.edges) > 15:
            lines.append(f"  ... ({len(self.edges) - 15} more)")
        lines.append("")
        lines.append("This truncation is a sample, not the Collatz dynamics.")
        lines.append("")
        return "\n".join(lines)


def synchronizing_digit_contexts(
    precision: int, length: int
) -> tuple[str, ...]:
    """Right-strings that collapse all odd states to one valuation class."""
    if length < 1:
        raise ValueError("length must be >= 1")
    auto = TwoAdicDigitAutomaton(precision)
    odd = auto.odd_states()
    found: list[str] = []
    for chars in product(DIGIT_CHARS, repeat=length):
        word = "".join(chars)
        labels: set[str] = set()
        for r in odd:
            s = r
            for ch in word:
                s = auto.transition(s, CHAR_TO_DIGIT[ch])
            labels.add(auto.classify_state(s).label())
            if len(labels) > 1:
                break
        if len(labels) == 1:
            found.append(word)
    return tuple(found)


def layer_d_report(
    limit: int,
    k_max: int,
    precision: int,
    pattern_length: int,
    sync_length: int,
) -> str:
    graph = build_joint_graph(limit, k_max=None)
    auto = AdmissibleValuationAutomaton(precision, k_max)
    forbidden = forbidden_patterns(auto, pattern_length)
    sync = synchronizing_digit_contexts(precision, sync_length)
    lines = [
        graph.format().rstrip(),
        "",
        f"Forbidden valuation words of length {pattern_length} "
        f"(Layer C, P={precision}, k_max={k_max}): {len(forbidden)}",
    ]
    for w in forbidden[:20]:
        lines.append(f"  {w}")
    if len(forbidden) > 20:
        lines.append(f"  ... ({len(forbidden) - 20} more)")
    lines.append("")
    lines.append(
        f"Synchronizing right-strings of length {sync_length} "
        f"on TwoAdicDigitAutomaton({precision}): {len(sync)}"
    )
    for w in sync[:20]:
        lines.append(f"  {w!r}")
    if len(sync) > 20:
        lines.append(f"  ... ({len(sync) - 20} more)")
    lines.append("")
    return "\n".join(lines)
