"""Tests for v2 and finite-precision valuation classification."""

from __future__ import annotations

import pytest

from research.collatz.core import collatz_valuation
from research.collatz.valuation import (
    AT_LEAST_K,
    classify_collatz_valuation,
    v2,
)


def test_v2_basic():
    assert v2(0) is None
    assert v2(1) == 0
    assert v2(-1) == 0
    assert v2(2) == 1
    assert v2(-8) == 3
    assert v2(12) == 2
    assert v2(16) == 4


def test_v2_rejects_non_int():
    with pytest.raises(TypeError):
        v2(True)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        v2(1.0)  # type: ignore[arg-type]


def test_collatz_valuation_matches_v2():
    for n in range(1, 2000, 2):
        assert collatz_valuation(n) == v2(3 * n + 1)


def test_classify_exact_when_below_precision():
    for precision in range(1, 10):
        modulus = 1 << precision
        for n in range(1, 4000, 2):
            actual = v2(3 * n + 1)
            assert actual is not None
            cls = classify_collatz_valuation(n % modulus, precision)
            if actual < precision:
                assert cls.is_exact
                assert cls.exact_k == actual
                assert cls.label() == str(actual)
            else:
                assert not cls.is_exact
                assert cls.kind == AT_LEAST_K
                assert cls.label() == AT_LEAST_K
                assert actual >= precision


def test_classify_cannot_separate_k_equals_precision_from_larger():
    """Mod 2^K, v2 = K and v2 > K both look like y ≡ 0. Not exact."""
    # n = 1: 3*1+1 = 4, v2 = 2. At precision 2 this is AT_LEAST_K, not exact 2.
    cls = classify_collatz_valuation(1, 2)
    assert not cls.is_exact
    assert v2(4) == 2
    # n = 5: 16, v2 = 4. At precision 4 this is AT_LEAST_K.
    cls4 = classify_collatz_valuation(5 % 16, 4)
    assert not cls4.is_exact
    assert v2(16) == 4
    # At precision 5, v2(16)=4 is exact.
    cls5 = classify_collatz_valuation(5 % 32, 5)
    assert cls5.is_exact and cls5.exact_k == 4


def test_even_residue_gives_valuation_zero_when_visible():
    cls = classify_collatz_valuation(2, 4)
    assert cls.is_exact and cls.exact_k == 0


def test_precision_must_be_positive():
    with pytest.raises(ValueError):
        classify_collatz_valuation(1, 0)
