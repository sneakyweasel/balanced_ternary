"""Digit calculus on coefficient words versus after normalization.

``D_coeff`` drops ``c_0``. ``I_a`` prepends a trit ``a``. ``S`` prepends ``0``.

``D(normalize(P)) = normalize(D_coeff(P))`` fails when ``c_0`` is not a
trit: the low coefficient still contributes to the integer value until
it is rewritten.
"""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.integral import I
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.strategies import normal_form

# Canonical semantic derivative on raw words: ``bt.normtheory.hatd.hatD``.
# Naive ``D_coeff`` is kept as the false drop operator.


def D_coeff(word: CoeffWord) -> CoeffWord:
    if word.width() <= 1:
        return CoeffWord((0,))
    return CoeffWord(word.coeffs[1:])


def I_coeff(a: int, word: CoeffWord) -> CoeffWord:
    if a not in (-1, 0, 1):
        raise ValueError(f"a must be a trit, got {a}")
    return CoeffWord((a,) + word.coeffs)


def S_coeff(word: CoeffWord) -> CoeffWord:
    return I_coeff(0, word)


def D_normalize_commute(word: CoeffWord) -> bool:
    """True iff ``D(normalize(P))`` equals ``normalize(D_coeff(P))`` as values
    *and* as coefficient words of those integers.
    """
    nf = normal_form(word)
    left = D(nf.value())
    right = normal_form(D_coeff(word)).value()
    return left == right and CoeffWord.from_value(left).value() == right


def D_normalize_words_equal(word: CoeffWord) -> bool:
    left = normal_form(D_coeff(normal_form(word)))
    # D of a canonical word is the tail (or 0).
    nf = normal_form(word)
    d_word = D_coeff(nf)
    right = normal_form(D_coeff(word))
    return d_word.coeffs == right.coeffs == left.coeffs


def commute_side_condition(word: CoeffWord) -> bool:
    """Sufficient: the LSD is already a trit.

    Then dropping it commutes with later high-site rewrites, and
    Strategy A on the tail is ``D`` of Strategy A on the word.
    """
    return word.coefficient(0) in (-1, 0, 1)


def I_section_on_coeff(a: int, word: CoeffWord) -> bool:
    """``D_coeff(I_coeff(a, P)) = P`` always."""
    return D_coeff(I_coeff(a, word)).coeffs == word.coeffs


def integer_I_matches(a: int, word: CoeffWord) -> bool:
    return I_coeff(a, word).value() == I(a, word.value())


def integer_D_matches_when_canonical(word: CoeffWord) -> bool:
    if not word.is_canonical():
        return D_coeff(word).value() != D(word.value()) or word.coefficient(0) in (-1, 0, 1)
    return D_coeff(word).value() == D(word.value())
