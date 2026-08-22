"""Pinned smallest witnesses. Do not weaken or delete."""

from __future__ import annotations

from bt.operators import digit_derivative, get_operator
from bt.sequences import bt_reverse
from research.collatz.asymptotic import N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE
from research.collatz.core import collatz_step
from research.collatz.dual_code import CollatzDualCode, lift_digit_formula
from research.collatz.warp import preserved_counterexamples


def test_W_of_three_is_one_and_not_involutive():
    W = get_operator("W")
    assert W.apply(3) == 1
    assert bt_reverse(3) == 1
    assert W.apply(W.apply(3)) == 1 != 3


def test_W_three_n_fails_at_one():
    assert bt_reverse(3) != 3 * bt_reverse(1)


def test_W_does_not_commute_with_T_at_three():
    assert bt_reverse(collatz_step(3)) != collatz_step(bt_reverse(3))


def test_digit_derivative_is_not_floor_division():
    assert digit_derivative(2) == 1
    assert 2 // 3 == 0


def test_BT_R_suffix_does_not_determine_next_valuation():
    a = CollatzDualCode.from_valuations((1,))
    b = CollatzDualCode.from_valuations((1, 4))
    assert a.R == b.R == 3
    assert a.balanced_ternary_R == b.balanced_ternary_R == "+0"
    assert a.endpoints[-1] != b.endpoints[-1]
    assert lift_digit_formula((1,), 2) != lift_digit_formula((1, 4), 2)


def test_n_star_le_n_smallest_counterexample_is_165():
    assert N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE["n"] == 165
    assert N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE["m"] == 17


def test_warp_module_preserves_naive_counterexamples():
    rows = preserved_counterexamples()
    assert rows["W_W_equals_id"]["counterexample"] == 3
    assert rows["W_3n_equals_3_W_n"]["counterexample"] == 1
    assert rows["W_T_equals_T_W"]["counterexample"] == 3
