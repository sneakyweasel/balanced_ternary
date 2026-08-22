"""Tests for the single-modulus residue automaton."""

from __future__ import annotations

import pytest

from automata.modular import ALPHABET, ModularAutomaton
from balanced_ternary.representation import decode, encode


def test_modulus_must_be_at_least_two():
    with pytest.raises(ValueError):
        ModularAutomaton(1)
    with pytest.raises(ValueError):
        ModularAutomaton(0)
    with pytest.raises(ValueError):
        ModularAutomaton(True)  # type: ignore[arg-type]


def test_transition_formula():
    auto = ModularAutomaton(7)
    for r in range(7):
        for a in ALPHABET:
            assert auto.transition(r, a) == (3 * r + a) % 7


def test_run_includes_start_state():
    auto = ModularAutomaton(5)
    path = auto.run("+--")  # 5
    assert path[0] == 0
    assert path[-1] == 5 % 5
    assert len(path) == len("+--") + 1


def test_is_divisible():
    auto = ModularAutomaton(5)
    assert auto.is_divisible(encode(5))
    assert not auto.is_divisible(encode(7))
    assert auto.is_divisible(encode(0))


def test_transition_table_and_reachable():
    auto = ModularAutomaton(4)
    table = auto.transition_table()
    assert set(table) == {0, 1, 2, 3}
    assert table[0][1] == 1
    assert table[0][-1] == 3  # -1 % 4
    reachable = auto.reachable_states()
    assert 0 in reachable
    # From 0, digits ±1,0 reach 0, 1, and q-1 at least.
    assert reachable == frozenset(range(4)) or 0 in reachable


def test_minimize_deferred():
    with pytest.raises(NotImplementedError):
        ModularAutomaton(5).minimize()


def test_residue_equals_decode_mod_q_random_moduli():
    moduli = (2, 3, 5, 7, 11, 17, 29, 81)
    values = (
        list(range(-500, 501))
        + [3**k for k in range(12)]
        + [-(3**k) for k in range(12)]
        + [10**6, -(10**6), 2**20, -(2**20)]
    )
    for n in values:
        word = encode(n)
        decoded = decode(word)
        assert decoded == n
        for q in moduli:
            assert ModularAutomaton(q).residue(word) == decoded % q
