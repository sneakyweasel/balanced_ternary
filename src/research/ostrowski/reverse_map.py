"""Exact reverse residual map for the non-Pisot order-3 system.

Forward: ``t = A s - (0, 0, w)`` with companion ``A`` of ``Γ_NP``.
Integer preimages are lattice points of ``A s + (0,0,-w) = t``.
"""

from __future__ import annotations

from fractions import Fraction

from research.ostrowski.spectral_residual import residual_matrix, transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3
from research_engine.algebra.lattices import (
    apply_matrix_q,
    identity_matrix_q,
    integer_affine_preimage,
    inverse_over_q,
    matrix_over_q as engine_matrix_over_q,
    multiply_matrices_q,
)

State3 = tuple[int, int, int]
Frac3 = tuple[tuple[Fraction, Fraction, Fraction], ...]


def _as_frac3(matrix: tuple[tuple[Fraction, ...], ...]) -> Frac3:
    return tuple(tuple(row) for row in matrix)  # type: ignore[return-value]


def matrix_over_q(rows: tuple[tuple[int, ...], ...]) -> Frac3:
    return _as_frac3(engine_matrix_over_q(rows))


def mat_mul(a: Frac3, b: Frac3) -> Frac3:
    return _as_frac3(multiply_matrices_q(a, b))


def mat_vec(a: Frac3, v: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return apply_matrix_q(a, v)


def identity3() -> Frac3:
    return _as_frac3(identity_matrix_q(3))


def mat_transpose(a: Frac3) -> Frac3:
    n = len(a)
    return tuple(tuple(a[j][i] for j in range(n)) for i in range(n))


def np_forward_matrix() -> Frac3:
    sys = nonpisot_order3()
    return matrix_over_q(residual_matrix(sys))


def np_inverse_matrix() -> Frac3:
    """Exact ``A^{-1}`` for ``Γ_NP``. Not a floating inverse."""
    sys = nonpisot_order3()
    return _as_frac3(inverse_over_q(residual_matrix(sys)))


def inverse_times_forward_is_identity() -> bool:
    a = np_forward_matrix()
    inv = np_inverse_matrix()
    return mat_mul(inv, a) == identity3() and mat_mul(a, inv) == identity3()


def reverse_affine_q(
    t: State3,
    w: int,
    inverse: Frac3 | None = None,
) -> tuple[Fraction, Fraction, Fraction]:
    """``s = A^{-1}(t + (0,0,w))`` over ``Q``."""
    inv = inverse if inverse is not None else np_inverse_matrix()
    rhs = (Fraction(t[0]), Fraction(t[1]), Fraction(t[2] + w))
    return mat_vec(inv, rhs)


def integer_preimage(t: State3, w: int) -> State3 | None:
    """Lattice preimage of ``t`` under ``T_w``, or ``None`` if not integral."""
    matrix = residual_matrix(nonpisot_order3())
    found = integer_affine_preimage(matrix, (0, 0, -w), t)
    if found is None:
        return None
    return (found[0], found[1], found[2])


def reverse_matches_forward(
    system: OstrowskiSystem,
    state: State3,
    w: int,
) -> bool:
    t = transition_affine(system, state, w)
    pred = integer_preimage(t, w)
    qpred = reverse_affine_q(t, w)
    return pred == state and all(qpred[i] == Fraction(state[i]) for i in range(3))
