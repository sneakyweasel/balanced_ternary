"""Integer and word semantics for calculus expressions."""

from __future__ import annotations

from bt.calculus.derivative import D, lsd
from bt.calculus.expressions import (
    EAdd,
    ECmp3,
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    EMul,
    ENeg,
    ENormalize,
    ESelect3,
    EShift3,
    ETrit,
    Expr,
)
from bt.calculus.integral import I
from bt.calculus.order import cmp3
from bt.calculus.select import select3
from bt.calculus.trit import Trit, as_trit
from bt.operators import drop_lsd_word, prepend_lsd_word
from bt.representation import BalancedTernary, WordLike, decode, digits, normalize


def evaluate(expr: Expr) -> int:
    """Exact integer evaluation."""
    if isinstance(expr, EInt):
        return expr.value
    if isinstance(expr, ETrit):
        return int(expr.value)
    if isinstance(expr, EAdd):
        return evaluate(expr.left) + evaluate(expr.right)
    if isinstance(expr, EMul):
        return evaluate(expr.left) * evaluate(expr.right)
    if isinstance(expr, ENeg):
        return -evaluate(expr.arg)
    if isinstance(expr, ED):
        return D(evaluate(expr.arg))
    if isinstance(expr, EIm):
        return I(Trit.MINUS, evaluate(expr.arg))
    if isinstance(expr, EI0):
        return I(Trit.ZERO, evaluate(expr.arg))
    if isinstance(expr, EIp):
        return I(Trit.PLUS, evaluate(expr.arg))
    if isinstance(expr, EShift3):
        return 3 * evaluate(expr.arg)
    if isinstance(expr, ENormalize):
        return evaluate(expr.arg)
    if isinstance(expr, ECmp3):
        return int(cmp3(evaluate(expr.left), evaluate(expr.right)))
    if isinstance(expr, ESelect3):
        return select3(
            evaluate(expr.cond),
            evaluate(expr.x_minus),
            evaluate(expr.x_zero),
            evaluate(expr.x_plus),
        )
    raise TypeError(f"unknown expression {type(expr).__name__}")


def head(word: WordLike) -> Trit:
    """Least-significant trit of a canonical word."""
    return as_trit(digits(normalize(word))[0])


def tail(word: WordLike) -> BalancedTernary:
    """Word-level derivative: drop the LSD."""
    return drop_lsd_word(word)


def derivative_word(word: WordLike) -> BalancedTernary:
    return tail(word)


def integral_word(a: Trit | int, word: WordLike) -> BalancedTernary:
    return prepend_lsd_word(word, int(as_trit(int(a))))


def decode_derivative(word: WordLike) -> int:
    """``decode(derivative(w)) = D(decode(w))``."""
    return decode(derivative_word(word))


def decode_integral(a: Trit | int, word: WordLike) -> int:
    """``decode(integral_a(w)) = I_a(decode(w))``."""
    return decode(integral_word(a, word))


def integer_word_commute_D(n: int) -> bool:
    from bt.representation import encode

    return decode_derivative(encode(n)) == D(n)


def integer_word_commute_I(a: Trit | int, n: int) -> bool:
    from bt.representation import encode

    return decode_integral(a, encode(n)) == I(a, n)


def lsd_matches_head(n: int) -> bool:
    from bt.representation import encode

    return lsd(n) == head(encode(n))
