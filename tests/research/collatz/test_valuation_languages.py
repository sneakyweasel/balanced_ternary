"""Tests for regular valuation-class languages L_k."""

from __future__ import annotations

import pytest

from bt.representation import encode
from research.collatz.transducers.valuation_languages import ValuationClassDFA
from research.collatz.valuation import v2


def test_dfa_rejects_bad_k():
    with pytest.raises(ValueError):
        ValuationClassDFA(-1)


def test_l0_is_odds():
    dfa = ValuationClassDFA(0)
    for n in range(-500, 501):
        assert dfa.accepts(encode(n)) == (n % 2 != 0)


def test_lk_matches_v2():
    for k in range(0, 7):
        dfa = ValuationClassDFA(k)
        for n in range(-800, 801):
            if n == 0:
                assert not dfa.accepts(encode(0))
                continue
            assert dfa.accepts(encode(n)) == (v2(n) == k)


def test_accept_states_are_residues_of_exact_valuation():
    dfa = ValuationClassDFA(3)
    states = dfa.accept_states()
    assert all(v2(r) == 3 for r in states)
    assert 8 in states  # 8 = 2^3, v2=3, 8 mod 16 = 8, precision k+1=4
    assert 0 not in states
