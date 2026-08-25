"""Exact affine blocks of the shortcut map.

A word ``w`` of length ``k`` induces ``C^k(n) = (a n + b) / 2^k`` on the
unique residue class that realises ``w``. Coefficients are derived by
composition, not by an assumed closed form for ``b``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from research.collatz_finite_descent.shortcut import (
    CONTROL_EVEN,
    CONTROL_ODD,
    apply_word,
    iterate_shortcut,
    parity_word,
    require_positive_int,
    shortcut_step,
)

CONTROLS: tuple[str, ...] = (CONTROL_EVEN, CONTROL_ODD)
DEFAULT_BLOCK_BOUND = 12


@dataclass(frozen=True)
class ShortcutBlock:
    """Exact affine action of one legal parity word."""

    word: tuple[str, ...]
    slope: int
    intercept: int
    denominator: int
    residue: int
    odd_count: int

    def __post_init__(self) -> None:
        k = len(self.word)
        if self.denominator != 2**k:
            raise ValueError("denominator must be 2^{length}")
        if self.odd_count != sum(1 for control in self.word if control == CONTROL_ODD):
            raise ValueError("odd_count must match the word")
        if not 0 <= self.residue < self.denominator:
            raise ValueError("residue must lie in 0 .. 2^k - 1")

    @property
    def length(self) -> int:
        return len(self.word)

    @property
    def modulus(self) -> int:
        return self.denominator

    def apply_legal(self, n: int) -> int:
        n = require_positive_int(n)
        if n % self.modulus != self.residue:
            raise ValueError(f"{n} is not legal for {self.word!r}")
        return (self.slope * n + self.intercept) // self.denominator

    def contracts(self, n: int) -> bool:
        n = require_positive_int(n)
        if n % self.modulus != self.residue:
            return False
        return (self.slope - self.denominator) * n + self.intercept < 0

    def contraction_threshold(self) -> tuple[str, int | None]:
        """Exact large-n behaviour and the integer threshold when it exists.

        Returns ``("expanding", None)`` if every sufficiently large legal
        ``n`` increases, ``("contracting", t)`` if every legal ``n > t``
        decreases, or ``("affine_tie", None)`` if the slope equals ``2^k``.
        """
        delta = self.slope - self.denominator
        if delta == 0:
            return ("affine_tie", None)
        if delta > 0:
            return ("expanding", None)
        raw = -self.intercept // delta
        return ("contracting", raw)

    def smallest_legal(self) -> int:
        if self.residue == 0:
            return self.modulus
        return self.residue

    def smallest_noncontracting_legal(self) -> int | None:
        """Smallest legal positive ``n`` with ``C^k(n) >= n``, if any exist."""
        start = self.smallest_legal()
        kind, threshold = self.contraction_threshold()
        if kind == "expanding":
            return start
        if kind == "affine_tie":
            if not self.contracts(start):
                return start
            return None
        assert threshold is not None
        n = start
        while n <= max(start, threshold):
            if not self.contracts(n):
                return n
            n += self.modulus
        return None


def _compose_coefficients(
    word: tuple[str, ...],
    odd_mul: int,
    odd_add: int,
) -> tuple[int, int, int]:
    slope, intercept, denom = 1, 0, 1
    for control in word:
        if control == CONTROL_EVEN:
            denom *= 2
            continue
        if control != CONTROL_ODD:
            raise ValueError(f"unknown control {control!r}")
        slope = odd_mul * slope
        intercept = odd_mul * intercept + odd_add * denom
        denom *= 2
    return slope, intercept, denom


def residue_of_word(
    word: tuple[str, ...],
    odd_mul: int = 3,
    odd_add: int = 1,
) -> int:
    """Unique ``r`` in ``0 .. 2^k - 1`` whose parity word is ``word``.

    Each letter constrains one further 2-adic bit of ``n`` by lifting the
    already-determined residue so that the next affine image has the
    required parity. The lift is unique because the running slope is odd.
    """
    residue = 0
    for index, control in enumerate(word):
        if control not in CONTROLS:
            raise ValueError(f"unknown control {control!r}")
        slope, intercept, denom = _compose_coefficients(word[:index], odd_mul, odd_add)
        image = (slope * residue + intercept) // denom
        wanted = 0 if control == CONTROL_EVEN else 1
        bit = (wanted - (image % 2)) % 2
        residue = residue + bit * denom
    return residue


def block_from_word(
    word: tuple[str, ...],
    odd_mul: int = 3,
    odd_add: int = 1,
) -> ShortcutBlock:
    slope, intercept, denom = _compose_coefficients(word, odd_mul, odd_add)
    odd_count = sum(1 for control in word if control == CONTROL_ODD)
    residue = residue_of_word(word, odd_mul, odd_add)
    block = ShortcutBlock(
        word=word,
        slope=slope,
        intercept=intercept,
        denominator=denom,
        residue=residue,
        odd_count=odd_count,
    )
    witness = block.smallest_legal()
    if parity_word(witness, block.length, odd_mul, odd_add) != word:
        raise ArithmeticError("derived residue does not realise the word")
    image = apply_word(witness, word, odd_mul, odd_add)
    if image != block.apply_legal(witness):
        raise ArithmeticError("derived affine action disagrees with the shortcut map")
    return block


def enumerate_blocks(
    max_length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> tuple[ShortcutBlock, ...]:
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 0:
        raise ValueError(f"max_length must be a nonnegative integer, got {max_length!r}")
    out: list[ShortcutBlock] = []
    for length in range(1, max_length + 1):
        for letters in product(CONTROLS, repeat=length):
            out.append(block_from_word(letters, odd_mul, odd_add))
    return tuple(out)


def unique_block(
    n: int,
    length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> ShortcutBlock:
    return block_from_word(parity_word(n, length, odd_mul, odd_add), odd_mul, odd_add)


def is_asymptotically_contracting(block: ShortcutBlock) -> bool:
    return block.slope < block.denominator


def escape_residues(length: int, odd_mul: int = 3, odd_add: int = 1) -> tuple[int, ...]:
    """Residues mod ``2^length`` whose unique word is not eventually contracting."""
    modulus = 2**length
    found: list[int] = []
    for residue in range(modulus):
        n = modulus if residue == 0 else residue
        block = unique_block(n, length, odd_mul, odd_add)
        if not is_asymptotically_contracting(block):
            found.append(residue)
    return tuple(found)


def contraction_profile(
    residue: int,
    length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> tuple[bool, ...]:
    """Whether each prefix of the unique length-``length`` word contracts for large ``n``."""
    modulus = 2**length
    n = modulus if residue == 0 else residue
    word = parity_word(n, length, odd_mul, odd_add)
    return tuple(
        is_asymptotically_contracting(block_from_word(word[:k], odd_mul, odd_add))
        for k in range(1, length + 1)
    )


def behavioral_classes(
    length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> dict[tuple[bool, ...], tuple[int, ...]]:
    """Partition of ``Z/2^length`` by prefix-contraction profiles."""
    groups: dict[tuple[bool, ...], list[int]] = {}
    for residue in range(2**length):
        profile = contraction_profile(residue, length, odd_mul, odd_add)
        groups.setdefault(profile, []).append(residue)
    return {key: tuple(values) for key, values in groups.items()}


def separating_residues(
    length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> tuple[int, int] | None:
    """Two residues with the same profile only if the quotient is not discrete.

    If the map residue → profile is injective, returns ``None``. Otherwise
    returns one colliding pair.
    """
    seen: dict[tuple[bool, ...], int] = {}
    for residue in range(2**length):
        profile = contraction_profile(residue, length, odd_mul, odd_add)
        if profile in seen:
            return (seen[profile], residue)
        seen[profile] = residue
    return None


def expanding_legal_witness(
    length: int,
    odd_mul: int = 3,
    odd_add: int = 1,
) -> tuple[int, int, tuple[str, ...]]:
    """Smallest residue class mod ``2^length`` whose unique block does not descend."""
    if isinstance(length, bool) or not isinstance(length, int) or length < 1:
        raise ValueError(f"length must be a positive integer, got {length!r}")
    for residue in range(2**length):
        n = 2**length if residue == 0 else residue
        block = unique_block(n, length, odd_mul, odd_add)
        if is_asymptotically_contracting(block):
            continue
        image = iterate_shortcut(n, length, odd_mul, odd_add)
        if image >= n:
            return n, image, block.word
    raise ArithmeticError(f"no expanding length-{length} class for ({odd_mul},{odd_add})")


def all_odd_witness(length: int) -> int:
    if isinstance(length, bool) or not isinstance(length, int) or length < 1:
        raise ValueError(f"length must be a positive integer, got {length!r}")
    return 2**length - 1


def all_odd_image(length: int, odd_mul: int = 3, odd_add: int = 1) -> int:
    """``C^L(2^L - 1)`` for the all-odd word. Derived by iteration, then checked."""
    n = all_odd_witness(length)
    word = parity_word(n, length, odd_mul, odd_add)
    if word != (CONTROL_ODD,) * length:
        raise ArithmeticError("2^L - 1 did not realise the all-odd word")
    image = iterate_shortcut(n, length, odd_mul, odd_add)
    if image <= n:
        raise ArithmeticError("all-odd block did not expand")
    return image


def one_step_lyapunov_witness(odd_mul: int = 3, odd_add: int = 1) -> int:
    """Smallest positive odd ``n`` with ``C(n) >= n``."""
    n = 1
    while True:
        nxt = shortcut_step(n, odd_mul, odd_add)
        if nxt >= n:
            return n
        n += 2
        if n > 1000:
            raise RuntimeError("no one-step Lyapunov witness below 1000")
