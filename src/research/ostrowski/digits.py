"""Canonical digit constraints.

Two families, kept separate:

* classical Ostrowski (Baranwal Def. 2.1) for the order-2 regression;
* proposed order-m rules (thesis §5.3, p. 49) for the Phase-0 case.

Digits are LSD-first: ``digits[i] = a_i``. A missing digit
``a_j`` with ``j<0`` is read as 0.
"""

from __future__ import annotations

from typing import Iterator, Sequence

from research.ostrowski.system import OstrowskiSystem


def digit_at(digits: Sequence[int], i: int) -> int:
    if i < 0:
        return 0
    if i >= len(digits):
        return 0
    return digits[i]


def is_canonical_ostrowski(system: OstrowskiSystem, digits: Sequence[int]) -> bool:
    """Def. 2.1: ``0 ≤ a_0 < d_1``, ``0 ≤ a_i ≤ d_{i+1}``, and
    ``a_i = d_{i+1}`` implies ``a_{i-1} = 0``.

    Uses only ``α_1`` of an order-2 Ostrowski embedding.
    """
    if system.order < 1:
        return False
    if any(a < 0 for a in digits):
        return False
    d1 = system.d(1, 1)
    if digits and digits[0] >= d1:
        return False
    for i in range(1, len(digits)):
        cap = system.d(1, i + 1)
        a = digits[i]
        if a > cap:
            return False
        if a == cap and digit_at(digits, i - 1) != 0:
            return False
    return True


def is_canonical_order_m(system: OstrowskiSystem, digits: Sequence[int]) -> bool:
    """Proposed §5.3 rules, transcribed, not proved unique or complete."""
    if any(a < 0 for a in digits):
        return False
    d11 = system.d(1, 1)
    if digits and digits[0] >= d11:
        return False
    m = system.order
    for i in range(1, len(digits)):
        cap = system.d(1, i + 1)
        a = digits[i]
        if a > cap:
            return False
        if a == cap:
            ok = False
            for k in range(1, m + 1):
                if digit_at(digits, i - k) < system.d(k, i + 1):
                    ok = True
                    break
            if not ok:
                return False
    return True


def max_digit(system: OstrowskiSystem, i: int) -> int:
    """Largest digit allowed at place ``i`` by rule 2 (rule 1 if ``i=0``)."""
    if i == 0:
        return system.d(1, 1) - 1
    return system.d(1, i + 1)


def greedy_digits(system: OstrowskiSystem, n: int, length: int | None = None) -> tuple[int, ...]:
    """Greedy (normal) representation of ``n ≥ 0``, LSD first.

    This is the classical linear-numeration greedy map, not the §5.3
    proposed rules. Used only as a comparison.
    """
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return (0,) if length is None else (0,) * max(1, length)
    if length is None:
        L = 1
        while system.place_value(L) <= n:
            L += 1
        length = L
    qs = system.place_values(length)
    digits = [0] * length
    rem = n
    for i in range(length - 1, -1, -1):
        cap = max_digit(system, i)
        a = min(rem // qs[i], cap) if qs[i] else 0
        digits[i] = a
        rem -= a * qs[i]
    if rem != 0:
        raise ValueError(f"greedy remainder {rem} for n={n} at length {length}")
    return tuple(digits)


def enumerate_canonical(
    system: OstrowskiSystem,
    length: int,
    *,
    order_m: bool = True,
) -> Iterator[tuple[int, ...]]:
    """All length-``length`` words (LSD first) obeying the chosen rules.

    Leading MSD zeros are included, so each value may appear at several
    lengths. The predicate is ``is_canonical_order_m`` or
    ``is_canonical_ostrowski``.
    """
    check = is_canonical_order_m if order_m else is_canonical_ostrowski
    caps = [max_digit(system, i) for i in range(length)]

    def rec(prefix: list[int]) -> Iterator[tuple[int, ...]]:
        i = len(prefix)
        if i == length:
            word = tuple(prefix)
            if check(system, word):
                yield word
            return
        for a in range(caps[i] + 1):
            prefix.append(a)
            if check(system, prefix):
                yield from rec(prefix)
            prefix.pop()

    yield from rec([])


def canonicality_census(
    system: OstrowskiSystem,
    length: int,
    *,
    order_m: bool = True,
) -> dict[str, object]:
    """Uniqueness / completeness of proposed (or Ostrowski) rules below ``q_length``.

    Values of padded words of exact length ``length`` in ``[0, q_length)``.
    """
    qs = system.place_values(length + 1)
    modulus = qs[length] if length < len(qs) else system.place_value(length)
    hits: dict[int, list[tuple[int, ...]]] = {}
    for word in enumerate_canonical(system, length, order_m=order_m):
        value = system.val(word)
        hits.setdefault(value, []).append(word)
    collisions = {v: ws for v, ws in hits.items() if len(ws) > 1}
    covered = set(hits)
    missing = [n for n in range(modulus) if n not in covered]
    extras = sorted(v for v in covered if v < 0 or v >= modulus)
    return {
        "length": length,
        "modulus": modulus,
        "word_count": sum(len(ws) for ws in hits.values()),
        "distinct_values": len(hits),
        "collision_count": len(collisions),
        "sample_collisions": dict(list(collisions.items())[:5]),
        "missing_count": len(missing),
        "sample_missing": missing[:10],
        "extras": extras[:10],
        "unique_on_range": not collisions and not missing,
        "complete_on_range": not missing,
        "injective_on_range": not collisions,
    }


def first_canonical(
    system: OstrowskiSystem,
    n: int,
    max_length: int,
    *,
    order_m: bool = True,
) -> tuple[int, ...] | None:
    """Shortest canonical word for ``n``, or None if none exists up to ``max_length``."""
    check = is_canonical_order_m if order_m else is_canonical_ostrowski
    for length in range(1, max_length + 1):
        for word in enumerate_canonical(system, length, order_m=order_m):
            if word[-1] == 0 and length > 1:
                continue
            if system.val(word) == n and check(system, word):
                return word
    return None
