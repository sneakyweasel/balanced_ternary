"""Metrics, digit statistics, and executable balanced-ternary identities.

Theorem status lives in documentation. Functions here are exact
computations, not proofs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bt.automata.modular import ModularAutomaton
from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    digits,
    encode,
    msd_digits,
    normalize,
)


def weight(word: WordLike) -> int:
    """Number of nonzero digits: ``w(n) = sum_i |a_i|``."""
    return sum(abs(d) for d in digits(word))


def signed_digit_sum(word: WordLike) -> int:
    """``s(n) = sum_i a_i``."""
    return sum(digits(word))


def positive_digit_count(word: WordLike) -> int:
    return sum(1 for d in digits(word) if d == 1)


def negative_digit_count(word: WordLike) -> int:
    return sum(1 for d in digits(word) if d == -1)


def zero_count(word: WordLike) -> int:
    return sum(1 for d in digits(word) if d == 0)


def position_class_sums(word: WordLike, period: int) -> tuple[int, ...]:
    """Position-class signed sums from the least-significant digit.

    For period ``t >= 1``:

        S_j^{(t)} = sum_{i ≡ j (mod t)} a_i,    j = 0, ..., t-1

    where ``i`` is the power of 3 (``a_0`` is the last displayed digit).
    """
    if not isinstance(period, int) or period < 1:
        raise ValueError(f"period must be an integer >= 1, got {period!r}")
    sums = [0] * period
    for i, a in enumerate(digits(word)):
        sums[i % period] += a
    return tuple(sums)


@dataclass(frozen=True)
class RunStatistics:
    """Runs of equal digits in display (MSD-first) order.

    Each run is ``(digit, length)`` with ``digit in {-1, 0, +1}``.
    ``leading_run`` is the MSD run; ``trailing_run`` is the LSD run.
    """

    runs: tuple[tuple[int, int], ...]
    number_of_runs: int
    leading_run: tuple[int, int]
    trailing_run: tuple[int, int]
    run_lengths: tuple[int, ...]
    max_run: int


def run_statistics(word: WordLike) -> RunStatistics:
    msd = msd_digits(normalize(word))
    runs: list[tuple[int, int]] = []
    current = msd[0]
    length = 1
    for d in msd[1:]:
        if d == current:
            length += 1
        else:
            runs.append((current, length))
            current = d
            length = 1
    runs.append((current, length))
    run_t = tuple(runs)
    lengths = tuple(ln for _, ln in run_t)
    return RunStatistics(
        runs=run_t,
        number_of_runs=len(run_t),
        leading_run=run_t[0],
        trailing_run=run_t[-1],
        run_lengths=lengths,
        max_run=max(lengths),
    )


@dataclass(frozen=True)
class ZeroGapStatistics:
    """Zero-run lengths and gaps between nonzero digits.

    ``zero_run_lengths`` lists maximal consecutive-zero runs in MSD-first
    order (empty if the word has no zeros). ``gaps_between_nonzero`` lists
    the number of zeros strictly between successive nonzero digits, still
    in MSD-first order. Lengths do not depend on indexing origin.
    """

    zero_run_lengths: tuple[int, ...]
    max_zero_run: int
    nonzero_run_lengths: tuple[int, ...]
    gaps_between_nonzero: tuple[int, ...]


def zero_gap_statistics(word: WordLike) -> ZeroGapStatistics:
    msd = msd_digits(normalize(word))
    zero_runs: list[int] = []
    nonzero_runs: list[int] = []
    gaps: list[int] = []
    seen_nonzero = False
    zeros_since_nonzero = 0

    i = 0
    n = len(msd)
    while i < n:
        d = msd[i]
        j = i
        while j < n and msd[j] == d:
            j += 1
        length = j - i
        if d == 0:
            zero_runs.append(length)
            if seen_nonzero:
                zeros_since_nonzero += length
        else:
            nonzero_runs.append(length)
            if seen_nonzero:
                gaps.append(zeros_since_nonzero)
            zeros_since_nonzero = 0
            seen_nonzero = True
        i = j

    return ZeroGapStatistics(
        zero_run_lengths=tuple(zero_runs),
        max_zero_run=max(zero_runs) if zero_runs else 0,
        nonzero_run_lengths=tuple(nonzero_runs),
        gaps_between_nonzero=tuple(gaps),
    )


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def bt_weight(n: int) -> int:
    return weight(encode(_require_int(n)))


def d_bt(a: int, b: int) -> int:
    """``d_BT(a, b) = w(a - b)``."""
    return bt_weight(_require_int(a, "a") - _require_int(b, "b"))


def carry_defect(a: int, b: int) -> int:
    """``w(a) + w(b) - w(a + b)``. May be negative."""
    a = _require_int(a, "a")
    b = _require_int(b, "b")
    return bt_weight(a) + bt_weight(b) - bt_weight(a + b)


def metric_properties(limit: int) -> dict[str, object]:
    """Exhaustive metric-like checks of ``d_BT`` on ``[-limit, limit]``.

    Returns witnesses rather than asserting a theorem.
    """
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    values = range(-limit, limit + 1)
    symmetry_fail: tuple[int, int] | None = None
    definite_fail: int | None = None
    triangle_fail: tuple[int, int, int, int, int] | None = None
    for a in values:
        if d_bt(a, a) != 0:
            definite_fail = a
            break
        if a != 0 and d_bt(a, 0) == 0:
            definite_fail = a
            break
    if definite_fail is None:
        for a in values:
            for b in values:
                if d_bt(a, b) != d_bt(b, a):
                    symmetry_fail = (a, b)
                    break
            if symmetry_fail is not None:
                break
    if definite_fail is None and symmetry_fail is None:
        if limit <= 12:
            triples = ((a, b, c) for a in values for b in values for c in values)
        else:
            sample = list(values)

            def triples():
                for a in sample:
                    for b in sample:
                        yield a, b, a
                        yield a, b, b
                        yield a, 0, b
                        yield a, b, -b
                        yield a, -a, b
                for a in sample:
                    yield a, a + 1 if a < limit else a - 1, a - 1 if a > -limit else a + 1

            triples = triples()
        for a, b, c in triples:
            left = d_bt(a, c)
            right = d_bt(a, b) + d_bt(b, c)
            if left > right:
                triangle_fail = (a, b, c, left, right)
                break
    return {
        "limit": limit,
        "symmetric": symmetry_fail is None,
        "definite": definite_fail is None,
        "triangle": triangle_fail is None,
        "symmetry_witness": symmetry_fail,
        "definite_witness": definite_fail,
        "triangle_witness": triangle_fail,
    }


def carry_defect_scan(limit: int) -> dict[str, object]:
    """Min/max carry defect and whether it takes both signs on a box."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    min_d = None
    max_d = None
    min_pair = None
    max_pair = None
    negative_count = 0
    zero_count_local = 0
    positive_count = 0
    for a in range(-limit, limit + 1):
        for b in range(-limit, limit + 1):
            d = carry_defect(a, b)
            if min_d is None or d < min_d:
                min_d = d
                min_pair = (a, b, d)
            if max_d is None or d > max_d:
                max_d = d
                max_pair = (a, b, d)
            if d < 0:
                negative_count += 1
            elif d == 0:
                zero_count_local += 1
            else:
                positive_count += 1
    return {
        "limit": limit,
        "min": min_d,
        "max": max_d,
        "min_pair": min_pair,
        "max_pair": max_pair,
        "negative_count": negative_count,
        "zero_count": zero_count_local,
        "positive_count": positive_count,
        "always_nonnegative": negative_count == 0,
    }


def disjoint_support_zero_defect(a: int, b: int) -> bool:
    """True if ``a`` and ``b`` have disjoint BT supports.

    **EXACT — HUMAN PROOF:** then there is no digitwise overlap, addition is carry-free,
    and ``carry_defect(a, b) = 0``.
    """
    from bt.support import support

    sa = set(support(a))
    sb = set(support(b))
    return sa.isdisjoint(sb)


def v2(n: int) -> int | None:
    """2-adic valuation ``v_2(n)``. ``None`` means ``v_2(0) = ∞``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0:
        return None
    v = 0
    m = n if n > 0 else -n
    while m % 2 == 0:
        m //= 2
        v += 1
    return v


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
