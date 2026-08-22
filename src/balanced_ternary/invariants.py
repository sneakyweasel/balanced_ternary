"""Executable mathematical invariants of balanced ternary.

Positions are least-significant-first: ``a_0`` is the last displayed digit.

Status of each claim is recorded in ``docs/mathematics.md``. These helpers
check identities; they do not search for new conjectures (Phase 6).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from automata.modular import ModularAutomaton
from balanced_ternary.features import weight
from balanced_ternary.representation import (
    BalancedTernary,
    WordLike,
    decode,
    digits,
    encode,
)


def v3(n: int) -> int | None:
    """3-adic valuation ``v_3(n)``. ``None`` means ``v_3(0) = ∞``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0:
        return None
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def lsd_nonzero_index(word: WordLike) -> int | None:
    """Smallest ``i`` with ``a_i != 0``, or ``None`` if the word is ``0``."""
    for i, a in enumerate(digits(word)):
        if a != 0:
            return i
    return None


def automaton_residue(word: WordLike, q: int) -> int:
    """Residue of ``word`` modulo ``q`` via the MSD-to-LSD automaton."""
    return ModularAutomaton(q).residue(word)


@dataclass
class InvariantFailure:
    name: str
    n: int
    detail: str


@dataclass
class InvariantReport:
    limit: int
    checked: int
    failures: list[InvariantFailure] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def check_round_trip(n: int) -> bool:
    return decode(encode(n)) == n


def check_parity(n: int, word: BalancedTernary | None = None) -> bool:
    """``n ≡ w(n) (mod 2)``."""
    w = word if word is not None else encode(n)
    return (n % 2) == (weight(w) % 2)


def check_v3_identity(n: int, word: BalancedTernary | None = None) -> bool:
    """``v_3(n)`` equals the index of the least-significant nonzero digit."""
    w = word if word is not None else encode(n)
    return v3(n) == lsd_nonzero_index(w)


def check_automaton_residue(
    n: int, q: int, word: BalancedTernary | None = None
) -> bool:
    w = word if word is not None else encode(n)
    return automaton_residue(w, q) == (n % q)


def verify_invariants(
    limit: int,
    moduli: tuple[int, ...] = (2, 3, 5, 7, 11),
) -> InvariantReport:
    """Check balanced-ternary identities for every ``n`` with ``|n| <= limit``."""
    if limit < 0:
        raise ValueError("limit must be >= 0")
    report = InvariantReport(limit=limit, checked=0)
    for n in range(-limit, limit + 1):
        word = encode(n)
        report.checked += 1
        if decode(word) != n:
            report.failures.append(
                InvariantFailure("round_trip", n, f"decode(encode({n})) != {n}")
            )
            continue
        if not check_parity(n, word):
            report.failures.append(
                InvariantFailure(
                    "parity",
                    n,
                    f"{n} mod 2 = {n % 2}, weight mod 2 = {weight(word) % 2}",
                )
            )
        if not check_v3_identity(n, word):
            report.failures.append(
                InvariantFailure(
                    "v3",
                    n,
                    f"v3={v3(n)!r}, lsd_nonzero={lsd_nonzero_index(word)!r}",
                )
            )
        for q in moduli:
            if not check_automaton_residue(n, q, word):
                report.failures.append(
                    InvariantFailure(
                        "automaton_residue",
                        n,
                        f"automaton % {q} = {automaton_residue(word, q)}, "
                        f"n % {q} = {n % q}",
                    )
                )
    return report
