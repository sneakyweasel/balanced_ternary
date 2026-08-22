"""Trit algebra and three-way comparison."""

from __future__ import annotations

from bt.calculus.order import cmp3
from bt.calculus.trit import (
    Trit,
    algebraic_name,
    as_trit,
    compare,
    is_boolean_algebra,
    is_bounded_lattice,
    is_de_morgan,
    is_distributive_lattice,
    is_kleene_algebra,
    neg,
    sign_trit,
    trit_max,
    trit_min,
)


def test_trit_values():
    assert list(Trit) == [Trit.MINUS, Trit.ZERO, Trit.PLUS]
    assert int(Trit.MINUS) == -1
    assert as_trit(1) is Trit.PLUS


def test_lattice_and_kleene_axioms():
    assert is_bounded_lattice()
    assert is_distributive_lattice()
    assert is_de_morgan()
    assert is_kleene_algebra()
    assert not is_boolean_algebra()
    assert "Kleene" in algebraic_name()
    assert "not Boolean" in algebraic_name()


def test_neg_min_max():
    assert neg(Trit.MINUS) is Trit.PLUS
    assert trit_min(Trit.PLUS, Trit.MINUS) is Trit.MINUS
    assert trit_max(Trit.ZERO, Trit.MINUS) is Trit.ZERO
    assert compare(Trit.PLUS, Trit.MINUS) is Trit.PLUS


def test_cmp3_laws():
    for x in range(-50, 51):
        for y in range(-50, 51):
            z = 7
            assert cmp3(x + z, y + z) == cmp3(x, y)
            assert cmp3(-x, -y) == neg(cmp3(x, y))
            assert cmp3(x, y) == neg(cmp3(y, x))
            assert cmp3(x, y) == sign_trit(x - y)
            assert cmp3(3 * x, 3 * y) == cmp3(x, y)
            assert cmp3(-3 * x, -3 * y) == neg(cmp3(x, y))
