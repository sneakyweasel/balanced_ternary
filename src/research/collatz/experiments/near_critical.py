"""Reproducible exponent-code datasets near ``3^m / 2^K = 1``.

Membership decisions use integer cross multiplication only.  Decimal/log
values may be added by diagnostic objects for display, but never select rows.
The named Rozier--Terracol pairs are fixtures from their finite computation;
they are not asserted to classify accelerated valuation codes.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from research.collatz.cylinders import parse_ks
from research.collatz.experiments.information_content import diagnostic_row
from research.collatz.experiments.schema import COMPATIBILITY_SCHEMA_VERSION, ExperimentManifest
from research.collatz.experiments.table_io import write_experiment


ROZIER_TERRACOL_FIXTURE_PAIRS: tuple[tuple[int, int], ...] = (
    (8, 5),
    (27, 17),
    (46, 29),
    (54, 34),
    (65, 41),
    (73, 46),
    (92, 58),
)


@dataclass(frozen=True)
class ExactDriftBand:
    """Closed rational band ``lower <= 3^m/2^K <= upper``."""

    lower_numerator: int = 3
    lower_denominator: int = 4
    upper_numerator: int = 4
    upper_denominator: int = 3

    def __post_init__(self) -> None:
        values = (
            self.lower_numerator,
            self.lower_denominator,
            self.upper_numerator,
            self.upper_denominator,
        )
        if any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in values):
            raise ValueError("drift-band bounds must be positive integers")
        if self.lower_numerator * self.upper_denominator > (
            self.upper_numerator * self.lower_denominator
        ):
            raise ValueError("lower drift bound exceeds upper drift bound")

    @property
    def lower(self) -> Fraction:
        return Fraction(self.lower_numerator, self.lower_denominator)

    @property
    def upper(self) -> Fraction:
        return Fraction(self.upper_numerator, self.upper_denominator)

    def contains(self, m: int, K: int) -> bool:
        _validate_m_K(m, K)
        three = pow(3, m)
        two = 1 << K
        return (
            three * self.lower_denominator >= two * self.lower_numerator
            and three * self.upper_denominator <= two * self.upper_numerator
        )

    def as_dict(self) -> dict[str, list[int]]:
        return {
            "lower": [self.lower_numerator, self.lower_denominator],
            "upper": [self.upper_numerator, self.upper_denominator],
        }


DEFAULT_DRIFT_BAND = ExactDriftBand()


def _validate_m_K(m: int, K: int) -> None:
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError("m must be an integer >= 1")
    if isinstance(K, bool) or not isinstance(K, int) or K < m:
        raise ValueError("K must be an integer >= m")


def exact_drift_pair(valuations: Sequence[int] | str) -> tuple[int, int]:
    """Return the unreduced exact pair ``(3^m, 2^K)``."""
    ks = parse_ks(valuations)
    return pow(3, len(ks)), 1 << sum(ks)


def is_near_critical(
    valuations_or_m: Sequence[int] | str | int,
    K: int | None = None,
    *,
    band: ExactDriftBand = DEFAULT_DRIFT_BAND,
) -> bool:
    """Exact membership for a code, or for an explicit ``(m,K)`` pair."""
    if isinstance(valuations_or_m, int) and not isinstance(valuations_or_m, bool):
        if K is None:
            raise ValueError("K is required when the first argument is m")
        return band.contains(valuations_or_m, K)
    if K is not None:
        raise ValueError("K must be omitted when passing a valuation code")
    ks = parse_ks(valuations_or_m)
    return band.contains(len(ks), sum(ks))


def critical_K(m: int) -> int:
    """Choose the integer ``K`` making ``3^m/2^K`` closest to 1.

    The comparison is exact: for the two powers bracketing ``3^m``, compare
    multiplicative distance by testing ``3^(2m)`` against ``2^(2K+1)``.
    """
    _validate_m_K(m, m)
    target = pow(3, m)
    lower = target.bit_length() - 1
    if target == 1 << lower:
        return lower
    return lower if target * target <= 1 << (2 * lower + 1) else lower + 1


def critical_K_values(
    m: int,
    *,
    band: ExactDriftBand = DEFAULT_DRIFT_BAND,
) -> tuple[int, ...]:
    """All integer budgets in the exact band, in increasing order."""
    _validate_m_K(m, m)
    center = critical_K(m)
    out: list[int] = []
    K = max(m, center)
    while K > m and band.contains(m, K - 1):
        K -= 1
    while band.contains(m, K):
        out.append(K)
        K += 1
    return tuple(out)


def exhaustive_near_critical_codes(
    max_length: int,
    max_k: int,
    *,
    band: ExactDriftBand = DEFAULT_DRIFT_BAND,
) -> tuple[tuple[int, ...], ...]:
    """Exhaust all bounded codes and retain exact band members."""
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 1:
        raise ValueError("max_length must be an integer >= 1")
    if isinstance(max_k, bool) or not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    return tuple(
        ks
        for m in range(1, max_length + 1)
        for ks in product(range(1, max_k + 1), repeat=m)
        if band.contains(m, sum(ks))
    )


def _random_composition(
    total: int, length: int, rng: random.Random
) -> tuple[int, ...]:
    if total < length:
        raise ValueError("a positive composition requires total >= length")
    if length == 1:
        return (total,)
    cuts = sorted(rng.sample(range(1, total), length - 1))
    points = (0, *cuts, total)
    return tuple(points[index + 1] - points[index] for index in range(length))


def seeded_random_critical_codes(
    length: int,
    count: int,
    *,
    seed: int,
    band: ExactDriftBand = DEFAULT_DRIFT_BAND,
) -> tuple[tuple[int, ...], ...]:
    """Generate seeded random positive compositions with exact critical budgets."""
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("count must be an integer >= 0")
    budgets = critical_K_values(length, band=band)
    if not budgets and count:
        raise ValueError("the requested drift band contains no integer budget")
    rng = random.Random(seed)
    return tuple(
        _random_composition(rng.choice(budgets), length, rng) for _ in range(count)
    )


def mechanical_critical_code(length: int) -> tuple[int, ...]:
    """A deterministic 1/2 word whose prefix budgets track critical ``K``."""
    _validate_m_K(length, length)
    totals = [0]
    for m in range(1, length + 1):
        totals.append(critical_K(m))
    code = tuple(totals[index + 1] - totals[index] for index in range(length))
    if any(k < 1 for k in code):
        raise ArithmeticError("mechanical critical construction produced k < 1")
    return code


def distinct_permutations(valuations: Sequence[int] | str) -> tuple[tuple[int, ...], ...]:
    ks = parse_ks(valuations)
    return tuple(sorted(set(permutations(ks))))


def adversarial_rearrangements(
    valuations: Sequence[int] | str,
) -> tuple[tuple[int, ...], ...]:
    """Deterministic order-sensitive arrangements of one fixed budget."""
    ks = parse_ks(valuations)
    ascending = tuple(sorted(ks))
    descending = tuple(reversed(ascending))
    low_high: list[int] = []
    left, right = 0, len(ascending) - 1
    while left <= right:
        low_high.append(ascending[left])
        left += 1
        if left <= right:
            low_high.append(ascending[right])
            right -= 1
    high_low = tuple(reversed(low_high))
    return tuple(dict.fromkeys((ks, ascending, descending, tuple(low_high), high_low)))


def rozier_terracol_fixture_pairs() -> tuple[dict[str, object], ...]:
    """Return named standard-map fixture pairs with exact ratios."""
    return tuple(
        {
            "K_standard_steps": K,
            "m_odd_steps": m,
            "three_power": pow(3, m),
            "two_power": 1 << K,
            "contracting": pow(3, m) < 1 << K,
            "source_status": "REPORTED COMPUTATIONAL FIXTURE (Rozier-Terracol)",
        }
        for K, m in ROZIER_TERRACOL_FIXTURE_PAIRS
    )


def _tagged(codes: Iterable[tuple[int, ...]], family: str) -> Iterator[tuple[str, tuple[int, ...]]]:
    for code in codes:
        yield family, code


@dataclass(frozen=True)
class NearCriticalResult:
    rows: tuple[dict[str, object], ...]
    fixtures: tuple[dict[str, object], ...]
    paths: dict[str, str]
    seed: int
    schema_version: str = COMPATIBILITY_SCHEMA_VERSION


def run_near_critical(
    *,
    exhaustive_max_length: int = 4,
    exhaustive_max_k: int = 4,
    random_length: int = 16,
    random_count: int = 32,
    seed: int = 0,
    mechanical_lengths: Sequence[int] = (8, 16, 32),
    permutation_code: Sequence[int] | str = (1, 1, 2, 2),
    band: ExactDriftBand = DEFAULT_DRIFT_BAND,
    output_dir: Path | str | None = None,
) -> NearCriticalResult:
    """Build exhaustive, random, mechanical, permutation and adversarial rows."""
    exhaustive = exhaustive_near_critical_codes(
        exhaustive_max_length, exhaustive_max_k, band=band
    )
    random_codes = seeded_random_critical_codes(
        random_length, random_count, seed=seed, band=band
    )
    mechanical = tuple(mechanical_critical_code(length) for length in mechanical_lengths)
    permutation_codes = distinct_permutations(permutation_code)
    adversarial = adversarial_rearrangements(permutation_code)
    tagged = (
        *_tagged(exhaustive, "exhaustive"),
        *_tagged(random_codes, "seeded_random_critical"),
        *_tagged(mechanical, "mechanical"),
        *_tagged(permutation_codes, "fixed_budget_permutation"),
        *_tagged(adversarial, "adversarial_rearrangement"),
    )
    rows: list[dict[str, object]] = []
    for index, (family, code) in enumerate(tagged):
        row = diagnostic_row(code)
        row.update(
            {
                "family": family,
                "family_index": index,
                "near_critical": band.contains(len(code), sum(code)),
                "selection_arithmetic": "exact integer cross multiplication",
            }
        )
        rows.append(row)
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="near_critical_compatibility",
            parameters={
                "exhaustive_max_length": exhaustive_max_length,
                "exhaustive_max_k": exhaustive_max_k,
                "random_length": random_length,
                "random_count": random_count,
                "seed": seed,
                "mechanical_lengths": list(mechanical_lengths),
                "permutation_code": list(parse_ks(permutation_code)),
                "drift_band": band.as_dict(),
                "selection": "integer-only; deterministic family ordering",
            },
            row_count=len(rows),
            claim_status=(
                "EXACT generation and drift membership; dataset patterns are "
                "OBSERVATIONS, not Collatz claims"
            ),
            schema_version=COMPATIBILITY_SCHEMA_VERSION,
        )
        paths = write_experiment(rows, output_dir, "near_critical", manifest)
    return NearCriticalResult(
        tuple(rows), rozier_terracol_fixture_pairs(), paths, seed
    )
