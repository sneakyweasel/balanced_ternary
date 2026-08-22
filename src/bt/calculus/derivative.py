"""Digit derivative ``D`` as a calculus operator.

Wraps :func:`bt.operators.digit_derivative` and :func:`bt.operators.lsd_digit`.
Does not reimplement balanced-ternary encoding.
"""

from __future__ import annotations

from bt.calculus.trit import Trit, as_trit
from bt.operators import digit_derivative, lsd_digit, multiply_by_3


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def lsd(n: int) -> Trit:
    """Least-significant balanced trit of ``n``."""
    return as_trit(lsd_digit(_require_int(n)))


def D(n: int) -> int:
    """``D(n) = (n - lsd(n)) / 3``. Not floor division by 3."""
    return digit_derivative(_require_int(n))


def D_k(n: int, k: int) -> int:
    """``D`` iterated ``k`` times. Deletes the ``k`` least-significant trits."""
    n = _require_int(n)
    k = _require_int(k, "k")
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k}")
    for _ in range(k):
        n = digit_derivative(n)
    return n


def digit_at(n: int, k: int) -> Trit:
    """The coefficient ``a_k`` of ``n``, recovered as ``lsd(D^k(n))``."""
    return lsd(D_k(n, k))


def reconstruct(n: int) -> int:
    """The exact identity ``n = lsd(n) + 3 D(n)``."""
    n = _require_int(n)
    return int(lsd(n)) + 3 * D(n)


def S(n: int) -> int:
    """Ternary shift ``S(n) = 3n = I_0(n)``."""
    return multiply_by_3(_require_int(n))
