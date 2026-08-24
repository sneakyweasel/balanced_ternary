"""Tests for encode / decode / normalize / canonical form."""

from __future__ import annotations

import pytest

from bt.representation import (
    BalancedTernary,
    decode,
    digits,
    encode,
    is_canonical,
    normalize,
)


def test_spec_examples_computed_not_hardcoded():
    five = encode(5)
    assert decode(five) == 5
    assert five.word() == "+--"

    forty_two = encode(42)
    assert decode(forty_two) == 42
    assert forty_two.word() == "+---0"


def test_zero_and_units():
    assert encode(0).word() == "0"
    assert decode("0") == 0
    assert encode(1).word() == "+"
    assert encode(-1).word() == "-"
    assert encode(2).word() == "+-"
    assert encode(-2).word() == "-+"
    assert encode(3).word() == "+0"
    assert encode(-3).word() == "-0"


def test_negative_is_digitwise_negation():
    for n in range(0, 200):
        assert encode(-n) == -encode(n)


def test_canonical_no_leading_zero():
    for n in range(-200, 201):
        w = encode(n).word()
        if n == 0:
            assert w == "0"
        else:
            assert not w.startswith("0")
            assert w[0] in "+-"
        assert is_canonical(w)


def test_positive_msd_is_plus():
    for n in range(1, 500):
        assert encode(n).word()[0] == "+"


def test_normalize_strips_leading_zeros():
    assert normalize("000").word() == "0"
    assert normalize("00+").word() == "+"
    assert normalize("+--").word() == "+--"
    assert decode("00+") == 1
    assert is_canonical("00+") is False
    assert is_canonical("+") is True


def test_normalize_idempotent():
    for n in [*range(-50, 51), 12345, -999]:
        w = encode(n)
        assert normalize(w) == w
        assert normalize(w.word()) == w


def test_digits_are_lsd_first():
    # 5 = 1*9 + (-1)*3 + (-1)*1  -> displayed "+--"
    assert digits(encode(5)) == (-1, -1, 1)
    assert digits("+--")[0] == -1  # a_0, last displayed character


def test_invalid_words():
    with pytest.raises(ValueError):
        decode("")
    with pytest.raises(ValueError):
        normalize("++x")
    with pytest.raises(ValueError):
        decode("2")
    with pytest.raises(TypeError):
        encode(True)
    with pytest.raises(TypeError):
        encode(1.0)  # type: ignore[arg-type]


def test_balanced_ternary_rejects_empty_and_bad_digits():
    with pytest.raises(ValueError):
        BalancedTernary(())
    with pytest.raises(ValueError):
        BalancedTernary((2,))


@pytest.mark.slow
def test_round_trip_million():
    """decode(encode(n)) == n for all n in [-10^6, 10^6]."""
    for n in range(-1_000_000, 1_000_001):
        if decode(encode(n)) != n:
            pytest.fail(f"round trip failed at n={n}")
