"""Digit-restricted balanced-ternary sets and their sumsets.

Moved from ``balanced_ternary.additive_sets`` without changing the
mathematics. Sparse-power and sparse-prime helpers live in their own
research modules.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from bt.metrics import weight
from bt.representation import decode, encode, from_digits_lsd


def _require_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError(f"k must be a nonnegative int, got {k!r}")
    return k


def interval_bound(k: int) -> int:
    """``(3^k - 1) / 2``: every integer in ``[-M, M]`` has length at most ``k``."""
    k = _require_k(k)
    return (3**k - 1) // 2


def iterate_digit_words(k: int, alphabet: tuple[int, ...]) -> list[tuple[int, ...]]:
    """LSD-first words of exact length ``k`` (leading zeros allowed)."""
    k = _require_k(k)
    if k == 0:
        return [()]
    words = [()]
    for _ in range(k):
        words = [w + (d,) for w in words for d in alphabet]
    return words


def set_from_alphabet(k: int, alphabet: tuple[int, ...]) -> list[int]:
    """Integers ``sum_{i<k} x_i 3^i`` with ``x_i`` in ``alphabet``."""
    out = []
    for w in iterate_digit_words(k, alphabet):
        if not w:
            out.append(0)
            continue
        out.append(decode(from_digits_lsd(w)))
    return out


def A_set(k: int) -> list[int]:
    """``{0,1}``-digit length-``k`` forms. Cardinality ``2^k``."""
    return set_from_alphabet(k, (0, 1))


def B_set(k: int) -> list[int]:
    """``{-1,+1}``-digit length-``k`` forms. Cardinality ``2^k``."""
    return set_from_alphabet(k, (-1, 1))


def C_set(k: int) -> list[int]:
    """All balanced length-``k`` forms. Equals ``[-M, M]`` with ``M=(3^k-1)/2``."""
    return set_from_alphabet(k, (-1, 0, 1))


def unbalanced_ternary_digits(n: int, k: int) -> tuple[int, ...]:
    """Ordinary base-3 digits of ``n`` in ``{0,1,2}``, length ``k``. ``n`` in ``[0, 3^k)``."""
    k = _require_k(k)
    if n < 0 or n >= 3**k:
        raise ValueError(f"n must lie in [0, 3^{k}), got {n}")
    digits = []
    x = n
    for _ in range(k):
        digits.append(x % 3)
        x //= 3
    return tuple(digits)


@dataclass(frozen=True)
class SumsetReport:
    name: str
    k: int
    cardinality: int
    covered_min: int
    covered_max: int
    interval: bool
    missing_count: int
    missing_sample: tuple[int, ...]
    energy: int
    multiplicity_min: int
    multiplicity_max: int
    formula: str
    proof_status: str


def _report_from_counter(
    name: str,
    k: int,
    counter: Counter[int],
    *,
    interval_lo: int | None,
    interval_hi: int | None,
    formula: str,
    proof_status: str,
) -> SumsetReport:
    if not counter:
        return SumsetReport(
            name, k, 0, 0, 0, True, 0, (), 0, 0, 0, formula, proof_status
        )
    keys = sorted(counter)
    lo, hi = keys[0], keys[-1]
    missing: list[int] = []
    if interval_lo is None:
        interval_lo, interval_hi = lo, hi
    for x in range(interval_lo, interval_hi + 1):
        if x not in counter:
            missing.append(x)
            if len(missing) >= 12:
                break
    energy = sum(c * c for c in counter.values())
    return SumsetReport(
        name=name,
        k=k,
        cardinality=len(counter),
        covered_min=lo,
        covered_max=hi,
        interval=len(missing) == 0 and lo == interval_lo and hi == interval_hi,
        missing_count=(interval_hi - interval_lo + 1) - len(counter)
        if interval_lo is not None
        else -1,
        missing_sample=tuple(missing[:8]),
        energy=energy,
        multiplicity_min=min(counter.values()),
        multiplicity_max=max(counter.values()),
        formula=formula,
        proof_status=proof_status,
    )


def sumset_A_plus_A(k: int) -> SumsetReport:
    """``A_k + A_k = {0, 1, ..., 3^k - 1}`` with energy ``6^k``."""
    k = _require_k(k)
    counter: Counter[int] = Counter()
    for n in range(3**k):
        r = 1
        for d in unbalanced_ternary_digits(n, k):
            if d == 1:
                r *= 2
        counter[n] = r
    return _report_from_counter(
        "A+A",
        k,
        counter,
        interval_lo=0,
        interval_hi=3**k - 1,
        formula="A_k+A_k=[0,3^k-1], |A+A|=3^k, E=6^k, r(n)=2^{#{i: d_i=1}}",
        proof_status="PROVED",
    )


def sumset_A_minus_A(k: int) -> SumsetReport:
    """``A_k - A_k = C_k = [-(3^k-1)/2, (3^k-1)/2]``."""
    k = _require_k(k)
    M = interval_bound(k)
    counter: Counter[int] = Counter()
    for n in range(-M, M + 1):
        r = 1
        w = encode(n).digits_lsd()
        padded = w + (0,) * (k - len(w))
        for d in padded[:k]:
            if d == 0:
                r *= 2
        counter[n] = r
    return _report_from_counter(
        "A-A",
        k,
        counter,
        interval_lo=-M,
        interval_hi=M,
        formula="A_k-A_k=C_k=[-M,M], |A-A|=3^k, r(n)=2^{#{zero digits in k pads}}",
        proof_status="PROVED",
    )


def sumset_B_plus_B(k: int) -> SumsetReport:
    """``B_k + B_k = 2 C_k``: all even integers in ``[-(3^k-1), 3^k-1]``."""
    k = _require_k(k)
    M = 3**k - 1
    counter: Counter[int] = Counter()
    inner = interval_bound(k)
    for t in range(-inner, inner + 1):
        r = 1
        w = encode(t).digits_lsd()
        padded = w + (0,) * (k - len(w))
        for d in padded[:k]:
            if d == 0:
                r *= 2
        counter[2 * t] = r
    return _report_from_counter(
        "B+B",
        k,
        counter,
        interval_lo=-M,
        interval_hi=M,
        formula="B_k+B_k=2 C_k, all even integers in [-(3^k-1), 3^k-1], |B+B|=3^k",
        proof_status="PROVED",
    )


def sumset_B_minus_B(k: int) -> SumsetReport:
    """``B_k - B_k = B_k + B_k`` because ``-B_k = B_k``."""
    rep = sumset_B_plus_B(k)
    return SumsetReport(
        name="B-B",
        k=rep.k,
        cardinality=rep.cardinality,
        covered_min=rep.covered_min,
        covered_max=rep.covered_max,
        interval=False,
        missing_count=rep.missing_count,
        missing_sample=rep.missing_sample,
        energy=rep.energy,
        multiplicity_min=rep.multiplicity_min,
        multiplicity_max=rep.multiplicity_max,
        formula="B-B=B+B because -B_k=B_k (digitwise sign flip)",
        proof_status="PROVED",
    )


def sumset_A_plus_B(k: int, *, enumerate_max_k: int = 12) -> SumsetReport:
    """``A_k + B_k``. No complete interval theorem for all ``k``; enumerate small ``k``."""
    k = _require_k(k)
    if k > enumerate_max_k:
        raise ValueError(f"A+B enumeration refused for k>{enumerate_max_k}")
    counter: Counter[int] = Counter()
    for a in A_set(k):
        for b in B_set(k):
            counter[a + b] += 1
    keys = sorted(counter)
    return _report_from_counter(
        "A+B",
        k,
        counter,
        interval_lo=keys[0],
        interval_hi=keys[-1],
        formula="enumerated; digits in {-1,0,1,2} before carry",
        proof_status="VERIFIED COMPUTATIONALLY",
    )


def rA_minus_sA(k: int, r: int, s: int, *, enumerate_max_k: int = 8) -> SumsetReport:
    k = _require_k(k)
    if r < 0 or s < 0:
        raise ValueError("r, s must be nonnegative")
    if k > enumerate_max_k:
        raise ValueError(f"rA-sA enumeration refused for k>{enumerate_max_k}")
    A = A_set(k)
    counter: Counter[int] = Counter()

    def scale_sum(coeff: int, acc: list[int]) -> list[int]:
        if coeff == 0:
            return [0]
        base = A
        out = [0]
        for _ in range(coeff):
            out = [x + a for x in out for a in base]
        return out

    left = scale_sum(r, A)
    right = scale_sum(s, A)
    for x in left:
        for y in right:
            counter[x - y] += 1
    keys = sorted(counter)
    return _report_from_counter(
        f"{r}A-{s}A",
        k,
        counter,
        interval_lo=keys[0] if keys else 0,
        interval_hi=keys[-1] if keys else 0,
        formula="enumerated Minkowski combination",
        proof_status="VERIFIED COMPUTATIONALLY",
    )


def smallest_r_covering_nonneg_interval(k: int) -> int:
    """Smallest ``r`` with ``r A_k`` containing an interval of length ``>= 2``."""
    k = _require_k(k)
    if k == 0:
        return 0
    return 2


def W_set(k: int, bound: int) -> list[int]:
    """``{ n : |n| <= bound, w(n) <= k }``."""
    k = _require_k(k)
    if bound < 0:
        raise ValueError("bound must be >= 0")
    return [n for n in range(-bound, bound + 1) if weight(encode(n)) <= k]
