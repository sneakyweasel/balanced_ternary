"""Tests for J, unique zero-lift k, and the dichotomy."""

from __future__ import annotations

from itertools import product

from collatz.automata.valuation_shift import growth_budget
from collatz.core import collatz_valuation
from collatz.min_realizer import min_realizer
from collatz.zero_lift import (
    J_along,
    ZeroLiftState,
    all_zero_J_words_are_twos,
    dichotomy_report,
    expanding_word_has_positive_J,
    finite_J_certificate,
    lift_J,
    zero_lift_k,
    zero_lift_trace,
)


def test_J_is_nonnegative_integer_lift():
    for ks in product(range(1, 4), repeat=3):
        js = J_along(ks)
        rs = [min_realizer(ks[:i]) for i in range(len(ks) + 1)]
        for i, j in enumerate(js):
            assert j >= 0
            mod = 1 << (sum(ks[:i]) + 1)
            assert rs[i + 1] == rs[i] + j * mod
            assert lift_J(ks[:i], ks[i]) == j


def test_unique_zero_lift_k():
    for m in range(0, 4):
        words = ((),) if m == 0 else product(range(1, 4), repeat=m)
        for ks in words:
            ks = tuple(ks)
            k = zero_lift_k(ks)
            assert k >= 1
            assert lift_J(ks, k) == 0
            r_p = min_realizer(ks)
            r_c = min_realizer(ks + (k,))
            assert r_c == r_p
            for j in range(1, 6):
                if j == k:
                    continue
                assert lift_J(ks, j) >= 1


def test_empty_zero_lift_is_the_one_cycle():
    assert zero_lift_k(()) == 2
    tr = zero_lift_trace((), steps=6)
    assert all(s.R == 1 for s in tr)
    assert all(s.successor_k() == 2 for s in tr[:-1]) or all(
        st.prefix == (2,) * st.m for st in tr
    )
    assert tr[3].prefix == (2, 2, 2)


def test_all_zero_J_iff_all_twos():
    assert all_zero_J_words_are_twos((2, 2, 2))
    assert all_zero_J_words_are_twos((1,))
    assert J_along((2, 2, 2)) == (0, 0, 0)
    assert not all(j == 0 for j in J_along((1,)))
    assert J_along((1,))[0] > 0


def test_expanding_has_positive_J():
    for m in range(1, 5):
        for ks in product(range(1, 4), repeat=m):
            if growth_budget(ks).kind == "expanding":
                assert expanding_word_has_positive_J(ks)
                assert any(j > 0 for j in J_along(ks))


def test_dichotomy_sample_agrees_with_R():
    rep = dichotomy_report((2, 2, 2))
    assert rep.all_J_zero
    assert rep.R[-1] == rep.R[0]
    rep1 = dichotomy_report((1, 1, 1))
    assert not rep1.all_J_zero
    assert rep1.R[-1] > rep1.R[0]


def test_zero_lift_state_from_three():
    st = ZeroLiftState.from_prefix((1,))
    assert st.R == 3
    assert st.x == 5
    assert st.successor_k() == collatz_valuation(5)
    nxt = st.step()
    assert nxt.R == 3
    assert lift_J((1,), nxt.prefix[-1]) == 0


def test_finite_J_certificate_exact_below_precision():
    # Empty canonical state is x=1 and v2(3x+1)=2.
    assert finite_J_certificate((), 2, 3).result == "CERTIFIED_ZERO"
    assert finite_J_certificate((), 1, 3).result == "CERTIFIED_POSITIVE"
    assert finite_J_certificate((), 3, 3).result == "CERTIFIED_POSITIVE"


def test_finite_J_certificate_at_least_precision():
    # At precision 2, 3*1+1 is 0 mod 4, so only valuation >= 2 is visible.
    assert finite_J_certificate((), 1, 2).result == "CERTIFIED_POSITIVE"
    assert finite_J_certificate((), 2, 2).result == "UNRESOLVED"
    assert finite_J_certificate((), 5, 2).result == "UNRESOLVED"


def test_finite_J_certificates_are_sound_on_bounded_words():
    for m in range(4):
        words = ((),) if m == 0 else product(range(1, 4), repeat=m)
        for parent in words:
            parent = tuple(parent)
            for j in range(1, 6):
                cert = finite_J_certificate(parent, j, precision=3)
                if cert.result == "CERTIFIED_ZERO":
                    assert lift_J(parent, j) == 0
                elif cert.result == "CERTIFIED_POSITIVE":
                    assert lift_J(parent, j) > 0
