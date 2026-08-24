"""Exact contraction certificate for ``A^{-1}`` of Γ_NP.

Spectral radius ``ρ(A^{-1})<1`` already follows from the integer cubic
certificate (conjugates of ``A`` lie outside the unit disk). That is
not an induced-norm bound.

This module supplies a rational SPD quadratic form ``Q`` such that
``Q - (A^{-1})^T Q A^{-1}`` is SPD by the Sylvester criterion over
``Q``. Then

    |A^{-1} x|_Q^2  ≤  (49/50) |x|_Q^2.

Floats were used only to guess ``Q``; the certificate does not use them.
"""

from __future__ import annotations

from fractions import Fraction

from research.ostrowski.reverse_map import (
    Frac3,
    mat_mul,
    mat_transpose,
    np_inverse_matrix,
)

# Integer SPD matrix guessed from the discrete Lyapunov equation, then
# verified exactly. Not unique.
Q_LYAPUNOV: Frac3 = (
    (Fraction(10), Fraction(-3), Fraction(-7)),
    (Fraction(-3), Fraction(11), Fraction(-3)),
    (Fraction(-7), Fraction(-3), Fraction(12)),
)

RHO_SQUARED: Fraction = Fraction(49, 50)
MU: Fraction = Fraction(1, 50)

# Crude exact overestimates used only to name a finite integer box
# containing C({0}). Not tight: the computed basin is much smaller.
RHO_UPPER: Fraction = Fraction(99, 100)  # (99/100)^2 = 9801/10000 > 49/50
INHOMOGENEOUS_Q_NORM_INT: int = 14  # 14^2 = 196 > 12 * 4^2 = 192
APRIORI_Q_NORM_BOUND: int = 1386  # 14 * 99, from 14 * RHO_UPPER / (1 - RHO_UPPER)
APRIORI_AXIS_BOUND: int = 1386  # Q - I is SPD, so |s|_Q^2 >= ||s||^2


def sylvester_minors(matrix: Frac3) -> tuple[Fraction, Fraction, Fraction]:
    """Leading principal minors of a 3x3 symmetric matrix."""
    a00, a01, a02 = matrix[0]
    a10, a11, a12 = matrix[1]
    a20, a21, a22 = matrix[2]
    m1 = a00
    m2 = a00 * a11 - a01 * a10
    det = (
        a00 * (a11 * a22 - a12 * a21)
        - a01 * (a10 * a22 - a12 * a20)
        + a02 * (a10 * a21 - a11 * a20)
    )
    return (m1, m2, det)


def is_spd(matrix: Frac3) -> bool:
    return all(m > 0 for m in sylvester_minors(matrix))


def mat_add(a: Frac3, b: Frac3, scale_b: Fraction = Fraction(1)) -> Frac3:
    return tuple(
        tuple(a[i][j] + scale_b * b[i][j] for j in range(3)) for i in range(3)
    )


def mat_scale(a: Frac3, c: Fraction) -> Frac3:
    return tuple(tuple(c * a[i][j] for j in range(3)) for i in range(3))


def pulled_back_q(inverse: Frac3 | None = None) -> Frac3:
    """``(A^{-1})^T Q A^{-1}``."""
    inv = inverse if inverse is not None else np_inverse_matrix()
    return mat_mul(mat_mul(mat_transpose(inv), Q_LYAPUNOV), inv)


def decrement_matrix() -> Frac3:
    """``Q - (A^{-1})^T Q A^{-1}``."""
    return mat_add(Q_LYAPUNOV, pulled_back_q(), Fraction(-1))


def q_norm_squared(state: tuple[int, int, int]) -> int:
    """Integer value of ``s^T Q s`` for the integer Lyapunov matrix."""
    x, y, z = state
    return 10 * x * x + 11 * y * y + 12 * z * z - 6 * x * y - 14 * x * z - 6 * y * z


def identity3() -> Frac3:
    z, o = Fraction(0), Fraction(1)
    return ((o, z, z), (z, o, z), (z, z, o))


def q_minus_i_is_spd() -> bool:
    """``Q - I`` SPD implies ``|s|_Q^2 >= ||s||^2``, hence axis bounds from ``|s|_Q``."""
    return is_spd(mat_add(Q_LYAPUNOV, identity3(), Fraction(-1)))


def a_priori_preimage_bound() -> dict[str, object]:
    """Integer box containing every backward orbit of a seed at the origin.

    Reverse: ``s = A^{-1}(t + (0,0,w))``, so
    ``|s|_Q <= ρ(|t|_Q + |(0,0,w)|_Q)``. With ``t = 0`` initially and
    ``|w| <= 4``,

        ``|(0,0,w)|_Q^2 = 12 w^2 <= 192 < 196 = 14^2``,
        ``ρ^2 = 49/50 < (99/100)^2``,
        hence ``|s|_Q < 14 · (99/100) / (1/100) = 1386``.

    Because ``Q - I`` is SPD, ``|s_i| <= |s|_Q < 1386``. This box is
    too large to enumerate (plan: possibly crude). Finiteness of
    ``C({0})`` follows; the exact set is the backward BFS, not the box.
    The bound does **not** apply to forward images of ``(0,0,0)``.
    """
    rho_upper_ok = RHO_UPPER * RHO_UPPER > RHO_SQUARED
    inhom_ok = INHOMOGENEOUS_Q_NORM_INT * INHOMOGENEOUS_Q_NORM_INT > 12 * 4 * 4
    bound = INHOMOGENEOUS_Q_NORM_INT * int(RHO_UPPER.numerator)
    # 1 - RHO_UPPER = 1/100, so C/(1-ρ) < 14 * 99.
    return {
        "rho_upper": RHO_UPPER,
        "rho_upper_squared_exceeds_rho_squared": rho_upper_ok,
        "inhomogeneous_q_norm_integer": INHOMOGENEOUS_Q_NORM_INT,
        "inhomogeneous_square_strict": inhom_ok,
        "q_minus_i_spd": q_minus_i_is_spd(),
        "apriori_q_norm_bound": APRIORI_Q_NORM_BOUND,
        "apriori_axis_bound": APRIORI_AXIS_BOUND,
        "bound_matches_arithmetic": bound == APRIORI_Q_NORM_BOUND,
        "proved": rho_upper_ok and inhom_ok and q_minus_i_is_spd() and bound == APRIORI_Q_NORM_BOUND,
        "enumerating_the_box_is_not_the_proof": True,
        "applies_to_forward_images_of_origin": False,
    }


def contraction_certificate() -> dict[str, object]:
    """Exact SPD certificate. ``rho_squared = 49/50`` is a proven ratio.

    Distinguishes: spectral radius (already known from the cubic) versus
    this induced ``Q``-norm bound. Eigenvalue floats are not used.
    """
    iq = pulled_back_q()
    decrement = decrement_matrix()
    mu_gap = mat_add(decrement, mat_scale(Q_LYAPUNOV, MU), Fraction(-1))
    rho_gap = mat_add(mat_scale(Q_LYAPUNOV, RHO_SQUARED), iq, Fraction(-1))
    # rho_gap = (49/50)Q - IQ = (49/50)Q - (Q - decrement) = decrement - (1/50)Q
    # which is mu_gap. Record both.
    return {
        "Q": Q_LYAPUNOV,
        "Q_spd": is_spd(Q_LYAPUNOV),
        "Q_minors": sylvester_minors(Q_LYAPUNOV),
        "decrement_spd": is_spd(decrement),
        "decrement_minors": sylvester_minors(decrement),
        "mu": MU,
        "mu_gap_spd": is_spd(mu_gap),
        "rho_squared": RHO_SQUARED,
        "rho_gap_spd": is_spd(rho_gap),
        "spectral_radius_less_than_one": True,
        "induced_q_norm_ratio_squared": RHO_SQUARED,
        "proved": (
            is_spd(Q_LYAPUNOV)
            and is_spd(decrement)
            and is_spd(mu_gap)
            and is_spd(rho_gap)
        ),
    }
