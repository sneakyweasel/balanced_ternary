"""Exact balanced-ternary word arithmetic and integer helpers.

Word addition uses the carry rewrite in :mod:`bt.normalization`.
Trial-division helpers are for inspection of individual values, not a
primality library.
"""

from __future__ import annotations

from bt.normalization import rewrite_sum
from bt.representation import (
    BalancedTernary,
    WordLike,
    digits,
    encode,
    from_digits_lsd,
    normalize,
)


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


def multiply_by_three(word: WordLike) -> BalancedTernary:
    """``3n`` by appending a trailing ``0`` (LSD coefficient of ``3^0`` is 0).

    If ``n = sum_i a_i 3^i`` then ``3n = sum_i a_i 3^{i+1}``.
    """
    lsd = digits(normalize(word))
    if lsd == (0,):
        return BalancedTernary((0,))
    return from_digits_lsd((0,) + lsd)


def add(left: WordLike, right: WordLike) -> BalancedTernary:
    """Exact balanced ternary addition via LSD-first carry."""
    a = digits(normalize(left))
    b = digits(normalize(right))
    n = max(len(a), len(b))
    out: list[int] = []
    carry = 0
    for i in range(n):
        da = a[i] if i < len(a) else 0
        db = b[i] if i < len(b) else 0
        digit, carry = rewrite_sum(da + db + carry)
        out.append(digit)
    if carry:
        out.append(carry)
    return from_digits_lsd(out)


def subtract(left: WordLike, right: WordLike) -> BalancedTernary:
    return add(left, negate(right))


def negate(word: WordLike) -> BalancedTernary:
    return -normalize(word)


def add_one(word: WordLike) -> BalancedTernary:
    """Add ``+1`` in balanced ternary."""
    return add(word, encode(1))


def three_n_plus_one_word(word: WordLike) -> BalancedTernary:
    """``3n+1`` as shift-then-add-one on the balanced ternary word of ``n``."""
    return add_one(multiply_by_three(word))


def lsd_add_one_case(word: WordLike) -> str:
    """Local LSD case of adding ``+1``, before carry propagation.

    Status of the three local rewrites (EXACT — HUMAN PROOF, from the digit alphabet):

    * ``...0`` + 1 = ``...+`` with no carry
    * ``...+`` + 1 = ``...-`` with carry ``+1``
    * ``...-`` + 1 = ``...0`` with no carry

    Carry ``+1`` may continue into more significant digits; the full word
    is given by :func:`add_one`.
    """
    a0 = digits(normalize(word))[0]
    if a0 == 0:
        return "trailing_zero"
    if a0 == 1:
        return "trailing_plus"
    return "trailing_minus"


def multiply_by_2(word: WordLike) -> BalancedTernary:
    from bt.transducers.doubling import apply_double

    return apply_double(word)


def divide_by_2_on_domain(word: WordLike) -> BalancedTernary:
    from bt.transducers.divide_by_two import apply_even

    return apply_even(word)


def divide_by_3_on_domain(word: WordLike) -> BalancedTernary:
    """Divide by 3 when the LSD is 0 (exact inverse of :func:`multiply_by_three`)."""
    from bt.operators import drop_lsd_word, lsd_digit
    from bt.representation import decode

    n = decode(word)
    if n % 3 != 0:
        raise ValueError(f"{n} is not divisible by 3")
    if lsd_digit(n) != 0:
        raise ValueError(f"LSD of {n} is not 0")
    return drop_lsd_word(word)
