"""Digit integrals ``I_a`` and projections ``P_a = I_a ∘ D``.

``I_a(x) = a + 3x`` for ``a in {-1, 0, +1}``. ``I_0 = S``.
Integer maps wrap :mod:`bt.operators`; they do not re-encode words.
"""

from __future__ import annotations

from bt.calculus.derivative import D, S, lsd
from bt.calculus.trit import Trit, as_trit
from bt.operators import lsd_digit


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def I(a: Trit | int, x: int) -> int:
    """``I_a(x) = a + 3x``."""
    return int(as_trit(int(a))) + 3 * _require_int(x, "x")


def I_minus(x: int) -> int:
    return I(Trit.MINUS, x)


def I_zero(x: int) -> int:
    """``I_0 = S``."""
    return S(x)


def I_plus(x: int) -> int:
    return I(Trit.PLUS, x)


def P(a: Trit | int, n: int) -> int:
    """Projection ``P_a(n) = I_a(D(n)) = n - lsd(n) + a``.

    ``P_a(n) = n`` if and only if ``lsd(n) = a``. The family
    ``{P_{-1}, P_0, P_{+1}}`` is a left-zero band: ``P_a ∘ P_b = P_a``.
    """
    return I(a, D(n))


def P_minus(n: int) -> int:
    return P(Trit.MINUS, n)


def P_zero(n: int) -> int:
    return P(Trit.ZERO, n)


def P_plus(n: int) -> int:
    return P(Trit.PLUS, n)


def section_holds(a: Trit | int, n: int) -> bool:
    """``I_a(D(n)) = n`` iff ``lsd(n) = a``."""
    n = _require_int(n)
    return lsd_digit(n) == int(as_trit(int(a)))
