"""Tests for the accelerated Collatz core and ternary 3n+1 arithmetic."""

from __future__ import annotations

import pytest

from bt.representation import decode, encode
from bt.arithmetic import (
    add,
    add_one,
    lsd_add_one_case,
    multiply_by_three,
    three_n_plus_one_word,
)
from research.collatz.core import (
    collatz_step,
    collatz_valuation,
    standard_collatz_step,
    three_n_plus_one,
)
from research.collatz.valuation import v2


def test_standard_vs_accelerated_distinction():
    assert standard_collatz_step(5) == 16
    assert standard_collatz_step(16) == 8
    assert collatz_step(5) == 1
    assert collatz_valuation(5) == 4
    assert three_n_plus_one(5) == 16


def test_known_accelerated_steps():
    assert collatz_step(1) == 1
    assert collatz_valuation(1) == 2
    assert collatz_step(3) == 5
    assert collatz_step(5) == 1
    assert collatz_step(7) == 11
    assert collatz_step(9) == 7
    assert collatz_step(27) == 41


def test_T_always_odd_positive():
    for n in range(1, 5000, 2):
        t = collatz_step(n)
        assert t >= 1 and t % 2 == 1
        y = 3 * n + 1
        k = v2(y)
        assert k is not None and k >= 1
        assert t == y // (1 << k)
        assert y % (1 << k) == 0
        if k + 1 < 64:
            assert y % (1 << (k + 1)) != 0 or y == 0


def test_rejects_even_and_nonpositive():
    with pytest.raises(ValueError):
        collatz_step(2)
    with pytest.raises(ValueError):
        collatz_step(0)
    with pytest.raises(ValueError):
        collatz_step(-3)
    with pytest.raises(TypeError):
        collatz_step(True)  # type: ignore[arg-type]


def test_multiply_by_three_is_digit_shift():
    for n in range(-200, 201):
        word = encode(n)
        shifted = multiply_by_three(word)
        assert decode(shifted) == 3 * n
        if n != 0:
            assert shifted.word() == word.word() + "0"


def test_add_one_trailing_cases():
    assert lsd_add_one_case(encode(3)) == "trailing_zero"  # "+0"
    assert add_one(encode(3)) == encode(4)
    assert lsd_add_one_case(encode(1)) == "trailing_plus"  # "+"
    assert add_one(encode(1)) == encode(2)
    assert lsd_add_one_case(encode(2)) == "trailing_minus"  # "+-"
    assert add_one(encode(2)) == encode(3)
    # carry through a trailing plus: 4 = "++"
    assert encode(4).word()[-1] == "+"
    assert add_one(encode(4)) == encode(5)


def test_add_matches_integer_addition():
    samples = list(range(-80, 81)) + [3**k for k in range(8)] + [-(3**k) for k in range(8)]
    for a in samples:
        for b in (-2, -1, 0, 1, 2, 5, 9):
            assert decode(add(encode(a), encode(b))) == a + b


def test_three_n_plus_one_via_ternary():
    for n in range(-200, 201):
        word = encode(n)
        assert three_n_plus_one_word(word) == encode(3 * n + 1)
        assert decode(three_n_plus_one_word(word)) == 3 * n + 1
