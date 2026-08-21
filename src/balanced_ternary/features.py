"""Digit statistics of canonical balanced ternary words.

All position-dependent quantities use least-significant-first indexing:
``a_0`` is the last displayed digit. Run statistics that refer to *leading*
or *trailing* digits follow the displayed (most-significant-first) word, so
``trailing_run`` is the run containing ``a_0``.
"""

from __future__ import annotations

from dataclasses import dataclass

from balanced_ternary.representation import WordLike, digits, msd_digits, normalize


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
