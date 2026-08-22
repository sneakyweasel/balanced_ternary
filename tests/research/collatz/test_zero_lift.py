"""Tests for lift digits, unique zero-lift k, and the dichotomy."""

from __future__ import annotations

from itertools import product

from collatz.automata.valuation_shift import growth_budget
from collatz.core import collatz_valuation
from collatz.min_realizer import min_realizer
from collatz.zero_lift import (
    ZeroLiftState,
    all_zero_lift_words_are_twos,
    dichotomy_report,
    expanding_word_has_positive_lift,
    finite_lift_certificate,
    lift_digit,
    lift_digits,
    zero_lift_k,
    zero_lift_trace,
)


def test_lift_digit_is_nonnegative_integer_lift():
    for ks in product(range(1, 4), repeat=3):
        digits = lift_digits(ks)
        rs = [min_realizer(ks[:i]) for i in range(len(ks) + 1)]
        for i, t in enumerate(digits):
            assert t >= 0
            mod = 1 << (sum(ks[:i]) + 1)
            assert rs[i + 1] == rs[i] + t * mod
            assert lift_digit(ks[:i], ks[i]) == t


def test_unique_zero_lift_k():
    for m in range(0, 4):
        words = ((),) if m == 0 else product(range(1, 4), repeat=m)
        for ks in words:
            ks = tuple(ks)
            k = zero_lift_k(ks)
            assert k >= 1
            assert lift_digit(ks, k) == 0
            r_p = min_realizer(ks)
            r_c = min_realizer(ks + (k,))
            assert r_c == r_p
            for j in range(1, 6):
                if j == k:
                    continue
                assert lift_digit(ks, j) >= 1


def test_empty_zero_lift_is_the_one_cycle():
    assert zero_lift_k(()) == 2
    tr = zero_lift_trace((), steps=6)
    assert all(s.R == 1 for s in tr)
    assert all(s.successor_k() == 2 for s in tr[:-1]) or all(
        st.prefix == (2,) * st.m for st in tr
    )
    assert tr[3].prefix == (2, 2, 2)


def test_all_zero_J_iff_all_twos():
    assert all_zero_lift_words_are_twos((2, 2, 2))
    assert all_zero_lift_words_are_twos((1,))
    assert lift_digits((2, 2, 2)) == (0, 0, 0)
    assert not all(t == 0 for t in lift_digits((1,)))
    assert lift_digits((1,))[0] > 0


def test_expanding_has_positive_lift():
    for m in range(1, 5):
        for ks in product(range(1, 4), repeat=m):
            if growth_budget(ks).kind == "expanding":
                assert expanding_word_has_positive_lift(ks)
                assert any(t > 0 for t in lift_digits(ks))


def test_dichotomy_sample_agrees_with_R():
    rep = dichotomy_report((2, 2, 2))
    assert rep.all_lifts_zero
    assert rep.R[-1] == rep.R[0]
    rep1 = dichotomy_report((1, 1, 1))
    assert not rep1.all_lifts_zero
    assert rep1.R[-1] > rep1.R[0]


def test_zero_lift_state_from_three():
    st = ZeroLiftState.from_prefix((1,))
    assert st.R == 3
    assert st.x == 5
    assert st.successor_k() == collatz_valuation(5)
    nxt = st.step()
    assert nxt.R == 3
    assert lift_digit((1,), nxt.prefix[-1]) == 0


def test_finite_lift_certificate_exact_below_precision():
    # Empty canonical state is x=1 and v2(3x+1)=2.
    assert finite_lift_certificate((), 2, 3).result == "CERTIFIED_ZERO"
    assert finite_lift_certificate((), 1, 3).result == "CERTIFIED_POSITIVE"
    assert finite_lift_certificate((), 3, 3).result == "CERTIFIED_POSITIVE"


def test_finite_lift_certificate_at_least_precision():
    # At precision 2, 3*1+1 is 0 mod 4, so only valuation >= 2 is visible.
    assert finite_lift_certificate((), 1, 2).result == "CERTIFIED_POSITIVE"
    assert finite_lift_certificate((), 2, 2).result == "UNRESOLVED"
    assert finite_lift_certificate((), 5, 2).result == "UNRESOLVED"


def test_finite_lift_certificates_are_sound_on_bounded_words():
    for m in range(4):
        words = ((),) if m == 0 else product(range(1, 4), repeat=m)
        for parent in words:
            parent = tuple(parent)
            for j in range(1, 6):
                cert = finite_lift_certificate(parent, j, precision=3)
                if cert.result == "CERTIFIED_ZERO":
                    assert lift_digit(parent, j) == 0
                elif cert.result == "CERTIFIED_POSITIVE":
                    assert lift_digit(parent, j) > 0
