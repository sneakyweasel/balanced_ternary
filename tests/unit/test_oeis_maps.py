"""OEIS fixtures and exact word-map identities."""

from __future__ import annotations

from bt.metrics import v3
from bt.sequences import (
    A065363_EXAMPLES,
    A065363_PREFIX,
    A065364_EXAMPLES,
    A065364_PREFIX,
    A134028_EXAMPLES,
    A134028_PREFIX,
    A160652_EXAMPLES,
    A160652_PREFIX,
    A351702_EXAMPLES,
    A351702_PREFIX,
    bt_alternating_digit_sum,
    bt_digit_sum,
    bt_is_palindrome,
    bt_length,
    bt_reverse,
    bt_reverse_tail,
    bt_reverse_zeros,
    reverse_is_involution,
)
from bt.representation import encode
from research.collatz.theorems import append_plus


def test_a134028_prefix_and_examples():
    for n, expected in enumerate(A134028_PREFIX):
        assert bt_reverse(n) == expected
    for n, expected in A134028_EXAMPLES:
        assert bt_reverse(n) == expected


def test_a351702_prefix_and_examples():
    for n, expected in enumerate(A351702_PREFIX):
        assert bt_reverse_tail(n) == expected
    for n, expected in A351702_EXAMPLES:
        assert bt_reverse_tail(n) == expected


def test_a160652_prefix_and_examples():
    for n, expected in enumerate(A160652_PREFIX):
        assert bt_reverse_zeros(n) == expected
    for n, expected in A160652_EXAMPLES:
        assert bt_reverse_zeros(n) == expected


def test_a065363_prefix_and_examples():
    for n, expected in enumerate(A065363_PREFIX):
        assert bt_digit_sum(n) == expected
    for n, expected in A065363_EXAMPLES:
        assert bt_digit_sum(n) == expected


def test_a065364_prefix_and_examples():
    for n, expected in enumerate(A065364_PREFIX, start=1):
        assert bt_alternating_digit_sum(n) == expected
    for n, expected in A065364_EXAMPLES:
        assert bt_alternating_digit_sum(n) == expected


def test_length_matches_canonical_word():
    for n in range(-80, 81):
        assert bt_length(n) == len(encode(n))


def test_sign_commutes_with_reverse_and_tail():
    for n in range(-80, 81):
        assert bt_reverse(-n) == -bt_reverse(n)
        assert bt_reverse_tail(-n) == -bt_reverse_tail(n)
        assert bt_reverse_zeros(-n) == -bt_reverse_zeros(n)
        assert bt_digit_sum(-n) == -bt_digit_sum(n)
        assert bt_is_palindrome(-n) == bt_is_palindrome(n)


def test_involution_criterion_and_companions():
    for n in range(-400, 401):
        restored = bt_reverse(bt_reverse(n))
        assert (restored == n) == reverse_is_involution(n)
        assert reverse_is_involution(n) == (n == 0 or n % 3 != 0)
        assert bt_reverse_zeros(bt_reverse_zeros(n)) == n
        assert bt_reverse_tail(bt_reverse_tail(n)) == n
        if n != 0:
            assert bt_reverse_zeros(n) == bt_reverse(n) * (3 ** v3(n))
        if bt_is_palindrome(n):
            assert bt_reverse(n) == n


def test_w_of_three_power_times_n_equals_w_n():
    for n in range(-40, 41):
        if n == 0:
            continue
        for m in range(0, 6):
            assert bt_reverse(n * (3 ** m)) == bt_reverse(n)
            assert bt_reverse_zeros(n * (3 ** m)) == bt_reverse_zeros(n) * (3 ** m)


def test_w_three_n_is_not_three_w_n():
    assert bt_reverse(3) != 3 * bt_reverse(1)
    assert bt_reverse(3 * 1) == 1
    assert 3 * bt_reverse(1) == 3


def test_digit_sum_recurrences_and_append_plus():
    for n in range(-200, 201):
        if n == 0:
            continue
        assert bt_digit_sum(3 * n) == bt_digit_sum(n)
        assert bt_digit_sum(3 * n + 1) == bt_digit_sum(n) + 1
        assert bt_digit_sum(3 * n - 1) == bt_digit_sum(n) - 1
        assert len(append_plus(encode(n))) == bt_length(n) + 1
        assert bt_length(3 * n + 1) == bt_length(n) + 1


def test_length_can_drop_under_reverse():
    assert bt_length(abs(bt_reverse(21))) < bt_length(21)
    for n in range(0, 200):
        assert bt_length(abs(bt_reverse(n))) <= bt_length(n)
