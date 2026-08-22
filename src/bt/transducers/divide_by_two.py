"""LSD-first sequential division by 2 on even integers.

This is the sequential inverse of doubling on ``Z_3``. Because 2 is a unit
in the 3-adics, for every input digit ``d`` and carry ``c`` there is a unique
output digit ``a`` and next carry ``c'`` satisfying

    2a + c = d + 3 c'     a, c' in {-1, 0, +1}.

Solve ``a ≡ 2(d - c) (mod 3)`` lifted to ``{-1, 0, +1}``.

**PROVED** as a 3-adic sequential function. Restriction to even *integers*:
the output is a finite canonical word and the final carry is 0.

On odd integers the 3-adic expansion of ``n/2`` is infinite (example:
``1/2 = sum_i (-1) 3^i``). ``apply_even`` then raises ``LeftoverCarryError``
rather than inventing an integer.
"""

from __future__ import annotations

from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    digits,
    from_digits_lsd,
    normalize,
)


class LeftoverCarryError(ValueError):
    """Finite word is not the canonical encoding of an even integer."""


def _lift_mod3(x: int) -> int:
    """Lift ``x mod 3`` in ``{0,1,2}`` to ``{0,1,-1}``."""
    r = x % 3
    return -1 if r == 2 else r


def divide_by_two_step(carry: int, digit: int) -> tuple[int, int]:
    """Return ``(next_carry, output_digit)``."""
    a = _lift_mod3(2 * (digit - carry))
    num = 2 * a + carry - digit
    if num % 3 != 0:
        raise ArithmeticError(
            f"non-integral carry: carry={carry} digit={digit} a={a} num={num}"
        )
    nxt = num // 3
    if nxt not in (-1, 0, 1) or a not in (-1, 0, 1):
        raise ArithmeticError(
            f"carry escaped {{-1,0,1}}: carry={carry} digit={digit} a={a} nxt={nxt}"
        )
    return nxt, a


class DivideByTwoTransducer:
    """3-state LSD Mealy machine for division by 2 on even integers."""

    alphabet: tuple[int, int, int] = (-1, 0, 1)

    def step(self, carry: int, digit: int) -> tuple[int, int]:
        if digit not in self.alphabet:
            raise ValueError(f"digit must be in {{-1,0,+1}}, got {digit!r}")
        if carry not in self.alphabet:
            raise ValueError(f"carry must be in {{-1,0,+1}}, got {carry!r}")
        return divide_by_two_step(carry, digit)

    def apply_even(self, word: WordLike) -> BalancedTernary:
        lsd = digits(normalize(word))
        n = decode(word)
        if n % 2 != 0:
            raise LeftoverCarryError(f"word decodes to odd integer {n}")
        carry = 0
        out: list[int] = []
        for d in lsd:
            carry, a = divide_by_two_step(carry, d)
            out.append(a)
        if carry != 0:
            raise LeftoverCarryError(
                f"leftover 3-adic carry {carry} after {normalize(word).word()!r}"
            )
        return from_digits_lsd(out)

    def trace(self, word: WordLike) -> list[tuple[int, int, int, int]]:
        """Rows ``(carry_in, input_digit, output_digit, carry_out)``."""
        lsd = digits(normalize(word))
        carry = 0
        rows: list[tuple[int, int, int, int]] = []
        for d in lsd:
            nxt, a = divide_by_two_step(carry, d)
            rows.append((carry, d, a, nxt))
            carry = nxt
        return rows


def apply_even(word: WordLike) -> BalancedTernary:
    return DivideByTwoTransducer().apply_even(word)
