"""Counterexample-first separators for jet and sieve compressions of Prime."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from bt.arithmetic import is_prime
from bt.calculus.jets import integer_jet
from research.prime_residual_complexity.sections import (
    TRITS,
    apply_section_word,
    value_from_jet,
)
from research.prime_residual_complexity.sieve import DEFAULT_SIEVE, sieve_modulus

MAX_LENGTH = 6
MAX_HORIZON = 3


@dataclass(frozen=True)
class Separator:
    left: int
    right: int
    word: tuple[int, ...]
    left_image: int
    right_image: int
    reason: str

    @property
    def left_prime(self) -> bool:
        return is_prime(self.left_image)

    @property
    def right_prime(self) -> bool:
        return is_prime(self.right_image)


def continuation_words(horizon: int) -> tuple[tuple[int, ...], ...]:
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    words: list[tuple[int, ...]] = [()]
    for length in range(1, horizon + 1):
        words.extend(product(TRITS, repeat=length))
    return tuple(words)


def prime_signature(x: int, horizon: int) -> tuple[bool, ...]:
    return tuple(is_prime(apply_section_word(x, word)) for word in continuation_words(horizon))


def residual_count(length: int, horizon: int) -> int:
    """``R_H(L)``: distinct Prime signatures of length-``L`` LSD windows at horizon ``H``."""
    if length < 0 or horizon < 0:
        raise ValueError("length and horizon must be nonnegative")
    if length > MAX_LENGTH or horizon > MAX_HORIZON:
        raise ValueError(f"Phase-0 cap is L≤{MAX_LENGTH}, H≤{MAX_HORIZON}")
    seen: set[tuple[bool, ...]] = set()
    for jet in product(TRITS, repeat=length):
        seen.add(prime_signature(value_from_jet(jet), horizon))
    return len(seen)


def residual_table(max_length: int, horizon: int) -> tuple[int, ...]:
    return tuple(residual_count(length, horizon) for length in range(1, max_length + 1))


def smallest_distinguishing_word(
    left: int,
    right: int,
    max_horizon: int = MAX_HORIZON,
) -> tuple[int, ...] | None:
    for word in continuation_words(max_horizon):
        left_image = apply_section_word(left, word)
        right_image = apply_section_word(right, word)
        if is_prime(left_image) != is_prime(right_image):
            return word
    return None


IntSeq = tuple[int, ...] | list[int]


def make_separator(left: int, right: int, word: IntSeq, reason: str) -> Separator:
    left_image = apply_section_word(left, word)
    right_image = apply_section_word(right, word)
    return Separator(
        left=int(left),
        right=int(right),
        word=tuple(int(digit) for digit in word),
        left_image=left_image,
        right_image=right_image,
        reason=reason,
    )


def jet_prime_separator(length: int = 1) -> Separator:
    """Same length-``L`` LSD jet, distinguished by ``I_0``.

    ``x=1`` and ``y=1+3^L`` share ``n mod 3^L``. ``I_0(1)=3`` is prime;
    ``I_0(1+3^L)=3(1+3^L)`` is composite.
    """
    if length < 1:
        raise ValueError("length must be at least 1")
    left = 1
    right = 1 + 3**length
    word = (0,)
    if integer_jet(left, length) != integer_jet(right, length):
        raise RuntimeError("jet separator construction failed")
    found = smallest_distinguishing_word(left, right, max_horizon=1)
    if found is None:
        raise RuntimeError("jet separator was not distinguished at horizon 1")
    return make_separator(
        left,
        right,
        found,
        reason=f"same integer_jet length {length}; I_0(1)=3 prime, I_0({right}) composite",
    )


def sieve_prime_separator(primes: IntSeq = DEFAULT_SIEVE) -> Separator:
    """Same residue mod ``M=∏S``, distinguished by ``I_0``.

    ``x=1`` and ``y=1+M`` are both coprime to ``M``. ``I_0(1)=3`` is prime;
    ``I_0(1+M)=3(1+M)`` is composite.
    """
    modulus = sieve_modulus(primes)
    left = 1
    right = 1 + modulus
    word = (0,)
    found = smallest_distinguishing_word(left, right, max_horizon=1)
    if found is None:
        raise RuntimeError("sieve separator was not distinguished at horizon 1")
    return make_separator(
        left,
        right,
        word,
        reason=(
            f"same residue mod {modulus}; smallest word {found}; "
            f"constructive I_0(1)=3 prime, I_0({right})={3 * right} composite"
        ),
    )
