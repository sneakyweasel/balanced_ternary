"""Integer recurrences, lattice inverses, and linear forms."""

from __future__ import annotations

from fractions import Fraction

from research_engine.algebra.lattices import (
    characteristic_polynomial,
    integer_affine_preimage,
    inverse_over_q,
    matrix_det,
)
from research_engine.algebra.linear_functionals import LinearFunctional, left_multiply
from research_engine.algebra.recurrences import RecurrenceSpec


def test_fibonacci_recurrence_is_not_ostrowski():
    spec = RecurrenceSpec(coefficients=(1, 1), initial_values=(0, 1))
    assert spec.sequence(8) == (0, 1, 1, 2, 3, 5, 8, 13)
    assert spec.term(-1) == 0
    assert spec.verify_recurrence(spec.sequence(10))
    assert spec.companion_matrix() == ((0, 1), (1, 1))
    assert spec.characteristic_polynomial() == (1, -1, -1)
    assert spec.companion_charpoly_matches()
    assert characteristic_polynomial(spec.companion_matrix()) == (1, -1, -1)


def test_doubling_recurrence_is_not_ostrowski():
    spec = RecurrenceSpec(coefficients=(2,), initial_values=(1,))
    assert spec.sequence(5) == (1, 2, 4, 8, 16)
    assert spec.companion_matrix() == ((2,),)
    assert spec.characteristic_polynomial() == (1, -2)
    assert spec.companion_charpoly_matches()


def test_integer_affine_preimage_is_exact():
    matrix = ((2, 0), (0, 2))
    assert integer_affine_preimage(matrix, (1, 0), (5, 2)) == (2, 1)
    assert integer_affine_preimage(matrix, (1, 0), (4, 2)) is None
    inverse = inverse_over_q(((3, 0), (0, 1)))
    assert inverse[0][0] == Fraction(1, 3)
    assert matrix_det(((1, 2), (3, 4))) == -2


def test_linear_form_observation_is_not_an_invariant():
    form = LinearFunctional((1, -2))
    states = ((0, 0), (3, 1), (-1, 4))
    assert form((3, 1)) == 1
    assert form.observed_bound(states) == 9
    assert left_multiply((1, 0), ((0, 2), (3, 1))) == (0, 2)


def test_exact_pisot_cubic_certificate_does_not_use_floats():
    from research_engine.algebra.spectral import cubic_roots, exact_pisot_cubic_certificate

    np_cert = exact_pisot_cubic_certificate((1, -2, -1, -3))
    assert np_cert["perron_non_pisot"]
    assert np_cert["pisot"] is False
    assert np_cert["real_root_interval"] == (2, 3)
    p_cert = exact_pisot_cubic_certificate((1, -2, -1, -1))
    assert p_cert["pisot"]
    assert p_cert["perron_non_pisot"] is False
    labels = cubic_roots((1, -2, -1, -3))
    assert len(labels) == 3

