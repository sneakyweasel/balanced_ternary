"""Tests for LSD doubling, /2, /2^k, and the odd-part map."""

from __future__ import annotations

import pytest

from bt.representation import decode, encode
from research.collatz.core import collatz_step
from research.collatz.theorems import append_plus
from bt.transducers.divide_by_two import (
    DivideByTwoTransducer,
    LeftoverCarryError,
    apply_even,
)
from bt.transducers.divide_by_two_power import (
    DivideByTwoPowerTransducer,
    apply_divisible,
)
from bt.transducers.doubling import apply_double
from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.valuation import v2


def test_doubling_matches_integer():
    for n in range(-400, 401):
        assert decode(apply_double(encode(n))) == 2 * n
        assert apply_double(encode(n)) == encode(2 * n)


def test_divide_by_two_inverts_doubling_on_evens():
    trans = DivideByTwoTransducer()
    for n in range(-400, 401):
        doubled = apply_double(encode(n))
        half = trans.apply_even(doubled)
        assert decode(half) == n
        assert half == encode(n)


def test_apply_even_rejects_odds():
    with pytest.raises(LeftoverCarryError):
        apply_even(encode(1))
    with pytest.raises(LeftoverCarryError):
        apply_even(encode(27))


def test_divide_by_two_power():
    for k in range(1, 6):
        machine = DivideByTwoPowerTransducer(k)
        for n in range(-200, 201):
            x = n * (1 << k)
            got = machine.apply(encode(x))
            assert decode(got) == n
            assert got == encode(n)
        report = machine.complexity_report()
        assert report["naive_bound"] == 3**k
        assert 1 <= report["reachable"] <= report["naive_bound"]
        assert 1 <= report["minimized"] <= report["reachable"]


def test_odd_part_word():
    assert odd_part_word(encode(0)) == encode(0)
    assert odd_part_word(encode(16)) == encode(1)
    assert odd_part_word(encode(82)) == encode(41)
    for n in range(-300, 301):
        if n == 0:
            continue
        k = v2(n)
        assert k is not None
        assert decode(odd_part_word(encode(n))) == n // (1 << k) if n > 0 else -((-n) // (1 << k))
        # exact: n / 2^k toward zero? For negatives, n >> k is arithmetic in Python
        # for negative n, n is even when k>=1; n // 2^k is floor. v2 uses abs.
        odd = n // (1 << k) if n % (1 << k) == 0 else None
        assert odd is not None
        # Python // on negatives floors. -10 / 2 = -5. Good.
        # -12 v2=2, -12/4 = -3. encode matches.
        assert decode(odd_part_word(encode(n))) == n // (1 << k)


def test_odd_part_of_powers_of_two_is_one():
    """Consistency with the FST-boundary setup, not a regularity proof."""
    for j in range(0, 24):
        assert odd_part_word(encode(1 << j)) == encode(1)


def test_odd_part_of_append_plus_is_T():
    for n in range(1, 500, 2):
        w = encode(n)
        assert odd_part_word(append_plus(w)) == encode(collatz_step(n))


def test_apply_divisible_rejects_insufficient_valuation():
    with pytest.raises(ValueError):
        apply_divisible(encode(6), 3)  # v2(6)=1
