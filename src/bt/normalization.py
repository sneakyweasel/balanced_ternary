"""Canonical carry / borrow rewrite for balanced ternary coefficients.

The local identity is the same algorithm previously used by word addition:

    2 = 3 - 1,    -2 = -3 + 1

so a coefficient sum ``s`` in ``{-3,...,3}`` is rewritten as
``digit + 3 * carry`` with ``digit in {-1, 0, +1}``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.representation import (
    BalancedTernary,
    WordLike,
    digits,
    from_digits_lsd,
    normalize,
)


def rewrite_sum(s: int) -> tuple[int, int]:
    """Rewrite ``s in {-3,...,3}`` as ``digit + 3*carry`` with ``digit in {-1,0,1}``."""
    if s >= 2:
        return s - 3, 1
    if s <= -2:
        return s + 3, -1
    return s, 0


# Historical name used by Collatz word arithmetic.
_rewrite_sum = rewrite_sum


@dataclass(frozen=True)
class CarryStep:
    """One LSD-first addition step."""

    index: int
    left: int
    right: int
    carry_in: int
    digit: int
    carry_out: int


@dataclass(frozen=True)
class CarryTrace:
    """Exact carry trace of a word addition. Not a complexity theorem."""

    steps: tuple[CarryStep, ...]
    final_carry: int
    result: BalancedTernary


def add_with_trace(left: WordLike, right: WordLike) -> CarryTrace:
    """Same addition as :func:`bt.arithmetic.add`, with the carry ledger."""
    a = digits(normalize(left))
    b = digits(normalize(right))
    n = max(len(a), len(b))
    out: list[int] = []
    steps: list[CarryStep] = []
    carry = 0
    for i in range(n):
        da = a[i] if i < len(a) else 0
        db = b[i] if i < len(b) else 0
        digit, nxt = rewrite_sum(da + db + carry)
        steps.append(
            CarryStep(
                index=i,
                left=da,
                right=db,
                carry_in=carry,
                digit=digit,
                carry_out=nxt,
            )
        )
        out.append(digit)
        carry = nxt
    if carry:
        out.append(carry)
    return CarryTrace(
        steps=tuple(steps),
        final_carry=carry,
        result=from_digits_lsd(out),
    )
