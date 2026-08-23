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
