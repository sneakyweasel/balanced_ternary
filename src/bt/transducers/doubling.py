"""LSD-first sequential doubling: ``n -> 2n``.

State is a carry in ``{-1, 0, +1}``. On input digit ``a``:

    s = 2a + carry
    s = d + 3 * next_carry    with d in {-1, 0, +1}

**PROVED:** this is exact integer doubling written in balanced ternary,
because the rewrite ``s = d + 3c'`` preserves value and the carry alphabet
is closed on ``s in {-3, ..., 3}``.
"""

from __future__ import annotations

from bt.representation import (
    BalancedTernary,
    WordLike,
    digits,
    from_digits_lsd,
    normalize,
)


def doubling_step(carry: int, digit: int) -> tuple[int, int]:
    """Return ``(next_carry, output_digit)``."""
    s = 2 * digit + carry
    if s >= 2:
        return 1, s - 3
    if s <= -2:
        return -1, s + 3
    return 0, s


class DoublingTransducer:
    """3-state LSD Mealy machine for multiplication by 2."""

    alphabet: tuple[int, int, int] = (-1, 0, 1)

    def step(self, carry: int, digit: int) -> tuple[int, int]:
        if digit not in self.alphabet:
            raise ValueError(f"digit must be in {{-1,0,+1}}, got {digit!r}")
        if carry not in self.alphabet:
            raise ValueError(f"carry must be in {{-1,0,+1}}, got {carry!r}")
        return doubling_step(carry, digit)

    def apply(self, word: WordLike) -> BalancedTernary:
        lsd = digits(normalize(word))
        carry = 0
        out: list[int] = []
        for a in lsd:
            carry, d = doubling_step(carry, a)
            out.append(d)
        if carry:
            out.append(carry)
        return from_digits_lsd(out)


def apply_double(word: WordLike) -> BalancedTernary:
    return DoublingTransducer().apply(word)
