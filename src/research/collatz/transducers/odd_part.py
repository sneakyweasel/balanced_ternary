"""Odd-part map ``x -> x / 2^{v2(x)}`` on balanced ternary words.

For each *fixed* k the restriction to ``{x : v2(x) = k}`` is a sequential
letter-to-letter Mealy transduction (the ``/2^k`` machine), followed by
canonical stripping of leading zeros. The unrestricted map, with unbounded
k, is a countable union of those machines. It is **not** a single
rational / subsequential transduction: see the four-step argument in
``docs/collatz_mathematics.md`` (model, closure, non-regularity of
``{BT(±2^j)}``, contradiction). A failed search for a small DFA is not
that proof.

Detecting k itself requires 2-adic precision growing with k, so k is not a
bounded-state function of the word.
"""

from __future__ import annotations

from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    encode,
    normalize,
)
from research.collatz.transducers.divide_by_two_power import apply_divisible
from research.collatz.valuation import v2


def odd_part_word(word: WordLike) -> BalancedTernary:
    """``BT(x / 2^{v2(x)})``. ``x = 0`` maps to ``0`` (valuation infinity)."""
    n = decode(word)
    if n == 0:
        return encode(0)
    k = v2(n)
    assert k is not None
    if k == 0:
        return normalize(word)
    return apply_divisible(word, k)
