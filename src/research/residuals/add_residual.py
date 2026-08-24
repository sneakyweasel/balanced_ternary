"""Phase-0 residual of a sum: the carry is a constant polynomial.

At each trit ``a``,

    𝔇_a(f+g) - 𝔇_a f - 𝔇_a g = (ρ_a(f) + ρ_a(g) - ρ_a(f+g)) / 3 ∈ {-1,0,+1}.

Iterating along a word, the difference of residuals stays degree ``0``.
"""

from __future__ import annotations

from bt.calculus.residual import residual_along
from bt.calculus.section import IntPoly


def step_carry(f: IntPoly, g: IntPoly, a: int) -> int:
    """Constant ``(ρ(f)+ρ(g)-ρ(f+g))/3`` at input trit ``a``."""

    total = f.rho(a) + g.rho(a) - f.add(g).rho(a)
    if total % 3:
        raise RuntimeError("carry is not divisible by 3")
    return total // 3


def residual_carry_constant(f: IntPoly, g: IntPoly, word: tuple[int, ...]) -> IntPoly:
    """``residual(f+g) - residual(f) - residual(g)``, a constant."""

    return residual_along(f.add(g), word).sub(residual_along(f, word)).sub(
        residual_along(g, word)
    )


def sum_residual_identity(f: IntPoly, g: IntPoly, word: tuple[int, ...]) -> bool:
    carry = residual_carry_constant(f, g, word)
    if carry.degree > 0:
        return False
    return residual_along(f.add(g), word) == residual_along(f, word).add(
        residual_along(g, word)
    ).add(carry)
