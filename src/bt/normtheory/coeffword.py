"""Integer coefficient vectors, LSD-first. Not canonical balanced words.

``coeffs[i]`` is the coefficient of ``3^i``. Trailing high zeros are stripped
except for the zero word ``(0,)``. Coefficients may be any integers.
"""

from __future__ import annotations

from dataclasses import dataclass


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def _strip(coeffs: tuple[int, ...]) -> tuple[int, ...]:
    i = len(coeffs)
    while i > 1 and coeffs[i - 1] == 0:
        i -= 1
    return coeffs[:i] if i else (0,)


@dataclass(frozen=True)
class CoeffWord:
    """LSD-first integer coefficient vector."""

    coeffs: tuple[int, ...]

    def __post_init__(self) -> None:
        raw = tuple(_require_int(c, "coefficient") for c in self.coeffs)
        object.__setattr__(self, "coeffs", _strip(raw))

    @classmethod
    def from_ints(cls, *coeffs: int) -> "CoeffWord":
        return cls(coeffs)

    @classmethod
    def from_value(cls, n: int) -> "CoeffWord":
        """Singleton ``[n]``, the raw integer as a degree-0 coefficient."""
        return cls((_require_int(n),))

    def value(self) -> int:
        acc = 0
        pow3 = 1
        for c in self.coeffs:
            acc += c * pow3
            pow3 *= 3
        return acc

    def degree(self) -> int:
        if self.coeffs == (0,):
            return -1
        return len(self.coeffs) - 1

    def width(self) -> int:
        return len(self.coeffs)

    def coefficient(self, i: int) -> int:
        i = _require_int(i, "i")
        if i < 0:
            raise ValueError(f"i must be >= 0, got {i}")
        if i >= len(self.coeffs):
            return 0
        return self.coeffs[i]

    def is_canonical(self) -> bool:
        """All coefficients are trits and there is no extra high zero."""
        if any(c not in (-1, 0, 1) for c in self.coeffs):
            return False
        return True

    def l1(self) -> int:
        return sum(abs(c) for c in self.coeffs)

    def excess(self) -> int:
        return sum(max(0, abs(c) - 1) for c in self.coeffs)

    def peak(self) -> int:
        return max(abs(c) for c in self.coeffs)

    def abs_tuple(self) -> tuple[int, ...]:
        return tuple(abs(c) for c in self.coeffs)

    def __len__(self) -> int:
        return len(self.coeffs)


def value(word: CoeffWord) -> int:
    return word.value()


def degree(word: CoeffWord) -> int:
    return word.degree()


def coefficient(word: CoeffWord, i: int) -> int:
    return word.coefficient(i)


def is_canonical(word: CoeffWord) -> bool:
    return word.is_canonical()
