"""Exact integer algebra: recurrences, lattices, linear forms."""

from research_engine.algebra.lattices import (
    adjugate,
    apply_matrix_q,
    characteristic_polynomial,
    identity_matrix_q,
    integer_affine_preimage,
    inverse_over_q,
    matrix_det,
    matrix_over_q,
    multiply_matrices_q,
    solve_over_q,
    transpose,
    vector_gcd,
)
from research_engine.algebra.linear_functionals import LinearFunctional, dot, left_multiply
from research_engine.algebra.recurrences import RecurrenceSpec
from research_engine.algebra.spectral import (
    cubic_roots,
    exact_pisot_cubic_certificate,
    polynomial_is_irreducible_cubic,
)

__all__ = [
    "LinearFunctional",
    "RecurrenceSpec",
    "cubic_roots",
    "exact_pisot_cubic_certificate",
    "adjugate",
    "apply_matrix_q",
    "characteristic_polynomial",
    "dot",
    "identity_matrix_q",
    "integer_affine_preimage",
    "inverse_over_q",
    "left_multiply",
    "matrix_det",
    "matrix_over_q",
    "multiply_matrices_q",
    "polynomial_is_irreducible_cubic",
    "solve_over_q",
    "transpose",
    "vector_gcd",
]
