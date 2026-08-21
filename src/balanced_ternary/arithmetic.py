"""Integer helpers used by analysis (not a primality library).

Trial division is sufficient for Milestone A inspection of individual
values. It is not a replacement for modern primality tests.
"""

from __future__ import annotations


def is_prime(n: int) -> bool:
    """True iff ``n`` is a positive prime. Negatives, 0, and 1 are not prime."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def factorize(n: int) -> list[tuple[int, int]]:
    """Prime factorization of ``|n|`` as ``[(p, exponent), ...]`` in increasing ``p``.

    Returns ``[]`` for ``n = 0, ±1``. Sign is not included; callers print it.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0 or abs(n) == 1:
        return []

    m = abs(n)
    factors: list[tuple[int, int]] = []

    def consume(p: int) -> None:
        nonlocal m
        exp = 0
        while m % p == 0:
            m //= p
            exp += 1
        if exp:
            factors.append((p, exp))

    consume(2)
    consume(3)
    p = 5
    while p * p <= m:
        consume(p)
        consume(p + 2)
        p += 6
    if m > 1:
        factors.append((m, 1))
    return factors


def format_factorization(n: int) -> str:
    """Human-readable factorization, including sign. ``0`` and ``±1`` are special."""
    if n == 0:
        return "0"
    if abs(n) == 1:
        return str(n)

    parts: list[str] = []
    if n < 0:
        parts.append("-1")
    for p, e in factorize(n):
        parts.append(str(p) if e == 1 else f"{p}^{e}")
    return " * ".join(parts)
