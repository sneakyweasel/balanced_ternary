"""Residual of a sum differs by a constant carry."""

from __future__ import annotations

from itertools import product

from bt.calculus.residual import TRITS
from bt.calculus.section import parse_poly
from research.residuals.add_residual import residual_carry_constant, sum_residual_identity


def test_carry_is_always_constant():
    pairs = (
        (parse_poly("x^3"), parse_poly("x^2")),
        (parse_poly("x^4"), parse_poly("2x-1")),
        (parse_poly("x^3-x"), parse_poly("x^3")),
    )
    for f, g in pairs:
        for m in range(4):
            for word in product(TRITS, repeat=m):
                carry = residual_carry_constant(f, g, word)
                assert carry.degree <= 0
                assert sum_residual_identity(f, g, word)
