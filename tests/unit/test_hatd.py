"""Normalized coefficient derivative ``hat D``."""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.normtheory.calculus_link import D_coeff, I_coeff
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.complexity import enumerate_words
from bt.normtheory.hatd import (
    hatD,
    hatD_I_canonical,
    hatD_I_raw,
    hatD_raw,
    hatD_via_normalize,
    milestone14_witness,
)
from bt.normtheory.strategies import normal_form
from bt.representation import encode


def test_hatD_raw_is_semantic():
    for word in enumerate_words(3, 2):
        assert hatD_raw(word).value() == D(word.value())
        assert hatD(word).coeffs == encode(D(word.value())).digits_lsd()
        assert hatD(word).coeffs == hatD_via_normalize(word).coeffs
    w = milestone14_witness()
    assert hatD_raw(w).coeffs == (1,)
    assert hatD(w).coeffs == (1,)
    assert D_coeff(w).value() != hatD_raw(w).value()


def test_canonical_drop_when_trit_lsd():
    w = CoeffWord((1, 2, -2))
    assert w.coefficient(0) in (-1, 0, 1)
    assert D_coeff(w).value() == D(w.value())
    assert hatD_raw(w).value() == D_coeff(w).value()


def test_hatD_I_raw_is_section():
    for a in (-1, 0, 1):
        for word in enumerate_words(2, 2):
            got = hatD_I_raw(a, word)
            assert got.coeffs == word.coeffs
            can = hatD_I_canonical(a, word)
            assert can.coeffs == normal_form(word).coeffs
            if not word.is_canonical():
                assert can.coeffs != word.coeffs or word.coeffs == (0,)
