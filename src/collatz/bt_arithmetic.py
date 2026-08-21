"""Exact balanced ternary addition used to analyse ``3n+1``.

Multiplication by 3 is a digit shift. Adding ``+1`` is *not* the same as
binary or unbalanced-ternary carry; digits live in ``{-1, 0, +1}`` and a
local sum of ``±2`` or ``±3`` is rewritten using ``2 = 3 - 1`` and
``-2 = -3 + 1``.

These operations are verified against integer arithmetic. They are helpers
for the Collatz decomposition

    n  ->  3n  (shift)  ->  3n+1  (add +1)  ->  (3n+1)/2^{v2(3n+1)}.
"""

from __future__ import annotations

from balanced_ternary.representation import (
    BalancedTernary,
    WordLike,
    digits,
    encode,
    from_digits_lsd,
    normalize,
)


def multiply_by_three(word: WordLike) -> BalancedTernary:
    """``3n`` by appending a trailing ``0`` (LSD coefficient of ``3^0`` is 0).

    If ``n = sum_i a_i 3^i`` then ``3n = sum_i a_i 3^{i+1}``.
    """
    lsd = digits(normalize(word))
    if lsd == (0,):
        return BalancedTernary((0,))
    return from_digits_lsd((0,) + lsd)


def _rewrite_sum(s: int) -> tuple[int, int]:
    """Rewrite ``s in {-3,...,3}`` as ``digit + 3*carry`` with ``digit in {-1,0,1}``."""
    if s >= 2:
        return s - 3, 1
    if s <= -2:
        return s + 3, -1
    return s, 0


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
        digit, carry = _rewrite_sum(da + db + carry)
        out.append(digit)
    if carry:
        out.append(carry)
    return from_digits_lsd(out)


def add_one(word: WordLike) -> BalancedTernary:
    """Add ``+1`` in balanced ternary."""
    return add(word, encode(1))


def three_n_plus_one_word(word: WordLike) -> BalancedTernary:
    """``3n+1`` as shift-then-add-one on the balanced ternary word of ``n``."""
    return add_one(multiply_by_three(word))


def lsd_add_one_case(word: WordLike) -> str:
    """Local LSD case of adding ``+1``, before carry propagation.

    Status of the three local rewrites (PROVED, from the digit alphabet):

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
