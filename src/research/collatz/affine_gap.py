"""Integer affine gap of a fixed Collatz start.

    G_m = n (2^{K_m} - 3^m) - C_m = 2^{K_m} (n - T^m(n)).

The second form is **EXACT — HUMAN PROOF** from the affine identity
``2^K x = 3^m n + C``. Consequently:

- ``G_m > 0`` iff ``T^m(n) < n``
- ``G_m = 0`` iff ``T^m(n) = n``
- ``G_m < 0`` iff ``T^m(n) > n``

This is the orbit-versus-start comparison, not positivity ``T^m(n) >= 1``.

The exact recurrence along a valuation ``k`` is

    G_{m+1} = 3 G_m + 2^{K_m} ( n (2^k - 3) - 1 ).

``G_0 = 0``. Each ``k = 1`` step contributes a strictly negative addend
``2^K (-n-1)``; each ``k >= 2`` contributes a nonnegative addend.
"""

from __future__ import annotations


def affine_gap(n: int, two_power: int, three_power: int, C: int) -> int:
    """``G = n(2^K - 3^m) - C``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (n, two_power, three_power, C)):
        raise TypeError("affine-gap arguments must be int")
    return n * (two_power - three_power) - C


def affine_gap_from_orbit(n: int, x: int, two_power: int) -> int:
    """``G = 2^K (n - x)``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (n, x, two_power)):
        raise TypeError("orbit-gap arguments must be int")
    return two_power * (n - x)


def next_affine_gap(G: int, n: int, two_power: int, k: int) -> int:
    """``G' = 3G + 2^K (n(2^k - 3) - 1)``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (G, n, two_power, k)):
        raise TypeError("gap-recurrence arguments must be int")
    if k < 1:
        raise ValueError("k must be an integer >= 1")
    return 3 * G + two_power * (n * ((1 << k) - 3) - 1)


def step_addend(n: int, two_power: int, k: int) -> int:
    """The explicit addend ``2^K (n(2^k-3)-1)``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (n, two_power, k)):
        raise TypeError("step-addend arguments must be int")
    if k < 1:
        raise ValueError("k must be an integer >= 1")
    return two_power * (n * ((1 << k) - 3) - 1)


def addend_sign_law(n: int, k: int) -> int:
    """Sign of ``n(2^k-3)-1``: negative for ``k=1``, nonnegative for ``k>=2`` when ``n>=1``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (n, k)):
        raise TypeError("sign-law arguments must be int")
    if k < 1:
        raise ValueError("k must be an integer >= 1")
    if n < 1:
        raise ValueError("n must be a positive integer")
    if k == 1:
        return -1
    return 0 if n == 1 and k == 2 else 1
