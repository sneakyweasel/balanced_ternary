"""Residual matrix of a constant order-3 Gamma-system.

The unread-tail transition of residual.py, for constant
``(d_1, d_2, d_3)``, is the affine map

    s' = A s - (0, 0, w)

with

    A = [[0, 0, d_3],
         [1, 0, d_2],
         [0, 1, d_1]].

``A`` has the same characteristic polynomial as the place-value
recurrence. Eigenfloats are classification only.
"""

from __future__ import annotations

from research.ostrowski.residual import next_state
from research.ostrowski.spectral import constant_digits, cubic_roots, spectral_data
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs
from research_engine.algebra.lattices import characteristic_polynomial as engine_charpoly
from research_engine.core.affine_system import affine_step, apply_matrix as engine_apply_matrix

State3 = tuple[int, int, int]


def residual_matrix(system: OstrowskiSystem) -> tuple[tuple[int, int, int], ...]:
    """Integer matrix ``A`` such that ``s' = A s - e_3 w``."""
    digits = constant_digits(system)
    if digits is None:
        raise ValueError("residual matrix is defined for constant order-3 systems")
    d1, d2, d3 = digits
    return (
        (0, 0, d3),
        (1, 0, d2),
        (0, 1, d1),
    )


def apply_matrix(matrix: tuple[tuple[int, int, int], ...], state: State3) -> State3:
    out = engine_apply_matrix(matrix, state)
    return (out[0], out[1], out[2])


def transition_affine(system: OstrowskiSystem, state: State3, w: int) -> State3:
    """Exact ``T_Γ(s, w)``. Independent of remaining length when ``d`` is constant."""
    out = affine_step(residual_matrix(system), state, (0, 0, -w))
    return (out[0], out[1], out[2])


def transition_matches_next_state(system: OstrowskiSystem, state: State3, w: int, i: int = 8) -> bool:
    return transition_affine(system, state, w) == next_state(system, state, w, i)


def charpoly_of_matrix(matrix: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int, int]:
    """Characteristic polynomial ``det(xI-A)`` as ``(1, a, b, c)`` for ``x^3+ax^2+bx+c``."""
    poly = engine_charpoly(matrix)
    if len(poly) != 4:
        raise ValueError("charpoly_of_matrix expects a 3x3 matrix")
    return (poly[0], poly[1], poly[2], poly[3])


def spectral_residual_report(system: OstrowskiSystem) -> dict[str, object]:
    data = spectral_data(system)
    matrix = residual_matrix(system)
    poly = characteristic_poly_coeffs(system)
    return {
        **data,
        "residual_matrix": matrix,
        "matrix_characteristic_polynomial": charpoly_of_matrix(matrix),
        "matches_place_value_polynomial": charpoly_of_matrix(matrix) == poly,
        "eigenvalues": cubic_roots(poly) if poly is not None else (),
    }
