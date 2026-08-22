"""Accelerated Collatz map on positive odd integers.

Two maps appear in the literature. This module uses the odd-only map.

1. Standard Collatz map (Hailstone / ``3n+1`` map) on positive integers::

       C(n) = n/2          if n is even
       C(n) = 3n+1         if n is odd

2. Accelerated odd-only map (Syracuse function) on positive odd integers::

       T(n) = (3n+1) / 2^{v2(3n+1)}

For every positive odd ``n``, ``3n+1`` is even, so ``v2(3n+1) >= 1`` and
``T(n)`` is a positive odd integer. All arithmetic is exact Python ``int``.

``T`` is the primary map for this research module. The standard map is
provided only to make the distinction executable.
"""

from __future__ import annotations

from research.collatz.valuation import v2


def require_positive_odd(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n <= 0:
        raise ValueError(f"{name} must be a positive integer, got {n}")
    if n % 2 == 0:
        raise ValueError(f"{name} must be odd, got {n}")
    return n


def require_positive_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n <= 0:
        raise ValueError(f"{name} must be a positive integer, got {n}")
    return n


def standard_collatz_step(n: int) -> int:
    """One step of the standard map ``C`` on a positive integer."""
    n = require_positive_int(n)
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def three_n_plus_one(n: int) -> int:
    """``3n+1`` for a positive odd integer (always even)."""
    n = require_positive_odd(n)
    return 3 * n + 1


def collatz_step(n: int) -> int:
    """One step of the accelerated map ``T``.

    ``T(n) = (3n+1) >> v2(3n+1)``. The right shift is exact integer division
    by ``2^{v2(3n+1)}``.
    """
    n = require_positive_odd(n)
    y = 3 * n + 1
    k = v2(y)
    if k is None:
        raise ArithmeticError("3n+1 was 0, which cannot occur for odd n")
    return y >> k


def collatz_valuation(n: int) -> int:
    """``v2(3n+1)`` for positive odd ``n``. Always ``>= 1``."""
    n = require_positive_odd(n)
    k = v2(3 * n + 1)
    if k is None:
        raise ArithmeticError("3n+1 was 0, which cannot occur for odd n")
    return k
