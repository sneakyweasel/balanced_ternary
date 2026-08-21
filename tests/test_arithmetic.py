"""Tests for trial-division helpers used by ``analyze``."""

from __future__ import annotations

from balanced_ternary.arithmetic import factorize, format_factorization, is_prime


def test_is_prime_edges():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(-7)
    assert not is_prime(9)
    assert not is_prime(49)


def test_factorize():
    assert factorize(0) == []
    assert factorize(1) == []
    assert factorize(-1) == []
    assert factorize(42) == [(2, 1), (3, 1), (7, 1)]
    assert factorize(-12) == [(2, 2), (3, 1)]
    assert format_factorization(42) == "2 * 3 * 7"
    assert format_factorization(-12) == "-1 * 2^2 * 3"
    assert format_factorization(0) == "0"
