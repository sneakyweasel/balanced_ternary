"""Normalized coefficient derivative ``hat D``.

Naive ``D_coeff`` (drop ``c_0``) is **not** semantic ``D``. Milestone 14
witness ``[2]``: ``D(normalize([2])) = 1`` while ``D_coeff([2])`` has
value ``0``.

The correct total operator on raw words is *drop plus carry correction*:

    hatD_raw(c :: tail) = addHead(DZ(c), tail)

which satisfies ``value(hatD_raw(P)) = D(value(P))`` with no side
condition. Canonical ``hat D`` is Strategy A of that word, equivalently
``encode(D(value(P)))``.
"""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.normtheory.calculus_link import D_coeff, I_coeff
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.rewrite import balanced_divmod
from bt.normtheory.strategies import normal_form
from bt.representation import encode


def hatD_raw(word: CoeffWord) -> CoeffWord:
    """One LSD ``balanced_divmod``, then drop the resulting trit.

    Total on every finite coefficient word. Value-correct, not necessarily
    canonical.
    """
    _r, q = balanced_divmod(word.coefficient(0))
    tail = list(word.coeffs[1:]) if word.width() > 1 else []
    if tail:
        tail[0] += q
    elif q:
        tail = [q]
    return CoeffWord(tuple(tail) if tail else (0,))


def hatD(word: CoeffWord) -> CoeffWord:
    """Canonical coefficient derivative: ``encode(D(value(P)))``."""
    return CoeffWord(encode(D(word.value())).digits_lsd())


def hatD_via_normalize(word: CoeffWord) -> CoeffWord:
    """``normalize(D_coeff(normalize(P)))``. Equals :func:`hatD`."""
    nf = normal_form(word)
    return normal_form(D_coeff(nf))


def semantic_D(word: CoeffWord) -> int:
    return D(word.value())


def naive_raw_fails(word: CoeffWord) -> bool:
    """True when naive drop disagrees with semantic ``D``."""
    return D_coeff(word).value() != D(word.value())


def milestone14_witness() -> CoeffWord:
    return CoeffWord((2,))


def hatD_I_raw(a: int, word: CoeffWord) -> CoeffWord:
    """``hatD_raw(I_a(P))``. Equals ``P`` as a raw word, including noncanonical ``P``."""
    return hatD_raw(I_coeff(a, word))


def hatD_I_canonical(a: int, word: CoeffWord) -> CoeffWord:
    """Canonical ``hat D(I_a(P)) = normalize(P)``, not raw ``P``."""
    return hatD(I_coeff(a, word))
