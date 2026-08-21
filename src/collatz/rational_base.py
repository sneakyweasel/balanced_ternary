"""Canonical nonnegative-integer numeration in rational base ``3/2``.

Extraction uses the exact recurrence

    a = (2n) mod 3,       n' = (2n-a)/3,

with digits ``a`` in ``{0,1,2}``.  Displayed words are most-significant
digit first.  Decoding is the inverse integer Horner recurrence

    n' = (3n+a)/2,

and rejects a word as soon as that division is not exact.
"""

from __future__ import annotations

from dataclasses import dataclass


DigitInput = str | tuple[int, ...] | list[int]


def _parse_digits(digits: DigitInput) -> tuple[int, ...]:
    if isinstance(digits, str):
        if not digits:
            return ()
        if any(ch not in "012" for ch in digits):
            raise ValueError("base-3/2 digits must be 0, 1, or 2")
        return tuple(int(ch) for ch in digits)
    if not isinstance(digits, (tuple, list)):
        raise TypeError("digits must be a string, tuple, or list")
    if not digits:
        return ()
    out: list[int] = []
    for digit in digits:
        if isinstance(digit, bool) or not isinstance(digit, int) or digit not in (0, 1, 2):
            raise ValueError(f"base-3/2 digit must be 0, 1, or 2, got {digit!r}")
        out.append(digit)
    return tuple(out)


def encode_base_3_2(n: int) -> str:
    """Return the canonical base-``3/2`` word of ``n >= 0``."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"n must be a nonnegative integer, got {n!r}")
    if n == 0:
        return ""
    lsd_first: list[str] = []
    current = n
    while current:
        digit = (2 * current) % 3
        numerator = 2 * current - digit
        if numerator % 3:
            raise ArithmeticError("base-3/2 extraction recurrence was not integral")
        lsd_first.append(str(digit))
        current = numerator // 3
    return "".join(reversed(lsd_first))


def decode_base_3_2(digits: DigitInput, *, canonical: bool = True) -> int:
    """Decode an admissible integer word, rejecting nonintegral prefixes."""
    parsed = _parse_digits(digits)
    if canonical and len(parsed) > 1 and parsed[0] == 0:
        raise ValueError("canonical base-3/2 words have no leading zero")
    value = 0
    for index, digit in enumerate(parsed):
        numerator = 3 * value + digit
        if numerator % 2:
            raise ValueError(
                f"inadmissible base-3/2 word: prefix ending at index {index} "
                "does not decode to an integer"
            )
        value = numerator // 2
    if canonical and encode_base_3_2(value) != "".join(str(d) for d in parsed):
        raise ValueError("word is not the canonical encoding of its integer")
    return value


def is_admissible_base_3_2(digits: DigitInput, *, canonical: bool = True) -> bool:
    try:
        decode_base_3_2(digits, canonical=canonical)
    except (TypeError, ValueError):
        return False
    return True


def append_odd_step(word: DigitInput) -> str:
    """Append ``1``, representing ``n -> (3n+1)/2`` for odd ``n``."""
    value = decode_base_3_2(word)
    if value % 2 == 0:
        raise ValueError("the appended-1 identity requires an odd integer")
    source = encode_base_3_2(value)
    result = source + "1"
    expected = (3 * value + 1) // 2
    if decode_base_3_2(result) != expected:
        raise ArithmeticError("base-3/2 appended-1 identity failed")
    return result


@dataclass(frozen=True)
class RationalBaseThreeHalves:
    """Canonical exact representation of one nonnegative integer."""

    value: int
    word: str
    digits: tuple[int, ...]

    @classmethod
    def from_int(cls, n: int) -> "RationalBaseThreeHalves":
        word = encode_base_3_2(n)
        representation = cls(n, word, tuple(int(ch) for ch in word))
        if not representation.validates():
            raise ArithmeticError("base-3/2 representation failed validation")
        return representation

    @classmethod
    def from_word(cls, word: DigitInput) -> "RationalBaseThreeHalves":
        value = decode_base_3_2(word)
        return cls.from_int(value)

    def validates(self) -> bool:
        try:
            return (
                self.word == "".join(str(digit) for digit in self.digits)
                and encode_base_3_2(self.value) == self.word
                and decode_base_3_2(self.word) == self.value
            )
        except (TypeError, ValueError):
            return False

    def odd_step(self) -> "RationalBaseThreeHalves":
        return RationalBaseThreeHalves.from_word(append_odd_step(self.word))


# Readable aliases for callers that prefer the module name in the function.
rational_base_encode = encode_base_3_2
rational_base_decode = decode_base_3_2
