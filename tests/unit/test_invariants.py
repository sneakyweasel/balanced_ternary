"""Executable checks of the Milestone A theorems."""

from __future__ import annotations

from balanced_ternary.arithmetic import is_prime
from balanced_ternary.features import weight
from balanced_ternary.invariants import (
    check_automaton_residue,
    check_parity,
    check_v3_identity,
    lsd_nonzero_index,
    v3,
    verify_invariants,
)
from balanced_ternary.representation import digits, encode


def test_v3_of_zero_is_infinity():
    assert v3(0) is None
    assert lsd_nonzero_index(encode(0)) is None


def test_v3_matches_dividing_out_threes():
    samples = [
        1,
        -1,
        2,
        3,
        -3,
        9,
        -9,
        27,
        42,
        81,
        162,
        5 * 9,
        -(3**8),
        3**10 * 7,
    ]
    for n in samples:
        assert check_v3_identity(n)
        expected = 0
        m = abs(n)
        while m % 3 == 0:
            m //= 3
            expected += 1
        assert v3(n) == expected
        assert lsd_nonzero_index(encode(n)) == expected


def test_parity_and_v3_million():
    """n ≡ w(n) (mod 2) and v3 identity on [-10^6, 10^6]."""
    for n in range(-1_000_000, 1_000_001):
        word = encode(n)
        if not check_parity(n, word):
            raise AssertionError(f"parity failed at n={n}")
        if not check_v3_identity(n, word):
            raise AssertionError(f"v3 failed at n={n}")


def test_odd_primes_have_odd_weight():
    for n in range(3, 5000, 2):
        if is_prime(n):
            assert weight(encode(n)) % 2 == 1


def test_primes_other_than_three_have_nonzero_last_digit():
    for n in range(2, 5000):
        if is_prime(n) and n != 3:
            assert digits(encode(n))[0] != 0
            assert v3(n) == 0


def test_verify_invariants_helper_small():
    report = verify_invariants(200, moduli=(2, 3, 5, 7))
    assert report.ok
    assert report.checked == 401


def test_automaton_matches_integer_mod_on_range():
    moduli = (2, 3, 4, 5, 7, 9, 11, 13)
    for n in range(-20_000, 20_001):
        word = encode(n)
        for q in moduli:
            if not check_automaton_residue(n, q, word):
                raise AssertionError(f"automaton residue failed n={n} q={q}")


def test_automaton_on_noncanonical_words():
    from automata.modular import ModularAutomaton

    assert ModularAutomaton(7).residue("00+") == 1 % 7
    assert ModularAutomaton(7).residue("+") == 1 % 7
    # 19 = "+-0+"
    assert encode(19).word() == "+-0+"
    assert ModularAutomaton(7).residue("+-0+") == 19 % 7
