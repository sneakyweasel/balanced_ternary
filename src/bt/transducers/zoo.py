"""Classification of integer maps as balanced-ternary transductions.

Reuses the existing LSD Mealy machines for ``×2`` and ``/2^k``. New maps
are classified exactly when a transducer or a non-existence proof is known.
State-count sequences are computational unless a formula is proved.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.divide_by_two_power import DivideByTwoPowerTransducer
from bt.transducers.doubling import doubling_step


@dataclass(frozen=True)
class ZooEntry:
    function: str
    finite_state: bool | None
    transducer_type: str
    reading_direction: str
    state_count: int | None
    minimized_state_count: int | None
    domain: str
    proof_status: str
    notes: str

    def as_dict(self) -> dict[str, object]:
        return {
            "function": self.function,
            "finite_state": self.finite_state,
            "transducer_type": self.transducer_type,
            "reading_direction": self.reading_direction,
            "state_count": self.state_count,
            "minimized_state_count": self.minimized_state_count,
            "domain": self.domain,
            "proof_status": self.proof_status,
            "notes": self.notes,
        }


def _doubling_power_complexity(k: int) -> dict[str, int]:
    """Product of ``k`` doubling carries. Computational, not a closed form."""
    from collections import deque

    start = (0,) * k
    alphabet = (-1, 0, 1)

    def step(carries: tuple[int, ...], digit: int) -> tuple[tuple[int, ...], int]:
        current = digit
        nxt: list[int] = []
        for c in carries:
            c2, out = doubling_step(c, current)
            nxt.append(c2)
            current = out
        return tuple(nxt), current

    seen = {start}
    queue = deque([start])
    while queue:
        st = queue.popleft()
        for a in alphabet:
            nxt, _ = step(st, a)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return {
        "k": k,
        "naive_bound": 3**k,
        "reachable": len(seen),
    }


def zoo() -> tuple[ZooEntry, ...]:
    return (
        ZooEntry(
            "S(n)=3n",
            True,
            "morphism: append LSD 0",
            "either",
            1,
            1,
            "Z",
            "PROVED",
            "BT(3n)=BT(n)0 for n≠0; BT(0)=0.",
        ),
        ZooEntry(
            "N(n)=-n",
            True,
            "letter-to-letter sign flip",
            "either",
            1,
            1,
            "Z",
            "PROVED",
            "Involution.",
        ),
        ZooEntry(
            "D(n)=(n-a0)/3",
            True,
            "LSD sequential: drop first letter",
            "LSD-first",
            1,
            1,
            "Z",
            "PROVED",
            "Not floor division. Left inverse of S.",
        ),
        ZooEntry(
            "H3 = D on 3Z",
            True,
            "D restricted to a0=0",
            "LSD-first",
            1,
            1,
            "3Z",
            "PROVED",
            "Inverse of S.",
        ),
        ZooEntry(
            "K3(n)=n/3^{v3(n)}",
            True,
            "LSD sequential: skip trailing zeros, copy",
            "LSD-first",
            2,
            2,
            "Z",
            "PROVED",
            "Trailing zeros are locally visible. Contrast: v2 is not.",
        ),
        ZooEntry(
            "Ip(n)=3n+1",
            True,
            "morphism: append LSD +",
            "either",
            1,
            1,
            "Z",
            "PROVED",
            "Append-plus theorem, with the n=0 convention BT(1)=+.",
        ),
        ZooEntry(
            "Im(n)=3n-1",
            True,
            "morphism: append LSD -",
            "either",
            1,
            1,
            "Z",
            "PROVED",
            "Same shift, LSD -1.",
        ),
        ZooEntry(
            "M2(n)=2n",
            True,
            "LSD Mealy, carry {-1,0,+1}",
            "LSD-first",
            3,
            3,
            "Z",
            "PROVED",
            "Existing DoublingTransducer.",
        ),
        ZooEntry(
            "H2(n)=n/2 on 2Z",
            True,
            "LSD Mealy, leftover carry on odds",
            "LSD-first",
            3,
            3,
            "2Z",
            "PROVED",
            "Existing DivideByTwoTransducer.",
        ),
        ZooEntry(
            "H2^k on 2^k Z",
            True,
            "product of k copies of H2",
            "LSD-first",
            None,
            None,
            "2^k Z",
            "PROVED existence; state counts VERIFIED COMPUTATIONALLY",
            "Naive bound 3^k. See h2_state_counts().",
        ),
        ZooEntry(
            "M2^k(n)=2^k n",
            True,
            "product of k doubling machines",
            "LSD-first",
            None,
            None,
            "Z",
            "PROVED existence; state counts VERIFIED COMPUTATIONALLY",
            "See m2_state_counts().",
        ),
        ZooEntry(
            "W(n)=bt_reverse",
            False,
            "not a one-way sequential transduction",
            "requires both ends",
            None,
            None,
            "Z",
            "PROVED (not sequential); not claimed non-rational in other models",
            "Global reverse plus canonicalize. Finite memory cannot wait for the MSD.",
        ),
        ZooEntry(
            "Wz, Wt",
            False,
            "not one-way sequential",
            "requires both ends",
            None,
            None,
            "Z",
            "PROVED (not sequential)",
            "Same obstruction as W.",
        ),
        ZooEntry(
            "odd_part = n/2^{v2(n)}",
            False,
            "not a single rational / subsequential transduction",
            "LSD-first per fixed k only",
            None,
            None,
            "Z",
            "PROVED",
            "Existing four-step argument. Each fixed k is finite-state.",
        ),
        ZooEntry(
            "Collatz T",
            False,
            "compose 3n+1 (FST) with unrestricted odd-part (not FST)",
            "LSD-first on each fixed valuation branch",
            None,
            None,
            "positive odd integers",
            "PROVED as a composition; T itself is not one FST",
            "Application of the zoo, not a search for Collatz invariants.",
        ),
        ZooEntry(
            "D^k",
            True,
            "drop k LSDs",
            "LSD-first",
            1,
            1,
            "Z",
            "PROVED",
            "k is fixed. Unbounded k is K3 after skipping zeros, still 2-state.",
        ),
        ZooEntry(
            "W ∘ D^k, D ∘ W",
            False,
            "contains reverse",
            "requires both ends",
            None,
            None,
            "Z",
            "PROVED (not sequential)",
            "Composing a non-sequential map with D does not restore sequentiality.",
        ),
        ZooEntry(
            "normalize on already-trit words",
            True,
            "identity / strip high zeros",
            "either",
            1,
            1,
            "{-1,0,+1}*",
            "PROVED",
            "Canonical words are already irreducible. High zeros are display.",
        ),
        ZooEntry(
            "normalize LSD on fixed [-B,B]",
            True,
            "LSD sequential Mealy, carry in [-B,B]",
            "LSD-first",
            None,
            None,
            "words with |c_i|<=B",
            "PROVED existence; state size algebraic in B",
            "Do not lift to unbounded Z. |q|<=floor((B+1)/3) on one coefficient.",
        ),
        ZooEntry(
            "normalize on unbounded Z coeffs",
            False,
            "not one finite-state transduction",
            "LSD-first algebraically, unbounded carry",
            None,
            None,
            "Z*",
            "PROVED (not sequential as one FST)",
            "A single coefficient 3^k forces carry scale 3^{k-1}.",
        ),
    )


def h2_state_counts(max_k: int = 8) -> list[dict[str, int]]:
    if max_k < 1 or max_k > 12:
        raise ValueError("max_k must be in 1..12")
    return [DivideByTwoPowerTransducer(k).complexity_report() for k in range(1, max_k + 1)]


def m2_state_counts(max_k: int = 8) -> list[dict[str, int]]:
    if max_k < 1 or max_k > 12:
        raise ValueError("max_k must be in 1..12")
    return [_doubling_power_complexity(k) for k in range(1, max_k + 1)]


def oeis_compare_state_counts(seq: tuple[int, ...]) -> str:
    """Closest known sequences, not a new OEIS claim.

    ``3^k`` is A000244. Reachable doubling-product states are compared to
    that bound only. No OEIS submission is made.
    """
    if not seq:
        return "empty"
    if seq == tuple(3**k for k in range(1, len(seq) + 1)):
        return "equals 3^k (A000244), the naive product bound"
    if all(seq[i] <= 3 ** (i + 1) for i in range(len(seq))):
        return "strictly below 3^k for at least one k" if any(
            seq[i] < 3 ** (i + 1) for i in range(len(seq))
        ) else "equals 3^k"
    return "does not match 3^k"
