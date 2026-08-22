"""Exact amplitude of an accelerated odd-only cycle.

Accelerated states are positive odd integers. Two conventions are stored:

- additive amplitude: ``max(states) - min(states)``
- multiplicative amplitude: ``max(states) / min(states)`` as a ``Fraction``

These are **not** assumed to match any preprint. Literature adapters live
in the same module and document the translation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from collatz.core import require_positive_odd


@dataclass(frozen=True)
class CycleAmplitude:
    min_state: int
    max_state: int
    additive: int
    multiplicative: Fraction

    def as_dict(self) -> dict[str, object]:
        return {
            "min_state": self.min_state,
            "max_state": self.max_state,
            "additive": self.additive,
            "multiplicative_num": self.multiplicative.numerator,
            "multiplicative_den": self.multiplicative.denominator,
        }


def cycle_amplitude(states: tuple[int, ...]) -> CycleAmplitude:
    """Amplitude of a nonempty tuple of positive odd cycle states."""
    if not states:
        raise ValueError("amplitude is undefined for an empty state list")
    cleaned = tuple(require_positive_odd(state, "state") for state in states)
    lo = min(cleaned)
    hi = max(cleaned)
    return CycleAmplitude(
        min_state=lo,
        max_state=hi,
        additive=hi - lo,
        multiplicative=Fraction(hi, lo),
    )


def additive_amplitude_is_even(states: tuple[int, ...]) -> bool:
    """Odd minus odd is even. **PROVED** for accelerated states."""
    return cycle_amplitude(states).additive % 2 == 0


def amplitude_lebel_radius(code: tuple[int, ...], christoffel: tuple[int, ...]) -> int:
    """Hamming distance to a reference Christoffel exponent word.

    Lebel's 2026 preprint speaks of a radius-1 exclusion problem around
    the Christoffel class. The preprint is **not** assumed correct. This
    adapter is the Hamming metric on equal-length exponent words.
    """
    if len(code) != len(christoffel):
        raise ValueError("Lebel-radius adapter requires equal lengths")
    return sum(int(a != b) for a, b in zip(code, christoffel))


def syracuse_parity_word(code: tuple[int, ...]) -> tuple[int, ...]:
    """Syracuse parity bits: each ``k`` contributes ``1`` then ``k-1`` zeros.

    This is the dictionary from accelerated exponent codes to the
    Fernández–Ibáñez / Terras parity-word length ``N = K``, ``r = p``.
    """
    bits: list[int] = []
    for k in code:
        if k < 1:
            raise ValueError("valuations must be >= 1")
        bits.append(1)
        bits.extend([0] * (k - 1))
    return tuple(bits)


def exponent_code_from_syracuse(bits: tuple[int, ...]) -> tuple[int, ...]:
    """Inverse of ``syracuse_parity_word``. The first bit must be ``1``."""
    if not bits or bits[0] != 1:
        raise ValueError("a Syracuse cycle word must start with an odd step")
    ks: list[int] = []
    run = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("parity bits must be 0 or 1")
        if bit == 1:
            if run:
                ks.append(run)
            run = 1
        else:
            if run == 0:
                raise ValueError("a leading even bit is not an accelerated start")
            run += 1
    ks.append(run)
    return tuple(ks)


def fernandez_slope(code: tuple[int, ...]) -> Fraction:
    """``N/r = K/p`` in the Syracuse/parity-word dictionary."""
    p = len(code)
    if p == 0:
        raise ValueError("empty code has no slope")
    return Fraction(sum(code), p)
