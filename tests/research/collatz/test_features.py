"""Tests for Collatz balanced ternary features and transition schema."""

from __future__ import annotations

from bt.metrics import weight
from bt.representation import encode
from research.collatz.features import FEATURE_NAMES, NUMERIC_FEATURE_NAMES, extract_features
from research.collatz.transitions import ROW_COLUMNS, feature_transition


def test_feature_vector_matches_existing_extractors():
    word = encode(27)
    feat = extract_features(word)
    assert feat.weight == weight(word)
    assert feat.weight_parity == weight(word) % 2
    assert feat.length == len(word)
    assert feat.positive_digit_count + feat.negative_digit_count == feat.weight


def test_transition_schema_columns():
    trans = feature_transition(27)
    row = trans.to_row()
    for col in ROW_COLUMNS:
        assert col in row
    assert trans.n == 27
    assert trans.T_n == 41
    assert trans.v2_three_n_plus_one == 1
    assert trans.ternary_shift_add_one_matches
    assert trans.balanced_ternary_n == encode(27).word()
    assert trans.balanced_ternary_T_n == encode(41).word()
    assert trans.balanced_ternary_three_n_plus_one == encode(82).word()


def test_deltas_are_output_minus_input():
    trans = feature_transition(27)
    for name in NUMERIC_FEATURE_NAMES:
        expected = getattr(trans.features_T_n, name) - getattr(trans.features_n, name)
        assert trans.deltas[f"delta_{name}"] == expected


def test_every_odd_row_has_odd_input_weight_even_intermediate():
    for n in range(1, 500, 2):
        trans = feature_transition(n)
        assert trans.features_n.weight_parity == 1
        assert trans.features_three_n_plus_one.weight_parity == 0
        assert trans.features_T_n.weight_parity == 1
        assert trans.ternary_shift_add_one_matches
        assert set(trans.to_row()) >= set(ROW_COLUMNS)


def test_prefixed_feature_names_are_documented():
    for prefix in ("n", "three_n_plus_one", "T_n"):
        for name in FEATURE_NAMES:
            assert f"{prefix}_{name}" in ROW_COLUMNS
