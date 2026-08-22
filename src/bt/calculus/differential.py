"""Exact sum and product rules for the digit derivative.

The sum correction reuses :func:`bt.normalization.rewrite_sum`. The product
rule is the twisted Leibniz identity

    D(xy) = lsd(x) D(y) + lsd(y) D(x) + 3 D(x) D(y)

with ``lsd(xy) = lsd(x) lsd(y)``. This is not the ordinary product rule.
"""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.trit import Trit, as_trit
from bt.normalization import rewrite_sum
from bt.operators import lsd_digit


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def add_correction(x: int, y: int) -> tuple[Trit, int]:
    """Balanced digit and carry of ``lsd(x) + lsd(y)``.

    This is the standard balanced-ternary addition table, written as a
    D-law correction: ``D(x+y) = D(x)+D(y)+carry``.
    """
    a = lsd_digit(_require_int(x, "x"))
    b = lsd_digit(_require_int(y, "y"))
    digit, carry = rewrite_sum(a + b)
    return as_trit(digit), carry


def D_of_sum(x: int, y: int) -> int:
    """Exact ``D(x+y)`` via the LSD carry correction."""
    _digit, carry = add_correction(x, y)
    return D(x) + D(y) + carry


def lsd_of_sum(x: int, y: int) -> Trit:
    digit, _carry = add_correction(x, y)
    return digit


def mul_correction(x: int, y: int) -> tuple[Trit, int]:
    """``lsd(xy)`` and the exact extra term in ``D(xy)``.

    The extra term beyond ``lsd(x) D(y) + lsd(y) D(x)`` is ``3 D(x) D(y)``.
    """
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    a = lsd_digit(x)
    b = lsd_digit(y)
    return as_trit(a * b), 3 * D(x) * D(y)


def D_of_product(x: int, y: int) -> int:
    """Twisted Leibniz rule for ``D(xy)``."""
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    a = lsd_digit(x)
    b = lsd_digit(y)
    return a * D(y) + b * D(x) + 3 * D(x) * D(y)


def lsd_of_product(x: int, y: int) -> Trit:
    return as_trit(lsd_digit(_require_int(x, "x")) * lsd_digit(_require_int(y, "y")))


def product_expansion(x: int, y: int) -> int:
    """``xy = ab + 3(a D(y) + b D(x) + 3 D(x) D(y))``."""
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    a = lsd_digit(x)
    b = lsd_digit(y)
    return a * b + 3 * (a * D(y) + b * D(x) + 3 * D(x) * D(y))
