"""LSD-first section words using existing ``I_a``. Do not re-encode digits."""

from __future__ import annotations

from collections.abc import Sequence

from bt.calculus.derivative import D, lsd
from bt.calculus.integral import I
from bt.calculus.jets import integer_jet

TRITS: tuple[int, int, int] = (-1, 0, 1)


def require_trit(digit: int) -> int:
    if digit not in TRITS:
        raise ValueError(f"digit must be a trit, got {digit!r}")
    return digit


def apply_section_word(x: int, word: Sequence[int]) -> int:
    """Apply ``I_{a0}`` then ``I_{a1}`` … ; each letter is a newly prepended LSD."""
    value = int(x)
    for digit in word:
        value = I(require_trit(int(digit)), value)
    return value


def value_from_jet(jet: Sequence[int]) -> int:
    """Integer whose length-``L`` LSD jet is ``jet`` and whose high part is 0."""
    value = 0
    for digit in reversed(tuple(jet)):
        value = I(require_trit(int(digit)), value)
    return value


def eval_lsd_word(word: Sequence[int]) -> int:
    """``a0 + 3 a1 + … + 3^{L-1} a_{L-1}``."""
    total = 0
    power = 1
    for digit in word:
        total += require_trit(int(digit)) * power
        power *= 3
    return total


def predecessor(n: int) -> int:
    """Unique integer preimage under some ``I_a``: ``D(n)`` with control ``lsd(n)``."""
    return D(int(n))


def predecessor_control(n: int) -> int:
    return int(lsd(int(n)))


def i0_prime_only_at_one(x: int) -> bool:
    """``Prime(I_0(x))`` holds if and only if ``x = 1``."""
    from bt.arithmetic import is_prime

    return is_prime(I(0, int(x)))


def same_jet(left: int, right: int, length: int) -> bool:
    return integer_jet(int(left), length) == integer_jet(int(right), length)
