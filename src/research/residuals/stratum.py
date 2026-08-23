"""Unified Newton-stratum face of the cubic residual fibre laws.

At horizon ``k`` and deficit ``r`` with ``r+1 ≤ k``, depth ``m = k-1-r``:

1. ``N2`` agrees iff ``p ≡ q (mod 3^r)``.
2. After ``N2``, ``N1`` agrees iff ``3^{k-1-r} | δ(p+q+3^m)``.
3. On ``p = 3^r u``, ``N0`` is the two-regime scaling, equivalently
   ``Q_{t,K,W}`` with ``(t,K,W) = (k-1-4r, k, k-1-2r)`` when
   ``k ≥ 4r+1``.
"""

from __future__ import annotations

from research.residuals.cubic_fibres import same_depth_n2
from research.residuals.cubic_n0_reduction import n0_regime, n0_scaled, reduced_depth
from research.residuals.cubic_n1_valuation import deficit_depth, n1_after_n2, n21_agree
from research.residuals.mismatched_cubic import q_int, q_params


def newton_stratum(k: int, r: int) -> dict[str, object]:
    """Named parameters and predicates matching ``NewtonStratum.lean``."""
    m = deficit_depth(k, r)
    regime = n0_regime(k, r)
    exhausted = k >= 4 * r + 1
    params = q_params(k, r) if exhausted else None
    return {
        "k": k,
        "r": r,
        "m": m,
        "n2_modulus": 3**r if r else 1,
        "n1_divisor_exp": k - 1 - r,
        "n0_regime": regime,
        "n0_reduced_depth": reduced_depth(k, r),
        "q_params": params,
        "exhausted": exhausted,
    }


def newton_stratum_n2(p: int, q: int, k: int, r: int) -> bool:
    """``newtonStratum_n2``: ``N2`` iff ``p ≡ q (mod 3^r)``."""
    m = deficit_depth(k, r)
    return same_depth_n2(m, p, q, k)


def newton_stratum_n1(p: int, q: int, k: int, r: int) -> bool:
    """``newtonStratum_n1``: ``N1`` after ``N2``."""
    return n1_after_n2(p, q, k, r)


def newton_stratum_n21(p: int, q: int, k: int, r: int) -> bool:
    return n21_agree(p, q, k, r)


def newton_stratum_n0(u: int, k: int, r: int) -> int:
    """``newtonStratum_n0``: exact ``D^m((3^r u)^3)``."""
    return n0_scaled(u, k, r)


def newton_stratum_q(u: int, k: int, r: int) -> int:
    """Mismatched quotient on the exhausted locus, or the unexhausted scale."""
    if k < 4 * r + 1:
        return n0_scaled(u, k, r)
    t, _K, _W = q_params(k, r)
    return q_int(t, u)


def newton_stratum_core_width(m: int, r: int, u: int) -> bool:
    """``newtonStratum_core_width``: ``u ∈ P_{m-r}`` (equivalently ``3^r u ∈ P_m``)."""
    from research.residuals.cubic_fibres import balanced_bound

    if r > m:
        return u == 0
    return abs(u) <= balanced_bound(m - r)


def newton_stratum_q_unit_family(t: int, K: int, a: int, b: int, c: int) -> bool:
    """``newtonStratum_q_unit_family``: unit ``G_a`` equality is ``b ≡ c (mod 3^{K-1})``."""
    from research.residuals.x3_state_complexity import unit_g_injective_mod

    return unit_g_injective_mod(t, K, a, b, c)


def newton_stratum_unit_square(W: int, u: int, v: int) -> bool:
    """``newtonStratum_unit_square``: units with the same square mod ``3^W`` are ``±``."""
    if u % 3 == 0 or v % 3 == 0:
        return False
    return (u * u - v * v) % (3**W if W else 1) == 0 and (u == v or u == -v)


def newton_stratum_n1_square(k: int, r: int, u: int, v: int) -> bool:
    """``newtonStratum_n1_square``: core ``N1`` agreement is square agreement."""
    from research.residuals.x3_state_complexity import A_coord, core_n1

    return (core_n1(u, k, r) == core_n1(v, k, r)) == (
        A_coord(u, k, r) == A_coord(v, k, r)
    )


def newton_stratum_n0_neg(k: int, m: int, u: int) -> bool:
    """``newtonStratum_n0_neg``: ``N0(u)=N0(-u)`` iff ``N0(u)=0``."""
    from bt.calculus.quadratic import iter_dz

    mod = 3**k if k else 1
    n0 = iter_dz(u**3, m) % mod
    n0n = iter_dz((-u) ** 3, m) % mod
    return (n0 == n0n) == (n0 == 0)
