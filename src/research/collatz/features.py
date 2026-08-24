"""Balanced ternary features of Collatz states.

All position-dependent quantities reuse the existing LSD-first convention
from ``bt.metrics``. This module does not reimplement them.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from bt.metrics import (
    negative_digit_count,
    position_class_sums,
    positive_digit_count,
    run_statistics,
    signed_digit_sum,
    weight,
    zero_count,
    zero_gap_statistics,
)
from bt.representation import WordLike, encode, normalize


DEFAULT_POSITION_PERIODS: tuple[int, ...] = (2, 3)

NUMERIC_FEATURE_NAMES: tuple[str, ...] = (
    "length",
    "weight",
    "weight_parity",
    "signed_digit_sum",
    "positive_digit_count",
    "negative_digit_count",
    "zero_count",
    "number_of_runs",
    "max_run_length",
    "max_zero_run",
)

TUPLE_FEATURE_NAMES: tuple[str, ...] = (
    "zero_run_lengths",
    "nonzero_run_lengths",
    "gaps_between_nonzero",
    "position_class_sums_period_2",
    "position_class_sums_period_3",
)

FEATURE_NAMES: tuple[str, ...] = NUMERIC_FEATURE_NAMES + TUPLE_FEATURE_NAMES


@dataclass(frozen=True)
class BalancedTernaryFeatures:
    length: int
    weight: int
    weight_parity: int
    signed_digit_sum: int
    positive_digit_count: int
    negative_digit_count: int
    zero_count: int
    number_of_runs: int
    max_run_length: int
    max_zero_run: int
    zero_run_lengths: tuple[int, ...]
    nonzero_run_lengths: tuple[int, ...]
    gaps_between_nonzero: tuple[int, ...]
    position_class_sums_period_2: tuple[int, ...]
    position_class_sums_period_3: tuple[int, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def prefixed_dict(self, prefix: str) -> dict[str, object]:
        return {f"{prefix}_{key}": value for key, value in self.as_dict().items()}


def extract_features(
    word: WordLike,
    periods: tuple[int, ...] = DEFAULT_POSITION_PERIODS,
) -> BalancedTernaryFeatures:
    """Extract the Milestone-1 Collatz feature vector of a word."""
    canonical = normalize(word)
    w = weight(canonical)
    runs = run_statistics(canonical)
    gaps = zero_gap_statistics(canonical)
    period_map = {p: position_class_sums(canonical, p) for p in periods}
    return BalancedTernaryFeatures(
        length=len(canonical),
        weight=w,
        weight_parity=w % 2,
        signed_digit_sum=signed_digit_sum(canonical),
        positive_digit_count=positive_digit_count(canonical),
        negative_digit_count=negative_digit_count(canonical),
        zero_count=zero_count(canonical),
        number_of_runs=runs.number_of_runs,
        max_run_length=runs.max_run,
        max_zero_run=gaps.max_zero_run,
        zero_run_lengths=gaps.zero_run_lengths,
        nonzero_run_lengths=gaps.nonzero_run_lengths,
        gaps_between_nonzero=gaps.gaps_between_nonzero,
        position_class_sums_period_2=period_map.get(2, position_class_sums(canonical, 2)),
        position_class_sums_period_3=period_map.get(3, position_class_sums(canonical, 3)),
    )


def features_of_int(n: int) -> BalancedTernaryFeatures:
    return extract_features(encode(n))
