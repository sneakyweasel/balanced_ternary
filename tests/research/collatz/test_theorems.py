"""Tests for Layer A: BT(3n+1) = BT(n)+ and closed-form features."""

from __future__ import annotations

import pytest

from bt.representation import decode, encode
from research.collatz.bt_arithmetic import three_n_plus_one_word
from research.collatz.features import extract_features
from research.collatz.theorems import (
    append_plus,
    append_plus_agrees_with_adder,
    append_plus_matches_integer,
    predicted_features_after_append_plus,
    shift_position_class_sums,
    three_n_plus_one_from_word,
)
from research.collatz.transitions import feature_transition


def test_append_plus_rejects_zero():
    with pytest.raises(ValueError):
        append_plus(encode(0))
    assert three_n_plus_one_from_word(encode(0)) == encode(1)


def test_append_plus_examples():
    assert append_plus(encode(27)).word() == encode(27).word() + "+"
    assert append_plus(encode(27)) == encode(82)
    assert append_plus(encode(5)).word() == "+--+"
    assert append_plus(encode(1)).word() == "++"


def test_append_plus_equals_encode_range():
    for n in list(range(-300, 0)) + list(range(1, 301)):
        assert append_plus_matches_integer(n)
        assert append_plus_agrees_with_adder(n)
        assert three_n_plus_one_from_word(encode(n)) == encode(3 * n + 1)
        assert three_n_plus_one_word(encode(n)) == append_plus(encode(n))


def test_closed_form_features():
    for n in list(range(-200, 0)) + list(range(1, 201)):
        word = encode(n)
        src = extract_features(word)
        pred = predicted_features_after_append_plus(word)
        actual = extract_features(encode(3 * n + 1))
        assert pred == actual
        assert pred.length == src.length + 1
        assert pred.weight == src.weight + 1
        assert pred.signed_digit_sum == src.signed_digit_sum + 1
        assert pred.positive_digit_count == src.positive_digit_count + 1
        assert pred.negative_digit_count == src.negative_digit_count
        assert pred.zero_count == src.zero_count
        assert pred.position_class_sums_period_2 == shift_position_class_sums(
            src.position_class_sums_period_2
        )
        assert pred.position_class_sums_period_3 == shift_position_class_sums(
            src.position_class_sums_period_3
        )


def test_feature_transition_records_append_plus():
    trans = feature_transition(27)
    assert trans.append_plus_matches
    assert trans.append_plus_features_match
    assert trans.predicted_features_three_n_plus_one == trans.features_three_n_plus_one
