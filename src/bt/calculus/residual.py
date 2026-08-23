"""Residual Mealy machine of a polynomial section calculus.

For a state ``f ∈ Z[x]`` and input trit ``a ∈ {-1,0,+1}``:

    ρ_a(f) = [f(a)]_3
    δ(f, a) = 𝔇_a f

    f  --[a / ρ_a(f)]-->  𝔇_a f

The emitted word on a trit path ``w`` is the first ``|w|`` balanced
output trits of ``f`` along that section path. Prefix locality (Milestone
15) says those trits do not depend on a residual argument after ``w``.
"""

from __future__ import annotations

from functools import lru_cache

from bt.calculus.jets import function_jet
from bt.calculus.section import IntPoly

TRITS: tuple[int, int, int] = (-1, 0, 1)


def _require_horizon(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("horizon must be a nonnegative int")
    return k


@lru_cache(maxsize=None)
def _delta_coeffs(coeffs: tuple[int, ...], a: int) -> tuple[int, ...]:
    return IntPoly(coeffs).section_deriv(a).coeffs


@lru_cache(maxsize=None)
def _rho_coeffs(coeffs: tuple[int, ...], a: int) -> int:
    return IntPoly(coeffs).rho(a)


def rho(f: IntPoly, a: int) -> int:
    if a not in TRITS:
        raise ValueError(f"input must be a trit, got {a}")
    return _rho_coeffs(f.coeffs, a)


def delta(f: IntPoly, a: int) -> IntPoly:
    if a not in TRITS:
        raise ValueError(f"input must be a trit, got {a}")
    return IntPoly(_delta_coeffs(f.coeffs, a))


def output_along(f: IntPoly, word: tuple[int, ...]) -> tuple[int, ...]:
    """Output trits of the residual machine on ``word``."""
    return function_jet(f, word).output_trits


def residual_along(f: IntPoly, word: tuple[int, ...]) -> IntPoly:
    cur = f
    for a in word:
        cur = delta(cur, a)
    return cur


def pack_trits(bits: tuple[int, ...], acc: int = 0) -> int:
    for b in reversed(bits):
        acc = b + 3 * acc
    return acc


def section_value(word: tuple[int, ...], residual_arg: int = 0) -> int:
    """Integer whose length-``|word|`` jet is ``word`` and residual is ``residual_arg``."""
    return pack_trits(word, residual_arg)
