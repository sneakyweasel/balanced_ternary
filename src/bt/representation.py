"""Canonical balanced ternary representation.

Every integer has a unique canonical expansion

    n = sum_{i=0}^{k-1} a_i 3^i,    a_i in {-1, 0, +1}

with no leading zeros (except n = 0, whose word is ``0``). Positive integers
have most-significant digit ``+``; negatives have most-significant digit ``-``.

Display alphabet (most-significant digit first):

    '-'  ->  -1
    '0'  ->   0
    '+'  ->  +1

Mathematical digit positions are always indexed from the *least*-significant
digit: a_0 is the last character of the displayed word. See
``docs/mathematics.md``.
"""

from __future__ import annotations

from typing import Iterable, Sequence, Union

CHAR_TO_DIGIT: dict[str, int] = {"-": -1, "0": 0, "+": 1}
DIGIT_TO_CHAR: dict[int, str] = {-1: "-", 0: "0", 1: "+"}

WordLike = Union[str, "BalancedTernary"]


class BalancedTernary:
    """Canonical balanced ternary word.

    Internally stores most-significant-first digits in ``{-1, 0, +1}``.
    Use :meth:`digits_lsd` (or the module-level :func:`digits`) for
    mathematically indexed coefficients ``a_0, a_1, ...``.
    """

    __slots__ = ("_msd",)

    def __init__(self, digits_msd: Sequence[int]):
        msd = tuple(digits_msd)
        _validate_digits(msd)
        self._msd = _strip_leading_zeros(msd)

    @property
    def digits_msd(self) -> tuple[int, ...]:
        """Digits most-significant first (display order)."""
        return self._msd

    def digits_lsd(self) -> tuple[int, ...]:
        """Digits least-significant first: ``(a_0, a_1, ..., a_{k-1})``."""
        return tuple(reversed(self._msd))

    def word(self) -> str:
        return "".join(DIGIT_TO_CHAR[d] for d in self._msd)

    def __str__(self) -> str:
        return self.word()

    def __repr__(self) -> str:
        return f"BalancedTernary({self.word()!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BalancedTernary):
            return self._msd == other._msd
        if isinstance(other, str):
            return self.word() == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._msd)

    def __len__(self) -> int:
        return len(self._msd)

    def __neg__(self) -> BalancedTernary:
        return BalancedTernary(tuple(-d for d in self._msd))


def _validate_digits(digits: Sequence[int]) -> None:
    if not digits:
        raise ValueError("digit sequence must be non-empty")
    for d in digits:
        if d not in DIGIT_TO_CHAR:
            raise ValueError(f"invalid balanced ternary digit: {d!r}")


def _strip_leading_zeros(digits_msd: Sequence[int]) -> tuple[int, ...]:
    i = 0
    n = len(digits_msd)
    while i < n - 1 and digits_msd[i] == 0:
        i += 1
    return tuple(digits_msd[i:])


def parse_digits_msd(word: str) -> tuple[int, ...]:
    """Parse a display string into MSD-first digits. Does not strip zeros."""
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    if word == "":
        raise ValueError("empty word is not a valid balanced ternary string")
    digits = []
    for ch in word:
        if ch not in CHAR_TO_DIGIT:
            raise ValueError(f"invalid balanced ternary digit {ch!r} in {word!r}")
        digits.append(CHAR_TO_DIGIT[ch])
    return tuple(digits)


def msd_digits(word: WordLike) -> tuple[int, ...]:
    """MSD-first digits of a string (as written) or a canonical object."""
    if isinstance(word, BalancedTernary):
        return word.digits_msd
    return parse_digits_msd(word)


def encode(n: int) -> BalancedTernary:
    """Convert an integer to its unique canonical balanced ternary word.

    Uses only integer ``%`` / ``//``. Remainder 2 is rewritten as digit -1
    with a carry of +1, since 2 = 3 - 1.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0:
        return BalancedTernary((0,))

    digits_lsd: list[int] = []
    while n != 0:
        rem = n % 3
        n = n // 3
        if rem == 2:
            digits_lsd.append(-1)
            n += 1
        else:
            digits_lsd.append(rem)
    return BalancedTernary(tuple(reversed(digits_lsd)))


def decode(word: WordLike) -> int:
    """Evaluate a balanced ternary word (canonical or with leading zeros)."""
    n = 0
    for d in msd_digits(word):
        n = 3 * n + d
    return n


def normalize(word: WordLike) -> BalancedTernary:
    """Validate a word and return its unique canonical representative."""
    if isinstance(word, BalancedTernary):
        return word
    return BalancedTernary(parse_digits_msd(word))


def digits(word: WordLike) -> tuple[int, ...]:
    """Canonical digits indexed from the least-significant position.

    ``digits(word)[i]`` is the coefficient ``a_i`` of ``3^i``.
    """
    return normalize(word).digits_lsd()


def is_canonical(word: WordLike) -> bool:
    """True if ``word`` is already in canonical form."""
    if isinstance(word, BalancedTernary):
        return True
    parsed = parse_digits_msd(word)
    return parsed == _strip_leading_zeros(parsed)


def from_digits_lsd(digits_lsd: Iterable[int]) -> BalancedTernary:
    """Build a canonical word from LSD-first coefficients ``a_0, a_1, ...``."""
    seq = tuple(digits_lsd)
    if not seq:
        return BalancedTernary((0,))
    return BalancedTernary(tuple(reversed(seq)))
