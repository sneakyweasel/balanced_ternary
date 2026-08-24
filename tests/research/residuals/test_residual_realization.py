"""One-state residual machines are ax for a trit."""

from __future__ import annotations

from itertools import product

from bt.calculus.section import IntPoly
from research.residuals.residual_realization import (
    ONE_STATE_ABSTRACT,
    is_one_state_residual,
    one_state_polynomials,
    two_state_residual_graphs,
)


def test_one_state_list_is_exact_in_coefficient_box():
    listed = set(one_state_polynomials())
    extras = []
    for coeffs in product(range(-3, 4), repeat=4):
        f = IntPoly(coeffs)
        if is_one_state_residual(f) and f not in listed:
            extras.append(f.coeffs)
    assert extras == []
    assert all(is_one_state_residual(f) for f in listed)


def test_abstract_one_state_count_is_729():
    assert ONE_STATE_ABSTRACT == 729


def test_two_state_graphs_are_few():
    assert two_state_residual_graphs() == 12
