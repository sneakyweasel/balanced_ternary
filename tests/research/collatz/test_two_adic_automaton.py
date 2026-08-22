"""Tests for TwoAdicDigitAutomaton(K)."""

from __future__ import annotations

import pytest

from automata.modular import ModularAutomaton
from balanced_ternary.representation import decode, encode
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.valuation import v2


def test_precision_and_modulus():
    auto = TwoAdicDigitAutomaton(8)
    assert auto.precision == 8
    assert auto.modulus == 256
    with pytest.raises(ValueError):
        TwoAdicDigitAutomaton(0)


def test_residue_equals_integer_mod_power_of_two():
    values = (
        list(range(-800, 801))
        + [3**k for k in range(10)]
        + [-(3**k) for k in range(10)]
        + [2**20, -(2**20), 5**8]
    )
    for precision in (1, 2, 3, 5, 8, 10):
        auto = TwoAdicDigitAutomaton(precision)
        inner = ModularAutomaton(auto.modulus)
        for n in values:
            word = encode(n)
            got = auto.residue(word)
            assert got == n % auto.modulus
            assert got == decode(word) % auto.modulus
            assert got == inner.residue(word)


def test_noncanonical_words():
    auto = TwoAdicDigitAutomaton(5)
    assert auto.residue("00+") == 1 % 32
    assert auto.residue("+") == 1


def test_run_starts_at_zero():
    auto = TwoAdicDigitAutomaton(4)
    path = auto.run(encode(27))
    assert path[0] == 0
    assert path[-1] == 27 % 16


def test_odd_partition_covers_odd_residues():
    for precision in range(1, 9):
        auto = TwoAdicDigitAutomaton(precision)
        part = auto.valuation_partition()
        odd = set(auto.odd_states())
        covered = set()
        for states in part.values():
            covered.update(states)
        assert covered == odd
        assert all(r % 2 == 1 for r in covered)


def test_partition_agrees_with_direct_v2():
    for precision in range(2, 8):
        auto = TwoAdicDigitAutomaton(precision)
        for r in auto.odd_states():
            cls = auto.classify_state(r)
            actual = v2(3 * r + 1)
            assert actual is not None
            if cls.is_exact:
                assert actual == cls.exact_k
                assert actual < precision
            else:
                assert actual >= precision


def test_known_mod4_partition():
    auto = TwoAdicDigitAutomaton(2)
    part = auto.valuation_partition()
    # n ≡ 3 (mod 4) => v2(3n+1) = 1; n ≡ 1 (mod 4) => v2 >= 2
    assert 3 in part["1"]
    assert 1 in part["AT_LEAST_K"]
