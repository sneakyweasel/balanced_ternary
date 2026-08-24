"""OEIS-faithful maps on canonical balanced ternary words.

All maps reuse :func:`bt.representation.encode` and
:func:`bt.representation.decode`. They do not introduce a
second encoder.

Maps:

- ``bt_reverse`` / :math:`W`: OEIS A134028, reverse the canonical MSD-first
  word then decode (leading zeros after reverse are stripped). This is
  **not** an involution: :math:`W(W(n))=n` if and only if :math:`n=0` or
  :math:`3\\nmid n`.
- ``bt_reverse_zeros`` / :math:`W_z`: OEIS A160652, reverse leaving trailing
  zeros. Involutive on :math:`\\mathbb{Z}`. Equals :math:`W(n)\\,3^{v_3(n)}`.
- ``bt_reverse_tail`` / :math:`W_{\\mathrm{tail}}`: OEIS A351702, reverse every
  digit except the MSD. Involutive on each A134021 length block.
- ``bt_is_palindrome``: OEIS A134027, the canonical word equals its reverse.
- ``bt_digit_sum`` / :math:`s_3`: OEIS A065363.
- ``bt_alternating_digit_sum``: OEIS A065364, :math:`\\sum_i a_i (-1)^i`.
- ``bt_length`` / :math:`L_3`: OEIS A134021.

Published prefixes below are copied from OEIS. They are fixtures, not
invented examples.
"""

from __future__ import annotations

from bt.metrics import signed_digit_sum
from bt.metrics import v3
from bt.representation import (
    BalancedTernary,
    decode,
    digits,
    encode,
)

# OEIS A134028, n = 0, 1, 2, ...
A134028_PREFIX: tuple[int, ...] = (
    0, 1, -2, 1, 4, -11, -2, 7, -8, 1, 10, -5, 4, 13, -38, -11, 16, -29,
    -2, 25, -20, 7, 34, -35, -8, 19, -26, 1, 28, -17, 10, 37, -32, -5, 22,
    -23, 4, 31, -14, 13, 40, -119, -38, 43, -92, -11, 70, -65, 16, 97, -110,
    -29, 52, -83, -2, 79, -56, 25, 106, -101, -20, 61, -74, 7, 88, -47, 34,
    115, -116, -35, 46, -89, -8, 73, -62, 19, 100,
)

# OEIS A351702, n = 0, 1, 2, ...
A351702_PREFIX: tuple[int, ...] = (
    0, 1, 2, 3, 4, 5, 8, 11, 6, 9, 12, 7, 10, 13, 14, 23, 32, 17, 26, 35,
    20, 29, 38, 15, 24, 33, 18, 27, 36, 21, 30, 39, 16, 25, 34, 19, 28, 37,
    22, 31, 40, 41, 68, 95, 50, 77, 104, 59, 86, 113, 44, 71, 98, 53, 80,
    107, 62, 89, 116, 47, 74, 101, 56, 83, 110, 65, 92,
)

# OEIS A160652, n = 0, 1, 2, ...
A160652_PREFIX: tuple[int, ...] = (
    0, 1, -2, 3, 4, -11, -6, 7, -8, 9, 10, -5, 12, 13, -38, -33, 16, -29,
    -18, 25, -20, 21, 34, -35, -24, 19, -26, 27, 28, -17, 30, 37, -32, -15,
    22, -23, 36, 31, -14, 39, 40, -119, -114, 43, -92, -99, 70, -65, 48, 97,
    -110, -87, 52, -83, -54, 79, -56, 75, 106, -101,
)

# OEIS A065363, n = 0, 1, 2, ...
A065363_PREFIX: tuple[int, ...] = (
    0, 1, 0, 1, 2, -1, 0, 1, 0, 1, 2, 1, 2, 3, -2, -1, 0, -1, 0, 1, 0, 1,
    2, -1, 0, 1, 0, 1, 2, 1, 2, 3, 0, 1, 2, 1, 2, 3, 2, 3, 4, -3, -2, -1,
    -2, -1, 0, -1, 0, 1, -2, -1, 0, -1, 0, 1, 0, 1, 2, -1, 0, 1, 0, 1, 2,
    1, 2, 3, -2, -1, 0, -1, 0, 1, 0, 1, 2, -1, 0, 1, 0, 1, 2, 1, 2, 3, 0,
    1, 2, 1, 2, 3, 2, 3, 4, -1, 0, 1, 0, 1, 2, 1, 2, 3, 0, 1, 2, 1, 2,
)

# OEIS A065364, offset 1.
A065364_PREFIX: tuple[int, ...] = (
    1, -2, -1, 0, 1, 2, 3, 0, 1, 2, -1, 0, 1, -2, -1, 0, -3, -2, -1, -4,
    -3, -2, -1, 0, 1, -2, -1, 0, -3, -2, -1, 0, 1, 2, -1, 0, 1, -2, -1, 0,
    1, 2, 3, 0, 1, 2, -1, 0, 1, 2, 3, 4, 1, 2, 3, 0, 1, 2, 3, 4, 5, 2, 3,
    4, 1, 2, 3, 0, 1, 2, -1, 0, 1, -2, -1, 0, 1, 2, 3, 0, 1, 2, -1, 0, 1,
    2, 3, 4, 1, 2, 3, 0, 1, 2, -1, 0, 1, -2, -1, 0, -3, -2, -1, 0,
)

# OEIS A134028 comments: a(20)=-20, a(21)=7, a(22)=34, a(23)=-35,
# a(24)=-8, a(25)=19.
A134028_EXAMPLES: tuple[tuple[int, int], ...] = (
    (20, -20),
    (21, 7),
    (22, 34),
    (23, -35),
    (24, -8),
    (25, 19),
)

# OEIS A351702 example: 224 = (1,0,-1,1,0,-1) maps to 168.
A351702_EXAMPLES: tuple[tuple[int, int], ...] = ((224, 168),)

# OEIS A065364 example: n=5 maps to 1.
A065364_EXAMPLES: tuple[tuple[int, int], ...] = ((5, 1),)

# OEIS A065363 example: n=5 maps to -1.
A065363_EXAMPLES: tuple[tuple[int, int], ...] = ((5, -1),)

# OEIS A160652 example: 87 maps to -51.
A160652_EXAMPLES: tuple[tuple[int, int], ...] = ((87, -51),)


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def bt_reverse(n: int) -> int:
    """A134028: reverse canonical MSD-first digits, then decode."""
    n = _require_int(n)
    if n == 0:
        return 0
    reversed_msd = tuple(reversed(encode(n).digits_msd))
    return decode(BalancedTernary(reversed_msd))


def bt_reverse_zeros(n: int) -> int:
    """A160652: reverse leaving trailing zeros. Involutive on Z."""
    n = _require_int(n)
    if n == 0:
        return 0
    valuation = v3(n)
    if valuation is None:
        return 0
    return bt_reverse(n) * (3 ** valuation)


def bt_reverse_tail(n: int) -> int:
    """A351702: reverse every digit except the most-significant digit."""
    n = _require_int(n)
    if n == 0:
        return 0
    if n < 0:
        return -bt_reverse_tail(-n)
    msd = encode(n).digits_msd
    if len(msd) == 1:
        return n
    return decode(BalancedTernary((msd[0],) + tuple(reversed(msd[1:]))))


def bt_is_palindrome(n: int) -> bool:
    """True iff the canonical MSD-first word is a palindrome (A134027)."""
    n = _require_int(n)
    msd = encode(n).digits_msd
    return msd == tuple(reversed(msd))


def bt_digit_sum(n: int) -> int:
    """A065363: signed sum of balanced ternary digits."""
    return signed_digit_sum(encode(_require_int(n)))


def bt_alternating_digit_sum(n: int) -> int:
    """A065364: replace 3^k by (-1)^k in the expansion of n."""
    n = _require_int(n)
    return sum(a * ((-1) ** i) for i, a in enumerate(digits(encode(n))))


def bt_length(n: int) -> int:
    """A134021: length of the canonical balanced ternary word."""
    return len(encode(_require_int(n)))


def reverse_is_involution(n: int) -> bool:
    """True iff ``bt_reverse(bt_reverse(n)) == n``.

    **EXACT — HUMAN PROOF:** this holds exactly when ``n == 0`` or ``n % 3 != 0``.
    Trailing zeros of a nonzero multiple of 3 become leading zeros after
    reverse and are stripped by canonicalization.
    """
    n = _require_int(n)
    return n == 0 or n % 3 != 0
