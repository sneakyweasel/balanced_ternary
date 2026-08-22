"""Rewrite soundness on small integers and operator words."""

from __future__ import annotations

from bt.calculus.expressions import ED, EI0, EIm, EInt, EIp, ENeg, EShift3
from bt.calculus.normalization import normal_form, normalize_expr
from bt.calculus.rewrite import REWRITE_RULES, rewrite_expr, rewrite_word
from bt.calculus.semantics import evaluate


def test_word_rules_include_legacy_identities():
    reasons = {reason for _src, _dst, reason in REWRITE_RULES}
    assert "D∘S = id" in reasons
    assert "W∘W = K3 (strip factors of 3)" in reasons
    word, used = rewrite_word(("W", "W"))
    assert word == ("K3",)
    ds, _ = rewrite_word(("D", "S"))
    assert ds == ()
    i0, _ = rewrite_word(("I0",))
    assert i0 == ("S",)


def test_tree_rewrite_operator_fragment():
    n = 7
    x = EInt(n)
    expr = ED(EIp(ED(EIm(x))))
    nf, reasons, _steps = rewrite_expr(expr)
    # D(I+(D(I-(x)))) = D(I+(x)) = x, not D(x).
    assert nf == x
    assert evaluate(expr) == evaluate(nf) == n
    nn = ENeg(ENeg(EShift3(x)))
    assert normal_form(nn) == EShift3(x)
    assert evaluate(EI0(x)) == evaluate(EShift3(x))
    swapped = ENeg(EShift3(x))
    assert normal_form(swapped) == EShift3(ENeg(x))
    assert evaluate(swapped) == evaluate(normal_form(swapped))


def test_rewrite_sound_on_small_integers():
    for n in range(-200, 201):
        x = EInt(n)
        pairs = [
            (ED(EIm(x)), x),
            (ED(EIp(x)), x),
            (ED(EI0(x)), x),
            (ED(EShift3(x)), x),
            (ENeg(ENeg(x)), x),
            (ENeg(EShift3(x)), EShift3(ENeg(x))),
            (ENeg(EIm(x)), EIp(ENeg(x))),
            (ENeg(EIp(x)), EIm(ENeg(x))),
            (EI0(x), EShift3(x)),
        ]
        for left, right in pairs:
            nf_l, _, _ = normalize_expr(left)
            nf_r, _, _ = normalize_expr(right)
            assert evaluate(left) == evaluate(right)
            assert evaluate(nf_l) == evaluate(left)
            assert evaluate(nf_r) == evaluate(right)
