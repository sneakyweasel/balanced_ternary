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
    return tuple(
        matrix[i][0] * state[0] + matrix[i][1] * state[1] + matrix[i][2] * state[2]
        for i in range(3)
    )


def transition_affine(system: OstrowskiSystem, state: State3, w: int) -> State3:
    """Exact ``T_Γ(s, w)``. Independent of remaining length when ``d`` is constant."""
    s1, s2, s3 = apply_matrix(residual_matrix(system), state)
    return (s1, s2, s3 - w)


def transition_matches_next_state(system: OstrowskiSystem, state: State3, w: int, i: int = 8) -> bool:
    return transition_affine(system, state, w) == next_state(system, state, w, i)


def charpoly_of_matrix(matrix: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int, int]:
    """Characteristic polynomial ``det(xI-A)`` as ``(1, a, b, c)`` for ``x^3+ax^2+bx+c``."""
    a00, a01, a02 = matrix[0]
    a10, a11, a12 = matrix[1]
    a20, a21, a22 = matrix[2]
    # For this companion orientation the polynomial is x^3 - d1 x^2 - d2 x - d3.
    # Compute det(xI-A) by the explicit 3x3 formula in the integer ring,
    # evaluating coefficients via traces of exterior powers.
    tr = a00 + a11 + a22
    # sum of principal 2x2 minors
    m2 = (
        (a00 * a11 - a01 * a10)
        + (a00 * a22 - a02 * a20)
        + (a11 * a22 - a12 * a21)
    )
    det = (
        a00 * (a11 * a22 - a12 * a21)
        - a01 * (a10 * a22 - a12 * a20)
        + a02 * (a10 * a21 - a11 * a20)
    )
    # det(xI-A) = x^3 - tr x^2 + m2 x - det
    return (1, -tr, m2, -det)


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
