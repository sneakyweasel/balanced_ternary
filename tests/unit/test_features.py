"""Tests for weight, counts, runs, and position-class sums."""

from __future__ import annotations

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
from bt.representation import encode


def test_weight_and_counts_for_five():
    w = encode(5)  # "+--"
    assert weight(w) == 3
    assert signed_digit_sum(w) == -1
    assert positive_digit_count(w) == 1
    assert negative_digit_count(w) == 2
    assert zero_count(w) == 0


def test_weight_and_counts_for_forty_two():
    w = encode(42)  # "+---0"
    assert weight(w) == 4
    assert signed_digit_sum(w) == 1 - 1 - 1 - 1 + 0
    assert positive_digit_count(w) == 1
    assert negative_digit_count(w) == 3
    assert zero_count(w) == 1


def test_position_class_sums_lsd_indexing():
    # 5: a = (-1, -1, +1)
    assert position_class_sums(encode(5), 2) == (0, -1)  # S0=-1+1, S1=-1
    assert position_class_sums(encode(5), 3) == (-1, -1, 1)
    # 42: a = (0, -1, -1, -1, 1)  → S0 = 0+(-1)+1, S1 = (-1)+(-1)
    assert position_class_sums(encode(42), 2) == (0, -2)


def test_run_statistics_leading_trailing():
    stats = run_statistics(encode(42))  # "+---0"
    assert stats.number_of_runs == 3
    assert stats.leading_run == (1, 1)
    assert stats.trailing_run == (0, 1)
    assert stats.run_lengths == (1, 3, 1)

    five = run_statistics(encode(5))  # "+--"
    assert five.leading_run == (1, 1)
    assert five.trailing_run == (-1, 2)


def test_zero_gap_statistics():
    # 3 = "+0" : one zero run of length 1 between + and (end)
    z = zero_gap_statistics(encode(3))
    assert z.zero_run_lengths == (1,)
    assert z.max_zero_run == 1
    assert z.nonzero_run_lengths == (1,)

    z0 = zero_gap_statistics(encode(0))
    assert z0.zero_run_lengths == (1,)
    assert z0.nonzero_run_lengths == ()
    assert z0.gaps_between_nonzero == ()

    # 9 = "+00"
    z9 = zero_gap_statistics(encode(9))
    assert encode(9).word() == "+00"
    assert z9.max_zero_run == 2
    assert z9.gaps_between_nonzero == ()  # only one nonzero digit
