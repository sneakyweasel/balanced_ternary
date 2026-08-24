"""Exact D / I / projection / differential identities."""

from __future__ import annotations

import random

import pytest

from bt.calculus.derivative import D, D_k, S, digit_at, lsd, reconstruct
from bt.calculus.differential import D_of_product, D_of_sum, lsd_of_product, lsd_of_sum, product_expansion
from bt.calculus.integral import I, I_minus, I_plus, I_zero, P, section_holds
from bt.calculus.semantics import (
    decode_derivative,
    decode_integral,
    integer_word_commute_D,
    integer_word_commute_I,
    lsd_matches_head,
)
from bt.calculus.trit import Trit
from bt.operators import lsd_digit, recovered_digits
from bt.representation import encode


@pytest.mark.slow
def test_decomposition_million():
    for n in range(-1_000_000, 1_000_001):
        assert reconstruct(n) == n
        assert n == int(lsd(n)) + 3 * D(n)
        assert D(S(n)) == n
        assert S(D(n)) == n - lsd_digit(n)


def test_integrals_and_projections():
    for n in range(-20_000, 20_001):
        for a in (-1, 0, 1):
            assert D(I(a, n)) == n
            assert integer_word_commute_I(a, n)
        assert I_zero(n) == S(n)
        assert I_minus(n) == 3 * n - 1
        assert I_plus(n) == 3 * n + 1
        assert integer_word_commute_D(n)
        assert lsd_matches_head(n)
        assert decode_derivative(encode(n)) == D(n)
        a0 = lsd_digit(n)
        assert section_holds(a0, n)
        assert I(a0, D(n)) == n
        for a in (-1, 0, 1):
            if a != a0:
                assert I(a, D(n)) != n
            assert P(a, P(0, n)) == P(a, n)
            assert P(a, P(1, n)) == P(a, n)
            assert P(a, P(-1, n)) == P(a, n)
            assert D(P(a, n)) == D(n)


def test_digit_at_recovers_word():
    for n in range(-2000, 2001):
        rec = recovered_digits(n)
        for k, digit in enumerate(rec):
            assert int(digit_at(n, k)) == digit
        assert D_k(n, len(rec) if n != 0 else 0) == 0 or n == 0


def test_sum_and_product_rules():
    rng = random.Random(13)
    for x in range(-200, 201):
        for y in range(-200, 201):
            assert D(x + y) == D_of_sum(x, y)
            assert lsd(x + y) == lsd_of_sum(x, y)
            assert D(x * y) == D_of_product(x, y)
            assert lsd(x * y) == lsd_of_product(x, y)
            assert x * y == product_expansion(x, y)
    for _ in range(400):
        x = rng.randint(-10**6, 10**6)
        y = rng.randint(-10**6, 10**6)
        assert D(x + y) == D_of_sum(x, y)
        assert D(x * y) == D_of_product(x, y)
        assert x * y == product_expansion(x, y)
