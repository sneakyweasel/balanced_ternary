"""Exact reverse residual map for the non-Pisot order-3 system.

Forward: ``t = A s - (0, 0, w)`` with

    A = [[0, 0, 3],
         [1, 0, 1],
         [0, 1, 2]].

``det A = 3``. Over ``Q``:

    A^{-1} = [[-1/3, 1, 0],
              [-2/3, 0, 1],
              [ 1/3, 0, 0]].

Integer preimages exist iff ``t_1`` is divisible by 3, in which case

    s_3 = t_1 / 3,  s_1 = t_2 - s_3,  s_2 = t_3 + w - 2 s_3.
"""

from __future__ import annotations

from fractions import Fraction

from research.ostrowski.spectral_residual import residual_matrix, transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3

State3 = tuple[int, int, int]
Frac3 = tuple[tuple[Fraction, Fraction, Fraction], ...]


def _f(x: int | Fraction) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def matrix_over_q(rows: tuple[tuple[int, ...], ...]) -> Frac3:
    return tuple(tuple(_f(v) for v in row) for row in rows)


def mat_mul(a: Frac3, b: Frac3) -> Frac3:
    n = len(a)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(sum(a[i][k] * b[k][j] for k in range(n)))
        out.append(tuple(row))
    return tuple(out)


def mat_vec(a: Frac3, v: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a)))


def identity3() -> Frac3:
    z, o = Fraction(0), Fraction(1)
    return ((o, z, z), (z, o, z), (z, z, o))


def mat_transpose(a: Frac3) -> Frac3:
    n = len(a)
    return tuple(tuple(a[j][i] for j in range(n)) for i in range(n))


def np_forward_matrix() -> Frac3:
    sys = nonpisot_order3()
    return matrix_over_q(residual_matrix(sys))


def np_inverse_matrix() -> Frac3:
    """Exact ``A^{-1}`` for ``Γ_NP``. Not a floating inverse."""
    t = Fraction(1, 3)
    return (
        (-t, Fraction(1), Fraction(0)),
        (-Fraction(2, 3), Fraction(0), Fraction(1)),
        (t, Fraction(0), Fraction(0)),
    )


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
    t1, t2, t3 = t
    if t1 % 3 != 0:
        return None
    s3 = t1 // 3
    s1 = t2 - s3
    s2 = t3 + w - 2 * s3
    return (s1, s2, s3)


def reverse_matches_forward(
    system: OstrowskiSystem,
    state: State3,
    w: int,
) -> bool:
    t = transition_affine(system, state, w)
    pred = integer_preimage(t, w)
    qpred = reverse_affine_q(t, w)
    return pred == state and all(qpred[i] == Fraction(state[i]) for i in range(3))
